---
comments: true
---
# Linux终端配置

## 启用zsh
```
sudo apt install zsh
chsh -s /bin/zsh
```
重启终端(docker中请重启容器)

## 安装zsh插件

安装p10k
```
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ~/.zsh/powerlevel10k
echo 'source ~/.zsh/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```
重启shell


安装autosuggestion
```
git clone https://gitee.com/renkx/zsh-autosuggestions.git ~/.zsh/plugins/zsh-autosuggestions
echo '#Enable autosuggestion' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc
```

安装syntaxhighlight
```
git clone https://gitee.com/renkx/zsh-syntax-highlighting.git ~/.zsh/plugins/zsh-syntax-highlighting
echo '#Enable syntax highlight' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc
```

安装autojump
```
sudo apt install autojump
echo '#Enable autojump' >> ~/.zshrc
echo 'source  /usr/share/autojump/autojump.sh'>>~/.zshrc
```

## 在命令行中启用vi
```
git clone https://github.com/soheilpro/zsh-vi-search.git ~/.zsh/plugins/zsh-vi-search
echo "#Enable vi mode" >> ~/.zshrc
echo "bindkey -v" >> ~/.zshrc
echo "source ~/.zsh/plugins/zsh-vi-search/src/zsh-vi-search.zsh" >> ~/.zshrc
```