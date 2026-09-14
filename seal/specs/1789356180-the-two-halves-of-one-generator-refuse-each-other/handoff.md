# Handoff — the session that takes 0.11.4 from here

Written 2026-09-14, at `8d8a753`, for a session with none of this in context.

## Start here

The branch is pushed and the tree is clean. **The next act is one spawn:**

```
sealer, with --base origin/release/v0.11.4 and this work item's directory
```

`chain_check --worktree --baseline origin/release/v0.11.4` refuses exactly one
line, `Broad gate is not yet` on `rounds/round-4.md`, and that is the line the
sealer's run closes. Nothing else is outstanding on the branch.

The gate has been run once on an earlier tree and came back NOT SEALED. Both
things it found that were genuine are repaired at `8d8a753`, and the two that
were not are gone with the revert described below. **Its first run never
reached `ruff`** — the repository's `Broad gate` row is an `&&` chain and
`bin/test` exited 1 — so when the suite goes green, lint and format run on this
branch's tree for the first time. Ask the sealer to say what they said rather
than folding them into the verdict.

## Where the release stands

`release/v0.11.4` is at `5bae06e` and carries two of three work items.

| | Work item | Merged as |
|---|---|---|
| 1 | `round-record` is reachable — a `bin/` wrapper pair and a locator in nine documents (#318) | `34b556a` |
| 2 | a wrapped terminal line is one value (#309, #339, #340) | `5bae06e` |
| 3 | the generator's own cells (#321, #341, #273, #353, #391) | **this branch** |

`#323` is closed as covered — its answer shipped in v0.10.0 and the grounds are
a comment on the ticket. Everything else in the milestone is claimed by a pull
request body, so `release_completeness_check.py` has what it reads.

## What this branch carries, and what it gave up

Four phases shipped and all five ticket claims still hold after the revert:
phase 1 answers #321's body and #353, phase 2 answers #341 and half of #273,
phase 3 answers #391, phase 4 the other half of #273. None of those commits was
reverted.

**What was reverted at `1ff0a6c` is what two FIX PASSES built on top of them** —
round 2's verdict-column arm and round 3's repair of the crash that arm
introduced. Rounds 2 and 3's verdict cells read `deferred #395`, which is what
the branch actually carries, and `#395` holds the whole seam with the
measurements and the reverted code named by SHA.

### Why, because the reasoning is worth more than the outcome

Round 3 answered the floor `yes`: a numbered short row crashed with an
`IndexError` where the base had refused it cleanly. The floor is the one
condition the chain will not let a branch defer, so the owner spawned round 4 —
one round past the reopening bound — rather than ship it capped.

The broad gate then showed what that cost, and it was not one red line on a
pull request. `test_this_repositorys_own_round_records_pass_the_per_record_checks`
and `test_the_reopening_is_one` **walk this repository's own records**, so
merging them would have left the suite red for every branch after this one.

The owner pulled the run back. Round 2's fix went with round 3's because it is
what introduced the crash — with both gone, no later record closes on a fix, the
bound is never approached, and the crash never lands.

**All four round records are kept.** Rounds 3 and 4 happened and found real
things; deleting them would erase review history. A record only trips the bound
by closing on a fix, and none of them does now.

## Then, in order

1. **Sealer.** On a green run it writes the `Broad gate` cell itself through
   `round-record seal`. Commit that, push.
2. **Mark #394 ready** and wait for CI on the pushed head — six jobs, Windows
   is the long one at six to nine minutes.
3. **Squash and merge** into `release/v0.11.4`. The ruleset offers no other
   button there.
4. **Release preparation**, `docs/release-checklist.md` from step 0. Its step 0
   box about the milestone is already true.

### What preparation will find

Three changelog fragments and three ledger fragments are waiting. The gather and
the fold both run in the preparation commit, and `fold_ledger.py` refuses while
any `evidence-todo.md` in the tree has an open row.

`seal/ledger.md` was touched by two of the three work items — item 2 re-stamped
eleven drifted hashes, item 3 corrected two clauses its own change had made
false and left six re-read notes. Both are the sanctioned reason to touch the
shared file, and `evidence-check --strict` is green on the result.

## Traps this run paid for

**A measurement taken without opening the coordinates was wrong six times**,
across four work items and four authors. Five were an aggregate from a loose
match; the sixth was taken *with* the module's own reader and still wrong, which
matters because *use the module's reader* is the repair everybody reached for.
If a number in a record or a ledger row is load-bearing, re-derive it.

**A reviewer's paste-ready fix was green against its own defect three times**,
by three different authors. Run the proposed case against the unfixed code
before committing it.

**`survivor-check` finds wording, not claims.** Twice a corrected sentence stood
in other files that the range check could not see — once because the corrected
wording fell under its phrase threshold, once because the diff never removed the
sentence anywhere. Grep the claim as well as the wording.

**The broad gate found two defects four review rounds did not.** Both arrived
with phase 2 and neither is exotic: a loaded document naming an unreleased
version, and a verdict word a checker matches literally missing from the
exclusion list a translating repository reads. Rounds review the diff; the gate
reads the tree.

## Decisions the owner made, so they are not re-litigated

- The `#` column admits a row that commissions nothing, and `new` validates the
  ids that are written (Q1).
- The SHA in a correction's verdict is not machine-readable; the spec was
  corrected to `answered` with the commit in the grounds cell (Q2).
- #323 closes as covered rather than carrying a remainder (Q3).
- #273's first half lands in this release rather than moving (Q4).
- The run was taken past the bound, and then pulled back when the cost turned
  out to be the repository's own suite.

## Open items, each with a home

| | Where |
|---|---|
| the verdict-column arm, the crash it introduced, and the prose around them | #395, `release: 0.11.5` |
| the segmenter's comment states its own measurement backwards | #393 |
| the pin holding #318's failure message passes when the bad repair is reworded | #390 |
| seven `bin/` wrapper pairs have no executable-bit assertion | #389 |
| `--reverify` moves a row's hash and leaves the date that says when it was read | #387 |
| `close` reducing a deferred row's grounds | #391, answered by this branch's phase 3 |

`#88` was consolidated this session and `#242` closed into it: the routing
question gains two presets and a per-axis fallback, split across two questions
in one `AskUserQuestion` call. It is in `release: 0.12.0` and #241 is its
dependency.
