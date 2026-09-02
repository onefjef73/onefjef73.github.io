#!/usr/bin/env python3
"""
Merge the saved onefjef.com pages into one clean, deduped static site.
Run from the "onefjef-site" folder's parent (the Desktop), with a
sibling "ONEFJEF.COM" folder containing the saved "Page - ..._files" dirs.
"""
import os
import re
import shutil

SRC_DIR = "ONEFJEF.COM"
OUT_DIR = "onefjef-site"

PAGES = [
    ("Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Jef Taylor __ filmmaker _ editor _ podcaster_files", "index.html"),
    ("About - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "About - Jef Taylor __ filmmaker _ editor _ podcaster_files", "about.html"),
    ("Commercial - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Commercial - Jef Taylor __ filmmaker _ editor _ podcaster_files", "commercial.html"),
    ("Narrative - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Narrative - Jef Taylor __ filmmaker _ editor _ podcaster_files", "narrative.html"),
    ("Podcasting - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Podcasting - Jef Taylor __ filmmaker _ editor _ podcaster_files", "podcasting.html"),
    ("Social Media - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Social Media - Jef Taylor __ filmmaker _ editor _ podcaster_files", "social-media.html"),
    ("Experimental _ Musical - Jef Taylor __ filmmaker _ editor _ podcaster.html",
     "Experimental _ Musical - Jef Taylor __ filmmaker _ editor _ podcaster_files", "experimental.html"),
]

SHARED = {
    "calico-vars-3c22aa9cc8f24141.css": "calico-vars-3c22aa9cc8f24141.css",
    "calico.min.js": "calico.min.js",
    "css": "fonts.css",
    "editor-grid.min.css": "editor-grid.min.css",
    "fabrik.min.css": "fabrik.min.css",
    "fabrik.min.js": "fabrik.min.js",
    "jquery.min.js": "jquery.min.js",
    "script.js": "script.js",
    "theme.css": "theme.css",
    "118dedebe548c228.JPG": "118dedebe548c228.JPG",
}

LINK_MAP = {
    "https://onefjef.com/": "index.html",
    "https://onefjef.com/commercial": "commercial.html",
    "https://onefjef.com/political": "social-media.html",
    "https://onefjef.com/narrative": "narrative.html",
    "https://onefjef.com/podcasting": "podcasting.html",
    "https://onefjef.com/pages/about": "about.html",
    "https://onefjef.com/experimental": "experimental.html",
}

def reset_out():
    for sub in ("assets", "assets/images"):
        os.makedirs(os.path.join(OUT_DIR, sub), exist_ok=True)
    for f in os.listdir(OUT_DIR):
        p = os.path.join(OUT_DIR, f)
        if f == "scripts":
            continue
        if os.path.isfile(p) and f.endswith(".html"):
            os.remove(p)
    for sub in ("assets", "assets/images"):
        d = os.path.join(OUT_DIR, sub)
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                os.remove(fp)

def copy_shared_assets():
    home_files = os.path.join(SRC_DIR, PAGES[0][1])
    for src_name, dst_name in SHARED.items():
        shutil.copy2(os.path.join(home_files, src_name),
                     os.path.join(OUT_DIR, "assets", dst_name))

FONT_WEIGHTS_USED = {
    ("Manrope", "normal", "700"),
    ("Work Sans", "normal", "400"),
    ("Work Sans", "italic", "400"),
    ("Work Sans", "normal", "600"),
    ("Lato", "normal", "300"),
}
FONT_SUBSETS_USED = {"latin", "latin-ext"}

def trim_fonts_css():
    """The saved font stylesheet declares every weight of every theme
    font (79 @font-face rules) even though the theme only actually uses
    5 weight/style combinations. Trim it down to just those, latin +
    latin-ext only."""
    path = os.path.join(OUT_DIR, "assets", "fonts.css")
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r"(?=/\* )", content)
    kept = []
    for b in blocks:
        m_family = re.search(r"font-family:\s*'([^']+)'", b)
        m_style = re.search(r"font-style:\s*(\w+)", b)
        m_weight = re.search(r"font-weight:\s*(\d+)", b)
        m_subset = re.search(r"/\*\s*([\w-]+)\s*\*/", b)
        if not (m_family and m_style and m_weight):
            continue
        key = (m_family.group(1), m_style.group(1), m_weight.group(1))
        subset = m_subset.group(1) if m_subset else None
        if key in FONT_WEIGHTS_USED and subset in FONT_SUBSETS_USED:
            kept.append(b.strip())
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(kept) + "\n")
    print(f"trimmed fonts.css to {len(kept)} @font-face rules")

def copy_page_images():
    for _, files_dir, _ in PAGES:
        full_dir = os.path.join(SRC_DIR, files_dir)
        for name in os.listdir(full_dir):
            if name in SHARED:
                continue
            dst = os.path.join(OUT_DIR, "assets", "images", name)
            if not os.path.exists(dst):
                shutil.copy2(os.path.join(full_dir, name), dst)

def rewrite_html(html, files_dir_name):
    for src_name, dst_name in SHARED.items():
        old = f"{files_dir_name}/{src_name}"
        html = html.replace(f'"./{old}"', f'"assets/{dst_name}"')
        html = html.replace(f'"{old}"', f'"assets/{dst_name}"')

    for prefix in (f"./{files_dir_name}/", f"{files_dir_name}/"):
        html = re.sub(
            re.escape(prefix) + r'([A-Za-z0-9._-]+)',
            lambda m: f"assets/images/{m.group(1)}" if m.group(1) not in SHARED
                       else f"assets/{SHARED[m.group(1)]}",
            html,
        )

    for old, new in LINK_MAP.items():
        html = html.replace(f'href="{old}"', f'href="{new}"')
        html = html.replace(f'href="{old}/"', f'href="{new}"')

    return html

def build():
    reset_out()
    copy_shared_assets()
    trim_fonts_css()
    copy_page_images()
    for html_name, files_dir, out_name in PAGES:
        with open(os.path.join(SRC_DIR, html_name), "r", encoding="utf-8") as f:
            html = f.read()
        html = rewrite_html(html, files_dir)
        with open(os.path.join(OUT_DIR, out_name), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {out_name}")
    print("shared assets:", len(os.listdir(os.path.join(OUT_DIR, "assets"))) - 1,
          "| images:", len(os.listdir(os.path.join(OUT_DIR, "assets", "images"))))

if __name__ == "__main__":
    build()
