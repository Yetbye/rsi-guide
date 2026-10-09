# FINAL_memit.md — MEND 博客交付

## 交付物
- `index.html`：13 章深度博客（Venus 樱吹雪配方、MathJax、5 内联 SVG、4 数学块、8 法证批判、5 科研问题卡、4 代码块）。
- `figures/`：论文原图精准裁剪 4 张（Fig1/2/3/4，fig1/fig3 经 image-bbox 重裁）。
- `BLOG_PLAN.md` / `ACCEPTANCE_memit.md`；论文提取文本 `../memit_text.txt`。

## 论文一句话（含命名澄清）
Fast Model Editing at Scale = **MEND**（Mitchell et al., ICLR 2022；≠ MEMIT/Meng 2023）：学习一组小编辑网络 g，把单样本微调梯度（天然 rank-1，分解为 (u, δ) 两因子）变换成可靠/局部/泛化的参数更新；编辑器参数 O(d)、恒等初始化、单卡可训 10B+ 基座，是 2022 年唯一成功编辑 10B+ 模型的方案（T5-XXL ES 0.89；GPT-J ES 0.88）。

## 八条取证
F1 T5 drawdown 度量偏软（欠拟合脚注）· F2 "Scales to 10B" 环境相对 · F3 KE 失败归因无隔离实验 · F4 等价邻域口径跨数据集不一致 · F5 批量 DD 随 k 恶化 6× · F6 locality KL 标签 token 近似 · F7 归一化/恒等初始化是命门（ES 0.02/0.27）· F8 ENN 对照复现偏差。

## 流程备注
- 本轮起评审代理改为**只读**（e2e-TTT 轮的并发写事故教训）；只读模式下无文件冲突，评审引用与文件实态一致。
- 百炼 key 仍 401，AI 封面继续用 SVG 主视觉（系列一致处置）。

## 待办（用户侧）
- 有效百炼 key 后补 AI 封面（`_genimg.py` 管线，spec 需按 MEND 主题新写）。
- Q1（秩-信息含量定律）与 Q3（vs locate-then-edit 统一基准）为零/低训练成本首选；Q5（MEND 化 TTT 内环）可两篇合流。
