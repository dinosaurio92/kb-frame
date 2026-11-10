---
name: close
description: Close ritual of this repo. Run at the end of any session that changed project or system state. Updates NOW.md and frontmatter, resolves stale deadlines, regenerates MAP.md, logs if needed, commits and pushes.
---

# /close — Close ritual

Run the steps in order. Stop and tell {{OWNER}} if a step fails.

1. **State.** Update `{{SYSTEM}}/NOW.md` (next action, blocker, deadline) within its budget: ≤4 KB, ≤3 lines per project. Narrative state belongs in the project's `Genesis.md`, not here.
2. **Frontmatter.** Set `updated` and `next` (≤140 characters) in every Genesis or area file whose state moved.
3. **Genesis budget.** If a `Genesis.md` is over 6 KB, move finished sprints and session notes to `Log.md` and closed decisions to `Decisions.md` in the same folder. Leave a pointer under `## Project files`.
4. **Stale deadlines.** Any date now in the past is closed or the project is re-scoped. Never leave an expired deadline shown as live.
5. **Eviction.** A project with no movement in 21 days goes to `{{PROJECTS}}/Backburner.md` with enough state to resume.
6. **Index.** Run `python3 .claude/skills/kb-frame/scripts/build_map.py` from the repo root (Linux, macOS or web). On Windows run `python .claude/skills/kb-frame/scripts/build_map.py` from PowerShell. It fails on a broken budget: fix the file it names, then rerun.
7. **Ledger.** Add one line to `{{SYSTEM}}/IA_System_Log.md` only if money, legal status or system rules changed.
8. **Decisions and dead ends.** A decision closed this session gets one row in the project's `Decisions.md`: why, what was rejected, what would revert it. Something tried and dropped gets one row under *Dead ends*. Template: `{{SYSTEM}}/templates/Decisions_Template.md`. Create the file if it does not exist.
9. **Learnings.** If something failed or was redone this session, add one dated line with the root cause to `{{AREAS}}/Knowledge/Global_Learnings.md`. Project-specific lessons go to step 8, not here.
10. **Git.** `git fetch origin main` first. Content → commit to `main`. System or structure → branch + PR. Commit only the files of this session. Then push.

Done means verified: after the push, confirm `git status` is clean for the files you touched.
