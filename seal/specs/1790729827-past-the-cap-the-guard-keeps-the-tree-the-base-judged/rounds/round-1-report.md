# Round 1 report — 1790729827 (#689)

Target SHA `69ebf6e7`, base `origin/release/v0.16.0` at `542f920b`, release base
`86256492`. This is a first round, so there is no earlier round record for this
item. Round 3 of 1790660768 was read for coordinates only.

## Summary

The condition works. It closes every row round 3 filed, and it closes both of
the flag's failures the build names. The build's claims about its own cases
reproduce: which cases were red, and which mutants were killed.

It does not keep the guard on the tree bash runs in, and that is question 2's
answer. Take a `cd` behind a redirection, into a directory that does not exist,
followed by `;` or a newline. The walk lands that `cd` in front, and that
landing is the walk's first directory, so the walk leads. The guard then finds
no repository there and falls back to the session's own tree. Bash's `cd` fails
and the switch runs in the dirty tree `86256492` asked about. The shape has
been silent since I13 (542f920b). Past the cap, the flag closed it and B keeps
it open, which answers the second half of question 1. That is yellow 1, and one
more clause in the same condition closes it (executed below).

The cause chain:

1. I13 lands a `cd` read past its redirections in front of the as-written
   answer. Nothing asks whether the landing exists.
2. The target keeps the walk in front wherever that landing is its first
   directory, before the cap and past it.
3. Joined by `;` or a newline, the guard takes the landing. It finds no
   repository there and falls back to the session's tree. The consent writer
   files the creation under the missing path, so nothing is recorded.
4. Bash stays where it was, in the tree `86256492` judged.

## Findings from execution

### Yellow 1 — a `cd` behind a redirection into a directory that does not exist leads, so the guard is silent on the dirty tree bash stays in

`hooks/cmdline.py#walk_directories`, the ordering condition:

```python
        if wheres and not isinstance(wheres[0], Unresolved):
            ordered = wheres + base_wheres
```

For `cd w; 2>/dev/null cd <missing>; git switch feature/x` the walk's
directories are `(<missing>, w, S, …)` and the base's are `(w, S)`. The first
is readable, so the walk leads. `judgeable` in `hooks/worktree-guard.py` falls
back to the session's own tree for a readable directory that holds no
repository. The guard is therefore silent. Bash's `cd` fails and the switch
runs in the dirty `w`.

Executed on a fixture with a clean session `S`, a nested `w`, a repository `O`
and a path `<missing>` that is never created. Bash ran each chain with `pwd` in
place of the git command.

| Chain (`<cap>` = `cd w; ` + 9 × `2>/dev/null cd nosuch; `) | bash in | `86256492` guard / consent | `542f920b` | target | round 3's flag |
|---|---|---|---|---|---|
| `cd w; 2>/dev/null cd <missing>; ` | `w` | `w` / `w` | `S` / `<missing>` | `S` / `<missing>` | `S` / `<missing>` |
| the same with a newline | `w` | `w` / `w` | `S` / `<missing>` | `S` / `<missing>` | `S` / `<missing>` |
| `<cap>2>/dev/null cd <missing>; ` | `w` | `w` / `w` | `S` / `<missing>` | `S` / `<missing>` | `w` / `w` |
| `<cap>2>/dev/null cd <missing>` + newline | `w` | `w` / `w` | `S` / `<missing>` | `S` / `<missing>` | `w` / `w` |
| `<cap>2>/dev/null cd O; ` (the landing exists) | `O` | `w` / `w` | `O` / `O` | `O` / `O` | `w` / `w` |
| control: `cd w; cd <missing>; ` (plain `cd`) | `w` | `S` / `<missing>` | the same | the same | the same |

The last row is `86256492`'s own silence, which comes from the guard's fallback.
The rows above it are silences the base did not have.

A generated corpus puts numbers on it: 4,380 commands, 19 segment shapes and
4 operators, half of them behind the capping chain. On a command where bash
switches in the dirty `w` and `86256492` judged `w`, the guard judges another
tree in 78 commands at `542f920b`, 36 at the target and 19 under the flag.
Every example printed at the target is a `2>/dev/null cd <path>` or `2>&1 cd
<path>` joined by `;` or a newline to a destination that does not exist.

- **Why it matters.** The guard exists to ask before a switch in a tree with
  uncommitted work. Here it is silent, and bash switches in exactly the tree the
  release base asked about.
- **The consent twin.** `cd w; 2>/dev/null cd <missing>; git worktree add ../wt`
  gets the answer `<missing>`. `hooks/worktree_consent.py#main` finds no
  repository there and records nothing. So `w`, where the creation ran, gets no
  record, where `86256492` filed it under `w`. The next creation there asks
  once. Round 3 of 1790660768 counted this same effect as *Loses a record*.
- **Whose it is.** The shape comes from I13 (round 2 of 1790660768). It is
  present at `542f920b`, so #689's condition did not cause it. It is in the class
  the spawn named (`;`, a newline, a `cd` past a redirection), and it is a
  regression against `86256492` inside this release. Past the cap, B is the
  choice that leaves it open, where the flag closed it.

The fix is a third clause in the same condition. The walk still leads where its
first directory is the base's too or is a directory on disk. Otherwise the base
leads. Executed on a clone:

- The four failing-landing cases (in front with `;`, in front with a newline,
  each with and without the cap) were red at `69ebf6e7` and are green with the
  clause. Each asks and names `f.txt`, and each files the creation under `w`.
- The landing that exists still leads, with and without the cap.
- The guard, guard-asks-once and no-shape modules pass with the clause, 13 new
  cases and the Q7 cap case included.
- Two routes stay silent with the clause: a plain `cd <missing>; ` and `cd
  <missing> 2>/dev/null; `. `86256492` is silent on both (the control row
  above), so they are the guard's fallback and not this finding.

The clause costs one `stat` per segment, and only where the walk's first
directory is a landing the base did not make. A directory that an earlier
segment of the same command creates does not exist yet at `PreToolUse`, so there
the base leads. That is a false ask in the conservative direction.

### Question 3 — the consent writer's reading past an unresolved first directory (yellow 2, deferred)

The build's 89 segments were not reproduced; that corpus was deleted. The shape
behind them was reproduced by hand:

| Chain | bash | `86256492` consent | `542f920b` / target / flag |
|---|---|---|---|
| `eval true; 2>/dev/null cd O \|\| git worktree add ../wt` | creation runs only if `cd O` fails | session `S` | `O` |
| the same behind the capping chain, with `eval true;` in front | the same | `S` | `O` |
| `eval true; cd O \|\| git worktree add ../wt` (plain `cd`) | the same | `O` | `O` |

- **The base thread names no readable directory.** The consent writer
  (`hooks/worktree_consent.py#creation_directory`) reads through the unresolved
  entries to the walk's `O`, which is the landing the `||` skips.
- **The order does not matter here.** `542f920b`, the target and the flag answer
  alike. So #689 did not cause this and did not change it.
- **Against `86256492`, the verdict splits by spelling.** For the redirection
  spelling this is a regression, because the base did not read that `cd` and
  filed under the session. For the plain spelling `86256492` gives the same
  answer.
- **The cost splits by branch.**
  - Where the creation runs, `cd O` failed, so `O` does not exist and the writer
    records nothing. That costs one extra ask.
  - Where `cd O` succeeds, nothing runs, and `O` gets a record nobody consented
    for. That is `86256492`'s own answer for the plain spelling.
- **No fix fits this layer.** A consent-side rule cannot tell this shape from
  S4's. There the entry behind the unresolved one is a live shell that runs the
  creation. Both spellings reach the writer as one flat tuple.
  Telling them apart needs `plan.md`'s alternative D, which splits running
  shells from skipped ones. That is a new interface for three consumers.

My answer to question 3: by command text, it is a regression for the
redirection spellings. The mechanism is `86256492`'s own, and the branch where a
creation runs fails in the conservative direction. It belongs with #686, which
already holds how the consent writer reads an unresolved first directory.

### The commit gate — the verdict set is unchanged

- **Read.** `ordered` is a permutation of `wheres + base_wheres`, and
  `_directories` deduplicates by the same key in either order. So the set of
  directories `commit_invocations` judges is the same as at `542f920b`, and
  only the listing order moves.
- **Executed.** Over the 4,380 commands, no directory in `86256492`'s set of
  `(directory, unresolved)` pairs is missing from the target's, `542f920b`'s or
  the flag's. Nothing raised.
- **Not re-run.** The build's corpus of 3,648 commands through `main()` was
  deleted, and I did not run another through `main()`.
