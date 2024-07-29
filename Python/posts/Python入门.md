---
title: Python入门
date: 2021-08-5 18:00:00
tags:
 - CS
 - python

typora-root-url: ..
typora-copy-images-to: ..\img\python

---



# 1、环境配置

python作为脚本语言，只需要一个python解释器就可以直接编写代码和运行。
但是为了方便我们通常会使用IDE(集成开发环境)或轻量级的文本编辑器进行开发。
这里首先介绍使用最简单的python编辑器编写代码，以及使用VS Code、Jupyter开发。

## 1.1 安装python解释器

这里推荐安装Conda,Conda是极其方便且强大的包管理器，安装后自带python解释器，同时为以后开发带来极大的便利。如果只想安装python解释器可以从下方地址下载：
官网Windows下载：https://www.python.org/downloads/windows/

## 1.2、安装Conda

conda分为anaconda和miniconda。anaconda是包含一些常用包的版本，miniconda则是精简版，需要什么装什么，这里介绍miniconda的安装。
官网地址：https://docs.conda.io/en/latest/miniconda.html

### 1.2.1、安装

进入官网：https://docs.conda.io/en/latest/miniconda.html

+ Windows installers一栏就是Windows安装包
+ Linux installers一栏就是Linux安装包

选择对应的操作系统和conda版本即可。
一般安装MiniConda3，python版本无所谓，3.x以上都可以，后面可以根据需要自行更改。

安装完成后，检测是否正常：conda info -e

### 1.2.2、配置

执行如下命令，配置Miniconda

### 1.2.3、常用命令参数

``` bash
查看虚拟环境： conda info -e
激活虚拟环境：conda activate <env_name>
	activate 后是虚拟环境名
退出虚拟环境： conda deactivate
删除虚拟环境：conda remove -n <env_name> --all
安装某个软件到当前虚拟环境：conda install 包名 -y
卸载当前虚拟环境中的某个软件包：conda uninstall 包名 -y
安装某个软件包到指定虚拟环境中：conda install -n 虚拟环境名 包名 -y
卸载指定虚拟环境中的某个软件包：conda uninstall -n 虚拟环境名 包名 -y
```

# 2、牛刀小试

打开cmd命令行，输入`python`

![image-20210805160322930](/img/python/image-20210805160322930.png)



如果你是Windows10,可能会跳转到Win10应用商店，因为Win10中有一个python下载程序。
可以通过 `where python`查看python程序

![image-20210805160005211](/img/python/image-20210805160005211.png)

下方这个`C:\sun_app\Anaconda\python.exe`才是我们安装的python解释器，
如果想运行这个程序，cmd命令行中输入`C:\sun_app\Anaconda\python.exe`即可，`.exe`后缀可以省略。

![image-20210805160533737](/img/python/image-20210805160533737.png)

此时进入python命令行中，可以输入简单的python语句执行：


```python
print("Hello World")
```

    Hello World



```python
a = 1
b = 2
print(a+b)
```

    3


在命令行中，只能执行一些简单命令。如果代码很长，可以将代码写入一个 `.py`后缀的文件中。通过 `python xxx.py` 执行。

![image-20210805165404778](/img/python/image-20210805165404778.png)



![image-20210805163940858](/img/python/image-20210805163940858.png)