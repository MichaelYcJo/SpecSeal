# 1790076080-every-orchestrator-rule-is-a-sentence — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `61cd0dad` |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The nineteen-row table and the case holding it from both sides. The table
lives in a new `## Orchestrator: which of these acts runs itself` section of
`skills/implement/orchestration.md`, one row per marked heading, each row's
`Delivered by` cell holding one of four values and nothing else — a command
that exists, a check that exists, `part of its parent's act`, or `still a
sentence` with grounds.
`tests/test_every_orchestrator_act_names_its_delivery.py` fails four ways,
each shown red first: a marked heading with no row, a row naming a heading no
file carries, a row naming `bin/does-not-exist`, and a `still a sentence` row
with an empty grounds cell.

Two standing instructions shaped it. **Reuse the reading that already
exists** —
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` parses
the `Orchestrator:` marker at `##` and `###` — rather than writing a second
parser. And **Q2 is this phase's work**: which `Delivered by` value is true
for each heading is decided with that heading's section open, because a cell
decided from the heading alone is the assertion contract §5 refuses.

Q1 was one command, run here and recorded below.

## What this phase found

**The table has twenty rows, not nineteen, and the frame says both things.**
`spec.md` §Scope states the row set as *every `##` heading whose text begins
`Orchestrator:` in either orchestration file, plus every `###` heading
directly beneath one*, and then says in the same bullet that putting the
table in a new `Orchestrator:` section *"makes the section a row of its own
table"*. Nineteen is the count of the class **before** this phase writes
anything; the rule the same paragraph states produces twenty the moment the
section exists. Measured both ways: the parser read exactly the nineteen
headings `plan.md` lists at its stated line numbers against the tree as it
stood, and twenty after the section landed. The table carries twenty rows and
`test_the_table_reads_the_section_that_holds_it` pins the self-reference, so
the one act nothing would otherwise count is counted. Exempting the section
holding the table was the alternative and it was rejected: an exemption is a
special case that hides an act, which is the state #330 reports.

**The ticket's premise is false of three quarters of the class as the tree
stands today, and that is the phase's own measurement.** #330 says every rule
reaching the orchestrator is a sentence it has to remember. Reading all
twenty sections, the delivery splits:

| `Delivered by` | Rows |
|---|---|
| `check: <path>` | 8 |
| `command: <path>` | 5 |
| `still a sentence` | 5 |
| `part of its parent's act` | 2 |

The distinction that makes this true rather than a contradiction of the
ticket: **every one of the twenty is still described in prose.** What
**thirteen** of them now have is something that refuses, or says so, when the
act did not happen — the 8 checks and the 5 commands the table two lines above
counts. **Corrected 2026-09-22 in round 2's fix pass:** this read *fourteen*,
which contradicted both its own tally table and the corrected passage below
it, and round 1's correction had repaired the denominator further down this
file without repairing it here. The names are
`hooks/commit-review-gate.py`, `hooks/mode-gate.py`,
`skills/code-review/scripts/chain_check.py`, `bin/round-record`,
`bin/evidence-check`. The ticket was filed on 2026-09-10 and measured three
misses; the tree has been closing this class steadily since, one act at a
time, and nobody counted. The five rows still reading `still a sentence` are
what a next work item picks from, and they are the answer to the ticket's
*which acts get one* that no reading of the headings could have produced.

**The four values needed a decidable question behind them, and the frame did
not supply one.** Several sections carry more than one act — *a fix pass
resumes the implementer* also holds the fix table, the range rule and the
survivor sweep — so *what delivers this section* has no single answer. The
question the section now states is **when the orchestrator forgets this act,
what notices?** That is decidable per heading, and it is paired with a
discipline the spec's own §*The limit this work does not close* already
demands of one row and this phase applies to all of them: **the grounds of a
row whose delivery reaches only part of its act name the part it does not
reach.** **Corrected 2026-09-22 in round 1's fix pass:** this said *eight
rows* and the count was never taken — it is **twelve of the thirteen
delivered rows**, after round 1's finding 4 gave the thirteenth's neighbour
the sentence it was missing. The one that carries none is `Then say who
checked them, in the record`, which has no gap to name: `close` handles the
capped run's last record explicitly and the verifying-round row's own check
covers the rest. Round 1 read the count as *eleven of fourteen*; eleven was
right before finding 4 was fixed and fourteen was not — `command:` and
`check:` rows number thirteen, and the reviewer's own list of eleven plus two
sums to that. Two examples, both found by
reading rather than inferred: `Orchestrator: closing the cycle` is delivered
by the commit gate's review arm, and on a branch with a routing declaration
in force that arm is already quiet, so for every branch this workflow routes
the missing mark is never noticed. `A fix pass adds the unit that pins it` is
delivered by `round-record close`, which refuses depth 2 — and the level
above it, *a fix pass may not add mechanism*, is refused by nothing.

**Q1 is answered (a), measured rather than reasoned.** `gh issue list --label
<name> --state all` against a label that exists nowhere exits **0 with empty
stdout and empty stderr** — run against this repository with the control
label `zzz-no-such-label-9x`. The same command with `flow-measurement`
returned five rows, one OPEN and four CLOSED, which is the log this
repository actually runs. So phase 2's *no history at all* state is the
empty-output branch, and a non-zero exit is a lookup that failed. The mode
must fall to **silent no-op** on non-zero, never to *post*: the failure
direction `plan.md` states makes a wrong refusal cost one reading a person
posts by hand, where a wrong post writes into a tracker.

**Q2 is answered with every section open**, which is what the phase was for.
Two readings changed on contact with the section and are worth naming because
the heading alone would have given the other answer. `Orchestrator: the pull
request opens before round 1, and a phase is re-run` reads as delivered from
its heading — `chain_check.py` is all over that section — but nothing reads
*when* the pull request opened, and nothing records that a closed phase's
suite was re-run, so the row is `still a sentence` with the delivered step
named in its grounds. `What the answer writes` reads as `part of its parent's
act` from its position under the routing question, and is not: `chain_check`
refuses a `Review` or `Destination` value outside the vocabulary, which is an
act of its own.

**One rule of the row set was underdetermined and is now pinned.** *Every
`###` directly beneath one* can mean the nearest `##` or the nearest marked
`##`. Read the second way, every `###` after the last marked section is swept
in, which in `skills/code-review/orchestration.md` would be most of the
document. `acts` takes the nearest `##`, and
`test_a_third_level_heading_under_an_unmarked_section_is_not_an_act` holds
it.

**How each case was shown red (contract §15).** The real-tree case was run
before the section existed and failed on the table's header line being
absent, naming the file. Each of the four planted directions builds a temp
tree with one defect and asserts the finding names it; a floor case,
`test_a_clean_planted_tree_is_clean`, asserts the same tree without the
defect is clean, so none of the four is passing over a tree that was already
dirty. Then every unit the phase added was broken one at a time and the
module re-run: eight mutations — `headings` refusing `###`, `acts` dropping
the `###` arm, `rows` skipping a row, `findings` dropping each of its two
sides, `_delivery` dropping the grounds demand and the path-exists demand,
and `_bare` keeping backticks — and all eight went red, with the tree
restored from kept bytes and green afterwards.

**Corrected 2026-09-22 in round 1's fix pass: the sentence above about the
floor case was false, and it is the reason to re-run the four directions
rather than take their old reds on trust.** `_delivery` resolved a named path
against this module's own repository instead of against the root `findings`
was handed, so `test_a_clean_planted_tree_is_clean` was clean because the
check never asked the planted tree anything — the path `SELF`'s row names was
absent from that tree, present in the repository, and reported by nobody.
Measured both ways with the two module versions side by side: at the reviewed
commit the floor tree does **not** carry the file its own table names and
`findings` still returns `[]`; repaired, the tree carries it and `findings`
is `[]` for the right reason. So *none of the four is passing over a tree that
was already dirty* was exactly what could not be claimed.

Re-run after the repair, this is what each of the four now demonstrates, and
one of them changed:

| Direction | What it demonstrated | What it demonstrates now |
|---|---|---|
| A1 · a marked heading with no row | unchanged — the row set is read from the tree under check on both versions | an act the planted tree carries and the planted table does not |
| A2 · a row naming a heading no file carries | unchanged, same reason | a row the planted table carries and the planted tree does not |
| A3 · a row naming `bin/does-not-exist` | **a path absent from the REPOSITORY is named.** `bin/does-not-exist` is absent from both trees, so it could not tell the two apart and was red for a reason narrower than the case claimed | a path absent from the tree under check is named |
| A4 · `still a sentence` with empty grounds | unchanged — the cell is read off the table, and no path is resolved | a grounds cell the planted table leaves empty |

A3's red was never wrong, only weaker than its name, and the shape that
separates the two is a path the repository HAS and the tree does not:
`test_a_named_path_is_resolved_against_the_tree_under_check` uses
`bin/round-record` for that, and it is **0 findings at the reviewed commit
against 1 after the repair** — executed, with the case lifted onto the
reviewed module so it ran against the reviewed `_delivery` and `_tree`, and
failing there on `assert 0 == 1`.

**What was run**, executed, output read: the new module and the neighbour
together (22 passed), the fourteen neighbouring document modules that read
either orchestration file or sweep the shipped documents (549 passed, 7
skipped), and `uvx ruff check` plus `uvx ruff format --check` on the two
changed Python files (exit 0, exit 0). The full suite is `unverified` and is
the sealer's, once, after the rounds settle.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `marked_headings`'s body and the fence reasoning in its docstring | `headings` in the same module, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`. `marked_headings` keeps its name, its signature and its return shape, and is now a filter over `headings`; every sentence of the fence reasoning stands, one function up, and both modules read that one parser |
