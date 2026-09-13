# 1789296100-the-seal-and-ci-read-one-ledger-differently — review round 1 report

| Field | Value |
|---|---|
| Target SHA | `37f73213c0c1629140d89d86cc36107983d3401c` |
| Base | `c7cc842b937ca36a28adfcb7e436bb9c4bece995` (`origin/release/v0.11.3`) |
| Branch | `fix/354-the-seal-and-ci-read-one-ledger-differently` |
| Round | 1 — no earlier round to inherit |
| Agents spawned | none |

**No agent was spawned for this round.** Every read, grep and run below was
taken in this session (contract §6).

## How to read the grades

`🔴` blocks · `🟡` fix or justify · `⬜` correction, nothing ships wrong.
Every finding says how it was established — **read** or **executed**.

Findings whose location is a work item's own paperwork are graded `⬜` and
kept out of `Needs a fix`, per `agents/warden.md`'s paperwork rule. That rule
is written inside the verifying-round paragraph and this is a first round, so
the grading is a reading rather than a quotation — regrade 4, 5 and 7 if you
read it the other way. The substance of each is in the finding, not the grade.

## Stage one — spec compliance

`spec.md`'s S1, S2, S3, S4, S5, S6 and S7 are met; I verified S1–S3 and the
grading table by running the new module (13 passed) and S4–S5 by reading the
case against the five documents. **S8 is not met as written** and the
judgment behind that is sound — finding 4 is about where the judgment is
recorded, not about the act.

The owner's Q1 answer, (a), rests on a stated ground: *phase 1's structural
case holds the line and the gate's call site together, so the assertion
cannot go stale in silence*. **That ground holds for two of the sentence's
three limbs and not for the third.** Finding 1 is the measurement.

## Findings

### 🟡 1 · The `NOT SEALED` half of the printed sentence is held by nothing

**Established: executed.**

The notice asserts three things. Two are pinned:

- *`broad-gate` runs this same check with `--strict`* — pinned by
  `test_the_gate_still_passes_the_flag_the_notice_names`, which reads the
  gate's own ledger call.
- *drift is exit 2 there* — pinned by
  `test_the_grading_is_one_function_and_the_line_reads_its_answer`, which
  calls `exit_code` with `strict=True`.

The third — *this tree would come back NOT SEALED* — is pinned only by
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:251`, which
asserts that the string `NOT SEALED` appears **somewhere** in
`skills/verify/scripts/seal_stamp.py`. Nothing in the module reads the step
that turns a failing ledger check into that verdict:
`skills/verify/scripts/broad_gate.py:590`, the loop that collects every
failing check, and the `stamp.not_sealed(...)` call under it.

I mutated `gate()` so that the ledger check is exempt from the failure form —
`if name == LEDGER or not check.failed: continue` — which is exactly *make
the broad gate lenient*, the one change `spec.md` §Scope names as out of
bounds and therefore the one a case should catch. The module came back **13
passed**. The file was restored from bytes held in the mutating process and
`git status --porcelain` is empty.

So a later change that stops the gate refusing on drift leaves the checker
printing a false sentence on every lenient run, and the whole repository
stays green. The overview's *Not verified* table names the gate's end-to-end
run as the sealer's, which covers this branch once; it does not leave a case
behind, and a case is what the Q1 answer was taken on.

### 🟡 2 · A third trigger of the deferred silence is live in `seal/ledger.md` now

**Established: executed.**

The deferral itself is sound: the venue is an existing `seal/follow-up.md`
row about the same silence, the row names the repository owner as answerer,
and `spec.md` scoped the defect out before the build started. What the row
understates is its own urgency. It reads as a hazard a writer could walk
into; the shared ledger already carries five instances.

`ANCHOR_RE` (`skills/evidence-check/scripts/evidence_check.py:65`) accepts a
quoted locator whose inner quotes are **escaped** — `\"` — and matches
nothing when they are bare. Five coordinates in `seal/ledger.md` are written
with bare inner quotes, so each is dropped whole: the claim it anchors is
measured by nothing while the run prints `1148 ok` for that file.

```
seal/ledger.md:63   tests/test_a_rider_reaches_its_file.py#"STAMP = re.compile(r"Verified ...")"@05033bb1
seal/ledger.md:71   tests/test_what_the_reader_understands.py#"("an eval", "eval 'cd %s'; git commit -m x", "eval 'cd %s'"),"@770c7def
seal/ledger.md:81   skills/code-review/scripts/chain_check.py#"CLOSED_WORDS = {"fixed", "answered", ...}"@9750da73
seal/ledger.md:81   skills/code-review/scripts/chain_check.py#"SEPARATORS = " " + chr(0x2014) + ..."@9750da73
seal/ledger.md:143  .github/workflows/hygiene.yml#"echo "base is ${{ github.base_ref }} ..."; exit 0"@0cb0ca06
```

