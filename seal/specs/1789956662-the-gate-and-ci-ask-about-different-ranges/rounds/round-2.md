# 1789956662-the-gate-and-ci-ask-about-different-ranges — review round 2

| Field | Value |
|---|---|
| Target SHA | e68f64a9ad19bd2a4ad96e41240bf919b39ceb6b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 459 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `2f1010c9ba34cf365b71828cc425b2179eaafb69..1101382634bfde9a07487d14416c3f1f7a4fa653`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 9 (10 to 14 are ⬜, so none of the five counts) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round: the fixes that closed round 1, opened by
somebody. The reviewer inherited round 1's committed record and was told its
eight verdicts are closed and not to be reopened unless the fix that closed
one does not do what its cell says. What each fix CLAIMS was listed per
finding, so the round could check the claim rather than rediscover the
finding, and the range it was over was named: `9a6d4a35..da117184`, twelve
commits, plus the record repair at `e68f64a`.

Three things the fix pass had raised about itself were handed over as the
round's own judgments rather than as facts. Whether finding 3's class is
closed or only its coordinates — the pass had found the same fact standing in
a third place after fixing two, so the question was asked of every fact round
1 moved, not only that one. Whether three `survivors.md` rows that the builder
says excuse nothing in this tree should stand or be deleted, with a plain
answer wanted either way. And whether the two phase records corrected in place
render what is true now, after the pass found phase 4's correction sitting
inside an HTML comment while the false claim rendered in bold.

