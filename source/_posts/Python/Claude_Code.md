---
title: Claude Code应用指南
date: 2026-02-12 17:30:00
tags:
 - Python
 - AI工具
typora-root-url: ../..
typora-copy-images-to: ../../img/python
---



> 参考视频：https://www.bilibili.com/video/BV1zqeMzfEiQ

## 环境配置

#### **npm 安装（需要 Node.js 18+）**

```bash
npm install -g @anthropic-ai/claude-code
```

### 3. 验证安装

```bash
claude --version
```

### 4. 配置 API Key

**Windows (CMD)**：

```cmd
set ANTHROPIC_API_KEY=sk-xxxx-xxxxxx
```

**macOS/Linux (Bash/Zsh)**：

```bash
echo "export ANTHROPIC_API_KEY='sk-xxxx-xxxxxx'" >> ~/.bashrc
source ~/.bashrc
```

------

## 二、替换/切换模型

Claude Code 支持三种模型，你可以根据任务需求随时切换 ：

| 模型           | 特点                         | 适用场景                       | 价格                |
| :------------- | :--------------------------- | :----------------------------- | :------------------ |
| **Opus 4.6**   | 最强推理能力，支持 1M 上下文 | 复杂架构、深度调试、多步骤推理 | $5/$25 每百万 token |
| **Sonnet 4.5** | 平衡速度与质量（默认）       | 日常开发、大多数编码任务       | $3/$15 每百万 token |
| **Haiku 4.5**  | 最快响应，成本最低           | 简单查询、批量操作、快速查找   | $1/$5 每百万 token  |

### 切换模型的 4 种方法

#### **方法 1：会话中切换（最常用）**

在 Claude Code 交互界面中输入：

```plain
/model opus      # 切换到 Opus（最强模型）
/model sonnet    # 切换到 Sonnet（默认平衡）
/model haiku     # 切换到 Haiku（最快最便宜）
```

或使用简写：

```plain
/mode opus
/mode sonnet  
/mode haiku
```

#### **方法 2：启动时指定**

```bash
claude --model opus
claude --model sonnet
claude --model haiku
```

#### **方法 3：设置默认模型（永久生效）**

添加到 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）：



```bash
export ANTHROPIC_MODEL=claude-opus-4-6
```

或使用具体版本号：



```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-5-20250929"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-5-20251001"
```



## 三、国内用户使用建议

如果需要使用国内模型作为替代，可以通过修改 API Base URL 和模型映射来实现 

```bash
export ANTHROPIC_BASE_URL=https://your-proxy-url.com
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.7"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
```
