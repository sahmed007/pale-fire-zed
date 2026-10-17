#!/usr/bin/env bash
# Visual ANSI foreground review; leaves terminal colors reset.
set -euo pipefail
trap 'printf "\033[0m"' EXIT
names=(black red green yellow blue magenta cyan white)
printf 'Pale Fire terminal contrast preview (default background)\n\n'
for index in 0 1 2 3 4 5 6 7; do
    normal=$((30 + index))
    bright=$((90 + index))
    printf '\033[%dm%-8s normal  0123456789 AaBb\033[0m  ' "$normal" "${names[$index]}"
    printf '\033[%dmbright 0123456789 AaBb\033[0m  ' "$bright"
    printf '\033[2;%dmdim 0123456789 AaBb\033[0m\n' "$normal"
done
printf '\nDefault: regular text 0123456789\n'
printf '\033[1mDefault: bright/bold text 0123456789\033[0m\n'
printf '\033[2mDefault: dim text 0123456789\033[0m\n'
