# the worktree guard judges a switch written after a creation (#620, #624, #243) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Answered from the tree, not open

The tickets left these open. The tree settled each one, and `spec.md`
§*Decisions the tickets left open* holds the grounds. They are listed here so
that nobody reopens them as questions:

- What "stricter" means across `deny` / `ask` / `silent` / `allow` (decision 1).
- How the stricter answer is produced: the existing switch ladder for any
  command carrying both a switch and a creation, whichever is written first
  (decision 2).
- Whose reason text reaches the person when both directions fire at the same
  level (decision 3).
- How a `cd` into the worktree the same command creates is judged
  (decision 5).
- Row 3's wording under `[shared-tree-ok]`, and the `[worktree-ok]` wording
  (decisions 6 and 7).
- `isSidechain` must be literally `false` (decision 8).
- #243's counts are replaced by classes and committed cases, not by new
  figures (decision 9).
- Round 2's report of work item 1790381327 still exists in the tree
  (`rounds/round-2-report.md`), so its paste-ready code is read there, not
  through history.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The walk defect has two more instances that this work does not close. (a) A switch after a switch in a **different tree** (`git switch a && git -C ../other switch b`): only the first tree is judged, so an ACTIVE `../other` goes unguarded when the first tree is clean. (b) A second creation in a **different clone**: it runs with no question, and the writer records only the first clone, so no consent is minted for it. Both come from #620's cause. Does this patch absorb them? | a person. The tree cannot settle it: closing both needs the ladder judged once per tree, which restructures `main`, and the owner's milestone says *fixes to instruments, no new gate*. Whether a restructure counts as "new mechanism" is the owner's reading of their own sentence | **Absorb:** refactor the switch ladder into a per-tree function, judge every classified segment, and take the strictest. This closes the class and moves every line every `main` ledger row anchors on, roughly doubling phase 1. **Defer:** the orchestrator files one issue naming both instances before the pull request, and the PR body names it | **Defer**, applied. The owner pressed `automation`, so the run does not wait. The orchestrator files the issue, and the PR body carries its number | ⬜ |
| Q2 | Which verdict each command-word spelling gets with a consent record present: which spellings reach `allow`, which reach `ask`, and which leave the guard silent. This includes whether `nice git` and `xargs git` are silent, as round 3 of 1788817291 reported | a measurement: one `test_tmp_*` probe over round 3's 55 shapes (its report lists them) with `decide`, in phase 3. #243 and round 3 are both claims until it is run | The probe's table decides which members the committed S10 case pins, and the wording of the rewritten paragraph | Round 3's grouping (17 allow, 20 ask, 18 silent), used only as the probe's expected result | ✅ measured 2026-09-28 in phase 3. The report lists only 39 of its 55 shapes, so the probe built 58 by construction. With a record: **20 allow** (every quoting spelling of the word `git`) and **38 silent** (every path, expansion, case, trailing slash, wrapper and leading assignment, `nice git` and `xargs git` included). **No shape asks**: the `ask` group round 3 measured predates #257, which made a consented compound silent, so the question's three groups are two. Without a record, the shapes `cmdline.parse_git` reads as git deny and the rest are silent. `phases/phase-3.md` holds the table, and `test_the_command_word_class_is_what_the_allow_covers` pins members of the four groups |
| Q3 | Is `docs/worktree-guard-spec.md` §*Known limits*'s first line (*A heredoc line that IS exactly a git command still matches*) still true? `_judgment_text`'s docstring says `cmdline.drop_heredoc_bodies` closed it | a measurement: `decide` on a command whose heredoc body holds a line `git switch feature/x`, in an ACTIVE tree, in the phase-3 probe | Silent means the limit is gone and the line is deleted. `deny` means the line stays | The line stays until the probe runs | ✅ measured 2026-09-28 in phase 3: **silent**, for a body line `git switch feature/x` and one `git worktree add ../wt f`, under a quoted and an unquoted delimiter, in an ACTIVE tree where a plain `git switch feature/x` denies. The line is deleted, and `test_a_git_command_inside_a_heredoc_body_is_not_judged` holds it |
| Q4 | How often do sessions write a creation followed by a switch in one command? This is the prompt-budget number the PR body owes (`CONTRIBUTING.md` §*What a change to a gate must carry*) | a measurement: count, over local transcripts, the Bash commands in which `git worktree add` is followed in the same command by `git switch` or a branch-form `git checkout`. Report aggregates only. No command text, path or session id leaves the probe (`tests/test_no_real_identifiers.py`) | Zero or near zero means the new stops are theoretical. A real count is stated as it is | The PR body says *not measured* until the count exists | ✅ measured 2026-09-28 in phase 4, over this machine's transcripts only (`~/.claude/projects/**/*.jsonl`, 728 files, subagent transcripts included, each `tool_use` counted once by id): 49,370 Bash commands, 44 of them carrying a `git worktree add`, and **0** of those 44 followed in the same command by a `git switch` or a `git checkout` of any form. 0 had one before the creation either. Segments were read with `hooks/cmdline.py`, the guard's own reader, checked on four synthetic commands first. So the new stops are theoretical on the one history measured; another person's history is not measured |
| Q5 | Does S2 hold byte for byte on the reason, or only on the decision and the reason's opening? `fmt_snippet` and `fmt_sessions` read inputs the order cannot change, but the builder has not run it | the work: phase 1 meets it when the case first runs | Byte-identical reasons are asserted as such. If a part differs for a reason unrelated to order, the case compares the decision and the first line, and `phases/phase-1.md` names what differed and why | Byte-identical | ✅ answered by the work 2026-09-28 in phase 1: **byte-identical**. S2 compares the whole reason in every tree state, consent state and attempt, and it passed on its first run after the walk change |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked.

Q1 is the only person row, and its default is already applied, so it does not
block the build. The owner may overturn it after reading the pull request.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
