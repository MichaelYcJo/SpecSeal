# Round 1 — review report

| Field | Value |
|---|---|
| Work item | `1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible` |
| Branch | `fix/203-204-205-206-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible` |
| Target SHA | `909647b43a51d13387768aa7533113a3b4130bc5` |
| Base | the release branch this work item is cut for, at `bcf48b8` (= `origin/main`). Named by SHA rather than by number: this report is written while the branch edits the check that refuses a version at or above the running one |
| Reviewed in | a `git clone --no-local` of the repository at the target SHA |
| Broad gate | not yet — the full suite, the repository-wide lint and the typecheck are the orchestrator's, once, after the rounds settle |

## How the findings relate

One cause produces the first three, and the branch names that cause itself: a
record that states a limit nobody measured, which then stands as grounds for
looking no further.

```
① the enumeration stopped one short again — two deletions inside `refusal`
   leave the module at 32 passed
        ↓ recorded as complete
② four documents say all seven elements are pinned, one of them the ledger
   fragment that folds into the shared file at the release
        ↓ and in the same breath
③ the sentence that replaced the old false limit carries a new one —
   "pinning it would mean reading this file's own source", disproved by
   writing the pin
④ separate, same class — a ledger row cites a document as stating the check's
   rule correctly, and that document states the rule the check replaced
⑤ cosmetic — the fixture writes the running version as a literal where the
   module has a constant for it
```

Four of the seven axes the round was asked to attack came back clean and are
recorded as such below the findings, with what I ran rather than what I read.

---

## ① The enumeration stopped one short again, and this time it is not a separator

**🔴 `tests/test_release_hygiene.py:350-358`**

`refusal` is four operands joined by three `+`. The first operand is one
f-string built from four adjacent string literals, and the case reads it with
two substring spot-checks. Between those two substrings sit 86 characters that
no assertion reads.

I mapped every character of `refusal("0.8.3", [first, second])` against the
seven assertions. 103 of 1186 characters are read by nothing, in three runs:

```
UNREAD (16 chars): ' Such a line is '
UNREAD (86 chars): ": it goes red on the day that version ships, on the release's own preparation commit, "
UNREAD  (1 char) : '.'
```

Two deletions inside that gap leave the module green. Each was run on its own,
with `tests/__pycache__` cleared between and the file restored from bytes read
before the first write:

| Deletion | Result |
|---|---|
| the whole literal `"it goes red on the day that version ships, on the release's own "` | **32 passed, exit 0** |
| `preparation commit, ` from the literal after it | **32 passed, exit 0** |
| control — the literal `"Such a line is right for exactly one release and a timer before it: "` | 1 failed, 31 passed |

The surviving deletions are not cosmetic. The first one takes away *when* the
line goes red, which is the half an author acts on; the second leaves the
sentence reading *"…a timer before it: preparation commit, after the broad gate
has already run."*

**Why the enumeration produced seven and not eight.** The plan and the phase-2
record both say the count was taken by construction. It was not, quite. Parsing
`refusal` gives four operands, and the first is a single `JoinedStr` of three
parts:

```
operand 1: JoinedStr
    part 1: Constant 'a loaded file names a version at or above the running '
    part 2: FormattedValue 'running'
    part 3: Constant ". Such a line is right … has already run.\n  "
operand 2: Call  '\n  '.join(offenders)
operand 3: Constant '\n\n'
operand 4: Call  what_to_write_instead()
```

Part 3 is one element, and the branch split it by reading — into "the paragraph"
and "the `\n  ` that closes the first literal" — then pinned the paragraph half
with two substrings taken from its two ends. Construction handed over one
element; reading turned it into two and read neither of them whole. That is the
same move the three attempts on the original branch made, one level down.

**A fourth survivor, reported for completeness.** Rewriting `refusal` so the
routes paragraph is emitted before the offender lines also leaves the module at
32 passed. Nothing here asks for the order to be pinned — doing that fully means
rebuilding `refusal` in the test, which `plan.md` rejected for good reasons —
but the corrected survivor sentence should say so rather than name one thing.

