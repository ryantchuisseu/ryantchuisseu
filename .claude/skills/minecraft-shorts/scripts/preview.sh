#!/usr/bin/env bash
# Usage: preview.sh <project> <t1> <t2> ...  -> <project>/preview_sheet.jpg (contact sheet; look at it with Read)
set -e
SK="$(cd "$(dirname "$0")/.." && pwd)"; P="$(cd "$1" && pwd)"; shift
rm -rf "$P/prev"; PROJ="$P" node "$SK/scripts/render.js" preview "$@"
N=$#; C=$(( N<6 ? N : 6 )); R=$(( (N+5)/6 ))
ffmpeg -v error -y -pattern_type glob -i "$P/prev/f_*.jpg" -vf "scale=300:-1,tile=${C}x${R}" -frames:v 1 "$P/preview_sheet.jpg"
echo "$P/preview_sheet.jpg"
