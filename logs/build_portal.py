# -*- coding: utf-8 -*-
"""Build the MHML · RSI reading-guide portal (index.html at repo root).

Design system: Venus composition protocol, Palette C "Hellenic Gold" (希腊暖金).
Decor culture: greek (meander frieze, Doric columns, laurel, amphora, sun disc),
universal (paper grain, colour washes, classical lines).

Regenerate:  python logs/build_portal.py
"""
import html
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# pattern assets
# ----------------------------------------------------------------------------
MEANDER_PATH = "M6 12 H12 V0 H0 V10 H10 V2 H2 V8 H8 V4 H4 V6 H6"


def meander_uri(stroke="%234A3A28", w=1.3):
    from urllib.parse import quote
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' "
           f"viewBox='-1 -1 14 14'><path d='{MEANDER_PATH}' fill='none' "
           f"stroke='{stroke}' stroke-width='{w}'/></svg>")
    return "url(\"data:image/svg+xml," + quote(svg, safe="'=:/%,#-") + "\")"


NOISE_URI = None  # computed in build()

# ----------------------------------------------------------------------------
# catalogue data (verified against each blog's FINAL/ACCEPTANCE docs)
# ----------------------------------------------------------------------------
PAPERS = [
    # --- container B: static parameters / editing -----------------------------
    dict(slug="mend", roman="I", group="B",
         cn="MEND 深度解读", en="Fast Model Editing at Scale",
         venue="ICLR 2022 · arXiv 2110.11309",
         desc="把单样本微调的 rank-1 梯度改造成可靠、局部、泛化的参数更新——编辑网络让 10B+ 模型秒级完成精准手术。",
         meta="13 章 · 3 图 · 8 法证批判 · 5 科研问题",
         sw=["#8B4570", "#5A7B6B", "#E86B8A"], cover=None, monogram="MEND"),
    # --- container G: parameter generation -----------------------------------
    dict(slug="genadapter", roman="II", group="G",
         cn="Generative Adapter 深度解读", en="Generative Adapter: Contextualizing Language Models in Parameters with a Single Forward Pass",
         venue="arXiv 2411.05877 · 2024", pdfname="generative-adapter",
         desc="单次前向把上下文写进冻结 LM 的参数：context → 条件化 LoRA，元学习覆盖 500+ 任务的分布。",
         meta="13 章 · 4 图 · MathJax",
         sw=["#16A34A", "#4ADE80", "#F97316"], cover="blogs/genadapter/assets/hero_cover.jpg", monogram="GA"),
    dict(slug="rpg", roman="III", group="G",
         cn="RPG 深度解读", en="Recurrent Diffusion for Large-Scale Parameter Generation",
         venue="arXiv 2501.11587 · 2025",
         desc="让循环扩散从零生成两亿参数的网络权重——参数生成（parameter generation）的第一性形式。",
         meta="13 章 · 3 图",
         sw=["#0891B2", "#22D3EE", "#94A3B8"], cover="blogs/rpg/assets/hero_cover.jpg", monogram="RPG"),
    dict(slug="dyprag", roman="IV", group="G",
         cn="DyPRAG 深度解读", en="Dynamic Parametric RAG for Test-time Knowledge Enhancement",
         venue="arXiv 2503.23895 · 2025",
         desc="用一个小翻译器把检索文档蒸馏成 LoRA 参数——参数化 RAG 的实用主义路线，测试时知识增强。",
         meta="13 章 · 3 图",
         sw=["#7C3AED", "#A78BFA", "#F97316"], cover="blogs/dyprag/assets/hero_cover.jpg", monogram="DyP"),
    dict(slug="text2lora", roman="V", group="G",
         cn="Text-to-LoRA 深度解读", en="Text-to-LoRA: Instant Transformer Adaption",
         venue="ICML 2025 · Sakana AI", pdfname="text-to-lora",
         desc="一句话生成 LoRA：超网络单次前向完成即时任务适配，把逐任务微调折叠成一次前向。",
         meta="11 章 · 2 图",
         sw=["#1B4B6F", "#5A8F7B", "#E85D4E"], cover="blogs/text2lora/assets/cover.jpg", monogram="T2L"),
    dict(slug="dnd", roman="VI", group="G",
         cn="DnD 深度解读", en="Drag-and-Drop LLMs: Zero-Shot Prompt-to-Weights",
         venue="arXiv 2506.16406 · 2025",
         desc="拖拽即用：prompt→权重超生成器 0.11 秒生成 0.5B 全套 LoRA，含 10 条法证批判与三假说检验。",
         meta="18 章 · 7 图 · 10 法证批判 · 5 科研问题",
         sw=["#1B4B6F", "#5A8F7B", "#E85D4E"], cover=None, monogram="DnD"),
    dict(slug="shine", roman="VII", group="G",
         cn="SHINE 深度解读", en="SHINE: A Scalable In-Context Hypernetwork for Mapping Context to LoRA",
         venue="ICML 2026 · PMLR 306 · 北大 Mu Lab",
         desc="Mu Lab 本家：冻结 LLM 全层 memory states + 行列交替双向注意力，单次前向生成全层 LoRA。",
         meta="13 章 · 3 图",
         sw=["#6B1D2A", "#8B3040", "#C9A227"], cover="blogs/shine/assets/cover.jpg", monogram="SHN"),
    dict(slug="d2l", roman="VIII", group="G",
         cn="Doc-to-LoRA 深度解读", en="Doc-to-LoRA: Learning to Instantly Internalize Contexts",
         venue="arXiv 2602.15902 · 2026 · Sakana AI", pdfname="doc-to-lora",
         desc="把 context distillation 元学习进 309M Perceiver 超网络：读一篇 32K 文档 0.2 秒产出 LoRA，此后免上下文。",
         meta="15 章 · 5 图 · 9 法证批判 · 5 科研问题",
         sw=["#2D2D2D", "#3C5A4A", "#C44D3F"], cover=None, monogram="D2L"),
    # --- container D: online state -------------------------------------------
    dict(slug="delmem", roman="IX", group="D",
         cn="δ-mem 深度解读", en="δ-mem: Efficient Online Memory for Large Language Models",
         venue="arXiv 2605.12357 · 2026",
         desc="冻结骨干 + 8×8 在线联想记忆状态（gated delta rule）+ 低秩读出修正注意力：0.12% 参数撬动长历史。",
         meta="17 章 · 4 图",
         sw=["#7C3AED", "#A78BFA", "#FBBF24"], cover="blogs/delmem/assets/hero_cover.jpg", monogram="δ"),
    dict(slug="unimem", roman="X", group="D",
         cn="UniMem 深度解读", en="UniMem: Complementary Episodic-to-Parametric Memory for Boundary-Agnostic Task Streams",
         venue="PREPRINT · 2026 · CAS / PKU / THU / UCL",
         desc="互补式情景-参数记忆：边界无关任务流上自主分配参数记忆块，CLS 理论启发的记忆扩展。",
         meta="11 章 · 2 图",
         sw=["#1B4B6F", "#5A8F7B", "#E85D4E"], cover="blogs/unimem/assets/cover.jpg", monogram="UM"),
    # --- container E: test-time gradient --------------------------------------
    dict(slug="ttt-e2e", roman="XI", group="E",
         cn="TTT-E2E 深度解读", en="End-to-End Test-Time Training for Long Context",
         venue="arXiv 2512.23675 · 2025",
         desc="长上下文即持续学习：测试时 NTP 内环 + grad-of-grad 外环；损失 scaling 与全注意力同轨、prefill 恒定快 2.7×。",
         meta="10 章 · 5 图 · 8 法证批判 · 5 科研问题",
         sw=["#0D9488", "#14B8A6", "#FBBF24"], cover=None, monogram="TTT"),
    dict(slug="inplace-ttt", roman="XII", group="E",
         cn="In-Place TTT 深度解读", en="In-Place Test-Time Training",
         venue="arXiv 2604.06169 · 2026 · ByteDance Seed × PKU",
         desc="把 gated MLP 的 W_down 就地当快权重：chunk-wise 闭式更新 + 显式 NTP 对齐，CP 原生的测试时训练。",
         meta="10 章 · 4 图 · 9 法证批判 · 5 科研问题",
         sw=["#4F46E5", "#34D399", "#F97316"], cover=None, monogram="IPT"),
]

