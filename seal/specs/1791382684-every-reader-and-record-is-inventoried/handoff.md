# 0.21.0 — handoff after the frames

Written 2026-10-08 by the orchestrating session, for a session on another
machine. Nothing here depends on that session's local worktrees, memory or
scratch files: every branch below is pushed, and each carries a short
`handoff.md` of its own that points back here.

## Where the run stopped

The owner asked for the inventory and the frames only ("framer까지만").
Both are done. **No smith has been spawned and no plan is approved.** The
next act is the owner's answers, then the builds.

| Step | State |
|---|---|
| `release/v0.21.0` | cut from main 5623d728 (0.20.0 as shipped), pushed, untouched since |
| #834 inventory | this branch: routing 108621bb, inventory and synthesis 9fb33b26 (`inventory/` beside this file, `spec.md` §*Decisions taken from the table*) |
| Decision issues | #835, #836, #837 reopened with the table's grounds; #866–#870 opened; all in milestone `release: 0.21.0` |
| Frames | 11 work items framed by `framer` on Fable 5.1, each on its own branch cut from `release/v0.21.0`, routing committed before the frame |
| Follow-ups the frames asked for | #871, #872 (from #867's frame), #873 (from #860's), #874 (from #864's; the owner's to run) |
| Flow log | every framer segment's reading is on #865 |

## The owner's batch (2026-10-07, one question call)

- Routing for every 0.21.0 work item: **`automation`** (Review through the
  review chain, Destination open the pull request, Implementation smith,
  Automation yes, Answer pressed automation). Each branch's `routing.md`
  records it.
- After the inventory, the session opens decision issues from the table
  itself and frames them together with the milestone's items, with no stop
  in between.
- The inventory ran on Opus 5.5. **The framers ran on Fable 5.1**, at the
  owner's word. Nothing was said about smith's model.

## The work items

| Issue(s) | Branch | Work item | Frame | Phases | Questions for a person |
|---|---|---|---|---|---|
| #835 | `feat/835-a-reader-declares-its-input-class` | 1791384152 | e2e39990 | 3 | Q1 |
| #836 | `feat/836-a-ledger-rows-claim-is-the-test-that-enforces-it` | 1791384153 | f48d92e8 | 5 | Q1 |
| #837 | `feat/837-a-records-finding-closes-once-at-the-runs-end` | 1791384154 | 4bd38ac5 | 4 | Q1 |
| #866 | `fix/866-a-round-record-cell-has-one-reader` | 1791384155 | 29b85035 | 7 | none |
| #867 | `fix/867-config-rows-coordinates-and-headings-have-one-reader` | 1791384156 | 9d87aec1 | 6 | none |
| #868, #856 | `fix/868-the-hooks-read-the-session-waiver-and-creation-one-way` | 1791384157 | 3c079add | 6 | none (see #856 below) |
| #869, #852, #853 | `fix/869-the-broad-gate-reads-its-counts-from-the-recorder` | 1791384158 | a71dd6aa | 6 | none |
| #870, #848 | `fix/870-a-unit-the-extractor-cannot-bound-is-refused` | 1791384159 | 2f8ada50 | 4 | none |
| #860, #805 | `fix/860-a-fix-range-is-its-own-commits-across-a-merge` | 1791384160 | c49ece7d | 4 | none |
| #858 | `fix/858-the-plugin-directory-check-reads-the-directory` | 1791384161 | dc617a7d | 3 | Q1 |
| #864 | `chore/864-the-macos-test-leg-runs-in-shards` | 1791384162 | 5ff8b2ab | 2 | none |

Each frame is `seal/specs/<work item>/spec.md`, `plan.md` and
`questions.md` on its branch. `plan.md`'s `Approved <date> by <who>` line is
left blank on purpose: filling it when smith is spawned is the approval.

Not framed, on purpose:
- **#844** (a docstring reflow) is below the ladder's spec rung, and the
  issue says to take it with the next change to that function.
- **#857** (the stamp's mark) waits on the owner, and two records disagree
  about what the owner chose (below).

## The owner's answers (2026-10-08)

All seven rows below were answered in one message, and each answer is ticked
where the build reads it:

1. #835 Q1: (a), as framed. Ticked in its `questions.md`.
2. #836 Q1: (a), no bulk pass. Ticked in its `questions.md`.
3. #837 Q1: (a), unbounded. Ticked in its `questions.md`.
4. #858 Q1: leave, dated in the checklist's box. Ticked in its `questions.md`.
5. #856: (c) confirmed. On #868's `questions.md` bullet and on #856.
6. #857: the 28-cell record holds (0.20.0's changelog, docs,
   `assets/seals/README`, `read_chart`'s 28×28). The 24-cell § "D" note was
   a superseded intermediate step. The mark is still undecided, so #857 is
   **not framed in 0.21.0**; it waits on the owner's mark.
7. Release size: all eleven work items ship in 0.21.0.

Smith, warden and sealer are spawned with `model: opus`.

## What the owner had not answered (answered above)

Put these in front of the owner **in one question call before any smith is
spawned** (CLAUDE.md §*The goal a design is chosen against*). Every row has a
default the build can ship on, so a missing answer blocks nothing.

1. **#835 Q1:** should the inventory table live under `docs/` anyway?
   - The frame makes the registry a `Reads:` line in each reading unit's own
     docstring, plus a shrink-only census file. `docs/the-reader-registry.md`
     states the rule.
   - (a) as framed — **default**;
   - (b) a table under `docs/`: over the 1,000-line ceiling, and a shared
     file that every branch edits;
   - (c) both, with a generated listing under `docs/` rebuilt at each release.
2. **#836 Q1:** should a release write one bulk pass of `Corrected ·` rows
   over the ~1,042 released claim rows that already cite a test?
   - (a) no, rows migrate as edits reach them — **default**;
   - (b) a fold fragment at a release, written by one session;
   - (c) the same, tool-assisted.
3. **#837 Q1:** may the commit that closes the run's ⬜ notes touch paths
   outside `seal/` and `tests/`?
   - (a) unbounded, with the broad gate as its reader — **default**;
   - (b) bounded by `behaviour_path`, so a code- or docs-located ⬜ is
     answered or deferred, never edited.
4. **#858 Q1:** move SpecSeal's Console submission to the developer portal,
   or leave it?
   - **Default: leave**, recorded in the release checklist's box with its
     date.
   - The build is the same either way, except for one dated sentence.
5. **#856, decided by a framer, needs the owner's confirmation.** #856 asked
   a person to choose between (a) expanding braces and (b) naming them a known
   limit. #868's frame chose **(c)**: an unquoted brace expansion in a git
   word is an unrecognised shape, and the guard stops on it. It derived (c)
   from #826's own rule, and #856's reviewer had suggested the same fix. Ask
   before #868's phase 3 is built.
6. **#857, two records disagree.** A note from the 0.20.0 session says the
   owner picked a § "D" emblem on a 24-cell disc in the sheet's corner.
   #857's body, written later the same day, says the owner settled a 28-cell
   disc and reviewed the § among marks of which none was kept. Ask which
   holds before anything is framed for #857.
7. **Release size.** Eleven work items plus #834's build is large for one
   release, and the ledger drift is heavy: #866's frame alone counts 172
   released rows on the units it edits. Splitting is the owner's call.

## Build order the frames ask for

The seams are in each `plan.md` (§*Seams*, or §*Operational impact*).

- **#835 builds last** among the 0.21.0 chains, after the others have
  squashed into `release/v0.21.0`. Its census must start from the tree they
  leave. **#834's own build comes after #835** and moves the inventory's
  classes into the docstrings #835 defines.
- **#867 → #836 and #870** share `evidence_check.py`. #835's Q5 also wants
  #867 landed first.
- **#860 and #837 → #866** share `round_record.py` and `chain_check.py`.
  #866 puts its heaviest phases last because of this.
- **#869 and #866** share `broad_gate.py` (different units).
- **Independent:** #858, #864, #868.
- **#864 needs the session at its phase boundary.** Smith cannot push, so
  the session pushes phase 1 and runs
  `gh workflow run test.yml --ref chore/864-the-macos-test-leg-runs-in-shards`
  (or opens the draft pull request first, so a push runs it). Phase 2 reads
  that run.

## Starting on a new machine

1. `git fetch origin` and check `git config user.email` against the address
   the owner pinned for this repository before the first commit.
2. One worktree per item that runs concurrently, from its pushed branch
   (`git worktree add <dir> <branch>`). `SpecSeal-worktrees/<issue>` beside
   the clone was this run's layout.
3. **Tests in a fresh worktree:** `uv run --frozen pytest` cannot start
   pytest there (`Failed to spawn: pytest`). `bin/test <files>` works and
   builds its own gitignored `.venv`. Tell every smith.
4. `gh issue view N` printed nothing without a TTY for one framer. Use
   `gh issue view N --json title,body,comments`.
5. `ruff` may not be on PATH. Use `uvx ruff`.
6. On an unattended run, keep the machine awake (`caffeinate -i`) and check
   every running agent's transcript for a stall at least every 30 minutes.
7. At each smith or warden segment end, measure the transcript with
   `skills/verify/scripts/session_cost.py` and post it with `--post` to the
   open `flow-measurement` issue (found by label; #865 today). **`--post`
   exits 0 even when the post failed**, so read its last line rather than its
   status.

## What this session saw that the next one should know

- GitHub refused every write for several minutes on 2026-10-08 (HTTP 500 on
  comments, issue creation and `git push`), while githubstatus.com read all
  operational. The writes went through unchanged on a retry later.
- The inventory's rows are each agent's reading. Every frame re-read the code
  it rests on, and two frames found an inventory claim that did not hold:
  - #867's frame: E46 and E35 say a vendored copy is held by a test, and no
    such case exists;
  - #864's frame: #841's work item is still in the tree, not retired.
