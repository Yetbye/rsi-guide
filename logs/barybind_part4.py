# -*- coding: utf-8 -*-
"""part 4: ch15-20 — 实验 / 批判 / 科研问题 / 路线图 / 代码 / 结语 + footer"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

P4 = r'''
<!-- ============ 15 ============ -->
<section id="s15">
<div class="kicker">CHAPTER 15 &middot; 实验 I</div>
<h2>零样本分类与检索：Table 1 / Table 2 逐表精读</h2>
<p>BaryBind 以 VAST 为骨干（BERT-B 文本、BEATs 音频、EVA-CLIP-ViT-G 视觉，约 1B 参数），
在 VAST150k 上继续预训练。基准覆盖三模态（DiDeMo/ActivityNet）、四模态（MSR-VTT/VATEX，
额外引入 ChronoDepth 深度）与音频中心（VGGSound）。</p>

<div class="mathcard"><h4>Table 1（VGGSound5K 零样本分类，Acc@1 / Acc@5）</h4>
<p class="note">BaryBind 在所有模态配置上最优：V+A 双模态 <b>55.6 / 83.4</b>，显著超过 VAST（48.1 / 79.6）、
OmniBind（46.2 / 76.2）、GRAM（42.3 / 74.5）、Triangle（44.8 / 80.0）。
弱模态音频-only（A）从 VAST 的 40.3 提到 <b>45.7</b>（+5.4）。</p>
<div class="cf">反事实：A 单模态涨幅（+5.4）大于 V 单模态（+2.0），说明 BaryBind 确实在<b>救弱模态</b>——
锚点法里被压制的模态（音频）受益最大，正对应「模态偏差被消除」的主张。</div></div>

<div class="mathcard"><h4>Table 2（零样本 T2V / V2T 检索，R@1）</h4>
<p class="note">MSR-VTT 上 BaryBind T-V 双向 54.2 / 52.0，T-VA 三模态 56.1 / 53.6，T-VAS 57.1 / 53.8；
对比 VAST（T-VA 49.3 / 43.7）。<b>关键</b>：T2V 与 V2T 的差距（modality bias 的症状）明显缩小——
BaryBind 在多数基准上双向更对称。论文主结果称把 T2V/V2T 差距比 VAST 缩小 3.1%。</p>
<div class="cf">反事实：若 BaryBind 只是「更强的骨干」而非「更平衡的空间」，双向应当同比例涨、差距不变。
但差距缩小，说明改善来自<b>对称性</b>，支持「WB 消除 modality bias」的归因。</div></div>

<p>注意一个诚实的细节：BaryBind 在 VATEX 的 V2T 上略低于 GRAM（84.3 vs 82.1 的 T-VAS 口径需仔细对齐），
并非每个格子全胜——但整体平衡性与鲁棒性是它的卖点。第 18 章会把「全胜 vs 平衡」这条归因链拎出来核查。</p>
</section>

<!-- ============ 16 ============ -->
<section id="s16">
<div class="kicker">CHAPTER 16 &middot; 实验 II</div>
<h2>模态缺失鲁棒性 + 消融 + 训练动态</h2>

<h3>模态缺失（Table 4/6）</h3>
<p>BaryBind 用「任意可用子集」算重心，所以缺模态时，可用模态的对齐表示能当代理特征。
两个设定：① AudioCaps 上训练时缺音频的 T2A/A2T 检索；② VGGSound 上推理时缺视频的事件分类。
两者都优于锚点法（VAST/GRAM）与专门的缺失模态法（SIML/ShaSpec），退化更平缓。</p>

<div class="mathcard"><h4>Table 5（损失消融，VGGSound Acc@1 + MSR-VTT R@1）</h4>
<p class="note">基线 TV+TA 余弦对比：分类 38.1/42.8/44.5，检索 46.8/40.1。逐个加损失：
<b>+MWB</b> 单独就涨（分类 A +5.5、检索 V2T +7.2）；<b>+BVC</b> 单独也涨；
<b>MWB+BVC（去掉 TV+TA）</b>最强：分类 45.2/47.8/54.7，检索 54.8/51.1；
<b>MWB+BVC+DAM</b> 完整版 45.7/48.3/55.6，检索 56.1/53.6。</p>
<div class="cf">反事实：去掉 MWB（只 BVC+DAM）各项普遍掉（分类 V+A 50.1 vs 55.6），印证 WB 是主要贡献；
去掉 BVC（只 MWB+DAM）分类 V+A 49.8、检索 50.6/48.8，也掉——说明体积对齐不可省。
两个都拿掉退回成对基线最差。这组消融是「WB 是主要贡献、BVC 是必要补充」的直接证据。</div></div>

<h3>训练动态（Fig 5）</h3>
<p>从头训练对比：BaryBind 总损失下降更快、更早稳定（说明 MWB+BVC 让优化更高效）；
R@1 全程更高；且 T2V/V2T 差距快速缩小并收敛——训练过程中空间持续变得更对称。
这动态图直接可视化了「平衡表示空间被逐步建立」的过程。</p>
</section>

<!-- ============ 17 ============ -->
<section id="s17">
<div class="kicker">CHAPTER 17 &middot; 实验 III</div>
<h2>初始化鲁棒性 + 语义共识 + 体积-性能相关</h2>

<h3>初始化鲁棒性（Table 10/11）</h3>
<div class="mathcard"><h4>Table 10（T-VA 设定，锚点选择消融）</h4>
<p class="note"><b>不加 WB 优化</b>：视频锚 46.5、文本锚 48.1、T+V+A 融合锚 50.5（VGGSound V+A）。
<b>加 WB 优化</b>：视频初始化 55.2、文本初始化 55.6、融合初始化 55.8。三个初始化都大幅涨，
且彼此接近（55.2/55.6/55.8）。</p>
<div class="cf">反事实：若「初始化即中心」（没 WB 优化），选哪个模态当锚结果差异大（46.5 vs 50.5）；
加了 WB 优化后差异被抹平——证明贡献在 <b>WB 公式</b>，不在初始化选择。这是「重心确实不偏向任何模态」
的实验指纹。</div></div>

<h3>语义共识检索（Table 20/21）</h3>
<p>用 WB 空间做跨模态检索：把文本查询映进 WB 空间，再去检索视频/音频/字幕。
检索结果稳定共享同一高层概念（如「厨房烹饪」「篮球」），同时保留模态特异变化
（Table 20：query「一个人在厨房做饭」→ 检索到「切龙虾」「备菜」「加汤」等视频/音频/字幕）。
这实证了 WB 空间确实捕获了跨模态的共享语义结构。</p>

<h3>体积-性能相关（Fig 6）</h3>
<div class="mathcard"><h4>Fig 6：体积与下游 R@1 负相关</h4>
<p class="note">在 MSR-VTT 零样本检索上，barycenter simplex 体积与 R@1 呈明显负相关，
Pearson $\rho=-0.9844$。这印证了「体积小 = 对齐好 = 性能高」的核心主张——
体积不仅是个训练损失，也是<b>性能的代理指标</b>（可预测检索质量）。</p>
<div class="cf">反事实：若体积与性能无关（$\rho\approx 0$），那它就只是个任意的正则项。$\rho=-0.98$
说明体积确实在度量「对齐质量」，有诊断价值。但注意：相关不等于因果，也可能是体积小同时
反映了别的因素（如嵌入范数小）。</div></div>
</section>

<!-- ============ 18 ============ -->
<section id="s18">
<div class="kicker">CHAPTER 18 &middot; 批判</div>
<h2>八条法证式批判</h2>
<p>以下是「证据 → 推理 → 影响 → 补救」格式的批判。它们不否定 BaryBind 的贡献，而是标出
我认为需要额外实验才能坐实的地方。</p>

<div class="critique-box"><span class="tag">C1 · 理论</span>
<h4>Thm 3.2 的 $\beta$-强凸是条件性假设，未被实证</h4>
<p><strong>证据</strong>：定理「Assume ... $\beta$-strongly convex」，正文称欧氏成本下神经势足够光滑时成立，
建议 weight decay。但无实测 Hessian 曲率、无 weight decay 消融、无 $W^2$ 实测对照界。
<strong>影响</strong>：界是条件性保证，不能读作「必然收敛到真重心」。
<strong>补救</strong>：小规模用 Sinkhorn 算真 $\mathbb{Q}^*$，实测 $W^2$ 与 $\frac{4}{\beta}(\mathcal{E}_1+\mathcal{E}_2)$ 对照，看界紧不紧。</p></div>

<div class="critique-box"><span class="tag">C2 · 理论</span>
<h4>Prop 3.1 用欧氏成本 $\|\mathbf{m}-\mathbf{b}\|$，但对偶假设一般成本 $C_k$</h4>
<p><strong>证据</strong>：附录 A.1 推导时写一般 $C_k$，最终取 $C_k=\|\mathbf{m}_k-\mathbf{b}\|$（Wasserstein）。
但 $\ell_2$ 范数不可导、非强凸，与 Thm 3.2 的强凸要求存在<b>张力</b>（见 C1）。
<strong>影响</strong>：理论（一般成本）与实现（欧氏成本）之间有错位，理想条件下成立的结论，
在真实成本下要额外论证。
<strong>补救</strong>：显式区分「对偶等式」与「误差界」两处假设；或改用平方成本 $\|\cdot\|^2$（强凸，
但对应 $W_2$ 二阶）并重跑。</p></div>

<div class="critique-box"><span class="tag">C3 · 归因</span>
<h4>「WB 是主要贡献」依赖单一消融表，缺隔离</h4>
<p><strong>证据</strong>：Table 5 显示去掉 MWB 掉点，但 MWB 与 BVC 耦合（BVC 的体积依赖 WB 锚点 b），
去掉 MWB 时 BVC 也随之失效或变形。<strong>影响</strong>：难以把「WB 的贡献」与「BVC 失效的损失」分开——
掉点可能部分来自 BVC 塌了，而非 WB 本身。
<strong>补救</strong>：加一组「固定 WB 锚点（用 Sinkhorn 离线算）+ 只训 BVC」的对照，隔离 WB 优化的净贡献。</p></div>

<div class="critique-box"><span class="tag">C4 · 数值</span>
<h4>体积度量的数值稳定性与归一化未充分讨论</h4>
<p><strong>证据</strong>：$\mathrm{V}^2=\det(\mathbf{R}^\top\mathbf{R})$ 在向量范数大时爆，附录 B.8 提到归一化
但主文只隐含假设 $\langle\mathbf{b},\mathbf{b}\rangle=1$（式 35）。<strong>影响</strong>：实现里若没归一化，
梯度会爆炸或被范数主导，损失意义漂移。
<strong>补救</strong>：明确归一化策略（单位化/层归一化）、给数值范围、消融归一化对训练稳定的影响。</p></div>

<div class="critique-box"><span class="tag">C5 · 符号</span>
<h4>「小体积=正样本」的符号方向易写反，需核实实现</h4>
<p><strong>证据</strong>：BVC 用 $\exp(-\mathrm{V}/\tau)$，即负体积进 softmax。但体积度量本身常被用来
做「最大化多样性」。<strong>影响</strong>：若实现里符号反了，会变成推散模态，与主张相反，
而检索指标涨点可能是别的机制补偿。
<strong>补救</strong>：开源代码核对（github.com/xl-tang3/BaryBind），并补一个「符号翻转」的对照实验。</p></div>

<div class="critique-box"><span class="tag">C6 · 训练</span>
<h4>sup-inf 对抗优化的稳定性未量化</h4>
<p><strong>证据</strong>：MWB 是 max-min，交替优化 $f$（上）与 $T_\theta$（下），但论文未报告
对偶 gap $\mathcal{E}_1,\mathcal{E}_2$ 的实测轨迹，也未讨论 $f$ 与 $T$ 的学习率比、收敛判据。
<strong>影响</strong>：对抗训练易震荡或模式坍缩，读者不知这套交替到底稳不稳。
<strong>补救</strong>：给 $\mathcal{E}_1,\mathcal{E}_2$ 随训练的曲线（与 C1 的实测结合），证明对偶确实在收紧。</p></div>

<div class="critique-box"><span class="tag">C7 · 泛化</span>
<h4>「语义共识」由检索案例定性支撑，缺定量度量</h4>
<p><strong>证据</strong>：Table 20/21 用若干查询展示语义一致，但是<b>定性</b>案例。
<strong>影响</strong>：「WB 空间捕获语义共识」是核心主张，却主要靠可视化与个案，
缺少如「跨模态语义一致性分数」的定量指标。
<strong>补救</strong>：定义并报告一个共识度量（如跨模态检索的语义标签一致性率），与 VAST 对比。</p></div>

<div class="critique-box"><span class="tag">C8 · 范围</span>
<h4>扩到更多模态的 scaling 只到 4-5 个模态，且重心唯一性未讨论</h4>
<p><strong>证据</strong>：附录 B.6/B.13 讨论扩到更多模态，但模态数有限；且未讨论 $K$ 大时
重心唯一性/稳定性（第 10 章发散点：正曲率下均值可能不唯一）。<strong>影响</strong>：
「可扩展」的主张在模态很多时，重心估计可能不稳。
<strong>补救</strong>：扩到 $K\ge 6$ 模态，报告重心方差/多解性；或引入重心唯一性的充分条件并验证。</p></div>
</section>

<!-- ============ 19 ============ -->
<section id="s19">
<div class="kicker">CHAPTER 19 &middot; 科研问题</div>
<h2>五个可追问的方向</h2>
<p>每张卡含「问什么 + 反向判据 + 下手处」，按零成本到训练成本分级。</p>

<div class="research-question"><span class="tag">Q1 · 理论</span>
<h4>体积度量能否推广到更高阶（三阶以上）不变量？</h4>
<p>Gram 行列式是二阶内积的乘积；能否构造<b>三阶/四阶张量不变量</b>来度量 $n$ 模态的更高阶对齐？
<strong>反向判据</strong>：若高阶不变量在检索上无增益，说明二阶（体积）已饱和，高阶是冗余；
若有增益，说明现有体积丢了信息。<strong>下手处</strong>：构造 $\sum_{i<j<k}\langle\mathbf{r}_i,\mathbf{r}_j,\mathbf{r}_k\rangle$
型三阶量，加入 BVC，测 MSR-VTT R@1；零训练成本（只改损失）。</p></div>

<div class="research-question"><span class="tag">Q2 · 理论</span>
<h4>Wasserstein-2 正曲率下，重心唯一性条件是什么？</h4>
<p>第 10 章指出 WB 可能不唯一。能否给出「各 $\mathbb{P}_k$ 落在凸测地球内 ⇒ 重心唯一」的可验证条件？
<strong>反向判据</strong>：若实测多模态分布总满足唯一性条件，C8 的担忧被证伪，可安全扩展模态数。
<strong>下手处</strong>：对真实多模态特征分布，用 Sinkhorn 估重心并测其对初始化的敏感度（多次采样看方差）；
低训练成本。</p></div>

<div class="research-question"><span class="tag">Q3 · 方法</span>
<h4>体积度量与矩匹配（moment matching）的等价性？</h4>
<p>体积小 ≈ 向量组共线，是否等价于「低阶矩匹配」？能否把 WB+体积理解成一种<b>分布矩匹配</b>？
<strong>反向判据</strong>：若加显式矩匹配（均值+协方差对齐）与体积损失等价，说明体积是矩匹配的压缩形式；
若不等价，体积有独立价值。<strong>下手处</strong>：加二阶矩匹配项，对比体积损失的检索结果；
零训练成本（损失替换）。</p></div>

<div class="research-question"><span class="tag">Q4 · 方法</span>
<h4>缺失模态时，重心能否做「插值」补全？</h4>
<p>现在缺模态是「用子集重算重心」。能否把 WB 当作<b>生成中心</b>，插值出缺失模态的代理特征？
<strong>反向判据</strong>：若插值代理与真实特征检索性能差距大，说明重心不含足够模态特异信息，
只能当共识不能当补全器。<strong>下手处</strong>：拿完整样本，遮蔽一模态，用重心插值重建，
测检索/分类；中等训练成本。</p></div>

<div class="research-question"><span class="tag">Q5 · 理论</span>
<h4>WB+体积与信息瓶颈（information bottleneck）的关系？</h4>
<p>把各模态压缩到重心，是否在最小化「模态特异信息」、保留「共享语义信息」——即一种 IB？
能否用 IB 目标解释 BaryBind 为何更平衡、更鲁棒？<strong>反向判据</strong>：若 IB 度量（互信息）
与 BaryBind 的平衡性无相关，说明 IB 解释不成立，需另寻理论。<strong>下手处</strong>：估
$I(\text{模态};\text{表示})-I(\text{共识};\text{表示})$，与 T2V/V2T 差距做相关分析；理论+低训练成本。</p></div>
</section>

<!-- ============ 20 ============ -->
<section id="s20">
<div class="kicker">CHAPTER 20 &middot; 路线图与代码</div>
<h2>怎么读、怎么复现</h2>
<div class="roadmap">
<div class="step"><h4>第 1-2 天：OT 与重心地基</h4><p>读 Monge/Kantorovich 对偶（Santambrogio《Optimal Transport for Applied Mathematicians》前 3 章）→
Agueh–Carlier 2011（WB 定义）→ Cuturi–Doucet 2014（快速 WB）。复推本文式 (1)(2)(3)，理解 $c$-transform 凹性。</p></div>
<div class="step"><h4>第 3-4 天：Prop 3.1 与 Thm 3.2</h4><p>对照附录 A.1/A.2 逐步复推。重点：Sion 三条前提、一致化消元（式 9）、强凸→$W^2$ 界（式 15-16）。
自己算一遍常数 $4/\beta$ 的来历（平行四边形 + Wasserstein-2 耦合）。</p></div>
<div class="step"><h4>第 5-6 天：体积几何与 BVC</h4><p>推 Gram 行列式 $\det(\mathbf{R}^\top\mathbf{R})$ 的 $n=2,3$ 显式（式 18-19），
理解耦合项 $2\cos\theta\cos\beta\cos\gamma$。对照 GRAM/Triangle 的体积度量，看清中心位置的差别。</p></div>
<div class="step"><h4>第 7 天：复现与验证</h4><p>跑 github.com/xl-tang3/BaryBind。按 Q1-Q5 选一个零成本实验动手（推荐 Q1 或 Q3，只改损失）。
核对 C1-C8 的批判点，尤其体积符号（C5）与归一化（C4）。</p></div>
</div>

<div class="codebox">
<div class="code-head"><span class="cred run">可运行实现</span><h4>A. barycenter simplex 体积（式 17，经维度自检）</h4></div>
<pre><code class="language-python">import torch

def barycenter_simplex_volume(b, r_list, normalize=True):
    """b: (D,) WB 锚点；r_list: list of K (D,) 间隙向量 r_k = b - m_k
    返回 V = sqrt(det(R^T R))，R = (b, r_1, ..., r_K) 形状 (D, K+1)"""
    R = torch.stack([b] + list(r_list), dim=1)        # (D, K+1)
    if normalize:
        R = R / (R.norm(dim=0, keepdim=True) + 1e-8)  # 单位化，防 det 爆炸
    gram = R.T @ R                                    # (K+1, K+1)
    # 用 slogdet 求数值稳定；volume^2 = det(gram)
    sign, logdet = torch.linalg.slogdet(gram)
    vol_sq = sign * torch.exp(logdet)
    return torch.sqrt(torch.clamp(vol_sq, min=0.0))

# 自检：n=2 时应等于 sin(theta)
b = torch.tensor([1.0, 0.0])
r = torch.tensor([torch.cos(torch.tensor(0.7)), torch.sin(torch.tensor(0.7))])
v = barycenter_simplex_volume(b, [r])
assert abs(v.item() - torch.sin(torch.tensor(0.7)).item()) &lt; 1e-5, v
print("ok, volume =", v.item(), " sin(0.7) =", torch.sin(torch.tensor(0.7)).item())</code></pre>
<div class="code-note">可信度：可运行（维度与 $n=2$ 解析值 $\sin\theta$ 自检通过）。注意归一化步——不做会因范数爆掉（对应 C4）。</div>
</div>

<div class="codebox">
<div class="code-head"><span class="cred idea">示意实现</span><h4>B. MWB loss 的交替优化骨架（式 11）</h4></div>
<pre><code class="language-python"># 示意：T_theta 最小化、f_omega 最大化，交替
for m_1K in dataloader:                     # K 个模态特征
    m0 = m_1K.mean(0)                       # 初始化器：算术均值
    b  = T_theta(m0)                        # 重心采样
    # 一致性势：f_k = g_k - sum_i lambda_i g_i
    g = [g_net[k](b) for k in range(K)]
    f = [g[k] - sum(lam[i]*g[i] for i in range(K)) for k in range(K)]
    # MWB loss
    L_mwb = sum(lam[k] * (torch.norm(m_1K[k]-b) - f[k]) for k in range(K))
    # 更新 f（最大化 -> 对 f 取 - ）与 T（最小化）
    opt_f.zero_grad();  (-L_mwb).backward(retain_graph=True); opt_f.step()
    opt_T.zero_grad();  (L_mwb + alpha1*L_bvc + alpha2*L_dam).backward(); opt_T.step()</code></pre>
<div class="code-note">可信度：示意（省略 cross-attention 的 DAM 头与 BVC 负样本构造）。真实实现见 Algorithm 1。</div>
</div>

<div class="codebox">
<div class="code-head"><span class="cred idea">示意实现</span><h4>C. BVC loss 两组负样本（式 21）</h4></div>
<pre><code class="language-python">def bvc_loss(bs, rs, tau=0.07):
    # bs: (B, D) 重心；rs: (B, K, D) 间隙向量
    B = bs.size(0)
    # 正样本体积
    pos = torch.tensor([barycenter_simplex_volume(bs[i], list(rs[i]))
                        for i in range(B)])
    # 第一组：固定 b_i，换 r_j
    neg1 = torch.tensor([[barycenter_simplex_volume(bs[i], list(rs[j]))
                          for j in range(B)] for i in range(B)])
    # 第二组：固定 r_i，换 b_j
    neg2 = torch.tensor([[barycenter_simplex_volume(bs[j], list(rs[i]))
                          for j in range(B)] for i in range(B)])
    p1 = torch.logsumexp(-neg1/tau, dim=1)
    p2 = torch.logsumexp(-neg2/tau, dim=1)
    return -( -pos/tau - p1 + -pos/tau - p2 ).mean()   # 对称两组</code></pre>
<div class="code-note">可信度：示意（逐对算体积，实际应批量）。注意 <code>-pos/tau</code> 的负号——对应 C5。</div>
</div>

<h3>结语</h3>
<p>BaryBind 的贡献是把「多模态绑定的中心」从「某个模态」换成「所有模态分布的 Wasserstein 重心」，
并用一个以重心为顶点的单纯形体积作为高阶全局对齐度量。它的两块理论——
<b>对偶（Prop 3.1）</b>与<b>误差界（Thm 3.2）</b>——把最优传输的语言完整引入多模态表示学习，
而体积几何则把对齐从二阶推向高阶。诚实地讲，误差界依赖未实证的强凸假设（C1）、对偶与实现的成本有错位（C2）、
主贡献的隔离不足（C3）——但「用几何共识中心消除模态偏差」这个方向，无论理论还是实验都立得住，
值得继续追。<b>它留给我的问题</b>：重心到底是一个「共识」还是一个「插值器」？这决定它是只做理解，
还是也能反过来做生成——论文自己也把「加入重建以支持生成」列为未来工作。</p>
</section>

</main>

<footer>
<div class="inner">
  <h3>参考文献（关键条目）</h3>
  <ol>
    <li>Agueh &amp; Carlier (2011). Barycenters in the Wasserstein space. <em>SIAM J. Math. Anal.</em> — WB 定义与存在性。</li>
    <li>Cuturi &amp; Doucet (2014). Fast computation of Wasserstein barycenters. <em>ICML</em> — WB 的快速算法。</li>
    <li>Santambrogio. Optimal Transport for Applied Mathematicians — Kantorovich 对偶与 $c$-transform。</li>
    <li>Gantmacher. The Theory of Matrices — Gram 行列式与体积。</li>
    <li>Sion (1958). On general minimax theorems — 极小极大定理。</li>
    <li>Tang, Xu, Gu, Yang, Sun (2026). Binding Multiple Modalities via Multimodal Wasserstein Barycenter (BaryBind). arXiv:2609.33800.</li>
  </ol>
  <div class="fin">
    <p>论文版权归原作者所有；本篇是我自己的深读笔记，批判观点不代表作者立场。代码见
    <a href="https://github.com/xl-tang3/BaryBind">github.com/xl-tang3/BaryBind</a>。</p>
  </div>
</div>
</footer>
</body>
</html>
'''

io.open(r'D:\success\RSI\blogs\barybind\_part4.html','w',encoding='utf-8').write(P4)
print('part4 written:', len(P4))
