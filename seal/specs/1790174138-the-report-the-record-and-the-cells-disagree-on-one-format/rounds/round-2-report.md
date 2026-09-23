# Round 2 report — the verifying round at round 1's fixes

Target SHA `0d3a9fb4f76f42cba62de6e3643ec37311e73761`, on
`fix/503-the-report-the-record-and-the-cells-disagree-on-one-format`, against
the base `0b8dc4b2`. The surface this round opened is the fix range
`83988abd..21b8d61e` (three commits) and the record commit `0d3a9fb4`; the
branch beyond that surface is round 1's, and round 1's 🟢 rows are carried
except where the fix range touched what they cover. Work was done in a
`git clone --no-local` of the worktree at the target SHA; the worktree was
read and never written, except for this file.

## Summary

Round 1's three 🟡 and five ⬜ each landed where the record says, and the
seven mutations the hand-back lists each turn their own case red in the
clone. The fix range touched nothing the eight findings did not name, apart
from the ledger re-reads that the third commit is for.

One thing needs a fix, and it is the decision the orchestrator asked me to
check rather than take. ⬜ 8's *replace* rule makes a re-seal at the commit
the newest entry names erase that entry, base included — and four carrier
sentences still say the opposite: `agents/sealer.md` twice (*a second broad
run never erases the record of the first*, *every earlier run kept behind
it*), `docs/review-chain-spec.md` (*a re-seal records a second run rather
than erasing the first*), and the comment `new_broad_gate_file` writes into
`broad-gate.md` (*a run taken again is written in front, and the earlier
one stays behind it*). The sealer's own binding says a seal is the commit
AND the base, so two runs at one commit against two bases are two claims,
and the case that pins the rule is exactly that shape — `against base`
replaced by `against origin/base`. That is 🟡 1: the documents and the code
disagree on the cell, in the class this work item is named for.

Two ⬜ on the new units (a pin phrase that was already in its carrier before
the rewrite; a docstring sentence true of one caller and not the other) and
one paperwork correction (A11 and round 1's grounds count nine documents
where eight are pinned; the ninth carrier is code) complete the list.

## The implementer's account, checked

- *`kept_broad_gate` is the one cell-writing path for `seal` and
  `close --broad-gate`.* **Read**: `round_record.py:3936-3943` builds
  `close`'s cell through it from the record's own rows
  (`chain.table_rows(reader, lines)`, where `lines` is the record read at
  `:3847`), and `seal` at `:4499` calls the same function; no other line
  writes `BROAD_GATE`. **Executed**: mutation m1 (`close` built from the
  flag alone) turns `test_close_broad_gate_keeps_a_run_the_cell_already_holds`
  red, exit 1; m3 (the helper never keeping) turns that case and three
  re-seal cases in the seal module red.
- *A `close` at HEAD before the fix replaced a held run.* **Read** off the
  diff: the removed line was `gate = cell(BROAD_GATE, args.broad_gate)`.
  m1 restores that shape and the case is red — same evidence one step over.
- *The ninth carrier is rewritten and all nine are pinned as gone/stands
  pairs.* **Executed**: for each of the eight `GATE_CARRIERS` tuples, the
  gone sentence is present in the carrier at `0b8dc4b2` and absent at the
  target, and the stands phrase is present at the target (a script over
  `git show 0b8dc4b2:<path>` and `flat`). m6 (the old `skills/verify/SKILL.md`
  sentence appended) turns the gone half red and leaves the stands half
  green. **Read**: *nine* counts the seven `spec.md` lists, the eighth phase
  4 found and the ninth round 1 found — and the seventh of the spec's is
  the comment `new_broad_gate_file` writes into `broad-gate.md`, which is
  code, not in `GATE_CARRIERS`, and pinned by no test. Eight documents are
  pinned; the claim of nine is the correction below.
- *A repeated header row is skipped by both readers and the second table's
  real rows are carried.* **Read**: `table_body` at `:1128-1139` drops a row
  whose visible cells equal the header tuple; `verdict_table` at
  `chain_check.py:1574-1580` drops a row whose casefolded cells equal the
  casefolded header. **Executed**: m4 and m5 each turn their own case red.
  The two readers compare with different case rules — the generator
  exactly, the checker casefolded — but the generator refuses a first
  header that is not exact (`:1121-1126`), so a second header in another
  case is a shape nobody writes; noted, not a finding.
- *The five ⬜ went where the table says.* **Read** in the diff:
  `agents/warden.md:466-469` names both enders; `bound_line:2136` takes
  `not running or counted > 1` and the `reaches {counted + 1}` sentence is
  gone; the aggregate is dropped from `docs/review-chain-spec.md:979-985`
  and `skills/code-review/SKILL.md:329-334` with #437 as the source; the
  three-places module's docstring states four; a same-commit re-seal
  replaces (`:376-381`). **Executed**: m7 turns the count-walk case red;
  m2 turns the replace case red and leaves the different-commit re-seal
  case green.
- *`bound_line`'s running branch hard-codes `reaches 2 here`.* **Read**
  against `floor_and_fixes`: `fires = spent > 1 if stopped else spent >= 1`,
  so a running walk that fires has `counted >= 1`, and the branch that is
  reached with `running` and `counted == 1` is the only one left after the
  new guard. The constant is right by construction.
- *29 re-read ledger rows and A9–A11 state what the landed code does.*
  **Executed**: `evidence-check --strict` in the clone, exit 0, 1622 ok, 0
  drifted, 0 broken. **Read**: the 29 rows re-anchor on `close`, `seal`,
  `bound_line`, `verdict_table`, `broad_gate` and the documents the pass
  touched; their claims are about refusals, states and walks the fix did
  not change — S6's *six `raise Refused` sites* in `seal` is still six
  (counted at `:4387-4484`), S9's three fatal refusals in `broad_gate` are
  untouched, G2's four states are untouched. A9 states the replace rule
  and is true of the code; A10 is true; A11 says *nine documents* — see
  the correction.
- *The fix range touched nothing the three findings did not name.* **Read**
  over `git diff --stat 83988abd..21b8d61e`: fifteen files, each one of the
  eight findings' or the ledger's; no unrelated hunk.
- *Modules 231 + 134 + 141, six document-pin modules 175, ruff on eight
  files, sweep one excused.* **Executed** in the clone: the six modules the
  fix range touched, 506 passed; `ruff check` and `ruff format --check`
  over the eight edited files, exit 0 each (ruff through `uvx`, the
  workflow pinning no version). The survivor sweep was round 1's and the
  fix range removes no sentence the sweep would read differently — **read**,
  not re-run.
- *The broad gate.* Labelled `unverified` by the hand-back and by round 1;
  the sealer's, and `not yet` below.

## Findings

### 🟡 1 · A same-commit re-seal erases the entry it replaces, and four carriers say a re-seal never erases

`skills/code-review/scripts/round_record.py:376-381`: when the newest
entry's SHA and the flag's SHA agree by prefix, `entries = entries[1:]`
drops the newest entry whole, base and all, and the flag's value takes its
place. The case that pins it, `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry`,
re-seals `against origin/base` over `against base` and asserts the first
base is gone.

The carriers say the opposite, and they were rewritten by phase 4 to say
it. `agents/sealer.md:141`: *so a second broad run never erases the record
of the first (#174)*. `agents/sealer.md:186-188`: *Your seal is the commit
the run happened at and the base it was compared against … the newest
first, and every earlier run kept behind it*. `docs/review-chain-spec.md:341-343`:
*so a re-seal records a second run rather than erasing the first*. And
`round_record.py:4259-4261`, the comment written into every `broad-gate.md`:
*a run taken again is written in front, and the earlier one stays behind
it*. Against those four, `templates/sdd-round.md:39`, the docstring at
`:360-368` and ledger row A9 say *replaces*. That is a cell three documents
describe one way and three another — #503's own sentence.

Why the grounds do not hold as stated: *two runs at one tree are one claim*
is true only when the base is the same. The sealer's binding names both
halves, and the base decides the range every sweep in `broad-gate` reads —
so a run at one commit against a moved release branch is a second
comparison, and the entry it replaces was the record of the first. That is
the erasure #174 was filed on, one field narrower.

Two ways to close it, and the paste-ready below is the first: replace only
when the new entry records the same run — the same commit AND the same base
— so an identical re-run does not grow the cell and the four sentences stay
true. The second is to keep the rule and rewrite the four sentences (and
A9's *at the commit the newest entry already names*) to say a same-commit
re-seal replaces; that is an answer with grounds, and it has to reach all
four. The helper's name in prose is `same_run` NAME NOT IN TREE, and the
new case's is
`test_a_re_seal_at_the_same_commit_against_another_base_keeps_both` NAME NOT IN TREE.

### ⬜ 2 · One carrier's stands phrase was already in the file before the rewrite

`tests/test_the_broad_gate_cell_keeps_every_run.py:54-58`: the
`skills/verify/SKILL.md` tuple holds `earlier run` as *the phrase only the
list shape uses*. At `0b8dc4b2` that file already carried it, at line 783 —
*Output quoted from an earlier run* under §Counterfeits, nothing to do with
the cell. So for that carrier the stands half is satisfied by a sentence the
rewrite never touched, and only the gone half pins the rewrite (executed:
the phrase is present at the base for this carrier alone, absent for the
other seven). The behaviour is right and the gone half holds; the
docstring's *a phrase that only the list shape uses* is not true of one of
eight. The carrier's own new text at `:456` has a phrase nothing else in the
file carries.

### ⬜ 3 · `kept_broad_gate`'s docstring says the value was resolved by the caller, which is true of one caller

`round_record.py:367-368`: *nothing here asks git, because the value has
already been resolved by the caller that refuses an unresolvable one*.
`seal` does (`:4467-4472`); `close` does not — its `--broad-gate` is an
argparse string (`:4554`) and no line of `close` looks for a SHA in it
(read over `:3824-4182`). A `close --broad-gate 'HEAD against base'` writes
`HEAD against base` in front of a held run, as it did before the fix, and
`chain_check.broad_gate` reports it at the pull request. The behaviour is
unchanged and caught downstream; the sentence describes one of the two
callers the function was written to unify.

### ⬜ · A11 and round 1's grounds count nine documents where eight are pinned

`seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:22`,
A11: *the nine documents that describe the `Broad gate` cell each say it
holds one entry per run … pinned as gone/stands pairs*. `GATE_CARRIERS` has
eight tuples. The ninth carrier is the comment `new_broad_gate_file` writes
into `broad-gate.md` — the seventh item of `spec.md:187-193`'s list — which
is code, is not in the module, and is pinned by no test (executed: `grep`
over `tests/` for its wording hits nothing). The record's 🟡 2 grounds at
`rounds/round-1.md:36`, *pins the nine carriers as gone/stands pairs*, is
the same count. Paperwork, no id: eight documents are pinned, the ninth
carrier is the comment, and it is one of the four sentences 🟡 1 names.

## Regression tests to plant

| Test | Destination |
|---|---|
| a re-seal at the same commit against another base keeps both entries (with 🟡 1's fix); the existing replace case re-seals against the same base | `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry` |
| the comment `new_broad_gate_file` writes says one entry per run, newest first, and no earlier run is erased | `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside `test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list` |

## Facts for the evidence ledger

- A9's clause, once 🟡 1 lands: the replace is keyed on the whole entry —
  commit and base — not on the commit alone; and the four carrier sentences
  are true of the code again.
- A11's clause: eight documents pinned as gone/stands pairs; the ninth
  carrier is the `broad-gate.md` comment, pinned by the seal module or not
  at all.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a re-seal at the commit the newest entry names erases that entry, base included, while `agents/sealer.md` (twice), `docs/review-chain-spec.md` and the `broad-gate.md` comment say a second run never erases the first; the sealer's own binding is commit AND base | `skills/code-review/scripts/round_record.py:376-381`, `:4259-4261`; `agents/sealer.md:141`, `:186-188`; `docs/review-chain-spec.md:341-343`; `templates/sdd-round.md:39` | open | read — the four sentences against the replace at `:381`; executed — m2 shows the replace is what the case pins, and the case's own shape is a different base |
| ⬜ 2 | the `skills/verify/SKILL.md` stands phrase `earlier run` stood in that file at `0b8dc4b2` under §Counterfeits, so the pair's present half pins nothing of the rewrite for that carrier | `tests/test_the_broad_gate_cell_keeps_every_run.py:54-58`; `skills/verify/SKILL.md:456`, and `:783` at the base | open | executed — the phrase is present at the base for this carrier alone; read — the file's new line carries `; earlier run: <sha> vs base <sha>` |
| ⬜ 3 | `kept_broad_gate`'s docstring says the caller resolved the value; `close --broad-gate` never resolves its flag | `skills/code-review/scripts/round_record.py:367-368`, `:4554` | open | read — no SHA check in `close` over `:3824-4182`; `seal` refuses at `:4467-4472`; behaviour unchanged from before the fix |
| ⬜ | A11 and round 1's 🟡 2 grounds say nine documents are pinned; `GATE_CARRIERS` pins eight, and the ninth carrier is the comment `new_broad_gate_file` writes, unpinned | `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:22`; `seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/rounds/round-1.md:36` | correction | read — `spec.md:187-193` lists the comment as the seventh carrier; executed — no test greps its wording |
| 🟢 | round 1's 🟡 1 — `kept_broad_gate` is the one cell-writing path for `seal` and `close --broad-gate`, and the template and orchestration say so | `skills/code-review/scripts/round_record.py:347-385`, `:3936-3943`, `:4499`; `templates/sdd-round.md:39`; `skills/code-review/orchestration.md:535-539` | verified | executed — m1 and m3 red at their cases, the close module green; read — no other writer of the cell |
| 🟢 | round 1's 🟡 2 — the ninth carrier in `agents/warden.md` §Role is rewritten and the eight documents are pinned as gone/stands pairs, each gone sentence the carrier's own at `0b8dc4b2` | `agents/warden.md:320-325`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | verified | executed — every gone sentence present at the base and absent at the target, every stands phrase present at the target; m6 red on the gone half; ⬜ 2 and the correction narrow the claim, not the fix |
| 🟢 | round 1's 🟡 3 — a repeated header row is skipped by `table_body` and by `chain_check.verdict_table`, and the rows under it are carried | `skills/code-review/scripts/round_record.py:1128-1139`; `skills/code-review/scripts/chain_check.py:1574-1580` | verified | executed — m4 and m5 red at their cases; read — the generator compares exactly and the checker casefolded, and the generator's first-header refusal makes the difference unreachable |
| 🟢 | round 1's ⬜ 4, 6 and 7 — both enders named, the aggregate sourced to #437 in both files, the three-places module says what it counts | `agents/warden.md:466-469`; `docs/review-chain-spec.md:979-985`; `skills/code-review/SKILL.md:329-334`; `tests/test_the_report_standard_is_one_in_three_places.py:1-6` | verified | read — the diff at each coordinate |
| 🟢 | round 1's ⬜ 5 — a running walk of two reports the gate's refusal; `reaches 2` on the remaining branch is right by construction | `skills/code-review/scripts/round_record.py:2136-2153`; `floor_and_fixes` | verified | executed — m7 red at `test_the_count_walks_message_says_records_when_it_counted_two`; read — `fires` admits a running walk only at `spent >= 1` |
| 🟢 | round 1's ⬜ 8 — the same-commit replace is implemented and pinned as the record says; whether it should be is 🟡 1 | `skills/code-review/scripts/round_record.py:376-381`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2555-2577` | verified | executed — m2 red at the replace case and green at the different-commit case |
| 🟢 | the fix range touched nothing outside the eight findings and the ledger re-reads; the 29 re-read rows and A9, A10 state what the landed code does | `git diff --stat 83988abd..21b8d61e`, fifteen files; `seal/ledger.md`; `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:20-21` | verified | read — every hunk maps to a finding; executed — `evidence-check --strict` 1622 ok, 0 drifted, 0 broken; `seal`'s `raise Refused` sites counted at six |
| 🟢 | the new units as code — `kept_broad_gate`, the two header skips, the `bound_line` guard, `ROOT`, `GATE_CARRIERS`, `flat` and the four cases — are correct, with 🟡 1, ⬜ 2 and ⬜ 3 as the exceptions above | `skills/code-review/scripts/round_record.py:347-385`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | verified | executed — the six modules, 506 passed; read — `flat` collapses whitespace so a wrapped sentence matches, `ROOT` resolves from the test file |
| 🟢 | round 1's nine 🟢 rows stand; the three the fix range touched (phases 1, 2 and 4) were re-derived by the modules above | `rounds/round-1.md` | confirmed | executed — the generator, checker, close and seal modules at the target; read — the other six cover code the fix range did not touch |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict` over the tree the sealer stands on, taken once after the rounds settle | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; the hand-back labelled it `unverified`; this round's `evidence-check` and per-file ruff are probes over the clone, not the gate |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_record_is_generated.py tests/test_chain_check_at_the_pull_request.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_the_report_standard_is_one_in_three_places.py -q` in the clone at `0d3a9fb4` | `506 passed in 343.29s`; the exit code was read through a pipe and is not claimed |
| m1 — `close` builds the cell from `args.broad_gate` alone (`kept_broad_gate(...)` replaced by the flag) | `test_close_broad_gate_keeps_a_run_the_cell_already_holds` 1 failed, exit 1 |
| m2 — `entries = entries[1:]` replaced by `pass` (the same-commit rule dropped) | `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry` 1 failed, exit 1; `test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest` 1 passed, exit 0 |
| m3 — `kept_broad_gate` returns `value` unconditionally | seal module `-k re_seal` 3 failed, 3 passed, exit 1; the close case 1 failed, exit 1 |
| m4 — `table_body`'s `!= header` clause removed | `test_a_second_tables_header_under_a_subheading_is_not_a_verdict_row` 1 failed, exit 1 |
| m5 — `verdict_table`'s casefolded header skip replaced by `if False:` | `test_a_repeated_header_row_is_not_a_verdict_row` 1 failed, exit 1 |
| m6 — `skills/verify/SKILL.md` given back *one SHA with the base it was compared against* | `test_no_carrier_still_describes_the_cell_as_one_run` 1 failed, exit 1; `test_every_carrier_says_the_cell_holds_one_entry_per_run` 1 passed, exit 0 |
| m7 — `bound_line`'s guard back to `if not running:` | `test_the_count_walks_message_says_records_when_it_counted_two` 1 failed, exit 1 |
| after every mutation `git checkout --` on the file; `git status --porcelain` in the clone | clean |
| a script over `git show 0b8dc4b2:<carrier>` and `flat` for each `GATE_CARRIERS` tuple: gone sentence at base / at target, stands phrase at base / at target | gone: present at base and absent at target for all eight; stands: present at target for all eight, and present at the base for `skills/verify/SKILL.md` alone |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone, exit read directly | exit 0 — `total: 1622 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm 0 refused, 0 drifted |
| `uvx ruff check` and `uvx ruff format --check` over the eight `.py` files the fix range edited, exits read directly | exit 0 and exit 0 |
| `awk` count of `raise Refused` inside `seal` at `0b8dc4b2`, `e3cc83c9` and the target | six sites at each (the seventh hit is the docstring sentence that names the count) |
| `grep -rn "newest first\|earlier run\|new_broad_gate_file" tests/` | three docstrings and one unrelated line; nothing pins the `broad-gate.md` comment |
| this report through `round_record.py new --round 2 --target 0d3a9fb4… --baseline 0b8dc4b2` in the clone, then `evidence-check --strict` with the report in place; the record it wrote and its reach-back into `round-1.md` were undone in the clone (the worktree's record is the orchestrator's to write) | `new` exit 0 — `Pass` unticked over 🟡 1, both terminal lines copied as values, 14 verdict rows and all eight fenced blocks carried, the bound printed as `one reopening remains`; `evidence-check` exit 0, 1622 ok, 0 refused with the report's names read |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` at the tree the sealer stands on | not yet |

## Paste-ready fixes

### 🟡 1 — skills/code-review/scripts/round_record.py

The helper, placed above `kept_broad_gate`; the replace keyed on it; the
docstring paragraph rewritten to say what it now does.

```python
def same_run(entry, value):
    """Whether `entry` and `value` record one run: the same commit AND the
    same base. A SHA-shaped word is compared by prefix, so an abbreviated
    entry and a full-length flag agree; every other word exactly. Two runs
    at one commit against different bases are two comparisons —
    `agents/sealer.md` binds a seal to both halves — and both are kept.
    """
    a, b = entry.split(), value.split()
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if chain.SHA_RE.fullmatch(x) and chain.SHA_RE.fullmatch(y):
            if not (x.startswith(y) or y.startswith(x)):
                return False
        elif x != y:
            return False
    return True
```

```python
    entries = held.split(EARLIER_RUN)
    if same_run(entries[0], value):
        entries = entries[1:]
    if not any(chain.SHA_RE.search(e) for e in entries):
        return value
    return EARLIER_RUN.join([value, *entries])
```

```python
    **A run the newest entry already records — the same commit against the
    same base — replaces that entry rather than standing beside it** (round
    1's ⬜ 8, narrowed by round 2's 🟡 1). It is the same claim about the
    same comparison — the sealer re-run over an unchanged checkout — and
    two entries for one claim would make the count of entries stop being
    the count of runs. A run at that commit against ANOTHER base is another
    comparison and is kept behind the new entry like any earlier run, which
    is what `agents/sealer.md` and the `broad-gate.md` comment promise. The
    comparison is by prefix per SHA-shaped word, so an abbreviated entry and
    a full-length flag name one commit; nothing here asks git.
```

### 🟡 1 — tests/test_the_seal_is_taken_once_by_the_sealer.py

The existing replace case re-seals against the same base; a new case pins
the other base kept.

```python
    code, out = run_seal(repo, f"{second} against base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_a_same_commit_re_seal", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{second} against base{generator.EARLIER_RUN}{first} against base"
    ), cell
    assert cell.count(second) == 1, "the same commit was entered twice"
```

```python
def test_a_re_seal_at_the_same_commit_against_another_base_keeps_both(repo):
    """Round 2's 🟡 1. The seal is the commit AND the base (`agents/sealer.md`
    §Bind the result to a tree state), so a run at one commit against a
    moved base is a second comparison and stays beside the first rather
    than replacing it — the erasure #174 was filed on, one field narrower."""
    _one, two = settled_item(repo)
    sha = short(repo, "HEAD")
    assert run_seal(repo, f"{sha} against base")[0] == 0
    code, out = run_seal(repo, f"{sha} against origin/base")
    assert code == 0, out
    generator = _load("specseal_round_record_for_another_base", GENERATOR)
    cell = fields(two.read_text(encoding="utf-8"))[ROW]
    assert cell == (
        f"{sha} against origin/base{generator.EARLIER_RUN}{sha} against base"
    ), cell
```

### 🟡 1 — templates/sdd-round.md

Inside the `Broad gate` row's comment, replacing *and a run at the commit
the newest entry already names replaces that entry rather than duplicating
it*.

```markdown
and a run the newest entry already records — the same commit against the same base — replaces that entry rather than duplicating it, while a run at that commit against another base is kept behind the new entry as any earlier run is
```

### ⬜ 2 — tests/test_the_broad_gate_cell_keeps_every_run.py

```python
    (
        ("skills", "verify", "SKILL.md"),
        "; earlier run: <sha> vs base <sha>",
        "one SHA with the base it was compared against",
    ),
```

### ⬜ 3 — skills/code-review/scripts/round_record.py

Replacing the docstring's last sentence, *nothing here asks git, because the
value has already been resolved by the caller that refuses an unresolvable
one*.

```python
    nothing here asks git: `seal` has already refused a flag that does not
    resolve, and `close --broad-gate` never resolves its flag, so a value
    with no SHA-shaped word is written as typed and left for
    `chain_check.broad_gate` to report at the pull request.
```

Needs a fix: yes — 🟡 1 (a same-commit re-seal erases the entry it replaces, base included, and four carrier sentences say a second run never erases the first; close it by keying the replace on commit AND base, or by rewriting the four sentences and A9 with grounds)
Loses a record or crashes: no — nothing found writes outside `seal/specs/` or raises; 🟡 1 drops one entry inside a cell the generator rewrites on purpose, a record kept short and not a record lost, and the run that wrote it is still named by the entry that replaced it

## Proof

Opened, in the clone at `0d3a9fb4` unless said otherwise:
`seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/rounds/round-1.md`,
`rounds/round-1-report.md`, `overview.md:24-34`, `spec.md:187-200`,
`phases/phase-4.md:20-30`; `skills/code-review/scripts/round_record.py`
(`kept_broad_gate`, `table_body`, `floor_and_fixes`, `bound_line`, `close`'s
head and cell wiring, `new_broad_gate_file`, `seal`'s head and tail, the
argparse rows); `skills/code-review/scripts/chain_check.py` (`field`,
`table_rows`, `verdict_table`, `says_gate_not_yet`, `SHA_RE`); the fix
range's diff over every one of its fifteen files, and the record commit's
diff; `agents/sealer.md:136-144`, `:183-190`; `docs/review-chain-spec.md:336-348`;
`skills/verify/SKILL.md:454-458`, `:781-785`; `bin/test`;
`.github/workflows/test.yml:24-26`; `seal/ledger.md` rows S6 (`:1942`), and
the fragment's A9–A11; `tests/test_the_broad_gate_cell_keeps_every_run.py`
whole. At `0b8dc4b2` through `git show`: the eight carriers and
`round_record.py`'s `seal`. Not opened: the survivor sweep's inputs, the
suite beyond the six modules.
