# One plugin-owned root, laid out by lifetime

*English · [한국어](./one-root-by-lifetime.ko.md)*

Where the plugin's root sits, how a repository opts in, what first setup asks,
and how long each part of the root lives.

## The change in four lines

<!-- specs/1788331011-two-roots-hold-three-lifetimes -->
**One root the plugin owns holds everything, sorted by how long it lives.**
`seal/specs/<id>/` holds a work item until `settle` folds it into `docs/`;
`seal/ledger/<id>.md` holds its ledger rows until the release folds them; what
is permanent sits directly under `seal/`. Where the root sits is the
repository's choice, shared (committed) or local (under the common git
directory, never committed), and its presence there is the opt-in. A
repository still on the 0.3.x layout is moved once, by the session-start hook
`hooks/root-migrate.py`, never over uncommitted files, and every gate is silent
there until it runs; `skills/implement/orchestration.md` §*Orchestrator:
Bootstrap — create what's missing* says which marks make that layout. A `specs/` without them is the project's own: a
reference root, read as history and never written (`templates/config.md`
§*Reference specs*).
Enforced by: tests/test_no_document_names_the_old_roots.py::test_no_shipped_document_names_the_old_roots, tests/test_optin_home.py::test_the_legacy_directory_is_not_an_opt_in

## The proposed tree

One root the plugin owns: it creates, moves and folds it, and its checkers
define the formats, the way `.github/` is GitHub's.

```
<repo>/
├── seal/                          created, moved and folded by the plugin. Committed in shared mode.
│   ├── README.md                  this folder's rules: export rules, what moves when
│   ├── ledger.md                  the gathered ledger. Permanent
│   ├── ledger/<id>.md             rows of work items in development. Folded at release, then removed
│   ├── follow-up.md               permanent
│   ├── parity.md                  migration projects only. Permanent
│   ├── pact.md                    only in the repository that holds the pact. Permanent
│   ├── pact-changes/<id>.md       a signer's pact changes, written by --reverify. Permanent
│   ├── pact-reviews/<id>.md       the pact's repository's pact reviews. Permanent
│   └── specs/<work-item-id>/      the whole work item. Lives until settle folds it
│       ├── spec.md plan.md questions.md overview.md      the SDD set: what was decided and why
│       ├── changelog.md                                  gathered at release
│       ├── routing.md rounds/round-N.md                  what the commit gate and CI read
│       ├── tests-todo.md evidence-todo.md                evidence-todo must be empty before anything folds
│       └── pr.ko.md
├── docs/                          policy, and where settle folds the SDD set. Written by people and by settle
├── CHANGELOG.md
└── .git/                          never committed
    ├── seal/                      local mode only: the whole root above lives here instead of <repo>/seal/
    ├── specseal-planner           the framer mark. Session state
    ├── specseal-implementer       the smith mark. Session state
    └── specseal-worktree-choice/  the worktree question's record. Session state
```

| Lifetime | Lives in | Ends when |
|---|---|---|
| a session | `.git/` | the session ends |
| between releases | `seal/ledger/<id>.md` · `seal/specs/<id>/` | the release step folds the fragment; `settle` folds the work item |
| permanent | `seal/ledger.md` · `follow-up.md` · `parity.md` · `docs/` · `CHANGELOG.md` | never |

**Every `seal/…` path means `<repo>/seal/` where it exists, and
`$(git rev-parse --git-common-dir)/seal/` otherwise.** The `implement` skill
and the agents say so in one sentence; the hooks resolve it in code.

**What the names say.** `seal/specs/<id>/` holds the spec and its process
record. `seal/ledger*` is the binding of spec to code that breaks on drift —
what the product name seals, rather than one of the seals an agent takes
(`skills/verify/SKILL.md` §*Every agent seals what it verified, and one of
them is final*).

## What happens at a release

1. **`seal/ledger/<id>.md` folds into the release's ledger file**, and the
   fragment is removed; a work item still unmerged keeps its fragment. A move,
   not a deletion: every row survives, and after the merge no branch is left
   to queue at the file the fragment protected.
2. **`seal/specs/<id>/` folds into `docs/`, then the directory is removed.**
   This is `settle` (`skills/settle/SKILL.md`). It merges the SDD set of each
   released work item into a `docs/` document that exists, creating one only
   for a new area; the newest work item wins. Each folded sentence carries the
   work item id as an HTML comment, which is the fold record and the only one.
