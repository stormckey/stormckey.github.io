---
comments: true
authors:
    - stormckey
categories:
    - Cool
date: 2023-11-26
nostatistics: true
---

# 用 Vim 批量优化中文排版
!!! abstract
    众所周知中英文混杂的排版其实是有讲究的，但是实际操作起来输入法切来切去麻烦得很，本文讲的是用 vim 的 Pangu 插件来批量自动格式化的方法
<!-- more -->
## 安装 Vim 工具 Pangu

首先安装 [:octicons-mark-github-16: vim-plug](https://github.com/junegunn/vim-plug)，这是一个可以帮助我们方便的安装 vim 插件的插件

随后安装 Pangu 插件，在 ~/.vimrc 中添加

```bash
Plug 'hotoo/pangu.vim'， { 'for': ['markdown'， 'vimwiki'， 'text'] }
let g:pangu_rule_date = 1
```

随后在 vim 中执行`:PlugInstall`即可安装

Pangu 的 [:octicons-book-16: 官方首页](https://github.com/hotoo/pangu.vim)上已经有比较详细的说明了，想要启用其中的功能照着做就是了

## 批量使用 Pangu 格式化

首先用 vim 批量打开想要格式化的文件，一般来说，我们需要格式化的是文件夹下的所有 markdown 文件

```bash
vim **/*.md
```

那么所有符合格式的文件都被打开在缓存(buffer)中了，我们可以用`:ls`来查看，用`:n`来切换

我们可以把 vim 的缓存和文件的关系理解成内存和磁盘的关系，我们在缓存中可以修改文件，但直到`w`之前都不会写入磁盘

要批量处理，使用以下命令
```vim
:bufdo PanguAll
:bufdo update
:q
```

其中的 bufdo 的意思就是对所有缓存中的文件执行命令

我们可以把这一逻辑写入 bash 脚本中，下面是一个示例：

```bash
vim **/*.md -c ':silent! bufdo execute  "PanguAll" | update' -c ':q'
```
其中的 silent!可以让 vim 在执行命令时不输出任何信息，这样就不用按 more 了，之所以用 execute 而不直接 PanguAll 是因为好像后者会导致 bufdo 不执行后续的 update，具体为啥我还菜菜看不出来

最后的退出放在另一个-c 可以保证是在前者执行完了才退出而不是每写一个文件就试着退出一次

如果你还有其他的格式化的需求可以继续添加指令，不出意外的话上面的脚本是能够直接跑的


