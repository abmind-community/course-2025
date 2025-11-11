# 狼-羊捕食模型（Wolf-Sheep Predation Model）设计与实现笔记

---

## 🎯 模型概述

### 模型描述
经典的捕食者-被捕食者生态系统模型，模拟狼、羊和草之间的相互作用：
- **羊（Sheep）**：吃草获取能量，能量耗尽死亡，可以繁殖
- **狼（Wolf）**：吃羊获取能量，能量耗尽死亡，可以繁殖
- **草地（Grass）**：被羊吃掉后会自动再生

### 核心机制
- 能量系统：每个智能体都有能量，消耗能量移动，通过进食补充能量
- 繁殖机制：智能体按概率繁殖，能量减半产生后代
- 空间交互：智能体在网格空间中移动，同一格子内的智能体可以交互
- 倒计时机制：使用 `countdown` 属性实现草地的延迟再生，在 `model.step()` 中手动更新

---

## 💡 设计思路

### 1. 分层设计

```
┌─────────────────────────────────┐
│   可视化层 (run.py)            │  ← 用户交互界面
├─────────────────────────────────┤
│   模型层 (model.py)             │  ← 整体控制和协调
├─────────────────────────────────┤
│   智能体层 (agent.py)           │  ← 个体行为实现
├─────────────────────────────────┤
│   基础设施层 (Mesa框架)         │  ← 空间、数据收集
└─────────────────────────────────┘
```

### 2. 继承关系

```
Agent (Mesa基类)
├── CellAgent (可移动的智能体)
│   └── Animal (动物基类)
│       ├── Sheep (羊)
│       └── Wolf (狼)
└── FixedAgent (固定位置的智能体)
    └── GrassPatch (草地)
```
---

## 🏗️ 架构设计

### 1. 文件结构

```
mesa_offical/
├── agent.py      # 智能体定义（Sheep, Wolf, GrassPatch）
├── model.py      # 模型定义（WolfSheep）
└── run.py        # 可视化启动脚本
```

### 2. 核心组件

#### 2.1 Model（模型层）
- **职责**：管理整个模拟环境
- **功能**：
  - 初始化空间（网格）
  - 创建智能体
  - 定义时间步行为（包括草地更新）
  - 收集数据

#### 2.2 Agent（智能体层）
- **Animal（基类）**：
  - 能量管理
  - 移动行为
  - 繁殖逻辑
  - 死亡判断
- **Sheep（羊）**：
  - 吃草行为
  - 避狼移动
- **Wolf（狼）**：
  - 捕食行为
  - 追羊移动
- **GrassPatch（草地）**：
  - 生长状态管理
  - 倒计时属性（countdown）

#### 2.3 Visualization（可视化层）
- **SpaceRenderer**：空间可视化
- **SolaraViz**：交互式可视化界面
- **DataCollector**：数据收集和图表

---

## 📝 实现步骤

### 步骤 1：定义智能体（agent.py）

#### 1.1 创建 Animal 基类
```python
class Animal(CellAgent):
    def __init__(self, model, energy, p_reproduce, energy_from_food, cell):
        # 初始化能量、繁殖概率等属性
        
    def step(self):
        # 定义基本行为：移动、消耗能量、进食、繁殖/死亡
```

**关键点**：
- 继承 `CellAgent`（可移动智能体）
- 使用 `self.__class__()` 实现动态类型创建
- 能量耗尽时调用 `self.remove()` 自动移除

#### 1.2 实现 Sheep 类
```python
class Sheep(Animal):
    def feed(self):
        # 查找当前格子的草地，如果已长好则吃掉
        
    def move(self):
        # 优先选择：1) 没有狼的格子 2) 有草的格子
```

**关键点**：
- 使用 `next()` 查找第一个匹配的草地
- 使用 `cell.neighborhood.select()` 过滤邻居格子
- 使用 `select_random_cell()` 随机选择目标

#### 1.3 实现 Wolf 类
```python
class Wolf(Animal):
    def feed(self):
        # 查找当前格子的羊，随机吃掉一只
        
    def move(self):
        # 优先选择有羊的格子
```

