"""
智能体模块
定义可配置的 Schelling 智能体，支持：
- 多种邻域类型（4邻域、8邻域、24邻域）
- 自定义效用函数
"""

from mesa.discrete_space import CellAgent
from typing import Callable, Optional

from neighborhoods import NeighborhoodType, get_neighborhood_offsets
from utility_classes import BaseUtility, ThresholdUtility


class SchellingAgent(CellAgent):
    """
    可配置的 Schelling 隔离模型智能体

    支持：
    - 多种邻域配置（Von Neumann, Moore, Extended）
    - 自定义效用函数（面向对象版本）
    """

    def __init__(
        self,
        model,
        cell,
        agent_type: int,
        neighborhood_type: NeighborhoodType = NeighborhoodType.MOORE,
        neighborhood_radius: int = 1,
        utility_function: Optional[BaseUtility] = None,
    ) -> None:
        """
        创建一个新的 Schelling 智能体

        Args:
            model: 模型实例
            cell: 智能体所在的网格单元
            agent_type: 智能体类型 (0 或 1)
            neighborhood_type: 邻域类型
            neighborhood_radius: 邻域半径
            utility_function: 效用函数对象（如果为None，使用默认的阈值函数）
        """
        super().__init__(model)
        self.cell = cell
        self.type = agent_type

        # 邻域配置
        self.neighborhood_type = neighborhood_type
        self.neighborhood_radius = neighborhood_radius

        # 效用函数
        if utility_function is None:
            self.utility_function = ThresholdUtility(threshold=0.3)
        else:
            self.utility_function = utility_function

        # 状态
        self.utility = 0.0
        self.happy = False
        self.similar_count = 0
        self.total_count = 0

    def get_neighbors(self):
        """
        获取邻居智能体列表（使用偏移量方法）

        Returns:
            邻居智能体列表
        """
        # 获取邻域偏移量
        offsets = get_neighborhood_offsets(
            self.neighborhood_type, self.neighborhood_radius
        )

        neighbors = []
        x, y = self.cell.coordinate

        # 遍历所有偏移量
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy

            # 检查边界（周期性边界条件）
            if hasattr(self.model.grid, "width"):
                nx = nx % self.model.grid.width
                ny = ny % self.model.grid.height

            # 获取该位置的智能体
            try:
                neighbor_cell = self.model.grid._cells.get((nx, ny))
                if neighbor_cell and neighbor_cell.agents:
                    neighbors.extend(neighbor_cell.agents)
            except (KeyError, AttributeError):
                continue

        return neighbors

    def calculate_utility(self) -> float:
        """
        计算当前位置的效用值

        Returns:
            效用值
        """
        # 获取邻居
        neighbors = self.get_neighbors()

        # 统计相似和总数
        self.total_count = len(neighbors)
        self.similar_count = sum(1 for n in neighbors if n.type == self.type)

        # 计算效用
        self.utility = self.utility_function.calculate(
            self.similar_count, self.total_count
        )

        return self.utility

    def assign_state(self) -> None:
        """
        更新智能体状态（效用和满意度）
        """
        self.calculate_utility()

        # 判断是否满意（效用 >= 0.5 表示满意）
        # 可以根据需要调整这个阈值
        happiness_threshold = 0.5
        if self.utility >= happiness_threshold:
            self.happy = True
            self.model.happy += 1
        else:
            self.happy = False

    def step(self) -> None:
        """
        智能体的行动步骤
        如果不满意，移动到随机空位置
        """
        if not self.happy:
            # 移动到随机空单元
            self.cell = self.model.grid.select_random_empty_cell()


class SchellingAgentFunctional(CellAgent):
    """
    使用函数式效用函数的 Schelling 智能体

    这是为了演示函数式和面向对象两种实现方式
    """

    def __init__(
        self,
        model,
        cell,
        agent_type: int,
        neighborhood_type: NeighborhoodType = NeighborhoodType.MOORE,
        neighborhood_radius: int = 1,
        utility_function: Optional[Callable] = None,
        utility_params: Optional[dict] = None,
    ) -> None:
        """
        创建一个新的 Schelling 智能体（函数式版本）

        Args:
            model: 模型实例
            cell: 智能体所在的网格单元
            agent_type: 智能体类型 (0 或 1)
            neighborhood_type: 邻域类型
            neighborhood_radius: 邻域半径
            utility_function: 效用函数（接受 similar_count, total_count, params）
            utility_params: 效用函数参数字典
        """
        super().__init__(model)
        self.cell = cell
        self.type = agent_type

        # 邻域配置
        self.neighborhood_type = neighborhood_type
        self.neighborhood_radius = neighborhood_radius

        # 效用函数（函数式）
        if utility_function is None:
            # 默认阈值函数
            from utility_functions import threshold_utility

            self.utility_function = threshold_utility
            self.utility_params = utility_params or {"threshold": 0.3}
        else:
            self.utility_function = utility_function
            self.utility_params = utility_params or {}

        # 状态
        self.utility = 0.0
        self.happy = False
        self.similar_count = 0
        self.total_count = 0

    def get_neighbors(self):
        """获取邻居智能体列表"""
        offsets = get_neighborhood_offsets(
            self.neighborhood_type, self.neighborhood_radius
        )

        neighbors = []
        x, y = self.cell.coordinate

        for dx, dy in offsets:
            nx, ny = x + dx, y + dy

            # 周期性边界条件
            if hasattr(self.model.grid, "width"):
                nx = nx % self.model.grid.width
                ny = ny % self.model.grid.height

            try:
                neighbor_cell = self.model.grid._cells.get((nx, ny))
                if neighbor_cell and neighbor_cell.agents:
                    neighbors.extend(neighbor_cell.agents)
            except (KeyError, AttributeError):
                continue

        return neighbors

    def calculate_utility(self) -> float:
        """计算当前位置的效用值"""
        neighbors = self.get_neighbors()

        self.total_count = len(neighbors)
        self.similar_count = sum(1 for n in neighbors if n.type == self.type)

        # 使用函数式效用函数
        self.utility = self.utility_function(
            self.similar_count, self.total_count, self.utility_params
        )

        return self.utility

    def assign_state(self) -> None:
        """更新智能体状态"""
        self.calculate_utility()

        happiness_threshold = 0.5
        if self.utility >= happiness_threshold:
            self.happy = True
            self.model.happy += 1
        else:
            self.happy = False

    def step(self) -> None:
        """智能体行动步骤"""
        if not self.happy:
            self.cell = self.model.grid.select_random_empty_cell()
