# Data wrangling

!!! abstract "本节列举一些命令行常用的数据处理工具，不试图保持逻辑连贯"

## Sed
Sed是 Stream editor 流编辑器

!!! info "用Sed替换"
    `Sed 's/REGEX/SUBSTITUTION/'`

!!! info "简单的正则表达式"
    - 正则表达式可以实现字符串匹配，大部分自负都保持愿意除了一些特殊的
    - `.` 代表除了换行任何的单字符
    - `*` 前一个重复0-无限次
    - `+` 前一个重复1-无限次
    - `[abc]` abc任意一个
    - `(RX1|RX2)` 表达式一或者二
    - `^` 行首
    - `$` 行尾
    - `()` 捕获，位于补货内的字符串可在被替代部分用\1 \2 \3 引用
!!! warning "Sed中使用特殊符号需要先导\ 或者传递参数-E"

## Awk
Awk 是另一个强大的流编辑器

!!! info "只有一些简单的应用"
    - `<condition> {<manipulation>}`:条件语句
    - `{print $2}`: 打印一行中的第2块字符串
    - `$n ~/REGEX/`: 检测是否匹配正则
    - `BEGIN {manipulation1} <...> END{manipulation2}`: 输入初始行懂；遍历；输入结尾行动

## Aided Command line Tools

!!! info "辅助使用的命令行工具"
    - grep: 筛选出含有制定内容的行
    - sort: 排序
    - uniq: 去重
    - tail: 截图头部几条
    - head: 截取尾部几条
    - paste: 通过指定的间隔字符链连接两行
    - bc: 计算器
    - xargs: 把stdin转换为参数调用后续程序