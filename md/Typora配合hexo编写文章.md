---
title: Typora配合hexo编写文章
date: 2020-03-13 12:00:00
tags:
 - 入门实践
 - 配置相关
typora-root-url: ..
typora-copy-images-to: ..\img
---
### 图像插入设置

* 主要涉及Typora的两个参数设置
  * 图片根目录设置
    * 既告诉Typora哪个文件夹作为网站的根目录
  * 图片复制路径
    * 既图片插入时，自动复制图片到指定路径，如此上传至空间，才能生成正确的url

+ 设置图像根目录
  
  + 以hexo根目录下的source文件夹为例
  + 该文件夹中的内容会上传至web根目录，因此此文件相当于网站的根目录
  + 而文章所在目录为source文件夹下的_post文件夹, 根目录在文章的上级目录
  + 因此设置图片根目录为`..`
  + 既在标题栏添加此内容：`typora-root-url: ..`
  + ![typera_setting2](/img/typera_setting2.JPG)
  
  + 设置图片目录
  
    + 设置source文件夹下的img文件夹，为图片所在文件夹
    + 因为img在source文件夹下，既在文章的上级目录下的img文件夹下
    + 因此设置图片目录为`..\img`
  
    * 既在标题连添加此内容：`typora-copy-images-to: ..\img`
  
* 注意事项：**以上设置只能采用相对路径**

<!--more-->

  + Typora换行Enter键自动添加一个空行，Shift+Enter普通换行。

### hexo 设置

* 无需进行设置

  * 说明一下hexo的目录结构
  * hexo根目录下需要关注的有以下几个文件：
    * source/
      * 资源文件夹，用来存储生成页面的资源文件，图片文章等
    * themes/
      * 主题文件夹，也就是网站皮肤，每个主题也有一个source/文件夹，作用同根目录的source/文件夹
    * public/
      * 根据source/文件夹生成的最终会上传至服务器的文件
    * _config.yml
      * hexo配置文件
  
  