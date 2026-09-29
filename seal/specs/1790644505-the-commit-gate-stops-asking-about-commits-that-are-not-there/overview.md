# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

An `automation` run was promised that nothing stops to ask, and the commit gate
put four prompts to the person in one; under that press every stop is now a
refusal the model handles, and what the gate stops has not moved.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S3's loop shape | `spec.md` S3: "a commit inside a `for` loop over a variable". Written on one line, `for d in a b; do git -C $d commit -m x; done` reads NO commit at `release/v0.16.0`, so the base is silent there and there is nothing to refuse | The measured loop's own shape, `for w in …; do IFS=: read d n <<< "$w"; git -C $d commit -m x; done`, whose `git` follows a `;` | Executed: `commit_invocations` returns no invocation for `do git commit`, `then git commit` or `while …; do git commit` written on one line, and one for the multi-line form. The reading is out of this work item's scope (`spec.md` §*Scope*, Out), so the case uses the shape the frame measured. The base hole itself is under *Not done* **Corrected 2026-09-29 by phase 4:** the hole became #669 and was fixed on this branch, so the reading is no longer out of scope in that one, stricter direction; the loop case keeps the measured shape, and the one-line shapes are `tests/test_a_commit_behind_a_reserved_word_is_judged.py`'s |
| `hooks/cmdline.py` byte-identical | `spec.md` property 1 and S7 (a): `hooks/cmdline.py` untouched, `git diff release/v0.16.0 -- hooks/cmdline.py` empty | Phase 4 changes it: `command_word` added, `parse_git` and `walk_directories` call it (#669) | The owner's standing rule that a defect the branch finds is fixed where it arises, and the orchestrator's phase 4 in `plan.md`. The frame's reason for the file being untouched was that narrowing reads real commits silent; this change only widens, since every segment it reaches is one where the base found no command (`phases/phase-4.md`). `spec.md`'s three sentences carry dated corrections **Corrected 2026-09-29 by phase 5 (#670):** phase 5 changes it again, and `commit_invocations` and `_hides_a_commit` in the gate with it, for wrappers, shell strings and substitutions; the same grounds and the same direction (`phases/phase-5.md`) |
| The guard's pinned command-word groups | `tests/test_the_guard_asks_once_per_session.py` pinned `nice git` as a word the guard does not read as git, and `docs/worktree-guard-spec.md` named `nice` as a wrapper not read past | `nice git` moved to the group the guard judges, `uv run git` took its place as the example not read, and the spec sentence says so | `parse_git` is the reading both gates share, and #670 made `nice` one of the enumerated runners, so the guard now judges `nice git worktree add` too, which is the stricter direction for it as well. The one existing case edited in phases 4 and 5 besides the contract's registry |
| The two READMEs | `plan.md` names no README | Both gate rows gain one sentence saying an `automation` run meets no prompt | `README.md`'s row said "after that it is the plain confirmation", which is false under the press, and `CONTRIBUTING.md` moves the two editions together. `tests/test_one_word_one_meaning.py`'s grain phrases are kept |
| How the reader is imported | `questions.md` Q3: import in place | Imported in place, inside a `try`, so a reader that fails to load reads as no press | Spec silent on the import's failure. An ImportError at module load leaves the gate with no verdict, which `hooks/dispatch.py` turns into silence; no press is the base's answer (contract §13) |
| The marker under the press | Spec silent | Not written: under the press `already_asked` is not consulted | The press decides the answer before the budget matters, and a marker nobody reads would only change what a later, unpressed read of the same session sees first |

## Not verified

| Item | Who must answer |
|---|---|
| The cases on Windows | CI's `windows-latest` leg, at the pull request |
| Whether a refused model re-issues the same command (`questions.md` Q2) | The orchestrator of the next `automation` run, from its own transcript |
| The whole suite, the repository-wide lint and the typecheck | The sealer, once, after the review rounds settle |

## Not done

- **Done since, in phase 4 (#669):** a commit after a reserved word on the
  same line — `for d in a; do git commit -m x; done`, `while true; do git
  commit -m x; break; done`, `if true; then git commit -m x; fi` — returned no
  invocation at `release/v0.16.0`. Phase 1 left it as a reading change out of
  scope; the orchestrator filed it as #669 and put it on this branch as phase
  4, which reads past the word. This bullet stays so the phase 1 record's
  pointer here still lands.
- **Done since, in phase 5 (#670):** `exec git commit`, `timeout 5 git
  commit`, `nice git commit`, `xargs git commit` and a commit inside `$( … )`
  or backticks returned no invocation at phase 4's reader. The orchestrator
  filed them as #670 and put them on this branch as phase 5, which enumerates
  the programs that run their operands and reads shell strings and
  substitutions. This bullet stays so the phase 4 record's pointer still
  lands.
- **A program whose operands are a script or a remote command is not read.**
  `bash run.sh`, `source f`, `make`, `uv run git commit`, `npx`, `pnpm exec`,
  `ssh host git commit` and `docker exec c git commit` each stay silent, as at
  the base. The first three run a file this reader would have to open, the
  task runners are an ecosystem list with no closed form, and the last two
  commit in a repository on another machine or in a container, which the
  gate has no way to see. Executed at phase 5's reader: each of the eight
  returns no invocation, and `uv run git` is pinned as unread in the guard's
  case. The orchestrator decides whether any becomes an issue.
- **Two other hooks keep their own copy of the five wrappers.**
  `hooks/evidence-advisor.py` and `hooks/review-history-guard.py` each hold a
  `WRAPPERS` of their own and a loop that stops at the first word it does not
  know. Neither decides whether a commit is judged, so #670's class does not
  reach a silent commit through them; they read less than the gates now do.
  Read, not executed.
- **The worktree guard does not read inside a substitution or a shell
  string.** `parse_git` is shared, so it reads the enumerated wrappers, but a
  `git switch` inside `$( … )` or `sh -c` is still invisible to it. The
  commit gate's readers for those live in the gate. Read, not executed.
- **A subprocess run of the gate can glob the real projects root.** The
  suite's autouse fixture points the reader at an empty directory for
  in-process cases only. A `run_hook` case that stops a commit now looks for
  `~/.claude/projects/*/<session>.jsonl`; it reads a file only where one of
  that name exists, and the guard's subprocess cases already had this. Left as
  it is, because closing it is a change to `tests/conftest.py`'s environment
  that this work item does not need.

## Fed back into the spec

none
