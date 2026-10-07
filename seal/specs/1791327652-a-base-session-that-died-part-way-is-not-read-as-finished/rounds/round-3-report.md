# Review round 3 — a base session that died part-way is not read as finished (#849)

This is the verifying round for round 2's fixes, `c339dccd..b1de5a0b`. PR
#851's head is `034fbe4c`, which adds only round 2's closed record after
`b1de5a0b`. I reviewed it in a `git clone --no-local` at `034fbe4c`, under
this round's scratchpad directory. Round 2's record, its report, the new
`survivors.md` and the overview were read for their coordinates, and every
verdict below was derived again here.

How the answers relate:

```
round 2's fixes
 ├─ 🔴 1: RAN_TO_ITS_END's comment named a three-part pytest version   -> closed
 │    └─ the comment now says every exit was measured on 6.1 and 7.0   -> ⬜ 2: exit 3 was read there, not measured
 ├─ 🔴 2: the New? bullet copied 21 words of rule 3                    -> closed
 │    └─ the changelog's sentence reworded beyond the finding          -> states rule 3's two stops; ⬜ 4 drops `--maxfail`
 ├─ ⬜ 3: "a failed collection exits 2" was said without a condition   -> closed where it said 2
 │    └─ the fix now says that under `-x` it exits 1                   -> ⬜ 1: only when another file is collected after it
 │    └─ the overview still carries the old sentence                   -> ⬜ 3: a correction to the paperwork
 └─ survivors.md's eight rows                                          -> each true
```

None of the four ⬜ changes a word the gate prints. Each is a sentence that
says more than was measured, and the gate's reading stays right in every case
I could construct.

## Round 2's verdicts, answered

**🔴 1 is closed.** `skills/verify/scripts/broad_gate.py:1940` now names
"pytest 6.1, 7.0 and 9.1", each in two components. Executed in the clone:
`tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one`
passes.

**🔴 2 is closed.** The **New?** bullet at `skills/verify/SKILL.md:517` is the
round-2 report's paste-ready text word for word, and its pin in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it` moved with it.
Executed in the clone: the whole of
`tests/test_no_passage_is_pasted_into_a_second_file.py` passes, and so do both
pins. I also measured the runs with that module's own `longest_run`:

| Pair | at `c339dccd` | at `b1de5a0b` |
|---|---|---|
| `skills/verify/SKILL.md` and `templates/config.md` | 21 words | none of 15 |
| the changelog fragment and `templates/config.md` | 20 words | none of 15 |
| the changelog fragment and `skills/verify/SKILL.md` | none of 15 | none of 15 |

The module does not read `seal/`, so the changelog's 20-word run never failed
a case. The smith reworded it anyway, and the fix table's claim that the three
share no 15-word run holds.

**⬜ 3 is closed for what it said, and the narrowing goes one step too far.**
Each of the four places round 2 named now ties exit 2 to a failed collection
without `-x`, and that is true. Two of them now say more. The comment and the
case docstring say that under `-x` a failed collection exits 1. That holds
only when pytest starts another collector after the failing one. ⬜ 1 below
covers it.

## Under `-x`, a failed collection in the last file still exits 2 (⬜ 1)

pytest counts a failed collection in its collect-report hook. Under `-x` that
count sets `shouldfail`, but `Failed` is raised only at the start of the
*next* collection. If the failing file is the last one collected, nothing
starts after it. The run loop then sees the count and raises `Interrupted`,
which is exit 2.

Executed on pytest 9.1.1, two files, one of which cannot import:

| Order | `-x` | `--maxfail=1` | `--maxfail=2` | nothing |
|---|---|---|---|---|
| the broken file collected first | 1 | 1 | 2 | 2 |
| the broken file collected last | 2 | 2 | 2 | 2 |

Round 2 measured the first shape only. So these sentences overstate it:

- `skills/verify/scripts/broad_gate.py:1932` gives exit 2 to "a failed
  collection without `-x` or `--continue-on-collection-errors`".
- `skills/verify/scripts/broad_gate.py:1944` lists "a failed collection under
  `-x`" among the stops that exit 1.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py:4308`, the docstring of
  `test_a_keyed_session_whose_end_shows_a_stop_is_counted_unended`, says
  "under `-x` a failed collection gives 1".

The gate's word is right in both shapes. Exit 2 counts the session as stopped
part-way, so `new` reads `new?`, which is the strict side. Exit 1 is the case
round 2 already judged harmless. That is why this is ⬜ and not 🟡. Rule 3,
U3 and the changelog say only that a failed collection without `-x` exits 2,
which stays true, so they need nothing.

## The comment claims a measurement that was a reading (⬜ 2)

`skills/verify/scripts/broad_gate.py:1940` now says "Each exit above was
measured with the recorder loaded on pytest 6.1, 7.0 and 9.1". Round 2's ten
stops gave 0, 1, 2, 4 and 5 on all three builds. They did not include exit 3.
Round 2 read exit 3 in the session wrapper of 6.1.0 and 7.0.0, and its report
labels that as read. Exit 3 was measured on 9.1.1 alone, by round 1's fix
pass. The comment blurs the line between executed and read that the contract
keeps separate (§4). The value is right, so the comment needs one clause and
nothing else.

## survivors.md's eight rows

Executed: `survivor-check --range c339dccd..359badfc` names exactly eight
places, and they are the eight rows. Run over the whole fix range with
`--exempt` pointing at `survivors.md`, it excuses all eight and exits 0.

Read, each against the text at `034fbe4c`:

| Row | True? | Why |
|---|---|---|
| `templates/config.md`, the two named stops | yes | it is rule 3's own sentence, and the changelog no longer repeats it (measured above) |
| `templates/config.md`, the stopped-session sentence | yes | rule 3's own sentence, and the bullet no longer copies it |
| the test module's two pins | yes | each pins rule 3's text and has to carry it; both pass |
| the ledger's U3, the two stops | yes | U3 names both stops, `--maxfail` included, as rule 3 does |
| the ledger's U3, the stopped-session claim | yes | U3 quotes rule 3, including its new "without `-x`" |
| `base_word`'s docstring in `broad_gate.py` | yes | it names `UNENDED_AT_BASE` for a session with no `end` line or a stopping exit, and makes no claim about collection |
| `overview.md`'s *Not done* | yes | it names the two stops in rule 3 and in the comment, both still there |

The file's lead also holds. It says two sentences were removed, and the
removed sentences behind all eight survivors are the bullet's and the
changelog's. The 20-word run it gives for the changelog is the measured one.

## The changelog sentence the smith reworded

Rule 3 says: "Two stops are named rather than closed: a test that calls
`pytest.exit` with a return code of 0, 1 or 5 chooses one of the three, and a
run without xdist that `-x` or `--maxfail` stops exits 1, which leaves no file
partly run only while each file's tests run together."

The changelog now says: "Two stops still pass as a finished session, and are
named: a `pytest.exit` in a test that picks 0, 1 or 5 as its return code, and
a run without xdist that `-x` stops while its order mixes files."

- **The same** — the first stop. "Picks 0, 1 or 5" is rule 3's "chooses one of
  the three", and "still pass as a finished session" is what choosing one of
  the three means for `RAN_TO_ITS_END`.
- **The same** — the second stop's harm. "While its order mixes files" is the
  converse of rule 3's "leaves no file partly run only while each file's tests
  run together".
- **Narrower** — `--maxfail` is missing. The sentence before the rewording
  missed it too, so the rewording did not introduce this. It is still the one
  place where the release note says less than the rule, and the fix costs two
  words (⬜ 4).

## The overview still says what ⬜ 3 corrected (⬜ 3)

`overview.md:19` still says pytest writes exit 2 for "a failed collection",
with no condition, and that "every exit was measured … on pytest 9.1.1".
`overview.md:32` leaves to round 2 a question round 2 answered: whether the
exits hold on a pytest older than 9.1.1. The fix pass did not touch the
overview. These lines are paperwork under `seal/specs/`, so this is a
correction and not a fix.

## CI on PR #851 at `034fbe4c`

Read with `gh pr checks 851` at 00:23 UTC and again at 00:33 UTC, after the
`tests` run (37551387092) completed. All eleven checks pass at `034fbe4c`:

| Workflow | State |
|---|---|
| `lint` | pass |
| `ledger` | pass |
| `release` (the `hygiene` run, 37551387143) | pass |
| `arm-check-grammar (3.13)` | pass |
| `arm-check-grammar (3.14)` | pass |
| `pytest (ubuntu-latest, 3.12)` | pass |
| `pytest (macos-latest, 3.12)` | pass |
| `pytest (windows-latest, 3.12)`, groups 1, 2, 3 and 4 | pass, each |

Ubuntu and Windows group 2 were the jobs that failed at `5d21ccd9`, and both
now pass. macOS was still pending at round 2, and it passes here. None is red,
missing or pending.

## Regression tests to plant

None. ⬜ 1 and ⬜ 2 are prose in a comment and a docstring, and nothing reads
either.

## Facts for the evidence ledger

- U1's Executed cell can add the following. On pytest 9.1.1, a failed
  collection under `-x` or `--maxfail=1` exits 1 only where another file is
  collected after it, and 2 where it is the last. A failed collection under
  `--maxfail=2` with one error exits 2. Measured by #849 round 3.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The comment and one case's docstring say that under `-x` a failed collection exits 1; when the failing file is the last collected, it exits 2 | `skills/verify/scripts/broad_gate.py:1944` | open | executed on pytest 9.1.1: 1 with the broken file first, 2 with it last, under `-x` and `--maxfail=1`; read: pytest raises `Failed` only at the next collection's start; the gate's word is right in both, so no defect ships; also at `broad_gate.py:1932` and `tests/test_the_seal_is_taken_once_by_the_sealer.py:4308` |
