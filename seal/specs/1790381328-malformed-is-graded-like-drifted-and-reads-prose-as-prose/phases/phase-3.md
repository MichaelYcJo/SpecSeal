# 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 353224c2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records. The four ledger rows of `spec.md` §*Data & interfaces*, plus
any other row `evidence-check .` names: false claims corrected in place with a
`Corrected 2026-09-26` note, then re-read, `evidence-check --reverify`
narrowed to the files holding them, and a dated `Re-read` note. New rows in
`seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`.
`changelog.md` in this directory. `survivor-check --range
origin/release/v0.15.5...HEAD`, with any exemption in `survivors.md`.
`overview.md`. The spawn prompt added: run `evidence-check --strict .` and the
sweep before the handoff and report both.

## What this phase found

- **Sixteen rows drifted, not the frame's six.** `evidence-check .` after
  phase 2 named the frame's rows and ten more: every anchor the 0.15.4
  `MALFORMED` row cites that this work edited (the claim was false, so it is
  corrected), and three rows citing `main` in `0.4.0.md`, `0.8.3.md` and
  `0.9.0.md`, which drifted on `--strict`'s help text alone. Re-reading the
  `0.4.0.md` row then drifted a seventeenth, `0.13.1.md`'s row that hashes
  the whole `### 1788331011` section of `0.4.0.md`; this is the two-pass shape
  that row's own notes describe, and it took one more `--reverify`.
- **The new rows anchor two YAML files.** `.github/workflows/test.yml#ledger`
  resolves to the job from `ledger:` to its last `fi` (lines 85–103 at
  `353224c2`), which holds the warning; `templates/evidence-check.yml`'s
  quoted `--strict` line resolves to its step, comment included. Both checked
  through `resolve` before the rows were written.
- **One survivor**, `test_an_old_format_row_is_silent`'s docstring, which
  shares four phrases with the renamed case's old docstring and states
  `OLD-FORMAT`'s unchanged grading. Exempted with its quote. The frame
  expected `SKILL.md`'s `OLD-FORMAT` row to be reported and it was not.
- **A pipe in a ledger claim splits the row.** The `evidence-ci` row quotes
  the recipe `|| [ $? -eq 1 ]`; it is written `\|\|` in the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
