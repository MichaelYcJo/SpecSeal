# Round 4 report — 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer

| Field | Value |
|---|---|
| Target SHA | 3fa1f5bc01441a176fa0cdf7774f8423f1f4189f |
| Base | `origin/release/v0.19.0` (4b363e68, the merge's second parent) |
| Pull request | #828, labelled `chain: reframed` |
| Round kind | finding round, the first of the redesign's run — phases 5 and 6 (`ba4957f9..c6d8580c`) and the merge at the target |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

The redesign does what the reframed spec asks for every `Location` shape
the three earlier rounds met. A name with no `.py` path lands nowhere
whatever stands beside it, and a path with a line, a unit or a class method
lands in its top-level unit. The four readings the spec names are gone from
the code. Q6's replay reproduces at the target: 26 work items stop, all at
round 3, and #814 and #801 read first and then second (executed).

Three findings remain. Two are in the reading and one is in a test:

```
location_units ── the one reading landings now keeps
   ├─ 🟡 1  a bare `#name` after a path still lands, through the LAST path
   │        the cell resolved — a fourth form, and it reads prose
   └─ 🟡 2  a path with a `\` separator is cut to its tail, so a path the
            tree does not hold lands in a same-named file elsewhere
test module
   └─ 🟡 3  the case that pins "the redesign starts the count at `no`"
            locates its finding by a bare name, which since the reframe
            never lands, so it passes with the guard removed
```

### 🟡 1 — a `#name` after a path lands through the last path the cell resolved

The spec says a finding lands only through a `.py` path its own `Location`
carries, written as `path:line`, `path#unit` or `path::unit`. A name with
no path lands nowhere, "whatever is written beside it" (`spec.md` §Scope,
S5). The owner says the same (`skills/code-review/orchestration.md`: "It
reads no prose to decide which name in a cell is the place"), and so do
ledger row A8 and the changelog fragment.

`landings` keeps every pair from `location_units` whose path is not None
(`skills/code-review/scripts/round_record.py:2437`). One reading in
`location_units` gives a path to a name that carries none.
`FRAGMENT_RE` matches any `#name` that does not follow a word character, a
`.`, a `-`, a quote or a `#`. It pairs the name with `last`, the path of the
last `path#unit` match anywhere in the cell
(`skills/code-review/scripts/round_record.py:3982`). So:

- `` `mod.py#v`; see #w `` reads `first — 🟡 1 at mod.py#w, a unit round-1's fixes added`. The `#w` is prose.
- `` `f.py#x` and `#w`, beside `mod.py#v` `` reads the same. The writer's `#w` follows `f.py`; it is paired with `mod.py` because that path came last.
- `` `mod.py:9` and `#u` `` reads `no`, because a `path:line` never sets `last`.

All three were executed at the target. This is the shape the reframe
removed: a name placed by what stands beside it. Here the thing beside it is
a path instead of prose. The corpus carries the form once, in a round-1
report at `v0.18.0` (`settle.py#RULE_BASE_HEADING`, `#report`, `#retire`,
`#main`). A round 1 never lands, so dropping the form changes no stop. Q6's
replay with the fix applied still stops the same 26 work items (executed).

Why it matters: the documents, the ledger and the changelog each say no prose
is read. A `#name` anywhere in a cell is read, and it can land in a file it
does not follow. It would cost a framer segment on a cell nobody wrote as
that place.

### 🟡 2 — a path with a Windows separator lands through its tail

`LOCATION_UNIT_RE` and `LOCATION_LINE_RE` capture `[\w./-]+\.py`, which
stops at a `\`. `` `pkg\mod.py:5` `` is captured as `mod.py`. `resolve_path`
then accepts the one tracked path that ends in it. The tree in the probe
holds `mod.py` and not `pkg/mod.py`. So `` `pkg\mod.py:5` `` reads
`first — 🟡 1 at mod.py#u`, and `` `pkg/mod.py:5` `` reads `no` (both
executed). The spec reads a path as one that "the tree tracks at the
target" and lists "beside a path the tree does not hold" among what lands
nowhere. A path the tree does not hold, written with a `\`, lands.

The corpus has no `Location` with a backslash before `.py` at any of the
four tags or at the target (executed). A wrong landing needs the written
directory to be absent and the basename to be held once elsewhere. The fix
below closes it in the regexes. It makes every `\`-separated path land
nowhere, including `` `.\mod.py:5` `` that lands correctly today, and that is
the permissive direction the spec chose for an unplaceable `Location`.

Residue, read and not fixed by the fence: a path with a space,
`` `sp ace/m.py:5` ``, is captured from `ace/m.py` and reads `no` (executed).
If the tree also held `x/ace/m.py`, the tail would resolve there. No regex
can tell a space inside a path from the one before it, and the tree in this
repository holds no tracked path with a space.

### 🟡 3 — the redesign's "count starts at `no`" case no longer catches its defect

`test_a_reframed_record_is_written_and_starts_the_count_at_no`
(`tests/test_a_fix_of_a_fix_is_counted.py:536`) is the case for S7's second
arm. Its `touched` parameter puts a commit that changes `u` inside the
stopped round's range. It asserts that the redesign's first record still
reads `no`, which is what the guard
`previous_pair == stopped` in `build` exists for. Its finding is located at
`` `u` ``. Before the reframe a bare `u` landed. Since phase 5 it lands
nowhere, so the row reads `no` whether or not the guard exists.

Executed in the scratch clone: with the guard disabled
(`if False and previous_pair …`), both parameters pass, `2 passed`. With
the location changed to `` `mod.py#u` `` and the guard still disabled,
`touched=True` fails (`assert 'first — 🟡 1 ...fixes changed' == 'no'`).
With the guard restored, both pass. Phase 5 rewrote two `u` locations to
paths and left this one.

## Answered and confirmed

- **The four readings are gone.** `git grep` over every `.py` file at the
  target finds `names_a_file`, `range_carriers`, `CELL_WORD_RE`,
  `PATH_TAIL_RE` and `TRACKED_FILES` only in two comments that name them for
  the records (executed).
- **Every shape the prompt names, at the target** (executed, one probe):
  - a path in a code span or bare (`mod.py:5`, `mod.py#u`) lands;
  - `./mod.py:5`, `mod.py#u@<hash>` and `mod.py:5-6` land;
  - a class method as `c.py::C::m`, `c.py#C.m` or `c.py:3` lands on `C`;
  - `c.py::C::n`, a method the fix did not touch, also lands on `C`, which is
    the unit grain the spec chose;
  - a name beside its path without a unit (`` `mod.py`, in `u` ``,
    `mod.py u`) reads `no`;
  - a link or a URL ending `mod.py#L5` reads `no`.
- **A path the range deleted** (`f.py:1` after the fix removed `f.py`) reads
  `no`. A path renamed by the fix lands. A unit the fix only moved
  (`git mv mod.py pkg/mod2.py`, `u` unchanged) reads `first … added`, because
  `touched` treats a renamed file's units as new, and the record's
  `New units` names them the same way. That matches the spec's "named by
  round K-1's `New units`". The false-stop exposure belongs to how
  `New units` reads a rename, which this work did not change.
- **Two paths in one cell** both land: `` `mod.py#u` and `mod.py#w` `` gives
  two `;`-separated landings. `` `f.py#x`, which calls into `mod.py#u` ``
  lands on `u` although the place is `f.py#x`. The spec reads every path the
  cell carries, so this is compliant. The corpus holds 14 distinct fix-owing
  cells with two or more `.py` coordinates at `v0.18.0`, 1 at `v0.18.2` and
  none since (executed). Q6's 26 already includes whatever they did.
- **Q6 reproduces.** A bare clone with the 138 pull request heads and the four
  tags, `landings` at the target, closed fix verdicts reopened as the round-1
  reviewer did: 122 records have a previous record, 119 resolve, 36 work
  items reach `first`, **26 reach `second`, all at round 3**. #814 reads
  `first` at round 2 (`compare_at_base`, `proof_refused`, `COMPANY`) and
  `second` at round 3 (`proof_refused`). #801 reads `first` at round 2 and
  `second` at round 3, in `reverify` (executed).
- **The count, the floor, the bound and the depth restart past the stop.**
  This report run through `round-record new --round 4` in the scratch clone
  wrote `Fix of a fix | no`. Round 3 is `stopped`, so `landings` is not
  asked. The printed bound and `chain_check.py` over the clone with that
  `round-4.md` in place both said nothing of round 3's floor or count (see
  the probe table). The depth reset is
  `test_the_depth_restarts_at_a_stop`, which passed in the module run.
- **The merge at the target.** git resolved it without conflict. The files
  that differ from both parents are the two ledger fragments, three documents
  and `chain_check.py`, which both work items edited. The fragments' changes
  are hash re-stamps only: 9 coordinates in #822's fragment and 11 in this
  work item's, with no claim text changed. `evidence-check --strict .` exit 0.
  `correction-check --range origin/release/v0.19.0...HEAD` exit 0, no marker
  dropped. The freeze diff over `seal/releases` and `seal/ledger.md` is
  empty. The six modules the merged files feed pass: 669 passed (all
  executed). The re-stamps in #822's fragment carry no note naming this
  merge; their date cells already read 2026-10-06 and the commit message
  records the re-read.

## Regression tests to plant

- `tests/test_a_fix_of_a_fix_is_counted.py`, S5's parameter list: the two
  fragment shapes and the backslash shape in the fences below. All three read
  `first` at the target and `no` with fixes 1 and 2 applied (executed).
- The same file, the reframed case: the location `` `mod.py#u` ``, red with
  the guard disabled (executed).

## Facts for the evidence ledger

- A8's sentence "No prose is read to decide which name is the place" is true
  only once 🟡 1's fix lands. A8 should then cite S5's two new fragment
  parameters beside its anchors.
- A1 names the three forms. Once 🟡 1 is fixed it is true as written. If the
  fix is taken the other way, by documenting the fragment form instead of
  removing it, A1, the spec, the owner and the changelog each need the
  fourth form named.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A bare `#name` after a path still lands, paired with the last path the cell resolved: a fourth form the spec does not name, and one that reads prose (`see #w`) and can land in a file the name does not follow | `skills/code-review/scripts/round_record.py:2437` | open | executed: `mod.py#v` then `see #w`, and `f.py#x` then `#w` beside `mod.py#v`, both read `first … mod.py#w` at the target and `no` with the fenced fix; the corpus holds one fragment cell, in a round-1 report; Q6 with the fix still 26 |
