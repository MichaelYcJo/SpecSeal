# Round 2 — verifying round 1's fixes

Target: the fix diff `246c65b..59dcffe`, three commits, HEAD `59dcffe`, on
`fix/318-the-one-script-an-agent-is-told-to-run-cannot-be-typed`. Round 1
reviewed `8208928`; everything before `246c65b` is already reviewed and I did
not re-open it.

Round 1's seven verdicts are all closed, and I measured each rather than
reading the fix commits for it. Two findings are new, both on the one surface
this round was told to judge as code rather than as a fix: the hyphen guard in
`reachable` and the case that pins it. Three more are corrections.

## The seven verdicts are closed

- **🟡 1** — the guard is in `reachable` and it works. `reachable` answers
  false for `seal.py` against a locator-free line and true against the path.
  The unfalsifiability is gone for that script.
- **🟡 2** — `os.access(posix, os.X_OK)` is asserted, and I drove it red rather
  than reading it: `chmod 644` on `bin/round-record` in a clone takes the
  module from `30 passed, 8 skipped, exit 0` to `1 failed, 29 passed`, naming
  the executable bit; restoring the mode returns it to exit 0. That is §15
  discharged for the assertion, which nothing in the tree had recorded.
- **🟡 3** — the `NO_WRAPPER` reason now says *shown with a flag in none of
  them* and names `templates/config.md` as the place the detector cannot see.
  The user-facing half stands unfixed, which is `spec.md` §Out's standing
  refusal and not an omission.
- **🟡 4** — `agents/warden.md` carries the path at line 140, inside the first
  mention's own sentence at 138. The pinned phrase survives whole.
- **🟡 5** — `skills/implement/SKILL.md:521` reads *The generator that row
  names*.
- **⬜ 6** — five invokers, and I checked all five rather than accepting them.
  Three carry the path by hand; `skills/verify/scripts/broad_gate.py` runs it
  as a subprocess at line 577 with `CHAIN` built at 130; `round_record.py`
  loads it as a module at line 245 from the path built at 207. The class of
  copies is four, not five: I swept the work item for the claim in any
  wording and found no fifth live copy. `plan.md:82`'s late correction was
  the last one.
- **⬜ 7** — `seal/ledger.md` is untouched by this diff, so the deferral to
  #387 stands as round 1 left it.

## The guard closes one hole and opens a smaller one — the message

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:275`.

The locator case fails with *Add either reachable form, once: the command
`{command}`, or the path `{script}`*. That message is built from the same
`command_name` the guard reads, and for a one-word command the first half of
it is no longer true. **Executed**: with the message printed beside the
reader, `reachable` answers false for every form of the command it offers —

```
  the message: … Add either reachable form, once: the command `seal`, or the
               path `skills/implement/scripts/seal.py`
  reachable('Run `seal --record <item>` after the rounds settle.')  = False
  reachable('The sealer types `seal`.')                            = False
  reachable('seal')                                                = False
  reachable('It lives at `skills/implement/scripts/seal.py`.')     = True
```

So a reader who meets this failure, does what it says, and re-runs is still
red, with no way to tell why. That is #318's own shape — a document telling
somebody to reach for something that is not there — reproduced inside the fix
for #318.

This is not a loose end the plan left open; it is a property the plan claims.
`plan.md` §*Failure scenario of the chosen approach* names two things aimed at
the six-month failure, and the first is *the pin's message names both accepted
forms and the document, so the correct repair is the one in front of the
reader*. For `seal.py` it no longer does.

The comment the fix added is wrong in the same direction.
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:139-142`
says those scripts *are reachable by path only*. They are not: `bin/seal` and
`bin/seal.cmd` both ship, `seal` resolves on PATH, and the wrapper pair is
one of the twelve. What is true is narrower — this reader cannot tell the
command from the sentence, so it asks for the path. The fix wrote a property
of the detector as a property of the script, which is the substitution round 1
raised as 🟡 3 one function away.

