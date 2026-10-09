# BLOG_PLAN.md — In-Place TTT 深度阅读博客

> 论文：In-Place Test-Time Training, arXiv:2604.06169v1（2026-04-07），ByteDance Seed + 北大。20 页。
> 输出：`ipttt_blog/index.html`。风格：自组"青瓷 Celadon"配色（区别于系列前五篇）+ 紧凑行文。

## 方法一句话
三大壁垒（架构不兼容/逐 token 低效/重建目标错配）的工程化解法：gated MLP 的最终投影矩阵 W_down 就地充当快权重（drop-in、可热启动），chunk-wise 闭式更新（W += η·V̂ᵀZ），目标 V̂ = Conv1D(X₀)·W_target 显式 NTP 对齐；定理 1 在归纳头设定下证明 NTP 对齐目标保证正确 token 的 logit 上升而重建目标不能；三段并行 scan 实现 CP 原生。

## 章节设计（14 章）
1 三大壁垒 · 2 in-place 设计（W_down 即快权重；FFN=KV 记忆先验）· 3 chunk-wise 更新（apply/update）· 4 LM-Aligned 目标（Eq1 闭式）· 5 Theorem 1（归纳头；两条假设；NTP vs 重建）· 6 工程（CP 三段 scan/因果 padding/文档边界重置/初始化/τ 裁剪）· 7 实验 I drop-in（Table1/2）· 8 实验 II from scratch（Fig2/Table3；RULER-8k 6.58→43.82 异常取证）· 9 消融+效率（state/chunk/objective；Fig4）· 10 批判×8 · 11 谱系坐标（④/⑤ 边界坍缩；vs TTT-E2E 内环非线性程度；vs δ-mem delta-rule）· 12 科研问题×5 · 13 路线图+代码×4 · 14 结语

## 取证清单（8 条）
F1 推理期 τ=1e-5 裁剪未消融（RULER 增益对 τ 的敏感性未知）· F2 Table 3 基线 RULER-8k=6.58 反常低（8k 即训练窗口，FA 基线近乎零分更像训练不稳）· F3 500M/1.5B 仅测到 32k 且 SWA 窗口 2048/4096 偏小 · F4 "drop-in"仍需 ~35B token 持续训练（架构兼容 ≠ 免训练）· F5 Theorem 1 假设偏强（key-query 对齐期望精确成立、其余项期望恰为零）· F6 损失是 −⟨·,·⟩_F 嵌入相似度而非 NTP 交叉熵（"NTP 对齐"按构造成立；定理证的是 value 嵌入 logit 上升）· F7 未与 TTT-E2E 对比（最近亲：同改 MLP + 同 NTP 对齐）· F8 效率只报推理（prefill/显存），训练期开销（外环学 Conv1D/W_target 需穿过 scan 的梯度）未报。

## 关键数字（已核对）
Table 1（Qwen3-4B RULER）：Baseline 96.6/94.1/92.1/88.7/74.3/74.8/41.7 vs In-Place TTT 96.1/95.6/92.7/89.3/78.7/77.0/43.9（4k-256k）。Table 2：LLaMA-3.1-8B @64k 81.6→83.7；Qwen3-14B 67.9→70.6（YaRN 81.3→82.5）。Table 3（4B/120B token）：RULER-8k FA 6.58→43.82；SWA 9.91→26.80；ARC-C 33.19→32.34 反降。消融：state size 单调↑；C=512/1024 最优；Conv1D 主长上下文、W_target 主短上下文。持续训练：20B@32k + 15B@128k（lr 5e-6，YaRN，Conv size 5）；τ=1e-5。

## 验收
- [x] 4 张裁剪 verify=OK
- [ ] 公式/定理核对 · 每章 ≥2 深度元素 · ≥5 SVG · 无废话
- [ ] 自博弈（只读）回填 · 浏览器验证 · ACCEPTANCE/FINAL
