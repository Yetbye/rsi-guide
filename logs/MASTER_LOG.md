# Master Log: DnD 深度阅读博客（one-step 6A）

Started: 2026-09-28
Configuration: AUTO_PROCEED=true, SELF_PLAY=true（adv-writer ≥1 轮）, paper-reading-blog v5 × venus × one-step 三技能合用

---

## Stage 1: ALIGN
- 论文定位：Drag-and-Drop LLMs (arXiv:2506.16406)，prompt→LoRA 超生成器，18 页含附录。
- 用户要求：深度 > δ-mem 篇；封面精美。
- 决策：深度升级四策略（反事实分析/三段式实验精读/法证式批判/可证伪假说），写入 BLOG_PLAN.md §1。
- 事实取证：发现论文内部矛盾 5 项（prompt batch 长度矛盾、三处倍数口径、base PIQA=16.6% 异常、noise aug 未定义、半成品监督）。

## Stage 2-3: ARCHITECT + ATOMIZE
- 18 章结构 + 8 内联 SVG + 4 代码块 + 5 RQ + 8 批判，全部写入 BLOG_PLAN.md。
- 反幻觉核实：p-diff ✓ / RPG ✓ / CondP-Diff ✓ / ORAL ✓ / Text-to-Model(Tina) ✓ / Text-to-LoRA ✓（本地 PDF）；Hyper-Representations 保持论文自述不展开。
- 图表：Fig1/2/3/4a/4b/4c/5/6 共 8 张精准裁剪全部 verify=OK；fig5 首裁混入正文一行，视觉复查后重裁通过（验证闭环有效）。

## Stage 5: AUTOMATE
- 封面：用户提供的百炼 key 返回 401 InvalidApiKey（本会话早期对 delmem 时尚可用，判定 key 已被撤销）。决策：不阻塞——以 Venus 设计系统手绘程序化 SVG 主视觉（夜景+prompt 卡片之河+金色拖拽轨迹+权重晶格+光标）作为最终封面；3 个 AI 候选 spec 保留于 `_specs_cover.json`，`_genimg.py` 可一键重跑。
- index.html 完成后静态校验：8 SVG / 18 sections / 9 洞察框 / 8 批判框 / 5 RQ / 4 代码块 / 标签闭合 / 无缺图。
- 浏览器验证：MathJax 53 容器无裸 LaTeX、7/7 图片、8/8 SVG、pre-wrap、徽章正确；截图目检 hero/生成器章/pixel 图。
- 修复：insight 框 "ammortized" 拼写错误。

## Trade-offs
- 牺牲：AI 生成封面与 AI 概念图（key 失效）→ 换取确定性、矢量、可编辑的手绘 SVG 主视觉（间接收益：无限分辨率、主题更贴合论文隐喻）。
- 牺牲：不在正文复算 Figure 4c 的每条 acc 曲线读数（图内标签只含开销）→ 以论文自己的结论性表述 + 开销标签为准，避免臆测。

---

## Stage 6: ASSESS — 自博弈批判与回填（2026-09-28）
### Self-Play（adv-writer，1 轮，MAX 3 未用尽）
- Adversary: general-purpose（adv-writer 立场），通读博客全文 + 论文提取文本 + 对标 δ-mem 博客。
- 评分：7/10；判定 P0×3 / P1×7 / P2×9。
- 关键发现：§9 两处基座数字写错导致结论翻转（HumanEval 1.5B 基座应为 14.7 而非 17.6；LiveCodeBench 7B 基座应为 34.1 而非 32.3）；§14 核心句归因错误（40.7 是目标数据集自身 full-shot，不在监督里）；§10 与自图矛盾；Q2 公式有数学错误；数学推导密度未超过对标博客。
- 处置：P0/P1 全部回填（含 4 个新数学推导块、C9/C10 两条新批判、口径全程限定）；P2 择要修复（拼写/口径统一/代码可信度降级/导航补全）。未采纳：章节合并重构（权衡记录于 ACCEPTANCE §2）。
- 回填后复检：MathJax 90 容器无裸 LaTeX、7/7 图、8/8 SVG、10 洞察 / 10 批判 / 8 推导 / 5 RQ、标签闭合、无残留错误字符串。

### Artifacts
- dnd_blog/index.html · BLOG_PLAN.md · ACCEPTANCE_dnd.md · FINAL_dnd.md · figures/×8 · _specs_cover.json · 本日志。
