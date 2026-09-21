# 1789985781-the-gates-arm-list-is-maintained-by-hand — review round 1

| Field | Value |
|---|---|
| Target SHA | 8490328a7fac5558193236d4abbf6d849eeb6f46 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 472 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `8ac8dd93b0750ab297db6efd2da721ece5da648d..c0b0d7120cf1b4e57082efeb2ec36b2beebaa3df`, 3 commits |
| Contract changes | none |
| New units | test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was (depth 1); UNCLASSIFIED_WORKFLOW (depth 1); test_a_step_no_row_classifies_is_not_said_to_carry_a_reason (depth 1); test_a_step_a_row_excludes_is_still_pointed_at_its_reason (depth 1) |
| Needs a fix | yes — findings 1, 2, 3, 4 and 5. One is the shipped declaration stating its own measurement two contradictory ways; two is a deferral whose home closes with this release; three is a line that tells a reader a reason exists where none does; four is a justification naming jobs that do not exist; five is an uncaught decode error that ends the gate on a traceback. |
| Loses a record or crashes | yes — finding 5. `workflow_text` raises `UnicodeDecodeError` out of `gate()` for a `hygiene.yml` that is not UTF-8, and `main` catches only `Refused`, so the run ends on a traceback instead of a verdict. Reproduced in a probe; not reachable in this repository, whose workflow is UTF-8. |

- [x] Pass

## What this round was asked

Round 1, the first round of the work item: the whole branch against its own
frame, spec compliance before quality.

The reviewer was told the frame was drawn by the orchestrating session rather
than by a framer, and told to give the spec MORE suspicion than usual on that
account — with the fact that the session's two earlier work items had each
produced a spec that was wrong about the tree, once as a 🔴.

The judgment asked for first was the one the build had to make because the
frame refused to: `questions.md` M1 asked how many of the `release` job's
thirteen steps a gate could mirror but does not, and the build answered six,
then split the six on a line the frame never drew — **does the plugin ship the
check** — adding arms for the two under `skills/` and excluding the four that
live in `.github/scripts/` or inline. Whether that line is the right one,
drawn in the right place, and actually stated by each exclusion's reason was
the round's first question.

Four declared divergences were handed over: W1 answered *both, in different
streams*; §Scope 3's *however many* becoming two; `plan.md`'s retyped list of
the thirteen having already rotted by one step when it was written; and the
new arms following their steps' range but not their guard.

Two things on the reviewer's own account. A mutation had SURVIVED and taken a
unit out of the tree — `job_steps`'s comment-stripping line — and the round was
asked whether it was dead or load-bearing in a case nobody wrote, and to look
for others, since this session's two earlier work items had produced nine
green-while-broken units between them. And a silence the builder reported in
the shared ledger: `broad_gate.py#gate` drifted, the lenient report said
`1 drifted` where three rows cite that coordinate, so `--reverify` as
documented would stamp *somebody read this* on two rows nobody read.

Also asked: whether the totality case can pass while the gate runs an arm no
row describes; whether an exclusion reason could be written to silence the
case rather than to state a truth, and whether A4 catches that; and whether
the stderr line and the panel row can print something a reader misreads.

