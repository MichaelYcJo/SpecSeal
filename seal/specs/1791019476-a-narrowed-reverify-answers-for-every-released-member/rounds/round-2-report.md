# Round 2 report — #740, a verifying round over round 1's fixes

Ran by: `specseal:warden on claude-opus-5-5`.

| Field | Value |
|---|---|
| Work item | `1791019476-a-narrowed-reverify-answers-for-every-released-member` |
| Branch | `fix/740-a-narrowed-reverify-answers-for-every-released-member` |
| Target SHA | `2e595b8e` |
| Fix range | `465adf33..604f8969`, then the merge `5e7e75de` of `9511f6cd` and the close `2e595b8e` |
| Where it ran | a `git clone --no-local` of the worktree at `2e595b8e`, and a second at `465adf33` for the before-the-fix runs, both under the session scratchpad; the worktree's HEAD was never moved |

## Summary

Every fix round 1 commissioned is closed at its commit. Round 1's one
blocking-for-the-run finding, the coordinate only fragment re-reads carry,
is closed in all three modes. The grid's new axis turns 7 of its 72 new cells
red against `465adf33`'s checker, which matches the build's account. The
released-root guard, the S3 case and the narrowing notice were each seen red
by breaking the line they pin. The merge lost nothing: `correction-check`
finds no dropped marker, every anchor of #736's fragment kept the side that
moved it, and `evidence-check --strict .` reads 4,029 ok and 0 drifted.

Three new findings, all ⬜. None needs a fix for the run to end:

- **⬜ 10** is a correction to the run's records. The fix changed one
  unnarrowed run, and N1, the changelog and spec D3 still say a run without
  `--ledger` behaves as before.
- **⬜ 11** is the class ⬜ 8 belonged to. The home names one family a
  re-read cannot clear, the double correction, and two more behave the same
  way.
- **⬜ 12** comes from #736's `--into` and not from this item. A `--checked`
  date older than the family's newest reading writes a row that clears
  nothing, and the run exits 0.

**The class round 1 opened is closed on every axis the prompt named.** 105
runs outside the 144 cells covered families of four members, a `Corrected ·`
row beside re-reads, `seal/ledger.md` in both roles, and one coordinate
carried by released and fragment rows on different dates. Every
configuration that varies a narrowing axis holds. What still exits 0 while
`--strict` exits 2 is a coordinate no re-read can clear, plus ⬜ 12. Those
behave the same narrowed and unnarrowed, and the same at `465adf33`.

## Each fix at its commit

**Round 1's finding 1, `27b6991e` — closed. Executed.**

- `released_drift` now takes the first released member carrying the
  coordinate. Where there is none, it falls back to the first member that is
  not BROKEN, but only under a released root (read, `evidence_check.py:3298-3327`).
- HEAD's new cases, run against `465adf33`'s checker, gave 11 failures:
  - 7 of the grid's 72 new cells;
  - the round's case in all three modes;
  - one cell of the S3 case, the fragment re-reads-only cell.
- At HEAD the module and its two siblings pass, 236 cases.
- My own probes outside the grid were red at `465adf33` and green at HEAD:
  - four members spread over three fragments (12 of 12);
  - a folded `Corrected ·` root whose re-reads sit in fragments (3 of 3,
    narrowed to M);
  - a root in `seal/ledger.md` (3 of 3, narrowed to M).
- The docstring of `released_drift` says what the loop does.
- The home's sentences at `docs/the-evidence-ledger.md:140` and `:168`, L4,
  N1's first clause and the changelog entry now hold in round 1's cell. N1
  still has one false clause, which is ⬜ 10.

**The released-root guard, a unit the fix created — confirmed. Executed.**
I deleted the two guard lines in the clone. With them gone,
`test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read` failed: the
run named `seal/ledger/2000000001-a-later-item.md:1` as a released row left,
and gave the `--into` repair for it. With the lines restored, it passes. The
case is a real pin, but commit `27b6991e` does not say it was seen red;
§15 is met by this run and not by the fix's handover.

**Round 1's finding 2, `5c8baa17` — confirmed. Read.** The home now reads
*named with each of them as written* (`docs/the-evidence-ledger.md:103-105`).
The code names each string once (`evidence_check.py:2503-2513`). The
changelog's second entry still describes the one-date case. That is not
false, because it claims nothing exclusive, so it is not a finding.

