# Ask 模式规则（仅保留非显而易见信息）

- 用户若问“为什么有编辑/历史/新建按钮但打不开正确链接”，先解释该仓库使用占位符协议：`$remote$/$branch$/$path$/$file$/$template$`，并通过模板内链式 `replace` 生成最终 URL。
- repo 信息说明必须包含回退顺序：优先 `site.Params.repo.*`，缺失时读取 `data/gitremote.toml`，且会在模板里去掉 `.git` 后缀。
- “其他贡献者”来源不是 Hugo 内建数据，而是外部脚本产物 `data/git_history.json`；其键需与页面 `.File.Path`（`docs/xxx.md`）一致。
- 解释评论问题时要强调“双条件”：`comments.type` 只选供应商，真正显示仍依赖 `comments.enable` 或页面级 `comments: true`。
- 回答“新建页面模板从哪来”时，应指出 `layouts/_shortcodes/newpage-tool.html` 与 `layouts/_shortcodes/wiki.html` 都会读取 `archetypes/default.md` 并注入远端创建链接。
- 若讨论主题子模块实现，需提醒 `themes/hextra/CLAUDE.md` 仅指向 `themes/hextra/AGENTS.md`，主题内部改动应以该规则为准。