# Feature Specification: two roots hold three lifetimes

<!-- specs/1788331011-two-roots-hold-three-lifetimes/spec.md — WHAT this work
delivers and how we'll know. `docs/one-root-by-lifetime.md` outranks this
file; it is cited, not restated. Phase 1 of plan.md moves this directory to
seal/specs/<id>/ with every other work item. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §"The proposed tree" | one plugin-owned root, committed in shared mode: `seal/README.md`, `seal/ledger.md`, `seal/ledger/<id>.md`, `seal/follow-up.md`, `seal/parity.md`, `seal/specs/<id>/…`. Three lifetimes, each with one home |
| §"The opt-in signal is the root itself, wherever the mode put it" | opted in means `seal/` exists at the mode's location, `<repo>/seal/` first and `.git/seal/` second; no config key; cannot tell means not opted in |
| §"What first setup asks", the shared half | the once-per-repo moment creates `<repo>/seal/`; the mode question needs a second answer to be a question, and that answer is #80 |
| §"What happens to the existing directories at the switch" | every work item moves whole, released or not; the session-start hook does it once, never over uncommitted files, with a marker of its own; `map.md` and `map/` become `ledger.md` and `ledger/`; `specs/` ends up empty here and goes away |
| §"What it touches in this repository" | the per-area list this work starts from: hooks 11 · skills 13 · tests 20 · templates 8 · .github 2 · agents 3 · docs 3 · root 4 (re-counted below) |
| §"The dependency rule" | nothing permanent may read `seal/specs/<id>/` after the merge, and nothing may need finding and updating when a path moves; a new reader lands in the "must change before `settle`" group and the review says so |
| §"What does not change" | every gate's fail direction; fragments per work item; `.git/` session state; `CHANGELOG.md` and the judgment order; every file a work item writes today |
| §"Order", step 3 | 0.4.0 is the root merge in shared mode only; local mode, the setup question, `config.md` and export/import are 0.5.0 |
| §"Decided after the thread" | nothing is deleted before `settle` folds it; the opt-in is the folder |
| §"Decisions left open", rows 1–4 | the names, and the `scratch` opt-out — the working answers are in `questions.md` Q1 and Q4 |
| `docs/review-handoff-protocol.md` §"Why the records moved a second time" | no fallback ships with a move: a reader that finds the old location says which file is in the wrong place and where it goes, and stops. Reading both locations forever was rejected there, and this work inherits the rejection |
| `CLAUDE.md` §"Repo rule — commit early" | a ledger row names no commit, so the move is free to be several commits; `plan.md`'s Status column names the commit that closed each phase |
| issue #79 "Done when" | the acceptance list; S1–S16 below cover each line |

## Scope

**In.**

- The tree: `.specseal/` and `specs/` become `seal/`, laid out by lifetime.
  In this repository the move is made by this branch, by hand with `git mv`,
  so the pull request carries it; the hook below is for every other
  repository.
- The opt-in: `hooks/optin.py` reads `seal/` at two places and nothing else;
  the throwaway opt-out moves out of the tree.
- The migration: a session-start hook that moves an existing `.specseal/`
  and `specs/<id>/` once per repository, with its own marker, refusing a
  dirty tree, and re-pointing the ledger rows that cite a moved file.
- Every gate, checker and release script on the new paths, and the one
  reader that would otherwise judge fifteen declarations on this pull
  request (`chain_check.py`, S10).
- CI: `hygiene.yml`'s path argument; `test.yml`'s `ledger` job unchanged
  because the checker's defaults move.
- Templates, skills, agents and documents re-pointed; the two READMEs
  together; the test fixtures on the new paths.
- The record: `seal/ledger/<id>.md` rows for what was executed, the closing
  memo, the changelog fragment.

**Out.**

