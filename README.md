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

```bash
# Check translation gaps in any docs repo
python scripts/check_translations.py /path/to/docs-repo

# Example: Use in docs-product
cd ~/docs-product
python ~/doc-automation-tools/scripts/check_translations.py .
```

## Tools

### 1. Translation Gap Finder (`check_translations.py`)
Scans zh/ and en/ folders to find:
- Missing translations
- Structure mismatches
- Incomplete documentation

**Usage:**
```bash
python scripts/check_translations.py <repo-path>
```

## VS Code Integration

Add to your docs repo's `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Check Translations",
      "type": "shell",
      "command": "python",
      "args": [
        "${env:HOME}/doc-automation-tools/scripts/check_translations.py",
        "${workspaceFolder}"
      ],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

Then run with `Ctrl+Shift+B` or Command Palette → "Tasks: Run Task".

## RSI Philosophy

Each tool:
1. Solves a real problem
2. Reveals new patterns
3. Informs the next tool
4. Compounds your productivity

Build → Use → Learn → Improve → Repeat

## Roadmap

- [x] Phase 1: Translation gap finder
- [ ] Phase 2: Content validator (links, images, formatting)
- [ ] Phase 3: Auto-fixer and generators
- [ ] Phase 4: Analytics and insights
- [ ] Phase 5: Meta-tools (tools that build tools)

## License

MIT - Use freely, improve continuously
