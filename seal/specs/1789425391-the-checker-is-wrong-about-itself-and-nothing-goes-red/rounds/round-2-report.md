# Round 2 — the fixes hold, and the widened map brought its own defect

Target SHA `5701141`, branch
`fix/142-333-334-335-342-395-the-checker-is-wrong-about-itself-and-nothing-goes-red`,
PR #403, fix diff `0ff4e3e..5701141`. Reviewed in a `git clone --no-local` at
that commit, deleted at the end of the round.

**This is the verifying round and the run ends here.** Round 1's record met the
floor and closed on a fix, so `docs/review-chain-spec.md` §*The reopening — one,
and then the run is capped* caps the run at this record. Everything opened below
goes to an issue rather than to a fix pass, and `Needs a fix` reads `no` for that
reason and not because nothing was found.

## How this round's findings relate

Round 1's five findings are all genuinely closed. Four of the five were verified
by mutation rather than by reading, and the fifth by running the check that had
gone red.

What this round opens comes from one place: the fix for 🔴 1 widened the map
`close` hands the forward reach, and widening it changed two things at once.

```
🔴 1's fix — the map now holds EVERY verdict row
     ├── ① the map is last-wins and `inherited_rows` is first-wins, so two
     │      rows at one coordinate now write the WRONG row's word forward
     └── (the refusal that used to catch the mismatch is gone — see ②)

🔴 2's fix — the empty-fill refusal became unconditional silence
     └── ② a round N+1 record whose section lost its body rows is now
            accepted silently, and nothing else reads that section

separately, in the two branch-caused repairs the fix pass disclosed
     ├── ③ the seal refusal's new pin is stricter than the rule it names
     └── ④ one new fixture rewrites a record with an unasserted `re.sub`

and ⑤ is nobody's fix — it is what the pull-request check said when this
report was run through the generator, and the branch never touched that file
```

---

## 🟡 1 — the widened map writes the wrong row's verdict into the next round

**Location** `skills/code-review/scripts/round_record.py#close`, the `now` map,
at the line `now[seen[location]] = (seen[number], chain.verdict_of(seen,
VERDICT_COL))`.

`inherited_rows` skips a `Location` it has already emitted, so round N+1's
`## Inherited coordinates` attributes a repeated coordinate to the **first**
verdict row that carries it. `close`'s map assigns into a plain dict, so it ends
holding the **last**. Before `df404e2` the two could only disagree between two
numbered rows; the map now holds unnumbered rows too, so a confirmation or a
carried-forward closure at an open finding's coordinate lands in it and wins.

**Executed** in the clone, on a round 1 carrying `| 🔴 1 | … |
`mod.py#helper` | open | … |` and, below it, `| 🟢 | … | `mod.py#helper` |
verified | … |`, with finding 1 closed `fixed`:

```
BEFORE close: {'`mod.py#helper`': "round 1's 🔴 1 — open"}
EXIT: 0
OUT: round-record: closed …/round-1.md — 1 fixed, 0 answered, 0 deferred;
     …; ## Inherited coordinates of round-2.md | 1 row filled
AFTER close: {'`mod.py#helper`': "round 1's 🟢 — verified"}
```

**Why it matters.** Round 1's own record now says `**fixed** df404e2` for
finding 1 while round 2's inherited row says the coordinate was `verified` by a
row that commissioned nothing. That is #342's disease — two records committed
together disagreeing about one coordinate — arriving through the repair for it.
And it arrives at **exit 0**: before the fix this same input exited 2 with
nothing written.

**Measured against the corpus, and this is the honest half.** Through the
generator's own readers, 164 of the 212 committed records parse under
`verdict_rows`; 49 of them carry a repeated `Location`, over 74 coordinates, and
**0** of those 74 pair a numbered row with an unnumbered one. So the state is not
in the shipped corpus. It is the shape the rules now ask for: `agents/warden.md`
tells a reviewer to write a confirmation and a carried-forward closure without an
id, and a verifying round re-reading a coordinate it also opens a new finding at
is the ordinary way to get two rows there.

The repair is one line and makes the two sides agree by construction. **Executed**
with it applied: 194 passed across both record modules.

---

## 🟡 2 — the removed refusal took a malformed record with it

**Location** `skills/code-review/scripts/round_record.py#reach_forward`, the
`if not filled:` arm.

Round 1's 🔴 2 was right that `filled == 0` is the ordinary shape of a re-review
round. The fix answers it with unconditional silence, and `filled == 0` has a
second cause the removed refusal was also catching: round N+1's section edited
or truncated after `new` wrote it.

**Executed** in the clone. Round 2 generated normally, then every body row of its
`## Inherited coordinates` deleted, then `close --round 1`:

```
EXIT: 0
OUT: round-record: closed …/round-1.md — 1 fixed, 0 answered, 0 deferred;
     Contract changes | helper → caller, pytest; New units | none
```

No mention of the reach, nothing written to round 2, exit 0. The same input
refused at exit 2 before `df404e2`.

**Nothing else reads the section.** `grep -n "Inherited" skills/code-review/
scripts/chain_check.py` returns nothing, so `close`'s reach is its only reader
and the two refusals left standing — an unreadable table, and a coordinate the
verdict table lacks — are both bypassed by a table that simply has no rows.

**A narrower condition was available.** `inherited_rows` writes one row per
`Location` cell of every earlier record, so every coordinate of round N appears
in a well-formed round N+1 table, under round N or under an earlier one. Silence
is right exactly when the table accounts for all of them. **Executed** with the
narrowing applied: 194 passed, including
`test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused`, which
is the case the silence exists for.

---

## 🟡 3 — the new pin refuses the one spelling the rule it names allows

**Location** `tests/test_the_seal_is_taken_once_by_the_sealer.py:1307`, the
assertion `assert "the seal" not in out`, added by `ef4542a`.

The docstring says this holds "the rule `skills/verify/SKILL.md` owns". The
sweep that actually holds that rule,
`tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous`,
skips every hit whose next character is a letter — its own comment says
`# the sealer, the sealed tree`. This assertion has no such guard, so it refuses
`the sealer`, which is the correct way to name the agent.

**Executed.** The refusal's exit sentence rewritten to *Spawn the verifying round
first, before the sealer runs*:

```
E  AssertionError: the refusal names a seal without saying whose, which is the
   rule `skills/verify/SKILL.md` owns
E  assert 'the seal' not in 'round-recor…as written\n'
E    'the seal' is contained here:
E      t, before the sealer runs; its record is the one this cell belongs on…
1 failed, 85 passed
```

`test_one_word_one_meaning.py` stayed green on that same text. The two pins
disagree, and the stricter one is the one whose docstring claims to be holding
the other.

**§12, the class.** `grep -rn '"the seal" not in' tests/ skills/` finds this one
occurrence. One member.

---

## 🟡 4 — a new fixture rewrites a record without checking the rewrite landed

**Location** `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit`,
the `re.sub(r"^\| New units \|.*$", …)` that puts `alpha (depth 1)` into round
1's record.

The substitution's result is not asserted, and the case it feeds,
`test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one`, asserts
negatives — `"depth 2" not in out` and `"FILE-LEVEL" not in out`. A miss leaves
round 1 naming no unit at all, `depth_two` returns at its own guard, and both
assertions hold for a reason that has nothing to do with the finding.

**It works today**, and I saw it work: the case is red against the pre-fix module
(below). What it cannot do is notice its own fixture breaking, which is one level
in on this work item's own subject.

The two 🔴 cases in the same commit each carry a guard —
`assert inherited(repo)["`README.md`"].endswith("verified"), "the fixture is not
the state this is about"` — so the omission is an inconsistency inside one fix
pass rather than a house style.

---

## 🟡 5 — the pull-request check reads a row's severity from the whole row, and prints a line that contradicts itself

