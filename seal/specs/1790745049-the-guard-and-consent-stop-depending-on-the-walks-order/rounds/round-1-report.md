# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — round 1 report

| Field | Value |
|---|---|
| Round | 1, a finding round over the whole branch |
| Target SHA | `4bc94f05` |
| Range reviewed | `542f920b...4bc94f05` |
| Bases compared against | `86256492` for the worktree guard and the consent writer; `542f920b` for the commit gate |
| Ran by | specseal:warden on claude-opus-5-5 |

Every executed row ran in a `git clone --no-local` at `4bc94f05` and in
exported `hooks/` trees of `86256492` and `542f920b`, each loaded in its own
process. The fix candidate below was applied to that clone only. The build's
account (the handoff, `overview.md`, the phase records, ledger rows M1 to M4)
was read as claims and checked against the code or by execution.

## What this round found, in the order one causes the next

**The containment works for the shapes it was built against.** Over 407
commands, every family the prompt named gives the guard's judged tree, its
decision and the consent writer's directory exactly as `86256492` gives them:
`||` and `&&` after a failing `cd`, subshells, the merged view, newlines,
`pushd`/`popd`, env prefixes, chains past the cap, and S6's unplace rule. The
commit gate's invocations and walk are identical to `542f920b`'s.

**It is not equal by construction, because the base thread shares readers
that #674 widened.** The thread walks like `86256492`, but it asks the
target's `command_word` and the guard asks the target's `parse_git`. Both
read more than the base did: past a redirection (`2>/dev/null git`, `git
2>/dev/null switch`) and past zsh's `noglob`, `nocorrect`, `repeat N` and `for
i (…)`. Two effects follow.

- **Red 1, a silence the base did not have.** The guard keeps the first
  switch-kind segment and the first creation. A segment only the wider reading
  reads as git takes the first slot, so the later segment `86256492` judged is
  never judged. With an ACTIVE session in `w`,
  `2>/dev/null git switch feature/x; cd w && git switch feature/x` is denied
  at `86256492` and silent at the target. bash then switches `w`. The prompt
  asked whether this recognition only adds asks. It does not.
- **Yellow 2, the records claim more than the code gives.** For `repeat N git
  …` and `for i (…) git …`, the target's first reading unplaces the segment,
  so `base_directories` gives it an unresolved directory where `86256492`'s
  walk gave a readable one. M1, the `base_directories` docstring and spec S3
  say every segment's directories equal the base's, and 12 commands here
  differ. The recorded list of recognition differences also names
  `2>/dev/null git switch` alone.

**Three wording items, none a defect (white 3 to 5).**

## Findings from execution

### Red 1 — a segment only #674 reads as git takes the place of the one the base judged

`hooks/worktree-guard.py:2086` (`main`'s selection loop), and the same rule in
`hooks/worktree_consent.py:437` (`creation_directory`):

```python
        found_already = creation_at if creates else switch_reason
        if found_already is not None:
            continue
