# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — review round 1

| Field | Value |
|---|---|
| Target SHA | 302fa30e91ee44e9b8b7d0d1fc01f9093a2b6b94 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #828 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1, a prose `Location` that names a code identifier lands in a Python unit and can stop a run falsely |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Spec compliance first against `spec.md` (the `Fix of a fix` row written by `round_record.py new` from the previous record's fix range at function grain, `first` then `second` within one run; at `second` no fix pass, the open findings closed `deferred the frame`, and the next record refused until `spec.md` ends with a `Reframed` line; `chain_check.fix_of_a_fix` behind `REFRAME_FROM` with its refusal rows; the floor, the bound and the count reading the current run), then quality: every path that decides a landing, attacked (a function renamed, moved, split, or decorated in the fix range; a finding whose `Location` names a line outside any function, a non-Python file, or a file the range deleted; a range that does not resolve after a squash); the run partition at each `second` against chains with zero, one and two reframes; the four divergences in `overview.md`, above all the exclusion of 🟢, ❓ and ⬜ from landing; and Q4: whether the replay's 18 stops in 57 work items are fixes of fixes or false landings, judged by opening a sample of the stopped items' findings against the functions they landed in.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A prose `Location` that names a code identifier in backticks lands in a Python unit of any file the fix range touched, against S5 and §Out | `skills/code-review/scripts/round_record.py:2396` | open | executed: a planted range changing `main` and adding `helper`; `` `docs/x.md:3` — … `main` `` and `` … `helper` `` each landed. Cause is `IDENTIFIER_RE` at `:2907`. No case pins the shape |
| ⬜ 2 | The gate refuses a `first` its run already landed before, but not a `second` with no earlier landing, nor a non-`no` value on a run's first record; an orphan `second` cuts the run | `skills/code-review/scripts/chain_check.py:3933` | open | executed: `runs_of` and `fix_of_a_fix` over planted chains passed all three shapes. Generator never writes them; the next record still needs a reframe |
| ⬜ 3 | `new` refuses an unresolvable previous range even when no row of the report is open, where the row reads `no` whatever the range holds | `skills/code-review/scripts/round_record.py:2373` | open | executed: `deadbeef..cafebabe` with one `answered` row raised `Refused` |
| ⬜ 4 | `frame`'s refusal still says the last non-empty line has to be the `Framed` line, though the foot may now end with `Reframed` lines | `skills/code-review/scripts/chain_check.py:4715` | open | read: `frame_foot` and `frame_mark` against the sentence; contract §14 |
| ⬜ 5 | The overview's unverified row about the 23 records at `v0.18.1` and `v0.18.2` has an answer: they resolve with the pull request heads fetched, and five more work items stop | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/overview.md:28` | open | executed: 119 of 122 records resolve; a records correction, outside `Needs a fix` |
| 🟢 | The ⬜ / 🟢 / ❓ exclusion from landing (overview divergence 4) is justified | `skills/code-review/scripts/round_record.py#landings` | confirmed | read: `OWED_MARKERS`' comment and the findings format's rule that `Needs a fix` never counts a ⬜; executed: a numbered open ⬜ does not land |
| 🟢 | Added units derived from the range's ends equal what `close` writes into `New units` (divergence 2) | `skills/code-review/scripts/round_record.py#fix_pass_units` | confirmed | read: `measure` derives `added` with the same rule over the same ends |
| 🟢 | Renamed, moved, split and decorated units, a method inside a changed class, a deleted file, a module-level line and a re-commented unit each read as the spec says | `skills/code-review/scripts/round_record.py#fix_pass_units` | confirmed | executed: rename and move read `added`, decorate and docstring read `changed`, a method lands at its class, a deleted file and a module-level line land nowhere |
| 🟢 | The run partition holds with zero, one and two reframes, and a missing second `Reframed` line is refused at the record after the second stop | `skills/code-review/scripts/chain_check.py#runs_of` | confirmed | executed: five planted chains |
| 🟢 | S12 holds: #814 and #801 read `first` at round 2 and `second` at round 3 | `skills/code-review/scripts/round_record.py#landings` | confirmed | executed: the corpus replay |
| 🟢 | Q4: of 11 stopped work items opened, 10 are real fixes of fixes, 1 is a fix-written defect from the pass before the previous one, 0 are false | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | read, after the executed replay; the table above |
| ❓ | The depth walk still reads every earlier record's `New units`, across a stop, so the redesign's first fix pass may meet a depth-2 refusal for a unit the stopped run added | `skills/code-review/scripts/round_record.py#units_named_earlier` | ❓ out of verified scope | read only: the spec scopes the reset to the floor, the bound, the count and the cap, and says nothing of depth. Whether the depth should reset at a reframe is the orchestrator's to answer, or the repository owner's |

## Paste-ready fixes

```python
# A file the cell names, of any kind. Beside one, a backticked name is prose
# about that file and never a unit in another (#823 round 1's yellow 1).
NAMES_A_FILE_RE = re.compile(r"[\w./-]+\.(?:py|md|txt|json|toml|ya?ml|cfg|ini|sh)\b")
```
```python
        pairs = location_units(reader, root, target, location, tracked)
        if NAMES_A_FILE_RE.search(reader.visible(location)):
            pairs = [(rel, unit) for rel, unit in pairs if rel is not None]
        for rel, unit in pairs:
```
```python
        # A prose file whose sentence names the unit the fixes changed.
        "`README.md:1`, which describes `u`",
```
```python
def test_a_name_beside_a_file_the_range_did_not_touch_does_not_land(repo):
    """A backticked name beside a path is about that path's file."""
    code, out, text, _ = two_rounds(repo, "`f.py:1`, called from `u`")
    assert code != 2, out
    assert row(text) == "no", row(text)
```
```python
    if count and not earlier:
        errors.append(
            (
                rel,
                0,
                f"`{FIX_OF_A_FIX}` reads `{cell.strip()}` on the first record "
                "of its run, which follows no fix pass of the run: round 1 "
                f"has none, and the record after a `{FOF_SECOND}` follows one "
                f"that closed on deferrals. It reads `{FOF_NO}`",
            )
        )
    elif count == 2 and not landed:
        errors.append(
            (
                rel,
                0,
                f"`{FIX_OF_A_FIX}` reads `{FOF_SECOND}`, and no earlier record "
                f"of this run landed, so the count says `{FOF_FIRST}`. A "
                f"`{FOF_SECOND}` ends the run, and one the run did not count "
                "restarts the floor's walks",
            )
        )
```
```python
    rows = []
    for _number, (_i, cells) in keyed.items():
        seen = [reader.visible(c) for c in cells]
        if chain.verdict_of(seen, VERDICT_COL) in chain.CLOSED_WORDS:
            continue
        label = seen[NUMBER_COL].strip()
        if label.startswith(COMMISSIONS_NOTHING):
            continue
        rows.append((label, cells[LOCATION_COL] if len(cells) > LOCATION_COL else ""))
    # Nothing open lands anywhere, whatever the range holds, so a range this
    # tree cannot resolve decides nothing here.
    if not rows:
        return []
```
```python
            problems.append(
                f"{item}/spec.md does not END with the framer's mark. The "
                "last non-empty line that is not a `Reframed <date> by <who>, "
                "after round <N>.` line has to read `Framed <date> by <who>, "
                "before the build.` — `templates/sdd-spec.md` ships it, and "
                "it is the only evidence in the tree that the framing "
                "happened, because the other framer mark lives in the git "
                "dir and a git dir does not travel here"
            )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_fix_of_a_fix_is_counted.py` and `tests/test_the_chain_goes_back_to_its_framer.py`, at the target in a scratch clone | 56 passed, exit 0 |
| A landings probe, run once and deleted: a planted range and 13 `Location` shapes through `landings` and `fix_pass_units` | 🟡 1 and ⬜ 3 reproduced; the 🟢 shapes above as stated; `fix_of_a_fix_count` reads `no-op` as 0 and a bare `second` as none |
| A run probe, run once and deleted: `runs_of` and `fix_of_a_fix` over eight planted chains | zero, one and two reframes partition correctly; a missing `Reframed` line is refused at the right record; ⬜ 2's three shapes pass |
| A corpus replay, run once and deleted: the shipped `landings` over every round record at `v0.18.0` to `v0.18.3`, with `refs/pull/*/head` fetched into the scratch clone | 119 of 122 records resolve; 26 of 64 work items reach `second`; #814 and #801 as S12 says |
| A docstring measurement over the replay's `changed` landings | 3 of 69 changed in the docstring alone; one is a genuine docstring regression |
| The broad gate — the full suite, the repository-wide lint and the typecheck over the branch | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