| 🟡 2 | A path written with a `\` separator is cut to its tail, so a path the tree does not hold lands in a same-named file elsewhere | `skills/code-review/scripts/round_record.py:2938` | open | executed: `pkg\mod.py:5` reads `first` and `pkg/mod.py:5` reads `no` at the target; both `no` with the fenced fix; no backslash `.py` cell in the corpus; a path with a space misses (permissive), read |
| 🟡 3 | The case pinning that the redesign's first record reads `no` locates its finding by a bare name, which never lands since the reframe, so it passes with the guard removed | `tests/test_a_fix_of_a_fix_is_counted.py:536` | open | executed: guard disabled, 2 passed; location `mod.py#u` with the guard disabled, `touched=True` fails; guard restored, 2 passed |
| 🟢 | round 3's yellow finding 1 is answered by the redesign — a basename held twice, a path not held, a quoted path and a path before an apostrophe each read `no` | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_location_that_lands_in_no_written_unit_reads_no` | confirmed | executed: the module at the target, 82 passed with the gate's module; the four shapes are S5 parameters |
| 🟢 | round 3's sentence correction 2 is answered — the carrier sentence left `docs/round-record-spec.md` with the reading | `docs/round-record-spec.md` | confirmed | read: phase 5's diff of the field section; the file is 992 lines |
| 🟢 | the four readings are gone and only comments name them | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: `git grep` over `*.py` at the target |
| 🟢 | a `.py` path with a line, a unit, a class method, `./`, `@hash` or a line range lands, in a code span or bare; a name beside a path without a unit does not | `skills/code-review/scripts/round_record.py#location_units` | confirmed | executed: the shape probe, 34 cases |
| 🟢 | Q6's replay reproduces — 26 stops at round 3, #814 and #801 first then second | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | executed: 119 of 122 records resolve with 138 pull request heads |
| 🟢 | the redesign's first record starts the count at `no`, and the run's floor and bound restart past the stop | `skills/code-review/scripts/round_record.py#build` | confirmed | executed: `round-record new --round 4` and `chain_check.py` in the scratch clone; the depth reset by its own case |
| 🟢 | the merge of the release branch holds — re-stamps only, the ledger checks pass, no correction dropped, the freeze untouched | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | executed: evidence-check, correction-check, the freeze diff, six merge-touched modules 669 passed |
| 🟢 | a unit a fix pass only moved reads `added`, as `New units` reads it | `skills/code-review/scripts/round_record.py#touched` | confirmed | executed: `git mv` in the fix, `pkg/mod2.py#u` reads `first … added`; compliant with the spec's `New units` clause |

