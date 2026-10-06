# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — questions for the planner

<!-- seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, so nobody reopens them.** #825 fixed the direction
and left the mechanism's shape and two issues' fate open. The tree, and
pytest's own source in the built environment, answered each (`spec.md`
§*Read by this frame*, `plan.md` Alternatives):

- **How the recorder is loaded**: `-p specseal_pytest_record` appended to
  `PYTEST_ADDOPTS`, the module reached through a `PYTHONPATH` entry that
  exposes nothing else (R1, R2; Alternatives A, B).
- **Which process records**: the first pytest session in a process that
  finds `SPECSEAL_RECORD_KEY` claims it and takes it out of its
  environment; a child pytest and an xdist worker inherit no key and
  record nothing, and the controller's record covers a `-n auto` run
  (R3, R5; Alternatives C, D, E).
- **The unit of the word stays the file**, identified by the realpath of
  the test's absolute path made relative to the run's worktree, spelled
  posix (Alternatives F, G).
- **A file in no base session** reads `new` where the base run exited 0
  and `new?` otherwise (Alternative H; Q1 below is about the noise, not
  the rule).
- **Where `HEAD` left no record**, the `FAILED` lines name the files, each
  reads `new?`, and the base is not run (Alternatives J, K).
- **#813 and #818 disappear with the regexes** on the measured path; the
  fallback's `FAILED_RE` is widened so a spaced path is named (Alternative
  L). Both are closed by this work item's pull request.
- **No `docs/` clause and no edit** to `agents/sealer.md`, `agents/smith.md`
  or either README: each still says what is true (`spec.md` Scope 10).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | A file the base run never collected reads `new` only where that run exited 0. On a base that is already red for an unrelated reason, a file the branch added therefore reads `new?` (`NOT_REACHED`, naming the exit) rather than `new`, and a person opens `suite-at-base.txt` to see that the file is simply new. Is that noise acceptable? The tree answers the direction (every failure of the mechanism is strict, `CONTRIBUTING.md` §*What a change to a gate must carry*) and not the trade: the alternative is to read `new` whenever every recorded session wrote its `end` line, which misses a later runner the shell never started because a part before it failed, and so can call `new` a file the base would have failed. Nothing in the records says which happens more often in practice | a person — the repository owner | (a) strict as built: `new?` with the exit named, a person checks a red base by hand · (b) `new` where every recorded session ended, accepting the missed-runner case as a named limit in rule 3 · (c) (a) now, and a measurement over the next release's gate runs of how often the row fires, before deciding | (a) — this frame builds it; the answer does not block the build | ⬜ |
