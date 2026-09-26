#!/bin/bash
# Pubblicazione automatica giornaliera - eseguito da cron su questa VPS.
# Stesso schema di /home/salvatore/risparmio-energetico/scripts/daily_publish_vps.sh
set -uo pipefail

# Il cron ha un PATH minimale
export PATH="/home/salvatore/.npm-global/bin:/home/salvatore/.local/bin:/usr/local/bin:/usr/bin:/bin"

cd /home/salvatore/guidapets || exit 1
echo "===== $(date '+%Y-%m-%d %H:%M')"

git pull --ff-only origin main

BEFORE="$(git rev-parse HEAD)"

PROMPT="$(cat scripts/daily_publish_prompt.txt)"

/home/salvatore/.local/bin/claude -p "$PROMPT" \
  --model claude-sonnet-5 \
  --allowedTools "Bash Read Write Edit Glob Grep WebSearch WebFetch ToolSearch mcp__claude_ai_ElevenLabs__creative_add_flow_node mcp__claude_ai_ElevenLabs__creative_run_flow_nodes mcp__claude_ai_ElevenLabs__creative_get_flow_run_status" \
  --permission-mode bypassPermissions

# Post Facebook (solo se e' stato pubblicato un nuovo articolo)
AFTER="$(git rev-parse HEAD)"
if [ "$BEFORE" != "$AFTER" ]; then
  ARTICLE="$(git diff --name-only --diff-filter=A "$BEFORE" "$AFTER" -- 'content/*/*.md' | grep -v '_index.md' | head -1)"
  [ -n "$ARTICLE" ] && scripts/fb_post_articolo.sh "$ARTICLE"
fi