Two docstrings above it now overstate for the same reason, and both are in the
same file: `reachable`'s own (*Either accepted form counts*) and the module's
stated rule (*carries the command or the script's repo-relative path*).

## The premise underneath it is leaky, and there is a live coordinate

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143`.

The guard treats the hyphen as what separates a command from an English word.
That is not what a hyphen does. A hyphenated command name reads as an ordinary
compound modifier in prose, and this repository's own documents already write
several that way.

**Executed**, every wrapped script against all 43 shipped documents, looking
for the command token present with no path anywhere: `broad-gate` in nine
documents, `evidence-check` in eight, `unverified-check` in four,
`survivor-check` in three, `arm-check` and `deferral-check` in one each. Most
are real typed commands in code fences, which is the accepted form working as
designed. One is not:

```
  agents/warden.md:247: - **Carry the broad-gate state into your report** …
  reachable(agents/warden.md, skills/verify/scripts/broad_gate.py) = True
```

`agents/warden.md` does not name `broad_gate.py` today, so no case is wrong —
which is exactly what round 1 said about `seal.py`. The day that file names
the script, the pin reports it as covered on the strength of a sentence that
tells nobody the script exists. §12 asks for the class and the fix took one
member of it.

**I do not have a reader that fixes this, and I measured one rather than
proposing it from reading.** Accepting the bare command only where something
follows it — the tell this same file already calls *the only sound one in
prose* for `command_forms` — is either too loose or too strict: widened to a
flag, a placeholder or a following word it still passes *the seal after the
rounds* and *the broad-gate state*; narrowed to a flag alone it turns
`skills/code-review/orchestration.md` red for `evidence_check.py`, a live pair
that is green for a good reason.

So this is fix or justify and the justification is available: the heuristic is
a bound, not a rule, and the alternative costs a live pair. What it should not
do is stand unstated in a file whose subject is documents that claim more than
they check. The paste-ready fix below states the bound rather than changing the
reader.

## The executable bit is asserted for one more wrapper, and seven still have nobody

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231`.

The residue handed to me was four — `arm-check`, `broad-gate`, `payload-meter`
and `seal-stamp`. **Executed**, over all twelve `bin/` pairs and every
executable-bit assertion in `tests/`: the residue is seven.

| Wrapper | Who asserts the executable bit |
|---|---|
| `deferral-check`, `unverified-check` | a dedicated module |
| `evidence-check`, `round-record` | a dedicated module, and the new class assertion |
| `session-cost` | the new class assertion, and nothing before it |
| `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test` | nobody |

The three the handover's figure missed are `seal`, `survivor-check` and
`test`. `bin/seal` and `bin/survivor-check` have file-existence assertions in
other modules and no mode assertion; `bin/test` wraps
`.github/scripts/run_tests.py`, which is not a skill script, so this pin can
never reach it. `os.access` is the only idiom in use — I checked the
alternatives (`st_mode`, a literal mode, running the wrapper) and found none
guarding a `bin/` pair.

**The gap is not a defect of this pin.** The new assertion sits inside a case
that skips any script no shipped document names, and eight of the twelve skip.
That skip is the pin's design, and a script nobody is sent looking for is
outside what this module governs. The number is worth correcting because it is
the number a later reader would use to decide whether the class is covered,
and because it was measured twice already in this work item and came in wrong
both times.

## The invoker sentence reads as an enumeration and is not one

`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70-76`.

*Every place that invokes it carries its full path — A, B and C by hand, and D
and E in code.* The five are right. The list reads closed, and at least twelve
test modules also load `chain_check.py` by full path —
`tests/test_the_reopening_is_one.py:30`,
`tests/test_chain_check_at_the_pull_request.py:24` and
`tests/test_the_record_is_generated.py:35` among them.

Nothing is misled about the conclusion: every one of them carries the path
too, so *reachable everywhere it is reached* holds harder rather than less.
What it needs is one phrase saying where the list stops. This is the third
reading of the same sentence in this work item and the second thing about it
that has been short; a bound on the enumeration is what stops a fourth.

## A correction note split a table in half

`seal/specs/…/plan.md:83-95`.

The note explaining `plan.md:82`'s late correction is placed inside the
*Alternatives considered* table: line 82 is a row, 83 is blank, 84–93 are the
comment, 94 is blank, and 95 is the table's last row — *A rule in
`CONTRIBUTING.md` and no test*. A markdown table ends at the first blank line,
so line 95 has no header above it any more and renders as a paragraph of
literal pipes rather than as a row. **Read**, from the line structure; I ran
no renderer.

The note itself belongs in the file and its content is right. It belongs below
the table, where `spec.md`'s equivalent note sits inside a bullet and breaks
nothing.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The locator rule cannot fail for `seal.py` | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143` | answered | Closed. **Executed** 2026-09-14 at `59dcffe`: `reachable` is false for `seal.py` against a locator-free line and true against the path. The new case is in the file and green |
| 🟡 2 | The class pin asserts the file and the twin and not the executable bit | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231` | answered | Closed. **Executed** 2026-09-14: `chmod 644` on `bin/round-record` in a clone takes the module from exit 0 to `1 failed, 29 passed` naming the executable bit, and restoring the mode returns exit 0 — §15 for this assertion, which nothing in the tree had recorded |
| 🟡 3 | `NO_WRAPPER` claimed *invoked in none of them* where *followed by a flag* is what is asserted | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | answered | Closed. **Read** 2026-09-14: the reason now says *shown with a flag in none of them* and names `templates/config.md`. The user-facing half of the finding is `spec.md` §Out's standing refusal, not an omission |
| 🟡 4 | `agents/warden.md` named the generator 48 lines before it said where it is | `agents/warden.md:138` | answered | Closed. **Executed** 2026-09-14: the file's `round_record.py` mentions are at 138, 184, 292, 352 and 381, and the path now sits at 140, inside the first mention's own sentence (a second path was already at 188). `test_the_rules_have_one_owner.py` and `test_docs_line_wrap.py` were green at `5a8f6ac`, so the pinned phrase survived whole |
| 🟡 5 | *The generator both rows name* — one row names it | `skills/implement/SKILL.md:521` | answered | Closed. **Read** 2026-09-14: the line reads *The generator that row names* |
| ⬜ 6 | *All three places that DO invoke it* undercounts | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | answered | Closed. **Executed** 2026-09-14: all five verified individually — three by hand, `broad_gate.py:577` as a subprocess, `round_record.py:245` as a module load. The class of copies is four; I swept the work item for the claim in any wording and found no fifth |
| ⬜ 7 | Eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | `seal/ledger.md` | answered | Unchanged by this diff; the deferral to #387 stands as round 1 left it |
| 🟡 8 | The locator failure message names a repair that does not work for a one-word command, and the comment beside the guard calls a wrapped script *reachable by path only* | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:275` · `:142` | open | **Executed** 2026-09-14: `reachable` is false for `seal`, for `` `seal --record <item>` `` and for `` `seal` `` in prose, while the message the case prints offers the command as an accepted form. `bin/seal` and `bin/seal.cmd` both ship, so *reachable by path only* is false. `plan.md` §*Failure scenario* claims the message names both accepted forms |
| 🟡 9 | The hyphen is not what separates a command from prose, and `agents/warden.md:247` already carries `broad-gate` as an ordinary compound | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:143` | open | **Executed** 2026-09-14, every wrapped script against all 43 documents: `reachable(agents/warden.md, broad_gate.py)` is true today on the strength of line 247 alone. No case is wrong because that file does not name the script — which is what round 1 said about `seal.py`. Fix or justify: I measured the obvious alternative reader and it is either too loose or reds `skills/code-review/orchestration.md` for `evidence_check.py` |
| ⬜ 10 | The executable-bit residue is seven, not the four the handover named | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:231` | open | **Executed** 2026-09-14 over all twelve `bin/` pairs and every exec-bit assertion in `tests/`: `seal`, `survivor-check` and `test` are also unasserted. The new assertion newly covers exactly one wrapper, `session-cost`. Not a defect of the pin — the case skips any script no shipped document names, and that skip is its design |
| ⬜ 11 | *Every place that invokes it* reads as a closed list and omits at least twelve test modules that load it by full path | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py:70` | open | **Executed** 2026-09-14: `tests/test_the_reopening_is_one.py:30`, `tests/test_chain_check_at_the_pull_request.py:24`, `tests/test_the_record_is_generated.py:35` and nine more build the same path. The conclusion holds harder, not less; the enumeration needs a bound |
| ⬜ 12 | The correction note sits inside the *Alternatives considered* table and orphans its last row | `seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md:83` | open | **Read** 2026-09-14: line 82 is a row, 83 blank, 84–93 the comment, 94 blank, 95 the last row. A table ends at the first blank line, so line 95 renders as literal pipes. Under `seal/specs/`, so a correction rather than a fix to commission |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_document_that_names_a_script_says_how_to_reach_it.py -q` in a clone at `59dcffe` | exit 0, 30 passed, 8 skipped |
| the same module with `bin/round-record` chmod'd to `644`, then restored | `1 failed, 29 passed, 8 skipped`, exit 1, the failure naming the executable bit; exit 0 again after restoring `0755` — §15 for the assertion 🟡 2 commissioned |
| every `bin/` pair cross-referenced against every executable-bit assertion in `tests/` | five asserted, seven not: `arm-check`, `broad-gate`, `payload-meter`, `seal`, `seal-stamp`, `survivor-check`, `test`. The new assertion adds exactly one, `session-cost` |
| `reachable` for `skills/implement/scripts/seal.py` against the command, the command with a flag, the bare word, and the path | false, false, false, true — and the failure message the case prints offers the command as an accepted form |
| every wrapped script against all 43 shipped documents, for the command token present with no path | `broad-gate` in nine documents, `evidence-check` in eight, `unverified-check` in four, `survivor-check` in three, `arm-check` and `deferral-check` in one. `agents/warden.md:247` carries `broad-gate` as prose |
| an alternative reader accepting the bare command only where something follows it, over the thirteen live pairs | widened it still passes *the seal after the rounds*; narrowed to a flag alone it reds `skills/code-review/orchestration.md` for `evidence_check.py`. Not proposable |
| the five `chain_check.py` invokers, each opened | `broad_gate.py:577` runs it as a subprocess from the path at `:130`; `round_record.py:245` loads it as a module from the path at `:207`; three carry it by hand. All five carry the full path |
| the work item swept for the invoker claim in any wording | four copies, all corrected. No fifth |
| `tests/` swept for executable-bit idioms other than `os.access` | none guarding a `bin/` pair |
| the broad gate — the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's single act under `skills/agent-contract/SKILL.md` §2 and no segment in this round has taken it |

Carried rather than re-run, from the orchestrator at `59dcffe`: six modules at
`5a8f6ac` (249 passed, 8 skipped, exit 0) and `survivor-check --range
246c65b..HEAD` exit 0. Nothing between `5a8f6ac` and `59dcffe` touches code, so
the module results still hold; I re-ran the pin at `59dcffe` anyway because my
findings sit in it.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 7 — eleven `seal/ledger.md` rows re-stamped with unmoved `Checked` dates | #387, as round 1 deferred it | the repository owner |

## Paste-ready fixes

🟡 8 — `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`, the
comment inside `reachable`, replacing the four lines the fix added:

```python
    # A command name with no hyphen in it cannot be told from ordinary
    # English -- `seal.py` answers to `seal`, and this repository's prose is
    # made of that word -- so this reader does not take the bare form as a
    # locator for it. The command is real and `bin/seal` ships; what is
    # missing is a way to tell the command from the sentence, so for those
    # scripts the path is the form that counts.
```

and the body of `test_a_document_naming_a_wrapped_script_says_how_to_reach_it`,
so the repair it names is one that works:

```python
    document, script = pair
    command, text = command_name(script), read(os.path.join(ROOT, document))
    forms = (
        f"the path `{script}`. `{command}` has no hyphen in it, so this rule "
        "does not read the bare command as a locator -- see `reachable`"
        if "-" not in command
        else f"either reachable form: the command `{command}`, or the path "
        f"`{script}`"
    )
    assert reachable(text, script), (
        f"{document} names {os.path.basename(script)} and never says where it "
        f"is. A reader who goes looking finds nothing, which is #318. Add "
        f"{forms}, once"
    )
```

🟡 9 — same file, appended to the comment above, stating the bound rather than
changing the reader:

```python
    # The hyphen is a bound and not a rule: a hyphenated command reads as an
    # ordinary compound in prose too, and `agents/warden.md:247` writes
    # `broad-gate` that way today. That file names no script, so no case is
    # wrong -- but the day it names `broad_gate.py`, this reader calls it
    # covered on the strength of that sentence. Measured 2026-09-14: a reader
    # that accepts the bare command only where something follows it either
    # passes the same prose or turns `skills/code-review/orchestration.md`
    # red for `evidence_check.py`, so the bound stays and is written down.
```

⬜ 11 — same file, the invoker sentence of the `NO_WRAPPER` row, bounded:

```python
        "Every place outside `tests/` that invokes it carries its full path "
        "-- `.github/workflows/hygiene.yml`, `templates/hygiene.yml` and "
        "`docs/release-checklist.md` by hand, and "
        "`skills/verify/scripts/broad_gate.py` and this skill's own "
        "`round_record.py` in code; the test modules that load it build the "
        "same path -- so it is reachable everywhere it is reached. "
```

⬜ 12 — `seal/specs/…/plan.md`: move lines 83-94 (the blank line, the comment
and the blank line after it) to below line 95, so the table is contiguous and
the note follows it.

Needs a fix: yes — 🟡 8

Loses a record or crashes: no

🟡 8 is the one that cannot be answered with grounds: there is no reading under
which *Add the command `seal`* is correct advice, and the branch's own
`plan.md` names that message as a deliverable. 🟡 9 is fix or justify and the
justification is available — the heuristic is a bound and the alternative
costs a live pair — so it needs an answer rather than an edit. ⬜ 10, ⬜ 11 and
⬜ 12 are corrections; ⬜ 12's location is under `seal/specs/`, which
`agents/warden.md` §Role puts outside `Needs a fix` on its own.

Nothing found here leaves a record outside the root and nothing crashes. The
one thing needing a fix is a failure message that misinstructs a reader who
will not exist until somebody writes a one-word script into a shipped
document.

## Proof

Opened at `59dcffe`: the full diff `246c65b..59dcffe`;
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` entire;
`agents/warden.md` (the changed block and every generator mention);
`skills/implement/SKILL.md:518-522`;
`skills/verify/scripts/broad_gate.py` (lines 120-145, 460-470, 570-625);
`skills/code-review/scripts/round_record.py:200-250`;
`skills/evidence-check/SKILL.md` (the command-form lines);
`templates/config.md:165`; `bin/test`; `git ls-tree HEAD bin/`;
`tests/test_docs_line_wrap.py`'s `COVERED` list;
`seal/specs/…/` — `spec.md`, `plan.md`, `questions.md`, `overview.md`,
`changelog.md`, `phases/phase-3.md`, `rounds/round-1.md`,
`rounds/round-1-report.md`; the three fix commit messages.

Work done in a `git clone --no-local` at `59dcffe` under the session
scratchpad, with the virtual environment the repository's own runner builds
for reuse. Nothing was written in the checkout except this file. The clone and
four throwaway probe scripts, named as the contract asks, were deleted before
this report was handed over.
