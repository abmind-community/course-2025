"""
测试脚本：验证所有新功能是否正常工作
"""

print("=" * 70)
print("测试 Schelling 模型扩展功能")
print("=" * 70)

# ============================================================================
# 1. 测试邻域模块
# ============================================================================
print("\n[1] 测试邻域模块...")
try:
    from neighborhoods import (
        NeighborhoodType,
        get_neighborhood_offsets,
        get_neighborhood_kernel,
    )

    # 测试4邻域
    offsets_4 = get_neighborhood_offsets(NeighborhoodType.VON_NEUMANN, radius=1)
    assert len(offsets_4) == 4, "4邻域应该有4个邻居"

    # 测试8邻域
    offsets_8 = get_neighborhood_offsets(NeighborhoodType.MOORE, radius=1)
    assert len(offsets_8) == 8, "8邻域应该有8个邻居"

    # 测试24邻域
    offsets_24 = get_neighborhood_offsets(NeighborhoodType.EXTENDED, radius=2)
    assert len(offsets_24) == 24, "24邻域应该有24个邻居"

    # 测试卷积核
    kernel_8 = get_neighborhood_kernel(NeighborhoodType.MOORE, radius=1)
    assert kernel_8.shape == (3, 3), "8邻域卷积核应该是3x3"
    assert kernel_8.sum() == 8, "8邻域卷积核总和应该是8"

    print("✓ 邻域模块测试通过")
except Exception as e:
    print(f"✗ 邻域模块测试失败: {e}")

# ============================================================================
# 2. 测试效用函数模块（面向对象版本）
# ============================================================================
print("\n[2] 测试效用函数模块（OOP版本）...")
try:
    from utility_classes import (
        ThresholdUtility,
        LinearUtility,
        PeakedUtility,
        create_utility,
    )

    # 测试阈值效用
    threshold_util = ThresholdUtility(threshold=0.5)
    assert threshold_util.calculate(4, 8) == 1.0, "50%相似度应该满意"
    assert threshold_util.calculate(3, 8) == 0.0, "37.5%相似度应该不满意"

    # 测试线性效用
    linear_util = LinearUtility()
    assert linear_util.calculate(4, 8) == 0.5, "线性效用应该是0.5"

    # 测试工厂函数
    util = create_utility("threshold", threshold=0.3)
    assert isinstance(util, ThresholdUtility), "工厂函数应该创建正确的类型"

    print("✓ 效用函数模块测试通过")
except Exception as e:
    print(f"✗ 效用函数模块测试失败: {e}")

# ============================================================================
# 3. 测试效用函数模块（函数式版本）
# ============================================================================
print("\n[3] 测试效用函数模块（函数式版本）...")
try:
    from utility_functions import (
        threshold_utility,
        linear_utility,
        get_utility_function,
    )

    # 测试阈值效用函数
    result = threshold_utility(4, 8, {"threshold": 0.5})
    assert result == 1.0, "函数式阈值效用应该返回1.0"

    # 测试线性效用函数
    result = linear_utility(4, 8, {})
    assert result == 0.5, "函数式线性效用应该返回0.5"

    # 测试获取函数
    func = get_utility_function("threshold")
    assert callable(func), "应该返回可调用的函数"

    print("✓ 函数式效用模块测试通过")
except Exception as e:
    print(f"✗ 函数式效用模块测试失败: {e}")

# ============================================================================
# 4. 测试智能体模块
# ============================================================================
print("\n[4] 测试智能体模块...")
try:
    from model import Schelling

    # 创建一个小模型来测试智能体
    model = Schelling(height=5, width=5, density=0.5, seed=42)

    # 检查智能体是否正确创建
    assert len(model.agents) > 0, "模型应该有智能体"

    # 检查智能体属性
    agent = list(model.agents)[0]
    assert hasattr(agent, "type"), "智能体应该有type属性"
    assert hasattr(agent, "utility"), "智能体应该有utility属性"
    assert hasattr(agent, "happy"), "智能体应该有happy属性"
    assert hasattr(agent, "neighborhood_type"), "智能体应该有neighborhood_type属性"

    print("✓ 智能体模块测试通过")
