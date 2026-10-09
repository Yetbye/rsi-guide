# FINAL_ipttt.md — In-Place TTT 博客交付

## 交付物
- `index.html`：14 章深度博客（青瓷 Celadon 配色、MathJax、5 内联 SVG、4 数学块、9 法证批判、5 科研问题卡、4 代码块）。
- `figures/`：论文原图精准裁剪 4 张（Fig1/2/3/4）。
- `BLOG_PLAN.md` / `ACCEPTANCE_ipttt.md`；论文提取文本 `../ipttt_text.txt`。

## 论文一句话
In-Place TTT（ByteDance Seed，arXiv:2604.06169）把 gated MLP 的最终投影矩阵 W_down 就地充当快权重（drop-in 热启动），chunk-wise 闭式更新 W += η·V̂ᵀZ，目标 V̂=Conv1D(X₀)·W_target 显式 NTP 对齐（定理 1：归纳头设定下 NTP 目标保证正确 token logit 上升、重建目标无效）；三段并行 scan 实现 CP 原生。热启动 Qwen3-4B/LLaMA-3.1-8B/Qwen3-14B 后 64k-256k RULER 持续领先；从头训练 4B 在 RULER-8k/16k 大幅提升。

## 八条取证
F1 推理期 τ=1e-5 裁剪未消融 · F2 from-scratch 基线绝对分偏低（SWA@4k 14.77）· F3 500M/1.5B 小窗口未展开（规划项）· F4 drop-in 仍需 ~35B token 持续训练 · F5 定理假设理想化 · F6 "NTP 对齐"按构造成立（损失是内积非 CE）· F7 未与 TTT-E2E 对比 · F8 效率只报推理侧。

## 谱系定位（本系列）
五容器谱系中"解析更新 × NTP 目标"的空格：更新规则与 δ-mem/gated delta rule 同族（外积累加），目标语义与 TTT-E2E 同族（NTP 对齐），内环线性化换来 CP 原生并行。与 TTT-E2E 构成"内环非线性程度"的两端对照。

## 待办（用户侧）
- 有效百炼 key 后补 AI 封面。
- Q1（Conv1D 核读出）零成本；Q3（τ vs 门控衰减）与 Q4（delta-rule 化）为方法改进首选。
