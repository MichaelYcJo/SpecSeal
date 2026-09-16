# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — review round 3

The final verifying round. Target: `git diff 9919b265..HEAD`, HEAD at
`92ca63ec` on `fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for`,
working tree clean. HEAD has not moved from the SHA the prompt named. Pull
request #412, draft.

## How the findings hang together

Round 2 opened two findings and both are closed in the document. The first —
a case that read a whole section — is closed completely: the two mutations
round 2 ran are red now, and so are two more. The second is closed in the
document and half-closed in the pin, and that half is this round's first
finding.

```
round 2's 🟡 2 — the platform hedge was missing from the two cells
     ↓ fixed: the hedge is in both cells, and a new case pins it
🟡 1 — that case does not pin WHICH shell does which, so the two
       names can be swapped in either cell with all 18 cases green
```

The second finding is unrelated to the first and comes out of the record the
diff adds rather than the code:

```
round 2 reported a rendering defect in round-1.md as a ⬜ correction
     ↓ the fix pass repaired round-1.md's nine cells by hand at 9919b265
🟡 2 — the generator that produced them was never touched, so round-2.md,
       written afterwards at 92ca63ec, carries the same class in a new spelling
```

## Round 2's 🟡 1 is closed, and the helper has no wider slice one level up

`refusal_paragraph()` at
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:313` slices
from `**An absent row is a refusal, not a default.**` to the first blank line,
and asserts the opening exists before it slices. Three mutations executed:

- `#401` removed from that paragraph alone, leaving the section's second
  occurrence at `templates/config.md:81` of the section — **red**. This is the
  first of the two round 2 ran, and it left 17 cases green before the fix.
- The whole clause round 1 added deleted from the paragraph — **red**. The
  second of round 2's two.
- The paragraph's opening bold sentence removed — **red**, raised by the
  helper rather than passed on as an empty slice.

One level up, the helper cannot widen into a false green. The only other
`#401` under `## Broad gate` stands in the criterion's closing prose, three
paragraphs and a `###` heading away, and a blank-line bound cannot reach it.
A blank line inserted inside the paragraph shrinks the slice, which reddens
the case rather than greening it.

## Round 2's 🟡 2 is closed in the document, and the new case does not pin which shell is which

Both cells carry the hedge, and neither can lose it silently. Deleting the
`cmd.exe` sentence from `templates/config.md:206` is red, and deleting the
platform sentence from `:225` is red. The case reads each row from the table
that row is in, which is what round 2 asked for.

What it does not read is the attribution. Swapping the two shell names in
either cell leaves all 18 cases green:

| `templates/config.md:206`, as it stands | as the mutation writes it |
|---|---|
| `/bin/sh` backgrounds the whole line and answers 0 … `cmd.exe` separates two commands instead | `cmd.exe` backgrounds the whole line and answers 0 … `/bin/sh` separates two commands instead |

Both spellings satisfy the case, because it asserts that each row contains
`/bin/sh`, contains `cmd.exe`, and contains one consequence phrase — never
which name the phrase belongs to. The mutated document states the opposite of
the truth on the surface a person reads before writing the row, which is
exactly the defect round 2 opened 🟡 2 for, in a worse form.

This is the class rounds 1 and 2 have been closing in this module twice
already. Round 1's 🟡 6 was a reason paired with another form's reason, and
`named()`'s own docstring records a row found by its own prose. An assertion
that reads a row without reading what binds its two halves together is the
third instance (`agent-contract` §12).

`round-2.md:40` states the repair as *pins both cells, per cell, in the list
each cell is in*. Per cell and per list are true. Which shell does which is
not pinned, and the docstring's own claim — *Both cells now say what each
shell does* — is what nothing checks.

## And the record generator still writes the defect round 2 reported

`round-2.md:39` and `:40` read `fixed at 6233b769 — . ` — an em dash, a space,
a stray period. Round 2 reported this shape at `rounds/round-1.md` as a ⬜
correction and named the cause at `skills/code-review/scripts/round_record.py`.
The fix pass rewrote round-1.md's nine cells by hand at `9919b265`. Nothing on
this branch touched the generator, so the next record generated — round-2.md,
at `92ca63ec` — carries it again.

The cause is one character wide. `round_record.py:3115` cuts the commit's own
code span and strips `chain.SEPARATORS`, which is `" —–-:,"`. A comma after
the span strips clean and a period does not, and `round-2-fixes.md` writes a
period. Measured:

| The fix table's third cell | What the record gets today |
|---|---|
| `` `6233b769`. `refusal_paragraph()` bounds … `` | `fixed at <sha> — . ``refusal_paragraph()`` bounds …` |
| `` `6233b769`, `refusal_paragraph()` bounds … `` | `fixed at <sha> — ``refusal_paragraph()`` bounds …` |

The comment at `round_record.py:3105-3112` records the last pass through this
same class — #391 part 2, an empty code span left beside the commit on 210
committed rows — and says the widening was done there rather than in
`chain.SEPARATORS`, which five other readers share. The same place takes this
one. Widened locally, the generator's own 119 cases stay green.

Left alone, `round-3.md` gets it too: the closing commit's fix table is the
next cell this code reads.

## The three ⬜ corrections, the survivors, and the two lessons

**The nine survivor rows quote standing text.** Executed rather than read:
`survivor-check` with the work item's `survivors.md` passed as `--exempt`
exits 0 and excuses all nine. The quote is the exemption's anchor, so a quote
that did not match the standing text would come back reported rather than
excused. The truncated quote the fix pass described is repaired. Run without
`--exempt` the check exits 1 and prints the same nine, which is the flag's
behaviour and not a defect.

**The eighth ledger row's claim is true and its second coordinate carries no
part of it.** `skills/implement/orchestration.md` step 2 reads *Say in three
lines what you created, that its presence at that place is the opt-in, and
what each part of the root is for* — the claim verbatim, so the first
coordinate holds. The second,
`tests/test_first_setup_asks_once.py#test_a_repository_with_the_root_at_either_place_is_never_asked`,
asserts three strings inside the *Ask only here* paragraph and says nothing
about step 2. Nothing in `tests/` matches *three lines* or *what each part*,
so no case pins this claim at all. The `Checked` cell says **Read**, which is
honest; the Code grounds column says a case pins it, which is not. It is a
row under `seal/ledger/`, so it is a correction here rather than a numbered
finding.

**`spec.md:129` and `questions.md` are correct.** The allowed list now carries
the mid-line `&` with the `/bin/sh` hedge, consistent with
`templates/config.md:225` and with Q6's answer. `questions.md` reads Q1
through Q6 in order. One wobble in the new `spec.md` cell: it cites *round 2's
⬜ 3*, and round-2.md numbers none of its five ⬜ rows, so the reference is a
count somebody has to make by hand and it rots if a row moves. Naming the row's
subject would hold; leaving it costs a reader ten seconds.

**Both lessons in `overview.md` §*Fed back into the spec* are true.** Lesson 1
at `:99` is confirmed against the commits: `9a52268c` both repaired round 1's
🟡 7 in `tests/test_first_setup_asks_once.py` and planted the unbounded case
one module over, and round 2 measured 17 cases green under the deletion. The
class it names — *a case whose slice is wider than the thing it is named for*
— generalises, and this round's 🟡 1 is the same lesson one level further in.

Lesson 2 at `:109` is true and its headline clause is loose. *Not only where
the form is executed* describes one of the three places round 1's fix reached;
the other two, `overview.md` and the pull request body, are documents. The
paragraph's closing sentence carries the real distinction precisely — the
document a decision is made from is a different surface from the code that
acts on it — so this is a clause worth tightening, not a lesson worth
doubting.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a `Broad gate` row can ever carry a pipe, and whether `config_rows` should learn to unescape one | `questions.md` Q5, already deferred by the work item and routed to an issue. Nothing this round found changes its weighing | the repository owner |
| Whether the gate behaves on Windows as the two `&` cells now say | `overview.md` §*Not verified*, already deferred. 🟡 1 above is about the pin on those cells, not about the measurement | the repository owner, at the next `windows-latest` run |

