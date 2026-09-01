# a subagent rediscovers what the session established — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens. -->

📋 implement applied
· spec:     `specs/1788224363-…/{routing,spec,plan,questions}.md`; issue #29
            with all five comments and the row moved in from #27;
            `docs/review-handoff-protocol.md` (whole, before extending it);
            `agents/smith.md`; `agents/warden.md`; `skills/implement/SKILL.md`
            §1; `templates/sdd-plan.md`; `.specseal/follow-up.md` (empty —
            nothing here was its prerequisite); `.specseal/map.md` header rules
· evidence: `.specseal/map.md` — one section, *What the cost meter can read*,
            five rows, stamped at the base tip per the template rule, plus a
            baseline-numbering row under *Evidence drift*. All five cite
            lines this branch touched; which four read DRIFTED at birth is
            decided by overlap with old-side hunks in baseline numbering,
            not by what was touched (executed: `evidence_check.py`, 31 ok ·
            4 drifted · 0 broken; the cause is round 1's finding 2)
· verified: executed — `tests/test_session_cost.py` (13 cases, the six new
            ones each shown red against the pre-fix meter first),
            `tests/test_the_handoff_before_round_one.py` (6 cases, each red
            before its prose landed), `test_broad_gate_rule.py`,
            `test_docs_line_wrap.py`, `test_one_word_one_meaning.py`,
            `test_review_axes.py`, `test_handoff_outlives_the_merge.py`,
            `test_the_last_rounds_fixes_are_checked.py`,
            `test_the_set_a_work_item_always_has.py`,
            `test_edits_go_through_the_edit_tool.py`, `ruff check` and
            `ruff format --check` on the changed Python files,
            `session_cost.py` against this run's own transcript. Read —
            `evidence_check.py` semantics at `:150-205` before choosing the
            stamp. Unverified — the full suite and tree-wide ruff; see below

## Why this work exists

The meter that measures what a spawned agent costs could not count above
1.00 tools per turn, so a day of conclusions was drawn from a floor. This
work makes the meter able to disagree with the rule it observes, gives the
pre-round-1 handoff the section round N→N+1 already had, states the batching
expectation in the contracts the meter now measures against, and points the
orchestrator at the progress readout the implementer was already writing.

## Acceptance — this run's own segments, measured with the meter it fixed

The owner's instruction: the meter fix lands first, and every later segment
of this very run is measured with it. The orchestrator appends the review
rounds' rows. Both readings below are **executed**, `session_cost.py --json`
against this segment's transcript (newest under `<session-id>/subagents/`).

| Segment | tools per turn | span | tool calls | model time share | repeats |
|---|---|---|---|---|---|
| `smith`, implementation — at the phase 1 commit | 1.27 | 9.2 m | 33 | 89% | 0 s |
| `smith`, implementation — at close of phase 4 | 1.27 | 16.4 m | 65 | 84% | 0 s |
| `warden`, round 1 — instructed, with the runner incantation omitted | **2.0** | 10.2 m | 19 | — | 0 s |
| `smith`, round-1 fixes — resumed rather than respawned | — | 3.9 m | 30 | — | 0 s |
| `warden`, round 2 (verifying) — instructed, runner incantation included | 1.5 | 4.2 m | 10 | — | 0 s |

The orchestrator appended the three review rows, **executed**, from each
round's report and its transcript. What they add to the reading above:

- **Round 1 is the first segment to hit the 2.0 bar**, and it is a reviewing
  segment — supporting the paragraph below that the bar fits reviewing.
- **Resuming beats respawning by roughly an order of magnitude.** The same
  fix-pass shape cost 45 m and 282 calls on the previous work item as a fresh
  spawn, and 3.9 m and 30 calls here as a resume with context intact.
- **A verifying round has fewer independent axes to open**, so its 1.5 is not
  a miss of the reviewing bar; the bar wants recalibrating per round kind.
- Each round lost exactly one round trip to a missing invocation: round 1 to
  the pytest runner (not yet handed over), round 2 to `evidence_check.py`'s
  argument shape (handed the pytest incantation, which fixed round 1's loss,
  and nothing else's). The protocol section's "runner incantation" means
  every checker the round will run, not pytest alone.

Against the issue's proposed bar (≥ 2.0 on every segment): **1.27 misses
it**, and the honest reading is that the bar fits reviewing segments better
than this one. Where the serial stretches were, from the transcript:

- The SDD-set writes — four `Write` calls that went out one per turn. The
  files are independent; this could have been two turns, not four.
- The phase 1 edit→test loop and the per-phase `git commit` calls — serial
  by data dependency, the shape the smith contract's caveat now names.
- What batched: the requirements read (the issue, the repo state, six
  constraint files), the suite runs, and the ledger-coordinate greps.
- `repeats: 0` on both readings — the instructed half of the rule held.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Piece 3 — the contract-override clause | The ticket: *"Put it in both `agents/smith.md` and `agents/warden.md`, naming the measured case"* / both files already carry it — `agents/smith.md:134-160` and `agents/warden.md:79-93`, with the 28-minute measurement, the WIDENING line and the ambiguous-instruction default | Verify, add nothing | `tests/test_broad_gate_rule.py` pins every half of the clause in both files (executed, green on this tree). The row moved from #27 to #29 after the clause had shipped with this history's initial commit; re-adding it would state the same rule twice, which is the drift that suite exists to catch |
| Ledger stamps | The spawn instruction: every row carries date+SHA / `templates/sdd-plan.md`: the Checked stamp may never name a commit the branch itself made | Both — date plus the base tip | All five rows cite lines this branch touched; four read DRIFTED and the fifth does not, because drift is judged in baseline numbering and these coordinates are HEAD-numbered — the re-stamp after the squash is what makes the tripwire cover them. The alternative — stamping the phase commit — reads OK today and falls back **silently** to the header baseline in every clone after the squash, which is the exact failure the per-row stamp exists to prevent, and which the previous work item's seven orphaned stamps now demonstrate (the follow-up row this work filed) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, `ruff check .` and `ruff format --check .` tree-wide | The broad gate — run once by the orchestrator after the review rounds settle (`agents/smith.md` §4; the spawn instruction says the same) |
| The review rounds' own meter readings for the acceptance table | The orchestrator, appending rows as each round's transcript closes |
| Whether a review segment actually clears the ≥ 2.0 bar now that the contracts state the expectation | The next `warden` round of this very work item — it is the experiment the issue's last comment asks for |

## Not done

The batching advisory threshold stays at 1.2 (Q1, default declared). No hook,
no mid-run reminder, no progress narration — all three declined on the issue
itself, and the multi-tool-turn-possible-at-all question is answered by this
run's own readings rather than by new mechanism: 1.27 measured here means a
multi-tool turn is possible and `session_cost.py` counts it above 1.00.

## Fed back into the spec

None beyond what `spec.md` already carried before the first edit. The
keyless-transcript degradation (one turn per row — the old floor, never an
inflated ratio) was written into the plan's failure scenario before
implementation and is pinned by the existing fixture cases.
