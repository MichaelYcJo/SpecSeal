# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — review round 2

| Field | Value |
|---|---|
| Target SHA | 1b4447731830a159891941c5451cee51d13207d2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #679 — https://github.com/MichaelYcJo/SpecSeal/pull/679 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `6a5afede50f415e21b1db7d2cc7d402602bc4806..c18d8a56ed1a109ccef3987fed70de48bd68fb04`, 6 commits |
| Contract changes | none |
| New units | test_a_cd_behind_a_redirection_moves_the_tree_the_guard_judges (depth 1); CD_BEHIND_A_REDIRECTION (depth 1); test_a_cd_with_a_redirection_among_its_words_lands (depth 1); test_a_cd_behind_a_redirection_the_splitter_cut_lands (depth 1); test_a_cd_the_splitter_cut_after_its_operand_lands_once (depth 1); test_a_cd_landed_past_a_redirection_keeps_the_directory_the_base_judged (depth 1); test_a_second_reading_that_unplaces_keeps_the_base_directory (depth 1) |
| Needs a fix | yes — 🟡 1 (a `cd` with a redirection among its words is never landed: the guard, the consent writer and two session kinds of the commit gate judge the wrong tree), 🟡 2 (the walk's second reading replaces the base's directory where only it unplaces) |
| Loses a record or crashes | yes — 🟡 1: `creation_directory` files `2>/dev/null cd w && git worktree add` and `cd w 2>/dev/null && git worktree add` under the session's own clone, so the clone the creation ran in gets no record and the session's clone gets one nobody gave. The same effect counted as yes for round 1's red 1, and here it is also present at `86256492` |

- [x] Pass

## What this round was asked

