# kb-frame

A knowledge frame for repositories run with AI agents (Claude Code first; the kernel is portable). It keeps the context small, the state in one place and the reasons on record.

It is packaged as an [Agent Skill](https://agentskills.io/specification): `SKILL.md` + `scripts/` + `templates/` + `references/`.

## What you get

- **`AGENTS.md` kernel** (≤4.5 KB): persona, risk tiers, boot, budgets, guardrails. `CLAUDE.md` imports it in one line.
- **Budgets with a gate:** `build_map.py` regenerates the index and exits 1 when a file is over budget.
- **Measurement:** an `InstructionsLoaded` hook logs every instruction file that enters the context. `context_report.py` reads it.
- **Hard guard:** a `PreToolUse` hook denies writes to a read-only folder and asks before touching a restricted file.
- **Two skills:** `/close` (end of session) and `/kb-audit` (health report plus fixes).
- **Templates** for live state, project Genesis, area dashboard, decisions with *why / rejected / reverts if*, dead ends, backburner, learnings.

## Install

From the root of the target repo:

```bash
git clone https://github.com/dinosaurio92/kb-frame .claude/skills/kb-frame
python3 .claude/skills/kb-frame/scripts/kb_init.py --owner "Your Name"
```

On Windows use `python` from PowerShell. `kb_init.py` never overwrites: rerun it after a `git pull` of the skill and it adds only what is missing.

Then edit `AGENTS.md` §1, §7, §8 and the two patterns at the top of `.claude/hooks/guard_writes.sh`. Full steps in `SKILL.md`.

## Layout it creates

```
AGENTS.md  CLAUDE.md  CLAUDE.local.md (gitignored)
00_System_Ops/   NOW.md  MAP.md (generated)  IA_System_Log.md  templates/
10_Projects/     <Name>/Genesis.md  Log.md  Decisions.md   Backburner.md
20_Areas/        <Name>/<Name>.md   Knowledge/Global_Learnings.md
.claude/         settings.json  hooks/guard_writes.sh  skills/close  skills/kb-audit  skills/kb-frame
```

Other folder names: `.kb-frame.json` at the root with `system`, `projects`, `areas`.

## Why

The seven principles and the numbers behind them: `references/PRINCIPLES.md`.

## License

MIT.
