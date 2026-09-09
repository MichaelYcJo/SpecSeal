# Implementation Plan: three sentences are wrong about where a duration is

## Summary

Two printed sentences and one arithmetic rule, in one file. The sentences come
paste-ready and verified from #145's round-3 report; the rule is Q5's second
answer, which the measurement below shows costs nothing already published.

## Technical context

`analyse` (`skills/verify/scripts/session_cost.py#analyse`) takes a window's
span as `calls[-1]["end"] - calls[0]["start"]` over calls ordered by start, so
it reads the end of the last call **to begin**. `in_windows` assigns a call to
a window by its start, which is what makes the calls partition and what leaves
a long-lived call's seconds covered by two rows. `report_spawns`
(`#report_spawns`) prints the between-the-rows line, and its refusal branch is
what items 1 and 2 are about.

**Order matters, and item 3 goes first.** Taking the span to `max(end)` makes
a window's own span cover every call assigned to it, so the refusal in items 1
and 2 fires strictly less often afterwards — it cannot fire on a row's own
call at all, only on two rows covering the same seconds. Fixing the sentences
first would mean writing them against a rule that is about to change, and the
report's paste-ready text was written against today's rule. So: change the
rule, re-read the two sentences against it, then take the report's text where
it still holds and say where it does not.

**What the rule change does not touch.** `command_s` sums the calls and is
unchanged. `model_s` walks the gaps and is unchanged. The partition of calls
is unchanged, and its case must stay green — two ledger rows are anchored on
that property.

**Failure scenario, in six months.** A reader compares a span printed after
this change with one printed before it and the two came from different rules.
The measurement says no transcript on this machine moves, so the comparison
is safe for everything already published — but the guarantee is *measured*,
not *structural*, and a transcript with a genuinely long-lived call would
move. The disclosure sentence in `skills/verify/SKILL.md` is what makes that
readable rather than surprising, which is why it is in scope rather than
optional.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Span to `max(end)` everywhere** (Q5's answer 2) | A published span with an outliving call moves. Measured: 15 transcripts, 0 move, `command` shares identical to one decimal | **Chosen — the owner's answer.** One line, and it closes the plain report's `command 101%` in the path every published reading uses |
| Leave the span and add a sentence (Q5's answer 1) | `command 101%` stays in that path, guarded by prose. Covering a wrong number with a sentence is the class this work item is closing | Rejected |
| `max(end)` for the run and the old rule for a row (Q5's answer 3) | Two numbers on one page come from two rules, and the one rule is what makes the printed partition checkable — which #145 spent three rounds establishing | Rejected |
| Assign a call to a window by its END instead | The calls stop partitioning, which two ledger rows assert and a case pins | Rejected, and it is `spec.md`'s out-of-scope row |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | Item 3 — a window's span is `max(end)` over its calls, so it can no longer be shorter than a single call inside it | a case on calls 0–1000s · 10–12s · 990–995s asserting the span covers its longest call; the partition case still green; the sweep re-run — 16 transcripts here and 169 machine-wide, no printed figure moving | `82c1dbb` |
| 2 | Items 1 and 2 — the refusal names the cut its row ends at and prints both sums, re-read against phase 1's rule and taken from the report where it still holds. Item 1's clause in `skills/verify/SKILL.md` moved here rather than to phase 3, so no phase boundary leaves a false sentence in the tree | the report's own case, seen red first; the `outside == 0` boundary case planted — the spec cited an existing one and there was none — and seen red under `> 0` | `be5bc18` |
| 3 | The span's own disclosure in `skills/verify/SKILL.md`, the two fragments, and the six ledger rows the edits to `#analyse` and `#report_spawns` drift | the modules the skill change touches; `evidence-check`; `survivor-check` over the whole fix range | |

## Operational impact

One published number changes definition, and the change is measured to move
nothing on this machine. No new flag, no new file, no migration. `command_s`,
`model_s` and the call partition are untouched.