3. **The guard.** A sentence in a `spec.md` that must outlive the release has
   to be in a `docs/` policy or a ledger row before the merge. The release
   step refuses while a released work item has an open `evidence-todo.md` row,
   and `settle` skips such an item, naming it.

**The process record leaves after the release that ships its work item, fold
or no fold.** `settle --retire-process` removes it, and no check reads it once
its release has merged to `main`; what the SDD set still cites of it is read
at the release tag. Which files it is: `docs/the-record-layout.md`
§*seal/specs/<work-item-id>/*.

## The dependency rule

**Anything that must outlive a release may not read `seal/specs/<id>/` after
the merge.** `settle` removes the directory, so every permanent purpose treats
it as gone.

- **Safe.** A ledger row carries the clause text beside its coordinate. A
  round record's `Target SHA` is read only while the pull request is open. The
  HTML comment on a released entry names the work item, a pointer that git
  history still resolves.
- **The two readers a removal reached.** `unverified_check.py --baseline`
  compares the work-item tree against the merge base — the fork point on a
  branch checkout, and the base's tip in CI — and reads the fold record, naming
  a folded directory rather than reporting it gone.
  `gather_changelog.py --check` counts the markers in the release files and
  refuses a corpus with neither a fragment nor a marker. A check over the
  corpus with a population floor is a third kind, and `skills/settle/SKILL.md`
  holds what a fold owes it.
- **Kept on purpose.** The evidence-todo guard, the export rules in
  `seal/README.md`, and `settle` itself, the one sanctioned reader after the
  merge.

A new reader of `seal/specs/<id>/` after the merge is in the second group, and
review says so.

**Nothing may need to be found and updated when something else moves.** A
ledger row is a content anchor (`path#unit@hash`), so it changes state only
when its code does, and `settle` rewrites `docs/` and removes directories every
release; anything coupled to a path or position inside a work item breaks the
same way.

**What keeps `settle` light**:

- It moves and does not verify: whether a coordinate holds is
  `evidence-check`'s. The command reads and groups; the session judges what is
  still true and writes it.
- It runs incrementally: only work items released since the last fold, so an
  interrupted run resumes and nothing folds twice.
- A sentence carrying a work item's comment is replaced by the newer one;
  judgment is needed only when an area gets its first document.
- An item with an open `evidence-todo.md` row is skipped and named.
- A fold is not a work item: `skills/settle/SKILL.md` §*A fold is not a work
  item* says how it commits and where it is reviewed.

## What "spec" means after this

`spec.md` is the spec of one change. What outlives the change has two homes,
the `docs/` policy (policy > SDD > code) and the ledger row, and `settle` moves
it there. `docs/` is defined by who reads it, people; people write it, and
`settle` is the one writer that folds into it.

## The opt-in signal is the root itself, wherever the mode put it

<!-- specs/1788817289-local-mode-from-first-setup-to-the-gate -->
**A repository is opted in when `seal/` exists at its mode's location**:
`<repo>/seal/` in shared mode, `.git/seal/` in local mode. The hooks look at
the two places in that order; whichever exists says both "on" and which mode.
Nothing else is read, and there is no config key: in local mode the folder is
already a per-clone signal, and in shared mode a collaborator who never
installed the plugin runs nothing. A throwaway fixture opts out with the file
`.git/specseal-scratch` under the common git directory, which cannot be
committed. No folder at either place means not opted in, and a hook that
cannot tell does nothing.
Enforced by: tests/test_optin_home.py::test_new_home_opts_in, tests/test_optin_home.py::test_the_git_directory_is_the_second_place, tests/test_optin_home.py::test_the_shared_root_wins_when_both_exist

## What first setup asks

<!-- specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in -->
**The one moment this project allows a question is first setup, and it asks
one: shared or local.** One `AskUserQuestion` with two options, **shared**
first as the default, each saying what it does:

- **shared** creates `<repo>/seal/` in the tree, and the routing commit carries
  it; it installs `.github/workflows/hygiene.yml` from `templates/hygiene.yml`
  only where that path is absent.
- **local** creates `$(git rev-parse --git-common-dir)/seal/`, installs no
  workflow, and touches nothing in the tree.

A repository with `seal/` at either place, or still on the 0.3.x layout, is
never asked; the mode is read from where the folder is. The migration hook
stamps a repository whose root is at either place as moved, so a local-mode
repository that checks out an old branch is not moved into the tree.
Enforced by: tests/test_first_setup_asks_once.py::test_a_repository_with_the_root_at_either_place_is_never_asked, tests/test_first_setup_asks_once.py::test_the_two_options_are_named_in_order_with_shared_as_the_default

### Shared or local

<!-- specs/1788411058-the-mode-is-two-shell-lines-in-a-readme -->
<!-- specs/1788398967-local-modes-records-never-leave-the-clone -->
**The question is not "commit the folder or not" but "do CI and collaborators
see this workflow".** Which answer fits is mostly decided by whose repository
it is.

| | Local mode | Shared mode |
|---|---|---|
| Fits | a repository whose conventions keep this plugin's files out of the tree: a company repository, a contribution to someone else's project | your own repository, or any where a committed `seal/` bothers nobody |
| Where `seal/` lives | `.git/seal/`, inside the common git dir | `<repo>/seal/`, in the tree |
| Committed | never; nothing to gitignore either | yes |
| Linked worktrees and parallel sessions | read each other's records: the git dir is common | read each other's records: the files are committed |
| Other machines and a re-clone | start empty; `seal export` / `seal import` carry a copy by hand | have everything |
| CI (`ledger` and chain checks) | cannot run; the hygiene workflow is not installed | runs |
| Switching later | `seal mode shared` moves `.git/seal/` to `<repo>/seal/`, stages it and installs the workflow; you commit | `seal mode local` moves it back, stages the removal and takes the workflow out; you commit |

**`seal/config.md`'s `Mode` row is not a key, and the difference is what
reads it.** The row says where the root *should* be; the folder's location says
where it *is*, and no hook, gate or check resolves the root through the row —
`hooks/optin.py#home_at` is the only reader, in the two places above. A check
names a row and a folder that disagree, and an absent row is filled in from
where the folder is.

**Local mode installs no hygiene workflow, because a workflow left there is
red forever**: both checks read committed files and local mode commits none.
`unverified_check.py` exits 2 for a path that is nowhere and the job stops, so
`chain_check.py`, which would have exited 0 having examined nothing, never runs.

**Local mode lives under `.git/` and not in a gitignored folder**: a linked
worktree checks out committed files only, so an ignored `<repo>/seal/` is
absent in every worktree. `git rev-parse --git-common-dir` is shared by every
worktree of the clone, never a commit candidate, and needs no `.gitignore`
line.

**Local records never leave that clone on that machine.** A new machine or a
re-clone starts with no ledger and no work-item records, and CI's ledger and
chain checks cannot run. That is the whole trade-off, and the per-work-item
fragment layout, not branch isolation, keeps parallel items apart.

**Local records can be copied by hand, and a copy is not a sync.** The ledger's
rows are content anchors, so a copied ledger degrades to DRIFTED where the
other tree differs and never breaks; round records name pushed commits.
`.git/seal/` is its own folder so that it alone is copied, without the session
state beside it. Last copy wins, so needing a copy twice is the signal to
switch to shared mode.

**The mode is not a one-way door; the history is.** Records committed in
shared mode stay in the repository's history after a switch back, so the
command says so before it acts and stages rather than commits.

**Local mode gets an export/import pair**:

- `seal export` zips `.git/seal/` alone into `seal-<repo>-<date>.zip`, with a
  manifest naming the remote URL and the HEAD SHA at export.
- `seal import <zip>` never overwrites: an id already present lands as
  `<id>.incoming.md` beside the existing file, reported and not asked about;
  `evidence-check` then says which rows drift against this tree.
- The same pair is the mode switch: export, unzip into `<repo>/seal/`, commit.
- One reminder only: in local mode the release-preparation step prints "N work
  items changed since the last export". Nothing is uploaded anywhere.

Enforced by: tests/test_first_setup_asks_once.py::test_each_option_says_what_it_creates_and_what_it_installs, tests/test_optin_home.py::test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore

### Retention: measured, and answered by `settle`

**First setup asks no retention question.** What is worth keeping of a work
item, the SDD set, is folded into `docs/` by `settle`, and the process record
leaves after its release (§*What happens at a release*), so nothing in the
directory is left to choose about.

## Naming

**Product name: SpecSeal; bare `seal` is the vocabulary inside it.** The root
`seal/`, the `seal export` / `seal import` commands, "the seal" for the record.

| Name | Its one sentence | Why not |
|---|---|---|
| SpecSeal | seals a spec to the code that implements it | — names what and how; says "spec borrowed, seal ours" |
| Seal | seals | circular without its object; heavy collisions (Microsoft SEAL, kubeseal); unfindable as a marketplace name |
| AiSeal | seals what AI made | names the maker, not the thing sealed; the prefix dates; collisions |

**Root name: `seal/`, visible, rather than `.seal/`.** The items in flight are
what people read while a pull request is open; the hooks find the folder by
name and do not care about a dot.

**Sub-directory name: `seal/specs/<id>/`.** A directory says what is in it to
whoever opens it first; smith and warden stay agent personas and name no
directory.

**English is the language of every shipped artifact.** What language a
repository's own commits and records use is its config's
(§*What the repository decides for itself, and how it is read*).

## What the repository decides for itself, and how it is read

`seal/config.md` is the one file a repository writes about itself — one row
per item, read by the checkers and editable by hand. The rows are documented in
`templates/config.md`, and an absent row's default is stated there.

<!-- specs/1788420761-the-settings-live-in-a-file-nobody-opens -->
**A setting nobody can find is a setting nobody has.** Every row is reachable
from a command that shows the whole file and routes a change, because first
setup asks its questions in one batch and never asks again. The routing layer
holds no logic of its own: a row with a side effect routes to the script that
performs it, and a row that is only a row is written directly, because logic
inside a skill cannot be mutation-tested the way a script can.
Enforced by: tests/test_the_settings_have_a_front_door.py::test_the_skill_names_every_row_the_template_ships, tests/test_the_settings_have_a_front_door.py::test_the_skill_shows_rows_that_are_absent

<!-- specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill -->
**What language this plugin writes in is the repository's answer, not the
plugin's.** The language lives in a config row, and the mirror file a
translated pull-request body goes in is named for the language it holds.
Enforced by: tests/test_the_pull_request_language_is_the_repositorys.py::test_the_skill_names_the_file_and_the_row, tests/test_the_pull_request_language_is_the_repositorys.py::test_the_mirror_is_named_for_its_own_language

<!-- specs/1788420760-a-language-row-that-governs-four-things -->
**Two rows, because one cannot express the middle answer.**
`Commit and pull request language` governs what the outside world reads — the
commit subject and body, the pull request title and body — and
`Record language` governs the prose in the documents a work item writes.
Setting one does not carry the other: a pull request is read by whoever opens
it, and a record by whoever comes back to the decision six months later.
Whatever either row says, **the names a checker matches stay English** — the
field names, the verdict words, the markers, a ledger anchor, and all code.
Enforced by: tests/test_the_pull_request_language_is_the_repositorys.py::test_the_template_is_one_item_value_table_whose_first_row_is_the_language, tests/test_the_pull_request_language_is_the_repositorys.py::test_every_document_that_names_a_language_row_names_the_shipped_one

<!-- specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it -->
**A cell may carry an escaped pipe, and one line that will not parse is named
rather than treated as the end of the table.** The reader and the writer share
the constant that describes a row, so they agree on which line is a given row.
Enforced by: tests/test_the_mode_question_is_asked_once.py::test_an_escaped_pipe_is_one_row_and_the_rows_below_it_still_arrive, tests/test_the_mode_question_is_asked_once.py::test_a_line_that_will_not_parse_is_named_and_the_hook_still_says_nothing

<!-- specs/1788789329-a-git-call-that-fails-reads-as-no-remote -->
**A git call that fails is not a git call that answered "nothing".** Every call
site whose caller needs the distinction returns it, and the refusal says which
call failed rather than reporting a confident nothing — no remote, no other
worktree, no tracked file.
Enforced by: tests/test_the_records_can_be_carried_out_and_in.py::test_the_export_omits_a_remote_it_could_not_read, tests/test_the_records_can_be_carried_out_and_in.py::test_an_unreadable_remote_here_refuses_the_import, tests/test_the_mode_is_a_row_and_a_command.py::test_a_git_that_cannot_answer_does_not_report_no_submodule