## Paste-ready fixes

### 🟡 1 — a fix-of-a-fix landing reads only the path-carrying forms

`skills/code-review/scripts/round_record.py`, the signature and the body of
`location_units` (the depth walk's call is unchanged):

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

The loop in `landings`:

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

Two parameters for S5 in `tests/test_a_fix_of_a_fix_is_counted.py`, after
`"bin/tool's `u`",`:

```python
        # Round 4's yellow 1: a `#name` fragment borrows the last path the
        # cell resolved, so it is placed by what stands beside it.
        "`mod.py#v`; see #w",
        "`f.py#x` and `#w`, beside `mod.py#v`",
```

### 🟡 2 — a path starts at a boundary, never after a `\`

`skills/code-review/scripts/round_record.py`, the two regexes. The
lookbehind stops the capture from starting inside a longer path, so
`pkg\mod.py` is no `mod.py`:

```python
LOCATION_UNIT_RE = re.compile(r"(?<![\w./\\-])([\w./-]+\.py)(?:#|::)([A-Za-z_]\w*)")
LOCATION_LINE_RE = re.compile(r"(?<![\w./\\-])([\w./-]+\.py):(\d+)")
```

And one S5 parameter beside the two above:

```python
        # Round 4's yellow 2: a path the tree does not hold, with a Windows
        # separator, is not its basename.
        "`pkg\\mod.py:5`",
```

With fixes 1 and 2 applied in the scratch clone,
`tests/test_a_fix_of_a_fix_is_counted.py`,
`tests/test_the_chain_goes_back_to_its_framer.py`,
`tests/test_a_fix_pass_may_add_a_unit.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_fixes_name_their_surface.py` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py` gave 306 passed.
Q6's replay gave 26 stops (both executed).

### 🟡 3 — the reframed case locates its finding by its path

`tests/test_a_fix_of_a_fix_is_counted.py`, in
`test_a_reframed_record_is_written_and_starts_the_count_at_no`:

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1, a `#name` fragment lands through the last path the cell resolved; 🟡 2, a backslash-separated path lands through its tail; 🟡 3, the reframed case no longer sees the guard it pins

Loses a record or crashes: no

## Proof block

Opened in the scratch clone at the target: `skills/code-review/scripts/round_record.py`
(the comment above `fof_count_of`, `current_run`, `reframed_after`,
`unit_dumps`, `fix_pass_units`, `landings`, `fix_of_a_fix_value`,
`stop_line`, `build`'s run and stop block, the location regexes, `touched`,
`top_units`, `enclosing_unit`, `measure`, `tracked_at`, `resolve_path`,
`location_units`) and its phase-5 diff;
`tests/test_a_fix_of_a_fix_is_counted.py` (whole) and its phase-5 diff;
`tests/test_the_record_is_generated.py` (`write`, `commit`, `declared`,
`report`, `generate`); `tests/test_the_fixes_close_the_record.py` (`close`,
`fix_table`); `bin/test`; `.github/workflows/hygiene.yml` (the chain-check
step); the phase-5 diffs of `agents/warden.md`, `docs/round-record-spec.md`
and `skills/code-review/orchestration.md`; the work item's `spec.md`,
`routing.md`, `phases/phase-5.md`, `phases/phase-6.md`, `questions.md` (Q1
to Q6), `changelog.md` and `rounds/round-3.md`; ledger rows A1 and A8; the
merge's combined diff of both ledger fragments; `seal/config.md`.
