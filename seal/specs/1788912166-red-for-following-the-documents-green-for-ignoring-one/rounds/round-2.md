# 1788912166-red-for-following-the-documents-green-for-ignoring-one — review round 2

| Field | Value |
|---|---|
| Target SHA | 090bbd0 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #302 |
| Broad gate | 8abf13c against 86dd599 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of two arms that refused less than their own documents
said, on a branch whose own pull request is the first thing two of them judge.
It read the six fix commits, reverted each of the four fixes to watch its case
go red, and judged the two places the fix pass departed from the report's
paste-ready text.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A range declaration spelled `origin/<base>...HEAD` resolves to whatever range the current run is over, so one work item's row excuses every later work item on the same base and turns the step off | `skills/code-review/scripts/survivor_check.py:816` | answered | fixed at `7355201`, and confirmed by execution rather than by reading the fix pass's account. Both directions cased, both mutants killed: the refusal never firing turns the foreign-declaration case red, always firing turns the own-declaration case red. The `foreign` return is better than my paste-ready `continue` — `whole_range`'s only other refusal prints, and its stated reason binds symmetrically, so a silent ownership refusal would have been the one quiet path in a function whose design is that refusals are loud. Read at `report:911`: the `not yours` line prints independently of the exit code. The narrowing's performance claim is true — `git diff --name-only` is reached only after the range matches, `changed is None` is an identity test so an empty diff is cached, and the CI run on this branch hands over four exemption files and makes no `git diff` call. The docstring ranks the two reasons correctly: the primary one is that ownership asked of a non-matching row would print `not yours` beside rows the run has nothing to do with |
| 🔴 2 | Above the cutoff a `Broad gate` cell with no SHA in it exits 0 with a notice, so `skipped`, `pending` or `n/a` is a one-word way past the arm — shorter than the deleted row the absent-row judgment was taken to close | `skills/code-review/scripts/chain_check.py:2940` | answered | fixed at `ebfdb2b`. Seven cells fail at `GATE_FROM`, the free-text record prints at `GATE_FROM - 1`, and restoring `fatal = False` turns all seven red. The false grounds are recorded as false in three places rather than one — the arm's docstring, `phases/phase-2.md`, and the ledger's G2 row — which is the half a code-only correction leaves behind. Executed the one consequence that could reach elsewhere: notice → error over the thirteen other modules that read the row, 637 passed |
| 🟡 3 | The gate SHA is tested only for the premature direction, so a resolvable commit that is neither the reviewed one nor a descendant of it passes with nothing printed | `skills/code-review/scripts/chain_check.py:2970` | answered | fixed at `ebfdb2b`, closed at `f356b75`, and the hole between them measured at both commits. At `ebfdb2b` deleting the at-or-after pass leaves `test_a_broad_gate_taken_after_the_rounds_settled_passes` green — the mutant survives; at `f356b75` the same deletion turns it red. The general conclusion is true: once an arm gains a reporting state, the honest shape and the reporting shape both exit 0, so a case asserting only the exit code reads the arm saying it has no idea as a pass. Asserting the silence is the only assertion left that means anything |
| 🟡 4 | The `unknown` state is parametrised over two shapes at the gate arm and four at the record arm; the two omitted are the two `phases/phase-1.md` names as dangerous | `tests/test_chain_check_at_the_pull_request.py:1478` | answered | fixed at `ebfdb2b`. One `UNKNOWN_SHAPES` and one `UNKNOWN_IDS`, both arms parametrised over them, so a third arm cannot acquire a third literal without deleting the shared one. Read |
| ⬜ 5 | `phases/phase-4.md` records the second red window's sentence as restored verbatim; the word `too` was dropped from it | `skills/code-review/orchestration.md:435` | answered | corrected at `ebfdb2b`, and correcting the record rather than the document is the right half. The word pointed at the first red window and #296 closed it, so putting it back would restore a sentence referring to nothing. My finding was that the record called an edit a restoration, and `phases/phase-4.md` now says which it was. The clause is asserted through its final word and period. Read at `orchestration.md:435-437` and confirmed by the case passing |
| 🟡 6 | `OWNER_DIR` matches only a `survivors.md` directly under `seal/specs/<id>/`, so one directory deeper the row reads as belonging to no work item and silently keeps the unscoped reach 🔴 1 closed — with no `not yours` line, because ownership is never asked | `skills/code-review/scripts/survivor_check.py:689` | deferred #304 | **Deferred to #304**, which carries the paste-ready pattern fix and its case. CI cannot reach it — `hygiene.yml:229` globs one level — and a fix here would answer a finding inside the unit round 1's fix created, which `orchestration.md` refuses as depth 2. Executed against the compiled pattern: `seal/specs/A/rounds/survivors.md` and `seal/specs/A/notes/x/survivors.md` both read as owned by nobody, which routes them into the branch documented as *keeps the old reach* — the hatch meant for a file with no work item above it at all. The failure is silent and permissive, which is the pair the finding was about, and the function's own rule is true of a nested file; the pattern is what cannot see it. Answerable with grounds: `hygiene.yml:229` globs `seal/specs/*/survivors.md` alone, so only a by-hand run can reach it, and the fix pass's fourth mutation covered depth in the other direction. The same line also scopes a cross-repository `--exempt` path against this repository's changed paths |
| ⬜ 7 | `seal/follow-up.md`'s new row measures the second silencing path over `7355201..a18754c`, a fix-pass range nothing runs; at the range the gate runs, the exemption file changes nothing | `seal/follow-up.md:62` | answered | **Corrected in the row itself.** The eleven-to-one figure came from a range no gate runs; at `origin/release/v0.9.5...090bbd0`, which is what CI runs, there are 41 removed sentences and no survivors — with the exemption files, without `--exempt`, and with the file deleted from HEAD. The row now says so, and what a person weighs is the mechanism against an unmeasured reach. Executed at `origin/release/v0.9.5...090bbd0`, the range `hygiene.yml` passes: 41 sentences removed, 0 standing with the four exemption files and 0 with `--exempt` omitted. Then `survivors.md` deleted at HEAD in the clone so its text leaves the added side: still 0. The mechanism is real and the pass measured it; what is unmeasured is its reach at the gate, which is the number that decides urgency. Placement is right — `orchestration.md` §*A fix pass adds the unit that pins it* names a deferral with an answerer as the first of two homes, and the citation is accurate. The candidate repair is the one I would take: `survivor_check.py:64` already excludes everything under `rounds/` by construction, so this follows the module's own precedent. One correction to the row's reasoning — its objection, that a branch may edit prose in the same commit as its exemption file, does not apply to a candidate that excludes one filename rather than one commit |
| ⬜ 8 | Six `seal/ledger.md` rows were re-stamped, not four, and two carry no record of the re-read — one of them sharing its anchor and hash with a row that does | `seal/ledger.md` | answered | **Corrected at the commit carrying this record.** L5 takes the trace its sibling already carried — re-anchored, not re-verified, because a different sentence inside the same section moved. Two rows on one anchor no longer disagree about who read it. Read, and the hashes recomputed rather than trusted. `L5` (`agents/smith.md#"## Phases"`) and *A fix pass is obtained by resuming the implementing session* took a new hash with no note and an unmoved `Checked` date; four others carry *Re-read again 2026-09-09 … and the claim holds*. Both bare anchors genuinely changed content in this range — smith.md's section spans 27–278 and holds both smith.md edits, orchestration.md's spans 18–96 and holds the reworded paragraph at line 72. The second bare row cites the same anchor at the same hash as *The orchestrator is bound by the same contract*, which is noted, so the pair disagrees about whether anybody looked. Inside the keep-it-true exception on the axis that matters: no claim rewritten, no row re-pointed, every new hash the true one — `content_hash` over the three spans at `090bbd0` returns `94d1cef6`, `187a7304`, `67ff9cd3`, and `evidence_check.py .` reports 1023 ok · 0 drifted · 0 broken. The rider is clean and I withdraw the doubt: `region_hash` excludes rider comment blocks, and it returns exactly `7d41769f` at `090bbd0` and `466f9948` at `dc1326c` |
| ⬜ 9 | The fix pass appended its own account of the rename to round 1's report, above the marker that keeps the report parseable | `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/rounds/round-1-report.md:126` | answered | **Accepted rather than repaired.** The marker was required and the attribution is correct; the extra sentence is one line in the reviewer's own artifact and removing it now would be a second edit to that file for no reader's benefit. Recorded so the minimum-edit rule is not read as having been kept. Read. The `NAME NOT IN TREE` marker was required — the pass renamed the case my report named and the evidence checker reads every `.md` under a live work item — and it is correctly attributed, so that half is the keep-it-true exception reaching a report. The sentence after it is the fix pass's account in the reviewer's voice. True and attributed, but the minimal edit that keeps the tree green is the marker alone, and `round-1.md`'s fix table already carries the account. A report is the one artifact whose authority is the reviewer's, and the next round inherits it as one voice |
| ⬜ 10 | The new refusal for an unparseable `Broad gate` cell tells a person what to write, and nothing asserts that half | `skills/code-review/scripts/chain_check.py:2951` | deferred seal/follow-up.md | **Deferred to `seal/follow-up.md`** with the repository owner named. A case is mechanism a fix pass may not add after a run has ended, and a `# RIDER:` at the coordinate is refused by measurement — four ledger rows anchor at `#report_spawns` and two at `#analyse`. Read, and grepped: the message's own words appear nowhere in `tests/`. `test_a_one_word_cell_is_not_a_way_past_the_arm` asserts the exit code, the row label and the cell echoed back; `test_a_broad_gate_cell_nobody_can_parse_is_reported_below_the_cutoff` asserts the row label. Its sibling from the same commit, the divergent notice, is phrase-pinned on `different line of history`, which is the shape §14 asks for. Not a 🟡 and not a regression — the verdict is pinned seven ways and the text this replaced was unpinned too. One assertion short of the standard the same commit met one branch over |

