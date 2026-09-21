# round 1 — the gate and CI ask about different ranges (#423)

Target SHA `327ef1f7e2b346569dda59004641ab11b7187e48`, base `release/v0.12.2`,
branch `fix/the-gate-and-ci-ask-about-different-ranges`. Reviewed in a
`git clone --no-local` of this repository checked out at that commit. There is
no earlier round to inherit from.

## What the branch gets right, so the findings below are read at their size

The repair itself holds. `resolve_base` does what `spec.md` §Scope 2 asks, in
the order `plan.md` argues for, and the fallback is genuinely three-deep. All
six consumers named in §*The class, enumerated by construction* take
`base.commit`, and the structural count is a real pin rather than a described
one — I parsed the file myself and `args.base` occurs once. The measured case
is reproduced end to end by a fixture that merges the remote base in, which is
the condition `survivor_check.py#parse_range` actually turns on. Both readers
of the `Broad gate` cell take `SHA_RE.findall(...)[0]`, which is the tree, so
the builder's claim that neither sees the base half move is correct — I read
both call sites rather than taking the sentence.

The four re-verified rows of `seal/ledger.md` hold, and I checked the claims
rather than the hashes. `draft_env` and its call site are byte-identical in
the diff. `seal`'s two-exit reading is unchanged and only the value handed to
`seal_record` moved. `not_as_written` is at line 1267, `resolve_base` at 1278
and the first `run` at 1312, so the refusal does still stand between the row
being read and the first shell. `agents/sealer.md` has one diff hunk, at line
54, and the absent-row paragraph this row is about sits at line 116 untouched.

The document pin is not vacuous. Exactly one block of `agents/sealer.md` and
exactly one block of `skills/verify/SKILL.md` carry both halves of the fact,
which I counted; the builder measured only the first of the two and the second
happens to hold as well.

## The findings

### 🟡 1 · the stated failure direction is wrong, and it is a required clause

`skills/verify/scripts/broad_gate.py#gate`, and the sentence in
`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md`

Three documents state a guarantee: *the gate blocks MORE, never less, because
the resolved base is at or ahead of the given one.* It is in `plan.md`
§*Operational impact*, in `overview.md`, and in the `changelog.md` fragment
that is gathered into the released file. `CONTRIBUTING.md` §*What a change to
a gate must carry* asks for a stated failure direction, so this is one of the
four clauses a gate change owes.

It is false, and the branch's own `spec.md` §*What is wrong* says so: *The
direction is not one-way … What is guaranteed is not a direction but a
disagreement.* I built the other direction and ran it. A base whose newer
commit DELETES wording, merged into the branch: under the stale spelling that
deletion falls inside the range and reads as wording this branch removed, so
the survivor arm refuses; under the resolved spelling the deletion is at the
base and the arm passes.

```
stale    (gate as it stood)   base       exit 1   2 sentence(s) the range removed
resolved (gate now)           9aa1595    exit 0   0 sentence(s) the range removed
```

The new answer is the right one — a deletion the base made is not this
branch's removal, and CI reaches the same verdict. What is wrong is the claim,
and it is the claim a reviewer of the next gate change will reason from. The
same reversal applies to `unverified-check --baseline` and to
`chain_check --baseline`: moving a baseline forward drops the rows the base's
own newer commits added, so those arms also see less. That half is read, not
executed.

### 🟡 2 · the printed line can assert something about CI that is not true

`skills/verify/scripts/broad_gate.py#moved_line`

The line says `CI reads {base.ref}`. `base.ref` comes from step 1 of the rule,
`<base>@{upstream}`, which can land on a remote that is not `origin`. Measured
on a clone whose `base` branch was retargeted to a second remote while
`origin/base` still existed:

```
broad-gate: --base base is ced5e4d in this checkout; CI reads other/base,
which is 715d933 — 1 ahead, 0 behind. Every check below was asked about
other/base.
```

CI does not read `other/base`. Every base-taking step of
`.github/workflows/hygiene.yml` spells `origin/${{ github.base_ref }}`, which
in that checkout is a different commit. The resolution order is a decided
question and I am not reopening it — `plan.md` §*Alternatives considered*
argues it from the fork case. What is not decided is the sentence: `agents/
sealer.md` tells the sealer to quote this line in its report, so a reader is
handed a false statement about what CI compared against, in the one place the
branch built for telling a fresh base from a stale one. `agent-contract` §14
is the rule — a change to what a person reads is pinned by a case, and the
case here pins a sentence that can be wrong.

### 🟡 3 · a repository with no remote is not left untouched

`skills/verify/scripts/broad_gate.py#resolve_base`, and the same sentence in
`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md`

`resolve_base`'s docstring, `spec.md` §Scope 2 and the changelog all say a
base with no remote-tracking counterpart *resolves to itself and nothing about
that run changes*, and the changelog adds *that is every fixture in the suite
today and every user on a local-only tree*. Measured on a repository built by
`git init` with no remote:

```
ref='base'  commit='ced5e4d'  moved=False
children are handed 'ced5e4d', where they used to be handed 'base'
```

The resolution lands on the ref as given; what every consumer is HANDED still
moves from the ref to its commit. In that repository the `Broad gate` cell
moves, which is the branch's own A3 divergence; `NOT SEALED <tree> against
<base>` moves from a branch name to a hash; `unverified_check.py#base_label`
quotes a hash back; and the panel gains a `from` row. So the sentence is
contradicted by the divergence table three files away, and the reader it
misleads is the local-only plugin user the changelog addresses by name.

### 🟡 4 · the drift pin reads three of the workflow's base spellings, not all of them

`tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments`

`BASE_ARGUMENT` is `r'^\s*(--baseline|--range)\s+"([^"]+)"'`. It requires the
flag at the start of a line and a double-quoted value. `phases/phase-4.md` and
the changelog claim more than that: *a base-taking step added later is covered
the day it is written*. I ran the pattern over six spellings.

```
SEEN    --baseline "origin/${{ github.base_ref }}" seal/specs/
UNSEEN  python3 x.py --baseline "${{ github.base_ref }}" seal/specs/
UNSEEN  --baseline ${{ github.base_ref }}
SEEN    --baseline "$BASE"
UNSEEN  BASE: ${{ github.base_ref }}
SEEN    --range "${{ github.base_ref }}...HEAD"
```

The third unseen form is not hypothetical. `.github/workflows/hygiene.yml:291`
already spells a base that way — `BASE: origin/${{ github.base_ref }}` — and
`plan.md` §*Technical context* counts that line as one of the four base-taking
steps. So the pin covers three of the four the plan itself enumerates, and the
most ordinary YAML spelling, the flag on the same line as the command, is
invisible to it. The fourth row is the other direction: refactoring a step to
`--baseline "$BASE"` turns the case red although the workflow is still
correct.

### 🟡 5 · the panel's `from` row is cut with no marker, and nothing prints beside it

`skills/verify/scripts/broad_gate.py#panel`

`seal_stamp.letter` gives a panel value 23 columns and cuts at the frame with
no ellipsis. `questions.md` W1's default relied on the printed line to carry
the full spelling, and the builder's own divergence row records that the line
prints only where resolving MOVED the answer — A4 requires silence otherwise.
So on an agreeing run a ref that does not fit is cut with nothing correcting
it. Rendered:

```
|  from     origin/release/v0.12.2 |
|  from     origin/release/2026-09-|
|  from     origin/feature/the-gate|
```

The second and third read as whole ref names. This repository's own release
refs are 22 columns and fit, which is why no case caught it —
`test_the_panel_names_the_ref_the_base_came_from` asserts `origin/base`, 11
columns, so the cut is never exercised. The whole point of the row is letting
a reader tell which ref the commit came from, and a silently truncated ref is
one they cannot check.

### ⬜ 6 · `@{upstream}` is appended to whatever the caller typed

`skills/verify/scripts/broad_gate.py#resolve_base`

Step 1 builds `{given}@{{upstream}}` from any revision expression, not only
from a branch name. `--base HEAD` therefore resolves to the CURRENT branch's
upstream rather than to HEAD. Measured on a clone sitting on `topic` with
`topic` tracking `origin/base`:

```
--base HEAD -> ref: origin/base  commit: ced5e4d  given_commit: ced5e4d
```

The two agreed in that fixture so nothing printed, but where the branch has
moved ahead the gate would compare against a ref the caller did not name.
`--base HEAD` is a degenerate input and the moved-line would fire in the
interesting case, which is why this is not higher.

### ⬜ 7 · the distance does not say ahead of what

`skills/verify/scripts/broad_gate.py#moved_line`

`— 1 ahead, 0 behind` names no subject. The reading that makes it true is
*the resolved ref is 1 ahead of the given one*, which is the nearer noun, but
the sentence does not say so and the two refs are both in it.

### ⬜ 8 · `spec.md` §Out still carries the sentence the branch proved false

`seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md`

A correction, located in the run's paperwork. §*Out, and why each* rules the
`Broad gate` cell out of scope on the grounds *The cell already names
commits*, which §Scope 3 contradicts and the branch overrode. `overview.md`
§*Fed back into the spec* says `none`. The divergence table is the right place
for the argument, and the spec is where a later round looks first — it is
currently a ratified-looking sentence that the tree disproves.

## Judging the six declared divergences

1. **Seven reads, not six.** Accepted. I parsed `broad_gate.py` myself: one
   occurrence of `args.base`. The seventh read was the refusal sentence, which
   quotes the spelling rather than consuming it, and `spec.md`'s table is
   headed *Consumer*. The count case asserting one is the stronger property.
2. **A3 did not hold whole.** The argument holds and I checked its load-bearing
   half rather than accepting it. §Out's sentence is true of the tree half and
   false of the base half: the old cell was `f"{tree} against {args.base}"`,
   which is a ref. §Scope 3 names the cell among the six that must take the
   resolved commit, so the two clauses of one spec disagreed and the branch took
   the one that repairs the defect. Both parsers read `named[0]`, verified at
   `chain_check.py:3530` and `round_record.py:4291`. The tests that write
   `against base` by hand are calling `round_record.py seal` directly and are
   unaffected. Accepted — with finding 8, which is that `spec.md` was not
   corrected.
3. **W1 answered more narrowly.** Accepted as a description of what was built,
   and finding 5 is the cost it leaves open.
4. **Two fillings.** Accepted. The second filling turns a former exit 2 into a
   run, which is a widening the ticket's shape supports, and the given spelling
   is still quoted in the refusal when all three steps fail.
5. **The document pin read through `ast.get_docstring`.** Accepted, and
   stronger than claimed: both remaining documents have exactly one qualifying
   block, so neither is vacuous.
6. **Four ledger rows re-verified.** Accepted, each claim checked against the
   new code rather than the hash — see the section above.

## Regression tests to plant

| What | Destination |
|---|---|
| the moved-line where `@{upstream}` is not `origin/<base>` and `origin/<base>` exists, asserting the line does not claim CI reads the other remote (finding 2) | `tests/test_the_gate_asks_the_range_ci_will_ask.py` |
| the panel `from` row over a ref longer than 23 columns, asserting the rendered line shows it was cut (finding 5) | `tests/test_the_gate_asks_the_range_ci_will_ask.py` |
| the workflow reader over a `--baseline` on the same line as its command, and over a `BASE:` assignment (finding 4) | `tests/test_the_gate_asks_the_range_ci_will_ask.py` |

## Facts for the evidence ledger

- The direction of the change is not one-way, measured: the survivor arm goes
  from exit 1 to exit 0 when the base's own deletion leaves the range. This
  belongs beside R3 in the work item's fragment rather than in the shared file.
