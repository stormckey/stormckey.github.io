---
comments: true
authors:
    - stormckey
categories:
    - Cool
date: 2023-03-23
nostatistics: true
render_macros: false
---

# 配置 Github Profile
!!! abstract
    我配置 Github 主页 Profile 的方案，灵感来自[:octicons-link-16:Tonycrane 的 GitHub 主页](https://github.com/TonyCrane)
<!-- more -->


## 启用 Github 主页 Profile
我们先创建一个跟自己账号同名的公开仓库，这是一个特殊的用作主页仓库
Github 会在主页上显示这一仓库的 README 文档作为 Profile，所以我们只要编写这个 README 文档即可
??? "本人主页预览"
    ![](images/github_profile/2023-03-23-14-49-05.png#pic)


## 启用 Metrics 生成 Profile 图片

推荐使用[:octicons-link-16:Metrics](https://github.com/lowlighter/metrics/blob/master/.github/readme/partials/documentation/setup/action.md)来生成好看的 Profile

Metrics 使用 GitHub Action 自动更新，我们只要照着链接里的介绍就可以完成部署。Metrics 还支持许多不同的[:octicons-link-16:插件](https://github.com/lowlighter/metrics/blob/master/README.md)，大家可以随意选择自己喜欢的，最后贴上笔者注释的的 Action 配置和 README 源代码，欢迎借鉴使用！

??? info "参考配置"

    === "Metrics.yml"

        ``` yaml
        name: Metrics
        on:
        # Schedule updates per hour
        schedule: [{cron: "0 * * * *"}]
        # (optional) Run workflow manually
        workflow_dispatch:
        # (optional) Run workflow when pushing on master/main
        push: {branches: ["master", "main"]}
        jobs:
        #generate the left picture
        github-left-metrics:
            runs-on: ubuntu-latest
            permissions:
            contents: write
            steps:
            - name: left
                # use the official generator
                uses: lowlighter/metrics@latest
                with:
                token: ${{ secrets.METRICS_TOKEN }}

                # the file this action generates
                filename: matrics-left.svg
                config_timezone: Asia/Shanghai


                # enable plugins
                plugin_followup: yes


                plugin_languages: yes
                # repositories that wont be accounted
                plugin_languages_skipped: stormckey/dotfiles
                plugin_languages_ignored: html, css, ruby, perl, javascript
                # show the size of source code and percentage of each language
                plugin_languages_details: bytes-size, percentage


                plugin_starlists: yes
                plugin_starlists_languages: yes


                config_order: followup, languages, starlists

        github-right-metrics:
            runs-on: ubuntu-latest
            permissions:
            contents: write
            steps:
            - name: right
                uses: lowlighter/metrics@latest
                with:
                #disable the basic metrics
                base: ""
                token: ${{ secrets.METRICS_TOKEN }}
                filename: matrics-right.svg
                config_timezone: Asia/Shanghai

                plugin_topics: yes
                plugin_topics_mode: icons


                plugin_isocalendar: yes


                plugin_anilist: yes
                plugin_anilist_user: stormckey
                plugin_anilist_sections: favorites, characters


                config_order: topics, isocalendar, anilist


        ```
    === "README.md"

        ``` html

        <h3 align="center"> Stormckey </h3>

        <p align="center">
        <samp>
            <a href="https://stormckey.github.io/">home page</a> ∙
        </samp>
        </p>

        <p align="center">
        <a href="https://github.com/stormckey">
            <img width="400" align="top" src="https://github.com/stormckey/stormckey/blob/main/matrics-left.svg" />
        </a>
        &emsp;
        <a href="https://github.com/stormckey">
            <img width="400" align="top" src="https://github.com/stormckey/stormckey/blob/main/matrics-right.svg" />
        </a>
        </p>

        ```
