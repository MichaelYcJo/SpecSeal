# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — review round 1

| Field | Value |
|---|---|
| Target SHA | e3cc83c90d104c742f06d07d3878c282044e30e0 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 541 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (`close --broad-gate` replaces a held run), 🟡 2 (the ninth carrier and the missing pin), 🟡 3 (a repeated header row copied as a verdict row) |
| Loses a record or crashes | no — nothing found writes outside `seal/specs/` or raises; 🟡 1 erases one entry inside a cell the generator itself rewrites, which is a record kept short rather than a record lost |

- [ ] Pass

## What this round was asked

Round 1 of the review record's shape, the whole branch `fix/503-the-report-the-record-and-the-cells-disagree-on-one-format` against work item 0's sealed tip `0b8dc4b2` (the branch's base until #537 squashes into `release/v0.15.0`): eight tickets in five phases plus #366's three cases as a sixth, #218, #505 and #382, #436 and #217, #174, #503 and #437 with the `&lt;!--` rule. Stage 1 asked whether each phase builds what `spec.md`'s scenarios say, whether the five divergences `overview.md` records were the right call, and whether the five points inherited from work item 0 (`plan.md` Alternatives) still hold of the landed code. Stage 2 asked five things:

- whether `section_end` is one definition in `chain_check.py` that `round_record.py` delegates to, whether all three readers (`section_body`, `swallowed`, `verdict_table`) take it, and whether a report with six `###` paste-ready entries reaches the record with all six
- whether the `Broad gate` cell's newest-first list is read correctly by `broad_gate`, `direct_seal` and `seal`'s descends-from refusal on both homes, and whether a first seal is byte-identical to before
- whether the reviewer standard in `agents/warden.md`, `skills/code-review/SKILL.md`, `docs/review-chain-spec.md` and `templates/sdd-round.md` is one text pinned to itself, and whether the skeleton run through `new` produces a record without refusal
- whether the 38 mutations tabled in the phase files and the ledger fragment's A1–A8 are true of the landed code, and whether the 584-sequence differential reproduces 16 → 0
- whether the four `survivors.md` rows excuse what they quote on grounds that hold, and whether the `#436` arm's `RANGE_FROM` grandfathering excuses exactly what the record-order arm would

The hand-back labelled the broad gate unverified; the sealer answers that after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `close --broad-gate` is the second writer of the `Broad gate` cell and still replaces a run the cell already holds; three documents say it writes "the same cell" | `skills/code-review/scripts/round_record.py:3883`, `:4067`, `templates/sdd-round.md:39`, `skills/code-review/orchestration.md:535` | open | read — `gate = cell(BROAD_GATE, args.broad_gate)` is built from the flag alone and written over the row; `seal` keeps the held run at `:4441-4444`; reachable through the header-only fix table `seal`'s docstring names and through a partial table, since `Pass` ticks only when no row is open |
| 🟡 2 | a ninth carrier of the one-run wording stands in the reviewer's own file, and no test pins any of the eight the branch rewrote | `agents/warden.md:320-322`; `plan.md:74-77` | open | executed — `grep -rn "the SHA it ran at"` over `agents docs skills templates` hits this line alone outside the rewritten files; `grep -rn "newest first\|earlier run" tests/` hits one docstring; read — the plan says a pin makes the class red and A16 pins something else |
| 🟡 3 | a second table's header row under a `###` inside `## Verdicts` is copied into the record as a verdict row at exit 0, and the checker reads the same shape on a record | `skills/code-review/scripts/round_record.py:1086-1090`, `skills/code-review/scripts/chain_check.py:1569-1583` | open | executed — the probe in §Executed probes; read — `table_body` drops separators only and `finding_number` admits `#` as a no-id cell; `verdict_table` skips separators only |
| ⬜ 4 | "a section ends at the next `##`" names one of the two enders | `agents/warden.md:466` | open | read — `section_end` ends at own level or shallower, so a `#` ends it too |
| ⬜ 5 | a running walk that already reached two prints "reaches N+1 here" where the gate already refuses at the floor record with N — #218's sibling | `skills/code-review/scripts/round_record.py:2093-2102` | open | read — `fires` at `:2013` admits a running walk of two; the stopped branch at `:2081` is the sentence for it and the running branch falls past it; verdict unchanged |
| ⬜ 6 | "Measured over the 71 work items …" states an aggregate without source or tree state; 25 records exist at the target SHA | `docs/review-chain-spec.md:982-984`, `skills/code-review/SKILL.md:332-334` | open | read — the number is #437's; executed — 25 committed round records at `e3cc83c9` |
| ⬜ 7 | the module named for three places pins four carriers | `tests/test_the_report_standard_is_one_in_three_places.py` | open | read — `CARRIERS` has four entries |
| ⬜ 8 | a re-seal at the commit the cell already names appends a duplicate entry; none of `seal`'s refusals is *already holds this run* | `skills/code-review/scripts/round_record.py:4441-4444` | open | read — the keep is keyed on a held SHA, not on a different one; a question for the owner, not a defect by the cell's definition |
| 🟢 | phase 1 (#218): a stopped walk that reached two fires with `running` false, `bound_line` prints the gate's refusal, the inner `break` is load-bearing, the exits table matches (A9, A10, A11, A17) | `round_record.py:2003-2016`, `:2081-2092`; `docs/review-chain-spec.md:1517-1518` | verified | executed — the generator module (A9, A10 green; `grep -n FLOOR_YES` returns six lines, none a reopening read); read — the `one reopening remains` row's condition is `fires` negated |
| 🟢 | phase 2 (#505, #382): one definition of a section's end in `chain_check.py`, delegated to by the generator, read by `section_body`, `swallowed`'s row loop and `verdict_table`; six `###` entries reach the record; `Target SHA` holds the resolved commit (A1–A5) | `chain_check.py:1180-1223`, `:1529-1533`; `round_record.py:1006-1032`, `:1035-1048`, `:1219-1224`, `:2119-2125`, `:2215` | verified | executed — the generator, target and close modules; read — `heading_level` keeps `startswith("#")` and adds depth; `commit_of` is the resolver `resolves` wraps |
| 🟢 | phase 3 (#436, #217): `fix_range`'s pending arm is keyed on `Fixes checked by`, normalised as `fix_surface` normalises, behind `RANGE_FROM`; `claim_lines` holds an unclosed comment's lines symmetrically with `held` (A6–A8) | `chain_check.py:1862-1894` against `:2641-2648`; `evidence_check.py:2065-2103` | verified | executed — the pull-request module's cases and the records-arm module; executed — corpus count of 25 records, no pending pair at or after `RANGE_FROM`, no `Fix range` row between the two cutoffs |
| 🟢 | phase 4 (#174): `seal` keeps a held run behind the new entry on both homes, a first seal is byte-identical, `broad_gate` and `direct_seal` read `named[0]` (A12–A14) | `round_record.py:4313-4319`, `:4441-4444`; `chain_check.py:3684`, `:3723`, `:4012-4021` | verified | executed — the seal module's three new cases inside 579; read — `direct_seal` delegates to `broad_gate` with its own floor; the `not chain.says_gate_not_yet(held)` guard is what keeps a first seal one entry |
| 🟢 | phase 5 (#503, #437, the opener rule): the skeleton carries the three shapes of a `#` cell and runs through `new`; the carried-closure row is one text in four carriers; the five markers, `&lt;!--` and the `###` permission are pinned (A15, A16) | `agents/warden.md:423-441`, `:443-453`, `:464-471`; `tests/test_the_report_standard_is_one_in_three_places.py` | verified | executed — the pin module and the skeleton case inside 579; read — the standard and the generator agree on every shape I wrote in this report, and the report's own `###` entries under `## Paste-ready fixes` are the A1 shape |
| 🟢 | phase 6 (#366's three cases): each pins a widening of the sweep against the reader itself | `tests/test_a_release_is_sized_by_a_criterion.py:100-142` | verified | executed — the module inside 579; the reversions are the phase record's account, read |
| 🟢 | the five divergences `overview.md` records — A9's home, the frame's dropped stamps, the sixth phase, the eighth carrier, the third reader — were each the right call | `overview.md:26-32` | verified | read — each names its grounds and the code agrees; the third reader is the one this round's 🟡 2 and 🟡 3 are siblings of, which says the class was named right and enumerated by sweep rather than by construction |
| 🟢 | work item 0's five inherited points hold: the terminal values with reasons, one reopening reader with no `== FLOOR_YES`, two `Review` answers, `broad-gate.md` through `broad_gate`, the gone/stands pairs untouched | `round_record.py:1397`, `:1973-1975`; `templates/sdd-round.md` diff; `chain_check.py:4012-4021` | verified | executed — the A11 grep and the floor-and-depth module (211 passed with five document-pinning modules); read — the branch's diff touches neither the declaration table nor the four-combination table |
| 🟢 | the four `survivors.md` rows excuse what they quote on grounds that hold, and the sweep in CI's form exits 0 | `seal/specs/1790174138-…/survivors.md:17-20` | verified | executed — `survivor_check.py --range 0b8dc4b2...HEAD --exempt …` exit 0, one exempt; read — the phase-record helper already reads to the first `## `, the ledger row is a past reading, the two paragraph walks share loop tokens and nothing of the rule |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict`, taken once after the rounds settle | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; the hand-back labelled it `unverified` and the orchestrator re-ran thirteen modules — the sealer answers it once this round's fixes land |

## Paste-ready fixes

```python
def kept_broad_gate(reader, rows, value):
    """`value` in front of the run `rows`' `Broad gate` cell already holds,
    or `value` alone where it holds none (#174).

    ONE ENTRY PER RUN, NEWEST FIRST, for every writer of the cell: `seal` and
    `close --broad-gate` used to disagree, the first keeping a held run and
    the second replacing it, and the template describes them as writing the
    same cell. `not yet` holds no run and is replaced, so a first seal is
    byte-identical to what it always was; the new entry goes in front so that
    `chain_check.broad_gate`, which takes the first SHA-shaped word as the
    run, reads what it read before.
    """
    held = reader.visible(chain.field(rows, BROAD_GATE) or "").strip()
    if held and chain.SHA_RE.search(held) and not chain.says_gate_not_yet(held):
        return f"{value}{EARLIER_RUN}{held}"
    return value
```
```python
    gate = cell(BROAD_GATE, kept_broad_gate(reader, rows, args.broad_gate)) if args.broad_gate else None
```
```python
    value = kept_broad_gate(reader, rows, args.broad_gate)
```
```markdown
  Whether
  the one full-suite run has happened — `not yet`, or one entry per run,
  newest first, each the SHA it ran at and the base it was compared against,
  an earlier run kept behind the newest as `earlier run` — is invisible in the
  code, and the next
  session either repeats a sealed run or ships assuming someone else made it.
```
```python
# Every document that describes the `Broad gate` cell's shape, with the phrase
# that says it holds one entry per run (#174). A carrier that drifts back to
# one run is the stale sentence `plan.md` §What breaks in six months names.
GATE_CARRIERS = (
    (("agents", "sealer.md"), "earlier run"),
    (("agents", "warden.md"), "earlier run"),
    (("docs", "review-chain-spec.md"), "earlier run"),
    (("docs", "review-handoff-protocol.md"), "earlier run"),
    (("skills", "code-review", "SKILL.md"), "one entry per full-suite run"),
    (("skills", "code-review", "orchestration.md"), "earlier run"),
    (("skills", "verify", "SKILL.md"), "earlier run"),
    (("templates", "sdd-round.md"), "earlier run"),
)


def test_every_carrier_says_the_cell_holds_one_entry_per_run():
    """#174's shape is stated in eight documents and pinned in none of them
    until now; the ninth carrier (`agents/warden.md` §Role) was found by grep
    one round after the eight were rewritten."""
    for parts, phrase in GATE_CARRIERS:
        text = flat(*parts)
        assert phrase in text, (
            f"{'/'.join(parts)} no longer says the Broad gate cell holds "
            f"one entry per run ({phrase!r} missing)"
        )
        assert "the SHA it ran at and the base it was compared against — is" not in text, (
            f"{'/'.join(parts)} describes the cell as one run"
        )
```
```python
    return [
        (i, cells)
        for i, cells in rows[1:]
        if not reader.is_separator([reader.visible(c) for c in cells])
        and tuple(reader.visible(c) for c in cells) != header
    ]
```
```python
    for line_no, cells in rows[1:]:
        seen = [reader.visible(c) for c in cells]
        if reader.is_separator(seen):
            continue
        if [c.casefold() for c in seen] == header:
            # A second table's header under a `###` inside the section
            # (#505): a row that names the columns is not a verdict row, and
            # read as one it carries a `#` cell reading `#` that nothing
            # refuses.
            continue
```
```markdown
nothing else, and a section ends at the next heading of its own level or
shallower — a `##` or a `#` — never at a `###` (#505). **Write `&lt;!--`
```
```python
        if not running or counted > 1:
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_record_is_generated.py tests/test_chain_check_at_the_pull_request.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_a_record_states_what_the_tree_has.py tests/test_new_says_when_head_is_not_the_target.py tests/test_the_report_standard_is_one_in_three_places.py tests/test_a_release_is_sized_by_a_criterion.py tests/test_the_fixes_close_the_record.py -q` in the clone at `e3cc83c9` | 579 passed, exit 0 |
| `bin/test tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_the_reviewers_report_reaches_the_record.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py -q` | 211 passed, exit 0 |
| `python3 skills/code-review/scripts/survivor_check.py --range 0b8dc4b2...HEAD` with `--exempt` for every `seal/specs/*/survivors.md` (CI's form) | exit 0 — 418 files, 151 removed sentences, one place exempt (`tests/test_a_phase_hands_the_next_one_a_record.py:108`); the same command without `--exempt` exits 1 naming that place |
| corpus count over `seal/specs/*/rounds/round-*.md` (records, not reports): id between `ORDER_FROM` and `RANGE_FROM` with a `Fix range` row; id at or after `RANGE_FROM` with the pending value beside a `round-N`; any `###` inside `## Verdicts` | 25 records; 0, 0 and 0 |
| `grep -n FLOOR_YES skills/code-review/scripts/round_record.py` (A11) | six lines — `terminal_value` and `written_late_cell`'s own refusals and one comment; no `== FLOOR_YES` |
| `grep -rn "the SHA it ran at" agents docs skills templates` | one hit outside the rewritten carriers: `agents/warden.md:321` |
| `grep -rn "newest first\|earlier run\|EARLIER_RUN" tests/` | the seal module's docstring and one unrelated line; no pin over the carriers |
| coverage probe `test_tmp_probe_second_table` (one file, run once, deleted — NAME NOT IN TREE): a report with the verdict table, then `### earlier rounds, re-checked`, then a second table with its header row, through `generate()` | exit 0, record written; the record's `## Verdicts` carries `\| # \| Finding \| Location \| Verdict \| Grounds \|` as a row between the two findings; `chain-check` after the write reports only the ordinary `nobody` notice |
| this report itself through `round_record.py new --round 1 --target e3cc83c9… --baseline 0b8dc4b2` in the clone (the record it wrote there was removed; the worktree's record is the orchestrator's to write) | exit 0 — `Pass` unticked over the three 🟡s, both terminal lines copied as values, 17 verdict rows and all nine fenced blocks under the `###` entries carried; the standard at the target SHA and the generator at the target SHA agreed on every shape written here |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #366's second half — what `depth_two` should do when one finding's `Location` spans units of two depths | already deferred in `overview.md` §Not done, on #366 | the repository owner |
| #159 — a record cell corrected in place leaves no trace; the sketch for it | already deferred in `plan.md` §Alternatives and `questions.md` Q1, relayed to #159 | the repository owner, who relays it to the framer of the release after |
