---
comments: true
authors:
  - stormckey
categories:
  - 环境
  - VSCode
date: 2023-03-21
nostatistics: true
---

# 在 VSCode 中使用 conda 的虚拟环境问题

!!! abstract
用 conda 的过程中遇到的一个神秘问题 🤔

<!-- more -->

## 新方法

下面的旧方法是好久以前不知道从哪个犄角旮旯里找出来的，我使用到目前也没有问题。

但最近看到 [:octicons-link-16:建议](https://code.visualstudio.com/updates/v1_36#_launch-terminals-with-clean-environments)，试着换了其中建议的方法，发现也是可行的。

```title="请在 setting.json 中加入"
  "terminal.integrated.inheritEnv": false,
```

## 旧方法

最近开始使用 conda，试图在 VSCode 终端里切换虚拟环境，命令行提示已经切换，但是 python 环境实际上没有变。
解决方案如下：

1. 快捷键`command shift p`，搜索 settings，打开 user settings json
2. 加入如下内容：

```
    "terminal.integrated.env.osx": {
      "PATH": ""
  }，
```

3. 重启 VSCode 即可
