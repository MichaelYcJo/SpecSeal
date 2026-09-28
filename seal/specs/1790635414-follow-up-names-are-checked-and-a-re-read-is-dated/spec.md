# Feature Specification: follow-up names are checked, and a re-read is dated

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone 49 (0.16.0), item C: issues #508 and #387, two behaviours of
`evidence-check` that a consuming repository sees. Both edit
`skills/evidence-check/scripts/evidence_check.py`, the file item A (#585) is
editing in parallel, so the build starts on the release branch after A's
squash (`plan.md` phase 1).

**The owner answered #387's question before this frame** (read: the caller's
spawn prompt, and `routing.md` §*Why this way*). `--reverify --checked <date>`
writes that date into the `Checked` cell of every row whose hash it moved.
Without the flag, the date is left alone, and the output names the rows whose
hash moved while their date was left. A row whose hash did not move is never
touched, with or without the flag. This spec builds that answer and does not
reopen it.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | #508's measured instance was caught by grepping by hand. A check that reads the file replaces that, and it asks nobody anything |
| `CLAUDE.md` §*Repo rule — commit early* (the paragraph beginning "The `Checked` column holds the date somebody read the code") and `templates/ledger.md` §*<spec area>*'s preamble | Define re-verifying as two acts, re-reading and then `--reverify`. This work makes the second act able to record the first. Both documents are corrected here (D1) |
| `CLAUDE.md` §*Repo rule — a change writes fragments* and `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* ("Appended is the word") | A shared-file row that an edit drifted is re-read and re-stamped **in the file it stands in**, with a dated note. `--checked` is how the date lands in that row, so this work's own re-stamps use it (phase 4) |
| `docs/the-evidence-ledger.md`, the statement headed "A `\|` inside a ledger cell is escaped" | "A row under no header is counted against the five columns `templates/ledger.md` declares." This is the grounds for where the date cell sits in a fragment row (R4) |
| `docs/the-evidence-ledger.md`, "A work item whose ledger fragment still exists has not shipped" | The boundary stays as it is. `seal/follow-up.md` lies outside it by lifetime rather than by date: it is permanent, and a row leaves it when the item is done, so every row is live (F3) |
| `seal/follow-up.md`'s header | Every row names a person and is read months after it was written. Anything tied to a coordinate is a `# RIDER:`. `tests/test_a_rider_reaches_its_file.py#test_no_schedulable_row_carries_a_coordinate` forbids the old `file.py:120` shape only, so `path#name` in a row stays legal and becomes checked (P1) |
| `skills/implement/SKILL.md` §1 ("Read `seal/follow-up.md` before starting") | Row 69 of that file is about `--reverify` stamping rows nobody read. This work makes that failure write a date, so the row is in scope (D3) |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The checker is what `broad-gate` and CI's `ledger` job run. This change refuses more, so it owes a case seen red, a stated failure direction, a prompt budget and platform honesty (§*What a gate change owes*) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The documents describing either behaviour form a class, and it is enumerated in D1–D2. Every new line of output is pinned in the commit that adds it, and every new case is seen red |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | Fixtures use neutral paths and names |

## What was measured before the frame, and by whom

Every figure below was taken in this framer at `1f218ae6`. A read-only
extraction in the scratchpad imported the checker's pure helpers
(`claim_lines`, `stated_names`, `tree_names`, `resolve_unit`). It never
called `main`, so no check's verdict is being reported here.

| # | Fact | Label |
|---|---|---|
| M1 | `seal/ledger/` does not exist in this tree, so the records arm reads no work item today: 0 live | read (`ls`) |
| M2 | `seal/follow-up.md`'s claim lines carry 8 compound bare names. None of them is absent from the corpus, and none becomes absent once `seal/follow-up.md` is taken out of the corpus | executed |
| M3 | `seal/follow-up.md` carries 11 backticked `path#name` spans. Ten have a path that resolves from the root, and each such name is both a unit (`resolve_unit`) and a token of its file. One, `gather_changelog.py#ungathered`, has a bare file name that does not resolve from the root, and its name is in the corpus | executed |
| M4 | Every record under `seal/specs/`, shipped ones included, carries 791 `path#name` spans. 424 resolve a file: in 420 of them the unit is found; the other 4 are two spec lines proposing constants that were never built (history) and two `tests/test_unverified_rows_close.py#block_ends_at`, a nested function that the unit rule misses and the token rule finds. 367 do not resolve: 356 are bare file names and 11 are example or fixture paths. The bare-name fallback finds 2 of the 367 absent from the corpus, one of them a single word. 140 of the 791 names carry no underscore | executed |
| M5 | `Checked` cells over `seal/ledger.md` and `seal/releases/*.md`: 701 hold one date and 29 hold a list of dates. All 34 separators between dates are ` · `. The `Re-read <date>` and `Corrected <date>` markers sit in the Notes cell, not in `Checked` | executed |
| M6 | Anchors by the table they sit in: 2460 under a `Checked` header, 203 under a `Date` header (release files 0.5.0, 0.12.0–0.12.3, 0.13.0), 310 in 67 rows under no header (every one five cells wide, with a date-shaped fourth cell), and 0 outside a table row | executed |
| M7 | Rows in `seal/ledger.md` and `seal/releases/` citing units this work will edit: `reverify` 6, `claim_lines` 4, `main` 3, `exit_code` 3, `unshipped` 2, `tree_names` 2, `check_records` 2, and one each for `stated_names`, `compound` and `built_name` | read (`git grep`) |
| M8 | `rider_check.py --reverify` writes today's date on a rider, and only where the hash moved. `tests/test_a_rider_reaches_its_file.py` pins that a date whose content did not move is left | read |

