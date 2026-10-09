# BLOG_PLAN.md — TTT-E2E 深度阅读博客

> 论文：End-to-End Test-Time Training for Long Context, arXiv:2512.23675v2（2025-12-31），Astera/NVIDIA/Stanford/Berkeley/UCSD（Yu Sun 组）。29 页。
> 输出：`e2ettt_blog/index.html`。风格：venus 配方 C（希腊暖金）+ 紧凑行文（用户"减少废话"约束延续）。

## 方法一句话
长上下文 = 持续学习问题：标准 SWA Transformer，测试时在上下文上做 NTP（内环，更新最后 1/4 块的 MLP），元学习外环优化 TTT 后的最终损失（grad-of-grad）。双向 E2E：测试时（NTP 替代 TTT-KVB 的逐层重建）+ 训练时（元学习替代 dynamic evaluation）。

## 章节设计（15 章）
1 问题重构 · 2 玩具+TTT（Eq1-2）· 3 E2E 元学习（Eq3-4）· 4 mini-batch+SWA+三细节（Eq5-6）· 5 另一条推导：KVB 三步（Eq7-9+Table1）· 6 上下文 scaling+Fig9 伪影 · 7 compute scaling（边界 760M/48B）· 8 token 分解与"专注当下" · 9 NIAH 诚实失败 · 10 效率全景 · 11 批判×8 · 12 记忆层级+五容器谱系 · 13 科研问题×5 · 14 路线图+代码×4 · 15 结语

## 取证清单
F1 摘要叙事 vs NIAH 惨败（Table 2：S-NIAH-1@128K FA 0.99 vs TTT-E2E 0.06）· F2 "RNN 32K 后退化"部分是微调批次方差伪影（Fig9 自释）· F3 tokenizer/数据 recency 轶闻非系统研究 · F4 终步 −0.001 低于自设 0.001 显著性阈值 · F5 训练延迟 8K 慢 3.4×+checkpointing log(T)；蒸馏初始化与 E2E 叙事张力 · F6 DCLM 只保留 ≥8K 文档（避免边界重置 MLP）· F7 LR 只对 FA 网搜（4e-4 全用）· F8 双 MLP 安全存储无单独消融（与 1/4 层耦合）。

## 关键数字（已核对）
Table 1（760M/DCLM/8K）：SWA 2.827 · KVB 2.818(−0.009) · 简化 2.819(+0.001) · all-layers-MH 2.806(−0.013) · E2E 2.805(−0.001)；状态 88M vs 18M（5×）；prefill 0.0086 vs 0.017 s/1k tok。k=8K 时 TTT-E2E 在 FA 之上仍 +0.018。b=8K（无 TTT）：E2E 2.825/KVB 2.826 vs FA 2.827。层数：1/3 层不 scale、6/12 层 scale、12≈6。NIAH S-NIAH-1@128K：FA 0.99 · SWA 0.07 · M2 0.07 · GDN 0.03 · KVB 0.01 · E2E 0.06。训练延迟：@128K 快 1.2×、@8K 慢 3.4×。3B/164B（3× 基础 token）。

## 验收
- [ ] 公式 Eq1-9 PDF 提取核对 · 8 张裁剪 verify=OK（已完成）
- [ ] 每章 ≥2 深度元素、无废话 · ≥5 自绘 SVG（规划 7）
- [ ] 自博弈 ≥1 轮回填 · 浏览器验证 · ACCEPTANCE/FINAL
