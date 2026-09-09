# Implementation Plan: red for following the documents, green for ignoring one

## Summary

Three arms, two scripts, one theme: a check at a pull request into `release/*`
judging a range or a state it was not built for. Each arm is a few lines and a
case; the work is in the cases and in the failure direction, which
`CONTRIBUTING.md` requires each of them to state.

## Technical context

Everything the three arms need already exists.

- `chain_check.py#pull_request_state` reads the draft flag from
  `GITHUB_EVENT_PATH` and `strict = state != "draft"` (`:2973`) is computed
  for every run. It reaches the `Pass` arm alone. #296 is that value reaching
  one more arm.
- The declaration walk already opens the last round record and reads its
  `Target SHA`. #295 reads one more cell from the record it already has.
  `chain_check.py` has no occurrence of `broad` today, so the cell's name and
  its `not yet` sentinel come from `round_record.py:325, 331` and belong in
  one place both can read.
- `survivor_check.py` already takes `--exempt <survivors.md>`, and
  `hygiene.yml:229` already loops every `seal/specs/*/survivors.md` into it.
  #297 is a second row shape inside a file the check already parses.

**The cutoff is not optional and it is why #295 is safe.** Every round record
ever written defaults to `Broad gate: not yet`, so an arm that reads the cell
without a cutoff fails every work item in flight — including #145, whose
rounds are running while this is built. The file already has seven cutoffs of
this shape (`STRICT_FROM` … `DEPTH_FROM`) and states the reason at `:127`:
*"A check whose first production act is red on history nobody can fix is a
check people learn to skip."* This adds the eighth, keyed on the work item id
the way the others are.

**Failure scenario, in six months.** A harness stops writing `draft` into the
event payload, `pull_request_state` returns `unknown`, and #296's arm decides
a real pull request is a draft — a missing round record then passes. The
existing function already answers this: `unknown` is not `draft`, so it is
strict, and the printed line names where the state was read from. The cases
have to pin that, or the fix for one ticket becomes a way past another.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#296**: the arm becomes draft-aware | A pull request that never leaves draft never meets the arm — but it also never merges, and `converted_to_draft` is already in the trigger list | **Chosen** |
| #296 alternative: `orchestration.md` opens the pull request after round 1 | The reviewer has no pull request to review, and the round record's `PR` cell has nothing to name. It moves the cost onto the review rather than removing it | Rejected |
| **#295**: read the `Broad gate` cell of the last record at a ready pull request | A record can name a SHA nobody ran anything at. The cell is written by the session that ran it, so this is the same trust the `Target SHA` already has | **Chosen** |
| #295 alternative: make the seal block's `broad gate:` line the source | It is prose in a session's output, and making it load-bearing changes what the seal block is. The record's cell exists and is already written on every record | Rejected, and recorded |
| **#297**: a whole-range row in `survivors.md` | A branch can declare a range and hide a real correction's survivor inside it. The grounds are a written sentence a reviewer reads, which is what the per-survivor row already relies on | **Chosen** |
| #297 alternative: exempt `docs/flow.md` by path | A real correction inside that file stops being checked, and `CONTRIBUTING.md` asks a separate argument for changing what a check guards | Rejected |
| #297 alternative: compare survivors against the durable copies | The most code of the three, and it encodes which files are durable — a list that rots | Rejected, and recorded |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #296 — the record-count arm reads the draft state; the message on a draft names what is missing without failing | cases: draft + no record passes · ready + no record still fails with the message unchanged · `unknown` is strict | `178fd44` |
| 2 | #295 — the `Broad gate` cell is read at a ready pull request, behind the eighth cutoff; `not yet` and a SHA older than the record's `Target SHA` each fail with their own sentence | cases: `not yet` fails · premature SHA fails · settled SHA passes · draft + `not yet` passes · an id below the cutoff is untouched | `7df4e69` |
| 3 | #297 — `survivors.md` takes a whole-range row with grounds; `survivor_check` honours it | cases built from #293's own range: declared passes, undeclared fails | `4558c21` |
| 4 | The fragments, and the four `CONTRIBUTING.md` answers written where the pull request will carry them | `evidence-check`, and the narrow modules | |

Each phase states its own failure direction in its phase record, because
`CONTRIBUTING.md` asks it per gate change and this branch changes three.

## Operational impact

All three make a gate **allow more**, and each says where:

- #296 allows a draft to lack a round record. Nothing that reaches `main` is
  exempt: `ready_for_review` re-runs the workflow.
- #295 allows nothing — it is a new refusal, and its blast radius is bounded
  by the cutoff to work items opened after it.
- #297 allows a declared range to keep its survivors. The declaration is a
  written sentence in the tree, read by a reviewer.

Prompt budget: **zero** for all three. No interactive path, no hook, no
question. Platform honesty: no process inspection anywhere in the change —
`git diff`, file reads, and one environment variable.
