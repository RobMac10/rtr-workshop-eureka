"""Build index.html for the one-case (Eureka) workshop page. Helpers and content are shared with the six-case page."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html import escape as e
from parts import pic, ta, bias_panel, evidence_card, witness_card, BIAS_INV
from content import CASES

V = '20261123e5'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = {c['id']: c for c in CASES}
EU = C['eureka']

# Year levels are taken from each app's own Teacher Note (Australian Curriculum v9). Teacher-facing only.
KITS = [
 ('deep-time', 'Year 4', 'Year 4 HASS · AC9HS4K01, AC9HS4K06', 'take-away-case-file-deep-time.pdf'),
 ('batavia', 'Year 4', 'Year 4 HASS · AC9HS4K02', 'take-away-case-file-batavia.pdf'),
 ('eureka', 'Year 5', 'Year 5 HASS (History) · AC9HS5K03', 'take-away-case-file-eureka.pdf'),
 ('federation', 'Year 6', 'Year 6 HASS · AC9HS6K01', 'take-away-case-file-federation.pdf'),
 ('frontier', 'Years 8–9', 'The app maps it to Year 9 History · AC9HH9K03', 'take-away-case-file-frontier.pdf'),
 ('freedom-ride', 'Year 10', 'Year 10 History · AC9HH10K10, AC9HH10K11', 'take-away-case-file-freedom-ride.pdf'),
]

# Suggested timings (minutes): full 55, condensed 45
RUN = [
 ('Open the envelope', 5, 4, 'Read the opener aloud together. Ask the room: what do we think we already know about Eureka? Write it up, to test later.'),
 ('Read what is agreed', 5, 3, 'The few things every record agrees on. Mark what is agreed and what is still disputed.'),
 ('Evidence cards', 12, 10, 'Pairs take one or two cards each (A–E): who made it, when, for whom, and what it says about the first shot. Report back in one sentence.'),
 ('Three witnesses', 12, 10, 'Lalor, Thomas and Carboni. The same three questions for each. Compare answers around the room.'),
 ('Bias Button', 8, 7, 'Everyone presses the button on one source and answers the four questions. Share one loaded word and one missing voice.'),
 ('Decide: our finding', 8, 7, 'Each person chooses a finding, names the one piece of evidence behind it, and says how sure they are. “We can’t know” is allowed.'),
 ('Close the file', 5, 4, 'Return to the list from the start. What changed? Show the take-aways: the printed Eureka file, the Bias Button, and all six cases.'),
]

def eureka_section():
    c = EU; cid = 'eureka'
    inq = c['inquiry']
    cols = [('People','people','Who was there? Who speaks, and who is spoken for?'),('Documents','documents','Who made each record, when, and for whom?'),
            ('Silences','silences','What is missing, lost, or never asked?'),('Still unsettled','unsettled','What can the record not settle?')]
    inq_html = ''.join('<div class="inq inq-%s"><h4>%s</h4><p class="note">%s</p><ul>%s</ul></div>' % (k, t, e(sub), ''.join('<li>%s</li>' % e(x) for x in inq[k])) for t,k,sub in cols)
    decide = ''.join('<label class="choice"><input type="radio" name="%s-find" value="%d" data-key="%s-find"> <span>%s</span></label>' % (cid, i, cid, e(o)) for i,o in enumerate(c['decide']))
    decide += '<label class="choice"><input type="radio" name="%s-find" value="own" data-key="%s-find"> <span>My own finding, written below.</span></label>' % (cid, cid)
    ev_opts = ''.join('<label class="choice"><input type="radio" name="eu-bb-src" value="%s" data-key="eureka-bb-src"> <span>Evidence %s: %s</span></label>' % ('ABCDE'[i], 'ABCDE'[i], e(ev['title'])) for i, ev in enumerate(c['evidence']))
    bq = ['Who made it, and why?','Who is missing?','What are the loaded words doing?','What does it want you to think or do?']
    app_t, app_u, app_qr = c['app']
    return f'''
<section class="case open print-me" id="case-eureka" data-case="eureka" style="--case:{c['colour']}" aria-labelledby="h-eureka">
 <div class="case-head">
  <div class="folder">
   <span class="folder-tab">Case file</span><span class="string" aria-hidden="true"></span>
   <div class="folder-grid">
    <div>
     <p class="env-eyebrow">Reopen the Record · Ballarat · {e(c['dates'])}</p>
     <h2 id="h-eureka">{e(c['title'])}</h2>
     <p class="key-q">{e(c['question'])}</p>
     <div class="case-actions">
      <button type="button" class="btn btn-primary print-case" data-case="eureka">Download / print my case file</button>
      <a class="btn" href="{e(app_u)}" target="_blank" rel="noopener">Open the full app ↗</a>
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
 <p class="lead-in small-gap"><strong>What the record agrees on.</strong></p>
 <ul class="agreed">{''.join('<li>%s</li>' % e(a) for a in c['agreed'])}</ul>

 <div class="step"><span class="step-n">2</span><h3>Evidence cards</h3></div>
 <p class="lead-in">Five real documents, each with its citation and a link to the archive. Read your card. Who made it, when, and for whom?</p>
 <div class="ev-grid">{''.join(evidence_card(c,i,ev) for i,ev in enumerate(c['evidence']))}</div>

 <div class="step"><span class="step-n">3</span><h3>Three witnesses, three questions</h3></div>
 <p class="lead-in">Ask every witness the same three questions. Tap a picture to enlarge it.</p>
 <div class="witnesses">{''.join(witness_card(c,i,w) for i,w in enumerate(c['witnesses']))}</div>

 <div class="step"><span class="step-n">4</span><h3>Bias Button</h3></div>
 <div class="bb-step">
  <div class="bb-intro">
   <span class="bb-big" aria-hidden="true">Bias<br>Button</span>
   <div><p>Choose one Eureka source and press the button: the same four questions for every source. The button does not give the answer.</p>
   <ol class="four-q mini">{''.join('<li>%s</li>' % q for q in bq)}</ol></div>
  </div>
  <fieldset class="bb-pick"><legend>The source I am checking</legend>{ev_opts}</fieldset>
  <div class="bb-qs">{''.join(ta('eureka-bb%d' % i, q, 2) for i, q in enumerate(bq))}</div>
 </div>

 <div class="step"><span class="step-n">5</span><h3>Decide: my finding</h3></div>
 <details class="inq-wrap"><summary>Before you decide: inquiry questions on people, documents, silences, and what is still unsettled</summary>
  <div class="inq-grid">{inq_html}</div>
 </details>
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

 <div class="step"><span class="step-n">+</span><h3>Super Sleuths <small>after the session</small></h3></div>
 <ul class="sleuths">{''.join('<li>%s</li>' % e(s) for s in c['sleuths'])}</ul>

 <div class="app-card">
  <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/{app_qr}" alt="QR code that opens {e(app_t)}"></button></figure>
  <div><p class="env-eyebrow">The full case app</p><h4>{e(app_t)}</h4>
  <p>The app has the whole case: the opening page, the witnesses, My finding, Super Sleuths and a Teacher Note. Scan the code or use the link.</p>
  <p><a class="btn btn-primary" href="{e(app_u)}" target="_blank" rel="noopener">Open the app ↗</a> <span class="url">{e(app_u.replace('https://',''))}</span></p></div>
 </div>
 <p class="credits"><strong>Pictures.</strong> {e(c['credits'])}</p>
 <p class="case-nav"><a class="btn btn-quiet" href="#takeaways">Next: take-aways for every year level →</a></p>
</section>'''

def kit(cid, yr, curric, pdf):
    c = C[cid]; t, u, q = c['app']
    src, cap = c['tile_img']
    return f'''<article class="kit" style="--case:{c['colour']}">
 <div class="kit-top"><button type="button" class="zoom-btn kit-zoom" aria-label="Enlarge picture"><img class="kit-pic" src="assets/{src}" alt="{e(cap)}" loading="lazy"></button><span class="kit-yr">{e(yr)}</span></div>
 <div class="kit-body">
  <p class="kit-dates">{e(c['dates'])}</p><h3>{e(c['title'])}</h3><p class="kit-q">{e(c['question'])}</p>
  <p class="kit-cur">{e(curric)}</p>
  <div class="kit-row"><figure class="kit-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/{q}" alt="QR code that opens {e(t)}"></button></figure>
  <div class="kit-links"><a class="btn btn-primary" href="{e(u)}" target="_blank" rel="noopener">Open the app ↗</a>
  <a class="btn" href="assets/pdf/{pdf}" download>Case file PDF ↓</a>
  <span class="url">{e(u.replace('https://',''))}</span></div></div>
 </div></article>'''

def page():
    bias_cards = ''.join(f'<article class="inv"><h4>{e(t)}</h4><p>{e(d)}</p><p class="note">Sources include {e(s)} <a href="{u}" target="_blank" rel="noopener">{e(lt)} ↗</a></p></article>' for t,d,s,u,lt in BIAS_INV)
    run_rows = ''.join(f'<tr><th scope="row"><span class="rs-n">{i+1}</span> {e(n)}</th><td class="t">{a} min</td><td class="t">{b} min</td><td>{e(d)}</td></tr>' for i,(n,a,b,d) in enumerate(RUN))
    tot_a = sum(r[1] for r in RUN); tot_b = sum(r[2] for r in RUN)
    kits = ''.join(kit(*k) for k in KITS)
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
<title>Reopen the Record · Eureka: a guided investigation</title>
<meta name="description" content="A guided investigation for the whole room: reopen the Eureka file, read real records, ask three witnesses, press the Bias Button, and decide. Six case files to take away.">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/image-fit.css?v={V}">
<link rel="stylesheet" href="assets/style.css?v={V}">
<link rel="stylesheet" href="assets/eureka.css?v={V}">
</head>
<body class="one-case">
<div class="print-cover" aria-hidden="true">
 <img class="pc-hero" src="assets/img/hero.jpg" alt="">
 <p class="pc-eyebrow">Reopen the Record · Workshop case file</p>
 <h1 class="pc-title">Eureka</h1>
 <p class="pc-q">{e(EU['question'])}</p>
 <p class="pc-tag">Real people. Real records. Real questions the record never settled.</p>
 <div class="pc-qrs"><figure><img class="pc-qr-case" src="assets/qr/eureka-qr.png" alt=""><figcaption>The full Eureka app</figcaption></figure><figure><img src="assets/qr/bias-button-qr.png" alt=""><figcaption>The Bias Button</figcaption></figure><figure><img src="assets/qr/workshop-qr.png" alt=""><figcaption>All six case files</figcaption></figure></div>
 <p class="pc-note">Investigator: ______________________________ &nbsp; Date: ______________</p>
 <p class="pc-small">This file includes histories of First Nations peoples. Aboriginal and Torres Strait Islander readers are advised that it names people who have died. No photographs of them are used. Sources are cited with their links. Your answers stay on your device unless you print them.</p>
</div>
<a class="skip" href="#main">Skip to the workshop</a>
<header class="topbar">
 <div class="topbar-in">
  <a class="brand" href="#top">Reopen the Record<small>Eureka · a guided investigation</small></a>
  <nav aria-label="Workshop sections"><a href="#session">The session</a><a href="#case-eureka">Eureka file</a><a href="#bias">Bias Button</a><a href="#takeaways">Take-aways</a><a href="#classroom">Teachers</a></nav>
 </div>
</header>
<p class="banner">This workshop includes histories of First Nations peoples and of colonial violence. Aboriginal and Torres Strait Islander participants are advised that it names people who have died. It shows no photographs of them: silhouettes are used. It retells no cultural stories and shows no rock art. Some linked sources use the racist language of their time; they carry a content note. If something here should be corrected, please tell the workshop presenter, so the file can be updated.</p>

<main id="main">
<section class="hero hero-eureka" id="top" aria-labelledby="h-title">
 <div class="hero-art" role="img" aria-label="Illustration: case-file folders tied with red string, a brass scales of justice, a magnifying glass and old documents on an archive desk."></div>
 <div class="hero-in">
  <div class="envelope">
   <span class="folder-tab">Today’s case</span><span class="string" aria-hidden="true"></span><span class="ring" aria-hidden="true"></span>
   <div class="env-grid">
    <div>
     <p class="env-eyebrow">Reopen the Record · Ballarat · 3 December 1854</p>
     <h1 id="h-title">Eureka</h1>
     <p class="env-sub">{e(EU['question'])}</p>
     <p class="tagline">Real people. Real records. Real questions the record never settled.</p>
     <div class="hero-actions"><a class="btn btn-primary" href="#case-eureka">Open the Eureka file</a><a class="btn" href="#session">The session</a><a class="btn btn-quiet" href="#takeaways">All six cases</a></div>
    </div>
    <div class="env-pic">{pic(EU['tile_img'][0], EU['tile_img'][1])}</div>
   </div>
   <span class="stamp" aria-hidden="true">Case reopened</span>
  </div>
  <figure class="hero-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-eureka-qr.png" alt="QR code that opens this workshop page"></button><figcaption>Scan to open this page on a phone.</figcaption></figure>
 </div>
</section>

<section class="brief wrap" aria-labelledby="h-brief">
 <div class="memo">
  <p class="memo-head" id="h-brief">Briefing</p>
  <p>In this guided investigation, you step into the role of investigator. Together, the whole room reopens one Australian history case file: <strong>Eureka</strong>, Ballarat, 1854.</p>
  <p>Using primary sources, evidence cards, three witnesses and a Bias Button activity, you will reopen the record in a culturally appropriate and apolitical way. You will examine different perspectives and publicly available records, through specific inquiry questions that explore the people, documents, silences, and questions the official story never fully settled.</p>
  <p>By the end of the session you will leave with the Eureka case file, the Bias Button activity, a ready-to-use approach for immediate classroom use, and links to all six case files (Deep Time, Batavia, Eureka, Federation, Freedom Ride and Frontier) for the year levels you teach.</p>
  <p class="closing">Real people. Real records. Real questions the record never settled.</p>
  <p class="closing closing-2">What a terrible thing to lose.</p>
 </div>
</section>

<section class="why wrap" aria-labelledby="h-why">
 <p class="eyebrow">Why one case in the room</p>
 <h2 id="h-why">One file, opened properly.</h2>
 <div class="why-grid">
  <article class="why-card"><span class="why-n">1</span><h3>Focus</h3><p>A guided investigation needs focus. Switching cases mid-session dilutes the “reopen the file” experience.</p></article>
  <article class="why-card"><span class="why-n">2</span><h3>It fits the time</h3><p>Envelope, evidence cards, three witnesses, Bias Button, finding: one case fits 45–60 minutes. Several cases do not.</p></article>
  <article class="why-card"><span class="why-n">3</span><h3>You see how it scales</h3><p>Every case file is built the same way. Work through one and you can see how the other five run, from Year 4 to Year 10.</p></article>
 </div>
</section>

<section class="session wrap" id="session" aria-labelledby="h-session">
 <p class="eyebrow">The guided session</p>
 <h2 id="h-session">Read. Ask. Decide.</h2>
 <div class="rad">
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="12" y="6" width="40" height="52" rx="3" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="3"/><path d="M20 18h24M20 26h24M20 34h24M20 42h14" stroke="#4a2e1b" stroke-width="3"/></svg>
   <h3>Read</h3><p>Open the envelope and the evidence cards: an official report, a letter to the newspapers, an eyewitness book, the first Melbourne report and a diary.</p></article>
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="27" cy="27" r="16" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="4"/><path d="M39 39l16 16" stroke="#4a2e1b" stroke-width="6" stroke-linecap="round"/><circle cx="27" cy="23" r="5" fill="#4a2e1b"/><path d="M18 35c2-6 16-6 18 0" fill="#4a2e1b"/></svg>
   <h3>Ask</h3><p>Three real witnesses, the same three questions: <em>What did they say they saw? Could they really have seen it? Why might they say it?</em> Then press the Bias Button.</p></article>
  <article class="rad-card"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 8v46M18 54h28M12 18h40" stroke="#4a2e1b" stroke-width="3.5" stroke-linecap="round"/><path d="M12 18l-8 16h16zM52 18l-8 16h16z" fill="#fbf3e6" stroke="#4a2e1b" stroke-width="3" stroke-linejoin="round"/><circle cx="32" cy="8" r="3.5" fill="#a67c2e"/></svg>
   <h3>Decide</h3><p>Write your finding and the one piece of evidence behind it. Say how sure you are. <strong>“We can’t know”</strong> is a fair finding when the record will not support more.</p></article>
 </div>
 <div class="cant-know"><span class="stamp stamp-flat">We can’t know</span><p>Sometimes the most honest finding. At Eureka, the people who were there still disagreed about the first shot. Saying what the record cannot tell us is part of the work.</p></div>

 <h3 class="sub">Run sheet for the presenter</h3>
 <div class="run-wrap"><table class="run">
  <thead><tr><th scope="col">Step</th><th scope="col" class="t">Full</th><th scope="col" class="t">Condensed</th><th scope="col">What happens</th></tr></thead>
  <tbody>{run_rows}</tbody>
  <tfoot><tr><th scope="row">In all</th><td class="t">about {tot_a} min</td><td class="t">about {tot_b} min</td><td>Everyone works through the same steps together.</td></tr></tfoot>
 </table></div>
 <p class="note">Timings are suggestions. For a 60-minute slot, add five minutes of questions at the end. In the condensed version, give each pair one evidence card and one witness, and hear the other answers from the room. Typed answers stay in each person’s browser, on their own device only.</p>
</section>

<div class="wrap cases-wrap">
 {eureka_section()}
</div>

<section class="bias-sec" id="bias" aria-labelledby="h-bias">
 <div class="wrap">
  <p class="eyebrow">The Bias Button activity · take it further</p>
  <h2 id="h-bias">A word can hide an act.</h2>
  <div class="bias-grid">
   <div>
    <p>Every source was made by someone, for a reason. Some words soften what happened. Some leave people out. Some tell you who belongs, who to blame, or what to do next. The Bias Button asks the same four questions of every source, from a paper of 1858 to a post from this week.</p>
    <ol class="four-q"><li>Who made it, and why?</li><li>Who is missing?</li><li>What are the loaded words doing?</li><li>What does it want you to think or do?</li></ol>
    <p class="note">The button does not give the answer. “We can’t know” is a fair finding when a source will not support a firm claim.</p>
   </div>
   <article class="try-card">
    <p class="ev-kind">Try it again · First World War poster · 1915</p>
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

<section class="kits-sec" id="takeaways" aria-labelledby="h-kits">
 <div class="wrap">
  <p class="eyebrow">Take-aways for teachers</p>
  <h2 id="h-kits">Six case files. Pick your year level.</h2>
  <p class="kits-lead">Today you opened Eureka. Every case below is built the same way: envelope, evidence cards, three witnesses, Bias Button, finding. Each has a full app, a QR code and a printable case file. Year levels are suggestions, taken from each app’s own Teacher Note (Australian Curriculum v9); the same structure works from Year 4 to Year 10.</p>
  <div class="kits">{kits}</div>
  <div class="app-card all-card">
   <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-qr.png" alt="QR code that opens the full workshop page with all six case files"></button></figure>
   <div><p class="env-eyebrow">The full workshop page</p><h4>All six case files, ready to use</h4><p>Every case worked through on one page, with evidence cards, witnesses, inquiry questions and a print button for each.</p>
   <p><a class="btn btn-primary" href="https://robmac10.github.io/rtr-workshop/" target="_blank" rel="noopener">Open the full workshop page ↗</a> <span class="url">robmac10.github.io/rtr-workshop/</span></p></div>
  </div>
  <div class="mine">
   <h3>Your Eureka case file</h3>
   <p>Press the button, then choose <em>Save as PDF</em> in the print window to keep it. It prints with a cover, the evidence, your answers, the Bias Button, the classroom approach and these links.</p>
   <p><button type="button" class="btn btn-primary print-case" data-case="eureka">Download / print my Eureka case file</button> <a class="btn" href="assets/pdf/take-away-case-file-eureka.pdf" download>Blank Eureka PDF ↓</a></p>
   <p class="note"><button type="button" class="linkish" id="clear-all">Clear all my answers on this device</button></p>
  </div>
 </div>
</section>

<section class="class-sec wrap" id="classroom" aria-labelledby="h-class">
 <p class="eyebrow">Take it to your classroom</p>
 <h2 id="h-class">A ready-to-use approach</h2>
 <div class="presenter"><strong>Presenter note.</strong> The same structure works across Years 4 to 10. Eureka runs well with the whole room; in class, choose the case for your year level, from Deep Time and Batavia (Year 4) to the Freedom Ride (Year 10). <em>Frontier</em> (the Bathurst War and Myall Creek) is suited to Year 8/9.</div>
 <p>The same routine works for every case file and every app in the Reopen the Record family. In a classroom, run it in one long lesson, or split it across two.</p>
 <div class="lesson">
  <div class="lesson-step"><span class="ls-time">5 min</span><h4>Open the envelope</h4><p>Read the opener aloud. Ask: what do we think we already know? Write it up, to test later.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Read the agreed file</h4><p>Students mark what is agreed and what is still disputed. Teach any new words.</p></div>
  <div class="lesson-step"><span class="ls-time">15 min</span><h4>Evidence stations</h4><p>Print the evidence cards. Groups rotate, noting who made each source, when, and for whom.</p></div>
  <div class="lesson-step"><span class="ls-time">15 min</span><h4>Ask three witnesses</h4><p>Same three questions for every witness. Compare answers across groups.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Bias Button</h4><p>Each group presses the button on one source and reports one loaded word and one missing voice.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Decide</h4><p>Each student writes a finding, one piece of evidence, one thing we can’t know, and sure, maybe or guess.</p></div>
  <div class="lesson-step"><span class="ls-time">5 min</span><h4>Close the file</h4><p>Return to the opening list. What changed? What would we need to settle the question?</p></div>
 </div>
 <p class="note">Suggested classroom timings: about 70 minutes in all. For two lessons, stop after the witnesses.</p>

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
 <li>Swap witnesses with another team and test their finding against your evidence.</li>
 <li>Write a “Case reopened” note: evidence for, evidence against, and what we still can’t know.</li></ul>

 <details class="teacher" id="teacher">
  <summary>Teacher Note</summary>
  <div class="teacher-body">
   <p><strong>What is true on this page.</strong> Every date, place and quotation comes from the cited records, as already checked for the live Reopen the Record apps, or from the linked public source. Nothing is invented. Several apps open with a page labelled <em>Imagined</em> (a constructed notebook or diary page, based on real events). Those openers are not reproduced here. Tell students which parts of an app are imagined, and ask how they could check.</p>
   <p><strong>Cultural safety.</strong> Follow the <a href="https://aiatsis.gov.au/research/ethical-research/code-ethics" target="_blank" rel="noopener">AIATSIS Code of Ethics</a> and the protocols of the local communities whose Countries and histories each case concerns. Use only openly shareable, public-record content. There is no secret or sacred material, ceremony, retold cultural story, rock art image or photograph of a deceased Aboriginal or Torres Strait Islander person on this page; silhouettes are used. Seek local guidance before adding community voices, oral histories or images. Keep the advisory notes on student materials.</p>
   <p><strong>Oral histories.</strong> In the other case files, recorded interviews are linked to their public catalogue entries (National Library of Australia), and published recollections to their source. Living people are quoted only in their published words.</p>
   <p><strong>Harmful language and violence.</strong> Racist historical material is linked to the archive or quoted as a short, attributed extract with a content note. Killings are named and counted, not described. Some linked reports, memoirs and diaries describe the fighting at Eureka and its dead: preview them before class.</p>
   <p><strong>An apolitical approach.</strong> The routine asks what a source can prove, not what to think. Frame modern comparisons as a study of published language, not a verdict on a person.</p>
   <p><strong>Year levels (for teachers only).</strong> Student pages carry no year level. The levels in the take-away section come from each app’s own Teacher Note. The same structure works across Years 4 to 10. <em>Frontier</em> is suited to Year 8/9; the app’s own note maps it to Australian Curriculum v9 Year 9 History (AC9HH9K03), so check the fit for your class.</p>
   <p><strong>Corrections.</strong> If something here should be corrected, it will be updated. The note asking for corrections is permanent.</p>
  </div>
 </details>
</section>
</main>

<footer class="foot">
 <div class="wrap">
  <p><strong>Reopen the Record: Australian Histories</strong> · Eureka, a guided investigation</p>
  <p>Real, cited sources only. No invented quotes, outcomes or faces. Portraits are public-domain images of named public figures; other people are shown as labelled silhouettes. The opening illustration is a drawn scene of an archive desk, made for this page; it is not a historical image.</p>
  <p>Eureka sources are held by, among others: Public Record Office Victoria, State Library Victoria, the National Library of Australia (Trove) and Wikisource. The other case files cite the National Archives of Australia, the Federal Register of Legislation, AIATSIS, the National Museum of Australia, the Western Australian Museum, the State Library of Western Australia, the Nationaal Archief, AustLII, the Internet Archive, UNESCO, the Australian War Memorial, ABC News and the Friends of Myall Creek Memorial.</p>
  <p>Search engines are asked not to index this page. If something here should be corrected, please tell the workshop presenter, so the file can be updated.</p>
 </div>
</footer>

<div class="lightbox" id="lightbox" hidden><button type="button" class="lb-close" aria-label="Close">×</button><img alt=""><p class="lb-cap"></p></div>
<script src="assets/app.js?v={V}"></script>
</body>
</html>
'''

open(os.path.join(ROOT, 'index.html'), 'w').write(page())
print('wrote index.html')
