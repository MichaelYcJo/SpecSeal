# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — review round 2

| Field | Value |
|---|---|
| Target SHA | 906c78b375e68793115f16fa007d9da2685fa744 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 428 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round over round 1's fixes, at the diff `c4e9c58b..af5b756c`.
Round 1 opened four 🟡 and the fix pass closed two by repair and two by
correcting a claim, so the round was asked first whether the two *answered*
verdicts are answers or concessions — whether the escape's narrowing really
leaves nothing unwritable, and whether the four disclosure sites now say the
same thing as each other and as the code. Then, as in round 1, whether the
repairs are blind one layer down: finding 1's case must go red on the
CONDITION, not on the presence of the conditional sentence; finding 3's new
branch must be guarded by the file that genuinely has no `Broad gate` row;
and the fix pass's own two widenings — a backslash before any cell-ending
pipe, and a later `seal mode` leaving a file stating two different modes —
must be pinned by something that fails, not only written down.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `refusal` answers about the first refused line while both callers ask about the table, so a second refused line makes the absent-row message and the cost sentence false again | `hooks/config.py:152` | open | Executed: with two refused lines the `Broad gate` row on line 6 is reported ABSENT, and in the mirror shape the refusal says the rows below were read while `Record language` was lost. `hides_this_row` is handed a list holding the row and the branch is gated on `ended`, which describes a different line |
| ⬜ | the changelog states the round 1 🟡 3 repair without the condition it has | `seal/specs/1789598366-…/changelog.md:49` | correction | Executed: for the two-refused-line file the row is reported absent, not named unreachable |
| ⬜ | seven of the thirteen re-anchored `seal/ledger.md` rows carry no note saying who read them, and the record that discloses the re-reads says four and says each carries one | `seal/ledger.md`, `seal/specs/1789598366-…/overview.md:37` | correction | Executed: thirteen rows changed over `0995f62f..906c78b3`, ten re-stamped again inside the fix range, six carry a `Re-read 2026-09-17 … (#415)` note, dates still 2026-09-10/11. `bin/evidence-check --strict .` exit 0 either way |
| ⬜ | the bare-spelling limitation case names one of the four records that must change when the limit is closed | `tests/test_the_mode_question_is_asked_once.py:332` | correction | Read: the messages name `overview.md` §*Not done* and otherwise say *the records that disclose it*; the other three are `changelog.md:35`, `spec.md` §*What this repair cannot see*, `templates/config.md` |
| ⬜ | `refusal` gives up at a prose line above the table's first row where `config_rows` keeps reading | `hooks/config.py:204` | correction | Executed: a refused row under such a prose line is reported as an absent row. The old `refused_row` did the same, so it predates the branch |
| 🟢 | round 1 🟡 1 is closed — the cost sentence is read off the file and the case is red on the condition in both directions | `skills/verify/scripts/broad_gate.py:328` | confirmed | Executed: chooser wired to `True` reddens the first-row half, the two sentences swapped redden the second-row half |
| 🟢 | round 1 🟡 2 is an answer — no value lost a spelling, and the tree-wide measurement reproduces | `hooks/config.py:70` | confirmed | Executed: 17,297 old-reachable pairs all come back byte for byte from `\| item \| value \|`; 1,460 files, 84 lines differing, 83 widening, one narrowing and it is the report's own fixture |
| 🟢 | round 1 🟡 3 is closed for the member it named, and the guard on the new branch is real | `skills/verify/scripts/broad_gate.py:352` | confirmed | Executed: the branch widened to every other-item refusal reddens `test_a_refused_row_of_some_other_item_is_not_read_as_this_one`; a file with no such row anywhere still reaches the absent-row refusal |
| 🟢 | round 1 🟡 4 is an answer — the four disclosure sites agree with the code and with each other, and the worse claim is true | `seal/specs/1789598366-…/overview.md` §*Not done* | confirmed | Executed: `seal mode local` over a two-deep file sets the first row and leaves the second, so the file states two modes and `config_rows` takes the first |
| 🟢 | both new widenings are pinned, the second in the inverted direction | `tests/test_the_mode_question_is_asked_once.py:230`, `:332` | confirmed | Executed: `CELL` reverted reddens the first; a greedy last cell reddens the second |
| 🟢 | round 1's ⬜ correction is closed on both halves | `hooks/config.py:152` | confirmed | Executed: a refused line in a second table comes back `None`; an indented refused line is returned with its indentation |
| 🟢 | the new branch is about unparseable lines rather than about pipes | `skills/verify/scripts/broad_gate.py:352` | confirmed | Executed: a three-column row hiding a `Broad gate` row reaches the *never reached it* branch |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules this branch touches, at the target SHA, in the clone | exit 0 · 343 passed |
| the cost chooser wired to `True` — the sentence the build shipped | exit 1 · `test_what_a_refused_line_cost_is_read_off_the_file_and_not_stated_flat`, first-row half |
| the two cost sentences swapped | exit 1 · the same case, second-row half |
| the hidden-row branch widened to every other-item refusal | exit 1 · `test_a_refused_row_of_some_other_item_is_not_read_as_this_one` |
| the hidden-row branch made unreachable | exit 1 · `test_a_broad_gate_row_below_a_refused_line_is_not_reported_absent` |
| `CELL` back to `[^\|]`, the pattern that predates the escape | exit 1 · 3 failed, including `test_a_backslash_against_a_pipe_is_the_one_shape_the_escape_narrows` |
| a greedy last cell, so the bare pipe parses | exit 1 · 4 failed, including `test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe` |
| each of the six restored from bytes, `tests/__pycache__` cleared | exit 0 each |
| reachability: every `(item, value)` the old pattern produced, respelled `\| item \| value \|` and read by the new one | 17,297 pairs, 0 unreachable, 0 altered by `unescaped` |
| tree-wide line-by-line comparison, old pattern against new, over every tracked file | 1,461 tracked · 1,460 read · 84 lines differ · 83 widen · 1 narrows, at `rounds/round-1-report.md:135` |
| `write_row` over a bare-piped config, then `seal mode local` over the two-deep result | first row `local`, the person's own row still `shared`, `config_rows` returns `local` |
| `missing_row` over ten config shapes — piped first, piped second, other-item refusal hiding the row, no row anywhere, refusal first, two refusals, blank line, second table, indented, three-column | eight correct; the two-refusal shape reports ABSENT while the row is in the file |
| `refusal` and `missing_row` over the two two-refused-line shapes | the row called absent; and *the rows below it were read* while one was lost |
| the proposed repair applied in the clone, then the two test modules and the two shapes re-run | exit 0 · 143 passed; both messages correct; every file restored from bytes |
| `bin/survivor-check` over `c4e9c58b..af5b756c`, `c4e9c58b..HEAD` and `0995f62f..HEAD`, each with and without `--exempt` | exit 0 in all six · *no removed wording is still standing* in all six |
| `bin/evidence-check --strict .` | exit 0 |
| `bin/unverified-check seal/specs/` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:283` | round 1's 1 — fixed |
| round-1 | `hooks/config.py:70` | round 1's 2 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py:265` | round 1's 3 — fixed |
| round-1 | `seal/specs/1789598366-…/changelog.md:20` | round 1's 4 — answered |
| round-1 | `hooks/config.py:156` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_mode_question_is_asked_once.py:189` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_pull_request_language_is_the_repositorys.py:711` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_mode_question_is_asked_once.py:225` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:684` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1789445605-…md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/mode-gate.py` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `survivors.md` silences nothing at any range, including the one CI runs | `seal/follow-up.md`, the `#371` / `#308` row | already deferred — the repository owner. Measured here: `0995f62f..HEAD` reports zero survivors with the file, without `--exempt`, and at every narrower range too. The fix record says this of its two new rows; it is true of all twenty-one, and the cause is the one that row names — the quote joins the range's own added text before `--exempt` is consulted |
| A file already two `Mode` rows deep is repaired by nothing | `overview.md` §*Not done* | already deferred there by round 1's fix pass — the repository owner |
| A pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |
