# FINAL_dnd.md — DnD 博客交付说明

## 交付物
- `index.html`：18 章深度博客（Venus 浮世绘蓝调设计系统，MathJax，8 内联 SVG，8 数学推导块，10 洞察框，10 法证式批判，5 科研问题卡，4 代码块）。
- `figures/`：论文原图精准裁剪 8 张（Fig1/2/3/4a/4b/4c/5/6）。
- `assets/`：暂无位图（AI key 失效，主视觉为内联 SVG）；`_specs_cover.json` + `_genimg.py` 备用。
- `BLOG_PLAN.md`（6A 合并文档）、`ACCEPTANCE_dnd.md`；过程日志 `../one-step-output/MASTER_LOG.md`。
- 论文提取文本：`../dnd_text.txt`。

## 一句话总结论文
DnD 把 LoRA 适配从"每任务一次梯度下降"折叠为"一次前向"：在 prompt-检查点对上做 MSE 回归的超卷积生成器，0.11s 生成 0.5B 全套 LoRA，在未见过的常识任务上平均比训练它的 LoRA 高 21 分——但监督是"半成品快照"，且基座越强增益越窄。

## 博客独有的十项取证（论文未明说/互相矛盾的）
C1 base PIQA=16.6% 低于随机 · C2 半成品×错位参照系 · C3 三处倍数口径 · C4 noise aug 未定义 · C5 同一基座两套评测数字 · C6 prompt 批长自相矛盾 · C7 缺 model-soup/LoRA 合并基线 · C8 关键设计未消融+单骨干家族 · C9 Table 5 的 HumanEval 行实为 pass@10 · C10 Fig 6 投影未说明+最佳单 LoRA 打败 DnD。

## 待办（用户侧）
| # | 事项 | 优先级 |
|---|------|--------|
| 1 | 提供新的百炼 API key 后运行 `python _genimg.py _specs_cover.json` 生成 AI 封面（3 候选），选中后替换 hero SVG 区块 | 中（现 SVG 封面已可用） |
| 2 | 若作者放出官方代码：核验 noise aug（C4）与代码 B 的维度对齐细节 | 低 |

## 复现入口
- 最小复刻：代码 A（tokenization）+ 代码 C（配对）+ 0.5B 两个数据集 leave-one-out（对应 Table 4c 的 2-1 组，预期失效）。
- 三个假说检验（§14）与五个科研问题（§15）均有独立实验设计。
