# 1789956662-the-gate-and-ci-ask-about-different-ranges — review round 1

| Field | Value |
|---|---|
| Target SHA | 327ef1f7e2b346569dda59004641ab11b7187e48 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 459 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `9a6d4a35d242e2bc1aafbdafc4eeab1293a08d6c..da11718489a7a8c2fb4a6d651e047168c6d20693`, 12 commits |
| Contract changes | behind_clone → pytest only |
| New units | PANEL_VALUE_WIDTH (depth 1); ELISION (depth 1); names_a_branch (depth 1); BASE_ENVIRONMENT (depth 1); SHELL_VARIABLE (depth 1); base_spellings (depth 1); a_clone_tracking_a_second_remote (depth 1); test_the_line_does_not_claim_ci_reads_a_second_remote (depth 1); test_the_line_still_speaks_for_ci_where_the_two_agree (depth 1); test_the_distance_says_what_it_is_measured_against (depth 1); test_a_revision_that_is_not_a_branch_does_not_take_a_branchs_upstream (depth 1); test_a_bare_sha_does_not_take_a_branchs_upstream (depth 1); WORKFLOW_SHAPES (depth 1); test_the_workflow_reader_sees_every_shape_a_base_is_spelled_in (depth 1); test_the_workflow_reader_finds_the_env_assignment_the_file_already_has (depth 1); STAMP (depth 1); stamp_module (depth 1); panel_of (depth 1); test_the_panel_value_width_is_what_the_stamp_actually_gives (depth 1); test_a_ref_too_long_for_the_panel_says_it_was_cut (depth 1); test_a_ref_that_fits_is_left_exactly_as_it_is (depth 1) |
| Needs a fix | yes — findings 1, 2, 3, 4 and 5 (6 and 7 are ⬜, and 8 is a correction in the run's own paperwork, so none of the three counts) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first round of the work item: the whole branch against its own
frame, spec compliance before quality. The reviewer was given the target SHA,
the base, and the six divergences the builder had declared in `overview.md` —
the seventh read of `args.base`, A3 not holding whole because the `Broad gate`
cell's base half moved, W1 answered more narrowly than its default, the
moved-line's second filling, the document pin that could not fail for one of
three files, and four re-verified rows of the shared ledger. A declared
divergence is still a divergence, so each was named as something to judge
rather than to accept, and the ledger rows were asked for on the claim rather
than on the hash.

Four things were asked on the reviewer's own account rather than because the
builder raised them: whether the resolution order can pick a ref CI would not
read; whether the fallback really leaves a remote-less repository untouched in
every arm and not only in the ones with cases; whether the moved-line and the
panel's `from` row can print something a reader misreads; and whether
`questions.md` P1's default — resolve, print, never refuse — leaves any case
where the gate now seals something it should not. P1 itself was declared
answered under this run's `Automation = yes` and was not the reviewer's to
reopen; a defect it lets through was.

`evidence_check.py .` was required unscoped, because the scoped form blinds a
round to rows the branch falsified but does not own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the stated failure direction is wrong — the gate can allow MORE, measured | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | answered | corrected at 9a6d4a35; Probe: stale spelling exit 1, resolved exit 0, over a base whose own commit deleted wording. `spec.md` §*What is wrong* already corrects the direction claim; `plan.md` §*Operational impact* and `overview.md` carry the same false sentence. `CONTRIBUTING.md` §*What a change to a gate must carry* makes it a required clause |
| 2 | 🟡 the moved-line can assert `CI reads <ref>` about a ref CI never reads | `skills/verify/scripts/broad_gate.py#moved_line` | **fixed** `0baac5c3` | fixed at 0baac5c3; Probe on a clone with a second remote: the line named `other/base` while `origin/base` existed at a different commit. `agents/sealer.md` tells the sealer to quote this line in its report |
| 3 | 🟡 *nothing about that run changes* is false for a remote-less repository | `skills/verify/scripts/broad_gate.py#resolve_base` | **fixed** `e1dc0bc1` | fixed at e1dc0bc1; Probe: children handed `ced5e4d` where they were handed `base`. The `Broad gate` cell, the `NOT SEALED` line, `base_label`'s quotation and the panel all move. The branch's own A3 divergence row is the same fact |
| 4 | 🟡 the drift pin reads 3 of the 4 base-taking steps `plan.md` enumerates | `tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments` | **fixed** `c0413556` | fixed at c0413556; Probe over six spellings: 3 unseen, including `BASE: origin/${{ github.base_ref }}`, which `.github/workflows/hygiene.yml:291` already uses. `phases/phase-4.md` and the changelog claim a later step is covered the day it is written |
| 5 | 🟡 the panel `from` row is cut at 23 columns with no marker and no line beside it | `skills/verify/scripts/broad_gate.py#panel` | **fixed** `e7488cec` | fixed at e7488cec; Rendered a 32-column ref through `seal_stamp.letter`: `origin/release/2026-09-` reads as a whole ref. A4 means nothing prints beside it on an agreeing run. The case asserts an 11-column ref, so the cut is never exercised |
| 6 | ⬜ `@{upstream}` is appended to any revision expression, so `--base HEAD` resolves to the current branch's upstream | `skills/verify/scripts/broad_gate.py#resolve_base` | **fixed** `aeef875a` | fixed at aeef875a; Probe on a clone sitting on `topic`: `--base HEAD` resolved to `origin/base`. Degenerate input, and the moved-line fires in the interesting case |
| 7 | ⬜ the distance reads `1 ahead, 0 behind` with no subject | `skills/verify/scripts/broad_gate.py#moved_line` | **fixed** `0baac5c3` | fixed at 0baac5c3; Read. Both refs are in the sentence and neither is named as the thing the counts are relative to |
| 8 | ⬜ correction — `spec.md` §Out still says the cell already names commits | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | answered | corrected at 9abf7a6c; Located in the run's paperwork, so it owes no fix pass. `overview.md` §*Fed back into the spec* reads `none` while §Out carries a sentence phase 2 disproved |
| 🟢 | divergence 1 verified — `args.base` read once | `skills/verify/scripts/broad_gate.py#gate` | not a defect | Parsed the file: one occurrence. `spec.md`'s table is headed *Consumer*, and the count case asserts the stronger property |
| 🟢 | divergence 2 verified — the `Broad gate` cell's base half | `skills/code-review/scripts/chain_check.py#broad_gate` | not a defect | Both parsers take `SHA_RE.findall(...)[0]`, read at `chain_check.py:3530` and `round_record.py:4291`. §Out and §Scope 3 disagreed and the branch took the repairing side |
| 🟢 | divergence 5 verified — the document pin is not vacuous in either file | `tests/test_the_gate_asks_the_range_ci_will_ask.py#says_what_the_base_resolves_to` | not a defect | Counted the qualifying blocks: one in `agents/sealer.md`, one in `skills/verify/SKILL.md`. The builder measured only the first |
| 🟢 | divergence 6 verified — four re-verified ledger rows still hold | `seal/ledger.md` | not a defect | `draft_env` and its call site byte-identical; `seal`'s two-exit reading unchanged; `not_as_written` at 1267 still above `resolve_base` at 1278 and the first `run` at 1312; `agents/sealer.md` has one hunk at line 54 and the absent-row paragraph at 116 is untouched |

## Paste-ready fixes

```markdown
    **It is not a refusal, and that was argued rather than assumed.** A
    refusal's only repair is a `git fetch` and a second nine-minute gate,
    performed by a person the sealer has no way to ask, and it would fire on
    the ordinary release case where a sibling merges while a branch is open.
    Prompt budget: zero. **Failure direction: each arm moves toward CI's
    answer, and that is not one direction.** Wording the base itself removed
    leaves the range, so the survivor arm can pass where it used to refuse;
    the branch's replacement of base wording enters it, so the arm can refuse
    where it used to pass. `spec.md` §*What is wrong* has the argument — what
    a stale base guarantees is a disagreement, not a direction. The cheaper
    mistake is still this one: a gate that answers a question the merge is not
    judged by is worse than a gate that errs either way, because its stamp
    reads as a pass.
```
```python
def moved_line(root, base):
    """The one line printed where resolving the base MOVED the answer, or
    None where the given spelling and the resolved one are the same commit.

    ... (docstring unchanged above this paragraph) ...

    **It never says CI reads a ref CI does not read.** Step 1 of the rule is
    `<base>@{upstream}`, which a clone tracking a second remote answers with
    something that is not `origin/<base>` — and the workflow spells
    `origin/<base>` literally. Where the two part, the line says what THIS
    checkout declares and names the ref a runner would read beside it.
    """
    if not base.moved:
        return None
    runner = REMOTE_LABEL.format(ref=base.given)
    if base.ref == runner:
        reads = f"CI reads {base.ref}, which is {base.commit}"
    else:
        reads = (
            f"this checkout says {base.given} tracks {base.ref}, which is "
            f"{base.commit} — not the {runner} a runner reads"
        )
    if base.given_commit is None:
        return (
            f"broad-gate: --base {base.given} names no commit in this "
            f"checkout; {reads}. Every check below was asked about {base.ref}."
        )
    # `--left-right` counts each side of the symmetric difference: what the
    # given spelling holds that the resolved one does not, then the reverse.
    counts = git(
        root, "rev-list", "--count", "--left-right", f"{base.given}...{base.ref}"
    )
    apart = ""
    if counts and len(counts.split()) == 2:
        behind, ahead = counts.split()
        apart = f" — {base.ref} is {ahead} ahead and {behind} behind {base.given}"
    return (
        f"broad-gate: --base {base.given} is {base.given_commit} in this "
        f"checkout; {reads}{apart}. Every check below was asked about "
        f"{base.ref}."
    )
```
```python
def test_the_line_does_not_claim_ci_reads_a_second_remote(tmp_path):
    """The gate prefers what the checkout says the base tracks, which can be a
    remote CI never reads. The line may say what resolving found; it may not
    say a runner reads it."""
    fork = upstream_repo(tmp_path / "fork")
    work = clone(fork, tmp_path / "work")
    other = upstream_repo(tmp_path / "other")
    write(other, "docs/second.md", "# the tree moved\n")
    commit(other, "the real base moved")
    git(work, "remote", "add", "other", str(other))
    git(work, "fetch", "-q", "other")
    git(work, "branch", "--set-upstream-to=other/base", "base")
    mod = gate_module()
    said = mod.moved_line(str(work), mod.resolve_base(str(work), "base"))
    assert "other/base" in said, said
    assert "CI reads other/base" not in said, said
    assert "origin/base" in said, f"the runner's own spelling is missing: {said}"
```
```python
      3. the ref as given. A base with no remote-tracking counterpart — never
         pushed, a bare SHA, a repository with no remote at all — resolves to
         itself, and every gate fixture in the suite is that repository. What
         does NOT stay the same there is what the consumers are handed: the
         resolution turns the ref into its commit for them too, so that
         repository's `Broad gate` cell, its `NOT SEALED` line and the
         baselines the child checks quote back all name a hash where they
         named a branch. One assertion in
         `tests/test_the_seal_is_taken_once_by_the_sealer.py` moved for it.
```
```markdown
    **A repository with no remote resolves to itself, and the ONLY thing that
    moves there is the spelling the consumers get.** The resolution lands on
    the ref as given; the commit is what every check, the `Broad gate` cell
    and the `NOT SEALED` line are handed, in that repository as in any other.
    That is every fixture in the suite today and every user on a local-only
    tree, and it is why one assertion in the gate's own module reads a hash
    where it read a branch name.
```
```python
# Every place the workflow names a base, not only the ones spelled as a
# quoted argument at the start of a line. Three shapes occur or plausibly
# will: the flag on its own continuation line, the flag on the same line as
# its command, and an `env:` assignment a later `run:` block reads.
BASE_ARGUMENT = re.compile(r'(?:--baseline|--range)\s+(?:"([^"]+)"|(\S+))')
BASE_ENVIRONMENT = re.compile(r"^\s*BASE:\s*(\S.*?)\s*$")
REMOTE_TRACKING = "origin/${{ github.base_ref }}"


def workflow_base_arguments():
    """Every revision the hygiene workflow names as a base, as it spells it.

    A substring search for the remote-tracking spelling stays green while a
    fourth base-taking step is added without it, because the earlier three
    still carry the string — so each occurrence is read on its own. An `env:`
    assignment counts: `.github/workflows/hygiene.yml` already names a base
    that way, and a step reading `$BASE` is as much a reader of the base as
    one spelling it on a command line.
    """
    found = []
    for line in read(HYGIENE).splitlines():
        for match in BASE_ARGUMENT.finditer(line):
            found.append(match.group(1) or match.group(2))
        environment = BASE_ENVIRONMENT.match(line)
        if environment:
            found.append(environment.group(1))
    assert found, "the hygiene workflow names no base at all"
    return found
```
```markdown
  - **One case holds the gate's spelling against the workflow's**, from both
    sides. The workflow side is read as every revision the file names as a
    base — each `--baseline` and `--range` argument wherever it sits on the
    line, and each `BASE:` assignment — rather than as one substring search,
    so a base-taking step written in any of those three shapes is covered the
    day it is written. A step that names its base some fourth way is not, and
    that is the reach of the pin rather than a promise about all of them.
```
```python
    # `seal_stamp.letter` gives a value 23 columns and cuts at the frame with
    # no marker, and on a run where the two agree nothing prints beside this
    # row (A4). A cut ref that reads as a whole ref is the misreading the row
    # exists to prevent, so the elision is made here and the TAIL is kept:
    # `origin/` is the part a reader can infer and the branch name is not.
    width = stamp.PANEL_WIDTH - 2 - len("  {:<8} ".format(""))
    shown = base.ref
    if len(shown) > width:
        shown = "..." + shown[-(width - 3) :]
    rows = [
        ("SEALED", ""),
        None,
        ("tree", tree),
        ("base", base.commit),
        ("from", shown),
```
```python
def test_a_ref_too_long_for_the_panel_says_it_was_cut(tmp_path):
    """A6. `seal_stamp.letter` cuts a value at the frame with no marker, and
    A4 means nothing prints beside the row on an agreeing run — so a ref that
    does not fit has to say so in the row itself."""
    mod = gate_module()
    long_ref = "origin/release/2026-09-21-hotfix"
    base = mod.Base("release/2026-09-21-hotfix", "aaaaaaa", long_ref, "bbbbbbb")
    checks = {
        name: mod.Check(name, 0, "1 passed in 0.1s", "out.txt")
        for name in (mod.SUITE, mod.LEDGER, mod.CHAIN_NAME)
    }
    shown = dict(row for row in mod.panel("ccccccc", base, checks, None) if row)
    assert shown["from"] != long_ref[: len(shown["from"])], (
        f"the ref was cut with no marker: {shown['from']!r}"
    )
    assert shown["from"].endswith("hotfix"), shown["from"]
```
```python
    given_commit = short_commit(root, given)
    # `@{upstream}` is a suffix on any revision expression, and `HEAD@{upstream}`
    # answers for the CURRENT branch rather than for the one `--base` named. The
    # rule is about what a BRANCH tracks, so the step is asked only of a branch.
    tracked = None
    if git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{given}"):
        tracked = git(
            root, "rev-parse", "--abbrev-ref", UPSTREAM_BASE.format(ref=given)
        )
    if tracked and tracked.strip():
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_asks_the_range_ci_will_ask.py -q`, in a clone at the target SHA | exit 0 — 21 passed |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q`, same clone | exit 0 — 121 passed. A3's *nothing else moved*, with the one declared edit in it |
| `evidence_check.py .` unscoped, same clone | exit 0 — 1370 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| probe — `survivor_check.py --range` at both spellings, over a base whose own commit deleted wording the branch then merged in | stale exit 1 (2 sentences removed), resolved exit 0 (0 removed). Finding 1 |
| probe — `resolve_base` in a clone whose `base` tracks a second remote while `origin/base` exists | resolved to `other/base`; the line says *CI reads other/base*. Finding 2 |
| probe — `resolve_base` in a repository with no remote | children handed `ced5e4d` where they were handed `base`. Finding 3 |
| probe — `BASE_ARGUMENT` over six workflow spellings | 3 of 6 unseen. Finding 4 |
| probe — `seal_stamp.letter` over refs of 22, 30 and 32 columns | cut at 23 with no marker. Finding 5 |
| probe — `resolve_base` with `--base HEAD` | resolved to the current branch's upstream. Finding 6 |
| the broad gate — the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's one run, after the rounds settle (`agent-contract` §2), and it has not come due while findings 1 to 5 are open |

```
P1 STALE (gate as it stood)     spelling=base       exit=1
     survivor-check: examined 2 files at bf3d7b5, against 2 sentence(s)
     the range 9d68e3f..bf3d7b5 removed
P1 RESOLVED (gate now)          spelling=9aa1595    exit=0
     survivor-check: examined 2 files at bf3d7b5, against 0 sentence(s)
     the range 9aa1595..bf3d7b5 removed
       no removed wording is still standing
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame by M1's own default |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default (a) under this run's `Automation = yes`, and not reopened here |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix |
