---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/维基"]
---

Ceci est la documentation d'aide pour {{<wiki "ModernWiki">}}.

## Comment éditer

Vous pouvez éditer en cliquant sur le bouton "Éditer" en haut à droite, veuillez utiliser la syntaxe Markdown.

## Créer une nouvelle page

Veuillez utiliser l'outil ci-dessous pour créer une nouvelle page :

{{< newpage-tool >}}

Structure du répertoire du dépôt :

```
content/
├── docs/
│   └── catégorie/
│       └── nom-de-page.md
└── _index.md
```

Tous les fichiers `.md` situés dans le répertoire `/content/docs/` seront rendus en tant que pages.

### Téléverser des images

Si vous souhaitez ajouter des images à une page, convertissez la page en répertoire, puis placez les images dans ce répertoire.

Exemple :

- Vous avez une page `content/docs/help/wiki.md` et vous voulez lui ajouter des images.
- Vous devez la changer en `content/docs/help/wiki/index.md`, puis placer les images dans le répertoire `content/docs/help/wiki/`.

## Lier vers d'autres pages

Vous pouvez utiliser par exemple : `{{</*wiki "维基"*/>}}` => {{<wiki "维基">}}.

Si l'article a un répertoire de catégorie, alors : `{{</*wiki "catégorie/article"*/>}}`

Si la page n'existe pas, par exemple `{{</*wiki "chemin/notExist.md"*/>}}` => {{<wiki "chemin/notExist.md">}}, elle apparaîtra en rouge.

{{< callout >}}
  Pour un lien direct vers une URL, utilisez `[texte du lien](URL)`
{{< /callout >}}

## Syntaxe Markdown courante

Aide-mémoire des syntaxes Markdown de base

| Élément / Effet                | Syntaxe                                   | Aperçu                          |
| :----------------------------- | :---------------------------------------- | :------------------------------ |
| **Titre (Heading)**            | `# H1` `## H2` `### H3`                  | /                               |
| **Gras (Bold)**                | `**ce texte est en gras**` ou `__ce texte est en gras__` | **ce texte est en gras**        |
| **Italique (Italic)**          | `*ce texte est en italique*` ou `_ce texte est en italique_` | _ce texte est en italique_      |
| **Gras et Italique (Bold & Italic)** | `***ce texte est en gras et italique***` | **_ce texte est en gras et italique_** |
| **Barré (Strikethrough)**      | `~~ce texte est barré~~`                 | ~~ce texte est barré~~          |
| **Liste ordonnée (Ordered List)** | `1. Premier élément` `2. Deuxième élément` | /                               |
| **Liste non ordonnée (Unordered List)** | `- Élément` `* Élément`                | /                               |
| **Code (Code en ligne)**       | `` Utiliser la fonction `printf()` ``     | Utiliser la fonction `printf()` |
| **Bloc de code (Code Block)**  | \`\`\` contenu du bloc de code \`\`\`    | (affiché comme un bloc de code surligné) |
| **Ligne de séparation (Horizontal Rule)** | `***` ou `---`                     | /                               |
| **Lien (Link)**                | `[texte du lien](https://example.com)`    | [texte du lien](https://example.com) |
| **Image (Image)**              | `![texte alternatif](chemin ou URL de l'image)` | (affiche l'image)               |

### Bloc de citation

```markdown {filename=Markdown}
> [!NOTE]
> Informations utiles que les utilisateurs devraient connaître, même s'ils ne font que parcourir le contenu.

> [!WARNING]
> Informations urgentes nécessitant l'attention immédiate de l'utilisateur pour éviter des problèmes.
```

> [!NOTE]
> Informations utiles que les utilisateurs devraient connaître, même s'ils ne font que parcourir le contenu.

> [!WARNING]
> Informations urgentes nécessitant l'attention immédiate de l'utilisateur pour éviter des problèmes.

```markdown {filename=Markdown}
> Citation simple
```

> Citation simple

### Tableaux

```markdown {filename=Markdown}
| Nom | Âge |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |
```

| Nom | Âge |
| :--- | :--- |
| Zhang San | 27   |
| Li Si | 23   |

## Autres extensions Markdown

### Formules mathématiques Latex

Utilisez `\(...\)` pour les formules en ligne. Par exemple : `\(\ce{H2O}\) est de l'eau` => \(\ce{H2O}\) est de l'eau.

Utilisez `$$...$$` pour les formules hors ligne :

```latex
$$\mu_p=x^T\bm{\mu}$$
```

 $$\mu_p=x^T\bm{\mu}$$

### Diagrammes / Organigrammes

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

### Shortcodes du thème

D'autres shortcodes de thème sont également pris en charge, consultez la [documentation du thème Hextra](https://imfing.github.io/hextra/zh-cn/docs/guide/shortcodes/)
