# Round 3 — the last round of this run

| Field | Value |
|---|---|
| Target SHA | `2c7de851` |
| Fix range verified | `ed85fc2a..2970f694`, two commits |
| Base | `release/v0.12.1` at `5bf22ddb` |
| Reviewed in | a `git clone --no-local` at the target SHA |

## What this round found

**Round 2's two findings are closed, and I re-derived both.** The behavioural
one is decisive: the exact tree that made round 2's gate go quiet now makes it
name the offender.

**The fix pass's own argument is right, and my draft was short by one.** I
left the dict equality behind the decline as a third statement. It is the same
defect one line down, and removing it in favour of a third question loses
nothing — I measured the partition rather than reasoning about it.

**Two things I open, and neither must be fixed before this ships.** The
AST-ordering case pins one degree less than its docstring claims, and the new
`NAME NOT IN TREE` convention is spelled two different ways in the five lines
that introduce it. Both are deferred candidates. The run ends here either way,
and I say so of each rather than leaving the reader to infer it.

---

## The dict equality belonged in front of the decline, and my draft left it behind

**Location** — `tests/test_a_shrunken_corpus_declines_to_judge.py:400`.

The reading is now three questions where my draft had two in front of the
decline and one behind it:

| Question | What it is evidence about | Declines? |
|---|---|---|
| `unaccounted` — a scope found that no table accounts for | a module the reader has just read | no |
| `miscounted_scopes` — a scope on both sides whose call count moved | a module the reader has just read | no |
| `vanished_scopes` — a scope in the table the reader no longer finds | a module that may be off disk | yes |

**The argument holds, and the coordinate is what settles it.**
`miscounted_scopes` iterates `found.items()`. Every key in `found` came from a
module `derivers` opened and parsed, so every key is a module that is on disk.
A skipped module explains nothing about it. That is the same sentence that
justified moving the offender half forward, and it is true of the count half
for the same reason — so leaving `assert found == PATH_LIST_CALLS` behind the
decline, as I drafted it, would have silenced a moved call count on a mid-edit
tree. Round 2's finding one line down, exactly as the pass says.

**Nothing was lost by dropping the dict equality**, and I measured that rather
than arguing it. Over 3000 random readings built from the real table plus
planted keys, every reading that differs from `PATH_LIST_CALLS` is caught by
at least one of the three questions — 0 holes. The three partition the old
assertion: keys only in the reading, keys only in the table, and shared keys
whose values differ.

So the split I drafted was incomplete and the pass corrected it. That is the
verdict on the argument.

---

## ⬜ 1 · The AST-ordering case pins the first mention of a name, not the assertion

**Location** — `tests/test_a_shrunken_corpus_declines_to_judge.py:587`
(`test_the_positive_halves_are_asked_before_the_decline`).

**The instrument is right for the problem.** The defect lived in the sequence
of one function's body, reproducing it needs a module deleted from the running
suite's own tree, and no unit-level case can see an ordering. Reading the
source is the correct answer, and it is what `_catches_oserror` and the class
reader already do in this module. I am not asking for a different instrument.

What it measures is one degree looser than what the docstring claims. The
docstring says what keeps the two positive halves judging is *that they sit in
front of it*; the case finds the first body statement whose dump contains the
string `unaccounted`, and the first containing `miscounted_scopes`, and
asserts those indices precede the `vanished_scopes` one. The assignment is
what carries the name first, so the assertion can move without the case
noticing.

**Executed, both directions:**

| Mutation | The AST case |
|---|---|
| the decline moved back in front of everything — round 2's shape | **exit 1**, red |
| only `assert not unaccounted` moved after the decline, its assignment left in front | **exit 0**, green |

Under the second, the guarded case does go quiet the way round 2 described: on
a tree with one test module off disk and an unguarded scope planted, it skips
instead of naming the scope. The module still exits 1, but through a
neighbour — `test_an_unguarded_scope_is_named_although_a_module_is_mid_edit`
trips because a real unguarded scope joins the one it planted, and its message
is about its own fixture. That is a second net rather than the intended one.

**Why this does not block the release.** The instrument catches the mutation
it was built for, which I ran. The defect it guards is closed, which I
verified behaviourally on the real tree. The gap needs a future refactor that
separates an assert from its assignment, and even then the module goes red.
Tightening it is mechanism, which is not this run's to add.

*A smaller thing in the same unit, folded in here rather than given a row of
its own.* `decline = next(i for i, d in enumerate(dumped) if ...)` has no
default, so if `vanished_scopes` ever leaves that body the case raises
`StopIteration` instead of saying what is wrong. It still goes red, which is
the direction that costs nothing. The suggested form below fixes both at once.
The hardcoded module path in `SELF` is the third of these — a sibling module
derives its own from the file it is in — and it matters least, since a rename
would break the case loudly.

---

## ⬜ 2 · The new marker is spelled two ways in the five lines that introduce it

**Location** — `rounds/round-2.md:31` and `rounds/round-2-report.md:33, 36,
209, 254`, commit `a04d2818`.

