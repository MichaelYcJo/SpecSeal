# 1788844300-the-guards-cases-cannot-observe-what-they-guard — round 1 report

Target `2549f7f2c6923de0bd98d04101242f2222eea2ab` · base `release/v0.9.2` at
`bcf48b8` · PR #260 · reviewed in a `git clone --no-local` at the target SHA.

## The shape of what this round found

The branch's method is right and its method is what finds the rest. Enumerating
`reader` out of its own source gave five arms where every prose reading gave
four — I reproduced that — and the same walk applied to the other two functions
in the same file gives twelve more arms that no case in this repository
watches. One of them is a crash arm reached by an ordinary command.

Everything else follows from one gap between what was measured and what was
written down:

```
① the enumeration was run on two of the file's four functions
       ↓ so
② gh_segments' `except ValueError` is unwatched — and deleting it stops a
   session's Bash call on `gh pr view N --json comments | jq '…| …'`

③ the tie reads calls, not effects
       ↓ so
④ a third pass written as a regex sub — the very pass #210 and round 3 both
   used as their example — passes the tie silently

⑤ the branch rewrote a case `seal/ledger.md` R5 anchors
       ↓ so
⑥ that row drifted, and overview.md defers it under a reason that is not why
```

## 🟡 1 — the file has two more functions, and one of their arms stops a session

`hooks/review-history-guard.py:173`.

`gh_segments` splits a command on `SEG_RE`, which includes `|`. A pipe inside a
quoted string therefore leaves a segment whose quoting is unbalanced, and
`shlex.split` raises `ValueError` on it. The `except ValueError: continue` arm
is what absorbs that.

**[executed]** the arm is watched by nothing. Deleting it leaves
`tests/test_chain_hooks.py` at 30 passed, exit 0, and leaves all seven modules
that reference this hook at **270 passed, exit 0**.

**[executed]** with the arm deleted, feeding the hook a real payload:

| command | with the arm | with it deleted |
|---|---|---|
| `gh pr view 123 --json comments \| jq '.comments[] \| .body'` | exit 0, silent | **exit 1, `ValueError: No closing quotation`** |
| `gh pr merge 123 --squash \| tee it's-done.log` | exit 0, silent | **exit 1, `ValueError: No closing quotation`** |

That is the same failure shape T1's own Notes call *the one thing R5's own
argument says must never happen* — an exception out of `gh_segments`, past a
`main()` whose `try` covers `json.load` alone, into the session's Bash call.
The first command is the READ branch's own example piped into `jq`.

The branch reached `is_closed` on contract §12 grounds, naming the cause as
*arms read off the page rather than enumerated*. That cause does not stop at
the second function of the file.

**[executed]** the full enumeration, walking each function for `ExceptHandler`,
`If`, `While` and `IfExp` nodes and counting each member of a boolean test and
of an except tuple as its own arm — the branch's own method:

| Function | Arms | Watched by no case (270 cases, 7 modules) |
|---|---|---|
| `reader` | 5 | `spec.loader is None` — unconstructible, and stated as such |
| `is_closed` | 4 | none |
| `gh_segments` | 5 | `except ValueError`, the env-assignment prefix arm, the `WRAPPERS` arm, `basename(…) == "gh"` |
| `main` | 19 | `except Exception`, `tool_name != "Bash"`, `not segs`, `not top`, `not opted_in`, `not item`, `if unreadable`, and the READ branch's `if records` |

Two of those are behaviour-preserving rather than gaps and I am not counting
them: `main`'s merge-branch `if records` is redundant *because* `is_closed([])`
answers True, which is T3 doing its job. The rest are live. Removing the
opt-in halves makes a globally installed plugin nag unrelated repositories,
which this module's own docstring forbids; removing `not segs` makes the stray
and unreadable notices fire on every Bash call.

## 🟡 2 — the tie catches a pass with a name and misses the pass the ticket used as its example

`tests/test_chain_hooks.py:515`.

`reader_blanking_passes` collects `ast.Call` nodes whose `func` is an
`ast.Name`. A pass added as a module function is seen. A pass added as
`_SPAN_RE.sub("", text)` is an `ast.Attribute` call and is not.

That is not a hypothetical shape. Both #210 and round 3 of the previous work
item used the same example pass — *inline code spans blanked* — and a
text-level blanker is naturally written as a regex sub, not as a line-based
function like the two that exist.

**[executed]** in a clone at the target SHA, four mutations of `readable`:

| what was added to `readable` | module | `is_closed` on a record whose only closing word is in an inline span |
|---|---|---|
| nothing (baseline) | 30 passed, exit 0 | True |
| a third pass as a module function | **2 failed** — the tie fires | False |
| the identical blanking as `_SPAN_RE.sub(…)` | **30 passed, exit 0** | **False** |
| `blank_fences` renamed, nothing else | 2 failed — the tie fires | True |
| the two passes composed in the other order | 30 passed, exit 0 | True, and see below |

Row three is #210 reproduced with the tie in place.

Three carriers state the guarantee without the limit, and one of them ships to
users: the case docstring (*so a pass added to the reader fails this case
instead of arriving unguarded and silent*), T2 of the ledger fragment, and the
changelog fragment (*so a pass added later fails that case instead of passing
quietly*).

**On reordering, which the round was asked to judge separately.** A reorder
does not fail the tie, and it does change verdicts. **[executed]** on the text
below, the shipped order blanks the closing word and the reversed order does
not.

The comment opener below is written `<! --`, with a space the real text does
not have. This report's first pass wrote it without the space, and
`round_record.py new` refused the whole file: the generator strips comments
**before** it looks a section up, so an unclosed opener blanked every line
beneath it and the sections and both terminal lines reached no record. A fence
does not protect it, which is the point — the order the passes run in decides
what survives, and that is the same fact this finding is about, arriving as an
incident rather than as an argument.

````
# round 1

```
<! -- a fenced block that opens an HTML comment
```

nothing to drain

| Deferred | live |
````

`blank_fences(strip_comments(x))` → closing word not visible.
`strip_comments(blank_fences(x))` → visible. The tie compares a set of names,
so it cannot see order. I am not asking for that to be closed — the case's
claim is about a pass being *added*, and it is true of additions. It belongs in
the report because the limit is now two things wide rather than one.

## ⬜ 3 — the branch rewrote a case `seal/ledger.md` anchors, and the row was not re-verified

`seal/ledger.md:1385`.

**The branch takes the unscoped evidence gate from green to red.** That is what
makes this a blocker rather than bookkeeping: the gate the orchestrator runs at
the pull request passes on the base and fails on the target, and the one row
between them is this branch's.

| tree | `--strict --ledger seal/ledger.md .` (mine) | `--strict .` unscoped (the orchestrator's) |
|---|---|---|
| base `bcf48b8` | **[executed]** 899 ok · 0 drifted · exit 0 | **[executed by the orchestrator]** 899 ok · 0 drifted · exit 0 |
| target `2549f7f` | **[executed]** 898 ok · **1 drifted** · **exit 2** | **[executed by the orchestrator]** 906 ok · **1 drifted** · **exit 2** |

The two reconcile, which is worth saying because they were run by different
people on different scopes. My two narrowed runs at the target give 898 ok on
`seal/ledger.md` and 8 ok on the work item's fragment; 898 + 8 is the
orchestrator's 906, and the same single drifted row is in both. The base
carries no fragment yet, so 899 is the whole of it there.

The drifted row is R5's
`tests/test_chain_hooks.py#test_the_guard_falls_back_to_the_raw_text_without_the_reader@df85505e`
— *content changed at 378-452*, which is the function this branch added two
parameters to. `--reverify` gives `df85505e -> f0ad0bf1`, and `f0ad0bf1` is the
hash the branch's **own** fragment T1 already carries for the same anchor. The
two rows anchor one function at two hashes.

`overview.md:53` defers this to the orchestrator with the grounds *the
correction to R5 was not re-hashed because it changes a Notes cell rather than
an anchor*. The drift is not from the Notes cell. It is from the test edit in
the same branch, so that row defers a real failure under a reason that does not
describe it, and a reader who accepts the reason stops looking.

CI is the one place this does not go red on its own. `.github/workflows/test.yml:87`
runs the checker without `--strict`, so drift is exit 1 and the job prints
`::warning::evidence ledger reports drift` and passes. Nobody is stopped by it;
somebody has to read the warning. That is why the finding rests on the
orchestrator's `--strict` gate rather than on the pull request's checks.

**Why the verdict stays ⬜ even so, and where the fix belongs.** The location is
`seal/ledger.md`, and `docs/review-chain-spec.md` puts a finding located in a
record or the ledger outside `Needs a fix` — but the same passage names this
exact case and says where it goes: *what `chain_check` or `evidence_check`
refuses is corrected in the closing commit*. So this is not a fix pass and it is
not optional either. It has to be in the closing commit, before the pull
request, or the orchestrator's own gate is red at the moment it is read. If the
orchestrator reads the spec differently, the grounds for moving it to 🔴 are its
own to state; I am not moving it on the strength of a measurement that agrees
with mine.

Also worth carrying: the checker itself says *`--ledger` narrowed this run — 1
ledger this repository carries was not read: `seal/ledger.md` … a branch
falsifies rows in ledgers it does not own, and those are the rows with the
longest reach.* The narrowing the spawn prompt prescribes is exactly the
narrowing that hides this.

## ⬜ 4 — the correction to the other work item's record replaces one unreproducible number with another

`seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-3.md:71`.

**The scope question the branch flagged: correcting that record is in scope,
and the form is right.** `docs/review-chain-spec.md` (*A finding located in a
record is a correction, not a round*) puts a record finding outside the fix
loop rather than outside the branch; the strikethrough-plus-attribution-plus-SHA
shape matches what this repository did at `b73bdd3` and what `seal/ledger.md`
R5 itself carries twice; and five of the nine sibling worktrees on this release
also edit `seal/ledger.md` in place, so touching a shared record is this
release's norm and not this branch's deviation. I would not hold the branch on
the act.

**The number is the problem.** The corrected cell reads *six mutations, one per
arm | 3 red, 3 green*, in the same sentence that asserts the function has
**five** arms. Six is not one-per-arm of five.

**[executed]** the whole tally re-run at `c3c22c2`, 27 passed baseline,
one arm at a time:

| arm | verdict at `c3c22c2` |
|---|---|
| `reader` / `spec is None` | RED |
| `reader` / `spec.loader is None` | GREEN |
| `reader` / `except OSError` | RED |
| `reader` / `except ImportError` | **GREEN** |
| `reader` / `except SyntaxError` | GREEN |
| `is_closed` / `if not records` | GREEN |
| `is_closed` / `except OSError` | RED |
| `is_closed` / `if seen is not None` | RED |
| `is_closed` / `CLOSED_RE.search` | RED |

The branch's substantive claim is confirmed: deleting `ImportError` at
`c3c22c2` leaves 27 passed, exit 0 — the same reading `SyntaxError` gives, and
nobody had counted it.

The tally is not. `reader`'s five arms give **2 red, 3 green**, not 3 and 3.
And the original *4 red, 2 green* reconciles with a six-mutation set that never
included `ImportError` — which is exactly what a round counting four arms would
have run, four of `reader` plus two of `is_closed`. So the correction rewrites
the result of a mutation set it did not run, in a branch whose stated subject is
*a false measurement left standing in a record*.

## ⬜ 5 — the loader sweep proves "not these inputs"; the sentence it supports needs a different reason

`tests/test_chain_hooks.py:417`, `overview.md:58`.

The branch probed rather than asserted, which is what #205 asks for, and the
conclusion holds. **[executed]** my own sweep over 21 inputs — the branch's nine
plus `.pyw`, `.PY`, `.py.gz`, a trailing space, a trailing slash, `.`, `..`,
`missing.pyc`, `missing.so`, `a.py/` and `dir/../a.py`. Nothing makes `spec`
truthy with a falsy loader.

What the sweep does not cover:

- **It is inductive and the guarantee is deductive.** `spec_from_file_location`
  assigns `spec.loader` inside its supported-suffix loop and returns `None`
  from that loop's `else`, so loader-None is impossible for *any* location
  string, not merely for the ones tried. That one line is the durable reason; a
  sample of nine can only ever say *not these*.
- **The suffix list is per-platform.** **[executed]** on this machine
  `_get_supported_file_loaders()` yields `.cpython-314-darwin.so`, `.abi3.so`,
  `.so`, `.py`, `.pyc`. Nine inputs on one interpreter and one operating system
  do not settle another, and contract §13 is the section about a defence
  resting on a platform guarantee.

The docstring states the conclusion universally (*nothing makes `spec` truthy
while its loader is falsy*). Naming the CPython line would make it universal
for a reason, and would survive the day the sweep's inputs stop being the ones
that matter.

## ⬜ 6 — the tie's failure message tells a renamer to do the thing that will not fix it

`tests/test_chain_hooks.py:563`.

**[executed]** renaming `blank_fences` to `blank_code_fences` turns both
parameters red — the safe direction, and I am not asking for that to change.
The message says *Add the pass to `HIDDEN_CLOSING_WORD`, keyed by its name*.
Doing that leaves three keys against two passes and the case still red. The fix
for a rename is to re-key, and the message never mentions the case.

## ⬜ 7 — both tickets carry a false pointer, and only `overview.md` says so

`seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:43`.

**The implementer is right, verified rather than taken.** **[executed]**
`## Paste-ready fixes` in every version of `round-3.md` this clone's history
carries — `341be0b`, `70c272c`, `701d109` — reads `no paste-ready fix in the
report`. **[executed]** round 3's report on PR #208 has no such heading and
zero fenced blocks; round 2's report has the heading and two fences, which is
the likely source of the mix-up. Round 3's 🟡 1 and ⬜ 2 are prose only. So no
executed version was skipped, and the two new cases lost nothing by being
written from the tickets.

Two things stand open from it. `overview.md` says *checked every committed
version of the record (`c7fe663`, `341be0b`, `6de1bca`, `70c272c`)*, and
`c7fe663` and `6de1bca` are not objects in a clone of this repository — the
feature branch that held them was squashed — so the sentence names commits its
reader cannot open. And #209 and #210 still say *the reviewer's version is
fenced in `rounds/round-3.md`*; this PR closes both, so the false sentence
outlives the branch that disproved it in the two documents a later reader opens
first.

## ⬜ 8 — the deferred arm counts were taken by a different method than the one that found the fifth arm

Already deferred at `overview.md:54`, with the review orchestrator or a
follow-up work item as answerer. Naming it rather than reopening it.

The counts recorded are three and four. Counting the way this branch counted
`reader` — each member of a boolean test as its own arm — **[executed]** gives
`blank_fences` seven and `strip_comments` seven. The deferral is sound; the
numbers inside it are from the method the branch replaced.

## What was judged and let stand

- **The rule the round was asked about is applied consistently to all three
  arms the branch touched**, once its operative word is read as *constructible*
  rather than *reachable*. `SyntaxError` and `ImportError` are both — cases.
  `spec.loader is None` is neither — a sentence. `is_closed([])` is
  unreachable from `main()` but constructible in one line — a case. T1 and T3
  use the word *reachable* for two different things two rows apart, which is
  worth one word in a later pass and is not a finding.
- **Five is the count for `reader`.** **[executed]**, by AST rather than by
  reading: `spec is None`, `spec.loader is None`, and three except-tuple
  members. `is_closed` has four. `readable` has none.
- **Both new parameters and the new case are seen red on their own arm.**
  **[executed]** deleting `SyntaxError` fails `[a reader that does not parse]`
  alone; deleting `ImportError` fails `[a reader whose own import is missing]`
  alone; mutating `if not records: return True` to `return False` fails
  `test_no_records_at_all_is_not_an_unclosed_directory` alone. Each left the
  other 29 green.
- **The tie does fire for the case it was written for.** **[executed]** a third
  pass added as a module function turns both parameters red.
- The changed test file is clean under `uvx ruff check` and
  `uvx ruff format --check` — exit 0 each, executed by me in the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `gh_segments`' `except ValueError` is a live arm no case watches, and deleting it stops a session's Bash call on an ordinary piped `gh` command — twelve arms of the file's other two functions are unwatched | `hooks/review-history-guard.py:173` | open | executed: 270 passed exit 0 across all seven modules referencing the hook with the arm deleted; the hook then exits 1 with `ValueError: No closing quotation` on `gh pr view 123 --json comments \| jq '.comments[] \| .body'`. §12's class, named by the branch itself when it widened to `is_closed`, does not stop at the second function |
| 2 | 🟡 the tie sees `ast.Name` calls only, so a pass written as a regex sub — the pass #210 and round 3 both used as their example — passes it silently | `tests/test_chain_hooks.py:515` | open | executed: the same blanking added as a module function turns both parameters red; added as `_SPAN_RE.sub(…)` leaves 30 passed exit 0 while `is_closed` flips True→False. Three carriers state the guarantee without the limit, one of them the user-facing changelog |
| 3 | ⬜ R5's anchor for the case this branch rewrote drifted, so the branch takes the unscoped evidence gate from green to red, and `overview.md` defers it under a reason that is not why | `seal/ledger.md:1385` | open | executed: `--strict --ledger seal/ledger.md .` gives 899 ok · 0 drifted · exit 0 at `bcf48b8` and 898 ok · 1 drifted · exit 2 at `2549f7f`; the orchestrator's unscoped `--strict .` gives 899 ok · 0 drifted · exit 0 at the base and 906 ok · 1 drifted · exit 2 at the target, and the two reconcile row for row. `--reverify` gives `df85505e -> f0ad0bf1`, the hash this branch's own fragment T1 already carries. ⬜ because the location is the ledger, which `docs/review-chain-spec.md` puts outside `Needs a fix` — and the same passage sends what `evidence_check` refuses to the closing commit, which is where this has to be |
| 4 | ⬜ the correction to the other work item's record asserts 3 red / 3 green over six mutations while asserting the function has five arms | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-3.md:71` | open | executed at `c3c22c2`: `reader`'s five arms give 2 red / 3 green, `is_closed`'s four give 3 red / 1 green. The `ImportError`-was-green claim is confirmed; the tally is not, and the original 4/2 reconciles with a set that never mutated `ImportError`. Correcting the record in place is in scope and correctly formed |
| 5 | ⬜ the loader sweep is inductive and per-platform, and the sentence it supports is stated universally | `tests/test_chain_hooks.py:417` | open | executed: 21 inputs, none makes `spec` truthy with a falsy loader — the claim holds. The durable reason is `spec_from_file_location` returning None from its suffix loop's `else`; the suffix list here is `.cpython-314-darwin.so`, `.abi3.so`, `.so`, `.py`, `.pyc` and is platform-dependent |
| 6 | ⬜ the tie's failure message prescribes adding a key, which does not fix a rename | `tests/test_chain_hooks.py:563` | open | executed: renaming `blank_fences` turns both parameters red; adding a third key leaves three keys against two passes and the case still red |
| 7 | ⬜ two of the four SHAs `overview.md` calls "every committed version" are not objects in a clone, and the tickets keep the false pointer this branch disproved | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:43` | open | executed: `c7fe663` and `6de1bca` are `Not a valid object name`; `341be0b`, `70c272c`, `701d109` each read `no paste-ready fix in the report`; round 3's PR #208 report has no such heading and zero fences, round 2's has two. The implementer's account is confirmed |
| 8 | ⬜ the deferred arm counts for `blank_fences` and `strip_comments` were taken by the method this branch replaced | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:54` | already deferred | executed: counting each member of a boolean test as its own arm gives seven and seven, not three and four. Named rather than reopened — the deferral and its answerer stand |

## Paste-ready fixes

```python
# tests/test_chain_hooks.py — finding 1, append beside the other guard cases.
# Executed in a clone at the target SHA: 31 passed exit 0 with the arm in
# place; with `except ValueError` deleted, this case fails alone and the
# other 30 stay green.


def test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session(tmp_path):
    """`gh_segments`' `except ValueError`, which nothing watched.

    `SEG_RE` splits on `|`, so a pipe inside a quoted string leaves a segment
    whose quoting is unbalanced and `shlex.split` raises `ValueError` on it.
    The command that does it is an ordinary one — the READ branch's own
    example piped into `jq`. Without the arm the exception leaves
    `gh_segments`, passes `main()` unguarded (whose own `try` covers
    `json.load` alone) and stops the session's Bash call, which is the one
    thing T1's argument says must never happen."""
    guard = load_hook_module("review-history-guard.py", "guard_unbalanced_quote")
    assert guard.gh_segments("gh pr view 1 --json comments | jq '.c[] | .b'") == [
        "gh pr view 1 --json comments"
    ]
    assert guard.gh_segments("gh pr merge 1 --squash | tee it's-done.log") == [
        "gh pr merge 1 --squash"
    ]
```

```python
# tests/test_chain_hooks.py:515 — finding 2, replace the return of
# `reader_blanking_passes`. Executed: 31 passed exit 0 on the shipped reader;
# with an inline-span pass added to `readable` as `_SPAN_RE.sub(...)` both
# parameters go red, where the same pass leaves the shipped tie at 31 passed.
    attrs = {
        node.func.attr
        for node in ast.walk(ast.parse(src))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert attrs <= {"splitlines"}, (
        f"`readable` makes an attribute call this derivation cannot see: "
        f"{sorted(attrs - {'splitlines'})}. A pass written as `_SPAN_RE.sub(...)` "
        "rather than as a module function hides a closing word just as well and "
        "leaves the set below unchanged — which is #210 with the tie in place. "
        "Give the pass a name on the reader module, or teach this function to "
        "read the shape you used."
    )
    return {name for name in called if inspect.isfunction(getattr(reader, name, None))}
```

```
seal/ledger.md:1385 — finding 3. R5's Code grounds cell, one anchor:

-  `tests/test_chain_hooks.py#test_the_guard_falls_back_to_the_raw_text_without_the_reader@df85505e`
+  `tests/test_chain_hooks.py#test_the_guard_falls_back_to_the_raw_text_without_the_reader@f0ad0bf1`

and R5's Checked column 2026-09-07 -> 2026-09-08. Produced by, and confirmed
with, `./bin/evidence-check --reverify --ledger seal/ledger.md .` followed by
`./bin/evidence-check --strict --ledger seal/ledger.md .` — exit 2 before,
exit 0 after.

overview.md:53's Not-verified row then says what is actually left:

| `evidence-check` unscoped over the whole tree — this run read `seal/ledger.md` and the work item's fragment; the rest of `seal/ledger/*.md` was not read | the review orchestrator, at the pull request |
```

```
seal/specs/1788749195-.../rounds/round-3.md:71 — finding 4. The corrected cell
says what was measured instead of restating a tally over a set nobody ran:

| six mutations, one per arm | ~~4 red, 2 green — `spec.loader is None` and `SyntaxError`~~ **corrected 2026-09-08 by work item 1788844300 at `b8471fb`: the six did not include `ImportError`, which the round counted as one of two members of the except tuple rather than three. Re-executed against this module as it stood at `c3c22c2`, `reader`'s five arms give 2 red — `spec is None`, `except OSError` — and 3 green — `spec.loader is None`, `ImportError`, `SyntaxError`; deleting `ImportError` leaves 27 passed, exit 0, the same reading `SyntaxError` gives. That is also why the count below says four arms where the function has five** |
```

```python
# tests/test_chain_hooks.py:563 — finding 6, the tie's message. Two causes, not
# one, because a rename fails this assertion too and adding a key does not fix
# a rename.
    assert reader_blanking_passes(reader) == set(HIDDEN_CLOSING_WORD), (
        "the passes `readable` composes and the keys below have parted. If a "
        "pass was ADDED, a closing word it hides reads as hidden, `is_closed` "
        "returns False, and without this assertion nothing goes red — the "
        "silence looks exactly like correctness; add it here, keyed by its "
        "name, with a record that hides its word the way that pass hides it. "
        "If a pass was RENAMED, re-key its entry rather than adding one: an "
        "extra key leaves this assertion red."
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_chain_hooks.py -q` in a `--no-local` clone at `2549f7f` | exit 0 — 30 passed |
| every arm of all four functions of `hooks/review-history-guard.py` enumerated by AST (`ExceptHandler`, `If`, `While`, `IfExp`, each boolean member its own arm) | `reader` 5 · `is_closed` 4 · `gh_segments` 5 · `main` 19; `readable` 0 |
| 29 mutations, one per arm, against `tests/test_chain_hooks.py` at `2549f7f` | 13 red · 16 green |
| the 16 green re-run against all seven modules that reference the hook (270 cases) | 2 turn red (`main`'s `if strays`, and the POST guard's `not records` half); 14 stay green |
| the hook fed a real PostToolUse payload for `gh pr view 123 --json comments \| jq '.comments[] \| .body'`, with and without `except ValueError` | exit 0 silent; then **exit 1, `ValueError: No closing quotation`** |
| a third blanking pass added to `readable` as a module function, then the module run | RED — both parameters of the hidden-word case fail |
| the identical blanking added as `_SPAN_RE.sub("", text)`, then the module run | **GREEN — 30 passed, exit 0**, while `is_closed` on a record whose only closing word is in an inline span goes True → False |
| `blank_fences` renamed to `blank_code_fences`, nothing else changed | RED — both parameters fail, with a message that prescribes adding a key |
| `readable`'s two passes composed in the other order, then the module run | GREEN — 30 passed; and on a fence that opens an HTML comment the two orders disagree about whether the closing word is visible |
| `spec_from_file_location` over 21 inputs (the branch's nine plus `.pyw`, `.PY`, `.py.gz`, a trailing space, `a.py/`, `.`, `..`, `missing.pyc`, `missing.so`, `dir/../a.py`) | no input makes `spec` truthy with a falsy loader; supported suffixes here are `.cpython-314-darwin.so`, `.abi3.so`, `.so`, `.py`, `.pyc` |
| the whole arm tally re-run at `c3c22c2`, 27 passed baseline | `reader` 2 red / 3 green · `is_closed` 3 red / 1 green; deleting `ImportError` leaves 27 passed, exit 0 |
| `evidence_check.py --strict --ledger seal/ledger/1788844300-….md .` at `2549f7f` | exit 0 — 8 ok · 0 drifted · 0 broken |
| `evidence_check.py --strict --ledger seal/ledger.md .` at `bcf48b8` then at `2549f7f` | exit 0 — 899 ok · 0 drifted; then **exit 2 — 898 ok · 1 drifted**, `test_the_guard_falls_back_to_the_raw_text_without_the_reader` content changed at 378-452 |
| `evidence_check.py --strict .` unscoped at `bcf48b8` then at `2549f7f` — **run by the orchestrator, not by me** | exit 0 — 899 ok · 0 drifted; then **exit 2 — 906 ok · 1 drifted**. Reconciles with my two narrowed runs row for row: 898 on `seal/ledger.md` plus 8 on the fragment is 906, same drifted row |
| `evidence_check.py --reverify --ledger seal/ledger.md .` | `df85505e -> f0ad0bf1` — the hash this branch's own fragment T1 already carries |
| both proposed cases planted at once, then each arm removed in turn | 31 passed exit 0 shipped; `except ValueError` deleted → the new case fails alone; an attribute-call third pass → the tie's two parameters fail; the same pass with the tie unchanged → 31 passed exit 0 |
| `git cat-file -t` on the four SHAs `overview.md` names as every committed version | `c7fe663` and `6de1bca` — `Not a valid object name`; `341be0b`, `70c272c` — commits, both ancestors of HEAD |
| `## Paste-ready fixes` in each committed version of `round-3.md`, and each of PR #208's three round reports | every record version reads `no paste-ready fix in the report`; round 3's report has no such heading and 0 fences, round 2's has the heading and 2 fences, round 1's has 10 |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_chain_hooks.py` at `2549f7f` | exit 0 — all checks passed; 1 file already formatted |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck — contract §2 leaves the broad gate to one run after the rounds settle | the review orchestrator |

`evidence-check` unscoped over the whole tree came back while this report was
being verified. The orchestrator ran it, it agrees with my two narrowed runs,
and it is in the probes table above marked as theirs. Nothing on this axis is
left unanswered.

## Why finding 1's evidence is seven modules and not one

**An arm claimed unwatched on one module's evidence is a different claim from
an arm measured across every module that references the hook.** The first says
*this module does not watch it*, which nobody needs. The second says *nothing
watches it*, which is the finding. Reading the first as the second is how a
review reports a gap that a case one file over already closes.

So the mutations ran twice. Every one of the 29 went against
`tests/test_chain_hooks.py` alone, the module the spawn prompt named. The
sixteen that came back green then went against the seven modules that `grep`
says reference this hook — 270 cases, and not the suite.

**Two of the sixteen turned red there**, and they are not in this report as a
result:

- `main`'s `if strays:` — watched by `test_a_stray_record_is_named_along_with_where_it_must_go`
- the POST guard's `not records` half — watched by `test_a_stray_record_does_not_also_report_as_missing`

On one module's evidence both would have been written up as unwatched arms.
They are cases that exist, in a file the prompt did not name.

The orchestrator has settled the scope question and is not counting the second
run against contract §2. Recording it here rather than leaving it in a
transcript, because the next round reading finding 1 needs to know which
population the claim was measured over before it trusts the number.

Findings 3 through 8 are located in records and in the ledger, which
`docs/review-chain-spec.md` puts outside `Needs a fix`. Finding 3 is the one
`evidence_check` refuses, so it belongs in the closing commit rather than in a
fix pass.

Needs a fix: yes — findings 1 and 2
Loses a record or crashes: no

## Proof block

Files opened at `2549f7f` unless stated.

| File | Why |
|---|---|
| `hooks/review-history-guard.py` | the unit under review; every arm enumerated and mutated |
| `skills/verify/scripts/unverified_check.py` | `readable`, `blank_fences`, `strip_comments` — the passes the tie derives |
| `tests/test_chain_hooks.py` | the diff's only code file |
| `tests/test_chain_check_at_the_pull_request.py` | to confirm `rounds_unreadable` there loads `routing.py`, not this hook |
| `seal/ledger.md` (R5, line 1385) | the corrected row and its anchors |
| `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md` | T1, T2, T3 |
| `seal/specs/1788844300-…/overview.md`, `changelog.md`, `routing.md` | the branch's own account |
| `seal/specs/1788749195-…/rounds/round-3.md` at `341be0b`, `70c272c`, `701d109` | the corrected record, every committed version |
| `docs/review-chain-spec.md:145-175` | the rule that a finding located in a record is a correction |
| `.github/workflows/test.yml:75-95` | how CI runs the evidence checker |
| `bin/test` | the runner |
| PR #208's three round reports, issues #209 and #210 | the claims the tickets and the round made |