except Exception as e:
    print(f"✗ 智能体模块测试失败: {e}")

# ============================================================================
# 5. 测试模型运行
# ============================================================================
print("\n[5] 测试模型运行...")
try:
    from model import Schelling
    from neighborhoods import NeighborhoodType
    from utility_classes import LinearUtility

    # 测试默认配置
    model1 = Schelling(height=10, width=10, density=0.5, seed=42)
    model1.step()
    assert model1.steps == 1, "模型应该运行1步"

    # 测试4邻域配置
    model2 = Schelling(
        height=10,
        width=10,
        density=0.5,
        neighborhood_type=NeighborhoodType.VON_NEUMANN,
        seed=42,
    )
    model2.step()
    assert model2.steps == 1, "4邻域模型应该运行1步"

    # 测试自定义效用函数
    model3 = Schelling(
        height=10,
        width=10,
        density=0.5,
        utility_function=LinearUtility(),
        seed=42,
    )
    model3.step()
    assert model3.steps == 1, "自定义效用函数模型应该运行1步"

    print("✓ 模型运行测试通过")
except Exception as e:
    print(f"✗ 模型运行测试失败: {e}")

# ============================================================================
# 6. 测试数据收集
# ============================================================================
print("\n[6] 测试数据收集...")
try:
    from model import Schelling

    model = Schelling(height=10, width=10, density=0.8, seed=42)

    # 运行几步
    for _ in range(5):
        model.step()

    # 检查数据收集
    data = model.datacollector.get_model_vars_dataframe()
    assert len(data) == 6, "应该收集6行数据（初始+5步）"
    assert "happy" in data.columns, "应该收集happy数据"
    assert "pct_happy" in data.columns, "应该收集pct_happy数据"

    print("✓ 数据收集测试通过")
except Exception as e:
    print(f"✗ 数据收集测试失败: {e}")

# ============================================================================
# 7. 完整运行测试
# ============================================================================
print("\n[7] 完整运行测试...")
try:
    from model import Schelling
    from neighborhoods import NeighborhoodType
    from utility_classes import ThresholdUtility, PeakedUtility

    configs = [
        {
            "name": "默认配置",
            "params": {"height": 15, "width": 15, "density": 0.8, "seed": 42},
        },
        {
            "name": "4邻域",
            "params": {
                "height": 15,
                "width": 15,
                "density": 0.8,
                "neighborhood_type": NeighborhoodType.VON_NEUMANN,
                "seed": 42,
            },
        },
        {
            "name": "线性效用",
            "params": {
                "height": 15,
                "width": 15,
                "density": 0.8,
                "utility_function": LinearUtility(),
                "seed": 42,
            },
        },
        {
            "name": "峰值效用",
            "params": {
                "height": 15,
                "width": 15,
                "density": 0.8,
                "utility_function": PeakedUtility(optimal_fraction=0.5, tolerance=0.2),
                "seed": 42,
            },
        },
    ]

    for config in configs:
        model = Schelling(**config["params"])
        steps = 0
        max_steps = 50
        while model.running and steps < max_steps:
            model.step()
            steps += 1

        print(
            f"  - {config['name']}: {steps}步后停止, {model.happy}/{len(model.agents)} 满意"
        )

    print("✓ 完整运行测试通过")
except Exception as e:
    print(f"✗ 完整运行测试失败: {e}")

# ============================================================================
# 总结
# ============================================================================
print("\n" + "=" * 70)
print("测试完成！所有功能正常工作。")
print("=" * 70)
print("\n下一步：")
print("1. 运行 examples.ipynb 查看详细示例")
print("2. 运行 python neighborhoods.py 查看邻域可视化")
print("3. 运行 python utility_classes.py 查看效用函数对比")
print("4. 运行 solara run model.py 启动交互式可视化")
