# Implementation Plan: `settle` — the fold a shipped spec has been waiting for

<!-- seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-22 by the orchestrating session, when `smith` was spawned.
The owner pressed `automation` in the routing batch before the first edit, which
routes this gate through the session rather than stopping the run for it; the
owner has not read this plan. Q1 of `questions.md` is theirs and is the one
answer that would change the phase list — it carries a default that continues.

## Summary

`seal/README.md` has named a `settle` step since the root existed and nothing
was ever built. This ships it: a skill under `skills/settle/` with a
`bin/settle` wrapper pair, a reader that enumerates and groups what would
fold, and a procedure a session follows to turn that into one standing
statement per segment and then retire what was absorbed.

**The split that decides the whole shape.** The command **reads, groups and
records**; the session **judges and writes prose**.
`docs/one-root-by-lifetime.md` §*What keeps `settle` light* says the step
*moves and does not verify* — so nothing mechanical can decide which of a
spec's sentences is still true, and folding *only what is still true* is
exactly that decision. A script that wrote the policy statement itself would
either splice every sentence up (a move, not a compaction) or assert truth it
cannot check. A skill with a command beside it is the only arrangement where
both halves of the ticket hold.

**The mechanism ships; this repository's own 97 do not fold on this branch.**
That is a decision, not an omission — the Alternatives table carries it and
Q1 of `questions.md` is where the owner overturns it. Phases 1–5 are identical
under either answer.

## Technical context

What this builds on, with coordinates:

- `docs/one-root-by-lifetime.md` §*What happens at a release* step 2, §*The
  dependency rule*, §*What keeps `settle` light* — the specification of
  `settle` as it was decided on 2026-09-02, and the source of the fold rule,
  the guard, the incrementality requirement and the two readers.
- `.github/scripts/fold_ledger.py#marker`, `#is_marked`, `#open_items` — the
  marker convention (`<!-- specs/<id> -->`), its line-anchored test, and the
  evidence-todo guard already written. `settle` reuses all three rather than
  inventing a second spelling of each.
- `.github/scripts/gather_changelog.py#fragments`, `#ungathered`,
  `#marker` — the second existing fold, and the one whose `--check` goes
  vacuous after a removal.
- `skills/verify/scripts/unverified_check.py#overviews_at`, `#main`'s
  `deleted` list — the reader that genuinely fails after a removal, and the
  arm phase 1 changes.
- `skills/code-review/scripts/round_record.py#below_floor` — written to be
  copied, and named as such in `seal/follow-up.md`. `settle.py` copies it.
- `skills/code-review/scripts/survivor_check.py` §*A deletion is one row,
  because otherwise it is 153* — the `survivors.md` range-row shape both this
  branch and the later fold branch may need.
- `tests/test_chain_hooks_hardening.py#NUMBER_WORDS` and
  `#test_both_readmes_count_the_skills_that_are_actually_there` — the pin that
  turns red the moment a twenty-fourth skill ships and neither README moves.
- `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` — the
  wrapper-pair rule and the reachability rule the new command must satisfy.

**What breaks in six months, for the chosen approach.** The judgment half
lives in a skill, so a session that runs `settle` without loading it gets a
grouped listing and writes whatever it likes into `docs/`. Nothing can stop
that: the command cannot refuse prose it does not write, and a gate that
refused would be the build-failing check the ticket's *Not this* forbids. The
mitigation is that the command's output is a report and not a patch — it never
leaves a half-written `docs/` file behind — and that the retirement is a
separate act the skill makes conditional on a policy having absorbed the item.
The failure mode is therefore *a thin policy document*, which a reader can
see, rather than *a directory deleted with nothing absorbing it*, which nobody
can.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A script under `.github/scripts/`, beside the two existing folds | Every repository running this methodology accumulates the same sediment and gets no way to clear it. The ticket decides this and the reason holds: 98 directories at 15M is what the method does to anyone who uses it long enough, not this repository's circumstance | rejected — ships as a skill with a `bin/` wrapper |
| A pure script that writes the policy prose itself, splicing each sentence up under its work-item comment | Produces a document of 97 spliced sentences rather than one standing statement, and asserts that each moved sentence is still true — which G1 says the step may not do. The largest segment would gain 110 rows' worth of provenance comments and no reader | rejected |
| Fold this repository's own 97 on this branch | Four costs, and the first was measured rather than feared. **Fourteen test modules read this repository's own `seal/specs/` corpus and at least six carry a population floor the fold turns red** — `spec.md` §*The ticket's headline claim is false* has the coordinates; three were re-opened. So the mechanism's own review round would run on a tree whose suite the commit under review had just broken in six places. The unverified-record step goes red unless phase 1 and the fold sit in one diff. A `survivors.md` range-row becomes mandatory. And the release's diff turns mostly into deletions with the mechanism buried inside them. The fold is also the judgment act — nine segments of policy prose — and putting it in the same pull request as the mechanism means one review round judges both | rejected, deferred to its own work item · Q1 |
| Run it inside the release-preparation commit, beside `gather_changelog.py` and `fold_ledger.py` | `docs/release-checklist.md` §2 is two dry runs a person reads and then one mechanical commit. A third fold that writes policy prose puts a judgment act inside that commit, and a release then stops for someone to write documentation. #101 already chose the shape the repository wants here — a count, a nudge, and a command to point at | rejected — by hand, named in the checklist |
| Group by the repository's topic labels (`evidence-check`, `hooks-gates`, `review-chain`, `agents-skills`, `measurement`, `documentation`) | A work item's directory carries no issue number anywhere a machine reads — `templates/sdd-routing.md` has no such row — so the label is not reachable from the tree. Building that link is a second mechanism before the first one exists | rejected — the ledger anchor, which covers 83 of 98 already |
| Keep `overview.md` and delete the rest | `docs/one-root-by-lifetime.md` §*What happens at a release* step 2 says the process record is dropped **with** the directory, and the SDD set's value is what the fold moved into `docs/`. Keeping one file per work item leaves 97 files nothing reads and re-opens the retention setting that document already closed | rejected — delete the directory whole |
| Rewrite `docs/one-root-by-lifetime.md`'s 2026-09-02 text to match what was built | `tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD` classifies it as a record of a moment, and that document's own shape — *Decided after the thread*, dated — is how it takes a later decision | rejected — add a dated section in both editions |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The two readers stop reading released work items.** `unverified_check.py --baseline` no longer reports a removed released work item's `overview.md` as this branch's deletion, and still reports one a branch actually deleted. `gather_changelog.py --check` judges by the `CHANGELOG.md` markers rather than by a fragment glob that goes empty, and says what it read | A1, A2 — each case shown red against the shipped code before it is committed (§15) | cc3c4f3b |
| 2 | **`settle` reads.** `skills/settle/scripts/settle.py` plus `bin/settle` and `bin/settle.cmd`: enumerate released, unfolded work items; group them by ledger anchor rolled up to a segment; name the ungrouped; skip and name an item with an open `evidence-todo.md` row; record what was folded so a second run folds nothing twice and an interrupted one resumes. Writes nothing to `docs/`, removes nothing. Carries the interpreter-floor guard | A3, A4, A5, A7 — cases over a fixture root, and the report over this repository's own tree | b3ddd2b7 |
| 3 | **`skills/settle/SKILL.md`.** The procedure: what goes up and who decides it, where it lands (merge into an existing `docs/` document, create one only for a new area), the work-item-id comment each folded sentence carries, newest-wins, and the retirement as the second half of the fold and never its own act — including the `survivors.md` range-row a fold branch owes **and the population floors a repository's own checks carry over `seal/specs/`, with the three ways to answer one** | A6, A11, and the shipped-document rules: the wrapper pair, the command named, 88-column wrap, the interpreter floor | ccee10e2 |
| 4 | **The documents stop describing a `settle` that does not exist.** `seal/README.md` and `templates/seal-README.md`; a dated section in `docs/one-root-by-lifetime.md` **and** `docs/one-root-by-lifetime.ko.md`; `docs/review-handoff-protocol.md` §*Layout* and §*Why the directory is not deleted*, distinguishing the pre-merge deadline from the post-release fold; `skills/implement/SKILL.md`'s layout table (G6) | A9 — one case per corrected sentence (§14), the wrap test, and the survivor sweep read rather than assumed | 0111020a · 5c40359 |
| 5 | **The plugin counts what it ships.** Both READMEs' skills rows and *Run it yourself* cheat sheets, `NUMBER_WORDS[24]`, and `docs/release-checklist.md`'s by-hand step | A8 | 86b5bf25 |
| 6 | **The dry run over this repository's own 97, read.** Its numbers into `overview.md`; `changelog.md` and `seal/ledger/<id>.md` written. **Nothing removed** | A10 | 93a65ebd |

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

Phase 1 is first because it is the precondition
`docs/one-root-by-lifetime.md` §*Order* states — *first the two checks in "The
dependency rule" stop reading released work items; then `settle` folds* — and
because it is the one slice that stands entirely on its own.

What a phase discovers and the next needs goes to
`seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

## Operational impact

- **A new shipped command**, `settle`, on the Bash tool's PATH in every
  repository with the plugin enabled. It writes nothing unless asked and
  removes nothing without the skill's procedure having produced a policy
  document first.
- **A version bump is already owed.** `skills/` and `bin/` both ship
  (`tests/test_the_release_check_watches_what_ships.py#SHIPS`), so the
  hygiene workflow's *a change to what ships must move the version* step
  demands it at the release pull request. The release already carries one.
- **`NUMBER_WORDS` gains 24.** Without it the suite refuses with *no spelling
  is recorded for that number — add it rather than loosening the check*, which
  is the test working.
- **The survivor sweep runs on this pull request**, because its base is a
  release branch. Rewording the `settle` sentence in six documents removes
  wording that stands in released design records under `seal/specs/`, which is
  in the corpus. Where it reports, the answer is a row in
  `seal/specs/1790027178-…/survivors.md` with the standing text quoted and the
  grounds — never turning the check off.
- **Fragments, never the shared files.** The entry goes to
  `seal/specs/1790027178-…/changelog.md` and the rows to
  `seal/ledger/1790027178-….md`. `CHANGELOG.md` and `seal/ledger.md` are not
  touched by this branch.
- **No migration, no new environment variable, no new dependency, and no
  compatibility break.** Nothing existing changes shape: the two reader
  changes are both in the direction of judging more rather than refusing more,
  and no user repository's tree is altered by installing this.
