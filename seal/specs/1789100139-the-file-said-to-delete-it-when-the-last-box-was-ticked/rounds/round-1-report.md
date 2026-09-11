# round 1 — review report

| | |
|---|---|
| Target SHA | `ae2d0ac842ed774df02b6526d2c375c16f0b8413` |
| Review at | `d8c1ad519abfad22f37fbefe12ad68ce9cea4011` — adds only `round-1-asked.md` on top of the target |
| Base | `origin/release/v0.11.1` = `5646717` |
| Ran by | `specseal:warden on Opus 5` |
| Worked in | a `git clone --no-local` at the target, removed after this report |

## What this round found, in the order one thing caused the next

The branch's **first** commit turned a committed case red, and it is still red
at the target. Every later commit was measured against a module set that was
never written down, and that set did not include the red module — so the
defect was invisible from inside the work while being plainly visible to
`pytest tests/`. The same habit of recording a count without recording what
was counted put a second number in the closing memo that was never true at
any commit of this branch.

Everything else is smaller: one loaded instruction file makes a claim about a
section it no longer holds, and six record corrections.

```
① routing.md answers the fourth axis      ← the branch's first commit
       ↓ turns red
② test_every_declaration_in_this_repository_still_parses
       ↓ nobody saw it, because
③ the "nine modules" the handoff calls green are named nowhere
       ↓ same habit
④ "33 survivors" was 32 at every commit of this branch
```

---

### 🔴 1. The branch's first commit left a committed case red, and it still is

`tests/test_routing_is_recorded.py:487`

This work item's `routing.md` answers the fourth axis (`| Planning | the
session |`). `test_every_declaration_in_this_repository_still_parses` asserts
that **no** committed declaration answers it, and names the file that does:

```
AssertionError: seal/specs/1789100139-…/routing.md answers the fourth axis;
this case's premise is that none of the committed declarations does, so it no
longer measures the population the optional row exists for
```

**Executed**, exit codes read directly:

| Commit | `bin/test -q tests/test_routing_is_recorded.py` |
|---|---|
| `5646717` — the base | 31 passed, exit 0 |
| `3439319` — the routing commit, first on the branch | 1 failed, 30 passed, exit 1 |
| `ae2d0ac` — the target | 1 failed, 30 passed, exit 1 |

Why it matters rather than being a stale assertion somebody trips over:
`.github/workflows/test.yml:68` runs `pytest tests/ -q -n auto` on every
push, so the draft pull request's CI is red now, and the sealer's broad gate
would return a failing suite for a branch handed over as green. The commit
message for `3439319` says in so many words that *the fourth axis gets its
first real answer*, so the condition the case asserts was known to be broken
by the same act that broke it.

The declaration is right and the case is what has to move. `the session` is a
legal `Planning` answer (`hooks/routing.py:65`, `PLANNING_ANSWERS`), and
`templates/sdd-routing.md:19` ships the row. What the case was protecting —
that an absent optional row reads as unanswered rather than taking the whole
declaration down — is a claim about the *declarations that omit the row*, and
asserting it as *nobody answers* makes it a tripwire that fires on the first
correct answer instead of on a defect.

**One measurement changes the shape of the fix.** All 73 committed
declarations now carry an `| Implementation |` row, so the third axis has no
absent population in the tree either. A vacuity guard written per axis goes
red immediately; it has to be over the two axes together. The case's own
docstring says the fourth axis *has the same population the third had*, which
is no longer true of the third.

The class was enumerated rather than assumed: `git grep -n "this case's
premise\|premise is that none\|not one has a" -- tests` returns two lines, both
inside this one case. No other case asserts a tree-wide absence.

### 🟡 2. The file the section moved into says nothing changed when it moved

`skills/implement/orchestration.md:23`

Lines 10–13 are new and correct: they say the sequence arrived from the
deleted checklist and sits first. Ten lines later the file says this, which
predates that arrival:

> Nothing here changed when it moved, except one sentence a `# RIDER:` had
> asked to name its arm. The headings keep the `Orchestrator:` prefix they
> were marked with, so a reference to one of these sections names the section
> it always named and only the file it names changed (#292 …)

Both halves are false of the fourth section. Its heading was `## Order inside
a ticket` and is now `## Orchestrator: the order inside a ticket`, so it did
not keep a prefix it was marked with, and a citation of the old name does not
resolve. The `(#292 …)` at the end scopes the paragraph for a careful reader;
a reader who arrives after lines 10–13 reads it as covering all four.

Nothing is broken in the tree today — `git grep -in "order inside a ticket"`
over `docs`, `skills`, `agents`, `templates` and `tests` returns one line, the
heading itself. What is wrong is that a loaded instruction file answers *does
this citation still resolve* with a yes it cannot support, which is the class
the paragraph exists to close.

### ❓ 3. The ticket sent two standing rules to one document; the spec sent one

`seal/specs/…/spec.md:56` · issue #351 · **the repository owner answers**

Issue #351's table row reads:

| In `flow.md` | Where it already is, or should be |
|---|---|
| the standing rules — *a release is sized in work items, and three or four is the size*; *a branch writes its own rows* | `docs/issues-and-milestones.md`, which owns tracker conventions |

and its `Done when` says *the standing rules it carried are in
`docs/issues-and-milestones.md` … and nothing else restates them*. The spec
puts the second rule in **Out** — *both are rules about maintaining
`docs/flow.md`. They do not move; they end* — and the work followed the spec.

The narrowing looks right to me: with the file gone the rule has no subject,
and the general form is already stated in `CLAUDE.md` §*a change writes
fragments, never the shared file*, with `docs/release-checklist.md:38` now
naming this file as *the third file cured of being written by every branch*.
What is missing is anybody saying the ticket was overridden. `overview.md`'s
divergence table records spec against implementation and this is ticket
against spec, so it has no row there, and a `Done when` bullet is left
unsatisfied with no record of the decision.

It is not counted in `Needs a fix`: the answer may be that the narrowing
stands, and if it does the whole fix is one sentence in a record.

---

## The record corrections

`docs/review-chain-spec.md` §*The last round verifies, and what it verifies is
a diff* puts a finding located under `seal/specs/`, `seal/ledger/` or
`seal/ledger.md` outside `Needs a fix` — it is corrected in the closing commit
and owes no fix pass. Findings 4 to 9 are all there. Two of them are false
executed claims rather than typos, so they are listed first.

### ⬜ 4. The executed count names no module set, and three numbers disagree

`seal/specs/…/overview.md:22` and `:54`

The memo records *264 passed across the nine doc-scanning and rule-owner
modules, exit 0* and, in `## Not verified`, *Nine modules and a
repository-wide `ruff check` / `ruff format --check` were run and are green*.
The nine are named nowhere in the work item, so the number cannot be
reproduced or re-run. Three figures now exist for one act:

| Source | Claim |
|---|---|
| the builder's hand-back | 351 passed across 11 modules |
| `overview.md:22` | 264 passed across nine modules |
| this round, the 8 the orchestrating session ran | 234 passed, exit 0 |
| this round, the 26 modules that read a file this branch changed | 1274 collected · 1 failed · exit 1 |

This is finding 1's cause rather than a separate defect. A module set written
down as a list is a set the next reader can re-run; a set described as *nine
doc-scanning and rule-owner modules* is one nobody can check, and the module
that was red is not in any of the three.

### ⬜ 5. "33 survivors" was 32 at every commit of this branch

`seal/specs/…/overview.md:26` · `survivors.md:16`, `:17`, `:38`

**Executed** at two commits, exit codes read directly:

| Commit | `bin/survivor-check --range … --exempt …/survivors.md` |
|---|---|
| `90f2f9d` — the phase-6 commit, where the builder ran it | 32 exempt, exit 0 |
| `ae2d0ac` — the target | `every survivor is excused by a row above (32)`, exit 0 |

So *33 survivors then all 33 excused* was never true on this branch. The
arithmetic in `survivors.md` — *29 of the 33 sit in `CHANGELOG.md`,
`seal/ledger.md` or `seal/specs/`* and four loaded files — is 29 + 4; the
check reports 29 records and **three** loaded files.

The fourth, `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602`,
is not among the 32. Nothing was missed by leaving it unopened, because it was
never reported — but the sentence at that line is about pytest-xdist not being
installed in the virtualenv, where `survivors.md:26` describes it as *#337's
row described the deadlock; the case is about it*. The entry describes a
sentence the file does not carry.

The three that are real — `CLAUDE.md:81`,
`tests/test_a_record_states_what_the_tree_has.py:1013` and
`skills/evidence-check/scripts/evidence_check.py:2189` — I opened, and the
memo's verdict holds: each states, about the code it is written in, the fact
the deleted row pointed at. The one range row rather than 32 rows is the right
call, and `skills/code-review/scripts/survivor_check.py` §*A deletion is one
row, because otherwise it is 153* is the escape it is written for.

### ⬜ 6. A ledger row carries another row's grounds, pasted verbatim

`seal/ledger.md:1367`

R1 (line 1366) and R3 (line 1367) each gained an appended note, and the two
are **byte-identical at 490 characters**. R1's note is correct where it sits.
On R3 it argues *the exemption count is three MECHANISMS, not four entries* —
a claim R1 makes and R3 does not. R3's clause is that the refusal names a
route for every kind of token the check reads as a version.

R3's actual reason for being touched is narrower and is not written down: its
fourth coordinate re-anchored from `@08730484` to `@98c5bec1`, because the
docstring of
`test_no_loaded_file_names_a_version_at_or_above_the_running_one` lost the
clause about the deleted file.

### ⬜ 7. A live ledger row lost half its grounds to this branch

`seal/ledger.md:1646`

The row's Notes says:

> One exists now: `docs/flow.md` writes `an uppercase V0.9.0 is invisible` in
> the row describing this very work item. It is still not an offender, for two
> independent reasons rather than the ticket's one — that file is in
> `RECORDS_OF_A_MOMENT`, and the version is below the running one.

This branch made both halves of the first reason untrue: it deleted the file
and it removed that entry from `RECORDS_OF_A_MOMENT`. The row was left
standing under the memo's blanket verdict that all four surviving ledger
mentions are *dated observations about a past state*.

The memo's own discriminator points the other way here. It corrected a fifth
mention *because it quoted a sentence this branch repaired* — and this one
names a constant this branch edited, inside the row's own grounds rather than
inside an observation of a commit. Two of the four (`:343`, `:1524`) are
plainly dated observations; `:1649` still holds, because the two documents it
counts both still exist.

### ⬜ 8. Two counts in the records are off by one, and one table breaks

- `overview.md:87` — *The five divergences above* where the table above it has
  six rows.
- `plan.md:81` — phase 6's row sits below two prose paragraphs, so the phase
  table ends at phase 5 and the row renders as literal pipe text rather than
  as the sixth row.

### ⬜ 9. Three ledger cells are formatted unlike the other 468

`seal/ledger.md:1366`, `:1367`, `:1953`

- The `Checked` cells read `|  2026-09-11  |` with doubled padding, where the
  other 468 date cells in the file read `| 2026-09-08 |`. Markdown trims it
  and `evidence-check` exits 0, so this is appearance only.
- Each Notes cell runs straight into the appended note with no sentence break
  — `… reports no offender **Re-read 2026-09-11 (#351).**`. Three instances.
- `docs/issues-and-milestones.md:35` and `:39` end at 56 and 48 columns inside
  a paragraph otherwise wrapped near 75, which is what an edit that did not
  re-wrap leaves behind. `test_docs_line_wrap.py` bounds the maximum only, so
  it passes.

---

## The leads that came back empty, and what settled each

| Lead | What I found |
|---|---|
| Does `orchestration.md` read correctly with the new section first, and do citations of the older three resolve? | Yes on both, apart from finding 2. All four headings keep the `Orchestrator:` prefix, and every citation in `CLAUDE.md`, `templates/claude-md-block.md`, `skills/implement/SKILL.md`, `docs/issues-and-milestones.md` and the four test modules names a heading that is unchanged |
| Was the claim that no other file has the constant-spelled `FLOW` shape measured or asserted? | Measured, and it holds. `git grep -nw "FLOW"` returns no live usage — only records. No other test module binds a name to a path this branch removed |
| Is `survivor_check.py`'s written-in list the same list the deleted sentence named? | Yes. The deleted sentence named *the CHANGELOG, the design records under `seal/specs/` and the tickets themselves*; `survivor_check.py:109` and `test_a_corrected_sentence_survives_elsewhere.py:611` both state those three |
| Were the three ledger re-reads real, and do the claims hold at the new anchors? | The anchors verify: `bin/evidence-check --strict` returns 1121 ok · 0 drifted · 0 broken, exit 0, so the two re-anchored hashes match the tree. R1's *three exemptions* is still three mechanisms, R3's refusal claim is untouched, and S15's `quote` argument is unchanged. What is wrong is the prose, findings 6 and 7 |
| Was step 0's first bullet safe to delete rather than replace (divergence 6)? | Yes. The bullet above it checks that *every work item of the release is squash-merged … and its pull request's CI was green at the commit that merged*, which is what the deleted bullet checked through the ticks. The replacement would have stated one check twice |
| Does the changelog name all four parts of the deleted file and where each went? | Yes, and the two rules that end with it as well. The one loose phrase is *its 120 lines went four ways* over a list whose fourth item is the clause removed from another file, which is not one of those 120 lines — the owner's Q3 call asked for that clause, so the content requirement is met |
| Is the spec's S6 claim about what survives the grep right? | It was widened correctly. `seal/ledger.md` survives with four mentions, and the divergence row records it |

## Labels

- **Executed** — everything in `## Executed probes` below, exit codes read
  directly with `; echo $?` and no pipe, in a `--no-local` clone at
  `ae2d0ac`.
- **Read** — findings 2, 3, 6, 7, 8, 9 and every row of the table above
  except the four that name a command.
- **Unverified** — the broad gate. Contract §2 and §3 forbid it to this
  round; `agents/sealer.md` is the agent it is assigned to, and it is now due
  only after findings 1 and 2 are closed. Also unverified, and carried from
  `overview.md` rather than re-opened: whether the four milestone descriptions
  and two ticket comments phase 5 wrote read back as stated, which the
  orchestrating session answers.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The branch's first commit turned `test_every_declaration_in_this_repository_still_parses` red by writing the first `Planning` answer, and it is red at the target | `tests/test_routing_is_recorded.py:487` | open | Executed at three commits: 31 passed exit 0 at `5646717`, 1 failed exit 1 at `3439319` and at `ae2d0ac`. CI runs `pytest tests/ -q -n auto` on every push |
| 2 | 🟡 `orchestration.md` says nothing changed when the sections moved and that every heading kept the prefix it was marked with; the section #351 moved gained the prefix and changed name | `skills/implement/orchestration.md:23` | open | Read. The heading was `## Order inside a ticket`; it is now `## Orchestrator: the order inside a ticket`. No live citation of the old name, so nothing is broken today |
| 3 | ❓ Issue #351 sends two standing rules to `docs/issues-and-milestones.md`; the spec ends one of them and no record says the ticket was overridden | `seal/specs/…/spec.md:56` | open | Read, against #351's table and `Done when`. The narrowing reads right to me; only the owner can settle whether it stands. Not counted in `Needs a fix` |
| 4 | ⬜ The executed count names no module set, and the hand-back, the memo and this round give three different figures | `seal/specs/…/overview.md:22`, `:54` | open | Executed: 234 across the 8 modules the session ran; 1274 collected and 1 failed across the 26 that read a changed file. Neither is 264/9 or 351/11 |
| 5 | ⬜ *33 survivors then all 33 excused* was 32 at both commits where it could have been run, and one of the four named loaded-file survivors is not among them | `seal/specs/…/overview.md:26`, `survivors.md:16`, `:17`, `:38` | open | Executed: 32 exempt and exit 0 at `90f2f9d` and at `ae2d0ac`. `test_the_suite_has_a_command_that_is_cheap_twice.py:602` is not reported, and the sentence there is about pytest-xdist rather than a deadlock |
| 6 | ⬜ R3's appended ledger note is byte-identical to R1's and argues an exemption count R3 does not claim | `seal/ledger.md:1367` | open | Read, and measured: both notes are the same 490 characters. R3's real reason, a coordinate re-anchoring from `@08730484` to `@98c5bec1`, is unrecorded |
| 7 | ⬜ A live ledger row's first of *two independent reasons* names a file this branch deleted and an entry this branch removed, and was left standing as an observation | `seal/ledger.md:1646` | open | Read. The memo corrected a fifth mention for quoting a sentence this branch repaired; this one names a constant this branch edited, inside the row's grounds |
| 8 | ⬜ *The five divergences above* over a six-row table, and phase 6's row falls outside the phase table | `seal/specs/…/overview.md:87`, `plan.md:81` | open | Read. Six divergence rows. Two prose paragraphs sit between phase 5's row and phase 6's, so the table ends at 5 |
| 9 | ⬜ Three `Checked` cells carry doubled padding, three Notes cells run on into the appended note, and two lines of the new milestones paragraph are left short | `seal/ledger.md:1366`, `:1367`, `:1953`; `docs/issues-and-milestones.md:35`, `:39` | open | Read, and counted: 3 cells as `\|  2026-09-11  \|` against 468 written with single spaces. `evidence-check --strict` exits 0 either way |

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

## Paste-ready fixes

Finding 1 — replace the whole case at `tests/test_routing_is_recorded.py:468`.
Measured: 31 passed exit 0 unmutated, and red with the offending declaration
named when `hooks/routing.py` is mutated so an absent `Planning` row reads as
answered.

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

Finding 2 — `skills/implement/orchestration.md:23`, replace the paragraph's
first two sentences.

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

Finding 4 — `seal/specs/…/overview.md:22`, name the modules instead of
counting them.

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

Finding 5 — `seal/specs/…/overview.md:26` and the three counts in
`survivors.md`.

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

Delete the `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602`
bullet from `survivors.md`; the check does not report that line, and the
sentence there is about pytest-xdist not being installed rather than about a
deadlock. Then the range row's closing clause becomes:

```markdown
All 32 reported places were opened; the three outside the records are listed
above and each states the fact where it belongs
```

Finding 6 — `seal/ledger.md:1367`, replace R3's appended note with the one
that fits R3.

```markdown
**Re-read 2026-09-11 (#351).** This row's fourth coordinate re-anchored:
`test_no_loaded_file_names_a_version_at_or_above_the_running_one`'s docstring
lost the clause arguing the exemption for the deleted shared checklist.
Nothing this row claims moved — the refusal's routes and the message that
prints them are untouched by that branch
```

Finding 7 — `seal/ledger.md:1646`, correct the first of the two reasons rather
than leaving it standing.

```markdown
It was still not an offender, for two independent reasons rather than the
ticket's one — that file was in `RECORDS_OF_A_MOMENT`, and the version is
below the running one and so is history either way. **#351 deleted that file
and removed its `RECORDS_OF_A_MOMENT` entry**, so the first reason is gone
with its subject and the second is the one that stands; no instance of the
invisible shape is in the loaded set again.
```

Finding 8 — `seal/specs/…/overview.md:87`.

```markdown
Nothing was added to `spec.md`. The six divergences above are recorded here
```

and in `plan.md`, move phase 6's row up so it sits directly under phase 5's,
with the two `Phase 5, as executed` and `The file was already stale`
paragraphs following the completed table.

Needs a fix: yes — finding 1, the committed case this branch's first commit
turned red, and finding 2, the paragraph in `skills/implement/orchestration.md`
that claims a property the moved section does not have.

Loses a record or crashes: no

## Proof

Opened and read: `seal/specs/1789100139-…/` (`spec.md`, `plan.md`,
`questions.md`, `overview.md`, `changelog.md`, `routing.md`, `survivors.md`,
`rounds/round-1-asked.md`), `seal/ledger/1789100139-…md`; the full diff
`5646717...ae2d0ac`; `docs/flow.md` as deleted; `docs/issues-and-milestones.md`,
`docs/release-checklist.md`, `docs/one-root-by-lifetime.md` and its Korean
edition, `docs/review-chain-spec.md`; `skills/implement/orchestration.md`,
`skills/code-review/scripts/survivor_check.py`,
`skills/verify/scripts/broad_gate.py`; `tests/test_the_rules_have_one_owner.py`,
`tests/test_release_hygiene.py`,
`tests/test_a_corrected_sentence_survives_elsewhere.py`,
`tests/test_routing_is_recorded.py`,
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:598-608`;
`hooks/routing.py`, `templates/sdd-routing.md`, `seal/config.md`, `bin/test`,
`CONTRIBUTING.md`, `CLAUDE.md`, `.github/workflows/test.yml`;
`seal/ledger.md` at lines 343, 1363-1367, 1524, 1646, 1649, 1953; and
`gh issue view 351`.
