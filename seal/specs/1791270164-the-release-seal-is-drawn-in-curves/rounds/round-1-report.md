# Round 1 report — 1791270164-the-release-seal-is-drawn-in-curves

| Field | Value |
|---|---|
| Target SHA | 9612759380174d6c1ae8935fbe1317032ed69c08 |
| Base | `6de64c19`, `git merge-base HEAD origin/release/v0.20.0` — the release branch's tip when the branch last merged it at `e90dbaed`. The release branch is now at `559977a3` |
| Pull request | #859 (draft) into `release/v0.20.0` |
| Round kind | first round, the branch's whole range `6de64c19..96127593` |
| Ran by | specseal:warden on claude-opus-5-5 |

HEAD did not move during the review: `96127593` at spawn and at hand-over.
Every probe ran in a `git clone --no-local` at the target, and nothing was
written to the worktree but this file.

## Summary

The build does what decisions 5 and 6 ask, and most of it holds under
execution. The S in the release SVG is Georgia Bold's outline to the last
decimal at all three anchors. The lean writer ends the disc's background
with `49` before the first blank, and `22;39` closes bold, dim and green
correctly. The 19 `Corrected ·` rows say what the code does, and the two
figures they measure (5,254 units at 80 × 14, a small pair at 9,488) come
out the same here. The release modules pass with the real `rsvg-convert`.

Five things need a fix, in the order one causes the next:

1. **The pull request cannot merge, so no CI ran on it** (🔴 1). The two
   foreign fragments the branch re-stamped in place were changed on the
   release branch too, and `gh pr checks 859` reports no checks at all.
2. **The lean writer drops the green on a tick that follows the disc
   through blanks** (🟡 2). Phase 6 removed the guard that prevented it as
   unreachable. It is reachable from any row, though `panel` writes none
   today.
3. **Replacing the mark turns a budget case red** (🟡 3). Decision 5 says
   changing the mark is changing `seal-mark.txt` alone. With the archived
   key, which the README says is accepted as it stands, two small stamps
   fit one message and the pair case fails on its asserted premise.
4. **The case cited as the 9,000 pin cannot fail on size** (🟡 4). A stamp
   over the budget is drawn without its disc, which is under the budget by
   construction, so the case passes. Six other cases catch it.
5. **The twin raises on a value that carries `▀` or `▄`** (🟡 5). The base's
   `letter_row` wrote a text cell's character first; this one keys on the
   character, so `KEY[None]` raises. That is the one crash this round found.

Three ⬜ remain: stale *sheet* wording in the hook and its cases, a BOM in
`seal-mark.txt` reported as a 29-character line, and the install step's
`&&`.

Two counts in the spawn prompt differ from the tree. The fragment carries
29 `Re-read ·` rows, not 21: phase 9 wrote 21, and 8 predate it. The range
adds 99 lines that carry `NAME NOT IN TREE` across the work item's files,
not 15. `evidence-check --strict .` reads 6,782 ok with nothing refused, so
every marker makes the checker pass. Whether each one is needed was not
judged (the ❓ row below).

## Findings from execution

### 🔴 1 — The pull request conflicts with its base, and GitHub ran no workflow

`gh pr checks 859` prints *no checks reported* and exits 1. `gh pr view 859`
says `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY`. A conflicting pull
request has no merge ref, so no `pull_request` workflow starts: test,
hygiene and every other check is missing, not red.

The conflict is the in-place re-stamps. `git merge-tree --write-tree HEAD
origin/release/v0.20.0` at the target conflicts in exactly two files,
`seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`
and `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md`. Phase 9
re-stamped rows there that `3d78c22`, `ec09faf` and `559977a` on the release
branch also touched. `skills/verify/SKILL.md`, `broad_gate.py` and the sealer
test module auto-merge, so they need the suite after the merge rather than a
hand resolution.

Why it matters: the pull request cannot merge as it stands, and no line of
this branch has met CI. The `Executed` cells across the records rest on
local slices alone until it does.

The re-stamp itself was the right remedy. `docs/the-evidence-ledger.md`
§*A citation that does not hold is named* says to re-stamp a fragment's row
in place rather than cite it. The cost is this conflict, which a merge and a
second `--reverify` pay.

### 🟡 2 — A tick after the disc on a `""` row is written `32;39`, and the terminal shows it plain

`colour_row` (`skills/verify/scripts/seal_stamp.py:486`) carries the
foreground across blank cells, because a space shows none. After the disc,
the running foreground is therefore the last disc colour. A `""` label is
eight spaces, so the first visible cell of such a row is its value's first
character. When that is a `✓ ` mark, the style part `32` is written and
then `fg != shown` writes `39` in the same SGR. SGR parts apply in order, so
`39` takes the foreground back from green to the terminal's own.

Probe, executed: rows `[("SEALED", ""), ("tree", "aaa1111"), None,
("suite", "x"), ("", "✓ 3 passed")]` at 0.90 write `\x1b[32;39m✓`. Read
through the S11 case's own `what_a_terminal_shows`, the `✓` is `None`, not
`green`.

Why it matters: `spec.md` §*Data & interfaces › The writers* says the
foreground part is *not written for a green cell, whose colour is the
style*. Phase 6 removed that guard as one *no cell can reach*
(`phases/phase-6.md`, `ac421623`). `panel` writes no `""` row with a tick
today, which is why no case saw it. But `text_lines` draws whatever rows it
is given, and its own docstring says so. A suite line that `wrapped` someday
breaks before the tick, or any values file, reaches it.

With the guard back (the fence below), the probe is green, and the S11,
S4a, reference, twin, layout, sample and budget cases pass, 26 of 26.

### 🟡 3 — The disc's mark sets whether the budget pair case's premise holds

Decision 5 says *changing the mark later is changing that chart alone*.
`spec.md` §In 2 says *no case pins the S's shape*, and `plan.md`
constraint 7 says only the reference case goes red when #857 replaces the
chart. The changelog says changing the mark *is replacing that one file*.

Probe, executed: `assets/seals/candidates/key-28.txt` copied over
`seal-mark.txt`, then the drawing cases of the two stamp modules, 40
selected. Two fail. The reference case fails as planned. So does
`test_several_files_come_out_one_stop_each_oldest_first`
(`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:343`): with
the key, a `SMALL_ROWS` stamp is 4,216 units and the pair is 8,434, under
the 9,000 budget, so the asserted premise *two small stamps share one
message again* fires.

Why it matters: the key is the one 28-cell candidate the README says is
*accepted as it stands*. #857 will meet a red case that the frame promised
would not go red, with a message that blames the case. The case's
behaviour, one stamp per `Stop` oldest first, does not depend on the mark;
only its fixture's size does. `test_two_files_in_one_turn_are_under_the_budget_together`
already grows its fixture until the pair does not fit. The same derivation
fixes this one, and was run green over both the S and the key (fence
below).

The same dependence sits in three sentences that are true for the S and
not for every mark: `B2`'s *no two stamps of any panel the cases draw share
one message*, the policy's *one real run's stamp goes out per message*, and
the hook case docstring's *9,488*. For a real run they hold with the key
too, because a full panel's pair is still over the budget. They are
grounds for the fix, not separate findings.

### 🟡 4 — The case cited as the 9,000 pin passes with a stamp over 9,000

`test_the_hooks_message_is_under_the_budget_for_one_file`
(`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:543`)
asserts `len(text) <= MESSAGE_BUDGET` and the label. But `admitted` returns
the text block with no disc when a block does not fit with its disc, and
that block is under the budget whatever the disc's size. So the assertion
holds by construction.

Probe, executed with `bin/mutation-check`: `RESET` padded by 300 spaces
makes the real run's stamp 9,454 units with its disc. The case
**survived**. A probe over the same mutation shows the hook's message at
3,696 units with no disc. With the hook module run whole under the same
mutation, seven cases fail, among them
`test_seals_past_what_one_message_carries_wait_for_the_next_turn`. The
property is held, but not by this case.

Why it matters: this is the case the records name as the pin. `spec.md`
S5 and `plan.md` constraint 3 call it the case that *pins one real-size
stamp under the budget through the real hook*, `questions.md` Q3 cites it,
the ledger's `Corrected · B2` anchors it, and `docs/the-broad-gate.md` lists
it first on the budget paragraph's `Enforced by:` line. One assertion makes
it hold the stamp WITH its disc. That version was seen red under the same
mutation and green at the target.

### 🟡 5 — The letter twin raises `KeyError` on a value that carries a half-block

`letter_row` (`skills/verify/scripts/seal_stamp.py:506`) asks whether a
cell's character is `▀` or `▄` and then looks up `KEY[fg]`. A text cell's
foreground is `None`, so a value carrying either character raises.

Probe, executed: `stamp([("SEALED", ""), ("tree", "a▀b")], 0.9,
shape=True)` raises `KeyError: None`.

Why it matters: the base's `letter_row` wrote a text cell's own character
before it looked at any colour, so this is behaviour the diff removed. A
branch name may carry the character, because git allows UTF-8 in a ref,
and `panel` puts the branch on a row. The gate draws the twin on a console
that is not UTF-8 or on `--shape`, after the cell is written
(`skills/verify/scripts/broad_gate.py:3503`), with no `try` around it. The run would end in a
traceback over a written seal. `seal-stamp --shape --from` raises the
same way. The input is unlikely, but the failure is a crash, so the floor
line below says yes. Keyed on the colour (`fg in KEY`), the probe draws and
the twin, reference, symmetry, same-bytes and piped cases pass, 15 of 15.

### ⬜ 7 — A chart saved with a BOM is refused as a 29-character first line

`read_chart` opens the chart as `utf-8`, so a byte-order mark is a
character of line 1. Probe, executed: the shipped chart written back with
`utf-8-sig` is refused with *line 1 is 29 characters*, which sends a
person looking for an extra dot. `encoding="utf-8-sig"` reads both, and it
still names its encoding. The refusal is right, only its fault is
misleading.

## Findings from reading

### ⬜ 6 — Six sentences still call the no-disc rung *the sheet*, and the hook says a stamp can be drawn smaller

`hooks/sealer-stamp.py:40` says *a stamp may therefore be drawn smaller
than its file's `scale` says*. The disc has one size since phase 3, so a
stamp is never smaller, only without its disc. The branch edited this
sentence and kept the word.

In `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, the no-disc
rung is *the sheet* in the budget case's assert message (`:539`, *then the
sheet alone*), the oversized case's docstring and its assert message
(`:768`, `:790`), and the ladder case's docstring (`:856`–`:857`). The S8
class is every place that describes the sheet. `survivors.md` does not
excuse these, and `survivor-check` cannot see them, because they are prose
rather than a removed name. A reader of a failing case is told about a
sheet that no longer exists.

### ⬜ 8 — `apt-get update &&` skips an install that might have succeeded

`.github/workflows/publish-release.yml:111` runs `sudo apt-get update && sudo
apt-get install …`. `apt-get update` exits non-zero when any one list
fails, including a third-party list on the runner image that has nothing
to do with `librsvg2-bin`. Then the install never runs and the seal is
skipped with a `::warning::`. `overview.md` gives the reason for the update,
which stands. `;` in place of `&&` keeps the refresh and still tries the
install. The cost of either is the image, never the release, so this is ⬜.

### What was checked and holds

- **The mark.** `read_chart` refuses 27 lines, a 29-character line, a
  stray character and an `M` outside the field, each with the path and the
  fault. The extra refusal (an `M` in the groove) is right: `build` paints
  the groove over such a cell, so the mark would lose a cell nobody sees
  go. The archived § is refused at line 5, columns 12, 17 and 18
  (1-based), exactly as the README and `overview.md` say. The key is
  accepted. The 14-cell § is refused as 14 lines, which the README says.
  No case in the sealer module pins the S; the reference case pins it by
  design (constraint 7), and 🟡 3 is the one case that pins it by accident.
- **The lean writer.** `49` ends the disc's background at the first blank
  after it, and a line with no text ends at the disc's last visible cell
  under `RESET`. `22;39` closes bold, dim and green, and `shown = None`
  keeps a second `39` out of the same SGR. A line that wrote no code ends
  with no `RESET`, and the line before it always ends with one. The S11
  case reads each line as a terminal would, which is how 🟡 2 is
  demonstrable at all.
- **The panel.** `·` dims only `CI also`'s value and `✓` marks only a
  result row whose count or exit was read. A value is `·` or `✓` followed
  by a space or it is text. `fit`'s `width` gives the ref the room its
  commit leaves, so the ref keeps its tail. `wrapped` holds back two
  columns and strips `·` from a continuation's lead. Every label `panel`
  writes is at most seven columns, so `28 + 3 + 8 + 41 = 80` holds for
  every row. `CI also` reads `· 4 more steps` for a feature seal and `· 8
  more steps` for a release seal, in the gate's module and in
  `skills/verify/SKILL.md`. `TWIN_ASCII` maps the four characters one for
  one, and the twin over a real run is ASCII.
- **The release path.** The three `<path>` layers are Georgia Bold's `S`
  at font-size 20, anchored at half its advance and its baseline. The
  outline was rebuilt here from the font with fontTools, and every
  coordinate of all three layers matches to 0.000. Fills and opacities are
  the owner's three. `sealed_glance` escapes the URL and the alt with
  `html.escape`, quotes included, and `int(width)`. The `rsvg-convert`
  stand-in hands every other command to the real `subprocess.run`, captured
  before the patch. The install step precedes the suite and the draw and is
  `continue-on-error`. `rasterise` raises `Refused` for a missing SVG, a
  missing binary and a non-zero exit, and `main` turns any other exception
  into the same warning and exit 0.
- **The records.** The 19 `Corrected ·` rows were read against the code.
  L1's 80 × 14 and 5,254, and B2's pair of 9,488, were measured here and
  agree. N10's and P2's `· 4 more steps` and `· 8 more steps` are the
  values the steps module asserts. Of the 29 `Re-read ·` rows, ten were
  read against their released claim: 0.10.0 S3, 0.12.2 G6, 0.15.1 G2,
  0.15.7 N5, 0.17.0 B3 and N8, and 0.18.0 W1, W2, W4 and R3. Each holds.
  The other 19 cite `COVERED`, `CONTRIBUTING.md`, `agents/sealer.md` or the
  checklist's §6, and this range's change to each is a hunk read in full
  that touches no clause those claims state. That is a reading of the
  hunks, not of each released row. `evidence-check --strict .` at the
  target exits 0.

## What earlier rounds found

None. This is the work item's first round, and `rounds/` held no record.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the S11
  case: a `""` row whose value leads with `✓ `, drawn beside the disc, read
  through `what_a_terminal_shows`, its tick green (🟡 2). Seen red at the
  target in this round.
- `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`: the one-file
  budget case asserts the message is the stamp with its disc (🟡 4). Seen
  red under the padded `RESET`.
- The same module: the pair case grows its fixture until the pair does not
  fit (🟡 3). Green over the S and over the key.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the twin
  case: a value carrying `▀` draws in the twin (🟡 5). Red at the target.

## Facts for the evidence ledger

- The release SVG's three `<path>` layers are Georgia Bold's `S`
  (`/System/Library/Fonts/Supplemental/Georgia Bold.ttf`, 2,048 units to the
  em) at font-size 20, each at half the advance and the baseline of its
  anchor, `(16.5, 21.5)`, `(16, 21)` and `(15.7, 20.7)`. All 158 numbers of
  each layer equal fontTools' outline at three decimals (executed, this
  round). This is what `Corrected · R1` states, measured.
- With `assets/seals/candidates/key-28.txt` as the mark, a `SMALL_ROWS`
  stamp is 4,216 units at 0.90 with its label, and two share one message
  (executed). Whether two small stamps share a message is the chart's, not
  the frame's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The pull request conflicts with `release/v0.20.0` in the two foreign fragments phase 9 re-stamped, so GitHub ran no workflow on it | PR #859 against `release/v0.20.0` at `559977a3`; `seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md` | open | executed: `gh pr checks 859` reports no checks, exit 1; `mergeable: CONFLICTING`; `git merge-tree` conflicts in exactly the two fragments |
| 🟡 2 | The lean writer writes `32;39` for a tick that follows the disc through blanks, so the tick is drawn in the terminal's own colour, not green | `skills/verify/scripts/seal_stamp.py:486` | open | executed: the probe writes `\x1b[32;39m✓`, and `what_a_terminal_shows` reads it as not green; the guard phase 6 removed as unreachable restores it, 26 cases green |
| 🟡 3 | `test_several_files_come_out_one_stop_each_oldest_first` asserts a premise the mark sets, so replacing `seal-mark.txt` with the accepted key turns it red | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:343` | open | executed: with the key, two `SMALL_ROWS` stamps are 8,434 units and the premise fires; the derived fixture is green over both charts |
| 🟡 4 | `test_the_hooks_message_is_under_the_budget_for_one_file` cannot fail on the stamp's size, because the no-disc rung is under the budget by construction | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py:551` | open | executed: `mutation-check` with the stamp at 9,454 units survived; the message was 3,696 with no disc; one added assertion turns it red |
| 🟡 5 | The letter twin raises `KeyError` on a value carrying `▀` or `▄`, which the base's `letter_row` wrote as text | `skills/verify/scripts/seal_stamp.py:506` | open | executed: `stamp(..., shape=True)` over `("tree", "a▀b")` raises `KeyError: None`; keyed on `fg in KEY`, 15 twin cases green |
| ⬜ 6 | The hook says a stamp can be drawn smaller, and four places in the hook's cases call the no-disc rung the sheet | `hooks/sealer-stamp.py:40` | open | read: the disc has one size since phase 3; `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` lines 539, 768, 790 and 856 |
| ⬜ 7 | A chart saved with a byte-order mark is refused as a 29-character first line | `skills/verify/scripts/seal_stamp.py:330` | open | executed: the shipped chart written as `utf-8-sig` is refused with that fault |
| ⬜ 8 | `apt-get update &&` skips the install whenever any list on the runner fails to refresh | `.github/workflows/publish-release.yml:111` | open | read: the install has no dependency on a third-party list; `;` keeps the refresh |
| 🟢 | The release SVG's S is Georgia Bold's outline at the owner's three anchors, fills and opacities | `.github/scripts/release-seal.svg:21` | confirmed | executed: fontTools' outline equals every coordinate of all three layers |
| 🟢 | `read_chart`'s refusals, and the archived §'s refusal at line 5, columns 12, 17 and 18 | `skills/verify/scripts/seal_stamp.py:323` | confirmed | executed: the three cells listed from the chart; the key accepted |
| 🟢 | `49` ends the background at a blank, and `22;39` closes bold, dim and green at a change and `RESET` at a line's end | `skills/verify/scripts/seal_stamp.py:462` | confirmed | read, and executed through the S11 case at the target |
| 🟢 | The panel's rows, `fit` and `wrapped` with `width`, the `CI also` row and the twin's ASCII mapping | `skills/verify/scripts/broad_gate.py:2976` | confirmed | read; the drawing cases ran green at the target, and the panel's own cases were not run this round |
| 🟢 | `<img width>` escaping, the stand-in's pass-through, the install step's place, and `rasterise`'s three refusals | `.github/scripts/publish_release_note.py:393` | confirmed | executed: the two release modules, 68 passed with `rsvg-convert` 2.58.4 present |
| 🟢 | The 19 `Corrected ·` rows say what the code does | `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md:1` | confirmed | read; L1's and B2's figures measured and equal |
| ❓ | Whether each of the 99 `NAME NOT IN TREE` lines the range adds is needed, and 19 of the 29 `Re-read ·` rows against their full released claim | `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md:1` | ❓ out of verified scope | not judged line by line; the checker passes with all of them. Answered by the orchestrator, who decides whether round 2 reads them |
| ❓ | The `apt-get` install on `ubuntu-latest` and `<img width="160">` on a published release page (Q10, Q4) | `.github/workflows/publish-release.yml:111` | ❓ out of verified scope | nothing but a tag runs the job; the release session answers at 0.20.0's tag, as `overview.md` §*Not verified* says |
| ❓ | The full suite, lint and typecheck after the rounds settle | the tree at the last round's target | ❓ out of verified scope | not run (contract §2); the sealer answers, once, after the merge in 🔴 1 |

## Paste-ready fixes

### 🔴 1

Merge the release branch, resolve the two fragments, then re-stamp. In each
conflicted hunk, keep the release branch's row text and drop this branch's
stamp of it: the re-stamp is regenerated by the second command.

```sh
git -C <worktree> merge origin/release/v0.20.0
# resolve seal/ledger/1791270161-…md and seal/ledger/1791270165-…md: take the
# release branch's side of each conflicted row, then
bin/evidence-check --reverify --into seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md --checked <today> .
bin/evidence-check --strict .
git -C <worktree> push
gh pr checks 859
```

Read each row `--reverify` names before dating it, as
`docs/the-evidence-ledger.md` asks; the seal and stamp modules auto-merged,
so the stamp and sealer slices run once after the merge.

### 🟡 2

`skills/verify/scripts/seal_stamp.py`, in `colour_row`:

```python
            if fg != shown and style != "green":
                parts.append(colour_code(38, fg))
```

And the docstring's last sentence:

```python
    first, which takes the foreground back to the terminal's own as well, so
    `39` is not written a second time in the same SGR. A green cell writes no
    foreground part: `32` is its colour, and a `39` after it in the same SGR
    would take the green back off."""
```

The case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py` after
the S11 case:

```python
def test_a_tick_beside_the_disc_on_a_continuation_row_is_green():
    """#832 S11. A `""` label is spaces, which carry the disc's foreground
    across to the value, so a tick leading a continuation row beside the
    disc is the first cell to change it. Its SGR is `32` alone: a `39` after
    `32` in one SGR takes the green back off, and the terminal draws the
    tick in its own colour."""
    mod = module()
    rows = [("SEALED", ""), ("tree", "aaa1111"), None, ("suite", "x"), ("", "✓ 3 passed")]
    letter = mod.compose(rows, 0.9)
    ticks = 0
    for cells, line in zip(letter.cells, mod.stamp(rows, 0.9), strict=True):
        shown = what_a_terminal_shows(line.removesuffix(RESET))
        for (_char, _fg, _bg, style), seen in zip(cells, shown, strict=True):
            if style == "green":
                ticks += 1
                assert seen[1] == "green", (line, seen)
    assert ticks == 1, ticks
```

### 🟡 3

`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, the body of
the pair case up to its first `stop`:

```python
    mod = stamp_module()
    repo = opted_in(tmp_path)
    other = LABEL.replace("aaa1111", "ccc3333")
    rung = mod.SCALE_LADDER[-1]
    # The disc's mark sets a stamp's size (#857 replaces it), so the pair is
    # grown until it does not fit rather than assumed not to.
    rows = list(SMALL_ROWS)
    while sum(len(drawn(mod, who, rows, rung)) for who in (LABEL, other)) + 2 <= (
        mod.MESSAGE_BUDGET
    ):
        rows.append(("", f"home-{len(rows)}"))
    small = values(rows=rows)
    first = mod.write_values(str(repo / ".git"), "s-1", small, now=1)
    second = mod.write_values(
        str(repo / ".git"), "s-1", {**small, "tree": "ccc3333"}, now=2
    )
    broken = os.path.join(os.path.dirname(first), "3-ddd4444.json")
    with open(broken, "w", encoding="utf-8") as handle:
        handle.write("not json")
    older, newer = (drawn(mod, who, rows, rung) for who in (LABEL, other))
    assert len(older) + 2 + len(newer) > mod.MESSAGE_BUDGET
```

The docstring's *even the smallest panel's pair is over the budget together
(9,488 units)* then reads *the pair is grown until it is over the budget
together, because the mark sets a stamp's size*.

### 🟡 4

`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, at the end
of the one-file budget case:

```python
    assert len(text) <= mod.MESSAGE_BUDGET, len(text)
    assert text.split("\n", 1)[0] == mod.label(full_values())
    # Under the budget by itself is what `admitted` guarantees whatever the
    # stamp's size, by dropping the disc; a real run's stamp has to fit WITH it.
    assert text == drawn(mod, mod.label(full_values()), FULL_ROWS, 0.9), (
        "a real run's stamp no longer fits the budget with its disc"
    )
```

### 🟡 5

`skills/verify/scripts/seal_stamp.py`, in `letter_row`:

```python
    out = []
    for char, fg, _bg, _style in cells:
        if char in HALF_BLOCKS and fg in KEY:
            out.append(KEY[fg])
        else:
            out.append(TWIN_ASCII.get(char, char or " "))
    return "".join(out)
```

The case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py` after the
twin case:

```python
def test_a_half_block_in_a_value_is_text_in_the_twin():
    """#832 S4. A disc cell is a half-block in a disc colour; a value that
    carries `▀` or `▄` — a branch may — is text, written as itself, as the
    twin before #832 wrote every text cell. Keyed on the character alone,
    the twin looked up the text's foreground and raised."""
    mod = module()
    twin = mod.stamp([("SEALED", ""), ("tree", "a▀b▄c")], 0.9, shape=True)
    assert any(line.endswith("tree    a▀b▄c") for line in twin), twin
```

## Executed probes

| What was run | Result |
|---|---|
| the drawing cases of the two stamp modules (`-k` over disc, twin, letter, text lines, SGR, title, reference, chart, ladder, budget, one stop) at the target | exit 0, 40 passed |
| the same 40 with `key-28.txt` copied over `seal-mark.txt` | exit 1, 2 failed: the reference case and the pair case, the pair at 8,434 units |
| the two release modules at the target, `rsvg-convert` 2.58.4 on `PATH` | exit 0, 68 passed |
| `bin/evidence-check --strict .` at the target | exit 0, `total: 6782 ok · 0 drifted · 0 broken`, 0 refused |
| a test_tmp probe: the writer over a `""` row leading with `✓`, the twin over `a▀b`, the three candidates and three malformed charts through `read_chart` | `\x1b[32;39m✓`; `KeyError: None`; § refused at line 5 column 12, key accepted, 14-cell refused as 14 lines; CRLF accepted, BOM refused as *line 1 is 29 characters*, a trailing blank line refused as 29 lines |
| a test_tmp probe: `full_values()`' stamp and message, and the `SMALL_ROWS` pair | 80 × 14, 5,254 units; pair 9,488; the twin ASCII |
| `mutation-check`, `RESET` padded by 300 spaces, against the one-file budget case | SURVIVED |
| the same mutation, a probe of the hook's message | the message 3,696 units with no disc; the stamp with its disc 9,454 |
| the same mutation, the hook module whole | exit 1, 7 failed, among them the twelve-file case |
| the one-file case with 🟡 4's assertion, under the same mutation | red; green at the target as `mutation-check`'s baseline |
| a test_tmp case for 🟡 2 at the target, then with 🟡 2's fix, beside the S11, S4a, reference, twin, layout, sample and budget cases | red at the target; 26 passed with the fix |
| 🟡 3's derived pair case over the S and over the key | 1 passed each |
| 🟡 5's fix, the twin over `a▀b`, then the twin, reference, symmetry, same-bytes and piped cases | draws; 15 passed |
| fontTools' outline of Georgia Bold's `S` against the SVG's three paths, through `uvx --from fonttools` | 158 numbers per layer, the largest difference 0.000 |
| `git merge-tree --write-tree HEAD origin/release/v0.20.0` at the target | conflicts in the 1791270161 and 1791270165 fragments only |
| `gh pr checks 859`; `gh pr view 859` | no checks reported, exit 1; `CONFLICTING`, `DIRTY` |
| the full suite, lint and typecheck | not yet — the sealer's, once, after the rounds settle and the merge in 🔴 1 |

Needs a fix: yes — 🔴 1 (merge the release branch and get CI to run), 🟡 2 (the green tick after the disc), 🟡 3 (the pair case's premise follows the mark), 🟡 4 (the one-file budget case cannot fail), 🟡 5 (the twin raises on a half-block in a value)

Loses a record or crashes: yes — 🟡 5: the letter twin raises `KeyError` on a panel value carrying `▀` or `▄`, and the gate's terminal path raises it after the cell is written

## Proof — files opened

`seal/specs/1791270164-the-release-seal-is-drawn-in-curves/` `routing.md`,
`spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
`phases/phase-5.md` to `phase-9.md`; `seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md`
(the 19 `Corrected ·` rows whole, the 29 `Re-read ·` rows' citations);
ten released rows in `seal/releases/` 0.10.0, 0.12.2, 0.15.1, 0.15.7,
0.17.0 and 0.18.0; `skills/verify/scripts/seal_stamp.py` (lines 1–720 and
955–1075) and `seal-mark.txt`; the diff of `skills/verify/scripts/broad_gate.py`
with its `main` from line 3300; `.github/scripts/release_seal.py`'s diff and
its `seal_release` and `main`; `.github/scripts/release-seal.svg`; the diffs
of `publish_release_note.py`, `run_tests.py`, `publish-release.yml`,
`test.yml`, `hooks/sealer-stamp.py`, `docs/the-broad-gate.md`,
`skills/verify/SKILL.md`, `agents/sealer.md`, `docs/branch-and-release.md`,
`docs/release-checklist.md`, `CONTRIBUTING.md` and
`tests/test_a_release_publishes_its_note.py`;
`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` lines 250–875;
`tests/test_the_seal_is_taken_once_by_the_sealer.py` lines 130–850;
`tests/test_the_release_seal_is_drawn.py` lines 60–230, 570–610 and
700–775; `assets/seals/README.md`'s candidates section and
`candidates/section-28.txt`; `docs/the-evidence-ledger.md` lines 110–150;
`bin/test`; `bin/mutation-check`.
