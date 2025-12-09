# 财富分配模型（Boltzmann Wealth Model）详解

## 📋 目录
1. [模型概述](#模型概述)
2. [代码详解](#代码详解)
3. [关键概念](#关键概念)
4. [使用方法](#使用方法)
5. [可视化说明](#可视化说明)
6. [常见问题](#常见问题)

---

## 🎯 模型概述

### 模型描述
财富分配模型模拟了智能体之间的财富转移过程，展示了即使从完全平等的初始状态开始，财富也会逐渐集中，形成不平等分布。

### 核心机制
- **移动**：智能体在网格空间中随机移动到邻居格子
- **财富转移**：智能体将 1 单位财富给予同一格子内的随机智能体
- **数据收集**：自动计算基尼系数来衡量财富不平等程度

### 模型特点
- 规则简单：每个时间步，智能体移动 → 给予财富（如果财富 > 0）
- 涌现行为：从简单规则中产生复杂的财富分布模式
- 财富守恒：总财富保持不变

---

## 📝 代码详解

### 1. 基尼系数计算

```python
def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B
```

**功能**：计算财富分配的不平等程度（0-1，0 表示完全平等，1 表示完全不平等）

### 2. MoneyAgent 类

#### 初始化
```python
def __init__(self, model, cell):
    super().__init__(model)
    self.cell = cell
    self.wealth = 1  # 初始财富为 1
```

#### 移动
```python
def move(self):
    self.cell = self.cell.neighborhood.select_random_cell()
```
随机移动到 8 方向邻居格子之一（Moore 邻域）

#### 给予财富
```python
def give_money(self):
    cellmates = [a for a in self.cell.agents if a is not self]
    if cellmates:
        other = self.random.choice(cellmates)
        other.wealth += 1
        self.wealth -= 1
```
将 1 单位财富给予同一格子内的随机智能体

#### 步进
```python
def step(self):
    self.move()
    if self.wealth > 0:
        self.give_money()
```
每个时间步：先移动，如果财富 > 0 则给予财富

### 3. MoneyModel 类

#### 初始化
```python
def __init__(self, n=10, width=10, height=10, seed=None):
    super().__init__(seed=seed)
    self.num_agents = n
    self.grid = OrthogonalMooreGrid((width, height), random=self.random)
    
    # 批量创建智能体
    MoneyAgent.create_agents(
        self,
        self.num_agents,
        self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
    )
    
    # 设置数据收集
    self.datacollector = mesa.DataCollector(
        model_reporters={"Gini": compute_gini}, 
        agent_reporters={"Wealth": "wealth"}
    )
    self.datacollector.collect(self)
```

**关键点**：
- 使用 `OrthogonalMooreGrid` 创建 8 方向邻居网格
- 使用 `create_agents()` 批量创建智能体
- 使用 `DataCollector` 自动收集基尼系数和财富数据

#### 步进
```python
def step(self):
    self.agents.shuffle_do("step")  # 随机顺序执行智能体
    self.datacollector.collect(self)  # 收集数据
```

---

## 🔧 关键概念

### 1. 网格空间
- **OrthogonalMooreGrid**：8 方向邻居网格（上、下、左、右、四个对角线）
- 每个格子可以包含多个智能体
- 默认环形边界（torus）

### 2. 智能体管理
- **create_agents()**：批量创建智能体，高效且灵活
- **shuffle_do()**：随机打乱顺序后执行方法，确保随机性

### 3. 数据收集
- **DataCollector**：自动收集模型和智能体数据
- **model_reporters**：模型级别统计（如基尼系数）
- **agent_reporters**：智能体级别属性（如财富值）

### 4. 基尼系数
- **范围**：0-1（0=完全平等，1=完全不平等）
- **意义**：衡量财富分配的不平等程度
- **变化**：初始接近 0，运行后上升并稳定在某个值

---

## 🚀 使用方法

### 基础运行
```python
# 创建模型
model = MoneyModel(n=100, width=10, height=10)

# 运行多个时间步
for _ in range(20):
    model.step()

# 获取数据
agent_data = model.datacollector.get_agent_vars_dataframe()
model_data = model.datacollector.get_model_vars_dataframe()
```

### 分析财富分布
```python
import seaborn as sns

# 获取最后一次的数据
data = model.datacollector.get_agent_vars_dataframe()
last_step = data[data.index.get_level_values('Step') == data.index.get_level_values('Step').max()]

# 绘制财富分布直方图
g = sns.histplot(last_step["Wealth"], discrete=True)
g.set(title="Wealth distribution", xlabel="Wealth", ylabel="number of agents")
```

### 观察基尼系数变化
```python
import matplotlib.pyplot as plt

model_data = model.datacollector.get_model_vars_dataframe()
plt.plot(model_data["Gini"])
plt.xlabel("Step")
plt.ylabel("Gini Coefficient")
plt.title("Wealth Inequality Over Time")
plt.show()
```

---

## 🎨 可视化说明

### 1. 智能体可视化函数
```python
def agent_portrayal(agent):
    return AgentPortrayalStyle(color="orange", size=50)
```
定义智能体的颜色和大小（可根据财富值动态设置）

### 2. 模型参数配置
```python
model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": 10,
    "height": 10,
}
```
定义交互式参数控件（滑块、输入框等）

### 3. 创建可视化
```python
# 创建空间渲染器
renderer = SpaceRenderer(model=money_model, backend="matplotlib").render(
    agent_portrayal=agent_portrayal
)

# 创建图表组件
GiniPlot = make_plot_component("Gini", page=1)

# 创建可视化页面
page = SolaraViz(
    money_model,
    renderer,
    components=[GiniPlot],
    model_params=model_params,
    name="Boltzmann Wealth Model",
)
```

**页面结构**：
- **Page 0**：空间可视化（网格和智能体）
- **Page 1**：基尼系数时间序列图
- **控制面板**：参数调整和运行控制

---

## 📖 参考资源

- Mesa 官方文档：https://mesa.readthedocs.io/
- 基尼系数维基百科：https://en.wikipedia.org/wiki/Gini_coefficient
