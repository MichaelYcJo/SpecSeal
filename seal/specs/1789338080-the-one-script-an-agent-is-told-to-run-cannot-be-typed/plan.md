# Implementation Plan: the one script an agent is told to run cannot be typed

<!-- seal/specs/1789338080-the-one-script-an-agent-is-told-to-run-cannot-be-typed/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-14 by the owner, when `smith` was spawned.

## Summary

Write the wrapper pair the script has been announcing since it shipped, spell
the two typed command forms as that command, give every shipped document that
names `round_record.py` one way to reach it, and pin the whole class with a
test that enumerates the scripts and the documents rather than naming
`round_record.py` in the assertion.

Four phases. The wrapper is phase 2 and stands alone; the documents are phase 3
and are preceded by their own pin, seen red against all nine of them.

## Technical context

**What exists.**

- `skills/code-review/scripts/round_record.py` — 162 KB, subcommands
  `new`, `close`, `seal`. **Executed** 2026-09-14: `--help` exits 0 and prints
  `usage: round-record [-h] {new,close,seal} ...`. It carries its own
  below-floor guard at entry (`#below_floor`, #226), so the wrapper needs no
  version logic of its own — the siblings have none either.
- `bin/` holds eleven wrapper pairs. Ten of the twelve scripts under
  `skills/*/scripts/` have one; the two without are `round_record.py` and
  `chain_check.py`.
- `bin/survivor-check` is the model: same skill, same scripts directory,
  eleven lines, `here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)` then
  `exec python3 "$here/../skills/code-review/scripts/survivor_check.py" "$@"`.
  Its `.cmd` twin resolves `py -3` first and falls back to `python`.
- `.gitattributes` is `* text=auto eol=lf`, so the `.cmd` twin ships with LF
  endings exactly as the existing eleven do. Nothing new is being decided here.
- `bin/` is already inside the hygiene step's *what ships* pattern
  (`tests/test_the_release_check_watches_what_ships.py`, work item
  `1788302682`), so a new file under it needs no workflow change and no new
  classification.

**The existing practice this makes checkable.** Four scripts are named as
`.py` in shipped documents: `round_record.py` (36 lines), `chain_check.py`
(23), `evidence_check.py` (8) and `session_cost.py` (6). **Executed**
2026-09-14, per document: every document naming `evidence_check.py` also names
`evidence-check`, and the one naming `session_cost.py` also names
`session-cost`. Four documents, four hits, no misses. `round_record.py` is the
sole violator, and it is the one with no wrapper to name.

So phase 3's pin does not invent a convention. It states one the repository
already keeps everywhere it can, and names the single place it cannot.

**Where the wrapper pairs are pinned today.** Each script's own test module
carries the case —
`tests/test_unverified_rows_close.py::test_the_wrapper_is_present_and_executable`
is the four-assertion form (file, twin, exec bit, target exists), and
`tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_wrapper_pair_is_run_through_the_twin_the_platform_can_execute`
is the platform form. Phase 2 follows the first; phase 3's pin generalises it
across the class, which is what nothing does today.

**Failure scenario of the chosen approach** (what breaks in 6 months): a new
document names a shipped script in passing, the pin goes red, and the cheapest
green is to delete the mention rather than add the locator. Two things are
aimed at that. The pin's message names both accepted forms and the document, so
the correct repair is the one in front of the reader; and the rule is satisfied
by *one* mention per document, so a document that names a script forty times
pays one sentence. What it cannot prevent is a reader who deletes the sentence
that made it green — which is the same exposure every prose pin in this
repository has, and is why the message is part of the deliverable rather than
an afterthought.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| The wrapper alone — #318's own preference, *the smaller change* | Thirty-four of the thirty-six mentions describe the generator rather than invoking it, and a reader who meets one goes looking for a filename. Three of the four segments in the incident were `warden`, whose definition never tells it to run the script at all — so the half of the defect the wrapper fixes is the half those segments never touched | rejected as half a fix |
| The path written into each document, and no wrapper | The two typed forms become a 43-character path somebody retypes, where every sibling command in the same file is a bare word; the one script the orchestrator actually runs stays the odd one out. A path in prose also rots when the script moves, and a wrapper does not — that is why `bin/` exists | rejected as half a fix |
| Wrapper, plus one locator in a single document that the others point at | An agent's payload is its own definition and its skills. A `warden` that has `agents/warden.md` and must open a second file to learn the script exists is being asked for exactly the read that did not happen. #292 is the cost argument for small payloads, and one sentence is not what it is arguing against | rejected |
| Wrapper, plus a locator in each of the ticket's three documents | Leaves `templates/sdd-round.md` — the file the four segments hand-wrote from, seven mentions, not in the ticket — untouched, along with five others. Fixes the coordinate the finding pointed at, which §12 names as the failure | rejected |
| **Wrapper pair, `round-record` at both typed forms, one locator in each of the nine documents, and a test that enumerates scripts and documents instead of naming this one** | The deletion path above, which the message is written against | **chosen** |
| The same, plus a `bin/chain-check` wrapper so `bin/` is uniform | Widens the branch into a script no other 0.11.4 item opens, and changes `templates/config.md`'s user-facing broad-gate row. `chain_check.py` is reachable at all three places it is invoked, and appears in no shipped document as a command — a property phase 3 asserts rather than assumes | rejected; classified instead |
| A rule in `CONTRIBUTING.md` and no test | `CLAUDE.md` §*The goal a design is chosen against*: between a rule somebody has to remember at the moment of writing and a check that goes red on its own, the check wins. This defect is itself an instance — every one of the nine documents was written by somebody who knew the script existed | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | SDD set (`spec.md`, `plan.md`, `questions.md`) committed | the three files in the tree at the phase commit | 5f131bb |
| 2 | `bin/round-record` and `bin/round-record.cmd`, modelled on `bin/survivor-check`; the wrapper-pair case planted with them | the case seen **red** before the two files exist, green after; **executed** `bin/round-record --help` exit 0 printing `usage: round-record`, and `bin/round-record new --help` exit 0; the `.cmd` twin's command construction asserted from this machine for both platforms | 8dfde46 |
| 3 | The class pin seen red against all nine documents and both unwrapped scripts; then the two typed forms in `skills/code-review/orchestration.md` respelled `round-record`, one locator added to each of the nine documents, and `chain_check.py` classified with its reason; pin green | the pin red first, named per document, then green; the classification-defence case red when a `chain_check.py` command form is planted in a fixture; `tests/test_docs_line_wrap.py` green for the four covered files this phase edits (`agents/warden.md`, `agents/sealer.md`, `skills/code-review/SKILL.md`, `skills/code-review/orchestration.md`) | 432af98 |
| 4 | `changelog.md` and `seal/ledger/1789338080-….md` fragments, and `overview.md` | the two hygiene-adjacent modules green, `evidence-check --strict .` clean on the fragment, `uvx ruff check` and `ruff format --check` on the one new test file | |

**Phase 3 is one slice on purpose.** A pin seen red is not a phase that ends
with something verified, and a document sweep with no pin in front of it is the
state this work item exists to end. They close together.

**What phase 2 must not do.** It plants the wrapper and its own case only. It
does not touch a document — the respelling is phase 3's, behind the pin that
proves the respelling was owed.

## Verification scope

Narrow and often. Phase 2 runs the wrapper module; phase 3 runs the new pin and
`tests/test_docs_line_wrap.py`; phase 4 runs the two hygiene-adjacent modules
and the lint of the files it changed. **The full suite, the repository-wide
lint and the typecheck are the sealer's single act after the review rounds
settle** — `skills/agent-contract/SKILL.md` §2 — and no phase here takes them.

Every case this work plants is seen red before it is committed
(`skills/agent-contract/SKILL.md` §15), and the handover says how each was
shown red. The phase 3 pin is shown red twice: once against the tree as it
stands, and once by mutation after it is green, by deleting one locator.

## Operational impact

None to a user of the plugin, and nothing to deploy. One new command lands on
the Bash tool's PATH while the plugin is enabled; no existing command changes
name, arguments or output. A release pull request that touched only these
files would need `plugin.json` moved, which the hygiene step already demands
for `bin/` and which the release-preparation commit already does.
