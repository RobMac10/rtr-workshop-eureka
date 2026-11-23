"""Print-friendly PDF of Nell's Diary (the imagined case-opening story), text verbatim from the canonical source
/workspace/story/nells_diary.py (the same source as https://robmac10.github.io/nells-diary/). Teacher notes are left out."""
import os, sys, asyncio
from html import escape as e
sys.path.insert(0, '/workspace/story')
import nells_diary as D
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = 'file://' + os.path.join(ROOT, 'assets')
BADGE = 'Written for this case, based on real events, not a real document.'
CREDIT = 'Cover: Eugene von Guérard, Catholic Chapel on the Gravel Pit Line, Ballarat, January 1854. State Library of Victoria, H12532. Out of copyright.'

def runs(p):
    out = []
    for r in p:
        if isinstance(r, str): out.append(e(r))
        else: out.append('<span class="sp"><s>%s</s><span class="fix">%s</span></span>' % (e(r[1]), e(r[2])))
    return ''.join(out)

def entry(en):
    notes = dict(en.get('notes') or [])
    paras = ''.join('<div class="para"><p>%s</p>%s</div>' % (runs(p), '<p class="note">%s</p>' % e(notes[j]) if j in notes else '') for j, p in enumerate(en['paras']))
    lab = '<p class="label">%s</p>' % e(en['class_label']) if en['class_label'] else ''
    return '<section class="entry"><p class="place">%s</p><h2>%s</h2>%s%s</section>' % (e(en['place']), e(en['date']), lab, paras)

badge = '<div class="badge"><b>Imagined</b> <span>%s</span></div>' % BADGE
html = f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>{e(D.TITLE)}</title>
<style>
@font-face{{font-family:EBG;src:url("{A}/fonts/EBGaramond-Regular.ttf")}}
@font-face{{font-family:EBG;font-style:italic;src:url("{A}/fonts/EBGaramond-Italic.ttf")}}
@font-face{{font-family:Hand;src:url("{A}/fonts/Kalam-Regular.ttf")}}
@page{{size:A4;margin:16mm 16mm 18mm}}
body{{font:12pt/1.55 EBG,serif;color:#2b2420;margin:0}}
.cover{{text-align:center;page-break-after:always;padding-top:8mm}}
.cover h1{{font-size:38pt;margin:4mm 0 0;color:#4a2e1b}}
.cover .sub{{font-style:italic;font-size:18pt;color:#8b3a1e;margin:1mm 0}}
.cover .strap{{font-size:13pt;margin:1mm 0 6mm}}
.cover img{{width:120mm;border:1px solid #c9a96a;padding:3mm;background:#fffdf7}}
.cover .cap{{font-size:9.5pt;color:#5c5148;margin:1mm 0 6mm}}
.cover .ex{{font-size:11pt;letter-spacing:.06em;text-transform:uppercase;color:#6b4a22}}
.badge{{display:inline-block;border:1.5px dashed #6b5a4a;border-radius:8px;padding:2.5mm 4mm;margin:5mm auto;font:10.5pt EBG,serif;background:#faf3e3}}
.badge b{{letter-spacing:.12em;text-transform:uppercase;margin-right:2mm}}
.entry{{break-inside:auto;margin:0 0 8mm;padding:4mm 0 0;border-top:1px solid #d9c39a;background:repeating-linear-gradient(transparent 0 8.3mm,#dfe7f0 8.3mm calc(8.3mm + 1px))}}
.place{{margin:0;font-size:10pt;letter-spacing:.08em;text-transform:uppercase;color:#6b4a22}}
h2{{margin:0 0 1mm;font-size:16pt;color:#4a2e1b;break-after:avoid}}
.label{{margin:0 0 2mm;font-style:italic;color:#5c5148}}
.para p{{font:13pt/8.3mm Hand,cursive;margin:0 0 1mm;color:#1f3a6b}}
.para{{break-inside:avoid}}
.note{{font:italic 11pt/1.35 EBG,serif!important;color:#a3281f!important;margin:0 0 2mm 18mm!important;border-left:2px solid #a3281f;padding-left:3mm}}
.sp s{{color:#555}} .sp .fix{{color:#a3281f;font-style:italic;margin-left:1mm}}
.end{{text-align:center;margin-top:8mm;font-size:13pt;break-inside:avoid}}
.end a{{color:#7c2938}}
.foot{{position:fixed;bottom:-12mm;left:0;right:0;text-align:center;font-size:8.5pt;color:#6b5a4a}}
</style></head><body>
<section class="cover">
 <p class="ex">{e(D.EXHIBIT)}</p>
 <h1>{e(D.TITLE)}</h1><p class="sub">{e(D.SUB)}</p><p class="strap">{e(D.STRAP)}</p>
 {badge}
 <div><img src="{A}/img/chapel.jpg" alt=""><p class="cap">{e(D.CHAPEL_CAPTION)}</p></div>
 <p>{e(D.SCHOOL)}</p>
 <p class="cap">{e(CREDIT)}</p>
</section>
{''.join(entry(x) for x in D.ENTRIES)}
<div class="end"><p>{e(D.END)}</p><p>Who fired first? Open the case: <a href="https://robmac10.github.io/who-fired-first/">robmac10.github.io/who-fired-first</a></p>
<p>Read the diary online: <a href="https://robmac10.github.io/nells-diary/">robmac10.github.io/nells-diary</a></p>{badge}</div>
</body></html>'''

async def main():
    from playwright.async_api import async_playwright
    tmp = '/tmp/nells-diary-print.html'; open(tmp, 'w').write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(); await pg.goto('file://' + tmp); await pg.wait_for_timeout(500)
        await pg.pdf(path=os.path.join(ROOT, 'assets/pdf/nells-diary.pdf'), format='A4', print_background=True, prefer_css_page_size=True, display_header_footer=True, header_template='<span></span>', footer_template='<div style="width:100%;text-align:center;font-size:7.5pt;color:#6b5a4a;font-family:serif">Nell’s Diary · Imagined: ' + BADGE + ' · <span class="pageNumber"></span>/<span class="totalPages"></span></div>')
        await b.close()
    print('wrote assets/pdf/nells-diary.pdf')
asyncio.run(main())
