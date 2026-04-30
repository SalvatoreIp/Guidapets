# Istruzioni Operative - Sito GuidaPets

## SEZIONI DISPONIBILI
- cani            -> razze, alimentazione, addestramento, salute cane
- gatti           -> razze, comportamento, alimentazione, salute gatto
- salute          -> veterinario, vaccini, parassiti, pronto soccorso animali
- prodotti        -> recensioni cibo, accessori, giochi, trasportini
- piccoli-animali -> conigli, criceti, uccelli, pesci, rettili

## CARTELLE REALI
- /home/salvatore/guidapets/content/cani/
- /home/salvatore/guidapets/content/gatti/
- /home/salvatore/guidapets/content/salute/
- /home/salvatore/guidapets/content/prodotti/
- /home/salvatore/guidapets/content/piccoli-animali/
- Immagini: /home/salvatore/guidapets/static/immagini/

## KEYWORD PRIORITA (attacca da qui in ordine)
1. "Miglior cibo secco per cani 2026"              -> prodotti
2. "Come scegliere il gatto perfetto per casa"      -> gatti
3. "Addestramento base cucciolo passo passo"        -> cani
4. "Vaccini cane obbligatori Italia 2026"           -> salute
5. "Miglior cibo per gatti sterilizzati"            -> prodotti
6. "Conigli come animali domestici guida completa"  -> piccoli-animali
7. "Sintomi malattia renale nel gatto"              -> salute
8. "Trasportino cane auto sicuro"                   -> prodotti
9. "Razze cani ideali per appartamento"             -> cani
10. "Criceto come prendersi cura guida"             -> piccoli-animali
11. "Leishmaniosi cane prevenzione e cura"          -> salute
12. "Miglior lettiera gatto autodetergente 2026"    -> prodotti

## OBIETTIVO
Ogni esecuzione:
1. Scegli la prossima keyword dalla lista PRIORITA non ancora pubblicata
2. Ricerca dati aggiornati (prezzi reali, modelli 2026, normative veterinarie IT)
3. Scarica immagine con Pixabay (keyword in INGLESE)
4. Scrivi articolo originale italiano 800-1200 parole
5. Includi SEMPRE tabella prodotti con link Amazon
6. Esegui scripts/publish_post.sh poi deploy+push

