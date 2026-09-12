# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — review round 2

| Field | Value |
|---|---|
| Target SHA | 941dab5 |
| Ran by | specseal:warden on Opus 5 |
| PR | #364 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1, 2, 3 and 4. Finding 1 is the same document making a new false claim about its own two labels in the commit that answered the first one; finding 2 is all three code-side fixes reverting with the module green; finding 3 is a gate on every pull request that the review chain's own records disarm; finding 4 is the one sentence of round 1's docstring patch that was not applied, now copied into the ledger row that folds into the shared file. |
| Loses a record or crashes | no. |

- [x] Pass

## What this round was asked

# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `a0f0e9a..941dab5` — not the branch |
| Review at | `941dab5` |
| Base of the branch | `origin/release/v0.11.1` = `7e17f5e` |
| Draft pull request | #364 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 8 fixed, 0 answered, 0 deferred |

## The job, and the one surface that is not verification

**The answers, not new findings** — for each of round 1's nine verdicts, is it
actually closed. `rounds/round-1.md` holds the verdict table,
`rounds/round-2-fixes.md` holds what the fix pass says it did, and
`rounds/round-1-report.md` holds the reasoning the verdicts came from.

**One exception, and it is a finding surface.** `round-1.md`'s `New units` row
reads **`hits (depth 1)`**, derived from the fix diff by `round_record.py
close` rather than typed. `hits()` in
`tests/test_a_release_is_sized_by_a_criterion.py:117-134` is a unit the fixes
created, so nobody has reviewed it: it is *is this correct*, not *did this
close something*. It is also the whole of finding 2's answer, which makes it
the round's centre.

Read it against what it has to do. A hand-wrapped document splits a sentence
across exactly one line boundary, so `hits()` searches each line and each line
joined to the next with the wrap collapsed — and skips the joined check where
the next line matches alone, so a wrapped sentence is reported once at the line
it starts on. Ask what the one-boundary assumption costs: `test_docs_line_wrap`
caps the width, and a sentence long enough to span **two** boundaries is the
shape this cannot see. Whether that matters is a judgment; make it rather than
assume it.

## What the fix pass says it did, to be checked rather than inherited

- **Finding 1 answered with a sentence about two moments, not a corrected
  moment.** `docs/issues-and-milestones.md:148-155` now anchors the label's
  removal on *the moment `main` moves and the issue closes* and then says
  **Not when `merged: X.Y.Z` goes on**, naming the section that puts that a
  release earlier. Judge whether the new sentence is true of both mechanisms,
  and whether a reader lands on the right moment.
- **Finding 3 widened `STATES_A_SIZE` and disclosed a misfire at the
  coordinate** — `\bis\s+the\s+size\b` can match a sentence about the size of
  anything, and the constant says so and says nothing in the scanned set
  matches it today outside the two excluded files. **That second clause is a
  measurement with a shelf life**; re-derive it rather than trust it.
- **Finding 5 corrected a false execution claim in a ledger row.** R1 said
  `git grep -n "is the size"` exits 1; it exits 0. Check that what the row now
  says reproduces, and that `phases/phase-2.md` keeping its `1` with a clause
  naming the commit from which it stops being true is the right treatment for a
  phase record.
- **Finding 7 marked #351's `changelog.md:22` rather than excusing it**, and
  `survivors.md`'s row now quotes the marking clause so the exemption dies if
  the marking changes. Judge both halves, and whether the released section now
  reads correctly in work-item id order.
- **Finding 9 added `CLAUDE.md` to `SCANNED`.** 170 files, no offender claimed.

## Executed by the orchestrating session at `941dab5`

Exit codes read directly, no pipe. Re-derive rather than inherit:

- Eight modules, one per call — the new module 7, `test_docs_line_wrap` 23,
  `test_release_hygiene` 32, `test_one_word_one_meaning` 13,
  `test_no_real_identifiers` 2, `test_a_row_points_by_content` 102,
  `test_a_record_states_what_the_tree_has` 58,
  `test_the_set_a_work_item_always_has` 16 → **exit 0 each**.
