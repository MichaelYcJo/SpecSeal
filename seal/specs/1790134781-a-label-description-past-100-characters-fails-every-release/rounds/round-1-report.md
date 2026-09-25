# Review round 1 — `fix/515-a-label-description-past-100-characters-fails-every-release`

Target SHA `a479a38`, base `release/v0.14.0` (`1bafeb7`). Reviewed in a
`git clone --no-local` at the target, since deleted. This is a first round:
the work item has no `round-N.md`, so there are no earlier coordinates to
carry and no earlier verdicts to answer.

How the findings relate:

```
#515's cost was two things: the label never created, and the roll behind it skipped
  ├ the description now fits and a case holds it there            (judgments below: sound)
  └ ① the roll still runs only if the label step succeeds          (🟡, the coupling that turned one bad string into a skipped roll)
② the test module's case index and §15 paragraph miss the new case (⬜)
③ overview.md counts five mutations where C1 lists four            (⬜ correction)
```

## Spec compliance

The spec for this rung is #515's body, `docs/issues-and-milestones.md`
§*A label answers what it is about, and survives the move*, and the module
comments the change edits. #515's *Shape of the repair* asks for two things:
a description of 100 characters or fewer, and a case over every declared
label. Both are present. What #515 names as the cost is also two things: the
label does not exist, and the flow-measurement roll was skipped. The diff
removes the cause of both for this one string, and finding 1 is about the
second half surviving the next cause.

### The judgments the prompt asked me to attack

**The shortened text still says both halves.** I counted it: 95 characters,
against 119 before (executed, `len()` on both strings). The document's
sentence is *"`size: now` says this ticket has to be in effect before the next
work item starts"*, and the description keeps that clause word for word minus
its subject. The removal half reads *"removed when its release closes the
issue"*. The document says the workflow *"removes `size: now` from each issue
it closes when the release reaches `main`"*, and the close happens on that
push (`.github/workflows/close-issues-on-release.yml:17-19`), so the two name
one moment. The old text named the close too. On the tracker's labels page,
where no issue is in view, `its` has no antecedent. I judged that acceptable:
every fitting rewording I tried that restores one runs past 100.

**`LABEL_DESCRIPTION_LIMIT` is in a defensible place.** Two functions call
`gh label create`, and I found no third (read, `git grep` over the tree):
`label_merged_on_release_branch.py#create_label` and
`tracker_labels.py#create`. The constant sits beside the first. The second
reaches it through the `signal` import it already had
(`.github/scripts/tracker_labels.py:76`). `close_issues_on_release.py` is the
module both import, but it creates no label, so moving the constant there
would put it beside no user.

**Editing T2 in the shared `seal/ledger.md` is the permitted act.**
`CONTRIBUTING.md:204-215` says a branch that changes cited code must touch
the row, and gives `evidence-check --reverify` as the arm for *the claim
still holds*. That is this case: the reconcile still makes one
`gh label create` carrying the declared text. The `Re-read <date>` marker is
the form `correction_check.py` reads, and T1 two rows above carries one in
the same shape. `evidence-check --ledger seal/ledger.md . --strict` returned
1468 ok, 0 drifted (executed).

**C1 is a claim this ledger carries.** Rows here routinely cite a case as
their grounds, and T1, T2 and S3 all do. What C1 adds that the case cannot
hold is where the number comes from, and why it is not this repository's to
raise. One fact in it can now move from unverified to read, and it is under
*Facts for the evidence ledger* below.

**Nothing else in the tree states the old description or the 119-character
state as current** (read, `git grep` for `release carrying it` and a bare
`119`). The old text survives only as a quotation in this work item's
`overview.md`. Every `119` outside `CHANGELOG.md` issue numbers is a sentence
telling the history. `docs/issues-and-milestones.md` never quoted the
description.

## Quality

### 1. 🟡 The roll still runs only if the label step succeeds

`.github/workflows/close-issues-on-release.yml:56-61`.

**What is wrong.** The three steps run in order and none carries an `if:`.
So the roll inherits GitHub's default of `success()`, and any non-zero exit
from `tracker_labels.py --apply` skips it. The diff removes one such exit,
the over-long description, and leaves every other one in place.

**Why it matters.** The skipped roll is half of what #515 is about, and its
title says so: *the measurement log never rolls*. Other refusals lead to the
same place:

- a transient API error on `gh label create`;
- a second declared label that is wrong in a way the new case does not
  check, such as a colour the tracker rejects;
