"""Build the participant page (index.html) and the presenter page (presenter/index.html) for the Eureka workshop. Helpers and content are shared with the six-case page."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html import escape as e
from parts import pic, ta, bias_panel, evidence_card, witness_card, BIAS_INV
from content import CASES

V = '20261123h1'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = {c['id']: c for c in CASES}
EU = C['eureka']
import copy
# Participant copy: the same records, with classroom and teacher wording taken out.
EUP = copy.deepcopy(EU)
EUP['country'] = 'This file is about the Eureka Stockade at Ballarat, on Wadawurrung Country. Some linked accounts of the battle describe wounds and deaths in detail.'
EUP['evidence'][4]['kind'] = 'Diary · 1853–1855'
EUP['evidence'][4]['cite'] = 'State Library Victoria, “An eyewitness account of the Eureka Stockade”. Once wrongly said to be by Samuel Lazarus. It records a death.'
ESTABLISHED = [
 ('During 1854 police checked digger licences, and the diggers grew angry.', [1, 2]),
 ('On 29 November a huge meeting on Bakery Hill burned licences and raised the blue Southern Cross flag.', [1]),
 ('On 30 November Peter Lalor led the diggers in an oath under the flag.', [1]),
 ('Thomas’s force of 276 men (100 mounted, 176 on foot) left the Government Camp early on 3 December; Thomas wrote, “At 3 o’clock I left”. Witnesses differ on the time of the attack: Carboni woke at “full dawn, not daylight”.', [3, 1]),
 ('Thirteen men, including Raffaello Carboni, were tried for high treason in 1855. All were found not guilty.', [1, 4]),
]
# Bibliography: (anchor, citation html, supports)
BIB = [
 ('carboni', 'Carboni, Raffaello. <cite>The Eureka Stockade: The Consequence of Some Pirates Wanting on Quarter-Deck a Rebellion</cite>. Melbourne, 1855. Free full text: Project Gutenberg, eBook 3546.', 'https://www.gutenberg.org/ebooks/3546',
  'Established: licence checks and anger; the Bakery Hill meeting of 29 November, licence burning and the Southern Cross flag (chs XXVI–XXXII; the flag described in ch. XXXVII); Lalor’s oath of 30 November (ch. XXXVII); “full dawn, not daylight” (ch. LVI); the thirteen tried for high treason and his own “Not Guilty” verdict (chs LXIX, LXXIII, XC). Also Evidence C and Witness 3.'),
 ('lalor', 'Lalor, Peter. “To the Colonists of Victoria.” <cite>The Argus</cite> (Melbourne), 10 April 1855, p. 7. Also printed in the <cite>Geelong Advertiser</cite>, 9 April 1855. National Library of Australia, Trove, article 4806503.', 'https://trove.nla.gov.au/newspaper/article/4806503',
  'Established: licence checks and the diggers’ anger. Also Evidence B and Witness 1.'),
 ('thomas', 'Thomas, Captain J. W. Report to Head Quarters, Camp, Ballaarat, 3 December 1854. Government records held by Public Record Office Victoria. Transcription on Wikisource.', 'https://en.wikisource.org/wiki/Capt._J._W._Thomas_report_to_Headquarters_following_Eureka_rebellion',
  'Established: the force of 276 men, “one hundred mounted men, and one hundred and seventy-six foot”, and “At 3 o’clock I left”. Also Evidence A and Witness 2.'),
 ('prov', 'Public Record Office Victoria. “Eureka on trial: Ballarat goldfields rebellion.” Online exhibition of government records, last updated 18 May 2021.', 'https://prov.vic.gov.au/explore-collection/online-galleries-and-exhibitions/eureka-trial',
  'Established: the treason trials of 1855 “failed to convict any of those charged”. Also holds the records behind Evidence A.'),
 ('argus-1854', '“By Express. Fatal Collision at Ballaarat.” <cite>The Argus</cite> (Melbourne), 4 December 1854, p. 5. National Library of Australia, Trove, article 4801224.', 'https://trove.nla.gov.au/newspaper/article/4801224',
  'Evidence D.'),
 ('evans', 'Evans, Charles. Goldfields diary, 1853–1855. State Library Victoria, “An eyewitness account of the Eureka Stockade” (once wrongly attributed to Samuel Lazarus).', 'https://slv.vic.gov.au/stories/eyewitness-account-eureka-stockade',
  'Evidence E.'),
 ('hayes', '“Anastasia Hayes, A Eureka Heroine.” <cite>Australian Town and Country Journal</cite>, 18 June 1892. Summarised in Eurekapedia, “Anastasia Hayes”.', 'https://eurekapedia.org/Anastasia_Hayes',
  'Inquiry questions (silences) and Super Sleuths.'),
 ('flag', 'Art Gallery of Ballarat. “The Eureka Flag (The Flag of the Southern Cross).” Unknown maker, 1854, wool and cotton; gift of the King family, 2001. On display at the Eureka Centre Ballarat.', 'https://www.artgalleryofballarat.com.au/stories/the-eureka-flag-the-flag-of-the-southern-cross/',
  'Super Sleuths: who sewed the flag. See also the <a href="https://eurekacentreballarat.com.au/about-eureka/" target="_blank" rel="noopener">Eureka Centre ↗</a>.'),
]
EUP['inquiry']['silences'][1] = 'Women of the goldfields, such as Anastasia Hayes, appear in later notices (1892), but no source in this case says she saw the first shot.'

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
 ('Read what reliable sources have established', 5, 3, 'The facts reliable sources have established, with their sources. Mark what is established and what is still disputed.'),
 ('Evidence cards', 12, 10, 'Pairs take one or two cards each (A–E): who made it, when, for whom, and what it says about the first shot. Report back in one sentence.'),
 ('Three witnesses', 12, 10, 'Lalor, Thomas and Carboni. The same three questions for each. Compare answers around the room.'),
 ('Bias Button', 8, 7, 'Everyone presses the button on one source and answers the four questions. Share one loaded word and one missing voice.'),
 ('Decide: our finding', 8, 7, 'Each person chooses a finding, names the one piece of evidence behind it, and says how sure they are. “We can’t know” is allowed.'),
 ('Close the file', 5, 4, 'Return to the list from the start. What changed? Show the take-aways: the printed Eureka file, the Bias Button, and all six cases.'),
]

def eureka_section():
    c = EUP; cid = 'eureka'
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

 <div class="step" id="envelope"><span class="step-n">1</span><h3>Open the envelope</h3></div>
 <div class="opener">{''.join('<p>%s</p>' % e(p) for p in c['opener'])}<p class="opener-src">Every date, place and quotation here is from the records cited below.</p></div>
 <p class="lead-in small-gap est-head"><strong>What reliable sources have established.</strong> <a class="bib-link" href="#bibliography">See the bibliography ↓</a></p>
 <ul class="agreed">{''.join('<li>%s %s</li>' % (e(t), ''.join('<sup class="ref"><a href="#bib-%s" aria-label="Source %d">%d</a></sup>' % (BIB[n-1][0], n, n) for n in refs)) for t, refs in ESTABLISHED)}</ul>

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

 <div class="step"><span class="step-n">+</span><h3>Super Sleuths <small>go further</small></h3></div>
 <ul class="sleuths">{''.join('<li>%s</li>' % e(s) for s in c['sleuths'])}</ul>

 <div class="app-card">
  <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/{app_qr}" alt="QR code that opens {e(app_t)}"></button></figure>
  <div><p class="env-eyebrow">The full case app</p><h4>{e(app_t)}</h4>
  <p>The app has the whole case: the opening page, the witnesses, My finding and Super Sleuths. Scan the code or use the link.</p>
  <p><a class="btn btn-primary" href="{e(app_u)}" target="_blank" rel="noopener">Open the app ↗</a> <span class="url">{e(app_u.replace('https://',''))}</span></p></div>
 </div>
 <p class="credits"><strong>Pictures.</strong> {e(c['credits'])}</p>
 <p class="case-nav"><a class="btn btn-quiet" href="#bias">Next: the Bias Button →</a></p>
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

def explore(cid):
    c = C[cid]; t, u, q = c['app']; src, cap = c['tile_img']
    return f'''<article class="kit" style="--case:{c['colour']}">
 <div class="kit-top"><button type="button" class="zoom-btn kit-zoom" aria-label="Enlarge picture"><img class="kit-pic" src="assets/{src}" alt="{e(cap)}"></button></div>
 <div class="kit-body">
  <p class="kit-dates">{e(c['dates'])}</p><h3>{e(c['title'])}</h3><p class="kit-q">{e(c['question'])}</p>
  <div class="kit-row"><figure class="kit-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/{q}" alt="QR code that opens {e(t)}"></button></figure>
  <div class="kit-links"><a class="btn btn-primary" href="{e(u)}" target="_blank" rel="noopener">Open the case ↗</a>
  <span class="url">{e(u.replace('https://',''))}</span></div></div>
 </div></article>'''

def page():
    bias_cards = ''.join(f'<article class="inv"><h4>{e(t)}</h4><p>{e(d)}</p><p class="note">Sources include {e(s)} <a href="{u}" target="_blank" rel="noopener">{e(lt)} ↗</a></p></article>' for t,d,s,u,lt in BIAS_INV)
    run_rows = ''.join(f'<tr><th scope="row"><span class="rs-n">{i+1}</span> {e(n)}</th><td class="t">{a} min</td><td class="t">{b} min</td><td>{e(d)}</td></tr>' for i,(n,a,b,d) in enumerate(RUN))
    tot_a = sum(r[1] for r in RUN); tot_b = sum(r[2] for r in RUN)
    explores = ''.join(explore(k[0]) for k in KITS)
    bib_items = ''.join(f'<li id="bib-{a}">{cit} <a href="{u}" target="_blank" rel="noopener">{e(u.replace("https://","").split("/")[0])} ↗</a> <span class="bib-sup">Supports: {sup}</span></li>' for a, cit, u, sup in BIB)
    bias_bib = ''.join(f'<li>Bias Button investigation {e(t)}: {e(src)} <a href="{u}" target="_blank" rel="noopener">{e(lt)} ↗</a></li>' for t, d, src, u, lt in BIAS_INV)
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
<title>Reopen the Record · Eureka: who fired first?</title>
<meta name="description" content="Reopen the Eureka file: read real records, ask three witnesses, press the Bias Button, and decide. Then explore five more case files.">
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
 <div class="pc-qrs"><figure><img class="pc-qr-case" src="assets/qr/eureka-qr.png" alt=""><figcaption>The full Eureka app</figcaption></figure><figure><img src="assets/qr/bias-button-qr.png" alt=""><figcaption>The Bias Button</figcaption></figure><figure><img src="assets/qr/workshop-eureka-qr.png" alt=""><figcaption>This page: explore all six cases</figcaption></figure></div>
 <p class="pc-note">Investigator: ______________________________ &nbsp; Date: ______________</p>
 <p class="pc-small">This file includes histories of First Nations peoples. Aboriginal and Torres Strait Islander readers are advised that it names people who have died. No photographs of them are used. Sources are cited with their links. Your answers stay on your device unless you print them.</p>
</div>
<a class="skip" href="#main">Skip to the workshop</a>
<header class="topbar">
 <div class="topbar-in">
  <a class="brand" href="#top">Reopen the Record<small>Eureka · a guided investigation</small></a>
  <nav aria-label="Sections"><a href="#investigate">Investigate</a><a href="#case-eureka">Eureka file</a><a href="#bias">Bias Button</a><a href="#bibliography">Bibliography</a><a href="#explore">Explore more</a></nav>
 </div>
</header>
<p class="banner">This workshop includes histories of First Nations peoples and of colonial violence. Aboriginal and Torres Strait Islander participants are advised that it names people who have died. It shows no photographs of them: silhouettes are used. It retells no cultural stories and shows no rock art. Some linked sources use the racist language of their time; they carry a content note. If something here should be corrected, please let us know, so the file can be updated.</p>

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
     <div class="hero-actions"><a class="btn btn-primary" href="#investigate">Investigate Eureka</a><a class="btn" href="#case-eureka">Open the Eureka file</a></div>
    </div>
   </div>
   <span class="stamp" aria-hidden="true">Case reopened</span>
  </div>
  <figure class="hero-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-eureka-qr.png" alt="QR code that opens this workshop page"></button><figcaption>Scan to open this page on a phone.</figcaption></figure>
 </div>
</section>

<section class="brief wrap" aria-labelledby="h-brief">
 <div class="memo">
  <p class="memo-head" id="h-brief">Briefing</p>
  <p>In this guided investigation, you step into the role of investigator and reopen one Australian history case file together: <strong>Eureka</strong>, Ballarat, 1854.</p>
  <p>Using primary sources, evidence cards, three witnesses and the Bias Button, you will reopen the record in a culturally appropriate and apolitical way, through questions about the people, documents, silences, and questions the official story never fully settled.</p>
  <p>You will leave with your Eureka case file, the Bias Button, and links to all six case files: Deep Time, Batavia, Eureka, Federation, Freedom Ride and Frontier.</p>
  <p class="closing">Real people. Real records. Real questions the record never settled.</p>
  <p class="closing closing-2">What a terrible thing to lose.</p>
 </div>
</section>

<section class="decide-point wrap" id="investigate" aria-labelledby="h-inv">
 <div class="dp-grid">
  <div class="dp-art" aria-hidden="true">
   <svg viewBox="0 0 240 260" role="img" focusable="false">
    <ellipse cx="120" cy="246" rx="78" ry="9" fill="#4a2e1b" opacity=".18"/>
    <!-- detective silhouette: deerstalker cap, cape coat -->
    <path d="M70 244c-2-46 8-86 30-104h40c22 18 32 58 30 104z" fill="#3a2a1f"/>
    <path d="M62 170c14-22 34-32 58-32s44 10 58 32l-10 30c-12-16-28-24-48-24s-36 8-48 24z" fill="#4a3426"/>
    <rect x="108" y="122" width="24" height="22" rx="6" fill="#3a2a1f"/>
    <circle cx="120" cy="100" r="30" fill="#3a2a1f"/>
    <path d="M86 92c2-26 16-40 34-40s32 14 34 40c-10-6-22-8-34-8s-24 2-34 8z" fill="#5a4030"/>
    <path d="M84 92c-14 2-22 8-24 14 12-2 24-4 34-6zM156 92c14 2 22 8 24 14-12-2-24-4-34-6z" fill="#5a4030"/>
    <path d="M104 58c4-8 10-12 16-12s12 4 16 12" stroke="#6b4c38" stroke-width="4" fill="none" stroke-linecap="round"/>
    <!-- arm and big magnifying glass -->
    <path d="M150 176c16 4 30-4 40-20" stroke="#3a2a1f" stroke-width="16" fill="none" stroke-linecap="round"/>
    <line x1="196" y1="148" x2="182" y2="170" stroke="#7a4a1e" stroke-width="12" stroke-linecap="round"/>
    <circle cx="206" cy="122" r="30" fill="#e8f0f6" fill-opacity=".85" stroke="#a67c2e" stroke-width="9"/>
    <path d="M192 110a18 18 0 0 1 16-8" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
   </svg>
  </div>
  <div class="dp-body">
   <p class="eyebrow">Decision point</p>
   <h2 id="h-inv">Investigate Eureka</h2>
   <p class="dp-lead">Two ways in. Choose one: the full case app, or the case file on this page.</p>
   <div class="dp-choices">
    <a class="dp-card dp-app" href="https://robmac10.github.io/who-fired-first/" target="_blank" rel="noopener">
     <span class="dp-tab">Choice A</span>
     <svg class="dp-ico" viewBox="0 0 64 64" aria-hidden="true"><rect x="16" y="4" width="32" height="56" rx="6" fill="none" stroke="currentColor" stroke-width="4"/><rect x="21" y="12" width="22" height="36" rx="2" fill="currentColor" opacity=".25"/><circle cx="32" cy="54" r="2.6" fill="currentColor"/><path d="M26 22h12M26 29h12M26 36h8" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
     <span class="dp-title">Open the App</span>
     <span class="dp-sub">Who Fired First? The whole case on your phone or tablet. Opens in a new tab ↗</span>
    </a>
    <a class="dp-card dp-env" href="#envelope">
     <span class="dp-tab">Choice B</span>
     <svg class="dp-ico" viewBox="0 0 64 64" aria-hidden="true"><rect x="5" y="14" width="54" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="4"/><path d="M5 17l27 20 27-20" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/><circle cx="32" cy="37" r="6" fill="#e0be82"/></svg>
     <span class="dp-title">Open the Envelope</span>
     <span class="dp-sub">Work through the case file here: evidence cards, three witnesses, the Bias Button and your finding ↓</span>
    </a>
   </div>
  </div>
 </div>
</section>


<div class="wrap cases-wrap">
 {eureka_section()}
</div>

<section class="bias-sec" id="bias" aria-labelledby="h-bias">
 <div class="wrap">
  <p class="eyebrow">The Bias Button · go further</p>
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
  <p class="note">The first two are about racism in historical sources, the core of the app. The next two use the same button on gender, wartime and class. Each ends with a modern comparison: a real, dated, published example, never an invented one, and never one that names a private person. Some sources use racist, sexist or violent language; the app carries content notes and quotes only short extracts.</p>
  <div class="inv-grid">{bias_cards}</div>
  <div class="app-card">
   <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/bias-button-qr.png" alt="QR code that opens The Bias Button"></button></figure>
   <div><p class="env-eyebrow">The full activity</p><h4>The Bias Button</h4><p>Four investigations, each with Read, Ask and a finding, plus Super Sleuths.</p>
   <p><a class="btn btn-primary" href="https://robmac10.github.io/bias-button/" target="_blank" rel="noopener">Open the Bias Button ↗</a> <span class="url">robmac10.github.io/bias-button/</span></p></div>
  </div>
 </div>
</section>

<section class="bib wrap" id="bibliography" aria-labelledby="h-bib">
 <p class="eyebrow">Bibliography</p>
 <h2 id="h-bib">Sources for this case file</h2>
 <p class="note">Numbers match the small numbers in “What reliable sources have established”. Each entry says what it supports. Picture credits are given with the pictures.</p>
 <ol class="bib-list">{bib_items}</ol>
 <h3 class="sub">The Bias Button</h3>
 <ul class="bib-list bib-plain">
  <li id="bib-awm">Australian War Memorial. “To the women of Australia…” recruiting poster, 1915, printed by the Victorian Government Printer. ARTV02512 (catalogue also at C98067). <a href="https://www.awm.gov.au/collection/C98067" target="_blank" rel="noopener">awm.gov.au ↗</a> <span class="bib-sup">Supports: the “Try it again” poster.</span></li>
  {bias_bib}
 </ul>
</section>

<section class="mine-sec wrap" id="take-away" aria-label="Your Eureka case file">
  <div class="mine">
   <h3>Your Eureka case file</h3>
   <p>Press the button, then choose <em>Save as PDF</em> in the print window to keep it. It prints with a cover, the evidence, your answers, the Bias Button, the bibliography and the links to all six cases.</p>
   <p><button type="button" class="btn btn-primary print-case" data-case="eureka">Download / print my Eureka case file</button> <a class="btn" href="assets/pdf/take-away-case-file-eureka.pdf" download>Blank Eureka case file (PDF) ↓</a></p>
   <p class="note"><button type="button" class="linkish" id="clear-all">Clear all my answers on this device</button></p>
  </div>
</section>

<section class="kits-sec" id="explore" aria-labelledby="h-explore">
 <div class="wrap">
  <p class="eyebrow">Explore more</p>
  <h2 id="h-explore">Six case files. Reopen another.</h2>
  <details class="explore-panel">
   <summary class="dp-card dp-explore">
    <span class="dp-tab">Explore more</span>
    <svg class="dp-ico" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"><path d="M4 10h10l3 3h11v13H4z"/><path d="M36 10h10l3 3h11v13H36z"/><path d="M4 36h10l3 3h11v13H4z"/><path d="M36 36h10l3 3h11v13H36z"/></g><circle cx="48" cy="46" r="9" fill="none" stroke="#e0be82" stroke-width="4"/><path d="M54 52l7 7" stroke="#e0be82" stroke-width="5" stroke-linecap="round"/></svg>
    <span class="dp-title">Explore all six cases</span>
    <span class="dp-sub">Deep Time, Batavia, Eureka, Federation, Freedom Ride and Frontier. Tap to open the case cards, with QR codes and links <span class="dp-chev" aria-hidden="true">▾</span></span>
   </summary>
   <p class="kits-lead">Every case is built the same way: an envelope, evidence cards, three witnesses, the Bias Button and a finding. Scan a code or tap a link to open the full case.</p>
   <div class="kits">{explores}</div>
  </details>
 </div>
</section>

<section class="closing-sec wrap" aria-label="Closing">
 <div class="memo closing-memo">
  <p class="closing">Real people. Real records. Real questions the record never settled.</p>
  <p class="closing closing-2">What a terrible thing to lose.</p>
 </div>
</section>

</main>

<footer class="foot">
 <div class="wrap">
  <p><strong>Reopen the Record: Australian Histories</strong> · Eureka: who fired first?</p>
  <p>Real, cited sources only. No invented quotes, outcomes or faces. Portraits are public-domain images of named public figures; other people are shown as labelled silhouettes. The opening illustration is a drawn scene of an archive desk, made for this page; it is not a historical image.</p>
  <p>Eureka sources are held by, among others: Public Record Office Victoria, State Library Victoria, the National Library of Australia (Trove) and Wikisource. The other case files cite the National Archives of Australia, the Federal Register of Legislation, AIATSIS, the National Museum of Australia, the Western Australian Museum, the State Library of Western Australia, the Nationaal Archief, AustLII, the Internet Archive, UNESCO, the Australian War Memorial, ABC News and the Friends of Myall Creek Memorial.</p>
  <p>Search engines are asked not to index this page. If something here should be corrected, please let us know, so the file can be updated.</p>
 </div>
</footer>

<div class="lightbox" id="lightbox" hidden><button type="button" class="lb-close" aria-label="Close">×</button><img alt=""><p class="lb-cap"></p></div>
<script src="assets/app.js?v={V}"></script>
</body>
</html>
'''


# ---------------- Presenter page (presenter/index.html; not linked from the participant page) ----------------
# Each step: (prompts to the room, what the cited sources support). Drawn only from the case's cited records
# and the Who Fired First? app's Teacher Note.
GUIDE = [
 ('Open the envelope',
  ['Read the opener aloud. Ask: what do we think we already know about Eureka? Write it up, to test at the end.',
   'Words to check: licence, stockade, sentry, signal shot, volley.'],
  ['Every record agrees there was shooting before dawn on 3 December 1854. The dispute is who started it.',
   'Captain Thomas led 276 men (100 mounted, 176 on foot). Inside the stockade there were far fewer diggers.']),
 ('Read what reliable sources have established',
  ['Which source supports each fact? (The numbers lead to the bibliography.) Which detail is still disputed?'],
  ['The licence burning and the Southern Cross flag on Bakery Hill (29 November) and Lalor’s oath (30 November) are established from Carboni’s account (chs XXVI–XXXII, XXXVII); the participant page’s bibliography lists every source.',
   'Thomas wrote “At 3 o’clock I left”; witnesses differ on the time of the attack (Carboni woke at “full dawn, not daylight”).',
   'Thirteen men, including Carboni, were tried for high treason in 1855. All were found not guilty.']),
 ('Evidence cards',
  ['For each card: who made it, when, for whom, and were they there?',
   'Which card was written closest to the event? Which was written for the public?'],
  ['A. Thomas wrote the same day, to his superiors. He says his men were fired on “without word or challenge”, and that only then did he order “commence firing”. He does not mention a warning shot from a sentry.',
   'B. Lalor wrote four months later, to the newspapers: “I believe that one or two signal shots were fired by our sentries”, and “The military fired the first volley.” He separates a signal shot from a volley, and hedges with “I believe”.',
   'C. Carboni, a year later: he woke to “a discharge of musketry—then a round from the bugle”. He does not say which side fired.',
   'D. The Argus of 4 December was the first report in Melbourne. No complete set of the Ballarat Times from 1854 survives.',
   'E. The State Library Victoria diary was once wrongly credited to Samuel Lazarus; it is now attributed to Charles Evans. It records a death: preview it before sharing.']),
 ('Three witnesses',
  ['What did they say they saw? Could they really have seen it? Why might they say it?',
   'Where was each witness standing, and what could they not see in the half-light?'],
  ['Lalor was inside the stockade, as the diggers’ leader. Thomas commanded the attacking force outside it. Carboni was asleep in a tent “the second from the stockade”.',
   'Strong answers notice that Thomas wrote for his superiors, that Lalor chooses careful words, and that Carboni heard the firing but does not name a side.',
   'When quoting, check the originals: some modern summaries change Lalor’s “fifteen yards” to “fifteen feet” and his “twenty with pikes” to thirty.']),
 ('Bias Button',
  ['Who made it, and why? Who is missing? What are the loaded words doing? What does it want you to think or do?',
   'Ask for one loaded word and one missing voice from the room.'],
  ['Thomas calls the diggers “insurgents”. Lalor writes “our sentries”. Each word places the writer on a side.',
   'Missing voices: the sentries are never named; the women of the goldfields appear only in later notices. No source in this case says Anastasia Hayes saw the first shot.']),
 ('Decide: our finding',
  ['Rebels, soldiers, or we can’t know: which piece of evidence most changed your mind? How sure are you?'],
  ['There is no answer key. Historians still disagree about who fired first.',
   'Strong findings use more than one witness, separate a signal shot from a volley, say who could see what, and say how sure they are. “We can’t know” is a legitimate finding.',
   'Nobody knows exactly how many died: diggers, soldiers, and at least one woman.']),
 ('Close the file',
  ['Return to the list from the start. What changed? What would we need to settle the question?',
   'How did Eureka affect the way the colony was governed?'],
  ['The stockade was taken in minutes. Lalor was badly wounded and hidden by friends. The thirteen accused were found not guilty. The licence was soon replaced, and Lalor was later elected to Victoria’s parliament.']),
]

def kit_p(cid, yr, curric, pdf):
    return kit(cid, yr, curric, pdf)

def presenter_page():
    run_rows = ''.join(f'<tr><th scope="row"><span class="rs-n">{i+1}</span> {e(n)}</th><td class="t">{a} min</td><td class="t">{b} min</td><td>{e(d)}</td></tr>' for i,(n,a,b,d) in enumerate(RUN))
    tot_a = sum(r[1] for r in RUN); tot_b = sum(r[2] for r in RUN)
    guide = ''.join(f"""<article class="g-step"><div class="g-head"><span class="rs-n">{i+1}</span><h3>{e(n)}</h3><span class="g-time">{RUN[i][1]} min · condensed {RUN[i][2]} min</span></div>
 <div class="g-cols"><div class="g-ask"><h4>Ask the room</h4><ul>{''.join('<li>%s</li>' % e(x) for x in pr)}</ul></div>
 <div class="g-ans"><h4>What the sources support</h4><ul>{''.join('<li>%s</li>' % e(x) for x in an)}</ul></div></div></article>""" for i,(n,pr,an) in enumerate(GUIDE))
    kits = ''.join(kit_p(*k) for k in KITS)
    html_ = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
<title>Presenter notes · Reopen the Record · Eureka</title>
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/image-fit.css?v={V}">
<link rel="stylesheet" href="assets/style.css?v={V}">
<link rel="stylesheet" href="assets/eureka.css?v={V}">
</head>
<body class="presenter-page">
<a class="skip" href="#main">Skip to the notes</a>
<header class="topbar">
 <div class="topbar-in">
  <a class="brand" href="#top">Reopen the Record<small>Presenter notes · Eureka</small></a>
  <nav aria-label="Presenter sections"><a href="#run">Run sheet</a><a href="#guide">Step by step</a><a href="#takeaways">Take-aways</a><a href="#teacher">Teacher Note</a></nav>
 </div>
</header>
<main id="main">
<section class="p-head wrap" id="top" aria-labelledby="h-p">
 <div class="folder" style="--case:#2c4a7a">
  <span class="folder-tab">Presenter</span><span class="string" aria-hidden="true"></span>
  <div class="folder-grid">
   <div>
    <p class="env-eyebrow">Reopen the Record · Eureka, Ballarat, 1854</p>
    <h1 id="h-p">Presenter notes</h1>
    <p class="key-q">One case in the room: everyone reopens Eureka together. Six case files to take away.</p>
    <div class="case-actions">
     <button type="button" class="btn btn-primary" id="print-presenter">Download / print presenter notes</button>
     <a class="btn" href="assets/pdf/presenter-notes-eureka.pdf" download>Presenter notes (PDF) ↓</a>
     <a class="btn btn-quiet" href="../" target="_blank" rel="noopener">Open the participant page ↗</a>
    </div>
   </div>
   <figure class="qr p-qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-eureka-qr.png" alt="QR code that opens the participant page"></button><figcaption>Show this code to the room: it opens the participant page.</figcaption></figure>
  </div>
 </div>
 <p class="note">This page is for the presenter. It is not linked from the participant page, and search engines are asked not to index it.</p>
</section>

<section class="why wrap" aria-labelledby="h-why">
 <p class="eyebrow">Why one case in the room</p>
 <h2 id="h-why">One file, opened properly.</h2>
 <div class="why-grid">
  <article class="why-card"><span class="why-n">1</span><h3>Focus</h3><p>A guided investigation needs focus. Switching cases mid-session dilutes the “reopen the file” experience.</p></article>
  <article class="why-card"><span class="why-n">2</span><h3>It fits the time</h3><p>Envelope, evidence cards, three witnesses, Bias Button, finding: one case fits 45–60 minutes. Several cases do not.</p></article>
  <article class="why-card"><span class="why-n">3</span><h3>Teachers see how it scales</h3><p>Every case file is built the same way. Work through one and teachers can see how the other five run, from Year 4 to Year 10.</p></article>
 </div>
</section>

<section class="session wrap" id="run" aria-labelledby="h-run">
 <p class="eyebrow">Run sheet</p>
 <h2 id="h-run">Suggested timings</h2>
 <div class="run-wrap"><table class="run">
  <thead><tr><th scope="col">Step</th><th scope="col" class="t">Full</th><th scope="col" class="t">Condensed</th><th scope="col">What happens</th></tr></thead>
  <tbody>{run_rows}</tbody>
  <tfoot><tr><th scope="row">In all</th><td class="t">about {tot_a} min</td><td class="t">about {tot_b} min</td><td>Everyone works through the same steps together.</td></tr></tfoot>
 </table></div>
 <p class="note">Timings are suggestions. For a 60-minute slot, add five minutes of questions at the end.</p>
 <div class="presenter"><strong>Condensed option (optional).</strong> Give each pair one evidence card and one witness, then hear the other answers from the room. Everyone still presses the Bias Button and writes a finding.</div>
</section>

<section class="guide wrap" id="guide" aria-labelledby="h-guide">
 <p class="eyebrow">Step by step</p>
 <h2 id="h-guide">Prompts and answer guidance</h2>
 <p class="note">The guidance uses only the records cited in the case file and the Who Fired First? app’s Teacher Note. It is not an answer key: the record does not settle who fired first.</p>
 <div class="g-list">{guide}</div>
</section>

<section class="kits-sec" id="takeaways" aria-labelledby="h-kits">
 <div class="wrap">
  <p class="eyebrow">Take-aways for teachers</p>
  <h2 id="h-kits">Six case files. Pick your year level.</h2>
  <p class="kits-lead">Every case is built the same way: envelope, evidence cards, three witnesses, Bias Button, finding. Each has a full app, a QR code and a printable case file. Year levels are suggestions, taken from each app’s own Teacher Note (Australian Curriculum v9). The printable case files include a classroom routine and a Teacher Note.</p>
  <div class="kits">{kits}</div>
  <div class="app-card all-card">
   <figure class="qr"><button type="button" class="zoom-btn" aria-label="Enlarge QR code"><img src="assets/qr/workshop-qr.png" alt="QR code that opens the full workshop page with all six case files"></button></figure>
   <div><p class="env-eyebrow">The full workshop page</p><h4>All six case files, ready to use</h4><p>Every case worked through on one page, with evidence cards, witnesses, inquiry questions, a classroom routine and a print button for each.</p>
   <p><a class="btn btn-primary" href="https://robmac10.github.io/rtr-workshop/" target="_blank" rel="noopener">Open the full workshop page ↗</a> <span class="url">robmac10.github.io/rtr-workshop/</span></p></div>
  </div>
 </div>
</section>

<section class="class-sec wrap" id="classroom" aria-labelledby="h-class">
 <p class="eyebrow">Take it to the classroom</p>
 <h2 id="h-class">A ready-to-use approach</h2>
 <div class="presenter"><strong>Presenter note.</strong> The same structure works across Years 4 to 10. Eureka runs well with the whole room; in class, teachers choose the case for their year level, from Deep Time and Batavia (Year 4) to the Freedom Ride (Year 10). <em>Frontier</em> (the Bathurst War and Myall Creek) is suited to Year 8/9.</div>
 <div class="lesson">
  <div class="lesson-step"><span class="ls-time">5 min</span><h4>Open the envelope</h4><p>Read the opener aloud. Ask: what do we think we already know? Write it up, to test later.</p></div>
  <div class="lesson-step"><span class="ls-time">10 min</span><h4>Read what is established</h4><p>Students mark what reliable sources have established and what is still disputed. Teach any new words.</p></div>
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

 <details class="teacher" id="teacher" open>
  <summary>Teacher Note</summary>
  <div class="teacher-body">
   <p><strong>Year levels.</strong> The same structure works across Years 4 to 10. Year levels come from each app’s own Teacher Note: Deep Time and Batavia, Year 4; Eureka, Year 5; Federation, Year 6; Freedom Ride, Year 10. <em>Frontier</em> is suited to Year 8/9; the app’s own note maps it to Australian Curriculum v9 Year 9 History (AC9HH9K03), so check the fit for your class. Participant pages carry no year level.</p>
   <p><strong>What is true on these pages.</strong> Every date, place and quotation comes from the cited records, as already checked for the live Reopen the Record apps, or from the linked public source. Nothing is invented. Several apps open with a page labelled <em>Imagined</em> (for Eureka, Nell’s Diary). Those openers are not reproduced on the workshop pages. Tell students which parts of an app are imagined, and ask how they could check.</p>
   <p><strong>Cultural safety.</strong> Follow the <a href="https://aiatsis.gov.au/research/ethical-research/code-ethics" target="_blank" rel="noopener">AIATSIS Code of Ethics</a> and the protocols of the local communities whose Countries and histories each case concerns. Eureka took place on Wadawurrung Country. There is no secret or sacred material, ceremony, retold cultural story, rock art image or photograph of a deceased Aboriginal or Torres Strait Islander person on these pages; silhouettes are used.</p>
   <p><strong>Violence and harmful language.</strong> Men died at Eureka, and at least one woman’s death is recorded. Some linked reports, memoirs and diaries describe wounds and deaths in detail, including the Charles Evans diary: preview them before class. Racist historical material in the other cases is linked or quoted as a short, attributed extract with a content note.</p>
   <p><strong>An apolitical approach.</strong> The routine asks what a source can prove, not what to think. Frame modern comparisons in the Bias Button as a study of published language, not a verdict on a person.</p>
   <p><strong>Corrections.</strong> If something here should be corrected, it will be updated. The note asking for corrections is permanent.</p>
  </div>
 </details>
</section>
</main>
<footer class="foot">
 <div class="wrap">
  <p><strong>Reopen the Record: Australian Histories</strong> · Eureka presenter notes</p>
  <p>Real, cited sources only. No invented quotes, outcomes or faces. Search engines are asked not to index this page.</p>
 </div>
</footer>
<div class="lightbox" id="lightbox" hidden><button type="button" class="lb-close" aria-label="Close">×</button><img alt=""><p class="lb-cap"></p></div>
<script src="assets/app.js?v={V}"></script>
<script>document.getElementById('print-presenter').addEventListener('click',function(){{window.print();}});</script>
</body>
</html>
"""
    return html_.replace('"assets/', '"../assets/')

os.makedirs(os.path.join(ROOT, 'presenter'), exist_ok=True)
open(os.path.join(ROOT, 'presenter', 'index.html'), 'w').write(presenter_page())
print('wrote presenter/index.html')
open(os.path.join(ROOT, 'index.html'), 'w').write(page())
print('wrote index.html')
