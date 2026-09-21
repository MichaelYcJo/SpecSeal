# Feature Specification: the outside contributor has no procedure

<!-- seal/specs/1789919879-the-outside-contributor-has-no-procedure/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## Why this work exists

A first-time contributor from a fork opened **PR #443**, a one-line change to
`skills/evidence-check/SKILL.md`, **against `main`**. Two things went wrong and
neither is the contributor's.

**Nothing this repository shows a contributor says where a pull request goes.**
`CONTRIBUTING.md` carries no such sentence; its only branch-related section,
`## Cutting a release`, points at `docs/branch-and-release.md`, whose own
opening says it was split out because *nobody opens a contribution guide at
that moment* — it addresses the person merging. `README.md`'s `## Contributing`
states the bar for gate changes and defers. There is no
`.github/PULL_REQUEST_TEMPLATE.md`. So GitHub's default, the default branch
`main`, is what the contributor got, and nothing offered an alternative.

**The gate that caught it named the wrong cause.** The hygiene step *a change
to what ships must move the version* is correct: it exits 0 for any base but
`main`, and its own comment holds the reasoning — *Asking every feature PR to
bump it is what made one commit one release*. But the refusal a contributor
sees names `plugin.json` and a version:

```
this PR changes what ships but leaves plugin.json at 0.12.0 — an update
keyed to the version will not reach anyone
```

The real cause is *this pull request is aimed at the wrong branch*, and the
message never says it. A contributor following that message would edit the one
file they must not touch. Verified by executing `gh run view 35301136290
--log-failed`: the step expanded to `if [ "main" != "main" ]`, fell through,
printed `version: 0.12.0 -> 0.12.0`, and emitted exactly that line.

The owner then widened the scope: **the procedure for an outside contributor
should be written down end to end**, not only which branch.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The refusal text is a gate change, so the message work owes a test seen red, a stated failure direction, a prompt budget, and platform honesty |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between two ways to tell a contributor where a PR goes, the one that needs no maintainer to intervene wins |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | The PR template and every example use `example.com` and `/Users/x/`; the contributor's handle appears in records (history) and never in a template |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | This work's changelog entry goes in `seal/specs/<id>/changelog.md`, its evidence rows in `seal/ledger/<id>.md` |
| `CONTRIBUTING.md` §*House rules* → *Both READMEs move together* | `README.ko.md` is in scope by rule, not by preference — the hygiene workflow warns when only one moves |
| `docs/branch-and-release.md` §*Work accumulates on a release branch* | The base-branch fact the document has to state: feature branches are cut from, and squash into, the open `release/vX.Y.Z` branch |

## The measurement at the centre of the frame — what CI actually demands

This repository runs an SDD ladder on itself, and almost none of it can apply
to an outside contributor, who has no local hook, no `seal/` conventions and no
reason to know any of it. The document being written must state, as fact rather
than hope, which ceremonies a contributor is exempt from.

**Established by reading every step of `.github/workflows/hygiene.yml` and
`.github/workflows/test.yml`, each checker's own decision logic, and the live
run on #443 after its base was corrected to `release/v0.12.1` at 15:49:11Z.**

| Step (base = a release branch) | What a contributor's PR, carrying no work item, meets | How established |
|---|---|---|
| `issue_claims_check.py` | reports and **never fails**; an empty body is a body, and the only exit 2 is a step handed none | read: its docstring and `body_from` <!-- the framer wrote read_body (no backticks here on purpose: the record checker reads backticked names, and quoting the wrong one re-raises the refusal it is being corrected for). No such name is in the tree, and the checker refused the row at phase 5. body_from is the function that decides "handed none", and its own docstring states both halves of this row's claim — an empty PR_BODY is a body, an absent one is the only thing worth an exit code. Corrected 2026-09-21 --> |
| a change to what ships must move the version | `exit 0` — the guard is `base_ref != main` | read + executed (#443, both runs) |
| every changelog fragment reached the released file | `exit 0` — same guard | read |
| every ledger fragment folded | `exit 0` — same guard | read |
| the unverified record is readable | scans `seal/specs/` **in the tree**, not the diff; a PR that deletes no `overview.md` row passes | read: `unverified_check.py` docstring, *fewer rows* |
| a declared review chain has the round record it claimed | **no declaration naming the head branch → pass, with a notice** | read: `chain_check.py` docstring row *no declaration at all*; executed (#443 green) |
| wording this branch removed is not still standing elsewhere | **runs, and can fail** — see the one asterisk below | read + executed (#443 green) |
| the mode the row declares is the mode the folder is in | reads a committed row against the folder; a contributor changes neither | read |
| the CLAUDE.md block is the template's | fails only if `CLAUDE.md` was edited without regenerating | read |
| both READMEs move together | `::warning::` only, never a failure | read |
| `tests.yml` — lint, pytest ×3, ledger | ordinary: `ruff check`, `ruff format --check`, `pytest tests/`, the lenient `evidence_check.py` | read + executed (#443 green 4/4) |

**So the exemption list is this, and the document states it.** A contributor
writes no `routing.md`, no `spec.md` or `plan.md`, no round record, no ledger
row, no changelog fragment, no `overview.md`, and bumps no version. They have
no commit gate and no worktree guard, because those are plugin hooks on a
machine they do not have. Live proof: #443 carries none of those and its checks
are green.

**The one asterisk, and the document must name it.** `survivor_check.py` runs
on a pull request into a release branch and can refuse a documentation change
that reuses wording the branch removed elsewhere. Its refusal tells the author
to *record it in `seal/specs/<work-item-id>/survivors.md`* — a convention a
contributor has none of. This work does **not** change that message; the
document tells a contributor who meets it to say so on the pull request and let
a maintainer judge it. Recorded as Q4.

**A second fact the scope depends on.** The step whose message changes lives
only in `.github/workflows/hygiene.yml`; the shipped `templates/hygiene.yml`
carries five steps and not this one (`grep -c 'plugin.json' templates/hygiene.yml`
→ `0`). `.github/` is in `STAYS_HOME` in
`tests/test_the_release_check_watches_what_ships.py`, so **this work requires no
version bump** and its own pull request will not meet the refusal it repairs.

## Scope

### In

| # | Surface | What changes |
|---|---|---|
| S1 | `CONTRIBUTING.md` | A contributor-facing procedure, end to end, **above** `## Running the checks` — the file currently opens on how to run the suite, which is the fourth thing a newcomer needs. It states which branch to base on and how to find it, what a contributor does, and what they are **not** asked to do |
| S2 | `.github/PULL_REQUEST_TEMPLATE.md` | New file. Its whole advantage is that it reaches a contributor who opened no document — so it carries the base-branch fact itself rather than only a link |
| S3 | `.github/workflows/hygiene.yml` | The refusal message of *a change to what ships must move the version*, so a contributor whose base is wrong is told the base is wrong |
| S4 | `README.md` **and** `README.ko.md` | `## Contributing` / `## 기여` point at the new procedure. Both editions, because `CONTRIBUTING.md`'s house rule and the hygiene workflow's warning both require it |
| S5 | `tests/` | Two pins, each seen red before the thing it pins exists: the case for S3's refusal message, and the minimal case Q6 decided for S1's exemption section |
| S6 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` | The fragments this repository's own rules require of any work item |

### Out, each with the reason

| # | Not changed | Why |
|---|---|---|
| O1 | The gate's **logic** — the `base_ref != main` condition | It is correct, and its own comment holds the reasoning. Only the text a refused author reads changes |
| O2 | The merge-method table in `CLAUDE.md` / `docs/branch-and-release.md` | Fixed per direction and enforced by two rulesets; the owner put it out of scope |
| O3 | The `NAME NOT IN TREE` marker spelling of #442/#443 | That is #443's own pull request, already green. This work is about how #443 arrived, not what it says |
| O4 | The repository's **default branch** | Changing it from `main` would make GitHub default a contributor's PR to the right place at the source — and would also move what the marketplace clone tracks (`README.md` §*Work accumulates on a release branch*) and what two branch rulesets name. A documentation fix that costs nothing is tried first. Recorded as Q2 |
| O5 | `docs/branch-and-release.md` | Its own opening says it addresses the person merging. Putting the contributor's base-branch fact there would repeat this work item's own defect |
| O6 | `templates/hygiene.yml` | Verified: it does not carry the step whose message changes |
| O7 | `survivor_check.py`'s refusal text | The only CI message that can send a contributor into a `seal/` convention, and repairing it is a second gate change with its own red-test bar. The document warns instead. Recorded as Q4 |
| O8 | A `CODE_OF_CONDUCT.md`, a discussions link, or a `.github/ISSUE_TEMPLATE` addition | Nothing asked for them and none prevents a measured failure. #442 shows the issue path already works |
| O9 | `.claude-plugin/plugin.json` | No version bump: nothing under a shipping root changes (see the second fact above) |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | The refusal names the real cause | **Given** a pull request whose base is `main` that changes a shipping root without moving the version, **when** the hygiene step refuses, **then** the message names both causes and asserts neither — the release case first, because that is the reader the old text already served, and the base-branch case second, naming where a contribution's base belongs | The case from A6 asserts the new text; the old text fails it <!-- Corrected during round 1's fix pass (🟡 2). The frame asked for the base-branch case BEFORE `plugin.json`; the built message ships the opposite order, deliberately, and `tests/test_the_release_check_watches_what_ships.py::test_the_refusal_still_serves_the_release_and_puts_it_first` pins it that way. The grounds are in `plan.md` §*The design constraint the message has to satisfy* and in `phases/phase-2.md` Q7: the step cannot tell a release that forgot the bump from a contribution on the wrong base, so it must serve both, and the release reader is the one the old text was already right for. A1 was the older sentence and is corrected to match rather than the message being reordered. `overview.md` carries this as a divergence a planner may overturn. --> |
| A2 | The refusal still refuses a real release | **Given** a genuine release pull request into `main` that changes a shipping root and leaves the version alone, **when** the step runs, **then** it still exits 1 | `tests/test_the_release_check_watches_what_ships.py` unchanged cases stay green; the guard's `if … fi … exit 0` shape is asserted |
| A3 | A contributor who opens no document is told where the PR goes | **Given** someone opening a pull request on GitHub, **when** the description box is pre-filled, **then** `.github/PULL_REQUEST_TEMPLATE.md` states the base branch and how to find it, without requiring another file to be opened | Read the rendered template; it contains the branch fact in its own words |
| A4 | The procedure is the first thing in the contribution guide | **Given** `CONTRIBUTING.md`, **when** a newcomer opens it, **then** the contributor procedure appears before `## Running the checks` | `CONTRIBUTING.md`'s first `## ` heading is the new section |
| A5 | The exemptions are stated, not implied | **Given** the new section, **then** it names what a contributor does **not** do — no `routing.md`, no spec or plan, no round record, no ledger row, no changelog fragment, no version bump — and says CI does not ask for them | Read against the measurement table above; every row of the exemption list appears |
| A6 | The new message is pinned by a case seen red | **Given** the test planted for S3, **when** it runs against the pre-fix workflow, **then** it fails; against the post-fix workflow it passes | `bin/test tests/<file> -q; echo $?` on both trees, recorded in the phase record |
| A7 | Both READMEs moved | **Given** the branch's diff, **then** `README.md` and `README.ko.md` both changed | `git diff --name-only` names both; the hygiene warning stays silent |
| A8 | No real identifier entered a template | **Given** the new template and every example added, **then** no real domain, user path, handle or PR number appears in them | `bin/test tests/test_no_real_identifiers.py -q`, plus a read of the template for the contributor's handle |
| A9 | Documentation stays within the wrap limit | **Given** `CONTRIBUTING.md`, `README.md`, `README.ko.md`, **then** no prose line exceeds 88 columns | `bin/test tests/test_docs_line_wrap.py -q` |
| A10 | The exemption list is pinned, minimally | **Given** the new `CONTRIBUTING.md` section, **when** the pin Q6 decided runs, **then** it asserts the section exists and names the release-only guard in the terms a reader searches for — and it is red against a tree without the section | `bin/test tests/<file> -q; echo $?` on both trees, recorded in `phases/phase-1.md` |

## Data & interfaces

No schema, no endpoint, no payload. Three text surfaces and one workflow step:

- `.github/workflows/hygiene.yml`, step `a change to what ships must move the
  version` — the `::error::` line only.
- `.github/PULL_REQUEST_TEMPLATE.md` — a new tracked file, therefore
  automatically inside `tests/test_no_real_identifiers.py`'s scan, which reads
  `git ls-files`.
- `CONTRIBUTING.md`, `README.md`, `README.ko.md` — all three are in
  `tests/test_docs_line_wrap.py`'s `COVERED` at `LIMIT = 88`.

Whether the new template joins `COVERED` is Q3.

## Open questions → questions.md

Seven rows — four a person's, two settled by measurement, one the work's. The
routing answer is the `automation` preset, so each of the four is answered the
way the evidence points and marked as a decision the owner can overturn at
review; none blocks the build.

Framed 2026-09-21 by framer, before the build.
