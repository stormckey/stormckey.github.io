---
comments: true
authors:
    - stormckey
categories:
    - 效率
    - VSCode
date: 2023-12-24
nostatistics: true
---

# VSCode Snippet

!!! abstract
    在 VSCode 中我们可以自定义 Snippet，这可以极大地提高我们在输入某种重复的代码时的效率

<!-- more -->

## Snippet 简介

其实 Snippet 就是我们在自动补全中经常看见的选项之一，一般 Snippet 会自动补充出一种框架，自动填充其中一些信息(1)，然后再把我们的光标依次移动到对应的位置进行输入。
{ .annotate }

1.  比如说日期，当前文件名，或者剪贴板内容等

但我们也可以对指定的语言设置我们自己的 Snippet，这样以后我们在输入的时候自动补全中就可以使用我们自己的 Snippet 了。

具体的语法和介绍可以参考 [:octicons-link-16:官方文档](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

## Markdown 中的自动补全问题

你或许注意到了 markdown 中输入文本并不会触发自动补全(1)，这一现象在这个 [:octicons-link-16:问题](https://stackoverflow.com/questions/43639841/how-to-set-markdown-snippet-trigger-automatically) 中已有讨论
{ .annotate }

1.  又或者其实你没注意到（乐）

解决方法正如回答中所说，我们需要手动为 markdown 开启自动补全；

```json title="settings.json"
  "[markdown]": {
    "editor.quickSuggestions": {
      "other": true,
      "comments": false,
      "strings": true
    },
  }
```

这样子 Snippet 就可以正常使用了。