Round 2, verifying, over round 1's fix range `3b8522c3..cd4a65d7` at HEAD `1b444773`, against `86256492` and `3b8522c3`. Asked whether each of round 1's nine verdicts is closed. The pushes:
- the invariant, rebuilt: a W1 corpus in four session kinds, the header depths to 10,000 with timing, and the recorded transcript commands, both directions;
- the new readers against real bash and zsh on the pinned controls and near shapes;
- the worktree guard and the consent writer against the base;
- whether `2>/dev/null cd w && git switch -c nb`, silent in the guard at every SHA, is a defect in this item's class, with a minimal fix;
- the ledger rows and the three checks, and the interpreter floor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a `cd` with a redirection among its words (`cd W 2>/dev/null`, `2>/dev/null cd W`, `cd W>/dev/null`) is never landed, so the worktree guard skips the tracked-changes question for a switch into a dirty clone, the consent writer files the creation under the session's clone, and the commit gate is silent from a directory not opted in and under `[no-review]` over a parity arm | `hooks/cmdline.py#walk_directories` | **fixed** `70f36764` | fixed at 70f36764 — `4782fd65`, `b9098078`, `274b4932`. The walk now reads a `cd` again with its redirections taken off, and adds that landing in front of the answer it already had. It never replaces that answer. The glued view is read only where no earlier part of its group held a `cd`. Seen red (executed): 14 cases were red against `6a5afede`'s `cmdline.py` and are green at the head: the 7 `CD_BEHIND_A_REDIRECTION` spellings, the 3 cut shapes, the 3 landing-once shapes and the guard/consent case. Mutants on an exported copy: M3 (no landing) turned 14 red; M4 (landing behind) turned the guard case red; M5 (the paste-ready version) and M7 (`cds` never recorded) turned the 3 landing-once shapes red; M6 (glued view never read) turned the 3 cut shapes red. M8, where the landing replaces the as-written answer, survived every case. So `274b4932` plants `test_a_cd_landed_past_a_redirection_keeps_the_directory_the_base_judged`, which is red under M8 only and green at `86256492`, `6a5afede` and the head. Records: new row I13, I2 and I12 re-read (`4133a2f5`). What it costs: the landing counts toward `STATE_CAP`, so 9 `2>/dev/null cd sub;` segments now read silent under `[no-review]` (questions.md Q7, `c18d8a56`); Executed through `main()`: silent at `86256492`, `3b8522c3` and the head on 8 of 9 tails from a directory not opted in and 5 of 9 under the waiver. The guard is silent on 3 switches, and bash 3.2.57 and zsh 5.9 commit in all 8 shapes given. With the fix, 38 of 38 stop and the guard asks. The corpus loses 0 and adds 8 real commits. 9 cases are red at the head and green with the fix |
| 🟡 2 | the walk's reading past redirections replaces the directory the base judged wherever it alone unplaces the segment, so a command the base stopped reads silent under `[no-review]` | `hooks/cmdline.py#walk_directories` | **fixed** `70f36764` | fixed at 70f36764 — Where only the second reading unplaces and the first found `git`, the walk adds the unresolved directory beside the base's. Seen red (executed): `test_a_second_reading_that_unplaces_keeps_the_base_directory` was red at `6a5afede` and is green at the head. M1 (`placed` never true) turns it red. M2 (`placed` always true) turns `REDIRECTED_UNPLACED`'s `2>/dev/null nice -n 5 git` red. Records: new row I14; E10 re-read; E7's "holds again" corrected (`4133a2f5`); E7's claim narrowed to the cap (`c18d8a56`); Executed: `nice 2>/x/git commit -m git` and `env </x/git commit -m git` under `[no-review]` over a parity arm ask at `86256492`, are silent at `3b8522c3` and the head, and ask with the fix. Neither commits, but the policy sentence, E7's lead and the changelog's "only adds stops" are false as written |
| ⬜ 3 | round 1's fix-pass note says a commit is counted only where a shell reads `git`, and a quoted `>` reads as one the shell does not run | `seal/ledger.md` | answered | Corrected at `4133a2f5`. The `seal/ledger.md` row now says a quoted `>` also reads as a commit, and carries a `Corrected 2026-09-30` note; the claim cell is narrowed as well. Executed: `"git>x" commit -m x` and `git">"/dev/null commit -m x` give 1 invocation at the head and 0 at `86256492`, and deny in an opted-in undeclared repository. Neither bash 3.2.57 nor zsh 5.9 commits for either; Executed: `"git>x" commit -m x` and `git">"/dev/null commit -m x` read as commits at the head, while bash and zsh commit neither. A correction to the note |
| ⬜ 4 | every body read is split twice and cut again, so a flat chain of host words costs about 1.8 times the base | `hooks/commit-review-gate.py#_reads_a_commit` | answered | Recorded at `c18d8a56` in `overview.md` §Not done. Executed through `commit_invocations` on `git -C /x commit -m x; ` followed by `sh -c` ×600 and ×1,000. At `86256492`: 2.33 s and 6.20 s, with 180,300 and 500,500 calls to `split_segments_with_separators`. At `b9098078`: 4.14 s and 11.04 s, with 360,599 and 1,000,999 calls. That is 2.0 times the splits and about 1.8 times the time. Extrapolated, not run: the 600 s limit falls near 9,800 words at the base and 7,400 at the head. It is a performance pass, not a fix here; Executed: 600 `sh -c` words take 13.7 s against 8.1 s, and 1,000 take 15.9 s against 8.7 s, quadratic at both. The 600 s window between about 6,150 and 8,300 words is extrapolated, not run |
| 🟢 | round 1's blocking finding 1 is closed — W1's refusal is added beside the base's directory in the gate, the guard and the consent writer | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 9,408 W1 commands in four session kinds lose 0 and add 0 against `86256492`, where `3b8522c3` lost 1,646. 15 of head's cases red at `3b8522c3`'s hooks. The guard and `creation_directory` match the base on 21 shapes |
| 🟢 | round 1's blocking finding 2 is closed — the header readings stop at 32 and keep the commits found | `hooks/cmdline.py#_is_the_program` | confirmed | Executed: 24 depth cases through `main()` stop at the head at every depth, silent at `3b8522c3` from 1,200, 0.5–12.6 s at 10,000 against 0.5–12.8 s. 6 cases red at `3b8522c3` |
| 🟢 | round 1's yellow 3 is closed — a `cd` behind a cut redirection adds an unresolved directory | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 7 cut shapes add it, bash and zsh commit in `U`. 11 walk cases red at `3b8522c3` |
| 🟢 | round 1's yellow 4 is closed — a glued operator is read | `hooks/cmdline.py#unglued` | confirmed | Executed: all 12 glued shapes bash commits read, and 21 no-commit cases red at `3b8522c3`. Two extra stops that commit nothing are white 3 |
| 🟢 | round 1's yellow 5 is closed — zsh's precommand words and short loop are read | `hooks/cmdline.py#RUNNERS` | confirmed | Executed under zsh 5.9. `for d in git commit` reads nothing and commits nothing. Four new stops commit nothing and are the stand-in's accepted class |
| 🟢 | round 1's yellow 6 is closed — a shell's string is found past options and `--` | `hooks/cmdline.py#command_strings` | confirmed | Executed: 11 shapes bash commits all read. `--norc` behind `-c` is a stop bash refuses to run |
| 🟢 | round 1's white 7 is closed — the checker refuses nothing | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md` | confirmed | Executed: `evidence-check . --strict` exit 0, 3,026 ok, 0 refused |
| 🟢 | round 1's white 8 is closed — the records say added beside | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | confirmed | Read against the code at the head. The changelog's "only adds stops" waits on yellow 2 |
| 🟢 | round 1's white 9 is closed — I5 carries the recorded figure | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | confirmed | Executed over 28,527 recorded commands: the same 3 are the only difference between `86256492` and `3b8522c3` |
| ❓ | the 18 mutants round 1's fix pass names for its changed branches | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | ❓ out of verified scope | Read, not re-run. The fix pass's records answer for them |
| ❓ | the cases on Windows | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | CI's `windows-latest` leg at the pull request answers it |

