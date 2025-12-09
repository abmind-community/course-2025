"""狼-羊捕食模型可视化启动脚本。

使用 Solara 构建交互式可视化界面，包含：
- 空间视图：显示网格和智能体位置
- 时间序列图：展示种群数量变化
- 控制台：交互式命令执行

运行方式：切换到对应目录和激活对应环境后，执行 solara run run.py
"""

# 导入模型和智能体
from model import WolfSheep
from agent import GrassPatch, Sheep, Wolf

# 导入 Mesa 可视化组件
from mesa.visualization import (
    CommandConsole,
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle


def wolf_sheep_portrayal(agent):
    """会传入进来多个 agent 对象，需要根据 agent 的类型，返回不同的可视化样式。
    
    Args:
        agent: 智能体对象，可以是 Wolf、Sheep 或 GrassPatch

    Returns:
        portrayal: 智能体的可视化样式，AgentPortrayalStyle 对象
    """
    if agent is None:
        return None

    portrayal = AgentPortrayalStyle(size=50, marker="o", zorder=2)

    if isinstance(agent, Wolf):
        portrayal.update(("color", "red"))
    elif isinstance(agent, Sheep):
        portrayal.update(("color", "white"))
    elif isinstance(agent, GrassPatch):
        color = "tab:green" if agent.fully_grown else "tab:brown"
        portrayal.update(("color", color), ("marker", "s"), ("size", 125), ("zorder", 1))

    return portrayal


# 模型参数配置
model_params = {
    "seed": {"type": "InputText", "value": 42, "label": "Random Seed"},
    "grass": {
        "type": "Select",
        "value": True,
        "values": [True, False],
        "label": "Grass regrowth enabled?",
    },
    
    "grass_regrowth_time": Slider("Grass Regrowth Time", 20, 1, 50),
    "initial_sheep": Slider("Initial Sheep Population", 100, 10, 300),
    "sheep_reproduce": Slider("Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01),
    "initial_wolves": Slider("Initial Wolf Population", 10, 5, 100),
    "wolf_reproduce": Slider("Wolf Reproduction Rate", 0.05, 0.01, 1.0, 0.01),
    "wolf_gain_from_food": Slider("Wolf Gain From Food", 20, 1, 50),
    "sheep_gain_from_food": Slider("Sheep Gain From Food", 4, 1, 10),
}


def post_process_space(ax):
    """美化空间视图：设置等比例并移除坐标轴。"""
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    """美化曲线图：调整图例位置。"""
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))


# 创建可视化组件
lineplot_component = make_plot_component(
    {"Wolves": "tab:orange", "Sheep": "tab:cyan", "Grass": "tab:green"},
    post_process=post_process_lines,
)

# 初始化模型
model = WolfSheep(grass=True)

# 创建空间渲染器
renderer = SpaceRenderer(model, backend="matplotlib")
renderer.draw_agents(wolf_sheep_portrayal)
renderer.post_process = post_process_space

# 创建可视化页面
page = SolaraViz(
    model,
    renderer,
    components=[lineplot_component, CommandConsole],
    model_params=model_params,
    name="Wolf Sheep",
)

page  # noqa

