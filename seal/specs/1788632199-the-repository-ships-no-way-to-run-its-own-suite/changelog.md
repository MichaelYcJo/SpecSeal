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
  virtualenv is invisible to git on every path that can produce one**, which is
  three rather than one: `uv venv` writes `.venv/.gitignore` and `python -m
  venv` writes none, so the runner writes it after a build that succeeded,
  after one that failed partway — `uv venv` has made the directory by the time
  the install step finds no network — and over a `.venv` it merely adopts,
  which is the one somebody else made and the one call in its life that could
  write an ignore at all. **The floor is asked of an adopted environment too**:
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
