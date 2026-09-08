# 1788844127-the-reviewers-report-reaches-the-record-retyped — review round 2

| Field | Value |
|---|---|
| Target SHA | ab62e6dd67832c6d3a902cd0862255e883687548 |
| Ran by | warden on claude-opus-5 |
| PR | 258 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

A verifying round, spawned after round 1's fixes were committed and targeted at
the diff of those fixes: `76e2f75..dd152e8`. Its job was stated as the answers
rather than new findings, with one surface exempt — what the fixes themselves
created.

Six checks, in the order the prompt set them.

1. **🟡 1, and whether the class is closed rather than the coordinate.** The
   fix pass measured the corpus wider than round 1 had: 204 paths, 151
   records, 53 non-records, of which only 20 parsed as a verdict table and
   were counted while 33 fell out silently. The round was told to enumerate
   every reader of `rounds/` itself, by construction, and that a third wrong
   count would be the finding of this round — round 1's own count of two
   readers was wrong and was stated in three places plus a test docstring.
2. **🟡 2, judged as instructions the round was about to follow.** The fix
   adds a block to `agents/warden.md` §Report telling a reviewer its report is
   now scanned by the tree's own readers, with the way through for each. This
   round was the first reviewer to work under it, and two sibling branches of
   this release were refused for exactly that class while it ran.
3. **🟡 3, answered rather than fixed on a measurement** — the reviewer's own
   paste-ready gate failing 36 of 41 cases. The round was asked to verify the
   measurement and to judge whether the reasoning holds, or whether a narrower
   gate exists that the fix pass did not weigh.
4. **The four new units**, checked for the shape a sibling branch found: a
   case whose input never reaches the thing it claims to pin.
5. **⬜ 6's second instance**, found by enumerating the cause rather than the
   coordinate — whether the class is two instances and not three, and whether
   the refusal still carries both the path and the convention.
6. **The depth-2 sentence**, which is about this round: that depth 2 is
   unreachable in round 1 and only in round 1, so from round 2 onward a case
   pinning something inside a unit round 1's fixes created is refused.

Carried as not the round's to close: four ledger rows in this work item's
fragment and six more unscoped, all left for the closing commit.

Facts carried as executed by the orchestrator: the module at 7 passed exit 0
and ruff clean at round 1's target; the corpus breakdown reproduced; and
`round_record.py new` finding the conventional report path with `--report`
absent on this work item while the three sibling branches still require the
flag — the change working in its own review.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a third reader of the round-record directory selects records by directory membership | `tests/test_a_finding_id_is_a_bare_integer.py:302` | answered | closed at `1e35d5d`. Executed — the corpus reproduces at 204/151/53 at `a50431b`, and removing the filter turns the new case red at 54 of 206 while every other case in the module stays green. The class is nine readers, enumerated by construction and all opened; there is no fourth |
| 🟡 2 | nothing warns the reviewer that its report is now scanned by the identifier rule and the evidence checker | `agents/warden.md:272` | answered | closed at `b76ce68`. Executed — both escapes the block names are the exact strings the two checkers carry. The block's own worked example is wrong, which is finding 7 below rather than a reopening of this one |
| 🟡 3 | nothing carries the report into the commit, and `close` was never weighed as the gate | `skills/code-review/SKILL.md:182` | answered | the gate as written is defeated by the flag. Executed — 36 failed, 5 passed of 41 with round 1's gate inserted at `b76ce68`, reproducing the fixer's measurement exactly. The residual stands; what the record says it would cost does not, which is finding 8 |
| ⬜ 4 | the acceptance row described the write as happening in the clone | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:42` | answered | corrected at `dd152e8`; the row now matches `agents/warden.md`, which says the repository under review |
| ⬜ 5 | the spec said the clone rule needed no change | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:60` | answered | corrected at `dd152e8`; the section now names the exception as the cost the chosen design pays |
| ⬜ 6 | a directory at the conventional path is refused as nothing being there | `skills/code-review/scripts/round_record.py:739` | answered | closed at `dd152e8`, both members. Executed — reverting either lead turns its own case red, and each refusal keeps the path and the convention. Enumerated: the class is two, and the two other sites that ask the same question are not members |
| 🟡 7 | the reviewer warning's one worked example sends the exemption marker into a fenced paste-ready fix, which the checker never reads and which a smith pastes | `agents/warden.md:286` | open | executed — a proposed name in prose is refused at `NOT-IN-TREE`, exit 2; the same name backticked inside a fence is not read at all, 0 refused. `claim_lines` reads a fence as a quotation and its docstring names the pasted-fix corruption as the reason |
| ⬜ 8 | the recorded ground for deferring the report gate says any surviving gate needs a new record field, a template section and a checker; a gate conditioned on the conventional path needs none of them | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md:69` | open | executed at `b76ce68` — round 1's unconditional gate fails 36 of 41, and the same gate wrapped in a file test at the conventional path passes 41 of 41, exit 0. The narrower gate buys less, which is the honest ground for deferring; the cost sentence is what overstates. `overview.md:61` carries the same sentence |

## Paste-ready fixes

```markdown
The evidence checker reads every `.md` under a live work item and asks the
tree for each backticked name carrying an underscore that it finds in prose.
A name your report writes that the tree does not carry comes back
`NOT-IN-TREE`, and writing `NAME NOT IN TREE` on that prose line exempts the
line.

