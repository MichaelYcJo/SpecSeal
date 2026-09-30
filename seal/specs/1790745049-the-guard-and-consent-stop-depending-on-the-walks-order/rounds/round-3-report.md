# 1790745049 — review round 3 report

Round 3 is verifying and last. It targets `28199afc` over round 2's fix range
`00ed11be..9f5261c5` (three commits: `53d30647`, `615f1bf5`, `9f5261c5`), with
`28199afc` closing `rounds/round-2.md`. The base is `542f920b`, and the guard
and consent reference is `86256492`.

## In short

Every verdict round 2 closed is closed. The fix range opened nothing that needs
a fix, and nothing in it loses a record or crashes.

1. The policy no longer names a release, and the hygiene module passes. This
   was round 2's blocking finding.
2. The four smaller corrections hold. The reference points at the section that
   holds the groups, and the five cost lists name `foreach`. S6 is split per
   reader, and each row is red under a mutant of its own. The four test
   sentences name the reader each module imports.
3. The corrections the fix pass made to two other unshipped specs, and I9's
   re-read, are true against the tree.
4. The containment still holds. The frozen copy equals `86256492`'s reader, and
   the gate's two files equal `542f920b`'s. Over 784 generated commands the
   guard and the consent writer answer exactly as `86256492` does.

Two ⬜ findings are in the same class as round 2's ⬜ 3 and ⬜ 5, just outside
the fix range. Neither changes behaviour, and neither counts toward
`Needs a fix`.

## Round 2's verdicts, answered

### The policy no longer names the next release (round 2's blocking finding)

The fix range's policy text claimed the blocking finding was gone. The code
agrees. `docs/worktree-guard-spec.md` now reads *"#692, the redesign of how the
gates learn where a command acts"*, and the changelog fragment uses the same
words. A `git grep` for `0.16`–`0.19` versions over the loaded roots the case
scans (`skills`, `agents`, `docs`, `templates`, both READMEs,
`CONTRIBUTING.md`, the two install scripts) finds nothing. **Executed**:
`tests/test_release_hygiene.py` passed inside the 23-module run below, which
exited 0.

`0.17.0` survives in `hooks/cmdline_base.py:12`, the rider, and in the work
item's own `overview.md`, `plan.md`, `spec.md` and `routing.md`. None of these
is a loaded root, and the rider goes when #692 deletes the module. Read.

### The reference names §*Creation consent* (round 2's ⬜ 2)

The cost paragraph at `docs/worktree-guard-spec.md:583` now cites §*Creation
consent*'s command-word groups. The groups sit at line 262 onward, under the
heading at line 88 (`## Creation consent — the first creation is the question,
not every one`), which runs to line 373. **Read.**

### `foreach` is in every cost list, and the new row pins it (round 2's ⬜ 3)

The five lists that state the guard's cost all name `foreach i (…)`:
`docs/worktree-guard-spec.md:280` and `:582`, the changelog fragment, M2 and
spec S5. **Read**, and a `git grep` for `repeat N` / `nocorrect` found no
sixth cost list.

The new `ZSH_PREFIXED` row is a real pin. **Executed**:

- With `542f920b`'s hooks over this tree, all five `ZSH_PREFIXED` rows fail,
  the `foreach` row included.
- With `86256492`'s hooks the five pass, and at the target they pass inside the
  module run.
- zsh 5.9 runs the row's shape: `zsh -f -c 'foreach i (1) echo ran-$i; end'`
  printed `ran-1` and exited 0.

### S6 breaks each reader alone, and each row catches its own mutant (round 2's ⬜ 4)

The fix range claimed each row pins "no gate that does not import it". That
holds. **Executed**: a deleted probe replayed the three rows' scenario (the
`pre-bash` and `post-bash` dispatch and `stop`) on a copied `hooks/`, under
seven mutants of the importing gates:

| Mutant | `cmdline` row | `cmdline_base` row | `both` row |
|---|---|---|---|
| none | holds | holds | holds |
| the guard imports `cmdline` again | **red** (guard named) | holds (guard still named through `hooks/worktree_consent.py`) | holds |
| the consent writer imports `cmdline` again | **red** | **red** | holds |
| the commit gate's import of the consent writer unguarded | holds | **red** (gate named) | holds |
| `mode-gate.py` imports `cmdline` | **red** | holds | **red** |
| `session-lease.py` imports `hooks/cmdline_base.py` | holds | **red** | **red** |
| the notice's or the consent writer's import guarded | holds | holds | holds (each still fails at run) |

Each row is therefore red under at least one mutant of its own. The docstring's
claim that the commit gate's import of the consent writer is guarded matches
`hooks/commit-review-gate.py:127-130`. **Read.**

### The import sentences name the reader each module imports (round 2's ⬜ 5)

The three test modules now say *"the plain name the commit gate imports"*. The
docstring in `tests/test_what_the_reader_understands.py` now says
`import cmdline_base as cmdline`, which is `hooks/worktree-guard.py:130`.
**Read.** The same class continues into a hook file; see ⬜ 1.

## The corrections to other records

- **1790635415's fact table.** The claim is that `cmdline.py` is now imported by
  the commit gate and `implementer-notice.py` alone. That matches the tree:
  `import cmdline` / `from cmdline` appears only in `hooks/commit-review-gate.py:101`
  and `hooks/implementer-notice.py:47`. The guard and the consent writer import
  `hooks/cmdline_base.py`. **Read**, and the mutant table above confirms it
  through dispatch.
- **1790635415's S6.** The correction names the three partitions. The mutant
  table executes each one. **Executed.**
- **1790660768's grounding row and §*What the worktree guard sees*.** The note
  says none of the section's three bullets holds for the guard any more. Each
  bullet describes a reading only `hooks/cmdline.py` has: a redirected git
  classified, the consent writer recording it, and W1's `Unresolved` reaching
  the guard. The frozen reader has none of them, and the differential below
  shows the guard answering as `86256492`. **Read**, and executed through the
  differential.
- **I9's re-read.** The note says the section's list of zsh words gained
  `foreach i (…)` and nothing else. The fix range's only hunk in
  §*Creation consent* is that one, at line 280. The new anchor hash `850cb483`
  resolves (`bin/evidence-check`, 0 drifted). **Read and executed.**
- **The survivor row.** `bin/survivor-check --range 00ed11be..9f5261c5` found
  one survivor, the S6 sentence in 1790635415's spec, and the work item's
  `survivors.md` excuses it. **Executed.**

## The containment, re-confirmed

- **The frozen copy.** The shebang plus lines 20 onward of
  `hooks/cmdline_base.py` equal `git show 86256492:hooks/cmdline.py` byte for
  byte (2,267 lines). Lines 2–19 are all comments. **Executed.**
- **The gate.** `git diff 542f920b 28199afc -- hooks/cmdline.py
  hooks/commit-review-gate.py` is 0 bytes. Across `hooks/` only
  `hooks/cmdline_base.py`, `hooks/worktree-guard.py` and
  `hooks/worktree_consent.py` differ from the base. **Executed.**
- **The decisions.** A deleted probe generated 784 commands: 14 heads (`cd`
  with and without redirections, a subshell, a failing `cd`, a wider segment
  first) × 14 git spellings (redirections, the four zsh words and `foreach`,
  runners, a path) × 4 verbs. Each hook set ran in its own process, using the
  guard's `main()` with a unique session id per command and a
  `sessions_in_tree` stub that reports a session active in `w` alone, plus
  `creation_directory` for consent. **Executed**:
  - Target against `86256492`: 0 differences in decision, reason text, judged
    tree or consent directory, and no exceptions on either side. The target
    gave 642 silent, 113 deny and 29 ask, and consent filed 84.
  - The same probe with `542f920b`'s hooks differs from `86256492` on 317
    commands, all in the redirection, zsh-word and redirected-`cd` families
    (30 of them `foreach`). So the probe can see the difference it rules out.

## Findings

### ⬜ 1 — The commit gate still says both gates import `hooks/cmdline.py`

`hooks/commit-review-gate.py:92-93` reads *"`hooks/cmdline.py` owns it and
both gates import it by plain name"*. Since #689 the guard imports
`hooks/cmdline_base.py`. The file is frozen at `542f920b` on purpose (M4). The
overview's divergence row and the rider in `hooks/cmdline_base.py` both say the
frozen comments describe `542f920b` and that #692 reconciles them. Both, though,
name only *"comments in `cmdline.py`"*, so nothing records that this comment is
stale too. This is the class of round 2's ⬜ 5, one directory over. It is
**read** only, and nothing executes the sentence. The fix is the rider's
sentence, which the byte-identity below it does not cover.

### ⬜ 2 — The gate's policy list of zsh words omits `foreach`, which the gate reads

`docs/commit-review-gate-spec.md:392-394` lists *"`noglob`, `nocorrect`,
`repeat N` and `for i (…) cmd`"* as read past. `hooks/cmdline.py:1563` treats
`foreach` exactly as `for` (`toks[i] in ("for", "foreach")`). Line 371 and I12
in 1790660768's ledger fragment list the same words without `foreach`. This is
the gate's list and not the guard's cost, and it stands at `542f920b`, from
work item 1790660768, which ships in the same release. The list is
incomplete, and nothing in it is false. **Read**: the gate's answer on a
`foreach` commit was not executed this round; round 2 executed the guard's.

### ❓ Windows, carried

This is carried from rounds 1 and 2 unchanged. `hooks/cmdline_base.py` is
`86256492`'s splitter byte for byte, and no Windows shell was run.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's blocking finding is closed — the policy names no release, and the hygiene case passes | `docs/worktree-guard-spec.md#"### Which tree, when the command walks to it"` | confirmed | Executed: `tests/test_release_hygiene.py` in a 23-module run, exit 0; `git grep` over the loaded roots finds no `0.16`–`0.19` version |
| 🟢 | round 2's ⬜ 2 is closed — the cost paragraph cites §*Creation consent*, which holds the command-word groups | `docs/worktree-guard-spec.md:583` | confirmed | Read: the groups at line 262 sit under the heading at line 88 |
| 🟢 | round 2's ⬜ 3 is closed — the five cost lists name `foreach`, and its `ZSH_PREFIXED` row pins it | `tests/test_guard_resolves_the_tree_it_judges.py#ZSH_PREFIXED` | confirmed | Executed: the five rows red at `542f920b`'s hooks, green at `86256492`'s and the target's; zsh 5.9 ran the shape |
| 🟢 | round 2's ⬜ 4 is closed — S6 is parametrised per reader, and each row is red under a mutant of its own | `tests/test_a_gate_that_fails_says_so.py#test_a_broken_shared_module_names_every_gate_that_imports_it` | confirmed | Executed: seven mutants on a copied `hooks/`; see the table in the findings |
| 🟢 | round 2's ⬜ 5 is closed — the four test sentences name the reader each module imports | `tests/test_what_the_reader_understands.py#test_the_guard_reads_the_same_answer` | confirmed | Read against `hooks/worktree-guard.py:130` |
| 🟢 | The corrections to 1790635415's S6 and fact table and to 1790660768's grounding and §*What the worktree guard sees* are true | `seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md` | confirmed | Read the import lines of `hooks/`; executed through the S6 mutants and the differential |
| 🟢 | I9's re-read is true — the section's only change in the fix range is the `foreach` word | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | confirmed | Read the fix range's diff; `bin/evidence-check` 0 drifted, 0 broken |
| 🟢 | The frozen copy equals `86256492:hooks/cmdline.py` below its rider | `hooks/cmdline_base.py` | confirmed | Executed, byte comparison |
| 🟢 | The commit gate's two files equal `542f920b` | `hooks/commit-review-gate.py` | confirmed | Executed: empty diff |
| 🟢 | The guard's and the consent writer's answers equal `86256492`'s | `hooks/worktree-guard.py#main` | confirmed | Executed: 0 of 784 commands differ; the same probe finds 317 at `542f920b` |
| ⬜ 1 | The commit gate's comment says both gates import `hooks/cmdline.py`, and the rider that marks frozen comments as `542f920b`'s names only `cmdline.py`'s | `hooks/commit-review-gate.py:93` | deferred #692 | Read; the class of round 2's ⬜ 5; no behaviour depends on it |
| ⬜ 2 | The gate's policy lists zsh's words without `foreach`, which `hooks/cmdline.py` reads as it reads `for` | `docs/commit-review-gate-spec.md:392` | deferred #692 | Read; present at `542f920b`, from work item 1790660768; incomplete, not false |
| ❓ | The guard's Windows backslash doubling on a Windows machine | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | Carried from rounds 1 and 2; the repository owner answers it on a Windows machine |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over 23 modules: release hygiene, the record modules (generated, floor and depth, reviewer's report, fixes close, last round's fixes, reopening), the document checks (evidence, content anchors, line wrap, no real identifiers, one word, survivors, merge corrections, old roots, rule owners, riders) and the six test modules the fix range touched | 1986 passed, 1 skipped, exit 0 |
| `bin/evidence-check` | exit 0; every ledger file 0 drifted, 0 broken; the work item's fragment 14 ok |
| `bin/correction-check --range 542f920b...28199afc` | no merge commit in the range, exit 0 |
| `bin/survivor-check --range 00ed11be..9f5261c5 --exempt` the work item's `survivors.md` | exit 0; one survivor, excused |
| The frozen copy against `git show 86256492:hooks/cmdline.py`, as bytes | Equal: the shebang plus lines 20 onward |
| `git diff 542f920b 28199afc -- hooks/cmdline.py hooks/commit-review-gate.py` | 0 bytes |
| A deleted differential over 784 generated commands, each hook set in its own process | Target against `86256492`: 0 differences, 0 exceptions. `542f920b` against `86256492`: 317 differences |
| The five `ZSH_PREFIXED` rows at `542f920b`'s and at `86256492`'s hooks | 5 failed, exit 1; 5 passed |
| A deleted probe replaying S6's three rows under seven import mutants | Each row red under at least one mutant of its own |
| `zsh -f -c 'foreach i (1) echo ran-$i; end'` | `ran-1`, exit 0 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch. With nothing open that needs a fix, it comes due now, through the sealer's spawn |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should read zsh-prefixed and redirected segments rather than leave them to the user's settings | already deferred in round 1 to #692, the owner's redesign of how the gates learn where a command acts | the repository owner |