**Location** `skills/code-review/scripts/chain_check.py#open_blocking`, the
predicate `BLOCKING in "".join(seen)`.

**Not branch-caused.** `git log --oneline aa3000d..5701141 --
skills/code-review/scripts/chain_check.py` is empty, and the predicate came in
at `2d4a52a` on 2026-09-01. I met it by running the generator against this
report, which is the reason it is here rather than in a sweep.

The row's severity lives in its `#` cell. This joins **every** cell and asks
whether `🔴` appears anywhere in the row, so a `🟢` row whose Finding or Grounds
quotes an earlier round's 🔴 is read as a blocking finding. Two rows of this
report do that, because naming what an earlier round found is what a carried-
forward closure is for.

**Executed.** `round-record new --round 2` in the clone, against an earlier draft
of this report whose confirmation rows read `verified`:

```
seal/specs/1789425391-…/rounds/round-2.md:32  `Pass` is checked, and this 🔴
row reads `verified` — a blocking finding that is not fixed, answered or
withdrawn: 🟢
```

**The message names two different severities for one row, in one sentence.**
`still_open` builds the last field from `seen[0]`, the `#` cell, which is `🟢`;
`BLOCKING` in the message text is the constant, not the row. The reader is told
to go find a blocking finding and handed a row that says it is a confirmation.

**The refusal is directionally right and that is what makes it expensive.**
`verified` is outside `CLOSED_WORDS`, and the comment above that set says an
unrecognised verdict counting as closed is *the tolerant read this whole file
exists to refuse* — so failing the row is correct. What is wrong is the reason
printed for it. The reader who takes the message at its word looks for a 🔴,
finds none, and never learns that the actual complaint is a verdict word the
vocabulary does not hold.

**How the two interact, which is why this stayed invisible.** With a row whose
verdict IS closed the arm never runs, and the committed corpus closes its
confirmation rows with `answered`. So the whole-row read needs an unnumbered row
with an unrecognised verdict beside it to become visible — and an unnumbered row
is exactly what `close` does not count toward `Pass`, so `Pass` is ticked while
that row stands. This report is the instance: four confirmation rows, and the
first of them quotes `🔴 1, 🔴 2` in naming what round 1 found.

I corrected this report to `answered` rather than reword the row, because
`answered` is the vocabulary and `verified` was my error. The finding is the
checker's message, not the word I chose.

---

## ⬜ 6 — the ledger row I was asked to judge: right conclusion, half-wrong grounds

**Location** `seal/ledger.md`, row S13, the clause *how many of the three values
the seal accepts on a LAST record*.

**I agree it should stay.** `tests/test_one_word_one_meaning.py`'s `SEAL_SWEPT`
comment states the boundary deliberately: *Files that instruct somebody, swept
below. A record of what was true when it was written is not brought to a new
wording, so `seal/` is not here.* The ledger is a record, not an instruction, and
it is outside the sweep by design rather than by oversight. Nothing is red, and
nothing should be.

**I disagree with the other half of the grounds.** The fix pass also placed it
*outside what a branch may edit in the shared ledger*. That is not what happened
here:

- `git log --oneline -S "the three values the seal accepts" -- seal/ledger.md`
  names `3ece7b7`, which is a commit of this branch — phase 4.
- The branch edited `seal/ledger.md` in this very row, twice, appending its
  re-read clauses, and `0ff4e3e..5701141` edits the file again.

So the sentence is this branch's own prose in a row this branch was already
writing, and the rule that would have forbidden touching it did not apply. The
conclusion survives on the first ground alone, which is why this is ⬜ and not a
finding: nothing needs to change, and the reason recorded for it should.

---

## What round 1 commissioned, and whether it is closed

All five verified, four of them by putting the defect back.

