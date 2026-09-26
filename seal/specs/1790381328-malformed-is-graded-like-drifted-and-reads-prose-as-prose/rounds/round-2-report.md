# Round 2 report — 1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose

| Field | Value |
|---|---|
| Target SHA | `eb30a068` |
| Fix range verified | `d05cc2c3..6c260d34` (a0624b63 code and tests, 6c260d34 records); `eb30a068` only closes round 1's record |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 621 (draft, base `release/v0.15.5`, head `eb30a068`) |

This is the verifying round. Its target is the fix diff, not the branch.
Probes ran in a `git clone --no-local` of the worktree at `eb30a068`,
under this round's scratch directory, and the clone and every probe were
removed before handover. Nothing was written in the worktree except this
file.

I read round 1's record and report for coordinates. Every verdict below
is re-derived here.

## Summary

The fixes hold for every example round 1 named. The four reader modules
pass (227: round 1's 215 plus the fix's 12 new cases). All six new units
go red when their own claim is broken. `GLUED_MARKS_RE`'s new form gives
the same verdict as the old one on all 4 850 probe cells. Each of the
four grading sentences goes red when its base wording is restored.

Two classes are still not closed, and two ⬜ follow.

1. **The list of what rule (a) gives up is still narrower than the code
   (🟡 1).** A digit-opening locator with a path is silent whenever its
   hash is not glued to it, whitespace included:
   `docs/a.md#1-scope @abcdef12` in a code span. The base names it. The
   docstring says that class is silent "when no hash follows", and says
   the per-word rule still names a spaced hash when there is a path.
   Read together, the two sentences promise this shape is named, and it
   is not.
2. **Two of the four new pins do not go red when the grading changes
   (🟡 2).** The new case's docstring says a change to the grading "moves
   them or goes red". I put `MALFORMED` back to exit 2 under both
   readings and moved step 4 and the module docstring with it. The case
   stayed green, while the `--strict` flag row ("instead of 1") and the
   template comment ("softens drift and MALFORMED") had both become false.
3. **The search is not linear for every input (⬜ 3).** A chain of quoted
   strings holding escaped quotes, `#"\"` repeated, still costs quadratic
   time: 1.48 s at 20 000 characters and 5.94 s at 40 000. The comment,
   the ledger claim, the spec and the changelog all say "linear" or "no
   longer takes seconds" without that condition.
4. **One more pair of shapes the list does not name (⬜ 4).**
   `docs/a.md#²` and `docs/a.md#①` are silent at the base, because
   `str.isdigit` is true for them. They are named at the target, because
   `\d` does not match them.

## 🟡 1 — a digit-opening locator is silent whenever its hash is not glued, and the list says otherwise

`skills/evidence-check/scripts/evidence_check.py:1636-1639`, the
digit-locator sentence in `refused_coordinate`'s *What each edge gives up*.
The same "when no hash follows" wording is at `changelog.md:35` and
`spec.md:175` of this work item.

**What is wrong (executed).** I generated 2 425 shapes: 10 heads × 30
locators × 8 hash endings, plus 26 prose and edge shapes. I ran each one
through `malformed_rows` beside a good anchor, in a code span and as a
bare word, with the checker at `47e32d57`, `591c6cdf` and `eb30a068`.
589 cells are named at the base and silent at the target. I sorted all
589 into the classes the docstring states. Every one fits a stated class
except this one:

| Shape (in a code span, beside a good anchor) | Base | Target |
|---|---|---|
| `src/a.py#1-scope @abcdef12`, `src/a.py#1.2 @abcdef12`, `src/a.py#1장 @abcdef12`, `src/a.py#1>"x" @abcdef12` | named | silent |
| `src/a.py#12 @abcdef12`, `docs/a.md#12 @abcdef12` (digits only) | named | silent |

Same result with a short hash (`@abc`) and with `docs/a.md`, `a.b` or
`org/repo` as the head: 96 cells in all. They are silent because
`GLUED_MARKS_RE` cannot cross the space, and `ISSUE_TAIL_RE` takes the
locator as an issue number. The `@` word then has no path before it.

**Why it matters.** The docstring says the class is silent "when no hash
follows". Here a hash does follow, after a space. The next sentence says
that with a path, "the per-word rule still names" a coordinate with
whitespace between its marks. That holds for `src/a.py#handler @abcdef12`,
not for a digit-opening locator. So a reader of the docstring or the
release note believes this shape is still named. Round 1's 🟡 1 was this
same class: a stated trade narrower than the silence. And
`test_what_rule_a_gives_up_is_silent_and_says_so` says "the list cannot
go narrower than the code", which is true only for the shapes it lists.

**The fix.** State the condition the code actually has, *unless its hash
is glued to it*, and add the shape to `GIVEN_UP`. I applied both in the
clone. The new `GIVEN_UP` entry is red against the current docstring
(`1 failed, 12 passed`) and green with the new one (`13 passed`).
`changelog.md` and `spec.md` take the same wording as a correction to this
run's own records.

## 🟡 2 — the flag row's and the template's pins do not follow the grading

`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:456` and
`:464`, in `test_every_other_page_that_grades_the_flag_names_malformed`.

**What is wrong (executed).** Restoring each of the four base documents
alone turns the case red, so round 1's 🟡 2 is closed against someone
deleting the sentences. The case's docstring promises more than that:
"each is held against `exit_code` rather than against a number written
here, so the next change to the grading moves them or goes red". Two of
the four assertions do not read the grading in a way that can fail:

- The flag row checks `"malformed" in flag and f"exit {strict}" in flag`.
  The row says "drift and a malformed coordinate exit 2 … instead of 1".
  Under grading (a), `strict` is still 2, so the check passes while
  "instead of 1" is false.
- The template check is a fixed string, "softens drift … and MALFORMED,
  and nothing else", which does not depend on `lenient` or `strict`.

Mutant M12: `exit_code` put back to (a), with step 4 and the module
docstring changed to match. Result: `12 passed`. The two stale sentences
went unnoticed.

**Why it matters.** This is the failure the S6 pin's own docstring
records: the old `(exit 2, --strict or not)` row never went red when the
grading moved. Two of the four sentences are still in that position,
under a test that says they are not.

**The fix.** Two assertions, both taken from `grading`. With them the
same mutant is red (`1 failed, 12 passed`), and the case is green at the
target.

## ⬜ 3 — "the search stays linear" does not hold for chained quoted strings

`skills/evidence-check/scripts/evidence_check.py:1622-1625`. The same
claim is in the S8–S12 row of this work item's ledger fragment ("the
search stops each attempt at the next `#`, so it is linear"), at
`spec.md:137-138`, and in the changelog's last sentence.

**What is wrong (executed).** Taking `#` out of the unquoted class stops
an attempt at the next *unquoted* `#`. A `#` inside a quoted string does
not stop it. In `#"\"` repeated, every `#` sits inside a quote for every
attempt: the `\"` is an escape and the next `"` closes the quote. So each
attempt still runs to the end of the span.

| Input | `refused_coordinate`, before the fix | after the fix |
|---|---|---|
| `#a` × 10 000 (20 000 characters) | 4.19 s | 0.0009 s |
| `#"\"` × 5 000 (20 000 characters) | 1.55 s | 1.53 s |
| `#"\"` × 10 000 (40 000 characters) | 6.41 s | 6.06 s |

The time quadruples when the length doubles. `malformed_rows` over that
span in a cell takes 1.56 s. No ledger row comes near this shape, so
this is a claim to narrow and not a defect to ship a fix for, like
round 1's ⬜ 5. On correctness, the comment's other claim holds. I
checked it by reading and by execution: any string the new pattern
matches, the old one matches too. And any old match that crosses an
unquoted `#` is found again by the attempt that starts at the last such
`#`. The probe found no cell where `591c6cdf` and `eb30a068` disagree.

The ledger and spec halves are corrections to this run's own records.
The changelog sentence, "A span of many `#` characters no longer takes
seconds to read", is true only for `#` outside quotes.

## ⬜ 4 — a path followed by a lone superscript or circled digit is newly named

`skills/evidence-check/scripts/evidence_check.py:1617`, `ISSUE_TAIL_RE`.
At the base the check was `tail.isdigit()`, which is true for `²` and
`①`. So `docs/a.md#²` and `docs/a.md#①` read as issue numbers and were
silent. `\d` matches only decimal digits, so at the target they are named
(executed, beside a good anchor, in a span and as a bare word). Neither
`TAKEN_UP` nor the docstring says so. These shapes do not occur in a
`Code grounds` cell, and on a lenient run they only warn. I record it
because `TAKEN_UP` is meant to be the complete other direction of the
list, and these are the only newly named cells in the probe that no
stated rule explains. Every other newly named cell (138) is a dotless
name followed by `_`, `"` or `<`, which the docstring states as a rule.

## Round 1's findings, each answered

- **Round 1's 🟡 1.** Closed for its own shapes. `docs/a.md#1-scope`,
  `docs/a.md#1.2`, `src/a.py#1>"x"` and `#handler>"a"b"@abcdef12` are
  silent, listed and pinned. Mutants M1, M3 and M7 turn the matching
  `GIVEN_UP` parameters red. The class has one more shape, which is this
  round's 🟡 1.
- **Round 1's 🟡 2.** Closed against removal. M8–M11 each restore one base
  document or the docstring's old exit line, and each turns
  `test_every_other_page_that_grades_the_flag_names_malformed` red.
  `overview.md`'s divergence row is corrected. The part that does not
  follow the grading is this round's 🟡 2.
- **Round 1's ⬜ 3.** Closed. The code-span condition is stated in the
  comment at `:1622-1623`, in `malformed_rows`' docstring, in the
  opener-list case's docstring and in the S8–S12 claim. `spec.md:199`
  names the shape inside a span, which is correct.
- **Round 1's ⬜ 4.** Closed for its two shapes. `C#"hello"` and
  `vector#<T>` are listed and pinned (M2 and M6 red). The one leftover is
  this round's ⬜ 4.
- **Round 1's ⬜ 5.** Closed for its own input (`#a` repeated: 4.19 s
  before, 0.0009 s after). No verdict changed across 4 850 cells.
  `test_a_glued_mark_attempt_stops_at_the_next_hash` is red against the
  old pattern (M5). The remaining quadratic input is this round's ⬜ 3.

## Other super-linear paths — executed, not counted

`URL_RE` is the only other pattern `refused_coordinate` runs across a
whole string. It is quadratic on a long run of letters with no `://`:
0.56 s at 20 000 characters and 2.2 s at 40 000, with the same numbers at
`591c6cdf`. It dates from #299, is unchanged by this branch, and does not
set the cost. `malformed_rows` on the same cell takes 4.57 s, and 3.51 s
of that is `ANCHOR_RE` and `OLD_COORD_RE`, whose cost the rider on
`OLD_COORD_RE` already records. `ISSUE_TAIL_RE` and `PATH_HASH_RE` run
with `.match` once per word and backtrack at most once across it, so they
are linear (read; 20 000 digits in 0.0001 s, executed). Nothing here is in
the fix diff. It is recorded so the next reader does not have to measure
it again.

## Also read, not counted

- **Claims in both languages, by meaning.** I searched the tree for each
  changed sentence's claim: the trade shapes, "issue number" / "이슈
  번호", "linear" / "선형", "quoted string", "gives up" / "포기". The trade
  list appears only in the checker's docstring, this work item's
  `changelog.md`, `spec.md` and `overview.md`, the S8–S12 ledger row,
  earlier rounds' records, and the tests. No Korean copy exists. The
  linear claim appears in the four places named under ⬜ 3.
- **The windows-latest leg** was still pending on PR #621 at `eb30a068`
  when I read the checks. The other five checks pass.
- **`seal/releases/0.15.4.md`.** Its row's re-read note says
  `GLUED_MARKS_RE`'s change "changes no verdict". The probe agrees
  (4 850 cells, none different).

## Regression tests to plant

- `tests/test_a_row_points_by_content.py`, `GIVEN_UP`: add
  `"docs/a.md#1-scope @abcdef12"` (🟡 1). Shown red against the current
  docstring in the clone.
- `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`,
  `test_every_other_page_that_grades_the_flag_names_malformed`: the two
  assertions under 🟡 2. Shown red under mutant M12 in the clone.

## Facts for the evidence ledger

- The S8–S12 row of `seal/ledger/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose.md`:
  *so it is linear* needs the condition from ⬜ 3, "for a run of `#`
  outside quotes". Its Notes list of silences takes 🟡 1's shape once the
  docstring does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the list of what rule (a) gives up says a digit-opening locator is silent "when no hash follows" and that a path keeps a spaced hash named; with a path and a hash after whitespace (`docs/a.md#1-scope @abcdef12`, `src/a.py#12 @abcdef12`, in a span) the base names it and the target is silent | `skills/evidence-check/scripts/evidence_check.py:1638` | open | Executed: 2 425 shapes at `47e32d57` and `eb30a068`; 96 cells of this class named then silent, all other 493 given-up cells fit a stated class; the paste-ready `GIVEN_UP` entry is red against the current docstring and green with the new one. Same wording at `changelog.md:35` and `spec.md:175` |
| 🟡 2 | two of the four grading pins do not follow `exit_code`: the flag row is checked for `exit {strict}` only and the template comment against a fixed string, so a grading change leaves both stale and green, although the case's docstring says it goes red | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:456` | open | Executed: mutant M12 (grading back to (a), step 4 and the module docstring moved) leaves the case green; with the two paste-ready assertions it is red, and green at the target |
| ⬜ 3 | "the search stays linear" holds for `#` outside quotes only; `#"\"` repeated still costs quadratic time (1.48 s at 20 000 characters, 5.94 s at 40 000) | `skills/evidence-check/scripts/evidence_check.py:1624` | open | Executed: timing before and after the fix; no verdict differs across 4 850 cells. Same claim in the S8–S12 ledger row, `spec.md:137-138` and the changelog, each a correction to this run's own records |
| ⬜ 4 | `docs/a.md#²` and `docs/a.md#①` are silent at the base (`str.isdigit`) and named at the target (`\d`); `TAKEN_UP` and the docstring do not say so | `skills/evidence-check/scripts/evidence_check.py:1617` | open | Executed beside a good anchor, in a span and as a word; no such shape occurs in a `Code grounds` cell |
| 🟢 | round 1's finding 1 is closed for its own shapes — `docs/a.md#1-scope`, `docs/a.md#1.2`, `src/a.py#1>"x"`, `#handler>"a"b"@abcdef12` are silent, listed and pinned | `skills/evidence-check/scripts/evidence_check.py:1635` | confirmed | Executed: mutants M1, M3, M7 each turn the matching `GIVEN_UP` parameters red; the rest of the class is this round's finding 1 |
| 🟢 | round 1's finding 2 is closed against removal — each of the four sentences restored to its base wording turns the new case red, and `overview.md`'s row is corrected | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py:448` | confirmed | Executed: mutants M8–M11, each red; the part that does not follow the grading is this round's finding 2 |
| 🟢 | round 1's finding 3 is closed — the code-span condition is stated in the comment, `malformed_rows`' docstring, the opener-list case and the S8–S12 claim | `skills/evidence-check/scripts/evidence_check.py:1622` | confirmed | Read at `eb30a068`; executed: the unticked shape is silent and the ticked one named |
| 🟢 | round 1's finding 4 is closed for `C#"hello"` and `vector#<T>` — listed and pinned | `tests/test_a_row_points_by_content.py:1209` | confirmed | Executed: mutants M2 and M6 red; the leftover is this round's finding 4 |
| 🟢 | round 1's finding 5 is closed for its input — `#a` repeated reads in 0.0009 s where it took 4.19 s, and no verdict moved | `skills/evidence-check/scripts/evidence_check.py:1626` | confirmed | Executed: 4 850 cells identical at `591c6cdf` and `eb30a068`; M5 turns the stop-at-`#` case red; the remaining quadratic input is this round's finding 3 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the four reader modules (`test_a_row_points_by_content.py`, `test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `test_evidence_check.py`, `test_dispatch.py`) at `eb30a068` | 227 passed |
| `malformed_rows` over 2 425 shapes × {code span, bare word}, beside a good anchor, with the checker at `47e32d57`, `591c6cdf` and `eb30a068` | `591c6cdf` = `eb30a068` on all 4 850 cells; 589 cells named at the base and silent at the target, 138 the other way; unexplained by the lists: 🟡 1's 96 cells and ⬜ 4's two shapes |
| twelve mutants of the six new units and the four documents, one at a time, against the fix's 12 new cases | M1–M11 each red on the case that owns the claim; M12 (grading back to (a), step 4 and docstring moved) green: 🟡 2 |
| 🟡 1's and 🟡 2's paste-ready fixes applied in the clone | new `GIVEN_UP` entry red against the old docstring; all 13 cases green with the fix; M12 red with the fix |
| timing of `refused_coordinate`, `GLUED_MARKS_RE`, `URL_RE` and `malformed_rows` on 20 000 and 40 000 characters | as in ⬜ 3 and *Other super-linear paths* |
| `gh pr checks 621` at `eb30a068` | lint, ledger, release, ubuntu, macos pass; windows-latest pending |
| the broad gate (full suite, repository-wide lint, typecheck) | not yet: nobody has run it on this branch. It is the sealer's, and it is not due while 🟡 1 and 🟡 2 are open |

## Paste-ready fixes

### 🟡 1 — `refused_coordinate`'s docstring, lines 1635-1640

```python
    What each edge gives up (#614): `src/a.py@abc`, a path followed by fewer
    than six hex characters, is silent. A locator that opens with a run of
    digits no ASCII letter, digit or `_` continues reads as an issue number
    unless its hash is glued to it: `docs/a.md#1장`, `docs/a.md#1-scope`,
    `docs/a.md#1.2`, `src/a.py#1>"x"`, and in a code span
    `docs/a.md#1-scope @abcdef12`, whitespace before its hash. A dotless
    file name takes a locator opening with a letter, `_`, `"` or `<` and
    never a digit, so
```

### 🟡 1 — `GIVEN_UP` in `tests/test_a_row_points_by_content.py`

```python
    '#handler>"a"b"@abcdef12',
    "docs/a.md#1-scope @abcdef12",
]
```

### 🟡 1 — `changelog.md` of this work item, the trade sentence

```markdown
  `C#"hello"` and `vector#<T>`. What this gives up: `src/a.py@abc` with a
  hash shorter than six characters; a locator opening with digits that no
  ASCII letter, digit or underscore continues, unless its hash is glued to
  it (`docs/a.md#1장`, `docs/a.md#1-scope`, `docs/a.md#1.2`,
  `src/a.py#1>"x"`, and `docs/a.md#1-scope @abcdef12` with a space before
  the hash); `Makefile#1x`; and a path-less `#handler @abcdef12` or
  `#handler>"a"b"@abcdef12` are not named. A run of `#` characters outside
  quotes no longer takes seconds to read.
```

### 🟡 2 — `test_every_other_page_that_grades_the_flag_names_malformed`

```python
    flag = table_row(skill, "`--strict`")[1]
    assert "malformed" in flag and f"exit {strict}" in flag, flag
    assert f"instead of {lenient}" in flag, "the flag row's lenient exit"
```
```python
    template = read(os.path.join(ROOT, "templates", "evidence-check.yml"))
    assert lenient < strict, "the template says dropping --strict softens it"
    assert "softens drift\n          # and MALFORMED, and nothing else" in template
```

### ⬜ 3 — the comment above `GLUED_MARKS_RE`, lines 1624-1625

```python
# `#` is out of the unquoted class so each attempt stops at the next `#`
# outside a quote: the attempt that starts there finds the same match, and a
# run of them is read in linear time. A `#` inside a quote does not stop
# one, so a chain of quoted strings holding escaped quotes (`#"\"` repeated)
# is still quadratic: 1.5 s at 20 000 characters, far past any real row.
```

## Proof block

Opened and read in full or at the cited lines:
`seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/rounds/round-1.md`,
`rounds/round-1-report.md`, the fix diff `d05cc2c3..6c260d34` for
`skills/`, `tests/`, `seal/ledger/`, `seal/releases/0.15.4.md` and the
work item's `spec.md`, `changelog.md` and `overview.md`;
`skills/evidence-check/scripts/evidence_check.py` lines 30-48, 60-135,
1600-1780 and 2760-2783 at `eb30a068`, and lines 1600-1660 at `47e32d57`;
`tests/test_a_row_points_by_content.py` lines 873-923 and 1196-1255;
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` lines
61-73, 381-400 and 443-465; `skills/evidence-check/SKILL.md` line 173 at
both SHAs; `skills/evidence-ci/SKILL.md` lines 63-72;
`templates/evidence-check.yml` lines 36-50; `spec.md` lines 125-145 and
170-199. Executed: the commands in *Executed probes*, in the clone.

Needs a fix: yes — 🟡 1 (the list of what rule (a) gives up still omits a digit-opening locator whose hash follows after whitespace, in the docstring, `GIVEN_UP` and the release note) and 🟡 2 (the flag row's and the template's pins stay green when the grading changes)

Loses a record or crashes: no

