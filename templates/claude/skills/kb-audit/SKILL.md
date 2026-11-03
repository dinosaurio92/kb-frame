---
name: kb-audit
description: Health check of this knowledge base. Run it when {{OWNER}} asks for an audit, before a big session, or every two weeks. Finds budget breaks, expired dates in NOW.md, projects to evict, instruction-load growth and Genesis files without frontmatter, then fixes them.
---

# /kb-audit — Knowledge base audit

Read-only report first, fixes second. Stop and tell {{OWNER}} if a step fails.

1. **Report.** Run `python3 .claude/skills/kb-frame/scripts/kb_audit.py` from the repo root (Linux, macOS or web). On Windows run `python .claude/skills/kb-frame/scripts/kb_audit.py` from PowerShell. Keep the output: it is the checklist.
2. **Budgets.** For each WARN or ERROR, apply `/close` step 3: history to `Log.md`, closed decisions to `Decisions.md`, `next` under 140 characters, `NOW.md` under 4 KB.
3. **Expired dates.** For each line listed: the event happened or it did not. Happened: remove the line or mark it done. Did not: re-scope with a new date, or move the item to the project's `Genesis.md` as a blocker. Never leave a past date shown as live.
4. **Eviction.** For each candidate: confirm the last real movement with `git log -1 --format=%cs -- <folder>`. No movement: one row in `{{PROJECTS}}/Backburner.md` with enough state to resume, and frontmatter `status: parked`. Movement: set `updated` to that date.
5. **Instructions.** If the fixed path is over 8 KB, move text out of `AGENTS.md` or `CLAUDE.md` into a skill or a rule with `paths:`. Rules that never load are free; rules that load every session are not.
6. **Hygiene.** A Genesis without frontmatter gets the header from `{{SYSTEM}}/templates/Genesis_Template.md`.
7. **Verify.** Run the audit again. Then `build_map.py`. Report the before and after counts to {{OWNER}} in one line.
8. **Git.** Content fixes → commit to `main` and push. A change to `AGENTS.md`, `CLAUDE.md`, a skill or a rule → branch + PR.
