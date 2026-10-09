# MHML · RSI 深读指南

> 自改进之径 · 十二篇论文 · 五个容器
>
> 跟随北京大学 **Mu Lab** 的 *In-Parameter Learning* 纲领：新知识应该住在哪里——上下文、权重、生成器、在线状态，还是测试时的梯度？

打开 **[`index.html`](index.html)** 进入门户（古希腊风格 · Venus「希腊暖金」配方）。

---

## 这是什么

一份 **Recursive Self-Improvement（RSI）方向的深度阅读指南**。每篇博客不是论文摘要，而是陪读者走完全程：从零建立坐标系 → 数学谱系 → 实验逐表精读 → 法证式批判 → 开放研究问题与复现入口。目标：**读完一篇 ≈ 该方向入门到能独立提出科研问题**。

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

## 仓库结构

```
RSI/
├── index.html            # 门户（Venus 希腊暖金 · 古希腊风格）
├── blogs/                # 12 篇深读 · 自包含单文件 HTML
│   └── <slug>/
│       ├── index.html            # 深读正文（MathJax + 内联 SVG）
│       ├── BLOG_PLAN.md          # 写作计划与取证清单
│       ├── ACCEPTANCE_*.md       # 验收记录
│       ├── FINAL_*.md            # 交付说明与复现入口
│       ├── assets/               # 封面等位图
│       └── figures/              # 论文原图精准裁剪
├── papers/
│   ├── pdf/              # 12 篇论文原文
│   └── text/             # 12 份 PDF 全文提取（公式核对依据）
└── logs/                 # 构建日志 · 偏好档案 · 门户脚本
```

## 门户设计（Venus 协议）

| 层 | 内容 |
|----|------|
| **Base** | Venus 常量：流体字号、8px 间距、`cubic-bezier(0.16,1,0.3,1)` 缓动、`prefers-reduced-motion` |
| **Palette** | 配方 C「希腊暖金」：羊皮纸底 `#FBF8F1` / 青铜墨 `#2B2419` / 陶土红 `#B85C38` / 金 `#C09A54` |
| **Decorations** | 回纹饰带（meander）、多立克柱、日晷星盘、桂冠、双耳瓶、神庙山花、菱形古典线 |

希腊回纹由内联 SVG data-URI 平铺（非位图），任意分辨率不失真；门户其余图形全部程序化 SVG。

## 阅读路径

- **时间有限** → δ-mem → DnD → TTT-E2E（在线记忆总览 · 生成参数全景 · 测试时训练前沿）
- **生成参数主线** → RPG → Text-to-LoRA → GenAdapter → DyPRAG → DnD → SHINE → D2L
- **自改进两端** → MEND（2022 权重手术刀）→ In-Place TTT（2026 就地快权重）

## 本地使用

```bash
# 直接打开即可（无构建步骤）
start index.html            # Windows
# 或起一个静态服务
python -m http.server 8080  # 然后访问 http://127.0.0.1:8080
```

门户目录表由脚本生成，新增一卷后重跑：

```bash
python logs/build_portal.py
```

## 图谱：Mu Lab 相关仓库

- [In-Parameter-Learning](https://github.com/MuLabPKU/In-Parameter-Learning) — 纲领 · 立场论文《为什么终身 AI 系统需要的不止是更长的上下文》
- [SHINE](https://github.com/MuLabPKU/SHINE) — 本指南卷 Ⅶ
- [PiSSA](https://github.com/MuLabPKU/PiSSA) · [TransArch](https://github.com/MuLabPKU/TransArch) · [PaST](https://github.com/MuLabPKU/PaST) · [LIFT](https://github.com/MuLabPKU/LIFT) · [LooGLE-v2](https://github.com/MuLabPKU/LooGLE-v2) 等

## 说明

- 论文版权归原作者所有；各卷解读为本仓库原创深读文本，批判观点不代表论文作者立场。
- 封面与插图部分由 AI 生成（阿里云百炼 qwen-image）或基于论文原图裁剪，仅作学习用途。
- 生成脚本 `blogs/*/_genimg.py` 通过环境变量 `DASHSCOPE_API_KEY` 读取密钥，仓库内不含任何 API key。
- 一切引用请回到 `papers/` 原文核对。
