# Feature Specification: the signer sweep's leftovers from the second check (#831)

<!-- seal/specs/1791270163-the-signer-sweeps-leftovers-from-the-second-check/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#831 holds the four ⬜ findings the second post-review check of #830 left
open and filed instead of fixing, because each check of #830's fixes had
named new neighbouring shapes and the orchestrator ended the loop. The record
with the executed probes and the paste-ready fixes for findings 1–3 is
`seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/post-review-check-2.md`
(read; coordinates there are at ae5dec8a, the commit #827 squashed into
4b363e68 on `release/v0.19.0`). None of the four ships a wrong exit code or
loses a record: 1 and 2 are gaps in a test, 3 is a printed string, 4 is the
run's paperwork.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-pact.md`, the statement under the `<!-- specs/1791239490-… -->` fold marker (*A pact or a pact review record headed with the word 0.18.x used still reads…*) | A file holding a table under the new header is read from it alone and an old header beside it is refused; no command rewrites a pact. The glued-header sentence of finding 3 is a refusal under this clause, and its remedy (delete the line) stays; only the quote changes. The statement's own text is NOT edited by this work (`post-review-check-2.md` §*The new sentence against the policy and the changelog*: nothing contradicts) |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | Finding 4. `seal/config.md` declares `Ledger frozen from \| 1790993141`; work item 1791239490's rows R1 and R6 now stand in `seal/releases/0.19.0.md` (lines 31 and 36, read), so neither is edited there. R1's claim is false as written and takes a `Corrected ·` row in this item's fragment; R6's claim becomes true once finding 1 is fixed and takes a `Re-read ·` row, which `--reverify --into` writes |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | Where the ledger rows and the changelog entry go: `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md` (the `seal/ledger/` directory does not exist at the branch point and is created by the first row) and `seal/specs/1791270163-…/changelog.md` under `### Fixed`, no line starting `## ` |
| `skills/agent-contract/SKILL.md` §14, §15 | Finding 3 changes a sentence a person reads: the S4 case pins the new quote in the same commit. Every case this work adds or changes is seen red first, and the hand-back says how |
| `skills/agent-contract/SKILL.md` §12 | Finding 1 is a class, not a coordinate: every block GFM lets begin directly under a paragraph's last line ends the span, not only the `---` shape that regressed |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | The link that sends a session to the two clauses above |

## Scope

**In**, one item per finding of #831:

1. **`tests/test_one_word_one_meaning.py#without_the_policy_span`** ends the
   excluded span wherever GFM ends the statement's paragraph: a blank line,
   an ATX heading, a fold marker (as now), and also a list item that can
   interrupt a paragraph, a block quote, a fence, an HTML block, a thematic
   break and a setext underline, each directly under the statement with no
   blank line. A lazy continuation line of the statement stays inside the
   span. The regex is the one under `post-review-check-2.md` §*Paste-ready
   fixes* ⬜ 1 (executed there: the six block plants red in both sweep cases,
   the continuation line green, the module green at 21 passed). The
   docstring then reads true as it stands.
2. **`tests/test_a_signer_declares_its_pact.py#test_s4_a_pact_holding_both_tables_reads_signer_and_refuses_the_old_one`**
   gains, at its end, the shape that tells the filter's two positions apart:
   a glued old header, a blank line, then a whole old table. One refusal,
   the walk's stray-row one naming `| Signatory |`; the glued line is not
   also refused as an entry, and `orders-web` is the one signer read. The
   case is ⬜ 2's fence; it goes red when the filter is moved back inside the
   stray-row branch, which is how it is seen red.
3. **`hooks/config.py#read_table`** quotes a glued old header as the line is
   written, not rebuilt from its cells: `|Signatory|` is named as a
   `` `|Signatory|` `` line and `| Signatory |` as before. The rows carry
   their line numbers from `gfm_table`, and both `gfm_table` and the quote
   index `text.splitlines()`, so `text.splitlines()[line - 1]` is the line
   the walker numbered (read, `hooks/config.py#gfm_table`: `lines =
   text.splitlines()`, `rows.append((index + 1, found))`). The "beside"
   sentence is unchanged. The S4 case's glued loop expects the quote as
   written for each of its three shapes.
4. **Rows R1 and R6 of work item 1791239490**, now in
   `seal/releases/0.19.0.md`, are corrected and re-read in this item's
   fragment and nowhere else. R1: a `Corrected ·` row whose claim's last
   clause reads as ⬜ 4's fence says (refused once as a line inside the
   table *unless the walk's stray-row refusal already names an old header
   further down*), whose grounds carry the citation and every coordinate R1
   rests on at its current hash, and whose notes append the post-review
   check 2 fact. R6: the `Re-read ·` row `evidence-check --reverify --into`
   writes once `without_the_policy_span` has moved. `Corrected · P8`
   (`seal/releases/0.19.0.md:22`) also cites `read_table` and takes a
   `Re-read ·` row from the same run.
5. The closing records of this work item: `changelog.md` (`### Fixed`),
   `overview.md`, `phases/phase-N.md`, written by the builder.

**Out**, with the reason:

- The wording of `docs/the-pact.md`'s statement and of `changelog/0.19.0.md`.
  The second check read the new glued sentence against both and found no
  contradiction; the released changelog is a record and is not edited.
- `hooks/config.py#renamed_header` and the "beside" sentence. Neither finding
  names them.
