# -*- coding: utf-8 -*-
"""One-off migration: organize RSI blog folders into a clean repository layout.

Layout after migration:
  blogs/<slug>/index.html ...  12 deep-reading blogs (self-contained)
  papers/pdf/<slug>.pdf       canonical paper PDFs (12 unique, dupes removed)
  papers/text/<slug>.txt      PDF text extracts (12)
  logs/                       build logs & preference profile
"""
import hashlib
import os
import shutil
import sys

ROOT = r"D:\success\RSI"
os.chdir(ROOT)

BLOG_MOVES = {
    "d2l_blog": "blogs/d2l",
    "delmem_blog": "blogs/delmem",
    "dnd_blog": "blogs/dnd",
    "dyprag_blog": "blogs/dyprag",
    "e2ettt_blog": "blogs/ttt-e2e",
    "genadapter_blog": "blogs/genadapter",
    "ipttt_blog": "blogs/inplace-ttt",
    "memit_blog": "blogs/mend",
    "rpg_blog": "blogs/rpg",
    "shine_blog": "blogs/shine",
    "text2lora_blog": "blogs/text2lora",
    "unimem_blog": "blogs/unimem",
}

PDF_MOVES = {
    "DND.pdf": "papers/pdf/dnd.pdf",
    "Doc-to-LoRA.pdf": "papers/pdf/doc-to-lora.pdf",
    "Fast Model Editing at Scale.pdf": "papers/pdf/mend.pdf",
    "Generative Adapter.pdf": "papers/pdf/generative-adapter.pdf",
    "RPG.pdf": "papers/pdf/rpg.pdf",
    "SHINE.pdf": "papers/pdf/shine.pdf",
    "Text-to-LoRA.pdf": "papers/pdf/text-to-lora.pdf",
    "UniMem.pdf": "papers/pdf/unimem.pdf",
    "del-mem.pdf": "papers/pdf/delmem.pdf",
    "dyprag.pdf": "papers/pdf/dyprag.pdf",
    "e2e ttt.pdf": "papers/pdf/ttt-e2e.pdf",
    "inplace ttt.pdf": "papers/pdf/inplace-ttt.pdf",
}

# blog-local copies of the very same PDFs (verified byte-identical) -> removed
DUP_PDFS = [
    "dyprag_blog/dyprag.pdf",
    "genadapter_blog/genadapter.pdf",
    "rpg_blog/rpg.pdf",
    "shine_blog/shine.pdf",
    "text2lora_blog/paper.pdf",
    "unimem_blog/paper.pdf",
]

TXT_MOVES = {
    "d2l_text.txt": "papers/text/d2l.txt",
    "delmem_text.txt": "papers/text/delmem.txt",
    "dnd_text.txt": "papers/text/dnd.txt",
    "e2ettt_text.txt": "papers/text/ttt-e2e.txt",
    "ipttt_text.txt": "papers/text/inplace-ttt.txt",
    "memit_text.txt": "papers/text/mend.txt",
    "dyprag_blog/paper_text.txt": "papers/text/dyprag.txt",
    "genadapter_blog/paper_text.txt": "papers/text/genadapter.txt",
    "rpg_blog/paper_text.txt": "papers/text/rpg.txt",
    "shine_blog/paper_text.txt": "papers/text/shine.txt",
    "text2lora_blog/paper_text.txt": "papers/text/text2lora.txt",
    "unimem_blog/paper_text.txt": "papers/text/unimem.txt",
}

LOG_MOVES = {
    "one-step-output/MASTER_LOG.md": "logs/MASTER_LOG.md",
    "project_memory.md": "logs/project_memory.md",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def move(src, dst):
    if not os.path.exists(src):
        print("  SKIP (missing):", src)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print("  MOVE:", src, "->", dst)


def main():
    # 1. remove byte-identical duplicate PDFs (verify hash against root copy first)
    print("[1] dedupe blog-local PDF copies")
    canon = {v: sha256(k) for k, v in PDF_MOVES.items() if os.path.exists(k)}
    for dup in DUP_PDFS:
        if not os.path.exists(dup):
            print("  SKIP (missing):", dup)
            continue
        h = sha256(dup)
        if h in canon.values():
            os.remove(dup)
            print("  REMOVED duplicate:", dup)
        else:
            print("  KEEP (not a duplicate!):", dup)

    # 2. blogs
    print("[2] blogs/")
    for src, dst in BLOG_MOVES.items():
        move(src, dst)

    # 3. papers
    print("[3] papers/pdf + papers/text")
    for src, dst in PDF_MOVES.items():
        move(src, dst)
    for src, dst in TXT_MOVES.items():
        move(src, dst)

    # 4. logs
    print("[4] logs/")
    for src, dst in LOG_MOVES.items():
        move(src, dst)
    # drop now-empty one-step-output dir if empty
    if os.path.isdir("one-step-output") and not os.listdir("one-step-output"):
        os.rmdir("one-step-output")
        print("  RMDIR empty: one-step-output/")

    print("[done]")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
