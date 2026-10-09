# FINAL_d2l.md — Doc-to-LoRA 博客交付

## 交付物
- `index.html`：15 章深度博客（Venus 水墨丹青配方、MathJax、5 内联 SVG、7 数学推导块、9 法证批判、5 科研问题卡、4 代码块）。
- `figures/`：论文原图精准裁剪 5 张。
- `BLOG_PLAN.md` / `ACCEPTANCE_d2l.md`；论文提取文本 `../d2l_text.txt`。

## 论文一句话
D2L（Sakana AI，arXiv:2602.15902）把 context distillation 元学习进 309M Perceiver 超网络：101M (context, query, response) 三元组上训练后，读一篇 32K 文档 0.2-0.6s 产出 LoRA，此后免上下文回答；SQuAD 达 ICL 上界 82.5%，2Wiki 逼近 oracle（0.857 vs 0.901），MFQA/QASPER 差 oracle 41-56 点；NIAH 上 256-token 训练外推到 40K（chunk ×4、数 ×5）；VLM→纯文本 LLM 零样本跨模态 75%。

## 九条取证（博客 §10 及各章）
C1 "<2GB" 话域 · C2 NIAH 用 CE 简化管线 · C3 oracle 差距跨基准 4-56 点 · C4 Mistral 长文全线失败未解释 · C5 top-16 截断教师分布 · C6 单参数化单注入点 · C7 每基座重训 5 天×8 H200 · C8 知识干扰无修复实验 · （另）NIAH 图 "2K 封顶" 为本博客自查修正项。

## 待办（用户侧）
- 提供有效百炼 key 后可补 AI 封面（管线同 DnD 篇 `_genimg.py`）。
- Q3（D2L-init CD）是零训练成本首选实验；Q4（为 δ-mem 生成初始状态）可两篇合流。
