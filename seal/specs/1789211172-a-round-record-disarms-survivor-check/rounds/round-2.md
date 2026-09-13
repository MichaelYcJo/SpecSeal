# 1789211172-a-round-record-disarms-survivor-check — review round 2

| Field | Value |
|---|---|
| Target SHA | fb64d06 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #372 |
| Broad gate | 9a1246d against bc5248c |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

# round 2 — the verifying round, and the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `fb64d06` — HEAD had not moved when the round ended |
| Diff under review | `b9caadb..fb64d06` — the fix pass's two commits and round 1's closure |
| Base | `release/v0.11.2` = `bc5248c` |
| Draft pull request | #372 |
| Ran by | specseal:warden on claude-opus-5 |
| Inherits | round 1 — seven findings, six `fixed`, one `answered`, plus two rows checked and found clean |

## What this round was for

The fix pass's own diff, and nothing else. Round 1 opened and closed the filter
on `corrected`, `whole_range`'s unfiltered list, phase 1's red output and A6;
the reviewer was told to inherit those rather than re-derive them.

Six things by name:

1. **Finding 1's fix** — the enumeration case's unit became the call site, with
   `PATH_LIST_CALLS`, `MODULE_SCOPE` and `_path_list_words` shipping unreviewed.
   Two of the smith's six mutations had already been re-taken by the
   orchestrating session; the reviewer was asked to take the other four, or a
   shape neither had tried, and to judge whether the unit is now tight enough to
   be brittle.
2. **The smith's refusal of round 1's paste-ready fix**, and its measurement of
   why — a claim about the reviewer's own proposed remedy.
3. **The five ⬜ corrections**, including finding 6's deliberate retention of a
   tautological conjunct as two assertions.
4. **The two things the fix pass found on its own** — the `#371`/`#308` clause,
   and the restoration of a `## Not verified` row the orchestrating session had
   deleted rather than marked closed.
5. **The ledger** — S2 widened from *every function* to *every call site, module
   scope included*, re-verified rather than re-pointed.
6. **The survivor step, checked rather than read**, because this work item is a
   change to that gate and it is where a wrong call is least visible.

## What was withheld

The broad gate, still the sealer's. Pushing, committing, and the pull request,
per `agent-contract` §6.

**The reviewer was told in as many words not to manufacture a finding to justify
the round**, because a verifying round that opens nothing needing a fix does not
consume the cap and that was a real possible outcome.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The enumeration case measures function names, so a second unfiltered path list inside an already-declared function, or one at module scope, passes it | `tests/test_a_corrected_sentence_survives_elsewhere.py:615`, `:676` | answered | Closed at `b002b3f` on my own grounds. Executed ten red shapes, four of the smith's six re-taken here and six neither side tried — async, a nested function, a class method, and module scope reached three ways (a direct `subprocess.run`, inside an `if`, inside a comprehension). Module restored byte-identical after each, checked by hash |
| 2 | 🟡 The pull request body attributes four red mutations to the enumeration case; `phases/phase-3.md:57` records two | PR #372 body | answered | Round 1 closed it in the body, not in the tree, and no commit ever carried the claim. Nothing in this diff re-introduces it |
| 3 | ⬜ The memo's executed line omits the one repository-wide `ruff` run the smith disclosed | `seal/specs/1789211172-…/overview.md:10` | answered | Read. The line now names the run, the two contract sections, and that it is spent rather than banked |
| 4 | ⬜ Phase 5's removal table names one changed clause; the follow-up edit changed two | `phases/phase-5.md` removal table | answered | Read. The second row is present with the grounds and with the limit — the eleven-to-one figure is of the added side alone |
| 5 | ⬜ `_mentions` and `_function` accept only `FunctionDef` | `tests/test_a_corrected_sentence_survives_elsewhere.py:671`, `:773` | answered | Executed: an async path-list function is now red with the enumeration message rather than with *is no longer a function in this module* |
| 6 | ⬜ `"foreign" in grounds` is a tautology, and its failure message blames the module | `tests/test_a_corrected_sentence_survives_elsewhere.py:760` | answered | Read, and the smith's judgment is right. The conjuncts fail for opposite reasons — `grounds` is a constant in the case, `body` comes from the module — so two messages blame the correct party each. The first fires when the recorded grounds are reworded away from `foreign` |
| 7 | ⬜ The docstring case's message names the wrong pair | `tests/test_a_corrected_sentence_survives_elsewhere.py:574` | answered | Read the pinned paragraph: its *both sides* is the two sides of the range's path list. The corrected message names that pair |
| 8 | ⬜ After the classify act, a second **unfiltered** site in a declared scope passes — `_mentions` cannot tell which of two calls carries the filter | `tests/test_a_corrected_sentence_survives_elsewhere.py:723`, `:671` | deferred #373 | #373 |

