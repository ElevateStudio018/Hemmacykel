"""Sju förslag på startsidan, alla med heltäckande herobild. Kör: python3 design/forslag/build.py

Innehållet (priser, omdömen, FAQ, cyklar) hämtas från scripts/build.py så att förslagen alltid
visar samma sak som sajten. Bilder och bokning länkar till ../../docs/.
"""
import importlib.util
from pathlib import Path

# Elevate Studio's credit under every footer: the mark and the name, the whole of it one link to elevatestudio.nu.
ELEVATE_CREDIT = '''<!-- elevate-credit -->
<style>.elevate-credit{max-width:1240px;margin:24px auto 0;padding:20px 16px 0;border-top:1px solid rgba(128,128,128,.25);display:flex;justify-content:center;box-sizing:border-box}.elevate-credit a{display:inline-flex;align-items:center;gap:10px;padding:8px 0;font:inherit;font-size:15px;line-height:1;color:inherit;opacity:.55;text-decoration:none;transition:opacity .2s}.elevate-credit a:hover,.elevate-credit a:focus-visible{opacity:1}.elevate-credit svg{width:20px;height:20px;flex:none;display:block}@media(min-width:1024px){.elevate-credit a{font-size:16px}}</style>
<div class="elevate-credit"><a href="https://elevatestudio.nu" target="_blank" rel="noopener"><svg viewBox="0 0 1884.3 1353.9" aria-hidden="true"><path d="M0.0 1353.9 L1218.7 0.0 L1218.7 329.1 L479.7 1136.4 L786.7 1132.4 L1215.5 687.4 L1884.3 1349.9 L1590.1 1349.9 L1218.6 994.7 L865.4 1349.9Z" fill="currentColor"/></svg>Byggd av Elevate Studio</a></div>
'''


OUT = Path(__file__).parent
ROOT = OUT.parent.parent
spec = importlib.util.spec_from_file_location("site", ROOT / "scripts" / "build.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
e, kr = S.e, S.kr

IMG = "../../docs/img/"
BOKA = "../../docs/boka.html"
HERO_IMG = IMG + "hemmacykel-hero.jpg"
KICK = "Mobil cykelservice i Uppsala"
H1 = "Få vardagen att rulla igen."
LEAD = "Vi kommer hem till dig och fixar cykeln där den står. Fasta priser, inga gömda avgifter."
FACTS = [("★ 5,0", "13 omdömen på Google"), ("Från 199 kr", "Fasta priser inkl. moms"), ("7 dagar i veckan", "Vardagar 15–19, helger 9–19")]
QUICK = [("punktering", "Punktering", 299), ("dackbyte", "Däckbyte", 349), ("kedjebyte", "Kedjebyte", 299), ("cykelcheck", "Cykelcheck", 499)]
NAV = [("tjanster", "Tjänster"), ("paket", "Paket"), ("omdomen", "Omdömen"), ("om-oss", "Om oss"), ("fragor", "Frågor")]
ARR = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
TEL = f'<a class="btn btn-g" href="tel:{S.TEL}">Ring {S.PHONE}</a>'
BOOK = f'<a class="btn btn-p" href="{BOKA}">Boka service {ARR}</a>'

TILES = [  # (bokningsvärde, rubrik, text, pris, bild)
    ("punktering", "Punktering", "Vi lagar eller byter slang på plats.", "299 kr", "tjanst-punktering.jpg"),
    ("dackbyte", "Däckbyte", "Byte av däck, fram eller bak.", "349 kr", "tjanst-dack.jpg"),
    ("kedjebyte", "Kedjebyte", "Byte och service av kedja.", "299 kr", "tjanst-kedja.jpg"),
    ("bromsjustering", "Bromsar", "Justering, nya klossar eller ny vajer.", "från 199 kr", "tjanst-bromsar.jpg"),
    ("cykelcheck", "Service", "Genomgång och säkerhetskontroll av hela cykeln.", "från 499 kr", "tjanst-service.jpg"),
    ("ovrigt", "Övrigt", "Något annat? Beskriv problemet så ger vi ett prisförslag.", "Prisförslag", "tjanst-ovrigt.jpg"),
]


def nav(light=True):
    mark = "logo-mark-vit.png" if light else "logo-mark.png"
    links = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in NAV)
    return (f'<nav class="topnav"><div class="wrap"><a class="logo" href="#"><img src="{IMG}{mark}" alt="" width="34" height="30">Hemmacykel</a>'
            f'<ul>{links}</ul><a class="btn btn-p btn-s" href="{BOKA}">Boka service</a></div></nav>')


def facts_html(cls="facts"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in FACTS) + "</dl>"


