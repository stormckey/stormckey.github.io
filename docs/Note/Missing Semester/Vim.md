# Vim （Revisited）
!!! abstract "重写这篇笔记的时候我已经用了一段时间vim，笔记可能会过于简略，可参考[:octicons-link-16:课程网站](https://missing.csail.mit.edu/2020/editors/)"


## Basic

我们写代码事并不一直都是连续的输入，有时是跳转到某个地方，有时是做些小修改替换，有时是阅读代码，或者才是连续输入。   
为此，vim使用不同模式来便利各个不同目的的操作模式，使得相同的键在不同模式下意义不同。

!!! info "vim中最常用的模式有"
    - normal: 默认初始模式，任何模式都可以按<Esc>回到normal。阅读模式
    - insert: i进入，进行连续的输入,只用i可以无缝退化回原先什么功能都没有的编辑器。
    - replace: R进入，进行连续的替换
    - visual: v进入，进行选择，V进入行模式，按行选择， C-v进入块模式，按任意边长选择长方形 
    - command-line: ：进入，处理命令行操作（最基本的有 :w保存 :q退出 :wq保存退出 :q!强制退出）
!!! tip "一个Vim进程可以有多个标签页，一个标签页可以有多个窗口，而一个窗口像只眼睛看向一个特定的文件(Buffer)"

## Interface

!!! info "Normal move"
    - 上下左右: hjkl 
    - 以单词为界: w (下一个单词), b (单词开头), e (单词结尾)
    - 以行为界: 0 (行开头), ^ (行首个非空字符), $ (行尾)
    - 以屏为界: H (屏幕开头), M (屏幕中间), L (屏幕底部)
    - 滚动: Ctrl-u (上), Ctrl-d (下)
    - 以文件为界: gg (文件开头), G (文件尾), <num> G(对应行)
    - 以左右为界: % (对应的另一半括号或者类似的)
    - 行内寻找: f{character}, t{character}, F{cracter}, T{character} 小写往后大写往前
    - 搜索: /{regex} ?{regex} 往后往前搜索 ，按n继续搜下一个，按N反向继续
!!! info "Normal edit"
    - o / O ：在下/上新建一行并进入插入模式
    - d{motion} ：按照motion删除，motion见 move 部分
    - c{motion} ：比d{motion}多一步进入插入模式
    - x ： 删除当光标字符
    - s ： 以下一个输入代替当光标字符
    - Visual mode + manipulation ： 这些操作也适用于选择模式选中后
    - u 撤回, <C-r> 取消撤回
    - y 复制
    - p 粘贴
    - <num> manipulation ： 重复<num>次操作
    - i/a ： inside/around ，在什么之内/周围操作。例如：di( 在（）之内删除; da( 包括（）删除

## Advanced Vim

- Vim 是高度可定制化的。只要要改变用户目录下的配置文件即可(~/.vimrc)。也可参考笔者自己非常简单的的[:octicons-link-16:配置文件](https://github.com/stormckey/dotfiles/blob/main/dot_vimrc)  
- Vim也有许多优质的插件，笔者几乎没有添加任何插件，而是把Vim作为一个插件在VSCode上使用  
- Vim 的命令行高深莫测，笔者最常用的只是退出、替换而已