- **Where order still counts.** `hooks/commit-review-gate.py#main` reads
  `stopped[0]` to pick which repository's marks the question names and which
  repository's `already_asked` budget is spent. So the three texts the build
  counted can name a different repository, while the decision stays the same.

## Findings from reading

### White 3 — the policy sentence says any `cd` after the collapse leads, and a relative one does not

`docs/commit-review-gate-spec.md` §*Which repository*, the `STATE_CAP`
paragraph: "A `cd` that moves the running shell after the collapse makes the
walk's first directory readable again, so it leads."

Executed through the target's walk:

- **Relative `cd`.** `<cap>cd sub && git switch x` gives the walk's first as
  unresolved. `_step` keeps an unresolved base unresolved for a relative
  operand, so the base leads, with `S/w/sub` first. The behaviour is right; the
  sentence is wider than it.
- **Absolute `cd`.** Only an absolute operand or `~` makes the first readable
  again.

### White 4 — M1's clause and phase 1's class table overclaim the same way

Corrections to the run's paperwork, not counted as fixes:

- **M1's clause.** It says "a `cd` that moves the running shell after the
  collapse leads again" (`seal/ledger/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged.md`,
  M1). The same relative-`cd` exception applies.
- **Phase 1's class table.** It says "`&&`, `;` and a newline, into a
  repository or a missing directory: the same at all four trees"
  (`seal/specs/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged/phases/phase-1.md`).
  For `2>/dev/null cd <missing>;` past the cap, `86256492` and the flag judge
  `w`, while `542f920b` and the target judge the session (the third row of the
  yellow 1 table).

### White 5 — I13's clause says the guard and the consent writer take W, which holds only where W exists

`seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`,
I13: "the worktree guard and the consent writer, which take the first one they
can name, take W". Where W does not exist and the next segment is joined by `;`
or a newline, they take W and the guard falls back to the session's tree
(yellow 1). This is a correction to the run's paperwork, and yellow 1's fix
makes the sentence true as written.

## The build's claims, opened

| Claim | What this round found |
|---|---|
| 10 of 12 guard cases red at `542f920b` | Executed: the 11 new cases and the Q7 cap case against `542f920b`'s hooks with this branch's tests. 10 are red and the landing case and the Q7 case are green. The gate's order case is red as well |
| the landing case red at `86256492` and under the flag, and the flag also leaves the 3 subshell cases red | Executed: `86256492` red on the landing case and the gate's order case. The flag red on the landing case and the 3 subshell cases |
| 4 non-equivalent mutants killed, `wheres and` equivalent | Executed: the pre-#689 test 10 red, the walk always first 11 red, the base always first 1 red, the last directory tested 5 red, and the `wheres and` mutant 0 red. Read: `running` is never empty, because every branch of `_branches` returns a non-empty list |
| 0 of 2,228 base stops lost over 3,648 jobs, 0 decision changes | Not re-run through `main()`. Read and executed at the level of the verdict set (above) |
| 0 cap-caused moves of the guard's first directory over 20,234 segments | Not reproduced as defined. The metric compares against an uncapped walk, so it cannot see yellow 1, where the capped and the uncapped walk are wrong alike and `86256492` is right |
| the flag makes I13 false past the cap, and leaves `(cd O)` under `w/nosuch` with no cap | Executed, both. The flag judges `w` and files under `w` for `<cap>2>/dev/null cd O && …`, where bash switches in `O`. It files `cd w; 2>/dev/null cd nosuch \|\| (cd O) && git worktree add` under `w/nosuch` |
| the fix moves the guard only toward `86256492` | Read: it differs from `542f920b` only where the walk's first is unresolved, and there it hands the consumers the base thread's order. Executed: the guard's losses against `86256492` fall from 78 to 36 and the consent writer's from 202 to 142, over the same corpus |

## The class (§12)

**Every way the walk's first directory can stand for a shell that is not
there.** There are three, and only the first two are this item's:

- a collapsed or unresolved first with a readable skipped branch behind it,
  which is round 3's case and closed;
- a readable first that is a landing the shell never made, because the `cd`
  failed, which is yellow 1;
- an unresolved first with a skipped landing behind it that the consent writer
  reads through, which is yellow 2 and goes to #686.

**Operators.**

- `||` is closed.
- `&&` into a missing directory runs nothing, so silence is right.
- `;` and a newline are yellow 1.
- A subshell is closed (S4).
- The merged view (`2>&1 cd <missing>`) keeps the as-written shell first, and
  it answered `w` at every tree measured.

**Consumers.**

- The commit gate: the set is unchanged; `stopped[0]` and the listing order
  move.
- The guard: yellow 1.
- The consent writer: yellow 1 and yellow 2.
- The creation allow-list reads no directory, so it is out of the class.

## Regression tests to plant

Destination: `tests/test_guard_resolves_the_tree_it_judges.py`, below the
subshell case. The block is under `## Paste-ready fixes`.

- **Seen red.** At `69ebf6e7` the four failing-landing cases fail with
  `('silent', '')`. With the clause they pass.
- **Not seen red.** The two cases of the landing that exists are controls.
  They pass at `69ebf6e7`, with the clause and at `542f920b`. They pin what the
  clause keeps, and no tree measured turns them red except the flag. §15 counts
  that as seen red only against round 3's flag, so the fix pass has to show it.

## Facts for the evidence ledger

- **M3, from the fix pass.** The walk leads only where its first directory is
  readable and is either named by the base thread or a directory on disk.
  Executed 2026-09-30: `cd w; 2>/dev/null cd <missing>; ` and the same with a
  newline, with and without the capping chain, ask about `w` and file under
  `w`. They were silent and filed under `<missing>` at `69ebf6e7` and
  `542f920b`, and asked at `86256492`.
- **The consent writer records nothing where the creation's directory holds no
  repository** (`hooks/worktree_consent.py#main`, `optin.repo_root`). So a
  misfiled missing directory costs the clone the creation ran in its record,
  and never writes one elsewhere.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a `cd` behind a redirection into a directory that does not exist is the walk's first directory and leads, so after `;` or a newline the worktree guard is silent on the dirty tree bash stays in, and the consent writer records nothing for it; `86256492` asked and filed there; before the cap since I13, and past it where round 3's flag closed it | `hooks/cmdline.py#walk_directories` | open | Executed: `cd w; 2>/dev/null cd <missing>; git switch feature/x` is silent at `542f920b` and the target and asks at `86256492`, while bash switches in `w`. Guard losses against `86256492` over 4,380 commands: 78 at `542f920b`, 36 at the target, 19 under the flag. The paste-ready clause turns the four planted cases green, and the guard, guard-asks-once and no-shape modules pass with it |
| 🟡 2 | behind an unresolved first directory, the consent writer reads through to a `cd` landing the `\|\|` skips when the base thread names no readable directory, which files `eval true; 2>/dev/null cd O \|\| git worktree add` under `O`, where `86256492` filed under the session | `hooks/worktree_consent.py#creation_directory` | deferred #686 | Executed: `O` at `542f920b`, the target and the flag, and the session at `86256492`. The plain spelling gives `O` at `86256492` too. No fix fits the order layer, because S4 needs the same read-through. Where the creation runs, `O` is missing and nothing is recorded. The build's 89 segments were not reproduced |
| ⬜ 3 | the policy sentence says a `cd` after the collapse makes the walk's first readable again, and a relative one leaves it unresolved, so the base leads | `docs/commit-review-gate-spec.md` §*Which repository* | open | Executed through the target's walk: `<cap>cd sub && git switch x` gives an unresolved first and the base leads. The behaviour is right; only the sentence is wide |
| ⬜ 4 | M1's clause says a `cd` after the collapse leads, and phase 1 says `;` and a newline into a missing directory answer the same at all four trees | `seal/ledger/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged.md` (M1) | open | A correction. Executed: `<cap>2>/dev/null cd <missing>; ` gives `w` at `86256492` and under the flag, and the session at `542f920b` and the target |
| ⬜ 5 | I13's clause says the guard and the consent writer take W, and where W does not exist and `;` follows, the guard takes the session's tree | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` (I13) | open | A correction. Executed, the first row of yellow 1's table. Yellow 1's fix makes the clause true as written |
| 🟢 | the condition closes round 3's yellow 1 and every row it filed, with the capping prefixes and the four spellings behind `\|\|` | `hooks/cmdline.py#walk_directories` | confirmed | Executed: the 10 cases red at `542f920b` are green at the target. The hand rows `<cap>cd <missing> \|\| ` and `<cap>2>/dev/null cd <missing> \|\| ` answer `w` at `86256492`, the target and the flag, and the session at `542f920b` |
| 🟢 | the flag breaks I13 past the cap and leaves the subshell case open, as the build said | `plan.md` §*Alternatives considered* | confirmed | Executed: the flag red on the landing case and the 3 subshell cases |
| 🟢 | the commit gate's set of directories is unchanged, and only the order moves | `hooks/cmdline.py#walk_directories` | confirmed | Read: a permutation, deduplicated by one key. Executed: 0 of 4,380 commands miss a directory of `86256492`'s |
| ❓ | whether the 3 deny texts that now name a different repository first read right to a person | `hooks/commit-review-gate.py#main` | ❓ out of verified scope | Read: `stopped[0]` decides the named repository and which `already_asked` budget is spent, and the decision is unchanged. The build's corpus was deleted and the three texts were not seen. The orchestrator answers, with the three commands from the build if they can be recovered |

## Executed probes

| What was run | Result |
|---|---|
| The two changed test modules at the target, `bin/test` in the clone | 90 passed |
| The 11 new cases, the Q7 cap case and the gate's order case against the hooks of `86256492`, `542f920b`, the target, round 3's flag and four mutants of the target, each paired with this branch's tests | `86256492` 2 red (landing, gate order). `542f920b` 11 red. Target 0. Flag 4 red (landing, 3 subshell). Walk always first 12. Base always first 1. Last directory tested 6. `wheres and` dropped 0 |
| 4,380 commands (27 by hand) through each tree's `walk_command`, `judgeable` and `classify`, `creation_directory` and `commit_invocations`, against bash's `pwd` on one fixture | Guard losses against `86256492` where bash is in the dirty tree: 78 / 36 / 19 at `542f920b` / target / flag. Consent answers wrong where `86256492` was right: 202 / 142 / 86. A base directory missing from the gate's set: 0 at every tree. Nothing raised |
| Yellow 1's clause on a clone: four failing-landing cases and two control cases, then the guard, guard-asks-once and no-shape modules | Without the clause: the four in-front and newline cases red. With the clause: those green, and every case in the three modules green. The plain and after-operand spellings stay silent, as at `86256492` |
| `walk_directories` on `<cap>` + `cd sub && …`, `cd /abs/Y && …`, `2>/dev/null cd sub && …`, `cd && …` at the target | A relative `cd` leaves the walk's first unresolved and the base leads. An absolute one and `cd` alone lead (white 3) |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once the rounds settle, and it is not due while yellow 1 is open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Yellow 2: behind an unresolved first directory, the consent writer reads through to a `cd` landing the `\|\|` skips, and for the redirection spellings this is a regression against `86256492` by command text. `86256492` does the same for the plain spelling | #686, beside the guard's reading of an unresolved directory | the owner, who decides whether `plan.md`'s alternative D (running shells apart from skipped ones) is worth a new interface on three consumers |

## Paste-ready fixes

### Yellow 1 — `hooks/cmdline.py#walk_directories`

```python
        # The base's directories go behind the walk's, since the worktree
        # guard and the consent writer take the first one -- and in front of
        # a walk whose FIRST directory it cannot name, or whose first is a
        # landing the base did not make and that is no directory on disk.
        # That first one is the shell the segment runs in: `_branches` puts
        # the running shells ahead of the skipped ones. Past `STATE_CAP`,
        # `cd /abs/Y || git switch` names Y behind the collapsed walk's
        # unresolved first (#689). And a `cd` read past its redirections
        # (I13) is landed in front of the as-written answer whether or not
        # it can succeed: `cd w; 2>/dev/null cd /abs/missing; git switch`
        # switches in `w`, and the landing led, so the guard found no
        # repository there and judged the session's own tree (round 1 of
        # 1790729827). Where the base names the same first directory the two
        # agree, and nothing is read from disk.
        lead = wheres[0] if wheres else None
        if (
            lead is not None
            and not isinstance(lead, Unresolved)
            and (lead in base_wheres or os.path.isdir(lead))
        ):
            ordered = wheres + base_wheres
        else:
            ordered = base_wheres + wheres
```

### Yellow 1 — `tests/test_guard_resolves_the_tree_it_judges.py`

```python
FAILED_LANDINGS = {
    "in front, then a semicolon": "2>/dev/null cd {missing}; ",
    "in front, then a newline": "2>/dev/null cd {missing}\n",
}


@pytest.mark.parametrize("capped", [False, True])
@pytest.mark.parametrize("route", sorted(FAILED_LANDINGS))
def test_a_cd_past_a_redirection_that_fails_keeps_the_tree_bash_stays_in(
    monkeypatch, capsys, repo, tmp_path, route, capped
):
    """Round 1 of 1790729827, yellow 1. A `cd` read past its redirections is
    landed in front of the as-written answer (I13). Where its destination
    does not exist, bash stays in `w` and runs the switch there, but the
    landing led, so the guard found no repository in it and judged the
    session's clean tree, and the consent writer filed the creation under
    the missing path. `86256492` did not read the `cd` and asked about `w`."""
    session = _dirty_nested_session(repo, tmp_path)
    tail = FAILED_LANDINGS[route].format(missing=tmp_path / "nosuch-either")
    chain = "cd w; " + ("2>/dev/null cd nosuch; " * 9 if capped else "") + tail
    _asks_in_w_and_files_under_w(monkeypatch, capsys, session, chain)


@pytest.mark.parametrize("capped", [False, True])
def test_a_cd_past_a_redirection_that_lands_still_leads_after_a_semicolon(
    monkeypatch, capsys, repo, tmp_path, capped
):
    """Round 1 of 1790729827. What yellow 1's fix keeps: the landing exists,
    bash switches in `O`, and the guard judges `O`."""
    session = _dirty_nested_session(repo, tmp_path)
    other = tmp_path / "O"
    shutil.copytree(repo, other)
    chain = (
        "cd w; "
        + ("2>/dev/null cd nosuch; " * 9 if capped else "")
        + f"2>/dev/null cd {other}; "
    )
    _, _, top = run(monkeypatch, capsys, chain + "git switch feature/x", session)
    assert top and os.path.samefile(top, other), top
```

### White 3 — `docs/commit-review-gate-spec.md`, the `STATE_CAP` paragraph

```markdown
the switch does not run in (#689). An absolute `cd` after the collapse makes
the walk's first directory readable again, so it leads; a relative one lands
inside the unresolved directory, and the base's thread leads. A `cd` landed
past its redirections leads where its destination is a directory, before the
cap and past it, and where it is not, the `cd` fails and the base's thread
leads (round 1 of 1790729827).
```

### Yellow 2 — the case for #686, not a fix at this layer

```python
def test_an_unresolved_first_does_not_file_a_creation_under_a_skipped_cd(tmp_path):
    """#686. The base thread names no readable directory, and the walk's
    readable one is the `cd` the `||` skips; `86256492` filed this under the
    session, and filed the plain `cd O ||` spelling under O."""
    other = tmp_path / "O"
    other.mkdir()
    command = f"eval true; 2>/dev/null cd {other} || git worktree add ../wt"
    acted = wg.worktree_consent.creation_directory(command, str(tmp_path))
    assert os.path.normpath(acted) == str(tmp_path), acted
```

Needs a fix: yes — 🟡 1 (a `cd` behind a redirection into a directory that does not exist leads, so after `;` or a newline the worktree guard is silent on the dirty tree bash stays in, before the cap and past it)
Loses a record or crashes: yes — 🟡 1: `cd w; 2>/dev/null cd <missing>; git worktree add ../wt` is answered with `<missing>`, where no repository exists, so `w`, where the creation ran, gets no record, where `86256492` filed it under `w`

## Proof block

Files opened: `hooks/cmdline.py` (`walk_directories`, `_branches`,
`_directories`, `_unplaced`, `_capped`, `_step`, `_land`, `_cd_target`,
`Unresolved`), `hooks/worktree-guard.py` (`walk_command`, `judgeable`,
`classify`, `main`'s judging loop), `hooks/worktree_consent.py`
(`creation_directory`, `main`), `hooks/commit-review-gate.py`
(`commit_invocations`, `unreadable_reason`, `main`, `already_asked`), the diff
`542f920b...69ebf6e7` over `hooks/`, `docs/`, `tests/` and `seal/ledger/`, this
item's `spec.md`, `plan.md`, `overview.md`, `phases/phase-1.md` and
`changelog.md`, `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/rounds/round-3-report.md`,
`tests/conftest.py`, `bin/test` and `.github/scripts/run_tests.py`.
