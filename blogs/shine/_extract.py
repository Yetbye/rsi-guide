import fitz
doc = fitz.open(r'D:\success\RSI\shine_blog\shine.pdf')
print(f'pages: {len(doc)}')
out = []
for i, p in enumerate(doc):
    out.append(f'\n========== PAGE {i} ==========\n')
    out.append(p.get_text())
text = ''.join(out)
open(r'D:\success\RSI\shine_blog\paper_text.txt', 'w', encoding='utf-8').write(text)
print('chars:', len(text))
print(text[:4000])
doc.close()
