# 1791270164-the-release-seal-is-drawn-in-curves — review round 1

| Field | Value |
|---|---|
| Target SHA | 9612759380174d6c1ae8935fbe1317032ed69c08 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #859 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (merge the release branch and get CI to run), 🟡 2 (the green tick after the disc), 🟡 3 (the pair case's premise follows the mark), 🟡 4 (the one-file budget case cannot fail), 🟡 5 (the twin raises on a half-block in a value) |
| Loses a record or crashes | yes — 🟡 5: the letter twin raises `KeyError` on a panel value carrying `▀` or `▄`, and the gate's terminal path raises it after the cell is written |

- [ ] Pass

## What this round was asked

Round 1 of #832's review run, at 96127593, the head of draft PR #859, over the branch's own range from its merge base with `origin/release/v0.20.0` (6de64c19). The build covered the owner's final seal and layout: phases 5–9 after the re-frame at 62f1b47d.

The reviewer was asked to judge:
- whether changing `seal-mark.txt` changes the mark alone, and whether `read_chart`'s refusals are right;
- the lean writer and the open layout, against the 9,000 budget;
- the panel's rows, `fit` and `wrapped`, and the twin's mapping;
- the release path: the SVG's S paths, the `rsvg-convert` stub and the install step;
- the 19 `Corrected ·` rows, the `Re-read ·` rows and the in-place re-stamps;
- every workflow of `gh pr checks 859`.

It did not run the full suite.

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

```sh
git -C <worktree> merge origin/release/v0.20.0
# resolve seal/ledger/1791270161-…md and seal/ledger/1791270165-…md: take the
# release branch's side of each conflicted row, then
bin/evidence-check --reverify --into seal/ledger/1791270164-the-release-seal-is-drawn-in-curves.md --checked <today> .
bin/evidence-check --strict .
git -C <worktree> push
gh pr checks 859
```
```python
            if fg != shown and style != "green":
                parts.append(colour_code(38, fg))
```
```python
    first, which takes the foreground back to the terminal's own as well, so
    `39` is not written a second time in the same SGR. A green cell writes no
    foreground part: `32` is its colour, and a `39` after it in the same SGR
    would take the green back off."""
```
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
```python
    assert len(text) <= mod.MESSAGE_BUDGET, len(text)
    assert text.split("\n", 1)[0] == mod.label(full_values())
    # Under the budget by itself is what `admitted` guarantees whatever the
    # stamp's size, by dropping the disc; a real run's stamp has to fit WITH it.
    assert text == drawn(mod, mod.label(full_values()), FULL_ROWS, 0.9), (
        "a real run's stamp no longer fits the budget with its disc"
    )
```
```python
    out = []
    for char, fg, _bg, _style in cells:
        if char in HALF_BLOCKS and fg in KEY:
            out.append(KEY[fg])
        else:
            out.append(TWIN_ASCII.get(char, char or " "))
    return "".join(out)
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
