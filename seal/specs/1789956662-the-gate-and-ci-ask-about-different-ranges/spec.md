# Feature Specification: the gate and CI ask about different ranges (#423)

<!-- seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## What is wrong, in the order the causes run

Two parties run the same five checks over one branch and hand them two
different ranges.

```
broad_gate.py:1162   --range f"{args.base}...HEAD"          the ref AS GIVEN
                     the sealer is given a plain branch name
                             ↓ so it resolves the LOCAL ref
                     release/v0.12.0         a35a3ea1
hygiene.yml:255      --range "origin/${{ github.base_ref }}...HEAD"
                             ↓ a runner has no local branch, so this is the
                               remote-tracking ref, always
                     origin/release/v0.12.0  58014fe4
```

On 2026-09-16 the local ref was one commit behind its remote. The gate
reported **2 survivors, all excused, exit 0** and drew the stamp; CI reported
**7 places, exit 1** on the same branch, the same check and the same commit.

**When the two spellings actually disagree, and it is narrower than the ticket
says.** `survivor_check.py#parse_range` resolves `A...B` through
`git merge-base`, so the range's start is the fork point and not the ref's
tip. Where HEAD does **not** carry the newer base commits, both spellings
produce the same merge base and the same answer. The answers part only once
HEAD already carries them — after a merge or a rebase from the base — and then
the stale spelling starts the range *before* those commits, so wording the
base already carried reads as **added by this branch** instead of as present,
and the branch's replacement of it is no longer a removal at all. That is
exactly the measured case:
`seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/survivors.md`
§*The merge with `release/v0.12.0`* records the merge, the seven places, and
the finding that all seven are the sibling's spelling of two ledger rows this
branch rewrote.

**The direction is not one-way, and the ticket's *can only narrow* is
corrected here.** The stale spelling gives a range that is wider in commits
and narrower in removals: wider, so the base's own deletions enter the range
and can be reported; narrower, so the branch's replacements of base wording
leave it. What is guaranteed is not a direction but a disagreement — the gate
answers a question the merge is not judged by. Read from
`survivor_check.py#parse_range` and from the record above; not executed here.

**It is worse than a stale ref because the stamp is drawn over it.** The
panel already records `base a35a3ea1`, so the evidence is right there and
still reads as a pass. `skills/verify/SKILL.md` §*The Seal Test* is about a
check that cannot fail; this is a check that passes because it was handed a
smaller question than the one that governs the merge.