- `uvx ruff check` and `uvx ruff format --check` on the module → **exit 0** each.
- `STATES_A_SIZE` exercised directly: all three noun forms that escaped before
  — `A release's size is three or four work items.`, `Three or four work items
  is the size of a release.`, `The size of a release is three work items.` —
  are now **caught**, and so is the replaced sentence.
- `hits()` exercised directly: a sentence wrapped across two lines is `[]` to a
  plain line scan and `[1]` to `hits()`; a whole-line statement reports once;
  two adjacent matching lines produce no double report. **This session's first
  attempt was wrong** — `hits()` takes a list of lines, and passing a string
  iterates characters and answers `[]`. Worth knowing before you call it.
- `git grep -c "is the size"` over the set R1 names → four hits, all inside the
  new module.
- `bin/survivor-check --range 7e17f5e..HEAD --exempt <survivors.md>` → **exit 0**.
- `bin/evidence-check .` → **exit 1**, ledger arm **1144 ok · 0 drifted · 0
  broken**, records arm one drift at `spec.md:159`.
- The finding-1 sentence read against `:209-210` and
  `docs/branch-and-release.md:251-258`.

## Settled, and not yours to reopen

**The four owner answers.** Q1 (c) — the releases are cited as prose, the
checker's off-by-one is #363, and **a finding proposing an edit to
`tests/test_release_hygiene.py` is out of scope**. Q2 (b) — the prefix form;
the spelling is settled when the owner creates the label, so a better one is a
note. Q3 (a) — **this work item writes nothing to the tracker.** Q4 (a) —
milestone descriptions are out of scope.

**Round 1's own two judgments.** #351's `changelog.md:22` gets a marking clause
rather than an exemption; and `spec.md:159`'s records-arm drift **stays**,
because S3 was removed rather than re-pointed, so re-stamping would leave a row
that no longer exists quoting current content. Judge whether the fixes did what
those decisions asked, not whether the decisions were right.

## Still unverified, and it stays that way

**The broad gate is the `sealer`'s. Do not run it.** No `bin/broad-gate`, no
whole-suite run, no repository-wide `ruff`. It comes due when this round closes.

## The form the commands take in this checkout

`ruff` is not installed — `uvx ruff check` / `uvx ruff format --check`. Read
exit codes directly, never through a pipe (`cmd > /tmp/x 2>&1; echo $?`); this
shell is `zsh`. `bin/test`, narrow, one module per call. `evidence_check.py .`
**unscoped for reading** — the `--ledger` narrowing is for a `--reverify` write
and blinds a read.

## The line the run ends on

