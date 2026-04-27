Istruzioni Operative - Sito GuidaPets
SEZIONI DISPONIBILI
•	cani            -> razze, alimentazione, addestramento, salute cane
•	gatti           -> razze, comportamento, alimentazione, salute gatto
•	salute          -> veterinario, vaccini, parassiti, pronto soccorso animali
•	prodotti        -> recensioni cibo, accessori, giochi, trasportini
•	piccoli-animali -> conigli, criceti, uccelli, pesci, rettili
Cartelle reali:
•	/home/salvatore/guidapets/content/cani/
•	/home/salvatore/guidapets/content/gatti/
•	/home/salvatore/guidapets/content/salute/
•	/home/salvatore/guidapets/content/prodotti/
•	/home/salvatore/guidapets/content/piccoli-animali/
Immagini: /home/salvatore/guidapets/static/immagini/
KEYWORD PRIORITA (attacca da qui in ordine)
1.	“Miglior cibo secco per cani 2026”              -> prodotti
2.	“Come scegliere il gatto perfetto per casa”      -> gatti
3.	“Addestramento base cucciolo passo passo”        -> cani
4.	“Vaccini cane obbligatori Italia 2026”           -> salute
5.	“Miglior cibo per gatti sterilizzati”            -> prodotti
6.	“Conigli come animali domestici guida completa”  -> piccoli-animali
7.	“Sintomi malattia renale nel gatto”              -> salute
8.	“Trasportino cane auto sicuro”                   -> prodotti
9.	“Razze cani ideali per appartamento”             -> cani
10.	“Criceto come prendersi cura guida”             -> piccoli-animali
11.	“Leishmaniosi cane prevenzione e cura”          -> salute
12.	“Miglior lettiera gatto autodetergente 2026”    -> prodotti
OBIETTIVO
Ogni esecuzione:
1.	Scegli la prossima keyword dalla lista PRIORITA non ancora pubblicata
2.	Ricerca dati aggiornati (prezzi reali, modelli 2026, normative veterinarie IT)
3.	Scarica immagine con Pixabay (keyword in INGLESE)
4.	Scrivi articolo originale italiano 800-1200 parole
5.	Includi SEMPRE tabella prodotti con link Amazon
6.	Esegui scripts/publish_post.sh poi deploy+push
STRUTTURA ARTICOLO OBBLIGATORIA
Introduzione
[Hook con beneficio concreto per l’animale o risparmio - 2-3 frasi]
Cose e perche e importante
[Spiegazione chiara e accessibile - 150-200 parole]
I migliori prodotti del 2026
[Tabella markdown: Nome | Prezzo | Pro | Contro | Link]
[Link: Nome Prodotto]
[OpenClaw: cerca su Amazon.it, trova ASIN nell’URL, costruisci il link]
Guida alla scelta
[Criteri pratici, errori da evitare - 150-200 parole]
Consigli del veterinario
[Indicazioni pratiche di salute/prevenzione - max 150 parole]
Conclusione
[Raccomandazione chiara e rassicurante - 2-3 frasi]
Fonti: nome testata
IMMAGINI - USA SEMPRE PIXABAY
PIXABAY_KEY=$(grep PIXABAY_API_KEY /home/salvatore/guidapets/.env | cut -d= -f2)
URL=$(wget -qO- “https://pixabay.com/api/?key=$PIXABAY_KEY&q=KEYWORD_INGLESE&image_type=photo&orientation=horizontal&per_page=3” | python3 -c “import sys,json; d=json.load(sys.stdin); print(d[‘hits’][‘largeImageURL’])”)
wget -O /home/salvatore/guidapets/static/immagini/SLUG.jpg “$URL”
Keyword per sezione:
•	cani            -> “dog” oppure “puppy training”
•	gatti           -> “cat” oppure “kitten”
•	salute          -> “veterinarian” oppure “pet health”
•	prodotti        -> “pet food” oppure “dog accessories”
•	piccoli-animali -> “rabbit pet” oppure “hamster”
Fallback se Pixabay fallisce:
wget -O /home/salvatore/guidapets/static/immagini/SLUG.jpg “https://picsum.photos/seed/SLUG/1280/720”
NAVIGAZIONE STEALTH
Se un sito blocca: ~/.openclaw/skills/stealth-browser/generate.sh URL
MAI Browser Relay (siamo su VPS)
REGOLE ASSOLUTE
•	MAI copiare testo originale da altre fonti
•	Tono: esperto ma caldo e accessibile, focus sul benessere dell’animale
•	Slug: solo minuscolo + trattini, niente apostrofi o accenti
•	UNA sola categoria per articolo
•	Virgolette doppie nel frontmatter, MAI apostrofi singoli
•	MAI creare cartelle non elencate sopra
•	SEMPRE almeno una tabella prodotti con link Amazon
•	SEMPRE link Amazon con formato Nome
•	Dati prezzi: indicare sempre “Prezzo indicativo aprile 2026”
•	MAI dare consigli medici definitivi: usare sempre “consulta il tuo veterinario”
•	Dopo creazione file eseguire SEMPRE (in questo ordine esatto):
cd /home/salvatore/guidapets && source .env && export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID && rm -rf public/ && hugo –minify && npx wrangler pages deploy public –project-name guidapets –commit-dirty=true && git add . && git commit -m “TITOLO” && git push
•	MAI fare solo git push senza wrangler deploy
•	MAI creare post di test, prova o placeholder
FRONTMATTER OBBLIGATORIO
---
title: “Titolo SEO max 60 caratteri”
date: YYYY-MM-DDTHH:MM:SSZ
draft: false
description: “Riassunto 120-155 caratteri con keyword principale”
categories: [”<sezione>”]
tags: [“tag1”, “tag2”, “tag3”]
cover:
image: “/immagini/slug.jpg”
alt: “Descrizione immagine”
VERIFICA FINALE PRIMA DI OGNI PUSH
Controlla _redirects (NON deve esistere con regole wildcard)
cat /home/salvatore/guidapets/static/_redirects 2>/dev/null && echo “ATTENZIONE verifica regole” || echo “ok”
Verifica HTTP sezioni dopo deploy
for SECTION in cani gatti salute prodotti piccoli-animali; do
CODE=$(curl -o /dev/null -s -w “%{http_code}” https://guidapets.com/$SECTION/)
echo “$SECTION -> $CODE”
done
