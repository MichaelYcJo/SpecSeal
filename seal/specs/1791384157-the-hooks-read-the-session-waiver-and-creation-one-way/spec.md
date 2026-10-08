# Feature Specification: the hooks read the session, the waiver and a creation one way (#868, #856)

<!-- seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate.
Issues #868 and #856, for release 0.21.0. Coordinates are at 5623d728
(0.20.0 as shipped) unless a commit is named. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two readers that catch the same defect, the one that stops to ask is the more expensive. Every design here is weighed for a run that verifies unattended |
| #834 §*What the table says* (`seal/specs/1791382684-…/spec.md`, read with `git show`) | What converged read an owned format or an observed fact and refused the unknown; what reopened guessed from text it does not control and let the unknown through; one judgment copied into several places disagreed with itself. This work imports a reader where one exists and names what it removes |
| `docs/worktree-guard-spec.md` §*A. Branch switch*, *The stop for an unrecognised shape* | The question §A asks is *is this command known to leave the branch where it is?*, and a shape it does not recognise stops where the tree matters, with its plain spelling. This is the rule that decides #856 (In 5) |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | The guard and the consent writer read every command through `hooks/cmdline_base.py`, frozen; the guard asks `hooks/cmdline.py` only what the frozen reading does not read as git. The brace rule of In 5 reads the frozen words and the judgment text, in the guard, and reopens nothing |
| `docs/worktree-guard-spec.md` §*Known limits*, the hidden-spelling bullet and the fallback bullet | A creation only a hidden spelling holds is an unrecognised shape, silent in a clean single-stream tree, and the writer files nothing for it; a tree the guard cannot place falls back to the session's own, by the owner's rule of 2026-10-03. In 5's creation joins the first; In 1 keeps the second |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | A wrong deny costs one prompt; a wrong allow breaks another session's tree. The direction every reader here fails in |
| `docs/worktree-guard-spec.md` §*Creation consent*, *The record* | The record stands for *this session may split this clone into worktrees*, under the common git directory of the clone the creation acted on. In 1 makes the clone the writer files under the one the guard judged, by one rule |
| `docs/the-commit-gate-inside-git.md` §*A commit with no Claude session behind it is a person's own* | The session is `CLAUDE_CODE_SESSION_ID`, else the lease whose recorded pid is the hook's nearest ancestor named `claude`. The writer of that pid and its reader must find the same process (In 2) |
| `docs/the-commit-gate-inside-git.md` §*The arms, the marks and the declaration*, and §*Known limits*, *The old spelling waives only where the hook can find the call's shell* | The old bare word is read out of the Bash call by `hooks/answer-write.py` through `hooks/tokens.py#given`; the match through `ps` is a named limit and stays (Out) |
| `docs/commit-review-gate-spec.md`, the consent-read paragraph under §*commit-review-gate (PreToolUse, Bash)* (*This is a JUDGMENT read. The scan for a waiver token is a CONSENT read*) | A token counts only where the command as written carries it, so a consent read can refuse a waiver and never grant one. In 3 removes the one read that grants where the command does not split |
| `docs/the-review-and-parity-arms.md` §*Parity arm* | *The change* is every path the commit would carry. A diff git could not take carries no paths and is not a change confined to `docs/` and `seal/`; In 4 makes the arm ask there |
| `skills/agent-contract/SKILL.md` §13 | A defence resting on a platform guarantee is verified with it removed. `CLAUDE_PID` (In 2) is one, so the `ps` walk stays as the route under it |
| `skills/agent-contract/SKILL.md` §15 | Every case In 1–5 adds is seen red at 5623d728 before it is planted |

## Scope

### In

Six items. Four are #868's disagreements, one is #856, and the sixth is the
list of what leaves the tree, which #834's direction asks every 0.21.0 frame
to name.

1. **A creation is placed by one rule, and the rule is the guard's.**
   `hooks/worktree-guard.py#main` places a segment at `wheres[0]` and
   `judgeable` falls back to the session's own directory where that entry is
   `Unresolved` or holds no repository (wg:598-636, 2998). `hooks/worktree_consent.py#creation_directory`
   takes the first entry that is not `Unresolved` (wc:448-451). Executed by
   this frame, through `hooks/cmdline_base.py`'s walk (a deleted probe,
   2026-10-07): the two agree on the three `BASE_TREE_CHAINS` of
   `tests/test_guard_resolves_the_tree_it_judges.py`, and disagree on the
   inventory's shape and on one more:

   | Command, from `S` | `wheres` | guard | writer |
   |---|---|---|---|
   | `eval x ; cd /tmp/a \|\| git worktree add ../wt f` (part 1 row 127) | `(Unresolved(S), /tmp/a)` | `S` | `/tmp/a` |
   | `cd <missing> ; git worktree add ../wt f` | `(<missing>, S)` | `S` | `<missing>`, so no record at all |

   bash runs the `\|\|` segment only where the `cd` failed, in the directory
   the shell was already in, and `/tmp/a` is the branch it skipped; and
   `;` runs its segment in the session's directory when the `cd` fails. The
   guard's answer is where bash runs the command in both, so the writer
   takes it. One function places a segment — `wheres[0]`, the `Unresolved`
   and no-repository fallbacks, the segment's own `-C` composed — and both
   `main` and `creation_directory` call it; the Windows backslash doubling
   the guard's `_tokenize_with_separators` does and the writer does not
   (part 1 row 90) goes through the same one adapter. The function lives in
   `hooks/worktree_consent.py`, which the guard already imports and which
   already reads through `cmdline_base`, so
   `tests/test_the_frozen_reading_never_grows.py#test_only_the_two_fallback_arms_read_it`
   keeps its list of importers. Input class: guess (the frozen walk's
   directories), unknown refused to the session's own directory, as
   §*Known limits* already says of a switch.

2. **The session's process is found by one reader, and it reads an observed
   value first.** `hooks/hooksession.py` owns it:
   - `is_claude(comm)`: `os.path.basename(comm) == "claude"`, the test
     `hooksession.claude_ancestor` (hs:59), `call_args` (hs:95) and the
     guard's `sessions_in_tree` (wg:1228) already use. `hooks/session-lease.py#owner_pid`'s — NAME NOT IN TREE since phase 4 removed it
     `"claude" in comm` at depth 15 (sl:78) goes: the lease it writes is read
     back by `claude_ancestor` at depth 20 with the stricter test, and a pid
     only the looser test finds is a lease no reader matches, which
     `from_lease` answers with no session and the commit is not judged
     (hs:136, 148). Read, not run: no process named that way was built.
   - `claude_pid(environ=None)` (NAME NOT IN TREE, the build's): `CLAUDE_PID`
     where the environment carries it, else `claude_ancestor()`. Measured by this frame on 2026-10-07 in a
     Bash child of this harness: `CLAUDE_PID` is exported beside
     `CLAUDE_CODE_SESSION_ID`, and it equals the pid `ps -o ppid=,comm=`
     names as the `claude` ancestor of the shell (10196 on both sides, read
     off the process table). Whether a hook process the harness spawns sees
     it is `questions.md` M1; the `ps` walk stays either way (§13).
     `session-lease.py#main` records `claude_pid()` (NAME NOT IN TREE, the build's);
     `hooksession.session`'s lease route asks `from_lease(common, claude_pid(environ))`.
   - `SESSION_VARIABLE = "CLAUDE_CODE_SESSION_ID"`, the one name. `hooks/githooks.py#_P2`
     is formatted from it, and `$CLAUDECODE` leaves the stub: `hooksession.session`
     never reads it (hs:142), so a stub that starts Python on it alone
     starts an interpreter that answers no session unless a lease stands, and
     a lease starts it anyway. `hooks/tokens.py#steps_around_hooks` compares
     the one name (tk:127); the word `CLAUDECODE` leaves its list, because
     unsetting a variable the stub no longer reads leaves the stub its
     session. The verdict is the same in every state (plan.md Alternatives).
   `commitgate._process` is the `git commit` process, not the session's, and
   is untouched. `worktree-guard.py#host_app` labels the host application
   for the stop's text and is display only; its substring labels stay.

3. **The waiver token has one reader, and it refuses what does not split.**
   `hooks/tokens.py#given` is the reader (tk:83): bare words through `shlex`
   with the punctuation characters, parentheses stripped, comments kept,
   read in the command as written AND in `without_bodies`, nothing where the
   command does not split. `hooks/commit-review-gate.py#has_marker`
   (crg:657) and `hooks/worktree-guard.py#has_token` (wg:381) become
   `token in tokens.given(command)`; `crg#_reads_marker` with its substring
   fallback (crg:691-697) and the guard's `carries` closure and
   `_without_bodies` (wg:442) go. `tokens.without_bodies` takes the fallback
   the guard's `_without_bodies` carried: where `hooks/cmdline.py` fails to
   load or the read raises, the frozen reader's `drop_heredoc_bodies` finds
   the bodies, so a broken reader leaves the single-stream creation deny a
   way past (released row T1 of `seal/releases/0.18.3.md`). What changes for
   a person: a command that does not split and carries `[no-review]` or
   `[no-parity]` as a substring waived its arm in the PreToolUse reading
   (crg:695) and now does not; the refusal names
   `git -c specseal.waive=review`, the spelling the hook reads with no text
   read at all. `hooks/answers.py#given` is untouched (Out).

4. **A failed git call is a failure the caller sees, and the parity arm asks
   on it.** `hooks/gate.py#git` is the one runner; `hooks/commit-review-gate.py#git`
   (crg:571) goes. The runner answers `None` on a non-zero exit, an
   `OSError` or a timeout, and `""` for an empty answer. Every caller that
   reads a non-zero exit as an ordinary *no* keeps that reading at its own
   line, explicitly (`rev-parse --verify --quiet HEAD` on an unborn branch,
   `config --get-all specseal.waive` with no key, `symbolic-ref -q HEAD`
   when detached, `rev-parse --git-dir` outside a repository). The path
   readers — `commitgate.pre_commit`'s `diff --cached --name-only` (cg:229),
   `_paths_between` (cg:266), `crg.changed_paths` (crg:616) — hand
   `arms_missing` `None` where git failed, and `gate.touches_code(None)` is
   True: a change git could not list is not a change confined to the
   document roots, and the parity arm asks. Read, not run, as #868 says of
   it; S10 runs it. The mark readers already refuse on `""` and are
   unchanged.

5. **#856: a brace expansion in a git segment is an unrecognised shape.** The
   third answer, and it follows from §A as #826 wrote it. bash and zsh make
   other words of `{main,feature/x}`, `--ro{,}` and `{1..3}` before git
   runs (executed by this frame: `git rebase main feature/x`,
   `git rebase --ro --ro feature/x`, `git stash branch x`, `x1 x2 x3`), so
   the words the frozen reading read are not the words git reads, and §A's
   question has no answer for them. A git segment one of whose words holds
   `{…,…}` or `{….. …}` outside quotes is unrecognised, finding kind
   `brace`; its plain spelling is the words written out as bash would make
   them. Quotes are read off the judgment text with its quoted spans removed
   (the test `hooks/tokens.py#is_plain` already makes, tk:216), because the
   frozen splitter has taken the quotes off the words: `git commit -m '{a,b}'`
   stays listed. Judged in the tree its segment names, like every
   unrecognised shape; silent in a clean single-stream tree, so
   `git worktree {add,} ../wt f` there creates without consent and the
   writer files nothing for it, the hidden-spelling bullet of §*Known
   limits* with one more example. Two named costs: a command holding a
   quoted brace in one listed segment and an unquoted one in another stops
   both; and `git -C <dir>` or a `cd` operand holding a brace is read by the
   frozen walk as one word, so the segment is placed where that word names,
   which is nowhere, and falls back to the session's own tree. The reading
   lives in `hooks/worktree-guard.py#_git_finding` and `_described`;
   `hooks/cmdline_base.py` is not opened. The docstring of
   `_rebase_names_a_branch` and released row R1 (`seal/releases/0.20.0.md`)
   say `--root` is read *off the words bash hands git*; the code reads the
   words once their redirections are off, and both say so (#856 item 2).
   Stop cost: measured by the method of work item 1791270162's phase 1
   (`questions.md` M2), recorded in `phases/phase-1.md` and in §A's
   failure-direction paragraph.

6. **What leaves the tree.** `worktree_consent.py#creation_directory`'s
   placement loop; the body of the guard's `judgeable` and its tokenizing
   adapter's doubling line (one home each); `session-lease.py#owner_pid`'s
   walk; the guard's basename test in `sessions_in_tree`;
   `commit-review-gate.py#git`; `commit-review-gate.py#_reads_marker` and
   the body of `has_marker`; the guard's `has_token` body and
   `_without_bodies`; the word `CLAUDECODE` from `githooks._P2` and from
   `tokens.steps_around_hooks`; two of the three `(…)` strips. Cases whose
   subject goes are retired or rewritten against the one reader, and the
   build names each in `phases/phase-N.md`.

### Out

- **`hooks/answers.py#given`'s match by `ps args=` text** (#868 item 3's
  last sentence). Two parallel calls with the same command text cannot be
  told apart, and `docs/the-commit-gate-inside-git.md` §*Known limits*
  already says so. Measured by this frame: the harness exports no per-call
  id to a Bash child (`env` on 2026-10-07 shows `CLAUDE_CODE_SESSION_ID`,
  `CLAUDECODE`, `CLAUDE_PID`, `CLAUDE_CODE_CHILD_SESSION` and nothing
  naming a tool use), so there is no owned input to read instead. Stays.
- **The other copies #868 lists for scope** — `WRAPPERS` ×4, the git-dir
  resolvers ×6, the once-per-session markers ×6, the `automation_answered`
  wrappers ×3. No measured disagreement; #835's registry names them.
- **The guard's enumeration of other sessions by `ps -axo comm`** against
  the lease records (part 1 row 184). That is the guard's activity model,
  not the session's identity; In 2 gives it the one predicate and nothing
  else.
- **The writer recording a creation whose exit status it never reads**
  (part 1 row 134). `test_a_failed_creation_still_records_the_approval`
  pins it as intended: the approval is the fact recorded.
- **`hooks/cmdline_base.py`.** Unchanged; nothing here needs it reopened.
- **#856's answer (a)**, expanding braces in the guard. Rejected in
  `plan.md` Alternatives.
- **Windows.** In 1's adapter and In 2's `ps`-less route are read, not run;
  `questions.md` names the answerer.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given a session at `S` with a clone, when `eval x ; cd <A> \|\| git worktree add ../wt f` reaches the guard and then the writer, then the guard judges `S`'s clone and the record is written under `S`'s clone | a case red at 5623d728 (the writer files under `<A>`'s clone there) |
| S2 | Given `cd <missing> ; git worktree add ../wt f`, when the writer runs, then it records under the session's clone | a case red at 5623d728 (no record there) |
| S3 | For every chain of `BASE_TREE_CHAINS`, the inventory's shape and S2's, the writer's directory is the guard's `judgeable` target | a property case over the list; the three existing writer cases stay green |
| S4 | Given a process tree whose nearest ancestor's comm is `/x/bin/claude`, both `session-lease.py#owner_pid` and `hooksession.claude_ancestor` name it; given one whose comm is `claude-host`, neither does and the lease omits `pid` | cases against a fixture tree, through the one reader |
| S5 | Given `CLAUDE_PID` in the environment, the lease records it and the hook's lease route reads it, with no `ps` run; with it absent, the `ps` walk answers as today | cases; `test_s9_an_emptied_environment_is_still_judged_through_the_lease` stays green |
| S6 | The stub's text carries `CLAUDE_CODE_SESSION_ID` and no `CLAUDECODE`; `CLAUDECODE= git commit -m x` is plain (`is_plain`) and stands aside where git decides; `CLAUDE_CODE_SESSION_ID= git commit -m x` is judged by the reading | cases; the `CLAUDECODE` fixtures of `test_the_commit_gate_decides_at_the_commit.py` rewritten to the one name, one of them flipped to plain |
| S7 | Given `git commit -m 'x [no-review]` (an unclosed quote), when the PreToolUse reading judges it in an opted-in, undeclared clone, then the review arm is missing and the refusal names `git -c specseal.waive=review` | a case red at 5623d728 (waived through the substring fallback there) |
| S8 | For every command in the three consent-token corpora (`test_the_old_spellings_reach_the_hook.py`, `test_one_heredoc_shape_is_data_to_the_commit_gate.py`, the guard's `BODY_TOKENS`/`TYPED_BESIDE_A_BODY`), `has_marker` and `has_token` answer what `tokens.given` answers | a property case over the corpora; T1's and W1's cases stay green |
| S9 | `[worktree-ok]` in a comment, in parentheses and beside a body is read as today; a token only a body carries is not | the existing guard cases, unchanged |
| S10 | Given a repository declaring `seal/parity.md` and a `git` whose `diff` exits non-zero, when `pre-commit` and the PreToolUse reading judge a code commit, then the parity arm is among the arms missing | a case red at 5623d728 (silent there) |
| S11 | `git rebase {main,feature/x}`, `git rebase --ro{,} feature/x`, `git stash {branch,} x` and `git worktree {add,} ../wt f` stop in an ACTIVE tree, each with the `brace` plain spelling; under the press the stop is a `deny` | cases red at 5623d728 (silent there; #856's table) |
| S12 | `git commit -m '{a,b}'`, `git log --format='{%h}'` and `git commit -m "{a, b}"` stay listed and silent in every tree | cases |
| S13 | The git-binding case of `tests/test_worktree_guard.py` runs the four S11 forms through bash and reads HEAD moved for the two rebases and the stash | the case extended, executed under bash |
| S14 | `_rebase_names_a_branch`'s docstring says the words are read once their redirections are off | the docstring; a `Corrected ·` row for R1 in the fragment |
| S15 | `docs/worktree-guard-spec.md` §A names the brace shape, its plain spelling and its two costs, §*Known limits* adds the brace creation to the hidden-spelling bullet, §*Creation consent* says the record's clone is the one the guard judged; `docs/the-commit-gate-inside-git.md` names `CLAUDE_PID`, the one predicate and the one variable; `docs/commit-review-gate-spec.md`'s consent-read paragraph says a command that does not split carries no token; `docs/the-review-and-parity-arms.md` §*Parity arm* says a diff git could not take is asked about | the policy pin cases, each sentence with its `Enforced by:` line |
| S16 | The stop cost of In 5 and the waiver cost of In 3 are counted over the recorded corpus by the method of 1791270162's phase 1 | `phases/phase-1.md`; the probe deleted |

## Data & interfaces

- `hooks/hooksession.py`, three names the build adds (NAME NOT IN TREE): `SESSION_VARIABLE`, `is_claude(comm)`,
  `claude_pid(environ=None)`; `session` and `from_lease` keep their
  signatures.
- `hooks/session-lease.py#owner_pid` → `hooksession.claude_pid()` — NAME NOT IN TREE since phase 4 removed it.
- `hooks/githooks.py#_P2` formatted from `hooksession.SESSION_VARIABLE`; the
  stub's bytes change, so the installer rewrites every opted-in clone's
  stubs at the next session, as §*The hooks are stubs* says it does.
- `hooks/tokens.py`: `given` unchanged in signature; `without_bodies` with
  the frozen fallback; `steps_around_hooks` reading the one name.
- `hooks/gate.py#git(args, cwd) -> str | None`; `touches_code(None) is True`;
  `arms_missing`'s `paths()` may answer `None`.
- `hooks/worktree_consent.py`: the one tokenizing adapter and the one
  placement function; `creation_directory` through them.
- `hooks/worktree-guard.py`: `has_token`, `judgeable`,
  `_tokenize_with_separators` and `sessions_in_tree` import; `_git_finding`
  and `_described` gain `brace`; `_rebase_names_a_branch`'s docstring.
- `hooks/commit-review-gate.py`: `git` → `gate.git`; `has_marker` →
  `tokens.given`; `changed_paths` answers `None` on a failed diff.
- Policy: the four documents S15 names, with `Enforced by:` lines.
- Ledger: `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md`,
  with `Re-read ·` or `Corrected ·` rows for G3 and G6
  (`seal/releases/0.17.0.md`), W1 (`0.18.2.md`), T1 (`0.18.3.md`), F3 and
  R1 (`0.20.0.md`), as `docs/the-evidence-ledger.md` §*A released row is
  read again in the branch's fragment* says.

## Open questions → questions.md

`questions.md` holds two measurements and one question the work answers.
No row is a person's: #856's choice is decided from §A (In 5), and the
grounds are there and in `plan.md`'s Alternatives for a reader to overturn.

Framed 2026-10-07 by framer, before the build.
