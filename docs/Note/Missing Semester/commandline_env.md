---
comments: true
---
# Commandline Enviroment

!!! abstract "记录missing semester[:octicons-link-16:此堂课](https://missing-semester-cn.github.io/2020/command-line/)的一些笔记"

## Job Control

终端的作业控制（Job Control）是一种在命令行环境下管理和控制正在运行的作业（Job）的机制。它提供了一些命令和技术，使用户能够在终端同时运行多个命令，并在需要时对其进行管理。

!!! info "作业"

    === "前台作业（Foreground Job）"
        前台作业是当前活动的作业，它会在终端显示其输出，并占用终端的输入。只有当前前台作业执行完毕或被暂停时，才能执行其他命令。

    === "后台作业（Background Job）"
        后台作业是在后台运行的作业，它不会占用终端的输入和输出。可以使用特殊字符 `&` 将命令放置在后台运行，从而允许同时运行多个命令。

    === "作业状态和信号"
        每个作业都具有一个状态，如运行中、停止或完成。可以使用信号来控制作业的行为，如 `Ctrl-C`（中断作业）和 `Ctrl-D`（结束作业输入）。

!!! info "作业控制命令"
    === "jobs"
        `jobs` 命令用于列出当前正在运行的作业。每个作业都有一个唯一的 ID，前面带有一个 `+` 号的作业是当前的前台作业，前面带有一个 `-` 号的作业是当前的后台作业。
    === "fg"
        `fg` 命令用于将后台作业切换到前台运行。可以使用作业 ID 或作业 PID 作为参数，也可以使用 `%` 符号加上作业 ID 作为参数。
    === "bg"
        `bg` 命令用于将前台作业切换到后台运行。可以使用作业 ID 或作业 PID 作为参数，也可以使用 `%` 符号加上作业 ID 作为参数。
    === "kill"
        `kill` 命令用于向作业发送信号。默认情况下，`kill` 命令会发送 `SIGTERM` 信号，可以使用 `-SIGNAL` 选项来指定信号类型。可以使用作业 ID 或作业 PID 作为参数，也可以使用 `%` 符号加上作业 ID 作为参数。
    === "man signal"
        `man signal` 命令用于查看所有可以发送给进程的信号。
    === "Ctrl-C"
        `Ctrl-C` 快捷键用于向前台作业发送 `SIGINT` 信号，通常用于终止前台作业。
    === "Ctrl-Z"
        `Ctrl-Z` 快捷键用于向前台作业发送 `SIGTSTP` 信号，通常用于暂停前台作业。

## Terminal Multiplexer

首先理解tmux的自上向下三个不同层级: session,window,pane

!!! info ""
    === "session"
        session是tmux的最高层级，可以理解为一个tmux的实例，可以有多个session，每个session可以有多个window，每个window可以有多个pane，每个pane可以有多个tty
    === "window"
        window是session的第二层级，可以理解为一个终端，可以有多个window，每个window可以有多个pane，每个pane可以有多个tty
    === "pane"
        pane是window的第三层级，可以理解为一个分屏，可以有多个pane，每个pane可以有多个tty

### 新建一个session

!!! info ""
    === "tmux"
        直接进入一个新的session
    === "tmux new -t NAME"
        新建一个名为NAME的session
    === "tmux a NAME"
        重新连接到名为NAME的session
    === "tmux ls"
        列出所有session
    === "Ctrl-b d"
        detach当前session

### session以内的操作

!!! info ""
    === "C-b c"
        创建一个新的window
    === "C-b n/p/NUMBER"
        切换到下一个/上一个/第x个window
    === "C-b ,"
        重命名当前window
    === "C-b &"
        关闭当前window

### window以内的操作

