# BLOG_PLAN.md — MEND (Fast Model Editing at Scale) 深度阅读博客

> 论文：Fast Model Editing at Scale（MEND）, Mitchell et al., ICLR 2022，arXiv:2110.11309v2，Stanford。21 页。
> ⚠️ 澄清：文件名易误导——这是 **MEND**（学习梯度变换网络），不是 MEMIT（Mass-Editing Memory, Meng et al. 2022，定位-闭式解路线）。两者是模型编辑的两条不同技术路线，博客需显式澄清。
> 输出：`memit_blog/index.html`。风格：venus 配方 D 樱吹雪（Sakura Storm）+ 紧凑行文。

## 用户硬约束
减少废话（延续）；深度维持；**评审代理设为只读**（上轮 e2e-TTT 出现评审代理并发写文件导致的编辑冲突事故）。

## 章节设计（14 章）
1 问题定义：四性质 + ES/DD 指标（Eq1；Theresa May→Boris Johnson 例子）· 2 三条旧路失败（FT 过拟合 / ENN 双层优化不可扩展 / KE rank-1 hypernetwork；Table 1 + Fig3/4 显存）· 3 核心洞察：MLP 梯度是 rank-1（App D 证明链）· 4 MEND 架构（Eq2-3：分解→g:O(d)→O(d)；FiLM 式 s/o；按形状共享；identity init；α_ℓ）· 5 训练（Alg1/2；无高阶梯度；L_e+L_loc, c_e=0.1）· 6 主结果 I 大模型（Table 3；KE 崩溃；T5 drawdown footnote 取证 F1）· 7 主结果 II 小模型+批量（Table 4/5；ENN 竞争力；k=25: 96%）· 8 消融（Table 6：norm/ID init 命门 0.02/0.27；only-smaller scaling 启示；attention<MLP Table 9；caching Table 11）· 9 批判×8 · 10 理论：编辑谱系坐标（intrinsic/extrinsic；与 locate-then-edit、D2L rank 容量、TTT-E2E 内环的桥）· 11 科研问题×5 · 12 路线图+代码×4 · 13 结语

## 取证清单（8 条，均溯源）
F1 T5 drawdown footnote（"may occur because not fully converged…task specification"——11B 头条的 locality 度量偏软）· F2 "Scales to 10B" 是单卡环境相对 claim（A40/bfloat16）· F3 KE 失败归因是 We hypothesize 无隔离实验 · F4 Wikitext 等价邻域=前缀截断启发式（跨数据集 generality 口径不一致）· F5 MEND 批量 DD 随 k 恶化 0.002→0.012（6×）· F6 locality KL 在标签 token 上近似（脚注 6 自认非原则性）· F7 norm/ID init 才是命门（No norm ES 0.02）却被归为"实现细节" · F8 ENN 复现差异（单步内环、简化损失）。

## 关键数字（已核对）
Table 3：GPT-Neo 0.81/0.057 · GPT-J 0.88/0.031 · T5-XL 0.88/0.001 · T5-XXL 0.89/<0.001；KE 大模型全崩（0.00-0.04）。Table 4：ENN 0.99/0.99/0.93 vs MEND >0.99/0.98/0.86。Table 5：k=25 ENN 0.35/MEND 0.89；k=125 0.11/0.67。Table 6：No norm 0.02/0.370 · No ID 0.27/0.898 · only-smaller 0.80/0.593。Table 9：attention 编辑全面差于 MLP。Table 11：caching Wikitext ES 0.001。

## 验收
- [x] 4 张裁剪 verify=OK（fig1 经 image-bbox 精确定位）
- [ ] 公式 Eq1-9 + Alg1/2 核对 · 每章 ≥2 深度元素 · ≥5 SVG
- [ ] 自博弈（只读）回填 · 浏览器验证 · ACCEPTANCE/FINAL