**And the survivor arm is not the only consumer.** `gate()` hands `args.base`
to six places — the stamp's `rev-parse`, `unverified-check --baseline`,
`chain_check --baseline`, `survivor-check --range`, `compare_at_base`'s
scratch worktree, and `round_record.py seal --baseline`. Every one of them
inherits the same staleness.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The ticket's second direction is a refusal, and a refusal stops an unattended run. It is weighed against the resolving direction here rather than taken because the ticket named it |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | This changes a gate. The branch owes a test seen red, a stated failure direction, a prompt budget, and platform honesty — the prompt budget is the one a passing suite cannot report, and it is answered in the pull request body |
| `skills/verify/SKILL.md` §*The Seal Test* | The defect is a seal drawn over a question nobody asked. Nothing added here may make the stamp assert more than the gate measured |
| `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base* | The base comparison's whole purpose is *whose failure is this*. It is asked of the base the merge will use, or it is asked of nothing |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class — *every consumer of `--base` inside one gate run* — and it is enumerated below by construction rather than fixed at the survivor arm the ticket points at |
| `skills/agent-contract/SKILL.md` §14 | The stamp, the failure form and the refusals are what a person reads. Every changed sentence ships with the case that pins it |
| `skills/agent-contract/SKILL.md` §15 | Every case here is seen red first, against the mutation its phase names |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry and the evidence rows go in this work item's own fragments |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Three parties hold a base here — the sealer's `--base`, the checkout's remote-tracking ref, and the runner's `github.base_ref`. Every sentence says which |

## Scope

### In

1. **The base is resolved once, at one point in `gate()`.** Before any check
   runs, `--base` becomes a resolved commit plus the ref it came from. After
   that point `args.base` is read nowhere.
2. **The resolution rule reaches for what CI will read.** In order: the
   upstream of the given ref (`<base>@{upstream}`) where the checkout declares
   one; else `refs/remotes/origin/<base>`, which is the spelling
   `.github/workflows/hygiene.yml` uses literally; else the ref as given. A
   base with no remote-tracking counterpart — never pushed, a bare SHA, a
   fresh test repository — resolves to itself. **CORRECTED at round 1,
   finding 3**: this clause then read *and nothing about that run changes*,
   which is false. The resolution lands on the ref as given, and what the
   consumers are HANDED still moves from the ref to its commit — so that
   repository's `Broad gate` cell, its `NOT SEALED` line and the baselines
   the child checks quote back name a hash where they named a branch. A3
   below and `overview.md`'s divergence table said so from the first build,
   three files away from this sentence.
3. **Every one of the six consumers takes the resolved commit**, including
   the base comparison's scratch worktree and the cell `round_record.py seal`
   writes.
4. **The gate says what it compared against.** The panel names the ref beside
   the commit. Where resolving MOVED the answer — the given ref and the
   resolved ref are different commits — the gate prints one line naming both
   SHAs, the ref names and the distance, and runs anyway. Where they agree it
   prints nothing extra.
5. **The failure form says it too.** `NOT SEALED <tree> against <base>` is
   what a reader meets on a red run, and it carries the same base the panel
   would have.
6. **A structural case holds the gate's spelling against the workflow's**, so
   the two readers cannot drift apart again in silence. The precedent is
   `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, written
   for #354's identical shape — three readers grading one tree differently.
7. **The documents that describe the gate's base change with it** —
   `agents/sealer.md` §*The command*, `skills/verify/SKILL.md` §*The broad
   gate*, this work item's `changelog.md` and its `seal/ledger/` fragment.

### Out, and why each

| Out | Why |
|---|---|
| Fetching inside the gate | #423 §*Not this*. An unattended run may have no credentials, and a check that moves refs to make itself pass is a different problem |
| Refusing when the remote-tracking ref is ahead | The ticket's second direction, weighed and dropped — `plan.md` §*Alternatives considered* holds the argument, and `questions.md` P1 is the owner's chance to overturn it. After the resolution the case a refusal was for produces the right answer instead of a stopped run |
| Refusing on any divergence at all | #423 §*Not this*. A base legitimately behind is ordinary |
| Changing `.github/workflows/hygiene.yml`'s spelling | A runner's checkout has no local branch, so `origin/<base>` is the only thing that resolves there. The workflow is already right; the gate is what moved away from it |
| Making the gate reproduce CI's checkout | CI checks out the merge of the head into the base (`unverified_check.py#base_label` says so in its own docstring), and the gate runs over the working tree. A residual difference stays and is named below rather than closed |
| A shared base-resolver for `unverified-check`, `chain-check` and `survivor-check` run directly | #423's comment measured where this matters: *the gate's base is the one place where resolving differently actually changes a verdict*. Three more interfaces would change for no measured defect |
| The `Broad gate` cell's text | `chain_check.SHA_RE` reads the first SHA-shaped word out of it and `round_record.py seal` refuses a cell with none, so the cell's SHAPE does not move here. **CORRECTED at round 1, finding 8**: this row went on to say *The cell already names commits, which is the property #423's comment asks for*, and that is true of the tree half and false of the base half — the half the comment is about. The old cell was `f"{tree} against {args.base}"`, a ref. §Scope 3 names this cell among the six that must take the resolved commit, so the two clauses of this spec disagreed and the build took the repairing side; `overview.md` carries the argument and round 1 verified it at `chain_check.py:3530` and `round_record.py:4291`. What stays out of scope is WIDENING the cell to carry the ref as well |
| Instance 2 of #423's comment — a count taken before a range's last commit | Already answered in the tree, by the range row in work item `1789518345`'s `survivors.md`. It is a record convention, and it seals nothing |
| Instance 3 — a session polling `HEAD` while a checkout moved | No code in this repository is involved. It is in the ticket as evidence that this is a habit, not as work |
| `hooks/` | No hook reads a base. Nothing here reaches one |

## The class, enumerated by construction

Every read of `args.base` inside one gate run, found by reading `gate()` top
to bottom rather than by recalling them:

| Line | Consumer | What it asks the base | After this work |
|---|---|---|---|
| `broad_gate.py:1116` | `git rev-parse --short <base>^{commit}` | the SHA the stamp and the cell print | reads the resolved commit |
| `broad_gate.py:1151` | `unverified_check.py --baseline` | rows that left the unverified record | reads the resolved commit |
| `broad_gate.py:1157` | `chain_check.py --baseline` | the round records this branch added | reads the resolved commit |
| `broad_gate.py:1162` | `survivor_check.py --range <base>...HEAD` | wording this branch removed | reads the resolved commit — the arm #423 measured |
| `broad_gate.py:1175` | `compare_at_base` → `git worktree add --detach <scratch> <base>` | `new` against `failing on base too` | reads the resolved commit |
| `broad_gate.py:1183` | `seal_record` → `round_record.py seal --baseline` | the cell, and the commit it is judged against | reads the resolved commit |

**The closure is structural, not a list.** After phase 2 the string
`args.base` occurs exactly once in `broad_gate.py` — at the resolution — so a
seventh consumer written later cannot take the unresolved value without that
single read being duplicated. The case that pins the count is what makes the
enumeration hold; the table above is what it is derived from.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given a repository whose local `base` is one commit behind `origin/base`, and a branch that has merged `origin/base` in, when `broad-gate --base base` runs, then every check is handed the commit `origin/base` names | a case reading the kept output files' `$ ` command lines, red against the gate as it stands, where they carry the local SHA |
| A2 | The same repository, when the survivor arm runs, then it reports what `survivor-check --range origin/base...HEAD` reports and not what the local spelling reports | a case whose fixture plants one sentence the branch replaced at the merge; red today, because that replacement is not a removal in the stale range |
| A3 | Given a repository with **no remote at all** — every fixture in `tests/test_the_seal_is_taken_once_by_the_sealer.py` — when the gate runs, then its behaviour, its exit code and its panel are what they are today | the existing module stays green with nothing edited in it; this is the *nothing else moved* half |
| A4 | Given a base whose remote-tracking ref exists and names the same commit, when the gate runs, then nothing extra is printed | a case asserting the absence of the moved-line, so the line cannot become one that prints on every run |
| A5 | Given the behind-base repository of A1, when the gate runs, then one line names the given ref and its SHA, the resolved ref and its SHA, and how many commits apart they are | a case asserting all four values in the line, red when the branch that prints it is deleted (§14) |
| A6 | Given any successful run, when the stamp prints, then the panel names the ref the base came from beside the commit | a case over `panel` and over the rendered output, since `seal_stamp.letter` cuts a value at the frame and a truncated ref is a ref nobody can read |
| A7 | Given a failing check on the behind-base repository, when the gate prints `NOT SEALED`, then the base in that line is the resolved commit | a case over the failure form, red today |
| A8 | Given `--base` naming a ref with no upstream and no `origin/` counterpart, when the gate runs, then it resolves to the given ref and says nothing about resolution | a case with a remote present but the base absent from it — the never-pushed branch |
| A9 | Given `--base` naming a bare commit SHA, when the gate runs, then it is used as given | a case; `<sha>@{upstream}` and `refs/remotes/origin/<sha>` both fail to resolve and neither may abort the run |
| A10 | Given a base that does not resolve at all, when the gate runs, then it exits 2 with nothing run and the message names the spelling the caller typed | the existing `test_a_base_that_does_not_resolve_is_refused_with_nothing_run` stays green, and the message still quotes `args.base` rather than a resolution of it |
| A11 | Given `.github/workflows/hygiene.yml` and `broad_gate.py`, when the suite runs, then a case holds the gate's base spelling against the workflow's | a structural case, red when either side is edited to stop naming the remote-tracking ref |
| A12 | Given the gate run from a linked worktree, when it resolves the base, then it reads the same remote-tracking refs the main checkout does | a case run from `git worktree add`; remote-tracking refs and branch tracking config live in the common git directory, and the claim is worth a case because the sealer runs from a worktree in this repository's own flow |

**A3 is the one that can come back inconvenient.** It asks for *no other
change*, and it is a measurement over this tree rather than a property of the
rule: every gate fixture today is a repository with no remote, so the fallback
is what keeps ninety-odd cases green. If a fixture's reading moves, that is a
divergence row in `overview.md` with the fixture named — not a reason to
weaken A3.

## Data & interfaces

| Coordinate | What changes |
|---|---|
| `skills/verify/scripts/broad_gate.py` | gains one resolver and one value holding the given spelling, the resolved ref and the resolved commit |
| `skills/verify/scripts/broad_gate.py#gate` | resolves once; every check call site takes the resolved commit; prints the moved-line where the resolution moved |
| `skills/verify/scripts/broad_gate.py#panel` | a row naming the ref the base came from |
| `skills/verify/scripts/broad_gate.py#seal_record` | its `base` argument is the resolved commit; its signature and the cell's shape are unchanged |
| `skills/verify/scripts/broad_gate.py#compare_at_base` | unchanged in source; its caller hands it the resolved commit |
| `skills/verify/scripts/seal_stamp.py#not_sealed` | unchanged in source if the caller passes the resolved base; changed only if the line's wording moves, and then with its case |
| `skills/verify/scripts/seal_stamp.py#letter` | unchanged. `PANEL_WIDTH` is 36 and the label field is 8, so a panel value is cut at 23 columns — `origin/release/v0.12.0` is 22 and fits, and a longer ref is why the authoritative statement is a printed line rather than a panel cell |
| `agents/sealer.md` §*The command* | the three outcomes gain what the gate now says about the base |
| `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base* | states which base the comparison is against |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | the new cases, and a fixture builder that can give a repository a remote |
| `.github/workflows/hygiene.yml` | **unchanged**, and held against the gate by A11 |

## What this repair cannot see

Stated here so nobody reads the change as wider than it is.

- **A remote-tracking ref is only as fresh as the last fetch.** The gate does
  not fetch and will not, so a checkout that has fetched nothing for a week
  still compares against a week-old base. What changes is that the panel and
  the line name the ref, so a reader can ask; what does not change is that the
  gate cannot answer it.
- **CI judges a different tree.** `actions/checkout` on a `pull_request` event
  checks out the merge of the head into the base, and the gate runs over the
  working tree. Where the base moves after the branch last took it in, the two
  trees differ and a green gate with a red CI is still reachable. That is
  `questions.md` M1, and this work does not close it.
- **A base branch with local commits that were never pushed** now compares
  against the remote's tip, which is what CI will do and is not what the local
  branch says. This repository's release branches move by merged pull request
  alone, so the case has no instance here.
- **Nothing outside the gate is resolved.** `bin/survivor-check`,
  `bin/unverified-check` and `chain_check.py` typed by hand still take the ref
  a person writes.

## Open questions → questions.md

One row needs a person: whether dropping the ticket's refusal direction
outright is the answer the owner wants, or whether a refusal should survive
for the case resolving cannot close. Two rows are measurements and two belong
to the work. None of them stops the build — this run is declared
`Automation | yes`, and every row carries the assumption the build proceeds
under.

Framed 2026-09-21 by framer, before the build.
