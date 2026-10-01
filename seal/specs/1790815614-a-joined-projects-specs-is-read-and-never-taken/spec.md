# Feature Specification: a joined project's `specs/` is read and never taken

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#688. A person joins a project that already has its own `specs/` and wants
to use SpecSeal there. Today the bootstrap reads that directory as the 0.3.x
layout and skips the shared/local question, and the session-start hook
stages a `git mv` of every `specs/<id>/` whose NAME has the shape a work
item's name has. The rule this work builds is the ticket's, written by the
repository owner: the plugin writes only to its own root, reads every other
`specs/` as history when a change needs it, and never moves, edits, absorbs
or deletes one. Every fact below is labelled `read` unless it says
`measured`; the frame executed nothing.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Whether a `specs/` is the plugin's is answered from its content, not by asking the person. A question a document could have answered was never a question |
| `docs/one-root-by-lifetime.md` §*The change in four lines* — "`specs/` stops being SpecSeal's directory" (line 30), and `hooks/root-migrate.py`'s docstring step 5, "anything else under `specs/` stays and is named, because `specs/` stops being SpecSeal's directory and a project may have had one first" | The design record already contemplates a project that had `specs/` first. This work narrows what the hook counts as *a work item* from a name to the plugin's own marks; it changes no decision in that record |
| `docs/one-root-by-lifetime.md` §*Decided after the thread*, row *The first-setup question's shape* — "A repository with `seal/` at either place, or still on the 0.3.x layout, is not asked" | Still true. What changes is what *on the 0.3.x layout* means: `.specseal/`, or a `specs/<id>/` carrying the plugin's marks. The record takes a dated section saying so, in the shape its 2026-09-22 and 2026-09-23 sections already use, in both editions (`tests/test_both_editions_carry_the_same_folds.py` compares the heading outlines) |
| `docs/one-root-by-lifetime.md` §*The opt-in signal is the root itself, wherever the mode put it*; `hooks/optin.py` module docstring | The plugin's own root is `<repo>/seal/` or `<git-common-dir>/seal/` and nothing else. A reference root is by definition outside it, so no reader of the root changes |
| `skills/settle/SKILL.md` §4 *Retire what the policy absorbed*; `skills/settle/scripts/settle.py#retire` (`SPECS = "seal/specs"`, `shutil.rmtree(under(root, f"{SPECS}/{work_item_id}"))`) | The retirement is already pinned to the root. This work adds the case that proves it against a planted team `specs/` and changes nothing in it |
| `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else* — "reports every place in the tree still carrying wording a range removed" | A team document the plugin never wrote is not a place a correction was owed. The standing statement gains the clause *outside the reference roots*, on the ticket's grounds; its `Enforced by:` line gains the new case |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*; §*Repo rule — commit early* (ledger rows name content, a drifted row is re-read and re-stamped with a dated note) | Rows anchored on `hooks/root-migrate.py#…`, the Bootstrap section heading and both READMEs' *Coming up from 0.3.x* sections drift under this work. Each is re-read; none is appended to in place. New claims go to `seal/ledger/1790815614-….md` |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures*; `tests/test_no_real_identifiers.py` | The planted team `specs/` fixture uses neutral names only |
| `templates/config.md` — "every absent row has a default, which is what every repository got before the row existed" | The `Reference specs` row is optional; its absence means the ticket's default, every directory named `specs` outside the root |

## Scope

**In.**

1. **The 0.3.x detection reads content.** A repository is on the 0.3.x
   layout when it holds `.specseal/`, or a `specs/<id>/` that carries the
   plugin's own marks. **The marks are `routing.md` directly under the
   directory, or a `rounds/` directory directly under it**, and the
   directory's name has the shape `ITEM_RE` already requires. Measured
   (read-only `git ls-tree` at tag `v0.3.0`): every one of the 13 work-item
   directories under `specs/` carried `routing.md`, and 29 `rounds/` files
   stood among them, so no 0.3.x work item is left behind by the content
   test. `spec.md`, `plan.md` and `overview.md` are not marks: a team's own
   specification may use those names.
