"""Pull public Google Play listing data for every app in tools/build.py.

Usage (from the repo root):
    pip install google-play-scraper pillow
    python tools/fetch_store.py
    python tools/build.py

For each package that has a public Play page it saves, in assets/img/<slug>/:
icon.webp + icon-128.png (store icon), banner.webp (store feature graphic),
shot-N.webp (store screenshots), and content/store/<slug>.json with the EN/VI
title, short description, full description and category. build.py prefers this
data over the hand-written text. Apps still in closed/internal testing have no
public page and are skipped (their local assets stay as they are).
"""
from __future__ import annotations

import io
import json
import pathlib
import sys
import urllib.request

from google_play_scraper import app as play_app
from google_play_scraper.exceptions import NotFoundError
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import APPS, ROOT  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0"}


def get_image(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read()))


def sized(url: str, suffix: str) -> str:
    # play-lh URLs take a size suffix: =s512, =w1080, =w1024-h500 ...
    return url.split("=")[0] + "=" + suffix


def fetch(a: dict) -> bool:
    pkg = a.get("package")
    if not pkg:
        return False
    try:
        en = play_app(pkg, lang="en", country="us")
    except NotFoundError:
        print(f"skip {a['slug']}: no public Play page")
        return False
    try:
        vi = play_app(pkg, lang="vi", country="vn")
    except NotFoundError:
        vi = en

    out = ROOT / "assets" / "img" / a["slug"]
    out.mkdir(parents=True, exist_ok=True)

    icon = get_image(sized(en["icon"], "s512")).convert("RGBA")
    icon.resize((256, 256), Image.LANCZOS).save(out / "icon.webp", quality=90)
    icon.resize((128, 128), Image.LANCZOS).save(out / "icon-128.png")

    if en.get("headerImage"):
        hdr = get_image(sized(en["headerImage"], "w1024")).convert("RGB")
        hdr.save(out / "banner.webp", quality=86)  # keep the store's own size and ratio

    shots = en.get("screenshots") or []
    landscape = False
    if shots:
        for f in out.glob("shot-*.webp"):
            f.unlink()
        for i, url in enumerate(shots, 1):
            im = get_image(sized(url, "w1080")).convert("RGB")
            if i == 1:
                landscape = im.width > im.height
            w = 960 if landscape else 540
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out / f"shot-{i}.webp", quality=84)

    data = {
        "title": en["title"],
        "summary": [en["summary"], vi["summary"]],
        "description": [en["description"], vi["description"]],
        "genre": [en["genre"], vi["genre"]],
        "landscape": landscape,
        "url": en["url"],
    }
    store = ROOT / "content" / "store"
    store.mkdir(parents=True, exist_ok=True)
    (store / f"{a['slug']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ok   {a['slug']}: icon, {'banner, ' if en.get('headerImage') else ''}{len(shots)} screenshots, EN/VI text")
    return True


if __name__ == "__main__":
    for a in APPS:
        fetch(a)
