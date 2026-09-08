# round 3 — verifying round, PR #260, target `a495e4f`

A verifying round, and the last the cap allows. Its job is round 2's three
verdicts, and the one surface exempt from that restraint is what round 2's
fixes themselves created.

Worked in a `git clone --no-local` at `a495e4f`, at
`/private/tmp/claude-501/…/scratchpad/warden-r3-209/repo`. `git rev-parse HEAD`
read `a495e4f38e59fc059a627890b00a65a4d4b2f201` before and after every mutation
batch, and `git status --porcelain` was empty after each. Nothing was written in
the primary tree except this file.

## The short answer

Round 2's three verdicts all hold as fixed. The case it prescribed is planted,
it is red on each of the three session-stopping arms in turn, its parameters
split by arm exactly as its docstring claims, and every parameter's input
reaches the arm rather than standing beside it. R5's `Checked` date moved to a
date somebody did read the code. Nothing needs a fix.

What the round opened is one class, five instances of it: the arithmetic the
correction left behind. **Four** of `gh_segments`' branch decisions are now red
where every carrier says three, and that one-off runs through T4's Notes,
issue #262's table, and `overview.md`. All five are corrections in record
locations — a ledger fragment, an issue body, a work item's memo — plus one
sentence of a test docstring. None of them ships a defect.

## 1 — the new case closes the class it claims

**Executed.** `bin/test tests/test_chain_hooks.py -q` gives 38 passed, exit 0
at the target. `gh_segments`' six branch decisions were mutated one at a time,
each with every `__pycache__` in the clone removed and the hook's mtime stamped
a minute apart, so no mutation could reuse an earlier one's bytecode:

| Mutation | Result | Which parameters went red |
|---|---|---|
| `except ValueError` removed | 3 failed · 35 passed | the two quoted-pipe parameters, plus round 1's own `test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session` |
| the `while`'s `i < len(toks)` removed | 3 failed · 35 passed | `FOO=bar`, `echo hi;`, `gh pr view 1 --json comments\n` |
| the env-assignment prefix member removed | 38 passed, exit 0 | none |
| the `WRAPPERS` member removed | 38 passed, exit 0 | none |
| the `if`'s `i < len(toks)` removed | 3 failed · 35 passed | the same three |
| `os.path.basename(toks[i]) == "gh"` removed | 1 failed · 37 passed | `echo hi;` alone |

So the docstring's split is right: the two quoted-pipe parameters are the
`except ValueError` arm and the other three are the index guards, and each arm
is watched by parameters no other arm shares.

**Executed — the input reaches the arm.** Tracing `SEG_RE.split` and
`shlex.split` over each parameter:

- `gh pr view 1 --json comments | jq '.c[] | .b'` — two of its three segments
  raise `No closing quotation`; `gh pr merge 1 --squash | tee it's-done.log` —
  one of two does. Both reach the `except`.
- `gh pr view 1 --json comments\n` and `echo hi;` — each leaves a trailing
  segment whose token list is `[]`, so both index guards are what stop
  `toks[i]`.
- `FOO=bar` — token list `['FOO=bar']`, **not empty**. The env-assignment
  prefix arm consumes the only token, `i` becomes 1, and both guards are then
  what stop `toks[1]`. It reaches the guards by a different route than the
  other two, which is finding 4 below.

**Executed — the floor the arms hold.** The hook fed real `PostToolUse`
payloads exits 0 on all five commands as shipped, and exits 1 with `IndexError:
list index out of range` on `gh pr view 1 --json comments\n`, on `echo hi;` and
on `FOO=bar` with either index guard removed. T5's outcome claim is confirmed.

## 2 — the three carriers of the false ground

**T4's Notes** — the false sentence is gone and the replacement is true:
`except ValueError` is now named as one of three arms whose failure stops a
session, with the index guards and their mechanism beside it. Two numbers in
the same cell are not, and they are findings 1 and 2.

**`overview.md`'s `Not done` paragraph** — the corrected text is true as
prose. Its internal arithmetic (fourteen survivors, three fixed, two
behaviour-preserving, nine left) is self-consistent, but the "three" is one
short: finding 3.

**Issue #262** — title and body prose both moved to nine, and both are right.
The table did not: it now sums to ten. Finding 2.

Beyond the three, `overview.md`'s closing memo carries three figures the fix
passes never swept: finding 5.

One sentence in #262 asserted a measurement at "round 3" before round 3 had
run — *both measured green again at round 3 with every other arm of that
function now red*. This round measured it, and it is true as written. Left
alone.

## 3 — T5, the new ledger row

**Executed.** `evidence-check --strict --ledger seal/ledger/1788844300-….md .`
gives **11 ok · 0 drifted · 0 broken** for the fragment: T5's two anchors
resolve. (The run exits 2 on the records arm alone, which is the refusal set
carried as not this round's to close.)

T5's headline figures are what the tree produces, measured above: of
`gh_segments`' six branch decisions, four are now red — both index guards,
`except ValueError`, `basename(…) == "gh"` — and two are still green, the
env-assignment prefix arm and the `WRAPPERS` arm. `38 passed, exit 0 as
shipped` and `each leaving 35 green` are both right.

Two of its sentences overstate — findings 3 and 4.

## 4 — the two smaller corrections

**T4's count, thirteen → twelve.** The correction was made and it is one
short. **Executed:** with the branch's two `gh` cases deselected — the state
`gh_segments` was in when round 1 walked it — every one of its branch
decisions is green, all six of them, including `except ValueError`. So under
the five-way enumeration T4's own sentence names (*`gh_segments` five arms and
`main` nineteen*), `gh_segments` contributed **five** unwatched arms and not
four, and the base is thirteen. Round 2's ⬜ 2 moved the number toward
#262's table, and the table is itself one short. Finding 1.

**R5's `Checked`, 2026-09-07 → 2026-09-08.** Right, and for the right reason.
`--reverify` rewrote the hash cell on 2026-09-08 and the date cell is the
writer's half; round 2 then re-read the anchored case and recorded that its
claim still holds under `504b6136`. Somebody read the code on that date, which
is what `CLAUDE.md` makes the column mean. **Read.**

## 5 — the declared deviation: `r"""`

Right, and it is the only correct form. The docstring names `\n` twice; in a
plain docstring both become real newlines and the sentence *`SEG_RE` splits on
`\n` as well as on `|`* loses the thing it is about. A raw docstring is also
what a docstring containing a backslash is supposed to be. `uvx ruff check` and
`uvx ruff format --check` on the file are both exit 0. **Executed.**

Nothing else in the case was changed, which the fix pass declared and this
round confirms against the diff.

---

# Findings

All five are ⬜. None is a defect the release would ship, and four of the five
sit in record locations, which `docs/review-chain-spec.md` puts outside
`Needs a fix`. The fifth is one sentence of a test docstring; it belongs in the
closing commit beside the others.

## ⬜ 1 — T4's Notes carry three numbers that cannot all be right

`seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6`

The cell now says twelve arms were watched by nothing, that this is one of
three whose failure stops a session, and that *The remaining eleven arms are
deferred to #262*. Twelve minus three is nine, and nine is what the other three
carriers were moved to in the same commit. The `eleven` is what round 2's own
⬜ 2 quoted in its finding text; the fix corrected the first half of that
sentence pair and left the second.

The base is also one short. Executed: with the branch's two `gh` cases
deselected, all of `gh_segments`' decisions are green — five under the
five-way enumeration this very sentence names — so the base is thirteen, not
twelve, and thirteen minus four closed is the nine every other carrier states.

Why it matters: this row is the branch's own account of how much of the file it
left unwatched, and #262 is the ticket that decides when the rest get watched.
A row that subtracts three from twelve and prints eleven cannot be reconciled
by a reader at all.

## ⬜ 2 — issue #262's table sums to ten where its title and prose say nine

Issue #262, the arm table and the `What is left` paragraph.

The row reads `| gh_segments | 5 | 2 |`, and `| main | 19 | 8 |` beside it, so
the column sums to ten. The title says nine arms, the prose says *Nine arms.
Two of them are in `gh_segments` … and the rest are in `main`* — which makes
main seven, where the table says eight.

The cause is two enumerations in one row. The `5` is round 1's, which counts
the `while`'s whole `(A or B)` test as one boolean member; the `2` is T5's,
which splits it into the env-assignment arm and the `WRAPPERS` arm. Executed:
taken as one arm, the whole prefix-skip loop removed leaves 38 passed, exit 0 —
one unwatched arm under the row's own denominator. `| gh_segments | 5 | 1 |`
makes the table agree with the title, the prose and `overview.md` at nine.

## ⬜ 3 — the branch closed four of `gh_segments`' decisions, not three

Issue #262 (*Three of the fourteen are closed*),
`seal/specs/1788844300-…/overview.md:77` (*Three of the fourteen survivors are
fixed here*).

Executed: with the new case deselected, `os.path.basename(toks[i]) == "gh"`
mutated away leaves 33 passed, exit 0 — nothing watched it. With the case, that
mutation goes red. So the case closed a fourth decision, which T5's Notes
already say ("as a by-product") while both prose carriers still count three.

Three is right for *arms whose failure stops a session*. It is wrong as the
number subtracted from the deferred list, which is what both sentences use it
for.

## ⬜ 4 — one parameter is described as something it is not, in three places

`tests/test_chain_hooks.py:330`, and
`seal/ledger/1788844300-…-the-guards-cases-cannot-observe-what-they-guard.md:7`
(T5's Executed cell and its Notes).

Three sentences call all three index-guard parameters empty-segment ones: the
docstring's *the three that reduce to an empty token list are the index
guards*, T5's *deleting either `i < len(toks)` fails the three empty-segment
ones*, and T5's *any multi-line Bash command leaves a trailing empty segment
whose token list is empty … on `gh pr view 1 --json comments` with a trailing
newline, on `echo hi;` and on `FOO=bar`*.

`FOO=bar` is neither multi-line nor empty. Executed: its token list is
`['FOO=bar']`, and it reaches the guards because the env-assignment prefix arm
consumes the token and leaves `i == len(toks)`.

Why it matters beyond the wording: that parameter's coverage depends on an arm
#262 leaves open and measured green. Change the env-assignment arm and
`FOO=bar` stops reaching the index guards while the case stays green — the
shape this work item exists about, one parameter down. The case as a whole is
safe, because the two genuinely-empty parameters still kill both guards, which
is why this is ⬜ and not 🟡.

T5's Notes also say the by-product is watched by *the two parameters expecting
`[]`*. Executed: only `echo hi;` goes red on that mutation. `FOO=bar` stays
green, because the prefix loop has already left `i == len(toks)` and the
widened `if i < len(toks):` is still False.

## ⬜ 5 — `overview.md`'s closing memo was never swept

`seal/specs/1788844300-…/overview.md:14`, `:17`, `:35`.

Three figures in the memo predate both fix passes:

- `· evidence: … T1, T2, T3 — added` — the fragment carries T4 and T5 as well,
  added by round 1's and round 2's fix passes.
- `· verified: EXECUTED — bin/test …, 30 passed at 57e9603` — the tree gives 38.
- *Four arms of the pre-merge guard could have been deleted without a single
  case going red, and two of them would have raised out of a `PostToolUse`
  hook* — the branch now pins seven such arms, and five of them raise
  (`SyntaxError`, `ImportError`, `except ValueError`, both index guards).

A memo is a snapshot of the implementation pass, so there is a reading under
which it is meant to stand still. That reading does not survive the same file's
`Not done` paragraph having been rewritten twice by review fixes. The
orchestrator settles which it is; if the memo stands still, the `Not done`
paragraph is the only place the branch's own counts should be read from, and
saying so is worth one sentence.

---

## What this round did not run

The broad gate, in full: the whole suite, unscoped `evidence-check`,
repository-wide lint and typecheck, `unverified_check` and `chain_check`.
Contract §2 leaves those to the orchestrator, once, after the rounds settle,
and this round's prompt carries them as not mine. What was run is one module
(`tests/test_chain_hooks.py`), `ruff` on the one changed `.py` file, and
`evidence-check` narrowed to the work item's own fragment.

Carried as not this round's to close, unchanged: the records-arm refusals
against round 1's own report and record (`_get_supported_file_loaders`,  <!-- NAME NOT IN TREE: naming the refusals, not claiming the units -->
`blank_code_fences` ×3, one drifted stamp — reproduced this round at  <!-- NAME NOT IN TREE: naming the refusals, not claiming the units -->
4 refused · 1 drifted), and `docs/flow.md:102`'s unticked box.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | ⬜ T4's Notes say twelve watched by nothing, three closed here, and eleven remaining — twelve minus three is nine, and the base measures thirteen | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | open | executed: with the branch's two `gh` cases deselected every one of `gh_segments`' decisions is green, so the five-way base is 5 + 8 = 13; `eleven` is the half of round 2's own ⬜ 2 that the fix did not take. A ledger fragment, so a correction rather than a fix |
| 2 | ⬜ issue #262's arm table sums to ten where its title, its prose and `overview.md` say nine, because the row's arm count and its unwatched count come from different enumerations | issue #262, the arm table | open | executed: the whole prefix-skip loop removed as ONE arm leaves 38 passed exit 0, so under the row's own five-way denominator `gh_segments` has one unwatched arm and `5 \| 1` reconciles the table with all three prose carriers |
| 3 | ⬜ the branch closed four of `gh_segments`' decisions, not three — `basename(…) == "gh"` too — and both prose carriers subtract three from the deferred list | issue #262 · `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:77` | open | executed: with the new case deselected, mutating `== "gh"` leaves 33 passed exit 0; with it, that mutation goes red on `echo hi;`. T5's Notes already name the by-product |
| 4 | ⬜ the `FOO=bar` parameter is called an empty-segment one in the case's docstring and twice in T5, and its coverage of the guards runs through an arm #262 leaves open | `tests/test_chain_hooks.py:330` · `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:7` | open | executed: its token list is `['FOO=bar']`; the env-assignment prefix arm consumes it and leaves `i == len(toks)`, which is how it reaches both guards. Also executed: only `echo hi;` of the two `[]` parameters goes red on the `== "gh"` mutation, where T5 says both do |
| 5 | ⬜ `overview.md`'s closing memo still says T1–T3, 30 passed, and four arms of which two raise | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:14` | open | read: the fragment carries T4 and T5, the module gives 38 passed, and the branch pins seven arms of which five raise. Whether a memo is swept after review fixes is the orchestrator's call, and the same file's `Not done` paragraph has been rewritten twice |
| 6 | round 2's 🟡 1 — `except ValueError` was not the only survivor whose failure stops a session | `hooks/review-history-guard.py:176` | answered | executed: the case is planted and red on each of the three arms in turn — `except ValueError` fails the two quoted-pipe parameters, either `i < len(toks)` fails the other three, each leaving 35 green; every parameter's input reaches its arm, traced through `SEG_RE` and `shlex`; the hook exits 1 with `IndexError` on three ordinary payloads with either guard removed. Residuals are findings 1–4 |
| 7 | round 2's ⬜ 2 — T4's count, thirteen where the other carriers give twelve | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | answered | the edit landed; measured, it moved the wrong way and left the row's other number untouched. Carried forward as finding 1 |
| 8 | round 2's ⬜ 3 — R5's `Checked` column against a 2026-09-08 re-verification | `seal/ledger.md:1385` | answered | read: the cell reads `2026-09-08`, and round 2 re-read the anchored case that day and recorded that its claim holds under `504b6136`. The date is a date somebody read the code, not a date typed to satisfy the column |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_chain_hooks.py -q` in a `--no-local` clone at `a495e4f` | exit 0 — 38 passed |
| `gh_segments`' six branch decisions mutated one at a time, `__pycache__` cleared and the hook's mtime stamped a minute apart between each | 4 red — `except ValueError` (3 failed), each `i < len(toks)` (3 failed), `basename(…) == "gh"` (1 failed) — and 2 green at 38 passed, the env-assignment prefix arm and the `WRAPPERS` arm |
| the same six with the new parametrized case deselected | `except ValueError` alone red, failing round 1's case; **`while` guard, `if` guard and `== "gh"` all green at 33 passed** |
| the same six, plus the whole prefix-skip loop as one arm, with BOTH `gh` cases deselected | **all eight mutations green at 32 passed, exit 0** — before this branch, no case watched any decision of `gh_segments` |
| the whole prefix-skip loop removed as one arm, at the shipped tree | 38 passed, exit 0 — one unwatched arm under round 1's five-way enumeration |
| `SEG_RE.split` and `shlex.split` traced over each of the case's five parameters | the two quoted-pipe commands raise `No closing quotation` on 2 of 3 and 1 of 2 segments; `…comments\n` and `echo hi;` each leave a segment whose token list is `[]`; **`FOO=bar` leaves `['FOO=bar']`** and reaches the guards only after the env-assignment prefix arm advances `i` to 1 |
| the hook fed real `PostToolUse` payloads for five commands, as shipped and with each `i < len(toks)` removed in turn | exit 0 on all five as shipped; exit 1 with `IndexError: list index out of range` on `gh pr view 1 --json comments\n`, `echo hi;` and `FOO=bar` with either guard removed |
| `./bin/evidence-check --strict --ledger seal/ledger/1788844300-….md .` | fragment **11 ok · 0 drifted · 0 broken** — T5's two anchors resolve; exit 2 from the records arm alone, 4 refused · 1 drifted, the set carried as not this round's |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_chain_hooks.py` | exit 0 both — all checks passed, 1 file already formatted |
| `git rev-parse HEAD` and `git status --porcelain` before and after every mutation batch | `a495e4f38e59fc059a627890b00a65a4d4b2f201` throughout, working tree clean after each restore |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the remaining unwatched arms of `main`, and the durable close that derives arms from source and mutates them | issue #262, already deferred by the branch | the orchestrator, or the work item #262 opens |
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |
| whether a work item's closing memo is swept after review fixes or stands as a snapshot of the implementation pass | finding 5 states both readings | the review orchestrator |

## Paste-ready fixes

```
seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md — T4,
findings 1 and 3 together. Two edits to the Notes cell.

The base, which the five-way enumeration in the same sentence gives as 5 + 8:

-  gives `gh_segments` five arms and `main` nineteen, and twelve of those
-  were watched by nothing.
+  gives `gh_segments` five arms and `main` nineteen, and thirteen of those
+  were watched by nothing — every one of `gh_segments`' own, measured with
+  this branch's two `gh` cases deselected.

and the remainder, four of the thirteen having been closed here:

-  The remaining eleven arms are deferred to #262 rather than pinned one by
-  one
+  The remaining nine arms are deferred to #262 rather than pinned one by
+  one
```
```
seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md — T5,
finding 4. Two edits: the Executed cell, then the Notes.

-  deleting either `i < len(toks)` fails the three empty-segment ones, each
-  leaving 35 green
+  deleting either `i < len(toks)` fails the other three, each leaving 35
+  green — two of them leave a segment whose token list is empty, and
+  `FOO=bar` leaves one token the env-assignment prefix arm consumes, so `i`
+  reaches `len(toks)` either way

-  The case closed `basename(…) == "gh"` as a by-product — the two parameters
-  expecting `[]` watch it — which leaves `gh_segments` with two unwatched
-  arms, and those stay with #262
+  The case closed `basename(…) == "gh"` as a by-product — `echo hi;` watches
+  it, and `FOO=bar` does not, because the prefix arm has already left
+  `i == len(toks)` and the widened test is False either way — which leaves
+  `gh_segments` with one unwatched arm under round 1's five-way enumeration,
+  two under the six-way split this cell uses, and it stays with #262
```
```python
# tests/test_chain_hooks.py:328-331 — finding 4, the docstring's second
# paragraph. `FOO=bar` is one token, not an empty segment, and it is worth
# saying which arm carries it there.

    The parameters are grouped by arm, so a mutation says which one went:
    the two quoted-pipe commands are the `except ValueError` arm, and the
    other three are the index guards. Two of those leave a segment whose
    token list is empty; `FOO=bar` leaves one token, which the
    env-assignment prefix arm consumes, so `i` reaches `len(toks)` by the
    other route. Contract §12 — the finding named one instance and the cause
    produces three.
```
```
Issue #262 — findings 2 and 3. The table row, and two sentences.

The row, so that its unwatched count uses the same enumeration as its arm
count (the whole prefix-skip loop taken as one boolean member is green, at
38 passed exit 0):

-  | `gh_segments` | 5 | 2 |
+  | `gh_segments` | 5 | 1 |

The count of what the branch closed, which is four decisions of which three
stop a session:

-  Three of the fourteen are closed on the branch for #209 · #210, all in
-  `gh_segments` and all under one parametrized case: `except ValueError` and
-  the two `i < len(toks)` index guards.
+  Four of the fourteen are closed on the branch for #209 · #210, all in
+  `gh_segments` and all under one parametrized case: `except ValueError`,
+  the two `i < len(toks)` index guards, and `basename(…) == "gh"` as a
+  by-product. The first three are the ones whose failure stops a session's
+  Bash call rather than misfiling a reminder.

and the paragraph under `What is left`, so that two in `gh_segments` is not
subtracted from a table that gives one:

-  Nine arms. Two of them are in `gh_segments` — the env-assignment prefix arm
-  and the `WRAPPERS` arm, both measured green again at round 3 with every
-  other arm of that function now red — and the rest are in `main`.
+  Nine arms. One of them is in `gh_segments` — the prefix-skip loop, whose
+  env-assignment half and `WRAPPERS` half were both measured green again at
+  round 3 with every other decision of that function now red — and the other
+  eight are in `main`.
```
```
seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md
— finding 3, the `Not done` paragraph at :77. One sentence, to match #262.

-  Three of the fourteen
-  survivors are fixed here, all in `gh_segments` and all under one parametrized
-  case: `except ValueError`, and the two `i < len(toks)` index guards. Those are
-  the three whose failure stops a session's Bash call rather than misfiling a
-  reminder
+  Four of the fourteen
+  survivors are fixed here, all in `gh_segments` and all under one parametrized
+  case: `except ValueError`, the two `i < len(toks)` index guards, and
+  `basename(…) == "gh"` as a by-product. The first three are the ones whose
+  failure stops a session's Bash call rather than misfiling a reminder
```
```
seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md
— finding 5, the closing memo, IF the orchestrator reads a memo as maintained.
Three lines, at :14, :17 and :35.

-  · evidence: `seal/ledger/1788844300-…` T1, T2, T3 — added
+  · evidence: `seal/ledger/1788844300-…` T1, T2, T3 — added; T4 and T5 added
+              by round 1's and round 2's fix passes

-  · verified: EXECUTED — `bin/test tests/test_chain_hooks.py -q`, 30 passed at
-              `57e9603`
+  · verified: EXECUTED — `bin/test tests/test_chain_hooks.py -q`, 30 passed at
+              `57e9603`, and 38 passed at the reviewed head

-  Four arms of the pre-merge guard could have been deleted without a single case
-  going red, and two of them would have raised out of a `PostToolUse` hook into
-  somebody's Bash call
+  Seven arms of the pre-merge guard could have been deleted without a single
+  case going red — four found by the implementation pass and three more by the
+  review rounds — and five of them would have raised out of a `PostToolUse`
+  hook into somebody's Bash call
```

Needs a fix: no
Loses a record or crashes: no
