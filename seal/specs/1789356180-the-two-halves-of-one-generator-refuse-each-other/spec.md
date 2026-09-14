# Feature Specification: the two halves of one generator refuse each other

<!-- seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Six tickets, and every one of them is a place where `round_record.py new`
writes a round record that `round_record.py close` then refuses, with a person
standing in between hand-editing a generated file. That much the milestone
already says.

**The frame's main finding is that the seam is not the one the tickets name.**
The release's own notes group #321, #341 and the `fixed`-outside-the-tree case
as *one decision about what `close`'s verdict vocabulary is for*. That grouping
puts three defects in one place and two of them are not there. The `—` in a `#`
cell is refused by `finding_number`, which reads the **`#` column**; the
correcting SHA is refused by `fix_table`'s verdict branch, which reads the
**Verdict column**. The two never meet in the code, they are argued on different
grounds, and a mechanism that answers either one leaves the other exactly where
it was.

Cut by the column of the record each disagreement is about, the six tickets are
**three changes**:

| Column of `rounds/round-N.md` | Tickets | The one question |
|---|---|---|
| `#` | #321 (its body), #341 (its body), #353 | what a verdict row that commissions nothing is |
| Verdict | #341 (its comment), #273 part 2, #321's comment on `fixed` | what the fix pass's verdict vocabulary admits |
| Grounds | #391 both halves, #273 part 1 | what `close` writes into a cell it was not asked to change |

#323 is in none of them, and §*What the tree says that the tickets do not* below
is why.

## What the tree says that the tickets do not

Every claim in this section was re-derived against
`fix/321-323-341-273-353-391-the-two-halves-of-one-generator-refuse-each-other`
at `e387bff`, under `skills/agent-contract/SKILL.md` §5. Nothing here is
executed; all of it is **read**, and the counts are read by a script over
committed files rather than by running the tool.

### 1. #323's first answer shipped one release ago, and the refusal it quotes is gone

#323 says `chain_check` tells you to record the broad gate with
`round_record.py close --broad-gate`, and that this command cannot be run at
that moment because `close` refuses a second application.

**Read**: the sentence the ticket quotes —
*"Run it once now that the rounds have settled, then write the SHA it ran at
and the base it was compared against into the cell"* — returns nothing from
`skills/`, `docs/` or `agents/`. The arm that used to carry it now says to
spawn the `sealer`, which runs `broad-gate --base <base> --record <item>`.