`evidence_check.py .` unscoped, exit codes read directly, `seal/ledger.md` off
limits to a whole read. The verdict-table shape was spelled out again, after
three rounds in this session were sent back by the generator for an unkeyed
row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The comment declaring `PARTITION` states M1's measurement two ways and both cannot be true: *Six of the eight exclusions could not run here at all; two could* against *The last four are the ones with a local answer*, and it splits the four as two inline-shell and two repository scripts where the workflow has one and three. Every other record of the same measurement says four-and-four | `skills/verify/scripts/broad_gate.py:1300` | **fixed** `c0b0d71` | fixed at c0b0d71; Counted against `.github/workflows/hygiene.yml`'s thirteen steps directly. The four with a local answer and no arm are the inline version bump, `gather_changelog.py`, `fold_ledger.py` and `claude_block.py`; a fourth `.github/scripts/` step, `issue_claims_check.py`, is excluded for the pull-request body instead. `overview.md` §*What `questions.md` M1 measured*, `phase-1.md`, `questions.md` Q2, `changelog.md` and `skills/verify/SKILL.md` agree with the count and disagree with this comment |
| 2 | The guard divergence is deferred to #423, which is milestone `release: 0.12.2` and OPEN, so it closes with this release; and #423 is about the gate resolving `--base` against a local ref, not about an arm whose step CI skips on a `main` base. After 0.12.2 the non-equivalence has no open home | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/spec.md:119`, `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:91` | answered | corrected at c0b0d71 — both coordinates are records, so a `fixed` verdict would send a reader to open a commit for a note; `gh issue view 423` reports state OPEN, milestone `release: 0.12.2`; its body names `--range "origin/${{ github.base_ref }}...HEAD"` and no guard. The branch's one new `seal/follow-up.md` row is about the `--reverify` silence. The divergence itself is sound — a correction arm guarding differently from the survivor arm beside it would put two readings in one function |
| 3 | `coverage_line` tells the reader each unanswered step carries a reason in `broad_gate.py#PARTITION`. For a step no row classifies there is no such reason, and the panel counts it beside the ones that have one | `skills/verify/scripts/broad_gate.py:1446` | **fixed** `92c8d17` | fixed at 92c8d17; Executed in a scratch repository with a `release` job of its own: the line named `deploy to staging; notify the channel` and the panel drew `workflow  2 of 2 not answered`. `unanswered`'s docstring at `:1414` names the case; no case in A1–A7 reaches it, and A7's fixture asserts the line's absence rather than its content |
| 4 | The exemption that lets `suite` and `ledger` run without a partition row is justified as *they answer the workflow's OTHER jobs*. `hygiene.yml` declares one job. `suite` is the `Broad gate` row and `ledger` mirrors the `ledger` job of `.github/workflows/test.yml` | `tests/test_the_gate_names_every_step_ci_runs.py:284`, `tests/test_the_gate_names_every_step_ci_runs.py:296` | **fixed** `c0b0d71` | fixed at c0b0d71; The assert message is read at the moment a maintainer adds an arm and must decide whether it needs a row; it hands them an empty category. `spec.md` §Scope Out carries the same reading and is where it came from. The exemption mechanism itself is sound and bounded |
| 5 | `workflow_text` promises *or None* and catches `OSError` only, so a `hygiene.yml` that is not UTF-8 raises `UnicodeDecodeError` out of `gate()`; `main` catches only `Refused`, and the gate ends on a traceback instead of sealing | `skills/verify/scripts/broad_gate.py:1398` | **fixed** `3e87599` | fixed at 3e87599; Executed against a `release` job written in latin-1: `UnicodeDecodeError 'utf-8' codec can't decode byte 0xe9 in position 45`. A repository the partition is not about must come out of the run as it went in, which is A7's whole clause |
| ⬜ | `overview.md`'s proof block says the new module is 15 cases. It is 20 | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/overview.md:19` | correction | `grep -c "^def test_"` returns 20 and the executed run reports `20 passed in 7.38s` |
| ⬜ | A trailing YAML comment on a `- name:` line is read as part of the step name, where YAML ends the scalar at the unquoted ` #` | `skills/verify/scripts/broad_gate.py:1237` | correction | Driven: `job_steps` returns `['a step  # with a trailing comment']`. Not live — no such line in `hygiene.yml` — and it fails loud through A1 rather than silently. `strip_comments` in `tests/test_ci_gives_the_checks_what_they_need.py:37` has the same gap, so it is a class rather than something this branch opened |
| ⬜ | R2's re-read marker writes a line number into a ledger row's notes (*line 1633, the resolution*), which will rot for an edit anywhere above it. The claim it decorates — the count — is the checkable half and is already stated | `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md:4` | correction | `CLAUDE.md` §*A ledger coordinate names content* says a row carries no line number. Existing rows do carry commit SHAs in prose, so the practice reads that clause as the coordinate cell's; noted as a rot risk rather than as a rule break. Verified accurate at this SHA: `args.base` at `:1574`, `:1628`, `:1633`, one read |
| 🟢 | The line the build drew — does the plugin ship the check — is the right one, and it is drawn in the right place | `skills/verify/scripts/broad_gate.py:1310` | not a defect | `broad_gate.py` ships to every installation, so an arm reaching `.github/scripts/` would fail in every clone but this one. `correction_check.py` and `seal.py` are under `skills/`, so the gate runs the file CI runs. Each of the four exclusion reasons is true of its step, checked one at a time against the workflow |
| 🟢 | The mutation that survived was dead rather than load-bearing, and the phase record's account of it is accurate | `skills/verify/scripts/broad_gate.py:1226` | not a defect | `STEP_RE` anchors on the list's dash and `JOB_RE` on a job key's letter, so a whole-line comment matches neither. Three further reader shapes driven — a `- name:` behind a command in a `run:` block, a `name:` under `with:`, a `jobs:` key with trailing whitespace — each came back correct, the last loudly through `workflow_steps`'s refusal |
| 🟢 | The three shared-ledger claims re-stamped after the drift all hold, and each marker says what was actually checked | `seal/ledger.md:1945`, `seal/ledger.md:1949`, `seal/ledger.md:2230` | not a defect | `draft_env` and its call site byte-identical; `seal_record`, the two-exit reading and the `sealed` discriminator byte-identical; both new arms recorded after the first `run`, so the refusal still precedes any shell. `evidence_check.py .` unscoped: exit 0, `1398 ok · 0 drifted · 0 broken` |
| 🟢 | The new arms do not refuse a repository that has no ledger file and no `Mode` row, which is the regression adding two unconditional arms could have shipped | `skills/verify/scripts/broad_gate.py:1697` | not a defect | Executed on two scratch repositories, one with no `seal/ledger.md` and one whose `seal/config.md` declares no `Mode` row: both sealed, exit 0. `seal.py mode --check` returns 0 with *no seal/ here* and `correction_check.py` walks an empty range without refusing |
| 🟢 | A4 catches a shape and never a truth, and the build says so in four places rather than claiming the hole is closed | `seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/plan.md` | not a defect | *The check is inline* passes both cases and says nothing. Named in `plan.md` §*The failure scenario at six months*, the `PARTITION` header, the case docstring and `overview.md` §*Not done*. Disclosure rather than a defect |

