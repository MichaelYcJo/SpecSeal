# 1789996775-the-gate-states-what-its-own-fixes-disproved — review round 1 report

Target SHA `9948b8af`. Range `a66e1352..9948b8af`, ten commits. Draft pull
request 479. Reviewed in a `git clone --no-local` of the repository at that
SHA; nothing was written in the working checkout except this file.

## What this round was asked

Round 1, the first round of the work item: the whole branch
`release/v0.12.3..9948b8af` — that is `a66e1352..9948b8af`, ten commits —
against its own frame, spec compliance before quality. The frame is
`spec.md` A1–A8 and §*The correction marker*, `plan.md`'s four phases and
§*Alternatives considered*, and `questions.md` Q1–Q4. The work is issues
461, 464 and 465, each read with its *Not this* section, and the earlier
reports they cite in work item 1789956662's `rounds/`. The reviewer was
given five things the build disclosed about itself and asked to weigh each
rather than take it: A6's grep criterion returning two lines where `spec.md`
says none; the `seal_stamp.letter` A5 marker sitting after the table rather
than beside the row; three of the four A5 markers reading *It is not false,
and that is the point* where the fixed template reads *It is false because*;
`evidence-check --reverify` re-stamping three ledger rows where A7 counts
two; and A2's guard being one `git check-ref-format` call, with the claim
that `origin/HEAD` passes that call and never reaches it. A declared
divergence is still a divergence, so each was judged rather than accepted.
The ledger was read with `evidence_check.py .` unscoped and with no
`--reverify`. The broad gate was withheld for the `sealer`.

## What was confirmed, by execution

**A1 and Q2 — the property the docstring now states is the property the
command has.** Measured in a scratch repository on git 2.54.0, exit codes
read from `subprocess.run().returncode` rather than through a pipe:
`check-ref-format --branch @{-1}` exits 0 and prints `base`, while `HEAD`,
`HEAD~1`, `base@{u}` and `topic@{1}` each exit 128. `names_a_branch` returns
True for `@{-1}`, `base`, `release/v0.1.0` and a short SHA, and False for the
other four. The docstring at `skills/verify/scripts/broad_gate.py#names_a_branch`
says exactly that, and it no longer names the class `@{…}`.

**A2 and Q3 — the guard is git's answer and not a pattern wearing git's
clothes.** `a_runner_could_hold` is `git check-ref-format <ref>` on the label
the line is about to print, with no string test of any kind in the function.
Measured on the constructed label: `origin/@{-1}`, `origin/HEAD~1`,
`origin/base@{u}` and `origin/topic@{1}` exit 1; `origin/base`,
`origin/HEAD`, `origin/abc1234` and `origin/release/v0.1.0` exit 0. The
`git` helper returns `r.stdout` on a zero exit, which is `''` for this
command, so the `is not None` test reads a success rather than an empty
string — checked by driving the function directly.

**The `origin/HEAD` claim holds, and I measured the path rather than reading
it.** Driving `resolve_base` and `moved_line` in a clone that has a remote:
`--base HEAD` and `--base origin/HEAD` both resolve to the ref as given, so
`given_commit` and `commit` are the same commit, `Base.moved` is False, and
`moved_line` returns None before the guard is reached. `--base @{-1}`
resolves to `origin/base` and prints

    broad-gate: --base @{-1} is 4fc0838 in this checkout; this checkout says
    @{-1} tracks origin/base, which is 0457d34; a runner's checkout has no
    counterpart for @{-1} — origin/base is 1 ahead and 0 behind @{-1}. Every
    check below was asked about origin/base.

`--base base` still prints the `CI reads origin/base` filling, so the third
branch did not swallow the second.

**§15 — the A2 case is not vacuous.** `a_runner_could_hold` mutated to
`return True` turns
`test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold` red alone,
and the red reproduces round 2's finding 10 word for word: *— not the
origin/@{-1} a runner reads —*. The mutation was reverted and the tree
verified clean afterwards.

**A6 — all three sites say what the branch did.** `:19`, `:68` and the
docstring of `test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given`
each now say that one assertion of
`tests/test_the_seal_is_taken_once_by_the_sealer.py` moved and name why. A3
of work item 1789956662's `spec.md` is untouched, which is issue 465's own
*Not this*.

**A7 — the ledger is in the state A7 describes, and the third row is marked.**
R4 of work item 1789956662 carries both a `Corrected 2026-09-21` marker and a
`Re-read` note; R5 carries two `Re-read` notes; G6 of work item 1789985781
carries two. `evidence_check.py .` unscoped exits 0 at 1399 ok, 0 drifted, 0
broken, and the records arm refuses nothing. `correction-check` over the
range reports no dropped correction.

**A8 — nothing moved that was not meant to.**
`tests/test_the_gate_asks_the_range_ci_will_ask.py` and
`tests/test_the_seal_is_taken_once_by_the_sealer.py` are green together at
154 passed. `tests/test_the_gate_names_every_step_ci_runs.py`,
`tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py` and
`tests/test_docs_line_wrap.py` are green at 71 passed.

**§12 — the class of the changed printed sentence is closed.** The only
carriers of the runner clause outside work item 1789956662's past-state
records are `broad_gate.py` itself and the case module, both corrected.
`agents/sealer.md` quotes the command and not the line, so it carries no
stale copy.

## What was confirmed, by reading

**The A5 marker after the table is the right call.** A `<!-- -->` line
between two rows ends the table in every renderer that reads a table as a run
of adjacent rows, and the `seal_stamp.py#letter` row has three rows below it.
The marker's first sentence says where it sits and names the row it is about,
so a reader who finds the marker can find the statement. The two properties
`spec.md` fixes deliberately — the uppercase verb and naming the work item
and the issue rather than a round and a finding — are both kept.

**The three markers reading *It is not false, and that is the point* are the
right call, and the wrong call was available.** The three A4 statements are
true; what they lacked is the label saying how anybody knows. A marker
asserting the sentence was false would put a second false statement into a
record this work item is correcting for carrying one. The slot's job under
`spec.md` §*The correction marker* is the grounds with the coordinate, and
each of the three still carries it —
`rounds/round-2-report.md`:195 and the R3 row of `seal/ledger.md`.

**The third re-stamped ledger row is the right call.** A7 names two rows
because it counted the rows citing `moved_line` and `panel` in work item
1789956662. G6 of work item 1789985781 cites `panel` too, `--reverify`
re-stamps by coordinate, and leaving a row re-stamped and unread is the
silence `seal/follow-up.md` already has an open item about. The row carries a
note saying what was read.

**Q1 was built and not answered, which is what `questions.md` requires.** The
row is ⬜, the released `CHANGELOG.md` §0.12.2 keeps the unlabelled sentence,
and the divergence is disclosed in this work item's `overview.md`
§*Not verified* and in `seal/follow-up.md`, both naming the repository owner.
`unverified-check --baseline origin/release/v0.12.3` reads four open rows
here and exits 0.

## Findings

### 1 ⬜ correction — `overview.md` says no `survivors.md` row was written, and two were

`seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/overview.md`,
§*Not done*, at the paragraph beginning *No `survivors.md` row was written*.

The paragraph says the file holds nothing because the check reported nothing.
`seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/survivors.md`
exists with two rows, and three other documents in the same directory say so:
`questions.md` Q4 — *The other two are excused in `survivors.md` with a quote
and grounds* — `phases/phase-3.md` §*What this phase removes*, and
`phases/phase-2.md`, which says Q4 was clean at phase 2 and did not stay
clean.

The paragraph was written at `cfa718ce` and `survivors.md` was added at
`95503f60`, the next commit, which also edited `overview.md` and did not
correct it. That is the class this work item exists to close, standing in its
own closing memo: a statement the same branch's later work disproved, left
where a reader meets it.

It is a correction rather than a round. `docs/review-chain-spec.md` §*The
last round verifies* — *A finding located in a record is a correction, not a
round* — puts a finding under `seal/specs/` outside `Needs a fix`, and this
one is prose no checker reads, so it is corrected in passing.

### 2 ⬜ — writing `survivors.md` silenced the survivor arm instead of excusing its rows visibly

`skills/code-review/scripts/survivor_check.py`, the corpus that feeds `FLOOR`.
The instance is
`seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/survivors.md`.

Measured, four tree states, `survivor-check --range origin/release/v0.12.3...HEAD`:

| Tree | Result |
|---|---|
| `f7c9dd39`, before `survivors.md` existed | 2 places, exit 1, scoring 1.90 and 1.67 against `FLOOR = 1.6` |
| `9948b8af`, as it stands | *no removed wording is still standing*, exit 0 |
| `9948b8af` with `--exempt` passed, which is the form CI uses | the same, exit 0 — no `exempt` line for either row |
| `95503f60` with `survivors.md` deleted in a probe commit | 2 places, exit 1 |
| `95503f60` with only the prose blockquote elided | 1 place, exit 1; with `--exempt`, `exempt seal/ledger.md:2377 -- <grounds>`, exit 0 |

