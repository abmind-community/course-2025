"""
邻域配置模块
定义不同类型的邻域结构，提供两种实现方式：
1. 偏移量方法（Offset-based）：适合教学，直观易懂
2. 卷积方法（Convolution-based）：适合大规模模拟，性能优化
"""

from enum import Enum
from typing import List, Tuple

try:
    import numpy as np
    from scipy import signal

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    np = None
    signal = None


class NeighborhoodType(Enum):
    """邻域类型枚举"""

    VON_NEUMANN = "von_neumann"  # 4邻域（上下左右）
    MOORE = "moore"  # 8邻域（周围8个格子）
    EXTENDED = "extended"  # 24邻域（扩展到半径2的范围）


# ============================================================================
# 方法1: 偏移量方法（Offset-based）- 教学友好
# ============================================================================


def get_von_neumann_offsets(radius: int = 1) -> List[Tuple[int, int]]:
    """
    获取 Von Neumann 邻域的偏移量（曼哈顿距离）

    4邻域示例 (radius=1):
    ```
        N
      W X E
        S
    ```

    Args:
        radius: 邻域半径

    Returns:
        邻域偏移量列表 [(dx, dy), ...]

    Example:
        >>> get_von_neumann_offsets(1)
        [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上、下、左、右
    """
    offsets = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            manhattan_distance = abs(dx) + abs(dy)
            if 0 < manhattan_distance <= radius:
                offsets.append((dx, dy))
    return offsets


def get_moore_offsets(radius: int = 1) -> List[Tuple[int, int]]:
    """
    获取 Moore 邻域的偏移量（切比雪夫距离）

    8邻域示例 (radius=1):
    ```
      NW N NE
      W  X  E
      SW S SE
    ```

    Args:
        radius: 邻域半径

    Returns:
        邻域偏移量列表 [(dx, dy), ...]

    Example:
        >>> len(get_moore_offsets(1))
        8  # 8个邻居
    """
    offsets = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            chebyshev_distance = max(abs(dx), abs(dy))
            if chebyshev_distance <= radius:
                offsets.append((dx, dy))
    return offsets


def get_extended_offsets(radius: int = 2) -> List[Tuple[int, int]]:
    """
    获取扩展邻域的偏移量（24邻域 = 半径2的Moore邻域）

    24邻域示例 (radius=2):
    ```
      . . . . .
      . X X X .
      . X O X .
      . X X X .
      . . . . .
    ```

    Args:
        radius: 邻域半径，默认为2

    Returns:
        邻域偏移量列表 [(dx, dy), ...]
    """
    return get_moore_offsets(radius)


def get_neighborhood_offsets(
    neighborhood_type: NeighborhoodType, radius: int = 1
) -> List[Tuple[int, int]]:
    """
    根据邻域类型获取相应的偏移量

    Args:
        neighborhood_type: 邻域类型
        radius: 邻域半径

    Returns:
        邻域偏移量列表
    """
    if neighborhood_type == NeighborhoodType.VON_NEUMANN:
        return get_von_neumann_offsets(radius)
    elif neighborhood_type == NeighborhoodType.MOORE:
        return get_moore_offsets(radius)
    elif neighborhood_type == NeighborhoodType.EXTENDED:
        return get_extended_offsets(radius if radius > 1 else 2)
    else:
        raise ValueError(f"Unknown neighborhood type: {neighborhood_type}")


# ============================================================================
# 方法2: 卷积方法（Convolution-based）- 性能优化
# ============================================================================


def get_von_neumann_kernel(radius: int = 1):
    """
    获取 Von Neumann 邻域的卷积核

    4邻域卷积核示例 (radius=1):
    ```
      [[0, 1, 0],
       [1, 0, 1],
       [0, 1, 0]]
    ```

    Args:
        radius: 邻域半径

    Returns:
        卷积核数组
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("需要安装 numpy 和 scipy 才能使用卷积方法")

    size = 2 * radius + 1
    kernel = np.zeros((size, size), dtype=int)
    center = radius

    for i in range(size):
        for j in range(size):
            manhattan_distance = abs(i - center) + abs(j - center)
            if 0 < manhattan_distance <= radius:
                kernel[i, j] = 1

    return kernel


def get_moore_kernel(radius: int = 1):
    """
    获取 Moore 邻域的卷积核

    8邻域卷积核示例 (radius=1):
    ```
      [[1, 1, 1],
       [1, 0, 1],
       [1, 1, 1]]
    ```

    Args:
        radius: 邻域半径

    Returns:
        卷积核数组
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("需要安装 numpy 和 scipy 才能使用卷积方法")

    size = 2 * radius + 1
    kernel = np.ones((size, size), dtype=int)
    kernel[radius, radius] = 0  # 中心点不算邻居
    return kernel


def get_extended_kernel(radius: int = 2):
    """
    获取扩展邻域的卷积核（24邻域）

    Args:
        radius: 邻域半径，默认为2

    Returns:
        卷积核数组
    """
    return get_moore_kernel(radius)


def get_neighborhood_kernel(neighborhood_type: NeighborhoodType, radius: int = 1):
    """
    根据邻域类型获取相应的卷积核

    Args:
        neighborhood_type: 邻域类型
        radius: 邻域半径

    Returns:
        卷积核数组
    """
    if neighborhood_type == NeighborhoodType.VON_NEUMANN:
        return get_von_neumann_kernel(radius)
    elif neighborhood_type == NeighborhoodType.MOORE:
        return get_moore_kernel(radius)
    elif neighborhood_type == NeighborhoodType.EXTENDED:
        return get_extended_kernel(radius if radius > 1 else 2)
    else:
        raise ValueError(f"Unknown neighborhood type: {neighborhood_type}")


