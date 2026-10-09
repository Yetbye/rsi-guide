import os
s = open(r'D:\success\RSI\dyprag_blog\index.html', encoding='utf-8').read()
print('size KB:', round(len(s.encode('utf-8'))/1024,1))
print('ends with </html>:', s.rstrip().endswith('</html>'))
print('footer:', '<footer class="footer">' in s)
print('content div:', s.count('<div class="content">'), s.count('</div><!-- /content -->'))
print('section:', s.count('<section class="chapter"'), s.count('</section>'))
print('svg:', s.count('<svg'), s.count('</svg>'))
print('formula:', s.count('class="formula"'))
print('tables:', s.count('<table>'), 'rows:', s.count('<tr>'))
print('rq:', s.count('class="rq"'), 'critique:', s.count('class="critique"'), 'insight:', s.count('class="insight"'))
print('code:', s.count('class="code-block"'))
base = r'D:\success\RSI\dyprag_blog'
for f in ['assets/hero_cover.jpg','figures/fig1_paradigms.png','figures/fig2_three_stage.png','figures/fig3_ragtruth.png']:
    p = os.path.join(base, f)
    print(f, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else 0)
