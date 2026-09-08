# 1788844300-the-guards-cases-cannot-observe-what-they-guard — review round 1

| Field | Value |
|---|---|
| Target SHA | 2549f7f2c6923de0bd98d04101242f2222eea2ab |
| Ran by | warden on claude-opus-5 |
| PR | 260 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1 and 2 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Six targets, in the order the prompt set them.

1. **The arm enumeration, by construction, past where the branch stopped.**
   The tickets said four arms; the implementer enumerated five out of the
   function's own source, because the except tuple has three members where
   every prose reading had counted two. The round was told to do the
   enumeration itself — on `reader`, on `is_closed`, and on `readable` — and
   carried the warning that this class was found by construction and missed by
   reading seven times on the branch these tickets came from.
2. **The fifth arm's sentence, which stands in place of a case.** The
   implementer's nine-input sweep was handed over as a claim to probe rather
   than read, with the note that a stated limit is exactly what #205 on a
   sibling branch is a ticket about.
3. **The tie, and whether it fails in the direction claimed.** To add a third
   blanking pass and confirm the tie goes red, and then the harder half:
   whether the tie survives a pass being renamed or reordered rather than only
   added.
4. **The branch's in-place edit of another work item's closed round record** —
   whether that is in scope, whether the correction is itself correct when
   re-run against the module as it stood at that commit, and whether anything
   downstream now disagrees with it. Named in the prompt as the likeliest 🟡.
5. **Two tickets state a fact that is false, and the branch says so** — that
   the reviewer's fixes are fenced in that round-3 record. To verify, because
   if the implementer is wrong its two new cases were written from ticket
   prose when an executed version existed.
6. **Whether the rule *reachable arms get a case, unconstructible arms get a
   sentence* is applied consistently** across the parse arm, the import arm
   and the loader arm.

Deliberately out of scope and named as already deferred: the shared reader's
own `blank_fences` and `strip_comments` branches, on the grounds that the
module has its own test file.

Facts carried as executed by the orchestrator at the target SHA: the module at
30 passed exit 0, and ruff check and format at exit 0 over the changed `.py`
file. Carried from a sibling branch of this release: a `.pyc` keys on source
mtime in whole seconds plus size, so two same-length mutations written inside
one second reuse the earlier one's bytecode.

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |
