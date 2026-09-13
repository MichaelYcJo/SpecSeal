# Round 2 — 1789296200-the-record-before-the-fix-sequence-has-no-arm

The verifying round. Target SHA `3db3a3a`, scope `git diff b88a0b2..80040fe`
— the nine fix commits — plus the record correction `3db3a3a` itself. Branch
`feat/345-the-record-before-the-fix-sequence-has-no-arm`, draft pull request
381.

**Round 1's fixes hold.** Each of the four was reproduced or mutated by
execution, the two new messages were run and read end to end, and each of the
three units the fix pass added dies alone. This round opens nothing needing a
fix. Two corrections and one question are below, and none of the three is a
defect the release would ship.

**No agent was spawned for this round** (`agent-contract` §6). The
`code-review` skill's Phase 1 and Phase 2 ask for finder and verifier agents;
§6 withholds that from every agent, so the angles were run here. The broad
gate was not run and is not this round's (`agent-contract` §2); §3 was never
reached, because the spawn prompt ordered no check §2 excludes. Every probe
was built and deleted in the session scratchpad, and the worktree was read
only — nothing under it was written but this report.

## What round 1 inherited, and what it carried

Round 1's coordinates were carried and its verdicts were re-derived. What was
NOT re-walked: the branch outside the fix range, which is what makes this
round the cheapest of the run.

## What the fix pass's account claimed, and what the code says

Eight claims were opened. All eight stand, and two of them looked wrong until
they were measured — both are written out below, because a number that looks
wrong and is right is worth the same as one that looks right and is wrong.

**The correction to round 1's own grounds is honest, and it is the narrower
true statement.** I re-ran the four commands myself in this worktree: `git
for-each-ref 'refs/remotes/pull/*'` returns 0, `git for-each-ref
refs/remotes/pull` returns 138, `git for-each-ref 'refs/remotes/pull/*/head'`
returns 138, and `git merge-base --is-ancestor a0f0e9a
refs/remotes/pull/364/head` exits 0. `phases/phase-1.md` §*The population, and
what it takes to stand where the number can be retaken* says exactly that —
the starred pattern is one path component short, the refs reach no clone that
has not fetched `refs/pull/*`, and the named list is what makes the forty
checkable either way. It does not repeat round 1's false claim that the
population is gone. `overview.md:29` now points at
`phases/phase-1-measurement.txt` rather than at a list that was never there.

**The rescued file is what it claims.** `cmp` against the measurement's own
output in the session scratchpad exits 0 and the two SHA-256 digests are
equal, so it is byte-identical. It carries 40 record entries — 40 path lines,
40 `Target SHA` lines, 40 *seen on* lines — and the header reads 310 pairs /
158 excluded / 152 counted / 112 same / 40 differ. The two records
`phase-1.md` opens by hand are at lines 121 and 115, with the SHAs that
record quotes.

**The figure that looked wrong.** `phase-1.md` says the measurement was taken
over 102 refs, and the clone holds 138 pull refs plus 29 countable local
heads — 167. I re-enumerated with the script's own rule: 167 refs have a
merge-base with `main`, and **102** of them add a file under `seal/specs`,
which is the first `continue` the walk passes. The sentence is true and the
reading that makes it true is the script's.

**The red case was red, and the rewording is faithful.** `git show
eb7a56a^:skills/code-review/orchestration.md` carries *spawned before* once,
so `test_the_verifying_round_is_spawned_after_the_fixes[parts3]` was failing
as the commit message says. The example now reads *the fix pass had already
run when the record reached a commit*, which teaches what the old sentence
taught: the flag is for the case where the fixes really did land first.

