# round 1 — review report

| | |
|---|---|
| Work item | `1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency` |
| Target SHA | `5ce162e` |
| Reviewed at | `b46ff77` — the target plus `round-1-asked.md` |
| Base | `origin/release/v0.11.1` = `7e17f5e` |
| Reviewed in | a `git clone --no-local` of the repository, checked out at `b46ff77` |
| Ran by | specseal:warden on Opus 5 |
| Migration config | none — no `seal/parity.md`, so no parity comparison and no parity mark |

Where this report says a check was run, it was run in that clone and the exit
code was read directly. Where it says something was read, it was read.

## What the account claimed, and what the code said

Five claims in `round-1-asked.md` and the builder's records were re-derived
rather than inherited. Four hold. One does not.

- **Claimed** that reverting the document leaves five of the seven units red
  and two green, and that the two green ones were each mutated separately.
  **Re-derived by execution.** The revert to `6de3f54` produced exactly the
  five named failures, and each of the two survivors went red on its own
  mutation. Both restores left the tree clean.
- **Claimed** that the case's reader flattens whitespace, so the absence half
  cannot pass for the wrong reason. **Half true, and the half that is false is
  the sweep.** `flat` does collapse every newline, and the five presence and
  absence units read through it. The two sweep units do not — they read
  `read(rel).splitlines()` — so finding 2 below.
- **Claimed** in the ledger that `git grep -n "is the size"` over the sweep's
  own file set exits 1 after the edit. **It exits 0.** Finding 5.
- **Claimed** that `chain: capped` is the tracker's existing shape for a
  prefixed state. **True** — `gh label list` carries `chain: capped` and
  `merged: 0.11.1`, and no `size:` label exists. The reasoning for taking
  `chain: capped` over `merged: X.Y.Z` as the precedent is sound: its value is
  a verdict where `merged:`'s value is a version.
- **Claimed** that the ledger arm is clean and only the records arm reports
  drift. **True** — 1144 ok · 0 drifted · 0 broken, and one records-arm
  DRIFTED at `spec.md:159`.

## 🟡 1 · `size: now`'s removal is pinned to two moments this document says are different

`docs/issues-and-milestones.md:147-148` reads *It comes off when the release
that carried the ticket ships, at the same moment `merged: X.Y.Z` goes on*.
That apposition asserts the two moments coincide. The same document says they
do not, and it says so twice.

`docs/issues-and-milestones.md:209-210` states that
`.github/scripts/label_merged_on_release_branch.py` runs **on a push to
`release/*`** and puts `merged: X.Y.Z` on the issues the arriving pull
requests claimed. The section holding it is titled *A label says a ticket is
already in, before the release ships* (`:201`), and
`docs/branch-and-release.md:257-258` adds that the answer to *is this in yet*
comes at the squash while the answer to *is this done* comes when `main`
moves — *`docs/issues-and-milestones.md` owns both mechanisms and the reason
the two moments are different*.

So a reader who follows the new sentence removes `size: now` at the squash
into the release branch, one release early, while the ticket is not yet in
effect anywhere. The sizing judgment the label exists to preserve is spent
before the thing it was judging has shipped. This is the document that owns
tracker conventions contradicting itself about one of its own labels, and no
check reads either label, so nothing else will catch it.

## 🟡 2 · the sweep reads line by line, so the hazard phase 1 found applies to the sweep itself

`tests/test_a_release_is_sized_by_a_criterion.py:184-193`. The sweep iterates
`read(rel).splitlines()` and matches each line on its own. Every file it
scans is hand-wrapped at 88 columns, so a phrase whose wrap falls inside it is
invisible to the scan.

Measured against the module as committed:

| Candidate re-appearance in a scanned file | Line scan | Flattened |
|---|---|---|
| `A release is` / `sized by a count, and three or four is it.` | **no offender** | caught |
| `A release is sized by a count.` on one line | caught | caught |

