# RSI Roadmap

## What RSI actually is (corrected 2026-10-15)

RSI means **the agent gets better at this job every time it does the job.**

The mechanism is **lesson capture**, not tool-building:

1. Doing real work surfaces a surprise, a mistake, or a non-obvious constraint
2. That rule gets written into memory immediately, during the job
3. Future work reads the rule instead of re-deriving it
4. Mistakes stop repeating; each job starts from a higher floor

**Scripts in this repo are not the RSI.** They are a side-effect, worth building
only when a captured lesson is mechanical enough to enforce automatically.

### The failure mode this repo already hit

Between 2026-10-10 and 2026-10-13 the work was: build a script, build a launcher,
log the script changes, call it improvement. A re-scan on 2026-10-15 returned
byte-identical numbers across all 18 repos — proof the tool was being *built*,
not *used*.

**A loop that only improves the tool, and never touches the real job, is a fake loop.**

Real improvement from the same period lives in the agent's repo-conventions
memory, not here: image paths are case-sensitive, squash-merge looks like
divergence, prose-only product-name checks, `-UseBasicParsing` on PS 5.1.
Those stop recurring costs on every future task.

---

## Tools

### check_translations.py

Scans `zh/` and `en/`, reports missing translations, structure mismatches, and
coverage percentage.

```bash
python scripts/check_translations.py <repo-path>            # full report
python scripts/check_translations.py <repo-path> --summary  # one line
```

Launchers: `check-all.bat` (scan every bilingual repo, zero input),
`rsi.bat` (interactive menu).

**Known gotcha:** the Windows console is GBK. Never emit emoji from these
scripts — it raises `UnicodeEncodeError` when output is piped. Fixed via
`sys.stdout.reconfigure` plus ASCII markers.

---

## When to build another tool

Not on a schedule, and not by phase number. Build only when **all** hold:

1. A lesson has been captured from real work
2. It is mechanically checkable
3. The manual version has actually been done more than once

Otherwise the right move is to record the rule in memory and move on.

---

## Open questions from the last scan

- `docs-chip` and `docs-chip-pr-clean` each report 55 extra EN files —
  intentional English-only docs, or a real gap?
- Is `docs-chip-pr-clean` a scratch copy that should be excluded from scans?
- Of the 178 missing translations across 18 repos, how many are live work
  versus archived repos? If mostly archived, the tool reports noise and needs
  an ignore list.