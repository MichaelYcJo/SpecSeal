# 1790683267-a-rider-read-ends-where-the-hasher-cuts — review round 2

| Field | Value |
|---|---|
| Target SHA | b87eb589940cddc344565c53101d8bd53a16899b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #683 — https://github.com/MichaelYcJo/SpecSeal/pull/683 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2, verifying, over round 1's fix range `91f0c949..c6ac02b3` at HEAD `b87eb589`. Asked whether each of round 1's five verdicts is closed. It pushed hardest on ⬜ 5, which changed shipped behaviour:
- every printed location against an independent editor line count;
- anything that reads a printed location back as a piece index;
- the new `Rider` field's reach into equality, sorting and consumers.

Also asked for K1 re-measured at HEAD, K2's correction and the new K3 row, the three ledger checks, and the interpreter floor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — `comment_blocks`' docstring states the block rule the reader keeps, a continued HTML comment included | `.github/scripts/rider_check.py:302` | confirmed | read: the paragraph is the report's text; no code in the unit changed over the range |
| 🟢 | round 1's finding 2 is closed — G13 and P5-1 carry the correction after this item's own | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` G13; `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` P5-1 | confirmed | read: one note on each row; executed: `evidence-check --strict` exit 0 |
| 🟢 | round 1's finding 3 is closed — `region_lines`' comment names the shared GFM lines | `.github/scripts/rider_check.py:490` | confirmed | read: the comment, the `overview.md` sentence and S2's re-stamp |
| 🟢 | round 1's finding 4 is closed — the oracle case holds the reader's own GFM-lines path | `tests/test_the_hooks_hide_what_a_renderer_hides.py:745` | confirmed | executed: red on 273 documents with `gfm_places` numbering pieces, green restored |
| 🟢 | round 1's finding 5 is closed — every printed rider location is the GFM line | `.github/scripts/rider_check.py:383` | confirmed | executed: 299,363 riders and 12,438 printed lines from check, `--migrate`, `--reverify` and check against an independent CRLF/CR/LF count, 0 wrong; the probe fails under the old `where`; `migrated` and the length error forced separately; the two cases 24 red at `91f0c949` |
| 🟢 | nothing reads a printed location back as a piece index, and the new field changes no consumer | `.github/scripts/rider_check.py:374` | confirmed | read: twelve `where()` callers, all prints; no equality or ordering method; one constructor call; executed: riders and writes identical to `91f0c949`, `inferred_anchor` identical |
| 🟢 | the fix range's new unit is correct | `tests/test_every_reader_ends_a_line_where_gfm_does.py:1129` | confirmed | read: one break above each rider, marker built from parts; executed: 8 of 8 red at `91f0c949`, the tree still reads 18 riders |
| 🟢 | K1 holds at HEAD | `.github/scripts/rider_check.py:387` | confirmed | executed: 30,000 texts, 150,354 riders, 0 off the cut; 3,883 of 9,000 reads fail under a piece-numbering mutant |
| 🟢 | K2's correction and K3 are true, and the three ledger checks agree | `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md` K2, K3 | confirmed | executed: `evidence-check --strict` exit 0, `correction-check` exit 0, `survivor-check` exit 0 with the exemptions and 1 without; K3 omits `migrated` from its list, narrower and not false |
| 🟢 | the shipped script stays on the interpreter floor | `.github/scripts/rider_check.py:629` | confirmed | read: no `zip(`, `pairwise` or `.UTC`, comments included; executed: the floor case and ruff |
| ⬜ 1 | `round-1.md`'s Deferred table still offers round 1's finding 5 as a candidate issue after the fix pass fixed it | `seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/rounds/round-1.md` `## Deferred` | open | read: the verdict row says `**fixed** bda0e0ba` and the Deferred row asks the orchestrator to file it; a correction to paperwork, outside `Needs a fix` |

## Paste-ready fixes

```markdown
| ⬜ 5 — a rider's printed location is a `str.splitlines` number, older than #664 | fixed in this run at `bda0e0ba`; confirmed by round 2 — no issue | nobody: closed |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_the_hooks_hide_what_a_renderer_hides.py`, `tests/test_a_script_says_which_interpreter_it_needs.py` at `b87eb589` | 353 passed, exit 0 |
| `91f0c949`'s `rider_check.py` put in the clone, the printed-line case and the verdict case run, then restored | 24 failed: 8 printed-line and 16 verdict, all on the location |
| `gfm_places` mutated to return piece numbers, the oracle case run, then restored | 1 failed, "273 documents"; 3 passed once restored |
| the location differential, reader level, HEAD and `91f0c949` loaded side by side | 60,000 texts, 39,798 with one of the eight, 299,363 riders, 186,056 with line and piece number apart; 0 wrong, 0 differing riders |
| the location differential, end to end through `main()` as check, `--migrate`, `--reverify`, check | 60 trees, 2,102 files, 12,438 location lines, 7,484 moved; 0 wrong, 0 raised, files byte-identical between versions |
| the same with `where` printing `rel:start` | reader level 936 of 1,575 wrong; end to end 248 of 373 wrong |
| `--migrate` writing in a git repository, rider at piece 5 on GFM line 3 | `migrated hooks/m.py:3 -> a@0e31ba39`, exit 0 |
| `write_block` with a body one piece too long, rider at piece 3 on GFM line 2 | `hooks/w.py:2: the body has 2 pieces and the rider 1 lines` |
| K1, reader against hasher at HEAD, with `inferred_anchor` compared to `91f0c949` | 30,000 texts, 150,354 riders, 0 wrong; 23 anchors named, 0 differ; under the piece-numbering mutant 3,883 of 9,000 reads wrong |
| `rider_check.py --root .` with each version | identical, `18 ok · 0 drifted · 0 broken`, exit 0; 0 of 18 riders have line and piece number apart |
| `bin/evidence-check --strict .` | `total: 3084 ok · 0 drifted · 0 broken`, exit 0 |
| `bin/correction-check --range origin/release/v0.16.0...HEAD` | 1 merge examined, no marker dropped, exit 0 |
| `survivor_check.py --range origin/release/v0.16.0...HEAD` with every `survivors.md` through `--exempt` | 1 exempt, exit 0; without the exemptions exit 1 on the same place |
| `chain_check.py --baseline origin/release/v0.16.0` | exit 1, judged as a ready pull request with no event payload: `Broad gate` is `not yet`, and `Fixes checked by` names nobody. The first is the sealer's cell. This round's record fills the second |
| `ruff check` and `ruff format --check` on the three changed Python files | clean, exit 0 |
| the broad gate: the full suite, repository-wide lint and typecheck over this branch | not yet — not run by this round. It is the sealer's, and it comes due now, since nothing here needs a fix |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/rider_check.py:307` | round 1's ⬜ 1 — answered |
| round-1 | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` G13; `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` P5-1 | round 1's ⬜ 2 — answered |
| round-1 | `.github/scripts/rider_check.py:476` | round 1's ⬜ 3 — answered |
| round-1 | `tests/test_the_hooks_hide_what_a_renderer_hides.py:753` | round 1's ⬜ 4 — fixed |
| round-1 | `.github/scripts/rider_check.py:374` | round 1's ⬜ 5 — fixed |
| round-1 | `.github/scripts/rider_check.py:377` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/rider_check.py:236` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/rider_check.py:341` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/rider_check.py:410` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_every_reader_ends_a_line_where_gfm_does.py:1024` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the `-->` shape's sentence "no verification stamp" when a stamp sits outside the comment | not placed: a message improvement, outside this item's class; already deferred in round 1 | the orchestrator, if the owner wants the message to name the case |