## Paste-ready fixes

```python
# **Four of the eight exclusions could not run here at all; four could.** The
# measurement `questions.md` M1 asked for, taken by construction over all
# thirteen: three steps have no local answer (the pull request's body, the
# remote's pull-request namespace, the tracker), one raises a warning and can
# refuse nothing, one is shell written inline in the workflow with no script
# to share, and three run a script that belongs to this repository rather
# than to the plugin. The last four are the ones with a local answer, and
# `seal/config.md`'s `Broad gate` row is where a repository names checks of
# its own — not the arm list of a script that ships to every repository that
# installs the plugin.
```
```markdown
| the new arms mirror their steps' **range**, not their steps' **guard** | the workflow skips the survivor and correction steps when the base is `main`; the gate skips neither | left as it is | The survivor arm has had this difference since it was added, and making the correction arm behave differently from its neighbour would put two readings of one question inside one function. The class is *whether a mirrored arm asks its step's question*, which `spec.md` §*What this repair cannot see* puts outside this item. #423 is not its home — that work item is about the base the gate resolves, and it ships in this release — so the class is carried into `seal/follow-up.md` instead |
```
```markdown
| **The gate runs the `survivors` and `corrections` arms on a base the workflow exempts.** `.github/workflows/hygiene.yml`'s survivor step and its correction step both open `if [ "${{ github.base_ref }}" = "main" ]; then … exit 0`, because a release branch carries squashed commits rather than its work items' merges and each work item was read at its own pull request. `broad_gate.py#gate` runs both unconditionally against `<base>...HEAD`. Read, not executed, 2026-09-21 in round 1 of #468: the difference arrived with the survivor arm and #468 added the second instance rather than opening the class. **Why it costs something**: a gate run whose base is `main` — a release-preparation branch, a hotfix cut from `main` — can refuse for a marker dropped by a merge of `main` back into a release branch, which is exactly the range CI decided not to judge. The failure is a wasted seal rather than a lost correction, which is the same shape #468 itself was ruled an issue for. **What needs a person is which side moves**: the arms could take the workflow's guard, which makes `gate()` read `base` twice for one question; or the partition could carry a third column saying *mirrored, with a narrower guard than its step*, which is a change to what the gate prints; or the pair could stay as they are with this row standing. Not measured: whether any sealer run in this repository has ever had `main` as its base | the repository owner |
```
```python
def coverage_line(text):
    """One line naming the steps this seal did not answer, or None.

    **Names here, a count on the panel** (`questions.md` W1).
    `seal_stamp.letter` gives a panel value 23 columns, which thirteen step
    names do not fit and a count does — and a reader who is told only a number
    has to reconstruct WHICH from two files, which is the reconstruction this
    work item exists to remove. So the panel carries the number and this
    carries the names, on the stream the gate already uses to say which
    command the row asked for.

    **A step no row classifies is named apart from one a row excludes.**
    `PARTITION` describes SpecSeal's own `release` job; in another repository
    whose workflow happens to carry that job name, every step is unclassified
    and none of them has a reason written anywhere. Pointing that reader at
    `PARTITION` sends them to thirteen rows about a workflow they do not run.
    """
    steps = job_steps(text, RELEASE_JOB)
    if not steps:
        return None
    short = unanswered(text)
    if not short:
        return (
            f"broad-gate: this seal answers every one of {WORKFLOW}'s "
            f"{len(steps)} `{RELEASE_JOB}` steps"
        )
    classified = {name for name, _, _ in PARTITION}
    excluded = [step for step in short if step in classified]
    unknown = [step for step in short if step not in classified]
    said = (
        f"broad-gate: {WORKFLOW}'s `{RELEASE_JOB}` job runs {len(steps)} "
        f"steps and this seal answers {len(steps) - len(short)}."
    )
    if excluded:
        said += (
            " Not answered, each with the reason no arm mirrors it in "
            "`broad_gate.py#PARTITION`: " + "; ".join(excluded) + "."
        )
    if unknown:
        said += (
            " In no row of `broad_gate.py#PARTITION` at all, so this gate has "
            "no reading of them and answers nothing for them: "
            + "; ".join(unknown)
            + "."
        )
    return said
```
```python
UNCLASSIFIED_WORKFLOW = """\
name: hygiene

on:
  pull_request:

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: a declared review chain has the round record it claimed
        run: true
      - name: deploy to staging
        run: true
"""


def test_a_step_no_row_classifies_is_not_said_to_carry_a_reason():
    """A6's other repository. `PARTITION` describes THIS repository's release
    job, and `broad_gate.py` ships to every installation — so a repository
    with a `release` job of its own has steps no row has ever heard of.

    Counting them as unanswered is honest; telling their reader the reason is
    in `PARTITION` is not, because `PARTITION` holds thirteen rows about a
    workflow that repository does not run."""
    said = gate.coverage_line(UNCLASSIFIED_WORKFLOW)
    assert "deploy to staging" in said, said
    reasoned = said.split("no arm mirrors it in", 1)
    assert "deploy to staging" not in reasoned[-1] or len(reasoned) == 1, (
        f"a step in no row of PARTITION is named among the ones PARTITION "
        f"gives a reason for:\n{said}"
    )
    assert "no row of `broad_gate.py#PARTITION` at all" in said, said
```
```python
def test_the_gate_runs_no_arm_the_partition_does_not_account_for():
    """A3's other side. An arm the gate runs and the partition never names is
    an arm nobody can say which step it stands for — the `suite` and `ledger`
    arms aside, which answer no step of this job at all: `suite` is the
    repository's own command from the `Broad gate` row, and `ledger` mirrors
    `evidence_check.py` as `.github/workflows/test.yml`'s `ledger` job runs
    it. `hygiene.yml` declares one job, so an arm that is not a `release`
    step's belongs in the set below."""
    answering_no_release_step = {gate.SUITE, gate.LEDGER}
    named = {arm for _, arm, _ in gate.PARTITION if arm}
    loose = sorted(
        getattr(gate, name)
        for name in arms_the_gate_runs()
        if getattr(gate, name) not in named | answering_no_release_step
    )
    assert not loose, (
        f"`gate()` runs these arms and no partition row names them: {loose}. "
        "An arm belongs to a step of the `release` job, or it answers "
        "something outside that job — the repository's own command, or a job "
        "of another workflow — and belongs in the set above"
    )
