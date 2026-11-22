# Reopen the Record · Eureka: who fired first?

Two pages, both asking search engines not to index them (`noindex` and `robots.txt`):

- `index.html`: the participant page. The investigation only: Eureka opener, briefing, Read/Ask/Decide, the envelope, evidence cards, three witnesses, Bias Button, Decide, Super Sleuths, the app QR, and the six case apps under Explore more. Its take-away is `assets/pdf/take-away-case-file-eureka.pdf`.
- `presenter/index.html`: the presenter page (not linked from the participant page). Run sheet with suggested timings, why one case, prompts and answer guidance per step, the optional condensed option, the six take-aways with year levels, curriculum codes, QR codes and PDFs, the classroom routine and the Teacher Note. Its PDF is `assets/pdf/presenter-notes-eureka.pdf`.

Build both with `python3 tools/build.py`. Content is shared with the six-case workshop page (`tools/content.py`, helpers in `tools/parts.py`). Answers typed on the participant page stay in the visitor's browser.
