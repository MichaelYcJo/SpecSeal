# 1788912166-red-for-following-the-documents-green-for-ignoring-one — review round 1 report

The first review of three checks that judge pull requests, on a branch whose
own pull request is the first thing two of them judge. What was asked is
whether each arm refuses exactly what its document says it refuses, and
whether the two judgments taken beyond the specification's letter are the
right ones.

Nothing was inherited: `rounds/` was empty, so every coordinate below was
derived this round.

**Review scope correction, first, because it changes what the diff is.** The
prompt names the base as `release/v0.9.5`, and the local ref of that name is
at `157f57c`. `origin/release/v0.9.5` is at `86dd599` and already carries
#293's `docs/flow.md` work, so `git diff release/v0.9.5...e26b5ed` shows 170
lines of `docs/flow.md` that are not this branch's. Read against
`origin/release/v0.9.5`, `docs/flow.md` is untouched — which is what
`routing.md` says. Twenty-nine files, and the three scripts are
`chain_check.py`, `round_record.py` and `survivor_check.py`.

## The shape of what was found

Two of the three arms refuse less than their documents say they refuse, and
both do it the same way: the arm's stated bound is written as a property of
something that is not actually pinned.

- **#297's arm** says the range is the anchor. The range it compares is
  resolved at check time, so the spelling the documentation recommends is not
  an anchor at all and one work item's declaration turns the check off for
  every later work item on the same base.
- **#295's arm** was given a judgment defending the refusal of an absent row,
  on the grounds that otherwise deleting one line is the way past the arm.
  Writing one word is a shorter way past it, and that way is open.
- The remaining two are narrower: the gate SHA comparison is written as its
  own complement, so a third state passes in silence; and the `unknown` pin
  the spawn prompt asked me to open first is four shapes at one arm and two
  at the other.

#296 — the arm the whole branch is named for — is correct. I found nothing
against it.

## 🔴 1 · one work item's range declaration turns the survivor check off for every later work item on the same base

`skills/code-review/scripts/survivor_check.py:772` (`whole_range`), with
`.github/workflows/hygiene.yml:229`.

**Executed.** A fixture repository with a base branch, work item A's
`survivors.md` declaring the whole range and merged into the base, and work
item B branched off that base making a real correction whose twin sentence
survives. B alone exits 1. B with A's declaration on `--exempt` exits 0, every
survivor excused.

The workflow loops **every** `seal/specs/<id>/survivors.md` in the tree into
`--exempt`, and runs the check over `origin/<base_ref>...HEAD`. `whole_range`
resolves each declared spec on the checkout it is running on and matches when
the two endpoints equal the run's. So a spec spelled `origin/<base>...HEAD`
resolves, on any branch cut from that base, to exactly that branch's own
range. It matches. Every survivor is excused. The step exits 0 and the check
is off.

That spelling is not an accident of the fixture — it is the one the change
recommends. The module docstring's worked example is
`| origin/release/vX.Y.Z...HEAD | … |`, `agents/smith.md` and
`skills/code-review/orchestration.md` both carry the row's shape, and
`test_a_whole_range_row_is_resolved_rather_than_string_matched`'s own
docstring says *"In CI the range is `origin/<base>...HEAD`, and that is the
spelling a smith copies into the declaration."*

**Why it matters beyond one branch.** A `survivors.md` lives in the tree from
the work item's first row until the release that ships it, so the row outlives
its own work item by a whole release cycle, and during that cycle it is handed
to every other work item's check. The one row #297 exists to make cheap to
write is also the row that disables the step for everybody else in the
release. That is the outcome the escape was designed to prevent, arriving
through the escape.

**And the stated bound is false as written.** `phases/phase-3.md`, the module
docstring and `agents/smith.md` all say the row *"stops holding the moment the
check runs over a different range, so a declaration cannot outlive the
deletion it was written for."* `origin/<base>...HEAD` is not a range; it is a
relation that re-resolves per checkout, so the row holds over every range that
relation names — later commits on its own branch included.

