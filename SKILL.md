---
name: kb-frame
description: Knowledge frame for repos run with AI agents. Use it to install the frame in a new repo (kernel AGENTS.md, budgets, close and audit skills, hooks), to check a repo against its seven principles, or when the user asks how to organize instructions, memory and project state for Claude Code or another agent.
---

# kb-frame — a knowledge frame for agent-run repos

The frame keeps the context small, the state in one place and the reasons on record. Seven principles in `references/PRINCIPLES.md`. This skill installs and maintains it.

## Install in a repo

Run from the target repo root. Never from inside this skill's own clone.

1. Put this skill at `.claude/skills/kb-frame/` (clone, submodule or copy).
2. Run `python3 .claude/skills/kb-frame/scripts/kb_init.py --owner "<Name>"` (`python` on Windows). It writes the skeleton and skips every file that exists. Use `--dry-run` first to see the list.
3. Open `AGENTS.md`. Edit §1 (persona), §7 (the two protected paths) and §8. Set the same two paths at the top of `.claude/hooks/guard_writes.sh`.
4. If `.claude/settings.json` existed before, merge the two hooks from `templates/claude/settings.json` by hand.
5. Create the first project from `<system>/templates/Genesis_Template.md`, then run `build_map.py`. Commit.

A non-default layout goes in `.kb-frame.json` at the root: `{"system": "...", "projects": "...", "areas": "..."}`.

## Maintain

- Every session that changed state ends with `/close`.
- Every two weeks, or before a big session, `/kb-audit`.
- `scripts/context_report.py` shows what loaded in the last sessions and what it cost. Read it when the fixed path grows.
- Update the skill with `git pull` inside `.claude/skills/kb-frame/`. Rerun `kb_init.py`: it only adds what is missing.

## Check a repo against the frame

Answer each line with yes or no, then fix the first no.

1. Fixed load path (user CLAUDE.md + AGENTS.md + CLAUDE.md + CLAUDE.local.md) ≤8 KB? `kb_audit.py` section 4 prints it.
2. One kernel for every tool (`AGENTS.md`), with the tool layer importing it?
3. Three state layers and nothing else in the load path: critical facts in the kernel, a generated index, one bounded unit of work?
4. Budgets enforced by a script that blocks the close, not by a sentence?
5. Hard prohibitions enforced by a `PreToolUse` hook?
6. Procedures as skills with a trigger in the description, body under 5,000 tokens?
7. Decisions recorded with why, rejected and reverts-if? Dead ends recorded?
8. History and big corpora retrieved on demand, never preloaded? Heavy research in a subagent?
9. Each datum with one owner: preferences in auto memory, state in the repo, machine facts in `CLAUDE.local.md`?

## Scripts

| Script | What | Exit |
| :--- | :--- | :--- |
| `kb_init.py` | Install the skeleton, never overwrite | 0 |
| `build_map.py` | Regenerate `MAP.md`, enforce budgets | 1 on a broken budget |
| `kb_audit.py` | Read-only health report, five sections | 0 always |
| `context_report.py` | What loaded per session, from the hook log | 1 if no log |

All scripts find the root with `git rev-parse --show-toplevel` from the cwd. Python 3.10+, standard library only.