The paste-ready fix below reads the paragraph as two contiguous halves, so the
two failure messages survive and nothing between them is unread. Applied, the
module stays at **32 passed**, all three deletions above turn it red, and
`ruff check` / `ruff format --check` stay at exit 0.

## ② And four records say the enumeration is complete

**🟡 `seal/ledger/1788844200-…-v-is-invisible.md:16` · `seal/ledger.md:1356` ·
`seal/specs/…/changelog.md:19` · `tests/test_release_hygiene.py:311`**

Each of these states finding ① as settled fact:

- the ledger fragment's S2 clause — *"every element of the text the version
  check prints is read by an assertion"*. This row folds into `seal/ledger.md`
  at the release, where it becomes the standing claim.
- `seal/ledger.md` R3 — *"`test_the_refusal_prints_every_piece_it_builds` pins
  each on its own"*.
- the changelog fragment — *"All seven of its elements … are now pinned one at
  a time"*. This one ships to users.
- the case's own docstring header — *"Seven elements … each pinned on its own"*.

The seven mutations the branch ran were real and all seven were caught; that
part of every sentence is true. What is not measured is the word *every*. Once
finding ①'s fix is in, four of these become true as written and only the
survivor sentence needs the correction below.

## ③ The sentence that replaced a false limit carries a new one

**🟡 `tests/test_release_hygiene.py:333-334`**

The docstring says of the check's own `assert` line:

> no assertion here reads it, and **pinning it would mean reading this file's
> own source**.

`seal/ledger.md` R3 records that this repository has written that sentence
before, that review round 2 corrected it once, and that #203 exists because it
came back. It has come back again, in the paragraph that explains why it must
not.

It is also false, and disproving it took ten lines and no source reading. Both
seams are module globals the module already swaps in another case:

```
the check raised, and its message == refusal(): True
```

`tracked` returns one path, `timers_in` returns one offender, the check is
called, and the `AssertionError` it raises is compared to `refusal(running,
offenders)`. Nothing reads the file.

The minimal fix is to say what was measured instead of what is impossible; the
larger one is to plant the case, since it is now written. Both blocks are below.
Which to take is the orchestrator's call — the smaller one is inside #203's
scope, the larger one is new mechanism.

## ④ A ledger row cites, as a document that states the rule correctly, the one that states the rule this check replaced

**🟡 `seal/ledger/1788844200-…-v-is-invisible.md:18`**

S4's evidence cell reads:

> `docs/release-checklist.md`'s table row and `docs/flow.md`'s sentence about
> #179 going red on the commit that raises the version both already state it
> correctly and were left alone

`docs/release-checklist.md:80` does state it correctly. `docs/flow.md:30` reads:

> #179 had to be in 0.9.0, because it goes red on the commit that raises the
> version to 0.9.0 and nowhere earlier.

In its own context that sentence is right — it explains why the ticket was
forced into that release, and *"goes red on the commit that raises the version"*
is the behaviour of the equality check #179 replaced. Read as a statement of
what the check does now, it is the old rule: the check refuses a version at or
above the running one on the commit that **writes** it, which is the whole point
of #179 and what #206 just corrected one document over.

So S4's clause — *"the three documents naming that check agree"* — rests on a
sentence that does not name the check and describes its predecessor. A reader
auditing that agreement later opens `docs/flow.md:30` and finds the
contradiction the row says is not there. Leaving `docs/flow.md` unedited is
right (`spec.md` puts it out of scope, and it is a record of a moment); what
needs correcting is the sentence that claims it as evidence.

## ⑤ The fixture writes the running version as a literal

**⬜ `tests/test_release_hygiene.py:339`**

`running = "0.8.3"`, where the module defines `RUNNING_IN_THE_FIXTURES = "0.8.3"`
with a comment saying why a fixture must not read `plugin.json`. Module-level
names resolve at call time, so the constant is usable from a case defined above
it — every other fixture in the module uses it. Nothing behaves differently
either way.

---

## What held

**The seven-element claim's other half.** All seven mutations the branch names
were re-run here independently and every one was caught. The `"\n  "` closing
the first literal — the separator three attempts missed — turns the case red on
its own deletion. Two offenders in the fixture is the right call: with one, the
join's separator is unobservable.