Two test modules still spell that reason the old way, in a fixture constant —
`tests/test_a_record_says_why_it_was_written_late.py:50` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py:354`. Neither is in
reach of the scan, which reads four documents and no `.py` file, and both
modules are green. It is fixture data rather than a sentence anybody reads.

**Nothing else this branch added is within reach of that scan.** I ran every
one of the eleven needles — the four `SPAWNED_BACKWARDS`, the four
`TARGETED_BACKWARDS`, the three `CAP_BACKWARDS` — over the flattened text of
all four carriers at HEAD. No hits.

## Findings

### ⬜ 6 — `overview.md`'s verified line still carries the pre-fix figures

`seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:6`.
Established by **execution**.

The line says `evidence-check` at *1161 ok · 0 drifted* and *the four units
this branch added*. At `3db3a3a` the checker answers **1164 ok · 0 drifted ·
0 broken**, because the fix pass added rows R4 and R5 to the branch's ledger
fragment, and the branch now carries seven new units rather than four — the
fix pass added `test_the_failure_names_the_fourth_exit`,
`test_one_commit_between_reads_as_one_commit` and
`test_a_tree_behind_the_reviewed_commit_gets_neither_false_reading`.

A record-located finding, so `docs/review-chain-spec.md` §*A finding located
in a record is a correction, not a round* makes it a correction: ⬜, no fix
pass owed, and `Needs a fix` does not count it. Why it is worth a line at all:
that sentence is the one a reader uses to judge what was verified, and the
same commit range edited `overview.md` two paragraphs lower without touching
it.

### ⬜ 7 — `survivors.md`'s first quote occurs four times in the file it anchors into

`seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md:7`.
Established by **execution** for the survivor itself, by **reading** for the
hazard.

Both rows are correct judgments, and I reproduced the survivors they are
about. `survivor-check --range b88a0b2..1468e48` reports exactly two places,
`skills/code-review/scripts/chain_check.py:2789` and `:2911`, sharing the two
phrases the rows name. Reading both: the first is the grandfathering notice of
the check that refuses a missing `Loses a record or crashes` row, whose own
message already spells both cell values and says they are copied from the
reviewer's line of the same name; the second is the reopening bound's second
walk, whose message ends in `CAPPED_EXIT`. Neither belongs to the class round
1's finding named — a refusal that names no exit its reader can take — so
neither is a fix that was skipped.

The hazard is in the anchor rather than the judgment. `survivors.md`'s own
header says *the quote is the anchor*, and `survivor_check.exempted` matches a
row when the quote's words appear as a contiguous run in the candidate's. The
first row's quote — *grandfathering `Fixes checked by` already uses* — stands
in four places in `chain_check.py`, one of which is `written_late`'s own
grandfathering branch. If a later round corrects the wording of one of the
other three and this one survives, this row exempts it with grounds that
describe a different check.

It is bounded: a `survivors.md` lives until the release that ships it, and an
exempted survivor is still printed with its grounds, so a reader sees the
mismatch rather than silence. Recorded so the next round does not re-derive
it, and not raised as something to fix.

### ❓ 8 — the fix pass's hand-edit exit is true and no case holds it

`skills/code-review/scripts/chain_check.py#written_late`. Established by
**execution**.

The new refusal tells a reader that the `Written late` row *may be added by
hand and committed like any other correction to a record already on the
branch*. I checked that this is true rather than reassuring: on a scratch
repository, the late record was refused at exit 1, the row was added by hand
to the end of its field table and committed, and the same check then exited 0
and printed the notice quoting the reason. `written_late_reason` reads through
`read_record`, which is `git show HEAD:<rel>`, so the hand-edit is read
wherever the flag's row would be.

The question is for the repository owner, not a defect: the flag route is
pinned by `test_a_late_record_that_says_why_prints_instead_of_failing`, and
the hand-edit route the message now advertises is pinned by nothing. Nothing
in this branch made that route newer or more fragile — it has always followed
from reading HEAD — so `agent-contract` §14 is satisfied by the case that
pins the message. Whether the advertised route earns a case of its own is a
judgment about how much a message may promise, and the answerer is the
repository owner.

## Checked and found clean

Axes this round opened, measured, and closed with nothing to fix. They carry
no finding number because they are not findings.

| What was checked | Location | Grounds |
|---|---|---|
| 🟡 1's fix ships a case, and the case dies alone | `tests/test_a_record_precedes_the_fixes_it_commissions.py#test_the_failure_names_the_fourth_exit` | executed — the appended text removed from a copied tree: 1 failed, 50 passed, and the one failure is that case. `test_the_failure_says_what_to_do_instead` stays green, so the old advice is still pinned beside the new exit |
| 🟡 2's case pins the BEHIND state rather than the sideways one | `tests/test_new_says_when_head_is_not_the_target.py#test_a_tree_behind_the_reviewed_commit_gets_neither_false_reading` | executed — the case detaches HEAD onto an ancestor. A separate probe put HEAD on a branch that diverged sideways: it still gets the listing line and both readings, which is the state `head_moved`'s docstring always covered. Removing the new branch fails that case and nothing else |
| ⬜ 3's verb arm is exercised, and the negative assertion is sound | `skills/code-review/scripts/round_record.py#head_moved_line` | executed — reverting the verb arm alone fails `test_one_commit_between_reads_as_one_commit` and the behind case, 2 of 8. The line reads *1 commit stands between them*, which does not contain the string the case forbids |
| ⬜ 5's guard skips nothing but the subprocess | `skills/code-review/scripts/chain_check.py#written_late` | read — `began` and `said` are used only inside the loop over `late.items()`, which is empty on the guarded path, and nothing else stands between the guard and the loop. executed — inverting the guard to `if late` fails 16 cases across the two modules that read the check |
| ⬜ 5's twelve-line comment survived the paste | `skills/code-review/scripts/chain_check.py#written_late` | read — the comment beginning *The fourth exit. Until this row* stands above `said = written_late_reason(...)`, and the guard was inserted above `began = item_began(rel)` rather than over it |
| the refusal a late record meets lets a reader act without opening another file | `skills/code-review/scripts/chain_check.py#written_late` | executed — captured verbatim from a scratch repository. It names the row, its cell shape, the flag that writes it, the hand-edit route, and why a bare `yes` buys nothing |
| the line a tree behind the reviewed commit meets offers no false reading | `skills/code-review/scripts/round_record.py#head_moved_line` | executed — captured verbatim: it names both commits, says HEAD reaches no commit the round did not, says what to check instead, and ends *Nothing is refused here, and the record is written*. Exit 0 and the record exists on disk |
| the two survivors `survivor-check` reported are real and their grounds hold | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md` | executed — reproduced over `b88a0b2..1468e48` at exit 1; both messages read at their coordinates. ⬜ 7 below is about the anchor, not the judgment |
| the four re-stamped `seal/ledger.md` rows each carry a dated re-read note | `seal/ledger.md` | read — every one of the four changed rows reads `Checked` 2026-09-13 and carries **Re-read 2026-09-13 by work item 1789296200 (#345), which drifted it** followed by what moved and why the claim still holds. executed — `evidence-check .` exit 0 at 1164 ok · 0 drifted · 0 broken |
| the branch's two new ledger claims went to the fragment | `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md` | read — R4 and R5 are new rows in the branch's own fragment and `seal/ledger.md` gained none, which is what `CLAUDE.md` §*a change writes fragments, never the shared file* asks. Both cite anchors the checker resolves |
| the population sentence's 102 is the script's own number | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/phases/phase-1.md` | executed — 167 refs have a merge-base with `main` and 102 of them add a file under `seal/specs`, which is where the walk's first `continue` sits |
| the empty code span in round 1's grounds cells is not this branch's | `skills/code-review/scripts/round_record.py#fix_table` | read — `fixed at <sha> — ``;` stands 65 times across this repository's records, and the RIDER above `fix_table` names the cause, the coordinate of the repair, and the round that found it. It predates this branch |
| the new prose is inside no scan it would fail | `skills/code-review/orchestration.md`, `docs/review-chain-spec.md` | executed — 122 passed over the six further modules that read those two documents, and 110 passed over the phrase scan, the wrap check, the identifier check and the one-word check |
| a `git log` that fails is still read as an empty listing | `skills/code-review/scripts/round_record.py#head_moved` | read — `git(...) or ""` makes a failed `log` indistinguishable from an empty one, so the new line would state the BEHIND case confidently. Both `rev-parse` calls have already answered by then, so this needs a repository-level failure, and the old line was equally wrong there. Named rather than raised |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the refusal at the pull request never names the fourth exit | `skills/code-review/scripts/chain_check.py:2607` | answered | **closed.** executed — the shipped refusal captured from a scratch repository names `Written late`, `--written-late` and *added by hand*; the case dies alone when the appended text is removed; and the advertised hand-edit exit was driven end to end, exit 1 to exit 0 |
| 🟡 2 | `head_moved_line` prints *0 commits stand between them* with two readings that are both false when HEAD is behind the reviewed commit | `skills/code-review/scripts/round_record.py:1557` | answered | **closed.** executed — the state reproduced on a scratch repository now prints the BEHIND line, names both commits, offers neither false reading, exits 0 and writes the record. A sideways branch still gets the listing line, so the new branch did not swallow the case it must not |
| ⬜ 3 | *1 commit stand between them* — the singular arm is written for the noun and not the verb | `skills/code-review/scripts/round_record.py:1580` | answered | **closed.** executed — the line reads *1 commit stands between them*, and reverting the verb arm fails the case written for it |
| ⬜ 4 | the forty differing records are named in no committed file | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29` | answered | **closed, and round 1's grounds corrected rather than repeated.** executed — the rescued file is byte-identical to the measurement's output, names 40 records, and carries the five header counts; `overview.md` and `phase-1.md` point at it; and the four ref commands re-run here show the number can be retaken in this clone |
| ⬜ 5 | `written_late_reason` is called on every record whether or not anything is late | `skills/code-review/scripts/chain_check.py:2531` | answered | **closed.** read — the guard skips nothing but the subprocess; executed — inverting it fails 16 cases. The twelve-line comment the paste-ready block would have deleted is intact |
| ⬜ 6 | `overview.md`'s verified line still says `evidence-check` at 1161 ok and four new units; the branch answers 1164 and seven | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:6` | open | executed — `evidence-check .` exit 0 at 1164 ok · 0 drifted · 0 broken, and the three units the fix pass added are in the range |
| ⬜ 7 | `survivors.md`'s first quote stands in four places in the file it anchors into, one of them a different check | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md:7` | open | read — `survivor_check.exempted` matches the quote as a contiguous run of words in the candidate, and the phrase is not unique to the survivor the row judges |
| ❓ 8 | the hand-edit exit the new refusal advertises is true and no case holds it | `skills/code-review/scripts/chain_check.py#written_late` | open | executed — the route works end to end. Whether a message that promises a route owes a case for it is the repository owner's call |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py -q` | 110 passed in 28.39s — the module that was red since `72c8eb5` is green, and the new prose and the new committed measurement file pass the wrap, identifier and one-word checks |
| `bin/test tests/test_new_says_when_head_is_not_the_target.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_a_record_says_why_it_was_written_late.py -q` | 70 passed in 49.51s — round 1 measured 67 here, and the three the fix pass added are the difference |
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_review_axes.py tests/test_a_fix_pass_may_add_a_unit.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_broad_gate_rule.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py -q` | 122 passed in 41.82s — the further modules that read the two documents this range added prose to |
| `git show eb7a56a^:skills/code-review/orchestration.md`, flattened and searched | one occurrence of *spawned before* — the case was genuinely red before the rewording |
| the eleven backwards needles of the three phrase scans, over the flattened text of all four carriers at HEAD | no hits — nothing else this branch added to those documents is within reach |
| `cmp` and `shasum -a 256` between the rescued `phases/phase-1-measurement.txt` and the measurement's output in the session scratchpad | exit 0, digests equal — byte-identical |
| the rescued file's own counts | 40 record entries, 40 `Target SHA` lines, 40 *seen on* lines, header 310 / 158 / 152 / 112 / 40, the two hand-opened records at lines 121 and 115 |
| `git for-each-ref 'refs/remotes/pull/*'`, `git for-each-ref refs/remotes/pull`, `git for-each-ref 'refs/remotes/pull/*/head'` | 0, 138, 138 — the pattern in round 1's grounds is one path component short, exactly as the records now say |
| `git merge-base --is-ancestor a0f0e9a refs/remotes/pull/364/head` | exit 0 — the adding commit `phase-1.md` names first is reachable in this clone |
| the measurement's population re-enumerated by its own rule | 167 refs have a merge-base with `main`; 102 of them add a file under `seal/specs` — `phase-1.md`'s figure |
| probe: `new` with HEAD detached one commit behind the reviewed commit | the BEHIND line verbatim, both commits named, neither false reading, exit 0, record written |
| probe: `new` with HEAD on a branch that diverged sideways | *1 commit stands between them* with the listing and both readings — the new branch does not reach the state it must not |
| probe: `new` with HEAD one commit ahead | *1 commit stands between them* — the singular verb, in the commonest real case |
| probe: the late record refused, the `Written late` row then added by hand and committed, the check re-run | exit 1 then exit 0, the notice quoting the reason — the exit the new refusal advertises is real |
| mutation, copied tree at `80040fe`: `if not late` → `if late` in `written_late` | 16 failed, 46 passed — killed |
| mutation: the appended fourth-exit text removed from the refusal | 1 failed, 50 passed — `test_the_failure_names_the_fourth_exit` alone |
| mutation: the BEHIND branch removed from `head_moved_line` | 1 failed, 7 passed — `test_a_tree_behind_the_reviewed_commit_gets_neither_false_reading` alone |
| mutation: the verb arm reverted as well | 2 failed, 6 passed — the second is `test_one_commit_between_reads_as_one_commit` |
| `bin/survivor-check --range b88a0b2..80040fe`, with and without the exemption file | exit 0 both ways — 14 sentences removed, no removed wording still standing |
| `bin/survivor-check --range c7cc842...HEAD --exempt seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/survivors.md` | exit 0 — 36 sentences removed, none standing, which is what `overview.md` claims |
| `bin/survivor-check --range b88a0b2..1468e48` | exit 1, two places — `chain_check.py:2789` and `:2911`, the two rows `survivors.md` records |
| `bin/evidence-check .` | exit 0 — 1164 ok · 0 drifted · 0 broken · 0 external · 0 old-format, over `seal/ledger.md` at 1148 and the fragment at 16 |
| `bin/unverified-check seal/specs/` | exit 0 — this work item has 1 open row, the broad gate, with the orchestrator named as its answerer |
| `git status --porcelain`, `git worktree list` | tree clean at `3db3a3a`; no worktree or branch left by this round. Every probe file, the copied tree the mutations ran in, and the bytecode they cached are deleted |
| the full suite, the repository-wide lint, the typecheck | **not yet — not run, and not this round's** (`agent-contract` §2). It is the sealer's, and with nothing open it has now come due: what comes next is that agent's spawn, not a run assembled here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `new --target <a revision that is not a full SHA>` writes the revision verbatim into `Target SHA` | already deferred by the branch: `overview.md` §Not done, the docstring of `test_a_target_given_as_a_revision_is_named_by_its_sha`, and an issue on the tracker. Round 1 recorded it too | the repository owner — carried forward so a later round does not re-open it as new |
| nothing counts how often `--written-late` is reached for | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/questions.md` Q5, added by the fix pass with both options and a stated answer | the repository owner — round 1's ❓ 6, and the row reached its durable home |

## Paste-ready fixes

⬜ 6 — the two figures, in `overview.md`'s verified line. Nothing else on that
line moved.

```
`evidence-check` at 1164 ok · 0 drifted
```

```
the seven units this branch added each broken alone and each seen red
```

Needs a fix: no
Loses a record or crashes: no

Round 1's two 🟡 were text a person acts on, and both are now text that tells
them something true. Nothing this round opened leaves a record outside the
root and nothing crashes. ⬜ 6 and ⬜ 7 are corrections to the work item's own
paperwork, and ❓ 8 is a question the repository owner answers.

## Proof block

Opened and read in full: `skills/code-review/scripts/chain_check.py`
(`written_late`, `written_late_reason`, `read_record`, and the two checks the
survivors stand in — the missing-floor-row refusal and the reopening bound's
second walk), `skills/code-review/scripts/round_record.py` (`head_moved`,
`head_moved_line`, `git`, `fix_table` and the RIDER above it, and the `new`
call site that prints the line), `skills/code-review/scripts/survivor_check.py`
(`exempted` and the exemption-file documentation),
`tests/test_the_last_rounds_fixes_are_checked.py` (the three needle sets and
the cases that read them), the diff of
`tests/test_new_says_when_head_is_not_the_target.py` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, the whole of
`git diff b88a0b2..80040fe`, the four changed rows of `seal/ledger.md`,
`seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md`,
`phases/phase-1-measurement.txt`, and the work item's `overview.md`,
`phases/phase-1.md`, `questions.md`, `survivors.md`, `changelog.md`,
`rounds/round-1.md` and `rounds/round-1-report.md`.

Read but not committed anywhere: the session scratchpad, for the byte-identity
comparison and for how the measurement enumerated its population. The smith's
and the orchestrator's files are still there — the measurement scripts, the
saved generator copies, the rescued list — and whether a session scratchpad is
a `agent-contract` §7 leaving is the orchestrator's call, as round 1 also
recorded. Nothing of this round's is among them.
