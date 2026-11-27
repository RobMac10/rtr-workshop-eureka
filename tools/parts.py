# -*- coding: utf-8 -*-
"""Build index.html for the Reopen the Record workshop page. Run: python3 tools/build.py"""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import CASES
V = '20261123b'
e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAINLAND = [[113.7,-26.6],[113.6,-24.9],[114.0,-22.0],[114.1,-21.8],[116.8,-20.6],[121.6,-18.8],[122.2,-18.2],[123.8,-16.4],[126.0,-14.3],[126.8,-13.8],[129.0,-14.9],[129.9,-14.4],[130.4,-13.3],[130.8,-12.4],[132.0,-12.2],[133.4,-12.1],[135.0,-12.2],[136.8,-13.8],[137.8,-15.6],[139.5,-17.0],[140.9,-17.5],[141.8,-15.0],[141.7,-12.8],[142.1,-11.0],[142.5,-10.7],[143.0,-11.7],[143.6,-14.3],[145.3,-15.0],[145.8,-16.9],[146.3,-19.0],[148.7,-20.3],[149.2,-21.2],[150.8,-23.5],[151.9,-24.2],[153.1,-25.3],[153.5,-27.0],[153.5,-28.2],[153.2,-30.0],[153.1,-31.5],[151.3,-33.8],[151.2,-34.0],[150.9,-34.6],[150.5,-35.3],[150.2,-36.2],[149.9,-37.3],[147.0,-38.3],[145.5,-38.4],[144.9,-38.5],[143.5,-38.9],[141.0,-38.3],[140.0,-38.0],[138.8,-35.6],[138.5,-35.0],[137.6,-35.0],[136.8,-35.3],[135.9,-34.8],[135.2,-34.6],[134.2,-32.8],[131.5,-31.6],[129.0,-31.7],[125.0,-32.8],[122.3,-34.0],[119.6,-34.4],[116.7,-35.0],[115.14,-34.37],[115.0,-33.6],[115.7,-32.0],[115.3,-30.5],[114.9,-29.2],[114.1,-28.0],[113.8,-26.8]]
TAS = [[144.7,-40.7],[146.3,-41.0],[148.3,-40.9],[148.3,-42.2],[148.0,-43.2],[147.0,-43.6],[145.9,-43.5],[144.7,-42.8],[144.6,-41.7]]
def xy(lon, lat):
    return round((lon-112)/(155-112)*400, 1), round(((-10)-lat)/35*340+12, 1)
def poly(pts): return ' '.join('%s,%s' % xy(*p) for p in pts)
PINS = {  # case id: [(lon, lat, label)]
 'deep-time': [(132.6,-12.5,'Madjedbebe'),(143.1,-33.7,'Lake Mungo'),(141.9,-38.1,'Budj Bim')],
 'batavia': [(113.8,-28.5,'Houtman Abrolhos')],
 'eureka': [(143.85,-37.56,'Ballarat')],
 'federation': [(152.0,-29.05,'Tenterfield'),(151.23,-33.9,'Sydney')],
 'freedom-ride': [(149.85,-29.47,'Moree'),(148.12,-30.02,'Walgett')],
 'frontier': [(149.58,-33.42,'Bathurst'),(150.65,-29.78,'Myall Creek')],
}
def map_svg():
    out = ['<svg class="ausmap" viewBox="-10 0 480 360" role="img" aria-labelledby="mapt"><title id="mapt">Map of Australia showing where each case file is set. Outline simplified.</title>',
           '<defs><pattern id="paper" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="#c9a96a55"/></pattern></defs>',
           '<rect width="470" height="360" fill="url(#paper)"/>',
           '<polygon points="%s" class="land"/><polygon points="%s" class="land"/>' % (poly(MAINLAND), poly(TAS))]
    for c in CASES:
        pins = PINS[c['id']]
        out.append('<a href="#case-%s" class="pin-group" data-case="%s" aria-label="Open the %s case file">' % (c['id'], c['id'], e(c['title'])))
        for i,(lon,lat,lab) in enumerate(pins):
            x,y = xy(lon,lat)
            out.append('<circle cx="%s" cy="%s" r="6.5" fill="%s" class="pin"/><circle cx="%s" cy="%s" r="2.2" fill="#fbf3e6"/>' % (x,y,c['colour'],x,y))
        x,y = xy(*pins[0][:2])
        dx = {'batavia':10,'eureka':-12,'federation':12,'freedom-ride':-14,'frontier':-12,'deep-time':10}[c['id']]
        dy = {'batavia':4,'eureka':18,'federation':-10,'freedom-ride':-10,'frontier':26,'deep-time':4}[c['id']]
        anchor = 'end' if dx < 0 else 'start'
        out.append('<text x="%s" y="%s" text-anchor="%s" class="pinlab" fill="%s">%s</text></a>' % (x+dx, y+dy, anchor, c['colour'], e(c['title'])))
    out.append('</svg>')
    return ''.join(out)

