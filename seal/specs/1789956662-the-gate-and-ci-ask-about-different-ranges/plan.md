# Implementation Plan: the gate and CI ask about different ranges (#423)

<!-- seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-21 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

The gate resolves `--base` once, before anything runs, to the ref CI will
read — the given ref's upstream where the checkout declares one, else
`origin/<base>`, else the ref as given — and hands that one commit to all six
consumers. Where resolving moves the answer it says so in one line and runs
anyway. It never refuses over a stale base, because a refusal stops an
unattended run and, after the resolution, the case a refusal was written for
gets the right answer instead.

## Technical context

**What the gate does today.** `skills/verify/scripts/broad_gate.py#gate`
reads `args.base` at six points: `broad_gate.py:1116` (the stamp's
`rev-parse`), `:1151` (`unverified-check --baseline`), `:1157`
(`chain_check --baseline`), `:1162` (`survivor-check --range <base>...HEAD`),
`:1175` (`compare_at_base`, which runs `git worktree add --detach <scratch>
<base>`), and `:1183` (`seal_record` → `round_record.py seal --baseline`).
None of them resolves anything; `git` is asked for a short SHA once, for
printing.

**What CI does.** `.github/workflows/hygiene.yml:162`, `:203`, `:255` and
`:291` all spell it `origin/${{ github.base_ref }}`. A runner's checkout has
no local branch, so this is not a choice the workflow made — it is the only
spelling that resolves there.

**Why the disagreement is conditional.**
`skills/code-review/scripts/survivor_check.py#parse_range` resolves `A...B`
through `git merge-base`. Where HEAD does not carry the base's newer commits
both spellings give the same merge base; they part once HEAD carries them,
which is what a merge from the base does. The measured case is recorded in
`seal/specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer/survivors.md`
§*The merge with `release/v0.12.0`*, whose own run of
`bin/survivor-check --range origin/release/v0.12.0...HEAD` reports the seven
places CI reported. That record is the evidence that resolving the base
reproduces CI's answer for the case the ticket opened on.

**Constraints the build has to respect.**

- Every gate fixture in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
  is built by `build_repo`, which runs `git init` and adds **no remote**. The
  fallback is what keeps that module green, and a fixture with a remote is new
  work.
- `seal_stamp.letter` renders a panel row as `"  {label:<8} {value}"` cut to
  `PANEL_WIDTH - 2` = 34 columns, so a value has 23. A ref longer than that is
  cut at the frame with no ellipsis.
- The `Broad gate` cell is parsed: `round_record.py seal` takes
  `chain.SHA_RE.findall(--broad-gate)[0]` as the tree's commit and refuses a
  cell with no SHA-shaped word; `chain_check.broad_gate` reads the cell again
  at the pull request. The cell's shape does not move in this work.
- The gate runs from a linked worktree in this repository's own flow.
  Remote-tracking refs and branch tracking config live in the common git
  directory, so `<base>@{upstream}` and `refs/remotes/origin/<base>` answer
  there the same as in the main checkout — claimed from reading git's layout,
  and A12 is the case that holds it.
- `agent-contract` §8: a probe that needs a repository drives git from Python,
  and the fixtures here already do.

**The failure scenario of the chosen approach, at six months.** A checkout
that has not fetched for a week resolves to a week-old remote-tracking ref and
seals green over it, exactly as today, while the panel now names a ref that
looks authoritative. The mitigation is that the ref is named at all: a reader
who doubts the seal has something to check, where today the panel shows a bare
SHA whose freshness nothing states. The alternative that closes it is fetching
inside the gate, which #423 refuses for an unattended run with no credentials.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Resolve to what CI reads, print where it moved, never refuse** | A remote-tracking ref nobody has fetched is still stale, and the gate cannot tell. The panel names the ref, so the doubt has somewhere to land | **chosen.** It closes the measured case, costs no interruption, and is the only direction compatible with `CLAUDE.md`'s first goal |
| Refuse when the remote-tracking ref is ahead, naming both SHAs and the distance | The refusal's only repair is `git fetch` followed by a re-run of a nine-minute gate — a human act standing in for the fetch the ticket refuses to automate. The sealer is a subagent with no way to ask, so the run stops with a report nobody is waiting on. And it fires on the ordinary case: a base moves by a sibling merge during every release | rejected as the whole answer; `questions.md` P1 is where the owner can bring it back. After resolution there is no wrong answer left for it to prevent |
| Resolve, and *also* refuse when the two are still far apart | Two mechanisms for one fact, and the threshold is a number nobody can derive. A distance that is safe on one branch is not on another | rejected. The distance is printed instead, and a reader who cares can act on it |
| Leave the gate alone and teach the sealer to pass `origin/<base>` | The prompt is where the rule would live, and `agent-contract`'s own preamble records what that costs: a rule kept in whoever last wrote a prompt goes missing without a trace. It also puts the resolution in the one party that opens no repository file | rejected |
| Change the workflow to match the gate | `github.base_ref` alone resolves to nothing on a runner. The workflow is the side that is already right | rejected |
| Fetch inside the gate | #423 §*Not this*: no credentials in an unattended run, and a check that moves refs to pass itself is a different problem | rejected by the ticket |
| A shared resolver every base-taking script imports | Three more interfaces change for no measured defect, and #423's comment measured that the gate is the one place a resolution difference seals something | rejected; the resolver stays private to the gate |
| Prefer `origin/<base>` over `<base>@{upstream}` | A clone whose base branch tracks a second remote — a fork with an upstream — would compare against the fork's stale copy, which is the defect class being repaired | rejected. `@{upstream}` is what this checkout says the base tracks, and `origin/` is the fallback because it is what a runner always has |
| Carry the ref name into every child check instead of the commit | The ticket's comment asks for the opposite property: *anything recorded as evidence names a commit, not a ref*. A ref re-resolves; a commit does not | rejected. The commit goes to the checks, the ref goes to what a person reads |
| Widen the `Broad gate` cell to carry the ref | Two parsers read that cell and one of them refuses on what it finds there. A gain of one word is not worth a second reader to keep in step | rejected; the stamp carries it |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The resolver, as a pure function in `broad_gate.py`: `(given spelling, resolved ref, resolved commit)`, with the three-step rule and the fallback. Nothing in `gate()` uses it yet | New cases for A8, A9, A12 and both halves of the rule, each seen red against the function's absence. A fixture builder that can add a remote and move it | b0b09908 |
| 2 | `gate()` resolves once and all six consumers take the resolved commit. `args.base` is read exactly once in the file | A1 and A2 end to end on a behind-base fixture, red against the gate as it stands. A3: `tests/test_the_seal_is_taken_once_by_the_sealer.py` green with nothing edited in it. A10 still green. The structural case counting the reads of `args.base` | c674ac26 |
| 3 | The gate says what it compared against: the panel's ref row, the moved-line, and the failure form's base | A4, A5, A6, A7 — each red when its branch is deleted (§14). A6 asserts the rendered panel, not only `panel`'s rows, because a value is cut at 23 columns | d1b6b757 |
| 4 | The drift pin: one case holding `broad_gate.py`'s base spelling against `.github/workflows/hygiene.yml`'s | A11, red when either side is edited to stop naming the remote-tracking ref. The shape is `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`'s structural half | 6a78a2ee |
| 5 | The documents and the records: `agents/sealer.md` §*The command*, `skills/verify/SKILL.md` §*The broad gate*, `changelog.md`, and the `seal/ledger/1789956662-*.md` fragment | The documents' own cases stay green; the ledger fragment's anchors resolve under `evidence-check --strict` | 42be239e |

Phase 1 delivers no behaviour change, which is deliberate: the resolver is the
part with the most cases and the least risk, and separating it is what lets
phase 2's end-to-end cases be about the routing rather than about the rule.

## Operational impact

- **Failure direction.** Each arm moves toward CI's answer, and that is **not
  one direction**. This row predicted *blocking more*, on the grounds that the
  resolved base is at or ahead of the given one; round 1 measured the other
  half and the prediction is corrected here rather than left standing.
  Wording the base itself removed leaves the range, so the survivor arm can
  pass where it used to refuse; the branch's replacement of base wording
  enters it, so the arm can refuse where it used to pass. The two baselines
  move the same way. `spec.md` §*What is wrong* already said so — what a stale
  base guarantees is a disagreement, not a direction — so the frame contained
  both claims and this row held the wrong one. The cheaper mistake is still
  this one: a gate that answers a question the merge is not judged by is worse
  than a gate that errs either way, because its stamp reads as a pass.
- **Prompt budget: zero.** No question is added to any session. The moved-line
  is printed and the run continues. This is the clause `CONTRIBUTING.md`
  §*What a change to a gate must carry* says a passing suite cannot report, so
  it is repeated in the pull request body.
- **No new dependency, no new env var, no migration.** The only external
  command added is `git rev-parse`, already used in this file.
- **Platform honesty.** `git rev-parse <ref>@{upstream}` and
  `refs/remotes/origin/<ref>` are git behaviour rather than OS behaviour, and
  the fixtures run on every matrix leg. Nothing here inspects processes or
  paths in a way that differs by platform.
- **A repository with no remote is unaffected**, which includes every fixture
  in the suite today and any consumer running this plugin on a local-only
  tree.
