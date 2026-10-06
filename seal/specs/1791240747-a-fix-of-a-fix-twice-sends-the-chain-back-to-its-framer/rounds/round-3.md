# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — review round 3

| Field | Value |
|---|---|
| Target SHA | 6ceb7d469199e1ce0e39904cb649ab94b38c86c3 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #828 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `6ceb7d469199e1ce0e39904cb649ab94b38c86c3..6ceb7d469199e1ce0e39904cb649ab94b38c86c3`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | second — 🟡 1 at skills/code-review/scripts/round_record.py#names_a_file, a unit round-2's fixes added; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🟡 1, a cell naming a file the reading cannot place (a basename held twice, a path not held, a path against a quote or apostrophe) lands its backticked name, regressed by round 2's fix |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 2's fix range `01b1f966..34e899c0`, which ends the run: whether `names_a_file` decides a file by the tracked paths at the target for every shape a `Location` takes (a path with `:line`, `#unit` or `::unit`, a path outside a code span, an extensionless or `.cmd` file, a path the tree does not hold, an identifier that equals a tracked path's basename); whether `range_carriers` counts every file of the range that defines a name, changed or not; whether the range refusal's sentence now says what the code does; and the records. A finding that lands in `landings`, `names_a_file` or `range_carriers` makes this record's `Fix of a fix` read `second`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A cell naming a file the reading cannot place reads as naming none, so its backticked name lands as a bare name: a basename the tree holds twice, a path the tree does not hold (one the fixes deleted), a path in quotes or followed by an apostrophe. The first two read `no` before round 2's fix and `first` after it | `skills/code-review/scripts/round_record.py:2259` | deferred the frame | the frame — the run read second at round 3; the redesign answers it; executed: six cells read `first` at the target and `no` with the fenced fix; four of them read `no` with `01b1f966`'s script. 0 of 414 committed rows owing a fix carry the shape |
| ⬜ 2 | The spec, ledger A1 and the changelog say a bare name lands only where one file the range touched defines it; the code counts Python files only, as its docstring and Q2 say | `docs/round-record-spec.md:697` | deferred the frame | the frame — the run read second at round 3; the redesign answers it; executed: a touched `tool.sh` defining `u()` beside a changed `mod.py#u`, a bare `u` reads `first`. A sentence correction; outside `Needs a fix` |
| 🟢 | round 2's yellow 1 is closed — a touched file carrying the name unchanged is a second carrier, and so is an added file | `skills/code-review/scripts/round_record.py#range_carriers` | confirmed | executed: both read `no` at the target; the unchanged case read `first` with `01b1f966`'s script |
| 🟢 | round 2's yellow 2 is closed for every tracked file the tree holds once — extensionless, `.cmd`, `Makefile`, `.html`, with `:line`, `#unit`, `::unit` or `@hash`, outside a code span before a comma or a full stop | `skills/code-review/scripts/round_record.py#names_a_file` | confirmed | executed: every such cell `no`; `mod.py#u`, `mod.py::u`, `mod.py:5` still `first`; a backticked or bare identifier equal to `bin/u`'s basename still `first`. The class's residue is yellow 1 |
| 🟢 | round 2's sentence correction 3 is closed — the refusal fires while any row owing a fix is open, wherever it points | `docs/round-record-spec.md:698` | confirmed | executed: open yellow at `README.md:1` over `deadbeef..cafebabe` exit 2, nothing written; an open white square or a `deferred` row, exit 0 and written |
| 🟢 | round 2's correction 4 is closed — the overview and Q4 say the orchestrator decided under the owner's delegation, on the reviewer's sample | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md` | confirmed | read: the overview and Q4 diffs in `1cfb3904` against round 1's report |
| 🟢 | round 1's finding 1 is closed for a document `Location` the tree holds once and a name beside an untouched `.py` path | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: the module's cases at the target, 75 passed; re-derived because round 2's fixes changed what it rested on, and its residue is this round's yellow 1 |
| 🟢 | round 1's finding 3 is closed — with no open row the range is not read | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: an open white square over a foreign range, written with exit 0 |
| carried | round 1's finding 2 is closed — the gate refuses a landing on a run's first record and an uncounted `second` | `skills/code-review/scripts/chain_check.py#fix_of_a_fix` | confirmed | carried from round 2; `chain_check.py` is outside round 2's fix range. Executed: the gate's module passes at the target |
| carried | round 1's finding 4 is closed — `frame`'s refusal names the lines a foot may end on | `skills/code-review/scripts/chain_check.py#frame` | confirmed | carried from round 2; outside round 2's fix range |
| carried | round 1's finding 5 is answered — the 23 records' numbers are in the overview and Q1 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | carried from round 2; Q1 untouched by round 2's fix range |
| carried | round 1's depth question is decided and built — the depth walk reads the current run | `skills/code-review/scripts/round_record.py#close` | confirmed | carried from round 2; `close` is outside round 2's fix range |
| 🟢 | round 2's record says what its fix pass did — `Fix range` of 4 commits, eight `New units`, and the ledger fragment's anchors hold | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/rounds/round-2.md` | confirmed | executed: `git rev-list --count 01b1f966..34e899c0` is 4; `evidence-check --strict` over the fragment, 228 ok, exit 0 |

## Paste-ready fixes

```python
CELL_WORD_RE = re.compile(r"[^\s`,;()\[\]'\"<>]+")
```
```python
        if "/" in path or "." in path:
            if resolve_path(path, tracked) is not None:
                return True
            # Held twice (`SKILL.md`) or not at all (a path the fixes
            # deleted, or one written wrong): still a file, and one the
            # reading cannot place, so nothing beside it lands.
            bare = path[2:] if path.startswith("./") else path
            if any(t.endswith("/" + bare) for t in tracked):
                return True
            if re.fullmatch(
                r"[\w./-]+\.(?:py|md|markdown|txt|rst|json|toml|ya?ml|cfg|ini"
                r"|sh|js|ts|cmd|html)",
                bare,
            ):
                return True
        elif path in tracked:
            return True