## Paste-ready fixes

```python
# The work item a `survivors.md` belongs to, read off the file's own path. It
# is the declaration's SECOND anchor, and without it the row has effectively
# one that does not hold: `hygiene.yml` hands every `seal/specs/*/survivors.md`
# in the tree to every run, and the spelling this module recommends --
# `origin/<base>...HEAD` -- re-resolves on each checkout, so one merged row
# matched every later branch cut from the same base and excused its whole run.
#
# The tail is `.*` rather than one path segment on purpose. `hygiene.yml`
# globs the file directly under the work item, but a path handed in by hand
# can be nested -- and reading a nested one as owned by NOBODY sends it into
# the branch below that keeps the old unscoped reach, silently, which is the
# reach this pattern exists to close. The hatch is for a file with no work
# item above it at all; a file inside one is not that.
OWNER_DIR = re.compile(r"(?:^|.*/)(seal/specs/[^/]+)/.*[^/]$")
```
```python
        owner = OWNER_DIR.match(source.replace("\\", "/"))
        if owner is not None:
            if changed is None:
                names = git(root, "diff", "--name-only", "-z", a, b)
                if names is None:
                    # None is not "no files changed", and this module's own
                    # `git` returns it rather than "" for that reason (#111).
                    # Collapsing the two would refuse an honest declaration
                    # under a `not yours` line saying the range touches
                    # nothing in it, which would be false. The declaration is
                    # still refused -- the safe direction -- but say which.
                    raise Refused(
                        f"cannot diff {a[:7]}..{b[:7]} in {root}, so whose "
                        "declaration a range row is cannot be asked"
                    )
                changed = [path for path in names.split("\0") if path]
            if not any(path.startswith(owner.group(1) + "/") for path in changed):
                foreign.append((spec, grounds, owner.group(1)))
                continue