`evidence_check.py .` unscoped. Exit codes read directly rather than through a
pipe. The broad gate was named as still belonging to the sealer, after this
round settles.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | 🟡 two copies of *nothing about that run changes* survive round 1's finding 3 | `tests/test_the_gate_asks_the_range_ci_will_ask.py:340` | **fixed** `11013826` | fixed at 11013826; Executed the A8 fixture: `base.ref` is `never-pushed`, `base.commit` is a hash, and the children are handed the hash where they were handed `args.base`. The fix pass edited this function's body three lines below the sentence. Pull request #459's body carries the same claim as *nothing about its run changes*, which the corrected phrasing does not grep |
| 10 | ⬜ `names_a_branch`'s docstring is wrong that `@{…}` is refused, and the line then names `origin/@{-1}` | `skills/verify/scripts/broad_gate.py#names_a_branch` | deferred #461 | #461 — the guard's docstring names a class `check-ref-format --branch` does not refuse, and the line then quotes `origin/@{-1}`; Measured on git 2.54.0: `@{-1}` accepted, `HEAD` `HEAD~1` `base@{u}` `topic@{1}` refused. `--base @{-1}` resolves through step 1 and the moved-line says *not the origin/@{-1} a runner reads*. Degenerate input; `moved_line`'s own promise is over-claimed by it |
| 11 | ⬜ `--baseline ""` yields `None` and the caller raises `TypeError` rather than asserting | `tests/test_the_gate_asks_the_range_ci_will_ask.py#BASE_ARGUMENT` | deferred #463 | #463 — an empty baseline returns `None` and the caller raises where its siblings assert; a test helper, reaching no user; Executed: `base_spellings` returns `[None]`, `SHELL_VARIABLE.match` raises. The widening from `[^"]+` to `[^"]*` is what admits it. Nothing in the workflow spells a base that way |
| 12 | ⬜ the reader counts a flag inside a YAML comment and any `BASE:` line, so the pin can go red on a correct workflow | `tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings` | deferred #462 | #462 — the widened reader counts a commented flag and any `BASE:` line; latent, fails closed, and the one square that could stop somebody; Executed over a commented flag: read as a base. Round 1's report named this direction for `$BASE` and the fix closed it with `SHELL_VARIABLE`; the two new shapes reopen it one step over. Latent — the file carries one `BASE:` line and three flags, all real |
| 13 | ⬜ the panel docstring keeps the accepting-the-cut argument phase 3 recorded as no longer arising | `skills/verify/scripts/broad_gate.py#panel` | deferred #464 | #464 — `panel`'s docstring leads with the argument phase 3 retired, and the elision's grounds assume an `origin/` prefix; Read. The first paragraph still says the cut is why the printed line is authoritative and this row is context; the paragraph under it says the ref now says it was cut. `spec.md`'s `seal_stamp.letter` row carries the same reasoning and is paperwork. The elision's stated grounds assume the prefix is `origin/`, which round 1's finding 2 disproved |
| 14 | ⬜ the baseline half of the direction claim is stated unlabelled in three documents | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | deferred #464 | #464 — the baseline half of the direction claim stands unlabelled in the three operational statements; Read. Round 1's report labelled that half *read, not executed*; the three operational statements carry it beside the measured half with no label and no answerer. The shared ledger's R3 row does keep the measured half labelled `Executed` |
| 🟢 | round 1 finding 1 verified — the direction claim | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | not a defect | Both halves of the replacement are grounded: the pass-where-it-refused half is round 1's probe, the refuse-where-it-passed half is the measured defect #423 opened on. No fourth standing copy in the tree, and pull request #459's body was corrected too. Finding 14 is the one clause it states without a label |
| 🟢 | round 1 findings 2 and 7 verified — the moved-line | `skills/verify/scripts/broad_gate.py#moved_line` | not a defect | Executed on a clone tracking a second remote: the line names `other/base`, does not say CI reads it, and names `origin/base` beside it. The opposite case pins that it still says *CI reads origin/base* in an ordinary clone. The distance names both ends. Finding 10 is the one spelling the promise does not cover |
| 🟢 | round 1 finding 3 verified for the code — the docstring and the spec | `skills/verify/scripts/broad_gate.py#resolve_base` | not a defect | Read: the paragraph now says what does NOT stay the same, names the three consumers and cites the round. `spec.md` §Scope 2 corrected in place. The class is not closed, which is finding 9 |
| 🟢 | round 1 finding 4 verified — the workflow reader | `tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments` | not a defect | Executed over the real file: four spellings found, including the `BASE:` assignment at `.github/workflows/hygiene.yml:291`, and the three flag shapes plus the range read correctly. `base_spellings` takes text, so the reader is driven rather than described. Finding 12 is its false-positive direction |
| 🟢 | round 1 finding 5 verified — the panel elision | `skills/verify/scripts/broad_gate.py#panel` | not a defect | Measured `seal_stamp.letter` at 23 columns and the constant, the comment's formula and the render agree. The elision keeps the tail and a ref that fits is untouched. Finding 13 is the prose left behind |
| 🟢 | round 1 finding 6 verified — the guard covers both steps | `skills/verify/scripts/broad_gate.py#resolve_base` | not a defect | Executed: `--base HEAD` resolves to `HEAD`, not to `origin/base` and not to `origin/HEAD`. A short SHA still reaches the fallback, so A9 is intact, and of the four remote-tracking refs here only `HEAD` is rejected by the guard, so nothing real narrowed |
| 🟢 | round 1 finding 8 verified — the spec's two disproved sentences | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | not a defect | Read: §Scope 2 and §Out corrected in place with the round and finding named, and `overview.md` §*Fed back into the spec* no longer reads `none`. Both corrections say what stays out of scope rather than only what was wrong |
| 🟢 | the record correction at `e68f64a9` verified | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/rounds/round-1.md` | not a defect | `9a6d4a35..da117184` is twelve commits, and the three commits it adds touch documents only, so `New units` and `Contract changes` are rightly unchanged. Correcting the cell by hand is what the skill asks for where `close` refuses to rewrite a reviewer's verdict |
| 🟢 | the three exemption rows may stand | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/survivors.md` | not a defect | Verified the mechanism: a path-and-quote row that matches nothing prints nothing and silences nothing, unlike a whole-range declaration, which is reported as unresolved. `sentences` does not strip an HTML comment, so the first row's quotation is in the corpus and the row has a live subject. Re-measured both ranges at the target SHA: exit 0 with no `--exempt` |
| 🟢 | the phase records render what is true now | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/phases/phase-4.md` | not a defect | Read both. The false sentence is inside the correction marker in phase 4 and the two superseded ones in phase 3; each file's rendered prose states the current fact above the marker. Phase 4's *Why the quotation stays* names something that renders nowhere, which a raw reader still sees |

## Paste-ready fixes

```python
def test_a_base_with_no_remote_counterpart_resolves_to_itself(tmp_path):
    """A8. A remote is present and the base is absent from it — the
    never-pushed branch. It resolves to the ref as given and `moved` is
    false, so nothing is printed about the resolution. What the consumers are
    HANDED still moves: `base.commit` is the ref's commit, where every check
    used to be handed `args.base` itself (round 1, finding 3)."""
    work = behind_clone(tmp_path)
    git(work, "switch", "-qc", "never-pushed", "base")
    mod = gate_module()
    base = mod.resolve_base(str(work), "never-pushed")
    assert base.ref == "never-pushed", f"resolved to {base.ref}"
    assert base.commit == short(work, "never-pushed")
    assert base.commit != base.ref, (
        "the consumers are handed the ref, so nothing about the run moved"
    )
    assert base.moved is False
```
```markdown
A repository with no remote resolves to itself, and the one thing that moves
there is the spelling the consumers get. The resolution lands on the ref as
given; the commit is what every check, the `Broad gate` cell and the
`NOT SEALED` line are handed, in that repository as in any other. That is
every gate fixture in the suite today and every user on a local-only tree.
```
```python
def names_a_branch(root, given):
    """True where `given` is a spelling a branch could have.

    Asked of git rather than of a pattern written here, because the rule this
    guards — which remote-tracking ref a BRANCH corresponds to — is meaningful
    only for a branch name, and git already owns what one is.
    `check-ref-format --branch` refuses `HEAD`, `HEAD~2`, `base@{u}` and
    `topic@{1}`, and accepts `base`, `release/v0.12.2` and a short SHA. The
    SHA being accepted is right: it is a legal branch name, and no ref exists
    for it, so it reaches the fallback either way.

    **It accepts `@{-1}`**, which is the one form the command expands rather
    than refuses. That spelling does name a branch, so step 1 firing for it is
    right; what is not right is `moved_line` then reading the runner's ref as
    `origin/@{-1}`, which names nothing. Measured on git 2.54.0.
    """
    return git(root, "check-ref-format", "--branch", given) is not None
