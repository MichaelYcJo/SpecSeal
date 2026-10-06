# Round 5 report — 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer

| Field | Value |
|---|---|
| Target SHA | e8f767ec9748ffc28208f6ff83fc60c2fa8181b4 |
| Base | `origin/release/v0.19.0` (4b363e68) |
| Pull request | #828 |
| Round kind | verifying round of round 4's fix range `2e211cc6..23c230fe` (3 commits), and of the units its `New units` row names: `PATH_FORM_RE`, `CODE_SPAN_RE`, `CLAUSE_END`, `path_forms` |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Round 4's three fixes hold. A landing is now read only from a token that is
wholly a path form, every shape the records write still lands, the depth walk
reads as it did, and the reframed-record case now sees the guard it pins.
Q6's replay reproduces at 26, all at round 3, and it gives the same landings
on every record pair with the code before the fix and after it (executed).

One note remains, and it commissions nothing:

```
path_forms ── the whole-token reading the fix pass added
   ├─ round 4's three yellows ── closed (executed, each red when its fix is undone)
   └─ ⬜ 1  a path form followed by a member or a parameter
           (`mod.py::u::inner`, `mod.py#u.attr`, `mod.py::u[a-b]`) is no
           longer read, so round 4's confirmation that a class method lands on
           its class no longer holds; the documents' whole-token sentence
           already implies it, and nothing names or pins it
```

This round opens nothing that lands in a unit round 4's fixes added or
changed with a severity that commissions a fix, so its `Fix of a fix` row
should read `no`.

## What the account claimed, and what was found

The fix commits, the ledger's A8 note and the Q6 note make six claims. Each
was checked against the code.

- **"`landings` reads only tokens that are wholly a path form."** True.
  `landings` calls `location_units(…, paths_only=True)`
  (`skills/code-review/scripts/round_record.py:2438`), which returns
  `path_forms` at once (`round_record.py:4003`). `path_forms` takes each code
  span's whole content and each whitespace-separated word outside the spans,
  strips clause punctuation and an unmatched parenthesis, and keeps a token
  only where `PATH_FORM_RE.fullmatch` matches it (`round_record.py:4036-4042`).
- **"Five new S5 shapes are red at `2e211cc6`."** True (executed). At
  `2e211cc6` all five read `first`. At the target all five read `no`. With
  the `paths_only` switch disabled, the five S5 parameters fail and nothing
  else in the two location cases does.
- **"The reframed-record case is red with the guard off."** True (executed).
  With `previous_pair == stopped` disabled in `build`, the `touched=True`
  parameter fails. With the guard restored it passes.
- **"Through mutation, the whole-token match and the parenthesis rule are
  red."** True for the two I ran. `fullmatch` turned into `search` fails the
  three tail parameters. The parenthesis count dropped fails `mod.py#u()`.
  The claims for "the words outside spans" and "the line range" were read and
  not executed.
- **"Q6 re-run: 26 stops."** True (executed, method below).
- **"The depth walk's reading is unchanged."** True. Read: the only change to
  `location_units` is an early return behind `paths_only`, which defaults to
  `False`. Its other caller, the depth walk at `round_record.py:4163`, passes
  no flag. `LOCATION_UNIT_RE`, `LOCATION_LINE_RE` and `FRAGMENT_RE` are
  untouched. Executed: the depth and framer modules pass (43 passed).

## What lands nowhere, and what still lands

Executed in one probe over the module's two-round fixture, once at the target
and once at `2e211cc6`. In that fixture `u` changed, `w` was added and `v`
was only re-commented.

| Shape | At `2e211cc6` | At the target |
|---|---|---|
| `#w` apart from its path: `` `mod.py#v`; see #w ``, `` `f.py#x` and `#w`, beside `mod.py#v` ``, `` `mod.py#v` #w ``, `` `mod.py#v`, `#w` `` | `first … mod.py#w` | `no` |
| a tail joined by `\` or `+`, in a span or bare: `pkg\mod.py:5`, `a+mod.py:5`, `pkg\mod.py#w` | `first` | `no` |
| other joins: `=mod.py#w`, `'mod.py#w'` in a span, `x,mod.py#w` | `first` | `no` |
| a path with a space inside one span: `` `my mod.py:5` `` | `first` | `no` |
| the five the prompt names: `mod.py:4-5`, `./mod.py:5`, `mod.py#u()`, `mod.py:5, the return value`, `the return value (mod.py:5).` | `first` | `first` |
| `mod.py:5`, `mod.py#u`, `mod.py::u`, `mod.py#w` bare, `mod.py#u@<hash>`, an en-dash range, `` (`mod.py:5`) ``, `` **`mod.py:5`** ``, `see mod.py:5.`, two forms in two spans | `first` | `first` |

