"""
效用函数模块 - 函数式版本
定义不同的效用函数来表示智能体的偏好 (函数式编程风格)

这是简化版本，适合快速原型和简单场景
如需更复杂的功能，请参考 utility_classes.py
"""

from typing import Callable, Dict, Any
import numpy as np


# ============================================================================
# 效用函数类型定义
# ============================================================================

UtilityFunction = Callable[[int, int, Dict[str, Any]], float]
"""
效用函数类型定义

Args:
    similar_count: 相似邻居数量
    total_count: 总邻居数量
    params: 额外参数字典

Returns:
    效用值 (通常在0-1之间)
"""


# ============================================================================
# 预定义的效用函数
# ============================================================================


def threshold_utility(
    similar_count: int, total_count: int, params: Dict[str, Any]
) -> float:
    """
    阈值效用函数（原始Schelling模型）

    智能体需要至少 threshold 比例的相似邻居才满意
    - 如果相似度 >= threshold: 效用 = 1 (满意)
    - 如果相似度 < threshold: 效用 = 0 (不满意)

    Args:
        similar_count: 相似邻居数量
        total_count: 总邻居数量
        params: 必须包含 'threshold' (0-1之间的浮点数)

    Returns:
        效用值: 0 或 1

    Example:
        >>> threshold_utility(3, 8, {'threshold': 0.3})
        1.0  # 3/8 = 0.375 >= 0.3, 满意
        >>> threshold_utility(2, 8, {'threshold': 0.3})
        0.0  # 2/8 = 0.25 < 0.3, 不满意
    """
    threshold = params.get("threshold", 0.3)

    if total_count == 0:
        return 0.0

    similarity_fraction = similar_count / total_count
    return 1.0 if similarity_fraction >= threshold else 0.0


def linear_utility(
    similar_count: int, total_count: int, params: Dict[str, Any]
) -> float:
    """
    线性效用函数

    效用随相似邻居比例线性增长
    utility = similarity_fraction

    Args:
        similar_count: 相似邻居数量
        total_count: 总邻居数量
        params: 可选参数（此函数不使用）

    Returns:
        效用值: 0 到 1 之间

    Example:
        >>> linear_utility(3, 8, {})
        0.375  # 3/8
    """
    if total_count == 0:
        return 0.0

    return similar_count / total_count


def quadratic_utility(
    similar_count: int, total_count: int, params: Dict[str, Any]
) -> float:
    """
    二次效用函数

    效用随相似邻居比例二次增长，更偏好高相似度
    utility = (similarity_fraction)^2

    Args:
        similar_count: 相似邻居数量
        total_count: 总邻居数量
        params: 可选参数（此函数不使用）

    Returns:
        效用值: 0 到 1 之间

    Example:
        >>> quadratic_utility(4, 8, {})
        0.25  # (4/8)^2 = 0.5^2 = 0.25
    """
    if total_count == 0:
        return 0.0

    similarity_fraction = similar_count / total_count
    return similarity_fraction**2


def peaked_utility(
    similar_count: int, total_count: int, params: Dict[str, Any]
) -> float:
    """
    峰值效用函数

    智能体偏好中等程度的多样性，在 optimal_fraction 处效用最大
    使用高斯分布形式

    Args:
        similar_count: 相似邻居数量
        total_count: 总邻居数量
        params: 必须包含 'optimal_fraction' (最优相似度) 和 'tolerance' (容忍度)

    Returns:
        效用值: 0 到 1 之间

    Example:
        >>> peaked_utility(4, 8, {'optimal_fraction': 0.5, 'tolerance': 0.2})
        1.0  # 4/8 = 0.5，正好在最优点
    """
    optimal_fraction = params.get("optimal_fraction", 0.5)
    tolerance = params.get("tolerance", 0.2)

    if total_count == 0:
        return 0.0

    similarity_fraction = similar_count / total_count
    deviation = abs(similarity_fraction - optimal_fraction)

    # 高斯形式: exp(-(deviation^2) / (2 * tolerance^2))
    utility = np.exp(-((deviation**2) / (2 * tolerance**2)))
    return float(utility)


def sigmoid_utility(
    similar_count: int, total_count: int, params: Dict[str, Any]
) -> float:
    """
    Sigmoid 效用函数

    S形曲线，在阈值附近快速变化
    utility = 1 / (1 + exp(-steepness * (similarity_fraction - threshold)))

    Args:
        similar_count: 相似邻居数量
        total_count: 总邻居数量
        params: 可选，包含 'threshold' 和 'steepness'

    Returns:
        效用值: 0 到 1 之间

    Example:
        >>> sigmoid_utility(4, 8, {'threshold': 0.5, 'steepness': 10})
        0.5  # 在阈值处
    """
    threshold = params.get("threshold", 0.5)
    steepness = params.get("steepness", 10)

    if total_count == 0:
        return 0.0

    similarity_fraction = similar_count / total_count

    # Sigmoid函数
    utility = 1 / (1 + np.exp(-steepness * (similarity_fraction - threshold)))

    return float(utility)


# ============================================================================
# 效用函数注册表
# ============================================================================

UTILITY_FUNCTIONS: Dict[str, UtilityFunction] = {
    "threshold": threshold_utility,
    "linear": linear_utility,
    "quadratic": quadratic_utility,
    "peaked": peaked_utility,
    "sigmoid": sigmoid_utility,
}


def get_utility_function(name: str) -> UtilityFunction:
    """
    根据名称获取效用函数

    Args:
        name: 效用函数名称

    Returns:
        效用函数

    Raises:
        ValueError: 如果函数名称未找到
    """
    if name not in UTILITY_FUNCTIONS:
        raise ValueError(
            f"Unknown utility function: {name}. "
            f"Available: {list(UTILITY_FUNCTIONS.keys())}"
        )
    return UTILITY_FUNCTIONS[name]


def register_utility_function(name: str, func: UtilityFunction) -> None:
    """
    注册自定义效用函数

    Args:
        name: 函数名称
        func: 效用函数

    Example:
        >>> def my_utility(similar, total, params):
        ...     return similar / total if total > 0 else 0
        >>> register_utility_function('my_custom', my_utility)
    """
    UTILITY_FUNCTIONS[name] = func


# ============================================================================
# 可视化和分析工具
# ============================================================================


def visualize_utility_function(
    utility_name: str, params: Dict[str, Any], max_neighbors: int = 8
) -> None:
    """
    可视化效用函数（用于教学）

    Args:
        utility_name: 效用函数名称
        params: 效用函数参数
        max_neighbors: 最大邻居数量
    """
    utility_func = get_utility_function(utility_name)

    print(f"\n效用函数: {utility_name}")
    print(f"参数: {params}")
    print("\n相似邻居数 | 总邻居数 | 相似度 | 效用值")
    print("-" * 50)

    for total in range(1, max_neighbors + 1):
        for similar in range(0, total + 1):
            similarity_fraction = similar / total
            utility = utility_func(similar, total, params)
            print(
                f"     {similar:2d}      |    {total:2d}     | {similarity_fraction:5.2f}  | {utility:6.3f}"
            )


if __name__ == "__main__":
    print("=" * 60)
    print("效用函数演示 - 函数式版本")
    print("=" * 60)

    # 演示阈值效用函数
    visualize_utility_function("threshold", {"threshold": 0.375}, max_neighbors=8)
