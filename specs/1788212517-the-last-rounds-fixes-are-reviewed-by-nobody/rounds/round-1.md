# 1788212517-the-last-rounds-fixes-are-reviewed-by-nobody — review round 1

| Field | Value |
|---|---|
| Target SHA | `617d0c0` |
| PR | not yet |
| Broad gate | not yet |
| Fixes checked by | `round-2` |
| Needs a fix | yes — three 🔴 and seven 🟡, all closed below |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The `no fixes to check` refusal never fired on the spelling every record in this repository uses. `verdict_of` lowercased and stripped and nothing else, so `**fixed** \`d3fe44d\`` matched neither `FIX_WORDS` nor `CLOSED_WORDS` | `chain_check.py:824` · `:222` | **fixed** `ef1cfba` | Verified by the orchestrator before the fix, executed: fourteen closed verdicts across `specs/1788184145-…/rounds/round-{1,2,3}.md` are `**fixed**`, ten of them with a commit after the word, and **zero** are the bare `fixed` the vocabulary was spelled with. `open_blocking` shared the same normalizer, so a 🔴 legitimately closed read as still open |
| 🔴 2 | Option A's rules could be written backwards and nothing went red. `assert "after the fixes" in skill` and `assert "diff of" in text and "fixes" in text` are substring greps; `fixes` appears 4–18 times per carrier | `tests/…:429` · `:461` | **fixed** `60e4cb8` | The reviewer inverted both axes in `skills/code-review/SKILL.md:167-168` and the suite returned **27 passed**. Option A is prose in four documents with no code enforcing it, so these cases were the only thing holding it. Now pinned as whole rows and sentences per axis, with the inverted spelling refused beside each |
| 🔴 3 | `overview.md` claimed *"The field is not read on records the pull request does not touch"*, and the code reads it on every record | `overview.md:68` ↔ `chain_check.py:1294` · `:1305` | **fixed** `851fa90` | The code carries the comment *"EVERY record, where the block above reads the last one alone"* with its reason, and `CHANGELOG.md` and the `chain_check.py` docstring agree with it. The memo was the outlier. Judged by the orchestrator, read. The cost the reviewer measured — one line of a work item's `routing.md` puts the declaration in the diff and every historical record in that item is then read — went into `questions.md` Q2 rather than being fixed silently |
| 🟡 4 | The case pinning the `nobody` trade searched `chain_check.py` for `teaches people to write none`, which has sat at `:82` since `9829412 Initial commit` about a different gate. Deleting the whole new 45-line docstring section left the suite green | `tests/…:394-409` | **fixed** `60e4cb8` | The reviewer ran `git log -S` and got the initial commit. The case's own docstring had already warned about this failure mode one spelling earlier, so the lesson recorded is that a needle is chosen per document, not once |
| 🟡 5 | The checker refusal said *"one that ran before these fixes existed"* and compared round numbers only. Two records with the same `Target SHA`, round 1 naming round 2, exited 0 | `chain_check.py:919-930` | **fixed** `225b9b7` | `Target SHA` was already read on the same record and `reachable()` already existed. A named checker's own target must now be later — the same commit, or an ancestor, fails |
| 🟡 6 | The template row a session copies could be misspelled, widened to `any round`, replaced with a refused value, or moved inside the comment block, and the suite stayed green. Row counting counted lines inside comments | `templates/sdd-round.md:15` · `tests/…:374` | **fixed** `60e4cb8` | Rows are now counted outside comments through the real `strip_comments`, and the value is pinned |
| 🟡 7 | `spec.md` said last-record in one place and every-record in another; `plan.md` named `check_round` as the reader where that function's own docstring says it is not, claimed one migrated record where the same file said three | `spec.md:24` ↔ `:78-82` · `plan.md:52` · `:118` · `:120` ↔ `:95` | **fixed** `851fa90` | Read. The scope changed mid-implementation when mutation testing showed the first shape made `round-N` unreachable, and the documents were not all brought along |
| 🟡 8 | Three citations named `tests/test_the_last_rounds_fixes.py`, which does not exist | `spec.md:61` · `:69` · `tests/test_chain_check_at_the_pull_request.py:114` | **fixed** `851fa90` | Executed — the file is `tests/test_the_last_rounds_fixes_are_checked.py` |
| 🟡 9 | Three branches had no case: the separator check after `nobody`, backtick stripping, `.md` suffix tolerance. Each could be deleted with the suite green | `chain_check.py:870` · `:913` · `:917` | **fixed** `225b9b7` | The backtick branch is the one closest to practice — every document writes the value in backticks, so a session copying the template's spelling depends on it |
| 🟡 10 | `agents/warden.md:66` tells the reviewer to say plainly whether it opened anything needing a fix, and neither the report format nor the round record had a field for that answer. `agents/warden.md` itself refuses this shape | `agents/warden.md:66` ↔ `:199-206` | **fixed** `225b9b7` | The verifying round's terminal condition **is** that answer, so option A had no channel for the thing it ends on. `Needs a fix` now exists in the record, the reviewer's report format, the skill and the protocol. Migrating it onto the three merged records was **rejected** — a reviewer nobody asked left no answer, and deriving one from the verdict table is the exact derivation the field is defined against (`6fe9c73`) |
| ❓ 11 | Nothing enforces the round cap in code; `chain_check.py:1279` prints it. Whether a cap exhausted while a verifying round opens something is a third case the spec's paragraph denies could not be judged | `chain_check.py:1279` | answered | Became `questions.md` Q4 with the repository owner as answerer. Not this round's fix: the cap's enforcement is a separate mechanism from the field and the verifying round, and building it here would widen a diff already under review |

## Executed probes

| What was run | Result |
|---|---|
| `awk` over the verdict cells of `specs/1788184145-…/rounds/round-{1,2,3}.md` | 14 `**fixed**` variants, 7 `answered`, **0 bare `fixed`** — 🔴 1 confirmed independently of the reviewer |
| `chain_check --baseline origin/main` (reviewer) | exit 1; `round-3.md`'s `nobody` prints. Q1's premise confirmed — the strict version would redden this repository's own release pull request |
| Option A's two axes inverted in `skills/code-review/SKILL.md:167-168` (reviewer) | **27 passed** — 🔴 2 |
| `git log -S"teaches people to write none" -- chain_check.py` (reviewer) | `9829412 Initial commit` — 🟡 4 |
| Two records with the same `Target SHA`, round 1 naming round 2 (reviewer) | exit 0 — 🟡 5 |
| Twenty targeted mutations over the fixes, each reverted and the tree re-checked green | each red; 57 cases in `tests/test_the_last_rounds_fixes_are_checked.py` |
| Nineteen narrow test files at `6fe9c73` | 473 passed |
| `evidence_check.py` · `unverified_check.py` | 24 ok · 0 drifted · 0 broken · exit 0 |

The full suite, `ruff check .` and `ruff format --check .` across the tree did
not run. The broad gate is the orchestrator's, once, after the rounds settle.

## Inherited coordinates

Round 1 inherits nothing. This section carries for round 2.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The round cap is printed, not enforced, and a cap exhausted while a verifying round opens something is a case the spec denies | `questions.md` Q4 | the repository owner |
| Reading the field on every record makes a one-line `routing.md` edit fail on a work item's historical records | `questions.md` Q2, which owns this axis | the repository owner |
| Whether verifying rounds need a bound. The default is an argument rather than a measurement | `questions.md` Q3 — its first measurement arrives from this work item's own round 2 | the repository owner |
| `.specseal/map.md` had three coordinates drifted by hundreds of lines while `evidence_check` reported `ok` | issue #31, where the orchestrator recorded it | the repository owner |
