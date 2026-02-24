---
title: Modern Wiki Help
linkTitle: Wiki
tags: [help]
aliases: ["/docs/wiki", "/docs/维基"]
---

Esta es la documentación de ayuda de {{<wiki "ModernWiki">}}.

## Cómo editar

Puedes editar haciendo clic en el botón "Editar" en la esquina superior derecha. Por favor, utiliza la sintaxis Markdown.

## Crear una nueva página

Utiliza la siguiente herramienta para crear una nueva página:

{{< newpage-tool >}}

Estructura del directorio del repositorio:

```
content/
├── docs/
│   └── directorio-de-categoría/
│       └── nombre-de-página.md
└── _index.md
```

Todos los archivos `.md` dentro del directorio `/content/docs/` se renderizarán como páginas.

### Subir imágenes

Si deseas agregar imágenes a una página, convierte la página en un directorio y luego coloca las imágenes dentro de ese directorio.

Ejemplo:

- Tienes una página `content/docs/help/wiki.md` y quieres agregarle imágenes.
- Necesitas cambiarla a `content/docs/help/wiki/index.md` y luego colocar las imágenes en el directorio `content/docs/help/wiki/`.

## Enlazar a otras páginas

Puedes usar, por ejemplo: `{{</*wiki "维基"*/>}}` => {{<wiki "维基">}}.

Si el artículo tiene un directorio de categoría, entonces: `{{</*wiki "categoría/artículo"*/>}}`

Si la página no existe, por ejemplo `{{</*wiki "ruta/noExiste.md"*/>}}` => {{<wiki "ruta/noExiste.md">}}, se mostrará en rojo.

{{< callout >}}
  Para enlazar directamente a una URL, puedes usar `[texto del enlace](URL)`
{{< /callout >}}

## Sintaxis Markdown común

Hoja de referencia rápida de sintaxis Markdown básica

| Elemento / Efecto               | Sintaxis                                     | Vista previa                        |
| :------------------------------ | :------------------------------------------- | :---------------------------------- |
| **Encabezado (Heading)**        | `# H1` `## H2` `### H3`                      | /                                   |
| **Negrita (Bold)**              | `**este texto está en negrita**` o `__este texto está en negrita__` | **este texto está en negrita**      |
| **Cursiva (Italic)**            | `*este texto está en cursiva*` o `_este texto está en cursiva_`     | _este texto está en cursiva_        |
| **Negrita y Cursiva (Bold & Italic)** | `***este texto está en negrita y cursiva***` | **_este texto está en negrita y cursiva_** |
| **Tachado (Strikethrough)**     | `~~este texto está tachado~~`                | ~~este texto está tachado~~         |
| **Lista ordenada (Ordered List)** | `1. Primer elemento` `2. Segundo elemento`   | /                                   |
| **Lista desordenada (Unordered List)** | `- Elemento` `* Elemento`                    | /                                   |
| **Código (Inline Code)**        | `` Usa la función `printf()` ``              | Usa la función `printf()`           |
| **Bloque de código (Code Block)** | \`\`\` contenido del bloque de código \`\`\` | (se muestra como bloque de código resaltado) |
| **Línea divisoria (Horizontal Rule)** | `***` o `---`                                | /                                   |
| **Enlace (Link)**               | `[texto del enlace](https://ejemplo.com)`    | [texto del enlace](https://ejemplo.com) |
| **Imagen (Image)**              | `![texto alternativo](ruta-o-URL-de-la-imagen)` | (muestra la imagen)                 |

### Bloques de cita

```markdown {filename=Markdown}
> [!NOTE]
> Información útil que los usuarios deberían conocer, incluso si solo están navegando por el contenido.

> [!WARNING]
> Información urgente que requiere la atención inmediata del usuario para evitar problemas.
```

> [!NOTE]
> Información útil que los usuarios deberían conocer, incluso si solo están navegando por el contenido.

> [!WARNING]
> Información urgente que requiere la atención inmediata del usuario para evitar problemas.

```markdown {filename=Markdown}
> Cita simple
```

> Cita simple

### Tablas

```markdown {filename=Markdown}
| Nombre | Edad |
| :----- | :--- |
| Zhang San | 27   |
| Li Si | 23   |
```

| Nombre | Edad |
| :----- | :--- |
| Zhang San | 27   |
| Li Si | 23   |

## Otras extensiones de Markdown

### Fórmulas matemáticas Latex

Usa `\(...\)` para fórmulas en línea. Por ejemplo: `\(\ce{H2O}\) es agua` => \(\ce{H2O}\) es agua.

Usa `$$...$$` para fórmulas en bloque:

```latex
$$\mu_p=x^T\bm{\mu}$$
```

 $$\mu_p=x^T\bm{\mu}$$

### Diagramas/Flujogramas

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

### Shortcodes del tema

También se admiten otros shortcodes del tema. Consulta la [documentación del tema hextra](https://imfing.github.io/hextra/zh-cn/docs/guide/shortcodes/)
