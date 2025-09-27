---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/维基"]
---

这是 ModernWiki 的帮助文档。

## 如何编辑

你可以通过点击右上角的 "编辑" 按钮来编辑，请使用 Markdown 语法。

## 新建页面

所有在 `/content/docs/` 目录下的 `.md` 文件都会被渲染为页面。

请前往 [本 Wiki 的 Git 仓库]({{<repo "url">}})网站（或直接使用各种 Git 工具），在 `/content/docs/` 目录下选择一个目录（或新建目录），在里面新建 `.md` 文件。

目录结构：

```
content/
├── docs/
│   └── 类别目录/
│       └── 页面名.md
└── _index.md
```

### 上传图片

如果你要给页面添加图片，请把页面转换成目录，然后把图片放在这个目录下。

举例：

- 你有一个页面 `content/docs/help/wiki.md`，你想给它添加图片。
- 你需要把它改成 `content/docs/help/wiki/index.md`，然后把图片放在 `content/docs/help/wiki/` 目录下。

## 链接到其他页面

可以使用例如：`{{</*wiki "维基"*/>}}` => {{<wiki "维基">}}。

如果文章带类别目录，则：`{{</*wiki "类别/文章"*/>}}`

{{< callout >}}
  如果要直接链接网址，可用 `[链接文字](网址)`
{{< /callout >}}

## 常用 Markdown 语法

基本 Markdown 语法速查表

| 元素 / 效果                   | 语法                                     | 预览效果                        |
| :---------------------------- | :--------------------------------------- | :------------------------------ |
| **标题 (Heading)**            | `# H1` `## H2` `### H3`                  | /                               |
| **粗体 (Bold)**               | `**这是粗体文本**` 或 `__这是粗体文本__` | **这是粗体文本**                |
| **斜体 (Italic)**             | `*这是斜体文本*` 或 `_这是斜体文本_`     | _这是斜体文本_                  |
| **粗斜体 (Bold & Italic)**    | `***这是粗斜体文本***`                   | **_这是粗斜体文本_**            |
| **删除线 (Strikethrough)**    | `~~这是删除文本~~`                       | ~~这是删除文本~~                |
| **有序列表 (Ordered List)**   | `1. 第一项` `2. 第二项`                  | /                               |
| **无序列表 (Unordered List)** | `- 项目` `* 项目`                        | /                               |
| **代码 (内联代码)**           | `` 使用 `printf()` 函数 ``               | 使用 `printf()` 函数            |
| **代码块 (Code Block)**       | \`\`\` 代码块内容 \`\`\`                 | (显示为高亮的代码块)            |
| **分隔线 (Horizontal Rule)**  | `***` 或 `---`                           | /                               |
| **链接 (Link)**               | `[链接文字](https://example.com)`        | [链接文字](https://example.com) |
| **图片 (Image)**              | `![替代文本](图片路径或URL)`             | (显示图片)                      |

### 引用块

```markdown {filename=Markdown}
> [!NOTE]
> 即使用户只是浏览内容，也应该知道的有用信息。

> [!WARNING]
> 需要用户立即关注的紧急信息，以避免出现问题。
```

> [!NOTE]
> 即使用户只是浏览内容，也应该知道的有用信息。

> [!WARNING]
> 需要用户立即关注的紧急信息，以避免出现问题。

```markdown {filename=Markdown}
> 简单引用
```

> 简单引用

### 表格

```markdown {filename=Markdown}
| 姓名 | 年龄 |
| :--- | :--- |
| 张三 | 27   |
| 李四 | 23   |
```

| 姓名 | 年龄 |
| :--- | :--- |
| 张三 | 27   |
| 李四 | 23   |

## 其他 Markdown 扩展

### Latex 数学公式

使用`\(...\)`包裹行内公式。例如：`\(\ce{H2O}\) 是水` => \(\ce{H2O}\) 是水。

使用`$$...$$`包裹行间公式：
```latex
$$\mu_p=x^T\bm{\mu}$$
```
 $$\mu_p=x^T\bm{\mu}$$

### 图表/流程图

````markdown {filename=Markdown}
```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```
````

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

### 主题短代码

还支持其他主题短代码，可参考 [hextra主题文档](https://imfing.github.io/hextra/zh-cn/docs/guide/shortcodes/)
