# Commandline Enviroment

!!! abstract
    记录missing semester[:octicons-link-16:本堂课](https://missing-semester-cn.github.io/2020/command-line/)的一些笔记

### Job Control

`Ctrl-C`: 向前台的程序发送中断信号

`man signal`: 查看所有signal

`SIGHUP`: Hang up 信号，不用深入了解，只要知道一般是终端被关闭时发送给所有进程的信号，默认的处理方式是收到就终止

`jobs`: 查看所有未终止的进程

`Ctrl-Z`: 暂停程序，但后续可以重新继续

`&`： 以此结尾，程序会在后台执行

`bg %JOB_ID/ PID`: 让暂停的后台进程在后台继续运行,<job id>在`jobs`命令中获取,pid 通过`ps`获取

`fd %JOB_ID/ PID`:让后台程序在前台运行（无论是否暂停）

`kill -STOP/... %JOB_ID/ PID`: 给某个进程发送指定的信号

`nohup COMMAND`: 对SIGHUP的默认处置改为不搭理

### Terminal Multiplexer

首先理解tmux的三个不同层级: session,window,pane

##### 新建一个session
`tmux`启动一个session，不同于原来的终端的进程，通过`C-a d`来detach，但session的进程仍然存在，所以上面的程序都会继续运行，`tmux a NAME`来重新连接，默认是0，1....只有一个名字的时候可以缺省，`tmux new -t NAME`来给新的session命名(-t target)

`tmux ls`:列出所有 session

##### session以内的操作

`C-a c`: 创建（create）一个新的windows，这将会是一个新的进程,虽然从属于同一个tmux session  
![](images/commandline_env/2023-03-27-01-48-05.png#pic)

`C-a n/p/NUMBER` 下一个/上一个/第x个window

`C-a ,`:重命名window

##### window以内的操作

`C-a "`: 上下分裂pane,这会是新的进程和新的tty
![](images/commandline_env/2023-03-27-01-41-57.png#pic)
![](images/commandline_env/2023-03-27-01-43-10.png#pic)

`C-a %`: 左右分裂pane
![](images/commandline_env/2023-03-27-01-44-35.png#pic)

`C-a ARROW`: 在pane之间移动

`C-a SPACE`: 一键切换下一个布局模式

`C-a z`:放大缩小当前pane

### dotfiles

~/zshrc是zsh的默认配置文件，可以理解为每次启动都会执行其中的语句，比如你在里面写上一句`echo Hello`最后在每次启动zsh的时候自动问候你一句

`alias STRING="STRING"`别名，打前面的缩写会被扩展成后面的全称，=前后无空格，否则会被当作是alias的多个不同的参数,写入zshrc使之常常生效

`alias STRING`: 查看你设置的别名是啥

在github上可以找到许多人的配置文件，当然也有[:octicons-link-16:笔者自己的](https://github.com/stormckey/dotfiles)

##### 符号连接

很多时候把配置文件放在～目录下并不方便，也不好混乱，也不好建立GitHub仓库进行管理，配置文件的读取位置往往是定死的，移动到别处就失效了，我们可以利符号连接来整理他们。

`ln -s TRUE_PATH VIRTUAL_PATH`: 软连接，VIRTUAL_PATH上实际上什么文件都没有，但我们试图读写这个文件的时候，会被导向TRUE_PATH上那个真实存在的文件，利用这个就可以配置.

注意创建符号连接时VIRTUAL_PATH不能存在

若删去TRUE_PATH，符号连接仍然存在，但已不可访问（显示文件不存在）

### Remote Machine

详情可以看[:octicons-link-16:这一篇](https://stormckey.github.io/Blog/ssh_wsl/)，是一个具体的ssh连接实践

`ssh USERNAME@IP_ADDRESS`: 连接remote machine

`ssh-keygen`: 自动生成迷药，注意keyphrase应该为空（直接回车）

`ssh-copy-id USERNAME@IP_ADDRESS`: 复制公钥到remote machine的指定文件中

用rsync或者scp传输文件，rsync可以从中断处恢复

`scp -p xxxx LOCAL_PATH USERNAME@IP_ADDRESS:REMOTE_PATH`:复制过去

`scp -p xxxx USERNAME:IP_ADDRESS LOCAL_PATH`: 复制过来

～/.ssh/config 里面可以设置remote machine别名 默认端口 默认ip地址等属性
![](images/commandline_env/2023-03-27-02-36-41.png#pic)

!!! tip
    在remote machine使用tmux，可以在连接关闭后，连接回来，再重新attach，之前运行的程序都会仍然存在。
    在远程的tmux的快捷键需要按两次C-a

!!! tip
    VSCode的Remote ssh相当好用，可以让你用VSCode对远程机器上操作，包括debug啥的