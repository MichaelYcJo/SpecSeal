# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — round 2, fix pass

Both findings were reproduced before either was fixed, and the report's
paste-ready fix for finding 1 was not taken on reading.

**Finding 1's paste-ready fix was refused for what it costs, and a narrower one
shipped.** The report proposed moving `judge_creation` above rows 1-b and 2
wholesale, on the argument that every row below the ACTIVE deny ends in an
`ask` whose approval runs the whole command line. That argument is right about
the `ask` branch and wrong about the other one: a choice site's **deny** stops
the whole command, creation included, and it is the branch that names the idle
sessions and offers *split into a worktree*. Moving the creation above the site
entirely takes that first-attempt deny away — and with a consent record present
it takes it away in favour of a bare `ask`, because `guard_worktree_creation`'s
record row sits above its own ladder. The record says *this session may create
worktrees*; it says nothing about taking another session's branch out from
under it, and the switch direction is documented as never reading it.

So `choose` takes a `before_ask` that runs on the fallback branch only. The
deny branch is untouched, every switch verdict is where it was, and the branch
that would have let the command through hands the creation its verdict first.
Executed, both the idle and the detection-unusable state: attempt 1 `deny` with
the switch's two options, attempt 2 `deny` naming the creation, attempt 3 `ask`
naming the creation. There is no attempt at which the command proceeds without
the creation question having been put.

**Two things came out of re-enumerating rather than out of the report.**

- Finding 2's class is wider than the four shapes measured. `~/git worktree add
  …` and `*/git worktree add …` were allowed too — and the docstring one line
  above already claimed that *a glob in the COMMAND WORD is refused one line
  below, where `git` has to be the word itself*, which the basename comparison
  made false.
- The property the `576` figure stood for was the weaker half. *Never silent*
  does not cover a row that answers `ask` about something else, which is
  exactly what finding 1 is. The sweep and the case that pins it both test
  *denied, or the `ask` names the creation* now.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `bba7dab` — `choose` takes a `before_ask` its fallback yields to, and the switch ladder's two choice rows pass it the creation's own judgment. The deny branch is untouched, so every switch verdict is where it was; only the `ask` that would have run the command line yields. Seen red first: idle → `deny` then `ask`, detection-unusable → `deny` then `ask`, the creation question put at neither, and the `ask` reading *Approve — switch branches in this shared tree*. Mutation, `before_ask=` deleted at both sites: `test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned` and `test_the_guard_is_never_silent_where_the_writer_records` both go red, source restored from bytes saved first |
| 2 | fixed | `bba7dab` — `os.path.basename(tokens[0]) != "git"` becomes `tokens[0] != "git"`. The boundary the line implements is *a command word carrying no separator, so the shell resolves it on `PATH`*; anything with a `/` names a file this hook cannot identify. Re-enumerated by construction over 32 command-word shapes: exactly five pass, and all five are the word `git` after lexing (`git`, `\git`, `'git'`, `"git"`, `g"i"t`). Seen red first: `./git`, `../git`, `bin/git`, `/tmp/evil/git`, `~/git` and `*/git` all answered `allow` with a record present. Mutation, the basename restored: `test_a_path_qualified_git_carries_no_allow` goes red, source restored from bytes saved first |
| 8 | fixed | `f4db784` — the figure does not reconstruct and the axes were the weaker property, so both were replaced. `docs/worktree-guard-spec.md`, `spec.md` and the ledger row now carry 21 command shapes × 5 tree states × 2 shell directories × 2 record states × 3 attempts = **1260 combinations**, of which 230 are cells `worktree_consent.creation_directory` resolves a repository for, and **0** reach a verdict that lets the command run without the creation question. With both fixes reverted the same sweep finds **64** |
| 13 | fixed | `f4db784` — `rounds/round-1-report.md`'s `Worktree` field carried this machine's own absolute path; it is `/Users/x/…` now, the shape `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* names. Seen red first: `bin/test tests/test_no_real_identifiers.py -q` failed on that line and nothing else; green after |