The cause is the arithmetic `survivor_check.py`'s own module docstring
describes: a file carrying the wording raises the document frequency of every
phrase it holds, and both survivors sat within 0.07 and 0.30 of the floor. An
exemption row quotes the surviving text by design, so writing the row is what
pushes the thing it excuses under the floor. The docstring already excludes a
work item's `rounds/` records for exactly this reason — *the review chain is
what produces the disarming input* — and does not exclude `survivors.md`.

What it costs is the property the skill states in the same file: *An exempted
survivor is still printed, under `exempt`, with its grounds — a row that
silences something invisibly is a row nobody audits.* For this branch the two
rows are silenced invisibly, and `overview.md` then reads the silence as a
clean branch, which is finding 1.

The tool change is out of this work item's scope. Issues 461, 464 and 465 do
not reach `survivor_check.py`, the branch does not touch it, and a round on a
docs branch should not commission a change to an untouched gate. It goes to
`seal/follow-up.md` for the repository owner. What belongs to this branch is
saying what was measured, which finding 1's fix carries.

### 🟢 A6's criterion returns two lines, and leaving round 3's text is the right call

`seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/spec.md`,
A6.

The criterion's own sentence disagrees with itself. It reads *`grep -n
"byte-identical\|exactly as it did\|reading as it did"` over the module
returns nothing that still claims the module was untouched* — the command
half says the grep is empty and the qualifier half says no surviving hit may
claim the module was untouched. A correction written in the vocabulary of the
sentence it corrects cannot satisfy the first half, so the two halves could
never both be met. The build met the qualifier, which is the half that
carries the claim.

Measured: the grep returns `:22` — *all but ONE assertion … reading as it
did* — and `:74` — *It is NOT byte-identical*. Both are corrections. The
third replacement is not matched at all, because the phrase wraps across two
lines and the grep is line-based.

Rewording round 3's paste-ready text to empty a grep would be the move this
repository refuses elsewhere in the same breath — `plan.md`'s own Q4 row says
a survivor is answered with grounds and *never a reword chosen to quiet the
checker*. The divergence row in `overview.md` is the right home and it is
already written. Nothing is owed.

### 🟢 the `origin/HEAD` account is true, and its stated mechanism is one link short

`seal/ledger/1789996775-the-gate-states-what-its-own-fixes-disproved.md`, W2,
Notes; the same sentence stands in `overview.md` §*Fed back into the spec*.

The claim is that `origin/HEAD` is the one spelling `check-ref-format`
accepts that no `--base` reaches, because `names_a_branch` refuses `HEAD` a
step earlier. Measured, both halves hold: `check-ref-format origin/HEAD`
exits 0, `names_a_branch(HEAD)` is False, and `moved_line` returns None for
`--base HEAD`.

The link that is not written down is the one that actually stops it. Refusing
`HEAD` sends the resolution to step 3, step 3 leaves `ref` equal to `given`,
so `Base.moved` is False and `moved_line` returns before `a_runner_could_hold`
is called at all. The guard lives in `moved_line` and is not gated by
`names_a_branch`, so *a step earlier* names the cause and not the mechanism.
The sentence is true as written and a Notes cell is where an account like
this belongs, so this is recorded rather than asked for.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | ⬜ correction — `overview.md` §*Not done* says no `survivors.md` row was written; two were, in the next commit, and `questions.md` Q4, `phases/phase-2.md` and `phases/phase-3.md` all say so | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/overview.md#"## Not done"` | open | Read: the paragraph landed at `cfa718ce`, `survivors.md` at `95503f60`. A finding under `seal/specs/` is a correction and not a round (`docs/review-chain-spec.md` §*The last round verifies*), so `Needs a fix` does not count it |
| 2 | ⬜ writing `survivors.md` pushes the survivors it excuses under `FLOOR`, so the arm prints nothing where the skill says it prints `exempt` with the grounds | `skills/code-review/scripts/survivor_check.py#FLOOR` | deferred seal/follow-up.md | Executed over four tree states: 2 places at `f7c9dd39`, 0 at `9948b8af` with and without `--exempt`, 2 again with `survivors.md` removed in a probe commit, and 1 printed as `exempt` with the blockquote elided. Out of scope — issues 461, 464 and 465 do not reach that file and the branch does not touch it |
| 🟢 | A1 and Q2 verified — the docstring states the property the command has | `skills/verify/scripts/broad_gate.py#names_a_branch` | not a defect | Executed on git 2.54.0 in a scratch repository, exit codes read from `returncode`: `@{-1}` exits 0 printing `base`; `HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}` each exit 128 |
| 🟢 | A2 and Q3 verified — the guard is git's own answer, with no string test in the function | `skills/verify/scripts/broad_gate.py#a_runner_could_hold` | not a defect | Executed: `origin/@{-1}`, `origin/HEAD~1`, `origin/base@{u}`, `origin/topic@{1}` exit 1; `origin/base`, `origin/HEAD`, `origin/abc1234`, `origin/release/v0.1.0` exit 0. Issue 461's *Not this* is satisfied |
| 🟢 | A2's case verified not vacuous, and the red reproduces round 2's finding 10 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold` | not a defect | Executed: the guard mutated to `return True` turns that case red alone, at *— not the origin/@{-1} a runner reads —*. Mutation reverted, tree verified clean |
| 🟢 | the `origin/HEAD` claim verified by driving the resolver, not by reading it | `skills/verify/scripts/broad_gate.py#moved_line` | not a defect | Executed: `--base HEAD` and `--base origin/HEAD` both resolve to the ref as given, `Base.moved` is False and the line is None; `--base base` still prints the `CI reads` filling. The Notes cell's mechanism is one link short and is recorded above |
| 🟢 | A6 verified — all three sites say what the branch did, and A3 of the shipped `spec.md` is untouched | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_a_repository_with_no_remote_at_all_resolves_to_the_ref_as_given` | not a defect | Read the three sites against round 3's finding 15; executed the module at 154 passed with `tests/test_the_seal_is_taken_once_by_the_sealer.py` |
| 🟢 | A6's criterion returns two lines, and leaving round 3's paste-ready text is the right call | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/spec.md` | not a defect | The criterion's two halves disagree and the build met the one carrying the claim. Both hits are corrections. The divergence row in `overview.md` is the right home and is written |
| 🟢 | the A5 marker after the table verified — the placement moved, the two fixed properties did not | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | not a defect | Read: a comment line between two rows ends the table, three rows sit below the one being corrected, and the marker's first sentence names where it sits and which row it is about |
| 🟢 | the three markers reading *It is not false* verified — the template's slot still carries the grounds with the coordinate | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/overview.md` | not a defect | Read all four markers. The three A4 statements are true, so asserting falsity would add a second false statement to a record being corrected for carrying one |
| 🟢 | A7 verified — three rows marked where A7 counts two, and the third is the right one to mark | `seal/ledger.md` | not a defect | Executed `evidence_check.py .` unscoped: exit 0, 1399 ok, 0 drifted, 0 broken, records arm refuses nothing. `correction-check` over the range reports no dropped correction. Read R4, R5 and G6 for the markers |
| 🟢 | A8 verified — no exit code, verdict or resolution moved beyond A2's one sentence | `skills/verify/scripts/broad_gate.py#panel` | not a defect | Executed 225 cases across six modules, all green; `panel`'s rows and elision are unchanged in source |
| 🟢 | §12 verified — no stale copy of the runner clause outside the past-state records | `agents/sealer.md` | not a defect | Read a tree-wide sweep for the clause and for the printed line's prefix: the only carriers are `broad_gate.py` and the case module, both corrected. `agents/sealer.md` quotes the command, not the line |
| 🟢 | Q1 verified built and not answered | `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/questions.md` | not a defect | Executed `unverified-check --baseline origin/release/v0.12.3`: four open rows here, exit 0. The row is ⬜, and `seal/follow-up.md` carries the item for the owner |