| ⬜ 2 | The comment says each exit was measured on pytest 6.1, 7.0 and 9.1; exit 3 was read there, not measured | `skills/verify/scripts/broad_gate.py:1940` | open | read: round 2's ten stops gave 0, 1, 2, 4 and 5 and no 3; its report labels exit 3 on 6.1.0 and 7.0.0 as read; the value is right |
| ⬜ 3 | The overview still gives exit 2 to every failed collection, says the exits were measured on 9.1.1 alone, and leaves round 2 a question it answered | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/overview.md:19` | open | read: rows 19 and 32 unchanged by the fix pass; a correction to the paperwork, outside `Needs a fix` |
| ⬜ 4 | The changelog's reworded sentence names `-x` but not `--maxfail` for the second stop, which rule 3 names | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/changelog.md:18` | open | read against rule 3; the sentence before the rewording missed it too; a correction to the paperwork, outside `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed — no three-part pytest version in `RAN_TO_ITS_END`'s comment | `skills/verify/scripts/broad_gate.py:1940` | confirmed | executed in the clone: the version-timer case passes |
| 🟢 | round 2's blocking finding 2 is closed — the **New?** bullet shares no 15-word run with rule 3, and its pin moved | `skills/verify/SKILL.md:517` | confirmed | executed in the clone: the pasted-passage module and both pins pass; `longest_run` gives 21 words before and none of 15 after |
| 🟢 | round 2's finding 3 is closed where it said exit 2 — every place it named ties exit 2 to a collection without `-x` | `skills/verify/scripts/broad_gate.py:1932` | confirmed | read at `034fbe4c`; what the narrowing now adds about `-x` is ⬜ 1 |
| 🟢 | survivors.md's eight rows are each true, and survivor-check excuses exactly those eight | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/survivors.md:21` | confirmed | executed: `survivor-check` over `c339dccd..359badfc` names eight places, and with `--exempt` over `c339dccd..b1de5a0b` excuses all eight and exits 0; read: each quote against its file |
| 🟢 | The changelog's reworded sentence states rule 3's two stops | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/changelog.md:18` | confirmed | read against rule 3; shares no 15-word run with it (`longest_run`, executed); the missing `--maxfail` is ⬜ 4 |
| 🟢 | round 2's open CI question is answered — every workflow of PR #851 passes at `034fbe4c`, macOS included | PR #851 | confirmed | read: `gh pr checks 851` at 00:33 UTC, eleven checks pass; `tests` run 37551387092 completed with all ten jobs succeeding |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on `tests/test_no_passage_is_pasted_into_a_second_file.py`, the version-timer case and the two pins, in the clone at `034fbe4c` | 11 passed, exit 0 |
| `survivor-check --range c339dccd..359badfc` in the clone | exit 1, eight places, the eight rows of `survivors.md` |
| `survivor-check --range c339dccd..b1de5a0b --exempt` pointing at `survivors.md` | exit 0, all eight excused |
| The pasted-passage module's `longest_run` over SKILL.md, rule 3's file and the changelog fragment, at `c339dccd` and `b1de5a0b` | 21 and 20 words before; none of 15 after |
| A probe run once and deleted: two files, one that cannot import, on pytest 9.1.1, with `-x`, `--maxfail=1`, `--maxfail=2` and nothing | broken file first: 1, 1, 2, 2; broken file last: 2, 2, 2, 2 |
| `gh pr checks 851` at 00:23 and 00:33 UTC, and `gh run view` of run 37551387092 once it completed | at 00:33: all eleven pass; the ten `tests` jobs succeeded, the last (macOS) at 00:33:39 |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: this round did not run it. It is the sealer's, once, after the rounds settle |

## Paste-ready fixes

### ⬜ 1

```python
#   2 INTERRUPTED -- a `KeyboardInterrupt` or `pytest.exit()` in a test, a
#     failed collection without `--continue-on-collection-errors` (no test
#     runs) that `-x` or `--maxfail` did not stop at the next collection, a
#     failed collection in the last file collected among them, xdist under
#     `-x` or `--maxfail`, and a plugin that sets `shouldstop`. Stopped
#     part-way, and still writes its `end` line.
```

```python
# without xdist that `-x` or `--maxfail` stops exits 1, a failed collection
# under `-x` with another file collected after it among them. That one leaves
# no file partly run while each file's tests run together: it stops in the
```

```python
    """#849 round 1's 🟡 1, at `read_record`. pytest writes an `end` line for
    a session it stopped itself: a `KeyboardInterrupt` or `pytest.exit()` in
    a test, a failed collection and xdist under `-x` give 2 (a failed
    collection under `-x` gives 1 where another file is collected after it),
    a run loop that raised gives 3, an argument refused after the session
    started gives 4.
```

### ⬜ 2

```python
# exit of a session that ran to its end. Each exit above was measured with
# the recorder loaded on pytest 9.1, and every one but 3 on 6.1 and 7.0,
# where 3 was read in pytest's session wrapper (#849 round 2). Two stops
```

### ⬜ 4

```markdown
  its return code, and a run without xdist that `-x` or `--maxfail` stops
  while its order mixes files.
```

Needs a fix: no
Loses a record or crashes: no

Nothing in this round needs a fix. The four ⬜ are sentences that say more
than was measured, and two of them are paperwork. So the broad gate has come
due. What comes due is the sealer's spawn, once, at `034fbe4c` or at whatever
commit the ⬜ land on if the smith takes them.

## Proof block

Files opened in this round:

- `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/rounds/round-2.md`, `rounds/round-2-report.md`, `survivors.md`, `overview.md`, `changelog.md`
- `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md` (U1 to U4)
- the fix diff `c339dccd..b1de5a0b` whole, and `b1de5a0b..034fbe4c`
- `skills/verify/scripts/broad_gate.py` (`RAN_TO_ITS_END`'s comment, `base_word`'s docstring), `skills/verify/SKILL.md` (the **New?** bullet), `templates/config.md` (rule 3)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the docstring at 4308, the two pins), `tests/test_no_passage_is_pasted_into_a_second_file.py` (its helpers)
- `skills/code-review/orchestration.md` (§*A fix of a fix twice sends the work item back to its framer*), `docs/round-record-spec.md` (§*A fix of a fix*)
- pytest 9.1.1's `_pytest/main.py` (the run loop, the collect-report counter, the collection-start check)
- CI: `gh pr checks 851`, `gh run view` of the runs at `034fbe4c`
