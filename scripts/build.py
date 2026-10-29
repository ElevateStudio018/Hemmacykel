"""Genererar docs/*.html för Hemmacykel. Kör: python3 scripts/build.py

Allt innehåll är hämtat från hemmacykel.se (oktober 2026). Cyklarna till salu ligger i
scripts/cyklar.json och bilderna i docs/img/cyklar/. Texterna på tjänstesidorna (tecken, vad som
ingår) är skrivna utifrån sajtens beskrivningar och bör stämmas av med Hemmacykel.
"""
import html
import json
import pathlib
import re
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"

SITE = "https://hemmacykel.se"
PHONE, TEL, MAIL = "070-682 88 45", "+46706828845", "hemmacykel@gmail.com"
STREET, ZIP_CITY, AREA = "Almstigen 30", "756 53 Uppsala", "Södra Sunnersta"
MAPS = "https://maps.google.com/?cid=1143771656914339290"
RATING, REVIEW_COUNT = "5,0", 13
UPDATED = "2026-10-29"

e = html.escape

# --- ikoner (Lucide, MIT) -------------------------------------------------------------
ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-ur": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 8h16"/><path d="M4 16h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
}


def ico(name, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


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

TRAVEL = [("Över 15 minuters körtid", 50), ("Över 25 minuters körtid", 100)]

REVIEWS = [  # (namn, text) – från Google, oktober 2026. Den första visas stort.
    ("Rebecka Astenvald", "Professionellt, snabb service, och bra pris! Väldigt nöjd och skulle anlita igen, kan varmt rekommendera."),
    ("Malin Härenstam", "Snabb och kompetent service som kommer hem till dig! Och dessutom väldigt bra priser."),
    ("Sofia Ribeiro", "Trevlig och superbra kille, fixade cykeln snabbt och det blev jättebra! Fantastiskt nöjd! ❤️🙏"),
    ("Olof", "Snabbt, enkelt, billigt och mycket trevliga att ha att göra med."),
    ("Tristan Johansson", "Bra jobb och väldigt prisvärt med tanke på att dom kommer hem till en"),
    ("Johan", "Kan varmt rekommendera! Proffsigt och prisvärt!"),
    ("Ella Hellberg", "Smidigt, prisvärt, rekommenderar starkt!"),
]
REVIEW_THEMES = [  # (mönster, text) – räknas på omdömena ovan
    (r"pris|billig", "nämner priset"),
    (r"snabb", "nämner hur snabbt det gick"),
    (r"rekommend", "rekommenderar oss rakt ut"),
]

STEPS = [
    ("Boka på någon minut", "Välj hjälpen och tiden som passar din vardag. Vi bekräftar tid och pris via telefon eller e-post."),
    ("Vi fixar den där den står", "Vi kommer hem till dig med allt vi behöver. Du behöver inte lyfta ett finger."),
    ("Rulla vidare", "Betala med Swish när jobbet är klart. Kvitto får du alltid."),
]

AREAS = ["Centrum", "Luthagen", "Flogsta", "Sala backe", "Gottsunda", "Sävja", "Årsta", "Sunnersta"]

VALUES = [
    ("Spara tid", "Boka på någon minut. Ingen transport, ingen väntan på verkstaden."),
    ("Vi kommer hem", "Vi tar med allt vi behöver och fixar cykeln där den står."),
    ("Full koll", "Inga gömda avgifter. Du ser priset innan vi börjar."),
    ("Hela Uppsala", "Centrum, Luthagen, Flogsta, Sala backe och fler stadsdelar."),
]

FAQ_GROUPS = [  # (ankare, rubrik, frågor) – svaren kommer från hemmacykel.se och användarvillkoren
    ("bokning", "Bokning och tider", [
        ("Hur fungerar det?", "Du bokar en tid här på hemsidan, och sedan kommer vi hem till dig med hela verkstaden. Du behöver inte lyfta ett finger."),
        ("När kan ni komma?", "På vardagar är vi ute mellan 15 och 19, och på helgerna mellan 9 och 19. Du väljer en tid som passar dig direkt i bokningen."),
        ("Var i Uppsala kommer ni?", "Hela Uppsala! Centrum, Luthagen, Flogsta, Sala backe, Gottsunda, Sävja, Årsta och fler stadsdelar. Skriv in din adress när du bokar, så ser vi direkt om vi kan komma förbi."),
        ("Behöver jag ta med cykeln någonstans?", "Nej! Du behöver inte ta dig någonstans. Vi kommer hem och fixar cykeln, så du kan använda tiden till annat."),
        ("När är min bokning bekräftad?", "När du bokar på hemsidan skickar du en preliminär förfrågan. Vi återkommer via e-post eller telefon för att bekräfta tid och pris, och bokningen gäller när vi har bekräftat den."),
        ("Kan jag avboka?", "Ja. Avbokning ska göras senast 24 timmar innan bokad tid. Vid sen avbokning eller utebliven tid kan en avgift tas ut."),
    ]),
    ("priser", "Priser och betalning", [
        ("Vad kostar det?", "Det beror på vad du vill ha hjälp med. En punktering ligger på 299 kr, en Cykelcheck på 499 kr och däckbyte på 349 kr. Du ser alltid priset innan vi börjar, så inga överraskningar."),
        ("Tillkommer det några avgifter?", "Inga gömda avgifter. För elcykel, lådcykel och andra tyngre cyklar tillkommer 50 kr, för elsparkcykel 100 kr. Vid över 15 minuters körtid tillkommer 50 kr i reseavgift, vid över 25 minuter 100 kr."),
        ("Hur betalar jag?", "Betalning sker på plats efter utfört arbete via Swish, om inget annat överenskommits. Kvitto erbjuds alltid och lämnas på begäran."),
        ("Hur fungerar rabattkoden?", "Efter besöket får du en personlig kod. När en kompis bokar med din kod får hen 100 kr rabatt, och du får 100 kr rabatt på ditt nästa besök. Har du fått en kod skriver du in den när du bokar."),
    ]),
    ("cyklar", "Cyklar vi servar", [
        ("Kan ni serva elcykel?", "Ja, det går bra! Vi tar både vanliga cyklar och elcyklar, allt från bromsar och växlar till kedja, och vi gör en grundläggande koll på motorn också."),
        ("Vilka cyklar tar ni?", "Vanliga cyklar, elcyklar, lådcyklar, tandemcyklar, trehjulingar och andra specialcyklar, fatbikes och elsparkcyklar."),
        ("Vad händer om ni hittar fler fel?", "Du ser alltid priset innan vi börjar. Eventuella ändringar stäms av med dig innan arbetet utförs."),
    ]),
    ("kop", "Köpa begagnad cykel", [
        ("Är cyklarna servade?", "Ja. Alla cyklar vi säljer är genomgångna av oss innan de säljs. Vad som är gjort på varje cykel står i annonsen."),
        ("Kan jag provköra innan jag köper?", "Ja. Du har möjlighet att inspektera och provköra cykeln innan köpet genomförs."),
        ("Finns det ångerrätt?", "Cyklarna säljs som privatköp. Vid privatköp gäller inte konsumentköplagen och därmed finns ingen ångerrätt. Köpet är bindande när betalning skett."),
        ("Var hämtar jag cykeln?", "Cyklarna hämtas i Uppsala. Var varje cykel finns står i annonsen."),
    ]),
    ("garanti", "Garanti och reklamation", [
        ("Vad händer om något inte blev bra?", f"Som konsument har du 3 års reklamationsrätt enligt konsumenttjänstlagen. Reklamation ska göras inom skälig tid, senast två månader efter att felet upptäcktes. Kontakta oss på {MAIL}."),
        ("Vad gäller vid tvist?", "Vid tvist försöker vi alltid hitta en lösning. Du har rätt att vända dig till Allmänna reklamationsnämnden (ARN)."),
    ]),
]
FAQ = [qa for _, _, qs in FAQ_GROUPS for qa in qs]
SERVICE_FAQ = [FAQ_GROUPS[0][2][1], FAQ_GROUPS[0][2][3], FAQ_GROUPS[1][2][2]]  # visas på tjänstesidorna

SERVICES = [
    dict(slug="punktering", cta="Boka punktering", name="Punktering", short="Vi lagar eller byter slang på plats.", price="299 kr", img="tjanst-punktering.jpg",
         book="tjanst=punktering", h1="Punktering? Vi lagar den där cykeln står.",
         lead="Vi kommer hem till dig och lagar eller byter slangen på plats. Fast pris 299 kr inklusive moms, arbete och material.",
         signs=["Däcket tappar luft på några timmar eller över natten", "Du hör ett pysande ljud från hjulet", "Cykeln känns tung och svajig att styra"],
         includes=["Vi tar loss hjulet och letar upp läckan", "Slangen lagas eller byts, beroende på skadan", "Däcket kontrolleras så att inget vasst sitter kvar", "Hjulet monteras och pumpas till rätt tryck"],
         prices=[("Punktering", 299, "tjanst=punktering")],
         note="Är däcket slitet eller trasigt kan det behöva bytas – däckbyte kostar 349 kr. Eventuella ändringar stäms alltid av med dig innan arbetet utförs."),
    dict(slug="dackbyte", cta="Boka däckbyte", name="Däckbyte", short="Byte av däck på plats, fram eller bak.", price="349 kr", img="tjanst-dack.jpg",
         book="tjanst=dackbyte", h1="Däckbyte hemma hos dig.",
         lead="Slitet, sprucket eller punkterat en gång för mycket? Vi byter däcket på plats. Fast pris 349 kr inklusive moms, arbete och material.",
         signs=["Mönstret är nött eller däcket har blivit blankt", "Det syns sprickor i däckets sidor", "Du får punktering gång på gång på samma hjul"],
         includes=["Hjulet tas loss och det gamla däcket demonteras", "Nytt däck monteras och slangen kontrolleras", "Hjulet sätts tillbaka och pumpas till rätt tryck"],
         prices=[("Däckbyte", 349, "tjanst=dackbyte")],
         note="Vi byter däck på elcyklar, lådcyklar och fatbikes också. För tyngre cyklar tillkommer 50 kr."),
    dict(slug="kedjebyte", cta="Boka kedjebyte", name="Kedjebyte", short="Byte och service av kedja.", price="299 kr", img="tjanst-kedja.jpg",
         book="tjanst=kedjebyte", h1="Ny kedja, tyst och smidig växling.",
         lead="En sliten kedja gör cykeln tung och växlarna oprecisa. Vi byter kedjan på plats för 299 kr inklusive moms, arbete och material.",
         signs=["Kedjan hoppar eller slirar när du trampar hårt", "Kedjan är rostig eller gnisslar", "Växlingen är ojämn trots att växlarna är justerade"],
         includes=["Den gamla kedjan tas bort", "Ny kedja monteras och anpassas till rätt längd", "Kedjan smörjs", "Vi provar att växlarna går rent"],
         prices=[("Kedjebyte", 299, "tjanst=kedjebyte")],
         note="Behöver hela drivlinan ses över passar paketet Hemmaservice (749 kr), där genomgång av drivlina ingår."),
    dict(slug="bromsar", cta="Boka bromsar", name="Bromsar", short="Justering, nya bromsklossar eller ny vajer.", price="från 199 kr", img="tjanst-bromsar.jpg",
         book="tjanst=bromsjustering", h1="Bromsar som tar när du behöver dem.",
         lead="Justering, nya bromsklossar eller ny bromsvajer – på plats hemma hos dig, till fast pris.",
         signs=["Bromshandtaget går nästan ända in till styret", "Bromsarna gnisslar eller tar dåligt", "Bromsklossarna är nedslitna"],
         includes=["Bromsjustering – bromsen ställs in så att den tar jämnt och i rätt läge", "Byte av bromsklossar – nedslitna klossar byts och bromsen justeras", "Byte av bromsvajer – ny vajer monteras och bromsen justeras"],
         prices=[("Bromsjustering", 199, "tjanst=bromsjustering"), ("Byte av bromsklossar", 249, "tjanst=bromsklossar"), ("Byte av bromsvajer", 249, "tjanst=bromsvajer")],
         note="Osäker på vad som behövs? Välj bromsjustering när du bokar och beskriv problemet – vi säger till om något mer behöver göras innan vi börjar."),
    dict(slug="service", cta="Boka service", name="Service och paket", short="Hela cykeln genomgången, till fast pris.", price="från 499 kr", img="tjanst-service.jpg",
         book="paket=cykelcheck", h1="Hela cykeln genomgången, till fast pris.",
         lead="Tre servicepaket. Välj rätt nivå direkt och slipp gömda avgifter eller oväntade tillägg.",
         note="Har ni flera cyklar hemma? Paketet Flera cyklar ger Cykelcheck på två cyklar vid samma hembesök för 899 kr."),
    dict(slug="elcykel", cta="Boka service", name="Elcykel och specialcyklar", short="Elcyklar, lådcyklar, fatbikes och fler.", price="+50 kr", img="band-drivlina.jpg",
         book="tjanst=bromsjustering&typ=elcykel", h1="Service på elcykel och specialcyklar.",
         lead="Vi tar både vanliga cyklar och elcyklar – allt från bromsar och växlar till kedja, och vi gör en grundläggande koll på motorn också.",
         includes=["Alla reparationer och servicepaket går att boka för elcykel och specialcyklar", "Bromsar, växlar, kedja och däck", "En grundläggande koll på motorn på elcyklar"],
         note="Elcykel, lådcykel och andra tyngre cyklar kostar 50 kr extra. För elsparkcykel tillkommer 100 kr. Tillägget syns i priset när du bokar."),
]
SVC = {s["slug"]: s for s in SERVICES}

BIKES = json.loads((ROOT / "scripts" / "cyklar.json").read_text(encoding="utf-8"))
BIKES.sort(key=lambda b: b["sold"])  # cyklar till salu först
for _b in BIKES:
    _b["file"] = f"cykel-{_b['id']}.html"

# --- ramverk --------------------------------------------------------------------------
NAV = [("tjanster.html", "Tjänster"), ("priser.html", "Priser"), ("cyklar.html", "Cyklar till salu"),
       ("omdomen.html", "Omdömen"), ("om-oss.html", "Om oss"), ("kontakt.html", "Kontakt")]


def section_of(name):
    if name.startswith("tjanst"):
        return "tjanster.html"
    if name.startswith("cykel"):
        return "cyklar.html"
    return name


def logo(light=False):
    mark = "logo-mark-vit.png" if light else "logo-mark.png"
    return f'<img src="img/{mark}" alt="" width="34" height="30"><span>Hemmacykel</span>'


def header(name):
    cur = section_of(name)
    ac = lambda h: ' aria-current="page"' if h == cur else ""
    dd = "".join(f'<a href="tjanst-{s["slug"]}.html"><b>{s["name"]}</b><small>{s["price"]}</small></a>' for s in SERVICES)
    links = ""
    for h, t in NAV:
        if h == "tjanster.html":
            links += (f'<div class="dd"><a href="{h}"{ac(h)}>{t}{ico("down", "i dd-i")}</a>'
                      f'<div class="dd-menu">{dd}<a class="dd-all" href="{h}">Alla tjänster {ico("arrow")}</a></div></div>')
        else:
            links += f'<a href="{h}"{ac(h)}>{t}</a>'
    sub = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    drawer = "".join(f'<li><a href="{h}">{t}</a>' + (f'<ul class="sub">{sub}</ul>' if h == "tjanster.html" else "") + "</li>" for h, t in NAV)
    return f'''<header class="site-h">
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="Hemmacykel, till startsidan">{logo()}</a>
    <nav class="mainnav" aria-label="Huvudmeny">{links}</nav>
    <div class="nav-cta">
      <a class="nav-tel" href="tel:{TEL}">{PHONE}</a>
      <a class="btn btn-ink btn-s" href="boka.html">Boka service</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Meny">{ico("menu", "i i-open")}{ico("x", "i i-close")}</button>
    </div>
  </div>
  <div class="drawer" id="drawer" hidden>
    <div class="wrap">
      <ul>{drawer}</ul>
      <div class="drawer-cta"><a class="btn btn-ink" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a></div>
      <p class="muted">Vardagar 15–19 · Helger 9–19</p>
    </div>
  </div>
</header>'''


def footer(cta=True):
    end = f'''<section class="cta"><div class="wrap cta-in">
  <div><h2>Redo att få cykeln fixad?</h2><p>Boka en tid och få vardagen att rulla igen. Vi kommer till dig – vardagar 15–19, helger 9–19.</p></div>
  <div class="btns"><a class="btn btn-lime" href="boka.html">Boka service {ico("arrow")}</a><a class="btn btn-ghost" href="tel:{TEL}">Ring {PHONE}</a></div>
</div></section>''' if cta else ""
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    return f'''{end}
<footer class="foot"><div class="wrap">
  <div class="foot-top">
    <div class="foot-brand">
      <a class="logo" href="index.html" aria-label="Hemmacykel, till startsidan">{logo()}</a>
      <p>Mobil cykelverkstad i Uppsala. Vi kommer hem till dig och fixar cykeln på plats.</p>
      <a class="foot-rate" href="omdomen.html"><span class="st">★★★★★</span> {RATING} på Google · {REVIEW_COUNT} omdömen</a>
    </div>
    <div><h4>Tjänster</h4><ul>{svc}</ul></div>
    <div><h4>Hemmacykel</h4><ul><li><a href="boka.html">Boka service</a></li><li><a href="priser.html">Priser</a></li><li><a href="cyklar.html">Cyklar till salu</a></li>
      <li><a href="omdomen.html">Omdömen</a></li><li><a href="om-oss.html">Om oss</a></li><li><a href="fragor.html">Vanliga frågor</a></li></ul></div>
    <div><h4>Kontakt</h4><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{STREET}, {ZIP_CITY}</li><li>Vardagar 15–19, helger 9–19</li><li><a href="kontakt.html">Kontaktsida</a></li></ul></div>
  </div>
  <div class="foot-bot"><p>© 2026 Hemmacykel. Alla rättigheter förbehållna. Hobbyverksamhet.</p>
    <p class="foot-legal"><a href="integritetspolicy.html">Integritetspolicy</a><a href="villkor.html">Användarvillkor</a><a href="cookies.html">Cookie-policy</a></p></div>
</div></footer>'''


BUSINESS = {"@type": "LocalBusiness", "@id": f"{SITE}/#localbusiness", "name": "Hemmacykel – Mobil cykelverkstad Uppsala",
            "image": f"{SITE}/img/og.jpg", "url": SITE, "telephone": TEL, "email": MAIL, "priceRange": "199–899 kr",
            "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Uppsala", "postalCode": "756 53",
                        "addressRegion": "Uppsala län", "addressCountry": "SE"},
            "areaServed": {"@type": "City", "name": "Uppsala"},
            "geo": {"@type": "GeoCoordinates", "latitude": 59.7877839, "longitude": 17.632907}, "hasMap": MAPS,
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "15:00", "closes": "19:00"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "09:00", "closes": "19:00"}]}


