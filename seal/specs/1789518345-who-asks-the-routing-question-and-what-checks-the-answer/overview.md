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
| `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox` | `plan.md` phase 1 said to reword it where it names `Planning` by position | **renamed and both count assertions removed** | Both of its assertions were counts — `len(boxes) == 3` and `"four axes" not in skill` — and neither is what #88's rule is about. Both would have gone red at phase 2 for a change the rule PERMITS, and a reader meeting that red would have read it as the rule being broken. It is now `test_the_planning_row_is_a_record_and_not_a_checkbox` and asserts by name |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Every phase ran its own slice and read the exit code directly; the broad gate is one act with one owner and it is the sealer's | the orchestrator, by spawning the sealer after the rounds settle |
| Whether a session reading the new two-question shape actually asks it in one `AskUserQuestion` call. The cases pin the document, and a document is not a run | the orchestrator, at the first work item framed after this ships |

## Not done

Nothing yet.

## Fed back into the spec

`spec.md` §*The fifth row* gained a paragraph recording that the name and its
values are the owner's, given at the approval, with the three grounds and what
the shorter values cost. `plan.md`'s Alternatives table gained the row that
`Automation` was chosen over `Attendance` and why the frame's reason for
rejecting it stopped holding once question 1's first option took the same word.
Both are marked as decided at the approval rather than inferred during
implementation — they are an answer to `questions.md` Q1, which named that
moment.