def pic(src, cap, cls='zoom', alt=None):
    alt = alt or cap
    return ('<figure class="%s"><button type="button" class="zoom-btn" aria-label="Enlarge picture"><img src="assets/%s" alt="%s" loading="lazy"></button>'
            '<figcaption>%s</figcaption></figure>') % (cls, src, e(alt), e(cap))

def ta(key, label, rows=3):
    return ('<label class="field"><span>%s</span><textarea data-key="%s" rows="%d"></textarea><span class="print-lines" aria-hidden="true"></span></label>') % (e(label), key, rows)

def bias_panel(key):
    qs = ['Who made it, and why?','Who is missing?','What are the loaded words doing?','What does it want you to think or do?']
    inner = ''.join(ta('%s-b%d' % (key,i), q, 2) for i,q in enumerate(qs))
    return ('<details class="bias"><summary><span class="bb-dot" aria-hidden="true"></span> Bias Button</summary>'
            '<div class="bias-body"><p class="note">Four questions. The button does not give the answer. “We can’t know” is a fair finding.</p>%s</div></details>') % inner

def evidence_card(c, i, ev):
    key = '%s-e%d' % (c['id'], i)
    q = '<blockquote>“%s”</blockquote>' % e(ev['quote']) if ev.get('quote') else '<p class="ev-sum">%s</p>' % e(ev['summary'])
    warn = '<p class="cw">Content note: this source uses the racial language of its time. It is quoted only as a short, attributed extract.</p>' if ev.get('warn') else ''
    links = ' '.join('<a class="src-link" href="%s" target="_blank" rel="noopener">%s ↗</a>' % (e(u), e(t)) for t,u in ev['links'])
    return ('<article class="ev-card"><div class="ev-tag">Evidence %s</div><p class="ev-kind">%s</p><h4>%s</h4>%s%s'
            '<p class="ev-cite"><strong>Source.</strong> %s</p><p class="ev-look"><strong>Look for.</strong> %s</p><p class="ev-links">%s</p>%s</article>') % (
            'ABCDEFG'[i], e(ev['kind']), e(ev['title']), warn, q, e(ev['cite']), e(ev['look']), links, bias_panel(key))

def witness_card(c, i, w):
    key = '%s-w%d' % (c['id'], i)
    qs = ['What did they say they saw?','Could they really have seen it?','Why might they say it?']
    return ('<article class="witness"><div class="w-pic">%s</div><div class="w-body"><p class="w-num">Witness %d</p><h4>%s</h4><p class="w-role">%s</p>'
            '<p class="w-said">%s</p><p class="w-src"><strong>Source.</strong> %s</p><div class="w-qs">%s</div></div></article>') % (
            pic(w['img'], w['cap'], 'zoom portrait'), i+1, e(w['name']), e(w['role']), e(w['said']), e(w['src']),
            ''.join(ta('%s-q%d' % (key,j), q, 2) for j,q in enumerate(qs)))