- a hand-made label whose name differs from the declared one only in case.
  `missing` compares case-sensitively, and I have not checked what GitHub
  does with that create (unverified).

Each one skips the roll again, and it happens after the merge, where nobody
is looking. It is also against the module's own design.
`tracker_labels.py`'s docstring says *"It is not a gate and must not become
one"*, and in this workflow it gates the step after it.

**The fix** is one line on the roll step, plus a case that pins it. The job
still goes red when the label step fails, so nothing is hidden, and the roll
reads nothing the steps before it write.

**Executed.** In the clone I ran the case below against the current
workflow, and it failed. I added the `if:` line and ran it again beside
`tests/test_a_declared_label_reaches_the_tracker.py` and
`tests/test_a_release_rolls_the_flow_measurement_issue.py`: 52 passed.
`tests/test_release_hygiene.py -k "close or workflow or token"`, which covers
this workflow's permissions and trigger, gave 8 passed. Both edits were then
reverted and the probe file deleted.

### 2. ⬜ The test module's index and its §15 paragraph miss the new case

`tests/test_a_declared_label_reaches_the_tracker.py:10-34`.

The docstring lists A9 to A12 as the module's cases, and the new cap case is
not among them. The §15 paragraph says each case's red run is recorded in
phase 4 of work item `1790076050`. For the new case the red run is recorded
in this work item's C1, and `1790076050` is no longer under `seal/specs/`,
which predates this branch. Nothing behaves differently. A reader looking for
how the new case was shown red is sent to the wrong place.

### 3. ⬜ correction — `overview.md` counts five mutations, and C1 lists four

`seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6`.

The `verified` line says *"five single-unit mutations"*. C1 lists four: the
119-character value restored, the limit tightened to 50, the merged template
grown, and the removal half dropped. The hand-back also says four. This is
the run's own record, so it is a correction and not a fix.

## Executed and read, kept apart

- **Executed**:
  - both changed case files, 44 passed;
  - the cap case against the 119-character text: red on `[('size: now', 119)]`, and A9 red beside it;
  - `evidence-check --strict` on this work item's fragment (5 ok) and on `seal/ledger.md` (1468 ok);
  - the finding 1 probe, red before the fix and green after.
- **Read**:
  - the diff and both scripts in full;
  - the specifying section and #515's body;
  - `CONTRIBUTING.md` §*Changing cited code is the case the rule has to answer*;
  - GitHub's REST reference for *Create a label*, fetched 2026-09-23 at `docs.github.com/en/rest/issues/labels`. It says of `description`: *"Must be 100 characters or fewer."* It states no maximum for `name`.
- **Unverified**:
  - whether GitHub counts that 100 in characters or bytes. It matters only once a description carries a non-ASCII character. The case counts code points. Answerer: whoever next declares a description with a non-ASCII character. The case is then the first place the question can be settled.
  - the live outcome, meaning `size: now` created and #496 rolled. Answerer: the repository owner, from the next close-issues run.
- **The broad gate**: not run. This round handed it to nobody. See the probes table.

## Regression tests to plant

- `tests/test_a_declared_label_reaches_the_tracker.py`: the case in fix 1's
  fence, which needs `import re` at the module's head. It was seen red in
  this round against `a479a38`'s workflow.

## Facts for the evidence ledger

- C1's **Unverified here: the cap's value** can become **Read 2026-09-23**:
  GitHub's REST reference for *Create a label* says the description *"Must be
  100 characters or fewer."* The 404 on run `35796513013` stops being the
  only thing behind the number.
- The same page states no cap for a label's `name`, which is consistent with
  the overview's *Not done* choice not to pin one.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The roll step has no `if:`, so any failure of the label step skips the flow-measurement roll, which is #515's second cost | `.github/workflows/close-issues-on-release.yml:56-61` | open | The workflow has three steps in sequence with the default `success()` condition. The probe was red at `a479a38` and green with `if: ${{ !cancelled() }}`, and the neighbouring workflow cases stayed green |
