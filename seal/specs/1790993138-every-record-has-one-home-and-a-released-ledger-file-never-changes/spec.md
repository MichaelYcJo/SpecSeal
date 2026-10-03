# Feature Specification: every record has one home, and a released ledger file never changes

<!-- seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md
     Issue #715 and its comment. Record language: English (seal/config.md has no
     `Record language` row). Every coordinate below was opened by the framer at
     233f0455 unless it says otherwise. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | A coordinate is `path#major[>minor]@hash`, it degrades to DRIFTED and never to BROKEN below the major level, and a row whose anchor goes is REMOVED, not re-pointed. This work keeps all three. It replaces one paragraph of that section, *Appended is the word, and a removal is not one — nor is an edit*, which sends a re-read and a correction into the file the row lives in |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped* | Hunk by hunk, never a side; only the notes are a union, and the hash belongs to the side that edited the unit and to neither side where both did. This work computes that halves rule in the checker (D3), so a person no longer applies it by hand to a released file. The hunk-by-hunk rule stays for the one file two branches can still both edit: a fragment that stacked branches share |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*: the ceiling statement and *A fold is not a work item, and it adds nothing to the ledger* | `docs/commit-review-gate-spec.md` is frozen over the 1000-line ceiling *until #715*, and this work decides its cut (D7). A fold branch "changes a ledger file only by removal and re-verification". Under D1 it cannot change a released file at all, so it gets a fragment of its own (D6) |
| `docs/release-checklist.md` §*2. Gather, fold, bump* | The fold writes `seal/releases/X.Y.Z.md` and never `seal/ledger.md`. A second fold for one version joins that version's file (#540). `--split` ran once and now exits 1 with `nothing to split` |
| `docs/branch-and-release.md` (the merge-direction table) | A feature branch squashes into its release branch. So the four 0.18.0 branches meet each other only at squash time, which is where a conflict costs a re-run of the broad gate |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Two checkers change their verdicts: `evidence-check` and `correction-check`. Each change carries a case seen red, a stated failure direction and a prompt budget. The budget here is zero, because no change in this work asks a person anything |
| `skills/agent-contract/SKILL.md` §12 and §15 | The carriers of the ledger rule, the readers of the ledger files and the tests that pin rule copies are each a class, and each is enumerated by construction (§*The classes, enumerated*). Every new case is seen red before it is planted |
| `skills/implement/SKILL.md` §*Document layout*: *A work item does not create one [a `docs/` document] … The one writer that does is `settle`* | It pulls against box 1. `questions.md` Q4 decides it, with #526 as the precedent: that work item split `docs/review-chain-spec.md` and created `docs/round-record-spec.md` |
| `seal/config.md` rows `Fold shape from`, `Document line ceiling`, `Over the ceiling`; `templates/config.md` §*The fold's values* | The precedent for a cutoff written as a work-item id in a config row, which `hooks/config.py#config_rows` reads. D5's `Ledger frozen from` row follows it |
| `skills/settle/SKILL.md` §*What a fold branch owes* | A fold has no work item and so, today, no fragment. D6 changes that |
| `docs/one-root-by-lifetime.md` (skimmed: §*The proposed tree*, §*What happens at a release*) | The lifetime axis the layout is built on. That file is a dated proposal with a Korean edition, which is why box 1's document does not go there (Q4) |

## Scope

**In.** Each of the five boxes of #715 is in, and boxes 1 and 5 have the bounds stated here.

1. **Box 1: a layout document**, `docs/the-record-layout.md`. It lists each kind of record with its one home, its size target and its index (D8). For the parts this work does not build, it records the decided target and names the follow-up issue that builds it.
2. **Box 2.** A re-read or a correction of a row in a released ledger file is written into the editing branch's own fragment, and no released file changes after its release. `evidence-check` reads that (D2, D3). `--reverify` writes it (D4). `correction-check` reads a dropped correction (D3) and refuses a changed released file (D5). Each change comes with a case seen red first.
3. **Box 3.** A case shows that two branches re-reading the same released row merge without a conflict. When both branches edited the same unit, the merged tree names the row as DRIFTED (S6, S7).
4. **Box 4.** `seal/releases/` is kept, frozen, with grounds (D1). `fold_ledger.py` changes to match: `--split` is retired, and a fold into a version older than the newest release file is refused (D6).
5. **Box 5, bounded to the ledger and fragment rules.** These are the rules this work rewrites anyway: where a re-read or a correction goes, the conflict rule, the fragment rule, and the coordinate rules `CLAUDE.md` restates. Each gets one home. Every other file that states one of them links to that home and no longer restates it. The carriers are enumerated in §*The classes, enumerated*.

