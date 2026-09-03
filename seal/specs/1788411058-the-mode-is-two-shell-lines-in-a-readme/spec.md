# Feature Specification: the mode is two shell lines in a README

<!-- seal/specs/1788411058-the-mode-is-two-shell-lines-in-a-readme/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself" | The presence of `seal/` at one of two places is the opt-in **and** the mode. This work adds a row that must not become a second answer to that question — §"The row is not the signal" below is what keeps it from being one |
| `docs/one-root-by-lifetime.md` §"Shared or local" → *A copy is not a sync, and the modes convert into each other* | "The setup choice is *where does it live now*, not a one-way door" — true of the mode and **not** true of the history. §S12 is where that correction lands |
| `docs/one-root-by-lifetime.md` §"Shared or local" → the switching rows | `move .git/seal/ to <repo>/seal/ and commit` is the whole of what exists today. This work is that sentence made runnable, plus the four parts a `mv` cannot do |
| `templates/config.md` §"Repository config" | The file's shape — one markdown table, one row per item, optional, an absent row is not an error. The `Mode` row is the second row and obeys all of it |
| `templates/hygiene.yml` header, *Why local mode installs no copy* | Already states, correctly, that the two checks read committed files and what each does in a repository that has none. This work makes the switch carry the file rather than leaving a person to act on that paragraph |
| `seal/README.md` §"Export rules — drain before closing" | The word *export* already has a meaning in the root. This document uses **switch** for what `seal mode` does and never *export* |
| `CONTRIBUTING.md` §"Hooks stay local and quiet" | A hook may not move a person's files. `seal mode` is not a hook: a person types it, and nothing in the plugin calls it |

## Scope

**In.**

- A `Mode` row in `seal/config.md`, documented in `templates/config.md`.
- `seal mode` in `skills/implement/scripts/seal.py`, beside `export` and
  `import`: a report, a check with an exit code, and two directions of an
  applied switch.
- The refusals a `mv` has no way to make, and the two halves a `mv` leaves
  behind — the index and `.github/workflows/hygiene.yml`.
- Both READMEs' *Shared or local* section, `docs/one-root-by-lifetime.md`
  and its Korean mirror, and the `implement` skill's bootstrap, which is
  where a repository that was never asked finds out it can still choose.
- A CI step, in this repository's `.github/workflows/hygiene.yml` and in the
  `templates/hygiene.yml` shared mode installs.

**Out.**

- **Committing.** The command stages and stops. The two README lines end in
  *then commit* and so does this; a plugin that commits into someone's
  repository is the act `CONTRIBUTING.md` keeps hooks away from, and the
  commit gate is downstream of it besides.
- **Any runtime reader of the row.** No hook, no gate and no check resolves
  the root through `config.md`. §"The row is not the signal".
- **A "start fresh" command.** The issue's own *Not this* section: discarding
  the ledger and the work-item records is discarding the evidence chain, and
  it stays a deliberate act done by hand.
- **Syncing between machines.** `seal export` / `seal import` already own
  that, and the switch names them rather than repeating them.
- **Undoing history.** Nothing here rewrites, filters or removes a commit.

## The row is not the signal

The objection that killed this idea the first time is that a file *inside*
`seal/` cannot describe where `seal/` is. It can, as long as it describes
where it **should** be while something else decides where it **is**.

| | Says | Read by | Can be wrong |
|---|---|---|---|
| The folder's location | where the records are | every hook and check, through `hooks/optin.py#home_at` | no — it is the files themselves |
| The `Mode` row | where the repository wants them | `seal mode` and its CI check, and nothing else | yes, and that is the point: a disagreement is the input the command consumes |

**Nothing at runtime may read the row**, and the reason is not tidiness: a
gate that trusted a hand-editable row would go looking in a place with no
folder, and everything in `hooks/optin.py` is documented to fail toward *not
opted in* rather than toward a guess. The row can be edited by anyone with a
text editor; the folder is where the files actually are.

**The row has no default at all. An absent one is written from the folder.**
Every repository that has a `config.md` today has one row in it — the
pull-request language #82 shipped — so *the row is absent* is not an edge
case, it is the state of every existing repository on the day this ships.
`seal mode` with no argument fills it in from where the folder actually is:
`home_paths` gives both places and exactly one of them exists, so the first
value the row ever carries is an observation rather than an assumption. It
says that it did so, and reports. It is not an error and not a question.

Two defaults were being conflated, and they stay apart:

| | Applies when | What it is |
|---|---|---|
| The first-setup question's default — shared, offered first | `seal/` exists at **neither** place | An answer pre-selected in a question a person answers. `tests/test_first_setup_asks_once.py` pins it and nothing here changes it |
| The `Mode` row | the folder already exists, which is the only way to read the row at all | **No default.** It is written from an observation or from a person's edit, and nothing ever falls back to a value |

