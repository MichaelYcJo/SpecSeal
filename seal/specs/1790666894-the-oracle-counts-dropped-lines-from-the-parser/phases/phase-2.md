# 1790666894-the-oracle-counts-dropped-lines-from-the-parser — phase 2

<!-- seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 128dda72 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md`'s phase 2 row: the class enumerated (§12). S3's sixteen rows go in
`test_the_oracle_counts_the_lines_the_parsers_strip_dropped`, phase 1's case,
and S4 is a case of its own over every character the strip drops, computed
rather than listed, each character in two shapes (at the top level and behind
a list marker). `changelog.md` is written. The fragment's P1-1 gains the S3
and S4 anchors, and whatever this phase drifted is re-read. Every S3 row and
every S4 shape is seen red with the count forced to 0; which S3 rows are also
red with the oracle from `cd56113c` is recorded here (Q2). S4 runs on a Python
other than the 3.13.9 `bin/test` builds, since CI runs 3.12 and the spec
measured its set on 3.14.

The phase ran in two spawns. The first wrote and committed the code at
`128dda72` and saw every case red. The second, which writes this record,
re-ran the module at that commit, re-ran S4 on 3.12 and 3.14 and the S1–S4
rows against the base oracle, and wrote the records.

## What this phase found

**The runs.** The first spawn's are its own and are in the fragment's P1-1
`Re-read` note; the ones below were executed by the second spawn, at
`128dda72`, with nothing edited in the tree.

| Run | Result |
|---|---|
| `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py -q` (Python 3.13.9) | exit 0, 129 passed |
| S4 and the guard case, `uv run --isolated --python 3.12` with `markdown-it-py==4.2.0` | exit 0, 18 passed on 3.12.11 (17 characters and the guard) |
| The same, `--python 3.14` | exit 0, 18 passed on 3.14.3 |
| S1 to S4 and the guard against `git show cd56113c:tests/commonmark_oracle.py`, in a scratch copy of the tree | 5 failed, 37 passed: the five S1 rows alone |
| The same scratch copy with the oracle at `128dda72` | 42 passed |

The first spawn recorded 3.12.12 and 3.14.4; the uv here had 3.12.11 and
3.14.3. Both pairs give 17 characters, so the set is the same across the four
3.12 and 3.14 patch releases measured, and 3.13.9 agrees. On 3.13.9 the 17
are the spec's list for 3.14: U+001F, U+00A0, U+1680, U+2000 to U+200A,
U+202F, U+205F and U+3000.

**Q1, S3 and S4: markdown-it-py gives CommonMark's answer on every row.** All
sixteen S3 rows and all 34 S4 shapes hide what the spec wrote, so no row pins a
departure. With phase 1's eight, the parser agrees on every row of S1 to S4.

**Q2: only S1's five rows are red at the base oracle.** The sixteen S3 rows,
the three S2 rows and every S4 shape are green there, so the hand-written
helper already had every shape the class names except the `>` it misread; the
instances of the defect were S1's five. §15 for S3 and S4 is met by the
count-forced-to-0 run instead, as the spec's table says.

**A third case the spec does not name**, `test_the_strips_set_is_the_one_measured`.
The S4 case is parametrized over a computed list, and pytest skips a
parametrized case whose list is empty rather than failing it (the first spawn
executed this: exit 0, 1 skipped). So a mistake in the set's condition that
empties it, or turns it into a space and a tab, would leave S4 silent. The
guard pins the floor: five characters the set must hold on every Python the
suite runs, and neither a space nor a tab. `overview.md` carries the
divergence row.

**What the next reader needs.** The S4 set's condition excludes the eight
break characters `str.splitlines` makes and CommonMark does not; without that
condition the S4 case is red on those eight (the first spawn executed this),
because `hidden_text`'s reader-split mapping, F's work, is what handles them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase added rows and cases and removed nothing | none |
