# 1788686494-the-printed-ledger-name-collapses-through-relpath — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. -->

📋 implement applied
· spec:     `spec.md`, `plan.md`, `phases/phase-1.md`, `routing.md` (this work item); `CLAUDE.md` §*The goal a design is chosen against*, §*A ledger coordinate names content*, §*a change writes fragments, never the shared file*; `skills/agent-contract/SKILL.md` §1, §2, §7, §9, §12, §13, §15; `skills/implement/SKILL.md` §2, §3, §4; `seal/config.md` (no `Record language` row → English)
· evidence: four rows added to `seal/ledger/1788686494-the-printed-ledger-name-collapses-through-relpath.md`; that fragment reads 10 ok · 0 drifted · 0 broken at exit 0. `seal/ledger.md` deliberately untouched — see Not done
· verified: **executed** — 328 cases over every module asserting checker output text, exit 0; the three new cases each seen red first under a named mutation and green after; all five sites reverted in one batch to prove the class case names each; `uvx ruff check` and `uvx ruff format --check` on all three changed files, exit 0. **read** — the five-site enumeration's completeness argument, which is a closure over the ways a value moves rather than a search. **unverified** — the full suite, the repository-wide lint and the typecheck, which are the orchestrator's (`agent-contract` §2)

## Why this work exists

The evidence check opened one ledger and printed the name of another, so a
person acting on its output went and edited a file the run had never read.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many sites are in the class | Issue #163 named four; `plan.md` §Technical context predicted five and named the fifth | Five, confirmed by data-flow closure rather than by grep | `plan.md`: "the `--ledger narrowed this run` block, which prints `os.path.relpath(path, root)` under the name `path` rather than `ledger`. A grep for `relpath(ledger` finds four of five" |
| Where the source-reading case lives | `spec.md`'s acceptance table says only "a case that reads the source"; phase 1's record says the module it created "wants the same home" | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`, beside the unit cases | `phases/phase-1.md`: "Phase 2's source-reading case, which refuses a future `relpath` on a ledger path, wants the same home." One module per symptom sentence is this repository's convention, and the symptom is the same one |
| Whether the drifted rows in `seal/ledger.md` get re-stamped | `CLAUDE.md`: "Re-verifying is re-reading and then running `evidence-check --reverify`". Repo rule: "a change writes fragments, never the shared file … Appended is the word, and a removal is not one" | Left DRIFTED, named below | The two rules point opposite ways here and neither anticipates this case. Measured: `--reverify` cannot be scoped to a row — it re-stamped two rows that drifted before `885acf8` and this work item never opened — and doing it honestly bumps the `Checked` date on thirteen rows belonging to other work items. DRIFTED is the correct state and says *go re-read the claim* |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator, once, after the review rounds settle (`agent-contract` §2) |
| Four rows in `seal/ledger.md` now read DRIFTED because this change edited `check_ledger`, `migrate`, `reverify` and `main`. Their claims were re-read and hold; only the anchors moved | the orchestrator or the release step, by `evidence-check --reverify` over the whole ledger with every branch in flight in view |
| Two rows in `seal/ledger.md` — `templates/config.md#"# Repository config"` and `round_record.py#swallowed` — drift at `885acf8`, before this work item. Measured on the base tree: 680 ok · 2 drifted · 0 broken, exit 1 | whoever owns the work items those rows belong to; outside this change's scope and not touched by it |
| The integration case skips on Win32, so nothing pins the printed header end-to-end there. The premise is what is absent rather than the platform — Win32 folds `..` before the filesystem is consulted, so the guess and the answer name one file — and every other Windows behaviour of the helper runs from a POSIX machine by passing `ntpath` | the Windows CI leg, which runs the unit cases; a reviewer who disputes the premise should say so rather than asking for a skipped case to be unskipped |

## Not done

**`seal/ledger.md` was not re-stamped.** Editing four units moved four anchors,
so the shared ledger reads six drifted where the base reads two. Re-verifying
was attempted and reverted: `--reverify` operates per ledger file rather than
per row, so the run also re-stamped two rows that had drifted before this work
item began and that nobody here opened — certifying a claim nobody read is what
the ledger design exists to refuse — and re-stamping honestly means bumping the
`Checked` date on thirteen rows owned by other work items, in the one file the
fragment rule keeps branches out of. The four rows' claims were re-read and
hold. The alternative, re-stamping the four and hand-reverting the two, is one
edit away if a reviewer prefers it.

**The scan-suggestion site keeps its `os.path.relpath`.** `spec.md` puts it out
of scope and `phases/phase-2.md` carries the judgement. It renders a scanned
source file rather than a ledger, `os.walk` composes it downward so it carries
no `..` to fold, it is compared against a path spelled the way a ledger row
spells one, and it appends `.replace(os.sep, "/")` — which `display_name`
deliberately does not do, so routing it through the helper would change what
Windows prints for every `(moved?)` hint. A case pins it out of the class in
both directions.

**The detector behind `test_no_ledger_path_reaches_relpath` over-reaches.** Its
return rule marks two names that are not paths — `main`'s `findings` and
`resolve_patterns`' `key`. Narrowing it was not attempted: the over-reach can
only produce a false alarm, never a false pass, and a false pass is this defect
again.

## Fed back into the spec

None. `spec.md`'s scope and acceptance rows were written before phase 1 and
both phases landed inside them; `plan.md` had already predicted the fifth site
and the scan-suggestion judgement, so nothing was inferred during
implementation that the plan did not already carry.
