"""Generate the TXC Labs site (GitHub Pages user site).

Usage (from the repo root):  python tools/build.py

Edit APPS below to add an app or flip one to "live", then re-run.
Legal text lives in content/legal/<slug>-privacy.html and <slug>-terms.html
(HTML fragments, no <html>/<body>); a page is only generated when its file exists.
Images live in assets/img/<slug>/ (icon.webp, icon-128.png, shot-1.webp ...).
"""
from __future__ import annotations

import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://tangxuanchien.github.io"
BRAND = "TXC Labs"
EMAIL = "tangxuanchien511@gmail.com"
YEAR = 2026
DEV_URL = "https://play.google.com/store/apps/dev?id=7260813708846735372"

# App data lives in content/apps/<slug>.json (one file per app, editable in the CMS).
# status: "live" shows a Google Play button, "testing" shows "Coming soon".


def _pair(v):
    if not v:
        return None
    if isinstance(v, dict):
        return (v.get("en", ""), v.get("vi") or v.get("en", ""))
    return tuple(v)


def load_apps() -> list[dict]:
    import json
    apps = []
    for f in sorted((ROOT / "content" / "apps").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("hidden"):
            continue
        slug = f.stem
        a = dict(d)
        a["slug"] = slug
        a["short"] = d.get("short") or d["name"].split(":")[0]
        a["status"] = d.get("status", "testing")
        for k in ("category", "tagline", "about", "note"):
            a[k] = _pair(d.get(k))
        a["category"] = a["category"] or ("App", "Ứng dụng")
        a["tagline"] = a["tagline"] or ("", "")
        a["features"] = [_pair(x) for x in d.get("features") or [] if x]
        a["icon"] = d.get("icon") or f"/assets/img/{slug}/icon.webp"
        a["screenshots"] = [x if isinstance(x, str) else x.get("image", "") for x in d.get("screenshots") or []]
        apps.append(a)
    apps.sort(key=lambda a: (a.get("order", 999), a["name"]))
    return apps


APPS = load_apps()

def esc(s: str) -> str:
    return html.escape(s, quote=True)


def t(pair, tag: str = "span") -> str:
    en, vi = pair
    return f'<{tag} data-lang="en">{esc(en)}</{tag}><{tag} data-lang="vi">{esc(vi)}</{tag}>'


def legal_path(app, kind: str) -> pathlib.Path:
    rel = app.get(kind) or f"content/legal/{app['slug']}-{kind}.html"
    return ROOT / rel.lstrip("/")


def legal_text(app, kind: str) -> str:
    """Policy HTML: typed in the CMS (privacy_html / terms_html) or a file in content/legal/."""
    typed = (app.get(f"{kind}_html") or "").strip()
    if typed:
        return typed
    p = legal_path(app, kind)
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def has_legal(app, kind: str) -> bool:
    return bool(legal_text(app, kind))


def play_url(app) -> str:
    return f"https://play.google.com/store/apps/details?id={app['package']}"


def exists(url: str) -> bool:
    return bool(url) and (ROOT / url.lstrip("/")).exists()


def shots(app) -> list[str]:
    return [u for u in app["screenshots"] if exists(u)]


def banner(app) -> str:
    b = app.get("banner") or f"/assets/img/{app['slug']}/banner.webp"
    return b if exists(b) else ""


def shots_strip(app) -> str:
    cls = "shots shots-land" if app.get("landscape") else "shots"
    imgs = "".join(
        f'<img src="{n}" alt="{esc(app["short"])} screenshot {i}" loading="lazy">'
        for i, n in enumerate(shots(app), 1)
    )
    return f'<div class="{cls}">{imgs}</div>' if imgs else ""


PLAY_SVG = (
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
    '<path fill="#00d7fe" d="M3.6 2.3 13.3 12l-9.7 9.7c-.4-.2-.6-.6-.6-1.1V3.4c0-.5.2-.9.6-1.1z"/>'
    '<path fill="#ffce00" d="M16.6 15.3 13.3 12l3.3-3.3 3.8 2.2c1 .6 1 1.6 0 2.2z"/>'
    '<path fill="#ff3a44" d="M16.6 15.3 13.3 12l-9.7 9.7c.4.2.9.2 1.4-.1z"/>'
    '<path fill="#00f076" d="M16.6 8.7 5 2.4c-.5-.3-1-.3-1.4-.1l9.7 9.7z"/></svg>'
)
ARROW = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FLAG_VN = (
    '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#DA251D"/>'
    '<path fill="#FFFF00" d="M15 4l1.76 5.41h5.69l-4.6 3.35 1.76 5.41L15 14.82l-4.61 3.35 1.76-5.41-4.6-3.35h5.69z"/></svg>'
)
FLAG_EN = (
    '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="uk-c"><path d="M0 0v30h60V0z"/></clipPath>'
    '<clipPath id="uk-t"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#uk-c)">'
    '<path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
    '<path d="M0 0l60 30m0-30L0 30" clip-path="url(#uk-t)" stroke="#C8102E" stroke-width="4"/>'
    '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>'
)
MAIL = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M4 6h16v12H4z M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'


def fmt_count(n: int) -> str:
    """44 -> 44, 1234 -> 1.2K, 2500000 -> 2.5M."""
    for div, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")):
        if n >= div:
            v = n / div
            return (f"{v:.1f}".rstrip("0").rstrip(".") if v < 100 else f"{v:.0f}") + suffix
    return str(n)


def play_button(app, big: bool = False) -> str:
    cls = "btn btn-dark" + (" btn-lg" if big else "")
    if app["status"] == "live":
        return (f'<a class="{cls}" href="{play_url(app)}" target="_blank" rel="noopener">{PLAY_SVG}'
                f'{t(("Get it on Google Play", "Tải trên Google Play"))}</a>')
    return f'<span class="btn btn-soft{" btn-lg" if big else ""}" aria-disabled="true">{t(("Coming soon", "Sắp ra mắt"))}</span>'


def status_pill(app) -> str:
    if app["status"] == "live":
        return f'<span class="pill pill-live">{t(("On Google Play", "Đã lên Google Play"))}</span>'
    return f'<span class="pill pill-test">{t(("In testing", "Đang thử nghiệm"))}</span>'


def page(title: str, desc: str, body: str, path: str, image: str = "/assets/img/og.png") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{image}">
<meta name="theme-color" content="#f4f6fb">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,600..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script>(function(){{document.documentElement.classList.add('js');try{{var l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('lang');if(!l)l=(navigator.language||'').toLowerCase().indexOf('vi')===0?'vi':'en';document.documentElement.lang=l}}catch(e){{}}}})();</script>
</head>
<body>
{nav()}
{body}
{footer()}
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def nav() -> str:
    return f"""<header class="nav">
  <div class="container nav-in">
    <a class="logo" href="/" aria-label="{BRAND} home"><span class="logo-mark">tx</span><span class="logo-word">{BRAND}</span></a>
    <nav class="nav-links" aria-label="Main">
      <a href="/#apps">{t(("Apps", "Ứng dụng"))}</a>
      <a href="/#about">{t(("About", "Giới thiệu"))}</a>
      <a href="/#contact">{t(("Contact", "Liên hệ"))}</a>
    </nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" data-set="vi" aria-label="Tiếng Việt">{FLAG_VN}<span>VN</span></button><button type="button" data-set="en" aria-label="English">{FLAG_EN}<span>EN</span></button>
    </div>
  </div>
</header>"""


def footer() -> str:
    links = []
    for a in APPS:
        if has_legal(a, "privacy"):
            links.append(f'<a href="/apps/{a["slug"]}/privacy/">{esc(a["short"])}</a>')
    return f"""<footer class="footer">
  <div class="container footer-in">
    <div>
      <a class="logo" href="/"><span class="logo-mark">tx</span><span class="logo-word">{BRAND}</span></a>
      <p class="muted">{t(("Independent mobile apps for people everywhere.", "Ứng dụng di động độc lập cho mọi người, ở mọi nơi."))}</p>
    </div>
    <div>
      <h3>{t(("Privacy policies", "Chính sách quyền riêng tư"))}</h3>
      <div class="footer-links">{''.join(links)}</div>
    </div>
    <div>
      <h3>{t(("Contact", "Liên hệ"))}</h3>
      <div class="footer-links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{DEV_URL}" target="_blank" rel="noopener">{t(("TXC Labs on Google Play", "TXC Labs trên Google Play"))}</a></div>
    </div>
  </div>
  <div class="container footer-base muted">&copy; {YEAR} {BRAND}. {t(("All rights reserved.", "Bảo lưu mọi quyền."))}</div>
</footer>"""


def app_card(a) -> str:
    b = banner(a)
    cover = (f'<a class="card-cover" href="/apps/{a["slug"]}/" tabindex="-1" aria-hidden="true"><img src="{b}" alt="" loading="lazy" width="1024" height="500"></a>'
             if b else '<div class="card-cover card-cover-empty"></div>')
    return f"""<article class="card app-card">
  {cover}
  <div class="card-top">
    <span class="chip">{t(a["category"])}</span>{status_pill(a)}
  </div>
  <a class="app-icon-wrap" href="/apps/{a["slug"]}/"><img class="app-icon" src="{a["icon"]}" alt="{esc(a["short"])} icon" width="80" height="80" loading="lazy"></a>
  <h3><a href="/apps/{a["slug"]}/">{esc(a["short"])}</a></h3>
  <p class="muted">{t(a["tagline"])}</p>
  <div class="card-bottom">
    <a class="link" href="/apps/{a["slug"]}/">{t(("Details", "Chi tiết"))} {ARROW}</a>
    {play_button(a)}
  </div>
</article>"""


def home() -> str:
    cluster = "".join(
        f'<img src="{a["icon"]}" alt="" width="112" height="112" style="--i:{i}">'
        for i, a in enumerate(APPS)
    )
    cards = "\n".join(app_card(a) for a in APPS)
    n = len(APPS)
    live = [a for a in APPS if a["status"] == "live"]
    total_installs = sum(int(a.get("install_count") or 0) for a in live)
    rows = "".join(
        f'<a class="inst-row" href="/apps/{a["slug"]}/"><img src="{a["icon"]}" alt="" width="44" height="44" loading="lazy">'
        f'<span class="inst-name">{esc(a["short"])}</span>'
        f'<span class="inst-num"><strong>{fmt_count(int(a.get("install_count") or 0))}</strong> {t(("installs", "lượt cài"))}</span></a>'
        for a in sorted(live, key=lambda a: -int(a.get("install_count") or 0))
    )
    installs_list = (
        f'<div class="installs"><h3>{t(("Installs by app", "Lượt cài theo từng app"))}</h3>'
        f'<div class="inst-grid">{rows}</div>'
        f'<p class="inst-note">{t(("Live figures from Google Play, updated daily.", "Số liệu từ Google Play, cập nhật mỗi ngày."))}</p></div>'
        if rows else ""
    )
    featured = "".join(
        f"""<section class="section container featured">
  <div class="feat card">
    <div class="feat-copy">
      <p class="eyebrow"><span class="dots"></span>{t(("Now on Google Play", "Đã có trên Google Play"))}</p>
      <div class="feat-head"><img class="app-icon" src="{a["icon"]}" alt="" width="72" height="72"><h2>{esc(a["name"])}</h2></div>
      <p class="lead">{t(a.get("about", a["tagline"]))}</p>
      <ul class="ticks">{"".join(f"<li>{t(f)}</li>" for f in a["features"][:4])}</ul>
      <div class="hero-cta">{play_button(a, big=True)}<a class="link link-underline" href="/apps/{a["slug"]}/">{t(("Learn more", "Xem thêm"))} {ARROW}</a></div>
    </div>
    <div class="feat-shots">{shots_strip(a)}</div>
  </div>
</section>"""
        for a in live
    )
    body = f"""<main>
<section class="hero container">
  <div class="hero-copy">
    <h1>{t(("Small apps,", "Ứng dụng nhỏ,"))}<br><em>{t(("made with care", "làm bằng tâm huyết"))}</em></h1>
    <p class="lead">{t(("TXC Labs is an independent studio building camera, creative and game apps for users around the world: simple, fast and respectful of your privacy.", "TXC Labs là studio độc lập làm ứng dụng camera, sáng tạo và game cho người dùng trên toàn thế giới: đơn giản, nhanh và tôn trọng quyền riêng tư của bạn."))}</p>
    <div class="hero-cta">
      <a class="btn btn-dark btn-lg" href="#apps">{t(("Explore apps", "Khám phá ứng dụng"))}<span class="btn-ico">{ARROW}</span></a>
      <a class="link link-underline" href="{DEV_URL}" target="_blank" rel="noopener">{t(("Our Google Play page", "Trang Google Play của chúng tôi"))} {ARROW}</a>
    </div>
  </div>
  <div class="hero-art" aria-hidden="true"><div class="cluster">{cluster}</div></div>
</section>
{featured}

<section id="apps" class="section container">
  <div class="section-head">
    <div>
      <p class="eyebrow"><span class="dots"></span>{t(("Our apps", "Sản phẩm"))}</p>
      <h2>{t(("Apps we're", "Những app chúng tôi"))} <em>{t(("building", "đang làm"))}</em></h2>
    </div>
    <p class="muted section-note">{t(("Most of our apps are in testing on Google Play right now. Check back soon.", "Phần lớn ứng dụng đang trong giai đoạn thử nghiệm trên Google Play. Hãy quay lại sớm nhé."))}</p>
  </div>
  <div class="grid">
{cards}
  </div>
</section>

<section id="about" class="band">
  <div class="container band-in">
    <p class="eyebrow eyebrow-light"><span class="dots"></span>{t(("About", "Giới thiệu"))}</p>
    <h2>{t(("Made for everyone,", "Làm cho mọi người,"))} <em>{t(("everywhere", "ở mọi nơi"))}</em></h2>
    <div class="stats">
      <div><strong>{fmt_count(total_installs)}</strong><span>{t(("total installs across our live apps", "tổng lượt cài của các app đã phát hành"))}</span></div>
      <div><strong>{n}</strong><span>{t(("apps and games", "ứng dụng và game"))}</span></div>
      <div><strong>{len(live)}</strong><span>{t(("live on Google Play, more coming soon", "đã lên Google Play, thêm nhiều app sắp ra mắt"))}</span></div>
      <div><strong class="word">{t(("Global", "Toàn cầu"))}</strong><span>{t(("built for users worldwide", "hướng tới người dùng khắp thế giới"))}</span></div>
    </div>
    {installs_list}
  </div>
</section>

<section class="section container">
  <div class="section-head">
    <div>
      <p class="eyebrow"><span class="dots"></span>{t(("How we work", "Cách chúng tôi làm"))}</p>
      <h2>{t(("Three things we", "Ba điều chúng tôi"))} <em>{t(("care about", "luôn giữ"))}</em></h2>
    </div>
  </div>
  <div class="values">
    <div class="card value reveal"><span class="num">01</span><h3>{t(("Privacy first", "Quyền riêng tư trước tiên"))}</h3><p class="muted">{t(("Your photos and progress stay on your device. We only collect what an app truly needs, and say so plainly.", "Ảnh và tiến độ của bạn nằm trên máy bạn. Chúng tôi chỉ thu thập những gì app thực sự cần và nói rõ điều đó."))}</p></div>
    <div class="card value reveal"><span class="num">02</span><h3>{t(("Works offline", "Chạy được offline"))}</h3><p class="muted">{t(("Wherever we can, apps run fully on-device, so they're quick and work without a connection.", "Khi có thể, app chạy hoàn toàn trên máy để nhanh và dùng được cả khi không có mạng."))}</p></div>
    <div class="card value reveal"><span class="num">03</span><h3>{t(("Small & polished", "Nhỏ gọn & chỉn chu"))}</h3><p class="muted">{t(("Fewer features, done well: smooth motion, clear screens and a light install size.", "Ít tính năng nhưng làm kỹ: chuyển động mượt, màn hình rõ ràng và dung lượng nhẹ."))}</p></div>
  </div>
</section>

<section id="contact" class="section container">
  <div class="cta card">
    <div>
      <h2>{t(("Let's", "Hãy"))} <em>{t(("talk", "trò chuyện"))}</em></h2>
      <p class="muted">{t(("Feedback, bug reports or partnership ideas: we read every email.", "Góp ý, báo lỗi hay ý tưởng hợp tác: chúng tôi đọc mọi email."))}</p>
    </div>
    <a class="btn btn-dark btn-lg" href="mailto:{EMAIL}">{MAIL}{EMAIL}</a>
  </div>
</section>
</main>"""
    return page(f"{BRAND} — Independent mobile apps",
                "TXC Labs builds camera, creative and game apps for Android: Hogicam, Domi, Colorumi, Battery Buddy, BitArcade and Zodiac Shards.",
                body, "/")


def app_page(a) -> str:
    gallery = ""
    strip = shots_strip(a)
    if strip:
        gallery = f'<section class="section container sec-tight"><h2 class="h-sm">{t(("Screenshots", "Ảnh màn hình"))}</h2>{strip}</section>'
    b = banner(a)
    cover = f'<div class="app-banner"><img src="{b}" alt="{esc(a["short"])} feature graphic" width="1024" height="500"></div>' if b else ""
    about = f'<p class="about">{t(a["about"])}</p>' if a.get("about") else ""
    note = f'<p class="muted small note">{t(a["note"])}</p>' if a.get("note") else ""
    feats = "".join(f"<li>{t(f)}</li>" for f in a["features"])
    legal = []
    if has_legal(a, "privacy"):
        legal.append(f'<a class="legal-link" href="/apps/{a["slug"]}/privacy/">{t(("Privacy Policy", "Chính sách quyền riêng tư"))} {ARROW}</a>')
    if has_legal(a, "terms"):
        legal.append(f'<a class="legal-link" href="/apps/{a["slug"]}/terms/">{t(("Terms of Use", "Điều khoản sử dụng"))} {ARROW}</a>')
    legal_html = "".join(legal) or f'<p class="muted">{t(("Policies will be published before release.", "Chính sách sẽ được đăng trước khi phát hành."))}</p>'
    pkg = f'<p class="muted small">Package: <code>{esc(a["package"])}</code></p>' if a["package"] else ""
    body = f"""<main>
<section class="container app-hero">
  <a class="crumb" href="/#apps">← {t(("All apps", "Tất cả ứng dụng"))}</a>
  {cover}
  <div class="app-hero-in">
    <img class="app-icon app-icon-lg" src="{a["icon"]}" alt="{esc(a["short"])} icon" width="144" height="144">
    <div>
      <div class="card-top"><span class="chip">{t(a["category"])}</span>{status_pill(a)}</div>
      <h1 class="h-app">{esc(a["name"])}</h1>
      <p class="lead">{t(a["tagline"])}</p>
      <div class="hero-cta">{play_button(a, big=True)}<a class="link link-underline" href="mailto:{EMAIL}?subject={esc(a["short"])}">{t(("Send feedback", "Gửi góp ý"))} {ARROW}</a></div>
    </div>
  </div>
</section>
{gallery}
<section class="section container two-col">
  <div class="card"><h2 class="h-sm">{t(("About this app", "Về ứng dụng"))}</h2>{about}<ul class="ticks">{feats}</ul>{note}</div>
  <div class="card"><h2 class="h-sm">{t(("Legal & support", "Pháp lý & hỗ trợ"))}</h2>{legal_html}<a class="legal-link" href="mailto:{EMAIL}">{t(("Contact support", "Liên hệ hỗ trợ"))} {ARROW}</a>{pkg}</div>
</section>
</main>"""
    return page(f"{a['name']} — {BRAND}", a["tagline"][0], body, f"/apps/{a['slug']}/",
                image=(a["icon"].rsplit("/", 1)[0] + "/icon-128.png") if exists(a["icon"].rsplit("/", 1)[0] + "/icon-128.png") else a["icon"])


def legal_page(a, kind: str) -> str:
    content = legal_text(a, kind)
    label = ("Privacy Policy", "Chính sách quyền riêng tư") if kind == "privacy" else ("Terms of Use", "Điều khoản sử dụng")
    body = f"""<main class="container legal-wrap">
  <a class="crumb" href="/apps/{a["slug"]}/">← {esc(a["short"])}</a>
  <article class="legal card">
{content}
  </article>
</main>"""
    return page(f"{label[0]} — {a['name']}", f"{label[0]} for the {a['name']} Android app.", body,
                f"/apps/{a['slug']}/{kind}/")


def not_found() -> str:
    body = f"""<main class="container nf">
  <h1><em>404</em></h1>
  <p class="lead">{t(("This page doesn't exist.", "Trang này không tồn tại."))}</p>
  <a class="btn btn-dark btn-lg" href="/">{t(("Back home", "Về trang chủ"))}</a>
</main>"""
    return page(f"Not found — {BRAND}", "Page not found.", body, "/404.html")


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", rel)


def main() -> None:
    write("index.html", home())
    write("404.html", not_found())
    urls = ["/"]
    for a in APPS:
        write(f"apps/{a['slug']}/index.html", app_page(a))
        urls.append(f"/apps/{a['slug']}/")
        for kind in ("privacy", "terms"):
            if has_legal(a, kind):
                write(f"apps/{a['slug']}/{kind}/index.html", legal_page(a, kind))
                urls.append(f"/apps/{a['slug']}/{kind}/")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    main()
