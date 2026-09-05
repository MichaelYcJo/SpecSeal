- **`bin/test` runs this repository's suite from an environment it builds
  once.** The command `CONTRIBUTING.md` named resolved and installed its
  dependency on every call — 55–58 seconds each, paid on all seventeen test
  calls of one measured segment (#133) — so the gap was never a missing
  command, it was a command that is cheap only the first time you forgive it.
  `bin/test` and `bin/test.cmd` join the five `bin/` pairs already there over
  `.github/scripts/run_tests.py`: a virtualenv at `.venv` built on the first
  call and reused after, arguments passed straight through, the repository root
  resolved from the script's own path so it works from any directory or
  worktree, and the interpreter it used printed every time. Measured on one
  machine: **5.24 s cold, then 0.60 s** — and the claim is not that the first
  call is cheap but that it is the only one. **Every failure is a sentence
  rather than a traceback**, which is what a command that writes to the working
  tree owes: no `uv` and no 3.12-or-newer interpreter names both and says which
  to install, a build step that exits non-zero names the directory to remove, a
  build that leaves no pytest behind stops instead of rebuilding forever, and a
  copy of `bin/` with no runner beside it says so — on both platforms, in the
  same words. The file has to parse and run under Python 3.9 to print the first
  of those, so nothing in it is newer than the floor it refuses. **The
  virtualenv is invisible to git on every path that can produce one**, and that
  is a guarantee about exits rather than a list of paths: `uv venv` writes
  `.venv/.gitignore` and `python -m venv` writes none, so the runner writes it
  itself, from the one function that reaches a virtualenv at all, on every way
  out of it. A list was tried first and went short twice — it named a build
  that succeeded, then a build that failed partway and a `.venv` merely
  adopted, and review still found two more: the one adopted `.venv` the floor
  **refuses**, which is also the one least likely to carry an ignore of its own
  because every version that refusal rejects predates the 3.13 where `python -m
  venv` began writing one, and a directory an earlier run left on a machine
  where neither builder can now finish. **The floor is asked of an adopted
  environment too**:
  the version both builders record in `pyvenv.cfg` is read rather than run, and
  a `.venv` below the floor is refused with a sentence naming what to remove. A
  directory that says nothing about its version is kept — refusing on silence
  turns one unknown into a suite nobody can run. No `-n auto`, because
  `pytest-xdist` is CI's install and a freshly built environment has pytest and
  nothing else. (#156)
- **A session finds the runner instead of being handed it, or guessing.**
  `CONTRIBUTING.md` §*Running the checks* names `bin/test` first and shows the
  narrow `bin/test tests/<file> -q` a segment types, with the sentence saying
  the full five-minute run is the orchestrator's, once, after the review rounds
  settle. The `uvx` form stays as a labelled **no-write** fallback — for a
  reader who does not want a `.venv` in their tree — carrying the 55–58 seconds
  that demoted it, because a fallback named without its cost gets promoted back
  by the next reader. The floor sentence now names `FLOOR` in the runner, so
  the document's 3.12 and the code's are traceable to each other rather than
  two numbers that happen to agree today. `docs/review-handoff-protocol.md`
  §*The handoff before round 1* takes a fifth requirement: **a runner the
  repository ships is found, not typed into every prompt**, with the old
  requirement kept intact for a repository that ships none. What bought it:
  four build segments of one work item read repeats of **17 s, 2 s, 0 s and
  0 s**, and the only difference between them was whether the orchestrator had
  remembered to type the runner into the spawn prompt — a requirement met by
  hand, once per prompt, is met until somebody forgets. `agents/smith.md` is
  the carrier that closes that, because it reaches a segment at startup with
  nobody typing anything, and it names the protocol's section rather than
  restating the rule. (#156)
- **A round record's `Contract changes` row now has its vocabulary written
  down.** `docs/review-chain-spec.md` §*The fix surface* defined the reach half
  as the call sites of a changed unit and named none of the five values the
  generator actually writes there — the enclosing unit, the file's basename,
  and the three words `round_record.py` substitutes: `pytest` when any caller
  sits under `tests/`, `pytest only` when those are the whole reach, and `no
  call site found` when there is none. Reading a correct cell as a mistake cost
  a review round of this very work item. The three words are read out of the
  generator's own constants by the case that pins them, so the document cannot
  drift from the code. (#156)
