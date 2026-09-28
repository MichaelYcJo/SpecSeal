# Feature Specification: what the 0.15.5 rounds deferred (#626, #625)

<!-- seal/specs/1790550713-what-the-last-rounds-deferred/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §12 | each item is fixed as a class. The copies and instances are enumerated below by construction, each with a coordinate, and the build re-runs the enumeration before editing |
| `skills/agent-contract/SKILL.md` §14, §15 | a person-read sentence that states a verdict is pinned in the same commit, and every new parameter or case is seen red before it is planted |
| `docs/review-chain-spec.md` §*What the sweep reads, and what it counts as written* — "a released entry is not rewritten" | `CHANGELOG.md`'s 0.15.5 section and the gathered fragment `seal/specs/1790381328-…/changelog.md` stay as they are. This work's own fragment says what the 0.15.5 entry left out |
| `CLAUDE.md` *a change writes fragments, never the shared file* | the changelog entry goes in this work item's `changelog.md`, new ledger rows in `seal/ledger/1790550713-what-the-last-rounds-deferred.md`, and a row an edit drifts is re-read and re-stamped in the release file it lives in, with a dated `Re-read` note |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped* | a release file that conflicts with chain A's or C's squash is resolved hunk by hunk, then `evidence-check` runs |
| Milestone 48's description | a patch release: no new gate. Nothing here adds a refusal, and the completeness case below is a test of one docstring, not a check on anybody's build |

## Scope

Two issues, each carrying its round's paste-ready fix, each widened here to
its class.

### #626 — rule (a)'s glued rule, and the docstring examples with no pin

**Item 1, the order condition.** `refused_coordinate` counts both marks as
one coordinate only where `GLUED_MARKS_RE` finds `#…@`, so an `@` has to
come AFTER a `#`. `@alice#299` and `@types/node#1` are silent, and
`@alice#299@abcdef12` is named, because its `#299@` is glued (read from the
regex, and seen in a probe for this frame, 2026-09-28).

Every place that defines when both marks count, by construction: every
sentence in the tree (rounds excluded) holding *glued*, *both marks*,
*`@` glued after a `#`*, *`@` follows*, *`@` after a `#`* or
`@lru_cache  # memoized`, read in context 2026-09-28.

| Copy | States the order? | This work |
|---|---|---|
| `skills/evidence-check/scripts/evidence_check.py#refused_coordinate`, the docstring's first sentence ("an `@` glued after a `#`") | yes | keep |
| same unit, the third bullet ("Both marks count only where they are glued: no whitespace…") | **no** | correct |
| `evidence_check.py#GLUED_MARKS_RE`, the comment above it ("an `@` after a `#`") | yes | keep |
| `evidence_check.py#malformed_rows`, the docstring's first bullet ("an `@` glued after a `#`") | yes | keep |
| `tests/test_a_row_points_by_content.py#test_prose_marks_beside_a_good_anchor_are_not_refused`, docstring | yes | keep |
| `tests/test_a_row_points_by_content.py#test_a_decorated_line_holding_both_marks_apart_is_prose`, docstring ("the `@` follows the `#`") | yes | keep |
| `tests/test_a_row_points_by_content.py#test_a_coordinate_the_opener_list_misses_is_named`, docstring ("a `#` and an `@` stay glued through a quoted string") | describes named shapes, defines nothing | keep |
| `seal/releases/0.15.5.md`, row S8–S12, claim ("an `@` is glued after a `#`") | yes | re-read only (its anchors drift) |
| `seal/releases/0.15.4.md`, the `MALFORMED` row under `1790297087-…`, the phase-3 `Re-read` note ("an `@` glued after a `#`") | yes | re-read only (its anchor drifts) |
| `seal/specs/1790381328-…/spec.md` §*Scope* item 13 ("an `@` follows a `#`") | yes | keep |
| `seal/specs/1790381328-…/spec.md`, the five-rule trade list, third bullet ("Both marks count only where they are glued") | **no** | correct in place |
| `seal/specs/1790381328-…/changelog.md`, third bullet | **no** | not rewritten: gathered, marker in `CHANGELOG.md` |
| `CHANGELOG.md` §0.15.5, the same bullet | **no** | not rewritten: a released entry |
| `seal/specs/1790381328-…/plan.md` row *Item 4: glued marks*, `questions.md`, `phases/`, `overview.md`, `rounds/` | — | records of a past state, out |