def case_section(c):
    cid = c['id']
    inq = c['inquiry']
    cols = [('People','people','Who was there? Who speaks, and who is spoken for?'),('Documents','documents','Who made each record, when, and for whom?'),
            ('Silences','silences','What is missing, lost, or never asked?'),('Still unsettled','unsettled','What can the record not settle?')]
    inq_html = ''.join('<div class="inq inq-%s"><h4>%s</h4><p class="note">%s</p><ul>%s</ul></div>' % (k, t, e(sub), ''.join('<li>%s</li>' % e(x) for x in inq[k])) for t,k,sub in cols)
    decide = ''.join('<label class="choice"><input type="radio" name="%s-find" value="%d" data-key="%s-find"> <span>%s</span></label>' % (cid, i, cid, e(o)) for i,o in enumerate(c['decide']))
    decide += '<label class="choice"><input type="radio" name="%s-find" value="own" data-key="%s-find"> <span>My own finding, written below.</span></label>' % (cid, cid)
    app_t, app_u, app_qr = c['app']
    extra = pic(c['extra_img'][0], c['extra_img'][1]) if c.get('extra_img') else ''
    return f'''
<section class="case" id="case-{cid}" data-case="{cid}" style="--case:{c['colour']}" aria-labelledby="h-{cid}">
 <div class="case-head">
  <div class="folder">
   <span class="folder-tab">Case file</span><span class="string" aria-hidden="true"></span>
   <div class="folder-grid">
    <div>
     <p class="env-eyebrow">Reopen the Record · {e(c['dates'])}</p>
     <h2 id="h-{cid}">{e(c['title'])}</h2>
     <p class="key-q">{e(c['question'])}</p>
     <div class="case-actions">
      <button type="button" class="btn btn-primary print-case" data-case="{cid}">Download / print my case file</button>
      <a class="btn" href="{e(app_u)}" target="_blank" rel="noopener">Open the full app ↗</a>
      <a class="btn btn-quiet back" href="#cases">← All cases</a>
     </div>
    </div>
    <div class="folder-pic">{pic(c['tile_img'][0], c['tile_img'][1])}</div>
   </div>
   <span class="stamp" aria-hidden="true">Case reopened</span>
  </div>
  <p class="country">{e(c['country'])}</p>
 </div>

 <div class="step"><span class="step-n">1</span><h3>Open the envelope</h3></div>
 <div class="opener">{''.join('<p>%s</p>' % e(p) for p in c['opener'])}<p class="opener-src">Every date, place and quotation here is from the records cited below.</p></div>

 <div class="step"><span class="step-n">2</span><h3>Read: what the record agrees on</h3></div>
 <ul class="agreed">{''.join('<li>%s</li>' % e(a) for a in c['agreed'])}</ul>
 {extra}

 <div class="step"><span class="step-n">3</span><h3>Evidence cards</h3></div>
 <p class="lead-in">Real documents, each with its citation and a link to the archive. Press the <strong>Bias Button</strong> on any card to open the four questions.</p>
 <div class="ev-grid">{''.join(evidence_card(c,i,ev) for i,ev in enumerate(c['evidence']))}</div>

 <div class="step"><span class="step-n">4</span><h3>Ask: three witnesses, three questions</h3></div>
 <p class="lead-in">Ask every witness the same three questions. Tap a picture to enlarge it.</p>
 <div class="witnesses">{''.join(witness_card(c,i,w) for i,w in enumerate(c['witnesses']))}</div>

 <div class="step"><span class="step-n">5</span><h3>Inquiry questions</h3></div>
 <div class="inq-grid">{inq_html}</div>

 <div class="step"><span class="step-n">6</span><h3>Decide: my finding</h3></div>
 <div class="decide">
  <p class="decide-q">{e(c['question'])}</p>
  <p class="note">There is no answer at the back. Write only what these records can support. “We can’t know” is an honest finding.</p>
  <div class="choices">{decide}</div>
  {ta(cid+'-why','My finding, and the one piece of evidence that most changed my mind',4)}
  {ta(cid+'-cant','What I still can’t know',2)}
  <div class="sure" role="group" aria-label="How sure am I?"><span>How sure am I?</span>
   <label><input type="radio" name="{cid}-sure" value="sure" data-key="{cid}-sure"> Sure</label>
   <label><input type="radio" name="{cid}-sure" value="maybe" data-key="{cid}-sure"> Maybe</label>
   <label><input type="radio" name="{cid}-sure" value="guess" data-key="{cid}-sure"> Guess</label></div>
 </div>

 <div class="step"><span class="step-n">7</span><h3>Super Sleuths <small>optional</small></h3></div>
 <ul class="sleuths">{''.join('<li>%s</li>' % e(s) for s in c['sleuths'])}</ul>

 <div class="app-card">
  <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/{app_qr}" alt="QR code that opens {e(app_t)}"></button></figure>
  <div><p class="env-eyebrow">The full case app</p><h4>{e(app_t)}</h4>
  <p>The app has the whole case: the opening page, the witnesses, My finding, Super Sleuths and a Teacher Note. Scan the code or use the link.</p>
  <p><a class="btn btn-primary" href="{e(app_u)}" target="_blank" rel="noopener">Open the app ↗</a> <span class="url">{e(app_u.replace('https://',''))}</span></p></div>
 </div>
 <p class="credits"><strong>Pictures.</strong> {e(c['credits'])}</p>
 <p class="case-nav"><a class="btn btn-quiet" href="#cases">← Choose another case</a> <a class="btn btn-quiet" href="#bias">Next: the Bias Button →</a></p>
</section>'''

