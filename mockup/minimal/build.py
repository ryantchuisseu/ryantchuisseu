#!/usr/bin/env python3
"""Génère deux fichiers HTML AUTONOMES (CSS, JS et images intégrés) :
   dist/jcia-minimal-3d.html   : icônes 3D
   dist/jcia-minimal-flat.html : icônes plates (traits)
   dist/jcia-leger.html        : habillage « Léger » (inspiré d'Atoms), icônes plates fines
Usage : python3 build.py   (depuis le dossier mockup/minimal)"""
import base64, json, pathlib

here = pathlib.Path(__file__).parent
b64 = lambda p: "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
css = (here / "style.css").read_text(encoding="utf-8") + "\n" + (here / "leger.css").read_text(encoding="utf-8")
js = (here / "app.js").read_text(encoding="utf-8")
html = (here / "index.html").read_text(encoding="utf-8")
asset = {
    "logo": b64(here.parent / "assets/logo-jcia.png"),
    "logoDay": b64(here.parent / "assets/logo-jcia-jour.png"),
    "band": b64(here.parent / "assets/bande-toghu.png"),
    "map": b64(here.parent / "assets/carte-cameroun.png"),
}
icons3d = {p.stem: b64(p) for p in sorted((here / "assets/3d").glob("*.png"))}

def build(style: str, skin: str = "") -> str:
    pre = f'window.JCIA_ICONS="{style}";window.JCIA_ICONS_FIXED=true;window.JCIA_SKIN="{skin}";window.JCIA_ASSET={json.dumps(asset)};'
    if style == "3d":
        pre += f"window.JCIA_IMG={json.dumps(icons3d)};"
    out = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}\n</style>").replace('<link rel="stylesheet" href="leger.css">\n', "")
    out = out.replace('<script src="app.js"></script>', f"<script>\n{pre}\n{js}\n</script>")
    return out

dist = here / "dist"
dist.mkdir(exist_ok=True)
for name, style, skin in (("jcia-minimal-3d", "3d", ""), ("jcia-minimal-flat", "flat", ""), ("jcia-leger", "flat", "leger")):
    f = dist / f"{name}.html"
    f.write_text(build(style, skin), encoding="utf-8")
    print(f"{f.relative_to(here)}  {f.stat().st_size // 1024} Ko")
