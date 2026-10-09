import fitz
doc = fitz.open(r'D:\success\RSI\dyprag_blog\dyprag.pdf')
page = doc[8]
print(f'idx 8 size: {page.rect.width:.0f}x{page.rect.height:.0f}')
for i, b in enumerate(page.get_text('dict')['blocks']):
    if b['type'] == 1:
        print(f'  IMG {i}: {[round(x,1) for x in b["bbox"]]}')
    else:
        t = ' '.join(s['text'] for l in b['lines'] for s in l['spans'])
        if any(k in t for k in ['RAGTruth','Win','Tie','Loss','Number of','Qwen-1.5B','LLaMA-1B','LLaMA-8B','Knowledge Internalization']):
            print(f'  TXT {i}: {[round(x,1) for x in b["bbox"]]} "{t[:60]}"')
doc.close()
