# Round 3 — the last round, on round 2's fixes

Round 3 of #344, #426 and #427 at `f2e8a010`, on
`fix/344-426-427-nothing-reads-a-record-against-the-tree`, against
`release/v0.12.1` at `56945007`. The target is the fix range
`d34ef317..f4e7d768`, three commits. Reviewed in a `git clone --no-local` at
the target SHA; every mutation was reverted there and the clone ended
byte-clean at `f2e8a010`. Nothing was written in the working checkout but
this file.

This record ends the run whatever it finds. Nothing below asks for another
round, and two of the three things it opens should still be answered before
the pull request goes ready — each says which, and by whom.

## How the findings relate

**Both of round 2's own findings are closed, and I proved it with the
mutations I built rather than with new ones.** What this round opens is one
claim and two records.

```
① 🔴 1 and 🟡 2 — closed, re-opened with round 2's own mutations
      ↓ but one of the eight rows closed `answered`, and its grounds are
        a claim about the generator rather than a judgment
② `close` does NOT refuse at depth 2 — it wrote the cell   ⬜ 1
      ↓ and the cause is a rider already in the tree, with no issue on it
③ the ⬜ 5 repair wrote a present-tense claim that a clone cannot run  ⬜ 2
      ↓ same file, a rendering artifact the repair left standing
④ the sentence still renders as two paragraphs   ⬜ 3
```

⬜ 1 is the one that matters. The other two are the run's own paperwork.

---

## The eight closures

### 🔴 1 — the case that reddened after the squash. Closed.

The repair is the paste-ready text round 2 wrote, applied verbatim. I re-ran
**my own mutation** three ways in the clone:

| | Arithmetic | Record's range ends | Result |
|---|---|---|---|
| A | round 3's repair | untouched | **exit 0** |
| B | round 3's repair | unresolvable | **exit 0** |
| C | round 1's, restored | unresolvable | **exit 1** |

C's failure, which is the defect reappearing under the old arithmetic:

```
E   AssertionError: 230 notices over 229 records with no row: a record that
    predates the row has to print, not go quiet
E   assert 230 == (231 - 2)
```

The `231 - 2` is worth reading: since round 2 there are **two** records
carrying the row, `round-1.md` and `round-2.md`, and both name commits of
this feature branch. So I ran the real post-merge state as well — **both**
records' ends made unresolvable at once:

```
BOTH records' ends unresolvable (the real post-squash state) -> exit 0
    1 passed in 0.25s
```

That is the case it has to survive, and it does. The repair counts notices
over the group with no row instead of subtracting the carrying ones from the
total, so any number of carrying records may print without touching the
arithmetic.

### 🟡 2 — the assertion that could not fail. Closed.

The repair compares against `stripped`, the bytes the test itself writes
before the run. I re-ran **my own clobbering mutation** — `close` altered to
overwrite every `round-*.md` under the work item before raising:

```
=== F. round 3's repair, UNDER round 2's clobbering mutation -> exit 1
E   AssertionError: the refusal wrote anyway
E   assert 'CLOBBERED BY THE PROBE\n' == '# 1799000000...he CI leg |\n'
E     + CLOBBERED BY THE PROBE
E     - # 1799000000-a-later-work-item — review round 1
```

Unmutated it is exit 0, restored it is exit 0. The assertion whose message is
*the refusal wrote anyway* now says so, and it names the bytes it expected.
This is the same mutation that passed silently in round 2.

### ⬜ 3, ⬜ 4, ⬜ 6, ⬜ 7 of round 2 — the four corrections. Closed.

**read**, each at its coordinate:

- the exemption file's heading now reads ``## Round 1's fix pass — `b38bd920..bf693bc1` ``;
- the retired `8 spellings` figure is gone from all three coordinates round 2
  named — ledger R8's `Notes`, and `overview.md` lines 26 and 59 — and the
  only places that still hold it are `phases/phase-3.md` and
  `phases/phase-4.md`, which are records of a moment and already carry the
  correction beside them;
- `chain_check.py:4271` now cites `(round 1's ⬜ 4)`;
- round-1.md's ⬜ 9 grounds now carry the HTML-comment correction, giving the
  `1` call beside the `0`.

### ⬜ 5 of round 2 — the doubled phrase. Closed on the substance.

The sentence no longer says *across this branch's life* and *across this
branch* on either side of the command. What it still does is render as two
paragraphs, which is ⬜ 3 below and is not what round 2 raised.

