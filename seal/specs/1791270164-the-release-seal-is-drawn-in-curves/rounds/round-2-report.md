# Round 2 report — 1791270164-the-release-seal-is-drawn-in-curves

| Field | Value |
|---|---|
| Target SHA | bf1a944776e4de1ecf2ab238e4e4b04d9d7baaa4 |
| Round kind | verifying round over round 1's fix range `99bcad40..092004bb`, which holds the merge `f6d39425` of `release/v0.20.0` at `559977a3` |
| Pull request | #859 (draft) into `release/v0.20.0`, its first CI |
| Ran by | specseal:warden on claude-opus-5-5 |

HEAD did not move during the review: `bf1a9447` at spawn and at hand-over,
and the same SHA on the remote branch. Every probe ran in a
`git clone --no-local` at the target under the session's scratchpad, and
nothing was written to the worktree but this file.

## Summary

Round 1's fixes hold. Each case the fix pass planted goes red with its fix
reverted and green at the target, and the merge kept every row the release
branch changed. One fix does not do what it says, and the pull request's
first CI found a defect that was in the branch before round 1:

```
the branch's build (phase 8)            round 1's fix pass
        |                                       |
  release SVG carries the SVG          apt-get update;  under bash -e
  namespace host                               |
        |                              still stops the step  ->  🟡 2
  test_only_neutral_domains red  ->  🔴 1
  on ubuntu, macOS and Windows group 2

the work item's paperwork
  spec.md's foot  ->  release job red  ->  ⬜ 3
  round-1.md counts the merge's units as the fixes'  ->  ⬜ 4
```

1. **Three pytest legs are red on a domain the release SVG must carry**
   (🔴 1). This is not a fix of a fix. Phase 8 wrote the SVG, round 1 could
   not see it because no CI ran, and the merge is what let CI run.
2. **`apt-get update;` still stops the install step** (🟡 2). The step runs
   under `bash -e`, so a failed refresh ends the step before the install,
   exactly as `&&` did. Round 1's ⬜ 8 is not closed, and four places now
   say it is.
3. **The `release` job is red on `spec.md`'s last line** (⬜ 3). The rule
   behind it shipped in 0.19.0 and was already in the branch's base.
4. **Round 1's record lists 111 new units, and 109 of them came in through
   the merge** (⬜ 4).

## Round 1's verdicts, one by one

### 🔴 1, the merge: closed

The pull request is `MERGEABLE`, and every workflow ran on this push. A
probe compared every table row of the two foreign fragments at four points:
the merge base `6de64c19`, round 1's target, the release branch at
`559977a3`, and the merge.

- **Rows the release branch changed or removed.** Each is the release
  branch's row in the merge. That covers every such row of the 1791270161
  fragment and the two rows the release branch removed from the 1791270165
  fragment.
- **Rows both sides changed.** There are six, all in 1791270161: `D2`,
  `C4` (§*What the count does not say*), `N3` (the shipped verify skill),
  `P11`, `R9` and `W8`.
  Each equals the release branch's row except for one anchor: the
  `skills/verify/SKILL.md` §*The broad gate* section, which auto-merged
  into text neither side had, re-stamped to `5c121a55`.
- **Rows only this branch changed.** These keep this branch's re-stamp.

`correction-check` exits 0 over the merge-base range and over the fix
range. `evidence-check --strict .` reports 6,835 ok, 0 drifted, 0 broken.

### 🟡 2, the tick after the disc: closed, and the class with it

`colour_row` writes no foreground part for a green cell
(`skills/verify/scripts/seal_stamp.py:492`). With that guard reverted, the
new case fails on its `✓` parameter, the line carrying `32;39`. The `·`
parameter passes either way, which is right: dim was never broken.

