# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — review round 2

| Field | Value |
|---|---|
| Target SHA | 5701141 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | #403 |
| Broad gate | 5ac452e against release/v0.11.5 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round, and the run ends here. Round 1's record answers
`Loses a record or crashes: no` and round 1 closed on a fix, so
`docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*
puts this record at the end: it reads round 1's fixes and ends the run whatever
it finds. The bound was stated first in the spawn, so that anything found would
be opened as an issue rather than chased — `deferred #N`, `no fixes to check`,
`chain: capped`. The one exception named was the floor itself, and it was named
as a different question from wanting a fix.

Round 1's spec-compliance pass was inherited rather than re-run. The round's
work was round 1's five findings and what their fixes did, plus three things
the fix pass reported that round 1's fix table does not carry: the anonymous
`seal` instances repaired with their pin in one commit, the `NAME NOT IN TREE`
marker the orchestrator added to round 1's own asked paragraph, and a shared
ledger clause the fix pass named rather than changed.

Named risks: §15 applied to the fix pass's own three new cases, because a case
planted for a fix and never seen red is this work item's subject one level in;
the fix pass's rejection of round 1's paste-ready for 🟡 3, which is the kind of
answer that is right for a wrong reason; the depth of the seven test-side units,
because a refusal not firing is not evidence; and whether `Contract changes`
should say that an argument now accepts a callable as well as a mapping.

Two runs the orchestrator had already executed were named so the round would
not repeat them. The broad gate was forbidden — `agent-contract` §2 assigns the
full suite, the repository-wide lint and the typecheck to `agents/sealer.md`,
once, after this round.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the widened map is last-wins where `inherited_rows` is first-wins, so two verdict rows at one `Location` carry the wrong row's number and word into round N+1 | `skills/code-review/scripts/round_record.py#close` | deferred #404 | Executed: exit 0, `round 1's 🟢 — verified` written over a coordinate round 1's own record closed `**fixed**`. #342's disease through the repair for it, and the refusal that caught it is gone. 0 of 74 repeated coordinates in the committed corpus are this shape; it is the shape `agents/warden.md` now asks for. Capped run — the fix is in this report and the issue is the home |
| 🟡 2 | the empty-fill refusal became unconditional silence, so a `## Inherited coordinates` table edited after `new` wrote it is accepted at exit 0 | `skills/code-review/scripts/round_record.py#reach_forward` | deferred #405 | Executed: every body row deleted from round 2's section, `close --round 1` exits 0 and writes nothing there; the same input exited 2 before `df404e2`. Read: `chain_check.py` never reads that heading, so this reach is its only reader. A narrower condition is available and runs green |
| 🟡 3 | the new pin refuses `the sealer`, which the rule it names explicitly allows | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1307` | deferred #406 | Executed: the refusal's exit sentence naming the sealer turns this case red while `test_one_word_one_meaning.py` stays green. That sweep skips a hit followed by a letter and says so in its own comment. §12: one occurrence in the tree |
| 🟡 4 | a new fixture rewrites round 1's `New units` row with an unasserted `re.sub`, and the case it feeds asserts only negatives | `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit` | deferred #407 | Read: a miss leaves round 1 naming no unit, `depth_two` returns at its guard, and both assertions hold vacuously. Executed: the case is red against the pre-fix module today, so the substitution does land. The two 🔴 cases in the same commit each carry the guard this one lacks |
| 🟡 5 | the pull-request check reads a row's severity from the whole row, so a 🟢 row quoting an earlier round's 🔴 is failed as a blocking finding — and the message names both severities in one sentence | `skills/code-review/scripts/chain_check.py#open_blocking` | deferred #408 | Executed: `round-record new --round 2` against an earlier draft of this report → *this 🔴 row reads `verified` … : 🟢*. Read: **not branch-caused** — the branch never touched this file and the predicate dates to `2d4a52a`. The refusal is directionally right; the reason printed for it is not. Found by running the generator over this report |
| ⬜ 6 | the ledger's S13 clause leaves a `seal` instance anonymous; it should stay, and the recorded reason is half wrong | `seal/ledger.md` §S13 | answered | Read: `SEAL_SWEPT`'s own comment excludes `seal/` deliberately, so the conclusion holds. Executed: `git log -S` names `3ece7b7`, a commit of this branch, as the writer of the clause — so *outside what a branch may edit in the shared ledger* is not why. Paperwork, and it commissions nothing a fix pass may do |
| 🟢 | round 1's 🔴 1, 🔴 2, 🟡 3, 🟡 4 and ⬜ 5 are closed | `round_record.py` at `#close`, `#reach_forward`, `#depth_two`; `tests/test_the_fixes_close_the_record.py:1253` | answered | Executed — four mutations, each turning exactly the intended case red, and the rider check red against the pre-repair comment. An earlier round's closure carried forward, so it takes no id |
| 🟢 | the fix pass's rejection of round 1's paste-ready for 🟡 3 | `skills/code-review/scripts/round_record.py#depth_two` | answered | Executed: `if resolved` in place of `if resolved and not owners` turns `test_a_depth_two_refusal_it_cannot_attribute_says_so_and_names_every_candidate` red. Two candidate findings sharing one commit resolve the commit and not the fix. A confirmation this round verified, so it takes no id |
| 🟢 | round 1's `New units` row is complete and its depth is 1, and `Contract changes` reads `none` accurately | `seal/specs/1789425391-…/rounds/round-1.md` §the field table | answered | Executed: no unit added after the close range, and exactly the seven named added inside it. Read: all seven module-level, no earlier record to be inside; and `templates/sdd-round.md:41` puts an argument's accepted type on none of the row's four axes. A confirmation, so it takes no id |
| 🟢 | the absent-name marker round 1's asked paragraph carries, and both ledgers | `seal/specs/1789425391-…/rounds/round-1.md:26`; `seal/ledger.md`; `seal/ledger/1789425391-…​.md` | answered | Executed: `bin/evidence-check --strict .` → 1258 ok · 0 drifted · 0 broken · 0 refused, exit 0, reproducing the orchestrator's figures. A confirmation, so it takes no id |