def tile(c):
    src, cap = c['tile_img']
    return f'''<a class="tile" href="#case-{c['id']}" data-case="{c['id']}" style="--case:{c['colour']}">
 <span class="tile-pic"><img src="assets/{src}" alt="" loading="lazy"></span>
 <span class="tile-body"><span class="tile-dates">{e(c['dates'])}</span><span class="tile-title">{e(c['title'])}</span>
 <span class="tile-q">{e(c['question'])}</span><span class="tile-go">Open the case file →</span></span></a>'''

BIAS_INV = [
 ('1. Hidden words','Some official and newspaper words sound milder than the act they describe.','The Moreton Bay Courier, 1858; The Sydney Morning Herald, 1912.','https://trove.nla.gov.au/newspaper/article/15303445','Trove'),
 ('2. Who is allowed in?','A law can draw a line without naming a race. A masthead can say the line out loud.','Federal Hansard extract, 1901; Immigration Restriction Act 1901.','https://www.legislation.gov.au/C1901A00017/asmade/text','Federal Register of Legislation'),
 ('3. Send a man','Wartime posters and later articles can tell women what they are for.','Australian War Memorial poster, 1915; The Daily Telegraph, 1938.','https://www.awm.gov.au/collection/C98067','Australian War Memorial'),
 ('4. Who gets the label?','Class bias often arrives as a short, sticky word.','The Murrumbidgee Irrigator, 1931; The Canberra Times, 1976.','https://trove.nla.gov.au/newspaper/article/110798231','Trove'),
]

def page():
    tiles = ''.join(tile(c) for c in CASES)
    cases = ''.join(case_section(c) for c in CASES)
    bias_cards = ''.join(f'<article class="inv"><h4>{e(t)}</h4><p>{e(d)}</p><p class="note">Sources include {e(s)} <a href="{u}" target="_blank" rel="noopener">{e(lt)} ↗</a></p></article>' for t,d,s,u,lt in BIAS_INV)
    case_opts = ''.join(f'<li><a href="#case-{c["id"]}" style="--case:{c["colour"]}">{e(c["title"])}</a></li>' for c in CASES)
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
<title>Reopen the Record · Workshop case files</title>
<meta name="description" content="A guided investigation: choose an Australian history case file, read real records, ask three witnesses, press the Bias Button, and decide.">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/image-fit.css?v={V}">
<link rel="stylesheet" href="assets/style.css?v={V}">
</head>
<body>
<div class="print-cover" aria-hidden="true">
 <img class="pc-hero" src="assets/img/hero.jpg" alt="">
 <p class="pc-eyebrow">Reopen the Record · Workshop case file</p>
 <h1 class="pc-title">Case file</h1>
 <p class="pc-q"></p>
 <p class="pc-tag">Real people. Real records. Real questions the record never settled.</p>
 <div class="pc-qrs"><figure><img class="pc-qr-case" src="" alt=""><figcaption>The full case app</figcaption></figure><figure><img src="assets/qr/bias-button-qr.png" alt=""><figcaption>The Bias Button</figcaption></figure><figure><img src="assets/qr/workshop-qr.png" alt=""><figcaption>This workshop page</figcaption></figure></div>
 <p class="pc-note">Investigator: ______________________________ &nbsp; Date: ______________</p>
 <p class="pc-small">This file includes histories of First Nations peoples. Aboriginal and Torres Strait Islander readers are advised that it names people who have died. No photographs of them are used. Sources are cited with their links. Your answers stay on your device unless you print them.</p>
</div>
<a class="skip" href="#main">Skip to the workshop</a>
<header class="topbar">
 <div class="topbar-in">
  <a class="brand" href="#top">Reopen the Record<small>Workshop case files</small></a>
  <nav aria-label="Workshop sections"><a href="#how">How it works</a><a href="#cases">Cases</a><a href="#bias">Bias Button</a><a href="#classroom">Classroom</a></nav>
 </div>
</header>
<p class="banner">This workshop includes histories of First Nations peoples and of colonial violence. Aboriginal and Torres Strait Islander participants are advised that it names people who have died. It shows no photographs of them: silhouettes are used. It retells no cultural stories and shows no rock art. Some linked sources use the racist language of their time; they carry a content note. If something here should be corrected, please tell the workshop presenter, so the file can be updated.</p>

<main id="main">
<section class="hero" id="top" aria-labelledby="h-title">
 <div class="hero-art" role="img" aria-label="Illustration: case-file folders tied with red string, a brass scales of justice, a magnifying glass and old documents on an archive desk."></div>
 <div class="hero-in">
  <div class="envelope">
   <span class="folder-tab">History</span><span class="string" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span>
   <p class="env-eyebrow">A guided investigation · Australian Histories</p>
   <h1 id="h-title">Reopen the Record</h1>
   <p class="env-sub">Workshop case files</p>
   <p class="tagline">Real people. Real records. Real questions the record never settled.</p>
   <div class="hero-actions"><a class="btn btn-primary" href="#cases">Choose your case</a><a class="btn" href="#how">How it works</a></div>
   <span class="stamp" aria-hidden="true">Case reopened</span>
  </div>
  <figure class="hero-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-qr.png" alt="QR code that opens this workshop page"></button><figcaption>Scan to open this page on a phone.</figcaption></figure>
 </div>
</section>

<section class="brief wrap" aria-labelledby="h-brief">
 <div class="memo">
  <p class="memo-head" id="h-brief">Briefing</p>
  <p>In this guided investigation, you step into the role of investigator and work through one Australian history case file of your choice: <strong>Deep Time</strong>, <strong>Batavia</strong>, <strong>Eureka</strong>, <strong>Federation</strong>, <strong>Freedom Ride</strong>, or <strong>Frontier</strong> (the Bathurst War and Myall Creek).</p>
  <p>Using primary sources, evidence cards, structured inquiry and a Bias Button activity, you will reopen the record in a culturally appropriate and apolitical way. You will examine different perspectives and publicly available oral histories, through specific inquiry questions that explore the people, documents, silences, and questions the official story never fully settled.</p>
  <p>By the end of the session you will leave with the case file, the Bias Button activity, and a ready-to-use approach for immediate classroom use.</p>
  <p class="closing">Real people. Real records. Real questions the record never settled.</p>
  <p class="closing closing-2">What a terrible thing to lose.</p>
 </div>
</section>

