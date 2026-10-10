# RSI Roadmap

## Philosophy

This system follows **Recursive Self-Improvement (RSI)** principles:

1. Build one tool at a time
2. Use it until patterns emerge
3. Let real usage drive the next tool
4. Each tool makes building the next one easier

**Don't build ahead. Build what's needed, informed by what's used.**

---

## Phase 1: Translation Gap Finder ✅

**Status:** Live and testing

**What it does:**
- Scans zh/ and en/ directories
- Reports missing translations
- Shows structure mismatches
- Calculates coverage percentage

**Tool:** `scripts/check_translations.py`

**Trigger phrases for Phase 2:**
- "links keep breaking"
- "images missing"
- "formatting inconsistent"
- "terminology all over the place"
- "build next tool"

---

## Phase 2: Content Validator

**Status:** Not started - waiting for Phase 1 insights

**What it will do** (tentative, may change based on actual needs):
- Validate internal links
- Check image references
- Verify formatting consistency
- Style guide compliance
- Terminology consistency

**Will build when:**
- Phase 1 has been used across multiple repos
- Clear validation pain points emerge
- User reports manual checking friction

**Trigger phrases for Phase 3:**
- "can you auto-fix this?"
- "tired of fixing manually"
- "generate templates"
- "automate the fixes"

---

## Phase 3: Auto-Fixer & Generator

**Status:** Not started - depends on Phase 2 findings

**What it might do:**
- Auto-fix common issues found by Phase 2
- Generate boilerplate from templates
- Suggest translations for repeated terms
- Batch corrections

**Will build when:**
- Phase 2 reveals fixable patterns
- Manual fixing becomes repetitive
- Clear automation opportunities emerge

**Trigger phrases for Phase 4:**
- "show me patterns"
- "what's most broken?"
- "analytics time"
- "track improvements"

---

## Phase 4: Analytics & Insights

**Status:** Not started - depends on usage data

**What it might do:**
- Track what issues appear most
- Measure time saved
- Identify documentation debt
- Suggest next automations
- Generate reports

**Will build when:**
- Multiple tools generate useful data
- Need to prioritize improvements
- Want to measure impact

**Trigger phrases for Phase 5:**
- "tool to build tools"
- "meta level"
- "workflow optimizer"

---

## Phase 5: Meta-Tools

**Status:** Conceptual - far future

**What it might do:**
- Tools that generate new tools
- Workflow optimization
- Template-based tool creation
- True RSI: tools building tools

**Will build when:**
- Clear patterns in tool structure emerge
- Enough tools exist to abstract
- Need to accelerate tool creation

---

## How to Move Forward

### You Tell Me When Ready:

**Simple triggers:**
- "ready for Phase X"
- "build next tool"
- "let's move forward"

**Or describe your pain:**
- "I keep doing X manually"
- "This is getting repetitive"
- "Can we automate Y?"

### I'll Suggest When:

- You report friction multiple times
- Clear patterns emerge from your work
- Tool logs reveal opportunities
- But only after real usage, never prematurely

---

## Design Principles

1. **Start minimal** - Solve one problem well
2. **Use immediately** - Test on real repos right away
3. **Iterate fast** - Fix and improve based on feedback
4. **Build on success** - Each tool informs the next
5. **Stay focused** - Don't add features that aren't needed
6. **Measure impact** - Know what's working

---

## Current Testing

- [x] docs-product: 100% translation coverage ✅
- [ ] docs-ros: Not tested yet
- [ ] Other repos: Not tested yet

**Next action:** Use Phase 1 across all repos for 1-2 weeks, note friction points.
