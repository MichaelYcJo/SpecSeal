# Review round 2 — `fix/515-a-label-description-past-100-characters-fails-every-release`

Target SHA `d02c479`. This is the run's verifying round. Its target is the
fix range `24f8a92..a6bdf34` (59d067e and a6bdf34), not the branch; d02c479
only closes the round-1 record. It was reviewed in a `git clone --no-local`
at the target, and the clone has been deleted.

Coordinates carried from round 1 and not searched for again: the workflow's
three steps, the two scripts the label step and the roll run, and
`seal/ledger.md` T2. Round 1's verdicts were not carried. Each one was
re-derived below.

How the findings relate:

```
round 1's three verdicts                       → all three are closed (🟢 rows)
  └ finding 1's fix was widened to the label step → sound, and the condition is the right one (🟢)
      └ the widening's own sentence, "reads nothing an earlier step writes"
          ├ ⑥ the workflow comment says it, and checkout is an earlier step    (⬜)
          └ ⑦ C2's Read cell says it too                                        (⬜ correction)
the fix pass updated the records for round 1's condition, but not all of them
  ├ ④ the changelog fragment still gives the description as the only repair   (⬜ correction)
  └ ⑤ overview.md's verified line still calls the cap unverified              (⬜ correction)
```

Nothing here needs a fix. Every finding is ⬜, and four of them are about
the run's own paperwork.

## Round 1's verdicts, verified

### Finding 1 is closed: the roll no longer waits on the label step

The account says the roll step now carries `if: ${{ !cancelled() }}`. The
code at `.github/workflows/close-issues-on-release.yml:65` has that line.
PyYAML parses the workflow and gives the two steps `'${{ !cancelled() }}'`
and the first two steps no `if` (executed). GitHub's expressions reference
reads, of the default, *"A default status check of `success()` is applied
unless you include one of these functions"*. It defines `cancelled()` as
*"Returns `true` if the workflow was canceled."* So after a failed step,
`!cancelled()` is true and the step runs (read, at
`docs.github.com/en/actions/reference/workflows-and-actions/expressions`).
How a real runner evaluates it stays unexecuted. The first close-issues run
in which a step fails answers that, and the repository owner reads its log.

### The widening to the label step is right, and so is `!cancelled()`

The implementer also put the condition on the label step. So a failed close
step no longer skips the label reconcile. I judged that on its own merits:

- **What the label step reads.** `tracker_labels.py --apply` reads the
  declared labels from the tree and the tracker's label list. The close step
  closes issues and removes `size: now` from each one it closes. Neither
  step's write is the other's input (read).
- **What running it after a failed close costs.** The reconcile creates only
  labels that are missing. It is idempotent, and its own docstring says *"It
  is not a gate and must not become one."* A failed close skipping it was
  the same coupling as finding 1, one step up. So this is §12 applied, not
  scope creep.
- **What a failed checkout now does.** Both steps now also run after
  `actions/checkout` fails. Each then exits non-zero because its script is
  missing. The job was red already, so this adds two red steps and loses
  nothing (read; not executed on a runner).

On the condition itself:

- `always()` would also run after a cancel, and the reference warns against
  it for anything that needs sources: *"otherwise the workflow may hang until
  it times out."* It is the wrong choice here.
- `success() || failure()` means the same as `!cancelled()` at a step. The
  new case refuses it (executed, below). That pins one form out of two that
  are equal, which is what a case pinning text is for, so I did not raise
  it.

### Finding 2 is closed: the index and the §15 paragraph name the new cases

`tests/test_a_declared_label_reaches_the_tracker.py:18-21` lists A13 and A14.
The §15 paragraph at lines 34-43 now scopes `1790076050` to A9-A12, says
that directory was retired, and sends A13 and A14 to ledger rows C1 and C2.
I checked the retirement claim. `git log` over that directory ends at
f2943c0, *"the second fold retires them into docs (#514)"* (read).

### Finding 3 is closed: overview.md counts four mutations

`overview.md:6` says *"four single-unit mutations (one of them run twice…)"*,
and C1 lists four (read). The *run twice* part is the implementer's claim
alone. Nothing in the tree records the first try, and it changes no count.

## The new unit, judged as code

`test_a_failed_step_cannot_skip_the_independent_steps_after_it` splits the
workflow at six-space `- ` items. It requires exactly one chunk starting
`name: <step>\n`, and it looks for the exact `if:` line at eight spaces
inside that chunk. I mutated the workflow seven ways in the clone and ran
the case each time (executed):

| Mutation | Case result |
|---|---|
| both conditions removed | both params red |
| the label step's condition removed | the label param alone red |
| the roll's condition removed | the roll param alone red |
| the roll's condition turned into `always()` | the roll param alone red |
| the label step's condition turned into `success() \|\| failure()` | the label param alone red |
| the roll's condition moved below its `env:` block | green (same meaning, and correctly accepted) |
| the roll's condition commented out | the roll param alone red |