## Paste-ready fixes

```python
        if len(seen) > VERDICT_COL and seen[location]:
            # FIRST wins, because `inherited_rows` is first-seen-wins WITHIN a
            # record as well as across rounds: it skips a `Location` it has
            # already emitted, so the row round N+1 attributes the coordinate
            # to is the first one carrying it. Assigning here let the LAST row
            # win, and a confirmation below an open finding at one coordinate
            # then wrote `verified` forward over a finding this pass had just
            # closed `fixed` -- #342's disease through the repair for it.
            now.setdefault(
                seen[location], (seen[number], chain.verdict_of(seen, VERDICT_COL))
            )
```
```python
    if not filled:
        # NOT a refusal (round 1's 🔴 2). `inherited_rows` is first-seen-wins
        # ACROSS rounds, so a round whose every coordinate an earlier round
        # already claimed is written into this section under that earlier
        # round and under no other. A re-review round looking again where the
        # round before it looked is the ordinary shape, and refusing it stops
        # the run this reach exists to keep truthful. The refusal's grounds
        # stated a rule about `new` without that qualifier, so the reader was
        # sent to correct a table that was already right.
        #
        # SILENT only where the table accounts for every coordinate, which is
        # the qualifier the other way round. `new` writes one row per
        # `Location` cell of every earlier record, so a well-formed table
        # carries every coordinate of round N under SOME round. One under none
        # is the second cause of `filled == 0` -- a section edited after `new`
        # wrote it -- and nothing else reads this heading, so unconditional
        # silence retired that guard along with the wrong one (round 2's 🟡 2).
        carried = {
            reader.visible(cells[1])
            for _i, cells in body
            if len(cells) >= len(INHERITED_HEADER)
        }
        unclaimed = sorted(c for c in rows if c not in carried)
        if unclaimed:
            raise Refused(
                f"round-{n + 1}.md's `{INHERITED}` carries no row at all for "
                f"{', '.join(f'`{c}`' for c in unclaimed)}, which round-{n}'s "
                "verdict table holds. `new` writes one row per `Location` "
                "cell of every earlier record, under this round or an earlier "
                "one, so a coordinate under neither is a table that was "
                "edited after it was written; no cell was written"
            )
        return None
```
```python
    # `the seal` followed by a letter is `the sealer` or `the sealed tree`,
    # which the sweep that owns this rule skips by the same test
    # (`tests/test_one_word_one_meaning.py`, `if after[:1].isalpha()`). Without
    # it this pin refused the correct way to name the agent (round 2's 🟡 3).
    for hit in re.finditer(r"the seal", out):
        rest = out[hit.end() :]
        assert rest[:1].isalpha() or rest.startswith((" Test", " block")), (
            "the refusal names a seal without saying whose, which is the rule "
            f"`skills/verify/SKILL.md` owns: ...{out[hit.start() - 60 : hit.end() + 60]}..."
        )
```
```python
    text, hits = re.subn(
        r"^\| New units \|.*$",
        "| New units | alpha (depth 1) |",
        text,
        flags=re.MULTILINE,
    )
    assert hits == 1, "the fixture is not the state this is about"
    first.write_text(text, encoding="utf-8")
```
```python
def open_blocking(reader, lines, rel):
    """(rows, errors) — findings the last round left open, blocking flagged."""
    rows, col, errors = verdict_table(reader, lines, rel)
    if col < 0:
        return [], errors
    still_open = []
    for line_no, seen in rows:
        verdict = verdict_of(seen, col)
        if verdict in CLOSED_WORDS:
            continue
        marker = seen[0] if seen else ""
        # The `#` CELL, not the joined row. A row's severity is what its own
        # `#` cell says, and joining read a 🔴 quoted ANYWHERE in the row --
        # a Finding cell naming what an earlier round found, a Grounds cell
        # citing it -- as this row's severity. The message then printed
        # `this 🔴 row reads ... : 🟢`, two severities for one row in one
        # sentence (round 2's 🟡 5).
        #
        # Every open row still comes back, blocking or not: an unrecognised
        # verdict counting as closed is the tolerant read this file exists to
        # refuse, and it is a DIFFERENT complaint from an open 🔴. Narrowing
        # the predicate alone would have dropped it.
        still_open.append(
            (line_no, marker or f"row at line {line_no}", verdict, BLOCKING in marker)
        )
    return still_open, errors
