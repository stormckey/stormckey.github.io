---
comments: true
---
# 启用chatGPT_academic

!!! info
    请在阅读此文前准备好ChatGPT的API Key和好用的代理。（前者主要是注册好账号就行，合理利用https://sms-activate.org/）

主要的流程就在项目的[:octicons-link-16:源地址](https://github.com/binary-husky/chatgpt_academic)讲的很详细了,照做即可。

笔者没有用docker部署，部署过程中只遇到一个问题，换过源后pip找不到高版本的gradio
![](images/GPT_academic/2023-03-29-01-35-34.png#pic)  

解决方案是：
```
pip install --upgrade gradio -i https://pypi.org/simple
```

建议使用虚拟环境。
