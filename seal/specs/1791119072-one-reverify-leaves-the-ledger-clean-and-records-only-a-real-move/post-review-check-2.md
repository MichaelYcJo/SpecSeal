# Post-review check 2 — the second #791 fix on PR #786

Target SHA `e50ef3d6` on `fix/774-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move`,
base `release/v0.18.2` at `94d7b2e0`. Range read: `c53219ee..e50ef3d6`
(`a394d118` the fold, `walked_move` and `owed_moves`, the three `still` call
sites, two cases, the pact sentence and its pin; `01e3ad6b` E4 and the
fragment re-stamped with `--checked 2026-10-05`; `e50ef3d6` two survivors
rows). This is not a numbered round: the chain ended capped at round 3, and
the first post-review fix was read by `post-review-check.md`. This pass reads
the second post-review fix once. Ran by: specseal:warden on claude-opus-5-5.
Worked in a `git clone --no-local` at the target under
`<scratchpad>/<work-item-id>/post-review-2/clone`. Nothing was written in the
checkout but this file. The clone, the probe file, its mutated module copy
and its outputs are deleted.

## Summary

The fold closes the first pass's finding and keeps round 3's closure. Driven
through `main` with `Pact notify | always`, each shape records what the file
holds and a second run appends nothing:

| Shape | X1's record after run 1 | Run 2 | `--strict` after |
|---|---|---|---|
| Round 3's (two moves) | `@5127adb5 → @46e82957` | nothing | 0 |
| The first pass's (a move, then left) | `@5127adb5 → @07b2ad6b`, `@07b2ad6b` BROKEN | nothing | 2 (X1 DRIFTED, as the file says) |
| A revert (left, left, unchanged) | no row | nothing | 0 |

The smith's claim that *left then unchanged* cannot happen inside one run is
false. The third shape does it. X1 was stamped when `handler` was at v1. The
code moved to v2 and back, so the run re-stamps the line X1 names back to the
bytes X1 recorded. The line never returns to an earlier state of the run, but
it does return to a state from before the run, which is what X1's hash
describes. The code gets this shape right, and the `still` calls are what get
it right: with `still` a no-op, X1 is recorded BROKEN at `0166b3c4` while
`--strict` reads it clean. No case pins this. With `still` a no-op, all 515
cases of the two touched modules pass (⬜ 1). A case that is red under that
mutation is under *Paste-ready fixes*.

The 36-sequence case calls the code's own fold, and its expected parts come
from the rule rather than from the code. Its walk-to-call mapping matches
what `reverify` passes, which I logged in all three shapes. Its second-run
assertion follows from its first and checks nothing on its own (⬜ 3). The
five mutations I made to the fold's rules were each red. The docstrings, E4,
the pact sentence and its pin say what the code does. The 2026-10-05 re-stamp
touched exactly the eighteen rows that `01e3ad6b`'s message says were
re-opened, and the fold contradicts none of their claims.

## What the account claimed, and what the code does