A path with a space written outside any code span is two words, and its tail
is a word of its own. `my mod.py:5` written bare reads `first … mod.py#u` at
the target (executed). No reader can tell that word from `see mod.py:5`. A8
scopes its claim to "a space inside one code span", and round 4 named the same
residue, so this is not a finding.

### ⬜ 1 — a path form followed by a member or a parameter is no longer read

`PATH_FORM_RE` allows a line range after `path:line`, and `()` and `@hash`
after `path#unit` or `path::unit`. Nothing else may follow
(`skills/code-review/scripts/round_record.py:2957`). So these shapes, which
the reading before the fix placed in the unit named first, now land nowhere
(all executed, `first` at `2e211cc6` and `no` at the target):

- a class method: `mod.py::u::inner`, `mod.py#u.attr`;
- a parametrized test id: `mod.py::u[a-b]`;
- a ledger minor anchor: `mod.py#u>return`;
- a line and column, `mod.py:5:9`, and `mod.py:5 (u)` in one span;
- two forms in one span, `` `mod.py:5, mod.py:13` ``, and `` `mod.py#u, #w` ``;
- `[mod.py:5](https://example.com/mod.py#L5)`, `**mod.py:5**`, `mod.py:5/13`
  and `mod.py:5—the return`, each written bare.

Two of these contradict a record. Round 4 confirmed in a 🟢 row that
"a class method as `c.py::C::m`, `c.py#C.m` or `c.py:3` lands on `C`". After
the fix only `c.py:3` does.

Why this is a ⬜ and not a 🟡: the behaviour matches the documents and the
direction the spec chose. `docs/round-record-spec.md` now says "the form is a
whole token", and `mod.py::C::m` is a whole token that is not the form. A
miss is the permissive direction the spec states for anything the reader
cannot place. The corpus does not use any of these shapes. Every 🔴 and 🟡
row in 529 distinct round records and reports, at the four `v0.18.x` tags,
the 138 pull request heads and the target, was read: 820 rows. Exactly one
cell loses a pair under the whole-token reading. It is the fragment cell round
4 already found (`settle.py#RULE_BASE_HEADING`, `#report`, …, a round-1
report at `v0.18.0`), which the fix meant to drop (executed).

What is wrong is that nothing says it. A reviewer reading `path::unit` in the
spec and the changelog has no way to learn that a pytest id of a class method
counts for nothing, and no case pins either answer. The fence below names it
and pins it in the direction the fix pass took. Widening `PATH_FORM_RE` to
accept a trailing member is the other answer. It is a new suffix rule, which
is the kind of reading the reframe declined.

## Answered and confirmed

- **Round 4's yellow 1 is closed.** A `#name` apart from its path places
  nothing, whatever path stands beside it (executed, four shapes above).
- **Round 4's yellow 2 is closed, and its class with it.** A path that is the
  tail of a longer token lands nowhere, for `\`, `+`, `=`, a quote, a comma
  and a space inside a span (executed). Undoing the whole-token match turns the
  three tail parameters red (executed).
- **Round 4's yellow 3 is closed.**
  `test_a_reframed_record_is_written_and_starts_the_count_at_no` locates its
  finding at `mod.py#u` and fails with the guard off (executed).
- **Q6 is still 26.** The phase-6 method was replayed in a scratch bare clone
  with the 138 pull request heads and the four tags. Every `round-K.md` with a
  `round-(K-1).md` beside it was read, closed fix verdicts reopened, and
  `landings` asked. Over the four tags: 36 work items reach `first` and 26
  reach `second`, all at round 3. #814 (`1791180640`) reads `first` at round 2
  in `compare_at_base`, `proof_refused` and `COMPANY`, then `second` at round
  3 in `proof_refused`. #801 (`1791163980`) reads `first` then `second`, both
  in `reverify`. The same replay run with `round_record.py` at `2e211cc6`
  gives identical landings on all 164 distinct record pairs, across all 142
  refs (executed).