def ld(obj):
    obj = {"@context": "https://schema.org", **obj}
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>\n'


def page(name, title, desc, body, head="", cta=True, image="og.jpg"):
    url = SITE + "/" + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta name="geo.region" content="SE-C"><meta name="geo.placename" content="Uppsala">
<meta property="og:site_name" content="Hemmacykel"><meta property="og:locale" content="sv_SE"><meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="assets/site.css">
{head}</head>
<body>
<a class="skip" href="#main">Hoppa till innehållet</a>
{header(name)}
<main id="main">
{body}
</main>
{footer(cta)}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    (OUT / name).write_text(doc, encoding="utf-8")


def crumbs(trail, current):
    links = "".join(f'<a href="{h}">{e(t)}</a><span>/</span>' for h, t in [("index.html", "Start"), *trail])
    return f'<nav class="crumbs" aria-label="Brödsmulor">{links}<span aria-current="page">{e(current)}</span></nav>'


def page_head(h1, lead="", trail=(), current=None, kick="", extra="", img=None, img_alt="", pos="50% 50%"):
    kick_html = f'<p class="kick">{kick}</p>' if kick else ""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    fig = f'<figure class="ph-img"><img src="img/{img}" alt="{e(img_alt)}" style="object-position:{pos}"></figure>' if img else ""
    return f'''<section class="page-h{" has-img" if img else ""}"><div class="wrap ph-g">
  <div class="ph-t">{crumbs(trail, current or re.sub("<[^>]+>", "", h1))}{kick_html}<h1>{h1}</h1>{lead_html}{extra}</div>{fig}
</div></section>'''


def sec_head(kick, h2, side=""):
    if side and not side.startswith("<"):
        side = f"<p>{side}</p>"
    return f'<div class="sh"><div><p class="kick">{kick}</p><h2>{h2}</h2></div>{side}</div>'


def btn(href, label, cls="btn-ink", arrow=True):
    return f'<a class="btn {cls}" href="{href}">{label}{" " + ico("arrow") if arrow else ""}</a>'


def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{ico('check')}<span>{e(i)}</span></li>" for i in items) + "</ul>"


def faq_list(items):
    return '<div class="qa">' + "".join(
        f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in items) + "</div>"


def price_calc():
    svc = ('<optgroup label="Reparationer">'
           + "".join(f'<option value="{v}" data-price="{p}">{n}{f" – {kr(p)}" if p else ""}</option>' for v, n, p in REPAIRS)
           + '</optgroup><optgroup label="Servicepaket">'
           + "".join(f'<option value="{v}" data-price="{p}">{n} – {kr(p)}</option>' for v, n, p, *_ in PACKAGES)
           + "</optgroup>")
    typ = "".join(f'<option value="{v}" data-add="{a}">{n}{f" (+{a} kr)" if a else ""}</option>' for v, n, a in BIKE_TYPES)
    return f'''<form class="calc" action="boka.html" method="get" data-calc>
  <label class="calc-f"><span>Vad behöver fixas?</span><select name="tjanst">{svc}</select></label>
  <label class="calc-f"><span>Typ av cykel</span><select name="typ">{typ}</select></label>
  <p class="calc-p"><span>Uppskattat pris</span><b data-calc-total aria-live="polite">{kr(REPAIRS[0][2])}</b></p>
  <button class="btn btn-lime" type="submit">Boka {ico("arrow")}</button>
</form>'''


def svc_card(s):
    return (f'<a href="tjanst-{s["slug"]}.html"><img src="img/{s["img"]}" alt="" loading="lazy">'
            f'<span class="t"><span class="row"><b>{s["name"]}</b><span class="pr">{s["price"]}</span></span><small>{s["short"]}</small></span></a>')


def extra_cards():
    return [
        f'<a href="boka.html?tjanst=ovrigt"><img src="img/tjanst-ovrigt.jpg" alt="" loading="lazy"><span class="t"><span class="row"><b>Övrigt</b><span class="pr">Prisförslag</span></span>'
        f'<small>Något annat? Beskriv problemet så ger vi ett prisförslag.</small></span></a>',
        f'<a href="cyklar.html"><img src="img/tjanst-begagnat.jpg" alt="" loading="lazy"><span class="t"><span class="row"><b>Begagnade cyklar</b><span class="pr">Till salu</span></span>'
        f'<small>Vi köper, servar och säljer begagnade cyklar.</small></span></a>',
    ]


def bike_card(b):
    over = '<span class="sold-over"><span>Såld</span></span>' if b["sold"] else '<span class="state">Till salu</span>'
    return f'''<a class="bc{" sold" if b["sold"] else ""}" href="{b["file"]}">
  <span class="ph"><img src="img/cyklar/{b["images"][0]}" alt="{e(b["title"])}" loading="lazy">{over}</span>
  <span class="row"><b>{e(b["title"])}</b><span class="pr">{kr(b["price"])}</span></span>
  <small>{e(b["size"])} · {e(b["condition"])}{" · Såld" if b["sold"] else ""}</small>
</a>'''


def review(n, t):
    return f'<figure><span class="st">★★★★★</span><blockquote>”{e(t)}”</blockquote><figcaption><b>{e(n)}</b> · Google</figcaption></figure>'


def score_block():
    return (f'<div class="score"><b>{RATING}</b><span><span class="st">★★★★★</span>{REVIEW_COUNT} omdömen på Google<br>'
            f'<a href="omdomen.html">Alla omdömen {ico("arrow")}</a></span></div>')


def steps_html():
    return '<ol class="steps">' + "".join(f'<li><span class="n">{i + 1}</span><h3>{t}</h3><p>{s}</p></li>' for i, (t, s) in enumerate(STEPS)) + "</ol>"


def plans_html():
    return '<div class="pk">' + "".join(
        f'''<article{' class="hl"' if slug == FEATURED else ""}>
  <div class="top"><h3>{name}</h3>{'<span class="tag">Populärast</span>' if slug == FEATURED else ""}</div>
  <p class="for">{for_who}</p><p class="amt">{price}<span>kr</span></p><p class="vat">Fast pris inkl. moms, arbete och material</p>
  <ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul>
  {btn(f"boka.html?paket={slug}", f"Boka {name}", "btn-lime" if slug == FEATURED else "btn-line")}
</article>''' for slug, name, price, for_who, items in PACKAGES) + "</div>"


def types_html():
    return '<ul class="types">' + "".join(f'<li><span>{n}</span><b>{f"+{a} kr" if a else "Ordinarie pris"}</b></li>' for _, n, a in BIKE_TYPES) + "</ul>"


# --- bokningsformuläret ---------------------------------------------------------------
def booking_html():
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
    return f'''<div class="booking">
  <form id="booking" class="bk-form" novalidate data-mail="{MAIL}">
    <ol class="bk-steps"><li class="on"><span>1</span>Tjänst</li><li><span>2</span>Tid och plats</li><li><span>3</span>Kontakt</li></ol>
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
      <label class="fld"><span>Beskriv problemet <small>(valfritt)</small></span><textarea name="beskrivning" rows="3" placeholder="T.ex. bakdäcket tappar luft och växlarna hoppar."></textarea></label>
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
    <a class="sum-call" href="tel:{TEL}">Föredrar du att ringa?<b>{PHONE}</b></a>
  </aside>
</div>'''



# --- startsidan -----------------------------------------------------------------------
def index():
    tiles = "".join(svc_card(s) for s in SERVICES)
    reviews = "".join(review(n, t) for n, t in REVIEWS[:6])
    bikes = "".join(bike_card(b) for b in BIKES[:3])
    faq = [qa for qa in FAQ if qa[0] in ("Vad kostar det?", "Hur fungerar det?", "Kan ni serva elcykel?", "Var i Uppsala kommer ni?", "När kan ni komma?", "Hur betalar jag?")]
    # Gamla länkar från ensidesversionen (index.html#boka, #merida-2670 …) skickas till rätt sida
    old = {"boka": "boka.html", **{b["id"]: b["file"] for b in BIKES}}
    head = ld({"@graph": [{"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Hemmacykel", "url": SITE,
                           "logo": f"{SITE}/img/apple-touch-icon.png", "telephone": TEL, "email": MAIL}, BUSINESS]})
    head += f'<script>(function(){{var m={json.dumps(old)},h=location.hash.slice(1);if(m[h])location.replace(m[h]+location.search);}})();</script>\n'

    body = f'''<section class="hero">
  <img class="hero-bg" src="img/hemmacykel-hero.jpg" alt="Hemmacykel servar en cykel på plats vid ett cykelställ i Uppsala" width="1170" height="1560" fetchpriority="high">
  <div class="wrap hero-c">
    <p class="kick">Mobil cykelservice i Uppsala</p>
    <h1>Få vardagen att rulla igen.</h1>
    <p class="lead">Vi kommer hem till dig och fixar cykeln där den står. Fasta priser, inga gömda avgifter.</p>
    {price_calc()}
    <div class="hero-meta"><a href="omdomen.html"><span class="st">★★★★★</span> {RATING} på Google · {REVIEW_COUNT} omdömen</a><span>Inkl. moms. Reseavgift kan tillkomma.</span></div>
  </div>
</section>

<section class="sec" id="tjanster"><div class="wrap">
  {sec_head("Tjänster och priser", "Fast pris på det vanligaste.", btn("tjanster.html", "Alla tjänster", "btn-line"))}
  <div class="svc">{tiles}</div>
  <p class="note">Elcykel, lådcykel och andra tyngre cyklar +50 kr · elsparkcykel +100 kr · reseavgift 50 kr vid över 15 min körtid, 100 kr vid över 25 min. <a href="priser.html">Hela prislistan</a></p>
</div></section>

<section class="sec alt" id="paket"><div class="wrap">
  {sec_head("Servicepaket", "Hela cykeln genomgången, till fast pris.", btn("tjanst-service.html", "Jämför paketen", "btn-line"))}
  {plans_html()}
</div></section>

<section class="sec" id="sa-funkar-det"><div class="wrap">
  {sec_head("Så funkar det", "Från trasig till rullande på tre steg.", btn("boka.html", "Boka nu"))}
  {steps_html()}
</div></section>

<section class="sec alt" id="om-oss"><div class="wrap about">
  <img src="img/hemmacykel-team.jpg" alt="Grundarna av Hemmacykel vid Ångströmlaboratoriet, Uppsala" loading="lazy" width="1170" height="1560">
  <div>
    <p class="kick">Om oss</p>
    <h2>Två unga entreprenörer från Uppsala.</h2>
    <p>Vi startade Hemmacykel för att ge Uppsalabor mer tid och mindre krångel. En bokning, en tid som passar dig, och sedan fungerar cykeln igen.</p>
    <p>Cykeln tar dig till jobbet, träningen, kompisarna och familjen. Därför ska cykelservice passa din vardag – inte tvärtom.</p>
    <ul class="facts">
      <li><small>Område</small>Hela Uppsala – Centrum, Luthagen, Flogsta, Sala backe, Gottsunda, Sävja, Årsta m.fl.</li>
      <li><small>Tider</small>Vardagar 15–19, helger 9–19</li>
      <li><small>Cyklar</small>Vanliga cyklar, elcyklar, lådcyklar, fatbikes och elsparkcyklar</li>
      <li><small>Betalning</small>Swish på plats när jobbet är klart</li>
    </ul>
    <p class="more">{btn("om-oss.html", "Mer om oss", "btn-line")}</p>
  </div>
</div></section>

<section class="sec" id="omdomen"><div class="wrap">
  {sec_head("Omdömen", "Vad kunderna i Uppsala säger.", score_block())}
  <div class="rv">{reviews}</div>
</div></section>

<section class="sec sec-tight"><div class="wrap"><div class="refer">
  <div><p class="kick">Tipsa en kompis</p><h2>Ge en kompis 100 kr – och få 100 kr själv.</h2>
  <p>Efter besöket får du en personlig kod. När en kompis bokar med din kod får hen 100 kr rabatt, och du får 100 kr rabatt på ditt nästa besök.</p></div>
  {btn("boka.html", "Boka med kod")}
</div></div></section>

<section class="sec alt" id="cyklar"><div class="wrap">
  {sec_head("Cyklar till salu", "Begagnat, genomgånget och redo att rulla.", btn("cyklar.html", "Alla cyklar", "btn-line"))}
  <div class="bikes">{bikes}</div>
</div></section>

<section class="sec" id="fragor"><div class="wrap faq">
  <div><p class="kick">Vanliga frågor</p><h2>Frågor och svar.</h2><p class="muted">Hittar du inte svaret? Ring <a href="tel:{TEL}">{PHONE}</a> eller mejla <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  <p class="more">{btn("fragor.html", "Alla frågor", "btn-line")}</p></div>
  {faq_list(faq)}
</div></section>'''
    page("index.html", "Cykelservice Uppsala – Mobil cykelverkstad | Hemmacykel",
         "Mobil cykelservice i Uppsala. Vi kommer hem till dig och fixar cykeln på plats – punktering, däckbyte, bromsar, kedja och service. Fasta priser, inga gömda avgifter.",
         body, head=head)


# --- tjänster -------------------------------------------------------------------------
def tjanster():
    cards = "".join(svc_card(s) for s in SERVICES) + "".join(extra_cards())
    body = page_head("Tjänster och priser", "Vi kommer hem till dig och fixar cykeln där den står – från en punktering till en hel genomgång. Fast pris på det vanligaste, inklusive moms, arbete och material.",
                     kick="Tjänster", extra=f'<div class="btns">{btn("boka.html", "Boka service")}{btn("priser.html", "Se prislistan", "btn-line", False)}</div>') + f'''
<section class="sec"><div class="wrap">
  {sec_head("Det här hjälper vi dig med", "Välj tjänst och läs mer.", "Osäker på vad cykeln behöver? Välj Övrigt när du bokar och beskriv problemet, så ger vi ett prisförslag.")}
  <div class="svc svc-4">{cards}</div>
</div></section>

<section class="sec alt"><div class="wrap">
  {sec_head("Servicepaket", "Hela cykeln genomgången, till fast pris.", btn("tjanst-service.html", "Jämför paketen", "btn-line"))}
  {plans_html()}
</div></section>

<section class="sec"><div class="wrap split2">
  <div><p class="kick">Alla sorters cyklar</p><h2>Vanlig cykel, elcykel eller lådcykel.</h2>
    <p class="muted">Vi tar både vanliga cyklar och elcyklar – allt från bromsar och växlar till kedja. För tyngre cyklar tillkommer ett litet tillägg som syns i priset när du bokar.</p>
    <p class="more">{btn("tjanst-elcykel.html", "Elcykel och specialcyklar", "btn-line")}</p></div>
  <div class="card">{types_html()}</div>
</div></section>

<section class="sec alt"><div class="wrap">
  {sec_head("Så funkar det", "Från trasig till rullande på tre steg.", btn("boka.html", "Boka nu"))}
  {steps_html()}
</div></section>'''
    page("tjanster.html", "Tjänster och priser – cykelservice i Uppsala | Hemmacykel",
         "Punktering, däckbyte, kedjebyte, bromsar, servicepaket och elcykelservice hemma hos dig i Uppsala. Fasta priser inklusive moms, arbete och material.", body)


def service_page(s):
    others = [o for o in SERVICES if o["slug"] != s["slug"]][:3]
    book = f"boka.html?{s['book']}"
    extra = (f'<div class="ph-cta"><span class="price-chip">{s["price"]}</span>{btn(book, s["cta"])}'
             f'<a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a></div>')
    head = page_head(s["h1"], s["lead"], trail=[("tjanster.html", "Tjänster")], current=s["name"], kick=s["name"], extra=extra,
                     img=s["img"] if s["slug"] != "elcykel" else None)
    parts = []
    if s.get("signs"):
        signs = "".join(f'<li><span class="n">{i + 1}</span><p>{e(t)}</p></li>' for i, t in enumerate(s["signs"]))
        parts.append(f'''<section class="sec"><div class="wrap">
  {sec_head("Känner du igen det här?", "Tecken på att det är dags.")}
  <ol class="signs">{signs}</ol>
</div></section>''')

    if s["slug"] == "service":
        rows = [("Antal cyklar", "1", "1", "2")]
        base = PACKAGES[0][4]
        extra_items = [i for i in PACKAGES[1][4] if i != "Allt i paket Cykelcheck"]
        rows += [(i, True, True, True) for i in base]
        rows += [(i, False, True, False) for i in extra_items]
        cell = lambda v: f'<td>{ico("check")}<span class="sr">Ingår</span></td>' if v is True else ('<td class="no">–</td>' if v is False else f"<td>{v}</td>")
        table = "".join(f"<tr><th scope=\"row\">{e(r[0])}</th>{''.join(cell(v) for v in r[1:])}</tr>" for r in rows)
        heads = "".join(f'<th scope="col"{" class=\"hl\"" if slug == FEATURED else ""}>{n}<small>{kr(p)}</small></th>' for slug, n, p, *_ in PACKAGES)
        books = "".join(f'<td>{btn(f"boka.html?paket={slug}", "Boka", "btn-lime btn-s" if slug == FEATURED else "btn-line btn-s")}</td>' for slug, *_ in PACKAGES)
        parts.append(f'''<section class="sec alt"><div class="wrap">
  {sec_head("Paketen", "Välj rätt nivå direkt.", s["note"])}
  {plans_html()}
</div></section>
<section class="sec"><div class="wrap">
  {sec_head("Jämför", "Det här ingår i varje paket.")}
  <div class="cmp-wrap"><table class="cmp"><thead><tr><th scope="col"><span class="sr">Ingår</span></th>{heads}</tr></thead><tbody>{table}</tbody>
  <tfoot><tr><td></td>{books}</tr></tfoot></table></div>
</div></section>''')
    else:
        if s["slug"] == "elcykel":
            side = f'<div class="pcard"><h3>Tillägg per cykeltyp</h3>{types_html()}<p class="small muted">Tillägget läggs på priset för tjänsten du bokar.</p>{btn(book, "Boka service", "btn-lime")}</div>'
        else:
            rows = "".join(f'<li><span>{n}</span><b>{kr(p)}</b><a href="boka.html?{q}">Boka</a></li>' for n, p, q in s["prices"])
            side = (f'<div class="pcard"><h3>Pris</h3><ul class="plines">{rows}</ul>'
                    f'<p class="small muted">Inklusive moms, arbete och material. Elcykel och tyngre cyklar +50 kr, elsparkcykel +100 kr. Reseavgift vid över 15 min körtid.</p>'
                    f'{btn(book, "Boka nu", "btn-lime")}</div>')
        parts.append(f'''<section class="sec alt"><div class="wrap svc-detail">
  <div><p class="kick">Det här ingår</p><h2>Så gör vi.</h2>{checks(s["includes"])}<p class="tip">{e(s["note"])}</p></div>
  {side}
</div></section>''')

    faq = SERVICE_FAQ + ([FAQ_GROUPS[2][2][0], FAQ_GROUPS[2][2][1]] if s["slug"] == "elcykel" else [FAQ_GROUPS[2][2][2]])
    parts.append(f'''<section class="sec{" alt" if s["slug"] == "service" else ""}"><div class="wrap">
  {sec_head("Så funkar det", "Från trasig till rullande på tre steg.")}
  {steps_html()}
</div></section>
<section class="sec{"" if s["slug"] == "service" else " alt"}"><div class="wrap faq">
  <div><p class="kick">Frågor</p><h2>Bra att veta.</h2><p class="more">{btn("fragor.html", "Alla frågor", "btn-line")}</p></div>
  {faq_list(faq)}
</div></section>
<section class="sec"><div class="wrap">
  {sec_head("Fler tjänster", "Något annat som behöver fixas?", btn("tjanster.html", "Alla tjänster", "btn-line"))}
  <div class="svc">{"".join(svc_card(o) for o in others)}</div>
</div></section>''')

    offers = ([{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "SEK"} for n, p, _ in s["prices"]] if s.get("prices")
              else [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "SEK"} for _, n, p, *_ in PACKAGES] if s["slug"] == "service" else [])
    schema = {"@type": "Service", "name": f"{s['name']} – Hemmacykel", "serviceType": s["name"], "areaServed": {"@type": "City", "name": "Uppsala"},
              "provider": {"@type": "LocalBusiness", "name": "Hemmacykel", "telephone": TEL, "url": SITE}}
    if offers:
        schema["offers"] = offers
    page(f"tjanst-{s['slug']}.html", f"{s['name']} i Uppsala – hemma hos dig | Hemmacykel", f"{s['short']} {s['lead']}",
         head + "\n" + "\n".join(parts), head=ld(schema), image=s["img"] if s["slug"] != "elcykel" else "og.jpg")


