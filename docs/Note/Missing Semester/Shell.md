# Shell Notes (revisited)

!!! abstract "一个离散的知识列表，没有逻辑顺序"

## Tips

!!! tip "$PATH : 默认的变量，会打印出所有的路径环境变量"  
!!! tip "`>` : 重定向并覆盖写入 ; `>>` : 重定向并附加在尾部; stderr重定向要`2>file`, stderr和stdout一起重定向 `&>file`"
!!! tip "文件的执行权限"
    用`touch` `tee`新建的文件没有执行权限 ，用`ls -l`查看  
    没有权限的时候不可用`./`调用， 但可以用`source`调用，后者会在当前目录就地执行脚本  
    用`chmod +x <file>`增加执行权限

## Commands

!!! info "tee"
    ```
    tee <file1> <file2> ...[-a]
    ```
    回显同时写入文件  
    在前台运行并等待从stdin的输入; 不需要被写入的文件提前存在  
    可以用在pipeline中，解决echo在pipeline中可能引发的[[:octicons-link-16:权限问题](https://missing.csail.mit.edu/2020/course-shell/)]{在这个网页中搜索tee以查看相应描述}。 
!!! info "touch"
    ```
    touch <file1> <file2> ...
    ```
    创建几个空的新文件，或者更新已存在文件的最后更改时间。

## Syntax

!!! info "命令行参数在脚本中通过$1 $2获取,索引从1开始"

!!! info "字符串比较"
    ```
    if [ $1="Hello" ];then
    fi
    ```  
    请勿随意省略空格，if后，[]内的都不可省略; 注意;不要漏
    `=`和`==`是等价的  

!!! info "并列的字符串会自动连接： `"Hello"" World!" = "Hello World!"`"