#!/bin/sh
# PreToolUse guard for AGENTS.md section 7 (data guardrails).
# Reads the tool call as JSON on stdin. Pure POSIX sh + grep/sed: no Python.
#
#   READONLY   (a folder)  -> deny every write tool; Bash that names it -> ask
#   RESTRICTED (a file)    -> ask before any write tool or Bash that names it
#
# Edit the two patterns below. They match as substrings of the path or command.
# Output: a PreToolUse permission decision, or nothing (= allow).

READONLY='Legal_Docs'
RESTRICTED='Sensitive_Identifiers'

input=$(cat)

tool=$(printf '%s' "$input" | sed -n 's/.*"tool_name": *"\([^"]*\)".*/\1/p')

case "$tool" in
  Bash)
    target=$(printf '%s' "$input" | sed -n 's/.*"command": *"\(.*\)".*/\1/p') ;;
  *)
    target=$(printf '%s' "$input" | sed -n 's/.*"file_path": *"\([^"]*\)".*/\1/p') ;;
esac

[ -z "$target" ] && exit 0

decide() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
  exit 0
}

if [ -n "$READONLY" ] && printf '%s' "$target" | grep -q "$READONLY"; then
  if [ "$tool" = "Bash" ]; then
    decide ask "AGENTS.md section 7: $READONLY is read-only. Confirm this command only reads."
  fi
  decide deny "AGENTS.md section 7: $READONLY is read-only. No tool writes there."
fi

if [ -n "$RESTRICTED" ] && printf '%s' "$target" | grep -q "$RESTRICTED"; then
  decide ask "AGENTS.md section 7: $RESTRICTED is RESTRICTED. Editing a personal-data line needs the owner's express consent."
fi

exit 0