```
```python
def test_a_declaration_nested_under_its_work_item_is_still_that_work_items(
    tmp_path,
):
    """🟡 6 of round 2. `OWNER_DIR`'s tail read one path segment, so a
    `survivors.md` one directory deeper matched nothing and fell into the
    branch that keeps the OLD unscoped reach -- the hatch meant for a file
    with no work item above it at all. Silent and permissive, which is the
    pair round 1's 🔴 1 was about."""
    repo = tmp_path / "probe"
    base_and_item_a(repo)
    probe_git(repo, "switch", "-q", "release")
    probe_git(repo, "merge", "-q", "--ff-only", "work-item-a")
    probe_git(repo, "fetch", "-q", "origin")
    probe_git(repo, "switch", "-qc", "work-item-b", "release")
    fixed = (
        "The exemption row is anchored by the work item and the checker "
        "leaves that reach untouched afterwards."
    )
    build(
        repo,
        {"b-notes.md": f"# b\n\nFirst. {fixed}\n\nSecond. {CLAIM_B}\n"},
        "work item B corrects its claim and declares nothing",
    )
    nested = os.path.join(str(repo), ITEM_A, "rounds", "survivors.md")
    os.makedirs(os.path.dirname(nested), exist_ok=True)
    with open(declaration_of_a(repo), encoding="utf-8") as handle:
        row = handle.read()
    with open(nested, "w", encoding="utf-8") as handle:
        handle.write(row)
    code, text = run(
        "--range", "origin/release...HEAD", "--root", str(repo), "--exempt", nested
    )
    assert code == 1, (
        "a declaration one directory deeper read as belonging to nobody and "
        f"excused work item B's whole run\n{text}"
    )
    assert "1799000001-work-item-a" in text, (
        f"the refused declaration is not printed with its work item\n{text}"
    )
