# 1788411058-the-mode-is-two-shell-lines-in-a-readme — review round 1

<!-- The first round on #104's implementation (target: 7b00c85 against
f173b83). It opened four 🔴 — three of them lose a record or send a person
down a path that does not work — so the bound is five rather than three while
one is open, and round 2 verifies the fixes. Written by the review
orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | the whole branch from its base f173b83, reviewed at 7b00c85 |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | round-2 |
| Contract changes | `indexed` → `refusals`, `switch`; `remove_workflow` → `switch`; `table_span` → `with_row`; `gitlinks_under_root` → `refusals`; `mode` → `main` |
| New units | `CONFIG_PATHSPEC`, `gitlinks_under_root`, and seven test cases |
| Needs a fix | yes — 🔴 1 (the row this command writes makes the next switch refuse), 🔴 2 (the way back it names is blocked by its own guard), 🔴 3 (an untracked workflow file is removed with no copy anywhere), 🔴 4 (a failed `git add` is reported as staged), 🟡 5 (two `Mode` rows never converge), 🟡 6 (`--check` passes when no repository resolves), 🟡 7 (a submodule under the root breaks at exit 0), 🟡 8–10 (documents) |

- [ ] Pass

## What this round was asked to attack

Recorded because a round's findings cannot be read against a round that was
asked something else, and nothing else keeps it. The prompt named: **every
path this command moves, removes, creates or renames** as the class to
enumerate before probing — the root at both places,
`.github/workflows/hygiene.yml`, `seal/config.md`, and whatever the rename
walks over — and for each, what happens when it is a link, a broken link,
occupied, occupied by something that is not a directory, on another
filesystem, or changed between a check and its use.

Then, in order: whether a record can be lost by interrupting the run at each
step; the four `git rm -r --cached` tree states the smith measured plus the
ones it did not; `--check` as a gate that must not fail open; that nothing
but `seal mode` reads the row; the two spec claims the smith corrected
mid-build; every unit's mutation; and every document against what executes.

It was also told one fact the orchestrator had got wrong and the smith had
corrected — that both CI checkers exit 0 in a repository with no `seal/`,
when `unverified_check.py` exits 2 — and asked to check what the branch says
about it against the true values. That instruction is what found 🟡 8.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `seal mode` fills an absent `Mode` row in from the folder. Where `config.md` is TRACKED that write leaves ` M seal/config.md`, and the switch the person runs next refuses over the file the reporting command just wrote. The `??` exception written for exactly this reached the untracked spelling only — and the tracked one is every repository `hooks/root-migrate.py` carried over from the 0.3.x layout, whose `.specseal/config.md` arrives committed. That is the population #104 exists for | `skills/implement/scripts/seal.py:1416-1419` | fixed at e3d71b2 — `CONFIG_PATHSPEC`, and a worktree-only change to that one file no longer refuses. A STAGED edit still does | reviewer executed it; orchestrator reproduced it independently on a tracked `config.md` with no `Mode` row: `seal mode` then `seal mode local` exits 1, and exits 0 after the fix. The planted case reddens when the clause is removed |
| 🔴 2 | the switch to shared prints that `seal mode local` walks it back until the commit, twice. It stages, and the guard refuses a switch over a staged change, so the command it names cannot run. The same sentence stood in five places, one of which folds into `CHANGELOG.md` at the release | `skills/implement/scripts/seal.py:1746`, `:1836`, `README.md`, `README.ko.md`, `changelog.md` | fixed at e3d71b2 — both sentences say `git reset` first, and so do both READMEs and the fragment | reviewer executed the sequence; orchestrator reproduced it before and after. **The case that covered this asserted the command was NAMED** — `assert "seal mode local" in out` — so it read the words and never the way back. The new case runs the way back and counts both sentences |
| 🔴 3 | an untracked `.github/workflows/hygiene.yml` was removed with `os.remove`. Git holds no copy, so that was the only one. The guard watches this path in `git status --porcelain` for exactly that reason, and the untracked exception was reasoned from a file under the root — which travels with the folder either way. This one does not travel and is not under the root. `spec.md` S18 promised a refusal | `skills/implement/scripts/seal.py:1577` | fixed at e3d71b2 — an untracked workflow is left and named, and the `os.remove` branch is gone | reviewer executed it: exit 0, file gone, nothing tracked. **No mutation reached the branch** — the fixture always commits the workflow, so the input did not exist |
| 🔴 4 | `git add` failing was reported as `staged seal/`, followed by `Now commit`. `git()` reads a failure as `""`, and the local direction has checked the return code since it was written while this side had not. An ignore rule matching the root reaches it, and so does a held `index.lock` | `skills/implement/scripts/seal.py:1827-1828` | fixed at e3d71b2 — the return code is read and the failure names what a commit would record | reviewer executed both causes. The planted case uses the ignore rule and reddens when the check is disabled |
| 🟡 5 | `config_rows` reads the FIRST `Mode` row and `table_span` writes the LAST, so a file with two of them disagrees with itself and no number of runs closes it. CI stays red with no way out but editing by hand | `skills/implement/scripts/seal.py:1245` against `:1289` | fixed at e3d71b2 — the writer takes the first match | reviewer executed it and reports the first/last mutant survived. The planted case reddens when the guard is removed |
| 🟡 6 | `--check` answers `no seal/ here` and exits 0 where no git repository resolves — including a `repo_root` timeout or a git that is not on PATH, which is a shared root committed beside a row saying `local` going unchecked. A gate that cannot tell reads exactly like an allow, which is issue #28's shape | `skills/implement/scripts/seal.py:1841-1848` | fixed at e3d71b2 — an unresolvable repository exits 1 saying the check could not run | reviewer executed both shapes |
| 🟡 7 | a submodule under the root switches at exit 0 and breaks: the gitlink leaves the index, `.gitmodules` goes on naming the path, and the moved root's relative gitdir is gone. `spec.md`'s *What the switch touches* table — which says it is enumerated rather than fixed where a finding points — had five members and needed six | `skills/implement/scripts/seal.py:1811-1819` | fixed at e3d71b2 — `gitlinks_under_root`, refused before anything moves | reviewer executed it. The planted case skips where a git refuses a file-protocol submodule |
| 🟡 8 | three documents drew a wrong conclusion from exit codes that were right: `templates/hygiene.yml`, `docs/one-root-by-lifetime.md` and its Korean mirror all say a workflow left behind would *go green having examined nothing*. A step exiting 2 is not a green build. The orchestrator's own correction fixed the numbers and left the sentences they supported | `templates/hygiene.yml:16`, `docs/one-root-by-lifetime.md:342`, `.ko.md:323`, and both files' summary tables | fixed at e3d71b2 — all five places say both directions, and two existing cases were moved to the true values | reviewer re-derived the exit codes without a pipe: `unverified_check.py` 2, `chain_check.py` 0 |
| 🟡 9 | `templates/hygiene.yml` still told a person to install it by hand, after this branch made `seal mode shared` write it | `templates/hygiene.yml:19-22` | fixed at e3d71b2 | reviewer executed the switch and watched the file arrive pinned |
| 🟡 10 | five more documented claims wider than what runs: the workflow "carried in and out" where six branches do not carry it, both READMEs' tree line naming one config row, the refusal sentence covering `seal/` only, the skill's singular "edit the value", and `bin/seal` listing three of four spellings | `README.md`, `README.ko.md`, `seal/README.md`, `templates/seal-README.md`, `skills/commit-pr-convention/SKILL.md` | fixed at e3d71b2, except `bin/seal`'s example list — deferred below | reviewer read each against what executes |

