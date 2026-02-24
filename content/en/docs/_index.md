---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/wiki-en"]
---

This is the help page for {{< wiki "ModernWiki" >}}.

## How to edit

Click the "Edit" button at the top-right corner and edit with Markdown.

## Create a new page

Use the tool below to create new pages:

{{< newpage-tool >}}

Repository structure:

```
content/
├── docs/
│   └── category/
│       └── page-name.md
└── _index.md
```

All `.md` files under `/content/docs/` are rendered as pages.