def sections(about_dark=True):
    tiles = "".join(
        f'<a href="{BOKA}?{"paket" if v == "cykelcheck" else "tjanst"}={v}"><img src="{IMG}{img}" alt="" loading="lazy">'
        f'<span class="t"><span class="row"><b>{n}</b><span class="pr">{p}</span></span><small>{d}</small></span></a>'
        for v, n, d, p, img in TILES)
    plans = "".join(
        f'''<article{' class="hl"' if slug == S.FEATURED else ""}><div class="top"><h3>{name}</h3>{'<span class="tag">Populärast</span>' if slug == S.FEATURED else ""}</div>
<p class="for">{for_who}</p><p class="amt">{price}<span>kr</span></p>
<ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul><a class="btn {"btn-p" if slug == S.FEATURED else "btn-o"}" href="{BOKA}?paket={slug}">Boka {name}</a></article>'''
        for slug, name, price, for_who, items in S.PACKAGES)
    steps = "".join(f'<li><span class="n">0{i + 1}</span><h3>{t}</h3><p>{s}</p></li>' for i, (t, s) in enumerate(S.STEPS))
    reviews = "".join(f'<figure><span class="st">★★★★★</span><blockquote>”{e(t)}”</blockquote><figcaption><b>{e(n)}</b> · Google</figcaption></figure>'
                      for n, t in S.REVIEWS[:6])
    bikes = "".join(
        f'''<a class="{"sold" if b["sold"] else ""}" href="../../docs/{b["file"]}"><span class="ph"><img src="{IMG}cyklar/{b["images"][0]}" alt="{e(b["title"])}" loading="lazy">
<span class="state">{"Såld" if b["sold"] else "Till salu"}</span></span><span class="row"><b>{e(b["title"])}</b><span class="pr">{kr(b["price"])}</span></span><small>{e(b["size"])} · {e(b["condition"])}</small></a>'''
        for b in S.BIKES[:3])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in S.FAQ[:6])
    return f'''
<section class="sec" id="tjanster"><div class="wrap">
  <div class="sh"><div><p class="kick">Tjänster och priser</p><h2>Fast pris på det vanligaste.</h2></div><p>Du ser alltid priset innan vi börjar. Priserna gäller inklusive moms, arbete och material.</p></div>
  <div class="svc">{tiles}</div>
  <p class="note">Elcykel, lådcykel och andra tyngre cyklar +50 kr · elsparkcykel +100 kr · reseavgift 50 kr vid över 15 min körtid, 100 kr vid över 25 min.</p>
</div></section>
<section class="sec alt" id="paket"><div class="wrap">
  <div class="sh"><div><p class="kick">Servicepaket</p><h2>Hela cykeln genomgången, till fast pris.</h2></div><p>Välj rätt nivå direkt och slipp gömda avgifter eller oväntade tillägg.</p></div>
  <div class="pk">{plans}</div>
</div></section>
<section class="sec" id="sa-funkar-det"><div class="wrap">
  <div class="sh"><div><p class="kick">Så funkar det</p><h2>Från trasig till rullande på tre steg.</h2></div></div>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="sec {"dark" if about_dark else "alt"}" id="om-oss"><div class="wrap about">
  <img src="{IMG}hemmacykel-team.jpg" alt="Grundarna av Hemmacykel vid Ångströmlaboratoriet, Uppsala" loading="lazy">
  <div><p class="kick">Om oss</p><h2>Två unga entreprenörer från Uppsala.</h2>
    <p>Vi startade Hemmacykel för att ge Uppsalabor mer tid och mindre krångel. En bokning, en tid som passar dig, och sedan fungerar cykeln igen.</p>
    <p>Cykeln tar dig till jobbet, träningen, kompisarna och familjen. Därför ska cykelservice passa din vardag – inte tvärtom.</p>
    <ul class="facts2"><li><small>Område</small>Hela Uppsala</li><li><small>Tider</small>Vardagar 15–19, helger 9–19</li>
    <li><small>Cyklar</small>Vanliga, el, låd, fatbike</li><li><small>Betalning</small>Swish på plats</li></ul></div>
</div></section>
<section class="sec" id="omdomen"><div class="wrap">
  <div class="sh"><div><p class="kick">Omdömen</p><h2>Vad kunderna i Uppsala säger.</h2></div>
    <div class="score"><b>{S.RATING}</b><span><span class="st">★★★★★</span>{S.REVIEW_COUNT} omdömen på Google<br><a href="{S.MAPS}" target="_blank" rel="noopener">Läs alla</a></span></div></div>
  <div class="rv">{reviews}</div>
</div></section>
<section class="sec alt" id="cyklar"><div class="wrap">
  <div class="sh"><div><p class="kick">Cyklar till salu</p><h2>Begagnat, genomgånget och redo att rulla.</h2></div><a class="more" href="../../docs/cyklar.html">Alla cyklar</a></div>
  <div class="bikes">{bikes}</div>
</div></section>
<section class="sec" id="fragor"><div class="wrap faq">
  <div><p class="kick">Vanliga frågor</p><h2>Frågor och svar.</h2><p class="muted">Hittar du inte svaret? Ring <a href="tel:{S.TEL}">{S.PHONE}</a>.</p></div>
  <div class="qa">{faq}</div>
</div></section>
<section class="cta"><div class="wrap"><div><h2>Redo att få cykeln fixad?</h2><p>Boka en tid – vi kommer till dig.</p></div><div class="btns">{BOOK}{TEL}</div></div></section>
<footer class="foot"><div class="wrap"><span>© 2026 Hemmacykel · {S.STREET}, {S.ZIP_CITY} · Hobbyverksamhet</span><span><a href="tel:{S.TEL}">{S.PHONE}</a> · <a href="mailto:{S.MAIL}">{S.MAIL}</a></span></div>{ELEVATE_CREDIT}</footer>'''


BASE = """
*,*::before,*::after{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--f-body);-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}a{color:inherit}p{margin:0}
h1,h2,h3{margin:0;font-family:var(--f-head);font-weight:var(--hw);letter-spacing:var(--ht);line-height:1.04;text-transform:var(--htt,none);text-wrap:balance}
h2{font-size:var(--h2,clamp(2rem,3.8vw,3.1rem))}
h3{font-size:1.3rem;line-height:1.2}
.wrap{max-width:1240px;margin:0 auto;padding-inline:clamp(20px,4vw,40px)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;height:54px;padding:0 26px;border-radius:var(--br);font:600 16px/1 var(--f-body);text-decoration:none;border:1.5px solid transparent;white-space:nowrap;transition:background-color .2s,border-color .2s,color .2s,transform .2s}
.btn svg{transition:transform .2s}.btn:hover svg{transform:translateX(3px)}
.btn-s{height:44px;padding:0 20px;font-size:15px}
.btn-p{background:var(--accent);color:var(--accent-ink)}.btn-p:hover{background:var(--accent-h)}
.btn-g{border-color:rgba(255,255,255,.5);color:#fff}.btn-g:hover{border-color:#fff}
.btn-o{border-color:var(--line-s);color:var(--ink)}.btn-o:hover{border-color:var(--ink)}
.kick{font:600 13px/1.3 var(--f-body);letter-spacing:.1em;text-transform:uppercase;color:var(--kick)}
.muted{color:var(--muted)}
.st{color:var(--star);letter-spacing:2px;font-size:14px}

.topnav{position:absolute;top:0;left:0;right:0;z-index:5;color:#fff}
.topnav .wrap{display:flex;align-items:center;gap:36px;height:88px}
.logo{display:flex;align-items:center;gap:10px;font:700 19px/1 var(--f-head);letter-spacing:-.02em;text-transform:none;text-decoration:none;margin-right:auto}
.logo img{width:34px;height:30px}
.topnav ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px;font-weight:500}
.topnav ul a{text-decoration:none;opacity:.85;transition:opacity .2s}.topnav ul a:hover{opacity:1}

.hero{position:relative;isolation:isolate;color:#fff;min-height:max(660px,100svh);display:flex;flex-direction:column;overflow:hidden;background:#111}
.hero-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:var(--hpos,62% 28%);z-index:-2}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:var(--shade)}
.hero h1{font-size:var(--h1,clamp(3.2rem,7vw,6.2rem));line-height:var(--h1l,.98);letter-spacing:var(--h1t,var(--ht))}
.hero .lead{font-size:clamp(1.08rem,1.4vw,1.25rem);line-height:1.5;max-width:40ch;opacity:.88}
.btns{display:flex;flex-wrap:wrap;gap:12px}

.sec{padding-block:clamp(80px,10vw,136px)}
.sec.alt{background:var(--bg-alt)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:40px;margin-bottom:clamp(36px,4vw,56px)}
.sh h2{max-width:16ch}.sh .kick{margin-bottom:16px}
.sh>p{max-width:40ch;color:var(--muted)}
.more{font-weight:600;text-decoration:none;white-space:nowrap;border-bottom:1.5px solid currentColor;padding-bottom:2px}

.svc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--g)}
.svc a{display:flex;flex-direction:column;text-decoration:none;background:var(--card);border:var(--card-bd);border-radius:var(--r);overflow:hidden;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
.svc a:hover{transform:translateY(-4px)}
.svc img{width:100%;aspect-ratio:16/10;object-fit:cover}
.svc .t{display:grid;gap:4px;padding:var(--pad,20px 22px 24px)}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.svc b,.bikes b{font:var(--hw) 1.22rem/1.2 var(--f-head);letter-spacing:var(--h3t,-.015em);text-transform:var(--htt,none)}
.pr{font-weight:600;white-space:nowrap;color:var(--price,var(--ink))}
.svc small,.bikes small{color:var(--muted);font-size:15px}
.note{margin-top:28px;font-size:14.5px;color:var(--muted)}

.pk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--g)}
.pk article{display:flex;flex-direction:column;background:var(--card);border:var(--card-bd);border-radius:var(--r);padding:34px 32px}
.pk .top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.pk .tag,.state{font:700 11.5px/1 var(--f-body);letter-spacing:.08em;text-transform:uppercase;background:var(--tag);color:var(--tag-ink);padding:7px 10px;border-radius:var(--br)}
.pk .for{color:var(--muted);font-size:15px;margin-top:6px;min-height:3.2em}
.pk .amt{font:var(--hw) clamp(2.8rem,4vw,3.6rem)/1 var(--f-head);letter-spacing:-.04em;margin-top:28px}
.pk .amt span{font-size:1.05rem;letter-spacing:0;margin-left:6px;opacity:.6}
.pk ul{list-style:none;padding:0;margin:26px 0 30px;display:grid;gap:9px;font-size:15px}
.pk li{display:flex;gap:10px}.pk li::before{content:"✓";color:var(--check);font-weight:700}
.pk .btn{margin-top:auto}
.pk .hl{background:var(--hl);color:var(--hl-ink);border-color:transparent}
.pk .hl .for{color:inherit;opacity:.7}.pk .hl li::before{color:var(--hl-check,var(--accent))}

.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--g)}
.steps li{border-top:2px solid var(--ink);padding-top:22px}
.steps .n{font:600 14px var(--f-body);color:var(--muted)}
.steps h3{margin-top:36px;font-size:1.5rem}
.steps p{margin-top:10px;color:var(--muted);max-width:34ch}

.dark{background:var(--dark);color:var(--on-dark)}
.dark .kick,.dark p{color:var(--on-dark-2)}
.about{display:grid;grid-template-columns:1fr 1.05fr;gap:clamp(40px,7vw,104px);align-items:center}
.about img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 45%;border-radius:var(--r)}
.about h2{margin:16px 0 22px}.about p{max-width:50ch}.about p+p{margin-top:14px}
.about p:not(.kick){color:var(--muted)}.dark .about p:not(.kick){color:var(--on-dark-2)}
.facts2{list-style:none;margin:36px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:20px 28px}
.facts2 li{border-top:1px solid var(--line);padding-top:12px;font-weight:500}
.dark .facts2 li{border-color:rgba(255,255,255,.16)}
.facts2 small{display:block;font-size:13px;font-weight:400;color:var(--muted)}.dark .facts2 small{color:var(--on-dark-2)}

.score{display:flex;align-items:center;gap:18px;font-size:15px;color:var(--muted)}
.score>b{font:var(--hw) 4.6rem/1 var(--f-head);letter-spacing:-.05em;color:var(--ink)}
.score .st{display:block}.score a{color:var(--ink);font-weight:600}
.rv{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--g)}
.rv figure{margin:0;display:flex;flex-direction:column;gap:16px;background:var(--card);border:var(--card-bd);border-radius:var(--r);padding:28px}
.rv blockquote{margin:0;font-size:1.12rem;line-height:1.5}
.rv figcaption{margin-top:auto;font-size:14.5px;color:var(--muted)}.rv figcaption b{color:var(--ink);font-weight:600}

.bikes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--g)}
.bikes a{display:grid;gap:6px;text-decoration:none}
.bikes .ph{position:relative;border-radius:var(--r);overflow:hidden;margin-bottom:10px}
.bikes img{width:100%;aspect-ratio:4/3;object-fit:cover;transition:transform .6s}
.bikes a:hover img{transform:scale(1.03)}
.state{position:absolute;top:12px;left:12px}
.sold .state{background:var(--bg);color:var(--ink)}
.sold .pr{text-decoration:line-through;color:var(--muted)}

.faq{display:grid;grid-template-columns:1fr 1.5fr;gap:clamp(36px,7vw,104px)}
.faq h2{margin:16px 0 18px}
.qa{border-top:1px solid var(--line)}
.qa details{border-bottom:1px solid var(--line)}
.qa summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 0;font-weight:600;font-size:1.1rem}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";font-size:1.6rem;font-weight:300;line-height:1;transition:transform .25s}
.qa details[open] summary::after{transform:rotate(45deg)}
.qa details p{padding:0 40px 22px 0;color:var(--muted)}

.cta{background:var(--dark);color:var(--on-dark);padding-block:clamp(80px,10vw,136px)}
.cta .wrap{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;flex-wrap:wrap}
.cta h2{font-size:var(--h2c,clamp(2.4rem,5vw,4.2rem));max-width:13ch}
.cta p{color:var(--on-dark-2);margin-top:14px;font-size:1.1rem}
.foot{background:var(--dark);color:var(--on-dark-2);font-size:14px;border-top:1px solid rgba(255,255,255,.1)}
.foot .wrap{display:flex;justify-content:space-between;gap:12px 24px;flex-wrap:wrap;padding-block:26px}
.foot a{text-decoration:none}.foot a:hover{color:var(--on-dark)}

@media (max-width:960px){
  .topnav ul{display:none}
  .svc,.rv,.bikes{grid-template-columns:1fr 1fr}
  .pk,.steps{grid-template-columns:1fr}.pk .for{min-height:0}
  .about,.faq{grid-template-columns:1fr}
  .sh{flex-direction:column;align-items:flex-start;gap:16px}
}
@media (max-width:600px){
  .svc,.rv,.bikes{grid-template-columns:1fr}
  .topnav .wrap{height:72px}
  .hero .btns .btn,.cta .btn{width:100%}
  .facts2{grid-template-columns:1fr}
}
"""