## Checked and found clean

Not findings, so they carry no id — a fix table's `#` is a bare integer and a
row here has nothing for a fix pass to do. Each is something this round was sent
to check rather than to hunt, and each was opened and found to hold.

| What was checked | Location | Verdict | Grounds |
|---|---|---|---|
| The smith's refusal of round 1's paste-ready fix | `tests/test_a_corrected_sentence_survives_elsewhere.py:628` (`_path_list_words`) | answered | Executed both shapes on the same mutated tree: the subtree-reading shape counts `corrected: 1` and passes, the shipped shape counts 2 and fails; they agree on the unmutated module. The refusal is correct |
| No `survivors.md` written | `.github/workflows/hygiene.yml`, the two ranges | answered | Executed both ranges: the gate's range exits 0 with nothing standing, the fix range's five places all trace to a body that did not exist at `bc5248c`. Reading `hygiene.yml`, every `seal/specs/*/survivors.md` is handed to every run, so five rows of generic `ast` idiom would silence it for every future branch |
| The ledger's S2 widening and S3 re-verify | `seal/ledger/1789211172-a-round-record-disarms-survivor-check.md` | answered | The widened claim is what the code does, measured. Re-verified rather than re-pointed is correct: the anchor names a unit that still exists. `evidence-check` exit 0, 1149 ok, 0 drifted, 0 broken |
| The restored `## Not verified` row | `seal/specs/1789211172-…/overview.md` | answered | All four phase records carry `specseal:smith` on `claude-opus-5`, so the row's claim is true. The blind-spot claim holds: the memo is absent at `bc5248c` and `unverified-check --baseline bc5248c` exits 0 either way |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` at `fb64d06` | 47 passed, exit 0 |
| Mutation: the filter removed from `corrected` | red — `corrected derives a path list and no longer applies records_a_past_round` |
| Mutation: a fourth unfiltered path-list function | red — names the four scopes against the three declared |
| Mutation: two path lists in **one outer call's arguments** inside `corrected` | red — `{'corrected': 2}` against `{'corrected': 1}` |
| Mutation: a second unfiltered caller of `tracked` | red — `tracked is reached from ['audit', 'corpus']` |
| Mutation: an **async** path-list function | red — the enumeration message, not the *no longer a function* one |
| Mutation: a path list in a **nested function** inside `corrected` | red — the inner scope is named separately |
| Mutation: a path list in a **method of a class** | red |
| Mutation: a direct `subprocess.run` path list at **module scope** | red — reports `<module>` |
| Mutation: a module-scope path list **inside an `if` block** | red — reports `<module>` |
| Mutation: a module-scope path list **inside a comprehension** | red — reports `<module>` |
| Refactor with no defect: rename a local in `corrected`; the call reflowed across lines | green, green — no false red |
| Refactor with no defect: git arguments hoisted into a tuple | **red** — and red against the pre-fix case at `b9caadb` too, so inherited rather than introduced |
| Refactor: a second but already-**filtered** path list in `corrected` | red (green before the fix) — judged a correct tightening, `_mentions` cannot tell which site filters |
| Finding 8: a second **unfiltered** path list, count bumped to 2 | **green** — the residual |
| Round 1's paste-ready shape vs the shipped `_path_list_words`, on the nested-calls mutation | `{'corrected': 1}` passes vs `{'corrected': 2}` fails; identical on the unmutated module |
| `bin/survivor-check --range bc5248c...fb64d06` — the gate's own range | **exit 0** · 902 files · 6 removed sentences · no removed wording still standing |
| `bin/survivor-check --range b9caadb..fb64d06` — the fix pass's range | exit 1 · 14 removed sentences · 5 places, all naming the old `_derives_a_path_list` body |
| `bin/evidence-check .` at `fb64d06` | exit 0 · 1149 ok · 0 drifted · 0 broken · `0 refused` |
| `bin/unverified-check` on the memo | exit 0 · 5 open · 1 closed — the restored row is the closed one |
| `bin/unverified-check --baseline bc5248c` | exit 0 — the memo is absent at the base, so the deletion was invisible to it |
| The four `phases/phase-N.md` records, read for `Ran by` | all four carry `specseal:smith` on `claude-opus-5` |
| The broad gate — the full suite, the repository-wide lint, the format check | **not yet.** Unrun and unclaimed at `fb64d06`. `agent-contract` §2 keeps it out of this round and the memo's `## Not verified` assigns it to the sealer. **It has now come due**: this round leaves nothing open, so what comes next is the sealer's spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py:615`, `:676` | round 1's 1 — fixed |
| round-1 | PR #372 body, §*The class, enumerated by construction* | round 1's 2 — answered |
| round-1 | `seal/specs/1789211172-…/overview.md:10` | round 1's 3 — fixed |
| round-1 | `seal/follow-up.md:62`, `phases/phase-5.md` removal table | round 1's 4 — fixed |
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py:634`, `:717` | round 1's 5 — fixed |
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py:709` | round 1's 6 — fixed |
| round-1 | `tests/test_a_corrected_sentence_survives_elsewhere.py:574` | round 1's 7 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The exemption path — a `survivors.md` row still silences its own survivor through the diff | Already deferred by this work item: Q1 answered *out*, `plan.md` phase 4 closes `deferred #371`, and the `seal/follow-up.md` row now names #308 as its corpus half | the repository owner, on #371 with #308 |
| Whether any branch in flight now reports a survivor it did not report before | Already deferred: `overview.md` `## Not verified` | the first pull request into a release branch after this merges |
| Windows | Already deferred: `overview.md` `## Not verified` | CI, or whoever next runs the check on Windows |
| Finding 8 — a second unfiltered site in a declared scope, after the count is bumped | Not deferred by this round; recorded as ⬜ so the next reader does not re-find it. No ticket asked for | the repository owner, if it is ever worth a row |

