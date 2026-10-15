# Doc Automation Tools

RSI (Recursive Self-Improvement) system for technical documentation workflow automation.

## Purpose

Build once, use everywhere. These tools work across all your documentation repositories to:
- Find translation gaps
- Validate content quality
- Generate templates
- Automate repetitive tasks

## Installation

```bash
# Clone this repo (already done!)
cd ~/doc-automation-tools

# Create virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

Double-click `check-all.bat` to scan every bilingual repo at once (no input
needed), or `rsi.bat` for an interactive menu.

From a shell:

```bash
# Full report for one repo
python scripts/check_translations.py /path/to/docs-repo

# One line per repo, for scanning many
python scripts/check_translations.py /path/to/docs-repo --summary
```

## Tools

### Translation Gap Finder (`scripts/check_translations.py`)
Scans zh/ and en/ folders to find:
- Missing translations
- Structure mismatches
- Coverage percentage

### Launchers
- `check-all.bat` — scans every bilingual repo found next to this one, zero input
- `rsi.bat` — interactive menu (check one repo, check all, list repos)

Both auto-detect repos, so a newly cloned docs repo shows up with no config.

## Gotcha

The Windows console is GBK. **Never emit emoji from these scripts** — it raises
`UnicodeEncodeError` as soon as output is piped. Handled via
`sys.stdout.reconfigure` plus ASCII status markers.


## RSI Philosophy

RSI here means **the agent gets better at this job every time it does the job.**
The mechanism is capturing lessons into agent memory during real work, so a
mistake or a non-obvious constraint is never re-derived.

These scripts are a *side-effect* of that process, not the process itself. A
script is only worth writing when a captured lesson is mechanical enough to
enforce automatically.

See [ROADMAP.md](ROADMAP.md) for the full definition, the failure mode this
repo already hit, and the bar a new tool has to clear.

## License

MIT - Use freely, improve continuously
