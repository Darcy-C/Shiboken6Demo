# 文档里的 shiboken6-genpyi 工具, 直接跑跑不通, 调试了一下写了下面的代码跑通了.
# 下面的代码就是基于直接调用 shiboken6-genpyi Universe.so 跑不通以后修改了2处地
# 方

import logging
import argparse

import PySide6

# --- (无语) 导入 shiboken6 以后才有 shibokensupport, 下面的 shibokensupport 是
#     内嵌的模块, 这么难调, 搞得补全都没有
import shiboken6  # type: ignore
import shiboken6_generator
from PySide6.QtCore import qVersion
from shibokensupport.signature.lib.pyi_generator import *  # type: ignore

# 打印几个版本, 这几个版本在要一样 不然可能有问题 (PySide6的版本在生成非PySide6
# 的绑定时无关紧要, 但是也顺便打印出来看看)
print(f"PySide6.QtCore.{qVersion()=}")
print(f"{shiboken6.__version__=}")
print(f"{shiboken6_generator.__version__=}")


# --- (改动 1) pyi生成器内部会访问这个全局变量, 但是不知道为什么这个变量在我的环
#     境里没被定义, 也不太清楚哪里定义的, 这里直接设置一个后面就没问题了, Sample
#     Binding 这个案例本身也没有用 PySide, 没有副作用. 这个东西要自己定义一下,
#     这里就是代表自己实则没用到PySide6的模块
PySide6.__all__ = []

# --- (无语) shiboken6 内部的 options 参数是直接用 argparse, 下面的一些内部数据
#     字段也是直接暴力设置到对象上. 这里本来是用命令行触发的, 因为它底层业务逻辑
#     直接访问的这个数据结构, 我们这里虽然没用命令行, 但也还是创建一个
parser = argparse.ArgumentParser()
options = parser.parse_args()


# --- (无语) (改动 2) pyi生成器这个字段内部写死 False 的, 导致后面有的一些逻辑走
#     不下去, 这里模仿 PySide6 用的生成 pyi 的代码改成 True, 后续逻辑就跑通了
options._pyside_call = True

# --- 这几个字段内部逻辑会用, 给他设置上
options.quiet = False
options.logger = logging.getLogger()

generate_pyi(  # type: ignore
    # 要处理的模块. 实验发现这里发现如果开了 _pyside_call 以后不用加 .so
    "Universe",
    # 保存 pyi 到当前目录
    ".",
    options=options,
)
print("ok.")

# --- 其他阅读注明:
# Win 下的 Py C 扩展的后缀是 .pyd
# macOS 下的 Py C扩展的后缀是 .so

# --- 其他备注

# 运行时 屎啵啃版本和PySide6版本不一样 可能 会导致PySide6无法加载; shiboken6 和
# shiboken6_generator 版本不一样的话可能能正常生成 但是无法实际import导入

# 用户端使用的这个库的时候, 理论上没有这个限制, 只要是PySide6都可以用基于Qt6的导出.

# -- 关于打包问题的其他想法

# 如果开发阶段这些都可以跑通, 如果这个扩展要自己本机用然后本机打包, 一般没有什么
# 额外的问题, 因为打包器(如pyinstaller)会自己修复这些 动态链接库 的 rpath 依赖
# (*NIX平台), 如果是自己要做成一个wheel发布让别的项目用这个组件的话, 要自己想办
# 法修复一下, 比如把形似 libshiboken6.abi3.XXX.dylib 一起打包进 wheel, 然后加一
# 下 rpath 之类的, 否则不做处理的话其他用户因为环境不一样, 还是无法使用你的扩展