#### 1.4 实现 GrassPatch 类
```python
class GrassPatch(FixedAgent):
    def __init__(self, model, countdown, grass_regrowth_time, cell):
        # 初始化倒计时和生长状态
        
    @property
    def fully_grown(self):
        # 获取生长状态
        
    @fully_grown.setter
    def fully_grown(self, value):
        # 设置生长状态，如果被吃掉则重置倒计时
```

**关键点**：
- 使用 `countdown` 属性记录剩余等待时间
- 使用 `@property` 和 `@setter` 实现属性访问控制
- 被吃掉时重置 `countdown = grass_regrowth_time`
- 在 `model.step()` 中手动更新倒计时

### 步骤 2：定义模型（model.py）

#### 2.1 创建 WolfSheep 模型类
```python
class WolfSheep(Model):
    def __init__(self, ...):
        # 1. 初始化基类
        super().__init__(seed=seed)
        
        # 2. 创建空间
        self.grid = OrthogonalVonNeumannGrid(...)
        
        # 3. 设置数据收集
        self.datacollector = DataCollector(model_reporters)
        
        # 4. 创建智能体
        Sheep.create_agents(...)
        Wolf.create_agents(...)
        if grass:
            GrassPatch(...)
        
        # 5. 收集初始数据
        self.datacollector.collect(self)
```

**关键点**：
- 使用 `create_agents()` 批量创建智能体
- 使用 `DataCollector` 自动收集统计数据

#### 2.2 实现 step() 方法
```python
def step(self):
    # 1. 按类型分组执行智能体
    self.agents_by_type[Sheep].shuffle_do("step")
    self.agents_by_type[Wolf].shuffle_do("step")
    
    # 2. 手动更新草地倒计时
    if self.grass:
        for grass_patch in self.agents_by_type[GrassPatch]:
            if not grass_patch.fully_grown:
                grass_patch.countdown -= 1
                if grass_patch.countdown <= 0:
                    grass_patch.fully_grown = True
    
    # 3. 收集数据
    self.datacollector.collect(self)
```

**关键点**：
- 使用 `agents_by_type` 按类型分组
- 使用 `shuffle_do()` 随机顺序执行
- 先执行羊再执行狼，避免同一时间步内冲突
- **手动遍历草地并更新倒计时**，实现再生逻辑

### 步骤 3：创建可视化（run.py）

#### 3.1 定义可视化函数
```python
def wolf_sheep_portrayal(agent):
    # 根据智能体类型返回不同的可视化样式
    # - Wolf: 红色圆点
    # - Sheep: 白色圆点
    # - GrassPatch: 绿色/棕色方块
```

#### 3.2 设置模型参数
```python
model_params = {
    "seed": {...},
    "initial_sheep": Slider(...),
    "sheep_reproduce": Slider(...),
    # ... 其他参数
}
```

#### 3.3 创建可视化组件
```python
# 1. 创建空间渲染器
renderer = SpaceRenderer(model, backend="matplotlib")
renderer.draw_agents(wolf_sheep_portrayal)

# 2. 创建图表组件
lineplot_component = make_plot_component(
    {"Wolves": "tab:orange", "Sheep": "tab:cyan", "Grass": "tab:green"}
)

# 3. 创建可视化页面（不传递 simulator）
page = SolaraViz(
    model,
    renderer,
    components=[lineplot_component, CommandConsole],
    model_params=model_params,
    # 注意：不传递 simulator 参数
)
```

---

## 📚 参考资源

- Mesa 官方文档：https://mesa.readthedocs.io/
- NetLogo 原始模型：http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation

---

## 🔍 常见问题

### Q2: 为什么使用 `self.__class__()`？
**A**: 保证子类调用时创建子类实例，支持继承和多态。

### Q3: 草地再生如何工作？
**A**: 
1. 羊吃草时设置 `fully_grown = False`，触发 setter 重置 `countdown`
2. 每个时间步在 `model.step()` 中遍历所有草地
3. 未成熟的草地倒计时减 1，倒计时为 0 时设置为成熟