**The lookaround argument covers both characters, and reaches the decision.**
The `\w` half is argued (`py3.13.9` names CPython — a preceding word renames the
token) and the `.` half is argued separately (`1.9.9.9`'s tail would otherwise be
refused as a version the line never named). The asymmetry with the trailing side
is stated. The uppercase decision follows from both: a `V` is a prefix, not a
preceding word, so neither argument reaches it and the fix widens `v?` instead
of touching a lookaround.

**Neither lookaround was narrowed.** Diffed character by character:
`(?<![\w.])` and `(?!\.\d)` are byte-identical to the base. The only change is
`v?` → `[vV]?`.

**§15 holds for the new case.** Reverting `[vV]?` to `v?` turns exactly
`test_an_uppercase_v_is_a_prefix_and_not_a_preceding_word` red — 1 failed,
31 passed — and nothing else.

**The widening's measurement reproduces exactly.** Enumerated over all 64 loaded
files under both patterns: 78 raw tokens before, 79 after; exactly one token
admitted, `docs/flow.md:101` `V0.9.0`; none lost; the offender list empty under
both. Both stated reasons that token is not an offender hold independently —
`is_a_record_of_a_moment('docs/flow.md')` is `True`, and the version is below
the running one so the comparison is `False`. Either alone is sufficient.

**#205's deletion is right and its replacement sentence is true.** The four
arrangements through both implementations, in both orders:

| Arrangement | `any()` as-is | `any()` reversed | early-return as-is | early-return reversed |
|---|---|---|---|---|
| exact path under a wider prefix | True | True | **False** | **True** |
| narrower prefix, undated file | False | False | False | False |
| narrower prefix, dated file | True | True | True | True |
| wider prefix only, dated file | True | True | True | True |

The exact-path row is the only one where the implementations differ and the only
one whose answer moves with order. A narrower prefix never changed an answer, in
either implementation, in either order. **No assertion was added** — the case
body is byte-identical to the base; only the docstring changed.

**#206's sentence protects the line it has to.** `docs/issues-and-milestones.md`
now states at-or-above with the below-the-running half beside it, and names the
use: *"it is what lets this document say further down which release an issue
shipped in"*. That line is `:164`, further down the same file, and both versions
it carries are below the running one, so it is kept. The handoff's coordinate
`docs/flow.md:51` is about how a release is sized; the #179 sentence is at
`:30`. The implementer's report of both is correct.

**The `seal/ledger.md` edits are the case `CONTRIBUTING.md` sanctions.** §House
rules says in as many words that *"Changing cited code … is not an append"* and
that a row whose cited content drifted while the claim still holds is
re-verified in place. Two of the three edited rows are exactly that. The third,
R1, is a prose correction with no drift — `CONTRIBUTING.md` does not name that
case, and there is no mechanism by which a fragment could correct a row already
folded into the shared file, so the act was the only correct one available.
Worth a sentence in `CONTRIBUTING.md` eventually; nothing to fix here.

**The order of measurement was honest.** At `84c1b1c`, before phase 3's ledger
edits, the scoped check reports exactly one drifted row —
`test_the_message_has_a_route_for_every_token_the_check_refuses`, phase 2's own
edit. The second drift is the docs heading phase 3 itself edited in the same
commit. Both are units this work item re-read; `--reverify` re-stamped no row
nobody here opened. Only three of 899 rows changed, and every one is named in
the phase record.

## What I did not judge

**The full suite, the repository-wide lint and the typecheck.** Not run —
`skills/agent-contract/SKILL.md` §2. The orchestrator answers them, once, after
the rounds settle. The branch's own module and its lint are clean at the target
SHA (below).