def count_neighbors_convolution(
    grid,
    neighborhood_type: NeighborhoodType = NeighborhoodType.MOORE,
    radius: int = 1,
    boundary: str = "wrap",
):
    """
    使用卷积方法快速计算每个位置的邻居数量

    这是性能优化版本，适合大规模网格

    Args:
        grid: 二维网格，1表示有智能体，0表示空
        neighborhood_type: 邻域类型
        radius: 邻域半径
        boundary: 边界条件 ('wrap'=周期性, 'fill'=固定值)

    Returns:
        邻居数量的二维数组

    Example:
        >>> grid = np.array([[1, 0, 1],
        ...                   [0, 1, 0],
        ...                   [1, 0, 1]])
        >>> count_neighbors_convolution(grid, NeighborhoodType.MOORE, 1)
        # 返回每个位置周围8邻域中的邻居数量
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("需要安装 numpy 和 scipy 才能使用卷积方法")

    kernel = get_neighborhood_kernel(neighborhood_type, radius)

    if boundary == "wrap":
        # 周期性边界条件
        neighbor_count = signal.convolve2d(grid, kernel, mode="same", boundary="wrap")
    else:
        # 固定值边界条件
        neighbor_count = signal.convolve2d(
            grid, kernel, mode="same", boundary="fill", fillvalue=0
        )

    return neighbor_count.astype(int)


def count_similar_neighbors_convolution(
    grid,
    agent_types,
    neighborhood_type: NeighborhoodType = NeighborhoodType.MOORE,
    radius: int = 1,
    boundary: str = "wrap",
):
    """
    使用卷积方法快速计算每个位置的相似邻居数量

    Args:
        grid: 二维网格，1表示有智能体，0表示空
        agent_types: 智能体类型网格（0或1），空位置用-1表示
        neighborhood_type: 邻域类型
        radius: 邻域半径
        boundary: 边界条件

    Returns:
        相似邻居数量的二维数组
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("需要安装 numpy 和 scipy 才能使用卷积方法")

    kernel = get_neighborhood_kernel(neighborhood_type, radius)

    # 为每种类型计算邻居数量
    type0_mask = (agent_types == 0).astype(int)
    type1_mask = (agent_types == 1).astype(int)

    if boundary == "wrap":
        type0_neighbors = signal.convolve2d(
            type0_mask, kernel, mode="same", boundary="wrap"
        )
        type1_neighbors = signal.convolve2d(
            type1_mask, kernel, mode="same", boundary="wrap"
        )
    else:
        type0_neighbors = signal.convolve2d(
            type0_mask, kernel, mode="same", boundary="fill", fillvalue=0
        )
        type1_neighbors = signal.convolve2d(
            type1_mask, kernel, mode="same", boundary="fill", fillvalue=0
        )

    # 创建结果数组：对于type=0的智能体，统计type0邻居；对于type=1的智能体，统计type1邻居
    similar_neighbors = np.where(agent_types == 0, type0_neighbors, 0) + np.where(
        agent_types == 1, type1_neighbors, 0
    )

    return similar_neighbors.astype(int)


# ============================================================================
# 工具函数
# ============================================================================


def get_neighborhood_size(neighborhood_type: NeighborhoodType, radius: int = 1) -> int:
    """
    获取邻域大小（最大邻居数量）

    Args:
        neighborhood_type: 邻域类型
        radius: 邻域半径

    Returns:
        邻域大小
    """
    return len(get_neighborhood_offsets(neighborhood_type, radius))


def visualize_neighborhood(
    neighborhood_type: NeighborhoodType, radius: int = 1
) -> None:
    """
    可视化邻域结构（用于教学）

    Args:
        neighborhood_type: 邻域类型
        radius: 邻域半径
    """
    kernel = get_neighborhood_kernel(neighborhood_type, radius)
    size = kernel.shape[0]
    center = size // 2

    print(f"\n{neighborhood_type.value.upper()} 邻域 (半径={radius})")
    print(f"邻居数量: {get_neighborhood_size(neighborhood_type, radius)}")
    print("\n可视化 (X=中心, 1=邻居, 0=非邻居):")

    for i in range(size):
        row_str = ""
        for j in range(size):
            if i == center and j == center:
                row_str += "X "
            else:
                row_str += f"{kernel[i, j]} "
        print(row_str)
    print()


# 预定义的邻域配置
NEIGHBORHOOD_4 = (NeighborhoodType.VON_NEUMANN, 1)  # 4邻域
NEIGHBORHOOD_8 = (NeighborhoodType.MOORE, 1)  # 8邻域
NEIGHBORHOOD_24 = (NeighborhoodType.EXTENDED, 2)  # 24邻域


# ============================================================================
# 测试和演示代码
# ============================================================================

if __name__ == "__main__":
    # 演示不同邻域类型
    print("=" * 60)
    print("邻域类型演示")
    print("=" * 60)

    for nh_type in NeighborhoodType:
        if nh_type == NeighborhoodType.EXTENDED:
            visualize_neighborhood(nh_type, radius=2)
        else:
            visualize_neighborhood(nh_type, radius=1)

    # 性能对比示例
    print("=" * 60)
    print("性能对比示例")
    print("=" * 60)

    # 创建一个测试网格
    test_grid_data = np.random.randint(0, 2, size=(10, 10))
    print("\n测试网格 (10x10):")
    print(test_grid_data)

    # 使用卷积方法计算邻居数量
    neighbor_counts = count_neighbors_convolution(
        test_grid_data, NeighborhoodType.MOORE, radius=1
    )
    print("\n每个位置的邻居数量 (8邻域):")
    print(neighbor_counts)
