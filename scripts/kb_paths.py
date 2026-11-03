"""kb_paths.py - root detection and folder layout shared by the kb-frame scripts.

The root is the git toplevel of the current working directory. Run every
script from inside the target repo, not from inside this skill's own clone.
Fallback without git: walk up until a `.git` folder or a `.kb-frame.json`.

Layout defaults can be overridden with a `.kb-frame.json` at the root:

    {"system": "00_System_Ops", "projects": "10_Projects", "areas": "20_Areas"}
"""
import json
import subprocess
from pathlib import Path

CONFIG = ".kb-frame.json"
DEFAULTS = {
    "system": "00_System_Ops",
    "projects": "10_Projects",
    "areas": "20_Areas",
    "knowledge": "20_Areas/Knowledge",
}


def find_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return Path(out).resolve()
    except (OSError, subprocess.CalledProcessError):
        pass
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists() or (candidate / CONFIG).exists():
            return candidate
    return start


ROOT = find_root()


def layout() -> dict:
    cfg = dict(DEFAULTS)
    f = ROOT / CONFIG
    if f.exists():
        try:
            cfg.update(json.loads(f.read_text(encoding="utf-8")))
        except ValueError:
            print(f"WARN  {CONFIG} is not valid JSON; using defaults")
    return cfg


L = layout()
SYSTEM = ROOT / L["system"]
PROJECTS = ROOT / L["projects"]
AREAS = ROOT / L["areas"]
KNOWLEDGE = ROOT / L["knowledge"]
NOW = SYSTEM / "NOW.md"
MAP = SYSTEM / "MAP.md"
CONTEXT_LOG = SYSTEM / "context_log.jsonl"
