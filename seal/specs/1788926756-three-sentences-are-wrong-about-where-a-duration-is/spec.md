# Feature Specification: three sentences are wrong about where a duration is

`analyse` assigns a call to a window by the moment it **starts**. That is what
makes the calls partition — every call in exactly one row — and it is why the
rows' spans do not partition the time. #145's round 3 measured three
consequences and this work item closes all three: two are printed sentences
inside the mode 0.9.5 itself ships, and the third is the span rule those
sentences are about, which is Q5 of that work item and is now answered.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #145 `questions.md` §Q5 | **Answered by the owner on 2026-09-09: take the span to `max(end)` over the calls** — the second of its three costed answers. This work item is where that answer lands |
| #145 `rounds/round-3-report.md` §*Paste-ready fixes* | Carries the whole change for items 1 and 2, verified, with a case seen red. This is transcription, not design |
| #145 `rounds/round-3.md` findings 1, 2, 5 | The three defects, each with the probe that produced it |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* | Why these could not be fixed on #145's own branch: findings 1 and 2 are inside the unit that branch's round-2 fixes created, which is depth 2 |
| `CLAUDE.md` §*a ledger coordinate names content* | Four ledger rows anchor at `session_cost.py#report_spawns` and two at `#analyse`, so a `# RIDER:` inside either drifts them. It is why this is a work item rather than a comment |
| #200's repair | The precedent for a number whose meaning moves: the report names what it could not classify rather than printing a row that reads as nothing having happened |

## Scope

**In.**

- **Item 1** — the refusal names *the cut its row ends at* rather than *a
  spawn's result*. The head row's cut is the first spawn's **start**, so a
  head call can outlive its own row's cut and end before any spawn's result:
  executed, and the line printed the result as the cause with no such call in
  the transcript.
- **Item 2** — the refusal prints the **two sums** rather than their
  difference. `minutes` carries one decimal, so a sub-three-second overlap
  printed `by 0.0m` as the grounds for withholding a figure.
- **Item 3, and it is Q5's answer** — a window's `span_s` is taken to
  `max(end)` over its calls rather than to the end of the last call **to
  begin**, so a window can no longer be shorter than a single call inside it.
  **It does not close the plain report's `command 16.8m 101%`, and phase 1
  measured that.** On that shape the span moves 995 → 1000 and the share
  stays 101%, because `command_s` sums three calls that overlap: 1007s of
  command time inside 1000s of wall clock. The span understatement was the
  smaller of two causes and #145's finding 5 named only it. The other is
  `questions.md` Q3, with the owner.
- The disclosure in `skills/verify/SKILL.md` beside the span's own definition,
  because after item 3 the span means something a reader can state.

**Out.**

- **Changing how a call is assigned to a window.** Assignment by start is what
  makes the calls partition, two ledger rows are anchored on that property,
  and #145 spent three rounds establishing that the rows partition the calls
  and not the time. Q5's third answer — a different rule for the run than for
  a row — was refused for the same reason.
- **Re-marking the readings already published.** Measured below: none moves.
- #304, the `survivors.md` ownership pattern one directory deeper. Different
  script, its own issue.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The refusal names a cut, not a result | Given head call 0–8s, spawn 5–9s, calls 6–9s and 9–10s / when `--spawns` runs / then the refusal names *the cut its row ends at* and the phrase *a spawn's result* is absent | the case `test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result`, which the report carries and which is red on the module as it stands |
| Nothing rounds to `by 0.0m` | Given the overlap the case above builds — three seconds / when the refusal prints / then it prints both sums and no magnitude that rounds away | the same case: `sum to 0.2m against the run's own 0.2m`. **Corrected in round 1's fix pass** — this row read *a one-second overlap*, which is #145's round-3 fixture (head 0–9s, spawn 5–7s, call 10–12s) and not the one this case builds. That fixture is the shape whose difference printed `by 0.0m`; this one printed `by 0.1m`, and what it pins is the cut rather than the magnitude |
| The exact-cover boundary still reads as the partition agreeing | Given `outside == 0` / when the line prints / then it reads *is BETWEEN the rows — mostly the wait* | the existing boundary case, still green |
| A span ends at the last call to END | Given calls 0–1000s, 10–12s, 990–995s / when the plain report runs / then `span_s` is 1000, which is no shorter than the longest single call in the window | a case asserting the span against `slowest`'s head. **Corrected in phase 1** — this row asked for `command` at or under 100% as well, and that is not something a span rule can deliver: see `overview.md` and `questions.md` Q3 |
| The rows still partition the calls | Given any transcript with a spawn / when `--spawns` runs / then every call lands in exactly one row | the existing partition case, still green |
| No published reading moves | Given the transcripts on this machine / when both span rules are computed / then they agree | executed, below — 15 transcripts, 0 move |
| A reader meets the span's meaning where the span is defined | Given `skills/verify/SKILL.md` / when a session reads the span's definition / then it says what the span ends at and what that costs | the sentence is in the file |

## Data & interfaces

No schema, no new flag. Two printed sentences and one arithmetic rule.

| Fact | Coordinate | Label |
|---|---|---|
| `spawn_cuts` opens its cut list at the first spawn's **start**, which is why the head row's cut is not a result | `session_cost.py#spawn_cuts` | read, and executed through the probe in #145's round-3 report |
| `analyse` **took** a span as `calls[-1]["end"] - calls[0]["start"]` with `calls` ordered by start — the state this work item was written against, and item 3 is what removed it. It now takes `max(end)` over the calls | `session_cost.py#analyse` | read, **before the change**. The two rows below were rewritten to post-change values, so this table mixes both states and each row now says which it is |
| **No PRINTED figure in THIS PROJECT's transcripts moves under `max(end)`, and five move elsewhere on the machine — 2 row spans and 3 between-the-rows figures** — this project's directory: 16 transcripts, 12 to 836 calls, 0 spans and 0 rows move. Every project: 169 transcripts, one run span moves by 0.006s and prints 10.3m either way; 2 row spans move a printed figure (368.5m → 368.7m, 195.7m → 195.8m); the between-the-rows figure moves on 3 transcripts (6.7m → 6.6m, 24.4m → 24.2m, 3.3m → 3.2m). `idle`, `model` share and the whole-run `command` share move nowhere, and the figure/refusal branch never flips | `~/.claude/projects/*/*.jsonl` | **executed 2026-09-09** — the safety of the published readings is the per-project result, not a machine-wide absence |
| **A share over 100% is already on this machine and is not the span's fault** — 169 transcripts, one printing `command` at 115.7% under the new rule, from 5,761.8s of real call overlap across 99 calls; overlap above a second in 72 of 169 | `~/.claude/projects/*/*.jsonl` | **executed 2026-09-09** by phase 1. This is `questions.md` Q3 |
| Four ledger rows anchor at `#report_spawns` and two at `#analyse`, so a comment inside either drifts them | `seal/ledger.md:101`, `:1818`, and #145's fragment | executed during #145's round 3 |

## Open questions → questions.md

One assumption, and one thing that is genuinely open: whether the span's new
definition needs a marking line in the readings already posted. The
measurement above says nothing moved, so the assumption is that it does not.
