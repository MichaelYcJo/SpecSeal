# Review round 1 — `fix/299-a-ledger-row-that-will-not-parse-is-counted`

Target `7b14b1fb`, read against `origin/release/v0.15.4` (`7b557144`). The build
range is `0abfb371..7b14b1fb`, on the frame `7c912915` + `5f3c5654`. Probes ran
in a `git clone --no-local` at the target. This is a first round, so there is
no earlier `round-N.md` to take coordinates from. Q1 and Q2 belong to the owner
and are built on default (a). They are not reopened here.

## Summary

The arm does what the frame asked. `MALFORMED` is a verdict of its own. It is
counted on both totals lines, printed at zero, and exits 2 under either
reading. `--reverify` names each row it leaves and returns 1, and the commit
advisor prints a block. `ANCHOR_RE` and `resolve_unit` are byte-identical to
the base. The five live rows and the two extra ones in Notes cells now resolve
`OK`. Their claims hold against the code, and the rider-stamp claim that was
removed really was false. #322's claim of already fixed is true.

Two things are wrong, both in rule (a) of the arm:

- **The narrowing is keyed on the wrong feature (🟡 1).** It refuses prose in
  a code span, `` `#299` `` or `` `@cache` `` beside a good anchor, which exits 2
  in a repository that installs the update. It also lets through a coordinate
  written without backticks that is missing its hash.
- **The remedy text is wrong for one shape (🟡 2).** It tells a writer who
  left the hash off a quoted locator to escape a bare quote that is not there.

Two ⬜ findings cover the advisor block's wording and a repaired coordinate
that hashes 460 lines. One ❓ asks whether an empty `Code grounds` cell in a
row that makes a claim is meant to stay silent.

## Spec compliance

Each clause of `spec.md` §*In* was checked against the code, and each
scenario was checked against the case or run that holds it.

- **§In 1, the arm.** `malformed_rows` sits beside `old_format_rows` and is
  called third from `check_ledger` (`evidence_check.py:1364`). It reads through
  `unquoted` and only the `Code grounds` cell (`grounds_cells`, `:1606-1633`).
  Rule (a) was narrowed on purpose, and `overview.md` records it as a
  divergence. What the narrowing does in practice is finding 1.
- **§In 2, the totals.** Both lines end `· N old-format · N malformed`
  (`:2831-2841`), and `broad_gate.py#LEDGER_RE` still reads the unchanged
  prefix. Executed: `total: 2249 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0.
- **§In 3, exit 2 under both readings.** `exit_code` gives `MALFORMED` its own
  branch after `OLD-FORMAT` (`:2700-2701`), with the Q1 pointer in its comment.
  The lenient-run case file pins both readings.
- **§In 4, `--reverify`.** A `LEFT  <coord>  MALFORMED — <remedy>` line is
  printed for each row, the row is not rewritten, and the command returns 1
  (`:1920`, `:2048-2050`). The `--reverify` callers in the tree are
  documentation and the advisor's printed advice. No script branches on its
  return code, so the new 1 changes no caller.
- **§In 5, the advisor.** The filter holds three verdicts
  (`hooks/evidence-advisor.py:142`), the docstring says so, and `main` prints a
  block (`:184-194`). Its wording is finding 3.
- **§In 6, the live rows.** All seven are re-read below, under *The seven rows*.
- **§In 7, the documents.** `SKILL.md` has a `MALFORMED` verdict row, the
  `--reverify` sentence, the *Known limits* bullet and the `\"` sentence.
  `templates/ledger.md` has the `\"` sentence, and so does the comment above
  `ANCHOR_RE`.
- **§In 8.** The #299 row in `seal/follow-up.md` is removed.
- **§In 9, #322.** Read: `tests/test_a_row_points_by_content.py:827` is an
  `r"""` docstring, and it became one in `97e29b7a`. Executed: all 176 tracked
  `.py` files compile under `-W error` with 0 errors on Python 3.13.5. The
  smith's run used 3.12.11, so the claim now holds on two interpreters.
- **§Data & interfaces.** `ANCHOR_RE`: the base-to-target diff changes only
  the comment above it. The pattern and the name are unchanged. `resolve_unit`
  is not in the diff at all. The `seal/releases/0.4.0.md` row anchored at
  `resolve_unit@c6839923` still reads `OK` under `--strict`. Work item B's
  branch (`origin/fix/603-…`) does not edit `evidence_check.py` and cites no
  anchor in it. It loads the file by path, and nothing new runs at import.
- **Vendoring.** `vendored_split_row` is identical to `split_row` in
  `unverified_check.py:157-167`. `cell_rule` falls back the way `fence_rule`
  does, and a case holds the two splitters in step.
- **S1–S13.** Each has its case or run. S12 is confirmed by my own run. S13
  was read.

### The seven rows

| Row | Now | Claim re-read against |
|---|---|---|
| `seal/ledger.md`, the eval row: the `EXPANDS` coordinate | `OK`, 670-678 | `hooks/commit-review-gate.py:176-188`: `_eval_hides_a_commit` returns True for any character of `EXPANDS`. Holds |
| the same row: the fixture coordinate | `OK`, 79-119 | `tests/test_what_the_reader_understands.py:89` has the `("an eval", …)` tuple. Holds |
| `seal/ledger.md`, the separator row: `SEPARATORS` | `OK`, but the region is 347-807 | `chain_check.py:547` still opens with the space. Holds. The width is finding 4 |
| the same row: `CLOSED_WORDS` by name | `OK`, 410-418 | a multi-line set that now also holds `DEFERRED`. The quoted one-liner really is gone, so citing by name is right. Holds |
| `seal/releases/0.4.0.md`, the hygiene step | `OK`, 100-119 | `.github/workflows/hygiene.yml:116-119` exits 0 off `main` and runs `gather_changelog.py --check` on `main`. Holds |
| `seal/releases/0.12.0.md`, `claude_block.py` | `OK`, `TEMPLATE` 83 and `write` 193-205 | `TEMPLATE` names `templates/claude-md-block.md`, and `write` regenerates the region. Executed: `claude_block.py --check` exits 0. Holds |
| `seal/ledger.md`, the rider-stamp row (removed) | now in the fragment, 2 rows `OK` | the claim was *the SHA is an ancestor of HEAD*, and it is false. `tests/test_a_rider_reaches_its_file.py:181` keeps the SHA form only as `OLD_STAMP`, and `test_no_rider_stamp_names_a_commit` (`:204`) refuses any stamp that names a commit. Removing the row and writing a new one follows `CLAUDE.md`. `seal/releases/0.9.1.md:172`, the S1 row the new row points to, exists |

Executed: the arm run over the three ledger files as they stood at
`ca2afdb9` names exactly the five coordinates in `spec.md`, and nothing else.

## Quality

### 1. 🟡 Rule (a) refuses prose in a code span and misses a coordinate outside one

`skills/evidence-check/scripts/evidence_check.py:1682-1685`.

The narrowing treats code spans and bare words differently:

- **In a code span**, one mark is enough. A span holding a `#` or an `@` is
  refused.
- **In a bare word**, both marks are needed. A word is refused only if it
  holds `#` and `@`.

`overview.md` explains the narrowing with one example: `(#299)` beside a good
anchor must not turn an installing repository red on prose. It only protects
that example when the issue number is written without backticks. The
evidence is in the Executed probes table below, each row one cell next to a
good anchor.

**What is refused wrongly, exit 2 under both readings:**

- `` (`#299`) ``
- `` the `@cache` decorator ``
- `` owner `ops@example.com` ``

A Java or Spring repository that writes `` `@Transactional` `` in its grounds
cell is the realistic case. That repository gets a red build on update, and
the remedy line tells it the text "does not parse as `path#anchor@hash`".

**What is let through silently:**

- `src/service.py#Box` without backticks, which is a coordinate with no hash
- `b.py@abcdef12`, which has no locator
- `b.py#g>h`, a bare minor anchor

That is #299's own class. The suite pins the backticked form of the first
(`test_what_is_left_of_a_cell_is_read_span_by_span`, row A), so the two
halves of the cell disagree about the same text. Measured on this tree: no
Code grounds cell holds a leftover of either kind today. So this concerns
installing repositories, not this one.

The feature that tells a coordinate from prose is the shape of the mark, not
whether it sits in a span. A leftover is a coordinate if it holds both marks,
or if it has a `#` that opens a locator (a name, a quote or `<`). `#299` opens
no locator and `@cache` has no `#`. The fix below applies that one test to
spans and bare words alike and leaves URLs alone. I executed it in the clone:
the four modules the diff touches plus three probe cases gave 184 passed. The
three cases were red without it. Over this tree the fixed arm still reads
`0 malformed`. The one remaining gap is `b.py@abcdef12` beside a good anchor,
which has no locator. The fix does not reach it, because a reliable rule for
`@` alone would also catch `first.last@example.com`.

### 2. 🟡 A quoted locator with no hash is told to escape a quote that is not there

`evidence_check.py:1603`, `BARE_QUOTE_RE = re.compile(r'[#>]"[^"\n]*"(?![>@])')`.

The negative lookahead also succeeds at the end of the text. So a quoted
locator whose hash was left off is read as a bare quote. Executed:

- `a.py#"line"` gets *a bare `"` ends a quoted locator — write each one inside it as `\"`*
- `a.py#f>"g"` gets the same
- `a.py#"line">"claim"` gets the same

None of them holds a bare quote. The hash is what is missing. The verdict is
right, but the line a person acts on names the wrong repair, and contract §14
counts that line as behaviour. A forgotten hash is one of the two ends #299
measured, and a quoted minor anchor is the form `SKILL.md` asks for, so this
shape will come up. Requiring a character after the closing quote that is not
`>` or `@` fixes it, and every bare-quote case in the suite still matches.
This is in the same fix below, and it was seen red and then green the same
way.

### 3. ⬜ The advisor block's header and closing line misdescribe some rows

`hooks/evidence-advisor.py:184-194`.

The header reads *N ledger rows whose coordinate does not parse*, but:

- **N counts texts, not rows.** Two bad coordinates in one cell give 2, and
  one text repeated in two rows gives 1.
- **A rule-(b) row has no coordinate at all.** Its line says so, and the
  header contradicts it.

The closing line, *the hash as `@00000000`*, repeats the remedy that each
`MALFORMED` line already carries. For a bare-quote row whose hash is correct,
it also prescribes discarding that hash. The behaviour is right, so this is ⬜.
A header such as *N ledger coordinates nothing checks*, with no closing line,
would fit every shape. `tests/test_dispatch.py`'s case asserts `@00000000` and
`--reverify` on the output, and the per-row remedy still carries both.

### 4. ⬜ The repaired `SEPARATORS` coordinate hashes 460 lines

`seal/ledger.md:76`, the row's quoted-line coordinate for the
`SEPARATORS = " " + …` line, hash `3a4ffca3`.

This coordinate resolves to `347-807`. That is the whole stretch of
module-level code between two `def`s in `chain_check.py`, because a quoted
line at module level takes that stretch as its unit. Executed: the same row
cited as `chain_check.py#SEPARATORS` resolves to `547-547`.

As written, any new constant between those two `def`s drifts this row, and
`chain_check.py` gains constants in most work items. The same correction cites
`CLOSED_WORDS` by name for a different reason. `SEPARATORS` can be cited the
same way. The claim is true either way, so this is ⬜.

### ❓ An empty `Code grounds` cell in a row that makes a claim is still silent

Rule (b) requires the cell to be non-empty (`evidence_check.py:1690`).
`| A claim | | read | 2026-09-25 | |` is counted nowhere, and the totals read
clean. That is the shape #299 describes, and the owner's comment covers it:
*whatever the reason*. `spec.md` §In 1 (b) says "is not empty" in so many
words, so the build complies. The all-empty template row is already excluded
by the *other cell* condition. What the non-empty condition adds is a pass
for group-label rows (`| **Area** | | | | |`), which may be why the frame
wrote it. Measured on this tree: no such row exists. Whether the release
should stay silent there is the repository owner's call, not a finding.

## Executed and read, kept apart

- **Executed**
  - `evidence_check.py --strict .` at the target
  - the arm over the ledgers as they stood at `ca2afdb9`
  - the rows' status under `check_text`
  - `claude_block.py --check`
  - #322's compile under `-W error`
  - the boundary and remedy probes
  - the four touched modules through `bin/test`
  - the proposed fix, green with it and red without it
  - `SEPARATORS` resolved by name and by the quoted line
- **Read**
  - every hunk of `evidence_check.py`, `hooks/evidence-advisor.py`,
    `SKILL.md`, `templates/ledger.md` and the four test files
  - every ledger hunk, word by word
  - the code behind all seven rows
  - `spec.md`, `plan.md`, `questions.md`, `overview.md`, `survivors.md` and
    `changelog.md`
  - how `broad_gate.py#ledger_counts` is used
  - work item B's use of `evidence_check.py`
- **Unverified**
  - the full suite, repository-wide lint and typecheck. Answerer: the sealer,
    once, after the rounds settle
  - the smith's mutation claims in `phases/phase-2.md`. I did not repeat
    them. Answerer: nobody is owed this. It is recorded so nobody reads it as
    checked.

## Regression tests to plant

In `tests/test_a_row_points_by_content.py`, beside
`test_what_is_left_of_a_cell_is_read_span_by_span`. These are the three
probe cases, and all three were seen red at `7b14b1fb`:

- prose marks in spans beside a good anchor: 0 malformed, exit 0 (finding 1)
- a coordinate with no hash, written without backticks, is named (finding 1)
- a quoted locator with no hash gets the generic remedy, not the bare-quote
  one (finding 2)

The fenced blocks under *Paste-ready fixes* hold them.

## Facts for the evidence ledger

- A module-level quoted-line anchor resolves to the whole run of module-level
  statements between two `def`s. `chain_check.py`'s `SEPARATORS` line gives
  `347-807`, and the same constant by name gives `547-547`. This matters to
  any row repaired by escaping rather than naming.
- Rule (a) as built: a span needs one mark, and a word outside a span needs
  both (`evidence_check.py#malformed_rows`). If finding 1's fix lands, the row
  for `malformed_rows` in this work item's fragment is re-read against it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Rule (a) refuses a code span holding one mark (`` `#299` ``, `` `@cache` ``, `` `ops@example.com` `` beside a good anchor), which exits 2 on prose. It also lets through a coordinate outside backticks that has one mark (`src/service.py#Box`, `b.py#g>h`), which is #299's silence | `skills/evidence-check/scripts/evidence_check.py:1682-1685` | open | Executed probe in the clone. The fix below keeps 184 cases green, turns three probe cases from red to green, and the tree still reads 0 malformed |
| 🟡 2 | `BARE_QUOTE_RE`'s negative lookahead matches at end of text, so a quoted locator with no hash (`a.py#"line"`, `a.py#f>"g"`) is told to escape a bare quote | `skills/evidence-check/scripts/evidence_check.py:1603` | open | Executed: three shapes, each given the bare-quote remedy. §14: the remedy line is what a person acts on |
| ⬜ 3 | The advisor header says *rows whose coordinate does not parse*, but it counts texts, and a rule-(b) row has no coordinate. The closing line repeats the per-row remedy and prescribes `@00000000` for a bare-quote row whose hash is right | `hooks/evidence-advisor.py:184-194` | open | Read. The verdicts printed are right |
| ⬜ 4 | The repaired `SEPARATORS` quoted-line coordinate resolves to 347-807, so any module-level edit in `chain_check.py` drifts it. By name it resolves to 547 | `seal/ledger.md:76` | open | Executed: both resolutions. The claim holds either way |
| ❓ | Whether a claim row with an empty `Code grounds` cell should stay silent. Rule (b) requires a non-empty cell as `spec.md` §In 1 (b) says, and 0 such rows exist in this tree | `skills/evidence-check/scripts/evidence_check.py:1690` | ❓ out of verified scope | A product question behind the spec's wording, possibly there to spare group-label rows. Answerer: the repository owner |
| 🟢 | The five live rows and the two Notes coordinates parse and resolve, and each claim holds against its code | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.12.0.md` | confirmed | Executed: each reads `OK`. The code is read in the table above. `claude_block.py --check` exits 0 |
| 🟢 | The removed rider-stamp row's claim was false | `tests/test_a_rider_reaches_its_file.py:181`, `:204` | confirmed | A stamp names an anchor and a hash since #239. The SHA form survives only as `OLD_STAMP`, and a case refuses it |
| 🟢 | `ANCHOR_RE` and `resolve_unit` are unchanged, and work item B is unaffected | `skills/evidence-check/scripts/evidence_check.py:72-77` | confirmed | The diff touches only the comment above `ANCHOR_RE`. The `resolve_unit@c6839923` row reads `OK`, and B's branch cites and edits nothing in the file |
| 🟢 | Exit codes: `MALFORMED` is 2 with and without `--strict`, and `--reverify` returns 1 when it leaves one | `skills/evidence-check/scripts/evidence_check.py:2700-2701`, `:2050` | confirmed | Read. The cases in the lenient-run file and `test_reverify_names_a_malformed_row_and_leaves_it` passed in my run |
| 🟢 | #322 is already fixed | `tests/test_a_row_points_by_content.py:827` | confirmed | An `r"""` docstring since `97e29b7a`. 176 files compile under `-W error` with 0 errors on 3.13.5 |

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py --strict .` at `7b14b1fb` | `total: 2249 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed`, exit 0 |
| `malformed_rows` over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` as at `ca2afdb9` | the five coordinates `spec.md` lists and no others |
| `check_text` on the seven repaired coordinates and the fragment's two rider rows | all `OK`, regions as in *The seven rows* |
| `claude_block.py --check` | exit 0 |
| every tracked `.py` compiled under `-W error`, Python 3.13.5 | 176 files, 0 errors |
| `malformed_rows` on 20 single-cell shapes beside or without a good anchor | `` `#299` ``, `` `@cache` ``, `` `ops@example.com` `` refused beside a good anchor. `b.py#g`, `b.py@abcdef12` and `b.py#g>h` outside backticks not refused. `(#299)` outside backticks not refused |
| `malformed_remedy` on quoted locators with no hash | `a.py#"line"`, `a.py#f>"g"`, `a.py#"line">"claim"` and `#"line"` all get the bare-quote remedy |
| Leftover marks in every Code grounds cell of this tree's ledgers | none in either shape |
| Claim rows with an empty Code grounds cell in this tree | 0 of 806 rows read |
| `chain_check.py` `SEPARATORS` by name and by quoted line | `547-547` and `347-807` |
| `bin/test` on `test_a_row_points_by_content.py`, `test_evidence_check.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py` and `test_dispatch.py` | 181 passed, exit 0 |
| The same four modules plus three probe cases, with findings 1 and 2's fix applied | 184 passed, exit 0 |
| The three probe cases without the fix | 3 failed, exit 1 |
| `evidence_check.py --strict .` with the fix applied | 0 malformed. 1 drifted, the edited unit itself |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due when the rounds leave nothing open |

## Paste-ready fixes

### Findings 1 and 2 — `skills/evidence-check/scripts/evidence_check.py`

Replace `BARE_QUOTE_RE` and add the coordinate test beside it:

```python
# A quoted locator closed by its second `"` and then followed by something
# other than the `>` or `@` that must come next: the quote inside it was bare.
# At the end of the text the hash is what is missing, not a quote.
BARE_QUOTE_RE = re.compile(r'[#>]"[^"\n]*"(?=[^>@])')
# A leftover is a coordinate somebody wrote, not prose, when it holds both
# marks, or a `#` that opens a locator: a name, a quoted line, `<module>`.
# `#299` is an issue number and `@cache` a decorator, in a span or out of one.
LOCATOR_OPEN_RE = re.compile(r'#[A-Za-z_"<]')


def refused_coordinate(s):
    """True where S, left over after both patterns, is a coordinate."""
    if "://" in s:
        return False
    return ("#" in s and "@" in s) or bool(LOCATOR_OPEN_RE.search(s))
```

In `malformed_rows`, replace the two `refused` statements:

```python
        spans = [m.group(2).strip() for m in CODE_SPAN_RE.finditer(left)]
        words = CODE_SPAN_RE.sub(" ", left).split()
        refused = [s for s in spans + words if refused_coordinate(s)]
```

and the first bullet of its docstring:

```python
    - a coordinate the patterns refused: what is left of the cell once every
      `ANCHOR_RE` and `OLD_COORD_RE` match is blanked still holds a span or a
      word that holds both marks or a `#` opening a locator. An issue number
      `#299` and a decorator `@cache` are prose, in a span or out of one;
```

The cases, in `tests/test_a_row_points_by_content.py`:

```python
def test_prose_marks_beside_a_good_anchor_are_not_refused(repo):
    """An issue number, a decorator and an address in a code span are prose,
    exactly as `(#299)` outside one is; refusing them exits 2 on prose."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text()).group(0)
    ledger.write_text(
        f"| A | {good} (`#299`), the `@cache` decorator, owner `ops@example.com` |\n"
    )
    r = run(["."], str(repo))
    assert "0 old-format · 0 malformed" in r.stdout, r.stdout
    assert r.returncode == 0, r.stdout


def test_an_unticked_coordinate_with_no_hash_is_named(repo):
    """The same text row A of the span case names in backticks."""
    write_row(repo, "src/service.py", "handler")
    ledger = repo / "seal" / "ledger" / "f.md"
    good = re.search(r"`[^`]+`", ledger.read_text()).group(0)
    ledger.write_text(f"| A | {good}, src/service.py#Box |\n")
    r = run(["."], str(repo))
    assert "MALFORMED src/service.py#Box  " in r.stdout, r.stdout


def test_a_quoted_locator_with_no_hash_is_not_told_about_a_bare_quote(repo):
    """The hash is what is missing; the line must say so."""
    (repo / "seal" / "ledger" / "f.md").write_text(
        '| A | `src/service.py#"def handler"` |\n'
    )
    r = run(["."], str(repo))
    assert "MALFORMED" in r.stdout and "bare" not in r.stdout, r.stdout
    assert "@00000000" in r.stdout, r.stdout
```

Needs a fix: yes — finding 1 (rule (a) refuses prose in a code span and
misses a coordinate outside one) and finding 2 (a quoted locator with no hash
is told to escape a quote)
Loses a record or crashes: no

## Proof block

Files opened at `7b14b1fb` (clone) or in the work item's tree:

- `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/`:
  `spec.md`, `questions.md`, `plan.md`, `overview.md`, `survivors.md`,
  `changelog.md`
- `skills/evidence-check/scripts/evidence_check.py`: the diff, `:60-100`,
  `:1598-1700`, `:2685-2725` and `:2828-2870`
- `hooks/evidence-advisor.py`: `:1-50` and `:145-200`
- `skills/evidence-check/SKILL.md`: the diff, `:170-200` and `:540-570`
- `templates/ledger.md`
- `skills/verify/scripts/unverified_check.py:157-187`
- the diff of `tests/test_a_row_points_by_content.py`,
  `tests/test_dispatch.py`, `tests/test_evidence_check.py` and
  `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`
- the word diff of every ledger file in the range
- `hooks/commit-review-gate.py:176-200` and `hooks/cmdline.py:678-683`
- `tests/test_what_the_reader_understands.py:89`
- `skills/code-review/scripts/chain_check.py:345-349`, `:410-418` and `:547`
- `.github/workflows/hygiene.yml:98-120`
- `.github/scripts/claude_block.py:80-85` and `:190-206`
- `tests/test_a_rider_reaches_its_file.py:181-223`, by grep
- `skills/code-review/scripts/broad_gate.py:224`, `:1889-1891` and
  `:1940-1960`
- the `survivor_check.py` of work item B's branch, by grep
- `bin/test`
