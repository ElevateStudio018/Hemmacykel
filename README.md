# Hemmacykel – ny webbplats

Ny webbplats för [Hemmacykel](https://hemmacykel.se/), mobil cykelverkstad i Uppsala. Allt innehåll, alla priser,
omdömen och bilder är hämtade från den nuvarande sajten (se [`scrape/`](scrape/)).

Designen är redaktionell och stram:

- Ett typsnitt, **Geist** (Geist Mono för små etiketter och priser), stor rubriktypografi med tät spärrning.
- 12-kolumners grid där varje sektion har etikett till vänster och innehåll till höger, hårlinjer i stället för
  kort, skuggor och ikonrutor. Inga scroll-animationer.
- Varm off-white bakgrund, skogsgrönt från Hemmacykels logga för de mörka partierna (om oss, slut-CTA, footer)
  och deras lime (`#6fd439`) bara på knappar och små markeringar.
- Tjänster och priser är en enda lista; på desktop byter bilden bredvid när man pekar på en rad.

Slogan: **”Få vardagen att rulla igen.”** – rubriken i heron, återkommer i slut-CTA:n.

[`Hemmacykel-ny-hemsida.pdf`](Hemmacykel-ny-hemsida.pdf) är ett förslag att skicka till kunden: försättsblad,
startsidan, mobilvyer, bokningen och cyklar till salu, renderat direkt från sajten i `docs/`.

## Sidor

Allt ligger i [`docs/`](docs/) och behöver inga verktyg – öppna `docs/index.html` i en webbläsare.
Mappen kan publiceras direkt med GitHub Pages (Settings → Pages → `main` / `docs`) eller valfritt webbhotell.

- `index.html` – startsidan: hero, tjänster och priser, servicepaket, så funkar det, om oss,
  **omdömen** (Google-betyg + kundcitat), tipsa en kompis, cyklar till salu, FAQ
- `boka.html` – bokning i tre steg med prisberäkning och veckokalender
- `cyklar.html` – begagnade cyklar med bildgalleri per cykel
- `integritetspolicy.html`, `villkor.html`, `cookies.html`, `404.html`

## Ändra innehåll

Sidorna genereras av [`scripts/build.py`](scripts/build.py). Ändra där och kör:

```sh
python3 scripts/build.py
```

- **Priser, tjänster, paket, FAQ, omdömen, kontaktuppgifter**: konstanterna högst upp i `build.py`.
- **Cyklar till salu**: [`scripts/cyklar.json`](scripts/cyklar.json). Lägg bilderna i `docs/img/cyklar/`,
  sätt `"sold": true` när en cykel är såld. Cyklar till salu visas först.
- **Stil**: `docs/assets/site.css`. **Meny, karuseller, bokning**: `docs/assets/site.js`.

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
