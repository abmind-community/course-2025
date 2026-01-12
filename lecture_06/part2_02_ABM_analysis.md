> [!warning]
>
> 每个 ABM 研究的设计都千差万别，本文不教授如何对具体的模型进行编程，我们假设用户已经有了一个初步地建模思路，想用 Python 实现该模型并进行研究，或者想复现某个经典的模型实验。

在进行多主体模型研究时，设计好模型通常仅仅是开启了 ABM 研究的第一步。为了方便用户做一个健壮的多主体模型并利用它进行严谨的学术研究，我们建议建模者使用以下流程推进编程实施，每个阶段都有各自技术实现重点：

| 阶段          | 关注重点 | 技术栈            |
| ----------- | ---- | -------------- |
| [[#模型实现阶段]] | 程序跑通 | 日志查看、迅速作图、行为测试 |
| [[#参数实验阶段]] | 找到涌现 | 参数敏感性分析、模型行为监测 |
| [[#结果分析阶段]] | 写故事线 | 重复实验、情景对照、最终作图 |

> [!tip]
>
> 本文以仓库 `fire_forest/` 的森林火灾模型为例：模型代码在 `fire_forest/model.py`，命令行入口在 `fire_forest/__main__.py`，配置在 `configs/`，可视化在 `fire_forest/app.py`，分析脚本在 `analysis.ipynb`。

## 快速开始（给新手的一条跑通路径）

如果你第一次接触这类工程结构，建议先按下面顺序把“单次运行 → 批量实验 → 汇总分析”跑通一遍，再回来读每一段原理。

1) 安装依赖（推荐用 `uv`）：

```bash
uv sync
```

2) 单次运行（使用 `configs/config.yaml`，适合检查模型是否能跑、行为是否正确）：

```bash
uv run python -m fire_forest
```

3) 网页动态可视化（适合肉眼检查火焰传播过程是否符合直觉）：

```bash
solara run fire_forest/app.py
```

4) 批量实验（用 Hydra multirun 扫参数，产出大量结果到 `out/`）：

```bash
uv run python -m fire_forest --multirun exp=exp
```

> [!note]
>
> - 快速测试建议用 `exp=test`（更少重复/更少进程/不落盘），正式实验再用 `exp=exp`。
> - 若你开启了 `tracker: aim`（`configs/tracker/aim.yaml`，默认已启用），关键指标会被自动记录。

## 模型实现阶段

### 利用可视化

> [!tip]
>
> 本阶段的重点是快速实现一个可以如期望运行的 ABM 原始模型，它可以很简单，但必须让你有足够的信心在其基础上进行数字实验。

以[森林火灾模型](https://www.netlogoweb.org/launch#https://www.netlogoweb.org/assets/modelslib/Sample%20Models/Earth%20Science/Fire.nlogox)为例，假设用户已经基本实现了一个 Python 版本的模型。确定其实施是否靠谱的过程中要针对关键变量迅速作图，以确定模型按预期行为进行执行。推荐在笔记本里进行交互式展示输出。可视化能极大降低 debug 成本，碰到有疑惑的地方立刻加入新的日志并重跑单次模型。

> [!example]
>
> 例如，单次跑通后直接画出 `tree_state` 的栅格图（这个属性在 `Tree` 上被 `@raster_attribute` 标记，可以“一行出图”）。

当完成一个阶段后，也要进行动态可视化，如 `app.py` 中展示的，启动网页可视化，看看整个单次模型运行的过程是不是有问题。

### 日志记录

如果碰到问题，用户应该在自己的代码里加入适当的日志进行追踪：

```python
import logging

# A logger for this file
log = logging.getLogger(__name__)

log.debug("方便纠错的信息")
log.info("重要的信息")
log.warning("警告!可能产生非预期行为")
log.critical("错误，影响程序正常运行")
```

这样的日志不需要任何配置，便可以默认地**将 info 即以上等级的信息输出到控制台和后台日志文件**，这是 `ABSESpy` 和 `hydra` 共同实现的便捷功能。如果用户仍然想自己配置各类日志的输出等级与格式，可以参考以下配置的 schema：

```yaml
log:
  # Logging mode for repeated runs: once | separate | merge
  mode: str                # "once" | "separate" | "merge"

  # Experiment-level logging (progress, high-level summary)
  exp:
    stdout:
      enabled: bool        # Enable experiment logs to console
      level: str           # e.g. "INFO", "DEBUG"
      format: str          # Log format string
      datefmt: str         # Time format
    file:
      enabled: bool        # Enable experiment log file
      level: str           # File log level
      format: str          # File log format
      datefmt: str         # File time format

  # Run-level logging (each model execution)
  run:
    stdout:
      enabled: bool        # Enable per-run logs to console
      level: str
      format: str
      datefmt: str
    file:
      enabled: bool        # Enable per-run log files
      level: str
      format: str
      datefmt: str
      name: str            # Base log file name (without extension)
      rotation: str | null # e.g. "1 day", "100 MB", null = no rotation
      retention: str | null# e.g. "10 days", null = default policy
    mesa:
      level: str | null    # If null, uses run.file.level
      format: str | null   # If null, uses run.file.format
```

`ABSESpy` 本就是为了快速进行多主体模型实验而设计的包，能够帮助用户方便分离配置与代码。建议从一开始就区分配置与代码，追踪重要的指标属性、变量。

开发的时候，可以使用 debug 级别的日志，并设置 `hydra.verbose=true`，在输出里看到更完整的配置与运行信息：

```zsh
uv run python -m fire_forest hydra.verbose=true
```

## 参数实验阶段

首先使用良好的结构，将影响模型行为的实际参数与配置实验（如名称、重复次数、并行情况...）等配置参数进行分开。

对于小型模型，合理地设计用以测试的配置 `test.yaml` 与用以真正实验的配置 `exp.yaml`，在探索不同参数组合的时候灵活地缩短测试时间，一旦确定了真正需要重复运行，再调用 `exp.yaml` 配置。

`hydra` 支持在命令行里进行快速的参数修改实验，可以直接在命令行里进行覆写特定参数。

```shell
uv run python -m fire_forest Tree.moor=true
```

当你已经有一个“可能出现涌现/阈值现象”的假设（比如这里的树密度阈值），就进入批量测试：用 `-m/--multirun` 扫参数，结合重复运行来获得稳定的统计结论。这个仓库已经在 `configs/config.yaml` 的 `hydra.sweeper.params` 里配置好了一个典型的扫描：

- **`model.density`**：`0.1 → 0.9` 步长 0.1
- **`Tree.moor`**：`True/False`（对比 Von Neumann vs Moore 邻域的差异）

```shell
uv run python -m fire_forest --multirun exp=exp
[2026-01-07 14:11:55,338][HYDRA] Launching 18 jobs locally
[2026-01-07 14:11:55,338][HYDRA]        #0 : model.density=0.1 Tree.moor=True exp=exp
[14:11:55][abses.core.experiment][INFO] - Running experiment with 10 repeats and 5 parallels.
Job 0 repeats 10 times.: 100%|███████████████████████████████████████████| 10/10 [00:21<00:00,  2.15s/it]
[2026-01-07 14:12:16,922][HYDRA]        #1 : model.density=0.1 Tree.moor=False exp=exp
[14:12:16][abses.core.experiment][INFO] - Running experiment with 10 repeats and 5 parallels.
Job 1 repeats 10 times.: 100%|███████████████████████████████████████████| 10/10 [00:19<00:00,  1.99s/it]
[2026-01-07 14:12:36,874][HYDRA]        #2 : model.density=0.2 Tree.moor=True exp=exp
[14:12:36][abses.core.experiment][INFO] - Running experiment with 10 repeats and 5 parallels.
Job 2 repeats 10 times.:  40%|█████████████████▌                          | 4/10 [00:09<00:14,  2.38s/it]
```

同时，利用 `ABSESpy` 的 `tracker` 可以让你的模型关键变量、`metric` 被自动记录和追踪。这个例子使用 `aim` 作为后端（配置在 `configs/tracker/aim.yaml`）：你只需要声明“记录什么”，其余的命名、落盘与组织结构交给框架处理。

### 使用 Tracker 记录

你可以启动 `aim` 查看实时更新的实验结果，以及每个实验的参数、运行时间、内存消耗...

```shell
uv run aim up
```

![监测关键的模型涌现指标](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/CleanShot%202026-01-07%20at%2016.25.31.png)

在上面展示的这样一个交互式页面中，你可以迅速地对比不同的实验结果，通过高级地筛选功能确定你感兴趣的实验，并查看其参数详情。

### Hydra 的实验管理

> [!warning]
>
> 如果你在本阶段碰到了需要修改模型逻辑的情况，务必进行版本管理，在实验中也修改好标签并更新实验描述！才不会遇到版本混乱的情况。

根据我们在 `model.end()` 方法中导出 `csv` 文件的配置， `Hydra` 将自动使用如下结构来进行实验结果的集中管理：

```python
class Forest(MainModel):
	...
	def end(self) -> None:
		"""运行完毕后将实验结果以 `.csv` 格式导出到配置的输出目录。"""
		if self.settings.exp.save_data:
			df = self.datacollector.get_model_vars_dataframe()
			df.reset_index(names="step").to_csv(
				self.outpath / f"burned_rate_{self.run_id}.csv"
			)
		return super().end()
```

```shell
... ...
├── 8_Tree.moor=True,exp=exp,model.density=0.5
│   ├── burned_rate_1.csv
│   ├── burned_rate_2.csv
│   ├── fire_spread.log
│   └── model.log
├── 9_Tree.moor=False,exp=exp,model.density=0.5
│   ├── burned_rate_1.csv
│   ├── burned_rate_2.csv
│   ├── fire_spread.log
│   └── model.log
└── multirun.yaml
```

## 结果分析阶段

> [!warning]
>
> 如果你在这个阶段发现“需要回头改模型逻辑/加指标”，请一定回到第二阶段：更新版本标签、重新跑实验、明确记录差异。不要在同一份输出目录里混跑不同实验。

当你完成批量实验后，真正的研究工作才刚开始：你需要把“很多次运行”的输出变成可比较、可复现、可写进论文/报告的结论。这个仓库的推荐做法是：

1) **确定最终用于分析结论的实验目录**：如果你用 Hydra 管理输出，每一次 `multirun` 都会输出一个“实验批次文件夹”，里面有 `multirun.yaml`（记录这批实验如何生成）以及若干个 job 子目录（例如 `0_Tree.moor=True,exp=exp,model.density=0.1/`）。
2) **用 `ExpAnalyzer` 读入整批实验**：它会遍历这批实验的每个 job，帮你取回数据与对应的配置值（例如某个 job 的 `Tree.moor`、`model.density` 等）。
3) **把数据整理成“可讲故事”的表**：常见做法是提取每次重复运行的最后一步指标，再按情景分组统计（均值/方差/置信区间）。

