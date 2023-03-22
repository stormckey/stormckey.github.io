# wsl终端配置

## 启用zsh
```
sudo apt install zsh
chsh -s /bin/zsh
```
重启终端

## 安装zsh插件

安装p10k
```
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```
重启shell

进入`~/.zsh/plugins`

安装autosuggestion
```
git clone https://gitee.com/renkx/zsh-autosuggestions.git
echo '#Enable autosuggestion' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc
```

安装syntaxhighlight
```
git clone https://gitee.com/renkx/zsh-syntax-highlighting.git
echo '#Enable syntax highlight' >> ~/.zshrc
echo 'source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc
```

安装autojump
```
sudo apt-get install autojump
echo '#Enable autojump' >> ~/.zshrc
echo 'source  /usr/share/autojump/autojump.sh'>>~/.zshrc
```
