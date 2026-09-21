<!-- seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The broad gate and CI ran the same five checks over one branch and asked
  them about different ranges** (#423). `broad-gate` built every child check's
  argument out of `--base` as the caller typed it, so a plain branch name
  resolved to the LOCAL ref, while every base-taking step of
  `.github/workflows/hygiene.yml` spells it `origin/<base>` — not a choice the
  workflow made, since a runner's checkout has no local branch. On 2026-09-16
  the local ref was one commit behind its remote: the gate reported two
  survivors, all excused, exit 0 and drew the stamp, and CI reported seven
  places and exit 1 on the same branch, the same check and the same commit.

  - **The base is resolved once, before anything runs, to the ref CI will
    read.** The given ref's upstream where the checkout declares one, else
    `refs/remotes/origin/<base>`, else the ref as given. The upstream comes
    first because a clone whose base branch tracks a second remote — a fork
    with an upstream — is the defect class being repaired, and reaching for
    `origin/` there would compare against the fork's stale copy.

    **A repository with no remote resolves to itself, and the one thing that
    moves there is the spelling the consumers get.** The resolution lands on
    the ref as given; the commit is what every check, the `Broad gate` cell
    and the `NOT SEALED` line are handed, in that repository as in any other.
    That is every fixture in the suite today and every user on a local-only
    tree, and it is why one assertion in the gate's own test module now reads
    a hash where it read a branch name.

  - **All six consumers take the resolved commit**, and the closure is
    structural rather than a list: `args.base` is read exactly once in
    `broad_gate.py`, at the resolution, and a case counts the reads. A seventh
    consumer written later cannot take the unresolved value in silence. The
    six are the panel's SHA, `unverified-check --baseline`,
    `chain_check --baseline`, `survivor-check --range`, the scratch worktree
    the base comparison checks out, and the `Broad gate` cell — whose base
    half used to be the ref as typed and is now the commit, which is the
    property #423's comment asks for: evidence names a commit, because a ref
    re-resolves.

  - **The gate says which base it compared against.** The stamp's panel gains
    a `from` row naming the ref beside the commit. Where resolving MOVED the
    answer one line names the given ref and its commit, the resolved ref and
    its commit, and how far apart they are, and the run continues; where the
    two agree, nothing extra prints. A given spelling that names no commit in
    the checkout at all — a clone that never made a local branch for its
    base — used to be exit 2 and now gets the same line's second filling.

    **It is not a refusal, and that was argued rather than assumed.** A
    refusal's only repair is a `git fetch` and a second nine-minute gate,
    performed by a person the sealer has no way to ask, and it would fire on
    the ordinary release case where a sibling merges while a branch is open.
    Prompt budget: zero.

    **Failure direction: each arm moves toward CI's answer, and that is not
    one direction.** Wording the base itself removed leaves the range, so the
    survivor arm can pass where it used to refuse; the branch's replacement of
    base wording enters it, so the arm can refuse where it used to pass. The
    two baselines should move the same way — a baseline carried forward drops
    the rows the base's own newer commits added — and that half is **read, not
    executed**. The survivor arm is the half that was measured, in both
    directions, and the repository owner answers whether the baseline half is
    worth a case of its own. What a stale base guarantees is a
    disagreement rather than a direction, and the argument for the change is
    that the resolved answer is the one the merge is judged by, not that it is
    the stricter one. The cheaper mistake is still this one: a gate that
    answers a question the merge is not judged by is worse than a gate that
    errs either way, because its stamp reads as a pass.

<!-- CORRECTED 2026-09-21 by work item 1789996775 (#464). What stood here:
"The two baselines move the same way — a baseline carried forward drops the
rows the base's own newer commits added." It is not false, and that is the
point: round 1's report labelled that half read rather than executed, and it
stood here beside the measured half with no label and no answerer, which
`skills/agent-contract/SKILL.md` §4 is the rule against. Round 2's finding 14
(`rounds/round-2-report.md`:195) names the three sites and its
§*Paste-ready fixes* carries this replacement; `seal/ledger.md`'s R3 row of
this work item is where the distinction survived. Corrected in place with the
issue named, never deleted silently: a record of a past state that quietly
becomes true is a record nobody can audit.

This fragment was gathered into `CHANGELOG.md` §0.12.2 before the correction.
`gather_changelog.py#ungathered` decides by marker and never by content, so
the gathered copy is not re-gathered and keeps the unlabelled sentence. That
divergence is Q1 of work item 1789996775 — the repository owner's row — and
it is disclosed in that work item's `overview.md` §*Not verified* and in
`seal/follow-up.md`. -->

    **It never fetches.** A remote-tracking ref is only as fresh as the last
    fetch, and that limit is named rather than closed — a check that moves
    refs to make itself pass is a different problem, and an unattended run may
    have no credentials. Naming the ref in the panel is what gives a reader
    somewhere to put the doubt.

  - **One case holds the gate's spelling against the workflow's**, from both
    sides. The defect was not a bug inside either file; it was two readers
    answering one question differently, each correct alone, with nothing in
    the tree comparing them. The workflow side is read as every revision the
    file names as a base — each `--baseline` and `--range` argument wherever
    it sits on the line, quoted or bare, and each `BASE:` assignment — rather
    than as one substring search, so a base-taking step written in any of
    those shapes is covered the day it is written. A step that names its base
    some other way is not, and that is the reach of the pin rather than a
    promise about all of them.

  - **The sealer's definition, `skills/verify/SKILL.md` and the gate's own
    docstring say which base**, and a case keeps each of them from taking the
    fact back. The gate's docstring is checked through the parsed module
    rather than the file, because the file also holds the constants naming the
    same refs and would otherwise answer for it — a check that cannot fail.
