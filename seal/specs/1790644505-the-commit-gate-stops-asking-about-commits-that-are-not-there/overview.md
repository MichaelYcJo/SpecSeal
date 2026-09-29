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
| S3's loop shape | `spec.md` S3: "a commit inside a `for` loop over a variable". Written on one line, `for d in a b; do git -C $d commit -m x; done` reads NO commit at `release/v0.16.0`, so the base is silent there and there is nothing to refuse | The measured loop's own shape, `for w in …; do IFS=: read d n <<< "$w"; git -C $d commit -m x; done`, whose `git` follows a `;` | Executed: `commit_invocations` returns no invocation for `do git commit`, `then git commit` or `while …; do git commit` written on one line, and one for the multi-line form. The reading is out of this work item's scope (`spec.md` §*Scope*, Out), so the case uses the shape the frame measured. The base hole itself is under *Not done* |
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

- **A commit after a reserved word on the same line is read as no commit at
  all, on the base as on this branch.** `for d in a; do git commit -m x; done`,
  `while true; do git commit -m x; break; done` and `if true; then git commit
  -m x; fi` each return no invocation from `commit_invocations` at
  `release/v0.16.0` (executed). A shell runs each commit, so this is a silent
  the base already has. It is a reading change, which this work item's owner
  constraint and `spec.md` §*Scope* put out of scope, and no open issue owns
  it. The orchestrator files it; the answerer is the repository owner.
- **A subprocess run of the gate can glob the real projects root.** The
  suite's autouse fixture points the reader at an empty directory for
  in-process cases only. A `run_hook` case that stops a commit now looks for
  `~/.claude/projects/*/<session>.jsonl`; it reads a file only where one of
  that name exists, and the guard's subprocess cases already had this. Left as
  it is, because closing it is a change to `tests/conftest.py`'s environment
  that this work item does not need.

## Fed back into the spec

none
