# 1790683267-a-rider-read-ends-where-the-hasher-cuts — round 2 report

| Field | Value |
|---|---|
| Round | 2, a verifying round |
| Target | round 1's fix range `91f0c949..c6ac02b3` (5 commits), read at branch HEAD `b87eb589`, which adds only round 1's closed record |
| Base | `91f0c949`, the reader round 1 reviewed, loaded beside HEAD; `origin/release/v0.16.0` is `346b4af7` for the range checks |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` at `b87eb589`, with a second clone at `91f0c949` |
| Earlier rounds | `rounds/round-1.md` and `rounds/round-1-report.md`, read for coordinates; every verdict below was re-derived |

## What this round found, in the order one causes the next

1. All five of round 1's verdicts are closed (executed and read). The three
   answered ones say what the code does. The two fixed ones do what their
   grounds claim, and each was seen red again this round.
2. Finding 5 changed shipped behaviour, so this round pushed on it hardest.
   Every location `rider_check.py` prints now names the GFM line: the check's
   DRIFTED and BROKEN, `--migrate`'s REFUSED and `migrated`, `--reverify`'s
   `restamped` and REFUSED, and the length error in `write_block`. This held
   with CRLF, lone CR, the eight characters, and none of them, against a
   line count this round wrote itself (executed).
3. Nothing reads a printed location back as a piece index, and the new field
   changes no consumer of a rider (read, and executed for `inferred_anchor`
   and the writes).
4. K1 still holds at HEAD (executed). K2's correction and the new K3 row are
   true, and the three ledger checks agree (executed).
5. One stale row is left in the paperwork. `round-1.md`'s Deferred table
   still offers finding 5 as "a candidate for its own issue", but the fix
   pass fixed it (⬜ 1). That is a correction to a record, outside
   `Needs a fix`.

Nothing here needs a fix. The broad gate, the sealer's run, comes due now.

## Round 1's five verdicts

### Finding 1 — `comment_blocks`' docstring (answered at `89a8419f`)

`.github/scripts/rider_check.py:302-311` now says a mid-line marker piece is a
rider where "its GFM line lies inside a block this returns -- a comment it
opens, or an HTML comment an earlier block left open". That is the report's
paste-ready paragraph word for word, and the rule K1 states. The diff over
the range touches only the docstring in this unit, and no code (read).

### Finding 2 — G13 and P5-1 (answered at `d0f0103f`)

Each row now carries one `Corrected 2026-09-29 in round 1 of work item
1790683267` note, and each note sits after this item's own correction. G13 is
in `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md`, and
P5-1 in `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md`.
Both rows moved their `comment_blocks` anchor to `@bc2c1144` with a `Re-read`
note, and `evidence-check --strict` reads them ok (executed).

### Finding 3 — `region_lines`' comment (answered at `89a8419f`)

`.github/scripts/rider_check.py:490-492` now says the blocks are cut from the
same GFM lines `riders_in` hands `comment_blocks`. The `overview.md` sentence
that kept the old comment is rewritten, and S2 took a re-stamp with a dated
note (read).

### Finding 4 — the oracle case's reader half (fixed at `e1177056`)

`test_the_rider_check_never_leaves_both_readings` now runs `quoted_lines`
over GFM lines too, and maps each piece to its GFM line through `gfm_places`.
The fix pass claimed that half turns red on 273 documents when `gfm_places`
numbers pieces. **This round planted that mutant** (an early `return` of piece
numbers in `gfm_places`) and ran the case. It failed with "273 documents".
With the file restored it passed (executed).

### Finding 5 — the printed location (fixed at `bda0e0ba`)

**The fix pass claimed** that a `Rider` now carries the GFM line of its first
piece, that `where` prints it, and that `start` and `end` stay piece numbers.
The code matches. `riders_in` computes `places = gfm_places(...)` once. It
groups pieces by it, as before, and passes `places[starts[i]]` as LINE.
`write_block`'s length error now prints `rider.where()`.

**Every print, enumerated by construction.** `where()` has twelve callers in
`rider_check.py`: lines 524, 538, 550 and 555 in `check`; 634 in
`write_block`; 681, 688 and 695 in `reverify`; 776, 785, 791, 801 and 811 in
`migrate`. `main` prints nothing else about a rider. The one other print is
`reverify`'s refusal of an `--only` no rider carries, and it prints the path
alone. No print in the script reads `rider.start` any more.

**The differential** (executed). A probe built its own editor line for each
rider. It counts `\r\n`, `\r` and `\n` in the text before the offset of the
rider's first piece, and it takes that offset from
`str.splitlines(keepends=True)`, not from `gfm_places`. The texts have one to
nine lines, ended by LF, CRLF or lone CR at random. The lines are built from
both comment kinds, stamps, `-->`, `# note`, code, fences and prose, joined
by nothing, a space or one of the eight, and sometimes led by one of the
eight. 30% of texts use no eight at all. Each text is read as `.py`, `.md`
and `.yml`.

