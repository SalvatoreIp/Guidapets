# CLAUDE.md

Guida per Claude Code in questo repository.

## Cos'è

Sito Hugo `guidapets.com` (tema PaperMod come submodule in `themes/PaperMod`): blog italiano su cani, gatti, piccoli animali e acquari, con link affiliati Amazon. Pubblicato su Cloudflare Pages (progetto `guidapets`, upload diretto, NON collegato a Git). Repo `SalvatoreIp/Guidapets`.

## Comandi

Ciclo completo di pubblicazione:

```bash
cd /home/salvatore/guidapets && rm -rf public/ && hugo --minify \
  && npx wrangler pages deploy public --project-name guidapets --commit-dirty=true \
  && git add . && git commit -m "TITOLO" && git push
```

- wrangler legge `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID` da `.env` (gitignored): esportali prima (`set -a; . ./.env; set +a`).
- `scripts/salva_immagine.py URL SLUG` — salva un'immagine ElevenLabs (URL firmato, scade in ~2 h) come `static/immagini/SLUG.jpg` a 1280 px.
- Pubblicazione automatica: cron della VPS alle 10:05 → `scripts/daily_publish_vps.sh` (prompt in `scripts/daily_publish_prompt.txt`), log in `logs/daily_publish.log`.

## Struttura contenuti

- Sezioni registrate (`hugo.toml` `mainSections` + menu): `cani`, `gatti`, `salute`, `prodotti`, `piccoli-animali`, `acquari`. Non crearne altre.
- Un file Markdown per articolo in `content/<sezione>/<slug>.md` (nessuna data nel nome file). URL: `https://guidapets.com/<sezione>/<slug>/`.
- Immagini in `static/immagini/`, referenziate come `/immagini/<slug>.jpg`.
- `OPENCLAW.ISTRUZIONI*.md` sono le vecchie istruzioni per OpenClaw (Pixabay, Pinterest): storiche, non vincolanti per il cron.

Frontmatter obbligatorio (sempre virgolette doppie):

```yaml
---
title: "..."
date: YYYY-MM-DDTHH:MM:SS+02:00
draft: false
description: "120-155 caratteri"
categories: ["<sezione>"]
tags: ["tag1", "tag2", "tag3"]
cover:
  image: "/immagini/slug.jpg"
  alt: "..."
---
```

## Regole editoriali

- Italiano, 900-1400 parole, testo originale. Tono concreto e credibile, da persona competente a padrone: fatti, numeri (grammi, giorni, euro, età), cosa fare e quando serve il veterinario. Niente linguaggio sdolcinato o "puccioso" (no "batuffolo", "piccolo amico a quattro zampe", "coccole", "amore incondizionato", "musetto"), niente frasi a effetto o esclamative. Il lettore deve pensare "questa è un'informazione che mi serve".
- Struttura: paragrafo introduttivo `<p class="lead">…</p>` → box CTA → sezioni `##` che rispondono alla domanda di ricerca (cause, cosa fare, come scegliere, errori comuni) → tabella prodotti in Markdown quando l'argomento è commerciale → "Quando andare dal veterinario" per temi di salute → Conclusione → `*Fonti: ...*`.
- Box CTA dopo l'introduzione, verso una ricerca Amazon.it della categoria di prodotto:
  ```html
  <div class="cta-box">
    <a href="https://www.amazon.it/s?k=parole+chiave&tag=audiobookit-21" target="_blank" rel="nofollow sponsored" class="cta-button">🔍 Confronta ... su Amazon</a>
  </div>
  ```
- Tag affiliato: `audiobookit-21` (voluto, uguale su tutti i siti). Link Amazon di prodotto solo se trovati davvero su Amazon.it, mai ASIN inventati; altrimenti link di ricerca `amazon.it/s?k=...&tag=audiobookit-21`.
- Salute: mai dosi di farmaci, mai sostituirsi al veterinario; informazioni verificate su fonti veterinarie serie (ANMVI, università, ospedali veterinari, WSAVA). Prezzi datati ("prezzo indicativo settembre 2026").
- Slug: minuscolo e trattini, niente accenti né apostrofi. Una sola categoria. 2-3 link interni ad articoli correlati.
- Mai post di prova o bozze committati.
