# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — review round 1

| Field | Value |
|---|---|
| Target SHA | 0ff4e3e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | #403 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Contract changes | none |
| New units | PAIR_BOTH_FIXED (depth 1); ONE_INSIDE_ONE_OUTSIDE (depth 1); one_finding_inside_one_earlier_unit (depth 1); test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one (depth 1); CONFIRMATION (depth 1); test_a_row_that_commissions_nothing_does_not_stop_the_reach (depth 1); test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused (depth 1) |
| Needs a fix | yes — findings 1 and 2, the two reachable states where `close` refuses a pair of records the generator itself wrote; and findings 3 and 4. |
| Loses a record or crashes | no — every refusal above lands with nothing on disk changed, which is the property `close` is built around. |

- [x] Pass

## What this round was asked

Review the whole branch against `spec.md`'s S1–S16, spec compliance before
quality. The acceptance rows are written as states that are green today and
must go red, so they are checked in that shape rather than as a list of edits.

Three things the builder disclosed were to be **verified rather than taken**:
the record corpus carried as 176 and re-measured to 211; a unit name
`SUMMARY_WORDS` <!-- NAME NOT IN TREE: the name this round was asked to check FOR absence; it exists in no branch of this repository --> that `spec.md` cites and the tree does not hold; and a
docstring measurement re-taken against the four conditions `plan.md` sets for
it — population named exactly, the date, the reader it was taken through, and
all three figures of the sentence re-derived in one pass.

Two runs the orchestrator had already executed were named so the round would
not spend itself on them: the `seal` module at HEAD, and the mutation of the
`round-record: sealed` literal.

Named risks: §15, a case not seen red; §14, a refusal message a person acts
on; a citation that does not resolve, searched whitespace-normalised and
case-insensitive because a case-sensitive search had already produced one
wrong conclusion in this work item's history; and §12, the class — two
`_real_records` copies and a third corpus reader.

The broad gate was forbidden. `agent-contract` §2 assigns the full suite, the
repository-wide lint and the typecheck to `agents/sealer.md`, once, after the
rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `close` refuses a generated pair whenever the round carries a row that commissions nothing | `skills/code-review/scripts/round_record.py#reach_forward` `:1535` | **fixed** `df404e2` | fixed at df404e2 — the map is keyed from every verdict row, built beside `words` so no inserted line has shifted the indices; Executed: exit 2, nothing written, on records `new` itself wrote. The shape is the one `agents/warden.md` instructs reviewers to use, and the corpus holds 25 of them |
| 2 | 🔴 `close` refuses when an earlier round already claimed every coordinate this round opened | `skills/code-review/scripts/round_record.py#reach_forward` `:1552` | **fixed** `df404e2` | fixed at df404e2 — the empty-fill refusal is silence, and `reach_forward`'s docstring and `templates/sdd-round.md` say why; Executed: exit 2, nothing written. `inherited_rows` is first-seen-wins across rounds, and the refusal states a rule about `new` without that qualifier |
| 3 | 🟡 the file-level fallback fires where the adder resolved, and the message says it did not | `skills/code-review/scripts/round_record.py#depth_two` `:3487` | **fixed** `df404e2` | fixed at df404e2 — a unit whose adder resolves to no candidate row is depth 1; resolving to several still takes the fallback, which the round's own paste-ready skipped; Executed: a depth-1 unit refused. Contradicts `docs/review-chain-spec.md:1274`, written in this branch |
| 4 | 🟡 a case comment names `seal/follow-up.md` as the home of a defect that file does not carry | `tests/test_the_fixes_close_the_record.py:1252-1253` | **fixed** `df404e2` | fixed at df404e2 — the comment names the `# RIDER:` at `round_record.py#units_named_earlier`; Read: no occurrence in that file, and the branch never touched it. The real home is the `# RIDER:` at `units_named_earlier` |
| ⬜ 5 | `unit_adders` runs before the guard that would skip it | `skills/code-review/scripts/round_record.py:3622` | **fixed** `df404e2` | fixed at df404e2 — `depth_two` takes the pass, not its result, so its own guard runs first; Read: 127.8 ms paid on every round-1 `close`, where `depth_two` returns at once. Numbered because it does commission the one-line move under `## Paste-ready fixes` — fixed in passing or not at all, and ⬜ is never counted by `Needs a fix` |
| ⬜ | two frame documents keep the corrected corpus figure | `seal/specs/1789425391-…/plan.md:21`, `spec.md:143` | answered | Read: both say 176; measured 211 of 212. **No id, because it commissions nothing a fix pass may do** — `plan.md` and `spec.md` are the framer's files. It is a line for the closing memo, and `overview.md`'s divergence table already carries the correction with its grounds |
| 🟢 | S1–S7 and S9–S16 confirmed | the modules named in `plan.md`'s Verified-by column | answered | Executed — the narrow run and seven mutations above. A confirmation this round verified and did not open, so it takes no id |
| 🟢 | the three build disclosures confirmed | `round_record.py#says_open`'s docstring; `spec.md:138`; `overview.md:19` | answered | Executed — the corpus re-measured in one pass, and the name searched over every branch. A confirmation, so it takes no id |

