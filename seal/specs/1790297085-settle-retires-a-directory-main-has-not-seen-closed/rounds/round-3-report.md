# 1790297085 — review round 3 report (verifying round, after the reopening)

Target: `67fda0558d1c9df8f768fd413f65416f6c571a76`. Fix range read:
`4c7fb0b3..a20a02a3` (bc63b91d, a20a02a3), plus the record-closing commit
67fda055. The surface is that diff and the class round 2's 🟡 1 named:
sentences that place CI's question at the fork or at the merge base. Round 2's
`New units` row reads `none`; the fix range adds no Python unit. This round
ends the run whatever it finds, so nothing below commissions a fix on this
branch. Each open row names a candidate home and an answerer.

## Summary

All five of round 2's findings are closed in the code and in the documents
they named. Each pin the fix pass planted turns red when its sentence is put
back the way it was, so the pins are real.

Round 2's ❓ is answered. CI's windows-latest leg went green at 6576a226, the
first tip carrying 51564382. At b589cf91, one tip earlier, it had failed on
exactly the `chain_check.py` case that 51564382 fixed.

Four ⬜ remain, and none of them needs a fix.

- ⬜ 1 and ⬜ 2 come from round 2's ⬜ 4 fix. The fix renamed the moved-case
  heading, and three sentences still describe it by its old opening: the
  skill (⬜ 1), and the 0.14.0 D3 row and ledger M2 (⬜ 2, paperwork).
- ⬜ 3: the same fix reworded the report's summary line, and no case pins
  the new wording.
- ⬜ 4: the class search, run a second way, turned up the unverified-check
  instances of *CI compares at the fork*. They are older than this run
  (#272). Their conclusion still holds on the merge ref, and what they say
  about which commit is compared does not.

The fix pass's list of what it left standing did not reach this round. It is
not in the spawn prompt, the two commit messages, the round-2 fixes table or
the work item. So ⬜ 4 comes from this round's own search and not from
checking that list. The orchestrator holds the list and can compare the two.

## Findings

### ⬜ 1 — The skill still gives one heading for every directory kept at the base, and the moved case prints another

`skills/settle/SKILL.md` §*1. Read what is waiting*, the paragraph bc63b91d
rewrote. It says *"Once it has, the heading says so"*, and two sentences later
that a directory closed in the tree and open at that base *"is listed under
*kept until the closure reaches <base>*"*. Since bc63b91d the moved case
prints `RULE_MOVED_HEADING`, which opens *kept: the closure has not reached
<base>*. So a reader who searches the output for the heading the skill names
does not find it in the moved case. The directory is still kept and the
remedy is still printed, so behaviour is unaffected. The documents case pins
the old phrase in the skill
(`test_the_documents_say_the_closure_has_to_reach_the_base`). Any rewording
therefore has to keep that phrase and add the second heading beside it.
Round 2's ⬜ 4 note predicted this: renaming the opening *"would move the
phrase that SKILL.md and the documents case pin"*. The fix renamed only the
moved heading and left the skill naming one heading.

Found by reading.

### ⬜ 2 — Paperwork: 0.14.0 D3 and ledger M2 still describe the moved heading by its old opening

A correction, outside `Needs a fix`.

- `seal/releases/0.14.0.md` D3 ends with a re-read note from round 1's fix
  pass. It says the third heading *"comes in two wordings chosen by
  `base_heading`, both opening *kept until the closure reaches <base>*; the
  claim holds as corrected above"*. Since bc63b91d only one of the two
  wordings opens that way. The row's grounds anchor `RULE_KEPT_HEADING` and
  not the moved heading, so `evidence-check` does not drift it, and a20a02a3
  did not re-read it.
- `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md`
  M2's claim says such a directory *"is listed under *kept until the closure
  reaches <base>* … and where the base has moved the heading says to merge"*.
  The claim reads as one heading with an extra clause. a20a02a3 edited M2's
  note for *never less* and did not re-read the claim against the heading
  change. M5's re-read note in the same commit states the change correctly.

Found by reading.

### ⬜ 3 — The report's summary line was reworded, and no case pins the new wording

`skills/settle/scripts/settle.py#report`: bc63b91d changed the summary line
from *"N kept until the closure reaches <base>"* to *"N kept because the
closure has not reached <base>"*. It is a line a person reads, and
`agent-contract` §14 asks for it to be pinned in the same commit. No case in
`tests/test_settle_reads_before_it_removes.py` asserts it. The only pin on
that line is `0 to retire by the rule`. The old wording was not pinned
either (phase-2.md records only that substring). This fix changed the line,
so this fix owed the pin. The new wording is true in both the moved and the
unmoved case.

Found by reading (a grep of the test modules for the new and old wording).

### ⬜ 4 — The unverified-check documents still say CI compares at the fork; on the merge ref it compares at the base's tip

This is the class round 2's 🟡 1 belongs to, found by a second search. The
first search was for the settle wording. This one looked for the meaning in
English and Korean: *fork*, *forked*, *merge base*, *merge ref*, *where CI
asks/compares*, `갈라진`, `갈라져`, `분기`, `병합 기준`, and *CI* near `지점`
or `기준`. It covered the READMEs, `docs/`, `skills/` (prose and scripts),
`agents/`, `templates/`, `hooks/`, `CONTRIBUTING.md` and `.github/`. The
settle sentences are now all true. These are what stand, all describing
`unverified-check --baseline`:

- `.github/workflows/hygiene.yml`, the comment on the step *the unverified
  record is readable, and rows leave it closed*: *"a table with fewer rows
  than where this branch forked from the base"*. The same file's comment on
  the milestone step says the opposite of the merge ref this job checks out:
  *"`git merge-base origin/main HEAD` then answers the base tip instead of
  the fork point"*.
- `templates/hygiene.yml`, the same comment on the same step. This file
  ships to every adopting repository.
- `skills/verify/scripts/unverified_check.py`: the module docstring (*"A row
  present at the fork point and absent here was removed by THIS branch"*),
  the `merge_base` docstring (*"The merge base is the fork point"*), and the
  `--baseline` help (*"fewer rows than it did where this branch forked from
  REF"*). The `base_label` docstring in the same module says CI's merge base
  is the ref's own commit.
- `README.md` and `README.ko.md`, the `unverified-check` rows (*"the point
  where this branch forked from that ref"*, *"이 브랜치가 갈라진 지점"*).
- `docs/one-root-by-lifetime.md` (*"the fork point, never the base branch's
  moving tip (#272)"*) and its Korean edition (*"base 브랜치의 현재 끝이
  아니라 갈라진 지점"*).
- `skills/verify/SKILL.md` §`--baseline` (*"what it reads is where you forked
  from it"*). This one is true for a local run and false on CI.

This is ⬜ and not 🟡 for three reasons. On the merge ref, the base's tip is
the right commit for #272's purpose, because a sibling's squash is present in
both the base's tip and the merge ref. So every conclusion these sentences
draw holds, and only the naming of the compared commit is wrong. The
sentences predate this run. And no action a reader would take goes wrong.

Standing correctly, not findings: `docs/release-checklist.md` (it names
`git merge-base` without saying where CI asks),
`docs/the-evidence-ledger.md` §*The unverified record, and the baseline it
is read against* (*"resolved once, to a merge base"*),
`docs/commit-review-gate-spec.md` (*"asked … of the merge base"*),
`docs/the-broad-gate.md`, and `.github/scripts/release_completeness_check.py`,
which states the merge ref correctly. The settle sentences in `settle.py`
(the module docstring, the `survey`, `retire` and `main` comments and the
`RULE_BASE_HEADING` comment), `skills/settle/SKILL.md` and
`docs/the-evidence-ledger.md` each say the fork holds only until the base
moves.

Found by reading.

## Round 2's verdicts, answered

- **🟡 1 (README rows, skill), verified.** Both README rows now say CI asks
  where `--released-at` and `HEAD` meet only until `--released-at` moves
  past that commit, and that `settle` then names the merge. The skill says CI
  asks at *"the merge base of that pull request's base and its merge ref,
  which is the base's tip"*, that this is the same commit as `settle`'s only
  until `--released-at` moves past the fork, and that merging it in is what
  lets the directory go. All three are true against the moved heading and
  `base_heading`. Executed: each of the four new pins turned red when its
  sentence was put back the way round 2 found it (probe below).
- **🟡 2 (*never less*), verified.** The module docstring now states both
  directions. A closure the base took after the fork makes `settle` keep a
  directory CI would pass. A record file the base added after the fork is
  read by CI and not by `settle`, so `settle` retires a directory CI refuses.
  `main`'s comment points to that paragraph. Read against round 2's executed
  probe, which is the second direction exactly. A grep for *never less*,
  *keeps more* and *more, never* across tracked prose and code finds the
  clause only in the rounds and in two places where it is true. One is the
  moved-case test docstring, *"keeps more than it must"*, which is true of
  that case. The other is plan.md's rejected row, which limits the claim to
  *"every flow this repository uses"*. Round 2 let that row stand as the
  frame's judgment, and this round carries that.
- **⬜ 3 (paperwork, five coordinates), answered.** The changelog fragment,
  plan.md's chosen row, 0.14.0 D3's correction note, ledger M2's note and
  spec.md's first *Data & interfaces* item each drop *never less* or say
  where CI compares. Read. D3 and M2 carry a second stale clause, from the
  ⬜ 4 fix rather than from this finding, and that is ⬜ 2 of this round.
- **⬜ 4 (moved heading's opening), verified.** `RULE_MOVED_HEADING` opens
  *kept: the closure has not reached {base}*. Executed: the moved-base case
  is red with the old opening restored. The skill's wording that this
  leaves behind is ⬜ 1.
- **⬜ 5 (README row read after flattening), verified.** The case now reads
  the raw file, so `split("\n")[0]` is the row. Executed: red on either
  README row reverted. On Windows a CRLF checkout leaves a `\r` at the end
  of the row, and every assertion is `in` or `not in`, so it does not
  matter. Executed by CI: the windows-latest leg passed at this tip.
- **❓ (51564382 on windows-latest), verified.** At b589cf91 the leg failed,
  with `test_a_script_copied_alone_exits_2_and_names_what_it_misses[chain_check.py]`
  as the only failure (4675 passed). At 6576a226, the first tip carrying
  51564382, the leg passed (4683 passed, 45 skipped). Executed by CI and
  read from its logs.
- **Round 1's finding 6, carried.** Deferred to #610 in round 1. #610 is
  open.

## Regression tests to plant

- `tests/test_settle_reads_before_it_removes.py#test_the_report_does_not_promise_what_the_retirement_refuses`:
  the summary line's new wording (⬜ 3). The fence below has the assertion.
  Executed in the clone and then removed: green at 67fda055, and red with the
  line put back to its old wording.

## Facts for the evidence ledger

- On a `pull_request` checkout with no `ref:`, `unverified_check.py
  --baseline <base>` compares against the base's tip, not the fork. This is
  the same fact M2 records for settle's CI readers, and it holds for the
  unverified record's own row-count and deletion arms. Read from
  `.github/workflows/hygiene.yml` and the `base_label` docstring. Not
  executed this round.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The skill names *kept until the closure reaches <base>* as the heading for every directory kept at the base; since bc63b91d the moved case prints *kept: the closure has not reached <base>* | `skills/settle/SKILL.md#"### 1. Read what is waiting"` | open | Read. The directory is still kept and the remedy printed, so behaviour is unaffected. Capped run: candidate `deferred` to a new from-review issue the orchestrator files (with ⬜ 3), answered by the repository owner |
| ⬜ 2 | 0.14.0 D3's re-read note says both heading wordings open *kept until the closure reaches <base>*; ledger M2's claim names that heading for the moved case | `seal/releases/0.14.0.md` D3; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2 | open | Read. Paperwork correction, outside Needs a fix; the stale clause comes from round 2's ⬜ 4 fix and not from round 2's ⬜ 3 |
| ⬜ 3 | bc63b91d reworded the report's summary line and pinned nothing on it | `skills/settle/scripts/settle.py#report` | open | Read: no case asserts either wording; agent-contract §14. Capped run: candidate `deferred` to the same new issue as ⬜ 1, answered by the repository owner |
| ⬜ 4 | The unverified-check documents say CI compares at the fork; on the merge ref it compares at the base's tip | `.github/workflows/hygiene.yml` unverified step comment; `templates/hygiene.yml` same; `skills/verify/scripts/unverified_check.py` module docstring, `#merge_base`, `#main` help; `README.md` and `README.ko.md` unverified-check rows; `docs/one-root-by-lifetime.md` and `.ko.md`; `skills/verify/SKILL.md` baseline paragraph | open | Read. Predates this run (#272), and every conclusion holds on the merge ref. Capped run: candidate `deferred` to a new from-review issue, answered by the repository owner |
| 🟢 | round 2's finding 1 is closed — both README rows and the skill say CI asks at the fork only until `--released-at` moves past it, and the skill names the merge | `README.md` and `README.ko.md` settle rows; `skills/settle/SKILL.md#"### 1. Read what is waiting"` | verified | Executed: each of the four new pins red with its sentence reverted, green restored; read against `base_heading` |
| 🟢 | round 2's finding 2 is closed — settle.py says the fork and CI can disagree in either direction | `skills/settle/scripts/settle.py` module docstring; `#main` comment | verified | Read against round 2's executed probe; a grep for the clause finds it nowhere it is false |
| 🟢 | round 2's finding 3 is closed at its five coordinates | changelog fragment #602; plan.md chosen row; 0.14.0 D3; ledger M2; spec.md Data and interfaces | answered | Read; the heading clause D3 and M2 still carry is this round's ⬜ 2 |
| 🟢 | round 2's finding 4 is closed — the moved heading opens with what has not happened | `skills/settle/scripts/settle.py#RULE_MOVED_HEADING` | verified | Executed: the moved-base case red with the old opening restored |
| 🟢 | round 2's finding 5 is closed — the documents case reads the raw README row | `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | verified | Executed: red with either README row reverted |
| 🟢 | round 2's open question is closed — 51564382 turns the windows-latest leg green | `tests/test_a_script_copied_alone_exits_2.py#names_path` | verified | Executed by CI: windows failed at b589cf91 on the chain_check.py case alone, passed at 6576a226 with 4683 passed |
| carried | round 1's finding 6, seal.py and payload_meter.py copied alone | `spec.md` Scope Out | deferred #610 | already deferred in round 1; #610 is open |
| 🟢 | PR 605's tests at this tip pass on all three operating systems, windows-latest included | `tests/test_a_script_copied_alone_exits_2.py#names_path`; `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | verified | Executed by CI at 67fda055 and read from its logs: windows-latest 4683 passed, 45 skipped. The `release` check is red on `Pass` ticked beside `Fixes checked by: nobody` in round-2.md, which is the state this round's record exists to change |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_settle_reads_before_it_removes.py` and `tests/test_a_script_copied_alone_exits_2.py`, in this round's clone at 67fda055 | exit 0, 131 passed |
| Probe (one file, run once, deleted): five reversions made one at a time in the clone, each followed by the documents case and the moved-base case (`-k`) and then restored — README.md's row, README.ko.md's row, the skill's *which is the base's tip*, the skill's *merging it into this branch and running `settle` again*, and the old opening of `RULE_MOVED_HEADING` | each exit 1, `1 failed, 1 passed`; `git status --short` in the clone empty afterwards |
| Probe (one file, run once, deleted): the ⬜ 3 fence added to the report case in the clone, run with `-k does_not_promise` at 67fda055 and again with the summary line put back to its old wording, then both files restored | exit 0, `1 passed`; then exit 1, `1 failed`; `git status --short` in the clone empty afterwards |
| `./bin/evidence-check --ledger <file> .` on the work item's ledger fragment, `seal/releases/0.13.0.md` and `seal/releases/0.14.0.md`, in the clone | exit 0 on each |
| `gh pr checks 605` at 67fda055, after the tests run finished | lint, ledger and all three pytest legs pass: ubuntu 4716 passed and 12 skipped, macos 4719 passed and 9 skipped, windows 4683 passed and 45 skipped. `release` fails on `chain_check.py` refusing `Pass` ticked beside `Fixes checked by: nobody` in round-2.md |
| CI logs read for PR 605's tests workflow at b589cf91 and 6576a226, windows-latest leg | b589cf91: failure, `1 failed, 4675 passed, 45 skipped`, the failure `test_a_script_copied_alone_exits_2_and_names_what_it_misses[chain_check.py]`; 6576a226: success, `4683 passed, 45 skipped` |
| The broad gate: the full suite, lint and typecheck | not yet. That run is the sealer's, once, after the rounds settle. This round ran two modules only |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal.py` and `payload_meter.py` die with a traceback when copied alone (already deferred in round 1) | #610 | the repository owner, who holds #610 |
| ⬜ 1 and ⬜ 3: the skill names one heading for both kept-at-base cases, and the reworded summary line is unpinned | candidate: a new from-review issue the orchestrator files | the repository owner, who decides whether settle's moved-case wording is followed up; without that agreement it is rung 4, this record and the pull request body |
| ⬜ 4: the unverified-check documents say CI compares at the fork | candidate: a new from-review issue the orchestrator files | the repository owner, who owns the #272 wording across the workflow, the template, the script and the READMEs |

## Paste-ready fixes

### ⬜ 1

```markdown
tree and open at that base is listed under *kept until the closure reaches
<base>*, or, where `--released-at` has moved, *kept: the closure has not
reached <base>*, with every row open there, and `settle --retire` keeps it
and exits 1.
```

### ⬜ 2

```markdown
D3, the end of the round-1 re-read note: … and the third heading comes in two
wordings chosen by `base_heading`: *kept until the closure reaches <base>*
where the ref has not moved, and *kept: the closure has not reached <base>*
where it has (**Corrected 2026-09-25 in round 3**: this said both open *kept
until the closure reaches <base>*, which round 2's ⬜ 4 fix changed); the
claim holds as corrected above

M2, in the claim: … is listed under *kept until the closure reaches <base>*
with every row open there, or, where the base has moved, under *kept: the
closure has not reached <base>*, whose heading says to merge `--released-at`
into this branch, …
```

### ⬜ 3

In `test_the_report_does_not_promise_what_the_retirement_refuses`, after its
last assertion:

```python
    # Round 3, ⬜ 3: the summary line counts the directories kept at the base.
    assert f"1 kept because the closure has not reached {BASE}" in text, text
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round:
`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/rounds/round-2.md`,
`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/rounds/round-2-report.md`,
`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/phases/phase-2.md`
(lines 33–55), the fix diff `4c7fb0b3..a20a02a3` in full,
`skills/settle/scripts/settle.py` (lines 60–90, 440–500, 750–765,
885–900, 1020–1035, 1244–1265), `skills/settle/SKILL.md` (lines 95–130),
`tests/test_settle_reads_before_it_removes.py` (lines 765–830),
`docs/the-evidence-ledger.md` (lines 180–200, 285–305),
`docs/one-root-by-lifetime.md` (193–206) and `.ko.md` (180–195),
`docs/release-checklist.md` (14–26), `skills/verify/SKILL.md` (274–292),
`templates/hygiene.yml` (58–72), `.github/workflows/hygiene.yml` (144–160,
326–340), `skills/verify/scripts/unverified_check.py` (36–46, 945–985,
1222–1236, 1360–1376), `skills/code-review/scripts/survivor_check.py`
(918–928), `docs/the-broad-gate.md` (55–70), `docs/commit-review-gate-spec.md`
(414–432), `docs/review-chain-spec.md` (60–125, 465–545), the README rows for
`settle` and `unverified-check` in both editions, and the D3 row of
`seal/releases/0.14.0.md`.
