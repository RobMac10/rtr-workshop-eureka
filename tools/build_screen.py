"""Big-screen (projector) view: /screen/. Built only from content already on the participant page."""
import os, sys
from html import escape as e
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, '/workspace/story')
import build as B
import nells_diary as D
from make_qr import make, INK, WHITE
from PIL import Image, ImageDraw

V = B.V; c = B.EUP
A = '../assets/'

def book(S):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((S*.14, S*.16, S*.86, S*.84), radius=S*.05, fill=INK)
    d.rectangle((S*.22, S*.22, S*.80, S*.78), fill=WHITE)
    d.rectangle((S*.22, S*.22, S*.30, S*.78), fill=INK)
    for k in range(5): d.rectangle((S*.38, S*(.32+k*.09), S*.72, S*(.35+k*.09)), fill=INK)
    return im

QR_NELL = 'qr/nells-diary-qr.png'
if not os.path.exists(os.path.join(ROOT, 'assets', QR_NELL)):
    make('https://robmac10.github.io/nells-diary/', 'Nell’s Diary', book).save(os.path.join(ROOT, 'assets', QR_NELL), optimize=True)

def img(src, alt, cap=None, cls=''):
    f = '<figure class="s-fig %s"><img src="%s%s" alt="%s">' % (cls, A, src, e(alt))
    if cap: f += '<figcaption>%s</figcaption>' % e(cap)
    return f + '</figure>'

def qr(src, alt, url):
    return '<figure class="s-qr"><img src="%s%s" alt="%s"><figcaption>%s</figcaption></figure>' % (A, src, e(alt), e(url))

S = []
def slide(body, cls='', label=''):
    S.append((body, cls, label))

# 1 title + content note
slide(f'''<p class="eyebrow">Reopen the Record · Today’s case</p>
<h1 class="s-title">{e(c['title'])}</h1>
<p class="s-q">{e(c['question'])}</p>
<p class="s-sub">Ballarat, {e(c['dates'])}</p>
<span class="stamp s-stamp" aria-hidden="true">Case reopened</span>
<p class="s-note">{e(c['country'])}</p>''', 's-cover', 'Eureka')

# 2 briefing
slide('''<p class="eyebrow">Briefing</p>
<p class="s-big">In this guided investigation, you step into the role of investigator and reopen one Australian history case file together: <strong>Eureka</strong>, Ballarat, 1854.</p>
<p>Using primary sources, evidence cards, three witnesses and the Bias Button, you will reopen the record in a culturally appropriate and apolitical way, through questions about the people, documents, silences, and questions the official story never fully settled.</p>
<p>You will leave with your Eureka case file, the Bias Button, and links to all six case files: Deep Time, Batavia, Eureka, Federation, Freedom Ride and Frontier.</p>''', 's-memo', 'Briefing')

# 3 investigate
app_t, app_u, app_qr = c['app']
slide(f'''<p class="eyebrow">Decision point</p>
<h2>Investigate Eureka</h2>
<p class="s-lead">Two ways in. Choose one: the full case app, or the case file on this page.</p>
<div class="s-choices">
 <div class="s-card s-app"><span class="dp-tab">Choice A</span><h3>Open the App</h3><p>Who Fired First? The whole case on your phone or tablet.</p>{qr(app_qr, 'QR code for the Who Fired First? app', 'robmac10.github.io/who-fired-first/')}</div>
 <div class="s-card s-env"><span class="dp-tab">Choice B</span><h3>Open the Envelope</h3><p>Work through the case file here: evidence cards, three witnesses, the Bias Button and your finding.</p></div>
</div>''', '', 'Investigate')

# 4 Nell's Diary
slide(f'''<div class="s-split">
<div>
<p class="eyebrow">Envelope contents · 1</p>
<h2>{e(D.TITLE)}</h2>
<p class="s-q">{e(D.SUB)}</p>
<p>{e(D.EXHIBIT)}</p>
<p class="s-imag"><span class="imag">Imagined</span> Written for this case, based on real events, not a real document.</p>
{qr(QR_NELL, 'QR code for Nell’s Diary', 'robmac10.github.io/nells-diary/')}
</div>
{img('img/chapel.jpg', D.CHAPEL_CAPTION, 'Eugene von Guérard, Catholic Chapel on the Gravel Pit Line, Ballarat, January 1854. State Library of Victoria, H12532. Out of copyright.')}
</div>''', '', 'Nell’s Diary')

# 5 opener
slide('<p class="eyebrow">Open the envelope</p>' + ''.join('<p class="s-line">%s</p>' % e(x) for x in c['opener']), 's-opener', 'Opener')

# 6 established
slide('<p class="eyebrow">Envelope contents · 3</p><h2>What reliable sources have established</h2><ul class="s-list">' +
      ''.join('<li>%s</li>' % e(x) for x in c['agreed']) + '</ul><p class="s-small">Full sources: see the bibliography on the participant page.</p>', '', 'Established')

