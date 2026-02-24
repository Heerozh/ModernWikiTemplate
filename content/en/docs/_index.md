---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/维基"]
---

This is the help documentation for {{<wiki "ModernWiki">}}.

## How to Edit

You can edit by clicking the "Edit" button in the top right corner. Please use Markdown syntax.

## Create a New Page

Please use the tool below to create a new page:

{{< newpage-tool >}}

Repository directory structure:

```
content/
├── docs/
│   └── category-directory/
│       └── page-name.md
└── _index.md
```

All `.md` files under the `/content/docs/` directory will be rendered as pages.

### Upload Images

If you want to add images to a page, convert the page into a directory and place the images inside that directory.

Example:

- You have a page `content/docs/help/wiki.md` and you want to add images to it.
- You need to change it to `content/docs/help/wiki/index.md` and then place the images in the `content/docs/help/wiki/` directory.

## Link to Other Pages

You can use, for example: `{{</*wiki "维基"*/>}}` => {{<wiki "维基">}}.

If the article has a category directory, then: `{{</*wiki "category/article"*/>}}`

If the page does not exist, such as `{{</*wiki "path/notExist.md"*/>}}` => {{<wiki "path/notExist.md">}}, it will be displayed in red.

{{< callout >}}
  To link directly to a URL, you can use `[link text](URL)`
{{< /callout >}}

## Common Markdown Syntax

Basic Markdown syntax quick reference

| Element / Effect              | Syntax                                   | Preview                        |
| :---------------------------- | :--------------------------------------- | :------------------------------ |
| **Heading**                   | `# H1` `## H2` `### H3`                  | /                               |
| **Bold**                      | `**This is bold text**` or `__This is bold text__` | **This is bold text**                |
| **Italic**                    | `*This is italic text*` or `_This is italic text_`     | _This is italic text_                  |
| **Bold & Italic**             | `***This is bold and italic text***`                   | **_This is bold and italic text_**            |
| **Strikethrough**             | `~~This is strikethrough text~~`                       | ~~This is strikethrough text~~                |
| **Ordered List**              | `1. First item` `2. Second item`                  | /                               |
| **Unordered List**            | `- Item` `* Item`                        | /                               |
| **Code (Inline Code)**        | `` Use the `printf()` function ``               | Use the `printf()` function            |
| **Code Block**                | \`\`\` code block content \`\`\`                 | (displayed as a highlighted code block)            |
| **Horizontal Rule**           | `***` or `---`                           | /                               |
| **Link**                      | `[link text](https://example.com)`        | [link text](https://example.com) |
| **Image**                     | `![alt text](image path or URL)`             | (displays the image)                      |

### Callouts

```markdown {filename=Markdown}
> [!NOTE]
> Useful information that users should know even when just browsing content.

> [!WARNING]
> Urgent information that requires immediate user attention to avoid problems.
```

> [!NOTE]
> Useful information that users should know even when just browsing content.

> [!WARNING]
> Urgent information that requires immediate user attention to avoid problems.

```markdown {filename=Markdown}
> Simple quote
```

> Simple quote

### Tables

```markdown {filename=Markdown}
| Name | Age |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |
```

| Name | Age |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |

## Other Markdown Extensions

### Latex Math Formulas

Use `\(...\)` to wrap inline formulas. For example: `\(\ce{H2O}\) is water` => \(\ce{H2O}\) is water.

Use `$$...$$` to wrap block formulas:

```latex
$$\mu_p=x^T\bm{\mu}$$
```

 $$\mu_p=x^T\bm{\mu}$$

### Charts/Flowcharts

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

### Theme Shortcodes

Other theme shortcodes are also supported. Please refer to the [hextra theme documentation](https://imfing.github.io/hextra/zh-cn/docs/guide/shortcodes/)
