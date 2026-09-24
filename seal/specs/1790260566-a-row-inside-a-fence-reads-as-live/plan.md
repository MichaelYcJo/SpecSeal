# Implementation Plan: a reader's fence and comment state (#444, #491, #487, #220)

Approved <date> by <who>, when `smith` was spawned.

## Summary

The work creates one fence-delimiter rule, written to CommonMark 4.5, in
`skills/verify/scripts/unverified_check.py`. It lives there because every
reader in scope already loads that module, or can. The rule then goes in
front of each reader that decides row-ness, marker-ness or claim-ness by
line. The "live" rule stays with `live_lines`, but only for lines that
excuse something. A line that holds something (an anchor, an open row, a
claim) is skipped only when it is certainly quoted.
`spec.md` §*The direction rule* holds the argument.

There are four phases, and each one ships a verdict change with its own
cases, documents and ledger rows. Phase 1 comes first because phases 2 to 4
use its rule.

## Technical context

The code this builds on, anchored by unit (read 2026-09-24 at `baa1416f`):

- `skills/verify/scripts/unverified_check.py#blank_fences`: its opener regex
  is `^\s*(`{3,}|~{3,})`, and a closer may carry trailing text. It reaches
  `readable`, and through `readable` it reaches `check_text`, 13 call sites
  in `chain_check.py`, the `reader.*` calls in `round_record.py`, and
  `hooks/review-history-guard.py`.
- `unverified_check.py#FENCE_RE` (bounded) and `#_liveness`: a closer is
  matched with `FENCE_RE.match` and nothing about what follows it is
  checked.
- `unverified_check.py#_paragraph_ends_at`: `s = line.strip()` and then
  `s.startswith("#")`, with no indentation bound. The oracle
  `tests/test_unverified_rows_close.py#block_ends_at` bounds the heading
  branch at `indent <= 3`.
