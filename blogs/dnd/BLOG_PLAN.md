# BLOG_PLAN.md — DnD: Drag-and-Drop LLMs 深度阅读博客

> one-step 6A 流程：本文档合并 ALIGNMENT/CONSENSUS/DESIGN/TASK（v5 精简）。
> 论文：Drag-and-Drop LLMs: Zero-Shot Prompt-to-Weights, arXiv:2506.16406v1 (2025-06-19)，NUS/UT Austin/St. Gallen/Oxford，18 页（含附录）。
> 输出：`D:\success\RSI\dnd_blog\index.html`。执行日志：`one-step-output/MASTER_LOG.md`。

## 1. 需求理解（ALIGN）

- 用户三点要求：① 给 DND 论文做阅读博客；② **内容深度必须超过 δ-mem 那篇**（用户明确批评"之前你的内容深度是不够的"）；③ **封面图片要精美**。
- 深度升级策略（相对 δ-mem 版的增量）：
  - 每个公式：变量表 + 直觉 + **反事实分析**（去掉这一项会发生什么）
  - 每个实验：数字 → 机制解释 → **适用边界**三段式
  - 批判：**8 条法证式**（证据→推理→影响→补救），含数据异常取证（base 模型 PIQA=16.6% 低于随机水平）
  - 理论章：三个假说解释"生成的权重为何赢过训练的权重"，每个假说配可证伪实验
  - 自博弈批判：写完后 dispatch adv-writer 子代理攻击深度，≥1 轮回填
- 封面：用户给的百炼 key 已失效（401 InvalidApiKey，本会话早前可用）。降级方案：**Venus 设计系统手绘精品 SVG 封面**（程序化、确定性、可做到高精美度），3 个 AI 候选 spec 保留在 `_specs_cover.json`，收尾时重试；仍失败则在 FINAL 文档写明一键重生成命令。

## 2. 技术方案（CONSENSUS + DESIGN）

- **视觉**：venus 可组合设计系统。Palette = 配方 A 浮世绘蓝调（bg #FAF9F6 / ink #2C3E50 / primary #1B4B6F / secondary #5A8F7B / warm #E85D4E / gold #C9A86C），与此前三篇博客配色全部区分。装饰：宣纸纹理 BG-03、希腊角 CR-03（重点区）、古典线 SC-07、波浪分隔 DV-01，每 section ≤4 单元，pointer-events:none。Hero 按 paper-reading-blog 模板 A（居中、徽章、图片卡片），融入 Venus 色斑/双层边框数据条。MathJax 3。
- **图表**：论文原图精准裁剪 8 张（Fig1/2/3/4a/b/c/5/6，全部 verify=OK）；自绘内联 SVG ≥8（含 pixel-art 效果图）；AI 概念图视 API 恢复情况。
- **反幻觉**：p-diff ✓（AE+latent diffusion）、RPG ✓（recurrent diffusion，200M/分钟）、CondP-Diff ✓（条件 latent diffusion 生成 LoRA）、ORAL ✓（条件 recurrent diffusion，text 条件）、Text-to-Model/Tina ✓（DiT+CLIP 条件）、Text-to-LoRA ✓（本地 PDF：Sakana AI，超网络单次前向，9 个 LoRA 训练）。Hyper-Representations 引用保持论文自述（NeurIPS 2022）不展开。

## 3. 章节设计（18 章 + 8 SVG + 8 批判 + 5 RQ）

1. 引子：4×A100 半天 vs 0.11 秒（成本账 SVG）
2. 核心洞察：LoRA 是训练数据的函数（Eq1 解剖 + 反事实）
3. 谱系：参数生成五年史（SVG 时间线，RPG/T2L 工作区联动）
4. DnD 全景：三阶段流水线（Fig2 + SVG + 组件分解表）
5. 条件设计：无标注 prompts 为何最优（Table 4a/4b/14；decoder-only 失败机理）
6. 生成器解剖：hyper-conv decoder（Eq5 推导链 + Fig3 + 成本数学）
7. 训练配方精读（Table 7/9；mild checkpoints 的深意；noise aug 之谜；26624 长度处理）
8. 实验 I：常识推理全矩阵（Table 1/10；BoolQ 崩溃；PIQA 16.6% 异常取证）
9. 实验 II：代码/数学/多模态 + 7B（Table 3/5/6/11/12）
10. 实验 III：配对策略与多样性定理（Fig 4a）
11. 实验 IV：效率前沿（Fig 4b/c + pixel chart + 三处倍数口径考据）
12. 实验 V：vs RPG + 权重空间（Fig 5/6；最近邻 19.1% 陷阱）
13. 批判评估（8 条法证）
14. 理论视角：三个假说解释"生成的赢过训练的"（各配可证伪实验）
15. 自主科研问题 ×5（指纹假说/凸覆盖/外推边界/scaling 与 tokenization 瓶颈/安全）
16. 小白→学者路线图（六步 + 工作区阅读地图）
17. 代码附录 ×4（tokenization[可运行]、hyper-conv block[可运行]、配对策略[示意]、训练循环[示意]）
18. 结语 + 参考文献

## 4. 已核实的论文内部矛盾（批判素材，均已溯源）

| # | 发现 | 证据 |
|---|------|------|
| 1 | prompt batch 长度自相矛盾 | §3.1 "128, 64, 64, 32" vs Table 7 "128/16/32/16" |
| 2 | 加速倍数三种口径 | 摘要 "up to 12,000×" vs Fig4b "2.5~12K×" vs Fig4c "120~60000×" |
| 3 | base 模型 PIQA/OBQA=16.6% 低于随机 | Table 10 末二行（PIQA 二选一随机 50%）→ 评测管线可疑 |
| 4 | noise aug. amplitude 1e-4 未解释 | Table 7 出现，全文无定义 |
| 5 | 监督信号是"温和微调"快照而非最终 LoRA | Table 9：finetune 仅 50-200 步；Fig4b full-shot 300 iter 反超 |

## 5. 验收 checklist（APPROVE）

- [ ] 公式 5 组全部来自 PDF 提取核对（含 Eq5 三向卷积顺序）
- [ ] 8 张裁剪图验证闭环通过
- [ ] 每章 ≥2 深度元素；深度增量策略落实（反事实/三段式/法证/假说）
- [ ] ≥8 内联 SVG；≥8 洞察框；5 RQ 卡；4 代码块带自检
- [ ] 自博弈批判 ≥1 轮并回填
- [ ] 浏览器验证（MathJax/图片/SVG/控制台）
- [ ] 收尾：ACCEPTANCE/FINAL/MASTER_LOG/TODO
