#!/bin/bash
# Dump the quiz database, keep the last 30 dumps here, and copy them to Server 2.
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p backups
out="backups/quiz-$(date +%F).sql.gz"
trap 'rm -f "$out.tmp"' EXIT

docker compose exec -T db pg_dump -U quiz quiz | gzip > "$out.tmp"
mv "$out.tmp" "$out"

# Local retention: only the last 30 dump files (never touches the database itself)
ls -1t backups/quiz-*.sql.gz | tail -n +31 | xargs -r rm --

# Copy to Server 2. No --delete, so nothing is ever removed there from this side.
rsync -a -e "ssh -i $HOME/.ssh/id_backup -o IdentitiesOnly=yes" \
  backups/ devops@192.168.1.131:/mnt/storage/backups/quiz-maker/

echo "$(date -Is) backup ok: $out"
