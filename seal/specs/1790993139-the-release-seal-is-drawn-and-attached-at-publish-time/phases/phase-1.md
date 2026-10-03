# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 016177e9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#721 and #722. `admitted`'s docstring becomes round 3's paste-ready
paragraph. `NAME_CAP = 40` and one UTF-16 cutter shared by `first_line` and
the name. `record` caps at write, and `describe` caps `error` and `message`
at read. The `MESSAGE_RESERVE` comment is re-measured over `describe` with a
name and a message at their caps, for one, two and three gates. Ledger:
`0.17.0.md` B1 corrected, B2 re-stamped, `0.16.0.md` G1–G3 re-read. Cases
S13, S14 and S15, each seen red first. The spawn added: the plugin's longest
exception class name is `NoMutationDefined`, 17 characters, and "28" is not
to be copied.

## What this phase found

**The frame holds for this phase, with two corrections.**

- **No case pinned 533 and 909.** `spec.md` S14 says the re-measured
  figures "are pinned by the case that already pins 533 and 909". `git grep`
  over `tests/` at `6ee8d2b7` finds neither number and no reference to
  `MESSAGE_RESERVE` beyond one comment. The figures lived only in the
  comment above the constant and in `seal/releases/0.17.0.md` B1. This phase
  added the pin: `test_two_failed_gates_fit_the_reserve_with_every_field_at_its_cap`
  measures the longest report through `longest_report` and requires the
  comment to state each figure.
- **533 and 909 were already stale at the base.** Measured 2026-10-03 with
  `hooks/dispatch.py` as it stands at `6ee8d2b7` and a 19-character name
  (`ModuleNotFoundError`): 538, 915 and 1,289 for one, two and three gates.
  The `GROUPS` table changed after #717's round 3 measured, and nothing re-ran
  the measurement. `spec.md`'s arithmetic, `909 + 2 × (40 − 19) = 951`,
  started from the stale figure; from 915 it is 957, which is what the
  measurement gives.

**Measured, `describe` over every gate in every group it is in, both phases,
separator included:**

| Name | Units | Message | One gate | Two | Three |
|---|---|---|---|---|---|
| `ModuleNotFoundError` | 19 | 200 ASCII or 100 U+1D54F | 538 | 915 | 1,289 |
| `PendingDeprecationWarning` | 25 | the same | 544 | 927 | 1,307 |
| `E` × 40 | 40 | the same | 559 | 957 | 1,352 |
| U+1D54F × 20 | 40 | the same | 559 | 957 | 1,352 |

Before the cap, a 120-character name gave two gates `915 + 2 × 101 = 1,117`,
past the reserve.

**`group` is capped at read too.** Contract §12 asks for every field the
report takes from a record without a fixed vocabulary. Of the four fields
`describe` reads, `phase` goes through a fixed table, and `error` and
`message` are what #722 named. `group` has a fixed vocabulary only at the
writer, which is this plugin. A record from another plugin version can carry
anything there, so `describe` cuts it at `NAME_CAP`. Every group this plugin
writes is shorter than that, so nothing it writes changes. The gate's own
name is the record's file name, which `record` writes from `GROUPS`; that is
the set the figures measure over, and it is not cut.

**`__doc__` is not the source on Python 3.13.** The local `.venv` runs 3.13,
which strips a docstring's common indent from `__doc__`, and CI runs 3.12,
which keeps it. S13 therefore reads the docstring from
`inspect.getsource`, so it checks the columns the file holds on both.

**Verified.**

- Red first (executed): S13 named the 113-column line; S14's two cases and
  the reserve case failed on `NAME_CAP` missing; S15 failed on the uncut
  fields.
- Mutations through `bin/mutation-check hooks/dispatch.py`, against the four
  cases of `tests/test_a_gate_that_fails_says_so.py` that cover the caps
  (executed). Each of these went red: the write-side cap removed; each of the
  three read-side caps removed; every character one unit; `>` made `>=`;
  `NAME_CAP` 41. One survived: `break` made `continue`, which is equivalent,
  because the count only grows once past the cap.
- The 26 modules that read `hooks/dispatch.py` or `seal_stamp.py` (executed):
  `bin/test <26 modules> -q` gave 1507 passed and 69 skipped, exit 0.
- `uvx ruff check` and `uvx ruff format --check` on the four touched files
  (executed): clean.

**Ledger.** `seal/releases/0.17.0.md` B1 is corrected in place: 909 becomes
957, and the stale base figures are named. B2 and `seal/releases/0.16.0.md`
G1 and G2 are re-read, noted and re-stamped with
`evidence-check --reverify --checked 2026-10-03 --ledger <file>`. G3 cites
`report`, which did not change, so its hash did not move and it takes no
note. The new claims are D1 and D2 in this work item's fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The 533, 909 and 1,274 figures in `MESSAGE_RESERVE`'s comment | the same comment, re-measured, and `seal/ledger/1790993139-…md` D1 |
| `first_line`'s inline cutting loop | `hooks/dispatch.py#capped`, which `first_line` now calls |
