# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — review round 1

| Field | Value |
|---|---|
| Target SHA | ae2d0ac842ed774df02b6526d2c375c16f0b8413 |
| Ran by | specseal:warden on Opus 5 |
| PR | #358 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1, the committed case this branch's first commit turned red, and finding 2, the paragraph in `skills/implement/orchestration.md` that claims a property the moved section does not have. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `ae2d0ac842ed774df02b6526d2c375c16f0b8413` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `5646717` |
| Draft pull request | #358, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope handed to the round

Issue #351 — `docs/flow.md` is deleted, and its four parts are placed where
they are read. Six commits, `7ed455b` through `ae2d0ac`, on top of the frame
commit `6035bee`.

## Facts, with labels

**Executed by the orchestrating session** at `ae2d0ac`, exit codes read
directly with no pipe:

- `bin/test -q tests/test_the_rules_have_one_owner.py
  tests/test_release_hygiene.py
  tests/test_a_corrected_sentence_survives_elsewhere.py
  tests/test_one_word_one_meaning.py tests/test_docs_line_wrap.py
  tests/test_no_real_identifiers.py
  tests/test_no_document_names_the_old_roots.py
  tests/test_the_seal_is_taken_once_by_the_sealer.py` → **234 passed, exit 0**.
- `uvx ruff check` and `uvx ruff format --check` over the five changed Python
  files → **exit 0** each.
- `git grep -ln "flow\.md" -- '*.md' '*.py' '*.yml'`, less `CHANGELOG.md` and
  `seal/specs/`, returns **`seal/ledger.md` alone**, four Notes mentions.

**Executed by the builder**, recorded in `overview.md`'s `· verified` line
with its own numbers: the two moved cases seen red (3 failed, exit 1) then
green (45 passed, exit 0); `evidence-check --strict` 1121 ok · 0 drifted · 0
broken; `survivor-check` over this range, 33 survivors then all 33 excused;
`unverified-check`; repository-wide `ruff check` and `ruff format --check`.
Re-derive rather than inherit.

**Read, not executed** — `docs/flow.md`'s `## 0.11.1` section was already
stale against the milestones when it was deleted: it listed #331, #335, #339
and #149 as this release's, and the tracker puts #331 and #335 in 0.11.3,
#339 and #149 in 0.11.2.

**Unverified** — the broad gate. It is the sealer's, after this chain settles.

## Where a claim flips on measurement point

The `RECORDS_OF_A_MOMENT` entry's removal was measured **with the file still
tracked**: seven offending lines, all seven inside `docs/flow.md`. Measured
after the deletion the same check has nothing to report. That is why the
entry comes out in phase 4's commit rather than phase 3's, and it is
divergence 3 in `overview.md`.

## The command with two forms

