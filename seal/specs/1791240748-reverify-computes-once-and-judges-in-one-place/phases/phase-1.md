# 1791240748-reverify-computes-once-and-judges-in-one-place — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4a7ff227 |
| Ran by | unknown — the spawn prompt named neither the agent nor the model, and this record does not source the value from the segment itself |

## What this phase was asked

The judge, read by the check (spec D2, D3). The judge function with the
full verdict; `classify` as its finding; `family_view.grade`, `check_text`
and `released_drift` reading it; `reverify_into` reading the judge's hash in
place of `current_hash`, which is removed. S3a's `--into` arm seen red, then
green. D6's probes 1 and 2 run for `--strict` alone, byte-identical.

## What this phase found

**The frame holds, with two corrections to its lists.**

- `tests/test_a_row_points_by_content.py::test_the_two_commands_that_must_know_ask_for_the_flag`
  is not in the spec's lists of tests whose assertion changes, and it has to
  change: it pins `classify` as one of the two consumers that call
  `resolve_unit`, and `classify` no longer calls anything but `judge`. Its
  consumer is now `judge`. Phase 2 changes it again, because `reverify`
  stops calling `resolve_unit` at all.
- S3b's check-side wording (`locator is ambiguous — 3 places: … (2 hold the
  recorded content, a tie it cannot break)`) is already what the base
  prints, so it cannot be seen red at the base. Only `--reverify`'s side of
  S3b is red there; it is planted in phase 2.

**The verdict's shape.** `Verdict(status, coord, detail, now, region,
dest)`, a namedtuple, so `classify` is `judge(...)[:3]` and two verdicts
compare by value. The spec's sketch also listed the places, which of them
hold, and whether they are unsure: no command reads those once the status,
the hash and the destination are on the verdict, so they are not carried.
`region` is carried instead: the `(start, end)` the hash was taken over, or
the unit a claim's statement is gone from. Phase 2 reads it to tell a
coordinate that cannot settle from one downstream of it.

**`dest` is carried only for a row with no claim.** A claim's recorded hash
is of a statement, which no unit reconstructs, and the base never re-pointed
a claim row. The destination's hash is read from the destination's own file.

**One `--into` cell moves beside C8.** `current_hash` answered None for any
place the declaration rule is unsure of; `judge` answers the hash wherever the
check grades the coordinate `OK` or `DRIFTED`. So a row with no claim whose
unsure place holds its hash, outranked by a newer reading holding other
content, is now re-read at that hash rather than named *no one place to
hash*. Same class as C8 (#809): the check said the place holds, and `--into`
said there was none.

**D6 probe 1, executed.** `--strict` over this repository's own ledger at the
base script (`e6d5a055`, from a `git archive` in the scratchpad) and at this
commit: stdout byte-identical, 212 lines, exit 2 at both. Exit 2 is this
branch's own drift: the rows citing the units this phase edited, and the
two citing `current_hash`, which is BROKEN until phase 4's `Corrected ·`
rows.

**D6 probe 2 for `--strict` and `--migrate`, executed.** A pytest plugin
(`test_tmp_differential.py`, in the scratchpad, never in the tree) wrapped
`subprocess.run` for the seventeen modules the spec names under *What must
survive*. Each call of the script ran first through the base script in the
same tree, the tree was put back byte for byte, then through this commit's.
674 calls (656 `--strict`, 18 `--migrate`), 1467 cases passing, **0
differences** in exit, stdout or written files. Questions Q2 is answered:
identical.

A first version of the probe copied each tree and ran the base script in the
copy. It reported 22 differences, all the copy's own: 20 in the order of
`corrected by 2 rows (…)`, which `family_view` sorts by `str(file_identity)`
and so by inode; two where the copy turned a hard link into two files; one
where the copy left the git repository above it behind. Running both scripts
in the one tree removed all 22.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `current_hash` | `judge(...).now`; the released rows citing it (`seal/releases/0.18.0.md`, `0.18.1.md`) take `Corrected ·` rows in phase 4 |
