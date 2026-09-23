# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — review round 2

| Field | Value |
|---|---|
| Target SHA | 0d3a9fb4f76f42cba62de6e3643ec37311e73761 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 541 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `43afbc1e5877ea1ba8509b2ada6779ea7316f9e4..db292bfbb01cae187f801617003558cc91f42c32`, 2 commits |
| Contract changes | none |
| New units | same_run (depth 1); test_a_re_seal_at_the_same_commit_against_another_base_keeps_both (depth 1) |
| Needs a fix | yes — 🟡 1 (a same-commit re-seal erases the entry it replaces, base included, and four carrier sentences say a second run never erases the first; close it by keying the replace on commit AND base, or by rewriting the four sentences and A9 with grounds) |
| Loses a record or crashes | no — nothing found writes outside `seal/specs/` or raises; 🟡 1 drops one entry inside a cell the generator rewrites on purpose, a record kept short and not a record lost, and the run that wrote it is still named by the entry that replaced it |

- [x] Pass

## What this round was asked

Round 2 of the review record's shape, the verifying round at round 1's fixes: the range `83988abd..21b8d61e` on `fix/503-the-report-the-record-and-the-cells-disagree-on-one-format`, three commits, plus the record commit that closed round 1, against the branch's base `0b8dc4b2`. It asked whether the three 🟡 are closed as the record says — `kept_broad_gate` is the one cell-writing path for `seal` and `close --broad-gate` and a `close` at HEAD before the fix replaced a held run; the ninth carrier of the one-run wording is rewritten and all nine are pinned as gone/stands pairs that go red when one old sentence is restored; a repeated header row is skipped by both `table_body` and `chain_check.verdict_table` and the second table's real rows are carried — and whether the five ⬜ went where the table says: both enders named, the running walk's sentence, the aggregate sourced, the module's count stated, a same-commit re-seal replacing its entry. It also asked whether the seven mutations reproduce, whether the 29 re-read ledger rows and A9–A11 state what the landed code does, and whether the fix range touched anything the three findings did not name. A round that opens nothing needing a fix does not consume the cap.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a re-seal at the commit the newest entry names erases that entry, base included, while `agents/sealer.md` (twice), `docs/review-chain-spec.md` and the `broad-gate.md` comment say a second run never erases the first; the sealer's own binding is commit AND base | `skills/code-review/scripts/round_record.py:376-381`, `:4259-4261`; `agents/sealer.md:141`, `:186-188`; `docs/review-chain-spec.md:341-343`; `templates/sdd-round.md:39` | **fixed** `fb960e6c` | fixed at fb960e6c — the report's paste-ready fix as given: `same_run(entry, value)` decides the replace on commit AND base (SHA words by prefix, the rest exactly), and `kept_broad_gate` replaces the newest entry only when `same_run(entries[0], value)`; the new case `test_a_re_seal_at_the_same_commit_against_another_base_keeps_both` seen red at `43afbc1e` (the cell kept one entry and lost the first base) then green; the existing case reshaped to a third seal against the same base to pin the replace; the template sentence says so; A9 restated with `same_run` and the case as anchors. The paperwork row: A11 corrected in the fragment with a dated note, and round 1's 🟡 2 grounds cell corrected by the orchestrator at `e101abac`. The orchestrator re-ran at `db292bfb`: four modules 263 passed, tree-wide ruff clean, `evidence-check --strict` exit 0, CI-form sweep one excused; read — the four sentences against the replace at `:381`; executed — m2 shows the replace is what the case pins, and the case's own shape is a different base |
| ⬜ 2 | the `skills/verify/SKILL.md` stands phrase `earlier run` stood in that file at `0b8dc4b2` under §Counterfeits, so the pair's present half pins nothing of the rewrite for that carrier | `tests/test_the_broad_gate_cell_keeps_every_run.py:54-58`; `skills/verify/SKILL.md:456`, and `:783` at the base | **fixed** `fb960e6c` | fixed at fb960e6c — `GATE_CARRIERS`' stands phrase for `skills/verify/SKILL.md` is now `; earlier run: <sha> vs base <sha>`, absent at `0b8dc4b2` and present once at the target; restoring the old seal-block line turns the stands half red; executed — the phrase is present at the base for this carrier alone; read — the file's new line carries `; earlier run: <sha> vs base <sha>` |
| ⬜ 3 | `kept_broad_gate`'s docstring says the caller resolved the value; `close --broad-gate` never resolves its flag | `skills/code-review/scripts/round_record.py:367-368`, `:4554` | **fixed** `fb960e6c` | fixed at fb960e6c — `kept_broad_gate`'s docstring says `seal` has already refused a flag that does not resolve and `close --broad-gate` never resolves its flag, so a value with no SHA-shaped word is written as typed and left for `chain_check.broad_gate` to report; read — no SHA check in `close` over `:3824-4182`; `seal` refuses at `:4467-4472`; behaviour unchanged from before the fix |
| ⬜ | A11 and round 1's 🟡 2 grounds say nine documents are pinned; `GATE_CARRIERS` pins eight, and the ninth carrier is the comment `new_broad_gate_file` writes, unpinned | `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:22`; `seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/rounds/round-1.md:36` | answered — corrected at e101abac | read — `spec.md:187-193` lists the comment as the seventh carrier; executed — no test greps its wording |
| 🟢 | round 1's 🟡 1 — `kept_broad_gate` is the one cell-writing path for `seal` and `close --broad-gate`, and the template and orchestration say so | `skills/code-review/scripts/round_record.py:347-385`, `:3936-3943`, `:4499`; `templates/sdd-round.md:39`; `skills/code-review/orchestration.md:535-539` | verified | executed — m1 and m3 red at their cases, the close module green; read — no other writer of the cell |
| 🟢 | round 1's 🟡 2 — the ninth carrier in `agents/warden.md` §Role is rewritten and the eight documents are pinned as gone/stands pairs, each gone sentence the carrier's own at `0b8dc4b2` | `agents/warden.md:320-325`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | verified | executed — every gone sentence present at the base and absent at the target, every stands phrase present at the target; m6 red on the gone half; ⬜ 2 and the correction narrow the claim, not the fix |
| 🟢 | round 1's 🟡 3 — a repeated header row is skipped by `table_body` and by `chain_check.verdict_table`, and the rows under it are carried | `skills/code-review/scripts/round_record.py:1128-1139`; `skills/code-review/scripts/chain_check.py:1574-1580` | verified | executed — m4 and m5 red at their cases; read — the generator compares exactly and the checker casefolded, and the generator's first-header refusal makes the difference unreachable |
| 🟢 | round 1's ⬜ 4, 6 and 7 — both enders named, the aggregate sourced to #437 in both files, the three-places module says what it counts | `agents/warden.md:466-469`; `docs/review-chain-spec.md:979-985`; `skills/code-review/SKILL.md:329-334`; `tests/test_the_report_standard_is_one_in_three_places.py:1-6` | verified | read — the diff at each coordinate |
| 🟢 | round 1's ⬜ 5 — a running walk of two reports the gate's refusal; `reaches 2` on the remaining branch is right by construction | `skills/code-review/scripts/round_record.py:2136-2153`; `floor_and_fixes` | verified | executed — m7 red at `test_the_count_walks_message_says_records_when_it_counted_two`; read — `fires` admits a running walk only at `spent >= 1` |
| 🟢 | round 1's ⬜ 8 — the same-commit replace is implemented and pinned as the record says; whether it should be is 🟡 1 | `skills/code-review/scripts/round_record.py:376-381`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2555-2577` | verified | executed — m2 red at the replace case and green at the different-commit case |
| 🟢 | the fix range touched nothing outside the eight findings and the ledger re-reads; the 29 re-read rows and A9, A10 state what the landed code does | `git diff --stat 83988abd..21b8d61e`, fifteen files; `seal/ledger.md`; `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:20-21` | verified | read — every hunk maps to a finding; executed — `evidence-check --strict` 1622 ok, 0 drifted, 0 broken; `seal`'s `raise Refused` sites counted at six |
| 🟢 | the new units as code — `kept_broad_gate`, the two header skips, the `bound_line` guard, `ROOT`, `GATE_CARRIERS`, `flat` and the four cases — are correct, with 🟡 1, ⬜ 2 and ⬜ 3 as the exceptions above | `skills/code-review/scripts/round_record.py:347-385`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | verified | executed — the six modules, 506 passed; read — `flat` collapses whitespace so a wrapped sentence matches, `ROOT` resolves from the test file |
| 🟢 | round 1's nine 🟢 rows stand; the three the fix range touched (phases 1, 2 and 4) were re-derived by the modules above | `rounds/round-1.md` | confirmed | executed — the generator, checker, close and seal modules at the target; read — the other six cover code the fix range did not touch |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict` over the tree the sealer stands on, taken once after the rounds settle | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; the hand-back labelled it `unverified`; this round's `evidence-check` and per-file ruff are probes over the clone, not the gate |

