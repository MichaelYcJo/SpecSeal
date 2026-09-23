# Round 3 report — the verifying round at round 2's fix, and the round that ends the run

Target SHA `8b04523a831b9268f1ff39c980b5f64137a6e285`, on
`fix/503-the-report-the-record-and-the-cells-disagree-on-one-format`, against
the base `0b8dc4b2`. The surface this round opened is the fix range
`43afbc1e..db292bfb` (two commits) and the two record commits `e101abac` and
`8b04523a`; the branch beyond that surface is rounds 1 and 2's, and their 🟢
rows are carried except where the fix range touched what they cover. Work
was done in a `git clone --no-local` of the worktree at the target SHA; the
worktree was read and never written, except for this file.

Every claim below is labelled. **executed** means I ran the command in the
clone and read its output, exit codes read directly; **read** means I opened
the coordinate and it says what is stated; **unverified** names who answers.

## Summary

Round 2's 🟡 1 is closed as the record says. `same_run` decides the replace
on the commit AND the base, `kept_broad_gate` drops the newest entry only
when `same_run` says the flag records it, the same-commit-other-base case is
red under the SHA-alone rule the fix replaced and green at the target, the
reshaped same-base case still pins the replace, and the template sentence and
A9 say what the code does. ⬜ 2's new stands phrase is absent at the base and
present once at the target; ⬜ 3's docstring is true of both callers; the two
paperwork corrections state what `GATE_CARRIERS` pins. The three mutations
reproduce, and a fourth I added (the verify skill's new line removed) turns
⬜ 2's pin red. The fix range touched six files and nothing the findings did
not name, with one bookkeeping exception below.

Nothing needs a fix, so the run ends here and the sealer's spawn is due.
What this round opened is prose beside behaviour that is right: the HTML
comment `new_broad_gate_file` writes into every `broad-gate.md` still
promises that a run taken again leaves the earlier one behind it, and the
docstring and A9 now say the count of entries is the count of runs, where a
same-run re-seal is two runs and one entry. Both go to one ticket, together
with the pin round 2 asked for over that comment and nobody planted. One
`seal/ledger.md` row was re-hashed by the fix pass without a re-read note,
which is a correction and not a defect.

## The implementer's account, checked

- *The another-base case red at `43afbc1e` (`'e70fa1e against origin/base'
  == 'e70fa1e agai... against base'`), then green.* **Executed** one step
  over: mutation m1 below restores the SHA-alone rule that stood at
  `43afbc1e` (the `elif x != y` arm of `same_run` disabled, so only SHA-shaped
  words are compared) and
  `test_a_re_seal_at_the_same_commit_against_another_base_keeps_both` fails
  with the cell reading `f302329 against origin/base` alone — the first base
  erased, the shape the hand-back quotes. Unmutated, the seven `re_seal or
  another_base` cases pass. **Read**: `git show 43afbc1e` of
  `kept_broad_gate` compares `newest[0]` and `new[0]` by prefix and nothing
  else, which is the rule m1 restores.
- *Three mutations each red.* **Executed**: m1, m2 and m3 in §Executed
  probes, each red at the case named, each restored with `git checkout --`,
  and the clone clean afterwards.
- *Modules 129 + 142 + 7 passed; ruff on three files, one B905 fixed with
  `strict=True`.* **Executed**: the three modules in the clone (row below);
  `uvx ruff check` and `uvx ruff format --check` over the three edited `.py`
  files, exit 0 and exit 0. **Read**: `zip(a, b, strict=True)` at
  `round_record.py:394` follows a `len(a) != len(b)` guard at `:392`, so the
  strict flag can never raise; the floor `.github/scripts/run_tests.py`
  holds is Python 3.12 and `ruff.toml` targets the same, so the keyword is
  within the floor.
- *`evidence-check --reverify` 7 rows, then `--strict` exit 0 (1624 ok).*
  **Executed**: `evidence_check.py --strict .` in the clone, exit 0, `1624 ok
  · 0 drifted · 0 broken`. **Read** over the fix range's diff: the seven
  moved hashes are A9's `kept_broad_gate`, the reshaped case, the new case
  and `same_run` (four), A11's `GATE_CARRIERS` (one), and the two
  `seal/ledger.md` rows anchored on `templates/sdd-round.md`'s field table
  (two) — the table moved because the `Broad gate` row's comment changed.
- *CI-form sweep exit 0, one excused.* **Read**: the fix range removes no
  sentence from a scanned document — its document edits are the template
  row's clause and the fragment's rows — so the sweep round 1 executed reads
  nothing new. Not re-run.
- *`close` derived `same_run` and the new case at depth 1.* **Read**:
  `round-2.md`'s `New units` row names the two, and the fix range's diff adds
  exactly those two units.
- *The broad gate.* Labelled `unverified` by the hand-back and by both
  earlier rounds; the sealer's, and `not yet` below.

## Round 2's findings, each answered

**🟡 1 — verified.** **Read**: `same_run` at `round_record.py:386-402`
splits both texts on whitespace, refuses on a different word count, compares
a pair of SHA-shaped words by prefix in either direction and every other pair
exactly, so `abc1234 against base` and `abc1234 against origin/base` are two
runs and `abc1234 against base` and `abc1234567 against base` are one.
`kept_broad_gate` at `:380-381` drops `entries[0]` only when
`same_run(entries[0], value)`; the keep at `:382-384` is unchanged from round
2. `templates/sdd-round.md:39` says *a run the newest entry already records —
the same commit against the same base — replaces that entry rather than
duplicating it, while a run at that commit against another base is kept
behind the new entry as any earlier run is*; A9 in the fragment at `:20` says
the same and anchors on `same_run` and both cases. **Executed**: m1 (the
SHA-alone rule) turns the another-base case red alone; m2 (the replace
dropped) turns the same-base case red alone — the cell reads
`cceb665 against base; earlier run: cceb665 against base; earlier run:
2666969 against base`, the duplicate the case forbids; m3 (`same_run` true
unconditionally) turns four re-seal cases red, the direct home's among them,
so both homes take the rule through the one path.

**⬜ 2 — verified.** **Executed**: `git show 0b8dc4b2:skills/verify/SKILL.md`
carries `; earlier run: <sha> vs base <sha>` zero times and the target once
(`skills/verify/SKILL.md:456`); the bare `earlier run` stands once at the
base and twice at the target, the base's one being `:783`'s *Output quoted
from an earlier run*. m4 removes the bracketed clause from `:456` and
`test_every_carrier_says_the_cell_holds_one_entry_per_run` fails naming that
carrier; the other two cases pass. **Read**: the tuple at
`tests/test_the_broad_gate_cell_keeps_every_run.py:57-61` with its comment
naming the reason.

**⬜ 3 — verified.** **Read**: the docstring's last sentence at
`round_record.py:371-375` says `seal` has refused a flag that does not
resolve and `close --broad-gate` never resolves its flag. `seal` refuses a
flag with no SHA-shaped word at `:4484-4489` and one whose first SHA
`resolves_to` nothing at `:4490-4493`; over `close`'s body (`:3824-4182`) the
only `resolves_to` call is the fix table's commit column, and `SHA_RE` is not
consulted, so the flag is written as typed at `:3956-3960`.

**The paperwork row — confirmed.** **Read**: A11 at the fragment's `:22`
says *the eight documents … pinned as gone/stands pairs* and names the
`broad-gate.md` comment as the ninth carrier no test pins; round 1's 🟡 2
grounds at `rounds/round-1.md:36`, rewritten at `e101abac`, says *pins the
eight rewritten documents as gone/stands pairs* and names the same comment
as unpinned. `GATE_CARRIERS` has eight tuples. The two cells each use *the
ninth carrier* for a different thing — the grounds cell for `agents/warden.md`
§Role in the order the carriers were found, A11 for the comment in the count
of what is pinned — and each is true in its own count; noted, not a finding.

**The fix range's surface.** **Read** over `git diff --stat 43afbc1e..db292bfb`:
six files. `round_record.py` (the helper, the replace, the docstring), the
seal module (the reshaped case and the new one), the carrier module (the
tuple), the template (the clause), the fragment (A9 and A11) and
`seal/ledger.md` (two anchors on the template's field table). Every hunk maps
to 🟡 1, ⬜ 2, ⬜ 3 or the paperwork row, except that the second
`seal/ledger.md` row's move is a hash and nothing else — the correction
below. **Executed**: `git rev-list --count` over the range is 2, as the
record's `Fix range` row states.

**The new units as code.** `same_run` is correct for the cell's shape.
**Read**: one edge is worth a sentence and not a finding — a SHA-shaped word
glued to punctuation (`abc1234,`) fails `fullmatch` and is compared exactly,
so an abbreviated entry and a full flag in that shape would be two entries
rather than one; that is a duplicate, never an erasure, and neither writer
produces the shape. The new case asserts the cell's whole text, so it pins
the order as well as the keep.

**Rounds 1 and 2's 🟢 rows.** Confirmed. The fix range touched
`kept_broad_gate`, which round 2's phase-4 and one-path rows rest on, and
those were re-derived by the seal and close modules and by m1–m3; the carrier
module re-derives round 2's ⬜ 2 row. The rest cover code the fix range did
not touch.

## Findings

### ⬜ 1 · The `broad-gate.md` comment and the count sentence still describe the cell as it was before `same_run`

`skills/code-review/scripts/round_record.py:4278-4280`, the HTML comment
`new_broad_gate_file` writes into every `broad-gate.md`: *One entry per run,
newest first: a run taken again is written in front, and the earlier one
stays behind it as `earlier run`*. A run taken again over an unchanged
checkout — the sealer re-run, the plainest reading of *taken again* — now
replaces its entry, and only a run against another base stays behind. Round
2 named this comment as one of the four carriers of *a second run never
erases the first* and asked for a case over it in its regression table; the
fix range touched neither. **Executed**: `grep -rn "stays behind it\|a run
taken again\|earlier one stays" tests/` hits one docstring in the seal
module and nothing that reads the written file.

The same commit rewrote the count sentence the other way. The docstring at
`:363-365` says *two entries for one claim would make the count of entries
stop being the count of runs*, and A9 (fragment `:20`) ends *so a second run
never erases the first and the count of entries is the count of runs*. A
same-run re-seal is two runs and one entry, so the count is of distinct
comparisons — commit and base — which is what the previous text's *runs at
distinct commits* said one field too narrowly. The behaviour is the one the
template states; the two sentences read against it. The A9 half is a
paperwork correction and sits in its own row below.

Why ⬜ and not 🟡: the comment and the docstring are read by a person and
pin nothing a reader acts on; the template, the sealer and the code agree,
and the release ships no defect if this stands. The reopening is spent, so
it goes to a ticket rather than a fix pass. **What the ticket should carry**:
the comment sentence rewritten to name the replace and its key; the docstring
sentence and A9 rewritten to say distinct comparisons; and a case in the seal
module that reads a written `broad-gate.md` for the sentence — round 2's
second regression row — seen red before it is planted.

### ⬜ · A `seal/ledger.md` row was re-hashed twice on this branch with no re-read note

`seal/ledger.md:88`, the row *The answer a run ends on had no field*,
anchored on `templates/sdd-round.md`'s field table. **Executed**: its second
anchor reads `@22992524` at `0b8dc4b2`, `@35e76377` at `21b8d61e` and
`@4286fbab` at the target, while its last note is still *Re-read 2026-09-10*;
S5, anchored on the same table, carries a note for each of the same moves,
the last one *by the same work item's round 2 fix pass (🟡 1)*. The claim
holds — **read**: the branch's diff of the template changes the `Broad gate`
and `Fix range` rows and not `Needs a fix` — so the hash is right and the
row is silent about who moved it. Paperwork: a re-read note on the row
naming the two passes, or the statement that the move was a re-hash and not
a reading.

## Regression tests to plant

| Test | Destination |
|---|---|
| a written `broad-gate.md` carries the sentence that says a same-run re-seal replaces its entry and another base is kept (with ⬜ 1's ticket) | `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside `test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list` |

## Facts for the evidence ledger

- A9's last clause, once ⬜ 1's ticket lands: the count of entries is the
  count of distinct comparisons, commit and base, and not the count of runs.
- The `seal/ledger.md` row above: re-hashed at `21b8d61e` and `db292bfb` by
  the template's `Broad gate` row moving the field table's anchor; the
  `Needs a fix` row it is about is untouched.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the `broad-gate.md` comment says a run taken again leaves the earlier one behind it, and the docstring says the count of entries is the count of runs; under `same_run` a same-run re-seal replaces and is two runs in one entry; no test reads the written comment | `skills/code-review/scripts/round_record.py:4278-4280`, `:363-365` | deferred to a new issue, filed from this record by the repository owner | read — the comment against the replace at `:380-381` and the template's clause; executed — the grep over `tests/` hits one docstring and nothing that reads the file; round 2's regression row for the comment was not planted |
| ⬜ | A9's last clause says the count of entries is the count of runs; a same-run re-seal is two runs and one entry, so the count is of distinct comparisons | `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:20` | correction | read — the clause against `kept_broad_gate:380-381`; the previous text said *runs at distinct commits* |
| ⬜ | the `seal/ledger.md` row anchored on the template's field table was re-hashed at `21b8d61e` and `db292bfb` with no re-read note, while S5 carries one per move; the claim holds | `seal/ledger.md:88` | correction | executed — the anchor `@22992524` → `@35e76377` → `@4286fbab`, last note 2026-09-10; read — the template's `Needs a fix` row is untouched on the branch |
| 🟢 | round 2's 🟡 1 — `same_run` keys the replace on commit AND base, `kept_broad_gate` replaces only on `same_run`, the another-base case is red under the SHA-alone rule and green at the target, the same-base case pins the replace, and the template and A9 say what the code does | `skills/code-review/scripts/round_record.py:376-402`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2555-2594`; `templates/sdd-round.md:39`; the fragment's `:20` | verified | executed — m1 red at the another-base case alone with the cell holding one entry, m2 red at the same-base case alone, m3 red at four re-seal cases including the direct home; read — the helper and the two sentences |
| 🟢 | round 2's ⬜ 2 — the verify skill's stands phrase is absent at `0b8dc4b2` and present once at the target, and removing it turns the stands half red | `tests/test_the_broad_gate_cell_keeps_every_run.py:57-61`; `skills/verify/SKILL.md:456` | verified | executed — 0 at the base, 1 at the target; m4 red at `test_every_carrier_says_the_cell_holds_one_entry_per_run` |
| 🟢 | round 2's ⬜ 3 — the docstring is true of both callers: `seal` refuses a flag with no SHA-shaped word or one that does not resolve, `close` writes its flag as typed | `skills/code-review/scripts/round_record.py:371-375`, `:3956-3960`, `:4484-4493` | verified | read — `close`'s body consults `SHA_RE` nowhere and `resolves_to` only for the fix table's commits |
| 🟢 | the two paperwork corrections — A11 in the fragment and round 1's 🟡 2 grounds at `e101abac` — state what `GATE_CARRIERS` pins: eight documents, the `broad-gate.md` comment unpinned | the fragment's `:22`; `rounds/round-1.md:36` | confirmed | read — eight tuples in `GATE_CARRIERS`; each cell's *ninth carrier* names a different thing and each is true in its count |
| 🟢 | the fix range touched nothing the findings did not name: six files, every hunk one of 🟡 1, ⬜ 2, ⬜ 3, the paperwork row or a re-anchor moved by the template's row; the range is two commits as the record states | `git diff --stat 43afbc1e..db292bfb`; `rounds/round-2.md` | verified | read — every hunk mapped; executed — `git rev-list --count` 2; `evidence-check --strict` exit 0, 1624 ok |
| 🟢 | the new units as code — `same_run` and the another-base case — are correct; `zip(strict=True)` sits behind a length guard within the Python 3.12 floor | `skills/code-review/scripts/round_record.py:386-402`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2580-2594` | verified | executed — the three modules and m1–m3; read — the punctuation edge yields a duplicate and never an erasure |
| 🟢 | round 2's record at `8b04523a` states the fix as it landed — 🟡 1, ⬜ 2 and ⬜ 3 fixed at `fb960e6c`, the paperwork row answered at `e101abac`, the fix range two commits, two new units at depth 1 | `rounds/round-2.md:11-16`, `:28-31` | verified | read — against the fix range's diff; executed — the commit count |
| 🟢 | round 1's and round 2's 🟢 rows stand; the rows resting on `kept_broad_gate` and the carrier module were re-derived by the modules and mutations above | `rounds/round-1.md`; `rounds/round-2.md` | confirmed | executed — the seal, close and carrier modules at the target; read — the other rows cover code the fix range did not touch |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict` over the tree the sealer stands on, taken once now that the rounds have settled | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; this round leaves nothing open, so the sealer's spawn is due; this round's `evidence-check` and per-file ruff are probes over the clone, not the gate |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_the_fixes_close_the_record.py -q` in the clone at `8b04523a`, exit read from the file it was written to | `232 passed in 215.75s`, exit 0 |
| baseline before any mutation: the seal module `-k "re_seal or another_base"`, and the carrier module | 7 passed, 119 deselected, exit 0; 3 passed, exit 0 |
| m1 — `same_run`'s `elif x != y` arm disabled, so only SHA-shaped words are compared (the rule at `43afbc1e`) | `test_a_re_seal_at_the_same_commit_against_another_base_keeps_both` 1 failed with the cell `f302329 against origin/base`, 6 passed, exit 1 |
| m2 — the replace dropped (`entries = entries[1:]` → `pass`) | `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry` 1 failed with the commit entered twice, 6 passed, exit 1 |
| m3 — `same_run` returns True unconditionally | 4 failed (`…keeps_the_earlier_run…`, `…replaces_that_entry`, `…keeps_both`, `test_the_direct_home_takes_the_same_shape_on_a_re_seal`), 3 passed, exit 1 |
| m4 — `skills/verify/SKILL.md:456` loses `[; earlier run: <sha> vs base <sha>]` | `test_every_carrier_says_the_cell_holds_one_entry_per_run` 1 failed naming that carrier, 2 passed, exit 1 |
| after every mutation `git checkout --` on the file; `git status --porcelain` in the clone | clean |
| `git show 0b8dc4b2:skills/verify/SKILL.md`, grep counts of `; earlier run: <sha> vs base <sha>` and of `earlier run`, then the same at the target | 0 and 1 at the base; 1 and 2 at the target |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone, exit read directly | exit 0 — `total: 1624 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm 0 refused, 0 drifted |
| `uvx ruff check` and `uvx ruff format --check` over the three `.py` files the fix range edited, exits read directly | exit 0 and exit 0; `All checks passed!`, `3 files already formatted` |
| `git rev-list --count 43afbc1e..db292bfb` | 2 |
| the anchor hash of the `seal/ledger.md` row *The answer a run ends on had no field* at `0b8dc4b2`, `21b8d61e`, `43afbc1e` and the target | `@22992524`, `@35e76377`, `@35e76377`, `@4286fbab`; last note 2026-09-10 at every one |
| `grep -rn "stays behind it\|a run taken again\|earlier one stays" tests/` | one docstring, `tests/test_the_seal_is_taken_once_by_the_sealer.py:2556`; nothing reads a written `broad-gate.md` for the sentence |
| this report through `round_record.py new --round 3 --target 8b04523a… --baseline 0b8dc4b2` in the clone, then `evidence-check --strict` with the report in place; the record it wrote and its reach-back into `round-2.md` undone in the clone (the worktree's record is the orchestrator's to write) | `new` exit 0 — `Pass` ticked with ⬜ 1 read as closed on `deferred`, both terminal lines copied as values, 12 verdict rows and both fenced blocks carried, `Fixes checked by` reads `no fixes to check`, and the generator printed that this record ends the run and the run is capped; `evidence-check` exit 0, 1624 ok, 641 names read, 0 refused |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` at the tree the sealer stands on | not yet |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the `broad-gate.md` comment's *the earlier one stays behind it* and the *count of runs* sentence in the docstring and A9 predate `same_run`; no test reads the written comment | a new issue, filed from this record: the comment names the replace and its key, the docstring and A9 say distinct comparisons, and the seal module pins the written sentence (round 2's second regression row), seen red first | the repository owner |

## Paste-ready fixes

### ⬜ 1 — skills/code-review/scripts/round_record.py

The comment's last sentence, replacing *One entry per run, newest first: a
run taken again is written in front, and the earlier one stays behind it as
`earlier run`, so the reader takes the first SHA as the run.*

```python
        "having run. One entry per run, newest first: a run at a new commit,\n"
        "or at this one against another base, is written in front and the\n"
        "earlier one stays behind it as `earlier run`; a run the newest entry\n"
        "already records — the same commit against the same base — replaces\n"
        "it. The reader takes the first SHA as the run. -->\n"
```

The docstring's count sentence at `:363-365`, replacing *two entries for one
claim would make the count of entries stop being the count of runs*.

```python
    two entries for one claim would make the count of entries stop being
    the count of distinct comparisons — commit and base — which is what
    the run-level table reads off the cell.
```

Needs a fix: no — ⬜ 1 is prose beside behaviour the template, the sealer and the code agree on, deferred to a ticket the owner files; the two corrections are paperwork
Loses a record or crashes: no — nothing found writes outside `seal/specs/` or raises; the one erasure round 2 opened is closed, and a same-run re-seal replaces an entry with the same bytes

## Proof

Opened, in the clone at `8b04523a` unless said otherwise:
`seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/rounds/round-1.md`,
`rounds/round-1-report.md:1-80`, `rounds/round-2.md`, `rounds/round-2-report.md`,
`changelog.md` (tail); `skills/code-review/scripts/round_record.py`
(`EARLIER_RUN` and its comment, `kept_broad_gate`, `same_run`, `close`'s cell
wiring at `:3956-3960` and its body by grep, `new_broad_gate_file`, `seal`'s
head and refusals at `:4380-4415` and `:4465-4495`);
`skills/code-review/scripts/chain_check.py` (`SHA_RE`, `says_gate_not_yet`,
`CLOSED_WORDS` and the vocabulary comments at `:386-440`); the fix range's
diff over all six files, and the diffs of `e101abac` and `8b04523a`;
`agents/sealer.md:136-144`, `:183-190`; `docs/review-chain-spec.md:336-348`;
`templates/sdd-round.md:39`; `skills/verify/SKILL.md:456`, `:783`;
`tests/test_the_broad_gate_cell_keeps_every_run.py:1-90`;
`tests/test_the_seal_is_taken_once_by_the_sealer.py:2540-2600` and `run_seal`;
`seal/ledger.md` rows S5 and *The answer a run ends on had no field*, and
the fragment's A9 and A11; `bin/test`; `.github/scripts/run_tests.py` (the
venv and floor lines); `ruff.toml:27`; `CONTRIBUTING.md:127`. At `0b8dc4b2`,
`21b8d61e` and `43afbc1e` through `git show`: `skills/verify/SKILL.md`,
`seal/ledger.md`'s two rows, and `round_record.py`'s `kept_broad_gate`. Not
opened: the survivor sweep's inputs, the suite beyond the three modules.
