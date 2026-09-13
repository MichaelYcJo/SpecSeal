# Round 1 — 1789296200-the-record-before-the-fix-sequence-has-no-arm

Target SHA `edb4578`, base `c7cc842`, branch
`feat/345-the-record-before-the-fix-sequence-has-no-arm`, draft pull request
381. No earlier round; nothing inherited.

**No agent was spawned for this round** (`agent-contract` §6). The
`code-review` skill's Phase 1 and Phase 2 ask for finder and verifier agents;
§6 withholds that from every agent, so the eight angles were run here,
sequentially. The broad gate was not run and is not this round's
(`agent-contract` §2); §3 was never reached, because the spawn prompt ordered
no check §2 excludes.

## What the implementer's account claimed, and what the code says

The pull request body and `overview.md` were read in full and treated as
claims. Nine were opened. Seven stand as written, two do not, and both of the
two are recorded below — ⬜ 4 is the second, and the first is that
`overview.md` §*What the gate change carries* calls the phase 2 observation's
platform cost *one `git rev-parse HEAD`*, where `head_moved` in fact makes up
to three git calls (`rev-parse HEAD`, `rev-parse <target>^{commit}`, and
`log`). That is an understatement of a cost that is still negligible, so it is
noted here rather than raised as a finding.

The account's central factual claim — 40 differing records of 152 — is
checkable in its method and in the two records it names, and I checked both.
It is not checkable in its result, and ⬜ 4 is why.

## Findings

### 🟡 1 — the record that needs the fourth exit is never told the fourth exit exists

`skills/code-review/scripts/chain_check.py:2585` (the `else` branch), reading
the message built at `skills/code-review/scripts/chain_check.py:2542`.
Established by **execution**.

This branch adds a pass state to `written_late` and documents it in four
places: the template, the spec, the orchestration half, and the notice the
check prints for a record that already carries the row. It does not add it to
the **error** message — the one text the person who needs the exit actually
reads, because they meet it by having no row.

Captured by running the shipped refusal and printing what a person sees. The
message ends:

```
Commit the record when the round posts, with its verdicts `open`, and update
them when the fixes land: the UPDATE commit may descend from the fix, the
adding commit may not
```

`Written late`, `--written-late` and the word *fourth* are all absent from it.

Why it matters is the work item's own story. The record that fails here is
already committed, so *commit the record when the round posts* is advice
nobody meeting this line can act on — that is precisely the dead end work item
`1789034970` reached, and the reason this branch exists. The exit is reachable
in one hand-edit-and-commit, and the failure text sends the reader back to the
three repairs the branch set out to replace.

`agent-contract` §14 is the rule: the change moved what a person sees, so the
sentence they see is what has to move with it. The existing case
`test_the_failure_says_what_to_do_instead` pins the old advice and nothing
pins the new exit on the error path.

### 🟡 2 — `new` prints *0 commits stand between them*, with two readings that are both false, when HEAD is behind the reviewed commit

`skills/code-review/scripts/round_record.py:1548` (`head_moved_line`), reached
from `skills/code-review/scripts/round_record.py:1517` (`head_moved`).
Established by **execution**.

`head_moved` asks `git log <reviewed>..<head>`, which lists what HEAD reaches
and the reviewed commit does not. When HEAD is an ancestor of the reviewed
commit that set is empty, and the two differ all the same, so the line is
printed with nothing in it. Observed on a scratch repository whose HEAD was
moved back one commit:

```
round-record: the commit this round read is not the branch's HEAD — the round
read 63b3260, HEAD is ca01f6e, and 0 commits stand between them.
  There are two readings and only you can tell them apart. Either the fix pass
  for this round has already run … Or HEAD moved during the review …
```

Neither reading is true. Nothing was committed after the review on this tree;
the tree is behind the commit the record names. The orchestrator is asked to
choose between two wrong explanations with an empty listing to choose from,
at the one moment the whole observation exists to inform.

`head_moved`'s own docstring claims this case is covered — *a target that is
not an ancestor of HEAD still answers, the listing is what HEAD reaches and
the target does not, and that is the honest answer for a branch somebody
reset*. That holds for a branch reset sideways, where HEAD does carry commits
the target lacks; it does not hold for a tree that is simply behind, and the
difference is not in the code.

