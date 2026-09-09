# 1788912166-red-for-following-the-documents-green-for-ignoring-one — review round 1

| Field | Value |
|---|---|
| Target SHA | e26b5ed |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #302 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | whole_range → round-1-report.md, round-1.md, main; report → report, main, round-3.md, round-1.md, round-1-report.md, round-3-report.md, pytest |
| New units | OWNER_DIR (depth 1); CLAIM_A (depth 1); CLAIM_B (depth 1); ITEM_A (depth 1); probe_git (depth 1); base_and_item_a (depth 1); declaration_of_a (depth 1); test_a_work_items_own_declaration_still_holds_in_the_ci_spelling (depth 1); test_a_declaration_does_not_reach_a_work_item_that_did_not_write_it (depth 1); BROAD_GATE_ROW (depth 1); UNKNOWN_SHAPES (depth 1); UNKNOWN_IDS (depth 1); test_a_broad_gate_cell_nobody_can_parse_is_reported_below_the_cutoff (depth 1); test_a_one_word_cell_is_not_a_way_past_the_arm (depth 1); test_a_gate_sha_on_a_divergent_line_makes_no_claim_and_says_so (depth 1) |
| Needs a fix | yes — 🔴 1, 🔴 2 and 🟡 3 (🟡 4 is a thin pin the smith may answer |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The first review of three checks that judge pull requests, on a branch whose
own pull request is the first thing two of them judge. What the round was
asked is whether each arm refuses exactly what its document says it refuses,
and whether the two judgments taken beyond the specification's letter are the
right ones. The class to enumerate was every case putting an above-cutoff
round record in front of a ready `chain_check`, by construction rather than
by grep, because the implementer's own enumeration had been short by the
generated half and said so.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A range declaration spelled `origin/<base>...HEAD` resolves to whatever range the current run is over, so one work item's row excuses every later work item on the same base and turns the step off | `skills/code-review/scripts/survivor_check.py:772` | **fixed** `7355201` | fixed at 7355201 — a declaration is anchored on the range AND the work item directory it sits in; refused ones print under `not yours` with that work item named. Two cases seen red first, on a fixture that varies the checkout rather than the spec's text. §12: the false bound corrected in all four live carriers and struck through in `phases/phase-3.md`; Executed: work item B exits 1 alone and 0 with work item A's row on `--exempt`. `hygiene.yml:229` globs every work item's file into `--exempt`; the recommended spelling is the module docstring's own example. The stated bound — the row cannot outlive the deletion it was written for — does not hold for it |
| 🔴 2 | Above the cutoff a `Broad gate` cell with no SHA in it exits 0 with a notice, so `skipped`, `pending` or `n/a` is a one-word way past the arm — shorter than the deleted row the absent-row judgment was taken to close | `skills/code-review/scripts/chain_check.py:2922` | **fixed** `ebfdb2b` | fixed at ebfdb2b — above the cutoff a cell with no SHA-shaped word in it fails; the tail still grandfathers below it. Seven cells seen red at `GATE_FROM`, and the existing case moved to `GATE_FROM - 1` where its own subject lives. The absent-row judgment stands and its grounds are true now that the shorter way is closed; Executed over seven cells at `GATE_FROM`, all exit 0. `questions.md` assumption 3's reason is retroactive history, which the cutoff already excuses; above it `round_record.py new` writes the row and `close --broad-gate` writes the value |
| 🟡 3 | The gate SHA is tested only for the premature direction, so a resolvable commit that is neither the reviewed one nor a descendant of it passes with nothing printed | `skills/code-review/scripts/chain_check.py:2941` | **fixed** `ebfdb2b` | fixed at ebfdb2b — the passing condition is asked directly, `the gate ran at the reviewed commit or after it`, and a divergent SHA is reported with the commit named. Seen red first: exit 0 and no gate line at all. f356b75 then closed what the mutation sweep found — both passing cases asserted only an exit code, so the honest shape stayed green while the arm printed that it could not relate the two commits; Executed with a sibling-branch commit: exit 0, no gate line. `spec.md`'s three acceptance shapes do not include it, and an unresolvable SHA at least gets a *no claim* notice |
| 🟡 4 | The `unknown` state is parametrised over two shapes at the gate arm and four at the record arm; the two omitted are the two `phases/phase-1.md` names as dangerous | `tests/test_chain_check_at_the_pull_request.py:1478` | **fixed** `ebfdb2b` | fixed at ebfdb2b — one `UNKNOWN_SHAPES` list both arms parametrise over, so a third arm cannot get a third literal. Green when planted and shown red by mutating `strict` to read `unknown` as a draft, which is the inversion it exists to catch; Read. Both arms share one `strict` today, so a `pull_request_state` regression is still caught; what is unpinned is the arms diverging, which is what this branch just did to one of them |
| ⬜ 5 | `phases/phase-4.md` records the second red window's sentence as restored; the word `too` was dropped from it | `skills/code-review/orchestration.md:434` | answered | corrected at ebfdb2b. Dropping `too` is right — the word pointed at the first red window, which #296 closes — so it is an edit and not the restoration `phases/phase-4.md` called it. The record says which, and `test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits` now asserts the clause through its final word; it stopped short of where the word lived, which is why nothing caught it. Seen red by restoring `too` |
| 6 | #296 — the record-count arm reads the draft state, `unknown` reaches it as ready, the notice names `ready_for_review`, and nothing that can reach `main` is exempt | `skills/code-review/scripts/chain_check.py:3254` | answered | Read and executed. `strict = state != "draft"` is a comparison and not a truthiness test, `pull_request_state` drops every non-boolean to `unknown`, and the four-shape case at the record arm is green |
| 7 | The cutoff is the eighth of its shape, keyed `>=` on the work item id, and a work item whose id is not a unix second is grandfathered whole | `skills/code-review/scripts/chain_check.py:625` | answered | Read, and the three boundary cases are green: one second below is excused, at the cutoff is held, a non-date id is grandfathered |
| 8 | `Broad gate` and `not yet` have one definition, in the reader, and the writer imports both | `skills/code-review/scripts/round_record.py:329` | answered | Read. The case asserts the literal appears once in the reader and never in the writer, which an `is` comparison could not say |
| 9 | `close --broad-gate` replaces the row in place rather than appending a second one, and `field_index` refuses a record with none or two | `skills/code-review/scripts/round_record.py:2872` | answered | Read. A duplicated row would have been read as `not yet` by `field`, which returns the first match |
| 10 | The two row shapes coexist in one `survivors.md` and a path can never be read as a range | `skills/code-review/scripts/survivor_check.py:673` | answered | Read. `../notes.md` cannot match the pattern — the dots need a non-space word on both sides — and the parser tests the narrower shape first |

## Paste-ready fixes

```python
# A first cell naming a range rather than a path, which is what tells the two
# row shapes apart. A path cannot match it: the dots need a non-space word on
# BOTH sides, so `../notes.md` is a path and `A..B` is a range.
RANGE_CELL = re.compile(r"^[^\s|]+\.\.\.?[^\s|]+$")
# The work item a `survivors.md` belongs to, taken from the file's own path.
# A declaration is that work item's, and `whole_range` will not let it reach a
# range that work item did not write. Without this the row is not anchored at
# all: `hygiene.yml` hands every work item's file to every run, and the
# recommended spelling `origin/<base>...HEAD` RE-RESOLVES on each checkout, so
# one merged declaration matched -- and excused -- every later branch cut from
# the same base.
OWNER_DIR = re.compile(r"(?:^|.*/)(seal/specs/[^/]+)/[^/]+$")
```
```python
            if RANGE_CELL.match(first):
                if cells[1]:
                    # The file is carried so `whole_range` can ask whose
                    # declaration this is. A row with no work item directory
                    # above it -- an `--exempt` file passed from anywhere --
                    # keeps the old reach, because there is nothing to scope
                    # it to and refusing it would break running by hand.
                    ranges.append((first, cells[1], path))
                continue
```
```python
def whole_range(root, ranges, a, b):
    """The declared range covering this run, and the ones that do not resolve.

    Resolved rather than string-matched, because the two spellings of one
    range are both real: CI runs `origin/<base>...HEAD`, which is what a
    session copies into the declaration, and a person running it by hand
    types two oids. Comparing the text would refuse the same range for being
    spelled the other way.

    **Resolving is also why the range alone is not an anchor.**
    `origin/<base>...HEAD` is not a range, it is a RELATION, and it resolves
    to whatever range the checkout it is read on is over. `hygiene.yml` hands
    every `seal/specs/<id>/survivors.md` in the tree to every run, and a
    `survivors.md` lives until the release that ships it -- so one merged
    declaration in that spelling matched every later branch cut from the same
    base and excused its whole run. The second anchor is the work item: a
    declaration holds only over a range that touches the directory the
    declaration lives in, which is the work item that wrote it.

    **A spec that will not resolve is REPORTED, never exit 2**, and that is a
    landmine avoided rather than leniency. A `survivors.md` lives in the tree
    from the work item's first row until the release that ships it, and the
    refs its range names -- a release branch -- get deleted. Refusing the run
    then would turn every later range's check into exit 2 over a row that has
    nothing to do with it.
    """
    match, unresolved = None, []
    names = git(root, "diff", "--name-only", "-z", a, b)
    changed = [path for path in (names or "").split("\0") if path]
    for spec, grounds, source in ranges:
        owner = OWNER_DIR.match(source.replace("\\", "/"))
        if owner and not any(
            path.startswith(owner.group(1) + "/") for path in changed
        ):
            # Somebody else's work item. Not `unresolved`: the spec is fine
            # and the row is honest, it simply is not about this range.
            continue
        try:
            left, right = parse_range(root, spec)
        except Refused:
            unresolved.append((spec, grounds))
            continue
        if (left, right) == (a, b) and match is None:
            match = (spec, grounds)
    return match, unresolved
```
```python
    rows, ranges = reader.read_exemptions([str(table)])
    assert [where for where, _q, _g in rows] == ["seal/ledger.md"], (
        f"a range row was read as a per-survivor row, whose path cell it is not: {rows}"
    )
    assert ranges == [
        ("abc1234..def5678", "a documented deletion", str(table))
    ], ranges
```
```python
    elif not named:
        # NOT excused above the cutoff, and the tail of this function is what
        # excuses it below one. `questions.md` assumption 3 argued for
        # reporting an unparseable cell because records in the tree hold free
        # text -- true of records written before `GATE_FROM`, which the tail
        # already grandfathers. Above it there is no such history:
        # `round_record.py new` writes this row on every record it generates
        # and `close --broad-gate` is the only thing that changes the value,
        # so a cell this arm cannot parse is a cell somebody chose. Left as a
        # notice, `pending`, `skipped` or `n/a` was a shorter way past this
        # arm than deleting the row -- which is the very edit the absent-row
        # judgment above was taken to close.
        message = (
            f"`{BROAD_GATE}` is `{written}` — no SHA-shaped word in it, so "
            "this arm cannot tell a run that happened from one that did not. "
            "Write the SHA the one full-suite run happened at and the base "
            "it was compared against (`round_record.py close --broad-gate "
            f"'<sha> against <base>'`), or `{GATE_NOT_YET}` while it has "
            "not run"
        )
```
```python
def test_a_broad_gate_cell_nobody_can_parse_is_reported_below_the_cutoff(repo):
    """`questions.md` assumption 3, bounded by the cutoff it rests on.

    Nothing validates this cell where it is WRITTEN — that is Q4, and it is
    the owner's — so records written before `GATE_FROM` hold free text, and a
    real one in this tree reads `due after this record — see the row below`.
    Failing THOSE would be the retroactive red the cutoff exists to avoid.
    """
    gated(repo, GATE_FROM - 1, gate="due after this record — see the row below")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "Broad gate" in out, (
        "reported, which is the half that is not optional. A cell nobody can "
        "parse and a cell nobody wrote must not look the same"
    )


@pytest.mark.parametrize("cell", ["pending", "skipped", "n/a", "TBD", "-"])
def test_a_one_word_cell_is_not_a_way_past_the_arm(repo, cell):
    """Round 1's 🔴 2. The absent row fails and `not yet` fails; leaving one
    other word a notice made it the cheapest way past the arm there is —
    cheaper than deleting the row, which is the edit the absent-row judgment
    was taken to close. `skipped` is the word a session that skipped the run
    would write.

    Above the cutoff there is no free-text history to grandfather:
    `round_record.py new` writes the row and `close --broad-gate` writes the
    value, so this cell is a choice.
    """
    gated(repo, GATE_FROM, gate=cell)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "Broad gate" in out and cell in out, (
        "and it quotes the cell back, so nobody goes looking for a different row"
    )
