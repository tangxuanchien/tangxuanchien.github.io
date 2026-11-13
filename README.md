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
| `content/apps/<slug>.json` | One file per app: names, texts (EN/VI), status, images, order |
| `.pages.yml` | Pages CMS config (edit apps in the browser) |
| `.github/workflows/build.yml` | Rebuilds on every push, daily, or on demand |
| `tools/build.py` | Generator: all HTML above is produced from it |

## Ways to update

1. **CMS (browser):** open https://app.pagescms.org, sign in with GitHub, open this repo. Add or edit an app,
   upload icon/header/screenshots, save. The save is a commit; the "Build site" Action rebuilds the HTML and
   GitHub Pages redeploys within a few minutes.
2. **Claude:** type `/update-site` in Claude Code in `D:\AndroidProject`. It finds new app projects, adds them,
   pulls store data, rebuilds, previews and pushes.
3. **By hand:** edit `content/apps/*.json`, run the commands below, commit and push.

Every 3 hours the Action also pulls Google Play data, so an app that goes public switches to "live" by itself.

## Pull data from Google Play

For apps with a public Play page, `tools/fetch_store.py` (uses
[google-play-scraper](https://pypi.org/project/google-play-scraper/)) downloads the store icon, feature graphic,
screenshots and EN/VI descriptions into `assets/img/<slug>/` and `content/apps/<slug>.json`, and marks the app live.
Set `"sync_store": false` on an app to keep your own text. Apps in internal/closed testing have no public page and are skipped.

```bash
pip install google-play-scraper pillow
python tools/fetch_store.py
python tools/build.py
```

## Pull private data from Play Console (Developer API)

`tools/fetch_play_api.py` reads what the public page can't show: the track each app is on
(internal / closed / open / production) and its version, the store listing of apps that are **not public yet**
(text, icon, feature graphic, screenshots, so changes made in Play Console reach the site without the local
project), and, from the Play Console reports bucket, active installs and active subscribers (`play_stats`).
It also warns when an app's contact website in Play Console isn't this site (AdMob needs it for `app-ads.txt`).
Untick "Show Play Console figures" (`"show_stats": false`) to keep subscriber/tester counts off an app's page.

One-time setup:

1. Google Cloud Console: create a project, enable **Google Play Android Developer API**, create a service account,
   add a JSON key.
2. Play Console → Users and permissions → invite the service account email with *View app information*
   (add *View financial data* for subscriber figures).
3. Play Console → Download reports → copy the Cloud Storage URI (`gs://pubsite_prod_…`).
4. GitHub repo → Settings → Secrets and variables → Actions: secret `PLAY_SERVICE_ACCOUNT` = the whole JSON key,
   variable `PLAY_REPORTS_BUCKET` = the bucket name.

Locally: put the key at `.secrets/play-service-account.json` (git-ignored) or set `PLAY_SERVICE_ACCOUNT_FILE`, then

```bash
pip install google-auth requests google-play-scraper pillow
python tools/fetch_play_api.py
```

Without a key the script skips itself and the site uses public data only. Report figures lag about a day.

## Edit & rebuild

1. Change app data in `content/apps/<slug>.json` (`"status": "live"` turns "Coming soon" into a Google Play button).
2. Put images in `assets/img/<slug>/` (`icon.webp` 256px, `icon-128.png`, `shot-1.webp` …).
3. Put policy text in `content/legal/<slug>-privacy.html` / `<slug>-terms.html`.
4. Run `python tools/build.py` and commit the result.

Preview locally: `python -m http.server 8765` then open http://localhost:8765.

## Publish

The repository must be named exactly `tangxuanchien.github.io` (a user site), otherwise `app-ads.txt` is not at the
domain root. Settings → Pages → Deploy from branch `main`, folder `/ (root)`.