**Claimed** (`a394d118`'s message and the spawn prompt): each walk's outcome
for a coordinate is folded. The move that landed runs from the pre-run hash to
the last hash a walk wrote, BROKEN follows at the hash the file holds where
the last walk left it, and a walk reading it unchanged clears an earlier
BROKEN. Every two- and three-walk sequence is enumerated.

**The code** at `skills/evidence-check/scripts/evidence_check.py:3002-3030`
does that. `walked_move` keeps the first old hash and, unless the walk left
the coordinate, the walk's new hash; it marks BROKEN when the walk left it
and clears the mark when the walk read it unchanged. `owed_moves` hands over
the move, and then BROKEN at the landed hash, or at the first hash when no
walk wrote one. `reverify` folds each pending move or leaving at `:3441`, and
calls `still` at `:3258`, `:3312` and `:3369` where a walk reads the
coordinate unchanged. `still` folds only where an earlier walk gave the
coordinate a part (`:3159`). The hand-over is at `:3458`.

**Claimed** (the spawn prompt, for the smith): *left then unchanged* cannot
happen within one run, because a re-stamped ledger line never returns to
earlier bytes, so the three `still` call sites survive mutation.

**Executed:** the mutation half is true and the reachability half is false.
The probe below gives the sequence left, left, unchanged in one run of an
ordinary `--reverify --checked`. The premise is true of states inside the run
and does not cover a coordinate whose recorded hash describes a state from
before the run. That is the state a reverted code change brings back, and
`docs/the-pact.md` §*A signatory records a pact change* already names code
that went back to an earlier hash.

## Finding 1 — the `still` calls carry a shape the suite does not run

**Executed.** In the clone, `seal/releases/0.1.0.md` held R1, a `Re-read ·`
row citing R1, and X1 under a second heading. X1's ledger coordinate names
the `Re-read ·` line by the claim `"@<the citation hash it held at v1>"`.
Every date cell held `2026-03-01`, the run's `--checked`. With `handler` at
v1 this file read `--strict` 0. The file was then written as a re-stamp at v2
leaves it: R1 and the `Re-read ·` row at v2, and X1 unchanged, because its
quoted hash was gone. `handler` was then restored to v1. The logged calls to
`walked_move` for X1 were:

- walk 0: left, because the line holds the v2 citation;
- walk 1: left, because the line holds the v1 code hash and still the v2 citation;
- walk 2: unchanged, because the citation is re-stamped back to v1 and the line is byte for byte what X1 recorded.

| | the code at `e50ef3d6` | `still` a no-op |
|---|---|---|
| X1 in MOVES | nothing | `(0166b3c4, None)` |
| The file after the run | the v1 file, byte for byte | the v1 file, byte for byte |
| `--strict` after | 0 | 0 |

Through `main` with `Pact notify | always`, the record held R1's and the
`Re-read ·` row's moves (`@96c68feb → @d06d1b56`) and nothing for X1. A
second run appended nothing and `--strict` read 0 after both.

`bin/mutation-check` with `still`'s `if key in parts:` turned into `if
False:`, over `tests/test_a_released_row_is_read_again_in_a_fragment.py` and
`tests/test_a_signatory_records_a_pact_change.py`, printed `SURVIVED` (515
passed).
The case below, `test_a_coordinate_left_and_then_read_unchanged_records_nothing` (NAME NOT IN TREE),
was green at `e50ef3d6` and red under that mutation (`[(…, 10, …"@74e4d92d"', '0166b3c4', None)] == []`). `ruff check`
and `ruff format --check` were clean on the module with it inserted. The
insertion was then reverted.

- **Why it matters.** The behaviour is right today, so nothing ships wrong.
  The unit that keeps it right is one the smith left unpinned on grounds that
  do not hold. A later edit that drops a `still` call would write a permanent
  BROKEN row for a coordinate `--strict` reads clean, and every case would
  stay green.
- **Which `still` site this reaches.** Only the single-place site at `:3369`
  was constructed. The ambiguous-place site at `:3258` and the re-anchor site
  at `:3312` were read, not constructed. Both are the same fold call, under
  the same key.
- **Severity.** ⬜, because no defect ships if it stands. Round 2's white 2,
  a skip called equivalent that was in fact load-bearing, is the precedent.
  Whether to plant the case in a capped run is the orchestrator's call.

## Finding 2 — walk 0 says a coordinate is left that a later walk clears

**Executed, in the same probe.** The run printed `seal/releases/0.1.0.md#"###
1000000001-the-first-item">"@74e4d92d"  the anchored statement is gone from
"### 1000000001-the-first-item" — the check calls this DRIFTED; left`. After
the run, the check calls X1 OK. The line comes from walk 0. Walks after the
first are quiet (`say = quiet if repeat else print`, `:3183`), so no later
line takes it back. This is the same family as the first pass's ⬜ 2: what
the run prints about a coordinate that a later walk changes. The unit is this
branch's, from #772's repeated walk at round 1, and outside the post-review
range. It is reported for the orchestrator to file with that ⬜ 2, not for
this range's fix list. The first pass's ⬜ 2 was seen again too: the first
pass's shape through `main` exits 1 on the `run it without --ledger` LEFT
line.

## Finding 3 — the enumeration's second-run assertion restates its first

**Read**, at `tests/test_a_released_row_is_read_again_in_a_fragment.py:2784-2786`.
`again` is `(held_hash, None)` exactly when the last walk left the
coordinate. `want` then ends with the same tuple, and `parts == want` was
asserted one line earlier, so `again == recorded` cannot fail on its own. The
docstring says the case checks that a second run appends nothing. It does
not. Run 2 through `main` (above) is what showed that, for three shapes.

## How each question in the prompt was answered

- **(1) Does the fold hand MOVES what the file holds?** Executed, for three
  shapes, both through `reverify` with MOVES logged and through `main` with
  `Pact notify | always`, twice each (table in the summary). In each shape
  the parts end at the hash the file holds after the run. The 36-sequence
  case calls `ec.walked_move` and `ec.owed_moves`, the code's own functions.
  Its walk-to-call mapping (moved is the file's hash and a new one, left is
  the file's hash and None, unchanged folds only after an earlier part) is
  the one `reverify` makes; the logged calls match it in all three shapes.
  Its expected parts are written from the rule, so they cannot simply agree
  with the code. Read, not enumerated by the case: a move in a row
  `left_whole` under `--checked` (not folded, as before #791), a citation
  (skipped), and a re-anchored coordinate, whose key changes on the next
  walk because the key carries the coordinate's text.
- **(2) Can left then unchanged happen in one run?** Yes. It is executed in
  ⬜ 1. The `still` calls are load-bearing and pinned by nothing.
- **(3) Do the documents say what the code does?** Read. The `reverify`
  docstring (*where the last walk that reached it left it*) and the
  `walked_move` and `owed_moves` docstrings say what the code does. E4 and
  `docs/the-pact.md:132-134` say *a later walk*, and the code reads the last
  walk. The two readings differ only for a move, then a leaving, then a
  second move. I did not construct that sequence, and it is not a finding.
  The pin at `tests/test_a_signatory_records_a_pact_change.py:1330-1333`
  quotes the sentence as it stands. E4's *the fold's four rules each red
  under `bin/mutation-check`*: I made five mutations of my own to those rules
  (the unchanged clear, the first-hash default, the landed hash, the BROKEN
  hash, the move hand-over). Each was red on the 36 cases.
- **(4) Was the 2026-10-05 re-stamp a recorded reading?** Read. `01e3ad6b`
  changes eighteen rows (lines 2, 3, 4, 8, 9, 10, 12, 13, 14, 16, 21, 24, 25,
  28, 31, 32, 33, 36). Its message names the same eighteen: E2, E3, E4, the
  `Corrected ·` row over 0.18.0:79, and the `Re-read ·` rows over P2-1,
  MALFORMED, O4, R1, R2, H1, C1, W8, W9, F2, the three 0.4.0 rows and
  `display_name`. The hash moves are `reverify@c228822f → @d3e718d4` (sixteen
  rows, E4's included), the pact section `a07d7285 → f36bdf73` (E2, F2), and
  its pin `e1217a3b → 227c0976` (E2, W8). The dates already read 2026-10-05,
  so none changed. Between the two `reverify` hashes, the fold and the
  `still` calls are the only change. Of the cited claims, only C1 (*the same
  move or the same BROKEN is not appended again*) and E4 speak about the
  record. Both hold, by the executed second runs. W8, W9, E3, R1, R2, F2 and
  the rest speak about printing, strict reads, walking, dating and naming,
  which the fold does not touch. The first pass's question is answered: the
  reading is now in a commit message.

## Regression tests to plant

Destination: `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
beside `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken`. It is
the case under *Paste-ready fixes*, seen green at `e50ef3d6` and red with
`still` a no-op.

## Facts for the evidence ledger

- If the case lands, E4 gains it as a coordinate. Its clause can then say
  that a walk reading the coordinate unchanged clears a leaving before it.
  E4's Executed cell would carry *the `still` calls red under
  `bin/mutation-check` with the case*. As it stands, they survive.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Left then unchanged happens inside one run, against the smith's grounds, and the `still` calls that keep its record right are pinned by no case | `skills/evidence-check/scripts/evidence_check.py:3159` | open | Executed in the clone at e50ef3d6: a reverted `handler` makes walks left, left, unchanged for X1; MOVES holds nothing for X1 and `--strict` is 0, and with `still` a no-op X1 is `(0166b3c4, None)`; `bin/mutation-check` SURVIVED over the two touched modules (515 passed); the case under Paste-ready fixes is green at e50ef3d6 and red under that mutation; no defect ships, round 2's white 2 is the precedent |
| ⬜ 2 | Walk 0 prints `the check calls this DRIFTED; left` for a coordinate that a later walk reads unchanged, and no later line takes it back | `skills/evidence-check/scripts/evidence_check.py:3183` | open | Executed in the same probe: `--strict` 0 after the run; the unit is this branch's repeated walk (#772), outside the post-review range; for the orchestrator to file with the first pass's ⬜ 2 |
| ⬜ 3 | The 36-sequence case's second-run assertion follows from its first and checks nothing on its own | `tests/test_a_released_row_is_read_again_in_a_fragment.py:2786` | open | Read: `again` equals `want[-1]` whenever the last walk left the coordinate, and `parts == want` is asserted first; the second run was shown through `main`, not by this case |
| 🟢 | The first pass's finding is closed — a move then a leaving is handed over as that move and then BROKEN at the hash the file holds, and a second run appends nothing | `skills/evidence-check/scripts/evidence_check.py:3019` | confirmed | Executed through `main`, `Pact notify` always: X1 `@5127adb5 → @07b2ad6b`, `@07b2ad6b` BROKEN, run 2 nothing; the case `test_a_restamp_a_later_walk_leaves_is_a_move_and_then_broken` passes in the 515 |
| 🟢 | Round 3's closure is kept — two moves are one part from the pre-run hash | `skills/evidence-check/scripts/evidence_check.py:3002` | confirmed | Executed through `main`: X1 `@5127adb5 → @46e82957`, run 2 nothing, `--strict` 0 |
| 🟢 | The 36-sequence case models the real walk and calls the code's fold; its expected parts come from the rule | `tests/test_a_released_row_is_read_again_in_a_fragment.py:2755` | confirmed | Executed: the calls `reverify` made in three shapes match the case's mapping; five mutations of the fold's rules each red on the 36; read: `left_whole` moves, citations and re-anchored keys are outside the enumeration |
| 🟢 | The docstrings, E4, the pact sentence and its pin say what the code does | `docs/the-pact.md:132` | confirmed | Read against `:3002-3030`, `:3441`, `:3458`; *a later walk* and *the last walk* differ only for move, leaving, move, which was not constructed |
| 🟢 | The first pass's question is answered — the 2026-10-05 rows are a recorded reading, and no dated row's claim is contradicted | `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md:2` | confirmed | Read: the eighteen rows `01e3ad6b` changes are the eighteen its message names; the hash moves are `reverify` (16), the pact section (2) and its pin (2); only C1 and E4 speak about the record and both hold by the executed second runs |

## Executed probes

| What was run | Result |
|---|---|
| Round 3's shape: `reverify` with MOVES logged, then `main` `--reverify --checked 2026-03-01 .` twice with `Pact notify` always on a declared branch, `--strict` after each | X1 one part `@5127adb5 → @46e82957`; walks moved, moved; run 2 appends nothing; `--strict` 0 |
| The first pass's shape, the same way | X1 `@5127adb5 → @07b2ad6b`, `@07b2ad6b` BROKEN; walks moved, left; run 2 appends nothing; run 1 and run 2 exit 1 on the first pass's ⬜ 2 LEFT line; `--strict` 2 (X1 DRIFTED) |
| The revert shape, the same way, at e50ef3d6 and with `still` a no-op | walks left, left, unchanged; X1 nothing at e50ef3d6 and `(0166b3c4, None)` with the no-op; the file ends byte for byte the v1 file; record without X1, run 2 nothing, `--strict` 0 |
| `bin/mutation-check`, `still`'s `if key in parts:` to `if False:`, over the two touched modules | SURVIVED, 515 passed |
| The proposed case at e50ef3d6, then under the same mutation; `ruff check`, `ruff format --check` on the module with it | 1 passed; red; clean |
| `bin/mutation-check` on the 36 cases, five mutations: `if new == old:` off; first hash always the walk's; landed always the walk's new; BROKEN always at the first hash; no move handed over | red each time (5, 18, 7, 6 and 24 failed of 36) |
| The full suite, the repository lint and the typecheck at this branch's head | not yet — not run by this pass; the sealer's, once the post-review fix settles |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 2 — walk 0's left line for a coordinate a later walk clears | candidate: the issue the first pass's ⬜ 2 goes to, as one family (what the run prints about a coordinate a later walk changes) | the orchestrator of this run, filing it for the next milestone |
| the first pass's ⬜ 2 — `run it without --ledger` for a coordinate the run left itself | already deferred in `post-review-check.md`; seen again in this pass's probe | the orchestrator of this run, as that report says |

## Paste-ready fixes

### ⬜ 1 — pin the `still` calls

```python
def test_a_coordinate_left_and_then_read_unchanged_records_nothing(repo):
    """Second post-review pass of #791. A walk can leave a coordinate and a
    later walk read it unchanged. X1 was stamped while handler was at v1,
    quoting the citation hash its `Re-read ·` line held then; handler moved
    and came back, so the run re-stamps that line back to the bytes X1
    recorded. Two walks find the quoted hash gone and leave X1, the third
    reads it unchanged, and the file ends where X1's hash says. MOVES holds
    nothing for X1: a BROKEN from the walks that left it would write the
    permanent record a trigger for a coordinate `--strict` reads clean. Red
    with `still` a no-op."""
    o = unit_hash(repo, "src/service.py", "other")
    day = "2026-03-01"

    def r1(h):
        return (
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | {day} | |"
        )

    def reread(cite, h):
        return (
            f"| Re-read · the row it cites | `{cite}`, "
            f"`src/service.py#handler@{h}` | read | {day} | Re-read {day} |"
        )

    def cite_for(h):
        released(repo, [r1(h), reread(citation(r1(h), "R1 · handler adds one"), h)])
        return ec.citation_for(str(repo), str(repo / R_FILE), 5)

    def write(h, cite, x):
        (repo / R_FILE).write_text(
            f"## 0.1.0 — 2026-01-01\n\n{SECTION}\n\n{r1(h)}\n{reread(cite, h)}\n\n"
            "### 1000000002-the-second-item\n\n"
            f"| X1 · other, beside the re-read | `src/service.py#other@{o}`, "
            f"`{x}` | read | {day} | |\n",
            encoding="utf-8",
        )

    h1 = unit_hash(repo, "src/service.py", "handler")
    cite1 = cite_for(h1)
    x = citation(reread(cite1, h1), f"@{cite1.rsplit('@', 1)[1]}")
    write(h1, cite1, x)
    assert run(["--strict", "."], repo).returncode == 0
    before = (repo / R_FILE).read_text(encoding="utf-8")
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    write(h2, cite_for(h2), x)
    (repo / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    moves = []
    ec.reverify([str(repo / R_FILE)], str(repo), {}, None, day, moves)
    assert (repo / R_FILE).read_text(encoding="utf-8") == before
    assert [m for m in moves if m[1] == 10] == [], moves
    assert run(["--strict", "."], repo).returncode == 0
```

### ⬜ 3 — let the second-run assertion say only what it checks

```diff
--- a/tests/test_a_released_row_is_read_again_in_a_fragment.py
+++ b/tests/test_a_released_row_is_read_again_in_a_fragment.py
@@ -2781,6 +2781,1 @@ def test_every_walk_sequence_hands_over_what_the_file_holds(walks):
     assert parts == want, (walks, parts)
-    # A second run reads the file as the first left it: the coordinate is
-    # left again where the last walk left it, else unchanged.
-    recorded = parts[-1] if parts else None
-    again = (held_hash, None) if ends_left else None
-    assert again is None or again == recorded, (walks, parts)
```

and, in that case's docstring, drop the clause *a second run of
`record_pact_changes`'s last-word rule over the same coordinate appends
nothing*, which the case does not run.

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened in this pass:

- `skills/evidence-check/scripts/evidence_check.py` — `walked_move` and
  `owed_moves` (`:3002-3030`), `cited_first`, `reverify` (`:3091-3470`),
  `resolve_unit`, `minor_region`, `recorded_here`, `coordinate_of`,
  `planned_key`, `read`, `content_matches`, `record_pact_changes`
  (`:4090-4290`), `pact_change_item`
- `tests/test_a_released_row_is_read_again_in_a_fragment.py` — helpers
  (`:28-150`), `:2640-2790`
- `tests/test_a_signatory_records_a_pact_change.py` — helpers (`:20-123`),
  the declared-branch case, the property case, the pin (diff)
- `docs/the-pact.md:130-136` (diff)
- `seal/ledger/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move.md`
  — every row's label, `reverify` hash and date; E2, E3, E4, C1, W8, W9 and
  F2 whole
- `seal/releases/0.18.1.md` — the C1, W8, W9 and F2 rows the fragment cites
- `seal/specs/1791119072-one-reverify-leaves-the-ledger-clean-and-records-only-a-real-move/post-review-check.md`,
  `survivors.md` (diff), `spec.md` (grep), `rounds/round-3.md` (Deferred)
- commit messages of `a394d118`, `01e3ad6b` and `e50ef3d6`
- `bin/test`, `bin/mutation-check`
