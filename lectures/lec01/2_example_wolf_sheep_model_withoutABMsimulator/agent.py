"""Agent definitions for the Wolf-Sheep predation example.

Animal 基类，封装通用的能量与生命周期逻辑。
Sheep 和 Wolf 继承自 Animal 基类，封装了吃草和捕食的行为。
GrassPatch 是固定位置的智能体，封装了草地生长和再生的逻辑。

This模块包含三类智能体：
1. `Sheep` —— 会移动、吃草、繁殖、消耗能量。
2. `Wolf`  —— 会移动、捕食羊、繁殖、消耗能量。
3. `GrassPatch` —— 固定在格子上，被吃后会按设定的再生时间重新生长。

所有移动型动物都继承 `Animal`，通过复用能量流转、繁殖与死亡逻辑，便于扩展。
"""

from mesa.discrete_space import CellAgent, FixedAgent

class Animal(CellAgent):
    """动物基类，封装通用的能量与生命周期逻辑。"""

    def __init__(
        self, model, energy=8, p_reproduce=0.04, energy_from_food=4, cell=None
    ):
        """Initialize an animal.

        Args:
            model: Model instance
            energy: Starting amount of energy
            p_reproduce: Probability of reproduction (asexual)
            energy_from_food: Energy obtained from 1 unit of food
            cell: Cell in which the animal starts
        """
        super().__init__(model)
        self.energy = energy  # 当前能量值
        self.p_reproduce = p_reproduce  # 繁殖概率（无性繁殖）
        self.energy_from_food = energy_from_food  # 每次进食获得的能量
        self.cell = cell  # 动物所处的网格 Cell 对象

    def spawn_offspring(self):
        """创建一个与当前类型相同的后代，并按能量守恒分摊。"""
        self.energy /= 2  # 后代与父代均分能量，避免能量凭空增加
        self.__class__( # 创建一个与当前类型相同的后代，并按能量守恒分摊。
            self.model, # 模型实例
            self.energy, # 能量
            self.p_reproduce, # 繁殖概率
            self.energy_from_food, # 每次进食获得的能量
            self.cell, # 动物所处的网格 Cell 对象
        )

    def feed(self):
        """抽象方法，由子类实现具体进食逻辑。"""

    def step(self):
        """执行动物的一个行为周期。"""
        # 1. 先移动到邻近网格（具体策略由子类实现）
        self.move()

        # 2. 移动会消耗基础能量
        self.energy -= 1

        # 3. 尝试进食获取能量
        self.feed()

        # 4. 能量耗尽则死亡；否则按概率繁殖
        if self.energy < 0:
            self.remove()
        elif self.random.random() < self.p_reproduce:
            self.spawn_offspring()

class Sheep(Animal):
    """羊：会避开狼、优先寻草的草食动物。"""

    def feed(self):
        """若所在格子存在可食用草地，则摄入能量并触发草地再生倒计时。"""
        grass_patch = next(  # 获取同一 cell 中的草地对象
            obj for obj in self.cell.agents if isinstance(obj, GrassPatch)
        )
        if grass_patch.fully_grown:  # 草地成熟即可食用
            self.energy += self.energy_from_food
            grass_patch.fully_grown = False

    def move(self):
        """优先移动至安全且有成熟草地的格子。"""
        cells_without_wolves = self.cell.neighborhood.select( # 自动获取周围 cell 的列表
            lambda cell: not any(isinstance(obj, Wolf) for obj in cell.agents) # 查看是否周围 cell 中有 Wolf 对象
        )
        if len(cells_without_wolves) == 0:
            return  # 周围全是狼则原地不动，避免送死

        cells_with_grass = cells_without_wolves.select( # 自动获取周围 cell 的列表
            lambda cell: any(
                isinstance(obj, GrassPatch) and obj.fully_grown for obj in cell.agents
            )
        )
        target_cells = (
            cells_with_grass if len(cells_with_grass) > 0 else cells_without_wolves
        )
        self.cell = target_cells.select_random_cell()


class Wolf(Animal):
    """狼：会追逐羊的捕食者。"""

    def feed(self):
        """若当前格子有羊，随机捕食一只并获得能量。"""
        sheep = [obj for obj in self.cell.agents if isinstance(obj, Sheep)]
        if sheep:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.energy_from_food
            sheep_to_eat.remove()  # Mesa 会负责从空间与调度器中移除

    def move(self):
        """优先向有羊的邻居格子移动，以提高捕食概率。"""
        cells_with_sheep = self.cell.neighborhood.select(
            lambda cell: any(isinstance(obj, Sheep) for obj in cell.agents)
        )
        target_cells = (
            cells_with_sheep if len(cells_with_sheep) > 0 else self.cell.neighborhood
        )
        self.cell = target_cells.select_random_cell()


class GrassPatch(FixedAgent):
    """草地：被羊啃食后按固定时间再生的固定型智能体。"""

    def __init__(self, model, countdown, grass_regrowth_time, cell):
        """创建草地智能体。

        Args:
            model: 模型实例
            countdown: 距离成熟还需等待的步数
            grass_regrowth_time: 再生所需的总步数
            cell: 所在的网格格子
        """
        super().__init__(model)
        self.grass_regrowth_time = grass_regrowth_time
        self.countdown = countdown
        self.cell = cell
        self._fully_grown = countdown == 0

    @property
    def fully_grown(self):
        """草地是否成熟可食。"""
        return self._fully_grown

    @fully_grown.setter # 设置草地状态：被吃掉时重置倒计时。
    def fully_grown(self, value: bool) -> None:
        """设置草地状态：被吃掉时重置倒计时。"""
        self._fully_grown = value
        if not value:
            self.countdown = self.grass_regrowth_time
            
            
