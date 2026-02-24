# Architect 模式规则（仅保留非显而易见信息）

- 链接体系采用“模板占位符协议”而非硬编码 URL：`$remote$/$branch$/$path$/$file$/$template$`。涉及编辑/历史/新建流程设计时需保证完整替换链不被破坏。
- 仓库来源配置存在统一回退策略：`site.Params.repo.*` → `data/gitremote.toml`，并在模板层统一去掉 `.git`；架构设计中应避免在多个组件重复实现不同分支逻辑。
- 页面贡献者信息是“静态预计算”架构：构建前脚本 `scripts/gen-git-history.sh` 生成 `data/git_history.json`，页面渲染时仅读取 data 文件，不做运行时 Git 查询。
- `git_history` 键空间与内容目录脱钩：键名是相对 `content/` 的路径（`docs/*.md`）。任何数据流重构都必须保持此契约，否则 UI 无报错但功能失效。
- 评论系统是“启用开关 + 供应商选择”双层架构：`comments.enable` 控制渲染，`comments.type` 控制组件分派；仅切换供应商不等于启用评论。
- 模板环境变量受 Hugo 安全白名单约束（`hugo.toml` 的 `[security.funcs].getenv`）；新增环境变量属于架构变更，必须同步更新安全配置。
- 主题来自 `themes/hextra` 子模块，根目录 `layouts/` 覆盖主题模板；方案设计需先判断是“站点覆盖层”还是“子模块层”改动，避免后续升级冲突。