# 1788873620-two-in-range-values-make-one-that-is-not — overview

📋 implement applied
· spec:     `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments*, §*a ledger coordinate names content*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `docs/flow.md` §*0.9.3 — the enumeration was done by reading*; `skills/agent-contract/SKILL.md` §§1–2, 4–5, 9–10, 12, 14–15; `skills/implement/SKILL.md` §§1–4; `seal/config.md` (Record language absent → English); `seal/follow-up.md` (read; no row is a prerequisite of this work and none was drained); `seal/ledger.md` R3 and R6 of work item `1788700685`; that item's `rounds/round-3.md` and `rounds/round-4.md`; `seal/specs/1788700685-…/phases/phase-1.md` §*The enumeration, and why it is complete rather than merely larger*; issue #192; `seal/specs/1788873620-…/routing.md`
· evidence: three rows added in `seal/ledger/1788873620-two-in-range-values-make-one-that-is-not.md`; one row re-read in `seal/ledger.md` (R3 of `1788700685`) — its `#token_thirds` hash and its Checked and Notes cells
· verified: **executed** — `tests/test_a_derived_number_reaching_an_int_carries_a_guard.py` (38 cases) and `tests/test_session_cost.py` (36) together, 74 passed, exit 0; a 44-mutation battery, one mutation at a time, 43 caught; `uvx ruff check` and `ruff format --check` on the two touched files, clean; `evidence_check.py --reverify`, 8 rows re-verified, exit 0. **read** — the base suite figure (2808 passed, 2 skipped in 439.63s at `c0a65d5`), handed over by the orchestrator and not run here. **unverified** — the full suite, whose answerer is the orchestrator

## Why this work exists

`count` answers for each value entering a transcript and nothing answered for
what the arithmetic made of two of them; the one site was fixed in 0.9.2, and
this closes the class so that a *new* int-conversion site added without a
guard is refused by the suite instead of by the next review round.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether the three measured shapes of #192's table pass at the base | The spawn prompt: *"They pass at `origin/release/v0.8.3` and after round 3's fix."* #192's own table: at the base, *"exit 1, stdout empty, both arms"* | Read as *the cases pass after the fix*; nothing was re-measured at the base | The ticket outranks the prompt on a fact the ticket measured — `agent-contract` §5, and `implement` §1's precedence, put a prompt's prose below the record it summarises. The three shapes pass at HEAD, which is what this branch needs; re-measuring at the base is work #175 already did and recorded |
| What makes a site a member | `plan.md` §Summary: the six-method integer-conversion protocol | The protocol **and** an exact-`int` answer to a benign number | Building it showed the first probe alone classifies `math.isfinite` as a member, which reddens the shipped module at `token_thirds`, where `mean` is a float by construction and the call cannot raise. The owner's own wording is *converting a derived number **to** an int*, and the second half is the other clause of that sentence. `phases/phase-1.md` holds the measurement; the alternative was dead defensive code or a provenance pass |
| What a `try` guard must catch | `plan.md` §Operational impact: `OverflowError` **and** `ValueError`, stated as the deliberate refusing direction | Whatever the conversion is probed to raise | The written pair is the shape this release exists to replace, and it was also wrong for `count`'s `math.isfinite` guard, which catches `OverflowError` alone and correctly. Probing answers the same question by measurement and yields a third discharge for free. The refusing direction the plan argued for survives — a `try` catching one of two seen failures is still refused, and that shape is in the table |
| `integer_shaped` and `bool` | The first implementation excluded `bool`, copying `count` | `bool` counts as an integer literal | Found by mutation: the exclusion refuses `round(True)`, which cannot raise. `count` excludes `bool` because `True + 1` is a wrong number in a token column, and that reason does not reach a question about whether a transcript could have derived the operand |
| Where the phases landed | `plan.md`'s table has three | Phase 1 carried both the checker and `token_thirds`' docstring; the mutation battery became phase 2 because it changed code | The docstring is what the checker's last case pins, so shipping them apart would have shipped a red case. The battery earned a phase of its own on the same rule — it altered `integer_shaped` and added a discharge shape |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and typecheck. `agent-contract` §2 reserves them; the base figure (2808 passed, 2 skipped, `c0a65d5`) is cited as **read** | the orchestrator |
| Whether the class should include subscript and slice bounds, which convert through `__index__`. Both available rules are wrong in one direction and the measurement is in `questions.md` Q1 | the repository owner |
| Whether membership should widen from *converts* to *raises*, which would catch the true-division route and also flag `share`'s `part / whole * 100`. `questions.md` Q2 | the repository owner |
| The probe calls every callable the module's source names, with an operand that answers no protocol but the six. Nothing here reaches a filesystem today, checked callable by callable; what is not verified is that a future edit cannot add a call whose mere invocation matters | the repository owner, if the checker's docstring bound is ever judged too weak |
| `Converted`'s base class. It survived the mutation battery and no case can tell `BaseException` from `Exception`, because `_recorder` records before it raises; recorded in the docstring rather than pinned by a case that would prove nothing | the repository owner |

## Not done

**The wrong-number direction was not touched**, on the owner's instruction: a
finite but nonsensical count — a negative token total — still sums as given
and prints. It stays open on #192's body, and the last sentence of
`seal/ledger.md` R3's clause still describes it correctly.

**Neither widening in `questions.md` was taken.** Q1 (subscript bounds) needs
a provenance pass whose two available shortcuts are each wrong in one
direction; Q2 (membership by *raises*) changes a site — `share` — that #192
did not ask about and nobody has measured a failure at. Both are recorded
with the measurement rather than left as impressions.

**The two instrument defects scheduled into 0.9.4 were left alone**, and
nothing here pins either behaviour as correct. Neither is touched by the
class: #200 lives in `FAMILIES`, which the walk classifies as a
non-converting site, and #202 lives in `load`'s per-message counting, whose
only conversion-shaped neighbour is the addition `count` already funnels. The
0.9.4 branch should know that `token_thirds`' docstring grew, since that is
`#193`'s own unit.

**No transcript case was added.** The three measured shapes of #192's table
are `tests/test_session_cost.py`'s already, planted by round 3 of #175, and
re-running them is the right relationship to them; adding a fourth arm would
pin the same behaviour twice.

## Fed back into the spec

None. The rule this branch adds lives in `token_thirds`' docstring and in the
checker, both of which are code; no policy document in `docs/` gained a
clause, and `CONTRIBUTING.md` §*What a change to a gate must carry* was
answered rather than amended — the test seen red, the stated failure
direction, the prompt budget of zero, and the platform note (macOS only; the
probes are pure Python with no process inspection).
