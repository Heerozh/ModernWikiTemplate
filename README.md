这是 ModernWiki 的一个模板。

请前往 [ModernWiki](https://github.com/Heerozh/ModernWiki) 获取更多信息。

## 结构

### `content/docs` 百科页面目录

#### 主页文件

- `_index.md` 为目录页面（表示还有子目录），常用来列出子页面
- `index.md` 百科页面文件（无子目录）

### `archetypes` 页面模板目录

- `default.md` 为新建页面的默认模板

### `data` config数据目录

此目录的内容可通过 {{< site.Data.filename >}} 访问。

### `i18n` 多语言目录

此目录的文本可通过{{< (T "key") >}} 访问。

### `layouts` 布局目录

#### `partials`

这里的文件可以替换theme的布局文件。

- `partials/breadcrumb.html` 页面顶部的面包屑导航，以及编辑/历史按钮
- `partials/components/last-updated.html` 页面底部的最后更新信息，包含git贡献信息

#### `shortcodes`

短代码程序

- `shortcodes/repo.html` 仓库remote信息短代码
- `shortcodes/wiki.html` 生成wiki页面链接的短代码

## 配置参考

其他配置参考可参见主题文档：

[hextra主题文档](https://imfing.github.io/hextra/zh-cn/docs/guide/configuration/)