
# Slides

```
uv run quarto preview slide/abmind03_present.qmd
```

# Model
运行模型并绘图

```bash
uv run snakemake -j 4
```

这将运行 workflow/Snakefile 中定义的所有步骤，并使用 4 个并行作业。结果图将保存在 results/ 目录中。
通过调整 Snakefile 中的参数，您可以更改模拟的设置，进行敏感性分析。
