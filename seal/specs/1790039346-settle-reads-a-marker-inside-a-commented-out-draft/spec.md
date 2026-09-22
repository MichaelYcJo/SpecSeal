# Feature Specification: `settle` reads a marker inside a commented-out draft, and the opt-out arm accepts a directory as the marker

<!-- seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

This is #489: the five findings review round 3 of #458's work item
(`seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/`)
opened after the chain's one reopening was spent. Its rounds settled the
shape of `settle` across three records, and **a row a round settled is not
reopened here** — this work closes the five deferrals and nothing the rounds
confirmed. Every coordinate below was re-resolved at `3cdfd8ad`, the squash of
#486. The ticket's line numbers were taken at `02b2038d`, and every one of
them still lands: the squash left `settle.py`, `unverified_check.py`,
`optin.py` and the two test modules byte-identical at those lines.

## What the tree answered, so nobody reopens it

The spawn prompt left two things open and named several more as facts to
re-check. All of them are decided below with the grounds, and none is a row in
`questions.md`.

| Left open | Answered | Where the grounds are |
|---|---|---|
| **Where the code-span rule lives** — one owner in `unverified_check.py`, or a `settle.py`-local pre-pass | **One owner, in `skills/verify/scripts/unverified_check.py`**, beside `blank_fences` and `opens_outside_a_comment`, composed into one helper that answers *is this line live* for every reader of the fold record and the ledger sections. Both callers can meet the shape: a ledger anchor quotes an unclosed opener inside backticks at four lines today, and every top-level `docs/` document that explains the marker convention quotes `<!-- specs/<id> -->` inside backticks (three lines, all closed on their own line today, so nothing is misread yet). A rule that one reader has and the other does not is exactly the state round 3 found and this ticket exists to end | §*The class, enumerated*, §*Measured on this tree* |
| **Whether the obvious closure is wrong** — the ticket says applying `opens_outside_a_comment` to `seal/ledger.md` loses three real markers | **Confirmed by measurement at `3cdfd8ad`**: 94 section markers through `blank_fences`; 91 with the comment state asked next, the three lost at lines 767, 992 and 1619; 94 again with inline code spans blanked before the comment state is asked, and the parked-draft shape still not live | §*Measured on this tree* |
| **Whether the `readable()` pair gains the pass** — `check_text`, `round_record.py` and `chain_check.py` read through `blank_fences(strip_comments(...))` | **No.** `readable` blanks a comment's content and the marker IS one, which the parent's S1 row and `test_readable_would_erase_every_fold_record` already establish; and `tests/test_chain_hooks.py#reader_blanking_passes` derives a parametrisation from `readable`'s own source, so a pass added there is #210's measured behaviour change to the review-history guard. The new helper is a sibling of `readable`, not a pass inside it | `plan.md` §*Alternatives* |
| **Whether five findings are one phase or several** | **Three phases.** The refusal path (findings 1 and 5) is twenty lines of `main` and stands alone; the single-scan pin (finding 4) adds no behaviour and is the guard the rule change is built under; the live-line rule (findings 2 and 3) is one site in `coordinates` plus the helper and the `folded_items` switch | `plan.md` §*Phases* |
| **Whether a correct finding-2 fix changes the dry run** — `81 work items in 37 segments, 16 ungrouped, 0 skipped` | **No, and a change would be a defect in the span rule.** Under the composed rule the ledger's not-live lines fall from 787 to 761, and those 761 are 48 genuine multi-line HTML comments (the *This work item's ledger rows* headers) carrying 0 coordinates and 0 markers; the per-section coordinate counts are identical to today's. Executed at `3cdfd8ad`: `bin/settle` prints the line above at exit 0 | §*Measured on this tree*, `plan.md` §*Phases* row 3 |
| **Whether this work item touches #487** | **No.** #487 is `open_rows` duplicated between `.github/scripts/fold_ledger.py` and `settle.py`, and its repair is a walk comparing the two functions' source. This work adds nothing under `.github/`, imports nothing from it (`tests/test_the_release_check_watches_what_ships.py#SHIPS` is `skills · agents · hooks · templates · bin · .claude-plugin`), and gives the code-span rule one owner so #487's list does not grow by a third copy. One thing is corrected in passing: `settle.py#coordinates`'s docstring says `.github/scripts/fold_ledger.py#demote` *carries the second copy and #487 is the ticket for it*, and #487's text is about `open_rows`, not the fence rule | §*Scope* |
| **Whether the parent's drifted rows are re-stamped in `seal/ledger.md`** | **They are not there.** The two rows this work drifts — S1 (`skills/verify/scripts/unverified_check.py#folded_items@7a8d3c99`) and S3 (`skills/settle/scripts/settle.py#coordinates@9b5febe4`) — sit in the parent's own fragment `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`, which no release has folded yet. `CLAUDE.md` §*a change writes fragments* and `CONTRIBUTING.md` §*House rules* put the re-read in the file the row is in, with a dated note; #488 is the ticket for the rule not naming drift-by-edit, and this work follows the documented repair rather than waiting for the rule. No row in `seal/ledger.md` cites a unit this work changes | §*Data & interfaces* |
| **Which accessor the class uses** | `os.path.isfile`, and the class is three readers of one marker: `hooks/optin.py#home_at` and `skills/implement/scripts/seal.py#no_root` already spell it that way; `settle.py#main` is the one instance that does not. `hooks/root-migrate.py:489`'s `os.path.exists` reads the OLD `.specseal/scratch`, a different signal asked in order to refuse a move, and is outside the class | §*The class, enumerated* |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| G1 · `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Nothing here asks a person anything. The one design choice (where the span rule lives) is decided from the tree with the measurement beside it, and the build runs to the pull request |
| G2 · `CLAUDE.md` §*a change writes fragments, never the shared file* · `CONTRIBUTING.md` §*House rules* — *Changing cited code is the case the rule has to answer, and it is not an append* | New rows go in `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`; the entry in this directory's `changelog.md`. The two parent rows this drifts are re-read and re-stamped **in the parent's fragment**, with a dated note naming what moved and why the claim still holds — the documented repair, never a removal and never an append |
| G3 · `CONTRIBUTING.md` §*What a change to a gate must carry* | `unverified_check.py#folded_items` is read by `.github/workflows/hygiene.yml`'s unverified-record step on every pull request, so the reader change carries the four items: a case seen red first; the failure direction, and after four rounds it is no longer a trade this gate makes. The reader was three passes composed — blank fences, blank code spans, then read comment state — and the middle pass had to decide whether a backtick run was a code span without knowing the comment state, which is the one thing that decides it: inside an HTML comment markdown is not parsed, so a closing delimiter between backticks there really closes the comment. Comment state depends in turn on which delimiters the span pass left standing, so the two are mutually dependent and no stateless pre-pass can be right. Four formulations were each a guess and three of the four moved the gate toward removing a directory, each caught by the round that read the one before. So `live_lines` is now ONE scan carrying fence, comment and span state together, which is the reading the guesses were approximating; there is no expensive-versus-cheap direction left to declare, because there is no approximation. It reads the document rather than modelling it, it closes the multi-line span the composition could not, and `test_the_scan_never_reads_live_what_the_format_parks` holds it against a reading derived from the format rather than from the scan — and round 6 found the first version of that reading sharing the scan's own fence bound, so it returned the scan's verdict and saw nothing; the bound moved in both, and the mutations that redden the case were run before it was trusted — the earlier oracle borrowed `live_lines`'s own boundary list, which round 5 found, and a case that agrees with the code it is pinning reports nothing. It asserts the safety direction rather than agreement, because the scan parks where two readings of a line disagree and full agreement would forbid exactly that — the generator whose absence let two rounds report different numbers for the same question. Every shape the four rounds named is pinned by a case; a prompt budget of zero; platform honesty, which here is that the rule is a text scan with no process in it |
| G4 · `skills/agent-contract/SKILL.md` §12 — *a defect belongs to a class* | The ticket names the class itself: *a line stops being live two ways*, one door closed in `folded_items` and not carried back. §*The class, enumerated* lists every reader of the live-line rule and every reader of the scratch marker, and says which are in and which are out |
| G5 · `skills/agent-contract/SKILL.md` §15 — *a new case is not planted until it has been seen red* | Finding 3 is a case that was never planted. Every case below names the mutation or the tree state it is red against, and the phase record says how it was shown |
| G6 · `skills/agent-contract/SKILL.md` §14 — *a fix that changes what a person sees documents it and pins it* | Finding 1 changes which refusal a directory-named marker produces. The case pins which sentence prints; `settle.py`'s docstring says the marker is a FILE where it names the opt-out |
| G7 · `tests/test_the_release_check_watches_what_ships.py#SHIPS` — `.github/` is not shipped | The reader this work extends is the shipped one, `skills/verify/scripts/unverified_check.py`, which `settle.py#load` already imports by path. Nothing is imported from `.github/scripts/` |
| G8 · `docs/one-root-by-lifetime.md` §*Decided when `settle` was built (2026-09-22)* — *Where the fold record lives: the `<!-- specs/<id> -->` comment the folded sentence already carries in its `docs/` document. No second file* | The record is a comment, so the reader of it cannot be the pair that blanks comments; what makes a marker a record is the line being live, and this work gives that judgment one owner |
| G9 · `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures use `example.com` and neutral ids of the `1700000001-alpha` shape the settle test module already uses |
| G10 · `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | No shipped file this work edits names the release version. The branch name in `routing.md` is the only place it appears in this directory |

