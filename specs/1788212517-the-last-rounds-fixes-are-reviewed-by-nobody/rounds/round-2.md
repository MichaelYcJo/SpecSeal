# 1788212517-the-last-rounds-fixes-are-reviewed-by-nobody — review round 2

<!-- The first verifying round this repository has run. Its target was the diff
of round 1's fixes rather than the branch, which is what `docs/review-chain-spec.md`'s
*The last round verifies, and what it verifies is a diff* asks for. It opened
something needing a fix, so it consumed a round like any other. -->

| Field | Value |
|---|---|
| Target SHA | `2ea13da` (the diff `617d0c0..2ea13da`) |
| PR | not yet |
| Broad gate | not yet |
| Fixes checked by | `round-3` |
| Needs a fix | yes — one 🔴 at the site round 1 was closing, six uncovered branches, five documents contradicting the code |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A verdict citing a commit with no digit reopened the finding it closed. `CITATION` required a digit inside the hex run, so with none it did not cut at all and `**fixed** \`deadbee\`` normalised to `fixed deadbee` — outside the vocabulary, so a properly closed 🔴 read as still open | `chain_check.py:261` · `:881` | **fixed** `8a5628a` | Reproduced by the orchestrator before handing it over, executed. **This is the same site round 1 was closing**, which `docs/review-chain-spec.md:34-56` calls the structure signal whatever the count, so the run stopped and the repository owner was asked. The answer was to change the structure rather than add a special case: `CITATION` is gone and the vocabulary is matched as a prefix of the cell. Re-verified by the orchestrator at `4eb098f` — `deadbee`, `defaced` and `d3fe44d` all give `fixed`; `not fixed` and `fixedly` stay outside the vocabulary and count open; a long `answered` cell mentioning a fix still gives `answered`. No existing round record needed editing |
| 🟡 2 | Six branches this diff added had no case. Two were `CITATION`'s and left with it; the other four survived mutation | `chain_check.py:261` · `:1005` · `:1007` · `:1189` | **fixed** `8a5628a` | Two were real holes rather than test gaps. `templates/sdd-round.md:12` allows two SHAs in `Target SHA`, and `reviewed_later` compared the checker's newest against this record's **first**, so a round that read exactly what this round read passed as its checker — both sides now read the newest. And the cutoff comparison is `>=` with `STRICT_FROM` equal to this work item's own id, while both fixtures sat hundreds of millions of seconds away; the new case reads `STRICT_FROM` from the module rather than hardcoding the second, so it pins the boundary and not a number |
| 🟡 3 | Five documents said the code does what it stopped doing. The refusal table called a case *passes* that the code exits 1 on; `README.md` contradicted itself; the spec's opening paragraph contradicted its own table; `overview.md` announced a false claim on every `unverified_check` run; `plan.md` said one record where the same file said three | `docs/review-chain-spec.md:533` · `README.md:187-191` ↔ `:369-371` · `docs/review-chain-spec.md:178-181` · `overview.md:78` · `plan.md:85` ↔ `:141` | **fixed** `9b5501d` | This is round 1's 🔴 3 and 🟡 7 recurring inside the commits that closed them. `README.ko.md` had both places fixed and the English file one, which `CONTRIBUTING.md`'s both-editions rule forbids. Six prose coordinates were also re-aimed, not five — the reviewer found two and the smith found four more |
| 🟡 4 | The negative needles catch a rule rewritten in place and not a document that keeps the sentence and states the opposite elsewhere. Three such additions passed | `tests/…:709-710` · `:731-736` · `:753-758` · `:777-781` | answered | Enumeration cannot close this, and that was accepted. What was not acceptable was the comment claiming a reach the code does not have — the paragraph beside it warns against exactly that forgery. The comment now states the real reach: in-place rewriting only |
| 🟡 5 | `test_the_answer_the_run_ends_on_has_a_field` asserted a phrase was present, so renaming the protocol's table row passed on the phrase surviving in prose | `tests/…:851` · `docs/review-handoff-protocol.md:115` | **fixed** `9b5501d` | The weak half was kept and labelled; a case counting the row **as a row** was added beside it. Under a `\| Needs fixing \|` rename the four existing cases stay green and only the new one goes red |
| 🟡 6 | The test module's docstring said the field is read on the LAST record while the same file said EVERY record | `tests/…:18` ↔ `:207` | **fixed** `9b5501d` | Predates `617d0c0`, and this diff rewrote 592 lines of that file without catching it |
| 🟡 7 | `agents/warden.md` told the reviewer to copy its line into the `\| Needs a fix \|` row *straight*, producing `\| Needs a fix \| Needs a fix: no \|`. Nothing said to drop the prefix | `agents/warden.md:218` | **fixed** `9b5501d` | Raised by the reviewer as the field's first user. Both the instruction and the template placeholder now say the value stands after the colon, with the wrong form shown beside it |
| 🟡 8 | Two ledger rows quote a markdown row's name with its pipes, so a five-cell row splits into seven and every column slides right. On `:61` the `Checked` column landed on prose and the row fell back to the header baseline — on a row about the very check this work item adds | `.specseal/map.md:61` · `:66` | **fixed** `3002dbb` | **Found by the orchestrator, not the reviewer**, executed: parsing the table header per section and reading `Checked` by name. `evidence_check.py` reported 24 ok · 0 drifted · 0 broken on both, because it reads coordinates out of the text and never validates a row against its section's header — `evidence_check.py:13-16` is what makes the fallback silent. Re-verified after the fix: 23 rows, 0 malformed, every `Checked` carrying a SHA |
| ❓ 9 | Whether `evidence_check` should refuse a row whose cell count disagrees with its section header | `evidence_check.py` | answered | Deliberately not built — it widens this diff into a file this work item does not touch. Sent to issue #31, which already covers the checker being green on rows that claim what it never verified. Round 1 sent the same file's coordinate drift there |