| Q2 | A row that REPLACES `PYTHONPATH` (`PYTHONPATH=src pytest`) keeps the gate's `-p specseal_pytest_record` in `PYTEST_ADDOPTS`, and pytest then cannot import the recorder and exits 1 before any test runs (measured in phase 2 on pytest 9.1, `phases/phase-2.md`). `spec.md` and `plan.md` Alternative A read such a row as one that only loses the recorder (`new?`); it loses its whole suite at the gate instead, though every test passes. Rule 3 names it and tells the author to add to the variable. Is that the trade the owner wants? | a person — the repository owner | (a) as built: the row fails at the gate with pytest's import error in `suite.txt`, rule 3 says to write `PYTHONPATH=src:$PYTHONPATH`, and `test_a_row_that_replaces_pythonpath_cannot_load_the_recorder` holds it · (b) the gate notices the import error in `suite.txt` and runs the row again without the recorder — a text inference of the kind #825 removed, and one more run · (c) a loading route that survives a replaced `PYTHONPATH`, which nothing read so far offers (`PYTEST_PLUGINS` needs the same import) — a frame question | (a) — built; the answer does not block phases 3–4 | ⬜ |
| Q-M1 | Does a `-p specseal_pytest_record` carried in `PYTEST_ADDOPTS` load the module on pytest 7.4, 8.0 and 8.1 as it does on 9.1.1 (R1), and do `config.rootpath`, `config.invocation_params.dir`, `report.location` and `report.fspath` exist on each? One probe per version through `uvx --with pytest==<v>`, the way the 0.18.3 frame ran M12 | a measurement — phase 1 | yes on all four: the recorder's floor is pytest 6.1 by reading, and the comment over it says which builds were measured · no on some: the recorder reads the names it has (`getattr` with the older spelling) and the floor sentence names the oldest it loaded on | yes, by reading pytest's source at 9.1.1 and the names' known ages | ✅ yes on all four, measured in phase 1 (`phases/phase-1.md`) |
| Q-M2 | Under `-n 2`, does the controller's `pytest_collectreport` receive a worker's failed collection (R5 reads that it forwards test reports; the collect path is read in `xdist`'s `DSession.worker_collectreport` but not confirmed here), and does `report.location[0]` on a forwarded report stay relative to the controller's `rootpath`? | a measurement — phase 1, S4 | yes: one record file covers the run · no: the collect line is written from the worker's `collectreport` on the controller side by another hook, or the recorder records on workers for collect lines only, and `plan.md` Alternative E is reopened for that line alone | yes, by reading `xdist/remote.py` and `dsession.py` names | ✅ yes, measured in phase 1: one controller record, paths relative to the controller's rootpath; a failed collection arrives once per worker (`phases/phase-1.md`) |
| Q-W1 | Which of the roughly sixty end-to-end cases over `compare_at_base` keep their word, which move to a measured word, and which move to `NO_RECORD` or `NOT_REACHED` — and for each case that asserts a kept file (`suite-at-base-<k>[-<n>].txt`, `.xml`, `collected-at-base-<n>.txt`), what it asserts now | the work — phase 2, `phases/phase-2.md` lists each with before and after, and the row of the table that gave the new word | — | — | ✅ answered in phase 2: `phases/phase-2.md` §*What this phase found* lists every case with its word at a9d7b0e5 and now, and the row that gave it |
| Q-W2 | Whether `tests/test_release_hygiene.py` checks that every entry of `VERSIONS_OF_ANOTHER_PRODUCT` still names a token in its file, which decides whether the `9.1.1` and `3.8.0` entries for `broad_gate.py` are moved to the recorder's path (where its comment names the builds it was measured on) or deleted | the work — phase 2, read in that module before the exemptions move | — | moved, keyed on the recorder's path | ✅ deleted, phase 2: the module checks no entry for liveness (`timers_in` only skips a listed `(file, token)`), the recorder carries no three-part token to move them to, and a dead row would let either number back into `broad_gate.py` unexamined; a comment in the table says where they went (`overview.md`'s divergence row) |
| Q-W3 | Whether any case outside `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` reads a retired name (`row_prefixes`, `report_counts`, `proof_refused`, `MULTI_RUNNER`, `COMPANY`, `COLLECTED_BEYOND`, `NO_RUNNER`, `NOT_ENDED`, `collected-at-base`), beyond `tests/test_release_hygiene.py`'s three exemption rows this frame found by grep | the work — phase 2, one `grep -rn` over `tests/` and `docs/` before the retirement commit | — | none beyond the three | ✅ none, phase 2: outside the two named modules the grep over `tests/`, `docs/`, `agents/`, `skills/`, `templates/` and the READMEs found the two `broad_gate.py` exemption rows of `tests/test_release_hygiene.py` (four lines), the **New?** bullet's kept-file names in `skills/verify/SKILL.md`, and released records under `seal/` and `changelog/`, which are not edited. `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` pins rule 3's title and reason, which moved with it |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build, and Q1 does
  not: its default is built.
- **a measurement** — a probe, a command or a count settles it. Q-M1 and
  Q-M2 are phase 1's first act, before the recorder is written against an
  assumption.
- **the work** — unknowable at framing time; the phase that meets it decides
  it there and records it in its phase record.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked. Answered rows
feed back into docs/ (policy clause or open-questions section) before this
directory's work merges.
