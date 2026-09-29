# Feature Specification: the hooks and the rider check read fences and comments by one rule (#667, #658)

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #667 §*The constraint a redo starts from* (the ticket; it ranks below `docs/` and above the code) | Two directions are each worse than `release/v0.16.0`'s reading: a declaration, a `Mode` row or a `Broad gate` row the base reads that is now missed, and a fenced or commented-out row that is now read. Every shape the three rounds of `1790635413` executed is held to both. This frame turns the two directions into one checkable property (§*The acceptance property*) |
| `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row* | One walk is consumed by every walk of the `\| Item \| Value \|` table: the reader, the refusal, and the writer that locates the line it overwrites. The comment half goes through that same one walk, never beside it |
| `docs/commit-review-gate-spec.md` §*The declaration, and where the check went instead* | The commit gate reads `routing.md` before anything else, and CI reads the same file at the pull request. Whatever `hooks/routing.py#table_rows` reads, both of them read |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Phases 3, 4 and 5 change a gate's verdict. Each carries a test seen red, a stated failure direction, a prompt budget and a platform note (§*Failure direction and prompt budget* below) |
| `CONTRIBUTING.md` §*Running the checks* | "The suite needs only `pytest`." Phase 1 changes that sentence if Q1 is answered (a). It is why Q1 is a person's row |
| `CLAUDE.md` §*The goal a design is chosen against* | A design that stops a run to ask is the more expensive one. This is why a construct that never closes keeps the base reading instead of turning into a refusal (§*A construct that never closes changes nothing*) |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New claims go to `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md`. The rows this work drifts are re-read where they live (§*Data & interfaces*) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is enumerated below, not taken from the ticket. Phase 3 adds a sentence a person reads, documented and pinned in its own commit. Every case that claims a defect is seen red against `3911a8cf` |

## Why three rounds traded one direction for the other

Read in the three review reports of `1790635413` (`rounds/round-{1,2,3}-report.md`
at `4edc5de6`). Every finding in the three readers has one of two causes.

| Round | Finding | Cause |
|---|---|---|
| 1 | 🟡 3: code-span delimiters either side of the config table hide it | the reader held **inline** comment state and could not see a code span |
| 1 | 🟡 4: a fence line inside a rider's body hides every rider below | a fence was decided with no knowledge of the **block** comment it stood in |
| 2 | 🟡 1: a code-span opener loses a rider | inline comment state again, one reader over |
| 2 | 🟡 2: a fence line inside a comment above the routing table hides the declaration; a commented `Review` row answers | fence decided before the block comment; no comment state at all |
| 3 | 🟡 1: an unclosed comment switches off every fence below it | an **unclosed** opener resolved toward one side, then inherited by every line below |
| 3 | 🟡 2: a prose opener loses a rider | inline comment state again, from a trigger the code-span fix could not reach |
| 3 | ⬜ 3: a stray opener closed by a later example hides the live table | an inline opener treated as able to hide a block |

Round 3's report names the second half of the trouble itself: "The oracle cannot
catch this, because it is built the same way." The parity oracle was composed of
`unverified_check.py` functions, so it shared the readers' model and agreed with
them exactly where they were wrong.

So the redo removes both causes rather than patching a third reading:

- it holds **no inline state at all** — no code span, no mid-line comment opener;
- it resolves nothing uncertain toward either side, because an uncertain line keeps
  the reading the base already gives it;
- it is checked against a parser that shares nothing with it.

## The reading

### What is modelled: two block constructs, by CommonMark's own block rules

A line is **hidden** when it lies inside one of these two, and the construct
closes:

1. **A fenced code block** (CommonMark §4.5). The delimiter rule is the one
   `skills/verify/scripts/unverified_check.py#fence_opener` and `#fence_closes`
   already state, and `hooks/config.py#FENCE` already copies: at most three
   spaces, three or more backticks or tildes, no backtick in a backtick opener's
   info string, and a closer of the same character at least as long with nothing
   after it.
2. **An HTML comment block** (CommonMark §4.6, HTML block type 2). It starts on a
   line that begins, after at most three spaces, with `<!--`. It ends on the first
   line that contains `-->`, which may be the start line itself.

The two are walked in one pass in document order. A start is looked for only on a
line outside both, so whichever starts first owns its lines until its own end:

- inside a fence nothing but the closing fence is read, so a `<!--` there opens
  nothing;
- inside a comment block nothing but `-->` is read, so a fence line, a backtick or
  a quoted rider there is comment text.

**Why these two rules can be exact where the earlier readings could not.** Both
start conditions and both end conditions are properties of one line. Neither
depends on a paragraph's extent or on a code span, because CommonMark decides
block structure before it parses any inline content (its Appendix A, *A parsing
strategy*). A fence can interrupt a paragraph, and so can an HTML block of type 2,
so no inline construct can hide either start line. Those section numbers are cited
from the specification and not opened in this tree. Q2 is where they are checked
by execution, before anything is built on them.

**A mid-line `<!--` is not modelled.** It is inline raw HTML. It can hide text
inside its own paragraph, but it can never hide a fence line or a comment-block
line, so ignoring it cannot move a construct. Five of the seven findings above
began at a mid-line opener that a reading had given the power to open a block,
whether it stood in a code span or in prose.

### What is not modelled, and what each reader does there

The walk claims only what it knows. Where a line's context is one it does not
model, the line is **uncertain**, and each reader reads it exactly as the base
does.

| Context | Why the walk is not exact there | How far the uncertainty reaches |
|---|---|---|
| a construct start indented one to three spaces | inside a list item, the item's end can end the construct before its delimiter, and the walk does not track list items | the rest of the file, because every later pairing may have shifted |
| a line at up to three spaces beginning `<` plus a letter, `/`, `?` or `!`, other than `<!--` | it may start an HTML block of another type (§4.6 types 1 and 3 to 7), inside which a fence or `<!--` line opens nothing | the rest of the file, for the same reason |
| a paragraph line after a mid-line `<!--`, up to the first line holding `-->` or the next blank line | an inline comment may hide it, and knowing whether it does needs code spans and the paragraph's extent | those lines only; no block start can be inside |
| lines of a block quote, and lines indented four spaces or more | a fence inside a block quote ends with the quote; four spaces is an indented code block or paragraph text | those lines only |
| lines below a construct that never closes | a renderer hides them all | the live answers there, to the end of the file (next section) |

These are the **minimum**. Phase 2 may widen what the walk calls exact, and only
where the property test holds on the generated corpus (Q4). It may never narrow
what it calls uncertain without that.

Each reader's base reading is the one `3911a8cf` ships:

| Reader | Its base reading of a line |
|---|---|
| `hooks/config.py` | hidden inside a fenced block by `fence_map`'s rule, an unclosed block to the end, which is `tests/test_unverified_rows_close.py#fenced_by_the_shared_rule` |
| `hooks/routing.py#table_rows` | never hidden |
| `.github/scripts/rider_check.py#comment_blocks` | never hidden by a fence; its own comment walk decides what a rider block is |

### A construct that never closes is not a construct

A fence with no closing fence below it, or a `<!--` line with no `-->` at or below
it, is **not a construct** to this walk. Its start line is read as an ordinary
line and the walk goes on. Below that line a renderer hides everything, so the two
kinds of answer the walk gives there are not worth the same:

- **its hidden answers stand.** A line inside a closed construct further down is
  hidden by the renderer too, so hiding it cannot leave both readings;
- **its live answers are uncertain**, so each reader keeps its base reading of
  those lines.

Three consequences are deliberate:

- **`hooks/config.py` keeps hiding every line below an unclosed fence**, because its
  base does. That is #429's reading, and `broad_gate.py#fence_left_open` already
  tells a person about it.
- **`hooks/routing.py` and the rider check read through an unclosed fence**, because
  their base does, and hide only what a closed construct further down holds. This
  reverses two things `1790635413` pinned: its routing assertion
  `routing.parse("```\n" + two_axis_text()) is None`, and its rider rule *"fence
  spans in `.md` files only, unclosed to the end"*.
- **An unclosed comment switches off no fence below it** (round 3, 🟡 1), because it
  is not a construct at all. The fences below it are walked as if it were not
  there. Nothing further down can undo that: no `-->` follows it, so no comment
  block below it can close either, and the fences below it pair exactly as the
  fence-only reading pairs them.

The grounds are the constraint. A renderer hides everything below an unclosed
construct, so following it would miss a declaration, a `Mode` row or a rider the
base reads, which is the first direction. Round 3's rider finding was that shape,
and its proposed fix flipped the `lone` assertion to `[]`. Keeping the base
reading of the live lines loses nothing either direction forbids.

### The acceptance property

For every line L of a document, with `base(L)` the reader's base reading and
`renderer(L)` the oracle's (§*The oracle*):

1. **The reader never leaves both.** `new(L)` equals `base(L)` or `renderer(L)`.
   A line the reader newly hides is hidden by the renderer, so it was never a live
   row. A line the reader newly reads is read by the renderer, so it was never
   fenced or commented out. This is the constraint, for every document at once.
2. **Where the walk claims to be exact, it is.** On every line the walk does not
   call uncertain, its hidden-or-live answer equals `renderer(L)`. Without this
   half, a reader that did nothing would pass half 1.
3. **Better where the issues say.** On every shape in §*The shapes*, the reader
   gives the *Expected* answer.

Half 1 and half 2 run over the shape table and over a seeded generated corpus of
delimiter-heavy documents. Half 3 is the case table.

### The oracle

The oracle is a CommonMark parser that shares no code and no model with the walk.
It says which lines a renderer puts inside a fenced block, an indented code block,
an HTML block, or an inline HTML comment. It judges nothing else: which lines form
a table is each reader's own grammar and does not change here (§*Scope*, out).

The candidate is `markdown-it-py`, pinned, as a test-only dependency. The gates
stay stdlib-only; only the suite gains a package. Whether the suite may take one
is Q1, a person's row. Its options, and what each one leaves the property able to
see, are there.

## Scope

### The class, enumerated

A reader is in the class when it is on the hook path or is the rider check, walks
markdown lines, and decides whether a line is a row or a rider with no fence or
comment rule, or with a rule that holds inline state. Enumerated 2026-09-29 by
reading every table walk under `hooks/` (`git grep` for `startswith("|")` and
`split("|")`) and every importer of `hooks/config.py` and `hooks/routing.py`.

**In scope:**

| Reader | Its rule today | What it adopts | Phase |
|---|---|---|---|
| `hooks/config.py#config_rows`, `#refusal`, and `#unfenced` / `#fence_map` | fences by CommonMark §4.5, unclosed to the end; no comment state | the walk; an uncertain line keeps the fence-only reading | 3 |
| `skills/implement/scripts/seal.py#table_span`, the writer | reads through `hooks/config.py#unfenced` | nothing of its own: it follows `unfenced`, so reader and writer stay one walk | 3 |
| `skills/verify/scripts/broad_gate.py#fenced_row_at`, `#fenced_row`, `#fence_left_open`, `#missing_row` | takes the complement of `unfenced` and calls every hidden `Broad gate` line fenced | tells a line hidden inside a comment from one inside a fence, and says which (a new sentence, §14) | 3 |
| `hooks/routing.py#table_rows`, which `#parse` reads | no fence and no comment state; every two-cell pipe line is a row, and `parse` keeps the last of a label | the walk; an uncertain line is read, as today | 4 |
| `.github/scripts/rider_check.py#comment_blocks`, and `#region_lines` through it | no fence state | in a `.md` file, a marker line the walk places inside a fence that closes opens no rider. Other file types unchanged | 5 |

`routing.parse` is read by `hooks/commit-review-gate.py`, `hooks/implementer-notice.py`,
`hooks/implementer-mark.py`, `hooks/review-history-guard.py`,
`skills/code-review/scripts/chain_check.py`, `round_record.py` and `survivor_check.py`.
Each inherits the new reading with no edit of its own, and phase 4's corpus
measurement is what shows none of them changes answer on a committed file.

**Out of scope:**

| What | Why it is out | Who answers what is left |
|---|---|---|
| `unverified_check.py#live_lines`, `#readable`, and every reader #584 moved onto them (the release scripts, `correction_check.py`, `payload_meter.py`, the role test) | They ship in #663, which held through three rounds. They answer a different question: a fold marker is safe when an uncertain line is parked, and a hook row is safe when an uncertain line keeps its base reading. One walk cannot serve both safe directions without choosing wrong for one of them | nothing left |
| `survivor_check.py`'s `--exempt` reader, #658's other half | Moved onto `readable` by #663 | nothing left |
| The fence toggles in `tests/test_docs_line_wrap.py` and `tests/test_handoff_outlives_the_merge.py`, the third row of #658 | Moved by #663 | nothing left |
| `close_issues_on_release.py` and the scripts that read a pull request body through it | GitHub's rule on purpose (`docs/issues-and-milestones.md` §*A keyword inside a fence or a code span claims nothing*) | nothing left |
| Each reader's table grammar: the header and separator rules, the stop rule, `parse`'s last-row-wins | Not a question about fences or comments, and each was argued through its own rounds (#82, #415) | nothing left |
| A row hidden only by an **inline** comment, an opener that does not begin its line | Knowing it is hidden needs code spans and the paragraph's extent, which is where all three rounds failed. The base reads such a row too, so reading it is not worse. Every comment this plugin writes into these files begins its line (`seal.py`'s `NEW_CONFIG` header, the two comments in `templates/sdd-routing.md`), and none of its documents shows a row commented out mid-paragraph (read: `templates/config.md` holds `<!--` once, inside a code span on line 97, and `skills/config/SKILL.md` not at all) | the orchestrator, who files an issue if a case is ever reported |
| The commit gate and `chain_check.py` naming a `routing.md` whose whole table is hidden | Such a file reads as no declaration, and it gets the message every non-parsing `routing.md` gets today. That generic path already exists and is not changed here. No committed declaration has the shape (§*The shapes*, R10) | the orchestrator, as a follow-up issue if wanted |
| Python and YAML riders (`#`) | Markdown fences mean nothing there | nothing left |
| `evidence_check.py#fence_rule` and its readers | Already on the shared delimiter rule; files A and C of this milestone | nothing left |

## The shapes

Every shape the three rounds executed against these three readers, and every case
`1790635413` planted for them, with two neighbours of the class. *Base* is
`3911a8cf`. The three readers and their tests are byte-identical at `551c7967`, the
base the rounds compared against (`git diff --stat 551c7967 3911a8cf` over them is
empty, read 2026-09-29). *Renderer* is what CommonMark's block rules give, derived
by reading them and **not executed** — Q2 executes it. It names what the reader
would return with the renderer's hidden lines removed; whether those lines form a
GFM table is not its question. Where a round executed the base answer, the cell
says so; the rest are read from the base code.

Texts marked *B* are `1790635413`'s own test strings at `4edc5de6`, which the
build can take verbatim. `two_axis_text()` is `tests/test_routing_is_recorded.py`'s
helper, a table declaring `through the review chain`.

**The config reader** (`config_rows`, and `refusal` where named):

| # | Shape | Base | Renderer | Expected | Case |
|---|---|---|---|---|---|
| C1 | *B* `QUOTED_DELIMITERS`: an opener quoted in a code span above the table, a closer below (round 1, 🟡 3) | both rows (executed, round 1) | both rows | both rows | pins |
| C2 | *B* a closed comment above the table whose body holds a fence line (round 2, ❓) | `[]`, and an unclosed fence reported (executed, round 2) | the table | `[("Mode", "shared")]`, and no unclosed fence | red at base |
| C3 | a mid-line opener nobody closed, a fenced example table (`Mode local`, `Broad gate true`), then the live table (round 3, 🟡 1) | the live table | the live table | the live table | pins |
| C4 | a mid-line opener, the live table, a fenced example below holding a closed comment (round 3, ⬜ 3) | the live table | the live table | the live table | pins |
| C5 | *B* `COMMENTED_OLD_ROW`: a closed comment inside the table holding `Broad gate old -q` | `[("Broad gate", "old -q")]` alone | the two live rows | the two live rows | red at base |
| C6 | *B* `COMMENTED_OLD_TABLE`: a whole old table in a closed comment above the live one | the parked table | the live table | the live table | red at base |
| C7 | C5 with CRLF endings | as C5 | as C5 | as C5 | red at base |
| C8 | *B* a malformed pipe-line inside a closed comment, then `Mode shared` (`refusal`) | the commented line reported as the person's refused row | no refused line | `([], [], None)` | red at base |
| C9 | *B* S14: a `<!--` never closed, above the table and inside it | every row | nothing below the opener | every row | pins |
| C10 | *B* S15: the writer, with a commented `Mode local` above the live one | rewrites the commented row | — | rewrites the live row | red at base |
| C11 | the only `Broad gate` row sits inside a closed comment (`broad-gate`) | refusal says the row is absent | — | refusal says it is inside a comment, and runs nothing | red at base |
| C12 | #429's fenced example table above the live one | the live table | the live table | the live table | pins (existing cases) |
| C13 | *B*'s lone-backtick entry in `COMMENT_SHAPES`: a prose line holding a lone backtick and then a mid-line `<!--`, a pipe-line, a line holding `-->`, a second pipe-line | nothing hidden | the first pipe-line hidden by an inline comment | nothing hidden | pins the residual |
| C14 | a fence never closed above the live table | `[]`, the fence reported | `[]` | `[]`, the fence reported | pins |

