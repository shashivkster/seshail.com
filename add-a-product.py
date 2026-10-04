#!/usr/bin/env python3
"""
Builds the Products section: products.html plus one detail page per product.

TO ADD ANOTHER PRODUCT
----------------------
Append one entry to PRODUCTS below and re-run this script. It writes the
index card, the detail page, the nav and footer entries and the sitemap
line. Nothing else needs touching.
"""

import re, glob, os, json

DOMAIN = "https://seshail.com"
EMAIL = "seshailkamanna@bdo.in"

# --------------------------------------------------------------------------
# PRODUCTS — newest first. Each becomes a card on products.html and a page.
# --------------------------------------------------------------------------
PRODUCTS = [
{
 "slug": "fieldcheck",
 "name": "FieldCheck",
 "eyebrow": "Inspection and field data capture",
 "status": ("Working build", "pill-live"),
 "pitch": "Inspections that stand up when someone asks.",
 "what": "Captures checklists, photos and signatures in the field, works with "
         "no signal, and keeps the record intact from the first answer through "
         "to the closed corrective action.",
 "facts": ["17 roles", "4 modelled processes", "23 tests passing", "Works offline"],
 "meta_desc": "FieldCheck — offline-capable inspection and field data capture software: "
              "checklists, photo evidence, signatures, review workflow and corrective actions.",
 "keyfacts": [
   ("Category", "Enterprise software"),
   ("Status", "Working build, pilot-ready"),
   ("Deployment", "Desktop, container, managed or multi-tenant"),
   ("Documents", "BRD v0.3 · User manual v1.1"),
   ("Platform", "Web, responsive to phone"),
 ],
 "live_url": "https://claude.ai/artifact/7MThD3V7BRMH9ACHb6rt3N",
 "live_label": "Open the full product page",
 "intro": [
   "Field inspections generate arguments. Whether the work was really done on "
   "site. Whether a critical item passed. Who signed it off, and whether that "
   "person should have been allowed to. Which version of the checklist was "
   "actually used. Each of those is settled by a record, and the record is "
   "usually the weakest part of the process.",
   "FieldCheck is built around that record. An inspector works through a "
   "checklist on a phone with no signal, attaches photographs and a signature, "
   "and the answers sync when the connection returns — without a retry ever "
   "creating a duplicate. A failed critical question fails the inspection "
   "whatever the overall score says. The reviewer cannot be the inspector, and "
   "whoever raised a corrective action cannot be the one who closes it. "
   "Template versions are frozen on publication, so an inspection always shows "
   "the exact version it was run against.",
 ],
 "sections": [
   ("What it settles", [
     ("Was it really done on site?",
      "Inspectors keep working offline. Answers sync when the connection "
      "returns, and a retry never creates a duplicate."),
     ("Did the critical item pass?",
      "A failed critical question fails the inspection, whatever the overall "
      "score says."),
     ("Who signed it off?",
      "The reviewer cannot be the inspector, and the person who raised an "
      "action cannot be the one who closes it."),
     ("Which checklist was used?",
      "Template versions are immutable. An inspection always shows the exact "
      "version it was run against."),
   ]),
 ],
 "process": ("Four processes, modelled in BPMN", [
    ("P-01 Template", "Authoring, review and publication. Publishing freezes the version."),
    ("P-02 Inspection", "Scheduling and execution. Run on site, capture evidence, sync online or not."),
    ("P-03 Review", "Review, approval and record closure. The person who did the work does not sign it off."),
    ("P-04 Action", "Corrective and preventive action lifecycle. Closing needs a different person from the one who raised it."),
 ]),
 "deploy": ("Four ways to run it", [
    ("Windows desktop, single file", "One site or a small team on a LAN, no IT involvement. SQLite, data in the user profile."),
    ("Container on a small host", "A pilot or a department. PostgreSQL optional."),
    ("Managed platform", "An organisation-wide rollout with backups and monitoring."),
    ("Multi-tenant service", "Several customers on one platform."),
 ]),
 "built": [
    "Templates, inspections, review, actions and reports",
    "Offline queue with duplicate-free sync",
    "Role-based access and separation-of-duties rules",
    "Responsive front end; 23 backend tests passing",
    "Windows executable build — tested on Linux, not yet on Windows",
 ],
 "pending": [
    "Multi-tenant isolation (requirements MT-01 to MT-13)",
    "The seven operating layers of supportability",
    "Code signing for the Windows executable",
 ],
 "disclaim": "FieldCheck is an independent product and is not affiliated with or "
             "endorsed by any third-party inspection software vendor. Supporting "
             "documents are marked confidential and are shared on request for "
             "evaluation.",
},
{
 "slug": "fitdiary",
 "name": "FitDiary",
 "eyebrow": "Fitness tracking for aspiring athletes",
 "status": ("On Google Play", "pill-live"),
 "pitch": "Training logs a coach has actually verified.",
 "what": "Aspiring players record their training; partner coaches and academies "
         "validate the entries afterwards, so the record carries weight. Partner "
         "gyms and sports nutrition stores offer discounts when players hit targets.",
 "facts": ["Android", "Google Play", "Coach-validated", "Partner rewards"],
 "meta_desc": "FitDiary — an Android fitness tracking app where aspiring players log "
              "training that partner coaches and academies validate, with partner rewards for hitting targets.",
 "keyfacts": [
   ("Category", "Consumer mobile"),
   ("Platform", "Android"),
   ("Distribution", "Google Play"),
   ("Status", "Published"),
 ],
 "live_url": "",
 "live_label": "",
 "intro": [
   "Most fitness apps take the user's word for it. That is fine when the log is "
   "for your own motivation, and useless the moment it needs to persuade "
   "somebody else — a selector, an academy, a sponsor.",
   "FitDiary separates the two. A player records their training as they would "
   "anywhere else, and a partner coach or academy validates the entries "
   "afterwards. A validated history is worth something a self-reported one is "
   "not. Partner gyms, fitness studios and sports nutrition stores attach "
   "discounts to targets, so hitting them pays off immediately as well as "
   "eventually.",
 ],
 "sections": [],
 "process": None,
 "deploy": None,
 "built": [],
 "pending": [],
 "disclaim": "FitDiary is an independent product. Partner programmes are subject to "
             "the terms published in the app.",
},
]

# --------------------------------------------------------------------------
src = open("index.html").read()
HEADER = re.search(r'<header class="masthead">.*?</header>', src, re.S).group(0)
FOOTER = re.search(r'<footer>.*?</footer>', src, re.S).group(0)

NAV_JS = """
document.getElementById('yr').textContent=new Date().getFullYear();
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rise').forEach(function(el){io.observe(el);});
(function(){
  var t=document.getElementById('navToggle'), n=document.getElementById('primaryNav');
  if(!t||!n) return;
  t.addEventListener('click',function(){
    var open=n.classList.toggle('open');
    t.setAttribute('aria-expanded',String(open));
    t.setAttribute('aria-label',open?'Close menu':'Open menu');
  });
  n.addEventListener('click',function(e){ if(e.target.closest('a')){n.classList.remove('open');t.setAttribute('aria-expanded','false');} });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&n.classList.contains('open')){n.classList.remove('open');t.setAttribute('aria-expanded','false');t.focus();}
  });
})();
"""

ICON = ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<link rel="manifest" href="/site.webmanifest">\n'
        '<meta name="theme-color" content="#0D1A26">')


def shell(fname, title, desc, jsonld, content):
    url = f"{DOMAIN}/{fname}"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="Seshail Kamanna">
<meta property="og:site_name" content="Seshail Kamanna">
<meta property="og:locale" content="en_IN">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
{ICON}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">
{json.dumps(jsonld, indent=1, ensure_ascii=False)}
</script>
</head>
<body>
<script>document.documentElement.className+=' js';</script>

{HEADER}

{content}

{FOOTER}

