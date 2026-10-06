# Round 3 report — 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer

| Field | Value |
|---|---|
| Target SHA | 6ceb7d469199e1ce0e39904cb649ab94b38c86c3 |
| Base | `origin/release/v0.19.0` |
| Pull request | #828 (draft) |
| Round kind | verifying round — round 2's fix range `01b1f966..34e899c0`, and the units its `New units` row names |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Every verdict round 2 closed is closed for the shapes it named. A `bin/`
wrapper, a `.cmd` file, a `Makefile` and an `.html` file now keep their
backticked name from landing elsewhere. A touched file that carries a bare name
unchanged now counts as a second carrier. Seven of the fix pass's eight new
cases fail against `round_record.py` as it stood at `01b1f966`, and the eighth
is the guard for the other half (executed).

The fix pass also introduced one new problem, and it sits in `names_a_file`,
a unit round 2's fixes added:

1. **A cell naming a file the reading cannot place lands its backticked name
   again** (🟡 1). The check asks `resolve_path` for one tracked path. Three
   kinds of cell get no answer from it: a basename the tree holds twice
   (`SKILL.md`, `conftest.py`), a path the tree does not hold (one the fixes
   deleted, or one written wrong), and a path written in quotes or followed
   by `'s`. Each of these cells then reads as naming no file, so its
   backticked name is treated as a bare name and lands. The first two kinds
   read `no` at `01b1f966` and read `first` at the target. The fix pass
   regressed them.

That finding is inside a unit round 2's fixes added. Under this branch's own
rule, this record's `Fix of a fix` therefore reads `second`. The grade below
is set by what the defect does, not by that consequence.

One sentence needs correcting and needs no fix:

- `docs/round-record-spec.md`, ledger row A1 and the changelog fragment all
  say a bare name lands only where exactly one file the range touched defines
  it. `range_carriers` counts only Python files, which is what its own
  docstring and Q2 say (⬜ 2).

The records say what happened. The range refusal's sentence now says what the
code does.

## How often the regressed shapes occur

I counted the shapes before grading them. Over the 237 round records committed
at the tags `v0.15.0` to `v0.18.3` and at the target, 414 rows owe a fix. None
of them has a `Location` that the old extension check read as naming a file
and the new one reads as naming none (executed, each record against the tree
of its own tag). The fenced fix below changes the reading of none of those 414
rows.

So the defect has not occurred in the corpus. It is graded 🟡 anyway, for
three reasons:

- It is a regression the fix pass introduced, not a gap that was already there.
- The documented claims (spec, ledger A1, changelog) say that a document
  `Location` lands nowhere. For these shapes that is false.
- Its cost is a false `first`/`second`, and a false `second` stops the run and
  sends the work item to its framer. The docstring's own rule is that what the
  reading cannot place goes the permissive way.

Round 2 graded the mirror-image shape 🟡 as well.

## 🟡 1 — a file the reading cannot place stops being a file

`skills/code-review/scripts/round_record.py:2259`. `names_a_file` treats a
word containing a `/` or a `.` as a file only when `resolve_path` returns a
single tracked path. `resolve_path` returns None in two cases: when two
tracked paths end in the word, and when none do. So `` `SKILL.md` §*X*, which
names `u` `` reads as naming no file in a tree that holds `docs/a/SKILL.md` and
`docs/b/SKILL.md`. The same goes for `` `gone.md`, which names `u` `` after
the fixes deleted `gone.md`. In both cells `` `u` `` becomes a bare name, and
it lands in `mod.py#u`.

`CELL_WORD_RE` also does not split on `'` or `"`. As a result `bin/tool's`
and `"bin/tool"` are each one word, and neither one resolves.

The removed `NAMES_A_FILE_RE` read every one of these cells as naming a file,
except the two whose path has no extension (`bin/tool's` and `"bin/tool"`).
So the other cells read `no` before the fix and `first` after it. Round 1's 🟡 1 had closed exactly this class: a document
`Location` lands nowhere. For these shapes it is open again.

What the fix keeps and what it changes:

- **What stays** — the tree answers first. A unique tracked path of any kind
  is a file, and a bare identifier is a file only where the tree tracks it
  exactly. An identifier equal to `bin/u`'s basename still lands (executed).
- **What it adds** — a word the tree holds more than once is a file, and so
  is a word the tree does not hold that ends in a file extension. Quotes and
  apostrophes stop a word.
- **What it leaves alone** — a directory such as `` `docs/missing/` ``. That
  cell read `first` before the fix pass too, and a directory is not a file.

The fix adds no top-level name. The pattern stays local to the function so
the fix does not create a unit of its own inside a unit an earlier fix pass
created.

## ⬜ 2 — "one file the range touched" means one Python file

`docs/round-record-spec.md:697`, ledger row A1 and the changelog fragment say
a bare name lands only where exactly one file the range touched defines it.
`range_carriers` reads only `.py` files. So when a touched `tool.sh` defines
`u()` and `mod.py`'s `u` changed, a bare `` `u` `` still lands in `mod.py#u`
(executed). The code follows Q2, where a file the AST cannot read contributes
nothing, and its docstring says so. The three sentences are what overclaim.
The fix is one word in each.