2. **The bootstrap** (`skills/implement/orchestration.md` §*Orchestrator:
   Bootstrap — create what's missing*, the paragraph beginning *First, look
   for the 0.3.x layout*) sends a bare `specs/` — one with no marked
   directory — on to the shared/local question, and reserves the *told, not
   asked* path for the marked case. `tests/test_first_setup_asks_once.py#test_an_unmoved_old_layout_is_not_asked_but_told`
   stays green: the marked case is still told.
3. **The move hook** (`hooks/root-migrate.py`) moves a `specs/<id>/` only
   on that proof. An id-shaped directory without a mark stays where it is
   and is named in the printed line with the reason (*no `routing.md` or
   `rounds/`*), the way `specs/notes` is named today. The ledger re-point
   (`#repoint_path`) follows the moved set, not the name pattern, so a row
   citing an unmoved team directory keeps its path. A repository with
   nothing of the plugin's old layout stays silent, as the hook's *silent
   when there is nothing to do* boundary already says.
4. **A `Reference specs` row** in `seal/config.md`, documented in
   `templates/config.md`, names the reference roots; one resolver in
   `hooks/config.py` reads it and answers *is this repository-relative path
   under a reference root*. Absent, every directory named `specs` outside
   the plugin's root is one. §*Data & interfaces* has the shape.
5. **The checks that reach outside the root as a record stop doing so.**
   Counted by reading each shipped script's walk (the table below). Two
   read a reference root as a record and change: `survivor-check` (pool and
   range) and `unverified-check` (its directory walk). The rest are pinned
   already, or read the tree as the tree, and each gets the case that shows
   a planted team `specs/` is left alone.
6. **The readers say when they read a reference root and that they cite
   it.** `agents/framer.md` §*What you read, and how widely*,
   `agents/smith.md` §Phases step 1, `agents/warden.md` §Role (stage 1),
   `skills/settle/SKILL.md` §2, and one sentence in
   `skills/implement/SKILL.md` §*Document layout — two roots, three
   lifetimes*: a reference root is read-only history, read when the work
   touches what it describes, and what was read is cited in `spec.md` or in
   the settled statement. `templates/seal-README.md` and `seal/README.md`
   line 51 (*Nothing reads `.specseal/` or a top-level `specs/` any more*)
   are reworded to say nothing WRITES there.
7. **Both READMEs' §*Coming up from 0.3.x*** say the hook moves a marked
   directory and leaves the rest; the by-hand block stays as it is.
8. **The explicit adopt command is refused**, with its reason in §*What is
   refused* below. Box 5 of the ticket allows either answer.

**Out.**

- **#647's structure** — a hub, satellites, a `Records` row, who in a
  repository is a participant. 0.18.0 owns it. This work gives a
  satellite-shaped repository one thing only: its own `specs/` is read and
  never taken.
- **`seal adopt specs/<x>`** — refused, see below. A follow-on ticket can
  overturn it; the plan does not wait on it.
- **The commit gate's `DOC_ROOTS = ("docs/", "seal/")`**
  (`hooks/commit-review-gate.py#DOC_ROOTS`): an edit to a team `specs/`
  file counts as code-touching for the parity arm, which wakes only where
  `seal/parity.md` is declared. That is a gate's wake rule, not a check
  reading a record, and nobody has met it. Left as it is; the repository
  owner opens an issue if a parity repository with a reference root meets
  the prompt.
- **`settle`'s citation scan** (`settle.py#tracked_text`, `#citations`)
  reads every tracked text file outside `seal/specs/` for a `specs/<id>/`
  path into a retiring directory. A reference root's file is read there as
  a *citer*, never as a record, and a hit needs the team directory to carry
  the retiring work item's own id. Left as it is and named in the table.
- **`evidence-check`'s tree corpus and relocation hint**
  (`evidence_check.py#tree_names`, `#scan_candidates`) walk the whole tree
  on purpose: *a name in any other file is a name the tree has*, and a
  hint names where a unit may have gone. Neither reads a reference root as
  a record. Left as it is and named in the table.