## STRUTTURA ARTICOLO OBBLIGATORIA
- **Introduzione**: hook con beneficio concreto per l'animale o risparmio (2-3 frasi)
- **Cosa è e perché è importante**: spiegazione chiara e accessibile (150-200 parole)
- **I migliori prodotti del 2026**: tabella markdown Nome | Prezzo | Pro | Contro | Link
  - Link formato: [Nome Prodotto](https://amzn.to/XXXXX)
  - OpenClaw: cerca su Amazon.it, trova ASIN nell'URL, costruisci il link
- **Guida alla scelta**: criteri pratici, errori da evitare (150-200 parole)
- **Consigli del veterinario**: indicazioni pratiche di salute/prevenzione (max 150 parole)
- **Conclusione**: raccomandazione chiara e rassicurante (2-3 frasi)
- **Fonti**: nome testata

## IMMAGINI - USA SEMPRE PIXABAY
```bash
PIXABAY_KEY=$(grep PIXABAY_API_KEY /home/salvatore/guidapets/.env | cut -d= -f2)
URL=$(wget -qO- "https://pixabay.com/api/?key=$PIXABAY_KEY&q=KEYWORD_INGLESE&image_type=photo&orientation=horizontal&per_page=3" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['hits'][0]['largeImageURL'])")
wget -O /home/salvatore/guidapets/static/immagini/SLUG.jpg "$URL"
```

Keyword per sezione:
- cani            -> "dog" oppure "puppy training"
- gatti           -> "cat" oppure "kitten"
- salute          -> "veterinarian" oppure "pet health"
- prodotti        -> "pet food" oppure "dog accessories"
- piccoli-animali -> "rabbit pet" oppure "hamster"

Fallback se Pixabay fallisce:
```bash
wget -O /home/salvatore/guidapets/static/immagini/SLUG.jpg "https://picsum.photos/seed/SLUG/1280/720"
```

## NAVIGAZIONE STEALTH
- Se un sito blocca: `~/.openclaw/skills/stealth-browser/generate.sh URL`
- MAI Browser Relay (siamo su VPS)

## DEPLOY - COMANDO VERIFICATO E CORRETTO
```bash
cd /home/salvatore/guidapets && source .env && export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID && rm -rf public/ && hugo --minify && npx wrangler pages deploy public --project-name guidapets --commit-dirty=true && git add . && git commit -m "TITOLO" && git push
```
- MAI fare solo `git push` senza wrangler deploy
- MAI usare `wrangler` direttamente — usare sempre `npx wrangler`

## STRUTTURA FILE - NIENTE CARTELLE CON DATE
Salva SEMPRE i file markdown direttamente nella cartella della categoria, SENZA sottocartelle di date.

✅ CORRETTO:
- content/prodotti/miglior-cibo-secco-cani-2026.md
- content/cani/come-addestrare-cucciolo.md

❌ SBAGLIATO:
- content/prodotti/2026/04/28/miglior-cibo-secco-cani-2026.md

La data va SOLO nel frontmatter: `date: 2026-04-28T10:00:00+02:00`

## REGOLA URL PER FACEBOOK E SOCIAL
Formula: `https://guidapets.com/[cartella]/[nome-file-senza-.md]/`

Esempi:
- content/prodotti/miglior-cibo-secco-cani-2026.md → https://guidapets.com/prodotti/miglior-cibo-secco-cani-2026/
- content/cani/come-addestrare-cucciolo.md → https://guidapets.com/cani/come-addestrare-cucciolo/

Regole:
- MAI aggiungere la data nell'URL
- MAI inventare l'URL, ricavarlo SEMPRE dal percorso file
- Aggiungere SEMPRE il trailing slash finale /
- NON includere content/ nell'URL pubblico

## POST FACEBOOK - MASSIMO 2 RIGHE
✅ CORRETTO:
```
🐾 Qual è il miglior cibo secco per il tuo cane nel 2026? Abbiamo testato 5 marche per te!
👉 https://guidapets.com/prodotti/miglior-cibo-secco-cani-2026/
```
❌ SBAGLIATO: post lunghi con paragrafi, elenchi puntati, descrizioni dettagliate.

Regola: emoji iniziale + frase curiosità/hook + link. Nient'altro.

## FRONTMATTER OBBLIGATORIO
```yaml
---
title: "Titolo SEO max 60 caratteri"
date: YYYY-MM-DDTHH:MM:SSZ
draft: false
description: "Riassunto 120-155 caratteri con keyword principale"
categories: ["<sezione>"]
tags: ["tag1", "tag2", "tag3"]
cover:
  image: "/immagini/slug.jpg"
  alt: "Descrizione immagine"
---
```

## VERIFICA FINALE PRIMA DI OGNI PUSH
```bash
# Controlla _redirects (NON deve esistere con regole wildcard)
cat /home/salvatore/guidapets/static/_redirects 2>/dev/null && echo "ATTENZIONE verifica regole" || echo "ok"

# Verifica HTTP sezioni dopo deploy
for SECTION in cani gatti salute prodotti piccoli-animali; do
  CODE=$(curl -o /dev/null -s -w "%{http_code}" https://guidapets.com/$SECTION/)
  echo "$SECTION -> $CODE"
done
```

## REGOLE ASSOLUTE
- MAI copiare testo originale da altre fonti
- Tono: esperto ma caldo e accessibile, focus sul benessere dell'animale
- Slug: solo minuscolo + trattini, niente apostrofi o accenti
- UNA sola categoria per articolo
- Virgolette doppie nel frontmatter, MAI apostrofi singoli
- MAI creare cartelle non elencate sopra
- SEMPRE almeno una tabella prodotti con link Amazon
- Dati prezzi: indicare sempre "Prezzo indicativo aprile 2026"
- MAI dare consigli medici definitivi: usare sempre "consulta il tuo veterinario"
- MAI creare post di test, prova o placeholder
