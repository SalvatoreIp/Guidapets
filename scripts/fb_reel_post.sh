#!/bin/bash
# Pubblica un reel (video MP4 gia' online su guidapets.com/video/) sulla pagina Facebook Guida Pets
# e mette come primo commento il link a un articolo del sito.
# Chiama Composio direttamente (~/assistente-pagine/composio.mjs): nessun agente LLM in mezzo,
# quindi niente ID inventati.
#
# Uso: scripts/fb_reel_post.sh SLUG_VIDEO FILE_TESTO [LINK_ARTICOLO]
#   es. scripts/fb_reel_post.sh reel-3d-cucciolo /home/salvatore/reel-prove/testo-cucciolo.txt https://guidapets.com/cani/...
# Pensato anche per essere lanciato a un orario preciso con `at`.
set -u
export PATH=/home/salvatore/.npm-global/bin:/home/salvatore/.local/bin:/usr/local/bin:/usr/bin:/bin
cd /home/salvatore/guidapets
. scripts/fb_config.sh   # PAGE_ID, PAGE_NAME, SITE
LOG=logs/fb_reel.log
COMPOSIO=/home/salvatore/assistente-pagine/composio.mjs
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

SLUG="$1"; TESTO_FILE="$2"; LINK="${3:-}"
URL="$SITE/video/$SLUG.mp4"
[ "$(curl -s -o /dev/null -w '%{http_code}' -m 30 "$URL")" = "200" ] || { log "ERRORE: video non raggiungibile $URL"; exit 1; }

ARGS="$(python3 -c 'import json,sys; print(json.dumps({"tools":[{"tool_slug":"FACEBOOK_CREATE_VIDEO_POST","arguments":{"page_id":sys.argv[1],"file_url":sys.argv[2],"description":open(sys.argv[3]).read().strip()}}]}))' "$PAGE_ID" "$URL" "$TESTO_FILE")"
OUT="$(node "$COMPOSIO" call COMPOSIO_MULTI_EXECUTE_TOOL "$ARGS" 2>&1)"
VID="$(echo "$OUT" | python3 -c '
import json,sys
raw=sys.stdin.read()
try:
    d=json.loads(raw[raw.index("{"):])
    r=d["data"]["results"][0]["response"]
    print(r["data"].get("id","") if r.get("successful") else "")
except Exception:
    print("")')"
if [ -z "$VID" ]; then log "ERRORE: reel NON pubblicato ($SLUG)"; echo "$OUT" | tail -c 800 >> "$LOG"; exit 1; fi
log "reel pubblicato: video $VID ($SLUG)"

if [ -n "$LINK" ] && [ "$(curl -s -o /dev/null -w '%{http_code}' -m 20 "$LINK")" = "200" ]; then
  CARGS="$(python3 -c 'import json,sys; print(json.dumps({"tools":[{"tool_slug":"FACEBOOK_CREATE_COMMENT","arguments":{"object_id":sys.argv[1],"message":"📖 Se vuoi approfondire, qui trovi la guida completa:\n"+sys.argv[2]}}]}))' "$VID" "$LINK")"
  COUT="$(node "$COMPOSIO" call COMPOSIO_MULTI_EXECUTE_TOOL "$CARGS" 2>&1)"
  if echo "$COUT" | grep -q '"successful":true' && ! echo "$COUT" | grep -q '"error_count":[1-9]'; then
    log "primo commento con link pubblicato ($LINK)"
  else
    log "ATTENZIONE: primo commento NON pubblicato ($LINK)"; echo "$COUT" | tail -c 400 >> "$LOG"
  fi
fi