`test_a_whole_range_row_does_not_reach_a_different_range` does not reach this.
It declares `HEAD..HEAD` against a run over `HEAD^..HEAD` on one checkout, so
what it varies is the spec's text and never the checkout the spec resolves on.
An elastic spec is identical to itself under that case.

The fix has to make the row belong to the work item that wrote it. The
declaration's file already says which work item that is — it is the directory
it sits in — and the run's own range already says which work item wrote it.
Paste-ready fix below.

## 🔴 2 · the `Broad gate` arm is bypassed by one word, which is cheaper than the deletion the absent-row judgment was taken to close

`skills/code-review/scripts/chain_check.py:2922–2923` (`broad_gate`, the
`elif not named:` branch).

**Executed**, at a ready pull request with the work item id equal to
`GATE_FROM`. Every one of these cells exits 0 with a notice: `pending`,
`n/a`, `TBD`, `not run`, `skipped`, `-`, `due later`. An absent row exits 1.
`not yet` exits 1.

So the three states the arm tells apart are really four, and the fourth is
open. `skipped` is not an exotic value — it is the word a session that skipped
the run would write.

**This is the judgment I was asked to weigh, and my answer is split.**
Refusing an absent row is right and should stand: the cell's question is *did
the run happen*, and no row answers it the way `not yet` does. What is wrong
is the grounds `overview.md` gives for it — *"reading it as nothing to check
would make deleting one line the way past the whole arm."* Deleting one line
is not the way past the arm, because a shorter way is already open. The
absent-row refusal closes a door beside an open one.

**The lenient path's own reason does not survive the cutoff.** `questions.md`
assumption 3 defends reporting an unparseable cell rather than failing it,
because *"no code validates the cell today, so records in the tree may hold
anything"* and failing would be *"the retroactive red the cutoff exists to
avoid."* The cutoff already answers that: everything below `GATE_FROM` is
excused by the tail of this very function, and there is no free-text history
above it — `round_record.py new` writes the row on every record it generates,
and `close --broad-gate` is the only thing that changes the value. Above the
cutoff a cell this arm cannot parse is a cell somebody chose.

`test_a_broad_gate_cell_nobody_can_parse_is_reported_rather_than_failed`
(`tests/test_chain_check_at_the_pull_request.py:1535`) runs at `GATE_FROM` and
asserts exit 0, so the case pins the bypass at the one id where the arm is
supposed to apply. Its real subject — the record in this tree reading *"due
after this record — see the row below"* — is a record from below the cutoff,
which is where the case belongs.

This is adjacent to `questions.md` Q4 and is not Q4. Q4 asks whether the cell
should be validated where it is **written**, and it is the owner's. This asks
whether the **reader** should be lenient above its own cutoff, which is this
branch's arm and this branch's question.

## 🟡 3 · the gate SHA comparison is written as its own complement, so a third state passes in silence

`skills/code-review/scripts/chain_check.py:2941–2945` (`broad_gate`).

**Executed.** A record whose `Target SHA` names the commit the round reviewed
and whose `Broad gate` names a commit on a sibling branch — resolvable, and
neither the reviewed commit nor a descendant of it — exits 0, and the arm
prints nothing about the gate at all.

The loop asks one question, `is_ancestor(ran_at, reviewed)`, which is the
premature direction. The honest passing shape is the other one: the gate ran
at the reviewed commit or after it. Written as the complement of *premature*,
the condition admits everything that is neither — a commit on a divergent
line, a commit from another branch, a commit from a base the branch never
descended from.

`spec.md`'s acceptance rows name three shapes: `not yet` fails, a SHA the
`Target SHA` descends from fails, a SHA at or after it passes. A divergent SHA
is none of the three. What makes it worth a fix rather than a note is the
comparison: an unresolvable SHA gets a printed *no claim* notice, and a
resolvable-but-unrelated one gets silence — the arm is quieter about the case
where the cell asserts something it can check than about the case where it
cannot.

Asking the honest question directly answers all three states in one
condition, which is also the shallower fix: no special case is added, one
comparison is turned round.

## 🟡 4 · the `unknown` pin is four shapes at one arm and two at the other, and the handoff says four at both

`tests/test_chain_check_at_the_pull_request.py:1478`.

**Read.** The handoff states that `unknown` is *"pinned at both arms by a
parametrised case over four `unknown` shapes."* At the record-count arm that
is exact: `test_an_unknown_state_is_not_a_draft_at_this_arm_either`
parametrises no payload, an unparseable payload, one naming no pull request,
and one whose `draft` is the string `"true"`, with ids for each. At the gate
arm, `test_an_unknown_state_is_held_to_the_broad_gate_too` parametrises two —
no payload and an unparseable payload.

The two that are missing are the two the branch's own record calls the
dangerous ones. `phases/phase-1.md` names the string case as *"the one where a
truthy read would have inverted the answer"* and records that `"draft":
"false"` inverting it *"is a defect this function has already had once."*

It is 🟡 and not 🔴 because both arms consume one `strict`, so a regression in
`pull_request_state` would still turn the record arm red. What the thin
parametrisation costs is the case where the arms stop sharing that value —
which is exactly what #296 did to the record arm this round, a hundred lines
from the arm that already had it.

The fix is one shared list rather than a second literal, which is also what
keeps the next arm from getting a third.

## ⬜ 5 · a phase record says a sentence was restored, and one word of it is gone

`skills/code-review/orchestration.md:434`.

**Read.** `phases/phase-4.md` records that the second red window's sentence
*"was reworded by accident and put back … the original phrasing is restored
rather than the case updated."* The sentence now ends *"and that window is
expected."* It ended *"and that window is expected too."*

Dropping `too` is very likely right — it pointed at the first window, and
#296 closed that one — but then it is a deliberate edit and not a
restoration, and the record says restoration.
`test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits`
asserts only the clause before it, so nothing pins either reading.

No release ships a defect for this, which is why it is ⬜ and not counted in
`Needs a fix`.

## The second judgment, weighed

**An unresolvable range declaration is reported and never fatal — right, and
for a stronger reason than the one recorded.** `overview.md` and
`phases/phase-3.md` justify it by the release branch a `survivors.md` names
getting deleted. The sharper reason is the same glob that produces 🔴 1: every
work item's file is handed to every run, so one rotted row would refuse every
unrelated work item's check. Exit 2 there would be a landmine with a much
wider blast radius than the record claims.
`test_a_range_row_that_does_not_resolve_silences_nothing_and_says_so` pins it
and prints the spec, which is the loud direction. Confirmed.

## The class, enumerated by construction

**The class asked for: every case that puts an above-cutoff round record in
front of a ready `chain_check`.** Taken by construction rather than by grep of
literals — every module that reaches `chain_check` at all, crossed with every
work-item id it builds a record under:

| Module reaching `chain_check` | Above-cutoff id | State |
|---|---|---|
| `tests/test_a_record_precedes_the_fixes_it_commissions.py` | `1799000000` | row added |
| `tests/test_a_record_says_what_ran_it.py` | `1799000000` | row added |
| `tests/test_the_fixes_name_their_surface.py` | `1799000000` | row added |
| `tests/test_the_last_rounds_fixes_are_checked.py` | `1799000000` | row added |
| `tests/test_the_record_is_generated.py` | `1799000000` | row added |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` | `1799000000` | row added |
| `tests/test_the_fixes_close_the_record.py` | inherited, generated | `--broad-gate` passed |
| `tests/test_the_reviewers_report_reaches_the_record.py` | inherited, generated | untouched, green |
| `tests/test_chain_check_at_the_pull_request.py` | `GATE_FROM` | the new cases |

**The enumeration is complete and the seventh member the phase record found by
failure is the only one there was.** No test derives a work-item id from the
clock, so nothing here becomes above-cutoff with the passage of time, which is
the shape that would have made the class unbounded. Every other module
reaching `chain_check` builds records under ids below the cutoff
(`1780000000`, `1787700000`, `1788184145`, `1788354065`, `1788411058`,
`1788597029`, `1788597030`, `1788817289`). All fifteen modules run green —
587 passed, 1 skipped, executed.

## What the handoff claimed, and what the code said

| Claim | Verdict |
|---|---|
| `chain_check.py` had no occurrence of `broad` at the base | confirmed by reading the base file; the constants now live in the reader and `round_record.py` imports both |
| 14 mutations killed, both files restored byte-for-byte | **unverified by me.** The mutation script is not in the tree and I did not re-run the sweep. The orchestrator answers, or it stands as the smith's executed claim |
| The `Broad gate` arm turned 43 cases red; six modules by static enumeration, a seventh from the generator | confirmed by construction — the class is nine members and the seventh is the generated one |
| An absent `Broad gate` row fails | **right, and its stated grounds are false** — see 🔴 2 |
| An unresolvable range declaration is reported, never fatal | right, and for a stronger reason — see above |
| `GATE_FROM` is this work item's own id, cutoff `>=`, so this pull request is the first the arm applies to | confirmed by reading and by the two cutoff cases; and it means the last record of this run needs a real broad-gate SHA before the draft goes ready |
| `unknown` pinned at both arms over four shapes | **not what the code says** — see 🟡 4 |
| The eleven `seal/ledger.md` rows are re-stamps, not appends | confirmed. Eleven added lines, eleven re-read notes, hashes changed and `Checked` dates unchanged — `--reverify` rewrites hashes only, so this is the tool's behaviour and not a choice this branch made |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A range declaration spelled `origin/<base>...HEAD` resolves to whatever range the current run is over, so one work item's row excuses every later work item on the same base and turns the step off | `skills/code-review/scripts/survivor_check.py:772` | open | Executed: work item B exits 1 alone and 0 with work item A's row on `--exempt`. `hygiene.yml:229` globs every work item's file into `--exempt`; the recommended spelling is the module docstring's own example. The stated bound — the row cannot outlive the deletion it was written for — does not hold for it |
| 🔴 2 | Above the cutoff a `Broad gate` cell with no SHA in it exits 0 with a notice, so `skipped`, `pending` or `n/a` is a one-word way past the arm — shorter than the deleted row the absent-row judgment was taken to close | `skills/code-review/scripts/chain_check.py:2922` | open | Executed over seven cells at `GATE_FROM`, all exit 0. `questions.md` assumption 3's reason is retroactive history, which the cutoff already excuses; above it `round_record.py new` writes the row and `close --broad-gate` writes the value |
| 🟡 3 | The gate SHA is tested only for the premature direction, so a resolvable commit that is neither the reviewed one nor a descendant of it passes with nothing printed | `skills/code-review/scripts/chain_check.py:2941` | open | Executed with a sibling-branch commit: exit 0, no gate line. `spec.md`'s three acceptance shapes do not include it, and an unresolvable SHA at least gets a *no claim* notice |
| 🟡 4 | The `unknown` state is parametrised over two shapes at the gate arm and four at the record arm; the two omitted are the two `phases/phase-1.md` names as dangerous | `tests/test_chain_check_at_the_pull_request.py:1478` | open | Read. Both arms share one `strict` today, so a `pull_request_state` regression is still caught; what is unpinned is the arms diverging, which is what this branch just did to one of them |
| ⬜ 5 | `phases/phase-4.md` records the second red window's sentence as restored; the word `too` was dropped from it | `skills/code-review/orchestration.md:434` | open | Read. Probably the right edit, but then it is an edit and not a restoration, and no case pins either reading |
| 🟢 | #296 — the record-count arm reads the draft state, `unknown` reaches it as ready, the notice names `ready_for_review`, and nothing that can reach `main` is exempt | `skills/code-review/scripts/chain_check.py:3254` | answered | Read and executed. `strict = state != "draft"` is a comparison and not a truthiness test, `pull_request_state` drops every non-boolean to `unknown`, and the four-shape case at the record arm is green |
| 🟢 | The cutoff is the eighth of its shape, keyed `>=` on the work item id, and a work item whose id is not a unix second is grandfathered whole | `skills/code-review/scripts/chain_check.py:625` | answered | Read, and the three boundary cases are green: one second below is excused, at the cutoff is held, a non-date id is grandfathered |
| 🟢 | `Broad gate` and `not yet` have one definition, in the reader, and the writer imports both | `skills/code-review/scripts/round_record.py:329` | answered | Read. The case asserts the literal appears once in the reader and never in the writer, which an `is` comparison could not say |
| 🟢 | `close --broad-gate` replaces the row in place rather than appending a second one, and `field_index` refuses a record with none or two | `skills/code-review/scripts/round_record.py:2872` | answered | Read. A duplicated row would have been read as `not yet` by `field`, which returns the first match |
| 🟢 | The two row shapes coexist in one `survivors.md` and a path can never be read as a range | `skills/code-review/scripts/survivor_check.py:673` | answered | Read. `../notes.md` cannot match the pattern — the dots need a non-space word on both sides — and the parser tests the narrower shape first |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the `Broad gate` cell should be validated where it is WRITTEN | `questions.md` Q4, already open before this round | the repository owner. 🔴 2 does not wait on it — it is the reader's leniency above its own cutoff, not the writer's validation |
| The 1.6 similarity floor that #297's 153 survivors scored 1.60–1.62 against | `spec.md` §Scope, recorded as out | already deferred; not re-litigated here |
| Making the seal block's `broad gate:` line the source | `spec.md` §Scope, recorded as out | already deferred |
| The three arms running inside a real GitHub Actions pull-request event | `overview.md` §Not verified | the pull request's `release` leg. Unchanged by this round: what the probes exercise is the reading, not the workflow wiring |
| The full suite, the repository-wide lint and the typecheck | `agent-contract` §2 | the orchestrator, at the broad gate after the rounds settle |

## Paste-ready fixes

🔴 1 — make a range declaration belong to the work item that wrote it. Three
edits in `skills/code-review/scripts/survivor_check.py`, and the row's file
path is the only new input.

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

🔴 1 also changes what `read_exemptions` returns, so its one existing
parser-level case has to name the third element:

```python
    rows, ranges = reader.read_exemptions([str(table)])
    assert [where for where, _q, _g in rows] == ["seal/ledger.md"], (
        f"a range row was read as a per-survivor row, whose path cell it is not: {rows}"
    )
    assert ranges == [
        ("abc1234..def5678", "a documented deletion", str(table))
    ], ranges
```

🔴 2 — scope the lenient path by the cutoff the arm already has. The tail of
`broad_gate` already downgrades a fatal message to a notice below `GATE_FROM`,
so the fix is to stop opting out of it: delete `fatal = False` and say what to
write instead.

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

🔴 2 moves the existing case below the cutoff, which is where its own subject
lives, and adds the one above it:

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

🟡 3 — ask the honest question instead of its complement. Replace the `for` /
`else` block that begins at `for sha in SHA_RE.findall(field(rows, TARGET)`:

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

🟡 4 — one list, so a third arm cannot get a third literal:

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

⬜ 5 — restore the word, or record the edit. If the sentence is meant as it
now stands, `phases/phase-4.md`'s *"the original phrasing is restored"* is the
line to change instead.

```
`nobody` on the last record — and that window is expected too.
```

## Regression tests to plant

Every case above names its destination file in the fix it belongs to. In one
place:

- `tests/test_a_corrected_sentence_survives_elsewhere.py` — the amended
  parser assertion for 🔴 1, and a new case building two work items on one
  base and asserting that the first's declaration does not reach the second's
  range. §15: run it against `e26b5ed` first and see it green-for-the-wrong-
  reason, then against the fix.
