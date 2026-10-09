import fitz
doc = fitz.open(r'D:\success\RSI\dyprag_blog\dyprag.pdf')
out = r'D:\success\RSI\dyprag_blog\figures'
crops = [
    (1, (300, 145, 508, 235), 'fig1_paradigms.png', 'Fig1 three paradigms'),
    (3, (108, 68, 508, 292), 'fig2_three_stage.png', 'Fig2 three-stage framework'),
    (8, (100, 155, 300, 250), 'fig3_ragtruth.png', 'Fig3 RAGTruth win/tie/loss'),
]
for idx, rect, fn, _ in crops:
    page = doc[idx]
    r = fitz.Rect(*rect)
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=r)
    p = out + '\\' + fn
    pix.save(p)
    print(fn, pix.width, 'x', pix.height)
doc.close()