The class is every styled cell beside the disc, not the tick alone.
Reading: of `STYLE_CODES`, only `32` sets a foreground, and the title's
bold carries `TITLE_RED` as its own foreground. Execution: a probe drew
246 row sets, each at 0.90 and with no disc. The sets mixed titles, dim
labels, `""` continuation rows, a leading `✓` and `·`, a mid-value `✓`
and a half-block in a value. Every non-blank text cell showed what
`compose` drew, more than a thousand cells per scale.

### 🟡 3, the pair case: closed under any chart `read_chart` accepts

`test_several_files_come_out_one_stop_each_oldest_first` grows its panel
until the pair does not fit, and asserts that the grown stamp still fits
with its disc. It passed under seven charts: the S, the archived key, and
five extremes `read_chart` accepts (an empty field, a full field, a
checkerboard, row stripes and column stripes). The checkerboard is about
the worst a chart can do to the stamp's size, because every cell changes
colour. Its small stamp is 7,728 units, still under the 9,000 budget, so
the case's second premise holds there too. The archived § is refused by
`read_chart` before the case can draw, as designed.

### 🟡 4, the one-file budget case: closed

With `RESET` padded by 300 spaces, the case now fails on its new
assertion: *a real run's stamp no longer fits the budget with its disc*.
It is green at the target and under all seven charts. Under the
checkerboard a real run's stamp is 8,320 units, close to the budget but
under it.

### 🟡 5, a half-block in a value: closed

`letter_row` takes a half-block as the disc's only when its foreground is
a `KEY` colour (`skills/verify/scripts/seal_stamp.py:514`). With that
reverted, all three parameters of the new case fail. `TITLE_RED` is not a
`KEY` colour, so no text cell can take a letter. The twin's ASCII is still
pinned at `tests/test_the_seal_is_taken_once_by_the_sealer.py:822`.

### ⬜ 6 and ⬜ 7: closed

The hook says "never smaller" (`hooks/sealer-stamp.py:41`). *The sheet*
remains in the hook's cases only where they say it was retired (lines 844,
944 and 975).

`read_chart` reads `utf-8-sig`. The BOM copy in
`test_the_disc_mark_is_one_chart_file_read_as_data` fails with the reader
reverted. The encoding and line-reader hygiene modules pass over the new
call, 305 cases.

## Findings

### 🔴 1 — Three pytest legs are red, because the release SVG carries a domain the hygiene check refuses

`test_only_neutral_domains` fails on the ubuntu leg (1 failed, 12,738
passed), the macOS leg (1 failed, 12,730 passed) and Windows group 2
(1 failed, 6,706 passed). No other case fails on any leg. It names two
lines:

- `.github/scripts/release-seal.svg:1`, the SVG's `xmlns` attribute;
- `tests/test_the_release_seal_is_drawn.py:38`, the case's `NS` constant.

Both hold the W3C's SVG namespace URI. A renderer reads a file as SVG only
through that namespace, so it cannot be dropped or replaced with
`example.com`. The check's own message offers the other way: *consciously
extend `ALLOWED_DOMAINS`*.

Why it matters: the pull request cannot merge on red legs, and every later
push meets the same failure. Phase 8 introduced both lines at `09417ab5`.
This is not a fix of a fix.

The fix extends the allowlist with the namespace's registrable domain.
The fence below splits that literal into two strings, so that this report,
which the same check scans once it is committed, does not trip it. Join
the two strings when pasting; the check does not scan its own file. With
the entry added, the module passes, 5 cases. Without it, the module fails
in the clone exactly as on the runners.

### 🟡 2 — `apt-get update;` still stops the install step