- `tests/test_chain_check_at_the_pull_request.py` — 🔴 2's two cases, 🟡 3's
  case, and 🟡 4's shared list. The renamed case for 🔴 2 must be seen red
  against `e26b5ed` before it is committed; the seven cells in this round's
  probe are what it is built from.

## Facts for the evidence ledger

Rows for this work item's own fragment, once the fixes land — each is a claim
this round established by execution and none of them is in the fragment now:

- A whole-range declaration is anchored on **two** things, the range and the
  work item directory it lives in, because the range spelling CI uses
  re-resolves per checkout. Grounds: the new case, and `hygiene.yml:229`.
- Above `GATE_FROM` a `Broad gate` cell with no SHA in it is refused, and the
  lenient path is the grandfathering below the cutoff. Grounds: the two cases
  replacing the one at `tests/test_chain_check_at_the_pull_request.py:1535`.
- The gate SHA is admitted only when it is the reviewed commit or a
  descendant of it; everything else that resolves is reported. Grounds: the
  divergent-line case.

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the orchestrator, at the broad gate after the rounds settle — `agent-contract` §2, and §3 refuses a prompt that widens it. Nothing in this round's prompt did |
| The 14-mutation sweep the handoff reports | the smith's executed claim, or the orchestrator. The script is not in the tree and I did not reconstruct it |
| The three arms inside a real pull-request event rather than against a written `event.json` | the pull request's `release` leg. The probes exercise the reading off disk, which is what the cases already do; the workflow wiring is unproven either way |
| Whether `questions.md` Q4 should be answered before this ships | the repository owner. 🔴 2 does not wait on it |

**The broad gate has not come due.** This round leaves three findings that
need a fix, so the one full-suite run is not the next step. When a later round
leaves nothing open, the arm this branch added applies to this branch's own
pull request: `GATE_FROM` is this work item's id and the cutoff is `>=`, so
the last round record's `Broad gate` cell needs the SHA of that run and the
base it was compared against before the draft goes ready. Broad gate state
carried into this round's record: **not yet**.

Needs a fix: yes — 🔴 1, 🔴 2 and 🟡 3 (🟡 4 is a thin pin the smith may answer
with grounds; ⬜ 5 is a correction and is not counted)
Loses a record or crashes: no

## Proof

Files opened this round, and nothing recorded as passing that was not run.

**Read** — `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/`:
`spec.md`, `plan.md`, `overview.md`, `questions.md`, `routing.md`,
`changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`,
`phases/phase-4.md`; `seal/ledger/1788912166-red-for-following-the-documents-green-for-ignoring-one.md`;
`seal/ledger.md` (the diff alone); `seal/config.md`;
`skills/code-review/scripts/chain_check.py` (`broad_gate`,
`says_gate_not_yet`, `pull_request_state`, `field`, `item_began`,
`resolves_to`, `is_ancestor`, the constant block, `main`'s declaration walk);
`skills/code-review/scripts/round_record.py` (the constant block, `close`,
`field_index`, the argument parser);
`skills/code-review/scripts/survivor_check.py` (the module docstring,
`read_exemptions`, `whole_range`, `report`, `main`, `parse_range`,
`corrected`); `skills/code-review/orchestration.md`;
`docs/review-handoff-protocol.md`; `templates/sdd-round.md`; `agents/smith.md`;
`.github/workflows/hygiene.yml`; `bin/test`; `CONTRIBUTING.md` (the runner
line); `tests/test_chain_check_at_the_pull_request.py`;
`tests/test_a_corrected_sentence_survives_elsewhere.py`;
`tests/test_the_rules_have_one_owner.py`; the seven fixture modules' diffs;
`seal/specs/1788904490-every-published-reading-carries-three-wrong-rows/survivors.md`.

**Executed** — every row of the *Executed probes* table above, in a
`git clone --no-local` of the worktree at `e26b5ed`, with a `uv`-built
virtualenv inside the clone. Both probe files were deleted before this report
was written. Nothing was written in the worktree except this file, and it is
not committed.

**Unverified** — the four rows of *Not verified* above, each with its
answerer.
