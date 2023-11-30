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
ERROR: mkdocs 1.4.3 has requirement markdown<3.4,>=3.2.1, but you'll have markdown 3.4.3 which is incompatible.
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

在 settings-pages 中可以看到网站的网址了，一般为`username.github.io/repo`,如果你创建的仓库是特殊的，名为`username.github.io`，那么网址就是`username.github.io`了
当前的网站为默认样式：
![](images/Build_this_website/2023-07-02-02-35-34.png#pic)

??? info "可选优化：自动编译部署"
    我们可以使用 GitHub action 来帮助我们每次更新 master 分支后自动编译网站并推送到 gh-pages 分支，这样我们就不用每次都手动执行`mkdocs gh-deploy`了。
    1. 在仓库中新建一个`.github/workflows/auto-deploy.yml`文件，内容如下：
    ```yaml
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
        - run: pip install  mkdocs-material mkdocs-changelog-plugin mkdocs-glightbox jieba pillow cairosvg mkdocs-tooltips mkdocs-statistics-plugin mkdocs-table-reader-plugin mkdocs-git-revision-date-localized-plugin
        - run: mkdocs gh-deploy --force
    ```
    注意，推送到 Github 的话需要你的 token 有 workflow 权限
    如果你依赖了额外的库，需要修改 action

## 3.添加特性

### 3.1 修改网站的 css 样式

我们需要新增的样式君放置于`docs/css/`目录下，每个 css 文件都要在`mkdocs.yml`中添加：

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
    我们可能不熟悉 css，没事，我也完全不懂，对于一些简单的修改颜色修改字，直接用 F12 查看对应的样式改成自己喜欢的就好了，浏览器一般都支持直接改并且显示修改后的效果的
    另一个好用的设置就是修改默认的图片样式，我们只要像这样引用图片
    ```
    ![](images/Build_this_website/2023-07-02-02-35-34.png#pic)
    ```
    也就是在结尾加上#pic,就可以对图片应用默认样式了，我用的是圆角+阴影。这一添加的过程可以用 VSCode 插件 Paste Image 自动实现，我在[:octicons-link-16:这里](https://stormckey.github.io/Blog/VSCode-Markdown/#_2)有介绍

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

### 3.3 添加全局脚注

所有脚注都放在`includes/abbreviatioins.md`（在 docs 之外），格式为：
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

### 3.4 启用网站数据分析

在`mkdocs.yml`中添加：
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

随后前往 Google Analytics 注册使用即可。

!!! warning "启用这项功能需要向每个网页注入 google code"

### 3.5 启用最新更新时间

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

### 3.6 启用评论区

[:octicons-link-16:原文档](https://squidfunk.github.io/mkdocs-material/setup/setting-up-comments/)介绍的很清楚了

### 3.7 从文件读取表格

参考[:octicons-link-16:原文档](https://squidfunk.github.io/mkdocs-material/reference/data-tables/#import-table-from-file)

### 3.8 使用 emojis 和 icons

这个[:octicons-link-16:链接](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search)可以搜索 emoji

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

### 3.10 启用 blog

官方的起步[:octicons-link-16:指导](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/)很详细了，照着走就好！

### 3.11 我的所有配置

以下附上我的`mkdocs.yml`文件，已经删去了导航部分，所以可以直接复制使用：
??? example "mkdocs.yml"
    ```yaml
    # Project information
    site_name: Stormckey's Page
    site_url: https://stormckey.github.io/
    site_author: Stormckey
    # Repository
    repo_name: stormckey
    repo_url: https://github.com/stormckey/stormckey.github.io

    # The path to edit the content
    edit_uri: edit/main/docs/

    # Copyright
    copyright: Copyright &copy; stormckey

    theme:
    name: material
    custom_dir: overrides
    favicon: cat.svg # put in /docs/cat.svg
    font:
        text: Roboto Mono
        code: Roboto Mono
    features:
        - content.action.edit # enable the button to edit the source code of the page
        - content.action.view # enable the button to view the source code of the page
        - content.code.copy # enable the button to copy the code block
        - navigation.tabs  # enable the row of tabs under the title
        # - navigation.sections # unfold the secondary titles to the left
        # - navigation.footer # enable the next and previous button
        - navigation.indexes # the index page will be incoperate into the tab
        - search.suggest # auto suggestion
        - search.highlight # highlight when search
        - search.share # enable share when search
        - navigation.instant # optimize loading
        - navigation.tracking # URL will change as we scroll down
        - toc.follow # the sidebar will scroll automatically following the user
        - navigation.top # button to back to the top
    palette: # my customized schema
        - media: "(prefers-color-scheme: light)"
        scheme: default
        primary: indigo
        accent: indigo
        toggle:
            icon: material/brightness-7
            name: Switch to dark mode
        - media: "(prefers-color-scheme: dark)"
        scheme: slate
        toggle:
            icon: material/brightness-4
            name: Switch to light mode
    icon:
        repo: fontawesome/brands/github-alt # the github cat icon in the topright
        logo: material/cat # the cat icon in the topleft

    plugins:
    - search
    # - social: #social card
    #     enabled: !ENV [CI, false]
    #     cards: !ENV [CI, false]
    #     cards_font: Noto Sans SC
    - git-revision-date-localized:
        enabled: !ENV [CI, false]
        enable_creation_date: true
    - offline: # enable searching offline
        enabled: !ENV [OFFLINE, false]
    - table-reader
    - changelog #see https://github.com/TonyCrane/mkdocs-changelog-plugin
    - tooltips
    - statistics
    - glightbox



    markdown_extensions:
    #enable admonition
    - admonition
    - pymdownx.details # enable ??? admonition
    - pymdownx.betterem # better emphasize
    - pymdownx.superfences: # allow nest codes
        custom_fences:
            - name: mermaid
            class: mermaid
            format: !!python/name:pymdownx.superfences.fence_code_format
    #enable code config
    - pymdownx.inlinehilite #inline code highlight
    - pymdownx.snippets: #enable to embed arbitrary files
        auto_append:
            - includes/abbreviations.md
    - pymdownx.highlight:
            linenums: true # enable line display
            line_spans: __span
            pygments_lang_class: true # detect language automatically
            anchor_linenums: true # offer line anchor
    - pymdownx.keys # render key symbols
    - pymdownx.smartsymbols
    #enable button
    - attr_list
    #enable content tabs
    - pymdownx.tabbed:
        alternate_style: true
    - tables
    #daigrams are not enabled
    - footnotes
    #enable emoji
    - pymdownx.emoji:
        emoji_index: !!python/name:materialx.emoji.twemoji
        emoji_generator: !!python/name:materialx.emoji.to_svg
        options:
            custom_icons:
            - "overrides/.icons"
    #image alignment
    - md_in_html
    #better list
    - def_list
    - pymdownx.tasklist:
        custom_checkbox: true
    #abbr
    - abbr
    #enable math syntax
    - pymdownx.arithmatex:
        generic: true
    #enable table of content
    - toc:
        permalink: true
        permalink_title: Anchor link to this section for reference
    - pymdownx.caret
    - pymdownx.mark
    - pymdownx.tilde
    - pymdownx.critic

    extra_javascript:
    - javascripts/extra.js
    - javascripts/mathjax.js
    - https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js # enable table sort
    - javascripts/tablesort.js # enable table sort
    - https://polyfill.io/v3/polyfill.min.js?features=es6
    - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

    extra:
    social:
        - icon: fontawesome/brands/github # icons to the right bottom of the page
        link: https://github.com/stormckey
        - icon: fontawesome/solid/paper-plane # icons to the right bottom of the page
        link: mailto:sortygraph@gmail.com
    alternate: # change the language, the link should point to different directories
        - name: English
        link: /
        lang: en
        - name: 中文
        link: /
        lang: zh
    consent:
        title: Cookie consent
        description: >-
        We use cookies to recognize your repeated visits and preferences, as well
        as to measure the effectiveness of our documentation and whether users
        find what they're searching for. With your consent, you're helping us to
        make our documentation better.
    analytics:
        provider: google
        property: G-XXXXXXXXXX

    extra_css:
    - css/hint.min.css
    - css/extra.css
    ```

### 3.x 更多特性（我还不会用但考虑启用的）

1. 自定义 html 样式[:octicons-link-16:](https://squidfunk.github.io/mkdocs-material/customization/#extending-the-theme)