## Scope

**In.**

1. `skills/settle/scripts/settle.py#main`'s refusal path: the marker read with
   `os.path.isfile` (finding 1), and the common git directory resolved once
   and handed to `home_at(root, common)` (finding 5).
2. `skills/verify/scripts/unverified_check.py`: a code-span blanker beside
   `blank_fences`, and one helper that composes *fenced → spans blanked →
   began outside a comment* so every reader asks one function whether a line
   is live. `folded_items` reads through it.
3. `skills/settle/scripts/settle.py#coordinates`: both loops — the
   `seal/ledger.md` sections and the `seal/ledger/<id>.md` fragments — read
   through that helper (finding 2), and the fragments loop gets the case it
   never had (finding 3).
4. `tests/test_unverified_rows_close.py#test_one_comment_scanner_serves_both_readers`
   earns its name: the single scan is pinned by replacing `comment_scan` at
   module level, not by the two views agreeing (finding 4).
5. The docstrings that describe the rule — `coordinates`, `folded_items`, the
   `FOLD_MARKER` comment, `opens_outside_a_comment` — say where the rule lives
   now and correct the #487 attribution.
6. This work item's `changelog.md` and ledger fragment; the two parent rows
   re-read in the parent's fragment.

**Out, and each with why.**

- **`readable()`, `check_text`, `round_record.py`, `chain_check.py`,
  `hooks/review-history-guard.py`.** They blank comment content, which is the
  right reading for a record's table and the wrong one for a fold record; a
  span pass added to `readable` is #210's measured behaviour change and
  `tests/test_chain_hooks.py#reader_blanking_passes` refuses it by design.
  A different rule for a different question.
- **`evidence-check`'s own readers.** `seal/follow-up.md` rows *reads a
  ledger row written inside a code fence as a live row* (#444) and *reads a
  backticked name inside an HTML comment* are the same class one module over,
  each with an answerer named. This work does not touch
  `skills/evidence-check/scripts/evidence_check.py`; the one-owner helper it
  adds is what a fix there would reuse, and that is written in the plan for
  whoever opens #444.
- **#487 and #488.** Neither is touched, for the reasons in the table above.
- **`.github/scripts/fold_ledger.py#demote`'s fence tracking.** Not shipped;
  its own rider says what it misreads. Out for the same reason the parent's
  build kept `open_rows` in the shipped script.
- **`skills/settle/SKILL.md`.** Its sentence — *read on a line of its own; a
  marker quoted inside a sentence is a description, not a fold* — stays true.
  No text a person reads there changes.
- **A second real repository, and the fold of this repository's own 97.**
  The parent's `overview.md` §*Not verified* holds both with their answerers.
- **Multi-line code spans.** CommonMark lets a code span cross a line break;
  a ledger row cannot, and a `docs/` paragraph that opens backticks on one
  line and closes them on the next around a comment opener is a shape this
  repository has never carried. The rule is single-line and says so; Q2 of
  `questions.md` is the work's to confirm with a sentence in the docstring.

## The class, enumerated

**The live-line rule.** A line is live when it is outside a fenced block and
began outside an HTML comment. Every reader in the shipped tree that needs
that answer, and what each has today:

| Reader | Fences | Comment state | Spans before the comment state | Pinned |
|---|---|---|---|---|
| `skills/verify/scripts/unverified_check.py#folded_items` (`:709-713`) | yes | yes | **no** — and `docs/` carries the shape | yes, two families |
| `skills/settle/scripts/settle.py#coordinates`, the `seal/ledger.md` loop (`:319`) | yes | **no** — finding 2 | **no** | fence half only |
| `skills/settle/scripts/settle.py#coordinates`, the fragments loop (`:330-336`) | yes | **no** | **no** | **nothing** — finding 3 |

After this work all three rows read through one function and the table has one
line. Readers outside the class, and why: `readable()` and its callers answer
*what text is a reader judging*, not *is this line live*, and blank the very
comment a marker is; `evidence_check.py` is the follow-up rows above.

**The scratch marker.** `hooks/optin.py#SCRATCH` is an empty FILE under the
common git directory, and the module says a directory of that name is not it.

| Reader | Accessor |
|---|---|
| `hooks/optin.py#home_at` (`:200`) | `os.path.isfile` — the measured decision, with the comment saying why |
| `skills/implement/scripts/seal.py#no_root` (`:663`) | `os.path.isfile` |
| `skills/settle/scripts/settle.py#main` (`:614`) | **`os.path.exists`** — finding 1, the one instance |

`hooks/root-migrate.py:489` reads `.specseal/scratch`, the pre-#80 marker, and
reads it to refuse a migration; it is a different signal and outside the class.

## Measured on this tree

Executed 2026-09-22 at `3cdfd8ad` by the framer's probes, over the shipped
`unverified_check.py` loaded by path and over `seal/ledger.md` as committed.
The ticket's figures were taken at `02b2038d`; every one of them holds here.

| Measurement | Result |
|---|---|
| section markers in `seal/ledger.md` through `blank_fences` alone | **94** |
| the same, then `opens_outside_a_comment` — the obvious closure | **91**; lost: 767 `1788472135-…`, 992 `1788613827-…`, 1619 `1788844127-…` |
| the same, with inline code spans blanked before the comment state | **94**, none lost |
| ledger lines the naive rule calls not live · the composed rule | **787 · 761**. The 761 are 48 genuine multi-line comment blocks holding **0 coordinates and 0 markers**, so no section changes |
| ledger lines whose only comment opener sits inside a code span and never closes | **4**: lines 78, 762, 980, 1612 — the anchors that park everything below them under the naive rule |
| per-section coordinate counts, composed rule against today's `coordinates()` | **identical** — no work item's segment moves |
| top-level `docs/*.md`: liveness differing between the naive and the composed rule | **0 lines** in 8 documents; 3 lines quote `<!-- specs/<id> -->` inside backticks and each closes on its own line |
| the parked-draft shape (`<!-- parked` / marker / `-->` / marker) under the composed rule | second line not live, fourth live — the defect is still caught |
| round 3's paste-ready regex `` `+[^`]*`+ `` against the CommonMark equal-length rule, over the ledger | both 94/94 and both 761 not live; they blank **60 lines differently** and agree on every liveness answer today |
| `bin/settle` at `3cdfd8ad` | `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped`, exit 0 |

## User scenarios & acceptance *(mandatory)*

Each row's last cell names how the case is shown red before it is committed
(G5). *Against the tree* means against `3cdfd8ad`'s code; *by mutation* means
against a named reversion applied and restored in the build.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 · a directory is not the marker | Given a repository with no `seal/` at either place and a **directory** named `specseal-scratch` under its git directory · When `settle` runs · Then it exits 2 saying *has no seal/specs/ at either place*, and the stderr does not say *has opted out* | a case beside `test_an_opted_out_repository_is_told_which_state_it_is_in` (`tests/test_settle_reads_before_it_removes.py:706`); red against the tree, which prints the opt-out sentence |
| A2 · a parked marker in the ledger opens no section | Given a `seal/ledger.md` with a real section and, below it, a commented-out draft holding a marker and a coordinate row · When `coordinates` runs · Then the draft's coordinate is attributed to no work item, and a real marker after the draft's `-->` still opens its section | a case beside `test_a_fenced_marker_in_the_ledger_opens_no_section` (`:679`); red against the tree |
| A3 · an opener quoted inside a code span parks nothing | Given a ledger row whose anchor quotes `<!--` inside backticks with no closer on the line, followed by a real marker and its rows · When `coordinates` runs · Then the marker opens its section and its rows are counted | the same module; red by mutation — the comment state asked without the span pass, which is the closure round 3 measured wrong |
| A4 · the rule over this repository's own ledger loses nothing | When `coordinates(ROOT)` runs over the real `seal/ledger.md` · Then the set of work item ids it sections is the set `blank_fences` alone would section, and it is non-empty | a case over `ROOT` asserting set equality rather than a number, because 94 grows at every release fold and a floor over the corpus is the shape `skills/settle/SKILL.md` §3 warns about; red by the same mutation as A3 (three ids missing) |
| A5 · a fragment's quoted coordinate is not the fragment's own | Given a `seal/ledger/<id>.md` fragment carrying a fenced example row and a commented-out example row · When `coordinates` runs · Then neither coordinate is the fragment's | a case beside A2; red by mutation — the fragments loop reverted to a whole-file `finditer`, which is round 3's M7 |
| A6 · the two views come off one scan — **RETIRED, see the note at the end of this row** | Given `comment_scan` replaced at module level by a stub yielding one sentinel pair · When `strip_comments`, `opens_outside_a_comment` and the new live-line helper are called · Then each answers from the stub | `test_one_comment_scanner_serves_both_readers` (`tests/test_unverified_rows_close.py:1482`) extended; red by mutation — a private copy of the walk inlined into one reader, which today's assertions cannot see | <!-- NAME NOT IN TREE: A6 is kept as the frame wrote it. The fourth formulation replaced the three-pass composition with one scan, so there are no longer two views to come off it; `comment_scan` and `strip_comments` survive and `opens_outside_a_comment` and the case named here do not. The acceptance that stands in its place is the safety direction against a reading derived from the format — not agreement, which G3 above records this design as forbidding, because the scan parks where two readings of a line disagree. Marked 2026-09-22, round 4's fix pass. -->
| A7 · the refusal path asks for the common directory once | Given a repository with no root · When `main` runs to the refusal · Then `git_common_dir` is called once and `home_at` receives the value | a case counting calls through a stand-in `optin` module handed to `settle.load`; red against the tree, which counts two |
| A8 · the dry run over this repository is unchanged | When phase 3 closes · Then `bin/settle` prints `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped` at exit 0, read with `echo $?` and not through a pipe | executed at the tip and quoted in `overview.md`; a different reading is a defect in the span rule, not a fact to record |
| A9 · every existing case still passes | When the two modules and the modules that load the reader run · Then `tests/test_settle_reads_before_it_removes.py`, `tests/test_unverified_rows_close.py`, `tests/test_chain_hooks.py` and `tests/test_a_script_says_which_interpreter_it_needs.py` are green — the last two because they pin `readable`'s pass list and the interpreter-floor text scan over the unguarded reader | executed per phase; the broad gate is the sealer's |
| A10 · the docstrings say where the rule lives | When a reader opens `coordinates`, `folded_items` or the `FOLD_MARKER` comment · Then each says a line is live when fenced blocks and code spans are blanked and it began outside a comment, names the one helper, and `coordinates` no longer attributes the fence rule's second copy to #487 | read in review; no case, because the sentence a case would pin is the helper's own name and `test_surveys_docstring_does_not_invite_the_mutation_that_reopens_finding_4` is the precedent only where a docstring invites a defect |

## Data & interfaces

- **New units in `skills/verify/scripts/unverified_check.py`**, names not yet
  in the tree: a span blanker, `blank_code_spans(lines)` — the same lines with
  inline code spans blanked to spaces of equal length, indices intact, a
  backtick string closed by the next backtick string of **equal** length on
  the same line and an unmatched one left as literal text (CommonMark 6.1,
  single-line) — and a composed reader, `live_lines(lines)`, yielding
  `(fence-blanked line, began outside a comment)` per line with the span pass
  between the two existing readers. `plan.md` §*Technical context* says why
  the pass sits in front of `opens_outside_a_comment` rather than inside
  `comment_scan`.
- **`skills/settle/scripts/settle.py#coordinates`** reads both loops through
  `live_lines`; the coordinate extraction runs over the fence-blanked text,
  never the span-blanked text, because the coordinate lives inside backticks.
- **`skills/verify/scripts/unverified_check.py#folded_items`** reads through
  `live_lines` and its two-call form goes.
- **`skills/settle/scripts/settle.py#main`**: `common` resolved once before
  `home_at(root, common)`; the opt-out arm tests `os.path.isfile`. No exit
  code, no CLI flag and no printed sentence changes; which sentence prints for
  a directory-named marker does.
- **No `zip` in `unverified_check.py`.** The module carries no interpreter
  guard, ruff's B905 wants `strict=` on every `zip`, and
  `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`
  refuses that keyword in an unguarded script by text. `enumerate`, the way
  `folded_items` already does and says why.
- **Ledger.** New rows in
  `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`,
  anchored on `live_lines`, `folded_items`, `coordinates`, `main`, `OPENER`,
  the three helpers the two readings are built from and the cases.
  Two parent rows drift and are re-read in
  `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`:
  S1 (`folded_items`) and S3 (`coordinates`). `seal/ledger.md:80` cites
  `strip_comments@35bb5b22`, which does not change, and every other
  `seal/ledger.md` row citing the two scripts anchors on `main`, `readable`,
  `merge_base`, `commit_of`, `resolves` or `base_label` of the reader —
  none touched.
- **Changelog.** One entry in this directory's `changelog.md`.

## `seal/follow-up.md`

Read 2026-09-22, in full. No row waits on this work as its prerequisite.
Two rows are the same class in `evidence_check.py` and stay where they are
with their answerers (§*Scope*, out). Nothing is deleted from that file.

## Open questions → questions.md

Two rows, neither a person's: a measurement the build takes at the end (A8)
and a sentence the work confirms about single-line spans. Anything a planner
must answer lives there, not inline.

<!-- The line below is the framer's mark. -->

Framed 2026-09-22 by framer, before the build.