!!! info ""
    === "C-b \""
        上下分裂pane,这会是新的进程和新的tty
        ![](images/commandline_env/2023-03-27-01-41-57.png#pic)
        ![](images/commandline_env/2023-03-27-01-43-10.png#pic)
    === "C-b %"
        左右分裂pane
        ![](images/commandline_env/2023-03-27-01-44-35.png#pic)
    === "C-b o"
        切换到下一个pane
    === "C-b x"
        关闭当前pane
    === "C-b z"
        放大缩小当前pane
    === "C-b ARROW"
        在pane之间移动
    === "C-b SPACE"
        一键切换下一个布局模式

## Dotfiles

Dotfile 是以点（.）开头的配置文件，在Unix-like系统中被广泛使用。它们通常位于用户的主目录下，用于存储个人化和自定义的配置选项，以及其他应用程序和工具的设置。

Dotfile 的名称以一个或多个点开头，例如 `.bashrc`、`.vimrc`、`.gitconfig` 等。由于在默认情况下，Unix-like 系统会将以点开头的文件视为隐藏文件，因此这些配置文件在文件管理器中默认是不可见的。但可以通过特定的选项或命令查看和编辑它们。

Dotfile 的用途因文件名和所针对的应用程序而异，以下是一些常见的例子：

- `.bashrc`：Bash Shell 的配置文件，用于定义 Shell 的行为和环境变量。
- `.vimrc`：Vim 文本编辑器的配置文件，用于定义 Vim 的编辑器设置和插件。
- `.gitconfig`：Git 版本控制系统的配置文件，用于设置 Git 的用户信息、别名和其他选项。
- `.ssh/config`：SSH 客户端的配置文件，用于配置 SSH 连接的主机和选项。
- `.tmux.conf`：tmux 终端复用工具的配置文件，用于定义 tmux 的会话和窗格设置。

通过编辑和定制 Dotfile，用户可以按照个人偏好和需求来配置各种应用程序和工具。它们允许用户修改默认设置、添加快捷键、定义别名、设置环境变量等，以提升工作效率和个人化体验。

~/.zshrc是zsh的默认配置文件，可以理解为每次启动zsh,都会执行其中的语句。比如你在里面写上一句`echo Hello`，就会在每次启动zsh的时候自动问候你一句

在github上可以找到许多人分享的配置文件，这里也贴上[:octicons-link-16:我自己的](https://github.com/stormckey/dotfiles)

## 符号连接

很多时候把配置文件放在～目录下并不方便，也不好混乱，也不好建立GitHub仓库进行管理，配置文件的读取位置往往是定死的，移动到别处就失效了，我们可以利符号连接来整理他们。

`ln -s TRUE_PATH VIRTUAL_PATH`: 软连接，VIRTUAL_PATH上实际上什么文件都没有，但我们试图读写这个文件的时候，会被导向TRUE_PATH上那个真实存在的文件，利用这个就可以统一转移我们的配置文件了。

注意创建符号连接时VIRTUAL_PATH不能存在

若删去TRUE_PATH，符号连接仍然存在，但已不可访问（显示文件不存在）

## Remote Machine

详情可以看[:octicons-link-16:这一篇](https://stormckey.github.io/Blog/Environment/ssh_wsl/)，是一个具体的ssh连接实践。在[:ocitons-link-16:这一篇](http://stormckey.github.io/Blog/Minisql/docker_minisql/)中有关于docker的远程连接的实践，更加详细。

!!! info "常用指令"
    === "ssh USERNAME@IP_ADDRESS"
        连接remote machine
    === "ssh-keygen"
        自动生成迷药，注意keyphrase应该为空（直接回车）
    === "ssh-copy-id USERNAME@IP_ADDRESS"
        复制公钥到remote machine的指定文件中
    === "scp -p xxxx LOCAL_PATH USERNAME@IP_ADDRESS:REMOTE_PATH"
        将本地文件复制到remote machine
    === "scp -p xxxx USERNAME:IP_ADDRESS LOCAL_PATH"
        将remote machine文件复制到本地

～/.ssh/config 里面可以设置remote machine别名 默认端口 默认ip地址等属性
![](images/commandline_env/2023-03-27-02-36-41.png#pic)

!!! tip
    在remote machine使用tmux，可以在连接关闭后，连接回来，再重新attach，之前运行的程序都会仍然存在。
    在远程的tmux的快捷键需要按两次C-a

!!! tip
    VSCode的Remote ssh相当好用，可以让你用VSCode对远程机器上操作，包括debug啥的