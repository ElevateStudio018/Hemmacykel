"""Genererar docs/*.html för Hemmacykel. Kör: python3 scripts/build.py

Allt innehåll är hämtat från hemmacykel.se (oktober 2026). Cyklarna till salu ligger i
scripts/cyklar.json och bilderna i docs/img/cyklar/.
"""
import html
import json
import pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

SITE = "https://hemmacykel.se"
PHONE, TEL, MAIL = "070-682 88 45", "+46706828845", "hemmacykel@gmail.com"
STREET, ZIP_CITY, AREA = "Almstigen 30", "756 53 Uppsala", "Södra Sunnersta"
MAPS = "https://maps.google.com/?cid=1143771656914339290"
RATING, REVIEW_COUNT = "5,0", 13
UPDATED = "2026-10-28"

e = html.escape

# --- ikoner (Lucide, MIT) -------------------------------------------------------------
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-ur": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "menu": '<path d="M4 8h16"/><path d="M4 16h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
}
STAR = "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"


def ico(name, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


STARS = '<span class="stars" aria-hidden="true">' + "".join(f'<svg viewBox="0 0 24 24"><path d="{STAR}"/></svg>' for _ in range(5)) + "</span>"


def kr(n):
    return f"{n:,}".replace(",", " ") + " kr"


# --- innehåll -------------------------------------------------------------------------
REPAIRS = [  # (värde i bokningen, namn, pris)
    ("punktering", "Punktering", 299),
    ("dackbyte", "Däckbyte", 349),
    ("bromsjustering", "Bromsjustering", 199),
    ("bromsvajer", "Byte av bromsvajer", 249),
    ("bromsklossar", "Byte av bromsklossar", 249),
    ("kedjebyte", "Kedjebyte", 299),
    ("ovrigt", "Övrigt / vet inte", 0),
]

SERVICES = [  # (värde i bokningen, namn, beskrivning, pris, bild)
    ("punktering", "Punktering", "Vi lagar eller byter slang på plats.", 299, "tjanst-punktering.jpg"),
    ("dackbyte", "Däckbyte", "Byte av däck, fram eller bak.", 349, "tjanst-dack.jpg"),
    ("kedjebyte", "Kedjebyte", "Byte och service av kedja.", 299, "tjanst-kedja.jpg"),
    ("bromsjustering", "Bromsjustering", "Justering av bromsarna.", 199, "tjanst-service.jpg"),
    ("bromsklossar", "Byte av bromsklossar", "Nya bromsklossar och justering.", 249, "tjanst-bromsar.jpg"),
    ("bromsvajer", "Byte av bromsvajer", "Ny vajer och justering.", 249, "cyklar/bike3-6.jpg"),
    ("ovrigt", "Övrigt", "Något annat? Beskriv problemet så ger vi ett prisförslag.", 0, "tjanst-ovrigt.jpg"),
]

PACKAGES = [
    ("cykelcheck", "Cykelcheck", 499, "För dig som vill att cykeln ska kännas bra igen",
     ["Kontroll av hela cykeln", "Bromsjustering", "Växeljustering", "Kedjesmörjning", "Däcktryck",
      "Kontroll av däck och bromsbelägg", "Åtdragning av viktiga skruvar", "Säkerhetskontroll"]),
    ("hemmaservice", "Hemmaservice", 749, "För en cykel som behöver lite mer kärlek",
     ["Allt i paket Cykelcheck", "Grundligare genomgång", "Kontroll/justering av hjul", "Genomgång av drivlina",
      "Smörjning av rörliga delar", "Efterdragning av skruvar", "Slitagekontroll"]),
    ("flera-cyklar", "Flera cyklar", 899, "Cykelcheck på 2 cyklar vid samma hembesök",
     ["Kontroll av hela cyklarna", "Bromsjustering", "Växeljustering", "Kedjesmörjning", "Däcktryck",
      "Kontroll av däck och bromsbelägg", "Åtdragning av viktiga skruvar", "Säkerhetskontroll"]),
]
FEATURED = "cykelcheck"

BIKE_TYPES = [  # (värde, namn, tillägg)
    ("vanlig", "Vanlig cykel", 0),
    ("elcykel", "Elcykel", 50),
    ("ladcykel", "Lådcykel", 50),
    ("tandem", "Tandemcykel", 50),
    ("trehjuling", "Trehjuling / specialcykel", 50),
    ("fatbike", "Fatbike", 50),
    ("elsparkcykel", "Elsparkcykel", 100),
]

REVIEWS = [  # (namn, text) – från Google, oktober 2026. Den första visas stort.
    ("Rebecka Astenvald", "Professionellt, snabb service, och bra pris! Väldigt nöjd och skulle anlita igen, kan varmt rekommendera."),
    ("Malin Härenstam", "Snabb och kompetent service som kommer hem till dig! Och dessutom väldigt bra priser."),
    ("Sofia Ribeiro", "Trevlig och superbra kille, fixade cykeln snabbt och det blev jättebra! Fantastiskt nöjd! ❤️🙏"),
    ("Olof", "Snabbt, enkelt, billigt och mycket trevliga att ha att göra med."),
    ("Tristan Johansson", "Bra jobb och väldigt prisvärt med tanke på att dom kommer hem till en"),
    ("Johan", "Kan varmt rekommendera! Proffsigt och prisvärt!"),
    ("Ella Hellberg", "Smidigt, prisvärt, rekommenderar starkt!"),
]

STEPS = [
    ("Boka på någon minut", "Välj hjälpen och tiden som passar din vardag. Vi bekräftar tid och pris via telefon eller e-post."),
    ("Vi fixar den där den står", "Vi kommer hem till dig med allt vi behöver. Du behöver inte lyfta ett finger."),
    ("Rulla vidare", "Betala med Swish när jobbet är klart. Kvitto får du alltid."),
]

FAQ = [
    ("Vad kostar det?", "Det beror på vad du vill ha hjälp med. En punktering ligger på 299 kr, en Cykelcheck på 499 kr och däckbyte på 349 kr. Du ser alltid priset innan vi börjar, så inga överraskningar."),
    ("Hur fungerar det?", "Du bokar en tid här på hemsidan, och sedan kommer vi hem till dig med hela verkstaden. Du behöver inte lyfta ett finger."),
    ("Kan ni serva elcykel?", "Ja, det går bra! Vi tar både vanliga cyklar och elcyklar, allt från bromsar och växlar till kedja, och vi gör en grundläggande koll på motorn också."),
    ("Var i Uppsala kommer ni?", "Hela Uppsala! Centrum, Luthagen, Flogsta, Sala backe, Gottsunda, Sävja, Årsta och fler stadsdelar. Skriv in din adress när du bokar, så ser vi direkt om vi kan komma förbi."),
    ("När kan ni komma?", "På vardagar är vi ute mellan 15 och 19, och på helgerna mellan 9 och 19. Du väljer en tid som passar dig direkt i bokningen."),
    ("Behöver jag ta med cykeln någonstans?", "Nej! Du behöver inte ta dig någonstans. Vi kommer hem och fixar cykeln, så du kan använda tiden till annat."),
    ("Hur betalar jag?", "Betalning sker på plats efter utfört arbete via Swish, om inget annat överenskommits. Kvitto erbjuds alltid och lämnas på begäran."),
    ("Kan jag avboka?", "Ja. Avbokning ska göras senast 24 timmar innan bokad tid. Vid sen avbokning eller utebliven tid kan en avgift tas ut."),
]

BIKES = json.loads((ROOT / "scripts" / "cyklar.json").read_text(encoding="utf-8"))
BIKES.sort(key=lambda b: b["sold"])  # cyklar till salu först

# --- ramverk --------------------------------------------------------------------------
NAV = [("tjanster", "Tjänster"), ("paket", "Paket"), ("omdomen", "Omdömen"), ("om-oss", "Om oss"), ("fragor", "Frågor")]


def logo(light=False):
    mark = "logo-mark-vit.png" if light else "logo-mark.png"
    return f'<img src="img/{mark}" alt="" width="34" height="30"><span>Hemmacykel</span>'


def nav_href(anchor, home):
    return f"#{anchor}" if home else f"index.html#{anchor}"


def header(home, current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{nav_href(a, home)}">{t}</a>' for a, t in NAV)
    links += f'<a href="cyklar.html"{cur if current == "cyklar.html" else ""}>Cyklar till salu</a>'
    drawer = "".join(f'<li><a href="{nav_href(a, home)}">{t}</a></li>' for a, t in NAV)
    drawer += '<li><a href="cyklar.html">Cyklar till salu</a></li>'
    return f'''<header class="site-h">
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="Hemmacykel, till startsidan">{logo()}</a>
    <nav class="mainnav" aria-label="Huvudmeny">{links}</nav>
    <div class="nav-cta">
      <a class="nav-tel" href="tel:{TEL}">{PHONE}</a>
      <a class="btn btn-ink btn-sm" href="boka.html">Boka service</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Meny">{ico("menu", "i i-open")}{ico("x", "i i-close")}</button>
    </div>
  </div>
  <div class="drawer" id="drawer" hidden>
    <div class="wrap">
      <ul>{drawer}</ul>
      <div class="drawer-cta"><a class="btn btn-ink" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a></div>
      <p class="label">Vardagar 15–19 · Helger 9–19</p>
    </div>
  </div>
</header>'''


def footer(home, cta=True):
    end = f'''<section class="end"><div class="wrap">
  <p class="label">Boka</p>
  <h2>Redo att få cykeln fixad?</h2>
  <p class="end-lead">Boka en tid och få vardagen att rulla igen. Vi kommer till dig – vardagar 15–19, helger 9–19.</p>
  <div class="end-cta"><a class="btn btn-lime" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-line-light" href="tel:{TEL}">Ring {PHONE}</a></div>
</div></section>''' if cta else ""
    return f'''<div class="dark">
{end}<footer class="foot-wrap"><div class="wrap foot">
  <div class="foot-brand">
    <a class="logo" href="index.html" aria-label="Hemmacykel, till startsidan">{logo(True)}</a>
    <p>Mobil cykelverkstad i Uppsala. Vi kommer hem till dig och fixar cykeln på plats.</p>
  </div>
  <div>
    <h4>Kontakt</h4>
    <ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{STREET}, {ZIP_CITY}</li></ul>
  </div>
  <div>
    <h4>Sidor</h4>
    <ul><li><a href="boka.html">Boka service</a></li><li><a href="{nav_href("tjanster", home)}">Tjänster och priser</a></li>
    <li><a href="{nav_href("omdomen", home)}">Omdömen</a></li><li><a href="cyklar.html">Cyklar till salu</a></li></ul>
  </div>
  <div>
    <h4>Juridiskt</h4>
    <ul><li><a href="integritetspolicy.html">Integritetspolicy</a></li><li><a href="villkor.html">Användarvillkor</a></li><li><a href="cookies.html">Cookie-policy</a></li></ul>
  </div>
  <div class="foot-bot"><p>© 2026 Hemmacykel. Hobbyverksamhet.</p><p><a href="{MAPS}" target="_blank" rel="noopener">{RATING} på Google · {REVIEW_COUNT} omdömen</a></p></div>
</div></footer>
</div>'''


JSONLD_BUSINESS = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Hemmacykel", "url": SITE,
         "logo": f"{SITE}/img/apple-touch-icon.png", "telephone": TEL, "email": MAIL},
        {"@type": "LocalBusiness", "@id": f"{SITE}/#localbusiness", "name": "Hemmacykel – Mobil cykelverkstad Uppsala",
         "image": f"{SITE}/img/og.jpg", "url": SITE, "telephone": TEL, "email": MAIL, "priceRange": "199–899 kr",
         "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Uppsala", "postalCode": "756 53",
                     "addressRegion": "Uppsala län", "addressCountry": "SE"},
         "areaServed": {"@type": "City", "name": "Uppsala"},
         "geo": {"@type": "GeoCoordinates", "latitude": 59.7877839, "longitude": 17.632907},
         "hasMap": MAPS,
         "openingHoursSpecification": [
             {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "15:00", "closes": "19:00"},
             {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "09:00", "closes": "19:00"}]},
        {"@type": "Service", "serviceType": "Mobil cykelservice", "name": "Cykelservice Uppsala – Hemmacykel",
         "provider": {"@id": f"{SITE}/#localbusiness"}, "areaServed": {"@type": "City", "name": "Uppsala"},
         "offers": [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "SEK"} for _, n, p in REPAIRS if p]
         + [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "SEK"} for _, n, p, *_ in PACKAGES]},
    ],
}
JSONLD_FAQ = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'


