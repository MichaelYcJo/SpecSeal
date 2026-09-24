# Feature Specification: a reader's fence and comment state (#444, #491, #487, #220)

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A marker counts only on a live line* (the `1790039346` statement) | A line is live when it begins outside a fence, a comment and a code span, and "one function decides what live means". This work keeps `unverified_check.py#live_lines` as that function for the lines that EXCUSE something, and says in writing why the lines that HOLD something are read by a narrower rule (below, *The direction rule*). |
| `docs/the-evidence-ledger.md` §*A retirement would break every ledger row anchored inside the directory it removes* | States that `settle` reads the rows inside a fence "because the checker reads those too". Phase 2 makes that ground false, so the sentence is corrected in the same phase, and the behaviour it describes stays. |
| `docs/issues-and-milestones.md` §*A keyword inside a fence or a code span claims nothing* | States on purpose that a closing-keyword fence opens "at any indent". That reader is out of scope because policy chose the other direction for it (see *The class*). |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Every phase changes a gate's verdict, so each phase must carry a test seen red, a stated failure direction, a prompt budget and a platform note. |
| `CLAUDE.md` §*Repo rule — a change writes fragments* | New claims go to `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md`. An existing row whose anchored unit this work edits is re-read and re-stamped in the file it lives in. |
| `seal/follow-up.md`, the `#444` row and the records-arm aside row | This work is the prerequisite both rows wait on. Phase 2 deletes the first and phase 4 deletes the second (`skills/implement/SKILL.md` §1). |
| `skills/evidence-check/SKILL.md` §*What counts as a claim* | States that a fence is a quotation and an HTML comment is an aside, with no qualification. Phase 4 changes this sentence to match the code (Q1). |

## Scope

### The class, enumerated

The class is a markdown reader that walks lines and decides whether a line is a
row, a marker or a claim. Its fence state or comment state is missing, or does
not follow the format's own rule. Every reader was enumerated with
`grep -rln` for fence and comment tokens over `*.py` outside `tests/` and
`seal/`, and each one was then read (2026-09-24).

| Reader | Fence / comment state today | Shares the defect? | In or out |
|---|---|---|---|
| `skills/evidence-check/scripts/evidence_check.py` — `check_ledger`→`check_text`, `old_format_rows`, `migrate`, `reverify` (the four ledger walks) | none: `ANCHOR_RE.finditer(text)` over the whole file | **yes, #444**: a fenced example row is BROKEN, and the two writers rewrite inside an example | **in**, phase 2 |
| `skills/verify/scripts/unverified_check.py#blank_fences`, and through `readable` it feeds `check_text`, `chain_check.py`, `round_record.py` and `hooks/review-history-guard.py` | fence with `^\s*`, which accepts any indentation, and a closer may carry an info string | **yes, #491** | **in**, phase 1 |
| `unverified_check.py#_liveness` / `live_lines` (`folded_items`, `settle.py#coordinates`) | bounded `FENCE_RE`, but a closer may carry an info string, and a backtick opener whose info string holds a backtick still opens | **yes**, the same delimiter rule one step over | **in**, phase 1 |
| `unverified_check.py#_paragraph_ends_at` | an ATX heading with no indentation bound, while the oracle in `tests/test_unverified_rows_close.py#block_ends_at` is bounded to three spaces | **yes**. #491's round-7 comment names it. The fix it describes is not in this tree (read 2026-09-24) | **in**, phase 1 |
| `unverified_check.py#todo_open_rows` (the shipped copy of `open_rows`, which `settle.py#open_rows` and `open_record_rows` both ask) | none | **yes**: a `drained` line inside a fence or a comment closes the whole file, which is the silent direction for a guard. A fenced example row counts as open | **in**, phase 3 |
| `.github/scripts/fold_ledger.py#open_rows` | none, and a copy of the above | **yes, #487**: two copies and nothing holds them in step | **in**, phase 3 |
| `skills/code-review/scripts/survivor_check.py#gathered_fragments` | none: `MARKER.findall` over `CHANGELOG.md` | **yes**: a marker quoted in a fence excuses a removal. This is the direction `folded_items` already closed for `docs/` | **in**, phase 3 |
| `evidence_check.py#claim_lines` (the records arm: `stated_names`, `stated_stamps`) | fence with `lstrip().startswith`: any indentation, no length, and a closer may carry text. A comment ends at the WHOLE line holding `-->` | **yes, #220**, plus the delimiter rule | **in**, phase 4 |
| `hooks/config.py#fence_map` / `unfenced` (config readers, `seal.py#table_span`, `broad_gate.py#fenced_row_at`) | fence: CommonMark 4.5 in full (a three-space bound, the info-string rule, a closer with no info string) | **no, for fences.** It is the reference the others are brought to. **Comment half: unmeasured** — a row inside a multi-line HTML comment in `config.md` would be read | **out**. The fence half is correct. The comment half has no reported instance, and this reader runs on the hook path. The orchestrator files it as its own ticket |
| `.github/scripts/close_issues_on_release.py#FENCE` and `issue_claims_check.py` | fence at any indent, on purpose | not a defect: policy chose it (`docs/issues-and-milestones.md`, grounding row 3) | **out** |
| `.github/scripts/fold_ledger.py#doubled_markers` and the `--check` count, `gather_changelog.py`'s marker count | none | yes, but only in the loud direction: a false refusal at `--check`, or a count in a report line, which a person sees at the release | **out**. Release automation, loud only. The orchestrator files it |
| `.github/scripts/rider_check.py#comment_blocks` | its own HTML comment walk, and no fence state | yes, loud only: a rider quoted in a markdown fence is read and reported BROKEN | **out**, for the same reason as above |
| `skills/verify/scripts/payload_meter.py#FENCE` | fence at any indent | yes, #491's shape | **out**. It is a meter, not a gate, and a mis-split section changes no verdict. The orchestrator files it |
| `readable`'s pass order (`strip_comments` before `blank_fences`) | a `<!--` inside a fence opens a comment | yes, the comment/fence interaction | **out**. `round_record.py` refuses each such shape with a named message (`COMMENT_CROSSES_A_FENCE` and its two siblings), and `tests/test_chain_hooks.py#reader_blanking_passes` pins the passes |
| `.github/scripts/claude_block.py` | exact whole-line markers that it writes itself | no | out |
| readers under `tests/` | not enumerated | unmeasured | out. They are this repository's own checks over its own documents. Answerer: the work (phase 1's measurement lists any case whose oracle moves) |

