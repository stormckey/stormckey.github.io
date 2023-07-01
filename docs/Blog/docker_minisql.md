---
comments: true
---

# MacOS上利用Docker搭建MiniSQL环境

!!! abstract 
    一个简易的教程来介绍如何在MacOS上用docker搭建minisql环境，那么有人要问了，为什么不直接本地部署呢。
    
    我也想本地部署啊，但是编译起来破事太多了😅，索性试一种跨平台的方案。

## 1.启动容器

### 1.1下载Docker
首先你要有docker软件，先去官网下一个。

### 1.2拉取镜像
启动docker软件。来到命令行中输入以下命令来拉取ubuntu:20.04镜像（minisql当前推荐部署在ubuntu:20.04）：
```bash
docker pull ubuntu:20.04
```
??? info "镜像"
    镜像（Image）是一个静态的、只读的文件，它包含了操作系统、文件系统和应用程序的所有文件和设置。镜像是构建容器的基础，可以看作是一个模板或者蓝图。镜像是通过Dockerfile文件定义和构建的，Dockerfile中包含了一系列指令和配置，用于创建镜像。镜像可以存储在Docker Registry中，可以通过镜像名称和标签来唯一标识。镜像是不可修改的，如果需要对镜像进行更改，需要重新构建一个新的镜像。

    === "docker images"
        使用`docker images`命令查看当前已有的镜像列表。这将显示所有已下载和构建的镜像，以及它们的相关信息，如镜像 ID、名称、标签、大小等。![](images/docker_minisql/2023-07-01-17-34-32.png#pic)

    === "docker pull"
        使用`docker pull`命令从Docker Registry中拉取镜像。如果不指定标签，默认拉取latest标签的镜像。例如，`docker pull ubuntu:20.04`将拉取Ubuntu 20.04镜像。    

    === "docker rmi"
        使用`docker rmi`命令删除镜像。例如，`docker rmi ubuntu:20.04`将删除Ubuntu 20.04镜像,这里也可以使用ID指定要删除的镜像。

### 1.3启动容器
用`docker run`启动一个容器,参数`-it`表示启动完后直接启动容器的终端以供操作，`-p`表示端口映射，这里把loclahost:2333映射为容器的22号端口，`--name`后接容器名字，`ubuntu:20.04`表示使用的镜像。
```bash
docker run -it  -p 2333:22 --name minisql ubuntu:20.04
```
执行完命令应看到我们以root用户进入了容器的终端：
![](images/docker_minisql/2023-07-01-19-33-57.png#pic)
??? info "端口映射"
    端口映射是一种将主机（宿主机）端口与容器内部端口进行绑定的技术。它允许从主机上的特定端口访问容器内运行的服务或应用程序。

    在Docker中，通过使用`-p`或`--publish`参数来进行端口映射。参数的格式为主机端口:容器端口，其中主机端口是您希望在主机上暴露的端口号，容器端口是容器内部正在运行的服务所监听的端口号。

    `docker run -it -p 2333:22 --name minisql ubuntu:20.04`命令将主机的2333端口映射到容器的22号端口。这意味着主机上的任何请求发送到2333端口时，将被转发到容器的22号端口,22号端口是SSH使用的默认端口。因此，可以通过访问主机的2333端口来访问容器内部运行的SSH服务，以便进行远程连接和操作。

## 2.环境初步设置

### 2.1(可选)换源
??? warning "可能存在的问题"
    有时候直接换源会遇到报错：
    ![](images/docker_minisql/2023-07-01-19-42-06.png#pic)
    这需要我们先使用http，运行如下命令换http源：
    ```bash
    echo "    
    deb http://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
    deb http://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
    deb http://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
    deb http://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
    " > /etc/apt/sources.list
    ```
    这就可以进行下一步了，如果你希望在之后换回https源，那么在执行完2.2后，需要先

    更新证书：
    ```bash
    apt install --reinstall ca-certificates
    ```
    换回https源：
    ```bash
    echo "
    deb https://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
    " > /etc/apt/sources.list
    ```
    再次更新apt：
    ```bash
    apt update
    apt upgrade
    ```
    即可
直接执行命令即可
```bash
cp /etc/apt/sources.list /etc/apt/sources.list.bak
echo "    
    deb https://mirrors.zju.edu.cn/ubuntu/ focal main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
    deb https://mirrors.zju.edu.cn/ubuntu/ focal-security main restricted universe multiverse
    " > /etc/apt/sources.list
```
??? info "换源"
    换源是指将默认的软件包源（镜像）替换为特定地区或网络环境下更快速、可靠的软件包源。这是为了提高软件包的下载速度、解决网络访问限制或访问特定地区的软件包而采取的措施。

    更换软件包源的具体方法会因不同的操作系统和软件包管理工具而有所差异。在基于 Ubuntu 的 Docker 容器中，可以编辑 /etc/apt/sources.list 文件，将默认的软件包源替换为国内的镜像源，如浙江大学、清华大学等。这样一来，通过容器中的 `apt-get` 或 `apt` 命令安装软件时，将从国内镜像源下载软件包，提高速度和稳定性。

### 2.2安装必要工具
首先更新apt
```bash
apt update
apt upgrade
```

安装一些必要的工具：
```bash
apt install openssh-server vim git cmake gcc g++ gdb
```

## 3.配置SSH，使用VSCode开发

### 3.1（可选）创建用户

如果希望用非root用户登陆，那么我们可以先创建并设置一个用户：
```bash
useradd -m stormckey
passwd stormckey
```
这里的stormckey换成你自己起的用户名

### 3.2配置免密登陆
来到远程连接的发起者端（这里就是宿主机），执行下面命令生成密钥，输入paseephrase时直接回车（为空）
```bash
ssh-keygen
```
来到提示的目录下，复制id_rsa.pub的内容，将它写入被连接端（这里是容器）的`/home/stormckey/.ssh/authorized_keys`文件中

接着配置容器的sshd:
`vim /etc/ssh/sshd_config`

去掉以下的注释：
![](images/docker_minisql/2023-07-01-20-23-02.png#pic)
![](images/docker_minisql/2023-07-01-20-23-44.png#pic)
注意第二张图中的文件一定是你之前放公钥的文件,路径从用户根目录开始

更改完配置后启动/重启sshd
```bash
service ssh start
```

此时你在宿主机上就可以通过`ssh stormckey@localhost -p 2333`登陆容器了:
![](images/docker_minisql/2023-07-01-20-42-07.png#pic)

### 3.3配置VSCode

下载插件Remote-SSH插件，点击右边出现的插件图标，在侧栏中选择设置SSH：
![](images/docker_minisql/2023-07-01-20-43-59.png#pic)

写入如下的配置信息：
![](images/docker_minisql/2023-07-01-20-44-56.png#pic)

连接！
![](images/docker_minisql/2023-07-01-20-45-37.png#pic)

此后就没有什么特别的了，打开终端直接按照助教的文档配置minisql即可。
![](images/docker_minisql/2023-07-01-20-52-01.png#pic)





