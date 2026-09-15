# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — review round 3

| Field | Value |
|---|---|
| Target SHA | 92ca63ec |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 412 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1, the ampersand case that cannot fail on attribution, and 🟡 2, the record generator's stray period. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of the run. Round 1 met the floor and round 2 — a verifying
round that opened two findings — closed on a fix, so the one reopening is spent
and this record ends the run whatever it finds
(`docs/review-chain-spec.md` §*The reopening — one, and then the run is
capped*).

Its target is the diff of round 2's fixes, `9919b265..92ca63ec`, and its job is
the answers: are round 2's two verdicts actually closed. The two units that fix
pass added — `refusal_paragraph` and
`test_both_ampersand_cells_name_both_shells` — are exempt from that rule and
were read as a finding surface, because nobody had reviewed them.

The round was also asked to route rather than only to report, since no round
follows it: for each finding, the closing commit, an issue, or left alone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `test_both_ampersand_cells_name_both_shells` asserts that both shell names appear and never which one does which, so either cell can be inverted with every case green | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:221-234` | deferred #413 | Executed: the two names swapped in the refused row — 18 passed; swapped in the allowed row — 18 passed. The mutated document states one platform's semantics as the other's, which is round 2's 🟡 2 inverted. Third instance of round 1's 🟡 6 class in this module (`agent-contract` §12, §14). Paste-ready fix below measured green at HEAD and red under both swaps |
| 🟡 2 | The record generator leaves a stray period after the em dash, the class round 2 reported at round-1.md and the fix pass closed at the instance | `skills/code-review/scripts/round_record.py:3115`, rendered at `rounds/round-2.md:39` and `:40` | deferred #414 | Executed: the cut strips `chain.SEPARATORS`, which holds a comma and not a period, and `round-2-fixes.md` writes a period. round-1.md was repaired by hand at `9919b265`; the generator was untouched on this branch and round-2.md was written afterwards. The local widening at 3115 produces the right text and leaves the generator's own 119 cases green. `round-3.md` is the next cell it reads |
| 🟢 | Round 2's 🟡 1 — the paragraph case is bounded and the helper refuses a missing opening | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:313` | confirmed | Executed: both mutations round 2 ran are red, and the opening removed is red. No second `#401` is reachable inside a blank-line bound |
| 🟢 | Round 2's 🟡 2 — both `&` cells carry the platform grounds and neither can lose them silently | `templates/config.md:206` and `:225` | confirmed | Executed: the `cmd.exe` sentence deleted from the refused cell is red, the platform sentence deleted from the allowed cell is red. The attribution half is 🟡 1 above |
| 🟢 | `refusal_paragraph` has no wider slice one level up | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:313` | confirmed | Read and executed: the section's second `#401` is three paragraphs and a `###` heading away; a blank line inserted inside the paragraph shrinks the slice, which reddens rather than greens |
| 🟢 | All nine `survivors.md` rows for this fix range quote standing text | `survivors.md` §*Round 2's fix pass* | confirmed | Executed: `survivor-check` with the work item's file as `--exempt` exits 0 and excuses all nine. The quote is the anchor, so a stale one would report rather than excuse |
| 🟢 | `spec.md`'s allowed list and `questions.md`'s order are correct | `spec.md:129`, `questions.md` | confirmed | Read against `templates/config.md:225` and Q6's answer; the rows read Q1 through Q6. The cell's *round 2's ⬜ 3* is a positional reference into an unnumbered list — correct today, fragile |
| 🟢 | Both lessons in `overview.md` §*Fed back into the spec* are true | `overview.md:99` and `:109` | confirmed | Read against `9a52268c`, round-2.md and the commits: the fix pass that repaired 🟡 7 planted the unbounded case, and round 2 measured 17 green. Lesson 2's headline clause is the ⬜ below |
| ⬜ | The eighth ledger row cites a test case that asserts nothing about its claim | `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md:28` | correction | Executed: nothing in `tests/` matches *three lines* or *what each part*; the cited case asserts three strings in the *Ask only here* paragraph. The claim itself is verbatim in step 2 and the first coordinate holds; `evidence-check --strict` is exit 0, 1274 ok, 0 broken. Paperwork, so not counted in `Needs a fix` |
| ⬜ | Lesson 2's headline clause describes one of the three places round 1's fix reached | `overview.md:109` | correction | Read: `overview.md` and the pull request body are documents, not where the form is executed. The paragraph's closing sentence states the distinction precisely |
| ⬜ | `spec.md` cites *round 2's ⬜ 3* and round-2.md numbers none of its five ⬜ rows | `spec.md:129` | correction | Read: the reference is a count a reader makes by hand and it moves if a row moves |

## Paste-ready fixes

```python
    assert "`/bin/sh` backgrounds" in refused and "`cmd.exe` separates" in refused, (
        "the refused row does not say WHICH shell does which, so the two "
        "names could be swapped with this case green"
    )
    assert "That is `/bin/sh`" in legal and "`cmd.exe` sequences" in legal, (
        "the allowed row does not say WHICH shell does which"
    )
```
```python
            note = (third[:start] + third[end:]).strip(chain.SEPARATORS + ".")
```
```markdown
| The once-per-repo bootstrap says in three lines what it created, that the root's presence at that place is the opt-in, and what each part of the root is for | `skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's missing"@1da783ca` | **Read** 2026-09-15: step 2 of the Bootstrap carries all three, unchanged by this branch — what this branch changed is step 1, which now asks two questions in one `AskUserQuestion`. **No case pins this claim**, and the row says so rather than citing one that pins a neighbouring paragraph | 2026-09-15 | Replaces the second of the four claims S14 bound, which left `seal/ledger.md` with that row. Round 1 removed the row because its *and nothing else* went with the code and wrote one replacement; round 1's own review found the other three unreplaced, and round 2 confirmed it. The remaining two were correct to leave — they are about the mode question and the parity question, which rows 1885 and the parity rows already carry |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the target module at `92ca63ec`, in a `git clone --no-local` of the repository | exit 0, 18 passed |
| `bin/test` on the five modules that read the changed template and records | exit 0, 294 passed |
| `bin/test` on the repository-rule modules — real identifiers, line wrap, one word one meaning | exit 0, 40 passed |
| Nine mutations of `templates/config.md`, each restored from the original bytes before the next | red for both of round 2's, for the opening removed, and for either `cmd.exe` sentence deleted; green for either row's shells swapped and for the allowed row's consequence hollowed out |
| The two proposed assertions added to the case, then each swap re-run | green at HEAD, red under both swaps |
| `evidence-check --strict .` in the clone | exit 0 — 1274 ok, 0 drifted, 0 broken |
| `survivor-check --range 9919b265..HEAD --root .` with the work item's `survivors.md` as `--exempt` | exit 0 — 9 sentences removed, all nine excused |
| The same without `--exempt` | exit 1, all nine printed — the flag's behaviour, not a defect |
| `round_record.py`'s note cut, over a period, a comma and an em dash after the commit span | the period survives and the other two strip; the local widening fixes it |
| `bin/test tests/test_the_record_is_generated.py` with that widening applied | exit 0, 119 passed |
| `grep` over `tests/` for *three lines* and *what each part* | no match |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** `agent-contract` §2 makes it the sealer's one act; no round has run it and this round did not. It comes due when this round's findings are routed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py#not_as_written` | round 1's 1 — fixed |
| round-1 | `templates/config.md` §*What is refused, and what stays allowed*, the `a pipe` row | round 1's 2 — fixed |
| round-1 | `skills/implement/orchestration.md:145` | round 1's 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:13-17` | round 1's 4 — fixed |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` | round 1's 6 — fixed |
| round-1 | `tests/test_first_setup_asks_once.py:234` | round 1's 7 — fixed |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:210` | round 1's 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:248` | round 1's 9 — fixed |
| round-1 | `seal/ledger.md:1942` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:819` | round 1's ⬜ — correction |
| round-1 | `templates/config.md` §*Choosing a value — the criterion*, rule 3 | round 1's ⬜ — correction |
| round-1 | `skills/verify/scripts/broad_gate.py#gate` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | round 1's 🟢 — confirmed |
| round-2 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:275` | round 2's 🟡 1 — fixed |
| round-2 | `templates/config.md:206` and `:225` | round 2's 🟡 2 — fixed |
| round-2 | `templates/config.md:225`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:801` | round 2's 🟢 — fixed |
| round-2 | `templates/config.md:224`, `skills/implement/orchestration.md:152` | round 2's 🟢 — fixed |
| round-2 | `skills/implement/orchestration.md:144`, `skills/config/SKILL.md:63` | round 2's 🟢 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:12-20`, `templates/config.md:173` | round 2's 🟢 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:333-341`, `overview.md` §*Not verified* | round 2's 🟢 — fixed |
| round-2 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:66` and `:89` | round 2's 🟢 — fixed |
| round-2 | `tests/test_first_setup_asks_once.py:163`, `:230`, `:287` | round 2's 🟢 — fixed |
| round-2 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:349` | round 2's 🟢 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:251` and `:530`, `tests/test_one_word_one_meaning.py:184` | round 2's 🟢 — fixed |
| round-2 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:196` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` | round 2's 🟢 — confirmed |
| round-2 | pull request #412 | round 2's 🟢 — confirmed |
| round-2 | `rounds/round-1.md` | round 2's ⬜ — correction |
| round-2 | `rounds/` | round 2's ⬜ — correction |
| round-2 | `spec.md` §*What is refused, and what stays allowed* | round 2's ⬜ — correction |
| round-2 | `questions.md:21` | round 2's ⬜ — correction |
| round-2 | `seal/ledger.md:1885`, `:1942`, `:1943` | round 2's ⬜ — correction |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item and routed to an issue. Nothing this round found changes its weighing | the repository owner |
| Whether the gate behaves on Windows as the two `&` cells now say | `overview.md` §*Not verified*, already deferred. 🟡 1 above is about the pin on those cells, not about the measurement | the repository owner, at the next `windows-latest` run |