**Read**: `round_record.py#seal` exists and is exactly #323's answer 1 — a
`--broad-gate`-only path that takes neither `--fixes` nor `--range`, reads no
verdict row and writes one cell. Its docstring names the same measurement
#323's body does, down to the fix table with a header and no rows. It landed at
`c84f259`, *the sealer, its command, and its one cell (#30)*, which is in this
branch's history.

**Read**: #323's answer 3 largely landed with it.
`skills/code-review/orchestration.md` §*The last record's `Broad gate` cell*
now says the sealer's spawn is the route, and that `close --broad-gate` is for
the one case `seal` refuses by design — fixes and the gate landing in one pass.

What is left of #323 is its answer 2, and only in one place: the second arm of
`chain_check`'s broad-gate refusal, the one for a cell with no SHA-shaped word
in it, still offers `close --broad-gate` beside the sealer. That arm describes
the gate-then-close order, which is runnable. So the residue is a sentence,
not a defect, and **Q3 of `questions.md` asks whether the ticket closes here.**

### 2. #321 is two defects under one number, one in each of two columns

#321's body is about the `#` column: `new` copies a `#` cell through
`copied_row` validating nothing, and `finding_number` — reached only from
`fix_table` and `verdict_rows`, both on the `close` path — is the only reader
that validates it. **Read**: `copied_row` is called at one site,
`round_record.py#table_of`, and applies `row_cells` and `escape` and nothing
else.

#321's comment of 2026-09-14 carries a second defect that its body never
mentions: `fixed` cannot take a repair made outside the tree. **Read**:
`fix_table`'s `fixed` branch requires `chain.SHA_RE.search` to find a commit in
the third cell, and `close` then requires that commit to resolve in the
repository and to lie inside `--range`. A `gh issue edit` and an edit to a pull
request body produce no such commit, so `fixed` is unusable for either, and the
repair has to be written as `answered` with the repair described in the grounds.

That is the same fork #341's comment describes, one ticket over. It belongs
with the Verdict column and not with the `#` column, which is why this spec
splits #321 across two phases rather than treating it as one.

### 3. The two documents already disagree about the correcting SHA, and a case pins both spellings

#341's comment reports that `docs/review-chain-spec.md` prescribes
`answered — corrected at <sha>` and that `close` refuses it. Both halves hold.

**Read**, and the ticket does not say this: `agents/smith.md:156` already
carries the other spelling — *closes `answered` with `corrected at <sha>` as
its grounds, never `fixed`* — which is the shape `fix_table` accepts today. So
the repository ships both readings.

**Read**: `tests/test_the_rules_have_one_owner.py#test_a_correction_row_closes_answered_and_never_fixed`
asserts **both** sentences, in one case. The disagreement is therefore pinned
rather than merely present, and whichever fork Q2 takes, that case is edited.

**Read**, and it decides Q2's default: nothing machine-reads a SHA out of an
`answered` cell. `chain_check.py:2426` skips every row whose verdict is not in
`FIX_WORDS` before it looks for a commit, and `docs/review-chain-spec.md:1250`
states the same thing — a verdict closing with `answered` passes whatever commit
sits in the cell.

### 4. #273 part 2's preferred answer is already what the records do

#273 part 2 says a reviewer closing a finding as `already deferred` writes a
phrase `CLOSED_WORDS` does not read as closed, so the finding stays open and
`close` demands a row that overwrites the reviewer's verdict. It offers two ways
out and prefers the second — make `deferred <home>` cover it.

**Read**: no document tells a reviewer to write `already deferred` in a
**verdict** cell. `agents/warden.md:235` says *"Name it as already deferred, and
where"* about `round-N.md`'s **Deferred** field, which is a different table and
is not read by `verdict_of` at all.

**Read**: the two records in the tree that met this wrote the preferred shape
already — `| deferred questions.md Q4 | already deferred in round 1; not
re-opened |`, in `seal/specs/1788993115-…/rounds/round-2.md` and `round-3.md`.
The verdict cell is `deferred <home>`, and `already deferred` is grounds.

So part 2 has no live carrier. What is left is whether the documents should say
which cell the phrase belongs in, which is a sentence in `agents/warden.md` and
in `templates/sdd-round.md`, and whether `already deferred` is admitted to the
vocabulary at all. This spec's answer is that it is not — see Scope.

### 5. `close` discards a cell on two verdict words, and #391 names one

#391 reports that a `deferred` row's grounds are reduced to the home alone, and
asks, as an item for whoever builds it, whether any other verdict word reduces
its cell the same way. **Read**, from `close`'s write pass — the answer is yes,
and the two losses are different:

| Verdict written | What the cell was | What `close` leaves | What is lost |
|---|---|---|---|
| `fixed` | the reviewer's grounds | `fixed at <sha>` and the note, then `; ` and the old cell | nothing |
| `answered` | the reviewer's grounds | the fix table's third cell | **the reviewer's grounds** |
| `deferred` | the reviewer's grounds | the home, alone | **the reviewer's grounds and the fix pass's prose** |

`fixed` is the one word that preserves what stood. So the class #391 names is
three rows wide, not one, and the fix is owed to the class
(`skills/agent-contract/SKILL.md` §12).

### 6. What the corpus holds

Counts read on 2026-09-14 over the committed `seal/specs/*/rounds/round-*.md`
of this branch, by a script applying the module's own patterns. These are
**read**, not executed: no subcommand was run.

| What was counted | How many |
|---|---|
| verdict body rows in committed records | 1,992 |
| of those, rows whose `#` cell `FINDING_ID_RE` refuses | 253 |
| of those, rows whose cell carries digits — round-prefixed ids, the shape the rule deliberately refuses | 199 |
| of those, rows whose cell carries **no digit at all** — `🟡 A`, `🟢 fix-surface`, `carried` | **54** |
| rows in reviewers' reports whose `#` cell is a bare `—` | 21 |
| verdict rows whose Grounds cell is its home repeated and nothing else | 66 |
| verdict rows carrying `fixed at <sha> — ` followed by an empty code span | 103 |

The 54 and the 21 are what says the id-less row is a shape reviewers reach for
rather than a one-off: a non-numeric `#` cell is written about once in every
thirty-seven verdict rows this repository has committed.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The finding id — a bare integer, behind an optional severity marker* | the `#` cell's rule, the corpus argument behind it, and the three documents that have to state it. A row admitted without an id is a change to this section, not an exception to it |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | the sentence prescribing `answered — corrected at <sha>`, which is one of the two sides Q2 chooses between |
| `docs/review-chain-spec.md` §*`Fixes checked by` has to name a checker the repository can confirm* · §*The fix surface* | the two rows phase 4 touches, and the pairing `chain_check` refuses between them |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | all four burdens apply — `chain_check` is a gate and `round_record.py` writes what it reads. A test seen red, a stated failure direction, a prompt budget, platform honesty, answered in the pull request body |
| `skills/agent-contract/SKILL.md` §12 | the fix is owed to the class. §5 of this spec is one enumeration; phase 1's is the other |
| `skills/agent-contract/SKILL.md` §14, §15 | a changed refusal is documented and pinned in the same commit, and every new case is seen red first |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`; neither `CHANGELOG.md` nor `seal/ledger.md` is appended to |
| `CLAUDE.md` §*a ledger coordinate names content, never a position* | every row this work writes anchors on `path#unit@hash` |

## Scope

### In

1. **A verdict row that commissions nothing.** `close` stops demanding a fix
   table row for a row that is not an open finding, and stops writing a verdict
   word over one. Two spellings are members: a row with no finding id, and a row
   whose verdict is `❓ out of verified scope`. Covers #321's body, #341's body
   and #353.
2. **A refusal that names every offending row rather than the first.** #303,
   merged into #321, measured five offending rows and a message naming one, at
   two round trips per repair. This holds under every answer to Q1 and is not an
   alternative to any of them.
3. **The fix pass's verdict vocabulary**, settled once and stated in one place.
   Three cases fall under it: the correcting SHA (#341's comment), `fixed` on a
   repair made outside the tree (#321's comment), and `already deferred`
   (#273 part 2).
4. **What `close` preserves in the Grounds cell** — all three verdict words, per
   §5 above, not the one row #391 names. Covers #391 part 1.
5. **The empty code span** beside a fix commit, at `round_record.py#fix_table`'s
   `note` line and not in `chain.SEPARATORS`, which the standing `# RIDER:` at
   that coordinate already says. Covers #391 part 2.
6. **`Fixes checked by` after a fix table applies** — #273 part 1, subject to Q4.
7. **The documents the reviewer and the fixer read**, edited in the same commit
   as the behaviour each states: `agents/warden.md`, `agents/smith.md`,
   `templates/sdd-round.md`, `skills/code-review/SKILL.md`,
   `docs/review-chain-spec.md`, `skills/implement/SKILL.md` §5 where its
   vocabulary sentence moves.

### Out, each with the reason

| Left out | Why |
|---|---|
| **#323's residue**, unless Q3 answers otherwise | its answer 1 shipped at `c84f259` and its answer 3 shipped with it. What remains is one sentence in one refusal arm that offers a runnable order. Building a phase for it spends a round on a ticket the tree has already closed |
| **Rewriting the 66 deferred rows and the 103 empty spans already in committed records** | a round record asserts a **past** state, which is the property that lets it live beside the contract (`skills/implement/SKILL.md` §*Document layout*). A row rewritten now would assert a state that was not true at its own `Target SHA`. Q6 leaves the migration-arm question to the phase that meets it |
| **Accepting a round-prefixed id** (`R2-1`, `r3 🟡 2`) | `docs/review-chain-spec.md` §*The finding id* measured the corpus both ways: the rule takes away two wrong answers and no right one, and the 199 rows above are that shape. #341's own body agrees — *let the record's own file name carry the round* is the rule it keeps |
| **A second match site for `FINDING_ID_RE`** | `tests/test_a_finding_id_is_a_bare_integer.py#test_the_rule_is_one_constant_both_tables_read` asserts the pattern is matched in `finding_number` and nowhere else. Whatever phase 1 builds goes through that function |
| **Widening `chain.SEPARATORS`** to strip the backtick | the standing rider at `fix_table` says why: that constant is shared with the `deferred` home reader and with `chain_check`'s own readers, and widening it would strip a backtick off a home deliberately written as a code span |
| **Anything in `round_record.py#terminal_value` or `#BLOCK_START`** | the sibling work item of this release owns that seam and shipped it at `5bae06e`. Neither touched `#fix_table`, and this work does not touch theirs |
| **A fourth severity marker, or a new report table** | #353's shape 3 moves `❓` rows out of the verdict table into a section of their own. It is the largest of its three shapes and it changes what `new` parses out of a reviewer's report, which is the seam the sibling work item just finished. Scope 1 reaches the same outcome inside the table |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A confirmation row survives the round | **Given** a report whose verdict table holds six rows the round verified and did not open, written without a finding id · **When** `new` writes the record and `close` applies a fix table holding no row for them · **Then** both commands exit 0 and the six rows stand in the record as the reviewer wrote them | a case over `new` then `close` on a fixture report, seen red against `e387bff` |
| A scope marker keeps its own word | **Given** a verdict row reading `❓ out of verified scope` · **When** `close` applies a fix table with no row for it · **Then** `close` exits 0, the row's Verdict cell still reads `❓ out of verified scope`, and `Pass` is decided without counting it open | a case over `close`, seen red against `e387bff`, where the same fixture refuses |
| A malformed id is still refused, and every one of them is named | **Given** a verdict table with five rows whose `#` cells are `R2-1` … `R2-5` · **When** `close` runs · **Then** it refuses once, naming the format and quoting all five rows | a case asserting five quoted rows in one message, seen red |
| An earlier round's closure has a spelling | **Given** a round 3 report answering round 2's findings 1 and 2 while opening its own findings 1 and 2 · **When** `new` and `close` run · **Then** neither refuses for a duplicate id, and the record distinguishes the four rows | a case over both commands, seen red |
| A correction closes in the spelling both documents give | **Given** a fix table row for a finding located under `seal/specs/` · **When** `close` applies it in the spelling `docs/review-chain-spec.md` prescribes · **Then** it is accepted | a case over `fix_table`, plus `test_the_rules_have_one_owner.py` rewritten to assert one spelling in both files |
| A repair made outside the tree has a verdict | **Given** a finding repaired by an edit to a ticket or a pull request body, with no commit in the branch · **When** the fix pass writes the row the vocabulary provides · **Then** `close` accepts it and the record says where the repair is | a case over `fix_table`; the document that states the rule asserted in the same commit |
| A deferred row keeps its reasoning | **Given** a fix table row `deferred #N` whose third cell carries a paragraph · **When** `close` applies it · **Then** the record's Grounds cell holds that paragraph and the home, and the row is not reduced to `#N` | a case over `close`, seen red; the 66-row count re-measured after |
| No verdict word discards a cell it was not asked to change | **Given** a verdict row with reviewer's grounds and a fix table row for it · **When** `close` applies `fixed`, `answered` and `deferred` in three runs · **Then** none of the three leaves the reviewer's grounds unreachable | one parametrised case over the three words, seen red on two of them |
| A fix commit carries no empty code span | **Given** a fix table row whose third cell reads ``fixed at `<sha>` `` · **When** `close` applies it · **Then** the Grounds cell holds no empty code span | a case asserting the rendered cell, seen red; the 103-row count re-measured after |
| A capped run's last record says something true about its fixes | **Given** a record whose every verdict closes on a fix and which has no next round · **When** `close` applies the table · **Then** `Fixes checked by` does not still read *the fixes are not yet written* · **And** `chain_check` does not refuse the pair | a case over `close`, and the existing `chain_check` fix-surface arm run against the same record |

## Data & interfaces

No schema, no endpoint, no payload. The interfaces this work changes are three
cells of one generated file and the messages that refuse them:

| Surface | Unit | What changes |
|---|---|---|
| the `#` cell | `round_record.py#finding_number` · `#verdict_rows` · `#fix_table` · `#close` | which cells key a row, and which rows `close`'s open-finding computation reaches. One match site for `FINDING_ID_RE` stays one |
| the Verdict cell | `round_record.py#fix_table` | which verdict spellings a fix table may hand over |
| the Grounds cell | `round_record.py#close` write pass · `#fix_table`'s `note` line | what survives from the cell that stood there |
| the `Fixes checked by` row | `round_record.py#landing_values` · `#close` · `chain_check.py`'s fix-surface arm | the reason the cell carries after a fix table applies |
| the refusals | the `Refused` messages in the units above | one refusal naming every offending row; §14 applies, so each changed message is pinned by a case in the same commit |

The evidence rows this work adds go to
`seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md`,
anchored `path#unit@hash`. The changelog entry goes to
`seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/changelog.md`.

## Open questions → questions.md

Four rows need a person and none of them is answerable by reading: the
mechanism for a non-commissioning row (Q1), whether the correcting SHA is meant
to be machine-readable (Q2), whether #323 closes as covered (Q3), and whether
#273 part 1 has to be in effect before the next work item starts (Q4). Two more
rows are not a person's: Q5 is a measurement the build takes, Q6 is a decision
the phase that meets it makes.
