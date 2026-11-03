# CLAUDE.md — Claude Code layer

The operating system is `AGENTS.md`. It loads here in full:

@AGENTS.md

What follows applies only to Claude Code.

- **Close:** skill `/close` (`.claude/skills/close/`). Run it at the end of any session that changed project or system state.
- **Audit:** skill `/kb-audit` every two weeks or before a big session: budgets, expired dates, eviction, instruction load.
- **Project skills and rules:** `.claude/skills/<name>/` and `.claude/rules/*.md` carry `paths:` and load only when a matching file is touched. A skill outside `.claude/skills/` does not exist for the model.
- **Auto memory:** preferences and feedback only. Project state lives in the repo (`NOW.md`, `Genesis.md`), never in memory.
- **Scripts:** `.claude/skills/kb-frame/scripts/` (`build_map.py`, `kb_audit.py`, `context_report.py`). Run them from the repo root.
- **Measurement:** the `InstructionsLoaded` hook (`.claude/settings.json`) logs every instruction file that enters the context to `{{SYSTEM}}/context_log.jsonl`. Read it with `context_report.py`.
- **Guard:** the `PreToolUse` hook (`.claude/hooks/guard_writes.sh`) enforces `AGENTS.md §7`.
- **Machine-specific notes** (shells, interpreters, local tools) live in `CLAUDE.local.md`, outside git.