```
```python
    """True when a word of the `Location` cell names a file, with or without
    `:line`, `#unit` or `::unit` after it: a path the tree tracks, a basename
    it tracks more than once, or a path it does not track that ends in a file
    extension — the last two are files the reading cannot place.
```
```python
@pytest.mark.parametrize(
    "location",
    [
        # A basename the tree holds twice.
        "`SKILL.md` §*X*, which names `u`",
        "`conftest.py:1`, whose fixture calls `u`",
        # A path the tree does not hold.
        "`gone.md`, which names `u`",
        "`gone.py:3`, which calls `u`",
        # A path a quote or an apostrophe stands against.
        "bin/tool's wrapper calls `u`",
        '"bin/tool" calls `u`',
    ],
)
def test_a_name_beside_a_file_the_reading_cannot_place_does_not_land(repo, location):
    """Round 3's 🟡 1: `resolve_path` answering None is not the cell naming
    no file. A file held twice or not at all is one the reading cannot place,
    and that is the permissive direction."""
    for rel in ("docs/a/SKILL.md", "docs/b/SKILL.md", "pkg/a/conftest.py",
                "pkg/b/conftest.py", "bin/tool"):
        write(repo, rel, "u\n")
    commit(repo, "the files the cells name")
    code, out, text, _ = two_rounds(repo, location)
    assert code != 2, out
    assert row(text) == "no", (location, row(text))
```
```markdown
only through a `.py` path, and a bare name only where exactly one Python file
the range touched defines it at the target. A range whose ends this tree cannot resolve
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_fix_of_a_fix_is_counted.py` and `tests/test_the_chain_goes_back_to_its_framer.py`, at the target in a scratch clone | 75 passed, exit 0 |
| `bin/test` on `tests/test_a_fix_of_a_fix_is_counted.py` with `round_record.py` checked out at `01b1f966` | 7 failed, 34 passed, exit 1 — the seven new cases the fix pass wrote for its two findings; the eighth, the `.py`-path guard, passes there by design |
| A landings probe, one `test_tmp_` file run once and deleted: 17 `Location` shapes over planted `SKILL.md` and `conftest.py` pairs, `bin/tool`, `bin/u`, plus a deleted `notes.md`, at the target | 7 cells naming a file read `first`: the two ambiguous basenames, `gone.md`, `gone.py:3`, the deleted `notes.md`, `bin/tool's` and `"bin/tool"`; every uniquely tracked path read `no` |
| The same probe with `round_record.py` at `01b1f966` | `SKILL.md`, `conftest.py:1`, `gone.md`, `gone.py:3` and the deleted `notes.md` read `no`; the tracked `bin/tool` shapes read `first` — the regression and round 2's fix, side by side |
| The same probe and the two modules with the fenced fix applied in the scratch clone | the seven cells `no`; `` `docs/missing/` `` and the identifiers still `first`; 75 passed, exit 0 |
| Carrier probes, the same file: a touched file carrying `u` unchanged, an added file defining `class u`, an untouched `other.py`, a touched `tool.sh` defining `u()` | `no`, `no`, `first` (the spec's rule), `first` (⬜ 2) |
| Foreign-range probes, the same file: `deadbeef..cafebabe` with one open 🟡 at `README.md:1`, one open ⬜, one `deferred` 🟡 | exit 2 with nothing written; exit 0 and written; exit 0 and written |
| A corpus scan of every round record at the tags `v0.15.0` to `v0.18.3` and at the target, each against its tag's tracked paths: rows owing a fix with a backticked name whose `Location` the old extension check read as a file and the target reads as none, and rows the fenced fix reads differently | 237 records, 414 rows; 0 and 0 |
| `bin/evidence-check --strict --ledger` over the work item's fragment, at the target | 228 ok, 0 drifted, 0 broken, exit 0 |
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
| round-2 | `skills/code-review/scripts/round_record.py:2434` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:2426` | round 2's 🟡 2 — fixed |
| round-2 | `docs/round-record-spec.md:697` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:27` | round 2's ⬜ 4 — answered |
| round-2 | `skills/code-review/scripts/chain_check.py#fix_of_a_fix` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/chain_check.py#frame` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/round_record.py#close` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