<script>{NAV_JS}</script>
</body>
</html>
"""
    open(fname, "w").write(html)
    print("built", fname)


# ---------------------------------------------------------------- index page
cards = []
for p in PRODUCTS:
    label, cls = p["status"]
    facts = "\n".join(f'          <li>{x}</li>' for x in p["facts"])
    cards.append(f"""      <a class="appcard rise" href="{p['slug']}.html">
        <div class="appcard-top">
          <div>
            <span class="label">{p['eyebrow']}</span>
            <h3 style="margin-top:.5rem">{p['name']}</h3>
          </div>
          <span class="pill {cls}">{label}</span>
        </div>
        <p class="pitch">{p['pitch']}</p>
        <p class="what">{p['what']}</p>
        <ul class="appfacts">
{facts}
        </ul>
        <span class="go">View details <span aria-hidden="true">&rarr;</span></span>
      </a>""")

index_content = f"""<section class="subhero">
  <div class="wrap">
    <a class="crumb" href="index.html">&larr; Home</a>
    <span class="label">Products</span>
    <h1>Software I have built</h1>
    <p class="lead">Advisory work shows you the same problems repeatedly. Occasionally
    one is worth building a product around rather than writing another recommendation
    about. These are the ones that got built.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="appgrid">
{chr(10).join(cards)}
    </div>
  </div>
</section>

<section class="band band-dark on-dark">
  <div class="wrap cta">
    <h2 style="font-size:clamp(1.5rem,1.2rem + 1.4vw,2.2rem)">Interested in a pilot, or in building something similar?</h2>
    <a class="btn btn-light" href="contact.html">Get in touch</a>
  </div>
</section>
"""

shell("products.html",
      "Products &mdash; software built by Seshail Kamanna",
      "Software products built by Seshail Kamanna, including FieldCheck inspection "
      "software and the FitDiary fitness app.",
      {"@context": "https://schema.org", "@type": "CollectionPage",
       "name": "Products", "url": f"{DOMAIN}/products.html",
       "about": [{"@type": "SoftwareApplication", "name": p["name"],
                  "url": f"{DOMAIN}/{p['slug']}.html"} for p in PRODUCTS]},
      index_content)


# ---------------------------------------------------------------- detail pages
def detail(p):
    label, cls = p["status"]
    kf = "\n".join(
        f'        <li><b>{k}</b><span>{v}</span></li>' for k, v in p["keyfacts"])
    intro = "\n".join(f'      <p>{t}</p>' for t in p["intro"])

    links = []
    if p["live_url"]:
        links.append(f'<a class="btn" href="{p["live_url"]}" target="_blank" rel="noopener">{p["live_label"]} <span aria-hidden="true">&rarr;</span></a>')
    links.append('<a class="btn btn-ghost" href="contact.html#clients">Enquire about a pilot</a>')
    links_html = f'      <div class="applinks">\n        ' + "\n        ".join(links) + "\n      </div>"

    blocks = [f"""<section class="subhero">
  <div class="wrap">
    <a class="crumb" href="products.html">&larr; All products</a>
    <span class="label">{p['eyebrow']}</span>
    <h1>{p['name']}</h1>
    <p class="lead">{p['pitch']}</p>
  </div>
</section>

<section class="band">
  <div class="wrap applead">
    <div class="prose rise">
{intro}
{links_html}
    </div>
    <aside class="panel panel-sticky rise">
      <h4>At a glance</h4>
      <ul class="keyfacts">
{kf}
      </ul>
    </aside>
  </div>
</section>"""]

    for heading, items in p["sections"]:
        tiles = "\n".join(
            f'  <div class="tile"><h4>{h}</h4><p>{t}</p></div>' for h, t in items)
        blocks.append(f"""<section class="band band-mist">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="label">{heading}</span>
      <h2>Four arguments that usually end up in a meeting.</h2>
    </div>
    <div class="tiles rise">
{tiles}
    </div>
  </div>
</section>""")

    if p["process"]:
        heading, items = p["process"]
        steps = "\n".join(
            f'  <li class="step"><h4>{h}</h4><p>{t}</p></li>' for h, t in items)
        blocks.append(f"""<section class="band">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="label">Process</span>
      <h2>{heading}.</h2>
      <p>Each has owners, hand-offs, and the rule that stops it being short-circuited.</p>
    </div>
    <ol class="steps rise">
{steps}
    </ol>
  </div>
</section>""")

    if p["deploy"]:
        heading, items = p["deploy"]
        tiles = "\n".join(
            f'  <div class="tile"><h4>{h}</h4><p>{t}</p></div>' for h, t in items)
        blocks.append(f"""<section class="band band-mist">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="label">Deployment</span>
      <h2>{heading}.</h2>
    </div>
    <div class="tiles rise">
{tiles}
    </div>
  </div>
