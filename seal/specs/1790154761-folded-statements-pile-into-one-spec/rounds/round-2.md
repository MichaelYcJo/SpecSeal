# 1790154761-folded-statements-pile-into-one-spec — review round 2

| Field | Value |
|---|---|
| Target SHA | b527bd86ca45775afcb71edb5e0b015deb858972 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 527 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `8549aa3aa83824844ed4a79d4b213ab109e164ff..bbd984667adeef2854650e530cc63ce4a42fbb18`, 2 commits |
| Contract changes | none |
| New units | test_a_marker_removed_on_purpose_is_told_to_recompute_the_digest (depth 1); test_a_count_that_moved_is_told_to_recompute_the_digest_too (depth 1); test_a_rule_sentence_in_bold_italics_opens_bold (depth 1); test_a_heading_with_a_tab_or_no_text_ends_a_statement (depth 1); test_a_symlink_inside_the_root_that_leaves_it_is_named (depth 1); test_a_heading_with_a_tab_or_no_text_is_read (depth 1) |
| Needs a fix | yes — finding 3: after a marker is removed on purpose, the digest branch reports a swap that did not happen and neither message says to recompute `FROZEN_IDS_DIGEST` |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round over round 1's fixes (`edcd2e33..ca380837`, one commit, plus the record commit `b527bd86`), not the branch. For findings 1 and 2, recorded `fixed`, it asked whether each is actually closed, re-running round 1's own probes against the fix. It judged the units in round 1's `New units` row as code nobody had reviewed: `FROZEN_IDS_DIGEST`, `marker_digest`, `BOLD_OPENING` and the five new cases. It also checked round 1's three ⬜ corrections that rode the same commit. And it judged the smith's choice to drop the reviewer's `full == base` clause from the paste-ready fix for finding 2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1 finding 1: a marker swap at equal count into the listed document is now refused | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | verified | Executed: round 1's probe (old id plus a bound id, frozen at 2) is named "but not the ones frozen"; a duplicate-id swap is named too; the real-tree digest is `8f8c4d85f213` over 29, matching the constant |
| 🟢 | Round 1 finding 2: `.`, a directory, `../outside.txt` and `tests/../..` are now refused as targets | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | verified | Executed: all four are named; the pre-fix unit passed all four; with containment removed, `../outside.txt` passes again |
| 🟢 | The smith dropped round 1's `full == base` clause | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | verified | Executed: `.` normalises to the base, which is a directory, so `isfile` refuses it; no input reaches that clause and passes. The added `abspath` fixes a relative-root `commonpath` error round 1's fix had |
| 3 | 🟡 After a marker is removed on purpose and the count is lowered, the digest branch says a fold "adds a statement here and removes another" and "keeps the count", both false, and neither message says to recompute `FROZEN_IDS_DIGEST` | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | **fixed** `d8aa3054` | fixed at d8aa3054 — the count message names the recompute, and the digest message states the swap and the deliberate removal as conditions, each with its repair; Executed: frozen at 1 with the old two-id digest returned the swap message. The recompute instruction is only in a code comment. The text came from round 1's paste-ready fix |
| ⬜ | `BOLD_OPENING` refuses `***Rule.***`, which CommonMark renders bold, and says it is not bold | `tests/test_a_folded_statement_names_what_enforces_it.py#BOLD_OPENING` | correction | Executed. No instance in the tree; a writer can drop the italic |
| ⬜ | Both `HEADING` patterns skip `##` followed by a tab and a bare `##`, the rest of round 1's correction-5 class | `tests/test_both_editions_carry_the_same_folds.py#HEADING`; `tests/test_a_folded_statement_names_what_enforces_it.py#HEADING` | correction | Executed: one edition carrying either passes. No line of either shape under `docs/` |
| ⬜ | `target_problem` resolves a symlink inside the root that points at a file outside it | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | correction | Executed. `normpath` does not resolve links; `realpath` on both sides closes it. No such target is written anywhere |
| ⬜ | Ledger rows E1 and S1 claim the new heading and bold behaviour without anchoring `HEADING` or `BOLD_OPENING` | `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`, rows E1 and S1 | correction | Read. A paperwork correction: add the three constants to `Code grounds` |
| 🟢 | Round 1's three corrections (evidence-ledger exemption sentence, settle §2 "carries … written last" with bare `**` refused, headings indented up to three spaces) | `docs/the-evidence-ledger.md`; `skills/settle/SKILL.md`; the two `HEADING` patterns | verified | Read the wording; executed bare `**`, `   ## A`, ` ## A` and `    ## code` through the new units; the neighbouring pin modules are green |

