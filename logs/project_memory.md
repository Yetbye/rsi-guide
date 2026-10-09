# project_memory.md — 博客制作偏好档案

## 封面风格偏好
- **首选：水彩写意（风格 A）**——湿画法水彩、薰衣草紫夜空、金箔微粒、纸纹质感（dyprag 封面与 δ-mem 封面同款血脉）。
- δ-mem 封面 prompt 骨架（已验证成功，可复用）：`[PURPOSE]: Academic paper blog cover illustration. [STYLE]: Dreamlike watercolor, wet-on-wet washes, Art Nouveau flowing lines, bleeding edges, visible paper grain, golden sparkle. [SUBJECT]: 论文核心隐喻的左右分置构图（丰饶源流 → 浓缩核心）. [COLOR]: lavender #a855f7, deep violet, coral #fb7185, mint #34d399, golden amber #fbbf24, cream paper. No text, no watermark.`
- 备选：深色科幻数字艺术（rpg 封面款），仅当论文主题偏硬件/系统时使用。

## Hero 布局
- 默认模板 A（浅色渐变 + 图片卡片），与水印封面搭配可读性最佳。徽章只写 venue（arXiv/会议），不写作者。

## 插图生成管线
- 平台：阿里云百炼；模型：qwen-image-3.0-pro；端点：multimodal-generation/generation；脚本模板：`delmem_blog/_genimg.py`。
- 学术架构图经验：扩散模型对"多回路返回箭头"极不可靠（δ-mem 架构图迭代 4 轮）。**可靠套路**：双横带拓扑（骨干上排、模块下排）+ 最多 2-3 条垂直/斜向注入箭头；所有箭头声明 SINGLE-HEADED；标签 ≤3 词。仍失败则改用自绘 SVG 承担精确图，AI 图只做概念图。
- 精确数字图表：不用图像模型，用 pixel-art 风格内联 SVG（pattern 7px 像素格填充柱体）。

## 图表裁剪
- 沿用 dyprag 的坐标裁剪 + 验证闭环（clip 内不得含其他 Figure/Table 标题）。

## 博客配色 DNA
- 每篇独立配色：rpg=午夜青金、dyprag=紫夜金、delmem=紫水晶+羊皮纸金。保持 lavender-coral-mint 家族但换主色相。
