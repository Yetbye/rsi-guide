# -*- coding: utf-8 -*-
"""BaryBind 深度解读 — 理论发散版 (part 1: head + hero + ch1-5)
按项目约定的 Venus 暖白陶土配方；组件用 .mathcard/.insight-box/.cf/.critique-box/
.research-question/.svgbox/.roadmap（与系列一致）。
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
CSS = io.open(r'D:\success\RSI\_bb_css.txt', encoding='utf-8').read()

HEAD = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BaryBind 深度解读 | 用 Wasserstein 重心绑定多模态：理论、对偶与体积几何</title>
<script>
window.MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
''' + CSS + r'''
</style>
</head>
<body>
<nav class="nav"><div class="nav-inner">
  <div class="nav-logo">BaryBind <em>&middot;</em> 深度解读</div>
  <div class="nav-links">
    <a href="#s1">症状</a><a href="#s2">n&#8805;3 困境</a><a href="#s3">OT 谱系</a><a href="#s4">重心直觉</a><a href="#s5">对偶与 Sion</a>
    <a href="#s6">全景</a><a href="#s7">Prop 3.1</a><a href="#s8">MWB loss</a><a href="#s9">Thm 3.2</a><a href="#s10">误差界成色</a>
    <a href="#s11">单纯形体积</a><a href="#s12">体积 vs 余弦</a><a href="#s13">BVC</a><a href="#s14">总目标</a>
    <a href="#s15">实验 I</a><a href="#s16">实验 II</a><a href="#s17">实验 III</a><a href="#s18">批判</a>
    <a href="#s19">科研问题</a><a href="#s20">路线图</a>
  </div>
</div></nav>

<header class="hero">
  <div class="hero-wrap">
    <div class="hero-badge">NeurIPS 2026 Oral &middot; arXiv:2609.33800 &middot; 2026</div>
    <h1>BaryBind：<span class="mark">用 Wasserstein 重心</span><br>取代模态老大，绑定多模态</h1>
    <p class="hero-tagline">最优传输对偶 &middot; 重心单纯形体积 &middot; 高阶几何对齐 &middot; 模态偏差的消除</p>
    <p class="hero-desc">CLIP 之后，把三个以上模态对齐到一个空间，主流做法是指定一个「老大」（图文或语言），
      再让其他模态两两往它靠。BaryBind 反其道而行：先用最优传输求出所有模态分布的
      <b>Wasserstein 重心</b>作为几何共识中心，再让每个模态对齐到它，并用一个以重心为顶点的
      <b>单纯形体积</b>作为全局对齐度量。这一篇把它的两块理论核心——<b>对偶问题</b>与
      <b>误差界</b>——逐步拆开、拆到底，再发散到传输对偶、曲率几何与高阶矩。</p>
    <div class="hero-stats">
      <div class="hstat"><b>55.6%</b><span>VGGSound V+A Acc@1<br>（VAST 48.1）</span></div>
      <div class="hstat"><b>-3.1%</b><span>T2V/V2T 检索差<br>（相对 VAST）</span></div>
      <div class="hstat"><b>1B</b><span>参数量<br>（VAST 骨干）</span></div>
      <div class="hstat"><b>2</b><span>理论主线<br>对偶 + 误差界</span></div>
    </div>
    <div class="scroll-hint"><span>&darr;</span>SCROLL TO READ</div>
  </div>
</header>

<main>

<!-- ============ 1 ============ -->
<section id="s1">
<div class="kicker">CHAPTER 01 &middot; 症状</div>
<h2>为什么「绑定三个模态」不能靠指定一个老大</h2>
<p>先把问题摆清楚。多模态学习的本质假设是：不同传感器（图像、文本、音频、深度）捕捉的是
<b>同一个底层现实</b>，因此它们的表示应当落在一个共享语义空间里。CLIP 用对比学习把图像-文本对齐到了这个空间，
但它的损失是<b>成对</b>（pairwise）的：InfoNCE 与 BYOL 都是在 $n=2$ 的设定下写的。一旦要同时绑定
$n\geq 3$ 个模态，成对损失就不够用了——你不可能只靠两两对齐就保证三者同时聚在一起。</p>

<p>于是「模态老大」（modality anchor）的思路出现了。ImageBind 的做法很直接：以图像为枢纽，
让音频、视频、深度、文本各自与图像做两两对齐。之后 LanguageBind、UniBind、GRAM、Triangle、OmniBind
又把枢纽换成语言或别的模态，或者用平行六面体/三角形的体积来做全局损失。VAST 进一步把模态融合进共享空间，
但监督仍以文本为中心。</p>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>锚点（anchor）本质上是把「分布的共识」误当成了「某一个模态的分布」</h4>
<p>把某个模态指定为锚点，等于假设：这个模态的分布已经等于所有模态的语义共识中心。但事实未必如此——
每个模态都是共识的一种<b>特定变换</b>，没有任何一个模态天然就是中心。强行以它为中心，会引入
<b>模态偏差</b>（modality bias）：表示空间向这个模态倾斜，其他模态被迫屈从它，最终形成不平衡的空间。</p>
<p>论文用一个可观测的症状来刻画这种不平衡：VAST 在文本→视频（T2V）与视频→文本（V2T）检索上的
Recall@1 差距很大。如果两个模态真的对称地绑定在共享空间里，这两个方向的检索成绩应当接近；
差距大，说明空间偏向了某一边。</p></div>

<p>那么有没有一个<b>不偏向任何模态</b>的中心？BaryBind 的回答是：有，它就是所有模态分布的
Wasserstein 重心（Wasserstein barycenter, WB）。它是「离所有模态分布的 Wasserstein 距离加权平均最小」的那个分布，
是真正的几何共识。这一篇要做的，就是把这个想法背后的一整套理论——从最优传输的对偶，到重心的存在性，
再到体积度量的几何含义——彻底拆开。</p>
</section>

<!-- ============ 2 ============ -->
<section id="s2">
<div class="kicker">CHAPTER 02 &middot; n&#8805;3 困境</div>
<h2>从成对对比到超边：为什么简单加损失行不通</h2>
<div class="mathcard"><h4>式 (0)：成对对比损失的原型（InfoNCE）</h4>
$$\mathcal{L}_{\mathrm{NCE}}=-\mathbb{E}\Big[\log\frac{\exp(\langle \mathbf{v}_i,\mathbf{t}_i\rangle/\tau)}{\sum_{j}\exp(\langle \mathbf{v}_i,\mathbf{t}_j\rangle/\tau)}\Big]$$
<p class="note">$\mathbf{v}_i$：图像嵌入；$\mathbf{t}_i$：文本嵌入；$\tau$：温度。这一对 $(\mathbf{v}_i,\mathbf{t}_i)$ 是一条
<b>边</b>，把两个模态往一起拉。</p>
<div class="cf">反事实：若把 $n$ 个模态两两全连，得到的是 $\binom{n}{2}$ 条边；每条边都独立最小化，但没有任何一项
<b>直接约束三者的全局几何关系</b>。三模态可能两两都近，但整体仍偏离共享中心——这正是「三角不稳」。</div></div>

<p>把 $n$ 个模态两两做对比，看似解决，实则留下一个空洞：成对相似度是<b>二阶</b>信息（只看两两夹角），
它无法刻画「三个向量是否同时聚向同一点」这种<b>高阶</b>关系。GRAM 与 Triangle 的贡献正在这里——它们用
<b>体积</b>（平行六面体或三角形的体积）作为全局度量，把 $n$ 个模态的几何关系压进一个标量。但它们的几何中心
仍取在原点，且锚点仍是特定模态。</p>

<p>BaryBind 的两条改动路线，恰好对上这两个空洞：</p>
<div class="svgbox">
<svg viewBox="0 0 940 300" xmlns="http://www.w3.org/2000/svg" font-family="'Noto Sans SC',sans-serif">
<defs><marker id="a1" markerWidth="10" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0,10 4,0 8" fill="#7A3B2E"/></marker></defs>
<rect x="30" y="40" width="380" height="200" rx="12" fill="#F5EDE0" stroke="#C15B36" stroke-width="2"/>
<text x="220" y="72" text-anchor="middle" font-size="15" font-weight="700" fill="#7A3B2E">空洞 1：中心是谁</text>
<circle cx="120" cy="170" r="14" fill="#2F6E75"/><text x="120" y="175" text-anchor="middle" font-size="11" fill="#fff">T</text>
<circle cx="220" cy="140" r="14" fill="#C15B36"/><text x="220" y="145" text-anchor="middle" font-size="11" fill="#fff">锚</text>
<circle cx="320" cy="175" r="14" fill="#B5893F"/><text x="320" y="180" text-anchor="middle" font-size="11" fill="#fff">A</text>
<circle cx="175" cy="215" r="14" fill="#7A3B2E"/><text x="175" y="220" text-anchor="middle" font-size="11" fill="#fff">V</text>
<text x="220" y="255" text-anchor="middle" font-size="12.5" fill="#5F4B3B">两两往「锚」靠 = 模态偏差</text>
<line x1="415" y1="140" x2="500" y2="140" stroke="#7A3B2E" stroke-width="2.5" marker-end="url(#a1)"/>
<rect x="530" y="40" width="380" height="200" rx="12" fill="#F5EDE0" stroke="#2F6E75" stroke-width="2"/>
<text x="720" y="72" text-anchor="middle" font-size="15" font-weight="700" fill="#2F6E75">空洞 2：度量是几阶</text>
<circle cx="640" cy="165" r="13" fill="#2F6E75"/><circle cx="700" cy="135" r="13" fill="#C15B36"/><circle cx="800" cy="150" r="13" fill="#B5893F"/>
<line x1="640" y1="165" x2="700" y2="135" stroke="#7A3B2E" stroke-width="1.6" stroke-dasharray="4 3"/>
<line x1="700" y1="135" x2="800" y2="150" stroke="#7A3B2E" stroke-width="1.6" stroke-dasharray="4 3"/>
<line x1="640" y1="165" x2="800" y2="150" stroke="#7A3B2E" stroke-width="1.6" stroke-dasharray="4 3"/>
<text x="720" y="205" text-anchor="middle" font-size="12.5" fill="#5F4B3B">成对相似度 = 二阶，看不到全局</text>
<text x="720" y="255" text-anchor="middle" font-size="12.5" fill="#5F4B3B">→ 需要高阶（体积）度量</text>
</svg>
<p style="font-size:12.5px;color:#8C7663;margin-top:8px;text-align:center">图 0（自绘）：锚点对齐的两个结构性空洞——中心选择的偏差、度量阶数的不足。</p>
</div>

<p>把这两件事合起来，就能预读 BaryBind 的骨架：先用最优传输求出<b>几何共识中心</b>（WB），
再用一个以 WB 为顶点的<b>单纯形体积</b>作为全局对齐度量。接下来四章，先把这两件事的数学地基一砖一瓦铺起来。</p>
</section>

<!-- ============ 3 ============ -->
<section id="s3">
<div class="kicker">CHAPTER 03 &middot; OT 谱系</div>
<h2>数学地基 I：最优传输，从 Monge 到 Kantorovich 对偶</h2>
<p>Wasserstein 距离与重心都建立在<b>最优传输</b>（optimal transport, OT）之上。要读懂 BaryBind 的对偶
（Prop 3.1），必须先把 OT 的对偶语言说清楚。先给记号。</p>

<div class="mathcard"><h4>记号（论文 3.1 节）</h4>
<p class="note">$\bar{K}=\{1,\dots,K\}$；序列 $e_{0},\dots,e_{K}$ 记作 $e_{1:K}$。$\mathcal{X}\subset\mathbb{R}^d$、
$\mathcal{Y}\subset\mathbb{R}^{d'}$、$\mathcal{X}_k\subset\mathbb{R}^{d_k}$ 为紧子集。
$\mathcal{C}(\mathcal{X})$ 是连续实值函数空间，$\mathcal{P}(\mathcal{X})$ 是支撑在 $\mathcal{X}$ 上的概率测度集。
$\Pi(\mathbb{P},\mathbb{Q})$ 是边缘分布为 $\mathbb{P},\mathbb{Q}$ 的联合分布（传输方案）集。
$\langle\cdot,\cdot\rangle$ 表示特征余弦相似度。</p></div>

<h3>Monge 问题：搬运质量的最小成本</h3>
<p>给定 $\mathbb{P}\in\mathcal{P}(\mathcal{X})$、$\mathbb{Q}\in\mathcal{P}(\mathcal{Y})$ 与成本函数
$c:\mathcal{X}\times\mathcal{Y}\to\mathbb{R}_+$，经典 OT 问题找一个联合分布 $\pi\in\Pi(\mathbb{P},\mathbb{Q})$
最小化期望搬运成本：</p>
<div class="mathcard"><h4>式 (1)：最优传输问题</h4>
$$\mathrm{OT}_c(\mathbb{P},\mathbb{Q})\triangleq\inf_{\pi\in\Pi(\mathbb{P},\mathbb{Q})}\ \mathbb{E}_{(x,y)\sim\pi}\big[c(x,y)\big]$$
<p class="note">取 $c(x,y)=\|x-y\|$ 得到 $W(\mathbb{P},\mathbb{Q})=\inf_{\pi}\mathbb{E}_{\pi}\|x-y\|$，
即 Earth-Mover / Wasserstein 距离。注意 $\pi$ 是<b>联合分布</b>（transport plan），
允许把一个 $x$ 拆开送到多个 $y$——这比 Monge 的确定性映射 $y=T(x)$ 更一般。</p>
<div class="cf">反事实：若强行限制为确定性映射 $T$（Monge 形式），当 $\mathbb{P}$ 有原子而 $\mathbb{Q}$ 没有时
可能根本不存在可行解（质量无法拆分）。Kantorovich 放宽到联合分布，正是为了保证存在性——这也是 BaryBind
后面要用 Monge 形式 $\widehat{T}_{\#}\mathbb{P}_0=\mathbb{Q}^*$ 时必须额外假设的原因（第 9 章会回到这一点）。</div></div>

<h3>Kantorovich 对偶与 c-transform</h3>
<p>式 (1) 的原始问题（对 $\pi$ 取 inf）通过<b>线性规划对偶</b>转成对<b>势函数</b> $f,g$ 的 sup 问题。
对偶里的关键算子是 $c$-transform：</p>
<div class="mathcard"><h4>式 (2)：$c$-transform</h4>
$$f_k^{C_k}(\mathbf{m}_k)=\inf_{\mathbf{b}\in\mathcal{M}_B}\big[C_k(\mathbf{m}_k,\mathbf{b})-f_k(\mathbf{b})\big]$$
<p class="note">它把定义在「目标空间」的势 $f_k$，变成定义在「源空间」的 $f_k^{C_k}$。
直觉：$f_k^{C_k}(\mathbf{m})$ 是从 $\mathbf{m}$ 出发、扣掉势能 $f_k$ 之后能拿到的最小成本，
它是一个「下包络」。$c$-transform 对 $f_k$ 是<b>凹</b>的——这个凹性是后面交换 inf/sup 的前提。</p>
<div class="cf">反事实：若 $C_k$ 不是下半连续、$f_k$ 不连续，$c$-transform 的凹性与紧性论证会失效，
Sion 极小极大就用不了，对偶等号可能只有一边（$\le$ 或 $\ge$），Prop 3.1 的等式就不成立。</div></div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>对偶的本质：把「搬运方案」换成「势函数」</h4>
<p>原始问题是<b>组合</b>的（找一个联合分布 $\pi$），对偶问题是<b>函数</b>的（找 $K$ 个势函数 $f_k$）。
这个转换的价值是：在神经网络里，我们没法直接参数化「联合分布」，但可以轻松参数化「函数」
（一个 MLP 就是一个势函数）。BaryBind 正是把 $f_k$ 参数化成 MLP $g_{\omega_k}$，把「找联合分布」
转成「找网络」，这才让重心可以被神经网络学习出来。</p></div>
</section>

<!-- ============ 4 ============ -->
<section id="s4">
<div class="kicker">CHAPTER 04 &middot; 重心直觉</div>
<h2>数学地基 II：Wasserstein 重心，为什么它是「几何共识」</h2>
<p>有了 Wasserstein 距离，就能定义「平均」。但这里的平均不是分布的算术平均，而是
<b>在 Wasserstein 空间里的 Fréchet 均值</b>。先看定义。</p>

<div class="mathcard"><h4>式 (3)：Wasserstein 重心（WB）问题</h4>
$$\inf_{\mathbb{Q}\in\mathcal{P}(\mathcal{Y})}\ \sum_{k=1}^{K}\lambda_k\, W(\mathbb{P}_k,\mathbb{Q}),\qquad \lambda_k\ge 0,\ \sum_k\lambda_k=1$$
<p class="note">给定分布 $\mathbb{P}_{1:K}$ 与权重 $\lambda$，找一个 $\mathbb{Q}$ 使得到各分布的
Wasserstein 距离加权和最小。这个 $\mathbb{Q}$ 就是重心。它被应用到多模态隐空间 $\mathcal{M}$ 上：
第 $k$ 个模态的编码特征服从分布 $\mathbb{P}_k$，重心 $\mathbb{Q}$ 的支撑 $\mathcal{M}_B$ 含重心特征 $\mathbf{b}$。</p></div>

<h3>Fréchet 均值的 OT 版</h3>
<p>在欧氏空间里，一组点 $x_1,\dots,x_K$ 的均值是 $\arg\min_y\sum_k\lambda_k\|x_k-y\|^2$，
也即 Fréchet 均值。把「点的平方距离」换成「分布的 Wasserstein 距离」，就得到式 (3)。
所以 <b>WB 是欧氏均值在测度空间里的对应物</b>。发散一点：黎曼流形上 Fréchet 均值叫 Karcher mean，
在正曲率流形（如球面、Wasserstein 空间本身）上，均值的<b>唯一性</b>需要额外条件
（例如点都落在一个凸测地球内）。这解释了为什么 WB 一般存在但未必唯一——Wasserstein 空间
$\mathcal{P}_2(\mathbb{R}^d)$ 在 $W_2$ 下是一个非负 Alexandrov 曲率空间，均值可能不唯一
（Agueh–Carlier 2011 给出高斯情形的闭式）。</p>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>为什么重心能代表「语义共识」，而单个模态不能</h4>
<p>多模态数据是同一底层现实的异质观测，因此各模态表示可以看成「共享语义表示」的模态特定变换。
重心的定义（离所有模态分布的平均距离最小）恰好刻画了「共同部分」：任何偏向某模态的点，都会因为离
其他模态更远而增大加权距离。所以 <b>WB 是唯一不偏向任何模态的中心</b>——这就是 BaryBind 用来
消除 modality bias 的原理。</p>
<p>反事实读法：若用某模态 $\mathbb{P}_1$ 本身当锚点，加权距离 $\sum_k\lambda_k W(\mathbb{P}_k,\mathbb{P}_1)$
里有一项 $W(\mathbb{P}_1,\mathbb{P}_1)=0$，等于给 $\mathbb{P}_1$ 免费加了权重——这就是「锚点免罪券」，
也是模态偏差的代数来源。</p></div>

<div class="cf">反事实：如果 $\lambda_k$ 不均匀（比如给某模态 $\lambda$ 特别大），重心会朝该模态偏移——
退化成「软锚点」。BaryBind 实践里取 $\lambda_k=1/K$ 均匀，正是为了彻底去中心化。</div>
</section>

<!-- ============ 5 ============ -->
<section id="s5">
<div class="kicker">CHAPTER 05 &middot; 对偶与 Sion</div>
<h2>数学地基 III：什么时候可以交换 inf 和 sup</h2>
<p>Prop 3.1 要把式 (3) 的 inf 问题改写成 sup-inf 对偶。这一步能不能成立，取决于<b>极小极大定理</b>
（minimax theorem）。论文用的是 Sion 极小极大定理，所以这里必须把它的前提条件说清楚。</p>

<div class="mathcard"><h4>式 (4)：Sion 极小极大定理（所用形式）</h4>
$$\inf_{x\in X}\sup_{y\in Y} F(x,y)=\sup_{y\in Y}\inf_{x\in X} F(x,y)$$
<p class="note">成立条件：$X$ 紧、凸；$Y$ 凸；$F(\cdot,y)$ 对每个 $y$ 下半连续且<b>凸</b>；
$F(x,\cdot)$ 对每个 $x$ 上半连续且<b>凹</b>。条件缺一不可——尤其凸/凹性，交换后两式只有一边不等。</p></div>

<h3>回到我们的场景：为什么三条都满足</h3>
<p>论文对式 (13) 的处理给出三条：</p>
<div class="insight-box"><span class="tag">深度洞察</span>
<h4>三条前提逐条核对</h4>
<p><b>① 紧性</b>：$\mathcal{M}_B$ 紧 $\Rightarrow$ $\mathcal{P}(\mathcal{M}_B)$ 在弱拓扑下紧。
概率测度空间在弱拓扑下，紧支撑集上的测度集是紧的（Prokhorov）。所以「对 $\mathbb{Q}$ 取 inf」的域是紧的。</p>
<p><b>② 对 $\mathbb{Q}$ 线性/凸/连续</b>：固定势 $f_{1:K}$，泛函 $\widetilde{\mathcal{F}}(\cdot,f_{1:K})$
对 $\mathbb{Q}$ 是<b>线性</b>的（因为是积分），线性蕴含凸且连续。</p>
<p><b>③ 对 $f$ 凹</b>：固定 $\mathbb{Q}$，$\widetilde{\mathcal{F}}(\mathbb{Q},\cdot)$ 对 $f$ 凹，
因为 $c$-transform $f_k^{C_k}$ 对 $f_k$ 是凹的（下包络的凹性）。</p>
<p>三条齐备 $\Rightarrow$ Sion 允许交换 $\sup$ 与 $\inf$，这就是 Prop 3.1 第一步的合法性来源。</p></div>

<p>但还有一个必须处理的<b>一致性条件</b>（congruence）$\sum_k\lambda_k f_k=0$。对偶问题的 supremum
要限制在满足这个条件的势函数上。为什么？以及怎么在参数化里保证它？这正是下一章 Prop 3.1 的核心，
也是论文里最容易被跳过、却最值得抠的部分。</p>
</section>

'''

io.open(r'D:\success\RSI\blogs\barybind\_part1.html','w',encoding='utf-8').write(HEAD)
print('part1 written:', len(HEAD))
