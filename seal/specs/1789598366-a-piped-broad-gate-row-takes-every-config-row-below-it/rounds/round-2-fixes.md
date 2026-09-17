# 1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it — round 2 fixes

Target reviewed `906c78b3`. Fix commits `c83cee76`, `7eca576d`, `a2e72ea6` and
`dd964ca9`, over the range `5137e934..HEAD`.

Round 2's one finding and its four corrections were each re-executed here
before anything was written (`agent-contract` §5). All five reproduce. The
measurement then widened the finding by three members and turned one of the
corrections into a different defect than the one it was filed as.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `c83cee76`. `hooks/config.py#refusal` answers about the TABLE: every line the reader will not take as a row, each with whether the reader got that far, the rows lost under the line that actually stopped it, and that line. The gate finds its own row among all of them and reads the cost off the stopping line, which gives the sentence four cases where a flat condition gave it two. The paste-ready fix was measured rather than adopted — it closes two of the five members and its cost chooser is false about the most ordinary file of all |

## What the class turned out to be

The reviewer named the class *a sentence about the table computed from one
line of it*, and that is the right name. It has **five members**, measured at
`5137e934` over ten config shapes, nine of them malformed on purpose. Two
are the ones the round reported.

| The file | What the gate said | What was true |
|---|---|---|
| ① the `Broad gate` row parses, under the SECOND refused line | *has no `Broad gate` row* | the row is on line 6 |
| ② the `Broad gate` line refused first, a second bad line lower down | *The rows below it were read* | `Record language` never arrived |
| ③ the `Broad gate` line is itself the second refused line | *has no `Broad gate` row* | the line is in the file, quoted back now |
| ④ the `Broad gate` line below the line that stopped the reader | *has no `Broad gate` row* | the reader never reached it, and it would not parse either |
| ⑤ the `Broad gate` line under a paragraph of prose above the table's first row | *has no `Broad gate` row* | `config_rows` steps past prose there and reads on; the walk gave up |

③ and ④ are the round's own 🟡 3 arriving one line further down — the message
this work item exists to end, in the shape the round did not open. ⑤ is the
round's fourth correction, which arrived filed as a `refusal` / `config_rows`
disagreement and is the same defect: a question about the table answered from
one line.

**All five are closed by one repair**, because all five have one cause. The
walk hands back the whole picture and every caller names the line its own
sentence is about.

## The paste-ready fix, measured

Its walk and the three-case chooser it feeds, transcribed verbatim into a
probe and run over the same shapes:

| | ① | ② | ③ | ④ | ⑤ | the `Broad gate` line last in its table |
|---|---|---|---|---|---|---|
| the paste-ready fix | closed | closed | still absent | still absent | still absent | **newly wrong** |

The last column is the cost chooser's first branch, `if not below`. A
`Broad gate` line written as the last row of its table loses nothing below it
because there is nothing below it, so `below` is empty — and the sentence that
branch prints is *nothing had parsed above this line, so the table had not
begun*, to a person whose `Mode` row is one line above their eyes. `below`
being empty and the table not having begun are different facts, and reading
one as the other is the class the fix is for.

Keyed on the stopping line instead, the four cases are: nothing stopped the
reader; this line stopped it; this line was read and something lower down
stopped it; the reader had already stopped above this line and never met it.
`stopper` is what the branch asks about in every one of them.

Nothing else in the proposal was rejected. `stopper` is its idea and it is in
the repair; `rows_under` comes out for the reason it gives; `refused` is a
list rather than one line, which is what ③ and ④ needed.

## The mutation behind each fix

Every file restored from bytes the mutation script held, never from HEAD,
`tests/__pycache__` cleared between runs, exit codes read directly.

| Mutation | Result |
|---|---|
| the cost chosen by whether any row was lost rather than by the stopping line — **the paste-ready fix's own chooser** | exit 1 · both new cases, on the one-bad-line half |
| the cost collapsed back to two cases | exit 1 · both new cases, on the two-bad-line half |
| the hidden-row branch gated on the first refused line being the stopper | exit 1 · `test_a_second_refused_line_is_what_decides_what_a_first_one_cost` |
| `refused_broad_row` asking only the first refused line | exit 1 · `test_the_gate_reads_every_refused_line_and_not_only_the_first` |
| the walk giving up at prose above the table's first row | exit 1 · the same case, on ⑤ |
| every refused line reported as reached | exit 1 · the same case, on ④ |
| the hidden-row branch widened past `hides_this_row` | exit 1 · `test_a_refused_row_of_some_other_item_is_not_read_as_this_one`, the guard |
| both units put back to the commit before the fix | exit 1 · both new cases (`agent-contract` §15) |

Restored after each: exit 0, 145 passed.

**The case is red on which line the sentence describes, not on the sentence
existing.** Both new cases build two-refused-line files and one-refused-line
files together, so a walk pinned either way is red: the first two mutations
redden the same two cases on opposite halves, which is what a case asserting
only that a conditional sentence exists cannot do.

