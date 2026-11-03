# The seven principles

Tool-agnostic. Each one names the mechanism that implements it in Claude Code today.

## 1. Constant kernel, ≤4 KB

Only rules that change a decision: persona, risk tiers, boot, budgets, guardrails. Nothing narrative, nothing "just in case".

**Mechanism:** `AGENTS.md` holds the kernel. `CLAUDE.md` imports it with one `@AGENTS.md` line and adds what is specific to Claude Code. Machine facts go to `CLAUDE.local.md` (gitignored). The same kernel serves Cline, Codex or Cursor.

## 2. Three state layers, nothing else in the load path

- **L0 critical facts** (~120 tokens): who, where, time zone, the hard rules.
- **L1 index**, generated, linear and small (~80 bytes per unit).
- **L2 unit of work**, bounded (≤6 KB).

Everything else is retrieval, not load.

**Mechanism:** L0 at the top of the kernel. L1 is `MAP.md`, generated from frontmatter. L2 is the project `Genesis.md`. History, decisions and logs are read with `grep` or `Read` when needed.

## 3. Budgets with a gate, not with intent

Every file in the load path has a byte limit. A script checks it and blocks the close when it fails.

**Mechanism:** `build_map.py` exits 1 on a broken budget. The `InstructionsLoaded` hook logs what loaded and why, so "I think it loads 18 KB" becomes a number per session. Hard prohibitions go to a `PreToolUse` hook, because a rule in text can be ignored.

## 4. Procedures as skills, scoped, one level deep

What is done at a given moment (close, audit, apply) is a skill. Short description with an explicit trigger, body ≤5,000 tokens, references one level deep.

**Mechanism:** `.claude/skills/<name>/SKILL.md`, with `paths:` for project-scoped ones. Open spec: Agent Skills (`scripts/`, `references/`, `assets/`). A skill in a non-standard folder costs the same as not existing.

## 5. Record the why and the dead ends

Agents remember what was decided, not why, nor what was discarded. Then they repeat the failed attempt.

**Mechanism:** fixed format in `Decisions.md`: date · decision · why · **rejected** · what would revert it. One *dead end* row after each hard failure. The T3 decision pass already asks for this; the format makes it stick.

## 6. Retrieve instead of load; delegate instead of read

History and big corpora are queried, not preloaded. Heavy research runs in a subagent that returns one or two thousand tokens.

**Mechanism:** derivable paths (`<projects>/<Name>/`), `grep` over `Log.md`, a skill with `context: fork` for long searches. Graph or vector indexes only when the corpus passes a few hundred files or a second permanent agent appears.

## 7. One owner per datum

Preferences → auto memory. State → repo. Machine → `CLAUDE.local.md` or `.claude/rules/`. Two owners of the same datum guarantee divergence.

**Mechanism:** the kernel says where each kind of datum lives. `/kb-audit` section 4 shows what loads from where.

## Numbers that fix the design

| Number | Meaning |
| :--- | :--- |
| 18 / 18 | frontier models lose precision as input grows; the drop has steps, not a slope (Chroma, "Context Rot") |
| ≤200 lines | official target for `CLAUDE.md`; imports save nothing |
| 1,536 chars | per skill description in the listing; the body enters on invoke |
| 5,000 tokens | per skill survive a compaction (25,000 in total) |
| 1–2 k tokens | what a subagent returns after spending tens of thousands |

Sources: Claude Code docs on memory and skills, Anthropic "Effective context engineering for AI agents", Agent Skills specification, Chroma "Context Rot".