Measured by applying the module's own `ANCHOR_RE` to each ledger file and
comparing against every backticked coordinate-shaped token in it. The strict
count came back 1148 for `seal/ledger.md` and 5 for the new fragment — 1153,
which is exactly the total phase 4 recorded, so the method is reading what
the checker reads.

The new fragment is clean: its one minor anchor escapes its inner quotes, and
I found no unquoted minor anchor anywhere under `seal/`. The hole is only
this shape and the hash shape the row already carries.

### 🟡 3 · The `overview.md` scheduling divergence is a class, and a sibling branch of this release is red on it now

**Established: executed (the sibling branch) and read (the two coordinates).**

Phase 3 recorded that
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` was red
from the framer's own commit, because `plan.md` put the memo in phase 4. The
record treats it as this work item's scheduling mistake. It is not.

- `agents/framer.md:91` instructs the framer to write `spec.md`, `plan.md`
  and `questions.md` and **nothing else — not `overview.md`**.
- `tests/test_chain_hooks_hardening.py:1014` fails the moment a directory
  holds a `spec.md` or a `plan.md` without an `overview.md` beside it.

Those two cannot both be satisfied. Every work item framed by that agent is
red on an existing case from the framer's commit until whichever phase
happens to open the memo — which is the state contract §12 calls the class
behind the instance.

The orchestrator asked whether this reaches the other two work items of
0.11.3. It reaches one of them at its tip today: `git ls-tree` over
`feat/350-a-segments-own-wall-clock-is-in-no-column` shows
`seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/` carrying
`spec.md` and `plan.md` and no `overview.md`.
`feat/345-the-record-before-the-fix-sequence-has-no-arm` has the memo and is
clean.

The fix is not this branch's to make — `agents/framer.md` and that case are
shared surfaces and the choice between them (framer writes a stub memo, or
the case exempts a work item whose plan still has open phases) is the owner's.
What is owed here is that the class reaches a durable home with an answerer
instead of sitting in one work item's divergence table.

### ⬜ 4 · S8 says `seal/ledger.md` untouched, the branch touches it, and the divergence table does not carry it

**Established: read.**

My verdict on the act itself: **re-verification is not a violation of
`CLAUDE.md` §*a change writes fragments, never the shared file*.** The rule
forbids appending, and its removal carve-out shows it is about where a *new
claim* goes, not a freeze on the file. Leaving the seven rows drifted is not
an available alternative — `broad-gate` passes `--strict`, so drift is exit 2
and the branch would come back refused. I checked all seven: every drifted
anchor is `evidence_check.py#main` or one of the document sections this
branch edited, each row's `Checked` cell gained `2026-09-13`, and each Notes
cell gained a dated sentence saying why the claim survives. That is the
re-reading `CLAUDE.md` asks for, done and shown.

What is missing is the record of the divergence.
`spec.md` S8 reads *with `CHANGELOG.md` and `seal/ledger.md` untouched*, and
`plan.md`'s phase 4 verifies it as *`git diff --stat` showing neither shared
file in it*. Phase 4's run row narrowed that to one file — **`CHANGELOG.md`
is not in it** — without saying it had narrowed. And
`overview.md` §*Where spec and implementation diverged* lists two rows and
not this one, which is the table a later session opens to learn what the
build did differently from the contract.

### ⬜ 5 · `spec.md` still carries the anchor the build found wrong

**Established: read.**

`spec.md:138` names `skills/verify/scripts/broad_gate.py#main` as a
coordinate this work builds on. The call is in `gate()`, which phase 4 found
and the fragment's Notes cell records. `spec.md` itself was left as it stood
and `overview.md` §*Fed back into the spec* reads **None**, so a reader who
opens the contract gets the wrong unit and only finds the correction if they
open two other files.

### ⬜ 6 · The reader count is stated three different ways

**Established: read.**

This work item's subject is who the readers are, and the documents it
shipped do not agree on how many there are:

- `spec.md:83` — **four**, counting `hooks/evidence-advisor.py`.
- `skills/evidence-check/SKILL.md:178` — **three**, counting the advisor and
  merging `evidence-check` with CI's `ledger` job into one row.
- `CONTRIBUTING.md:21` — **three**, counting those two separately and
  dropping the advisor.

The SKILL's sentence is also slightly wide for its own table: the advisor
imports `check_ledger` in process and never reaches `main`, so it does not
*run this script* the way the other rows do — and that is why the notice
cannot reach it, which is correct and worth being the stated reason.

