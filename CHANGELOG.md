# Changelog

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