This is the same failure phase 1 measured one level up, and the module's own
docstring records it: `git grep -n "three or four is the size"` exits 1
against the *unedited* document because the line wrapped between `three` and
`or four`. The five presence and absence units were moved to `flat` for
exactly this reason. The sweep was not.

The docstring at `:13` states *Every assertion reads the document through
`flat()`*, which is false for this unit and for `test_the_sweep_can_fail`. The
next person to edit the pattern will trust a wrap-resilience the sweep does
not have.

Two smaller things in the same unit, fixed by the same patch. The owner is
filtered **after** the regex runs (`if rel != OWNER` nested inside the match
block at `:187-188`), so every line of the owner is matched to be discarded.
And the docstring at `:23` says the module *excludes only this module by
path*, while `:96` excludes by `os.path.basename`.

## 🟡 3 · the pattern catches the verb and misses the noun, on one line

`tests/test_a_release_is_sized_by_a_criterion.py:63-67`. `STATES_A_SIZE` has
three alternatives: `release … sized`, `sized in work items`, and the old
sentence literally. All three require the verb *sized* or the exact replaced
string. The noun form escapes with no wrap involved at all:

| Candidate, one line, in a scanned file | Verdict |
|---|---|
| `A release's size is three or four work items.` | **no offender** |
| `Three or four work items is the size of a release.` | **no offender** |
| `The size of a release is three work items.` | **no offender** |

S7 claims *nothing else in the tree states a release's size*, and
`agent-contract` §12 owes the fix to the class rather than to the coordinate.
The class here is *a second statement of what decides a release's size*, and
the pattern covers one conjugation of it. `questions.md` Q6 recorded a wider
recipe — `-niE "is the size|sized (in|by)|release's size"` — and the planted
regex dropped `release's size` and `is the size` as standalone alternatives.

The widening is safe to make: over the sweep's own file set, `release's size`
and `size of a release` appear only in the owner (excluded) and in the module
itself (excluded by `SELF`). Measured, then the widened module run — 7 passed.

## ⬜ 4 · `docs/issues-and-milestones.md:135-139` — the reconciliation rests on a value axis with one value

The section opens at `:77` with *a concern that outlives a schedule needs a
label instead*. The new paragraph answers it by splitting the label: *What the
release spends is the value, `now`, and not the subject.* The subject `size:`
is durable, so the rule is not broken.

The argument holds as written, and I am not calling it a defect. What is worth
one clause is that the design has exactly two states (`:129-131`), so no issue
ever carries `size:` with any other value — when the answer expires the whole
label is removed, prefix included. The durable subject is real as a naming
convention and never appears on the tracker as a durable label. A reader who
takes `:137` literally expects `size:` to persist with a new value.

Answerable with grounds, so it does not move `Needs a fix`.

## ⬜ 5 · R1's recorded measurement does not reproduce

`seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
row **R1**, `Verified behavior`: *and `git grep -n "is the size"` over the same
set exits 1 after it*.

Run at `b46ff77` over `docs skills agents templates tests README.md
README.ko.md CONTRIBUTING.md`, it exits **0**, with three hits — all in
`tests/test_a_release_is_sized_by_a_criterion.py`, at `:5`, `:18` and `:45`,
the module the same phase planted. The honest claim is *exits 1 over that set
with this module excluded*, which is the `SELF` exclusion the sweep already
makes and the reason the module names the phrase at all.

This is a false executed claim rather than a wording slip, and
`fold_ledger.py` moves the fragment into `seal/ledger.md` at the release,
where nobody re-runs it. Reported as a correction because its `Location` is
under `seal/ledger/`, per this agent's own rule; the orchestrator may want to
weigh whether that rule was meant to cover a row that folds into the shared
ledger.

## ⬜ 6 · two records say the edited fragment carries three rows; it carries two

`phases/phase-4.md` — *the row is removed from
`seal/ledger/1789100139-…md`, which now carries three rows* — and
`questions.md` Q8 — *which now carries three*.

