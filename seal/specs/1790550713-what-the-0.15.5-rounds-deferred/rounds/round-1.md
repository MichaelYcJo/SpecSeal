# 1790550713-what-the-0.15.5-rounds-deferred — review round 1

| Field | Value |
|---|---|
| Target SHA | 159d5d46638dfcd4a9e6412516aaab1030245eb5 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 631 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of the build, at the branch's tip after the smith's three phases. The round was asked to enumerate every live copy of the glued rule and every sentence stating what `close` or the Pass-beside-`nobody` rule does on a draft against a ready pull request, including the outcome words. It was also asked to break the completeness case and each new parameter by mutation, to check that the re-wraps change no word and leave `--help` byte-identical, and to run `evidence-check` over the whole tree.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | "An `@` before a `#` is not glued to it, so `@alice#299` is prose" reads as if the order alone silences it; `@alice#handler` has the same order and is named | `skills/evidence-check/scripts/evidence_check.py:1651-1653`, `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md:189-190` | open | Executed: `refused_coordinate("@alice#handler")` is True. The bullet's next sentence covers it, so nothing stated is false |
| ⬜ 2 | The 0.11.4 note says the re-wrapped line held three words; it held four | `seal/releases/0.11.4.md:61` | open | Read: the base line was `pull request — a reader`. A correction to paperwork, outside `Needs a fix` |
| 🟢 | #626 item 1: every live statement of the glued rule states the order or only describes named shapes, and each is true of a second trailing `@` | `skills/evidence-check/scripts/evidence_check.py:1618-1657,1744`, the 1790381328 `spec.md:187-195` | confirmed | Executed: class grep and `refused_coordinate` on nine shapes. The released copies stay, with grounds at `docs/review-chain-spec.md:927` |
| 🟢 | #626 item 2: all 21 rule examples are parameters, and each restored or new pin fails alone under its mutant | `tests/test_a_row_points_by_content.py:1209-1244` | confirmed | Executed: eight mutants, each applied alone over the module |
| 🟢 | The completeness case reads the loaded docstring and fails on a new unpinned example | `tests/test_a_row_points_by_content.py:1290-1308` | confirmed | Executed: an added example turned this case alone red. The two escapes it has are the two its docstring names |
| 🟢 | #625 item 1: both comments state the draft and ready outcomes as they are | `tests/test_the_fixes_close_the_record.py:710-714,2326-2333` | confirmed | Executed: the draft/ready probe over the four fixtures. `in (0, 1)` kept on the grounds at `plan.md:65` |
| 🟢 | #625 item 2: six re-wraps change no word, and `--help` is byte-identical | `round_record.py:1537-1544`, `unverified_check.py:1380-1386`, four test docstrings | confirmed | Executed: word comparison per hunk, and `--help` at two widths |
| 🟢 | The ledger re-stamps hold over the whole tree | the 11 `seal/releases/*.md` files, `seal/ledger/1790550713-what-the-0.15.5-rounds-deferred.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted. Each note was read against its edit (⬜ 2 aside) |

## Paste-ready fixes

```
    - Both marks count only where they are glued: an `@` after a `#`, with
      no whitespace between them outside a quoted string, which holds
      whitespace only in a code span, and no `"` left unclosed. An `@`
      before a `#` is not glued to it, so `@alice#299` is judged word by
      word, where `#299` is an issue number, and `@alice#299@abcdef12` is
      named by the `@` that follows its `#`. Where they are not glued each
      word is judged alone, so `src/a.py#handler @abcdef12` is still named,
      and `@lru_cache  # memoized`, `#handler @abcdef12`,
      `docs/a.md#1-scope @abcdef12` and `#handler>"a"b"@abcdef12` are not.
```
```
held four words
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_row_points_by_content.py tests/test_the_fixes_close_the_record.py -q` at `159d5d4` | 277 passed, exit 0 |
| `bin/test tests/test_unverified_rows_close.py -q -k baseline_help` | 1 passed, exit 0 |
| `bin/evidence-check .`, unscoped | 2469 ok · 0 drifted · 0 broken · 0 malformed; records arm 0 refused; exit 0 |
| Nine mutants of `evidence_check.py`, each alone, module run, bytes restored | the eight code mutants as tabled under *Every example the rules give has a case*; the added docstring example failed the completeness case alone |
| Draft/ready probe of `close` over the three words and the sibling fixture | draft: all exit 0, the notice only under `fixed`; ready: all exit 1 on `Broad gate`, `fixed` on the pair too |
| Completeness count: the docstring's rules-section shapes against the dicts | 21 at the target, all pinned; 9 missing at `0e475b1` |
| Word comparison of the eight changed hunks in the six re-wrapped files | six re-wrap hunks equal; the two #625 comment hunks differ, as rewrites |
| `unverified_check.py --help`, base against target, same file name | byte-identical at `COLUMNS=80` and `COLUMNS=200` |
| Width scan: `.py` lines over 88 added by this branch, and by `6875d64` still at the target | none |
| `uvx ruff check`, `uvx ruff format --check` on the eight changed `.py` files | exit 0 each |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's. This round leaves nothing that needs a fix, so it comes due once the orchestrator has written this round's record, and the next act is the sealer's spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
