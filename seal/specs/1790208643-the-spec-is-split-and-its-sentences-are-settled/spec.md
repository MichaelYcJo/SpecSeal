# Feature Specification: the spec is split and its sentences are settled

<!-- seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Record language: English (`seal/config.md` carries no `Record language` row).

`docs/review-chain-spec.md` is 2,238 lines and 149,096 bytes at `9f846733`
(the v0.15.0 tag, this branch's base). It is the one document over the
1,000-line ceiling `docs/the-evidence-ledger.md` §*The fold, and what tells
it from a deletion* states, frozen at 29 fold markers until #526 splits it,
and every other ticket of milestone 43 cites it. This work item splits it
into three documents along headings it already has, re-points every reader
of the moved sections, and then settles nine sentences that live in the
documents the split touches or the documents that describe the same
mechanisms — one work item, so no sentence is moved and then edited.

## What was measured, and against what

Measured 2026-09-24 by the framer, in this worktree at `21a5a98c` (the tag
plus this item's `routing.md`), with a heading walk that skips fenced
blocks. Line numbers are for opening, never for anchoring.

**The heading tree, with the size each heading owns to the next heading of
its level or above.** The ticket's *1,430-line section* is `## commit-review-
gate` (lines 435–1978, 1,544 lines here), and its bulk is one `####`,
*The declaration, and where the check went instead* (735–1938, 1,204
lines), which the ticket did not see: it holds thirteen `#####` subsections,
one per row the pull-request check reads of a round record. Those thirteen
are the seam.

| Section | Level | Span | Own | Markers |
|---|---|---|---|---|
| The cycle — the mark's unit | `##` | 18 | 18 | 0 |
| The review run has a bound, and an end (four `###`) | `##` | 326 | 31 | 4 |
| Two records, and what each of them says | `##` | 63 | 63 | 0 |
| Registration — gates run in groups | `##` | 14 | 14 | 0 |
| commit-review-gate (own prose + Which repository 172 + Why a deny 25) | `##` | 1,544 | 36 | 7 |
| — Review arm (own 39 + Where the marker goes 28) | `###` | 1,271 | 39 | 6 |
| — — The declaration, own prose (the two tables, the retired declaration, the marker, the rule, `--worktree`) | `####` | 1,204 | 71 | 1 |
| — — — `Pass` has to be checked | `#####` | 30 | | 0 |
| — — — `Fixes checked by` has to name a checker | `#####` | 86 | | 1 |
| — — — The finding id | `#####` | 20 | | 0 |
| — — — A verdict row that commissions nothing | `#####` | 140 | | 0 |
| — — — The fix range — `Fix range` | `#####` | 91 | | 0 |
| — — — The fix surface — `Contract changes` and `New units` | `#####` | 208 | | 1 |
| — — — The floor — `Loses a record or crashes` | `#####` | 53 | | 1 |
| — — — `Needs a fix` — the row the bound above rests on | `#####` | 28 | | 0 |
| — — — The reopening — one, and then the run is capped | `#####` | 116 | | 0 |
| — — — The depth in `New units` | `#####` | 69 | | 0 |
| — — — What ran the round — `Ran by` | `#####` | 72 | | 0 |
| — — — When the record was written | `#####` | 128 | | 1 |
| — — — What the record carries — a declaration (75 lines) **plus a 17-line tail that belongs to §The declaration**: *Which declaration applies is settled by the branch it names … Deleting the routing file restores today's behavior exactly* | `#####` | 92 | | 0 |
| — Parity arm | `###` | 40 | | 0 |
| review-history-guard | `##` | 20 | | 1 |
| implementer-mark · implementer-notice | `##` | 28 | | 1 |
| The survivor sweep (one `###`) | `##` | 50 | | 3 |
| The record generator (three `###`) | `##` | 150 | | 14 |
| Non-goals | `##` | 12 | | 0 |

**Who reads it.** 47 files name `review-chain-spec` outside `seal/specs/`
and `CHANGELOG.md` (measured with `grep -rl`): 28 test modules (97 lines),
14 shipped files (66 lines: three agents, four skills and two of their
scripts, four hooks, one template, five documents, both READMEs), and
`seal/ledger.md`, whose 22 rows cite 23 anchors on the document — 15
distinct headings and one paragraph. §*Data & interfaces* says what happens
to each anchor.

**How a heading anchor resolves.** `evidence_check.py#text_regions` matches
the heading LINE, whitespace-collapsed, and hashes the region from that line
to the next heading of its level or above; `#heading_level` reads the `#`
run. So a section moved to another file with its heading line and body
byte-identical is a clean move `evidence-check --reverify` re-anchors on its
own (`CONTRIBUTING.md` §*House rules*, *Renamed a cited symbol or file?*),
and a heading whose level changes is a different line and a different hash,
which the checker reports BROKEN and a person re-points. Read, in
`skills/evidence-check/scripts/evidence_check.py`, 2026-09-24.

**What the four sibling frames commit to that this item meets** (read from
their committed `spec.md` and `plan.md`, never from a working tree; each is
labelled *from a frame*):

- A (`1790206435`, at `a5c5cadd`): the sweep's reader over `.py` files and
  the released-changelog class; its §*Judgments the tree answered* 7 says a
  pure move is silent to the sweep and only a sentence reworded in the move
  is a source. E's phase 1 relies on that, and every rewording it makes is
  named below so the sweep's report is expected rather than a surprise.
- B (`1790206436`, at `421b0c0e`): edits `agents/warden.md` §*Where you
  work*, `agents/sealer.md` §*The command*, `skills/verify/SKILL.md`
  §*Capture once, filter locally*, `CONTRIBUTING.md` §*Running the checks*
  and `docs/release-checklist.md` §3. E touches `CONTRIBUTING.md` §*House
  rules*, `skills/verify/SKILL.md` §*`arm-check` asks condition 2 …* and its
  §*What the count does not say* paragraphs, and `agents/warden.md`'s one
  citation at its §Report — different sections, re-read from the merged
  base before any edit.
- C (`1790206437`, at `dfbbb614`): adds one sentence to
  `docs/review-chain-spec.md` §*The depth in `New units`* (its S13), pinned in
  `tests/test_the_report_standard_is_one_in_three_places.py#CARRIERS`, and
  one to `docs/release-checklist.md` §2. E moves that section whole, sentence
  included, and re-points `CARRIERS`. C's `depth_two` is untouched, so E's
  #222 docstring edit meets no conflict.
- D (`1790208593`, routing only at `eb7e03bf`; **no frame committed**): its
  subject is `fold_ledger.py` and the checker's glob — the mechanism #488 and
  #509's sentences describe. §*Scope* row *#488 and #509* says what E re-reads
  once D's frame lands.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*: *A top-level document under `docs/` stays at or under 1000 lines* and *One document is over that ceiling and listed: `docs/review-chain-spec.md`, frozen at 29 fold markers until #526 splits it* | The ceiling every resulting document meets, and the bullet this work rewrites: `tests/test_a_document_has_room_for_the_next_fold.py` pins the prose against `OVER_CEILING`, which becomes empty, and its A10 case says the entry cannot outlive the split |
| `skills/settle/SKILL.md` §2: *the fold either splits it first, along the headings it already has, or places the rule in the document for the rule's own sub-subject* | The split is along existing headings, and the three documents are named for the sub-subjects the folds have been sent to meanwhile |
| `CLAUDE.md` §*Repo rule — commit early*: *A row whose anchor a change removes is REMOVED, not re-pointed*; `CONTRIBUTING.md` §*House rules*: *Renamed a cited symbol or file? `bin/evidence-check --reverify .` re-anchors every row whose content provably moved intact and prints BROKEN with the destination for anything it cannot prove* | A move is a rename, not a removal: no claim goes with the code. A heading re-levelled on the move is BROKEN to the checker and re-pointed by hand with a `Re-read <date>` note; a heading moved at its level heals under `--reverify` |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*, and `docs/the-evidence-ledger.md` §*A row is a content anchor* and §*A correction a merge dropped* | The three carriers of the two sentences #488 and #509 add. The policy document is the owner and the two guides carry it; `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES` holds the guides against each other by needle, and gains the new needles |
| `tests/test_the_rules_have_one_owner.py` (the convention it pins): one carrier states a rule and every other carrier links to it by naming the owner | Five rules are owned by `docs/review-chain-spec.md` (1, 4, 8, 13, 14), with 18 link strings across seven carriers spelling that path. The split keeps every one of those five owner sentences in the file that keeps the name, so no link string and no carrier moves |
| `skills/agent-contract/SKILL.md` §8 and `tests/test_a_moved_rule_leaves_its_definition.py` | #55's three-row table is §8 now, delivered to every agent by mechanism; a definition may cite it and may not carry its sentences (a 15-word window, with the longest kept application measured at 10 and asserted `<=`). The #55 sentence in `agents/smith.md` is an application in its own words |
| `docs/review-chain-spec.md` §*The depth in `New units`*: *What no check can see is a depth declared wrong … The rule is a declaration* | #222's paragraph explains the by-file scoping the code still has (`for name in [n for r, n in added if r == f]`, `round_record.py#depth_two`), and names contract §15 as what the scoping keeps satisfiable |
| `CONTRIBUTING.md` §*What a change to a gate must carry*: a gate is *anything under `hooks/` or `.github/workflows/`* | #466's widened pin and the removed ceiling entry are test edits, not gate edits; nothing here carries the four answers. #331's census is a new instrument and is DEFERRED |
| `CLAUDE.md` §*The goal a design is chosen against* and milestone 43's own rule: *a patch release … prose edits, no design and no new gate* | Decides #331 (deferred, needs a check nobody has argued) and #466 (an existing test, one population wider) |
| `skills/implement/SKILL.md` §1: a ticket is a request, not an authority | #268 asks for nothing the tree lacks (§*Scope*, its row); #55's proposed test would violate the moved-rule check and is not planted; #526's item 2 (the `Enforced by:` retrofit) and item 3 (plugin commands) are its own checklist and not this item's (§*Out*) |

## Scope

**One line: three documents under the ceiling in place of one over it, every
reader of the moved text re-pointed, and nine sentences settled where they
now live.**

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #526 item 1 | **The split.** `docs/review-chain-spec.md` keeps its name and holds the run: the cycle, the bound and its four `###`, the three bound-checking subsections moved up under it (*The floor — `Loses a record or crashes`*, *`Needs a fix`*, *The reopening*) as `###`, *Two records* with *When the record was written* and *What the record carries* moved under it as `###`, the survivor sweep, non-goals. **`docs/commit-review-gate-spec.md`** (new) holds the hooks: *Registration*, `## commit-review-gate` with *Which repository* (and its `####`), *Why a deny*, *Review arm* (with *Where the marker goes* and *The declaration* — own prose plus the 17-line tail now stranded at the end of *What the record carries*), *Parity arm*, *review-history-guard*, *implementer-mark · implementer-notice*. **`docs/round-record-spec.md`** (new) holds the record's rows as the pull-request check reads them and the generator that writes them: *`Pass`*, *`Fixes checked by`*, *The finding id*, *A verdict row that commissions nothing*, *The fix range*, *The fix surface*, *The depth in `New units`*, *What ran the round*, each promoted from `#####` to `##`, then *The record generator* with its three `###`. Levels in the gate document are unchanged. Estimated sizes from the spans above: about 900, 505 and 880 lines (M1 measures them) | Phase 1 |
| #526 item 1 | **Every reader re-pointed.** 15 shipped files (§*Data & interfaces* lists each line), both READMEs' *Full decision tables* links, `docs/the-evidence-ledger.md`'s ceiling bullet and its declaration citation, `tests/test_a_document_has_room_for_the_next_fold.py`'s `OVER_CEILING` and `FROZEN_IDS_DIGEST` entries removed, `tests/test_docs_line_wrap.py#COVERED` and `tests/test_one_word_one_meaning.py`'s file list extended by the two new documents | Phase 1 |
| #526 item 1 | **The ledger.** 23 anchors on the document: 5 untouched (the sections that keep their file and level), 3 healed by `evidence-check --reverify` (the two arms' `###` headings, and the *Five values* paragraph — clean moves), 15 re-pointed by hand because the heading line changed level (9 to `##` in the record document; 6 to `###` in the run document), each with a `Re-read 2026-MM-DD — moved by #526's split, the claim unchanged` note and its hash recomputed by `--reverify`. Where D has moved a row into a per-release file, the row is re-pointed where it then lives | Phase 1 |
| #526 item 1 | **The 28 test modules** that read the document by path, each re-pointed by the section map in `plan.md` §*Where each section goes*; an absence assertion (`not in spec`) is re-pointed to a read over all three files, because an absence that holds in one third of the text proves nothing | Phase 2 |
| #488 | A third arm beside the two `CONTRIBUTING.md` §*House rules* already names, in all three carriers (`docs/the-evidence-ledger.md` §*A row is a content anchor*, `CLAUDE.md` §*a change writes fragments*, `CONTRIBUTING.md` §*House rules*): a branch that **edits** a unit an existing shared-file row cites — the case the 0.15.0 merge met — re-reads the drifted row and re-stamps it in the file the row is in, because that is keeping an existing claim true, which is not appending. *Appended is the word* stays; the exception widens from *removes* to *removes or edits*. Written against D's shape of the shared file, so the sentence says *the file the row is in* and never a path | Phase 3 |
| #509 | One paragraph in the same three carriers' conflict sections: a conflict's `Re-read` and `Corrected` notes are a union because each records a reading somebody performed; the anchor's hash belongs to exactly one side — the side that edited the anchored unit; run `evidence-check` after the resolution, because a drifted anchor is the tool naming which side that was. And one linking sentence at `docs/release-checklist.md`'s squash step (§0's *Squash the work items back to back*, or §1 — the phase reads which step meets the conflict) naming the owner. Needles for both go into `CONFLICT_SENTENCES` | Phase 3 |
| #55 | One sentence in `agents/smith.md`'s design-gate paragraph, beside the waiver example: the waiver is the last resort, it records something untrue of a probe, and §8 names the two shapes before it. In the smith's own words, sharing no run of 11 words with §8's body; pinned as a kept application in `tests/test_a_moved_rule_leaves_its_definition.py#test_a_citation_is_not_a_copy`. `agents/warden.md` and `agents/scribe.md` need nothing: the three-row table the ticket quotes at `warden.md:194-206` is §8 today, which prefers the Python shape and gives the call-count reason, and no test is planted for it (the ticket's case would plant §8's words into three definitions, which the moved-rule module refuses) | Phase 4 |
| #316 | One paragraph in `skills/verify/SKILL.md` after §*`arm-check` asks condition 2 of a whole module, one arm at a time*'s example, drafted from the ticket and from `arm_check.py#run_arms`'s docstring (read 2026-09-24: *bounds the WAIT and not the work*, 900 s default, an arm asks two operators so it can take twice it, only the direct child is killed, the `--tests "bin/test …"` form puts pytest one process further down): what the bound covers, what it does not reach, why the documented wrapper form is the one that leaks, and to name the pytest command directly for a module whose suite can approach the bound. The round-3 draft the ticket cites is gone with its directory (`1788936260` retired), so the ticket's own summary is the source. #313 is open and unchanged; the paragraph describes what ships | Phase 4 |
| #474 item 2 | `skills/verify/SKILL.md`'s two *this repository* sentences (at `:355` and `:360` on 2026-09-24, in §*What the count does not say* and §*The arms the plugin ships*) say *the repository this plugin is developed in* — or SpecSeal by name — so an installation reading the shipped skill is not told its own `release` job has four unmirrored steps | Phase 4 |
| #474 item 3 | `tests/test_the_gate_names_every_step_ci_runs.py`'s module docstring says #423's finding 4 was a narrow reader — three of four base spellings — naming both directions, rather than *the half* the partition case closes. The other two carriers the ticket names are gone: `1789985781`'s `spec.md` was retired by `settle`, and a pull request body is outside the tree | Phase 4 |
| #222 | One paragraph in `round_record.py#depth_two`'s docstring, beside the #333 paragraph: candidates are the units the range added in the file the finding's Location resolves in, so a case planted in another file is never a candidate — and that is what keeps the depth rule and contract §15 consistent, because otherwise no fix inside a unit an earlier round added could ever be pinned by a case. The three `seal/ledger.md` rows anchored on `depth_two` in `skills/code-review/scripts/round_record.py` drift and are re-read and re-stamped. **Closed by #559, not by this item.** An outside contribution (#559) added an equivalent paragraph and squashed first; the owner chose to take it, and the orchestrator removed this item's paragraph at the merge of `release/v0.15.1` (`4a077852`). This item keeps only the re-read notes on the `depth_two` rows, corrected to name #559's paragraph | Phase 4, withdrawn |
| #556 | Added at the spawn, after this frame was drawn. The two comments directly above the `kept_broad_gate` call in `round_record.py`'s `close` and `seal` still said a held run is always kept, and `agents/sealer.md`'s seal sentence said every earlier run is; the call replaces the newest entry where it is the same commit against the same base (`same_run`). The two comments take the issue's paste-ready blocks and the sentence reads *every earlier comparison kept behind it*. Comments and one definition sentence, no behaviour | Phase 4 |
| #268 | Verification, not an edit. The ticket says all three findings were corrected at `d860e33` and *nothing in the code* is open; `#266` is closed; `docs/issues-and-milestones.md` §*A keyword claims the one number after it* already says the hygiene workflow reports on every pull request; `close_issues_on_release.py` names #266 beside `FENCE`. Phase 4 greps for the three wrong statements (*a warning rather than a mention*, *four shapes*, *only on pull requests into main* beside the issue-claim step) and #268 closes on the report when none stands. A grep that finds one turns this row into an edit in the same phase | Phase 4 |
| #466 | `tests/test_the_contributor_has_a_procedure.py#test_no_contributor_facing_surface_names_a_concrete_release_branch` is parametrised over four surfaces. Its population becomes the files `tests/test_release_hygiene.py#LOADED` names (skills, agents, docs, templates, both READMEs, `CONTRIBUTING.md`, the two install scripts), read through that module's `tracked`, with a history allowlist of named phrases in the shape `test_release_hygiene.py` already uses for *the branch `release/v0.3.0` shipped as 0.2.0*. Measured 2026-09-24 over that population: four concrete names stand — `agents/smith.md`'s rider (`release/v0.9.3`, a dated measurement), `docs/issues-and-milestones.md:370` (history the hygiene case already protects), `skills/evidence-check/scripts/correction_check.py:23` (`release/v1.2.3`, illustrative — becomes `release/vX.Y.Z`, and `bin/correction-check:10` with it) and `:133` (`release/v0.9.3`, history). The widened case is driven red on a planted file in the new population and on `correction_check.py` before its line changes. The ticket's third bullet (drive it red over a file not already covered) is that | Phase 5 |
| #561 | Added at the resumption. `docs/release-checklist.md` §3 asks the release to compare the ledger's table-line count and `evidence_check.py --strict .`'s exit before and after the split, and nothing took the before-readings; its after-command globbed `seal/ledger/*.md`, which the fold has just emptied, so zsh printed `0`. Step 2 takes both readings before `--split`, and §3 uses one glob-free `find` in a fence, as the issue carries the fix | Phase 7 |
| #562 | Added at the resumption. A `\|` unescaped inside a ledger cell splits the row: R5 and P2, which #547's notes wrote, and twenty older rows. Each is escaped with the text otherwise byte-identical, and a case in `tests/test_release_hygiene.py` refuses a row with more cells than its table's header | Phase 8 |
| #474 item 1 | `seal/ledger.md` rows G6 and G7 of `1789985781` (their anchors: `broad_gate.py#coverage_line`, `#panel`, `#workflow_text` and two cases) gain the four cases the ticket names in `Code grounds` — `test_a_step_no_row_classifies_is_not_said_to_carry_a_reason`, `test_a_step_a_row_excludes_is_still_pointed_at_its_reason`, `test_the_two_clauses_render_together_and_hold_the_right_names`, `test_a_workflow_that_is_not_utf8_leaves_the_run_as_it_was` (all four exist in `tests/test_the_gate_names_every_step_ci_runs.py`, read 2026-09-24) — with a `Corrected <date>` note, the shape A9 and A11 of `1790174138` already take; `--reverify` hashes the new anchors | Phase 6 |
| The records | The fragment, `changelog.md`, `overview.md`, `survivors.md`, the sweep over the branch's range, `evidence-check --strict`, `unverified-check --baseline` | Phase 6 |

### Out, and where each one goes

| Left out | Why, and who answers |
|---|---|
| #331, the census and the tree-wide contradiction check | Its own body says *a census and a check, not an edit pass*, and its largest row (*does this tree contain two statements that contradict each other*) has nothing behind it. A check that reads the tree for restatements is a new instrument with a false-positive argument nobody has made; the milestone's rule sends design to 0.16.0. Nothing prose-only remains: the six words already pinned are pinned, and an edit pass without the census is what the ticket refuses. **DEFERRED** — home: #331 itself, moved to the 0.16.0 milestone by the repository owner (`questions.md` Q1) |
| #526 item 2, the `Enforced by:` retrofit of the 101 statements (and the below-cutoff folds of 0.14.0 the round-1 deferral widened it to) | 101 judgments about which check enforces each rule, across every `docs/` file; a work item of its own, as #520's frame said. The split moves markers and edits none. Home: #526's checklist, which stays open on that item after this pull request |
| #526 item 3, the shape and ceiling checks as plugin commands | A `bin/` wrapper pair and README rows `tests/test_chain_hooks_hardening.py` derives; not a prose edit. Home: #526's checklist |
| A fourth document, or splitting the record document again | `docs/round-record-spec.md` lands at about 880 lines with the generator; without the generator it is about 730 and the generator has no better home (its own first sentence says *the sections above say what each field means; this one says what the generator does about them*). Room for the next fold is about 120 lines; `plan.md` §*Alternatives* row 3 records the four-file shape as the fallback if M1 measures the estimate wrong |
| Re-levelling the gate document's headings, or renaming `## commit-review-gate (PreToolUse, Bash)` | Its `##`/`###`/`####` structure already reads as a standalone document; keeping every heading line byte-identical is what lets `--reverify` heal the two arm anchors, and `tests/test_chain_hooks_hardening.py:508` splits on `### Review arm` and `####` |
| Rewriting any moved paragraph beyond the positional references `plan.md` §*What the move has to reword* lists | A move is silent to the sweep and an edit is a source; the milestone made this one work item so that a sentence is not moved and then edited. Each rewording is named in advance so the sweep's report is the expected set |
| `docs/one-root-by-lifetime.md:515` and `.ko.md:491`, the table counting `docs/` files that mention the old roots | A record of 2026-09-02 that its own §*Decided when `settle` was built* says is not rewritten |
| `CHANGELOG.md`'s 19 mentions and `seal/specs/*` records naming the document | Released and past-state records; the sweep leaves both out (A's frame, phase 2, *from a frame*) and `CONTRIBUTING.md` §*House rules* reserves the changelog to the release branch |
| `hooks/cmdline.py`'s three mentions of `release/v0.22.0` and `tests/test_what_the_reader_understands.py:55`'s one | A concrete release name that has never existed, in files outside every population — `hooks/` and `tests/` are in neither the hygiene tuple nor the widened pin. `git log -S` says the four arrived in the initial commit. Whether the population widens to `hooks/` is `questions.md` Q2; the fact is recorded there for the owner |
| `seal/follow-up.md`'s row on a third arm for *a claim falsified by code a branch ADDED* | The #488 sentence is written as the ticket words it — *keeping an existing claim true* — which covers a correction-in-place with a `Corrected <date>` note, the shape this repository already uses. Whether that closes the follow-up row is the owner's (`questions.md` Q3); this item deletes no row of that file |
| The `Broad gate` cell, `chain_check.py`, `round_record.py` beyond one docstring, every hook | No behaviour changes. A citation in a `.py` comment or docstring is re-pointed; no code moves |
| A `.ko.md` edition for either new document | Neither the split file nor any document it cites has one; `tests/test_both_editions_carry_the_same_folds.py` pairs only where a `.ko.md` exists |

## User scenarios & acceptance *(mandatory)*

Every new case is seen red before it is committed (contract §15), and the
hand-back says how. Where a row's check is an existing module, the module
is named and its count read directly.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · three documents under the ceiling | Given the split, when `tests/test_a_document_has_room_for_the_next_fold.py` runs with `OVER_CEILING` and `FROZEN_IDS_DIGEST` empty, then every top-level `docs/*.md` is at or under 1,000 lines and the module is green; before the entries are removed the module is red on the A10 message *no longer over the ceiling* | executed; the red run recorded in `phases/phase-1.md` |
| S2 · every fold marker survives the move | Given 30 marker lines in the source file (29 live by the checker's reading, the one in a fence excluded), then the three files together carry the same multiset of live marker ids, and `settle` prints no released work item as newly unfolded | executed: `unverified_check.live_lines` + `FOLD_MARKER` over the three files, compared with the same walk at `9f846733`; `bin/settle` exit and its *already folded* list unchanged |
| S3 · the five owner sentences do not move | `tests/test_the_rules_have_one_owner.py` green with `SPEC` unchanged for rules 1, 4, 8, 13, 14; its three verdict-row and depth cases (`test_the_verdict_ruling…`, `test_the_open_verdicts_boundary…`, `test_the_depth_refusal…`) read the record document | executed |
| S4 · no citation names a section its file no longer holds | For every line naming `review-chain-spec` in `agents/`, `skills/`, `hooks/`, `templates/`, `docs/`, both READMEs and `CONTRIBUTING.md`: the section it names (§*…* or a described rule) is in the file it names. The 20 lines `plan.md` lists are re-pointed; the 46 that name a section staying in the run document are unchanged | read by the reviewer against the section map; a grep in `phases/phase-1.md` lists every line with the file it now names |
| S5 · the ledger stays true | `evidence-check --strict .` exit 0 at the close of every phase; after phase 1, 23 anchors resolve — 5 unchanged, 3 healed by `--reverify` (the heal reported by name), 15 re-pointed by hand with a dated note | executed; the `--reverify` output quoted in the phase record |
| S6 · absence assertions read all three files | Every `assert … not in spec` in the 28 modules reads a `flat` over the three documents, so a sentence forbidden in the spec cannot return in a sibling | read by the reviewer; the count of such assertions in `phases/phase-2.md` |
| S7 · heading-level pins follow the levels | `tests/test_the_reopening_is_one.py#HEADING/NEXT_HEADING/PREVIOUS_HEADING`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py#SUBSECTIONS`, `tests/test_a_record_says_what_ran_it.py`'s `##### What ran the round` become the new levels and neighbours; each module red before its edit and green after | executed |
| S8 · the sweep sees a move as silent | `survivor-check --range origin/release/v0.15.1...HEAD` after phase 1 reports only the rewordings `plan.md` §*What the move has to reword* names, each corrected in its copies or excused in `survivors.md` with grounds; a report outside that list is a sentence the move changed by accident | executed; M2 |
| S9 · #488's arm reaches all three carriers | Given `CLAUDE.md`, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md`, then each carries the *removes or edits* exception in one sentence and the *keeping an existing claim true* phrase; `CONFLICT_SENTENCES` gains the needle and `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` is red with the sentence absent from either guide | case extended, red first |
| S10 · #509's paragraph names the hash's side and the command to run | The same three carriers carry *the hash belongs to the side that edited the anchored unit* and *run `evidence-check` after the resolution*; the release checklist's squash step links to the owner; needles pinned as S9 | case extended, red first |
| S11 · #55's sentence is an application, not a copy | `agents/smith.md` says the waiver is the last resort and that §8 names the two shapes before it; `test_a_citation_is_not_a_copy` keeps the phrase and `test_the_window_sits_between_what_was_measured` still reads 10 as the longest kept application | case extended, red with the phrase absent; the window case green |
| S12 · #316's paragraph states the bound's reach | `skills/verify/SKILL.md`'s `arm-check` section says the bound is on the wait, names 900 s and *twice it*, says only the command's own process is killed, and says why the wrapper form leaks; whether a phrase is pinned in `tests/test_arm_check.py` is W4 | read; W4 |
| S13 · the shipped skill no longer says *this repository* about SpecSeal's CI | `grep -n "this repository" skills/verify/SKILL.md` no longer hits `:355` or `:360`'s sentences; the sentence at `:484`/`:548` (the measurement logs, addressed to the user's repository) is not in the class and stays | executed; the grep in the phase record |
| S14 · #474's docstring characterises finding 4 as narrow | `tests/test_the_gate_names_every_step_ci_runs.py`'s docstring says *narrow reader, three of four base spellings, both directions*, and no longer *the half* | read |
| S15 · #222's paragraph is in the docstring and the rows are re-stamped — met by #559's paragraph, not this item's (§*Scope*, the #222 row) | `depth_two`'s docstring names the by-file scoping, says a case in another file is never a candidate, and names contract §15; the three rows on `depth_two@8c7bfa47` are re-read, noted and re-stamped | read; `evidence-check --strict` exit 0 |
| S16 · #466's pin reaches the loaded files and is red on a planted name | The widened case fails over a fixture root holding `skills/x/SKILL.md` with `release/v1.2.3`, and over this tree with `correction_check.py:23` unchanged; passes after the two spellings change, with the history allowlist naming exactly the smith rider, the issues document's sentence and `correction_check.py:133` | case seen red both ways; the allowlist's three entries read |
| S17 · #474 item 1's rows name their cases | G6 and G7's `Code grounds` resolve the four cases; `evidence-check --strict` exit 0; the note names the ticket | executed |
| S18 · nothing else moves | `git diff --stat origin/release/v0.15.1...HEAD` names no file under `hooks/`, no `chain_check.py`, no `.github/workflows/`; `round_record.py`'s diff is the docstring alone | executed at hand-back |

## Data & interfaces

**The three documents.** Each opens with a title, a two-sentence account of
what it is the authority for, and the names of the other two; the
`## commit-review-gate` intro in the gate document keeps *Update spec and
code together*. The run document's opening paragraph (*Authority for
`hooks/commit-review-gate.py` and `hooks/review-history-guard.py`…*) is
rewritten to name the three files — that rewording is a source the sweep
reports, and it is expected.

**The ledger anchors on the document, and what happens to each** (22 rows,
23 anchors, `seal/ledger.md` at `9f846733`):

| Anchor | Rows | After the split |
|---|---|---|
| `"## Two records, and what each of them says"` | 1 | unchanged |
| `"### The cap bounds rounds, and not the fixes of the round it stopped"` | 2 | unchanged |
| `"### The last round verifies, and what it verifies is a diff"` | 1 | unchanged |
| `"### Where a leftover goes — the ladder, …"` | 1 | unchanged |
| `"### Review arm — opt-in: …"`, `"### Parity arm — opt-in: …"` | 1 row, both | clean move to the gate document; `--reverify` heals the path |
| `"**Five values can stand in the reach half, …"` (a paragraph) | 1 | clean move to the record document; `--reverify` heals the path |
| `"##### The floor — …"`, `"##### `Needs a fix` — …"`, `"##### The reopening — …"` (×3), `"##### What the record carries — …"` | 6 | re-levelled to `###` in the run document; re-pointed by hand |
| `"##### A verdict row that commissions nothing"` (×2), `"##### The fix range — `Fix range`"` (×3), `"##### The fix surface — …"`, `"##### The depth in `New units`"` (×3) | 9 | re-levelled to `##` in the record document; re-pointed by hand |

**Shipped lines re-pointed (20, in 15 files)** — the section each names
moves to the gate document (G) or the record document (R):
`docs/worktree-guard-spec.md:417` (G, *Which repository*);
`docs/the-evidence-ledger.md:262` (G, *The declaration*) and its ceiling
bullet at `:142`; `hooks/commit-review-gate.py:487,502` (G, *Review arm*);
`hooks/cmdline.py:1297,1375`, `hooks/mode-gate.py:63`, `hooks/routing.py:26`
(G, the unresolvable target and the standing waiver); `skills/code-review/SKILL.md:284`
(R, *The finding id*); `skills/code-review/orchestration.md:304,348` (R,
*Fixes checked by*, the fix surface's three spellings);
`skills/code-review/scripts/round_record.py:3049,3736` (R, the fix surface's
hole, the depth table); `skills/code-review/scripts/chain_check.py:552,2424`
(R, *The fix range*, the three spellings); `templates/sdd-round.md:163` (R,
the surface rows); `docs/review-handoff-protocol.md:378` (R, *The fix
surface*); `agents/warden.md:188` (R, *A verdict row that commissions
nothing*); `README.md:176` and `README.ko.md:174` (the gate tables → G,
beside the run document's link). The other 46 shipped lines name a section
that stays, and are not touched.

**Test modules, by the file their assertions now read**: run document only —
`test_the_reopening_is_one`, `test_the_run_stops_at_the_last_finding`,
`test_a_release_is_sized_by_a_criterion`, `test_the_seal_is_taken_once_by_the_sealer`
(docstring), `test_the_broad_gate_cell_keeps_every_run`,
`test_a_segment_feeds_the_flow_log`, `test_the_record_is_generated`,
`test_release_hygiene`, `test_what_the_reader_understands` (docstrings);
gate document — `test_chain_hooks_hardening` (`:507` and `:1252–1286` split
between G and the run document), `test_the_direct_answer_owes_the_sealers_record`,
`test_waiver_decided_at_start`, `test_handoff_outlives_the_merge`,
`test_gate_judges_the_repo_it_commits_to`, `test_one_word_one_meaning:131`;
record document — `test_a_finding_id_is_a_bare_integer`,
`test_a_new_returnable_value_is_a_contract_change`,
`test_a_runner_reached_unit_reads_pytest_only`, `test_the_fixes_name_their_surface`,
`test_a_record_says_what_ran_it`, `test_the_report_standard_is_one_in_three_places`,
`test_ci_gives_the_checks_what_they_need` (comment); split between two —
`test_the_rules_have_one_owner` (three cases → R), `test_the_last_rounds_fixes_are_checked`
(`:854–885` → R, the rest stays), `test_a_record_precedes_the_fixes_it_commissions`
(`:871`, `:896–901`, `:938` → R, the rest stays), `test_the_record_is_held_to_the_floor_and_the_depth`
(floor stays at `###`, depth → R), `test_the_fixes_close_the_record`
(docstrings); plus `test_a_document_has_room_for_the_next_fold`,
`test_docs_line_wrap`, `test_one_word_one_meaning:208` (lists).

**New rows** go in `seal/ledger/1790208643-the-spec-is-split-and-its-sentences-are-settled.md`:
the ceiling now met by every document (anchored on the evidence ledger's
bullet and the two constants), the widened release-branch pin (on the case
and its allowlist), the #488 and #509 sentences (on the three carriers'
headings and `CONFLICT_SENTENCES`), the #316 paragraph (on the `arm-check`
heading), the #222 paragraph (on `depth_two`; withdrawn, #559 closed the ticket), the #55 sentence (on
`agents/smith.md#"## Phases"` — which also drifts the rider stamped against
that heading; `rider_check.py --reverify` after reading it).

**Unchanged on purpose**: `hooks/*.py` (comments aside), `chain_check.py`
(comments aside), `round_record.py`'s code, `fold_ledger.py`,
`survivor_check.py`, `.github/workflows/`, `templates/` beyond one
citation, `seal/follow-up.md`.

## Judgments the tree answered

Listed so nobody reopens them; each can be overturned by opening what is
cited.

1. **Three documents, and the seam is the thirteen `#####` subsections.**
   The ticket's two-level split leaves 1,204 lines in one `####`; the
   `#####` level is where the record's rows are, one per subsection, and it
   is the level the thirteen already have. Measured above.
2. **The run document keeps the name, and the bound cluster stays in it.**
   Five owner rules and 18 link strings in seven carriers spell
   `docs/review-chain-spec.md` with a section title; the three
   bound-checking subsections (floor, `Needs a fix`, reopening) hold rule 4's
   owner sentence and the floor's, and `tests/test_the_run_stops_at_the_last_finding.py`
   says in so many words that the file owning the cap owns the floor. Moving
   them to the record document would cost the link strings in four carriers
   and `RULES[4]`; moving them up costs six anchors re-pointed and two test
   constants. The second is the cheaper edit and the truer subject.
3. **The generator section goes with the record's rows.** Its own first
   sentence points at *the sections above*; in the record document that
   stays true without an edit.
4. **`When the record was written` and `What the record carries` stay in the
   run document, under `## Two records`.** They are about the record as an
   artifact rather than a row of it; rule 8 (the moratorium) lives in the
   second and `test_a_record_precedes_the_fixes_it_commissions.py`'s
   fourteen reads are of the first. Three citations of `§*What the record
   carries*` stay true. The cost is three positional references to rewrite
   (§*plan.md* lists them).
5. **Headings are re-levelled on the move, and the ledger is re-pointed
   rather than left at `#####` for the checker's convenience.** A document
   whose every heading is `#####` fails the split's own purpose; the price
   is 15 hand re-points with a dated note, which `CONTRIBUTING.md`'s rename
   paragraph sanctions, against 3 automatic heals.
6. **#331 is deferred, whole.** Grounds under §*Out*.
7. **#466 is an existing test one population wider, not a gate.** The
   population is the hygiene tuple, which the ticket itself names as the
   candidate already enumerated; the history allowlist takes the shape that
   module already uses. Four standing names measured, two illustrative
   spellings to change, three history phrases to allow.
8. **#55 is one application sentence.** Contract §8 is the three-row table
   delivered by mechanism, and `test_a_moved_rule_leaves_its_definition.py`
   forbids the copy the ticket's own case would plant.
9. **#268 needs no edit until a grep says otherwise.** The ticket records
   corrections already made and names nothing open in the code; the fact it
   corrected about the hygiene workflow is stated correctly in
   `docs/issues-and-milestones.md`.
10. **#316's source is the ticket, not the retired round record.** The
    directory `1788936260` is gone; `arm_check.py#run_arms`'s docstring
    carries every fact the paragraph needs.
11. **#222's mechanism is unchanged by #333.** The candidate walk still
    reads `[n for r, n in added if r == f]`; #333 changed how the adder is
    named, not which units are candidates. The paragraph describes the code
    as it stands.
12. **#474 item 1 is a correction in place.** Widening `Code grounds` with a
    `Corrected <date>` note is what A9 and A11 of `1790174138` did in the
    same file and what `correction_check.py` reads.
13. **#488's sentence names *the file the row is in* and no path**, so it
    holds whichever shape D gives the shared ledger, and #509's *run
    `evidence-check` after the resolution* names the command, which D does
    not rename.
14. **The two new names.** `docs/commit-review-gate-spec.md` follows
    `docs/worktree-guard-spec.md` (a hook's spec named for the hook; the two
    smaller hooks ride with the gate they serve), and
    `docs/round-record-spec.md` names the artifact whose rows it specifies.
    Any other pair of names builds the same three files; a rename later is
    one `git mv` and the citations.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is ten
rows: three for a person, none of which blocks the build (Q1–Q3); three
measurements (M1–M3); four for the work (W1–W4).

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-09-24 by framer, before the build.
