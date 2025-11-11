"""狼-羊捕食模型（Mesa 实现）
================================

本文件复现经典的 NetLogo Wolf-Sheep 模型，并展示 Mesa 3.0 的关键特性：

* 使用 `OrthogonalVonNeumannGrid` 构建环形网格空间。
* 通过 `ABMSimulator` 混合固定时间步与事件调度（草地再生）。
* 利用 `agents_by_type` 与 `create_agents` 高效地管理大量智能体。
* 通过 `DataCollector` 自动收集模型级指标，为可视化与分析提供支持。
"""

import math

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalVonNeumannGrid
from agent import GrassPatch, Sheep, Wolf

class WolfSheep(Model):
    """狼-羊-草生态系统模型。

    - `Sheep`：草食动物，会吃草并繁殖。
    - `Wolf`：捕食者，会吃羊并繁殖。
    - `GrassPatch`：草地，被吃掉后若启用草生长，则按倒计时恢复。

    模型展示了能量流转、捕食关系以及环境资源再生的交互效果。
    """

    def __init__(
        self,
        width=20,
        height=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=True,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
        seed=None,
    ):
        """初始化模型参数并构建环境。

        Args:
            width: 网格宽度。
            height: 网格高度。
            initial_sheep: 初始羊数量。
            initial_wolves: 初始狼数量。
            sheep_reproduce: 羊的每步繁殖概率。
            wolf_reproduce: 狼的每步繁殖概率。
            wolf_gain_from_food: 狼吃掉一只羊获得的能量。
            grass: 是否启用草地生长（若 False，羊将直接获取固定能量）。
            grass_regrowth_time: 草地被吃掉后重新长好的步数。
            sheep_gain_from_food: 羊吃草获得的能量。
            seed: 随机种子，便于复现随机实验。
        """
        super().__init__(seed=seed)
        
        # Initialize model parameters
        self.height = height
        self.width = width
        self.grass = grass

        # Create grid using experimental cell space
        self.grid = OrthogonalVonNeumannGrid(
            [self.height, self.width],
            torus=True,
            capacity=math.inf,  # 使用无限容量的格子，以便多智能体共存
            random=self.random,
        )

        # Set up data collection
        model_reporters = {
            "Wolves": lambda m: len(m.agents_by_type[Wolf]), # m 就是self（模型实例），访问模型实例的agents_by_type属性，获取狼的数量
            "Sheep": lambda m: len(m.agents_by_type[Sheep]), # m 就是self（模型实例），访问模型实例的agents_by_type属性，获取羊的数量
        }
        
        if grass:
            model_reporters["Grass"] = lambda m: len( # m 就是self（模型实例），访问模型实例的agents_by_type属性，获取草地的数量
                m.agents_by_type[GrassPatch].select(lambda a: a.fully_grown)
            )

        self.datacollector = DataCollector(model_reporters)

        # Create sheep:
        Sheep.create_agents( # 调用 Sheep 类的 create_agents 方法，创建羊
            self,
            initial_sheep,
            energy=self.rng.random((initial_sheep,)) * 2 * sheep_gain_from_food, # 生成初始能量，范围是0到2倍sheep_gain_from_food
            p_reproduce=sheep_reproduce,
            energy_from_food=sheep_gain_from_food,
            cell=self.random.choices(self.grid.all_cells.cells, k=initial_sheep), # 随机选择一个格子，作为羊的初始位置
        )
        # Create Wolves:
        Wolf.create_agents(
            self,
            initial_wolves,
            energy=self.rng.random((initial_wolves,)) * 2 * wolf_gain_from_food,
            p_reproduce=wolf_reproduce,
            energy_from_food=wolf_gain_from_food,
            cell=self.random.choices(self.grid.all_cells.cells, k=initial_wolves),
        )

        # Create grass patches if enabled
        if grass:
            possibly_fully_grown = [True, False]
            
            for cell in self.grid:
                # 模拟开始生成草地时，草地是否成熟，如果没有成熟需要一个随机数来决定
                fully_grown = self.random.choice(possibly_fully_grown)
                # countdown 表示草地距离成熟还需等待的步数，如果草地成熟，则倒计时为0，如果草地不成熟，则倒计时为随机数(0到grass_regrowth_time-1)
                countdown = (
                    0 if fully_grown else self.random.randrange(0, grass_regrowth_time)
                )
                # 创建草地，并设置倒计时（和上面create_agents类似的模板）
                GrassPatch(self, countdown, grass_regrowth_time, cell)

        # Collect initial data
        self.running = True 
        self.datacollector.collect(self)  # 记录初始种群数量

    def step(self):
        """执行一个时间步的模型更新。"""
        # 1. 先让羊执行（随机顺序），确保被捕食前有机会移动/吃草
        self.agents_by_type[Sheep].shuffle_do("step")
        # 2. 再执行狼，避免一个时间步内“狼瞬间移动后立刻被吃”之类的不合理情况
        self.agents_by_type[Wolf].shuffle_do("step")
        
        # 3. 更新草地（这里没有使用ABMsimulator）
        if self.grass:  # 如果启用了草地生长            
            for grass_patch in self.agents_by_type[GrassPatch]: # 遍历所有草地
                if not grass_patch.fully_grown: # 会首先判断草地是否成熟，如果没成熟，则倒计时减1
                    grass_patch.countdown -= 1 # 倒计时减1，如果倒计时小于等于0，则草地成熟
                    if grass_patch.countdown <= 0: # 如果倒计时小于等于0
                        grass_patch.fully_grown = True # 草地成熟
                else: # 如果草地成熟，则不进行任何操作
                    pass

        # 4. 更新观测数据，便于绘制时间序列曲线
        self.datacollector.collect(self) # 收集当前的种群数量
