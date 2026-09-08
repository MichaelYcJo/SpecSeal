# Round 1 — the reviewer's report reaches the record retyped (#228)

| | |
|---|---|
| Target SHA | `a50431b024018f210dd3b6bd5b8ec714a57612cf` |
| Base | `bcf48b8` (`release/v0.9.2`) |
| Reviewed from | a `git clone --no-local` of this repository at the target SHA |
| Broad gate | not yet — the full suite, the repository-wide lint and the typecheck are the orchestrator's, once, after the rounds settle |

This report was written to the path the branch under review invents, in the
work tree the orchestrator is in. The write worked. That is the first thing
the round was asked and it is answered above the findings, because everything
below rests on it.

## How the findings hang together

The change does one thing that nothing in the branch says out loud: **it turns
the reviewer's report into tracked repository content.** Three of the four
things that need a fix follow from that single fact, and the fourth is the
branch's own spec describing an implementation it did not build.

```
the report becomes a file in the tree
   ├─ 🟡 1  something already reads that directory as if every member were a
   │        record — and this branch writes down that nothing does
   ├─ 🟡 2  something already scans every tracked file, and nothing warns the
   │        reviewer that its report is now one of them
   └─ 🟡 3  nothing makes sure the report is in the commit at all

separately
   └─ ⬜ 4·5  spec.md describes a design the branch rejected
```

## 🟡 1 — a reader already calls a report a record, and this branch writes down that none does

**Location** — `tests/test_a_finding_id_is_a_bare_integer.py:275` (`committed_records`)

`skills/code-review/SKILL.md`'s new table row ends with *"every reader of
`rounds/` selects records by name"*, and `docs/review-handoff-protocol.md`
§Layout says *"Two readers in the reference implementation took membership for
record-ness"*. Both sentences are false at this SHA. There is a third reader
and it is not fixed:

```python
def committed_records():
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "seal/specs/*/rounds/round-*.md"],
        ...
    ).stdout.split()
    return out
```

`round-*.md` is git's pathspec and git has no way to say *and then a number* —
which is the sentence the two fixed readers carry in their own comments, one
file over. Nothing filters the result here.

**Executed**, at the target SHA, in the clone:

| | |
|---|---|
| paths the pathspec returns | 204 |
| of which `round-N-report.md` | 20 |
| of which `round-N-asked.md` · `round-N-fixes.md` | 20 · 13 |
| paths that parse as a verdict table under the record's own header | 170 |
| **reports among those 170** | **20 — every one of them** |

So `test_the_committed_records_only_lose_a_miscount` is judging 20 reports as
records today, and its `assert parsed > 100` is counting them. The module's own
docstring says the corpus was *"130 records that parse"*; it is 150 records and
20 reports now, and nothing in the file says which is which.

Two costs, and the second is the one that bites. The corpus assertion measures
a mixed population, so it no longer says what it claims. And a report whose `#`
cell is not a bare integer turns a repository-wide test red with a message
naming a file that is not a record — a red build pointing at the wrong
document, on a branch that touched neither.

The finding is not that the branch broke this. It is that the branch states a
protocol rule — *a record is selected by name, never by directory membership* —
counts the readers that violate it, gets the count wrong, and ships a skill
document asserting the repair is complete. `skills/agent-contract/SKILL.md` §12
is the rule: the finding names an instance, the fix is owed to every instance
the same cause produces.

## 🟡 2 — the report is a tracked file now, and nothing tells the reviewer what that costs

**Location** — `agents/warden.md` §Report (the new block) · `skills/code-review/SKILL.md` §Cross-session records (the new table row)

Both blocks say where the report goes and who commits it. Neither says that a
committed report is subject to the rules this repository applies to its own
tree.

Two of those rules reach it, and a reviewer following the contract walks into
the first one:

- `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* is
  enforced by `tests/test_no_real_identifiers.py`, which reads **every tracked
  text file**. A reviewer's `## Executed probes` table naturally records the
  command it ran, and `skills/agent-contract/SKILL.md` §8 tells the reviewer to
  write the absolute path out — *"write the path out … because the reader also
  fills in a name the command assigned itself"*. The contract asks for exactly
  the string the test refuses.

  **Executed**: with a `round-1-report.md` staged under this work item carrying
  one absolute user path in a probe row,
  `bin/test tests/test_no_real_identifiers.py -q` exits 1 and names the report
  by path and line. The 20 reports already in the tree pass only because their
  authors happened to write `/Users/x/`.