### ⬜ 7 · Four phase records carry `Ran by | unknown`

**Established: read.**

All four of `phases/phase-1.md` through `phase-4.md` read *unknown — the
spawn prompt named no model, and the value is the spawning session's to fill*.
The final commit went back and filled every `Commit` cell; the cell beside it
was left. It is the orchestrator's to write, not the smith's, which is why it
is here rather than in the fix list.

### ⬜ 8 · Two other exits of 1 print nothing, and the documents generalise past them

**Established: read.**

`CONTRIBUTING.md:21`'s block says *a run whose answer is exit 1 prints which
reading you took*, and `skills/evidence-check/SKILL.md`'s new section says
*where the answer is exit 1 and only there*. Two other paths return 1:
`skills/evidence-check/scripts/evidence_check.py:1723` (`--reverify`, a
ledger it could not read) and `:2423` (`--migrate`, rows it could not prove).
Neither prints the notice, which is right — neither is the lenient reading —
but the sentences as written say they would.

No behaviour is at risk: a reader of a `--migrate` run who sees no notice
draws the correct conclusion. What is at risk is the document's own
precision, in the one paragraph this work item added to make it precise.

### ⬜ 9 · The repository's first ledger fragment contradicts its own header comment

**Established: read.**

`seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` opens
with a comment that reads *No header — `fold_ledger.py` writes the `###` at
the release*, and the next content line is a `####` heading. `demote` clamps
at six levels so the fold is safe, and `CLAUDE.md` says a fragment *needs* no
header rather than forbidding one — nothing breaks. But this is the first
fragment this repository has ever written and it is what the next one will be
copied from, so the comment and the file should say the same thing.

## What I could not judge

| Item | Who answers |
|---|---|
| Whether `broad-gate` itself prints no notice at exit 2 in its own invocation — the fixture covers the grading, not the wiring. The overview already names this | the sealer |
| Whether the fix for finding 3 belongs in `agents/framer.md` or in the case — both readings are defensible and the choice changes what a gate guards | the repository owner |
| `hooks/evidence-advisor.py`'s behaviour on a drifted tree. Read from its docstring and its status filter, never run. Nothing here touches it | the review chain, or a later work item |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The notice's `NOT SEALED` limb is pinned by nothing — exempting the ledger check from the gate's failure form leaves the module 13 passed | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:251` · `skills/verify/scripts/broad_gate.py:590` | open | executed — mutation run, file restored byte for byte, tree clean |
| 2 | A third trigger of the deferred silence stands in the shared ledger: five coordinates with bare inner quotes are dropped whole while the run prints `1148 ok` | `skills/evidence-check/scripts/evidence_check.py:65` · `seal/ledger.md:63,71,81,143` | open | executed — the module's own `ANCHOR_RE` applied per ledger file; strict counts 1148 + 5 reproduce phase 4's 1153 |
| 3 | The `overview.md` scheduling divergence is a class: `agents/framer.md` forbids the memo the case demands, and a sibling 0.11.3 branch is red on it at its tip | `agents/framer.md:91` · `tests/test_chain_hooks_hardening.py:1014` | open | executed — `git ls-tree` over `feat/350-a-segments-own-wall-clock-is-in-no-column` |
| 4 | S8 says `seal/ledger.md` untouched and the branch touches it; the act is correct and the divergence table does not carry it | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md` | open | read — S8, phase 4's narrowed verification row, and the two-row divergence table |
| 5 | `spec.md` still names `broad_gate.py#main`; the correction lives in two other files and *Fed back into the spec* reads None | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md:138` | open | read |
| 6 | Three documents state three different reader counts for a work item about who the readers are | `spec.md:83` · `skills/evidence-check/SKILL.md:178` · `CONTRIBUTING.md:21` | open | read |
| 7 | Four phase records carry `Ran by \| unknown` while every `Commit` cell was filled | `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/phases/phase-1.md` | open | read |
| 8 | `--reverify` and `--migrate` also return 1 and print nothing; two documents say exit 1 always prints | `skills/evidence-check/scripts/evidence_check.py:1723` · `:2423` · `CONTRIBUTING.md:21` | open | read |
| 9 | The first ledger fragment says *No header* and carries a `####` heading | `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` | open | read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` at the target SHA | **13 passed** in 0.44 s, exit 0 read directly |
| The same module with `gate()` mutated so the ledger check is exempt from the failure form, restored byte for byte afterwards | **13 passed**, exit 0 — finding 1. `git status --porcelain` empty after the restore |
| The module's own `ANCHOR_RE` applied to `seal/ledger.md` and the new fragment, against every backticked coordinate-shaped token in each | 1148 and 5 strict matches — phase 4's 1153 reproduced; **5 coordinates in `seal/ledger.md` matched by nothing** — finding 2 |
| A grep for an unquoted minor anchor across every `.md` under `seal/` | one prose placeholder and no real coordinate — the fragment's two rows escape their inner quotes |
| `git ls-tree -r` over the two sibling 0.11.3 branches for each work item's `spec.md`, `plan.md` and `overview.md` | `feat/350-…` carries a spec and a plan and no memo; `feat/345-…` carries all three — finding 3 |
| The four `return`s of the old exit block against `exit_code`, enumerated by construction over its four branches | identical in every state: old-format 2, broken-or-refused 2, drifted 2-under-strict-else-1, otherwise 0. The call passes `totals, refused, drifted, args.strict` in the declared order. **No reader's exit code moves** |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It has not been taken at any SHA on this branch. It is the sealer's one act, after the rounds settle (contract §2) |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `ANCHOR_RE` drops a coordinate it cannot parse instead of naming it — the hash shape, the bare minor anchor, and the bare inner quote of finding 2 | `seal/follow-up.md` §*Schedulable items with nowhere else to go*, the existing row. Already deferred by this branch; finding 2 asks only that the third shape and its five live instances join the row | the repository owner |
| Whether the broad gate's own end-to-end run shows the notice absent at exit 2 | `overview.md` §*Not verified*. Already deferred by this branch | the sealer |

## Paste-ready fixes

Finding 1 — add to
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, beside the
other structural cases:

```python
def test_a_failing_ledger_check_is_what_reaches_the_failure_form():
    """S4's third limb. The notice says this tree would come back NOT SEALED,
    which is true only while a failing ledger check reaches `not_sealed`.
    `gate()` exempts no check by name: every entry of `checks` goes through
    one loop, and the loop is what this reads."""
    src = read(BROAD_GATE)
    start = src.index("    failures = []")
    head = src.index("if failures:", start)
    loop = src[start:head]
    assert "for name, check in checks.items():" in loop, loop
    assert "LEDGER" not in loop, f"the failure loop exempts a check by name:\n{loop}"
    assert "stamp.not_sealed(" in src[head:], "the failure form is no longer taken"