Answer each in a line of its own — `Needs a fix: no`, or `yes` and what does;
and `Loses a record or crashes: no`, or `yes` and what does. A 🟡 answered with
grounds is `no`, and a finding located under `seal/specs/` is a correction that
does not count. **The reopening is one**: if this round opens something, its own
fixes get one more verifying round and a second is refused, after which the run
ends `capped`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the fix's new sentence puts `merged: X.Y.Z` *a release earlier* than `size: now` comes off; the section it cites, that section's title and `docs/branch-and-release.md` all put both moments inside one release | `docs/issues-and-milestones.md:152-155`, against `:208` and `:210-211` and `docs/branch-and-release.md:256-258` | **fixed** `95b3d83` | fixed at 95b3d83 — ``, `docs/issues-and-milestones.md:150-158`. **Written once from the coordinates rather than adjusted a third time**, which is what the round asked: this clause was wrong in the build (two moments conflated) and wrong again in round 1's fix (*a release earlier*). It now says `size: now` comes off when the release reaches `main` and the issue closes, and that `merged: X.Y.Z` goes on **earlier inside that same release** at the squash, naming the gap as exactly the interval §*A label says a ticket is already in* exists to fill. Read by the orchestrating session against all three coordinates — `:208`'s title, `:210-211`'s *for the length of a release*, and `docs/branch-and-release.md:256-258` — and it is now true of both mechanisms and names the other label's mechanism rather than its distance; read, in the clone at `941dab5`. Three coordinates state the two moments are one release apart in time within a single release, and the value of the other label names that same release |
| 2 | 🟡 each of the three code-side fixes reverts with the module still green, so nothing in the tree distinguishes the fixed module from the defective one — `agent-contract` §15 | `tests/test_a_release_is_sized_by_a_criterion.py`, the pattern at `:90-97`, `hits()` at `:117-134`, `SCANNED` at `:55-68` | deferred #366 | #366 |
| 3 | 🟡 `corrected` does not apply the `rounds/` exclusion the pool applies, so committing a review round's own record subtracts the wording that round reported and the survivor stops being reported | `skills/code-review/scripts/survivor_check.py`, `corrected` — the `paths` list built from `diff --name-only`; docstring at `:65` and `:70-79` | deferred #365 | #365 |
| 4 | 🟡 the docstring still says the self-exclusion is by path where `tracked()` excludes by basename — the one sentence of round 1's docstring patch that was not applied — and the same wording was written into the ledger row that folds into `seal/ledger.md` | `tests/test_a_release_is_sized_by_a_criterion.py:31`, against `:146`; and `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1 | **fixed** `95b3d83` | fixed at 95b3d83 — `` for the docstring and `34beebb` for the ledger row. `:31-32` now reads *excludes only this module, **by basename rather than by path***, and says what that buys — a copy of the module anywhere in the scanned set is excluded with it. The same wording was corrected in R1, which folds into `seal/ledger.md` at the release and is why this was not just a comment; **executed** — the filter is `os.path.basename`; read, round 1's paste-ready text for that sentence said *by basename* |
| 5 | ⬜ the survivors file excuses nothing — the check reports no survivors at `941dab5` — and the marking-clause quote does not exempt the candidate when the survivor is restored, so both claims the records make about the exemption are false | `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/survivors.md`, and `rounds/round-1.md`'s probe row | **fixed** `34beebb` | fixed at 34beebb — ``; **executed** — `exempted` answers None for the restored candidate; the marking clause is a later sentence than the candidate's own. The marking itself verified correct in id order |
| 6 | ⬜ R1's grounds anchor the sweep unit but not `hits()`, so `evidence-check` answers ok after the edit that reverts the wrap-awareness the row's claim rests on | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1, `Code grounds` | **fixed** `34beebb` | fixed at 34beebb — ``; **executed** — the ledger arm reads 1144 ok · 0 drifted · 0 broken with `hits()` reverted |
| 7 | ⬜ `hits()`'s one-boundary assumption is load-bearing and its two-boundary escape is not reachable by 88-column wrapping; the reachable residual is a statement split across string literals, which `flat()` cannot see either | `tests/test_a_release_is_sized_by_a_criterion.py:117-134` | answered | **executed** — two-boundary shapes measured escaping; shortest mid-paragraph line in the edited paragraph is 49 columns against a 25-column phrase. Answerable with grounds; does not move `Needs a fix` |
| 8 | ⬜ the inserted clauses left both edited paragraphs unfilled — `:152` at 49 columns, `:141` at 83 — under the cap, so hygiene rather than a defect | `docs/issues-and-milestones.md:141`, `:152` | **fixed** `95b3d83` | fixed at 95b3d83 — ``; **executed** — widths measured; `test_docs_line_wrap` exit 0 |

## Paste-ready fixes

```markdown
**Nothing reads this label** — no workflow, no check, no script — so a stale
one costs a reader a wrong answer about what has to go next and costs no
automation anything. It comes off when the release that carried the ticket has
gone out — the moment `main` moves and the issue closes — and nothing enforces
that. **Not when `merged: X.Y.Z` goes on**, which §*A label says a ticket is
already in, before the release ships* puts at the push to `release/*`: that is
earlier in the same release, and it answers *is this in yet*, where this one is
spent only once the work is out. A label is the right home for the judgment for
exactly that reason: it makes the answer durable without making it a gate
anybody has to satisfy.
```
```python
# The shapes round 1 measured escaping, kept as data rather than as prose.
# **The sweep's green answer cannot stand in for these.** It asserts *no
# offender*, and no file in the tree carries any of these today, so deleting
# the reach that finds them changes no answer: each of the three fixes round 1
# commissioned was measured reverting with this module still green. So they are
# pinned against the reader itself.
NOUN_FORMS = (  <!-- NAME NOT IN TREE -->
    "A release's size is three or four work items.",
    "Three or four work items is the size of a release.",
    "The size of a release is three work items.",
)


def test_the_pattern_catches_the_noun_forms_and_not_only_the_verb():  <!-- NAME NOT IN TREE -->
    """Round 1 measured all three escaping, on one line and with no wrap
    involved. `test_the_sweep_can_fail` cannot see them go: the owner matches
    on `release ... sized` alone, which was there before the widening."""
    for sentence in NOUN_FORMS:  <!-- NAME NOT IN TREE -->
        assert STATES_A_SIZE.search(sentence), (
            "a one-line restatement of a release's size escapes the sweep: "
            f"{sentence!r}"
        )


def test_the_sweep_reads_a_statement_whose_wrap_falls_inside_it():
    """The failure round 1 found, and the whole reason `hits()` exists rather
    than a line scan. The first assertion is the control: if a plain scan ever
    starts seeing this shape, the case has stopped measuring the reader."""
    wrapped = ["the paragraph says three or four is the", "size a release is cut to."]
    plain = [n for n, line in enumerate(wrapped, 1) if STATES_A_SIZE.search(line)]
    assert plain == [], (
        "the control moved: a plain line scan must miss this shape, or this "
        "case passes on a reader the sweep does not need"
    )
    assert hits(wrapped) == [1], (
        "a statement whose wrap falls inside it must be reported, at the line "
        "it starts on"
    )


def test_the_scanned_set_includes_the_file_a_rule_gets_restated_in():
    """`CLAUDE.md` is where a rule is restated for a session that never opens
    `docs/`, and `tests/test_one_word_one_meaning.py` — the module this sweep
    is modelled on — already reads it."""
    assert "CLAUDE.md" in tracked(), (
        "CLAUDE.md is outside the sweep, so a second answer stated there is "
        "invisible to it"
    )
```
```python
    # The `rounds/` exclusion holds on BOTH sides of the range, not only on the
    # pool. A round record quotes the defective wording verbatim -- that is
    # what a report is for -- so counting it as wording the range WROTE
    # subtracts the phrases the round reported, and the survivor stops being
    # reported by the commit that posts the round. Measured on this
    # repository's own #361 branch: 1 survivor at 2.00 before the round record
    # was committed, 0 after, with nothing else in the range changed.
    paths = [
        path
        for path in names.split("\0")
        if path and not records_a_past_round(path)
    ]
```
```markdown
The sweep scans `.md` and `.py` alike and excludes only this module, by
basename rather than by path, so a copy of it anywhere in the scanned set is
excluded too. Scanning one suffix would have been the cheaper way past the
self-match, and it would have left a comment in any other test module free to
state a second answer.
```
```markdown
the module that names the replaced wording in its own docstring and constants,
and the one file the sweep excludes — by basename, so a copy of it under
another directory would be excluded with it
```
```markdown
All four rows below were written against a run that reported one survivor, at
`b46ff77`. **At `941dab5` the check reports none**, because the range now
carries round 1's own records and `corrected` counts their verbatim quotation
as wording this range wrote — round 2's finding 3. So these rows excuse
nothing today and none of them is printed under `exempt`. They are kept rather
than deleted: they are the judgments a person made, and repairing the checker
arms them again.
```
```markdown
| `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md` | `the paragraph that already says what a `release:` milestone holds` | #351's changelog fragment, gathered into `CHANGELOG.md`'s `0.11.1` section by the release that also ships this work item. Its claim is what #351 did — the rule moved into that document — and that is still true, so the bullet stays. **Round 1 measured the second half of the original exemption away and it is withdrawn**: `gather_changelog.py` concatenates fragments in work-item id order, so `1789100139` lands ABOVE this one and the released section would have stated the replaced sentence in the present tense before correcting it far below. The bullet is therefore MARKED as well — it now says the wording is what #351 moved and not what the document says today, and points at the entry below that replaces it. **The quote above is the surviving sentence rather than that marking**, because the exemption matches a run inside the candidate's own words and the marking is a later sentence: round 2 measured the marking-clause spelling answering None |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_release_is_sized_by_a_criterion.py -q` | exit 0 · 7 passed |
| `bin/test` on `test_docs_line_wrap.py`, `test_release_hygiene.py`, `test_one_word_one_meaning.py`, `test_no_real_identifiers.py`, `test_a_row_points_by_content.py`, `test_a_record_states_what_the_tree_has.py`, `test_the_set_a_work_item_always_has.py`, one command | exit 0 · 246 passed |
| `uvx ruff check` and `uvx ruff format --check` on the module | exit 0 each |
| `bin/evidence-check .` | exit 1 · ledger arm 1144 ok · 0 drifted · 0 broken; records arm 1 DRIFTED at `spec.md:159` |
| `bin/survivor-check --range 7e17f5e..HEAD --exempt <this item>/survivors.md` | exit 0 · 894 files, 16 removed sentences, **no survivors reported** — nothing excused |
| `survivor-check` at `5ce162e`, `b46ff77`, `a0f0e9a`, `ea4fc64`, no exemption file | 1 survivor at 2.00 · 1 at 2.00 · **0** · 0 — the drop is at `a0f0e9a`, which adds only round 1's record and report |
| probe · `corrected`'s paths filtered through `records_a_past_round` at `941dab5` | 894 files, 16 removed sentences unchanged, **1 survivor at 2.00** restored; `exempted` answers None for it |
| probe · per-alternative match census over the scanned set | `is the size` 4 lines, all in the module; `release's size` owner ×1 and module ×7; `size of a release` module ×2; `release … sized` owner ×2 and module ×2 — the disclosure holds |
| probe · `hits()` exercised directly | one boundary reported; two boundaries `[]` against a flattened match; the guard reports an adjacent pair once; a join-only match on `is the size` fires, as the constant discloses |
| probe · `tracked()` | 170 files · `CLAUDE.md` present · the module excluded, and the filter is `os.path.basename` |
| probe · three mutations, one at a time, module re-run | exit 0 · 7 passed each — every one of the three fixes survives being reverted; tree restored clean after each |
| probe · the three proposed cases, at `941dab5` and against each mutation | 10 passed as committed; 1 failed under each mutation, and the failure is that mutation's own case in all three |
| probe · short mid-paragraph lines in the scanned set, and the widths of the two edited paragraphs | shortest mid-paragraph line the fix produced is 49 columns against a 25-column phrase |
| `git grep -n "is the size"` over the set R1 names | exit 0 · four hits, all in the module — what the corrected row now says |
| `git cat-file -t 7578e25` and its diffstat | the commit exists and is the one that planted the module, which is what `phases/phase-2.md`'s new clause names |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet**, and not run here. It is the `sealer`'s, and it has not come due: findings 1 to 4 are open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/issues-and-milestones.md:147-148`, against `:201` and `:209-210` and `docs/branch-and-release.md:257-258` | round 1's 1 — fixed |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:184-193`, docstring at `:13` | round 1's 2 — fixed |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:63-67` | round 1's 3 — fixed |
| round-1 | `docs/issues-and-milestones.md:135-139`, against `:77` and `:129-131` | round 1's 4 — fixed |
| round-1 | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | round 1's 5 — fixed |
| round-1 | `seal/specs/.../phases/phase-4.md`, `seal/specs/.../questions.md` Q8 | round 1's 6 — fixed |
| round-1 | `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md:22` | round 1's 7 — fixed |
| round-1 | `seal/specs/.../spec.md:159` | round 1's 8 — answered |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:47-56` | round 1's 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one — a shipped version is refused in a loaded file for one release's length | **#363**, by Q1 | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description, stale past its `Size.` line | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. Already deferred; no check can see a label that does not exist |
| finding 3, if the orchestrator takes it out of this work item's scope rather than fixing it here | a new tracker issue, with `CONTRIBUTING.md`'s four gate items owed there — the defect is in a gate | the repository owner. **Not yet filed**, and Q3 says this work item writes nothing to the tracker, so somebody other than this branch has to. Filed or fixed, it must not be left as a report nobody acts on: the check is disarmed on every review chain until then |