- **Reader level.** 60,000 texts, 39,798 of them with one of the eight, and
  299,363 riders. For every rider, `line` equals the probe's editor line,
  `where()` prints it, and that GFM line holds the marker. On texts without
  the eight, `line == start`. 186,056 riders have `line != start`, so the
  probe exercised the difference. 0 failures. The riders' `(start, end,
  body)` match `91f0c949`'s on every text.
- **End to end.** 60 trees, 2,102 marker-carrying files under `hooks/`,
  `templates/` and `.github/`, one tree per version. Each tree ran `main()`
  as check, then `--migrate`, then `--reverify`, then check again. That gave
  12,438 printed location lines. For each one, HEAD's number equals the
  probe's editor line for the piece `91f0c949` printed. The rest of the line
  is identical at both versions, and the GFM line named holds the marker.
  7,484 lines print a different number at the two versions. 0 failures and 0
  exceptions. The files are byte-identical between versions after every
  write.
- **The probe can fail.** With `where` put back to `rel:start`, the reader
  level failed 936 of 1,575 riders, and end to end failed 248 of 373 lines.
- **The two prints the generator cannot reach.** `migrated` needs a commit
  that resolves. A probe driving git from Python made one, with a rider at
  piece 5 behind a form feed and a U+2028. It printed `migrated
  hooks/m.py:3`, and GFM line 3 is where the rider sits. `write_block`'s
  length error was forced with a body one piece too long. It printed
  `hooks/w.py:2: …` for a rider at piece 3 on GFM line 2. Through `restamp`
  that error is unreachable, since a stamp writes no line break, so it is
  checked here and pinned nowhere. That is not a finding.
- **The tree.** Its 18 riders have `line == start`, and `rider_check.py
  --root .` prints identical output at both versions: `18 ok · 0 drifted · 0
  broken`, exit 0.

**Seen red (§15), re-run.** With `91f0c949`'s `rider_check.py` in the clone,
`test_a_rider_is_printed_at_the_line_an_editor_shows` failed for all eight
characters. `test_a_break_inside_a_cut_line_changes_no_verdict` failed for
all 16 on the location, for example `templates/doc.md:5` against `:4`. That
is 24 failures, the fix pass's 8 and 16 (executed).

## The asks, answered

**Does anything read a printed location back as a piece index?** No (read).
The DRIFTED sentence hands the reader `--only <path>`, and `--only` compares
the path alone. No workflow parses `rider_check.py`'s output, and
`.github/workflows/` does not name it.
`tests/test_a_rider_reaches_its_file.py:205` prints `where()` into an
assertion message and reads nothing back. `rider_stamps` at line 191 returns
`(r.rel, r.start)` under a docstring that says "(file, line)", so the value
is a piece number under the name of a line. Its one caller, at line 220,
discards the value (`_line`). It is older than #664, outside the fix range,
and changes nothing anybody sees, so it is noted here and not raised.

**Does anything compare `start` with a GFM line number?** No. There are two
places that could, and both first map `start` through `gfm_places`:
`inferred_anchor` at `rider_check.py:729`, and the class case at
`tests/test_every_reader_ends_a_line_where_gfm_does.py:909`. `write_block`
cuts the file by `start` and `end` as pieces, which is what they still are.

**Does the new field change equality, sorting or a consumer?** No. `Rider`
defines no equality, ordering or hash method, so it compares and hashes by
identity, before and after. Only `riders_in` builds a `Rider`. The
`Contract changes` row's other two sites are prose in 1790655302's
`round-3.md` and `round-3-report.md`. Every test that reads a rider reads
`start`, `end`, `body`, `new`, `old`, `rel` or `where()`, and the four
modules pass. `inferred_anchor` reads `start` and `end` only. It named the
same unit at both versions for every Python rider the K1 probe drew; that
was 23 named, 0 differing. The riders it gets are identical at both
versions (above).

**The new unit.** `test_a_rider_is_printed_at_the_line_an_editor_shows` is
the one unit the fix range created. Judged as code, it is correct. Each file
puts exactly one of the eight above the rider, so a piece number and a GFM
line differ by one. It builds the marker from parts, so the case file
plants no rider, and the tree check still reads 18. It pins seven of the
eight print sites. It does not pin `migrated`, which needs a commit, or the
length error, which is unreachable. The probe above executed both.

## K1, K2, K3 and the checks

**K1** (executed). The probe compared the reader against the hasher at
HEAD. It drew 30,000 texts, read each as three file types, and got 150,354
riders. The hasher's blocks are `comment_blocks` over the checker's
`gfm_lines`, as `region_lines` cuts them. For every rider:

- every piece lies on a GFM line inside one of those blocks;
- no piece after the first carries the marker;
- the riders' starts are exactly the marker pieces inside a block.

0 failures. With `gfm_places` mutated to number pieces, 3,883 of 9,000 reads
failed.

**K2's correction** is true. The verdict case now compares `sorted(problems)`
whole, the location included, and it passes at HEAD and fails 16 of 16
against `91f0c949`. The claim's own words still name only "the counts and
the severity and sentence". That is narrower than the case now checks, and
still true.

**K3** is true on every clause this round could execute. The claim lists
`#migrate`'s REFUSED and leaves out `#migrate`'s `migrated`, which prints the
same `where()`. That is a claim narrower than the code, not a false one. The
row's "18 riders print the same number as before" was re-run above.