# --- priser ---------------------------------------------------------------------------
def priser():
    rep = "".join(f'<li><span>{n}</span><b>{kr(p) if p else "Prisförslag"}</b><a href="boka.html?tjanst={v}">Boka</a></li>' for v, n, p in REPAIRS)
    pkg = "".join(f'<li><span>{n}<small>{f}</small></span><b>{kr(p)}</b><a href="boka.html?paket={v}">Boka</a></li>' for v, n, p, f, _ in PACKAGES)
    typ = "".join(f'<li><span>{n}</span><b>{f"+{a} kr" if a else "–"}</b></li>' for _, n, a in BIKE_TYPES[1:])
    trav = "".join(f'<li><span>{n}</span><b>+{p} kr</b></li>' for n, p in TRAVEL)
    facts = [("Fast pris", "Priserna gäller inklusive moms, arbete och material om inget annat tydligt anges."),
             ("Inga överraskningar", "Du ser priset innan vi börjar. Eventuella ändringar stäms av med dig innan arbetet utförs."),
             ("Swish på plats", "Du betalar när jobbet är klart, via Swish om inget annat överenskommits."),
             ("Kvitto alltid", "Kvitto erbjuds alltid och lämnas på begäran.")]
    facts_html = "".join(f'<li><b>{t}</b><p>{d}</p></li>' for t, d in facts)
    body = page_head("Priser", "Fasta priser inklusive moms, arbete och material. Du ser alltid priset innan vi börjar – inga gömda avgifter.", kick="Prislista") + f'''
<section class="sec"><div class="wrap price-pg">
  <div class="plist">
    <h2>Reparationer</h2><ul class="plines">{rep}</ul>
    <h2>Servicepaket</h2><ul class="plines">{pkg}</ul>
    <h2>Tillägg för cykeltyp</h2><ul class="plines">{typ}</ul>
    <h2>Reseavgift</h2><ul class="plines">{trav}</ul>
  </div>
  <aside class="calc-card"><h3>Räkna ut ditt pris</h3><p>Välj tjänst och typ av cykel. Priset följer med till bokningen.</p>{price_calc()}</aside>
</div></section>
<section class="sec alt"><div class="wrap">
  {sec_head("Så funkar priset", "Inga gömda avgifter.")}
  <ul class="fact-cards">{facts_html}</ul>
</div></section>
<section class="sec"><div class="wrap faq">
  <div><p class="kick">Frågor</p><h2>Om priser och betalning.</h2></div>
  {faq_list(FAQ_GROUPS[1][2])}
</div></section>'''
    page("priser.html", "Priser – cykelservice i Uppsala | Hemmacykel",
         "Prislista för mobil cykelservice i Uppsala: punktering 299 kr, däckbyte 349 kr, kedjebyte 299 kr, bromsar från 199 kr och servicepaket från 499 kr.", body)


# --- boka ------------------------------------------------------------------------------
def boka():
    body = page_head("Boka service", "Tre korta steg. Priset räknas ut medan du väljer, och vi bekräftar tid och pris innan vi kommer.", kick="Bokning") + f'''
<section class="sec sec-book"><div class="wrap">{booking_html()}</div></section>'''
    page("boka.html", "Boka cykelservice i Uppsala | Hemmacykel",
         "Boka mobil cykelservice i Uppsala på någon minut. Välj tjänst, tid och adress – vi kommer hem till dig.", body, cta=False)


# --- cyklar ----------------------------------------------------------------------------
def cyklar():
    n_sale = sum(not b["sold"] for b in BIKES)
    chips = (f'<ul class="chips-row"><li class="on">{n_sale} till salu just nu</li><li>{len(BIKES) - n_sale} sålda</li>'
             '<li>Genomservade</li><li>Hämtas i Uppsala</li><li>Provkör innan du köper</li></ul>')
    body = page_head("Cyklar till salu", "Vi köper, servar och säljer begagnade cyklar i Uppsala. Alla cyklar är genomgångna av oss innan de säljs.",
                     kick="Begagnade cyklar", extra=chips) + f'''
<section class="sec"><div class="wrap">
  <div class="bikes">{"".join(bike_card(b) for b in BIKES)}</div>
</div></section>
<section class="sec alt"><div class="wrap">
  <div class="refer refer-w">
    <div><p class="kick">Inget som passar?</p><h2>Letar du efter något specifikt – eller vill du sälja din cykel?</h2>
    <p>Vi köper begagnade cyklar och har ofta fler på gång än det som syns här. Hör av dig så berättar vi vad vi har.</p></div>
    <div class="btns"><a class="btn btn-ink" href="tel:{TEL}">Ring {PHONE}</a><a class="btn btn-line" href="mailto:{MAIL}">Mejla oss</a></div>
  </div>
  <p class="fine">Cyklarna säljs som privatköp. Du har möjlighet att inspektera och provköra cykeln innan köpet genomförs. Läs mer i <a href="villkor.html">användarvillkoren</a>.</p>
</div></section>'''
    page("cyklar.html", "Begagnade cyklar till salu i Uppsala | Hemmacykel",
         "Servade begagnade cyklar till salu i Uppsala. Alla cyklar är genomgångna av Hemmacykel innan de säljs.", body)


