---
comments: true
authors:
    - stormckey
categories:
    - Environment
date: 2023-03-21
nostatistics: true
---
# 在 VSCode 中使用 conda 的虚拟环境问题
<!-- more -->

最近开始使用 conda，试图在 VSCode 终端里切换虚拟环境，命令行提示已经切换，但是 python 环境实际上没有变。
解决方案如下：

1. 快捷键`command shift p`，搜索 settings，打开 user settings json
2. 加入如下内容：
  ```
      "terminal.integrated.env.osx": {
        "PATH": ""
    },
  ```
3. 重启 VSCode 即可