## Paste-ready fixes

```python
def same_run(entry, value):
    """Whether `entry` and `value` record one run: the same commit AND the
    same base. A SHA-shaped word is compared by prefix, so an abbreviated
    entry and a full-length flag agree; every other word exactly. Two runs
    at one commit against different bases are two comparisons —
    `agents/sealer.md` binds a seal to both halves — and both are kept.
    """
    a, b = entry.split(), value.split()
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if chain.SHA_RE.fullmatch(x) and chain.SHA_RE.fullmatch(y):
            if not (x.startswith(y) or y.startswith(x)):
                return False
        elif x != y:
            return False
    return True
```
```python
    entries = held.split(EARLIER_RUN)
    if same_run(entries[0], value):
        entries = entries[1:]
    if not any(chain.SHA_RE.search(e) for e in entries):
        return value
    return EARLIER_RUN.join([value, *entries])
```
```python
    **A run the newest entry already records — the same commit against the
    same base — replaces that entry rather than standing beside it** (round
    1's ⬜ 8, narrowed by round 2's 🟡 1). It is the same claim about the
    same comparison — the sealer re-run over an unchanged checkout — and
    two entries for one claim would make the count of entries stop being
    the count of runs. A run at that commit against ANOTHER base is another
    comparison and is kept behind the new entry like any earlier run, which
    is what `agents/sealer.md` and the `broad-gate.md` comment promise. The
    comparison is by prefix per SHA-shaped word, so an abbreviated entry and
    a full-length flag name one commit; nothing here asks git.
```
```python
    code, out = run_seal(repo, f"{second} against base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_a_same_commit_re_seal", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{second} against base{generator.EARLIER_RUN}{first} against base"
    ), cell
    assert cell.count(second) == 1, "the same commit was entered twice"
```
```python
def test_a_re_seal_at_the_same_commit_against_another_base_keeps_both(repo):
    """Round 2's 🟡 1. The seal is the commit AND the base (`agents/sealer.md`
    §Bind the result to a tree state), so a run at one commit against a
    moved base is a second comparison and stays beside the first rather
    than replacing it — the erasure #174 was filed on, one field narrower."""
    _one, two = settled_item(repo)
    sha = short(repo, "HEAD")
    assert run_seal(repo, f"{sha} against base")[0] == 0
    code, out = run_seal(repo, f"{sha} against origin/base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_another_base", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{sha} against origin/base{generator.EARLIER_RUN}{sha} against base"
    ), cell
```
```markdown
and a run the newest entry already records — the same commit against the same base — replaces that entry rather than duplicating it, while a run at that commit against another base is kept behind the new entry as any earlier run is
```
```python
    (
        ("skills", "verify", "SKILL.md"),
        "; earlier run: <sha> vs base <sha>",
        "one SHA with the base it was compared against",
    ),
```
```python
    nothing here asks git: `seal` has already refused a flag that does not
    resolve, and `close --broad-gate` never resolves its flag, so a value
    with no SHA-shaped word is written as typed and left for
    `chain_check.broad_gate` to report at the pull request.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_record_is_generated.py tests/test_chain_check_at_the_pull_request.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_the_report_standard_is_one_in_three_places.py -q` in the clone at `0d3a9fb4` | `506 passed in 343.29s`; the exit code was read through a pipe and is not claimed |
| m1 — `close` builds the cell from `args.broad_gate` alone (`kept_broad_gate(...)` replaced by the flag) | `test_close_broad_gate_keeps_a_run_the_cell_already_holds` 1 failed, exit 1 |
| m2 — `entries = entries[1:]` replaced by `pass` (the same-commit rule dropped) | `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry` 1 failed, exit 1; `test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest` 1 passed, exit 0 |
| m3 — `kept_broad_gate` returns `value` unconditionally | seal module `-k re_seal` 3 failed, 3 passed, exit 1; the close case 1 failed, exit 1 |
| m4 — `table_body`'s `!= header` clause removed | `test_a_second_tables_header_under_a_subheading_is_not_a_verdict_row` 1 failed, exit 1 |
| m5 — `verdict_table`'s casefolded header skip replaced by `if False:` | `test_a_repeated_header_row_is_not_a_verdict_row` 1 failed, exit 1 |
| m6 — `skills/verify/SKILL.md` given back *one SHA with the base it was compared against* | `test_no_carrier_still_describes_the_cell_as_one_run` 1 failed, exit 1; `test_every_carrier_says_the_cell_holds_one_entry_per_run` 1 passed, exit 0 |
| m7 — `bound_line`'s guard back to `if not running:` | `test_the_count_walks_message_says_records_when_it_counted_two` 1 failed, exit 1 |
| after every mutation `git checkout --` on the file; `git status --porcelain` in the clone | clean |
| a script over `git show 0b8dc4b2:<carrier>` and `flat` for each `GATE_CARRIERS` tuple: gone sentence at base / at target, stands phrase at base / at target | gone: present at base and absent at target for all eight; stands: present at target for all eight, and present at the base for `skills/verify/SKILL.md` alone |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone, exit read directly | exit 0 — `total: 1622 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm 0 refused, 0 drifted |
| `uvx ruff check` and `uvx ruff format --check` over the eight `.py` files the fix range edited, exits read directly | exit 0 and exit 0 |
| `awk` count of `raise Refused` inside `seal` at `0b8dc4b2`, `e3cc83c9` and the target | six sites at each (the seventh hit is the docstring sentence that names the count) |
| `grep -rn "newest first\|earlier run\|new_broad_gate_file" tests/` | three docstrings and one unrelated line; nothing pins the `broad-gate.md` comment |
| this report through `round_record.py new --round 2 --target 0d3a9fb4… --baseline 0b8dc4b2` in the clone, then `evidence-check --strict` with the report in place; the record it wrote and its reach-back into `round-1.md` were undone in the clone (the worktree's record is the orchestrator's to write) | `new` exit 0 — `Pass` unticked over 🟡 1, both terminal lines copied as values, 14 verdict rows and all eight fenced blocks carried, the bound printed as `one reopening remains`; `evidence-check` exit 0, 1622 ok, 0 refused with the report's names read |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` at the tree the sealer stands on | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:3883`, `:4067`, `templates/sdd-round.md:39`, `skills/code-review/orchestration.md:535` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md:320-322`; `plan.md:74-77` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1086-1090`, `skills/code-review/scripts/chain_check.py:1569-1583` | round 1's 🟡 3 — fixed |
| round-1 | `agents/warden.md:466` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2093-2102` | round 1's ⬜ 5 — fixed |
| round-1 | `docs/review-chain-spec.md:982-984`, `skills/code-review/SKILL.md:332-334` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_the_report_standard_is_one_in_three_places.py` | round 1's ⬜ 7 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:4441-4444` | round 1's ⬜ 8 — fixed |
| round-1 | `round_record.py:2003-2016`, `:2081-2092`; `docs/review-chain-spec.md:1517-1518` | round 1's 🟢 — verified |
| round-1 | `chain_check.py:1180-1223`, `:1529-1533`; `round_record.py:1006-1032`, `:1035-1048`, `:1219-1224`, `:2119-2125`, `:2215` | round 1's 🟢 — verified |
| round-1 | `chain_check.py:1862-1894` against `:2641-2648`; `evidence_check.py:2065-2103` | round 1's 🟢 — verified |
| round-1 | `round_record.py:4313-4319`, `:4441-4444`; `chain_check.py:3684`, `:3723`, `:4012-4021` | round 1's 🟢 — verified |
| round-1 | `agents/warden.md:423-441`, `:443-453`, `:464-471`; `tests/test_the_report_standard_is_one_in_three_places.py` | round 1's 🟢 — verified |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:100-142` | round 1's 🟢 — verified |
| round-1 | `overview.md:26-32` | round 1's 🟢 — verified |
| round-1 | `round_record.py:1397`, `:1973-1975`; `templates/sdd-round.md` diff; `chain_check.py:4012-4021` | round 1's 🟢 — verified |
| round-1 | `seal/specs/1790174138-…/survivors.md:17-20` | round 1's 🟢 — verified |
| round-1 | the last record's `Broad gate` cell | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
