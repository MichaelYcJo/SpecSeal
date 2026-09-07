# 1788761915-a-record-states-what-nothing-reads — review round 2

| Field | Value |
|---|---|
| Target SHA | 88c7110 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 214 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | floor_and_fixes → round-1.md, round-2.md, bound_line, pytest; unshipped → round-1.md, unread_items, check_records, main, pytest; record_files → round-2.md, check_records, pytest |
| New units | test_a_multi_line_html_comment_is_an_aside_to_its_end (depth 1); test_a_name_after_a_multi_line_comment_closes_is_a_claim_again (depth 1); test_a_fence_the_record_never_closes_does_not_silence_what_follows (depth 1); test_a_tilde_fence_does_not_close_a_backtick_fence (depth 1); test_the_marker_exempts_a_line_a_never_closed_fence_held (depth 1); refuses_scandir (depth 1); test_a_records_directory_that_cannot_be_listed_is_named (depth 1); test_a_ledger_fragment_directory_that_cannot_be_listed_is_named (depth 1); test_a_missing_ledger_folder_is_still_an_empty_answer (depth 1); test_an_intermediate_floor_record_starts_a_count_walk_of_its_own (depth 1); test_the_count_walks_message_says_records_when_it_counted_two (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, **the verifying round**, spawned against `88c7110` with round 1 closed
— twelve findings fixed and two answered — and the fix diff `377cfab..88c7110`
as the primary surface.

**The prompt stated the bound rather than a round number**, as round 1's did:
this round either ends the run by opening nothing, or the record after it ends
it whatever that record finds. It said in as many words that there is no round
3 to defer to, so a finding raised here is either fixed in one pass or becomes
a filed issue.

Round 1's dispositions were handed over as inherited rather than re-derivable.
Findings 3 and 13 were named as **answered, not open** — 3 because the repair
needs `git ls-files` and `test_the_checker_asks_git_for_nothing` runs the
checker under an empty `PATH`, and 13 because the correction landed in a pull
request body this repository does not commit. What was left to this round on
both was whether the answer survives execution, not whether to reopen it.

The finding surface `close` had derived was handed over as the thing to judge:
one contract change — `floor_and_fixes`' return widened from two values to four
— and two product units, `unread_items` and `claim_lines`, both depth 1.

Five facts were handed over with coordinates attached and §5 applied to each,
including the fix pass's `593 passed`, its `208 names read`, its
`fold_ledger --check exit 0`, and its use of a monkeypatched read rather than
`chmod 000` under §13. **The prompt asked the round to assume at least one
mutation survivor the fix pass had not found**, on the grounds that the same
assumption had already been right once on this branch.

Five axes: each claimed fix against the finding AND against its class, with the
enumeration method judged rather than its result; finding 2's fix, which is the
branch's own subject, against a constructed chain where the two walks disagree
and one where the two grandfathering constants disagree; what the fixes broke —
a widened return, two new units and a changed summary line; the revert of
finding 3, against what actually executes; and the records arm's new
`N work items read · M unread` line, read as a person on a red build would read
it.

The assumption was right again. Two of round 1's twelve fixes close their
coordinate and leave the class open one step over, both in units the fix pass
widened, and two of the handed-over numbers do not hold at the target SHA.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the count walk runs from the earliest floor record only, and `stopping_floor` runs it from every record whose floor row reads `no` — round 1's 🔴 2 one floor record over | `skills/code-review/scripts/round_record.py:1103` | **fixed** `d09810c` | fixed at d09810c — `` — the count walk runs from every floor record and the reopening walk still from one, enumerated by construction over `stopping_floor`'s body and then a monotonicity question per walk: the reopening walk never stops, so the earliest start dominates; the count walk stops, which breaks that. The message names the record the firing walk started from, and `docs/review-chain-spec.md` carries the correction; executed: floor `no` · reopened without fixes · quiet, writing round 4 — `bound_line` printed `one reopening remains` while `stopping_floor` returned 1 error at `round-2.md` and 0 at `round-1.md` and `round-3.md` |
| 2 | 🟡 a multi-line HTML comment is an aside only on the line that opens it, so its continuation lines are read as claims | `skills/evidence-check/scripts/evidence_check.py:1885` | **fixed** `a58fffe` | fixed at a58fffe — `` — an aside is a region, not the line that opens it; executed: a two-line template comment naming `gone_helper` on the second line produced `NOT-IN-TREE … plan.md:4` — a false refusal at exit 2 |
| 3 | 🟡 a fence the record never closes silences every claim under it, and the arm says nothing | `skills/evidence-check/scripts/evidence_check.py:1885` | **fixed** `a58fffe` | fixed at a58fffe — `` — a fence nobody closes is malformed rather than a licence to read nothing; the `held` answer, no unit added. One correction to the reviewer's form: as written it lost the `NAME NOT IN TREE` exemption on a held line, filtered at the hold and pinned with a case seen red against the reviewer's version; executed: an unclosed ` ```python ` fence took a following `gone_helper` claim from refused to `0 names read`, no findings, exit 0; ` ``` ` and `~~~` share one flag and can close each other |
| 4 | 🟡 a records directory that cannot be listed reads as a work item with nothing in it, where an unreadable file is `UNREADABLE` and exit 2 | `skills/evidence-check/scripts/evidence_check.py:1797` | **fixed** `9e9f627` | fixed at 9e9f627 — `` — enumerated by construction over every way the file reads a directory (`os.walk`, `os.listdir`, `os.scandir`, `glob`): six sites, three fail-open. `record_files` is the opened one; `unshipped`'s `ledger/` listing is the same defect one directory up and strictly worse, fixed here through an optional `refused` list so no call site or case moved; `unread_items` moves a count rather than a finding and is deferred as a rider at its own line. The other two refuse more, not less. Each verdict is in `record_files`' docstring; executed as non-root: readable `rounds/` gave `([NOT-IN-TREE …], 1, 0)`, `chmod 000` gave `([], 0, 0)` and exit 0; pre-existing to the fix range, round 1 did not open it |
| 5 | ⬜ the eight-line `Both resolution arguments, not one` comment is pasted twice | `skills/evidence-check/scripts/evidence_check.py:2213` | **fixed** `9e9f627` | fixed at 9e9f627 — `` — the duplicated comment is gone; read: lines 2213-2221 and 2221-2229 are byte-identical; no behaviour |
| 6 | ⬜ the plural branch of the count-walk message has no case pinning it | `skills/code-review/scripts/round_record.py:1147` | **fixed** `d09810c` | fixed at d09810c — `` — the plural branch has a case; read: `test_two_quiet_rounds_after_the_floor_end_the_run` reaches `counted == 1` only; §14 asks the changed printed line to be pinned |
| 7 | ⬜ sixteen `seal/ledger.md` rows were re-anchored across the branch and not one `Checked` date moved | `seal/ledger.md` | **fixed** `2f2144c` | fixed at 2f2144c — `` — ten `seal/ledger.md` claims re-read at their coordinates before being dated; nothing was dated that was not opened, so the finding is closed whole rather than half; executed: over `8740da3..88c7110`, 16 rows changed content hash and the six `Checked` dates are byte-identical before and after; `CLAUDE.md` — *the `Checked` column holds the date somebody read the code* |
| 8 | ⬜ two handed-over facts do not hold at the target SHA | `seal/specs/1788761915-a-record-states-what-nothing-reads/rounds/round-1.md` | **fixed** `2f2144c` | fixed at 2f2144c — `` — the two rows that overstated no longer do; executed: the arm reads `218 names read`, not 208 (stale by one commit); `fold_ledger.py --check` exits 1 naming the three ungathered fragments, which is correct for a branch before its release — the fact is wrong, not the tool |
| 9 | ⬜ `N unread` mixes shipped history with the live case it was built for, and only ever grows | `skills/evidence-check/scripts/evidence_check.py:1751` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/216 | https://github.com/MichaelYcJo/SpecSeal/issues/216 |
| 10 | round 1's findings 1, 4, 5, 6, 7, 9, 10, 12, 13 and 14 — each fix opened against the finding and against its class | `seal/specs/1788761915-a-record-states-what-nothing-reads/rounds/round-1.md` | answered | each closes both; enumeration methods judged rather than their results — by signature for 🔴 1 (two optional arguments, one product call site), over the three `SKIP_DIRS` walks for 🟡 4 (only `tree_names` builds the corpus), over `unshipped` for 🟡 10 (the one place a file name becomes an id). Finding 3's revert left nothing behind and its four documents agree with the code; finding 13's three corrected sentences are true at `88c7110` |
| 11 | round 1's 🔴 2 and 🟡 11 — the coordinate closed, the class did not | `seal/specs/1788761915-a-record-states-what-nothing-reads/rounds/round-1.md` | answered | the meta-row: round 1's 🔴 2 and 🟡 11 closed their coordinate and not their class. Both classes are closed by this pass — 🔴 2's third instance by `d09810c`, 🟡 11's two by `a58fffe` |

## Paste-ready fixes

```python
# 1 — skills/code-review/scripts/round_record.py. `stopping_floor` is called
# on EVERY record, so every record whose floor row reads `no` starts a count
# walk of its own; reading the earliest alone printed `one reopening remains`
# over a round the gate refuses at an intermediate floor record. Returns a
# fifth value, because the message has to name the record whose count fires.
def floor_and_fixes(reader, earlier):
    seen = []
    for _k, path in earlier:
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return None, [], 0, False, None
        lines = reader.readable(text)
        rows = chain.table_rows(reader, lines)
        floor = chain.field(rows, chain.FLOOR)
        met = floor is not None and (
            chain.yes_or_no(reader.visible(floor).strip())[0] == chain.FLOOR_NO
        )
        needs = chain.field(rows, chain.NEEDS)
        reopened = needs is not None and (
            chain.yes_or_no(reader.visible(needs).strip())[0] == chain.FLOOR_YES
        )
        seen.append((path, met, reopened, chain.closed_with_a_fix(reader, lines, path)))

    floor_i = next((i for i, row in enumerate(seen) if row[1]), None)
    if floor_i is None:
        return None, [], 0, False, None
    fixes = [p for p, _m, _r, wrote in seen[floor_i + 1 :] if wrote]

    counted, counted_at = 0, None
    for i, (path, met, _r, _w) in enumerate(seen):
        if not met:
            continue
        spent, stopped = 0, False
        for _p, _m, reopened, wrote in seen[i + 1 :]:
            spent += 1
            if reopened or wrote:
                stopped = True
                break
        if not stopped and spent > counted:
            counted, counted_at = spent, path
    return seen[floor_i][0], fixes, counted, counted_at is not None, counted_at
```
```python
# 1, continued — in bound_line, the unpack and the count branch
    floor_at, fixes, counted, running, counted_at = floor_and_fixes(
        reader, earlier_records(routing, rounds, n)
    )
    ...
    if counted and running:
        if count_excused:
            return None
        quiet = "record" if counted == 1 else "records"
        started = os.path.basename(counted_at)
        return (
            f"round-record: {ENDS_THE_RUN} — {started} met the floor and the "
            f"{counted} {quiet} after it neither reopened the run nor closed "
            "on a fix, so the gate's count of round records after the floor "
            f"reaches {counted + 1} here. {chain.CAPPED_EXIT}"
        )
```
```python
# 1, continued — the case, into tests/test_the_record_is_generated.py beside
# test_two_quiet_rounds_after_the_floor_end_the_run
def test_an_intermediate_floor_record_starts_a_count_walk_of_its_own(repo):
    """`stopping_floor` is called on EVERY record, so a second record whose
    floor row reads `no` starts a count of its own. Reading the earliest
    alone printed `one reopening remains` at round 4 while the gate refused
    it at round-2.md (round 2, 🟡 1) — round 1's 🔴 2 one floor record over.
    """
    generator, reader = generator_module(), reader_module()
    routing = generator.load(check_module().ROUTING, "specseal_routing_second_floor")
    rounds = chain_of(
        repo,
        LATE,
        (1, "no", "yes — 🔴 1", CLOSED_ROW),
        (2, "no", "yes — 🟡 3", CLOSED_ROW),
        (3, "no", "no", CLOSED_ROW),
    )
    line = generator.bound_line(reader, routing, str(rounds), 4)
    assert line is not None and "this record ends the run" in line, line
    assert "round-2.md" in line, line
```
```python
# 2 and 3 — skills/evidence-check/scripts/evidence_check.py, claim_lines.
# An HTML comment was an aside on the line that OPENS it and a claim on every
# line after (round 2, 🟡 2), and a fence the file never closes took the rest
# of the record in silence (round 2, 🟡 3). The marker is remembered so ```
# and ~~~ cannot close each other, and what a never-closed fence took is read
# rather than lost: an unclosed fence is a malformed record, not a licence to
# read nothing.
def claim_lines(lines):
    out, opener, held, aside = [], None, [], False
    for number, line in enumerate(lines, 1):
        stripped = line.lstrip()
        mark = (
            "```"
            if stripped.startswith("```")
            else "~~~"
            if stripped.startswith("~~~")
            else None
        )
        if opener is not None:
            if mark == opener:
                opener, held = None, []
            else:
                held.append((number, line))
            continue
        if aside:
            if "-->" in line:
                aside = False
            continue
        if mark is not None:
            opener = mark
            continue
        if stripped.startswith("<!--"):
            if "-->" not in line:
                aside = True
            continue
        if NOT_IN_TREE in line:
            continue
        out.append((number, line))
    return sorted(out + held)
```
```python
# 4 — skills/evidence-check/scripts/evidence_check.py, record_files, and its
# one call site. `os.walk` swallows a directory it cannot list, so a work item
# whose `rounds/` is unreadable contributed no records and the run said
# nothing — ([], 0, 0) and exit 0, where an unreadable FILE is UNREADABLE and
# exit 2 (round 2, 🟡 4).
def record_files(directory):
    found, refused = [], []
    for dirpath, dirnames, filenames in os.walk(directory, onerror=refused.append):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                found.append(os.path.join(dirpath, name))
    return found, [error.filename for error in refused]
```
```python
# 4, continued — in check_records
        paths, unlistable = record_files(directory)
        for path in unlistable:
            findings.append(
                (
                    UNREADABLE_STATUS,
                    display_name(path, root),
                    "the records directory could not be listed",
                )
            )
        for path in paths:
```
```python
# 5 — skills/evidence-check/scripts/evidence_check.py:2221-2229: delete the
# second copy of the eight-line `Both resolution arguments, not one` comment.
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_a_record_states_what_the_tree_has.py tests/test_the_record_is_generated.py -q` | 141 passed |
| `./bin/test` on `test_a_row_points_by_content.py`, `test_gates_do_not_fail_open.py`, `test_the_printed_ledger_name_is_the_file_that_was_read.py` | 129 passed — `test_the_checker_asks_git_for_nothing` still green, so `7dac665` left no `subprocess` call behind |
| `./bin/evidence-check --strict .` at `88c7110` | exit 0 · `767 ok · 0 drifted · 0 broken · 0 external · 0 old-format` · records `3 work items read · 38 unread · 218 names read · 0 stamps read · 0 refused · 0 drifted · 0 external` |
| `python3 .github/scripts/fold_ledger.py --check` | exit 1 — three ungathered fragments named; correct for a pre-release branch, and not the exit 0 the handover claimed |
| probe: floor `no` · reopened without fixes · quiet, `bound_line` at round 4 vs `stopping_floor` at each floor record | printed `one reopening remains`; gate errors `{round-1: 0, round-2: 1, round-3: 0}` — finding 1 |
| probe: a two-line HTML comment naming a compound identifier on its second line | `NOT-IN-TREE … plan.md:4` — finding 2 |
| probe: an unclosed ` ```python ` fence with a claim beneath it | `0 names read`, no findings — finding 3 |
| probe: a `~~~` block quoted inside a ` ``` ` block, claim after it | read — the toggles re-pair for this shape; what is misread is the content between them |
| probe: `rounds/` at `chmod 000`, non-root, before and after | `([NOT-IN-TREE …], 1, 0)` → `([], 0, 0)`, exit 0 — finding 4 |
| three sample mutations of the fix pass's 24, one at a time with `tests/__pycache__` cleared | all three killed: `if not item` → `if False` (1 failed), `refused = len(records) - drifted` (1 failed), `if counted and running` → `if False` (1 failed). The extra survivor the prompt told me to assume is in un-mutated territory — findings 1 to 4 |
| `git diff 8740da3..88c7110 -- seal/ledger.md`, `Checked` cells before and after | six distinct dates, identical counts on both sides — finding 7 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2115` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1056` | round 1's 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1885` | round 1's 3 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:97` | round 1's 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2126` | round 1's 5 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1699` | round 1's 6 — fixed |
| round-1 | `tests/test_a_record_states_what_the_tree_has.py` | round 1's 7 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1017` | round 1's 8 — fixed |
| round-1 | `skills/evidence-check/SKILL.md:230` | round 1's 9 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1735` | round 1's 10 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1822` | round 1's 11 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1041` | round 1's 12 — fixed |
| round-1 | PR #214 body | round 1's 13 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:95` | round 1's 14 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