## The class this round enumerated, and what it cost the round before it

The prompt asked for the class rather than the coordinates, and three of the
four 🔴 are members of one: **a path this command touches that its own guard
reasoned about for a different member.**

- the `??` exception reasoned from *a file under the root* — and was applied
  to the workflow, which is not under the root (🔴 3);
- the same exception reached the untracked spelling of `config.md` and not
  the tracked one (🔴 1);
- the return code was read on one direction and not the other (🔴 4).

`spec.md`'s own class table says it is enumerated *"rather than fixed where a
finding points, because that is what #81 cost seven rounds"* — and it listed
five members where there were six.

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the index in eight states, `--check` in eleven, and the switch against a submodule, an unmerged entry, a source link, a broken destination, an empty destination and a linked `config.md` | four 🔴 and three 🟡 |
| reviewer: 59 mutations against the two test files | 18 survived — 69% detection |
| reviewer: both CI checkers in a repository with no `seal/`, without a pipe | 2 and 0 |
| orchestrator: a tracked `config.md` with no `Mode` row, before and after | exit 1, then exit 0 |
| orchestrator: `seal mode shared` then the way back it names, before and after | exit 1 both times before; the first sentence still false after the second was fixed, then both true |
| orchestrator: seven mutations, one per fix | six reddened their own case; the seventh did not — the case counted one of two sentences, and now counts both |
| orchestrator: full suite, `ruff check .`, `ruff format --check .`, `evidence_check --strict`, `unverified_check --baseline` | 1588 passed · 1 skipped; clean; 84 files; 435 ok · 0 drifted · 0 broken; exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| — | none; this is the first round | — |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `bin/seal`'s example list names three of four spellings | this record | the repository owner, at the next edit of that file |
| `--check` reports agreement when both roots exist, where `refusals` calls the same state unswitchable | `questions.md` Q2, beside the fail-or-warn question already there | the repository owner |
| `config.md` as a directory: `--check` exits 0 saying nothing is declared | `overview.md` §Not verified | the repository owner |
| Windows: `os.rename` across filesystems, `git rm -r --cached` pathspec spelling, the cases that skip without link permission | the pull request's windows leg | the windows leg |
