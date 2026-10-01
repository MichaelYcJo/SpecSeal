# Feature Specification: the seal names what it sealed and counts only the steps that run

<!-- seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #666, milestone 51 (`release: 0.17.0`). The owner wrote it on
2026-09-29 reading 0.16.0's first stamp, for work item `1790635412` (#585,
pull request #659): the panel named the base and never the branch or the work
item, `from` held the destination, and `workflow 8 of 13 not answered` counted
steps CI never runs for a feature pull request. The ticket's three tables
(Add · Change or drop · Keep) are the requested behaviour; every row of them
is answered below, and where a row conflicts with something the tree reads,
the tree wins and the clause says so.

**What this is, in one line.** The stamp, the `SEALED`/`NOT SEALED` lines and
the hook's label name the branch, the base's ref and the work item they
sealed; the panel drops the rows that said nothing; the `workflow` row and
its stderr line count only the steps CI runs for this base; and the record's
`Broad gate` cell does not change at all.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* — *"Every step CI runs is either mirrored by a named arm or excluded with a written reason. There is no third state and no silence."* | The `workflow` count stays a reading of `PARTITION`. What changes is the denominator: a step CI does not run for this base is neither answered nor unanswered, so it leaves the count, and the list that says which steps those are is declared and held against the workflow the way `SKIPPED_AT_MAIN` already is |
| `docs/the-broad-gate.md` §*The gate and CI ask about the same range, and the base is resolved once* — *"The base becomes a resolved commit plus the ref it came from"* | The name printed beside the base commit is the **resolved** ref (`Base.ref`, what CI reads), not the spelling the caller typed. The ticket's example `base 551c7967 (release/v0.16.0)` shows the given name; #423's whole repair was that a reader must be able to tell `origin/release/v0.16.0` from a local ref a week behind it, so the tree wins here |
| `docs/the-broad-gate.md` #475 paragraph — *"the panel's `gate` row reads `tree <version>` or `plugin <version>`"* | This sentence becomes false when the row prints only where the two copies differ. It is corrected in the same work item (same file, §*A document that its own work item's fixes disproved is corrected in the same work item*) |
| `docs/the-broad-gate.md` §*Where the stamp is drawn* — the stamp is drawn *"only over a run that earned it"*, and *"what is drawn is the run's values rather than a sample"* | Everything on the panel is drawn on success alone. So a row whose value success fixes (`row exit 0`) carries nothing, which is why the ticket's fold is answered by moving the exit under `suite` rather than by giving it a row of its own; and `SAMPLE_ROWS` must mirror the real panel's labels, because `seal-stamp` with no arguments is what *"shows a person what the gate will print"* (`seal_stamp.py`, the comment above `SAMPLE_ROWS`) and it still says `lint clean`, which `broad_gate.py#panel`'s own comment refuses as a counterfeit |
| `skills/verify/SKILL.md` §*A seal says what it did not answer* — *"The count is on the panel because a panel value is 23 columns and a step name is a sentence"* | The 23-column value width (`broad_gate.PANEL_VALUE_WIDTH`, pinned by `test_the_panel_value_width_is_what_the_stamp_actually_gives`) is a constraint the ticket's proposals do not fit: measured, four of its values are 26 to 33 columns (§*What was measured*). The panel is not widened; a value that does not fit continues on an unlabelled line under its label, and a ref or branch name, which has no bound, is elided at the frame as the `from` row already is |
| `skills/verify/SKILL.md` §*The broad gate — after the rounds* — *"a run that ends at the round cap closes its last finding `deferred <home>`, which is a closing word, so the box is checked while the reviewer's row keeps the `yes`"* | This is the tree's definition of a capped record, and `rounds … capped` is read off it: the last record's `Needs a fix` begins `yes` while `seal` has already refused an unchecked `Pass`. The deferred count and its homes come from the same record's verdict table, through `chain_check.py`'s own reader |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* — *"its verdict reads `deferred <home>` … `deferred #N` where that home is an issue"* | The home printed after `deferred` is whatever the cell carries after the word (`chain_check.verdict_of` reads it as `deferred <home>`); an issue number is the common case, and a file path is printed as it stands |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a failure direction, a prompt budget, platform honesty. Direction: the gate blocks nothing new and allows nothing new — every change is to what it prints and writes to the values file; exit codes and the cell are untouched. Prompt budget: zero; the one new line tells the orchestrator to commit, it asks nobody anything. Platform: the panel stays ASCII-separated for the letter twin, which exists for consoles that are not UTF-8 |
| `agent-contract` §14, §15 | Every rendered line this work changes is documented and pinned in the same commit, and every pin is seen red first (`plan.md`'s Verified-by column names the file each pin lives in) |
| `CLAUDE.md` *Repo rule — a change writes fragments, never the shared file*, and the paragraph after it | New rows go in `seal/ledger/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run.md`. Three existing release rows become false or drift and are handled in place (§*Data & interfaces*, *Ledger rows this work drifts*) |
| `CLAUDE.md` *Repo rule — a thing more than one party can have is named with whose* | The new prose says *the sealer's stamp* and *the panel*, never a bare *the seal* for the drawing. `tests/test_one_word_one_meaning.py` is the check |
| `skills/implement/SKILL.md` §3's ladder | Text a person reads and acts on changes on every seal, so this is the top rung: `spec.md`, `plan.md`, then the build |

## What was measured before the frame, and by whom

| Fact | Label | Where |
|---|---|---|
| The panel gives a value 23 columns (`PANEL_VALUE_WIDTH = 23`, `PANEL_WIDTH = 36`, `letter()` cuts at the frame with no marker) and the drawn stamp is 81 columns wide at the 0.90 default | executed 2026-10-01 by the framer: `python3 skills/verify/scripts/seal_stamp.py --shape` piped through a width count; constants read in `seal_stamp.py#letter` and `broad_gate.py#PANEL_VALUE_WIDTH` | this file |
| Of the ticket's proposed values, `3b76ca2a (feat/585-...)` is 23 columns, `551c7967 (release/v0.16.0)` 26, `551c7967 (origin/release/v0.16.0)` 33, `#659 · 1790635412` 17, `3 · capped · 2 deferred → #664` 30, `5081 passed, 10 skipped · exit 0` 32, `2662 ok . 0 drifted . 0 broken` 30, `4 of 9 not answered` 19; this branch's own name is 73 | executed 2026-10-01 by the framer, `len()` over the strings | this file |
| `hygiene.yml`'s `release` job has 13 named steps. Four open their `run:` with `if [ "${{ github.base_ref }}" != "main" ]; then … exit 0` — *a change to what ships must move the version*, *every changelog fragment reached the released file*, *every ledger fragment folded into the gathered ledger*, and *the milestone this release claims is the work it carries*. The ticket names three; the tree has four. Two open with `= "main"` (survivors, corrections), and `broad_gate.SKIPPED_AT_MAIN` already leaves their arms out at `main` | read 2026-10-01, `.github/workflows/hygiene.yml` lines 66, 116, 135, 347 (`!=`) and 250, 303 (`=`) | this file |
| So for a feature pull request CI runs 9 steps, of which the gate mirrors 5 (`unverified`, `chain`, `survivors`, `corrections`, `mode`): the honest row is `4 of 9 not answered`. For a release pull request CI runs 11 and the gate mirrors 3: `8 of 11` | read, derived from the two facts above and `broad_gate.PARTITION` | this file |
| `#659` in the ticket's `item` example is the **pull request** of work item 1790635412 (its issue is #585, carried in its branch name `feat/585-…`). The record holds it: `rounds/round-3.md` reads `| PR | #659 |`. `chain_check.PR_FIELD`/`PR_RE` already read that row, and `not yet opened` is its honest value before a pull request exists | read 2026-10-01, `seal/specs/1790635412-*/rounds/round-3.md` and `routing.md`; `gh pr view 659` executed | this file |
| That same record is the capped shape the ticket's `rounds 3 · capped · 2 deferred → #664` describes: `Fixes checked by | no fixes to check`, `Needs a fix | yes — 🟡 1, …`, verdicts closed `deferred #664` | read 2026-10-01, the same file | this file |
| `evidence-check --strict` exits 2 on DRIFTED, MALFORMED and OVERFLOW, and the gate passes `--strict`; so on a stamp, which is drawn on success alone, `drifted` and `broken` are both 0 by construction. The count that varies is on the `NOT SEALED` form, where `failure_lines` quotes the check's first 8 lines and `evidence-check`'s `total:` line is its last | read 2026-10-01, `evidence_check.py#exit_code` (line 3380 region), `broad_gate.py#failure_lines`, `#LEDGER_RE` | this file |
| The values file is written by the gate the **tree** ships and read by the hook the **installed** plugin ships (`hooks/sealer-stamp.py` docstring, `drawings`). `read_values` requires only that `rows` is a list of `[str, str]` pairs or `null` and `scale` a number; `label` reads `tree`, `base`, `item` and ignores other keys | read 2026-10-01, `seal_stamp.py#read_values`, `#label`, `hooks/sealer-stamp.py#drawings` | this file |
| `broad_gate.main` redirects to the tree's copy as a subprocess with the same argument vector and inherited streams; the child has no way to know the installed copy's path today, and `redirect_line` is the only place both are named | read 2026-10-01, `broad_gate.py#main`, `#redirect_line`, `#gate_copy` | this file |
| The `rounds` row today is a file count (`round_count`), and the gate reads nothing out of the record it just sealed. `chain_check.py` owns the record readers: `table_rows`, `field`, `verdict_table`, `verdict_of` (which hands back `deferred <home>` with the home), `PASS_RE`, `NEEDS`, `PR_FIELD` | read 2026-10-01 | this file |
| Sibling 0.17.0 branches: `feat/638-…` (`broad-gate --preflight`, named in the milestone as touching `broad_gate.py`) holds only its `routing.md` so far; `perf/641-…` and `chore/640-…` touch none of the gate files | executed 2026-10-01, `git diff --stat release/v0.17.0...<branch>` | this file |
| Tests that pin today's text: the label `SEALED aaa1111 against bbb2222 · 1799000000-an-item` (`tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` lines 246, 294–295, 315; `tests/test_a_gate_that_fails_says_so.py` line 621 by prefix); the signal line `<tree> against <base>` and the values file's label tuple (`tests/test_the_seal_is_taken_once_by_the_sealer.py` lines 2370–2440, and `row_of(values, "gate")` at 817–885); `("from", "origin/base") in rows`, the rendered `from` row, the `SEALED`/`NOT SEALED` heads and the document pin on `from` (`tests/test_the_gate_asks_the_range_ci_will_ask.py` lines 549–592, 786–799); `HISTORICAL_ROWS` and `2 of 3 not answered` (`tests/test_the_gate_names_every_step_ci_runs.py` lines 551–600, 696–705); the `SKIPPED_LINE` and `SKIPS_AT_MAIN` guard case (same file, 904–1055) | read 2026-10-01, `grep` then the regions opened | this file |

## Scope

### In

**S1 — The lines name what they sealed.** `broad_gate.py#signal`'s head and
`seal_stamp.not_sealed`'s head both read
`SEALED   <branch> @ <tree> against <ref> @ <base commit>` (and
`NOT SEALED   …` the same way), where `<branch>` is the checked-out branch
(`git symbolic-ref --short -q HEAD`) and `<ref>` is `Base.ref`. On a detached
HEAD the branch and its `@` are left out and the tree prints alone, as the
ticket asks. Where `Base.ref` is not a branch-shaped name but the commit
itself (a bare SHA given as `--base`, or a repository with no remote), the
`<ref> @` half collapses to the commit alone, so no line reads
`1e2bed9 @ 1e2bed9`. The hook's label (`seal_stamp.label`) carries the same
head and then ` · #<pr> · <item basename>`, with ` · #<pr>` left out where
the record names no pull request. **A values file without the new keys draws
the label it draws today**, because an installed hook may be older than the
gate that wrote the file and a file written before this change may still be
pending.

**S2 — A recorded seal says to commit the cell.** On a sealed run with
`--record`, one line follows the `SEALED` line on the same stream: the
`Broad gate` cell was written into the working tree and is not committed, and
CI reads the record at HEAD, so commit it before the pull request is marked
ready. It names the act and the reason; the exact wording is the work's and
the case that pins it fixes it. Only a recorded seal prints it — without
`--record` there is no cell — and a `NOT SEALED` run prints it never, because
nothing was written.

**S3 — The panel names the branch, the base's ref and the work item, and
loses the rows that said nothing.** `broad_gate.py#panel` returns, in this
order (a row in brackets is conditional):

```
SEALED
(blank)
tree      <tree>
          <branch>                      [absent on a detached HEAD]
base      <base commit>
          <Base.ref>
item      #<pr> . <id>                  [absent without --record; `<id>` alone with no PR number]
gate      tree <version>                [only where the running copy is the tree's AND differs from the installed copy]
(blank)
suite     <pytest counts, or `exit N` where there are none>
          exit <N>                      [only where the counts line is present]
ledger    <N> ok
          <D> drifted . <B> broken
chain     exit <N>
(blank)
workflow  <n> of <m> not answered       [absent without a hygiene workflow]
(blank)
rounds    <R>[ . capped]                [absent without --record]
          <k> deferred -> <homes>       [only where k > 0]
```

- An unlabelled continuation row is `("", value)`; `seal_stamp.letter`
  already renders it as the value under its label's column. **The panel is
  not widened and no value is cut**: every value on every row is at most
  `PANEL_VALUE_WIDTH` columns, and a case measures each over the longest
  realistic input (this branch's own 73-character name, a `refs/remotes/…`
  ref, five-digit counts).
- `<branch>` keeps its **head** (`feat/666-the-seal-na...`): the issue number
  leads and is what a reader matches to a ticket. `<Base.ref>` keeps its
  **tail** (`...release/v0.16.0`), the rule `panel` already applies to the
  `from` row and for the same reason — the prefix is the part a reader can
  infer. Both use `ELISION`.
- `<id>` is the digits before the first `-` of the item directory's name.
  `<pr>` is the last record's `| PR |` row read with `chain_check.PR_RE`;
  `not yet opened`, no record (a `broad-gate.md` home) and no row all mean
  no number.
- `from` and `row` are gone. The row's exit code moves under `suite`, which
  is what the ticket's fold means and the one place it fits; where
  `suite_counts` found nothing the row already reads `exit N` and no
  continuation is added.
- `ledger` carries `drifted` beside `broken`. On a drawn panel both are 0 by
  construction (§*What was measured*); the row is kept in the ticket's shape
  because the owner asked for it and it costs one line, and **the count that
  varies goes where it varies**: the `NOT SEALED` form's `ledger` entry ends
  with `evidence-check`'s `total:` line where its output has one, the way
  the `suite` entry already ends with pytest's counts (`failure_lines`).
- `gate` prints only where a tree copy ran and its `broad_gate.py` is not
  byte-identical to the installed copy's. `main` hands the child the running
  copy's realpath in the environment when it redirects; `gate_copy` compares
  the two files. A tree copy invoked directly, with no installed path handed
  over, prints the row — the direction that says more when it cannot tell.
  A repository that ships no gate never printed `tree` and now prints
  nothing, which is the ticket's *carries no information* case.
- Separators on the panel are ASCII — ` . ` as the `ledger` row already uses,
  and `->` — because the letter twin exists for a console that is not UTF-8
  (`seal_stamp.pick_shape`), and `·`/`→` are what such a console replaces
  with `?`. The ticket's `·` and `→` are read as *a separator* and *an
  arrow*.
- `SAMPLE_ROWS` mirrors the new panel's labels and shapes, with neutral
  values; a case holds the sample's label sequence against `panel()`'s over a
  fixture, so the two cannot drift again (`lint clean` has been standing on
  the sample since #400 kept it *unchanged*).

**S4 — `rounds` says capped and counts the deferred findings.** The gate
reads the item's last record through `chain_check.py` loaded by path (the
way it already loads `seal_stamp.py` and `hooks/config.py`), never through a
second reader of a round record. `capped` is appended where the record's
`Needs a fix` cell begins `yes` — `seal` has already refused an unchecked
`Pass`, so this is the tree's capped shape (Grounding). The continuation
line counts the verdict rows `verdict_of` returns as `deferred <home>` and
lists the distinct homes after `->`, in table order; `deferred (no home)`
rows are counted and print no home. A record with no `## Verdicts` section,
no `Needs a fix` row, or a `broad-gate.md` home prints `rounds <R>` alone.

**S5 — The `workflow` row and the stderr line count only the steps that run
for this base.** `broad_gate.py` declares `ONLY_AT_MAIN`, the four step
names whose `run:` exits on `base_ref != main`, beside `SKIPPED_AT_MAIN`.
One function answers *is the given base `main`* for both lists (today's
reading: the caller's spelling with one leading `origin/` removed is `main`),
and one function returns the steps that run for this base: every step of the
`release` job, less `ONLY_AT_MAIN` where the base is not `main`, less the
steps `SKIPPED_AT_MAIN`'s arms mirror where it is. `unanswered`,
`coverage_line` and `panel` count over that list. The stderr line names
only the unanswered steps CI will run, and adds one clause saying how many
steps are left out for this base and why (`run only on a pull request into
main`, or `CI skips at main`). The partition case holds `ONLY_AT_MAIN`
against the workflow's `!= "main"` guards from both sides, the way
`SKIPS_AT_MAIN` is held: a guard added to a fifth step, or dropped from one
of the four, fails the suite. The bound is the same as `skipped_at_main`'s
and is named rather than claimed: the list is keyed on step name and on the
spelling `main`/`origin/main`, so `refs/heads/main` reads as not-main and
counts the four steps as running, which over-asks.

**S6 — Every document that names a panel row, the `SEALED` line or the
`gate` row moves with the code**, and every pin that reads today's text is
seen red and then moved: `agents/sealer.md` (§*The command*: the exit-0
bullet, the `gate` paragraph, the *base beside `from`* sentence, the
release-pull-request paragraph), `skills/code-review/orchestration.md`
§*The stamp is drawn for you* (the `SEALED` line, and the commit-the-cell
instruction the new line now carries), `skills/verify/SKILL.md` §*A seal
says what it did not answer* and the sentence *the stamp's panel names the
ref beside the commit*, `docs/the-broad-gate.md`'s #475 paragraph,
`broad_gate.py`'s module docstring (*the disc and a panel carrying…*) and
`panel`/`gate_copy`/`coverage_line` docstrings, `seal_stamp.py`'s module
docstring and the comment above `SAMPLE_ROWS`. `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_documents_name_the_panel_row_the_gate_actually_prints`
pins `from` by name in `agents/sealer.md`; it moves to the row that now
carries the ref.

### Out, and why

- **The record's `Broad gate` cell and its readers.** It keeps
  `<sha> against <sha>`; `chain_check.broad_gate` takes the first SHA-shaped
  word (`SHA_RE`) and `round_record.kept_broad_gate` keys on the same, so a
  branch name in the cell would be read as prose at best. Ticket §Keep; the
  tree agrees. `round_record.py` and `chain_check.py` are not edited.
- **`seal-stamp --from <file>`.** Unchanged; it is the only route when the
  `Stop` hook cannot draw. Ticket §Keep.
- **`chain exit 0`.** It is as constant on a drawn panel as `row exit 0` was,
  and the ticket keeps it; dropping it is a question for the owner, not a
  thing to do unasked.
- **Widening the panel, the disc, the chart, the scale.** The geometry was
  chosen by the owner over six rendered scales (#400); a wider panel moves
  the 81-column stamp past what was looked at. `questions.md` Q1 holds the
  default and the reversal.
- **A second `workflow` reader.** The gate does not read the guards off the
  workflow at run time; it declares the list and a case holds it, the
  pattern `SKIPPED_AT_MAIN` set. A run-time reader of inline shell is the
  second reading of one question `PARTITION` exists to stop.
- **Looking the pull request up** (`gh`) where the record reads
  `not yet opened`. The gate reads no network and carries no token
  (`PARTITION`'s own exclusion of the milestone step).
- **The installed hook's label on files the new gate writes**, until 0.17.0
  is installed: it draws the rows the file holds (every row is a string
  pair) under its own, older label. Named as a cost, not repaired.
- **`#638` (`broad-gate --preflight`).** A sibling branch into the same
  release, touching the same file. Both squash into `release/v0.17.0`; the
  later one merges the release branch in, never rebases
  (`docs/release-checklist.md` §0). Named in `plan.md` §Operational impact.
- **The READMEs.** Both list the hook (`test_both_readmes_list_the_stamp_hook`)
  and name no panel row (`grep` over `README.md`, `README.ko.md`).

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | A sealer seals a feature branch | Given a checkout on branch `feat/x`, `--base base` resolving to `origin/base`, a sealable item whose last record reads `PR \| #12`, when the gate seals on a pipe, then stdout's `SEALED` line reads `SEALED   feat/x @ <tree> against origin/base @ <base commit>` followed by the clause it carries today, and the next line says the cell is written and not committed and that CI reads HEAD | `tests/test_the_seal_is_taken_once_by_the_sealer.py`, the `sealed_values` cases |
| A2 | A detached HEAD | Given HEAD is detached, then the head reads `SEALED   <tree> against <ref> @ <commit>` with no branch and no stray `@` | same file |
| A3 | A base that is a bare commit | Given `--base <sha>` or a repository with no remote, then the head reads `against <commit>` once, not `<commit> @ <commit>` | same file; `tests/test_the_gate_asks_the_range_ci_will_ask.py` A6/A7 cases |
| A4 | A red run | Given a planted failure, then the first line reads `NOT SEALED   <branch> @ <tree> against <ref> @ <commit>`, no commit-the-cell line follows, and the `ledger` entry, where that check failed, ends with its `total:` line | `tests/test_the_gate_asks_the_range_ci_will_ask.py#test_the_failure_form_names_the_base_the_checks_were_asked_about`; a new `ledger` failure case in the sealer test |
| A5 | The panel's rows | Given A1, then the values file's rows are exactly S3's sequence for that run — `SEALED`, blank, `tree`, `""`, `base`, `""`, `item`, [`gate`], blank, `suite`, `""`, `ledger`, `""`, `chain`, blank, [`workflow`], blank, `rounds`[, `""`] — and no row's value exceeds `PANEL_VALUE_WIDTH` | `test_the_values_file_holds_this_runs_panel`, rewritten; a width case over the longest inputs |
| A6 | The names are elided, not cut | Given a 73-character branch and a `refs/remotes/other/release/v0.16.0` ref, then the branch continuation keeps its head and ends in `...`, the ref continuation starts with `...` and keeps its tail, and the rendered panel carries both | the same width case, rendered through `seal_stamp.stamp(shape=True)` |
| A7 | `item` | Given the last record reads `PR \| #12` then `item` is `#12 . <id>`; given `not yet opened`, a `broad-gate.md` home, or no row, then `item` is `<id>` alone; given no `--record`, there is no `item` row and no `rounds` row | sealer test cases |
| A8 | `gate` only where the copies differ | Given a tree shipping a `broad_gate.py` byte-identical to the invoked copy, then the panel has no `gate` row; given a tree whose copy differs, then `gate` reads `tree <tree version>`; given a repository shipping no gate, no row; given the tree's copy invoked directly, the row | `tests/test_the_seal_is_taken_once_by_the_sealer.py` #475 cases (lines 752–885), rewritten |
| A9 | `suite` and `ledger` | Given pytest counts, then `suite` is the counts and the next row is `exit 0`; given no counts, `suite` is `exit 0` with no continuation. `ledger` is `<N> ok` and the next row `<D> drifted . <B> broken`, read from the same `total:` line | sealer test; `test_the_panel_renders_its_rows_and_its_blanks` for a `""` label |
| A10 | `rounds` on a capped run | Given a last record with `Pass` checked, `Needs a fix \| yes — …`, `Fixes checked by \| no fixes to check` and two verdicts `deferred #664`, then `rounds` reads `3 . capped` and the next row `2 deferred -> #664`; given two homes, both are listed in table order; given `Needs a fix \| no` and no deferral, `rounds` reads `3` with no continuation | new sealer test cases over a fixture record in that shape (the same shape as `seal/specs/1790635412-*/rounds/round-3.md`) |
| A11 | The count for a feature base | Given this repository's `hygiene.yml` and a base that is not `main`, then `workflow` reads `4 of 9 not answered`, the stderr line names the four unanswered steps that run and none of the four only-at-main steps, and says four steps are left out because they run only on a pull request into `main` | `tests/test_the_gate_names_every_step_ci_runs.py`: the not-answered case gains a base and a guarded step in `FIXTURE_WORKFLOW`; a case over the real workflow's step names |
| A12 | The count for a release base | Given base `main`, then `workflow` reads `8 of 11 not answered` over the real workflow's names, the two `SKIPPED_AT_MAIN` steps are left out of the count, and `SKIPPED_LINE` prints as today | same file, #473 cases extended |
| A13 | `ONLY_AT_MAIN` is held against the workflow | Given `hygiene.yml`, then the set of `release` steps whose `run:` carries the `!= "main"` guard equals `ONLY_AT_MAIN`, from both sides; a guard added to another step or removed from one of the four turns the case red | same file, a twin of `test_the_arms_left_out_at_main_are_the_arms_whose_steps_skip_there` (line 1023) over `workflow_step`, with a `!= "main"` pattern beside `SKIPS_AT_MAIN` |
| A14 | A repository with no workflow | Given no `.github/workflows/hygiene.yml`, then the panel has no `workflow` row and the rest of the panel is S3's; nothing else about the run changes | `test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before`, `HISTORICAL_ROWS` moved to the new set |
| A15 | The hook's label | Given a values file with `branch`, `from`, `pr`, then line 1 reads `SEALED <branch> @ <tree> against <from> @ <base> · #<pr> · <item basename>`; given a file without `branch`, line 1 reads today's `SEALED <tree> against <base> · <item basename>` | `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` label cases; `tests/test_a_gate_that_fails_says_so.py` line 621 keeps passing unchanged, which is the compatibility assertion |
| A16 | The sample follows the panel | Given `seal-stamp` with no arguments, then its labels, in order, are the labels `panel()` produces for a run with every conditional row present | a new case in the sealer or stamp test |
| A17 | Nothing else changed | The cell written by `seal` is `<tree> against <base commit>` exactly as before; `chain_check` reads it as before; exit codes 0/1/2 and their causes are unchanged | the existing cell and exit cases, untouched and green |
| A18 | The documents say what the code prints | Each sentence S6 names is replaced, and a pin reads the new sentence | document-pin cases, each seen red with its sentence deleted |

## Data & interfaces

**The values file** (`seal_stamp.write_values`) gains `branch` (string, or
`null` on a detached HEAD) and `pr` (string such as `#12`, or `null`), and
keeps `tree`, `base`, `from`, `item`, `session`, `scale`, `rows`. `rows` is
exactly `panel()`'s return, with `""` as the label of a continuation row.
`read_values` accepts it unchanged.

**`panel(tree, base, checks, item, workflow=None, copy=None)`** gains what it
needs to name the branch, the pull request, the capped state and the base
the count is keyed on; the signature is the work's, with the constraint that
the three existing readers of `panel` in the tests (`panel_rows`, the range
test, the sealer test) are updated in the same commit.

**`not_sealed(tree, base, failures)`** gains the branch and the ref, with
`None` for either meaning *leave it out*.

**`label(values)`** reads `branch`, `from`, `pr` where present and falls
back to today's shape where `branch` is absent.

**`gate_copy(root)`** reads the installed copy's path from the environment
variable `main` sets on redirect (name chosen by the work, documented beside
`SESSION_VAR` as the second undocumented-to-nobody variable the gate reads)
and returns `None` where the row is not printed.

**`ONLY_AT_MAIN`**, a tuple of four step names; `base_is_main(given)`;
`steps_for(workflow, given)`. `skipped_at_main` keeps its signature and
reads `base_is_main`.

**The new line after `SEALED`** is one `str` constant in `broad_gate.py`
beside `DRAWN_AT_TURN_END`, printed by `gate` after `signal`'s line on a
recorded seal.

**Ledger rows this work drifts or falsifies** (read 2026-10-01; the exact
set after the edit is what `evidence-check` names):

- `seal/releases/0.12.2.md` R5 — *The panel names the ref the base came from
  beside the commit … a ref too long for the row says so*. Still true in
  substance (the ref is beside the commit, one row down, and still elided);
  the anchor drifts. Re-read and re-stamped in place with a dated note, its
  text corrected where it names a `from` row.
- `seal/releases/0.15.1.md` G2 — *`panel` carries a `gate` row beside
  `from`, `tree <version>` where … and `plugin <version>` …*. False after
  S3: the row is conditional and `plugin` never prints. Corrected in place
  with a `Corrected <date>` note; the new claim is a row in this item's
  fragment.
- `seal/releases/0.15.7.md` N5 — *the values file holds exactly `panel`'s
  rows … beside the tree, base, ref, item, session and scale*. Still true
  and two keys short; re-read, the list extended with a dated note.
- `seal/releases/0.12.2.md` G6, `seal/releases/0.15.4.md` S3 and C4 — the
  count on the panel and the names on the stream; the two arms left out at
  `main`. Their claims hold; `evidence-check` says whether their anchors
  moved, and each row that drifts is re-read.

Rows this work adds — one per S1 to S6 unit, anchored on the unit — go in
`seal/ledger/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run.md`.

## Open questions → questions.md

Every judgment the ticket left open that the tree could answer is answered
above and listed at the head of `questions.md` so nobody reopens it. One row
there needs a person and carries a default the build proceeds on under the
pressed `automation`; the rest are a measurement's or the work's.

Framed 2026-10-01 by framer, before the build.
