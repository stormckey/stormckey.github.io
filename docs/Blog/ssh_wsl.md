---
comments:true
---
# 用ssh连接同一局域网下的wsl2

## 检查通路
总体的流程[:octicons-link-16:这篇]讲得已经很清楚了，照着做就行。  

Windows会给wsl2分配一个虚拟的本地的地址，我们在wsl中输入`ifconfig`可以查看，我们启用ssh服务后，想要验证wsl是否可被连接，可以现在windows的powershell中试着用ssh连接ifconfig中看到的地址，就可以输入密码链接成功了。这是验证了从Windows到wsl的这条路是通的。  

随后我们希望从局域网连接Windows也是通的，我们就在poweshell下输入`ipconfig`得到本机ip，尝试`ping [IP]`来试着连接一下，或者直接用ssh连接一下Windows。保证局域网到Windows这条路都是通的。 

!!! warning
    一些标明为“Secure”的局域网可能不允许局域网内连接，在这些局域网下是互相ping不通的，尝试换个局域网！这点坑了笔者很久。

最后我们需要确保把局域网，Windows，wsl都连接起来，需要Windows把我们从ssh发来的连接请求转到内部的wsl的端口，这样就通了。（对应的操作在上文的博客中已经提及，如果还有问题，可以尝试[:octicons-link-16:这篇](https://cloud.tencent.com/developer/article/1420930)看看是不是局域网到Windows的问题）

## 设置免密登陆

在远程连接的发起者端执行下面命令生成密钥，注意paseephrase最好为空，否则还是要再输一遍。（注意被连接主机的sshd_config已经允许用公钥连接）

```
ssh-kengen
```

就会在提示的目录下生成密钥，选择其一的公钥(.pub)后缀，把它写入要被远程连接的主机的登陆的用户的ssh配置文件夹下的“authorized_keys"文件，注意修改"authorized_keys"的权限改为600，所在文件夹权限改为700.

如果上述都做了之后仍然无法免密登陆，比如`ssh -v user@ip -p port`后看到试图使用公钥验证但是失败了，那么需要再定位问题。使用下列语句启用sshd监听连接
```
sudo /usr/sbin/sshd -d  -p 4444
```
注意不能使用已经被占用的端口，并在启用后去powershell进行端口转发，便可以在终端里看到认证失败的具体原因了。

## wsl静态ip

参考[:octicons-link-16:这篇](https://blog.csdn.net/weixin_41301508/article/details/108939520)

注意wsl要启动并启用ssh服务



