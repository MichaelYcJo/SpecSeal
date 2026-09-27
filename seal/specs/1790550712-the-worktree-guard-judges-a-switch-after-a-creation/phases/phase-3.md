# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 31fb7a3 |
| Ran by | unknown — the spawn prompt named no agent or model for this record; the orchestrator may fill this row |

## What this phase was asked

#243. A `test_tmp_*` probe that re-derives, by running, the verdict of each
command-word shape (at least round 3's 55) and the heredoc known limit (Q2,
Q3), then is deleted. A committed case pinning one or more members of each
verdict group (S10), shown red by moving one shape to the wrong group.
Paragraphs 15–16 of `plan.md` §*Enumerated copies* rewritten as classes citing
their cases (S11), rows 17–18 corrected in place, and docstring 19's *two*
made *one*. Decision 9: no count survives unless a committed case reproduces
it.

## What this phase found

**The frame does not hold on one point: there is no `ask` group.** Q2 and S10
both assume three verdicts for a command word with a record present — `allow`,
`ask` and silent. Measured, there are two. Round 3 of work item 1788817291 took
its 20 `ask` cells at `3287c78`, before #257 made a consented compound silent;
since then everything the allow's bound refuses is silent under consent. The
framer's *read and found true* note on `only_creates_a_worktree`'s docstring
(*falling to `ask` … said of `/usr/bin/git`, a path, which does ask*) is the
same premise, and it is false for the same reason. S10's case was built to the
groups that exist: `allow` and silent with a record, and `deny` and silent
without one, which is the split a reader needs to predict a verdict.

**The probe, executed** (`tests/test_tmp_243_probe.py`, one run, deleted). The
report names only 39 of its 55 shapes, so the probe built 58 by construction,
each as `<word> worktree add ../wt f` on a clean single-stream tree with its
own session id.

| Record | Verdict | Count | Shapes |
|---|---|---|---|
| present | `allow` | 20 | `git` `\git` `'git'` `"git"` `g"i"t` `g'i't` `gi"t"` `"g"it` `\g\i\t` `g\it` `''git` `""git` `git""` `git''` `"gi"t` `g''it` `;git` `'g'"i"t` `\gi\t` `gi\t` |
| present | silent | 38 | `./git` `../git` `bin/git` `/usr/bin/git` `/tmp/evil/git` `.//git` `/git` `~/git` `*/git` `./bin/../git` `/usr/local/bin/git` `gi*` `$GIT` `${GIT}` `` `which git` `` `$(which git)` `GIT` `Git` `git/` `gi?` `g[i]t` `~git` `sudo git` `env git` `command git` `time git` `nice git` `xargs git` `nohup git` `exec git` `VAR=1 git` `PATH=/tmp/evil git` `env VAR=1 git` `sudo -u x git` `command -p git` `builtin git` `stdbuf -o0 git` `timeout 5 git` |
| absent | `deny` | 39 | the 20 above, the 11 paths, `sudo git` `env git` `command git` `time git` `nohup git` `VAR=1 git` `PATH=/tmp/evil git` `env VAR=1 git` |
| absent | silent | 19 | the 11 expansion, case and trailing-slash shapes, `nice git` `xargs git` `exec git` `sudo -u x git` `command -p git` `builtin git` `stdbuf -o0 git` `timeout 5 git` |

The counts are this probe's and live here, not in the policy document.
`docs/worktree-guard-spec.md` states the class and names
`test_the_command_word_class_is_what_the_allow_covers`, which pins members of
all four groups.

**Q3, executed in the same probe.** A heredoc body line `git switch
feature/x`, and one `git worktree add ../wt f`, under a quoted and an unquoted
delimiter, in an ACTIVE tree: silent all four times, while a plain `git switch
feature/x` in the same tree denied. The known limit is closed, the line is
deleted, and a new case, `test_a_git_command_inside_a_heredoc_body_is_not_judged`,
holds it (the plan asked only for the deletion; a deleted limit with nothing
behind it is a claim nobody can re-run).

**The writer-record property does not hold with a record present, and is not
meant to.** The same probe ran four command shapes × four tree states × three
attempts with a record: 26 cells were silent or asked about the switch only.
That is consent working: the record the writer would write already exists,
and a consented compound is silent by design. The old paragraph claimed its
sweep covered *2 record states* with 0 holes, which was true only before #257.
The paragraph now says the property is for a session with no consent, and why.

**Seen red.**

| Case or claim | How it was shown to fail |
|---|---|
| S10, `test_the_command_word_class_is_what_the_allow_covers` | `sudo git` added to the no-record silent group: red, `('none', 'sudo git', 'silent', 'deny')`. Restored from a copy |
| S10 against the code | M12, `only_creates_a_worktree` comparing `os.path.basename(tokens[0])` again: this case and `test_a_path_qualified_git_carries_no_allow` red, nothing else |
| the sweep paragraph's *removing `before_ask` from either choice row turns the sweep red* | M13 (the idle row) and M14 (the detection-unusable row), each: `test_the_guard_is_never_silent_where_the_writer_records` and `test_a_spent_choose_budget_…` red, nothing else |
| the heredoc case | M15, `_judgment_text` keeping heredoc bodies: this case red, nothing else in `tests/test_worktree_guard.py` |

**Copies the enumeration did not list**, found by the sweep for *falls to
`ask`* and *costs … a prompt*:

- `hooks/worktree-guard.py#only_creates_a_worktree`'s docstring (*Falling to
  `ask` there is the trade*), listed by the plan as true.
- `tests/test_the_guard_asks_once_per_session.py#test_a_path_qualified_git_carries_no_allow`'s
  docstring (*costs is a prompt on `/usr/bin/git worktree add …`*). Its body
  already asserted `silent`.
- `docs/worktree-guard-spec.md` §*Creation consent*, *The prompt budget*:
  *Before consent, a creation written as one segment of a compound still costs
  one prompt each time*. Since #257 a consented compound is silent. Now: with
  consent it gets no allow and the guard is silent.
- `seal/releases/0.9.1.md`'s row *The command word must be the WORD `git`* said
  *It costs one prompt*; corrected with the rest of that row.

**One `Enforced by:` per folded statement.** §*Creation consent* is one
statement, so the S10 case and the writer-record sweep were appended to its
single line, and the rewritten paragraphs name their cases in prose.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *exactly five are vouched for* over *32 command-word shapes*, and *falls to `ask`* | the class, in the same paragraph, and `test_the_command_word_class_is_what_the_allow_covers` |
| *1260 combinations*, *230* and *64* | the property stated for a session with no consent, and the two committed cases that walk it |
| §*Known limits*' heredoc line | `test_a_git_command_inside_a_heredoc_body_is_not_judged` |
| the same counts in `seal/releases/0.9.1.md`'s two rows | the corrected rows, with `Corrected 2026-09-28` notes |
