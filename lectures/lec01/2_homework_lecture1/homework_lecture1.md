
# Mesa ABM 作业: MoneyModel

# Instructions

下载查看 `2_homework_lecture1` 文件夹，基于作业要求修改 `app.py`, `model.py`,`app.py` 完成对应练习。


提交：完成后，请将作业提交到 xx 仓库位置。

阅读材料：您可能发现以下参考资料很有用：

- `2_homework_lecture1` 文件夹中的 `moneymodel_tutorial.md` （对作业例子代码说明）
- `2_homework_lecture1` 文件夹中的快速上手的 `money_model.ipynb` （用于一键运行了解整个项目内容，但作业不是用这个做）
- mesa 官方的 moneyagent 模型：https://mesa.readthedocs.io/stable/tutorials/0_first_model.html

提示：
- 鼓励你将学习mesa的过程以博客的形式记录下来，有助于 mesa, abm 建模方法的推广应用

---

# 必答题

## Q1. Agent 属性拓展

* **要求：** 
	* 将现有的单一属性 Agent 拓展为一个持有**两种颜色属性**的 Agent。
    * Agent 必须新增一个或多个属性来记录其**颜色阵营**（例如，'Red' / 'Blue'）
    * 设置一个系数控制初始颜色的比例，默认红色 agent 占比为 30%

## Q2. agent 交互行为拓展

* **要求：** 
	* 拓展 Agent 的 $\texttt{step()}$ 方法，实现基于**颜色同质性**的财富分配规则。
    * 在传统的随机财富转移之外，Agent 必须检查其**相邻的 Agent**。
    * 如果相邻 Agent 与自身颜色不同，这两个 Agent 之间应进行固定的财富分配（例如，每个 Agent 分配/增加 0.5 个财富单位给对方，或者按规则交换）。


## Q3. 数据收集拓展

* **要求：** 
	* 利用 $\texttt{DataCollector}$ 收集 Agent 的**颜色属性**数据。
	* 类似于compute_gini的方法，统计不同颜色的 agent 财富总和
	* 分别统计运行过程中每个 agent 的财富、颜色

## Q4. 可视化交互操作

* **要求：** 
	* 为模型的初始化参数增加滑轨（Slider）控件，特别是用于控制**两种颜色阵营 Agent 的初始比例
	* 在可视化界面增加为不同颜色 agent 渲染的功能，使agent根据自己属性颜色来显示
	* 在 page 2 ，类似于计算 gini 系数一样，分别添加计算红色 和蓝色 agent 财富总和随时间变化的可视化图

## Q5.  参数变化观察（Sensitivity Analysis）

* **要求：** 
	* 设计一系列实验，观察当**网格大小**、**Agent 总数**以及 之前定义的财富分配数值发生变化时，模型结果如何变化。

举个例子：
类似于设置参数变化分析表格：

|        网格数量         | `10*10` | `50*50` | `100*100` |
| :-----------------: | :-----: | ------- | --------- |
| gini 系数 30 步长时刻对应数值 |         |         |           |

|       agent总数       | 50  | 10  | 100 |
| :-----------------: | :-: | --- | --- |
| gini 系数 30 步长时刻对应数值 |     |     |     |

## Q6. 结果保存（Data Persistence）

* **要求：** 
	* 学会保存 $\texttt{DataCollector}$ 的结果。
    * 在运行脚本中，实现循环运行模型 $100$ 次。
    * 将**每次运行**的`model`级和 `Agent` 级数据转换为 Pandas $\texttt{DataFrame}$。
    * 最终将数据以 **CSV 文件格式**保存到本地并提交。


# 如何提交？