### 1) 选择你要分析的实验批次（exp_data）

在 `configs/config.yaml` 里有一个 `exp_data`，它应该指向你要分析的那次 multirun 结果目录。例如：

- `out/fire_spread/2026-01-07/15-01-16`

> [!tip]
>
> 新手最常见的坑是把 `exp_data` 指到了某个 job 子目录。正确的是“包含多个 job 的那层目录”（能看到 `multirun.yaml` 那层）。

### 2) 用 ExpAnalyzer 汇总每个 job 的结果

下面这段代码在 `analysis.ipynb` 里已经给出，它展示了一个非常实用的范式：对每个 job，拿到数据（`res.data`）与配置（`res.select(...)`），然后拼成一个“长表”便于后续统计分析。

```python
from abses.utils import ExpAnalyzer
import pandas as pd

analyzer = ExpAnalyzer(cfg.exp_data)

final_results = pd.DataFrame()

for res in analyzer.results:
    # Keep only the final step for each repeat
    data = res.data
    job_data = data[data["step"] == data["step"].max()].copy()

    # Attach scenario parameters for grouping/plotting
    job_data["moor"] = res.select("Tree.moor")
    job_data["density"] = res.select("model.density")

    final_results = pd.concat([final_results, job_data], ignore_index=True)
```

### 3) 从“长表”到结论：对照情景 + 稳健统计

当你有了 `final_results`，下一步建议按研究问题组织你的分析结构，而不是“看到什么画什么图”。以森林火灾模型为例，一个典型的新手友好问题是：

- **密度阈值是否存在？大概在多少？**
- **邻域选择（Von Neumann vs Moore）是否会移动阈值或改变曲线陡峭程度？**

你可以先做最朴素但稳健的一步：按 `density × moor` 分组，计算 `burned_rate` 的均值与不确定性（比如标准差、标准误或 bootstrap 置信区间）。然后再决定要不要画最终图、画哪一种图。

![论文发表质量的插图](https://songshgeo-picgo-1302043007.cos.ap-beijing.myqcloud.com/uPic/a4J1Pg.png)
