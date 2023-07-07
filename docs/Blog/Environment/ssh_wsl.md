---
comments: true
---
# Use SSH to Connect WSL2 in the same LAN
!!! abstract 
    基础的流程参考[:octicons-link-16:这篇博客](https://blog.csdn.net/qq_24211837/article/details/117386077)就好，本文记录一下踩的雷和更进阶的设置

## 检查通路

!!! abstract "这一步我们要检查我们到要连接的系统的网络通路是正常的"


Windows会给Wsl2分配一个虚拟的本地的地址，在Windows输入`ipconfig`以查看该地址。  
我们在Wsl中启用ssh服务后，想要验证Wsl是否可被连接，可以先在Windows中试着用ssh连接ifconfig中看到的地址

随后我们希望从局域网连接Windows也是通的，我们就用`ipconfig`得到服务器（也就是这台机器）ip，在另一台机器上（客户）尝试`ping <ip>`来试着连接，或者直接用ssh连接Windows，保证局域网到Windows这条路都是通的。 

!!! warning
    一些标明为“Secure”的局域网可能不允许局域网内连接，在这些局域网下是互相ping不通的，尝试换个局域网！这点坑了我很久。

最后我们需要确保把局域网，Windows，wsl都连接起来，需要Windows把我们从ssh发来的连接请求转到内部的wsl的端口，这样就通了。（对应的操作在上文的博客中已经提及，如果还有问题，可以尝试[:octicons-link-16:这篇](https://cloud.tencent.com/developer/article/1420930)看看是不是局域网到Windows的问题）

## 设置免密登陆
 
!!! info "免密登陆也可参考[:octicons-link-16:这篇](https://stormckey.github.io/Blog/docker_minisql/#3sshvscode)"
来到客户端，执行下面命令生成密钥，输入passephrase时直接回车（为空）

```
ssh-keygen
```

就会在提示的目录下生成密钥，选择其公钥(.pub后缀)，把它写入服务器登陆用户的ssh配置文件夹下的“authorized_keys"文件（一般为`~/.ssh/authorized_keys`），注意修改"authorized_keys"的权限改为600，所在文件夹权限改为700.

如果上述都做了之后仍然无法免密登陆，比如`ssh -v user@ip -p port`后看到连接时试图使用公钥验证但是失败了，那么需要再定位问题。在服务器端使用下列语句启用sshd监听连接某个端口
```
sudo /usr/sbin/sshd -d  -p 4444
```
注意不能使用已经被占用的端口  
启用后去powershell进行端口转发，便可以在终端里看到服务器端认证的全过程了

## 设置Wsl2静态ip

参考[:octicons-link-16:这篇](https://blog.csdn.net/weixin_41301508/article/details/108939520)

还可以顺带设置一下Wsl2开机启动和自动开始ssh服务