`bin/evidence-check` unscoped reads the whole ledger; `--strict` is the form
this branch was checked with. Do not narrow it to this work item's fragment:
that narrowing is what once let fifteen drifted rows reach a pull request.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The branch's first commit turned `test_every_declaration_in_this_repository_still_parses` red by writing the first `Planning` answer, and it is red at the target | `tests/test_routing_is_recorded.py:487` | **fixed** `62c22ca` | fixed at 62c22ca — ``. The case's premise moved from *no committed declaration answers the fourth axis* to *every declaration that OMITS an optional row reads as unanswered on that axis*, which is the claim the row exists for. Seen red first at HEAD (1 failed, 30 passed, exit 1, naming this work item's `routing.md`), green after (31 passed, exit 0). §15 on the new assertion: with `hooks/routing.py` mutated so an absent `Planning` row reads as `framer`, the new assertion is red naming `1788177600-the-tree-that-arrives-without-its-history/routing.md`, exit 1; the parser was restored from bytes kept before the mutation, not from HEAD. **Measured, and it decided the guard's shape**: 0 of 73 declarations omit `Implementation` and 72 omit `Planning`, so the vacuity guard covers the two axes together — per axis it would be red the day it was written. **One limit, stated rather than left to be found**: because nothing omits `Implementation`, this case's `Implementation` arm is unexercised by the tree — mutating that default to `smith` leaves this case green (exit 0) and is caught by three fixture-based cases in the same module (exit 1). The guard is what will notice if `Planning` ever reaches the same state; Executed at three commits: 31 passed exit 0 at `5646717`, 1 failed exit 1 at `3439319` and at `ae2d0ac`. CI runs `pytest tests/ -q -n auto` on every push |
| 2 | 🟡 `orchestration.md` says nothing changed when the sections moved and that every heading kept the prefix it was marked with; the section #351 moved gained the prefix and changed name | `skills/implement/orchestration.md:23` | **fixed** `62c22ca` | fixed at 62c22ca — ``. The paragraph now scopes itself to the three sections #292 moved and names the order as the exception that gained the prefix. **The paste-ready text was not pasted on trust and one word of it was wrong**: it read *The order above is the exception*, and the order section is at line 31, below the paragraph at line 23. It reads *The order below*; Read. The heading was `## Order inside a ticket`; it is now `## Orchestrator: the order inside a ticket`. No live citation of the old name, so nothing is broken today |
| 3 | ❓ Issue #351 sends two standing rules to `docs/issues-and-milestones.md`; the spec ends one of them and no record says the ticket was overridden | `seal/specs/…/spec.md:56` | deferred the repository owner | the repository owner |
| 4 | ⬜ The executed count names no module set, and the hand-back, the memo and this round give three different figures | `seal/specs/…/overview.md:22`, `:54` | answered | Corrected at `62c22ca`. `overview.md`'s `· verified` line names thirteen modules with a count each — 45 · 32 · 23 · 43 · 13 · 11 · 2 · 86 · 9 · 58 · 29 · 31 · 65 — and 447 passed over the thirteen together, exit 0, each also run on its own. The `## Not verified` row stops saying *nine modules* and points at that list. **Both earlier figures were real runs of unnamed sets**: the first nine of that list sum to 264 and the first eleven to 351, which is why neither could be reproduced. The replacement docstring in finding 1's case carries no count either, for the same reason — the one it replaced said *the twelve committed here* and *Seventy-two declarations* about a tree holding 73 |
| 5 | ⬜ *33 survivors then all 33 excused* was 32 at both commits where it could have been run, and one of the four named loaded-file survivors is not among them | `seal/specs/…/overview.md:26`, `survivors.md:16`, `:17`, `:38` | answered | Corrected at `62c22ca`. 33 becomes 32 in `overview.md` and in all three places in `survivors.md`. Measured at `62c22ca`: `every survivor is excused by a row above (32)`, exit 0, and the reported places split 29 records to 3 loaded files, so the arithmetic is 29 + 3. The `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` bullet is withdrawn and replaced by a paragraph saying what it got wrong — the place is not among the 32 (`grep -c` returns 0) and the docstring there is about pytest-xdist being installed by the workflow rather than by the virtualenv, not the deadlock the bullet described |
| 6 | ⬜ R3's appended ledger note is byte-identical to R1's and argues an exemption count R3 does not claim | `seal/ledger.md:1367` | answered | Corrected at `62c22ca`. R3's appended note was R1's, byte-identical, arguing an exemption count R3 does not claim. R3 now records its actual reason — its fourth coordinate re-anchored from `@08730484` to `@98c5bec1` because that test function's docstring lost the clause about the deleted checklist — and says the refusal's routes and message are untouched. Verified not identical afterwards |
| 7 | ⬜ A live ledger row's first of *two independent reasons* names a file this branch deleted and an entry this branch removed, and was left standing as an observation | `seal/ledger.md:1646` | answered | Corrected at `62c22ca`. `seal/ledger.md:1646`'s first of two independent reasons named a file this branch deleted and an entry it removed. The sentence goes to the past tense and gains what #351 did to it, so the second reason is named as the one that stands. The reviewer's discriminator is the right one: this was inside the row's grounds, not an observation of a commit, which is why it differs from `:343` and `:1524` |
| 8 | ⬜ *The five divergences above* over a six-row table, and phase 6's row falls outside the phase table | `seal/specs/…/overview.md:87`, `plan.md:81` | answered | Corrected at `62c22ca`. *The five divergences above* becomes *six*. Phase 6's row moved up under phase 5's and the two prose paragraphs follow the completed table — the prose was moved rather than the row deleted, as directed. **The first move left a blank line between rows 5 and 6, which breaks the table exactly as the prose did**; it was caught by parsing the table back and asserting the contiguous data rows are `1 2 3 4 5 6`, which they now are |
| 9 | ⬜ Three `Checked` cells carry doubled padding, three Notes cells run on into the appended note, and two lines of the new milestones paragraph are left short | `seal/ledger.md:1366`, `:1367`, `:1953`; `docs/issues-and-milestones.md:35`, `:39` | **fixed** `62c22ca` | fixed at 62c22ca — ``. Three doubled `Checked` cells re-padded — measured at 3 doubled against 467 single, and 0 doubled afterwards. Three Notes cells gained a sentence break before the appended note. `docs/issues-and-milestones.md:35` and `:39`, at 56 and 48 columns inside a paragraph wrapped near 75, re-wrapped. **The class had two more instances the round did not report, both mine**: `plan.md`'s phase 1 and 2 Status cells were written `\|` + backtick with no space, by the same script that doubled the date cells. Both re-padded. The verdict is `fixed` rather than `answered` because one half of this finding is in a loaded document rather than in a record; Read, and counted: 3 cells as `\|  2026-09-11  \|` against 468 written with single spaces. `evidence-check --strict` exits 0 either way |

## Paste-ready fixes

```python
def test_every_declaration_in_this_repository_still_parses():
    """Executed against the real files, not a fixture: the declarations
    committed here are the population the optional rows exist for.

    S8 of #84 extends it rather than opening a second case beside it. What an
    optional row has to survive is a declaration that does not carry it -- a
    required row, or a row whose absence took the declaration down, would
    un-silence the commit gate on every one of those. So the assertion is over
    the declarations that OMIT each row, and never over how many answer it:
    #351 wrote the first `Planning` answer, and a case premised on nobody
    answering goes red on the commit that writes one rather than on a defect.

    The vacuity guard is over the two axes together, not per axis. Every
    committed declaration answers `Implementation`, so a per-axis guard would
    be red the day it was written.
    """
    import glob

    root = os.path.join(os.path.dirname(__file__), "..")
    found = sorted(glob.glob(os.path.join(root, "seal", "specs", "*", "routing.md")))
    assert found, "no declarations found -- the check would pass vacuously"
    omitted = {routing.PLANNING: 0, routing.IMPLEMENTATION: 0}
    for path in found:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        parsed = routing.parse(text)
        assert parsed is not None, path
        for row, key in (
            (routing.PLANNING, "planning"),
            (routing.IMPLEMENTATION, "implementation"),
        ):
            if f"| {row} |" in text:
                continue
            omitted[row] += 1
            assert parsed[key] is None, (
                f"{path} has no `{row}` row and did not read as unanswered on "
                f"that axis -- an absent optional row has to read as nothing, "
                f"or the commit gate un-silences on every declaration like it"
            )
    assert sum(omitted.values()), (
        "every declaration answers both optional rows -- the case is vacuous"
    )
```
```markdown
Nothing changed in the three sections #292 moved out of
`skills/implement/SKILL.md`, except one sentence a `# RIDER:` had asked to
name its arm; their headings keep the `Orchestrator:` prefix they were marked
with, so a reference to one of those names the section it always named and
only the file it names changed (#292, the shape #265 gave `code-review`). The
order above is the exception: it gained the prefix when it moved, so it is
cited by its new name and not by the one the shared checklist gave it. Every
`seal/…` path here means what it means in the other half: `<repo>/seal/` where
that directory exists, and `$(git rev-parse --git-common-dir)/seal/` otherwise
(contract §16).
```
```markdown
· verified: **executed** — the two moved cases seen red (3 failed, exit 1)
            and green (45 passed, exit 0); the nine modules that read a file
            this branch changed, named rather than counted —
            `test_the_rules_have_one_owner` 45, `test_release_hygiene` 32,
            `test_a_corrected_sentence_survives_elsewhere` 43,
            `test_one_word_one_meaning` 13, `test_docs_line_wrap` 23,
            `test_no_real_identifiers` 2, `test_no_document_names_the_old_roots`
            11, `test_the_seal_is_taken_once_by_the_sealer` 65 — 234 passed,
            exit 0
```
```markdown
            `bin/survivor-check --range origin/release/v0.11.1...HEAD`
            32 survivors then all 32 excused, exit 0
```
```markdown
**The 32 were opened rather than waved through, and the three that are not
records are named here.** 29 of the 32 sit in `CHANGELOG.md`, `seal/ledger.md`
or `seal/specs/`. The other three are loaded files, and each one states, about
the code it is written in, the fact the deleted row only pointed at:
```
```markdown
All 32 reported places were opened; the three outside the records are listed
above and each states the fact where it belongs
```
```markdown
**Re-read 2026-09-11 (#351).** This row's fourth coordinate re-anchored:
`test_no_loaded_file_names_a_version_at_or_above_the_running_one`'s docstring
lost the clause arguing the exemption for the deleted shared checklist.
Nothing this row claims moved — the refusal's routes and the message that
prints them are untouched by that branch
```
```markdown
It was still not an offender, for two independent reasons rather than the
ticket's one — that file was in `RECORDS_OF_A_MOMENT`, and the version is
below the running one and so is history either way. **#351 deleted that file
and removed its `RECORDS_OF_A_MOMENT` entry**, so the first reason is gone
with its subject and the second is the one that stands; no instance of the
invisible shape is in the loaded set again.
```
```markdown
Nothing was added to `spec.md`. The six divergences above are recorded here
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q tests/test_routing_is_recorded.py` at `5646717` | 31 passed, exit 0 |
| `bin/test -q tests/test_routing_is_recorded.py` at `3439319` | 1 failed, 30 passed, exit 1 — `test_every_declaration_in_this_repository_still_parses` |
| `bin/test -q tests/test_routing_is_recorded.py` at `ae2d0ac` | 1 failed, 30 passed, exit 1 |
| `bin/test -q` over the 8 modules the orchestrating session named | 234 passed, exit 0 — reproduces the handoff's figure |
| `bin/test -q` over the other 18 modules that read a file this branch changed | 1 failed, 1039 passed, exit 1 |
| `bin/test -q tests/test_the_rules_have_one_owner.py` | 45 passed, exit 0 — the two moved cases green at their new home |
| `bin/evidence-check --strict` | total 1121 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| `bin/survivor-check --range origin/release/v0.11.1...HEAD --exempt seal/specs/1789100139-…/survivors.md` at `ae2d0ac` | 32 exempt, `every survivor is excused by a row above (32)`, exit 0 |
| the same command at `90f2f9d`, the commit the builder ran it at | 32 exempt, exit 0 |
| `bin/unverified-check` | 3 open rows for this work item, each with an answerer, exit 0 |
| `uvx ruff check` and `uvx ruff format --check` over the five changed Python files | exit 0 each |
| `grep -rn "flow\.md" docs/` · `grep -c "flow\.md" docs/release-checklist.md` | no match, exit 1 · `0` — S2 and S4 |
| `git grep -n "flow\.md"` over `*.md *.py *.yml *.yaml *.toml *.json`, less `CHANGELOG.md` and `seal/specs/` | `seal/ledger.md` alone, four mentions — S6 as the divergence row widened it |
| `git grep -n "sized in work items"` and `git grep -in "order inside a ticket"` over `docs skills agents templates tests` | one line each, in `docs/issues-and-milestones.md:24` and `skills/implement/orchestration.md:31` — S3 and S1 |
| `git grep -nw "FLOW"` over the tracked tree | records only, no live usage |
| `git grep -n "premise is that none\|not one has a" -- tests` | two lines, both inside the one failing case — the class has one instance |
| count of `\| Implementation \|` rows across `seal/specs/*/routing.md` | 73 of 73 — the third axis has no absent population left either |
| a `test_tmp_*` probe: the proposed replacement for finding 1, unmutated and against a mutated parser | as reviewed exit 1 · with the fix **31 passed, exit 0** · with the fix and `planning` defaulting to `BY_FRAMER` when the row is absent, exit 1 with the new assertion naming the offender. Deleted; the clone is clean |
| **broad gate** — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 and §3 forbid it to this round. It comes due as the `sealer`'s spawn once findings 1 and 2 are closed, and it is not this session's to assemble |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
