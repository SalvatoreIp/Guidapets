#!/bin/bash
# Pubblica sulla pagina Facebook Guida Pets il prossimo video della coda scripts/fb_video_queue.json
# (foto animate gratis con scripts/anima_foto.py, gia' generate in static/video/<slug>.mp4 e online).
# Lanciato dal cron una volta al giorno. La pubblicazione vera la fa scripts/fb_reel_post.sh
# (Composio diretto + primo commento col link + storia).
# Lo stato sta FUORI dal repo, cosi' il working tree resta pulito per il git pull del cron delle 10:05.
#
# Uso: scripts/fb_video_coda.sh [--prova]   (--prova: mostra cosa pubblicherebbe, senza pubblicare)
set -u
export PATH=/home/salvatore/.npm-global/bin:/home/salvatore/.local/bin:/usr/local/bin:/usr/bin:/bin
cd /home/salvatore/guidapets
STATO=/home/salvatore/output/guidapets_video_state.json
LOG=logs/fb_reel.log
mkdir -p logs /home/salvatore/output
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }
PROVA="${1:-}"

TESTO="$(mktemp)"
trap 'rm -f "$TESTO"' EXIT
# scrive il testo del post in $TESTO e stampa: id <TAB> slug <TAB> link <TAB> quanti restano dopo questo
NEXT="$(python3 - "$STATO" "$TESTO" <<'EOF'
import json, os, sys
stato, testo = sys.argv[1], sys.argv[2]
fatti = json.load(open(stato))["pubblicati"] if os.path.exists(stato) else []
ids = {p["id"] for p in fatti}
coda = [v for v in json.load(open("scripts/fb_video_queue.json"))["video"] if v["id"] not in ids]
if coda:
    v = coda[0]
    open(testo, "w").write(v["testo"])
    print(f'{v["id"]}\t{v["slug"]}\t{v["link"]}\t{len(coda) - 1}')
EOF
)"
if [ -z "$NEXT" ]; then log "coda video vuota: niente da pubblicare, va rifornita"; exit 0; fi
IFS=$'\t' read -r ID SLUG LINK RESTANO <<< "$NEXT"
log "video #$ID ($SLUG) - restanti in coda dopo questo: $RESTANO"
[ "$RESTANO" -le 3 ] && log "ATTENZIONE: restano solo $RESTANO video in coda, prepararne altri"

if [ "$PROVA" = "--prova" ]; then
  echo "PROVA: pubblicherei #$ID https://guidapets.com/video/$SLUG.mp4 con link $LINK"; cat "$TESTO"; echo
  exit 0
fi

if scripts/fb_reel_post.sh "$SLUG" "$TESTO" "$LINK"; then
  python3 - "$STATO" "$ID" "$SLUG" <<'EOF'
import json, os, sys, datetime
stato, i, slug = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = json.load(open(stato)) if os.path.exists(stato) else {"pubblicati": []}
d["pubblicati"].append({"id": i, "slug": slug, "quando": datetime.datetime.now().isoformat(timespec="seconds")})
json.dump(d, open(stato, "w"), ensure_ascii=False, indent=1)
EOF
  log "video #$ID segnato come pubblicato"
else
  log "ERRORE: video #$ID non pubblicato, resta il prossimo in coda"
fi