GROUPS = [
    dict(key="B", letter="Βʹ", name="静态参数 · 模型编辑", tag="STATIC PARAMETERS · MODEL EDITING",
         note="把「新知识」写进既有权重：不训练基座，只学习如何做参数手术。",
         aside=dict(title="容器 · Βʹ", lead="在被冻结的权重上做定点手术——不改变模型的使用方式，只让少数事实或行为被精确替换。",
                    points=["核心问句：改了这块权重，哪些输入会变、哪些必须不变？",
                            "代表工作 MEND（2022）：学习「如何更新」，而不是重新学习「更新什么」。",
                            "后续对照：locate-then-edit 系列（ROME / MEMIT）与生成式编辑（SHINE / D2L）。"])),
    dict(key="G", letter="Γʹ", name="生成参数 · 超网络", tag="PARAMETER GENERATION · HYPERNETWORKS",
         note="不优化权重，而是生成权重：context/prompt → 单次前向 → 一整套增量参数。", aside=None),
    dict(key="D", letter="Δʹ", name="在线状态 · 记忆", tag="ONLINE STATE · MEMORY",
         note="权重之外的第二容器：推理期持续读写的在线记忆状态，快、省、非参数化。",
         aside=dict(title="容器 · Δʹ", lead="参数之外的记忆层：推理期持续读写，容量有限但完全可逆——清空即忘记。",
                    points=["δ-mem：8×8 联想状态 + gated delta rule 在线更新，读出低秩修正注意力。",
                            "UniMem：情景缓冲 + 参数记忆块，CLS 理论下的稳定性-可塑性折中。",
                            "核心问句：同一份经验，该固化进参数，还是留在可逆的状态里？"])),
    dict(key="E", letter="Εʹ", name="测试时梯度 · 内环学习", tag="TEST-TIME GRADIENT · INNER LOOP",
         note="部署后仍在学习：推理期在上下文上跑梯度内环，目标与效率是主战场。",
         aside=dict(title="容器 · Εʹ", lead="部署后仍在学习：推理时在上下文上跑内环优化，梯度是唯一的更新语言。",
                    points=["TTT-E2E：NTP 内环 + grad-of-grad 元学习外环，损失 scaling 与全注意力同轨。",
                            "In-Place TTT：W_down 就地当快权重，chunk-wise 闭式更新换来 CP 原生并行。",
                            "核心问句：内环做到多非线性、目标怎么对齐，才不牺牲召回与效率？"])),
]

MU_REPOS = [
    ("In-Parameter-Learning", "纲领 · 立场论文：In-Parameter Learning（为什么终身 AI 需要的不止更长上下文）", "guide"),
    ("SHINE", "可扩展 in-context hypernetwork —— 本指南卷 Ⅶ", "collection"),
    ("PaST", "ACL 2026 Oral · Knowledge is Not Enough: Injecting RL Skills for Continual Adaptation", "repo"),
    ("PiSSA", "NeurIPS 2024 Spotlight · 主奇异向量的 LoRA 初始化（431★）", "repo"),
    ("TransArch", "硬件友好的架构设计与 LLM 迁移（512★）", "repo"),
    ("LIFT", "Long Input Fine-Tuning · 长上下文理解框架", "repo"),
    ("LooGLE-v2", "NeurIPS DB Track 2025 · 真实世界长依赖评测", "repo"),
    ("Meta-RFFT", "NeurIPS 2025 · 多任务长度泛化", "repo"),
    ("RDBPFN", "关系型 in-context learning 与结构先验预训练", "repo"),
    ("SESA", "序列采样增强 LLM 探索（The Road Less Traveled）", "repo"),
]


def esc(s):
    return html.escape(s, quote=True)


