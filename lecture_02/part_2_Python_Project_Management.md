# Python 项目管理

> [!info]
>
> 本文档介绍 Python 项目管理的核心概念、工具和最佳实践，帮助构建可维护、可协作、高质量的项目。

## 目录

1. [为什么需要项目管理](#1-为什么需要项目管理)
2. [项目管理的核心要素](#2-项目管理的核心要素)
3. [项目管理的最佳实践](#3-项目管理的最佳实践)
4. [工具与资源](#4-工具与资源)

---

## 1. 为什么需要项目管理

### 1.1 协作需要

**问题场景：**
- 多人同时修改同一项目时，如何避免代码冲突？
- 如何确保团队成员使用相同的代码风格和工具版本？
- 如何让新成员快速理解项目结构并上手？

**解决方案：**
- **版本控制**：使用 Git 管理代码变更历史
- **依赖管理**：使用 `pyproject.toml` 或 `requirements.txt` 锁定依赖版本
- **代码规范**：统一代码风格（如 Black、Ruff），使用 pre-commit hooks 自动检查

**实际影响：**
- 减少合并冲突，提高协作效率
- 避免"在我机器上能跑"的问题
- 降低新成员的学习成本

### 1.2 标准化

**问题场景：**
- 不同项目使用不同的项目结构，难以快速定位代码
- 缺少统一的配置管理方式
- 代码风格因人而异，难以维护

**解决方案：**
- **项目结构标准化**：遵循 Python 项目最佳实践（如 src-layout）
- **配置文件标准化**：使用 `pyproject.toml` 统一管理项目元数据、依赖、工具配置
- **代码风格标准化**：使用统一的格式化工具和 lint 规则

**实际影响：**
- 提高代码可读性和可维护性
- 降低项目间的切换成本
- 便于自动化工具集成

### 1.3 避免新改动引起问题

**问题场景：**
- 修改代码后，如何确保没有破坏现有功能？
- 如何快速发现回归问题？
- 如何安全地重构代码？

**解决方案：**
- **自动化测试**：编写单元测试、集成测试，确保代码变更不会破坏现有功能
- **持续集成（CI）**：每次提交自动运行测试，及时发现问题
- **类型检查**：使用类型提示（Type Hints）和 mypy 提前发现潜在错误

**实际影响：**
- 提高代码质量和稳定性
- 减少生产环境中的 bug
- 增强重构的信心

### 1.4 用户友好

**问题场景：**
- 用户如何安装和使用你的项目？
- 如何让用户快速了解项目功能？
- 如何提供清晰的错误信息和使用示例？

**解决方案：**
- **清晰的文档**：README、API 文档、使用教程
- **简单的安装流程**：使用 `pip install` 或 `uv` 一键安装
- **友好的错误提示**：提供有意义的错误信息和解决建议

**实际影响：**
- 提高项目的可用性和采用率
- 减少用户支持成本
- 建立项目声誉

### 1.5 对贡献者友好

**问题场景：**
- 如何让外部贡献者快速理解项目结构？
- 如何引导贡献者遵循项目规范？
- 如何简化贡献流程？

**解决方案：**
- **贡献指南**：CONTRIBUTING.md 说明如何提交代码、报告问题
- **开发环境设置**：提供清晰的开发环境配置说明
- **代码审查流程**：使用 Pull Request 流程，提供反馈和改进建议

**实际影响：**
- 吸引更多贡献者
- 提高代码质量
- 建立活跃的社区

### 1.6 权限与职责的分级

**问题场景：**
- 如何控制谁可以合并代码到主分支？
- 如何管理不同角色的权限（维护者、贡献者、用户）？
- 如何保护关键分支不被误操作？

**解决方案：**
- **分支保护规则**：主分支需要代码审查才能合并
- **角色管理**：使用 GitHub/GitLab 的权限系统管理不同角色
- **自动化检查**：要求通过测试、lint 检查才能合并

**实际影响：**
- 保护代码库的稳定性
- 确保代码质量
- 明确责任分工

---

## 2. 项目管理的核心要素

### 2.1 测试（Testing）

**重要性：**
测试是确保代码质量的核心手段，能够：
- 验证代码功能是否符合预期
- 防止回归问题（新改动破坏旧功能）
- 作为代码文档，展示如何使用代码
- 支持安全重构

**测试类型：**

1. **单元测试（Unit Tests）**
   - 测试单个函数或类的功能
   - 快速、隔离、可重复
   - 工具：`pytest`、`unittest`

2. **集成测试（Integration Tests）**
   - 测试多个组件之间的交互
   - 验证系统整体功能

3. **端到端测试（E2E Tests）**
   - 测试完整的工作流程
   - 模拟真实使用场景

**最佳实践：**
- 测试覆盖率目标：80%+（关键代码 100%）
- 使用测试驱动开发（TDD）：先写测试，再写实现
- 测试应该独立、可重复、快速执行

**示例：**

```python
# tests/test_model.py
import pytest
from course.lecture_01.part_3_homework_lecture1.model import MoneyModel

def test_model_initialization():
    """Test that model initializes with correct number of agents."""
    model = MoneyModel(width=10, height=10, num_agents=50)
    assert len(model.schedule.agents) == 50
    assert model.grid.width == 10
    assert model.grid.height == 10

def test_agent_step():
    """Test agent step function updates agent state."""
    model = MoneyModel(width=10, height=10, num_agents=10)
    agent = model.schedule.agents[0]
    initial_wealth = agent.wealth
    agent.step()
    # Agent should have interacted with neighbors
    assert agent.wealth >= 0  # Wealth should be non-negative
```

### 2.2 文档（Documentation）

**重要性：**
文档是项目与用户、贡献者沟通的桥梁，包括：
- **README.md**：项目概览、快速开始、安装说明
- **API 文档**：函数、类的详细说明
- **教程和示例**：使用场景和最佳实践
- **贡献指南**：如何参与项目开发

**文档类型：**

1. **用户文档**
   - 安装指南
   - 使用教程
   - 常见问题（FAQ）
   - 示例代码

2. **开发者文档**
   - 架构设计
   - API 参考
   - 开发环境设置
   - 贡献指南

3. **代码文档**
   - 函数/类的 docstring
   - 行内注释（解释"为什么"而非"是什么"）

**最佳实践：**
- 使用 Google 或 NumPy 风格的 docstring
- 保持文档与代码同步更新
- 提供可运行的示例代码
- 使用文档生成工具（如 Sphinx、MkDocs）

**示例：**

```python
class MoneyAgent(Agent):
    """An agent with fixed initial wealth.

    The agent moves randomly and exchanges wealth with neighbors
    based on certain rules.

    Args:
        unique_id: Unique identifier for the agent.
        model: The model instance the agent belongs to.
        wealth: Initial wealth of the agent. Defaults to 1.

    Attributes:
        wealth: Current wealth of the agent.
        color: Color attribute of the agent ('red' or 'blue').
    """

    def __init__(self, unique_id, model, wealth=1):
        super().__init__(unique_id, model)
        self.wealth = wealth
        self.color = None
```

### 2.3 持续集成/持续部署（CI/CD）

**重要性：**
CI/CD 自动化了测试、构建、部署流程，确保：
- 每次代码提交都经过自动化检查
- 快速发现和修复问题
- 减少人工操作错误
- 提高发布效率

**CI/CD 流程：**

1. **持续集成（CI）**
   - 代码提交触发自动化测试
   - 运行 lint 检查
   - 构建项目
   - 生成测试报告

2. **持续部署（CD）**
   - 自动部署到测试环境
   - 运行集成测试
   - 部署到生产环境（可选）

**常用工具：**
- **GitHub Actions**：GitHub 集成的 CI/CD 平台
- **GitLab CI**：GitLab 的 CI/CD 系统
- **Jenkins**：开源的自动化服务器

**示例 GitHub Actions 配置：**

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install uv
        uv sync
    - name: Run tests
      run: |
        uv run pytest tests/ --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### 2.4 代码质量工具

**Linting（代码检查）：**
- **Ruff**：快速的 Python linter，替代 Flake8、isort 等
- **Pylint**：全面的代码质量检查
- **mypy**：静态类型检查

**格式化（Formatting）：**
- **Black**：统一的代码格式化工具
- **Ruff format**：Ruff 内置的格式化功能

**Pre-commit Hooks：**
在提交代码前自动运行检查，确保代码质量：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### 2.5 依赖管理

**重要性：**
- 确保项目在不同环境中使用相同的依赖版本
- 避免依赖冲突
- 简化安装流程

**工具选择：**

1. **pyproject.toml + uv/pip**
   - 现代 Python 项目标准
   - 统一管理项目元数据和依赖
   - `uv` 提供更快的依赖解析和安装

2. **requirements.txt**
   - 传统方式，简单直接
   - 适合小型项目

**示例 pyproject.toml：**

```toml
[project]
name = "course"
version = "0.1.0"
description = "ABM Course Materials"
requires-python = ">=3.11"
dependencies = [
    "mesa>=3.3.1",
    "numpy>=2.2.2",
    "pandas>=2.3.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "pre-commit>=4.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## 3. 项目管理的最佳实践

### 3.1 项目结构

**推荐的项目结构：**

```
project-name/
├── .github/
│   └── workflows/          # CI/CD 配置
├── docs/                   # 文档
│   ├── conf.py
│   └── index.md
├── src/                    # 源代码（src-layout）
│   └── package_name/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/                  # 测试代码
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── .gitignore              # Git 忽略文件
├── .pre-commit-config.yaml # Pre-commit 配置
├── pyproject.toml          # 项目配置
├── README.md               # 项目说明
└── LICENSE                 # 许可证
```

**为什么使用 src-layout？**
- 避免导入本地开发代码而非安装的包
- 强制测试安装的包，而非源代码
- 更清晰的项目结构

### 3.2 版本控制最佳实践

1. **分支策略**
   - `main`：生产环境代码
   - `develop`：开发分支
   - `feature/*`：功能分支
   - `fix/*`：修复分支

2. **提交信息规范**
   - 使用清晰的提交信息
   - 遵循约定式提交（Conventional Commits）
   - 示例：`feat: add color attribute to MoneyAgent`

3. **代码审查**
   - 所有代码变更通过 Pull Request
   - 至少一人审查后才能合并
   - 使用自动化检查确保代码质量

### 3.3 开发工作流

**典型开发流程：**

1. **创建功能分支**
   ```bash
   git checkout -b feature/add-color-attribute
   ```

2. **开发代码**
   - 编写代码
   - 编写测试
   - 运行测试确保通过

3. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add color attribute to MoneyAgent"
   ```

4. **推送并创建 Pull Request**
   ```bash
   git push origin feature/add-color-attribute
   ```

5. **代码审查和合并**
   - 等待审查反馈
   - 根据反馈修改
   - 审查通过后合并到主分支

### 3.4 发布流程

1. **版本号管理**
   - 遵循语义化版本（Semantic Versioning）
   - 格式：`MAJOR.MINOR.PATCH`（如 1.2.3）

2. **发布检查清单**
   - [ ] 所有测试通过
   - [ ] 文档已更新
   - [ ] 版本号已更新
   - [ ] CHANGELOG 已更新
   - [ ] 创建 Git tag

3. **自动化发布**
   - 使用 CI/CD 自动构建和发布
   - 自动生成发布说明

---

## 4. 工具与资源

### 4.1 推荐工具栈

**项目管理：**
- **uv**：快速的 Python 包管理器和项目管理工具
- **poetry**：依赖管理和打包工具
- **hatch**：现代 Python 项目构建工具

**代码质量：**
- **Ruff**：快速的 linter 和 formatter
- **mypy**：静态类型检查
- **pre-commit**：Git hooks 管理

**测试：**
- **pytest**：测试框架
- **pytest-cov**：测试覆盖率
- **tox**：多环境测试

**文档：**
- **Sphinx**：文档生成工具
- **MkDocs**：基于 Markdown 的文档生成
- **Jupyter Book**：基于 Jupyter 的文档

**CI/CD：**
- **GitHub Actions**：GitHub 集成的 CI/CD
- **GitLab CI**：GitLab 的 CI/CD
- **CircleCI**：云 CI/CD 平台

### 4.2 学习资源

**参考项目：**
- [Python Project Template](https://songshgeo.github.io/Python-Project-Template/doc/tools/)：完整的 Python 项目模板和工具说明

**官方文档：**
- [Python Packaging User Guide](https://packaging.python.org/)：Python 打包官方指南
- [PEP 517](https://peps.python.org/pep-0517/)：构建系统接口规范
- [PEP 518](https://peps.python.org/pep-0518/)：指定构建系统要求

**最佳实践指南：**
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)：Python 最佳实践指南
- [Real Python](https://realpython.com/)：Python 教程和最佳实践

### 4.3 快速开始检查清单

**新项目设置：**

- [ ] 创建项目结构（使用 src-layout）
- [ ] 配置 `pyproject.toml`
- [ ] 设置 Git 仓库和 `.gitignore`
- [ ] 配置 pre-commit hooks
- [ ] 编写 README.md
- [ ] 设置 CI/CD（如 GitHub Actions）
- [ ] 编写初始测试
- [ ] 配置代码质量工具（Ruff、mypy）

**持续维护：**

- [ ] 保持依赖更新
- [ ] 定期运行测试
- [ ] 更新文档
- [ ] 审查和合并 Pull Request
- [ ] 发布新版本

---

## 总结

Python 项目管理不仅仅是工具的使用，更是一种工程思维的体现。通过：

1. **标准化**：统一的项目结构和工具配置
2. **自动化**：测试、检查、部署的自动化
3. **文档化**：清晰的文档和代码注释
4. **协作化**：规范的开发流程和代码审查

我们可以构建出高质量、可维护、可协作的 Python 项目。记住：**好的项目管理是长期投资，虽然初期需要一些时间投入，但会显著提高项目的质量和开发效率。**
