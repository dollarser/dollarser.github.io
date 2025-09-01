Python 作为一门强调“可读性”和“简洁性”的语言，拥有非常完善的**代码规范与最佳实践体系**。遵循主流规范不仅能提升代码质量，还能增强团队协作效率。

以下是目前 Python 主流的**编码规范、风格指南和工程实践**，涵盖语法、命名、结构、文档、测试等多个方面。

---

## ✅ 一、PEP 8：官方代码风格指南（最核心）

> 📚 官方文档：[PEP 8 -- Style Guide for Python Code](https://pep8.org/)

这是 Python 官方推荐的**代码风格标准**，几乎所有 Python 项目都以此为基础。

### 1. 缩进
- 使用 **4 个空格**缩进（不要用 Tab）
- 不要混用空格和 Tab

```python
# ✅ 正确
if x > 0:
    print("positive")

# ❌ 错误
if x > 0:
	print("positive")  # 使用了 Tab
```

### 2. 行宽
- 每行不超过 **79 个字符**（代码），注释/文档字符串不超过 72
- 超长表达式可用括号隐式换行

```python
# ✅
long_list = [
    "item1", "item2", "item3",
    "item4", "item5"
]
```

### 3. 空行
- 顶层函数和类之间：**2 行**
- 类内方法之间：**1 行**
- 逻辑块之间可用空行分隔

### 4. 导入（Imports）
- 每行一个导入
- 顺序：标准库 → 第三方库 → 本地应用
- 用空行分隔三类

```python
import os
import sys

import requests
import numpy as np

from mypackage import mymodule
```

### 5. 命名规范
| 类型             | 规范                          | 示例                                |
| ---------------- | ----------------------------- | ----------------------------------- |
| 变量、函数       | `lower_case_with_underscores` | `user_name`, `calculate_total`      |
| 类               | `CapitalizedWords`（驼峰）    | `UserProfile`, `DatabaseConnection` |
| 常量             | `UPPER_CASE`                  | `MAX_RETRY`, `API_TIMEOUT`          |
| 私有成员         | `_single_leading_underscore`  | `_internal_var`                     |
| 强私有           | `__double_leading_underscore` | `__private_method`（名称改写）      |
| 不要使用的变量名 | `_`（临时变量可用）           | `O`, `l`, `I`（易混淆）             |

---

## ✅ 二、PEP 257：文档字符串规范（Docstring）

> [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)

规定如何编写函数、类、模块的文档字符串。

### 基本格式
```python
def my_function(param: str) -> bool:
    """
    简要描述函数功能。

    更详细的说明可以放在这里。

    参数:
        param (str): 参数说明

    返回:
        bool: 返回值说明

    示例:
        >>> my_function("hello")
        True
    """
    return True
```

### 推荐格式
- 使用 `"""` 三引号
- 首行为一句话摘要
- 空一行后写详细说明
- 参数、返回值、异常要明确标注

> 🔧 工具支持：Sphinx、PyCharm、VS Code 可自动解析 docstring

---

## ✅ 三、类型提示（Type Hints）—— PEP 484 及后续

Python 3.5+ 支持类型注解，极大提升可读性和工具支持。

```python
from typing import List, Dict, Optional

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    if not users:
        return None
    return users[0].get("name")
```

### 主流用法
- 函数参数和返回值加类型
- 使用 `Optional[T]`, `Union`, `Literal`, `Annotated` 等高级类型
- 配合 `mypy` 进行静态类型检查

> ✅ 现代 Python 项目（如 FastAPI、Django 4+）广泛使用类型提示

---

## ✅ 四、代码格式化工具（自动化规范）

手动遵守 PEP 8 很难，推荐使用自动化工具。

### 1. **Black**（“不妥协的代码格式化器”）

- 自动格式化代码，**无需配置**
- 强制统一风格
- 命令：`black .`

### 2. **autopep8**
- 自动修复 PEP 8 问题
- 可配置

### 3. **isort**
- 自动排序和分组导入

### 4. **flake8**
- 检查代码风格 + 简单错误（如未使用变量）

> ✅ 推荐组合：
```bash
pip install black isort flake8 mypy
```

---

## ✅ 五、项目结构规范

现代 Python 项目的典型结构：

```
myproject/
│
├── src/                    # 源码（可选）
│   └── mypackage/
│       ├── __init__.py
│       ├── module.py
│       └── utils.py
│
├── tests/                  # 测试
│   ├── __init__.py
│   └── test_module.py
│
├── pyproject.toml          # 构建配置（推荐）
├── requirements.txt        # 依赖（传统）
├── README.md
├── LICENSE
└── .gitignore
```

### 使用 `pyproject.toml` 替代 `setup.py`
```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
dependencies = [
    "requests",
    "click",
]
```

---

## ✅ 六、依赖管理

| 工具                       | 用途                       |
| -------------------------- | -------------------------- |
| `pip` + `requirements.txt` | 传统方式                   |
| `poetry`                   | 现代依赖与打包管理（推荐） |
| `pipenv`                   | 虚拟环境 + 依赖管理        |
| `conda`                    | 数据科学环境管理           |

> ✅ 推荐：**Poetry** 或 **PDM**（新一代工具）

---

## ✅ 七、测试规范

### 1. 使用 `unittest` 或 `pytest`
- `pytest` 更简洁，功能强大

```python
# tests/test_math.py
def test_add():
    assert 1 + 1 == 2
```

### 2. 测试覆盖率
- 使用 `pytest-cov`
- 目标：> 80% 覆盖率

### 3. 测试目录
- `tests/` 或 `test/`
- 与源码分离

---

## ✅ 八、日志规范

避免使用 `print()`，使用 `logging` 模块：

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("程序启动")
logger.error("出错了")
```

---

## ✅ 九、错误处理

- 使用异常处理而非返回错误码
- 自定义异常类
- 不要裸 `except:`

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"输入无效: {e}")
    raise  # 重新抛出或包装
```

---

## ✅ 十、现代 Python 最佳实践总结

| 方面        | 推荐做法                                  |
| ----------- | ----------------------------------------- |
| Python 版本 | ≥ 3.8（推荐 3.9+）                        |
| 类型提示    | 全局启用 `->` 和 `: str` 等               |
| 格式化      | 使用 `black` + `isort`                    |
| 静态检查    | `mypy` + `flake8`                         |
| 依赖管理    | `poetry` 或 `pdm`                         |
| 构建配置    | `pyproject.toml`                          |
| 文档        | `Google Style` 或 `NumPy Style` docstring |
| 测试        | `pytest` + `coverage`                     |
| 日志        | `logging` 模块                            |
| 虚拟环境    | `venv` 或 `poetry shell`                  |

---

## ✅ 十一、常用工具链推荐

```bash
# 安装
pip install black isort flake8 mypy pytest pytest-cov requests

# 格式化
black .
isort .

# 检查
flake8 src/
mypy src/

# 测试
pytest --cov=src
```

配合 `pre-commit` 钩子自动检查：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks: [- id: black]
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks: [- id: flake8]
```

---

## 📌 总结：Python 主流规范一句话

> **“遵循 PEP 8，使用类型提示，用 Black 格式化，Pytest 测试，Poetry 管理依赖，pyproject.toml 配置，logging 写日志。”**

---

📌 **推荐学习资源**：
- [PEP 8](https://pep8.org/)
- [The Hitchhiker’s Guide to Python](https://docs.python-guide.org/)
- [Effective Python](https://effectivepython.com/)（书籍）
- [Real Python](https://realpython.com/)（网站）

遵循这些规范，你的 Python 代码将更专业、更易维护、更适合团队协作！