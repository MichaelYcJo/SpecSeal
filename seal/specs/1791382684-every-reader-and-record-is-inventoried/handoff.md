# 0.21.0 — handoff after the first builds

Written 2026-10-08 (evening, KST) by the orchestrating session, for a session
on another machine. Every branch below is pushed. Nothing here depends on the
old machine's worktrees, memory or scratch files. Each open work item also
carries its own `seal/specs/<id>/handoff.md` on its branch, and that file says
what its next step is.

## Where the run stands

Six of the eleven work items are squashed into `release/v0.21.0`. Four are in
the review chain, and one has not started.

| Issue(s) | Work item | PR | State | Next step |
|---|---|---|---|---|
| #858 | 1791384161 | #875 | **merged** 9b644676 | — |
| #864 | 1791384162 | #876 | **merged** d712a632 | — |
| #837 | 1791384154 | #879 | **merged** 279a580b | — |
| #867 | 1791384156 | #882 | **merged** 56ade5c8 | — |
| #869, #852, #853 | 1791384158 | #880 | **merged** b6c81a83 | — |
| #860, #805 | 1791384160 | #878 | **merged** ad447367, after a reframe at round 3 | — |
| #836 | 1791384153 | #887 (draft) | round 2 recorded at da1a0cd3: 🟡 1, 🟡 2, `Fix of a fix: first`, one reopening left | **on hold** — see §*Review of the run*; do not spawn the fix pass until the owner decides |
| #870, #848 | 1791384159 | #889 (draft) | round 1 recorded at 8b0d4d7a: 🟡 1–3 | **on hold** — see §*Review of the run* |
| #868, #856 | 1791384157 | #881 (draft, `chain: reframed`) | reframed after round 3; the redesign's round 5 closed at 11b6ed14 (2 fixed, 2 answered) | **on hold** — see §*Review of the run*; the next record would be round 6, which ends the run |
| #866 | 1791384155 | none yet | phases 1–4 closed; phase 5 stopped mid-edit and committed as an unverified `wip:` | finish phase 5 (or revert the wip), build 6–7, then the draft PR and round 1 — its branch's `handoff.md` |
| #835 | 1791384152 | none | framed; not started | builds **last**, after #836, #870, #866, #868 land |
| #834 (its own build) | 1791382684 | none | the inventory only | after #835 |

`release/v0.21.0` is at ad447367. Not framed for 0.21.0: #844 (a docstring
reflow) and #857 (the stamp's mark waits on the owner's design; it is still
in the milestone).

## Decisions the owner made (2026-10-08)

- The seven handoff questions were all answered at their defaults, except
  that #856 is (c), confirmed. All eleven items ship in 0.21.0.
- **"나머지 전부다 동시진행해 최초 세팅대로 automation"**: run everything
  concurrently under the original `automation` answer, with no mid-run
  questions.
- **The owner's go-ahead (“진행해”) covers squash-merging a sealed PR into
  `release/v0.21.0`.**
- **#868's `questions.md` P1 is built on its default (yes) and is not yet
  answered by the owner.** The reframe widened #856's rule from "a git word"
  to every word of every segment. The over-stop is 42 of 33,287 recorded
  pairs, one of them git. If the owner says no, the frame reopens.

## Review of the run (2026-10-08, the owner and the orchestrating session)

0.21.0's theme was to break the guess → record → re-tag loop: #834's inventory
gives every reader one of three fates, which are observe, force a format, or
delete. The owner read the run against that theme and judged that much of the
open work patches over the problem and makes new ones. **The three open chains
below are on hold until the owner decides their direction.** Every finding
round so far has found the next case of the same class, and another fix pass
would add one more layer of the same patch.

### The six merged items keep to the theme

- #860 reads what git computes (`git log --ancestry-path --no-merges`).
  The frame only went wrong in the prose describing it. The reframe stated the
  rule once and pinned the shapes as tests.
- #869 replaced reading pytest's printed text with a record pytest's own hooks
  write. That is a guess turned into an observation.
- #867 merged several readers into one and held the heading rule to
  CommonMark.
- #858, #864 and #837 add no guessing reader.

### The three open chains each predict a foreign tool, and patch the prediction

| Item | What it does now | Why it is a patch | The observation-based direction to weigh |
|---|---|---|---|
| #868 (#856's braces) | reads a segment's raw text with quoted spans neutralised and stops on anything brace-like | still imitates bash. Six rounds, one reframe; the stop rule costs 42 of 33,287 recorded pairs | observe the act instead of predicting the command: git's `reference-transaction` hook sees HEAD move whatever spelled the command. This is #692's own conclusion ("shell prediction does not converge") |
| #870 | a string, comment and bracket lexer for nine language families | every family has its own exceptions; round 1 found three more of the same class | force a format: bound units only where a real parser exists (`.py`), and require a quoted-line anchor everywhere else |
| #836 (the collection half) | reads a test file statically to decide whether pytest would collect and could fail the test | each round finds another `skip`/`xfail` spelling | observe: #869's pytest recorder already writes a line per test that ran in the sealed run. Whether a cited test ran is in that record |

The other half of #836, a ledger row naming the test that holds its claim, is
not a prediction. It can stand apart from the collection half.

### The ledger's re-read cost is structural

This run wrote **360 `Re-read ·` rows against 55 `Corrected ·` rows**, across
the nine fragments (counted at the release branch and the open branches).
Most of the 55 record a change the branch made on purpose, not a stale claim
that re-reading caught. So almost all re-reading confirmed and changed
nothing. The release branch holds 2,347 released rows, and the cost recurs on
every edit to a cited unit. Siblings editing the same unit doubled it: four
PRs sealed against one base left 33 drifted rows nobody read.

Test rows (#836) and a bulk migration of #836 Q1's (c) would lower the cost
inside the hash ledger's premise without questioning that premise. Whether a
row of claim plus hash is the right record at all is the question to open, in
0.22.0 or later.

### Derived prose was where most findings sat

After round 1, #860's findings were all about sentences restating its rule
more widely than the code. Each closed by deleting the sentence. "One owner
per rule" holds in `docs/` and breaks in docstrings, changelog fragments and
ledger claims. The word-list guard #860 added is itself a patch, and its
docstring says so.

### The run's own mechanics were patched by hand

- **No rule says which plugin version governs a run.** When #837 landed, the
  tree's `round-record` and the installed 0.20.0 one disagreed, and the run
  went on with the installed copy by hand.
- **A smith's hand-back checks lived only in prompts.** The eight guard
  modules, `survivor-check` and `correction-check` were not in one command.
  Five of seven first PRs went red on CI over this.
- **Landing order and re-seals were a scratch script and memory.**

The fix for these is one hand-back command and a pinned plugin version per
run, not longer prompts.

### What the owner decides next

1. For #868, #870 and #836's collection half, choose one:
   - reframe against the observation-based direction above inside 0.21.0;
   - or drop them from 0.21.0.
2. Whether 0.21.0 ships as the six merged items plus #866, #835 and #834's
   build.
3. #836 Q1. The owner leaned towards (c), a tool-assisted bulk migration,
   after seeing the 360/55 count. The timing is open: release preparation or
   0.22.0. Weigh it against the ledger-premise question above.

## How a chain is run, as this run learned it

Each step below cost a red CI run, a reopened round or a reframe before it was
written down.

1. **Records are written with the installed generator**, not the tree's.
   #837's `round_record.py` refuses ⬜ rows in a fix table and is now in the
   release branch. The run is governed by the installed 0.20.0 rules:
   `python3 ~/.claude/plugins/cache/specseal/specseal/0.20.0/skills/code-review/scripts/round_record.py {new|close} … --root .`
   Every ⬜ still takes a row (`answered` with grounds, or `corrected at`).
2. **Before landing a sealed PR, check whether the release branch moved since
   its seal.** If it did:
   1. `git merge` it in (never rebase);
   2. read the drifted ledger rows again (`evidence-check .`);
   3. run `correction-check` and `broad-gate --preflight`;
   4. seal again.

   Four PRs sealed against one base and landed in sequence left the release
   branch with 33 drifted rows. #836's branch clears them (`overview.md`
   §*The release branch's integration drift, cleared here*), so **land #836
   before #870 and #866**.
3. **Landing script** (re-create it; it lived in the old scratch dir): wait on
   `gh pr checks --watch`, stop on any non-SUCCESS, `gh pr ready`, wait for
   the re-run, then
   `gh pr merge <n> --squash --match-head-commit <full sha>`, and read
   `state` and `mergeCommit` back.
4. **Every smith spawn prompt names:**
   - the ledger fragment's full file name,
     `seal/ledger/<id>-<slug>.md`. A bare id folds under a heading that names
     no work item;
   - the eight suite-wide guard modules:
     `test_a_shrunken_corpus_declines_to_judge`,
     `test_a_rider_reaches_its_file`,
     `test_every_reader_ends_a_line_where_gfm_does`,
     `test_one_word_one_meaning`, `test_no_real_identifiers`,
     `test_a_record_states_what_the_tree_has`, `test_release_hygiene`,
     `test_docs_line_wrap`;
   - `survivor-check --range origin/release/v0.21.0...HEAD --exempt …` and
     `correction-check`, which CI's `release` job runs.

   Narrow runs missed each of these once.
5. **Probes that run bash or git use a scratch repository as `cwd`.** One
   reviewer probe ran `git switch` in the main checkout. Git refused it, and
   nothing changed.
6. **When a fix would list one more spelling, change what the check reads
   instead.** #860 (three rounds of merge-shape examples) and #868 (three
   rounds of brace spellings) were each reframed for this.
   - #860 now states the rule once, as the git command `own_commits` runs, and
     pins each shape as a test.
   - #868 now reads a segment's raw text with quoted spans neutralised and
     errs toward stopping.
