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

# status: "live" shows a Google Play button, "testing" shows "Coming soon".
APPS = [
    {
        "slug": "hogicam",
        "name": "Hogicam: Digital Camera",
        "short": "Hogicam",
        "package": "vn.txclabs.digicam",
        "status": "testing",
        "category": ("Photography", "Nhiếp ảnh"),
        "tagline": (
            "A shelf of retro cameras in your pocket: 35mm film, toy lens, DV camcorder and Y2K CCD.",
            "Cả kệ máy ảnh retro trong túi: phim 35mm, toy lens, máy quay DV và CCD Y2K.",
        ),
        "about": (
            "Hogicam brings the feel of a vintage camera to your phone. Pick a camera from the shelf, preview its look in the viewfinder, and capture photos with your favorite style. Each camera gives your photos a distinct character with film grain, soft fade, light leaks, vignettes and color effects. Photos are processed on your device and saved to Pictures/Hogicam. No account is needed.",
            "Hogicam mang cảm giác cầm một chiếc máy ảnh hoài cổ vào điện thoại của bạn. Chọn máy trên kệ, xem trước màu ảnh trong khung ngắm rồi chụp theo phong cách mình thích. Mỗi kiểu máy tạo chất ảnh riêng bằng hạt phim, độ mờ, ánh sáng loé, viền tối và hiệu ứng màu. Ảnh được xử lý ngay trên thiết bị và lưu vào Pictures/Hogicam. Không cần tài khoản.",
        ),
        "features": [
            ("Live film looks right in the viewfinder", "Hiệu ứng phim hiển thị ngay trong khung ngắm"),
            ("Photo and video, with the same grade on both", "Chụp ảnh và quay video với cùng một tông màu"),
            ("Instant prints, disposables, B&W and more", "Ảnh lấy liền, máy dùng một lần, đen trắng và nhiều hơn nữa"),
            ("Fully offline: everything stays on your phone", "Hoạt động offline: mọi thứ nằm trên máy bạn"),
        ],
    },
    {
        "slug": "domi",
        "name": "Domi: Photobooth Camera",
        "short": "Domi",
        "package": "com.txclabs.photobooth",
        "status": "testing",
        "category": ("Photography", "Nhiếp ảnh"),
        "tagline": (
            "Make photobooth strips with cute frames, layouts, stickers and filters.",
            "Tạo dải ảnh photobooth với khung xinh, bố cục, sticker và bộ lọc.",
        ),
        "about": (
            "Domi turns your phone into a photobooth. Pick a frame by theme, choose a layout, then shoot right inside the frame or use photos from your gallery. Finish with filters, stickers and text, and save or share your strip in the exact frame ratio.",
            "Domi biến điện thoại thành một quầy photobooth. Chọn khung theo chủ đề, chọn bố cục rồi chụp ngay trong khung hoặc lấy ảnh từ thư viện. Hoàn thiện với bộ lọc, sticker và chữ, sau đó lưu hoặc chia sẻ đúng tỉ lệ khung.",
        ),
        "features": [
            ("Hundreds of themed frames, updated over time", "Hàng trăm khung theo chủ đề, cập nhật liên tục"),
            ("Shoot inside the frame or pick from your gallery", "Chụp ngay trong khung hoặc chọn ảnh từ thư viện"),
            ("Filters, stickers and text in one editor", "Bộ lọc, sticker và chữ trong một trình chỉnh sửa"),
            ("Save and share in the original frame ratio", "Lưu và chia sẻ đúng tỉ lệ khung"),
        ],
    },
    {
        "slug": "colorumi",
        "name": "Colorumi: Color by Number",
        "short": "Colorumi",
        "package": "com.txclabs.color",
        "status": "testing",
        "category": ("Art & Design", "Nghệ thuật"),
        "tagline": (
            "Relaxing pixel color-by-number, plus turn your own photos into paintings.",
            "Tô tranh pixel theo số thư giãn, và biến ảnh của bạn thành tranh tô màu.",
        ),
        "about": (
            "Colorumi turns tiny color cells into vivid pictures. Choose a picture you like, find each color by its number and watch the image appear with every tap. Explore pixel art across animals, food, flowers and landscapes, or turn your own photo into a new picture to color.",
            "Colorumi biến từng ô màu nhỏ thành một bức tranh rực rỡ. Chọn tranh bạn thích, tìm màu theo số và tận hưởng cảm giác hình ảnh dần hiện ra sau mỗi lần chạm. Khám phá tranh pixel nhiều chủ đề như động vật, đồ ăn, hoa lá, phong cảnh, hoặc dùng ảnh của bạn để tạo tranh tô số mới.",
        ),
        "features": [
            ("Pixel art across animals, food, flowers and places", "Tranh pixel đủ chủ đề động vật, đồ ăn, hoa lá, phong cảnh"),
            ("Pixelfy: create a new picture from any photo", "Pixelfy: tạo tranh mới từ bất kỳ ảnh nào"),
            ("Daily picture, streaks and hints", "Tranh mỗi ngày, chuỗi tô màu và gợi ý"),
            ("No account needed, progress saved on device", "Không cần tài khoản, tiến độ lưu trên máy"),
        ],
    },
    {
        "slug": "battery-buddy",
        "name": "Battery Buddy: Emoji Battery",
        "short": "Battery Buddy",
        "package": "com.txclabs.emoji.battery",
        "status": "live",
        "category": ("Entertainment", "Giải trí"),
        "tagline": (
            "Add a personal touch to your phone: emoji battery icons, a custom status bar, animated stickers and screen companions.",
            "Cá nhân hoá điện thoại: biểu tượng pin emoji, thanh trạng thái tuỳ chỉnh, sticker động và bạn đồng hành trên màn hình.",
        ),
        # Text below follows the Google Play listing.
        "about": (
            "Add a personal touch to your phone with Battery Buddy! Explore various ways to decorate your screen and customize your interface to match your own unique style.",
            "Thêm dấu ấn riêng cho điện thoại với Battery Buddy! Khám phá nhiều cách trang trí màn hình và tuỳ chỉnh giao diện theo phong cách của bạn.",
        ),
        "features": [
            ("Change your battery display: choose your favorite battery icon and view your actual battery percentage", "Đổi hiển thị pin: chọn biểu tượng pin yêu thích và xem đúng phần trăm pin"),
            ("Customize the status bar: icons, colors, sizes, backgrounds, date and time", "Tuỳ chỉnh thanh trạng thái: biểu tượng, màu, kích thước, nền, ngày và giờ"),
            ("Decorate with animated stickers and arrange them however you like", "Trang trí bằng sticker động và sắp xếp tuỳ ý"),
            ("Screen companions: animated characters with adjustable size and speed", "Bạn đồng hành: nhân vật hoạt hình với kích thước và tốc độ tuỳ chỉnh"),
            ("Notch Glow: personalize a light accent around the camera", "Notch Glow: hiệu ứng sáng quanh camera theo ý bạn"),
            ("Save favorite battery icons and stickers", "Lưu biểu tượng pin và sticker yêu thích"),
        ],
        "note": (
            "Accessibility Service disclosure: Battery Buddy uses Android's AccessibilityService API solely to display your chosen stickers and custom status bar/notch overlay on top of other apps, and to detect which app is in the foreground so the overlay can be hidden in apps you exclude. It does not read, collect, store or share your screen content, text, passwords or any personal data, and does not perform actions on your behalf.",
            "Công bố về Dịch vụ trợ năng: Battery Buddy chỉ dùng AccessibilityService API của Android để hiển thị sticker và lớp phủ thanh trạng thái/tai thỏ bạn chọn trên các ứng dụng khác, và để biết ứng dụng nào đang mở nhằm ẩn lớp phủ trong những ứng dụng bạn loại trừ. Ứng dụng không đọc, thu thập, lưu trữ hay chia sẻ nội dung màn hình, văn bản, mật khẩu hay bất kỳ dữ liệu cá nhân nào, và không thực hiện thao tác thay bạn.",
        ),
    },
    {
        "slug": "bitarcade",
        "name": "BitArcade: GBA Emulator",
        "short": "BitArcade",
        "package": "com.txclabs.gba",
        "status": "testing",
        "category": ("Games", "Trò chơi"),
        "tagline": (
            "A clean, fast Game Boy Advance and Game Boy Color emulator for your own game files.",
            "Trình giả lập Game Boy Advance và Game Boy Color gọn nhẹ, mượt cho game của chính bạn.",
        ),
        "about": (
            "BitArcade is a pocket arcade for classic handheld games. Load your own GBA, GB and GBC game files, play with responsive on-screen controls and pick up exactly where you left off with save states. No games are included.",
            "BitArcade là máy chơi game cầm tay bỏ túi cho các game cổ điển. Mở file game GBA, GB và GBC của bạn, chơi bằng tay cầm trên màn hình nhạy và tiếp tục đúng chỗ đang chơi nhờ lưu trạng thái. Ứng dụng không kèm game.",
        ),
        "features": [
            ("GBA, GB and GBC support", "Hỗ trợ GBA, GB và GBC"),
            ("Save states and on-screen controls", "Lưu trạng thái và tay cầm trên màn hình"),
            ("Library that organises your files", "Thư viện sắp xếp file game của bạn"),
            ("No games included: bring your own backups", "Không kèm game: bạn dùng bản sao lưu của mình"),
        ],
    },
    {
        "slug": "zodiac-shards",
        "name": "Zodiac Shards",
        "short": "Zodiac Shards",
        "package": "",
        "status": "testing",
        "category": ("Action game", "Game hành động"),
        "tagline": (
            "A 2D pixel-art action platformer: collect 12 zodiac stones, unlock 12 armour forms.",
            "Game hành động pixel 2D: thu thập 12 viên đá con giáp, mở khoá 12 bộ giáp.",
        ),
        "about": (
            "Lam starts as an ordinary villager with a dry branch. Cross the Celestial Board map by map, defeat every enemy and reach the gate to win a zodiac stone. Each stone unlocks a transforming armour with its own moves, and all twelve complete the journey.",
            "Lam khởi đầu là người thường cầm cành cây khô. Vượt qua từng màn trên bản đồ Thiên Bàn, hạ hết quái và tới cổng để nhận một viên đá con giáp. Mỗi viên mở một bộ giáp biến hình với chiêu thức riêng, đủ mười hai viên là hoàn thành hành trình.",
        ),
        "landscape": True,
        "features": [
            ("12 hand-made maps across the Celestial Board", "12 màn chơi trên bản đồ Thiên Bàn"),
            ("Transforming armour inspired by the zodiac", "Bộ giáp biến hình lấy cảm hứng từ 12 con giáp"),
            ("Collect 12 spirit beasts", "Sưu tập 12 Linh Thú"),
            ("Progress saved automatically", "Tiến độ tự động lưu"),
        ],
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def t(pair, tag: str = "span") -> str:
    en, vi = pair
    return f'<{tag} data-lang="en">{esc(en)}</{tag}><{tag} data-lang="vi">{esc(vi)}</{tag}>'


def legal_path(app, kind: str) -> pathlib.Path:
    return ROOT / "content" / "legal" / f"{app['slug']}-{kind}.html"


def play_url(app) -> str:
    return f"https://play.google.com/store/apps/details?id={app['package']}"


def shots(app) -> list[str]:
    d = ROOT / "assets" / "img" / app["slug"]
    return sorted(p.name for p in d.glob("shot-*.webp"))


def banner(app) -> str:
    p = ROOT / "assets" / "img" / app["slug"] / "banner.webp"
    return f"/assets/img/{app['slug']}/banner.webp" if p.exists() else ""


def shots_strip(app) -> str:
    cls = "shots shots-land" if app.get("landscape") else "shots"
    imgs = "".join(
        f'<img src="/assets/img/{app["slug"]}/{n}" alt="{esc(app["short"])} screenshot {i}" loading="lazy">'
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
MAIL = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M4 6h16v12H4z M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'


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
      <button type="button" data-set="vi">VN</button><button type="button" data-set="en">EN</button>
    </div>
  </div>
</header>"""


def footer() -> str:
    links = []
    for a in APPS:
        if legal_path(a, "privacy").exists():
            links.append(f'<a href="/apps/{a["slug"]}/privacy/">{esc(a["short"])}</a>')
    return f"""<footer class="footer">
  <div class="container footer-in">
    <div>
      <a class="logo" href="/"><span class="logo-mark">tx</span><span class="logo-word">{BRAND}</span></a>
      <p class="muted">{t(("Independent mobile apps, made in Vietnam.", "Ứng dụng di động độc lập, làm tại Việt Nam."))}</p>
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
  <a class="app-icon-wrap" href="/apps/{a["slug"]}/"><img class="app-icon" src="/assets/img/{a["slug"]}/icon.webp" alt="{esc(a["short"])} icon" width="80" height="80" loading="lazy"></a>
  <h3><a href="/apps/{a["slug"]}/">{esc(a["short"])}</a></h3>
  <p class="muted">{t(a["tagline"])}</p>
  <div class="card-bottom">
    <a class="link" href="/apps/{a["slug"]}/">{t(("Details", "Chi tiết"))} {ARROW}</a>
    {play_button(a)}
  </div>
</article>"""


def home() -> str:
    cluster = "".join(
        f'<img src="/assets/img/{a["slug"]}/icon.webp" alt="" width="112" height="112" style="--i:{i}">'
        for i, a in enumerate(APPS)
    )
    cards = "\n".join(app_card(a) for a in APPS)
    n = len(APPS)
    live = [a for a in APPS if a["status"] == "live"]
    featured = "".join(
        f"""<section class="section container featured">
  <div class="feat card">
    <div class="feat-copy">
      <p class="eyebrow"><span class="dots"></span>{t(("Now on Google Play", "Đã có trên Google Play"))}</p>
      <div class="feat-head"><img class="app-icon" src="/assets/img/{a["slug"]}/icon.webp" alt="" width="72" height="72"><h2>{esc(a["name"])}</h2></div>
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
    <p class="lead">{t(("TXC Labs is an independent studio from Vietnam building camera, creative and game apps that are simple, fast and respectful of your privacy.", "TXC Labs là studio độc lập tại Việt Nam, làm ứng dụng camera, sáng tạo và game đơn giản, nhanh và tôn trọng quyền riêng tư của bạn."))}</p>
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
    <h2>{t(("Built in Vietnam,", "Làm tại Việt Nam,"))} <em>{t(("for everyone", "cho mọi người"))}</em></h2>
    <div class="stats">
      <div><strong>{n}</strong><span>{t(("apps and games", "ứng dụng và game"))}</span></div>
      <div><strong>{len(live)}</strong><span>{t(("live on Google Play, more coming soon", "đã lên Google Play, thêm nhiều app sắp ra mắt"))}</span></div>
      <div><strong>2</strong><span>{t(("languages: English & Tiếng Việt", "ngôn ngữ: Tiếng Việt & English"))}</span></div>
      <div><strong>0</strong><span>{t(("accounts required", "tài khoản bắt buộc"))}</span></div>
    </div>
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
    if legal_path(a, "privacy").exists():
        legal.append(f'<a class="legal-link" href="/apps/{a["slug"]}/privacy/">{t(("Privacy Policy", "Chính sách quyền riêng tư"))} {ARROW}</a>')
    if legal_path(a, "terms").exists():
        legal.append(f'<a class="legal-link" href="/apps/{a["slug"]}/terms/">{t(("Terms of Use", "Điều khoản sử dụng"))} {ARROW}</a>')
    legal_html = "".join(legal) or f'<p class="muted">{t(("Policies will be published before release.", "Chính sách sẽ được đăng trước khi phát hành."))}</p>'
    pkg = f'<p class="muted small">Package: <code>{esc(a["package"])}</code></p>' if a["package"] else ""
    body = f"""<main>
<section class="container app-hero">
  <a class="crumb" href="/#apps">← {t(("All apps", "Tất cả ứng dụng"))}</a>
  {cover}
  <div class="app-hero-in">
    <img class="app-icon app-icon-lg" src="/assets/img/{a["slug"]}/icon.webp" alt="{esc(a["short"])} icon" width="144" height="144">
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
                image=f"/assets/img/{a['slug']}/icon-128.png")


def legal_page(a, kind: str) -> str:
    content = legal_path(a, kind).read_text(encoding="utf-8")
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
            if legal_path(a, kind).exists():
                write(f"apps/{a['slug']}/{kind}/index.html", legal_page(a, kind))
                urls.append(f"/apps/{a['slug']}/{kind}/")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    main()
