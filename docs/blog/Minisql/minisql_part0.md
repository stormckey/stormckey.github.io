---
comments: true
---

# Minisql Environment Configurations

!!! abstract
    虽然已经搭出能用的环境了，但还是很难不在开头放上三个流汗黄豆来表达我对搭环境这件事的无语😅😅😅

## 初试：本地运行

本人目前使用的的 MacBookPro，MacOS Ventura13.3.1. 直说的话，本地运行的尝试失败了😅

### Cmake
第一个坑是 cmake 阶段 有如下的经典报错（经典是因为我见过他无数次了）：
```bash
cmake ..                                                                                                                                                                                       ─╯
CMake Error at /Users/xxx/opt/anaconda3/lib/cmake/GTest/GTestTargets.cmake:37 (message):
  Some (but not all) targets in this export set were already defined.

  Targets Defined: GTest::gtest;GTest::gtest_main

  Targets not yet defined: GTest::gmock;GTest::gmock_main

Call Stack (most recent call first):
  /Users/xxx/opt/anaconda3/lib/cmake/GTest/GTestConfig.cmake:32 (include)
  thirdparty/glog/CMakeLists.txt:71 (find_package)
```

我不懂 cmake，也搜不到这个问题，感觉可能跟版本兼容啥的有关（有知道的大佬可以直接在评论区里说说，感谢！）不过我看到了报错路径上了 anaconda3，想起来我终端的环境还是 conda base，所以我一个`conda deactivae`后，重建 build 目录，再 cmake 就没有这个问题了。

但这个问题只是被暂时修复了算是，因为我调用 VSCode 的 cmake 插件啥的还是会这样，我也没找出来这里的要怎么解决。

### Make
Cmake 通了 Make 又不通😅
报错如下：
```bash
In file included from /Users/xxx/Desktop/minisql/src/executor/execute_engine.cpp:1:
In file included from /Users/xxx/Desktop/minisql/src/include/executor/execute_engine.h:5:
In file included from /Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/string:551:
In file included from /Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/string_view:222:
In file included from /Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/algorithm:1851:
In file included from /Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/__algorithm/ranges_sample.h:13:
In file included from /Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/__algorithm/sample.h:18:
/Library/Developer/CommandLineTools/SDKs/MacOSX13.3.sdk/usr/include/c++/v1/__random/uniform_int_distribution.h:162:5: error: static_assert failed due to requirement '__libcpp_random_is_valid_inttype<char>::value' "IntType must be a supported integer type"
    static_assert(__libcpp_random_is_valid_inttype<_IntType>::value， "IntType must be a supported integer type");
    ^             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/Users/xxx/Desktop/minisql/test/include/utils/utils.h:24:41: note: in instantiation of template class 'std::uniform_int_distribution<char>' requested here
    std::uniform_int_distribution<char> uniform_dist(33， 122);
```
看起来是框架里实例化模板的时候用的的 char 类型，但是这里不让用 char 类型，那怎么办，要我去改框架吗，这玩意万一耦合的很紧我的理解成本加修改成本估计都够我受的了.这里的两个选择一个是换个 SDK 版本，这个不知道能不能起效，另一个就是跑路，因为我还有一台 Windows 游戏本，所以果断润了。

## 二试：WSL2

我的 Win 本早就装过 WSL2 了，之前跑一些模型的时候把 ssh 啥的也配好了（不过玉湖只能用动态 IP 我三天两头就得换一下😅），所以成本其实不大。
这里遇到两个问题，一是 cmake 阶段跟上面一样的问题，解决方法还是`conda deactivate`，二是提示没有 gflag 模块，这个最简单，直接安装一下就好了
```bash
sudo apt-get install gflags
```

然后就能跑了，虽然在这里用各种 Cmake 插件一类的还是没一个能跑的（报 Cmake 阶段的那个错），我试图用 Clion 远程开发结果后端也崩坏了开不起来，各种事情搞得我很烦，但总算有个能用的 VSCode + ssh + WSL2 的方案能跑了，他的优点是能跑，缺点是能跑的补集，但我实在折腾不动了就先这样了。