### ⬜ 8 of round 2 — `answered`, and the answer does not hold. This is ⬜ 1.

---

## ⬜ 1 — `close` does not refuse at depth 2, and the answer rests on the claim that it does

`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/rounds/round-2.md`,
⬜ 8's `Grounds` cell; and the same work item's `overview.md` §*Not verified*,
the row beginning *The `isdigit()` half of `close`'s count guard is pinned by
no case*.

The grounds are a claim about the generator, so I executed it rather than
read it. I put the work item's `round-2.md` back to its pre-close state,
added one new top-level unit to
`tests/test_the_fixes_close_the_record.py` — the file the grounds name — committed it,
and ran `close` with the same eight-row fix table over a range ending at that
commit.

**`close` did not refuse. It closed the record and wrote the cell:**

```
round-record: closed …/rounds/round-2.md — 7 fixed, 1 answered, 0 deferred;
Fix range | `d34ef3177711c20e…..590f1e5cb683ad53…`, 7 commits;
Contract changes | none;
New units | test_tmp_the_count_guard_refuses_a_non_digit (depth 1);
Fixes checked by | nobody — the fixes are written and no round has opened them
```

`record unchanged: False`. The unit was recorded at **depth 1**. The exit 1
that followed came from `chain-check`'s `Pass` arm on an artificially
re-closed record, not from `depth_two`.

**Why, and it is already written down in the tree.** `depth_two` matches a
finding's `Location` unit against the keys of `units_named_earlier`, and
those two disagree about the shape of a name:

```
named (units_named_earlier) keys : ['testarecordwithnofixrangerowistoldwhichrowtoadd']
location_units units             : ['test_a_record_with_no_fix_range_row_is_told_which_row_to_add']
  'test_a_record_with_no_fix_range_row_is_told_which_row_to_add'  in named? False
```

