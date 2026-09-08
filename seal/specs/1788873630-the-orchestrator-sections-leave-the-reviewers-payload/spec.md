# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — spec

Issue #265, release 0.9.3. Two halves of one claim: what a `warden` spawn
reads before its first tool call is more than half addressed to somebody
else.

## What this claims, and what it does not

**The claim is occupancy, not speed.** The characters sit in the agent's
context window on every spawn whether prompt caching served them from cache
or not, and a round that is killed and re-run pays the full write again —
which is how #255's measurement was taken. Nothing here is argued from a
wall-clock reading or a per-spawn token price: the meter is wrong until #200
and #202 land in 0.9.4, and every figure below is `wc`.

## Scope

### In

| # | What | Where |
|---|---|---|
| 1 | The five sections `skills/code-review/SKILL.md` prefixes `Orchestrator:` leave the file a `warden` spawn preloads, and land where the orchestrator still reaches them | `skills/code-review/` |
| 2 | Three of the four per-document sections of `skills/writing-style/SKILL.md` — the three that are not a reviewer's — leave the reviewer's payload; 「리뷰 코멘트에만 해당하는 것」 stays | `skills/writing-style/` |
| 3 | Every live reference to a moved heading names the file the heading is now in | `agents/`, `docs/`, `skills/`, `tests/` |
| 4 | Ledger rows whose anchor this change removes are removed in `seal/ledger.md`, and the surviving claims are re-written into this work item's fragment | `seal/` |

### Out

- **No style gate in `round_record.py new`.** The owner took the narrow half
  of #265's part 2 for exactly this reason: whether a style rule can be
  checked mechanically is an open question, and #180's conclusion is that an
  instruction standing in a check's place is the next instance of a class
  that has failed seven times. Nothing here answers that question, and
  nothing here pretends to.
- **`writing-style` stays in every agent's `skills:` list.** Both `warden`
  and `smith` keep it.
- The host repository's `CLAUDE.md`, which the harness injects whole and no
  plugin file can trim (#265 §3).
- The `Orchestrator:` prefix on the five headings. It is what drew the seam,
  every live reference names a heading by that text, and three ledger rows
  anchor on it. Renaming would be a second change wearing this one's clothes.

## The seam, measured at this branch's base

Measured on `perf/265-…` at `d2f5712`, by construction: the file parsed into
`##` sections fence-aware, each section's characters counted from its heading
to the next `##`.

| section | characters |
|---|---|
| `Orchestrator: the run ends with a verifying round` | 19,388 |
| `Findings format` | 7,417 |
| `Cross-session records — seal/specs/<work-item-id>/` | 6,621 |
| `Comparison axes` | 4,851 |
| `Orchestrator: a fix pass resumes the implementer` | 2,581 |
| `Orchestrator: the pull request opens before round 1, and a phase is re-run` | 1,999 |
| `Two stages, in order` | 1,324 |
| `The language the round records are written in` | 952 |
| `Orchestrator: verify before posting` | 557 |
| `Orchestrator: closing the cycle` | 423 |
| (heading) | 301 |

**The five are 24,948 characters of 46,986 — 53.1%.** The ticket's 24,553 and
55% were taken on `release/v0.9.2` at `a495e4f`; 0.9.2 shipped prose into the
file after that reading, so the section grew and the file grew more.

**The five sections are contiguous — lines 236–653, one block**, from
`## Orchestrator: a fix pass resumes the implementer` to the blank line
before `## Findings format`. That is the strongest available evidence that
the seam is real rather than argued: the author wrote the orchestrator's half
as one run of text and prefixed every heading in it.

## What the enumeration by construction found that the ticket did not

The ticket's grep was for the literal string `Orchestrator:`, so it saw only
the five `##` headings and none of the seven `###` subsections inside them.
Every heading inside the five was searched across every tracked file, with
whitespace collapsed so a wrapped reference still matches.

| Heading that moves | Live references outside the skill |
|---|---|
| `## Orchestrator: a fix pass resumes the implementer` | `seal/ledger.md` (2 rows) |
| `## Orchestrator: the run ends with a verifying round` | `seal/ledger.md` (1 row) |
| `### The cap is a ceiling, and this is the floor it never had` | none |
| `### A fix pass adds the unit that pins it, and that unit ships unreviewed` | **`agents/smith.md`**, **`skills/implement/SKILL.md`** |
| `### Then say who checked them, in the record` | `tests/test_the_rules_have_one_owner.py` |
| `### And name the fix surface, in the same record` | `tests/test_the_rules_have_one_owner.py` |
| `### And say what ran the round` | `tests/test_the_rules_have_one_owner.py` |
| `### And commit the record before commissioning the fixes` | **`tests/test_a_record_precedes_the_fixes_it_commissions.py`**, `tests/test_the_rules_have_one_owner.py` |
| `### The check a round runs reads everything, and only a write is narrowed` | none |
| `## Orchestrator: the pull request opens before round 1, and a phase is re-run` | `docs/flow.md`, **`docs/review-handoff-protocol.md`** |
| `## Orchestrator: verify before posting` | none |
| `## Orchestrator: closing the cycle` | none |

Four of those are references the ticket's *no reference crosses it* did not
account for, and the ticket's narrower sentence — *`agents/warden.md`,
`agents/smith.md`, `agents/scribe.md`, `skills/agent-contract/SKILL.md` and
`templates/*.md` contain no `Orchestrator:` section reference at all* — is
literally true and substantively wrong: `agents/smith.md` names a
subsection of one of the five, and that reference crosses the seam.

**The eleven test modules are exactly eleven.** Eleven modules name
`skills/code-review/SKILL.md`; three more name a path under
`skills/code-review/scripts/` and are untouched by a move of prose. A
twelfth module is affected all the same —
`tests/test_a_record_precedes_the_fixes_it_commissions.py` names a moving
`###` heading without naming the file it is in.

## Part 2, measured

| section | characters | bytes |
|---|---|---|
| 「리뷰 코멘트에만 해당하는 것」 — stays | 554 | 1,192 |
| 「PR 본문에만 해당하는 것」 | 1,169 | 2,417 |
| 「다른 팀에 답할 때」 | 1,084 | 2,408 |
| 「사용자와의 대화에만 해당하는 것」 | 881 | 1,949 |
| the three that move | **3,134** | **6,774** |
| all four | 3,688 | 7,966 |

**3,688 is all four sections, to the character.** The ticket's §2 lists four
by name and calls all four *not a reviewer's*, which is self-contradictory —
one of them is precisely a reviewer's — and the owner's answer keeps that one.
So part 2 recovers 3,134 characters and not 3,688, and the difference is the
554 characters the reviewer needs.

The three are also contiguous, lines 240–333, between the section that stays
and 「English prose rules」.

## Acceptance

| # | Criterion | How it is judged |
|---|---|---|
| A1 | No file in `agents/warden.md`'s `skills:` list, nor that file, contains any of the twelve moved headings | grep over the four preloaded paths |
| A2 | The orchestrator's five sections survive verbatim — same headings, same prose | `git diff` shows the block moved and not rewritten |
| A3 | `skills/code-review/SKILL.md` names the file the five sections are in, so a session that loaded the skill reaches them without being told a path | the pointer paragraph exists and names the path |
| A4 | Every live reference in the table above names the file its heading is now in | the same construction re-run: no live reference names a heading in a file that does not hold it |
| A5 | The eleven modules plus the twelfth pass | `bin/test` on the twelve |
| A6 | A sentence `test_a_fix_pass_may_add_a_unit.py` pinned as appearing once in one file still appears once across both halves | the case counts across both |
| A7 | `evidence_check.py --strict .` is clean, with removed anchors removed rather than re-pointed | executed |
| A8 | 「리뷰 코멘트에만 해당하는 것」 is still in `skills/writing-style/SKILL.md` | grep |

## Grounding

- `docs/flow.md` §0.9.3 — the release this sits in, and why before 0.10.0.
- `CLAUDE.md` §*a change writes fragments, never the shared file* — the
  changelog and ledger destinations, and the removal exception this change
  meets.
- `agent-contract` §12 — the class, not the coordinate: the reference
  enumeration above is the class, and it was taken by construction because
  the ticket's was taken by grep.
- #180 — why part 2 is the narrow half and no gate is built.