```

Seen red before it is planted: apply
`if name == LEDGER or not check.failed:` at `broad_gate.py:591`, run the
module, restore the file from bytes held in the mutating process. That is the
mutation this report ran, and it is the one this case exists to kill.

Finding 2 — append to the first row of
`seal/follow-up.md` §*Schedulable items with nowhere else to go*, after the
sentence ending *does not change who decides what to call it*:

```
**A third shape was measured on 2026-09-13 during round 1 of #354, and unlike the other two it is already standing in the shared ledger**: a quoted locator whose inner quotes are bare rather than escaped as `\"`. `ANCHOR_RE` matches nothing across it, so the coordinate is dropped whole — five rows of `seal/ledger.md` (`:63`, `:71`, `:81` twice, `:143`) are anchored by nothing while the run prints `1148 ok` for that file. Executed by applying the module's own `ANCHOR_RE` per ledger file and comparing against every backticked coordinate-shaped token in it; the strict counts, 1148 and 5, reproduce the 1153 the checker itself reported. So the fix has three shapes to catch, not two, and it has live instances rather than only a hazard.
```

Finding 3 — a new row in the same section of `seal/follow-up.md`:

```
**A framed work item is red on an existing case from the framer's own commit.** `agents/framer.md` §*What the framer writes* tells the framer to write `spec.md`, `plan.md` and `questions.md` and nothing else — **not** `overview.md` — while `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview` fails the moment a directory holds a spec or a plan without a memo beside it. The two cannot both be satisfied, so every work item on the ladder carries a red case from the framer's commit until whichever phase opens the memo. Met in #354, where the smith moved the memo from phase 4 to phase 3 and recorded it as that work item's own scheduling; measured again in round 1 of #354 on a sibling branch of the same release, `feat/350-a-segments-own-wall-clock-is-in-no-column`, whose work item carries a spec and a plan and no memo at its tip. What needs a person is which side gives: the framer writes a stub memo the builder replaces, or the case exempts a work item whose plan still has an open phase. Adding an exemption changes what a gate guards, which `CONTRIBUTING.md` asks a separate argument for.
```

Finding 4 — a third row in
`seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/overview.md`
§*Where spec and implementation diverged*:

```
| Whether `seal/ledger.md` is touched | `spec.md` S8 and `plan.md` phase 4 both say the shared ledger is untouched; seven of its rows were re-read, re-stamped and re-dated | touched, and the rows re-verified in place | This work's edits changed content under seven anchors that file cites. `broad-gate` passes `--strict`, so leaving them drifted is exit 2 and a branch that comes back refused. `CLAUDE.md` §*a change writes fragments* forbids APPENDING and carves out removal; re-verification is the third case and it is what leaves the ledger true. Not one row was appended — the new claims are all in this work item's own fragment. Phase 4 checked `git diff --stat` for `CHANGELOG.md` alone rather than for both files, which is where S8's other half went quiet |
```

Finding 5 — `spec.md:137-138`, §*Data & interfaces*:

```
Coordinates this builds on, to be cited by the ledger fragment rather than
duplicated here: `skills/evidence-check/scripts/evidence_check.py#main`,
`skills/verify/scripts/broad_gate.py#gate` — the ledger call site is in
`gate`, not in `main`, which phase 4 found and the fragment records.
```

Finding 6 — `skills/evidence-check/SKILL.md:178`:

```
Three readers grade drift over one tree, and the command above is the most
lenient of them. A fourth, `hooks/evidence-advisor.py`, imports this module
in process rather than running the script, so it never reaches the exit code
and never carries the line below.
```

and `CONTRIBUTING.md:21`, replacing *Three readers, one tree*:

```
Three readers of the exit code, one tree, and the disagreement is deliberate
```

Finding 7 — the `Ran by` cell of each of `phases/phase-1.md` through
`phase-4.md`, filled by the session that spawned the segment.

Finding 8 — `skills/evidence-check/SKILL.md`, in the new section:

```
**So a lenient run says it.** Where a check run's answer is exit 1 and only
there, the check prints which reading you took and what `broad-gate` would
say instead. Exit 0 and exit 2 print nothing extra, because every reader
grades those alike — and `--migrate` and `--reverify` have exit codes of
their own, which report what those writers could not do rather than how
anyone reads drift (#354).
```

and `CONTRIBUTING.md:21`, replacing *A run whose answer is exit 1 prints
which reading you took*:

```
A check run that comes back exit 1 prints which reading you took
```

Finding 9 — the header comment of
`seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md`:

```
<!-- One work item's rows. No `# <id>` title — `fold_ledger.py` writes the
`###` at the release and moves this file into `seal/ledger.md`; the `####`
below demotes to `######` under it. -->
```

Needs a fix: yes — 1, the notice's `NOT SEALED` limb is pinned by no case and
a mutation proves it; 2, the third shape of the deferred silence and its five
live instances are not in the row that tracks it; 3, the framer's contradiction
with the overview case reaches a sibling branch of this release and has no
durable home.

Loses a record or crashes: no

Nothing found leaves a record outside the root and nothing crashes. No exit
code moves in any of the four readers, and the `exit_code` extraction is
identical to the four `return`s it replaced in all four states. Finding 1 is
a case that will not fire, not a defect that fires now.

## Proof block

**Executed**

- `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` — 13 passed
- the same module under a mutated `gate()`, restored byte for byte — 13 passed
- `ANCHOR_RE` applied per ledger file against every backticked coordinate-shaped token
- a grep for unquoted minor anchors across every `.md` under `seal/`
- `git ls-tree -r` over `feat/345-…`, `feat/350-…`, `main` and `release/v0.11.3`
- `git diff`, `git log` and `git show` over `c7cc842...37f7321`
- `gh pr view 378`

**Read**

- `seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/`: `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`, `changelog.md`, `phases/phase-1.md` … `phase-4.md`
- `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md`, `seal/ledger.md` (the changed rows, cell by cell), `seal/follow-up.md`
- `skills/evidence-check/scripts/evidence_check.py` — `ANCHOR_RE`, `check_records`, `tree_names`, `exit_code`, `main`
- `skills/evidence-check/SKILL.md`, `CONTRIBUTING.md`, `README.md`, `README.ko.md`, `.github/workflows/test.yml`
- `skills/verify/scripts/broad_gate.py` — the header, `gate()`, the failure loop
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_chain_hooks_hardening.py` (the overview case), `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the failure-form cases)
- `.github/scripts/fold_ledger.py` — `demote`, `section`
- `hooks/evidence-advisor.py` — the docstring and the import of the checker
- `agents/framer.md`, `templates/sdd-plan.md`, `templates/sdd-phase.md`, `CLAUDE.md`

**Unverified**

- the full suite, the repository-wide lint and the typecheck — the sealer's, after the rounds settle (contract §2)
- `broad-gate`'s own end-to-end run on this branch — the sealer's
- `hooks/evidence-advisor.py` on a drifted tree — read, never run
