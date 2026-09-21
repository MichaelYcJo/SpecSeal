# 1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections — review round 1

| Field | Value |
|---|---|
| Target SHA | d860978f40381e02b5694227e71c7c81636f9447 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 467 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `27535c8f76b0b665aa959560d5f226088202f785..d9a2e57df28e9402189d0f719bab82a565955310`, 5 commits |
| Contract changes | standing → round-1-report.md, round-1.md, losses |
| New units | test_a_qualifier_between_the_verb_and_the_date_is_the_same_marker (depth 1); test_the_qualifier_does_not_swallow_the_next_sentence (depth 1); test_a_capital_word_after_the_verb_is_not_a_qualifier (depth 1); test_a_run_long_enough_to_be_a_sentence_is_not_a_qualifier (depth 1); test_a_resolution_that_rewords_the_qualifier_is_not_a_loss (depth 1); test_a_qualified_marker_reverted_at_a_merge_is_reported (depth 1); test_a_marker_both_parents_carried_is_reported_once (depth 1); test_two_rows_sharing_a_first_cell_decide_nothing_either (depth 1); test_a_key_two_result_rows_share_falls_through_to_the_anchors (depth 1); test_a_row_ambiguous_on_both_identities_is_not_identified (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4. Finding 1 is the one that matters: the check is blind to 38 of the 403 markers in the file it watches, and reports a loss when a resolution rewords one. |
| Loses a record or crashes | no — nothing here writes, nothing crashed in any run, and no record leaves the root that would not have left without this branch. Finding 1 under-detects a loss rather than causing one; the branch is strictly better than the tree without it. |
<!-- New units: .github/workflows/hygiene.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1, the first round of the work item: the whole branch against its own
frame, spec compliance before quality.

The reviewer was told something unusual and told it plainly — **the frame was
drawn by the orchestrating session rather than by a framer**, after two
`framer` spawns died to the harness's no-progress watchdog without writing a
file. So the spec was handed over as something to distrust rather than to
measure against, with the note that the separation which matters survives
(the builder is `smith` and did not write the contract), and that if the spec
is wrong about the tree it should say so.

Three of the frame's own claims were named as checkable and asked for by
measurement rather than by assumption: that `Checked` is read by no machine
in the repository, that the marker counts are what the frame says, and that
row survival is `CLAUDE.md`'s rule rather than a judgment this work invented.
Three declared divergences were handed over the same way — the merge base as a
third input, the row-versus-occurrence correction to the counts, and an
unreadable blob being named rather than passed.

**Two units the builder had found green while broken** were named, with the
instruction that a unit green while broken is a unit whose case was not
measuring what it claimed, and that a third of the same kind should be looked
for.

On the reviewer's own account: whether the marker regex can miss a marker a
person would write or match one they did not; whether the check can refuse
correct work at a merge this repository will actually make; whether the leg is
wired where M2 says; whether the two rule documents agree with each other and
with the check's behaviour; and whether the new fragment's rows say what the
code does.

One ruling was asked for rather than a finding: whether `broad_gate.py` not
mirroring the new sixth hygiene arm is a defect this branch ships or an issue
for later.

`evidence_check.py .` unscoped. Exit codes read directly. `seal/ledger.md` was
declared off-limits to a whole read — 2364 lines, 1.07 MB — with the two
stalled spawns given as the reason.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The marker regex requires the date to follow the verb immediately; 38 of `seal/ledger.md`'s 403 markers put a qualifier between them. Silent on a real loss, and red on a resolution that rewords one. A7 broken, and the same false fact is stated in six places | `skills/evidence-check/scripts/correction_check.py#MARKER` | **fixed** `92ea378c` | fixed at 92ea378c — the pattern, 3f64cda2 the class — nine statements, not the six the round enumerated; Executed: both directions reproduced through the CLI against constructed merges. Measured: 403 markers in the file, 365 matched, 1 row wholly invisible, 9 qualifier spellings, 6 commits in history that introduced `Re-read again` |
| 2 | One lost marker is reported once per parent that carried it, so the closing count over-reports | `skills/evidence-check/scripts/correction_check.py#examine` | **fixed** `796a72ed` | fixed at 796a72ed; Executed: one marker lost from one row printed two entries and `2 correction marker(s)` |
| 3 | `_index` guards anchor ambiguity and nothing guards key ambiguity, so removing one of two rows sharing a first cell would report a loss against its twin — A3 broken by the cheap identity | `skills/evidence-check/scripts/correction_check.py#_index` | **fixed** `796a72ed` | fixed at 796a72ed — ; one sub-point of the paste-ready case answered rather than applied, with the contradiction recorded in the case docstring; Read, and measured for reach: 0 of 189 marked rows share a key today, so latent rather than live. The two duplicated keys are section headers |
| 4 | The case pinning the skill's *when it runs* asserts `squash` over the whole file, and the word appears twice more in unrelated sections | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_skill_says_what_the_command_is_for_and_when_it_runs` | **fixed** `796a72ed` | fixed at 796a72ed; Executed: deleting the whole paragraph that states the command's moment left the case green |
| 5 | ⬜ `broad_gate.py` does not mirror the new hygiene arm | `skills/verify/scripts/broad_gate.py#gate` | deferred #468 | Ruled an issue for later, not a defect this branch ships: the leg still catches the defect, `spec.md` §*Data & interfaces* excludes the coordinate, and the branch's own range holds no merge so its seal and its leg agree. The issue is owed and does not exist yet |
| 🟢 | The rule documents say the leg runs on a pull request into a release branch; the workflow's condition is `base_ref != "main"` | `CLAUDE.md#"## Repo rule — a change writes fragments, never the shared file"` | not a defect | True and not exhaustive. Behaviour and fact both stand |
| 🟢 | `Checked` is read by no machine — the frame's claim | `skills/evidence-check/scripts/evidence_check.py#reverify` | not a defect | Verified wider than the frame: two hits in `evidence_check.py`, both in the rider; every other hit in the tree is a fixture header or unrelated prose |
| 🟢 | The marker counts are rows, not occurrences — the builder's correction | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Where spec and implementation diverged* | not a defect | Measured: 10/185 rows, 12/353 occurrences. Nothing in the frame's conclusions turns on it |
| 🟢 | Row survival is `CLAUDE.md`'s own rule, not a judgment this work invented | `CLAUDE.md#"## Repo rule — a change writes fragments, never the shared file"` | not a defect | `CLAUDE.md:121` and `templates/ledger.md:72`, both present in the base at `release/v0.12.2` |
| 🟢 | `87eced1` is correct work and the merge base only narrows — M1's judgment | `skills/evidence-check/scripts/correction_check.py#honoured` | not a defect | Executed: the merge base equals the first parent and the merge's ledger text is byte-identical to the second parent's. `honoured` filters `losses`, so it can only remove reports; a merge with no base is skipped and named under `not judged` |
| 🟢 | The two units that were green while broken now measure what they claim | `skills/evidence-check/scripts/correction_check.py#standing` | not a defect | Executed: a reachable permissive `standing` turns 4 cases red; removing `_index`'s guard turns its case red; switching `honoured` off turns its case red |
| 🟢 | The hygiene leg is wired where M2 says | `.github/workflows/hygiene.yml` | not a defect | Read: `release` job, no `if`, no path filter, `fetch-depth: 0`, the step skips `main` with a printed reason and passes `origin/${{ github.base_ref }}...HEAD` |
| 🟢 | The new ledger fragment's 8 rows and 14 anchors resolve | `seal/ledger/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections.md` | not a defect | Executed: `evidence_check.py .` unscoped, exit 0, `14 ok · 0 drifted · 0 broken` for the fragment. Row C1's Notes carries a false claim, which is finding 1 |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `broad_gate.py` does not mirror the new hygiene arm, so a branch can seal green and meet a red leg | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/overview.md` §*Not done* — and the issue it names, which does not exist yet | the repository owner |
