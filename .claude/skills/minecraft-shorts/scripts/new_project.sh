#!/usr/bin/env bash
# Usage: new_project.sh <project_dir>   — copies the engine and installs three.js + fonts (once).
set -e
SK="$(cd "$(dirname "$0")/.." && pwd)"; P="$1"; [ -z "$P" ] && { echo "usage: $0 <dir>"; exit 1; }
mkdir -p "$P"; cp "$SK"/engine/* "$P"/; [ -f "$P/scenario.js" ] || cp "$SK/examples/hello.js" "$P/scenario.js"
cd "$P"; [ -f package.json ] || npm init -y >/dev/null
[ -d node_modules/three ] || npm i -s three@0.170.0 @fontsource/vt323 @fontsource/montserrat >/dev/null 2>&1
echo "Project ready: $P (edit scenario.js)"