| Round 1 | Verified how |
|---|---|
| 🔴 1 | **Executed.** The map keyed from `rows.values()` again → `test_a_row_that_commissions_nothing_does_not_stop_the_reach` red, alone, 74 passed |
| 🔴 2 | **Executed.** The empty-fill `raise Refused` restored → `test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused` red, alone, 74 passed |
| 🟡 3 | **Executed.** Whole module reverted to `0ff4e3e` → all three new cases red, with the FILE-LEVEL sentence in the output |
| 🟡 4 | **Executed.** The comment restored to `df404e2`'s spelling → `test_every_rider_carries_a_verification_stamp` red on `tests/test_the_fixes_close_the_record.py:1253`, exit 1 |
| ⬜ 5 | **Read.** `lambda: unit_adders(reader, root, fixes)` at the call site, `adders() if callable(adders)` behind the guard; `depth_two` returns before the call on a round-1 `close` |

**The fix pass's rejection of round 1's paste-ready for 🟡 3 is right, and right
for the reason it gave.** `if resolved: continue` in place of `if resolved and
not owners: continue`, **executed**: exactly
`test_a_depth_two_refusal_it_cannot_attribute_says_so_and_names_every_candidate`
red, `assert 1 == 2`, 74 passed. `owners` holds two entries when one commit
answers two candidate findings, which resolves the commit and not the fix, so the
file-level sentence is the true one there. Round 1's version would have called
that depth 1.

## The three the fix pass reported outside round 1's table

**The seal refusal (`ef4542a`, `ef857c2`) — the pin fails, and the exit survives.**
**Executed**: both sentences reverted to `the seal` →
`test_the_refusal_says_which_value_the_last_record_may_hold` **and**
`test_no_instructing_document_leaves_an_instance_anonymous` red, 2 failed / 84
passed. The refusal still names `no fixes to check`, both refused values, and
*Spawn the verifying round first*, each asserted. The pin is over-strict in one
direction, which is 🟡 3 above.

**The `SUMMARY_WORDS` <!-- NAME NOT IN TREE: the name round 1 was asked to check FOR absence; it exists in no branch of this repository --> marker (`5701141`) — accepted.** **Executed**:
`bin/evidence-check --strict .` in the clone → `total: 1258 ok · 0 drifted · 0
broken`, and the records reader `1 work item read · 181 names read · 0 refused`,
exit 0. The orchestrator's figures reproduce.

**The ledger row — ⬜ 5 above.**

## The two the handover asked me to judge

**The depth of round 1's seven new units — correct, and correct for a reason
nothing checked.** `close` writes `units_entry(n, 1)` unconditionally, so the
depth is only ever tested by `depth_two`'s refusal, and round 1 has no earlier
records at all, so that walk returns at its first guard. **Read**: all seven are
module-level definitions in `tests/test_the_fixes_close_the_record.py`, and there
is no earlier record whose `New units` could name a parent. Depth 1 holds.

**The row is also complete, which the three later commits put in doubt.**
`close` ran at `df404e2`, and `9c728a8`, `ef4542a`, `ef857c2` and `5701141`
landed after it. **Executed**: `git diff df404e2..5701141 -- '*.py'` adds no
`def`, no `class` and no module-level assignment. And `git diff
53259ab..df404e2` adds exactly the seven the row names — `PAIR_BOTH_FIXED`,
`ONE_INSIDE_ONE_OUTSIDE`, `one_finding_inside_one_earlier_unit`,
`test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one`,
`CONFIRMATION`, `test_a_row_that_commissions_nothing_does_not_stop_the_reach`,
`test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused`.

**Judging those seven as code**, which is what `New units` is for: the two 🔴
cases each open with a fixture guard and assert the attribution as well as the
exit code, and the 🟡 3 case asserts `New units` reads `beta_guard (depth 1)`
rather than only that nothing was refused. That is the right shape. The one
defect in them is 🟡 4 above.

**`Contract changes | none` — accurate, and the record should not say more.**
`templates/sdd-round.md:41` defines the row as *every unit whose signature,
return arity, return type, or set of returnable values this round's fixes
changed*. `depth_two`'s signature is unchanged; what widened is the type its
`adders` parameter accepts, which is on none of those four axes. The widening is
also compatible and unreachable from outside: a mapping still works, the default
is still `None`, and the one call site is in the same module and changed in the
same commit. `chain_check.py` refuses a unit listed without its reach, so
listing it would ask for call sites that are not the point. The comment at the
`adders = adders() if callable(adders)` line already carries the reason.

