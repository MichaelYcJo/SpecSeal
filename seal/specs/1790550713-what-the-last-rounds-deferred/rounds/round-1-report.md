# Review round 1 — `test/625-626-the-deferred-sentences-and-pins`

Target SHA `159d5d4` (`159d5d46638dfcd4a9e6412516aaab1030245eb5`), base
`origin/release/v0.15.6` at `2037cf0`. This is a first round, so its target is
the branch, and no earlier `round-N.md` exists to carry from. The review ran
in a `git clone --no-local` at the target under the session scratchpad. Every
probe ran there, and the clone and its probes are deleted.

The account I was handed (the spawn prompt, `spec.md`, `plan.md`,
`questions.md` and the three phase records) was read in full and treated as
claims. Every claim this report relies on was checked against the code or
re-run. Where I re-ran a claim, the report says so.

How the findings relate:

```
#626 item 1: the glued rule did not state the order of the marks
  ├ the rule's statement now states it, in every live copy       (🟢)
  │   └ the new "so" clause reads as if the order alone silences  (⬜ 1)
  └ #626 item 2: rule examples without a case
      ├ 13 silent + 8 named parameters, each red under its mutant  (🟢)
      └ a completeness case holds the rules section to the dicts   (🟢)
#625 item 1: a comment said `close` exits 1 where it exits 0
  └ both comments now say what draft and ready produce, measured   (🟢)
#625 item 2: ragged lines left by #623
  └ re-wrapped, no word changed, --help byte-identical             (🟢)
the ledger re-stamps that follow the edits
  ├ evidence-check over the whole tree: 0 drifted, exit 0          (🟢)
  └ one Re-read note miscounts the words it describes              (⬜ 2)
```

Nothing this round found needs a fix.

## The rule now states the order, and every live copy agrees

**#626 item 1.** `refused_coordinate`'s third rule now says the two marks count
as one coordinate only where an `@` comes after a `#`. It also says
`@alice#299` is prose and `@alice#299@abcdef12` is named
(`skills/evidence-check/scripts/evidence_check.py:1649-1657`). The code is
unchanged: the diff of that file touches only the docstring (read).

I ran the class search myself rather than inheriting the frame's table. A
`git grep` for *glued*, *both marks*, *one coordinate*, and an `@` after or
before a `#`, with round records excluded, returned these live statements of
the rule (executed):

- the `GLUED_MARKS_RE` comment (`evidence_check.py:1618`);
- the first sentence of `refused_coordinate` (`:1632`), and its second and third bullets;
- `malformed_rows`' first bullet (`:1744`);
- the two test docstrings at `tests/test_a_row_points_by_content.py:1053` and `:1186`;
- `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md:129-135` and `:187-195`;
- the two new ledger rows;
- the released copies in `CHANGELOG.md:60` and 1790381328's gathered `changelog.md:34`.

Each live copy either states the order (an `@` after or following a `#`) or
only describes named shapes. Each one is true of a second trailing `@`,
because none says an `@` before the `#` silences the whole text. The two
released copies still leave the order out. The frame left them standing on
the grounds of `docs/review-chain-spec.md:927`, "a released entry is not
rewritten", and that sentence is there (read). The work item's own
`changelog.md` says what 0.15.5's entry left out, which is the route that rule
leaves open. Neither README edition nor `docs/` states the rule (the same grep).

What the checker returns, executed in the clone at the target:

| Shape | `refused_coordinate` |
|---|---|
| `@alice#299`, `@types/node#1`, `@x#1 @abcdef12`, `docs/a.md#1장 @abcdef12` | False |
| `@alice#299@abcdef12`, `@x#1@abcdef` | True |
| `@alice#handler`, `@types/node#readme` | True |

The last row is what ⬜ 1 is about.

### ⬜ 1 — "so `@alice#299` is prose" reads as if the order alone makes it prose

