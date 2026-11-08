# tangxuanchien.github.io — TXC Labs

Developer website for the TXC Labs Android apps, served by GitHub Pages at
https://tangxuanchien.github.io/

## Layout

| Path | What |
|---|---|
| `index.html` | Home: hero, app grid, about, contact |
| `apps/<slug>/` | App page (screenshots, highlights, legal links) |
| `apps/<slug>/privacy/`, `apps/<slug>/terms/` | Privacy policy / terms (use these URLs in Play Console) |
| `app-ads.txt` | AdMob authorised sellers (`pub-2978360902369190`) — must stay at the site root |
| `content/legal/<slug>-privacy.html` | Source text of each policy (HTML fragment) |
| `assets/` | CSS, JS, icons, screenshots |
| `tools/build.py` | Generator: all HTML above is produced from it |

## Edit & rebuild

1. Change app data in `APPS` at the top of `tools/build.py` (set `"status": "live"` once an app is public — that
   turns "Coming soon" into a Google Play button).
2. Put images in `assets/img/<slug>/` (`icon.webp` 256px, `icon-128.png`, `shot-1.webp` …).
3. Put policy text in `content/legal/<slug>-privacy.html` / `<slug>-terms.html`.
4. Run `python tools/build.py` and commit the result.

Preview locally: `python -m http.server 8765` then open http://localhost:8765.

## Publish

The repository must be named exactly `tangxuanchien.github.io` (a user site), otherwise `app-ads.txt` is not at the
domain root. Settings → Pages → Deploy from branch `main`, folder `/ (root)`.