- **The documents are right.** `docs/round-record-spec.md`'s new sentence,
  the changelog fragment's paragraph, ledger A8's claim and its `Corrected`
  note, the Q6 note, and the docstrings of `landings`, `location_units` and
  `path_forms` each say what the code does (read). The spec document is 994
  lines, under the 1000 ceiling. `evidence-check --strict .` exits 0 with 0
  drifted and 0 broken. `correction-check` over the base range exits 0, and
  no released ledger file changed (executed). One omission, read: the
  `path_forms` docstring says a word has `CLAUSE_END` stripped. It does not
  say that a leading `(` and an unmatched closing `)` are stripped too. The
  comment above `CLAUSE_END` carries the second, and nothing carries the
  first. This reads short. It is not wrong.
- **The work item's `spec.md` was not changed by the fix range.** Its reading
  paragraph and S5 still name the three forms without "whole token". That is
  consistent with the new reading, which is narrower and never wider, so it
  is not a correction.

## Regression tests to plant

- `tests/test_a_fix_of_a_fix_is_counted.py`, S5's parameter list: the two
  shapes in the fence below, if ⬜ 1 is answered by naming the narrowing. Both
  read `first` at `2e211cc6` and `no` at the target (executed), so they pin the
  whole-token rule against a reading that searches inside a token.

## Facts for the evidence ledger

- A8, if ⬜ 1 is answered by naming: a form followed by a member or a
  parameter (`path::C::m`, `path#C.m`, `path::case[a]`) is no form, and a
  line inside a method still lands on its class.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | A path form followed by a member or a parameter (`mod.py::u::inner`, `mod.py#u.attr`, `mod.py::u[a-b]`) is no longer read, so round 4's confirmation that a class method lands on its class no longer holds; no document names it and no case pins it | `skills/code-review/scripts/round_record.py#path_forms` | open | executed: each such shape `first` at `2e211cc6` and `no` at the target; matches the whole-token sentence and the permissive direction; corpus scan, 820 fix-owing rows, none uses it |
| 🟢 | round 4's yellow finding 1 is closed — a `#name` apart from its path lands nowhere | `skills/code-review/scripts/round_record.py#path_forms` | confirmed | executed: four fragment shapes `no` at the target, `first` at `2e211cc6`; with the switch off the five S5 parameters fail |
| 🟢 | round 4's yellow finding 2 is closed — a path that is the tail of its token lands nowhere, for a backslash, a plus, a space inside a span and three more joins | `skills/code-review/scripts/round_record.py#PATH_FORM_RE` | confirmed | executed: `fullmatch` as `search` fails the three tail parameters; a bare path with a space is two words, which A8 scopes out |
| 🟢 | round 4's yellow finding 3 is closed — the reframed-record case sees the `previous_pair == stopped` guard | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_reframed_record_is_written_and_starts_the_count_at_no` | confirmed | executed: guard off, the touched parameter fails; restored, it passes |
| 🟢 | every shape the records use still lands — the five the prompt names, the three plain forms, `./`, `@hash`, an en-dash range, a form in parentheses, in bold or bare | `tests/test_a_fix_of_a_fix_is_counted.py#test_a_location_carrying_its_py_path_still_lands` | confirmed | executed: the shape probe and the module, 58 passed; the parenthesis count dropped fails `mod.py#u()` |
| 🟢 | the depth walk's reading is unchanged | `skills/code-review/scripts/round_record.py#location_units` | confirmed | read: an early return behind a flag only `landings` passes; executed: the depth and framer modules, 43 passed |
| 🟢 | Q6 is still 26, all at round 3, with #814 and #801 first then second | `seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/questions.md` | confirmed | executed: replay over the four tags with 138 pull request heads; identical landings before and after the fix on 164 record pairs |
| 🟢 | the round-record spec, the changelog, ledger A8 and the docstrings say what the code does | `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` | confirmed | read: each against the code; executed: evidence-check and correction-check exit 0, freeze diff empty |

## Paste-ready fixes

### ⬜ 1 — name the narrowing, and pin it

`docs/round-record-spec.md`, §*A fix of a fix — `Fix of a fix`*, the second
and third sentences of the first paragraph:

```markdown
unit has not changed. The form is a whole token, a code span or a word: a path
that is the tail of a longer token, a form with a member or a parameter after
its unit (`path::C::m`, `path#C.m`, `path::case[a]`), and a `#name` apart from
its path, are no form; a line inside a method, `path:line`, lands on its class.
```

Two parameters for `test_a_location_that_lands_in_no_written_unit_reads_no`,
after the three tail shapes:

```python
        # Round 5's note 1: a form with a member or a parameter after its
        # unit is a whole token that is not the form, so it lands nowhere.
        "`mod.py::u::inner`",
        "`mod.py::u[a-b]`",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_fix_of_a_fix_is_counted.py` at the target, in the round-5 scratch clone | 58 passed, exit 0 |
| A test_tmp shape probe, 48 `Location` shapes over the module's two-round fixture, at the target and in a second clone at `2e211cc6` | exit 0 in both; the rows are the table under *What lands nowhere* and ⬜ 1 |
| `bin/test` on the two location cases and the reframed case, with the `previous_pair == stopped` guard off and `fullmatch` turned into `search` | 4 failed (the three tail parameters, the reframed case with `touched=True`), 33 passed, exit 1 |
| The two location cases with `paths_only` ignored | 5 failed (the five new S5 parameters), 30 passed, exit 1 |
| The keep cases with the parenthesis count dropped | 1 failed (`mod.py#u()`), 9 passed, exit 1 |
| A test_tmp Q6 replay, `round_record.py` at the target and at `2e211cc6`, in a bare clone with 138 pull request heads and the four tags | both: 164 record pairs, 3 unresolved, 2 refused; over the tags 36 reach `first`, 26 reach `second`, all at round 3; identical landings on every pair across all 142 refs |
| A corpus scan of the `Location` cell of every 🔴 and 🟡 row in 529 distinct round records and reports at the tags, the pull request heads and the target | 820 rows; one cell loses a pair under the whole-token reading, the round-1 fragment cell at `v0.18.0` |
| `bin/test tests/test_a_fix_pass_may_add_a_unit.py tests/test_the_chain_goes_back_to_its_framer.py` | 43 passed, exit 0 |
| `bin/evidence-check --strict .` at the target | exit 0, 0 drifted, 0 broken |
| `bin/correction-check --range 4b363e68...HEAD` | exit 0, no correction marker dropped, no released ledger file changed |
| `git diff --stat 4b363e68...HEAD -- seal/releases seal/ledger.md` | empty |
| `round-record new --round 5` from this report, in a fresh scratch clone at the target | exit 0; `Fix of a fix` reads `no`, `Needs a fix` and `Loses a record or crashes` read `no`, `Pass` unchecked while ⬜ 1 is open; round-4.md's `Fixes checked by` set to round-5. The generator's chain-check printed a notice that the changelog fragment predates `23c230fe`, a docstring-only commit, so the fragment still says what ships |
| The broad gate — the full suite, the repository-wide lint and the typecheck over the branch | not yet — the sealer's, once the rounds settle |

Every probe file, both scratch clones, the bare corpus clone and the
virtualenv built inside the clone were deleted before this report was written.

Needs a fix: no

Loses a record or crashes: no

With nothing open that needs a fix, the broad gate has come due: what comes
due is the sealer's spawn.

## Proof block

Opened in the round-5 scratch clone at the target:
`skills/code-review/scripts/round_record.py` (`landings`, `build`'s landing
block, the location regexes and the comments above them, `PATH_FORM_RE`,
`CODE_SPAN_RE`, `CLAUSE_END`, `tracked_at`, `resolve_path`, `location_units`,
`path_forms`, the depth walk's call, `verdict_rows`, `load`, `git`,
`read_text`, `COMMISSIONS_NOTHING`); `skills/code-review/scripts/chain_check.py`
(`table_rows`, `verdict_of`, `CLOSED_WORDS`);
`skills/verify/scripts/unverified_check.py` (`visible`, `readable`);
`tests/test_a_fix_of_a_fix_is_counted.py` (the fixtures, `two_rounds`, the S5
and S5b parameter lists, the reframed case);
`tests/test_the_record_is_generated.py` (`generate`); `bin/test`; the full
diff of `2e211cc6..23c230fe` and of `23c230fe..e8f767ec`. In the worktree:
`rounds/round-4.md`, `rounds/round-4-report.md`, `spec.md` (the reading, the
section on what round 3 moved, S5, S5b, data and interfaces),
`phases/phase-6.md`, `docs/round-record-spec.md` (the field section),
`skills/code-review/orchestration.md` (the rule's opening), and
`seal/config.md` (no `Record language` row).
