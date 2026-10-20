# -*- coding: utf-8 -*-
"""part 3: ch11-14 — 单纯形体积几何 / 体积 vs 余弦 / BVC / 总目标"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P3 = r'''
<!-- ============ 11 ============ -->
<section id="s11">
<div class="kicker">CHAPTER 11 &middot; 单纯形体积</div>
<h2>Barycenter simplex：为什么体积是好度量</h2>
<p>第二条理论主线是<b>体积</b>。BaryBind 定义了一个叫 <b>barycenter simplex</b> 的几何体：
以 WB 嵌入 $\mathbf{b}$ 为顶点，由「原点到 $\mathbf{b}$ 的向量」与各模态到重心的<b>间隙向量</b>
$\mathbf{r}_k=\mathbf{b}-\mathbf{m}_k$ 张成。它的体积同时量化两件事：对重心的全局对齐、以及模态间的差异。</p>

<div class="mathcard"><h4>式 (17)：张成矩阵与体积平方（式 9，Gantmacher）</h4>
$$\mathbf{R}=(\mathbf{b},\ \mathbf{r}_1,\ \cdots,\ \mathbf{r}_K),\qquad \mathrm{V}^2(\mathbf{b},\mathbf{r}_{1:K})=\det(\mathbf{R}^\top\mathbf{R})$$
$$=\begin{vmatrix}\langle\mathbf{b},\mathbf{b}\rangle&\langle\mathbf{b},\mathbf{r}_1\rangle&\cdots&\langle\mathbf{b},\mathbf{r}_K\rangle\\ \langle\mathbf{r}_1,\mathbf{b}\rangle&\langle\mathbf{r}_1,\mathbf{r}_1\rangle&\cdots&\langle\mathbf{r}_1,\mathbf{r}_K\rangle\\ \vdots&\vdots&\ddots&\vdots\\ \langle\mathbf{r}_K,\mathbf{b}\rangle&\langle\mathbf{r}_K,\mathbf{r}_1\rangle&\cdots&\langle\mathbf{r}_K,\mathbf{r}_K\rangle\end{vmatrix}$$
<p class="note">$K$ 个向量张成的平行多面体体积平方 = Gram 行列式 $\det(\mathbf{R}^\top\mathbf{R})$。
这是线性代数的标准结果：$n$ 个向量的体积平方等于它们两两内积构成的 Gram 矩阵的行列式。
发散：这正是 GRAM（Gramian Multimodal）名字的来源——Gram 行列式度量「向量组是否线性独立/张成大体积」，
独立性越强体积越大，越共线体积越小。BaryBind 沿用同一工具，但把中心从原点换成了 WB 锚点。</p></div>

<h3>$n=2$ 情形：体积 = $\sin\theta$</h3>
<div class="mathcard"><h4>式 (18)：二模态的体积（附录 A.3）</h4>
<p class="note">取归一化向量，$\langle\mathbf{b},\mathbf{b}\rangle=\langle\mathbf{r}_1,\mathbf{r}_1\rangle=1$，
记 $\cos\theta=\langle\mathbf{b},\mathbf{r}_1\rangle$：</p>
$$\mathrm{Vol}_{n=2}^2=\begin{vmatrix}1&\cos\theta\\ \cos\theta&1\end{vmatrix}=1-\cos^2\theta=\sin^2\theta\ \Longrightarrow\ \mathrm{Vol}_{n=2}=\sin\theta$$
<p class="note">二模态时，体积退化成<b>两个方向夹角的正弦</b>——衡量「模态向量与重心方向的偏离」。
$\theta$ 越小（越共线）体积越小，对齐越好；$\theta\to 90^\circ$ 体积最大。这是「体积=对齐度」最直观的特例。</p></div>

<h3>$n=3$ 情形：三角展开与耦合项</h3>
<div class="mathcard"><h4>式 (19)：三模态的体积（附录 A.3）</h4>
<p class="note">记 $\cos\theta=\langle\mathbf{b},\mathbf{r}_1\rangle,\ \cos\beta=\langle\mathbf{b},\mathbf{r}_2\rangle,\ \cos\gamma=\langle\mathbf{r}_1,\mathbf{r}_2\rangle$：</p>
$$\mathrm{Vol}_{n=3}^2=1-\cos^2\theta-\cos^2\beta-\cos^2\gamma+2\cos\theta\cos\beta\cos\gamma$$
$$=\sin^2\theta+\sin^2\beta+\sin^2\gamma+2\cos\theta\cos\beta\cos\gamma-2$$
<p class="note">$\sin^2$ 项是各方向的角偏差，$2\cos\theta\cos\beta\cos\gamma$ 是三个方向的<b>角耦合项</b>。
$\gamma$ 是两个间隙向量 $\mathbf{r}_1,\mathbf{r}_2$ 的夹角，直接反映<b>非锚模态之间的结构差异</b>。
三者角都小 $\Rightarrow$ 正弦 $\approx 0$、余弦 $\approx 1$ $\Rightarrow$ 体积小。</p></div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>耦合项 $2\cos\theta\cos\beta\cos\gamma$ 是「高阶信息」的所在</h4>
<p>如果只用两两余弦相似度，你能拿到 $\cos\theta,\cos\beta,\cos\gamma$ 三个二阶量，但它们是<b>独立</b>的三个数，
没有刻画三者的<b>联合</b>几何。而体积把它们通过一个行列式耦合起来——尤其那个乘积项
$\cos\theta\cos\beta\cos\gamma$，是三个方向<b>同时</b>共线性的度量。这就是为什么体积是「高阶」度量：
它不是三个角的平均，而是它们的<b>协调一致程度</b>。</p>
<p>发散：这与统计里「协方差矩阵的行列式」= 广义方差是同一回事。$\det(\mathbf{R}^\top\mathbf{R})$ 衡量
向量组张成空间的「胖瘦」；把模态聚到重心方向，就是让这个行列式变小（向量组退化到低维子空间）。
对比学习里用 trace 或成对内积，等于只用了「对角+两两」信息；体积用了<b>全部</b>特征值乘积。</p></div>

<div class="cf">反事实：若改用「体积最大化」（让向量组尽量正交），就会把模态推开——方向反了。
BaryBind 用的是<b>小体积是正样本</b>，即「聚到一起」，逻辑与「正交=独立」恰好相反，因为这里追求的是
<b>共识</b>而非独立性。这个符号方向在实现里最容易写反，是 C5 取证点。</div>
</section>

<!-- ============ 12 ============ -->
<section id="s12">
<div class="kicker">CHAPTER 12 &middot; 体积 vs 余弦</div>
<h2>高阶矩的优势：与 GRAM / Triangle 的几何谱系</h2>
<p>把体积度量放进谱系里看，能更清楚它的位置。成对余弦（CLIP 系）是<b>二阶</b>；GRAM 用
<b>平行六面体体积</b>（以原点为中心）；Triangle 用<b>三角形</b>（以原点为中心）；BaryBind 用
<b>重心单纯形</b>（以 WB 为顶点）。差别在两处：几何体的形状、以及中心在哪。</p>

<div class="svgbox">
<svg viewBox="0 0 940 280" xmlns="http://www.w3.org/2000/svg" font-family="'Noto Sans SC',sans-serif">
<text x="160" y="32" text-anchor="middle" font-size="13.5" font-weight="700" fill="#5F4B3B">CLIP：成对余弦（二阶）</text>
<circle cx="110" cy="120" r="12" fill="#2F6E75"/><circle cx="210" cy="120" r="12" fill="#C15B36"/>
<line x1="110" y1="120" x2="210" y2="120" stroke="#7A3B2E" stroke-width="2.5"/>
<text x="160" y="175" text-anchor="middle" font-size="11.5" fill="#5F4B3B">一对，一个内积</text>
<text x="160" y="205" text-anchor="middle" font-size="11.5" fill="#8C7663">看不到第三方</text>
<text x="470" y="32" text-anchor="middle" font-size="13.5" font-weight="700" fill="#5F4B3B">GRAM / Triangle：原点中心体积</text>
<line x1="420" y1="140" x2="520" y2="95" stroke="#2F6E75" stroke-width="2"/><line x1="420" y1="140" x2="525" y2="130" stroke="#C15B36" stroke-width="2"/><line x1="420" y1="140" x2="515" y2="160" stroke="#B5893F" stroke-width="2"/>
<polygon points="520,95 525,130 515,160" fill="#B5893F" opacity="0.2"/>
<circle cx="420" cy="140" r="6" fill="#33241A"/><text x="410" y="160" font-size="11" fill="#33241A">原点</text>
<text x="470" y="205" text-anchor="middle" font-size="11.5" fill="#5F4B3B">向量组从原点张成</text>
<text x="470" y="225" text-anchor="middle" font-size="11.5" fill="#8C7663">中心=原点，非语义中心</text>
<text x="790" y="32" text-anchor="middle" font-size="13.5" font-weight="700" fill="#2F6E75">BaryBind：重心单纯形</text>
<line x1="700" y1="150" x2="780" y2="95" stroke="#7A3B2E" stroke-width="2.4"/><circle cx="780" cy="95" r="10" fill="#7A3B2E"/>
<line x1="700" y1="150" x2="745" y2="108" stroke="#2F6E75" stroke-width="1.8"/><circle cx="745" cy="108" r="7" fill="#2F6E75"/>
<line x1="700" y1="150" x2="775" y2="132" stroke="#C15B36" stroke-width="1.8"/><circle cx="775" cy="132" r="7" fill="#C15B36"/>
<circle cx="700" cy="150" r="5" fill="#33241A"/><text x="682" y="168" font-size="11" fill="#33241A">原点</text>
<polygon points="780,95 745,108 775,132" fill="#2F6E75" opacity="0.18"/>
<text x="790" y="205" text-anchor="middle" font-size="11.5" fill="#5F4B3B">顶点=WB 锚点 b</text>
<text x="790" y="225" text-anchor="middle" font-size="11.5" fill="#2F6E75">中心=语义共识，非原点</text>
</svg>
<p style="font-size:12.5px;color:#8C7663;margin-top:8px;text-align:center">图 3（自绘）：三类几何度量的谱系——成对余弦、原点中心体积、重心单纯形。</p>
</div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>为什么「中心从原点换成 WB」是本质改进</h4>
<p>GRAM/Triangle 的体积度量其实已经抓住了「高阶几何」，但它们把所有向量都看成从原点出发——
这个原点是<b>任意的坐标原点</b>，不含语义。BaryBind 的改进是：先把中心换成<b>语义共识</b>（WB），
再在「各模态相对共识中心的间隙」上度量体积。所以它度量的是「各模态偏离共识多少」，
而不是「各模态在坐标系里有多分散」。前者是我们想要的对齐，后者会被坐标选择污染。</p>
<p>论文附录 B.5 正是在强调这一点：与纯锚点方法（GRAM/Triangle）的本质区别，在于 WB 优化是
<b>对齐之前的一个额外优化过程</b>——它先造出一个「优化过的几何参考」，再用它指导对齐。
消融显示去掉 WB 就掉点，说明 WB 是主要贡献，而不只是换了个体积公式。</p></div>

<div class="mathcard"><h4>式 (20)：体积度量与二阶度量的信息量对比</h4>
<p class="note">$n$ 个模态，成对余弦给出 $\binom{n}{2}$ 个二阶量；体积给出 1 个标量，
但它<b>编码了</b>全部 $\binom{n}{2}$ 个角 + 它们的耦合（行列式展开含所有混合乘积项）。
所以体积是<b>压缩的高阶统计</b>——用 1 个数承载了整个 Gram 矩阵的谱信息
（$\det=\prod\text{eigenvalues}$）。</p>
<div class="cf">反事实：若只用体积这一个标量做损失，会不会信息太压缩、梯度信号太弱？实践里 BVC 用了
两组负样本（第 13 章）+ DAM 二分类（第 14 章）来补信号，说明单一体积确实不足以单独支撑训练。</div></div>
</section>

<!-- ============ 13 ============ -->
<section id="s13">
<div class="kicker">CHAPTER 13 &middot; BVC</div>
<h2>BVC loss：两组负样本与「小体积=正样本」</h2>
<p>有了体积度量，就能量化「对齐好不好」，再用对比学习的方式把它变小。这就是
<b>Barycenter-anchored Volumetric Contrastive（BVC）loss</b>。</p>

<div class="mathcard"><h4>式 (21)：BVC loss（式 10）</h4>
$$\mathcal{L}_{\mathrm{BVC}}=-\mathbb{E}_i\Big[\log\frac{\exp(-\mathrm{V}(\mathbf{b}^{(i)},\mathbf{r}_{1:K}^{(i)})/\tau)}{\sum_j\exp(-\mathrm{V}(\mathbf{b}^{(i)},\mathbf{r}_{1:K}^{(j)})/\tau)}+\log\frac{\exp(-\mathrm{V}(\mathbf{b}^{(i)},\mathbf{r}_{1:K}^{(i)})/\tau)}{\sum_j\exp(-\mathrm{V}(\mathbf{b}^{(j)},\mathbf{r}_{1:K}^{(i)})/\tau)}\Big]$$
<p class="note">$\mathbf{b}^{(i)}=T_\theta(\mathbf{m}_0^{(i)})$ 是第 $i$ 个样本的 WB 锚点，
$\mathbf{r}_{1:K}^{(i)}=\{\mathbf{b}^{(i)}-\mathbf{m}_k^{(i)}\}$ 是各模态到重心的间隙向量。
<b>正样本</b>：$(\mathbf{b}^{(i)},\mathbf{r}_{1:K}^{(i)})$ 同一样本配对；<b>负样本</b>有两组——
（i）固定 $\mathbf{b}^{(i)}$ 配 $\mathbf{r}_{1:K}^{(j)},j\ne i$；（ii）固定 $\mathbf{r}_{1:K}^{(i)}$ 配 $\mathbf{b}^{(j)},j\ne i$。
小体积 → 概率大 → 拉近；大体积 → 概率小 → 推远。</p></div>

<h3>为什么是「小体积 = 好」</h3>
<p>由第 11 章，体积小意味着各模态向量都紧贴重心方向（$\theta,\beta$ 小）、且间隙向量彼此共线（$\gamma$ 小）
——也就是<b>所有模态聚向同一共识中心</b>。这正是我们要的。所以对比式里用
$\exp(-\mathrm{V}/\tau)$：体积越小，指数越大，softmax 里越占优。符号方向是「负体积」，
容易写反（若写成 $\exp(+\mathrm{V}/\tau)$ 就变成把模态推开）。</p>

<h3>两组负样本的作用</h3>
<div class="insight-box"><span class="tag">深度洞察</span>
<h4>双向负样本防止「重心坍缩」与「间隙坍缩」</h4>
<p>只用第一组（固定 $\mathbf{b}$、换 $\mathbf{r}$）：网络可以让所有 $\mathbf{b}^{(i)}$ 塌成同一个点
（重心坍缩），这样第一项分母全相等、损失退化。加第二组（固定 $\mathbf{r}$、换 $\mathbf{b}$）逼迫
不同样本的 $\mathbf{b}^{(i)}$ 互不相同，防坍缩。反过来也一样：两组一起，让<b>锚点</b>与<b>间隙</b>
都保持区分度。这是 InfoNCE 里「对称正负」思想在体积上的推广。</p></div>

<div class="cf">反事实：若只用一组负样本（比如固定 $\mathbf{b}$），训练会退化成「让所有样本共享同一重心」，
而间隙向量各自乱飞——全局几何就散了。双向负样本是保证<b>样本级</b>区分与<b>模态级</b>对齐同时成立的关键。</div>

<h3>温度 $\tau$ 与数值稳定</h3>
<p>$\tau=0.07$（与 CLIP 一致）。发散：体积的量纲与余弦不同（余弦在 $[-1,1]$，体积是
$\det$ 开根、可任意大），所以 $\tau$ 的选取对体积损失比对余弦损失更敏感。论文附录 B.8
专门讨论了「多面体体积度量的归一化」——因为 $\mathrm{V}^2=\det(\mathbf{R}^\top\mathbf{R})$
在向量范数大时会爆，必须做归一化（如把 $\mathbf{b},\mathbf{r}_k$ 单位化，见式 35-36 的假设
$\langle\mathbf{b},\mathbf{b}\rangle=1$）。这也是实现里必须小心的点（C6 取证）。</p>
</section>

<!-- ============ 14 ============ -->
<section id="s14">
<div class="kicker">CHAPTER 14 &middot; 总目标</div>
<h2>DAM loss 与三合一训练目标</h2>
<p>第三个损失是 <b>data-anchor matching（DAM）</b>，一个二分类头，用来区分「匹配/不匹配」的
数据-锚点对。加上 MWB 与 BVC，构成总目标。</p>

<div class="mathcard"><h4>式 (22)：DAM loss（式 11）</h4>
$$\mathcal{L}_{\mathrm{DAM}}=\mathbb{E}_{(\mathbf{b},\mathbf{m}_{1:K})}\big[y\log p_m(\mathbf{b},\mathbf{m}_{1:K})+(1-y)\log(1-p_m(\mathbf{b},\mathbf{m}_{1:K}))\big]$$
<p class="note">$p_m$ 由二分类器产生：锚模态数据过锚编码器，与拼接的非锚特征 $\mathbf{m}_{1:K}$
经 cross-attention 融合，再过两层 MLP 输出概率。$y=1$ 表示匹配对。这延续 VAST 的做法，提供
「样本级」的判别信号，补充体积损失的「几何级」信号。</p></div>

<div class="mathcard"><h4>式 (23)：总预训练目标（式 12）</h4>
$$\mathcal{L}:=\mathcal{L}_{\mathrm{MWB}}+\alpha_1\mathcal{L}_{\mathrm{BVC}}+\alpha_2\mathcal{L}_{\mathrm{DAM}}$$
<p class="note">实践中 $\tau=0.07,\ \alpha_1=1,\ \alpha_2=0.1$。$\mathcal{L}_{\mathrm{MWB}}$ 里的势
$f_{\omega_{1:K}}$ 走最大化，其余网络走最小化，交替训练（Algorithm 1）。</p></div>

<div class="insight-box"><span class="tag">深度洞察</span>
<h4>三个损失各管一「阶」</h4>
<p><b>MWB</b>：造中心（分布层面的最优传输对偶，管「中心在哪」）；
<b>BVC</b>：管高阶几何（体积，管「全局聚得好不好」）；
<b>DAM</b>：管样本判别（二分类，管「对不对得上号」）。
三者分别对应<b>零阶</b>（分布/中心）、<b>高阶</b>（几何/体积）、<b>实例阶</b>（判别）。
去掉任何一个都会让某一「阶」失去监督——消融（第 16 章 Table 5）正是这么设计的。</p></div>

<div class="cf">反事实：若只留 MWB（造中心但不对齐），中心算出来了但模态没聚过去；若只留 BVC
（对齐但中心是锚点），退回 GRAM/Triangle 的原点中心问题；若只留 DAM，退回成对判别、无全局几何。
三者缺一不可，这正是消融要证的事。</div>
</section>

'''

io.open(r'D:\success\RSI\blogs\barybind\_part3.html','w',encoding='utf-8').write(P3)
print('part3 written:', len(P3))
