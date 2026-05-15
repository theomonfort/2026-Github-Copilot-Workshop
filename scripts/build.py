#!/usr/bin/env python3
"""Build the codelab HTML for both JP and EN markdown sources.

Usage:
    python3 scripts/build.py

Reads:
    workshop-nikon.md     -> github-copilot-workshop/custom/{handson,nikon}/index.html
    workshop-nikon-en.md  -> github-copilot-workshop/custom/{handson-en,nikon-en}/index.html (if exists)
"""
from __future__ import annotations
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DARK_CSS = (ROOT / "scripts" / "dark-mode.css").read_text()
CLAAT = Path.home() / "claat"

PRISM_INJECT = """  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/toolbar/prism-toolbar.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</head>"""

CSS_MARKER = "      color: red;\n    }\n  </style>"
CSS_REPLACEMENT = (
    f"      color: red;\n    }}\n  </style>\n"
    f"  <style>\n{DARK_CSS}  </style>"
)


def lang_toggle_html(current_lang: str) -> str:
    """Return a fixed-position language toggle button linking to the other lang."""
    if current_lang == "ja":
        # On JP page, link to EN
        return (
            '<a class="lang-toggle" href="../handson-en/index.html" '
            'title="Switch to English">🌐 EN</a>'
        )
    else:
        # On EN page, link to JP
        return (
            '<a class="lang-toggle" href="../handson/index.html" '
            'title="日本語に切り替える">🌐 日本語</a>'
        )


def build_one(md_path: Path, out_dirs: list[str], lang: str) -> None:
    """Run claat export on md_path, post-process, write to each out_dir."""
    print(f"  building {md_path.name} -> {out_dirs} (lang={lang})")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        subprocess.run(
            [str(CLAAT), "export", str(md_path)],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # claat creates a folder named after the codelab id (frontmatter `id:`)
        exported = next(tmp_path.iterdir())
        src_html = (exported / "index.html").read_text()

        # Copy any new images to the deployed img/ folder
        img_src = exported / "img"
        if img_src.exists():
            img_dst = ROOT / "github-copilot-workshop" / "img"
            img_dst.mkdir(parents=True, exist_ok=True)
            for png in img_src.glob("*.png"):
                shutil.copy2(png, img_dst / png.name)

    # Post-process the HTML
    out_html = src_html.replace(CSS_MARKER, CSS_REPLACEMENT, 1)
    out_html = out_html.replace("</head>", PRISM_INJECT, 1)
    # Tag plain <pre><code> with language-none so Prism toolbar/copy attaches
    out_html = re.sub(
        r"<pre>(\s*)<code>",
        r'<pre class="language-none">\1<code class="language-none">',
        out_html,
    )
    out_html = out_html.replace("<pre>", '<pre class="language-none">')
    # Inject language toggle right after <body>
    toggle = lang_toggle_html(lang)
    out_html = re.sub(
        r"(<body[^>]*>)", r"\1\n  " + toggle, out_html, count=1
    )

    for out in out_dirs:
        out_dir = ROOT / "github-copilot-workshop" / "custom" / out
        out_dir.mkdir(parents=True, exist_ok=True)
        # Fix img paths for the custom subdirectory (../../img)
        page = out_html.replace('src="img/', 'src="../../img/')
        (out_dir / "index.html").write_text(page)


def main() -> None:
    builds = [
        (ROOT / "workshop-nikon.md", ["handson", "nikon"], "ja"),
        (ROOT / "workshop-nikon-en.md", ["handson-en", "nikon-en"], "en"),
    ]
    for md, dirs, lang in builds:
        if md.exists():
            build_one(md, dirs, lang)
        else:
            print(f"  skip {md.name} (not found)")
    print("✓ build complete")


if __name__ == "__main__":
    main()