## Executed probes

| What was run | Result |
|---|---|
| `verdict_of` on seven spellings, at `4eb098f`, by the orchestrator | `deadbee` · `defaced` · `d3fe44d` → `fixed`; `not fixed` · `fixedly` → outside the vocabulary; long `answered` cell → `answered`; `agreed, fixed \`abc1234\`` → `agreed, fixed`. `CITATION` no longer exists in the module |
| Every verdict cell in `specs/*/rounds/round-*.md` through the real `verdict_table` | 34 of 34 recognised. No existing record needed editing |
| Seven mutations, each red then restored and re-checked green | round 1's cutting regex restored (8 cases red) · whole-cell search · word-boundary removal · `mine[-1]`→`mine[0]` · `theirs[-1]`→`theirs[0]` · squash path deleted · `>=`→`>` |
| A protocol-row rename to `\| Needs fixing \|` | four existing cases green, the new row-counting case red |
| 26 narrow suites touching the changed files | 755 passed |
| `chain_check` in a fresh clone, three directions | with `round-2.md` present: exit 0. Round 2's target rolled back to `617d0c0`: exit 1, same-commit refusal. `nobody` beside a checked `Pass`: exit 1 — the first time the refusal fired on a real record rather than a fixture, because this work item's id **is** `STRICT_FROM` |
| `.specseal/map.md` parsed per section by header | 23 rows, 0 malformed, every `Checked` carrying a SHA |
| `evidence_check.py` · `unverified_check.py` | 28 ok · 0 drifted · 0 broken · 7 open · 2 closed |

The full suite, `ruff check .` and `ruff format --check .` across the tree did
not run. The broad gate is the orchestrator's, once, after the rounds settle.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 🔴 1 | `chain_check.py` `verdict_of` | Round 1 fixed it here and round 2 reopened it here. A third change at this site is the signal, not a finding |
| round 1 🔴 3 · 🟡 7 | `overview.md` · `spec.md` · `plan.md` · `README.md` | Both rounds found prose that outlived the code it describes, and round 2 found five more inside round 1's own fixes. This is the class that recurs |
| round 2 🟡 2 | `chain_check.py:1005` `reviewed_later` · `:1189` the cutoff | Two behaviours whose only defence, until this round, was that nobody had written the fixture |
| round 2 🟡 8 | `.specseal/map.md` row shape | The checker still cannot see a malformed row. Fixed by hand here; the mechanism is issue #31's |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `evidence_check` should refuse a row shape mismatch, or a `Checked` cell with no SHA | issue #31 | the repository owner |
| Whether the negative needles should reach a document that adds an opposite sentence elsewhere | the comment at `tests/…:709-710` now states the real reach; the widening is not scoped | the repository owner |
| `VOCAB`'s longest-first ordering is a defence nothing verifies — no current word is a prefix of another, so a case for it could not fail | recorded in the code comment and a ledger row rather than as a counterfeit test | the repository owner |
| Q2, Q3, Q4 | `questions.md`, unchanged. Q3 gained its first measurement in the row and stays ⬜ | the repository owner |
