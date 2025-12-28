# Vibe Coding Best Practice for Researchers

## 目录

- [搭建项目框架](#搭建项目框架)
- [草拟项目计划](#详细项目计划)
- [执行项目实现](#执行项目实现)
- [最后的建议](#最后的建议)

## 搭建项目框架

1. 前往 [Python  项目模板仓库](https://github.com/SongshGeo/Python-Project-Template)，使用模板创建新的仓库
2. 克隆到本地，调用 `make setup` 快捷命令构建
3. 使用提示词进行项目规划：

```markdown
我将要在本项目中使用 Python 复现 NetLogo 里的经典模型 ${模型名称}，这是本模型的 NetLogo 说明：

${在此处插入 NetLogo 代码}

这是 Netlogo 里面的代码供你参考：

${在此处插入 NetLogo 代码}

我希望请你帮我设计一个简洁的文档说明，包括如何使用 Python 实现的愿景，主要内容包括：

1. 模型说明
2. 实现愿景
3. 技术栈
4. 用户接口

我的初步想法是：
${初步想法}
<!-- 比如我在示例仓库中这样说：使用不同的框架进行实现，包括纯 Python、Mesa、ABSESpy。 -->

请你现在 XX.md 中完成一个简洁的项目文档，说明模型的设计愿景和框架，不要过度设计，我们后面会不断迭代。然后在 README.md 中说明本项目的实现愿景和未来的迭代路线。
```

4. 人工检验生成的文档，确保符合你的愿景，并删除冗余内容，保证简洁，简洁，简洁！
5. 要求 AI 完善技术栈文档：

```
这是我要做的模型设计 @cache/model-design.md，这是我的大致技术栈  @cache/tech-stack.md:1-10，我接下来要设计纯 Python 实现的版本，请你提出**最简单但最健壮**的技术栈并补充到技术文档里。
```

## 详细项目计划

1. 将生成的设计文档与技术文档喂给 AI，生成一个详细实施计划（Plan 模式），检查，并将生成的计划纳入到你的框架里
2. 检查 AI 对技术栈的选择是不是符合你的预期，对任何修订反哺到之前的技术栈说明之中
3. 确定粗略的技术栈没问题后，让另一个 AI Agent（最好是另一个 model）帮你看看技术栈是否有问题，有没有需要进一步确定的细节

```prompt
阅读 @cache 里所有文档，再看看 @.cursor/plans/纯python基础实现计划_b2c56ad0.plan.md 里的计划对你来说是否完全清晰？你有哪些问题需要我澄清，让它对你来说 100% 明确？

...
我的回答
...
```

4. 回到 Plan 模式的第一个 Agent，告诉他更新，并回答他的问题

```
我的同伴对计划做了一些更详细的修改，这个修改对你来说有问题吗？你再看看我的 @cache 里的所有文档，有任何不清楚的地方还需要我澄清吗？
```
5. 根据你的回答修改 implementation-plan.md，让计划更完善。

## 执行项目实现

1. 让 Agent 开始执行：

```prompt
阅读 @cache 所有文档，然后执行实施计划的第 1 步。我会负责跑测试。在我验证测试通过前，不要继续推进。
```

2. 检验 `make test` 是否能顺利执行，如果不能则让 AI 修订
3. 检验 `pre-commit` 是否能顺利运行，如果不能则让 AI 修订

```prompt
${引用命令行输出} 有未通过的检查，请你核查本问题存在并修改
```

4. 手动更新 “design” 里的设计变化，自动更新所有文件的进度：

```prompt
你的修改全部验证通过，再次查看 @cache/ 里的内容，打开 progress.md 记录你做了什么供后续开发者参考，再把新的架构洞察添加到 architecture.md 中解释每个文件的作用，如果有什么新的技术栈需要声明，也需要在 @cache/tech-stack.md 中进行补充，以方便后来的开发者上手。最后可以把实施计划里的当前标记为“已完成”了
```

5. Code Review (新 Agent 或者 Review 模式)，与此同时浏览一下 AI 对你代码库所做的改动，Cursor 会自动写这个 prompt

```prompt
Verify this issue exists and fix it: ...
```

6. 把改动提交到 Git，尝试提交标准化 commit message
7. 新建 Agent，继续用类似上述步骤 1 的提示词继续推进，重复推进后续步骤，按此流程直到整个计划全部完成。

## 最后的建议

### Tips

1. 永远 先用 "Ask" 或 "Plan"模式，确认满意后再执行
2. 多个模型互相检验，减少幻觉出现的可能性
3. 不要认为上下文压缩以后能保持好很好的上下文

### 参考资料

- [Awesome cursor rules](https://github.com/PatrickJS/awesome-cursorrules/tree/main)
- [Cursor Best Practices](https://github.com/digitalchild/cursor-best-practices)
- [Vibe Coding best practice 2025](https://github.com/2025Emma/vibe-coding-cn)