## Scope

**In.**

1. **#508, first half — `seal/follow-up.md` is read by the records arm**
   (F1–F8). It is read on every run, whether or not a work item is live,
   under the same claim rules a record gets. It is taken **out of** the name
   corpus, because otherwise the row naming a name would be the evidence that
   the name exists.
2. **#508, second half — a name written as `path#name` is checked** (P1–P7).
   Where the path resolves, the name has to be a token of **that file**.
   Where it does not resolve, the name half is read as a bare name, under the
   bare-name rule.
3. **#387 — `--reverify --checked <date>`** (R1–R9), to the owner's answer
   above. It covers where the date cell is, what is written into it, which
   dates are refused, and what is said when the flag is absent.
4. **The RIDER in `skills/evidence-check/scripts/evidence_check.py#reverify` is
   removed.** It asks exactly #387's question ("refuse … or print the ones it
   left"), and this work answers it. `seal/follow-up.md`'s header rule for a
   rider says: do what it asks, then delete it.
5. **Every document that describes either behaviour** (D1–D3), both README
   editions included.
6. **The ledger stays true.** Shared rows this work drifts are re-read and
   re-stamped in their own files with the new flag. New claims go into
   `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md`,
   and the release note goes into this directory's `changelog.md`.

**Out, and why.**

- **The check report naming every row rather than every coordinate**, the
  first option in `seal/follow-up.md` row 69. It changes what the check
  prints, the row puts it to the owner, and nothing in #508 or #387 asks for
  it. D3 narrows the row and does not close it.
- **Other permanent files under `seal/`** (`README.md`, `config.md`). #508
  names `seal/follow-up.md` alone. `seal/README.md` is a copy of
  `templates/seal-README.md`, and its names are the template's.
- **Names in `docs/`, `CHANGELOG.md` and the prose of shipped ledger files.**
  Policy and history, and not what either issue is about. They stay in the
  corpus as they are.
- **Quoted locators in coordinate form** (`path#"a heading"` with no hash)
  **and `path#name>"minor"` with no hash.** Neither appears in
  `seal/follow-up.md`, and a quoted locator is not a name. A span that
  carries `@hash` is a stamp, and the stamp half already reads it.
- **Resolving a bare file name by searching the tree for its basename.**
  There are 356 such spans in the records (M4). The fallback reads their name
  half against the corpus, which is what the issue asks for ("where the path
  part resolves"). Resolving by basename is a second resolution rule, with
  its own ambiguity to argue.
- **`rider_check.py`.** It already dates what it re-stamps (M8). The two
  tools differ on purpose: a rider's date is written automatically, and the
  owner chose an explicit flag for the ledger.
- **`unread_items`' own RIDER**, on the unlistable-`specs/` count. It sits in
  the same file, but its class is unrelated and this work does not touch that
  function.
- **The commit advisor** (`hooks/evidence-advisor.py`). It imports the ledger
  arm only; M7's `git grep` finds no call to `check_records` outside the
  checker and its tests. Its `--reverify` remedy line stays true.

## User scenarios & acceptance *(mandatory)*

Each case in the build is seen red before it is committed (§15), either
against the checker at the rebased base or with the pinned sentence deleted.
Fixtures are temporary repositories with no git, the way
`tests/test_a_record_states_what_the_tree_has.py` builds them. New cases for
F and P go in that file. New cases for R go in
`tests/test_a_row_points_by_content.py`, beside §*re-verifying*.

### #508 — `seal/follow-up.md` is read (F)

| # | Given / When / Then | Verifiable how |
|---|---|---|
| F1 | Given a `seal/follow-up.md` row naming an invented compound backticked name that no other file carries, when the check runs (lenient or `--strict`), then the name is `NOT-IN-TREE` at `seal/follow-up.md:<line>` and the run exits 2 | a case. Red at the base: the issue measured `0 refused` at exit 0 |
| F2 | Given that same row, the name is refused even though `seal/follow-up.md` itself carries it: the file is out of the corpus. A name that another file carries passes | a case, plus a mutation that puts the file back in the corpus and turns F1 green |
| F3 | Given no `seal/ledger/` at all (no live work item), `seal/follow-up.md` is still read | a case. Red at the base, which returns early with nothing live |
| F4 | Given no `seal/follow-up.md`, nothing is refused and nothing raises. Given one that cannot be read, it is `UNREADABLE` and the run exits 2, the way an unreadable record is | two cases |
| F5 | The claim rules are the records' own: `NAME NOT IN TREE` exempts the line; a closed fence is a quotation; a comment that begins a line is an aside; a never-closed region is read | one case per rule, or one parametrised case |
| F6 | In local mode, `<git-common-dir>/seal/follow-up.md` is read and is out of the corpus, with the same answers as shared mode | a case beside `test_the_gathered_ledger_is_in_the_corpus_in_local_mode_too` |
| F7 | A record refusal's detail names every place the corpus leaves out: `seal/specs/`, `seal/ledger/` and `seal/follow-up.md`. The records heading and the summary line say whether `seal/follow-up.md` was read | the texts pinned (§14). A case asserts the summary line for present and for absent |
| F8 | This repository's own tree stays at zero refused, now with `seal/follow-up.md` read | the existing `test_this_repositorys_own_records_state_nothing_the_tree_lacks`, unchanged, green after the rebase (M2, M3; `questions.md` Q1) |

### #508 — `path#name` is checked (P)

| # | Given / When / Then | Verifiable how |
|---|---|---|
| P1 | Given a record or follow-up line with a backticked `path#Name`, `path#Name()` or a dotted `path#Class.method`, where the path is spelled as a ledger coordinate's path and resolves through the ledger's own `place` to a readable file: when a segment of the name is not a token of that file, it is `NOT-IN-TREE`, and the detail names the path | a case per place (record, follow-up). Red at the base, where the span is skipped (issue table, row 4) |
| P2 | The same form passes when the file carries the name. It is refused when only **another** file carries the name | two cases |
| P3 | With a resolved path, a name with no underscore is checked too. The path is what makes it a claim | a case with a one-word invented name, red when the compound narrowing is applied to this form |
| P4 | Given a path that does not resolve (a bare file name, a missing path, a path escaping the root), the name half is read exactly as the bare backticked name would be: compound rule, whole corpus | a case with a bare file name and an invented compound name (refused), and one with a one-word name (not read) |
| P5 | A span carrying `@hash` is read by the stamp half only, and never counted as a name as well | a case asserting the counts |
| P6 | The claim rules of F5 apply to this form too | covered with F5's fixture |
| P7 | `N names read` counts coordinate-form names | the count asserted in P1's case |

### #387 — a re-read is dated (R)

| # | Given / When / Then | Verifiable how |
|---|---|---|
| R1 | Given a row whose hash `--reverify --checked D` moves: the hash is rewritten as today, and the row's date cell gains D. A cell holding dates gets ` · D` appended; an empty cell becomes D; a cell already ending in D is left as it is. The run names each row it dated | three cases (append, empty, idempotent) |
| R2 | A row none of whose hashes moved is byte-identical afterwards, with or without the flag, and is not named | a case over a two-row ledger, one row moved and one not, run both ways |
| R3 | Without the flag, the hash moves and the date cell is byte-identical. After the count line the run names each such row by its ledger file, its first cell (the label `skills/settle/scripts/settle.py#first_cell` gives a row) and its date cell as it stands, with a remedy naming `--checked`. The exit code is what it would have been without the block | a case. The lines are pinned (§14) |
| R4 | The date cell is the column headed `Checked`; failing that, the column headed `Date`; under no header, the fourth cell of a five-cell row. Under `--checked`, a row with a moved hash and no date cell found is **left whole**, hash included, and named on a `LEFT` line; the run exits 1 | a case per header kind (M6), and one for a row with no date cell |
| R5 | `--checked` takes `YYYY-MM-DD` only: four, two and two digits, a real calendar date, and not later than the local date the run is on. Anything else (`2026-9-1`, `20260929`, `2026-02-30`, `today`, tomorrow's date) is refused with exit 2 before any ledger is read. `--checked` without `--reverify`, and beside `--migrate`, is refused the same way, by name | a parametrised case asserting exit 2 and that the fixture ledger is byte-identical |
| R6 | A row re-anchored by the heal path (`identical content`) has a moved hash, so it is dated under the flag and named without it | a case beside the existing heal case |
| R7 | A row with several coordinates is dated once, however many of them moved | a case |
| R8 | A row in a fenced block that closes is never touched (#444 unchanged) | the existing case, green |
| R9 | The RIDER on `reverify` is gone, and `rider_check.py` reads the tree clean | `grep` shows no rider in the function, and `rider-check` is left for the broad gate |

### Documents (D)

| # | Given / When / Then | Verifiable how |
|---|---|---|
| D1 | Every document that tells a reader to re-read and then run `--reverify` says what `--checked` records. It also says that the flag asserts **every** row whose hash moves was re-read, so each row citing a drifted coordinate is read first, or the write is narrowed with `--ledger`. The class, enumerated: `CLAUDE.md` (the `Checked` paragraph); `templates/ledger.md`; `docs/the-evidence-ledger.md` ("Appended is the word"); `skills/evidence-check/SKILL.md` (§*Run*'s block and flag table, §*Re-verifying is recomputing the hash*); `README.md` **and** `README.ko.md` (the re-verifying sentence in each); `CONTRIBUTING.md` §*House rules* (the three answers); `skills/implement/SKILL.md` §2; `skills/code-review/orchestration.md` (the writing form); `docs/release-checklist.md` (the `evidence-check --strict` row); `skills/settle/SKILL.md` (the re-verify sentence); and the checker's module docstring *Usage*. A mention of `--reverify` as a **rename heal** (`README*.md`'s migration block, `CONTRIBUTING.md`'s "Renamed a cited symbol", `hooks/evidence-advisor.py`, `hooks/root-migrate.py`) claims no reading and stays as it is | read in review. A pinned phrase per document where one exists |
| D2 | Every document that describes what the records arm reads or refuses names `seal/follow-up.md` and the `path#name` form: `skills/evidence-check/SKILL.md` (the `NOT-IN-TREE` verdict row, §*The records arm*); `templates/evidence-check.yml`'s comment; `skills/code-review/SKILL.md` (the marker paragraph); `agents/warden.md` (the paragraph on names a report writes, since a reviewer writes `path#name` constantly); `CONTRIBUTING.md` §*The two checks that can ask you for something you do not have* (the ledger job now refuses a stale follow-up name too, and a contributor says so on the pull request); and the checker's own comments and docstrings | read in review |
| D3 | `seal/follow-up.md` row 69 gains a dated note. `--reverify` now names every row whose hash it moved; the documents now carry the row's third option (*read every row that cites it*); and `--checked` turns an unread re-stamp into a false date rather than a stale one. What stays open is the row's first two options, and its answerer is unchanged | read in review |

## What a gate change owes (`CONTRIBUTING.md`)

- **Failure direction: it blocks more.** A stale name in `seal/follow-up.md`,
  or a wrong `path#name` in a live record, is now exit 2 in every reader. A
  false refusal costs one correction or one `NAME NOT IN TREE`, at the commit
  or pull request that caused it. A false allow is #508's measured instance:
  a row naming a case in no file, found months later by grepping. `--checked`
  refuses nothing new and adds a `LEFT` for one shape (R4).
- **Prompt budget: zero.** Nothing asks a person anything. The checker
  refuses, and a writer's flag is typed by whoever runs it.
- **Platform.** Paths go through `place` and `contained`, and every printed
  coordinate goes through `built_name`, whose `ntpath` flavour lets a POSIX
  machine exercise Windows separators. A follow-up refusal's coordinate is
  built, so it takes the same route. The date check compares against the
  local date and reads no platform API. What CI's three legs say is
  `unverified` until they run (the pull request).

## Data & interfaces

- **CLI.** `--checked DATE`, valid with `--reverify` only (R5). No other flag
  changes.
- **Output.** `--reverify` gains a block naming the rows whose date was left
  (no flag) or the rows it dated (flag), and `LEFT` lines for R4. The records
  heading and the summary line say whether `seal/follow-up.md` was read (F7).
  A coordinate-form refusal's detail names the path (P1). The wording is the
  build's (`questions.md` Q3); what each line has to carry is fixed above.
- **Exit codes.** Unchanged for the check, except that the new refusals are
  `NOT-IN-TREE` or `UNREADABLE`, which are already exit 2. For `--reverify`:
  without the flag, as today. With the flag, 1 also for a row R4 left, and 2
  for a refused `--checked` (argument error, nothing read).
- **`check_records`' return** stays the three-tuple its many call sites read.
  Follow-up names are counted in `names read`, and the summary line learns
  about the file from `main`, the way the `unread` count already does.
- **Ledger coordinates** for the new claims go in this work item's fragment
  as each phase closes.

## Open questions → questions.md

No row blocks the build. `questions.md` lists the judgments this frame made
from the tree, so nobody reopens them, and three rows for a measurement or for
the work.

Framed 2026-09-29 by framer, before the build.
