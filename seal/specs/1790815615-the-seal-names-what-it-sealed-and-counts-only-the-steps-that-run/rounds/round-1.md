# 1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run — review round 1

| Field | Value |
|---|---|
| Target SHA | 512f6a89ee82d20f0b8588fdc0c9cf60a06553ae |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 699 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (counts and homes elided against Q1), 🟡 2 (a home read as its first word), 🟡 3 (the coverage base unpinned, #638 rewrites that line), 🟡 4 (the gate row's third arm missing from three documents) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 targets `512f6a89` and the diff `cd24f516..512f6a89`, the whole build. The change alters what a person reads on every seal, so the round was asked to check stage 1 against `spec.md` S1–S6 and A1–A18 and the approved plan, then to attack seven things:
1. The names on the `SEALED` and `NOT SEALED` heads, and that the `Broad gate` cell is unchanged.
2. The panel: the width, the cut side, the conditional rows, the new environment variable, `SAMPLE_ROWS`, and the failure form's `total:` line.
3. `rounds`: `capped` and the deferred homes, read through `chain_check`'s own readers.
4. `workflow`: `ONLY_AT_MAIN` against the workflow guards, and the two counts.
5. When the uncommitted-cell line prints.
6. The ledger's 28 re-stamped rows, six corrected in place, and the two kept survivors.
7. The class: every document naming a moved panel row, `13 steps`, or the old head shape.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the suite's counts and the deferred homes are elided at the frame, where the owner's Q1 answer says a long value continues beneath its label; two real records lose homes (`4 deferred -> #673, ...`, `4 deferred -> #611, ...`) | `skills/verify/scripts/broad_gate.py:2555` | open | `questions.md` Q1's answered default; executed over the tree's 36 work items; the width case pins the elision at `tests/test_the_seal_is_taken_once_by_the_sealer.py:2883` |
| 🟡 2 | a deferral's home is the first word after `deferred`, so `— issue #97 …` reads `issue`, `phase 9 of this branch` reads `phase`, `to #664` reads `to`, `→ #664` reads a non-ASCII `→` | `skills/verify/scripts/broad_gate.py:2366` | open | executed over every `round-N.md` in the tree (four rows) and over typed shapes; `verdict_of` accepts all of them as homed |
| 🟡 3 | the coverage line's base is unpinned through the gate: dropping it survives the gate modules and makes the release-base line say `answers 5` over two arms that did not run; #638's hunk rewrites that line with one argument | `skills/verify/scripts/broad_gate.py:2713` | open | mutation executed (281 passed); line compared for `main` and `None` (executed); #638's hunk read; trial merge executed |
| 🟡 4 | `docs/the-broad-gate.md`, `agents/sealer.md` and the section comment state the `gate` row's condition without the no-invoked-path arm, which fires on every seal of the 0.17.0 run under the installed 0.16.0 copy | `docs/the-broad-gate.md:106` | open | `gate_copy` returns the row where `installed` is None (read; `test_the_gate_row_prints_only_where_the_copy_that_ran_is_not_the_one_invoked` asserts it); the 0.16.0 copy sets no variable |
| ⬜ 5 | the changelog fragment carries 🟡 4's two-arm sentence | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/changelog.md:11` | open | paperwork; goes with 🟡 4's fix |
| 🟢 | the `Broad gate` cell is `<sha> against <sha>` as before and `chain_check` reads it unchanged | `skills/verify/scripts/broad_gate.py:2616` | confirmed | outside every hunk; `round_record.py` and `chain_check.py` not in the diff |
| 🟢 | `SPECSEAL_BROAD_GATE_INVOKED_AS` reaches no check and no child gate | `skills/verify/scripts/broad_gate.py:3047` | confirmed | read: fresh `env` for the child, popped before `gate()`; both channel cases green |
| 🟢 | `ONLY_AT_MAIN` is held both ways, and `4 of 9` and `8 of 11` come from the real workflow | `tests/test_the_gate_names_every_step_ci_runs.py:1100` | confirmed | executed: module green; the flipped-guard arm shows the case can fail |
| 🟢 | the uncommitted-cell line prints only over an uncommitted record and never in local mode, on a red run or on a refusal | `skills/verify/scripts/broad_gate.py:2911` | confirmed | probed in a scratch repository in both modes; red and refusal return earlier (read) |
| 🟢 | the ledger's corrections and re-reads are true of the target | `seal/releases/0.15.1.md` | confirmed | `evidence-check .` and `--strict .` exit 0 (executed); each note read against the code |
| ❓ | whether the installed 0.16.0 hook draws a file the new gate writes, on screen | `hooks/sealer-stamp.py` | ❓ out of verified scope | no case can see a screen; `questions.md` Q3 names the owner as its answerer, on the first real 0.17.0 seal |

## Paste-ready fixes

```python
def wrapped(label, value, sep=", "):
    """`value` on as many panel rows as it needs, broken after `sep`: the
    first row under `label`, the rest as `""` rows beneath it, which is what
    the owner chose over a wider panel (`questions.md` Q1). A list of counts
    or homes continues; only one part wider than the frame is still elided,
    by `fit`, with the marker (#666)."""
    out, line = [], ""
    for part in str(value).split(sep):
        joined = f"{line}{sep}{part}" if line else part
        if line and len(joined) > PANEL_VALUE_WIDTH:
            out.append(line + sep.rstrip())
            line = part
        else:
            line = joined
    out.append(line)
    return [(label if i == 0 else "", fit(row)) for i, row in enumerate(out)]
```
```python
    rows += (
        [*wrapped(SUITE, counts), ("", exit_row)] if counts else [(SUITE, exit_row)]
    )
```
```python
    if count:
        tail = f" -> {', '.join(homes)}" if homes else ""
        rows.extend(wrapped("", f"{count} deferred{tail}"))
```
```python
    at = next(i for i, row in enumerate(rows) if row and row[0] == "rounds")
    beneath = " ".join(value for _label, value in rows[at + 1 :])
    for home in ("seal/follow-up.md", "#12345", "#12346"):
        assert home in beneath, beneath
    assert "67890 skipped" in " ".join(values), values
```
```python
# What a home looks like inside a deferral's prose: an issue, or a path.
HOME_TOKEN = re.compile(r"#\d+|[\w.-]+(?:/[\w.-]+)+|[\w.-]+\.md\b")
# Where a home written as words ends: a spaced dash, or a sentence's stop.
HOME_END = re.compile(rf" [{chr(0x2014)}{chr(0x2013)}-] |\. ")


def deferred_home(chain, cell):
    """The home a `deferred <home>` verdict cell names, or None.

    Read after `chain_check`'s own normalisation (`EMPHASIS`, `MARKER`) and
    separators (`SEPARATORS`), and only for a row `verdict_of` already
    called `deferred`. An issue or a path anywhere in what follows is the
    home, because the tree writes `deferred — issue #97 already holds…` and
    a person types `deferred to #664`; where there is neither, the words up
    to the first spaced dash or full stop are, so `phase 9 of this branch`
    prints whole rather than as `phase` (#666)."""
    s = chain.MARKER.sub("", chain.EMPHASIS.sub("", cell).strip())
    if not s.lower().startswith(chain.DEFERRED):
        return None
    rest = s[len(chain.DEFERRED) :].strip(chain.SEPARATORS)
    if not rest:
        return None
    found = HOME_TOKEN.search(rest)
    if found:
        return found.group(0)
    return HOME_END.split(rest, maxsplit=1)[0].rstrip(".,;")
```
```python
@pytest.mark.parametrize(
    "cell, home",
    [
        ("deferred #664", "#664"),
        ("**deferred** #664.", "#664"),
        ("deferred to #664", "#664"),
        ("deferred → #664", "#664"),
        ("deferred (#664)", "#664"),
        ("deferred — issue #97 already holds this axis", "#97"),
        ("deferred `seal/follow-up.md`", "seal/follow-up.md"),
        ("deferred [#664](https://example.com/664)", "#664"),
        ("deferred phase 9 of this branch", "phase 9 of this branch"),
    ],
)
def test_a_deferrals_home_is_read_whole(cell, home):
    """S4's homes over the shapes the tree's records and a person write: the
    home is an issue or a path wherever it stands, and words where it is
    neither, never the first word alone."""
    gate = gate_module()
    chain = gate.load(gate.RECORD, "specseal_round_record_for_home_case").chain
    assert chain.verdict_of([cell], 0) == chain.DEFERRED, cell
    assert gate.deferred_home(chain, cell) == home
```
```python
    # #666 through the gate: the coverage line is keyed on the base it was
    # given, so at `main` it leaves out the two skipped steps, not the
    # milestone step that runs only into `main`.
    assert (
        "2 more are steps CI skips on a pull request into `main`, so this "
        "count leaves them out."
    ) in result.stderr, result.stderr
```
```python
def unanswered(text, given):
```
```python
def coverage_line(text, given):
```
```markdown
that breaks an arm and passes itself, is named rather than dismissed: one
stderr line names the running copy's path and reads `tree <version>` or
`plugin <version>`, the panel's `gate` row reads `tree <version>` wherever
the copy that ran is not byte for byte the copy invoked, or where the tree's
copy ran with no invoked copy named to compare against — invoked directly,
or redirected by an installed copy older than #666 — and the pull request
asks the same scripts again. The row prints nowhere else: on every
redirected seal of a tree whose gate the branch did not change it said the
same thing and was read by nobody (#666).
```
```markdown
or `plugin <version>`. The stamp carries a `gate` row only where the copy
that ran is not byte for byte the copy you invoked, or where nothing told
it which copy you invoked — the tree's copy run directly, or an installed
copy older than #666: `tree <version>` there means the branch was measured
by the gate it ships, and a stamp with no `gate` row was measured by the
copy you invoked (#666). Quote the gate line
```
```python
# says so; every run's stderr names which copy ran, `tree` or `plugin`, with
# its version, and the panel's `gate` row says `tree <version>` where that
# copy's bytes differ from the one the caller invoked, or where no invoked
# copy was handed over to compare (#666, `gate_copy`). A
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules the diff touches, in the clone | exit 0, 487 passed |
| `bin/evidence-check .` unscoped, then `--strict .` | both exit 0; `total: 3205 ok · 0 drifted · 0 broken` |
| a one-off probe calling `sealed_record`, `rounds_rows`, `pull_request` and `item_value` for each of the 36 work items with round records | no exception; 15 records read `capped`; two deferral rows over 23 columns (`1790645290`, `1790297085`) |
| the same probe reading every deferred row of every `round-N.md` through `verdict_table`, `verdict_of` and `deferred_home` | four rows whose printed home is not their home (🟡 2's table) |
| a one-off probe drawing `panel` over the longest inputs, `sealed_names` over nine shapes, `label` over three values files, `deferred_home` over ten cells, and the uncommitted line in a scratch repository in local and shared mode | as reported above |
| `gate`'s coverage call with `base.given` removed, then the three gate modules | exit 0, 281 passed — the mutation survives |
| 🟡 3's proposed assertion, at the target and then with the mutation | green at the target, red with the mutation; both files restored with `git checkout` |
| `coverage_line` over `hygiene.yml` for `main` and for `None` | `runs 11 … answers 3` against `runs 9 … answers 5` |
| `git merge-tree --write-tree` of the target with `origin/feat/638-the-record-arms-run-before-the-sealer-is-spawned` | conflicts in `skills/verify/scripts/broad_gate.py` and six `seal/releases/*.md` |
| the full suite, repository lint and typecheck (the broad gate) | not yet: not run by this round, and it is the sealer's once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
