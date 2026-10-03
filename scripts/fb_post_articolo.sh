#!/bin/bash
# Pubblica sulla pagina Facebook del sito il post con link di un articolo appena uscito.
# Uso: scripts/fb_post_articolo.sh content/<sezione>/<file>.md
# Chiamato da scripts/daily_publish_vps.sh dopo la pubblicazione; si puo' lanciare a mano.
set -uo pipefail
export PATH="/home/salvatore/.npm-global/bin:/home/salvatore/.local/bin:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.." || exit 1
. scripts/fb_config.sh   # definisce PAGE_ID, PAGE_NAME, SITE, STILE

ARTICLE="$1"
TITLE="$(grep -m1 '^title:' "$ARTICLE" | sed 's/^title: *"\(.*\)"$/\1/')"
DESC="$(grep -m1 '^description:' "$ARTICLE" | sed 's/^description: *"\(.*\)"$/\1/')"
# URL esatto calcolato da Hugo (i permalink cambiano da sezione a sezione)
URL="$(hugo list all 2>/dev/null | python3 -c 'import csv,sys; a=sys.argv[1]; print(next((r[7] for r in csv.reader(sys.stdin) if r[0]==a), ""))' "$ARTICLE")"
if [ -n "$URL" ] && [ "$(curl -s -o /dev/null -w '%{http_code}' -m 20 "$URL")" != "200" ]; then
  echo "ERRORE: $URL non risponde 200"; URL=""
fi
if [ -z "$URL" ]; then
  echo "ERRORE: pagina dell'articolo non trovata o non raggiungibile ($ARTICLE), post Facebook NON pubblicato"
  exit 1
fi
echo "Post Facebook ($PAGE_NAME) per: $TITLE ($URL)"
/home/salvatore/.npm-global/bin/openclaw agent --agent main --json --timeout 240 \
  --message "Pubblica ORA sulla Pagina Facebook $PAGE_NAME (page_id $PAGE_ID) usando FACEBOOK_CREATE_POST un post in italiano basato su questo articolo. Titolo: $TITLE. Descrizione: $DESC. $STILE Includi il link $URL come parametro link. Non chiedere conferma: pubblica direttamente e rispondi con l'ID del post. $(cat /home/salvatore/assistente-pagine/fb_nota_account.txt 2>/dev/null)" \
  | grep -o '"text": *"[^"]\{0,300\}' | tail -3
