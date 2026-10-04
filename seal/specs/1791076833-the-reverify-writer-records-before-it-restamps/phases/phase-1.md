# 1791076833-the-reverify-writer-records-before-it-restamps — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e249d57d |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The carry. Every carry-set path at its `b4c9deb2` content, read from the old
worktree with `git checkout b4c9deb2 -- <paths>` and nothing committed, reset
or switched there. The nine `docs/the-pact.md` markers name this item; the
comments citing `round N of #647 C and D` name PR #749's round; the old work
item's `changelog.md` becomes this item's. This item's fragment holds the
claim rows W1, W2, G1, G2, C1, D1, D2 and F1–F3, re-read and dated, with
hashes from this tree and no `Re-read ·` rows. Excluded: `plugin.json`,
`CHANGELOG.md`, `tests/test_a_record_precedes_the_fixes_it_commissions.py`,
the old fragment and the five folded fragments. K1's and K2's commands and
their output go in this record.

## What this phase found

**The carry set is the frame's.** Recomputed with
`git log --first-parent --no-merges --format= --name-only b9824454^..b4c9deb2 | sort -u`
in the old worktree: 56 paths, of which 30 lie outside `seal/`, plus
`seal/README.md` — 31, the count `plan.md` states. `b9824454^` is `aa7fb285`,
the old branch's merge base with `e141980a`, and
`git diff --name-only aa7fb285 e141980a` names none of the 31, so each took
its `b4c9deb2` content whole. None of the phase's exclusions is in the set.

**The frame counted 17 round citations, and there are 19.** `spec.md`'s table
says `hooks/config.py` 4, `evidence_check.py` 9, `pact_check.py` 3,
`tests/gfm_table_oracle.py` 1. A pattern that lets whitespace and a comment's
`#` fall between any two words finds 5, 10, 3 and 1. Four of them wrap across
a line: one in `config.py` ("round 1 of #647 C" / "and D") and three in
`evidence_check.py`, broken after "round 2", after "of" and after "round". A
one-line `git grep -E 'round [0-9]+ of #647 C and D'` finds the other 15, so
neither count reaches the frame's 17 by the same reading. All 19 now read
`round N of PR #749`, keeping each line break where it stood. The citations
reading `round N of #647` without "C and D" were at `aa7fb285` already: they
are #735's rounds, the item that shipped in 0.18.0, and stay.

**Two more comments cited the old item's records by a name this item reuses.**
`tests/test_one_word_one_meaning.py` cited "`questions.md` Q2" and
`tests/test_pact_check.py` headed a section "phase 2". In this tree both
resolve to this item's files, whose Q2 and phase 2 are something else, so both
now say PR #749's. Same class as the round citations (§12). Left as they are:
`S1`–`S18` and "`spec.md` item 5", which `spec.md` carries under the same
numbers, and "Q15" in `test_a_vendored_copy_says_it_recorded_nothing`, which
`questions.md` names as inherited from PR #749's.

**A carried docstring is false against the carried code.**
`evidence_check.py#record_pact_changes` still says "`main` puts the ledger
back on it (`restore`)" and "the ledger is written exactly as it would be
without it". The put-back was replaced by plan, record, apply in
`f9469ad8..b4c9deb2`, and no `restore` exists. Phase 2 changes this unit's
neighbours and rewrites the paragraph. Recorded here because the frame's
"carried unchanged in intent" does not cover a sentence the code contradicts.

**The fragment's nine drifted coordinates moved under comments alone.**
`bin/evidence-check --ledger <fragment>` read 57 OK and 9 DRIFTED: `gfm_table`,
`a_list_above`, `raw_html_open`, `record_pact_changes`, `reverify`,
`reverify_into`, `main`, `pact_check.py#pact_changes` and
`docs/the-pact.md#"## The pact anchor"` (its marker). Re-stamped with
`--reverify --checked 2026-10-04 --ledger <fragment>`; the strict re-run reads
66 OK, 0 drifted.

**Verified, executed:** the thirteen modules of `plan.md`'s Verified-by cell,
`bin/test … -q`, 1262 passed; D2's
`tests/test_every_orchestrator_act_names_its_delivery.py`, 14 passed;
`uvx ruff check` and `uvx ruff format --check` on the seven Python files
changed on the way in, clean.

### K1 — the carry is the carry set and the changes on the way in

`git diff --stat b4c9deb2 HEAD -- <the 31 carry-set paths>` at `e249d57d`:

```
 docs/the-pact.md                                | 18 +++++++++---------
 hooks/config.py                                 | 12 ++++++------
 skills/evidence-check/scripts/evidence_check.py | 20 ++++++++++----------
 skills/evidence-check/scripts/pact_check.py     |  6 +++---
 tests/gfm_table_oracle.py                       |  2 +-
 tests/test_one_word_one_meaning.py              |  2 +-
 tests/test_pact_check.py                        |  2 +-
 7 files changed, 31 insertions(+), 31 deletions(-)
```

`git diff -U0 b4c9deb2 HEAD -- <the 31> | grep '^[-+][^-+]'`, counted: nine
`-`/`+` pairs of the `<!-- specs/… -->` marker, nineteen pairs that change
`of #647 C and D` to `of PR #749`, and the two pairs above that add
`PR #749's`. No other line differs.

### K2 — the tree names no work item it does not hold

`git grep -n 1791019474 -- . ':!seal/specs/1791076833-…' ':!seal/ledger/1791076833-….md'`
at `e249d57d`: no match, exit 1. Inside this item's own records it is named
by `spec.md`, `plan.md`, `questions.md`, `routing.md` and the fragment's
Notes cells, each as PR #749's history.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the carry adds; the old item's records and `Re-read ·` rows were never on this tree | none |