<section class="how wrap" id="how" aria-labelledby="h-how">
 <p class="eyebrow">How the session works</p>
 <h2 id="h-how">Read. Ask. Decide.</h2>
 <div class="rad">
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="12" y="6" width="40" height="52" rx="3" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="3"/><path d="M20 18h24M20 26h24M20 34h24M20 42h14" stroke="#4a2e1b" stroke-width="3"/></svg>
   <h3>Read</h3><p>Open the envelope. Read what the record agrees on, then work through real evidence cards: journals, reports, Acts, letters, diaries and recorded interviews.</p></article>
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="27" cy="27" r="16" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="4"/><path d="M39 39l16 16" stroke="#4a2e1b" stroke-width="6" stroke-linecap="round"/><circle cx="27" cy="23" r="5" fill="#4a2e1b"/><path d="M18 35c2-6 16-6 18 0" fill="#4a2e1b"/></svg>
   <h3>Ask</h3><p>Three real witnesses. The same three questions for each: <em>What did they say they saw? Could they really have seen it? Why might they say it?</em></p></article>
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 8v46M18 54h28M12 18h40" stroke="#4a2e1b" stroke-width="3.5" stroke-linecap="round"/><path d="M12 18l-8 16h16zM52 18l-8 16h16z" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="3" stroke-linejoin="round"/><circle cx="32" cy="8" r="3.5" fill="#a67c2e"/></svg>
   <h3>Decide</h3><p>Write your finding and the one piece of evidence behind it. Say how sure you are. <strong>“We can’t know”</strong> is always a fair finding when the record will not support more.</p></article>
 </div>
 <div class="cant-know"><span class="stamp stamp-flat">We can’t know</span><p>Sometimes the most honest finding. A governor who wrote “conjecture”. A witness who was not allowed to speak. A list written and later lost. Saying what the record cannot tell us is part of the work.</p></div>

 <h3 class="sub">The session, step by step</h3>
 <ol class="runsheet">
  <li><span class="rs-t">Choose</span><span>Pick one case file below. Work alone, in pairs or in a small team.</span></li>
  <li><span class="rs-t">Read</span><span>Open the envelope and the agreed file. Mark what is agreed and what is disputed.</span></li>
  <li><span class="rs-t">Evidence</span><span>Work through the evidence cards. Note who made each one, when, and for whom.</span></li>
  <li><span class="rs-t">Ask</span><span>Question the three witnesses with the same three questions.</span></li>
  <li><span class="rs-t">Bias Button</span><span>Press the Bias Button on one source and answer its four questions.</span></li>
  <li><span class="rs-t">Decide</span><span>Write your finding, what you still can’t know, and how sure you are.</span></li>
  <li><span class="rs-t">Take it away</span><span>Download or print your case file. Your answers print with it.</span></li>
 </ol>
 <p class="note">Your typed answers stay in this browser, on this device only. Nothing is sent anywhere.</p>
</section>

<section class="cases-sec" id="cases" aria-labelledby="h-cases">
 <div class="wrap">
  <p class="eyebrow">Choose your case</p>
  <h2 id="h-cases">Six case files. One question each.</h2>
  <div class="cases-intro">
   <div class="map-wrap">{map_svg()}<p class="note">Tap a pin or a card to open its case file. Map outline simplified.</p></div>
   <div class="tiles">{tiles}</div>
  </div>
 </div>
</section>

<div class="wrap cases-wrap">
 <div class="case-switch" aria-label="Switch case"><span>Case files:</span><ul>{case_opts}</ul></div>
 {cases}
</div>

<section class="bias-sec" id="bias" aria-labelledby="h-bias">
 <div class="wrap">
  <p class="eyebrow">The Bias Button activity</p>
  <h2 id="h-bias">Spotting bias in a source</h2>
  <div class="bias-grid">
   <div>
    <p>Every source was made by someone, for a reason. Some words soften what happened. Some leave people out. Some tell you who belongs, who to blame, or what to do next. The Bias Button asks the same four questions of every source, from a paper of 1858 to a post from this week.</p>
    <ol class="four-q"><li>Who made it, and why?</li><li>Who is missing?</li><li>What are the loaded words doing?</li><li>What does it want you to think or do?</li></ol>
    <p class="note">The button does not give the answer. “We can’t know” is a fair finding when a source will not support a firm claim.</p>
   </div>
   <article class="try-card">
    <p class="ev-kind">Try it now · First World War poster · 1915</p>
    <h4>“To the women of Australia… won’t you help and send a man to the front today?”</h4>
    <p class="ev-cite"><strong>Source.</strong> Australian War Memorial, ARTV02512 (catalogue also at C98067). A 1915 poster printed by the Victorian Government Printer, which puts questions to women and urges them to send “lovers, brothers and friends” to enlist. Public domain.</p>
    <p class="ev-links"><a class="src-link" href="https://www.awm.gov.au/collection/C98067" target="_blank" rel="noopener">Open the poster at the War Memorial ↗</a></p>
    {bias_panel('bias-try')}
   </article>
  </div>
  <h3 class="sub">Four investigations in the Bias Button app</h3>
  <p class="note">The first two are about racism in historical sources, the core of the app. The next two use the same button on gender, wartime and class. Each has a modern comparison chosen in class: a real, dated, published example, never an invented one, and never one that names a private person. Some sources use racist, sexist or violent language; the app carries content notes and quotes only short extracts.</p>
  <div class="inv-grid">{bias_cards}</div>
  <div class="app-card">
   <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/bias-button-qr.png" alt="QR code that opens The Bias Button"></button></figure>
   <div><p class="env-eyebrow">The full activity</p><h4>The Bias Button</h4><p>Four investigations, each with Read, Ask and a finding, plus Super Sleuths and a Teacher Note.</p>
   <p><a class="btn btn-primary" href="https://robmac10.github.io/bias-button/" target="_blank" rel="noopener">Open the Bias Button ↗</a> <span class="url">robmac10.github.io/bias-button/</span></p></div>
  </div>
 </div>