## Executed probes

| What was run | Result |
|---|---|
| `git check-ref-format --branch` over nine spellings in a scratch repository, exit code read from `returncode` | `@{-1}` exit 0 printing `base`; `HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}` exit 128; `base`, `release/v0.1.0`, `abc1234`, `origin/HEAD` exit 0 |
| `git check-ref-format` on the constructed runner label, eight spellings | `origin/@{-1}`, `origin/HEAD~1`, `origin/base@{u}`, `origin/topic@{1}` exit 1; `origin/base`, `origin/HEAD`, `origin/abc1234`, `origin/release/v0.1.0` exit 0 |
| `moved_line` driven against a clone with a remote for `HEAD`, `origin/HEAD`, `@{-1}`, `base`, `HEAD~1` | the first two and the last return None with `moved` False; `@{-1}` prints the no-counterpart filling; `base` prints the `CI reads` filling |
| `a_runner_could_hold` mutated to `return True`, the two new cases re-run | `test_the_line_does_not_name_a_ref_a_runners_checkout_cannot_hold` red alone, reproducing round 2's finding 10 verbatim; mutation reverted, tree clean |
| `bin/test tests/test_the_gate_asks_the_range_ci_will_ask.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q` | 154 passed |
| `bin/test` over `tests/test_no_real_identifiers.py`, `tests/test_one_word_one_meaning.py`, `tests/test_the_gate_names_every_step_ci_runs.py`, `tests/test_docs_line_wrap.py` | 71 passed |
| `bin/evidence-check .` unscoped, no `--reverify` | exit 0 · 1399 ok · 0 drifted · 0 broken · records arm 0 refused |
| `bin/correction-check --range origin/release/v0.12.3...HEAD` | exit 0, no merge commit in the range so no correction can have been dropped |
| `bin/unverified-check --baseline origin/release/v0.12.3` | exit 0, four open rows for this work item |
| `bin/survivor-check --range origin/release/v0.12.3...HEAD` at four tree states, with and without `--exempt` | 2 places at `f7c9dd39`; 0 at `9948b8af` either way; 2 with `survivors.md` removed in a probe commit; 1 printed as `exempt` with the blockquote elided. Finding 2 |
| the grep `spec.md` A6 names, over the case module | two lines, `:22` and `:74`, both corrections; the third replacement wraps and is not matched |
| the broad gate — full suite, repository-wide lint, typecheck | not yet — withheld for the `sealer`, which takes it once after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 2 — a `survivors.md` raises the document frequency of the phrases it quotes and pushes its own survivors under `FLOOR`, so the arm prints nothing where the skill promises an `exempt` line with the grounds. The `rounds/` exclusion in the same module is the shape of the repair | `seal/follow-up.md`, added in the closing commit | the repository owner |