## Paste-ready fixes

```python
# tests/test_a_document_has_room_for_the_next_fold.py — ceiling_problems
        found = markers(text)
        if found != frozen:
            problems.append(
                f"{rel} carries {found} fold markers and is frozen at {frozen} "
                f"until {home} splits it. A new fold goes to the document for "
                "the rule's own sub-subject; a removed marker lowers the frozen "
                "count, so the room it made is not refilled, and recomputes "
                "FROZEN_IDS_DIGEST with marker_digest() in the same commit"
            )
            continue
        want = (digests or {}).get(rel)
        if want is not None and marker_digest(text) != want:
            problems.append(
                f"{rel} carries {frozen} fold markers, but not the ones frozen "
                f"until {home} splits it: their ids no longer match "
                "FROZEN_IDS_DIGEST. If a fold added a statement here and "
                "removed another, the new rule goes to the document for its own "
                "sub-subject. If a marker was removed on purpose, set the digest "
                "to marker_digest() of the file in the commit that lowered the "
                "count"
            )


# a planted case, red on the current message (it names no marker_digest)
def test_a_marker_removed_on_purpose_is_told_to_recompute_the_digest(tmp_path):
    frozen = body(12, 2)
    root = tree(tmp_path, {"big.md": body(12, 1)})
    found = ceiling_problems(
        root, 10, {"docs/big.md": (1, "#1")}, {"docs/big.md": marker_digest(frozen)}
    )
    assert len(found) == 1 and "marker_digest" in found[0], found
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three new modules at `b527bd86`, in the clone | 37 passed |
| `bin/test` over `test_settle_reads_before_it_removes`, `test_docs_line_wrap`, `test_the_rules_have_one_owner` at `b527bd86` | 154 passed |
| `bin/evidence-check --strict .` at `b527bd86` | exit 0 |
| `bin/unverified-check` at `b527bd86` | exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the three touched modules only | all checks passed; 3 files already formatted |
| One `test_tmp_` probe re-running round 1's planted inputs through the new units | swap named; duplicate swap named; `.`, `tests`, `../outside.txt`, `tests/../..` named; bare `**` named; `   ## A` named; real digest `8f8c4d85f213` over 29 |
| The same probe, new inputs | removal with count lowered and stale digest: swap message (finding 3); symlink escape `[]`; `***Rule.***` refused; `##` plus tab and bare `##` `[]`; indented heading ends a statement in the shape reader |
| The same probe, new case inputs against the pre-fix units from `edcd2e33` | old `target_problem`: all four `[]`; old bold opening: bare `**` `[]`; old pairing heading: `   ## A` `[]`; containment removed from the new unit: `../outside.txt` `[]`. Probe file, the extracted pre-fix modules and the clone are deleted |
| The swap case with the digest comparison mutated out | not run here: the smith's claim in ledger row P1, read and not re-executed |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet run, and not this round's; the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | round 1's 1 — fixed |
| round-1 | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | round 1's 2 — fixed |
| round-1 | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, first bullet | round 1's ⬜ — correction |
| round-1 | `skills/settle/SKILL.md` §*2. Write one standing statement per segment*; `tests/test_a_folded_statement_names_what_enforces_it.py#shape_problems` | round 1's ⬜ — correction |
| round-1 | `tests/test_both_editions_carry_the_same_folds.py#outline` | round 1's ⬜ — correction |
| round-1 | `docs/one-root-by-lifetime.ko.md` | round 1's 🟢 — verified |
| round-1 | `tests/test_both_editions_carry_the_same_folds.py` | round 1's 🟢 — verified |
| round-1 | the three new modules | round 1's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
