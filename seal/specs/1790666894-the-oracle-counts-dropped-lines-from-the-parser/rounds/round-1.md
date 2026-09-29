# 1790666894-the-oracle-counts-dropped-lines-from-the-parser — review round 1

| Field | Value |
|---|---|
| Target SHA | 2ee3e62f0874779e38952c59048606748e20aec5 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #681 — https://github.com/MichaelYcJo/SpecSeal/pull/681 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `80845d3829a289ad78a5c04860a5877d2bd732ec..bcbed21fa15393f66b1a6dc37d5b83dd6b0da1eb`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 over the branch `cd56113c..2ee3e62f`. Spec compliance first, then quality. The pushes:
- whether the wrapper reads the parser's own dropped count on every path through `paragraph` and `lheading`, checked by a differential against CommonMark;
- whether each new case is red against the code it was written for, and whether the guard fails where it says it does;
- whether wrapping markdown-it-py's rules leaks state, and whether the module holds on 3.12 and 3.14;
- whether H's record edits and the `NAME NOT IN TREE` marks are true;
- whether the changelog fragment's trigger, "a line of only a Unicode space", is complete given U+001F.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The changelog fragment and three docstrings name the trigger as a line of only a Unicode space; U+001F, a C0 control, triggers the same false red and is fixed too, and one docstring says every row opens with such a line where two rows' paragraphs do | `seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/changelog.md:4` | answered | `328894c6` — the changelog fragment and three docstrings (`_recording_lines`, `_inline_html_lines`, `test_the_oracle_counts_the_lines_the_parsers_strip_dropped`) now name U+001F beside a no-break space and the other Unicode spaces as a trigger, and the case's docstring says every row's paragraph, not every row, opens with such a line; U+001F on S1a gives `{}` at `cd56113c` and `{3: 'inline html'}` at head. The two ledger rows the edit drifted are re-read and re-stamped; Executed: all 17 characters of the S4 set, U+001F among them, give `{}` at the base and `{3}` at the head on the S1a shape; also `tests/commonmark_oracle.py:84`, `:123` and `tests/test_the_hooks_hide_what_a_renderer_hides.py:262` |
| ⬜ 2 | H's P1-1 keeps a round 2 `Re-read` note that the deletion made false, and the new `Corrected` note names only round 1's sentence | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` P1-1 | answered | `bcbed21f` — H's P1-1 carries a `Corrected 2026-09-29` note saying its round 2 note no longer holds: `_behind_markers` (NAME NOT IN TREE: phase 1 deleted it) and R1-1 went in phase 1, and round 2's nine rows stand in `test_the_oracle_names_each_kind_it_hides`; Read: the round 2 note says the helper is told whether a line opens the paragraph and that R1-1 is the claim about both; the helper and R1-1 are gone. Paperwork, so not counted in `Needs a fix` |
| 🟢 | The wrapper reads the count the parser drops on every path through `paragraph` and `lheading`: setext, lazy lines, interruption by a list, fence, HTML block or heading, end of input, and nested containers | `tests/commonmark_oracle.py:73` | confirmed | Executed differential against a mark appended at a line's end: 117,206 line questions, 0 disagreements at the head and 26 at the base |
| 🟢 | Every new case is red against the code it was written for, and the guard fails where its docstring says | `tests/test_the_hooks_hide_what_a_renderer_hides.py:186` | confirmed | Executed, seven mutations: base oracle 6 failed; `lheading` unwrapped 3; count 0 53, with the S4 second shape 17 of 17 run apart; set emptied and set of a space and a tab both red on the guard alone |
| 🟢 | Wrapping leaks no state and changes no token | `tests/commonmark_oracle.py:100` | confirmed | Executed: a fresh parser keeps the library's rule functions; 30,000 documents give identical token streams; the module passes 129 of 129 on 3.12.11 and 3.14.3 |
| 🟢 | H's R1-1 removal, P1-1 correction and 24 markers are true, and the checkers agree | `seal/ledger/1790659274-the-walk-leaves-every-inline-html-construct-uncertain.md` | confirmed | Executed: with the markers stripped the records arm refuses 26 names on those 24 lines, all the one deleted helper; `evidence-check` 0 drifted and `--strict` exit 0; `correction-check` exit 0 with no merge commit in range |
| 🟢 | The expected answers of the 24 rows and 34 S4 shapes are CommonMark's | `tests/test_the_hooks_hide_what_a_renderer_hides.py:186` | confirmed | Executed against cmark 0.29.0.gfm.2: 58 of 58 agree |
| ❓ | The module on Python 3.13 and on CI's Linux and Windows legs | `.github/workflows/test.yml:35` | ❓ out of verified scope | Only macOS on 3.12.11 and 3.14.3 ran here. The oracle is pure Python and reads no path, so the risk is low. The sealer's broad run and CI at the pull request answer it |

## Paste-ready fixes

```markdown
- The suite's CommonMark oracle no longer reports a false disagreement with
  the hooks' walk on a paragraph that opens with a line holding only
  characters Python's `str.strip` removes and CommonMark reads as text (a
  no-break space, another Unicode space, or U+001F) and has a `>` indented
  four columns, or behind a tab, on a later line (#677). markdown-it-py's
  strip drops such an opening line, and the oracle
```
```python
    The joined lines end in `\\n` and only there, so every `\\n` inside what
    `lstrip` removes from the top ends a line it removed whole, whichever of
    the characters the strip removes that line held, U+001F among them
    (#677)."""
```
```python
    `str.strip` applied to the whole by the parser. That strip also takes a
    line holding only a no-break space, another Unicode space or U+001F,
    which CommonMark reads as paragraph text, so the lines it dropped from
    the top are counted before an offset is turned into a line. The parser's own
```
```python
    """#677. The parser joins a paragraph's lines from behind the container
    markers it consumed and applies `str.strip` to the whole, which also
    drops a line holding only a no-break space, another Unicode space or
    U+001F, which CommonMark reads as text. Every row's paragraph opens with
    such a line, so every row puts its inline HTML one line early or late
    wherever the oracle counts those lines wrong.
```
```markdown
**Corrected 2026-09-29 in phase 1 of work item 1790666894 (#677):** the round 1 note's last sentence and the round 2 note are no longer true.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q` in the clone at `2ee3e62f`, Python 3.14.3 | exit 0, 129 passed |
| the same module through `uv run --isolated --no-project --python 3.12 --with pytest --with markdown-it-py==4.2.0` | exit 0, 129 passed on 3.12.11 |
| the module under seven mutations, `-p no:xdist`, restored after each | as tabled under *Every new case is red*; `git status` clean after |
| differential: a mark appended at line K-1's end against the oracle's lines, 60,000 seeded documents, head and base | head 0 of 117,206 disagree; base 26 of 117,206 |
| coverage count over the same documents: inline tokens with a dropped line | 2,990 paragraph and 51 setext tokens with a dropped line and inline HTML |
| wrapped against fresh parser over 30,000 documents, and the fresh parser's rule functions | 0 documents differ; `paragraph` and `lheading` are the library's own |
| the S4 second shape under the count-0 mutation; all 34 S4 shapes at the base oracle | 17 of 17 red; 0 of 34 red |
| the S1a shape opened by each of the 17 S4 characters, and by mixed lines, base against head | base `{}` and head `{3}` for all 17, U+001F included, and for the mixed lines |
| the 24 new rows and 34 S4 shapes through cmark 0.29.0.gfm.2 | 58 of 58 agree |
| the records arm with H's 24 markers stripped, restored after | exit 2, 26 refused, every one the deleted helper, on exactly the 24 lines; `git status` clean after |
| `bin/evidence-check .` and `bin/evidence-check --strict .` | exit 0 both; 2,992 ok, 0 drifted, 0 broken; records arm 0 refused |
| `bin/correction-check --range cd56113c...HEAD` | exit 0: no merge commit in range |
| `bin/unverified-check` on the work item | exit 0: 1 open (the sealer's), 2 closed |
| a dry `round-record new` over this report, in the clone, the record deleted with the clone | the record was written: three tables, `Needs a fix` and `Loses a record or crashes` both `no`, and `Pass` unchecked over the two open ⬜ rows. Its chain-check exit 1 comes only from other work items' targets that the clone cannot reach |
| the broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, and this round ran none of it |

```python
def truth(src_lines, k):
    prev = src_lines[k - 1]
    if prev[-1:].isascii() and prev[-1:].isalpha():
        mark = "QzqMARKqzQ"
    elif prev and all(c.isspace() and c not in " \t" for c in prev) \
            and not set(prev) & {"\x0c", "\x85", "\u2028"}:
        mark = "\u2002\u2003\u2002"
    else:
        return None
    marked = list(src_lines)
    marked[k - 1] = prev + mark
    return any(t.type == "html_inline" and mark in t.content
               for t in all_tokens(P.parse("\n".join(marked))))
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
