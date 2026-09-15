# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `703cf9c` |
| Ran by | specseal:smith on Claude Opus 5 (1M context) |

## What this phase was asked

#333. `depth_two` attributes a unit to the row whose fix commit added it,
using the commits `close` already resolves for the fix table, and falls back to
the file-level answer only where a range cannot resolve one. The refusal still
fires on the fallback, and its message says the attribution is file-level and
names every candidate finding rather than asserting one. The exit sentence is
unchanged. Cases built on the measured #30 shape and on a single-commit range
that forces the fallback.

## What this phase found

**Q5 is answered *not derivable*, and the cost is measured rather than
assumed.** `close` resolves every `fixed` commit and places it inside the
range, but `measure` compares the range's **two ends** and never asks which
commit introduced a unit — so the per-commit answer needs a second pass.
`unit_adders` is that pass, one `measure` per `fixed` commit over that commit
alone.

| Over a two-commit, one-file fix range | Time |
|---|---|
| `measure` over the range | 36.4 ms |
| `unit_adders` over the two fix commits | 127.8 ms |
| ratio | **3.51×** |

The cost is dominated by git subprocesses rather than by AST work — each pass
runs `touched` and then parses only the files that ONE commit changed — and it
is bounded by the fix range, which is two or three commits. 128 ms is far under
one round trip, so the default in `questions.md` stands.

**A fixture constraint that is a finding of its own, and it is not repaired
here.** `units_named_earlier` runs each `New units` entry through
`chain.EMPHASIS`, which is `[*_`]+`, applied to the WHOLE entry — so
`only_tested` is read back as `onlytested`, while the names in `added` come
from the AST unstripped. `unit not in named` is therefore true for **every
snake_case parent**, which is most Python units, and the depth-2 walk reaches
none of them.

Measured 2026-09-15 while building the cases: committed records write entries
like `` `test_a_cell_of_only_separators_is_not_an_answer` ``, and this reads
them as one long word. It also explains something #333's own body records
without explaining — the refusal fired on #30 through `quote`, which carries no
underscore, and named `quote` as the parent for units added by a fix inside a
unit that does.

It is **outside this work item's six tickets** and it widens what the rule
refuses, which is a change to a gate. So it is a `# RIDER:` at
`units_named_earlier`, stamped, with the repair named (strip the emphasis
characters from the ENDS of the entry rather than everywhere in it) and the
repository owner as answerer — and both of this phase's cases use
underscore-free parent units for that reason, which their own comment states.

**What the file-level walk got wrong is two things, not one**, and the cases
assert both. It named the wrong finding AND the wrong enclosing unit, because
the parent comes from the row the walk paired the unit with. A case asserting
only the finding would pass against a repair that fixed the pairing and kept
the parent.

**Q4's answer for this phase.** Four anchors drifted: `close` and `depth_two`
(carried by `seal/ledger.md` R2), and two heading anchors in
`docs/review-chain-spec.md`. R2 is the row `plan.md` flagged for a substance
re-read, and it holds on all three of its counts — the fix SURFACE is still
measured from the range's two ends, because `unit_adders` feeds the depth
walk's attribution and nothing the `Contract changes` or `New units` cells
carry; the refusal still comes before any cell is written; `Fixes checked by`
is untouched. `evidence-check --strict` exit 0 at 1249 ok · 0 drifted ·
0 broken.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The single-raise inside the candidate loop, which refused on the first file-level match it reached | The collected walk below it, which builds every candidate first and then decides per unit whether the range attributes it. Nothing is lost: the refusal still comes before any cell is written, and it now reports every offending unit in one message rather than the first |
| Nothing else. The exit sentence, the depth rule and the grandfathering are untouched | — |
