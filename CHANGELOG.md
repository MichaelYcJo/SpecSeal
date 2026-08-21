# Changelog

## 0.5.1 — 2026-08-21

- `evidence-check` runs as a command: the plugin puts a `bin/` wrapper on the
  Bash tool's PATH, so the drift check no longer needs a path into the plugin
  directory that the README never gave.
- Session detection reads `/proc/<pid>/cwd` before falling back to `lsof`.
  Without it, Linux hosts that ship no lsof saw no other sessions at all and
  the guard called a shared tree single-stream.
- `commands/` moved to the documented `skills/` layout. Invocation names are
  unchanged, and the three that moved stay user-invoked.
- A typo in `WORKTREE_GUARD_IDLE_MIN` falls back to the default instead of
  raising at import, where the crash read as "no verdict".
- READMEs gained a Limits section, a language switcher, and a link to
  CONTRIBUTING; both now describe what the hooks actually do rather than
  overstating the gates.

## 0.5.0 — 2026-08-21

First public release.

- Implement / review agent chain — **smith** (forges), **warden** (keeper of
  the seal), **scribe** (records) — with preloaded methodology skills
  (`implement`, `code-review`, `legacy-parity`, `writing-style`).
- Evidence ledger with spec-to-code drift detection (`evidence-check`:
  BROKEN / DRIFTED / EXTERNAL / OK, CI workflow template included).
- Worktree guard: session leases, idle-session classification, bilingual
  prompts (English default, `SPECSEAL_LANG=ko`).
- SDD file set (`spec.md` / `plan.md` / `questions.md` templates) and the
  three-axis document layout (`docs/` · `specs/` · `_ai/`).
- Conformance eval suite and the Review Handoff Protocol spec.
- The Seal Test: verification protocol for completion claims — proving
  command named before it runs, checks must have been seen red, evidence
  bound to a tree state, every claim labeled executed / read / unverified.
- Distributed as a Claude Code plugin: `/plugin marketplace add` ready.
