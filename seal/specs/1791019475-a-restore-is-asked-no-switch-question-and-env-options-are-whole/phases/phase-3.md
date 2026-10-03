# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 2ad5a046 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Write the records. New claims go in this item's fragment. E14, E16, I5 and
I6, and any other released row the change drifts, are re-read through
`bin/evidence-check --reverify --into <that fragment> --checked 2026-10-03`,
with a `Corrected ·` row where a claim became false. Write `changelog.md` and
`overview.md`. Close on S11: 0 drifted and 0 broken on every ledger file
touched, and `bin/survivor-check --range 2b1dcb1f...HEAD` passing, with a
`survivors.md` only for a quote that is defended.

## What this phase found

**`bin/evidence-check` found one released row the plan's list did not
name.** M2 in `seal/releases/0.16.0.md` cites `docs/worktree-guard-spec.md`
§*Which tree*, which phase 1 drifted. The `--into` run wrote five `Re-read ·`
rows, for E14, E16, I5, I6 and M2. Each was read against its cited claim,
and each claim holds. None needed a `Corrected ·` row: E14's round-2 note
says the table lacks two rows, and that note is dated. The re-read row says
the table now holds them.

**K7 drifted too**, in work item 1790993140's fragment, through the same
section. It was re-read and re-stamped in place with a note, as K3 and K5
were (`questions.md` D5).

**S11.** Each ledger file the branch touched reads 0 drifted and 0 broken:
this item's fragment, 1790993140's fragment and `seal/releases/0.16.0.md`.
`bin/evidence-check --strict .` over the whole tree does not pass. It reads
17 drifted rows before this phase's writes, and the 8 this branch drifted
are the ones above. The other 9 are drifted at `2b1dcb1f` too (executed:
`evidence_check.py --strict` over a `git archive` of `2b1dcb1f`). They sit in
files this branch does not touch: 7 in work item 1790993138's fragment, 1 in
1790993139's and 1 in `seal/releases/0.5.0.md`, against released files and
`templates/config.md`, `docs/branch-and-release.md` that moved under them.
This branch leaves them alone. The integration branch re-stamped the rows the
first four items drifted at `bb2f3400`, after this branch was cut.

**`bin/survivor-check`** reported three places still carrying K3's old
wording, that the table was built from the two synopses. The comment above
`ENV_SPELLINGS` was this branch's to fix, and it was reworded. E14's dated
note in a released file and 1790993140's closed `overview.md` are recorded in
`survivors.md`, each with its quote.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
