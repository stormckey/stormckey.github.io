# Shell++ 

!!! abstract "一个离散的知识列表，没有逻辑顺序"

## Shell Scripts

!!! warning "定义变量**请勿空格** : `a=b`, 否则会被识别成用两个参数运行程序a&ensp;`a = b`"
!!! warning "'和"都是字符串，但是前者不会解引用变量，后者会"
!!! warning "使用if[[&ensp;]];而不是if[],前者更不容易出bug"
!!! info "一些特殊的变量"
    - $0 - Name of the script
    - $1 to $9 - Arguments to the script. $1 is the first argument and so on.
    - $@ - All the arguments
    - $# - Number of arguments
    - $#X - Length of $X
    - $? - Return code of the previous command
    - $$ - Process identification number (PID) for the current script
    - !! - Entire last command, including arguments. A common pattern is to execute a command only for it to fail due to missing permissions; you can quickly re-execute the command with sudo by doing sudo !!
    - $_ - Last argument from the last command. If you are in an interactive shell, you can also quickly get this value by typing Esc followed by . or Alt+.
!!! tip "好用的引用语法"
    我们可以把在shell中执行指令的结果当场一个临时的变量来用（什么右值引用）
    `&(ls)` 会把ls的结果当做一个变量，我们可以用for来遍历它` for file in $(ls)` 
    `<(ls)` 会把结果当做一个临时文件，我们可以把临时文件作为参数传给其他命令
!!! tip "shell自动扩展"
    foo？会匹配foo1、foo2，而foo*会匹配foo、foo1、foo114514
    {1,2}x{3,4}会扩展成 1x3 1x4 2x3 2x4
!!! tip "更好的shebang"
    `#! /usr/in/env zsh` 这样子系统会自动去环境变量中找zsh的安装位置，提高了可移植性

## Shell Tools

!!! info "有用的命令行工具\命令"
    - tldr： 太长不看，更简短的manpage
    - ffmpeg： 视频格式转换
    - find： 递归查找（ls在本目录），随后可以对找到的文件执行命令
    - grep：处理文件的文本内容，查找、筛选、替换
    - 启用zsh基于历史命令补全和历史命令模糊搜索
    - j: autojump插件，自动跳转到匹配的最常用文件夹
    - tree: 生成文件树
