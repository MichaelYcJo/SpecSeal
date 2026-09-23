# Feature Specification: four shipped work items wait unfolded

<!-- seal/specs/1790119502-four-shipped-work-items-wait-unfolded/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

The second run of `settle` (#514), on the population one release added. The
mechanism shipped and the first fold (#497) is the model; nothing here
invents procedure. Four released work items get their standing statements in
`docs/`, every path and every open leftover that lives only inside their
directories gets a home that survives them, and `settle --retire` removes the
four.

**Measured in this worktree at `cb07876`, by the framer, before the plan.**
`./bin/settle` reports **4 released and unfolded work items in 4 segments, 11
ungrouped, 0 skipped**, and 1 unreleased (this work item). On disk: **16
directories and 106 files** under `seal/specs/`; the four hold **71 files and
10 committed round records** of the 17.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/settle/SKILL.md` §2 | one standing statement per segment, only what is still true, the newest work item wins, flat `docs/`, merge into a document that exists, and every folded sentence carries `<!-- specs/<id> -->` on a line of its own |
| `skills/settle/SKILL.md` §3 | every population floor over `seal/specs/` is answered **retire**, **re-point** or **decline**; lowering a literal is refused by name |
| `skills/settle/SKILL.md` §4 and §*What a fold branch owes* | the retirement is the second half of the fold and never its own act; a `survivors.md` range-row is owed |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* | the marker counts only on a live line at the **top level** of `docs/` (`unverified_check.py#folded_items`, `#live_lines`) — so every destination below is a top-level file |
| `docs/release-checklist.md` §2b | a separate branch and pull request from the release-preparation commit, run by hand |
| `docs/review-chain-spec.md` §*Where a leftover goes — the ladder, and why a new issue is not the default* | how an open item that loses its directory is re-homed (G4) |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md`; any ledger row in `seal/ledger/<id>.md` |
| `CLAUDE.md` §*A row whose anchor a change removes is REMOVED, not re-pointed* and §*Re-verifying is re-reading* | governs any ledger row this branch drifts or breaks (G3) |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | folded prose uses neutral values |
| `tests/test_release_hygiene.py#test_no_loaded_file_names_a_version_at_or_above_the_running_one` | `.claude-plugin/plugin.json` reads `0.13.1`, so no sentence this branch writes names `0.13.1` or anything above it. The work item is cited instead of a version (G2, as replaced) *(Corrected 2026-09-23 in round 2's fix pass.)* |
| `tests/test_docs_line_wrap.py#COVERED` | `docs/release-checklist.md`, `docs/issues-and-milestones.md`, `docs/the-evidence-ledger.md`, `docs/measuring-a-run.md` and `docs/the-agent-set.md` are covered; every line written into `docs/` is wrapped at 88 either way, and a fold marker on its own line is exempt |

### G1 · the destination is a top-level `docs/` file, and each was chosen against the ledger

A marker written inside a `docs/` section that a `seal/ledger.md` row anchors
on drifts that row, and a drifted row is re-verified by rewriting its hash in
`seal/ledger.md` — which is how the first fold ended with 23 rows re-verified
and a ledger it had promised would be byte-identical. Measured here: the
anchored units in the candidate files are
`docs/release-checklist.md#"## 6. After the merge"` (1 row),
`docs/issues-and-milestones.md#"## A label answers *what it is about*, and survives the move"`
(4), `docs/review-chain-spec.md#"### The cap bounds rounds, and not the fixes of the round it stopped"`
(2) and `#"### Where a leftover goes — the ladder, and why a new issue is not the default"`
(1). `docs/the-evidence-ledger.md`, `docs/measuring-a-run.md`,
`docs/the-agent-set.md` and every heading of `docs/branch-and-release.md`
carry **none**. So where two destinations are equally true, the unanchored one
wins. Two edits cannot avoid an anchored unit — 1790076060's rules are
already the sentences of the cap section, and the dangling pointer in
`docs/release-checklist.md` §6 has to be rewritten where it stands — and those
drift rows that are then re-read and re-verified, never re-pointed.

### G2 · a path into a retired directory is pinned to a commit `main` keeps

`main` takes only merge commits (`CLAUDE.md` §*the merge method is fixed per
direction*; the `main` ruleset allows `merge` alone), so a commit on `main` is
never squashed away. `b0cbd34` is the merge that shipped the four work items,
it is `origin/release/v0.13.2`'s tip, and every file of the four directories
resolves there — checked with `git cat-file -e` for all four
`1790076050-…/phases/phase-N.md` files. A citation of a file this branch
removes therefore keeps its path and gains `at \`b0cbd34\``, which
`git show b0cbd34:<path>` opens. A version is not the handle, because naming
`0.13.1` in a loaded file is the timer G-row above refuses.

**SHA pin replaced — the history is rewritten into a new repository after this release; a SHA in a file would dangle.** Decided by the orchestrator during the build: each citation names the work item id and the `docs/` section carrying its marker instead (`phases/phase-2.md`).

### G3 · no ledger row anchors inside the four directories (#511)

Measured: `grep -n 'seal/specs/17900760[5-8]0' seal/ledger.md` returns
nothing, and `seal/ledger/` does not exist. The only `seal/specs/…` anchor in
the ledger is `1788184145-…/rounds/round-3.md`, a kept directory. So #511
does not bite this run — **provided this branch writes no row that anchors
under a directory it retires, or under its own**, which the next fold
retires. The plan re-checks it immediately before `--retire`.

### G4 · an open leftover whose only home is a retiring `overview.md` is re-homed first

`unverified_check --baseline` reads a removed `overview.md` as *folded*, so
an open `## Not verified` row inside one disappears with no reader noticing.
The first fold had no step for this. Each open row of the four, and where it
lives after the retirement:

| # | Row (work item) | State, measured or read | Home after the retirement |
|---|---|---|---|
| L1 | A1 — a tag push fires `publish-release.yml` (1790076050) | **observed**: run `35796549648` succeeded on `v0.13.1`, and `gh release view v0.13.1` returns the note | none needed — closed by observation, recorded in phase 1 |
| L2 | the reconcile step creates `size: now` (1790076050) | **measured false**: run `35796513013` failed at `tracker_labels.py --apply` — *description is too long (maximum is 100 characters)* — so the label does not exist and the next step, rolling the flow log, was **skipped** | an issue — `questions.md` Q1 |
| L3 | the full suite, lint, typecheck (1790076050, 1790076060, 1790076070) | **read**: each chain's last record carries it — `59a72d91`, `e62b5864`, `49ee16ad` | none — closed by those cells |
| L4 | a case red under any checkout path containing `release` (1790076050) | open | #499 already owns it |
| L5 | whether an update reaches a listed plugin on its own (1790076050) | open, a person's | `docs/release-checklist.md` §6 already states the unknown; its pointer to *the work item that built this box* is rewritten to name the repository owner |
| L6 | `CAPPED_EXIT` and `DEPTH_EXIT` still say a refused finding *becomes an issue* (1790076060) | open, a person's | a sentence in `docs/review-chain-spec.md` beside the filing ladder, naming the gap and the repository owner as who decides |
| L7 | whether a statement of the first fold dropped an overturned sentence (1790076070) | closed by that fold's review chain, two rounds | none |
| L8 | a ledger row with more than one anchor, one of them dead (1790076070) | open, a person's | `seal/ledger.md` §1788354065's S12 row and #511 already carry it |
| L9 | four new `docs/` files as the policy surface (1790076070) | shipped on its default and merged | none — the files stand |
| L10 | a network-writing command and `CONTRIBUTING.md`'s list of hook network touches (1790076080 Q3) | shipped on its default | the default becomes the standing statement in `docs/measuring-a-run.md`, where the owner can overturn it |
| L11 | the acts table's three enumerations (1790076080 *Not done*) | open | #506 already owns it |

## Scope

### In

| # | What |
|---|---|
| S1 | one standing statement per segment, in the destination the table below names, each folded sentence carrying its marker |
| S2 | the six references into the four directories resolved (below) |
| S3 | L1–L11 each given the home the G4 table names. L2's issue is the orchestrator's act before the pull request — no agent posts (`skills/agent-contract/SKILL.md` §6) — and until it exists L2 is an open row of this work item's own `overview.md` |
| S4 | the population floors re-measured after the retirement and each answered (below) |
| S5 | `settle --retire` in a commit of its own, removing **exactly** the four |
| S6 | `survivors.md` with the range-row `origin/release/v0.13.2...HEAD`; `changelog.md`; a `seal/ledger/1790119502-….md` fragment only for a claim this work establishes, anchored outside `seal/specs/` |
| S7 | `overview.md`, written in phase 1 — the frame's own `spec.md` turns `tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview` red until it exists (#379) |

### Destinations — one per segment

| Segment | Work item | Destination | What is still true, and why here |
|---|---|---|---|
| `.github/scripts/close_issues_on_release.py` | `1790076050-the-release-tail-is-three-acts-no-document-names` | `docs/branch-and-release.md` §*Cutting a release* | The rule the item established: **every act the release performs once it reaches `main` belongs to a machine or to a command that answers it** — the merge to `main` fires the label acts, the tag push fires the note, and a person runs the directory check. *(Corrected 2026-09-23 in round 1's fix pass: the frame attributed all three acts to the tag push, and the close-issues workflow fires on the merge to `main`.)* The note publishes from the gathered section, the directory is read by a command that never fails a release, and a label a document specifies is created and spent by the close-issues workflow. The file already owns the tag and holds the item's third-reader and fixed-name sentences, and no heading in it is anchored (G1). The label's own rule stays owned by `docs/issues-and-milestones.md` and is named, not restated. The statement asserts the design and **not** that the label exists — L2 measured it does not |
| `docs/review-chain-spec.md` | `1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys` | `docs/review-chain-spec.md` | The item wrote its rules as the sections themselves: the cap bounds rounds, *who owns the unit now*, the two exits named apart, and the filing ladder. Nothing later overturned them. The fold is a marker on the sentence each rule already is — a second copy beside it is the failure `settle` §2 names — plus L6's sentence. The two anchored units drift and are re-verified (G1); `docs/issues-and-milestones.md`'s `from-review` paragraph is not marked, because a marker there drifts four rows to record a sentence the destination already links |
| `seal/ledger.md` | `1790076070-the-fold-ships-and-the-corpus-is-still-on-disk` | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* | Four standing rules, and the first is load-bearing for every later fold because the directory holding it is retired here: **(a)** an ungrouped released item that wrote no `spec.md` states no rule and is kept by name, and one kept because a permanent ledger row anchors into it stays until that row is answered — the grounds for the 11 kept today; **(b)** a retirement breaks every ledger row anchored inside the retired directory; a hit the grep finds before the removal keeps the directory by (a), `CLAUDE.md`'s REMOVED rule decides only what the grep missed, and the multi-anchor case is the owner's (L8) *(Corrected 2026-09-23 in round 2's fix pass.)*; **(c)** a population floor is replaced by an independent listing of the same tree, never lowered; **(d)** a fold marker alone on its line is exempt from the wrap limit, because wrapping it stops it being a fold record. The chain checker's retirement arm is already stated in `docs/review-chain-spec.md` and is linked, not restated. No row anchors this file (G1) |
| `skills/verify/scripts/session_cost.py` | `1790076080-every-orchestrator-rule-is-a-sentence` | `docs/measuring-a-run.md` §*Where a reading goes*, and `docs/the-agent-set.md` | Where a reading goes is now one command: `session-cost … --post` refuses without a reading the session wrote, resolves the log by label through the four states, posts to exactly one open log and **never opens one** — and a command does not make anybody run it. L10's default is the rule: it is not a hook, so the list of hook network touches does not reach it. The orchestrator's acts are enumerated against their delivery in `skills/implement/orchestration.md`, held by a test that reads the marker and not the meaning — one sentence in `docs/the-agent-set.md`, which owns why the orchestrator's half is separate. Neither file is anchored (G1) |

### The references into the four directories

`grep -rnE "17900760[5-8]0"` over the tree outside `seal/specs/`, every hit
read:

| Hit | Dangles? | Answer |
|---|---|---|
| `tests/test_a_release_publishes_its_note.py:31`, `tests/test_the_release_tail_does_not_end_at_the_tag.py:32`, `tests/test_the_plugin_directory_answers_the_box.py:27`, `tests/test_a_declared_label_reaches_the_tracker.py:33` — docstrings citing `1790076050-…/phases/phase-{1,2,3,4}.md` | yes, a file path | drop the path and name the work item and the `docs/` section carrying its marker (G2, as replaced) *(Corrected 2026-09-23 in round 1's fix pass: the SHA pin G2 names was replaced during the build.)* |
| `docs/branch-and-release.md:101` — *the counts and the command … are in* `…/phases/phase-3.md` | yes, a file path | the same |
| `docs/release-checklist.md:261` — *the work item that built this box carries it as an open question* | yes, by description, and the grep does not see it | L5 — name the repository owner as who answers it |
| `CHANGELOG.md:5,72,122,182` — the four gathered markers | no | a record of a past release, and `gathered_entry` reads them |
| `seal/ledger.md:2457–2526` — the four folded sections' markers and headings | no | records; the ledger does not move |
| `seal/ledger.md` — twenty-one `Re-read … by work item 1790076060` notes and two `dropped … by work item 1790076070` notes | no | provenance naming an id, not a path; `correction_check.py` reads the date marker and nothing resolves the id |
| `seal/follow-up.md:80–83` — *measured on work item 1790076050* | no | the same kind of provenance; after the fold the id resolves to its `docs/` marker |

**Does any check resolve such paths? No.** Nothing in `tests/` or the
scripts asserts that a path named in prose exists: 26 citations of
directories no longer on disk stand in 15 files — under `docs/`, `tests/`,
`skills/`, `agents/`, `hooks/`, `.github/scripts/`, and in
`seal/follow-up.md` — today, and nothing is red (O3). The
one reader close to it is `evidence_check.py#check_records`, and it reads only
the records of a work item whose ledger fragment is on disk, for backticked
identifiers and anchor stamps — it applies to **this** work item's own
records if a fragment is written, so every identifier this frame and the
build cite must still be in the tree after the retirement.

### The population floors — re-measured, not carried

`grep -rn "seal/specs" tests/` → **160 hits in 49 modules**. The first fold
re-pointed F1–F10; each floor below was re-derived from the reader, and each
post-fold value computed by counting the tree minus the four directories.

| # | Coordinate | Floor | Now → after | Answer |
|---|---|---|---|---|
| F1, F2 | `tests/test_chain_check_at_the_pull_request.py#_the_walk_found_every_committed_record` | the walk covers what `git ls-tree HEAD` carries | 17 → 7 records, both sides | decline — green at any size, which is what the re-point bought |
| F3 | the same module's fix-range sweep | `printed_without_a_row == len(records) - len(carrying)` | 10 → **0** carriers | decline — the split holds at zero; the carrying half lives in `tmp_path` since #497 |
| F4 | `tests/test_a_finding_id_is_a_bare_integer.py#_the_corpus_covers_every_work_item_that_has_rounds` | `assert with_rounds` | 6 → 2 work items (`1788184145`, `1788395377`) | decline |
| F5, F11 | the same module, `parsed` and `assert paths` | something parsed; the corpus is not empty | 17 → 7 | decline |
| F6 | the same module, `assert teeth` | a record whose `#` cell the rule refuses | carried by `1788395377` rounds 1–4, kept | decline |
| F7, F8 | `tests/test_the_set_a_work_item_always_has.py` | fixtures | — | none; not a real-corpus reader since #497 |
| F9, F10 | `REOPEN_FROM` `1788597030`, `FLOOR_FROM` `1788472135` via `conftest.cutoff_item_is_traceable` | directory or marker | unaffected — neither cutoff is one of the four | decline |
| F12 | `tests/test_the_reopening_is_one.py`, `assert records` | not empty | 17 → 7 | decline |
| F13 | `tests/test_release_hygiene.py`, `assert items` over `routing.md` | at least one | 16 → 12 | decline |
| F14 | `tests/test_routing_is_recorded.py`, `assert found` | at least one | 16 → 12 | decline |
| F15 | `tests/test_the_pull_request_language_is_the_repositorys.py`, `assert mirrors` | at least one `pr.*.md` | 4 → 4, none in the four | decline |
| F16 | `tests/test_unverified_rows_close.py`, `>= 90` markers | over `seal/ledger.md` | unchanged | decline |

**No new floor.** Numeric floors elsewhere in `tests/` (`> 50`, `> 500`,
`> 30`) read Python files or `docs/`, not `seal/specs/`. Named readers of a
single work item (`1788501054`, `1788229400`) name none of the four. The
no-floor readers — the overview, prefix and top-level-round sweeps, the
routing-placeholder and `pr.ko.md` sweeps, the survivor corpus (5 → 2
`survivors.md`) — assert *no offender* and can only weaken.

### Out — and why, one line each

| # | Not done | Why |
|---|---|---|
| O1 | #511's repair — `settle --retire` refusing over a ledger anchor | a change to a shipped command's verdict with its own ticket and milestone; G3 answers it for this run by measurement |
| O2 | #368's repair | the same grounds as #497's O1: the retirement is staged and committed before any check runs, so the defect cannot bite |
| O3 | the 26 citations of directories already gone **before** this branch | the ticket names the five; `skills/settle/SKILL.md` §2 already says a reader traces a folded item through git history; the repair spans 15 files including `hooks/`; the orchestrator names the class in the pull request body and the owner decides whether it is an issue |
| O4 | repairing `tracker_labels.py` and re-running the skipped flow-log roll | a change to a workflow's behaviour under `CONTRIBUTING.md` §*What a change to a gate must carry*, found by this frame and belonging to no segment; `questions.md` Q1 |
| O5 | reopening the 11 kept items | #497's rule decides them, and the tree gives no reason to reopen it: the 10 still hold no `spec.md`, and `1788184145`'s ledger anchor still stands |
| O6 | marking `docs/issues-and-milestones.md` | four anchored rows drift to record sentences the destinations link (G1) |
| O7 | `docs/one-root-by-lifetime.ko.md` and every mirror | no destination is mirrored, and no check pairs `docs/` mirrors |
| O8 | lowering any floor literal | `skills/settle/SKILL.md` §3 |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 the prose exists | Given the four statements · When the prose phases close · Then `./bin/settle` lists 0 released and unfolded, the 11 kept as ungrouped, and exactly the four as folded and waiting | `./bin/settle`, read whole and compared by name |
| A2 the removal is named | When `settle --retire` runs · Then it removes exactly the four, and 12 directories remain: the 11 kept by name and this one | the command's own `removed` lines; `ls seal/specs` |
| A3 no reference dangles | Then `grep -rnE "17900760[5-8]0"` outside `seal/specs/` returns only the markers, headings and provenance notes the references table keeps, and each of the six rewritten references names the work item as provenance or the owner *(Corrected 2026-09-23 in round 1's fix pass: the SHA pin G2 names was replaced during the build.)* | the grep, read hit by hit |
| A4 every leftover has a home | Then each of L1–L11 is closed with its evidence or names its home, and L2's issue exists | phase 1's record; `gh issue view` |
| A5 the removals read as folds | When `bin/unverified-check --baseline origin/release/v0.13.2 seal/specs/` runs · Then the four removed overviews are reported **folded** and none as a deletion | its summary line, exit code read directly |
| A6 the chain checker survives | When `skills/code-review/scripts/chain_check.py --baseline origin/release/v0.13.2` runs after the retirement · Then each of the four declarations prints `retired:`, and the only error, if any, is this work item's own absent round record | exit code and output, read directly |
| A7 the survivor sweep has its row | When `bin/survivor-check --range origin/release/v0.13.2...HEAD` runs with this branch's `survivors.md` · Then it exits 0 | the hygiene step's command |
| A8 the ledger adds, removes and re-points nothing | Then `git diff origin/release/v0.13.2 -- seal/ledger.md` is empty, or holds only the hash and `Re-read` changes of rows whose anchored unit this branch edited (G1), each named in a phase record; and `bin/evidence-check --strict .` exits 0 | the diff; the command |
| A9 the floors hold | Then every module in the floor table and every real-corpus reader passes against the folded tree, and no literal was made smaller | the modules, run narrow; `git diff` of `tests/` |
| A10 the documents stay loadable | Then `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py` and the modules pinning the edited sentences are green | the named modules |

## Data & interfaces

No schema, no endpoint. Three file shapes that already exist: the
`<!-- specs/<id> -->` line, the `survivors.md` range-row, and `plan.md`'s
Status column. The citation shape G2 adds — the work item's id and the
`docs/` section carrying its marker, where the frame first wrote a path and a
commit — is prose, and nothing parses it. *(Corrected 2026-09-23 in round 2's fix pass.)*

## Open questions → questions.md

One row a person answers and it does not block; two a measurement answers.
Everything else the tree answered above.

Framed 2026-09-23 by framer, before the build.
