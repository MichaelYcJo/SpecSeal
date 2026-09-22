# Feature Specification: `settle` — the fold a shipped spec has been waiting for

<!-- seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## What the tree answered, so nobody reopens it

The ticket leaves three things open and the tree answers all three. They are
answered below with the grounds, and they are not in `questions.md`.

| Ticket's open item | Answered | Where the grounds are |
|---|---|---|
| **What goes up** — the whole spec's conclusion, or only what is still true | Only what is still true, and **the session running `settle` decides which** — the command supplies the corpus and writes no prose into `docs/` | §*Grounding* rows G1 and G2 |
| **What groups** | The ledger anchor's enclosing file, rolled up to a segment. Already written for **83 of the 98** work items; the other 15 are named below | §*What groups, measured on this tree* |
| **When it runs** | By hand, named as a step in `docs/release-checklist.md`, never inside the release-preparation commit and never as a check that fails a build | §*Grounding* row G5 |

Two more the ticket names as open and the documents already decide:

- **Delete, move, or keep `overview.md` alone.** Delete the directory whole.
  `seal/README.md` grants it — *safe to delete a work item's directory
  wholesale after the export rules have run* — and
  `docs/one-root-by-lifetime.md` §*What happens at a release* step 2 says the
  process record is dropped with the directory. Keeping `overview.md` alone
  was weighed and is a row of `plan.md`'s Alternatives table.
- **Whether this work item closes #83.** It closes it. #83 is the same
  mechanism, named in `docs/one-root-by-lifetime.md` §*Order* as *Later: the
  `settle` item (#83)*, and its *Done when* list is the acceptance below as
  #458 amends it. #101 and #216 stay open: #101 waits on this shipping and
  then widens `seal export --check`'s line, which is out of scope here; #216
  is `evidence-check`'s own count and is untouched.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| G1 · `docs/one-root-by-lifetime.md` §*What keeps `settle` light* — *It moves and does not verify. Whether a coordinate still holds is `evidence-check`'s job* | The command may not judge whether a spec sentence is still true. Deciding that is the only way to fold *what is still true*, so the judgment belongs to the session and the command is a reader and a scaffolder. **This is why `settle` ships as a skill with a command beside it rather than as a script alone**, and it is the reading that makes #458's *write one policy statement* and this clause hold together |
| G2 · `docs/one-root-by-lifetime.md` §*What happens at a release* step 2 — the SDD set folds into `docs/<domain>`, merging into a document that already exists and creating one only for a new area; the newest work item wins; each folded sentence carries the work item id as an HTML comment | The destination rule, the collision rule, and the provenance mark. No `docs/policy/` directory: `docs/` is flat today and six segments already have a document there |
| G3 · `docs/one-root-by-lifetime.md` §*What happens at a release* step 3, *The guard* | An item with an open `evidence-todo.md` row is **skipped and named**, never folded and never removed. Read on this tree 2026-09-22: `fold_ledger.open_items('.')` returns `[]`, so no item is in that state today |
| G4 · `docs/one-root-by-lifetime.md` §*The dependency rule* | Two readers must stop reading released work items **before** anything is removed. Both were opened rather than taken from the document; what each actually does is §*The two readers* below |
| G5 · `CLAUDE.md` §*The goal a design is chosen against* and the ticket's *Not this* — *not a check that fails a build for an unsettled spec* | `settle` is invoked, never triggered. It is not wired into `gather_changelog.py` or `fold_ledger.py`, and no gate refuses a branch over an unfolded work item |
| G6 · `skills/implement/SKILL.md` §*Document layout* — `docs/` is *never created here* | That sentence stops being true the moment `settle` writes there. `docs/one-root-by-lifetime.md` §*Decided after the thread* already names it as *the `implement` skill's "never created here" sentence, to be corrected*, and this work item is what corrects it |
| G7 · `CLAUDE.md` §*a change writes fragments, never the shared file* | The entry goes to this work item's `changelog.md`, rows to `seal/ledger/1790027178-….md`. Neither `CHANGELOG.md` nor `seal/ledger.md` is appended to |
| G8 · `CONTRIBUTING.md` §*Proposing a new gate or skill* — *Skills that load on demand are a much easier case to make than anything added to the CLAUDE.md block* | `settle` adds nothing to the always-on surface: no CLAUDE.md line, no hook, no `skills:` list entry on any agent |

## Scope

**In.**

1. `skills/settle/` — the skill, and `skills/settle/scripts/settle.py` with the
   `bin/settle` + `bin/settle.cmd` wrapper pair.
2. The two readers of `seal/specs/` that a removal reaches
   (`skills/verify/scripts/unverified_check.py --baseline`,
   `.github/scripts/gather_changelog.py --check`), changed so that a released
   work item's removed directory is not read as this branch's deletion.
3. The documents that describe `settle` as a thing that will exist, brought
   into step with the thing that now does: `seal/README.md`,
   `templates/seal-README.md`, `docs/one-root-by-lifetime.md` and its Korean
   twin, `docs/review-handoff-protocol.md`, `skills/implement/SKILL.md` (G6).
4. The plugin's own surfaces that count what ships: **both** `README.md` and
   `README.ko.md` — the skills row and the *Run it yourself* cheat sheet — and
   `NUMBER_WORDS` in `tests/test_chain_hooks_hardening.py`.
5. `docs/release-checklist.md` gains the by-hand step (G5).
6. A dry run of `settle` over this repository's own 97 released work items,
   read and reported. **Nothing is removed.**

**Out, and each with why.**

- **Folding this repository's own 97 work items.** The mechanism and this
  repository's fold are separable on purpose, and the plan says so rather than
  letting momentum decide. Q1 of `questions.md` is the owner's to overturn;
  the default is a work item of its own, and nothing in phases 1–5 changes
  either way. The ticket's *Not this* forbids deleting before a policy exists
  to have absorbed it, and writing policy for nine segments is the judgment
  act, not the mechanism.
- **A count-based nudge, and its threshold.** That is #101, which names
  `seal export --check`'s line as its home and depends on `settle` existing.
  This work makes it possible and does not do it.
- **`evidence-check`'s `N unread` line.** #216 is a different count over a
  different population and is untouched here.
- **Separating the SDD set from the process record while a work item is in
  development.** `docs/one-root-by-lifetime.md` §*Out of scope* already
  refuses it; the line between them is used only to say what folds and what is
  dropped.
- **Any change to `seal/ledger.md`'s rows.** A row is a content anchor and
  survives the fold untouched — that is the ticket's own reading and it is why
  the file's first line, `# spec-to-code map`, needs no edit.
- **`docs/one-root-by-lifetime.md`'s 2026-09-02 text.** It is classified as a
  design record — `tests/test_no_document_names_the_old_roots.py`'s
  `DESIGN_RECORD` — and a record of a moment is not rewritten. What #458
  decided later is added as a dated section in the shape that document already
  uses for *Decided after the thread*.

## What groups, measured on this tree

Executed 2026-09-22 on this branch, by counting rather than by reading the
ticket. The ticket's figures were taken before this branch existed and every
one of them has moved.

| | Ticket (#458) | This tree, 2026-09-22 |
|---|---|---|
| work items under `seal/specs/` | 92 | **98** |
| files · size | 1,255 · 13M | **1,338 · 15M** |
| `rounds/round-N.md` | 281 | **253** |
| `phases/phase-N.md` | 264 | **286** |
| `overview.md` · `spec.md` | 84 · — | **89 · 85** |
| work items with a `<!-- specs/<id> -->` marker in `seal/ledger.md` | 78 of 92 | **83 of 98** |
| work items with an open `evidence-todo.md` row | — | **0** |

**The 15 that wrote no ledger row**, named so the second axis is a list to read
rather than an open classification problem — which is the whole of what the
ticket's *named 14* was worth:

```
1788177600-the-tree-that-arrives-without-its-history
1788184145-the-gate-stops-the-session-editing-its-tests
1788212517-the-last-rounds-fixes-are-reviewed-by-nobody
1788217118-a-gate-change-is-not-judged-on-prompt-cost
1788220055-the-skill-was-followed-and-the-text-was-still-hard
1788224363-a-subagent-rediscovers-what-the-session-established
1788276387-the-windows-step-never-reaches-its-guard
1788395377-the-release-guard-globs-one-place
1788425222-release-0-5-0
1788449488-measure-what-flow-finds
1788824000-a-rider-stamp-names-a-commit-the-squash-discards
1788938400-the-shipped-section-goes-and-the-plan-is-renumbered
1789024700-the-framer-moves-and-three-tickets-take-rows
1789053786-the-plan-is-renumbered-and-eight-tickets-take-rows
1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built
```

The last is this work item, which is unreleased; the other 14 are the
population needing a second axis.

**The segment table re-derived**, counting ledger coordinates by the file they
anchor in, across `seal/ledger.md` and `seal/ledger/*.md`:

| Segment | Rows, ticket | Rows, this tree |
|---|---|---|
| `skills/code-review/scripts/round_record.py` | 110 | **110** |
| `skills/code-review/scripts/chain_check.py` | 79 | **76** |
| `skills/evidence-check/scripts/evidence_check.py` | 71 | **71** |
| `skills/implement/scripts/seal.py` | 63 | **63** |
| `skills/verify/scripts/session_cost.py` | 60 | **60** |
| `hooks/root-migrate.py` | 43 | **40** |
| `skills/verify/scripts/broad_gate.py` | 26 | **39** |
| `skills/code-review/scripts/survivor_check.py` | 21 | **21** |

The grouping claim holds. **What the ticket's table leaves out is the larger
half**: of 1,772 coordinates, **852 — 48% — anchor under `tests/`**, and the
ticket's table says *tests excluded* without saying where they go. What a
test-file anchor rolls up to is Q2 of `questions.md`, and it is the phase that
builds the grouping that decides it.

## The two readers, opened rather than taken from the document

`docs/one-root-by-lifetime.md` §*The dependency rule* names two checks as
*would break on removal*. Both were opened. One of the two claims is right and
the other overstates, and the difference decides how much of phase 1 there is.

| Reader | What it actually does after a removal | Label |
|---|---|---|
| `skills/verify/scripts/unverified_check.py --baseline` | **Fails, as the document says.** `overviews_at()` lists every `overview.md` at the baseline ref by `git ls-tree`, and each one absent from the working tree is appended to `deleted`, which exits 1. A fold removing 97 of them is 97 rows in that list. `.github/workflows/hygiene.yml` runs it on every pull request | read |
| `.github/scripts/gather_changelog.py --check` | **Degrades to vacuous, not to red.** `fragments()` globs `seal/specs/*/changelog.md` and `ungathered()` reports a fragment whose marker is missing from `CHANGELOG.md`. After a removal there are no fragments, so the list is empty and the check passes having examined nothing — the silent direction, which is the one this repository's checkers are written not to fail in | read |

Both still change, and for different reasons: the first because it stops a
fold from being possible at all, the second because a check that passes having
examined nothing is the failure `unverified_check`'s own docstring argues
against one file over. Q3 of `questions.md` is the one-command probe that
confirms the second.

**A third reader the document does not name**, found by reading
`skills/code-review/scripts/survivor_check.py`: `seal/specs/` outside
`rounds/` is **in** the survivor sweep's corpus, and that step runs on every
pull request into a release branch — which is the pull request this work item
opens. The script's own §*A deletion is one row, because otherwise it is 153*
already carries the answer, a range-row in
`seal/specs/<id>/survivors.md`. So the fold branch inherits a constraint the
dependency rule never wrote down, and this spec is where it is written down.
It also touches **this** branch in a smaller way: rewording the `settle`
sentence in six documents removes wording that stands in released design
records, which is what that row shape exists for.

## The ticket's headline claim is false, and the correction is a constraint

#458 states *work items any check actually reads: **0** — `0 work items read ·
92 unread`*. That figure is `evidence-check`'s records arm reading its own
population, and the ticket generalises it to *any check*. **Fourteen test
modules read this repository's own `seal/specs/` corpus, and at least six
carry a population floor that a fold turns red.** Established by reading, with
the coordinate for each; three were re-opened directly and matched.

| Coordinate | The floor | Verified |
|---|---|---|
| `tests/test_chain_check_at_the_pull_request.py:2649` and `:2825` | `assert len(records) > 200, f"the walk found {len(records)} records"`, over `os.walk(ROOT/seal/specs)` | re-opened |
| `tests/test_a_finding_id_is_a_bare_integer.py:752` | `assert len(paths) > 100, f"the corpus is {len(paths)} records; the case is vacuous"` | re-opened |
| `tests/test_the_set_a_work_item_always_has.py` §the todo globs | two non-empty assertions over `seal/specs/*/evidence-todo.md` and `*/tests-todo.md` — *this case is blind, and would stay green if every one of them moved* | re-opened |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` · `tests/test_the_reopening_is_one.py` | each requires a **named** work-item directory to exist, by its epoch prefix | read |
| `tests/test_routing_is_recorded.py` · `tests/test_release_hygiene.py` | non-empty assertions over `seal/specs/*/routing.md` — *no declarations found, the check would pass vacuously* | read |
| `tests/test_the_pull_request_language_is_the_repositorys.py` | non-empty over `seal/specs/*/pr.*.md` | read |

Eight more read the corpus with no floor and would **silently assert less** —
`test_chain_hooks_hardening.py`, `test_handoff_outlives_the_merge.py`,
`test_waiver_decided_at_start.py`, `test_unverified_rows_close.py`,
`test_a_record_states_what_the_tree_has.py`,
`test_a_corrected_sentence_survives_elsewhere.py`, and the `git ls-tree HEAD`
arms of the two named above.

**Three things follow, and they are this spec's, not the fold's.**

1. The fold's prerequisites are **not** the two readers
   `docs/one-root-by-lifetime.md` §*The dependency rule* names. They are those
   two, the survivor sweep, and every population floor a repository's own
   checks carry over `seal/specs/`. The dependency rule was written in 0.4.0
   when there were 13 work items and most of those cases did not exist.
2. **This is general, not local.** Any repository running this methodology
   accumulates checks over its own records, and a floor is exactly the shape a
   check takes when its author worried about a vacuous pass. So
   `skills/settle/SKILL.md` carries the rule: a fold is not finished until
   every check with a population floor over the corpus has been answered — by
   retiring the case, by re-pointing it at a fixture corpus, or by declining.
   `tests/conftest.py`'s `decline_if_shrunken` is this repository's existing
   answer to the same shape and **not one of these fourteen uses it**.
3. It is the strongest argument for Q1's default. The mechanism's own review
   would otherwise run on a tree whose suite had just lost six cases to the
   very commit under review.

**One interlock does hold, and it is worth stating because it is what makes
removal safe at all.** `.github/scripts/fold_ledger.py#open_items` globs
`seal/specs/*/evidence-todo.md` for the release guard, and a fold that removed
those files would appear to disarm it. It does not: G3 makes `settle` skip and
name any item with an open row, so the only directories a fold removes are
ones the guard was never holding. Read on this tree 2026-09-22 — `open_items`
returns `[]` and no item is in that state.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · a removed work item is not read as this branch's deletion | Given a repository where a released work item's directory has been removed · When the hygiene workflow's unverified-record step runs · Then it does not report that directory's `overview.md` as deleted, and still reports one a branch actually deleted | a case over a fixture repository, shown red against the shipped code first (§15) |
| A2 · the changelog check stops passing on an empty corpus | Given a tree whose released work items have been folded away · When `gather_changelog.py --check` runs · Then it judges by the `<!-- specs/<id> -->` markers in `CHANGELOG.md` rather than by fragments that are gone, and says what it read | a case with a fragment removed and its marker absent, shown red first |
| A3 · the command names what it would fold, and folds nothing by itself | When `settle` runs with no write flag · Then it prints the released, unfolded work items grouped by segment, names the ungrouped ones, names any item skipped for an open `evidence-todo.md` row, and writes nothing to `docs/` and removes nothing | a case over a fixture root, and the dry run over this repository's own 97 |
| A4 · a second run folds nothing twice | Given a work item whose fold is recorded · When `settle` runs again · Then that item is neither listed nor folded, and an interrupted run resumes | a case over a fixture root with a partial record |
| A5 · an open evidence-todo row stops one item and not the run | Given one work item with an open `evidence-todo.md` row among several · When `settle` runs · Then that one is skipped **and named**, and the others are unaffected | a case over a fixture root |
| A6 · the command is reachable by the name a document gives it | When a shipped document names `settle` · Then `bin/settle` and `bin/settle.cmd` both exist and the document carries the command or the script's repo-relative path | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` |
| A7 · below the interpreter floor it says so before anything is read | Given a `python3` below the supported floor · When `settle` is invoked · Then it refuses at entry naming the version it needs, rather than dying in a traceback after argument parsing | the two cases `tests/test_a_script_says_which_interpreter_it_needs.py` already uses, extended to this script |
| A8 · both editions count the skill that shipped | When the suite runs · Then `README.md` says `Twenty-four` and `README.ko.md` says `스물네` in their skills rows, and `NUMBER_WORDS` carries the spelling for 24 | `tests/test_chain_hooks_hardening.py#test_both_readmes_count_the_skills_that_are_actually_there` |
| A9 · no document still describes a `settle` that does not exist | When the suite runs · Then `seal/README.md`, `templates/seal-README.md` and `skills/implement/SKILL.md` describe what ships, and `docs/one-root-by-lifetime.md` carries a dated section saying what #458 changed rather than a rewritten 2026-09-02 text | the wrap test, the survivor sweep, and a case pinning the corrected sentence in each file (§14) |
| A10 · the dry run over this repository is read, not assumed | When phase 6 closes · Then `overview.md` carries the run's own numbers — items foldable, segments, items skipped, items ungrouped — each labelled executed | the command's output, quoted |
| A11 · the skill names the floors a fold has to answer | When a session reads `skills/settle/SKILL.md` · Then it is told that the fold's prerequisites include every check in its own repository carrying a population floor over `seal/specs/`, with the three ways to answer one — retire, re-point at a fixture corpus, decline — and that the two readers named in `docs/one-root-by-lifetime.md` are not the whole list | a case pinning the sentence (§14), and the enumeration in this spec as its worked example |

## Data & interfaces

- **New**: `skills/settle/SKILL.md`, `skills/settle/scripts/settle.py`,
  `bin/settle`, `bin/settle.cmd`. `bin/` already ships
  (`tests/test_the_release_check_watches_what_ships.py`'s `SHIPS`), so the
  pair needs no new classification and the release's version move already
  covers it.
- **The fold record.** `settle` runs incrementally and records what it folded
  (G2, and `docs/one-root-by-lifetime.md` §*What keeps `settle` light*). Where
  that record lives is a phase-2 decision constrained by one thing this spec
  fixes: **it may not live inside `seal/specs/<id>/`**, because that is what
  the fold removes. The `<!-- specs/<id> -->` marker convention that
  `fold_ledger.py#marker` and `gather_changelog.py#marker` both already use is
  the candidate to reuse rather than to reinvent.
- **Released, defined.** A work item is released when its directory is present
  on the branch the release merges to. Measured on this tree: `origin/main`
  holds **97** of the 98, the exception being this work item. The two
  alternatives were measured and both are wrong — 11 work items carry no
  `<!-- specs/<id> -->` marker in `CHANGELOG.md` although several plainly
  shipped, and 15 carry none in `seal/ledger.md`.
- Nothing in `seal/ledger.md` is re-pointed, and no ledger row's anchor moves.

## `seal/follow-up.md`

Read 2026-09-22, in full. **No row is waiting on this work as its
prerequisite**, and none names `settle`, spec retirement or the size of
`seal/specs/`. Nothing is deleted from that file by this work item.

## Open questions → questions.md

Four rows, one of them a person's. Anything a planner must answer lives there,
not inline.

<!-- The line below is the framer's mark. -->

Framed 2026-09-22 by framer, before the build.
