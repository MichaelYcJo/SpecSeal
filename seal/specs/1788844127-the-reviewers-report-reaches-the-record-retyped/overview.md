# the reviewer's report reaches the record retyped — overview

📋 implement applied
· spec:     `docs/review-handoff-protocol.md` §Problem · §Layout · §Files · §Conformance · §The handoff before round 1 · `skills/agent-contract/SKILL.md` §1 §2 §3 §4 §5 §6 §9 §10 §15 · `skills/implement/SKILL.md` §1–§4 · `agents/warden.md` §Where you work · §Role · §Report · `skills/code-review/SKILL.md` §Cross-session records · §And commit the record before commissioning the fixes · §Paste-ready fixes · `CLAUDE.md` §The goal a design is chosen against · §Repo rule — a change writes fragments · `seal/follow-up.md` · this item's `routing.md`
· evidence: 4 rows in `seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md` (S1–S4), 14 coordinates, all re-verified — `14 ok · 0 drifted · 0 broken`, exit 0
· verified: **executed** — `tests/test_the_reviewers_report_reaches_the_record.py` 7 passed; the seven modules that read the generator and the round-record layout, 280 passed 1 skipped exit 0; the seven document modules, 118 passed; six of the seven new cases seen red against the pre-change tree; four mutations of the two added units, all killed. **read** — nothing this work rests on was taken from prose alone. **unverified** — the full suite, lint and typecheck, which are the orchestrator's, once, after the rounds settle

## Why this work exists

The chain's own artifact — the reviewer's report — never reached a file, so
the orchestrator retyped a document whose whole value is that it is exact;
now the reviewer writes it where `round_record.py new` reads it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which tree the reviewer writes its report in | The handoff said *"under the work item"* and named no checkout. `agents/warden.md` §Where you work says the reviewer works in a `git clone --no-local` *"and only there … you never write in it"* | The repository under review, with a named exception written beside the clone rule | The clone's lifetime is stated nowhere in this repository, so a returned path into it names a file the next segment may not be able to open — the ticket's own failure shape one step along. `plan.md` §Alternatives considered carries both readings and what each costs. `questions.md` Q1 puts it to the orchestrator |
| Where the permission is written | The handoff anticipated that *"the contract text needs a sentence to permit this"* | `skills/agent-contract/SKILL.md` is untouched; the exception is in `agents/warden.md` | §6 itself: *"An exception is one agent's, and it is named in that agent's definition — never here."* Writing it in the agent file is the mechanism the contract prescribes, not a departure from it |
| `plan.md`'s two phases | Planned as phase 1 (the generator) and phase 2 (the documents) | One phase | A default that reads a path nothing fills delivers nothing, and a file nothing reads delivers nothing either. Splitting them meant either a red case in a commit or an untested commit in the branch, which is what says the split was wrong. `plan.md` says so where the table is |
| The narrowed evidence-check command | The handoff gave `evidence_check.py --strict seal/ledger/<id>.md` | `evidence_check.py --strict --ledger seal/ledger/<id>.md` | Executed: `--strict` is `store_true` and the fragment path landed on the positional `root`, so the run read the fragment as a repository and answered `no evidence ledgers found — nothing to check`, exit 2 — a narrowing that silently narrowed to nothing. `--ledger` is the flag that narrows, and it says out loud which ledger it did not read |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck — not run, per `skills/agent-contract/SKILL.md` §2 | the orchestrator, once, after the rounds settle |
| The unscoped ledger read, `evidence_check.py --strict` with no `--ledger`. The narrowed run says out loud that `seal/ledger.md` was not read, and that is the read a branch's own rows must not silence | the orchestrator, at the pull request |
| Whether a real warden actually writes `rounds/round-<n>-report.md` when told to. The instruction is pinned by a case; an agent following it is not something a test can execute | the orchestrator, at round 1 of this branch — which is the first live trial of the change |
| Whether `docs/flow.md`'s `[ ] #228` box should be ticked by this branch or by the release that ships it. Every other 0.9.2 entry is unticked and every shipped one is ticked, so the tick looks like the release's act; the file was left alone rather than guessed at, and it is a shared file this branch has no fragment for | the orchestrator |

## Not done

**`--asked` was left with the same defect `--report` had.** It is a required
path to a file that exists as prose in a spawn prompt, and the orchestrator
types it out. It is out of scope on the ticket's own terms, and the loss is
smaller: the round paragraph is the orchestrator's own text, so retyping it
loses nothing another party wrote. `questions.md` Q2.

**`round-N-asked.md` and `round-N-fixes.md` were not documented.** Executed:
`grep -rn 'asked\.md\|fixes\.md' agents/ skills/ docs/ templates/
CONTRIBUTING.md` returns nothing — both live in two test comments and
`CHANGELOG.md` alone. The handoff called them an existing convention, and they
are one in the tree and not one on paper. Naming them is a documentation pass
over files this ticket does not otherwise touch. `questions.md` Q3.

**Nothing enforces that the report is committed with the record.** The
sentence is in `skills/code-review/SKILL.md` beside the rule that the record
is committed before the fixes are commissioned, and the two files sit in one
directory so `git status` shows them together. Making `round_record.py new`
refuse an uncommitted report was considered and rejected: `new` runs before
the record is committed by design, so it would refuse every correct run.

Round 1 🟡 3 asked for `close` instead, which runs after that commit, and the
fix pass weighed it and answered no. `--report` is what defeats it: the flag
exists so a report can live elsewhere, `new` records nowhere which path it
read, and a gate in `close` therefore refuses the runs the flag was added for
— executed, 36 of 41 cases in `tests/test_the_fixes_close_the_record.py` fail
with the proposed gate inserted. `plan.md` §*Technical context* carries the
measurement. **A gate that survives `--report` needs `new` to record the path
it read, which is a new record field, a template section and a checker.**
That is a mechanism nobody has decided to build, and whether to open an issue
for it is the orchestrator's call.

**The ticket's smaller version was not built.** It is recorded as the rejected
alternative in `plan.md`, with what it costs.

## Fed back into the spec

**A record is selected by name, never by directory membership** —
`docs/review-handoff-protocol.md` §Layout, marked here as inferred during
implementation. It is a protocol-level rule that nothing had stated, and the
diagram above it read as an inventory of a directory that has held three other
file shapes for several releases. Three readers took membership for
record-ness: two raised `TypeError` rather than failing an assertion, and the
third counted fifty-three non-records into a corpus of records and said
nothing at all — that third one was found by round 1 and fixed in its fix
pass, and it is the measurement behind the rule. A planner may overturn the placement — the report
itself is implementation, and one could argue the selection rule is too — but
the diagram cannot stay the only thing saying what `rounds/` holds.