## Round 1's spec-compliance pass

Inherited, not re-run. No fix in this diff touches what S1–S16 rest on: the two
map changes are inside `close` and `reach_forward`, which S8 covers and which
round 1 already named as the two shapes S8 does not reach; the `depth_two` arm is
S11/S12 and its own case moves with it; the rest is prose and paperwork.

## Nothing else I went looking for

**Executed**: `bin/survivor-check --range 53259ab..5701141` → *examined 989 files
at 5701141, against 30 sentence(s) the range removed · no removed wording is
still standing*, exit 0. And over `df404e2..5701141` alone — the three commits
`survivors.md` records no sweep for — 16 sentences, nothing standing, exit 0. The
gap I expected in the survivors note is not one.

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

## Paste-ready fixes

**🟡 1.** In `close`, the `now` map — first-wins, so the two sides agree by
construction rather than by the record's row order:

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

**🟡 2.** In `reach_forward`, the `if not filled:` arm — silent where the table
accounts for every coordinate, and refusing where it does not:

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

**🟡 3.** In `tests/test_the_seal_is_taken_once_by_the_sealer.py`, the assertion
at `:1307` — the same guard the sweep uses, so the pin holds the rule it names
and no more:

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

**🟡 4.** In `tests/test_the_fixes_close_the_record.py`, inside
`one_finding_inside_one_earlier_unit` — assert the rewrite landed, the way the
two cases beside it assert their fixture:

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

**🟡 5.** In `chain_check.py`, `open_blocking` and its one consumer. The
predicate reads the `#` cell, and the row still comes back open so an
unrecognised verdict does not slip through — that is the half a narrowing alone
would lose, and the comment above `CLOSED_WORDS` is what forbids losing it:

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

and at the one consumer, so each row is refused for its own reason:

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

Needs a fix: no

Loses a record or crashes: no

## Proof

Opened and read: `seal/specs/1789425391-…/{routing,overview,spec}.md` and
`rounds/{round-1.md,round-1-report.md}`; `phases/phase-6.md`; `survivors.md`;
`seal/ledger.md` §§S6, S13 and the branch's diff of it;
`seal/ledger/1789425391-…​.md`; `seal/config.md`;
`skills/code-review/scripts/round_record.py` at `row_cells`, `table_body`,
`table_of`, `inherited_rows`, `reach_forward`, `verdict_rows`, `unit_adders`,
`depth_two`, `contract_entry`, `units_entry`, `surface_cell`, `close` and `seal`;
`skills/code-review/scripts/chain_check.py` at `open_blocking`,
`closed_with_a_fix`, `CLOSED_WORDS`, `MARKER` and the `Pass`-and-still-open arm,
and searched for the inherited heading;
`tests/test_the_fixes_close_the_record.py` over the branch diff and its
fixtures; `tests/test_the_seal_is_taken_once_by_the_sealer.py` at
`test_the_refusal_says_which_value_the_last_record_may_hold`;
`tests/test_one_word_one_meaning.py` at `SEAL_SWEPT`, `SEAL_EXCLUDED`,
`SEAL_BARE_IS_THE_CONCEPT` and the sweep; `tests/test_a_rider_reaches_its_file.py`
(run); `templates/sdd-round.md` over the branch diff and its field table;
`docs/review-chain-spec.md` over the branch diff; `agents/sealer.md` over the
branch diff; `bin/test`; `~/.claude/skills/writing-style/SKILL.md`.

Executed: the runs in `## Executed probes`. Every mutation was reverted with
`git checkout` and the clone's tree confirmed empty under `git status
--porcelain` after each. The clone, its virtualenv and all three probe files were
deleted at the end of the round.