# --- de sju förslagen ------------------------------------------------------------------
V = {}

V[1] = dict(
    name="Mörk klassiker", desc="Helbild med mörk toning från vänster, rubrik nere till vänster och faktarad längst ner. Geist, lime knappar.",
    fonts="family=Geist:wght@400;500;600;700",
    vars="--f-head:'Geist',sans-serif;--f-body:'Geist',sans-serif;--hw:600;--ht:-.04em;--bg:#f5f4f0;--bg-alt:#ecebe5;--ink:#121513;--muted:#646a64;--line:rgba(18,21,19,.12);--line-s:rgba(18,21,19,.2);"
         "--accent:#6fd439;--accent-h:#82df4f;--accent-ink:#121513;--kick:#4c7a3a;--star:#e9a514;--card:#fff;--card-bd:1px solid rgba(18,21,19,.06);--r:12px;--br:999px;--g:20px;"
         "--tag:#6fd439;--tag-ink:#121513;--check:#3e8f1f;--hl:#15281c;--hl-ink:#fff;--dark:#15281c;--on-dark:#eef2ee;--on-dark-2:rgba(238,242,238,.66);"
         "--shade:linear-gradient(90deg,rgba(9,14,10,.85) 0%,rgba(9,14,10,.55) 45%,rgba(9,14,10,.1) 80%),linear-gradient(0deg,rgba(9,14,10,.75),transparent 45%)",
    css="""
.v1 .hero-c{margin-top:auto;padding-bottom:48px}
.v1 .hero .kick{color:#b9e89d}
.v1 .hero h1{max-width:11ch;margin:20px 0 26px}
.v1 .hero .btns{margin-top:34px}
.v1 .facts{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin:0;padding:22px 0 36px;border-top:1px solid rgba(255,255,255,.22)}
.v1 .facts dt{font-weight:600;font-size:1.1rem}.v1 .facts dd{margin:2px 0 0;font-size:14.5px;opacity:.7}
@media (max-width:600px){.v1 .facts{grid-template-columns:1fr;gap:10px}}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-c"><p class="kick">{KICK}</p><h1>{H1}</h1><p class="lead">{LEAD}</p><div class="btns">{BOOK}{TEL}</div></div>
<div class="wrap">{facts_html()}</div></header>''')

V[2] = dict(
    name="Vit panel", desc="Helbild med en vit innehållspanel nere till vänster. Lugnt och vänligt, Manrope och skogsgröna knappar.",
    fonts="family=Manrope:wght@400;500;600;700;800",
    vars="--f-head:'Manrope',sans-serif;--f-body:'Manrope',sans-serif;--hw:700;--ht:-.035em;--bg:#fff;--bg-alt:#f2f4f1;--ink:#14211a;--muted:#5f6b63;--line:#e3e7e2;--line-s:#cfd6d0;"
         "--accent:#1f3a2a;--accent-h:#2b4d38;--accent-ink:#fff;--kick:#3f7a2b;--star:#e9a514;--card:#fff;--card-bd:1px solid #e3e7e2;--r:18px;--br:12px;--g:20px;"
         "--tag:#6fd439;--tag-ink:#14211a;--check:#3f7a2b;--hl:#1f3a2a;--hl-ink:#fff;--dark:#14211a;--on-dark:#eef3ef;--on-dark-2:rgba(238,243,239,.66);"
         "--shade:linear-gradient(180deg,rgba(8,14,10,.45) 0%,rgba(8,14,10,0) 22%,rgba(8,14,10,0) 60%,rgba(8,14,10,.35))",
    css="""
.v2 .hero{justify-content:flex-end}
.v2 .panel{background:#fff;color:var(--ink);border-radius:22px;padding:clamp(28px,3.4vw,44px);max-width:580px;margin:0 0 clamp(20px,4vw,48px)}
.v2 .panel h1{font-size:clamp(2.6rem,4.8vw,4.1rem);color:var(--accent);margin:14px 0 18px}
.v2 .panel .lead{opacity:1;color:var(--muted)}
.v2 .panel .btns{margin-top:28px}
.v2 .panel .btn-g{border-color:var(--line-s);color:var(--ink)}.v2 .panel .btn-g:hover{border-color:var(--ink)}
.v2 .panel .rate{display:flex;align-items:center;gap:10px;margin-top:24px;padding-top:20px;border-top:1px solid var(--line);font-size:14.5px;color:var(--muted)}
.v2 .panel .rate b{color:var(--ink)}
.v2 .alt .svc a,.v2 .alt .pk article:not(.hl){border-color:transparent}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap"><div class="panel"><p class="kick">{KICK}</p><h1>{H1}</h1><p class="lead">{LEAD}</p><div class="btns">{BOOK}{TEL}</div>
<p class="rate"><span class="st">★★★★★</span><b>{S.RATING}</b> · {S.REVIEW_COUNT} omdömen på Google</p></div></div></header>''')

V[3] = dict(
    name="Centrerad med snabbval", desc="Jämn mörk toning, allt centrerat och snabbknappar med pris direkt i heron som går till bokningen. Instrument Sans.",
    fonts="family=Instrument+Sans:wght@400;500;600;700",
    vars="--f-head:'Instrument Sans',sans-serif;--f-body:'Instrument Sans',sans-serif;--hw:600;--ht:-.035em;--bg:#f7f7f4;--bg-alt:#eeeee9;--ink:#111311;--muted:#62675f;--line:rgba(17,19,17,.12);--line-s:rgba(17,19,17,.2);"
         "--accent:#6fd439;--accent-h:#82df4f;--accent-ink:#111311;--kick:#62675f;--star:#e9a514;--card:#fff;--card-bd:0;--r:16px;--br:999px;--g:16px;"
         "--tag:#111311;--tag-ink:#fff;--check:#3e8f1f;--hl:#111311;--hl-ink:#fff;--dark:#111311;--on-dark:#f2f2ef;--on-dark-2:rgba(242,242,239,.62);"
         "--shade:radial-gradient(ellipse at 50% 55%,rgba(10,12,10,.45),rgba(10,12,10,.72))",
    css="""
.v3 .hero-c{margin:auto;text-align:center;display:flex;flex-direction:column;align-items:center;padding-block:120px 72px}
.v3 .hero .kick{color:rgba(255,255,255,.8)}
.v3 .hero h1{font-size:clamp(3.2rem,7.6vw,6.8rem);max-width:12ch;margin:22px 0 24px}
.v3 .hero .lead{margin-inline:auto}
.v3 .hero .btns{justify-content:center;margin-top:34px}
.v3 .quick{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:44px;list-style:none;padding:0}
.v3 .quick a{display:inline-flex;gap:8px;align-items:baseline;background:#fff;color:#111311;text-decoration:none;padding:10px 16px;border-radius:999px;font-size:15px;font-weight:500;transition:background-color .2s}
.v3 .quick a:hover{background:#6fd439}
.v3 .quick small{color:#62675f;font-size:13.5px}.v3 .quick a:hover small{color:#111311}
.v3 .rate{margin-top:26px;font-size:14.5px;color:rgba(255,255,255,.75)}
.v3 .sh{flex-direction:column;align-items:center;text-align:center}.v3 .sh>p{text-align:center}
.v3 .svc a{box-shadow:0 1px 2px rgba(0,0,0,.04)}.v3 .svc a:hover{box-shadow:0 18px 40px -20px rgba(0,0,0,.25)}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-c"><p class="kick">{KICK}</p><h1>{H1}</h1><p class="lead">{LEAD}</p><div class="btns">{BOOK}{TEL}</div>
<ul class="quick">{"".join(f'<li><a href="{BOKA}?{"paket" if v == "cykelcheck" else "tjanst"}={v}">{n}<small>{p} kr</small></a></li>' for v, n, p in QUICK)}</ul>
<p class="rate"><span class="st">★★★★★</span> {S.RATING} på Google · {S.REVIEW_COUNT} omdömen</p></div></header>''')

V[4] = dict(
    name="Redaktionell", desc="Jättestor rubrik som spänner över hela bredden längst ner på bilden. Inter Tight, svart och papper, raka hörn.",
    fonts="family=Inter+Tight:wght@400;500;600&family=Inter:wght@400;500;600",
    vars="--f-head:'Inter Tight',sans-serif;--f-body:'Inter',sans-serif;--hw:500;--ht:-.045em;--bg:#efede7;--bg-alt:#e6e3da;--ink:#0f100f;--muted:#5f625d;--line:rgba(15,16,15,.18);--line-s:rgba(15,16,15,.3);"
         "--accent:#0f100f;--accent-h:#2a2c29;--accent-ink:#fff;--kick:#5f625d;--star:#0f100f;--card:transparent;--card-bd:0;--r:2px;--br:2px;--g:28px;--pad:16px 0 0;"
         "--tag:#6fd439;--tag-ink:#0f100f;--check:#0f100f;--hl:#0f100f;--hl-ink:#efede7;--hl-check:#6fd439;--dark:#0f100f;--on-dark:#efede7;--on-dark-2:rgba(239,237,231,.6);"
         "--h2:clamp(2.2rem,4.6vw,3.8rem);--shade:linear-gradient(0deg,rgba(8,8,8,.82) 0%,rgba(8,8,8,.2) 48%,rgba(8,8,8,.2) 62%,rgba(8,8,8,.6) 100%)",
    css="""
.v4 .hero-top{margin-top:120px;display:flex;justify-content:flex-end}
.v4 .hero-top>div{max-width:380px;display:grid;gap:20px}
.v4 .hero-top .lead{font-size:1.1rem}
.v4 .hero-h{margin-top:auto}
.v4 .hero h1{font-size:clamp(3.4rem,10.4vw,10.5rem);letter-spacing:-.065em;line-height:.86;padding-bottom:36px;max-width:none}
.v4 .hero .btn-p{background:#fff;color:#0f100f}.v4 .hero .btn-p:hover{background:#6fd439}
.v4 .hero .kick{color:rgba(255,255,255,.75)}
.v4 .svc a{border-top:1px solid var(--ink);padding-top:16px;border-radius:0}.v4 .svc img{border-radius:2px}.v4 .svc a:hover{transform:none}.v4 .svc a:hover b{text-decoration:underline}
.v4 .pk article{border-top:1px solid var(--ink);border-radius:0;padding:28px 0 0}.v4 .pk .hl{padding:28px;border-top:0}
.v4 .rv figure{border-top:1px solid var(--ink);border-radius:0;padding:22px 0 0}.v4 .rv blockquote{font-family:'Inter Tight';font-size:1.35rem;line-height:1.3;letter-spacing:-.02em}
.v4 .steps h3{font-size:1.9rem}
@media (max-width:760px){.v4 .hero-top{justify-content:flex-start;margin-top:110px}}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-top"><div><p class="kick">{KICK}</p><p class="lead">{LEAD}</p><div class="btns">{BOOK}</div></div></div>
<div class="wrap hero-h"><h1>{H1}</h1></div></header>''')

V[5] = dict(
    name="Skogsgrön", desc="Bilden tonad i skogsgrönt från loggan, serif-rubrik med kursiv och crème. Varmt och premium. Fraunces + Inter.",
    fonts="family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@400;500;600",
    vars="--f-head:'Fraunces',serif;--f-body:'Inter',sans-serif;--hw:400;--ht:-.025em;--bg:#f4f0e6;--bg-alt:#ebe5d5;--ink:#1b2a20;--muted:#5f675f;--line:rgba(27,42,32,.14);--line-s:rgba(27,42,32,.25);"
         "--accent:#1d3324;--accent-h:#2a4733;--accent-ink:#f4f0e6;--kick:#7a6a3d;--star:#b88a2a;--card:#fbf8f1;--card-bd:1px solid rgba(27,42,32,.08);--r:4px;--br:999px;--g:20px;"
         "--tag:#d8e9c9;--tag-ink:#1b2a20;--check:#557a3a;--hl:#1d3324;--hl-ink:#f4f0e6;--hl-check:#a8d88a;--dark:#1d3324;--on-dark:#f4f0e6;--on-dark-2:rgba(244,240,230,.66);"
         "--shade:linear-gradient(90deg,rgba(18,34,24,.82),rgba(18,34,24,.35) 60%,rgba(18,34,24,.15)),linear-gradient(0deg,rgba(18,34,24,.6),transparent 50%)",
    css="""
.v5 .hero{background:#1d3324}
.v5 .hero-bg{mix-blend-mode:luminosity;opacity:.78}
.v5 .hero-c{margin:auto 0 0;padding-bottom:clamp(48px,7vw,96px)}
.v5 .hero .kick{color:#d8c999;letter-spacing:.14em}
.v5 .hero h1{font-size:clamp(3.4rem,7.4vw,6.6rem);font-weight:400;max-width:10ch;margin:22px 0 26px;color:#f4f0e6}
.v5 .hero h1 em{font-style:italic;color:#c9e3b0}
.v5 .hero .btn-p{background:#f4f0e6;color:#1d3324}.v5 .hero .btn-p:hover{background:#fff}
.v5 .hero .btns{margin-top:34px}
.v5 .rate{margin-top:30px;font-size:14.5px;color:rgba(244,240,230,.75)}.v5 .rate .st{color:#d8c999}
.v5 .pk .amt,.v5 .score>b{font-weight:400}
.v5 .rv blockquote{font-family:'Fraunces',serif;font-size:1.3rem;line-height:1.4}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-c"><p class="kick">{KICK}</p><h1>Få vardagen att <em>rulla</em> igen.</h1><p class="lead">{LEAD}</p><div class="btns">{BOOK}{TEL}</div>
<p class="rate"><span class="st">★★★★★</span> {S.RATING} på Google · {S.REVIEW_COUNT} omdömen</p></div></header>''')

V[6] = dict(
    name="Sportig", desc="Smal fet versalrubrik med lime, raka hörn och svart faktarad i botten. Energiskt. Barlow Condensed + Barlow.",
    fonts="family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600",
    vars="--f-head:'Barlow Condensed',sans-serif;--f-body:'Barlow',sans-serif;--hw:700;--ht:-.005em;--htt:uppercase;--h3t:0;--bg:#f2f2ee;--bg-alt:#e7e7e1;--ink:#0d0f0d;--muted:#5d625b;--line:rgba(13,15,13,.14);--line-s:rgba(13,15,13,.3);"
         "--accent:#6fd439;--accent-h:#82df4f;--accent-ink:#0d0f0d;--kick:#0d0f0d;--star:#0d0f0d;--card:#fff;--card-bd:0;--r:0;--br:0;--g:16px;"
         "--tag:#6fd439;--tag-ink:#0d0f0d;--check:#0d0f0d;--hl:#0d0f0d;--hl-ink:#fff;--dark:#0d0f0d;--on-dark:#f2f2ee;--on-dark-2:rgba(242,242,238,.62);"
         "--h2:clamp(2.6rem,5vw,4.4rem);--h2c:clamp(3rem,6vw,5.4rem);--shade:linear-gradient(90deg,rgba(6,7,6,.86),rgba(6,7,6,.45) 55%,rgba(6,7,6,.15)),linear-gradient(0deg,rgba(6,7,6,.5),transparent 40%)",
    css="""
.v6 .hero-c{margin:auto 0;padding-top:96px}
.v6 .hero h1{font-size:clamp(3.6rem,8.4vw,7.6rem);line-height:.88;max-width:11ch;margin:18px 0 26px}
.v6 .hero h1 mark{background:none;color:#6fd439}
.v6 .hero .kick{color:#6fd439;font-weight:600;letter-spacing:.16em}
.v6 .hero .btns{margin-top:32px}
.v6 .btn{text-transform:uppercase;letter-spacing:.06em;font-size:15px}
.v6 .kick{font-family:'Barlow Condensed';font-size:15px;font-weight:700;letter-spacing:.14em}
.v6 .facts{display:grid;grid-template-columns:repeat(3,1fr);margin:0;background:#0d0f0d}
.v6 .facts div{padding:22px clamp(20px,4vw,40px);border-right:1px solid rgba(255,255,255,.12)}.v6 .facts div:last-child{border-right:0}
.v6 .facts dt{font:700 1.5rem/1 'Barlow Condensed';text-transform:uppercase;color:#6fd439}.v6 .facts dd{margin:6px 0 0;font-size:14.5px;color:rgba(255,255,255,.7)}
.v6 .steps li{border-top:4px solid #6fd439}.v6 .steps .n{font:800 2.4rem/1 'Barlow Condensed';color:var(--ink)}.v6 .steps h3{margin-top:18px}
.v6 .score>b{font-weight:800}
.v6 .qa summary{font-family:'Barlow Condensed';text-transform:uppercase;font-size:1.35rem;letter-spacing:.01em}
@media (max-width:600px){.v6 .facts{grid-template-columns:1fr}.v6 .facts div{border-right:0;border-bottom:1px solid rgba(255,255,255,.12)}}
""",
    hero=lambda: f'''<header class="hero">{nav()}<img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-c"><p class="kick">{KICK}</p><h1>Få vardagen att <mark>rulla igen.</mark></h1><p class="lead">{LEAD}</p><div class="btns">{BOOK}{TEL}</div></div>
{facts_html()}</header>''')

V[7] = dict(
    name="Inramad med bokningsfält", desc="Bilden ligger inramad med rundade hörn under en ljus meny, med ett bokningsfält direkt i heron (som en sökruta). Hanken Grotesk.",
    fonts="family=Hanken+Grotesk:wght@400;500;600;700",
    vars="--f-head:'Hanken Grotesk',sans-serif;--f-body:'Hanken Grotesk',sans-serif;--hw:600;--ht:-.04em;--bg:#fff;--bg-alt:#f4f4f1;--ink:#161816;--muted:#646862;--line:#e7e7e3;--line-s:#d3d4cf;"
         "--accent:#161816;--accent-h:#30332f;--accent-ink:#fff;--kick:#646862;--star:#e9a514;--card:#f4f4f1;--card-bd:0;--r:22px;--br:999px;--g:16px;"
         "--tag:#6fd439;--tag-ink:#161816;--check:#3e8f1f;--hl:#1a2e21;--hl-ink:#fff;--hl-check:#6fd439;--dark:#1a2e21;--on-dark:#eef2ee;--on-dark-2:rgba(238,242,238,.64);"
         "--shade:linear-gradient(0deg,rgba(8,10,8,.78) 0%,rgba(8,10,8,.2) 55%,rgba(8,10,8,.05))",
    css="""
.v7 .topnav{position:relative;color:var(--ink)}
.v7 .topnav .wrap{height:76px}
.v7 .topnav .btn-p{background:var(--ink)}
.v7 .hero{margin:0 12px;border-radius:28px;min-height:max(600px,calc(100svh - 88px));justify-content:flex-end}
.v7 .hero-c{padding-bottom:clamp(24px,4vw,44px);display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:32px}
.v7 .hero h1{font-size:clamp(3rem,6.6vw,6rem);max-width:11ch;margin:16px 0 20px}
.v7 .hero .kick{color:rgba(255,255,255,.8)}
.v7 .quickform{display:flex;align-items:center;gap:6px;background:#fff;border-radius:999px;padding:6px 6px 6px 22px;color:var(--ink);min-width:min(460px,100%)}
.v7 .quickform label{display:grid;flex:1;min-width:0;font-size:12.5px;color:var(--muted);font-weight:500}
.v7 .quickform select{width:100%;min-width:0;text-overflow:ellipsis;font:500 16px var(--f-body);border:0;background:transparent;color:var(--ink);padding:2px 0;outline:none;cursor:pointer;-webkit-appearance:none;appearance:none}
.v7 .quickform .btn{height:52px;background:#6fd439;color:var(--ink)}.v7 .quickform .btn:hover{background:#82df4f}
.v7 .rate{margin-top:14px;font-size:14px;color:rgba(255,255,255,.78);text-align:right}
.v7 .sec{padding-block:clamp(72px,9vw,120px)}
.v7 .cta{margin:0 12px 12px;border-radius:28px}.v7 .foot{background:#fff;color:var(--muted);border:0}.v7 .foot a:hover{color:var(--ink)}
@media (max-width:860px){.v7 .hero-c{grid-template-columns:minmax(0,1fr)}.v7 .quickform{min-width:0;width:100%}.v7 .rate{text-align:left}.v7 .hero{margin:0 8px;border-radius:20px}.v7 .cta{margin:0 8px 8px;border-radius:20px}}
""",
    hero=lambda: f'''{nav(light=False)}<header class="hero"><img class="hero-bg" src="{HERO_IMG}" alt="Hemmacykel servar en cykel på plats i Uppsala" fetchpriority="high">
<div class="wrap hero-c"><div><p class="kick">{KICK}</p><h1>{H1}</h1><p class="lead">{LEAD}</p></div>
<div><form class="quickform" action="{BOKA}" method="get"><label>Vad behöver fixas?<select name="tjanst">{"".join(f'<option value="{v}">{n}{f" – {kr(p)}" if p else ""}</option>' for v, n, p in S.REPAIRS)}</select></label><button class="btn" type="submit">Boka {ARR}</button></form>
<p class="rate"><span class="st">★★★★★</span> {S.RATING} på Google · {S.REVIEW_COUNT} omdömen</p></div></div></header>''')


def page(n, v):
    return f'''<!doctype html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hemmacykel – förslag {n}: {v["name"]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{v["fonts"]}&display=swap">
<style>:root{{{v["vars"]}}}{BASE}{v["css"]}</style></head>
<body class="v{n}">
{v["hero"]()}
<main>{sections(about_dark=n in (1, 5, 6))}</main>
</body></html>
'''


def gallery():
    cards = "".join(f'''<a href="forslag-{n}.html"><img src="forslag-{n}.jpg" alt="Förslag {n}: {v["name"]}" loading="lazy">
<span><b>{n}. {v["name"]}</b><small>{v["desc"]}</small></span></a>''' for n, v in V.items())
    return f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hemmacykel – sju förslag</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&display=swap">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f3ee;color:#121513;font:400 16px/1.55 Geist,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
main{{max-width:1320px;margin:0 auto;padding:56px clamp(16px,4vw,48px) 96px}}
h1{{font-weight:500;font-size:clamp(2.4rem,5vw,4rem);letter-spacing:-.045em;line-height:1;margin:0}}
p.l{{color:#5f655f;margin:16px 0 48px;max-width:60ch}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:40px 24px}}
.g a{{text-decoration:none;color:inherit;display:grid;gap:14px}}
.g img{{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;border-radius:8px;border:1px solid rgba(0,0,0,.08);transition:transform .3s}}
.g a:hover img{{transform:translateY(-3px)}}
.g b{{display:block;font-weight:500;font-size:1.2rem;letter-spacing:-.02em}}.g small{{color:#5f655f;font-size:14.5px}}
@media (max-width:440px){{.g{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>Sju förslag på startsidan</h1>
<p class="l">Alla har heltäckande herobild och samma innehåll som sajten – priser, paket, omdömen, cyklar och FAQ. Klicka för att öppna hela sidan.</p>
<div class="g">{cards}</div></main></body></html>
'''


if __name__ == "__main__":
    for n, v in V.items():
        (OUT / f"forslag-{n}.html").write_text(page(n, v), encoding="utf-8")
    (OUT / "index.html").write_text(gallery(), encoding="utf-8")
    print(f"{len(V)} förslag + index.html")
