# Round 3 — the verifying round after the reopening

Target: the diff of round 2's fixes, `cd7ea2f..bd08f52`, read in a
`git clone --no-local` of this repository at `50520de`. The run's one
reopening is spent, so nothing below is a fix to commission — every finding
this round opened is written as a `deferred #N` candidate with the issue it
would become.

**How the five findings relate.** Four of them are one shape: a repair that
closed its finding on the value it was shown and left the neighbouring value
of the same class open. That is the shape round 2 itself opened 🟡 13 for, and
it is worth saying that the fix pass then closed 🟡 13's class properly — the
two that stayed open are 🟡 11's and 🟡 12's.

```
🟡 11 fixed   the gate reads the WORD `sealed`      → A: nothing pins that word
                                                        to the line that prints it
🟡 12 fixed   seal refuses every value outside      → B: `round-N` is inside the
              the row's vocabulary                     vocabulary and still lies
🟡 13 fixed   the suite row reads the wall clock    → D: narrowed, not closed
🟡 14 fixed   `quote` takes the platform            → the `%VAR%` residual is
                                                        named honestly; C and E
                                                        are the two new units'
                                                        own diagnostics
```

## The four verdicts are closed, and each was turned red

Every one was re-derived by reverse-applying the fix commit against its source
file and running its case in the clone, never by reading the diff. Each revert
was taken from a clean tree.

- **🟡 11 · closed.** With `5a20202` reversed on
  `skills/verify/scripts/broad_gate.py`,
  `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` fails on
  `assert "the cell WAS written" in out.err` — the old message says *a
  `round-record:` line above is a refusal and no cell was written* while the
  stub's own stdout reads `round-record: sealed round-2.md …`. Its pair,
  `test_the_gate_with_record_prints_no_stamp_when_the_record_refuses`, stays
  green under the revert, which is correct: only one half of the pair binds
  the change, and the other exists to kill the mutation that reads the bare
  `round-record:` prefix.
- **🟡 12 · closed.** With `0cbd6ad` reversed on
  `skills/code-review/scripts/round_record.py`, all three parametrisations of
  `test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary` fail
  on `assert code == 2` with `assert 1 == 2`, and each failure prints
  `round-record: sealed …` followed by the post-write chain check refusing on
  that same row. `test_seal_refuses_while_the_fixes_have_been_read_by_nobody`
  fails beside them on `assert "read by no LATER round" in out`.
- **🟡 13 · closed.** The rebuild does not weaken the reds. With both
  `bd08f52` and `c0a139b` reversed — the pattern moved inside `suite_counts`
  and the module-level constant that preceded it, in that order —
  `test_the_suite_row_reads_pytests_counts_and_not_a_linters` fails on
  `assert '2 errors' == '1 passed'`. Read off the reverted unit directly, the
  second red binds too: `suite_counts("3 skipped in 0.10s\n")` returns `None`
  under the word list where `'3 skipped'` is asserted.
  <!-- NAME NOT IN TREE: the module-level constant this range removed, and the top-level name the first repair added, are named in the fix commits rather than here. -->
- **🟡 14 · closed.** With `67cdbda` reversed, all three parametrisations of
  `test_a_path_is_quoted_for_the_shell_of_either_platform` fail on
  `TypeError: quote() got an unexpected keyword argument 'windows'`. The
  signature is the assertion, which is the point the fix pass made.

## A · Nothing ties the gate's discriminator to the line that prints it

`skills/verify/scripts/broad_gate.py:620` decides whether the cell was written
by reading `line.startswith("round-record: sealed")`. The line it reads is
printed at `skills/code-review/scripts/round_record.py:3066`, in a different
package, and no case connects the two.

I changed that print from `round-record: sealed …` to `round-record: wrote …`
and ran the three modules: **130 passed, exit 0**. Nothing went red. With that
mutation in the tree, a `seal` that writes the cell and then fails its own
chain check makes the gate tell the reader *the `round-record:` line above is
a refusal raised before the write, and no cell was written* — the exact
misdirection 🟡 11 was opened for, restored by an edit in the other file.

The reason the mutation survives is visible at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:1243`: the only case that
drives the discriminator stubs `seal_record` and hands it a hardcoded
`"round-record: sealed round-2.md — …"` string. Both ends of the coupling are
literals, and the case supplies one of them itself.

The ledger records the fact as verified —
`seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md`
row S12 says the gate *tells the two apart by the word `sealed`* — and its
three anchors are all on `broad_gate.py` and its case. The line that produces
the word is not among them.

- **The issue it would become** — *the gate's `sealed` discriminator has no
  case tying it to the line `round_record.py seal` prints*. Either a shared
  constant both modules import, or a case that runs the real subcommand to a
  successful write and asserts the gate's reading of its output.

## B · `round-N` is inside the vocabulary, and every reachable one is a lie

🟡 12 replaced *refuse `nobody`* with *refuse everything that is neither a
later round nor `no fixes to check`*, at
`skills/code-review/scripts/round_record.py:3022`. The predicate is
`chain.CHECKER_RE.match(plain)`, and `CHECKER_RE` is `^round-\d+(?:\.md)?$` —
a shape, not a round.

`seal` reads the highest-numbered record on disk, so on that record no
`round-N` value can name a later round. Every value that matches therefore
names either this round or one git does not carry. All four I drove reach the
write:

| Cell | Exit | Cell written | What the post-write chain check then said |
|---|---|---|---|
| `round-1` | 1 | yes | `names round-1, which is this round or one that ran before these fixes existed` |
| `round-9` | 1 | yes | `git carries no such record in this work item` |
| `round-2.md` | 1 | yes | `git carries no such record in this work item` |
| `ROUND-1` | 1 | yes | `names round-1, which is this round …` |

Each printed `round-record: sealed …` first. That is the state the fix's own
comment names as the thing it is preventing — *a cell written there is a cell
standing on a record its own check will not accept* — reached through the one
value the predicate lets past.

`test_the_refusal_names_the_three_values_the_row_holds` argues this is
deliberate, on the grounds that hard-coding *only `no fixes to check`* would
move `chain_check.checked_by`'s conclusion into a subcommand that should not
derive it. The argument is sound about where the knowledge lives and does not
answer the write: the same `chain_check` module is already imported here for
`CHECKER_RE`, `NO_FIXES` and `field`, so asking it which rounds git carries is
not a new dependency.

Reachability is the honest caveat. `close` writes `nobody — <why>` and `new`
writes the later round's name onto the earlier record, so a last record
carrying `round-N` comes from a hand edit or a bug — which is exactly what
`the smith` and `pending` are, and 🟡 12 was opened for those.

- **The issue it would become** — *`seal` accepts any `round-N` shaped
  checker, including this round and one git does not carry*.

## C · The sweep's new guard misreads an absent span as a last section

`tests/test_one_word_one_meaning.py:268` asserts that the excluded span is not
the file's last `##`, which closes a real silent drop: the old
`partition(" ## ")[2]` returned `""` there and removed everything from the
heading to the end of the file from the sweep.

The same `partition` returns `""` for a second state — the span is not in the
file at all — and the assert cannot tell them apart. I pointed the first
exclusion at a heading `skills/verify/SKILL.md` does not carry and ran the
case. The message:

> `skills/verify/SKILL.md: the excluded span '## A heading this file does not carry' is the last '##' in the file, so this exclusion now removes everything after it from the sweep`

The span is not the last heading; it is not there. A reader sent to the end of
that file looks for something that is not the problem. The state is reachable
the ordinary way — someone renames the heading the exclusion names.

- **The issue it would become** — *the sweep's exclusion guard reports an
  absent span as a last-`##` span*. `assert span in text` before the
  partition separates the two.

## D · The suite row's new axis narrows the class rather than closing it

`skills/verify/scripts/broad_gate.py:429` now requires a wall clock after the
counts, which is the right axis and holds for every shape I drove:

| Input | `suite_counts` |
|---|---|
| `1 passed in 1s` + `Found 2 errors.` | `1 passed` |
| `3 skipped in 0.10s` | `3 skipped` |
| `768 passed, 1 skipped in 30s` + `warning: 2 warnings emitted` | `768 passed, 1 skipped` |
| `2 warnings emitted` | `None` |
| `Found 2 errors in 1 file (checked 30 source files)` | `None` |
| `1 passed in 1s` + `something took 2 errors in 3s` | **`2 errors`** |

The last row is the residual: a line standing after pytest's summary that
carries counts *and* a clock still displaces it. No tool this repository's row
runs prints that shape, which is why this is a low candidate and not a fix.

The half worth more attention is what the skipped case now reveals rather than
hides. `3 skipped in 0.10s` used to render `suite  exit 0`; it now renders `3
skipped`, and the gate still seals. The panel stopped lying, and nothing
refuses a broad run in which no test executed.

