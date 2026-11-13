#!/usr/bin/env bash
# Usage: make_video.sh <project> <out.mp4> [mood]  — renders frames (~1 min per 7 s), builds music/SFX, muxes (voice ducking if <project>/voix.mp3).
set -e
SK="$(cd "$(dirname "$0")/.." && pwd)"; P="$(cd "$1" && pwd)"; OUT="$2"
PROJ="$P" node "$SK/scripts/render.js" full
python3 -I "$SK/scripts/audio.py" "$P" "$3"
if [ -f "$P/voix.mp3" ]; then
  ffmpeg -v error -y -i "$P/video_noaudio.mp4" -i "$P/music.wav" -i "$P/voix.mp3" -filter_complex \
   "[1:a]volume=0.30[m];[2:a]aresample=44100,volume=1.15,asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];[md][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
   -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$P/video_noaudio.mp4" -i "$P/music.wav" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
fi
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
