---
comments: true
---
# 在Mac上使用VSCode进行C/C++调试

!!! info "环境"
    MacOS: Ventura 13.2.1  
    VSCode: 1.76.2 x64  
    C/C++: 1.14.5  
    CodeLLDB: 1.8.0  
    Code Runner: 0.12.0  

### C/C++

启用后，会在VSCode中添加C/C++的语法高亮、代码提示、代码跳转等功能。
同时右上角出现如下图标：  
![](images/Mac_VSC_DEBUG/2023-04-05-23-25-33.png#pic)

选择run的话，插件就会接着让我们选择使用的编译器
![](images/Mac_VSC_DEBUG/2023-04-05-23-26-52.png#pic)

比如我选择clang++，那么插件就会在当前工作区下自动生成相应的配置文件，并开始运行，很遗憾的是，此时是运行在Debug Console中的，而不是我们想要的终端中，运行在debug console中是没有stdin让我们输入的。

用C/C++进行debug的话，也是会类似的自行生成配置文件。进行debug，但是也是运行在debug console中的，而非我们想要的终端中。

经过查询，发现Mac上C/C++插件不支持运行在内置终端中，setting里也没有修改选项，只能运行在debug console中，或者外部终端。详见[:octicons-link-16:官网](https://code.visualstudio.com/docs/cpp/launch-json-reference)
![](images/Mac_VSC_DEBUG/2023-04-05-23-32-55.png#pic)

所以我们要在launch.json中配置，让其在外部终端中运行。
当前版本，默认配置文件只会生成task.json,没有launch.json：
![](images/Mac_VSC_DEBUG/2023-04-05-23-34-15.png#pic)

这里的一些参数是可以修改的，比如args，就是运行时的参数，注意到-g参数，这会让编译器生成调试信息，这样才能进行debug。还有cwd参数，这个参数可以不写，但是如果不写的话，就会在当前文件所在的目录下运行，而不是当前工作区的根目录下运行。最后注意一下label，我们可以通过这个label来引用这个task。

我们新建一个配置文件launch.json：选择侧栏的debug图标，点击`create a launch.json file`:
![](images/Mac_VSC_DEBUG/2023-04-05-23-38-02.png#pic)

刚开始是空的，什么都没有。点击右下角的`Add Configuration`，就有一些选项，这里有插件为我们准备的默认模版，我们选择`C/C++ lldb（启动）`，意思是C/C++提供的，启动一个新的可执行文件并对其debug，附加是附加到一个已经在执行的进程上的:
![](images/Mac_VSC_DEBUG/2023-04-05-23-39-19.png#pic)

默认的模板长这个样子：
![](images/Mac_VSC_DEBUG/2023-04-05-23-40-26.png#pic)

这并不能直接使用，首先修改program为`"program": "${workspaceFolder}/${fileBasenameNoExtension}",`，这样他运行的就会是当前目录下的当前文件（一般就是光标悬停的那个文件）同名的可执行文件（意思就是没后缀），如果我们编译出来的可执行文件叫做`a.out`，这个配置就不适用，请改为`/a.out`。新加一列`preLaunchTask`，值就是之前task.json上的label，这样就会在运行前可执行文件前先运行tasak编译当前文件（这样比较方便，自动把最新的源代码编译，如果手动的话，记得加上-g）。最后，我们要把`"externalConsole": false,`改为`"externalConsole": true,`，这样就会在外部终端中运行了。
![](images/Mac_VSC_DEBUG/2023-04-05-23-45-03.png#pic)

笔者到这一步就可以在外部终端debug啦，也可以在watch窗口执行命令来监视变量，如全局变量一类的，但是C/C++对一些类型的变量的监视支持不是很好，比如说string：
![](images/Mac_VSC_DEBUG/2023-04-05-23-47-26.png#pic)

### Code Runner

启用后右上角又回多一个标：
![](images/Mac_VSC_DEBUG/2023-04-05-23-49-08.png#pic)

这个是可以跑在内置终端里的：
![](images/Mac_VSC_DEBUG/2023-04-05-23-49-51.png#pic)

### CodeLLDB

这个也可以进行debug，比C/C++还是好用多了。

启用后，我们在launch.json中可选配置就多了几个，我们使用`CodeLLDB (launch)`模板：
![](images/Mac_VSC_DEBUG/2023-04-05-23-51-28.png#pic)

同样稍微修改：
![](images/Mac_VSC_DEBUG/2023-04-05-23-52-33.png#pic)

回到侧边栏debug模块，选择新的启动配置：
![](images/Mac_VSC_DEBUG/2023-04-05-23-53-05.png#pic)

这会在我们启用debug的时候去launch.json里面找我们指定的配置，然后进行debug。

!!! warning "有时候debug弹出奇怪的报错，是因为当前打开的是配置文件，以为要对launch.json进行debug，所以报错了。我们打开要debug的文件就好了。"

CodeLLDB 可以使用内置终端：
![](images/Mac_VSC_DEBUG/2023-04-06-00-00-07.png#pic)

可以在监视里直接用变量名监视变量：
![](images/Mac_VSC_DEBUG/2023-04-06-00-00-37.png#pic)

可以在debug console中输入命令：
![](images/Mac_VSC_DEBUG/2023-04-06-00-01-06.png#pic)

变量里的字符串支持也好一些：
![](images/Mac_VSC_DEBUG/2023-04-06-00-01-51.png#pic)

[:octicons-link-16:这里](https://github.com/vadimcn/codelldb/blob/master/MANUAL.md)还有官方文档，可以看看。

!!! info "手动创建一个task.json"
    在菜单 terminal > Configure Tasks 选择C/C++来生成模板
