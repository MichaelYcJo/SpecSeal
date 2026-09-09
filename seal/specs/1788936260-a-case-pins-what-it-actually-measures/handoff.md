# Handoff — SpecSeal 0.9.5, session of 2026-09-09

## Start here — what to say to the next session

Paste this as the first message of a fresh session in this repository:

> Read `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md`
> and pick up where it stops. The branch
> `fix/262-310-a-case-pins-what-it-actually-measures` is pushed at `9b3d451`
> with no pull request and no review round yet; take it from the draft pull
> request through the chain to ready. Do not re-ask the routing question —
> `routing.md` on that branch already answers all three axes. The owner's open
> decisions are listed in the handoff and none of them blocks you: state the
> assumption and keep going.

**Three things that session should not have to discover.**

- **`git switch <branch>` then `git status -sb`, every time.** A switch that
  did not take is what let this session run `git merge` on `main`. Nothing was
  committed and `main` is unmoved, but `docs/release-checklist.md` step 0 asks
  for that check and it is cheap.
- **`ruff` is absent from this checkout.** `uvx ruff check .` and
  `uvx ruff format --check .` are the form that works, and they are half the
  broad gate.
- **The issues that are merged but still open are correct.** #145, #295, #296,
  #297 and #300 close when the release reaches `main`. Closing one by hand
  breaks the next release.


Written for the session that picks this up. Everything below was executed in
this session unless labelled otherwise.

## Where the release stands

`release/v0.9.5` is at `0df9508`. Five pull requests are merged into it:
#293, #294, #298, #302, #306.

| Item | State |
|---|---|
| #145 · #295 · #296 · #297 · #300 | merged into `release/v0.9.5`. **Still open as issues, and must stay open** — `close_issues_on_release.py` closes them when the release reaches `main`, and closing one by hand breaks the next release (`docs/issues-and-milestones.md`) |
| #160 | **closed.** It had already been fixed a release and a half earlier |
| #262 · #310 | **branch pushed, no pull request yet** — see below |
| #149 · #103 · #198 | not started. Recommended for 0.9.6 |

## What is in flight, and it is two things

### 1. `fix/262-310-a-case-pins-what-it-actually-measures` at `9b3d451`

Pushed, **no pull request opened, no review round run.** Six commits: routing,
the SDD set, #310's fix, the checker, the phase records, and one survivor
exemption.

Built by `specseal:smith`; **the implementer's report has not been verified by
a reviewer.** What it delivers:

- **#310** — the four substring assertions in
  `test_the_section_names_batching_as_the_way_a_share_passes_one_hundred`
  replaced by the whole-clause version. Three rearrangements of the claim used
  to pass at exit 0.
- **#262** — `skills/verify/scripts/arm_check.py`, `bin/arm-check`,
  `bin/arm-check.cmd`, 35 cases in `tests/test_arm_check.py`, and a section in
  `skills/verify/SKILL.md` §2.

**The next steps, in order:** open a draft pull request into
`release/v0.9.5` → `specseal:warden` round 1 at `9b3d451` → the rounds → the
broad gate **once, after they settle** (`agent-contract` §2) → mark ready.
`ruff` is absent from this checkout; `uvx ruff check .` and
`uvx ruff format --check .` are the form that works.

**The one finding that changed the build, and the reviewer should open it
first.** The survivor count depends on which way an arm is broken: `invert`
alone gives **1** survivor, `remove` gives **12**. #262's nine is a *removal*
count — every sentence in its table is about taking something out — so a
checker reporting 1 beside the ticket's 9 would have read as a refutation by
an instrument measuring something else, which is this work item's own subject.
Reproduced by this session:

```
32 arms mutated · 31 killed · 1 watched by no case
  invert   32 asked · 31 killed · 1 survived
  remove   32 asked · 20 killed · 12 survived
```

Ten of the twelve are in `main`, where #262 put eight of its nine, and
`gh_segments` has none — which matches the four the ticket says were closed on
an earlier branch. The single arm nothing notices either way is `main:189`,
`except Exception` around `json.load(sys.stdin)`: no case feeds the hook
malformed stdin.

**The arm count, three numbers and why they differ.** Counted by construction
with #262's own rule: `reader` 5, `is_closed` 4, `gh_segments` 5, `main`
**17** — total 31 per function, **32** including `if __name__ ==
"__main__":`, which sits in no function so a per-function table had nowhere to
put it. #262's table says 33, differing only in `main` (19), and the file
changed twice after that measurement (`341be0b`, `1dedd1e`). **The ticket's
table is deliberately left as written**: it was true when measured, and
correcting a shipped ticket's number hides the argument the ticket makes.

**Three defects the implementer found by building, worth a reviewer's eye:**

1. **Cached bytecode can decide an arm's verdict and no hash sees it.** A
   `.pyc` is validated on mtime *and size*, and two different mutations can
   both add six characters. A fixture's unreached arm came back `killed`.
   `restore` compares the file's hash, and the file was right. The
   reproduction is timing-dependent, so the case pins the mechanism rather
   than the occurrence.
2. An except tuple and a wrapped boolean test span their own brackets —
   `except OSError, ValueError:` is not Python, and `reader`'s three-member
   handler is exactly that shape.