**An absent row cannot mean "uninitialised", because `config.md` lives inside
`seal/`.** Reading the row at all requires having already resolved the
folder, and resolving the folder has already answered the question the row
would be answering. The absence that means uninitialised is the absence of
the **folder** — which is what `hooks/optin.py#home_at` returning `""`
already is, and it is read before anything opens a config file. This is
§"The row is not the signal" arriving from the other side: the row cannot be
the signal even when it is missing.

`--check` never writes. It is a check, it runs in CI, and an absent row is
nothing to disagree with — so it reports the row as not declared and passes.

## User scenarios & acceptance *(mandatory)*

### The report and the check

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given a repository whose row names a mode, when `seal mode` runs, then it prints the mode the folder says, the mode the row says, and whether they agree — and moves nothing, stages nothing, and exits 0 | `tests/test_the_mode_is_a_row_and_a_command.py` — compare the root's file list and the index before and after |
| S2 | Given no `Mode` row — no file, no such row, an empty value, or a file that does not parse as that table — when `seal mode` runs, then it writes the row from where the folder is, says it did, reports agreement, and exits 0 | S2 case, one per shape, in **both** modes: the value written is the folder's, never a fixed one |
| S2b | Given the row was just written by S2, when `seal mode` runs a second time, then it writes nothing more and reports the same mode | S2b case: bytes of `config.md` compared across the second run |
| S2c | Given a `config.md` that cannot be written — a directory at that name, a symbolic link, a root with no write permission — when `seal mode` runs, then it says the row could not be written, still reports the mode from the folder, and exits 0 | S2c case, three shapes |
| S2d | Given no `Mode` row, when `seal mode --check` runs, then it writes nothing at all and exits 0 | S2d case: a check may not mutate the tree it checks |
| S3 | Given a row naming the mode the folder is in, when `seal mode --check` runs, then it exits 0 | S3 case, both modes |
| S4 | Given a row naming the other mode, when `seal mode --check` runs, then it exits 1, names both sides, and names the two commands that end the disagreement — the one that moves the folder and the one that corrects the row | S4 case, both directions |
| S5 | Given a `Mode` row whose value is neither `local` nor `shared`, when `seal mode --check` runs, then it exits 1 naming the value; `--apply` refuses; the report says the row names no mode | S5 case |
| S6 | Given a repository with no root at either place, when `seal mode --check` runs, then it exits 0 saying there is no root here — a workflow that outlived its root fails on the checks that read records, not on this one | S6 case |
| S7 | Given a repository with no root at either place, when `seal mode`, `seal mode local`, `seal mode shared` or `seal mode --apply` runs, then each exits 1 naming both places the root is looked for | S7 case, four spellings |

### Switching

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S8 | Given a shared-mode repository with a clean tree, when `seal mode local` runs, then the root is at `<git-common-dir>/seal/`, `<repo>/seal/` is gone, every tracked path under it is staged as a deletion, the `Mode` row reads `local`, and the run exits 0 | S8 case: assert the two paths, `git status --porcelain`, and the row |
| S9 | Given a local-mode repository, when `seal mode shared` runs, then the root is at `<repo>/seal/`, staged as an addition, and the `Mode` row reads `shared` | S9 case |
| S10 | Given a repository already in the mode asked for, when `seal mode <that mode>` runs, then it finishes what is unfinished — the row, the index, the workflow file — says so, and exits 0 | S10 case: a root already moved by hand with the index untouched |
| S11 | Given an edited row and a folder that disagrees, when `seal mode --apply` runs, then the folder moves to what the row says and the two agree afterwards | S11 case, both directions |
| S12 | Given the local → shared direction, when it runs, then before anything is moved it says that a commit puts the records in the history for good, that `seal mode local` walks it back only until that commit, and that removing them later removes them from the tree and not from the history | S12 case: read stdout, assert the line precedes the *now commit* line |
| S13 | Given the shared → local direction, when it runs, then it says every other clone loses the records at the next pull and names `seal export` / `seal import` as how a teammate gets a copy | S13 case |

### Refusing

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S14 | Given both roots exist, when any applying spelling runs, then it refuses, names both paths and which one the gates read, and writes nothing | S14 case, three spellings |
| S15 | Given anything at all under `seal/` in `git status --porcelain` — a modification, a staged edit, an untracked file, a deletion — when an applying spelling runs, then it refuses naming the porcelain lines, and nothing moves | S15 case, four shapes |
| S16 | Given the destination path already exists as anything — a file, a directory, a symbolic link, a broken link — when an applying spelling runs, then it refuses naming it, and nothing moves | S16 case, four shapes |
| S17 | Given the source root is a symbolic link rather than a directory, when an applying spelling runs, then it refuses rather than moving the link, and nothing moves | S17 case |
| S18 | Given `.github/workflows/hygiene.yml` is dirty in `git status --porcelain`, when an applying spelling runs, then it refuses before moving anything | S18 case |
| S19 | Given the rename cannot be performed — the two paths are on different filesystems, or the destination's parent cannot be written — when an applying spelling runs, then it refuses, names the error, and prints the `mv` that does work, and nothing else has been done | S19 case: a destination parent with its write bit cleared |
| S20 | Given a `config.md` that is a directory, a symbolic link, or unreadable, when an applying spelling runs, then it refuses before moving anything, naming the path | S20 case, three shapes |

### The workflow file, which is the half a `mv` leaves behind

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S21 | Given shared → local and a `.github/workflows/hygiene.yml` this plugin wrote, when the switch runs, then the file is removed from disk and from the index, and the removal is named | S21 case |
| S22 | Given shared → local and a `hygiene.yml` this plugin did not write, when the switch runs, then it is left alone, the switch still completes, and the report names the file and says the checks it runs will read nothing | S22 case: a file with the same name and someone else's content |
| S23 | Given local → shared and no `.github/workflows/hygiene.yml`, when the switch runs, then the file is written from `templates/hygiene.yml` with `v<version>` replaced by the installed plugin's version, and staged | S23 case: assert no `v<version>` survives and the version matches `.claude-plugin/plugin.json` |
| S24 | Given local → shared and a file already at that path, when the switch runs, then it is never overwritten, and the report says it was left alone | S24 case |
| S25 | Given local → shared and a plugin version that cannot be read, when the switch runs, then no workflow is written at all — a `v<version>` left in the file makes CI's `git clone --branch` fail — and the report names the by-hand step | S25 case: an unreadable `plugin.json` |

### Worktrees

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S26 | Given a clone with more than one worktree, when an applying spelling runs, then the report names every other worktree and what root it will read until it checks out the commit — and the switch still completes | S26 case: a linked worktree, both directions |

## Fail direction — what each guard does when it cannot tell

A guard that cannot answer must not act. Every unanswerable question here is
answered the same way, and it is the direction `hooks/root-migrate.py#dirty`
already takes: *treat it as work in progress and refuse.*

