---
title: python-gRPC实战
date: 2024-05-20 20:00:00
tags:
 - Python
 - 深度学习
typora-root-url: ../..
typora-copy-images-to: ../../img/python
---



# python-gRPC实战



## 前言

**RPC**：远程过程调用（Remote Procedure Call）的缩写，即在不同设备进行远程方法调用，隐藏了底层网络技术。随着微服务的兴起而兴起。

**gRPC**：谷歌开源的一套RPC框架，基于http2.0，采用protocol buffer的语法(检查proto)，通过proto语法可以定义好要调用的方法、和参数以及响应格式，可以很方便地完成远程方法调用，而且非常利于扩展和更新参数。

![grpc框架](/img/python/grpc_struct.jpg)

<!--more-->

## 环境配置

```shell
conda create -n test python=3.8
conda activate test
pip install grpcio -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install grpcio-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
```



## 编译配置

```shell
# 编译 proto 文件
python -m grpc_tools.protoc --python_out=.  --grpc_python_out=.  -I. test.proto

python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
--python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
--grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
-I. test.proto : proto 文件的路径, 这里的 proto 文件在当前目录
```

