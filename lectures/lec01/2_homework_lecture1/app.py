#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MoneyModel 可视化入口。

通过 Mesa 3.0 的 Solara 可视化栈，快速搭建空间视图与统计曲线：

* `SpaceRenderer`：负责渲染网格与代理位置（此处使用 Matplotlib 后端）。
* `make_plot_component`：将数据收集器中的 `Gini` 指标绘制成时间序列。
* `SolaraViz`：将空间视图、图表与可配置参数组合成交互式页面。

运行方式：

```bash
solara run app.py
```

或在 Notebook 中直接执行本文件。
"""

from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle
from model import MoneyModel

def agent_portrayal(agent):
    """定义 MoneyAgent 在空间视图中的外观。"""
    return AgentPortrayalStyle(color="orange", size=50)

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

# Create initial model instance
money_model = MoneyModel(n=50, width=10, height=10)


# --- 可视化 ---
renderer = SpaceRenderer(model=money_model, backend="matplotlib").render(
    agent_portrayal=agent_portrayal
)


GiniPlot = make_plot_component("Gini", page=1)

page = SolaraViz(
    money_model,
    renderer,
    components=[GiniPlot],
    model_params=model_params,
    name="Boltzmann Wealth Model",
)

# 在 Notebook 中直接显示页面（在 Solara 服务器下会自动处理）
page



