#!/usr/bin/env python3
"""
在 pre-commit 中自动翻译 staged 的默认语言内容文件。

功能：
1) 仅处理 Git 暂存区中、位于默认语言 contentDir 下、且不在其他语言目录中的 Markdown 文件。
2) 将这些文件翻译到所有目标语言，并写入对应语言的 contentDir。
3) 自动 git add 生成/更新的翻译文件。

环境变量（OpenAI 兼容接口）：
- TRANSLATE_API_URL / OPENAI_BASE_URL / OPENAI_API_BASE
- TRANSLATE_API_TOKEN / OPENAI_API_KEY
- TRANSLATE_API_MODEL / OPENAI_MODEL（可选，默认 gpt-4o-mini）
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
HUGO_CONFIG_PATH = REPO_ROOT / "hugo.toml"
MARKDOWN_EXTENSIONS = {".md", ".markdown"}

LANGUAGE_NAME_FALLBACK = {
    "zh-cn": "Simplified Chinese",
    "en": "English",
    "ja": "Japanese",
    "es": "Spanish",
    "fr": "French",
    "ar": "Arabic",
    "de": "German",
    "ru": "Russian",
}

SYSTEM_PROMPT = """你是一名专业技术文档翻译助手。
请将输入的 Hugo/Markdown 文档翻译为目标语言。
必须严格遵守：
1) 保持原始格式与结构不变：front matter 分隔符、键顺序、标题层级、列表缩进、空行、表格、引用、HTML、Hugo shortcode、代码块围栏、行内代码、链接 URL、图片路径。
2) front matter 的键名、shortcode 名称、代码、URL、路径、变量名、占位符不得翻译。
3) 仅翻译自然语言文本。
4) 仅输出翻译后的完整文档，不要解释，不要添加代码围栏。"""


@dataclass
class LanguageConfig:
    key: str
    content_dir: str
    language_name: str


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def run_git(args: list[str], text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=text,
        capture_output=True,
        check=False,
    )


def strip_inline_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    out_chars: list[str] = []

    for ch in line:
        if escaped:
            out_chars.append(ch)
            escaped = False
            continue

        if ch == "\\" and in_double:
            out_chars.append(ch)
            escaped = True
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            out_chars.append(ch)
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            out_chars.append(ch)
            continue

        if ch == "#" and not in_single and not in_double:
            break

        out_chars.append(ch)

    return "".join(out_chars).strip()


def parse_toml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def normalize_rel_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./").strip("/")


def is_subpath(path: str, base: str) -> bool:
    path = normalize_rel_path(path)
    base = normalize_rel_path(base)
    return path == base or path.startswith(base + "/")


def parse_hugo_languages(config_path: Path) -> tuple[str, str, list[LanguageConfig]]:
    if not config_path.exists():
        raise RuntimeError(f"找不到配置文件: {config_path}")

    default_lang = ""
    current_section = ""
    languages: dict[str, dict[str, str]] = {}

    lines = config_path.read_text(encoding="utf-8").splitlines()
    for raw_line in lines:
        line = strip_inline_comment(raw_line)
        if not line:
            continue

        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            continue

        if "=" not in line:
            continue

        key, raw_value = line.split("=", 1)
        key = key.strip()
        value = parse_toml_scalar(raw_value)

        if not current_section and key == "defaultContentLanguage":
            default_lang = str(value).strip().lower()
            continue

        if current_section.startswith("languages.") and current_section.count(".") == 1:
            lang_key = current_section.split(".", 1)[1].strip().lower()
            lang_cfg = languages.setdefault(lang_key, {})

            if key == "contentDir":
                lang_cfg["contentDir"] = normalize_rel_path(str(value))
            elif key == "languageName":
                lang_cfg["languageName"] = str(value).strip()

    if not languages:
        raise RuntimeError("hugo.toml 中未检测到 [languages.*] 配置")

    if not default_lang:
        if "zh-cn" in languages:
            default_lang = "zh-cn"
        else:
            default_lang = next(iter(languages.keys()))

    default_cfg = languages.get(default_lang, {})
    default_content_dir = normalize_rel_path(
        default_cfg.get("contentDir", "content") or "content"
    )

    targets: list[LanguageConfig] = []
    for lang_key, cfg in languages.items():
        if lang_key == default_lang:
            continue

        content_dir = normalize_rel_path(
            cfg.get("contentDir", f"content/{lang_key}") or f"content/{lang_key}"
        )
        language_name = cfg.get("languageName") or LANGUAGE_NAME_FALLBACK.get(
            lang_key, lang_key
        )

        targets.append(
            LanguageConfig(
                key=lang_key,
                content_dir=content_dir,
                language_name=language_name,
            )
        )

    return default_lang, default_content_dir, targets


def get_staged_files() -> list[str]:
    proc = run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git diff --cached 执行失败")

    files = [
        normalize_rel_path(line) for line in proc.stdout.splitlines() if line.strip()
    ]
    return files


def collect_source_files(
    staged_files: list[str], default_content_dir: str, target_content_dirs: list[str]
) -> list[str]:
    sources: list[str] = []

    for rel_path in staged_files:
        suffix = Path(rel_path).suffix.lower()
        if suffix not in MARKDOWN_EXTENSIONS:
            continue

        if not is_subpath(rel_path, default_content_dir):
            continue

        if any(is_subpath(rel_path, d) for d in target_content_dirs):
            continue

        sources.append(rel_path)

    return sources


def read_staged_file(path: str) -> str:
    proc = run_git(["show", f":{path}"], text=False)
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="ignore").strip()
        raise RuntimeError(stderr or f"读取 staged 文件失败: {path}")

    data = proc.stdout
    if not isinstance(data, (bytes, bytearray)):
        raise RuntimeError(f"读取 staged 文件异常: {path}")

    return bytes(data).decode("utf-8-sig")


def resolve_api_endpoint(base_url: str) -> str:
    base_url = base_url.strip().rstrip("/")
    if not base_url:
        return ""
    if base_url.endswith("/chat/completions"):
        return base_url
    if base_url.endswith("/v1"):
        return base_url + "/chat/completions"
    return base_url + "/v1/chat/completions"


def resolve_api_env() -> tuple[str, str, str]:
    api_url = (
        os.getenv("TRANSLATE_API_URL")
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or ""
    )
    api_token = os.getenv("TRANSLATE_API_TOKEN") or os.getenv("OPENAI_API_KEY") or ""
    model = os.getenv("TRANSLATE_API_MODEL") or os.getenv("OPENAI_MODEL") or ""

    endpoint = resolve_api_endpoint(api_url)

    if not endpoint:
        raise RuntimeError(
            "缺少 API URL。请设置 TRANSLATE_API_URL（或 OPENAI_BASE_URL / OPENAI_API_BASE），带v1"
        )
    if not api_token:
        raise RuntimeError(
            "缺少 API Token。请设置 TRANSLATE_API_TOKEN（或 OPENAI_API_KEY）"
        )
    if not model:
        raise RuntimeError(
            "缺少 API Model。请设置 TRANSLATE_API_MODEL（或 OPENAI_MODEL），例如 deepseek-chat"
        )

    return endpoint, api_token, model


def unwrap_code_fence_if_needed(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1])
    return text


def keep_trailing_newline_like(source: str, translated: str) -> str:
    if source.endswith("\n") and not translated.endswith("\n"):
        return translated + "\n"
    if not source.endswith("\n") and translated.endswith("\n"):
        return translated.rstrip("\n")
    return translated


def translate_text(
    endpoint: str,
    token: str,
    model: str,
    source_lang: str,
    target_lang_key: str,
    target_lang_name: str,
    source_text: str,
) -> str:
    user_prompt = (
        f"源语言：{source_lang}\n"
        f"目标语言：{target_lang_name} ({target_lang_key})\n\n"
        "请翻译下面的文档，严格保持原始格式：\n"
        "---BEGIN DOCUMENT---\n"
        f"{source_text}\n"
        "---END DOCUMENT---"
    )

    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    }

    req = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=180) as resp:
            body = resp.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"翻译接口 HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"翻译接口连接失败: {exc}") from exc

    try:
        parsed = json.loads(body)
        translated = parsed["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"翻译接口返回格式异常: {body}") from exc

    if not isinstance(translated, str) or not translated.strip():
        raise RuntimeError("翻译接口返回空内容")

    translated = unwrap_code_fence_if_needed(translated)
    translated = keep_trailing_newline_like(source_text, translated)
    return translated


def read_text_exact(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text_exact(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(content)


def stage_files(paths: list[str]) -> None:
    if not paths:
        return
    proc = run_git(["add", "--", *paths])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git add 执行失败")


def main() -> int:
    try:
        default_lang, default_content_dir, targets = parse_hugo_languages(
            HUGO_CONFIG_PATH
        )
    except Exception as exc:  # noqa: BLE001
        eprint(f"[translate-hook] 读取 hugo.toml 失败: {exc}")
        return 1

    if not targets:
        print("[translate-hook] 未检测到目标语言，跳过")
        return 0

    try:
        staged_files = get_staged_files()
    except Exception as exc:  # noqa: BLE001
        eprint(f"[translate-hook] 读取 staged 文件失败: {exc}")
        return 1

    target_content_dirs = [t.content_dir for t in targets]
    source_files = collect_source_files(
        staged_files, default_content_dir, target_content_dirs
    )

    if not source_files:
        print("[translate-hook] 未发现需翻译的默认语言 content 文件，跳过")
        return 0

    try:
        endpoint, token, model = resolve_api_env()
    except Exception as exc:  # noqa: BLE001
        eprint(f"[translate-hook] 环境变量错误: {exc}")
        return 1

    print(
        "[translate-hook] 待翻译源文件: "
        + f"{len(source_files)}，目标语言: {', '.join(t.key for t in targets)}"
    )

    generated_or_updated: list[str] = []

    for src_path in source_files:
        try:
            source_text = read_staged_file(src_path)
        except Exception as exc:  # noqa: BLE001
            eprint(f"[translate-hook] 读取源文件失败 {src_path}: {exc}")
            return 1

        rel = normalize_rel_path(
            src_path[len(normalize_rel_path(default_content_dir)) :]
        )
        if not rel:
            eprint(f"[translate-hook] 源路径异常，无法计算相对路径: {src_path}")
            return 1

        for target in targets:
            target_path = normalize_rel_path(f"{target.content_dir}/{rel}")
            target_abs = REPO_ROOT / target_path

            print(
                f"[translate-hook] 翻译 {src_path} -> {target_path} ({target.language_name})"
            )
            try:
                translated = translate_text(
                    endpoint=endpoint,
                    token=token,
                    model=model,
                    source_lang=default_lang,
                    target_lang_key=target.key,
                    target_lang_name=target.language_name,
                    source_text=source_text,
                )
            except Exception as exc:  # noqa: BLE001
                eprint(f"[translate-hook] 翻译失败 {src_path} -> {target.key}: {exc}")
                return 1

            existing = ""
            if target_abs.exists():
                try:
                    existing = read_text_exact(target_abs)
                except Exception as exc:  # noqa: BLE001
                    eprint(f"[translate-hook] 读取目标文件失败 {target_path}: {exc}")
                    return 1

            if existing == translated:
                continue

            try:
                write_text_exact(target_abs, translated)
            except Exception as exc:  # noqa: BLE001
                eprint(f"[translate-hook] 写入目标文件失败 {target_path}: {exc}")
                return 1

            generated_or_updated.append(target_path)

    try:
        stage_files(generated_or_updated)
    except Exception as exc:  # noqa: BLE001
        eprint(f"[translate-hook] git add 失败: {exc}")
        return 1

    if generated_or_updated:
        print(
            f"[translate-hook] 已生成/更新并加入暂存区: {len(generated_or_updated)} 个文件"
        )
    else:
        print("[translate-hook] 翻译结果无变更")

    return 0


if __name__ == "__main__":
    sys.exit(main())
