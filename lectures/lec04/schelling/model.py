import os

import solara
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

from agents import SchellingAgent
from neighborhoods import NeighborhoodType
from utility_classes import BaseUtility, ThresholdUtility


class Schelling(Model):
    """Model class for the Schelling segregation model."""

    def __init__(
        self,
        height: int = 20,
        width: int = 20,
        density: float = 0.8,
        minority_pc: float = 0.5,
        homophily: float = 0.4,
        radius: int = 1,
        neighborhood_type: NeighborhoodType = NeighborhoodType.MOORE,
        utility_function: BaseUtility = None,
        seed=None,
    ):
        """Create a new Schelling model.

        Args:
            width: Width of the grid
            height: Height of the grid
            density: Initial chance for a cell to be populated (0-1)
            minority_pc: Chance for an agent to be in minority class (0-1)
            homophily: Minimum number of similar neighbors needed for happiness (兼容旧版)
            radius: Search radius for checking neighbor similarity
            neighborhood_type: 邻域类型 (VON_NEUMANN=4邻域, MOORE=8邻域, EXTENDED=24邻域)
            utility_function: 效用函数对象 (如果为None，使用阈值函数)
            seed: Seed for reproducibility
        """
        super().__init__(seed=seed)

        # Model parameters
        self.density = density
        self.minority_pc = minority_pc
        self.neighborhood_type = neighborhood_type
        self.neighborhood_radius = radius

        # 效用函数设置
        if utility_function is None:
            # 使用 homophily 参数创建默认的阈值效用函数（向后兼容）
            self.utility_function = ThresholdUtility(threshold=homophily)
        else:
            self.utility_function = utility_function

        # Initialize grid
        self.grid = OrthogonalMooreGrid((width, height), random=self.random, capacity=1)

        # Track happiness
        self.happy = 0

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={
                "happy": "happy",
                "pct_happy": lambda m: (
                    (m.happy / len(m.agents)) * 100 if len(m.agents) > 0 else 0
                ),
                "population": lambda m: len(m.agents),
                "minority_pct": lambda m: (
                    sum(1 for agent in m.agents if agent.type == 1)
                    / len(m.agents)
                    * 100
                    if len(m.agents) > 0
                    else 0
                ),
            },
            agent_reporters={"agent_type": "type"},
        )

        # Create agents and place them on the grid
        for cell in self.grid.all_cells:
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < minority_pc else 0
                SchellingAgent(
                    model=self,
                    cell=cell,
                    agent_type=agent_type,
                    neighborhood_type=self.neighborhood_type,
                    neighborhood_radius=self.neighborhood_radius,
                    utility_function=self.utility_function,
                )

        # Collect initial state
        self.agents.do("assign_state")
        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.happy = 0  # Reset counter of happy agents
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.agents.do("assign_state")
        self.datacollector.collect(self)  # Collect data
        self.running = self.happy < len(self.agents)  # Continue until everyone is happy


def get_happy_agents(model):
    """Display a text count of how many happy agents there are."""
    return solara.Markdown(f"**Happy agents: {model.happy}**")


path = os.path.dirname(os.path.abspath(__file__))


def agent_portrayal(agent):
    style = AgentPortrayalStyle(
        x=agent.cell.coordinate[0],
        y=agent.cell.coordinate[1],
        marker=os.path.join(path, "resources", "orange_happy.png"),
        size=75,
    )
    if agent.type == 0:
        if agent.happy:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "blue_happy.png"),
                ),
            )
        else:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "blue_unhappy.png"),
                ),
                ("size", 50),
                ("zorder", 2),
            )
    else:
        if not agent.happy:
            style.update(
                (
                    "marker",
                    os.path.join(path, "resources", "orange_unhappy.png"),
                ),
                ("size", 50),
                ("zorder", 2),
            )

    return style


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "density": Slider("Agent density", 0.8, 0.1, 1.0, 0.1),
    "minority_pc": Slider("Fraction minority", 0.2, 0.0, 1.0, 0.05),
    "homophily": Slider("Homophily", 0.4, 0.0, 1.0, 0.125),
    "width": 20,
    "height": 20,
}

# Note: Models with images as markers are very performance intensive.
model1 = Schelling()
renderer = SpaceRenderer(model1, backend="matplotlib")
# Here we use renderer.render() to render the agents and grid in one go.
# This function always renders the grid and then renders the agents or
# property layers on top of it if specified. It also supports passing the
# post_process function to fine-tune the plot after rendering in itself.
renderer.render(agent_portrayal=agent_portrayal)

HappyPlot = make_plot_component({"happy": "tab:green"})

page = SolaraViz(
    model1,
    renderer,
    components=[
        HappyPlot,
        get_happy_agents,
    ],
    model_params=model_params,
)
page  # noqa
