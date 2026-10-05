# 1791119070-a-waiver-inside-a-here-document-body-is-data — review round 1

| Field | Value |
|---|---|
| Target SHA | b414c7200b82fa78e57849cf1af0736ef4e57320 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #783 |
| Broad gate | 64b306a0 against 94d7b2e0 |
| Fixes checked by | no fixes to check |
| Fix range | `7df09f5568f75653928fa5837f340458b81be338..669e66866afd812c41fe030ffc9c970fe97b647f`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #773 (PR #783), at b414c720 against `release/v0.18.2` (94d7b2e0): spec compliance first, then quality. Judge whether both consent reads (`has_marker`, `tokens.given`) leave here-document bodies out and whether a third waiver read on the commit gate's path was missed; whether the direction claim (base read AND the body-free read, so only silence-to-stop) holds by structure; whether the surviving mutation M2 (skipping `one_heredoc.reduce`) marks a dead branch; and the smith's two corrections to the frame's plan coordinates. Judged by the gate's decision functions only; no command that commits through a bypass is run, and shapes are described in words.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `without_bodies`' `reduce` branch is equivalent to `drop_heredoc_bodies` on every admitted string, so M2 survives by construction; the docstring does not say so | `hooks/tokens.py:74` | answered | Kept as the frame decided: the reviewer's own reading is that the branch is equivalent today and buys protection if `_heredoc_split`'s boundaries move; a docstring note changes no behaviour and would spend the reopening on a verifying round for prose.; Executed: 13,308 admitted variants, zero text or verdict differences. Read: clauses A–D of `hooks/one_heredoc.py` leave `_heredoc_split` in its neutral state at the opener's newline with the same delimiter and the same terminator test |
| ⬜ 2 | The `classify` correction left `spec.md:79` naming the old coordinate, and phase 2 and the overview call worktree-guard's `classify` "the only" one while `hooks/dispatch.py:207` holds another | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/spec.md:79` | answered | A correction to records, not a code fix: `spec.md` §Out now names `hooks/worktree-guard.py#classify`, and `phases/phase-2.md` and `overview.md` say "the one beside `switch_kind`" instead of "the only one" (669e6686).; Read: grep for `def classify` over `hooks/`. Paperwork, a correction |
| ⬜ 3 | The changelog says one stop is new; `spec.md` case 5 is a second | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/changelog.md:14` | answered | A correction to a record: `changelog.md` names the rarer stop of `spec.md` case 5 and no longer counts one (669e6686). The reviewer's grounds for leaving case 5 unpinned are adopted.; Read against `spec.md` case 5. Paperwork, a correction |
| ⬜ 4 | `has_marker` recomputes `without_bodies` per marker and per target | `hooks/commit-review-gate.py:686` | answered | Cleanup with no defect: each pass is microseconds on a command-sized string, and the reviewer names the cheaper shape for whoever next touches `has_marker`.; Read: call sites at `:1122` (per arm, per target) and `:1418`. Cleanup only |
| 🟢 | Both consent reads on the commit gate's path leave here-document bodies out, and the class holds no third read | `hooks/commit-review-gate.py:686`, `hooks/tokens.py:86` | confirmed | Read: every reader of the two tokens enumerated from `gate.TOKENS` and `tokens.KNOWN`; `commitgate.waived` reads stored files and git config, not text. Executed: the new cases are red at the base hooks and green at the target |
| 🟢 | The new reads can only refuse, by structure | `hooks/commit-review-gate.py:686`, `hooks/tokens.py:86`, `hooks/gate.py` `arms_missing` | confirmed | Read: AND and intersection with the base read, and every consumer monotone in the waived set. Executed: 60,000-string fuzz, no exception and no newly honoured token |
| 🟢 | The two corrected `plan.md` coordinates are right | `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/plan.md` §*Operational impact* | confirmed | Read: `seal/releases/0.17.0.md:77` cites `given` at `e436fefe`; sibling D's branch edits `hooks/worktree-guard.py#classify`; `hooks/cmdline_base.py` has none |
| 🟢 | A body token cannot reach the git hook end to end | `hooks/answers.py:134`, `hooks/commitgate.py:83` | confirmed | Read: `answers.write` stores only what `given` returns, and nothing downstream reads command text for a token |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` and `tests/test_the_old_spellings_reach_the_hook.py` at `b414c720`, in the clone | 306 passed |
| The same two modules, `-k` on the S1/S2/S3/S5/S6 cases and `test_a_token_is_a_bare_word_and_nothing_else`, with `hooks/tokens.py` and `hooks/commit-review-gate.py` checked out at `94d7b2e0` over the target tree, then restored | 7 failed (S1, the three S2 openers, S5, `given`'s two body rows), 17 passed |
| A pure-function probe (one temporary test file, run once, deleted): for 13,308 admitted variants of `corpus` and `program_corpus` with the token on each body line, compare `reduce`'s text with `drop_heredoc_bodies`' text with the opener's redirect removed, and compare `_reads_marker` and the known-token sets between them | 0 text differences, 0 verdict differences |
| The same probe: 60,000 random strings from shell-significant pieces, seed 773; call `has_marker` and `given`, and compare each with its base read | 0 exceptions; 0 strings where a new read honours a token its base read did not |
| The same probe: one hand-built case-5 attempt, an ANSI-C-quoted word ahead of a line carrying the token | no body found; both reads keep the token, as at the base. Case 5 not reached |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet — not run by anyone at this SHA; it belongs to the sealer, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
