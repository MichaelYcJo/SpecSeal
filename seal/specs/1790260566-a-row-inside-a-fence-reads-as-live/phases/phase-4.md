# 1790260566-a-row-inside-a-fence-reads-as-live — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | e78ccea9 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

A closer is a position (#220), and the fence rule in the records arm.
`claim_lines` re-reads the remainder after `-->` by the line's own rules, so
a reopened comment reopens and a claim after the closer is read. Its fence
recognition uses phase 1's rule: the bound, the character, the length, and a
closer with no info string. Under that rule #220's fence half ("a name after
a closing fence on the fence's own line") is not a closer at all, and the
phase records that. The text returned is what lies outside the regions, and
`NOT_IN_TREE` is still tested on the raw line. `skills/evidence-check/SKILL.md`
§*What counts as a claim* is narrowed per Q1's default (a), with no
positional scanner. The records-arm aside row leaves `seal/follow-up.md`.
Cases S10, S11 and S12, each seen red. The existing
`tests/test_a_record_states_what_the_tree_has.py` stays green. Q5: the
records arm's `names read` count over this tree before and after, with any
new refusal judged.

## What this phase found

**The frame holds.** `claim_lines` reads as the plan describes, and its two
callers, `stated_names` and `stated_stamps`, take `(number, text)` and need
no change.

**The rule as built.** When an aside is open, a line with no `-->` is held
as before. A line with one closes the aside, and what follows the closer is
read. When no aside is open, a fence opener asks `fence_rule()`, the shared
delimiter pair or phase 2's vendored pair. Then, while what is left of the
line begins with `<!--`, the comment is consumed to its `-->`. A comment
with no closer opens the aside, and the rest of that line is dropped. What
remains is returned as the line's text, unless the raw line carries
`NAME NOT IN TREE` or nothing remains. `held` and `aside_held` work as they
did.

**One more shape moved with the rule, and it is the same rule.** A comment
that begins a line and closes on it used to drop the whole line. Now
anything after its `-->` is read. `test_a_claim_after_a_one_line_comment_is_read`
pins it.

**#220's fence half is not a closer (read).** Under CommonMark 4.5 a
closing fence carries nothing after its run, so a line like
```` ``` `name` ```` inside an open block is fence content, and the block
stays open. The name on it is not a claim, and neither is anything up to the
real closer. That answers the ticket's fence half without positional
reading. No case was written for it, because the spec asked for none and
S12 exercises the same closer rule.

**Cases seen red (executed).** The body of `claim_lines` was swapped for
`c52e8350`'s and the module was run. The file was then restored from a
saved copy of this tree, compared with `cmp`, and `tests/__pycache__` was
cleared:

| Case | Against `c52e8350` |
|---|---|
| S10 `test_a_claim_after_a_closing_delimiter_is_read` | red: no name read |
| S11 `test_a_comment_reopened_on_its_closing_line_is_an_aside_again` | red: the reopened comment's name was read as prose |
| `test_a_claim_after_a_one_line_comment_is_read` | red: the whole line was dropped |
| S12 `test_a_shorter_fence_does_not_close_a_longer_one` | red: ```` ```markdown ```` closed the ```` ```` ```` block |
| `test_a_mid_line_comment_is_read_with_its_text` | green on both, as a pin of Q1's default should be |

Every earlier case in the module stays green: 66 passed.

**Q5 (executed).** On this tree the records arm reads one work item, 158
names, 0 stamps and 0 refused, before the change and after it. Over the 130
tracked `.md` files, old and new `stated_names` and `stated_stamps` agree
line for line: 1,762 names each. **Over every record file this repository's
history holds, 1,711 of them**, one file reads differently.
`seal/specs/1789721571-…/rounds/round-2-report.md`, as it stood before its
retirement, has a ```` ```` ```` block at lines 139–154 quoting two
```` ``` ```` blocks. Under the old three-character mark, line 144 closed the
outer block, and every later fence in the file flipped between open and
closed. The new reading follows the format. It reads 45 names in prose the
flip had hidden (lines 165–479), and it drops one name at line 382, which
is inside a ```` ```python ```` block (379–431). That work item has shipped,
so the arm no longer reads its records, and no verdict moves today.

**The class had two more readers of the old sentence.** Two rows anchored on
`claim_lines` drifted. `seal/releases/0.15.0.md` A4 holds, and got a
`Re-read` note. `seal/releases/0.9.0.md` R5 said "an HTML comment … to its
`-->`, a fence to a close carrying the marker that opened it". That was
false before this phase for a mid-line comment, which is why the follow-up
row existed, and false after it for the fence close. It was **corrected in
place** with a `Corrected 2026-09-25` note. The two phase-4 rows went into
the fragment. `evidence-check --strict .`: `2097 ok · 0 drifted`, exit 0.
The docstring of `fence_opener` gained `claim_lines` in its list of readers.
That drifted this work item's own P1-1, which was re-stamped.

**The branch's survivors (executed).** `bin/survivor-check --range
d3814875..HEAD` reported 18 places, exit 1. Every one is correct where it
stands:

- five carry the open-rows rule, which now has one home in
  `unverified_check.py`;
- nine share phrases with the two `seal/follow-up.md` rows this branch
  removed because it answered them;
- the rest are the frame's own `spec.md`, which records the question, and
  released rows that still hold.

Each is in `survivors.md` with a quote from the standing text and its
grounds. Two quotes first failed to match, because `\n` in a code span
normalises to the word `n`. After those two were fixed: exit 0, "every
survivor is excused by a row above (18)". `bin/correction-check --range
d3814875..HEAD`: no merge commit in the range, exit 0.

**Modules run (executed).** The 87 modules of phase 3, which include
`tests/test_a_record_states_what_the_tree_has.py` and every module naming
the checker or its skill: `3595 passed, 8 skipped`, exit 0. The ledger check
beside that run printed exit 2 for the one self-drift above, and it was
re-stamped before the commit. `uvx ruff check` and `format --check` over
the three edited Python files are clean.

**What `CONTRIBUTING.md` §*What a change to a gate must carry* asks:**

- **The case seen red:** the table above.
- **Failure direction:** a claim after a closer is now read, which refuses
  more at exit 2. That is loud, and a person answers it with the marker. A
  comment reopened on its closing line, or a shorter run inside a longer
  block, now reads less. That follows the documented rule, and Q5 found one
  historical file where it applies. A comment opening mid-line was read
  before and is still read (Q1's default), and the skill now says so.
- **Prompt budget:** 0.
- **Platform note:** pure text processing. CI's test matrix runs Linux,
  macOS and Windows. This phase ran on macOS only.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/follow-up.md`'s records-arm aside row | this phase: the skill's sentence is narrowed to the code, Q1's default. `questions.md` Q1 holds the alternative for a person |
| `claim_lines`' own three-character fence marks | `fence_rule()`, the shared delimiter rule |
