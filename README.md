# Reopen the Record · Eureka: a guided investigation

A one-case workshop page: the whole room reopens the Eureka file together (envelope, evidence cards, three witnesses, Bias Button, finding), in 45 to 60 minutes. All six Reopen the Record case files are offered as take-aways, with suggested year levels, QR codes, app links and printable case files.

- `index.html` is generated: `python3 tools/build.py`
- Content is shared with the six-case workshop page (`tools/content.py`, helpers in `tools/parts.py`).
- `assets/pdf/` holds the printable case files. The Eureka file is exported from this page; the other five come from the full workshop page.
- Answers typed on the page stay in the visitor's browser (localStorage). Nothing is sent anywhere.
- Search engines are asked not to index the site (`noindex` and `robots.txt`).