3. An operator that could not be asked of one arm was invisible: the report
   printed `remove 31 asked` against 32 arms and named neither the arm nor the
   reason. That is the skip-versus-refuse failure the module refuses, inside
   the code that reports refusals.

**And four of its own cases first passed against the mutation aimed at them**
and were rewritten — each asserted something true that was not the claim. All
four would have shipped. That is #310's class, found by the implementer in its
own work.

### 2. `docs/the-two-merged-items-are-ticked` — pull request #305, open

Ticks #145, [#296 · #295 · #297] and #300 on `docs/flow.md`, and adds #310's
row. It carries a merge of `release/v0.9.5`, which the checklist permits for a
branch that needs something the release branch holds. **Merge it before or
after #262's, either way** — but the #262 · #310 branch does not touch
`docs/flow.md`, so those two rows are still owed after it merges.

## Decisions waiting on the owner, none of them blocking

| # | Question | Where |
|---|---|---|
| Q1 | **What `arm-check`'s exit code should mean.** It is report-only today, pinned by a case so changing it is a decision rather than a slip. Three answers: report-only · non-zero on any unwatched arm · non-zero when the count rises above a recorded baseline. The third is this session's recommendation, and the first run's number now exists to set a baseline from | this work item's `questions.md` |
| Q2 | Whether the twelve survivors are gaps. #262 already names two as behaviour-preserving | same |
| Q3 | **`command` exceeding 100% of a span**, measured at 115.7% on a real transcript. Three costed answers, none built. Round 1 of #300 corrected the trigger: over 100% is 1 of 169 transcripts, but overlap moves a printed number in 23, and answer 3 leaves 22 quietly inflated | `seal/specs/1788926756-…/questions.md` |
| Q4 | Whether `session_cost.py`'s `span_s` question is fully settled — Q5 of #145 was answered (`max(end)`) and this is the residue | same |
| Q4 | Whether the `Broad gate` cell should be validated where it is written, now that `chain_check` reads it | `seal/specs/1788912166-…/questions.md` |

## Issues this session opened, all found by using the tools

| # | What | Milestone |
|---|---|---|
| #292 | A payload is written again on every spawn — `cache_creation` 40,259–75,737 tokens on every one of 49 spawns, `cache_read` a constant covering only the harness prefix | 0.10.0 |
| #299 | A ledger row whose coordinate the anchor pattern rejects is dropped and the total reports clean. **Four instances now**, the fourth a bare `#unit@hash` with no path | backlog: ledger & checker |
| #301 | The commit gate asks a person about a `-C $W` whose assignment is in the same command string | backlog: gates & hooks |
| #303 | `round_record.py new` writes a verdict row `close` refuses | backlog: review chain & agents |
| #304 | A `survivors.md` one directory deeper has no owner, so its declaration reaches every work item | backlog: gates & hooks |
| #307 | A shipped changelog entry is a record of a past release, and every behaviour change survives in it | backlog: gates & hooks |
| #308 | Writing a `survivors.md` row removes its own quote from what `survivor-check` searches for. **This session's first diagnosis was wrong and is corrected in a comment** — the cause is `wanted`'s added-n-gram subtraction, not document frequency | backlog: gates & hooks |
| #309 | `round_record.py new` reads one physical line of a field; `close` drops a deferred row's grounds and writes an empty code span | backlog: review chain & agents |
| #310 | A case pins a paragraph's vocabulary and lets three rearrangements of its claim pass | 0.9.5, **in flight above** |

## What this session got wrong, so the next one does not inherit it as fact

Five errors, every one caught by a subagent rather than by me:

1. **A false acceptance row in `spec.md`** of `1788926756`: that the span rule
   would close the plain report's `command 101%`. It does not —
   `command_s` sums overlapping calls. The row **stays as written** and
   `overview.md` records the divergence, so the Design Gate's approval is not
   erased.
2. **A single-axis sweep reported as complete.** *"Nothing printed moves"* was
   measured per run; the readings publish per **row**, and a third surface
   (between-the-rows figures) existed too. Five printed figures move
   machine-wide, all in other projects' transcripts.
3. **#308's diagnosis**, above.
4. **A `seal/follow-up.md` row whose rider grounds named the wrong file's
   anchors** — `session_cost.py`'s for a coordinate in `chain_check.py`.
   Corrected by the session that wrote it.
5. **"All four carriers closed"** written in a round record without adding the
   enumeration up, which left a flat *three printed figures* against an
   enumeration of five. That is the class the work item was closing.

**And one procedural slip**: a `git switch` that did not take, followed by a
`git merge` on `main`. No commit resulted and `main` is still at
`origin/main`; `docs/release-checklist.md` step 0 asks for `git status -sb`
after every switch, and skipping it is what allowed it.

## The pattern worth carrying forward

Across four work items today, **every sharpest defect was in a sentence rather
than in code** — nine pages wrong about where a delegated wall clock went, a
line printing a negative and calling it a wait, a disclosure naming the rarer
cause as the ordinary one, and a pin that asserted vocabulary where the claim
had a ranking. The arithmetic was right every time.

Twice the implementer refused a number the reviewer's report handed it and was
right both times (12–31% not 12–26%; 97 not 96). Both refusals are in the
records.
