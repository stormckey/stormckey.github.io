---
comments: true
authors:
    - stormckey
categories:
    - 效率
    - 环境
date: 2023-03-22
nostatistics: true
---
# Linux 终端配置
!!! abstract
    一些极大地增强 linux 终端易用性的工具

    对我来说，如果我要新开一个用一段时间的环境的话，就会把这些配置先跑一遍
<!-- more -->

## 启用 zsh
```
sudo apt install zsh
chsh -s /bin/zsh
```
重启终端（docker 中请重启容器）

## 安装 zsh 插件

安装 p10k
```
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ~/.zsh/powerlevel10k
echo 'source ~/.zsh/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```
重启 shell


安装 autosuggestion
```
git clone https://gitee.com/renkx/zsh-autosuggestions.git ~/.zsh/plugins/zsh-autosuggestions
echo '#Enable autosuggestion' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc
```

安装 syntaxhighlight
```
git clone https://gitee.com/renkx/zsh-syntax-highlighting.git ~/.zsh/plugins/zsh-syntax-highlighting
echo '#Enable syntax highlight' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc
```

安装 autojump
```
sudo apt install autojump
echo '#Enable autojump' >> ~/.zshrc
echo 'source  /usr/share/autojump/autojump.sh'>>~/.zshrc
```

## 在命令行中启用 vi
```
git clone https://github.com/soheilpro/zsh-vi-search.git ~/.zsh/plugins/zsh-vi-search
echo "#Enable vi mode" >> ~/.zshrc
echo "bindkey -v" >> ~/.zshrc
echo "source ~/.zsh/plugins/zsh-vi-search/src/zsh-vi-search.zsh" >> ~/.zshrc
```
