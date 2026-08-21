# Changelog

## 0.6.1 — 2026-08-21

- **The SDD set now says when it applies.** Gated work — 6+ files, a new
  module, an architectural choice — writes `spec.md` and `plan.md` before
  implementing, and approving that plan is the Design Gate. 3–5 files get a
  closing `overview.md`; anything smaller gets neither. A methodology that
  never states its threshold is skipped by judgment call each time, which is
  what happened in this repo: two features shipped with no work item and
  nothing noticed.
- **Task lists have a home: `_ai/tasks/`, not `specs/`.** `specs/` holds what
  was agreed and stays true for the life of the work item; a task list is
  where the work has got to and changes every session. `plan.md`'s Phases
  table remains the stable layer, and each phase carries a *Verified by*
  column, so a phase cannot be ticked off the way a checkbox can.
- Spec directories are timestamped as the skill always specified
  (`<unix-epoch-seconds>-<slug>`), the four that predate the convention were
  backfilled from the commit that introduced each, and a test now fails the
  build on a directory without the prefix.

## 0.6.0 — 2026-08-21

- **Skills stop firing on keywords.** Nine model-invoked skills had triggers
  written before the agent chain existed — `confidence-check` fired on
  "implement/create/build", so one request could open three scope
  conversations while the smith's design gate was already deciding. Every
  auto-firing skill now states where it does *not* belong, the smith owns the
  design gate and calls `confidence-check` / `feature-planner` when it needs
  them, and a test fails the build if a model-invoked skill ships without
  that boundary. This is the plugin's own context-cost argument applied to
  itself.

- **Migration mode is reachable without reading the README.** The smith asks
  once, when it first bootstraps a repo's layout, whether the project ports
  behavior from an existing codebase — and derives what the machine can:
  it proposes candidates for the original (sibling checkouts, an upstream in
  `git remote -v`, overlapping paths), reads the baseline from the one you
  confirm, and writes `docs/parity.md` from a template. Answering no is final.
  `/specseal:parity-setup` covers deciding later.
- **The commit gate also asks whether the original was consulted.** In a repo
  declaring `docs/parity.md`, committing code with no `.git/specseal-parity`
  for this HEAD raises a prompt (`[no-parity]` skips it, visibly). Folded into
  the existing gate rather than added as a fifth hook; commits confined to
  `docs/`, `specs/` and `_ai/` stay silent.
- **`/specseal:evidence-ci` wires the drift check into CI.** It resolves the
  plugin's own location, vendors the checker to `tools/`, and writes the
  workflow — the setup instructions used to name a path no document gave.

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