So the case pins what it claims, and each param fails on its own. The
implementer's account of its red runs matches what I saw. I found no defect
in it.

## Findings

### ④ ⬜ correction — the changelog fragment still gives the description as the only repair

`seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/changelog.md:1-12`.

**What is wrong.** Round 1's fix changed what the workflow does. A failed
step no longer skips the label step or the roll. The fragment was not
touched in the fix range (`git log` over it ends at a479a38). It still
describes the skipped roll only as a result of the over-long description.
a6bdf34's own subject is *"the label cap's records carry round 1's
condition"*. The overview and the ledger carry it, and the changelog does
not.

**Why it matters.** At the release, `gather_changelog.py` turns this
fragment into the released section. A reader of `CHANGELOG.md` would then
learn that one string was shortened, and not that the next refusal of any
kind no longer costs the roll. That second half is the one that outlives
this string.

### ⑤ ⬜ correction — overview.md's verified line still calls the cap unverified

`seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6`.

**What is wrong.** The `verified` line ends *"unverified — the cap's value
on GitHub's side, the live tracker, the broad gate"*. a6bdf34 marked the cap
✅ read in the same file's question table and moved it to **Read** in C1. It
also added the runner's evaluation of `!cancelled()` to that table, and the
verified line does not list it. a6bdf34 edited this very line, so it is
inside the fix surface.

**Why it matters.** Nothing behaves differently. A reader of the overview
header gets the opposite state for the cap from the table twenty lines
below it.

### ⑥ ⬜ The workflow comment and the new case say the two steps read nothing an earlier step writes

