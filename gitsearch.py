#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://gitlab.local"
API="$BASE_URL/api/v4/projects"
OUT_FILE="repos.txt"
PER_PAGE=100
RATE=5                 # max requests per second
SLEEP_TIME=$(awk "BEGIN{print 1/$RATE}")  # 0.2s for 5 rps

# Если нужен токен — раскомментируй и вставь:
# TOKEN="YOUR_TOKEN"
# AUTH_HEADER=(-H "PRIVATE-TOKEN: $TOKEN")
AUTH_HEADER=()

: > "$OUT_FILE"        # очистить/создать файл
page=1
total=0

while true; do
  res=$(curl -s "${AUTH_HEADER[@]}" "$API?per_page=$PER_PAGE&page=$page")

  count=$(echo "$res" | jq 'length')
  [ "$count" -eq 0 ] && break

  # Пишем ссылки в файл
  echo "$res" | jq -r '.[].web_url' >> "$OUT_FILE"

  total=$((total + count))
  page=$((page + 1))

  # ограничение ≤ 5 запросов/сек
  sleep "$SLEEP_TIME"
done

echo "Total repositories: $total"
echo "Saved URLs to: $OUT_FILE"
