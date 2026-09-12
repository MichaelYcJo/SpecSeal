# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — review round 1

| Field | Value |
|---|---|
| Target SHA | 5ce162e |
| Ran by | specseal:warden on Opus 5 |
| PR | #364 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | hits (depth 1) |
| Needs a fix | yes — findings 1, 2 and 3. Finding 1 is a document contradicting itself about when one of its own labels comes off; findings 2 and 3 are the sweep that carries S3 and S7 missing shapes measured escaping it. |
| Loses a record or crashes | no. |

- [x] Pass

## What this round was asked

# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `5ce162e` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `7e17f5e` |
| Draft pull request | #364, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope

Issue #361 — a release's size stops being a count and becomes a criterion, and
a label records the answer so the next release is cut without re-reading every
open issue body. Six commits, `6de3f54` through `5ce162e`, on the frame commit
`3b9651b` and the routing commit `bbb6727`.

One document edited (`docs/issues-and-milestones.md`, +62 lines), one new test
module, three ledger files touched, and this work item's records.

## Facts, with labels

**Executed by the orchestrating session** at `5ce162e`, exit codes read
directly with no pipe:

- Nine modules, one per call — `test_a_release_is_sized_by_a_criterion` 7,
  `test_docs_line_wrap` 23, `test_release_hygiene` 32,
  `test_one_word_one_meaning` 13, `test_no_real_identifiers` 2,
  `test_a_row_points_by_content` 102, `test_the_set_a_work_item_always_has` 16,
  `test_a_record_states_what_the_tree_has` 58,
  `test_a_question_says_who_can_answer_it` 6 → **exit 0 each**.
- **The new module seen red, by reverting the document rather than by
  reasoning.** `docs/issues-and-milestones.md` restored to `7e17f5e` → **5
  failed, 2 passed, exit 1**; the five are `test_the_rule_states_the_criterion_and_not_the_count`,
  `test_the_count_survives_as_a_ceiling_in_the_wording_the_cap_already_uses`,
  `test_the_two_releases_are_cited_without_a_version_number`,
  `test_the_rule_says_what_it_does_not_change`,
  `test_the_label_is_two_states_and_nothing_reads_it`. Restored → 7 passed,
  exit 0, `git status --porcelain` empty. **The two that stayed green measure
  the tree rather than the sentence** — the sweep and its can-fail control —
  and the builder reports mutating each of those separately. Re-derive that.
- `uvx ruff check` and `uvx ruff format --check` on the new module → exit 0 each.
- `timers_in` re-run over the whole `LOADED` set at the running version →
  **no offenders**.
- `bin/evidence-check .` → **exit 1 on the records arm only**; the ledger arm
  reads 1144 ok · 0 drifted · 0 broken.

**Executed by the builder**, its own numbers, in `overview.md` and the phase
records: the full narrow set above plus `survivor-check` over
`7e17f5e..HEAD` with `survivors.md` (exit 0, every survivor excused),
`unverified-check` on the memo (exit 0, 4 open), and one deleted `test_tmp_*`
probe. Re-derive rather than inherit — in particular the survivor exemptions
and the claim that each of the sweep's two units was mutated.

**Read, and it is why the evidence carries no version numbers** —
`tests/test_release_hygiene.py`'s `timers_in` refuses every version-shaped
token at or above the running version in the `LOADED` set, `LOADED` includes
`docs`, and the running version is read from `.claude-plugin/plugin.json`.
Both releases the rule cites sit at or above it.

**Read, and it is the defect that was filed rather than fixed** — `v0.11.0` is
tagged, `origin/main` is its release merge, and `CHANGELOG.md` carries its
heading, while `plugin.json` still names it as running. So the refused number
is one the repository has shipped. **#363** holds it.

**Read** — the document's two internal references resolve. The bolded lead-in
it cites for keeping a version illustrative exists and says exactly that, and
names the same check.

**Unverified** — the broad gate. It is the `sealer`'s, after this chain settles.

## Four answers a person gave, which are not yours to reopen

**Q1 — (c).** The two releases are cited as prose with no numbers, and the
checker's off-by-one is #363. Judge whether the prose does that, not whether
numbering would have been better. **A finding that proposes editing
`tests/test_release_hygiene.py` is out of scope by the owner's answer.**

**Q2 — (b), the prefix form.** The owner chose the shape, not the string. The
builder chose `size: now` and took `chain: capped` as the precedent rather than
`merged: X.Y.Z`. Judge the reasoning; the spelling is finally settled when the
owner creates the label, so a better spelling is a note and not a defect.

**Q3 — (a).** The label is created and applied by the owner after this merges.
**This work item writes nothing to the tracker**, and a finding that it should
have is out of scope.

**Q4 — (a).** Release milestone descriptions are out of scope.

## Three divergences the builder declared — judge each, do not inherit

- **The paragraph does not say *nothing automated reads either*.** It says
  nothing *schedules* from either, because §*One thing reads a milestone, and it
  can stop a release* has said the opposite since #359. The narrower clause is
  the true one. `spec.md` expected the wider wording.
- **No exception is written for the label**, against `spec.md`'s expectation.
  The argument: the prefix makes `size:` a topic — sizing, which every release
  has — so §*A label answers what it is about* is not broken and only the value
  is spent. `flow-measurement` stays the one label that is not a topic at all.
- **Two ledger rows drifted where the frame found one.** `seal/ledger.md`'s G5
  and S4 both cite the label section; both were re-read, dated and re-anchored.

## Two things the builder flagged for a second reading

- **`#351`'s `changelog.md:22` quotes the sentence this branch replaces**, and
  both fragments gather into the same released section. Excused in
  `survivors.md` on the ground that its own claim is still true. The builder
  names the alternative reading itself — that a released section should not
  quote a sentence the same section replaces — and it is also a
  `## Not verified` row. This is the judgment most worth a reviewer.
- **The records arm's drift**: this work item's `spec.md:159` quotes the section
  the branch then edits. Inherent to a spec that grounds itself in the code it
  changes, a warning rather than a failure — the ledger job exits only at 2 or
  above. Whether the quote should be re-stamped was left to this round on
  purpose.

## Where a claim flips on how it is measured

**The sweep's absence check cannot be a plain `git grep`.**
`git grep -n "three or four is the size"` exits 1 against the *unedited*
document, because the line wrapped between `three` and `or four` — so the
obvious spelling of that check passes for the wrong reason. The case reads
through a whitespace-flattening reader instead. Check that the reader is
actually flattening, and that the sweep would catch the sentence reappearing
with a different wrap.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `ruff` is not installed here — `uvx
ruff check` / `uvx ruff format --check`. Read exit codes directly, never
through a pipe (`cmd > /tmp/x 2>&1; echo $?`); this shell is `zsh`.
`evidence_check.py .` **unscoped for reading** — the `--ledger` narrowing is
for a `--reverify` write and blinds a read.
`bin/survivor-check --range 7e17f5e..HEAD --exempt <this item>/survivors.md`.

**Do not run the broad gate.** No `bin/broad-gate`, no full suite, no
repository-wide `ruff`.

## The two lines the run ends on

