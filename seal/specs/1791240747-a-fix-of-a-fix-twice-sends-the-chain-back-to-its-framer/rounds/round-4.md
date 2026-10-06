# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — review round 4

| Field | Value |
|---|---|
| Target SHA | 3fa1f5bc01441a176fa0cdf7774f8423f1f4189f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #828 |
| Broad gate | not yet |
| Fixes checked by | round-5 |
| Fix range | `2e211cc65602884f5e2443abc0ceac3fb06273d5..23c230fe9b88653a7dc2ccf2876ed25de7d57949`, 3 commits |
| Contract changes | location_units → 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md, round-1-report.md, round-1.md, round-2-report.md, round-2.md, round-4-report.md, round-4.md, landings, depth_two |
| New units | PATH_FORM_RE (depth 1); CODE_SPAN_RE (depth 1); CLAUSE_END (depth 1); path_forms (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1, a `#name` fragment lands through the last path the cell resolved; 🟡 2, a backslash-separated path lands through its tail; 🟡 3, the reframed case no longer sees the guard it pins |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The redesign's first round, after the run stopped at round 3 and the framer reframed (`Reframed 2026-10-06 by framer, after round 3.`). Spec compliance first against the reframed `spec.md` (§*What round 3 moved*, the reading rule, S5 and S5b): a finding lands only through a `.py` path its own `Location` carries, as `path:line`, `path#unit` or `path::unit`, and a cell with no such path lands nowhere, whatever stands beside it; `names_a_file`, `range_carriers`, `CELL_WORD_RE` and `PATH_TAIL_RE` are gone; Q6's replay keeps every measured stop (26) and #814 and #801 still read first then second. Then quality: every shape a `Location` takes, attacked against the path-only reading (a path in a code span or bare, with a line, a unit or a class method, a path the range deleted or renamed, two paths in one cell, a path with a space, a Windows separator); that this record starts the count at `no` and the run's floor, bound and depth restart past the stop; the merge of release/v0.19.0 at 3fa1f5bc and its ledger re-stamps; and that no reading of prose came back.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A bare `#name` after a path still lands, paired with the last path the cell resolved: a fourth form the spec does not name, and one that reads prose (`see #w`) and can land in a file the name does not follow | `skills/code-review/scripts/round_record.py:2437` | **fixed** `573237f4` | fixed at 573237f4; executed: `mod.py#v` then `see #w`, and `f.py#x` then `#w` beside `mod.py#v`, both read `first … mod.py#w` at the target and `no` with the fenced fix; the corpus holds one fragment cell, in a round-1 report; Q6 with the fix still 26 |
| 🟡 2 | A path written with a `\` separator is cut to its tail, so a path the tree does not hold lands in a same-named file elsewhere | `skills/code-review/scripts/round_record.py:2938` | **fixed** `573237f4` | fixed at 573237f4; executed: `pkg\mod.py:5` reads `first` and `pkg/mod.py:5` reads `no` at the target; both `no` with the fenced fix; no backslash `.py` cell in the corpus; a path with a space misses (permissive), read |
| 🟡 3 | The case pinning that the redesign's first record reads `no` locates its finding by a bare name, which never lands since the reframe, so it passes with the guard removed | `tests/test_a_fix_of_a_fix_is_counted.py:536` | **fixed** `573237f4` | fixed at 573237f4; executed: guard disabled, 2 passed; location `mod.py#u` with the guard disabled, `touched=True` fails; guard restored, 2 passed |
| 🟢 | round 3's yellow finding 1 is answered by the redesign — a basename held twice, a path not held, a quoted path and a path before an apostrophe each read `no` | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_location_that_lands_in_no_written_unit_reads_no` | confirmed | executed: the module at the target, 82 passed with the gate's module; the four shapes are S5 parameters |
| 🟢 | round 3's sentence correction 2 is answered — the carrier sentence left `docs/round-record-spec.md` with the reading | `docs/round-record-spec.md` | confirmed | read: phase 5's diff of the field section; the file is 992 lines |
| 🟢 | the four readings are gone and only comments name them | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: `git grep` over `*.py` at the target |
| 🟢 | a `.py` path with a line, a unit, a class method, `./`, `@hash` or a line range lands, in a code span or bare; a name beside a path without a unit does not | `skills/code-review/scripts/round_record.py#location_units` | confirmed | executed: the shape probe, 34 cases |
| 🟢 | Q6's replay reproduces — 26 stops at round 3, #814 and #801 first then second | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | executed: 119 of 122 records resolve with 138 pull request heads |
| 🟢 | the redesign's first record starts the count at `no`, and the run's floor and bound restart past the stop | `skills/code-review/scripts/round_record.py#build` | confirmed | executed: `round-record new --round 4` and `chain_check.py` in the scratch clone; the depth reset by its own case |
| 🟢 | the merge of the release branch holds — re-stamps only, the ledger checks pass, no correction dropped, the freeze untouched | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | executed: evidence-check, correction-check, the freeze diff, six merge-touched modules 669 passed |
| 🟢 | a unit a fix pass only moved reads `added`, as `New units` reads it | `skills/code-review/scripts/round_record.py#touched` | confirmed | executed: `git mv` in the fix, `pkg/mod2.py#u` reads `first … added`; compliant with the spec's `New units` clause |

## Paste-ready fixes

```python
def location_units(reader, root, a, text, tracked, paths_only=False):
    """[(path or None, unit)] the `Location` cell of a finding names.

    Every path is resolved against `tracked`, the tree at `a` where the fix
    started (`resolve_path`); one that resolves to nothing names no unit
    here. A `path:line` is resolved to the top-level unit holding that line
    at `a`. A backticked identifier, with or without `()`, or a cell that
    is one bare identifier, names a unit and no file, and the caller finds
    the file among the ones the range touched.

    `paths_only` keeps the forms that carry their own file -- `path#unit`,
    `path::unit`, `path:line` -- and nothing else: a `#unit` fragment is
    paired with the last path the cell resolved, which need not be the path
    it follows, and `landings` counts no name placed by what stands beside
    it (round 4's yellow 1 of #823).
    """
    visible = reader.visible(text)
    out, last = [], None
    for m in LOCATION_UNIT_RE.finditer(visible):
        last = resolve_path(m.group(1), tracked)
        if last is not None:
            out.append((last, m.group(2)))
    if not paths_only:
        for m in FRAGMENT_RE.finditer(visible):
            out.append((last, m.group(1)))
    for m in LOCATION_LINE_RE.finditer(visible):
        rel = resolve_path(m.group(1), tracked)
        module = parse_module(reader.show(root, a, rel)) if rel is not None else None
        unit = enclosing_unit(top_units(module), int(m.group(2))) if module else None
        if unit:
            out.append((rel, unit))
    if paths_only:
        return out
    for m in IDENTIFIER_RE.finditer(visible):
        out.append((None, m.group(1)))
    m = BARE_IDENTIFIER_RE.match(visible)
    if m:
        out.append((None, m.group(1)))
    return out
```
```python
    for label, location in open_rows:
        # The reframe after round 3: only a pair placed through a `.py` path
        # the cell carries for THAT name can land -- `path:line`, `path#unit`,
        # `path::unit`. A name with no path, and a `#unit` fragment that
        # borrows the last path the cell resolved, land nowhere.
        for rel, unit in location_units(
            reader, root, target, location, tracked, paths_only=True
        ):
            landing = (label, rel, unit, units.get((rel, unit)))
            if landing[3] is not None and landing not in found:
                found.append(landing)
```
```python
        # Round 4's yellow 1: a `#name` fragment borrows the last path the
        # cell resolved, so it is placed by what stands beside it.
        "`mod.py#v`; see #w",
        "`f.py#x` and `#w`, beside `mod.py#v`",
```
```python
LOCATION_UNIT_RE = re.compile(r"(?<![\w./\\-])([\w./-]+\.py)(?:#|::)([A-Za-z_]\w*)")
LOCATION_LINE_RE = re.compile(r"(?<![\w./\\-])([\w./-]+\.py):(\d+)")
```
```python
        # Round 4's yellow 2: a path the tree does not hold, with a Windows
        # separator, is not its basename.
        "`pkg\\mod.py:5`",
```
```python
    code, out, text = generate(
        repo, n=4, report_text=round_report(finding("`mod.py#u`"))
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_fix_of_a_fix_is_counted.py` and `tests/test_the_chain_goes_back_to_its_framer.py`, at the target in a scratch clone | 82 passed, exit 0 |
| A test_tmp shape probe, run once and deleted: 22 `Location` shapes over the module's two-round fixture, 5 class-method shapes, 3 space shapes, 4 rename and delete shapes | 34 passed, exit 0; the rows are quoted in the findings and in *Answered and confirmed* |
| The same shape probe with fixes 1 and 2 applied | `see #w`, `#w` beside `mod.py#v`, `pkg\mod.py:5` and `.\mod.py:5` read `no`; every path-carrying shape still `first` |
| `bin/test` on the six location-reading modules with fixes 1 and 2 applied | 306 passed, exit 0 |
| The reframed case with the `previous_pair == stopped` guard disabled, as committed | 2 passed, exit 0 — the case does not see the guard |
| The same with the location `mod.py#u` | 1 failed (`touched=True`, `first … == 'no'`), 1 passed, exit 1; with the guard restored, 2 passed, exit 0 |
| A test_tmp corpus scan of every round record and report at `v0.18.0` to `v0.18.3` and the target: distinct fix-owing `Location` cells with a fragment, a backslash `.py` path, or two `.py` coordinates | 236, 24, 20, 19 and 24 cells; fragment 1 (`v0.18.0`, a round-1 report), backslash 0, two coordinates 14, 0, 1, 0, 0 |
| A test_tmp Q6 replay, run once and deleted, in the scratch clone with 138 pull request heads and the four tags | 122 records with a previous record, 119 resolve; 36 reach `first`, 26 reach `second`, all at round 3; #814 and #801 as Q6 states; with fixes 1 and 2, the same 26 |
| `git grep` for the removed names over `*.py` at the target | two comments only |
| `git diff-tree --cc --name-only` on the merge, and the word diff of both ledger fragments against each parent | seven paths differ from both parents; the fragments change in hashes only |
| `bin/evidence-check --strict .` at the target | exit 0, 0 drifted, 0 broken, 0 refused |
| `bin/correction-check --range origin/release/v0.19.0...HEAD` | exit 0, no marker dropped; no released ledger file changed |
| `git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md` | empty |
| `bin/test` on the six modules the merged files feed (one word one meaning, rules have one owner, orchestrator acts, pact-check, no passage pasted, released row read again) | 669 passed, exit 0 |
| `chain_check.py --baseline origin/release/v0.19.0` at the target, before round 4 exists | exit 1, and the work item's only line is `Broad gate` reading `not yet` on a pull request judged ready without an event payload; no `Fix of a fix` complaint |
| `round-record new --round 4` from this report, in the scratch clone | exit 0; `Fix of a fix` reads `no`; no stop line and no bound line printed; round-3.md's `Fixes checked by` left at `no fixes to check`; the generator's own chain-check printed only the open round's `Fixes checked by` notice |
| `chain_check.py` in the scratch clone with that `round-4.md` committed | exit 1, and the work item's lines are the open round's three: `Fixes checked by` not yet, `Pass` unchecked, `Broad gate` not yet; no `Fix of a fix`, floor or `Reframed` complaint |
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
| round-3 | `skills/code-review/scripts/round_record.py:2259` | round 3's 🟡 1 — deferred |
| round-3 | `skills/code-review/scripts/round_record.py#range_carriers` | round 3's 🟢 — confirmed |
| round-3 | `skills/code-review/scripts/round_record.py#names_a_file` | round 3's 🟢 — confirmed |
| round-3 | `docs/round-record-spec.md:698` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md` | round 3's 🟢 — confirmed |
| round-3 | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/rounds/round-2.md` | round 3's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
