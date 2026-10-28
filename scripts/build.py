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
RATING, REVIEW_COUNT = "5.0", 13
HOURS = [("Vardagar", "15–19"), ("Lördag–söndag", "9–19")]
UPDATED = "2026-10-28"

e = html.escape

# --- ikoner (Lucide, MIT) -------------------------------------------------------------
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "house": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "tag": '<path d="M12 2H2v10l9.29 9.29a2.41 2.41 0 0 0 3.42 0l6.58-6.58a2.41 2.41 0 0 0 0-3.42L12 2Z"/><path d="M7 7h.01"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-ur": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "bike": '<circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C9.5 3 12 5.5 12 8c0-2.5 2.5-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "swish": '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>',
    "star": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
}


def ico(name, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


GOOGLE = ('<svg class="g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.6-.4-3.9z"/>'
          '<path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
          '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
          '<path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.9z"/></svg>')

STARS = '<span class="stars" aria-hidden="true">' + "".join(
    f'<svg viewBox="0 0 24 24"><path d="{ICONS["star"][9:-3]}"/></svg>' for _ in range(5)) + "</span>"


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

TILES = [  # (länk, rubrik, text, bild, pris, bildposition)
    ("boka.html?tjanst=punktering", "Punktering", "Vi lagar eller byter slang snabbt på plats.", "tjanst-punktering.jpg", "299 kr", "50% 50%"),
    ("boka.html?tjanst=dackbyte", "Däckbyte", "Byte av däck på plats, fram eller bak.", "tjanst-dack.jpg", "349 kr", "50% 50%"),
    ("boka.html?tjanst=kedjebyte", "Kedjebyte", "Byte och service av kedja.", "tjanst-kedja.jpg", "299 kr", "50% 50%"),
    ("boka.html?tjanst=bromsjustering", "Bromsar", "Justering och byte av bromsar, vajrar och klossar.", "tjanst-bromsar.jpg", "från 199 kr", "50% 40%"),
    ("boka.html?paket=cykelcheck", "Service", "Genomgång och säkerhetskontroll av hela cykeln.", "tjanst-service.jpg", "från 499 kr", "50% 50%"),
    ("boka.html?tjanst=ovrigt", "Övrigt", "Har du något annat problem? Kontakta oss för prisförslag.", "tjanst-ovrigt.jpg", "Prisförslag", "50% 50%"),
    ("cyklar.html", "Begagnade cyklar", "Vi köper, servar och säljer begagnade cyklar.", "tjanst-begagnat.jpg", "Se cyklar till salu", "50% 60%"),
]

USPS = [
    ("house", "Vi kommer hem till dig", "Vi tar med allt vi behöver och fixar cykeln där den står."),
    ("tag", "Inga gömda avgifter", "Du ser priset innan vi börjar. Inga överraskningar."),
    ("zap", "Snabb service", "Boka på någon minut. Vi är ute både vardagar och helger."),
    ("shield", "Nöjd-kund-garanti", "Vi står bakom jobbet vi gör – med 3 års reklamationsrätt."),
]

REVIEWS = [  # (namn, text) – från Google, oktober 2026
    ("Malin Härenstam", "Snabb och kompetent service som kommer hem till dig! Och dessutom väldigt bra priser."),
    ("Rebecka Astenvald", "Professionellt, snabb service, och bra pris! Väldigt nöjd och skulle anlita igen, kan varmt rekommendera."),
    ("Sofia Ribeiro", "Trevlig och superbra kille, fixade cykeln snabbt och det blev jättebra! Fantastiskt nöjd! ❤️🙏"),
    ("Johan", "Kan varmt rekommendera! Proffsigt och prisvärt!"),
    ("Tristan Johansson", "Bra jobb och väldigt prisvärt med tanke på att dom kommer hem till en"),
    ("Olof", "Snabbt, enkelt, billigt och mycket trevliga att ha att göra med."),
    ("Ella Hellberg", "Smidigt, prisvärt, rekommenderar starkt!"),
]

AREAS = ["Centrum", "Luthagen", "Flogsta", "Sala backe", "Gottsunda", "Sävja", "Årsta", "Sunnersta"]

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
NAV = [("tjanster", "Tjänster"), ("priser", "Priser"), ("sa-funkar-det", "Så funkar det"),
       ("omdomen", "Omdömen"), ("om-oss", "Om oss")]


def logo(light=False):
    mark = "logo-mark-vit.png" if light else "logo-mark.png"
    return (f'<img src="img/{mark}" alt="" width="46" height="40">'
            '<span class="wm"><b>HEMMACYKEL</b><small>Mobil cykelverkstad</small></span>')


def nav_href(anchor, home):
    return f"#{anchor}" if home else f"index.html#{anchor}"


def header(home, current):
    links = "".join(f'<a href="{nav_href(a, home)}">{t}</a>' for a, t in NAV)
    links += f'<a href="cyklar.html"{" aria-current=\"page\"" if current == "cyklar.html" else ""}>Cyklar till salu</a>'
    drawer = "".join(f'<li><a href="{nav_href(a, home)}">{t}</a></li>' for a, t in NAV)
    drawer += '<li><a href="cyklar.html">Cyklar till salu</a></li>'
    return f'''<div class="topbar"><div class="in">
  <p class="tb-l"><span>{ico("pin")}Mobil cykelverkstad i Uppsala</span><span>{ico("clock")}Vardagar 15–19 · Helger 9–19</span></p>
  <p class="tb-r"><a href="{nav_href("omdomen", home)}" class="tb-rating">{STARS}<b>{RATING}</b> på Google</a><a class="hide-m" href="mailto:{MAIL}">{ico("mail")}{MAIL}</a><a href="tel:{TEL}">{ico("phone")}{PHONE}</a></p>
</div></div>
<header class="site-h">
  <div class="in nav">
    <a class="logo" href="index.html" aria-label="Hemmacykel, till startsidan">{logo()}</a>
    <nav class="mainnav" aria-label="Huvudmeny">{links}</nav>
    <div class="nav-cta">
      <a class="nav-tel" href="tel:{TEL}">{ico("phone")}<span>{PHONE}</span></a>
      <a class="btn btn-f btn-sm" href="boka.html">Boka service</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Meny">{ico("menu", "i i-open")}{ico("x", "i i-close")}</button>
    </div>
  </div>
  <div class="drawer" id="drawer" hidden>
    <div class="in">
      <ul>{drawer}</ul>
      <div class="drawer-cta"><a class="btn btn-f" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">{ico("phone")}{PHONE}</a></div>
      <p class="drawer-meta">{ico("clock")}Vardagar 15–19 · Helger 9–19</p>
    </div>
  </div>
</header>'''


def footer(home):
    svc = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, *_ in TILES[:6])
    return f'''<footer class="foot">
  <div class="in foot-top">
    <div class="foot-brand">
      <a class="logo logo-light" href="index.html" aria-label="Hemmacykel, till startsidan">{logo(True)}</a>
      <p><b class="foot-slogan">Få vardagen att rulla igen.</b>Mobil cykelverkstad i Uppsala. Vi kommer hem till dig och fixar cykeln på plats – utan gömda avgifter.</p>
      <a class="foot-rating" href="{MAPS}" target="_blank" rel="noopener">{GOOGLE}{STARS}<span><b>{RATING}</b> · {REVIEW_COUNT} omdömen</span></a>
    </div>
    <div>
      <h4>Tjänster</h4>
      <ul>{svc}</ul>
    </div>
    <div>
      <h4>Hemmacykel</h4>
      <ul>
        <li><a href="boka.html">Boka service</a></li>
        <li><a href="{nav_href("priser", home)}">Prislista</a></li>
        <li><a href="{nav_href("omdomen", home)}">Omdömen</a></li>
        <li><a href="{nav_href("om-oss", home)}">Om oss</a></li>
        <li><a href="cyklar.html">Cyklar till salu</a></li>
        <li><a href="{nav_href("fragor", home)}">Vanliga frågor</a></li>
      </ul>
    </div>
    <div>
      <h4>Kontakt</h4>
      <ul class="foot-contact">
        <li>{ico("phone")}<a href="tel:{TEL}">{PHONE}</a></li>
        <li>{ico("mail")}<a href="mailto:{MAIL}">{MAIL}</a></li>
        <li>{ico("pin")}<span>{STREET}, {ZIP_CITY}<br><small>{AREA}</small></span></li>
        <li>{ico("clock")}<span>Vardagar 15–19<br>Helger 9–19</span></li>
      </ul>
    </div>
  </div>
  <div class="in foot-bot">
    <p>© 2026 Hemmacykel. Alla rättigheter förbehållna. Hobbyverksamhet.</p>
    <p class="foot-legal"><a href="integritetspolicy.html">Integritetspolicy</a><a href="villkor.html">Användarvillkor</a><a href="cookies.html">Cookie-policy</a></p>
  </div>
</footer>'''


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


