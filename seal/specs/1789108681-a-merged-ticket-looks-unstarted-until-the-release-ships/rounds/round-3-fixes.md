# round 2's fix pass — the table `round_record.py close` applies

Range: `99005ba..64d830b`. Three commits, one per finding; the round record
they answer is `rounds/round-2.md`.

Spelled parent-of-first-fix to last, the way round 1's `076d691..ab069b1`
was: `a..b` excludes `a`, so `4eda3a5..` would drop finding 16's own commit
from the diff `close` measures. Confirmed against `survivor-check`, which
sees 2 removed sentences over `4eda3a5..64d830b` and 3 over this range.

Findings 1 through 4 and 6 through 15 take no row: round 2 closed them, and a
row here would overwrite the reviewer's verdict with mine.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 16 | fixed | `4eda3a5`, `.github/scripts/release_completeness_check.py:48-52`. The finding holds as stated: `grep -n environ` over the file returns four reads — `HEAD_BRANCH:251`, `REPO:260`, `BASE:261`, `HEAD_SHA:266` — and the line named three. It now names `HEAD_SHA` with its default (`HEAD`) and one clause saying its absence is the silent one, pointing at `merge_base` for the cost. **The paste-ready text was taken in part and declined in part:** it restated the merge-ref argument in full, and that argument already stands twice in this file — `merge_base`'s docstring at `:88-98` and the comment above `point` at `:262-265`. A third copy adds a third place to keep in step, which is the failure mode finding 16 is itself an instance of. The enumeration, the default and the pointer are what close the defect; the retelling is what the finding says is already there. **Class swept:** only two scripts in `.github/scripts/` carry an `Environment:` line. The sibling's is complete — its fifth, `DRY_RUN`, has its own paragraph at `:44-46` — and `close_issues_on_release.py` reads four and carries no such line at all, so there is no false enumeration there and it is outside this branch's diff |
| 17 | fixed | `f4384ed`, `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488`. *all four* → *every entry*. The reviewer's paste-ready text was taken over the arithmetic correction *all five*: the tuple at `:492` has five members today and the step's `env:` block can gain a sixth, which would rot *five* exactly as it rotted *four*. The sentence now describes the loop rather than counting it. No case pins this and none was added — the unit is round 1's own fix surface, so a case for it would be depth 2 |
| 5 | fixed | `64d830b`, `overview.md:31`, *Eight modules* → *Nine*. Both figures re-derived rather than inherited, and the module list at `:9` names the same nine. **Class swept rather than the coordinate**, which is what produced this finding: `grep -rniE "\b(eight\|nine)\b"` over the work item excluding `rounds/` returns **five** hits — `overview.md:9` already correct, `overview.md:31` this one, `questions.md:17` and `plan.md:81` both counting open milestone issues, a different subject and both true, and `phases/phase-5.md:31`'s *Eight rows*, which counts ledger rows and agrees with `overview.md:9`. (This cell said *four* while naming the fifth in its own next breath; round 3 re-ran the command and reported it as finding 20.) The `rounds/` records keep their *eight*: they are past-state documents read at their own target SHA, and `round-1-report.md:17` saying *165 across the eight modules the paragraph names* is a true statement about what that paragraph said |

## What was run over the fix range

Executed by the fix pass, exit codes read directly with no pipe: seven test
modules one per call — 29 · 23 · 13 · 2 · 32 · 23 · 2, exit 0 each;
`uvx ruff check` and `uvx ruff format --check` on the two changed Python
files, exit 0 each; `bin/survivor-check --range 99005ba..64d830b`, exit 0
over 880 files against 3 removed sentences, no `survivors.md` needed;
`bin/evidence-check --strict .`, exit 0, 1137 ok · 0 drifted · 0 broken — the
three ledger rows anchored into `release_completeness_check.py` (`#judge`,
`#milestone_titles`, `#merge_base`) all resolve, and the module docstring is
not inside a hashed unit.

**Re-run by the orchestrating session at `64d830b`**, because a hand-back's
verification claim is a claim: eight modules one per call —
`test_a_release_cannot_ship_an_untrue_milestone` 29,
`test_ci_gives_the_checks_what_they_need` 2,
`test_a_merged_ticket_says_so_on_the_tracker` 23, `test_docs_line_wrap` 23,
`test_release_hygiene` 32, `test_one_word_one_meaning` 13,
`test_no_real_identifiers` 2, `test_a_record_states_what_the_tree_has` 58 —
**182 passed, exit 0 each**; `uvx ruff check` and `uvx ruff format --check`
on both changed Python files, **exit 0** each. The diff was read line by line
and touches three files and nine lines.

**No unit was added**, so there is nothing for the seen-red requirement to
apply to. Both findings 16 and 17 sit inside round 1's fix surface, where a
case would be depth 2 and is refused. No mechanism was added.

**Not run: the broad gate.** `agent-contract` §2 assigns it to the sealer,
once, after the rounds settle.