7. **A subagent refused by the permission layer is not done for.** Re-run the
   step with a fresh agent. Do not write files on its behalf. A previous
   attempt left `<old scratch>/1791384158/round-2/`, which is old-machine
   scratch only.

## Issues this run filed

- #877: `survivor-check` reads a hand-typed `--range` holding a merge.
- #883: a head run that pytest stopped with exit 0 still seals.
- #884: unplaced counts; fixed by #880.
- #885: remove `SCALE_FOR_OLDER_HOOKS` after 0.21.
- #886: the guard reads past substitution, a here-string, an untokenizable
  line, or `--git-dir`.
- #888: evidence-check's opener misses a Go receiver, a generic function and a
  typed constant.

Filed earlier by the frames: #871, #872, #873, #874.

## Starting on a new machine

1. `git fetch origin`, then check `git config user.email` against the pinned
   address before the first commit.
2. Make one worktree per item that runs concurrently:
   `git worktree add ../SpecSeal-worktrees/<issue> <branch>`. The guard asks
   once; `[worktree-ok]` answers it for concurrent work.
3. Run tests with `bin/test <files>` (not `uv run --frozen pytest`). Use
   `uvx ruff` and `gh issue view N --json title,body,comments`.
4. Agents: framer on `model: fable`; smith, warden and sealer on
   `model: opus`.
5. At each segment's end, post its reading with `session_cost.py --segments
   <transcript> --post --says -` to the open `flow-measurement` issue (#865).
   `--post` exits 0 even when the post fails, so read its last line.
6. Keep the machine awake on an unattended run (`caffeinate -i`).

## After all eleven land

The release preparation follows `docs/release-checklist.md` §*2. Gather,
fold, bump*:
- gather the eleven `changelog.md` fragments and fold the ledger fragments;
- retire the process records with `settle --retire-process`;
- bump the version;
- open the release PR into `main`, which takes a merge commit.

0.20.0's process records (1791270161–1791270165) are still in the tree, as
#864's frame noted.
