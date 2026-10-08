# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — review round 5

| Field | Value |
|---|---|
| Target SHA | 551efb7a8140ca078255b7698f8462c5559dfa72 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 878 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 5 of round 4's fixes: 6445933a..76de29c3 (f2d7d9ab, 76de29c3), plus the table, two survivors rows and the close at 551efb7a. The job was the answers to round 4's five verdicts, plus the new unit test_a_sentence_linking_the_home_uses_no_listed_word as a finding surface. The spawn told it to open no new derived-wording findings beyond what the fixes wrote. It asked for plain probes, with a scratch repository as cwd. It also ran the eight guard modules once. Facts arrived labelled. Read: the orchestrator's direction to remove claims rather than restate them. Read from the smith: the five removals, the narrowed guard, 602 passed, and evidence-check and survivor-check at exit 0.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 4's finding 1 is closed — the home's clause saying every reader of a range imports `own_commits` is gone, and nothing replaces it | `docs/the-record-layout.md:122` | confirmed | read: the section; executed: no tree sentence outside the round records says "every reader of a range"; pasting it back turns nothing red, which a removal needs no pin for |
| 🟢 | round 4's note 2 is closed — the owner sentence is the git command alone, in the home, rule 17's pin and ledger row 16 | `docs/the-record-layout.md:121` | confirmed | executed: the gloss pasted back turns rule 17 red; the gloss survives only in `spec.md`, excused in `survivors.md` and accepted by `survivor-check` |
| 🟢 | round 4's note 3 is closed — the guard's docstring says it is a word list that other words pass | `tests/test_the_range_rule_states_no_shape.py:17` | confirmed | read; what the docstring newly says about the four carriers is this round's note 1 |
| 🟢 | round 4's note 4 is closed — the silent-state row says "squashed away" again, outside the guard's reading | `skills/code-review/scripts/chain_check.py:4585` | confirmed | executed: a listed word in `fragment_left_behind`'s linking sentence is red, and outside it passes |
| 🟢 | round 4's note 5 is closed — the fragment section's input sentence carries no shape clause | `docs/the-record-layout.md:100` | confirmed | read; the clause survives only in `spec.md:170`, excused and accepted by `survivor-check` |
| ⬜ 1 | The guard's docstring and ledger row 16 say each of the four range readers' docstrings reaches the list through its linking sentence; nothing checks that a docstring keeps its link, and `touched` dropping it leaves the guard and rule 17 green | `tests/test_the_range_rule_states_no_shape.py:12` | open | executed: `touched`'s link replaced by a shape sentence, 69 passed; the paste-ready case passes at the target and is red under that edit |
| ⬜ 2 | Ledger row 16 rests "every sentence linking the home (the four docstrings' among them)" on the linking case and does not anchor it | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:16` | open | read: the anchors carry `SHAPE_WORDS`, the home case, the list case and `RULES`; a correction to the run's paperwork, not counted in Needs a fix |

## Paste-ready fixes

```python
# The units whose docstrings carry the rule, by file: each reaches the list
# only through its linking sentence, so each must keep one.
CARRIERS = {
    "chain_check.py": ("own_commits", "fragment_left_behind"),
    "round_record.py": ("fix_pass_units", "touched"),
}


def test_each_reader_of_a_range_keeps_its_linking_sentence():
    missing = []
    for name, units in CARRIERS.items():
        module = ast.parse(read(os.path.join(SCRIPTS, name)))
        found = {
            node.name: flat(ast.get_docstring(node) or "")
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name in units
        }
        missing += [f"{name}#{u}" for u in units if LINK not in found.get(u, "")]
    assert not missing, (
        "a docstring of a unit that reads a range no longer links the home, "
        f"so the list no longer reads it ({LINK}): " + ", ".join(missing)
    )
```
```text
`tests/test_the_range_rule_states_no_shape.py#test_a_sentence_linking_the_home_uses_no_listed_word@<stamp>`
```

## Executed probes

| What was run | Result |
|---|---|
| a `--no-local` clone of the worktree at the target, in the round's scratch directory | HEAD 551efb7a8140ca078255b7698f8462c5559dfa72 |
| `bin/test` over the eight guard modules the spawn named, in the clone | exit 0; 435 passed |
| every sentence `linking_sentences` yields, and whether each of the four docstrings contains the link | 8 sentences; all four docstrings link; `fragment_left_behind`'s whole docstring holds "squash" outside its linking sentence |
| `test_tmp_round5.py` in the round's scratch directory, run once and deleted — NAME NOT IN TREE | exit 0; results in the rows below; the clone clean after each restore |
| baseline, the guard module | exit 0; 3 passed |
| "After a squash" in `fragment_left_behind`'s linking sentence, the guard module | exit 1; 1 failed |
| "A sibling's units are a fork's." at the head of `touched`'s docstring, outside its linking sentence | exit 0; 3 passed |
| `touched`'s link replaced by a shape sentence, the guard module and rule 17's module | exit 0; 69 passed |
| `own_commits`'s link replaced by a shape sentence, the same two modules | exit 1; 1 failed |
| round 4's 🟡 1 clause pasted back into the home, the same two modules | exit 0; 69 passed |
| round 4's ⬜ 2 gloss pasted back after "lists", rule 17's module | exit 1; 1 failed |
| ⬜ 1's paste-ready case added to the guard module, then `touched`'s link removed, in a `python3 -` script | exit 0, 4 passed; then exit 1, 1 failed |
| `git grep` for the five removed phrases outside the round records | the gloss and the ⬜ 5 clause only in `spec.md` and `survivors.md`; "squashed away" in the restored row; "gone from this clone" only in `phases/phase-6.md`'s record of the rewording |
| `bin/evidence-check --strict` in the clone | exit 0 |
| `bin/survivor-check --range 6445933a..551efb7a --exempt` the item's `survivors.md` | exit 0; 2 excused, both `spec.md` |
| the same without `--exempt` | names `spec.md:70` and `spec.md:170`, the two places the rows excuse |
| `round-record new` over this report, in the clone only, its output discarded | exit 0; all three tables and both lines parsed; the fragment notice names `f2d7d9a`, and the item's `changelog.md` carries none of the five removed phrases (read), so it needs no change |
| `gh pr checks 878`, read twice, the last after this report was written | head 551efb7a: 5 pass (release, lint, ledger, both arm-check-grammar legs), 8 pending (every pytest leg), none failed |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle; never run in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_shrunken_corpus_declines_to_judge.py:245` | round 1's 🔴 1 — fixed |
| round-1 | `docs/the-record-layout.md:121` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2384` | round 1's ⬜ 3 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:4450` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/orchestration.md:372` | round 1's ⬜ 5 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:4370` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py:3711` | round 1's 🟢 — confirmed |
| round-2 | `docs/the-record-layout.md:148`, `skills/code-review/scripts/chain_check.py#own_commits` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/orchestration.md:370` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:13` | round 2's ⬜ 3 — answered |
| round-2 | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:11` | round 2's ⬜ 4 — answered |
| round-2 | `tests/test_a_shrunken_corpus_declines_to_judge.py:248` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/round_record.py:2402` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/spec.md:70` | round 2's 🟢 — confirmed |
| round-3 | `docs/the-record-layout.md:99` | round 3's 🟡 1 — deferred |
| round-3 | `docs/the-record-layout.md:126` | round 3's 🟡 2 — deferred |
| round-3 | `skills/code-review/scripts/chain_check.py#own_commits` | round 3's 🟡 3 — deferred |
| round-3 | `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md:4` | round 3's ⬜ 4 — deferred |
| round-3 | `docs/the-record-layout.md:150` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:7` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/survivors.md:27` | round 3's 🟢 — confirmed |
| round-4 | `docs/the-record-layout.md:125` | round 4's 🟡 1 — fixed |
| round-4 | `docs/the-record-layout.md:122` | round 4's ⬜ 2 — fixed |
| round-4 | `tests/test_the_range_rule_states_no_shape.py:10` | round 4's ⬜ 3 — fixed |
| round-4 | `skills/code-review/scripts/chain_check.py#fragment_left_behind` | round 4's ⬜ 4 — fixed |
| round-4 | `docs/the-record-layout.md:102` | round 4's ⬜ 5 — fixed |
| round-4 | `docs/the-record-layout.md:100` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_a_range_owns_what_git_lists_for_it.py` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_a_fragment_left_behind_is_named.py:181` | round 4's 🟢 — confirmed |
| round-4 | `seal/specs/1791384160-a-fix-range-is-its-own-commits-across-a-merge/changelog.md:27` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_a_fragment_left_behind_is_named.py#check` | round 4's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
