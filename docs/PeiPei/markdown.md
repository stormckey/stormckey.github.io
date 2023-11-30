# Markdown All in One

## VSCode like highlighting

即使用了 VSCode 的 MPE 的插件，Markdown 里的代码块还是十分的丑陋.这里提供了一种方法，可以让 Markdown 里的代码块的高亮效果和 VSCode 里的一样.

首先，如果导出的是白色底，就把 VSCode 的主题改成白色底的，如果是黑色底，就改成黑色底的.下面的配置是白色底的.

安装 [Paste Special](https://marketplace.visualstudio.com/items?itemName=d3v.pastespecial) 插件，直接在 VSCode 里复制写好的代码，在 Markdown 文件里粘贴时右键选择 `Paste Special`，粘贴为 HTML 格式.为了和 MPE 的默认格式匹配，我们需要对 css 进行一些微调.

例如如果粘贴完的如下：

```html
<div style="color: #3b3b3b;background-color: #1f1f1f;font-family: Fira Code Retina， 思源黑体 HW， Consolas， 'Courier New'， monospace， Consolas， 'Courier New'， monospace;font-weight: normal;font-size: 14px;line-height: 19px;white-space: pre;">...</div>
```

我们需要把它改成：

```html
<div style="color: #3b3b3b;background-color: #f5f5f5;font-family: Consolas， 'Courier New'， monospace， Consolas， 'Courier New'， monospace;font-weight: normal;font-size: 14px;line-height: 1.4;white-space: pre;border-radius: 3px;padding: .8em;margin-top: 0;margin-bottom: 16px;overflow: auto;">...</div>
```

主要是加了圆角、padding 和 margin.字体和行高可改可不改，看个人喜好.另外，为了打印方便，我们还可以更改 `white-space` 为 `pre-wrap`，这样就可以自动换行了，同时也可以去掉 `overflow: auto;`：

```html
<div style="color: #3b3b3b;background-color: #f5f5f5;font-family: Consolas， 'Courier New'， monospace， Consolas， 'Courier New'， monospace;font-weight: normal;font-size: 14px;line-height: 1.4;white-space: pre-wrap;border-radius: 3px;padding: .8em;margin-top: 0;margin-bottom: 16px;">...</div>
```

## `![]()` -> `<img src="" />`

在 Markdown 里插入图片时，我们一般使用 `![]()` 的方式，但是这样导出的 PDF 里的图片是不会居中的，而且也没有办法设置图片的宽高.所以我们需要把 `![]()` 改成 `<img src="" />`.使用以下正则表达式替换：

```regex
!\[(.*?)\]\((.*?)\)
```

替换为：

```regex
<img src="$2" alt="$1" style="max-width: 100%" />
```
