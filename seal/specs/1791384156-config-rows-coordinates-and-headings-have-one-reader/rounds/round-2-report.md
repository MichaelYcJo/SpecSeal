# Round 2 report — #867, draft PR #882

Target SHA `bb48b1b5acaf3e3c38d1fe7a1215cf0ab82b8038`. This round verifies
round 1's fixes, so the target is the fix range `9f186d2a..105d96ea` (eight
commits) plus the table and close commits. Reviewed in a `--no-local` clone
at the target SHA, under the session scratchpad.

Carried from round 1, not re-established: the coordinates of each finding,
and the reading of the 33 survivor places (round 1's paste-ready table).
Re-derived here: every verdict.

## How the findings relate

```
round 1's eleven findings ................. each closed as recorded (rows below)
the two questions the prompt asked ........ both hold: the oracle hides no live
                                            survivor; the lenient read widens nothing CI did not
round 1's new units ....................... sound, with two small gaps in one of them
  config_at_head under --worktree ......... names a disk path; a directory goes unseen  ⬜ 1, ⬜ 2
the fix pass's own paperwork .............. survivors.md misattributes two of 29        ⬜ 3
```

Nothing here needs a fix before the pull request. The three findings are
wording or edge cases that move no exit status.

## The two questions the prompt asked

### The frozen oracle silences 29 survivors, and none of them is a live reader

Executed. With `SETTLE_COPY_AT_0_20_0` replaced by an empty pattern in a
probe commit, `survivor-check --range d712a632...HEAD` names 33 places
again. These are the same 33 round 1 read. With the oracle in place it names
four, and `survivors.md` excuses all four (exit 0).

The 29 split by the removed sentence they matched:

- 27 matched `settle.py`'s removed coordinate pattern. The oracle is that
  text verbatim, so the sweep reads it as a move (`paired_across_paths`)
  and not as a removal.
- 2 matched `.github/scripts/rider_check.py`'s removed stamp pattern
  (`NEW_STAMP`, NAME NOT IN TREE). The oracle is not a copy of that one.
  These two vanish because the oracle's `@[0-9a-f]{6,12}` is wording the
  range wrote, and its n-grams are subtracted. The two places are the
  checker's own `ANCHOR_HASH` line and `pact_check.py`'s `CHANGE_RE`, a
  record id that K14 already exempts.

None of the 29 reads a ledger coordinate except the checker's grammar
itself, as round 1 found. A live third copy would still be caught by K14's
case, `test_no_shipped_script_spells_the_coordinate_grammar_again`, which
reads every shipped script whatever the sweep says. The oracle lives under
`tests/`, which that case does not read, and that is right for an oracle.
So the silencing is legitimate. One sentence in `survivors.md` describes it
inaccurately (⬜ 3).

### `errors="replace"` in `read_record` lets nothing through that CI did not already let through

Read. At HEAD, which is the mode CI runs, `read_record` goes through
`git()`, and that helper has always decoded with `errors="replace"`
(`skills/code-review/scripts/chain_check.py:878`). So `--worktree` now reads
a file the way CI reads it. That is the direction `read_record`'s own
docstring asks for: the local run must not be the more permissive one.

Before the fix, an undecodable record under `--worktree` raised. That was a
crash and not a refusal. `round_record.py`'s `run_check` calls the check
after the record is written, so the traceback stopped nothing.

What remains predates the branch and is the same in both modes. A byte that
breaks the 🔴 glyph inside a row would hide that row from `open_blocking`,
which selects on the glyph. It needs a record that is not UTF-8, and nothing
in the plugin writes one. `seal/config.md` is the file whose loss matters,
and it no longer goes through this read: `config_at_head` reads it strictly.

## Round 1's findings

- **Round 1's two blocking findings are closed.** The Windows assertion now
  reads `out.stderr.replace(os.sep, "/")` (read). The release job passes at
  bb48b1b5 (read from `gh pr checks 882`), and the survivor sweep exits 0
  with `survivors.md` exempting in the clone (executed). The Windows pytest
  shards were still pending when this round read them, so the first
  finding's CI evidence is a question below.
- **Yellow 3 is answered.** The fragment carries one `Corrected · C1` row in
  place of the two re-reads, and its clause on an unreadable config states
  the exit-2 refusal. `bin/evidence-check --strict .` exits 0 (executed).
- **Yellow 4 is closed.** S7 now compares `coordinate_paths` with the
  frozen 0.20.0 pattern over `released_by_0_20_0`. Executed in the clone:
  red with `ANCHOR_QUOTED` narrowed, and red with `settle` stripping a
  leading dot from each path. Dropping the dot from `ANCHOR_NAME` stays
  green. That mutant is equivalent on this corpus, because no released
  ledger cites a dotted name (counted: 0).
- **Yellow 5 is closed.** The new case is red with `config_at_head`
  bypassed (both parameters) and red with `read_record` strict (the
  `--worktree` parameter). Executed.
- **Yellow 6 is closed.** `_LooseHeading.match` asks `heading_level`, and
  its case is red with the old `#{2,3}\s` pattern put back (executed). The
  other spellings a grep finds in shipped code (`ATX_HEADING`,
  `GITHUB_HEADING_RE`, the paragraph-end patterns, the comment tests) are
  each in `HEADING_EXEMPT` with a reason. The two `lstrip("#")` calls are
  `heading_level` and its twin.
- **White 7, 10 and 11 are closed.** The docstrings read as recorded. The
  memo returns a fresh list per call, and every caller of `markdown_lines`
  (`resolve_unit`, `heading_path` in `pact_check.py`, line 1008, a test)
  only reads it.
- **White 8 stays deferred to #872.** `overview.md` §*Not done* now states
  the limit of the spec's sentence.
- **White 9 is answered on grounds I accept.** `spec.md` §*Data &
  interfaces* ordered the generic sentence.

### The `run` in round 1's `Contract changes` row

The `run` that changed is `tests/test_a_signers_ci_prints_its_pact.py#run`,
which gained `*extra`. Every caller in that module passes one positional
argument or `*extra` (read: lines 147–294), and nothing imports the module.
Every caller holds. The rest of the long list is callers of other functions
also named `run` across the tree. The record generator matched the bare
name, so the list says nothing about this change.

## Round 1's new units

`_shown_lines`, `_LooseHeading`, `SETTLE_COPY_AT_0_20_0`,
`released_by_0_20_0` and the two new cases read correct, and the cases were
each seen red above. `config_at_head` is correct at HEAD. It has two gaps
under `--worktree`, both executed with a probe that calls `pact_notices`
directly.

### ⬜ 1 — under `--worktree` the notice names the absolute disk path

`skills/code-review/scripts/chain_check.py:1103`. Under `--worktree`,
`config_at_head` hands the disk directory to `config_text`, and that
refusal names the path it opened. At HEAD the same notice reads
`seal/config.md at HEAD`. So one state gives two notices depending on the
mode, and the local one carries a machine path.

The new case asserts that the first space-delimited word after
`was not read: ` contains `config.md`. On a checkout whose path holds a
space, that word is a fragment of the directory and the case fails. CI's
temporary paths hold no space, so this is not red today.

### ⬜ 2 — under `--worktree` a directory at `seal/config.md` prints nothing

`skills/code-review/scripts/chain_check.py:4360`. The comment the fix added
says `read_record` answers "whether there is anything at the path". Under
`--worktree`, a directory at that path makes `open` fail and `read_record`
return None. With no `seal/pact.md` and no declared work item,
`pact_notices` then returns before `config_at_head` is called. Executed: at
HEAD the same tree prints the notice, and under `--worktree` it prints
nothing.

The ledger's K26 row says "a tree at that path, is one notice naming it, at
HEAD and under `--worktree` alike". That holds only when something else is
present. No exit status moves either way.

## The fix pass's paperwork

### ⬜ 3 — `survivors.md` gives all 29 to `settle.py`'s copy

`seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md:10`.
The file says the 29 shared "only character classes with `settle.py`'s
removed copy", and that freezing that copy is why the sweep stopped naming
them. Two of the 29 matched `rider_check.py`'s removed pattern instead, and
one of those two is the checker's own grammar rather than "a pattern of its
own". This is a correction to a record and is not counted in `Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Under `--worktree`, `config_at_head`'s notice names the absolute disk path where HEAD names `seal/config.md at HEAD`, and the new case's first-word assertion fails on a path holding a space | `skills/code-review/scripts/chain_check.py:1103` | open | executed: probe calling `pact_notices` in both modes over an undecodable config; read: the case's assertion |
| ⬜ 2 | Under `--worktree`, a directory at `seal/config.md` gives no notice when there is no `seal/pact.md` and no declaration, because `pact_notices` returns before `config_at_head`; K26 says HEAD and `--worktree` alike | `skills/code-review/scripts/chain_check.py:4360` | open | executed: the same tree prints the notice at HEAD and nothing under `--worktree` |
| ⬜ 3 | `survivors.md` attributes all 29 silenced places to `settle.py`'s copy; two matched `rider_check.py`'s removed pattern, one of them the checker's own grammar | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md:10` | open | executed: the sweep with the oracle removed names 33, 27 from `settle.py:196` and 2 from `rider_check.py:158`; a correction to a record, outside Needs a fix |
| 🟢 | round 1's blocking finding 1 is closed — the doubled freeze row's case reads the path with `os.sep` as `/` | `tests/test_a_released_row_is_read_again_in_a_fragment.py:861` | confirmed | read at c6e32946; the case passes on macOS (executed); the Windows shards were pending at bb48b1b5, see the question row |
| 🟢 | round 1's blocking finding 2 is closed — the survivor sweep names four places and `survivors.md` excuses each | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/survivors.md` | confirmed | executed: exit 1 with four places, exit 0 with the file exempting; read: the release job passes at bb48b1b5 |
| 🟢 | round 1's yellow 3 is answered — one `Corrected · C1` row replaces the two re-reads and states the exit-2 refusal | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` | confirmed | read; `bin/evidence-check --strict .` exit 0 and `bin/correction-check` exit 0, executed |
| 🟢 | round 1's yellow 4 is closed — S7 compares `coordinate_paths` with the frozen 0.20.0 pattern | `tests/test_settle_reads_before_it_removes.py:1873` | confirmed | executed: red with `ANCHOR_QUOTED` narrowed and with `settle` altering a path; the `ANCHOR_NAME` mutant is equivalent here, since no released ledger cites a dotted name |
| 🟢 | round 1's yellow 5 is closed — the pact notices read the config through `config_at_head`, and `read_record` no longer raises | `skills/code-review/scripts/chain_check.py:1093` | confirmed | executed: the new case red with `config_at_head` bypassed (2 failed) and with `read_record` strict (1 failed) |
| 🟢 | round 1's yellow 6 is closed — `LOOSE_HEADING` asks `heading_level`, and the grep reads any counted `#` run | `skills/verify/scripts/unverified_check.py:155` | confirmed | executed: the case red with the old pattern put back; read: every other spelling a grep finds is in `HEADING_EXEMPT` or is the rule itself |
| 🟢 | round 1's white 7, 10 and 11 are closed — the twin's docstring, the garbled clause and the memo | `skills/evidence-check/scripts/evidence_check.py:579` | confirmed | read; every caller of `markdown_lines` only reads the list it gets |
| 🟢 | round 1's white 9 is answered — the generic doubled-row sentence is what the spec ordered | `hooks/config.py:977` | confirmed | read against `spec.md` §*Data & interfaces* |
| carried | round 1's white 8, which lines a reader hides before it asks the heading rule | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md:200` | deferred #872 | already deferred in round 1; `overview.md` §*Not done* now states the sentence's limit (read) |
| 🟢 | The frozen oracle silences only the 29 places round 1 read, and none reads a coordinate | `tests/test_settle_reads_before_it_removes.py:1850` | confirmed | executed: oracle removed, 33 places, the same 33; K14's case still reads every shipped script |
| 🟢 | `errors="replace"` in `read_record` makes `--worktree` read as HEAD already reads, and widens nothing | `skills/code-review/scripts/chain_check.py:1056` | confirmed | read: `git()` decodes with `errors="replace"`; the old raise came after `round_record.py` wrote the record, a crash and not a refusal |
| 🟢 | The `run` in round 1's Contract changes row is the test helper, which gained `*extra`; every caller holds | `tests/test_a_signers_ci_prints_its_pact.py:120` | confirmed | read: every call passes one argument or `*extra`, and no module imports it; the long list is other functions named `run` |
| ❓ | The pytest shards at bb48b1b5, among them the Windows shard round 1's first finding failed on | `tests/test_a_released_row_is_read_again_in_a_fragment.py:861` | ❓ out of verified scope | pending when read; the orchestrator answers it from the CI run at bb48b1b5 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named | exit 0, 436 passed |
| `bin/test` over `test_a_signers_ci_prints_its_pact.py`, `test_unverified_rows_close.py`, `test_a_format_has_one_reader.py`, the S7 case and the doubled freeze row's case | exit 0, 218 passed |
| `survivor-check --range d712a632...HEAD`, without and with `survivors.md` exempting | exit 1 with 4 places; exit 0, 4 excused |
| the same sweep after a probe commit that empties `SETTLE_COPY_AT_0_20_0` | exit 1, 33 places: 27 against `settle.py:196`, 2 against `rider_check.py:158`, 4 others |
| S7 with `ANCHOR_QUOTED` narrowed; with `settle` stripping a leading dot; with the dot dropped from `ANCHOR_NAME`; with `/` dropped from `ANCHOR_PATH`'s middle class | red; red; green (no dotted name in the corpus, 0 counted); green (the class after it still takes `/`) |
| the new notice case with `config_at_head` bypassed; with `read_record` strict | 2 failed; 1 failed, 1 passed |
| the `LOOSE_HEADING` case with `^#{2,3}\s` put back | 1 failed, 7 passed |
| probe: `pact_notices` at HEAD and under `--worktree`, over a directory at `seal/config.md` and over an undecodable one, nothing else present | directory: a notice at HEAD, none under `--worktree`; undecodable: a notice in both, the `--worktree` one naming the disk path |
| `bin/evidence-check --strict .` | exit 0 |
| `bin/correction-check --range d712a632...HEAD` | exit 0, no merge commit, no released ledger file changed |
| read, not executed by me: `gh pr checks 882` at bb48b1b5 | release, ledger, lint and both arm-check jobs pass; every pytest shard pending |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Round 1's white 8: which lines a reader hides before it asks the heading rule | #872, already deferred in round 1 | the repository owner, who triages #872 |

This round opens nothing that needs a fix. Once the pytest shards at
bb48b1b5 report green, the broad gate comes due, and with it the sealer's
spawn.

Needs a fix: no

Loses a record or crashes: no

## Proof

Opened: `rounds/round-1.md`, `rounds/round-1-fixes.md`,
`rounds/round-1-report.md`, `survivors.md`, and the diffs of `overview.md`,
`changelog.md` and the ledger fragment over `9f186d2a..105d96ea`; the code
diff of that range in full; in the clone,
`skills/code-review/scripts/chain_check.py` (870–905, 1040–1125, 1751–1787,
4333–4440), `hooks/config.py` (480–570),
`skills/verify/scripts/unverified_check.py` (520–560, 860–915, 1425–1440),
`skills/code-review/scripts/survivor_check.py` (1–80, 1301–1420),
`skills/code-review/scripts/round_record.py` (2660–2695),
`skills/settle/scripts/settle.py` (195–211),
`tests/test_a_format_has_one_reader.py` (72–170),
`tests/test_settle_reads_before_it_removes.py` (1836–1890), and
`tests/test_a_signers_ci_prints_its_pact.py` (117–225, the `run` callers).
The clone, its probe commits and the probe scripts were removed before
handover.
