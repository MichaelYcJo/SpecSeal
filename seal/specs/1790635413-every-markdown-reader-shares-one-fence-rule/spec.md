# Feature Specification: every markdown reader shares one fence rule (#584)

<!-- seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A marker counts only on a live line, and one function decides what live means* | "Every reader of the fold record and of the ledger's own sections asks the same function." `fold_ledger.py`'s marker readers read the ledger's own section markers, and `gather_changelog.py`'s read the same `<!-- specs/<id> -->` marker that `survivor_check.py#gathered_fragments` already reads through `unverified_check.py#live_lines`. So every marker reader in scope asks `live_lines`. This clause decides it; no direction argument is needed on top. |
| `docs/the-evidence-ledger.md` §*A retirement would break every ledger row anchored inside the directory it removes* | States the ledger's direction rule: the checker skips a fence that closes, and reads the rest. `correction_check.py#rows` reads ledger rows, so it takes the same rule the checker takes (`closed_fence_lines`). A row inside a comment is still read. |
| `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row* | One rule is consumed by every walk of the `\| Item \| Value \|` table: the reader, the refusal, and the writer. The comment half added here goes through that same single walk, and the clause gains the comment sentence. |
| `docs/issues-and-milestones.md` §*A keyword inside a fence or a code span claims nothing* | Says on purpose that a closing-keyword fence opens "at any indent". That is why `close_issues_on_release.py` stays out (see *The class*). |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Phases 1, 2 and 6 change a gate's verdict (`fold_ledger.py --check`, `gather_changelog.py --check`, `broad-gate` and the config readers). Each carries a test seen red, a stated failure direction, a prompt budget and a platform note. |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New claims go to `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md`. Existing rows anchored on a unit this work edits are re-read and re-stamped in the file they live in (listed under *Data & interfaces*). |
| `skills/agent-contract/SKILL.md` §12 | A defect belongs to a class. The class below was enumerated from the tree, not from the issue's list. |
| `skills/agent-contract/SKILL.md` §14 | Phase 6 adds a sentence a person reads. It is documented and pinned in the same commit. |

The issue lists five readers and its comment adds two. The milestone
(`gh api repos/MichaelYcJo/SpecSeal/milestones/49`) places this item as B: it
runs in parallel with A (#585, `evidence_check.py`) and D (#28,
`hooks/dispatch.py`), and C follows A in `evidence_check.py`.

## Scope

### The class, enumerated

A reader is in the class when it walks markdown lines and decides whether a
line is a row, a marker, a heading or a rider, and it decides that with a
fence or comment rule of its own, or with none where a reader of the same
file already has one. The class was enumerated on 2026-09-29 with `git grep`
for fence and comment tokens over every `.py` file, `tests/` included, and
for table-row walks (`startswith("|")`) over `hooks/`, `skills/`, `.github/`
and `bin/`. Each hit was then read.

**In scope:**

| Reader | Its rule today | What it adopts | Phase |
|---|---|---|---|
| `.github/scripts/fold_ledger.py#demote` | ```` ``` ```` or `~~~` by `startswith`, closed by any line starting with the same three characters. Its own `# RIDER:` says so | `fence_opener` / `fence_closes`. An unclosed block still runs to the end, as today. The rider is retired, because its condition is met | 1 |
| `fold_ledger.py#is_marked` (and `#folded` through it), `#doubled_markers`, the `--check` count in `#main` | none: a line-anchored regex over the whole text | `live_lines`, by the grounding clause above | 1 |
| `fold_ledger.py#version_headings` (which `#misnamed`, `#doubled_versions` and `--check`'s `headed` read), `#section_heading`, and the walk to the next `## ` in `#insert` | none | skip the lines inside a fence span (`fence_spans`, an unclosed block to the end). `demote` copies a fenced `#` line byte for byte into the release file. A heading reader that then reads that line as `## X.Y.Z` contradicts what `demote` just decided, and `--check` refuses the fold `demote` wrote | 1 |
| `.github/scripts/gather_changelog.py#ungathered` and the `--check` count in `#main` | the count is a line-anchored regex. `ungathered` is a SUBSTRING test, so a marker quoted in prose, a fence or a code span marks a fragment gathered | `live_lines`, so this command and `survivor_check.py#gathered_fragments` read one file's markers by one rule | 2 |
| `.github/scripts/rider_check.py#comment_blocks` | its own HTML comment walk, no fence state | in a `.md` file, a line inside a fence span (unclosed to the end) opens no rider and changes no comment state. Other file types are unchanged. `#region_lines` reads the blocks this returns, so the hash agrees without its own edit | 3 |
| `skills/evidence-check/scripts/correction_check.py#rows` | none: every `\|` line is a row | skip the rows inside a fenced block that closes (`closed_fence_lines`), the ledger's rule. A commented row is still read | 4 |
| `skills/verify/scripts/payload_meter.py#FENCE` / `#heading_starts` | `^\s*` (any indentation), and any delimiter line of the right character and length closes, info string or not | `fence_opener` / `fence_closes` | 5 |
| `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings` | a copy of `payload_meter.py`'s rule | the same rule. Its docstring says it applies "the same rule `payload_meter.py#heading_starts` applies", so the two move together or that sentence is false | 5 |
| `hooks/config.py#fence_map` / `#unfenced`, comment half | no comment state: a row inside a multi-line HTML comment is read | a line inside an HTML comment **that closes** is not shown to the table walks. The hook keeps its own copy (see *How the hook reaches the rule*) | 6 |
| `skills/verify/scripts/broad_gate.py#fenced_row_at` and the refusal it feeds | takes the complement of `unfenced` and calls every hidden `Broad gate` line "inside a code fence" | once phase 6 hides commented lines, a `Broad gate` row that stands only inside a comment is named as that, not as fenced and not as absent | 6 |

**A shape where the old rule is already wrong in the shipped tree.**
Line 443 of `skills/evidence-check/SKILL.md` is a line of prose that happens
to begin with a run of four backticks, and more backticks follow later on the
same line. Under `payload_meter.py#FENCE` and the test's copy, that line opens
a fence and hides the headings after it. Under `fence_opener`, a backtick
opener whose info string holds a backtick opens nothing. Read on 2026-09-29,
not executed. Q2 measures what it changes.

**Out of scope:**

| Reader | Why it is out | Who answers what is left |
|---|---|---|
| `hooks/config.py#FENCE`, the fence half | Already CommonMark 4.5 in full and held to the shared rule, shape by shape, by `tests/test_unverified_rows_close.py#test_the_fence_rule_agrees_with_the_config_reader` (S6 of `1790260566`). Nothing to bring over | nothing left |
| `.github/scripts/close_issues_on_release.py#FENCE`, and `issue_claims_check.py` and `label_merged_on_release_branch.py` through it | It reads a pull request body against GitHub's own reference rule, and opens a fence at any indent on purpose so a fence under a list item masks a keyword. `docs/issues-and-milestones.md` chose that direction (grounding row 4). `fence_opener`'s three-space bound would un-mask those and close issues on quoted examples | nothing left |
| `skills/code-review/scripts/round_record.py#fenced_after` | Keeps a wider opener on purpose, so a fix fenced inside a list item still reaches the record, and keeps a vendored copy for the copy `evidence-ci` puts alone in a user repository (`fence_opener`'s docstring) | nothing left |
| `skills/evidence-check/scripts/evidence_check.py` | Already asks the shared rule through `#fence_rule`. It is also A's file. One comment in it (the `READER` block above `VENDORED_FENCE_RE`) says `fence_opener`'s docstring names "the readers #584 has not brought over yet". Phase 7 rewrites that docstring so the pointer still resolves, and leaves the word "yet" standing | work item C (#508 + #387), which edits that file next in this release |
| `gather_changelog.py#insert` and `#section_lines`, `publish_release_note.py#section_body` | A released section ends at the next `## ` line for both readers, and their predicate is deliberately the same (#586, `SECTION_LINE`'s comment). A fragment carrying a `## ` line is refused before anything is written, fenced or not, so a fenced one never reaches the file | nothing left |
| `fold_ledger.py#release_sections`, `#body_rows`, `#rewrite_self_anchors` | Read by `--split` alone, a one-time migration this repository has taken: `seal/releases/` exists and `seal/ledger.md` heads no release (0 lines matching `^## X.Y.Z`, counted 2026-09-29) | nothing left |
| `.github/scripts/claude_block.py` | Reads two exact whole-line markers that it writes itself | nothing left |
| `hooks/routing.py#table_rows`, and the `--exempt` file reader in `survivor_check.py#main` | Neither keeps a fence or comment rule of its own, and no in-scope reader reads their files, so nothing here disagrees with them. Giving `routing.py` a rule changes what the commit gate reads from every declaration already written, on the hook path D is changing in parallel. No instance has been reported | the orchestrator, who files an issue for readers with no fence state at all |
| `tests/test_release_hygiene.py#overwide_rows` | A (#585) decides whether this reader becomes an arm of `evidence_check.py`. Editing it here collides with that decision | work item A |
| `tests/test_docs_line_wrap.py` and `tests/test_handoff_outlives_the_merge.py` (their fence toggles) | Repository tests over this repository's own prose. A misread fails or passes this repository's CI in front of its author, and no consumer's verdict rests on it | the orchestrator, in the same issue as `routing.py` |
| The independent walk in `tests/test_unverified_rows_close.py` (around `block_ends_at`) | An oracle is kept independent of the rule it checks on purpose | nothing left |
| `readable`'s pass order (comments before fences) | Out for the reason `1790260566` gave: `round_record.py` refuses each crossing shape with a named message | nothing left |

### How the hook reaches the rule — it does not, and the copy is held

`hooks/config.py` runs inside `hooks/mode-gate.py`, a `PreToolUse` hook on
every Bash call, in a new process each time (`hooks/hooks.json`). Loading
`unverified_check.py` there would be paid on every command in every
consumer's session, and `fence_opener`'s docstring already records that
reason for the fence copy. Loading it would also make a hook's life depend on
a skill module while D (#28) decides what a hook's load failure does. So the
hook imports nothing new, and its copy grows by the comment half.

The copy stays honest the way the fence half does: the parity test is
extended with comment shapes, and its oracle is composed only of
shared-reader functions: `comment_scan` over the lines `blank_fences` leaves,
with a line hidden only where its comment closes. What the copy does not
model is therefore exactly what the oracle does not model. A `<!--` inside a
code span is read as an opener, as `comment_scan` and every reader through
`readable` already read it.

Moving the rule into a module under `hooks/` was considered and rejected in
`plan.md` §*Alternatives considered*.

### The direction of each change

- **Marker readers** (`fold_ledger.py`, `gather_changelog.py`): a marker
  counts only on a live line. A marker parked by mistake reads as not folded
  or not gathered, which a person sees at `--check`. The residual, stated
  rather than found: a ledger file with a fence that never closes hides every
  marker below it, so `is_marked` and `doubled_markers` cannot see a second
  fold of a fragment whose marker is down there. That needs a fragment
  folded before to come back AND an unclosed fence in a ledger file. Neither
  exists today (0 fence lines in `seal/ledger.md`, `seal/releases/*.md` and
  `CHANGELOG.md`, counted 2026-09-29).
- **`correction_check.py#rows`**: fewer rows are read, so fewer losses are
  reported. A row the checker reads (an unclosed fence, a comment) is still
  watched, so the two cannot disagree about which rows exist.
- **`rider_check.py`**: toward silence, the direction its own docstring
  requires. A quoted rider stops reading as BROKEN at exit 2.
- **`hooks/config.py`**: fewer rows. A commented row is not an answer
  somebody gave, which is the module's own stated direction. An unclosed
  comment hides nothing, so no file that reads today stops reading. The
  prompt budget does not grow: `mode-gate` asks only where the `Mode` row
  stood inside a closed comment, which is *nobody declared*, and that is
  inside the existing budget of two per session per repository.
- **`payload_meter.py` and its test**: a meter, and a repository test. No
  verdict in a consumer's repository.

### Assumed, not asked

- `gather_changelog.py`'s change from a substring test to a line-anchored
  live marker changes no current answer. `CHANGELOG.md` carries 140 markers
  on a line of their own and 145 substring occurrences. The five extra are
  `<!-- specs/<id> -->` and `<!-- specs/<work-item-id> -->` quoted in prose
  (lines 874, 1516, 1521, 7131, 7175), which name no work item. Counted with
  `grep` on 2026-09-29.
- No shipped markdown file carries a `RIDER:` inside a fence today. An `awk`
  approximation of the fence rule over every `.md` under `RIDER_ROOTS` found
  none on 2026-09-29, so phase 3 changes no current rider count. Phase 3
  re-measures with the real rule.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · `demote` keeps a longer fence | Given a fragment with a ```` ```` ```` block quoting ```` ``` ```` and a `## area` line after the inner delimiter, when `demote` runs, then the `## area` line inside the block is copied unchanged and the heading after the block is demoted | a case in `tests/test_the_ledger_fragments_fold_at_release.py`, seen red against `demote`'s three-character rule |
| S2 · `demote` does not close on an info string | Given a ```` ``` ```` block containing ```` ```python ```` and then `# x`, when `demote` runs, then `# x` is copied unchanged | a case beside S1, seen red |
| S3 · a quoted marker is not a fold | Given a release file whose only `<!-- specs/<id> -->` for a fragment's id stands inside a closed fence, when `fold_ledger.py --version` runs, then the fragment folds rather than being refused as already folded | a case, seen red |
| S4 · a quoted marker is not doubled | Given a ledger file with a real marker and the same marker inside a closed fence, when `fold_ledger.py --check` runs, then no doubled marker is reported and the printed count is one | a case, seen red |
| S5 · a fenced version heading is no heading | Given a release file `0.1.0.md` heading `## 0.1.0` with a fenced example holding `## 0.2.0`, when `--check` runs, then the file is not reported misnamed | a case, seen red |
| S6 · a quoted marker gathers nothing | Given `CHANGELOG.md` with `<!-- specs/<real id> -->` only inside a fenced block, or only inline in prose, when `gather_changelog.py --check` runs, then that fragment is reported not gathered | a case per shape, seen red |
| S7 · the two changelog readers agree | Given S6's file, when `gather_changelog.py` and `survivor_check.py#gathered_fragments` read it, then they name the same set of gathered ids | a case asserting equality |
| S8 · a quoted rider is not a rider | Given a `.md` file under a rider root with ```` ``` ```` / `<!-- RIDER: x -->` / ```` ``` ````, when `rider_check.py` runs, then no rider is reported for it and the exit code is 0 | a case in `tests/test_a_rider_reaches_its_file.py`, seen red (BROKEN at exit 2 today) |
| S9 · a Python rider is unchanged | Given a `.py` file holding a line of three backticks and a `# RIDER:` block after it, when `rider_check.py` runs, then the rider is read | a case that passes before and after (pins the scope) |
| S10 · a fenced ledger row is no row to lose | Given a parent and a merge result whose only difference is a `Re-read <date>` marker dropped from a row inside a closed fence, when `correction_check.py` reads them, then no loss is reported | a case in `tests/test_a_merge_cannot_silently_drop_a_correction.py`, seen red |
| S11 · a row under an unclosed fence is still watched | Given the same shape with the fence never closed, when `correction_check.py` reads it, then the loss is reported | a case that passes before and after (pins the direction) |
| S12 · the meter splits by the shared rule | Given a skill with a prose line that begins with four backticks and holds more backticks later on the line, then a `## H` heading, when `payload_meter.py#heading_starts` and the test's `headings` read it, then both find `## H` | a case per reader, seen red |
| S13 · a commented config row is not a row | Given `config.md` whose table has a multi-line HTML comment holding `\| Broad gate \| old \|` above the live row, when `config_rows` reads it, then only the live row arrives | a case, seen red |
| S14 · an unclosed comment hides nothing | Given `config.md` with a `<!--` never closed above the table, when `config_rows` reads it, then every row arrives as today | a case that passes before and after (pins the direction) |
| S15 · the writer agrees with the reader | Given S13's file, when `seal mode` writes the `Mode` row, then it writes into the live table and leaves the commented line byte-identical | a case, seen red |
| S16 · the comment copy agrees with the shared rule | Given a table of comment shapes, when `hooks/config.py` and the oracle composed of `comment_scan` and `blank_fences` read each shape, then they agree about which lines are hidden | the parity test extended, one case over the table |
| S17 · the gate names a commented row | Given `config.md` whose only `Broad gate` row is inside a closed comment, when `broad-gate` runs, then it refuses naming the row as commented out, not as fenced and not as absent, and runs nothing | a case in `tests/test_the_seal_is_taken_once_by_the_sealer.py` pinning the sentence, seen red |
| S18 · a copied script still says what is missing | Given `payload_meter.py` or `correction_check.py` copied without the reader it now loads, when it reaches the loader, then it exits 2 with a sentence naming the file | rows added to `tests/test_a_script_copied_alone_exits_2.py#CASES`, seen red |

## Data & interfaces

- **How each reader reaches the rule.** `fold_ledger.py` already loads
  `unverified_check.py` (`#load_reader`); it reads `fence_opener`,
  `fence_closes`, `fence_spans` and `live_lines` off that module.
  `gather_changelog.py` loads it the same way. `rider_check.py`,
  `correction_check.py` and `payload_meter.py` each load it by path with
  their own existing loader shape, and the two shipped ones (`correction_check.py`,
  `payload_meter.py`) exit 2 with a sentence when it is missing (S18). The
  test reads it the way its neighbours in `tests/` do. `hooks/config.py`
  loads nothing new.
- **`hooks/config.py`.** The three table walks (`config_rows`, `refusal`,
  `seal.py#table_span`) keep reading through ONE generator, and that
  generator hides commented lines as well as fenced ones. `fence_map`'s
  second value (an unclosed fence) is unchanged. `broad_gate.py#fenced_row_at`
  stays a question about fences alone. A second question beside it names a
  row inside a comment. Names and shapes are the work's to choose.
- **`fence_opener`'s docstring** lists the readers that ask it. Each phase
  moves its reader into that list. Phase 7 rewrites the paragraph that names
  "the readers #584 names", so what stays apart is listed with its reason.
- **Messages.** One new refusal sentence in `broad-gate` (S17), pinned.
  No new flag and no new exit code. Every other change is a changed verdict
  or count, each pinned by its scenario.
- **Ledger rows this work drifts**, re-read and re-stamped where they live
  (counted from `seal/ledger.md` and `seal/releases/*.md`, 2026-09-29):
  `fold_ledger.py#main` (6), `#folded`, `#MARKER_LINE_RE` (2 each);
  `gather_changelog.py#main` (4), `#ungathered`, `#marker` (2 each);
  `hooks/config.py#fence_map`, `#config_rows` (2 each);
  `unverified_check.py#fence_opener` (2);
  `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings` (1).
  The phase that edits a unit re-reads its rows.

## Open questions → questions.md

No row needs a person. Q1 and Q2 are measurements. Q3 and Q4 are the work's.

Framed 2026-09-29 by framer, before the build.