## Paste-ready fixes

🟡 1 — appended inside `test_both_ampersand_cells_name_both_shells`, after the
existing `nothing is left running` assertion. The existing presence loop stays:
it carries the message for a cell that names no shell at all.

```python
    assert "`/bin/sh` backgrounds" in refused and "`cmd.exe` separates" in refused, (
        "the refused row does not say WHICH shell does which, so the two "
        "names could be swapped with this case green"
    )
    assert "That is `/bin/sh`" in legal and "`cmd.exe` sequences" in legal, (
        "the allowed row does not say WHICH shell does which"
    )
```

🟡 2 — `skills/code-review/scripts/round_record.py:3115`, one character. Widened
here and not in `chain.SEPARATORS`, for the reason the comment six lines above
already gives.

```python
            note = (third[:start] + third[end:]).strip(chain.SEPARATORS + ".")
```

⬜ — `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md:28`,
Code grounds cell. The test anchor comes out and the Notes say what no case
covers, so the next person re-verifying does not go looking for one.

```markdown
| The once-per-repo bootstrap says in three lines what it created, that the root's presence at that place is the opt-in, and what each part of the root is for | `skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's missing"@1da783ca` | **Read** 2026-09-15: step 2 of the Bootstrap carries all three, unchanged by this branch — what this branch changed is step 1, which now asks two questions in one `AskUserQuestion`. **No case pins this claim**, and the row says so rather than citing one that pins a neighbouring paragraph | 2026-09-15 | Replaces the second of the four claims S14 bound, which left `seal/ledger.md` with that row. Round 1 removed the row because its *and nothing else* went with the code and wrote one replacement; round 1's own review found the other three unreplaced, and round 2 confirmed it. The remaining two were correct to leave — they are about the mode question and the parity question, which rows 1885 and the parity rows already carry |
```

## What this round routes, since no round follows it

| Finding | Where it should go | Why |
|---|---|---|
| 🟡 1 | **the closing commit** | Four lines inside a case this branch wrote, measured red under both swaps. Leaving it ships a release about a check that could not fail carrying a case that cannot fail on the axis it is named for |
| 🟡 2 | **the closing commit**, or an issue if a generator change is out of the commit's reach | One character with 119 green cases behind it. The cheap alternative — write the next fix table's note without a leading period — fixes `round-3.md` and leaves the class standing, which is how this recurred once already |
| ⬜ eighth ledger row | **the closing commit** | A one-cell edit to a file this branch already writes, and `evidence-check` will keep the wrong coordinate green forever |
| ⬜ lesson 2's clause, ⬜ `spec.md`'s ⬜ 3 | **leave** | Neither changes what anyone does. Tighten them if the closing commit is open anyway |

Needs a fix: yes — 🟡 1, the ampersand case that cannot fail on attribution, and 🟡 2, the record generator's stray period.
Loses a record or crashes: no

## Proof

Opened in a `git clone --no-local` at `92ca63ec`:
`templates/config.md`,
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
`tests/test_first_setup_asks_once.py` (the one cited case),
`skills/implement/orchestration.md` §*Orchestrator: Bootstrap — create what's missing*,
`skills/code-review/scripts/round_record.py:3100-3125` and `:3685-3705`,
`skills/code-review/scripts/chain_check.py:497`,
`skills/code-review/scripts/survivor_check.py` (the exemption reader),
`bin/survivor-check`, `seal/config.md`, `CONTRIBUTING.md`,
and in the work item: `rounds/round-2.md`, `rounds/round-2-fixes.md`,
`survivors.md`, `overview.md`, `questions.md`, `spec.md`, `changelog.md`,
`seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`.

Not opened: `rounds/round-2-report.md`, `rounds/round-1.md`,
`seal/ledger.md` beyond the two rows the diff touches, and the pull request
body. The round-2 record and its fix table carried what the report would have,
and round-1.md is outside this round's range.
