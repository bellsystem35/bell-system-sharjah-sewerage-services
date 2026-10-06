#!/usr/bin/env python3
"""Offline structure check for BELL SYSTEM drain-unclogging documentation."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "drain-unclogging"

REQUIRED = (
    BASE / "README.md",
    BASE / "SEO-INTENT-MAP.md",
    BASE / "SEO-WORDPRESS-CROSSWALK.md",
    BASE / "WORDPRESS-QUALITY-AUDIT-2026-10-06.md",
    BASE / "ARTICLE-INTENT-AUDIT-2026-10-06.md",
)

OFFICIAL_URLS = (
    "https://bellsystem35.com/تسليك-مجاري-في-الشارقة-فتح-الانسدادات/",
    "https://bellsystem35.com/دليل-مناطق-تسليك-مجاري-الصرف-الصحي-في-الشارقة/",
    "https://bellsystem35.com/تسليك-مجاري-بالضغط-في-الشارقة/",
    "https://bellsystem35.com/خدمة-تنظيف-بالوعات/",
    "https://bellsystem35.com/تسليك-بالوعات-المجاري-في-الشارقة/",
)

AREA_NAMES = (
    "المجاز", "الخان", "النهدة", "التعاون", "القاسمية", "مويلح",
    "النوف", "القرائن", "السيوح", "الرحمانية", "حوشي", "كشيشة",
)

def main() -> int:
    errors = []
    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    hub = (BASE / "README.md").read_text(encoding="utf-8")
    all_docs = "\n".join(path.read_text(encoding="utf-8") for path in REQUIRED)

    for url in OFFICIAL_URLS:
        if url not in hub:
            errors.append(f"hub missing official URL: {url}")

    for area in AREA_NAMES:
        if area not in hub:
            errors.append(f"hub missing area: {area}")

    if "+971528913062" not in hub:
        errors.append("hub missing official contact number")

    if "http://" in all_docs:
        errors.append("documentation contains non-HTTPS web URL")

    for marker in ("ID 114", "ID 2494", "ID 1077", "ID 105", "ID 1080"):
        if marker not in all_docs:
            errors.append(f"documentation missing authority marker: {marker}")

    if errors:
        print(f"FAIL: {len(errors)} drain-unclogging documentation check(s) failed")
        for error in errors:
            print(" -", error)
        return 1

    print("PASS: drain-unclogging documentation structure is complete.")
    print("PASS: 12 Sharjah areas and core WordPress authority IDs are documented.")
    print("NOTE: live URLs, indexing, canonical selection and rankings are not checked.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
