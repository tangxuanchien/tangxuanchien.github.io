"""Pull private Play Console data with the Google Play Developer API (service account).

Usage (from the repo root):
    pip install google-auth requests google-play-scraper pillow
    set PLAY_SERVICE_ACCOUNT_FILE=path\\to\\key.json     (or put it at .secrets/play-service-account.json)
    set PLAY_REPORTS_BUCKET=pubsite_prod_rev_0123456789  (optional, for installs / subscribers)
    python tools/fetch_play_api.py
    python tools/build.py

On GitHub Actions the key comes from the PLAY_SERVICE_ACCOUNT secret (the whole JSON)
and the bucket from the PLAY_REPORTS_BUCKET repository variable.

What it does for every app in content/apps/*.json that has a package:
  * Track: which Play track the app is released on (production / open / closed / internal),
    with version name and date -> "play" in the app JSON.
  * Listing: for apps that are not public yet (status != "live"), downloads the store listing
    you set up in Play Console (EN/VI text, icon, feature graphic, phone screenshots), the same
    way tools/fetch_store.py does for public apps. Skipped when "sync_store" is false.
  * Reports (only with PLAY_REPORTS_BUCKET): latest daily install and subscription figures
    from the Play Console reports bucket -> "play_stats" in the app JSON.
  * Checks that the app's contact website in Play Console is this site (AdMob needs it to
    verify app-ads.txt) and warns otherwise.

Without credentials it prints a note and exits 0, so the build carries on with public data.
"""
from __future__ import annotations

import csv
import io
import json
import os
import pathlib
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import APPS, ROOT, SITE  # noqa: E402

API = "https://androidpublisher.googleapis.com/androidpublisher/v3/applications"
GCS = "https://storage.googleapis.com/storage/v1/b"
SCOPES = [
    "https://www.googleapis.com/auth/androidpublisher",
    "https://www.googleapis.com/auth/devstorage.read_only",
]
# Higher wins when an app has releases on several tracks.
TRACK_RANK = {"internal": 1, "closed": 2, "open": 3, "production": 4}
SUMMARY: list[str] = []


def log(line: str) -> None:
    print(line)
    SUMMARY.append(line)


def credentials_info() -> dict | None:
    raw = os.environ.get("PLAY_SERVICE_ACCOUNT", "").strip()
    if raw:
        return json.loads(raw)
    path = os.environ.get("PLAY_SERVICE_ACCOUNT_FILE") or ROOT / ".secrets" / "play-service-account.json"
    path = pathlib.Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def session(info: dict):
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return AuthorizedSession(creds)


def get_json(s, url: str) -> dict:
    r = s.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


# ---------- Android Publisher: tracks, listing, images ----------

def track_kind(name: str) -> str:
    return {"production": "production", "beta": "open", "internal": "internal"}.get(name, "closed")


def best_release(tracks: list[dict]) -> dict | None:
    best = None
    for tr in tracks:
        kind = track_kind(tr.get("track", ""))
        for rel in tr.get("releases") or []:
            if rel.get("status") not in ("completed", "inProgress"):
                continue
            cand = {
                "track": kind,
                "track_name": tr.get("track", ""),
                "version": rel.get("name") or "",
                "version_code": max((int(v) for v in rel.get("versionCodes") or [0]), default=0),
            }
            key = (TRACK_RANK[kind], cand["version_code"])
            if best is None or key > (TRACK_RANK[best["track"]], best["version_code"]):
                best = cand
    return best


def pick_listing(listings: list[dict], lang: str) -> dict | None:
    for l in listings:
        if l.get("language", "").lower() == lang.lower():
            return l
    for l in listings:
        if l.get("language", "").lower().split("-")[0] == lang.split("-")[0].lower():
            return l
    return None


def sync_listing(s, base: str, d: dict, slug: str, default_lang: str) -> str:
    """Store listing from Play Console -> app JSON + assets/img/<slug>/. Returns a short report."""
    from PIL import Image
    from fetch_store import get_image, sized, split_description

    listings = get_json(s, f"{base}/listings").get("listings") or []
    en = pick_listing(listings, "en-US") or pick_listing(listings, default_lang) or (listings[0] if listings else None)
    if not en:
        return "no store listing yet"
    vi = pick_listing(listings, "vi") or en
    lang = en["language"]

    def images(kind: str) -> list[dict]:
        return get_json(s, f"{base}/listings/{lang}/{kind}").get("images") or []

    icon, header, shots = images("icon"), images("featureGraphic"), images("phoneScreenshots")
    current = {
        "icon": icon[0]["sha1"] if icon else "",
        "header": header[0]["sha1"] if header else "",
        "screenshots": [x["sha1"] for x in shots],
    }
    seen = d.get("play_images") or {}
    out = ROOT / "assets" / "img" / slug
    out.mkdir(parents=True, exist_ok=True)

    if icon and (seen.get("icon") != current["icon"] or not (out / "icon.webp").exists()):
        im = get_image(sized(icon[0]["url"], "s512")).convert("RGBA")
        im.resize((256, 256), Image.LANCZOS).save(out / "icon.webp", quality=90)
        im.resize((128, 128), Image.LANCZOS).save(out / "icon-128.png")
        d["icon"] = f"/assets/img/{slug}/icon.webp"

    if header and (seen.get("header") != current["header"] or not (out / "banner.webp").exists()):
        get_image(sized(header[0]["url"], "w1024")).convert("RGB").save(out / "banner.webp", quality=86)
        d["banner"] = f"/assets/img/{slug}/banner.webp"

    if shots and seen.get("screenshots") != current["screenshots"]:
        landscape = False
        for f in out.glob("shot-*.webp"):
            f.unlink()
        for i, img in enumerate(shots, 1):
            im = get_image(sized(img["url"], "w1080")).convert("RGB")
            if i == 1:
                landscape = im.width > im.height
            w = 960 if landscape else 540
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out / f"shot-{i}.webp", quality=84)
        d["screenshots"] = [f"/assets/img/{slug}/shot-{i}.webp" for i in range(1, len(shots) + 1)]
        d["landscape"] = landscape

    d["play_images"] = current
    report = f"listing {lang}, {len(shots)} screenshots"
    if vi is en and d.get("tagline"):
        # No Vietnamese listing in Play Console: keep the site's own EN/VI text rather than
        # replacing the Vietnamese with English. Images above are still synced. (A brand-new
        # app with no text yet falls through and takes the English listing.)
        return report + " (text kept: no vi listing)"
    if en.get("title"):
        d["name"] = en["title"]
    if en.get("shortDescription"):
        d["tagline"] = {"en": en["shortDescription"], "vi": vi.get("shortDescription") or en["shortDescription"]}
    (ei, eb, et) = split_description(en.get("fullDescription") or "")
    (vi_i, vb, vt) = split_description(vi.get("fullDescription") or "")
    if ei:
        d["about"] = {"en": ei, "vi": vi_i or ei}
    if eb:
        vb = vb if len(vb) == len(eb) else eb
        d["features"] = [{"en": x, "vi": y} for x, y in zip(eb, vb)]
    if et:
        d["note"] = {"en": et, "vi": vt or et}
    return report + " + EN/VI text"


# ---------- Reports bucket: installs and subscriptions ----------

def bucket_name() -> str:
    b = os.environ.get("PLAY_REPORTS_BUCKET", "").strip()
    return b.removeprefix("gs://").strip("/").split("/")[0]


def latest_object(s, bucket: str, prefix: str, suffix: str = ".csv") -> str | None:
    url = f"{GCS}/{bucket}/o?prefix={urllib.parse.quote(prefix, safe='')}&fields=items(name),nextPageToken"
    names, token = [], None
    while True:
        page = get_json(s, url + (f"&pageToken={token}" if token else ""))
        names += [i["name"] for i in page.get("items") or [] if i["name"].endswith(suffix)]
        token = page.get("nextPageToken")
        if not token:
            break
    return max(names) if names else None  # names end in _YYYYMM..., so the max is the newest month


