#!/usr/bin/env python3
"""Génère deux fichiers HTML AUTONOMES (CSS, JS et images intégrés) :
   dist/jcia-minimal-3d.html   : icônes 3D
   dist/jcia-minimal-flat.html : icônes plates (traits)
Usage : python3 build.py   (depuis le dossier mockup/minimal)"""
import base64, json, pathlib

here = pathlib.Path(__file__).parent
b64 = lambda p: "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
css = (here / "style.css").read_text(encoding="utf-8")
js = (here / "app.js").read_text(encoding="utf-8")
html = (here / "index.html").read_text(encoding="utf-8")
asset = {
    "logo": b64(here.parent / "assets/logo-jcia.png"),
    "logoDay": b64(here.parent / "assets/logo-jcia-jour.png"),
    "band": b64(here.parent / "assets/bande-toghu.png"),
    "map": b64(here.parent / "assets/carte-cameroun.png"),
}
icons3d = {p.stem: b64(p) for p in sorted((here / "assets/3d").glob("*.png"))}

def build(style: str) -> str:
    pre = f'window.JCIA_ICONS="{style}";window.JCIA_ICONS_FIXED=true;window.JCIA_ASSET={json.dumps(asset)};'
    if style == "3d":
        pre += f"window.JCIA_IMG={json.dumps(icons3d)};"
    out = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}\n</style>")
    out = out.replace('<script src="app.js"></script>', f"<script>\n{pre}\n{js}\n</script>")
    return out

dist = here / "dist"
dist.mkdir(exist_ok=True)
for style in ("3d", "flat"):
    f = dist / f"jcia-minimal-{style}.html"
    f.write_text(build(style), encoding="utf-8")
    print(f"{f.relative_to(here)}  {f.stat().st_size // 1024} Ko")