Counted at both ends: `7e17f5e` had S1, S3 and S5b, three rows. `b46ff77` has
S1 and S5b, two. Three is the count before the removal. `evidence_check.py`
reports 4 ok anchors for that fragment, which is the two surviving rows'
anchors and not a row count.

## ⬜ 7 · the survivor exemption for #351's changelog fragment — my answer, and it differs

`seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md:22`.
`survivors.md` excuses it because *its own claim is still true* and because
*rewriting a shipped phase record would falsify the account of a build that
happened*.

The first ground holds and the second does not apply. Nothing here is shipped:
`CHANGELOG.md`'s top section is `## 0.11.0 — 2026-09-11`, and #351's fragment
is still ungathered. So the exemption's strongest argument — do not rewrite a
released record — is about a state this fragment is not in.

What the release produces is measurable rather than arguable.
`.github/scripts/gather_changelog.py` concatenates fragments **in work item id
order** (`fragments`, *in id order*), so `1789100139` lands above `1789172128`
in the 0.11.1 section. A reader of that section meets, first, *The sizing rule
is now `docs/issues-and-milestones.md` — a release is sized in work items
rather than in ticket numbers, and three or four is the size* in the present
tense, and only further down the entry that says the wording changed. The
sweep cannot see it: `CHANGELOG.md` is outside `SCANNED`.

My verdict: the quote should be marked as the wording the same release
replaced. Editing another work item's fragment is the act Q8 already settled
as acceptable, on the ground that both fragments sit in `release/v0.11.1`.

Reported as a correction because its `Location` is under `seal/specs/`. It is
the one correction whose content leaves that directory at the release, so it is
the one worth the orchestrator's own reading.

## ⬜ 8 · the records-arm drift at `spec.md:159` — leaving it is right

Phase 4 left the quoted stamp `@95e3a483` as written. I reached the same answer
from the code rather than from the record, and the reason is stronger than the
one phase 4 gives.

S3 was **removed**, not re-anchored. So `spec.md:159` describes a row that no
longer exists anywhere. Re-stamping it to the current hash would produce a
sentence asserting that a nonexistent row cites the current content, which is
false in a way the present warning is not. The sentence is about what the row
said when the frame was drawn, and it says so.

The warning persists until the release folds the fragment, and `test.yml`'s
ledger job turns exit 1 into an annotation and fails only at 2 or above — read
at `:84-92`, and the ledger arm itself is clean.

## ⬜ 9 · `SCANNED` omits `CLAUDE.md`

`tests/test_a_release_is_sized_by_a_criterion.py:47-56` scans `docs`,
`skills`, `agents`, `templates`, `tests` and three root documents.
`tests/test_one_word_one_meaning.py:39` — the module this sweep is modelled on
— reads `CLAUDE.md`, which is the most-read instruction file in the
repository. Grepped: `CLAUDE.md` states no release size today, so this is a
gap in the sweep's reach rather than a live second answer.

## Regression cases to plant

None beyond the patch in finding 2 and finding 3, which is itself the
regression: both escapes are shapes the sweep must catch, and the widened
module was run against all five of them. `agent-contract` §15 is satisfied for
that patch by construction — the five shapes were measured escaping the
committed pattern first, and caught after.

## Facts for the evidence ledger

- R1 must be corrected before the fold, per finding 5. The reproducible form
  of its second claim is *`git grep -n "is the size"` over that set exits 0,
  with every hit in the sweep module the `SELF` exclusion already removes*.
- R2's `Notes` carry the value-and-subject argument that finding 4 qualifies.
  If finding 4's clause lands in the document, R2's note is the row that
  should say so.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `size: now`'s removal is pinned to the release shipping *and* to the moment `merged: X.Y.Z` goes on; the same document puts the second at the push to `release/*`, one release earlier | `docs/issues-and-milestones.md:147-148`, against `:201` and `:209-210` and `docs/branch-and-release.md:257-258` | open | read, in the clone at `b46ff77`. Two sections of one document and a third document state the two moments are deliberately different |
