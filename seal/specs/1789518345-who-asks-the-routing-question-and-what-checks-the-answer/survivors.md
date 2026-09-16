# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — survivors

<!-- Places `survivor-check` reported as still carrying wording this range
removed, and which are judged correct to leave standing. Each row quotes the
STANDING text, so the exemption stops holding as soon as that text changes.
Run: `bin/survivor-check --range cc05d31d..HEAD --exempt <this file>`. -->

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | `Spawn it where the SDD ladder already calls for a ``spec.md``, and it reads the repository widely, collects everything a person has to answer into one` | A released changelog entry is a record of what was true at that release, not an instruction anybody follows. Rewriting it would make the released section describe an agent that did not ship in it |
| `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/changelog.md` | `Spawn it where the SDD ladder already calls for a ``spec.md``, and it reads the repository widely, collects everything a person has to answer into one` | The same text, in the fragment the release gathered it from. Another work item's record, and the repository's fragment rule says a branch writes its own |
| `agents/framer.md` | `A question arriving at` | This is the sentence LANDING, not surviving. The act moved to the framer, so the framer's definition is where the reason for it belongs; `agents/smith.md`'s copy is what this range removed |
| `skills/implement/orchestration.md` | `Opening a pull request is an outward-facing act — it is not a detail that can wait for the end.` | The same shape: the routing question's home is this section, and the sentence stating why the destination cannot wait belongs where the question is asked. `agents/smith.md` carried it because it used to ask |
| `templates/claude-md-block.md` | `The commit gate reads that file, so a declared work item commits silently for either review answer, and CI reads the same file at the pull request.` | About the commit GATE, not about the routing question's shape, and what this range removed from `agents/smith.md` is the question. The block is the one file a session in an opted-in repository always has, so the gate's behaviour has to be in it |
| `CLAUDE.md` | `The commit gate reads that file, so a declared work item commits silently for either review answer, and CI reads the same file at the pull request.` | The generated copy of the row above. `.github/scripts/claude_block.py --write` writes it from the template and CI checks the two agree, so it is one place counted twice |
| `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-2.md` | `text unchanged except the arm sentence` | A phase record of an earlier work item, quoting the heading as it stood when that phase ran. A record asserts a past state, which is what lets it sit beside a contract at all |
| `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/spec.md` | `**``skills/implement/orchestration.md``** — headings: ``## Orchestrator: Bootstrap — create what's missing``` | The same work item's spec, enumerating the headings that file had when it was split. Rewriting it would make that contract describe a file it did not move |
| `tests/test_waiver_decided_at_start.py` | `Opening a pull request is an outward-facing act, and asked at the end it IS a mid-round prompt — the thing this release removes.` | The module's own reasoning for why the destination is asked in the first batch, which this work item does not change — it changes WHO asks and in what shape. The sentence is still what the module is for |
| `tests/test_review_axes.py` | `assert both in preset, f"the preset block lost `{both}`"` | **A false positive of the similarity matcher, reported only at the branch-wide range.** The phrases it shares with the rewritten `test_the_preset_block_carries_it_too` — *in preset f the preset*, *preset block lost* — are the two cases' common subject rather than copied wording. This case asserts the NEW shape and passes: its list holds `two questions in ONE `AskUserQuestion` call`. Nothing here is a leftover of a removed sentence |
| `tests/test_review_axes.py` | `A session that just commits never reads it and meets the gate at the commit instead` | **The same false positive, on the shared words *md in preset* and *read claude md*.** This is `test_the_preset_block_carries_the_routing_decision`'s docstring, about why the routing rule is in the block at all, and it is still true: the block is what a session that only commits ever reads. The case asserts `Routing, decided at the start` and the declaration path, both present |

## Round 1's fix pass — a range row rather than 28 path rows

<!-- The fix pass DELETED two shipped sections of `agents/framer.md`:
§*Yours is the one interactive phase*, and the separate-command paragraph
inside what was then §*The four writes*. Both went because the framer stopped
asking the routing batch and stopped writing `routing.md` — no agent this
plugin spawns has `AskUserQuestion`.

Every sentence of those sections stands, by design, in the copies that are
supposed to survive the deletion: `skills/implement/orchestration.md`,
`templates/claude-md-block.md` and its generated `CLAUDE.md`, and
`hooks/commit-review-gate.py`'s three prompts. The SESSION still writes
`routing.md` in a command of its own, and the gate still denies the whole
call — so the rule did not go anywhere, only the party did.

29 reports at HEAD, all correct as reports and none a defect. The count was
written as 28 because it was taken before the last commit of the pass; the
range row excuses all of them either way, which is why nothing turns on the
number and why it is corrected rather than re-taken each time.

**What the tool cannot bound, and round 2 found it by reading:** it matches the
sentences a range REMOVED, verbatim. Three lines in this branch's own tests
said the routing act was the framer's in words the removal never contained —
paraphrases the branch wrote about its own change — so they were never in the
removed set. `survivor-check` bounds what a removal left behind; it does not
bound what the branch itself wrote about the removal. The claim below is
therefore about the durable copies, which is what it was checked against. -->

| Range | Grounds |
|---|---|
| `6edfb71f..HEAD` | 22 survivors at HEAD, and the number moves with every commit of the range — 29 at round 2's target, 24 one commit later, 22 from `0b292ad0` on. **A count taken before the range's last commit is stale by construction**, which is how this row read 28 and then 29; the row is anchored on the range and the work item rather than on the number, so nothing turns on it. Measured at HEAD by re-running the check. The fix pass deleted `agents/framer.md`'s interactive phase and its separate-command paragraph, because a subagent cannot ask. Every sentence of both stands in the durable copies that are supposed to outlive the deletion — the orchestrator's routing section, the `CLAUDE.md` block and its template, and the commit gate's own prompts — because the SESSION still performs the act they describe. Opened directly rather than assumed: no hook and no shipped document still says the batch is the framer's |


## The merge with `release/v0.12.0` — a range row, and the "removal" is a resolution

`bin/survivor-check --range origin/release/v0.12.0...HEAD --exempt <this file>`

| Range | Grounds |
|---|---|
| `origin/release/v0.12.0...HEAD` | **Nothing was removed. Two ledger rows conflicted at the merge and each side was a different narrowing of the same claim, so choosing one makes the other read as deleted wording.** `seal/ledger.md`'s S6 and S9 were narrowed by this branch and by work item `1789455558` independently; this branch's text is a superset of both — S6 keeps *the count is six* and adds where a work item with no round record puts the cell, and S9 keeps the three refusals and says the count is that FUNCTION's rather than the module's. The claims survive; only the sibling's spelling of them does not. All seven places the check reports are records of other work items, or `tests/test_one_word_one_meaning.py:463`, discussing the same subject in their own words — none is a leftover of a sentence this branch deleted. Verified by reading each of the seven against the surviving row |
