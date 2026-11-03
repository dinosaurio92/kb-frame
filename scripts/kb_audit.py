#!/usr/bin/env python3
"""kb_audit.py - health report of the knowledge base. Read-only, exit 0 always.

    python3 .claude/skills/kb-frame/scripts/kb_audit.py   # Linux / macOS / web
    python  .claude/skills/kb-frame/scripts/kb_audit.py   # Windows, PowerShell

Run it from the target repo: the root is the git toplevel of the cwd.

Sections (each prints OK or a list to act on):
  1. Budgets        - same checks as build_map.py (next, Genesis, NOW).
  2. Expired dates  - past dates still shown as live in NOW.md.
  3. Eviction       - active projects with no movement in EVICT_DAYS.
  4. Instructions   - bytes of every file that loads at session start.
  5. Hygiene        - Genesis files without frontmatter.

The skill /kb-audit reads this output and fixes what it names.
"""
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_map  # noqa: E402  (shares constants and checks)
from kb_paths import CONTEXT_LOG, NOW, PROJECTS, ROOT  # noqa: E402

EVICT_DAYS = 21
FIXED_LOAD_WARN = 8000  # bytes: user CLAUDE.md + AGENTS + CLAUDE + CLAUDE.local

MONTHS = {
    # Spanish and English three-letter abbreviations
    "ene": 1, "jan": 1, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "may": 5,
    "jun": 6, "jul": 7, "ago": 8, "aug": 8, "sep": 9, "oct": 10,
    "nov": 11, "dic": 12, "dec": 12,
}
ISO = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")
SHORT = re.compile(r"\b(\d{1,2})-(" + "|".join(MONTHS) + r")\b", re.I)
CLOSED = re.compile(r"vencid|hecho|done|expired|closed|OK\b|✅|cerrad", re.I)
LIVE_END = "## Areas on Watch"   # NOW.md zone after this header is not audited

TODAY = date.today()


def section(title):
    print(f"\n== {title} ==")


def dates_in(line):
    out = []
    for y, m, d in ISO.findall(line):
        try:
            out.append(date(int(y), int(m), int(d)))
        except ValueError:
            pass
    for d, mon in SHORT.findall(line):
        try:
            out.append(date(TODAY.year, MONTHS[mon.lower()], int(d)))
        except ValueError:
            pass
    return out


def audit_budgets(entries):
    section("1. Budgets (build_map rules)")
    errors, warnings = build_map.check_budget(entries)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors and not warnings:
        print("OK")
    return len(errors) + len(warnings)


def audit_now_dates():
    section(f"2. Expired dates in NOW.md (before {TODAY})")
    if not NOW.exists():
        print("NOW.md missing (counted in section 1)")
        return 0
    text = NOW.read_text(encoding="utf-8")
    live = text.split(LIVE_END)[0]
    hits = 0
    for n, line in enumerate(live.splitlines(), 1):
        if line.startswith("**Last updated"):
            continue
        found = dates_in(line)
        # A line with a future date is still live. Flag it only when its
        # latest date is past and nothing says it was closed.
        if found and max(found) < TODAY and not CLOSED.search(line):
            hits += 1
            print(f"L{n}: {max(found)} -> {line.strip()[:110]}")
    if not hits:
        print("OK")
    return hits


def audit_eviction(entries):
    section(f"3. Eviction candidates (active, updated > {EVICT_DAYS} days ago)")
    limit = TODAY - timedelta(days=EVICT_DAYS)
    hits = 0
    for e in entries:
        if e.get("type") != "project" or e.get("status") not in ("active", "running"):
            continue
        try:
            upd = datetime.strptime(e.get("updated", ""), "%Y-%m-%d").date()
        except ValueError:
            hits += 1
            print(f"{e['path']}: updated='{e.get('updated', '')}' is not a date")
            continue
        if upd < limit:
            hits += 1
            print(f"{e['path']}: updated {upd} ({(TODAY - upd).days} d) -> Backburner or re-scope")
    if not hits:
        print("OK")
    return hits


def audit_instructions():
    section("4. Instruction files that load at session start")
    fixed = 0
    rows = []
    for p in [Path.home() / ".claude" / "CLAUDE.md", ROOT / "AGENTS.md",
              ROOT / "CLAUDE.md", ROOT / "CLAUDE.local.md"]:
        if p.exists():
            b = p.stat().st_size
            fixed += b
            rows.append((b, "fixed", p.name))
    for p in sorted((ROOT / ".claude" / "rules").glob("*.md")):
        rows.append((p.stat().st_size, "on paths:", f"rules/{p.name}"))
    for p in sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        rows.append((p.stat().st_size, "on demand", f"skills/{p.parent.name}"))
    for b, when, name in rows:
        print(f"{b:>6} B  {when:<9} {name}")
    print(f"{fixed:>6} B  fixed path total (~{fixed // 4} tokens)"
          + ("  WARN over " + str(FIXED_LOAD_WARN) if fixed > FIXED_LOAD_WARN else ""))
    if CONTEXT_LOG.exists():
        last = {}
        for raw in CONTEXT_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                ev = json.loads(raw)["event"]
                last.setdefault(ev["session_id"], []).append(ev["file_path"])
            except (ValueError, KeyError):
                continue
        if last:
            sid, files = list(last.items())[-1]
            print(f"last logged session {sid[:8]}: {len(files)} loads")
    return 1 if fixed > FIXED_LOAD_WARN else 0


def audit_hygiene():
    section("5. Genesis files without frontmatter")
    hits = 0
    for p in sorted(PROJECTS.glob("*/Genesis.md")) if PROJECTS.exists() else []:
        if build_map.read_frontmatter(p) is None:
            hits += 1
            print(p.relative_to(ROOT).as_posix())
    if not hits:
        print("OK")
    return hits


def main():
    entries = build_map.collect()
    total = 0
    total += audit_budgets(entries)
    total += audit_now_dates()
    total += audit_eviction(entries)
    total += audit_instructions()
    total += audit_hygiene()
    print(f"\n{total} item(s) to act on." if total else "\nClean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
