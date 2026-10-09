# FINAL_delmem.md — δ-mem 博客交付说明

## 交付物
- `index.html`：单文件深度博客（18 章，MathJax，7 内联 SVG，4 代码块，10 洞察框，5 研究问题卡）。
- `BLOG_PLAN.md` / `ACCEPTANCE_delmem.md` / 本文件。
- `assets/hero_cover.jpg`；`figures/` 下 5 张 AI 图（含迭代稿 v1-v4）+ 4 张论文原图裁剪。
- 工具脚本：`_genimg.py`（百炼 qwen-image-3.0-pro 生成器）、`_specs*.json`（prompt 记录）。
- `delmem_text.txt`（位于上级目录）：PDF 全文提取，公式核对依据。

## 阅读路径建议（用户：自进化小白 → 顶级学者）
1. 第 1-2 章建立问题与坐标系；2. 第 3 章数学谱系（Widrow-Hoff→Schlag→DeltaNet→Gated DeltaNet→Qwen3-Next）；3. 第 4-9 章架构逐组件；4. 第 10-14 章实验精读；5. 第 15-16 章地图与批判；6. 第 17 章选一个开放问题动手；7. 第 18 章路线图+代码复现。

## 关键学术结论速记
- δ-mem = 冻结全注意力骨干 + 8×8 在线联想记忆状态（gated delta rule 更新）+ 读出低秩修正注意力（q/o 分支，α/r 缩放）。
- 主结果：平均 46.79→51.66（TSW）；MAB 29.54→38.85（MSW）；TTL 26.14→50.50（SSW）；LoCoMo 40.79→49.12（MSW）。
- 参数 4.87M（0.12%）；训练仅 QASPER 2219 样本、1 epoch；上下文只写状态不回放。
- 两条引用注记：Context2LoRA 系自建基线；Qwen3-Next 锚点应为 Gated DeltaNet (ICLR 2025) + 官方模型卡。

## 待办（后续可选）
- [ ] 若作者放出官方代码，将代码块 A-D 升级为"可运行实现"并补对照实验。
- [ ] 第 17 章 Q1/Q2 任一实验落地后，回填结果到博客"开放问题"章。
- [ ] 门户页（RSI 根目录尚无 index.html 门户）：如后续建立博客门户，将本博客卡片加入。
- [ ] 复现 benchmark：LoCoMo / MemoryAgentBench 子集自跑一遍，校验 Table 1 读数。

## 复跑插图生成
```bash
cd D:\success\RSI\delmem_blog
python _genimg.py _specs.json     # 封面+4 概念图（API key 内置于 _genimg.py）
```
