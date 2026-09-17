# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 195877f0 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Close #432 at its own coordinate and establish the fixture shape the other
four helpers copy. `tests/test_no_real_identifiers.py#tracked_text_files`
takes a root, skips a listed path that is not on disk, and counts the skip;
both callers at `:48` and `:64` keep judging what remains. The module gains
its first can-fail case, on a fixture repository holding a
tracked-and-deleted file and a refused domain in a file that is present.
Acceptance is `bin/test -q tests/test_no_real_identifiers.py` at exit 0 read
directly, each new case seen red against the unguarded helper, and the
module's baseline pass count recorded — which is also half of Q4.

## What this phase found

**The guard has two homes, not one, and the split is what phase 2 copies.**
The existence filter went into `tests/conftest.py#on_disk`, shared, and the
root argument went into each helper. Splitting it that way is what makes the
four sibling helpers a one-line change each: they gain a `root` parameter and
a call, and nothing about the predicate is retyped. The three names this
phase introduces are `on_disk`, `shrunken_corpus` and `decline_if_shrunken`,
plus `build_tracked_tree` for the fixture; the last three exist for phase 3,
which is the phase that has to decline rather than judge.

**A can-fail case for this sweep cannot use either designated fixture value,
and that is not a loophole in `CLAUDE.md`'s rule.** The case has to plant a
token the sweep REFUSES, and `example.com` — every spelling of it, subdomains
included — is what the sweep allows. What it plants instead is
`fixture.example.net`: RFC 2606 reserves `example.net` in the same sentence
as `example.com`, so it is a domain nobody can ever register, and it is not
in `ALLOWED_DOMAINS`. The user-path case takes the same shape with
`/Users/someone/` against the allowed `/Users/x/`. Both literals sit in
`tests/test_no_real_identifiers.py`, which the sweep leaves out of its own
corpus by the line three functions above them, so neither is a real
identifier and neither is swept.

**The formatter deletes an import the same edit has not reached a user for
yet.** Adding `from conftest import build_tracked_tree, on_disk` in one edit
and the calls in the next left the import unused for the length of one tool
call, and the `PostToolUse` formatter removed it — the module then failed
with five `NameError`s that had nothing to do with the work. The import goes
in the edit that uses it, or back afterwards.

**Q4, first half.** The module's baseline is **2 passed**, `bin/test -q
tests/test_no_real_identifiers.py`, exit 0 read from `$?`. It stands at 5
passed after this phase. #432's *3736 passed* is a suite-wide aggregate and
is still unverified here; phase 5 records what the suite actually holds.

**§15, how each case was shown red.** `tests/conftest.py#on_disk`'s one
classifying line was replaced, the module run, and the line restored from
bytes kept by the probe rather than from HEAD:

| Mutation | What went red |
|---|---|
| `present.append(rel)` — the guard removed, which is the code as it stood | both survival cases, each with the `FileNotFoundError` on `seal/ledger/folded.md` that #432 reports. Exit 1, 2 failed 3 passed |
| `missing.append(rel)` — every listed path called missing | all three new cases. Exit 1, 3 failed 2 passed |

Two mutations rather than one, because they fail for opposite reasons.
`test_the_sweeps_still_report_nothing_on_a_clean_fixture` pins an ABSENCE —
that the guard does not buy its survival by dropping files that are there —
and deleting a guard cannot redden a case about over-filtering.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tracked_text_files` as a generator yielding paths | It returns a pair now. Both callers in the module were rewritten in the same commit; no other module imported it |
| The two sweep bodies' inline walk over `ROOT` | `domains_in(root)` and `user_paths_in(root)`, which the cases call with a fixture root. The two `test_` functions keep their refusal text unchanged |