The state is reachable without anybody doing anything strange: `--target`
naming the pull request's head ref while the local tree has not fast-forwarded,
or a `git switch --detach` onto an earlier commit to re-read something during
the round. Both leave the record itself correct and the printed advice wrong.

### ⬜ 3 — *1 commit stand between them*

`skills/code-review/scripts/round_record.py:1556`. Established by
**execution** — the same probe as 🟡 2, second scenario.

The count's singular arm is written (`'' if count == 1 else 's'`) but the verb
is not, so a one-commit difference prints *and 1 commit stand between them*.
The one-commit case is the commonest real one, since the round's own paragraph
is a single commit. No case exercises it: the module asserts only *2 commits
stand between them*, so mutating the singular arm away kills nothing.

### ⬜ 4 — the forty differing records are named in no committed file, and `overview.md` says they are

`seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29`,
and `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/phases/phase-1.md`
§*The differing records are innocuous*. A record-located finding, so
`docs/review-chain-spec.md` §*A finding located in a record is a correction,
not a round* makes it a correction: ⬜, no fix pass owed, and `Needs a fix`
does not count it. Established by **reading**, with one coordinate re-verified
by **execution**.

`overview.md` says *`phases/phase-1.md` holds the method, the exclusions, the
stated bias, and the 40 named individually.* `phase-1.md` holds the first
three. It names two of the forty, and says so in its own words: *Two recent
ones were opened by hand rather than counted.* The sentence phase 1 was given
asked for all of them — *naming the differing records individually so a reader
can open each* — and `phase-1.md` closes by recording that the script is a
probe and is not committed.

The number is not loose talk in a work item: `docs/review-chain-spec.md:1326`
states it, `skills/code-review/scripts/round_record.py:1564` prints it to
every user on every differing run, `skills/code-review/orchestration.md:396`
repeats it, and `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md`
row R1 carries **The number is 40 of 152** in its Notes column as the grounds
for the whole design. `test_the_spec_carries_the_measurement_the_refusal_rests_on`
pins the string. `agent-contract` §5's sentence is the exact shape of this:
the count can be checked and the claim it stands for cannot.

**What I could establish.** The method is sound. The measurement script is
still on disk in this session's scratchpad, and reading it confirms every
claim `phase-1.md` makes about it: the population is
`refs/remotes/pull/*` plus local feature branches, the adding commit is the
latest one as `chain_check.added_on_branch` takes it, the `Target SHA` is read
as that commit wrote it and every SHA in the cell counts, a commit adding more
than one `round-N.md` is excluded, and the stated bias does run one way. I
re-derived phase 1's first named example against this tree by execution:
`a0f0e9a` adds that record, its `Target SHA` cell reads `5ce162e`, its first
parent is `b46ff77`, and the single commit between is `b46ff77 docs: round 1's
paragraph is recorded before the round runs`. The exclusion rule is also
correct on that commit — it adds `round-1.md` and `round-1-report.md`, one
round record, so it is counted rather than dropped.

So the verdict the number supports is not in doubt. What is in doubt is
whether anyone can ever check it again, and the answer today is no: no
`refs/remotes/pull/*` ref exists in this worktree (`git for-each-ref
'refs/remotes/pull/*'` returns nothing), so the population cannot be
reconstructed from the tree.

**There is a window, and it is closing.** The list of forty, named
individually with each record's path, `Target SHA`, adding commit, subject,
parent and the ref it was seen on, is sitting in this session's scratchpad as
`phase1-result.txt` — 131 lines. Copying that block into `phase-1.md` makes
`overview.md`'s sentence true and costs one paste. A session scratchpad does
not outlive the session, and this is a work item about a fact that survived
only in a session that had ended.

The same scratchpad holds the rest of the smith's probe files — the
measurement scripts, the phase reddening drivers, the mutation drivers, and
two saved copies of the generator. `agent-contract` §7 asks a probe to leave
nothing behind; a session scratchpad is the harness's designated place for
temporary files, so whether that is a §7 leaving is the orchestrator's call
and not a finding here. What matters is the order: take the list out before
anything cleans the directory.

### ⬜ 5 — the record is fetched from git once more per record, for nothing

`skills/code-review/scripts/chain_check.py:2537`. Established by **reading**.

`said = written_late_reason(reader, root, rel)` is computed after the `late`
map is built and before it is consulted, so it runs even when `late` is empty
— the ordinary case for every correct record that closed a finding with a fix.
`written_late_reason` calls `read_record`, which is `git show HEAD:<rel>` and
is not cached, so every such record now costs one extra subprocess. Moving the
call below a `if not late: return [], []` guard, or into the loop, costs
nothing and reads the file only for the records the answer is about.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the refusal at the pull request never names the fourth exit, so the record that needs it is sent back to the three repairs this branch replaced | `skills/code-review/scripts/chain_check.py:2585` | open | executed — the shipped refusal captured and searched: `Written late`, `--written-late` and *fourth* all absent |
| 🟡 2 | `head_moved_line` prints *0 commits stand between them* with an empty listing and two readings that are both false, when HEAD is behind the reviewed commit | `skills/code-review/scripts/round_record.py:1548` | open | executed — scratch repository, HEAD detached one commit back, line captured verbatim |
| ⬜ 3 | *1 commit stand between them* — the singular arm is written for the noun and not the verb, and no case exercises it | `skills/code-review/scripts/round_record.py:1556` | open | executed — same probe, diverged-branch scenario |
| ⬜ 4 | the forty differing records are named in no committed file, and `overview.md` says `phase-1.md` names them | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/overview.md:29` | open | read, with phase 1's first named example re-derived by execution against this tree |
| ⬜ 5 | `written_late_reason` is called on every record whether or not anything is late, costing one uncached `git show` each | `skills/code-review/scripts/chain_check.py:2537` | open | read |
| 🟢 | hostile `--written-late` values cannot corrupt a record — a pipe, a newline and an unclosed HTML comment are each refused before the write | `skills/code-review/scripts/round_record.py:829`, `skills/code-review/scripts/round_record.py:593` | answered | executed — all three refused, exit 2, no record written. `write_record` asks the hider question of the composed artefact, so the new flag inherits the guard without a guard of its own |
| 🟢 | A6's pin is the existing case, genuinely unmodified and it still fires | `tests/test_a_record_precedes_the_fixes_it_commissions.py` | answered | executed — the case body is absent from the diff; only the `record` and `late_run` helpers gained a defaulted parameter it does not pass. Turning the error branch into a notice reddens it |
| 🟢 | the four new units each die alone | `skills/code-review/scripts/round_record.py:1486`, `skills/code-review/scripts/round_record.py:1517`, `skills/code-review/scripts/round_record.py:1548`, `skills/code-review/scripts/chain_check.py:2435` | answered | executed — five mutations in a throwaway clone, every one killed, each reddening the cases its own phase record claims |
| 🟢 | no red window between `templates/sdd-round.md` and the generator | `templates/sdd-round.md`, `skills/code-review/scripts/round_record.py:1865` | answered | executed — both land in `6d4f30f`, and five further modules that generate or read a record are green at 302 passed |
| 🟢 | `close` and `seal` keep the new row | `skills/code-review/scripts/round_record.py:2892` | answered | read — both assign into rows they find by `field_index` and never rebuild the block, which is what A7's probe found and what its case now holds |
| 🟢 | the ten re-stamped `seal/ledger.md` rows are honest, and the new claims went to the fragment | `seal/ledger.md`, `seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md` | answered | executed — `evidence-check .` exit 0, 1161 ok · 0 drifted · 0 broken. Re-verification is neither the appending `CLAUDE.md` forbids nor the removal it carves out: the three new claims are in the branch's own fragment and `seal/ledger.md` gained no row |
| 🟢 | neither spent word was coined with | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/spec.md:150` | answered | executed — no added line in `skills/`, `templates/`, `docs/` or `tests/` uses *arm* in any sense, and the one use of *declaration* is `routing.md`'s established meaning in a docstring; `tests/test_one_word_one_meaning.py` green |
| 🟢 | the A7 probe and its scratch repository really are gone | `seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/phases/phase-3.md` | answered | executed — nothing named for it survives in the repository, in the session scratchpad, or as a worktree or branch. The one `test_tmp_*` file still in the scratchpad belongs to a sibling work item's session and reads that item's own measurements, not this one's |
| ❓ | the run's only new arm is one the orchestrator holds, and nothing counts how often it is reached for | `skills/code-review/orchestration.md:415` | open | read — the guard against *reaching for it every round* is a sentence, not a check. `plan.md` names that as its own six-month failure scenario, and the gate-change disclosure states the direction honestly, so this is a question for the repository owner rather than a defect |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_new_says_when_head_is_not_the_target.py tests/test_a_record_says_why_it_was_written_late.py tests/test_a_record_precedes_the_fixes_it_commissions.py -q` | 67 passed in 46.92s |
| `bin/test tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py tests/test_a_record_says_what_ran_it.py tests/test_the_reopening_is_one.py -q` | 302 passed, 1 skipped in 174.95s — the modules that generate or read a record and were not named in the account's verification table |
| `bin/test tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py -q` | 38 passed |
| `bin/test tests/test_a_probe_does_not_outlive_its_round.py tests/test_a_probe_that_commits_says_so.py -q` | 10 passed |
| `bin/evidence-check .` | exit 0 — 1161 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| mutation, throwaway clone at `edb4578`: the three calling lines removed from `new` | 5 failed, 1 passed — killed |
| mutation: `head_moved_line`'s listing blanked | 1 failed, 5 passed — killed |
| mutation: `written_late_cell`'s emptiness test disabled | 5 failed, 6 passed — killed |
| mutation: `written_late_reason` returns a reason for a bare `yes` | 2 failed, 48 passed — killed |
| mutation: `written_late` never consults the cell | 1 failed, 49 passed — killed |
| mutation: `written_late` records the late record as a notice rather than an error | `test_a_record_added_after_its_own_fix_fails_after_the_cutoff` failed — A6's pin fires |
| probe: `new --written-late` with a pipe, a newline, and an unclosed HTML comment | exit 2 each, no record written, each refused by name |
| probe: `new` with HEAD detached one commit behind the reviewed commit | `and 0 commits stand between them`, empty listing, both readings printed — 🟡 2 |
| probe: `new` with the reviewed commit and HEAD on diverged branches | `and 1 commit stand between them` — ⬜ 3 |
| `git show a0f0e9a` and `git log 5ce162e..a0f0e9a^` | phase 1's first named differing record re-derived: parent `b46ff77`, one commit between, subject as `phase-1.md` quotes it |
| `git for-each-ref 'refs/remotes/pull/*'` | no refs — the measurement's population is not reconstructible from this tree |
| `git status --porcelain`, `git worktree list`, `git branch -a` | tree clean at `edb4578`; no worktree, branch or file left by this branch's probes. This round's own clone and probe files are deleted |
| the full suite, the repository-wide lint, the typecheck | **not yet — not run, and not this round's** (`agent-contract` §2). The sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `new --target <a revision that is not a full SHA>` writes the revision verbatim into `Target SHA`, and the cell then names no commit | already deferred by the branch: `overview.md` §Not done, the docstring of `test_a_target_given_as_a_revision_is_named_by_its_sha`, and an issue the orchestrator filed on the tracker | the repository owner — I confirmed the deferral is honest, since `new` ends in the very check that reports the state, so it is loud rather than silent. Recorded here so a later round does not re-open it as new |

