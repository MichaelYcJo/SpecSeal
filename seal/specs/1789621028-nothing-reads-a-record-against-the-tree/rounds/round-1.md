# 1789621028-nothing-reads-a-record-against-the-tree — review round 1

| Field | Value |
|---|---|
| Target SHA | 35796574 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 435 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `b38bd920004a2abcb3d7715861fc7e6c3e47ad69..bf693bc13d31f01368ea0decfe4d9e8f6d94ce47`, 6 commits |
| Contract changes | none |
| New units | test_a_record_with_no_fix_range_row_is_told_which_row_to_add (depth 1) |
| Needs a fix | yes — 🟡 1, the pending `Fix range` no arm ever reads back; and 🟡 2 and 🟡 3, either of which the smith may close with grounds instead |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Review the whole branch against the frame a different party wrote. Spec compliance first: `spec.md` closed #344's open question — whether a record is read against the tree by anchors in records, by a checker that re-reads them, or by a rule that pins a range when it is written — and chose the third with four stated grounds. Judge the built work against that decision, and the decision against the grounds it claims. Then quality, with `CONTRIBUTING.md` §*What a change to a gate must carry* over the four new refusals.

Three of the builder's disclosures were handed over as claims to check rather than as facts: three of the frame's corpus counts did not reproduce and the re-measured values went into the shipped documents while the frame was left as written; the frame estimated three new refusals where four landed; and the new arm that reads a stated fix range sits behind a cutoff while the duplicate-cell arm has none. Nothing the builder reported having run had been re-run by the orchestrator.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `Fix range` still saying *the fixes are not yet written* is never named, where `fix_surface` refuses exactly that state for its own two rows | `skills/code-review/scripts/chain_check.py` · `fix_range`, the `says_none` early return | deferred #436 | #436 — Closing it means adding a refusal arm to `fix_range`, which is mechanism a fix pass may not add — `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed*. The issue carries the orchestrator's execution, the paste-ready arm from round 1's report, and the cutoff question that comes with it; Executed: a planted record with `Fixes checked by \| round-2` gives `fix_range -> ([], [])` while `fix_surface` errors on both its rows and the full run exits 1 naming `Contract changes` and never `Fix range` |
| 🟡 2 | `close` refuses a record written before the row exists, at exit 2, with a message naming no repair — while the changelog and the pull request body both say such records print rather than fail | `skills/code-review/scripts/round_record.py` · `close`, the `field_index(reader, lines, chain.FIX_RANGE)` write | **fixed** `82c2ed56` | fixed at 82c2ed56; Executed: exit 2, `the record has 0 \| Fix range \| … \| rows and needs one`, record unchanged. `chain_check`'s `RANGE_FROM` covers the same state; the generator has no equivalent |
| 🟡 3 | The shipped specification states a corpus count with a date and no command, and I could not reproduce it | `docs/review-chain-spec.md` · §*The fix range — `Fix range`*, the *Measured over this repository* paragraph | **fixed** `82c2ed56` | fixed at 82c2ed56 — `b9ce125e`; Executed at both ends of the branch: 39 files, 11 stating a range, 11 spellings, 3 naming `HEAD`, against the document's 39 / 15 / 8 / 5. The work item's own R7 is the rule this breaks · **Orchestrator's verification, 2026-09-17**: a third method gives 39 files, 15 stating a range, 4 naming `HEAD` and 12 distinct spellings — so the document's 39 and 15 DO reproduce and its 8 and 5 do not, and the reviewer's 11 / 11 / 3 is a fourth answer rather than the right one. Three readers, three results, which is the finding: the paragraph names a date and no method, so nothing adjudicates. The repair is to name the command, not to swap the numbers <!-- Everything after the `·` was added by hand by the orchestrating session at the verify-before-posting step, from its own run over the same corpus. The reviewer's report is unchanged and still carries 11 / 11 / 3. --> |
| ⬜ 4 | Two `# EVERY record too` comment blocks are stacked, so `doubled_grounds`'s *it has no cutoff* sits above the `fix_range` call, which has one | `skills/code-review/scripts/chain_check.py` · `main`, above `range_errors, range_notices = fix_range(...)` | **fixed** `82c2ed56` | fixed at 82c2ed56; Read. `doubled_grounds`'s own call carries no comment; which arm is grandfathered is the load-bearing fact about either |
| ⬜ 5 | The new template row is the only field row in the table with no closing `\|` | `templates/sdd-round.md` · the `\| Fix range \|` row | **fixed** `82c2ed56` | fixed at 82c2ed56; Executed: every other field row ends ` \|`, this one ends `g>`. `split_row` tolerates it, so nothing breaks; a template is a form sessions copy |
| ⬜ 6 | A now-reproducible command is quoted beside a number it does not produce | `seal/specs/1789034970-…/survivors.md` · the line under `## Over the whole branch — what CI reads` | **fixed** `82c2ed56` | fixed at 82c2ed56; Executed by the branch itself and recorded in its own comment: the pinned range gives 2 today and 3 under the old checker; the prose still says sixteen |
| ⬜ 7 | The build re-stamped 22 rows of `seal/ledger.md`, which `spec.md` §Out excluded, and the divergence table has no row for it | `seal/specs/1789621028-…/overview.md` · §*Where spec and implementation diverged* | **fixed** `82c2ed56` | fixed at 82c2ed56; Executed: 22 rows changed, each in exactly the anchor hash and the `Checked` date. The act was required; the record of it is the omission |
| ⬜ 8 | `close` guards `rev-list --count` with `is None` alone where `chain_check` also checks `isdigit()` forty lines away | `skills/code-review/scripts/round_record.py` · `close`, `spanned = int(counted.strip())` | **fixed** `82c2ed56` | fixed at 82c2ed56; Read. Defensive only, and the two readings of one command disagree |
| ⬜ 9 | The new arm adds two `rev-parse` calls and one `rev-list` per record, and `resolves_to` is not memoized | `skills/code-review/scripts/chain_check.py` · `fix_range` and `resolves_to` | answered | The cost is zero today and that is measured, not assumed: `fix_range` returns before it calls git where the row is absent or says `none`, and the arm run over all 230 records in this tree makes 0 git calls in 0.057 s. The reviewer's 690 is arithmetic that becomes real only once records carry the row. Memoizing `resolves_to` changes a function five arms share, for a cost that is zero now, which is what a fix pass may not build; the moment it becomes real is measurable; Read. Zero cost today because no record carries the row; roughly 690 git invocations per pull-request run once they do |
| ⬜ 10 | Two fix tables still state `..HEAD` at the branch tip, and nothing will ever name them | `seal/specs/1789598366-…/rounds/round-1-fixes.md` and `round-2-fixes.md` | answered | Scope honoured, and nothing naming those two files is the design rather than a gap. `spec.md` §Out excludes other work items' records, `RANGE_FROM` excuses them, and the prose header is the place `spec.md` explicitly refuses to point a parser at — 15 files in 12 forms. Phase 5 repaired 1789034970's records because #344 named those five places; 1789598366's were never named. Recording the survival is the right handling; Executed. Scope honoured, not missed — `spec.md` §Out excludes other work items' records. Recorded so the survival is not invisible |

## Paste-ready fixes

```python
    text = read_record(root, rel)
    if text is None:
        return [], []
    lines = reader.readable(text)
    rows = table_rows(reader, lines)
```
```python
    if says_none(value):
        # A round that commissioned no fixes has no range, and `none` is the
        # honest value -- the one `new` writes before the fixes exist. What it
        # stops being honest about is a record a LATER round has already
        # opened the fixes of: they exist, so `not yet written` is false, and
        # this is the arm `fix_surface` runs on its own two rows for the
        # identical reason. The three rows take the same pending value from
        # `build` in one line; two of them were read back for whether anybody
        # replaced it and this one was not.
        checker = (
            reader.visible(field(rows, CHECKED_BY) or "")
            .strip()
            .strip("`")
            .strip()
            .rstrip(".")
            .lower()
        )
        if CHECKER_RE.match(checker) and says_not_yet(value):
            return [
                (
                    rel,
                    0,
                    f"`{FIX_RANGE}` still says the fixes are not yet written, "
                    f"and `{CHECKED_BY}` names `{checker}` above it — so a "
                    "later round opened those fixes and they do exist. The "
                    "cell contradicts its own file. It is the starting value "
                    "every record carries, because a record is committed "
                    "BEFORE its fixes; what is missing is the reach-back that "
                    "fills it when they land. Write "
                    "`` `<a>..<b>`, N commits ``, or let `round-record close` "
                    f"write it — or a bare `{NONE_WORD}` if this round "
                    "commissioned no fixes after all",
                )
            ], []
        return [], []
```
```python
    try:
        at_range = field_index(reader, lines, chain.FIX_RANGE)
    except Refused:
        raise Refused(
            f"the record has no `| {chain.FIX_RANGE} | … |` row, so there is "
            f"nowhere to write the range this pass was measured over. It was "
            f"written by a `new` from before that row existed — `close` "
            f"replaces the row rather than inserting one, because a record's "
            f"field order is the template's. Add `| {chain.FIX_RANGE} | "
            f"{chain.NONE_WORD} |` under `| {chain.CHECKED_BY} | … |` and run "
            f"`close` again. No cell was written"
        ) from None
```
```python
    raw[at_range] = fix_range
```
```markdown
prose to enforce, which is why the authoritative statement moves into the
record instead of a parser being pointed at the prose. The figures are
reproducible only against both the tree and the instrument (`seal/ledger/
1789621028-nothing-reads-a-record-against-the-tree.md` R7): measured at
`35796574` by `<the command>`. A different reading of *stating a range in
their first eight lines* gives a different count, and this sentence is what
lets the next reader tell the two apart.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone | 228 passed, exit 0 |
| `tests/test_chain_hooks_hardening.py` with `f.read()` mutated to `f.read(2000)`, then restored | exit 1 mutated, exit 0 restored — #426's new guard reddens under the mutation it pins |
| probe A — a planted record with `Fix range` and `Contract changes` both pending and `Fixes checked by \| round-2` | `fix_range -> ([], [])`; `fix_surface` errors on both its rows; full run exit 1 naming `Contract changes`, not `Fix range` |
| probe B — `Fix range \| none` beside a `**fixed**` verdict | `fix_range -> ([], [])`; `closed_with_a_fix` on the same lines returns `True` |
| probe D — the template's field rows | `Fix range` is the only row ending `g>`; every other ends ` \|`. `split_row` returns 2 cells for it |
| probe E — whether git resolves an uppercase abbreviated SHA | it does, and `resolves_to` returns the full lowercase commit. The uppercase branch of `FIX_RANGE_RE` is therefore harmless and is not a finding |
| probe F — `close --range <a>..<b>` against a record with no `\| Fix range \|` row | exit 2, `the record has 0 \| Fix range \| … \| rows and needs one`, record unchanged |
| A first-principles count of `seal/specs/*/rounds/round-N-fixes.md` at `release/v0.12.1` and at `35796574` | 39 / 11 / 11 / 3 at both, against the document's 39 / 15 / 8 / 5 |
| A count of `round-*.md` files carrying `\| Fix range \|` | 0 of 406, every work-item id below `RANGE_FROM` |
| `uvx ruff check` on the five changed Python files | All checks passed, exit 0 |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer, and this round ran none of them. They come due once nothing is open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |
