# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | cace4ac1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`MALFORMED` is graded like `DRIFTED`, the owner's answer (b) to #606's Q1 of
2026-09-26: exit 1 on a lenient run, exit 2 under `--strict`. `exit_code`'s
branch moves below `BROKEN`; `LENIENT_NOTICE` becomes the sentence in
`spec.md` §*Scope* item 2, verbatim; the module docstring's exit line,
`malformed_rows`' docstring and `--strict`'s help follow. The six test pins of
`spec.md` item 8 (one renamed), S3's `BROKEN`-beside-`MALFORMED` assertion and
two new pins (item 9). `skills/evidence-check/SKILL.md`,
`skills/evidence-ci/SKILL.md` step 4, `templates/evidence-check.yml`'s step
comment and `test.yml`'s `ledger` comment and warning. Q1 of work item
1790297087 ticked with the owner's answer. The spawn prompt added: grep every
sentence that states `MALFORMED`'s grading by meaning, in several phrasings,
English and Korean, and fix every twin.

## What this phase found

- **The drift branch took `MALFORMED` rather than a branch of its own.**
  `plan.md` left the choice open. One condition, `MALFORMED or DRIFTED or
  drifted`, below `BROKEN or refused`, reads as what the owner decided (the
  two are graded alike) and leaves nothing to reorder. The comment above it
  names the owner, the date, and the departure from `OLD-FORMAT` with its
  grounds.
- **Every red was seen before the change and under a mutant after it.**
  Before the checker edit, the moved pins failed 14 at once across the two
  modules. After it, one mutant at a time with each file restored from bytes
  kept before the loop: `MALFORMED` above `BROKEN` (1 red: the grading case's
  `BROKEN`-beside assertion); `MALFORMED` back at exit 2 (12 red across eight
  functions, both new pins among them); the old notice (5 red); `SKILL.md` as
  it stood at 47e32d57, its verdict row alone, and its `DRIFTED` row alone
  (1 red each, the skill pin); `test.yml` as it stood at 47e32d57 (1 red, the
  CI pin).
- **Twins the frame's list did not name**, found by grepping the claim by
  meaning (`malformed`, `does not parse`, `nothing can parse`, `strict or
  not`, `with or without --strict`, `under both readings`, `whatever this flag
  says`, `drift is exit 2`, `lenient`, `엄격`):
  - `SKILL.md` §*Which reader graded your tree*'s paragraph "All four are
    right … the disagreement is the design" explains drift's leniency by a
    branch mid-flight, which is not why `MALFORMED` is lenient. A paragraph
    after it says the owner's reason and that `OLD-FORMAT` stays exit 2.
  - `.github/workflows/test.yml`'s job comment "drift is reported and does
    not" gained the malformed half, beside the `broad-gate` sentence the
    frame named.
  - `tests/test_a_row_points_by_content.py#test_prose_marks_beside_a_good_anchor_are_not_refused`'s
    docstring said refusing prose "exits 2" and that a coordinate "holds both
    marks". Both were 0.15.4's rules.
  - `skills/evidence-ci/SKILL.md`'s new sentence ("the recipe above lets a
    malformed coordinate through") is text a reader acts on, so
    `tests/test_evidence_check.py#test_letting_drift_warn_takes_both_halves`
    runs the recipe over a malformed row: exit 0 without `--strict`, 1 with
    it. Red on the phase-1 checker (`assert 1 == 0`).
  - Not twins, read and left: `README.md`, `README.ko.md`, `CONTRIBUTING.md`
    and `docs/the-evidence-ledger.md` state drift's grading only and stay
    true (`spec.md` §*Out*); `old_format_rows`' "fails the run with or without
    `--strict`" is `OLD-FORMAT`'s and still true; `hooks/evidence-advisor.py`
    names verdicts and no exit code; `CHANGELOG.md`'s 0.15.4 entry is
    released history.
- **The enumeration re-run** (`spec.md` §*Data & interfaces*) over the edited
  tests lists no function asserting 2 for a lenient `MALFORMED`.
- **`tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`
  is red on this branch until phase 3 writes `overview.md`.** Seen while
  running the modules that read the edited documents; every other case in
  them passed (493).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_a_malformed_row_is_silent` (renamed) · NAME NOT IN TREE | `test_a_malformed_row_is_told_what_the_gate_would_say`, same module; no ledger row cited the old name |
| `exit_code`'s separate `MALFORMED` branch above `BROKEN` | the drift branch's condition, with its comment |