- A `pact-check` end-to-end pin of the as-written quote. No such pin exists
  today for the glued sentence (`grep -rn "line inside its" tests/` finds
  only the S4 case), and the S4 unit case is where #830 pinned it; adding an
  end-to-end case is a widening nobody asked for.
- The first post-review check's four findings. All four are confirmed closed
  in `post-review-check-2.md` §*Verdicts*.
- The exactness of the span's HTML-block end. The widened regex ends the span
  at any `<` at the start of a line, where GFM lets only HTML block kinds 1–6
  interrupt a paragraph. That errs toward sweeping more text, never less, and
  the baseline stayed green under it in the second check. A tighter pattern
  is not owed until a real line of `docs/the-pact.md` trips it.
- The broad gate. `routing.md` says `straight to the PR` and `stop before the
  pull request`, so no sealer runs in this segment; CI at the pull request,
  or the session that opens it, answers it (`overview.md` §*Not verified*
  names it).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a block directly under the policy statement is swept | Given `docs/the-pact.md` with the old word planted in a list item, a block quote, a fenced block, a paragraph after `***`, a `<div>` line, or a paragraph after a `---` underline, each directly under the statement's last line with no blank line / When `test_no_pact_text_names_a_signer_the_way_0_18_did` and `test_no_live_text_says_the_word_0_19_0_renamed` run / Then each plant is red in both cases, and a plant on a lazy continuation line of the statement is green | the six plants each seen red, by a `test_tmp_` probe over `without_the_policy_span` or by planting into the working tree and reverting (the work decides, W1); then `bin/test tests/test_one_word_one_meaning.py -q` green |
| S2 the glued sentence quotes the line as written | Given a pact `# Pact`, blank, `\| Signer \|` table, then `\|Signatory\|` on the next line / When `pact_signers` reads it / Then the one refusal naming the old header says ``holds a `\|Signatory\|` line inside its `\| Signer \|` table …``; given `\| Signatory \|` instead, the quote is `` `\| Signatory \|` `` as before; `pact_reviews` the same for `\|Signatory\|Change\|Verdict\|` | the S4 case's glued loop, red against the current `read_table` (the first shape is unspaced and expects the spaced quote today — revert the two `hooks/config.py` lines to show it), then green; `bin/test tests/test_a_signer_declares_its_pact.py -q` |
| S3 a glued header above a second old table is named once, by the walk | Given the `\| Signer \|` table, `\| Signatory \|` glued under it, a blank line, then a whole `\| Signatory \|` table / When `pact_signers` reads it / Then the signers are `["orders-web"]` and the refusals are exactly the stray-row sentence ``has a `Signer` table that ends above `\| Signatory \|`, a row the walk never reaches — it and every signer below it would go unread`` | the new assertions at the end of the S4 case: red with the `rows = [...]` filter moved back inside the `if holds_old and not any(...)` branch, green at HEAD |
| S4 the released rows are corrected in the fragment | Given `seal/releases/0.19.0.md` unchanged on the branch / When `bin/evidence-check --reverify --into seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md --checked 2026-10-06` runs after S1–S3 land, and R1's written row is turned into a `Corrected ·` row by hand / Then the fragment holds `Corrected · R1 ·`, `Re-read · R6 ·` and `Re-read · P8 ·` rows (M1 measures the count), each citing its released row by content, and `bin/evidence-check` over the repository exits 0 with 0 drifted and 0 broken | `git diff --stat origin/release/v0.20.0 -- seal/releases/` empty; `bin/evidence-check --reverify …` exit read directly; `bin/evidence-check` exit 0; `correction-check` at the pull request (CI, unverified in this segment) |
| S5 the change is in the release note | Given the work item's `changelog.md` / When `python3 .github/scripts/gather_changelog.py --dry-run --version 0.20.0` runs / Then the fragment is gathered under `### Fixed` and refused for no `## ` line | the dry run's exit, read directly |

## Data & interfaces

- `hooks/config.py#read_table`: signature and return unchanged. Inside, the
  boolean `glued` becomes the list of glued old-header lines as written
  (`text.splitlines()[line - 1].strip()` for each row whose cells equal the
  old header), computed before the `rows` filter as today; the glued
  sentence's first f-string takes `glued[0]` in place of `named`. `named`
  stays for the "beside" sentence. The docstring gains the as-written quote
  and `#831` beside `#830`.
- `tests/test_one_word_one_meaning.py#without_the_policy_span`: the one
  `re.search` call widens; `PACT_RENAMED_SPANS`, `FOLD_MARKER` and both sweep
  cases are unchanged. R6's claim text already says "to the end of its
  paragraph", which is what this makes true.
- `tests/test_a_signer_declares_its_pact.py`: the S4 case's glued loop
  asserts `glued.replace("`| Signatory |`", f"`{quoted}`")` with `quoted` the
  first line of each `under`; the ⬜ 2 assertions are appended after
  `assert refusals == [glued]`. No new `def`, so `docs/the-pact.md`'s
  `Enforced by:` targets do not move.
- `seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md`:
  three citing rows, header-less, as `docs/the-evidence-ledger.md` says. The
  `Corrected · R1` row's notes open `Corrected 2026-10-06 by work item
  1791270163-…:` in the shape `seal/releases/0.19.0.md:6`'s notes use.

## Open questions → questions.md

Nothing here blocks the smith; `questions.md` says which judgments the tree
answered and holds one measurement and one decision for the work.

Framed 2026-10-06 by framer, before the build.
