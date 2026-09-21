# round 2 — the verifying round, the gate and CI ask about different ranges (#423)

Target SHA `e68f64a9ad19bd2a4ad96e41240bf919b39ceb6b`, base `release/v0.12.2`,
branch `fix/the-gate-and-ci-ask-about-different-ranges`. The surface is round
1's fix range `9a6d4a35..da117184`, twelve commits, plus the record correction
at `e68f64a9`. Reviewed in a `git clone --no-local` of this repository checked
out at the target SHA; the venv that runs the suite was built inside that
clone by the repository's own runner.

Round 1's coordinates were carried, not re-derived: every finding below was
opened at the place round 1 named, and the branch was not re-walked.

## What the fixes get right, so the one finding is read at its size

All eight of round 1's verdicts do what their cells say for the instance each
names, and I checked the code rather than the commit messages.

The resolver's guard is the deeper of the two candidate fixes. `names_a_branch`
asks git what a branch name is instead of writing a pattern, and both
resolution steps sit behind it rather than only step 1 — the builder's note
that guarding step 1 alone moved the defect to `origin/HEAD` is reproducible,
and the case asserts both halves. I checked the guard does not narrow anything
real: of the four remote-tracking refs in this clone, only `HEAD` is rejected,
and that is the rejection the fix is for.

The moved-line no longer speaks for CI about a remote no runner has, and the
opposite case pins that it still speaks for CI where the two agree, so the new
branch cannot be satisfied by never mentioning CI at all. The distance names
both of its ends.

`PANEL_VALUE_WIDTH` is right and its pin is real. `PANEL_WIDTH` is 36, the
frame takes 2 and the `"  {label:<8} "` prefix takes 11, which leaves 23 — the
constant, the comment's formula and what `seal_stamp.letter` actually renders
all agree, and I measured the third rather than recomputing the second.

The workflow reader now sees all four base-taking steps `plan.md` enumerates,
including the `BASE:` assignment at `.github/workflows/hygiene.yml:291`, and
`base_spellings` taking text is what lets the reader be driven over shapes the
file does not carry. That is the repair round 1's finding 4 asked for.

`e68f64a9` is a correct record repair: the three commits it adds to the fix
range touch documents only, so leaving `New units` and `Contract changes`
alone is right, and `9a6d4a35..da117184` is twelve commits.

## The findings

### 🟡 9 · two copies of *nothing about that run changes* are still standing

`tests/test_the_gate_asks_the_range_ci_will_ask.py:340`, and the body of pull
request #459.

Round 1's finding 3 was that *a base with no remote-tracking counterpart
resolves to itself and nothing about that run changes* is false: the
resolution does land on the ref as given, and what the consumers are handed
still moves from the ref to its commit. The fix pass corrected that sentence
in four places — `resolve_base`'s docstring, `spec.md` §Scope 2,
`changelog.md` and `overview.md` — and left two.

The first is the docstring of the case that is about exactly this state:

```
def test_a_base_with_no_remote_counterpart_resolves_to_itself(tmp_path):
    """A8. A remote is present and the base is absent from it — the
    never-pushed branch. It resolves to the ref as given, and `moved` is
    false, so nothing about that run changes."""
```

I built that fixture and ran the resolver over it:

```
A8 fixture — `--base never-pushed` in a clone whose remote has no such branch
  base.ref     = 'never-pushed'
  base.commit  = 'cf0f708'   <- what every child check, the Broad gate cell
                                and the NOT SEALED line are handed
  base.moved   = False       <- so no line prints
```

Before this branch the children were handed `args.base`, the string
`never-pushed`. So the run does change, in the one fixture the sentence is
written about. This is the copy a reader of the resolver opens first, because
it is the case they go to for what A8 means — and the fix pass edited this
function's body three lines below the sentence without touching it.

The second copy is pull request #459's own body: *A repository with no remote
resolves to itself and nothing about its run changes, which is every gate
fixture in the suite today.* The pronoun is `its` rather than `that`, which is
why a fix driven by grep over the corrected phrasing does not reach it. The
body is what a merger reads, and `CONTRIBUTING.md` §*What a change to a gate
must carry* is why the body carries these clauses at all — the fix pass did
update the same body for finding 1's direction clause, so this is one
statement missed rather than a channel nobody thought of.

The same body's verification section is stale in a smaller way: it reports
*one excused survivor with its grounds in `survivors.md`*, and there are now
three rows, none of which fires.

### ⬜ 10 · the guard's docstring is wrong about the one spelling git expands

`skills/verify/scripts/broad_gate.py#names_a_branch`

The docstring states that `check-ref-format --branch` *refuses `HEAD`, `HEAD~2`
and anything carrying `@{…}`*. Measured against git 2.54.0:

```
  'HEAD'        -> False      'topic@{1}'  -> False
  'HEAD~1'      -> False      'base@{u}'   -> False
  '@{-1}'       -> True
```

`@{-1}` is accepted, and it is the one form `--branch` exists to expand. The
behaviour that follows is arguably right — `@{-1}` does name a branch, so
taking its upstream is coherent — but the stated fact is false, and the line
the gate then prints is not:

```
broad-gate: --base @{-1} is 58f3fd5 in this checkout; this checkout says
@{-1} tracks origin/base, which is 591e305 — not the origin/@{-1} a runner
reads — origin/base is 1 ahead and 1 behind @{-1}. Every check below was
asked about origin/base.
```

`origin/@{-1}` is a ref nothing reads, so the sentence `moved_line`'s new
paragraph promises never to say — *it never says CI reads a ref CI does not
read* — is over-claimed by one degenerate spelling. `--base @{-1}` is a
stranger input than the `--base HEAD` round 1 graded ⬜, and the moved-line
still names the resolved ref correctly, which is why this is not higher.

The same line carries two em-dash clauses in one sentence in this filling.
`agents/sealer.md` has the sealer quote it verbatim into a report.

### ⬜ 11 · an empty quoted value yields `None`, and the caller raises rather than asserts

`tests/test_the_gate_asks_the_range_ci_will_ask.py#BASE_ARGUMENT`

The widening changed the quoted alternative from `[^"]+` to `[^"]*`, so a
`--baseline ""` matches with an empty group 1, and
`found.append(match.group(1) or match.group(2))` falls through to a group that
did not participate:

```
'            --baseline "" seal/specs/'  ->  [None]
  SHELL_VARIABLE.match over that result: TypeError: expected string or
  bytes-like object, got 'NoneType'
```

Nothing in `.github/workflows/hygiene.yml` spells a base that way, so this is
latent. What it costs when it fires is a `TypeError` inside a drift pin rather
than the assertion that pin exists to raise, which is the harder failure to
read.

### ⬜ 12 · the reader's false-positive direction moved one shape over

`tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings`

Round 1's finding 4 named both directions, and the report said so: widening
the reader had to avoid turning the case red on a workflow that is still
correct. The fix closed that for `$BASE` with `SHELL_VARIABLE`, and the two
new shapes reopen it a step over. Dropping the line anchor makes a flag inside
a YAML comment count, and `BASE_ENVIRONMENT` matches any line whose first
token is `BASE:` wherever it sits:

```
'  # --baseline "origin/${{ github.base_ref }}" is what we pass'
    ->  ['origin/${{ github.base_ref }}']
```

`test_the_gate_reaches_for_the_spelling_the_workflow_uses` then requires that
spelling to start with the remote-tracking prefix, so a comment explaining a
flag, or a `BASE:` variable added for something that is not a base, turns the
pin red while the workflow is right. Today the file carries one `BASE:` line
and three flags, all of them real, so nothing fires.

### ⬜ 13 · the panel keeps the argument phase 3 recorded as no longer arising

`skills/verify/scripts/broad_gate.py#panel`

`phases/phase-3.md`'s correction says of the accepted cut that *the argument is
not merely weaker, it is about a state that no longer arises*. The docstring
the correction is about still carries that argument in its first paragraph:
*a ref longer than that is cut here — which is why the line the gate prints
when resolving MOVED the answer is the authoritative statement and this row is
context*. The new paragraph under it says the opposite, and a reader meets the
superseded sentence first. `spec.md`'s affected-surface row for
`seal_stamp.letter` carries the same reasoning — *a longer ref is why the
authoritative statement is a printed line rather than a panel cell* — and that
one is paperwork.

The elision's grounds have a smaller version of the same problem. *`origin/` is
the part a reader can infer* holds for the `origin/<base>` the workflow reads,
and round 1's finding 2 established that step 1 can land on a second remote.
Where a fork's base and `origin`'s agree in commit, `moved` is false, nothing
prints, and a long `other/…` ref renders as its tail with the remote hidden —
which is the distinction the `from` row was added to make.

### ⬜ 14 · the baseline half of the direction claim lost its label

`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md`,
`plan.md` §*Operational impact*, `overview.md`

The replacement sentence is true and I checked both of its measured halves.
The clause that follows it — *the two baselines move the same way, a baseline
carried forward drops the rows the base's own newer commits added* — is the
half round 1's report labelled *read, not executed*. It is stated in all three
documents as flatly as the measured half, with no answerer named. `agent-
contract` §4 is the rule; the shared ledger's R3 row does keep the measured
half labelled `Executed`, so the distinction survives in one place and not in
the three a reader of the change meets.

