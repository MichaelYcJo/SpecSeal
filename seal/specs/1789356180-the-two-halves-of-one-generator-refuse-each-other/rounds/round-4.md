# 1789356180-the-two-halves-of-one-generator-refuse-each-other — review round 4

| Field | Value |
|---|---|
| Target SHA | 151792e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 394 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 1, 2, 3 and 4 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A round the chain's reopening bound did not allow, spawned deliberately by the repository owner. Round 3 had answered the floor `yes` — a numbered short row crashed with an `IndexError` where the base refused it cleanly — and the floor is the one condition the chain will not let a branch defer, so the owner chose a further round over shipping that capped. The spawn said so plainly, and said that `chain_check` now refuses one line no later commit can clear — *round-3.md is the second later record whose verdicts closed on a fix* — which is expected and not this round's to chase.

The spawn also said there is no round after this one, so anything left has no later, and every finding had to be written so somebody could act on it without its author.

Target is the diff of round 3's fixes, `c2b2b30..151792e`, three commits. Rounds 1, 2 and 3 had reviewed everything before `c2b2b30`. Round 3's record was committed and its four verdicts inherited; the job was the answers rather than new findings.

The exempt surface, handed over as a finding surface because units the fixes created have been reviewed by nobody: the six round 3's record names — `says_open` and five cases. Two questions were weighted above the rest. First, the fix pass had **refused round 3's own paste-ready bound** and chosen a narrower one, because the proposed `len(seen) < len(VERDICT_HEADER)` refuses a four-cell row that has a Verdict cell and is only missing `Grounds`, which a shipped case deliberately admits — so the round was asked to judge the narrower bound on its own, for what it admits that reaches an index elsewhere and whether both subcommands stay inside it. Second, `says_open` ending the word on `chain.SEPARATORS` — what a reviewer can write that means open and it still misses, and whether borrowing that set couples two rules that should move independently.

Four acts of the fix pass were handed over as facts: that it re-measured the corpus rather than carrying round 3's numbers and got different figures because the corpus grew by this run's own records; that both the crash and the docstring indentation were regressions it had introduced itself in round 2 at `7b2c0d7`; that 4/4 mutations were killed after one survivor, the separator boundary nothing observed because no case fed it a longer word; and that it left round 3's ⬜ 5 alone deliberately — `chain_check.open_blocking` reading only 🔴 rows — because both generator subcommands refuse the shape and a second gate would be mechanism no finding required. The round was told to check that last reasoning rather than the code alone, it being the one place this run chose not to close something it could see.

The round was told this release has had five wrong measurements, every one from a loose match, and to re-derive anything it relied on with the module's own reader.

What the orchestrator had already executed at `151792e`, handed over so the round would not repeat it: five modules — `test_a_finding_id_is_a_bare_integer.py`, `test_the_fixes_close_the_record.py`, `test_the_record_is_generated.py`, `test_the_rules_have_one_owner.py`, `test_what_the_reader_understands.py` — 427 passed, exit 0; `survivor-check --range c2b2b30..5a9bf39 --exempt …` exit 0; and `chain_check --worktree` refusing exactly three lines, two of which this round and the sealer close.

The broad gate was withheld by name as the sealer's single act after this round settles.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The re-measurement *127 verdict cells begin `open`, 9 continue, equality reached 118* does not reproduce under any population. The module's own reader gives 95, 7 and 88 over 1,704 rows in 176 records — round 3's figures. The same sentence is in the ledger fragment | `skills/code-review/scripts/round_record.py:2391`, `tests/test_a_finding_id_is_a_bare_integer.py:379` | deferred #395 | #395 — The run ends at this record and its floor row reads `no`, so the findings are handed over rather than chased — which is what the floor is for. The docstring count is the release's sixth wrong measurement and the first taken WITH the module's reader and still wrong, which is why the issue says so; executed at `151792e` — six populations measured through `table_body` and through `chain_check.verdict_table`: records 95/7, records plus this item's reports 108/7, records plus all reports 570/15, loose pipe-row reading 95/7. The nearest figure to 127 is 129, and only by counting every cell of every column. The two neighbouring claims, *15 of 25* and *0 newly refused*, both reproduce exactly |
| 2 | 🟡 Four live coordinates say `says_open` borrows the boundary `verdict_of` uses for its vocabulary. `verdict_of` ends its vocabulary on a space or a comma and says so in its own docstring; `chain.SEPARATORS` is six characters wide, so `open-ended question` and `open: see 5` are refused as the open verdict and the refusal names a word the cell does not carry | `skills/code-review/scripts/round_record.py:2386`, `:2470`, `docs/review-chain-spec.md:776`, `tests/test_a_finding_id_is_a_bare_integer.py:382` | deferred #395 | #395 — Same bound. Verified independently by the orchestrator before filing: `open-ended question` and `open: see 5` both read as the open verdict and are refused with a message naming a word the cell does not carry. The narrow boundary the documents already describe is in the issue; executed at `151792e` — `fixed d3fe44d` reads `fixed`; `fixed—d3fe44d`, `fixed-d3fe44d` and `fixed:d3fe44d` read as the whole cell. `says_open` is True for `open-ended question` and `open: see 5`. The proposed narrower boundary reaches all 95 committed cells, excludes both, and leaves the two modules green at 63 and 119 passed |
| 3 | 🟡 The comment introducing `OPEN_WORD` still reads *exact rather than a vocabulary test*, ten lines above the function that replaced the exact match, and directly under a comment this same commit rewrote. Round 3's 🟡 3 class, one member left standing in the edited file | `skills/code-review/scripts/round_record.py:2370` | deferred #395 | #395 — Same bound. `OPEN_WORD`'s comment still says the match is exact, ten lines above the function that stopped it being exact — round 3's own 🟡 3 class, reproduced by the commit that closed it; read at `151792e`, class enumerated by grep: every other live carrier of the overturned ruling is corrected, and the only remaining copies are in committed records and reports, which are history. The spec's copy is guarded by a case; this one is guarded by nothing |
| 4 | 🟡 `test_a_row_missing_only_its_grounds_is_still_written_short` says the four-cell row *IS refused* and asserts `code in (0, 2)`. It is not refused: `new` exits 0 and writes the record with the row at four cells, because a keyed row never reaches the verdict arm. The assertion admits both answers, so the case cannot fail on the regression it names | `tests/test_a_finding_id_is_a_bare_integer.py:348` | deferred #395 | #395 — Same bound. `assert code in (0, 2)` admits both answers, so the case cannot fail on the regression its name describes. The behaviour is right and deliberate; the case is not; executed at `151792e` — the case's own input through `generate` gives exit 0, the record on disk, and `\| 1 \| one \| \`f.py:1\` \| open \|` in its verdict table. The repaired assertions were run and pass |
| 5 | ⬜ The new short-row guard raises on the first offending row, inside the loop whose docstring states #303's rule that offending rows are collected and refused once. Pre-existing in shape — only the condition widened — and zero committed rows are short | `skills/code-review/scripts/round_record.py:3126` | deferred #395 | #395 — Same bound. The short-row guard raises on the first offending row where `id_refusal` names every one — the shape #303 measured at two round trips per repair, arriving in the arm added to close a crash; read at `151792e` against `finding_number`'s own docstring and the `bad`/`owed` accumulation beside the guard |
| 6 | ⬜ The inserted clause left *test, and the* alone on a line | `docs/review-chain-spec.md:779` | deferred #395 | #395 — Same bound. A line-wrap artefact in the inserted clause; read at `151792e`; renders correctly |
| 7 | Round 3's 🔴 1 is closed on both subcommands, not only the one the new case covers | `skills/code-review/scripts/round_record.py:3112` | answered | executed at `151792e` — a two-cell numbered row through `new` exits 2 with the new refusal; the same row hand-edited into a record and run through `close` exits 2 with the same message, no traceback |
| 8 | The narrower bound admits nothing that reaches an index elsewhere. Every caller indexes `NUMBER_COL`, `VERDICT_COL`, or `GROUNDS_COL` behind the padding loop | `skills/code-review/scripts/round_record.py:1970`, `:3360`, `:3377`, `:3426`, `:3444` | answered | executed at `151792e` — a four-cell row through `new` (written short, exit 0), through `close` inside the fix table (rewritten and padded) and through `close` outside it (copied back untouched). No traceback on any path; read at all five index sites |
| 9 | The grounds for refusing round 3's own paste-ready bound are true | `tests/test_the_record_is_generated.py:2214` | answered | executed at `151792e` — with the bound widened to the header width, `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one` is the one failure, 1 failed and 118 passed against 119 passed unmutated |
| 10 | The new cases were seen red where they can be, and the rest are killed by the mutation each was written for | `tests/test_a_finding_id_is_a_bare_integer.py:324`, `:370`, `:397` | answered | executed at `151792e` — the module against `c2b2b30`'s generator: 4 failed, 59 passed. Mutations: bound back to `NUMBER_COL` kills the short-row case; dropping the separator test kills the longer-word case; equality restored kills three of the four spelling parameters |
| 11 | `says_open` reaches the corpus it claims and costs nothing, whatever the count beside it says | `skills/code-review/scripts/round_record.py:2380` | answered | executed at `151792e` — all 95 committed cells beginning `open` reached, none in `CLOSED_WORDS`, 0 of the 25 admitted no-digit rows newly refused |
| 12 | Round 3's 🟡 3 class is otherwise fully enumerated; the only remaining copies of the overturned ruling are in committed records and reports | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2449`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | answered | read at `151792e` — grep of the claim across the tree; four live carriers corrected, one missed and opened as finding 3 |
| 13 | Round 3's ⬜ 5 was left alone on sound grounds, and its premise is what the checker does | `skills/code-review/scripts/chain_check.py#open_blocking` | answered | read at `151792e` — rows are selected by `BLOCKING in "".join(seen)` and an unclosed verdict, so a no-digit row reading `open` is invisible at CI. Both generator subcommands refuse it. Named here rather than reopened, and worth recording as a stated divergence if the branch ships |
| 14 | The ledger fragment's anchors survive the fix and both moved functions re-hash | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | answered | executed at `151792e` — `evidence-check .` exits 0: 1,220 ok, 0 drifted, 0 broken, this fragment 28 ok |
| 15 | Round 3's record is a truthful application of its fix table, and `New units` names all six | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-3.md` | answered | read at `151792e` against the three commits. Under `seal/specs/`, so a correction surface rather than a fix surface |
| 16 | The ledger fragment carries findings 1 and 2 in its own words — the count 127 and the borrowed boundary. A correction, taken with whichever fix those two findings get | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | deferred #395 | #395 — Same bound, and it is the one that outlives the branch: the ledger fragment carries the unreproducible 127 in its own words, and a fragment folds into `seal/ledger.md` at the release. Named first in the issue for that reason; read at `151792e`. Under `seal/ledger/`, so a correction surface and not counted by `Needs a fix` |