```
```python
@pytest.mark.parametrize("cell", ["pending", "skipped", "n/a", "TBD", "-"])
def test_a_one_word_cell_is_not_a_way_past_the_arm(repo, cell):
    """Round 1's 🔴 2. The absent row fails and `not yet` fails; leaving one
    other word a notice made it the cheapest way past the arm there is --
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
    # Round 2's ⬜ 10, and §14's other half. The verdict was pinned seven ways
    # and the sentence telling a person what to DO about it was pinned
    # nowhere, where the divergent notice from the same commit is pinned on
    # its own words. A refusal that stops naming the way out is a refusal
    # somebody argues with instead of acting on.
    assert "--broad-gate" in out and GATE_NOT_YET in out, (
        "the refusal no longer names the two things a person may write, so "
        f"the arm refuses without saying what would satisfy it: {out}"
    )
```

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_chain_check_at_the_pull_request.py tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_the_rules_have_one_owner.py -q`, in a `git clone --no-local` under the session scratchpad at `090bbd0` | 172 passed |
| `pytest` over the thirteen other modules that read the `Broad gate` row — the surface the notice → error change could reach | 637 passed |
| Five mutations, one at a time, each reverted and the file compared byte-for-byte afterwards: ownership refusal never firing · always firing · `fatal = False` restored to the unparseable arm · the at-or-after pass deleted · the divergent branch returning in silence | all five **killed** — the case each fix was planted for goes red |
| The same at-or-after deletion at `ebfdb2b` and at `f356b75`, the commit the mutation sweep produced | at `ebfdb2b` the mutant **survives** (`test_a_broad_gate_taken_after_the_rounds_settled_passes` stays green); at `f356b75` it is killed. The hole was real and `f356b75` closed it |
| `survivor_check.py --range origin/release/v0.9.5...HEAD` with every `seal/specs/*/survivors.md` globbed into `--exempt`, as `hygiene.yml:229` builds it | exit 0 · 41 sentences removed · **0 standing**. No `git diff --name-only` call made — no declaration resolves onto that range |
| The same range with `--exempt` omitted entirely | exit 0 · **0 standing** — identical, so the exemption file silences nothing at the gate's range |
| `survivors.md` deleted at HEAD in the clone so its text leaves the added side of the range, then the same range again | exit 0 · **0 standing** — ⬜ 7 |
| `survivor_check.py --range 7355201..a18754c` with no `--exempt`, the range the follow-up row measures | 1 place standing, at `survivor_check.py:713` — the fix pass's number reproduces |
| `OWNER_DIR` evaluated over seven `--exempt` path shapes | `seal/specs/A/rounds/survivors.md` and `seal/specs/A/notes/x/survivors.md` read as owned by nobody; `/other/repo/seal/specs/A/survivors.md` reads as `seal/specs/A` — 🟡 6 |
| `evidence_check.py .` | 1023 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 refused, 106 names read |
| `content_hash` recomputed over the three re-stamped anchors' spans at `090bbd0` | `94d1cef6`, `187a7304`, `67ff9cd3` — the values the rows carry |
| `rider_check.py`'s `region_hash` over `agents/smith.md#"## Phases"` at `dc1326c`, `808804b` and `090bbd0` | `466f9948`, `7d41769f`, `7d41769f` — the stamp is right at both ends, and the two hashers differ by design |
| `chain_check.py --baseline origin/release/v0.9.5` with no event payload, so the state reads as ready | exit 1 on `round-1.md` for `Broad gate` = `not yet` and for `Pass` beside `Fixes checked by: nobody`. Both honest, both excused while #302 is a draft, and the second names a verifying round as the way out — which is this round. The arm is live on the branch that wrote it |
| `grep` for the new refusal's own words across `tests/` and `skills/` | found only in `chain_check.py` itself — ⬜ 10 |
| Every probe script deleted; the clone is a `git clone --no-local` under the session scratchpad, clean at `090bbd0`; nothing written in the worktree except this report | confirmed — `git status --short` empty in both |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:772` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:2922` | round 1's 🔴 2 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:2941` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_chain_check_at_the_pull_request.py:1478` | round 1's 🟡 4 — fixed |
| round-1 | `skills/code-review/orchestration.md:434` | round 1's ⬜ 5 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py:3254` | round 1's 6 — answered |
| round-1 | `skills/code-review/scripts/chain_check.py:625` | round 1's 7 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:329` | round 1's 8 — answered |
| round-1 | `skills/code-review/scripts/round_record.py:2872` | round 1's 9 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:673` | round 1's 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Writing a `survivors.md` row silences its survivor a second way, through the added side of the range, and that way has no anchor to degrade | `seal/follow-up.md`, written by the fix pass with the owner named | the repository owner. Placement confirmed this round, with one correction to the row's reasoning and one measurement it lacks — ⬜ 7 |
| Whether the `Broad gate` cell should be validated where it is written | `questions.md` Q4, open before round 1 | the repository owner. Unchanged by this round |
| The 1.6 similarity floor that #297's 153 survivors scored 1.60–1.62 against | `spec.md` §Scope, recorded as out | already deferred; not re-litigated |
| Making the seal block's `broad gate:` line the source | `spec.md` §Scope, recorded as out | already deferred |
| The three arms running inside a real GitHub Actions pull-request event | `overview.md` §Not verified | the pull request's `release` leg. Unchanged — what the probes exercise is the reading, not the workflow wiring |
| The full suite, the repository-wide lint and the typecheck | `agent-contract` §2 | the orchestrator. **Now due**: nothing this round opened needs a fix, so the rounds have settled and the broad run is the next step |
