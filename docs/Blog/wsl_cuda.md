---
coments: true
---
# 在wsl Ubuntu22.02上使用显卡加速

主要是参考了[:octicons-link-16:这篇文章](https://zhuanlan.zhihu.com/p/506477744)

## 在Windows上安装显卡驱动
这步很简单，在[:octicons-link-16:官网](https://www.nvidia.com/Download/index.aspx?lang=en-us)上找到适合自己显卡的版本就好了。  
Download Type选项选Game Ready Driver就好。  
想要查看自己电脑显卡型号，可以先win+R，输入dxdiag，选择dispaly就可以看到了。  

## 在wsl上安装驱动
上一步结束之后torch.cuda.is_available()就已经True了，但直接执行还是会报错。  
启动wsl，执行以下命令  
```shell
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-wsl-ubuntu-11-4-local/7fa2af80.pub
apt-get update
sudo apt-get -y install cuda
```
有些安装比较慢，没有换过源的可以换下国内镜像，可以用[:octicons-link-16:浙大源](http://mirrors.zju.edu.cn/)  

笔者在上面的命令执行中还遇到一个问题，最后一步报错liburcu6没有安装。  
可以在[:octicons-link-16:官方软件源](https://packages.debian.org/bullseye/liburcu6)上可以下载，但是浏览器提示下载不安全。如果可以的话，选择合适的版本。  
用`cat /proc/version` 查看版本，x86_64用amd64即可。  
最后采用的方式是在[:octicons-link-16:这里](https://askubuntu.com/questions/1407962/unable-to-install-cuda-on-ubuntu-22-04-wsl2)找到了，用命令：  
```
sudo add-apt-repository ppa:cloudhan/liburcu6
sudo apt update
sudo apt install liburcu6
```
第一条命令似乎需要科学上网，我没开的时候连接超时了。  
随后就可以安装cuda了。安装完毕后用nvidia-smi命令查看是否成功。(仍提示找不到命令的话，再按照提示安装)

此时仍然不能直接使用cuda，需要再安装nvcc，因为上面安装的是最新版的cuda，这里也不用控制版本，直接下载就好了。  

至此安装结束。

## pytorch
这不很简单，直接用pip安装即可，建议使用venv，防止环境混乱。

!!! tip 
    如果在使用`from mpi4py import MPI`中发生连接库找不着了，可以尝试`sudo apt install libopenmpi-dev`来安装所需的库