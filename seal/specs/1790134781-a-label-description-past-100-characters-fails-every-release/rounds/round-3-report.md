# Review round 3 — `fix/515-a-label-description-past-100-characters-fails-every-release`

Target SHA `3ffe13a`. This is the run's last record: round 2's corrections
used the run's one reopening, so this round verifies them and ends the run
whatever it finds. Its target is the fix range `0e2935c..af590c9` (e0b6601
and af590c9, 6 files), not the branch; 3ffe13a only closes the round-2
record. It was reviewed in a `git clone --no-local` at the target, and the
clone has been deleted.

Carried from round 2 and not searched for again: the workflow's four steps,
what `roll_flow_measurement_issue.py` and `tracker_labels.py` read, and the
T2 and C2 rows. Round 2's verdicts were not carried. Each of its four open
rows is re-derived below. New units: none, and none were created by this
range (it changes a comment, two docstring sentences, and records).

How the findings relate:

```
round 2's wording finding ⑥ — "reads nothing an earlier step writes" was false
  ├ round 2's own paste-ready fix ("nothing the close step writes") was false too
  │   └ the implementer declined it and wrote a narrower sentence → true (🟢 ⑥, ⑦)
  └ the same sentence in C2's Read cell → corrected in the same words (🟢 ⑦)
round 2's record findings
  ├ ④ the changelog fragment now names the condition   (🟢)
  └ ⑤ overview.md's verified line now matches its table (🟢)
```

Nothing opened this round needs a fix.

## The new wording is true, and round 2's suggestion was not

The implementer declined round 2's paste-ready wording for ⑥ and ⑦, *"read
nothing the close step writes"*, and argued it is false. I checked that
argument against the code, and it holds.

- **What the roll reads.** `roll_flow_measurement_issue.py` `main` reads
  the version from the checked-out tree and then requires exactly one open
  `flow-measurement` issue, and exits non-zero otherwise (read).
- **What the close step can write.** `close_issues_on_release.py` closes
  every issue a constituent pull request names with a closing keyword. It
  has no exclusion for the `flow-measurement` label (read, `grep` over the
  script). So a body that wrote `Closes #<log>` would close the issue the
  roll then looks for. Round 2's suggested sentence was therefore false for
  the roll, which is the same fault ⑥ raised, one step narrower.
- **What the label step reads.** `tracker_labels.py` reads `LABELS` from
  the tree and the tracker's label list. `LABELS` declares `size: now`
  alone. The roll creates its issue with `flow-measurement` and
  `measurement`, neither of which is declared, so the roll does not depend
  on the label step either (read).

The new sentence at `.github/workflows/close-issues-on-release.yml:50-52`
says both steps *"each read the checked-out tree and the tracker, and
neither needs a step after checkout to have succeeded"*. Each half is true
of both steps. It claims dependence on checkout, which is real, and claims
no dependence on the close step or on each other having succeeded, which is
also real. The close step can change what the roll finds, but that is not a
step needing to have succeeded.

One edge is worth naming, and it is not a defect. The comment's conclusion,
*"neither may be skipped by an earlier step failing"*, covers checkout too,
while its reason only covers the steps after checkout. That matches what
`!cancelled()` does. After a failed checkout both scripts are missing, so
`python3` exits non-zero in a job that is already red, and nothing is lost.
Round 2 judged that on reading, and I re-derived it on reading (not executed
on a runner).

The same sentence appears at
`tests/test_a_declared_label_reaches_the_tracker.py:21-22` (the A14 index
entry) and `:269-270` (the case's docstring). `git grep` for the old
phrasings finds no other instance outside the round records, so the class
is closed (read). `survivor-check --range 0e2935c..HEAD` reports no removed
wording still standing (executed).

## Round 2's four rows, verified

### ④ The changelog fragment now names the condition

`seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/changelog.md:12-15`
adds, inside the existing entry, that a failed step no longer skips the
label step or the roll unless the job was cancelled. *"That workflow"* has
its antecedent in the same bullet's first line (read). The fix did not use
round 2's separate-bullet form, and one entry for one work item reads
better. *"The next refusal of any kind"* is round 2's own wording. It means a
refusal in an earlier step, since a refusal by the roll itself still costs
the roll. A reader of the released section takes it that way, so I did not
raise it.

### ⑤ overview.md's verified line matches its table

`overview.md:6` now lists both GitHub references under read and a real
runner's `!cancelled()` under unverified. That agrees with the question
table at lines 27-28 and with C1 and C2 (read).

### ⑥ The workflow comment and the case docstring say what the steps depend on

Fixed at e0b6601, judged above. The docstring edit moved C2's test anchor
hash from `1caacb02` to `e5f8d26b`, and the comment moved the label step's
anchor from `0c428cf4` to `dcdc58b4` in both T2 and C2. `evidence-check
--strict` reads both ledgers with 0 drifted (executed). The case itself was
re-run green at the target (executed). The case's assertions did not change,
so round 2's seven mutations still describe it.

### ⑦ C2's Read cell carries the narrower claim, and the reference says what C2 quotes

C2's Read cell now says both steps read what checkout wrote, that the roll
reads an issue the close step could close, and that neither needs a step
after checkout to have succeeded. It carries `Corrected 2026-09-23 in round
2's fix pass` naming the old sentence (read). C2 also now quotes GitHub's
expressions reference. I fetched its *Status check functions* section this
round, and each quotation matches it. The reference says *"A default status
check of `success()` is applied unless you include one of these
functions"*, defines `cancelled()` as *"Returns `true` if the workflow was
canceled"*, and names `if: ${{ !cancelled() }}` as *"the recommended
alternative"* to `always()` (read). C2's Clause is unchanged, and it did not
need to change.

## Carried from round 2 without re-opening

Round 2's six 🟢 rows (round 1's three closures, the widening to the label
step, the choice of `!cancelled()`, and the new case as a unit) rest on
lines this range did not touch. The two `if:` lines at `:58` and `:66` are
byte-identical to round 2's target. The case that pins them passed at this
target (executed), so those rows stand.