```
```python
        else:
            # THE HONEST SHAPE, asked directly: the gate ran AT the commit the
            # round reviewed, or after it. Asked as the complement -- "is the
            # gate an ancestor of the target?" -- this answered the premature
            # case alone and let a commit on a DIVERGENT line through in
            # silence, which is quieter than the notice an unresolvable SHA
            # gets. `spec.md`'s three shapes are `not yet`, premature, and at
            # or after; a divergent commit is none of them.
            divergent = None
            for sha in SHA_RE.findall(field(rows, TARGET) or ""):
                reviewed = resolves_to(root, sha)
                if reviewed is None or reviewed == ran_at:
                    continue
                if is_ancestor(root, reviewed, ran_at):
                    continue
                if is_ancestor(root, ran_at, reviewed):
                    message = (
                        f"`{BROAD_GATE}` names `{named[0]}`, and this "
                        f"round's `{TARGET}` names `{sha}`, which descends "
                        "from it. The full-suite run was spent BEFORE the "
                        "round it was meant to seal, so everything the round "
                        "reviewed after that commit — its own fixes included "
                        "— went through no broad gate at all. A broad run "
                        "with an edit after it was spent, not banked. Run it "
                        "again now that the rounds have settled and write "
                        "the new SHA into the cell"
                    )
                    break
                divergent = sha
            else:
                if divergent is None:
                    return [], []
                fatal = False
                message = (
                    f"`{BROAD_GATE}` names `{named[0]}`, and this round's "
                    f"`{TARGET}` names `{divergent}` — the gate commit is "
                    "neither that commit nor a descendant of it, so it sits "
                    "on a different line of history and makes no claim "
                    "about this round. Reported rather than failed: a "
                    "divergent commit is not evidence either way"
                )
