# 1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built — review round 2

| Field | Value |
|---|---|
| Target SHA | 5a6ad96bfc8ac923dc4e6d55cf99195cf094df2b |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 486 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `cd4ed9dee5af3afd8f44e6700ed4e0373f91506d..8007512602cf1ad8d3437b1dca2e7130654746a7`, 2 commits |
| Contract changes | none |
| New units | comment_scan (depth 1); opens_outside_a_comment (depth 1); test_a_marked_item_still_on_disk_is_not_the_fold_being_complete (depth 1); test_the_fold_is_complete_still_prints_when_it_is (depth 1); test_a_fenced_marker_in_the_ledger_opens_no_section (depth 1); test_an_opted_out_repository_is_told_which_state_it_is_in (depth 1); test_the_released_at_refusal_is_about_the_ref_and_nothing_else (depth 1); test_the_module_and_the_skill_both_say_local_mode_is_refused (depth 1); test_surveys_docstring_does_not_invite_the_mutation_that_reopens_finding_4 (depth 1); test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record (depth 1); test_every_comment_shape_a_policy_document_can_carry (depth 1); test_one_comment_scanner_serves_both_readers (depth 1); test_readable_would_erase_every_fold_record (depth 1) |
| Needs a fix | yes — findings 1 through 7. Finding 1 is the fold's only safety property and is round 1's own 🔴 half-closed; 2, 3, 4 and 7 are what the new code tells a reader; 5 is the same class one function over; 6 is the docstring that invites the next editor to undo finding 4's repair. |
| Loses a record or crashes | yes — finding 1 removes a work item's directory under `seal/specs/` with no policy document having absorbed it, measured at exit 0, which is the one loss `skills/settle/SKILL.md` §4 says nothing can undo. |

- [x] Pass

## What this round was asked

The verifying round, against the diff of round 1's fixes rather than the
branch — two commits, `73ca11d1..f27f7e86`. Round 1's record reads `Fixes
checked by: nobody`, and closing that is what this round is for: for each
verdict round 1 recorded as closed, is it actually closed.

Three of round 1's seven fixes departed from the reviewer's paste-ready
patches on the builder's own judgment, and those three were named as where the
round earns its keep: the fence reader reused rather than written fresh, local
mode refused rather than resolved, and `retire` re-reading the tree rather than
trusting `survey`'s classification. Two cases the fix pass reported correcting
were named too — a case edited to agree with the code it was pinning is how a
suite goes green over a defect.

The one surface exempt from *the answers, not new findings* is what round 1's
`New units` row names: eleven units nobody has reviewed, treated as a finding
surface. The class to enumerate was every one of them against the mutation that
should turn it red.

Corrections handed over: the five further ledger re-stamps in `f27f7e86`, a
`## Not verified` row corrected rather than closed, the two deferrals as
settled rather than reopenable, and the orchestrator's own judgment that the
fix range's eleven survivor places are code idiom rather than statements —
handed over as overturnable.

The broad gate was withheld; it is the sealer's one act.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A marker inside a commented-out HTML block still satisfies the removal guard — the half of round 1's finding 1 the fence fix does not reach | `skills/verify/scripts/unverified_check.py:668` · `skills/settle/scripts/settle.py:497` | **fixed** `83d1f664` | fixed at 83d1f664; executed — `settle --retire` removed `seal/specs/1700000001-alpha/` at exit 0 with the only prose naming it commented out |
| 🟡 2 | `retire` prints *The fold is complete.* at exit 0 while a marked work item still has its directory; the arm fires on `if marked:` and the sentence asserts something narrower | `skills/settle/scripts/settle.py:482` | **fixed** `83d1f664` | fixed at 83d1f664; executed — the message printed and the directory was still on disk |
| 🟡 3 | The new local-mode refusal is in neither the module's exit-code list nor `skills/settle/SKILL.md`; §14's other half | `skills/settle/scripts/settle.py:52` · `skills/settle/SKILL.md` | **fixed** `83d1f664` | fixed at 83d1f664; read — the list names three exit-2 causes and there are now four; a grep for *local mode* in the skill returns nothing |
| 🟡 4 | The new comment claims the local-mode sentence is *reachable at last*; that clause sits behind the `--released-at` refusal, which local mode now returns before | `skills/settle/scripts/settle.py:559` · `:585` | **fixed** `83d1f664` | fixed at 83d1f664; read — `:563` returns 2 before `survey` is called, so `released()` never returns None in local mode |
| 🟡 5 | `coordinates` sections `seal/ledger.md` by marker line with no fence tracking — the remaining instance of finding 1's class, where `fold_ledger.py` tracks one | `skills/settle/scripts/settle.py:299` | **fixed** `83d1f664` | fixed at 83d1f664; read — 94 marker lines and 0 fences in `seal/ledger.md` today, so it is reachable and not live |
| 🟡 6 | `survey`'s docstring still says the retirement is derived from it and warns against the second traversal `retire` now performs | `skills/settle/scripts/settle.py:354` | **fixed** `83d1f664` | fixed at 83d1f664 — the docstring is rewritten and pinned. One sub-point was judged and not taken: `present` stays in `retire`'s intersection, because it is what keeps `shutil.rmtree` from being handed a path that is gone, and dropping it makes a destructive call depend on an invariant another function held at another moment. It also stopped being inert in this pass, since `stranded` is `marked & present`. The reason is in the docstring; read — `retire:454-465` documents the opposite; `present` at `:472` is also inert |
| 🟡 7 | An opted-out repository is told it has no `seal/specs/` at either place; `home_at` returns `""` for the opt-out and for no root alike | `skills/settle/scripts/settle.py:545` · `hooks/optin.py:200` | **fixed** `83d1f664` | fixed at 83d1f664; executed — exit 2 with that sentence against a tree holding a work item directory |
| ⬜ 8 | The S1 row says *eight shapes are parametrised*; the list has seven | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | **fixed** `80075126` | fixed at 80075126; read — `x-1` through `x-7`, and the run reports seven parametrised cases |
| 🟢 confirmation | Round 1 finding 1, the fenced shape: closed, across every fence shape named for this round | `skills/verify/scripts/unverified_check.py:668` | confirmed closed | executed — five shapes, and reverting the reader turns six cases red |
| 🟢 confirmation | The rejection of `readable()`: it really would erase every fold record | `skills/verify/scripts/unverified_check.py:97` | confirmed | executed — `readable()` blanks a genuine marker to the empty string |
| 🟢 confirmation | Round 1 finding 2, the recursive `docs/` walk: closed | `skills/verify/scripts/unverified_check.py:658` | confirmed closed | executed — the below-the-top-level case reddens on revert |
| 🟢 confirmation | Round 1 finding 3, and refusing local mode is the right reading of the two | `skills/settle/scripts/settle.py:545` · `:563` | confirmed closed | executed from a real local-mode layout; proceeding would leave the second quiet zero |
| 🟢 confirmation | Round 1 finding 4, and `retire` deriving its own candidate set is sound | `skills/settle/scripts/settle.py:376` · `:472` | confirmed closed | executed — reverting the candidate set reddens `test_retire_refuses_an_item_the_guard_is_holding`, a case the fix pass did not touch |
| 🟢 confirmation | Round 1 finding 5, and the correction to `test_an_interrupted_run_resumes` is a repair | `skills/settle/scripts/settle.py:482` · `tests/test_settle_reads_before_it_removes.py:244` | confirmed closed | executed — the vacated arm was planted as its own case, red when the new arm fires unconditionally; see finding 2 for what the repair introduced |
| 🟢 confirmation | Round 1 finding 7, the space before the comma | `skills/verify/scripts/unverified_check.py:894` | confirmed closed | executed — the case reddens on revert |
| 🟢 confirmation | Round 1 finding 8, the `Ran by` row | `overview.md:83` | confirmed closed | read — the row is ✅ and `unverified-check` counts it closed |
| 🟢 confirmation | Every one of the eleven new units reddens under a named mutation | `tests/test_settle_reads_before_it_removes.py` · `tests/test_unverified_rows_close.py` · `tests/test_a_script_says_which_interpreter_it_needs.py` | confirmed | executed — nine mutations, re-derived rather than carried |
| 🟢 confirmation | The five ledger re-stamps are real re-reads against the edit that drifted each row | `seal/ledger.md` · `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md` | confirmed | read — `main` moved `b7493a67` → `da6df86a`; every note names what changed and it matches the diff |
| 🟢 confirmation | The corrected `## Not verified` row is true and the count still passes | `overview.md:82` | confirmed | executed — `unverified-check` exit 0, 3 open · 1 closed |
| 🟢 confirmation | The orchestrator's survivor judgement over the fix range | the eleven places the fix-range run names | confirmed | executed — branch-range run exit 0; eight are the `os.walk` idiom, two are the name `found`, the eleventh is `report` reading `found["folded"]`, which is correct |
| ⬜ | Round 1 finding 6, deferred to #487 — the deferral was the right call | `skills/settle/scripts/settle.py:218` | deferred #487 | already deferred in round 1; a walk comparing two functions' source pins nothing findings 1–5 wrote |
| ⬜ | Round 1 finding 9, deferred to #488 — the deferral was the right call | `CLAUDE.md` §*a change writes fragments, never the shared file* | deferred #488 | already deferred in round 1; a rule change to the repository owner's file |
| ❓ scope | The broad gate | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers |

## Paste-ready fixes

```python
def opens_outside_a_comment(lines):
    """True for each line that BEGINS outside an HTML comment.

    `strip_comments` cannot answer this, and `readable` is why it cannot be
    used here: it blanks a comment's content, and a fold marker IS a comment,
    so a genuine record and a marker inside a commented-out draft both come
    back empty. What tells the two apart is the state the line STARTED in.
    Measured 2026-09-22: a `docs/` document with a draft section commented out
    around a real marker retired the directory at exit 0, nothing absorbed.
    That is the other half of the shape the fence blanking closed — a fence is
    one way a line stops being live and an enclosing comment is the other."""
    out, inside = [], False
    for line in lines:
        out.append(not inside)
        rest = line
        while rest:
            if inside:
                end = rest.find("-->")
                if end == -1:
                    rest = ""
                else:
                    rest, inside = rest[end + 3 :], False
            else:
                start = rest.find("<!--")  # -->
                if start == -1:
                    rest = ""
                else:
                    rest, inside = rest[start + 4 :], True
    return out
```
```python
        lines = blank_fences(text.splitlines())
        for bare, line in zip(opens_outside_a_comment(lines), lines):
            if bare:
                found.update(FOLD_MARKER.findall(line))
```
```python
        stranded = sorted(marked & present)
        if marked and not stranded:
            out.write(
                f"nothing left to retire: docs/ records the fold of "
                f"{len(marked)} work item{plural(len(marked))}, and none of "
                f"them still has a directory under {SPECS}/. "
                "The fold is complete.\n"
            )
            return 0
        if stranded:
            # The sentence above asserts that no marked item still has a
            # directory, and the arm used to fire on `if marked:`, which never
            # asked. An item marked in `docs/` and still on disk reaches here
            # when it is not present at `--released-at` — a policy absorbing
            # work that has not merged yet, or a run pointed at an older ref.
            out.write(
                f"nothing to retire: docs/ records the fold of "
                f"{len(stranded)} work item{plural(len(stranded))} whose "
                f"directory is still under {SPECS}/, and none of them is "
                f"present at the release ref, so nothing here reads as "
                "released:\n"
            )
            for work_item_id in stranded:
                out.write(f"    {work_item_id}\n")
            return 1
```
```python
Exit codes: 0 the report was produced, or the retirement ran · 1 a retirement
was asked for and something refused it · 2 the arguments or the tree were
unusable, which includes a `--released-at` ref that does not resolve, a root
with no `seal/specs/` at either place, a `seal/` root in local mode, and an
interpreter below the floor.

**Local mode is refused rather than reported on.** The root under the common
git directory is never committed, so no ref holds the work item directories,
nothing in them reads as released, and nothing removed from them could be
recovered. `seal mode shared` moves the root into the tree.
```
```python
    # named here. The sentence written for local mode lives behind the
    # `--released-at` refusal below, and it stays unreachable — that branch
    # fires only for a ref that does not resolve, and this returns first. So
    # the clause is removed from there and the state is stated here instead.
    # It is the right answer as well as the honest one: nothing removed from a
    # root git never held can be recovered.
```
```python
            f"settle: --released-at {args.released_at} does not resolve in {root} — nothing was "
            "read. Without it every work item reads as unreleased and this "
            "would report nothing to fold, which is the one answer it must "
            "not give by accident.\n"
```
```python
    if os.path.isfile(ledger):
        with open(ledger, encoding="utf-8") as f:
            current, fence = None, None
            for line in f:
                head = line.lstrip()
                run = re.match(r"^(`{3,}|~{3,})", head)
                if fence is None and run:
                    fence = run.group(1)
                    continue
                if fence is not None:
                    if run and run.group(1)[0] == fence[0] and len(run.group(1)) >= len(fence):
                        fence = None
                    continue
                # A fenced example is a quotation, so a marker inside one opens
                # no section. `fold_ledger.py#section` already reads the file
                # this way; this is the same rule, and it is the shape round 1
                # found in `folded_items` one function over.
                marker = MARKER_LINE_RE.match(line)
```
```python
def survey(root, ref):
    """What the report is derived from, and where the retirement gets released.

    One walk for the listing, so no work item appears in two of its lists.
    The retirement does NOT take its candidates from here: `retire` reads the
    markers, the directories and the guard from the tree again, because a
    classification made for a printed list is not a guard on a destructive
    act — see its docstring. What it does take from here is `released`, which
    only git can answer and which this has already asked.
    """
```
```python
    candidates = sorted(marked & released_at_base)
