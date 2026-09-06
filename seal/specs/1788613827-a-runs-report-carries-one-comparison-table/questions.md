# Questions — 1788613827

<!-- Decisions only a person can make. The first three were asked as one
batch before the first edit; what follows them are assumptions written down
rather than asked, because a different answer would not change what is
built. -->

## Asked and answered, 2026-09-05, before the first edit

| # | Question | Answer | What it decided |
|---|---|---|---|
| 1 | Scope of this session — #170 alone, #170 then #156, or all four of 0.8.2 | **#170 alone** | this work item is one branch and one chain; #156, #155 and #169 become the first three readings taken under the table this builds |
| 2 | Routing, three axes in one question | **smith · through the review chain · open the pull request** | `routing.md`, committed at `f02cb11` |
| 3 | Is the table enforced by a check, or stated in the documents | **documents plus the `session_cost.py` token line** | `spec.md` §Scope's first *Out*. The table's sources are a pull request body and an issue comment, neither of which CI can read |

## Assumed, not asked

| # | Assumption | Why it does not wait |
|---|---|---|
| 4 | The token line covers the transcript it is given **and** its subagents, always, rather than behind a flag | #170's own words are *"so the row is one command"*. A flag makes it two, and the flagless call would keep printing the number the table must not use |
| 5 | The token line's `turns` counts assistant messages carrying `usage`, not messages carrying a tool call | the table's row is *Model turns*, and a turn that only thought is still a turn the run paid for. Changing `tools_per_turn` to match would move the bars in `docs/review-handoff-protocol.md`, which is out of scope |
| 6 | A comparison whose transcript covers only part of a branch says so beside the number, in prose, rather than in a column | #170 §*The rule* says exactly this. A column would make it a field, and the moratorium on parsed fields refuses new ones without a reader |
| 7 | The table's rows are stated in `skills/verify/SKILL.md` rather than in a template | a template is copied into a work item's directory; the table is written into a pull request body and an issue comment, neither of which the work item holds |
