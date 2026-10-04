# a here-document body is data to the commit gate (#739) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the ticket left open that the tree answered

These are settled from the tree. Each lists its grounds so nobody has to reopen it.

- **Where the policy text goes.** #739 says `docs/commit-review-gate-spec.md` is "frozen until #727, so the note goes in the split's file". That no longer holds. `aadf2efb` (#744) cut the policy into three files and lifted the ceiling freeze. `seal/config.md` reads `Over the ceiling | none`, and the file is 586 lines against a ceiling of 1000. The paragraphs that state the old rule are in that file, so they are edited where they stand.
- **The worktree guard does not change.** `hooks/worktree-guard.py#_judgment_text` and its `wide` reading only drop bodies and never read them back. Its switch and creation arms read through the frozen `hooks/cmdline_base.py`, which no work item may edit.
- **`is_plain` does not change.** It is the owner's P7 rule for where the reading stands aside. This work reuses its sets and does not touch its verdict.
- **Unquoted delimiters keep today's reading.** #739's own checkbox conditions data on the quoted delimiter. The reverse direction would need a scanner that fails open if it reuses `substitution_bodies`.
- **Nested bodies keep today's reading.** A substitution's value goes wherever the enclosing command sends it, and the inner reading cannot see where (`plan.md` alternative E).
- **This is not the interpreter enumeration legacy #75 rejected.** That list named the runners. This one names the data consumers, and anything unlisted is read as today.
- **The ladder rung.** It alters a gate's verdict, so a `spec.md` is required (`skills/implement/SKILL.md` §3).

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May `tests/test_no_shape_the_base_stops_reads_silent.py`'s row "measured: a patch whose body loops over a commit string" leave the must-stop corpus? The row is `cd <w> && python3 - <<'EOF'` with a quoted delimiter and Python text only. The tree cannot settle it: two statements by the owner disagree. That module's docstring records the owner's constraint for work item `1790644505`, that no shape `release/v0.16.0` stops may read silent. #739, filed later by the owner, asks for exactly this shape to be pinned silent. | a person — the repository owner | **Move it** (default): #739's rows 1 and 3 stop being refused, and the module docstring names #739 as the later and narrower decision. **Keep it**: Python leaves the scope (Q2's other option), and rows 1 and 3 stay refused and go into the known limits. | Decided by the framer: move it. The grounds are that #739 is the owner's request for this shape, and that the constraint's own docstring scopes it "for the work" of `1790644505`, whose subject was who a stop goes to, not the reading. | ⬜ decided-by-framer, open to the owner at approval |
| Q2 | Is a Python program read from stdin (`python3 -`, `python3`, `python -`) data, in the strict form R2e gives? | a person — the repository owner | **Yes** (default): it is the same class as `python3 script.py`, which `docs/commit-review-gate-spec.md` already lists as unread. Shell-reading a Python body finds only shell-shaped text, never `subprocess.run([...])`. **No**: plan alternative F, under which only #739's row 2 is fixed. | Decided by the framer: yes, in the strict form only. Any flag, script, `$X` or `-c` in the first position keeps today's reading, and so does every row of #665's rounds 2 and 3. | ⬜ decided-by-framer, open to the owner at approval |
| Q3 | A sink writing a file on a line that also runs `git commit` keeps today's reading (R2f). So `cat > f <<'EOF' … EOF && git add f && git commit -m x` still stops when the body mentions a commit. Is that cost accepted? | a person — the repository owner | **Accept** (default): a commit runs hooks. In a clone whose hooks slot is foreign, the written file can be one, and the reader cannot know where that slot points. Naming hook paths instead is a list that rots. **Narrow it**: let that body be data unless its target names a hooks location. That is a name list, and the first reviewer to try `.husky/` or `.pre-commit-config.yaml` breaks it. | Decided by the framer: accept. The Write tool remains the way around it, as it was before. | ⬜ decided-by-framer, open to the owner at approval |
| Q4 | Does every `gh` subcommand under `pr`, `issue`, `release` and `api` leave a file it is handed unexecuted? | a measurement — read `gh help` for the four groups at the installed version | If one runs a file or its stdin, drop it from R2c's `gh` set. | The four groups as R2c lists them | ⬜ |
| Q5 | Do the shlex lexer `is_plain` uses and `_heredoc_split` count heredoc openers the same way for every line R2c admits? R2d's count check is the guard, and the work confirms it is the right one. | the work — phase 2 | If a shape inside (c) splits differently, add that construct to (c)'s exclusions. Do not add special handling. | The count check | ⬜ |

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
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
