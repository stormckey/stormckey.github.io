# Typst is All You Need

## 如何开始

因为 Typst 比较新，所以相关的（特别是中文的）文档还不是很多，所以目前还是靠官方的文档：[:octicons-link-16:Typst Documentation](https://typst.app/docs)，过一遍里面的 Tutorial 部分，就可以基本上掌握 Typst 的使用了。之后就是写的过程中遇到啥就在文档里搜啥。

另外就是看看 [:octicons-link-16:awesome-typst-cn](https://github.com/typst-doc-cn/awesome-typst-cn) 里面的一些资源，比如 Typst 的模板，Typst 的插件等等。比较详细了，就不再赘述了。特别是遇到啥问题可以先看看这里面的模板里时怎么解决的。

尤其推荐其中的 [:octicons-link-16:nju-thesis-typst](https://github.com/nju-lug/nju-thesis-typst)，这是南京大学的本科生毕业论文的模板，里面的 README 里有详细的使用方法，而且代码也非常简洁高效，基本把所有坑都解决了，可以作为参考。

## VSCode 插件

首先是 [:octicons-link-16:awesome-typst-cn](https://github.com/typst-doc-cn/awesome-typst-cn) 里推荐的插件，这里我就不再赘述了，可以直接看上面的链接。我自己用了 [:octicons-link-16:Typst LSP](https://marketplace.visualstudio.com/items?itemName=nvarner.typst-lsp) 和 [:octicons-link-16:Typst Preview](https://marketplace.visualstudio.com/items?itemName=mgt19937.typst-preview) 这两个插件，可以在 VSCode 里直接预览 Typst 的效果，十分方便。

除此之外，我还用了 VSCode 的 [:octicons-link-16:Paste Image](https://marketplace.visualstudio.com/items?itemName=mushan.vscode-paste-image) 插件，可以直接粘贴图片，十分方便。然后顺带修改一下粘贴格式：

```json
"pasteImage.insertPattern": "#figure(\n  image(\"${imageSyntaxPrefix}${imageFilePath}${imageSyntaxSuffix}\", width: 100%),\n  caption: \"\",\n) <>",
```

这样粘贴的图片就会变成：

```typ
#figure(
  image("xxx", width: 100%),
  caption: "",
) <>
```

## 一些坑点

### 段落首行缩进

Typst 和 $\LaTeX$ 一样，设置首行缩进后，每个章节的第一个段落仍然不会缩进。只好加一个假的段落，加上一个 `v(-1em)` 来实现：

```typ
#let fake-par = {
  v(-1em)
  show par: set block(spacing: 0pt)
  par("")
}
```

之后通过 show 命令在 `heading` `terms` `list` `enum` `figure` `table` `raw` 之类的东西后面加上这个假的段落就可以了，例如给 `heading` 加上：

```typ
show heading: it => {
  it
  v(5pt)
  fake-par
}
```

当然为了美观我这里另外加了个 `v(5pt)`，可以根据自己的喜好调整。对于代码块 `raw` 要注意一下，因为行内代码和代码块的 `raw` 似乎是一样的，我暂时是使用行数来判断的，如果行数大于 1 就加上假的段落，否则不加：

```typ
show raw: it => {
  set text(font: ("Lucida Sans Typewriter", "Source Han Sans HW SC"))
  if it.lines.len() > 1 [
      #it
      #fake-par
  ] else [
      #it
  ]
}
```

这里同时也改了字体。这里有个技巧是这样写可以让中英文显示不一样的字体，Typst 会按顺序选择第一个存在的字体，所以这里中文会显示思源黑体，英文会显示 Lucida Sans Typewriter。