- `skills/evidence-check/scripts/evidence_check.py`'s records arm reads **every
  `.md` under a live work item** — `record_files` says so in its own docstring,
  *"Nothing here is specific to the review chain, so nothing here reads a file
  name to decide"*. So every compound identifier in a report is checked against
  the tree, and a name the tree does not carry is reported as `NOT-IN-TREE` at
  the pull request. That includes a symbol a paste-ready fix proposes to add.

Neither is a defect in the checkers. The defect is that the branch made the
report their input and told the reviewer nothing.

## 🟡 3 — nothing carries the report into the commit, and the gate that could is not the one that was rejected

**Location** — `skills/code-review/SKILL.md` §*And commit the record before commissioning the fixes* · `skills/code-review/scripts/round_record.py` (`close`)

`overview.md` §*Not done* is honest about this: *"Nothing enforces that the
report is committed with the record"*, mitigated by the two files sitting a
line apart in `git status`. The residual is the ticket's own failure shape:
`Fixes checked by` naming a round whose report nobody can open.

The rejection is sound as far as it goes. `new` runs before the record is
committed by design, so making `new` refuse an uncommitted report refuses every
correct run. But `new` is not the only place that opens the record.

`close` runs after the fixes have landed — which is after the record's own
commit, by the same section that rejected the `new` gate. At that moment the
report either is in git or is not, and a false positive is not constructible.
`plan.md` and `overview.md` both consider only `new`, so the cheaper gate was
never weighed.

This one is a design choice rather than a bug, and the smith may answer it with
grounds. What it cannot be is unconsidered.

## ⬜ 4 — the spec's acceptance row describes the opposite of what was built

**Location** — `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md`, §*User scenarios & acceptance*, last row

> then it names the path, says it returns it, and **says the write happens in
> the clone**

`agents/warden.md` says the write happens in the repository under review, and
gives the clone's unstated lifetime as the reason it does not happen in the
clone. The acceptance criterion asserts the rejected alternative. No case
checks it, which is why it survived.

## ⬜ 5 — the spec says the clone rule needed no change; the clone rule is where the change is

**Location** — the same file, last line

> The implementation takes the answer that needs no change to
> `agents/warden.md`'s clone rule.

The implementation adds an eleven-line named exception directly beneath that
rule, and `plan.md`'s constraint table calls it *"the wall — sharper than §6"*.
Three documents in one work item, and one of them says the wall was left
standing.

## ⬜ 6 — a directory at the conventional path is refused as "no report at"

**Location** — `skills/code-review/scripts/round_record.py:739` (`report_path`)

`os.path.isfile` answers False for a directory, so the run refuses — which is
right. The message then says *"no report at &lt;path&gt;"* about a path that has
something at it. A reviewer that created the directory instead of the file
reads a message telling it nothing is there.

Low cost, and named because the guard's whole purpose is to be readable by
somebody who typed no path.

## What was attacked and cleared

- **The permission is in the file where §6 says it belongs.** Executed:
  `git diff bcf48b8...a50431b -- skills/agent-contract/` is empty. The contract
  is untouched, and §6's *"An exception is one agent's, and it is named in that
  agent's definition — never here"* is the mechanism used rather than departed
  from.
- **The exception lands on the rule that actually forbade the write.** It sits
  in `agents/warden.md` §*Where you work*, immediately under *"and only there …
  you never write in it"*. The implementer's reading is correct: §6 forbids a
  durable **record**, and the report is not one. The clone rule is what forbade
  the file.
- **It does not widen.** *"Nothing else joins it: not a probe, not a fixture,
  not a file you patched to see whether a finding reproduces, and you do not
  commit it."* The three things the clone rule exists for are named and kept
  inside the clone.
- **The derived path is robust.** `build` resolves `--item` through
  `os.path.abspath` before `rounds` is joined, so a trailing slash and a
  relative path normalize to the same string, and a `--item` that is not a
  directory is refused two lines earlier. The round number in the filename is
  the same `--round` the record's own name comes from, so the two cannot be
  spelled apart.