**The checks**, run in the clone against `origin/release/v0.16.0` at
`346b4af7`:

- `evidence-check --strict .` reads `total: 3084 ok · 0 drifted · 0 broken`
  and exits 0.
- `correction-check --range origin/release/v0.16.0...HEAD` examined 1 merge,
  found no dropped marker, and exits 0.
- `survivor_check.py --range origin/release/v0.16.0...HEAD`, with every
  `seal/specs/*/survivors.md` passed through `--exempt` the way
  `.github/workflows/hygiene.yml` loops them, exits 0 with 1 place exempt.
  Without the exemptions it exits 1 on that same place, at
  `tests/test_every_reader_ends_a_line_where_gfm_does.py:743`. The fix pass's
  new K2 row in `survivors.md` is not reported over this range, because the
  K2 phrase was added inside the range too. The row is harmless.

## The interpreter floor

`rider_check.py` carries no `zip(`, no `pairwise` and no `.UTC`, comments
included. The only `zip` is the words "a strict zip" in `write_block`'s
comment. `ABOVE_THE_FLOOR` (`zip\(.*strict=`) does not match it. The new
code adds a positional parameter, a list index and an f-string with no nested
quotes. The floor case passed in the narrow run. `ruff check` and `ruff
format --check` are clean on the three changed Python files (executed).

## ⬜ 1 — round 1's Deferred table still offers finding 5 as an issue to file

`seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/rounds/round-1.md`,
under `## Deferred`, still has the row "⬜ 5 — a rider's printed location is a
`str.splitlines` number … not placed: a candidate for its own issue | the
orchestrator, who files it or answers that it stays as is". The verdict row
above it now reads `**fixed** bda0e0ba`, so the record says two things about
one finding. The `Who answers it` column is what sends a leftover to a new
issue. Read as written, the row asks the orchestrator to file an issue for a
defect this branch already fixed. It is paperwork under `seal/specs/`, so it
is a correction and not a fix to commission. Two answers work:

- mark the row in `round-1.md` as fixed in this run (the fenced row below);
- or leave the row and answer here that no issue is filed.

This report's own Deferred table carries only the `-->` message row forward.

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

Every probe was one `test_tmp_*` file in this round's scratch directory,
outside the tree. It, its temporary trees and repository, and both clones
were deleted after the run.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the `-->` shape's sentence "no verification stamp" when a stamp sits outside the comment | not placed: a message improvement, outside this item's class; already deferred in round 1 | the orchestrator, if the owner wants the message to name the case |

## Paste-ready fixes

### ⬜ 1

The row in `round-1.md`'s `## Deferred`, if the record is annotated rather
than answered here:

```markdown
| ⬜ 5 — a rider's printed location is a `str.splitlines` number, older than #664 | fixed in this run at `bda0e0ba`; confirmed by round 2 — no issue | nobody: closed |
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened at `b87eb589` in the clone:
- `.github/scripts/rider_check.py` (lines 100–869, and the diff over `91f0c949..b87eb589`)
- `tests/test_every_reader_ends_a_line_where_gfm_does.py` (lines 51–62, 600–660, 725–740, and the diff)
- `tests/test_the_hooks_hide_what_a_renderer_hides.py` (the diff)
- `tests/test_a_rider_reaches_its_file.py` (lines 180–240)
- `tests/test_a_script_says_which_interpreter_it_needs.py` (lines 467–520)
- `hooks/blocks.py` (lines 115–121, 372–400)
- `.github/workflows/hygiene.yml` (lines 227–300)
- `.github/scripts/run_tests.py` (the venv lines), `bin/test`
- `skills/code-review/scripts/round_record.py` (lines 40–75), `skills/code-review/scripts/chain_check.py` (lines 1–40), `docs/round-record-spec.md` (lines 399–420)
- this item's `rounds/round-1.md`, `rounds/round-1-report.md`, `survivors.md`, `changelog.md`, `overview.md` (line 32)
- `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md` K1, K2, K3; the diff over the range for G13, P5-1 and the re-stamped rows