- **The issue it would become** — *the broad gate seals over a suite in which
  nothing ran*. This is the altitude question of the three, and it belongs to
  the gate rather than to `suite_counts`.

## E · The refusal names a value it will refuse

`skills/code-review/scripts/round_record.py:3026` tells the reader *the row
holds one of three values: `round-N`, `no fixes to check`, or `nobody — <why>`*
and then refuses `nobody — <why>` on the next attempt. The sentence is true of
the row and false of this subcommand, and the two readings sit one line apart.
The instruction that follows — *spawn the verifying round first* — is the
right action, so a reader who reads to the end is not stuck; one who acts on
the list is.

- **The issue it would become** — *`seal`'s vocabulary refusal lists a value
  it refuses*. Naming which of the three `seal` accepts costs a clause.

## The three new units, judged as code

**`SCALE_NOT_A_NUMBER` (`skills/verify/scripts/seal_stamp.py:154`) is
correct.** The branch order in `check_scale` now reads NaN first, then
`scale < SCALE_FLOOR`, then the ceiling, and the old `not scale > CEILING`
that sent NaN down the below-the-floor arm is gone. I drove the four states
the band excludes: `nan` gets the not-a-number sentence, `-inf` the floor
sentence, `inf` the ceiling sentence, and `0.5` / `1.5` their own. The case
pins both halves of the message — that it says `is not a number` and that it
does not say `under the floor` — which is the §14 shape.

**`SEAL_EXCLUDED` (`tests/test_one_word_one_meaning.py:181`) carries both of
the units it replaced, and one thing more.** The pair it folds keeps its
file and its span each, so neither exclusion widened to a whole file. The
rewrite also stopped dropping the `" ## "` separator: the old form joined
`head` to the text after the marker directly and could glue the last word of
one to the first word of the other, and the new `head + marker + after` cannot.
The added guard is the third thing, and finding C is its diagnostic and not
its logic.

**`set_checked_by` (`tests/test_the_seal_is_taken_once_by_the_sealer.py:1084`)
is right and is one caller short.** It returns `path.read_bytes()`, which is
what the module's own `read_bytes` does, so the `before` it hands back
compares cleanly. `test_seal_refuses_while_the_fixes_have_been_read_by_nobody`
one function above still reads its record without it, which is fine because
that case does not rewrite the cell. Nothing else in the module duplicates it.

## 🟡 14's residual — naming it is the right treatment

`cmd.exe` expands `%VAR%` inside double quotes, and I confirmed the unit does
what its docstring says: `quote("tests/test_%PATH%.py", windows=True)` returns
`"tests/test_%PATH%.py"`, percent signs intact and live. The docstring calls
it named rather than closed, and that is the correct call for this unit —
quoting cannot close it, because the expansion happens after quoting is read.

What closes it is one level up. `compare_at_base` builds
`skills/verify/scripts/broad_gate.py:389` as a string and runs it with
`shell=True`, which is why `quote` exists at all; a command that never reaches
a shell has no metacharacters to escape and no variables to expand. The row's
command is a shell string from `config.md` and `first_command` splits it at
`&&`, so this is not a small change — which is why it is a candidate for its
own issue rather than a finding against `quote`.

The ledger already carries the residual as row S15's second tidy-up, labelled
read rather than executed, and there is no Windows machine in this round
either. That labelling is honest. What it does not have is an owner.

## Corrections, in the records

None of these is a defect in the branch's code.

1. **`rounds/round-2.md` §Paste-ready fixes carries a superseded block for
   🟡 13.** Its verdict row names `bd08f52`, which moved the clock pattern
   inside `suite_counts`; the block above shows the module-level form that
   commit removed. A reader comparing the record to the code finds a name the
   tree does not carry, and nothing in the record says the block was
   superseded. `rounds/round-2-fixes.md` row 13 does not say it either — the
   trail is in `bd08f52`'s message and in `survivors.md`.
2. **`rounds/round-2.md`'s 🟡 12 block shows `plain.removesuffix(".md")`, and
   the shipped predicate has no `removesuffix`.** Harmless: `CHECKER_RE`
   already accepts the `.md` suffix, so the two agree on every input. It is
   named because the record's block is read as the fix that landed.
