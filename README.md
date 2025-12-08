个人静态博客他托管仓库
=========

[TOC]

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dollarser/dollarser.github.io/main.yml?branch=master)

## 环境配置

### 1. 安装Node.js
- 网：[下载 | Node.js 中文网](https://nodejs.cn/download/)
- 文档：https://hexo.io/zh-cn/docs/
- 更改国内源:
```bash
npm config set registry https://registry.npmmirror.com
```
- 安装cnpm
```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
```
> 说明:
> -g参数: 用于全局安装, 可以在任何地方使用该命令, 不添加-g参数则安装在当前目录下, 且无法使用命令行访问
> -registry参数: 指定npm的源

### 2. 安装Hexo
- 安装Hexo
```bash
cnpm install -g hexo-cli
```

### 3. 安装主题
推荐主题: butterfly
- 主题：https://github.com/jerryc127/hexo-theme-butterfly
- 官网：https://butterfly.js.org/posts/21cfbf15/
- 下载主题:
```bash
git clone -b master https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly
```
- 主题其他依赖
```bash
cnpm install hexo-renderer-pug hexo-renderer-stylus --save
```
### 4.公式支持
使用 Mathjax 前，你需要卸載 hexo 的 markdown 渲染器，然後安裝hexo-renderer-kramed

1. 安装插件
```bash
# 安装 --save的作用是将插件保存在依赖配置项中
npm install hexo-renderer-marked --save # 默认渲染器
npm install hexo-renderer-kramed --save  # 主题推荐的渲染器
npm install hexo-filter-mathjax --save  # 公式过滤
npm install hexo-renderer-pandoc --save  # 渲染公式
npm install hexo-deployer-git --save  # 部署网站用

# 卸载
npm un hexo-renderer-marked --save
npm un hexo-renderer-kramed --save
npm un hexo-renderer-pandoc --save
npm install hexo-renderer-ejs hexo-renderer-pug  --save
```
### 5. 配置
配置 hexo 根目錄的配置文件
```yaml
pandoc:
  extensions:
    - '-mathjax'           # 数学公式支持
    - '-smart'             # 智能标点
    - '-footnotes'         # 脚注支持
    - '-implicit_figures'  # 隐式图片
    - '-table-of-contents' # 目录
    - '-raw_tex'           # 原始 TeX 支持
    - '-markdown-in-html_blocks'
    - '-fenced_code_attributes'  # 代码块属性
    - '-fenced_code_blocks'      # 围栏代码块
  templates: []
```

```yaml
kramed:
  gfm: true
  pedantic: false
  sanitize: false
  tables: true
  breaks: true
  smartLists: true
  smartypants: true
```

### 最终所有的包：
```
npm ls --depth 0
hexo-site@0.0.0 D:\OneDrive\blog
├── hexo-filter-mathjax@0.9.1
├── hexo-generator-archive@2.0.0
├── hexo-generator-category@2.0.0
├── hexo-generator-index@3.0.0
├── hexo-generator-tag@2.0.0
├── hexo-renderer-ejs@2.0.0
├── hexo-renderer-pandoc@0.5.0
├── hexo-renderer-pug@3.0.0
├── hexo-renderer-stylus@3.0.1
├── hexo-server@3.0.0
└── hexo@7.3.0
```
### hexo常用命令
- 初始化Hexo
```bash
hexo init
```
- 安装依赖
```bash
cnpm install
```
- 生成静态文件
```bash
hexo generate
```
- 清除缓存
```bash
hexo clean
```
- 启动Hexo
```bash
hexo server
```
- 部署到GitHub Pages
```bash
hexo deploy
```

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