- Local mode's creation, the first-setup question and the hygiene workflow
  install (#80). 0.4.0 creates nothing under `.git/seal/`; whether it
  already *looks* there is Q3.
- `seal/config.md` (#82), `seal export` / `seal import` (#81).
- `settle` (#83). Nothing is deleted; the two readers the record names as
  "must change before `settle`" are re-pointed and not redesigned.
- Renaming the plugin, the hook-file prefixes, or `~/.claude/specseal/`
  (the per-machine state directory keeps its name; Q1).
- Rewriting prose paths inside round records, overviews and plans of
  released work items. They record what was true at their SHA.
- `docs/one-root-by-lifetime.md` and its Korean twin. The design record
  names both trees on purpose.

## The tree after this work, in this repository

```
seal/
├── README.md                      from templates/seal-README.md; the export rules
├── ledger.md                      was .specseal/map.md
├── ledger/<id>.md                 was .specseal/map/<id>.md — 7 fragments today
├── follow-up.md                   was .specseal/follow-up.md
└── specs/<epoch>-<slug>/          was specs/<epoch>-<slug>/ — 15 work items today
    ├── spec.md plan.md questions.md overview.md changelog.md
    ├── routing.md rounds/round-N.md tests-todo.md evidence-todo.md
    └── pr.ko.md
```

`parity.md` is not in this repository and moves the same way where it is.
`.git/specseal-implementer`, `.git/specseal-worktree-choice/` and the session
leases stay. `specs/` and `.specseal/` do not exist afterwards.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the tree | Given this branch after phase 1, then `seal/` holds the tree above, `git log --follow` on any moved file reaches its history, and neither `specs/` nor `.specseal/` exists | test over this repository (`tests/test_release_hygiene.py` shape); `git log --follow --oneline seal/ledger.md` read by hand |
| S2 opt-in is the root | Given a repository with `seal/` at the root, then `optin.home()` returns it and `opted_in()` is true; given `.git/seal/` and no `<repo>/seal/`, the same (Q3); given neither, `""` and false; given both, `<repo>/seal/` wins and nothing else is read | `tests/test_optin_home.py` |
| S3 `.specseal/` no longer opts in | Given a repository with `.specseal/` and no `seal/`, then every gate is silent, and the only thing that speaks is the migration hook at session start | `tests/test_optin_home.py`; the commit gate, review-skill gate and implementer hooks on such a fixture |
| S4 the throwaway opt-out moves out of the tree | Given `<git-common-dir>/specseal-scratch` is a file, then `home()` is `""` and every gate is silent; given a directory of that name, it is not the marker; given the old `.specseal/scratch` file, nothing reads it (Q4) | `tests/test_optin_home.py`, the existing scratch cases re-pointed; `test_this_repository_carries_no_scratch_marker` removed, because a file under `.git/` cannot be committed |
| S5 the migration moves once | Given a clean repository with `.specseal/` and `specs/<id>/…` and no `seal/`, when the session-start group runs, then the tree above exists, every move was a `git mv` (staged, history kept), one line is printed naming what moved, and `~/.claude/specseal/root-migrated` carries the root. A second session start does nothing | `tests/test_the_root_migrates_itself.py`, new, in the shape of `tests/test_the_ledger_migrates_itself.py` |
| S6 a dirty tree is refused | Given `git status --porcelain -- .specseal specs` prints anything, or git cannot answer, then nothing moves, no marker is stamped, and one line says why and what to do (text below) | the same test file |
| S7 the move resumes | Given a run that stopped after some moves (`seal/` and `.specseal/` both exist), then the next session start moves what remains and stamps only when nothing old is left | the same test file; a fixture with `seal/ledger.md` already moved and `.specseal/map/` not |
| S8 rows that cite a moved file follow it | Given a ledger row whose anchor path starts with `specs/` or `.specseal/`, then after the move the path reads `seal/specs/…` or `seal/…` with the hash unchanged, and `evidence_check.py` reports the same ok · drifted · broken totals before and after. On this repository: 160 ok before (executed, this branch at `07a0fc8`), one such row (`.specseal/map.md` citing `specs/1788184145-…/rounds/round-3.md`) | the same test file on a fixture; `evidence_check.py .` executed before and after phase 1's move, both outputs in the fragment |
| S9 a repository declaring itself throwaway is not migrated | Given `.specseal/scratch` exists, then the hook prints one line and stamps nothing; the repository stays as it is | the same test file |
| S10 a moved declaration is not one this pull request made | Given a pull request whose diff renames `specs/<id>/routing.md` to `seal/specs/<id>/routing.md`, then `chain_check.py --baseline` judges only declarations added or modified, plus the one for this branch — never a renamed one | `tests/test_chain_check_at_the_pull_request.py`; executed on this branch against `origin/release/v0.4.0` after phase 1, output in the fragment |
| S11 the commit gate reads `seal/specs/<id>/routing.md` | Given a declaration there naming the current branch, then a commit passes silently for either review answer; given none, the gate asks as before and its prompt names the new path; given a commit confined to `docs/` and `seal/`, the parity arm stays asleep | `tests/test_routing_is_recorded.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_gate_judges_the_repo_it_commits_to.py` |
| S12 every checker's default is the new path | `evidence_check.py .` reads `seal/ledger.md` and `seal/ledger/*.md` (and `docs/**/_evidence.md` still); `evidence-advisor.py` and `ledger-migrate.py` the same globs; `fold_ledger.py` folds `seal/ledger/*.md` into `seal/ledger.md` and reads `seal/specs/*/evidence-todo.md`; `gather_changelog.py` reads `seal/specs/*/changelog.md`; `unverified_check.py` is given `seal/specs/` by the workflow; the parity config is `seal/parity.md` | the existing test files for each, re-pointed; `hygiene.yml` read |
| S13 the markers do not change | Given a released entry marked `<!-- specs/<id> -->` in `CHANGELOG.md` or `seal/ledger.md`, then `--check` still finds it, and a new fold or gather writes the same marker text (Q2) | `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_the_ledger_fragments_fold_at_release.py`; `gather_changelog.py --check` executed on this branch |
| S14 the once-per-repo moment creates `seal/` and asks nothing new | Given a repository with no `seal/`, when the `implement` skill bootstraps, then it creates `seal/README.md` and `seal/ledger.md` from the templates, says in three lines what it created, and asks the parity question as today; the mode question is not asked (Q6) | `skills/implement/SKILL.md` read; `tests/test_the_set_a_work_item_always_has.py` |
| S15 no document, skill, agent or template names the old roots | Given the files in the plan's re-point list, then none contains `.specseal/` or a bare `specs/<` path, except the design record and its twin, and `hooks/root-migrate.py`, which reads the old names on purpose | a test over the list, the shape of `test_release_hygiene.py`'s document cases |
| S16 no new permanent reader | Given the diff of this work, then the only code reading `seal/specs/<id>/` after the merge is what the record already lists (`unverified_check.py --baseline`, `gather_changelog.py --check`, the evidence-todo guard), plus one ledger row (Q7); the round records say so | the round record's verdict table; `grep -rn "seal/specs" hooks skills .github` read at the last round |

## Rules the scenarios lean on

### Which entries of `specs/` are SpecSeal's

The migration moves a directory `specs/<name>/` when `<name>` matches
`^[0-9]{9,10}-[A-Za-z0-9._-]+$`, the shape `date +%s` and a slug produce.
Anything else under `specs/` stays where it is and is named in the printed
line, because `specs/` stops being SpecSeal's directory and a project may
have had one before the plugin arrived. `specs/` is gone afterwards only if
git left it empty, which is what happens here.

### The move, in order

1. `.specseal/map.md` → `seal/ledger.md`
2. `.specseal/map/` → `seal/ledger/`
3. `.specseal/README.md` → `seal/README.md`, then overwritten from
   `templates/seal-README.md` (Q5)
4. every other file directly under `.specseal/` → `seal/<same name>`
   (`follow-up.md`, `parity.md`, anything a project added)
5. each `specs/<id>/` → `seal/specs/<id>/`
6. in every ledger the hook reads (`seal/ledger.md`, `seal/ledger/*.md`,
   `docs/**/_evidence.md`), every anchor whose path starts with
   `.specseal/map.md`, `.specseal/map/`, `.specseal/` or `specs/` is
   rewritten to the new prefix. The hash after `@` is not touched: it covers
   the cited content, which did not change.
7. the marker line for the root is appended to
   `~/.claude/specseal/root-migrated`.

Every step is a `git mv` or a rewrite of a file git already tracks, so
`git diff --cached` shows the whole of it and nothing is lost if the person
resets. A step that fails stops the run at that step, prints what moved and
what did not, and stamps nothing; S7 is what makes the next start finish it.

### What the session prints, and what it refuses

| State at session start | Printed (one line, `systemMessage`) | Marker |
|---|---|---|
| clean, moved | `specseal: moved .specseal/ and N work items into seal/ (M ledger rows re-pointed) — review the diff and commit` | stamped |
| dirty | `specseal: .specseal/ and specs/ are the old layout, but they carry uncommitted changes — not touching work in progress. Commit, then the next session start moves them into seal/.` | not stamped |
| `.specseal/scratch` present | `specseal: .specseal/scratch says this repository is throwaway — not migrating it. Delete the file if it is not.` | not stamped |
| a move failed | `specseal: moved K of N into seal/ and stopped at <path>: <error>. The next session start continues.` | not stamped |
| nothing old left | nothing | stamped, if not already |
| marker already carries the root, old layout still there | nothing: the once-per-repo rule holds and the silent gates are the backstop | — |

The last row is the ledger hook's rule applied here, and it is the one
place the two migrations differ in weight: a ledger left in the old format
fails `evidence-check` loudly, where a tree left in the old layout gets
silence from every gate. Q8 asks whether that row should keep printing.

### The opt-in, read one way

`optin.home(cwd)` returns the first of `<root>/seal/` and
`<git-common-dir>/seal/` that is a directory, or `""`. It returns `""` when
`<git-common-dir>/specseal-scratch` is a file. Every hook builds its paths
from that answer (`os.path.join(home, "specs", id, "routing.md")`), so #80
changes where the folder is created and nothing that reads it. Readers that
classify repository-relative paths — the commit gate's `DOC_ROOTS`, the CI
scripts' globs, `chain_check.py`'s prefix — use `seal/` as a string, because
a path in a diff or a tree listing is only ever the shared root.

### The dependency rule, applied to this work

- `hooks/root-migrate.py` reads `.specseal/` and `specs/`, never
  `seal/specs/<id>/`; it is a reader of the old tree that can be deleted
  once no repository is left to migrate, and it carries a rider saying so.
- The ledger row citing `specs/1788184145-…/rounds/round-3.md` is a
  permanent row reading a work-item directory, which `settle` will remove.
  It is re-pointed here and named in Q7; it is not silently fixed.
- No other reader of `seal/specs/<id>/` is added. The three the record
  names are re-pointed in place.

## Data & interfaces

| Where | Today | After |
|---|---|---|
| `hooks/optin.py:25` `HOME` | `".specseal"` | `"seal"`; `home()` tries the common git dir second; `SCRATCH` becomes `specseal-scratch` under the common git dir |
| `hooks/routing.py:55` `WORK_ITEMS` | `"specs"` | `"seal/specs"`, and `declarations()` joins it under `optin.home()` |
| `hooks/commit-review-gate.py:480` `DOC_ROOTS` | `("docs/", "specs/", ".specseal/")` | `("docs/", "seal/")` |
| `hooks/commit-review-gate.py:857, 883` prompt text | `specs/<work-item-id>/routing.md` | `seal/specs/<work-item-id>/routing.md` |
| `hooks/ledger-migrate.py:67`, `hooks/evidence-advisor.py:111`, `evidence_check.py:1378` | `.specseal/map.md`, `.specseal/map/*.md`, `docs/**/_evidence.md` | `seal/ledger.md`, `seal/ledger/*.md`, `docs/**/_evidence.md` |
| `evidence_check.py:814` | `.specseal/parity.md` | `seal/parity.md` |
| `.github/scripts/fold_ledger.py:79-80, 252` | `.specseal/map.md`, `.specseal/map`, `specs/*/evidence-todo.md` | `seal/ledger.md`, `seal/ledger`, `seal/specs/*/evidence-todo.md`; `marker()` and `MARKER_LINE_RE` unchanged |
| `.github/scripts/gather_changelog.py:65` | `specs/*/changelog.md` | `seal/specs/*/changelog.md`; `marker()` unchanged |
| `skills/code-review/scripts/chain_check.py:438` | `p.startswith("specs/")` | `seal/specs/`, and renamed paths excluded (S10) |
| `.github/workflows/hygiene.yml:107` | `specs/` | `seal/specs/` |
| `hooks/dispatch.py:46` `session-start` | `version-check.py, ledger-migrate.py` | `version-check.py, root-migrate.py, ledger-migrate.py` |
| `hooks/root-migrate.py` | — | new; `MARKER = ~/.claude/specseal/root-migrated`; reads the old names and nothing else does |
| `templates/specseal-README.md`, `templates/map.md` | | `templates/seal-README.md`, `templates/ledger.md`; the five SDD template headers name `seal/specs/<epoch>-<slug>/` |
| `<!-- specs/<id> -->` in `CHANGELOG.md` and the ledger | | unchanged (Q2) |

The old tree gets no fallback reader. A `routing.md` at `specs/<id>/` after
this change is a file in the wrong place, and the commit gate's prompt says
where it goes; that is the handoff-protocol precedent, applied.

## Open questions → questions.md

Anything a planner must answer lives in `questions.md`, not inline.