**Round 1's finding 3, `bf9d833a` — confirmed. Executed.**
`dict.fromkeys` keeps the cell's first order, and the last date joins with
"and". The case gained a three-date cell and a repeated-date cell, and both
are red at `465adf33` (executed, as part of the copy of HEAD's module).

**Round 1's finding 4, `14a56599` — confirmed. Read** against the f-strings
below it.

**Round 1's finding 5, `da825ff1` — answered. Read.** N2 now quotes the
printed message, and its hashes are current (`--strict` reads 0 drifted).

**Round 1's finding 6, `e17069fa` — confirmed. Executed.** Every narrowed
cell of the grid now asserts that the output opens with the narrowing notice.
I broke the notice's wording in the clone and at least 12 cells went red. The
control's docstring now says what round 1's probe CONTROL measured.

**Round 1's finding 7, `bf27f5f5` — confirmed. Executed.** In the clone I
made `released_drift` key the owed entry on the picked member instead of the
root. The S3 case went red in both re-reads-only cells, and 3 grid cells went
red with it. The root-carrier cells survive that break, because there the
picked member is the root. That is why the case runs over both carriers, as
the commit says.

**Round 1's finding 8, `9c93f814` — confirmed. Executed.** A double
correction gives `--strict` exit 2 and `--reverify` exit 0 in all three
modes, narrowed and not (probe P8, 6 of 6). The home's new sentence at
`docs/the-evidence-ledger.md:171-173` says exactly that. The class the
finding belonged to is wider than this one instance, which is ⬜ 11.

**Round 1's finding 9, `b0a41a09` — answered. Read** against `root_of`,
`cited_row` and the guard. D3's corrected sentence is true about
fragment-rooted families. Its headline, *Unnarrowed runs do not change*, is
not true, which is ⬜ 10.

## The units the fix pass created

- **The grid's new axis, 144 cells.** `three_readings` with `re-reads only`
  makes M and N carry `other`, which R does not cite. Only the cells with
  both readings in fragments reach the new branch: 18 cells, 7 of them
  violations before the fix. The other placements reach the released branch
  and act as controls. Read and executed.
- **`test_a_narrowed_reverify_answers_for_a_coordinate_only_fragments_carry`.**
  Red in all three modes at `465adf33`, green at HEAD. Executed.
- **`test_a_family_rooted_in_a_fragment_is_owed_no_released_re_read`.** Seen
  red with the guard removed (above). It asserts only the absence of a `LEFT`
  line naming a fragment, which is what the guard decides. Executed.
- **⬜ 3's join and dedupe.** Read and executed (above).
- **⬜ 6's pinned notice.** It pins the notice's first words, not the list of
  files under them. The docstring says the run *names the files it did not
  read before anything else*, and the header line is what states that. I
  read this as held. Executed.
- **⬜ 7's two-carrier case.** Seen red with the root-keyed entry broken
  (above). Executed.

## The grid's axes, again — is the class closed?

Every probe below asks one question per run: does a narrowed `--reverify`
exit 0 while `--strict` with the same narrowing does not? 105 runs went
against HEAD's checker and the same 105 against `465adf33`'s. The table under
§Executed probes has the totals.

| Configuration | HEAD | `465adf33` |
|---|---|---|
| P1: four members, `other` carried by three fragment re-reads only; narrowed to M1, M2, M1 with M2, R with M1 | holds, 12 of 12 | violates, 12 of 12 |
| P1b: four members, one older re-read folded into 0.2.0 | holds, 6 of 6 | holds |
| P2a: a folded `Corrected ·` row roots the family, and fragment re-reads of it carry `other` | holds, 9 of 9 | violates narrowed to M, 3 of 3 |
| P2b: a fragment `Corrected ·` row supersedes R beside re-reads of R | holds, 6 of 6 (R's family is superseded) | holds |
| P3: the root in `seal/ledger.md`, re-reads only in fragments | holds, 6 of 6 | violates narrowed to M, 3 of 3 |
| P3b: the older re-read in `seal/ledger.md`, the newest in a fragment | holds, 6 of 6 | holds |
| P4: one coordinate carried by a folded and a fragment re-read on different dates, in four date orders (one impossible, one a tie), narrowed three ways | holds, 36 of 36 | holds |
| P5: `--into --checked` with a date before N's | violates under `--into`, 2 of 2 carriers | the same, and the other two modes too |
| P6: fragment-only carriers whose unit is gone | narrowed to M holds; unnarrowed exits 0 against `--strict` 2 | the same |
| P7: a fragment-only carrier whose anchored statement is gone | exits 1, 6 of 6 | exits 0 against `--strict` 2, 6 of 6 |
| P8: a double correction | exits 0 against `--strict` 2, 6 of 6 (the home's stated exception) | the same |
| P10: BROKEN coordinates, carried by a fragment only, by a released singleton, and by both | exits 0 against `--strict` 2 wherever the narrowing reads a BROKEN carrier, except under the freeze where a released row carries it | the same |
| P11: a fragment `Corrected ·` root whose anchored statement is gone | exits 0 against `--strict` 2, narrowed and not | the same |

**The answer is yes for the class round 1 opened.** No configuration that
varies the number of members, a `Corrected ·` row, `seal/ledger.md`, the
dates or the carriers escapes a narrowing any more. What remains is in three
groups, and none of them depends on the narrowing:

- **Coordinates no re-read can clear.** These are a BROKEN anchor (P6, P10),
  a row corrected by two rows (P8), and a statement gone from a row whose
  family is rooted in a fragment (P11). They behave the same narrowed and
  unnarrowed, before the fix and after it. The home scopes out only the
  second, which is ⬜ 11.
- **A `--checked` date older than the newest reading** (P5). This is #736's
  `--into`, and it is ⬜ 12.
- **P7 moved the other way.** The fix turned an exit 0 into an exit 1, which
  is right. P7 is also an unnarrowed run, which is ⬜ 10.

## The merge `5e7e75de`

**Executed.** `bin/correction-check --range 9511f6cd...HEAD` examined one
merge commit and reports that no correction marker was dropped and that no
released ledger file changed. `9511f6cd` is what the worktree's
`origin/release/v0.18.0` names, and the clone has no such remote ref.

**Executed.** `bin/evidence-check --strict .` at `2e595b8e` reads 4,029 ok,
0 drifted, 0 broken, and on the records arm 0 refused and 0 drifted. It
exits 0.

**Executed, anchor by anchor.** I compared every anchor in #736's fragment
across the merge base `2b1dcb1f`, this branch at `604f8969`, `9511f6cd` and
the merge:

- 20 anchors moved;
- none moved on both sides;
- each kept the side that moved it, including the two conflicted hunks at
  lines 17–18 and 29–30;
- the only non-hash text that differs is L4's new `Corrected` note, which
  only this branch wrote.

## The ledger

| Row | Unit moved in `604f8969` | Holds? |
|---|---|---|
| L1 | `family_view` | Holds. Only `reading`'s message changed; the family, the ordering and the verdicts did not. Read |
| L4 | `released_drift` | Holds. *Whichever members carry the drifted coordinate* is true in the grid and in P1–P4. The new `Corrected` note's figures, 7 of 72 and the round's case in three modes, are what `465adf33` gives. Read and executed |
| L9 | the home's section | Holds. The one-home module and its four neighbours pass, 134 cases. Executed |
| `Corrected ·` the de-duplication (line 25) | `family_view` | Holds. `dict.fromkeys` removes repeated date strings, not rows, so the claim that `family_view` does not de-duplicate rows still holds. Read |
| `Corrected ·` the freeze rule's home (line 57) | the home's section | Holds. The added sentences restate nothing a carrier holds. Read |
| N1 (this item) | corrected in place | One clause is false. *A run without `--ledger` answers as before* fails in P7, which is ⬜ 10. *144 cells* is 2 × 2 × 2 × 6 × 3. The executed figures match. Read and executed |
| N2 (this item) | corrected in place | Holds. It quotes the message the code prints. Read |

## Findings

### ⬜ 10 — a run without `--ledger` changed, and three records say it did not

**What is wrong.** Here is P7. R, in a release file, cites `handler`. A
fragment re-read M cites R and adds `other>"x * 2"`. The code then changes
`x * 2`, so the statement M's anchor names is gone. No re-stamp in place can
clear that, so `--strict .` exits 2.

- At `465adf33`, and at the base before it, `--reverify .` exits 0 in all
  three modes, because only released members were graded.
- At HEAD the fragment-only branch picks M and names R, and the run exits 1
  in all three modes.

That is the right direction: P9 shows that a released carrier with the same
gone statement already exits 1, at both commits. It is still a change to an
unnarrowed run. Three records say no such change happens:

- N1 (`seal/ledger/1791019476-…md:1`): *a run without `--ledger` answer[s]
  as before*;
- the changelog fragment, lines 13–14: *a run without `--ledger`, behave as
  before*;
- spec D3's headline, line 72: *Unnarrowed runs do not change*.

**Why it matters.** The changelog fragment is what the release note is
gathered from, and N1 is a ledger claim that the evidence check cannot see
is false. A person who reads either would not expect a new exit 1 from a
plain `--reverify`.

**What the run prints there is not new.** Without the freeze it says that
the newest reading *sits in a file this run did not write; run it without
`--ledger`*, in a run that had no `--ledger`. Under `--into` it says *no one
place to hash, so not re-read*. Both lines come from the code a released
carrier already went through (read: the no-freeze branch of `main`, and
`reverify_into`). So the messages are not this finding. The records are.

This is a correction to the run's paperwork: every location is under
`seal/`.

### ⬜ 11 — the home names one family no re-read can clear, and there are three

**What is wrong.** Two sentences make the same promise. The one at
`docs/the-evidence-ledger.md:165-169` says a narrowed `--reverify` names
*each family that a file it read holds a member of … where no in-place
re-stamp of the files it read clears that family, … and exits 1*. Round 1's
⬜ 8 fix added one exception after it, the double correction (`:171-173`).
Two more configurations behave the same way and are not named:

- **A BROKEN anchor.** Without the freeze, `--reverify` reports a BROKEN row
  it read as *left* and exits 0. Under the freeze it does the same where
  only fragment rows carry the coordinate (P10a, and P6). `--strict` exits 2.
- **A statement gone from a row whose family is rooted in a fragment** (P11).
  The in-place re-stamp says *left*, and the guard keeps the family from
  being named, so the run exits 0 against `--strict` 2.

Both behave the same at `465adf33`. Only the sentence is this item's.

**Why it matters.** It is the same gap ⬜ 8 closed for one instance. A
reader who trusts *exits 1* will read an exit 0 as clean.

### ⬜ 12 — `--into` with a `--checked` date older than the newest reading writes a row that clears nothing

**What is wrong.** P5 is the grid's family with both readings in fragments,
narrowed to M. The run passes `--into --checked 2026-02-15`, a date between
M's and N's. It writes a `Re-read ·` row dated 2026-02-15 that cites R and
prints *1 citing row written*, then exits 0. N, dated 2026-03-01, still
outranks every other reading, so `--strict` reads M DRIFTED and exits 2,
narrowed and whole. This happens with either carrier and the same at
`465adf33`. The code is `reverify_into` (`evidence_check.py:3348`), which
writes the row without asking whether its date can outrank the reading it
answers.

**Why it matters, and why it is not this item's.** A person who backdates
`--checked` to the day they read the code gets an exit 0 for a family that is
still owed. The DRIFTED line names the newer date, so the state is visible
afterwards. The behaviour belongs to #736's `--into` (#715), which the
narrowing did not touch. I list it here because the prompt asked for every
configuration where the exit codes disagree. Its home is the orchestrator's
call. I propose an issue against `--into`, with the repair to name the row
LEFT when `--checked` is older than the newest reading of a coordinate it
would write.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — a coordinate only fragment re-reads carry is now graded under a released root, and the narrowed run names or writes for the root in all three modes | `skills/evidence-check/scripts/evidence_check.py:3298` | confirmed | Executed: HEAD's new cases against `465adf33`'s checker fail 7 grid cells, the round's case in 3 modes and 1 S3 cell; all pass at HEAD, 236 cases with the two siblings; probes P1, P2a and P3 red before and green after |
| 🟢 | round 1's finding 2 is closed — the home names every impossible date | `docs/the-evidence-ledger.md:103` | confirmed | Read against `reading` |
| 🟢 | round 1's finding 3 is closed — one list joined with "and", each string once | `skills/evidence-check/scripts/evidence_check.py:2505` | confirmed | Executed: the three-date and repeated-date cells red at `465adf33`, green at HEAD |
| 🟢 | round 1's finding 4 is closed — the docstring says what the code prints | `skills/evidence-check/scripts/evidence_check.py:2492` | confirmed | Read |
| 🟢 | round 1's finding 5 — N2 quotes the printed message | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:2` | answered | Read; hashes current under `--strict` |
| 🟢 | round 1's finding 6 is closed — the notice is pinned and the control's docstring is true | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1598` | confirmed | Executed: at least 12 grid cells red with the notice's wording broken |
| 🟢 | round 1's finding 7 is closed — S3's root naming is pinned over both carriers | `tests/test_a_released_row_is_read_again_in_a_fragment.py:1631` | confirmed | Executed: both re-reads-only cells red with the entry keyed on the picked member |
| 🟢 | round 1's finding 8 is closed — the home states the double correction's exit codes | `docs/the-evidence-ledger.md:171` | confirmed | Executed, P8: `--strict` 2, `--reverify` 0, narrowed and not, 3 modes; the class is ⬜ 11 |
| 🟢 | round 1's finding 9 — D3 says why a fragment-rooted family adds nothing | `seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/spec.md:72` | answered | Read; the headline is ⬜ 10 |
| 🟢 | the released-root guard holds and its case is a real pin | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Executed: red with the guard deleted, green restored |
| 🟢 | the merge lost no correction and kept every moved hash | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Executed: `correction-check` none dropped; 20 anchors compared, none moved on both sides; `--strict .` 4,029 ok, 0 drifted, 0 refused |
| 🟢 | the five rows `604f8969` re-stamped hold against the edit | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` | confirmed | Read row by row; table above |
| 🟢 | the class round 1 opened is closed outside the 144 cells | `skills/evidence-check/scripts/evidence_check.py:3292` | confirmed | Executed: 105 runs, P1–P4 hold in every cell; the remaining disagreements are ⬜ 11 and ⬜ 12, and behave the same at `465adf33` |
| ⬜ 10 | A run without `--ledger` now exits 1 and names the released root where a coordinate only fragment re-reads carry has lost its anchored statement; it exited 0 before. N1, the changelog fragment and spec D3 say unnarrowed runs behave as before | `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md:1` | open | Executed, P7: exit 0 in 3 modes at `465adf33`, exit 1 at HEAD; the paste-ready case is red at `465adf33` and green at HEAD. A correction to the run's records |
| ⬜ 11 | The home's narrowed-run promise names one family no re-read can clear, the double correction; a BROKEN anchor and a statement gone from a fragment-rooted family also exit 0 against `--strict` 2 | `docs/the-evidence-ledger.md:171` | open | Executed, P6, P10, P11: the same at HEAD and `465adf33`; the sentence is this item's |
| ⬜ 12 | `--into` with a `--checked` date older than the family's newest reading writes a row that does not outrank it and exits 0, while `--strict` still exits 2 | `skills/evidence-check/scripts/evidence_check.py:3348` | open | Executed, P5: both carriers, at HEAD and `465adf33`. #736's behaviour, not this item's class; its home is the orchestrator's call |
| ❓ | The Windows leg: the separator handling of the cases the fix pass added | `tests/test_a_released_row_is_read_again_in_a_fragment.py` | ❓ out of verified scope | Read only: the new cases compare printed names, which `built_name` writes with `/`. The pull request's Windows CI leg answers it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the module, `test_two_branches_re_read_one_released_row.py` and `test_a_narrowed_ledger_read_says_what_it_skipped.py` at `2e595b8e` | 236 passed |
| HEAD's module copied into a clone at `465adf33`, the four new or changed case families selected | 11 failed, 141 passed: 7 grid cells, the round's case in 3 modes, 1 S3 cell |
| the released-root guard deleted in the clone, its case run | 1 failed, naming `seal/ledger/2000000001-a-later-item.md:1` LEFT; restored |
| `released_drift` keying the owed entry on the picked member, the S3 case and the grid run | 5 failed: both re-reads-only S3 cells, 3 grid cells; restored |
| the narrowing notice's wording changed, the S3 case and the grid run | at least 12 grid cells failed; restored |
| Warden probes P1–P8, 105 runs, against HEAD | 11 disagreements: P5 under `--into` (2), P6 unnarrowed (3), P8 (6) |
| the same 105 runs against `465adf33` | 37 disagreements |
| Warden probe P9: a released singleton and a folded re-read whose statement is gone, both checkers | exit 1 in all 12 runs at both |
| Warden probe P10: BROKEN carried by a fragment only, by a released singleton, and by both, both checkers | identical at both; exit 0 against `--strict` 2 except under the freeze where a released row carries it |
| Warden probe P11: a fragment `Corrected ·` root whose statement is gone, narrowed and not, both checkers | exit 0 against `--strict` 2 in all 6 runs at both |
| ⬜ 10's paste-ready case, at HEAD and at `465adf33` | 3 passed at HEAD; 3 failed at `465adf33` |
| `bin/correction-check --range 9511f6cd...HEAD` | 1 merge examined, no marker dropped, no released ledger file changed, exit 0 |
| `bin/evidence-check --strict .` at `2e595b8e` | 4,029 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted; exit 0 |
| every anchor of #736's fragment across `2b1dcb1f`, `604f8969`, `9511f6cd` and `5e7e75de` | 20 moved, none on both sides, each kept the side that moved it |
| `bin/test` over the one-home, docs line-wrap, no-real-identifiers, one-word-one-meaning and merge-correction modules at `2e595b8e` | 134 passed |
| `bin/test tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_docs_line_wrap.py`, and `evidence-check --strict .`, with this report staged in the clone | 60 passed; 4,029 ok, records arm 0 refused, exit 0 |
| `round-record new` over this report, in the clone only, the record it wrote then discarded with the clone | exit 0; `Needs a fix` and `Loses a record or crashes` read `no`; `Pass` unchecked over ⬜ 10–12 |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, once the rounds settle |
| `bin/survivor-check` over the fix range | not yet — not run by this round |

```
# P7, as the probe built it (warden probe, deleted)
R  seal/releases/0.1.0.md                         | R1 · handler adds one | `src/service.py#handler@<h>` | read | 2026-01-01 | |
M  seal/ledger/2000000002-m.md                    | Re-read · R1 · … | `<cite R>`, `src/service.py#other>"x * 2"@<stated>` | read | 2026-02-01 | Re-read 2026-02-01 |
code: other now returns x * 3
evidence-check --reverify .                        -> 465adf33: exit 0 · HEAD: exit 1, LEFT seal/releases/0.1.0.md:5
evidence-check --strict .                          -> exit 2 at both, M DRIFTED (the anchored statement is gone)

# P5 (warden probe, deleted)
three_readings(repo, "fragment", "fragment", <either carrier>), freeze declared
evidence-check --reverify --into seal/ledger/4000000001-the-re-reading-item.md --checked 2026-02-15 --ledger <M> .
                                                   -> exit 0, "1 citing row written"
evidence-check --strict --ledger <M> .             -> exit 2, M DRIFTED: the newest reading, 2026-03-01 at N, holds other content
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Regression tests to plant

- **⬜ 10.** Plant the case in ⬜ 10's first fence into
  `tests/test_a_released_row_is_read_again_in_a_fragment.py`, after the
  fragment-rooted guard's case. It was run: red at `465adf33` in all three
  modes, green at HEAD. It pins the exit 1 that the corrected records will
  describe.

## Facts for the evidence ledger

- **N1** takes ⬜ 10's clause, with a `Corrected <date>` note, and cites the
  planted case.
- **L4** needs no change. Its narrowing clause makes no claim about a run
  without `--ledger`.

## Paste-ready fixes

### ⬜ 10 — the case, and the three records

```python
@pytest.mark.parametrize("mode", MODES)
def test_an_unnarrowed_reverify_names_a_root_whose_fragment_only_statement_is_gone(
    repo, mode
):
    """Round 2, finding 10: a coordinate only a fragment re-read carries, whose
    anchored statement is gone, is one no in-place re-stamp clears. A run
    without `--ledger` names the family's released root and exits 1, as it
    does where a released row carries the coordinate."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
        ],
    )
    text = (repo / "src" / "service.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/service.py", "other", text)
    (inside,) = ec.minor_region("src/service.py", text, places[0], '"x * 2"')
    stated = ec.content_hash(ec.gfm_lines(text)[inside[0] - 1 : inside[1]])
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f'`src/service.py#other>"x * 2"@{stated}` | read | 2026-02-01 | '
            "Re-read 2026-02-01 |"
        ],
        name="2000000002-the-older-re-read",
    )
    (repo / "src" / "service.py").write_text(
        SERVICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    if mode != "no freeze":
        frozen(repo, "0")
    into = ["--into", MEMBER_INTO, "--checked", "2026-04-01"]
    out = run(
        ["--reverify", *(into if mode == "freeze with --into" else []), "."], repo
    )
    assert out.returncode == 1, out.stdout
    assert "LEFT  seal/releases/0.1.0.md:5" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 2
```

```diff
--- a/seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/changelog.md
+++ b/seal/specs/1791019476-a-narrowed-reverify-answers-for-every-released-member/changelog.md
@@
   names it with the `--into` form. That holds whichever rows carry the
-  drifted coordinate, including one only fragment re-reads record. A
-  narrowing to a file that holds no member of the family, and a run without
-  `--ledger`, behave as before.
+  drifted coordinate, including one only fragment re-reads record. A
+  narrowing to a file that holds no member of the family behaves as before,
+  and so does a run without `--ledger`, with one exception: where a
+  coordinate only fragment re-reads record has lost the statement its anchor
+  names, the run now names the family's first row and exits 1, as it
+  already did where a released row recorded that coordinate.
```

```
N1's claim, replacing "a narrowing to a file holding no member, and a run without `--ledger`, answer as before":

  a narrowing to a file holding no member answers as before, and so does a run without `--ledger` except where a coordinate only fragment re-reads carry has lost its anchored statement, which it now names by the released root and exits 1 for, as it did where a released row carried it

N1's Notes, appended:

  **Corrected <date> by round 2's fix pass (⬜ 10):** the fragment-only branch reaches a run without `--ledger` where no re-stamp clears the coordinate; red at 465adf33 in all three modes.

spec.md, D3, appended after the paragraph:

  *Corrected <date> by round 2's fix pass (⬜ 10): one unnarrowed run does change. A coordinate only fragment re-reads carry whose anchored statement is gone is one no in-place re-stamp clears; it used to exit 0 while `--strict` exited 2, and it now names the released root and exits 1, as a released carrier already did.*
```

### ⬜ 11 — the home names every family a re-read cannot clear

```diff
--- a/docs/the-evidence-ledger.md
+++ b/docs/the-evidence-ledger.md
@@
 narrowing left its file out, because the root is the row a `Re-read ·` cites.
-A row corrected by two rows is not a re-read's to clear: `--strict` names
-each correcting row and exits 2, while `--reverify`, narrowed or not, exits
-0 and leaves the choice of claim to a person.
+Three things are not a re-read's to clear, and `--strict` exits 2 on each.
+A row corrected by two rows leaves the choice of claim to a person, and
+`--reverify`, narrowed or not, exits 0. A BROKEN anchor takes a
+`Corrected ·` row, or an edit where its row sits in a fragment: `--reverify`
+names it left where the run read it and exits 0, except under the freeze,
+where a released row carrying it is named with that repair and the run
+exits 1. A statement gone from a row in a family a fragment roots is that
+fragment's to repair in place, and `--reverify` exits 0.
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened in the clone at `2e595b8e`, or by diff over `465adf33..2e595b8e`:

- `skills/evidence-check/scripts/evidence_check.py`: `family_view`'s
  `reading`, `released_drift` whole, `reverify_into` whole, `reverify`'s
  docstring and its left-and-return paths, `citation_for`'s docstring, and
  `main`'s `--ledger` notice and `--reverify` branches
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the helpers at
  lines 1–175 and 672–690, the double-correction case, and the #740 block
  from `three_readings` to the impossible-date case
- `docs/the-evidence-ledger.md`, lines 90–180
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md`:
  the fix-range diff and the merge's four-way anchor comparison
- `seal/ledger/1791019476-a-narrowed-reverify-answers-for-every-released-member.md`
- this work item's `spec.md` (D3), `changelog.md`, `rounds/round-1.md` and
  `rounds/round-1-report.md`
- the commit messages of `465adf33..604f8969`, `5e7e75de` and `2e595b8e`
- `bin/test`

Every probe file, the probe repositories and both clones were deleted before
hand-over.