## Paste-ready fixes

🟡 1 — name the fourth exit where the refusal is raised. In
`skills/code-review/scripts/chain_check.py`, replace the closing branch of
`written_late`:

```python
        else:
            errors.append(
                (
                    rel,
                    line_no,
                    message + ". Where the fix pass really did run before this "
                    "record reached a commit, the record may SAY so and this "
                    f"prints instead of failing: a `| {WRITTEN_LATE} | "
                    f"{FLOOR_YES} — <why> |` row in its field table, written by "
                    '`round_record.py new --written-late "<why>"`, or added by '
                    "hand and committed like any other correction to a record "
                    "already on the branch. A bare `yes` buys nothing — the "
                    "reason is the whole of what the row is for",
                )
            )
```

The hand-edit half is the sentence that matters: by the time this line is
read the record is committed, so the flag on its own names an exit the reader
can no longer take.

Pin it beside the case that pins the old advice, in
`tests/test_a_record_precedes_the_fixes_it_commissions.py`:

```python
def test_the_failure_names_the_fourth_exit(repo):
    """`agent-contract` §14. The record refused here is the only one that
    needs the row, and it is refused for not having it — so the refusal is
    the one text where naming the row changes what anybody does."""
    late_run(repo, NEW_ITEM)
    code, out = run(repo)
    assert code == 1, out
    assert check_module().WRITTEN_LATE in out, (
        "the record that needs the fourth exit is not told it exists"
    )
    assert "--written-late" in out, out
    assert "added by hand" in out, (
        "the flag alone names an exit a committed record can no longer take"
    )
