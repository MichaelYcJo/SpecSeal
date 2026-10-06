# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | ba4957f9 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The reading narrows to a path, the reframe after round 3. A finding lands only
through a `.py` path its own `Location` carries — `path:line`, `path#unit`,
`path::unit` — so the `landings` filter becomes unconditional, and
`names_a_file`, `range_carriers`, `CELL_WORD_RE` and `PATH_TAIL_RE` leave the
tree. The bare-name cases give way to S5, parametrized over every shape the
three rounds met, and S5b, each red shape shown red against `6ceb7d46`'s
`round_record.py`. The docs the plan names carry the narrower reading. No
reading of prose comes back.

## What this phase found

**§15, red at `6ceb7d46`.** `round_record.py` is byte-identical between
`6ceb7d46` and the phase's base (`git diff --stat 6ceb7d46 HEAD` printed
nothing for the code and the docs), so S5 and S5b were written first and run
against the tree as it stood: `bin/test tests/test_a_fix_of_a_fix_is_counted.py
-q -k "lands_in_no_written_unit or carrying_its_py_path or carries_its_path"`,
exit 1, 7 failed and 20 passed. The seven are the alone shapes (`` `u` ``,
`` `u()` ``, `` `w` ``) and round 3's four (`` `SKILL.md` `` held twice,
`` `gone.md` `` not held, `"bin/tool"` quoted, `bin/tool's` before an
apostrophe), each reading `first` there. The other S5 shapes already read `no`
under round 2's reading and stay as pins; S5b's five read `first` before and
after. After the change, the module's 418-case slice passes, and a mutation
that lands a path-less name on any unit of that name turns S5 red.

**Removed, by name.** From `round_record.py`: `names_a_file`,
`range_carriers`, `CELL_WORD_RE`, `PATH_TAIL_RE`, and the bare-name arm of
`landings`. From the test module: `TRACKED_FILES`,
`test_a_bare_name_two_files_of_the_range_carry_does_not_land`,
`test_a_bare_name_a_touched_file_carries_unchanged_does_not_land`,
`test_a_name_beside_a_tracked_file_of_any_kind_does_not_land`,
`test_a_name_beside_a_tracked_py_file_lands_only_through_it`, and
`test_every_location_shape_the_depth_walk_reads_lands`, which became
`test_every_location_shape_that_carries_its_path_lands` without its two
path-less parameters.

**Added.** No unit in `round_record.py`; a comment above `fof_count_of` names
the five removed readings, because the run's round records cite them and
`evidence-check`'s record walk refuses a name the tree no longer carries. In
the test module: `NAMED_FILES`, `with_named_files`, S5's case
(`test_a_location_that_lands_in_no_written_unit_reads_no`, now 22 shapes) and
S5b's (`test_a_location_carrying_its_py_path_still_lands`, 5 shapes).

**`location_units` is unchanged**, as the spec says: the depth walk in `close`
still reads a bare name there, and nothing the rounds found was in it.

**`tests/test_no_passage_is_pasted_into_a_second_file.py` caught one copy.**
The owner's disclosure paragraph and the spec section first shared the same
list of what lands nowhere; the owner now says it in its own words.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `names_a_file`, `range_carriers`, `CELL_WORD_RE`, `PATH_TAIL_RE` and the bare-name arm of `landings` | none — the reading they made is out of scope by the reframe (`spec.md` §Out, §*What round 3 moved*); their names stand in the comment above `fof_count_of` |
| the four bare-name cases and `TRACKED_FILES` | `tests/test_a_fix_of_a_fix_is_counted.py`'s S5 case, whose parameters carry every shape they pinned, now expecting `no` |
| the tracked-file and carrier sentence in `docs/round-record-spec.md`, the owner's disclosure and `agents/warden.md` | the same three places, stating the path-only reading |
