# Typst is All You Need

!!! info "我的一些自用模板在 [:octicons-mark-github-16:typst-template](https://github.com/PeiPei233/typst-template)"

## 如何开始

因为 Typst 比较新，所以相关的（特别是中文的）文档还不是很多，所以目前还是靠官方的文档：[:octicons-link-16:Typst Documentation](https://typst.app/docs)，过一遍里面的 Tutorial 部分，就可以基本上掌握 Typst 的使用了。之后就是写的过程中遇到啥就在文档里搜啥。

另外就是看看 [:octicons-mark-github-16:awesome-typst-cn](https://github.com/typst-doc-cn/awesome-typst-cn) 里面的一些资源，比如 Typst 的模板，Typst 的插件等等。比较详细了，就不再赘述了。特别是遇到啥问题可以先看看这里面的模板里时怎么解决的。

尤其推荐其中的 [:octicons-mark-github-16:nju-thesis-typst](https://github.com/nju-lug/nju-thesis-typst)，这是南京大学的本科生毕业论文的模板，里面的 README 里有详细的使用方法，而且代码也非常简洁高效，基本把所有坑都解决了，可以作为参考。

## VSCode 插件

首先是 [:octicons-mark-github-16:awesome-typst-cn](https://github.com/typst-doc-cn/awesome-typst-cn) 里推荐的插件，这里我就不再赘述了，可以直接看上面的链接。我自己用了 [:octicons-link-16:Typst LSP](https://marketplace.visualstudio.com/items?itemName=nvarner.typst-lsp) 和 [:octicons-link-16:Typst Preview](https://marketplace.visualstudio.com/items?itemName=mgt19937.typst-preview) 这两个插件，可以在 VSCode 里直接预览 Typst 的效果，十分方便。

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

## 一些技巧

### 中英文不同字体

给 text 传入 font 时，如果传入一个 array，Typst 会按顺序选择第一个存在的字体。所以可以这样写：

```typ
#set text(font: ("Times New Roman", "SimSun"))
```

这样中文就会显示宋体，英文就会显示 Times New Roman。另外注意一下自带的 SimSun、SimHei 之类的字体不支持 Typst 传入的 weight 参数，建议使用思源黑体、思源宋体之类的字体。Typst 的 weight 是选择变体，而不是手动加粗字体，所以如果字体不支持变体，就会显示不出来。

中文字体也不支持斜体，应该用楷体代替。`show` 一下再设置 `text` 就好了。例如：

```typ
#show emph: text.with(font: ("Linux Libertine", "STKaiti"))
```

更详细的看这个 [:octicons-link-16:issue](https://github.com/typst/typst/issues/725)

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

当然为了美观我这里另外加了个 `v(5pt)`，可以根据自己的喜好调整。对于代码块 `raw` 要注意一下，因为行内代码和代码块的 `raw` 要做区别，行内代码不需要在后面加假的段落，所以要加一个 `block: true` 来区分：

```typ
show raw.where(block: true): it => {
  it
  fake-par
}
```

另外 `terms` 如果设置了首行缩进会有一些问题，所以在 `terms` 块里要取消缩进，例如：

```typ
show terms: it => {
  set par(first-line-indent: 0pt)
  set terms(indent: 10pt, hanging-indent: 9pt)
  it
  fake-par
}
```

### 代码块显示行号

```typ
#show raw.where(block: true): it => { set par(justify: false); grid(
  columns: (100%, 100%),
  column-gutter: -100%,
  block(width: 100%, inset: 1em, for i, line in it.text.split("\n") {
    box(width: 0pt, align(right, str(i + 1) + h(2em)))
    hide(line)
    linebreak()
  }),
  block(radius: 1em, fill: luma(246), width: 100%, inset: 1em, it),
)}
```

另外这个 [:octicons-link-16:issue](https://github.com/typst/typst/issues/344) 里面也给出了其他的方法。
