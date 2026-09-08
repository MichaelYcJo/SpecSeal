# 1788844127-the-reviewers-report-reaches-the-record-retyped — review round 1

| Field | Value |
|---|---|
| Target SHA | a50431b024018f210dd3b6bd5b8ec714a57612cf |
| Ran by | warden on claude-opus-5 |
| PR | 258 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | test_the_corpus_is_records_only (depth 1); test_a_directory_at_the_record_path_is_refused_as_a_directory (depth 1); test_a_directory_at_the_report_path_is_refused_as_a_directory (depth 1); test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file (depth 1) |
| Needs a fix | yes — 🟡 1 (a third reader judges 20 reports as records while two shipped documents say none does), 🟡 2 (nothing warns the reviewer that its report is now scanned by the identifier rule and the evidence checker), 🟡 3 (nothing carries the report into the commit, and `close` was never weighed as the gate) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Six targets, in the order the prompt set them.

1. **The permission itself, and whether it is written where it binds.** The
   branch adds a named exception to `agents/warden.md` rather than to
   `skills/agent-contract/SKILL.md`. Carried as a coordinate: §6's sentence
   that an exception *"is one agent's, and it is named in that agent's
   definition — never here."* Asked to `git diff` the contract, to judge
   whether the exception widens past the report file, and to decide whether
   it lands on the rule that actually forbade the write.
2. **Which checkout the report is written in** — `questions.md` Q1, carried as
   unresolved. Asked specifically what a report written into the work tree
   does to the diff the NEXT round reviews.
3. **The derived path**, attacked at named inputs: a trailing slash, relative
   against absolute, a round number disagreeing with the filename, a missing
   item directory, an empty report file, and a directory at the report path.
4. **The refusal message**, judged against the branch's own stated requirement
   that it name the path AND the convention that fills it.
5. **Every reader that walks `rounds/`, enumerated by construction** — with the
   implementer's count of two named as not to be taken. `routing.round_number`,
   `chain_check.py`, the release guard, `fold_ledger.py` and the round-record
   hook were named as candidates.
6. **The flag still winning**, and whether mutation genuinely covered the one
   case that cannot be seen red by reverting the tree.

Facts carried as executed by the orchestrator at the target SHA: the module at
7 passed exit 0, and ruff check and format at exit 0 over both changed `.py`
files. The implementer's six-of-seven-red and four-mutations-killed were
handed over labelled as its claims.

This round was also the first live trial of the instruction the branch adds:
it was told to write its report to `rounds/round-1-report.md` and to report a
failure to do so as a finding of the first order.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a third reader of `rounds/` selects records by directory membership, and two shipped documents say none does | `tests/test_a_finding_id_is_a_bare_integer.py:275` | **fixed** `1e35d5d` | fixed at 1e35d5d — ``; executed — the pathspec returns 204 paths, 20 of them reports, and all 20 parse as verdict tables and are judged as records |
| 🟡 2 | the report is tracked content now and nothing warns the reviewer that the identifier rule and the evidence checker reach it | `agents/warden.md` §Report | **fixed** `b76ce68` | fixed at b76ce68 — ``; executed — a report carrying one absolute user path fails `test_no_real_identifiers.py`, and contract §8 asks for exactly that string |
| 🟡 3 | nothing carries the report into the commit, and `close` — which runs after the record commit by design — was never weighed as the gate | `skills/code-review/SKILL.md` §And commit the record before commissioning the fixes | answered | `--report` defeats a `close` gate. The flag exists so a report can live off the conventional path, `new` records nowhere which path it read, so `close` has nothing to ask and refuses the runs the flag was added for. **Executed** — with the reviewer's paste-ready gate inserted after `close`'s target check, 36 of 41 cases in `tests/test_the_fixes_close_the_record.py` fail, because the suite's own helper writes the report outside the repository and passes `--report` on purpose. A gate that survives it needs `new` to record the path — a new record field, a template section and a checker, which is mechanism a fix pass does not add. Weighed at `b38d694` in `plan.md`; the residual stays in `overview.md` §*Not done* with the orchestrator named |
| ⬜ 4 | the acceptance row says `warden.md` "says the write happens in the clone"; it says the opposite | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | answered | corrected at `dd152e8` |
| ⬜ 5 | the spec says the clone rule needed no change; the change is an exception written under that rule | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | answered | corrected at `dd152e8` |
| ⬜ 6 | a directory at the conventional path is refused as "no report at", which does not say what is there | `skills/code-review/scripts/round_record.py:739` | **fixed** `dd152e8` | fixed at dd152e8 — ``; executed — the probe created a directory at the path and read the message back |

## Paste-ready fixes

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
```markdown
Three readers in the reference implementation took membership for record-ness.
Two raised `TypeError` on sorting two `None`s rather than failing an
assertion; the third judged twenty reports as records and said nothing at all,
which is the quieter half of the same defect — a reader that cannot name a
file it does not understand is worse than one that refuses it.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `--asked` carries the same defect `--report` had — a required path to a file that exists as prose in a spawn prompt, with 20 `round-N-asked.md` already in the tree | `questions.md` Q2 — an issue rather than a widening | the orchestrator |
| `round-N-asked.md` and `round-N-fixes.md` are named in no shipped document, while this change documents the third sibling | `questions.md` Q3 | the orchestrator |
| Whether `docs/flow.md`'s `#228` box is this branch's tick or the release's | `overview.md` §Not verified | the orchestrator |