## Paste-ready fixes

```python
    # Every verdict row, not only the numbered ones. `inherited_rows` writes
    # one row per `Location` cell of every row -- a confirmation, an earlier
    # round's closure carried forward, a `?` out of verified scope -- and
    # `rows` holds only what `finding_number` keyed. Reading the map from
    # `rows` refused a pair of records this generator itself wrote.
    location = VERDICT_HEADER.index("Location")
    number = VERDICT_HEADER.index("#")
    now = {}
    for i, cells in table_body(reader, reader.readable("\n".join(raw)),
                               VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) > VERDICT_COL and seen[location]:
            now[seen[location]] = (
                seen[number],
                chain.verdict_of(seen, VERDICT_COL),
            )
    forward = reach_forward(reader, rounds, args.round, now)
```
```python
    if not filled:
        # NOT a refusal. `inherited_rows` is first-seen-wins across rounds,
        # so a round whose every coordinate an earlier round already claimed
        # is written into this section under that earlier round and under no
        # other. A re-review round looking again where the round before it
        # looked is the ordinary case, and refusing it stops the run this
        # reach exists to keep truthful.
        return None
```
```python
CONFIRMATION = "| 🟢 | round 0's finding, re-read | `README.md` | verified | read |\n"


def test_a_row_that_commissions_nothing_does_not_stop_the_reach(repo):
    """Finding 1. `inherited_rows` writes a row per `Location` cell of EVERY
    verdict row; `close` keyed its map from the numbered ones. A round
    carrying a confirmation -- the shape `agents/warden.md` asks for, and 25
    of the committed corpus -- then could not be closed at all."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1 + CONFIRMATION))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    a = commit(repo, "round 2")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, _ = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    why = inherited(repo)
    assert why["`mod.py#helper`"] == f"round 1's 🔴 1 {chr(0x2014)} fixed", why
    assert why["`README.md`"] == f"round 1's 🟢 {chr(0x2014)} verified", why


def test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused(repo):
    """Finding 2. Round 2 opens a finding where round 1 opened one, so round
    3's section carries the coordinate under `round-1` and nothing under
    `round-2`. That is silence, not a malformed record."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    a1 = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b1 = commit(repo, "round 1's fix")
    close(repo, 1, fix_table(f"| 1 | fixed | {b1[:7]} |\n"), f"{a1}..{b1}")
    commit(repo, "round 1 closed")
    code, out, _ = generate(
        repo, n=2,
        report_text=report(
            verdicts="| 🟡 1 | helper still drops b | `mod.py#helper` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    commit(repo, "round 2")
    code, out, _ = generate(
        repo, n=3,
        report_text=report(verdicts="| 🟡 1 | a third look | `mod.py:5` | open | read |\n"),
    )
    assert code in (0, 1), out
    a = commit(repo, "round 3")
    write(repo, "mod.py", MOD_CHANGED + "\n\ndef extra():\n    return 1\n")
    b = commit(repo, "round 2's fix")
    code, out, _ = close(
        repo, 2, fix_table("| 1 | answered | grounds |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "Inherited coordinates" not in out, out
```
```python
    for (f, name), rows_for in candidates.items():
        resolved = set(adders.get((f, name), ()))
        owners = sorted(resolved & set(rows_for))
        if len(owners) == 1:
            unit, record_n, cell_text, location = rows_for[owners[0]]
            lines.append(
                f"`{name}` in {f} would be at depth 2: added by the fix of "
                f"{cell_text}, whose Location `{location}` is inside `{unit}`, "
                f"a unit round-{record_n}.md's `{chain.NEW_UNITS}` names."
            )
            continue
        if resolved:
            # The range DID resolve the adder, to a row that sits inside no
            # unit an earlier record names. The unit is at depth 1 and this
            # rule has nothing to say about it -- #333's quiet direction,
            # where the file-level walk named every unit in the file against
            # whichever candidate it reached. Only an UNRESOLVED unit takes
            # the file-level sentence below.
            continue
        every = "; ".join(
            f"{cell_text} (inside `{unit}`, round-{record_n}.md)"
            for _n, (unit, record_n, cell_text, _loc) in sorted(rows_for.items())
        )
        lines.append(
            f"`{name}` in {f} would be at depth 2, and the attribution is "
            f"FILE-LEVEL: the range does not resolve which fix added it, so "
            f"every fix inside an earlier unit in {f} is a candidate — {every}."
        )
    if not lines:
        return
```
```python
def test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one(repo):
    """#333's quiet direction. Round 1 names `alpha` only; finding 2 sits
    inside `beta`, which no earlier record names, and finding 2's commit is
    what adds the unit. The range resolves that, so the unit is depth 1 and
    the walk says nothing -- where the file-level answer refused it and the
    fallback message claimed a non-resolution that did not happen."""
    a = one_finding_inside_one_earlier_unit(repo)
    write(repo, "pair.py", PAIR_ALPHA_FIXED)
    c1 = commit(repo, "finding 1's fix, adding nothing")
    write(repo, "pair.py", PAIR_BOTH_FIXED + BETA_GUARD)
    c2 = commit(repo, "finding 2's fix, adding the unit")
    code, out, _record = close(
        repo, 2,
        fix_table(f"| 1 | fixed | {c1[:7]} |\n| 2 | fixed | {c2[:7]} |\n"),
        f"{a}..{c2}",
    )
    assert "depth 2" not in out, out
    assert code == 0, out
```
```python
# of its own, outside this work item's six tickets, and it is written up in
# the stamped `# RIDER:` at `round_record.py#units_named_earlier` rather than
# repaired here.
```
```python
        lambda: unit_adders(reader, root, fixes),
```
```python
    named = units_named_earlier(reader, earlier)
    if not named or not added:
        return
    adders = adders() if callable(adders) else (adders or {})
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py tests/test_chain_check_at_the_pull_request.py tests/test_the_reopening_is_one.py tests/test_the_rules_have_one_owner.py -q` in the clone at `0ff4e3e` | 249 passed, 1 skipped, exit 0 |
| Mutation: `OPEN_BOUNDARY` borrowed from `chain.SEPARATORS` | exit 1 — the boundary and the coupling cases red; restored, tree clean |
| Mutation: the verdict-column arm disabled | exit 1 — 10 failed / 58 passed; all six no-commission shapes and all four spellings red |
| Mutation: `seal` back to shape-only on `Fixes checked by` | exit 1 — the `round-N` refusal cases red |
| Mutation: `depth_two` attribution back to the first candidate row | exit 1 — the naming case red |
| Mutation: both `failures.extend(errors)` in `tests/test_chain_check_at_the_pull_request.py` replaced with `pass` | exit 1 — the positive control red |
| Mutation: `reach_forward` returns `None` unconditionally | exit 1 — the two-records case red |
| Control: the same six selections unmutated | 5 / 4 / 5 / 1 / 1 / 1 passed, exit 0 each |
| Corpus re-measurement through the module's own readers (probe, deleted) | every shipped figure reproduced; see above |
| Probe: round 1 carrying one numbered row and one confirmation row, `new --round 2`, then `close --round 1` (deleted) | exit 2, refused — 🔴 1 |
| Probe: round 2's only finding at round 1's coordinate, `new --round 3`, then `close --round 2` (deleted) | exit 2, refused — 🔴 2 |
| Probe: one finding inside an earlier unit, the other outside, the outside one's commit adding the unit (deleted) | exit 2, refused a depth-1 unit — 🟡 3 |
| Ledger drift over `seal/ledger.md` and this work item's fragment, through the checker's own reader | 1214 rows and 40 rows, 0 not OK |
| Name scan over the work item's twelve documents and its ledger fragment, through the checker's own reader | 0 names the tree does not carry |
| The broad gate — full suite, repository-wide lint, typecheck | **not yet** — `skills/agent-contract/SKILL.md` §2 assigns all three to `agents/sealer.md`, spawned after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `chain.EMPHASIS` strip reaching no snake_case parent, so the depth-2 walk reaches no Python unit whose name carries an underscore | already deferred in the build — a stamped `# RIDER:` at `round_record.py#units_named_earlier`, named in `overview.md` §*Not verified* | the repository owner |
| Whether `no fixes to check` beside a fix-surface row reading *none — the fixes are not yet written* should be refused | already deferred — Q1, answered **(a) leave it open** by the owner before the build | the repository owner, in 0.12.0 beside #174 |
