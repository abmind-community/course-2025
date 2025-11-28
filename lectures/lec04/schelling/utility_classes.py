"""
效用函数模块 - 面向对象版本
使用类来实现效用函数，提供更好的封装和扩展性

这是推荐版本，适合教学和复杂场景
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


# ============================================================================
# 基类定义
# ============================================================================


class BaseUtility(ABC):
    """
    效用函数基类

    所有效用函数都应该继承这个基类并实现 calculate 方法
    """

    def __init__(self, name: Optional[str] = None):
        """
        初始化效用函数

        Args:
            name: 效用函数名称（可选）
        """
        self.name = name or self.__class__.__name__

    @abstractmethod
    def calculate(self, similar_count: int, total_count: int) -> float:
        """
        计算效用值

        Args:
            similar_count: 相似邻居数量
            total_count: 总邻居数量

        Returns:
            效用值 (通常在0-1之间)
        """
        pass

    def __call__(self, similar_count: int, total_count: int) -> float:
        """
        使效用函数对象可调用

        Example:
            >>> utility = ThresholdUtility(0.3)
            >>> utility(3, 8)  # 等价于 utility.calculate(3, 8)
        """
        return self.calculate(similar_count, total_count)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


# ============================================================================
# 具体效用函数类
# ============================================================================


class ThresholdUtility(BaseUtility):
    """
    阈值效用函数（原始Schelling模型）

    智能体需要至少 threshold 比例的相似邻居才满意
    - 如果相似度 >= threshold: 效用 = 1 (满意)
    - 如果相似度 < threshold: 效用 = 0 (不满意)

    Example:
        >>> utility = ThresholdUtility(threshold=0.3)
        >>> utility.calculate(3, 8)
        1.0  # 3/8 = 0.375 >= 0.3
    """

    def __init__(self, threshold: float = 0.3):
        """
        Args:
            threshold: 满意所需的最小相似邻居比例 (0-1之间)
        """
        super().__init__()
        if not 0 <= threshold <= 1:
            raise ValueError(f"threshold 必须在0-1之间，当前值: {threshold}")
        self.threshold = threshold

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0

        similarity_fraction = similar_count / total_count
        return 1.0 if similarity_fraction >= self.threshold else 0.0

    def __repr__(self) -> str:
        return f"ThresholdUtility(threshold={self.threshold})"


class LinearUtility(BaseUtility):
    """
    线性效用函数

    效用随相似邻居比例线性增长
    utility = similarity_fraction

    Example:
        >>> utility = LinearUtility()
        >>> utility.calculate(3, 8)
        0.375  # 3/8
    """

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0
        return similar_count / total_count


class QuadraticUtility(BaseUtility):
    """
    二次效用函数

    效用随相似邻居比例二次增长，更偏好高相似度
    utility = (similarity_fraction)^power

    Example:
        >>> utility = QuadraticUtility(power=2)
        >>> utility.calculate(4, 8)
        0.25  # (4/8)^2 = 0.25
    """

    def __init__(self, power: float = 2.0):
        """
        Args:
            power: 幂次，默认为2（二次）
        """
        super().__init__()
        if power < 0:
            raise ValueError(f"power 必须为非负数，当前值: {power}")
        self.power = power

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0
        similarity_fraction = similar_count / total_count
        return similarity_fraction**self.power

    def __repr__(self) -> str:
        return f"QuadraticUtility(power={self.power})"


class PeakedUtility(BaseUtility):
    """
    峰值效用函数

    智能体偏好中等程度的多样性，在 optimal_fraction 处效用最大
    使用高斯分布形式

    Example:
        >>> utility = PeakedUtility(optimal_fraction=0.5, tolerance=0.2)
        >>> utility.calculate(4, 8)
        1.0  # 4/8 = 0.5，正好在最优点
    """

    def __init__(self, optimal_fraction: float = 0.5, tolerance: float = 0.2):
        """
        Args:
            optimal_fraction: 最优相似度比例 (0-1之间)
            tolerance: 容忍度，值越大曲线越平坦
        """
        super().__init__()
        if not 0 <= optimal_fraction <= 1:
            raise ValueError(
                f"optimal_fraction 必须在0-1之间，当前值: {optimal_fraction}"
            )
        if tolerance <= 0:
            raise ValueError(f"tolerance 必须为正数，当前值: {tolerance}")

        self.optimal_fraction = optimal_fraction
        self.tolerance = tolerance

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0

        similarity_fraction = similar_count / total_count
        deviation = abs(similarity_fraction - self.optimal_fraction)

        # 高斯形式: exp(-(deviation^2) / (2 * tolerance^2))
        utility = np.exp(-((deviation**2) / (2 * self.tolerance**2)))
        return float(utility)

    def __repr__(self) -> str:
        return (
            f"PeakedUtility(optimal_fraction={self.optimal_fraction}, "
            f"tolerance={self.tolerance})"
        )


class StepUtility(BaseUtility):
    """
    阶梯效用函数

    根据相似度区间给予不同的效用值
    - [0, low_threshold): 低效用
    - [low_threshold, high_threshold): 中效用
    - [high_threshold, 1]: 高效用

    Example:
        >>> utility = StepUtility(low_threshold=0.3, high_threshold=0.7)
        >>> utility.calculate(2, 8)
        0.0  # 2/8 = 0.25 < 0.3
    """

    def __init__(
        self,
        low_threshold: float = 0.3,
        high_threshold: float = 0.7,
        low_utility: float = 0.0,
        mid_utility: float = 0.5,
        high_utility: float = 1.0,
    ):
        """
        Args:
            low_threshold: 低阈值
            high_threshold: 高阈值
            low_utility: 低区间效用值
            mid_utility: 中区间效用值
            high_utility: 高区间效用值
        """
        super().__init__()
        if not 0 <= low_threshold <= high_threshold <= 1:
            raise ValueError("必须满足 0 <= low_threshold <= high_threshold <= 1")

        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.low_utility = low_utility
        self.mid_utility = mid_utility
        self.high_utility = high_utility

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return self.low_utility

        similarity_fraction = similar_count / total_count

        if similarity_fraction < self.low_threshold:
            return self.low_utility
        elif similarity_fraction < self.high_threshold:
            return self.mid_utility
        else:
            return self.high_utility

    def __repr__(self) -> str:
        return (
            f"StepUtility(low_threshold={self.low_threshold}, "
            f"high_threshold={self.high_threshold})"
        )


class ExponentialUtility(BaseUtility):
    """
    指数效用函数

    效用随相似度指数增长，强烈偏好高相似度
    utility = (exp(steepness * similarity_fraction) - 1) / (exp(steepness) - 1)

    Example:
        >>> utility = ExponentialUtility(steepness=2)
        >>> utility.calculate(8, 8)
        # 接近 1.0
    """

    def __init__(self, steepness: float = 2.0):
        """
        Args:
            steepness: 陡度参数，值越大曲线越陡
        """
        super().__init__()
        if steepness <= 0:
            raise ValueError(f"steepness 必须为正数，当前值: {steepness}")
        self.steepness = steepness

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0

        similarity_fraction = similar_count / total_count

        # 归一化的指数函数
        max_utility = np.exp(self.steepness) - 1
        utility = (np.exp(self.steepness * similarity_fraction) - 1) / max_utility

        return float(utility)

    def __repr__(self) -> str:
        return f"ExponentialUtility(steepness={self.steepness})"


class SigmoidUtility(BaseUtility):
    """
    Sigmoid 效用函数

    S形曲线，在阈值附近快速变化
    utility = 1 / (1 + exp(-steepness * (similarity_fraction - threshold)))

    Example:
        >>> utility = SigmoidUtility(threshold=0.5, steepness=10)
        >>> utility.calculate(4, 8)
        0.5  # 在阈值处
    """

    def __init__(self, threshold: float = 0.5, steepness: float = 10.0):
        """
        Args:
            threshold: 中心点（拐点）位置
            steepness: 陡度参数，值越大变化越快
        """
        super().__init__()
        if not 0 <= threshold <= 1:
            raise ValueError(f"threshold 必须在0-1之间，当前值: {threshold}")
        if steepness <= 0:
            raise ValueError(f"steepness 必须为正数，当前值: {steepness}")

        self.threshold = threshold
        self.steepness = steepness

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0

        similarity_fraction = similar_count / total_count

        # Sigmoid函数
        utility = 1 / (
            1 + np.exp(-self.steepness * (similarity_fraction - self.threshold))
        )

        return float(utility)

    def __repr__(self) -> str:
        return f"SigmoidUtility(threshold={self.threshold}, steepness={self.steepness})"


# ============================================================================
# 工具函数
# ============================================================================


def create_utility(utility_type: str, **kwargs) -> BaseUtility:
    """
    工厂函数：根据类型创建效用函数对象

    Args:
        utility_type: 效用函数类型名称
        **kwargs: 传递给效用函数构造函数的参数

    Returns:
        效用函数对象

    Example:
        >>> utility = create_utility('threshold', threshold=0.3)
        >>> utility.calculate(3, 8)
    """
    utility_classes = {
        "threshold": ThresholdUtility,
        "linear": LinearUtility,
        "quadratic": QuadraticUtility,
        "peaked": PeakedUtility,
        "step": StepUtility,
        "exponential": ExponentialUtility,
        "sigmoid": SigmoidUtility,
    }

    if utility_type not in utility_classes:
        raise ValueError(
            f"Unknown utility type: {utility_type}. "
            f"Available: {list(utility_classes.keys())}"
        )

    return utility_classes[utility_type](**kwargs)


def visualize_utility(utility: BaseUtility, max_neighbors: int = 8) -> None:
    """
    可视化效用函数（用于教学）

    Args:
        utility: 效用函数对象
        max_neighbors: 最大邻居数量
    """
    print(f"\n效用函数: {utility}")
    print("\n相似邻居数 | 总邻居数 | 相似度 | 效用值")
    print("-" * 50)

    for total in range(1, max_neighbors + 1):
        for similar in range(0, total + 1):
            similarity_fraction = similar / total
            utility_value = utility.calculate(similar, total)
            print(
                f"     {similar:2d}      |    {total:2d}     | {similarity_fraction:5.2f}  | {utility_value:6.3f}"
            )


def compare_utilities(utilities: list[BaseUtility], total_neighbors: int = 8) -> None:
    """
    比较多个效用函数

    Args:
        utilities: 效用函数对象列表
        total_neighbors: 总邻居数量
    """
    print(f"\n效用函数比较 (总邻居数={total_neighbors})")
    print("\n相似邻居数 |", end="")
    for utility in utilities:
        name = utility.__class__.__name__.replace("Utility", "")
        print(f" {name:>10s} |", end="")
    print()
    print("-" * (15 + 13 * len(utilities)))

    for similar in range(0, total_neighbors + 1):
        print(f"     {similar:2d}      |", end="")
        for utility in utilities:
            utility_value = utility.calculate(similar, total_neighbors)
            print(f"   {utility_value:6.3f}  |", end="")
        print()


# ============================================================================
# 测试和演示代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("效用函数演示 - 面向对象版本")
    print("=" * 60)

    # 创建不同的效用函数对象
    utilities = [
        ThresholdUtility(threshold=0.375),
        LinearUtility(),
        QuadraticUtility(power=2),
        SigmoidUtility(threshold=0.5, steepness=10),
        PeakedUtility(optimal_fraction=0.5, tolerance=0.2),
    ]

    # 比较它们
    compare_utilities(utilities, total_neighbors=8)

    print("\n" + "=" * 60)
    print("详细查看阈值效用函数")
    print("=" * 60)
    visualize_utility(ThresholdUtility(threshold=0.375), max_neighbors=8)
