# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — review round 1

| Field | Value |
|---|---|
| Target SHA | 6b160c8 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 181 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes |
| Loses a record or crashes | yes — finding 1 writes a round record whose `## Inherited coordinates` and `## Deferred` are unreadable to every downstream reader, and finding 3 writes a record with all four sections unreadable |

- [ ] Pass

## What this round was asked

Round 1, the finding round, against `6b160c8` with base `774e76b`. Eight things
to attack, in order: the guard's placement and whether any entry point produces
a record without passing through it; the scope rule against phase 1's own
seven-member table, run member by member, with the instruction to find an eighth
or show the boolean decomposition closed; whether a section added to
`REPORT_TABLES` is guarded by being added there, and what the two constants do
not name that the generator nonetheless reads; the mention-versus-loss
distinction and where that judgment is wrong in either direction; whether
`fenced_after`'s removed raise is genuinely unreachable; the `strict=True` zip
and whether the two readings can differ in length; the two shared-ledger rows
this branch re-stamped; and whether F1 and F4 earn two rows or are one written
twice.

The round was told that the branch contradicts its own ticket in three places
and that every one of those is the round's to check. It was also told to run the
unscoped ledger read itself and confirm the count, because the orchestrator's
handoff to this branch's phase 2 had said one drift where there were two — the
third time in the release that gap cost something. And it was told, with
particular care on this item, that no fenced block in its own report may close
after a later heading, since that is the defect under review.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `fenced_after`'s never-closed raise was removed as unreachable; a fence opener inside an HTML comment reaches it, and `new` now writes a record whose `## Inherited coordinates` and `## Deferred` are unreadable | `skills/code-review/scripts/round_record.py#fenced_after` | open | executed in a clone at `6b160c8`: the record is written and both sections resolve to 0 occurrences through the shared reader; the same input at `774e76b` is refused and writes nothing |
| 🟡 2 | `swallowed` reads the headings and the terminal lines and not the table bodies, so a fence wholly inside `## Deferred` hides the table while the heading stands — the record reads `nothing to drain` beside a written row | `skills/code-review/scripts/round_record.py#swallowed` | open | executed at `6b160c8`; a verdict row inside a fence under `## Verdicts` is dropped the same way |
| 🟡 3 | the `--asked` text is spliced into the record above every section a reader looks up and never passes through `swallowed`; an unclosed fence there blanks the record from `## Verdicts` down | `skills/code-review/scripts/round_record.py#main` | open | executed at `6b160c8`: the record is written first, all four sections resolve to 0 occurrences, and the message blames a missing `## Verdicts` |
| ⬜ 4 | *"Its raise is now unreachable and was removed rather than left as dead code"* is false | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-1.md` | open | falsified by finding 1 |
| ⬜ 5 | F2's Notes name putting the raise back as the tidy-up to resist; it is the repair finding 1 needs | `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md` | open | read at `6b160c8` against finding 1's executed evidence |
| ⬜ 6 | *two* silent-loss members and the completeness claim are narrower than the class; finding 2 is a third silent shape | `seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/changelog.md` | open | executed — finding 2's measurement; the same sentence stands in `overview.md` and `phases/phase-1.md` |

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py .` at `6b160c8`, exit read directly | exit 1 · 677 ok · 2 drifted · 0 broken; both drifts are the two `overview.md` §Not verified names, confirming the handoff was one short |
| `new` on a report with a fence opener inside an HTML comment under the probes table, at `6b160c8` | the record is written; its `## Inherited coordinates` and `## Deferred` each resolve to 0 occurrences through the shared reader |
| the same report against `774e76b`'s `round_record.py` | refused — *a fenced block under `## Executed probes` is never closed* — and no record written |
| `new` on a report whose `## Deferred` heading stands with the whole table inside a fence | succeeds; the record's Deferred section reads `nothing to drain` |
| `new` on a report with a second verdict row inside a fence under `## Verdicts` | succeeds; the row absent from the record |
| `new` with an unclosed fence in the `--asked` round paragraph | the record is written, then the run fails; all four sections resolve to 0 occurrences |
| `new` on a fence crossing a prose heading | succeeds — the deliberate limit, as documented |
| a fourth heading pair added to `REPORT_TABLES` in a clone, nothing else edited | refused, naming the new heading — the derivation claim holds |
| the module's own suite against `774e76b`'s `round_record.py`, restricted to the fence cases | 6 failed, 5 passed — §15 satisfied; the green ones are the acceptance cases |
| the module's own suite at `6b160c8` | 49 passed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the full suite, the repository-wide lint and the typecheck | contract §2 — not run in this round | the orchestrator, once the rounds settle |
