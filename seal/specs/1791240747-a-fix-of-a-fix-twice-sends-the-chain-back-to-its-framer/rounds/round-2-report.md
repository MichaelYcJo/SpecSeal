# Round 2 report — 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer

| Field | Value |
|---|---|
| Target SHA | c705cd6d35c5e05c56cbb40e6ae0929ad6066665 |
| Base | `origin/release/v0.19.0` |
| Pull request | #828 (draft) |
| Round kind | verifying round — round 1's fix range `e66d04c0..16fbe326`, and the units its `New units` row names |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Every verdict round 1 closed is closed. The four fixed findings each have a
case, and all eleven new cases fail against the scripts as they stood at
`e66d04c0` (executed). The gate's `runs_of` and the generator's
`current_run` cut a run at the same record over all 5,460 chains of up to six
records (executed). The depth walk restarts at a stop. `frame`'s sentence says
what a foot may end on. The ledger fragment's anchors all hold.

What the fix pass wrote is still incomplete in two places. Both sit in
`landings`, and both are the class round 1's yellow 1 named: a finding lands
in a Python unit it is not about.

1. **A bare name still lands when two files of the range carry it** (🟡 1).
   The check counts only the files whose copy of the name the fixes changed.
   It does not count a file the range touched that carries the name
   unchanged. `docs/round-record-spec.md` and ledger row A1 promise more than
   that.
2. **A cell naming a file outside `NAMES_A_FILE_RE`'s extension list still
   lands its backticked name in another file** (🟡 2). That covers a `bin/`
   wrapper, a `.cmd` file, a `Makefile` and an `.html` file. This repository
   tracks 18 files with no extension and 17 `.cmd` files.

Two corrections follow, and neither needs a fix:

- The refusal over an unresolvable range is described as firing "where an
  open row could land". It fires whenever any row is open, including one
  located in a document that can never land (⬜ 3).
- `overview.md` and `questions.md` Q4 record the stop rate as settled by round
  1's reviewer. Round 1's report said that question stays with the owner
  (⬜ 4, a records correction).

**This round's own `Fix of a fix` row will read `first`.** Both yellows are
located in `landings`, which round 1's range changed. That is the rule working
on its own work item, not a fault in it. A third landing in this run would read
`second`.

## Round 1's verdicts, opened

| Round 1 | Claimed | What the code does now | Label |
|---|---|---|---|
| yellow 1 | a document `Location` lands nowhere, and a name beside a `.py` path lands only through that path | `landings` drops every unit with no file when `NAMES_A_FILE_RE` matches the cell (`round_record.py:2426`). A `.md`, `.rst` or `.txt` cell and a `.py` cell beside an untouched file each read `no` | executed — the three new parameters red at `e66d04c0`, green at the target. The class goes further than this fix reaches: 🟡 1 and 🟡 2 |
| white 2 | the gate refuses a landing on a run's first record and a `second` with no landing before it, and an orphan `second` cuts no run in either reader | `fix_of_a_fix` carries both refusals (`chain_check.py:3948`). `runs_of` and `current_run` cut only after a `second` whose run already landed | executed — the three gate cases and the generator's orphan case are red at `e66d04c0`. The two cuts agree over every chain of `None`, 0, 1 and 2 up to six records long |
| white 3 | `landings` reads no range when no row is open | the open rows are collected first, and an empty list returns before `round-K.md` is read (`round_record.py:2394`) | executed — the foreign-range case is red at `e66d04c0`. The wording around it overstates the narrowing: ⬜ 3 |
| white 4 | `frame`'s refusal names what a foot may end on | the sentence names `Reframed … after round <N>.` lines as what may stand under the mark, and the case pins it (§14) | executed — the pin is red at `e66d04c0` |
| white 5 | the 23 records resolve with the pull request heads fetched | `overview.md:28` and Q1 carry 119 of 122 and the five work items, as round 1's report gave them | read. Its neighbour row is ⬜ 4 |
| ❓ depth | the orchestrator decided the depth walk resets at a stop (Q5) | `close` hands the depth walk `current_run(...)[0]` (`round_record.py#close`) | executed — `test_the_depth_restarts_at_a_stop` is red at `e66d04c0` |

## 🟡 1 — A bare name lands when a second file of the range carries it unchanged

**Where.** `skills/code-review/scripts/round_record.py:2434`, the bare-name arm
of `landings`.

**What is wrong.** The arm keeps a name only when one key of `units` carries
it. `units` is what `fix_pass_units` returns: the names the fixes added or
changed, and nothing else. So suppose the range changes `u` in `mod.py` and
also touches `other.py`, which carries its own `u` unchanged. A bare `` `u` ``
then has one hit and lands at `mod.py#u`. The finding might as well be about
`other.py#u`, which no fix wrote.

**Why it matters.** Three places claim the narrower rule:

- `docs/round-record-spec.md:696` says a bare name lands "only where one file of
  the range carries it".
- Ledger row A1 says "only where exactly one file of the range carries it".
- The docstring says "a bare name two files of the range carry" lands nowhere.

A name the reading cannot place is meant to land nowhere, because a false
`first` brings a stop one landing closer and a false `second` costs a framer
segment. The new case
`tests/test_a_fix_of_a_fix_is_counted.py#test_a_bare_name_two_files_of_the_range_carry_does_not_land`
covers only two files that BOTH carry a changed or added `u`.

**Executed.** In a planted repository, round 1's fix changed `u` in `mod.py`
and changed `z` in `other.py`, which also defines `u`. Round 2's `` `u` ``
wrote `first — 🟡 1 at mod.py#u, a unit round-1's fixes changed`. With the
fix below applied in the scratch clone, it wrote `no`.

## 🟡 2 — A file the extension list does not name is not read as a file

**Where.** `skills/code-review/scripts/round_record.py:2426`, where `landings`
asks `NAMES_A_FILE_RE` whether the cell names a file.

**What is wrong.** The rule the fix states is "a cell that names a file is
about that file". The code implements it as a list of fourteen extensions. A
cell naming any other file falls through, and its backticked names land in
whichever touched file defines them. Four shapes do this:

- `` `bin/tool`, which calls `u` ``
- `` `bin/tool.cmd`, which calls `u` ``
- `` `Makefile`, the target that runs `u` ``
- `` `hooks/x.html`, which names `u` ``

**Why it matters.** This repository's own wrappers are exactly those shapes:
18 tracked files with no extension and 17 `.cmd` files. A finding about
`bin/round-record` that names the `main` it calls is a finding in a shell
script. It lands in a Python unit of another file, which is round 1's yellow 1
again under a different path.

**Executed.** All four cells wrote `first — 🟡 1 at mod.py#u, …` at the target,
with the files tracked. With the fix below they wrote `no`. The fix keeps the
extension list and also treats any code span or path the tree tracks as
naming a file. A cell that names an untracked `.html` path still lands. That
is the permissive direction, and no record names such a path.

**What the corpus says.** No `Location` at `v0.18.0` or `v0.18.3` names a
`bin/` wrapper or a `.cmd` file, so this is latent, as round 1's yellow 1 was.

## ⬜ 3 — "Where an open row could land" is not what the refusal checks

**Where.** `docs/round-record-spec.md:697`, the `landings` docstring at
`skills/code-review/scripts/round_record.py:2373`, and ledger row A1.

The three say an unresolvable range refuses `new` "where an open row could
land". The code refuses whenever any open row commissions a fix, whatever its
`Location`. With `deadbeef..cafebabe` as the previous range and one open 🟡 at
`` `README.md:1` ``, `new` exited 2 and wrote nothing (executed). That row can
never land. The behaviour is defensible because the tree is the wrong one either
way. The sentence describes a narrower rule than the code keeps.

## ⬜ 4 — Q4 is recorded as settled by the reviewer

**Where.**
`seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:27`
and `questions.md` Q4.

Both mark Q4 ✅, "settled by round 1's reviewer's sample", and "The function
grain stays". Round 1's report said: "Whether 26 stops in 64 is the stop rate
the owner wants is still the owner's call. What the sample settles is that the
stops are not noise." Q4's own answerer column names the repository owner. The
sample answered whether the stops are real. It did not answer whether the
owner wants the rate. This is the run's paperwork, so it is a correction and
stays out of `Needs a fix`.

## What was checked and found sound

- **The gate's new refusals** fire once each where they should. The
  `elif` keeps a `second` on a run's first record from reporting twice, and
  `test_a_landing_on_the_first_record_after_a_stop_fails` pins the count of
  one (read; the case executed).
- **The depth restart has no second reader.** `chain_check` checks the
  declared depth and never walks earlier records' `New units`, so the generator
  is the only walk to restart (read: every use of `NEW_UNITS` in
  `chain_check.py`).
- **A doc-located finding in `depth_two`.** `depth_two` still reads a backticked
  name beside a `.md` path as a bare unit. It refuses only when that finding's
  own fix commit adds a unit to a file carrying the name, and that fix touched
  the code. I found no false refusal there, so I raise no finding (read).
- **The ten new `Re-read ·` rows.** Each cites `round_record.py`'s `close`, at the hash `a258705d`,
  and none of the ten claims is about which records the depth walk reads.
  Their claims hold against `close` as it stands (read).
- **The docs and the changelog** say what the code does, except the
  sentences 🟡 1, 🟡 2 and ⬜ 3 name (read).

## Regression tests to plant

| Destination | Case |
|---|---|
| `tests/test_a_fix_of_a_fix_is_counted.py`, beside the bare-name case | a bare name that a second touched file carries unchanged reads `no` — red at the target (🟡 1, executed as a probe) |
| the same file | a name beside `bin/tool`, `bin/tool.cmd` or `Makefile`, each tracked, reads `no` — red at the target (🟡 2, executed as a probe) |

## Facts for the evidence ledger

- Ledger row A1's sentence "a bare name only where exactly one file of the
  range carries it" and "a backticked name beside it lands only through that
  path" are false at the target for 🟡 1's and 🟡 2's shapes (executed). The fix
  corrects the row in place with a `Corrected` note.
- `chain_check.py#runs_of` and `round_record.py#current_run` cut identically
  over all 5,460 chains of `None`, 0, 1 and 2 up to six records long
  (executed, monkeypatched readers).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A bare name lands when a second file of the range carries it unchanged: the one-file check counts only units the fixes added or changed, against `docs/round-record-spec.md:696` and ledger A1 | `skills/code-review/scripts/round_record.py:2434` | open | executed: `u` changed in `mod.py`, `other.py` touched and carrying `u` unchanged; a bare `` `u` `` wrote `first … at mod.py#u`; `no` with the fix applied |
| 🟡 2 | A cell naming a file outside `NAMES_A_FILE_RE`'s extensions — a `bin/` wrapper, `.cmd`, `Makefile`, `.html` — still lands its backticked name in a Python unit of another file | `skills/code-review/scripts/round_record.py:2426` | open | executed: four tracked shapes each wrote `first … at mod.py#u`; `no` with the fix applied. Latent in the `v0.18.0` and `v0.18.3` records |
| ⬜ 3 | The spec, the docstring and ledger A1 say an unresolvable range refuses where an open row could land; it refuses whenever any row is open, a document-located one included | `docs/round-record-spec.md:697` | open | executed: `deadbeef..cafebabe` and one open row at `` `README.md:1` `` exited 2 with nothing written |
| ⬜ 4 | `overview.md` and Q4 record the stop rate as settled by round 1's reviewer; round 1's report left it the owner's call | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:27` | open | read: round 1's report, Q4 section; a records correction, outside `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — a document `Location`, and a name beside an untouched `.py` path, land nowhere | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: the three new parameters red at `e66d04c0`, green at the target; the class's residue is this round's yellow 1 and yellow 2 |
| 🟢 | round 1's finding 2 is closed — the gate refuses a landing on a run's first record and a `second` with no landing before it, and an orphan `second` cuts no run | `skills/code-review/scripts/chain_check.py#fix_of_a_fix` | confirmed | executed: four new cases red at `e66d04c0`; `runs_of` and `current_run` agree over 5,460 chains |
| 🟢 | round 1's finding 3 is closed — with no open row the range is not read | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: `test_a_foreign_range_with_no_open_row_reads_no` red at `e66d04c0` |
| 🟢 | round 1's finding 4 is closed — `frame`'s refusal names the `Reframed` lines a foot may end on, pinned | `skills/code-review/scripts/chain_check.py#frame` | confirmed | executed: the pin red at `e66d04c0` |
| 🟢 | round 1's finding 5 is answered — the 23 records' numbers are in `overview.md:28` and Q1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | read |
| 🟢 | round 1's out-of-scope depth question is decided and built — the depth walk reads the current run | `skills/code-review/scripts/round_record.py#close` | confirmed | executed: `test_the_depth_restarts_at_a_stop` red at `e66d04c0`; read: `chain_check.py` walks no earlier `New units` |
| 🟢 | the ledger fragment's anchors hold, and the ten new `Re-read ·` rows' claims hold against `close` | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | executed: `evidence-check --strict` over the fragment, 223 ok, 0 drifted, exit 0; read: the ten cited claims |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_fix_of_a_fix_is_counted.py` and `tests/test_the_chain_goes_back_to_its_framer.py`, at the target in a scratch clone | 67 passed, exit 0 |
| The same two modules with `round_record.py` and `chain_check.py` checked out at `e66d04c0` | 11 failed, 56 passed, exit 1 — exactly the eleven cases the fix pass added |
| A landings probe, one `test_tmp_` file run once and deleted: a second touched file carrying `u`; six cells naming files of other kinds; one open document row over a foreign range | 🟡 1 and 🟡 2 reproduced; the `.md` cells read `no`; ⬜ 3 reproduced, exit 2 |
| The same probe and the two modules with the paste-ready fixes applied in the scratch clone | every probe cell `no`; 67 passed, exit 0 |
| A run-cut probe, one `test_tmp_` file run once and deleted: `runs_of` against `current_run` over every chain of `None`, 0, 1 and 2 up to six records | 5,460 chains, no disagreement |
| `bin/evidence-check --strict --ledger` over the work item's fragment, at the target | 223 ok, 0 drifted, 0 broken, exit 0 |
| The broad gate — the full suite, the repository-wide lint and the typecheck over the branch | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 and 🟡 2

Both locations are inside `landings`, which round 1's fixes changed, and not
inside a unit they added. So the two units below are added at depth 1.

In `skills/code-review/scripts/round_record.py`, above `landings`:

```python
def range_carriers(reader, root, a, b):
    """{name: {path}} for every top-level unit each Python file the range
    touched carries at `b`, whether or not the fixes changed it."""
    carriers = {}
    for rel in touched(root, a, b):
        if not rel.endswith(".py"):
            continue
        module = parse_module(reader.show(root, b, rel))
        for name in unit_dumps(module) if module is not None else {}:
            carriers.setdefault(name, set()).add(rel)
    return carriers


def names_a_file(reader, location, tracked):
    """True when a `Location` cell names a file of any kind: by an extension
    the records use, or by a code span or path the tree tracks -- `bin/test`,
    a `.cmd` wrapper, a `Makefile`, which no extension list reaches."""
    visible = reader.visible(location)
    if NAMES_A_FILE_RE.search(visible):
        return True
    tokens = re.findall(r"`([^`]+)`", visible) + re.findall(
        r"[\w.-]*/[\w./-]+", visible
    )
    for token in tokens:
        path = re.split(r"::|[:#@]", token.strip())[0]
        if path and resolve_path(path, tracked) is not None:
            return True
    return False
```

In `landings`, from `units = fix_pass_units(...)` to the end of the bare-name
arm:

```python
    units = fix_pass_units(reader, root, a, b)
    if not units:
        return []
    carriers = range_carriers(reader, root, a, b)
    tracked = tracked_at(root, target)
    found = []
    for label, location in open_rows:
        pairs = location_units(reader, root, target, location, tracked)
        # Round 1's 🟡 1. A cell that names a file is about that file, so a
        # backticked name beside it is prose about the file and never a unit
        # in another one: a document `Location` lands nowhere (S5, §Out), and
        # a name beside a `.py` path lands only through that path.
        if names_a_file(reader, location, tracked):
            pairs = [(rel, unit) for rel, unit in pairs if rel is not None]
        for rel, unit in pairs:
            if rel is not None:
                hits = [(rel, unit)]
            else:
                # A bare name lands only where ONE file of the range carries
                # it at all -- changed, added, or left as it was.
                if len(carriers.get(unit, ())) != 1:
                    continue
                hits = [key for key in units if key[1] == unit]
