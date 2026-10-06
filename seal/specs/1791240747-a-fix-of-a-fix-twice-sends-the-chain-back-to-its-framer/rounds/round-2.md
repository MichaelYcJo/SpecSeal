# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — review round 2

| Field | Value |
|---|---|
| Target SHA | c705cd6d35c5e05c56cbb40e6ae0929ad6066665 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #828 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `01b1f966a7a582d77296e8a678e5045bd2d25701..34e899c031a360273ccdd6486612beef3954a64f`, 4 commits |
| Contract changes | none |
| New units | CELL_WORD_RE (depth 1); PATH_TAIL_RE (depth 1); names_a_file (depth 1); range_carriers (depth 1); test_a_bare_name_a_touched_file_carries_unchanged_does_not_land (depth 1); TRACKED_FILES (depth 1); test_a_name_beside_a_tracked_file_of_any_kind_does_not_land (depth 1); test_a_name_beside_a_tracked_py_file_lands_only_through_it (depth 1) |
| Fix of a fix | first — 🟡 1 at skills/code-review/scripts/round_record.py#landings, a unit round-1's fixes changed; 🟡 2 at skills/code-review/scripts/round_record.py#landings, a unit round-1's fixes changed |
| Needs a fix | yes — 🟡 1, a bare name lands where a second touched file carries it unchanged; 🟡 2, a cell naming a file outside the extension list lands its backticked name in another file |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 1's fix range `e66d04c0..16fbe326`: whether a Location that names any file lands only through that file's units and a bare name only where exactly one file of the range carries it; whether the gate now refuses a `first` or `second` on a run's first record and a `second` with no earlier landing, and the generator's `current_run` and the gate's `runs_of` cut a run by one rule; whether `landings` reads no range when no row is open; whether `frame`'s refusal names what a foot may end on; whether the depth walk restarts at a stop; and whether the docs, changelog and ledger rows A1, A3, A4, A5 and the ten new Re-read rows say what the code now does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A bare name lands when a second file of the range carries it unchanged: the one-file check counts only units the fixes added or changed, against `docs/round-record-spec.md:696` and ledger A1 | `skills/code-review/scripts/round_record.py:2434` | **fixed** `b8c06276` | fixed at b8c06276; executed: `u` changed in `mod.py`, `other.py` touched and carrying `u` unchanged; a bare `` `u` `` wrote `first … at mod.py#u`; `no` with the fix applied |
| 🟡 2 | A cell naming a file outside `NAMES_A_FILE_RE`'s extensions — a `bin/` wrapper, `.cmd`, `Makefile`, `.html` — still lands its backticked name in a Python unit of another file | `skills/code-review/scripts/round_record.py:2426` | **fixed** `b8c06276` | fixed at b8c06276; executed: four tracked shapes each wrote `first … at mod.py#u`; `no` with the fix applied. Latent in the `v0.18.0` and `v0.18.3` records |
| ⬜ 3 | The spec, the docstring and ledger A1 say an unresolvable range refuses where an open row could land; it refuses whenever any row is open, a document-located one included | `docs/round-record-spec.md:697` | **fixed** `64324d11` | fixed at 64324d11; executed: `deadbeef..cafebabe` and one open row at `` `README.md:1` `` exited 2 with nothing written |
| ⬜ 4 | `overview.md` and Q4 record the stop rate as settled by round 1's reviewer; round 1's report left it the owner's call | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:27` | answered | corrected at 1cfb3904 — overview.md and Q4 say round 1 reviewer supplied the sample and the decision was the orchestrator under the owner automation delegation; read: round 1's report, Q4 section; a records correction, outside `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — a document `Location`, and a name beside an untouched `.py` path, land nowhere | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: the three new parameters red at `e66d04c0`, green at the target; the class's residue is this round's yellow 1 and yellow 2 |
| 🟢 | round 1's finding 2 is closed — the gate refuses a landing on a run's first record and a `second` with no landing before it, and an orphan `second` cuts no run | `skills/code-review/scripts/chain_check.py#fix_of_a_fix` | confirmed | executed: four new cases red at `e66d04c0`; `runs_of` and `current_run` agree over 5,460 chains |
| 🟢 | round 1's finding 3 is closed — with no open row the range is not read | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: `test_a_foreign_range_with_no_open_row_reads_no` red at `e66d04c0` |
| 🟢 | round 1's finding 4 is closed — `frame`'s refusal names the `Reframed` lines a foot may end on, pinned | `skills/code-review/scripts/chain_check.py#frame` | confirmed | executed: the pin red at `e66d04c0` |
| 🟢 | round 1's finding 5 is answered — the 23 records' numbers are in `overview.md:28` and Q1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | read |
| 🟢 | round 1's out-of-scope depth question is decided and built — the depth walk reads the current run | `skills/code-review/scripts/round_record.py#close` | confirmed | executed: `test_the_depth_restarts_at_a_stop` red at `e66d04c0`; read: `chain_check.py` walks no earlier `New units` |
| 🟢 | the ledger fragment's anchors hold, and the ten new `Re-read ·` rows' claims hold against `close` | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | executed: `evidence-check --strict` over the fragment, 223 ok, 0 drifted, exit 0; read: the ten cited claims |

## Paste-ready fixes

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
```markdown
this tree cannot resolve refuses `new` at exit 2 while any row of the report
is open, and is not read when none is.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:2396` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:3933` | round 1's ⬜ 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2373` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:4715` | round 1's ⬜ 4 — fixed |
| round-1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:28` | round 1's ⬜ 5 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#landings` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#fix_pass_units` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/chain_check.py#runs_of` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py#units_named_earlier` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