def page(name, title, desc, body, home=False, head=""):
    url = SITE + "/" + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1b3224">
<meta name="geo.region" content="SE-C"><meta name="geo.placename" content="Uppsala">
<meta property="og:site_name" content="Hemmacykel"><meta property="og:locale" content="sv_SE"><meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&amp;family=Outfit:wght@500;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/site.css">
{head}</head>
<body>
<a class="skip" href="#main">Hoppa till innehållet</a>
{header(home, name)}
<main id="main">
{body}
</main>
{footer(home)}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    (OUT / name).write_text(doc, encoding="utf-8")


def sub_hero(eyebrow, h1, lead="", crumbs=None, extra=""):
    crumb = f'<nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a><span>/</span>{e(crumbs or h1)}</nav>'
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<section class="sub-hero"><div class="in">
  {crumb}
  <p class="eyebrow eb-light">{eyebrow}</p>
  <h1>{h1}</h1>
  {lead_html}{extra}
</div></section>'''


def cta_band():
    return f'''<section class="cta"><div class="in cta-in">
  <div><h2>Redo att få cykeln fixad?</h2><p>Boka en tid och få vardagen att rulla igen.</p></div>
  <div class="cta-btns"><a class="btn btn-ink" href="boka.html">Boka nu {ico("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">{ico("phone")}{PHONE}</a></div>
</div></section>'''


# --- startsidan -----------------------------------------------------------------------
def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{ico('check')}<span>{e(i)}</span></li>" for i in items) + "</ul>"


def bike_card(b, i):
    badge = '<span class="flag flag-sold">Såld</span>' if b["sold"] else '<span class="flag">Till salu</span>'
    return f'''<a class="bcard rv{" is-sold" if b["sold"] else ""}" href="cyklar.html#{b["id"]}" style="--d:{i * 80}ms">
  <span class="ph"><img src="img/cyklar/{b["images"][0]}" alt="{e(b["title"])}" loading="lazy">{badge}</span>
  <span class="tx"><span class="brand">{e(b["brand"])}</span><b>{e(b["title"])}</b>
  <span class="meta"><span>{e(b["size"])}</span><span>{e(b["condition"])}</span></span>
  <span class="bprice">{kr(b["price"])}{ico("arrow")}</span></span>
</a>'''


def index():
    usps = "".join(f'<li><span class="usp-ico">{ico(i)}</span><span><b>{t}</b><small>{s}</small></span></li>' for i, t, s in USPS)
    tiles = "".join(
        f'<a class="tile rv" href="{h}" style="--d:{(n % 4) * 70}ms"><span class="ph"><img src="img/{img}" alt="" loading="lazy" style="object-position:{pos}"></span>'
        f'<span class="arr">{ico("arrow-ur")}</span><span class="tx"><b>{t}</b><small>{s}</small><em>{p}</em></span></a>'
        for n, (h, t, s, img, p, pos) in enumerate(TILES))
    tiles += (f'<div class="tile tile-dark rv" style="--d:210ms"><span class="usp-ico">{ico("bike")}</span>'
              f'<span class="tx"><b>Elcykel, lådcykel eller fatbike?</b><small>Vi tar både vanliga cyklar och elcyklar – från bromsar och växlar till kedja, '
              f'och vi gör en grundläggande koll på motorn också.</small>'
              f'<a class="more more-light" href="boka.html">Boka service {ico("arrow")}</a></span></div>')

    plans = ""
    for slug, name, price, for_who, items in PACKAGES:
        hl = slug == FEATURED
        plans += f'''<article class="plan rv{" plan-hl" if hl else ""}">
  {'<span class="badge">Populärast</span>' if hl else ""}
  <h3>{name}</h3><p class="for">{for_who}</p>
  <p class="amt">{price}<span>kr</span></p><p class="vat">Fast pris inkl. moms, arbete och material</p>
  {checks(items)}
  <a class="btn {"btn-l" if hl else "btn-f"}" href="boka.html?paket={slug}">Boka {name} {ico("arrow")}</a>
</article>'''

    rows = "".join(f'<div class="prow"><span>{n}</span><i></i><b>{kr(p)}</b></div>' for _, n, p in REPAIRS if p)
    rows += '<div class="prow"><span>Övrigt</span><i></i><b>Prisförslag</b></div>'
    pkg_rows = "".join(f'<div class="prow"><span>{n}</span><i></i><b>{kr(p)}</b></div>' for _, n, p, *_ in PACKAGES)
    add_rows = ('<div class="prow"><span>Elcykel, lådcykel och andra tyngre cyklar</span><i></i><b>+50 kr</b></div>'
                '<div class="prow"><span>Elsparkcykel</span><i></i><b>+100 kr</b></div>'
                '<div class="prow"><span>Reseavgift vid över 15 min körtid</span><i></i><b>+50 kr</b></div>'
                '<div class="prow"><span>Reseavgift vid över 25 min körtid</span><i></i><b>+100 kr</b></div>')

    reviews = "".join(
        f'''<figure class="rv-card">
  <div class="rv-top">{STARS}{GOOGLE}</div>
  <span class="qm" aria-hidden="true">”</span>
  <blockquote>{e(t)}</blockquote>
  <figcaption><span class="av" aria-hidden="true">{"".join(w[0] for w in n.split()[:2])}</span><span><b>{e(n)}</b><small>Omdöme på Google</small></span></figcaption>
</figure>''' for n, t in REVIEWS)

    steps = [("01", "Boka på någon minut", "Välj hjälpen och tiden som passar din vardag."),
             ("02", "Vi fixar den där den står", "Vi kommer hem till dig med allt vi behöver."),
             ("03", "Rulla vidare", "Få tillbaka friheten med en cykel som fungerar igen.")]
    steps_html = "".join(f'<li class="rv" style="--d:{i * 90}ms"><span class="num">{n}</span><h3>{t}</h3><p>{s}</p></li>' for i, (n, t, s) in enumerate(steps))

    faq = "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in FAQ)
    bikes = "".join(bike_card(b, i) for i, b in enumerate(BIKES[:3]))
    areas = "".join(f"<li>{a}</li>" for a in AREAS) + "<li>m.fl.</li>"

    body = f'''<section class="hero">
  <img class="hero-img" src="img/hemmacykel-hero.jpg" alt="Hemmacykel servar en cykel på plats vid ett cykelställ i Uppsala" width="1170" height="1560" fetchpriority="high">
  <div class="in hero-in">
    <p class="eyebrow eb-light">Mobil cykelverkstad · Uppsala</p>
    <h1>Cykelservice i Uppsala. <span>Få vardagen att rulla igen.</span></h1>
    <p class="hero-lead">Vi kommer hem till dig och fixar cykeln där den står. Du slipper släpa den till en verkstad – och behåller tiden och friheten i vardagen.</p>
    <div class="hero-cta"><a class="btn btn-l" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-ghost" href="tel:{TEL}">{ico("phone")}Ring {PHONE}</a></div>
    <a class="g-chip" href="#omdomen">{GOOGLE}{STARS}<span><b>{RATING}</b> · {REVIEW_COUNT} omdömen på Google</span></a>
  </div>
</section>
<section class="usp-wrap" aria-label="Därför Hemmacykel"><div class="in"><ul class="usps">{usps}</ul></div></section>

<section class="sec" id="tjanster"><div class="in">
  <div class="sec-head rv"><div><p class="eyebrow">Tjänster</p><h2>Det här hjälper vi dig med</h2></div><a class="more" href="#priser">Hela prislistan {ico("arrow")}</a></div>
  <div class="tiles">{tiles}</div>
</div></section>

<section class="sec sec-cream" id="om-oss"><div class="in split">
  <figure class="framed rv"><img src="img/hemmacykel-team.jpg" alt="Grundarna av Hemmacykel vid Ångströmlaboratoriet, Uppsala universitet" loading="lazy" width="1170" height="1560"></figure>
  <div class="rv">
    <p class="eyebrow">Om Hemmacykel</p>
    <h2>Två unga entreprenörer från Uppsala</h2>
    <p class="lead">Vi startade Hemmacykel för att ge Uppsalabor mer tid och mindre krångel. En bokning, en tid som passar dig, och sedan fungerar cykeln igen.</p>
    <dl class="stats">
      <div><dt>{RATING}</dt><dd>betyg på Google</dd></div>
      <div><dt>{REVIEW_COUNT}</dt><dd>omdömen</dd></div>
      <div><dt>7</dt><dd>dagar i veckan</dd></div>
    </dl>
    <ul class="minis">
      <li>{ico("clock")}<span><b>Spara tid</b><small>Boka på någon minut</small></span></li>
      <li>{ico("wrench")}<span><b>Vi kommer hem</b><small>Vi tar med allt vi behöver</small></span></li>
      <li>{ico("tag")}<span><b>Full koll</b><small>Inga gömda avgifter</small></span></li>
      <li>{ico("pin")}<span><b>Hela Uppsala</b><small>Centrum, Luthagen, Flogsta m.fl.</small></span></li>
    </ul>
  </div>
</div></section>

<section class="sec" id="paket"><div class="in">
  <div class="sec-head center rv"><p class="eyebrow">Servicepaket</p><h2>Mer trygghet för ett fast pris</h2><p class="lead">Välj rätt nivå direkt och slipp gömda avgifter eller oväntade tillägg.</p></div>
  <div class="plans">{plans}</div>
</div></section>

<section class="band"><img class="band-img" src="img/band-drivlina.jpg" alt="" loading="lazy"><div class="in band-in rv">
  <p class="eyebrow eb-light">Därför Hemmacykel</p>
  <h2>Låt inte en trasig cykel stoppa dig.</h2>
  <p>Cykeln tar dig till jobbet, träningen, kompisarna och familjen. När den går sönder försvinner inte bara möjligheten att cykla. Du förlorar tid, frihet och en del av det som får vardagen att fungera.</p>
  <p><b>Därför ska cykelservice passa din vardag, inte tvärtom.</b> Vi reparerar din cykel direkt hemma hos dig i Uppsala, så att du slipper släpa den till verkstaden, vänta på en ledig tid eller anpassa vardagen efter en reparation.</p>
  <a class="btn btn-l" href="boka.html">Boka service {ico("arrow")}</a>
</div></section>

<section class="sec" id="sa-funkar-det"><div class="in">
  <div class="sec-head rv"><div><p class="eyebrow">Så funkar det</p><h2>Från trasig till rullande på tre steg</h2></div><a class="more" href="boka.html">Boka nu {ico("arrow")}</a></div>
  <ol class="steps">{steps_html}</ol>
  <div class="info-row">
    <div class="info rv"><span class="usp-ico">{ico("clock")}</span><div><h3>När vi är ute</h3>
      <dl class="hours">{"".join(f"<div><dt>{d}</dt><dd>{h}</dd></div>" for d, h in HOURS)}</dl></div></div>
    <div class="info rv" style="--d:90ms"><span class="usp-ico">{ico("pin")}</span><div><h3>Vi täcker hela Uppsala</h3>
      <ul class="areas">{areas}</ul></div></div>
  </div>
</div></section>

<section class="sec sec-cream" id="priser"><div class="in price-split">
  <div class="rv">
    <p class="eyebrow">Prislista</p>
    <h2>Inga gömda avgifter</h2>
    <p class="lead">Du vet vad det kostar innan vi börjar. Priserna gäller i svenska kronor inklusive moms, arbete och material.</p>
    <ul class="fine-list">
      <li>{ico("swish")}<span>Betalning på plats efter utfört arbete via Swish.</span></li>
      <li>{ico("check")}<span>Kvitto erbjuds alltid och lämnas på begäran.</span></li>
      <li>{ico("shield")}<span>3 års reklamationsrätt enligt konsumenttjänstlagen.</span></li>
    </ul>
    <a class="btn btn-f" href="boka.html">Se ditt pris i bokningen {ico("arrow")}</a>
  </div>
  <div class="pricecard rv" style="--d:90ms">
    <h3>Reparationer</h3>{rows}
    <h3>Servicepaket</h3>{pkg_rows}
    <h3>Tillägg</h3>{add_rows}
  </div>
</div></section>

<section class="sec" id="omdomen"><div class="in" data-car>
  <div class="sec-head rv"><div><p class="eyebrow">Omdömen</p><h2>Vad kunderna i Uppsala säger</h2></div>
    <div class="car-nav"><button type="button" data-prev aria-label="Föregående omdöme">{ico("left")}</button><button type="button" data-next aria-label="Nästa omdöme">{ico("right")}</button></div></div>
  <div class="reviews">
    <aside class="rv-sum rv">
      <p class="rv-src">{GOOGLE}Google-omdömen</p>
      <p class="score">{RATING}</p>
      {STARS}
      <p>Baserat på {REVIEW_COUNT} omdömen från kunder i Uppsala.</p>
      <div class="rv-btns"><a class="btn btn-l" href="{MAPS}" target="_blank" rel="noopener">Läs alla omdömen {ico("arrow-ur")}</a>
      <a class="more more-light" href="{MAPS}" target="_blank" rel="noopener">Lämna ett omdöme {ico("arrow")}</a></div>
    </aside>
    <div class="rv-track" data-track tabindex="0" aria-label="Kundomdömen, scrolla i sidled">{reviews}</div>
  </div>
</div></section>

<section class="sec sec-tight"><div class="in"><div class="refer rv">
  <span class="refer-ico">{ico("gift")}</span>
  <div><p class="eyebrow">Tipsa en kompis</p><h2>Ge en kompis 100 kr – och få 100 kr själv</h2>
  <p>Efter besöket får du en personlig kod. När en kompis bokar med din kod får hen 100 kr rabatt, och du får 100 kr rabatt på ditt nästa besök. Har du fått en kod? Skriv in den när du bokar.</p></div>
  <a class="btn btn-f" href="boka.html">Boka med kod {ico("arrow")}</a>
</div></div></section>

<section class="sec sec-cream" id="cyklar"><div class="in">
  <div class="sec-head rv"><div><p class="eyebrow">Begagnade cyklar</p><h2>Servade cyklar, redo att rulla</h2>
    <p class="lead">Vi köper, servar och säljer begagnade cyklar i Uppsala. Alla cyklar är genomgångna av oss innan de säljs.</p></div>
    <a class="more" href="cyklar.html">Alla cyklar {ico("arrow")}</a></div>
  <div class="bike-grid">{bikes}</div>
</div></section>

<section class="sec" id="fragor"><div class="in faq">
  <div class="rv">
    <p class="eyebrow">Vanliga frågor</p>
    <h2>Frågor om cykelservice i Uppsala</h2>
    <p class="lead">Hittar du inte svaret? Ring oss på <a href="tel:{TEL}">{PHONE}</a> eller mejla <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </div>
  <div class="qa rv" style="--d:90ms">{faq}</div>
</div></section>
{cta_band()}'''
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

    body = sub_hero("Boka service", "Boka cykelservice", "Tre korta steg. Vi bekräftar tid och pris via telefon eller e-post innan vi kommer.", "Boka") + f'''
<section class="sec booking-sec"><div class="in booking">
  <form id="booking" class="bk-form" novalidate data-mail="{MAIL}">
    <ol class="bk-steps"><li class="on"><span>Steg 1</span>Tjänst</li><li><span>Steg 2</span>Tid och plats</li><li><span>Steg 3</span>Kontakt</li></ol>
    <noscript><p class="bk-err">Bokningen kräver JavaScript. Ring oss på {PHONE} eller mejla {MAIL} så bokar vi åt dig.</p></noscript>

    <fieldset class="bk-step" data-step="0">
      <legend>Vad vill du ha hjälp med?</legend>
      <p class="hint">Välj en eller flera.</p>
      <h3 class="bk-h">Reparationer</h3>
      <div class="opts">{repairs}</div>
      <h3 class="bk-h">Servicepaket – fast pris</h3>
      <div class="opts opts-1">{pkgs}</div>
      <h3 class="bk-h">Vilken typ av cykel?</h3>
      <div class="chips">{types}</div>
      <label class="fld"><span>Beskriv problemet <small>(valfritt)</small></span><textarea name="beskrivning" rows="3" placeholder="T.ex. bakdäcket tappar luft och växlarna hoppar."></textarea></label>
    </fieldset>

    <fieldset class="bk-step" data-step="1" hidden>
      <legend>Var och när?</legend>
      <p class="hint">Välj en tid som passar. Vardagar är vi ute 15–19, helger 9–19.</p>
      <div class="week" id="week"></div>
      <label class="check-line"><input type="checkbox" name="foreslag"> <span>Jag vet inte, föreslå en tid åt mig</span></label>
      <label class="fld"><span>Var står cykeln? *</span><input name="adress" autocomplete="street-address" placeholder="Gatuadress, Uppsala" required></label>
    </fieldset>

    <fieldset class="bk-step" data-step="2" hidden>
      <legend>Dina uppgifter</legend>
      <p class="hint">Vi återkommer via e-post eller telefon för att bekräfta tid och pris.</p>
      <div class="fld-grid">
        <label class="fld"><span>Namn *</span><input name="namn" autocomplete="name" required></label>
        <label class="fld"><span>Telefon *</span><input name="telefon" type="tel" autocomplete="tel" inputmode="tel" required></label>
        <label class="fld"><span>E-post *</span><input name="epost" type="email" autocomplete="email" required></label>
        <label class="fld"><span>Rabattkod <small>(valfritt)</small></span><input name="kod" autocomplete="off"></label>
      </div>
      <label class="check-line"><input type="checkbox" name="inga_erbjudanden"> <span>Jag vill inte få erbjudanden om liknande tjänster via e-post.</span></label>
      <label class="check-line"><input type="checkbox" name="villkor" required> <span>Jag har läst <a href="villkor.html" target="_blank">användarvillkoren</a> och <a href="integritetspolicy.html" target="_blank">integritetspolicyn</a>. *</span></label>
    </fieldset>

    <p class="bk-err" role="alert" aria-live="assertive"></p>
    <div class="bk-nav">
      <button type="button" class="btn btn-line" data-go="-1" hidden>{ico("left")}Tillbaka</button>
      <button type="button" class="btn btn-f" data-go="1">Fortsätt {ico("arrow")}</button>
      <button type="submit" class="btn btn-l" hidden>Skicka bokningsförfrågan {ico("arrow")}</button>
    </div>

    <div class="bk-done" hidden tabindex="-1">
      <span class="done-ico">{ico("check")}</span>
      <h2>Tack! Nu öppnas ditt mejlprogram.</h2>
      <p>Skicka mejlet så är din bokningsförfrågan hos oss. Vi återkommer via e-post eller telefon för att bekräfta tid och pris.</p>
      <p>Öppnades inget mejl? Ring oss på <a href="tel:{TEL}">{PHONE}</a> eller skicka uppgifterna nedan till <a href="mailto:{MAIL}">{MAIL}</a>.</p>
      <pre class="bk-copy"></pre>
    </div>
  </form>

  <aside class="bk-sum" aria-live="polite">
    <h3>Din bokning</h3>
    <ul class="sum-list" id="sum-list"><li class="empty">Inget valt ännu</li></ul>
    <div class="sum-meta" id="sum-meta"></div>
    <div class="sum-total"><span>Uppskattat pris</span><b id="sum-total">–</b></div>
    <p class="sum-note">Inga gömda avgifter. Vid över 15 minuters körtid tillkommer 50 kr i reseavgift, vid över 25 minuter 100 kr. Vi bekräftar alltid priset innan vi börjar.</p>
    <a class="sum-call" href="tel:{TEL}">{ico("phone")}<span>Föredrar du att ringa?<b>{PHONE}</b></span></a>
  </aside>
</div></section>'''
    page("boka.html", "Boka cykelservice i Uppsala | Hemmacykel",
         "Boka mobil cykelservice i Uppsala på någon minut. Välj tjänst, tid och adress – vi kommer hem till dig.", body)


# --- cyklar ----------------------------------------------------------------------------
def cyklar():
    cards = ""
    for b in BIKES:
        imgs = "".join(f'<img src="img/cyklar/{f}" alt="{e(b["title"])}, bild {i + 1}" loading="lazy">' for i, f in enumerate(b["images"]))
        lists = ""
        if b["done"]:
            lists += f'<h3 class="lh">Nyligen utfört</h3>{checks(b["done"])}'
        if b["equipment"]:
            lists += '<h3 class="lh">Utrustning</h3><ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in b["equipment"]) + "</ul>"
        if b["note"]:
            lists += f'<p class="bnote">{e(b["note"])}</p>'
        if b["sold"]:
            foot = f'<div class="bike-f"><span class="pr pr-sold">{kr(b["price"])}</span><span class="sold-txt">Såld</span></div>'
        else:
            subj = f"Intresserad av {b['title']}"
            foot = (f'<div class="bike-f"><span class="pr">{kr(b["price"])}</span><span class="bike-btns">'
                    f'<a class="btn btn-line btn-sm" href="mailto:{MAIL}?subject={quote(subj)}">{ico("mail")}Mejla</a>'
                    f'<a class="btn btn-f btn-sm" href="tel:{TEL}">{ico("phone")}Ring och köp</a></span></div>')
        flag = '<span class="flag flag-sold">Såld</span>' if b["sold"] else '<span class="flag">Till salu</span>'
        cards += f'''<article class="bike rv{" is-sold" if b["sold"] else ""}" id="{b["id"]}">
  <div class="gal" data-car>
    <div class="gal-track" data-track tabindex="0" aria-label="Bilder på {e(b["title"])}">{imgs}</div>
    {flag}
    <button type="button" class="gal-btn prev" data-prev aria-label="Föregående bild">{ico("left")}</button>
    <button type="button" class="gal-btn next" data-next aria-label="Nästa bild">{ico("right")}</button>
    <span class="gal-count" data-count>1 / {len(b["images"])}</span>
  </div>
  <div class="bike-b">
    <span class="brand">{e(b["brand"])}</span>
    <h2>{e(b["title"])}</h2>
    <p class="meta"><span>Storlek {e(b["size"])}</span><span>{e(b["condition"])}</span><span>{ico("pin")}{e(b["location"])}</span></p>
    <p>{e(b["intro"])}</p>
    <details class="bike-more"><summary>Visa vad som är gjort {ico("right")}</summary>{lists}</details>
    {foot}
  </div>
</article>'''
    extra = (f'<ul class="hero-checks"><li>{ico("check")}Genomservad</li><li>{ico("check")}Hämtas i Uppsala</li>'
             f'<li>{ico("check")}Provkör innan du köper</li></ul>')
    body = sub_hero("Begagnade cyklar", "Servade cyklar, redo att rulla",
                    "Vi köper, servar och säljer begagnade cyklar i Uppsala. Alla cyklar är genomgångna av oss innan de säljs.",
                    "Cyklar till salu", extra) + f'''
<section class="sec"><div class="in">
  <div class="bikes">{cards}</div>
  <div class="sell rv">
    <div><p class="eyebrow">Nya cyklar läggs upp löpande</p><h2>Letar du efter något specifikt – eller vill du sälja din cykel?</h2>
    <p>Vi köper begagnade cyklar och har ofta fler på gång än det som syns här. Hör av dig så berättar vi vad vi har.</p></div>
    <div class="sell-btns"><a class="btn btn-l" href="tel:{TEL}">{ico("phone")}{PHONE}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{ico("mail")}{MAIL}</a></div>
  </div>
  <p class="fine">Cyklarna säljs som privatköp. Du har möjlighet att inspektera och provköra cykeln innan köpet genomförs. Läs mer i <a href="villkor.html">användarvillkoren</a>.</p>
</div></section>
{cta_band()}'''
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
        body = sub_hero("Juridiskt", h1) + f'''
<section class="sec"><div class="in legal">
  <article class="prose">{content}
  <p class="updated">Senast uppdaterad: {UPDATED}</p></article>
  <aside class="legal-nav"><h3>Juridiskt</h3><ul>{"".join(f'<li><a href="{n}"{" aria-current=\"page\"" if n == name else ""}>{t}</a></li>' for n, (t, *_) in LEGAL.items())}</ul>
    <p>Frågor? Mejla <a href="mailto:{MAIL}">{MAIL}</a></p></aside>
</div></section>'''
        page(name, f"{h1} | Hemmacykel", desc, body)


def not_found():
    body = sub_hero("404", "Sidan finns inte", "Länken kan vara gammal eller felstavad. Gå till startsidan eller boka service direkt.", "404",
                    f'<div class="hero-cta"><a class="btn btn-l" href="index.html">Till startsidan {ico("arrow")}</a><a class="btn btn-ghost" href="boka.html">Boka service</a></div>')
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