Answer each in a line of its own — `Needs a fix: no`, or `yes` and what does;
and `Loses a record or crashes: no`, or `yes` and what does. A 🟡 answered with
grounds is `no`, and a finding located under `seal/specs/` is a correction that
does not count.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `size: now`'s removal is pinned to the release shipping *and* to the moment `merged: X.Y.Z` goes on; the same document puts the second at the push to `release/*`, one release earlier | `docs/issues-and-milestones.md:147-148`, against `:201` and `:209-210` and `docs/branch-and-release.md:257-258` | **fixed** `ea4fc64` | fixed at ea4fc64 — ``, `docs/issues-and-milestones.md:148-155`. Verified by the orchestrating session at all three coordinates before the round recorded it, and re-read after: the sentence said the label comes off *at the same moment* `merged: X.Y.Z` goes on, while `:209-210` puts that label at a push to `release/*` under a heading that says **before the release ships**, and `docs/branch-and-release.md:251-258` says the two moments are deliberately different. It now anchors on the later one the document already owns — *when the release that carried the ticket has gone out — the moment `main` moves and the issue closes* — followed by **Not when `merged: X.Y.Z` goes on**, which names the section that puts that a release earlier and the reason: that label answers *is this in yet*, where this one is spent only once the work is out. The fix is a sentence about two moments rather than a corrected moment, which is what stops the same conflation returning; read, in the clone at `b46ff77`. Two sections of one document and a third document state the two moments are deliberately different |
| 2 | 🟡 the sweep matches line by line, so a second statement whose wrap falls inside the phrase answers *no offender*; the docstring claims every assertion flattens | `tests/test_a_release_is_sized_by_a_criterion.py:184-193`, docstring at `:13` | **fixed** `ea4fc64` | fixed at ea4fc64 — ``. The sweep and its control read through a new `hits()` that searches each line, and each line joined to the next with the wrap collapsed — skipping the joined check where the next line matches alone, so a wrapped sentence is reported once at the line it starts on. **Re-derived by the orchestrating session rather than inherited**, and my first attempt was wrong: `hits()` takes a list of lines, and passing a string iterates characters and answers `[]`. Called correctly — a sentence wrapped across two lines is `[]` to a plain line scan and `[1]` to `hits()`; a whole-line statement reports once; two adjacent matching lines produce no double report. The module docstring no longer claims `flat()` for everything and says which reader each half uses, which is the half of finding 2 that was a false statement rather than a gap; **executed** — one wrapped shape escapes the committed pattern's line scan and is caught by the same pattern flattened |
| 3 | 🟡 `STATES_A_SIZE` requires the verb *sized* or the literal old sentence, so three one-line noun-form restatements escape | `tests/test_a_release_is_sized_by_a_criterion.py:63-67` | **fixed** `ea4fc64` | fixed at ea4fc64 — ``. `STATES_A_SIZE` gained `release(?:'s)?\s+size`, `size\s+of\s+a\s+release` and `is\s+the\s+size` — the tokens Q6's wider recipe already carried and the planted pattern had dropped. **Measured by the orchestrating session, the same three shapes that escaped before:** `A release's size is three or four work items.`, `Three or four work items is the size of a release.` and `The size of a release is three work items.` are now all **caught**, and so is the sentence this branch replaced. The constant records that `\bis\s+the\s+size\b` can misfire on a sentence about the size of anything, and that nothing in the scanned set matches it today outside the two excluded files — a disclosure at the coordinate rather than a silent widening; **executed** — three shapes measured escaping; the widened pattern catches all three and the module stays green |
| 4 | ⬜ the *value is spent, not the subject* argument rests on an axis with one value, and the label is removed whole | `docs/issues-and-milestones.md:135-139`, against `:77` and `:129-131` | **fixed** `ea4fc64` | fixed at ea4fc64 — ``. The label paragraph now says what two states mean for the argument it makes: the subject never carries a second value, so a spent label is removed whole rather than re-valued. This is the clause `spec.md` expected as an exception and the build had argued was unnecessary; it lands as an argument rather than a carve-out; read. Answerable with grounds; does not move `Needs a fix` |
| 5 | ⬜ R1 records `git grep -n "is the size"` as exiting 1 after the edit; it exits 0, three hits in the module the same phase planted | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | **fixed** `941dab5` | fixed at 941dab5 — ``. The false execution claim, and the one that mattered most because the row folds into `seal/ledger.md` at the release. R1 said `git grep -n "is the size"` exits 1 after the edit; it exits **0**. Confirmed by the orchestrating session both unscoped and scoped to exactly the set the row names, and again after the fix: `git grep -c` reports four hits, all inside `tests/test_a_release_is_sized_by_a_criterion.py`, the module the same phase planted. The row now records what the command answers and which reading was recorded as permanent. `phases/phase-2.md` keeps its `1` — true when taken — and gains the clause naming the commit from which it stops being true, which is the right treatment for a phase record rather than a rewrite; **executed**, exit code read directly |
| 6 | ⬜ two records say the edited fragment now carries three rows; it carries two | `seal/specs/.../phases/phase-4.md`, `seal/specs/.../questions.md` Q8 | **fixed** `941dab5` | fixed at 941dab5 — ``. `phases/phase-4.md` and `questions.md` Q8 said the `1789100139` fragment is now three rows; it is two — S1 and S5b. The third was the table header, counted by `grep -c "^\| "`; **executed** — rows counted at `7e17f5e` and at `b46ff77` |
| 7 | ⬜ the survivor exemption's second ground does not apply, because the fragment is unreleased; the fold puts the superseded wording above the correction in one released section | `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md:22` | **fixed** `941dab5` | fixed at 941dab5 — ``. #351's `changelog.md:22` is **marked rather than excused**, which is what the round decided after measuring half the original exemption away: `CHANGELOG.md`'s top section is still the previous release, the `1789100139` fragment is ungathered, and `gather_changelog.py` concatenates in work-item id order, so that fragment lands above this one and the released section would state the replaced sentence in the present tense before correcting it far below. The bullet now says that wording is what this work moved and not what the document says today, pointing at the entry that replaces it. `survivors.md`'s row quotes the marking clause, so the exemption dies the moment the marking changes, and it records that the original second ground was withdrawn on the reviewer's measurement. The memo's matching `## Not verified` row is closed rather than deleted; read `gather_changelog.py`'s `fragments` (id order) and `CHANGELOG.md`'s top section; **executed** `bin/survivor-check`, exit 0 |
| 8 | ⬜ the records-arm drift at `spec.md:159` should be left as written — S3 was removed, so a current stamp would be false | `seal/specs/.../spec.md:159` | answered | **executed** `bin/evidence-check .`; read `.github/workflows/test.yml:84-92`. My own grounds, not phase 4's |
| 9 | ⬜ `SCANNED` omits `CLAUDE.md`, which the module this sweep is modelled on reads | `tests/test_a_release_is_sized_by_a_criterion.py:47-56` | **fixed** `941dab5` | fixed at 941dab5 — ``. `CLAUDE.md` added to `SCANNED`, with the reason — `tests/test_one_word_one_meaning.py:39`, the module this sweep was modelled on, reads it. 170 files scanned, no offender. Reach rather than a live defect, and closed because the gap was in the model it copied; **executed** — `CLAUDE.md` absent from `tracked()`, and grepped: no live second answer there |

## Paste-ready fixes

```markdown
**Nothing reads this label** — no workflow, no check, no script — so a stale
one costs a reader a wrong answer about what has to go next and costs no
automation anything. It comes off when the release that carried the ticket
ships, and nothing enforces that. That is a later moment than the one
`merged: X.Y.Z` goes on, which §*A label says a ticket is already in, before
the release ships* puts at the push to `release/*`. A label is the right home
for the judgment for exactly that reason: it makes the answer durable without
making it a gate anybody has to satisfy.
```
```python
STATES_A_SIZE = re.compile(
    r"(?i)\brelease(?:'s)?\s+(?:is\s+|was\s+)?sized\b"
    r"|\bsized\s+in\s+work\s+items\b"
    r"|\bthree\s+or\s+four\s+is\s+the\s+size\b"
    r"|\brelease(?:'s)?\s+size\b"
    r"|\bsize\s+of\s+a\s+release\b"
)
```
```python
def wrapped_hits(lines):
    """Line numbers where the pattern matches a line, or a line joined to the
    next one with its wrap collapsed.

    A hand-wrapped phrase is split across exactly one line boundary at 88
    columns, so a scan of single lines answers *no offender* for a sentence a
    reader sees whole. That is the failure phase 1 of this work item measured
    one level up: `git grep -n "three or four is the size"` exits 1 against
    the document that carried it, because the line wrapped between `three`
    and `or four`.
    """
    hits = set()
    for number, line in enumerate(lines, 1):
        if STATES_A_SIZE.search(line):
            hits.add(number)
        elif number < len(lines):
            joined = " ".join((line + " " + lines[number]).split())
            if STATES_A_SIZE.search(joined):
                hits.add(number)
    return hits
```
```python
    offenders = []
    for rel in tracked():
        if rel == OWNER:
            continue
        lines = read(rel).splitlines()
        for number in sorted(wrapped_hits(lines)):
            offenders.append(f"{rel}:{number}: {lines[number - 1].strip()}")
```
```python
    hits = wrapped_hits(read(OWNER).splitlines())
```
```markdown
**Every assertion reads the file with its wraps collapsed** — the presence and
absence cases through `flat()`, the sweep through `wrapped_hits()`. The
sentences here are hand-wrapped at 88 columns (`test_docs_line_wrap.py`), so a
phrase pinned as written on one line breaks the moment a word is added earlier
in the paragraph, and a phrase SEARCHED for on one line is missed the moment
its wrap falls inside it. Phase 1 of this work item found the same thing from
the other side: `spec.md` proposed `git grep -n "three or four is the size"`
as the absence check, and that command exits 1 against the UNEDITED document,
because the line wrapped between `three` and `or four`. A check that passes
before the change is no check.

The sweep scans `.md` and `.py` alike and excludes only this module, by
basename. Scanning one suffix would have been the cheaper way past the
self-match, and it would have left a comment in any other test module free to
state a second answer.
```
```markdown
Two states means the subject never appears on the tracker with a second value,
so the label is removed whole rather than re-valued; what outlives the schedule
is the question the prefix names, not a label anybody is carrying.
```
```markdown
and `git grep -n "is the size"` over the same set exits 0 after it, with every
hit inside `tests/test_a_release_is_sized_by_a_criterion.py` — the module that
names the replaced wording in its own docstring and constants, which is why the
sweep excludes itself
```
```markdown
  - **The sizing rule is now `docs/issues-and-milestones.md`** — *a release
    is sized in work items rather than in ticket numbers, and three or four
    is the size*, in the paragraph that already says what a `release:`
    milestone holds, with the measurement behind it. That wording is what
    #351 moved and not what the document says now: the entry below replaces
    it in this same release. It is the only standing rule the file carried,
    and exactly one document states it now.
```
```python
SCANNED = (
    "docs",
    "skills",
    "agents",
    "templates",
    "tests",
    "CLAUDE.md",
    "README.md",
    "README.ko.md",
    "CONTRIBUTING.md",
)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_release_is_sized_by_a_criterion.py -q` | exit 0 · 7 passed |
| `bin/test` on `test_docs_line_wrap.py`, `test_release_hygiene.py`, `test_one_word_one_meaning.py`, `test_no_real_identifiers.py`, `test_a_row_points_by_content.py`, `test_the_set_a_work_item_always_has.py`, `test_a_record_states_what_the_tree_has.py`, `test_a_question_says_who_can_answer_it.py`, one command | exit 0 · 252 passed |
| `bin/evidence-check .` | exit 1 · ledger arm 1144 ok · 0 drifted · 0 broken; records arm 1 DRIFTED at `spec.md:159` |
| `bin/survivor-check --range 7e17f5e..HEAD --exempt <this item>/survivors.md` | exit 0 · 16 removed sentences, 1 survivor, excused by a row |
| `bin/unverified-check <this item>/overview.md` | exit 0 · 4 open · 0 closed |
| `uvx ruff check` and `uvx ruff format --check` on the new module | exit 0 each |
| probe · document reverted to `6de3f54`, module re-run | exit 1 · 5 failed, 2 passed — the same five units the account names; restore left `git status --porcelain` empty |
| probe · a second size statement appended to `docs/release-checklist.md` | exit 1 · `test_one_document_states_a_releases_size` named the file and line; restored clean |
| probe · `STATES_A_SIZE` replaced by a pattern nothing carries | exit 1 · `test_the_sweep_can_fail` failed; restored clean |
| probe · `flat` applied to the owner | no newline survives — the reader does flatten |
| probe · eight candidate re-appearances through `STATES_A_SIZE`, line scan against flattened | 4 caught · 1 escapes the line scan and is caught flattened · 3 escape the pattern on one line |
| probe · the patch below applied, module re-run and the five shapes re-measured | exit 0 · 7 passed · all five caught · ruff check and format clean; module restored, tree clean |
| `git grep -n "is the size"` over the sweep's own file set | exit 0 · three hits, all in the new module — R1 records exit 1 |
| `git grep -niE "release('?s)? size\|size of a release"` over the same set | exit 0 · hits only in the owner and in the module, both already excluded |
| `gh label list` | `chain: capped` and `merged: 0.11.1` exist; no `size:` label |
| Broad gate — the full suite, the repository-wide lint, the typecheck | not yet, and not run here. It is the sealer's, and it has come due once findings 1 to 3 are answered |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one — a shipped version is refused in a loaded file for one release's length | **#363**, by Q1, with `CONTRIBUTING.md`'s four gate items owed there | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description, stale past its `Size.` line and through its `Order, and why` paragraph | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. No check can see a label that does not exist |