**Out, each with its grounds and where it goes.**

| Cut | Grounds | Goes to |
|---|---|---|
| Splitting `docs/commit-review-gate-spec.md` and lifting its `Over the ceiling` freeze | #716, which runs in parallel in this release, fixes the commit gate's reading (`--config-env`, `env -S`, an unresolved `cd`). Its natural home is that document's §*commit-review-gate (PreToolUse, Bash)* and its *Known limits*. A split landing first would conflict with #716 at its squash. So this work decides the cut (D7) and leaves the move to an issue scheduled after #716 lands. The freeze row stays as it is until then | follow-up issue F1 |
| Splitting `CHANGELOG.md` into one file per release | `CHANGELOG.md` is already the one home of release notes, because `publish_release_note.py` generates the GitHub Release from it. Its only cost is size: 549 KB, with sections at a median of 12 KB and a maximum of 33 KB (measured at 233f0455). No parallel branch writes it, so the split conflicts with nobody whenever it lands. It touches 20 Python files that name it, and none of them is on this work's critical path. D8 fixes the target | follow-up issue F2 |
| Sorting a work item's directory by lifetime | The consumers of `rounds/`, `phases/` and `survivors.md` (`round_record.py`, `chain_check.py`, the survivor sweep and `settle`) together run to more than 15,000 lines, and this frame did not read them. A layout chosen without reading them is a guess. D8 records the principle and leaves the design to that issue's own frame | follow-up issue F3 |
| The other rules `CLAUDE.md` restates: the merge-direction table (`docs/branch-and-release.md` holds the same table), *no real identifiers* (`CONTRIBUTING.md` §*House rules* holds the same rule), and the commit cadence (`skills/implement/SKILL.md` §2). Also every restated rule outside `CLAUDE.md` and `CONTRIBUTING.md` | This work does not change the meaning of any of them, so moving them buys no correctness here and adds review surface under the cap. No instrument finds a restated rule repository-wide, so that sweep needs a method of its own | follow-up issue F4 |
| `seal/follow-up.md`'s rows about `--reverify` re-stamping rows nobody opened (the row that begins *`evidence-check`'s drift report names a coordinate once*), and about a claim falsified by code a branch added | Both name the repository owner as the one who answers, and each turns on a choice of policy wording. Neither is a prerequisite of this work. D4 narrows the first one without closing it: `--into` writes one citing row per row, never one per coordinate | stays in `seal/follow-up.md` |
| `templates/ledger.md`, `templates/seal-README.md` and both READMEs | They describe the shipped plugin to another repository, where the freeze is opt-in (D5). Their text stays true. The builder changes one only if it finds a sentence there made false | — |

## The decisions, with their grounds

The owner left D1, D2 and D8 to this frame on 2026-10-03. The rest follow from those.

**D1. `seal/releases/` is kept, and every file in it is frozen once its release is tagged. `seal/ledger.md` is frozen too.** Released files are not migrated.

- **Kept.** The issue argues that the per-release split adds nothing once re-reads leave it. That is true of the split as an index. It is not true of the split as the *unit that never changes*. A file named for a release and written once by that release's fold is exactly the object box 2 asks for, and nothing else in the tree can be pointed at as "released".
- **Not migrated.** Migrating means rewriting all 37 files (measured at 233f0455: 2.42 MB in total, a median of 56 KB, the largest 225 KB). That rewrite conflicts with #647, #716 and #718, each of which re-stamps rows in those files under today's rule. It would also break every content citation into them, the D2 citations included, since a citation names its file.
- **The size problem is answered by the reading unit, not by the file.** A release file is a sequence of `### <work-item-id>` sections. All 148 sections measured at 233f0455 are at most 58 KB (median 14 KB), so the section is the unit a reader takes (D8).

**D2. A re-read or a correction of a released row is a new row in the editing branch's own fragment, and it cites the row it reads by a content coordinate.**