## The four corrections

**The changelog stated the repair without the condition it has** — closed with
finding 1, in `c83cee76`. The bullet a release-notes reader meets now says the
cost is read off the line that actually stopped the reader, that a line above
it costs nothing, and that the line being quoted can itself be below the
stopping one.

**Seven re-anchored ledger rows said nothing about who read them** — corrected
at `7eca576d`. The count reproduces: thirteen rows of `seal/ledger.md` had
their anchor's content moved by this branch, six carry a note and seven carried
a new hash alone, all seven anchored on the Bootstrap section. Each of the
seven was re-read against that section before anything was written on its row,
and each note says where the claim sits relative to the paragraph this branch
edited — which for all seven is one paragraph inside the second question, twice
rewritten. `CLAUDE.md` is untouched by this branch, so the preset half of the
last row cannot have moved. The cited cases are green. `overview.md` said four
claims and said each carries a note; it says thirteen and five now, and names
the pass that gave seven of them theirs.

**The limitation case named one of the four records** — corrected at
`c83cee76`. All four are in its message. This one cannot be shown red and is
not claimed to be: a message's text is not what pytest reads, so the case
passes just as well with the list cut back to a pointer, which was executed to
confirm rather than to pin. What the correction repairs is the value the case
has for whoever reddens it, and there is no way to pin that short of asserting
the message about itself.

**`refusal` gave up where `config_rows` keeps reading** — judged and closed
with finding 1, as member ⑤ above. It predates the branch, as the round says,
and it is the same unit and the same class, so closing it here cost one branch
of the walk and one fixture.

## The survivor exemptions, and why the round's diagnosis was wrong

The round asked whether rows that exempt nothing should keep being added.
The answer turned out to be that they exempt nothing for a reason nobody had
opened.

`survivor_check.py#exempted` matches an exemption row's first cell against the
candidate's **path**. Every one of this file's twenty-one rows was written
`path:line` — which is the spelling the check's own report prints for a
survivor, so it is an easy habit to acquire — and no such row can ever match.

**Executed**, one range, one run, two rows: `.github/scripts/close_issues_on_release.py`
with a bare path excused its place and printed under `exempt`;
`tests/test_waiver_decided_at_start.py:76` with the line number did not.
Rewritten bare, all twenty-one rows are live, and the fix range now answers
`every survivor is excused by a row above (5)` where it used to answer
`no removed wording is still standing` — the two sentences the checker's own
comment says must not read as one.

So the round's deferral of this to #371 / #308 is withdrawn for this file.
That defect may well exist; it is not what was silencing these rows, and
nothing here measured it either way.

**The habit is this file's own.** Counted across the tree: 201 exemption rows
carry a bare path and exactly one other carries a line number, in
`seal/specs/1789002694-…/survivors.md`. That row is another work item's and
is left alone; it is named here so it can be filed.

**And the rows stand.** All twenty-one, plus six this pass adds — five for the
fix range and one for the branch range. Each records a judgment somebody took
about a real place, and now each of them also does the thing it was written
to do.

## What was run

| What | Result |
|---|---|
| `bin/test` over `test_the_seal_is_taken_once_by_the_sealer.py` and `test_the_mode_question_is_asked_once.py` | exit 0 · 145 passed |
| `bin/test` over `test_the_settings_have_a_front_door.py`, `test_first_setup_asks_once.py`, `test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `test_the_pull_request_language_is_the_repositorys.py` | exit 0 · 200 passed |
| `missing_row` and `refusal` over ten config shapes, before the repair and after it | five wrong before, all ten correct after |
| the paste-ready fix's walk and chooser transcribed into a probe, over the same shapes | two closed, three still reported absent, one newly wrong |
| the eight mutations above, each restored from bytes | exit 1 each · exit 0 restored |
| `bin/evidence-check --strict .` | exit 0 · 1352 ok · 0 drifted · 0 broken |
| `bin/evidence-check --reverify .` | 9 rows re-verified, each claim re-read first |
| `bin/unverified-check seal/specs/` | exit 0 |
| `bin/survivor-check --range 5137e934..HEAD --exempt …/survivors.md` | exit 0 · every survivor excused by a row above (5) |
| `bin/survivor-check --range 0995f62f..HEAD --exempt …/survivors.md` | exit 0 · every survivor excused by a row above (1) — `0995f62f` is `git merge-base origin/release/v0.12.0 HEAD`, the range CI's relation resolves to |
| `bin/survivor-check` over both ranges with no `--exempt` | exit 1 · 5 and 1, which is what proves the rows are now what excuses them |
| `ruff check` and `ruff format --check` over the four touched files | exit 0 · exit 0 |
| the full suite, the repository-wide lint, the typecheck | **not run** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |
