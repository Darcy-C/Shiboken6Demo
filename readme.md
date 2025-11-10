# Shiboken6 学习日记

注: shiboken6 是 Qt 提供的一个 C++ 到 Python 的通用绑定工具 (和 pybind11 是同类), Qt 用它来创建他们自己的 PySide6 绑定

本仓库写的比较详细, 方便之后有需要的人查看学习

## 目标

这里简单写一下一些基本要求

- 在 Python 里使用 Qt C++ 我们自己写的 QWidget 组件
- 体验需和正常的 Python 类一样, 有补全, 能过类型检查
- 能和 PySide6 结合在一起, 例如我们写的一个 Widget 类, 实例化以后能直接被 addWidget 到布局里

## 缘起

有的时候, 我们想在 Python 里使用**我们自己写的 C++ Qt**的组件, 和 PySide6 一起无缝使用, Qt官方社区提供了不少的 shiboken6 的文档和一些案例, 但是实操的时候, 有一些坑, 这里简单记录一下, 供后人和AI参考 (截止到目前, AI 目前喜欢编 shiboken6 的实测没有的 API)


## 仓库学习方式

仓库里有2个文件夹, 是直接从 Qt examples 里下载下来的 (shiboken的文档里直接可以下), 基本没有删减, 删减和修改处有写注释, 方便知道这里可能有个坑, 避免这些坑以后都可以跑起来

看的顺序是 samplebinding, 然后是 widgetbinding, 分别是不带 Qt 的绑定 和 带 Qt 的绑定

官方 shiboken 文档里写的流程是可以跟着走的, 请看着文档来尝试编译, 就像上面说的这里不会赘述编译流程

2个案例里官方自带的注释都没有修改, 案例里的代码也没有修改, 大家可以放心使用

## 前置知识和准备

1. CMake

    之前没构建过 CMake 项目的话建议放弃

2. ninja

    官方案例用的 ninja, 提前装好配在 PATH 等会会用, 之后不用 ninja 也可以

    Windows 用户不用单独安装, VS 里已经自带

    macOS 用户自行安装一下, 例如可以用例如 `brew` 这样的包管理器装
    > brew install ninja

3. C++ Qt SDK

    装好以后配到 PATH, 最好和 Python 里装的版本是一样的, 差几个版本没有关系, 原则上都只要是 Qt 6 就可以了


4. Visual Studio / Xcode

    - Windows 环境装 Visual Studio
    - macOS 环境装 Xcode

    这 2 个是 IDE, 但是会顺便下载系统的 SDK 和其他组件

    ---
    
     Windows 用户注意, 装 Community 版本的 VS 也可以
     
     然后要自己在安装时选 C++ 桌面开发 的SDK, 至少选上下面的组件 
     
     - MSVC (微软平台默认使用的编译器)
     - Windows 10/11 SDK

    组件的版本的话, 在今天的案例中, 原则上是无所谓的

    之前装过 VS 的找不到下载器的, 开始菜单搜 Visual Studio Installer 打开然后在右侧勾组件安装

    ---

    macOS 用户只要安装了 Xcode 就默认附带下列组件, 无需其他处理:
    
    - Apple clang (目前苹果平台默认使用的编译器, 装完 Xcode 以后默认就在 /usr/bin)
    - macOS SDK


## 常见坑记录

### shiboken6-generator 和 shiboken6 的版本不同导致的问题

不同版本可能会导致生成的时候用了一个较新的 shiboken API, 然后在使用的时候 (shiboken6) 没有找到的问题, 导致可以编译出, 但是实际不能import导入

可以自行用下面的命令检查一下版本
    
macOS 类 bash 用
> pip list | grep shibo

Windows PowerShell 用
> pip list | Select-String shibo

然后 shiboken6-generator 这个库现在已经可以在 pypi 直接下了, 可以不指定 Qt 的仓库, 如果你要下指定版本的话, 记得 shiboken6-generator 和 shiboken6 一起重新装, 不要只装一个, 如果你要生成的绑定如果和 Qt 有关, 也就是我们最终的目标, 在 PySide6 里能用的组件, 那么你 shiboken6 的版本和 PySide6 的版本也要一样

注明: C++ Qt 的版本可以不一样, 只要你没用到新版本的API

例如, C++ Qt 的预编译库可能你之前下的是 6.8, 然后你实际上你的 PySide6 是 6.6, 这个是没有关系的, 只要你写的 C++ 代码里没用 6.7 6.8 的新 API 就可以了

### 看错官网文档的版本教程导致的问题

近阶段 Qt 6.10 已经出来了, shiboken 的文档也默认是 6.10 的版本, 6.10 的案例里的代码里用的 API 和之前的版本是不一样的, 如果你没有意识到这一点, 可能你本机还在可能 ... 6.6 6.7 6.8 6.9 然后你找来找去也不知道那个 CMake 宏到底定义在哪里, 它定义在 Qt 6.10 的 shiboken 工具链里

由于我目前的项目还没有用新的 Qt 6.10, 我认为还需要一段时间才会到 6.10, 所以本文没有用 6.10 的新方法, 大家在看的时候, 在 Shiboken 的文档网页左侧, 改成看 6.9 及以下的版本, 例如 6.8

### (macOS) 用错编译器导致的问题

如果你当前的开发环境下的 clang 版本太高, 例如你从 brew 自己装了一个比较新的 llvm, 然后配套 PATH 里了, shiboken6-generator 可能无法运作, 可以暂时切到老一点的版本 (例如暂时去掉 brew 里下载版本的自己配置的 PATH 或者直接临时前置追加回 /usr/bin 就可以用 Xcode 自带的 clang了)

### 没有修改官网案例里 CMakeLists.txt 的一些配置导致的问题

如果你直接从网页上点 download 下载下来的案例, 有一个叫做 `pyside_config.py` 的辅助文件是不会下载下来的, 这里单独从仓库下载放到本仓库了, 具体见 CMakeLists.txt 文件内注释解释

### 纯坑 - 无法使用 shiboken6-genpyi 的问题

我们可能编译都通过了, 也能正常在 python 里用了, 但是就是用不了 shiboken6-genpyi 生成类型文件, 这一个板块官方文档是一笔带过, 这里我们可以自己去源代码里看一下官方是怎么在 PySide6 里用这个工具的, 我这里提取精髓部分写在了 `gen_pyi.py` 这个文件里, 2个案例的输出流程稍有不同

这里说一下看这个工具源代码的方法, 可以根据自己的 shiboken 版本, 到 pyside/pyside-setup 仓库选好版本 然后下载源码看一下, 它这个工具是内嵌的, 看代码要在 github 里根据报错的行去看对应版本的代码

这个生成工具应该根本没人用过, 去 QTBUG 平台看跟踪的问题, 有一些反馈, 但是基本上的回复是: 你自己看看吧, 能用就行

很难调, **基本上这个工具只包 PySide6 的成功生成**, 本仓库学习日志提供了在不修改 Qt工具链源码 的情况下跑通, 有些组织的项目是给这个工具链打 patch 以后才能用.

---

下面的一些问题不仅限于本仓库案例, 但是这里也写一些, 帮助后来人检查问题

### (Windows) 没有编译环境导致的问题

请在 `x64 Native Tools Command Prompt for VS 2022` 中执行你的编译命令, 这个就是所谓的 Visual Studio Developer Command Prompt 了

### Qt 预编译库的编译器版本不一致的问题

在下载 Qt 预编译库的时候, 可能会让你选是 MSVC 的版本还是 mingw 的版本, 官方文档里是假设 Windows 用户用了 MSVC 版本的, 请你确保你的 Qt 是基于 MSVC 编译的版本.


## 其他后续问题

这个仓库还有一些问题没有写出, 例如关于后续打成 wheel 让其他用户使用的问题, 例如 *NIX 系统需要处理 rpath 等问题, 后面有机会再写