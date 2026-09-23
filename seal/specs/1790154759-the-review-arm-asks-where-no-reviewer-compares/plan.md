# Implementation Plan: the review arm asks where no reviewer compares

<!-- seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/plan.md
— HOW, in phases. Frames MichaelYcJo/SpecSeal#518. -->

Approved 2026-09-23 by the orchestrating session, under the owner's `automation` preset, when `smith` was spawned.

<!-- Filled by the session that spawns `smith`: reading this plan and
spawning the builder is the approval. -->

## Summary

The commit gate's review arm keeps asking on a change confined to `docs/` and
`seal/`. The gate's behaviour does not change. The work writes the reason
where a reader meets the question — the review arm's decision table, the
wake/quiet table, the hook beside `DOC_ROOTS` — and plants a test that fails
if the parity arm's path line is ever added to the review arm.

The reason is the measurement in `spec.md`. The only docs/seal-only changes
that reached a reviewer produced seven fixed findings in `docs/`, one of them
🔴, and the docs-only commits that never reached one were planning bookkeeping
in a file that has since been retired.

## Technical context

- `hooks/commit-review-gate.py#judge` — the review arm is the first `if`:
  `optin.opted_in(cwd) and not has_marker(command, "[no-review]") and not routed`.
  It reads no paths. The parity arm is the second `if`, and it adds
  `touches_code(cwd, invocations)`.
- `hooks/commit-review-gate.py#touches_code` and the `DOC_ROOTS` constant above
  it. Its docstring gives the parity arm's reason and does not say the line is
  the parity arm's alone.
- `hooks/optin.py`, the comment above `WORK_ITEMS`, lists `DOC_ROOTS` among the
  readers that spell `seal/` as a string. Nothing changes there.
- `tests/test_chain_hooks_hardening.py#test_parity_gate_ignores_document_only_commits`
  — the parity half, with the `parity_repo`, `stage`, `payload`, `run_hook` and
  `decision_of` helpers the new case needs.
- `tests/test_optin_home.py#test_the_home_directory_counts_as_documents_not_code`
  — `touches_code` on `seal/`, the unit-level half.
- `docs/review-chain-spec.md` §*commit-review-gate* › *Review arm* holds a
  three-row decision table. §*Parity arm* holds the `docs/`, `seal/` row this
  work contrasts with.
- `skills/implement/orchestration.md` §*Orchestrator: how the work is routed*,
  the table with rows *Wakes when* and *Quiets when*.
- `seal/ledger.md` row `S11` already claims the parity arm's half.

**What breaks in six months.** The design adds prose and a case, so its
failure is a reader who does not open either. Someone proposes the path tier
again, or a refactor shares `touches_code` between the arms "for consistency".
The case is what stops the second one: it fails the suite before the change
ships. The first one meets the `docs/` row and its measurement, which is the
most a document can do.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Share the parity arm's line: the review arm skips a change confined to `docs/` and `seal/` | #514's fold commits with no work item and no reader. Its 🔴 — a folded policy sentence giving three release acts to the tag push — ships in `docs/branch-and-release.md`, and `seal/ledger.md` edits land unread (26 fixed ledger-only findings in the measurement) | rejected by the measurement |
| A tier by an explicit, named list of planning paths, read by the gate and CI from one place | The list has no member today: `docs/flow.md`, where 13 of the 17 unreviewed commits landed, was retired on 2026-09-11. It becomes a hand-kept enumeration (#506's standing complaint), and every entry is a silent bypass that a later edit can widen to a policy document | rejected: it buys nothing measured and costs a list |
| Exempt by branch name (`docs/…`, `chore/…`) | A `docs/` branch edits a hook and nothing asks. The issue calls this the cheapest bypass the gate would ever have had | rejected by the issue |
| Close the issue with a comment and change nothing in the tree | The asymmetry stays implicit. The next reader finds `touches_code` beside the review arm, reads the missing call as an oversight, and raises #518 again; the measurement lives only in a tracker comment | rejected |
| **Keep the review arm's question, and write down why where the question is met, with a case that pins it** | A reader who never opens the row. The case covers the code half; the prose half is a document's ordinary limit | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The pin. A case beside `test_parity_gate_ignores_document_only_commits`: an opted-in repository, no declaration, no mark, no waiver, a commit carrying only `docs/policies/note.md` → the review arm asks (A1). With `seal/parity.md` present the ask names `[no-review]` and not `[no-parity]` (A2). The `touches_code` docstring and the comment above `DOC_ROOTS` say the line is the parity arm's alone and name the `docs/` section phase 2 writes | the case seen red with `and touches_code(cwd, invocations)` added to the review arm's `if`, then green without it; `tests/test_chain_hooks_hardening.py` and `tests/test_gate_judges_the_repo_it_commits_to.py` pass unchanged (A6) | |
| 2 | The policy. `docs/review-chain-spec.md` §*Review arm*: a row for a change confined to `docs/` and `seal/`, contrasted with the parity arm's row, and a short paragraph carrying the measurement's result as grounds. The wake/quiet table's review-arm *Wakes when* cell says it wakes whatever the change touches (A5). A case pinning the row's sentence (A4) | the pinning case seen red with the row deleted; the repository's prose-hygiene cases that cover the two edited files (line width, one word one meaning) pass | |
| 3 | The records. `changelog.md` fragment; `seal/ledger/1790154759-the-review-arm-asks-where-no-reviewer-compares.md` with the claim that the review arm reads no paths, anchored on `hooks/commit-review-gate.py#judge`; `overview.md` | `evidence-check` on the fragment reports the new row `ok`; `unverified-check` reads the memo | |

Status stays empty until a phase closes, and then holds the commit that
closed it.

## Operational impact

None. No migration, environment variable, dependency or compatibility change.
The gate decides exactly what it decided before. `plugin.json` moves only at
the release, because `hooks/` ships.