```
```python
    if checked and still_open:
        for line_no, what, verdict, blocking in still_open:
            errors.append(
                (
                    rel,
                    line_no,
                    (
                        f"`Pass` is checked, and this {BLOCKING} row reads "
                        f"`{verdict or 'empty'}` — a blocking finding that is "
                        "not fixed, answered or withdrawn"
                        if blocking
                        else f"`Pass` is checked, and this `{what}` row reads "
                        f"`{verdict or 'empty'}`, which is in no verdict "
                        "vocabulary — an unreadable verdict counts OPEN, so "
                        "the row is refused for the word rather than for a "
                        "severity it does not carry"
                    )
                    + f": {what}",
                )
            )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py -q` in the clone at `5701141` | 75 passed, exit 0 |
| Whole `round_record.py` reverted to `0ff4e3e`, the three new cases run | 3 failed — all three red, with the FILE-LEVEL sentence and both refusal texts in the output; restored, tree clean |
| Mutation: the `now` map keyed from `rows.values()` again | exit 1 — `test_a_row_that_commissions_nothing_does_not_stop_the_reach` red alone, 74 passed |
| Mutation: the empty-fill `raise Refused` restored in `reach_forward` | exit 1 — `test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused` red alone, 74 passed |
| Mutation: `if resolved` in place of `if resolved and not owners` — round 1's own paste-ready | exit 1 — `test_a_depth_two_refusal_it_cannot_attribute_says_so_and_names_every_candidate` red alone, `assert 1 == 2`, 74 passed |
| Mutation: both seal-refusal sentences back to `the seal` | exit 1 — `test_the_refusal_says_which_value_the_last_record_may_hold` and `test_no_instructing_document_leaves_an_instance_anonymous` red, 2 failed / 84 passed |
| Mutation: the refusal's exit sentence naming `the sealer` — a spelling the sweep allows | exit 1 — the seal case red alone, the sweep green. 🟡 3 |
| `tests/test_the_fixes_close_the_record.py` restored to `df404e2`, rider module run | exit 1 — `test_every_rider_carries_a_verification_stamp` red on `tests/test_the_fixes_close_the_record.py:1253`. 🟡 4 of round 1 seen red |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` at `5701141` | 29 passed, exit 0 |
| Probe: a confirmation row at an open finding's coordinate, `new --round 2`, then `close --round 1` (deleted) | exit 0, round 2's `Why` cell rewritten from `round 1's 🔴 1 — open` to `round 1's 🟢 — verified`. 🟡 1 |
| Probe: the committed records read through `table_body` and `verdict_rows` (deleted) | 164 of 212 parse; 49 carry a repeated `Location` over 74 coordinates; 0 pair a numbered row with an unnumbered one |
| Probe: round 2's `## Inherited coordinates` body rows deleted, then `close --round 1` (deleted) | exit 0, silent, nothing written to round 2. 🟡 2 |
| Both proposed repairs applied — the map to `setdefault`, the silence narrowed — over both record modules | 194 passed, exit 0; restored, tree clean |
| Dry run: this report through `round-record new --round 2` in the clone, with the confirmation rows still reading `verified` (record and reach-back reverted) | exit 1 — the record generated and the three tables copied, and `chain_check` failed one row: *this 🔴 row reads `verified` … : 🟢*. 🟡 5 |
| Dry run again, the confirmation rows corrected to `answered` (record and reach-back reverted) | the tables copy, the `Needs a fix` and floor rows land as written, and the row above is gone |
| `bin/survivor-check --range 53259ab..5701141` | 989 files, 30 removed sentences, none standing, exit 0 |
| `bin/survivor-check --range df404e2..5701141` | 989 files, 16 removed sentences, none standing, exit 0 |
| `bin/evidence-check --strict .` in the clone at `5701141` | 1258 ok · 0 drifted · 0 broken · 0 external; records reader 181 names read · 0 refused; exit 0 |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** `skills/agent-contract/SKILL.md` §2 assigns all three to `agents/sealer.md`, spawned once after this round. Nothing in this report needs a fix, so that spawn is what comes due next |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py#reach_forward` `:1535` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#reach_forward` `:1552` | round 1's 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#depth_two` `:3487` | round 1's 3 — fixed |
| round-1 | `tests/test_the_fixes_close_the_record.py:1252-1253` | round 1's 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:3622` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/specs/1789425391-…/plan.md:21`, `spec.md:143` | round 1's ⬜ — answered |
| round-1 | the modules named in `plan.md`'s Verified-by column | round 1's 🟢 — answered |
| round-1 | `round_record.py#says_open`'s docstring; `spec.md:138`; `overview.md:19` | round 1's 🟢 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — the widened map is last-wins against a first-wins writer | an issue, opened by the orchestrator. The run is capped by `docs/review-chain-spec.md` §*The reopening*, so it is a candidate rather than a commissioned fix | the repository owner |
| 🟡 2 — the removed refusal took a malformed record with it | an issue, same cap | the repository owner |
| 🟡 3 — the new pin refuses `the sealer` | an issue, same cap | the repository owner |
| 🟡 4 — the unasserted fixture rewrite | an issue, same cap | the repository owner |
| 🟡 5 — the pull-request check reads a row's severity from the whole row | an issue, same cap. Pre-existing rather than branch-caused, so it is a 0.12.0 candidate rather than a regression | the repository owner |
| The `chain.EMPHASIS` strip reaching no snake_case parent | already deferred in the build — the stamped rider comment at `round_record.py#units_named_earlier`, named in `overview.md` §*Not verified* | the repository owner |
| Whether `no fixes to check` beside a fix-surface row reading *none — the fixes are not yet written* should be refused | already deferred — Q1, answered **(a) leave it open** by the owner before the build | the repository owner, in 0.12.0 beside #174 |
