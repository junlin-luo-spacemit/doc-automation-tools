#!/usr/bin/env python3
"""
Translation Gap Finder - Phase 1 RSI Tool

Scans zh/ and en/ directories to find translation gaps.
Reports missing files, structure mismatches, and translation status.

Usage:
    python check_translations.py <docs-repo-path>
    python check_translations.py . --summary
    python check_translations.py . --claims   # handoff table for the review AI
"""

import sys
from pathlib import Path
from typing import Set, Dict, List, Tuple

# Console codepages such as GBK cannot encode this report's output when piped.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def get_empty_files(base_path: Path, lang: str) -> List[Path]:
    """Zero-byte .md files. Placeholders that silently pass a presence check."""
    lang_dir = base_path / lang
    if not lang_dir.exists():
        return []
    return sorted(
        f.relative_to(lang_dir)
        for f in lang_dir.rglob("*.md")
        if f.stat().st_size == 0
    )


def count_headings(base_path: Path, lang: str) -> int:
    """Count lines starting with # as a rough size-parity signal, not a structure check."""
    lang_dir = base_path / lang
    if not lang_dir.exists():
        return 0
    total = 0
    for md_file in lang_dir.rglob("*.md"):
        with open(md_file, encoding="utf-8", errors="replace") as fh:
            total += sum(1 for line in fh if line.lstrip().startswith("#"))
    return total


def get_doc_files(base_path: Path, lang: str) -> Set[Path]:
    """Get all .md files in a language directory, relative to lang root."""
    lang_dir = base_path / lang
    if not lang_dir.exists():
        return set()
    
    md_files = set()
    for md_file in lang_dir.rglob("*.md"):
        # Get path relative to the language directory
        rel_path = md_file.relative_to(lang_dir)
        md_files.add(rel_path)
    
    return md_files


def get_directories(base_path: Path, lang: str) -> Set[Path]:
    """Get all directories in a language folder, relative to lang root."""
    lang_dir = base_path / lang
    if not lang_dir.exists():
        return set()
    
    dirs = set()
    for item in lang_dir.rglob("*"):
        if item.is_dir() and item.name != "static":
            rel_path = item.relative_to(lang_dir)
            dirs.add(rel_path)
    
    return dirs


def check_translations(repo_path: str) -> Dict[str, any]:
    """Main analysis function."""
    base = Path(repo_path).resolve()
    
    if not base.exists():
        return {"error": f"Path does not exist: {base}"}
    
    zh_dir = base / "zh"
    en_dir = base / "en"
    
    if not zh_dir.exists() and not en_dir.exists():
        return {"error": f"No zh/ or en/ directories found in {base}"}
    
    # Get files and directories
    zh_files = get_doc_files(base, "zh")
    en_files = get_doc_files(base, "en")
    zh_dirs = get_directories(base, "zh")
    en_dirs = get_directories(base, "en")
    
    # Find gaps
    missing_en_files = zh_files - en_files
    extra_en_files = en_files - zh_files
    missing_en_dirs = zh_dirs - en_dirs
    extra_en_dirs = en_dirs - zh_dirs
    
    # Calculate stats
    total_zh = len(zh_files)
    total_en = len(en_files)
    translated = len(zh_files & en_files)
    
    return {
        "base_path": str(base),
        "zh_files": sorted([str(f) for f in zh_files]),
        "en_files": sorted([str(f) for f in en_files]),
        "missing_en_files": sorted([str(f) for f in missing_en_files]),
        "extra_en_files": sorted([str(f) for f in extra_en_files]),
        "missing_en_dirs": sorted([str(d) for d in missing_en_dirs]),
        "extra_en_dirs": sorted([str(d) for d in extra_en_dirs]),
        "empty_zh_files": [str(f) for f in get_empty_files(base, "zh")],
        "empty_en_files": [str(f) for f in get_empty_files(base, "en")],
        "headings_zh": count_headings(base, "zh"),
        "headings_en": count_headings(base, "en"),
        "stats": {
            "total_zh": total_zh,
            "total_en": total_en,
            "translated": translated,
            "missing": len(missing_en_files),
            "extra": len(extra_en_files),
            "coverage_pct": round(translated / total_zh * 100, 1) if total_zh > 0 else 0
        }
    }


def print_summary(result: Dict, label: str) -> None:
    """Print a single aligned line, for scanning many repos at once."""
    if "error" in result:
        print(f"{label:<24} ERROR  {result['error']}")
        return

    stats = result["stats"]
    flag = "OK " if stats["missing"] == 0 and stats["extra"] == 0 else "GAP"
    print(
        f"{label:<24} {flag}  {stats['coverage_pct']:>5.1f}%  "
        f"zh={stats['total_zh']:<4} en={stats['total_en']:<4} "
        f"missing={stats['missing']:<4} extra={stats['extra']}"
    )


