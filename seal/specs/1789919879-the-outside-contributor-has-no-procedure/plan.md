# Implementation Plan: the outside contributor has no procedure

<!-- seal/specs/1789919879-the-outside-contributor-has-no-procedure/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable behaviour,
approval of this plan is the gate. -->

Approved 2026-09-20 by the routing batch and by no reader of this plan, when `smith` was spawned.

**What that line means here, written out because the short form would read as
a signature.** The repository owner answered the routing batch on 2026-09-20
before the first edit — the `automation` preset, recorded in `routing.md` —
and asked the run not to stop again. That answer is what let the build
proceed. Nobody read this plan clause by clause, and no approval of its
phasing or its alternatives was given. Round 1's fix pass filled the line
because the placeholder was still standing; filling it also silences
`chain_check`'s notice about an unfilled approval, which is deliberate, since
the fact the notice reports is now the content of the line itself.

## Summary

Write down, end to end, what an outside contributor does — and what they are
not asked to do — and repair the one gate message that misdirects them. Four
text surfaces and one workflow step. No logic changes, no version bump.

The document's unusual content is the **exemption list**: this repository runs
an SDD ladder on itself, and `spec.md` §*The measurement at the centre of the
frame* establishes by reading every CI step and by the live run on #443 that a
contributor's pull request is asked for none of it.

## Technical context

| Coordinate | What it is to this work |
|---|---|
| `.github/workflows/hygiene.yml`, step `a change to what ships must move the version` | The only line that changes: the `::error::` emitted when `old = new`. The `base_ref != main` guard above it is untouched |
| `tests/test_the_release_check_watches_what_ships.py` | Already reads this exact step, splitting on the step name and the next `- name:`. Its docstring says *This file is the pin* for the step, so the new case belongs here rather than in a new module |
| `tests/test_a_release_cannot_ship_an_untrue_milestone.py#hygiene_step` | The precedent for pinning a hygiene step's **shape** — a closed `if … fi` with `exit 0` in the body — after a mutation that deleted the `exit 0` passed a condition-only assertion |
| `tests/test_docs_line_wrap.py#COVERED` | Holds `README.md`, `README.ko.md`, `CONTRIBUTING.md` at `LIMIT = 88`. Its comments state the rule for a new file: one written wrapped *goes in at birth* |
| `tests/test_no_real_identifiers.py#tracked_text_files` | Reads `git ls-files`, so a new tracked template is inside the scan with no list to update |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The four things the message work owes, answered in the pull request body |
| `docs/branch-and-release.md` §*Work accumulates on a release branch* | The source of the base-branch fact. One open release branch exists today: `origin/release/v0.12.1` |

**The failure scenario of the chosen approach, at six months.** The document
names a branch-naming convention (`release/vX.Y.Z`) rather than a branch, so it
does not rot when the release rolls. What can rot is the exemption list: a new
always-on CI step that does demand something of a contributor would make the
list false while every test stays green, because nothing reads prose against
the workflow. The mitigation is stated rather than built — the list is grouped
by workflow step so a reader adding a step can see which sentence it lands in,
and Q1 records that no check binds them.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Change the default branch** from `main` to the open release branch, so GitHub defaults a contributor's base correctly at the source | The marketplace clone tracks `main` and `claude plugin update` installs whatever `main` holds; two branch rulesets name `main` and `release/*` by pattern, and a release branch is deleted after each release, so the default would have to be moved every release or point at a branch that no longer exists | Rejected. It reshapes shipping to repair a documentation gap, and the gap has a documentation fix |
| **Make the gate refuse** any pull request based on `main` that is not a release | `docs/branch-and-release.md` names a hotfix branch as the other thing that legitimately reaches `main`, and it carries no release milestone to tell it apart. The gate would deny a correct pull request — a wrong deny on the release path, which is the expensive direction `CONTRIBUTING.md` asks about | Rejected. The owner put the logic out of scope and the evidence agrees |
| **Put the procedure in `docs/branch-and-release.md`** and link to it | That file's own opening says it was split out because nobody opens a contribution guide at merge time — it addresses the person merging. A contributor never arrives. Writing the contributor's fact there repeats this work item's own defect one document over | Rejected (spec O5) |
| **The PR template alone**, leaving `CONTRIBUTING.md` untouched | A template is pre-filled text a contributor can delete, and it has no room for the half that matters most — what they are *not* asked to do, which is prose rather than a checkbox. Someone who reads the guide before opening anything still finds nothing | Rejected. Both, with the template carrying the one fact and the guide carrying the procedure |
| **An Action that auto-retargets** a pull request based on `main` | It needs write permission on pull requests, where `hygiene.yml` has declared `contents: read` / `issues: read` since #359 precisely so its token is a fact of the file rather than of an account setting. Silently moving somebody's base is also a change they cannot see | Rejected. Mechanism where a sentence suffices |
| **A refusal that only cites `CONTRIBUTING.md`**, with no fact inline | A CI log is read by somebody who is already stuck. A second hop is a second chance to stop, and a contributor who has not cloned the repository is reading GitHub's error panel | Rejected. The message states the cause and the fix inline, and cites the file after |

### The design constraint the message has to satisfy

At the moment the step refuses, the two readers are indistinguishable to it: a
release pull request that forgot the version bump, and a contribution filed
against the wrong branch both reach the same line with `base_ref = main`. The
message must serve both without misleading either — so it names the version
requirement as the release case **and** the wrong base as the other case, in
that order of likelihood for whoever is reading. It must not assert which one
this is.

## Phases

Vertical slices — each phase ends with something a reader or a check can
verify, and each stands alone as a commit.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `CONTRIBUTING.md` gains the contributor procedure **above** `## Running the checks`: which branch to base on and how to find it, what a contribution costs, the exemption list grouped by CI step, and what to do when `survivor-check` refuses. Plus the minimal pin Q6 decided, modelled on `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#contributing_section` | A4, A5, A10 by reading against `spec.md`'s measurement table; `bin/test tests/test_docs_line_wrap.py -q` and `bin/test tests/test_no_real_identifiers.py -q`, and the new pin seen red against the pre-phase tree | 7cf8dfec |
| 2 | The hygiene step's refusal message, and the case in `tests/test_the_release_check_watches_what_ships.py` that pins it — **written first and seen red against the unfixed workflow** | A1, A2, A6. `bin/test tests/test_the_release_check_watches_what_ships.py -q; echo $?` on the pre-fix tree (expect non-zero) and after (expect 0); `bin/test tests/test_a_release_cannot_ship_an_untrue_milestone.py -q` for the sibling step | b4cd6aad |
| 3 | `.github/PULL_REQUEST_TEMPLATE.md`, carrying the base-branch fact in its own words plus a short checklist, and pointing at the section phase 1 wrote | A3, A8 by reading; `bin/test tests/test_no_real_identifiers.py -q`. Q3 decides whether it joins `COVERED`, and the phase record says which way and why | a968cc7c |
| 4 | `README.md` §*Contributing* and `README.ko.md` §*기여* point at the procedure, in both editions | A7, A9. `git diff --name-only origin/release/v0.12.1...HEAD` names both; `bin/test tests/test_docs_line_wrap.py -q` | 282db265 |
| 5 | The fragments this work item owes: `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` | `python3 .github/scripts/gather_changelog.py --check`; `python3 skills/evidence-check/scripts/evidence_check.py .` resolves the new rows | 41e73f55 |

**Phase 1 is first because it is the destination.** Phases 2, 3 and 4 each cite
the section it writes, so building it first is what keeps every intermediate
commit internally consistent — a template pointing at a heading that does not
exist yet is a commit that does not stand alone.

**Phase 2 carries the whole gate bar.** `CONTRIBUTING.md` §*What a change to a
gate must carry* applies to it and not to the other four, and the pull request
body answers all four:

- **A test seen red** — the case is written against the unfixed workflow and
  its failing output recorded in `phases/phase-2.md` before the message moves.
- **A stated failure direction** — the change moves **neither** way. The
  condition, the exit codes and the set of refused pull requests are identical
  before and after; only the text a refused author reads differs. Say so
  plainly rather than claiming a direction.
- **A prompt budget** — zero. Nothing here puts a question in front of a
  person, in CI or in a session. The change removes a wrong instruction from a
  message a person was already reading.
- **Platform honesty** — the step is `shell: bash` on `ubuntu-latest` only, and
  the case reads the workflow file as text with Python's `re`, which the suite
  runs on ubuntu, macOS and Windows. No process inspection, nothing
  platform-dependent.

**What the ledger fragment claims (phase 5), drafted now so phase 5 is a write
rather than a re-derivation.** One row for the refusal message pinned by its new
case, and one for the exemption list anchored at the `CONTRIBUTING.md` heading
phase 1 adds. Both are content anchors, `path#major@hash`, with no line number
and no commit.

## Operational impact

- **No version bump.** Nothing under `skills/`, `agents/`, `hooks/`,
  `templates/`, `bin/` or `.claude-plugin/` changes; `.github/` is classified
  `STAYS_HOME`. Verified in `spec.md`.
- **No migration, no new dependency, no new environment variable.**
- **One new tracked file**, `.github/PULL_REQUEST_TEMPLATE.md`, which GitHub
  pre-fills into every new pull request in this repository — including the
  maintainers' own. Phase 3 keeps it short enough that a maintainer deleting it
  each time is not the outcome.
- **This branch's own pull request** is based on `release/v0.12.1` and meets the
  same checks it documents, which is the cheapest live re-test of the
  exemption list.