`units_named_earlier` applies `chain.EMPHASIS`, which is ``[*_`]+``, to the
whole entry, so every underscore inside a unit name is stripped along with
the backticks around it. `round_record.py:3417` carries a `# RIDER:` saying
exactly this, and it is explicit about the consequence: *The depth-2 walk
below therefore reaches no Python unit whose name carries an underscore,
which is most of them.* It is stamped *Verified 2026-09-15 against
`units_named_earlier@9165d624`* and marked `NOT REPAIRED HERE`, with the
repository owner as answerer.

**executed** — how much of the corpus that reaches: of the **542** units any
`New units` row in this tree names, **502** carry an underscore.

**The case the grounds cite is what refutes them.**
`test_a_depth_two_refusal_names_the_finding_whose_fix_added_the_unit` uses
`alpha` and `beta` as the units an earlier record names. Neither has an
underscore, so both survive the stripping and the refusal fires. The grounds
read that green case as covering a unit named
`test_a_record_with_no_fix_range_row_is_told_which_row_to_add`, which is the
one shape it cannot cover. Naming the case is what made the claim checkable,
and checking it is what breaks it.

**What it costs.** Two things, and the second is the reason this is not
merely a wrong sentence.

- The stated reason is false. The `isdigit()` case **could** have been
  planted by this pass; nothing in the generator would have stopped it.
- `overview.md` §*Not verified* is where a future session looks for
  precedent. That row now tells the next fix pass that a case in a file whose
  units an earlier record names is refused at depth 2 — and the next pass
  will decline to plant a case it was free to plant, citing this row.

**What I am not opening.** The underscore defect itself is disclosed at its
coordinate with an answerer named, so it is not a finding of mine. What is
missing is an issue: `gh issue list` over all states shows #333 and #222 on
`depth_two`, neither of them this, and the rider is the only record of it.

## ⬜ 2 — the repaired sentence states a command a clone cannot run

`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/survivors.md:5`,
and `seal/ledger.md` R7's `Verified behavior` cell, which records the same
execution.

Round 2's ⬜ 5 repair rewrote the line to read
``survivor-check --range d35c874...ce0f9fe` reports two places today``. That
is a present-tense, reproducible-sounding claim, and it replaced a
past-tense attribution. **executed** in the clone:

```
survivor-check: --range d35c874...ce0f9fe: `ce0f9fe` does not resolve in <the clone>
exit: 2
```

**executed**, the two ends compared:

| End | In a fresh clone | Reachable from a ref in the working checkout |
|---|---|---|
| `d35c874` | resolves | **1** ref |
| `ce0f9fe` | **does not resolve** | **0** refs |

`ce0f9fe` was a feature branch's tip. The branch was squashed and deleted, so
no ref reaches the object; it survives only as a loose object in a repository
that held it before the merge. `git clone` sends reachable objects, so the
commit does not travel — to a fresh clone, to CI, or to anybody who was not
there.

**What it costs.** This is the work item's own class, in the line the work
item corrected twice. Pinning a range was supposed to make a claim
re-runnable, and this one is re-runnable only by the person who already knows
the answer. Ledger R7's `Verified behavior` cell records the same execution
and inherits the same property — and R7 is the row that states *a measurement
is reproducible only against a named range AND a named version of what
measured it*.

**Re-pinning is not available**, which is why this is an issue rather than a
correction: the content the range names is gone from any clone. The choices
are to say so beside the figure, to drop the numeric claim, or to re-measure
against something a ref reaches. That is the repository owner's call.

## ⬜ 3 — the repaired sentence still renders as two paragraphs

`seal/specs/1789034970-…/survivors.md:5`, the HTML comment between the
sentence's two halves.

**executed** — the section put through GitHub's own markdown renderer, tags
stripped:

```
--- rendered paragraph 0 ---
… survivor-check --range d35c874...ce0f9fe reports two places today.
Sixteen were reported across this branch's life

--- rendered paragraph 1 ---
— fifteen at the head it was first run against, and a sixteenth once the
note explaining a removed ledger row landed, …
```

A comment starting a line opens an HTML block, which ends the paragraph, so
the tail becomes its own paragraph beginning with an em dash. This is not
what round 2 raised — the doubling it raised is gone — and the break is
older than either repair. It is one line: move the comment past the end of
the sentence it interrupts. Corrected in passing or not at all.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Round 2's ⬜ 8 closed `answered` on the claim that `close` refuses a new unit in that file at depth 2 before writing a cell. It does not — it writes the cell at depth 1 — and the case the grounds cite uses underscore-free names, which is the one shape the mechanism can reach | `seal/specs/1789621028-…/rounds/round-2.md` · ⬜ 8's `Grounds`; `seal/specs/1789621028-…/overview.md` · §*Not verified*, the `isdigit()` row | open | Executed: the record put back to its pre-close state, one new top-level unit committed into `tests/test_the_fixes_close_the_record.py`, the same eight-row fix table — `close` reported `7 fixed, 1 answered`, wrote `New units \| … (depth 1)` and the record changed. Cause is the `# RIDER:` at `round_record.py:3417` — `chain.EMPHASIS` strips every underscore from `units_named_earlier`'s keys while `location_units` returns them raw, so the lookup misses. Measured: 502 of the 542 units any `New units` row in this tree names carry an underscore. No issue tracks it; #333 and #222 are other `depth_two` defects |
| ⬜ 2 | The ⬜ 5 repair states `` `survivor-check --range d35c874...ce0f9fe` reports two places today `` — a present-tense claim that is exit 2 in any fresh clone, because `ce0f9fe` is reachable from no ref and does not travel | `seal/specs/1789034970-…/survivors.md:5`; `seal/ledger.md` · R7's `Verified behavior` | open | Executed: in a `--no-local` clone the command exits 2, `` `ce0f9fe` does not resolve ``. `d35c874` resolves in the clone and is reachable from 1 ref; `ce0f9fe` resolves in the working checkout and is reachable from 0. Re-pinning is not available — the object is gone from any clone — so this is the owner's call rather than a correction |
| ⬜ 3 | The HTML comment between the sentence's halves opens an HTML block, so the repaired sentence renders as two paragraphs and the tail begins with an em dash | `seal/specs/1789034970-…/survivors.md:5` | open | Executed through GitHub's own markdown renderer: paragraph 0 ends `Sixteen were reported across this branch's life`, paragraph 1 begins `— fifteen at the head it was first run against`. Older than either repair and not what round 2 raised; one line to move |
| 🟢 4 | 🔴 1 of round 2 — the case that reddened after the squash | `tests/test_chain_check_at_the_pull_request.py` · `test_the_records_in_this_repository_are_not_failed_by_the_new_row` | fixed | Executed with round 2's own mutation, three ways: the repair with the record untouched exit 0; the repair under the mutation exit 0; round 1's arithmetic restored under the same mutation exit 1, `assert 230 == (231 - 2)`. Also executed in the real post-merge state — BOTH records carrying the row made unresolvable at once — exit 0. The repair counts notices over the group with no row rather than subtracting, so any number of carrying records may print |
| 🟢 5 | 🟡 2 of round 2 — the assertion that could not fail | `tests/test_the_fixes_close_the_record.py` · `test_a_record_with_no_fix_range_row_is_told_which_row_to_add` | fixed | Executed with round 2's own clobbering mutation: `close` altered to overwrite every `round-*.md` before raising now gives exit 1, `AssertionError: the refusal wrote anyway`, naming the clobbered bytes against the record it expected. Unmutated exit 0, restored exit 0. The same mutation passed silently in round 2 |
| 🟢 6 | ⬜ 3 of round 2 — the exemption file's moving range | `seal/specs/1789621028-…/survivors.md:3` | fixed | Read: the heading reads `` `b38bd920..bf693bc1` ``, both ends commits, matching the sibling file's pinning |
| 🟢 7 | ⬜ 4 of round 2 — the retired `8 spellings` figure | `seal/ledger/1789621028-…md` · R8 `Notes`; `seal/specs/1789621028-…/overview.md:26` and `:59` | fixed | Read: all three coordinates now read 12 sentence forms, and `overview.md:59` names the command beside it. The two remaining holders are `phases/phase-3.md` and `phases/phase-4.md`, records of a moment that already carry the correction |
| ⬜ 8 | ⬜ 5 of round 2 — the doubled phrase | `seal/specs/1789034970-…/survivors.md:5` | fixed | Executed: the doubling is gone — the sentence no longer says `across this branch's life` and `across this branch` on either side of the command. What the repair left is the rendering break, ⬜ 3 above, and the claim itself, ⬜ 2 above |
| 🟢 9 | ⬜ 6 of round 2 — the wrong finding cited in shipped code | `skills/code-review/scripts/chain_check.py:4271` | fixed | Read: the comment now reads `(round 1's ⬜ 4)`, and `round_record.py:3797` still cites `(round 1's 8)` for the guard, so the two no longer collide |
| 🟢 10 | ⬜ 7 of round 2 — the `0 git calls` figure | `seal/specs/1789621028-…/rounds/round-1.md` · ⬜ 9's `Grounds` | fixed | Read: the cell carries the HTML-comment correction giving 1 call beside the 0, with the execution and the reason the answer is unaffected |
| ⬜ 11 | ⬜ 8 of round 2 — two closures pinned by no case | `templates/sdd-round.md`; `skills/code-review/scripts/round_record.py` · `close` | answered | **The answer is not accepted.** Its grounds are a claim about the generator and the generator does the opposite — ⬜ 1 above carries the execution. The template half stands: pinning it needs a walk, and a walk is on the list a fix pass may not add. The `isdigit()` half's stated reason is false, and the row it produced in `overview.md` §*Not verified* is precedent a future pass will read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone at `f2e8a010` | 229 passed, exit 0 — the baseline every mutation was taken against |
| round 2's squash mutation — the record's range ends made unresolvable — against round 3's repair | **exit 0**, 1 passed |
| the same mutation with round 1's arithmetic restored | **exit 1**, `230 notices over 229 records with no row`, `assert 230 == (231 - 2)` |
| the same mutation applied to **both** records carrying the row, the real post-merge state | **exit 0**, 1 passed |
| round 2's clobbering mutation — `close` overwriting every `round-*.md` before raising — against round 3's repair | **exit 1**, `AssertionError: the refusal wrote anyway`, naming the clobbered bytes |
| `close` re-run against the pre-close record with one new top-level unit committed into the file ⬜ 8 names | **no depth-2 refusal** — `7 fixed, 1 answered`, `New units \| … (depth 1)`, record changed |
| `units_named_earlier` and `location_units` asked for their key shapes | `testarecordwithnofixrangerowistoldwhichrowtoadd` against `test_a_record_with_no_fix_range_row_is_told_which_row_to_add`; membership `False` |
| every `New units` entry in the tree counted for underscores | **502 of 542** carry one |
| `bin/survivor-check --range d35c874...ce0f9fe` in the clone | **exit 2**, `` `ce0f9fe` does not resolve `` |
| both pinned ends checked for reachability | `d35c874` — resolves in the clone, 1 ref; `ce0f9fe` — does not resolve in the clone, 0 refs |
| the survivors section put through GitHub's markdown renderer | two paragraphs, the second beginning `— fifteen at the head it was first run against` |
| `gh issue list --state all` searched for the underscore defect | #333 and #222 are other `depth_two` defects; nothing tracks this one |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer and this round ran none of them. They come due now: this round opens nothing needing a fix, so the sealer's spawn is what follows this record |

Every mutation was applied alone, reverted in a `finally`, and every
substitution asserted it matched. Git was driven from Python so no commit
reached the commit gate. The clone ended with an empty
`git status --porcelain` at `f2e8a010` and was then deleted with the two
probe drivers, which lived outside it.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |

Both carried forward unchanged. The second is worth reading beside 🟢 4: the
deferral is about the checker after a squash, and this round ran the case
against both carrying records made unresolvable at once, which is the
fixture form of that event and not the event.

## Paste-ready fixes

⬜ 1 — `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/overview.md`,
§*Not verified*. Replace the `isdigit()` row's grounds with what was
measured, so the next pass reads the real precedent:

```markdown
| The `isdigit()` half of `close`'s count guard is pinned by no case, and round 2's fix pass did not add one. Reverted alone it is 102 passed, exit 0 | the repository owner, as its own work item. **The reason first given here was wrong and is corrected**: the pass argued that `close` would refuse the new unit at depth 2, because round 2's 🟡 2 sits inside a unit `rounds/round-1.md`'s `New units` names and the case would land in that unit's file. Round 3 executed it — one new top-level unit committed into that file, the same eight-row fix table — and `close` did **not** refuse: it closed the record and wrote `New units \| <the unit> (depth 1)`. The cause is the `# RIDER:` at `skills/code-review/scripts/round_record.py#units_named_earlier`, which strips every underscore from that function's keys while `location_units` returns them raw, so `depth_two` reaches no snake_case unit — 502 of the 542 units named by a `New units` row in this tree carry one. So the case WAS available to that pass and was simply not written; what is owed is the case, not a rule |
```

And in `rounds/round-2.md`, ⬜ 8's `Grounds` cell, beside the sentence rather
than over it — the record is not rewritten:

```markdown
<!-- Round 3, 2026-09-17: executed, and the generator does the opposite. `close` run against this record's pre-close state with one new top-level unit committed into `tests/test_the_fixes_close_the_record.py` and the same eight-row fix table wrote `New units | <the unit> (depth 1)` and changed the record; there was no depth-2 refusal. `units_named_earlier` strips underscores from its keys (`# RIDER:` at `round_record.py#units_named_earlier`) so `depth_two` reaches no snake_case unit, and the case cited here uses `alpha` and `beta`, which carry none. The template half of this answer stands; the `isdigit()` half's reason does not. -->
```

⬜ 2 — no paste-ready fix. The object `ce0f9fe` names is gone from any clone,
so the line cannot be re-pinned and the repair is a decision rather than an
edit. It is an issue, and the body it needs is the table above:
`d35c874` travels and `ce0f9fe` does not.

⬜ 3 — `seal/specs/1789034970-…/survivors.md`. Move the comment past the
sentence it splits, so the two halves are one paragraph again:

```markdown
`survivor-check --range d35c874...ce0f9fe` reports two places today. Sixteen
were reported across this branch's life — fifteen at the head it was first
run against, and a sixteenth once the note explaining a removed ledger row
landed, which put the sentence that row carried into the range's removed set.
None of the sixteen is a stale copy of a corrected claim standing where a
reader would act on it.
…and the comment that already stands in the file follows unchanged, opening
at `The range read origin/release/v0.10.0...HEAD until 2026-09-17`.
```

Needs a fix: no

Loses a record or crashes: no

**What that answer does and does not say.** Nothing here blocks the release
and no round is owed. Two things should still be answered before the pull
request goes ready, and neither is a fix pass: ⬜ 1's `overview.md` row is a
correction for the closing commit, because it is precedent a later session
will act on, and ⬜ 2 is an issue with the repository owner as answerer,
because the commit it names cannot be reached from any clone. ⬜ 3 is one
line, corrected in passing or not at all.

## Proof block

Files opened: `skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`seal/ledger.md`, `seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md`,
`seal/specs/1789621028-…/{overview,survivors}.md` and its
`rounds/{round-1,round-2,round-2-report}.md`,
`seal/specs/1789034970-…/survivors.md`,
`~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all inside a `git clone
--no-local` at `f2e8a010`, exit codes read from `returncode` or `$?` and
never through a pipe. The clone was verified clean at the target SHA and then
deleted; both probe drivers lived outside it and went with it.