def bike_page(b):
    imgs = "".join(f'<img src="img/cyklar/{f}" alt="{e(b["title"])}, bild {i + 1}"{" loading=\"lazy\"" if i else ""}>' for i, f in enumerate(b["images"]))
    thumbs = "".join(f'<button type="button" data-thumb aria-label="Visa bild {i + 1}"><img src="img/cyklar/{f}" alt="" loading="lazy"></button>' for i, f in enumerate(b["images"]))
    over = '<span class="sold-over big"><span>Såld</span></span>' if b["sold"] else '<span class="state">Till salu</span>'
    specs = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in
                    [("Märke", b["brand"]), ("Hjulstorlek", b["size"]), ("Skick", b["condition"]), ("Hämtas i", b["location"])])
    if b["sold"]:
        act = f'<div class="sold-note"><b>Den här cykeln är såld.</b><p>Nya cyklar läggs upp löpande. Letar du efter något specifikt? Hör av dig.</p><div class="btns">{btn("cyklar.html", "Se cyklar till salu")}<a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a></div></div>'
    else:
        act = (f'<div class="btns">{btn("tel:" + TEL, "Ring och köp", "btn-lime", False)}'
               f'<a class="btn btn-line" href="mailto:{MAIL}?subject={quote("Intresserad av " + b["title"])}">Mejla om cykeln</a></div>'
               '<p class="small muted">Privatköp. Du kan inspektera och provköra cykeln innan köpet genomförs.</p>')
    lists = ""
    if b["done"]:
        lists += f'<div><h3>Nyligen utfört</h3>{checks(b["done"])}</div>'
    if b["equipment"]:
        lists += '<div><h3>Utrustning</h3><ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in b["equipment"]) + "</ul></div>"
    note = f'<p class="tip">{e(b["note"])}</p>' if b["note"] else ""
    others = [o for o in BIKES if o["id"] != b["id"]][:3]
    body = f'''<section class="wrap bike-pg">
  {crumbs([("cyklar.html", "Cyklar till salu")], b["title"])}
  <div class="bp-g{" sold" if b["sold"] else ""}">
    <div class="bp-gal" data-car>
      <div class="gal">
        <div class="gal-track" data-track tabindex="0" aria-label="Bilder på {e(b["title"])}">{imgs}</div>
        {over}
        <button type="button" class="gal-btn prev" data-prev aria-label="Föregående bild">{ico("left")}</button>
        <button type="button" class="gal-btn next" data-next aria-label="Nästa bild">{ico("right")}</button>
        <span class="gal-count" data-count>1 / {len(b["images"])}</span>
      </div>
      <div class="thumbs">{thumbs}</div>
    </div>
    <aside class="bp-info">
      <p class="kick">{e(b["brand"])}</p>
      <h1>{e(b["title"])}</h1>
      <p class="bp-price">{kr(b["price"])}</p>
      <dl class="specs">{specs}</dl>
      {act}
    </aside>
  </div>
</section>
<section class="sec alt"><div class="wrap bp-desc">
  <div><p class="kick">Om cykeln</p><h2>{e(b["title"])}</h2><p class="lead">{e(b["intro"])}</p>{note}</div>
  <div class="bp-lists">{lists}</div>
</div></section>
<section class="sec"><div class="wrap">
  {sec_head("Fler cyklar", "Begagnat, genomgånget och redo att rulla.", btn("cyklar.html", "Alla cyklar", "btn-line"))}
  <div class="bikes">{"".join(bike_card(o) for o in others)}</div>
</div></section>'''
    schema = {"@type": "Product", "name": b["title"], "brand": {"@type": "Brand", "name": b["brand"]}, "description": b["intro"],
              "image": [f"{SITE}/img/cyklar/{f}" for f in b["images"]],
              "offers": {"@type": "Offer", "price": str(b["price"]), "priceCurrency": "SEK", "itemCondition": "https://schema.org/UsedCondition",
                         "availability": "https://schema.org/SoldOut" if b["sold"] else "https://schema.org/InStock"}}
    page(b["file"], f"{b['title']}{' (såld)' if b['sold'] else ''} – {kr(b['price'])} | Hemmacykel",
         f"{b['title']}, {b['size']}, {b['condition'].lower()}. {b['intro']}", body, head=ld(schema), image=f"cyklar/{b['images'][0]}")


# --- om oss, omdömen, frågor, kontakt -------------------------------------------------
def om_oss():
    values = "".join(f'<li><span class="n">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(VALUES))
    body = page_head("Två unga entreprenörer från Uppsala.",
                     "Vi startade Hemmacykel för att ge Uppsalabor mer tid och mindre krångel. En bokning, en tid som passar dig, och sedan fungerar cykeln igen.",
                     current="Om oss", kick="Om oss", img="hemmacykel-team.jpg", img_alt="Grundarna av Hemmacykel vid Ångströmlaboratoriet, Uppsala", pos="50% 40%",
                     extra=f'<div class="btns">{btn("boka.html", "Boka service")}{btn("kontakt.html", "Kontakta oss", "btn-line", False)}</div>') + f'''
<section class="sec"><div class="wrap story">
  <p class="kick">Därför finns vi</p>
  <p class="big">Låt inte en trasig cykel stoppa dig.</p>
  <div class="story-t">
    <p>Cykeln tar dig till jobbet, träningen, kompisarna och familjen. När den går sönder försvinner inte bara möjligheten att cykla. Du förlorar tid, frihet och en del av det som får vardagen att fungera.</p>
    <p>Därför ska cykelservice passa din vardag, inte tvärtom. Vi reparerar din cykel direkt hemma hos dig i Uppsala, så att du slipper släpa den till verkstaden, vänta på en ledig tid eller anpassa vardagen efter en reparation.</p>
  </div>
</div></section>
<section class="sec alt"><div class="wrap">
  {sec_head("Det vi står för", "Mer tid, mindre krångel.")}
  <ol class="values">{values}</ol>
</div></section>
<section class="sec"><div class="wrap about">
  <img src="img/hemmacykel-hero.jpg" alt="Hemmacykel servar en cykel på plats i Uppsala" loading="lazy" width="1170" height="1560">
  <div>
    <p class="kick">Så jobbar vi</p>
    <h2>Hela verkstaden, hem till dig.</h2>
    <p>Du bokar en tid, vi kommer dit cykeln står och fixar den på plats. Du ser priset innan vi börjar och betalar med Swish när jobbet är klart.</p>
    <ul class="facts">
      <li><small>Område</small>Hela Uppsala – {", ".join(AREAS)} m.fl.</li>
      <li><small>Tider</small>Vardagar 15–19, helger 9–19</li>
      <li><small>Cyklar</small>Vanliga cyklar, elcyklar, lådcyklar, fatbikes och elsparkcyklar</li>
      <li><small>Trygghet</small>3 års reklamationsrätt enligt konsumenttjänstlagen</li>
    </ul>
  </div>
</div></section>
<section class="sec alt"><div class="wrap">
  {sec_head("Omdömen", "Vad kunderna i Uppsala säger.", score_block())}
  <div class="rv">{"".join(review(n, t) for n, t in REVIEWS[:3])}</div>
</div></section>
<section class="sec sec-tight"><div class="wrap"><div class="refer">
  <div><p class="kick">Tipsa en kompis</p><h2>Ge en kompis 100 kr – och få 100 kr själv.</h2>
  <p>Efter besöket får du en personlig kod. När en kompis bokar med din kod får hen 100 kr rabatt, och du får 100 kr rabatt på ditt nästa besök.</p></div>
  {btn("boka.html", "Boka med kod")}
</div></div></section>'''
    page("om-oss.html", "Om oss – mobil cykelverkstad i Uppsala | Hemmacykel",
         "Hemmacykel drivs av två unga entreprenörer från Uppsala. Vi kommer hem till dig och fixar cykeln på plats.", body, image="hemmacykel-team.jpg")


def omdomen():
    stats = "".join(
        f'<li><b>{sum(bool(re.search(p, t, re.I)) for _, t in REVIEWS)} av {len(REVIEWS)}</b><span>{label}</span></li>' for p, label in REVIEW_THEMES)
    big_n, big_t = REVIEWS[0]
    body = page_head("Vad kunderna i Uppsala säger.", f"{RATING} i snittbetyg från {REVIEW_COUNT} omdömen på Google. Här är ett urval.",
                     current="Omdömen", kick="Omdömen",
                     extra=f'<div class="btns"><a class="btn btn-ink" href="{MAPS}" target="_blank" rel="noopener">Läs alla på Google {ico("arrow-ur")}</a>{btn("boka.html", "Boka service", "btn-line", False)}</div>') + f'''
<section class="sec"><div class="wrap rev-top">
  <div class="rev-score"><b>{RATING}</b><span class="st">★★★★★</span><p>{REVIEW_COUNT} omdömen på Google</p></div>
  <ul class="rev-stats">{stats}</ul>
  <p class="small muted rev-src">Räknat på omdömena på den här sidan.</p>
</div></section>
<section class="sec alt"><div class="wrap">
  <figure class="rev-big"><span class="st">★★★★★</span><blockquote>”{e(big_t)}”</blockquote><figcaption><b>{e(big_n)}</b> · Google</figcaption></figure>
  <div class="rv">{"".join(review(n, t) for n, t in REVIEWS[1:])}</div>
</div></section>
<section class="sec sec-tight"><div class="wrap"><div class="refer">
  <div><p class="kick">Har du anlitat oss?</p><h2>Lämna gärna ett omdöme.</h2>
  <p>Det tar en minut och hjälper andra i Uppsala att hitta oss.</p></div>
  <a class="btn btn-ink" href="{MAPS}" target="_blank" rel="noopener">Lämna omdöme på Google {ico("arrow-ur")}</a>
</div></div></section>'''
    page("omdomen.html", f"Omdömen – {RATING} på Google | Hemmacykel",
         f"Vad kunderna i Uppsala säger om Hemmacykel. {RATING} i snittbetyg från {REVIEW_COUNT} omdömen på Google.", body)


def fragor():
    nav = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _ in FAQ_GROUPS)
    groups = "".join(f'<section class="faq-g" id="{a}"><h2>{t}</h2>{faq_list(qs)}</section>' for a, t, qs in FAQ_GROUPS)
    schema = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = page_head("Vanliga frågor", f'Svar på det vanligaste om bokning, priser, cyklar vi servar och köp av begagnad cykel. Hittar du inte svaret? Ring <a href="tel:{TEL}">{PHONE}</a>.',
                     kick="Frågor och svar") + f'''
<section class="sec"><div class="wrap faq-pg">
  <nav class="side-nav" aria-label="Kategorier"><p class="kick">Kategorier</p><ul>{nav}</ul></nav>
  <div>{groups}</div>
</div></section>'''
    page("fragor.html", "Vanliga frågor om cykelservice i Uppsala | Hemmacykel",
         "Svar på vanliga frågor om bokning, priser, betalning, elcykelservice och köp av begagnad cykel hos Hemmacykel.", body, head=ld(schema))


