"""
使用 Repast4py 实现的谢林隔离模型。

本模块实现了一个分布式的、并行化的经典谢林隔离模型版本。Agent（居民）居住在网格中，并根据局部规则决定是否移动。如果同类邻居的比例低于指定的阈值，Agent 就会移动到一个随机位置。

本实现演示了：
1.  **分布式空间**：使用 `SharedGrid` 处理分布在多个进程中的 Agent。
2.  **Numba 优化**：使用 `@jitclass` 实现高性能的邻居查找。
3.  **MPI 同步**：处理 Agent 在不同秩（Rank）之间的状态转移。
4.  **数据记录**：使用 Repast4py 的日志基础设施。

运行模型：
> uv run mpirun -n 8 python schelling.py params.yaml
"""

from argparse import Namespace
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from mpi4py import MPI
from numba import int32
from numba.experimental import jitclass
from repast4py import context as ctx
from repast4py import core, logging, parameters, random, schedule, space
from repast4py.space import BorderType
from repast4py.space import DiscretePoint as dpt
from repast4py.space import OccupancyType
from scripts.analysis_utils import calculate_morans_i

# 使用 Numba 进行性能优化的网格邻居查找器，类似于 zombies 示例
spec = [
    ("mo", int32[:]),
    ("no", int32[:]),
    ("xmin", int32),
    ("ymin", int32),
    ("ymax", int32),
    ("xmax", int32),
]


