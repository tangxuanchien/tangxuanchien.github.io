"""Pull public Google Play listing data for every app in content/apps/*.json.

Usage (from the repo root):
    pip install google-play-scraper pillow
    python tools/fetch_store.py
    python tools/build.py

For each app in content/apps/*.json whose package has a public Play page it saves,
in assets/img/<slug>/: icon.webp + icon-128.png (store icon), banner.webp (store
feature graphic) and shot-N.webp (store screenshots), and writes the EN/VI title,
short description, full description (intro, bullet list, closing note) and
category into content/apps/<slug>.json. It also marks the app "live".
Set "sync_store": false in an app's JSON (or untick it in the CMS) to keep your
own text. Apps in closed/internal testing have no public page and are skipped.
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


def split_description(text: str):
    """Store full description -> (intro, bullet lines, closing paragraphs)."""
    intro, bullets, tail = [], [], []
    for line in (x.strip() for x in text.splitlines()):
        if not line:
            continue
        if line[0] in "•-*✓✔":
            bullets.append(line.lstrip("•-*✓✔ ").strip())
        elif bullets:
            tail.append(line)
        else:
            intro.append(line)
    return " ".join(intro), bullets, " ".join(tail)


def fetch(a: dict) -> bool:
    pkg = a.get("package")
    if not pkg or a.get("sync_store") is False:
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
    path = ROOT / "content" / "apps" / f"{a['slug']}.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    # Store image URLs change when an image is replaced on Play; only re-download then,
    # so daily runs don't create commits from re-encoding the same picture.
    seen = d.get("store_images") or {}
    shots = en.get("screenshots") or []
    current = {"icon": en["icon"], "header": en.get("headerImage") or "", "screenshots": shots}

    if seen.get("icon") != current["icon"] or not (out / "icon.webp").exists():
        icon = get_image(sized(en["icon"], "s512")).convert("RGBA")
        icon.resize((256, 256), Image.LANCZOS).save(out / "icon.webp", quality=90)
        icon.resize((128, 128), Image.LANCZOS).save(out / "icon-128.png")

    if current["header"] and (seen.get("header") != current["header"] or not (out / "banner.webp").exists()):
        hdr = get_image(sized(current["header"], "w1024")).convert("RGB")
        hdr.save(out / "banner.webp", quality=86)  # keep the store's own size and ratio

    landscape = d.get("landscape", False)
    if shots and seen.get("screenshots") != shots:
        landscape = False
        for f in out.glob("shot-*.webp"):
            f.unlink()
        for i, url in enumerate(shots, 1):
            im = get_image(sized(url, "w1080")).convert("RGB")
            if i == 1:
                landscape = im.width > im.height
            w = 960 if landscape else 540
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out / f"shot-{i}.webp", quality=84)

    d["store_images"] = current
    d["status"] = "live"
    d["name"] = en["title"]
    d["tagline"] = {"en": en["summary"], "vi": vi["summary"]}
    d["category"] = {"en": en["genre"], "vi": vi["genre"]}
    (ei, eb, et), (vi_i, vb, vt) = split_description(en["description"]), split_description(vi["description"])
    if ei:
        d["about"] = {"en": ei, "vi": vi_i or ei}
    if eb:
        vb = vb if len(vb) == len(eb) else eb
        d["features"] = [{"en": x, "vi": y} for x, y in zip(eb, vb)]
    if et:
        d["note"] = {"en": et, "vi": vt or et}
    d["icon"] = f"/assets/img/{a['slug']}/icon.webp"
    if en.get("headerImage"):
        d["banner"] = f"/assets/img/{a['slug']}/banner.webp"
    if shots:
        d["screenshots"] = [f"/assets/img/{a['slug']}/shot-{i}.webp" for i in range(1, len(shots) + 1)]
        d["landscape"] = landscape
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ok   {a['slug']}: icon, {'banner, ' if en.get('headerImage') else ''}{len(shots)} screenshots, EN/VI text")
    return True


if __name__ == "__main__":
    for a in APPS:
        fetch(a)