| Question | Cannot answer → | Why that direction |
|---|---|---|
| Is the tree clean under `seal/`? | refuse | Moving on a guess is the one direction with no undo: `git rm -r --cached` drops a staged edit out of the index with nothing printed (measured, S15's grounds) |
| Is this path a symbolic link? | refuse | `os.path.lexists` answers it without following; there is no unanswerable case, and a link followed is a move out of the root |
| Is `hygiene.yml` this plugin's? | leave it | Removing someone else's file is the destructive direction. The report says what was left and what it means |
| What version is installed? | write no workflow | A workflow carrying a literal `v<version>` fails CI's clone at the first pull request, which is worse than no workflow — and the report names the by-hand copy |
| Does the row name a mode? | report it, fail `--check`, refuse `--apply` | A value that is not a mode is a claim nobody can act on. The three other ways of not declaring (absent, empty, unparseable) are *no claim* and pass |
| The row is absent — what value goes in it? | **the folder's**, never an assumed one | The folder is observable and the row is not yet anything. A fixed default would write `shared` into every undeclared local-mode repository, which is the lie the check exists to catch, produced by the command that reports it |
| The row cannot be written | say so, report from the folder anyway, exit 0 | A person asked where things stand and that answer is available without the write. Failing the report would make an unwritable config a reason not to answer a question |
| Is there a root at all? | `--check` passes, everything else refuses | A check that fails where there is nothing to check teaches people to delete the check |

### Why the workflow file has to move with the root — measured, not asserted

Run in a repository with no `seal/` at all, 2026-09-03, both checkers of
`templates/hygiene.yml` at `d57a992`:

```
unverified_check.py --baseline base-ref seal/specs/
  unverified-check: no such path: seal/specs/ — and nothing under it at
  base-ref either, so there is nothing to compare it against      exit 2

chain_check.py --baseline base-ref
  this pull request declared neither way, so the review-chain check
  examined nothing.                                               exit 0
```

The two fail in opposite directions, and a workflow left behind after a
switch to local gets both at once:

- `unverified-check` goes **red on every pull request**, permanently, for a
  repository whose records are correctly out of the tree. Nobody can fix it
  except by deleting the workflow, which is what the switch should have done.
- `chain-check` goes **green having read nothing**, which is the silent-gate
  shape this repository designs against everywhere else: a check that cannot
  load reads exactly like a check that passed.

Going the other way and not writing the file is the same defect mirrored — a
repository whose records are committed and whose pull requests examine none
of them, with nothing on screen to say so.

`templates/hygiene.yml`'s own header already states both exit codes
correctly. What did not exist was anything that acted on them.

## Data & interfaces

### The row

```markdown
| Item | Value |
|---|---|
| Pull request language | English |
| Mode | local |
```

| | |
|---|---|
| Values | `local`, `shared`. Read case-insensitively, written lowercase — every document spells the modes that way |
| Absent, empty, or unparseable | no claim; nothing disagrees |
| Any other value | a claim that names no mode: reported, fails `--check`, refuses `--apply` |
| Written by | `seal mode local`, `seal mode shared`, `seal mode --apply`. A person may hand-edit it and then run `seal mode --apply` — that is the flow the issue describes |
| Parsed by | the same two-cell `Item` / `Value` table shape `templates/parity.md` and the pull-request-language row already use |

### The command

```
seal mode              report: the folder, the row, whether they agree.
                       An absent row is written from the folder first
seal mode --check      the same report, writing nothing; exit 1 on a
                       disagreement
seal mode local        switch to local mode, and write the row
seal mode shared       switch to shared mode, and write the row
seal mode --apply      switch to whatever the row says
```

**The bare command never moves a folder.** It may write the row, and only
ever with what it just observed — a value that cannot be wrong, in the one
file whose absence is the state every existing repository is in.

`--check` and `--apply` are refused together with a direction, and with each
other.

**`--check` fails where `export --check` never does, and the difference is
whose fault the state is.** `seal export --check` reports how many work items
changed since the last export — an honest state nobody did wrong, and a red
build for one teaches people to stop exporting. A mode disagreement is always
the author's, and always one command from fixed.

### What the switch touches — the whole class

Every path this command moves, removes, creates or renames, with the guard
that stands in front of it. The class is enumerated here rather than fixed
where a finding points, because that is what #81 cost seven rounds:

| # | Path | What happens to it | Guard |
|---|---|---|---|
| 1 | `<repo>/seal` ↔ `<git-common-dir>/seal` | renamed | source is a directory and not a link · destination does not `lexists` · both roots do not exist at once · the rename itself may fail, and then nothing else has run |
| 2 | index entries under `seal/` | `git rm -r --cached` going to local, `git add` going to shared | the tree is clean under `seal/` · skipped entirely when git tracks nothing there, because the pathspec would fail |
| 3 | `<home>/config.md` | the `Mode` row written, the rest of the file preserved | not a link, not a directory, readable |
| 4 | `.github/workflows/hygiene.yml` | written going to shared, removed going to local | that path is clean · written only when absent · removed only when it is this plugin's · not written at all when the version cannot be read |
| 5 | `.github/workflows/` | created going to shared | a failure to create it refuses before anything moves |

Path 5 is the one a coordinate-shaped fix would have missed: it is not a file
anybody names, it is created as a side effect of path 4, and on a repository
with no `.github/` at all it is the first thing that can fail.

### Order, and what a stopped run leaves

The rename runs first, because it is the step that can fail for reasons
outside this command, and until it succeeds nothing else has happened. Each
step after it is idempotent, so a second run finishes a stopped one — the
same property `hooks/root-migrate.py` has, for the same reason.

1. every guard above, in one pass, writing nothing
2. rename the root
3. write the `Mode` row
4. the index: `git rm -r --cached` or `git add`
5. the workflow file
6. print what was done, what is left, and the commit to make

A run that stops at step 4 or 5 says which step and what remains, and
`seal mode <the same mode>` afterwards does only the missing parts. That is
also what makes S10 — a person who already ran the README's `mv` by hand —
land on a working path rather than a refusal.

### Where the check lives, and why not in `skills/verify/scripts/`

`seal mode --check`, called from both hygiene workflows.

The check compares two facts the command already resolves: where the folder
is, through `hooks/optin.py#home_at`, and what the row says. A checker script
of its own would be a **second reader of both** — the drift `hooks/optin.py`
exists as a module to prevent ("Imported by the gates rather than copied into
each, because the answer moved once already"), and the same reason
`root_files` in `seal.py` carries the comment *this is the only walk*.

The two script directories are about other things: `skills/verify/scripts/`
reads the SDD record set (unverified rows, deferrals, session cost) and
`skills/evidence-check/scripts/` reads the ledger. Neither reads the root's
own config, and putting the first such reader in either would make the
directory mean something new.

**What the check can and cannot see.** In local mode nothing is committed, so
there is no CI and the row is not in the tree — the only disagreement that
can ever reach a pull request is *the row says local and the folder is
committed in the tree*, which is exactly the document that lies. The check is
complete over what CI can observe, and that is worth saying plainly rather
than leaving someone to discover the asymmetry.
