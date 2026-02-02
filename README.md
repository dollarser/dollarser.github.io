个人静态博客他托管仓库
=========

[TOC]

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dollarser/dollarser.github.io/main.yml?branch=master)



## Git全局递归忽略.DS_Store

### 1. 删除项目中已经提交到仓库的.DS_Store文件夹

搜索一下项目内所有的.DS_Store，全部rm掉，然后再push一把

```
find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch
```

删除当前目录下的所有的.DS_Store:

```
find . -name '*.DS_Store' -type f -delete
```

### 2.对于今后的项目，做全局的配置

1.创建全局配置文件，逐一执行以下代码，cat一下看是否正常写入

```
echo ".DS_Store" >> ~/.gitignore_global

echo "._.DS_Store" >> ~/.gitignore_global

echo "**/.DS_Store" >> ~/.gitignore_global

echo "**/._.DS_Store" >> ~/.gitignore_global
```

2.设置一下全局的配置

```
git config --global core.excludesfile ~/.gitignore_global
```

### 也可以创建`.gitignore`文件

只在本项目中忽略
```
.DS_Store
._.DS_Store
**/.DS_Store
**/._.DS_Store
```
