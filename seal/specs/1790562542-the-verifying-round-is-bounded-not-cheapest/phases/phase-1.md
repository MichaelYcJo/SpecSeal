# 1790562542-the-verifying-round-is-bounded-not-cheapest — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 32b5886f |
| Ran by | unknown — the spawn prompt named no agent or model for this row, and the value is the spawning session's to give |

## What this phase was asked

Edit C1–C5 per spec *In* 1–5, replace C6's needle with C1's new text, and
add `tests/test_the_verifying_round_is_bounded_not_cheapest.py` (a carriers
table for C1–C4, a stands case, a gone case, and the tree-wide `cheapest
round of the run` case), with the changelog fragment in the same commit.
Take a baseline `evidence-check .` before the first edit.

The spawn also handed over one claim from outside the frame: three files
say #81's round 1 (7.6 m / 29 calls) was the "cheapest round on record",
while #51's baseline shows #29's verifying round at 4.2 m / 10 calls.
Establish whether that is true by opening #81 and #51's baseline and when
each was written. If it is false or unsupported, correct it here with its
pin updated and seen red first. If it cannot be settled, leave the text and
record it in `overview.md`. Do not rewrite released `CHANGELOG.md` sections.
Keep the `skills/code-review/orchestration.md` edit to C1's row, because
item D (#400) edits the same file.

## What this phase found

**The baseline was clean.** `evidence-check .` before the first edit exited
0 with 2513 ok, 0 drifted and 0 broken, so a `--reverify` in phase 2 moves
only rows this branch drifted.

**The #81 sentence is false, and was false when it was written.** Every
item below was read through `gh`, and none of it is re-derived:

- The sentence entered the tree at `5107e30c`, 2026-09-04 00:30 +0900
  (2026-09-03T15:30Z). The source it copies is #119's body, which quotes
  #89.
- The current #81 is the `seal export`/`seal import` feature. "#81's
  round 1" means round 1 of that work item's review, and #81 carries no
  measurement.
- #89's comment of 2026-09-03T02:26Z gives "Span 7.6 m, 29 tool calls — the
  cheapest review round in this log".
- #89 already held cheaper rounds before that. Its comment of
  2026-09-02T11:50Z records #79's warden round 2 (verifying) at 5.6 m and
  28 calls, which is cheaper on both axes. Its body table rows 5–6 (#78's
  verifying rounds, 7.8 m / 13 and 7.0 m / 10) were added at
  2026-09-03T12:05Z, three hours before the sentence. Row 4 (#78 round 1,
  6.4 m / 32) went in at the same time.
- #51's first revision, 2026-09-01T01:49Z (read from `userContentEdits`,
  whose `diff` field holds each revision's full body), already carries
  `| verifying round (warden) | 1.5 | 4.2 m | 10 |`.
- Narrowed to finding rounds, the claim still fails. By span, #78 round 1
  (6.4 m) is shorter. By calls, #79 round 1 (23) has fewer.

What #89 did measure and support is the yield: "29 calls found five
defects; #82's six rounds averaged three times the calls for fewer." That
is the wording `skills/code-review/SKILL.md` and `templates/sdd-round.md`
now carry. The pin moved in `tests/test_a_segments_record_says_what_it_was_asked.py`:
the probe `cheapest round` became `five defects`, and a gone/stands pair
was added for both carriers. That module already owns #81's story, so the
new verifying-round module stays about one claim.

**The class sweep found no fifth verifying-round carrier.** After the
edits, `grep -rn "cheapest round of the run" agents skills docs templates
README.md README.ko.md` exits 1. `git grep -i "cheapest round"` outside
`CHANGELOG.md` and this work item finds it in the two test modules alone.
Those hits are the gone halves, the tree-wide case's needle, and two
docstrings that say the claim was retracted.

**The verifying bar gained a check the plan did not list.**
`test_the_verifying_bar_is_grounded_on_neither_cost_nor_size` reads the
one `| verifying | exempt |` line and refuses `cheap`, `small`, `by design`
or `afford` in its Grounds cell. This is spec *In* 2's "no cheapest, no
small, no by design" as an executed check rather than a reading.

**Two things met while building:**

- The C3 stands phrase first carried `×`, which ruff's RUF001 refuses. The
  phrase is now `29 verifying rounds ran at a median of 0.83`, and it was
  shown red again after the change.
- zsh does not word-split `$F`, so the first lint call checked one
  nonexistent path. The call was re-run with the paths inline.

**Red first (§15), executed.** A scratchpad script (not in the tree)
applied each mutation, asserted its pattern matched, ran only the named
cases with `-p no:xdist -p no:cacheprovider`, restored from bytes held in
memory, and cleared `tests/__pycache__`. It then compared a hash of every
touched file with the pre-run state: byte-identical. All 25 expected-red
cases exited 1:

| Mutation | Red cases |
|---|---|
| C1 old Target cell restored | the gone case, C6's `test_the_verifying_rounds_target_is_the_previous_rounds_fixes`, the tree-wide case |
| C1 stands phrase deleted | the stands case, C6 |
| C2 old Grounds cell restored | the gone case, the bar-grounds case, the tree-wide case |
| C2 `#51 observation 1` clause deleted | the stands case |
| C2 `small` reinserted alone | the bar-grounds case |
| C3 old cost paragraph restored | the gone case, the tree-wide case |
| C3 median sentence deleted (re-run after the RUF001 change) | the stands case |
| C4 affordability sentence restored | the gone case |
| C4 job sentence deleted | the stands case |
| phrase planted in `README.md`, then in `templates/sdd-phase.md` | the tree-wide case, each time |
| #81: `SKILL.md` old sentence restored | both #81 cases |
| #81: template old comment restored | both #81 cases, `test_the_round_sections_comment_names_81_and_the_measured_numbers` |
| #81: `SKILL.md` yield phrase deleted | the #81 stands case |
| #81: template `five defects` deleted | the #81 stands case, the `names_81` case |

**Narrow runs, executed, exit read directly:**

- `bin/test tests/test_the_verifying_round_is_bounded_not_cheapest.py tests/test_the_last_rounds_fixes_are_checked.py tests/test_the_handoff_before_round_one.py tests/test_a_segments_record_says_what_it_was_asked.py -q` exits 0.
- `bin/test tests/test_a_rider_reaches_its_file.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_one_word_one_meaning.py tests/test_the_broad_gate_cell_keeps_every_run.py -q` exits 0.
- `bin/test tests/test_the_changelog_is_gathered_at_release.py tests/test_release_hygiene.py -q` exits 0.
- `uvx ruff check` and `uvx ruff format --check` on the three changed test files exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the claim that the verifying round is the cheapest round of the run (C1–C3), and that its surface makes it affordable (C4, C5) | `docs/review-chain-spec.md` §*The last round verifies* now holds the measured cost with its sources. #51's body holds the durable log, corrected by the orchestrating session under #636 |
| the size clause of the protocol's verifying row, "a segment that small is the nuance below in its every case" | none. #456's 46–58-call verifying rounds make it false, and the nuance paragraph below the table stands on its own |
| "#81's round 1 was the cheapest round on record/measured" (`skills/code-review/SKILL.md`, `templates/sdd-round.md`, the test docstring) | none. It was false. What stands is the yield #89 measured. `CHANGELOG.md`'s released 0.7.0 entry keeps the old sentence as a record |