`.github/workflows/close-issues-on-release.yml:50-51`, and the same sentence
at `tests/test_a_declared_label_reaches_the_tracker.py:21` (the A14 index
entry) and `:268` (the new case's docstring). `git grep` finds no other
instance outside the round records (read).

**What is wrong.** *"This step and the roll below read nothing an earlier
step writes"*. Both read the tree that `actions/checkout`, an earlier step,
wrote. The roll also reads the one open `flow-measurement` issue, and the
close step closes every issue a constituent pull request claimed. That
would include the log if a body ever wrote `Closes` for it (read). The
sentence means the close step, and it says every earlier step.

**Why it matters.** It is a justification for the condition, so it is the
sentence a later edit reasons from. The behaviour is right either way. A
failed checkout makes both steps fail loudly, and a closed log makes the
roll fail loudly, which is what it did before this fix. So this is ⬜, and
it ships no defect.

### ⑦ ⬜ correction — C2's Read cell carries the same sentence

`seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md`,
row C2, **Read** cell: *"nothing either reads is written by a step before
it"*. This is the same overstatement as ⑥, in the ledger. The claim in C2's
Clause is unaffected.

## Executed and read, kept apart

- **Executed**:
  - the new case and the workflow cases in its module, at the target: 3 passed;
  - the seven workflow mutations above, one case run each;
  - PyYAML over the workflow, which parses and gives the two `if` values;
  - `evidence-check --strict` on this work item's fragment (8 ok, 0 drifted) and on `seal/ledger.md` (exit 0).
- **Read**:
  - the fix-range diff in full, and the whole workflow at the target;
  - the heads of `roll_flow_measurement_issue.py` and `close_issues_on_release.py`;
  - round 1's record and report, this work item's `changelog.md`, `routing.md` and `overview.md`;
  - GitHub's expressions reference, section *Status check functions*, fetched 2026-09-23.
- **Unverified**:
  - how a real runner evaluates `!cancelled()` after a failed step. Answerer: the repository owner, from the first close-issues run in which a step fails.
- **The broad gate**: not run. See the probes table.

## Regression tests to plant

None. The new case already pins the condition, and each of its params was
seen red on its own this round.

## Facts for the evidence ledger

- C2's **Unverified** cell can gain a **Read** half. GitHub's expressions
  reference says *"A default status check of `success()` is applied unless
  you include one of these functions"*, and defines `cancelled()` as
  *"Returns `true` if the workflow was canceled."* What a runner actually
  does stays unverified.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's finding 1: the roll step carries `if: ${{ !cancelled() }}` | `.github/workflows/close-issues-on-release.yml:65` | fixed `59d067e` | Verified this round. PyYAML reads the condition on the step, and the case goes red with it removed, on its own param |
| 🟢 | Round 1's finding 2: the module index and §15 paragraph name A13 and A14 and send them to C1 and C2 | `tests/test_a_declared_label_reaches_the_tracker.py:18-43` | fixed `59d067e` | Verified this round. Read, and the retirement claim is checked against f2943c0 |
| 🟢 | Round 1's finding 3: `overview.md` counts four mutations | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | answered | Verified this round. Read, and it matches C1's four |
| 🟢 | The fix was widened to the label step, so a failed close no longer skips the reconcile | `.github/workflows/close-issues-on-release.yml:57` | not a defect | The reconcile is idempotent and reads nothing the close writes. After a failed checkout it fails loudly on a missing script, in a job already red |
| 🟢 | `!cancelled()` rather than `always()` or `success() \|\| failure()` | `.github/workflows/close-issues-on-release.yml:57,65` | not a defect | `always()` also runs after a cancel, and GitHub's reference warns against it. The third is equal at a step, and the case pins one form |
| 🟢 | New unit `test_a_failed_step_cannot_skip_the_independent_steps_after_it` | `tests/test_a_declared_label_reaches_the_tracker.py:258-276` | not a defect | Seven mutations, executed. Each param goes red on its own, and a moved but equal condition stays green |
| 4 | ⬜ correction: the changelog fragment does not carry round 1's condition, so the released entry would name the description as the only repair | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/changelog.md:1-12` | open | Read. No commit in the fix range touches it, and a6bdf34's subject claims the records carry the condition |
| 5 | ⬜ correction: the verified line still lists the cap as unverified and omits the `!cancelled()` item | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | open | Read. The same file's table marks the cap ✅ read, and C1 says Read |
| 6 | ⬜ The comment and the new case say the two steps read nothing an earlier step writes, and both read checkout's tree | `.github/workflows/close-issues-on-release.yml:50-51`, `tests/test_a_declared_label_reaches_the_tracker.py:21,268` | open | Read, `git grep`. Behaviour is right. The sentence means the close step and says every earlier step |
| 7 | ⬜ correction: C2's Read cell carries the same overstatement | `seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md` C2 | open | Read. C2's Clause is unaffected |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_declared_label_reaches_the_tracker.py -k "failed_step or workflow"` at `d02c479` | 3 passed, exit 0 |
| A probe script (test_tmp prefix) that mutated the workflow seven ways and ran the new case after each, then restored the file | see the mutation table: each removal or changed form reds its own param alone; the condition moved below `env:` stays green; file restored, probe deleted, clone deleted |
| PyYAML (through `uv run --with pyyaml`) over the workflow | parses, exit 0; the label step and the roll carry `${{ !cancelled() }}`, and checkout and close carry none |
| `evidence-check --strict` on this work item's ledger fragment | 8 ok, 0 drifted, 0 broken, exit 0 |
| `evidence-check --strict` on `seal/ledger.md` | exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and with this round opening nothing that needs a fix it has come due: the next act is the sealer's spawn, once the orchestrator has written this round's record and applied the corrections |

## Paste-ready fixes

Finding 4, `changelog.md`, a paragraph after the existing entry's
parenthesis (the fragment's own `### Fixed` list):

```markdown
- A failed step in the close-issues workflow no longer skips the steps
  behind it that do not depend on it: the label step and the
  flow-measurement roll now run unless the job was cancelled, so the next
  refusal of any kind costs a red job and not a release's roll.
  (`1790134781-a-label-description-past-100-characters-fails-every-release`,
  #515)
```

Finding 5, the tail of `overview.md:6`, replacing from `read —` to the end
of the line:

```markdown
read — the specifying section, the scripts, #515, and GitHub's REST reference for *Create a label* for the cap's value; unverified — how a real runner evaluates `!cancelled()` after a failed step, the live tracker, the broad gate
```

Finding 6, `.github/workflows/close-issues-on-release.yml:50-51`, the first
two lines of the comment:

```yaml
      # This step and the roll below read nothing the close step writes, so
      # neither may be skipped by an earlier step failing: #515's over-long
```

And the same finding in the test module, line 21 of the index and line 268
of the docstring. The docstring sits inside C2's anchored unit, so this edit
moves C2's hash, and `evidence-check --reverify` follows it:

```python
       failed, because neither reads what the close step writes (#515)
```
```python
    it succeeded. Neither step reads what the close step writes, so a failure
```

Finding 7, C2's Read cell in the ledger fragment, the clause after the
second colon:

```markdown
nothing either reads is written by the close step before it
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round. Workflow, test module and ledgers at `d02c479` in
the clone, the rest in the user's checkout:

- `.github/workflows/close-issues-on-release.yml` (whole)
- `.github/scripts/roll_flow_measurement_issue.py` (lines 1-80)
- `.github/scripts/close_issues_on_release.py` (its `def` lines only)
- `tests/test_a_declared_label_reaches_the_tracker.py` (through the diff, and run)
- `tests/test_no_real_identifiers.py` (allowlist)
- `bin/test` (header)
- `seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md` and `seal/ledger.md` T2 (through the diff, and `evidence-check`)
- this work item's `rounds/round-1.md`, `rounds/round-1-report.md`, `changelog.md`, `routing.md`, `overview.md` (lines 1-8, and the rest through the diff)
- GitHub's expressions reference, *Status check functions*, through WebFetch
