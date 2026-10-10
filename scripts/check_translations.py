#!/usr/bin/env python3
"""
Translation Gap Finder - Phase 1 RSI Tool

Scans zh/ and en/ directories to find translation gaps.
Reports missing files, structure mismatches, and translation status.

Usage:
    python check_translations.py <docs-repo-path>
    python check_translations.py .
"""

import sys
from pathlib import Path
from typing import Set, Dict, List, Tuple


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
        "stats": {
            "total_zh": total_zh,
            "total_en": total_en,
            "translated": translated,
            "missing": len(missing_en_files),
            "extra": len(extra_en_files),
            "coverage_pct": round(translated / total_zh * 100, 1) if total_zh > 0 else 0
        }
    }


def print_report(result: Dict) -> None:
    """Print human-readable report."""
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    stats = result["stats"]
    
    print("=" * 70)
    print("📊 TRANSLATION GAP REPORT")
    print("=" * 70)
    print(f"Repository: {result['base_path']}")
    print()
    
    print("📈 Statistics:")
    print(f"  Chinese files (zh/):    {stats['total_zh']}")
    print(f"  English files (en/):    {stats['total_en']}")
    print(f"  Fully matched:          {stats['translated']}")
    print(f"  Missing translations:   {stats['missing']}")
    print(f"  Extra English files:    {stats['extra']}")
    print(f"  Translation coverage:   {stats['coverage_pct']}%")
    print()
    
    if result["missing_en_files"]:
        print("❌ Missing English Translations:")
        for f in result["missing_en_files"]:
            print(f"  - {f}")
        print()
    
    if result["extra_en_files"]:
        print("⚠️  Extra English Files (no Chinese source):")
        for f in result["extra_en_files"]:
            print(f"  - {f}")
        print()
    
    if result["missing_en_dirs"]:
        print("📁 Missing English Directories:")
        for d in result["missing_en_dirs"]:
            print(f"  - {d}/")
        print()
    
    if result["extra_en_dirs"]:
        print("📁 Extra English Directories:")
        for d in result["extra_en_dirs"]:
            print(f"  - {d}/")
        print()
    
    if not any([result["missing_en_files"], result["extra_en_files"], 
                result["missing_en_dirs"], result["extra_en_dirs"]]):
        print("✅ Perfect! All files are synchronized between zh/ and en/")
        print()
    
    print("=" * 70)
    print("💡 Next Steps:")
    if result["missing_en_files"]:
        print("  1. Translate missing files")
        print("  2. Run this tool again to verify")
    if result["extra_en_files"]:
        print("  - Review extra English files (might be English-only docs)")
    if stats['coverage_pct'] == 100 and not result["extra_en_files"]:
        print("  - Build Phase 2 tool: Content validator")
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_translations.py <docs-repo-path>")
        print("Example: python check_translations.py ~/docs-product")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    result = check_translations(repo_path)
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
