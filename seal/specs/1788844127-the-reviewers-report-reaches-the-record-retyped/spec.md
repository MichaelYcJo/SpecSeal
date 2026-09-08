# Feature Specification: the reviewer's report reaches the record retyped

<!-- seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-handoff-protocol.md` §*Problem* — findings that live only where the next session cannot recover them | The report is exactly that: it exists in a transcript the orchestrator must not open, and in chat text |
| `docs/review-handoff-protocol.md` §*Conformance* rule 2, *Writes after posting* | The record is written immediately because that is the only moment the verdicts still exist anywhere. This work makes the report a file, so that moment stops being the only one |
| `skills/agent-contract/SKILL.md` §6 — *You return a report* | The reviewer writes no durable record. A report written to a file is still a report; the exception mechanism §6 names is *"one agent's, and it is named in that agent's definition"* |
| `agents/warden.md` §*Where you work* — the clone, *"and only there"* | The wall this change has to get past, and the reason the exception is written where it is |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a design that keeps the report exact by itself and one that asks the orchestrator to retype it faithfully, the first is the cheaper one |

## Scope

**In.** The reviewer writes its report to `rounds/round-<n>-report.md` under
the work item and returns that path. `round_record.py new` defaults
`--report` to that location when the flag is absent. The four documents that
state who writes what under the work item say the record and the report are
different artifacts with different owners.

**Out.** The record's own format. The `--asked` flag, which has the same
shape of defect and is not this ticket. Anything about how the orchestrator
verifies a report before writing the record — unchanged, and the reason the
reviewer still writes no record.

**Explicitly rejected.** The ticket's smaller version — the reviewer returns
a path and nothing establishes what is at it — is recorded in `plan.md` as
the rejected alternative.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The default fires | Given `<item>/rounds/round-3-report.md` exists · when `round_record.py new --item <item> --round 3 …` runs with no `--report` · then the record is written from that file | executed — `test_the_reviewers_report_reaches_the_record.py` |
| The flag still wins | Given a report at some other path · when `--report <that path>` is passed · then that file is read and the conventional one is not | executed — same module |
| The absence is named | Given neither the flag nor a file at the conventional path · when `new` runs · then it refuses, and the message names the path it looked at | executed — same module |
| A report is not a record | Given `rounds/` holds `round-3-report.md` beside `round-3.md` · when any reader of `rounds/` runs · then only `round-3.md` is a record | executed — `routing.round_number` returns `None` for the report name |
| The reviewer is told where to write | Given `agents/warden.md` · when a warden reads it · then it names the path, says it returns it, and says the write happens in the clone | read + pinned — a case asserts the sentences are there (§14) |

## Data & interfaces

`round_record.py new` gains one behaviour and no new flag:

```
--report PATH   the reviewer's report, a file
                (default: <item>/rounds/round-<n>-report.md)
```

The path is derived from `--item` and `--round`, which are already required
and are already what `<item>/rounds/round-<n>.md` is derived from. So the
report and the record are two names built from one pair of arguments, which
is what makes the convention checkable rather than remembered.

## Open questions → questions.md

Q1 — which checkout the reviewer's report is written in — is answered there,
with the orchestrator named. The implementation takes the answer that needs
no change to `agents/warden.md`'s clone rule.
