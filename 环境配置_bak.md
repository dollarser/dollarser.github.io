### 2. 安装Hexo
- 安装Hexo
```bash
cnpm install -g hexo-cli
cnpm install hexo
```

### 3. 安装主题
推荐主题: butterfly
- 主题：https://github.com/jerryc127/hexo-theme-butterfly
- 官网：https://butterfly.js.org/posts/21cfbf15/
- 下载:
```bash
git clone -b master https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly
```
- 主题其他依赖
```bash
# --save命令将包依赖保存到当前目录的package.json中
cnpm install hexo-renderer-pug hexo-renderer-stylus --save

cnpm install hexo-deployer-git hexo-generator-archive hexo-generator-category hexo-generator-index hexo-generator-tag hexo-renderer-ejs --save
cnpm install @renbaoshuo/markdown-it-katex

cnpm install hexo-renderer-pandoc hexo-server hexo-filter-mathjax --save
cnpm install hexo-util moment-timezone --save
```

### 4.公式支持

使用 Mathjax 前, 需要先卸載 hexo 的 Markdown 渲染器，然后安裝hexo-renderer-kramed

1. 安装插件
```bash
# 安装 --save的作用是将插件保存在依赖配置项中
cnpm install hexo-renderer-markdown-it --save   # 主题推荐的渲染器
npm install hexo-renderer-kramed --save  # 主题推荐的渲染器
npm install hexo-filter-mathjax --save  # 公式过滤
npm install hexo-renderer-pandoc --save  # 渲染公式
cnpm install hexo-deployer-git --save  # 部署网站用

# 如果要卸载
cnpm un hexo-renderer-marked --save  # 默认渲染器
cnpm un hexo-renderer-kramed --save
cnpm un hexo-renderer-pandoc --save
cnpm install hexo-renderer-ejs hexo-renderer-pug  --save
```

### 5. 配置

- 配置 hexo 根目录的配置文件
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