</section>

<section class="class-sec wrap" id="classroom" aria-labelledby="h-class">
 <p class="eyebrow">Take it to your classroom</p>
 <h2 id="h-class">A ready-to-use approach</h2>
 <p>The same routine works for every case file and every app in the Reopen the Record family. Run it in one long lesson, or split it across two.</p>
 <div class="lesson">
  <div class="lesson-step"><span class="ls-time">5 min</span><h4>Open the envelope</h4><p>Read the opener aloud. Ask: what do we think we already know? Write it up, to test later.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Read the agreed file</h4><p>Students mark what is agreed and what is still disputed. Teach any new words.</p></div>
  <div class="lesson-step"><span class="ls-time">15 min</span><h4>Evidence stations</h4><p>Print the evidence cards. Groups rotate, noting who made each source, when, and for whom.</p></div>
  <div class="lesson-step"><span class="ls-time">15 min</span><h4>Ask three witnesses</h4><p>Same three questions for every witness. Compare answers across groups.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Bias Button</h4><p>Each group presses the button on one source and reports one loaded word and one missing voice.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Decide</h4><p>Each student writes a finding, one piece of evidence, one thing we can’t know, and sure, maybe or guess.</p></div>
  <div class="lesson-step"><span class="ls-time">5 min</span><h4>Close the file</h4><p>Return to the opening list. What changed? What would we need to settle the question?</p></div>
 </div>
 <p class="note">Suggested timings: about 70 minutes in all. For two lessons, stop after the witnesses.</p>

 <h3 class="sub">Investigation roles</h3>
 <div class="roles">
  <div class="role"><h4>Lead Investigator</h4><p>Keeps the case question in front of the team, and keeps time.</p></div>
  <div class="role"><h4>Archivist</h4><p>Tracks every source: who made it, when, where it is held, and the link.</p></div>
  <div class="role"><h4>Witness Examiner</h4><p>Asks each witness the three questions, and asks “how do you know?”</p></div>
  <div class="role"><h4>Bias Checker</h4><p>Runs the Bias Button and flags loaded words and missing voices.</p></div>
  <div class="role"><h4>Recorder</h4><p>Writes the team’s finding and the “We can’t know” list.</p></div>
 </div>
 <p class="note">Rotate roles between sessions, so every student practises every skill.</p>

 <h3 class="sub">Super Sleuths extension</h3>
 <ul class="sleuths"><li>Open the full case app and its Super Sleuths tab: timelines, source packs, sure / maybe / guess, and harder comparisons.</li>
 <li>Find one more real source on Trove, the National Archives, a state library or the Australian War Memorial. Cite it fully. Does it change the finding?</li>
 <li>Swap cases with another team and test their finding against your evidence.</li>
 <li>Write a “Case reopened” note: evidence for, evidence against, and what we still can’t know.</li></ul>

 <details class="teacher" id="teacher">
  <summary>Teacher Note</summary>
  <div class="teacher-body">
   <p><strong>What is true on this page.</strong> Every date, place and quotation comes from the cited records, as already checked for the live Reopen the Record apps, or from the linked public source. Nothing is invented. Several apps open with a page labelled <em>Imagined</em> (a constructed notebook or diary page, based on real events). Those openers are not reproduced here. Tell students which parts of an app are imagined, and ask how they could check.</p>
   <p><strong>Cultural safety.</strong> Follow the <a href="https://aiatsis.gov.au/research/ethical-research/code-ethics" target="_blank" rel="noopener">AIATSIS Code of Ethics</a> and the protocols of the local communities whose Countries and histories each case concerns. Use only openly shareable, public-record content. There is no secret or sacred material, ceremony, retold cultural story, rock art image or photograph of a deceased Aboriginal or Torres Strait Islander person on this page; silhouettes are used. Seek local guidance before adding community voices, oral histories or images. Keep the advisory notes on student materials.</p>
   <p><strong>Oral histories.</strong> Recorded interviews are linked to their public catalogue entries (National Library of Australia), and published recollections to their source. Living people are quoted only in their published words and are not given dates.</p>
   <p><strong>Harmful language and violence.</strong> Racist historical material is linked to the archive or quoted as a short, attributed extract with a content note. Full racist images are never hosted. Killings are named and counted, not described. Some linked court reports, museum pages and diaries describe violence in detail: preview them before class.</p>
   <p><strong>An apolitical approach.</strong> The routine asks what a source can prove, not what to think. Frame modern comparisons as a study of published language, not a verdict on a person.</p>
   <p><strong>Year levels (for teachers only).</strong> Student pages carry no year level. Each app’s own Teacher Note gives its curriculum links. <em>Frontier (the Bathurst War and Myall Creek)</em> is offered in this workshop for Year 8; the app’s own note maps it to Australian Curriculum v9 Year 9 History (AC9HH9K03), so check the fit for your class.</p>
   <p><strong>Corrections.</strong> If something here should be corrected, it will be updated. The note asking for corrections is permanent.</p>
  </div>
 </details>