```

Seen red by reverting the message change: with the branch as it stands the
case fails on the first assertion, which I confirmed by capturing the shipped
refusal.

🟡 2 — answer the empty listing instead of printing a line about nothing. In
`skills/code-review/scripts/round_record.py`, at the top of `head_moved_line`:

```python
def head_moved_line(reviewed, head, between):
    """The line `new` prints when the two differ. Read by a person, so
    `agent-contract` §14 pins every sentence of it in a case."""
    if not between:
        # HEAD reaches nothing the reviewed commit does not, and the two are
        # still different commits: HEAD is BEHIND the record's own target, or
        # sits on another branch entirely. Neither reading below describes
        # that, and printing them would send the reader to a repair for a
        # state they are not in.
        return (
            f"round-record: {HEAD_MOVED} {DASH} the round read {reviewed[:7]}, "
            f"HEAD is {head[:7]}, and HEAD reaches no commit the round did "
            "not.\n"
            "  So nothing landed after the review on THIS tree: HEAD is "
            "behind the commit this record names, or on another branch. "
            "Neither of the usual two readings applies.\n"
            f"  Check that `--target` names the commit this tree's HEAD stood "
            "at when the round ran, and that you are in the tree the round "
            "reviewed. Nothing is refused here, and the record is written."
        )
    count = len(between)
```

⬜ 3 — the verb, in the same function, in the branch the block above leaves
for a non-empty listing:

```python
        f"is {head[:7]}, and {count} commit{'' if count == 1 else 's'} "
        f"{'stands' if count == 1 else 'stand'} between them.{listing}\n"
```

⬜ 5 — read the record only for the records the answer is about. In
`skills/code-review/scripts/chain_check.py`, between the loop that fills
`late` and the line that reads the cell:

```python
    if not late:
        return [], []
    began = item_began(rel)
    said = written_late_reason(reader, root, rel)
```

Needs a fix: yes — 🟡 1 and 🟡 2
Loses a record or crashes: no

Neither finding leaves a record outside the root and neither crashes anything.
🟡 1 is a refusal that withholds the repair it was built to offer, and 🟡 2 is
a printed line that is wrong in a reachable state. Both are text a person acts
on, and both keep every record where it is.

## Proof block

Opened and read in full: `skills/code-review/scripts/round_record.py`
(`written_late_cell`, `head_moved`, `head_moved_line`, `new`, `build`,
`close`, `seal`, `cell`, `escape`, `row`, `write_record`, `hiders_close`,
`open_hider`, `git`, `repo_of`, `where`),
`skills/code-review/scripts/chain_check.py` (`written_late`,
`written_late_reason`, `yes_or_no`, `read_record`, `WRITTEN_LATE` and the
constants around it), `templates/sdd-round.md`,
`skills/code-review/orchestration.md` §*And commit the record before
commissioning the fixes*, `docs/review-chain-spec.md` §*When the record was
written* and §*A finding located in a record is a correction*,
`tests/test_new_says_when_head_is_not_the_target.py`,
`tests/test_a_record_says_why_it_was_written_late.py`, the diff of
`tests/test_a_record_precedes_the_fixes_it_commissions.py`,
`tests/test_the_record_is_generated.py#test_the_field_rows_are_the_templates_in_the_templates_order`,
`seal/ledger.md`'s eleven changed rows,
`seal/ledger/1789296200-the-record-before-the-fix-sequence-has-no-arm.md`,
and the work item's `spec.md`, `plan.md`, `overview.md` and
`phases/phase-1.md` through `phases/phase-5.md`. The draft pull request body
was read as a claim.

Read but not committed anywhere: this session's scratchpad, for ⬜ 4 —
`phase1-result.txt` and the phase 1 measurement script.