```
```python
def test_a_gate_sha_on_a_divergent_line_makes_no_claim_and_says_so(repo):
    """Round 1's 🟡 3. The arm asked `is the gate an ancestor of the target`,
    which is the premature direction, so everything that is NEITHER equal to
    the target nor descended from it passed — and passed in silence, which is
    quieter than the notice an unresolvable SHA already gets."""
    item = gated_item(GATE_FROM)
    write(repo, f"{item}/routing.md", declaration())
    first = commit(repo, "declare")
    subprocess.run(
        ["git", "-C", str(repo), "checkout", "-q", "-b", "side", first], check=True
    )
    write(repo, "side.py", "s = 1\n")
    side = commit(repo, "a commit on a line the branch never descended from")
    subprocess.run(["git", "-C", str(repo), "checkout", "-q", "feature"], check=True)
    write(repo, "another.py", "z = 3\n")
    second = commit(repo, "the commit the round reviewed")
    write(repo, f"{item}/rounds/round-1.md", gated_record(second, gate=side))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "different line of history" in out, (
        "a resolvable gate SHA the arm cannot relate to the target must not "
        "be quieter than one it cannot resolve at all"
    )
```
```python
# The four shapes of `unknown`, in one place because BOTH arms that `strict`
# excuses are held to them and a second literal is how they drift apart.
# `pull_request_state` has three answers, and `unknown` is judged as READY —
# otherwise `no pull-request context` becomes the quietest way past this
# check that exists. The string case is the one where a truthy read would
# have inverted the answer, and `"draft": "false"` inverting it is a defect
# this function has already had once.
UNKNOWN_SHAPES = [
    {},
    {"payload": "{not json"},
    {"payload": json.dumps({"repository": {}})},
    {"payload": json.dumps({"pull_request": {"draft": "true"}})},
]
UNKNOWN_IDS = ["no payload", "unparseable", "no pull request", "a string draft"]
```
```python
@pytest.mark.parametrize("kwargs", UNKNOWN_SHAPES, ids=UNKNOWN_IDS)
def test_an_unknown_state_is_held_to_the_broad_gate_too(repo, kwargs):
    """The same trap #296 opens, at the arm that would pay for it.

    If `unknown` were read as a draft, then `no pull-request context` would
    excuse the record's existence AND the broad gate AND the checked `Pass`
    all at once — which is the whole check. All four shapes, because the two
    arms share one `strict` today and that is exactly what stopped being
    true of the record arm this work item.
    """
    gated(repo, GATE_FROM, gate="not yet")
    code, out = run(repo, **kwargs)
    assert code == 1, out
    assert "Broad gate" in out
