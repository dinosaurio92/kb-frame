---
type: project
status: active | running | parked
tier: T1 | T2 | T3
updated: YYYY-MM-DD
next: "one line, ≤140 characters — the next concrete action"
---

# Project Genesis: [Project Name]

> Budget: this file stays ≤6 KB (`AGENTS.md §4`). It holds state, not history.
> Finished sprints and session notes → `Log.md`. Closed decisions → `Decisions.md`. Same folder.

## 1. Lean Kickoff
- **Why:** [the reason or vision driving this project]
- **Goal:** [what exactly is built or achieved]
- **Done (QA criteria):** [the checks that prove it is good enough — verified, not written]
- **Out:** [what is explicitly out of scope]

## 2. Guardrails
- **Tier:** [T1 | T2 | T3 — `AGENTS.md §2`]
- **Decision pass (T3 only):** strongest counterargument · what evidence would change the call · confidence.

## 3. Current state (YYYY-MM-DD)
- [3-6 lines: what exists today, what is blocked, what is next]

## 4. Open decisions
- [one line per decision waiting on {{OWNER}}]

## Project files
- [`Log.md`](Log.md) — sprints and session log (create on the first close)
- [`Decisions.md`](Decisions.md) — closed decisions (why, rejected, reverts if) and dead ends. Template: `{{SYSTEM}}/templates/Decisions_Template.md`
