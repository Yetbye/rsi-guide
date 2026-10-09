# BLOG_PLAN.md — Doc-to-LoRA (D2L) 深度阅读博客

> 论文：Doc-to-LoRA: Learning to Instantly Internalize Contexts, arXiv:2602.15902v1 (2026-02-13)，Sakana AI（与 Text-to-LoRA 同组）。28 页含附录。
> 输出：`D:\success\RSI\d2l_blog\index.html`。

## 用户硬约束
1. **减少废话**——写作风格收紧：无铺垫句、无重复总结、无比喻性绕路；每句话承载信息。保留深度元素（推导/取证/反事实），删掉叙事性废话。
2. 深度维持 DnD 篇标准（自博弈批判 ≥1 轮）。

## 方案
- Venus 配方 B（水墨丹青）——契合"文档→墨→参数"主题；装饰：水墨山 SI-03、中式角 CR-02、祥云 SC-04，每 section ≤4。
- AI 封面：key 仍 401 → 手绘水墨 SVG 主视觉；spec 待 key 恢复。
- 图表：论文原图裁剪 5 张（Fig1/2/3/4/9，全部 verify=OK）+ 自绘 SVG ≥6 + pixel 图 2。
- 相关工作核实：T2L=ICML 2025（D2L 参考文献 + 此前 arXiv 核实）、GA=ICLR 2025（本仓库有原文 PDF）、Cartridges=arXiv 2506.06266、MEND=ICLR 2024、Gisting=NeurIPS 2023、Perceiver=ICML 2021、RULER=COLM 2024、Lost-in-the-middle=TACL 2024——均取自论文参考文献与已核实条目，不另立说法。

## 章节（15）
1 问题与定义（Eq1-2）· 2 元学习 CD（Eq3-4 + 数据管线 101M 三元组）· 3 架构（Eq5-9、26 层 down_proj、α_l、batched/iterative）· 4 NIAH 外推（256→40K；⚠CE 简化版）· 5 短文 QA · 6 长文档 QA · 7 模拟多查询 CD（Table4）· 8 极端泛化（query 交换 / VLM→LLM 75.03% / HyperKV RoPE 陷阱）· 9 消融与失败模式（KL>NTP、rank16、知识干扰）· 10 批判 ×8（法证）· 11 理论：CD 均值视角 · 12 科研问题 ×5 · 13 路线图 + 工作区三方对照 · 14 代码 ×4 · 15 结语

## 取证清单（已溯源）
C1 "<2GB" 话域（长文档 batched 11.5-31.2GB 反超 oracle）· C2 NIAH 主结果用 CE 简化管线 · C3 与 oracle 差距在 MFQA/QASPER 巨大 · C4 Mistral 长上下文全线失败未解释 · C5 top-16 logits 截断教师分布 · C6 单参数化（仅 MLP down_proj）· C7 每目标 LLM 重训 5 天×8 H200 · C8 query 生成偏置→知识干扰只有假设无修复实验。

## 验收
- [ ] 公式 Eq1-9 全部 PDF 提取核对
- [ ] 每章 ≥2 深度元素且无废话
- [ ] 自博弈批判 ≥1 轮回填
- [ ] 浏览器验证 + ACCEPTANCE/FINAL
