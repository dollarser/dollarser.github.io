---
title: hexo避坑小结
date: 2019-10-14 01:41:45
tags:
 - 随笔
 - 踩坑记录
 - 入门实践
---

## 简单记录一下搭建过程
+ 启动（可能需要安装python）
   + `hexo init / hexo init <dir>` 此为hexo初始化，后加目录名则创建文件夹，将博客搭建环境部署在此文件夹下；否则将环境部署在当前文件夹下，故如果初始化不加文件夹，请手动创建一个文件夹后，在该文件夹下执行此命令。
+ 远程部署
   + 安装hexo-deployer-git，此为将hexo部署到github的插件，安装时若报错，提示缺eslint，则直接安装eslint即可，'npm install  hexo-deployer-git --save',另外可能是hexo-deployer-git没有创建软链接，手动创建即可：'sudo ln -s /usr/local/<nodejs安装目录>/lib/node_modules/hexo-deployer-git /usr/bin/hexo-deployer-git'.
+ 标签
   + 注意hexo配置文件中每个':'后都有一个空格' '，不要忘记，其次标签'tags:'多标签不可在用','隔开的形式，而是分行来写，各行之前均有一个' - '。例如

```
tags:
 - 随笔
 - 踩坑记录
```
+ 目录分析
   + source 下是资源文件，其中的文件会直接上传到服务器根目录,创建如两个文件移动到该文件夹。
   + 创建文件 CNAME （全部大写）此为域名解析文件，如果不想绑定自己的域名那就不要创建，文件内容填写自己的域名，例如：'blog.ahulearn.com'。
   + 创建 README.md，移动到source文件夹下,同时在根目录配置文件_config.yml下添加内容skip_render: "README.md"。
   + 主题目录下同有source和source-src也会上传到根目录，应将和当前使用主题相关的资源比如图片等放入此文件夹。
