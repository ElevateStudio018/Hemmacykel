# Hemmacykel – ny webbplats

Ny webbplats för [Hemmacykel](https://hemmacykel.se/), mobil cykelverkstad i Uppsala. Allt innehåll, alla priser,
omdömen och bilder är hämtade från den nuvarande sajten (se [`scrape/`](scrape/)).

Designen blandar två av våra tidigare sajter:

- **Ängö Entreprenad** (`angoentreprenad`): Outfit + DM Sans, eyebrows med accentstreck, tjänstekort med pil,
  statistikrad, foto med förskjuten färgplatta, FAQ i två spalter, CTA-band med streckad kant, mörk footer.
- **Bloms El & Data** (`Bloms-el-och-data`): fotohero med kort som överlappar nedre kanten, solid toppbar i
  varumärkesfärgen, mer "koncern"-känsla.

Färgerna kommer från Hemmacykels egen logga/favicon (skogsgrön + cream) med deras lime (`#6fd439`) som accent.

Slogan: **”Få vardagen att rulla igen.”** – i heron, footern och CTA-bandet.

[`Hemmacykel-ny-hemsida.pdf`](Hemmacykel-ny-hemsida.pdf) är ett förslag att skicka till kunden: försättsblad,
startsidan, mobilvyer, bokningen och cyklar till salu, renderat direkt från sajten i `docs/`.

## Sidor

Allt ligger i [`docs/`](docs/) och behöver inga verktyg – öppna `docs/index.html` i en webbläsare.
Mappen kan publiceras direkt med GitHub Pages (Settings → Pages → `main` / `docs`) eller valfritt webbhotell.

- `index.html` – startsidan: hero, tjänster, om oss, servicepaket, så funkar det, prislista,
  **omdömen** (Google-betyg + kundcitat i karusell), tipsa en kompis, cyklar till salu, FAQ
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