def page(name, title, desc, body, home=False, head="", cta=True):
    url = SITE + "/" + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f4f3ee">
<meta name="geo.region" content="SE-C"><meta name="geo.placename" content="Uppsala">
<meta property="og:site_name" content="Hemmacykel"><meta property="og:locale" content="sv_SE"><meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&amp;family=Geist+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="assets/site.css">
{head}</head>
<body>
<a class="skip" href="#main">Hoppa till innehållet</a>
{header(home, name)}
<main id="main">
{body}
</main>
{footer(home, cta)}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    (OUT / name).write_text(doc, encoding="utf-8")


def page_head(h1, lead="", crumb=None, extra=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<section class="page-h"><div class="wrap">
  <nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a><span>/</span><span>{e(crumb or h1)}</span></nav>
  <h1>{h1}</h1>
  {lead_html}{extra}
</div></section>'''


def sec_head(label, h2, text=""):
    p = f"<p>{text}</p>" if text else ""
    return f'<header class="sec-h"><p class="label">{label}</p><div><h2>{h2}</h2>{p}</div></header>'


# --- startsidan -----------------------------------------------------------------------
def bike_card(b):
    state = '<span class="state sold">Såld</span>' if b["sold"] else '<span class="state">Till salu</span>'
    return f'''<a class="bc{" is-sold" if b["sold"] else ""}" href="cyklar.html#{b["id"]}">
  <span class="ph"><img src="img/cyklar/{b["images"][0]}" alt="{e(b["title"])}" loading="lazy">{state}</span>
  <span class="bc-row"><span class="bc-t">{e(b["title"])}</span><span class="bc-p">{kr(b["price"])}</span></span>
  <span class="bc-m">{e(b["size"])} · {e(b["condition"])}</span>
</a>'''


def index():
    svc_imgs = "".join(
        f'<img src="img/{img}" alt="" data-for="{v}"{" class=\"on\"" if i == 0 else ""} loading="lazy">'
        for i, (v, _, _, _, img) in enumerate(SERVICES))
    svc_rows = "".join(
        f'<li><a href="boka.html?tjanst={v}" data-svc="{v}"{" class=\"on\"" if i == 0 else ""}><span class="svc-n">{n}</span><span class="svc-d">{d}</span>'
        f'<span class="svc-p">{kr(p) if p else "Prisförslag"}</span>{ico("arrow", "i svc-a")}</a></li>'
        for i, (v, n, d, p, _) in enumerate(SERVICES))

    plans = ""
    for slug, name, price, for_who, items in PACKAGES:
        hl = slug == FEATURED
        plans += f'''<article class="pk-i">
  <div class="pk-top"><h3>{name}</h3>{'<span class="tag">Populärast</span>' if hl else ""}</div>
  <p class="pk-for">{for_who}</p>
  <p class="pk-price">{price}<span>kr</span></p>
  <p class="pk-vat">Fast pris inkl. moms, arbete och material</p>
  <ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul>
  <a class="btn {"btn-ink" if hl else "btn-line"}" href="boka.html?paket={slug}">Boka {name} {ico("arrow")}</a>
</article>'''

    steps = "".join(f'<li><span class="n">Steg {i + 1}</span><h3>{t}</h3><p>{s}</p></li>' for i, (t, s) in enumerate(STEPS))
    big_name, big_text = REVIEWS[0]
    reviews = "".join(
        f'<figure><blockquote>{e(t)}</blockquote><figcaption><b>{e(n)}</b> · Google</figcaption></figure>' for n, t in REVIEWS[1:])
    faq = "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in FAQ)
    bikes = "".join(bike_card(b) for b in BIKES[:3])

    body = f'''<section class="hero"><div class="wrap hero-g">
  <div class="hero-t">
    <h1><span class="pre">Cykelservice i Uppsala</span>Få vardagen att rulla igen.</h1>
    <p class="lead">Vi kommer hem till dig och fixar cykeln där den står. Fasta priser, inga gömda avgifter.</p>
    <div class="hero-cta"><a class="btn btn-ink" href="boka.html">Boka service {ico("arrow")}</a><a class="link" href="tel:{TEL}">eller ring {PHONE}</a></div>
    <dl class="facts">
      <div><dt>{STARS} {RATING}</dt><dd><a href="#omdomen">{REVIEW_COUNT} omdömen på Google</a></dd></div>
      <div><dt>Från 199 kr</dt><dd>Fasta priser inkl. moms</dd></div>
      <div><dt>7 dagar i veckan</dt><dd>Vardagar 15–19, helger 9–19</dd></div>
    </dl>
  </div>
  <figure class="hero-f">
    <img src="img/hemmacykel-hero.jpg" alt="Hemmacykel servar en cykel på plats vid ett cykelställ i Uppsala" width="1170" height="1560" fetchpriority="high">
    <figcaption class="cap"><span>Service på plats</span><span>Uppsala</span></figcaption>
  </figure>
</div></section>

<section class="sec" id="tjanster"><div class="wrap">
  {sec_head("Tjänster och priser", "Fast pris på det vanligaste.", "Du ser alltid priset innan vi börjar. Priserna gäller inklusive moms, arbete och material.")}
  <div class="svc">
    <figure class="svc-fig" aria-hidden="true">{svc_imgs}</figure>
    <ul class="svc-list">{svc_rows}</ul>
    <p class="svc-note">Vi tar både vanliga cyklar och elcyklar. Tillägg: elcykel, lådcykel och andra tyngre cyklar +50 kr, elsparkcykel +100 kr.
    Vid över 15 minuters körtid tillkommer 50 kr i reseavgift, vid över 25 minuter 100 kr.</p>
  </div>
</div></section>

<section class="sec" id="paket"><div class="wrap">
  {sec_head("Servicepaket", "Hela cykeln genomgången, till fast pris.", "Välj rätt nivå direkt och slipp gömda avgifter eller oväntade tillägg.")}
  <div class="pk">{plans}</div>
</div></section>

<section class="sec" id="sa-funkar-det"><div class="wrap">
  {sec_head("Så funkar det", "Från trasig till rullande på tre steg.")}
  <ol class="steps">{steps}</ol>
</div></section>

<section class="sec dark" id="om-oss"><div class="wrap">
  <div class="about">
    <p class="label">Om oss</p>
    <p class="about-q">Vi är två unga entreprenörer från Uppsala. Vi startade Hemmacykel för att ge Uppsalabor mer tid och mindre krångel.</p>
    <figure class="about-img">
      <img src="img/hemmacykel-team.jpg" alt="Grundarna av Hemmacykel vid Ångströmlaboratoriet, Uppsala universitet" loading="lazy" width="1170" height="1560">
      <figcaption class="cap"><span>Grundarna</span><span>Ångströmlaboratoriet, Uppsala</span></figcaption>
    </figure>
    <div class="about-b">
      <p>Cykeln tar dig till jobbet, träningen, kompisarna och familjen. När den går sönder förlorar du tid, frihet och en del av det som får vardagen att fungera.</p>
      <p>Därför ska cykelservice passa din vardag – inte tvärtom. En bokning, en tid som passar dig, och sedan fungerar cykeln igen.</p>
      <dl class="kv">
        <div><dt>Område</dt><dd>Hela Uppsala – Centrum, Luthagen, Flogsta, Sala backe, Gottsunda, Sävja, Årsta, Sunnersta m.fl.</dd></div>
        <div><dt>Tider</dt><dd>Vardagar 15–19, helger 9–19</dd></div>
        <div><dt>Cyklar</dt><dd>Vanliga cyklar, elcyklar, lådcyklar, fatbikes och elsparkcyklar</dd></div>
        <div><dt>Betalning</dt><dd>Swish på plats när jobbet är klart</dd></div>
      </dl>
    </div>
  </div>
</div></section>

<section class="sec" id="omdomen"><div class="wrap">
  <div class="rev">
    <div class="rev-score">
      <p class="label">Omdömen</p>
      <p class="score">{RATING}</p>
      {STARS}
      <p>Snittbetyg från {REVIEW_COUNT} omdömen på Google.</p>
      <a class="link" href="{MAPS}" target="_blank" rel="noopener">Läs alla på Google {ico("arrow-ur")}</a>
    </div>
    <figure class="rev-big">
      <blockquote>”{e(big_text)}”</blockquote>
      <figcaption><b>{e(big_name)}</b> · Google</figcaption>
    </figure>
    <div class="rev-grid">{reviews}</div>
  </div>
</div></section>

<section class="ref-wrap"><div class="wrap ref">
  <p class="label">Tipsa en kompis</p>
  <div class="ref-t"><b>Ge en kompis 100 kr – och få 100 kr själv.</b>
  <p>Efter besöket får du en personlig kod. När en kompis bokar med din kod får hen 100 kr rabatt, och du får 100 kr rabatt på ditt nästa besök.</p></div>
  <a class="link" href="boka.html">Boka med kod {ico("arrow")}</a>
</div></section>

<section class="sec" id="cyklar"><div class="wrap">
  {sec_head("Cyklar till salu", "Begagnat, genomgånget och redo att rulla.", "Vi köper, servar och säljer begagnade cyklar i Uppsala. Alla cyklar är genomgångna av oss innan de säljs.")}
  <div class="bc-grid">{bikes}</div>
  <p class="more"><a class="link" href="cyklar.html">Alla cyklar {ico("arrow")}</a></p>
</div></section>

<section class="sec" id="fragor"><div class="wrap">
  {sec_head("Vanliga frågor", "Frågor och svar.", f'Hittar du inte svaret? Ring <a href="tel:{TEL}">{PHONE}</a> eller mejla <a href="mailto:{MAIL}">{MAIL}</a>.')}
  <div class="qa">{faq}</div>
</div></section>'''
    page("index.html", "Cykelservice Uppsala – Mobil cykelverkstad | Hemmacykel",
         "Mobil cykelservice i Uppsala. Vi kommer hem till dig och fixar cykeln på plats – punktering, däckbyte, bromsar, kedja och service. Fasta priser, inga gömda avgifter.",
         body, home=True, head=ld(JSONLD_BUSINESS) + "\n" + ld(JSONLD_FAQ) + "\n")


# --- boka ------------------------------------------------------------------------------
def boka():
    def opt(v, name, price, small=""):
        pr = kr(price) if price else "Prisförslag"
        sm = f"<small>{e(small)}</small>" if small else ""
        return (f'<label class="opt"><input type="checkbox" name="svc" value="{v}" data-name="{e(name)}" data-price="{price}">'
                f'<span class="box">{ico("check")}</span><span class="nm">{e(name)}{sm}</span><span class="pr">{pr}</span></label>')

    repairs = "".join(opt(v, n, p) for v, n, p in REPAIRS)
    pkgs = "".join(opt(v, n if v != "flera-cyklar" else "Flera cyklar (2 st)", p, f) for v, n, p, f, _ in PACKAGES)
    types = "".join(
        f'<label class="chip"><input type="radio" name="typ" value="{v}" data-name="{e(n)}" data-add="{a}"{" checked" if not i else ""}>'
        f'<span>{e(n)}{f" <em>+{a} kr</em>" if a else ""}</span></label>' for i, (v, n, a) in enumerate(BIKE_TYPES))

    body = page_head("Boka service", "Tre korta steg. Vi bekräftar tid och pris via telefon eller e-post innan vi kommer.") + f'''
<section class="wrap booking">
  <form id="booking" class="bk-form" novalidate data-mail="{MAIL}">
    <ol class="bk-steps"><li class="on"><span>Steg 1</span>Tjänst</li><li><span>Steg 2</span>Tid och plats</li><li><span>Steg 3</span>Kontakt</li></ol>
    <noscript><p class="bk-err">Bokningen kräver JavaScript. Ring oss på {PHONE} eller mejla {MAIL} så bokar vi åt dig.</p></noscript>

    <fieldset class="bk-step" data-step="0">
      <legend>Vad vill du ha hjälp med?</legend>
      <p class="hint">Välj en eller flera.</p>
      <h3 class="bk-h">Reparationer</h3>
      <div class="opts">{repairs}</div>
      <h3 class="bk-h">Servicepaket</h3>
      <div class="opts">{pkgs}</div>
      <h3 class="bk-h">Typ av cykel</h3>
      <div class="chips">{types}</div>
      <label class="fld"><span>Beskriv problemet <small>(valfritt)</small></span><textarea name="beskrivning" rows="2" placeholder="T.ex. bakdäcket tappar luft och växlarna hoppar."></textarea></label>
    </fieldset>

    <fieldset class="bk-step" data-step="1" hidden>
      <legend>Var och när?</legend>
      <p class="hint">Vardagar är vi ute 15–19, helger 9–19.</p>
      <div class="week" id="week"></div>
      <label class="check-line"><input type="checkbox" name="foreslag"> <span>Jag vet inte, föreslå en tid åt mig</span></label>
      <label class="fld"><span>Var står cykeln?</span><input name="adress" autocomplete="street-address" placeholder="Gatuadress, Uppsala" required></label>
    </fieldset>

    <fieldset class="bk-step" data-step="2" hidden>
      <legend>Dina uppgifter</legend>
      <p class="hint">Vi återkommer via e-post eller telefon för att bekräfta tid och pris.</p>
      <div class="fld-grid">
        <label class="fld"><span>Namn</span><input name="namn" autocomplete="name" required></label>
        <label class="fld"><span>Telefon</span><input name="telefon" type="tel" autocomplete="tel" inputmode="tel" required></label>
        <label class="fld"><span>E-post</span><input name="epost" type="email" autocomplete="email" required></label>
        <label class="fld"><span>Rabattkod <small>(valfritt)</small></span><input name="kod" autocomplete="off"></label>
      </div>
      <label class="check-line"><input type="checkbox" name="inga_erbjudanden"> <span>Jag vill inte få erbjudanden om liknande tjänster via e-post.</span></label>
      <label class="check-line"><input type="checkbox" name="villkor" required> <span>Jag har läst <a href="villkor.html" target="_blank">användarvillkoren</a> och <a href="integritetspolicy.html" target="_blank">integritetspolicyn</a>.</span></label>
    </fieldset>

    <p class="bk-err" role="alert" aria-live="assertive"></p>
    <div class="bk-nav">
      <button type="button" class="btn btn-line" data-go="-1" hidden>{ico("left")}Tillbaka</button>
      <button type="button" class="btn btn-ink" data-go="1">Fortsätt {ico("arrow")}</button>
      <button type="submit" class="btn btn-lime" hidden>Skicka bokningsförfrågan {ico("arrow")}</button>
    </div>

    <div class="bk-done" hidden tabindex="-1">
      <p class="label">Nästan klart</p>
      <h2>Tack! Nu öppnas ditt mejlprogram.</h2>
      <p>Skicka mejlet så är din bokningsförfrågan hos oss. Vi återkommer via e-post eller telefon för att bekräfta tid och pris.</p>
      <p>Öppnades inget mejl? Ring oss på <a href="tel:{TEL}">{PHONE}</a> eller skicka uppgifterna nedan till <a href="mailto:{MAIL}">{MAIL}</a>.</p>
      <pre class="bk-copy"></pre>
    </div>
  </form>

  <aside class="bk-sum" aria-live="polite">
    <p class="label">Din bokning</p>
    <ul class="sum-list" id="sum-list"><li class="empty">Inget valt ännu</li></ul>
    <div class="sum-meta" id="sum-meta"></div>
    <div class="sum-total"><span>Uppskattat pris</span><b id="sum-total">–</b></div>
    <p class="sum-note">Inga gömda avgifter. Vid över 15 minuters körtid tillkommer 50 kr i reseavgift, vid över 25 minuter 100 kr. Vi bekräftar alltid priset innan vi börjar.</p>
    <a class="sum-call" href="tel:{TEL}">Föredrar du att ringa?<b>{PHONE}</b></a>
  </aside>
</section>'''
    page("boka.html", "Boka cykelservice i Uppsala | Hemmacykel",
         "Boka mobil cykelservice i Uppsala på någon minut. Välj tjänst, tid och adress – vi kommer hem till dig.", body, cta=False)


# --- cyklar ----------------------------------------------------------------------------
def cyklar():
    cards = ""
    for b in BIKES:
        imgs = "".join(f'<img src="img/cyklar/{f}" alt="{e(b["title"])}, bild {i + 1}" loading="lazy">' for i, f in enumerate(b["images"]))
        lists = ""
        if b["done"]:
            lists += '<h3 class="lh">Nyligen utfört</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in b["done"]) + "</ul>"
        if b["equipment"]:
            lists += '<h3 class="lh">Utrustning</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in b["equipment"]) + "</ul>"
        if b["note"]:
            lists += f'<p class="bnote">{e(b["note"])}</p>'
        if b["sold"]:
            foot = '<p class="bike-f muted">Såld. Nya cyklar läggs upp löpande.</p>'
        else:
            foot = (f'<div class="bike-f"><a class="btn btn-ink btn-sm" href="tel:{TEL}">Ring och köp</a>'
                    f'<a class="btn btn-line btn-sm" href="mailto:{MAIL}?subject={quote("Intresserad av " + b["title"])}">Mejla om cykeln</a></div>')
        state = '<span class="state sold">Såld</span>' if b["sold"] else '<span class="state">Till salu</span>'
        cards += f'''<article class="bike{" is-sold" if b["sold"] else ""}" id="{b["id"]}">
  <div class="gal" data-car>
    <div class="gal-track" data-track tabindex="0" aria-label="Bilder på {e(b["title"])}">{imgs}</div>
    {state}
    <button type="button" class="gal-btn prev" data-prev aria-label="Föregående bild">{ico("left")}</button>
    <button type="button" class="gal-btn next" data-next aria-label="Nästa bild">{ico("right")}</button>
    <span class="gal-count" data-count>1 / {len(b["images"])}</span>
  </div>
  <div class="bike-b">
    <div class="bike-top"><h2>{e(b["title"])}</h2><span class="bike-p">{kr(b["price"])}</span></div>
    <p class="meta">{e(b["brand"])} · {e(b["size"])} · {e(b["condition"])} · {e(b["location"])}</p>
    <p class="intro">{e(b["intro"])}</p>
    <details class="bike-more"><summary>Vad som är gjort<span class="pm" aria-hidden="true"></span></summary>{lists}</details>
    {foot}
  </div>
</article>'''
    body = page_head("Cyklar till salu",
                     "Vi köper, servar och säljer begagnade cyklar i Uppsala. Alla cyklar är genomgångna av oss innan de säljs. "
                     "Hämtas i Uppsala – provkör gärna innan du köper.") + f'''
<section class="wrap">
  <div class="bikes">{cards}</div>
  <div class="sell">
    <p class="label">Inget som passar?</p>
    <div><h2>Letar du efter något specifikt – eller vill du sälja din cykel?</h2>
    <p>Vi köper begagnade cyklar och har ofta fler på gång än det som syns här. Hör av dig så berättar vi vad vi har.</p>
    <p class="sell-cta"><a class="btn btn-ink" href="tel:{TEL}">Ring {PHONE}</a><a class="btn btn-line" href="mailto:{MAIL}">Mejla oss</a></p></div>
  </div>
  <p class="fine">Cyklarna säljs som privatköp. Du har möjlighet att inspektera och provköra cykeln innan köpet genomförs. Läs mer i <a href="villkor.html">användarvillkoren</a>.</p>
</section>'''
    page("cyklar.html", "Begagnade cyklar till salu i Uppsala | Hemmacykel",
         "Servade begagnade cyklar till salu i Uppsala. Alla cyklar är genomgångna av Hemmacykel innan de säljs.", body)


# --- juridik ---------------------------------------------------------------------------
CONTACT_BLOCK = f"<p>Hemmacykel<br>{STREET}, {ZIP_CITY}<br>E-post: <a href=\"mailto:{MAIL}\">{MAIL}</a><br>Telefon: <a href=\"tel:{TEL}\">{PHONE}</a></p>"

LEGAL = {
    "integritetspolicy.html": ("Integritetspolicy", "Så behandlar Hemmacykel dina personuppgifter.", f'''
<p>Hemmacykel (”vi”, ”oss”) värnar om din personliga integritet. Denna policy beskriver hur vi samlar in och behandlar personuppgifter när du bokar en tjänst eller köper en cykel via vår hemsida.</p>
<h2>Personuppgiftsansvarig</h2>{CONTACT_BLOCK}
<h2>Vilka uppgifter vi samlar in</h2>
<ul><li>Namn, telefonnummer och e-postadress</li><li>Adress (för att kunna komma hem till dig)</li><li>Information om din cykel, din problembeskrivning och bilder du väljer att ladda upp</li><li>Bokningsdatum och vald tid</li></ul>
<h2>Ändamål och rättslig grund</h2>
<p>Uppgifterna behandlas för att kunna fullgöra avtalet med dig (utföra cykelservice eller leverera cykel) samt för att kontakta dig om bokningen. Den rättsliga grunden är avtal (GDPR art. 6.1.b) och i vissa fall berättigat intresse för att kunna driva verksamheten. Google Ads-mätning sker endast med ditt samtycke (GDPR art. 6.1.a).</p>
<p>Som kund kan du få erbjudanden om våra egna, liknande tjänster till den e-postadress du angav vid bokningen, enligt 19 § marknadsföringslagen och vårt berättigade intresse (GDPR art. 6.1.f). Du kan tacka nej redan vid bokningen och när som helst därefter genom att mejla <a href="mailto:{MAIL}">{MAIL}</a> eller svara på ett erbjudande.</p>
<h2>AI-baserad felsökning</h2>
<p>Om du använder vår AI-analys behandlas text och bilder som du själv skickar för att föreslå lämplig service och ett uppskattat pris. Undvik att skicka bilder som visar personer eller annan information som inte behövs för felsökningen. AI-svaren är förslag som bekräftas av oss innan arbetet börjar.</p>
<h2>Lagringstid</h2>
<p>Bokningsuppgifter, uppladdade bilder och AI-uppskattningar sparas så länge de behövs för att hantera ärendet. Uppgifter som måste bevaras för bokföring sparas i upp till 7 år enligt bokföringslagen. Övriga uppgifter raderas när de inte längre behövs eller efter en godkänd begäran om radering.</p>
<h2>Mottagare</h2>
<p>Vi använder tekniska underleverantörer för webbplats, databas och fillagring, e-postutskick, kalenderbokningar, adressökning och avståndsberäkning samt AI-analys av text och bilder. Det omfattar Lovable, Supabase, Resend, Google (Calendar, Maps, Places och Ads) och OpenAI via Lovables AI-tjänst. De får bara behandla de uppgifter som behövs för respektive funktion. Vissa leverantörer kan behandla uppgifter utanför EU/EES med tillämpliga skyddsåtgärder.</p>
<h2>Dina rättigheter</h2>
<p>Du har rätt att begära registerutdrag, rättelse, radering eller begränsning av behandlingen av dina personuppgifter. Kontakta oss på <a href="mailto:{MAIL}">{MAIL}</a>. Du kan även lämna klagomål till Integritetsskyddsmyndigheten (IMY).</p>
<h2>Cookies</h2>
<p>Hemsidan använder nödvändig lokal lagring. Google Ads-mätning aktiveras endast om du godkänner den. Se vår <a href="cookies.html">cookie-policy</a>.</p>'''),
    "villkor.html": ("Användarvillkor", "Villkor för bokning av mobil cykelservice och köp av cykel hos Hemmacykel.", f'''
<p>Dessa villkor gäller mellan dig som kund och Hemmacykel när du bokar mobil cykelservice eller köper en cykel via vår hemsida.</p>
<h2>Om oss</h2>{CONTACT_BLOCK}
<h2>Bokning av cykelservice</h2>
<p>När du gör en bokning på hemsidan är detta en preliminär förfrågan. Vi återkommer via e-post eller telefon för att bekräfta tid och pris. Avtal mellan dig och Hemmacykel uppstår när vi bekräftat bokningen.</p>
<h2>Priser och betalning</h2>
<p>Priserna på hemsidan är angivna i svenska kronor (SEK) inklusive moms, arbete och material om inget annat tydligt anges. Ett AI-estimerat pris är en uppskattning och kan skilja sig från slutpriset; eventuella ändringar stäms av innan arbetet utförs. Betalning sker på plats efter utfört arbete via Swish, om inget annat överenskommits. Kvitto erbjuds alltid och lämnas på begäran.</p>
<p>Elcykel, lådcykel och andra tyngre cyklar kostar 50 kr extra. För elsparkcykel tillkommer 100 kr. Vid över 15 minuters körtid tillkommer 50 kr i reseavgift, vid över 25 minuter 100 kr. Tilläggen visas i det uppskattade totalpriset när uppgifterna finns tillgängliga.</p>
<h2>Ångerrätt – tjänster</h2>
<p>Som konsument har du enligt distansavtalslagen 14 dagars ångerrätt. Om du begär att vi ska börja utföra tjänsten innan ångerfristen löpt ut förlorar du ångerrätten när tjänsten är fullt utförd. Påbörjad men ej slutförd tjänst kan du behöva betala för i proportion till utfört arbete.</p>
<h2>Ångerrätt – köp av cykel</h2>
<p>Cyklarna som säljs via hemsidan säljs som privatköp mellan privatpersoner. Vid privatköp gäller inte konsumentköplagen och därmed finns ingen ångerrätt. Du har möjlighet att inspektera och provköra cykeln innan köpet genomförs, och köpet är bindande när betalning skett.</p>
<h2>Reklamation</h2>
<p>Som konsument har du 3 års reklamationsrätt enligt konsumentköplagen respektive konsumenttjänstlagen. Reklamation ska göras inom skälig tid, senast två månader efter att felet upptäcktes. Kontakta oss på <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Avbokning</h2>
<p>Avbokning av servicebesök ska göras senast 24 timmar innan bokad tid. Vid sen avbokning eller utebliven tid kan en avgift tas ut.</p>
<h2>Ansvar</h2>
<p>Vi ansvarar för det arbete vi utför enligt gällande konsumentlagstiftning. Vi ansvarar inte för fel som beror på normalt slitage, felaktig användning eller skada som uppkommit efter utfört arbete.</p>
<h2>Tvist</h2>
<p>Vid tvist försöker vi alltid hitta en lösning. Du har rätt att vända dig till Allmänna reklamationsnämnden (ARN) eller EU:s plattform för tvistlösning online (ec.europa.eu/consumers/odr).</p>
<h2>Ändringar</h2>
<p>Vi förbehåller oss rätten att uppdatera dessa villkor. Den senaste versionen finns alltid publicerad på hemsidan.</p>'''),
    "cookies.html": ("Cookie-policy", "Så använder Hemmacykel cookies och lokal lagring.", f'''
<p>Hemmacykel använder nödvändig lokal lagring för att webbplatsen ska fungera. Med ditt godkännande använder vi även Google Ads för att mäta vilka annonser som leder till bokningar. Google Ads laddas inte innan du har godkänt detta.</p>
<h2>Vad är en cookie?</h2>
<p>En cookie är en liten textfil som sparas i din webbläsare när du besöker en hemsida. Den används bland annat för att komma ihåg dina inställningar och hålla dig inloggad.</p>
<h2>Nödvändig lagring</h2>
<ul><li>Sessionscookies för att hålla dig inloggad om du är administratör.</li><li>Tillfällig lagring i webbläsaren för att föra val från chatten till bokningen och återställa sidan vid tekniska anslutningsfel.</li><li>Ditt val om mätning sparas i webbläsaren så att vi kan respektera det vid nästa besök.</li></ul>
<h2>Valfri mätning med Google Ads</h2>
<p>Om du väljer Godkänn laddas Google Ads och en konvertering kan registreras när en bokning skickas. Syftet är att mäta annonsernas resultat. Uppgifter kan då delas med Google och behandlas utanför EU/EES med tillämpliga skyddsåtgärder. Du kan återkalla ditt val genom att rensa webbplatsens lagrade data i webbläsaren.</p>
<h2>Hantera cookies</h2>
<p>Du kan när som helst rensa eller blockera cookies i din webbläsares inställningar. Observera att vissa delar av hemsidan då kan sluta fungera.</p>
<h2>Kontakt</h2>
<p>Frågor om vår cookie-användning? Mejla oss på <a href="mailto:{MAIL}">{MAIL}</a>.</p>'''),
}


def legal():
    for name, (h1, desc, content) in LEGAL.items():
        nav = "".join(f'<li><a href="{n}"{" aria-current=\"page\"" if n == name else ""}>{t}</a></li>' for n, (t, *_) in LEGAL.items())
        body = page_head(h1, crumb=h1) + f'''
<section class="wrap legal">
  <nav class="legal-nav" aria-label="Juridiskt"><p class="label">Juridiskt</p><ul>{nav}</ul></nav>
  <article class="prose">{content}
  <p class="updated">Senast uppdaterad {UPDATED}</p></article>
</section>'''
        page(name, f"{h1} | Hemmacykel", desc, body)


def not_found():
    body = page_head("Sidan finns inte", "Länken kan vara gammal eller felstavad.", "404",
                     f'<p class="hero-cta"><a class="btn btn-ink" href="index.html">Till startsidan {ico("arrow")}</a><a class="link" href="boka.html">Boka service</a></p>')
    page("404.html", "Sidan finns inte | Hemmacykel", "Sidan kunde inte hittas.", body)


def sitemap():
    pages = ["", "boka.html", "cyklar.html", "integritetspolicy.html", "villkor.html", "cookies.html"]
    urls = "".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>" for p in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    index()
    boka()
    cyklar()
    legal()
    not_found()
    sitemap()
    print("Klart:", ", ".join(sorted(p.name for p in OUT.glob("*.html"))))