## The three things the fix pass raised

**Is finding 3's class closed?** No — finding 9 above. For the other two facts
it is. Finding 1's direction claim has no fourth standing statement: I grepped
the tree for *blocks more*, *never less* and *at or ahead*, and what is left is
`docs/review-chain-spec.md`, which is a different change's failure direction,
plus `plan.md`'s own account of what it used to predict. The pull request body
was corrected for this one. Finding 4's *read as arguments, not as text* has
exactly two occurrences left — the quotation inside `phases/phase-4.md`'s
correction, and the `survivors.md` row that excuses it. The fix pass's own
survivor step is what found the third place, and it worked.

**Should the three exemption rows stand?** Yes. I checked the mechanism rather
than the argument. `survivor_check.py` reports an unresolved whole-range
declaration, so a declaration that quietly stopped applying is printed — but a
`| Path | Quote | Grounds |` row that matches nothing is simply silent, so a
dead row costs nothing and cannot drift into excusing something else, which is
what the header claims. I also confirmed the first row still has a live
subject: `sentences` does not strip an HTML comment, so the quotation inside
`phases/phase-4.md`'s correction marker is in the corpus and the row would fire
if the pair ever scored above the floor again. The CI half of the argument is
sound too — `actions/checkout` on a `pull_request` event holds the merge of the
head into the base, which the milestone step's own comment in the workflow
already relies on. Delete none of them.

One stale pin, not worth a row: the header says *as of `d656f4be`*, and it was
written at `da117184` with `e68f64a9` landing after. I re-measured at the
target SHA and the claim holds — both ranges are exit 0 with no `--exempt`.

**Do the corrected phase records render what is true now?** Yes, both. Phase 4's
false sentence is inside the correction marker and the rendered prose above it
states what the reader does; phase 3's two superseded sentences are inside its
marker and a new rendered paragraph says the cost did not stay open. One
loose end that does not need a fix: phase 4's rendered prose says *Why the
quotation stays* while the quotation it names renders nowhere, so a reader of
the rendered record meets a reference with no referent. A reader of the raw
file — which is how a `seal/specs/` record is read — sees both.

## Regression tests to plant

| What | Destination |
|---|---|
| the A8 case asserting that `base.commit` is the ref's commit rather than the ref, so the sentence in its docstring cannot come back untested (finding 9) | `tests/test_the_gate_asks_the_range_ci_will_ask.py` |

## Facts for the evidence ledger

- `seal_stamp.letter` gives a panel value 23 columns, measured by rendering a
  value nothing could fit. `PANEL_WIDTH` is 36, the frame takes 2 and the label
  prefix 11. R5 already anchors the elision; this is the number behind it.
- `git check-ref-format --branch` accepts `@{-1}` and refuses `HEAD`, `HEAD~1`,
  `base@{u}` and `topic@{1}`, measured on git 2.54.0. R1's claim that both
  resolution steps are asked only of a spelling that command accepts is true;
  what that set contains is what finding 10 is about.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 9 | 🟡 two copies of *nothing about that run changes* survive round 1's finding 3 | `tests/test_the_gate_asks_the_range_ci_will_ask.py:340` | open | Executed the A8 fixture: `base.ref` is `never-pushed`, `base.commit` is a hash, and the children are handed the hash where they were handed `args.base`. The fix pass edited this function's body three lines below the sentence. Pull request #459's body carries the same claim as *nothing about its run changes*, which the corrected phrasing does not grep |
| 10 | ⬜ `names_a_branch`'s docstring is wrong that `@{…}` is refused, and the line then names `origin/@{-1}` | `skills/verify/scripts/broad_gate.py#names_a_branch` | open | Measured on git 2.54.0: `@{-1}` accepted, `HEAD` `HEAD~1` `base@{u}` `topic@{1}` refused. `--base @{-1}` resolves through step 1 and the moved-line says *not the origin/@{-1} a runner reads*. Degenerate input; `moved_line`'s own promise is over-claimed by it |
| 11 | ⬜ `--baseline ""` yields `None` and the caller raises `TypeError` rather than asserting | `tests/test_the_gate_asks_the_range_ci_will_ask.py#BASE_ARGUMENT` | open | Executed: `base_spellings` returns `[None]`, `SHELL_VARIABLE.match` raises. The widening from `[^"]+` to `[^"]*` is what admits it. Nothing in the workflow spells a base that way |
| 12 | ⬜ the reader counts a flag inside a YAML comment and any `BASE:` line, so the pin can go red on a correct workflow | `tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings` | open | Executed over a commented flag: read as a base. Round 1's report named this direction for `$BASE` and the fix closed it with `SHELL_VARIABLE`; the two new shapes reopen it one step over. Latent — the file carries one `BASE:` line and three flags, all real |
| 13 | ⬜ the panel docstring keeps the accepting-the-cut argument phase 3 recorded as no longer arising | `skills/verify/scripts/broad_gate.py#panel` | open | Read. The first paragraph still says the cut is why the printed line is authoritative and this row is context; the paragraph under it says the ref now says it was cut. `spec.md`'s `seal_stamp.letter` row carries the same reasoning and is paperwork. The elision's stated grounds assume the prefix is `origin/`, which round 1's finding 2 disproved |
| 14 | ⬜ the baseline half of the direction claim is stated unlabelled in three documents | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | open | Read. Round 1's report labelled that half *read, not executed*; the three operational statements carry it beside the measured half with no label and no answerer. The shared ledger's R3 row does keep the measured half labelled `Executed` |
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

