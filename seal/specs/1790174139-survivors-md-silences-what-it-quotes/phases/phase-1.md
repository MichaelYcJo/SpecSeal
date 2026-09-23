# 1790174139-survivors-md-silences-what-it-quotes — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | af5c4044 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Take the exemption file out of the sweep on both sides — the range's path
list (#507) and the pool (#308) — with one predicate the two call sites
already apply, keeping `records_a_past_round` untouched (Q4's default), and
give the docstring's §*What is excluded* a paragraph naming both sides.
Cases S1, S2, S3, S4, S9 (first extension) and S10, each seen red at
`531cc723` first. Delete the `seal/follow-up.md` row that was waiting on the
range half. Re-run the frame's S5 table over the three pull-request ranges
`spec.md` §*The measured state* names — with `--exempt`, without, and with the file deleted at
the tip in a scratch clone — and write it here beside the baseline, together
with Q2 (rows consulted against rows written) and Q3 (survivors that vanish
through a live file the range wrote).

## What this phase found

**The frame holds.** Every coordinate it named was opened: the two call
sites, the test constants, `OWNER_DIR`'s tail, the ledger anchors, the
follow-up row. The baseline it reported (7 / 0 / 0 `exempt` lines) was
re-executed before the first edit and reproduced exactly. One instrument in
`questions.md` did not hold as written, under Q3 below.

**Q4 — the predicate.** `records_a_past_state(path)`, one function for the
class, which calls `records_a_past_round` and adds the exemption file: true
where the path's segments after `specs/<id>/` are exactly `survivors.md`. The
anchored function is untouched. The reach is the existing predicate's: a
`docs/specs/<name>/survivors.md` matches it the way a
`docs/specs/<name>/rounds/` file matches `records_a_past_round`, which the
round-record exclusion has carried since it shipped and this phase does not
widen or narrow.

**Seen red, executed at `531cc723` with the unedited module**, six cases in
one run (`6 failed, 2 passed, 56 deselected`; the two passes are the
pre-existing empty-file refusals `-k` also matched):

- S1 `test_an_exemption_file_the_range_added_does_not_subtract_the_survivor_it_quotes`
  — `guide.md still carries the wording this range removed from notes.md,
  and the exemption file quoting that wording is what silenced it -- the
  row's quote counted as wording the fix wrote; exit 0`.
- S2 `test_an_exemption_file_in_the_pool_does_not_dilute_the_survivor_it_quotes`
  — `the exemption file sitting in the pool diluted the phrases it quotes
  under the floor; exit 0`.
- S3 `test_the_report_is_the_same_with_the_exemption_file_and_with_it_deleted`
  — `assert (0, ['  no re...ll standing']) == (1, ['', 'gui...s”', '', ...])`:
  the tip with the file reported nothing, the tip without it reported
  `guide.md`.
- S4 `test_an_exemption_file_the_range_edited_does_not_become_a_source` —
  `the check read that edit as a correction somebody has to chase into
  guide.md; exit 1`.
- S9 `test_the_docstring_names_both_sides_of_the_round_record_exclusion` —
  `**The work item's own exemption file.** is no longer an exclusion stated`.
- S10 `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
  — ``corrected derives a path list and no longer applies
  `records_a_past_state` ``.

After the edit: `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q`
→ `64 passed` (60 at `531cc723`), exit 0 read directly; `uvx ruff check` and
`uvx ruff format --check` on the two files, both exit 0.

**S5 — the three pull-request ranges, executed twice**, at `531cc723` before
the edit and at `af5c4044` after it. The probe column is a scratch clone
(`git clone --shared`, driven from Python) in which the exemption file is
deleted at the tip in one further commit, read over `<a>..<probe tip>`; the
clone is removed before the script returns.

| Pull request | Range, sentences removed | Rows | with `--exempt`, before → after | without, before → after | file deleted at the tip, without | file deleted, with |
|---|---|---|---|---|---|---|
| #525, `1790138190-…` | `f8f1c9d..edd022a`, 162 | 29 | exit 0, **7** exempt → exit 0, **14** exempt | exit 1, 7 standing → exit 1, **14** standing | exit 1, 15 standing → exit 1, **14** standing | 15 exempt → **14** exempt |
| #528, `1790154759-…` | `c626382..24ea206`, 5 | 4 | exit 0, 0 → 0 | exit 0, 0 → 0 | 0 → 0 | 0 → 0 |
| #527, `1790154761-…` | `edd022a..c626382`, 8 | 3 | exit 0, 0 → 0 | exit 0, 0 → 0 | 0 → 0 | 0 → 0 |

Every `exempt` line after the edit carries the grounds of a row in that
file (counted by the script against the rows' grounds cells); the count
without `--exempt` equals the count of `exempt` lines with it; and the probe
that deletes the file at the tip changes neither count. Those are S5's three
conditions, and each holds at `af5c4044` and fails at `531cc723` on #525.

**Why the deleted-file probe reads 15 before and 14 after.** The old probe's
fifteenth candidate was `seal/specs/1790119502-…/survivors.md:7` — the
previous fold's own range row, standing in the pool as prose and scoring 1.81
against `skills/settle/SKILL.md`. Under the fix every work item's
`survivors.md` is out of the pool, so that candidate is not produced, and
#525's eleventh row, which excused exactly it, matches nothing. So the
round-1 report's 15 is 14 consulted plus one row whose subject the fix
removed from the search. Measured with the `531cc723` module copied beside
the fixed one as a `test_tmp_*` probe, run once over the same probe clone,
deleted.

**Q2 — rows consulted against rows written**, at `af5c4044`: #525 **14 of
29**, #528 **0 of 4**, #527 **0 of 3**; 14 consulted, 22 dead. A dead row
silences nothing by design and none was edited. #528's and #527's rows are
dead in every state — with the file, without it, and with it deleted — and
at `--floor 1.0` those two ranges still report nothing, so the places their
rows quote do not reach even a one-run score over the squash commit's range.
The frame reported, from #528's round-2 report, that its four rows printed
under `exempt` at a tip without the file; that reading was taken over the
branch's own range at the time and does not reproduce over the squash range,
which is the range this table measures. Nothing in the fix turns on it.

**Q3 — survivors that vanish through a live file the range wrote.** The
instrument `questions.md` names — blank the quoting sentences in a probe
commit and compare — puts the blanking inside the range, so the blanked
sentences become removed wording and the comparison measures a different
range. Measured in-process instead: the module's predicate was widened, for
one run, to also exclude the `overview.md`, `changelog.md` and ledger
fragment the range wrote, on both sides, and the candidate set compared with
the shipped one. #525: **5** places appear only then —
`docs/review-chain-spec.md:392` (2.93), `tests/test_the_last_rounds_fixes_are_checked.py:8`
(2.75), `skills/code-review/SKILL.md:210` (1.85), `docs/review-chain-spec.md:845`
(1.76), `skills/code-review/orchestration.md:263` (1.64). #528 and #527:
none. That is the class `spec.md` §*Out* leaves out on purpose — those files
are live statements — and the count goes to `overview.md` §*Not done* with
the repository owner named.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `seal/follow-up.md` row opening *Writing a `survivors.md` row silences its survivor a SECOND way, and that way does not rot* — the range half waiting on this work, and its question to a person, *whether that exclusion is right* | `spec.md` §*Judgments the tree answered*, 2, answers the question; `changelog.md` of this work item and this record carry the discharge |
| `corrected` and `corpus` calling `records_a_past_round` directly | Both call `records_a_past_state`, which calls it; the function itself stands, and ledger row S6 of `1788873640` still anchors on it |
