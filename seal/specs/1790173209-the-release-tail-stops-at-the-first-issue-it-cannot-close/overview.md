# the release tail stops at the first issue it cannot close — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the first goal, the fragment rule, the identifier rule, the merge table); `CONTRIBUTING.md` §*What a change to a gate must carry*; `docs/branch-and-release.md` §*Cutting a release*; `docs/release-checklist.md` §2, §3, §5, §6; `docs/issues-and-milestones.md` §*A milestone answers when*, §*A label answers what it is about*; `seal/specs/1790173209-…/routing.md`, `spec.md` (Grounding, Scope, S1–S16, Data & interfaces), `plan.md` (Phases 1–7, Alternatives), `questions.md` (the seven judgments, Q1–Q3); `seal/follow-up.md`; the seven tickets #536, #266, #289, #363, #362, #198, #157 with their comments
· evidence: rows P1, P1b, P1c, P2, P3, P4, P5, P6, P7 in `seal/ledger/1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close.md`; in `seal/ledger.md`, R1 (the timer rule) and S4 (the tracker document's statement of it) corrected, and T1, R3 (both), G5, C5, R5, R1-sizing, G6, F4, F1, F2, F6, G1, G3, the gather's two rows and the update skill's row re-read, each with a dated note
· verified: executed — every new case seen red at the commit before its fix and green after, the narrow module runs named per phase in `phases/phase-N.md`, 39 mutations across the seven phases each watched go red (four needed a case strengthened first, all four recorded), the `DRY_RUN=1` closer run against the previous release's inputs, the completeness gate's five-input measurement, `evidence-check --strict` exit 0 at every phase's close; read — the documents above and the tickets; unverified — the table below

## Why this work exists

Every one of the seven tickets was paid for by hand at the previous release —
a closer that died on the second issue, a gather that wrote a second heading,
a sweep that refused the version that had just shipped, an empty measurement
log nobody noticed, an update that reported success on a stale copy — and a
change to the release tail is met only at the next release, so this item
makes each one a case before that day.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S4's count of pull requests in the dry run | *the seven pull requests of that push* / the tracker answered six | the tracker's six, recorded | an aggregate in a frame is a claim, and the run is the measurement (`phases/phase-1.md`) |
| S10's fixture | *a tag `v0.1.0`* below the running `0.2.0`, offenders `0.2.0` and `0.3.0` / the case tags `v0.2.0` and expects `0.3.0` alone | the running version tagged | a tag below the running version changes no answer, so the spec's fixture could not go red; the case has to exercise the shipped set (`phases/phase-4.md`) |
| S12's count word | `plan.md`: *drop the superlative and the count*; `spec.md`: *both say … five* and *neither carries … a count* | no count word in either text; the table enumerates and the case asserts each name | the ticket's own grounds — a count rots the next time an input is added (`phases/phase-5.md`) |
| S8's red | *seen red with the fixture* / the reader's fixture case is green from its first run; the real-tree case was seen red against a duplicate heading planted in this repository's own file and restored from a kept copy | the real-tree case shown red | the real-tree case is the one that fails a release, so it is the one whose red matters (`phases/phase-3.md`) |
| Data & interfaces on `close_issue` | the close loop *no longer calls `run` … but a `close_issue`* / `close_issue` is built on a new `attempt`, and `run` keeps exiting for the reads | as built | `run` is what `arrived` and `gh_json` need; a read the run depends on should still exit, only one issue's close should not (`phases/phase-1.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| the REST fallback closing a real issue on the real tracker after a real GraphQL refusal — every case here fakes both routes, and the `DRY_RUN=1` run writes nothing by design | the repository owner, at the next release's close-issues run (the job log prints one line per fallback taken) |
| the empty-log sentences appearing on real issues — the roll's cases fake `gh`, and the live open log has comments today | the repository owner, at the next release's roll (the job log prints the line, and the closed log carries the comment) |
| whether GitHub acts on a closing keyword inside an HTML comment (`questions.md` Q1) — the shape stays unmasked until measured | a measurement on a scratch pull request into a scratch repository's default branch; not on this tracker (`questions.md` Q1) |
| why `gh issue close` refused #515 on the GraphQL route twice while REST closed it at once (`questions.md` Q3) — the fallback is built for the class, not the cause | a measurement, when somebody has a reproduction; the repository owner decides whether it is worth one |
| the full suite, `ruff check .` and `ruff format --check .` over the whole tree — the narrow runs per phase are in `phases/phase-N.md`, and the two ruff commands over the tree ran at the hand-back | the sealer, after the review rounds settle |

## Not done

The four-space indented block and the HTML comment stay unmasked (#266's
other two shapes), each with a case pinning the current reading and the
reason at the pattern. Making a missing `HEAD_BRANCH` loud in the
completeness gate (#362) was left, because no workflow produces that state.
The roll does not read the log's contents for a `Ran by` row (#198); a
comment count is what the tracker answers without parsing prose. The update
skill does not extract the stale directory itself (#157); it prints the
repair, because deleting a directory a live PID may hold is a person's act.
#368 was dropped as already shipped in `fc3e1175`; nothing here touches it.
The `1bafeb78` run's `Invalid revision range` failure is `arrived()`'s
documented force-push direction and a different class from #536; the frame
flagged it for the caller to file, and nothing here changes it.

## Fed back into the spec

*Inferred during implementation*, each written into the fragment row named:

- P1: an issue closed through the REST route whose comment could not be
  posted counts as closed, with the failure printed — the close is the act
  and the comment says why (the spec left the comment's failure unnamed).
- P2: a fence closes on its own delimiter (`\1`), so a backtick line inside a
  tilde fence does not end it; and the double-backtick span may hold a single
  backtick.
- P3: the date a second gather keeps is decided in `main`, so the dry run
  prints the heading the entries will join.
- P4: a checkout that can read no `v*` tag fails the sweep loudly, naming
  `fetch-depth: 0`; and a tag that is not version-shaped is dropped from the
  shipped set.
- P6: only a count of zero speaks; an unreadable count says only that it
  could not be read, on the job's output and on neither issue.
