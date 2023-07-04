---
comments: true
hide:
    - navigation
---
# 如何构建一个像这样的网站！

!!! abstract "网站搭建教程"
    本站点使用mkdocs搭建，部署于Github Pages，使用了[:octicons-linkk-16:material](https://squidfunk.github.io/mkdocs-material/)主题

## 1.环境准备

安装python
```bash
sudo apt install python3 python3-pip
```

pip换源
```bash
pip install pip -U
pip config set global.index-url https://mirrors.zju.edu.cn/pypi/web/simple
```

启用虚拟环境：
```bash
sudo apt install python3.8-venv
pip install virtualenv
python -m venv webenv
source webenv/bin/activate
```

安装mkdocs
```bash
pip install mkdocs-material
```

出现报错：
```bash
ERROR: mkdocs 1.4.3 has requirement markdown<3.4,>=3.2.1, but you'll have markdown 3.4.3 which is incompatible.
```

修改markdown版本,然后重新安装mkdocs：
```bash
pip install markdown==3.2.1
pip install mkdocs-material
```

图片处理的依赖库：
```bash
pip install pillow cairosvg
```




??? info "可选优化：yaml补全"
    1. 安装VSCode-yaml  
    2. 把下面设置写入settings.json:
    ```json
    {
    "yaml.schemas": {
        "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    },
    "yaml.customTags": [ 
        "!ENV scalar",
        "!ENV sequence",
        "tag:yaml.org,2002:python/name:materialx.emoji.to_svg",
        "tag:yaml.org,2002:python/name:materialx.emoji.twemoji",
        "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
    ]
    }
    ```

## 2.部署到Github Pages

新建一个空的公开仓库，并且克隆到本地，在其中新建一个mkdocs site：
```bash
git clone repo
cd repo
mkdocs new .
```

在mkdocs.yml中启用主题：
```yaml
theme:
  name: material
```

如果你希望将markdown源文件也保存在同一个仓库里的话，先新建一个忽略`site/`的`.gitignore`文件，然后提交，推送：
```bash
echo "site/" > .gitignore
git add .
git commit -m "init"
git push -u origin master
```

然后用`gh-deploy`命令一键部署到Github Pages:
```bash
mkdocs gh-deploy
```
现在我们的仓库有两个分支了，master分支储存markdown源文件，gh-pages分支储存编译后的网站

在settings-pages中可以看到网站的网址了，一般为`username.github.io/repo`,如果你创建的仓库是特殊的，名为`username.github.io`，那么网址就是`username.github.io`了  
当前的网站为默认样式：
![](images/Build_this_website/2023-07-02-02-35-34.png#pic)

??? info "可选优化：自动编译部署"
    我们可以使用GitHub action来帮助我们每次更新master分支后自动编译网站并推送到gh-pages分支，这样我们就不用每次都手动执行`mkdocs gh-deploy`了。
    1. 在仓库中新建一个`.github/workflows/auto-deploy.yml`文件，内容如下：
    ```yaml
    name: auto-deploy
    on:
    push:
        branches:
        - master 
        - main
    permissions:
    contents: write
    jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
            with:
            python-version: 3.x
        - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV 
        - uses: actions/cache@v3
            with:
            key: mkdocs-material-${{ env.cache_id }}
            path: .cache
            restore-keys: |
                mkdocs-material-
        - run: pip install mkdocs-material 
        - run: mkdocs gh-deploy --force
    ```
    注意，推送到Github的话需要你的token有workflow权限  
    如果你依赖了额外的库，需要修改action

## 3.添加特性

### 3.1 修改网站的css样式

我们需要新增的样式君放置于`docs/css/`目录下,每个css文件都要在`mkdocs.yml`中添加：

```yaml
extra_css:
  - css/extra.css
```

??? exmaple "我使用的的样式"
    ```css
    [data-md-color-primary=indigo] {
        --md-primary-fg-color:  #FFACA6;
    }
    [data-md-color-accent=indigo] {
    --md-accent-fg-color: #FFACA6;
    }
    [data-md-color-scheme=default] {
        --md-typeset-a-color: #000000;
        --my-changlog-color: #EFEFEF;
    }
    [data-md-color-scheme=slate] {
        --md-typeset-a-color: #FFFFFF;
        --my-changlog-color: #161616;
    }
    .md-grid {
    max-width: 1400px; 
    }/* make the page wider */
    /* changelog config*/
    .timeline-card{
    background-color: var(--my-changlog-color); 
    }
    .timeline-content::before{
    background-color: var(--my-changlog-color); 
    } 
    .changelog-type{
    background-color: #CC8A85;
    }
    .changelog-type-newpage{
    background-color: #FF9C80;
    }
    .changelog-type-refactor::before {
    content: "文档更新";
    }

    /*图片格式设置*/
    /*默认样式*/
    img[src*="pic"] {
    box-shadow: 2px 2px 10px #666;
    border-radius: 4px;
    }
    ```

??? tip "自己定义样式"
    我们可能不熟悉css，没事，我也完全不懂，对于一些简单的修改颜色修改字，直接用F12查看对应的样式改成自己喜欢的就好了，浏览器一般都支持直接改并且显示修改后的效果的  
    另一个好用的设置就是修改默认的图片样式，我们只要像这样引用图片
    ```
    ![](images/Build_this_website/2023-07-02-02-35-34.png#pic)
    ```
    也就是在结尾加上#pic,就可以对图片应用默认样式了，我用的是圆角+阴影。这一添加的过程可以用VSCode插件Paste Image自动实现，我在[:octicons-link-16:这里](https://stormckey.github.io/Blog/VSCode-Markdown/#_2)有介绍

### 3.2 添加额外的javascript

我们需要新增的js文件放置于`docs/js/`目录下,每个js文件都要在`mkdocs.yml`中添加：
```yaml
extra_javascript:
  - js/extra.js
```
这里的url可以指向网络上的js文件，也可以是本地的

??? exmaple "我使用的的js"
    === "extra.js"
        ```javascript
        document.querySelectorAll('.zoom').forEach(item => {
            item.addEventListener('click', function () {
                this.classList.toggle('image-zoom-large');
            })
        });
        ```
    === "mathjax.js"
        ```javascript
        window.MathJax = {
            tex: {
            inlineMath: [["\\(", "\\)"]],
            displayMath: [["\\[", "\\]"]],
            processEscapes: true,
            processEnvironments: true
            },
            options: {
            ignoreHtmlClass: ".*|",
            processHtmlClass: "arithmatex"
            }
        };
        
        document$.subscribe(() => { 
            MathJax.typesetPromise()
        })
        ```
    === tablesort.js
        ```javascript
        document$.subscribe(function() {
            var tables = document.querySelectorAll("article table:not([class])")
            tables.forEach(function(table) {
            new Tablesort(table)
            })
        })
        ```

### 3.3添加全局脚注

所有脚注都放在`includes/abbreviatioins.md`(在docs之外)，格式为：
```md
*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium
```

在`mkdocs.yml`中添加：
```yaml
markdown_extensions:
    - abbr
    - attr_list
    - pymdownx.snippets
    - pymdownx.snippets:
        auto_append:
            - includes/abbreviations.md
```

??? example "效果图"

### 3.4启用网站数据分析

在`mkdocs.yml`中添加：
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

随后前往Google Analytics注册使用即可。

!!! warning "启用这项功能需要向每个网页注入google code"

### 3.5启用最新更新时间

安装库：
```bash
pip install mkdocs-git-revision-date-localized-plugin
```
添加设置到`mkdocs.yml`：
```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
```

### 3.6启用评论区
    
[:octicons-link-16:原文档](https://squidfunk.github.io/mkdocs-material/setup/setting-up-comments/)介绍的很清楚了

### 3.7从文件读取表格

参考[:octicons-link-16原文档:](https://squidfunk.github.io/mkdocs-material/reference/data-tables/#import-table-from-file)

### 3.8使用emojis和icons

这个[:octicons-link-16:链接](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search)可以搜索emoji

### 3.9 图片放大

先安装插件：
```bash
pip install mkdocs-glightbox
```

然后加入配置：
```yaml
plugins:
  - glightbox
```

### 3.x更多特性（我还不会用但考虑启用的）

1. 自定义html样式[:octicons-link-16:](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme)