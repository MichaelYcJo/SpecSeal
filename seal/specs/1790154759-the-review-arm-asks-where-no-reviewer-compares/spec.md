# Feature Specification: the review arm asks where no reviewer compares

<!-- seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/spec.md
Frames MichaelYcJo/SpecSeal#518. Record language: English (`seal/config.md`
has no `Record language` row). -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | A design that stops to ask is the more expensive one, and the difference has to be argued. Here it is argued with a measurement rather than assumed in either direction |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Four things are owed: a test seen red, a stated failure direction, a prompt budget, platform honesty. This work changes no verdict, so the direction is *neither more nor less* and the budget is *unchanged*; both still get said |
| `docs/review-chain-spec.md` §*commit-review-gate* › *Review arm* | The review arm's decision table. It has no row about which paths a change touches, and nothing next to it says that is deliberate |
| `docs/review-chain-spec.md` §*commit-review-gate* › *Parity arm* | The parity arm's row *the change confined to `docs/`, `seal/` → silent*, with its reason: nothing there can be compared against an original |
| `skills/implement/orchestration.md` §*Orchestrator: how the work is routed*, the wake/quiet table | Says the parity arm wakes only outside `docs/` and `seal/`. Says the review arm wakes when `seal/` exists, and does not say that this holds whatever the change touches |
| `skills/implement/orchestration.md`, same section: *Work that was never headed for a reviewer — a release chore, a documentation pass — declares `straight to the PR`* | The lighter tier the issue asks for already exists. It is chosen per work item by the person answering the routing batch, not inferred from paths |
| `skills/code-review/scripts/chain_check.py` module docstring, row *no declaration at all → pass, with a notice* | Answers the issue's open question 4 by reading: a pull request with no declaration already passes at CI |
| Issue #518 §*What not to do — exempt by branch name* | A branch prefix is a claim, not evidence. No design here reads a branch name |

## Scope

**In one line: the commit gate's review arm keeps asking on a change confined
to `docs/` and `seal/`, and this work writes down why — the measurement, the
decision, and a test that fails if the parity arm's path line ever leaks into
the review arm.**

The issue asks whether the review arm should draw the line the parity arm
draws. The measurement below says no. The two arms ask different questions:

- **The parity arm asks whether the original was consulted.** A `docs/` file
  has no original, so there is nothing to compare, and silence there is right.
- **The review arm asks whether anybody reads this before it lands.** In this
  repository `docs/` is the policy the code conforms to, and `seal/ledger.md`
  is the verified evidence. The measurement found real defects in both.

So the observable behaviour of the gate does not change. What changes is that
the asymmetry stops being implicit. Today a reader who finds `touches_code`
beside the review arm can take the missing call for an oversight, as the issue
did. After this work, the review arm's table, the wake/quiet table and the
hook itself say the review arm has no path line and why, and a test fails if
one is added.

**In:**

1. `docs/review-chain-spec.md` §*Review arm*: a row stating that a change
   confined to `docs/` and `seal/` is judged like any other change, with the
   parity arm's row named as the contrast, and a short paragraph carrying the
   measurement's result (M1 to M4 below, condensed) as the grounds.
2. `skills/implement/orchestration.md`, the wake/quiet table: the review arm's
   *Wakes when* cell says it wakes whatever the change touches, `docs/` and
   `seal/` included.
3. `hooks/commit-review-gate.py`: the `touches_code` docstring and the comment
   above `DOC_ROOTS` say the line is the parity arm's alone and point at the
   `docs/` section. Comments only. No code path changes.
4. A test beside `test_parity_gate_ignores_document_only_commits` in
   `tests/test_chain_hooks_hardening.py`: in a repository that opted in, with
   no declaration, no review mark and no waiver, a commit confined to `docs/`
   is stopped by the review arm. It is seen red by adding
   `and touches_code(cwd, invocations)` to the review arm's condition.
5. A test that pins the new `docs/` row's sentence, seen red by deleting it.
6. The work item's changelog fragment, ledger fragment and closing memo.

**Out, one line each:**

- **A lighter tier chosen by paths.** Refused by the measurement: review of
  `docs/` and ledger content finds defects there (M3, M4). No docs/seal-only
  change ever reached a reviewer (M1), so the seventeen that did not were
  never measured either way; thirteen of them touch `docs/flow.md`, which was
  retired on 2026-09-11 (`d851bd14`). No docs/seal-only commit has landed on
  the release branch since. *(Corrected 2026-09-23 in round 1's fix pass: this
  line said the only docs/seal-only changes that reached a reviewer produced
  defects, and M1 says none reached one.)*
- **An exemption by branch name.** The issue rules it out.
- **A shared path list for the gate and CI** (the issue's questions 2 and 3,
  and #506's complaint about hand-kept enumerations). With no tier there is no
  second list to keep in step. `DOC_ROOTS` stays the parity arm's own line.
- **Anything in `chain_check.py`.** Its *no declaration → pass, with a notice*
  row already answers the issue's question 4.
- **The fold's own routing** (#517's item 3, whether the last step of a fold
  runs as a no-work-item change). That is #517's design question, and this
  work's result is an input to it rather than an answer.
- **Both READMEs.** `README.md`'s `commit-review-gate` row names no paths and
  stays true, so neither edition moves. If a phase finds otherwise, both move
  together.
- **Changing the parity arm.** Its line is correct for the question it asks.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given a repository with `seal/` and no `routing.md` naming the branch, no review mark at HEAD and no waiver, when a commit carries only `docs/policies/note.md`, then the review arm stops it exactly as it stops a code change | the new case in `tests/test_chain_hooks_hardening.py`, shown red with `and touches_code(cwd, invocations)` added to the review arm's `if` |
| A2 | Given the same repository with `seal/parity.md` as well, when the same docs-only commit is typed, then the parity arm stays silent and the review arm asks — one arm, not two | the same case, or its sibling, asserting the ask names `[no-review]` and not `[no-parity]` |
| A3 | Given the same docs-only commit on a branch whose `routing.md` says `straight to the PR`, then the gate is silent | existing cases cover a declaration silencing the arm (`tests/test_routing_is_recorded.py`, `tests/test_waiver_decided_at_start.py`, read by name only); none stages a docs-only change under one. The phase decides whether a docs-only variant adds anything, and cites the existing case if it does not |
| A4 | A reader opening `docs/review-chain-spec.md` §*Review arm* finds a row for a change confined to `docs/` and `seal/`, and the reason the review arm does not share the parity arm's line | a case asserting the row's sentence, shown red by deleting it |
| A5 | A reader opening the wake/quiet table in `skills/implement/orchestration.md` sees that the review arm wakes whatever the change touches | read, and the same pinning case if the phase judges the cell worth one |
| A6 | Nothing the gate decides changes: every existing case in the two gate test files passes unchanged | executed by the phase: `tests/test_chain_hooks_hardening.py` and `tests/test_gate_judges_the_repo_it_commits_to.py` |

## Data & interfaces

None. No schema, file format, hook output or verdict changes. The ledger row
`S11` in `seal/ledger.md` already claims *a commit confined to `docs/` and
`seal/` leaves the parity arm asleep*; this work's fragment adds the other half,
that the review arm has no such line, anchored on
`hooks/commit-review-gate.py#judge`.

**The four things `CONTRIBUTING.md` asks of a gate change:**

- **A test seen red** — A1 and A4, each by the mutation named in its row.
- **Failure direction** — neither. The gate blocks and allows exactly what it
  did before.
- **Prompt budget** — unchanged, zero added. A docs-only commit with no
  declaration meets the one question it met before, and a declared work item
  meets none.
- **Platform honesty** — no process inspection and no new shell construct.

## The measurement the issue asked for

Issue #518 says one number has to be taken before any line is drawn: how many
review rounds on docs/seal-only changes found a real defect. It was taken from
the tree on 2026-09-23 against `origin/release/v0.14.0` at `f8f1c9de`, by three
scripts that read `git log` and the round records' `## Verdicts` tables. Every
figure below is **executed** unless it says otherwise.

**M1. No reviewed work item was ever confined to `docs/` and `seal/`.** Of the
88 work items with a round record on the release branch, the commit that added
each one's `round-1.md` touched a path outside those two roots in all 88. The
one apparent exception, `1788184145-the-gate-stops-the-session-editing-its-tests`,
is a pre-squash commit that recorded a round separately from the code it
reviewed, and that round's findings sit in `agents/`.

**M2. The seventeen docs/seal-only commits were never reviewed.** Of 175
non-merge commits on the release branch, 17 are confined to `docs/` and
`seal/`, the same count the issue took from `main`. None of them added a round
record. Thirteen of the seventeen touch `docs/flow.md`, which no longer exists
in the tree. Four touch `docs/one-root-by-lifetime.md` and its Korean edition,
the design record for the document roots.

**M3. The nearest thing to a docs/seal-only item is the second fold, and its
review found real defects in every round that had fixes.**
`1790119502-four-shipped-work-items-wait-unfolded` (#514, squashed as
`f2943c04`) changed `docs/`, `seal/` and four test files. Its three rounds
opened seven findings a later round verified as fixed, and all seven are
located in `docs/`:

| Round | New findings fixed | Severity | Where |
|---|---|---|---|
| 1 | 4 | one 🔴, one 🟡, two ⬜ | `docs/branch-and-release.md`, `docs/the-evidence-ledger.md`, `docs/the-agent-set.md`, `docs/review-chain-spec.md` |
| 2 | 3 | one 🟡, two ⬜ | `docs/review-chain-spec.md`, `docs/release-checklist.md`, `docs/branch-and-release.md` |
| 3 | 0 | — | verified the fixes |

The 🔴 was a folded policy sentence that gave three release acts to the tag
push when two of them fire on the merge to `main`. That is the defect the issue
predicts for a fold: *whether a folded sentence is true lives entirely in
`docs/`*.

**M4. Across every round record, a fixed finding located only in `docs/` or
`seal/` is common.** 279 round records carry a `## Verdicts` table. Of their
fixed, non-🟢 findings, those whose every cited location is under one root:

| Location | Fixed findings |
|---|---|
| a shipped path (`skills/`, `agents/`, `hooks/`, `templates/`, `bin/`, `.claude-plugin/`) | 372 |
| elsewhere outside the two roots (`tests/`, `.github/`, `README.md`, …) | 278 |
| `docs/` only | 25 |
| `seal/ledger.md` or `seal/ledger/` only | 26 |
| `seal/` otherwise — the work item's own records | 48 |
| `docs/` and `seal/` together | 2 |

The 25 `docs/`-only findings come from 14 different work items. The counts are
a lower bound: a finding whose Location cell cites no backticked path is not
counted, and neither is a verdict other than `fixed`.

**What the measurement decides.** The number the issue asked for is not zero,
and it is not small where it matters. When review reads `docs/` and the
ledger it finds defects there: at least 25 and 26 fixed findings (M4), and
#514's fold, the nearest thing to a docs/seal-only item, had all seven of its
fixed findings in `docs/` (M3). No docs/seal-only change ever reached a
reviewer (M1), so the seventeen commits of M2 were never measured either way.
A line drawn at `docs/` and `seal/`, the parity arm's line, would stop asking
exactly where the reviewed findings sit, on the strength of a population
nobody measured. The measurement refuses that line. *(Corrected 2026-09-23 in
round 1's fix pass: this paragraph said every docs/seal-only change that
reached a reviewer produced defects and that the unreviewed ones measured
empty; M1 says none reached one, and an unreviewed commit measured nothing.)*

**How the numbers were taken, so they can be re-taken.** M1: for every
`*/rounds/round-1.md` added on the release branch, the paths of the commit
that added it. M2: every non-merge commit on the release branch whose paths all
start with `docs/` or `seal/`. M3: `f2943c04`'s paths, and the `## Verdicts`
tables of `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/rounds/round-{1,2,3}.md`,
which are still in the tree. M4: the last version of every `round-N.md` ever
added on the release branch, its `## Verdicts` rows whose Verdict cell holds
`fixed` and whose severity is not 🟢, classified by the backticked paths in the
Location cell. The scripts were scratch probes and were not kept.

**The issue's four open questions, answered from the tree:**

1. *Which paths* — none. See the decision above.
2. *Where the list lives* — nowhere, because there is no list.
3. *Whether `DOC_ROOTS` becomes that list* — no. It stays the parity arm's
   line, and the comment above it says so.
4. *What `chain_check` does with a pull request that has no declaration* — it
   passes with a notice (`chain_check.py` module docstring, read). A person who
   wants the lighter tier for a docs pass declares `straight to the PR`, which
   CI requires nothing for.

## Open questions → questions.md

Framed 2026-09-23 by framer, before the build.