| 2 | 🟡 the sweep matches line by line, so a second statement whose wrap falls inside the phrase answers *no offender*; the docstring claims every assertion flattens | `tests/test_a_release_is_sized_by_a_criterion.py:184-193`, docstring at `:13` | open | **executed** — one wrapped shape escapes the committed pattern's line scan and is caught by the same pattern flattened |
| 3 | 🟡 `STATES_A_SIZE` requires the verb *sized* or the literal old sentence, so three one-line noun-form restatements escape | `tests/test_a_release_is_sized_by_a_criterion.py:63-67` | open | **executed** — three shapes measured escaping; the widened pattern catches all three and the module stays green |
| 4 | ⬜ the *value is spent, not the subject* argument rests on an axis with one value, and the label is removed whole | `docs/issues-and-milestones.md:135-139`, against `:77` and `:129-131` | open | read. Answerable with grounds; does not move `Needs a fix` |
| 5 | ⬜ R1 records `git grep -n "is the size"` as exiting 1 after the edit; it exits 0, three hits in the module the same phase planted | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | open | **executed**, exit code read directly |
| 6 | ⬜ two records say the edited fragment now carries three rows; it carries two | `seal/specs/.../phases/phase-4.md`, `seal/specs/.../questions.md` Q8 | open | **executed** — rows counted at `7e17f5e` and at `b46ff77` |
| 7 | ⬜ the survivor exemption's second ground does not apply, because the fragment is unreleased; the fold puts the superseded wording above the correction in one released section | `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md:22` | open | read `gather_changelog.py`'s `fragments` (id order) and `CHANGELOG.md`'s top section; **executed** `bin/survivor-check`, exit 0 |
| 8 | ⬜ the records-arm drift at `spec.md:159` should be left as written — S3 was removed, so a current stamp would be false | `seal/specs/.../spec.md:159` | answered | **executed** `bin/evidence-check .`; read `.github/workflows/test.yml:84-92`. My own grounds, not phase 4's |
| 9 | ⬜ `SCANNED` omits `CLAUDE.md`, which the module this sweep is modelled on reads | `tests/test_a_release_is_sized_by_a_criterion.py:47-56` | open | **executed** — `CLAUDE.md` absent from `tracked()`, and grepped: no live second answer there |

Stage 1, spec compliance. S1, S2, S4, S5, S6, S8, S9, S10 hold — each read
against the document and, where a case exists, run. S3 and S7 hold **as far as
the sweep reaches**, which is findings 2 and 3. S11 is not applicable: Q1 took
the prose route, no gate changed, and `CONTRIBUTING.md` §*What a change to a
gate must carry* owes nothing here.

The four settled answers were not reopened. Nothing in this report proposes
editing `tests/test_release_hygiene.py`, writing to the tracker, or touching a
milestone description.

The three declared divergences: the narrowed *nothing schedules from either*
clause is the true one — `docs/issues-and-milestones.md:167-186` says a
milestone is read and that the reader refuses a release rather than composing
one, so the wider wording would have been false. The absent label exception is
finding 4. The two drifted ledger rows are correct — G5 and S4 both cite the
edited section, both claims survive the edit, and the ledger arm is clean at
the re-anchored hash.

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

Every probe file was named `test_tmp_*`, run once and deleted; the clone's
tree was `git status --porcelain` empty afterwards. The virtual environment
`bin/test` built is the repository's own reused runner, not a probe's leaving.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one — a shipped version is refused in a loaded file for one release's length | **#363**, by Q1, with `CONTRIBUTING.md`'s four gate items owed there | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description, stale past its `Size.` line and through its `Order, and why` paragraph | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. No check can see a label that does not exist |

## Paste-ready fixes

Finding 1 — `docs/issues-and-milestones.md`, replacing the paragraph at
`:145-150`. The alternative, if the intended moment really is the squash, is to
say *it comes off when the ticket lands in a release branch* and drop *when the
release ships*; the two cannot both stand.

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