def get_neighborhood_offsets(name: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    为不同的邻域类型生成偏移量数组。
    支持的类型："4" (Von Neumann), "8" (Moore), "12" (Von Neumann r=2), "24" (Moore r=2), "48" (Moore r=3), "80" (Moore r=4)。
    """
    name = str(name)
    if name == "4":
        # Von Neumann (4 邻域)
        mo = np.array([0, 0, 1, -1], dtype=np.int32)
        no = np.array([1, -1, 0, 0], dtype=np.int32)
    elif name == "12":
        # 扩展 Von Neumann 半径 2 (12 邻域)
        # 曼哈顿距离 <= 2
        xs, ys = [], []
        for x in range(-2, 3):
            for y in range(-2, 3):
                dist = abs(x) + abs(y)
                if dist > 0 and dist <= 2:
                    xs.append(x)
                    ys.append(y)
        mo = np.array(xs, dtype=np.int32)
        no = np.array(ys, dtype=np.int32)
    elif name == "24":
        # Moore 半径 2 (24 邻域)
        xs, ys = [], []
        for x in range(-2, 3):
            for y in range(-2, 3):
                if x == 0 and y == 0:
                    continue
                xs.append(x)
                ys.append(y)
        mo = np.array(xs, dtype=np.int32)
        no = np.array(ys, dtype=np.int32)
    elif name == "48":
        # Moore 半径 3 (48 邻域)
        xs, ys = [], []
        for x in range(-3, 4):
            for y in range(-3, 4):
                if x == 0 and y == 0:
                    continue
                xs.append(x)
                ys.append(y)
        mo = np.array(xs, dtype=np.int32)
        no = np.array(ys, dtype=np.int32)
    elif name == "80":
        # Moore 半径 4 (80 邻域)
        xs, ys = [], []
        for x in range(-4, 5):
            for y in range(-4, 5):
                if x == 0 and y == 0:
                    continue
                xs.append(x)
                ys.append(y)
        mo = np.array(xs, dtype=np.int32)
        no = np.array(ys, dtype=np.int32)
    else:
        # 默认为 Moore (8 邻域)
        mo = np.array([-1, 0, 1, -1, 1, -1, 0, 1], dtype=np.int32)
        no = np.array([1, 1, 1, 0, 0, -1, -1, -1], dtype=np.int32)

    return mo, no


@jitclass(cls_or_spec=spec)  # type: ignore
class GridNghFinder:
    """
    一个 Numba 优化的类，用于计算网格上的 Moore 邻域。

    这个类避免了在计算邻居坐标时 Python 循环的开销，这对于大型 Agent 模型的性能至关重要。

    属性:
        mo (np.array): 8 个邻居的 X 轴偏移量。
        no (np.array): 8 个邻居的 Y 轴偏移量。
        xmin, ymin (int): 网格的最小边界。
        xmax, ymax (int): 网格的最大边界。
    """

    def __init__(self, xmin, ymin, xmax, ymax, mo, no):
        # 从外部传入邻域偏移量
        self.mo = mo
        self.no = no
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def find(self, x, y):
        """
        计算特定网格单元的邻居坐标。

        参数:
            x (int): 中心单元的 x 坐标。
            y (int): 中心单元的 y 坐标。

        返回:
            np.array: 有效邻居坐标的 2D 数组 (x, y, 0)。
                      超出网格边界的坐标会被过滤掉 (Sticky 边界)。
        """
        xs = self.mo + x
        ys = self.no + y

        # 针对 Sticky 边界进行过滤（非周期性）
        # 示例通常使用 Sticky 边界，因此我们过滤越界坐标。
        # 如果是周期性网格，我们会进行取模运算。
        # 根据参数假设为 Sticky（非周期性）。

        xd = (xs >= self.xmin) & (xs < self.xmax)
        xs = xs[xd]
        ys = ys[xd]

        yd = (ys >= self.ymin) & (ys < self.ymax)
        xs = xs[yd]
        ys = ys[yd]

        return np.stack((xs, ys, np.zeros(len(ys), dtype=np.int32)), axis=-1)


class SchellingAgent(core.Agent):
    """
    表示谢林隔离模型中的一个 Agent（居民）。

    每个 Agent 属于特定的组（类型 0 或 1），并期望一定比例的邻居属于同一组。

    属性:
        agent_type (int): 组标识符（0 或 1）。
        threshold (float): 感到满意所需的相似邻居的最小比例。
        happy (bool): Agent 当前的满意度状态。
    """

    TYPE = 0

    def __init__(
        self,
        a_id: int,
        rank: int,
        agent_type: int,
        threshold: float,
        always_happy: bool = False,
    ):
        super().__init__(id=a_id, type=SchellingAgent.TYPE, rank=rank)
        self.agent_type = agent_type  # 0 or 1
        self.threshold = threshold
        self.happy = False
        self.always_happy = always_happy

    def save(self) -> Tuple:
        """
        Serializes the agent's state for MPI transfer.

        Returns:
            Tuple: A tuple containing (uid, agent_type, threshold, happy, always_happy).
        """
        return (
            self.uid,
            self.agent_type,
            self.threshold,
            self.happy,
            self.always_happy,
        )

    def step(self, model):
        """
        Agent 的主要行为循环。

        1. 使用模型的 `ngh_finder` 识别邻居。
        2. 计算相似邻居的比例。
        3. 更新 `happy` 状态。
        4. 如果不满意则移动。

        参数:
            model (Model): 仿真模型实例。
        """
        grid = model.grid
        pt = grid.get_location(self)

        if pt is None:
            return

        if self.always_happy:
            self.happy = True
            return

        # 检查邻居
        nghs = model.ngh_finder.find(pt.x, pt.y)

        similar = 0
        total_neighbors = 0

        at = dpt(0, 0, 0)
        for ngh in nghs:
            at._reset_from_array(ngh)
            for neighbor in grid.get_agents(at):
                # 不统计自己（如果 get_agents 返回包括自己在内的列表）
                if neighbor.uid != self.uid:
                    total_neighbors += 1
                    if neighbor.agent_type == self.agent_type:
                        similar += 1

        if total_neighbors > 0:
            similarity = similar / total_neighbors
            self.happy = similarity >= self.threshold
        else:
            self.happy = True  # 如果没有邻居，则默认为满意。通常假设。

        if not self.happy:
            self.move(model)

    def move(self, model):
        """
        将 Agent 移动到网格范围内的一个新的随机空位置。
        """
        rng = random.default_rng
        # 限制尝试次数以防止死循环（如果网格非常满）
        for _ in range(100):
            dest = model.grid.get_random_local_pt(rng)
            # 检查目标位置当前是否为空
            # SharedGrid 上的 get_agents() 将返回此秩 *本地* 的 Agent
            # 或来自其他秩的缓冲 Agent。如果返回任何 Agent，则表示被占用。
            if not any(model.grid.get_agents(dest)):
                model.grid.move(self, dest)
                return

        # 如果尝试多次后未找到空位，Agent 保持原地不动。
        # 如果网格非常密集，这种情况可能会发生。
        # Agent 在此 tick 保持不满意状态，并在下一个 tick 再次尝试。


agent_cache = {}


def restore_agent(agent_data: Tuple):
    """
    回调函数：在 MPI 同步期间从序列化状态恢复 Agent。

    如果 Agent 从一个进程的网格区域移动到另一个进程，此函数
    将在新进程上重建 Agent 对象。

    参数:
        agent_data (Tuple): `SchellingAgent.save()` 返回的元组。

    返回:
        SchellingAgent: 恢复的 Agent 实例。
    """
    uid = agent_data[0]
    if uid in agent_cache:
        agent = agent_cache[uid]
    else:
        # 使用保存的类型和阈值重新创建 Agent
        # agent_data: (uid, agent_type, threshold, happy, always_happy)
        always_happy = agent_data[4] if len(agent_data) > 4 else False
        agent = SchellingAgent(
            uid[0], uid[2], agent_data[1], agent_data[2], always_happy
        )
        agent_cache[uid] = agent

    agent.happy = agent_data[3]
    return agent


@dataclass
class Summary:
    """
    用于跨 MPI 秩聚合仿真统计数据的数据容器。
    """

    total_agents: int = 0
    total_happy: int = 0
    percent_happy: float = 0.0


class Model:
    """
    中央仿真控制器。

    负责初始化、调度、网格管理以及协调分布式仿真步骤。
    """

    def __init__(self, comm: MPI.Intracomm, params: Dict):
        """
        初始化仿真模型。

        参数:
            comm (MPI.Intracomm): 用于进程间通信的 MPI 通信器。
            params (Dict): 配置参数（网格大小、Agent 数量等）。
        """
        self.comm = comm
        self.rank = comm.Get_rank()
        self.params = params

        self.world_width = params["world.width"]
        self.world_height = params["world.height"]

        self.runner = schedule.init_schedule_runner(comm)
        self.runner.schedule_repeating_event(1, 1, self.step)
        self.runner.schedule_stop(params["stop.at"])
        self.runner.schedule_end_event(evt=self.at_end)

        self.context = ctx.SharedContext(comm=comm)

        # 配置邻域
        nh_type = params.get("neighborhood", "8")
        mo, no = get_neighborhood_offsets(nh_type)

        # 根据邻域的最大范围确定缓冲区大小
        # 这确保了边界上的 Agent 可以看到足够的幽灵（Ghost）单元
        max_dist = max(np.max(np.abs(mo)), np.max(np.abs(no)))

        # 定义网格
        box = space.BoundingBox(0, self.world_width, 0, self.world_height, 0, 0)
        self.grid = space.SharedGrid(
            name="grid",
            bounds=box,
            borders=BorderType.Sticky,
            occupancy=OccupancyType.Single,
            buffer_size=int(max_dist),
            comm=comm,
        )
        self.context.add_projection(self.grid)

        self.ngh_finder = GridNghFinder(
            0, 0, self.world_width, self.world_height, mo, no
        )

        # 初始化 Agent
        # 在各秩之间分配 Agent 创建任务
        world_size = comm.Get_size()

        grid_size = self.world_width * self.world_height
        empty_ratio = params["empty_ratio"]
        total_agents = int(grid_size * (1 - empty_ratio))

        # 简单的创建责任分配
        my_agent_count = total_agents // world_size
        if self.rank < (total_agents % world_size):
            my_agent_count += 1

        rng = random.default_rng
        threshold = params["threshold"]
        always_happy_ratio = params.get("always_happy_ratio", 0.0)

        happy_count = 0
        for i in range(my_agent_count):
            # 类型大约 50/50 分裂，或随机
            a_type = rng.integers(0, 2)
            is_always_happy = rng.random() < always_happy_ratio
            if is_always_happy:
                happy_count += 1
            agent = SchellingAgent(i, self.rank, a_type, threshold, is_always_happy)
            self.context.add(agent)

            # 放置在随机位置，确保为空
            while True:
                pt = self.grid.get_random_local_pt(rng)
                if not any(self.grid.get_agents(pt)):
                    self.grid.move(agent, pt)
                    break

        if self.rank == 0:
            print(
                f"Rank {self.rank}: Initialized {happy_count}/{my_agent_count} agents as always happy (Target Ratio: {always_happy_ratio})"
            )

        # 日志记录
        self.summary = Summary()
        # 汇总满意计数
        loggers = logging.create_loggers(
            self.summary,
            op=MPI.SUM,
            names={"total_happy": "happy", "total_agents": "total"},
            rank=self.rank,
        )
        self.data_set = logging.ReducingDataSet(
            loggers, comm, params["summary_log_file"]
        )

        self.agent_logger = logging.TabularLogger(
            comm,
            params["agent_log_file"],
            ["tick", "agent_id", "rank", "type", "happy", "x", "y"],
        )

    def step(self):
        """
        执行仿真的一步（tick）。

        1. **Agent 行为**：对本地上下文中的所有 Agent 调用 `step()`。
        2. **同步**：同步上下文以处理 Agent 在进程间的移动。
        3. **日志记录**：记录 Agent 的当前状态和聚合统计数据。
        """
        # 移动/更新 Agent
        # 注意：在谢林模型中，顺序更新有时首选以避免震荡，
        # 但在并行 ABM 中，同步步骤是标准。
        # 我们基于*当前*状态（tick 开始时）检查满意度，然后移动。
        # 这是同步的。

        for agent in self.context.agents():
            agent.step(self)

        self.context.synchronize(restore_agent)

        # 日志记录
        tick = self.runner.schedule.tick

        local_happy = 0
        local_total = 0
        for agent in self.context.agents():
            local_total += 1
            if agent.happy:
                local_happy += 1

            pt = self.grid.get_location(agent)
            if pt is None:
                continue
            self.agent_logger.log_row(
                tick,
                agent.id,
                agent.uid[2],
                agent.agent_type,
                int(agent.happy),
                pt.x,
                pt.y,
            )

        self.summary.total_happy = local_happy
        self.summary.total_agents = local_total
        self.summary.percent_happy = 0  # 由 Reducer 或后处理计算？Reducer 汇总字段。

        # 检查全局停止条件（没有不满意的 Agent）
        local_unhappy = local_total - local_happy
        total_unhappy = self.comm.allreduce(local_unhappy, op=MPI.SUM)

        if total_unhappy == 0:
            self.runner.stop()

        # 我们无法轻易在 Reducer 内部自动计算百分比用于日志，除非定义自定义操作。
        # 但我们记录了总数，所以可以稍后计算百分比。

        self.data_set.log(tick)
        self.agent_logger.write()

    def at_end(self):
        """
        在仿真结束时调用的清理方法。
        关闭任何打开的数据日志文件句柄。
        """
        self.data_set.close()
        self.agent_logger.close()

        # Calculate and save final Moran's I if running on Rank 0 and file is specified
        if self.rank == 0 and "moran_file" in self.params:
            moran_file = self.params["moran_file"]
            try:
                # Build grid matrix
                # Note: This assumes n=1 or that we only care about local agents if distributed.
                # For n=1 (single process), local agents are all agents.

                # Use numpy.full with NaN
                grid_matrix = np.full((self.world_height, self.world_width), np.nan)

                for agent in self.context.agents():
                    pt = self.grid.get_location(agent)
                    if pt:
                        # Value: 1 for type 1, -1 for type 0 (matching final_stats.py logic)
                        val = 1 if agent.agent_type == 1 else -1
                        # Repast grid coords might need checking, but usually 0..W-1
                        if (
                            0 <= pt.x < self.world_width
                            and 0 <= pt.y < self.world_height
                        ):
                            grid_matrix[pt.y, pt.x] = val

                moran_i = calculate_morans_i(grid_matrix)

                import os

                os.makedirs(os.path.dirname(moran_file), exist_ok=True)
                with open(moran_file, "w") as f:
                    f.write(str(moran_i))
                # print(f"Rank 0: Saved final Moran's I ({moran_i}) to {moran_file}")
            except Exception as e:
                print(f"Error calculating/saving Moran's I: {e}")

    def start(self):
        """
        启动仿真运行器。
        """
        self.runner.execute()


def run(params: Dict):
    """
    设置和运行模型的入口点。

    参数:
        params (Dict): 从命令行或文件解析的参数字典。
    """
    model = Model(MPI.COMM_WORLD, params)
    model.start()


if __name__ == "__main__":
    parser = parameters.create_args_parser()
    args: Namespace = parser.parse_args()
    params = parameters.init_params(args.parameters_file, args.parameters)
    run(params)