## Paste-ready fixes

Replacing the whole `No survivors.md row was written` paragraph of
`seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/overview.md`
§*Not done*. This is finding 1's fix and it carries finding 2's measurement.

```markdown
**Two `survivors.md` rows were written, and the file is why the check is
now silent.** Phase 3's first removal was too wide, `survivor-check` over
the range reported two standing places at 1.90 and 1.67 against a floor of
1.6, and both were excused with a quote and grounds rather than reworded.
Measured afterwards at `9948b8af`: the same command reports nothing, with
`--exempt` and without it. Removing `survivors.md` in a probe commit brings
both places back. The file's own quotes raise the document frequency of the
phrases it excuses, which is the arithmetic
`skills/code-review/scripts/survivor_check.py` documents for a work item's
`rounds/` records and excludes them for — so the two rows are silenced
rather than printed under `exempt` with their grounds, and a reader of the
step learns nothing. The tool question is a `seal/follow-up.md` row for the
repository owner; the rows and their grounds stand as written.
```

Needs a fix: no
Loses a record or crashes: no

## Proof

Opened, in the clone at `9948b8af`:

- `skills/verify/scripts/broad_gate.py` — `git`, `REMOTE_LABEL`, `Base`,
  `moved_line`, `short_commit`, `names_a_branch`, `a_runner_could_hold`,
  `resolve_base`, `panel`
- `tests/test_the_gate_asks_the_range_ci_will_ask.py` — the diff whole, and
  the two new cases with their fixture builder
- `seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/` —
  `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
  `survivors.md`, `changelog.md`, `phases/phase-2.md`, `phases/phase-3.md`,
  `phases/phase-4.md`
- `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/` — the
  diff to `spec.md`, `plan.md`, `overview.md` and `changelog.md`;
  `rounds/round-1.md` and `rounds/round-3.md` for the record shape
- `seal/ledger.md` R4, R5 and G6 of the two cited work items;
  `seal/ledger/1789996775-the-gate-states-what-its-own-fixes-disproved.md`;
  `seal/follow-up.md`
- `skills/code-review/scripts/survivor_check.py` — the module docstring,
  `FLOOR`, `read_exemptions`, `exempted`, `main`
- `skills/code-review/scripts/chain_check.py` — `CLOSED_WORDS`, `HOME_WORDS`,
  `FIX_WORDS`
- `templates/sdd-round.md`, `bin/survivor-check`,
  `.github/workflows/hygiene.yml` §*wording this branch removed*
- issues 461, 464 and 465, read with `gh issue view`
- `CLAUDE.md`, and `agents/sealer.md` for the line's other reader

Not opened: `phases/phase-1.md` beyond its quoted red output, the round
reports of work item 1789956662 beyond the findings the build cites, and
`skills/verify/scripts/seal_stamp.py`.
