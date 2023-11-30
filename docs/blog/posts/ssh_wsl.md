---
comments: true
authors:
    - stormckey
categories:
    - 配环境
date: 2023-03-22
nostatistics: true

---
# 用 ssh 连接同一局域网下的 Wsl2
!!! abstract
    为什么会有这个需求，因为我大学入学带的电脑室是一个续航稀碎的巨重的游戏本，后来有了 mac 之后游戏本基本成台式了（不是）,用 ssh 连上去主要是用一下显卡啥的
<!-- more -->
!!! abstract
    基础的流程参考[:octicons-link-16:这篇博客](https://blog.csdn.net/qq_24211837/article/details/117386077)就好，本文记录一下踩的雷和更进阶的设置

## 检查通路

!!! abstract "这一步我们要检查我们到要连接的系统的网络通路是正常的"


Windows 会给 Wsl2 分配一个虚拟的本地的地址，在 Windows 输入`ipconfig`以查看该地址。
我们在 Wsl 中启用 ssh 服务后，想要验证 Wsl 是否可被连接，可以先在 Windows 中试着用 ssh 连接 ifconfig 中看到的地址

随后我们希望从局域网连接 Windows 也是通的，我们就用`ipconfig`得到服务器（也就是这台机器）ip，在另一台机器上（客户）尝试`ping <ip>`来试着连接，或者直接用 ssh 连接 Windows，保证局域网到 Windows 这条路都是通的。

!!! warning
    一些标明为“Secure”的局域网可能不允许局域网内连接，在这些局域网下是互相 ping 不通的，尝试换个局域网！这点坑了我很久。

最后我们需要确保把局域网，Windows，wsl 都连接起来，需要 Windows 把我们从 ssh 发来的连接请求转到内部的 wsl 的端口，这样就通了。（对应的操作在上文的博客中已经提及，如果还有问题，可以尝试[:octicons-link-16:这篇](https://cloud.tencent.com/developer/article/1420930)看看是不是局域网到 Windows 的问题）

## 设置免密登陆

!!! info "免密登陆也可参考[:octicons-link-16:这篇](https://stormckey.github.io/Blog/docker_minisql/#3sshvscode)"
来到客户端，执行下面命令生成密钥，输入 passephrase 时直接回车（为空）

```
ssh-keygen
```

就会在提示的目录下生成密钥，选择其公钥（.pub 后缀），把它写入服务器登陆用户的 ssh 配置文件夹下的“authorized_keys"文件（一般为`~/.ssh/authorized_keys`），注意修改"authorized_keys"的权限改为 600，所在文件夹权限改为 700.

如果上述都做了之后仍然无法免密登陆，比如`ssh -v user@ip -p port`后看到连接时试图使用公钥验证但是失败了，那么需要再定位问题。在服务器端使用下列语句启用 sshd 监听连接某个端口
```
sudo /usr/sbin/sshd -d  -p 4444
```
注意不能使用已经被占用的端口
启用后去 powershell 进行端口转发，便可以在终端里看到服务器端认证的全过程了

## 设置 Wsl2 静态 ip

参考[:octicons-link-16:这篇](https://blog.csdn.net/weixin_41301508/article/details/108939520)

还可以顺带设置一下 Wsl2 开机启动和自动开始 ssh 服务