```
```markdown
| The `ledger`, `lint` and `pytest` jobs of `.github/workflows/test.yml` | The gap is `hygiene.yml`'s `release` job list, and that workflow declares no other job. Those three are already answered by the declared row and the ledger arm, and widening the subject is how a bounded work item stops being one |
```
```python
def workflow_text(root):
    """The hygiene workflow of the repository being gated, or None.

    None is the ordinary case away from this repository: the plugin ships to
    repositories that have no such workflow, and for them nothing about the
    run changes (`spec.md` A7). **A file that is there and is not UTF-8 is
    the same case**, and it has to be: a decode error raised here leaves
    `gate()` on a traceback, which is the largest possible change to the run
    of a repository this partition is not about.
    """
    try:
        with open(os.path.join(root, WORKFLOW), encoding="utf-8") as handle:
            return handle.read()
    except (OSError, ValueError):
        return None
```
```python
def test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was(tmp_path):
    """A7's other shape. `UnicodeDecodeError` is a `ValueError`, not an
    `OSError`, and `broad_gate.main` catches only `Refused` — so before this
    the gate ended on a traceback for a repository whose workflow file
    happens to be latin-1."""
    repo = sealable_repo(tmp_path, resolution="kept")
    path = repo / ".github" / "workflows" / "hygiene.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        "jobs:\n  release:\n    steps:\n      - name: café step\n".encode(
            "latin-1"
        )
    )
    commit(repo, "a workflow file that is not utf-8")
    assert gate.workflow_text(str(repo)) is None
    result = run_gate(repo, tmp_path / "out")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SEALED" in result.stdout, result.stdout
    assert "Traceback" not in result.stderr, result.stderr
    assert "not answered" not in result.stdout, result.stdout
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_names_every_step_ci_runs.py -q` in a clone at the target SHA | exit 0 — `20 passed in 7.38s` |
| `bin/test` over the five modules that read `broad_gate.py` — the range module, the sealer module, the lenient-run module, the rule module and the row module | exit 0 — `203 passed in 77.38s` |
| `evidence_check.py .` unscoped, no `--ledger` | exit 0 — `total: 1398 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `3 work items read · 92 unread · 184 names read · 0 refused · 0 drifted` |
| Probe: the gate over a scratch repository with a `hygiene.yml` of its own whose `release` steps no `PARTITION` row names | exit 0, sealed — the stderr line claimed a reason in `PARTITION` for two steps it has no row for, and the panel drew `workflow  2 of 2 not answered`. Finding 3 |
| Probe: `workflow_text` against a `release` job written in latin-1 | raised `UnicodeDecodeError`, uncaught by `main`. Finding 5 |
| Probe: the gate over a scratch repository with no `seal/ledger.md`, and over one whose `seal/config.md` declares no `Mode` row | exit 0, sealed in both. No regression from the two unconditional arms |
| Probe: `job_steps` driven over a trailing-comment step line, a `- name:` inside a `run:` block, a `name:` under `with:`, and a `jobs:` key with trailing whitespace | one gap — the trailing comment joins the step name; the other three correct |
| The broad gate — the full suite, the repository-wide lint and the typecheck over this branch | not yet. It is the sealer's one run, after the rounds settle; `agent-contract` §2 keeps it out of this round. The last round record's `Broad gate` cell is the sealer's to write |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `round_record.py` and `correction_check.py` deduplicate a repeated ledger coordinate the way `evidence-check`'s drift report does | `seal/follow-up.md`, in the row this branch added | the repository owner |
| Whether the four excluded steps with a local answer should move into the `Broad gate` row of `seal/config.md` | `questions.md` Q2, default **(a)** — leave them excluded | the repository owner |
| Whether an exclusion written to make A1 green rather than to state a truth can be caught at all | `plan.md` §*The failure scenario at six months* and `overview.md` §*Not done* — named as an open hole, not closed | a planner, if it is ever worth closing |
