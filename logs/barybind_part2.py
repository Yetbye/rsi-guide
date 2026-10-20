# -*- coding: utf-8 -*-
"""part 2: ch6-10 — 全景 / Prop 3.1 / MWB loss / Thm 3.2 / 误差界成色"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P2 = r'''
<!-- ============ 6 ============ -->
<section id="s6">
<div class="kicker">CHAPTER 06 &middot; 全景</div>
<h2>BaryBind 两阶段：先把老大送去重心，再做体积对齐</h2>
<p>论文 Fig 3 的结构可以直接翻译成两步：</p>
<div class="svgbox">
<svg viewBox="0 0 940 340" xmlns="http://www.w3.org/2000/svg" font-family="'Noto Sans SC',sans-serif">
<defs><marker id="a2" markerWidth="10" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0,10 4,0 8" fill="#7A3B2E"/></marker>
<marker id="a3" markerWidth="10" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0,10 4,0 8" fill="#2F6E75"/></marker></defs>
<text x="235" y="34" text-anchor="middle" font-size="15" font-weight="700" fill="#7A3B2E">阶段一：WB 优化</text>
<rect x="60" y="52" width="350" height="120" rx="12" fill="#F5EDE0" stroke="#C15B36" stroke-width="2"/>
<circle cx="130" cy="112" r="18" fill="#B5893F"/><text x="130" y="117" text-anchor="middle" font-size="12" fill="#fff">m₀</text>
<text x="130" y="152" text-anchor="middle" font-size="11.5" fill="#5F4B3B">初始化器</text>
<line x1="152" y1="112" x2="255" y2="112" stroke="#7A3B2E" stroke-width="2.5" marker-end="url(#a2)"/>
<text x="203" y="102" text-anchor="middle" font-size="11" fill="#7A3B2E">T&#952;</text>
<circle cx="290" cy="112" r="20" fill="#7A3B2E"/><text x="290" y="117" text-anchor="middle" font-size="12" fill="#fff">b</text>
<text x="290" y="152" text-anchor="middle" font-size="11.5" fill="#5F4B3B">WB 锚点</text>
<circle cx="365" cy="82" r="11" fill="#2F6E75"/><circle cx="365" cy="112" r="11" fill="#C15B36"/><circle cx="365" cy="142" r="11" fill="#B5893F"/>
<text x="365" y="172" text-anchor="middle" font-size="11" fill="#5F4B3B">&#123;&#8493;&#8474;&#125; 联合拉</text>
<line x1="420" y1="112" x2="505" y2="112" stroke="#2F6E75" stroke-width="2.5" marker-end="url(#a3)"/>
<text x="705" y="34" text-anchor="middle" font-size="15" font-weight="700" fill="#2F6E75">阶段二：体积对齐</text>
<rect x="535" y="52" width="350" height="240" rx="12" fill="#F5EDE0" stroke="#2F6E75" stroke-width="2"/>
<line x1="620" y1="220" x2="720" y2="110" stroke="#7A3B2E" stroke-width="2.2"/>
<circle cx="720" cy="110" r="11" fill="#7A3B2E"/><text x="732" y="102" font-size="11" fill="#7A3B2E">b</text>
<line x1="620" y1="220" x2="660" y2="120" stroke="#2F6E75" stroke-width="1.8"/><circle cx="660" cy="120" r="8" fill="#2F6E75"/>
<line x1="620" y1="220" x2="700" y2="165" stroke="#C15B36" stroke-width="1.8"/><circle cx="700" cy="165" r="8" fill="#C15B36"/>
<line x1="620" y1="220" x2="760" y2="170" stroke="#B5893F" stroke-width="1.8"/><circle cx="760" cy="170" r="8" fill="#B5893F"/>
<polygon points="720,110 660,120 700,165" fill="#2F6E75" opacity="0.18"/>
<polygon points="720,110 700,165 760,170" fill="#C15B36" opacity="0.18"/>
<circle cx="620" cy="220" r="5" fill="#33241A"/><text x="608" y="238" font-size="11" fill="#33241A">原点</text>
<text x="715" y="255" text-anchor="middle" font-size="12.5" fill="#5F4B3B">barycenter simplex：顶点 b</text>
<text x="715" y="275" text-anchor="middle" font-size="12.5" fill="#5F4B3B">体积小 = 对齐好</text>
<text x="470" y="200" text-anchor="middle" font-size="12" fill="#2F6E75">对比</text>
</svg>
<p style="font-size:12.5px;color:#8C7663;margin-top:8px;text-align:center">图 1（自绘）：BaryBind 两阶段——WB 优化把初始化器映射成重心锚点；体积对齐用重心单纯形把各模态聚到锚点。</p>
</div>

<div class="mathcard"><h4>式 (5)：多模态 WB 问题（3）的可学习形式</h4>
$$\mathcal{L}_{\mathrm{MWB}}^{*}=\inf_{\mathbb{Q}\in\mathcal{P}(\mathcal{M}_B)}\sum_{k=1}^{K}\lambda_k\, W(\mathbb{P}_k,\mathbb{Q})$$
<p class="note">$\mathbb{P}_k$：第 $k$ 个模态编码特征 $\mathbf{m}_k\in\mathcal{M}_k\subset\mathcal{M}\subset\mathbb{R}^D$
的分布；$\mathbf{m}_0$ 是锚模态特征，也是 WB 初始化器（实践中取所有可用模态特征的算术均值）。
直接优化式 (5) 不可行——$\mathbb{Q}$ 是无穷维测度，$W$ 本身还要解一个 OT。所以必须走向对偶。</p></div>
</section>

<!-- ============ 7 ============ -->
<section id="s7">
<div class="kicker">CHAPTER 07 &middot; Prop 3.1</div>
<h2>Prop 3.1 逐步复推：从 inf 问题到 sup-inf 对偶</h2>
<p>这是全篇第一个理论核心。<b>命题</b>：多模态 WB 问题 (3) 的下确界值可写成</p>
<div class="mathcard"><h4>式 (6)：Prop 3.1（对偶形式）</h4>
$$\mathcal{L}^{*}_{\mathrm{MWB}}=\sup_{\sum_k\lambda_k f_k=0}\ \inf_{\mathbb{Q}\in\mathcal{P}(\mathcal{M}_B)}\sum_{k=1}^{K}\lambda_k\ \mathbb{E}_{\mathbf{m}_k\sim\mathbb{P}_k,\ \mathbf{b}\sim\mathbb{Q}}\big[\|\mathbf{m}_k-\mathbf{b}\|-f_k(\mathbf{b})\big]$$
<p class="note">supremum 遍历势函数 $f_k:\mathcal{M}_B\to\mathbb{R}$，但受约束 $\sum_k\lambda_k f_k=0$（一致性条件）。
对偶的意义：把「找无穷维分布 $\mathbb{Q}$」换成「找 $K$ 个标量函数 $f_k$」——后者可以用 MLP 参数化。</p></div>

<h3>Step 1：写出 inf-sup 形式与 $c$-transform</h3>
<div class="mathcard"><h4>式 (7)：对偶展开（附录 A.1 式 13）</h4>
$$\mathcal{L}^{*}=\inf_{\mathbb{Q}\in\mathcal{P}(\mathcal{M}_B)}\sup_{f_{0},\dots,f_{K}}\underbrace{\sum_{k=1}^{K}\lambda_k\Big\{\int_{\mathcal{M}_k}f_k^{C_k}(\mathbf{m}_k)\mathrm{d}\mathbb{P}_k+\int_{\mathcal{M}_B}f_k(\mathbf{b})\mathrm{d}\mathbb{Q}(\mathbf{b})\Big\}}_{\triangleq\widetilde{\mathcal{F}}(\mathbb{Q},f_{1:K})}$$
<p class="note">$f_k^{C_k}$ 是式 (2) 的 $c$-transform。第一项是「源侧」期望（只依赖 $\mathbb{P}_k$），
第二项是「目标侧」期望（依赖 $\mathbb{Q}$）。这一式是 Kantorovich 对偶在 barycenter 问题上的直接套用。</p></div>

<h3>Step 2：用 Sion 交换 inf/sup</h3>
<p>由第 5 章三条前提（$\mathbb{Q}$ 域紧凸、$\widetilde{\mathcal{F}}$ 对 $\mathbb{Q}$ 线性、对 $f$ 凹），
Sion 允许交换，得到 sup-inf 形式。交换后把 $\inf_{\mathbb{Q}}$ 收拢进一个「inf over b」：</p>
<div class="mathcard"><h4>式 (8)：交换后（附录 A.1 式 16）</h4>
$$\mathcal{L}^{*}=\sup_{f_{1:K}}\Big\{\sum_{k=1}^{K}\lambda_k\int_{\mathcal{M}_k}f_k^{C_k}(\mathbf{m}_k)\mathrm{d}\mathbb{P}_k+\inf_{\mathbf{b}\in\mathcal{M}_B}\bar{f}(\mathbf{b})\Big\},\qquad \bar{f}:=\sum_k\lambda_k f_k$$
<p class="note">关键化简：$\inf_{\mathbb{Q}}\int\bar f\,\mathrm{d}\mathbb{Q}=\inf_{\mathbf{b}}\bar f(\mathbf{b})$
——因为 $\mathbb{Q}$ 上的积分下确界由 Dirac 质点 $\delta_{\mathbf{b}}$ 达到（测度的下确界在退化分布上取到）。</p>
<div class="cf">反事实：若不把 $\inf_{\mathbb{Q}}$ 收成 $\inf_{\mathbf{b}}$，就得同时优化一个测度与 $K$ 个函数，
计算上无法用梯度下降做。收成点值，才让「每个 batch 采样一个 $\mathbf{b}$」成为合法的蒙特卡洛估计。</div></div>

<h3>Step 3：一致性条件 $\sum_k\lambda_k f_k=0$ 从哪来</h3>
<p>这是最容易被跳过的一步。论文要证明：supremum 可以限制在满足 $\sum_k\lambda_k f_k=0$ 的势函数上。
做法是构造一个「一致化」的势：</p>
<div class="mathcard"><h4>式 (9)：一致化构造（附录 A.1 式 17）</h4>
$$(\tilde f_0,\dots,\tilde f_K)=\Big(f_0,\dots,f_{K-1},\ f_K-\frac{\bar f}{\lambda_K}\Big)$$
<p class="note">把最后一个势减去 $\bar f/\lambda_K$，则新的加权和
$\sum_k\lambda_k\tilde f_k=\bar f-\bar f=0$，正好满足一致性。论文进一步证 $\widetilde{\mathcal{L}}(\tilde f)\ge\widetilde{\mathcal{L}}(f)$
（用 $c$-transform 的单调性 + $\bar f\ge M:=\inf_{\mathbf{b}}\bar f$），所以限制到一致势函数不损失最优值。</p>
<div class="cf">反事实：若不做一致化，$\inf_{\mathbf{b}}\bar f(\mathbf{b})$ 项会在 sup 里被 $\bar f\to-\infty$
驱动，导致对偶值发散（下界消失）。一致化正是把这个「自由平移」方向锁死，让 supremum 有限。</div></div>

<h3>Step 4：得到最终 sup-inf</h3>
<div class="mathcard"><h4>式 (10)：由 $c$-transform 回代（附录 A.1 式 19-20）</h4>
$$\mathcal{L}^{*}=\sup_{\sum_k\lambda_k f_k=0}\sum_{k=1}^{K}\lambda_k\inf_{\mathbf{b}\in\mathcal{M}_B}\int_{\mathcal{M}_k}\big[C_k(\mathbf{m}_k,\mathbf{b})-f_k(\mathbf{b})\big]\mathrm{d}\mathbb{P}_k(\mathbf{m}_k)$$
$$\Downarrow\ \text{（取 } C_k=\|\mathbf{m}_k-\mathbf{b}\|,\ \text{交换 }\sum\text{ 与 }\inf,\ \text{用 }\mathbb{Q}\text{ 采样}\mathbf{b}）$$
$$=\sup_{\sum_k\lambda_k f_k=0}\ \inf_{\mathbb{Q}\in\mathcal{P}(\mathcal{M}_B)}\sum_{k=1}^{K}\lambda_k\ \mathbb{E}_{\mathbf{m}_k\sim\mathbb{P}_k,\ \mathbf{b}\sim\mathbb{Q}}\big[\|\mathbf{m}_k-\mathbf{b}\|-f_k(\mathbf{b})\big]\quad\blacksquare$$
<p class="note">三处工程化：① 积分换成经验期望（mini-batch）；② 成本取 $C_k=\|\mathbf{m}_k-\mathbf{b}\|$（欧氏，
对应 Wasserstein 距离）；③ 交换 $\sum$ 与 $\inf$——合法，因为 $\mathbf{b}$ 被所有项共享且目标对 $\mathbf{b}$ 线性。</p></div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>对偶「换来」了什么，「代价」是什么</h4>
<p><b>换来</b>：无穷维测度 $\mathbb{Q}$ 变成 $K$ 个函数 $f_k$；梯度下降可做；每 batch 只需采样 $\mathbf{b}$。
<b>代价</b>：sup-inf 是<b>极大极小</b>问题，不是单边凸优化——$f_k$ 要往上推（对抗），
$T_\theta$ 要往下压。这正是第 8 章的交替优化，也是整个方法最不稳定的来源。
换句话说，对偶把「难算」换成了「难训」——这是所有神经 OT 方法（包括本文引用的神经 OT 重心估计
[47][50][53]）共同的债务。</p></div>
</section>

<!-- ============ 8 ============ -->
<section id="s8">
<div class="kicker">CHAPTER 08 &middot; MWB loss</div>
<h2>把对偶变成网络：$T_\theta$、$f_\omega$ 与交替优化</h2>
<p>有了式 (10)，就能参数化了。BaryBind 用一个可训练的<b>重心映射</b>
$T_\theta:\mathcal{M}_0\to\mathcal{M}_B$ 来采样重心特征 $\mathbf{b}=T_\theta(\mathbf{m}_0)$，
用 $K$ 个 MLP $g_{\omega_k}:\mathbb{R}^D\to\mathbb{R}$ 参数化势函数。</p>

<div class="mathcard"><h4>式 (11)：MWB loss（式 5，max-min）</h4>
$$\max_{\omega_{1:K}}\min_{\theta}\ \mathcal{L}_{\mathrm{MWB}}(\omega_{1:K},\theta)\triangleq\sum_{k=1}^{K}\lambda_k\ \mathbb{E}_{\mathbf{m}_k\sim\mathbb{P}_k}\big[\|\mathbf{m}_k-T_\theta(\mathbf{m}_0)\|-f_{\omega_k}(T_\theta(\mathbf{m}_0))\big]$$
<p class="note"><b>势函数的一致性参数化</b>（常见技巧，见 [26][23][24]）：
$f_{\omega_k}=g_{\omega_k}-\sum_{i=1}^{K}\lambda_i g_{\omega_i}$，这样 $\sum_k\lambda_k f_{\omega_k}=0$
<b>自动成立</b>——不需要在损失里显式加约束，一致化被「焊」进了参数化。这是实践中保证 Prop 3.1 前提的最关键一步。</p></div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>初始化器 $\mathbf{m}_0$ 是「热启动」，不是「中心」</h4>
<p>$T_\theta$ 取 $\mathbf{m}_0$ 为输入，但它吃的是<b>所有 $K$ 个模态</b>给的梯度（因为损失里是对
$\mathbf{m}_k$ 求期望、$k=1..K$ 全都参与）。所以尽管起点可能是文本或视频的特征，优化方向会
<b>把输出拽离任何单一模态的流形</b>、朝几何中心走。这正是论文附录 B.7 强调的鲁棒性来源：
换成视频初始化、文本初始化、或 T+V+A 算术融合初始化，加了 WB 优化后都能涨点
（VGGSound V+A：55.2/55.6/55.8），说明贡献在 <b>WB 公式本身</b>，不在初始化选择。</p></div>

<h3>交替优化与梯度的方向</h3>
<p>训练是两塔交替：$\omega_{1:K}$ 做 <b>最大化</b>（对偶势，对抗地压低可实现的传输成本），
$\theta$ 与其他网络做 <b>最小化</b>。梯度写开是：</p>
<div class="mathcard"><h4>式 (12)：$T_\theta$ 的梯度（直觉形式）</h4>
$$\nabla_\theta\mathcal{L}_{\mathrm{MWB}}=\sum_{k=1}^{K}\lambda_k\ \mathbb{E}_{\mathbf{m}_k}\Big[\frac{T_\theta(\mathbf{m}_0)-\mathbf{m}_k}{\|\mathbf{m}_k-T_\theta(\mathbf{m}_0)\|}-\nabla_\theta f_{\omega_k}(T_\theta(\mathbf{m}_0))\Big]\cdot\frac{\partial T_\theta(\mathbf{m}_0)}{\partial\theta}$$
<p class="note">第一项把 $\mathbf{b}$ 拉向所有 $\mathbf{m}_k$ 的加权平均方向（数据项，如同质心力）；
第二项由对抗势 $f_{\omega_k}$ 给出（对抗项，防止 $\mathbf{b}$ 塌到任一模态）。
两者平衡的结果，就是「不偏向任何模态的中心」。</p>
<div class="cf">反事实：若去掉势项 $f$（只留 $\sum\lambda_k\|\mathbf{m}_k-\mathbf{b}\|$），
$\mathbf{b}$ 会塌向 $\mathbf{m}_k$ 的欧氏质心，退化成「特征平均」——没有分布层面的结构，
也无法对应 Wasserstein 重心。消融（第 16 章 Table 5）显示去掉 MWB 后各项普遍掉点，印证了势项的必要性。</div></div>
</section>

<!-- ============ 9 ============ -->
<section id="s9">
<div class="kicker">CHAPTER 09 &middot; Thm 3.2</div>
<h2>Thm 3.2 逐步复推：两个对偶 gap 与 $W^2$ 误差界</h2>
<p>第二个理论核心是<b>误差分析</b>：学到的分布 $\widehat{T}_{\#}\mathbb{P}_0$ 离真重心 $\mathbb{Q}^*$ 有多远？
定理用两个「对偶 gap」来界定。</p>

<div class="mathcard"><h4>式 (13)：简记（式 6）</h4>
$$\mathcal{F}(f_{1:K},T):=\mathcal{L}_{\mathrm{MWB}}(f_{1:K},T),\quad \mathcal{L}(f_{1:K}):=\inf_{T}\mathcal{F}(f_{1:K},T),\quad \mathcal{L}^{*}:=\mathcal{L}_{\mathrm{MWB}}^{*}$$
<p class="note">$\mathcal{F}$ 是「给定势与映射」的总成本；$\mathcal{L}(f)$ 是「固定势、对映射取 inf」；
$\mathcal{L}^*$ 是真正的最优值（双取 inf）。</p></div>

<div class="mathcard"><h4>式 (14)：定理 3.2（误差界）</h4>
<p class="note">设成本 $C_k$ 任意，假设映射 $\mathbf{b}\mapsto C_k(\mathbf{m}_k,\mathbf{b})-\widehat f_k(\mathbf{b})$
对 $\mathbf{m}_k\in\mathcal{M}_k$ 是 <b>$\beta$-强凸</b>的。定义两个对偶 gap：</p>
$$\mathcal{E}_1(\widehat f,\widehat T)=\mathcal{F}(\widehat f,\widehat T)-\mathcal{L}(\widehat f),\qquad \mathcal{E}_2(\widehat f)=\mathcal{L}^{*}-\mathcal{L}(\widehat f)$$
$$\Longrightarrow\quad W^{2}\big(\widehat T_{\#}\mathbb{P}_0,\ \mathbb{Q}^{*}\big)\ \le\ \frac{4}{\beta}\big(\mathcal{E}_1+\mathcal{E}_2\big)$$</div>

<h3>两个 gap 的含义</h3>
<div class="insight-box"><span class="tag">深度洞察</span>
<h4>$\mathcal{E}_1$ 是「优化 gap」，$\mathcal{E}_2$ 是「表达 gap」</h4>
<p>$\mathcal{E}_1=\mathcal{F}(\widehat f,\widehat T)-\inf_T\mathcal{F}(\widehat f,T)$：给定你选的势 $\widehat f$，
你的映射 $\widehat T$ 比「最优映射」差多少——这是<b>训练没训好</b>（映射优化不足）。
$\mathcal{E}_2=\mathcal{L}^*-\mathcal{L}(\widehat f)=\mathcal{F}(\widehat f,T^*)-\mathcal{F}(\widehat f,T^{f})$：
你的势 $\widehat f$ 本身离最优势多远——这是<b>势函数表达不足</b>（网络容量/对偶没解够）。
两个 gap 加起来，就是「我们离真重心的全部距离」。</p>
<p>这与 PAC 学习的「近似误差 + 估计误差」分解、以及统计学习的 bias-variance 分解是同构的：
$\mathcal{E}_2$ ≈ bias（表达力），$\mathcal{E}_1$ ≈ variance/优化误差。不同处在于这里是确定性的
对偶 gap，不是概率的。</p></div>

<h3>Step-by-step：常数 $4/\beta$ 从哪来</h3>
<div class="mathcard"><h4>式 (15)：强凸 $\Rightarrow$ 二次下界（附录 A.2）</h4>
<p class="note">记 $g_k(\mathbf{m}_k,\mathbf{b}):=C_k(\mathbf{m}_k,\mathbf{b})-\widehat f_k(\mathbf{b})$，
由假设对 $\mathbf{b}$ 是 $\beta$-强凸的。强凸函数满足二次下界：
$g_k(\mathbf{b}')\ge g_k(\mathbf{b})+\langle\nabla g_k(\mathbf{b}),\mathbf{b}'-\mathbf{b}\rangle+\frac{\beta}{2}\|\mathbf{b}'-\mathbf{b}\|^2$。</p>
$$\mathcal{E}_1\ge\frac{\beta}{2}\,\mathbb{E}_{\mathbf{m}_0}\big\|\widehat T(\mathbf{m}_0)-T^{f}(\mathbf{m}_0)\big\|^{2},\qquad \mathcal{E}_2\ge\frac{\beta}{2}\,\mathbb{E}_{\mathbf{m}_0}\big\|T^{f}(\mathbf{m}_0)-T^{*}(\mathbf{m}_0)\big\|^{2}$$
<p class="note">$T^f$ 是给定 $\widehat f$ 时的最优映射（一阶变分为 0，见式 31）；$T^*$ 是真 OT 映射。
两式都是「gap $\ge \frac{\beta}{2}$ 乘以映射偏差的平方期望」——强凸把「目标差」转成「参数差的平方」。</p></div>

<div class="mathcard"><h4>式 (16)：合并与 $W^2$ 桥（附录 A.2 式 34）</h4>
$$\mathcal{E}_1+\mathcal{E}_2\ge\frac{\beta}{2}\mathbb{E}\|\widehat T-T^{f}\|^{2}+\frac{\beta}{2}\mathbb{E}\|T^{f}-T^{*}\|^{2}\ \ge\ \frac{\beta}{4}\mathbb{E}\|\widehat T-T^{*}\|^{2}$$
$$\ge\frac{\beta}{4}W^{2}\big(\widehat T_{\#}\mathbb{P}_0,\ T^{*}_{\#}\mathbb{P}_0\big)=\frac{\beta}{4}W^{2}\big(\widehat T_{\#}\mathbb{P}_0,\ \mathbb{Q}^{*}\big)$$
<p class="note"><b>常数推导</b>：第一步到第二步用了「$\|a\|^2+\|b\|^2\ge\frac12\|a+b\|^2$」（平行四边形/凸性），
把两个平方期望合成一个 $\|\widehat T-T^*\|^2$，系数从 $\beta/2$ 变 $\beta/4$。最后一步用
Wasserstein-2 距离的定义：$W^2(\widehat T_\#\mathbb{P}_0,\mathbb{Q}^*)\le\mathbb{E}\|\widehat T-T^*\|^2$
（取传输方案为「$\mathbf{m}_0\mapsto(\widehat T(\mathbf{m}_0),T^*(\mathbf{m}_0))$」这个耦合）。
整理即得 $W^2\le\frac{4}{\beta}(\mathcal{E}_1+\mathcal{E}_2)$。</p>
<div class="cf">反事实：若不假设强凸（$\beta=0$），右侧发散，界无信息——强凸是把「对偶 gap」翻译成
「Wasserstein 距离」的唯一桥梁。这也意味着：如果神经势 $f$ 太「曲折」（不平滑），$\beta$ 会很小，
界会很松，学到的重心可能离真重心很远（见下一章的成色讨论）。</div></div>
</section>

<!-- ============ 10 ============ -->
<section id="s10">
<div class="kicker">CHAPTER 10 &middot; 误差界成色</div>
<h2>误差界的成色：$\beta$-强凸假设站得住吗</h2>
<p>定理 3.2 干净，但它的<strong>前提</strong>值得较真：映射 $\mathbf{b}\mapsto C_k-\widehat f_k$ 是
$\beta$-强凸的。这个假设在真实设定里成色如何？这一章把它拆开，并发散到 OT 的曲率视角。</p>

<h3>$C_k$ 部分：欧氏范数的凸性</h3>
<p>$C_k(\mathbf{m}_k,\mathbf{b})=\|\mathbf{m}_k-\mathbf{b}\|$ 对 $\mathbf{b}$ 是凸的，但<strong>不是强凸</strong>
（欧氏范数在 $\mathbf{b}=\mathbf{m}_k$ 处不可导，Hessian 在射线方向为 0）。真正提供强凸的是
$-\widehat f_k(\mathbf{b})$：如果神经势 $f_k$ 是<strong>强凹</strong>的，那么 $-f_k$ 强凸，两者相加强凸。</p>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>$\beta$ 来自势函数的曲率，不是来自成本</h4>
<p>换句话说，误差界的松紧由<strong>学习到的势有多平滑</strong>决定。论文自己也点出：
「在欧氏成本下，这个局部条件在神经势足够光滑时成立；实践里用正则（如 weight decay）提高平滑性」。
这是诚实的——它承认强凸是<strong>一个需要满足的设计目标</strong>，不是自动成立的性质。
一个诚实的读法是：Thm 3.2 给的是<strong>条件性保证</strong>（conditional guarantee），
不是无条件的收敛定理。</p>
<p>发散：这与最优传输里「熵正则」的思路同源——Sinkhorn 用熵项让传输问题强凸可解，
代价是引入 bias。BaryBind 用 weight decay 让势平滑，也是在「可解性」与「保真」之间取平衡。
两者都是<strong>正则化换凸性</strong>。</p></div>

<h3>发散：Wasserstein-2 空间的正曲率与均值唯一性</h3>
<p>为什么这里必须小心？因为 $\mathcal{P}_2(\mathbb{R}^d)$ 配 $W_2$ 是一个<strong>非负 Alexandrov 曲率</strong>
空间。在正曲率空间里，Fréchet 均值（重心）一般<strong>存在但不唯一</strong>——多解对应多个局部谷。
这就解释了两件事：</p>
<div class="svgbox">
<svg viewBox="0 0 940 260" xmlns="http://www.w3.org/2000/svg" font-family="'Noto Sans SC',sans-serif">
<text x="235" y="34" text-anchor="middle" font-size="14" font-weight="700" fill="#7A3B2E">平坦空间：均值唯一</text>
<circle cx="120" cy="120" r="10" fill="#2F6E75"/><circle cx="320" cy="120" r="10" fill="#C15B36"/><circle cx="220" cy="120" r="12" fill="#7A3B2E"/>
<text x="220" y="160" text-anchor="middle" font-size="12" fill="#5F4B3B">算术均值 = 唯一 Fréchet 均值</text>
<line x1="220" y1="120" x2="220" y2="200" stroke="#B5893F" stroke-width="1" stroke-dasharray="3 3"/>
<text x="705" y="34" text-anchor="middle" font-size="14" font-weight="700" fill="#2F6E75">正曲率空间：均值可能不唯一</text>
<path d="M540,150 Q600,70 660,150" fill="none" stroke="#2F6E75" stroke-width="2.5"/>
<circle cx="560" cy="118" r="10" fill="#C15B36"/><circle cx="740" cy="118" r="10" fill="#B5893F"/>
<circle cx="620" cy="128" r="11" fill="#7A3B2E"/><circle cx="680" cy="128" r="11" fill="#7A3B2E"/>
<text x="650" y="205" text-anchor="middle" font-size="12" fill="#5F4B3B">W₂ 空间正曲率 → 多个局部重心</text>
<text x="650" y="228" text-anchor="middle" font-size="12" fill="#5F4B3B">（此处画出两个候选）</text>
</svg>
<p style="font-size:12.5px;color:#8C7663;margin-top:8px;text-align:center">图 2（自绘）：平坦空间均值唯一 vs 正曲率（Wasserstein-2）空间均值可能不唯一。</p>
</div>

<p>推论有两条：<strong>①</strong> WB 的唯一性需要额外条件（如各 $\mathbb{P}_k$ 落在一个凸测地球内），
论文用「存在近似」而非「唯一」的语言是恰当的；<strong>②</strong> Thm 3.2 的界是相对
<strong>某个</strong> $\mathbb{Q}^*$ 的，若真重心本身不唯一，界衡量的是「到最近/某个重心」的距离。</p>

<div class="critique-box"><span class="tag">C1 · 取证</span>
<h4>Thm 3.2 的 $\beta$-强凸是条件性假设，不是被验证的性质</h4>
<p><strong>证据</strong>：定理陈述「Assume that the maps ... are $\beta$-strongly convex」，正文补充
「欧氏成本下这个局部条件在神经势足够光滑时成立」，并建议用 weight decay。但论文<strong>没有</strong>给出
学到的 $\widehat f_k$ 的实测曲率（Hessian 最小特征值），也没有消融「加/不加 weight decay」对
$W^2(\widehat T_\#\mathbb{P}_0,\mathbb{Q}^*)$ 的影响。</p>
<p><strong>影响</strong>：界是<b>条件性的</b>（若强凸则...），读者不能把它当成「BaryBind 必然收敛到真重心」。
它是一张「如果条件满足就有保证」的路线图，不是安全气囊。</p>
<p><strong>补救</strong>：补一组实验——记录训练过程中 $\widehat f_k$ 的 Hessian 最小特征值，
或直接用 Sinkhorn 对小规模问题算出真 $\mathbb{Q}^*$，实测 $W^2(\widehat T_\#\mathbb{P}_0,\mathbb{Q}^*)$
并对照 $\frac{4}{\beta}(\mathcal{E}_1+\mathcal{E}_2)$，看界是否紧（而不是只看检索指标涨了）。</p></div>
</section>

'''

io.open(r'D:\success\RSI\blogs\barybind\_part2.html','w',encoding='utf-8').write(P2)
print('part2 written:', len(P2))
