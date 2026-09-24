# 1790260566-a-row-inside-a-fence-reads-as-live — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4f9b137b |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

One fence-delimiter rule, bounded (#491). Add CommonMark 4.5's delimiter
rule to `unverified_check.py`, and make `blank_fences`, `_liveness` and
`_paragraph_ends_at` use it. Give `_paragraph_ends_at`'s ATX branch the
three-space bound. Rewrite the comments above `FENCE_RE` and the
"`blank_fences` knows / keeps" sentences in `settle.py#coordinates` and
`live_lines`. Add the agreement case against `hooks/config.py#fence_map`
(S6). Cases S4, S5 and S6 seen red against `c52e8350`, a four-space `# x`
case on `_paragraph_ends_at` seen red, and Q2's measurement recorded here
with every moved line judged.

## What this phase found

**The frame holds.** Every coordinate `plan.md` §*Technical context* names
for this phase was opened and reads as it says. `c52e8350` and the base
`d3814875` hold the same reader, because the two frame commits touch only
this directory.

**The rule is two functions and a walk.** `fence_opener(line)` returns
`(character, length)` or None, and `fence_closes(line, opener)` answers the
closer's half. `FENCE_RE` keeps its name and gains the `run` and `info`
groups, so the ledger row anchored on it drifts rather than breaks.
`fence_spans(lines)` returns `[(first, last)]` with `last` None for a block
that never closes. `blank_fences` blanks the spans, an unclosed one to the
end as before. `closed_fence_lines` is the set phases 2 and 3 skip: only a
fence that closes. `_liveness` asks the two functions directly, because its
comment and span state decide whether a line can open a fence at all.

**The oracle had to learn the same two clauses.**
`tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules`
said it was written from the format, but its fence rule had neither
info-string clause. With the reader corrected and the oracle not, the
safety fuzz can report the corrected reader unsafe: the reader keeps a block
open past ```` ```text ```` while the oracle closes it and reopens on the
next run. The oracle's `fence_of` now returns the run and what follows it,
`opens` and `closes` apply the two clauses, and `block_ends_at`'s fence stop
asks `opens`. The fuzz is green over its 2,000 documents (executed).

**Cases seen red (executed).** Each new case was run against `c52e8350`'s
reader loaded from a saved copy, in a probe that was deleted afterwards:

| Case | Against `c52e8350` |
|---|---|
| S4 `test_an_indented_delimiter_is_not_a_fence_for_the_gates_reader` | red: `readable` blanked the table below `    ```` |
| S5 `test_each_reader_asks_the_one_delimiter_rule`, the ```` ```python ```` shape | red in both readers: the block closed there, and the last ```` ``` ```` opened a block that swallowed `after` |
| S5, the ```` ```x` ```` shape | red in both readers: it opened a block |
| S5, the ```` ~~~ `x` ```` shape | green in both, the control: a tilde opener's info string is unrestricted |
| S6 `test_the_fence_rule_agrees_with_the_config_reader` | red on shapes 3, 4, 6, 12 and 13 of 19 |
| `test_an_atx_heading_ends_a_paragraph_only_within_three_spaces` | red on the four-space line |

**Q2, measured (executed).** One script compared `c52e8350`'s `readable`
and `live_lines` with this tree's over `git ls-files '*.md'`, 124 files.
`live_lines` moved no line. `readable` moved 10 lines in 3 files, all
toward being read:

| File | Lines | What they are |
|---|---|---|
| `docs/release-checklist.md` | 364–367 | a ```` ```bash ```` block indented six spaces inside a list item |
| `skills/evidence-ci/SKILL.md` | 55–57 | a ```` ```yaml ```` block indented five spaces inside a list item |
| `skills/implement/orchestration.md` | 102–104 | a ```` ```bash ```` block indented five spaces inside a list item |

Each line is judged wrong by the format. A list item moves the indentation a
fence is measured from, and the reader has no block model, so these fenced
blocks now read as text. Q2's default says a wrong line reverts the sub-rule
that moved it. That sub-rule is the three-space bound, which is #491 itself,
so it is kept. Reverting it would bring back the silent direction, where a
four-space run in prose hides every row below it. The new error is loud,
because rows are read rather than hidden. No gate that reads through
`readable` reads these three files. `overview.md` records the divergence.

**The ledger moved, and each row was re-read (executed).**
`evidence_check.py --strict .` before the phase: 2054 ok. After the code
edit: 2047 ok and 7 drifted, all rows whose anchored unit this phase edited.
`seal/releases/0.13.0.md` S3, R6, R11, R12, R14 and R15, and
`seal/releases/0.15.1.md` R4. Each claim still holds. Each row got a dated
`Re-read` note saying what changed, and `--reverify` re-stamped it. Then
the phase's four rows went into the fragment: 2067 ok, 0 drifted.

**The records arm then read this work item, and refused its own frame.**
Once `seal/ledger/1790260566-….md` existed, the arm read this directory:
`NOT-IN-TREE` for the name S11 quotes on `spec.md`'s S11 line, and `BROKEN` for the
quoted `nosuchfile.py` stamp on its S1 line, exit 2. Both lines quote the
shapes the cases build. Each got ` · NAME NOT IN TREE`, the remedy
`skills/evidence-check/SKILL.md` names, and nothing else in `spec.md`
changed. After: `1 work item read · 85 names read · 0 stamps read · 0
refused`, exit 0. This is phase 4's Q5 baseline.

**Modules run (executed).** Every test module that reads a file this phase
edited, found by grep for the real-tree paths of the edited files and for
modules that load the edited scripts. That is 57 modules:
`bin/test <57 modules> -q`, exit 0, 2606 passed and 8 skipped in 112.86 s.
`uvx ruff check` and `uvx ruff format --check` over the three edited Python
files, both clean. The full suite was not run, which is the sealer's act.

**What `CONTRIBUTING.md` §*What a change to a gate must carry* asks:**

- **The case seen red:** the table above. Each case was run against
  `c52e8350`'s reader from a saved copy.
- **Failure direction:** `readable` blanks fewer lines, so `check_text`,
  `chain_check.py` and `round_record.py` read more. A misread there is a
  refusal a person sees, which is the cheaper mistake. `live_lines` extends a
  fence where a closer carries an info string, so fewer lines are live. That
  is the safe direction for the fold and for `settle`, which keep a
  directory. `live_lines` stops opening a fence on a backtick opener holding
  a backtick, so more lines are live. Q2 measured no such line in this tree.
- **Prompt budget:** 0. Nothing here asks anybody anything.
- **Platform note:** pure text processing, with no process or filesystem
  inspection. Run on macOS only, and CI runs the Linux leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `blank_fences`' own fence pattern, `^\s*(`{3,}\|~{3,})` | `unverified_check.py#fence_opener` and `#fence_closes` |
| `_liveness`' two inline `FENCE_RE` comparisons | the same two functions |
