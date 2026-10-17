#!/usr/bin/env bash
set -euo pipefail

# Functions, expansion, arithmetic, patterns, and heredocs.
readonly LIMIT=42
items=(ready waiting empty)

report() {
    local name="$1"
    local count="${2:-0}"
    if (( count >= LIMIT )); then
        printf '%s: full (%d)\n' "$name" "$count"
    else
        printf '%s: %d\n' "$name" "$count"
    fi
}

for name in "${items[@]}"; do
    case "$name" in
        ready) report "$name" "$((21 * 2))" ;;
        waiting) report "$name" 2 ;;
        *) report "$name" ;;
    esac
done

cat <<'MESSAGE'
Preview complete: literal $variables stay untouched here.
MESSAGE
