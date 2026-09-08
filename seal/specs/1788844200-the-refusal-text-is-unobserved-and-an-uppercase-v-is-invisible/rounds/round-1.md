# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — review round 1

| Field | Value |
|---|---|
| Target SHA | 909647b43a51d13387768aa7533113a3b4130bc5 |
| Ran by | warden on claude-opus-5 |
| PR | 259 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1, 2, 3 and 4: two deletions inside `refusal` go unobserved, and three records state that as complete |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Seven targets, in the order the prompt set them.

1. **The seven-element claim, enumerated by construction rather than read.**
   Named as the ticket's own trap: three consecutive attempts on the original
   branch each enumerated the elements and each stopped one short. The round
   was told that eight would be the finding, and told not to take the
   implementer's table.
2. **The survivor, and how it is recorded.** Whether the message-expression
   survivor is the only one, and whether any wording on the branch slips back
   into calling it unpinnable. Carried: this file has twice had a false limit
   written into a ledger row that then stood as grounds for looking no
   further, and #205 on this branch is one of the two.
3. **The lookaround argument, both characters** — the `\w` half and the `.`
   half, which does a different job. Whether the argument reaches the
   uppercase decision, and whether either lookaround was narrowed. Carried:
   the original branch's round-1 finding was a lookaround narrowed for one
   shape taking another with it.
4. **What the widening admits, re-measured rather than taken.** The
   implementer's enumeration of 64 loaded files, and the two independent
   reasons the one newly admitted token is not an offender — both to be
   checked, because a claim resting on two reasons where one is false breaks
   when the other changes.
5. **#205's deletion and the instruction to add nothing.** That no assertion
   was added, and that the replacement sentence is true.
6. **#206's sentence against the line it protects** — that
   `docs/issues-and-milestones.md`'s later line about a release branch
   shipping under another number reads as protected rather than as an
   oversight. The handoff's coordinate `docs/flow.md:51` was given, and the
   round was asked to verify which line actually states the rule.
7. **The branch's direct edits to `seal/ledger.md`**, against the repository
   rule that a change writes fragments — the implementer's grounds being that
   the rule forbids appending and a correction is not an append — and whether
   drift was measured before `--reverify` rather than after.

Facts carried as executed by the orchestrator at the target SHA: the module at
32 passed exit 0, and ruff check and format at exit 0 over the changed `.py`
file. The implementer's seven-element mutation table, its reverted-widening
red, and its 249-passed adjacent run were handed over labelled as its claims.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The seven-element enumeration reads the timer paragraph with two end-anchored substrings and leaves 86 characters between them unread; two deletions inside `refusal` leave the module at 32 passed | `tests/test_release_hygiene.py:350-358` | **fixed** `9aadedf` | fixed at 9aadedf — ``; Executed: both deletions run one at a time, `tests/__pycache__` cleared between, file restored from bytes — 32 passed, exit 0 each. Control deletion of the adjacent literal: 1 failed, 31 passed. Character-coverage map: 103 of 1186 chars read by no assertion. AST parse: operand 1 is one `JoinedStr` of three parts, so the split into "paragraph" and "closing `\n  `" was made by reading, not by construction |
| 2 | Four records state the enumeration as complete — the ledger fragment's S2 clause, `seal/ledger.md` R3, the changelog fragment, and the case's own docstring header | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md:19` · `tests/test_release_hygiene.py:311` | answered | corrected at `9aadedf` (docstring) and `2bce8ab` (ledger fragment S2 · `seal/ledger.md` R3 · changelog fragment) |
| 3 | The paragraph correcting the old false limit introduces a new one — *"pinning it would mean reading this file's own source"* | `tests/test_release_hygiene.py:333-334` | answered | corrected at `9aadedf` |
| 4 | Ledger fragment row S4 cites `docs/flow.md:30` as a document already stating the check's rule correctly; that sentence states the equality rule #179 replaced | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | answered | corrected at `2bce8ab` |
| 5 | The new fixture writes the running version as a literal where the module has `RUNNING_IN_THE_FIXTURES` for it | `tests/test_release_hygiene.py:339` | **fixed** `9aadedf` | fixed at 9aadedf — ``; Read: the constant is defined at `:448` with the comment saying why a fixture must not read `plugin.json`; module globals resolve at call time, so a case above it can use it, and every other fixture does. No behaviour difference |
| 6 | All seven mutations the branch names are caught; the `"\n  "` closing the first literal — the separator three earlier attempts missed — turns the case red on its own deletion | `tests/test_release_hygiene.py#refusal` | answered | Executed independently, one at a time with `tests/__pycache__` cleared between: `{running}` deletion, offender-join deletion, join separator, leading separator, `"\n\n"`, routes call, and the control literal — every one red |
| 7 | Neither lookaround was narrowed, and the argument beside `VERSION_TOKEN` covers both characters and reaches the uppercase decision | `tests/test_release_hygiene.py#VERSION_TOKEN` | answered | Read: `(?<![\w.])` and `(?!\.\d)` byte-identical to the base; the only change is `v?` → `[vV]?`. Executed: reverting the widening turns exactly `test_an_uppercase_v_is_a_prefix_and_not_a_preceding_word` red, 1 failed / 31 passed |
| 8 | The widening admits exactly one new token in the loaded set and loses none, and both reasons that token is not an offender hold | `docs/flow.md:101` | answered | Executed: 64 loaded files under both patterns — 78 raw tokens before, 79 after; admitted `('docs/flow.md', 101, 'V0.9.0')`; lost nothing; 0 offenders under both. `is_a_record_of_a_moment('docs/flow.md')` = True; the version compares below the running one = False. Either is sufficient on its own |
| 9 | #205's replacement sentence is true and no assertion was added | `tests/test_release_hygiene.py:544-556` | answered | Executed: four arrangements × two implementations × two orders. Only the exact-path arrangement differs between implementations (True/False) and only it moves with order; every narrower-prefix arrangement is identical in all four columns. The case body is byte-identical to the base — only the docstring changed |
| 10 | #206's sentence leaves `docs/issues-and-milestones.md:164` reading as protected, and the handoff's coordinate was wrong as the implementer reported | `docs/issues-and-milestones.md:66-71` · `docs/flow.md:30` | answered | Read: the corrected paragraph names the below-the-running half and the use it protects; `:164` carries `release/v0.3.0` and `0.2.0`, both below the running version. `docs/flow.md:51` is about release sizing; the #179 sentence is at `:30` |
| 11 | Editing `seal/ledger.md` directly, and re-verifying only what was re-read | `seal/ledger.md:1136` · `:1355` · `:1356` | answered | Read: `CONTRIBUTING.md` §House rules sanctions touching a drifted row in the shared file and forbids only appending. Executed: at `84c1b1c` the scoped check reports exactly one drifted row, phase 2's own edit; the second drift is phase 3's own docs edit. Three of 899 rows changed, all named in the phase record |

## Paste-ready fixes

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
```
| S2 · the text the version check prints is read whole by assertions, element by element: the running version and the sentence naming it, the paragraph saying why such a line is a timer — read across its full length rather than at its ends — the refused lines, the routes out, and each of the three separators that join them
```
```
 **Round 1 found the paragraph read at its ends only**: deleting the literal `"it goes red on the day that version ships, on the release's own "`, or just `preparation commit, `, each left the module at 32 passed, and a character map put 86 of the paragraph's characters outside every assertion. Two contiguous assertions now cover it end to end; both deletions turn the case red
```
```
`test_the_refusal_prints_every_piece_it_builds` reads each of them whole, which round 1 is what made true: the paragraph had been read at its two ends and 86 characters between them by nothing, so two deletions inside it left the module at 32 passed
```
```markdown
  the half a person acts on first and no test would say so. Every one of its
  elements — four pieces and the three separators that join them — is now read
  by an assertion, and read whole rather than sampled at its ends, so a
  sentence cannot lose its middle silently. Each was seen red on its own
  deletion before the case was committed.
```
```
`docs/release-checklist.md`'s table row states it correctly and was left alone. `docs/flow.md:30` does NOT state this rule and was left alone for a different reason: its sentence — #179 *"goes red on the commit that raises the version … and nowhere earlier"* — is the behaviour of the equality check #179 replaced, written as scheduling rationale for why the ticket was forced into that release, and it is correct as that. So the documents that state the rule are two, not three, and the third names the ticket rather than the check
```
```python
    running = RUNNING_IN_THE_FIXTURES
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Nothing pins the three documents naming this check agreeing with each other, which is #206's underlying class | `seal/specs/1788844200-…/questions.md` Q1, and stated in ledger fragment row S4 | the review orchestrator, or the repository owner it asks — already recorded, not re-opened here |
| `as_release`'s `lstrip("v")` does not strip an uppercase `V` | `seal/specs/1788844200-…/overview.md` §Not done and `phases/phase-1.md` | already argued unreachable and confirmed here — `as_release` has exactly two call sites, `as_release(running)` and `as_release(bare)` with `bare = match.group(1)`, neither of which can carry a prefix. No finding |
| The early-return implementation the arrangements were measured against is reconstructed from the docstring, not the historical bytes | `seal/specs/1788844200-…/overview.md` §Not verified | the review orchestrator, if the reverted branch's intermediate commits can be fetched. My table carries the same limitation |
| `CONTRIBUTING.md` §House rules does not name the case of correcting a false note in a `seal/ledger.md` row that has not drifted | nowhere yet — offered as a candidate for `seal/follow-up.md` | the repository owner. The act taken on this branch was the only correct one available; the rule is what is silent |