**The early-return implementation `#205` was measured against** is reconstructed
from the docstring that describes it, not the historical bytes. The overview
says so and names the orchestrator. My table above has the same limitation and
the same answerer.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The seven-element enumeration reads the timer paragraph with two end-anchored substrings and leaves 86 characters between them unread; two deletions inside `refusal` leave the module at 32 passed | `tests/test_release_hygiene.py:350-358` | open | Executed: both deletions run one at a time, `tests/__pycache__` cleared between, file restored from bytes — 32 passed, exit 0 each. Control deletion of the adjacent literal: 1 failed, 31 passed. Character-coverage map: 103 of 1186 chars read by no assertion. AST parse: operand 1 is one `JoinedStr` of three parts, so the split into "paragraph" and "closing `\n  `" was made by reading, not by construction |
| 2 | Four records state the enumeration as complete — the ledger fragment's S2 clause, `seal/ledger.md` R3, the changelog fragment, and the case's own docstring header | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md:19` · `tests/test_release_hygiene.py:311` | open | The seven mutations named are real and all seven were caught here too; the unmeasured word is *every*. The fragment row folds into `seal/ledger.md` at the release, and the changelog fragment ships to users. This is the class the branch exists to close, in the branch's own new rows |
| 3 | The paragraph correcting the old false limit introduces a new one — *"pinning it would mean reading this file's own source"* | `tests/test_release_hygiene.py:333-334` | open | Executed: the check's `assert` message pinned without reading any source, by swapping `tracked` and `timers_in` (module globals this module already swaps in another case) and comparing the raised `AssertionError` to `refusal(running, offenders)` — equal, True. `seal/ledger.md` R3 records this sentence being written and corrected once before |
| 4 | Ledger fragment row S4 cites `docs/flow.md:30` as a document already stating the check's rule correctly; that sentence states the equality rule #179 replaced | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | open | Read: `docs/flow.md:30` says #179 *"goes red on the commit that raises the version to 0.9.0 and nowhere earlier"* — correct as scheduling rationale about the predecessor check, and the opposite of what the check now does. `docs/flow.md` is the only other document S4 counts toward the three-way agreement besides `docs/release-checklist.md:80`, which does state it correctly |
| 5 | The new fixture writes the running version as a literal where the module has `RUNNING_IN_THE_FIXTURES` for it | `tests/test_release_hygiene.py:339` | open | Read: the constant is defined at `:448` with the comment saying why a fixture must not read `plugin.json`; module globals resolve at call time, so a case above it can use it, and every other fixture does. No behaviour difference |
| 6 | All seven mutations the branch names are caught; the `"\n  "` closing the first literal — the separator three earlier attempts missed — turns the case red on its own deletion | `tests/test_release_hygiene.py#refusal` | answered | Executed independently, one at a time with `tests/__pycache__` cleared between: `{running}` deletion, offender-join deletion, join separator, leading separator, `"\n\n"`, routes call, and the control literal — every one red |
| 7 | Neither lookaround was narrowed, and the argument beside `VERSION_TOKEN` covers both characters and reaches the uppercase decision | `tests/test_release_hygiene.py#VERSION_TOKEN` | answered | Read: `(?<![\w.])` and `(?!\.\d)` byte-identical to the base; the only change is `v?` → `[vV]?`. Executed: reverting the widening turns exactly `test_an_uppercase_v_is_a_prefix_and_not_a_preceding_word` red, 1 failed / 31 passed |
| 8 | The widening admits exactly one new token in the loaded set and loses none, and both reasons that token is not an offender hold | `docs/flow.md:101` | answered | Executed: 64 loaded files under both patterns — 78 raw tokens before, 79 after; admitted `('docs/flow.md', 101, 'V0.9.0')`; lost nothing; 0 offenders under both. `is_a_record_of_a_moment('docs/flow.md')` = True; the version compares below the running one = False. Either is sufficient on its own |
| 9 | #205's replacement sentence is true and no assertion was added | `tests/test_release_hygiene.py:544-556` | answered | Executed: four arrangements × two implementations × two orders. Only the exact-path arrangement differs between implementations (True/False) and only it moves with order; every narrower-prefix arrangement is identical in all four columns. The case body is byte-identical to the base — only the docstring changed |
| 10 | #206's sentence leaves `docs/issues-and-milestones.md:164` reading as protected, and the handoff's coordinate was wrong as the implementer reported | `docs/issues-and-milestones.md:66-71` · `docs/flow.md:30` | answered | Read: the corrected paragraph names the below-the-running half and the use it protects; `:164` carries `release/v0.3.0` and `0.2.0`, both below the running version. `docs/flow.md:51` is about release sizing; the #179 sentence is at `:30` |
| 11 | Editing `seal/ledger.md` directly, and re-verifying only what was re-read | `seal/ledger.md:1136` · `:1355` · `:1356` | answered | Read: `CONTRIBUTING.md` §House rules sanctions touching a drifted row in the shared file and forbids only appending. Executed: at `84c1b1c` the scoped check reports exactly one drifted row, phase 2's own edit; the second drift is phase 3's own docs edit. Three of 899 rows changed, all named in the phase record |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at the target SHA, in a fresh `git clone --no-local` | 32 passed, exit 0 |
| `ast.parse` of `refusal`, flattening the `+` chain and printing every operand and `JoinedStr` part | 4 operands; operand 1 is one `JoinedStr` of 3 parts, its third part carrying the whole timer paragraph and the trailing `"\n  "` |
| 11 mutations of `refusal` and of the check's `assert`, each on its own, `tests/__pycache__` cleared between, file restored from bytes read before the first write | 4 survivors: deleting the literal `"it goes red on the day that version ships, on the release's own "` (32 passed), deleting `preparation commit, ` (32 passed), the check's `assert` handed a literal (32 passed), and emitting the routes before the offender lines (32 passed). The other 7 caught |
| Character-coverage map of `refusal("0.8.3", [first, second])` against the eight substrings the case's assertions read | 103 of 1186 characters read by nothing, in three runs — 16, **86**, and 1 characters |
| The proposed fix for finding 1 applied, then the three deletions re-run | 32 passed unmutated; all three deletions now 1 failed / 31 passed; `ruff check` and `ruff format --check` exit 0 |
| Pinning the check's own `assert` line without reading the file's source — `tracked` and `timers_in` swapped for one offender, the raised `AssertionError` compared to `refusal(running, offenders)` | equal — True |
| Enumeration over all 64 loaded files under `v?` and under `[vV]?`, tokens and offenders both | 78 → 79 raw tokens; admitted exactly `('docs/flow.md', 101, 'V0.9.0')`; lost nothing; 0 offenders under both |
| Both stated reasons the admitted token is not an offender, checked separately | `is_a_record_of_a_moment('docs/flow.md')` = True; the version compares below the running one = False |
| `[vV]?` reverted to `v?`, module re-run | 1 failed, 31 passed — `FAILED test_an_uppercase_v_is_a_prefix_and_not_a_preceding_word`, nothing else |
| Four `RECORDS_OF_A_MOMENT` arrangements through the `any()` implementation and an early-return reconstruction, each in both orders | Only the exact-path arrangement differs between implementations and only it moves with order; narrower-prefix arrangements identical in all four columns |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict --ledger seal/ledger/1788844200-…-v-is-invisible.md .` | 6 ok · 0 drifted · 0 broken, exit 0 |
| the same, `--ledger seal/ledger.md` | 899 ok · 0 drifted · 0 broken, exit 0 |
| the same, at `84c1b1c` — the commit before phase 3's ledger edits | 1 drifted, exit 2 — `tests/test_release_hygiene.py#test_the_message_has_a_route_for_every_token_the_check_refuses`, and nothing else |
| `uvx ruff check tests/test_release_hygiene.py` and `uvx ruff format --check` on it | All checks passed, exit 0; 1 file already formatted, exit 0 |

All probe files were deleted; the clone's tree is clean at the target SHA and
nothing was written in the branch's own worktree except this report.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Nothing pins the three documents naming this check agreeing with each other, which is #206's underlying class | `seal/specs/1788844200-…/questions.md` Q1, and stated in ledger fragment row S4 | the review orchestrator, or the repository owner it asks — already recorded, not re-opened here |
| `as_release`'s `lstrip("v")` does not strip an uppercase `V` | `seal/specs/1788844200-…/overview.md` §Not done and `phases/phase-1.md` | already argued unreachable and confirmed here — `as_release` has exactly two call sites, `as_release(running)` and `as_release(bare)` with `bare = match.group(1)`, neither of which can carry a prefix. No finding |
| The early-return implementation the arrangements were measured against is reconstructed from the docstring, not the historical bytes | `seal/specs/1788844200-…/overview.md` §Not verified | the review orchestrator, if the reverted branch's intermediate commits can be fetched. My table carries the same limitation |
| `CONTRIBUTING.md` §House rules does not name the case of correcting a false note in a `seal/ledger.md` row that has not drifted | nowhere yet — offered as a candidate for `seal/follow-up.md` | the repository owner. The act taken on this branch was the only correct one available; the rule is what is silent |

## Paste-ready fixes

**Finding 1 — read the paragraph whole.** Replace the two assertions at
`tests/test_release_hygiene.py:350-358`. The two halves are contiguous, so
together they cover the paragraph from the `.` that follows the running version
through `run.`, and each still names which half went. Measured: 32 passed
unmutated, all three deletions red, ruff clean.

```python
    # The paragraph WHOLE, in two contiguous halves. Two substring
    # spot-checks used to read only its ends, and 86 characters between them
    # were read by nothing: deleting `"it goes red on the day that version
    # ships, on the release's own "`, or just `preparation commit, `, each
    # left this module at 32 passed (round 1).
    assert (
        ". Such a line is right for exactly one release and a timer before "
        "it: it goes red on the day that version ships," in text
    ), (
        "the reason went: the text says a line is refused and not why, which "
        "is the half that stops the next author writing another one"
    )
    assert (
        " on the release's own preparation commit, after the broad gate has "
        "already run." in text
    ), (
        "the timer's cost went — it fires on the release's own preparation "
        "commit, hours in, and that is what makes this worth a check rather "
        "than a convention"
    )
```

**Findings 1 and 3 — the docstring.** Replace
`tests/test_release_hygiene.py:311-312` and `:331-337`. The first block makes
the count honest about where it came from; the second names the survivors that
were actually measured, and drops the sentence that says the first of them
cannot be pinned.

```python
def test_the_refusal_prints_every_piece_it_builds():
    """Seven elements, enumerated from `refusal`'s own source, each read
    whole rather than at its ends.
```

```python
    **The survivors of that measured set are two, and neither is a limit.**
    The check's own last line, `assert not offenders, refusal(running,
    offenders)` handed a literal, leaves this module at 32 passed; so does
    emitting the routes before the refused lines, which nothing here pins
    because pinning the order fully means rebuilding `refusal` in the test.
    Round 1 found a third and it is closed above: the timer paragraph used to
    be read by two substrings taken from its ends, and 86 characters between
    them were read by nothing. That is what a survivor list is for — what is
    absent from a measured list is unmeasured, and this module has three
    times written the larger claim into a record where it then stood as
    grounds for looking no further.
    """
```

**Finding 3, the larger option — plant the case.** Only if the orchestrator
wants the mechanism rather than the wording. It reads no source; it swaps two
module globals the way the exemption-order case already does. Verified here
against the branch as it stands: the raised message equals `refusal(...)`.

```python
def test_the_check_prints_the_refusal_it_builds():
    """The one element the case above leaves to a survivor list.

    `assert not offenders, refusal(running, offenders)` can be handed a
    literal with every other case still green — measured, round 1. Nothing
    about pinning it needs this file's own source read: the check reaches the
    tree through two module globals, and swapping them is what
    `test_the_exemption_list_does_not_depend_on_the_order_it_is_written_in`
    already does one constant over.
    """
    running = version()
    real_tracked, real_timers = tracked, timers_in
    try:
        globals()["tracked"] = lambda *prefixes: ["README.md"]
        globals()["timers_in"] = lambda rel, text, run: [(1, "9.9.9")]
        try:
            test_no_loaded_file_names_a_version_at_or_above_the_running_one()
        except AssertionError as raised:
            assert str(raised) == refusal(running, ["README.md:1 names 9.9.9"]), (
                "the check no longer prints what `refusal` builds — the "
                "routes, the reason and the refused lines can all be right "
                "and reach nobody"
            )
        else:
            raise AssertionError("the check did not refuse an injected offender")
    finally:
        globals()["tracked"] = real_tracked
        globals()["timers_in"] = real_timers