**The choice is right and the rule is satisfied.** `skills/evidence-check/SKILL.md`
offers two repairs and correcting the record would falsify what round 2 found,
so the marker is the only honest one. The rule is that the marker exempts the
line it sits on, and all five sit on their line. `evidence-check --strict .`
exits 0 with `0 refused`, which I ran.

What is worth settling, because this sets the convention, is that the five
lines use two different spellings:

- **Two table rows** end the last cell with ` · NAME NOT IN TREE`, which reads
  as a trailing annotation separated from the prose.
- **Three prose lines** append it after a bare space, and two of those three
  end in a colon that introduces a fenced block. The rendered result is
  *…then declines before returning: NAME NOT IN TREE* followed by the code
  the colon was announcing, so the marker sits between a colon and its object.

One spelling for both would fix the colon problem as a side effect: ` · NAME
NOT IN TREE` reads as an aside after a colon, where a bare space reads as the
colon's object.

**This does not block the release either.** The refusal clears, the facts are
right, and it is five reversible lines in my own documents. It is worth
deciding once rather than five times, because the next run that renames a unit
will copy whichever of these two it happens to open first.

---

## Carried forward, each re-derived

**Round 2's first finding — the positive halves now judge what remains.** The
identical probe from round 2: one unguarded scope planted in a tracked test
module, one other tracked test module deleted from disk with the removal
unstaged.

| | round 2, at `e29a0e51` | round 3, at `2c7de851` |
|---|---|---|
| result | exit 0, `13 passed, 2 skipped` | **exit 1**, `2 failed, 14 passed, 1 skipped` |
| the planted scope named | no | **yes** |

The liveness half still declines on the same tree, which is round 1's finding
and is what the one skipped case is. Both directions hold at once, which was
the whole of the split.

**Round 2's second finding — the stale pointer says so where a reader meets
it.** The row now reads *is tracked as #371 (closed; see the correction at the
end of this row)*. The four words are at the first occurrence, which is the
one a reader meets; the second occurrence is inside the appended correction,
where the stale wording is being quoted deliberately, and leaving that one
alone is right. The owner's judgment is still untaken.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The AST-ordering case asserts on the first body statement that mentions a name rather than on the assertion, so moving an assert away from its assignment is not seen | `tests/test_a_shrunken_corpus_declines_to_judge.py:587` | deferred — candidate, does not block | Executed: red at exit 1 under the mutation it was built for; green at exit 0 under the mutation that moves only the assert, while the guarded case goes quiet on a mid-edit tree. Tightening it is mechanism, which a run past its reopening may not add |
| ⬜ 2 | The five lines introducing `NAME NOT IN TREE` use two spellings — ` · ` before it in table cells, a bare space in prose — and two prose lines put it between a colon and the fence that colon introduces | `rounds/round-2.md:31`, `rounds/round-2-report.md:33, 36, 209, 254` | deferred — candidate, does not block | Read, and the refusal verified clear: `evidence-check --strict .` exit 0, `0 refused`. The rule is satisfied at all five; this is the convention the next rename will copy |
| carried | Round 2's first finding — the decline sat in front of the halves that must judge what remains | `tests/test_a_shrunken_corpus_declines_to_judge.py` | confirmed | Executed: the identical round 2 probe gives exit 1 with the planted scope named, where it gave exit 0 with the scope named nowhere. The liveness half still declines on the same tree |
| carried | Round 2's second finding — the stale `#371` pointer sat ahead of its correction | `seal/follow-up.md` | confirmed | Read. The words are at the first occurrence, and the second occurrence is left alone because the correction quotes the stale wording on purpose |
| carried | The removal of `assert found == PATH_LIST_CALLS` in favour of a third question | `tests/test_a_shrunken_corpus_declines_to_judge.py:400` | confirmed | Executed: over 3000 random readings, every reading differing from the table is caught by at least one of the three questions — 0 holes, so the three partition what the dict equality caught. The count half is evidence about a module the reader has just read, so it belonged in front of the decline and my draft was short by one |
| ❓ | The full suite, the repository-wide lint and the typecheck | repository-wide | ❓ out of verified scope | `agent-contract` §2 keeps all three off this agent. Answered by `specseal:sealer`, whose spawn is what follows this record |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local`, checked out at `2c7de851` | clean tree, tip confirmed `2c7de85` |
| `bin/test -q` over the eight modules this work item touches | exit 0, `181 passed` |
| round 2's own probe: an unguarded scope planted in a tracked test module, one other test module off disk with the removal unstaged | exit 1, `2 failed, 14 passed, 1 skipped`, the planted scope named |
| the same probe on a clean tree, after restoring both files | exit 0, `17 passed`, nothing named |
| mutation: the decline moved back in front of everything | the AST-ordering case **red**, exit 1 |
| mutation: only `assert not unaccounted` moved after the decline, its assignment left in front | the AST-ordering case **green**, exit 0 — and the guarded case skips instead of naming the scope |
| 3000 random readings compared against `PATH_LIST_CALLS`, asking whether any differs from it and is caught by none of the three questions | 0 — the three partition the old dict equality |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0, records arm `367 names read · 0 refused · 0 drifted`, so all five markers hold |
| `python3 skills/code-review/scripts/survivor_check.py --range 5bf22ddb..HEAD` | exit 1, the payload-meter file named |
| the same with `--exempt …/survivors.md` | exit 0, one `exempt` line printed |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; it is the sealer's one act, and it comes due now |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Tighten the AST-ordering case to index the `ast.Assert` statements rather than the first mention of a name | this round, ⬜ 1 — a `deferred #N` candidate with no issue yet; the suggested form is below | the repository owner |
| Settle one spelling for `NAME NOT IN TREE` and apply it to the five lines that introduce it | this round, ⬜ 2 — a `deferred #N` candidate with no issue yet | the repository owner |
| The corpus half and the range half of the survivor-exemption silence | already deferred in round 1, to `deferred #308`; `seal/follow-up.md`'s survivor-exemption row carries the live measurement and now flags its own stale pointer | the repository owner |
| Whether #371's closure was meant to cover the range half | already deferred in round 2, to `seal/follow-up.md`, the same row | the repository owner |
| The `SyntaxWarning` at `tests/test_a_row_points_by_content.py:763` | already deferred in round 1, to `overview.md` §*Not done*, which still names no durable home | the repository owner |
| Q1 — whether a path missing from disk should have its index content swept | already deferred in round 1, to `questions.md` Q1 | the repository owner |

## Paste-ready fixes

Neither is owed before this ships. Both are written out so the deferred rows
have something to point at.

**⬜ 1** — index the assertions rather than the first mention, and say what is
wrong when the decline is gone rather than raising `StopIteration`:

```python
def test_the_positive_halves_are_asked_before_the_decline():
    """The ORDER is the fix, and no unit-level case can see it.

    `vanished_scopes` skips the rest of the function when it declines, so what
    keeps the two positive halves judging is that their ASSERTIONS sit in
    front of it. Round 2 🟡 1 was that ordering the other way round.

    Indexed on the `assert` statements rather than on the first mention of
    each name: an assignment carries the name first, so a case reading
    mentions passes while the assertion it is about has moved behind the
    decline -- measured in round 3, green under exactly that mutation.
    """
    body = _function(_tree_of(SELF), GUARDED_CASE).body
    decline = next(
        (i for i, node in enumerate(body) if "vanished_scopes" in ast.dump(node)),
        None,
    )
    assert decline is not None, (
        f"{GUARDED_CASE} no longer calls `vanished_scopes`, so this case is "
        "measuring an order that no longer exists"
    )
    asserted = {
        name: i
        for i, node in enumerate(body)
        if isinstance(node, ast.Assert)
        for name in ("unaccounted", "miscounted")
        if name in ast.dump(node.test)
    }
    for name in ("unaccounted", "miscounted"):
        at = asserted.get(name)
        assert at is not None, f"{GUARDED_CASE} no longer asserts on `{name}`"
        assert at < decline, (
            f"`{name}` is ASSERTED after `vanished_scopes`, so a tree that is "
            "merely mid-edit turns that half of this case off. It is evidence "
            "about a module the reader has just read, and a skip explains "
            "nothing about it — round 2 🟡 1"
        )
```

**⬜ 2** — one spelling, applied to the three prose lines so they match the two
table cells:

```
(`classified_scopes`), consumed at `:380` · NAME NOT IN TREE
```

```
`classified_scopes` computes `found`, then declines before returning · NAME NOT IN TREE:
```

```
`classified_scopes` with · NAME NOT IN TREE:
```

The last two put the marker before the colon so the colon still introduces the
fence it belongs to.

---

Needs a fix: no

Loses a record or crashes: no

---

## What follows

Round 2's findings are closed and verified, this round opens nothing that must
be fixed before the release, and the broad gate has not run. The sealer's
spawn is what comes due — the full suite, the repository-wide lint and the
typecheck, once, at this SHA and compared against the base.

## Proof block

**Executed** — `bin/test -q` over the eight modules (exit 0, 181 passed);
round 2's planted-scope probe on a mid-edit tree and on a clean one, rebuilt
from my own round 2 script rather than reconstructed from the fix pass's
account; two ordering mutations driven from one Python script that locates
each statement by regex, asserts the mutation applied, and compares the
restored bytes; a 3000-reading partition check against the real
`PATH_LIST_CALLS`; `evidence_check.py --strict .`; `survivor_check.py` at the
tip with and without the exemption. Every exit code was read from `$?` or from
a `returncode`, never through a pipe.

**Read** — the whole fix range diff; `round-2.md` as it now stands; the five
marked lines in context; `skills/evidence-check/SKILL.md`'s table of verdicts
and repairs; `seal/follow-up.md`'s survivor-exemption row; the guarded case's
docstring, to check it does not itself carry the names the AST case indexes.

**Unverified** — the fix pass's figures I did not re-run: 171 passed over
eight modules, 292 over six, `ruff`. Answered by `specseal:sealer`. The full
suite, the repository-wide lint and the typecheck stay out of this agent's
scope under `agent-contract` §2.

**Scope** — a verifying round, scoped to the two-commit fix range. I did not
widen.