## What this round was asked, answered

- **`names_a_file` decides by the tracked paths at the target.** This holds
  for a path with `:line`, `#unit`, `::unit` or `@hash`. It holds for a path
  outside a code span when a comma or a full stop follows it. It holds for an
  extensionless file and a `.cmd` file. An identifier equal to a tracked
  path's basename is not taken for a file. All of this was executed and reads
  as intended. It does not hold for a path the tree does not hold, an
  ambiguous basename, or a path next to a quote or an apostrophe (🟡 1).
- **`range_carriers` counts every file of the range that defines a name,
  changed or not.** For Python files it does: an unchanged touched file and
  an added file each count (executed). An untouched file does not count, as
  the spec says. A non-Python file does not count, and the spec does not say
  so (⬜ 2).
- **The range refusal's sentence says what the code does.** A foreign range
  with one open 🟡 at `README.md:1` exits 2 and writes nothing. With only an
  open ⬜, or only a `deferred` 🟡, it writes the record (executed).
- **The records.** `round-2.md`'s `Fix range` names 4 commits, and
  `git rev-list --count` agrees. Its `New units` row names the eight units the
  range added, and `NAMES_A_FILE_RE`, which it removed, is absent. The ledger
  fragment holds 228 rows, all ok. The overview and Q4 corrections say what
  round 1's report said (read).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A cell naming a file the reading cannot place reads as naming none, so its backticked name lands as a bare name: a basename the tree holds twice, a path the tree does not hold (one the fixes deleted), a path in quotes or followed by an apostrophe. The first two read `no` before round 2's fix and `first` after it | `skills/code-review/scripts/round_record.py:2259` | open | executed: six cells read `first` at the target and `no` with the fenced fix; four of them read `no` with `01b1f966`'s script. 0 of 414 committed rows owing a fix carry the shape |
| ⬜ 2 | The spec, ledger A1 and the changelog say a bare name lands only where one file the range touched defines it; the code counts Python files only, as its docstring and Q2 say | `docs/round-record-spec.md:697` | open | executed: a touched `tool.sh` defining `u()` beside a changed `mod.py#u`, a bare `u` reads `first`. A sentence correction; outside `Needs a fix` |
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

### 🟡 1 — `skills/code-review/scripts/round_record.py`, `CELL_WORD_RE` and `names_a_file`

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

The docstring's first paragraph then reads:

```python
    """True when a word of the `Location` cell names a file, with or without
    `:line`, `#unit` or `::unit` after it: a path the tree tracks, a basename
    it tracks more than once, or a path it does not track that ends in a file
    extension — the last two are files the reading cannot place.
```

The case, in `tests/test_a_fix_of_a_fix_is_counted.py`, after
`test_a_name_beside_a_tracked_py_file_lands_only_through_it`:

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

### ⬜ 2 — the three sentences

`docs/round-record-spec.md:696`:

```markdown
only through a `.py` path, and a bare name only where exactly one Python file
the range touched defines it at the target. A range whose ends this tree cannot resolve
```

Ledger row A1 and the changelog fragment take the same word: "exactly one
Python file the range touched defines it", and "a bare name more than one
touched Python file defines".

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

## Regression tests to plant

- `tests/test_a_fix_of_a_fix_is_counted.py` — the parametrized case under 🟡 1
  above. Each of its six cells reads `first` at the target and `no` with the
  fix (executed in the probe above).

## Facts for the evidence ledger

- Ledger row A1's clause about a cell naming a file should, once 🟡 1 is
  fixed, cite the new case beside the `names_a_file` anchor. Its bare-name
  clause takes the word "Python" (⬜ 2).

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1, a cell naming a file the reading cannot place (a basename held twice, a path not held, a path against a quote or apostrophe) lands its backticked name, regressed by round 2's fix

Loses a record or crashes: no

## Proof block

Opened in the scratch clone at the target: `skills/code-review/scripts/round_record.py`
(`CELL_WORD_RE` through `range_carriers`, `unit_dumps`, `fix_pass_units`,
`landings`, `touched`, `parse_module`, `tracked_at`, `resolve_path`,
`location_units`, the verdict-column constants and `LOCATION_UNIT_RE`);
`skills/code-review/scripts/chain_check.py` (`CLOSED_WORDS`, `verdict_of`'s
head); `skills/verify/scripts/unverified_check.py` (`visible`);
`tests/test_a_fix_of_a_fix_is_counted.py` (fixtures, `two_rounds`, `row`, the
foreign-range cases, the fix pass's new cases);
`tests/test_the_record_is_generated.py` (`git`, `write`, `commit`);
`docs/round-record-spec.md:688-698`; `bin/test`; the work item's
`rounds/round-2.md` and the head of `rounds/round-2-report.md`; ledger row A1
of `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md`;
and the fix range's diffs of `changelog.md`, `overview.md`, `questions.md` and
`survivors.md`.
