# who asks the routing question, and what checks the answer — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `seal/specs/1789518345-…/{spec,plan,questions,routing}.md`; `CLAUDE.md` §*a change writes fragments, never the shared file*, §*a thing more than one party can have is named with whose*, §*The goal a design is chosen against*; `skills/implement/SKILL.md` §1 and §3; `docs/review-handoff-protocol.md`; `seal/follow-up.md`; issues #88, #399, #419
· evidence: `seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md` — written at phase 7
· verified: per phase, in `phases/phase-N.md` and in `plan.md`'s Status column. The broad gate is the sealer's and is unrun here

## Why this work exists

One act — a person being asked how a work item is routed — was described by
three documents that disagreed about who performs it, shaped by a question that
could not say the thing people most often want to say, and checked by nothing.
After this the framer asks it, the question can say *do not come back*, and a
work item that declares a framer and draws no frame is refused at the pull
request.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The fifth row's name and values | `spec.md` §*The fourth row* shipped `Attendance`, values `nobody at the keyboard` · `somebody may be asked`; `plan.md`'s Alternatives table had rejected `Automation` | **`Automation`, values `yes` · `no`** | The owner's answer to `questions.md` Q1, given at the approval — which is the party and the moment that row named. Three grounds: it is the owner's own word, it is already question 1's first option label so the button pressed and the row recorded are one word (#88's request one level down), and `Attendance` reads as a school register first. The collision sweep was run before it landed: all 40 occurrences of the word in this tree are the ordinary English noun. `spec.md` and `plan.md` were brought to the answer rather than left disagreeing with the code |
| What the shorter values give up | `nobody at the keyboard` carried its own meaning; `no` does not | **the shorter values, with the meaning moved one line up** | `no` reads first as *a person did this by hand*, which is wrong — it means *this run may stop to ask*. That half now lives in `templates/sdd-routing.md`'s comment, in the constant's comment in `hooks/routing.py`, and in the box's unchecked cell. The trade is a value a person types correctly against a meaning they read one line up for |
| Where the owner's personal routing paragraph is edited | The spawn said `~/.claude/CLAUDE.md` is out of scope and owed only a changelog line; a mid-run correction said the block's one source is the repository's own `CLAUDE.md` | **`templates/claude-md-block.md`, with `CLAUDE.md` regenerated** | Neither was right. `install.sh` lines 43–47: the block used to be read out of the repository's `CLAUDE.md`, #292 measured the two copies and found `## Git` 95 % identical with one sentence moved in one and not the other, and the source is now `templates/claude-md-block.md`. The repository's `CLAUDE.md` carries a generated copy that `.github/scripts/claude_block.py --write` regenerates and CI checks. Editing `CLAUDE.md` directly would have been overwritten by the next regeneration and would have shipped the old paragraph to every installer. Nothing under `$HOME` was touched |
| This work item's own `Framed` line | `plan.md` rule 2: the framer's definition is read at spawn time, so phase 3's edit cannot reach the session that wrote these documents | **written by `smith`, naming `framer`** | The line records a true fact — a framer did frame this work item — and it is the one instance where the party that writes the mark is not the party it names. Every work item after this one has the framer write it. Recorded here rather than left for a reviewer to notice that the mark predates the instruction to write it |
| Where the cutoff lives for the seal arm | `plan.md` gives a cutoff to phase 6's arm and none to phase 5's | **phase 5's arm got one too**, `DIRECT_GATE_FROM`, at this work item's id | The identical retroactive-red hazard: 16 declarations answer `straight to the PR` and not one carries a `broad-gate.md`, because the file did not exist. A release pull request carries every work item the release adds. Shipping one arm with the mechanism and its twin without it is the near-identical-copy-missing-one-half failure this repository keeps recording |
| How much of `agents/smith.md`'s phase 2 the design gate is | `plan.md`'s Technical context locates it at lines 53–72 | **the span by content, PLUS the asking clause sixty lines below it** | *Present 2–3 approaches with failure scenarios and wait for an explicit go* is the design gate by content and sat outside the named range, so a removal keyed on the span left the file saying *phase 2 is your caller's spawn* in one paragraph and *wait for an explicit go* in another. The rung CONDITION stays — `test_the_top_rung_names_behaviour_rather_than_a_count` requires `observable behaviour` in that file, and a smith below the top rung still needs to know what the work owed |
| How many things the frame arm cannot see | `plan.md` and `spec.md` §S20 say **six**; `spec.md`'s own list has **seven** bullets | **seven, in the module** | All seven are real. The case asserts the phrases rather than the number, so it pins the disclosure instead of the arithmetic |
| Who asks the routing batch | `spec.md` §Scope 4 and #419 both send the act to the framer; the build did that | **the session that spawns the work**, reversed at round 1 | **A subagent in this harness has no `AskUserQuestion` and no equivalent** — measured from two agents independently, `warden` in round 1 and `smith` in the fix pass, each declaring no `tools:` key and inheriting the full set: the tool is absent from the list and `ToolSearch` returns *No matching deferred tools found*. A framer told to ask is told to call a tool it does not have; one told to write `routing.md` first writes an answer nobody gave, which is #151's shape arriving through the door this work opened. #419's finding survives whole — the acts are not `smith`'s — and only their destination was wrong. `spec.md` §Scope 4, S10 and `changelog.md` were brought to the answer |
| Which direction of the seal's misfiling to close | Round 1's 🟡 1 reproduced the chain-declared direction and named the direct-declared one without a case | **both, in one fix** | The report says one fix covers both and it does: each comes from `seal_home` choosing the home without reading the declaration. A fix aimed only at the reproduced direction would have left half the class standing (§12), so `seal_home` reads the `Review` row and two cases hold the two directions |
| Whose the `--reverify` sweep is | The plan's phase 7 says to run `bin/evidence-check --strict .` | **the drifted rows were re-READ first, one at a time, and two were corrected rather than re-stamped** | A whole-tree `--reverify` rewrote 27 hashes on its first run, 21 of them in the shared `seal/ledger.md` and belonging to earlier work items — which records that somebody re-read claims nobody had opened. Those were reverted and each drifted row was read. Two had been narrowed by this branch and were corrected in place: `round_record.py#seal`'s row said the cell goes on the LAST record and touches nothing else, and `chain_check.py#broad_gate`'s row counted three fatal refusals as the module's where they are that function's |
| `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox` | `plan.md` phase 1 said to reword it where it names `Planning` by position | **renamed and both count assertions removed** | Both of its assertions were counts — `len(boxes) == 3` and `"four axes" not in skill` — and neither is what #88's rule is about. Both would have gone red at phase 2 for a change the rule PERMITS, and a reader meeting that red would have read it as the rule being broken. It is now `test_the_planning_row_is_a_record_and_not_a_checkbox` and asserts by name |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Every phase and the round-1 fix pass ran their own slices and read the exit codes directly; the broad gate is one act with one owner and it is the sealer's | the orchestrator, by spawning the sealer after the rounds settle |
| Whether a session reading the new two-question shape actually asks it in one `AskUserQuestion` call. The cases pin the document, and a document is not a run. Round 1 settled the prior question — whether a SUBAGENT can ask at all — in the negative, which is why the act is the session's | the orchestrator, at the first work item framed after this ships |
| Whether `evidence-check`'s records arm can be satisfied for round 1. Renaming `test_a_direct_declaration_with_no_seal_is_a_notice_on_a_draft`, which the round asked for, makes three lines of `rounds/round-1.md` and `rounds/round-1-report.md` name a case the tree no longer has — and a fix pass may not edit either file, so `bin/evidence-check --strict .` exits 2 on records this pass is forbidden to touch | the orchestrator, by writing `NAME NOT IN TREE` beside the old name on those three lines, or by carrying the new name at `round-record close` |

