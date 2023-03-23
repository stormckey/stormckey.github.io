---
comments:true
---
# 用VSCode写Markdown

## 起步

首先启用以下的两个插件，就可以开始写markdown，并在右侧预览了

![](images/VSCode-markdown/2023-03-23-14-24-20.png)
??? info "效果图"
    ![](images/VSCode-markdown/2023-03-23-14-25-15.png)
    编写数学公式也没问题：
    ![](images/VSCode-markdown/2023-03-23-14-32-24.png)
注意预览需要在编辑器右上角点击预览按钮开启或者使用快捷键

如果需要保存成PDF或者别的格式，在预览界面右键就好，Chrome一栏的三个选项都是不需要额外安装的：

![](images/VSCode-markdown/2023-03-23-14-34-26.png)

??? tip "数学公式渲染问题"
    有时候保存成PDF时会发现数学公式渲染失败了，调查了一下发现是生成的速度太快了数学公式来不及渲染，调节以下参数可以解决问题：
    ![](images/VSCode-markdown/2023-03-23-14-35-52.png)

## 快捷地插入图片

就最原教旨主义的插入方式而言，需要把图片保存到指定文件夹，起好名字，再利用`![](url)`格式插入，步骤相当繁琐，跟Word的图片插入完全是两个量级的工作量。

推荐使用**Paste Image**插件：
![](images/VSCode-markdown/2023-03-23-14-37-41.png)

修改如下的设置：
![](images/VSCode-markdown/2023-03-23-14-38-36.png)
这会将图片插入到当前md文件下的images/mdfilename/time.png位置。

用系统自带的截屏工具截屏到粘贴板后Command+Option+v即可存入文件夹并自动引用正确的路径。
