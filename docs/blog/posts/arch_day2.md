---
comments: true
authors:
    - stormckey
categories:
    - Linux
    - Hyprland
    - Arch
date: 2024-01-20
nostatistics: true
---

# Arch Linux Day2

!!! abstract
    开始折腾 Arch Linux 的第二天！今天就是一些常规的环境配置

<!-- more -->

## 杂项

### 简单的命令行工具

用 bat 替代 cat，用 eza 代替 ls，并设置好 alias。

### 代理

本来代理这个事还挺简单的，但是前几个月 clash 一系全都删库跑路了，所以刚开始就试图找一个替代方案

找到了一个挺多人推荐的方案是使用 nekoray，相关的教程我觉得官方的文档说的不算清楚，可以去油管上看看相关的视频，比较清楚

但是对于我来说，sockboom 给的链接 nekoray 一直只能更新出 nothing，我也不太清楚是哪里的问题可能订阅链接返回的格式 nekoray 并不完全认？总之最后放弃了这个方案

最后的方案是使用 clash（没错还是它）加 webui，webui 就是时不时拿来切个节点的，clash 只要把配置文件在~/.config/clash/config.yaml(1)里面放好，然后运行 clash 就可以了。
{.annotate}

1.  `wget -O ~/.config/clash/config.yaml YOUR_SUBSCRIBE_URL`

为了全局开启代理，可以直接在/etc/environment 里面加上

```bash
http_proxy=http://127.0.0.1:7890
https_proxy=http://127.0.0.1:7890
all_proxy=http://127.0.0.1:7890
```

### python 环境

python 应该是预装的

anaconda 通过：

```bash
yay -S anaconda
```

安装

然后用 conda 安装 pip，pacman 装的 pip 疑似跟 conda 配合得不是很好

VSCode 也一并装了


