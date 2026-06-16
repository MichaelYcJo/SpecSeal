# worktree-guard hardening — overview

📋 implement applied
· spec:     docs/worktree-guard-spec.md (updated in step with each change —
            it is this work's authority)
· evidence: every judgment below is backed by a live measurement on the
            machine's real sessions, cited inline
· verified: regression scenarios re-run after each change; live
            discrimination tests listed below

## What was done

Four rounds of hardening, each triggered by a measured failure:

1. **False blocks and bypasses** — forgotten tabs counted as concurrent work
   (three sessions idle 27h+ observed); `git switch -`, remote-only-branch
   checkout, and prose mentions of git commands mis-handled.
2. **Idle threshold 60m → 5m** — keyboard input alone cannot go below ~an
   hour (a session 52 min past its last keystroke was writing its transcript
   that second); adding the transcript active-event signal made 5 minutes
   safe. Passive `attachment` appends were then found faking activity on
   idle sessions and are filtered by tail event-type parsing.
3. **Prompt forensics** — a blocked user could not identify the blocking
   session ("last activity 1 min ago" on a day-old session; a VS Code tab
   misattributed to Cursor from a sibling MCP process's flags). Prompts now
   show host app from the ANCESTOR chain, disaggregated signals, and the
   newest other transcript's last user message.
4. **Session leases** — the heuristics' measured ceiling: a background agent
   edited a tree while no `claude`-named process had its cwd there and the
   tree's project transcripts stayed quiet (driving session lived under
   another cwd's slug). A PostToolUse hook now DECLARES work per tool call
   into `<git-dir>/claude-preset-leases/<session-id>`; fresh foreign leases
   are active work streams, no inference involved.

## What changed

```
hooks/worktree-guard.py       all four rounds
hooks/session-lease.py        (new) lease stamper
hooks/hooks.json              lease hook wired (PostToolUse Bash + Write|Edit|NotebookEdit)
docs/worktree-guard-spec.md   decision matrices, signals, forensics, lease norm
```

## Key judgments

| Judgment | Chosen | Grounds |
|---|---|---|
| Idle sessions | ask, not deny | detection cannot tell an abandoned tab from a paused human; the human can |
| Unknown signals | conservative (active) | wrong deny costs a prompt; wrong allow breaks another session's tree |
| Transcript freshness | tail's last ACTIVE event, not mtime | idle sessions receive passive appends triggered by other sessions' edits (observed) |
| App attribution | ancestor chain only | sibling-process guessing produced a live misattribution (Cursor vs VS Code) |
| Declaration vs inference | leases win; heuristics remain as fallback | the blind spot is structural — sessions invisible to process/transcript scans exist (observed) |

## What was verified (executed)

- 10-scenario stdin regression after each round.
- Live: 3 forgotten sessions → ask with per-signal ages; autonomously
  working session → deny; threshold extremes flip ask/deny as designed.
- Lease end-to-end: a Write from another cwd leased the repo; the next
  branch switch was denied listing the lease; lease removal restored the
  single-stream path.

## Not verified (who must answer)

| Item | Who |
|---|---|
| Lease coverage of currently-running sessions (they stamp only after restarting with plugin ≥0.3.1) | resolves as sessions naturally cycle; until then, avoid switching under a known live background session |
| tty atime semantics on non-macOS hosts | first Linux adopter |