## Paste-ready fixes

```python
    Measured over every committed record: 95 verdict cells begin `open` and 7
    of them continue, so equality reached 88 of 95 while `agents/warden.md`,
    `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a
    match on the word. None of the 95 is in `CLOSED_WORDS`, and the boundary
    match newly refuses 0 of the 25 admitted rows (round 3's 🟡 2).
```
```python
    Measured over every committed record: 95 verdict cells begin `open` and
    **7 of them continue** — `open — deferred`, `open, comment only` and five
    more — so the equality reached 88 of 95 while the documents described all
    of them. A head match ended the way `verdict_of` ends its own vocabulary,
    on a space or a comma, reaches all 95 and newly refuses **0** of the 25
    admitted no-digit rows.
```
```python
# The boundary `verdict_of` ends its own vocabulary on -- `fixed d3fe44d` and
# `fixed, d3fe44d` are both `fixed`. Spelled here rather than reached for in
# `chain.SEPARATORS`, which is six characters wide and has five other readers:
# borrowing it made `open-ended question` and `open: see 5` read as the open
# verdict, and tied what counts as open to a constant the `deferred` home
# reader is free to widen.
OPEN_BOUNDARY = (" ", ",")


def says_open(word):
    """`word` is the open verdict, however the reviewer ended it.

    The grounds for not running a VOCABULARY test hold and are untouched:
    `verified` is in no vocabulary and would be refused, which costs 15 of the
    25 admitted no-digit rows in the committed records. What never followed
    from those grounds is EQUALITY. `verdict_of` ends a vocabulary word on a
    space or a comma — that is what makes `fixed d3fe44d` read as `fixed` —
    and the same boundary here reaches `open — deferred` and `open, comment
    only`.

    Measured over every committed record: 95 verdict cells begin `open` and 7
    of them continue, so equality reached 88 of 95 while `agents/warden.md`,
    `templates/sdd-round.md` and `skills/code-review/SKILL.md` all describe a
    match on the word. Every one of the 7 continues with a space or a comma,
    so the narrow boundary reaches all 95; none of them is in `CLOSED_WORDS`,
    and the match newly refuses 0 of the 25 admitted rows (round 3's 🟡 2).
    """
    if not word.startswith(OPEN_WORD):
        return False
    rest = word[len(OPEN_WORD) :]
    return not rest or rest[0] in OPEN_BOUNDARY
```
```python
    **The `#` cell is not the only cell that says a row owes an answer**, which
    is why `verdict_rows` reads the Verdict cell beside it. Reading the marker
    alone admitted six shapes whose Verdict cell said `open` — three of them
    carrying no marker at all, so the residual stated here for a round did not
    describe them (round 2's 🟡 7). It matches the WORD — `says_open` ends it
    on a space or a comma, the boundary `verdict_of` uses for its own
    vocabulary — rather than a vocabulary, and that is what makes it free:
    `verified` is in no vocabulary and therefore OPEN, so refusing everything
    outside `CLOSED_WORDS` would refuse 15 of the 25 admitted rows.
```
```markdown
That is a match on the word — ended by a space, a comma, or nothing, the
boundary `verdict_of` uses for its own vocabulary, so `open — deferred` and
`open, comment only` are reached and `opened` is not — rather than a
vocabulary test, and the difference is what makes it free. `verified` is in no
vocabulary and therefore reads OPEN, so refusing everything outside
`CLOSED_WORDS` would refuse every confirmation row — one refusal traded for
another. Refusing the word `open` refuses none of them: of the 25 admitted
no-digit cells in the committed records, not one reads it.
```
```python
@pytest.mark.parametrize(
    "verdict", ["opened in round 2", "openly carried", "open-ended question"]
)
def test_a_word_that_merely_begins_with_open_is_not_the_open_verdict(repo, verdict):
    """The boundary is what makes `says_open` match a WORD rather than a
    prefix of one — the same distinction `verdict_of` states for its own
    vocabulary, where without it `not a defect` would swallow `not a defective
    reading`.

    It is the same boundary as well as the same distinction: a space or a
    comma, not `chain.SEPARATORS`. The wider set reached `open-ended question`
    and `open: see 5`, and the refusal then named a word the cell does not
    carry.

    Found by mutation: dropping the separator test left every other case in
    this module green, because no case fed it a longer word.
    """
    _code, out = a_report(repo, f"| carried | one | `f.py:1` | {verdict} | read |\n")
    assert "`Verdict` cell reads `open`" not in out, out
```
```python
# The one verdict word that says the row is open in as many letters. Read only
# on a row whose `#` cell has already admitted it, where the two cells then
# contradict each other -- and one WORD rather than a vocabulary test, which
# is the distinction the grounds for NOT reading the verdict missed.
# `verified` is in no vocabulary and therefore OPEN, so reading the verdict as
# OPEN/CLOSED would refuse every confirmation; reading this one word refuses
# none of them. `says_open` below is where the word ends. Free against the
# corpus: of the 25 admitted no-digit rows in the committed records, not one
# has a Verdict cell reading `open` (round 2's 🟡 7).
```
```python
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(verdicts="| 1 | one | `f.py:1` | open |\n")
    )
    assert "Traceback" not in out and "IndexError" not in out, out
    assert "no `Verdict` cell" not in out, out
    # ADMITTED, and written at the width the reviewer left. The verdict arm
    # never sees this row -- a digit in the `#` cell keys it, and that arm runs
    # only where `finding_number` returned None -- so `new` exits 0 and the
    # record carries four cells. Round 3's wider bound turns exactly this case
    # red, which is why the bound is `VERDICT_COL`.
    assert code == 0, out
    assert "| open |" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_finding_id_is_a_bare_integer.py -q` at `151792e` in the clone | 63 passed, exit 0 |
| `bin/test tests/test_the_record_is_generated.py -q` at `151792e` in the clone | 119 passed, exit 0 |
| the same bare-integer module against `c2b2b30`'s `round_record.py` | 4 failed, 59 passed — the short-row case and three of the four spelling parameters red; the bare `open` parameter green, because equality already caught it |
| mutation: bound back to `len(seen) <= NUMBER_COL` | 1 failed — `test_a_numbered_short_row_is_refused_rather_than_raising` |
| mutation: bound widened to `len(seen) < len(VERDICT_HEADER)`, round 3's proposal | in the bare-integer module, 1 failed — `test_a_row_missing_only_its_grounds_is_still_written_short`; in `test_the_record_is_generated.py`, 1 failed and 118 passed — `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one`, against 119 passed unmutated. Finding 9's grounds |
| mutation: `says_open` returns True without testing the boundary | 2 failed — both parameters of `test_a_word_that_merely_begins_with_open_is_not_the_open_verdict`. The fix pass's survivor reproduces |
| mutation: the verdict arm restored to equality | 3 failed — the three wider spelling parameters |
| probe: `\| 1 \| one \|` through `new`, and the same row hand-edited into a record through `close` | exit 2 both times with the new refusal quoting the row; no traceback, no record written. Finding 7 |
| probe: a four-cell row through `new`, through `close` inside the fix table, and through `close` outside it | exit 0 and written short; rewritten and padded; copied back untouched. No traceback on any path. Finding 8 |
| every committed `round-N.md` through the module's own `table_body` | 176 of 216 parse, 1,704 verdict rows, **0 short**, 51 no-digit, 25 admitted, 15 of those outside `CLOSED_WORDS`. Finding 1 |
| every committed verdict cell through `verdict_of`, counting cells that begin `open` | **95** across 8 spellings — 88 bare, 7 wider, none in `CLOSED_WORDS`; `says_open` reaches all 95 and newly refuses 0 of the 25 admitted rows. Findings 1 and 11 |
| the same count over five other populations — records plus this item's reports, records plus all reports, every `.md` in the tree, the loose pipe-row reading, and `chain_check.verdict_table` | 108, 570, 570, 95, 95. None is 127. Finding 1 |
| `verdict_of` over `fixed d3fe44d`, `fixed, d3fe44d`, `fixed—d3fe44d`, `fixed-d3fe44d`, `fixed:d3fe44d` | `fixed`, `fixed`, and the whole cell for the last three — the vocabulary boundary is a space or a comma, not `chain.SEPARATORS`. Finding 2 |
| `says_open` over 22 spellings a reviewer might write | `open-ended question` and `open: see 5` are refused as the open verdict; `still open`, `open?` and `open; see 5` are not reached. Finding 2 |
| the proposed narrow boundary applied to the generator | reaches 95 of 95 committed cells, excludes `open-ended question` and `open: see 5`; 63 passed and 119 passed across the two modules, exit 0 both. Finding 2 |
| the repaired assertions for finding 4, run as written | 1 passed — exit 0, the record on disk, the row at four cells |
| `bin/evidence-check .` at `151792e` | exit 0 — 1,220 ok · 0 drifted · 0 broken; this work item's fragment 28 ok. Finding 14 |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 leaves all three to the sealer, and this round ran none of them. It has not come due: findings 1 through 4 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:2392` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2332`, `:2363`; `docs/review-chain-spec.md` §*The finding id*; `skills/code-review/SKILL.md` §*A row that commissions nothing takes no id at all*; `templates/sdd-round.md` | round 1's 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2950` | round 1's 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2936` | round 1's 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:3166` | round 1's 5 — fixed |
| round-1 | `seal/ledger.md`, row R1 · a finding id is a bare integer | round 1's 6 — answered |
| round-1 | `seal/specs/1789356180-…/phases/phase-1.md`, `phases/phase-3.md` | round 1's 7 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py#MARKER`, `#verdict_of` | round 1's 8 — answered |
| round-1 | `9d1e324`, `26c7696` | round 1's 9 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#fix_table` | round 1's 10 — answered |
| round-1 | `git diff release/v0.11.4...HEAD` | round 1's 11 — answered |
| round-1 | `seal/ledger.md` | round 1's 12 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2447`, `:3073` | round 2's 1 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2366` | round 2's 2 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2354`; `docs/review-chain-spec.md` §*A verdict row that commissions nothing*; `skills/code-review/SKILL.md`; `templates/sdd-round.md`; `phases/phase-1.md` | round 2's 3 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3025` | round 2's 4 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3000` | round 2's 5 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3262` | round 2's 6 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:2447`, `:3063` | round 2's 7 — fixed |
| round-2 | `seal/specs/1789356180-…/survivors.md:27` | round 2's 8 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:3073` | round 2's 9 — answered |
| round-2 | `skills/code-review/scripts/round_record.py`, `#inherited_rows`; `.github/workflows/hygiene.yml:191` | round 2's 11 — answered |
| round-2 | `seal/specs/1789356180-…/survivors.md`; `plan.md:72`; `phases/phase-1.md:64`; `skills/verify/scripts/broad_gate.py:584` | round 2's 12 — answered |
| round-2 | `58511d0` | round 2's 13 — answered |
| round-2 | `seal/specs/1789356180-…/rounds/round-1.md` | round 2's 14 — answered |
| round-3 | `skills/code-review/scripts/round_record.py:1970`, `:3307`, `:3324`, `:3383` | round 3's 1 — fixed |
| round-3 | `skills/code-review/scripts/round_record.py:2376`, `:3095` | round 3's 2 — fixed |
| round-3 | `docs/review-chain-spec.md:790`, `skills/code-review/scripts/round_record.py:2363`, `:2423`, `tests/test_a_finding_id_is_a_bare_integer.py:236` | round 3's 3 — fixed |
| round-3 | `skills/code-review/scripts/round_record.py:2387` | round 3's 4 — fixed |
| round-3 | `skills/code-review/scripts/chain_check.py#open_blocking` | round 3's 5 — answered |
| round-3 | `skills/code-review/scripts/round_record.py:3091` | round 3's 6 — answered |
| round-3 | `tests/test_a_finding_id_is_a_bare_integer.py:302` | round 3's 7 — answered |
| round-3 | `skills/code-review/scripts/round_record.py:3092` | round 3's 8 — answered |
| round-3 | `skills/code-review/scripts/round_record.py:3094` | round 3's 9 — answered |
| round-3 | `skills/code-review/scripts/round_record.py:2367`, `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` row 1 | round 3's 10 — answered |
| round-3 | `seal/ledger/1789356180-the-two-halves-of-one-generator-refuse-each-other.md` | round 3's 11 — answered |
| round-3 | `seal/specs/1789356180-the-two-halves-of-one-generator-refuse-each-other/rounds/round-2.md` | round 3's 12 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| nothing to drain | — | — |