- `hooks/config.py#FENCE` / `#fence_map`: the CommonMark-complete rule, with
  its grounds in the comment above `FENCE` (#429).
- `skills/evidence-check/scripts/evidence_check.py#check_text`,
  `#old_format_rows`, `#migrate` and `#reverify`: each walks
  `ANCHOR_RE.finditer` or `splitlines()` over a whole ledger file, with no
  fence state. `#reverify` and `#migrate` rewrite by match position, so any
  blanking must keep character offsets.
- `evidence_check.py#claim_lines`: `lstrip().startswith("```")`, where a
  3-character mark is compared for equality, so a ```` ```` ```` block is
  closed by ```` ``` ````. An aside opens only when `stripped.startswith("<!--")`
  and ends by `continue`ing past the whole line that holds `-->`.
- `unverified_check.py#todo_open_rows` and
  `.github/scripts/fold_ledger.py#open_rows`: the same code, character for
  character, and neither has fence or comment state. `settle.py#open_rows`
  already delegates to the first.
- `skills/code-review/scripts/survivor_check.py#gathered_fragments`: `MARKER.findall`
  over `CHANGELOG.md`. The module already loads the reader (`READER`).
- `skills/settle/scripts/settle.py#anchored_rows` reads every line on
  purpose, and its docstring names #444.
  `tests/test_settle_reads_before_it_removes.py#test_a_fenced_anchor_still_keeps_the_directory`
  pins that, and it must stay green.
- The precedent for `.github/` loading a shipped script:
  `.github/scripts/rider_check.py` loads `evidence_check.py` through
  `importlib.util.spec_from_file_location`.

**What breaks in six months.** The next reader is written with its own fence
regex, because nothing makes it ask the shared one. That is how five
spellings came to exist. The agreement case (S6) holds only
`hooks/config.py` in step with the shared rule, and it cannot reach a reader
that does not exist yet. What reaches that reader is the docstring of the
shared function, which names every caller. So the build writes that list
into the docstring, and a reviewer of the next reader has a place to look.
This is a sentence, not a check, and the plan says so rather than claiming
more.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Make `live_lines` the single liveness for every reader, including the checker and the open-rows guard | Its ambiguous line is settled as not live. For the checker, a real row after an unpaired backtick is skipped and a BROKEN anchor goes unreported. For the guard, a real open row is skipped and the fold proceeds. Both are silent. `settle.py#anchored_rows` already moved off `live_lines` for exactly this reason (#511 round 1, finding 1) | rejected |
| Fix each reader's own regex where it stands | Five spellings stay, and they drift again. #491 exists because the bound landed on `FENCE_RE` and not on `blank_fences` in the same file | rejected |
| Make `hooks/config.py#FENCE` the one definition, loaded by every reader | The leaf reader that everything loads (`unverified_check.py` imports only the standard library) would begin to load from `hooks/`. A change to the config reader would then move five skill gates, and `config.py` runs on the hook path | rejected |
| **Put one delimiter rule in `unverified_check.py`. Each walk keeps the state its question needs. The direction rule decides the unclosed and ambiguous cases. `hooks/config.py` is held in step by an agreement case** | The shared rule turns out wrong for a shape that `config.py` gets right. The agreement case catches that the moment the two differ | **chosen** |
| #487 as the ticket proposes: a walk comparing the two functions' source and constants | It holds two texts in step and keeps two definitions. The ground for the copy was that `.github/` may not depend on a shipped script, and `rider_check.py` already does | rejected |
| **#487 by a load: `fold_ledger.py` asks `todo_open_rows`** | If a later change moves `unverified_check.py` or renames the function, the fold fails at load with a traceback at the release. That is loud, and the S8 case names it first | **chosen** |
| #220 and the records-arm aside row, widened: `claim_lines` reads through a positional scanner with code-span state, so a comment opening mid-line is an aside | A `<!--` quoted in backticks mid-line would open an aside and silently drop every claim until the next `-->`. It took `live_lines` five review rounds to model this, and this repository's records quote `<!--` in backticks all the time | rejected by default (Q1) |
| **#220 narrowed: a closer is a position and the rest of the line is re-read. An aside opens where a line, or the remainder after a closer, BEGINS with `<!--`. The skill's sentence says so** | A name inside a comment that opens mid-line is read as a claim. That is a false refusal at exit 2, which a person sees and answers with the `NAME NOT IN TREE` marker | **chosen by default**, and Q1 is where a person overturns it |

## Phases

Each phase carries the four items `CONTRIBUTING.md` §*What a change to a
gate must carry* requires, and writes them in its `phases/phase-N.md`:
the case seen red and how it was shown, the direction and why it is the
cheaper mistake, a prompt budget of **0** (nothing here asks anybody
anything), and the platform note (pure text processing, no process
inspection; checked on macOS only, and CI runs Linux). Each phase also adds
its line to `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/changelog.md`
and its rows to the ledger fragment. It re-reads and re-stamps, in the file
it lives in, any existing ledger row whose anchored unit it edited, and names
those rows in its phase record.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **One fence-delimiter rule, bounded (#491).** Adds the CommonMark 4.5 delimiter rule to `unverified_check.py`. `blank_fences`, `_liveness` and `_paragraph_ends_at` use it, and `_paragraph_ends_at`'s ATX branch gets the three-space bound. Rewrites the comments above `FENCE_RE` and the "`blank_fences` knows / keeps" sentences in `settle.py#coordinates` and `live_lines`. Adds the agreement case against `hooks/config.py#fence_map` (S6). **Direction:** `readable` blanks fewer lines, so `check_text`, `chain_check` and `round_record` read more, which is the loud direction. `live_lines` either extends a fence (a closer with an info string no longer closes it: fewer live lines, safe for the fold) or no longer opens one (a backtick info string holding a backtick: more live lines, which Q2 measures) | S4, S5 and S6 as cases, each seen red against `c52e8350`'s code. A 4-space `# x` case on `_paragraph_ends_at`, seen red. Narrow runs of `tests/test_unverified_rows_close.py`, `tests/test_chain_hooks.py`, `tests/test_the_record_is_generated.py`, `tests/test_settle_reads_before_it_removes.py` and `tests/test_chain_check_at_the_pull_request.py`. Q2's measurement recorded in `phases/phase-1.md` with every moved line judged | |
| 2 | **The ledger walks skip a closed fence (#444).** `evidence_check.py` loads the reader and uses phase 1's rule in `check_ledger`/`check_text`-over-a-file, `old_format_rows`, `migrate` and `reverify`. A closed fence's lines are not read, an unclosed fence's lines are, and character offsets are kept for the two writers. `skills/evidence-check/SKILL.md` states the ledger rule. `docs/the-evidence-ledger.md`'s "because the checker reads those too" and `settle.py#anchored_rows`'s future-tense #444 sentence are corrected, and the behaviour stays. The `#444` row leaves `seal/follow-up.md`: the two readers it left unmeasured (`round_record.py` and `chain_check.py`) both read through `readable` and carry phase 1's rule, and one probe each confirms a fenced example row is not read. **Direction:** the checker reads fewer lines, which allows more. That is justified only for a closed fence, which is a certain quotation. The unclosed case is S3 | S1, S2 and S3 as cases, S1 and S2 seen red. `test_a_fenced_anchor_still_keeps_the_directory` still green. The two probes named in `phases/phase-2.md` and deleted. Q3's count recorded | |
| 3 | **One open-rows rule, and an excusing line must be live (#487).** `fold_ledger.py#open_rows` becomes a load of `todo_open_rows`, and its copy and the docstring clause "it may not depend on this" go. `todo_open_rows` takes `drained` only from a line `live_lines` calls live, and reads no row inside a closed fence (phase 1's rule), while rows inside a comment stay read. `survivor_check.py#gathered_fragments` counts a marker on a live line only, as `folded_items` does. The docstrings of `todo_open_rows` and `settle.py#open_rows` are corrected, and so is `fold_ledger.py`'s module docstring rule 2 ("wherever it stands"). **Direction:** `drained` and the marker now block more, which is safe. A fenced row allows more, which is the same justification as phase 2 | S7 (both commands), S8 and S9 as cases, each seen red. Narrow runs of `tests/test_the_ledger_fragments_fold_at_release.py`, `tests/test_settle_reads_before_it_removes.py`, `tests/test_release_hygiene.py` and the survivor-sweep module | |
| 4 | **A closer is a position (#220), and the fence rule in the records arm.** `claim_lines` re-reads the remainder after `-->` by the line's own rules, so a reopened comment reopens and a claim after the closer is read. Its fence recognition uses phase 1's rule (the bound, the character, the length, and a closer with no info string). Under that rule, #220's fence half ("a name after a closing fence on the fence's own line") is not a closer at all, so the line is fence content, and the phase records that. The text returned is what lies outside the regions, and `NOT_IN_TREE` is still tested on the raw line. `skills/evidence-check/SKILL.md` §*What counts as a claim* is narrowed per Q1's default, and the records-arm aside row leaves `seal/follow-up.md`. **Direction:** claims after a closer are read, which refuses more (loud). A reopened comment reads less, which is correct by the documented rule | S10, S11 and S12 as cases, each seen red. The existing `tests/test_a_record_states_what_the_tree_has.py` stays green. Q5: the records arm's `names read` count over this tree before and after, with any new refusal judged | |

## Operational impact

- No migration, environment variable or dependency. Two new load edges:
  `evidence_check.py` → `unverified_check.py`, and `fold_ledger.py` →
  `unverified_check.py`. `evidence-check` from an installed plugin now needs
  `skills/verify/scripts/` beside it, which the plugin layout ships
  (`settle.py` already relies on the same layout).
- **A ledger row inside a fence is no longer checked.** A repository whose
  ledger holds a real claim inside a fence loses that check silently. Q3
  measures this tree. The changelog fragment says so to adopters in one
  sentence.
- **Merge risk with two parallel chains.** `1790260565` (#501, #568) and
  `1790260563` (#530) are on sibling branches of `release/v0.15.3`. The
  first may edit `evidence_check.py` or `settle.py`, and the second edits
  `settle.py#first_cell`. This plan does not touch `first_cell` or a row's
  cell parsing. Where either lands first, this branch merges the release
  branch in rather than rebasing (memory of 0.15.0), and resolves any ledger
  conflict hunk by hunk.