</section>

<section class="takeaway wrap" aria-labelledby="h-take">
 <h2 id="h-take">Take your case file with you</h2>
 <p>Choose a case, then press <strong>Download / print my case file</strong>. In the print window, choose <em>Save as PDF</em> to keep it. Your case file prints with a cover, the evidence, your answers, the Bias Button activity and the classroom approach.</p>
 <p class="take-btns">{''.join(f'<button type="button" class="btn print-case" data-case="{c["id"]}" style="--case:{c["colour"]}">{e(c["title"])}</button>' for c in CASES)}</p>
 <p class="note"><button type="button" class="linkish" id="clear-all">Clear all my answers on this device</button></p>
</section>
</main>


<footer class="foot">
 <div class="wrap">
  <p><strong>Reopen the Record: Australian Histories</strong> · Workshop case files</p>
  <p>Real, cited sources only. No invented quotes, outcomes or faces. Portraits are public-domain images of named public figures; other people are shown as labelled silhouettes. The opening illustration is a drawn scene of an archive desk, made for this page; it is not a historical image.</p>
  <p>Sources are held by, among others: the National Library of Australia (Trove and the Oral History collection), the National Archives of Australia, the Federal Register of Legislation, AIATSIS, the National Museum of Australia, the Western Australian Museum, the State Library of Western Australia, State Library Victoria, Public Record Office Victoria, the Nationaal Archief, AustLII, the Internet Archive (Historical Records of Australia), UNESCO, the Australian War Memorial, ABC News and the Friends of Myall Creek Memorial.</p>
  <p>Search engines are asked not to index this page. If something here should be corrected, please tell the workshop presenter, so the file can be updated.</p>
 </div>
</footer>

<div class="lightbox" id="lightbox" hidden><button type="button" class="lb-close" aria-label="Close">×</button><img alt=""><p class="lb-cap"></p></div>
<script src="assets/app.js?v={V}"></script>
</body>
</html>
'''

if __name__ == '__main__':
    print('parts.py is a library for build.py (the six-case page lives in the rtr-workshop repo).')
