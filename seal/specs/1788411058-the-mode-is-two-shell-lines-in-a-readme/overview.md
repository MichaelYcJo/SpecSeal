# 1788411058-the-mode-is-two-shell-lines-in-a-readme — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"The opt-in signal is the root
            itself", §"Shared or local" (the switching rows, *A copy is not a
            sync*); `templates/config.md`; `templates/hygiene.yml`'s header;
            `seal/README.md`; `README.md` §"Shared or local";
            `skills/commit-pr-convention/SKILL.md` §"The language is the
            repository's"; `skills/implement/SKILL.md` §Bootstrap; issue
            #104; this work item's `spec.md`, `plan.md`, `questions.md`,
            `routing.md`
· evidence: 9 rows in
            `seal/ledger/1788411058-the-mode-is-two-shell-lines-in-a-readme.md`
· verified: **Executed** — `tests/test_the_mode_is_a_row_and_a_command.py`
            (61), `tests/test_first_setup_asks_once.py` (34),
            `tests/test_docs_line_wrap.py`,
            `tests/test_the_pull_request_language_is_the_repositorys.py`;
            `ruff check` and `ruff format --check` on the files this branch
            wrote; 29 mutations, one at a time. **Read** — nothing load-
            bearing; the two git behaviours this rests on were measured
            rather than read

## Why this work exists

Switching between shared and local mode worked only as two shell lines a
person had to find in a README, and a repository arriving from the 0.3.x
layout landed in shared without ever being asked — so the people most likely
to want local mode were the ones least likely to know it was still available.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| An untracked file under `seal/` | `spec.md` S15 and the issue both said "refuse when `git status --porcelain` reports **anything** under `seal/`" | Refuse only what the index carries; name an untracked file and proceed | The guard's whole grounds is that `git rm -r --cached` drops a staged edit out of the index without a word. The index cannot lose what it never had, and the file travels with the folder in both directions. Found by running the command rather than by reading it: the bare `seal mode` writes an absent row, so the switch a person runs next met the file it had just written and refused. S15b is the case; `spec.md` and the fail-direction table were corrected in place |
| A deletion under `seal/` while the move is already done | The same rule, which refused it | Allowed, and only once the destination holds the root | It is the shape a stopped run — or the README's by-hand `mv` — leaves behind, and refusing it means a resume can never finish. `hooks/root-migrate.py#dirty` makes exactly this exception in the same words. `MD` and `AD` still refuse, because a staged edit is precisely what is dropped silently |
| `.github/workflows/` being preflighted | `spec.md` §"What the switch touches" said a failure to create it refuses before anything moves | Reported at the step, and retried by a second run | Preflighting it means creating it — a write during a pass whose contract is to write nothing. The resume property makes it unnecessary, and the row was corrected in place |
| What CI does with a workflow that outlived its root | The handoff said both checks pass, so the leftover is a green build that read nothing | Both fail directions recorded, and they are opposite | Measured 2026-09-03: `unverified_check.py` exits **2** for a path that is nowhere and `chain_check.py` exits 0 having examined nothing. So the leftover is a build that is red forever for a repository doing the right thing, beside a check reporting a pass it never earned. `templates/hygiene.yml`'s own header already said both exit codes correctly; nothing acted on them |
| `seal mode` with no argument | The issue reads "with no argument after an edited row, applies the row"; the spawn prompt read it the other way | Report only, and `--apply` applies the row. The bare command does write an absent `Mode` row, from the folder | `questions.md` Q1 carries both halves. A command typed to find out where things stand must not move directories; a row written from an observation the command just made cannot be wrong |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, `ruff check .`, and a repository-wide format check | the review orchestrator's broad gate, once the rounds settle. This branch ran the suites for what it touched and lint on the files it wrote, per the verification-scope rule |
| Windows: `os.rename` across a repository and its common git directory, `git rm -r --cached`'s pathspec spelling, and whether a `config.md` symbolic link is refused where the platform has no link privilege | the Windows CI leg on the pull request. Every case that needs a link goes through `symlink_or_skip`, so on a runner without the privilege those cases skip rather than pass — which is a hole a green Windows leg does not close |
| Whether refusing a switch is right when the clone has other worktrees, rather than the note this builds | the repository owner. `questions.md` Q7 has the measurement and the alternative |
| Whether `seal mode --check` should fail a pull request or warn on it | the repository owner. `questions.md` Q2 |
| Whether first setup should write the `Mode` row when it creates the root | the repository owner. `questions.md` Q6 |
| Whether a `config.md` that is a directory should refuse the report as well as the switch — today the report says so and still answers | the repository owner |

## Not done

**No `--dry-run` on the switch.** `seal mode` is the dry run: it reports
without moving anything, and every refusal is decided before the first write.
A flag would be a third spelling of an answer the command already refuses to
take twice.

**No undo.** `seal mode local` walks a shared switch back only while it is
uncommitted, and nothing here rewrites history. That is stated where it
happens rather than automated: `questions.md` Q3.

**The row is not read by anything else.** No hook, gate or checker learned to
read `config.md`, and the `Mode` row deliberately gained no runtime reader —
which is the constraint that let it exist at all.

## What was fed back into the spec

- **The class of paths the switch touches** (`spec.md` §"What the switch
  touches") — five entries, and the fifth is `.github/workflows/`, which is
  not a file anybody names and is the first thing that can fail in a
  repository with no `.github/`. Inferred during implementation.
- **`--check` fails where `export --check` never does** — the difference is
  whose fault the state is. Written into `spec.md` §"The command" so the two
  are read together.
- **The four spellings of "not declared" and the fifth that is not one of
  them.** A row whose value is neither mode is a claim nobody can act on, and
  treating it as absent would overwrite what a person meant. Inferred.

## Mutation record

29 mutations, one at a time, each applied to the shipped file and reverted
from a copy the harness took — never from HEAD, which would have taken the
uncommitted work in the same file with it.

28 reddened at least one case. The 29th did not, and it should not have: it
reworded a bold sentence in `README.md` without changing what the section
does, and a case that reddens for a rewording pins prose rather than
behaviour.

Three cases were empty when first written, and each is now the mutation that
proves it:

| The case said | What it actually tested | Now |
|---|---|---|
| a version that cannot be read writes no workflow | it pointed `PLUGIN_ROOT` at an empty directory, which removes the **template** as well — so it passed through the unreadable-template branch and said nothing about the version. A fallback to `0.0.0` left it green | `plugin_version` is what is removed, and the message is asserted to name that reason |
| both READMEs name the command first | an index comparison between two strings, which survived deleting the command block outright — `seal mode local` appears in the prose above the by-hand block too | the section's first runnable block must carry both directions of the switch |
| going to shared says the commit is the door | it matched "history" in a sentence a partial mutation left intact | the whole warning is the mutation, and the case reddens for it |
