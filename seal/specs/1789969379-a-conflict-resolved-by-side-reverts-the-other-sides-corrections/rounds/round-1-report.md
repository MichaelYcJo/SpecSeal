# Round 1 — review report

| Field | Value |
|---|---|
| Work item | `1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections` (#424) |
| Branch | `fix/a-conflict-resolved-by-side-reverts-the-other-sides-corrections` |
| Base | `release/v0.12.2` |
| Target SHA | `d860978f40381e02b5694227e71c7c81636f9447` |
| Round | 1 — nothing inherited |
| Reviewed in | a `git clone --no-local` at the target SHA, under the session scratchpad |

The build is sound in its structure and unusually well evidenced. The check's
shape — merge walk, row survival, merge base, per-rev blob listing — holds up
against every axis I pushed it on, and the two units the builder found green
while broken are genuinely repaired: I re-ran both mutations and they go red.

One thing is wrong, and it is the middle of the work rather than an edge. The
marker the check matches is not the marker the file spells.

## 🔴 1 — the marker regex cannot see 38 of the 403 markers in the file it watches, and reports a loss when a resolution rewords one

`skills/evidence-check/scripts/correction_check.py#MARKER`

`MARKER` requires the date to follow the verb immediately. `seal/ledger.md`
does not spell it that way. Measured over the file at the target SHA:

| | occurrences in `seal/ledger.md` |
|---|---|
| markers the check matches | 365 |
| markers the file actually carries | 403 |
| **markers the check cannot see** | **38** |

The qualifiers sitting between the verb and the date, with their counts:
`again` ×19, `and re-executed` ×5, `a third time` ×4, `a fourth time` ×3,
`and re-stamped` ×2, `a fifth time` ×2, `and re-stamped again` ×1,
`and widened` ×1, `and re-measured` ×1.

One row of `seal/ledger.md` — `R4 · the printed bound reads BOTH of the
gate's walks …` — carries **only** the qualified spelling, so it is wholly
invisible: losing its marker at a merge reports nothing at all. And the
spelling is not a curiosity somebody wrote once. `git log -S "Re-read again"`
over `seal/ledger.md` returns six commits that introduced it, and
`hooks/worktree-guard.py:1954` writes it into a rider comment the same way.

**Both failure directions, which is the pair the design set out to avoid.**
Executed, through the CLI, against constructed merges:

- *Silent on a real loss.* A branch adds `Re-read again 2026-09-21 after
  #424.` to a row; the merge resolution reverts the row to its old text. The
  check answers `examined 1 merge commit(s)` · `no correction marker was
  dropped at a merge`, exit 0. That is #424's incident, and the check built
  for it says nothing.
- *Red on correct work.* Base and both parents carry `Re-read 2026-09-05`;
  the person resolving the conflict writes the merged cell as `Re-read again
  2026-09-05`. Nothing was lost — the verb stands, the date stands, the
  reading stands. The check exits 1 and reports the row as a loss.

The second one is `spec.md` A7 broken: *a marker whose sentence was reworded
but whose verb and date stand → reports nothing*. And it is the failure the
docstring names in its own words — *a check pinned to the prose goes red on a
rewording and stays quiet on a revert, which is both failure directions at
once*.

**Why nothing caught it.** The frame measured the spellings of the sentence
*after* the date and concluded the variation lives there. It also lives
before it, and nobody looked. `test_a_reworded_sentence_around_a_standing_marker_is_not_a_loss`
is A7's case and it only rewords the trailing sentence, so it is green while
A7 is broken — the third unit of that kind on this branch, after the two the
builder found. Measured: widening `MARKER` to accept a qualifier leaves all
35 cases in the module green, so nothing in the suite holds this axis in
either direction.

**§12 — the same false fact is stated in six places**, and the fix is owed to
all of them, not to the regex alone:

| Statement | What it says |
|---|---|
| `correction_check.py#MARKER` | the code |
| the module docstring, §*The marker is the leading verb and the date* | *10 rows … and 185 … (12 and 353 occurrences)* — those are the check's numbers, presented as the file's |
| `spec.md` §*What the markers actually look like* | *at least three spellings* — all three are after the date |
| `questions.md` §*What the framing settled from the tree* | the same |
| `seal/ledger/1789969379-…md` row C1's Notes | *at least three spellings of the `Corrected` sentence stand in `seal/ledger.md` today* — a ledger claim that is false about the tree, on a branch whose subject is ledger truth |
| `.github/workflows/hygiene.yml`, the leg's comment | *matched on the leading verb and date* |

## 🟡 2 — one lost marker is reported once per parent that carried it, and the closing count says so

`skills/evidence-check/scripts/correction_check.py#examine`

`examine` loops the parents and appends a `Report` for every loss each one
yields. Where both parents carried the marker — which is every marker the
merge base also carried, so the common case for anything older than the fork
— one lost marker produces two entries and the closing line reads `2
correction marker(s) … are gone`.

Executed: the false-positive fixture above printed two identical blocks for
one row and one marker, differing only in the `from parent` line, then `2
correction marker(s)`. A reader is told to open two hunks and there is one.

It does not hide a loss, so it is not the 🔴 above. It is the number a person
acts on, and `agent-contract` §14 is the rule that a change to what a person
reads gets pinned.

## 🟡 3 — the ambiguity guard is on the anchor route and not on the key route

`skills/evidence-check/scripts/correction_check.py#_index`,
`skills/evidence-check/scripts/correction_check.py#standing`

The docstring states the principle and the module has two cases for it: an
anchor set two rows cite decides nothing, *otherwise removing one of two rows
that cite one unit would report a loss because its neighbour still stands,
which is A3 broken by the fallback that exists to widen A1*.

The first cell is the other identity and it has no such guard. `standing`
returns `by_key.get(row.key, [])[0]` — the first row of the result carrying
that key, however many there are. So removing one of two rows that share a
first cell reports a loss against its twin, which is A3 broken by the cheap
identity exactly as it would be by the fallback.

**Not reachable in this repository today**, and I measured rather than
assumed it: of `seal/ledger.md`'s 189 marked rows, **0** have a key another
row shares. The only duplicated keys are the section table headers (`Clause`
×115, `Claim` ×8), which carry no markers. So this is a latent asymmetry
rather than a live false refusal — 🟡 and not 🔴 for that reason.

The 115-way header collision is worth seeing, though: `rows()` returns table
header lines as `Row` objects, and `test_a_separator_and_a_header_are_not_rows_that_can_be_lost`
asserts exactly that (`== ["Claim"]`) under a name saying the opposite. The
fix below makes the collision decide nothing, which is the right answer for a
header either way.

## 🟡 4 — the case that pins the skill's *when it runs* cannot fail for its subject

`tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_skill_says_what_the_command_is_for_and_when_it_runs`

The case asserts `"squash" in text` over the whole of
`skills/evidence-check/SKILL.md`. The word appears three times in that file
and two of them are in unrelated sections — *A coordinate names content,
never a position* (line 150) and *Migrating a pre-anchor ledger* (line 480).

Executed: I deleted the entire paragraph that states this command's moment —
*Its moment is the pull request, and it has no other* — from the
`correction-check` section and ran the case. It passed, with two `squash`
mentions still standing elsewhere.

`phases/phase-5.md` records the opposite: *Driving that case red needed every
occurrence of `squash` removed from the skill … which is the right shape,
since a single mention is not a statement anybody meets.* The reasoning does
not hold, because the other two mentions are about other subjects. The case
is a check that cannot fail for the thing it is about, which is
`skills/verify/SKILL.md` §*The Seal Test* — and it is the one case on this
branch that was driven red by an edit that did not actually remove its
subject.

## ⬜ 5 — `broad_gate.py` does not mirror the sixth arm: an issue for later, not a defect this branch ships

You asked me to rule. **Issue for later.** Three grounds, in the order they
weigh:

- **The bounded failure.** A branch seals green and then meets a red leg at
  its pull request. The leg still catches the defect; nothing reaches a
  release unchecked. The cost is one wasted seal and a surprise, not a lost
  correction.
- **The contract.** `spec.md` §*Data & interfaces* enumerates the coordinates
  this work touches and `broad_gate.py` is not among them. A reviewer who
  treats the spec as binding when it constrains the builder cannot treat it
  as advisory when it constrains the reviewer.
- **The second subject is real.** The gate resolves its own base, and #423 —
  the work item that merged immediately before this one — exists because that
  resolution was wrong. Adding an arm means resolving a base again, which is
  a failure mode with its own cases.

What makes it *not* a defect rather than a deferred one: I measured the
branch's own range and it holds no merge (`no merge commit in
755629d..d860978`), so this branch's seal and this branch's leg will agree.

Two things I would hold the owner to when routing it. The disclosure in
`overview.md` §*Not done* names the answerer as *the repository owner, as an
issue opened from this pull request* — that issue does not exist yet, and a
named answerer with no artifact is how #386's class starts. And the ticket's
real subject is wider than one arm: nothing holds the gate's check list
against the workflow's arms, so the seventh arm will arrive the same way.

## ⬜ 6 — the rule documents' sentence about where the leg runs is narrower than the leg

`CLAUDE.md:157`, `CONTRIBUTING.md:231`, `skills/evidence-check/SKILL.md:341`

All three say the hygiene workflow runs the check *on every pull request into
a release branch*. The workflow's condition is `base_ref != "main"`, so it
runs on every pull request whose base is not `main`. The sentence is true and
not exhaustive. Left as a correction because the behaviour and the fact both
stand; I raise it only because three documents were deliberately pinned
against each other here and all three carry the same narrowing.

# Verification — what I checked rather than accepted

**The three frame claims.** All three hold.

1. **`Checked` is read by no machine.** Confirmed, and I widened the search
   past the frame's. `grep -n "Checked"` over `evidence_check.py` returns
   exactly lines 1577 and 1587, both inside the `# RIDER:` at `reverify()`.
   Over the whole tree outside `seal/`, the only other hits are fixture table
   headers in five test modules and two unrelated English sentences in
   `skills/implement/scripts/seal.py`. Nothing reads the column. `spec.md`
   §*The ticket's second direction is wrong about the tree* is right and Q1's
   default stands.
2. **The marker counts.** `grep -c` gives 10 `Corrected` rows and 185
   `Re-read` rows in `seal/ledger.md`, plus 4 `Re-read` rows in the one live
   fragment — 189, as the frame says. Occurrences are 12 and 353. The
   builder's correction is right and nothing in the frame's conclusions turns
   on it. But see 🔴 1: both numbers count rows the check watches, and the
   file carries 190 marked rows and 403 occurrences.
3. **Row survival is `CLAUDE.md`'s own rule.** `CLAUDE.md:121`, §*A row whose
   anchor a change removes is REMOVED, not re-pointed*, and it is in the base
   at `release/v0.12.2` — pre-existing, not a judgment this work invented.
   `templates/ledger.md:72` states it a second time.

**The merge-base divergence, and whether `87eced1` is correct work.**
Confirmed correct work, and on stronger grounds than the record gives.
`git merge-base` of its two parents returns the *first parent itself* — the
release branch was a descendant of `main`, so the merge is a `--no-ff` of a
fast-forwardable branch. The merge result's `seal/ledger.md` is
**byte-identical to the second parent's**. There was no resolution; nobody
read anything; one parent had already decided the whole file. Reporting it
would be reporting a merge with no act in it.

**Does the base test only narrow?** Yes, for reports — `honoured` is a filter
applied to `losses`, so it can only remove. One thing it does that is more
than narrowing, and the code is honest about it: a merge whose parents share
no history has no base, so it is skipped entirely rather than judged by the
old rule, and it is named under `not judged`. That is the disclosure that
keeps the narrowing from being a silent pass.

**The two units that were green while broken.** Both repairs measure what
they claim. Mutating `standing` to fall back to the first row of the result —
placed where it is actually reachable — turns **4 cases red**, A3's among
them. Removing `_index`'s ambiguity guard turns
`test_two_result_rows_sharing_one_anchor_decide_nothing_either` red.
Switching `honoured` off turns its case red. **The third of the same kind is
🔴 1's A7 case**, and 🟡 4 is a fourth.

**Is the hygiene leg wired where M2 says?** Yes, read at the workflow. The
`release` job has no `if`, the workflow has no path filter, the trigger
carries the four default `pull_request` types plus `ready_for_review` and
`converted_to_draft`, and `actions/checkout@v4` runs with `fetch-depth: 0` —
so `origin/<base>` resolves and the merge ref is complete. The step sits
after the survivor step, skips `main` with a printed reason, and passes
`origin/${{ github.base_ref }}...HEAD`. M2's two cases execute the
reachability claim at the merge ref and after the squash.

**Do the two rule documents say the same thing?** Yes — both carry both
paragraphs, each names the other and names the case, and
`test_a8_both_rule_documents_say_what_to_do_at_the_conflict` matches six
needles over whitespace-collapsed text, which survives the 88-column wrap.
Held against the check's behaviour, they agree, with the one narrowing at
⬜ 6.

**The ledger fragment.** 8 rows, 14 anchors, all resolving — `evidence_check.py .`
unscoped reports `14 ok · 0 drifted · 0 broken` for it and exit 0 overall.
The rows say what the code does, with one exception: row C1's Notes cell
states a fact about the tree that is false, which is inside 🔴 1.

# What I could not judge

| Item | Who answers it |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer. `agent-contract` §2 leaves the broad gate to the agent whose definition assigns it, and `agents/warden.md` assigns none. I ran no broad command |
| whether the leg behaves on a real runner | CI, at this branch's pull request |
| Linux and Windows | CI's matrix |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The marker regex requires the date to follow the verb immediately; 38 of `seal/ledger.md`'s 403 markers put a qualifier between them. Silent on a real loss, and red on a resolution that rewords one. A7 broken, and the same false fact is stated in six places | `skills/evidence-check/scripts/correction_check.py#MARKER` | open | Executed: both directions reproduced through the CLI against constructed merges. Measured: 403 markers in the file, 365 matched, 1 row wholly invisible, 9 qualifier spellings, 6 commits in history that introduced `Re-read again` |
| 2 | One lost marker is reported once per parent that carried it, so the closing count over-reports | `skills/evidence-check/scripts/correction_check.py#examine` | open | Executed: one marker lost from one row printed two entries and `2 correction marker(s)` |
| 3 | `_index` guards anchor ambiguity and nothing guards key ambiguity, so removing one of two rows sharing a first cell would report a loss against its twin — A3 broken by the cheap identity | `skills/evidence-check/scripts/correction_check.py#_index` | open | Read, and measured for reach: 0 of 189 marked rows share a key today, so latent rather than live. The two duplicated keys are section headers |
| 4 | The case pinning the skill's *when it runs* asserts `squash` over the whole file, and the word appears twice more in unrelated sections | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_skill_says_what_the_command_is_for_and_when_it_runs` | open | Executed: deleting the whole paragraph that states the command's moment left the case green |
| 5 | ⬜ `broad_gate.py` does not mirror the new hygiene arm | `skills/verify/scripts/broad_gate.py#gate` | deferred #468 | Ruled an issue for later, not a defect this branch ships: the leg still catches the defect, `spec.md` §*Data & interfaces* excludes the coordinate, and the branch's own range holds no merge so its seal and its leg agree. The issue is owed and does not exist yet |
| 🟢 | The rule documents say the leg runs on a pull request into a release branch; the workflow's condition is `base_ref != "main"` | `CLAUDE.md#"## Repo rule — a change writes fragments, never the shared file"` | not a defect | True and not exhaustive. Behaviour and fact both stand |
| 🟢 | `Checked` is read by no machine — the frame's claim | `skills/evidence-check/scripts/evidence_check.py#reverify` | not a defect | Verified wider than the frame: two hits in `evidence_check.py`, both in the rider; every other hit in the tree is a fixture header or unrelated prose |
| 🟢 | The marker counts are rows, not occurrences — the builder's correction | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Where spec and implementation diverged* | not a defect | Measured: 10/185 rows, 12/353 occurrences. Nothing in the frame's conclusions turns on it |
| 🟢 | Row survival is `CLAUDE.md`'s own rule, not a judgment this work invented | `CLAUDE.md#"## Repo rule — a change writes fragments, never the shared file"` | not a defect | `CLAUDE.md:121` and `templates/ledger.md:72`, both present in the base at `release/v0.12.2` |
| 🟢 | `87eced1` is correct work and the merge base only narrows — M1's judgment | `skills/evidence-check/scripts/correction_check.py#honoured` | not a defect | Executed: the merge base equals the first parent and the merge's ledger text is byte-identical to the second parent's. `honoured` filters `losses`, so it can only remove reports; a merge with no base is skipped and named under `not judged` |
| 🟢 | The two units that were green while broken now measure what they claim | `skills/evidence-check/scripts/correction_check.py#standing` | not a defect | Executed: a reachable permissive `standing` turns 4 cases red; removing `_index`'s guard turns its case red; switching `honoured` off turns its case red |
| 🟢 | The hygiene leg is wired where M2 says | `.github/workflows/hygiene.yml` | not a defect | Read: `release` job, no `if`, no path filter, `fetch-depth: 0`, the step skips `main` with a printed reason and passes `origin/${{ github.base_ref }}...HEAD` |
| 🟢 | The new ledger fragment's 8 rows and 14 anchors resolve | `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` | not a defect | Executed: `evidence_check.py .` unscoped, exit 0, `14 ok · 0 drifted · 0 broken` for the fragment. Row C1's Notes carries a false claim, which is finding 1 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py -q`, in the clone at the target SHA | 35 passed |
| `python3 skills/evidence-check/scripts/evidence_check.py .` — unscoped, exit code read directly | exit 0 · `total: 1384 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `correction_check.py --range origin/release/v0.12.2...HEAD` | exit 0 · `no merge commit in 755629d..d860978` |
| `correction_check.py --range <root commit>..HEAD` over 31 reachable merges | exit 0 · `no correction marker was dropped at a merge` |
| Marker census over `seal/ledger.md` with a widened pattern | 403 occurrences against the check's 365; 9 qualifier spellings; 1 row invisible |
| Key- and anchor-ambiguity census over the three ledger files | 189 marked rows, 0 with a shared key; 20 ambiguous anchor sets; headers duplicate `Clause` ×115 |
| Constructed merge: a `Re-read again <date>` correction reverted by the resolution | exit 0 · `no correction marker was dropped` — the loss is silent |
| Constructed merge: the resolver rewords `Re-read <date>` to `Re-read again <date>` | exit 1 · one row reported twice · `2 correction marker(s)` |
| Mutation: `standing` made permissive, reachably | 4 failed, 31 passed — A3's guard is sound |
| Mutation: `_index`'s ambiguity guard removed | 1 failed — sound |
| Mutation: `honoured` always False | 1 failed — sound |
| Mutation: `MARKER` widened to accept a qualifier | 35 passed — nothing pins this axis |
| Mutation: the skill's whole *when it runs* paragraph deleted | 1 passed — the case cannot fail for its subject |
| Coverage probe — the 8 structural modules that read `CLAUDE.md`, `CONTRIBUTING.md`, `bin/` and the hygiene workflow, in the clone | 243 passed, 8 skipped. No existing case goes red for the branch, including the sixth-arm gap |
| the full suite, the repository-wide lint, the typecheck | not yet — `agent-contract` §2 leaves the broad gate to the sealer, and `agents/warden.md` assigns it to nobody here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — and the issue it names, which does not exist yet | the repository owner |

## Paste-ready fixes

Finding 1 — the marker is the verb and the date, with whatever short
qualifier the writer put between them. The rule stays structural rather than
a vocabulary, because a word list is the prose-pinning the design rejects:

```python
# The two verbs, and the date shape. Nothing AFTER the date is read, and a
# short run of lowercase words BEFORE it is read as part of the marker rather
# than as a different one. Measured over `seal/ledger.md`: 403 markers, of
# which 38 are spelled `Re-read again <date>`, `Re-read a third time <date>`,
# `Corrected and widened <date>`, `Re-read and re-executed <date>` and five
# more shapes, and one row carries nothing else. A pattern that demands the
# date immediately is silent when one of those is reverted, and reports a
# loss the moment a resolution rewords `Re-read <date>` into `Re-read again
# <date>` -- both failure directions at once, which is what matching the
# sentence was rejected for.
#
# Four words is the bound and lowercase is the gate: a marker's qualifier is
# a phrase inside the sentence, so a capital letter is the next sentence and
# a digit is the date itself. The identity stays `(verb, date)`, so the two
# spellings of one reading compare equal and a reword is not a loss.
VERBS = ("Corrected", "Re-read")
MARKER = re.compile(
    r"\b(" + "|".join(VERBS) + r")"
    r"(?:[ \t]+[a-z][a-z-]*){0,4}"
    r"[ \t]+(\d{4}-\d{2}-\d{2})(?!\d)"
)
```

The cases that hold it, both directions, red against the pattern above being
narrowed back:

```python
def test_a_qualifier_between_the_verb_and_the_date_is_the_same_marker():
    """The file spells 38 of its 403 markers this way -- `again` 19 times.
    A pattern that demands the date immediately watches neither the row nor
    the reword."""
    assert cc.markers("Re-read again 2026-09-05 and widened.") == {
        ("Re-read", "2026-09-05"): 1
    }
    assert cc.markers("Re-read a third time 2026-09-04.") == {
        ("Re-read", "2026-09-04"): 1
    }
    assert cc.markers("Corrected and widened 2026-09-07 by #98.") == {
        ("Corrected", "2026-09-07"): 1
    }


def test_the_qualifier_does_not_swallow_the_next_sentence():
    """A capital letter is the next sentence and a digit is the date."""
    assert cc.markers("Corrected. The row was Re-read 2026-09-05.") == {
        ("Re-read", "2026-09-05"): 1
    }
    assert cc.markers("Re-read 2026-09-05 and widened. Re-read 2026-09-06.") == {
        ("Re-read", "2026-09-05"): 1,
        ("Re-read", "2026-09-06"): 1,
    }


def test_a_resolution_that_rewords_the_qualifier_is_not_a_loss():
    """A7, in the direction the tree actually spells. The verb stands and
    the date stands; only the qualifier moved."""
    before = "| R1 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. |"
    after = "| R1 · a claim | `a/b.py#f@11111111` | Re-read again 2026-09-05. |"
    assert cc.losses(ledger(before), ledger(after)) == []


def test_a_qualified_marker_reverted_at_a_merge_is_reported(tmp_path):
    """A1 and A2, over the spelling one row of `seal/ledger.md` carries and
    nothing else. Red against the pattern demanding the date immediately."""
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. |"
    corrected = (
        "| A1 · the first claim | `a/one.py#f@11111111` "
        "| Read. Re-read again 2026-09-21 after #424. |"
    )
    root, start, head = merged(
        tmp_path, ledger(row), ledger(corrected), ledger(row), ledger(row)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert "Re-read 2026-09-21" in out, out
```

The other five statements of the same fact. Each is prose, and each says the
variation lives after the date:

```text
correction_check.py, module docstring, §*The marker is the leading verb
and the date, never the sentence*
    "10 rows ... and 185 carry a `Re-read` (12 and 353 occurrences ...)"
  → say these are the ROW counts a `grep -c` gives, that the file carries
    403 marker occurrences on 190 rows, and that the qualifier between the
    verb and the date is why the two numbers differ.

  Add under **Nothing after the date is read**:
    **And a short qualifier before it is.** `Re-read again <date>`, `Re-read
    a third time <date>`, `Corrected and widened <date>`: 38 of this
    repository's 403 markers, and one row carries no other spelling. The
    marker's identity is the verb and the date, so the qualifier changes
    neither -- which is what keeps a reworded marker from reading as a lost
    one.

spec.md §*What the markers actually look like, measured before anything is
built*
    "Spellings seen | at least three -- `...by issue #98.`, ..."
  → those three vary AFTER the date. Add the column or the sentence for the
    nine that vary before it, with the counts.

questions.md §*What the framing settled from the tree*, the third bullet
    "Markers are matched on the leading verb and date."
  → "on the leading verb and the date, with any short qualifier between them
    read as part of the marker."

seal/ledger/1789969379-...md row C1, Notes cell
    "at least three spellings of the `Corrected` sentence stand in
     `seal/ledger.md` today"
  → the claim is false about the tree as it stands. Rewrite the cell to say
    what was measured: 403 markers, 9 qualifier spellings before the date and
    three sentence spellings after it. The row's Verified behavior cell needs
    the new cases named, and the hash re-stamped with
    `evidence-check --reverify`.

.github/workflows/hygiene.yml, the leg's comment
    "matched on the leading verb and date and never on the sentence after it"
  → "... and never on the sentence after it, with a short qualifier before
    the date read as part of the marker."
```

Finding 2 — one marker gone from one row is one loss, whichever parents
carried it. In `examine`, replace the parent loop's body:

```python
            # One marker gone from one row is ONE loss, whichever parents
            # carried it -- and every marker older than the fork is carried
            # by both. Appending per parent made the closing line read `2
            # correction marker(s)` for one row and one marker, which sends a
            # reader to open two hunks when there is one. The parent reported
            # is the one that lost the most occurrences of it, because that
            # is the side whose text most needs reading.
            #
            # Grouped by `(row key, marker)` rather than deduplicated: a row
            # that carried one marker in two cells and carries it in none has
            # lost it twice, and that pair is still two entries.
            carried = {}
            for parent in kin:
                text = blobs.get((parent, path))
                if text is None:
                    continue
                for loss in losses(text, result):
                    if honoured(loss, in_base, held):
                        continue
                    tag = (loss.row.key, loss.marker)
                    carried.setdefault(tag, {}).setdefault(parent, []).append(loss)
            for by_parent in carried.values():
                parent, group = max(by_parent.items(), key=lambda kv: len(kv[1]))
                for loss in group:
                    reports.append(Report(path, merge, parent, loss))
```

```python
def test_a_marker_both_parents_carried_is_reported_once(tmp_path):
    """One marker gone from one row is one loss. Reporting it per parent
    told a reader to open two hunks for one, and the closing count said
    two."""
    row = "| A1 · the first claim | `a/one.py#f@11111111` | Read. Re-read 2026-09-05. |"
    ours = "| A1 · the first claim | `a/one.py#f@11111111` | Read. Re-read 2026-09-05. | ours |"
    theirs = "| A1 · the first claim | `a/one.py#f@11111111` | Read. Re-read 2026-09-05. | theirs |"
    dropped = "| A1 · the first claim | `a/one.py#f@11111111` | Read. | both |"
    root, start, head = merged(
        tmp_path, ledger(row), ledger(ours), ledger(theirs), ledger(dropped)
    )
    code, out = check(root, f"{start}..{head}")
    assert code == 1, out
    assert out.count("lost        Re-read 2026-09-05") == 1, out
    assert "1 correction marker(s)" in out, out
```

Finding 3 — the key route gets the guard the anchor route has. Replace
`_index` and `standing`, and the two lines in `losses` that build the
parent's ambiguity:

```python
def _index(parsed):
    """`(by_key, by_anchor)` for a file's rows.

    Neither index answers where it holds two answers. `by_anchor` keeps only
    anchor sets that ONE row of this file cites; `by_key` keeps only first
    cells that ONE row carries. The second guard is the first one's own
    argument applied to the other identity -- removing one of two rows that
    share a first cell would otherwise report a loss because its twin still
    stands, which is A3 broken by the cheap identity exactly as it would be
    by the fallback. It also disposes of the section table headers, which
    `rows` returns like any other row and which repeat once per section.
    """
    by_key, by_anchor = {}, {}
    shared_keys, shared = set(), set()
    for row in parsed:
        if row.key in by_key or row.key in shared_keys:
            shared_keys.add(row.key)
            by_key.pop(row.key, None)
        else:
            by_key[row.key] = row
        if not row.anchors:
            continue
        if row.anchors in by_anchor or row.anchors in shared:
            shared.add(row.anchors)
            by_anchor.pop(row.anchors, None)
            continue
        by_anchor[row.anchors] = row
    return by_key, by_anchor


def standing(row, ambiguous, ambiguous_keys, by_key, by_anchor):
    """The row in the result that IS `row`, or None if it did not survive.

    `ambiguous` and `ambiguous_keys` are the anchor sets and the first cells
    more than one row of the PARENT carries. A row whose identity is
    ambiguous on one side falls through to the other, and a row ambiguous on
    both is not identified at all -- silence, which is the direction A3
    argues for.
    """
    if row.key not in ambiguous_keys:
        found = by_key.get(row.key)
        if found is not None:
            return found
    if row.anchors and row.anchors not in ambiguous:
        return by_anchor.get(row.anchors)
    return None
```

```python
    seen = Counter()
    keys = Counter()
    for row in parsed:
        keys[row.key] += 1
        if row.anchors:
            seen[row.anchors] += 1
    ambiguous = {anchors for anchors, count in seen.items() if count > 1}
    ambiguous_keys = {key for key, count in keys.items() if count > 1}
    by_key, by_anchor = _index(rows(result_text))
    found = []
    for row in marked:
        survivor = standing(row, ambiguous, ambiguous_keys, by_key, by_anchor)
```

```python
def test_two_rows_sharing_a_first_cell_decide_nothing_either():
    """The ambiguity guard is not the anchor route's alone. Two rows with
    the same first cell, one removed, is a removal -- and reporting it
    because its twin still carries that cell is A3 broken by the cheap
    identity. `seal/ledger.md` has 123 such rows today: every section's
    table header."""
    a = "| same cell | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    b = "| same cell | `a/c.py#g@22222222` | Re-read 2026-09-05. | none |"
    assert cc.losses(ledger(a, b), ledger(b)) == []


def test_a_key_two_result_rows_share_decides_nothing():
    """The same guard on the result's side, which is where `_index` holds
    it for anchors."""
    parent = "| R6 · one claim | `a/b.py#f@11111111` | Corrected 2026-09-15. | none |"
    half = "| R6 · one claim | `a/b.py#f@11111111` | none | first half |"
    other = "| R6 · one claim | `a/c.py#g@22222222` | none | second half |"
    assert cc.losses(ledger(parent), ledger(half, other)) == []
```

Finding 4 — read inside the section the paragraph belongs to:

```python
def test_the_skill_says_what_the_command_is_for_and_when_it_runs():
    """A document that names a script has to give a reader a way to reach it
    (`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`), and
    a check whose moment nobody states is one that gets run at the wrong one:
    the merges it reads stop existing at the squash.

    Read inside the `correction-check` section, not over the whole file.
    `squash` appears twice more in this skill -- under *A coordinate names
    content, never a position* and under *Migrating a pre-anchor ledger* --
    so a whole-file assertion stayed green with this command's entire
    *when it runs* paragraph deleted. Measured, and that is the counterfeit
    `skills/verify/SKILL.md` §*The Seal Test* is about.
    """
    whole = read(os.path.join("skills", "evidence-check", "SKILL.md"))
    assert "correction-check" in whole
    parts = whole.split("## `correction-check`")
    assert len(parts) == 2, "the skill has no `correction-check` section"
    section = parts[1].split(" ## ")[0]
    assert "squash" in section, (
        "the `correction-check` section does not say when the command runs; "
        "the merges it reads stop existing at the squash, and a check whose "
        "moment nobody states gets run at the wrong one"
    )
```

Needs a fix: yes — findings 1, 2, 3 and 4. Finding 1 is the one that matters: the check is blind to 38 of the 403 markers in the file it watches, and reports a loss when a resolution rewords one.
Loses a record or crashes: no — nothing here writes, nothing crashed in any run, and no record leaves the root that would not have left without this branch. Finding 1 under-detects a loss rather than causing one; the branch is strictly better than the tree without it.

# Proof block

Files opened, in this repository unless noted, plus the same tree cloned at
`d860978f40381e02b5694227e71c7c81636f9447` under the session scratchpad,
where every command above was run:

- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/routing.md`, `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md` (listing only)
- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/phases/phase-1.md` … `phase-5.md`
- `skills/evidence-check/scripts/correction_check.py` (whole)
- `tests/test_a_merge_cannot_silently_drop_a_correction.py` (whole)
- `.github/workflows/hygiene.yml` (lines 1–60, 200–305)
- `bin/correction-check`, `bin/correction-check.cmd`, `bin/` listing
- `CLAUDE.md` and `CONTRIBUTING.md` — the diff hunks and the surrounding rule
- `skills/evidence-check/SKILL.md` — the diff hunk and the `squash` occurrences
- `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` (whole)
- `seal/ledger.md` — by census and by `grep`, never opened whole
- `skills/evidence-check/scripts/evidence_check.py` — the `Checked` hits only
- `skills/verify/scripts/broad_gate.py` — the arm list and the docstring header
- `tests/test_the_gate_asks_the_range_ci_will_ask.py` (lines 1–60, 600–720, 840–920)
- `templates/ledger.md` (lines 40–80)
- `gh issue view 424`