```
```
`nobody` on the last record — and that window is expected too.
```

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_chain_check_at_the_pull_request.py tests/test_a_corrected_sentence_survives_elsewhere.py -q`, in a clone of the worktree at `e26b5ed` | 118 passed |
| `pytest` over the eight modules the class fix touched, plus `tests/test_the_rules_have_one_owner.py` | 473 passed |
| `pytest` over the six remaining modules that reach `chain_check` with a generated or inherited record | 114 passed, 1 skipped |
| `pytest tests/test_no_real_identifiers.py tests/test_release_hygiene.py -q` | 34 passed |
| `evidence_check.py .` | 1017 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| Probe: work item A declares the whole range in the recommended spelling and is merged to the base; work item B branches off it and makes a real correction whose twin survives | B alone exit 1; B with A's row on `--exempt` **exit 0**, all survivors excused — 🔴 1 |
| Probe: seven `Broad gate` cells at `GATE_FROM`, at a ready pull request — `pending`, `n/a`, `TBD`, `not run`, `skipped`, `-`, `due later` | all **exit 0** — 🔴 2 |
| Probe: `Broad gate` naming a commit on a sibling branch, `Target SHA` naming the reviewed commit, ready | **exit 0** and no gate line printed — 🟡 3 |
| `git diff --stat origin/release/v0.9.5...e26b5ed` against the same range on the local ref | `docs/flow.md` is #293's, carried by `86dd599`, which `origin/release/v0.9.5` already holds — out of scope |
| Both probe files deleted; the clone is a `git clone --no-local` under the session scratchpad and nothing was written in the worktree except this report | confirmed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the `Broad gate` cell should be validated where it is WRITTEN | `questions.md` Q4, already open before this round | the repository owner. 🔴 2 does not wait on it — it is the reader's leniency above its own cutoff, not the writer's validation |
| The 1.6 similarity floor that #297's 153 survivors scored 1.60–1.62 against | `spec.md` §Scope, recorded as out | already deferred; not re-litigated here |
| Making the seal block's `broad gate:` line the source | `spec.md` §Scope, recorded as out | already deferred |
| The three arms running inside a real GitHub Actions pull-request event | `overview.md` §Not verified | the pull request's `release` leg. Unchanged by this round: what the probes exercise is the reading, not the workflow wiring |
| The full suite, the repository-wide lint and the typecheck | `agent-contract` §2 | the orchestrator, at the broad gate after the rounds settle |
