# 1788844127-the-reviewers-report-reaches-the-record-retyped — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 7bcf36a |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and this template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Implement issue #228's **primary** repair, both halves, with the direction
already settled: the warden writes its report to
`seal/specs/<work-item-id>/rounds/round-<n>-report.md` and returns that path,
and `round_record.py new` defaults `--report` to that location when the flag
is absent. The ticket's smaller version — a path-only return with no file
convention — was handed over as the rejected alternative, to be recorded in
`plan.md` and not built.

The phase was pointed at ten coordinates, one of them named as *"the
constraint that most nearly forbids this change"*: `agents/warden.md:156-163`,
§6's instance saying the reviewer writes no round record. It was asked to
make the record-against-report distinction explicit in the documents it
touched, to decide and state whether `round-N-report.md` is a protocol-level
addition or an implementation detail, and to check what walks `rounds/` for a
silent regression now that a second non-record file lives there.

## What this phase found

**The constraint that actually forbids this is one section higher than the
one the handoff named.** `agents/warden.md` §*Where you work* says the
reviewer works in a `git clone --no-local` *"and only there … you never write
in it"*. §6's instance is about **records**, and the record/report
distinction answers it cleanly. The clone rule is about **the tree**, and no
distinction gets past it — it needed an exception. That exception is written
where the rule is, which is the mechanism the contract's §6 already
prescribes: *"An exception is one agent's, and it is named in that agent's
definition — never here."* `skills/agent-contract/SKILL.md` is unchanged.

**Which checkout the report is written in was the real design question, and
the clone's lifetime settled it.** Writing in the clone keeps the rule
untouched and costs two things: the generator's default never fires, so the
orchestrator passes a path by hand; and nothing in this repository says when
the clone is cleaned, so the returned path names a file whose lifetime nobody
wrote down. That is the ticket's own failure shape one step further along.
`plan.md` §*Alternatives considered* carries both readings.

**The `rounds/` walkers are already safe, and it is worth knowing why.**
Every reader selects through `hooks/routing.py#round_number`, whose
`ROUND_RE` is `round-(\d+)\.md` under `fullmatch` — executed:
`round_number("round-1-report.md")` is `None`. That filter exists because two
readers once did not have it and each raised `TypeError` on sorting two
`None`s rather than failing an assertion
(`tests/test_the_reopening_is_one.py:428`,
`tests/test_chain_check_at_the_pull_request.py:1294`). So the layout already
anticipated this file; what it lacked was anything saying so outside two test
comments.

**`round-N-asked.md` and `round-N-fixes.md` are named in no shipped
document.** Executed: `grep -rn 'asked\.md\|fixes\.md' agents/ skills/ docs/
templates/ CONTRIBUTING.md` returns nothing. They live in test comments and
`CHANGELOG.md` alone. The handoff cited them as *"an existing convention"*,
and they are one in the tree and not one on paper. `questions.md` Q3.

**The protocol document takes one sentence, not a new file.**
`round-N-report.md` is implementation — the protocol's conformance rules
constrain the record, and a conforming tool whose reviewer writes
`round-N.md` directly needs no report at all. What is protocol-level is that
`rounds/` holds files beside the records, so a record is selected **by name**
and never by directory membership. The diagram read as an inventory and was
already wrong about three files.

**The two phases in `plan.md` were one vertical slice.** A default that reads
a path nothing fills delivers nothing, and a file nothing reads delivers
nothing either. Splitting them would have put either a red case or an
untested commit in the branch, which is the signal that the split was wrong.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `--report`'s `required=True` on the `new` subparser | Nowhere — the flag stays and still wins over the default. `tests/test_the_reviewers_report_reaches_the_record.py::test_the_flag_still_wins_over_the_conventional_path` is what keeps the removal from becoming a removal of the flag |
| `agents/warden.md`'s *"The parity mark below is §6's one exception"* | Rewritten in place as **two** exceptions, in the same sentence. Nothing left the repository |
| `skills/code-review/SKILL.md`'s reading that the reviewer writes nothing at the work item | The paragraph directly beneath it, which states what the reviewer does write and why it is not a record. The clause the sentence actually protects — no reviewer writes `round-N.md` or the two todo files — is unchanged and still there |