```

The loop takes the first segment of each kind that classifies. `parse_git`
reads git in segments `86256492` did not, and those segments now classify.
When one stands in front of a segment the base read, it wins the first slot.
The base's segment is skipped, and the guard judges a different tree.

Executed through `main()` with the fixture the new cases use: a clean `git
init` session, a dirty copy of the `repo` fixture at `w`, a clean `clean`
beside it. The sessions stub reports one ACTIVE session whose tree is `w` and
none elsewhere.

| Command | bash | `86256492` | `542f920b` | `4bc94f05` | with the fix |
|---|---|---|---|---|---|
| `2>/dev/null git switch feature/x; cd w && git switch feature/x` | `w` ends on `feature/x` (executed) | deny | silent | silent | deny |
| `nocorrect git switch feature/x; cd w && git switch feature/x` | not run | deny | silent | silent | deny |
| `cd w && git switch feature/x` (control) | | deny | deny | deny | deny |

With no other session the same shapes lose the dirty-tree question. In the
407-command probe, 5 commands asked at `86256492` and are silent at the
target: the two above, `git 2>/dev/null switch …;`, `repeat 1 git switch …;`
and `cd clean && 2>/dev/null git switch …; cd ../w && git switch …`. The
consent writer has the same rule. For `2>/dev/null git worktree add ../wt-a;
cd w && git worktree add ../wt-b` it files under the session's clone, where
`86256492` filed under `w`.

- **Why it matters.** A deny over an active session's tree is what this guard
  exists for, and the policy puts a wrong allow above a wrong deny
  (`docs/worktree-guard-spec.md` §*Unknowns resolve conservatively*).
- **It predates this branch.** `542f920b` gives the same answers, so #674
  introduced it and 0.16.0 has not shipped it yet. The branch's claim is what
  it contradicts: M1 and the changelog fragment say the guard's answer equals
  the base's "for every one they both read as git". Here both read the second
  segment as git.
- **The fix.** A segment only the wider reading finds is held, and a later
  segment of the same kind that the base's reader finds replaces it. A
  command with no such later segment keeps the wider one, so the recognition
  still adds its asks. Executed on the clone with the fix: the 5 silences are
  gone. Every remaining difference from `86256492` is a command the base read
  no git in, plus one that tightened from ask to deny. The guard and consent
  modules pass (160 passed). The 5 planted cases below pass, and at the
  target's hooks all 5 fail.

### Yellow 2 — `base_directories` is not the base's walk for zsh-prefixed segments

`hooks/cmdline.py:2617` (`walk_directories`, the `first_unplaced` step that
`base_directories` takes):

```python
        first, first_unplaced = command_word(tokens)
        ...
        if first_unplaced:
            base_wheres = _unplaced(base_wheres)
```

`command_word`'s first reading changed in #674. `RUNNERS` gained `noglob`,
`nocorrect` and `repeat`, and a zsh short `for` now unplaces. Where a runner's
operand is not `git`, the reading takes the stand-in and unplaces. So for
`cd w && repeat 2 git switch feature/x` the segment's directory is
`Unresolved(session/w)` at the target and `session/w` at `86256492`. Executed:
12 of the 407 commands differ in the directories the guard reads, all of them
`repeat N git …` or `for i (1) git …`.

- **Effect.** At `86256492` these segments were not git, so no decision
  changes. At the target they are git, and the unplaced directory sends the
  guard to the session's tree, and the consent writer to the session's
  clone, while zsh runs them in `w`. `cd w && repeat 2 git worktree add ../wt`
  is filed under the session.
- **What is false.** M1 says "each segment's directories as they read them
  … equal `86256492`'s" without a qualifier, and so do spec S3 and the
  `base_directories` docstring ("the directories `86256492`'s walk named, and
  only those"). M1 and the handoff also give the recognition difference as
  "every one `2>/dev/null git switch feature/x`". The probe finds `git
  2>/dev/null switch`, `nocorrect`, `noglob`, `repeat` and zsh's `for` as
  well, and the consent writer filing for each of them where the base filed
  nothing.
- **Why the build's corpus missed it.** Its generator carried no zsh prefix,
  so the 0 over 326,368 segments is a fact about that corpus.
- **The fix asked for is the record.** Code that reproduces the base's
  flag exactly would need the base's `RUNNERS` beside the current one, which
  is the vendored second walk plan alternative B rejected. The corrected
  sentences are below. Whether the guard should instead place these segments,
  as S6 does for the redirection family, is a question for the owner.

### White 3 — the policy says the guard reads `git -C` the way the base did

`docs/worktree-guard-spec.md:559`. "Both are read the way the release base
`86256492` read them" covers `git -C <path>` and the `cd`. The `cd` is the
base's. `-C` is read by the target's `parse_git`, which reads past a
redirection before it (`git 2>/dev/null -C O switch x`). This was read, not
run. It is a sentence and no behaviour.

### White 4 — the changelog calls the accepted cost something it gives back

`seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20`
opens the cost paragraph with "What this gives back". The cost is what the
guard gives up, so a reader can take it for a gain. This is the run's own
paperwork, so it is a correction.

### White 5 — S6 places a segment that the same words without the redirection leave unplaced

`hooks/cmdline.py:2617`. `cd w && nice -n 5 git switch feature/x` is unplaced
by the first reading at both SHAs, so the guard judges the session's tree.
`cd w && 2>/dev/null nice -n 5 git switch feature/x` is placed in `w` (M3).
bash runs both in `w`. So S6's answer is the right tree. M3's grounds call the
as-written flag "the one consistent with the base's walk", but the base
unplaced the plain form. Nothing needs to change in the code.

### What was checked and holds

- **The gate is unchanged (acceptance 2).** `hooks/commit-review-gate.py` is
  not in the diff. `walk_directories` with `base=False` computes what it did:
  the one split `if` is two unplacings of a tuple `_unplaced` leaves
  unchanged the second time. Executed: for the 407 commands with their tails
  made commits, `commit_invocations` and the walk equal `542f920b`'s in every
  one. The 5,092-command reason-text comparison was not repeated; this row
  rests on the unchanged gate code and the equal invocations.
- **No other consumer (acceptance 3).** Read with `git grep` over the tracked
  tree. The readers are `commit_invocations`, the guard's `walk_command` (its
  `main` and `only_creates_a_worktree`) and `creation_directory`. The
  enumeration in `phases/phase-1.md` is complete.
  `hooks/implementer-notice.py` imports `parse_git` and not the walk.
- **The changed case (acceptance 4).**
  `test_a_cd_behind_a_redirection_leaves_the_guard_on_the_tree_the_base_judged`
  keeps the same three spellings and flips each assertion to the base's
  answer. It drops only what M2 records. The gate's I13 cases are untouched
  and pass.
- **I's records (acceptance 5).** I13 is corrected, I's changelog no longer
  says the guard judges W, and I14 and I15 describe the gate's reading. No
  tracked sentence left says the guard or consent takes W.

## Regression tests to plant

In `tests/test_guard_resolves_the_tree_it_judges.py`, the five cases in the
Red 1 fence below. Seen red: at `4bc94f05`'s hooks all 5 fail, and with the
fix all 5 pass.

## Facts for the evidence ledger

- Red 1's selection rule, once fixed: the guard and the consent writer judge
  the first segment of a kind that `86256492`'s reader reads as git, and a
  segment only #674's reading finds only where none follows. That becomes a
  new row in this item's fragment, anchored on the new unit and the planted
  cases.
- M1's claim, corrected as in the Yellow 2 fence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A segment only #674's reading reads as git takes the first-of-kind slot, so the later segment `86256492` judged is skipped: deny over an ACTIVE session in `w` becomes silence, and consent files under another clone | `hooks/worktree-guard.py:2086`, `hooks/worktree_consent.py:437` | open | Executed through `main()` and bash; predates the branch (`542f920b` agrees) and contradicts M1 and the changelog's "for every one they both read as git" |
| 🟡 2 | `base_directories` unplaces `repeat N git …` and `for i (…) git …` where `86256492`'s walk placed them; M1, spec S3 and the docstring claim equality for every segment, and the recognition list names one shape of five | `hooks/cmdline.py:2617` | open | Executed: 12 of 407 commands differ in the guard's directories |
| ⬜ 3 | The guard policy says `git -C` is read the base's way; `parse_git` reads it past a redirection | `docs/worktree-guard-spec.md:559` | open | Read |
| ⬜ 4 | The changelog opens the accepted cost with "What this gives back" | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | open | A correction to the run's paperwork |
| ⬜ 5 | M3's grounds call the as-written flag the base-consistent one, while the base unplaced `nice -n 5 git switch` without the redirection | `hooks/cmdline.py:2617` | open | Read; S6's answer is the tree bash runs in |
| 🟢 | The commit gate's invocations and walk equal `542f920b`'s | `hooks/cmdline.py#walk_directories` | confirmed | Executed over 407 commands; the gate file is not in the diff |
| 🟢 | The consumers of the walk are the three the build enumerated | `hooks/` | confirmed | Read with `git grep` |
| 🟢 | The changed I13 guard case loses only what M2 records | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | Read; the module passes |
| 🟢 | `\|\|`, `&&`, subshells, merged view, newlines, `pushd`/`popd`, env prefixes, the cap and S6 give the base's tree | `hooks/cmdline.py#base_directories` | confirmed | Executed: 0 differences outside the recognition family |
| ❓ | The guard's Windows backslash doubling through `base_directories` | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | No Windows runner here; the repository owner answers it on a Windows machine |

## Executed probes