def read_csv(s, bucket: str, name: str) -> list[dict]:
    r = s.get(f"{GCS}/{bucket}/o/{urllib.parse.quote(name, safe='')}?alt=media", timeout=60)
    r.raise_for_status()
    raw = r.content
    text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def num(v) -> int:
    try:
        return int(float(str(v).replace(",", "").strip() or 0))
    except ValueError:
        return 0


def col(row: dict, *names: str):
    low = {k.strip().lower(): v for k, v in row.items() if k}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None


def report_stats(s, bucket: str, pkg: str) -> dict:
    stats: dict = {}
    name = latest_object(s, bucket, f"stats/installs/installs_{pkg}_", "_overview.csv")
    if name:
        rows = read_csv(s, bucket, name)
        if rows:
            last = max(rows, key=lambda r: col(r, "Date") or "")
            stats["date"] = col(last, "Date") or ""
            active = col(last, "Active Device Installs")
            total = col(last, "Total User Installs")
            if active is not None:
                stats["active_installs"] = num(active)
            if total is not None:
                stats["total_installs"] = num(total)
    name = latest_object(s, bucket, f"financial-stats/subscriptions/subscriptions_{pkg}_")
    if name:
        rows = read_csv(s, bucket, name)
        if rows:
            day = max(col(r, "Date") or "" for r in rows)
            today = [r for r in rows if (col(r, "Date") or "") == day]
            stats["subscribers"] = sum(num(col(r, "Active Subscriptions")) for r in today)
            stats["new_subscriptions"] = sum(num(col(r, "New Subscriptions")) for r in today)
            stats["subscriptions_date"] = day
    return stats


# ---------- Main ----------

def sync_app(s, a: dict, bucket: str) -> None:
    pkg, slug = a.get("package"), a["slug"]
    if not pkg:
        return
    path = ROOT / "content" / "apps" / f"{slug}.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    notes = []

    r = s.post(f"{API}/{pkg}/edits", json={}, timeout=60)
    if r.status_code in (403, 404):
        log(f"skip {slug}: no API access to {pkg} (invite the service account in Play Console > Users and permissions)")
        return
    r.raise_for_status()
    edit = r.json()["id"]
    base = f"{API}/{pkg}/edits/{edit}"
    try:
        details = get_json(s, f"{base}/details")
        site = (details.get("contactWebsite") or "").rstrip("/")
        if site != SITE:
            log(f"WARN {slug}: contact website in Play Console is '{site or '(empty)'}', AdMob app-ads.txt needs {SITE}")

        rel = best_release(get_json(s, f"{base}/tracks").get("tracks") or [])
        if rel:
            d["play"] = {k: rel[k] for k in ("track", "version", "version_code")}
            notes.append(f"{rel['track']} {rel['version']}".strip())
        else:
            d.pop("play", None)
            notes.append("no release yet")

        if d.get("status") != "live" and d.get("sync_store") is not False:
            notes.append(sync_listing(s, base, d, slug, details.get("defaultLanguage") or "en-US"))
    finally:
        s.delete(f"{API}/{pkg}/edits/{edit}", timeout=60)  # read-only: never commit the edit

    if bucket:
        try:
            stats = report_stats(s, bucket, pkg)
        except Exception as e:  # noqa: BLE001 - reports are optional
            stats = {}
            log(f"WARN {slug}: could not read reports bucket ({e})")
        if stats:
            d["play_stats"] = stats
            notes.append(", ".join(f"{k}={v}" for k, v in stats.items() if not k.endswith("date")))

    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"ok   {slug}: " + "; ".join(notes))


def main() -> None:
    info = credentials_info()
    if not info:
        print("skip: no service account (set PLAY_SERVICE_ACCOUNT / PLAY_SERVICE_ACCOUNT_FILE); using public data only")
        return
    s = session(info)
    bucket = bucket_name()
    if not bucket:
        print("note: PLAY_REPORTS_BUCKET not set, skipping installs/subscriber reports")
    failed = 0
    for a in APPS:
        try:
            sync_app(s, a, bucket)
        except Exception as e:  # noqa: BLE001 - one app failing must not stop the others
            failed += 1
            log(f"FAIL {a['slug']}: {e}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("### Play Console sync\n\n" + "".join(f"- {x}\n" for x in SUMMARY))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
