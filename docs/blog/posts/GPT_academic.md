---
comments: true
authors:
    - stormckey
categories:
    - Cool
date: 2023-03-28
nostatistics: true
---
# Enable ChatGPT_academic
!!! abstract
    逛大街的时候偶然看到的工具，跑起来用用看！
<!-- more -->
!!! info "准备工作"
    请在阅读此文前准备好 ChatGPT 的 API Key 和好用的代理.（前者主要是注册好账号就行，合理利用 https://sms-activate.org/）

主要的流程就在项目的[:octicons-link-16:源地址](https://github.com/binary-husky/chatgpt_academic)讲的很详细了，照做即可。

笔者没有用 docker 部署，部署过程中只遇到一个问题，换过源后 pip 找不到高版本的 gradio
![](images/GPT_academic/2023-03-29-01-35-34.png#pic)



解决方案是：

```bash
pip install --upgrade gradio -i https://pypi.org/simple
```

!!! tip "-i 是 --index-url 的缩写，意思是从指定源下载"