## Paste-ready fixes

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def walk_directories(items, cwd):
         # Asked as written and read past its redirections (#674), and either
         # one unplaces: `2>/dev/null nice -n 5 git commit` stands behind a
         # runner's options that the first reading never reached.
-        if command_word(tokens)[1] or command_word(tokens, redirections=True)[1]:
+        unplaced = tuple(
+            w if isinstance(w, Unresolved) else Unresolved(str(w), Unresolved.CONSTRUCT)
+            for w in wheres
+        )
+        first, first_unplaced = command_word(tokens)
+        if first_unplaced:
             # A command behind a reserved word that begins a list, or inside a
             # construct whose command word is not found by position (#669).
             # Written across lines it would follow a segment `understood`
             # refuses, and that is the directory it gets here too.
-            wheres = tuple(
-                w
-                if isinstance(w, Unresolved)
-                else Unresolved(str(w), Unresolved.CONSTRUCT)
-                for w in wheres
+            wheres = unplaced
+        elif command_word(tokens, redirections=True)[1]:
+            # Only the second reading unplaces. Where the first already found
+            # `git`, that is the commit `86256492` judged in WHERES, and the
+            # unresolved directory is added beside it rather than in its
+            # place (round 2 of 1790660768): `nice 2>/x/git commit -m git`
+            # stopped on the parity arm at the base, and `[no-review]` waived
+            # the replacement whole.
+            placed = bool(first) and os.path.basename(first[0]) == "git"
+            wheres = (
+                _directories([(w, None) for w in wheres + unplaced])
+                if placed
+                else unplaced
             )
         walked.append((tokens, wheres))

@@ def walk_directories(items, cwd):
             (here if target is None else _land(here, prev, target), here)
             for here, prev in running
         ]
+        # A redirection among a `cd`'s words -- after its operand (`cd W
+        # 2>/dev/null`), glued to one (`cd W>/dev/null`), in front of it, or
+        # cut by the splitter (`2>&1 cd W`) -- is the shell's, and the `cd`
+        # still lands in W (round 2 of 1790660768). Read as an operand it
+        # made the target unknown, and read as the program it left the shell
+        # where it was: silence from a session that is not opted in, and
+        # under `[no-review]` over a parity arm, where `cd W` stops. The
+        # landing read past it is ADDED in front of that answer and never
+        # replaces it, so the commit gate judges both, and the worktree guard
+        # and the consent writer, which take the first directory they can
+        # name, take the one the shell went to.
+        view = _expanded(glued[index], env) if index in glued else tokens
+        past = _cd_target(_without_redirections(unglued(view) or view))
+        if past is not None and past != target:
+            moved = _dedup(
+                [(_land(here, prev, past), here) for here, prev in running] + moved
+            )

         # A construct the reader does not understand leaves the shell
```
```diff
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@ So each place a program word stands is read past what the shell takes off it:
   for a redirection glued to a word's end (`cd>/dev/null W`), and for one the
-  splitter cut (`2>&1 cd W`).
+  splitter cut (`2>&1 cd W`). A redirection after a `cd`'s operand, or glued
+  to one (`cd W 2>/dev/null`, `cd W>/dev/null`), is the shell's as well. The
+  landing read past any of these is added in front of the directory the walk
+  read with it: the gate judges both, and the worktree guard and the consent
+  writer, which take the first directory they can name, take W.
@@ The reading can only have gained stops by this.
 asked before first and adds what the new reading finds, `understood`'s
-refusal is added beside the directory the walk read before, and a generated
+refusal is added beside the directory the walk read before, the walk's
+reading past redirections unplaces a segment beside its directory and never
+in place of it, and a generated
 corpus of 11,393 commands across these positions found none silent where the
--- a/docs/worktree-guard-spec.md
+++ b/docs/worktree-guard-spec.md
@@ ### Which tree, when the command walks to it
 was while the commands do not. Both are read the same way the commit gate
-reads them (`commit-review-gate-spec.md` §Which repository).
+reads them (`commit-review-gate-spec.md` §Which repository). A redirection
+among the `cd`'s words (`cd W 2>/dev/null`, `2>/dev/null cd W`, `cd>/dev/null
+W`) moves it too, since round 2 of work item 1790660768; until then the switch
+was judged in the session's own tree while it ran in W.
```
```diff
--- a/seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/changelog.md
+++ b/seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/changelog.md
@@
   cut (`2>&1 cd W`), and a shell's string past `--` or an option after a
   redirection (`bash -c 2>/dev/null -- "$CMD"`). bash or zsh committed for
-  each.
+  each. A `cd` with a redirection after its operand (`cd W 2>/dev/null && git
+  commit`) now lands in W too. It was silent from a directory that is not
+  opted in and under `[no-review]`, and the worktree guard judged the
+  session's own tree for a switch made in W.
```
```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
CD_BEHIND_A_REDIRECTION = [
    "cd {d} 2>/dev/null",
    "cd {d} >/dev/null",
    "cd {d} 2> /dev/null",
    "cd {d} </dev/null",
    "cd {d} >/dev/null 2>&1",
    "cd -P {d} 2>/dev/null",
    "cd {d}>/dev/null",
]


@pytest.mark.parametrize("cd", CD_BEHIND_A_REDIRECTION)
def test_a_cd_with_a_redirection_among_its_words_lands(
    monkeypatch, capsys, projects, tmp_path, cd
):
    """Round 2 of 1790660768. A redirection after a `cd`'s operand is the
    shell's, and the `cd` still lands; the walk read it as a second operand
    and left the target unresolved. An unresolved target is silence from a
    session that is not opted in and is waived whole by `[no-review]`, so
    both commands were silent at `86256492` and at #674's head, where `cd D
    && git commit` stops. bash 3.2.57 and zsh 5.9 commit in D."""
    plain = tmp_path / "plain"
    plain.mkdir()
    make_repo(plain / "u2")
    command = f"{cd.format(d='u2')} && {BODY}"
    got = decisions(monkeypatch, capsys, command, plain, "s")
    assert "silent" not in got, (command, got)
    session = make_repo(tmp_path / "session", declared=True)
    (session / "sub").mkdir()
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    command = f": '[no-review]'; {cd.format(d='sub')} && {BODY}"
    for which, got in with_and_without_the_press(
        monkeypatch, capsys, projects, command, session
    ).items():
        assert "silent" not in got, (command, which, got)


def test_a_second_reading_that_unplaces_keeps_the_base_directory(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 2 of 1790660768. The walk's reading past redirections REPLACED
    the directory the base judged with an unresolved one wherever it alone
    unplaced the segment, and `[no-review]` waived that whole: `nice
    2>/x/git commit -m git`, a commit to the base's reading, stopped on the
    parity arm at `86256492` and was silent at #674's head."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    for shape in ("nice 2>/x/git commit -m git", "env </x/git commit -m git"):
        command = f": '[no-review]'; {shape}"
        for which, got in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            assert "silent" not in got, (command, which, got)
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py: add `import shutil` beside
# `import shlex`, then append
def test_a_cd_behind_a_redirection_moves_the_tree_the_guard_judges(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of 1790660768. A redirection among a `cd`'s words is the
    shell's, and the switch runs in the tree the `cd` reached. The walk read
    it as an operand or as the program, and the guard judged the clean
    session tree instead of the dirty one the switch lands in -- silent at
    `86256492` and at #674's head. The consent writer filed the creation
    under the session's clone for the same reason."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    for command in (
        "cd w 2>/dev/null && git switch feature/x",
        "2>/dev/null cd w && git switch feature/x",
        "cd>/dev/null w && git switch feature/x",
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, session)
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, (command, reason)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null cd w && git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted
```

## Executed probes

| What was run | Result |
|---|---|
| The W1 corpus through `main()`: 9,408 commands (784 segments × 3 separators × 4 session kinds) at `86256492`, `3b8522c3`, the head and the fix | Head against base: 0 lost, 0 added. `3b8522c3`: 1,646 lost. Fix against base and head: 0 lost, 8 added, all real commits. Raised: 0 anywhere |
| 28,527 recorded commands from 525 transcripts through `commit_invocations` at the four trees | Every base and `3b8522c3` target is found at the head and with the fix. Head against `3b8522c3`: 3 differ, round 1's own heredoc patches. Fix against head: 0 differ. Raised: 0 |
| Header nesting through `main()`: 3 kinds × 2 forms at 400, 1,200, 3,000 and 10,000, at `86256492`, `3b8522c3` and the head | Head stops at all 24. `3b8522c3` is silent at 18. At 10,000 the head takes 0.5–12.6 s and the base 0.5–12.8 s |
| 15 other chains at 5,000 through `commit_invocations` at base, head and fix | Nothing raised. The fix makes 5,000 `cd>/dev/null x;` take 4.0 s against 0.3 s |
| A chain of `sh -c` words at 500 and 1,000 at base and head, and a profile at 600 | 2.2 s and 8.7 s at the base, 4.0 s and 15.9 s at the head, twice the splits (white 4) |
| 69 shapes near the new readers through `commit_invocations` at three SHAs, and each in bash 3.2.57 and zsh 5.9 against fresh repositories | A shell commits in 50, and the head reads all 50. The two controls read nothing, and no shell commits. 7 new stops commit nothing |
| 38 `cd` tail shapes through `main()` in three session kinds at the four trees | Silent at base, `3b8522c3` and head on 18, and all 38 stop with the fix |
| 8 `cd` tail shapes in bash 3.2.57 and zsh 5.9 | Both shells commit in `U` for all 8 |
| The worktree guard and `creation_directory` on 21 shapes from a clean `S` with a dirty nested `w`, at the four trees | Head equals base on all 21. `3b8522c3` differs on round 1's 5. The fix differs from the head on 4: three switches ask and one creation is filed under `S/w` |
| `: '[no-review]'` over a parity arm with 4 commands whose `git` word is a redirection target, at the four trees | 2 ask at the base, are silent at `3b8522c3` and the head, and ask with the fix |
| The two changed test modules of the head against `3b8522c3`'s hooks | 59 failed and 525 passed: the 10 waiver prefixes, 4 not-opted-in shapes, the parked case, 6 header cases, 21 no-commit shapes, 11 walk shapes and 3 wrapper rows × 2 |
| 13 reader modules at the head, and at the fix with the 9 planted cases | 1,141 passed at the head. 1,150 passed with the fix, after the first version of yellow 2's fix turned `REDIRECTED_UNPLACED` red |
| The 9 planted cases against the head's hooks, and a mutant appending the landing behind the answer | 9 failed at the head. The mutant fails the guard case only |
| `ruff check` and `ruff format --check` on the fix's three files. `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py` with its doc edits | Clean. 58 passed |
| `bin/evidence-check . --strict`, `bin/correction-check --range origin/release/v0.16.0...HEAD` and `bin/survivor-check` over the same range, at the head | Each exit 0: 3,026 ok and 0 refused, no merge commit, 43 removed sentences with none standing |
| The four hooks this item reads, parsed and the gate run under `/usr/bin/python3` 3.9.6, at the head and with the fix | They parse, and the gate answers. No `strict=`, `pairwise` or `.UTC` in the fix |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while this round leaves yellows 1 and 2 open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#understood` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/cmdline.py#_is_the_program`, `hooks/cmdline.py#_segment_names_an_unknown_command` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/cmdline.py#walk_directories` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/cmdline.py#_REDIRECTION` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/cmdline.py#RUNNERS` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/cmdline.py#command_strings` | round 1's 🟡 6 — fixed |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md:43` | round 1's ⬜ 7 — answered |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | round 1's ⬜ 8 — answered |
| round-1 | `hooks/cmdline.py#_behind_a_runner` | round 1's ⬜ 9 — answered |
| round-1 | `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commit-review-gate.py#NESTING_READ` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-6.md` | round 1's ❓ — out of verified scope |
| round-1 | `tests/test_no_shape_the_base_stops_reads_silent.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The worktree guard reads an unresolved directory as the session's own and judges only a segment's first directory. So a switch into a dirty clone is silent at `86256492` and the head after `builtin cd w`, `command cd w`, `time cd w`, `pushd w`, `noglob cd w`, `cd "$W"` with `W` unset, and `2>&1 cd w`, where the walk reads the splitter's `&` as a background job. §*Which tree* states the fallback on purpose, and changing it is a guard design choice | #686, in no milestone: it waits on the owner's decision | the orchestrator, who files it, and the owner, who decides whether the guard asks on an unresolved directory |
