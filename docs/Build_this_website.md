---
comments: true
render_macros: false
hide:
    - navigation
---
# 如何构建一个像这样的网站！

!!! abstract "网站搭建教程"
    本站点使用 mkdocs 搭建，部署于 Github Pages，使用了[:octicons-link-16:material](https://squidfunk.github.io/mkdocs-material/)主题

## 1.环境准备

安装 python
```bash
sudo apt install python3 python3-pip
```

pip 换源
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

安装 mkdocs
```bash
pip install mkdocs-material
```

出现报错：
```bash
ERROR: mkdocs 1.4.3 has requirement markdown<3.4，>=3.2.1， but you'll have markdown 3.4.3 which is incompatible.
```

修改 markdown 版本，然后重新安装 mkdocs：
```bash
pip install markdown==3.2.1
pip install mkdocs-material
```

图片处理的依赖库：
```bash
pip install pillow cairosvg
```




??? info "可选优化：yaml 补全"
    1. 安装 VSCode-yaml
    2. 把下面设置写入 settings.json:
    ```json
    {
    "yaml.schemas": {
        "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    }，
    "yaml.customTags": [
        "!ENV scalar"，
        "!ENV sequence"，
        "tag:yaml.org，2002:python/name:materialx.emoji.to_svg"，
        "tag:yaml.org，2002:python/name:materialx.emoji.twemoji"，
        "tag:yaml.org，2002:python/name:pymdownx.superfences.fence_code_format"
    ]
    }
    ```

## 2.部署到 Github Pages

新建一个空的公开仓库，并且克隆到本地，在其中新建一个 mkdocs site：
```bash
git clone repo
cd repo
mkdocs new .
```

在 mkdocs.yml 中启用主题：
```yaml
theme:
  name: material
```

如果你希望将 markdown 源文件也保存在同一个仓库里的话，先新建一个忽略`site/`的`.gitignore`文件，然后提交，推送：
```bash
echo "site/" > .gitignore
git add .
git commit -m "init"
git push -u origin master
```

然后用`gh-deploy`命令一键部署到 Github Pages:
```bash
mkdocs gh-deploy
```
现在我们的仓库有两个分支了，master 分支储存 markdown 源文件，gh-pages 分支储存编译后的网站

在 settings-pages 中可以看到网站的网址了，一般为`username.github.io/repo`，如果你创建的仓库是特殊的，名为`username.github.io`，那么网址就是`username.github.io`了
当前的网站为默认样式：
![](images/Build_this_website/2023-07-02-02-35-34.png#pic)

??? info "可选优化：自动编译部署"
    我们可以使用 GitHub action 来帮助我们每次更新 master 分支后自动编译网站并推送到 gh-pages 分支，这样我们就不用每次都手动执行`mkdocs gh-deploy`了，而只需要将新写的 markdown 推送至仓库就可以了。
    这样做的另一个好处是其他人希望对仓库做贡献的时候可以只对文本内容进行修改，而不必在乎便已部署的问题。只有当贡献者希望预览的时候需要完整的安装环境。
    1. 在仓库中新建一个`.github/workflows/auto-deploy.yml`文件，内容如下：
    ```
    name: ci
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
            with:
            fetch-depth: '0'
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
        - run: pip install  mkdocs-material mkdocs-changelog-plugin mkdocs-glightbox jieba pillow cairosvg mkdocs-tooltips mkdocs-statistics-plugin mkdocs-table-reader-plugin mkdocs-git-revision-date-localized-plugin mkdocs-meta-manager mkdocs-macros-plugin
        - run: mkdocs gh-deploy --force
    ```
    注意，推送到 Github 的话需要你的 token 有 workflow 权限
    此 Action 已经是根据本站安装的插件等进行了额外安装的，请按需使用。如果你依赖了额外的库，需要修改 Action

## 3.常规特性

### 3.1 修改网站的 css 样式

我们需要新增的样式均放置于`docs/css/`目录下，每个 css 文件都要在`mkdocs.yml`中添加：

```yaml
extra_css:
  - css/extra.css
```

??? exmaple "我使用的的样式"
    ```css
    [data-md-color-primary=P] {
        --md-primary-fg-color:  #FFACA6;
    }
    [data-md-color-accent=P] {
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
    background-color: #CC9052;
    }
    .changelog-type-newpage{
    background-color: #FF9C80;
    }
    .changelog-type-refactor::before {
    content: "文档更新";
    }

    /* 图片放大 start */
    /* .shadow {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .zoom {
    transition: transform ease-in-out 0.5s;
    cursor: zoom-in;
    }

    .image-zoom-large {
    transform: scale(1.9);
    cursor: zoom-out;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    z-index: 100;
    position: relative;
    } */
    /* 图片放大 end */



    /*图片格式设置*/
    /*默认样式*/
    img[src*="pic"] {
    box-shadow: 2px 2px 10px #666;
    border-radius: 4px;
    width: 98%;
    display: block;
    margin: 10px auto;
    }
    /*样式 1 同默认样式*/
    img[src*="pic1"] {
    box-shadow: 4px 4px 15px #666;
    border-radius: 10px;
    }

    /* beat like a heart */
    @keyframes heart {
    0%, 40%, 80%, 100% {
        transform: scale(1);
    }
    20%, 60% {
        transform: scale(1.15);
    }
    }
    .heart {
    animation: heart 1000ms infinite;
    }

    /* new admonitions */
    :root {
    --md-admonition-icon--definition: url('../icons/define.svg')
    }
    .md-typeset .admonition.definition,
    .md-typeset details.definition {
    border-color: rgb(43, 155, 70);
    }
    .md-typeset .definition > .admonition-title,
    .md-typeset .definition > summary {
    background-color: rgba(43, 155, 70, 0.1);
    }
    .md-typeset .definition > .admonition-title::before,
    .md-typeset .definition > summary::before {
    background-color: rgb(43, 155, 70);
    -webkit-mask-image: var(--md-admonition-icon--definition);
            mask-image: var(--md-admonition-icon--definition);
    }

    :root {
    --md-admonition-icon--reference: url('../icons/reference.svg')
    }
    .md-typeset .admonition.reference,
    .md-typeset details.reference {
    border-color: rgb(223, 251, 13);
    }
    .md-typeset .reference > .admonition-title,
    .md-typeset .reference > summary {
    background-color: rgba(249, 249, 90, 0.1);
    }
    .md-typeset .reference > .admonition-title::before,
    .md-typeset .reference > summary::before {
    background-color: rgb(223, 251, 13);
    -webkit-mask-image: var(--md-admonition-icon--reference);
            mask-image: var(--md-admonition-icon--reference);
    }
    /* new code highlight lines*/
    span.hll {
    width: 150%;
    }

    /*see https://xuan-insr.github.io/%E6%9D%82%E9%A1%B9/%E5%8D%9A%E5%AE%A2%E6%90%AD%E5%BB%BA%E8%AE%B0%E5%BD%95/#%E8%A7%A3%E5%86%B3%E5%85%AC%E5%BC%8F%E5%B8%A6%E7%BA%B5%E5%90%91%E6%BB%9A%E5%8A%A8%E6%9D%A1%E7%9A%84%E9%97%AE%E9%A2%98*/
    .md-typeset div.arithmatex {
    overflow-y: hidden;
    }
    ```

??? tip "自己定义样式"
    我们可能不熟悉 css，没事，我也完全不懂，对于一些简单的修改颜色修改字，直接用 F12 查看对应的样式改成自己喜欢的就好了，浏览器一般都支持直接改并且显示修改后的效果的
    另一个好用的设置就是修改默认的图片样式，我们只要像这样引用图片
    ```
    ![](images/Build_this_website/2023-07-02-02-35-34.png#pic)
    ```
    也就是在结尾加上#pic，就可以对图片应用默认样式了，我用的是圆角+阴影.这一添加的过程可以用 VSCode 插件 Paste Image 自动实现，我在[:octicons-link-16:这里](https://stormckey.github.io/Blog/VSCode-Markdown/#_2)有介绍

### 3.2 添加额外的 javascript

我们需要新增的 js 文件放置于`docs/js/`目录下，每个 js 文件都要在`mkdocs.yml`中添加：
```yaml
extra_javascript:
  - js/extra.js
```
这里的 url 可以指向网络上的 js 文件，也可以是本地的

??? exmaple "我使用的的 js"

    === "extra.js"
        ```javascript
        document.querySelectorAll('.zoom').forEach(item => {
            item.addEventListener('click'， function () {
                this.classList.toggle('image-zoom-large');
            })
        });
        ```

    === "mathjax.js"
        ```javascript
        window.MathJax = {
            tex: {
            inlineMath: [["\\("， "\\)"]]，
            displayMath: [["\\["， "\\]"]]，
            processEscapes: true，
            processEnvironments: true
            }，
            options: {
            ignoreHtmlClass: ".*|"，
            processHtmlClass: "arithmatex"
            }
        };

        document$.subscribe(() => {
            MathJax.typesetPromise()
        })
        ```

    === "tablesort.js"
        ```javascript
        document$.subscribe(function() {
            var tables = document.querySelectorAll("article table:not([class])")
            tables.forEach(function(table) {
            new Tablesort(table)
            })
        })
        ```


### 3.3 启用网站数据分析

在`mkdocs.yml`中添加：
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

随后前往 Google Analytics 注册使用，并将对应代码插入首页即可。


### 3.4 启用评论区

[:octicons-link-16:原文档](https://squidfunk.github.io/mkdocs-material/setup/setting-up-comments/)介绍的很清楚了

### 3.5 启用 blog

官方的起步[:octicons-link-16:指导](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/)很详细了，照着走就好！

## 4.其他插件与痛点解决

### 4.1 启用最新更新时间

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


### 4.2 图片放大

先安装插件：
```bash
pip install mkdocs-glightbox
```

然后加入配置：
```yaml
plugins:
  - glightbox
```


### 4.3 使用 snippets 辅助写作

在文档中我们有许多固定格式的内容，比如说我在文档中所有的连接几乎都是
```markdown
[:octicons-link-16:文字](链接)
```

或者说我所有博客的 post 的开头都是
```
---
comments: true
authors:
    - stormckey
categories:
    -
date: 2023-12-18
nostatistics: true
---
```

重复性很高。如果你像我一样使用 MacOS 的话，可以使用 raycast 的 snippet 功能来简化这一过程，例如，对于前者，我设置了如下的 snippet：

![](images/Build_this_website/20231218183828.png#pic)

这样可以在敲入！!lk 后自动转化为指定格式，插入剪切板文字并且将光标移动到指定位置。对于 post 的开头元数据，我的设置是：

![](images/Build_this_website/20231218183959.png#pic)

类似的可以设置别的 snippet。

如果你不使用 MacOS，VSCode 应该也有类似的 snippet 的功能，可以自行探索。

### 4.4 自动给插入图片设置样式

可以直接参考此篇[:octicons-link-16:博客](https://stormckey.github.io/blog/%E5%9C%A8-vscode-%E4%B8%8A%E5%86%99-markdown/#_2)中最后的为图片设置默认样式一栏

本站采用的默认样式为圆角+阴影，另带居中和更合适的间隔

### 4.5 自动中文排版优化

关于这个问题我之前写过一篇 [:octicons-link-16:博客](https://stormckey.github.io/blog/%E7%94%A8-vim-%E6%89%B9%E9%87%8F%E4%BC%98%E5%8C%96%E4%B8%AD%E6%96%87%E6%8E%92%E7%89%88/)，欢迎参考。


