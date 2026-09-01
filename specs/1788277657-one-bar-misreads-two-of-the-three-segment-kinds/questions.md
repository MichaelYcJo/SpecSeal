# one bar misreads two of the three segment kinds — questions

<!-- specs/1788277657-one-bar-misreads-two-of-the-three-segment-kinds/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

## Q0 — answered before the first edit

**The batch found nothing open.** All three decisions were made by the
repository owner on 2026-09-01, in issue #51's discussion and the session
that launched the overnight run: the bars with observation 1's numbers
verbatim, the resume rule on its three measurements, and Q1 of
`specs/1788224363-a-subagent-rediscovers-what-the-session-established/questions.md`
answered as "keep 1.2". Routing was committed before the first edit
(`routing.md`, 9d974b8).

**Plan approval is delegated.** Approval of this work item's `plan.md` is
covered by the owner's overnight authorization, recorded here per the spawn
instruction; nobody is at the keyboard, so the plan proceeds on that
delegation rather than on a mid-run question.

## Assumptions recorded rather than asked

| # | Assumption | Grounds | Status |
|---|---|---|---|
| A1 | Placement of the two new rules is the smith's judgment: bars in `docs/review-handoff-protocol.md` beside the meter pointer, resume rule in `skills/code-review/SKILL.md`'s orchestrator sections — and neither is duplicated into the other's home | the spawn instruction delegates placement; a rule with two homes drifts apart on the next edit to either | ✅ delegated |
| A2 | The spawn prompt quoted `agents/smith.md`'s caveat as "1.27 tools per turn"; the file reads "1.08–1.17 tools per turn where review rounds read 1.29–1.89". The file's figures are used | the file was opened; a spawn prompt ranks below the ratified documents (`implement` §1) | ✅ file read |
| A3 | `agents/smith.md` and `agents/warden.md` are not edited: their existing sentences agree with the bars, and consistency is kept by quoting the same measured ranges | editing them buys no new information and drifts four minor ledger anchors in `.specseal/map.md` | ✅ recorded |
| A4 | The protocol's draft number moves 0.7 → 0.8 for the bars section, per the document's own Status convention | every prior rule addition moved the draft (0.5, 0.6, 0.7 each name theirs) | ✅ inherited |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