def kontakt():
    cards = [
        ("phone", "Ring", f'<a href="tel:{TEL}">{PHONE}</a>', "Snabbast när du vill boka eller fråga något."),
        ("mail", "Mejla", f'<a href="mailto:{MAIL}">{MAIL}</a>', "Vi svarar så snart vi kan."),
        ("pin", "Adress", f'{STREET}, {ZIP_CITY}', f'<a href="{MAPS}" target="_blank" rel="noopener">Visa på karta</a> · {AREA}'),
        ("clock", "Tider", "Vardagar 15–19<br>Helger 9–19", "Då är vi ute och servar cyklar."),
    ]
    cards_html = "".join(f'<li><span class="c-ico">{ico(i)}</span><small>{t}</small><b>{v}</b><p>{d}</p></li>' for i, t, v, d in cards)
    areas = "".join(f"<li>{a}</li>" for a in AREAS) + "<li>m.fl.</li>"
    body = page_head("Kontakta oss", "Ring, mejla eller boka direkt. Vi är ute vardagar 15–19 och helger 9–19.", kick="Kontakt",
                     extra=f'<div class="btns">{btn("boka.html", "Boka service")}<a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a></div>') + f'''
<section class="sec"><div class="wrap"><ul class="ccards">{cards_html}</ul></div></section>
<section class="sec alt"><div class="wrap contact-g">
  <form class="cform" data-mailto="{MAIL}" novalidate>
    <h2>Skicka en fråga</h2>
    <p class="muted">Formuläret öppnar ett ifyllt mejl till oss. Vill du boka en tid går det snabbast via <a href="boka.html">bokningen</a>.</p>
    <div class="fld-grid">
      <label class="fld"><span>Namn</span><input name="namn" autocomplete="name" required></label>
      <label class="fld"><span>Telefon</span><input name="telefon" type="tel" autocomplete="tel" inputmode="tel"></label>
    </div>
    <label class="fld"><span>E-post</span><input name="epost" type="email" autocomplete="email" required></label>
    <label class="fld"><span>Meddelande</span><textarea name="meddelande" rows="5" required></textarea></label>
    <p class="bk-err" role="alert"></p>
    <button class="btn btn-ink" type="submit">Skicka {ico("arrow")}</button>
    <p class="form-done" hidden>Tack! Nu öppnas ditt mejlprogram. Öppnades inget? Mejla <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </form>
  <div class="area">
    <p class="kick">Här kommer vi</p>
    <h2>Hela Uppsala.</h2>
    <p class="muted">Skriv in din adress när du bokar, så ser vi direkt om vi kan komma förbi.</p>
    <ul class="area-list">{areas}</ul>
    <a class="map-link" href="{MAPS}" target="_blank" rel="noopener"><img src="img/hemmacykel-hero.jpg" alt="" loading="lazy"><span>Hemmacykel på Google Maps {ico("arrow-ur")}</span></a>
  </div>
</div></section>'''
    page("kontakt.html", "Kontakt – Hemmacykel, mobil cykelverkstad i Uppsala",
         f"Kontakta Hemmacykel: ring {PHONE} eller mejla {MAIL}. Vi är ute vardagar 15–19 och helger 9–19 i hela Uppsala.", body, head=ld(BUSINESS))


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
        body = page_head(h1, kick="Juridiskt") + f'''
<section class="wrap legal">
  <nav class="side-nav" aria-label="Juridiskt"><p class="kick">Juridiskt</p><ul>{nav}</ul></nav>
  <article class="prose">{content}
  <p class="updated">Senast uppdaterad 2026-10-28</p></article>
</section>'''
        page(name, f"{h1} | Hemmacykel", desc, body)


def not_found():
    body = page_head("Sidan finns inte", "Länken kan vara gammal eller felstavad.", current="404",
                     extra=f'<div class="btns">{btn("index.html", "Till startsidan")}{btn("boka.html", "Boka service", "btn-line", False)}</div>')
    page("404.html", "Sidan finns inte | Hemmacykel", "Sidan kunde inte hittas.", body)


PAGES = []


def sitemap():
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc><lastmod>{UPDATED}</lastmod></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    index()
    tjanster()
    for s in SERVICES:
        service_page(s)
    priser()
    boka()
    cyklar()
    for b in BIKES:
        bike_page(b)
    om_oss()
    omdomen()
    fragor()
    kontakt()
    legal()
    not_found()
    PAGES += sorted(p.name for p in OUT.glob("*.html") if p.name != "404.html")
    sitemap()
    print(f"Klart: {len(PAGES) + 1} sidor")
