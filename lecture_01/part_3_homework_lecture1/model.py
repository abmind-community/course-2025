"""MoneyModel：演示随机财富交换的最小示例模型。"""

import mesa
from mesa.discrete_space import CellAgent, OrthogonalMooreGrid
from agents import MoneyAgent

def compute_gini(model):
    """按照洛伦兹曲线公式计算当前的 Gini 系数。"""

    agent_wealths = [agent.wealth for agent in model.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class MoneyModel(mesa.Model):
    """声明并控制 MoneyAgent 的整体环境。"""

    def __init__(self, n=10, width=10, height=10, seed=None):
        """设定初始参数并创建网格与代理。"""
        super().__init__(seed=seed)
        self.num_agents = n
        self.grid = OrthogonalMooreGrid((width, height), random=self.random)

        # Create agents
        MoneyAgent.create_agents(
            self,
            self.num_agents,
            self.random.choices(self.grid.all_cells.cells, k=self.num_agents),
        )

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"},
        )
        self.datacollector.collect(self)

    def step(self):
        """执行一个时间步并更新统计信息。"""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)