Round 1's ⬜ 8 said `&&` skips the install when the refresh fails. The fix
replaced `&&` with `;` (`.github/workflows/publish-release.yml:114`). But
the step names no `shell:`, so it runs under GitHub's default, `bash -e`
(read from GitHub's documentation, and not opened this round). The pull
request's own `release` job logs its shell as
`/usr/bin/bash --noprofile --norc -e -o pipefail`. Under `-e`, a failed
`apt-get update` ends the step before the install runs, the same as `&&`.

Executed: `bash -e -c 'false; echo …'` exits 1 and prints nothing.
`bash -e -c 'false || true; echo …'` prints and exits 0.

Why it matters: the behaviour round 1 flagged ships unchanged. Four places
now state the opposite:

- the workflow's comment (`.github/workflows/publish-release.yml:106`);
- the case's docstring
  (`tests/test_a_release_publishes_its_note.py:694`);
- the ledger's `Corrected · W3` row, *the refresh not gating the install*
  (`seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md:27`);
- the overview's divergence row for phase 8
  (`seal/specs/1791270164-the-release-seal-is-drawn-in-curves/overview.md:54`).

The case holds the text `apt-get update;`, so it is green on a step that
does not do what the case says.

The fix is `|| true` after the refresh. The case's assertion below fails
against today's step and passes with the fix, both executed in the clone.
The finding sits in a `.yml` file, so the fix-of-a-fix count does not
read it.

### ⬜ 3 — `spec.md`'s foot fails the `release` job

`chain_check`'s `frame_foot` reads `spec.md` from its last line up. It
takes every `Reframed … after round <N>.` line, and the first line that is
not one must be `Framed … before the build.`
(`skills/code-review/scripts/chain_check.py:2636`). The last line,
`seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:419`, is
`Reframed 2026-10-07 by framer, after the owner's look at phase 2's
stamp.` It names no round, so `REFRAME_RE` does not match it. The job
stops at that step, and the six steps after it are skipped.

This is the run's paperwork, so it is a correction rather than a fix. It
still has to land before the pull request can go green. A probe committed
the fence below in the clone and re-ran `chain_check` there. The `spec.md`
refusal was gone. What remained were the round-1 record's
`Fixes checked by: nobody` and `Broad gate: not yet`, which this round's
record and the sealer answer. Four of the six skipped steps ran green in
the clone: the survivor check, the correction check, the mode check and
the CLAUDE.md block. The milestone step exits 0 on a base other than main,
by reading. The READMEs step was not run here; the job answers it once
⬜ 3 lands.

### ⬜ 4 — Round 1's record counts the merge's units as its fixes'

`round-1.md`'s `New units` row lists 111 units
(`seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13`).
109 of them are defined at `559977a3`. They came from #849, #851 and #855
through the merge, and their own pull requests reviewed them. The two that
round 1's fixes wrote are the two new cases:

- `test_a_mark_leading_a_continuation_row_beside_the_disc_is_drawn_in_its_style`
- `test_a_half_block_in_a_value_is_text_in_the_twin`

Both are judged above. The `Contract changes` row is the merge's too: no
commit of the fix pass touches `failure_lines` or `reason_for`.

Why it matters: the fix-of-a-fix rule reads this row. A later finding in
`hooks/gate.py` or the worktree guard would count as a fix of a fix, and
two of those send the work item back to its framer for code this branch
never wrote. The cause is `touched` in
`skills/code-review/scripts/round_record.py:3305`. It diffs `a..b` by path
and excludes no merge. The record is corrected here; the tool goes under
**Deferred**.

## Regression tests to plant

- **🟡 2** — `tests/test_a_release_publishes_its_note.py`,
  `test_the_seal_job_installs_rsvg_convert_before_the_suite_and_the_draw`:
  hold `|| true` instead of `;`. Seen red against today's step in the clone.
- **🔴 1** — none new: `test_only_neutral_domains` is the case, and it is
  red today.

## Facts for the evidence ledger

- `Corrected · W3` in `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`
  quotes the step's command. Rewrite it with `|| true` and re-stamp it with
  `evidence-check --reverify` once 🟡 2's fix lands.
- No other row moves. 🔴 1's fix changes a test module no row of this work
  item anchors.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `test_only_neutral_domains` is red on the ubuntu, macOS and Windows group 2 legs: the release SVG and its case carry the SVG namespace host, which `ALLOWED_DOMAINS` does not hold | `.github/scripts/release-seal.svg:1` | open | executed: the three legs' logs, 1 failed each, the same two lines; reproduced in the clone, exit 1; with the namespace's domain allowlisted, 5 passed. Phase 8's line, not a fix of a fix |
| 🟡 2 | Round 1's ⬜ 8 is not closed: the step runs under `bash -e`, so `apt-get update;` still ends it at a failed refresh, and the comment, the case, ledger W3 and an overview row say it does not | `.github/workflows/publish-release.yml:114` | open | executed: `bash -e` stops at `false;`, and `\|\| true` runs the next command; the proposed assertion is red against today's step and green with the fix. read: the PR's own job logs `-e` as its shell |
| ⬜ 3 | `spec.md` ends with a `Reframed` line that names no round, so `chain_check` refuses the foot and the `release` job is red | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:419` | open | a correction: executed, the job's log; the fence committed in the clone clears that refusal |
| ⬜ 4 | `round-1.md`'s `New units` row lists 109 units the merge brought, and `Contract changes` the merge's contracts | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | open | a correction: executed, 109 of 111 are defined at `559977a3`; the two others are the fix pass's cases |
| 🟢 | round 1's blocking finding is closed — the merge made the pull request mergeable, CI ran, and every row the release branch changed survived | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:1` | confirmed | executed: the four-point row probe; the six rows both sides changed differ from the release branch's only in the re-stamped SKILL.md anchor; `correction-check` exit 0 over two ranges; `evidence-check --strict` 0 drifted |
| 🟢 | round 1's 🟡 2 is closed, and so is its class: every styled cell beside the disc | `skills/verify/scripts/seal_stamp.py:492` | confirmed | executed: the case red with the guard reverted; a probe over 246 row sets at 0.90 and with no disc, every text cell shown as drawn |
| 🟢 | round 1's 🟡 3 is closed under any chart `read_chart` accepts | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:321` | confirmed | executed: green under seven charts, among them a checkerboard whose small stamp is 7,728 units |
| 🟢 | round 1's 🟡 4 is closed | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:553` | confirmed | executed: red with `RESET` padded by 300 spaces; green at the target and under seven charts |
| 🟢 | round 1's 🟡 5 is closed | `skills/verify/scripts/seal_stamp.py:514` | confirmed | executed: three parameters red with the fix reverted; read: `TITLE_RED` is no `KEY` colour |
| 🟢 | round 1's ⬜ 6 is closed | `hooks/sealer-stamp.py:41` | confirmed | read: *never smaller*; *the sheet* only where a case says it was retired |
| 🟢 | round 1's ⬜ 7 is closed | `skills/verify/scripts/seal_stamp.py:332` | confirmed | executed: the BOM copy red with the reader reverted; the encoding and line-reader modules, 305 passed |
| ❓ | The 109 units the merge brought, as code | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md:13` | ❓ out of verified scope | not reviewed here: they are #849's, #851's and #855's, reviewed at their own pull requests; the orchestrator decides whether that stands (⬜ 4) |
| ❓ | The full suite, lint and typecheck after the rounds settle | the tree at the last round's target | ❓ out of verified scope | not run (contract §2); the sealer answers, once, after 🔴 1 and 🟡 2 land |

## Executed probes

| What was run | Result |
|---|---|
| `gh pr checks 859 --watch` to the end, `gh pr view 859`, at `bf1a9447` | exit 1. Pass: `lint`, `ledger`, `arm-check-grammar` 3.13 and 3.14, Windows groups 1, 3 and 4. Fail: `release`, at *a declared review chain has the round record it claimed*; pytest ubuntu, macOS and Windows group 2. None pending. `MERGEABLE`, `UNSTABLE` |
| the ubuntu, macOS and Windows group 2 job logs | `test_only_neutral_domains` the one failure on each: 12,738, 12,730 and 6,706 passed |
| `tests/test_no_real_identifiers.py` in the clone, then with the namespace's domain in `ALLOWED_DOMAINS` | exit 1, 1 failed; exit 0, 5 passed |
| a test_tmp probe: each table row of the 1791270161 and 1791270165 fragments at `6de64c19`, `96127593`, `559977a3` and `f6d39425` | no release-branch row lost; six rows both sides changed, each equal to the release branch's but for the SKILL.md anchor |
| `bin/correction-check --range 559977a3...bf1a9447` and `--range 99bcad40..bf1a9447` | exit 0 each, no correction dropped, no released ledger file changed |
| `bin/evidence-check --strict .` at the target | exit 0, 6,835 ok · 0 drifted · 0 broken |
| the hook module whole; the sealer module's stamp slice (`-k` over disc, twin, letter, text lines, SGR, title, reference, chart, ladder, budget, mark, half-block, layout); the install case | exit 0: 35 passed; 281 passed; 1 passed |
| `856aeeec`'s change to `seal_stamp.py` reverted, the three new or changed cases | exit 1: the `✓` case, three half-block cases and the chart case failed, the `·` case passed |
| `bab19faa`'s workflow change reverted, the install case | exit 1, 1 failed |
| a test_tmp probe: 246 row sets at 0.90 and with no disc, every non-blank text cell against `what_a_terminal_shows` | exit 0, 2 passed |
| the pair case and the one-file case under the S, the key, and the empty, full, checkerboard, row-stripe and column-stripe charts | 2 passed under each of the seven; the archived § refused by `read_chart` |
| a test_tmp probe: a small stamp and a real run's stamp under those charts | small: S 4,662, key 4,135, empty 3,278, checkerboard 7,728; real: S 5,254, key 4,727, empty 3,870, checkerboard 8,320 |
| `RESET` padded by 300 spaces, the one-file budget case | exit 1, on *a real run's stamp no longer fits the budget with its disc* |
| `bash -e -c 'false; echo …'` and `bash -e -c 'false \|\| true; echo …'` | exit 1 with nothing printed; exit 0 and printed |
| 🟡 2's fence in the clone, the install case; the same case against today's step | exit 0, 1 passed; exit 1, 1 failed |
| ⬜ 3's fence committed in the clone, then `chain_check.py --baseline` against `559977a3` | the `spec.md` refusal gone; the round-1 record's `nobody` and `not yet` remain |
| the survivor, correction, mode and CLAUDE.md-block steps of the `release` job, in the clone | exit 0 each |
| the encoding and line-reader hygiene modules | exit 0, 305 passed |
| the full suite, lint and typecheck | not yet — the sealer's, once, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/code-review/scripts/round_record.py`'s `touched` diffs a fix range by path and excludes no merge, so a fix range holding a merge of the base lists the merge's units as the fixes' `New units` (⬜ 4) | a new issue against the round-record generator | the plugin's owner, through an issue the orchestrator opens |

## Paste-ready fixes

### 🔴 1

```python
ALLOWED_DOMAINS = (
    "example.com",  # the designated fixture domain — use this in examples
    "github.com",
    "arxiv.org",
    "claude.com",  # official docs this plugin is built against
    # The SVG namespace URI, which every SVG file carries for a renderer to
    # read it as SVG: an identifier, not an address (#832).
    "w3" ".org",
)
```

### 🟡 2

```yaml
      # dropped. `|| true` rather than `&&`: `apt-get update` exits non-zero
      # when any one list fails, a third-party list `librsvg2-bin` does not
      # come from included, and the install is still worth trying then. A
      # bare `;` is not enough: a step with no `shell:` runs under `bash -e`,
      # which ends the step at the failed refresh as `&&` did. Before the
      # suite, so the suite at the tag runs the one case that draws with the
      # real binary; an install that fails costs the image, and the draw's
      # `::warning::` says so.
      - name: install rsvg-convert
        continue-on-error: true
        run: sudo apt-get update || true; sudo apt-get install -y --no-install-recommends librsvg2-bin
```

```python
    The package lists are refreshed first, and the refresh does not gate
    the install: `apt-get update` exits non-zero when any one list fails,
    a third-party list the package does not come from included, so `&&`
    after it skipped an install that would have worked (round 1's ⬜ 8). A
    bare `;` skipped it too, because the step runs under `bash -e`, so the
    refresh is followed by `|| true` (round 2's 🟡 2)."""
```

```python
    run = next(line for line in held[at] if "librsvg2-bin" in line)
    assert "sudo apt-get update || true;" in run, run
    assert "apt-get update &&" not in run, run
```

```text
Both rows below sit in markdown tables, so each `|` of `||` is written `\|`.

ledger, Corrected · W3 — replace
  `sudo apt-get update; sudo apt-get install -y --no-install-recommends librsvg2-bin` (#832), the refresh not gating the install,
with
  `sudo apt-get update \|\| true; sudo apt-get install -y --no-install-recommends librsvg2-bin` (#832), the refresh not gating the install under the step's `bash -e`,
then: bin/evidence-check --reverify --into seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md --checked <today> .

overview.md, the phase 8 divergence row — its middle and right cells:
| The step runs `sudo apt-get update \|\| true; ` first — `&&` until round 1's ⬜ 8, `;` until round 2's 🟡 2 | A runner image's package lists can name a version the mirror has dropped, and that costs the image at the first tag. `\|\| true` because `apt-get update` exits non-zero when any one list fails, a third-party list included, and the step runs under `bash -e`, which ends it there after `&&` or `;` alike; the case holds the `\|\| true`. Q10 measures the step at the first tag (phase 8, rounds 1 and 2) |
```

### ⬜ 3

```markdown
The frame was redrawn on 2026-10-07 by framer, after the owner's look at
phase 2's stamp.

Framed 2026-10-06 by framer, before the build.
```

### ⬜ 4

```text
round-1.md, New units:
test_a_mark_leading_a_continuation_row_beside_the_disc_is_drawn_in_its_style (depth 1); test_a_half_block_in_a_value_is_text_in_the_twin (depth 1)

round-1.md, Contract changes:
none — the fix pass changed no unit's contract; the rows the generator wrote are the merge's
```

Needs a fix: yes — 🔴 1 (`test_only_neutral_domains` red on three legs), 🟡 2 (`apt-get update;` under `bash -e`)
Loses a record or crashes: no

The two corrections, ⬜ 3 (`spec.md`'s foot, which keeps the `release` job
red) and ⬜ 4 (round 1's `New units`), are the orchestrator's and are not
counted above. The broad gate has not come due: two findings are open.

## Proof block

Files opened this round, at `bf1a9447` in the clone unless noted:

- `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/rounds/round-1.md`, `rounds/round-1-report.md` (its head), `overview.md`, `survivors.md`, `changelog.md`, `spec.md` (its foot)
- `skills/verify/scripts/seal_stamp.py` (the style constants, `KEY`, `read_chart`, `colour_row`, `letter_row`, `text_lines`, `compose`, `stamp`)
- `hooks/sealer-stamp.py` (the changed docstring)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, `tests/test_a_release_publishes_its_note.py` (the changed cases)
- `.github/workflows/publish-release.yml` (the install step), `.github/workflows/hygiene.yml` (the `release` job's steps 9–15)
- `tests/test_no_real_identifiers.py` (`ALLOWED_DOMAINS`), `.github/scripts/release-seal.svg` (line 1), `tests/test_the_release_seal_is_drawn.py` (lines 30–42)
- `skills/code-review/scripts/chain_check.py` (`REFRAME_RE`, `frame_foot`, the mark's sentence), `skills/code-review/scripts/round_record.py` (`touched`)
- `tests/test_every_reader_ends_a_line_where_gfm_does.py` (the `read_chart` row), `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` (its tables)
- the diffs of `856aeeec`, `56e98860`, `bab19faa` and of round 1's records commits; the two foreign ledger fragments at four commits
- the job logs of PR #859's `release`, ubuntu, macOS and Windows group 2 runs