</section>""")

    if p["built"] or p["pending"]:
        b = "\n".join(f'        <li>{x}</li>' for x in p["built"])
        g = "\n".join(f'        <li>{x}</li>' for x in p["pending"])
        blocks.append(f"""<section class="band band-dark on-dark">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="label">Status</span>
      <h2>What is finished, and what is not.</h2>
      <p>Stated plainly, because a product described as complete when it is not
      wastes everybody's first meeting.</p>
    </div>
    <div class="statuscols rise">
      <div>
        <h4><span class="dot" style="background:#5BC08B"></span>Built and tested</h4>
        <ul>
{b}
        </ul>
      </div>
      <div>
        <h4><span class="dot" style="background:#D8B565"></span>Designed, not yet built</h4>
        <ul>
{g}
        </ul>
      </div>
    </div>
  </div>
</section>""")

    others = [q for q in PRODUCTS if q["slug"] != p["slug"]]
    if others:
        rows = "\n".join(
            f'      <a class="palink" href="{q["slug"]}.html"><b>{q["status"][0]}</b>'
            f'<span>{q["name"]}</span><i aria-hidden="true">&rarr;</i></a>'
            for q in others)
        blocks.append(f"""<section class="band band-mist">
  <div class="wrap">
    <div class="sec-head rise">
      <span class="label">More</span>
      <h2>Other products.</h2>
    </div>
    <div class="palinks rise">
{rows}
    </div>
    <p class="disclaim">{p['disclaim']}</p>
  </div>
</section>""")

    blocks.append(f"""<section class="band band-dark on-dark">
  <div class="wrap cta">
    <h2 style="font-size:clamp(1.5rem,1.2rem + 1.4vw,2.2rem)">Want to talk about a pilot?</h2>
    <a class="btn btn-light" href="contact.html#clients">Get in touch</a>
  </div>
</section>""")

    jsonld = {"@context": "https://schema.org", "@type": "SoftwareApplication",
              "name": p["name"], "description": p["meta_desc"],
              "url": f"{DOMAIN}/{p['slug']}.html",
              "applicationCategory": "BusinessApplication",
              "author": {"@type": "Person", "name": "Seshail Kamanna",
                         "url": f"{DOMAIN}/"}}

    shell(f"{p['slug']}.html",
          f"{p['name']} &mdash; {p['eyebrow']} | Seshail Kamanna",
          p["meta_desc"], jsonld, "\n\n".join(blocks))


for p in PRODUCTS:
    detail(p)


# ---------------------------------------------------------------- wire it in
for f in sorted(glob.glob("*.html")):
    h = open(f).read()
    o = h
    if '<a href="products.html">Products</a>' not in h:
        h = h.replace('      <a href="news.html">Tech news</a>',
                      '      <a href="products.html">Products</a>\n      <a href="news.html">Tech news</a>', 1)
    if 'Products</h5>' not in h:
        prod_links = "\n".join(
            f'          <li><a href="{p["slug"]}.html">{p["name"]}</a></li>' for p in PRODUCTS)
        h = h.replace("""      <div class="foot-col">
        <h5>Contact</h5>""",
f"""      <div class="foot-col">
        <h5>Products</h5>
        <ul>
          <li><a href="products.html">All products</a></li>
{prod_links}
        </ul>
      </div>
      <div class="foot-col">
        <h5>Contact</h5>""", 1)
    if h != o:
        open(f, "w").write(h)
        print("wired:", f)


# ---------------------------------------------------------------- sitemap
PRI = {"index.html": "1.0", "contact.html": "0.9", "products.html": "0.9",
       "news.html": "0.7", "blog.html": "0.7"}
urls = []
for f in sorted(glob.glob("*.html")):
    loc = DOMAIN + "/" + ("" if f == "index.html" else f)
    freq = "daily" if f == "news.html" else ("weekly" if f in ("index.html", "blog.html", "products.html") else "monthly")
    urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{PRI.get(f,'0.8')}</priority>\n  </url>")
open("sitemap.xml", "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "\n".join(urls) + "\n</urlset>\n")
print(f"sitemap.xml rewritten with {len(urls)} URLs")
