# FINAL_e2ettt.md — TTT-E2E 博客交付

## 交付物
- `index.html`：15 章深度博客（Venus 希腊暖金配方、MathJax、5 内联 SVG、5 数学块、8 法证批判、5 科研问题卡、4 代码块）。
- `figures/`：论文原图精准裁剪 8 张（Fig1/2/3/4/5/6/8/9）。
- `BLOG_PLAN.md` / `ACCEPTANCE_e2ettt.md`；论文提取文本 `../e2ettt_text.txt`。

## 论文一句话
TTT-E2E（arXiv:2512.23675，Yu Sun 组）把长上下文语言建模重构为持续学习：标准 SWA Transformer 在测试时对上下文做 NTP（内环，只更新最后 1/4 块的 MLP，b=1K、k=8K），训练时用 grad-of-grad 元学习优化 TTT 后的最终损失（外环）。3B/164B：损失 scaling 与全注意力同趋势、prefill 恒定快 2.7×；代价：NIAH@128K 仅 0.06（FA 0.99）、训练 @8K 慢 3.4×、对数据/tokenizer 敏感。

## 八条取证
F1 摘要"同趋势"不含召回任务 · F2 "RNN 32K 后退化"混入微调批次方差（协议×能力交互）· F3 数据/tokenizer 敏感性为轶事级证据 · F4 终版 Table 1 优势 −0.001 低于自设显著性阈值 · F5 训练延迟限制与蒸馏初始化的叙事张力 · F6 预训练分布被裁剪为 ≥8K 文档 · F7 LR 只对 FA 网搜（附基线加强注记）· F8 双 MLP 安全存储无单独消融。

## 待办（用户侧）
- 有效百炼 key 后补 AI 封面（同 `_genimg.py` 管线）。
- Q1（容量论检验）/Q3（蒸馏初始化）为零/低训练成本首选实验；Q5（参数比定律）为理论方向。

## 系列状态
本仓库博客系列至此覆盖五容器谱系：① ICL（—）② 静态参数（—）③ 生成参数（RPG、DnD、Doc-to-LoRA）④ 在线状态（δ-mem）⑤ 测试时梯度（本篇；inplace-TTT 原文在库待解读）。