## Not done

**Two tickets this work opens rather than closes**, both named here because a
leftover nobody can find was not handed over. Neither is a phase: the first is
defined by there being no work-item directory, and the second waits on a
measurement that does not exist yet.

- **A durable record that a person chose `no work item`.** Taking the exit
  writes no file, so a change that took it is indistinguishable from one the
  session never asked about — #151's shape exactly. It needs a home for a
  record belonging to no work item, which this repository does not have: the
  two candidates today are a shared file every branch appends to, which
  `CLAUDE.md`'s fragment rule forbids, and a commit-message convention nothing
  reads. **Who must answer it:** the repository owner, at the ticket.
- **Promoting the approval-line notice to a refusal.** #399's `Done when` asks
  for a refusal; this ships a notice, on a measurement the ticket did not
  have — 61 of 71 `plan.md` files carry the unfilled placeholder, and 3 of the
  11 work items declaring a framer are among them. The promotion is worth
  taking once the notice has been seen on a few releases and the figure has
  moved. **Who must answer it:** the repository owner, after two or three
  releases carry the notice.

**A third thing was found and left**, and it is not a ticket because it is one
line of prose: `plan.md` and `spec.md` §S20 say the frame arm discloses **six**
things it cannot see, and `spec.md`'s own list has seven. The module carries
seven. Corrected in this work item's own records rather than chased.

**A third ticket, opened by round 1's 🟡 4.** A sweep over `agents/*.md` for
every tool an agent cannot reach needs a list of what each agent has, kept in
step with the harness — that is **mechanism**, which a fix pass may not add
(`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
it*). What this pass added instead is one case holding the one name that was
measured, `AskUserQuestion`, over the `agents/*.md` glob. The general sweep is
the ticket. **Who must answer it:** the repository owner.

**All three tickets are for the ORCHESTRATOR to open**, not for this agent:
§6 withholds posting from every agent this plugin spawns.

## Fed back into the spec

`spec.md` §*The fifth row* gained a paragraph recording that the name and its
values are the owner's, given at the approval, with the three grounds and what
the shorter values cost. `plan.md`'s Alternatives table gained the row that
`Automation` was chosen over `Attendance` and why the frame's reason for
rejecting it stopped holding once question 1's first option took the same word.
Both are marked as decided at the approval rather than inferred during
implementation — they are an answer to `questions.md` Q1, which named that
moment.