**A fenced block is already exempt, and marking one up corrupts it.** The
checker reads a fence as a quotation, which is why a paste-ready fix may
propose a unit that does not exist yet and say nothing — so the marker never
goes inside a fence, where the smith would paste it. Where you also name that
proposed unit in prose, the marker goes on the prose line and nowhere else.

The identifier rule has a second half as well: a real-looking domain outside
its allowlist fails the same module, so quote a URL only from a host that
allowlist already carries.
```
```markdown
A gate that reaches every run has to make `new` record the path it read, which
is a new field in the record, a template section and a checker that reads it —
mechanism, and a fix pass adds none. A narrower gate needs none of that:
guarded on the conventional path actually holding a file, the same refusal
passes all 41 cases at `b76ce68`, because a run that passed the flag leaves
that path empty. It buys less — it cannot see a report written elsewhere and
never committed — and that, rather than the cost, is why it is deferred rather
than built here.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three changed modules, in a clone at `ab62e6d` | 81 passed, exit 0 |
| `git ls-tree` over the round-record pathspec at `a50431b`, `76e2f75` and `ab62e6d`, split by suffix | 204 / 151 records / 53 non-records (20 report, 20 asked, 13 fixes) at `a50431b`; 206 / 152 / 54 at both later commits |
| the id-corpus filter removed, `bin/test` over its own module and the report module | 2 failed of 39 — `test_the_corpus_is_records_only` naming 54 of 206, and the warden case; every other case in the id module green |
| the new block deleted from `agents/warden.md`, same run | `test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file` red, naming the missing needle |
| both directory leads reverted, `bin/test` over the report module and the close module | 2 failed of 51, each case naming its own refusal string |
| round 1's paste-ready `close` gate inserted after the target check at `b76ce68`, `bin/test` over the close module | **36 failed, 5 passed**, exit 1 — the fixer's measurement reproduced |
| the same gate wrapped in a file test at the conventional report path, same commit, same module | **41 passed**, exit 0 |
| a probe record naming a proposed unit in prose, then the same name backticked inside a fence, through `evidence_check.py --strict --ledger` | prose refused at `NOT-IN-TREE`, exit 2; fenced name not read, 0 refused |
| `evidence_check.py --strict --ledger` at `ab62e6d` with the probe removed | 10 ok · 4 drifted · 0 broken · 0 external · 0 old-format; records arm 0 refused. The drift is the orchestrator's, taken at the closing commit |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_finding_id_is_a_bare_integer.py:275` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md` §Report | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/SKILL.md` §And commit the record before commissioning the fixes | round 1's 🟡 3 — answered |
| round-1 | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:739` | round 1's ⬜ 6 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a gate in `close` that survives the flag, in either form — the narrow one measured here or the recorded path it would need | `overview.md` §*Not done*, unchanged by this round | the orchestrator |
| the four drifted ledger rows in this work item's fragment, and six unscoped | `seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md` | the orchestrator, at the closing commit |
| `--asked` carrying the same defect `--report` had, and the two sibling files named in no shipped document | `questions.md` Q2 and Q3, opened by round 1 | the orchestrator |
