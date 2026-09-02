# onefjef.com

A clean, static rebuild of onefjef.com, assembled from Chrome's "Save Page As" copies of the live Fabrik-hosted site.

## Structure

- `index.html`, `about.html`, `commercial.html`, `narrative.html`, `podcasting.html`, `social-media.html`, `experimental.html` — the site's pages.
- `assets/` — CSS, JS, and the profile photo, shared by every page (previously duplicated once per page; now one copy).
- `assets/images/` — every project thumbnail/photo, deduped by filename.
- `scripts/build_site.py` — the script that generated this from the raw saved pages. Re-run it if you save a new/updated page from the live site into a sibling `ONEFJEF.COM` folder (see the mapping at the top of the script).

## Known gap

All seven top-level pages are now rebuilt. A handful of individual project detail pages (e.g. `/portfolio/hollister-jean-lab`, `/portfolio/adults`) still link out to the live site — those were never saved as their own pages, only referenced from the category grids.

## What changed vs. the raw saved pages

- Seven copies of the same ~500KB of CSS/JS collapsed into one shared `assets/` folder.
- The font stylesheet was trimmed from 79 declared font-face variants down to the 8 actually used by the theme (Manrope 700, Work Sans 400/400-italic/600, Lato 300 — latin + latin-ext only).
- That font file was also renamed from a bare `css` to `fonts.css` — some static hosts don't guess the right content type for an extensionless file, which can silently break font loading.
- All internal navigation between these six pages now links to local files instead of back out to onefjef.com.

## Hosting

Push this repo to GitHub, then turn on GitHub Pages (Settings → Pages → deploy from the `main` branch). Point onefjef.com's DNS at GitHub Pages to use the existing domain.