| 2 | ⬜ The module docstring's case index omits the new cap case, and its §15 paragraph points every case's red run at `1790076050` | `tests/test_a_declared_label_reaches_the_tracker.py:10-34` | open | Read. The index lists A9 to A12. The new case's red run is in C1 |
| 3 | ⬜ correction: `overview.md` says five single-unit mutations, and C1 and the hand-back list four | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | open | Read. C1 names four mutations |
| 🟢 | The shortened description keeps what the label means and when it comes off | `.github/scripts/tracker_labels.py:111-114` | not a defect | 95 characters, measured. The first clause is the document's words minus the subject, and the close it names is the moment the document names |
| 🟢 | `LABEL_DESCRIPTION_LIMIT` lives beside one of its two users | `.github/scripts/label_merged_on_release_branch.py:104-113` | not a defect | Two functions call `gh label create`. The other reaches the constant through its existing `signal` import |
| 🟢 | T2 is edited in the shared ledger | `seal/ledger.md:2498` | not a defect | `CONTRIBUTING.md:204-215` gives the `--reverify` arm for a claim that still holds. `evidence-check --strict` returned 1468 ok |
| 🟢 | No other place in the tree states the old description or the 119-character state as current | tree at `a479a38` | not a defect | Read, `git grep`. The old text survives only as a quotation in `overview.md` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two changed case files | 44 passed, exit 0 |
| The cap case with the 119-character description restored | 2 failed (cap case and A9), exit 1. Reverted |
| `evidence-check --strict` on this work item's ledger fragment and on `seal/ledger.md` | 5 ok and 1468 ok, 0 drifted, exit 0 both |
| A `test_tmp_*` case asserting the roll step carries `if: ${{ !cancelled() }}` | red at `a479a38`, green with the line added. Reverted and deleted |
| That probe plus `test_a_declared_label_reaches_the_tracker.py` and `test_a_release_rolls_the_flow_measurement_issue.py`, with the fix | 52 passed, exit 0 |
| `test_release_hygiene.py -k "close or workflow or token"`, with the fix | 8 passed, exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due once the rounds leave nothing open |

## Paste-ready fixes

Finding 1, in `.github/workflows/close-issues-on-release.yml`, on the roll step:

```yaml
      # The roll reads the version in the tree and the open flow-measurement
      # issue, and nothing the steps above write. So a failure above must not
      # skip it: #515's over-long label description failed the label step and
      # cost a release its roll. The job still goes red on that failure.
      - name: roll the flow-measurement issue to the next version
        if: ${{ !cancelled() }}
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
        shell: bash
        run: python3 .github/scripts/roll_flow_measurement_issue.py
```

And the case, in `tests/test_a_declared_label_reaches_the_tracker.py` (add
`import re` to the imports):

```python
def test_a_failed_label_write_cannot_skip_the_roll():
    """#515's second cost. The label step failing skipped the roll behind it,
    because a step with no `if:` runs only when every step before it
    succeeded. The label reconcile is not a gate, so its failure must not
    decide whether the log rolls."""
    with open(WORKFLOW, encoding="utf-8") as f:
        text = f.read()
    steps = re.split(r"^      - ", text, flags=re.M)
    roll = [s for s in steps if s.startswith("name: roll the flow-measurement issue")]
    assert roll, "the workflow no longer has the roll step"
    assert re.search(r"^        if: \$\{\{ !cancelled\(\) \}\}\s*$", roll[0], re.M), (
        "the roll runs only when every step before it succeeded, so a failed "
        "label write skips it again"
    )
```

Finding 2, in the same module's docstring, after the A12 entry:

```text
  A13  every declared description fits the tracker's cap, read from
       `LABEL_DESCRIPTION_LIMIT` (#515); its red run is recorded in
       work item 1790134781's ledger row C1
```

Needs a fix: yes — finding 1, the roll step still depends on the label step succeeding
Loses a record or crashes: no

## Proof block

Files opened this round, all at `a479a38` in the clone unless noted:

- `.github/scripts/tracker_labels.py`, `.github/scripts/label_merged_on_release_branch.py`
- `.github/workflows/close-issues-on-release.yml`
- `.github/scripts/roll_flow_measurement_issue.py` (header)
- `tests/test_a_declared_label_reaches_the_tracker.py`, `tests/test_a_merged_ticket_says_so_on_the_tracker.py` (headers and the changed cases)
- `tests/test_release_hygiene.py:1020-1060`, `tests/test_a_release_rolls_the_flow_measurement_issue.py` (header)
- `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move*
- `CONTRIBUTING.md:202-216`
- `tests/test_no_real_identifiers.py` (allowlist)
- `skills/code-review/scripts/chain_check.py` (`CLOSED_WORDS`, `verdict_of`), in the user's checkout
- this work item's `routing.md`, `overview.md`, `changelog.md`, ledger fragment C1, and `seal/ledger.md` T2, from the diff
- #515's body, through `gh issue view`
