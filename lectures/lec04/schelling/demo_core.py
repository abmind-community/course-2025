"""
核心功能演示（不依赖Mesa和Scipy）
展示邻域和效用函数的基本实现
"""

print("=" * 70)
print("Schelling 模型扩展功能演示")
print("=" * 70)

# ============================================================================
# 1. 邻域类型演示
# ============================================================================
print("\n【1】邻域类型演示")
print("-" * 70)

from neighborhoods import (
    NeighborhoodType,
    get_neighborhood_offsets,
)

print("\n4邻域 (Von Neumann):")
offsets_4 = get_neighborhood_offsets(NeighborhoodType.VON_NEUMANN, radius=1)
print(f"  邻居数量: {len(offsets_4)}")
print(f"  偏移量: {offsets_4}")

print("\n8邻域 (Moore):")
offsets_8 = get_neighborhood_offsets(NeighborhoodType.MOORE, radius=1)
print(f"  邻居数量: {len(offsets_8)}")
print(f"  偏移量: {offsets_8}")

print("\n24邻域 (Extended):")
offsets_24 = get_neighborhood_offsets(NeighborhoodType.EXTENDED, radius=2)
print(f"  邻居数量: {len(offsets_24)}")
print(f"  前8个偏移量: {offsets_24[:8]}...")

# ============================================================================
# 2. 效用函数演示（面向对象版本）
# ============================================================================
print("\n\n【2】效用函数演示 - 面向对象版本")
print("-" * 70)

from utility_classes import (
    ThresholdUtility,
    LinearUtility,
    QuadraticUtility,
    PeakedUtility,
    SigmoidUtility,
)

# 创建不同的效用函数
utilities = {
    "阈值效用 (threshold=0.375)": ThresholdUtility(threshold=0.375),
    "线性效用": LinearUtility(),
    "二次效用": QuadraticUtility(power=2),
    "峰值效用 (optimal=0.5)": PeakedUtility(optimal_fraction=0.5, tolerance=0.2),
    "Sigmoid效用": SigmoidUtility(threshold=0.5, steepness=10),
}

# 测试案例：8个邻居中有3个相似
similar_count = 3
total_count = 8
similarity = similar_count / total_count

print(f"\n测试场景: {similar_count}/{total_count} 相似邻居 (相似度={similarity:.2%})\n")

for name, utility in utilities.items():
    utility_value = utility.calculate(similar_count, total_count)
    print(f"{name:30s}: 效用值 = {utility_value:.3f}")

# ============================================================================
# 3. 效用函数对比
# ============================================================================
print("\n\n【3】效用函数对比表")
print("-" * 70)

from utility_classes import compare_utilities

utilities_list = [
    ThresholdUtility(threshold=0.375),
    LinearUtility(),
    QuadraticUtility(power=2),
    PeakedUtility(optimal_fraction=0.5, tolerance=0.2),
]

compare_utilities(utilities_list, total_neighbors=8)

# ============================================================================
# 4. 自定义效用函数示例
# ============================================================================
print("\n\n【4】自定义效用函数示例")
print("-" * 70)

from utility_classes import BaseUtility


class StrictDiversityUtility(BaseUtility):
    """严格多样性效用：只接受40%-60%的相似度"""

    def __init__(self):
        super().__init__()

    def calculate(self, similar_count: int, total_count: int) -> float:
        if total_count == 0:
            return 0.0
        similarity = similar_count / total_count
        if 0.4 <= similarity <= 0.6:
            return 1.0
        else:
            return 0.0


print("\n自定义效用函数：StrictDiversityUtility")
print("规则：只有在40%-60%相似度时才满意\n")

custom_utility = StrictDiversityUtility()

print("相似邻居数 | 总邻居数 | 相似度  | 效用值")
print("-" * 50)
for similar in range(0, 9):
    total = 8
    if similar > total:
        continue
    similarity = similar / total if total > 0 else 0
    utility_val = custom_utility.calculate(similar, total)
    print(
        f"     {similar:2d}      |    {total:2d}     | {similarity:5.2%}  | {utility_val:6.3f}"
    )

# ============================================================================
# 5. 函数式版本对比
# ============================================================================
print("\n\n【5】函数式版本对比")
print("-" * 70)

from utility_functions import threshold_utility, linear_utility, peaked_utility

print("\n函数式实现：")
print(
    f"threshold_utility(3, 8, {{'threshold': 0.375}}) = {threshold_utility(3, 8, {'threshold': 0.375}):.3f}"
)
print(f"linear_utility(3, 8, {{}}) = {linear_utility(3, 8, {}):.3f}")
print(
    f"peaked_utility(4, 8, {{'optimal_fraction': 0.5, 'tolerance': 0.2}}) = {peaked_utility(4, 8, {'optimal_fraction': 0.5, 'tolerance': 0.2}):.3f}"
)

print("\n面向对象实现：")
print(
    f"ThresholdUtility(0.375).calculate(3, 8) = {ThresholdUtility(0.375).calculate(3, 8):.3f}"
)
print(f"LinearUtility().calculate(3, 8) = {LinearUtility().calculate(3, 8):.3f}")
print(
    f"PeakedUtility(0.5, 0.2).calculate(4, 8) = {PeakedUtility(0.5, 0.2).calculate(4, 8):.3f}"
)

# ============================================================================
# 总结
# ============================================================================
print("\n\n" + "=" * 70)
print("核心功能演示完成！")
print("=" * 70)

print("\n📚 已实现的功能：")
print("  ✓ 三种邻域类型（4、8、24邻域）")
print("  ✓ 两种实现方法（偏移量、卷积）")
print("  ✓ 多种效用函数（阈值、线性、二次、峰值、Sigmoid）")
print("  ✓ 两种编程风格（函数式、面向对象）")
print("  ✓ 完全可扩展（支持自定义邻域和效用函数）")

print("\n📖 教学价值：")
print("  • 理解空间邻域对个体决策的影响")
print("  • 学习如何用效用函数建模偏好")
print("  • 对比函数式编程和面向对象编程")
print("  • 探索不同参数对群体行为的影响")

print("\n🎯 下一步：")
print("  1. 查看 examples.ipynb 了解如何在模型中使用这些功能")
print("  2. 查看 Readme.md 了解完整文档")
print("  3. 尝试创建自己的效用函数")
print("  4. 运行参数扫描实验，比较不同配置")
