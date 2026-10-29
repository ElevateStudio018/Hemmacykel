# Hemmacykel – ny webbplats

Ny webbplats för [Hemmacykel](https://hemmacykel.se/), mobil cykelverkstad i Uppsala. Allt innehåll, alla priser,
omdömen och bilder är hämtade från den nuvarande sajten (se [`scrape/`](scrape/)).

Designen bygger på förslag 7 i [`design/forslag/`](design/forslag/) ("Inramad med bokningsfält"):

- **Hanken Grotesk**, vit grund med ljusgrå rundade kort (22 px), svarta pill-knappar och Hemmacykels lime
  (`#6fd439`) för bokning. Skogsgrönt från loggan i det populäraste paketet och i avslutningen.
- Herobilden ligger inramad med rundade hörn under en vit meny, och undersidornas rubrikfält har samma ram.
- **Priskalkylator i heron**: välj tjänst eller paket och typ av cykel så visas uppskattat pris direkt. "Boka" tar
  med båda valen till bokningen (`boka.html?tjanst=…&typ=…`), som räknar vidare därifrån.

Slogan: **”Få vardagen att rulla igen.”** – rubriken i heron, återkommer i avslutningen.

[`Hemmacykel-ny-hemsida.pdf`](Hemmacykel-ny-hemsida.pdf) är ett förslag att skicka till kunden: försättsblad,
startsidan, mobilvyer, en tjänstesida, servicepaketen, cyklar till salu och en cykelsida, renderat direkt från `docs/`.

## Designförslag

[`design/forslag/`](design/forslag/) har sju förslag på startsidan, alla med heltäckande herobild och samma innehåll
som sajten. Öppna `design/forslag/index.html` för en översikt. Förslagen byggs med `python3 design/forslag/build.py`
och hämtar priser, omdömen, FAQ och cyklar från `scripts/build.py`.

1. Mörk klassiker – Geist, mörk toning från vänster, faktarad i botten
2. Vit panel – Manrope, vit innehållspanel på bilden
3. Centrerad med snabbval – Instrument Sans, snabbknappar med pris till bokningen
4. Redaktionell – Inter Tight, jättestor rubrik över hela bredden
5. Skogsgrön – Fraunces + Inter, bilden tonad i loggans gröna
6. Sportig – Barlow Condensed, versaler och lime
7. Inramad med bokningsfält – Hanken Grotesk, rundad bild och bokningsfält som en sökruta

## Sidor

Allt ligger i [`docs/`](docs/) och behöver inga verktyg – öppna `docs/index.html` i en webbläsare.
Mappen kan publiceras direkt med GitHub Pages (Settings → Pages → `main` / `docs`) eller valfritt webbhotell.
Alla sidor har samma meny (Tjänster med rullgardin, Priser, Cyklar till salu, Omdömen, Om oss, Kontakt) och sidfot.

| Sida | Innehåll |
| --- | --- |
| `index.html` | Hero med priskalkylator, tjänster, paket, så funkar det, om oss, omdömen, tipsa en kompis, cyklar, frågor |
| `tjanster.html` | Alla tjänster, servicepaket, tillägg per cykeltyp, så funkar det |
| `tjanst-punktering.html`, `tjanst-dackbyte.html`, `tjanst-kedjebyte.html`, `tjanst-bromsar.html` | En sida per tjänst: tecken på att det är dags, vad som ingår, pris med bokningsknapp, frågor, fler tjänster |
| `tjanst-service.html` | Servicepaketen med jämförelsetabell |
| `tjanst-elcykel.html` | Elcykel och specialcyklar med tillägg per cykeltyp |
| `priser.html` | Hela prislistan med tillägg och reseavgift, priskalkylator, hur betalningen går till |
| `boka.html` | Bokning i tre steg med prisberäkning och veckokalender |
| `cyklar.html` | Cyklar till salu – sålda visas suddiga med en "Såld"-märkning |
| `cykel-*.html` | En sida per cykel: bildgalleri med miniatyrer, fakta, vad som är gjort, utrustning, kontakt för köp |
| `om-oss.html` | Grundarna, varför Hemmacykel finns, vad de står för, hur de jobbar |
| `omdomen.html` | Snittbetyg, vad kunderna nämner, alla omdömen, länk för att lämna omdöme |
| `fragor.html` | Alla frågor i fem kategorier |
| `kontakt.html` | Telefon, e-post, adress, tider, kontaktformulär (öppnar mejl), områden |
| `integritetspolicy.html`, `villkor.html`, `cookies.html`, `404.html` | Juridik och felsida |

Priskalkylatorn (startsidan och prissidan), tjänstesidornas prisrader och paketknapparna skickar valen till
`boka.html?tjanst=…&typ=…`, som förväljer dem. Gamla länkar från ensidesversionen (`index.html#boka`,
`index.html#merida-2670` osv.) skickas vidare till rätt sida.

## Ändra innehåll

Sidorna genereras av [`scripts/build.py`](scripts/build.py). Ändra där och kör:

```sh
python3 scripts/build.py
```

- **Priser, tjänster, paket, FAQ, omdömen, kontaktuppgifter**: konstanterna högst upp i `build.py`.
- **Tjänstesidorna**: `SERVICES` i `build.py`. Texterna om tecken och vad som ingår är skrivna utifrån
  hemmacykel.se och bör stämmas av med Hemmacykel innan lansering.
- **Cyklar till salu**: [`scripts/cyklar.json`](scripts/cyklar.json). Lägg bilderna i `docs/img/cyklar/`,
  sätt `"sold": true` när en cykel är såld – då blir bilderna suddiga och märks "Såld". Varje cykel får en
  egen sida (`cykel-<id>.html`). Cyklar till salu visas först.
- **Stil**: `docs/assets/site.css`. **Meny, bildgallerier, bokning**: `docs/assets/site.js`.

## Att tänka på innan lansering

- **Bokningen skickas via e-post.** Sista steget öppnar ett ifyllt mejl till hemmacykel@gmail.com (samma upplägg
  som på våra andra sajter). Den gamla sajten sparade bokningar i Supabase via Lovable. Ska bokningarna hamna i
  samma system eller en formulärtjänst (Formspree, Netlify Forms) byter man ut `submit`-hanteraren i `site.js`.
- **Omdömena är statiska.** Originalet hämtade dem live från Google. Uppdatera `RATING`, `REVIEW_COUNT` och
  `REVIEWS` i `build.py` när nya omdömen kommer in.
- **Cyklarna är statiska.** Originalet läste annonserna från en databas. Skeppshult-cykeln var den enda som var
  till salu vid skrapningen.
- **Juridiska texter är kopierade ordagrant.** De beskriver fortfarande Google Ads med samtyckesbanner, AI-analys
  och chatt samt underleverantörerna Lovable, Supabase, Resend och OpenAI. Den nya sajten har ingen av dessa –
  texterna behöver uppdateras (eller funktionerna läggas till) innan lansering.
- **Tider i bokningen** följer öppettiderna på sajten: vardagar 15–19 (eftermiddag), helger 9–13 och 13–19.
  Originalets bokning visade förmiddag även på vardagar.
- Bilderna på tjänstekorten är detaljbilder från Hemmacykels egna cykelannonser. Byt gärna mot bilder från riktiga
  servicejobb när de finns.
