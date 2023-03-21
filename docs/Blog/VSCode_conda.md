---
comments: true
---
# VSCode 终端里无法启用conda虚拟环境

最近用上了conda，在VSCode终端里切换虚拟环境，可以看到命令行提示符已经切换，但是python环境仍然是默认的，导致提示module not found.解决方案如下：

- 打开`command ,`，然后打开settings.json
- 加入如下内容：
  ```
      "terminal.integrated.env.osx": {
        "PATH": ""
    }
  ```
- 重启VSCode即可
