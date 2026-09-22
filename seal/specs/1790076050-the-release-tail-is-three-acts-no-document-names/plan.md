# Implementation Plan: the release tail is three acts no document names

<!-- seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/plan.md
     HOW, in phases. This is the Design Gate's artifact. -->

Approved 2026-09-22 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

Four vertical slices, in the order the release performs them, plus the
fragments. Each of the first four ends with something a case can run.

The work is three tickets at one address: the acts a release performs after
the tag. Two of them become workflows, one becomes a reported command behind a
checklist box, and every one of them gains the sentences the documents never
carried.

## Technical context

What this builds on, all of it read rather than executed:

- `.github/workflows/close-issues-on-release.yml` — `on: push: branches:
  [main]`, `permissions: contents: read, issues: write`, two steps, both
  `python3 .github/scripts/<name>.py` with `GH_TOKEN`/`REPO` in `env:`. The
  shape phase 4's new step copies.
- `.github/scripts/label_merged_on_release_branch.py#existing_labels`,
  `#label_description`, `#main` — the repository already creates a label on
  the tracker from a workflow, reads the whole label list rather than one
  name (because the name carries a space and a colon), and derives the
  description from what a person needs to read on the tracker. Phase 4's
  script is this, generalised over a declared set.
- `.github/scripts/close_issues_on_release.py#main` — the loop that closes
  each issue a shipped pull request claimed, with a `DRY_RUN` arm and a
  404-tolerant read. Phase 4 adds the label removal inside this loop.
- `.github/scripts/gather_changelog.py` — already parses `CHANGELOG.md`'s
  `## X.Y.Z — <date>` sections. Phase 1 reads the same file and should reuse
  its section reader rather than writing a second one; if the existing reader
  is not importable as-is, say so in the phase record rather than copying it.
- `hooks/version-check.py` — reads `git ls-remote --tags` and nothing else.
  Unchanged. The tag gains a second consumer and keeps its first.
- `docs/release-checklist.md` §5 and §6 — §5 prescribes the release pull
  request title, §6 is the three lines after the merge that this work extends.
- `docs/branch-and-release.md` §*What breaks when the last row is squashed* —
  the enumeration phase 2 adds to.
- `docs/issues-and-milestones.md` §*A label answers what it is about* — lines
  127 onward specify `size: now`. Phase 4 adds to it and rewords one sentence.

**Constraints a phase will otherwise rediscover**, each read out of the tree:

1. **`tests/test_the_gate_names_every_step_ci_runs.py`** partitions every step
   of `hygiene.yml`'s `release` job against `broad_gate.py`'s arms, red from
   both sides. Nothing here adds a step to that job, which is deliberate; if
   a phase finds itself wanting one, it has grown a second deliverable and
   the plan is wrong rather than the test.
2. **`tests/test_release_hygiene.py`** refuses a loaded document naming the
   running version or anything above it. Use `X.Y.Z` in prose and `1.2.3` for
   an illustrative number, which is what the documents already do.
3. **`tests/test_no_real_identifiers.py`** allows `github.com` and every
   subdomain of it, and is silent on the raw-content host GitHub serves file
   bodies from. The directory URLs belong inside `plugin_directory_check.py`;
   if a raw host is needed, extend `ALLOWED_DOMAINS` consciously with the
   reason in a comment, and never by rewording a document into a lie.
   **This constraint refused its own wording**: naming that host here put a
   refused domain in prose, and the sweep reported this line and `spec.md`'s
   row. No raw host is needed — phase 3 reads through `api.github.com`, which
   is a subdomain of an allowed one — so the allowlist is untouched and the
   two sentences say which host they mean instead of spelling it.
4. **`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`**
   enumerates `skills/*/scripts/*.py` only, so a `.github/scripts/` addition
   owes no `bin/` wrapper. The checklist box still carries the runnable
   command, because a box a reader cannot act on is the defect this work item
   is about.
5. **`tests/test_a_script_says_which_interpreter_it_needs.py`** classifies
   scripts using constructs above the interpreter floor. Stay at or below the
   floor, the way the sibling scripts do.
6. **`agent-contract` §15** — every new case is seen red before it is
   committed as a case, and the phase record says how it was shown.
7. **`CLAUDE.md` §*A change writes fragments*** — the changelog entry goes in
   `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/changelog.md`
   and any ledger row in
   `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`.
   `CHANGELOG.md` and `seal/ledger.md` are not appended to.

**What breaks in six months, for the chosen approach.** The release-note
workflow depends on two conventions it does not own: that `CHANGELOG.md`
carries a `## X.Y.Z` section by the time the tag is pushed, and that the
tagged commit's message carries the `release: X.Y.Z — ` line. The first is
already held by `gather_changelog.py --check` at the release pull request.
The second is held by nothing, which is why A4 gives it a fallback that says
in the job log which branch it took — a wrong title is visible and fixable in
one edit, where a failed job at the tag is a release that stops.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The release note is published by a workflow the tag push triggers** | Depends on two conventions it does not own; A4's fallback and A3's red are what make each visible | **chosen** — #386's shape 2, and the first goal decides it |
| A line in `docs/release-checklist.md` §6 beside the tag (#386 shape 1) | This is the design that already failed. The step has been a habit and nothing else, and three consecutive releases skipped it | rejected as the deliverable; kept as scope item 2, where the box confirms the workflow fired rather than performing the act |
| A check that refuses the next release while the previous tag has no note (#386 shape 3) | Reads GitHub rather than the tree, and fires one release too late by construction | rejected — the ticket's own reasoning, and the chosen shape removes the condition |
| Publish from the existing `push: branches: [main]` workflow | The tag does not exist at that moment, so the job would have to create it, and `docs/branch-and-release.md` says the tag is the maintainer's | rejected |
| Title from the `## X.Y.Z — <date>` changelog heading | The heading carries a date and no prose, so every release note would lose the symptom line the existing twenty-three carry | rejected |
| Title reproduced from the hand-written release names | Measured: they match neither the pull request title nor the changelog heading. Nothing can reproduce a sentence a person invented | rejected — §5's prescribed title is the only written-down source |
| A workflow that fails a release on the plugin directory's state | Measured in #417: one of the two directories went 22 days without a commit. A red the owner cannot act on | rejected — the ticket's, and consistent with the first goal |
| A reporting command behind a checklist box for the directory | A box is skippable, which is this work item's own subject | **chosen with that stated** — the act behind it is somebody else's repository, so nothing here can perform it; what a machine can do is answer the box, and the box carries the command |
| **The tracker's declared labels are reconciled by the workflow that already runs when `main` moves** | A label deleted by hand comes back at the next release rather than immediately | **chosen** — precedent in `label_merged_on_release_branch.py`, no new permission, no new trigger, no person |
| A hygiene step that fails a pull request while a declared label is missing | Red on this very branch: `agent-contract` §6 withholds posting from every agent, so no party in this run can create the label. It would also grow `broad_gate.py`'s partition | rejected |
| Creating the label by hand and writing a sentence asking the next person to remember | The exact shape #450 filed against — an act assigned to a person has no queue anything can read | rejected |
| A tracker issue holding "create the label" | Moves the act to a queue and leaves it a person's. #450 asks for a home; a workflow is a better home than a row | rejected |
| A sweep applying `size: now` across the open backlog | The section's own argument is that the judgment is cheap at filing and expensive in a batch | rejected — the document states the rule instead |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The release note publishes itself.** `.github/workflows/publish-release.yml` on `push: tags: ['v*']` with `contents: write`, and `.github/scripts/publish_release_note.py`: the `## X.Y.Z` section as the body, the tagged commit's `release: X.Y.Z — <symptoms>` line as the title, an existing release left alone, a missing section red | new `tests/test_a_release_publishes_its_note.py` — A1, A2, A3, A4, each seen red first, `gh` stubbed and `CHANGELOG.md` fixtured | `1b92121d` |
| 2 | **§6 stops at neither the tag nor a sentence, and two sentences reach `docs/branch-and-release.md`.** Two boxes in `docs/release-checklist.md` §6 — the release note exists, the directory carries the version — each with its command; the fixed-name sentence and the outside-pin sentence beside §*What breaks when the last row is squashed* | a case over both documents — A5, A8. The directory box's command exists from phase 3, so phase 2 lands before it only if the box names the command it is about to gain; otherwise run 3 before 2 and say so | `7efe496c` — 3 ran first; `phases/phase-2.md` says so |
| 3 | **The directory box has an answer.** `.github/scripts/plugin_directory_check.py`: both public files, listed or not, the pinned commit, whether it is an ancestor of `main`. Reports and exits 0 on absence and on a failed fetch | a case over captured fixture JSON in both shapes — A6, A7. The fixtures are captured, not fetched at test time, so the suite does not reach the network | `c8983b14` — built before phase 2, which this row's own sentence sanctions; `phases/phase-3.md` says so |
| 4 | **`size: now` exists and stops existing on the issue it is spent on.** `.github/scripts/tracker_labels.py` with `--check`/`--apply`, a step in `close-issues-on-release.yml`, the removal inside `close_issues_on_release.py#main`, and `docs/issues-and-milestones.md` gaining where the judgment is made, what removes a spent label and that no sweep is owed — with the one pinned sentence reworded and `tests/test_a_release_is_sized_by_a_criterion.py`'s literal moved in the same commit | a case for A9, A10, A11, A12; the existing case carries A13 with its literal updated | `cdfcc40b` |
| 5 | **The fragments.** `seal/specs/<work-item-id>/changelog.md`, and a `seal/ledger/<work-item-id>.md` row for each fact this work settled by opening code | `gather_changelog.py --check` and `evidence_check.py --strict .` at the broad gate, which is the sealer's single run | `c5c35693` — the ledger fragment rode phase 4's commit; `phases/phase-5.md` says why |

Phase 4 is last because it is the only one that edits a document another
module pins by literal, and the only one that writes to the tracker at all.
Putting it behind three green phases keeps a reworded sentence from being
debugged next to a new workflow.

## Operational impact

- **New permission surface, one workflow.** `publish-release.yml` declares
  `contents: write`, which is the first write of that scope in this
  repository. It is the minimum `gh release create` needs and the job does
  nothing else; state the scope and the reason in the file, the way
  `hygiene.yml`'s `permissions:` block states its two reads.
- **No new permission for phase 4.** `close-issues-on-release.yml` already
  declares `issues: write`.
- **No new dependency.** Every script is `python3` plus `gh`, which is what
  `.github/scripts/` already is. Phase 3 reads two URLs over HTTPS from the
  standard library; the suite reads fixtures, not the network.
- **A first run that is also the proof.** The release that merges this branch
  pushes a tag, which fires phase 1's workflow for the first time. Nothing in
  the suite can prove a tag-triggered job runs, so the release itself is
  where A1 stops being a case and becomes an observation — and `overview.md`
  carries it as an unverified row with the releasing session named until it
  does.
- **One prompt budget, three deliverables, and it is zero.** Every step added
  here runs on GitHub after a push. None of them puts a question in front of
  anybody, and two of them remove an act that used to need one.