Findings 2 and 3 — `tests/test_a_release_is_sized_by_a_criterion.py`. This
patch was applied in the clone and run: 7 passed, all five previously
escaping shapes caught, `uvx ruff check` and `uvx ruff format --check` clean.

Replace `STATES_A_SIZE` at `:63-67`:

```python
STATES_A_SIZE = re.compile(
    r"(?i)\brelease(?:'s)?\s+(?:is\s+|was\s+)?sized\b"
    r"|\bsized\s+in\s+work\s+items\b"
    r"|\bthree\s+or\s+four\s+is\s+the\s+size\b"
    r"|\brelease(?:'s)?\s+size\b"
    r"|\bsize\s+of\s+a\s+release\b"
)
```

Add this helper above `test_one_document_states_a_releases_size`:

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

Replace the sweep's body at `:184-189`. The owner is now skipped before the
regex runs rather than after it:

```python
    offenders = []
    for rel in tracked():
        if rel == OWNER:
            continue
        lines = read(rel).splitlines()
        for number in sorted(wrapped_hits(lines)):
            offenders.append(f"{rel}:{number}: {lines[number - 1].strip()}")
```

Replace the can-fail unit's body at `:201-203`, so the control measures the
same reader the sweep uses:

```python
    hits = wrapped_hits(read(OWNER).splitlines())
```

Then the module docstring: `:13` claims every assertion flattens, and `:23`
says the self-exclusion is by path. Replace both sentences:

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

Finding 4 — `docs/issues-and-milestones.md`, one sentence appended to the
paragraph at `:135-143`:

```markdown
Two states means the subject never appears on the tracker with a second value,
so the label is removed whole rather than re-valued; what outlives the schedule
is the question the prefix names, not a label anybody is carrying.
```

Finding 5 — `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
row R1's `Verified behavior`, replacing the clause after the sweep sentence:

```markdown
and `git grep -n "is the size"` over the same set exits 0 after it, with every
hit inside `tests/test_a_release_is_sized_by_a_criterion.py` — the module that
names the replaced wording in its own docstring and constants, which is why the
sweep excludes itself
```

Finding 6 — `phases/phase-4.md` and `questions.md` Q8: *which now carries
three rows* becomes *which now carries two rows*.

Finding 7 — `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md`,
the bullet at `:22`, adding one clause after the quote:

```markdown
  - **The sizing rule is now `docs/issues-and-milestones.md`** — *a release
    is sized in work items rather than in ticket numbers, and three or four
    is the size*, in the paragraph that already says what a `release:`
    milestone holds, with the measurement behind it. That wording is what
    #351 moved and not what the document says now: the entry below replaces
    it in this same release. It is the only standing rule the file carried,
    and exactly one document states it now.
```

Finding 9 — `tests/test_a_release_is_sized_by_a_criterion.py:47-56`, adding
one entry to `SCANNED`:

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

Needs a fix: yes — findings 1, 2 and 3. Finding 1 is a document contradicting
itself about when one of its own labels comes off; findings 2 and 3 are the
sweep that carries S3 and S7 missing shapes measured escaping it.

Loses a record or crashes: no.

## Proof

Files opened, in a `git clone --no-local` at `b46ff77`:
`docs/issues-and-milestones.md`, `docs/review-chain-spec.md`,
`docs/branch-and-release.md`, `docs/release-checklist.md`,
`tests/test_a_release_is_sized_by_a_criterion.py`,
`tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`,
`.github/workflows/test.yml`, `.github/scripts/gather_changelog.py`,
`agents/smith.md`, `bin/test`, `CHANGELOG.md`, `seal/config.md`,
`seal/ledger.md`, `seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md`,
`seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
and this work item's `spec.md`, `plan.md`, `questions.md`, `routing.md`,
`overview.md`, `changelog.md`, `survivors.md`, `phases/phase-4.md`,
`rounds/round-1-asked.md`, plus
`seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md`.