**The routing reader** (`parse`):

| # | Shape | Base | Renderer | Expected | Case |
|---|---|---|---|---|---|
| R1 | *B* #658: a fenced example below the table holding `Review straight to the PR` and another `Branch` | the example answers | the table | the table | red at base |
| R2 | *B* the whole table inside a closed `~~~` fence | a declaration | nothing | `None` | red at base |
| R3 | *B* `"```\n" + two_axis_text()`, a fence never closed | a declaration | nothing | a declaration | pins; reverses `1790635413`'s assertion |
| R4 | *B* a closed comment above the table whose body holds a fence line (round 2, 🟡 2) | the chain (executed, round 2) | the chain | the chain | pins |
| R5 | *B* a closed comment below the table holding `Review straight to the PR` (round 2, 🟡 2) | straight to the PR (executed, round 2) | the chain | the chain | red at base |
| R6 | the table, a mid-line opener nobody closed, then a fenced `Review straight to the PR` (round 3, 🟡 1) | straight to the PR | the chain | the chain | red at base |
| R7 | a mid-line opener, the table, then a fenced example holding a closed comment and a `Review` row (round 3, ⬜ 3) | the example answers | the chain | the chain | red at base |
| R8 | the table, a line-start `<!--` nobody closed, then a fenced `Review straight to the PR` | straight to the PR | nothing below the opener | the chain | red at base |
| R9 | a line-start `<!--` above the table whose only `-->` is below the table | a declaration | nothing | `None` | red at base |
| R10 | every committed `routing.md`, 26 files, and `templates/sdd-routing.md` | today's parse of each | — | the same parse, value for value | measurement (Q3) |

**The rider check** (`comment_blocks(lines, "doc.md")`):

| # | Shape | Base | Renderer | Expected | Case |
|---|---|---|---|---|---|
| K1 | *B* a fence line inside rider one's body, rider two below (round 1, 🟡 4) | both riders (executed, round 1) | both | both | pins |
| K2 | *B* a prose line quoting the opener in a code span, a fenced quoted rider, a real rider (round 2, 🟡 1) | the quoted and the real | the real | the real | red at base |
| K3 | *B* the same with the opener in prose, no backticks (round 3, 🟡 2) | the quoted and the real | the real | the real | red at base |
| K4 | *B* `lone`: a lone backtick, an opener, a fence line, `-->`, then a real rider | the real rider | none: the fence never closes | the real rider | pins; round 3's proposed flip to `[]` is not taken |
| K5 | *B* S8: a rider quoted alone in a closed fence | a rider, BROKEN at exit 2 | none | none, exit 0 | red at base |
| K6 | *B* S9: a `.py` file with a line of backticks, then a `# RIDER:` block | the rider | — | the rider | pins |
| K7 | *B* rider two, then a rider quoted in a fence after its closed comment | the quoted one too | rider two alone | rider two alone | red at base |
| K8 | every file under `RIDER_ROOTS` | today's blocks; 0 markdown riders in the tree (read: no `.md` line under the roots begins with an opener and carries the marker) | — | the same blocks | measurement (Q3) |

R2 and R9 are where the constraint's two directions meet. Each file's only rows
are fenced or commented out, so reading them is the second direction, and not
reading them misses what the base read, which is the first. The tree breaks the
tie: `hooks/routing.py`'s docstring says "Everything here fails toward 'no
declaration'. A file that cannot be read is not an answer somebody gave", and
`1790635413` pinned R2 the same way. So the gate asks, as it does for any
`routing.md` that does not parse, and CI does the same at the pull request.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the oracle is independent | Given the oracle helper, when its source is read, then it imports nothing from `hooks/`, `skills/` or `.github/scripts/`, and on every shape above it gives the *Renderer* column | the helper's own cases; Q2 settles the column |
| S2 · the walk is exact where it claims to be | Given the shape table and a seeded generated corpus, when the walk classifies each line, then every line it does not call uncertain is classed as the oracle classes it | the property case, seen red with the comment-block rule removed and with a mid-line opener allowed to open a comment |
| S3 · the delimiter rule stays one rule | Given `FENCE_SHAPES`, when the walk's fence half and `unverified_check.py#fence_spans` read them, then they agree line for line and on where an unclosed block opened | `tests/test_unverified_rows_close.py#test_the_fence_rule_agrees_with_the_config_reader`, retargeted if the copy moves |
| S4 · the config reader never leaves both readings | Given the shapes and the corpus, when `hooks/config.py` classifies each line, then each answer is the fence-only reading's or the oracle's | the property case over the config reader |
| S5 · the config shapes | C1 to C14 give the *Expected* column; each marked red fails at `3911a8cf` | one case per row, in `tests/test_the_mode_question_is_asked_once.py` and `tests/test_the_seal_is_taken_once_by_the_sealer.py` |
| S6 · the writer agrees with the reader | Given C10, when `seal mode shared` writes, then the live row changes and the commented line is byte-identical | a case asserting the bytes, red at base |
| S7 · the gate names a commented row | Given C11, when `broad-gate` runs, then it refuses, says the row is inside an HTML comment rather than absent or fenced, and runs nothing | a case pinning the sentence, red at base (§14) |
| S8 · no fence the walk refutes is reported | Given C2, when `broad_gate.py#fence_left_open` and `seal.py`'s write guard ask about an unclosed fence, then neither names one | a case, red at base |
| S9 · the routing reader never leaves both readings | as S4, over `hooks/routing.py#table_rows`: every line it hides, the oracle hides | the property case over the routing reader |
| S10 · the routing shapes | R1 to R9 give the *Expected* column | one case per row in `tests/test_routing_is_recorded.py` |
| S11 · no committed declaration changes | R10: every committed `routing.md` parses to the same value at `3911a8cf` and at HEAD | a measurement recorded in the phase record, and the count in its changelog fragment |
| S12 · the rider shapes | K1 to K7 give the *Expected* column | one case per row in `tests/test_a_rider_reaches_its_file.py` |
| S13 · no current rider changes | K8: `comment_blocks` and `rider_check.py`'s exit code over the tree are the same at `3911a8cf` and at HEAD | a measurement recorded in the phase record |
| S14 · the config corpus | every tracked `.md` file through `config_rows` reads the same at `3911a8cf` and at HEAD, except files that hold a shape above | a measurement recorded in the phase record |
| S15 · a copied script still says what is missing | Given a copy of `hooks/config.py`, `hooks/routing.py` or `seal.py` taken without the walk's module, when it loads, then it exits with a sentence naming the file, the shape `seal.py#refuse_without_hooks` already has | rows in `tests/test_a_script_copied_alone_exits_2.py`, and `seal.py#HOOK_PURPOSES` |

## Failure direction and prompt budget

`CONTRIBUTING.md` asks each gate change for these; they are stated once here and
repeated in the pull request.

- **The config reader** reads fewer rows in one family (a row inside a closed
  comment, C5, C6, C8) and more in one shape (C2, a table under a closed comment
  that quotes a fence). The first is the module's own direction, *nothing is
  declared*. The second reads a table the renderer shows and the base hid.
- **`broad-gate`** refuses where it ran a commented-out command (C11). A refusal
  costs a person a sentence; running a command nobody chose costs a stamp over the
  wrong suite.
- **The commit gate** asks where the only answer was fenced or commented out (R2,
  R9), and is otherwise silent where it was silent. That ask is the one every
  undeclared commit already gets.
- **The rider check** stops failing on a quoted rider (K5, K7) and reads every
  rider it read before (K1, K4).
- **Prompt budget.** No new question. `mode-gate` asks the mode question only where
  the `Mode` row stood inside a closed fence or comment, which is *nobody declared*
  and inside its existing budget of two per session per repository. The commit
  gate asks only in R2 and R9.