| What was run | Result |
|---|---|
| Differential over 407 commands (82 heads × 5 tails, plus 12 recognition shapes), each hook set in its own process: `walk_command`, `creation_directory`, `main()` with sessions stubbed | Target against `86256492`: 12 directory, 12 consent and 71 decision differences. 113 are commands `86256492` read no git in; 5 are asks that became silent (Red 1) |
| The same, target against `542f920b` for the gate: `commit_invocations` and `walk_directories` | 0 of 407 differ |
| ACTIVE session in `w`, three commands through `main()` at three hook sets; bash running the first on a fixture copy | `86256492` deny ×3; `542f920b` and target silent, silent, deny; bash exit 0, `w` on `feature/x` |
| Fix candidate on the clone: the differential again, the ACTIVE probe, and `bin/test` on the guard-tree, no-shape and asks-once modules | 0 asks became silent; deny ×3; 160 passed |
| The 5 planted cases, `bin/test … -k`, with the fix and at the target's hooks | 5 passed; 5 failed |
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py tests/test_no_shape_the_base_stops_reads_silent.py` at the target | 85 passed, exit 0 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch; the sealer's spawn, after the rounds settle |

### The fixture the probes shared

```text
session/        git init, no commits (clean)
session/w/      copy of a one-commit repo with branch feature/x; f.txt modified
session/clean/  the same copy, unmodified
O/              the same copy, outside the session
nosuch-either   never created
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should place a zsh-prefixed segment rather than unplace it (Yellow 2) | the owner's 0.17.0 redesign of how the gates learn where a command acts | the repository owner |

## Paste-ready fixes

### Red 1 — `hooks/cmdline.py`, after `base_directories`

```python
# The words in front of a command word that `86256492` did not read past and
# #674 does: zsh's three runners and its short `for`.
_WIDER_PREFIXES = frozenset({"noglob", "nocorrect", "repeat", "for", "foreach"})


def read_as_git_as_written(tokens):
    """True where `86256492`'s reader found a git invocation in TOKENS (#689).

    `parse_git` also finds one behind a redirection (`2>/dev/null git`, `git
    2>/dev/null switch`) and behind zsh's runners (#674). The worktree guard
    and the consent writer take the FIRST segment of a kind, so a segment only
    that wider reading finds must not take the place of a later one the base
    judged: `2>/dev/null git switch x; cd w && git switch y` was denied over an
    active session in `w` at `86256492` and silent at `542f920b`.
    """
    word, _unplaced = command_word(tokens)
    if not word or os.path.basename(word[0]) != "git":
        return False
    front = tokens[: len(tokens) - len(word)]
    if any(os.path.basename(t) in _WIDER_PREFIXES for t in front):
        return False
    rest = word[1:]
    at, _chdirs = _git_options(rest)
    return not redirection_width(rest, at)
```

### Red 1 — `hooks/worktree-guard.py`, `main`'s selection loop

```python
    switch_reason = None
    switch_at = cwd
    creation_at = None
    # A kind found only by the reading #674 added (`2>/dev/null git switch`)
    # is held until a segment `86256492` read as git is found, and that one
    # takes its place (#689): the base judged the later segment.
    switch_wider = creation_wider = False
    for tokens, wheres in walk_command(command, cwd):
        creates = cmdline.adds_a_worktree(tokens)
        # Nothing left to learn from a segment of a kind already found.
        # Skipping keeps the question cheap -- `classify` runs `git rev-parse`
        # for a `checkout`, so a command is now classified up to its first
        # switch-kind segment rather than up to its first verdict of any kind.
        found_already = creation_at if creates else switch_reason
        held = creation_wider if creates else switch_wider
        wider = not cmdline.read_as_git_as_written(tokens)
        if found_already is not None and (wider or not held):
            continue
        for where in wheres:
            here, target = judgeable(tokens, where, cwd)
            found = classify(tokens, here)
            if not found:
                continue
            if creates:
                creation_at, creation_wider = target, wider
            else:
                switch_reason, switch_at, switch_wider = found, target, wider
            break
        if (
            switch_reason is not None
            and creation_at is not None
            and not (switch_wider or creation_wider)
        ):
            break
```

### Red 1 — `hooks/worktree_consent.py`, `creation_directory`'s loop

```python
    held = ""
    for tokens, wheres in cmdline.base_directories(items, cwd):
        if not cmdline.adds_a_worktree(tokens):
            continue
        here = cwd
        for where in wheres:
            if not isinstance(where, cmdline.Unresolved):
                here = where
                break
        at = cmdline.apply_chdir(here, cmdline.parse_git(tokens)[2])
        # A creation only #674's reading finds waits for one `86256492`
        # read, which the base filed (#689), as the guard's walk does.
        if cmdline.read_as_git_as_written(tokens):
            return at
        held = held or at
    return held
```

### Red 1 — the cases, appended to `tests/test_guard_resolves_the_tree_it_judges.py`

```python
# A segment only #674's reading reads as git, in FRONT of one `86256492` read.
# The guard takes the first segment of each kind, so the wider one took the
# place of the one the base judged.
WIDER_FIRST = (
    "2>/dev/null git switch feature/x; cd w && git switch feature/x",
    "git 2>/dev/null switch feature/x; cd w && git switch feature/x",
    "nocorrect git switch feature/x; cd w && git switch feature/x",
    "repeat 1 git switch feature/x; cd w && git switch feature/x",
)


@pytest.mark.parametrize("command", WIDER_FIRST)
def test_a_segment_only_the_wider_reading_finds_does_not_take_the_base_judged_ones_place(
    monkeypatch, capsys, repo, tmp_path, command
):
    """#689. An ACTIVE session sits in `w`, and bash switches `w` (executed).
    `86256492` denied each command; `542f920b` judged the first segment in the
    session's clean tree and was silent."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    active = [(111, str(session / "w"), 1.0, 0.5, "VS Code")]
    decision, reason, top = run(
        monkeypatch, capsys, command, session, sessions=(active, [], True)
    )
    assert decision == "deny", (command, decision, reason)
    assert top and os.path.samefile(top, session / "w"), (command, top)


def test_the_consent_writer_files_the_creation_the_base_filed_behind_a_wider_one(
    repo, tmp_path
):
    """#689, the consent twin. `86256492` filed under `w`."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null git worktree add ../wt-a; cd w && git worktree add ../wt-b",
        str(session),
    )
    assert os.path.normpath(acted) == str(session / "w"), acted
```

The `run` helper's stub answers ACTIVE for any tree, so the `top` assertion
is what turns these red at the target. A tree-aware stub would pin the
silence itself.

### Yellow 2 — M1's claim cell, the clause after the semicolon

```text
so each segment's directories as they read them equal `86256492`'s wherever
the target's as-written reading of the command word unplaces what the base's
did (it also unplaces a runner's operand behind zsh's `noglob`, `nocorrect`
and `repeat`, and a zsh short `for`, segments the base read no git in); the
consent writer's filed directory and the guard's judged tree equal
`86256492`'s wherever `86256492` read the command's first segment of that
kind as git
```

### Yellow 2 — the `base_directories` docstring's first line, and spec S3

```text
"""[(tokens, wheres)] — the directories `86256492`'s walk named, for every segment the base read a command word in the same place.
```

```text
| S3 base equality | Over a generated corpus, every segment's directories as the guard reads them equal `86256492`'s except a zsh-prefixed segment the base read no git in; the guard's judged tree and consent's filed directory equal `86256492`'s hooks wherever the base read the segment of that kind as git | … |
```

Needs a fix: yes — 🔴 1, a segment only #674 reads as git displaces the one the base judged; 🟡 2, the records' unqualified equality claim
Loses a record or crashes: no

## Proof — files opened

- `hooks/cmdline.py` (`base_directories`, `walk_directories`, `command_word`, `understood`, and the unit-level diff against `86256492`)
- `hooks/worktree-guard.py` (`walk_command`, `only_creates_a_worktree`, `judgeable`, `classify`, `main`)
- `hooks/worktree_consent.py` (`consent_path`, `creation_directory`)
- `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/conftest.py`
- `docs/worktree-guard-spec.md`, `docs/commit-review-gate-spec.md` (the changed paragraphs)
- this work item's `routing.md`, `spec.md`, `plan.md`, `overview.md`, `survivors.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`
- `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md`; I13, I14 and I15 in `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`; that work item's `changelog.md` and `rounds/round-3-report.md`
