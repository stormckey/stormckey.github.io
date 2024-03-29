---
comments: true
authors:
    - stormckey
categories:
    - 环境
    - 效率
    - VSCode
date: 2023-03-23
nostatistics: true
---

# 在 VSCode 上写 Markdown
!!! abstract
    markdown 真方便啊真方便，本文讲了怎么在 VSCode 上配置一个好用的写 markdown 的环境
<!-- more -->

## 起步
首先启用以下的两个插件，就可以开始写 markdown，并在右侧预览了

![](images/VSCode-markdown/2023-03-23-14-24-20.png#pic)
??? info "效果图"
    ![](images/VSCode-markdown/2023-03-23-14-25-15.png#pic)
    ![](images/VSCode-markdown/2023-03-23-14-32-24.png#pic)
注意预览需要在编辑器右上角点击预览按钮开启或者使用快捷键

如果需要保存成 PDF 或者别的格式，在预览界面右键就好，Chrome 一栏的三个选项都是不需要额外安装的：

![](images/VSCode-markdown/2023-03-23-14-34-26.png#pic)

??? tip "数学公式渲染问题"
    有时候保存成 PDF 时会发现数学公式渲染失败了，调查了一下发现是生成的速度太快了数学公式来不及渲染，调节以下参数可以解决问题：
    ![](images/VSCode-markdown/2023-03-23-14-35-52.png#pic)

## 快捷地插入图片

就最原教旨主义的插入方式而言，需要把图片保存到指定文件夹，起好名字，再利用`![](url)`格式插入，步骤相当繁琐，跟 Word 的图片插入完全是两个量级的工作量。

推荐使用**Paste Image**插件：
![](images/VSCode-markdown/2023-03-23-14-37-41.png#pic)

修改如下的设置：
![](images/VSCode-markdown/2023-03-23-14-38-36.png#pic)
这会将图片插入到当前 md 文件下的 images/mdfilename/time.png 位置。

用系统自带的截屏工具截屏到粘贴板后 Command+Option+v 即可存入文件夹并自动引用正确的路径。
??? tip "设置默认图片样式"
    本人使用 mkdocs for material 搭建此网页，可以给此插件添加的图片添加统一样式：

    -  设置 css：比如阴影圆角等
        ``` css title="我正在使用的"
        img[src*="pic"] {
            box-shadow: 2px 2px 10px #666;
            border-radius: 4px;
            width: 98%;
            display: block;
            margin: 10px auto;
        }
        ```
    - 在 mkdocs.yml 添加 css 作为额外 css：
        ``` yaml
        extra_css:
        - css/extra.css
        ```
    - 设置 Paste Imgae 自动添加后缀：
        ``` json
        "pasteImage.suffix": "#pic"
        ```
    - 可以添加多个样式，并改变#后的名称来切换



