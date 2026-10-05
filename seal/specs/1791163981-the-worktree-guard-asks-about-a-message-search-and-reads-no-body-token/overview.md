# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `routing.md` of this item; `docs/worktree-guard-spec.md` §*A. Branch switch*, §*Choice sites*, §*Unknowns resolve conservatively*, §*Which tree, when the command walks to it*, §*Known limits*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; 1791119071's `rounds/round-2-report.md` §*Paste-ready fixes*
· evidence: `seal/ledger/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token.md`: R1–R3, T1, T2, `Corrected · D4`, `Corrected · K7`, and six `Re-read ·` rows (W8, M2, K6, Corrected G17, Corrected G1, D1)
· verified: executed — M1/M2 in a scratch repository, M3 over the recorded runs, every new case red at `a3aa139a` and green after, every new unit broken once through `bin/mutation-check`, the touched modules, `bin/evidence-check --strict .`; read — the policy and README sentences against the code clause by clause

## Why this work exists

The worktree guard read a `checkout`'s name and a consent token differently
from the programs that run the command, and both differences were silent: a
message search, a merge-base shorthand and a guess from a remote other than
`origin` moved the tree unasked (#790), and a token that a here-document body
only carried was read as typed consent (#780). Both now move only towards a
question. Round 1 of review found three places where that was not yet true
(a message search holding `..`, a guess through a fetch refspec, and a newly
read `checkout` taking a switch or candidate C's question from the base), and
its fix pass closed each in code.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The guess's reach | `spec.md` §*Scope* In 2: "a remote-tracking branch `refs/remotes/<remote>/<name>` in any remote counts". The build counts any ref under `refs/remotes/` that ends in `/<name>`, and since round 1's fix pass also every ref a remote's fetch refspec maps `refs/heads/<name>` to | the code | **Corrected 2026-10-05 by round 1's fix pass.** This row first argued that naming the remotes exactly would cost a second call and a read of git config, which the guard did not do, and called the name match a superset of git's guess. That ground was false: git's guess is itself a read of git config, each remote's `remote.<remote>.fetch` refspec, and a remote whose refspec puts its branches outside `refs/remotes/` or renames them with a partial glob was guessed from by git and read as no branch here (round 1, 🟡 2, executed). The fix reads those refspecs with one `git config` call, OR-ed after the name match, so the match still answers first and the guess now covers every refspec git maps through. What stays wider than git is the louder direction: a name ending a longer remote branch's name, a guessed name under `--detach`, and one two remotes hold, each a command git refuses. §*Known limits* names them |
| A2's second clause for the guess | A2: "each form git refused keeps the base's verdict". Under `checkout --detach <name>` git takes no guess and refuses, and the build reads a switch for a name only `upstream` holds | the code | `spec.md` §*Out*, "A name git refuses but the guard resolves", and In 2 ("the guard asks anyway — a refused command asked about costs one prompt, the louder direction") accept it; the base already did this for `origin`. The A2 case holds the clause for every C1 and C2 form, and §*Known limits* names the guess's refused shapes |
| How A8 breaks the wider reader, and when `has_token` falls back | A8: "Given `wide` unloadable (the way `test_a_broken_wider_reader_costs_only_the_question` makes it)". In 5: fall back "where `tokens.without_bodies` cannot load or raises" | the code falls back on any exception from `tokens.without_bodies`; the A8 case loads the guard from a copy of `hooks/` whose `cmdline.py` exits at load, and a second variant makes `without_bodies` raise | `tokens.without_bodies` imports `hooks/cmdline.py` when it runs, so a module that cannot load raises there. A separate `wide is None` condition read the same failure twice, and breaking it survived. Setting `wide` to None leaves `hooks/cmdline.py` loadable and would exercise nothing once the condition is gone (`phases/phase-3.md`) |
| The milestone in the policy sentence | `spec.md` §*The frozen reading*: the owner placed #790 in milestone `release: 0.18.3`. The policy sentence first named that milestone | "the milestone of the release that ships it" | `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` refuses a loaded file naming an unreleased version, because the line goes red on the release's own preparation commit |
| How `main` places a newly read switch | `spec.md` A4 checks `classify` alone ("every shape the base read as a switch the build reads as one"); the failure direction says #790 "ORs a lookup onto the base's, so a 'switch' never becomes 'no switch'" | `main` reads each segment with `classify(..., base_only=True)` first and takes a switch only #790's lookups read only where the base read none in the command, and does not hand it to candidate C as judged | `classify` is monotone, but `main` judges the first switch and C subtracts the kinds `main` judged, so a newly read `checkout` in front moved the verdict to a clean tree and took C's question away: base `ask`, build silent (round 1, 🟡 3, executed). The changelog's promise is about the guard, so the fix is in `main`, not in a limit |
| One more policy sentence than In 5 lists | In 5 lists the docstrings, §*Choice sites* and the READMEs. §*Which tree* also said the guard asks `hooks/cmdline.py` "one question", which the consent read's body question made untrue | §*Which tree* says one question about a command's kinds, and the consent read's body question beside it | Found by `bin/evidence-check --strict .`, which drifted released row K7 on that paragraph; a released claim that no longer holds is corrected, so `Corrected · K7` carries it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's head | the sealer, spawned by the orchestrator after the review rounds (contract §2) |
| The real-git cases (`a_history`, the message search through `main()`) on Windows, which no machine here runs | CI's Windows job on the pull request |
| `questions.md` P1, whether the owner's placement of #790 covers the guess from every remote | the owner, at the pull request; the build took default (a) on the orchestrator's relay |

## Not done

Nothing the plan asked for was left. The `tokens is None` branch of
`_without_bodies` has no case of its own: `hooks/tokens.py` loads in every run,
and breaking it would take a second copied `hooks/` beside the one A8 already
builds; `phases/phase-3.md` names it.

## Fed back into the spec

Inferred during implementation, and a planner may overturn them:

- `docs/worktree-guard-spec.md` §*Known limits*, the bullet naming the names
  git refuses that the guard still reads as a branch (`^<rev>`, a guessed name
  under `--detach`, held by two remotes, or ending a longer remote branch's
  name), the git config it does not read, and a later syntax `rev-parse
  --verify` cannot read.
- §*Which tree*: the guard asks `hooks/cmdline.py` one question about a
  command's kinds, and its consent read has it take here-document bodies out.
- §*Which tree*, from round 1's fix pass: a `checkout` only #790's lookups
  read as a switch takes the place of no switch the base read and no question
  from candidate C; and the guess reads each remote's fetch refspec.