def build():
    from urllib.parse import quote
    noise = ("<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'>"
             "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' "
             "numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/>"
             "</filter><rect width='260' height='260' filter='url(#n)' opacity='0.55'/></svg>")
    noise_uri = "url(\"data:image/svg+xml," + quote(noise, safe="'#") + "\")"
    meander_bronze = meander_uri("%234A3A28", 1.3)
    meander_gold = meander_uri("%23C09A54", 1.2)

    # ---------------------------------------------------------------- cards
    card_html = []
    for group in GROUPS:
        items = [p for p in PAPERS if p["group"] == group["key"]]
        cards = []
        aside_block = ""
        for p in items:
            if p["cover"]:
                plate = (f'<img class="plate-img" src="{p["cover"]}" '
                         f'alt="{esc(p["cn"])} 封面" loading="lazy">')
            else:
                uid = p["slug"].replace("-", "")
                plate = f'''<svg class="plate-emblem" viewBox="0 0 360 190" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <defs>
    <pattern id="mk-{uid}" width="14" height="14" patternUnits="userSpaceOnUse">
      <path d="{MEANDER_PATH}" fill="none" stroke="#C09A54" stroke-width="1.1" opacity="0.55"/>
    </pattern>
  </defs>
  <rect width="360" height="190" fill="#F3ECDC"/>
  <rect y="0" width="360" height="14" fill="url(#mk-{uid})"/>
  <rect y="176" width="360" height="14" fill="url(#mk-{uid})"/>
  <circle cx="180" cy="95" r="52" fill="none" stroke="#4A3A28" stroke-width="1.4"/>
  <circle cx="180" cy="95" r="45" fill="none" stroke="#C09A54" stroke-width="1"/>
  <text x="180" y="109" text-anchor="middle" font-size="34" fill="#4A3A28"
        font-family="Palatino Linotype, Georgia, serif" letter-spacing="1">{esc(p["monogram"])}</text>
</svg>'''
            sw = "".join(f'<i style="--c:{c}"></i>' for c in p["sw"])
            cards.append(f'''      <article class="card" id="paper-{p["slug"]}">
        <a class="plate" href="blogs/{p["slug"]}/index.html" aria-label="进入 {esc(p["cn"])}">
          {plate}
          <span class="plate-veil"></span>
          <span class="plate-num">{p["roman"]}</span>
          <span class="venue">{esc(p["venue"])}</span>
        </a>
        <div class="card-body">
          <div class="card-top">
            <span class="swatches" title="该篇博客的配色">{sw}</span>
            <span class="card-meta">{esc(p["meta"])}</span>
          </div>
          <h3><a href="blogs/{p["slug"]}/index.html">{esc(p["cn"])}</a></h3>
          <p class="card-en">{esc(p["en"])}</p>
          <p class="card-desc">{esc(p["desc"])}</p>
          <div class="card-links">
            <a class="btn btn-primary" href="blogs/{p["slug"]}/index.html">读深读</a>
            <a class="btn btn-ghost" href="papers/pdf/{p.get("pdfname", p["slug"])}.pdf">论文 PDF</a>
            <a class="btn btn-ghost" href="papers/text/{p["slug"]}.txt">全文提取</a>
          </div>
        </div>
      </article>''')
        if group["aside"]:
            a = group["aside"]
            pts = "".join(f"<li>{esc(x)}</li>" for x in a["points"])
            aside_block = f'''      <aside class="group-aside">
        <span class="aside-kicker">{esc(a["title"])}</span>
        <p class="aside-lead">{esc(a["lead"])}</p>
        <ul>{pts}</ul>
      </aside>'''
        card_html.append(f'''    <div class="tome-group" id="group-{group["key"]}">
      <div class="group-head reveal">
        <span class="group-letter" aria-hidden="true">{group["letter"]}</span>
        <div>
          <h3 class="group-name">{esc(group["name"])}</h3>
          <span class="group-tag">{esc(group["tag"])}</span>
        </div>
        <p class="group-note">{esc(group["note"])}</p>
      </div>
      <div class="card-grid{'' if not group['aside'] else ' with-aside'}">
{chr(10).join(cards)}
{aside_block}
      </div>
    </div>''')
    cards_block = "\n".join(card_html)

    # ------------------------------------------------------- constellation svg
    cols = [
        ("Αʹ", "ICL", "全上下文", "#8B7A5E",
         [("基线 · 一切方法的对照", None)], 0),
        ("Βʹ", "静态参数", "模型编辑", "#8B4570",
         [("MEND", "mend")], 1),
        ("Γʹ", "生成参数", "超网络", "#B85C38",
         [("Generative Adapter", "genadapter"), ("RPG", "rpg"), ("DyPRAG", "dyprag"),
          ("Text-to-LoRA", "text2lora"), ("DnD", "dnd"), ("SHINE", "shine"), ("Doc-to-LoRA", "d2l")], 7),
        ("Δʹ", "在线状态", "记忆", "#7C3AED",
         [("δ-mem", "delmem"), ("UniMem", "unimem")], 2),
        ("Εʹ", "测试时梯度", "内环学习", "#0D9488",
         [("E2E TTT", "ttt-e2e"), ("In-Place TTT", "inplace-ttt")], 2),
    ]
    W, H = 1180, 560
    cx0, dx = 128, 236
    svg = [f'<svg class="astrolabe" viewBox="0 0 {W} {H}" role="img" aria-label="五容器谱系星图：ICL、静态参数、生成参数、在线状态、测试时梯度">']
    svg.append(f'<circle cx="590" cy="272" r="252" fill="none" stroke="#C09A54" stroke-width="1" opacity="0.35"/>')
    svg.append(f'<circle cx="590" cy="272" r="196" fill="none" stroke="#C09A54" stroke-width="1" opacity="0.18" stroke-dasharray="2 6"/>')
    svg.append(f'<circle cx="590" cy="272" r="132" fill="none" stroke="#4A3A28" stroke-width="1" opacity="0.08"/>')
    # ticks
    import math
    for i in range(48):
        a = i * math.pi / 24
        r1, r2 = 252, 240 if i % 2 else 232
        x1, y1 = 590 + r1 * math.cos(a), 272 + r1 * math.sin(a)
        x2, y2 = 590 + r2 * math.cos(a), 272 + r2 * math.sin(a)
        svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#4A3A28" stroke-width="1" opacity="0.18"/>')
    # stars
    for sx, sy, r in [(178, 96, 1.6), (966, 120, 1.4), (420, 470, 1.5), (812, 452, 1.4), (612, 66, 1.3), (1042, 300, 1.6)]:
        svg.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="#C09A54" opacity="0.7"/>')
    # columns
    for i, (letter, name, sub, color, chips, _n) in enumerate(cols):
        x = cx0 + dx * i
        svg.append(f'<text x="{x}" y="86" text-anchor="middle" font-size="26" fill="{color}" '
                   f'font-family="Palatino Linotype, Georgia, serif">{letter}</text>')
        svg.append(f'<text x="{x}" y="112" text-anchor="middle" font-size="17" fill="#2B2419" '
                   f'font-family="Palatino Linotype, Georgia, serif" letter-spacing="1">{name}</text>')
        svg.append(f'<text x="{x}" y="132" text-anchor="middle" font-size="11" fill="#94876F" '
                   f'font-family="Consolas, monospace" letter-spacing="2">{sub}</text>')
        svg.append(f'<line x1="{x-58}" y1="144" x2="{x+58}" y2="144" stroke="{color}" stroke-width="1.4" opacity="0.55"/>')
        for j, (label, slug) in enumerate(chips):
            y = 168 + j * 38
            op = "1" if slug else "0.62"
            dash = '' if slug else ' stroke-dasharray="3 3"'
            svg.append(f'<g class="node" opacity="{op}">')
            svg.append(f'<rect x="{x-88}" y="{y-16}" width="176" height="30" rx="8" fill="#FFFDF7" '
                       f'stroke="{color}" stroke-width="1.2"{dash}/>')
            tcol = "#2B2419" if slug else "#94876F"
            svg.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="12.5" fill="{tcol}" '
                       f'font-family="Palatino Linotype, Georgia, serif">{label}</text>')
            svg.append('</g>')
    # arrows between column headers
    for i in range(4):
        x1 = cx0 + dx * i + 74
        x2 = cx0 + dx * (i + 1) - 78
        ym = 104
        svg.append(f'<line x1="{x1}" y1="{ym}" x2="{x2-6}" y2="{ym}" stroke="#B85C38" stroke-width="1.3" opacity="0.6" stroke-dasharray="5 4"/>')
        svg.append(f'<path d="M{x2-6} {ym} l-7 -4 v8 z" fill="#B85C38" opacity="0.6"/>')
    # caption
    svg.append(f'<text x="590" y="512" text-anchor="middle" font-size="14.5" fill="#5D5344" '
               f'font-family="Palatino Linotype, Georgia, serif">所有方法都在回答同一个问题：新知识住在哪里？—— 上下文 · 权重 · 生成器 · 在线状态 · 测试时梯度</text>')
    svg.append(f'<text x="112" y="540" text-anchor="start" font-size="11.5" fill="#94876F" font-family="Consolas, monospace">2018 — 2026 · OPENALEX 趋势：长上下文与上下文管理迅猛增长，持续性参数学习仍处新兴</text>')
    svg.append('</svg>')
    constellation = "\n".join(svg)

    # ------------------------------------------------------------- mu repos
    repo_rows = []
    for name, desc, kind in MU_REPOS:
        badge = {"guide": "纲领", "collection": "本指南", "repo": "仓库"}[kind]
        cls = {"guide": "mark-guide", "collection": "mark-collection", "repo": "mark-repo"}[kind]
        repo_rows.append(
            f'<a class="repo-row {cls}" href="https://github.com/MuLabPKU/{name}" target="_blank" rel="noopener">'
            f'<span class="repo-mark">{badge}</span>'
            f'<span class="repo-name">{esc(name)}</span>'
            f'<span class="repo-desc">{esc(desc)}</span>'
            f'<span class="repo-arrow" aria-hidden="true">↗</span></a>')
    repos_block = "\n        ".join(repo_rows)

    # ---------------------------------------------------------------- render
    page = f'''<!DOCTYPE html>
<html lang="zh-CN" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MHML · RSI 深读指南 | 自改进之路 · Twelve Tomes</title>
<meta name="description" content="跟随北大 Mu Lab 的 In-Parameter Learning 纲领：12 篇 RSI 论文深度解读——模型编辑、参数生成、在线记忆、测试时训练。">
<style>
/* ============================================================
   VENUS / Palette C — Hellenic Gold（希腊暖金）
   Base 层遵循 Venus 常量；装饰文化 = greek + universal
   ============================================================ */
:root {{
  --bg-primary:#FBF8F1; --bg-secondary:#F4EFE3; --bg-tertiary:#E9E0CE;
  --text-primary:#2B2419; --text-secondary:#5D5344; --text-muted:#94876F;
  --color-primary:#4A3A28; --color-secondary:#7A6B52; --color-tertiary:#35595A;
  --accent-warm:#B85C38; --accent-gold:#C09A54; --accent-soft:#E5D3AF;
  --font-display:'Palatino Linotype','EB Garamond','Book Antiqua',Georgia,'Noto Serif SC','Source Han Serif SC','Songti SC',serif;
  --font-body:'Segoe UI','Noto Sans SC',-apple-system,'Microsoft YaHei',sans-serif;
  --font-mono:'Consolas','JetBrains Mono',monospace;
  --ease-out:cubic-bezier(0.16,1,0.3,1); --duration:0.4s;
  --container:1200px;
  --radius-sm:4px; --radius-md:8px; --radius-lg:14px; --radius-full:9999px;
  --shadow-sm:0 2px 8px rgba(43,36,25,0.07);
  --shadow-md:0 6px 18px rgba(43,36,25,0.10);
  --shadow-lg:0 14px 40px rgba(43,36,25,0.16);
  --line:rgba(74,58,40,0.16);
  --meander:{meander_bronze};
  --meander-gold:{meander_gold};
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{
  font-family:var(--font-body); color:var(--text-primary); line-height:1.85; font-size:17px;
  background:var(--bg-primary);
  background-image:{noise_uri};
  background-size:260px 260px;
}}
h1,h2,h3,h4{{font-family:var(--font-display);font-weight:700;line-height:1.3}}
a{{color:var(--color-primary);text-decoration:none}}
img{{max-width:100%;display:block}}
.container{{max-width:var(--container);margin:0 auto;padding:0 24px}}

/* ---------- nav ---------- */
nav{{
  position:sticky;top:0;z-index:100;background:rgba(251,248,241,0.92);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line);
}}
.nav-inner{{max-width:var(--container);margin:0 auto;display:flex;align-items:center;gap:22px;height:56px;padding:0 24px;overflow-x:auto;scrollbar-width:none}}
.nav-inner::-webkit-scrollbar{{display:none}}
.nav-brand{{font-family:var(--font-display);font-weight:700;color:var(--color-primary);white-space:nowrap;font-size:15.5px;letter-spacing:1px}}
.nav-brand .gr{{color:var(--accent-warm)}}
.nav-link{{font-size:13.5px;color:var(--text-secondary);white-space:nowrap;transition:color .3s var(--ease-out);position:relative;padding:4px 0}}
.nav-link::after{{content:'';position:absolute;left:0;right:0;bottom:0;height:1.5px;background:var(--accent-warm);transform:scaleX(0);transform-origin:left;transition:transform .35s var(--ease-out)}}
.nav-link:hover{{color:var(--accent-warm)}}
.nav-link:hover::after{{transform:scaleX(1)}}

/* ---------- hero ---------- */
.hero{{position:relative;overflow:hidden;padding:110px 24px 76px;text-align:center}}
.hero::before{{content:'';position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 620px 420px at 18% 12%,rgba(192,154,84,0.16),transparent 62%),
             radial-gradient(ellipse 640px 420px at 84% 82%,rgba(184,92,56,0.10),transparent 60%),
             radial-gradient(ellipse 460px 300px at 62% 30%,rgba(53,89,90,0.07),transparent 65%);}}
.frieze{{position:absolute;top:0;left:0;right:0;height:18px;background-image:var(--meander);background-size:14px 14px;opacity:0.5;pointer-events:none}}
.frieze-b{{top:auto;bottom:0;opacity:0.3}}
.hero-sun{{position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);width:640px;height:640px;pointer-events:none;opacity:0.16}}
.hero-col{{position:absolute;top:48px;bottom:-24px;width:74px;opacity:0.15;pointer-events:none;color:var(--color-primary)}}
.hero-col.l{{left:2.5%}} .hero-col.r{{right:2.5%}}
.hero-inner{{position:relative;z-index:2;max-width:900px;margin:0 auto}}
.hero-tag{{display:inline-block;font-family:var(--font-mono);font-size:11.5px;letter-spacing:3px;color:var(--accent-warm);border:1px solid rgba(184,92,56,0.45);border-radius:var(--radius-full);padding:7px 20px;margin-bottom:30px;background:rgba(255,253,247,0.65)}}
.hero h1{{font-size:clamp(2.6rem,7vw,4.6rem);color:var(--color-primary);margin-bottom:8px;letter-spacing:2px}}
.hero h1 .hl{{position:relative;color:var(--accent-warm);white-space:nowrap}}
.hero h1 .hl::after{{content:'';position:absolute;left:-2%;right:-2%;bottom:6px;height:10px;background:var(--accent-soft);opacity:0.55;z-index:-1;border-radius:2px}}
.hero-sub2{{font-family:var(--font-display);font-size:clamp(1.05rem,2.4vw,1.4rem);color:var(--text-secondary);letter-spacing:1px;margin-bottom:22px}}
.hero-desc{{max-width:720px;margin:0 auto 34px;color:var(--text-secondary);font-size:16.5px}}
.hero-desc b{{color:var(--color-primary)}}
.motto{{font-family:var(--font-display);letter-spacing:6px;color:var(--accent-gold);font-size:14.5px;margin:30px 0 0}}
.motto small{{display:block;letter-spacing:2px;color:var(--text-muted);font-size:12px;margin-top:6px}}
.hero-cta{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:6px}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:12px 30px;border-radius:var(--radius-md);font-size:13.5px;letter-spacing:2px;font-family:var(--font-body);transition:all .35s var(--ease-out);border:1px solid transparent;cursor:pointer}}
.btn-primary{{background:var(--color-primary);color:#FBF8F1}}
.btn-primary:hover{{background:var(--accent-warm);transform:translateY(-2px);box-shadow:var(--shadow-md)}}
.btn-outline{{border-color:var(--color-primary);color:var(--color-primary);background:transparent}}
.btn-outline:hover{{background:var(--color-primary);color:#FBF8F1;transform:translateY(-2px)}}

/* stats bar — 双层边框（签名元素之一） */
.stats{{position:relative;max-width:1040px;margin:56px auto 0;background:linear-gradient(180deg,var(--bg-secondary),#EFE8D8);border:2px solid var(--color-primary);border-radius:var(--radius-lg);padding:26px 20px}}
.stats::before{{content:'';position:absolute;inset:6px;border:1px solid var(--accent-gold);opacity:0.55;border-radius:10px;pointer-events:none}}
.stats-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;position:relative}}
.stat b{{display:block;font-family:var(--font-display);font-size:clamp(1.5rem,3vw,2.1rem);color:var(--color-primary)}}
.stat span{{font-size:12.5px;color:var(--text-muted);letter-spacing:1.5px}}

/* ---------- sections ---------- */
.section{{position:relative;padding:92px 0}}
.section.alt{{background:linear-gradient(180deg,var(--bg-secondary) 0%,var(--bg-primary) 100%);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.section-head{{text-align:center;margin-bottom:52px;position:relative}}
.section-tag{{font-family:var(--font-mono);font-size:11.5px;letter-spacing:4px;color:var(--accent-warm);text-transform:uppercase}}
.section-title{{font-size:clamp(1.7rem,3.4vw,2.6rem);color:var(--color-primary);margin:12px 0 10px;letter-spacing:2px}}
.section-sub{{color:var(--text-secondary);max-width:640px;margin:0 auto;font-size:15.5px}}
.classical-line{{width:210px;height:9px;margin:18px auto 0;position:relative}}
.classical-line::before{{content:'';position:absolute;left:0;right:0;top:4px;height:1px;background:linear-gradient(90deg,transparent,var(--accent-gold) 18%,var(--accent-gold) 82%,transparent)}}
.classical-line::after{{content:'';position:absolute;left:50%;top:1px;width:7px;height:7px;margin-left:-3.5px;background:var(--accent-warm);transform:rotate(45deg)}}

/* ---------- guide: four arts ---------- */
.arts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:22px}}
.art{{background:#FFFDF7;border:1px solid var(--bg-tertiary);border-radius:var(--radius-lg);padding:30px 26px 26px;transition:all .4s var(--ease-out);position:relative;overflow:hidden}}
.art::before{{content:'';position:absolute;top:0;left:0;right:0;height:12px;background-image:var(--meander-gold);background-size:14px 14px;opacity:0.65}}
.art:hover{{transform:translateY(-8px);border-color:var(--accent-gold);box-shadow:var(--shadow-lg)}}
.art .gr{{font-family:var(--font-display);font-size:19px;color:var(--accent-gold);letter-spacing:3px}}
.art h3{{font-size:19px;color:var(--color-primary);margin:8px 0 10px}}
.art p{{font-size:14.5px;color:var(--text-secondary)}}
.guide-lead{{max-width:760px;margin:0 auto 46px;text-align:center;color:var(--text-secondary);font-size:16px}}
.guide-lead b{{color:var(--color-primary)}}
.paths{{margin-top:44px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}
.path{{background:var(--bg-secondary);border:1px solid var(--bg-tertiary);border-radius:var(--radius-lg);padding:22px 24px}}
.path .pl{{font-family:var(--font-mono);font-size:11px;letter-spacing:2px;color:var(--accent-warm)}}
.path h4{{font-size:16.5px;color:var(--color-primary);margin:6px 0 10px}}
.path .seq{{font-size:14px;color:var(--text-secondary);line-height:2.1}}
.path .seq a{{border-bottom:1px dotted var(--accent-gold);transition:color .3s}}
.path .seq a:hover{{color:var(--accent-warm)}}
.path .seq .sep{{color:var(--accent-gold);margin:0 6px}}
.path small{{display:block;margin-top:10px;color:var(--text-muted);font-size:12.5px}}

/* ---------- twelve tomes ---------- */
.tome-group{{margin-bottom:74px}}
.tome-group:last-child{{margin-bottom:0}}
.group-head{{display:grid;grid-template-columns:auto 1fr;gap:8px 20px;align-items:center;margin-bottom:30px;padding-bottom:18px;border-bottom:1px solid var(--line);position:relative}}
.group-head::after{{content:'';position:absolute;left:0;bottom:-1.5px;width:120px;height:3px;background:var(--accent-gold)}}
.group-letter{{grid-row:span 2;font-family:var(--font-display);font-size:clamp(2.4rem,5vw,3.4rem);color:var(--accent-gold);line-height:1;opacity:0.9}}
.group-name{{font-size:clamp(1.25rem,2.4vw,1.6rem);color:var(--color-primary);letter-spacing:1px}}
.group-tag{{font-family:var(--font-mono);font-size:11px;letter-spacing:2.5px;color:var(--text-muted)}}
.group-note{{grid-column:1/-1;color:var(--text-secondary);font-size:14.5px;max-width:820px}}

.card-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:26px}}
.card-grid.with-aside{{grid-template-columns:repeat(auto-fill,minmax(310px,1fr))}}
.group-aside{{display:flex;flex-direction:column;gap:12px;background:linear-gradient(180deg,#F7F1E2,#F2EADA);border:1px dashed rgba(192,154,84,0.7);border-radius:var(--radius-lg);padding:26px 24px;justify-content:center}}
.aside-kicker{{font-family:var(--font-mono);font-size:11px;letter-spacing:3px;color:var(--accent-warm)}}
.aside-lead{{font-family:var(--font-display);font-size:16px;color:var(--color-primary);line-height:1.75}}
.group-aside ul{{list-style:none;display:grid;gap:10px}}
.group-aside li{{position:relative;padding-left:20px;font-size:13.5px;color:var(--text-secondary);line-height:1.75}}
.group-aside li::before{{content:'—';position:absolute;left:0;color:var(--accent-gold)}}
.card{{background:#FFFDF7;border:1px solid var(--bg-tertiary);border-radius:var(--radius-lg);overflow:hidden;display:flex;flex-direction:column;transition:all .45s var(--ease-out)}}
.card:hover{{transform:translateY(-8px);border-color:var(--accent-gold);box-shadow:var(--shadow-lg)}}
.plate{{position:relative;display:block;height:178px;overflow:hidden;background:var(--bg-secondary)}}
.plate-img{{width:100%;height:100%;object-fit:cover;filter:sepia(0.18) saturate(0.92);transition:transform .6s var(--ease-out),filter .6s}}
.card:hover .plate-img{{transform:scale(1.05);filter:sepia(0.05) saturate(1)}}
.plate-emblem{{width:100%;height:100%}}
.plate-veil{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(43,36,25,0) 46%,rgba(43,36,25,0.42) 100%);pointer-events:none}}
.plate-num{{position:absolute;top:10px;left:12px;z-index:2;font-family:var(--font-display);font-size:15px;color:#FBF8F1;background:rgba(74,58,40,0.78);border:1px solid rgba(192,154,84,0.75);border-radius:var(--radius-sm);padding:1px 9px;letter-spacing:1px}}
.venue{{position:absolute;left:12px;right:12px;bottom:10px;z-index:2;font-family:var(--font-mono);font-size:10.5px;letter-spacing:1px;color:#F6EFDD;text-shadow:0 1px 6px rgba(0,0,0,0.5)}}
.card-body{{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}}
.card-top{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}}
.swatches{{display:inline-flex;gap:5px}}
.swatches i{{width:11px;height:11px;border-radius:50%;background:var(--c);border:1px solid rgba(43,36,25,0.18);display:inline-block}}
.card-meta{{font-family:var(--font-mono);font-size:10.5px;color:var(--text-muted);letter-spacing:0.5px;text-align:right}}
.card h3{{font-size:19.5px;color:var(--color-primary);margin-bottom:4px}}
.card h3 a{{transition:color .3s}}
.card h3 a:hover{{color:var(--accent-warm)}}
.card-en{{font-family:var(--font-display);font-size:13px;font-style:italic;color:var(--text-muted);margin-bottom:10px;line-height:1.5}}
.card-desc{{font-size:14.5px;color:var(--text-secondary);flex:1;margin-bottom:16px}}
.card-links{{display:flex;gap:8px;flex-wrap:wrap}}
.card-links .btn{{padding:8px 16px;font-size:12.5px;letter-spacing:1.5px;border-radius:var(--radius-sm)}}
.btn-ghost{{border-color:var(--line);color:var(--text-secondary);background:transparent}}
.btn-ghost:hover{{border-color:var(--accent-warm);color:var(--accent-warm);transform:translateY(-2px)}}

/* ---------- constellation ---------- */
.constellation-wrap{{position:relative;background:#FFFDF7;border:1px solid var(--bg-tertiary);border-radius:var(--radius-lg);padding:26px 18px 12px;overflow:hidden}}
.constellation-wrap::before{{content:'';position:absolute;inset:0;background-image:var(--meander-gold);background-size:14px 14px;height:12px;opacity:0.5;pointer-events:none}}
.astrolabe{{width:100%;height:auto;display:block}}
.const-note{{max-width:840px;margin:34px auto 0;text-align:center;color:var(--text-secondary);font-size:15.5px}}
.const-note b{{color:var(--accent-warm)}}

/* ---------- lighthouse / Mu Lab ---------- */
.lab-wrap{{position:relative;background:linear-gradient(180deg,#FFFDF7,#F7F1E2);border:2px solid var(--color-primary);border-radius:var(--radius-lg);padding:52px 46px;overflow:hidden}}
.lab-wrap::before{{content:'';position:absolute;inset:7px;border:1px solid var(--accent-gold);opacity:0.5;border-radius:9px;pointer-events:none}}
.corner-key{{position:absolute;width:86px;height:86px;opacity:0.5;pointer-events:none}}
.corner-key.tl{{top:14px;left:14px}} .corner-key.br{{bottom:14px;right:14px;transform:rotate(180deg)}}
.lab-amphora{{position:absolute;right:46px;bottom:34px;width:96px;opacity:0.14;pointer-events:none;color:var(--color-primary)}}
.lab-grid{{position:relative;display:grid;grid-template-columns:1.05fr 0.95fr;gap:44px;align-items:start}}
.lab-quote{{font-family:var(--font-display);font-size:clamp(1.1rem,2.1vw,1.35rem);color:var(--color-primary);line-height:1.85;border-left:3px solid var(--accent-warm);padding-left:22px;margin:18px 0 22px}}
.lab-quote small{{display:block;margin-top:10px;font-family:var(--font-body);font-size:12.5px;color:var(--text-muted);letter-spacing:1px}}
.lab-args{{list-style:none;display:grid;gap:12px;margin:0 0 6px}}
.lab-args li{{position:relative;padding-left:26px;font-size:14.5px;color:var(--text-secondary)}}
.lab-args li::before{{content:'◆';position:absolute;left:2px;top:0;font-size:10px;color:var(--accent-gold)}}
.lab-args b{{color:var(--color-primary)}}
.repo-list{{display:grid;gap:9px}}
.repo-row{{display:grid;grid-template-columns:auto minmax(112px,auto) 1fr auto;gap:12px;align-items:center;background:#FFFDF7;border:1px solid var(--bg-tertiary);border-radius:var(--radius-md);padding:10px 14px;transition:all .35s var(--ease-out)}}
.repo-row:hover{{transform:translateX(6px);border-color:var(--accent-gold);box-shadow:var(--shadow-sm)}}
.repo-mark{{font-size:10.5px;letter-spacing:1px;padding:2px 9px;border-radius:var(--radius-full);border:1px solid;white-space:nowrap}}
.mark-guide{{color:#B85C38;border-color:#B85C38;background:rgba(184,92,56,0.07)}}
.mark-collection{{color:#C09A54;border-color:#C09A54;background:rgba(192,154,84,0.09)}}
.mark-repo{{color:#5D5344;border-color:var(--line);background:transparent}}
.repo-name{{font-family:var(--font-display);font-weight:700;font-size:14.5px;color:var(--color-primary)}}
.repo-desc{{font-size:12.5px;color:var(--text-muted);line-height:1.5}}
.repo-arrow{{color:var(--accent-gold);font-size:14px}}
.lab-note{{margin-top:26px;font-size:13px;color:var(--text-muted)}}
.lab-note a{{border-bottom:1px dotted var(--accent-gold)}}

/* ---------- codex / repo map ---------- */
.codex-grid{{display:grid;grid-template-columns:1.1fr 0.9fr;gap:40px;align-items:start}}
.tree{{background:#2E2820;color:#E8DFCB;border-radius:var(--radius-lg);padding:26px 26px;font-family:var(--font-mono);font-size:13px;line-height:2;overflow-x:auto;box-shadow:var(--shadow-md);white-space:pre}}
.tree .dim{{color:#9C8F76}} .tree .gold{{color:#D8B96C}} .tree .terra{{color:#E0996F}}
.codex-list{{list-style:none;display:grid;gap:16px}}
.codex-list li{{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start}}
.codex-list .k{{font-family:var(--font-display);font-size:15px;color:var(--accent-gold);letter-spacing:1px;padding-top:2px;white-space:nowrap}}
.codex-list p{{font-size:14px;color:var(--text-secondary)}}
.codex-list b{{color:var(--color-primary)}}

/* ---------- footer ---------- */
footer{{position:relative;background:linear-gradient(180deg,var(--bg-secondary),#EDE4D2);border-top:1px solid var(--line);padding:70px 24px 44px;text-align:center;overflow:hidden}}
.foot-frieze{{position:absolute;top:0;left:0;right:0;height:16px;background-image:var(--meander);background-size:14px 14px;opacity:0.4}}
.temple{{width:110px;margin:0 auto 20px;color:var(--color-primary);opacity:0.75}}
.foot-motto{{font-family:var(--font-display);letter-spacing:7px;color:var(--color-primary);font-size:17px}}
.foot-sub{{color:var(--text-muted);font-size:13px;margin-top:10px}}
.foot-links{{display:flex;gap:20px;justify-content:center;margin:24px 0 8px;flex-wrap:wrap;font-size:13px}}
.foot-links a{{color:var(--text-secondary);transition:color .3s;position:relative}}
.foot-links a:hover{{color:var(--accent-warm)}}
.foot-note{{color:var(--text-muted);font-size:12px;max-width:720px;margin:16px auto 0;line-height:1.9}}

/* ---------- motion ---------- */
.reveal{{opacity:0;transform:translateY(26px);transition:opacity .8s var(--ease-out),transform .8s var(--ease-out)}}
.reveal.in{{opacity:1;transform:none}}
html.no-js .reveal, body.anim-off .reveal{{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){{
  html{{scroll-behavior:auto}}
  *{{transition-duration:0.01ms !important;animation-duration:0.01ms !important}}
  .reveal{{opacity:1;transform:none}}
}}

/* ---------- responsive ---------- */
@media (max-width:1080px){{
  .lab-grid,.codex-grid{{grid-template-columns:1fr}}
  .hero-col{{display:none}}
  .lab-amphora{{display:none}}
}}
@media (max-width:860px){{
  .stats-grid{{grid-template-columns:repeat(2,1fr);row-gap:18px}}
  .stat:last-child{{grid-column:1/-1}}
  .hero-sun{{width:420px;height:420px}}
  .group-letter{{font-size:2.2rem}}
}}
@media (max-width:560px){{
  body{{font-size:16px}}
  .section{{padding:66px 0}}
  .hero{{padding:84px 18px 60px}}
  .lab-wrap{{padding:34px 22px}}
  .card-grid{{grid-template-columns:1fr}}
  .frieze{{opacity:0.35}}
}}
</style>
</head>
<body>

<nav aria-label="主导航">
  <div class="nav-inner">
    <span class="nav-brand"><span class="gr">ΓΝΩΘΙ</span> ΣΑΥΤΟΝ · MHML 深读指南</span>
    <a class="nav-link" href="#guide">卷一 · 深读四艺</a>
    <a class="nav-link" href="#scrolls">卷二 · 十二卷</a>
    <a class="nav-link" href="#constellation">卷三 · 谱系星图</a>
    <a class="nav-link" href="#lab">卷四 · 参照坐标</a>
    <a class="nav-link" href="#codex">卷五 · 仓库地图</a>
  </div>
</nav>

<!-- ================= HERO ================= -->
<header class="hero">
  <div class="frieze" aria-hidden="true"></div>
  <svg class="hero-sun" viewBox="0 0 400 400" aria-hidden="true">
    <circle cx="200" cy="200" r="190" fill="none" stroke="#C09A54" stroke-width="1.2"/>
    <circle cx="200" cy="200" r="150" fill="none" stroke="#C09A54" stroke-width="0.8" stroke-dasharray="3 7"/>
    <circle cx="200" cy="200" r="105" fill="none" stroke="#4A3A28" stroke-width="0.8"/>
    <circle cx="200" cy="200" r="58" fill="none" stroke="#B85C38" stroke-width="1"/>
    <g stroke="#C09A54" stroke-width="1.1">
      <line x1="200" y1="10" x2="200" y2="28"/><line x1="200" y1="372" x2="200" y2="390"/>
      <line x1="10" y1="200" x2="28" y2="200"/><line x1="372" y1="200" x2="390" y2="200"/>
      <line x1="66" y1="66" x2="79" y2="79"/><line x1="321" y1="321" x2="334" y2="334"/>
      <line x1="334" y1="66" x2="321" y2="79"/><line x1="79" y1="321" x2="66" y2="334"/>
    </g>
  </svg>
  <svg class="hero-col l" viewBox="0 0 60 460" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.6">
      <rect x="4" y="2" width="52" height="10"/>
      <path d="M12 12 h36 l5 13 h-46 z"/>
      <line x1="15" y1="25" x2="45" y2="25"/>
      <rect x="16" y="31" width="28" height="382"/>
      <line x1="21" y1="31" x2="21" y2="413"/><line x1="26" y1="31" x2="26" y2="413"/>
      <line x1="30" y1="31" x2="30" y2="413"/><line x1="34" y1="31" x2="34" y2="413"/>
      <line x1="39" y1="31" x2="39" y2="413"/>
      <rect x="12" y="413" width="36" height="8"/>
      <rect x="6" y="421" width="48" height="9"/>
    </g>
  </svg>
  <svg class="hero-col r" viewBox="0 0 60 460" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.6">
      <rect x="4" y="2" width="52" height="10"/>
      <path d="M12 12 h36 l5 13 h-46 z"/>
      <line x1="15" y1="25" x2="45" y2="25"/>
      <rect x="16" y="31" width="28" height="382"/>
      <line x1="21" y1="31" x2="21" y2="413"/><line x1="26" y1="31" x2="26" y2="413"/>
      <line x1="30" y1="31" x2="30" y2="413"/><line x1="34" y1="31" x2="34" y2="413"/>
      <line x1="39" y1="31" x2="39" y2="413"/>
      <rect x="12" y="413" width="36" height="8"/>
      <rect x="6" y="421" width="48" height="9"/>
    </g>
  </svg>
  <div class="hero-inner">
    <span class="hero-tag">RECURSIVE SELF-IMPROVEMENT · A READING GUIDE</span>
    <h1><span class="hl">RSI</span> 深读指南</h1>
    <p class="hero-sub2">自改进之径 · 十二篇论文 · 五个容器</p>
    <p class="hero-desc">沿 <b>In-Parameter Learning</b> 纲领的问题线索（Mu Lab 立场论文）：新知识应该住在哪里——上下文、权重、生成器、在线状态，还是测试时的梯度？十二篇深度解读，一条从<b>模型编辑</b>到<b>测试时训练</b>的自改进之路。</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#scrolls">开启十二卷</a>
      <a class="btn btn-outline" href="#lab">纲领参照</a>
    </div>
    <p class="motto">ΓΝΩΘΙ ΣΑΥΤΟΝ<small>「认识你自己」——自改进研究的起点</small></p>
    <div class="stats" role="list">
      <div class="stats-grid">
        <div class="stat" role="listitem"><b>12</b><span>篇论文深读</span></div>
        <div class="stat" role="listitem"><b>157</b><span>个章节</span></div>
        <div class="stat" role="listitem"><b>12</b><span>份论文原文</span></div>
        <div class="stat" role="listitem"><b>45+</b><span>组内联图表</span></div>
        <div class="stat" role="listitem"><b>5</b><span>大容器谱系</span></div>
      </div>
    </div>
  </div>
</header>

<!-- ================= 01 GUIDE ================= -->
<section class="section" id="guide">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Volume I · ΤΕΧΝΗ</span>
      <h2 class="section-title">深读四艺</h2>
      <p class="section-sub">每篇博客遵循同一套工艺：从零建立坐标系 → 数学谱系 → 实验逐表精读 → 法证批判 → 开放问题与复现入口。</p>
      <div class="classical-line" aria-hidden="true"></div>
    </div>
    <p class="guide-lead reveal">不是论文摘要，而是<b>陪读者走完全程</b>：每篇 10–18 章、含公式变量表与反事实分析、逐条取证论文内部矛盾、
    并给出可动手的研究问题卡。目标只有一个：<b>读完一篇 ≈ 该方向入门到能独立提出科研问题</b>。</p>
    <div class="arts">
      <div class="art reveal">
        <span class="gr">ΜΑΘΗΜΑ</span>
        <h3>数学推导</h3>
        <p>每个公式配变量表、直觉与反事实分析——去掉这一项会发生什么；关键推导链逐步复算，公式全部经 PDF 全文提取核对。</p>
      </div>
      <div class="art reveal">
        <span class="gr">ΚΡΙΣΙΣ</span>
        <h3>法证批判</h3>
        <p>每条批判遵循「证据 → 推理 → 影响 → 补救」四段式，含论文内部矛盾与数据异常的逐条取证，不放过一句自相矛盾的表述。</p>
      </div>
      <div class="art reveal">
        <span class="gr">ΖΗΤΗΣΙΣ</span>
        <h3>研究问题</h3>
        <p>每篇 5 张科研问题卡，从零成本可验证的小实验到理论方向分级排列——把读者从"看懂"推向"能提问题"。</p>
      </div>
      <div class="art reveal">
        <span class="gr">ΠΡΑΞΙΣ</span>
        <h3>复现入口</h3>
        <p>代码块按可信度标注（可运行 / 示意），给出最小复刻路线与对照实验设计；论文原图精准裁剪、全文提取留档备查。</p>
      </div>
    </div>
    <div class="paths">
      <div class="path reveal">
        <span class="pl">PATH · 时间有限</span>
        <h4>入门三篇</h4>
        <div class="seq"><a href="blogs/delmem/index.html">δ-mem</a><span class="sep">→</span><a href="blogs/dnd/index.html">DnD</a><span class="sep">→</span><a href="blogs/ttt-e2e/index.html">TTT-E2E</a></div>
        <small>在线记忆总览问题 → 生成参数看全景 → 测试时训练看前沿。</small>
      </div>
      <div class="path reveal">
        <span class="pl">PATH · 生成参数主线</span>
        <h4>超网络七卷</h4>
        <div class="seq"><a href="blogs/rpg/index.html">RPG</a><span class="sep">→</span><a href="blogs/text2lora/index.html">Text-to-LoRA</a><span class="sep">→</span><a href="blogs/genadapter/index.html">GenAdapter</a><span class="sep">→</span><a href="blogs/dyprag/index.html">DyPRAG</a><span class="sep">→</span><a href="blogs/dnd/index.html">DnD</a><span class="sep">→</span><a href="blogs/shine/index.html">SHINE</a><span class="sep">→</span><a href="blogs/d2l/index.html">D2L</a></div>
        <small>从"生成权重"的第一性形式走到单次前向把长文档炼成 LoRA 的 2026 前沿。</small>
      </div>
      <div class="path reveal">
        <span class="pl">PATH · 自改进两端</span>
        <h4>从静态编辑到就地学习</h4>
        <div class="seq"><a href="blogs/mend/index.html">MEND</a><span class="sep">→</span><a href="blogs/inplace-ttt/index.html">In-Place TTT</a></div>
        <small>一端是 2022 年的权重手术刀，一端是 2026 年的就地快权重——同一条"参数更新"光谱的对照。</small>
      </div>
    </div>
  </div>
</section>

<!-- ================= 02 SCROLLS ================= -->
<section class="section alt" id="scrolls">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Volume II · ΙΒ ΤΟΜΟΙ</span>
      <h2 class="section-title">十二卷</h2>
      <p class="section-sub">按五容器谱系分组：静态参数 → 生成参数 → 在线状态 → 测试时梯度。每卷均可独立成篇，也可沿谱系连读。</p>
      <div class="classical-line" aria-hidden="true"></div>
    </div>
{cards_block}
  </div>
</section>

<!-- ================= 03 CONSTELLATION ================= -->
<section class="section" id="constellation">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Volume III · ΑΣΤΡΟΛΑΒΟΣ</span>
      <h2 class="section-title">谱系星图</h2>
      <p class="section-sub">五个容器，一张星图——所有方法都在回答同一个问题：新知识住在哪里？</p>
      <div class="classical-line" aria-hidden="true"></div>
    </div>
    <div class="constellation-wrap reveal">
{constellation}
    </div>
    <p class="const-note reveal">从 <b>ICL</b>（全上下文）出发，参数化的路径逐渐分叉：<b>静态参数</b>在被冻结的权重上做手术；
    <b>生成参数</b>用超网络一次前向造出增量权重；<b>在线状态</b>在权重之外维护一块持续读写的记忆；
    <b>测试时梯度</b>干脆在推理期跑内环学习。它们不是替代关系，而是一组可组合的容器——
    这也是 Mu Lab 纲领中「ICL 与 In-Parameter Learning 互补」的工程学注脚。</p>
  </div>
</section>

<!-- ================= 04 LIGHTHOUSE ================= -->
<section class="section alt" id="lab">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Volume IV · ΦΑΡΟΣ</span>
      <h2 class="section-title">参照坐标 · In-Parameter Learning</h2>
      <p class="section-sub">谱系线索参考 Mu Lab 的立场论文《In-Parameter Learning》。本仓库由 Yetbye 独立整理，与 Mu Lab 无隶属关系。</p>
      <div class="classical-line" aria-hidden="true"></div>
    </div>
    <div class="lab-wrap reveal">
      <svg class="corner-key tl" viewBox="0 0 100 100" aria-hidden="true">
        <path d="M0 22 H78 M22 0 V78" stroke="#C09A54" stroke-width="1.4" fill="none"/>
        <path d="M12 96 V12 H96" stroke="#B85C38" stroke-width="1" fill="none" opacity="0.55"/>
        <path d="M30 90 V30 H90" stroke="#4A3A28" stroke-width="1" fill="none" opacity="0.3"/>
      </svg>
      <svg class="corner-key br" viewBox="0 0 100 100" aria-hidden="true">
        <path d="M0 22 H78 M22 0 V78" stroke="#C09A54" stroke-width="1.4" fill="none"/>
        <path d="M12 96 V12 H96" stroke="#B85C38" stroke-width="1" fill="none" opacity="0.55"/>
        <path d="M30 90 V30 H90" stroke="#4A3A28" stroke-width="1" fill="none" opacity="0.3"/>
      </svg>
      <svg class="lab-amphora" viewBox="0 0 120 160" aria-hidden="true">
        <g fill="none" stroke="currentColor" stroke-width="2">
          <path d="M52 4 h16 v12 c0 6 -4 8 -8 8 s-8 -2 -8 -8 z"/>
          <path d="M60 24 c26 2 40 22 40 46 c0 30 -16 48 -40 52 c-24 -4 -40 -22 -40 -52 c0 -24 14 -44 40 -46 z"/>
          <path d="M26 78 h68"/>
          <path d="M30 88 h60"/>
          <path d="M20 40 c-12 6 -14 22 -2 28 M100 40 c12 6 14 22 2 28"/>
          <path d="M50 122 h20 l4 12 h-28 z"/>
          <path d="M42 134 h36 v6 h-36 z"/>
        </g>
      </svg>
      <div class="lab-grid">
        <div>
          <span class="section-tag">POSITION PAPER · 2026</span>
          <h3 style="font-size:clamp(1.3rem,2.6vw,1.8rem);color:var(--color-primary);margin:10px 0 4px">In-Parameter Learning</h3>
          <p style="font-family:var(--font-mono);font-size:11.5px;letter-spacing:1.5px;color:var(--text-muted)">WHY LIFELONG AI SYSTEMS NEED MORE THAN LONGER CONTEXT</p>
          <blockquote class="lab-quote">「现有 in-context 机制不足以支撑终身 AI；未来的终身系统应建立在混合范式之上——ICL 负责即时的、临时的、可逆的信息，In-Parameter Learning 负责持久的、累积的、可泛化的成长。」
            <small>—— 译自 Mu Lab 立场论文（Norizon AI / PKU / MIT / Tencent Youtu）· 引用不构成隶属</small></blockquote>
          <ul class="lab-args">
            <li><b>上下文有硬上限</b>：终身经验的保守估计也超出当前百万 token 前沿数个数量级。</li>
            <li><b>长度 scaling 有三重障碍</b>：计算、数据与架构层面的根本性困难。</li>
            <li><b>参数学习抬高能力天花板</b>：把新知识固化进权重——累积增长、更好泛化、推理开销更低。</li>
            <li><b>ICL 与 IPL 互补而非竞争</b>：本指南的十二卷，正是 IPL 纲领下「参数更新容器」的全景测绘。</li>
          </ul>
        </div>
        <div>
          <span class="section-tag">相关仓库 · GITHUB / MULABPKU</span>
          <div class="repo-list" style="margin-top:14px">
        {repos_block}
          </div>
          <p class="lab-note">两条与本指南直接相关的线索：卷 Ⅶ <b>SHINE</b> 出自 Mu Lab（ICML 2026 · PMLR 306）；
          卷 Ⅻ <b>In-Place TTT</b> 为 ByteDance Seed × PKU 合作。本指南沿 IPL 的问题线索独立组织谱系（非官方）。参考
          <a href="https://github.com/MuLabPKU" target="_blank" rel="noopener">github.com/MuLabPKU</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ================= 05 CODEX ================= -->
<section class="section" id="codex">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Volume V · ΧΑΡΤΗΣ</span>
      <h2 class="section-title">仓库地图</h2>
      <p class="section-sub">一个自包含的静态站点：无构建步骤，克隆后直接打开 index.html。</p>
      <div class="classical-line" aria-hidden="true"></div>
    </div>
    <div class="codex-grid">
      <div class="tree reveal" aria-label="仓库目录结构">
<span class="gold">RSI/</span>                        <span class="dim"># MHML · RSI 深读指南</span>
├── <span class="gold">index.html</span>            <span class="dim"># 本门户（Venus 希腊暖金）</span>
├── <span class="gold">blogs/</span>                <span class="dim"># 12 篇深读 · 自包含单文件 HTML</span>
│   ├── <span class="terra">mend/</span>  <span class="terra">rpg/</span>  <span class="terra">genadapter/</span>  <span class="terra">dyprag/</span>
│   ├── <span class="terra">text2lora/</span>  <span class="terra">dnd/</span>  <span class="terra">shine/</span>  <span class="terra">d2l/</span>
│   └── <span class="terra">delmem/</span>  <span class="terra">unimem/</span>  <span class="terra">ttt-e2e/</span>  <span class="terra">inplace-ttt/</span>
├── <span class="gold">papers/</span>
│   ├── pdf/              <span class="dim"># 12 篇论文原文</span>
│   └── text/             <span class="dim"># 12 份全文提取（公式核对依据）</span>
└── <span class="gold">logs/</span>                 <span class="dim"># 构建日志 · 偏好档案 · 门户脚本</span>
      </div>
      <ul class="codex-list reveal">
        <li><span class="k">离线友好</span><p>每篇深读为<b>单文件 HTML</b>，封面与图表随目录存放；公式由 MathJax 渲染（首次需联网，之后浏览器缓存）。</p></li>
        <li><span class="k">证据链</span><p><b>papers/text/</b> 保留 PDF 全文提取，博客中每个公式与数字都可在其中核对原文出处。</p></li>
        <li><span class="k">复现实验</span><p>各卷附最小复刻路线与对照实验设计；配置好百炼 key 后可按 <b>_genimg.py</b> 管线重生成插图。</p></li>
        <li><span class="k">扩展一卷</span><p>新增论文时：在 <b>blogs/</b> 放深读、在 <b>papers/</b> 放原文与提取，然后重跑 <b>logs/build_portal.py</b> 更新本门户目录表。</p></li>
      </ul>
    </div>
  </div>
</section>

<!-- ================= FOOTER ================= -->
<footer>
  <div class="foot-frieze" aria-hidden="true"></div>
  <svg class="temple" viewBox="0 0 120 74" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.8">
      <path d="M6 26 L60 4 L114 26 Z"/>
      <line x1="0" y1="26" x2="120" y2="26"/>
      <line x1="8" y1="32" x2="112" y2="32"/>
      <line x1="18" y1="32" x2="18" y2="62"/><line x1="40" y1="32" x2="40" y2="62"/>
      <line x1="60" y1="32" x2="60" y2="62"/>
      <line x1="80" y1="32" x2="80" y2="62"/><line x1="102" y1="32" x2="102" y2="62"/>
      <line x1="8" y1="62" x2="112" y2="62"/>
      <rect x="2" y="66" width="116" height="5"/>
    </g>
  </svg>
  <p class="foot-motto">ΓΝΩΘΙ ΣΑΥΤΟΝ</p>
  <p class="foot-sub">MHML · RSI 深读指南 —— Yetbye 独立整理 · 谱系线索参考 In-Parameter Learning 纲领</p>
  <div class="foot-links">
    <a href="#guide">深读四艺</a><a href="#scrolls">十二卷</a><a href="#constellation">谱系星图</a>
    <a href="#lab">参照坐标</a><a href="#codex">仓库地图</a>
    <a href="https://github.com/MuLabPKU" target="_blank" rel="noopener">github.com/MuLabPKU</a>
  </div>
  <p class="foot-note">论文版权归原作者所有；各卷解读为本仓库原创深读文本，观点与批判不代表论文作者立场。
  封面与插图部分由 AI 生成或基于论文原图裁剪，仅作学习用途。敬告读者：一切引用请回到 <b>papers/</b> 原文核对。</p>
</footer>

<script>
document.documentElement.classList.remove('no-js');
(function(){{
  var els=document.querySelectorAll('.reveal');
  function showAll(){{ els.forEach(function(e){{ e.classList.add('in'); }}); }}
  if(!('IntersectionObserver' in window)){{ showAll(); return; }}
  var io=new IntersectionObserver(function(entries){{
    entries.forEach(function(en){{ if(en.isIntersecting){{en.target.classList.add('in');io.unobserve(en.target);}} }});
  }},{{threshold:0.12,rootMargin:'0px 0px -40px 0px'}});
  els.forEach(function(e){{io.observe(e)}});
  /* 兜底：无论视口/环境如何，2 秒后全部显影，避免任何内容被动画状态永久隐藏 */
  window.setTimeout(showAll, 2000);
}})();
</script>
</body>
</html>
'''
    out = os.path.join(ROOT, "index.html")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print("WROTE", out, len(page.encode("utf-8")), "bytes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build()