- Both readers of the `Broad gate` cell take the first SHA-shaped word, read at
  `chain_check.py` and `round_record.py`. R2's note already states it; the
  coordinates above are what a re-reader should open.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the stated failure direction is wrong — the gate can allow MORE, measured | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md` | open | Probe: stale spelling exit 1, resolved exit 0, over a base whose own commit deleted wording. `spec.md` §*What is wrong* already corrects the direction claim; `plan.md` §*Operational impact* and `overview.md` carry the same false sentence. `CONTRIBUTING.md` §*What a change to a gate must carry* makes it a required clause |
| 2 | 🟡 the moved-line can assert `CI reads <ref>` about a ref CI never reads | `skills/verify/scripts/broad_gate.py#moved_line` | open | Probe on a clone with a second remote: the line named `other/base` while `origin/base` existed at a different commit. `agents/sealer.md` tells the sealer to quote this line in its report |
| 3 | 🟡 *nothing about that run changes* is false for a remote-less repository | `skills/verify/scripts/broad_gate.py#resolve_base` | open | Probe: children handed `ced5e4d` where they were handed `base`. The `Broad gate` cell, the `NOT SEALED` line, `base_label`'s quotation and the panel all move. The branch's own A3 divergence row is the same fact |
| 4 | 🟡 the drift pin reads 3 of the 4 base-taking steps `plan.md` enumerates | `tests/test_the_gate_asks_the_range_ci_will_ask.py#workflow_base_arguments` | open | Probe over six spellings: 3 unseen, including `BASE: origin/${{ github.base_ref }}`, which `.github/workflows/hygiene.yml:291` already uses. `phases/phase-4.md` and the changelog claim a later step is covered the day it is written |
| 5 | 🟡 the panel `from` row is cut at 23 columns with no marker and no line beside it | `skills/verify/scripts/broad_gate.py#panel` | open | Rendered a 32-column ref through `seal_stamp.letter`: `origin/release/2026-09-` reads as a whole ref. A4 means nothing prints beside it on an agreeing run. The case asserts an 11-column ref, so the cut is never exercised |
| 6 | ⬜ `@{upstream}` is appended to any revision expression, so `--base HEAD` resolves to the current branch's upstream | `skills/verify/scripts/broad_gate.py#resolve_base` | open | Probe on a clone sitting on `topic`: `--base HEAD` resolved to `origin/base`. Degenerate input, and the moved-line fires in the interesting case |
| 7 | ⬜ the distance reads `1 ahead, 0 behind` with no subject | `skills/verify/scripts/broad_gate.py#moved_line` | open | Read. Both refs are in the sentence and neither is named as the thing the counts are relative to |
| 8 | ⬜ correction — `spec.md` §Out still says the cell already names commits | `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md` | open | Located in the run's paperwork, so it owes no fix pass. `overview.md` §*Fed back into the spec* reads `none` while §Out carries a sentence phase 2 disproved |
| 🟢 | divergence 1 verified — `args.base` read once | `skills/verify/scripts/broad_gate.py#gate` | not a defect | Parsed the file: one occurrence. `spec.md`'s table is headed *Consumer*, and the count case asserts the stronger property |
| 🟢 | divergence 2 verified — the `Broad gate` cell's base half | `skills/code-review/scripts/chain_check.py#broad_gate` | not a defect | Both parsers take `SHA_RE.findall(...)[0]`, read at `chain_check.py:3530` and `round_record.py:4291`. §Out and §Scope 3 disagreed and the branch took the repairing side |
| 🟢 | divergence 5 verified — the document pin is not vacuous in either file | `tests/test_the_gate_asks_the_range_ci_will_ask.py#says_what_the_base_resolves_to` | not a defect | Counted the qualifying blocks: one in `agents/sealer.md`, one in `skills/verify/SKILL.md`. The builder measured only the first |
| 🟢 | divergence 6 verified — four re-verified ledger rows still hold | `seal/ledger.md` | not a defect | `draft_env` and its call site byte-identical; `seal`'s two-exit reading unchanged; `not_as_written` at 1267 still above `resolve_base` at 1278 and the first `run` at 1312; `agents/sealer.md` has one hunk at line 54 and the absent-row paragraph at 116 is untouched |

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

The decisive probe output, as it came back:

```
P1 STALE (gate as it stood)     spelling=base       exit=1
     survivor-check: examined 2 files at bf3d7b5, against 2 sentence(s)
     the range 9d68e3f..bf3d7b5 removed
P1 RESOLVED (gate now)          spelling=9aa1595    exit=0
     survivor-check: examined 2 files at bf3d7b5, against 0 sentence(s)
     the range 9aa1595..bf3d7b5 removed
       no removed wording is still standing
```

Every probe file and every repository a probe built was deleted before this
report was written (`agent-contract` §7).

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| M1 — whether a green gate can still meet a red CI because the base moved after the branch last took it in | `questions.md` M1, named as a standing limit in `spec.md` §*What this repair cannot see* | a measurement; already deferred in the frame by M1's own default |
| P1 — whether a refusal should survive anywhere in the gate | `questions.md` P1 | the repository owner. Answered by its default (a) under this run's `Automation = yes`, and not reopened here |
| the new fixtures on Windows and Linux | this branch's pull request | CI's matrix |

## Paste-ready fixes

Finding 1 — the direction sentence. The same replacement goes in all three
files; this is the `changelog.md` wording, and `plan.md` §*Operational impact*
and `overview.md` take the equivalent.

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

Finding 2 — the moved-line must not claim CI reads a ref CI does not read.

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

The same block closes finding 7: the distance now names both sides. The case
that pins it, seen red by reverting the branch above:

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

Finding 3 — the sentence about a repository with no remote. In
`resolve_base`'s docstring:

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

and the same correction in the changelog fragment:

```markdown
    **A repository with no remote resolves to itself, and the ONLY thing that
    moves there is the spelling the consumers get.** The resolution lands on
    the ref as given; the commit is what every check, the `Broad gate` cell
    and the `NOT SEALED` line are handed, in that repository as in any other.
    That is every fixture in the suite today and every user on a local-only
    tree, and it is why one assertion in the gate's own module reads a hash
    where it read a branch name.
```

Finding 4 — widen the workflow reader and correct what it claims.

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

and the claim, in `phases/phase-4.md` and in the changelog:

```markdown
  - **One case holds the gate's spelling against the workflow's**, from both
    sides. The workflow side is read as every revision the file names as a
    base — each `--baseline` and `--range` argument wherever it sits on the
    line, and each `BASE:` assignment — rather than as one substring search,
    so a base-taking step written in any of those three shapes is covered the
    day it is written. A step that names its base some fourth way is not, and
    that is the reach of the pin rather than a promise about all of them.
```

Finding 5 — elide the ref rather than letting the frame cut it. In `panel`:

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

`panel` does not import the stamp today, so its caller passes the width in, or
the constant is read the way `gate` already loads the module. The case, seen
red against the row as it stands:

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

Finding 6 — step 1 applies only to a local branch.

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

Needs a fix: yes — findings 1, 2, 3, 4 and 5 (6 and 7 are ⬜, and 8 is a correction in the run's own paperwork, so none of the three counts)
Loses a record or crashes: no

## Proof block

Opened and read: `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/`
— `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
`survivors.md`, `changelog.md`, `phases/phase-1.md` through `phase-5.md`;
`skills/verify/scripts/broad_gate.py`; `skills/verify/scripts/seal_stamp.py`;
`skills/verify/scripts/unverified_check.py` (`base_label` alone);
`skills/code-review/scripts/chain_check.py` (the cell reader and the verdict
vocabulary); `skills/code-review/scripts/round_record.py` (the seal path);
`tests/test_the_gate_asks_the_range_ci_will_ask.py`;
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the changed hunk);
`.github/workflows/hygiene.yml`; `agents/sealer.md`; `skills/verify/SKILL.md`;
`seal/ledger.md` (the four re-verified rows);
`seal/ledger/1789956662-the-gate-and-ci-ask-about-different-ranges.md`;
`CONTRIBUTING.md` §*What a change to a gate must carry*; `CLAUDE.md`;
`docs/review-chain-spec.md` §*A verdict row that commissions nothing* and
§*A finding located in a record is a correction*; `bin/test`; issue #423 and
its comment.

Run: the three commands and the six probes in §*Executed probes*, each exit
code read directly off the process and never through a pipe.
