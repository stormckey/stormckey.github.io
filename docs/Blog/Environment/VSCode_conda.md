---
comments: true
---
# 在VSCode中使用conda的虚拟环境问题

最近开始使用conda，试图在VSCode终端里切换虚拟环境，命令行提示已经切换，但是python环境实际上没有变。  
解决方案如下：

1. 快捷键`command shift p`，搜索settings，打开user settings json
2. 加入如下内容：
  ```
      "terminal.integrated.env.osx": {
        "PATH": ""
    },
  ```
3. 重启VSCode即可