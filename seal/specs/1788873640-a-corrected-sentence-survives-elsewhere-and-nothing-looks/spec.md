# Feature Specification: a corrected sentence survives elsewhere and nothing looks

<!-- seal/specs/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §12 — *a defect belongs to a class; do not fix the coordinate* | The rule is written, reaches every agent at startup, and has been re-broken seven times. This work stops adding sentences to it and builds the thing that observes it |
| `CLAUDE.md` §*The goal a design is chosen against* — verification that runs unattended | Decides where the check lives: at the act (a fix pass) and in CI, not in a reviewer's clone. #269's second clause is precisely a check that existed and ran nowhere |
| `docs/flow.md` §0.9.3, the `#180` row | **Supersedes the ticket's `Done when` list.** The deliverable is one check: *after a fix pass, grep the changed sentences' distinguishing terms across the rest of the corpus and report the survivors* |
| `skills/verify/SKILL.md` — a check that cannot fail is a counterfeit seal | The check exits non-zero on a survivor and names the file and the surviving sentence |
| `skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it* | Why the check belongs to the fix pass rather than to a review round: a round cannot see what its own fixes left behind |

## Scope

**In.** One check, shipped as a plugin script with a `bin/` wrapper, that takes
a commit range and reports every place in the tree that still carries wording
the range removed. Its refusal names the path, the surviving sentence and the
corrected sentence it matched. A content-anchored escape for the case where a
survivor is a deliberate carrier. Prose naming the check at the two places that
run it — the fix-pass procedure and the smith's verify phase. The `#180` row of
`docs/flow.md`.

**Out, and each has a home.**

| Out | Home |
|---|---|
| A `PreToolUse` hook refusing `git -C .` and `cd … && git commit` | #22 — *the gate guesses which repository a commit reaches; git already knows* |
| The handoff's ledger count taken from a scoped read | `docs/review-handoff-protocol.md` and the checker that today only warns — `questions.md` Q1, the repository owner |
| A fourth document restating §12 | Nothing. The ticket's own *Not this* section forbids it, and it is the failure mode this work exists to replace |
| Widening contract §12 with a method | #180's third rule, which this work does not take |

## User scenarios & acceptance *(mandatory)*

Every row is a measured event in this repository's own history, not a fixture.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| **S1 — a moved sentence leaves its pin behind** (#269) | Given `7bcf36a` on `chore/228-…`, which reworded `agents/warden.md` §6 from *writes the record from this report once the orchestrator has verified its findings* and did not touch `tests/test_the_rules_have_one_owner.py`, where `GENERATOR_NAMED[WARDEN]` still pinned the replaced sentence across two string literals. When the check runs over that commit's own range. Then it reports `tests/test_the_rules_have_one_owner.py` and prints the surviving sentence | Executed against the real commit. The module was red from that commit through two review rounds and two broad gates, and only `35ad9cd` fixed it |
| **S2 — a correction at the coordinate leaves the class standing** (#267) | Given `ad6f81a` on `fix/203-…`, round 2's fix pass, which corrected the docstring of `test_the_refusal_prints_every_piece_it_builds` and left the identical clause in `seal/ledger.md` row R3 and in the work item's fragment row S2. When the check runs over that fix pass's range. Then it reports both ledger carriers | Executed against the real commit. Round 3 found them by reading; `8b4b4b6` fixed them |
| **S3 — a record of a past state is not a survivor** | Given the same range as S2, where `rounds/round-2.md` and `rounds/round-2-report.md` quote the finding's wording verbatim. When the check runs. Then neither is reported | Executed on S2's range: the two round files carry the wording and are absent from the report |
| **S4 — the refusal names the coordinate, not a count** | When any survivor is found. Then stdout carries the path, the surviving text, and the corrected sentence it matched; the exit code is 1 | A case asserting each of the three, and the exit code |
| **S5 — a clean range is silent and exits 0** | Given a range that removed no wording still standing. When the check runs. Then it prints what it examined and exits 0 | Executed on this work item's own range |
| **S6 — a deliberate carrier is exempted by content, and the exemption rots loudly** | Given a survivor a person has judged legitimate, recorded as a row naming the path and a quoted distinctive substring. When the check runs, the survivor is not reported; when the surviving text is later edited so the substring is gone, it is reported again | Two cases — the row silences it, the edited text un-silences it |
| **S7 — the check runs where the act happens** | Given the fix-pass procedure and the smith's verify phase. Then each names the command | Cases reading both files |

## Data & interfaces

```
survivor-check --range A..B [--root R] [--exempt FILE]... [--json]
```

Exit **0** nothing survived · **1** survivors, each named · **2** unusable
input (a range that does not resolve, an exemption file that will not parse).

**No new schema.** The exemption file is a markdown table under the work item,
`seal/specs/<work-item-id>/survivors.md`, one row per judged survivor:

| Column | Holds |
|---|---|
| Path | the file carrying the surviving text |
| Quote | a distinctive substring of it — the content anchor |
| Grounds | why this carrier is legitimate |

It is per-work-item for the reason `CLAUDE.md` gives for every fragment: no two
work items share an id, so no two branches share a file. It is anchored on
content and not on a line, for the reason the ledger is: a line moves for edits
unrelated to the claim. It degrades toward **reported**, never toward silence.

## Open questions → questions.md

Two, both for the repository owner, neither blocking: the handoff's ledger
count (#180's second rule, whose home is the handoff protocol) and whether the
CI step fails the pull request or reports on it. The second is answered by the
noise measurement this work takes, and the answer is recorded rather than
asked.