- **What a citing row is.** Its first cell begins with `Re-read · ` or `Corrected · `. Its `Code grounds` cell starts with a coordinate naming the released row, and the rest of that cell names the code the claim rests on now. At 233f0455, zero ledger rows begin with either verb, so no existing row is reread as a citing row.
- **The citation's shape.** It names one row the way a row names code: `seal/releases/<X.Y.Z>.md#"### <work-item-id>">"<literal unique to that row>"@<hash>` for a release file, and `seal/ledger.md#"## <area heading>">"<literal>"@<hash>` for the gathered ledger. `minor_region` narrows that to the row's own line, so the hash covers that line alone.
- **Rows without a label still work.** The literal is a prefix of the row's first cell, long enough to be unique in its section. That matters because 325 of the 1,084 coordinate-bearing rows carry no `N1 ·`-style label (measured at 233f0455).
- **A citation into a fragment is refused, and the refusal names in-place re-stamping as the repair.** A fragment is not released and moves at the fold, so a citation into one would break at the next release.
- **Why a content coordinate, and not an id or a line number.** The repository rule is that a coordinate names content, never a position. A released file never changes, so this citation never drifts — except where something breaks the freeze, and then it says so.

**D3. `evidence-check` reads the rows that cite a released row as one family.**

- **Who is in the family.** The row R, every `Re-read ·` row that cites R, and every `Re-read ·` row that cites one of those.
- **When a code coordinate is OK.** A code coordinate (`path#unit[>minor]`) is OK when one of the family's newest readings of it — the members recording it with the newest `Checked` date, ties together — recorded the current hash for it. It is DRIFTED when none did. It is BROKEN by the same rules as today. *Amended by round 1's 🟡 2; it read "when* any *member of the family recorded the current hash".*
- **A `Corrected ·` row supersedes R.** R and R's re-read family stop being checked for code drift. The correcting row starts a family of its own. The citation coordinate itself is still checked: it is BROKEN if the cited row is gone, and DRIFTED if a released file changed under it.
- **Removal is a correction too.** The case where the claim went with the code is a `Corrected ·` row whose claim cell says so and whose grounds hold the citation alone.
- **A citing row must carry a marker in its Notes.** The marker is `Re-read <date>` or `Corrected <date>`, the vocabulary `correction-check` already reads. A citing row without one is named, the way MALFORMED rows are.
- **Why a union, and not the newest reading.** The issue's text says "the newest re-read". Two parallel branches can date their re-reads the same day, and "newest" across a squash has no order. A whole-row snapshot would also drop the other side's coordinate whenever two branches touch different units of one row. The union is the halves rule of `docs/the-evidence-ledger.md` §*A correction a merge dropped*, computed rather than applied by hand:
  - the side that edited a unit is the side whose hash matches it;
  - where both sides edited the unit, neither hash matches, and the row is DRIFTED.
- **The newest reading of each coordinate decides** (round 1's 🟡 2, the orchestrator's decision). Of the members that record a coordinate, only the readings with the newest `Checked` date count, and readings that tie on that date are a union. The union over every reading accepted a pair of hashes no reading had seen together: R at (h1, o1), a re-read at (h2, o2), then `handler` alone reverted to h1 read OK at (h1, o2). Per coordinate with ties is not the whole-row "newest re-read" this decision rejects above: two parallel re-reads on one day tie, so S6 and S7 hold.
- **Failure direction: it blocks more than the plain union, in one case.** Content that returns to a hash only an older reading recorded reads DRIFTED — a partial revert, and a whole revert of one unit alike — though somebody once read the claim against it. Its cost is a re-read, never a question, which is the cheaper mistake against a false claim reading OK. Two readings dated the same day are both kept, so a revert to either reads OK.
- **`correction-check` reads the same rows.** A `Corrected ·` citing row present in a merge parent and absent from the result, while the row it cites still stands, is a loss. The cited row always stands, because it is released. Without this arm, a dropped correction silently brings a false claim back to life.

**D4. `evidence-check --reverify --into <fragment> --checked <date>` writes the citing rows.**

