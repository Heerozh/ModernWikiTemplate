# Debug 模式规则（仅保留非显而易见信息）

- 页面底部“其他贡献者”为空时，先检查 `data/git_history.json` 是否存在且键名是 `.File.Path` 形态（`docs/xxx.md`）；若写成 `content/docs/xxx.md` 会静默匹配失败。
- `scripts/gen-git-history.sh` 在“非 git 仓库 / 缺少 content 目录”场景会写入空 `{}` 并正常退出，不会抛错；排障要先看输出文件内容而非仅看退出码。
- Windows 下优先用 `hugo_dev.ps1`：它在容器内执行 `sh scripts/gen-git-history.sh`，可绕开本机缺少 `sh` 的问题。
- 评论未显示时优先排查双开关：`params.comments.enable`（或页面 `comments: true`）+ `params.comments.type`；只设置 `type=artalk` 不会渲染。
- Artalk 资源 404 常见于 `ATK_SITE_URL`/`ATK_SITE_DEFAULT` 未注入，或新增 `getenv` 变量后未加入 `hugo.toml` 的 `[security.funcs].getenv` 白名单。
- `wiki` 短代码会强制小写，含大写的页面名在“存在性判断”和真实文件路径之间容易出现错位。