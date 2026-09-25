# Feature Specification: the survivor sweep reads removed and moved text as a correction (#603, #591, #592)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three defects in `skills/code-review/scripts/survivor_check.py`, all in how
`corrected` decides which removed sentences are corrections and which
departures a move pairs with. Each one changes either the sweep's verdict or
the line a person follows to find a correction.

| Issue | What goes wrong today | What this work changes |
|---|---|---|
| #603 | A range removes a ledger row because its anchor left the code. The row's cells count as removed wording, and every live document still stating the rule is reported as a survivor. Measured on #587 (`58629718^..58629718`): exit 1, eight places, every one sourced from the three removed rows | A ledger row the range removed, where one of its anchors resolved at the left end and does not at the right, takes no part in the removed wording. The same range reports 0 |
| #591 | A retired work item directory is dropped from the range before the cross-path pairing runs. A sentence a fold carries verbatim from the retired spec into `docs/` therefore counts as the range's own writing. It can pair with, and subtract, a correction the same range made elsewhere | The retired side takes part in the pairing and leaves the range after it, so fold-carried text is held, not written |
| #592 | A key removed at two paths and added at one pairs with whichever departure comes first in path order. When one departure was a correction and the other a move, the `corrected` line can name the path that only moved | A departure is paired with the path it shares the most keys with, so a move pairs with its own origin and the correction stays the source |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*Repo rule — commit early; on a declared branch it costs nothing*, **A row whose anchor a change removes is REMOVED, not re-pointed.** *Its claim went with the code.* | Decides #603. A removed row's claim went with its code, so the row's removal is not a correction of any document that still states the rule. It also fixes WHICH removals take the exit: a row whose anchor left. A false row is corrected in place with a `Corrected <date>` note (same file, §*a change writes fragments*), so a removed row whose anchors all still resolve is an act no rule describes. It stays measured, which is the loud direction |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* (*Only the major level can be broken*; *A row whose anchor a change removes is `REMOVED`*) and `skills/evidence-check/scripts/evidence_check.py#resolve_unit` | *Anchor left* means what the ledger checker already means by it: the major unit resolves at `a` and does not at `b`. It is loaded from that module, never re-derived, the way `reader()` loads `unverified_check.py` |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*: *a row whose every anchor goes is REMOVED … a row that keeps a live anchor beside the dead one loses only the dead one, and whether it should be removed instead is the repository owner's question* | The two removals the ledger's rules permit both follow an anchor leaving: every anchor gone, or some gone and the owner choosing removal over narrowing. A claim found false is corrected in place, never removed. So the exit's condition is **at least one anchor left**, not every anchor (judgment 1) |
| `docs/review-chain-spec.md` §*What the sweep reads, and what it counts as written*, **The sweep reads only wording that still instructs somebody** … *What is left out is left out by its shape, never by a list of files* | #603's exit is a shape (a live ledger row whose anchor left), not a list. This statement gains one clause naming it |
| same section, **Only wording the range itself wrote is subtracted from what it removed.** *A sentence moved verbatim to another path … is held and never written, because a move changes no sentence's author* | Decides #591: text a fold carries verbatim is a move, and the range is not its author. It also decides #592: the rule is about whose writing a sentence is, so a pairing that credits a correction's departure to a move misstates the author |
| `skills/settle/SKILL.md` §*What a fold branch owes*, *A sentence the same branch removes from anywhere else is measured as before* | #591 is the case where that sentence is not quite true today: a verbatim fold arrival can pair with and hide such a removal. After this work the sentence holds as written. No edit is owed there unless a phase makes it false |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Each phase carries a test seen red, a failure direction, a prompt budget and a platform note. `plan.md` gives all four per phase |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | §12: each issue is a class, and each phase names its members. §14: #592 changes a printed coordinate and #603 changes a verdict, so each is pinned in the commit that changes it, with the docstring and the `docs/` statement. §15: every new case is shown red against the unfixed code |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | New ledger rows go in `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`. Rows in `seal/releases/*.md` whose anchored units this work edits drift, and each is re-read and re-stamped in the file it lives in, corrected in place first where the edit made it false. The changelog entry goes in this directory's `changelog.md` |
| milestone 46's description (`gh api repos/{owner}/{repo}/milestones/46`) | A patch release: fixes to instruments, no new gate. Every refusal this work adds enforces a rule a document already states. No new CLI flag, no new report section |

## The judgments the tickets left open, decided from the tree

Each has its grounds, and each can be overturned by opening the same sources.
None is in `questions.md`.

1. **#603: the exit is "an anchor left", not "the row is gone".** A plain
   "every removed ledger row" exit would also drop a row corrected in place:
   its old line is removed and its new line added, so at line level it looks
   the same. That is the one ledger act that IS a correction, and dropping it
   is the silent direction. So a row takes the exit only when (a) it is a live
   table row in a ledger file at `a`, (b) its line is not in that file at `b`,
   and (c) at least one `path#locator` anchor in it resolves at `a` and does
   not resolve at `b`. **Measured** (executed, probe
   `test_tmp_603_probe.py`, deleted): on `58629718^..58629718` nine row lines
   are gone from every ledger file. Exactly three meet (c):
   `seal/releases/0.14.0.md` S1 and P1 and `seal/releases/0.15.1.md` S1, the
   three the range's own notes call REMOVED. The six edited rows stay
   measured. The removed sentences drop from 98 to 52, and the survivors from
   8 to 0.
   **Why at least one anchor, not every anchor.** Measured on the same
   range: each of the three removed rows kept live anchors at `b` (4 of 7,
   4 of 7, 1 of 4). An "every anchor left" exit takes none of them and
   leaves all 8 places reported, so it does not fix the issue's own
   instance. It is also not what the ledger's rules require: both removals
   they permit follow an anchor leaving (Grounding, the evidence-ledger
   fold row).
2. **#603: ledger files are the four locations `evidence_check.py#default_patterns`
   names**, read as committed path shapes: `seal/ledger.md`,
   `seal/ledger/*.md`, `seal/releases/*.md`, and the pre-0.10
   `docs/**/_evidence.md`. Local mode is never committed and never reaches a
   range, as `WORK_ITEM_DIR`'s comment already says.
3. **#603: a row counts only on a live line**, read through
   `unverified_check.py#live_lines` as `gathered_fragments` reads its marker.
   A row quoted in a fence or an HTML comment is an example, not a claim, and
   it stays measured. That is the direction a person sees.
4. **#591: it is #563's class, and the fix is order, not a new rule.**
   **Measured** (executed, probe `test_tmp_591_probe.py`, deleted) on #581's
   real fold range, `f673e3b1..8e13036c`, and again on its squash on `main`,
   `3c3f2342^..3c3f2342`, with identical results. 25 directories retire. Only
   2 of the 178 sentences the range writes at live paths carry a key that
   left a retired spec, and both are in `seal/releases/`, not `docs/`. Moving
   the retired side into the pairing subtracts 0 fewer n-grams and leaves the
   verdict identical: 0 survivors, and the same 27 rows at a floor of 1.0.
   **The issue's premise does not hold on its own instance.** That fold
   rewrote its statements into the Enforced-by shape rather than carrying
   them verbatim. The class is still reachable wherever a fold carries a
   sentence verbatim, and the fix only ever moves toward reporting (see 6),
   so it is built rather than closed.
5. **#592: pairing prefers affinity, then a departure from a path gone at `b`,
   then path order.** The affinity of a departure path P to an arrival path Q
   is the number of distinct keys that left P and arrived at Q. A file moved
   or a document split shares many keys with its destination. A correction
   shares at most the one key with the move's destination. The second
   tie-break covers a one-sentence move, where both affinities are 1: the
   moved file is gone at `b` and the corrected one is not. A retired
   directory is always gone at `b`, so the same order serves #591's
   one-sentence fold.
6. **The failure direction of the pairing changes is toward reporting.**
   Adding the retired side and removed rows as competing departures can only
   take pairings away from live departures, which keeps them as sources. It
   also takes their arrivals out of `written`, which can only grow `wanted`.
   Choosing a different departure for the same key changes the source's path,
   not its n-grams, so the score is identical and only the `corrected`
   coordinate moves. The one exception is the one `paired_across_paths`'s
   docstring already states: a larger `wanted` can merge two runs into one.
7. **The report prints nothing new.** The retired-directory exit prints
   nothing today, and the removed-row exit follows it. A count line was
   considered (`plan.md` *Alternatives considered*).
8. **The existing `docs/` statements are corrected in place, with no fold
   marker**, as work item 1790260564 did for the same two statements.

## Scope

**In:**

- `skills/code-review/scripts/survivor_check.py`: `corrected`,
  `paired_across_paths`, and one new predicate for the removed-row exit.
  The predicate loads `evidence_check.py` by path only when the range touches
  a ledger file, and a missing sibling is refused with exit 2 as `reader()`
  refuses. The module docstring's §*What is excluded, by construction rather
  than by list* and §*A retirement is out of the range, so a fold owes no row*
  are updated to match.
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: the new cases
  below, and any pinned count or coordinate that moves (`questions.md` Q1).
- `docs/review-chain-spec.md` §*What the sweep reads, and what it counts as
  written*: both statements, and each `Enforced by:` line gains the functions
  that now enforce it.
- The ledger fragment and the drifted `seal/releases/*.md` rows, as in
  Grounding.
- `seal/specs/1790297084-…/changelog.md`.

**Out, with the reason:**

- **`skills/evidence-check/scripts/evidence_check.py`**. This work reads
  `ANCHOR_RE` and `resolve_unit` from it and edits nothing there. Work item E
  of this release (#299) edits that file. If E changes `ANCHOR_RE`, the two
  meet at the release branch, not here.
- **A verbatim survivor with no rewording scores at most 1.0 and is never
  reported.** That is a property of the score (the `FILLER` comment in the
  test file says so), and every scenario below is built with a correction
  that rewords. Changing it is a design change to the floor, not an
  instrument fix.
- **The eight rows in `seal/specs/1790260563-the-fold-checks-run-only-as-this-repositorys-tests/survivors.md`**.
  After this work they excuse nothing the sweep still reports. A row that
  matches nothing prints nothing and costs nothing. That directory is
  retired by its own fold.
- **A gathered changelog fragment's text in the pairing.** `shipped` and the
  held path already settle it (#557), and neither issue names it.
- **`skills/settle/SKILL.md` and `docs/release-checklist.md`**. Both were read
  and both stay true (Grounding). A phase edits them only if it makes one
  false.
- **Any report line, flag or exit-code change.** Out, per the milestone.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · #592, the correction is named | Given a range that corrects FOUND→REPAIRED in `docs/a.md` and moves `docs/m.md` (the same sentence) to `docs/z.md`, with `docs/b.md` still carrying it. When the sweep runs. Then each report's `corrected` line names `docs/a.md`, the places and scores are unchanged, and the exit is 1 | A case in the test file; red today (names `docs/m.md:3`) |
| S2 · #592, path order does not decide | Given S1 with the names chosen so the moved file sorts first (e.g. `docs/0.md` moved, `docs/q.md` corrected). Then `corrected` still names the corrected file | A case; shows the fix is not the order |
| S3 · #592, a one-sentence move | Given a moved file holding only the one sentence (affinity 1 on both sides). Then the departure from the path gone at `b` is the one paired, and `corrected` names the corrected file | A case |
| S4 · #591, a verbatim fold hides no correction | Given a range that retires a work item directory whose `spec.md` holds sentence S, folds S verbatim into `docs/b.md`, and corrects S (reworded) in `docs/a.md`. When the sweep runs. Then `docs/b.md` is reported with `corrected` naming `docs/a.md`, and the exit is 1 | A case built on `retired_range`; red today (exit 0) |
| S5 · #591, the retirement alone stays silent | #517's A8 and its siblings (`test_a_retired_directory_is_not_corrected_wording`, `test_a_sentence_the_same_range_removes_from_docs_is_still_measured`, the rule-arm cases) | Existing cases, unedited and green |
| S6 · #591, the real fold range | `f673e3b1..8e13036c` (or `3c3f2342^..3c3f2342`) reports what it reports today: 0 survivors | Measured in the phase, recorded in `phases/phase-2.md` |
| S7 · #603, a removed row's cells are not a correction | Given a ledger row anchored on `pkg/mod.py#helper`, and `docs/x.md` restating the row's claim. When a range deletes `helper` and removes the row. Then nothing is reported and the exit is 0 | A case; red today (exit 1) |
| S8 · #603, a row corrected in place is still a correction | Given the same row, when the range rewords its claim cell (FOUND→REPAIRED) and re-stamps it, with `helper` still present. Then `docs/x.md` is reported | A case; green today, and it must stay green. Shown red against a mutation that exits every removed row line |
| S9 · #603, a row removed while its anchors resolve stays measured | Given the row removed and `helper` kept. Then `docs/x.md` is reported | A case; shown red against a mutation that drops condition (c) |
| S10 · #603, an anchor that left a file that still exists | Given two anchors, one unit removed from a file that remains (0.15.1 S1's shape). Then the row takes the exit | A case |
| S11 · #603, a row in a fence or an HTML comment | Given the removed "row" inside a fenced block or an HTML comment of a ledger file. Then its cells stay measured | A case |
| S12 · #603, a removed row's text still pairs | Given a removed row whose claim cell arrives verbatim in the work item's new fragment row. Then the arrival is held, not written, as any move is | A case, or covered by S7's construction; the phase says which |
| S13 · #603, the real range | `58629718^..58629718` reports 0 survivors | A case over the real commit that skips when the commit is absent, as the module's other real-commit cases do; red today (8) |
| S14 · every existing case | The whole test module, and `RELEASE_RANGES`' pinned coordinates | Re-run at each phase boundary; a coordinate that moves is explained coordinate for coordinate (`questions.md` Q1) |

## Data & interfaces

No CLI, flag, exit code or report section changes. What changes:

- `paired_across_paths(gone, fresh)` gains what it needs to order the
  departures: affinity is computable from the two lists alone, and "gone at
  `b`" needs the set of paths present at `b`, which `corrected` already reads
  (`after`).
- `corrected` builds `gone` and `fresh` over every path of the range,
  retired directories included, pairs once, and only then drops the
  departures that take an exit: a retired directory's, and a removed ledger
  row's. Nothing is added to `fresh` from a retired directory, which is gone
  at `b` by definition.
- A new predicate names the removed ledger rows of a range. It is a
  `(path, line at a)` set, or the equivalent, computed from the ledger files
  in the range's path list, their blobs at `a` and `b`, and the blobs of the
  anchors' paths at `a` and `b`.
- Ledger rows this work anchors go in the fragment. The coordinates are
  `path#unit@hash`, never a line.

## Open questions → questions.md

No row needs a person. Two measurements and one piece of the work are
there, each with the default the build proceeds on.

Framed 2026-09-25 by framer, before the build.