The new sentence is *"An `@` before a `#` is not glued to it, so `@alice#299`
is prose"* (`evidence_check.py:1651-1653`). The 1790381328 `spec.md` copy says
the same about "silent" (`:189-190`). Both are true of `@alice#299`. But the
order is not what silences it. Once the marks are not glued, each word is
judged alone, and `#299` is then read as an issue number. An `@` before a `#`
followed by a letter is still named, because the dotless-name rule reads
`@alice` as a file name: `refused_coordinate("@alice#handler")` is True
(executed).

The next sentence of the bullet ("Where they are not glued each word is judged
alone") covers this, so the docstring is true as a whole. The changelog
fragment also says "a mention followed by an issue number", which carries the
reason. That is why this is ⬜ and not 🟡: no statement is false, and no
verdict moves. The cost is that a reader who takes "an `@` before a `#` is
prose" away from the clause can write `@alice#main` in a Code grounds cell and
meet a MALFORMED they did not expect. A rewording is in *Paste-ready fixes*.
It would drift `refused_coordinate`'s anchor again, which is a reason to take
it only with another edit to that unit.

## Every example the rules give has a case, and each one fails on its own

**#626 item 2.** `GIVEN_UP` holds 13 shapes and `TAKEN_UP` holds 8
(`tests/test_a_row_points_by_content.py:1209-1244`). These are all 21 backticked
shapes carrying `#` or `@` in the rules section of the docstring the module
loads (executed: extracted with the case's own regex from the imported
module). The claim of nine missing shapes against the dicts at `0e475b1` was
re-counted: nine, against the docstring as it stood at `0e475b1`. That list
matches the one in phase 1 (executed).

Each mutant was applied alone to `evidence_check.py`, then the whole module
was run and the bytes restored (executed):

| Mutant | Cases that failed |
|---|---|
| dotless branch takes `isalnum` | `Makefile#1x` only |
| `ISSUE_TAIL_RE` also refuses `.` | `docs/a.md#1.2` only |
| `ISSUE_TAIL_RE` also refuses `>` | `src/a.py#1>"x"` only |
| `GLUED_MARKS_RE` also matches an `@` before a `#` | `@alice#299` only |
| `PATH_HASH_RE` takes 3 hex characters | `src/a.py@abc`, and the older `jane.doe@beef` |
| `GLUED_MARKS_RE` not searched | `@alice#299@abcdef12`, and five older glued-marks cases |
| per-word path test off | `docs/a.md#²`, `docs/a.md#①`, and two older cases |
| glued search and path-hash branch both off | `docs/a.md#1장@abcdef12` joins the list |

Two named examples are named by two branches each, as the case docstring
(`:1271-1280`) and the new ledger row say. `docs/a.md#1장@abcdef12` stays
named with the glued search off, because the path-hash branch also names it.
`src/a.py#handler @abcdef12` stays named with the path test off, because the
dotless-name test takes `y#h`. Both were confirmed by the mutants above. The
statements about them are honest, so this is not a finding. It does mean rule
2's sentence "named only where its `@` is glued to its `#`" has no parameter
that fails when the glued branch alone goes.

**The completeness case** (`:1290-1308`) reads the docstring of the module
the other cases import, through `ec`, which loads
`skills/evidence-check/scripts/evidence_check.py`. That is the only copy in the
tree (executed: `find`). Adding a new example, `docs/a.md#9z`, to the rules
section turned that case alone red (executed). The ways around it are the ones
its docstring names: an example with neither mark, or one above "What #614
changed". A reworded heading raises `ValueError`, which fails the case rather
than letting an example through. A backtick span that wraps across a line
cannot match a dict entry, so it too fails the case rather than escaping. The
rules section holds 70 backticks, so the spans pair up (executed).

## Both #625 comments now say what `close` does

The two comments (`tests/test_the_fixes_close_the_record.py:710-714` and
`:2326-2333`) make four claims. I measured them with a probe that ran the
comments' own fixtures (the three words and the sibling case). It ran each
one as a draft, and once more as ready with `run_check`'s draft payload
turned off for the `close` call only (executed):

| Fixture | Draft: exit, what printed | Ready: exit, what printed |
|---|---|---|
| `fixed` | 0, the `Pass` beside `nobody` notice | 1, `Broad gate` is `not yet` and the pair |
| `answered` | 0, nothing | 1, `Broad gate` is `not yet` |
| `deferred` | 0, nothing | 1, `Broad gate` is `not yet` |
| the sibling case (`fixed`) | 0, the notice | 1, both |

That is what both comments say. *"because `gh` never says a fixture's pull
request is ready"* is true too: `pull_request_is_ready` asks `gh pr view`, and
the fixture repository has no remote (read, `round_record.py:998-1020`, with
`env_without_a_pull_request` removing `GITHUB_EVENT_PATH`).

The assertion stays `code in (0, 1)`. `plan.md:65` gives the grounds: the
draft exit is already pinned by
`test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag`, which
asserts `code == 0` (read, `:249-275`). I judged those grounds and accept
them. The 22 other `in (0, 1)` assertions have no sentence claiming exit 1
beside them, so they are outside #625's class, which is sentences.

**The class sweep.** I scanned every tracked `.py` and `.md` for windows of
seven lines holding `nobody` with `Pass`, `close` or *checked by* and an
outcome word (exit 0/1, fails, red, refuse, notice, prints). Records and
ledger files were left out, and so were windows that say *draft* or *ready*
(executed). It returned 46 lines. None of them states what `close` or the
pair does on a draft as if it were the ready outcome. Four hits were read in
context:

- the ready-judged `test_a_correction_closed_answered_lands_on_no_fixes_to_check`, whose docstring says "judged as READY";
- the two honest-mid-run cases in `tests/test_a_record_precedes_the_fixes_it_commissions.py:936-950,1066-1080`;
- the "refused both ways" docstring in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:514`;
- the seal refusal in `broad_gate.py:79`, which is `seal`'s and not `close`'s.

The rest I judged from the line alone. They are about another command, or
about `Fixes checked by` before the last record, or they are the
`tests/test_the_last_rounds_fixes_are_checked.py` hits (the grandfathered
notice, and the cutoff cases the frame lists as ready-judged). I did not
reopen that module, so for its cases the frame's reading is carried and not
re-derived.

## The re-wraps change no word, and `--help` renders the same bytes

For each re-wrap hunk the words before and after are equal once whitespace is
split and adjacent string literals are joined (executed). The hunks are
`round_record.py#landing_values`, `unverified_check.py#main`'s help, the three
test docstrings, and the capped-run docstring. Only the two #625 comment hunks
differ, and they are rewrites. `unverified_check.py --help` is byte-identical
between the base and the target at `COLUMNS=80` (1415 bytes) and at
`COLUMNS=200` (1235 bytes), both run under the same file name (executed). The
smith's figure of 1432 bytes came from another terminal width, so it is not a
contradiction.

No `.py` line this branch added is over 88 columns. The four lines over 88
that `6875d64` added no longer exist at the target (executed: diff and
`git grep`). `ruff check` and `ruff format --check` on the eight changed
Python files exit 0 (executed).

## The ledger holds, and one note miscounts

`bin/evidence-check .`, unscoped, exits 0: 2469 ok, 0 drifted, 0 broken,
0 malformed. The records arm refused nothing (executed). I checked each
`Re-read` and `Corrected` note in the 11 release files against the edit it
follows. For the `unverified_check.py#main` rows, `--help` is byte-identical,
and `test_the_baseline_help_names_both_places` passes (executed). For the
`landing_values` rows and the three test-docstring rows, the words are equal.
For the two comment rows, my probe above confirms them. For S8–S12, the
count of 21, the rename and the three mutants are confirmed above. Every
note is true except one detail.

### ⬜ 2 — the 0.11.4 note says the ragged line held three words

`seal/releases/0.11.4.md:61`'s note on
`test_a_correction_row_closes_answered_and_never_fixed` says *"a line in the
middle of its first paragraph held three words"*. At the base, that line was
`pull request — a reader` (`tests/test_the_rules_have_one_owner.py:349` at
`2037cf0`, read from the diff). That is four words. The note's claim, that the
re-wrap changed no word, holds. This is a correction to paperwork under
`seal/releases/`, so it is ⬜ and outside `Needs a fix`.

## Executed and read, kept apart

- **Executed**, in the clone at `159d5d4`:
  - `bin/test tests/test_a_row_points_by_content.py tests/test_the_fixes_close_the_record.py -q`: 277 passed, exit 0;
  - `bin/test tests/test_unverified_rows_close.py -k baseline_help`: 1 passed, exit 0;
  - `bin/evidence-check .`: exit 0, totals above;
  - nine mutants of `evidence_check.py` (the eight tabled above, and the added docstring example) and the draft/ready probe of `close`. Each ran once, the files were restored from kept bytes, and `git status` in the clone was clean afterwards;
  - the completeness count at the target and at `0e475b1`, `refused_coordinate` on the shapes above, the re-wrap word comparison, the `--help` comparison, the width scan, and the class sweeps (glued rule; the pair's outcome);
  - `uvx ruff check` and `uvx ruff format --check` on the eight changed `.py` files: exit 0 each.
- **Read**: the full branch diff of `skills/` and `tests/`, the word-level diff of all 11 `seal/releases/*.md` files, the two new ledger rows, `refused_coordinate` and the regexes above it, `malformed_rows`' docstring, `run_check` and `pull_request_is_ready`, this work item's `spec.md`, `questions.md` (the settled list), `plan.md:65`, the three phase records, the corrected 1790381328 `spec.md` hunk, `CHANGELOG.md:52-66`, and `docs/review-chain-spec.md:916-935`.
- **Unverified**: the full suite, repository-wide lint and typecheck. Answerer: the sealer, once this round's record is written.

## Regression tests to plant

None. The branch's own cases pin every sentence it changed that a check can
pin, and each was seen red above.

## Facts for the evidence ledger

None beyond the two rows the branch wrote. Both were re-derived above. If ⬜ 1
is taken, the reworded sentence re-stamps `refused_coordinate` in
`seal/releases/0.15.4.md`, `seal/releases/0.15.5.md` and this work item's
fragment.

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
| 🟢 | The ledger re-stamps hold over the whole tree | the 11 `seal/releases/*.md` files, `seal/ledger/1790550713-what-the-last-rounds-deferred.md` | confirmed | Executed: `bin/evidence-check .` exit 0, 0 drifted. Each note was read against its edit (⬜ 2 aside) |

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

## Paste-ready fixes

### ⬜ 1 (optional)

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

### ⬜ 2

```
held four words
```

(in place of `held three words` in the 0.11.4 note)

Needs a fix: no
Loses a record or crashes: no

## Proof block

Opened this round, in the clone at `159d5d4` unless noted:

- `skills/evidence-check/scripts/evidence_check.py` (lines 1560-1790)
- `skills/code-review/scripts/round_record.py` (`run_check`, `pull_request_is_ready`, the `landing_values` hunk)
- `skills/verify/scripts/unverified_check.py` (the `--baseline` hunk, and run with `--help`)
- `tests/test_a_row_points_by_content.py` (lines 1048-1060, 1100-1308)
- `tests/test_the_fixes_close_the_record.py` (lines 25-145, 249-275, 680-725, 922-960, 2270-2350)
- `tests/test_the_record_is_generated.py` (`env_without_a_pull_request`)
- `tests/test_a_record_precedes_the_fixes_it_commissions.py` (lines 936-950, 1066-1080), `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` (lines 505-525), `skills/code-review/scripts/chain_check.py` (lines 2166-2215), `skills/verify/scripts/broad_gate.py` (lines 74-86)
- the branch diff of `tests/test_a_script_copied_alone_exits_2.py`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_rules_have_one_owner.py`
- `seal/releases/*.md` (word diff of all 11), `seal/ledger/1790550713-what-the-last-rounds-deferred.md`
- this work item's `spec.md`, `changelog.md`, `questions.md` (lines 20-35), `plan.md:65`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`
- `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` (the corrected hunk)
- `CHANGELOG.md` (lines 52-66), `docs/review-chain-spec.md` (lines 916-935)
- `bin/test` (header)
