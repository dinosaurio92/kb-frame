#!/usr/bin/env python3
"""context_report.py - summarizes <system>/context_log.jsonl, the log written
by the InstructionsLoaded hook (.claude/settings.json).

    python3 .claude/skills/kb-frame/scripts/context_report.py          # Linux / macOS / web
    python  .claude/skills/kb-frame/scripts/context_report.py          # Windows, PowerShell
    ... --sessions 5                                                    # last N sessions

Per session: every instruction file that entered the context, why
(session_start, nested_traversal, path_glob_match, include, compact), the
file that triggered a lazy load, and the bytes it cost. Use it to check that
project files load only when their project is touched.
"""
import argparse
import json
import os
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_paths import CONTEXT_LOG, ROOT  # noqa: E402


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT) if path.startswith(str(ROOT)) else path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", type=int, default=3, help="last N sessions (default 3)")
    args = ap.parse_args()
    if not CONTEXT_LOG.exists():
        print(f"no log at {CONTEXT_LOG}; start a session in this repo first")
        return 1

    sessions: "OrderedDict[str, list]" = OrderedDict()
    for line in CONTEXT_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = rec.get("event", {})
        sessions.setdefault(ev.get("session_id", "?"), []).append((rec.get("ts", ""), ev))

    for sid, events in list(sessions.items())[-args.sessions:]:
        total = 0
        print(f"\nsession {sid[:8]}  first load {events[0][0]}  ({len(events)} loads)")
        for ts, ev in events:
            path = ev.get("file_path", "?")
            try:
                size = os.path.getsize(path)
            except OSError:
                size = 0
            total += size
            reason = ev.get("load_reason", "?")
            trig = ev.get("trigger_file_path") or ev.get("parent_file_path") or ""
            if trig:
                trig = "  <- " + rel(trig)
            print(f"  {ts[11:19]}  {size:>6} B  {reason:<16} {rel(path)}{trig}")
        print(f"  total {total} B  (~{total // 4} tokens)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
