# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — round 2's corrections

<!-- Read by `round_record.py close`, which applies this table to
rounds/round-2.md. One row per finding round 2 left OPEN — findings 1 through
9 were closed by the reviewer in round 2's own verdict table and a row here
would overwrite the reviewer's verdict, which `close` refuses. -->

| Field | Value |
|---|---|
| Answers | round 2, target `17a4737` |
| Fix commits | `86d8e41..HEAD` |
| Ran by | the orchestrating session — every one of these is a correction located in a record, which `docs/review-chain-spec.md` §*The last round verifies* says owes no fix pass and no reader |

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 10 | answered | Corrected. `overview.md`'s `· verified` line now says the figure is 32 **at `ae2d0ac`, the tree that line describes**, and that it reads 36 at the branch tip because the range re-resolves and the exemption file's quotes move what is searched (#308). A count with no tree beside it was the whole of round 1's finding 4, and this is that class inside its own fix |
| 11 | answered | Corrected. `survivors.md` states both figures with their trees — 32 at `ae2d0ac`, 29 records and 3 loaded files; 36 at the tip, 31 and 5 — and names the two things that move them. The withdrawn bullet's paragraph now says that withdrawing it is what returned its place to the reported set, so round 1's *not among them* was true of a tree the bullet itself had made. The withdrawal still stands: the sentence was wrong about what is written at that line |
| 12 | answered | Corrected. The heading reads *six per-survivor rows* over the six that are there |
| 13 | answered | No edit, and the grounds are that nothing live carries the number. `467` and `468` appear only inside `rounds/`, which are records of what a party measured at a moment. Round 2's verdict row is where the correction belongs and it names what reproduces — 473 single-spaced date cells at `ae2d0ac` and `bfe8cdb`, 476 and 0 doubled at `17a4737`; re-derived here at the tip, 476 and 0 |
| 14 | answered | Corrected, and it is the one of the five that was a gap rather than a wrong number. The deferred decision is now `questions.md` Q6, with both answers spelled out and what shipped named as the default, and a `## Not verified` row carries it so `bin/unverified-check` reports it — exit 0, the row printed as `open` against the repository owner. It stood only in `rounds/round-1.md`'s Verdict and Grounds cells, both reading *the repository owner*, because `fix_table` discards a `deferred` row's third cell |

## What these corrections did not add

No new unit, no mechanism, no `phases/phase-N.md` and no `plan.md` phase row.
Five records and one `questions.md` row.

**One of them reproduced the class it was closing, and it was caught by the
checker rather than by a reader.** The S5 closure's paragraph was written
inside `## Not verified`, which `unverified_check` reads as a table — exit 1,
`a line inside the table that is not a table row`, three times. That is
finding 8's class, in the commit closing round 2's corrections. The paragraph
has a heading of its own now and the check exits 0.

## Verification

| What was run | Result |
|---|---|
| `bin/evidence-check --strict .` | 1121 ok · 0 drifted · 0 broken, exit 0 |
| `bin/unverified-check --baseline origin/release/v0.11.1 seal/specs/` | exit 1 on the S5 paragraph, then **exit 0** after the heading was added; Q6's row prints as `open` |
| `bin/survivor-check --range bfe8cdb..HEAD --exempt .../survivors.md` | every survivor excused (2), exit 0 |
| the same over `origin/release/v0.11.1...HEAD` | every survivor excused (36), exit 0 — 31 records, 5 loaded |
| `grep -o "\| 2026-..* \|" seal/ledger.md \| wc -l` and the doubled form | 476 single, 0 doubled at the tip |
| `gh api repos/:owner/:repo/milestones/{40,42,43,44}` and the two comment ids | each opens with the sentence phase 5 wrote — S5 closed |
| broad gate | **not run.** The `sealer`'s, and it is next |
