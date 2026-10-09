# BLOG_PLAN.md — δ-mem: Efficient Online Memory for Large Language Models

> 单文档计划（v5 精简版）：需求理解 + 技术方案 + 章节设计 + 验收 checklist。
> 论文：arXiv:2605.12357v1（2026-05-12），15 页，NTU / Fudan / Mind Lab 等。
> 博客目录：`D:\success\RSI\delmem_blog\`，主文件 `index.html`。

## 1. 需求理解

- 读者画像：**自进化 / agent 记忆方向小白**，目标是"读完一篇博客 ≈ 该方向入门到能独立提科研问题"。
- 因此博客必须：从零讲清"为什么需要记忆机制"→ 统一分类坐标 → 数学谱系（delta rule 家族）→ 架构逐组件拆解 → 实验逐表精读 → 批判与开放问题 → 自学路线图。
- 图表要求（用户指定）：架构/范式/概念图用 **阿里云百炼 qwen-image-3.0-pro** 生成（已完成，严格评审通过）；效果图另用 **pixel-art 风格自绘 SVG**（精确数字）；论文原图用 PyMuPDF 精准裁剪（已验证）。

## 2. 技术方案与约束

- 单文件 `index.html`：MathJax 3 CDN、Noto Serif/Sans SC、lavender-amethyst-gold 配色（与封面水彩一致，区别于 rpg 的青色、dyprag 的紫夜）、Hero 模板 A（浅色渐变+图片卡片）、glassmorphism 导航。
- 深度门控：15 页论文 → ≥5 章；实际规划 **18 章**，每章 ≥2 深度元素（实验展示章 ≥1）。
- 自绘内联 SVG ≥5：实际 7 个（分类坐标 / 谱系时间线 / read-steer-write 循环 / 粒度对比 / pixel-art 效果柱状图 / 消融因果链 / 容量瓶颈漏斗）。
- 代码附录 4 块（1 可运行 + 3 示意），全部带自检说明与可信度标注。
- 反幻觉：相关工作 19 条已由核查 agent + WebFetch 双重验证；两条关键更正写入博客：
  1. **Context2LoRA 无独立公开论文**——系 δ-mem 自建基线（上下文→LoRA 权重），引用支撑为 LoRA (Hu 2022) 与 Back et al. 2026 (arXiv:2603.01097)。
  2. **δ-mem 用 Qwen3 技术报告支撑 "Qwen-Next gated retention" 属引用错配**；Qwen3-Next 架构（Gated DeltaNet:Gated Attention = 3:1 混合）出自官方模型卡；gated delta rule 学术锚点为 Gated DeltaNet (Yang et al., ICLR 2025)。
- 论文内部不一致（批判章素材）：正文称 LoCoMo no-context 3.49→8.05，Figure 2 读数为 Avg 6.89→9.62（F1 口径）；博客两者并列标注出处。

## 3. 公式清单（已从 PDF 全文提取并逐项核对）

| # | 公式 | 核对点 |
|---|------|--------|
| 1 | v̂_t = S_{t−1} k_t | 预测方向 S·k |
| 2 | L_t = ½‖S k_t − v_t‖²; S_t = S_{t−1} + β_t(v_t − S_{t−1}k_t)k_tᵀ | 系数 ½、残差方向、外积 kᵀ 在右 |
| 3 | S_t = λ_t S_{t−1} + β_t(v_t − S_{t−1}k_t)k_tᵀ | λ 乘旧状态 |
| 4 | qᵐ=L2norm(tanh(W_qᵐ x)); kᵐ=L2norm(tanh(W_kᵐ x)); vᵐ=W_v x | 仅 q,k 归一化 |
| 5 | β_t=σ(W_β x_t+b); λ_t=1−β_t | 互补门 |
| 6 | r_t = S_{t−1} qᵐ_t | 读旧状态 |
| 7 | Δq_t=W_q^Δ r_t; Δo_t=W_o^Δ r_t | 两映射 |
| 8 | q̃_t = q⁰_t + (α/r)Δq_t | 系数 α/r（LoRA 式缩放） |
| 9 | a_t=Attn(q̃_t,K_≤t,V_≤t); ỹ_t=a_t+(α/r)Δo_t | 输出侧加在 attention 后 |
| 10-12 | Diag 门控更新 + 三项展开 + 逐行展开 | Diag(λ) 在左乘 |
| 13-16 | TSW / SSW(mean) / MSW(concat) | MSW 读后 concat |
| 17 | L_SFT = −Σ log p(y_j | Q, y_<j, S^C) | 上下文不回放 |

## 4. 章节大纲（18 章）

1. **引子：记忆问题不是上下文问题**（小白向；二次代价 + context rot；百万 token 也不够）
2. **统一坐标系：记忆状态 × 记忆引导 → 三范式**（SVG#1 + AI 范式图 + 优劣表）
3. **数学地基：从 Widrow-Hoff 到 gated delta rule**（谱系 SVG#2；Eq1-3 推导与直觉）
4. **δ-mem 总架构：读→引导→写循环**（Fig1 裁剪 + AI 架构图 + SVG#3 + 组件分解表）
5. **记忆投影与互补门**（Eq4-5；tanh+L2 的尺度漂移论证；逐维预算直觉）
6. **读取与低秩引导**（Eq6-9；O(r²) vs O(Nd)；与 LoRA 的本质差异：state-conditioned）
7. **写入：先擦后写**（Eq10-12 三项分解；干扰抑制直觉；与 Gated DeltaNet 的关系）
8. **写入粒度 TSW/SSW/MSW**（Eq13-16 + AI 粒度图 + SVG#4；容量依赖的最优粒度）
9. **训练：2219 个样本教会模型"用记忆"**（Eq17；512 vs 8192；0.12% 参数）
10. **实验 I：主结果**（Table1 复现 + pixel-art SVG#5；基线失败模式分析）
11. **实验 II：跨骨干**（Table2；8B→SSW、3B→MSW 的容量交互）
12. **实验 III：记忆真的住在状态里吗**（Fig2 裁剪 + AI 恢复概念图；批判读数）
13. **实验 IV：注入位置消融**（Table3/4 + SVG#6 因果链；qo vs qkvo 的性价比）
14. **效率与代价**（Fig3/4 裁剪；吞吐-记忆权衡；参数量对比）
15. **相关工作地图：两条大河的合流**（验证后谱系；Context2LoRA 与 Qwen3-Next 注记）
16. **批判评估**（6 条带证据的批评：恢复绝对值低、图-文不一致、引用错配、基线公平性、训练分布窄、解码开销）
17. **自主科研问题**（5 张研究问题卡：容量界/TTL 机制匹配/跨会话干扰/r 的 scaling/状态隐私）
18. **小白→学者路线图 + 代码附录**（阅读顺序、复现 checklist、4 代码块）

## 5. 验收 checklist

- [x] 公式全部来自 PDF 提取文本并核对系数/上下标/符号
- [x] 图表裁剪验证闭环（4 图 verify=OK）
- [x] AI 插图严格评审：cover 9.5 / paradigms 9 / arch v4 9 / granularity v3 9 / recovery 9（v1-v3 迭代记录保留在 figures/）
- [x] 相关工作 19 条网络核实（agent 报告 + 8 条 WebFetch 直核）
- [ ] Hero：会议徽章（arXiv 2026 · Preprint）、无作者、居中、模板 A
- [ ] ≥5 内联 SVG（规划 7）；≥3 深度洞察框（规划 8+）；4-5 研究问题卡（规划 5）
- [ ] 代码块 white-space:pre-wrap + 可信度标注 + 自检
- [ ] 浏览器验证：MathJax/图片/SVG/控制台无错
- [ ] 收尾：BLOG_PLAN / ACCEPTANCE / FINAL 文档；README 清单