- **Local mode's own root.** A reference root is always in the tree; the
  plugin's root may be under the git directory. The predicate is on
  repository-relative tree paths, so local mode needs no arm of its own.
- **The hook's `dirty()` reading `git status -- .specseal specs`** refuses
  a `.specseal/` move while a team `specs/` has uncommitted work. A joined
  project holding `.specseal/` is the plugin's own old layout, so the case
  is not this work's; named here so the builder does not widen the move
  into it.

### The checks, counted

Read from each script's walk; the `Reaches outside the root` column is the
ticket's question, and the verdict is this work's.

| Check | What it walks | Reaches outside the root as a record | Verdict |
|---|---|---|---|
| `survivor-check` (`skills/code-review/scripts/survivor_check.py`) | `#corpus` → `#tracked`: every path in the tree at `b`, less `#records_a_past_state` and gathered fragments; `#corrected`: every path the range changed; `#WORK_ITEM_DIR = ^((?:seal/)?specs/[^/]+)/` asks `retired_by_rule` of a removed top-level `specs/<x>/` | **Yes**, on both sides: a sentence a branch removed can "survive" in a team document, and a team document the range edited becomes a source | change: reference roots out of the pool and out of the range, one predicate on both sides (the `records_a_past_state` precedent); `WORK_ITEM_DIR` narrowed to `seal/specs/` |
| `unverified-check` (`skills/verify/scripts/unverified_check.py`) | `#overviews(paths)` walks whatever paths it is handed; `templates/hygiene.yml` and `broad_gate.py` hand it `seal/specs/`, and by hand it defaults to `.` | **Yes**, under the default path: a team `specs/<x>/overview.md` is read as a record | change: the directory walk prunes reference roots; a file path named explicitly is still read |
| `correction-check` (`skills/evidence-check/scripts/correction_check.py`) | `#ledger_listing`: `git ls-tree` of `seal/ledger.md`, `seal/ledger/`, `seal/releases/` | No | pinned; gets the planted case |
| `evidence-check`, ledger arm | `seal/ledger.md`, `seal/ledger/*.md`, `seal/releases/*.md`, `docs/**/_evidence.md` | No (`docs/**/_evidence.md` is the plugin's own pre-0.10 name) | pinned; gets the planted case |
| `evidence-check`, records arm | `#unshipped`: `<home>/specs/<id>/` for every live `<home>/ledger/<id>.md`; `<home>/follow-up.md` | No | pinned; gets the planted case |
| `evidence-check`, tree corpus and hint | `#tree_names`, `#scan_candidates`: the whole tree, as the tree | Outside the root, not as a record | left; named in §Scope *Out* |
| `settle` (`skills/settle/scripts/settle.py`) | `#work_items`, `#released`, `#open_items`, `#has_spec`, `#retire`: `seal/specs/` only; `#folded_items` (shared reader): top level of `docs/`; `#tracked_text` → `#citations`: every tracked text file outside `seal/specs/` | `--retire`: no. Citations: outside the root, as a citer | pinned; gets the planted case (`--retire` leaves the team directory on disk; the report is unchanged by it) |
| `chain_check.py` | `git ls-tree HEAD -- seal/specs/` (`routing.WORK_ITEMS`) | No | pinned; gets the planted case |
| `hooks/routing.py#declarations` | the working tree under `seal/specs/` | No | pinned by `WORK_ITEMS` |
| `deferral-check`, `arm-check`, `fold-check` | no walk of `specs/`; `fold-check` reads the top level of `docs/` and `seal/config.md` | No | nothing to do |
| `broad-gate` | hands `seal/specs/` and `seal/specs/*/survivors.md` to the checks above | No | nothing to do |

The ticket's figure *530 files at #674's round 2* for the survivor pool was
not located in any round record under `seal/specs/` (read: a grep over
`rounds/round-2*.md`); it is the ticket's and nobody's finding here. The
phase that changes the pool prints the examined count before and after on
this repository, which is the measurement that matters.

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist and the
regression tests' skeleton. Each ticket box is seen red first, against the
old code or with the sentence it pins deleted, and the hand-back says how.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · A bare `specs/` reaches the shared/local question (box 1, first half) | Given the Bootstrap section; when a session reads the 0.3.x paragraph; then it says a `specs/` with no marked directory is NOT the 0.3.x layout and goes on to the question, and names the two marks | `tests/test_first_setup_asks_once.py`: a new case reads the paragraph and asserts `routing.md`, `rounds/` and the bare-`specs/` sentence; red with the sentence deleted. `test_an_unmoved_old_layout_is_not_asked_but_told` stays green |
| A2 · The 0.3.x path needs the plugin's marks (box 1, second half) | Given a repository holding `.specseal/` or a marked `specs/<id>/`; then the paragraph still says *told, not asked*, and the condition is content, not a name | same file; the ledger row Q7 (`seal/releases/0.10.0.md`) re-read with a dated note |
| B1 · `root-migrate` moves nothing without the marks (box 2) | Given a committed `specs/1788000001-team-thing/spec.md` with no `routing.md` and no `rounds/`; when the session-start hook runs; then the directory is where it was, nothing is staged for it, the marker is stamped only if something of the plugin's moved, and the printed line names `specs/1788000001-team-thing` with the reason | `tests/test_the_root_migrates_itself.py`: new case, red against the old `old_items` (which moves it); the fixture's marked item still moves (`test_the_first_session_start_moves_the_tree_and_says_so_in_one_line` green) |
| B2 · A row citing an unmoved id-shaped directory keeps its path | Given a ledger row anchored at `specs/1788000001-team-thing/spec.md`; when the hook re-points; then the path is unchanged and the checker's totals are equal before and after | same file, beside `test_a_row_citing_a_foreign_specs_entry_is_left_where_it_is`; red against the old `repoint_path` |
| B3 · A marked directory with only `rounds/` still moves | Given `specs/<id>/rounds/round-1.md` and no `routing.md`; then it moves | same file; a pin, shown red by removing `rounds/` from the marks in a probe |
| C1 · The row and its default (box 3, mechanism) | Given `seal/config.md` with `Reference specs \| specs/, docs/adr/`; then the resolver answers those two prefixes; given no row, then every directory named `specs` outside the plugin's root; given `none`, then no reference root | `tests/test_a_reference_root_is_read_and_never_taken.py` (new): row present, absent, `none`, a row inside a fence (not a row, `hooks/config.py#unfenced`), local mode (every tree `specs` is a reference root) |
| C2 · The readers read the reference roots when relevant, and cite what they read (box 3) | Given the four definitions and the settle skill; then each names the row, the absent-row default, *read when the work touches what it describes*, and *cite it in `spec.md` / the settled statement* | same new file: a case per document asserting the row's name and the citing sentence; `tests/test_docs_line_wrap.py` and `tests/test_no_document_names_the_old_roots.py` green |
| D1 · The survivor sweep leaves a team `specs/` alone (box 4) | Given a range that removes a sentence from a plugin document while a team `specs/x/design.md` carries it verbatim; then it is not reported as a survivor, and a team file the range edited is not a source | `tests/test_a_corrected_sentence_survives_elsewhere.py`: two new cases, red against the old `corpus`/`corrected` |
| D2 · `unverified-check .` leaves a team `specs/` alone (box 4) | Given `specs/x/overview.md` with a malformed `## Not verified` section; when run from the repository root with the default path; then it is not read and the exit is 0; when the file is named explicitly, it is read | `tests/test_unverified_rows_close.py`: red against the old `overviews` |
| D3 · `settle --retire` and the pinned checks leave a team `specs/` alone (box 4) | Given a planted `specs/1788000001-team-thing/` beside a retirable `seal/specs/<id>/`; then `settle --retire` removes the latter and the former is on disk unchanged; `evidence-check`, `correction-check` and `chain_check.py` report nothing about the team directory | `tests/test_settle_reads_before_it_removes.py` and the new file: pins, each shown red in a probe by widening the constant it rests on (`SPECS`, `LEDGER`/`FRAGMENTS`/`RELEASES`, `WORK_ITEMS`) |
| E1 · The adopt path is refused in the spec with its reason (box 5) | §*What is refused* below | read; the review's stage 1 reads it |
| F1 · The READMEs and the design record say what the hook now does | Given both READMEs' *Coming up from 0.3.x* and both editions of `docs/one-root-by-lifetime.md`; then they say a marked directory moves and the rest stays, and the design record carries one dated section in both editions | `tests/test_both_editions_carry_the_same_folds.py`, `tests/test_the_root_migrates_itself.py#test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set` green; the README rows in `seal/releases/0.4.0.md` re-read |

## Data & interfaces

**The marks.** `hooks/root-migrate.py` gains one constant, `MARKS =
("routing.md", "rounds")`, and `old_items` keeps an id-shaped directory
only when one of them exists directly under it (`routing.md` a file,
`rounds` a directory). `moves`, `repoint_path` and the symlink refusal in
`main` read the same set. The hook's docstring step 5 and the Bootstrap
paragraph name the same two words, so a reader of either finds the test.

**The row.**

```markdown
| Reference specs | specs/, docs/adr/ |
```

- The value is one or more repository-relative directory prefixes,
  separated by commas, each with or without a trailing `/`. `none` declares
  no reference root. Absent, empty or unreadable means the default.
- The default, with no row: **every directory named `specs` outside the
  plugin's root**, at any depth, in the tree. The plugin's root is
  `<repo>/seal/` in shared mode; in local mode it is under the git
  directory, so every `specs` directory in the tree is a reference root.
- The reader is `hooks/config.py#reference_roots(home)` (the row through
  `config_rows`, under the root `hooks/optin.py#home_at` resolves, the way
  `fold_check.py` reads its three rows) and
  `hooks/config.py#under_reference_root(rel, roots)`, a predicate on a
  repository-relative `/`-joined path. Scripts load `hooks/config.py` by
  path, as `broad_gate.py` and `fold_check.py` already do; there is no
  second copy of the row's grammar anywhere.
- A row inside a code fence or a closed HTML comment is not a row
  (`hooks/config.py#unfenced`, `templates/config.md` §*Broad gate*).

**What the row governs.** Which paths `survivor-check` leaves out of its
pool and range, and which directories `unverified-check` prunes from a
walk. What it does not govern: the retirement, which is `seal/specs/`
whatever the row says, and the readers' prose, which names the row and
its default.

**Printed lines.** `root-migrate`'s tail gains the reason:
`; left specs/1788000001-team-thing where it is (no routing.md or rounds/
— not a SpecSeal work item)`, beside the existing `(not tracked as a
SpecSeal work item)` for a non-item name. The new text is pinned by the
case that sees it (§15 of the contract).

## What is refused

**`seal adopt specs/<x>` is not built in this work item.** The ticket's
box 5 allows either answer; this is the refusal and its reason, read from
the tree.

- A directory that carries the plugin's marks needs no command: the hook
  moves it at the next session start, and the by-hand block in both
  READMEs (`git mv specs/<id> seal/specs/<id>` then `evidence-check
  --reverify .`) is the same move for a person who will not wait. That is
  the existing adopt path for the plugin's own shape, and it already shows
  the diff and leaves the commit to the person.
- A directory that does not carry the marks is a team's document, and
  moving it under `seal/specs/` hands it to the root's lifetime rules
  without the record that lifetime assumes. `settle`'s rule arm retires a
  released directory with no `spec.md` and nothing open
  (`unverified_check.py#retired_by_rule`), and one with a `spec.md` is
  listed as waiting to fold with no ledger row to group it by. What is
  still true in a team document belongs in `docs/`, which is a fold — the
  `settle` skill's act, written by a session — and not a move.
- So an adopt command would do one of two things that already exist, or a
  third thing the root's own rules then undo. The owner can overturn this
  with a follow-on ticket that says what *adopted* means for a document
  without the plugin's record; nothing in this plan waits on it.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. `questions.md`'s head
lists what this frame decided from the tree, so nobody reopens it.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-01 by framer, before the build.
