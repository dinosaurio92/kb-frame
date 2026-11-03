#!/usr/bin/env python3
"""kb_init.py - installs the kb-frame skeleton into the current git repo.

    python3 .claude/skills/kb-frame/scripts/kb_init.py --owner "Ada"
    python  .claude/skills/kb-frame/scripts/kb_init.py --owner "Ada"   # Windows
    ... --dry-run        # list what would be written, write nothing

Run it from the target repo. It never overwrites an existing file: it prints
SKIP and moves on, so it is safe to rerun after a skill update.

What it writes (from ../templates):
  root/      -> <root>/            AGENTS.md, CLAUDE.md, CLAUDE.local.md
  system/    -> <system>/          NOW.md, IA_System_Log.md, templates/*
  projects/  -> <projects>/        Backburner.md
  areas/     -> <areas>/           Knowledge/Global_Learnings.md
  claude/    -> <root>/.claude/    settings.json, hooks/, skills/close, skills/kb-audit
Then it appends to .gitignore and .gitattributes, and prints the next steps.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_paths import L, ROOT  # noqa: E402

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
DEST = {
    "root": ".",
    "system": L["system"],
    "projects": L["projects"],
    "areas": L["areas"],
    "claude": ".claude",
}
GITIGNORE = ["CLAUDE.local.md", f"{L['system']}/context_log.jsonl"]
GITATTRIBUTES = ["*.sh text eol=lf"]


def render(text: str, owner: str) -> str:
    return (text.replace("{{OWNER}}", owner)
                .replace("{{TODAY}}", date.today().isoformat())
                .replace("{{SYSTEM}}", L["system"])
                .replace("{{PROJECTS}}", L["projects"])
                .replace("{{AREAS}}", L["areas"]))


def append_lines(path: Path, lines, dry: bool) -> None:
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    missing = [ln for ln in lines if ln not in existing]
    if not missing:
        return
    print(f"APPEND {path.relative_to(ROOT).as_posix()}: {', '.join(missing)}")
    if dry:
        return
    with path.open("a", encoding="utf-8", newline="\n") as f:
        if existing and existing[-1] != "":
            f.write("\n")
        f.write("\n".join(missing) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default="the owner", help="name used in AGENTS.md and skills")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not TEMPLATES.exists():
        print(f"templates folder not found: {TEMPLATES}")
        return 1
    print(f"root: {ROOT}")
    written = skipped = 0
    for group, dest in DEST.items():
        src_dir = TEMPLATES / group
        if not src_dir.exists():
            continue
        for src in sorted(p for p in src_dir.rglob("*") if p.is_file()):
            target = ROOT / dest / src.relative_to(src_dir)
            shown = target.relative_to(ROOT).as_posix()
            if target.exists():
                print(f"SKIP   {shown} (exists)")
                skipped += 1
                continue
            print(f"WRITE  {shown}")
            written += 1
            if args.dry_run:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.suffix in (".md", ".json", ".sh", ".txt", ".yml", ".yaml"):
                text = render(src.read_text(encoding="utf-8"), args.owner)
                target.write_text(text, encoding="utf-8", newline="\n")
            else:
                target.write_bytes(src.read_bytes())

    append_lines(ROOT / ".gitignore", GITIGNORE, args.dry_run)
    append_lines(ROOT / ".gitattributes", GITATTRIBUTES, args.dry_run)

    print(f"\n{written} written, {skipped} skipped{' (dry run)' if args.dry_run else ''}.")
    print("Next:")
    print("  1. Read AGENTS.md and edit sections 1, 7 and 8 for this repo.")
    print("  2. If .claude/settings.json already existed, merge the hooks from "
          "templates/claude/settings.json by hand.")
    print("  3. Edit the protected paths at the top of .claude/hooks/guard_writes.sh.")
    print(f"  4. Create the first project: {L['projects']}/<Name>/Genesis.md "
          f"from {L['system']}/templates/Genesis_Template.md.")
    print("  5. Run scripts/build_map.py, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