- **What it writes.** For every row in a released file with a drifted coordinate, it appends to `<fragment>` one `Re-read ·` row. That row carries the citation, the drifted coordinates at their current hashes, the date, and `Re-read <date>` in its Notes. It names each row it wrote.
- **What stays as it is.** Rows in fragments are re-stamped in place, as today.
- **What it refuses.** `--into` without `--checked` is refused, because a citing row with no date is a stamp nobody read. In a repository that declares D5's row, `--reverify` without `--into` writes no released file. It still re-stamps the fragments, then exits non-zero naming each released row it left and the `--into` form.
- **What does not change.** The check itself still calls git for nothing.
- **One row per row.** `--into` writes one citing row for each row, never one for each coordinate. That narrows the `seal/follow-up.md` row about re-stamps nobody read without closing it.
- **The post-commit advisor.** `hooks/evidence-advisor.py` prints the same repair.

**D5. The freeze is declared by a `seal/config.md` row, `Ledger frozen from | <work-item id>`, and `correction-check` enforces it.**

- **This repository's value.** It writes `1790993141`. That is the next id after the four 0.18.0 work items: 1790993137 for #647, 1790993138 for this one, 1790993139 for #718 and 1790993140 for #716. Each of those was read from its branch's `routing.md` path.
- **What the arm refuses.** On `correction-check --range origin/<base>...HEAD`, it refuses a change to `seal/ledger.md`, or to any `seal/releases/*.md` that existed at the merge base. The refusal is exit 1, naming each file.
- **Who the arm applies to.**
  - It applies when the range adds a `seal/specs/<id>/routing.md` whose id is at or above the cutoff.
  - It also applies when the range adds no `routing.md` at all, which covers a fold, a release preparation and a change that belongs to no work item.
  - A range whose added work items all sit below the cutoff is read under the rule it was cut under, and the report says so in one line.
- **What the arm allows.** Adding a release file. Removing a fragment. Changing the release file named for the base's own version (`release/vX.Y.Z` → `X.Y.Z.md`), which is #540's join before the tag.
- **Where it runs.** The hygiene step that already runs `correction-check` on every pull request into a release branch. It skips `main` and says why. The step itself does not change.
- **Without the row.** A repository without the row is not frozen, and today's in-place behaviour is what the shipped plugin keeps. `templates/config.md` documents the row.
- **Failure direction: it blocks more.** It does so only for work cut after the rule, and it costs no prompt, because it is a CI refusal and not a question.
- **Lowering the cutoff.** Anyone may lower it to `0` once no branch below it is open. That needs no follow-up, because a stale cutoff exempts nobody who exists.

**D6. The fold and `settle` change to match.**