```

**Finding 2 — the ledger fragment's S2 clause.** Replace the clause cell at
`seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16`.

```
| S2 · the text the version check prints is read whole by assertions, element by element: the running version and the sentence naming it, the paragraph saying why such a line is a timer — read across its full length rather than at its ends — the refused lines, the routes out, and each of the three separators that join them
```

And append to that row's Verified cell, after the existing sentence:

```
 **Round 1 found the paragraph read at its ends only**: deleting the literal `"it goes red on the day that version ships, on the release's own "`, or just `preparation commit, `, each left the module at 32 passed, and a character map put 86 of the paragraph's characters outside every assertion. Two contiguous assertions now cover it end to end; both deletions turn the case red
```

**Finding 2 — `seal/ledger.md` R3.** In the row at `seal/ledger.md:1356`,
replace the clause *"`test_the_refusal_prints_every_piece_it_builds` pins each
on its own"*:

```
`test_the_refusal_prints_every_piece_it_builds` reads each of them whole, which round 1 is what made true: the paragraph had been read at its two ends and 86 characters between them by nothing, so two deletions inside it left the module at 32 passed
```

**Finding 2 — the changelog fragment.** Replace
`seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md:19-22`.

```markdown
  the half a person acts on first and no test would say so. Every one of its
  elements — four pieces and the three separators that join them — is now read
  by an assertion, and read whole rather than sampled at its ends, so a
  sentence cannot lose its middle silently. Each was seen red on its own
  deletion before the case was committed.
```

**Finding 4 — the ledger fragment's S4 evidence cell.** Replace the clause at
`seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18`
that reads *"`docs/release-checklist.md`'s table row and `docs/flow.md`'s
sentence about #179 going red on the commit that raises the version both already
state it correctly and were left alone"*:

```
`docs/release-checklist.md`'s table row states it correctly and was left alone. `docs/flow.md:30` does NOT state this rule and was left alone for a different reason: its sentence — #179 *"goes red on the commit that raises the version … and nowhere earlier"* — is the behaviour of the equality check #179 replaced, written as scheduling rationale for why the ticket was forced into that release, and it is correct as that. So the documents that state the rule are two, not three, and the third names the ticket rather than the check
```

**Finding 5 — use the constant.** At `tests/test_release_hygiene.py:339`:

```python
    running = RUNNING_IN_THE_FIXTURES
```

---

The two terminal lines. Finding 1 is the case leaving two deletions inside
`refusal` unobserved; findings 2 and 3 are records stating a completeness and a
limit that measurement disproves; finding 4 is a ledger row citing a document
that states the superseded rule. Finding 5 is cosmetic and is not counted.
Nothing found here leaves the root, drops a record or raises: the refusal text
is a test-time message, the records are prose, and the module is green at the
target SHA.

Needs a fix: yes — findings 1, 2, 3 and 4: two deletions inside `refusal` go unobserved, and three records state that as complete

Loses a record or crashes: no

## Proof block

Opened, at `909647b43a51d13387768aa7533113a3b4130bc5`:

- `tests/test_release_hygiene.py` (whole)
- `docs/issues-and-milestones.md` — `:39` heading, `:50-90`, `:164`
- `docs/flow.md` — `:20-60`, `:95-105`
- `docs/release-checklist.md:80`
- `seal/ledger.md` — the word-diff against the base, and rows G5, R1, R3 in full
- `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md` (whole)
- `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/` — `routing.md`, `spec.md`, `plan.md`, `overview.md`, `questions.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`
- `CONTRIBUTING.md` §House rules
- `CLAUDE.md` — the fragment rule and the merge-method rule
- `seal/follow-up.md` — §Schedulable items with nowhere else to go
- `bin/test`
- `skills/evidence-check/scripts/evidence_check.py` — the usage block and `--reverify`

No earlier `round-N.md` exists for this work item; nothing was carried.
