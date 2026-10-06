#!/usr/bin/env python3
"""Check BELL SYSTEM sewer-suction Markdown structure, links and WebP coverage.

Checks are offline: remote WordPress URLs are not HTTP-tested and Google
indexing/canonical/search-result status cannot be inferred from this script.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sewer-suction"
AREAS = (
    "al-nouf", "al-qarayen", "al-suyoh", "al-rahmaniya",
    "hoshi", "kshisha", "al-majaz", "al-khan", "al-nahda",
    "al-taawun", "al-qasimia", "muweilah",
)
ARTICLES = (
    "sewer-suction-cost-factors-sharjah",
    "suction-truck-access-hose-route",
    "sewage-lift-pump-failure-vs-tank-overflow",
    "post-suction-checklist",
    "sewer-smell-after-tank-suction",
    "building-manager-sewer-suction-log",
    "how-often-septic-tank-needs-suction-sharjah",
    "sewer-suction-vs-desludging-sharjah",
    "sewage-problem-apartment-or-building-sharjah",
    "sewer-suction-commercial-properties-sharjah",
)
REQUIRED = (
    ROOT / "README.md",
    BASE / "README.md",
    BASE / "SEO-INTENT-MAP.md",
    BASE / "SEO-WORDPRESS-CROSSWALK.md",
    BASE / "areas" / "README.md",
    BASE / "guides" / "README.md",
    BASE / "articles" / "README.md",
    BASE / "media" / "README.md",
)
LINK_RE = re.compile(r"(?P<image>!)?\[[^\]]*\]\((?P<target><[^>]+>|[^)]+)\)")
ISSUES: list[str] = []


def issue(path: Path, message: str) -> None:
    relative = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    ISSUES.append(f"{relative}: {message}")


def external_webp(target: str) -> bool:
    parsed = urlsplit(target)
    return (
        parsed.scheme == "https"
        and parsed.netloc.lower() in ("bellsystem35.com", "www.bellsystem35.com")
        and parsed.path.lower().endswith(".webp")
    )


def analyze_file(file: Path) -> tuple[int, int]:
    markdown = file.read_text(encoding="utf-8")
    links = 0
    webp_images = 0
    for match in LINK_RE.finditer(markdown):
        target = match.group("target").strip("<>")
        is_image = bool(match.group("image"))
        if target.startswith(("#", "mailto:", "tel:")):
            continue
        parts = urlsplit(target)
        if parts.scheme in {"http", "https"}:
            if is_image:
                if external_webp(target):
                    webp_images += 1
                else:
                    issue(file, f"external image is not an official HTTPS WebP: {target}")
            links += 1
            continue
        if parts.scheme:
            issue(file, f"unsupported link scheme: {target}")
            continue
        relative_target = unquote(parts.path)
        if not relative_target:
            continue
        resolved = (file.parent / relative_target).resolve()
        if not resolved.is_relative_to(ROOT):
            issue(file, f"link escapes repository: {target}")
        elif not resolved.is_file():
            issue(file, f"missing internal target: {target}")
        elif is_image and resolved.suffix.lower() != ".webp":
            issue(file, f"local image is not WebP: {target}")
        elif is_image:
            webp_images += 1
        links += 1
    return links, webp_images


def main() -> int:
    for path in REQUIRED:
        if not path.is_file():
            issue(path, "required documentation file is missing")
    for area in AREAS:
        path = BASE / "areas" / f"{area}.md"
        if not path.is_file():
            issue(path, "missing Sharjah area file")
    for article in ARTICLES:
        path = BASE / "articles" / f"{article}.md"
        if not path.is_file():
            issue(path, "missing detailed article")

    checked = 0
    total_links = 0
    for file in [ROOT / "README.md", *sorted(BASE.rglob("*.md"))]:
        if not file.is_file():
            continue
        checked += 1
        links, images = analyze_file(file)
        total_links += links
        if (file.parent == BASE / "areas" and file.name != "README.md") or (
            file.parent == BASE / "articles" and file.name != "README.md"
        ):
            if images == 0:
                issue(file, "area/article lacks an official WebP image")
    if ISSUES:
        print(f"FAIL: {len(ISSUES)} content check(s) failed")
        for error in ISSUES:
            print(" -", error)
        return 1
    print(f"PASS: {checked} Markdown files checked, {total_links} links inspected.")
    print(f"PASS: {len(AREAS)} area documents and {len(ARTICLES)} articles have WebP imagery.")
    print("NOTE: Remote URL availability, live HTML headings, canonical and indexing were not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