- **Platform.** String processing only. CRLF is a case in each reader's table
  (C7), because `hooks/config.py#unfenced` already takes either line ending.

## Data & interfaces

- **One implementation, under `hooks/`.** A new module, stdlib only, holding the
  walk and its uncertainty mask. `hooks/config.py` and `hooks/routing.py` import it
  as a sibling, the way `routing.py` imports `optin.py` today, and each puts its own
  directory on `sys.path` so the loaders that execute it by path keep working:
  `broad_gate.py#load` (`CONFIG_READER`), `chain_check.py` and `survivor_check.py`
  (`ROUTING`), `seal.py` (`HOOKS`, which also gains a `HOOK_PURPOSES` entry).
  `rider_check.py` loads it by path, in `load_checker`'s shape. A hook imports
  nothing from `skills/` (`hooks/config.py`'s docstring,
  `unverified_check.py#fence_opener`'s hook-path paragraph), and nothing here
  asks it to. The name and the API are Q5's.
- **The delimiter copy.** `hooks/config.py#FENCE` is today the one deliberate copy
  of `unverified_check.py#FENCE_RE`. It moves into the new module, or the new module
  reads it, and `unverified_check.py#fence_opener`'s docstring names where the copy
  now lives. The parity case keeps holding it (S3).
- **What the walk hands back.** For each line: hidden inside a fence, hidden inside
  a comment block, live, or uncertain; and where a fence that never closes opened.
  `hooks/config.py#fence_map` and `#unfenced` keep their names and their shapes for
  their callers, with the fence-only reading on uncertain lines.
  `broad_gate.py` asks the new "which kind" question beside `fenced_row_at`.
- **Messages.** One new refusal sentence in `broad-gate` (S7), documented in
  `templates/config.md` beside the fenced-row sentence and pinned. No new flag, exit
  code or prompt.
- **The oracle helper** lives in `tests/`, reads `markdown-it-py`'s tokens and
  nothing of this repository's, and returns per line whether a renderer hides it.
  The generated corpus is seeded and deterministic, and its size is set against the
  suite's time (Q7).
- **Ledger rows this work drifts**, re-read and re-stamped where they live, counted
  from `seal/ledger.md` and `seal/releases/*.md` on 2026-09-29:
  `hooks/config.py#fence_map` (2), `#config_rows` (2), `#refused_row` (2),
  `#unfenced`, `#refusal`, `#declared_mode`, `#CONFIG_ROW` (1 each) in
  `seal/releases/0.9.1.md`, `0.12.0.md`, `0.12.1.md` and `0.15.3.md`;
  `hooks/routing.py#parse` (2); `.github/scripts/rider_check.py#comment_blocks`,
  `#region_lines` (1 each) in `seal/releases/0.9.1.md`;
  `skills/implement/scripts/seal.py#table_span` (2);
  `skills/verify/scripts/broad_gate.py#fenced_row`, `#fence_left_open`,
  `#missing_row`, `#rows_read` and the rest the edit reaches;
  `unverified_check.py#fence_opener` (2) where its docstring changes;
  `tests/test_unverified_rows_close.py#test_the_fence_rule_agrees_with_the_config_reader`
  and `#FENCE_SHAPES` (1 each). `seal/releases/0.15.3.md`'s P1-2 says
  `hooks/config.py#fence_map` "is the one deliberate second copy of the delimiter
  rule"; if the copy moves, that claim is corrected in place with a dated note. The
  phase that edits a unit re-reads its rows, and `evidence-check` names the rest.
- **Two open pull requests touch the same files.** #663 (work item B) edits
  `unverified_check.py#fence_opener`'s docstring, `tests/test_unverified_rows_close.py`,
  `tests/test_a_rider_reaches_its_file.py`, `hooks/routing.py` and `seal.py`, and is
  reverting its own changes to the three readers as this is framed. #660 (work item
  D) edits `hooks/routing.py`'s docstring, `seal.py` and
  `tests/test_a_rider_reaches_its_file.py`. Whichever lands first, the other is
  merged hunk by hunk (Q6).

## Open questions → questions.md

One row needs a person: Q1, whether the suite may take `markdown-it-py`. Q2, Q3 and
Q7 are measurements; Q4, Q5 and Q6 are the work's.

Framed 2026-09-29 by framer, before the build.