- **The `isfile` guard covers what it claims.** Executed: forcing
  `if not os.path.isfile(path):` false fails
  `test_the_absence_names_the_path_and_the_convention`, exit 1.
- **The refusal names the path and the convention.** Executed, verbatim: *"no
  report at &lt;path&gt; and no --report. The reviewer writes its report there and
  returns the path (`agents/warden.md` §Report), and this reads it from where
  the reviewer left it rather than from a copy somebody retyped (#228).
  `--report &lt;path&gt;` names one written somewhere else"*. Path, convention,
  owner document, issue, and the way through — the stated requirement is met.
- **The flag still wins, and the claim that mutation covered it is true.**
  Executed: forcing `report_path`'s `if given is not None:` arm false fails
  `test_the_flag_still_wins_over_the_conventional_path`, exit 1.
- **Every other reader of `rounds/` selects by name.** Enumerated by
  construction over `os.listdir`, `os.scandir`, `glob`, `git ls-files` and
  `git ls-tree` in `hooks/`, `skills/`, `.github/scripts/` and `tests/`:
  `hooks/routing.py` `_ordered` · `rounds` · `stray_rounds` ·
  `rounds_unreadable`; `hooks/review-history-guard.py` (through
  `routing.rounds`); `chain_check.py` `round_records` · `stray_records` ·
  `rounds_unreadable` · the `Fixes checked by` walk;
  `round_record.py` `earlier_records`; and the two tests the branch names.
  `fold_ledger.py`, `gather_changelog.py` and `deferral_check.py` do not read
  `rounds/` at all. `evidence_check.py` `record_files` reads every `.md` under
  the work item deliberately and sorts nothing — that is 🟡 2, not a
  mis-sort.

## What a report in the work tree does to the next round's diff

Asked, and answered by reading rather than by execution.

The report is written **uncommitted** into the tree the smith is working in,
and `skills/code-review/SKILL.md` puts it in the record's own commit, which
lands before the fixes are commissioned. So the fix diff a verifying round is
handed does not carry it, and the branch diff a first round is handed does.

Nothing excludes a reviewer's own file from a later round's review target, and
nothing needs to: `agents/warden.md` already rules that a finding whose
`Location` is under `seal/specs/` is a ⬜ correction and never `Needs a fix`.
A reviewer can therefore read its own report as branch content but cannot
commission a fix to it. That is the right answer and it arrived by accident —
the rule predates this branch and no document connects the two.

The window that is genuinely open is between the reviewer's write and the
orchestrator's commit. During it the report is untracked in the smith's tree,
where a fix pass that stages broadly sweeps it into a fix commit and a branch
switch raises the worktree guard's dirty-tree question. That is 🟡 3 seen from
the other side.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a third reader of `rounds/` selects records by directory membership, and two shipped documents say none does | `tests/test_a_finding_id_is_a_bare_integer.py:275` | open | executed — the pathspec returns 204 paths, 20 of them reports, and all 20 parse as verdict tables and are judged as records |
| 🟡 2 | the report is tracked content now and nothing warns the reviewer that the identifier rule and the evidence checker reach it | `agents/warden.md` §Report | open | executed — a report carrying one absolute user path fails `test_no_real_identifiers.py`, and contract §8 asks for exactly that string |
| 🟡 3 | nothing carries the report into the commit, and `close` — which runs after the record commit by design — was never weighed as the gate | `skills/code-review/SKILL.md` §And commit the record before commissioning the fixes | open | read — `plan.md` and `overview.md` reject a gate in `new` only, for a reason that does not apply to `close` |
| ⬜ 4 | the acceptance row says `warden.md` "says the write happens in the clone"; it says the opposite | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | open | read — `agents/warden.md` §Where you work names the repository under review |
| ⬜ 5 | the spec says the clone rule needed no change; the change is an exception written under that rule | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | open | read — `plan.md` calls the clone rule "the wall" |
| ⬜ 6 | a directory at the conventional path is refused as "no report at", which does not say what is there | `skills/code-review/scripts/round_record.py:739` | open | executed — the probe created a directory at the path and read the message back |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_reviewers_report_reaches_the_record.py -q`, in a clone at the target SHA | 7 passed, exit 0 |
| the same module, with `report_path`'s `if given is not None:` arm forced false | exit 1 — `test_the_flag_still_wins_over_the_conventional_path` |
| the same module, with `report_path`'s `if not os.path.isfile(path):` guard forced false | exit 1 — `test_the_absence_names_the_path_and_the_convention` |
| `report_path` called directly: nothing at the derived path · a directory at it · an empty file at it · an empty `--report` · `--report` naming a directory | refuses on the first two with the same message · returns the path for the empty file and `read_text` hands back `''` · returns `''` for the empty flag · returns the directory and `read_text` refuses with `Is a directory` |
| `git ls-files "seal/specs/*/rounds/round-*.md"` at the target SHA, then each path through the generator's own `table_body` | 204 paths · 20 `-report.md`, 20 `-asked.md`, 13 `-fixes.md`, 151 records · 170 parse as a verdict table · all 20 reports are among them |
| `bin/test tests/test_no_real_identifiers.py -q` with a `round-1-report.md` staged under this work item carrying one absolute user path | exit 1 — `test_only_fixture_user_paths` names the report by path and line |
| `evidence_check.py --strict --ledger seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md .` | exit 0 — 14 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `git diff bcf48b8...a50431b -- skills/agent-contract/` | empty — the contract is untouched |
| **this report itself**, staged in the clone, through both repository-wide readers: `bin/test tests/test_no_real_identifiers.py -q` and `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q` | exit 0 and exit 0 — 🟡 1 and 🟡 2 are latent here, not red. This report was written to avoid both, which is the point: nothing told it to |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `--asked` carries the same defect `--report` had — a required path to a file that exists as prose in a spawn prompt, with 20 `round-N-asked.md` already in the tree | `questions.md` Q2 — an issue rather than a widening | the orchestrator |
| `round-N-asked.md` and `round-N-fixes.md` are named in no shipped document, while this change documents the third sibling | `questions.md` Q3 | the orchestrator |
| Whether `docs/flow.md`'s `#228` box is this branch's tick or the release's | `overview.md` §Not verified | the orchestrator |

## Paste-ready fixes

🟡 1 — `tests/test_a_finding_id_is_a_bare_integer.py`, replacing `committed_records`:

```python
def committed_records():
    """`seal/specs/*/rounds/round-*.md` git carries — the RECORDS among them.

    `round-*.md` is git's pathspec and git has no way to say "and then a
    number", so it also returns the three files the review chain writes beside
    a record: `round-N-report.md`, `round-N-asked.md`, `round-N-fixes.md`.
    Measured at a50431b: 204 paths, of which 151 are records and 20 are
    reports -- and every one of those 20 parses as a verdict table under this
    module's own header, so the corpus below was judging reports as records.
    A record is selected by name (`docs/review-handoff-protocol.md` §Layout),
    and `routing.round_number` is the one place that rule lives.
    """
    generator = generator_module()
    routing = generator.load(generator.chain.ROUTING, "routing_for_the_id_corpus")
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "seal/specs/*/rounds/round-*.md"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return [p for p in out if routing.round_number(os.path.basename(p)) is not None]
```

The module imports `re`, `shutil`, `subprocess` and `time` but not `os`; add it
to the import block. `assert len(paths) > 100` still holds — 151 records at
this SHA — and `assert parsed > 100` becomes a count of records only.

🟡 1 (second half) — `docs/review-handoff-protocol.md` §Layout, the sentence
that states the count:

```markdown
Three readers in the reference implementation took membership for record-ness.
Two raised `TypeError` on sorting two `None`s rather than failing an
assertion; the third judged twenty reports as records and said nothing at all,
which is the quieter half of the same defect — a reader that cannot name a
file it does not understand is worse than one that refuses it.
```

🟡 2 — `agents/warden.md` §Report, after the paragraph that names the path:

```markdown
**The report is tracked content once the orchestrator commits it, so the
rules this repository applies to its own tree apply to your prose.** Two of
them reach it. `CLAUDE.md` §*Repo rule — no real identifiers in examples or
fixtures* is enforced over every tracked file, and §8 of the contract is what
told you to write your clone's absolute path out — so the probe row that
records the command you ran is the row that turns
`tests/test_no_real_identifiers.py` red at the pull request. Name paths
relative to the repository root, and spell a user path `/Users/x/`. And the
evidence checker reads every `.md` under a live work item, so a compound
identifier your report names — including one a paste-ready fix proposes to
add — is reported as a name the tree does not carry unless the line says so.
```

🟡 3 — `skills/code-review/scripts/round_record.py`, in `close`, immediately
after the `target` existence check:

```python
    # The report the record was written from has to be in git by now. `new`
    # cannot ask -- it runs BEFORE the record is committed, by design, so a
    # gate there refuses every correct run. `close` runs after the fixes have
    # landed, which is after the record's own commit, so by here the report
    # either is tracked or was left behind. A record committed without it
    # leaves `Fixes checked by` pointing at a round whose report nobody can
    # open, which is the audit line the record exists to hold (#228).
    report = os.path.join(rounds, REPORT_NAME.format(n=args.round))
    if git(root, "ls-files", "--error-unmatch", "--", report) is None:
        raise Refused(
            f"git does not carry {report} at this commit. The record was "
            f"written from that report, and `{chain.CHECKED_BY}` names this "
            "round to a reader who then has nothing to open. Commit it beside "
            f"round-{args.round}.md -- it sits in the same directory, a line "
            "away in `git status` (`skills/code-review/SKILL.md` §*And commit "
            "the record before commissioning the fixes*)"
        )
```

`close` already unpacks `root` and `rounds` from `where(args)` on its first
line, and `git()` returns `None` on a non-zero exit, which is what
`--error-unmatch` produces for an untracked or absent path.

Needs a fix: yes — 🟡 1 (a third reader judges 20 reports as records while two shipped documents say none does), 🟡 2 (nothing warns the reviewer that its report is now scanned by the identifier rule and the evidence checker), 🟡 3 (nothing carries the report into the commit, and `close` was never weighed as the gate)
Loses a record or crashes: no

## Proof

**[executed]**, in a `git clone --no-local` of this repository at
`a50431b024018f210dd3b6bd5b8ec714a57612cf`, every command's exit code read
directly:

- `bin/test tests/test_the_reviewers_report_reaches_the_record.py -q` — 7 passed, exit 0
- the same module under two mutations of `report_path` — one failure each, exit 1 each
- `bin/test tests/test_no_real_identifiers.py -q` with a staged probe report — exit 1, the report named
- `evidence_check.py --strict --ledger seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md .` — exit 0
- `report_path` driven directly over five inputs; the corpus measured through the generator's own `table_body`
- `git diff bcf48b8...a50431b -- skills/agent-contract/` — empty

The probe scripts were deleted and the clone's tree is clean at the target SHA.

**[read]** — files opened at the target SHA:
`agents/warden.md` · `skills/agent-contract/SKILL.md` §6 §8 §9 §12 ·
`skills/code-review/SKILL.md` · `docs/review-handoff-protocol.md` ·
`skills/code-review/scripts/round_record.py` ·
`skills/code-review/scripts/chain_check.py` · `hooks/routing.py` ·
`hooks/review-history-guard.py` · `hooks/root-migrate.py` ·
`skills/evidence-check/scripts/evidence_check.py` ·
`skills/verify/scripts/deferral_check.py` · `.github/scripts/fold_ledger.py` ·
`.github/scripts/gather_changelog.py` · `bin/test` ·
`tests/test_the_reviewers_report_reaches_the_record.py` ·
`tests/test_a_finding_id_is_a_bare_integer.py` ·
`tests/test_no_real_identifiers.py` · `tests/test_the_reopening_is_one.py` ·
`tests/test_chain_check_at_the_pull_request.py` ·
`tests/test_the_set_a_work_item_always_has.py` ·
`tests/test_the_last_rounds_fixes_are_checked.py` ·
`tests/test_handoff_outlives_the_merge.py` · `CLAUDE.md` · `seal/config.md` ·
this work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`,
`routing.md`, `changelog.md`

**[unverified]** — the full suite, the repository-wide lint and the typecheck,
and the unscoped `evidence_check.py --strict` read of `seal/ledger.md`. All
four are the orchestrator's, after the rounds settle. Answerer: the
orchestrator.

No earlier round exists, so no coordinate was carried in. No probe file
survives this round.