# 7-11 evidence
port = {0: ('img/thomas.jpg', 1), 1: ('img/lalor.jpg', 0), 2: ('img/carboni.jpg', 2)}
for i, ev in enumerate(c['evidence']):
    L = 'ABCDE'[i]
    body = ('<p class="ev-tag-s">Evidence %s</p><p class="eyebrow">%s</p><h2>%s</h2>' % (L, e(ev['kind']), e(ev['title'])))
    if ev.get('quote'): body += '<blockquote class="s-quote">“%s”</blockquote>' % e(ev['quote'])
    else: body += '<p class="s-big">%s</p>' % e(ev['summary'])
    body += '<p class="s-look"><strong>Look closer.</strong> %s</p><p class="s-small">%s</p>' % (e(ev['look']), e(ev['cite']))
    if i in port:
        w = c['witnesses'][port[i][1]]
        body = '<div class="s-split s-split-r"><div>%s</div>%s</div>' % (body, img(w['img'], w['name'], w['cap'], 'portrait'))
    slide(body, 's-ev', 'Evidence ' + L)

# 12 three witnesses, three questions
Q3 = ['What did they say they saw?', 'Could they really have seen it?', 'Why might they say it?']
slide('<p class="eyebrow">Three witnesses, three questions</p><h2>Ask every witness the same three questions.</h2><div class="s-wits">' +
      ''.join('<div>%s<p class="s-wname">%s</p></div>' % (img(w['img'], w['name'], None, 'portrait'), e(w['name'])) for w in c['witnesses']) +
      '</div><ol class="s-q3">' + ''.join('<li>%s</li>' % q for q in Q3) + '</ol>', '', 'Witnesses')

# 13-15 each witness
for k, w in enumerate(c['witnesses']):
    slide('<div class="s-split s-split-r"><div><p class="eyebrow">Witness %d</p><h2>%s</h2><p class="s-role">%s</p><p class="s-said">%s</p><p class="s-small"><strong>Source.</strong> %s</p></div>%s</div>'
          % (k + 1, e(w['name']), e(w['role']), e(w['said']), e(w['src']), img(w['img'], w['name'], w['cap'], 'portrait')), '', 'Witness %d' % (k + 1))

# 16 Bias Button
BQ = ['Who made it, and why?', 'Who is missing?', 'What are the loaded words doing?', 'What does it want you to think or do?']
slide('<div class="s-bb"><div class="bb-btn" aria-hidden="true">Bias<br>Button</div><div><p class="eyebrow">Bias Button</p><h2>The same four questions for every source.</h2><ol class="s-q4">' +
      ''.join('<li>%s</li>' % q for q in BQ) + '</ol><p class="s-lead">The button does not give the answer.</p></div></div>', '', 'Bias Button')

# 17 decide
slide('<p class="eyebrow">Decide: my finding</p><h2>Who fired first?</h2><div class="s-opts">' +
      ''.join('<div class="s-opt%s">%s</div>' % (' s-opt-k' if 'know' in o else '', e(o)) for o in c['decide']) +
      '</div><p class="s-lead">There is no answer at the back. Write only what these records can support. “We can’t know” is an honest finding.</p>', '', 'Decide')

# 18 explore
KITS = [('Deep Time', 'deep-time-qr.png', 'robmac10.github.io/65000-years/'), ('Batavia', 'batavia-qr.png', 'robmac10.github.io/batavia-case/'),
        ('Eureka', 'eureka-qr.png', 'robmac10.github.io/who-fired-first/'), ('Federation', 'federation-qr.png', 'robmac10.github.io/federation-case/'),
        ('Frontier', 'myall-creek-qr.png', 'robmac10.github.io/myall-creek-case/'), ('Freedom Ride', 'freedom-ride-qr.png', 'robmac10.github.io/freedom-ride-case/')]
slide('<div class="s-explore">' + img('img/cover-australian-histories.jpg?v=' + V, 'Reopen the Record: Australian Histories cover', None, 'cover') +
      '<div><p class="eyebrow">Explore more</p><h2>Explore all six cases</h2><div class="s-kits">' +
      ''.join('<figure class="s-kit"><img src="%sqr/%s" alt="QR code for %s"><figcaption><strong>%s</strong><br>%s</figcaption></figure>' % (A, f, e(n), e(n), e(u)) for n, f, u in KITS) +
      '</div></div></div>', '', 'Explore')

# 19 closing
slide('<p class="s-close">Real people. Real records. Real questions the record never settled.</p><p class="s-close s-close-2">What a terrible thing to lose.</p>', 's-closing', 'Close')

N = len(S)
secs = ''.join('<section class="slide %s" id="s%d" aria-label="%s, slide %d of %d"%s><div class="s-in">%s</div></section>\n'
               % (cls, i + 1, e(lab), i + 1, N, '' if i == 0 else ' hidden', body) for i, (body, cls, lab) in enumerate(S))
page = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Eureka · big screen · Reopen the Record</title>
<link rel="stylesheet" href="{A}screen.css?v={V}">
</head>
<body>
<main class="deck" id="deck">
{secs}</main>
<nav class="s-ctl" aria-label="Slide controls">
 <button type="button" id="prev" aria-label="Previous slide">←</button>
 <span id="count" aria-live="polite">1 / {N}</span>
 <button type="button" id="next" aria-label="Next slide">→</button>
 <button type="button" id="fs" aria-label="Full screen (F)">⛶ Full screen</button>
</nav>
<script src="{A}screen.js?v={V}"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'screen', 'index.html'), 'w').write(page)
print('wrote screen/index.html', N, 'slides:', ', '.join(l for _, _, l in S))
