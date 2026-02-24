# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## 作用域
- 本仓库是 ModernWiki 的 Hugo 站点模板；`themes/hextra/` 以 Git submodule 方式引入主题，根目录 `layouts/` 的同名文件会覆盖主题实现。

## 构建/测试/格式化（仅仓库特有）
- 一键构建（PowerShell）：`./hugo_dev.ps1`
  - 先在容器中执行 `scripts/gen-git-history.sh --limit 10` 生成 `data/git_history.json`
  - 再用 `hugomods/hugo:git` 输出站点到 `public/`
- 仅更新贡献历史：`sh ./scripts/gen-git-history.sh --limit 10`（通常在 Linux 环境或容器中执行）。
- 测试：仓库未配置测试框架与测试目录；不存在“单个测试”命令。
- Lint：仓库无独立 lint 脚本，仅有 Prettier 配置（见 `.prettierrc`）。

## 项目特有约束（高误踩）
- 评论渲染开关在 `layouts/_partials/components/comments.html`：`params.comments.type = "artalk"` 不会自动生效，仍需 `params.comments.enable = true`（或页面级 `comments: true`）。
- `layouts/_partials/components/artalk.html` 依赖 `ATK_SITE_URL`、`ATK_SITE_DEFAULT`；若新增模板环境变量，需同步更新 `hugo.toml` 的 `[security.funcs].getenv` 白名单。
- 编辑/历史/新建页面链接依赖占位符协议：`$remote$/$branch$/$path$/$file$/$template$`，并统一从 `site.Params.repo.*` 回退到 `data/gitremote.toml`。
- “其他贡献者”头像依赖 `data/git_history.json`；其键名必须与 `.File.Path` 对齐（例如 `docs/xxx.md`，不是 `content/docs/xxx.md`）。
- `layouts/_shortcodes/wiki.html` 会将页面参数统一小写；新页面命名若含大写，链接目标与文件路径可能不一致。
- 新建页面工具会读取 `archetypes/default.md` 并注入远端新建 URL，front matter 风格由该模板决定（当前是 TOML `+++`，可与现有 YAML 页面并存）。

## 已存在的 AI 规则来源
- `themes/hextra/CLAUDE.md` 仅指向 `themes/hextra/AGENTS.md`；若改动子模块内主题代码，需同时遵循该文件。