```
```python
# The quoted value takes `+` rather than `*`: `--baseline ""` names no base,
# and an empty group 1 falls through to a group that did not participate, so
# the reader would hand its caller a `None` to match against.
BASE_ARGUMENT = re.compile(
    r"(?:--baseline|--range)\s+(?:\"([^\"]+)\"|((?:\$\{\{[^}]*\}\}|\S)+))"
)
```
```python
# A `#` line is not a step. The workflow explains its own flags in comments,
# and a flag quoted in prose is not a base a runner takes — reading one turns
# the pin red while the workflow is correct, which is the direction round 1's
# finding 4 asked the widening not to open.
YAML_COMMENT = re.compile(r"^\s*#")


def base_spellings(text):
    """Every revision `text` names as a base, as it spells it.

    Takes text rather than reading the file, so the reader itself can be
    driven over shapes the workflow does not happen to use today — round 1's
    finding 4 was that a reader nothing drives is a reader nobody can tell is
    partial.
    """
    found = []
    for line in text.splitlines():
        if YAML_COMMENT.match(line):
            continue
        for match in BASE_ARGUMENT.finditer(line):
            found.append(match.group(1) or match.group(2))
        environment = BASE_ENVIRONMENT.match(line)
        if environment:
            found.append(environment.group(1))
    return found
```
```python
    **A ref too long for the row says so.** `seal_stamp.letter` gives a value
    `PANEL_VALUE_WIDTH` columns and cuts at the frame with no marker, so the
    elision is made here instead and the TAIL is kept: for the `origin/<base>`
    a runner reads, the prefix is the part a reader can infer. Where step 1
    lands on a second remote the prefix is NOT inferable, and the line the
    gate prints is what names that ref in full — it fires whenever the given
    and resolved commits differ (`questions.md` W1, round 1 finding 5).
```
```markdown
The two baselines should move the same way — a baseline carried forward drops
the rows the base's own newer commits added — and that half is read rather
than executed. The survivor arm is the half that was measured, in both
directions.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_gate_asks_the_range_ci_will_ask.py -q`, in a clone at the target SHA | exit 0 — 31 passed |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q`, same clone | exit 0 — 121 passed |
| `evidence_check.py .` unscoped, same clone | exit 0 — 1370 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `bin/survivor-check --range 9a6d4a35...HEAD`, no `--exempt` | exit 0 — 58 sentences removed, none still standing |
| `bin/survivor-check --range origin/release/v0.12.2...HEAD`, no `--exempt` | exit 0 — 19 sentences removed, none still standing |
| probe — `resolve_base` over the A8 fixture, a clone whose remote has no such branch | `ref='never-pushed'`, `commit='cf0f708'`, `moved=False`. The children are handed the hash. Finding 9 |
| probe — `names_a_branch` over eleven spellings and over every remote-tracking ref in the clone | `@{-1}` accepted; `HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}` refused; of four remote-tracking refs only `HEAD` rejected. Findings 10 and the finding 6 confirmation |
| probe — `resolve_base` and `moved_line` with `--base @{-1}` on a clone whose previous branch tracks `origin/base` | resolved through step 1 to `origin/base`; the line says *not the origin/@{-1} a runner reads*. Finding 10 |
| probe — `seal_stamp.letter` over a 200-column value, against `PANEL_VALUE_WIDTH` and the comment's formula | all three give 23. Confirms finding 5's fix |
| probe — `base_spellings` over five workflow lines and over the real file | `--baseline ""` returns `[None]` and `SHELL_VARIABLE.match` raises `TypeError`; a commented flag is read as a base; the real file gives four spellings. Findings 11 and 12 |
| the broad gate — the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's one run, after the rounds settle (`agent-contract` §2). CI's `lint`, `ledger`, `release` and three `pytest` legs are green on this branch at the target SHA, which is a different act from that run |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | round 1's 1 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#moved_line` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#resolve_base` | round 1's 3 — fixed |
| round-1 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments` | round 1's 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#panel` | round 1's 5 — fixed |
| round-1 | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | round 1's 8 — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#gate` | round 1's 🟢 — not a defect |
| round-1 | `skills/code-review/scripts/chain_check.py#broad_gate` | round 1's 🟢 — not a defect |
| round-1 | `tests/test_the_gate_asks_the_range_ci_will_ask.py#says_what_the_base_resolves_to` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger.md` | round 1's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame by M1's own default |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default under this run's `Automation = yes`; already deferred in round 1 and not reopened here |
| widening `records_a_past_round` to exclude a work item's `phases/` records the way it excludes `rounds/` | a follow-up named in `survivors.md`'s first row and in `phases/phase-4.md` | a later work item. Already deferred by the fix pass as mechanism a fix pass may not add |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix; already deferred in round 1 |
