# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — overview

More than half of `skills/code-review/SKILL.md` was addressed to the
orchestrator and a `warden` spawn read all of it before its first tool call;
the five sections the file prefixed `Orchestrator:` now live in
`skills/code-review/orchestration.md`, and three of `writing-style`'s four
per-document sections — the three a reviewer never writes — live in
`skills/writing-style/outside-the-review.md`. What a `warden` spawn reads
goes from 108,399 bytes to 78,109.

## Where spec and implementation diverged

| The document said | What was built | Which won, and why |
|---|---|---|
| #265: *No reference crosses it* — `agents/warden.md`, `agents/smith.md`, `agents/scribe.md`, `skills/agent-contract/SKILL.md` and `templates/*.md` contain no `Orchestrator:` section reference at all | Four live references cross the seam that the ticket's grep could not see, one of them in `agents/smith.md` | **The construction won.** The ticket greped the literal `Orchestrator:`, which matches the five `##` headings and none of the seven `###` subsections under them. Its sentence is true as written — `agents/smith.md` carries no `Orchestrator:`-prefixed reference — and wrong about the thing it was written to establish, because the reference it carries is to a subsection of one of the five |
| #265: *Eleven test modules pin the path `skills/code-review/SKILL.md` by name* | 21 modules name the file; eleven failed, and it is a different eleven | **The construction won.** Eleven name it as a path and that count is exact; ten more name it as the Python tuple `("skills", "code-review", "SKILL.md")`, which no path grep reaches. Six of the ticket's eleven needed no change, and five modules it never named broke. This session's own first check had the same hole and confirmed the ticket before a failing test in an unlisted module exposed it |
| #265: the five sections are *24,553 characters, 55% of the file* | 24,947 characters, 53.1% | **Both readings are right about their own commit.** The ticket measured `release/v0.9.2` at `a495e4f`; 0.9.2 shipped prose into the file afterwards, so the section grew and the file grew more. The records carry the figure measured at this branch's base, `d2f5712` |
| #265 §2: 「PR 본문에만」, 「다른 팀에 답할 때」, 「사용자와의 대화에만」 and 「리뷰 코멘트에만」 *are 3,688 characters that are not a reviewer's* | 3,688 is all four to the character; the three that moved are 3,134 | **The measurement won.** The ticket's sentence lists four and calls all four not a reviewer's, which cannot hold — one of them is precisely a reviewer's, and the owner's answer keeps it. The 554-character difference is the section `warden` needs, so part 2 recovers 3,134 |
| The task: *a skill of its own that the review skill names, or a reference file under the skill's directory, are both shapes this plugin already uses* | A reference file under the skill's directory | **Half of that sentence is true of this tree.** No skill here carries non-preload Markdown at all — the seven non-`SKILL.md` files under `skills/` are all scripts. `plan.md` records the full cost of the skill-of-its-own option: four pinned counts in two READMEs, and a runtime choice between firing on its own description mid-round or becoming a command nobody types |
| `CLAUDE.md`: *A row whose anchor a change removes is REMOVED, not re-pointed. Its claim went with the code* | The three rows were removed and re-stated in this work item's fragment | **The rule won, and its rationale does not describe this case.** The claim did not go with the code; the code moved file. Followed as written because the task instructed it explicitly and because `evidence-check` reports the anchor BROKEN, which means go edit the ledger. Recorded as Q1 rather than decided here |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Contract §2 makes these the orchestrator's, once, after the rounds. The base reading (`c0a65d5`, macOS, 2026-09-08, `2808 passed, 2 skipped in 439.63s`) reached this session as prose in the spawn prompt and is cited as **read**, never executed | the orchestrator |
| The `Ran by` value in the five phase records. The spawn prompt carried no model, so `claude-opus-5[1m]` is the id the harness stated at spawn rather than a value the orchestrator handed over. `templates/sdd-phase.md` makes the value the spawning session's | the orchestrator |
| Whether an orchestrating session actually opens `skills/code-review/orchestration.md`. Nothing can execute this: it is prose reached by a pointer, exactly as `round_record.py` and `chain_check.py` already are, and `plan.md` records it as the cost the chosen shape pays. The enforcement of the moved rules did not move — `chain_check.py` still refuses a record missing the fix-surface rows, and still refuses one committed after the fixes it commissions | the repository owner |
| Whether `smith` losing three `writing-style` sections from preload degrades a pull-request body in practice. `evals/pr-body-style/` exists and grades exactly this, and running it was not in scope | the repository owner |

## Fed back into the spec

| Clause | Where | Marked |
|---|---|---|
| The seam is contiguous — lines 236–653, one unbroken block, every heading in it prefixed and no heading outside it | `spec.md` §*The seam, measured at this branch's base*, and a row in the ledger fragment | *inferred during implementation* — nothing before this branch had measured contiguity, and it is what turns "the author drew the line" from an argument into a fact |
| A reference to a moved heading is not found by grepping the heading's own naming convention, and a reference to a file is not found by grepping the file's path when the language allows a tuple | `spec.md` §*What the enumeration by construction found that the ticket did not*, and two rows in the ledger fragment | *inferred during implementation*. This is `agent-contract` §12 arriving in the enumeration rather than in the fix, and it caught this session as well as the ticket |
| A check that reads a fixed list of paths loses coverage silently when material leaves a listed file | `phases/phase-3.md`, and a ledger row | *inferred during implementation* — `tests/test_docs_line_wrap.py` had no failure to report and had lost 418 lines of guarded prose |

## Not done

- **No style gate in `round_record.py new`**, and `writing-style` was not
  moved out of any agent's `skills:` list. Both are the owner's answers,
  recorded in `routing.md`. Whether a style rule can be checked mechanically
  stays open, and #180's conclusion is why an instruction was not written in
  its place.
- **The `Orchestrator:` prefix stays on the five headings.** Renaming would
  be a second change wearing this one's clothes, and every live reference,
  three ledger rows and two test constants name a heading by that text.
- **`skills/writing-style/SKILL.md`'s frontmatter was left alone.** A
  `description` is injected into every session's skill listing, so naming the
  new file there would be paid by every session — against this work item's
  own goal.
- **The construction that verified the reference enumeration was not made a
  permanent check.** It is mechanism the ticket did not ask for; Q2 in
  `questions.md` puts it to the owner with the script's location.
- **`evals/pr-body-style/` was not run.** See *Not verified*.
