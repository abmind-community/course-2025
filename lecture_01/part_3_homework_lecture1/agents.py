"""定义 MoneyModel 中的智能体行为。

本示例展示了最简单的“财富交换”机制：

1. 代理在二维网格上随机移动。
2. 若与其他代理处于同一格子且自身仍有财富，则随机赠送 1 单位财富。

通过大量代理重复该过程，可以观察到财富分布与 Gini 系数的演化。
"""

from mesa.discrete_space import CellAgent

class MoneyAgent(CellAgent):
    """代表单个拥有财富的经济主体。"""

    def __init__(self, model, cell):
        """初始化代理。

        Args:
            model: 关联的 `MoneyModel` 实例。
            cell: 初始所在的网格格子（`Cell` 对象）。
        """
        super().__init__(model)
        self.cell = cell  # 代理所在的空间格子
        self.wealth = 1  # 初始财富设置为 1

    def move(self):
        """随机移动到邻居格子。"""
        self.cell = self.cell.neighborhood.select_random_cell()

    def give_money(self):
        """如果同格存在其他代理，则随机赠送 1 单位财富。"""
        cellmates = [a for a in self.cell.agents if a is not self]

        if cellmates:  # 仅在存在其他代理时才进行转移
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        """代理在单个时间步内的行为。"""
        self.move()  # 先移动后互动
        if self.wealth > 0:
            self.give_money()
            