3. **The handoff's suite number does not match what the module list produces.**
   The round was handed *three modules → 78 passed*. The three modules
   `rounds/round-2.md`'s probe row names give **130 passed in 25.33s** at the
   fix head — 123 at `a46e642` plus the seven cases round 2's fixes added.
   Either a different trio was run or the number is wrong; I could not tell
   which from the prose, which is what §5 asks me to say rather than assume.
4. **`rounds/round-3-asked.md` names a unit the tree does not carry, and the
   evidence checker refuses it.** `evidence-check .` in the clone reports
   `NOT-IN-TREE  …/rounds/round-3-asked.md:1  SUMMARY_TAIL`.
   <!-- NAME NOT IN TREE: SUMMARY_TAIL is the top-level name bd08f52 removed, quoted here because the asked paragraph quotes it. -->
   The name is correct as history — it is what the first repair added and what
   `bd08f52` took back out — so the fix is the marker, not the sentence.
   `round_record.py new` copies that paragraph into `round-3.md` verbatim, so
   without the marker the record ships carrying the one refusal in an
   otherwise clean 1,103.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 11 | the gate tells the reader no cell was written, under a line saying `sealed` | `skills/verify/scripts/broad_gate.py:620` | answered | executed — `5a20202` reverse-applied to the source file alone; `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` red on `assert "the cell WAS written" in out.err`. Closed. Its pair stays green under the revert, correctly. The unpinned coupling is A below |
| 🟡 12 | a `Fixes checked by` nobody can read reaches the write | `skills/code-review/scripts/round_record.py:3022` | answered | executed — `0cbd6ad` reverse-applied; all three parametrisations of `test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary` red on `assert 1 == 2`, each printing `round-record: sealed …` and then the chain check refusing that row. Closed for values outside the shape; the shape itself is B below |
| 🟡 13 | a linter's error count still lands on the suite row, and an all-skipped run reports `exit 0` | `skills/verify/scripts/broad_gate.py:429` | answered | executed — `bd08f52` then `c0a139b` reverse-applied; `test_the_suite_row_reads_pytests_counts_and_not_a_linters` red on `assert '2 errors' == '1 passed'`, and the reverted unit returns `None` for `3 skipped in 0.10s` where `'3 skipped'` is asserted. The rebuild inside the function did not cost either red |
| 🟡 14 | `quote` has no case behind either branch, and the Windows branch does not quote for `cmd.exe` | `skills/verify/scripts/broad_gate.py:317` | answered | executed — `67cdbda` reverse-applied; all three parametrisations of `test_a_path_is_quoted_for_the_shell_of_either_platform` red on `TypeError: quote() got an unexpected keyword argument 'windows'`. The `%VAR%` residual is named rather than closed, and naming it is right for this unit — the close is `shell=True` one level up, which is D's neighbour and its own issue |
| 🟡 15 | the gate's `sealed` discriminator is a literal whose other end is a `print` in another package, and nothing pins them | `skills/verify/scripts/broad_gate.py:620`, `skills/code-review/scripts/round_record.py:3066` | open | executed — the print changed from `sealed` to `wrote`; three modules 130 passed, exit 0, nothing red. With that in the tree the gate tells a reader `no cell was written` on the ending 🟡 11 exists for. The only case driving the discriminator stubs `seal_record` and supplies the literal itself (`tests/…:1243`), and ledger row S12 anchors only `broad_gate.py` |
| 🟡 16 | `seal` accepts any `round-N` shaped checker, and on a last record every one of them is a lie | `skills/code-review/scripts/round_record.py:3022` | open | executed — `round-1`, `round-9`, `round-2.md` and `ROUND-1` each exit 1 with the cell written and `round-record: sealed …` printed, the post-write chain check then refusing on that same row. Same class as 🟡 12, one value over |
| ⬜ 17 | the sweep's exclusion guard reports an absent span as a last-`##` span | `tests/test_one_word_one_meaning.py:268` | open | executed — the exclusion pointed at a heading `skills/verify/SKILL.md` does not carry; the assert fires with *is the last `##` in the file*. `partition` returns `""` for both states and the guard reads only one of them |
| ⬜ 18 | the suite row's clock axis narrows the class rather than closing it, and an all-skipped run still seals | `skills/verify/scripts/broad_gate.py:429` | open | executed — `suite_counts("1 passed in 1s\nsomething took 2 errors in 3s\n")` is `'2 errors'`; no tool in this repository's row prints that shape. The second half is read: `3 skipped` now renders truthfully and nothing refuses the seal over it |
| ⬜ 19 | the vocabulary refusal names `nobody — <why>` as a permitted value and then refuses it | `skills/code-review/scripts/round_record.py:3026` | open | read — the sentence is true of the row and false of this subcommand. The instruction that follows is correct, so a reader who finishes the message is not stuck |
| ⬜ 20 | `rounds/round-2.md` carries the superseded module-level block for 🟡 13 beside a verdict row naming `bd08f52` | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2.md` §Paste-ready fixes | open | read — correction, out of `Needs a fix`. The trail is in `bd08f52`'s message and `survivors.md`, not in the record |
| ⬜ 21 | `rounds/round-2.md`'s 🟡 12 block shows a `removesuffix` the shipped predicate does not have | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2.md` §Paste-ready fixes | open | read — correction, harmless: `CHECKER_RE` accepts the `.md` suffix, so the two agree on every input |
| ⬜ 22 | the handoff's `three modules → 78 passed` does not match the module list the record names | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-3-asked.md` | open | executed — the three modules `round-2.md`'s probe row names give 130 passed in 25.33s at the fix head, which is 123 at `a46e642` plus round 2's seven new cases |
| ⬜ 23 | `rounds/round-3-asked.md:1` names a unit the tree does not carry, without the marker that exempts the line | `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-3-asked.md:1` | open | executed — `evidence-check .` in the clone at `50520de` reports `1103 ok · 0 drifted · 0 broken` and one `NOT-IN-TREE` refusal, on that line. `round_record.py new` copies the paragraph into `round-3.md` verbatim, so the record inherits it. Correction, out of `Needs a fix` |
| 🟢 24 | `SCALE_NOT_A_NUMBER` and the branch order in `check_scale` | `skills/verify/scripts/seal_stamp.py:154` | answered | executed — `nan` gets the not-a-number sentence, `-inf` the floor sentence, `inf` the ceiling sentence, `0.5` and `1.5` their own. The case pins the message it says and the message it must not say |
| 🟢 25 | `SEAL_EXCLUDED` carries both units it replaced | `tests/test_one_word_one_meaning.py:181` | answered | read — each exclusion keeps its own file and span, so neither widened to a file; the rewrite also stops dropping the `" ## "` separator, which the old form could use to glue two words into a phrase. C is its diagnostic, not its logic |
| 🟢 26 | `set_checked_by` | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1084` | answered | read — it returns what the module's own `read_bytes` returns, so the `before` it hands back compares cleanly, and nothing else in the module duplicates it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_one_word_one_meaning.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` at `50520de` | 130 passed in 25.33s |
| `5a20202` reverse-applied to `skills/verify/scripts/broad_gate.py` alone, then its two cases | `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` red on `assert "the cell WAS written" in out.err`; `test_the_gate_with_record_prints_no_stamp_when_the_record_refuses` green |
| `0cbd6ad` reverse-applied to `skills/code-review/scripts/round_record.py` alone, then its cases | four red — three parametrisations on `assert 1 == 2` with `round-record: sealed …` in the output, and `test_seal_refuses_while_the_fixes_have_been_read_by_nobody` on `assert "read by no LATER round" in out` |
| `bd08f52` then `c0a139b` reverse-applied, then `test_the_suite_row_reads_pytests_counts_and_not_a_linters` | red on `assert '2 errors' == '1 passed'` |
| `suite_counts` read off the reverted unit for `3 skipped in 0.10s` | `None`, where `'3 skipped'` is asserted — the second red binds |
| `67cdbda` reverse-applied, then `test_a_path_is_quoted_for_the_shell_of_either_platform` | three red on `TypeError: quote() got an unexpected keyword argument 'windows'` |
| `round_record.py`'s write line changed from `round-record: sealed` to `round-record: wrote`, then the three modules | 130 passed, exit 0 — nothing red, and the gate's message flips to `no cell was written` on a written cell |
| `round_record.py seal` on a fixed-but-unread record with `Fixes checked by` set to `round-1`, `round-9`, `round-2.md`, `ROUND-1` | exit 1 on all four, cell written on all four, `round-record: sealed …` printed on all four, the post-write chain check refusing that row on all four |
| `suite_counts` over six shapes at the fix head | `'1 passed'`, `'3 skipped'`, `'768 passed, 1 skipped'`, `None`, `None`, and `'2 errors'` for a clock-carrying line after pytest's summary |
| `quote` over `tests/test_%PATH%.py`, `tests/a%b.py` under `windows=True` | percent signs returned live inside the double quotes, as the docstring says |
| the sweep's first exclusion pointed at a heading `skills/verify/SKILL.md` does not carry | the guard fires with *the excluded span … is the last `##` in the file* |
| `check_scale` over `nan`, `-inf`, `inf`, `0.5`, `1.5` | the not-a-number sentence, the floor sentence, the ceiling sentence, and the floor and ceiling sentences |
| `python3 skills/evidence-check/scripts/evidence_check.py .` in the clone at `50520de` | `total: 1103 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, and one `NOT-IN-TREE` refusal on `rounds/round-3-asked.md:1` |
| `bin/test tests/test_no_real_identifiers.py -q` with this report copied into the clone at its own path | 2 passed |

One `test_tmp_*` probe file carried the last five rows. It was run once and
deleted, and the clone's tree is clean.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 15 — the gate's `sealed` discriminator has no case tying it to the line `round_record.py seal` prints | `deferred #N` candidate, a new issue | the sealer, at the release — the run's one reopening is spent |
| 🟡 16 — `seal` accepts any `round-N` shaped checker, including this round and one git does not carry | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ 17 — the sweep's exclusion guard reports an absent span as a last-`##` span | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ 18 — the broad gate seals over a suite in which nothing ran, and the clock axis leaves one displacing shape | `deferred #N` candidate, a new issue | the sealer, at the release |
| ⬜ 19 — `seal`'s vocabulary refusal lists a value it refuses | `deferred #N` candidate, a new issue | the sealer, at the release |
| the `%VAR%` residual in `quote`, closed only by removing `shell=True` from `compare_at_base` | ledger row S15's second tidy-up, labelled read | unowned — a candidate for the same issue as D |
| ⬜ F, ⬜ 21 — corrections in `rounds/round-2.md` | the record, not the tool | the orchestrator |
| ⬜ 22 — the handoff's suite count | this report | the orchestrator |
| ⬜ 23 — the missing marker in `rounds/round-3-asked.md` | the paragraph, before `round_record.py new` copies it | the orchestrator |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `skills/verify/scripts/broad_gate.py:570-583` | 🟡 11 — carried, re-derived, closed; now A |
| round-2 | `skills/code-review/scripts/round_record.py:3000-3010` | 🟡 12 — carried, re-derived, closed; now B |
| round-2 | `skills/verify/scripts/broad_gate.py:386-395` | 🟡 13 — carried, re-derived, closed; now D |
| round-2 | `skills/verify/scripts/broad_gate.py:313-322` | 🟡 14 — carried, re-derived, closed |
| round-1 | the ten rows of `rounds/round-1.md` | carried as coordinates only; round 2 answered every one and this round did not re-open them |

## The broad gate

`not yet`. Nothing in this report needs a fix, so the broad run is the next
step — the sealer's, once, at the tree as it then stands. §2 kept the full
suite, the repository-wide lint and the typecheck out of this round, and the
prompt did not ask for any of them.

## What was left unverified

- **The `cmd.exe` half of 🟡 14 and the `%VAR%` residual are read, not
  executed.** There is no Windows machine in this round, as there was none in
  round 2. Answered by CI's `windows-latest` leg, which runs `compare_at_base`
  on every push.
- **`survivor-check` over both ranges, and ruff**, reached me as prose from
  the orchestrator and I did not re-run them. Labelled read; answered by the
  orchestrator, who executed them at the fix head. `evidence-check .` I did
  run, because it is what reads this report's own prose, and it agrees with
  the handoff at 1,103 — with the one refusal correction I names.
- **The full suite** was not run. Answered by the sealer.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Read, in a `git clone --no-local` of this repository at `50520de`:

- `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2.md`
- `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-2-fixes.md`
- `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/rounds/round-3-asked.md`
- `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/survivors.md`
- `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md`
- `skills/verify/scripts/broad_gate.py`
- `skills/verify/scripts/seal_stamp.py`
- `skills/code-review/scripts/round_record.py`
- `skills/code-review/scripts/chain_check.py`
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`
- `tests/test_one_word_one_meaning.py`
- `tests/conftest.py`
- `bin/test`, `.github/scripts/run_tests.py`
- `git diff cd7ea2f..bd08f52`, and each of the six commits in it
