---
comments: true
authors:
    - stormckey
categories:
    - 配环境
date: 2023-03-21
nostatistics: true

---
# 在 WSL2 上启用 CUDA
!!! abstract
    别说了，开炼！
<!-- more -->

!!! info "主要是参考了[:octicons-link-16:这篇文章](https://zhuanlan.zhihu.com/p/506477744)"

## 1.在 Windows 上安装显卡驱动
这步很简单，在[:octicons-link-16:官网](https://www.nvidia.com/Download/index.aspx?lang=en-us)上找到适合自己显卡的版本就好了.
Download Type 选项选 Game Ready Driver 就好.
想要查看自己电脑显卡型号，可以先 win+R，输入 dxdiag，选择 dispaly 就可以看到了.

## 2.在 wsl 上安装驱动
上一步结束之后`torch.cuda.is_available()`就已经 True 了，但直接执行还是会报错.
启动 wsl，执行以下命令
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-wsl-ubuntu-11-4-local/7fa2af80.pub
apt-get update
sudo apt-get -y install cuda
```
有些安装比较慢，没有换过源的可以换下国内镜像，可以用[:octicons-link-16:浙大源](http://mirrors.zju.edu.cn/)

笔者在上面的命令执行中还遇到一个问题，最后一步报错 liburcu6 没有安装.
可以在[:octicons-link-16:官方软件源](https://packages.debian.org/bullseye/liburcu6)上可以下载，浏览器可能提示下载不安全.如果可以的话，选择合适的版本下载.用`cat /proc/version` 查看我们系统的版本，x86_64 用 amd64 即可.
如果无法解决，可以用[:octicons-link-16:这里](https://askubuntu.com/questions/1407962/unable-to-install-cuda-on-ubuntu-22-04-wsl2)的方法，使用命令：
```bash
sudo add-apt-repository ppa:cloudhan/liburcu6
sudo apt update
sudo apt install liburcu6
```
第一条命令似乎需要科学上网，我没开的时候连接超时了.
随后就可以继续上一步的安装 cuda 了.安装完毕后用 nvidia-smi 命令查看是否成功.

此时仍然不能直接使用 cuda，需要再安装 nvcc，直接下载就好了.

至此安装结束.

<!-- !!! tip
    如果在使用`from mpi4py import MPI`中报错连接库找不着，可以尝试`sudo apt install libopenmpi-dev`来安装所需的库 -->