## Verified by the orchestrating session, before the record was committed

The round's one open finding was re-measured here at `fb64d06`, module and test
file restored with `git checkout --` afterwards and `tests/__pycache__` cleared
first — the reviewer disclosed that a stale `.pyc` had given it one false red,
and this run was taken with the caches gone.

| What was re-taken | Result |
|---|---|
| a second **unfiltered** path list inside `corrected`, count left at `1` | **red** |
| the same, with `PATH_LIST_CALLS["corrected"]` raised to `2` | **green** — the gap |
| `:723`'s assertion and `_mentions` at `:671`, read | the count assertion compares integers; `_mentions` answers for the FUNCTION, so a scope whose first site is filtered reports `True` whatever the second does |

**Finding 8 is confirmed and deferred to #373**, not fixed. The reason is in the
fix table and it is about the shape of the remedy rather than about its size:
per-call-site detection of the predicate is a design step, and this round
reported `Needs a fix: no`.

The two mutations the reviewer was asked to take on trust from round 1 —
a second unfiltered list inside `corrected`, and one at module scope — were
re-taken by this session against the fixed case at `08fe497` and both went red,
with the module's own file at 47 passed and the tree clean.

Nothing else in the report was contradicted. The reviewer's own caveat about the
stale `.pyc` is recorded here rather than only in its report, because a false red
that a second run corrected is exactly the kind of thing a later reader needs to
know was looked at.

## What moved after the gate, and why the cell still holds

The gate was taken at `9a1246d`. Three commits follow it, and a reader is owed
the reason none of them re-opens it.

| Commit | What it changed | Why it cannot move what the gate measured |
|---|---|---|
| `5b09bf5` | this record's `Broad gate` cell, one line | the seal's own write — the cell cannot exist before the run that fills it |
| `6c11e9f` | two `## Not verified` rows in `overview.md`, marked ✅ | they record answers the gate and CI produced; no code, no test, no ledger row |
| this one | this section | the same |

**None of the three touches a Python file, a ledger anchor or a fixture**, so
the suite, `ruff`, `evidence-check` and `survivor-check` are all measuring the
same tree they measured at `9a1246d`. The one thing they do touch is prose the
document guards read, so those were re-run narrowly at `6c11e9f` rather than
assumed: `test_docs_line_wrap`, `test_the_set_a_work_item_always_has`,
`test_a_question_says_who_can_answer_it`, `test_no_real_identifiers`,
`test_one_word_one_meaning` and `test_a_row_points_by_content` — **162 passed**,
one command. `bin/unverified-check` on the memo: exit 0, 3 open, 3 closed.

**This is the narrow run a boundary owes, not a second broad one.** The rule the
repository states is that a broad run with an edit after it was spent rather
than banked; the answer to that is either a re-run or an argument, and the
argument has to name what the edit could have reached. It reached six document
guards, and they were run.

**CI at `5b09bf5` was green on all six checks** —
[run 34749466344](https://github.com/MichaelYcJo/SpecSeal/actions/runs/34749466344)
and [34749466057](https://github.com/MichaelYcJo/SpecSeal/actions/runs/34749466057):
lint, release, ledger, and `pytest` on ubuntu, macos and **windows** (7m10s).
The Windows leg is what closed the memo's platform row, which no run of mine
could have.