Every probe file and every repository a probe built was deleted before this
report was written (`agent-contract` §7). The clone is the review's own working
tree and outlives the report by design.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame by M1's own default |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default under this run's `Automation = yes`; already deferred in round 1 and not reopened here |
| widening `records_a_past_round` to exclude a work item's `phases/` records the way it excludes `rounds/` | a follow-up named in `survivors.md`'s first row and in `phases/phase-4.md` | a later work item. Already deferred by the fix pass as mechanism a fix pass may not add |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix; already deferred in round 1 |

## Paste-ready fixes

Finding 9, first coordinate — the A8 docstring.

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

Finding 9, second coordinate — pull request #459's body, replacing the
paragraph that begins *A repository with no remote resolves to itself*.

```markdown
A repository with no remote resolves to itself, and the one thing that moves
there is the spelling the consumers get. The resolution lands on the ref as
given; the commit is what every check, the `Broad gate` cell and the
`NOT SEALED` line are handed, in that repository as in any other. That is
every gate fixture in the suite today and every user on a local-only tree.
```

Finding 10 — the guard's docstring.

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

Finding 11 — the quoted alternative.

```python
# The quoted value takes `+` rather than `*`: `--baseline ""` names no base,
# and an empty group 1 falls through to a group that did not participate, so
# the reader would hand its caller a `None` to match against.
BASE_ARGUMENT = re.compile(
    r"(?:--baseline|--range)\s+(?:\"([^\"]+)\"|((?:\$\{\{[^}]*\}\}|\S)+))"
)
```

Finding 12 — skip comment lines.

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

Finding 13 — the panel docstring, replacing the two paragraphs after *The
`from` row is that missing half.*

```python
    **A ref too long for the row says so.** `seal_stamp.letter` gives a value
    `PANEL_VALUE_WIDTH` columns and cuts at the frame with no marker, so the
    elision is made here instead and the TAIL is kept: for the `origin/<base>`
    a runner reads, the prefix is the part a reader can infer. Where step 1
    lands on a second remote the prefix is NOT inferable, and the line the
    gate prints is what names that ref in full — it fires whenever the given
    and resolved commits differ (`questions.md` W1, round 1 finding 5).
```

Finding 14 — the clause in `changelog.md`, `plan.md` §*Operational impact* and
`overview.md`, replacing *The two baselines move the same way — a baseline
carried forward drops the rows the base's own newer commits added.*

```markdown
The two baselines should move the same way — a baseline carried forward drops
the rows the base's own newer commits added — and that half is read rather
than executed. The survivor arm is the half that was measured, in both
directions.
```

Needs a fix: yes — finding 9 (10 to 14 are ⬜, so none of the five counts)
Loses a record or crashes: no

## Proof block

Files opened, in this round, in a clone at the target SHA unless the finding
names the working tree:

- `skills/verify/scripts/broad_gate.py` — `git`, `moved_line`, `names_a_branch`,
  `resolve_base`, `panel`, `gate`, and the module docstring
- `skills/verify/scripts/seal_stamp.py` — `PANEL_WIDTH`, `letter`
- `skills/code-review/scripts/survivor_check.py` — `records_a_past_round`,
  `corpus`, `sentences`, `segments`, `blank_struck`, `exempted`, `report`
- `tests/test_the_gate_asks_the_range_ci_will_ask.py` — whole file
- `.github/workflows/hygiene.yml` — the three flag lines and the milestone
  step's `env:` block
- `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/` —
  `rounds/round-1.md`, `rounds/round-1-report.md`, `spec.md`, `plan.md`,
  `overview.md`, `changelog.md`, `questions.md`, `survivors.md`,
  `phases/phase-3.md`, `phases/phase-4.md`
- `seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md`
- `agents/sealer.md` §*The command*
- pull request #459's title and body
