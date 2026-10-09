# MHML · RSI 深读指南

> 自改进之径 · 十二篇论文 · 五个容器

这是我读 RSI（递归自改进）方向的深度笔记：**新知识该住在哪里**——上下文、权重、生成器、在线状态，还是测试时的梯度？
十二篇论文，一条从模型编辑走到测试时训练的路。每篇都拆公式、逐表读数，把我读到的矛盾和还想追的问题一并写下来。

打开 **[`index.html`](index.html)** 进入门户（古希腊风格 · Venus「希腊暖金」配方）。

> 问题线索来自 Mu Lab 的立场论文《In-Parameter Learning》，它把「新知识该住在哪里」问得最清楚。
> 这套笔记是我沿这个问题往下读的结果；除引用其公开论文外，与 Mu Lab 无其他关联。

---

## 这是什么

一份 **Recursive Self-Improvement（RSI）方向的深度阅读笔记**。每篇都不是论文摘要，而是陪你走完全程：从零建立坐标系 → 数学谱系 → 实验逐表精读 → 法证式批判 → 开放研究问题与复现入口。目标只有一个：**读完一篇 ≈ 该方向入门到能独立提出科研问题**。

## 十二卷 · 五容器谱系

| 容器 | 卷 | 论文 | 出处 |
|------|----|------|------|
| Βʹ 静态参数 | I | [MEND — Fast Model Editing at Scale](blogs/mend/) | ICLR 2022 |
| Γʹ 生成参数 | II | [Generative Adapter](blogs/genadapter/) | arXiv 2411.05877 |
| Γʹ 生成参数 | III | [RPG — Recurrent Diffusion for Parameter Generation](blogs/rpg/) | arXiv 2501.11587 |
| Γʹ 生成参数 | IV | [DyPRAG — Dynamic Parametric RAG](blogs/dyprag/) | arXiv 2503.23895 |
| Γʹ 生成参数 | V | [Text-to-LoRA](blogs/text2lora/) | ICML 2025 · Sakana AI |
| Γʹ 生成参数 | VI | [DnD — Drag-and-Drop LLMs](blogs/dnd/) | arXiv 2506.16406 |
| Γʹ 生成参数 | VII | [SHINE](blogs/shine/) | ICML 2026 · 北大 Mu Lab |
| Γʹ 生成参数 | VIII | [Doc-to-LoRA](blogs/d2l/) | arXiv 2602.15902 · Sakana AI |
| Δʹ 在线状态 | IX | [δ-mem](blogs/delmem/) | arXiv 2605.12357 |
| Δʹ 在线状态 | X | [UniMem](blogs/unimem/) | Preprint 2026 |
| Εʹ 测试时梯度 | XI | [TTT-E2E](blogs/ttt-e2e/) | arXiv 2512.23675 |
| Εʹ 测试时梯度 | XII | [In-Place TTT](blogs/inplace-ttt/) | arXiv 2604.06169 · ByteDance × PKU |

## 怎么读

每篇都是一份自包含的网页，点开就能读（公式由 MathJax 渲染，首次打开需联网）。

- **没有时间** → δ-mem → DnD → TTT-E2E：先把「记忆住在哪」的总问题、生成参数的全景、测试时训练的前沿各读一篇。
- **跟生成参数这条线** → RPG → Text-to-LoRA → GenAdapter → DyPRAG → DnD → SHINE → Doc-to-LoRA。
- **只看自改进的两端** → MEND（2022 的权重手术刀）→ In-Place TTT（2026 的就地快权重）。

每篇末尾都有：论文原文链接（自行核对）、研究问题卡（可以动手的方向）、以及我读完之后留下的疑问。

## 延伸阅读：我参照的源头（Mu Lab）

- [In-Parameter-Learning](https://github.com/MuLabPKU/In-Parameter-Learning) — 立场论文《为什么终身 AI 系统需要的不止是更长的上下文》，我这套笔记的问题线索来自这里
- [SHINE](https://github.com/MuLabPKU/SHINE) — 卷 Ⅶ 的原作
- [PiSSA](https://github.com/MuLabPKU/PiSSA) · [TransArch](https://github.com/MuLabPKU/TransArch) · [PaST](https://github.com/MuLabPKU/PaST) · [LIFT](https://github.com/MuLabPKU/LIFT) · [LooGLE-v2](https://github.com/MuLabPKU/LooGLE-v2) 等

## 说明

- 论文版权归原作者所有；各篇解读是我自己的深读笔记，其中的批判观点不代表论文作者立场。
- 封面与插图部分由 AI 生成（阿里云百炼 qwen-image）或基于论文原图裁剪，仅作学习用途。
- 生成脚本 `blogs/*/_genimg.py` 通过环境变量 `DASHSCOPE_API_KEY` 读取密钥，仓库内不含任何 API key。
- 一切引用请回到 `papers/` 原文核对。