## Paste-ready fixes

⬜ 1, the rider's last two sentence lines in `hooks/cmdline_base.py`
(lines 17–18). The lines below the rider are untouched:

```text
# Comments in `cmdline.py` that name the guard or the consent writer as its
# readers describe `542f920b`, and so does the comment above the commit gate's
# imports that says both gates import `cmdline.py`; #692 reconciles them.
```

⬜ 2, `docs/commit-review-gate-spec.md:392-394`:

```text
- **zsh's precommand words and short loops** — `noglob`, `nocorrect`, `repeat
  N`, `for i (…) cmd` and `foreach i (…) cmd; end` — are read past as runners,
  the count and the word list as operands.
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round, all at `28199afc` unless named:

- `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/rounds/round-2.md`, `rounds/round-2-report.md` (lines 100–118), `overview.md` (lines 20–40)
- the fix range's diff `00ed11be..9f5261c5`, whole
- `docs/worktree-guard-spec.md` (lines 262–292, 550–595, the heading list)
- `docs/commit-review-gate-spec.md` (lines 360–400)
- `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` §*What the worktree guard sees*, and its `changelog.md` (lines 15–40)
- `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md` E13; `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` I2, I13
- `hooks/cmdline_base.py` (lines 1–20, and whole by byte comparison), `hooks/cmdline.py` (lines 1545–1580), `hooks/commit-review-gate.py` (lines 86–132), `hooks/worktree-guard.py` (lines 126–140, 740–760, 905–925, 1504–1530), `hooks/worktree_consent.py` (lines 90–96), `hooks/implementer-notice.py` (lines 44–48), `hooks/dispatch.py` (the groups)
- `tests/test_guard_resolves_the_tree_it_judges.py` (lines 1–140, 735–900), `tests/test_a_gate_that_fails_says_so.py` (lines 1–110, 200–350), `tests/conftest.py` (the loader, the environment and the `repo` fixture), `tests/test_release_hygiene.py` (lines 40–60)
- `bin/test`