`skills/evidence-check/SKILL.md`, `skills/evidence-ci/SKILL.md`,
`templates/evidence-check.yml` and `docs/` hold no statement of the rule
(searched, 2026-09-28). The shipped spec is corrected rather than left
because `settle` folds a released spec's still-true text into `docs/`, and
`survivor-check` reads it as live prose where it skips the two changelog
copies.

**Item 2, the docstring examples with no pin.** The issue names three that
round 2's rebuild of `GIVEN_UP` dropped. Enumerated by construction for this
frame: every backticked shape holding `#` or `@` in `refused_coordinate`'s
docstring, checked for a test module that carries it. Five of the rules'
examples appear in no case at all:

| Shape | The docstring says | Case today |
|---|---|---|
| `docs/a.md#1.2` | silent (rule 2) | none |
| `src/a.py#1>"x"` | silent (rule 2) | none |
| `Makefile#1x` | silent (rule 4) | none |
| `docs/a.md#1장@abcdef12` | named (rule 2's glued exception) | none |
| `src/a.py#handler @abcdef12` | named (rule 3's word-by-word exception) | none |

The last two are this frame's, not the issue's. Round 3 of 1790381328 looked
for the three it knew had been dropped. The shapes in the docstring's first
paragraph (`#299`, `C#`, `@cache`, `#ifdef`, `chart.js@4`,
`org/repo#299's`, `@lru_cache  # memoized`) are carried by the older named
cases and are outside the rules section this item is about.

So the fix is two parts:

1. Each of the five examples, and the new `@alice#299`, is a parameter of
   the case for its verdict: `GIVEN_UP` for silent, `TAKEN_UP` (or a sibling
   the builder names) for named. `GIVEN_UP`'s comment and
   `test_what_rule_a_gives_up_is_silent_and_says_so`'s docstring say "one or
   two examples of each" and "the verdicts #614 moved". The restored pins make
   both false (rule 2 holds four examples, and `Makefile#1x` did not move), so
   both are reworded in the same commit.
2. **One completeness case**: every backticked shape holding `#` or `@` in
   the rules section of `refused_coordinate`'s docstring (after "What #614
   changed") is a parameter of one of those dicts. Round 2's rebuild would
   have turned it red. It reads the docstring and the dicts. It adds no
   refusal to anybody's build.

### #625 — a comment on `close`'s exit, and ragged docstring lines

**Item 1, the Pass-beside-nobody class.** `round_record.py#run_check`
tells `chain_check` it is judging a draft unless `gh` says the pull request is
ready. In a fixture repository it never says so. Since #598 the pair prints in
a draft and exits 0, and at a ready pull request it fails with exit 1.

Enumerated by construction: every sentence in the tree (rounds excluded) that
holds `` `nobody ``, `by: nobody` or `nobody —` within three lines of *Pass*,
*close*, *exit*, *refus*, *fail*, *notice*, *print*, *draft*, *ready* or
their Korean forms (164 windows, 109 in live prose), read 2026-09-28. Every
sentence of `close`'s exit (*`close` exits*, *still exits*, *exits 1 on*,
*notice about*) was also read.

Two sentences state an exit the local run cannot produce:

| Instance | Sentence | This work |
|---|---|---|
| `tests/test_the_fixes_close_the_record.py#test_re_closing_a_half_restored_record_is_refused_for_every_word`, the comment above the first `close` | "a green `close` still exits 1 on the chain-check notice about `Pass` beside `Fixes checked by: nobody`" | rewrite (the issue's) |
| `tests/test_the_fixes_close_the_record.py#test_a_fix_commit_carries_no_empty_code_span`, the comment above `assert "bare integer"` | "Not `code == 0`: a `fixed` verdict leaves `Pass` beside `nobody` …; this run is judged as a draft, where it prints." Each clause is true, but the opener reads as a reason `close` might exit non-zero here, and judged as a draft it exits 0 | reword the opener (this frame's) |

The rewritten comment has to be true of all three parameters. `fixed` leaves
the pair, which prints. `answered` and `deferred` land on `no fixes to check`,
so no notice prints at all. All three exit 0 as a draft (round 2 of
1790381329, executed). The paste-ready text in that round's report says the
pair prints without the second half, so it is corrected before it is used.

Sentences read and judged true, so nobody reopens them:

- **They state the timing.** `README.md` and `README.ko.md` (the
  `Fixes checked by` paragraph and the bullet under the review chain's
  limits), `agents/sealer.md` §*The command*, `agents/smith.md` (the
  `Fixes checked by` paragraph), `docs/review-chain-spec.md` (three places),
  `docs/round-record-spec.md` (the draft-excuse paragraph, the `nobody — <why>`
  table row, the arm's limit paragraph), `skills/code-review/orchestration.md`
  (the vocabulary table, the #598 window paragraph),
  `skills/implement/orchestration.md` (the delivery row),
  `templates/sdd-round.md`, `chain_check.py` (the module docstring,
  `checked_by`, `fix_surface`, the `strict` paragraph, both message strings),
  `round_record.py#landing_values` and `#run_check`.
- **The fixture is judged as ready.** Three test sentences that say "exits 1"
  or "refused" are true because their `run` passes no payload, so the check
  judges them as ready:
  - `tests/test_the_fixes_close_the_record.py#test_a_correction_closed_answered_lands_on_no_fixes_to_check`;
  - `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, the
    docstring that says ending at round 2 "was refused both ways";
  - the cutoff cases of `tests/test_the_last_rounds_fixes_are_checked.py`.
- **They say "prints" for a grandfathered item.** This holds in both states:
  `tests/test_the_last_rounds_fixes_are_checked.py`'s `ITEM` comment and the
  bold-fix case.
- **They say "never fires" because the verdict closes without a fix.** The
  record helpers in `tests/test_a_record_says_what_ran_it.py`,
  `tests/test_the_fixes_name_their_surface.py` and
  `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`.
- **Ledger rows that say "exits 1".** `seal/ledger.md`'s `>=` boundary row,
  `seal/releases/0.8.1.md` R2 and `seal/releases/0.4.0.md`'s `changed_routing`
  row are dated executions of a ready-judged fixture, or of a tree before #598.
  Every other ledger row about the pair carries *ready* in its note.

**Item 2, the ragged lines.** By construction: every docstring, comment or
string line the #623 range (`6875d64`) added that is over the 88 columns
`ruff.toml` sets, or that holds a mid-paragraph fragment. Five, where the
issue names three:

| Site | Width | Named by |
|---|---|---|
| `tests/test_a_script_copied_alone_exits_2.py`, module docstring ("… In the first four 1 means a finding or a refusal") | 108 | the issue |
| `tests/test_the_fixes_close_the_record.py#test_a_capped_runs_last_record_reads_no_fixes_to_check_and_the_check_exits_zero`, docstring ("(phase 3 measured exit 1 here, before #598). `close` derives …") | 115 | the issue |
| `tests/test_the_gate_hands_cmd_a_path_it_can_run.py#test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points`, docstring, a line holding only "name from the" | 17 | the issue |
| `skills/code-review/scripts/round_record.py#landing_values`, docstring ("of the work item that added this). The other answer was left standing on the grounds that a fix") | 99 | this frame |
| `skills/verify/scripts/unverified_check.py#main`, the `--baseline` help string ("cut is not this branch's removal. Nor is a work item whose fold `docs/` records with ") | 95 | this frame |

Each is re-wrapped with no word changed. The 148 other prose lines over 88
columns in the tree (153 in 58 files, measured 2026-09-28) were not left by
that range and are out.

### Out

- Rewriting `CHANGELOG.md` §0.15.5 or the gathered fragment of 1790381328.
  Grounds: `docs/review-chain-spec.md`, quoted above.
- The 22 other `assert code in (0, 1)` after `close` in
  `tests/test_the_fixes_close_the_record.py`. No sentence beside any of them
  claims exit 1, so they are not #625's class, which is sentences. Tightening
  them is a pin change to cases about other things. Answerer: the
  orchestrator of this run, which files an issue or leaves them.
- A width check for Python prose. It would be a new gate, and a patch release
  adds none (milestone 48). Answerer: the repository owner.
- The files chains A and C edit: `hooks/worktree-guard.py`,
  `hooks/worktree_consent.py`, `docs/worktree-guard-spec.md` and
  `skills/verify/scripts/session_cost.py`.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the order is stated where rule 3 is | Given `refused_coordinate`'s third bullet, then it says the `@` must come after the `#`, and names `@alice#299` as silent | `GIVEN_UP` holds `@alice#299`. Seen red against the current docstring (the `__doc__` assertion), green with the new bullet |
| S2 · the wording is true of a reversed pair followed by a glued one | Given `@alice#299@abcdef12`, then `refused_coordinate` returns True. The bullet must not say an `@` before the `#` makes the text silent while another `@` follows glued | read against the new bullet; the builder executes the call once and says so in the phase record |
| S3 · the three dropped pins are back | Given each mutant of round 3's ⬜ 2 (the dotless branch takes `isalnum`; `ISSUE_TAIL_RE`'s lookahead also refuses `.`; also refuses `>`), then the parameter for `Makefile#1x`, `docs/a.md#1.2` or `src/a.py#1>"x"` goes red | each mutant applied alone, then the file restored from bytes kept first |
| S4 · the two named examples are pinned | Given `docs/a.md#1장@abcdef12` and `src/a.py#handler @abcdef12`, then a case asserts each is named and is in the docstring | seen red with the example deleted from the docstring, and with the named branch it relies on disabled (`GLUED_MARKS_RE` not searched; the per-word `/` or `.` path test) |
| S5 · the docstring cannot lose a pin again | Given the rules section of `refused_coordinate`'s docstring, then every backticked shape holding `#` or `@` is a parameter of `GIVEN_UP` or `TAKEN_UP` | the completeness case, seen red against today's dicts, which lack five shapes |
| S6 · the shipped spec agrees | Given `seal/specs/1790381328-…/spec.md`'s trade list, then its third bullet carries the order condition, and the edit is marked with the date and this work item | read; `survivor-check` over the range reports no survivor of the old bullet in live prose |
| S7 · the comment says what `close` does | Given the first `close` in `test_re_closing_a_half_restored_record_is_refused_for_every_word`, then its comment says: a draft judgment and exit 0 for all three words; the pair's notice only under `fixed`; exit 1 only at a ready pull request | the assertion temporarily tightened to `code == 0`, green for all three parameters, then restored. With `run_check`'s draft payload removed (a mutant), the `fixed` parameter exits 1 |
| S8 · the sibling comment says the same | Given `test_a_fix_commit_carries_no_empty_code_span`, then its comment says the exit is not what the case judges, and gives the draft and ready outcomes the same way S7 does | read |
| S9 · no ragged line is left by #623 | Given the five sites, then each paragraph is re-wrapped under 88 columns with its words unchanged | a probe comparing each paragraph's words before and after (whitespace-normalised equal), and one listing the #623 range's prose lines over 88 at the tip: none left |
| S10 · the `--baseline` help renders the same | Given `unverified_check.py --help` before and after, then the two outputs are byte-identical | both rendered and compared; `tests/test_unverified_rows_close.py` passes |
| S11 · the ledger stays true | Given every row whose anchor this work edits, then each is re-read, re-stamped with a dated note, and `evidence-check` reports 0 drifted | `bin/evidence-check .` at the build tip |

## Data & interfaces

- **Behaviour.** None changes. No verdict, exit code or output line moves.
  What moves is one docstring a person reads to learn which shapes are
  silent, test comments and docstrings, one help string's source layout, and
  the cases.
- **Ledger, re-read.** Rows expected to drift, from the units they cite. The
  build confirms with `evidence-check`:
  - `seal/releases/0.15.5.md`: S8–S12, C3, C5.
  - `seal/releases/0.15.4.md`: the `MALFORMED` row under
    `1790297087-…`, and S1 under `1790297086-…`.
  - `seal/releases/0.14.0.md`: G5.
  - `seal/releases/0.12.1.md`: R2.
  - `seal/releases/0.11.4.md`: the row starting "The cut that removes a fix
    commit", and the row starting "`close` writes both of
    `landing_values`' answers".
  - `seal/releases/0.10.0.md`: S13.
  - `seal/releases/0.9.3.md`: R1.
  - `seal/releases/0.8.1.md`: R2.
  - `seal/releases/0.5.0.md`: S7.
  - `seal/releases/0.4.0.md`: the row starting "the checker and the
    unverified reader at the close of the fix pass".

  Fourteen rows in all. None of their claims is about wording this work
  changes, except S8–S12's Notes. They say the rules are stated in
  "`changelog.md`", and "a case holds one or two examples of each". The
  re-read note says what changed.
- **Ledger, new.** In `seal/ledger/1790550713-what-the-last-rounds-deferred.md`,
  which does not exist yet:
  - the order condition as rule 3 now states it, with `@alice#299` silent;
  - the completeness case holding the rules' examples to the dicts.
- **Changelog.** One fragment,
  `seal/specs/1790550713-what-the-last-rounds-deferred/changelog.md`. It
  says `evidence-check`'s statement of when `#` and `@` count as one
  coordinate now says the `@` must follow the `#`, and that 0.15.5's entry
  left that condition out.

## Open questions → questions.md

None needs a person, and none blocks the build. `questions.md` holds two
measurements and two items the work settles, each with the default the build
proceeds on, and lists the judgments the issues left open that the tree
answered.

Framed 2026-09-28 by framer, before the build.
