# Schelling Segregation Model - 扩展版

## 概述

这是经典 Schelling 隔离模型的扩展实现，增加了以下教学功能：

1. **多种邻域配置**：4邻域、8邻域、24邻域
2. **可自定义效用函数**：线性、二次、峰值、Sigmoid等
3. **两种实现方式**：函数式和面向对象（用于教学对比）
4. **性能优化选项**：卷积方法用于大规模模拟

## 新增功能

### 1. 邻域配置 (neighborhoods.py)

支持三种邻域类型：

- **Von Neumann (4邻域)**：上下左右4个邻居
- **Moore (8邻域)**：周围8个邻居（原版默认）
- **Extended (24邻域)**：扩展到半径2的范围

提供两种实现：
- **偏移量方法**：直观易懂，适合教学
- **卷积方法**：高性能，适合大规模模拟

### 2. 效用函数 (utility_classes.py & utility_functions.py)

支持多种效用函数来表示智能体偏好：

- **ThresholdUtility**：阈值效用（原版Schelling）
- **LinearUtility**：线性效用
- **QuadraticUtility**：二次效用（更偏好高相似度）
- **PeakedUtility**：峰值效用（偏好中等多样性）
- **SigmoidUtility**：S形曲线效用
- **自定义**：可继承BaseUtility创建自己的效用函数

两种实现风格：
- **utility_classes.py**：面向对象版本（推荐，易扩展）
- **utility_functions.py**：函数式版本（简单快速）

### 3. 可配置智能体 (agents.py)

- **SchellingAgent**：使用面向对象效用函数
- **SchellingAgentFunctional**：使用函数式效用函数

## 文件结构

```
schelling/
├── model.py                    # 主模型类（已更新）
├── agents.py                   # 智能体类（新增）
├── neighborhoods.py            # 邻域配置（新增）
├── utility_classes.py          # 效用函数-OOP版本（新增）
├── utility_functions.py        # 效用函数-函数式版本（新增）
├── examples.ipynb              # 完整使用示例（新增）
├── analysis.ipynb              # 原始分析notebook
├── Readme.md                   # 本文件
└── resources/                  # 可视化资源
```

## 快速开始

### 基本使用（兼容原版）

```python
from model import Schelling

# 使用默认配置
model = Schelling(
    height=20,
    width=20,
    density=0.8,
    minority_pc=0.5,
    homophily=0.3,  # 阈值
    seed=42
)

# 运行模型
for _ in range(100):
    model.step()
    if not model.running:
        break
```

### 使用不同邻域

```python
from model import Schelling
from neighborhoods import NeighborhoodType

# 4邻域
model = Schelling(
    height=20,
    width=20,
    neighborhood_type=NeighborhoodType.VON_NEUMANN,
    seed=42
)

# 24邻域
model = Schelling(
    height=20,
    width=20,
    neighborhood_type=NeighborhoodType.EXTENDED,
    radius=2,
    seed=42
)
```

### 使用自定义效用函数

```python
from model import Schelling
from utility_classes import LinearUtility, PeakedUtility

# 线性效用
model1 = Schelling(
    height=20,
    width=20,
    utility_function=LinearUtility(),
    seed=42
)

# 峰值效用（偏好50%相似度）
model2 = Schelling(
    height=20,
    width=20,
    utility_function=PeakedUtility(optimal_fraction=0.5, tolerance=0.2),
    seed=42
)
```

### 创建自定义效用函数

```python
from utility_classes import BaseUtility

class MyUtility(BaseUtility):
    def __init__(self, threshold=0.5):
        super().__init__()
        self.threshold = threshold

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0
        similarity = similar_count / total_count
        # 自定义逻辑
        return 1.0 if similarity >= self.threshold else 0.0

# 使用自定义效用函数
model = Schelling(
    height=20,
    width=20,
    utility_function=MyUtility(threshold=0.4),
    seed=42
)
```

## 运行示例

### 1. 查看邻域类型

```bash
python neighborhoods.py
```

### 2. 查看效用函数

```bash
python utility_classes.py
```

### 3. 运行完整示例

```bash
jupyter notebook examples.ipynb
```

### 4. 交互式可视化

```bash
solara run model.py
```

## 教学用途

本扩展版本特别适合：

1. **概念教学**：通过不同邻域理解空间影响
2. **偏好建模**：通过效用函数理解个体决策
3. **对比实验**：比较不同配置的模拟结果
4. **编程练习**：学习OOP设计和函数式编程
5. **性能优化**：理解偏移量法vs卷积法

## 作业建议

1. 比较4邻域、8邻域、24邻域对隔离程度的影响
2. 实现一个新的效用函数并分析其效果
3. 使用参数扫描找到"临界点"
4. 对比偏移量方法和卷积方法的性能差异
5. 探索不同效用函数组合的社会含义

## 参考文献

Schelling, Thomas C. Dynamic Models of Segregation. Journal of Mathematical Sociology. 1971, Vol. 1, pp 143-186.

[原始论文PDF](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)

[Parable of the Polygons](http://ncase.me/polygons/) - 交互式解释

## 依赖

- mesa
- numpy
- scipy
- matplotlib
- pandas
- solara (可视化，可选)