```

In `tests/test_a_fix_of_a_fix_is_counted.py`:

```python
def test_a_bare_name_a_touched_file_carries_unchanged_does_not_land(repo):
    """Round 2's 🟡 1: `other.py` is touched by round 1's fix and carries a
    `u` the fix left alone, so a bare `u` names either file."""
    declared(repo)
    write(repo, "other.py", "def u():\n    return 0\n\n\ndef z():\n    return 1\n")
    commit(repo, "other.py")
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    write(repo, "other.py", "def u():\n    return 0\n\n\ndef z():\n    return 2\n")
    fixed(repo, 1, a, MOD_FIXED, [1])
    code, out, text, _ = a_round(repo, 2, finding("`u`"))
    assert code != 2, out
    assert row(text) == "no", row(text)


@pytest.mark.parametrize(
    "location",
    [
        "`bin/tool`, which calls `u`",
        "`bin/tool.cmd`, which calls `u`",
        "`Makefile`, the target that runs `u`",
    ],
)
def test_a_name_beside_a_file_of_any_kind_does_not_land(repo, location):
    """Round 2's 🟡 2: a file is a file whatever its extension."""
    for rel in ("bin/tool", "bin/tool.cmd", "Makefile"):
        write(repo, rel, "u\n")
    commit(repo, "the files the cells name")
    code, out, text, _ = two_rounds(repo, location)
    assert code != 2, out
    assert row(text) == "no", (location, row(text))
```

`docs/round-record-spec.md:695-696` and ledger row A1 then read true as written.
The `landings` docstring's "a bare name two files of the range carry" also
reads true.

### ⬜ 3

`docs/round-record-spec.md:696-697`, and the same words in the `landings`
docstring and ledger row A1:

```markdown
this tree cannot resolve refuses `new` at exit 2 while any row of the report
is open, and is not read when none is.
```

Needs a fix: yes — 🟡 1, a bare name lands where a second touched file carries it unchanged; 🟡 2, a cell naming a file outside the extension list lands its backticked name in another file
Loses a record or crashes: no

The broad gate has not run, and it is not yet due: 🟡 1 and 🟡 2 are open.

## Proof

Opened in the scratch clone at the target, or in the worktree for the work
item's own files:

- `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/`
  `rounds/round-1.md`, `rounds/round-1-report.md`, `overview.md` rows 27–28,
  `questions.md` Q1, Q4 and Q5
- the fix range's diff whole: `skills/code-review/scripts/round_record.py`,
  `skills/code-review/scripts/chain_check.py`, both test modules,
  `docs/round-record-spec.md`, `skills/code-review/orchestration.md`, the
  ledger fragment, `changelog.md`, `survivors.md`; and `c705cd6d`'s diff
- `skills/code-review/scripts/round_record.py`: `COMMISSIONS_NOTHING`,
  `NAMES_A_FILE_RE`, `fof_count_of`, `current_run`, `reframed_after`,
  `unit_dumps`, `fix_pass_units`, `landings`, `fix_of_a_fix_value`,
  `stop_line`, `build` from the verdict keying to the field rows,
  `earlier_records`, the `Location` patterns, `units_named_earlier`,
  `tracked_at`, `resolve_path`, `location_units`, `depth_two`, `close`
  around the depth call
- `skills/code-review/scripts/chain_check.py`: the `Fix of a fix` constants
  and `REFRAME_RE`, `fix_of_a_fix_count`, `frame_foot`, `fof_of`, `runs_of`,
  `fix_of_a_fix`, `main`'s run placement, every use of `NEW_UNITS`
- `tests/test_a_fix_of_a_fix_is_counted.py` lines 1–200 and the fix range's
  hunks; `tests/test_the_chain_goes_back_to_its_framer.py`'s fix range hunks
- `docs/round-record-spec.md` §*The depth in `New units`* and §*A fix of a
  fix*
- the ten released rows the new `Re-read ·` rows cite, in
  `seal/releases/0.8.1.md`, `0.11.4.md`, `0.11.5.md`, `0.12.0.md`,
  `0.12.1.md`, `0.15.0.md`, `0.15.1.md` and `0.16.0.md`
- `bin/test`