def print_report(result: Dict) -> None:
    """Print human-readable report."""
    if "error" in result:
        print(f"[ERROR] {result['error']}")
        return
    
    stats = result["stats"]
    
    print("=" * 70)
    print("TRANSLATION GAP REPORT")
    print("=" * 70)
    print(f"Repository: {result['base_path']}")
    print()
    
    print("Statistics:")
    print(f"  Chinese files (zh/):    {stats['total_zh']}")
    print(f"  English files (en/):    {stats['total_en']}")
    print(f"  Fully matched:          {stats['translated']}")
    print(f"  Missing translations:   {stats['missing']}")
    print(f"  Extra English files:    {stats['extra']}")
    print(f"  Translation coverage:   {stats['coverage_pct']}%")
    print()
    
    if result["missing_en_files"]:
        print("Missing English Translations:")
        for f in result["missing_en_files"]:
            print(f"  - {f}")
        print()
    
    if result["extra_en_files"]:
        print("Extra English Files (no Chinese source):")
        for f in result["extra_en_files"]:
            print(f"  - {f}")
        print()
    
    if result["missing_en_dirs"]:
        print("Missing English Directories:")
        for d in result["missing_en_dirs"]:
            print(f"  - {d}/")
        print()
    
    if result["extra_en_dirs"]:
        print("Extra English Directories:")
        for d in result["extra_en_dirs"]:
            print(f"  - {d}/")
        print()
    
    if not any([result["missing_en_files"], result["extra_en_files"], 
                result["missing_en_dirs"], result["extra_en_dirs"]]):
        print("OK - all files are synchronized between zh/ and en/")
        print()
    
    print("=" * 70)
    print("Next Steps:")
    if result["missing_en_files"]:
        print("  1. Translate missing files")
        print("  2. Run this tool again to verify")
    if result["extra_en_files"]:
        print("  - Review extra English files (might be English-only docs)")
    if stats['coverage_pct'] == 100 and not result["extra_en_files"]:
        print("  - Build Phase 2 tool: Content validator")
    print("=" * 70)


def print_claims(result: Dict, label: str) -> None:
    """Emit a handoff claims table for the review AI.

    Deterministic facts only, each paired with the command that reproduces it.
    Translation fidelity is out of scope here and must be reviewed by reading.
    """
    if "error" in result:
        print(f"[ERROR] {result['error']}")
        return

    stats = result["stats"]
    rows = [
        ("zh/ .md file count",
         f"Get-ChildItem {label}\\zh -Recurse -Filter *.md | Measure-Object",
         str(stats["total_zh"])),
        ("en/ .md file count",
         f"Get-ChildItem {label}\\en -Recurse -Filter *.md | Measure-Object",
         str(stats["total_en"])),
        ("matched pairs",
         "compare the two listings above",
         str(stats["translated"])),
        ("missing translations",
         "see list below",
         str(stats["missing"])),
        ("extra English files",
         "see list below",
         str(stats["extra"])),
        ("empty zh/ files",
         f"Get-ChildItem {label}\\zh -Recurse -Filter *.md | Where-Object Length -eq 0",
         str(len(result["empty_zh_files"]))),
        ("empty en/ files",
         f"Get-ChildItem {label}\\en -Recurse -Filter *.md | Where-Object Length -eq 0",
         str(len(result["empty_en_files"]))),
        ("zh heading lines",
         f'Select-String -Path {label}\\zh\\*.md -Pattern "^#" -AllMatches | Measure-Object',
         str(result["headings_zh"])),
        ("en heading lines",
         f'Select-String -Path {label}\\en\\*.md -Pattern "^#" -AllMatches | Measure-Object',
         str(result["headings_en"])),
    ]

    print("=" * 70)
    print(f"REVIEW HANDOFF - {label}")
    print("=" * 70)
    print("Reviewer: reproduce every claim below with the given command.")
    print("Do not accept a claim by reading it. Any unverified row blocks PASS.")
    print()
    print("| # | Claim | Reproduce with | Expected | Verified |")
    print("|---|-------|----------------|----------|----------|")
    for i, (claim, cmd, expected) in enumerate(rows, 1):
        print(f"| {i} | {claim} | `{cmd}` | {expected} | |")
    print()

    if result["empty_zh_files"]:
        print("Empty zh/ files (placeholders - a presence check passes them silently):")
        for f in result["empty_zh_files"]:
            print(f"  - zh/{f}")
        print()

    if result["empty_en_files"]:
        print("Empty en/ files:")
        for f in result["empty_en_files"]:
            print(f"  - en/{f}")
        print()

    if result["missing_en_files"]:
        print("Missing English translations:")
        for f in result["missing_en_files"]:
            print(f"  - {f}")
        print()

    if result["extra_en_files"]:
        print("Extra English files (no Chinese source to verify against):")
        for f in result["extra_en_files"]:
            print(f"  - {f}")
        print()

    print("-" * 70)
    print("Out of scope for this table (reviewer must check by reading):")
    print("  - translation fidelity of any matched pair")
    print("  - image and link targets resolving to real files")
    print("  - terminology and tone consistency")
    print("  - whether heading totals reflect real structural parity")
    print("-" * 70)
    print("Verdict (reviewer fills in): PASS / PASS WITH GAPS / FAIL")
    print("=" * 70)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    summary = "--summary" in sys.argv[1:]
    claims = "--claims" in sys.argv[1:]

    if not args:
        print("Usage: python check_translations.py <docs-repo-path> [--summary|--claims]")
        print("Example: python check_translations.py ~/docs-product")
        sys.exit(1)
    
    repo_path = args[0]
    result = check_translations(repo_path)
    if claims:
        print_claims(result, Path(repo_path).resolve().name)
    elif summary:
        print_summary(result, Path(repo_path).resolve().name)
    else:
        print_report(result)
    
    # Exit code indicates if there are gaps
    if "error" in result:
        sys.exit(2)
    elif result["stats"]["missing"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
