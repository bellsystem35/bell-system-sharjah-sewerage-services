#!/usr/bin/env python3
"""Offline structure check for BELL SYSTEM drain-cleaning documentation."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "drain-cleaning"

REQUIRED = (
    BASE / "README.md",
    BASE / "SEO-INTENT-MAP.md",
    BASE / "SEO-WORDPRESS-CROSSWALK.md",
    BASE / "WORDPRESS-QUALITY-AUDIT-2026-10-08.md",
    BASE / "ARTICLE-INTENT-AUDIT-2026-10-08.md",
    BASE / "areas" / "README.md",
    BASE / "articles" / "README.md",
    BASE / "media" / "README.md",
)

AREA_FILES = (
    "al-majaz.md", "al-khan.md", "al-nahda.md", "al-taawun.md",
    "al-qasimia.md", "muwaileh.md", "al-nouf.md", "al-qarain.md",
    "al-suyoh.md", "al-rahmaniya.md", "hoshi.md", "kshisha.md",
)

CORE_URLS = (
    "https://bellsystem35.com/خدمة-تنظيف-بالوعات/",
    "https://bellsystem35.com/تنظيف-بالوعات-المجاري-في-مناطق-الشارقة/",
    "https://bellsystem35.com/تسليك-بالوعات-المجاري-في-الشارقة/",
    "https://bellsystem35.com/تسليك-مجاري-في-الشارقة-فتح-الانسدادات/",
    "https://bellsystem35.com/شفط-المجاري/",
)

CORE_IDS = ("ID 105", "ID 2374", "ID 1080", "ID 114", "ID 132")

def main() -> int:
    errors = []

    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    for name in AREA_FILES:
        path = BASE / "areas" / name
        if not path.is_file():
            errors.append(f"missing area file: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    hub = (BASE / "README.md").read_text(encoding="utf-8")
    all_docs = "\n".join(path.read_text(encoding="utf-8") for path in REQUIRED)

    for url in CORE_URLS:
        if url not in hub and url not in all_docs:
            errors.append(f"documentation missing core URL: {url}")

    for marker in CORE_IDS:
        if marker not in all_docs:
            errors.append(f"documentation missing authority marker: {marker}")

    if "+971528913062" not in hub:
        errors.append("hub missing official contact number")

    if "http://" in all_docs:
        errors.append("documentation contains non-HTTPS URL")

    area_index = (BASE / "areas" / "README.md").read_text(encoding="utf-8")
    for name in AREA_FILES:
        if name not in area_index:
            errors.append(f"area index missing link: {name}")

    if errors:
        print(f"FAIL: {len(errors)} drain-cleaning documentation check(s) failed")
        for error in errors:
            print(" -", error)
        return 1

    print("PASS: drain-cleaning documentation structure is complete.")
    print("PASS: 12 Sharjah area files and core WordPress authority pages are documented.")
    print("NOTE: this check does not verify Google indexing, rankings, canonicals or live page rendering.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
