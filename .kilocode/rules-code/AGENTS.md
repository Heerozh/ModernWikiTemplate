# Code 模式规则（仅保留非显而易见信息）

- 评论组件开关是“双条件”：`params.comments.type` 仅决定供应商，真正渲染仍依赖 `params.comments.enable`（或页面级 `comments: true`）。
- 任何模板里新增 `getenv` 变量后，必须同步更新 `hugo.toml` 的 `[security.funcs].getenv` 白名单，否则变量会被 Hugo 安全策略拦截。
- 编辑/历史/新建页面链接依赖占位符协议（`$remote$/$branch$/$path$/$file$/$template$`）；改 URL 模板时必须保持占位符替换链完整。
- repo 信息读取遵循统一回退：`site.Params.repo.*` → `data/gitremote.toml`，且会去掉 `.git` 后缀；不要在不同模板里实现不一致逻辑。
- `data/git_history.json` 的键必须匹配 `.File.Path`（如 `docs/a.md`），不是 `content/docs/a.md`；否则“其他贡献者”会静默显示为空。
- `layouts/_shortcodes/wiki.html` 会把入参统一转小写；新页面命名含大写会导致“链接目标”与“文件路径”不一致。
- 新建页面工具把 `archetypes/default.md` 注入远端创建 URL；该模板当前是 TOML front matter（`+++`），与现有 YAML 页面可并存但改模板时需考虑兼容。