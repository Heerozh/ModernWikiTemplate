---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/维基"]
---

Dies ist die Hilfedokumentation für {{<wiki "ModernWiki">}}.

## Bearbeiten

Sie können eine Seite bearbeiten, indem Sie oben rechts auf die Schaltfläche "Bearbeiten" klicken. Bitte verwenden Sie die Markdown-Syntax.

## Neue Seite erstellen

Verwenden Sie das folgende Tool, um eine neue Seite zu erstellen:

{{< newpage-tool >}}

Repository-Verzeichnisstruktur:

```
content/
├── docs/
│   └── Kategorie-Verzeichnis/
│       └── Seitenname.md
└── _index.md
```

Alle `.md`-Dateien im Verzeichnis `/content/docs/` werden als Seiten gerendert.

### Bilder hochladen

Wenn Sie einer Seite Bilder hinzufügen möchten, konvertieren Sie die Seite bitte in ein Verzeichnis und legen Sie die Bilder in diesem Verzeichnis ab.

Beispiel:

-   Sie haben eine Seite `content/docs/help/wiki.md` und möchten ihr Bilder hinzufügen.
-   Sie müssen sie in `content/docs/help/wiki/index.md` umbenennen und die Bilder dann im Verzeichnis `content/docs/help/wiki/` ablegen.

## Auf andere Seiten verlinken

Sie können z.B. verwenden: `{{</*wiki "维基"*/>}}` => {{<wiki "维基">}}.

Wenn der Artikel ein Kategorieverzeichnis hat, dann: `{{</*wiki "Kategorie/Artikel"*/>}}`

Wenn die Seite nicht existiert, z.B. `{{</*wiki "path/notExist.md"*/>}}` => {{<wiki "path/notExist.md">}}, wird sie rot angezeigt.

{{< callout >}}
  Für direkte Links zu URLs können Sie `[Linktext](URL)` verwenden.
{{< /callout >}}

## Häufig verwendete Markdown-Syntax

Kurzreferenz für grundlegende Markdown-Syntax

| Element / Effekt                  | Syntax                                     | Vorschau                        |
| :-------------------------------- | :----------------------------------------- | :------------------------------ |
| **Überschrift (Heading)**         | `# H1` `## H2` `### H3`                    | /                               |
| **Fett (Bold)**                   | `**Dies ist fetter Text**` oder `__Dies ist fetter Text__` | **Dies ist fetter Text**        |
| **Kursiv (Italic)**               | `*Dies ist kursiver Text*` oder `_Dies ist kursiver Text_` | _Dies ist kursiver Text_        |
| **Fett & Kursiv (Bold & Italic)** | `***Dies ist fett-kursiver Text***`        | **_Dies ist fett-kursiver Text_** |
| **Durchgestrichen (Strikethrough)** | `~~Dies ist durchgestrichener Text~~`      | ~~Dies ist durchgestrichener Text~~ |
| **Geordnete Liste (Ordered List)** | `1. Erster Punkt` `2. Zweiter Punkt`       | /                               |
| **Ungeordnete Liste (Unordered List)** | `- Punkt` `* Punkt`                        | /                               |
| **Code (Inline Code)**            | `` Verwende die `printf()`-Funktion ``     | Verwende die `printf()`-Funktion |
| **Codeblock (Code Block)**        | \`\`\` Codeblock-Inhalt \`\`\`             | (wird als hervorgehobener Codeblock angezeigt) |
| **Trennlinie (Horizontal Rule)**  | `***` oder `---`                           | /                               |
| **Link**                          | `[Linktext](https://example.com)`          | [Linktext](https://example.com) |
| **Bild (Image)**                  | `![Alternativtext](Bildpfad oder URL)`     | (zeigt das Bild)                |

### Zitatblöcke

```markdown {filename=Markdown}
> [!NOTE]
> Nützliche Informationen, die der Benutzer kennen sollte, auch wenn er nur Inhalte durchsieht.

> [!WARNING]
> Dringende Informationen, die die sofortige Aufmerksamkeit des Benutzers erfordern, um Probleme zu vermeiden.
```

> [!NOTE]
> Nützliche Informationen, die der Benutzer kennen sollte, auch wenn er nur Inhalte durchsieht.

> [!WARNING]
> Dringende Informationen, die die sofortige Aufmerksamkeit des Benutzers erfordern, um Probleme zu vermeiden.

```markdown {filename=Markdown}
> Einfaches Zitat
```

> Einfaches Zitat

### Tabellen

```markdown {filename=Markdown}
| Name | Alter |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |
```

| Name | Alter |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |

## Andere Markdown-Erweiterungen

### Latex-Mathematikformeln

Verwenden Sie `\(...\)` für Inline-Formeln. Zum Beispiel: `\(\ce{H2O}\) ist Wasser` => \(\ce{H2O}\) ist Wasser.

Verwenden Sie `$$...$$` für abgesetzte Formeln:

```latex
$$\mu_p=x^T\bm{\mu}$$
```

 $$\mu_p=x^T\bm{\mu}$$

### Diagramme/Flussdiagramme

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

Es werden auch andere Theme-Shortcodes unterstützt. Siehe dazu die [Hextra-Theme-Dokumentation](https://imfing.github.io/hextra/zh-cn/docs/guide/shortcodes/)