```
```python
    home = load(OPTIN, "specseal_optin").home_at(root)
    if not home:
        # `home_at` returns "" for two states: no root at either place, and a
        # repository that opted out with the scratch marker. They used to
        # share one sentence, and a repository holding ninety-eight work items
        # was told it had none.
        common = load(OPTIN, "specseal_optin").git_common_dir(root)
        if common and os.path.isfile(os.path.join(common, "specseal-scratch")):
            sys.stderr.write(
                f"settle: {root} has opted out — the scratch marker is under "
                "its git directory, so every gate in this plugin is off here "
                "and this command will not remove anything. Delete the marker "
                "to turn them back on.\n"
            )
            return 2
        sys.stderr.write(
            f"settle: {root} has no {SPECS}/ at either place — nothing was "
            "read. This command folds work items, and a repository with none "
            "has nothing to settle.\n"
        )
        return 2
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_settle_reads_before_it_removes.py tests/test_unverified_rows_close.py -q` at the target SHA | `145 passed`, exit 0 read directly — the baseline the mutations run against |
| nine revert-mutations, each restored before the next, against the module that should catch it | every one red; the table above names which case each reddened |
| `settle --retire` against a fixture whose top-level `docs/` document carries the marker inside a commented-out draft block | `removed seal/specs/1700000001-alpha/`, exit 0 — finding 1 |
| `folded_items` over a `docs/` holding a commented-out marker, a genuine marker and a fenced marker | `{'1780000000-work'}` from the comment as well as the genuine one — finding 1 |
| `readable()` and `blank_fences` over a genuine marker line | `readable()` → `['', 'A standing statement.']`; `blank_fences` → the marker intact — the rejection is correct |
| `settle --retire` against a fixture with a marked work item present on disk and absent at the release ref | `The fold is complete.`, exit 0, directory still present — finding 2 |
| `settle` against a fixture with `seal/specs/` in the tree and `specseal-scratch` under the git common directory | exit 2, *has no seal/specs/ at either place* — finding 7 |
| both proposed fixes applied together, then the two modules re-run | the two shapes close, exit 1 in each, and `145 passed` holds — the patches below are what was run |
| `unverified-check seal/specs/1790027178-…` | exit 0, `1 overviews · 3 open · 1 closed · 0 unreadable` |
| `survivor-check --range origin/release/v0.13.0...HEAD` | exit 0, *no removed wording is still standing* |
| `survivor-check --range 73ca11d1..f27f7e86` | exit 1, eleven places; each opened and judged — the orchestrator's reading upheld |
| `git log -L` over `test_retire_refuses_an_item_the_guard_is_holding` | two commits, neither changing the case — the prompt's claim that it was corrected does not hold |
| the four modules the fixes touched plus `test_chain_hooks_hardening.py` | not run in this round — the orchestrator executed them at this SHA, `216 passed`, and handed the result over |
| the broad gate — full suite, repository-wide lint and typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/unverified_check.py:85` · `:636` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py:604` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py:497` · `:508` | round 1's 3 — fixed |
| round-1 | `skills/settle/scripts/settle.py:377` · `:426` | round 1's 4 — fixed |
| round-1 | `skills/settle/scripts/settle.py:450` | round 1's 5 — fixed |
| round-1 | `skills/settle/scripts/settle.py:218` · `.github/scripts/fold_ledger.py:210` | round 1's 6 — deferred |
| round-1 | `skills/verify/scripts/unverified_check.py:862` | round 1's 7 — fixed |
| round-1 | `overview.md:81` | round 1's 8 — fixed |
| round-1 | `CLAUDE.md` §*a change writes fragments, never the shared file* | round 1's 9 — deferred |
| round-1 | `spec.md` §*The ticket's headline claim is false* | round 1's 🟢 confirmation — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 confirmation — confirmed |
| round-1 | `overview.md` §*The dry run over this repository's own 97* | round 1's 🟢 confirmation — confirmed |
| round-1 | `overview.md` §*Where spec and implementation diverged* | round 1's 🟢 confirmation — confirmed |
| round-1 | `README*.md` · `docs/one-root-by-lifetime*.md` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py:95` | round 1's 🟢 confirmation — confirmed |
| round-1 | whole tree | round 1's ❓ scope — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `open_rows` duplicated with nothing holding the two copies in step | already deferred in round 1 to #487 | the work item #487 opens |
| `CLAUDE.md`'s ledger exception naming removal only | already deferred in round 1 to #488 | the repository owner |
| `settle` against a second real repository | already deferred in `overview.md` §*Not verified* | the repository owner, the next time the plugin is used elsewhere |
| whether the six population floors are still six after a fold | already deferred in `overview.md` §*Not verified* | the work item that folds this repository's own 97 |
