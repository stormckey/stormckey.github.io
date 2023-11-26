---
comments: true
---
# 用 Mac 的 VSCode 调试 C/C++程序

!!! info "环境"
    MacOS: Ventura 13.2.1
    VSCode: 1.76.2 x64
    C/C++: 1.14.5
    CodeLLDB: 1.8.0
    Code Runner: 0.12.0

## C/C++

这是一个 VSCode 插件，启用后，会在 VSCode 中添加 C/C++的语法高亮、代码提示、代码跳转等功能。
同时右上角出现如下图标：
![](images/Mac_VSC_DEBUG/2023-04-05-23-25-33.png#pic)

选择 run 的话，插件就会接着让我们选择使用的编译器
![](images/Mac_VSC_DEBUG/2023-04-05-23-26-52.png#pic)

比如我选择 clang++，那么插件就会在当前工作区下自动生成相应的配置文件，并开始运行。

对于调试，很遗憾的是，我们的程序是运行在 Debug Console 中的，而不是终端中，运行在 debug console 中的问题是没有 stdin 让我们输入。

经过查询，发现 Mac 上 C/C++插件不支持 debugger 运行在内置终端中，setting 里也没有修改选项，只能运行在 debug console 或者外部终端。详见[:octicons-link-16:官网](https://code.visualstudio.com/docs/cpp/launch-json-reference)
![](images/Mac_VSC_DEBUG/2023-04-05-23-32-55.png#pic)


如果希望在外部终端运行进行输入的话，我们要在 launch.json 中配置。注意，当前版本默认配置文件只会生成 task.json,没有 launch.json：
![](images/Mac_VSC_DEBUG/2023-04-05-23-34-15.png#pic)

那我们就先介绍一下 task.json.这里的一些参数是可以修改的，比如 args，就是编译时的参数，其中`-g`参数，会让编译器生成调试信息，这样才能进行 debug。还有 cwd 参数，运行程序的文件夹位置，如果不写的话，就会默认在当前工作区的根目录下运行，而非程序所在目录，这在一些打开文件的操作上可能会导致问题。最后注意一下 label，我们可以在别的配置文件中通过这个 label 来调用这个 task。

我们新建一个配置文件 launch.json：选择侧栏的 debug 图标，点击`create a launch.json file`:
![](images/Mac_VSC_DEBUG/2023-04-05-23-38-02.png#pic)

刚开始是空的，什么都没有。点击右下角的`Add Configuration`，就有一些选项，这里有插件为我们准备的默认模版，我们选择`C/C++ lldb（启动）`，意思是 C/C++插件提供的，启动一个新的可执行文件并对其 debug 的配置，选择附加的话是附加到一个已经在执行的进程上的：
![](images/Mac_VSC_DEBUG/2023-04-05-23-39-19.png#pic)

默认的模板长这个样子：
![](images/Mac_VSC_DEBUG/2023-04-05-23-40-26.png#pic)

这并不能直接使用，首先修改 program 为
```
"program": "${workspaceFolder}/${fileBasenameNoExtension}",
```
，这样他运行的就会是当前目录下的当前文件（一般就是光标悬停的那个文件）同名的可执行文件（意思就是没后缀），如果我们编译出来的可执行文件叫做`a.out`，这个配置就不适用（会调用`a`），请在配置中修改为`/a.out`或者让编译出来的可执行文件名为`a`。

新加一列`preLaunchTask`，值就是之前 task.json 上的 label，这样就会在运行前可执行文件前先运行 task 编译当前文件（这样比较方便，自动把最新的源代码编译，要多文件编译的话也在 task 设置。如果不使用 task 手动编译的话，记得加上-g）。最后，我们要把`"externalConsole": false,`改为`"externalConsole": true,`，这样就会在外部终端中运行了。
![](images/Mac_VSC_DEBUG/2023-04-05-23-45-03.png#pic)

笔者到这一步就可以在外部终端 debug 啦，也可以在 watch 窗口执行命令来监视变量，如全局变量一类的，但是 C/C++对一些类型的变量的监视支持不是很好，比如说 string：
![](images/Mac_VSC_DEBUG/2023-04-05-23-47-26.png#pic)
监视信息就是一坨。

## Code Runner

另一个 VSCode 插件，启用后右上角又会多一个标：
![](images/Mac_VSC_DEBUG/2023-04-05-23-49-08.png#pic)

这个是可以跑在内置终端里的：
![](images/Mac_VSC_DEBUG/2023-04-05-23-49-51.png#pic)

## CodeLLDB 👍

这个插件也可以进行 debug，我感觉比 C/C++好用多了。

启用插件后，我们在 launch.json 中可选配置就多了几个，我们使用`CodeLLDB (launch)`模板：
![](images/Mac_VSC_DEBUG/2023-04-05-23-51-28.png#pic)

同样稍微修改：
![](images/Mac_VSC_DEBUG/2023-04-05-23-52-33.png#pic)

回到侧边栏 debug 模块，选择新的启动配置（这里选的是 launch.json 里写好的几个配置）：
![](images/Mac_VSC_DEBUG/2023-04-05-23-53-05.png#pic)

这会在我们启用 debug 的时候去 launch.json 里面找我们指定的配置，然后进行 debug。

!!! warning "有时候 debug 弹出奇怪的报错，是因为当前打开的是配置文件，试图对 launch.json 进行 debug，所以报错了。我们打开要 debug 的源代码文件就好了。"

CodeLLDB 可以使用内置终端：
![](images/Mac_VSC_DEBUG/2023-04-06-00-00-07.png#pic)

可以在监视里直接用变量名监视变量：
![](images/Mac_VSC_DEBUG/2023-04-06-00-00-37.png#pic)

可以在 debug console 中输入命令：
![](images/Mac_VSC_DEBUG/2023-04-06-00-01-06.png#pic)

变量里的字符串支持也好一些：
![](images/Mac_VSC_DEBUG/2023-04-06-00-01-51.png#pic)

[:octicons-link-16:这里](https://github.com/vadimcn/codelldb/blob/master/MANUAL.md)还有官方文档，可以看看。

!!! info "手动创建一个 task.json"
    在菜单 terminal > Configure Tasks 选择 C/C++来生成模板
