import fitz
doc = fitz.open(r'D:\success\RSI\shine_blog\shine.pdf')
base = r'D:\success\RSI\shine_blog\figures'
# Fig 2 overall architecture idx3
doc[3].get_pixmap(matrix=fitz.Matrix(2.5,2.5), clip=fitz.Rect(50,130,560,520)).save(base+r'\fig2_architecture.png')
# Fig 3 M2P transformer idx4
doc[4].get_pixmap(matrix=fitz.Matrix(2.5,2.5), clip=fitz.Rect(50,130,560,520)).save(base+r'\fig3_m2p.png')
# Fig 6 multi-turn conversation idx6 (right side)
doc[6].get_pixmap(matrix=fitz.Matrix(3,3), clip=fitz.Rect(300,300,560,500)).save(base+r'\fig6_multiturn.png')
doc.close()
print('done')