## Executed and read, kept apart

- **Executed**, in the clone at `3ffe13a`:
  - `bin/test tests/test_a_declared_label_reaches_the_tracker.py -k "failed_step or workflow or description"`: 4 passed, exit 0;
  - `evidence-check --strict` on this work item's fragment (8 ok, 0 drifted) and on `seal/ledger.md` (1468 ok, 0 drifted), exit 0 each;
  - `survivor-check --range 0e2935c..HEAD`: exit 0, no removed wording standing;
  - `ruff check` and `ruff format --check` on the test module: exit 0 each.
- **Read**:
  - the fix-range diff in full, and the whole workflow at the target;
  - `roll_flow_measurement_issue.py` (constants, `create_args`, `main`), `tracker_labels.py` (`LABELS`), and `close_issues_on_release.py` (`KEYWORDS`, `main`, by `grep`);
  - this work item's `changelog.md`, `overview.md`, `round-2.md` and `round-2-report.md`;
  - GitHub's expressions reference, *Status check functions*, fetched 2026-09-23.
- **Unverified**:
  - how a real runner evaluates `!cancelled()` after a failed step. Answerer: the repository owner, from the first close-issues run in which a step fails. This is already C2's Unverified cell and `overview.md`'s table row.

## Regression tests to plant

None. This range changes prose, and the case that pins the behaviour was
already seen red on each param in round 2.

## Facts for the evidence ledger

None new. C2 already carries the one fact this round re-read, the
expressions reference.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2's finding 4: the changelog fragment names the workflow condition | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/changelog.md:12-15` | answered | Verified this round. Read; one entry, antecedent in the same bullet |
| 🟢 | Round 2's finding 5: `overview.md`'s verified line matches its table | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | answered | Verified this round. Read against lines 27-28, C1 and C2 |
| 🟢 | Round 2's finding 6: the comment and the case say what the two steps depend on | `.github/workflows/close-issues-on-release.yml:50-52`, `tests/test_a_declared_label_reaches_the_tracker.py:21-22,269-270` | not a defect | Verified this round that round 2's fix at `e0b6601` holds; this round wrote nothing. The new sentence is true of both steps. Round 2's suggested sentence was false, since the close step can close the log the roll requires. `git grep` finds no other instance, and `survivor-check` exits 0 |
| 🟢 | Round 2's finding 7: C2's Read cell carries the narrower claim | `seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md` C2 | answered | Verified this round. Read, and C2's three quotations match GitHub's expressions reference as fetched this round |
| 🟢 | The comment's conclusion covers a failed checkout, and its reason covers only the steps after it | `.github/workflows/close-issues-on-release.yml:50-52` | not a defect | The conclusion states what `!cancelled()` does. After a failed checkout both scripts are missing and exit non-zero in a job already red |
| 🟢 | T2 and C2 re-stamped after the comment and docstring edits | `seal/ledger.md:2498`, C2 | not a defect | `evidence-check --strict` reads both ledgers with 0 drifted, executed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_declared_label_reaches_the_tracker.py -q -k "failed_step or workflow or description"` at `3ffe13a` | 4 passed, exit 0 |
| `evidence-check --ledger` on this work item's fragment, `--strict` | 8 ok, 0 drifted, 0 broken, exit 0 |
| `evidence-check --ledger seal/ledger.md`, `--strict` | 1468 ok, 0 drifted, 0 broken, exit 0 |
| `survivor-check --range 0e2935c..HEAD` | 346 files against 9 removed sentences, none standing, exit 0 |
| `ruff check` and `ruff format --check` on the test module | exit 0 each |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's. This round leaves nothing open, so it has come due: the next act is the sealer's spawn, once the orchestrator has written this round's record |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, in the clone at `3ffe13a` unless noted:

- `.github/workflows/close-issues-on-release.yml` (whole)
- `.github/scripts/roll_flow_measurement_issue.py` (lines 1-30, 150-200, 395-420, 455-507, the rest by `grep`)
- `.github/scripts/tracker_labels.py` (lines 80-125)
- `.github/scripts/close_issues_on_release.py` (by `grep` only)
- `tests/test_a_declared_label_reaches_the_tracker.py` (lines 1-50, 250-290, and run)
- `bin/test`, `bin/evidence-check` (headers)
- `seal/ledger.md` T2 and the C2 row, through the diff and `evidence-check`
- this work item's `changelog.md`, `overview.md` (whole), `rounds/round-2.md`, `rounds/round-2-report.md` (whole, in the user's checkout)
- GitHub's expressions reference, *Status check functions*, through WebFetch