- **`--split` is retired:** its code, its cases and the lines that name it in `CONTRIBUTING.md` and `docs/release-checklist.md`. It already says `nothing to split` and exits 1 on this tree, and the only act left to it is writing `seal/ledger.md`, a released file. `--check` keeps refusing a release heading in `seal/ledger.md`, with a repair that no longer names `--split`.
- **A fold into an older version is refused.** `--version` lower than the newest `seal/releases/*.md` is refused, because that would change a released file. A fold into the same version still joins (#540).
- **A fold branch gets a fragment of its own.** A `settle` fold writes its readings and its corrections into `seal/ledger/<unix-seconds>-fold.md`, and the release folds that file like any other fragment. Under D1 such a branch can no longer remove or re-stamp a released row in place.
- **What changes with it.** `skills/settle/SKILL.md` §*What a fold branch owes*, `docs/the-evidence-ledger.md`'s fold statement and `settle.py`'s per-row guidance change with it. That guidance becomes: write a `Corrected ·` row, and never remove the row.
- **Whether the readers accept such a fragment** is measurement M1.

**D7. `docs/commit-review-gate-spec.md` is cut along its own headings into three files and the parent.** F1 builds it.

| File | Takes | Lines at 233f0455 |
|---|---|---|
| `docs/the-commit-gate-inside-git.md` | §*The commit gate inside git* with *Known limits* and *Where each state of a repository stands*, including the stand-aside rule (its `Enforced by:` line names `test_the_text_reading_stands_aside_where_git_decides`) | 41–277 |
| `docs/the-review-and-parity-arms.md` | §*Review arm*, *Where the marker goes*, *The declaration, and where the check went instead*, §*Parity arm* | 760–994 |
| `docs/commit-review-gate-spec.md` | *Registration*, §*commit-review-gate (PreToolUse, Bash)* through *Why a deny*, review-history-guard, implementer-mark, and a three-line index naming the other two | 1–40, 278–759, 995–1047 |

Each part answers one question: what git decides, what the text reading decides, and what each arm wants. Each is under 500 lines. Fold markers go across whole, as #526 carried them. The `Over the ceiling` row goes away in the same change.

**D8. Size targets and the index.**

- **A file a reader is meant to take whole stays at or under 1000 lines and 64 KB.** The line half is the existing ceiling. The byte half is added because ledger rows are long lines. At 233f0455 the longest single row is 8,831 characters, which the `OLD_COORD_RE` rider measured.
- **The index is one document, `docs/the-record-layout.md` itself.** It holds one table per place: `docs/`, `seal/`, `seal/specs/<id>/`, the root records (`CHANGELOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`). Each row names a file or a file shape and the one question it answers. So a reader opens one index and one file.
- **Inside `seal/releases/`** the file name is the index, by version, and so is the `### <work-item-id>` heading inside the file. No index file is added there: it would be one more file that every release edits.
- **The kinds over target are named as such:** release files, `CHANGELOG.md` (F2), `docs/commit-review-gate-spec.md` (F1).
- **F2's target.** `changelog/<X.Y.Z>.md`, one file per release, with all 43 existing sections migrated and `CHANGELOG.md` kept as a short index that links each one. The GitHub Release reads the release's own file. Migrated, not frozen: no branch writes the changelog in parallel, and links at old tags keep resolving at those tags.
- **F3's principle.** What outlives the merge stays or folds into `docs/` and the ledger. What a review run needs only while it runs leaves the tree, or becomes one file per run. F3's own frame decides which.

## How a branch cut before this one stays valid

The question here is #647, #718 and #716, each cut at 233f0455 and each following today's rule.

- **No textual conflict.** This branch changes no file under `seal/releases/`. It changes `seal/ledger.md` once, in its header prose above the first table: one hunk, which no sibling's row re-stamp touches (S12). Its own re-reads go into `seal/ledger/1790993138-….md`, a file no other branch has.
- **Their data stays readable.** A re-stamp they make in place is a hash in a released row. D3 reads it as that row's own reading, the first member of the family, so it counts exactly as it counts today.
- **No CI refusal.** Their ids, 1790993137, 1790993139 and 1790993140, sit below D5's cutoff, so `correction-check` reads their ranges under the old rule and says so. That holds after they merge the release branch in, because the cutoff is keyed on the work item and not on the merge base.
- **What changes for them once they merge this in.** Their own `--reverify` follows the new text and refuses an in-place write to a released file, naming `--into`. Its output is valid under both rules, so the cost is one re-run of that command.
- **The one interaction that remains.** A sibling might re-stamp in place a released row that this branch's fragment already cites. That citation then drifts, and `evidence-check` names it. The repair is one in-place re-stamp of the citing row, which lives in a fragment. Whichever branch lands second meets it after merging the release branch in. Under today's rule the same pair of edits is a conflict on one line.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A re-read clears a drifted released row | Given a released row R whose coordinate X drifted, when a fragment holds a `Re-read ·` row citing R with X at the current hash, then `evidence-check --strict` exits 0 and R is not reported DRIFTED | new case, seen red against 233f0455's checker |
| S2 | A re-read is per row, not per coordinate | Given rows R1 and R2 both citing X, both drifted, when the fragment re-reads only R1, then R2 is still DRIFTED | new case, seen red with family membership keyed on the coordinate |
| S3 | A correction supersedes | Given R whose code is unchanged, when a `Corrected ·` row cites R with a new claim and new coordinates, then R's coordinates are no longer checked, the new row's are, and a stale coordinate in the new row is DRIFTED | new case, seen red |
| S4 | A citation that does not hold is named | A citation into a fragment, a citing row with neither marker, and a citation whose row is gone: each one is named (the last is BROKEN), and none is silently ignored | new cases, one each, seen red |
| S5 | `--reverify --into` writes the rows, and refuses where it must | Given a repository with `Ledger frozen from` and a drifted released row: `--reverify --into F --checked D` appends one citing row per drifted row to F and leaves every released file byte-identical; `--reverify` without `--into` leaves released files byte-identical and exits non-zero naming `--into`; `--into` without `--checked` is refused; with no config row, `--reverify` re-stamps in place as today | new cases; byte-identical asserted by sha256 |
| S6 | **Box 3**: two branches re-reading one row do not conflict | Given a git repo with released R citing `a.py#f` and `b.py#g`: branch A edits `f` and re-reads R into its own fragment, branch B edits `g` and re-reads R into its own fragment. When both merge, then `git merge` exits 0 with no conflict and `evidence-check --strict` exits 0 | new case driven from Python (contract §8); seen red with 233f0455's in-place `--reverify`, which conflicts on R's line |
| S7 | Both branches edited one unit | As S6, but A and B edit different lines of `f` and git merges them cleanly. Then the merged tree reports R DRIFTED on `a.py#f`: the halves rule, computed | new case, seen red against a "newest re-read wins" implementation, or against one that unions over every row citing the coordinate |
| S8 | A dropped correction is a loss | Given a merge whose parent's fragment holds a `Corrected ·` row citing released R and whose result does not, then `correction-check --range` exits 1 naming the fragment, the merge and R | new case in `tests/test_a_merge_cannot_silently_drop_a_correction.py`, seen red |
| S9 | A released file changed after the cutoff is refused | With `Ledger frozen from` set: a range adding a work item at or above the cutoff that changes `seal/releases/0.1.0.md` exits 1 naming it; one changing only its own fragment exits 0; a range adding no `routing.md` that changes `seal/ledger.md` exits 1 | new cases, seen red |
| S10 | What the freeze still allows | A range adding a work item below the cutoff that changes a release file exits 0 and prints the one line saying which rule it was read under; adding `seal/releases/0.2.0.md` exits 0; changing `X.Y.Z.md` on a `release/vX.Y.Z` base exits 0; with no config row the arm is off | new cases |
| S11 | The fold matches | `fold_ledger.py --split` is no longer an option; `--version` older than the newest release file is refused and writes nothing; `--version` equal to it still joins (#540 unchanged) | new and adjusted cases in `tests/test_the_ledger_fragments_fold_at_release.py`, the refusal seen red |
| S12 | This branch keeps its own rule | `git diff --name-only origin/release/v0.18.0...HEAD -- seal/releases` is empty, and the diff of `seal/ledger.md` is one hunk above its first table row | the command, run by the warden; recorded in the round record |
| S13 | **Box 1**: the layout document exists and answers | `docs/the-record-layout.md` has a row for each record kind (the evidence ledger, the changelog, a work item's files, the repository rules, the config, the follow-up list), each with a home, a size target and an index, plus the D7 cut and the F1–F4 targets marked as not built; it is under the ceiling and passes `tests/test_docs_line_wrap.py` | read by the warden against this table; the line-wrap case executed |
| S14 | **Box 5**: one home, and links | For each rule in §*The classes, enumerated* (carriers): the home states the rule's needles; every carrier names the home's path and section and contains none of the home's needles; `tests/test_a_merge_cannot_silently_drop_a_correction.py` stops holding two copies against each other and holds the home against its links | a new case, seen red by restoring one needle into one carrier; the adjusted pins executed |
| S15 | The freeze is live in this repository | `seal/config.md` carries `Ledger frozen from | 1790993141`; `templates/config.md` documents the row, what its absence means, and the cutoff's comparison | read. The framer found no case that holds every `seal/config.md` row to a section of `templates/config.md` (searched: the ten tests naming `templates/config.md`, by name only). The build either finds one and extends it, or plants a case for this row |

## Data & interfaces

**A citing row** in a fragment (five columns, as `templates/ledger.md` declares; one line):

```
| Re-read · <first words of R's claim> | `seal/releases/0.15.1.md#"### 1790260564-<slug>">"N1 · two agents alive at once"@<hash>`, `agents/warden.md#"## Where you work"@<current>` | <what was read, labelled executed or read> | 2026-10-05 | Re-read 2026-10-05 by work item <id> |
| Corrected · <the new claim> | <citation of R>, <the coordinates of the new claim> | ... | 2026-10-05 | Corrected 2026-10-05 by work item <id>: <what was false> |
```

The work decides the exact spelling of the first cell after the verb and the literal-selection rule (questions W1). The semantics in D2 and D3 are fixed.

**Commands.**

- `evidence-check --reverify --into <fragment> --checked <YYYY-MM-DD> [ROOT]`, which is new.
- `correction-check --range A...B` gains the freeze arm. Its exit codes stay 0, 1 and 2, and exit 1 now covers a lost marker, a lost correction row and a changed released file. Each kind is named in its own words.
- `fold_ledger.py`: `--split` is removed. `--version` refuses an older version.

**Config.** `seal/config.md` gains the row `Ledger frozen from | 1790993141`. It is read through `hooks/config.py#config_rows`, the reader `fold-check` uses.

**Code this builds on**, opened by the framer:

- `skills/evidence-check/scripts/evidence_check.py`: `#check_text`, `#check_ledger`, `#reverify`, `#default_patterns`, `#ledger_table_rows`, `#minor_region`, `#literal_statements`, `#text_regions`.
- `skills/evidence-check/scripts/correction_check.py`: `#rows`, `#standing`, `#losses`, `#examine`, `#ledger_listing`, `#MARKER`.
- `.github/scripts/fold_ledger.py`: `#split`, `#insert`, `#release_files`, `#fragments`, `#main`.
- `hooks/evidence-advisor.py#failing_rows`.
- `skills/settle/scripts/settle.py`: the anchor guard, which reads `seal/releases/*.md`.
- `.github/workflows/hygiene.yml`: the step *no merge on this branch dropped a correction the ledger had made*.

## The classes, enumerated

Each class is enumerated by construction (contract §12). The builder re-runs each instrument at its phase, because the corpus moves.

**Carriers of the ledger and fragment rules**, from `git grep -l -- '--reverify'` and `git grep -n 'file the row is in\|row stands'` outside `seal/releases`, `seal/specs` and `CHANGELOG.md`, filtered to those that state a rule:

- `CLAUDE.md`: §*Repo rule — commit early*, its coordinate paragraphs; and §*Repo rule — a change writes fragments*.
- `CONTRIBUTING.md` §*House rules*: the fragment bullet and its command block.
- `docs/the-evidence-ledger.md` (the home).
- `docs/release-checklist.md` §2.
- `docs/branch-and-release.md`: its fold sentences.
- `skills/implement/SKILL.md` §2.
- `skills/settle/SKILL.md`: §*What a fold branch owes*, and the anchored-row paragraph.
- `skills/evidence-check/SKILL.md`.
- `skills/code-review/orchestration.md`: its `--reverify` mention.
- `seal/README.md`.
- `seal/ledger.md`: the header.
- `.github/scripts/fold_ledger.py`: the docstring.
- `skills/evidence-check/scripts/correction_check.py`: the docstring.
- `hooks/evidence-advisor.py`: the printed repair.
- `skills/settle/scripts/settle.py`: the printed guidance.

**Homes.** Where a re-read or correction goes, the families, the conflict rule and the coordinate rules live in `docs/the-evidence-ledger.md`. The fragment rule (which file a change writes) lives in `docs/the-record-layout.md`. The fold commands live in `docs/release-checklist.md` §2.

**Readers of the three ledger addresses.** These come from `git grep -n '"releases"\|seal/releases\|RELEASES' -- '*.py' ':!tests/'`: `evidence_check.py#default_patterns`, `correction_check.py` (`RELEASES`), `fold_ledger.py`, `settle.py`, `survivor_check.py#LEDGER_SHAPES` and `hooks/evidence-advisor.py`. Each is checked to see whether it misreads a citing row. Only the first two change in meaning.

**Tests that pin a copy of a moved rule.** Every test that reads `CLAUDE.md` or `CONTRIBUTING.md` (24 files at 233f0455, listed by `git grep -l -E '"CLAUDE\.md"|"CONTRIBUTING\.md"' -- tests/ .github/`) is filtered to the assertions whose needle belongs to a moved rule. Known members:

- `tests/test_a_merge_cannot_silently_drop_a_correction.py`: `CONFLICT_SENTENCES`, `EDIT_OUTCOMES`, `test_a8_*`.
- `tests/test_the_changelog_is_gathered_at_release.py#test_the_documents_send_a_change_to_its_own_fragment`.
- `tests/test_the_ledger_fragments_fold_at_release.py#test_the_release_sequence_names_the_fold_beside_the_gather` and its `--split` cases.
- `tests/test_a_row_points_by_content.py#test_no_document_claims_the_checker_never_calls_git`, which requires `CLAUDE.md` and `seal/ledger.md` to state the no-git property.

The rest is questions W2.

## Open questions → questions.md

Every row there is either decided by this frame, with its answer written in, or belongs to a measurement or to the work. None blocks the build.

Framed 2026-10-03 by framer, before the build.