### The direction rule, which decides where `live_lines` is the definition

`live_lines` settles an ambiguous line as **not live**. Its docstring says
that bias is chosen "toward keeping a work item's directory". That is the
right answer for a line that **excuses** something, and the wrong answer for
a line that **holds** something:

- **An excusing line** (a fold marker, a `drained` line) counts only when it
  is certainly live. Such a line reads through `live_lines`, unchanged.
- **A holding line** (a ledger anchor, an open evidence-todo row, a claim in
  a record) is skipped only when it is certainly quoted. For a line, that
  means inside a fence that CLOSES. An unclosed fence is read. A comment is
  read in the ledger and in an evidence-todo table. The records arm keeps its
  documented aside rule.

This rule is already the tree's practice in three places, and this work
names it:
`settle.py#anchored_rows` ("a guard that reads fewer lines than the checker
keeps fewer directories"), `claim_lines`'s `held` ("a fence the record never
closes is a malformed record, not a licence to read nothing"), and
`live_lines`'s own bias. So the ONE definition this work creates is the
**fence delimiter**: the rule for what opens a fence and what closes it. It
lives in `unverified_check.py`, the module every reader in scope already
loads, and each walk keeps the state its own question needs.

### In

1. One fence-delimiter rule in `unverified_check.py`, to CommonMark 4.5: at
   most three spaces of indentation, three or more backticks or tildes, a
   backtick opener's info string may not hold a backtick, and a closer uses
   the same character, is at least as long as its opener, and has nothing
   after it but whitespace. `blank_fences`, `_liveness` and
   `_paragraph_ends_at` use it, and `_paragraph_ends_at` also gets the ATX
   three-space bound (#491 and its round-7 comment).
2. The four ledger walks in `evidence_check.py` skip the lines of a closed
   fence and read the lines of an unclosed one (#444).
3. `fold_ledger.py#open_rows` becomes a load of
   `unverified_check.py#todo_open_rows` (#487). `todo_open_rows` takes
   `drained` from a live line only, and reads no row inside a closed fence.
   `survivor_check.py#gathered_fragments` counts a marker on a live line only.
4. `claim_lines` treats a closer as a position: the rest of the line is read
   by the line's own rules. Its fence recognition uses the rule from item 1
   (#220).
5. Documents that state what these readers do are changed in the phase that
   changes the reader: `skills/evidence-check/SKILL.md`,
   `docs/the-evidence-ledger.md` (the sentence in grounding row 2), the
   docstrings of `settle.py#anchored_rows`, `settle.py#coordinates` and
   `todo_open_rows`, and the two comment blocks above `FENCE_RE`.
6. The two `seal/follow-up.md` rows named in grounding row 6 leave that file.

### Out, each with why

- `settle.py#first_cell`: a parallel chain (`1790260563`, #530) edits it.
- A ledger row's cell count: the parallel chain `1790260565` (#501, #568)
  owns it.
- `settle.py#anchored_rows`'s behaviour: its own docstring already decided
  that it keeps reading a fenced row after #444, "the direction to be wrong
  in". Only its future-tense sentence changes.
- The ledger's and the evidence-todo file's comment state: a commented-out
  row is a claim someone parked, and dropping it is the silent direction.
  No ticket reports a false refusal from one, and `templates/ledger.md`'s
  comment carries no anchor. This is written down as an assumption, not
  asked.
- The readers marked **out** in the class table, each for the reason given
  there.
- Whether `_paragraph_ends_at` stays a list of shapes rather than a block
  model (#491's last question). It stays a list, and `questions.md` §*Decided
  from the tree* D5 gives the grounds.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a ledger that explains its own format | Given `seal/ledger.md` with a closed fenced block holding a row `\| X \| … \| nosuchfile.py#nothing@deadbeef \| …` above the live table, when `evidence-check` runs, then nothing is reported for the fenced coordinate and the exit code is what the live rows alone give | a case in the phase-2 module, seen red against `c52e8350` (the #444 reproduction) · NAME NOT IN TREE |
| S2 · the writers leave an example alone | Given S1's file with a drifted live row and a fenced example, when `--reverify` and `--migrate` run, then the bytes of the fenced block are unchanged | a case asserting the fenced span is byte-identical after each writer, seen red |
| S3 · an unclosed fence still holds | Given a ledger whose fence never closes above a row with a missing file, when the check runs, then that row is BROKEN | a case, which passes before and after (it pins the direction) |
| S4 · an indented delimiter is not a fence | Given a record with a line indented four spaces holding ```` ``` ````, when `readable` reads it, then the line is not a delimiter and the table after it is read | a case on `readable`, seen red against `blank_fences`'s `^\s*` |
| S5 · a closer carries no info string | Given an open ```` ``` ```` block holding a line ```` ```python ````, when `readable` and `live_lines` read it, then the block does not close there | a case per reader, seen red |
| S6 · the fence rules agree | Given a table of delimiter shapes, when `unverified_check`'s rule and `hooks/config.py#fence_map` read each shape, then they agree about which lines are fenced | one case, which walks the table |
| S7 · a quoted `drained` closes nothing | Given an `evidence-todo.md` with one open row and a fenced block holding `drained`, when `settle` and `fold_ledger.py --check` read it, then both report the row open | a case per command, seen red |
| S8 · one open-rows rule | When `fold_ledger.py#open_rows` is read, then it is `unverified_check.py#todo_open_rows` | a case asserting identity, red while the copy stands |
| S9 · a quoted marker gathers nothing | Given `CHANGELOG.md` with `<!-- specs/<real id> -->` only inside a fenced block, when the survivor sweep asks `gathered_fragments`, then that id is not gathered | a case, seen red |
| S10 · a claim after `-->` | Given the record lines `<!-- note` / `end --> gone_helper is used`, when the records arm reads them, then `gone_helper` is read | #220's first shape as a case, seen red |
| S11 · a comment reopened on its closing line | Given `<!-- a` / `b --> <!-- c` / `secret_name` / `-->`, when the records arm reads them, then no claim is read from lines 2 to 4 | #220's second shape as a case, seen red · NAME NOT IN TREE |
| S12 · a longer fence is not closed by a shorter one | Given a record with a ```` ```` ```` block quoting ```` ``` ````, when `claim_lines` reads it, then the inner delimiter does not close the block | a case, seen red |

## Data & interfaces

- `unverified_check.py` gains the delimiter rule as a public function. Its
  name and shape are the work's to choose, and `hooks/config.py#FENCE`'s
  `run`/`info` groups are the model. `FENCE_RE` either becomes that rule or
  retires, and its two comment blocks (one says "`blank_fences` keeps the old
  spelling") are rewritten either way.
- `evidence_check.py` loads `unverified_check.py` the way `chain_check.py`
  does (`READER`, by path). It has not loaded it before.
- `fold_ledger.py` loads `unverified_check.py` the way
  `.github/scripts/rider_check.py` loads `evidence_check.py`. The
  "it may not depend on this" clause in `todo_open_rows`'s docstring is
  corrected: that precedent shows the direction from `.github/` to a shipped
  script is already taken.
- `claim_lines` keeps its `[(line number, text)]` return shape. What
  changes is that the text is what lies outside the regions, and
  `NOT_IN_TREE` is still tested against the raw line.
- No CLI flag, exit code or message is added. A changed verdict is the only
  output change, and each one is pinned by the case listed above.

## Open questions → questions.md

Q1 goes to a person and carries a default the build proceeds on. Q2 to Q4
are measurements, and Q5 is the work's.

<!-- Framer's mark: the shape matches routing.md's and plan.md's feet-lines. -->

Framed 2026-09-24 by framer, before the build.
