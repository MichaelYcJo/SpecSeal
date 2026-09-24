# Feature Specification: the sweep reads a code idiom as removed wording

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

The survivor sweep (`survivor-check`,
`skills/code-review/scripts/survivor_check.py`) reports every place at a
range's tip that still carries wording the range removed. It exists for prose
that states a rule: a document, a skill, an agent definition, a comment, a
docstring, a pinned sentence in a test. Three things it reads today are not
that, and each one costs a branch a `survivors.md` row for a sentence nobody
should correct, or a printed line addressed to nobody:

- **A line of code is a sentence to it** (#543). `for i in range(start,
  len(lines))` normalises to the same words in every reader of a line list,
  so a branch that rewrites one loop is told that every other loop of that
  shape still stands. Four of one branch's five exemption rows were this, and
  the fourth arrived from another work item's merge as a red hygiene job.
- **A released changelog section is a live carrier to it** (#307). The
  section records what a past release did, in that release's words; the
  branch that changes the behaviour it describes is reported against it, and
  a released entry is not rewritten.
- **A range row whose refs are gone is printed to every run** (#439). A
  shipped work item's `survivors.md` names `origin/release/vX.Y.Z...HEAD`,
  the branch is deleted at the release, and every later pull request and
  every seal prints `unresolved` for a declaration that could never have
  applied to it. Three such lines printed on every seal of the 0.15.0 run.

This work changes what the sweep counts as a sentence in a Python file,
puts released changelog prose in the class it already leaves out, and prints
an unresolved declaration only to the run it is addressed to. The scoring,
the floor and the exemption mechanism are not touched.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else*: *reports every place in the tree still carrying wording the range removed* | The unit is **wording**. A loop's tokens are not wording, and the fix is a narrower reading of what a Python file says, never a file kind skipped: a docstring in a `.py` file is exactly where a removed rule survives (#543 §*What a fix has to keep*) |
| The same section, third clause: *A round record is outside the sweep's corpus on both sides. A record is the write-up of a finding rather than a carrier of the claim* | A released changelog section is the same object with a different name (#307): it carries the version it was written for and quotes the behaviour it changed. It joins the class on both sides, by construction — a heading that names a version, and a fragment whose marker is in the released file — never by a path list |
| The same section, second clause: *The row is anchored on the range **and** on the work item whose `survivors.md` holds it, so it cannot become a standing check nothing* | The second anchor is what makes an unresolved declaration of another work item a line addressed to nobody: it could not have excused this run whether or not it resolved. The line is kept for a declaration this run could have used — its own work item's, or one with no owner |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*, and `CONTRIBUTING.md` §*House rules*: a released entry is amended only by a release branch based on `main` | Why the changelog carrier cannot be corrected by the branch that is reported against it, and why the wrong deny arrives on every `fix:` |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The sweep can refuse a pull request, so each phase states its failure direction, its prompt budget (zero throughout) and a case seen red first; `plan.md` §*Operational impact* carries the table |
| `skills/agent-contract/SKILL.md` §12 — a defect belongs to a class | The class in #543 is *a file whose lines are code*, enumerated by the tree's own census under §*Judgments the tree answered* 2; the class in #439 is *a declaration addressed to nobody*, of which an unresolved foreign one is the member this run meets |
| `skills/implement/SKILL.md` §1: a ticket is a request, not an authority | #543 offers three candidate mechanics; §*Judgments the tree answered* 1 says which and why the other two cannot pass the module's own founding cases |

## Scope

### In

| Ticket | What it is | Where it goes |
|---|---|---|
| #543 | In a `.py` file, only the text of comments, docstrings and string literals is sentence material. Code tokens are separators, and a code token between two literals ends the sentence, so `"a", x, "b"` is two sentences and an implicit concatenation across a line break — #269's pin, two adjacent literals — is one. The same reader serves both sides of the range and the pool. A `.py` file the tokenizer refuses is read as it is today, whole | Phase 1 |
| #307 | A released changelog section — every line under a `## <version>` heading of a `CHANGELOG.md`, up to the next `## ` heading — and a **gathered** fragment — `seal/specs/<id>/changelog.md` whose `<!-- specs/<id> -->` marker stands in `CHANGELOG.md` at the range's tip — are out of the sweep on both sides. An `## Unreleased` section and an ungathered fragment stay in, because they are this release's own prose | Phase 2 |
| #439 | `whole_range` asks the ownership question of an unresolved declaration before the report prints it. A declaration that does not resolve and belongs to a work item this range touches nothing of prints nothing and silences nothing; one with no owner, or owned by a work item the range touches, prints `unresolved` as today. The record half of #439 needs no edit: `seal/ledger.md` R7 of `1789621028` already says beside its figure that `ce0f9fe` resolves in no clone, and the `survivors.md` the ticket quotes is retired | Phase 3 |
| The records | The drifted `seal/ledger.md` rows re-read and re-stamped, the fragment, the changelog fragment, `overview.md`, the branch's own sweep | Phase 4 |
| #551 | `corrected` and `whole_range` read the range with `--no-renames`, so a file moved whole is a deletion plus an addition: the old path's sentences enter `wanted` as removed, a pure move stays silent because every one of them is written back verbatim, and a move with one sentence reworded — a rename to git, `R096` when measured — reports the reworded sentence's copy standing elsewhere. Found by this work item's Q5 probe in phase 3 and added to its scope by the owner as phase 5 | Phase 5 |

### Out

| Left out | Why, and who answers |
|---|---|
| Reading a `#` comment block as one paragraph | Today `BLOCK` reads every `# ` line as a heading, so a comment paragraph in a `.py` file is one sentence per line and an n-gram never crosses the wrap. Keeping the `#` in the extracted text keeps that reading, so phase 1's change is subtractive — code tokens gone, nothing joined that was not joined before — and its failure direction is one thing. Joining the lines would find more, in the class the sweep is for, and it changes the report on every range that removed a comment; it is its own change with its own measurement. The repository owner decides whether it is ever worth taking |
| Code in any file that is not `.py` — the `run:` blocks of `.github/workflows/*.yml`, the two `.sh` files, the `bin/` wrappers and their `.cmd` pairs, `hooks/hooks.json` | Not one of the six measured instances is in one (§*The measured state*), and no line-oriented reader exists for them the way the standard library's tokenizer exists for Python. They keep today's reading. Named so the next instance in a workflow file is a known omission rather than a surprise; the repository owner decides whether it earns a reader |
| `CHANGELOG.md` files below the root, or a changelog under another name | The released-section rule is keyed on the file's name, and the gatherer writes one file at the root. A repository keeping its changelog elsewhere keeps today's reading of it |
| Excluding `seal/specs/` wholesale, or the live files a range writes that quote old wording — `overview.md`, an ungathered `changelog.md`, a ledger fragment | #307 §*Not this* and the previous frame's *Out* row (`seal/specs/1790174139-…/spec.md`): those files assert present states and are where a corrected sentence goes on standing |
| A `seal/ledger.md` row quoting the message a case printed on the day it was written (B's range reports `seal/ledger.md:2053`) | A ledger row is a live claim by design, re-read and re-stamped rather than excluded; the previous frame excused this shape in `survivors.md` and nothing here changes that |
| Editing or deleting `survivors.md` rows already in the tree that are of the code-idiom or released-changelog class | A row whose survivor is no longer reported silences nothing by design and is not edited (the previous frame's Q2 judgment, inherited). Phase 4 counts them and the count goes in `overview.md` |
| Retiring or re-pointing the three range rows whose refs are gone (`1788938400`, `1789053786`, `1790119502`) | They are shipped work items' records; `settle` retires the directories. Phase 3 makes their lines stop reaching runs they never addressed, which is the whole of what those lines cost |
| A sentence in `docs/review-chain-spec.md` §*The fix range* about what a record states once its range stops resolving | A work item does not write policy; the statement is §*Judgments the tree answered* 5 here, and `settle` folds this spec at the release. R7's own note is the instance |
| `docs/`, `hygiene.yml`, `agents/smith.md`, `skills/code-review/orchestration.md`, the templates | None describes what the sweep reads at the level this work changes; each still says *correct each report, or answer it in `survivors.md`* and that sentence stays true |

## The measured state, before the build

Executed 2026-09-24 by the framer at `3500e54f`, over the four squash
commits of the 0.15.0 release as they stand on `main` — the range
`<squash>^..<squash>` is exactly the range each pull request was checked
over, and the four commits are reachable from `main` and from
`release/v0.15.1` in every clone — with no `--exempt`, so every place is
seen. The four commits are `576fe39d` (#537), `cc49ae64` (#538), `3dd24073`
(#539) and `d2f2c0dc` (#541).

| Range | Files, sentences removed | Places | Code idiom (#543) | Released changelog (#307) | Prose |
|---|---|---|---|---|---|
| `cbb5809..576fe39` | 372, 65 | 5 | 1 — `chain_check.py:2960`, one function body against another's | 0 | 4 |
| `576fe39..cc49ae6` | 380, 90 | 2 | 1 — `.github/scripts/fold_ledger.py:358`, a `main` body against the gatherer's | 1 — `CHANGELOG.md:2252` | 0 |
| `cc49ae6..3dd2407` | 387, 36 | 9 | 0 | 1 — `CHANGELOG.md:2090` | 8 |
| `3dd2407..d2f2c0d` | 396, 171 | 5 | 4 — the four #543 names, at 2.77, 1.77, 1.65, 1.65 | 0 | 1 — `seal/ledger.md:2041`, the real survivor of a comment the range removed |
| **Total** | | **21** | **6** | **2** | **13** |

Two facts the table settles. The code-idiom class is not one branch's: it
stands on three of four ranges, and the two outside #543 are whole function
bodies matched on assignment and `if` shapes rather than loops. And the real
survivor on A's range is a **comment** — the removed sentence is
`tests/test_a_release_is_sized_by_a_criterion.py:304`, a `#` line — which is
why *skip code files* is not the fix and why the reader keeps comment text.

The three `unresolved` lines: every `seal/specs/*/survivors.md` in the tree
holding a range row names a deleted release branch — `origin/release/v0.10.0`
(`1788938400`), `v0.11.0` (`1789053786`) and `v0.13.2` (`1790119502`); read
by resolving each here. All three work items shipped, and none of the three
directories is touched by any range that is not the fold retiring it.

Read, not re-executed: #543's own figures at `0be23b80` (1 standing, 1.77)
and `4f7dfa8b` (five excused); #307's two instances on #145's and #300's
branches; #439's `ce0f9fe` table. R7's cell re-read 2026-09-24 as the ledger
holds it.

## User scenarios & acceptance *(mandatory)*

Each row is a case in `tests/test_a_corrected_sentence_survives_elsewhere.py`
unless it says otherwise, seen red against the module as it stands before
it is planted (`agent-contract` §15), and the hand-back says how.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · a loop rewritten in one file is not reported at every other loop of that shape | Given two `.py` files each holding a generic line-list walk that scores over the floor today (shaped after `round_record.py`'s removed `section_body` scan against the four #543 carriers), when the range rewrites one, then exit 0 and the other is not named | case, red first at exit 1 |
| S2 · a docstring sentence corrected in one file is still reported where a comment or another docstring carries it | Given the same claim in a docstring and in a `#` comment of another file, when the range corrects the docstring, then exit 1 naming the comment's file | case, green before and after — the direction that would break if the reader took too much |
| S3 · #269's pin is still found, and only it | The existing case over `fixture/survivor-pin-left-behind` asserts the carrier is the one place named; the two adjacent literals are joined by the reader because nothing but line-break tokens stands between them | existing case, unchanged, and its score recorded in `phases/phase-1.md` beside today's 1.89 |
| S4 · a code token between two literals ends the sentence | Given `"first half", name, "second half"` on one line, when the range removes a sentence whose words are `first half second half`, then the line is not a carrier | case, red first |
| S5 · a `.py` file the tokenizer refuses is read as today | Given a file with an unterminated triple-quoted string, when the range corrects a sentence it carries twice, then the second copy is reported as it is today | case, red first with the fallback deleted |
| S6 · the four real ranges | Over the four squash commits, resolved at the tip: A reports `seal/ledger.md` and none of the four #543 names; 0 loses `chain_check.py`'s function body and keeps its four prose reports; C loses `fold_ledger.py` and keeps `CHANGELOG.md` until phase 2; B is unchanged at nine. Prose reports unchanged coordinate for coordinate | case over real ranges, skipped when a commit does not resolve, in the pattern of `PIN_LEFT_BEHIND`; the counts read in `phases/phase-1.md` |
| S7 · a released changelog section is not a carrier | Given a sentence corrected in `docs/a.md` and standing under `## 1.0.0 — <date>` in `CHANGELOG.md`, then exit 0 | case, red first at exit 1 |
| S8 · an unreleased section is a carrier | The same sentence under `## Unreleased`, then exit 1 naming `CHANGELOG.md` | case, green before and after |
| S9 · a range that edits only a released section removes no sentence | Given a range whose one change is a line under `## 1.0.0`, then `against 0 sentence(s)` and exit 0 | case, red first — the source side |
| S10 · a gathered fragment is out on both sides; an ungathered one is in | Given `seal/specs/<id>/changelog.md` with the old wording, when its marker is in `CHANGELOG.md` at the tip, then it is neither reported nor a source; when the marker is absent, then it is reported | two cases, the first red first |
| S11 · the docstring names the new member on both sides | `EXCLUSIONS` gains the changelog paragraph's opener and the existing case reads `pool`, `range` and `both sides` from it | existing case, red with the paragraph absent |
| S12 · B's and C's ranges lose their changelog report and nothing else | Over `cc49ae6..3dd2407` and `576fe39..cc49ae6`, resolved at the tip: eight places and one, the `CHANGELOG.md` coordinate gone from each | the S6 case extended, counts in `phases/phase-2.md` |
| S13 · an unresolved declaration of another work item prints nothing | Given a `survivors.md` under `seal/specs/<other>/` naming `origin/gone..HEAD`, over a range touching nothing in that directory, then no `unresolved` line and the exit unchanged | case, red first with the line printed |
| S14 · an unresolved declaration this run could have used still prints | The existing case (`--exempt` from outside any work item directory) unchanged; and a second with the file under the work item the range touches, printing `unresolved` | existing case unchanged, one new case green before and after |
| S15 · the branch's own seal prints zero `unresolved` lines | The sealer's `survivors` arm, run with every `seal/specs/*/survivors.md` as today, over this branch | read in the sealer's report; the count in `phases/phase-3.md` |
| S16 · the ledger still anchors | `evidence-check --strict .` at the tip, after `--reverify` over the rows §*Data & interfaces* names | the sealer's `ledger` arm |

## Data & interfaces

No interface changes: `--range`, `--root`, `--exempt` and `--floor` are as
they are, and the report's lines keep their spellings. What moves:

- **`sentences(path, text)`**, or a step in front of it, becomes the place a
  `.py` file's prose is extracted, with the standard library's tokenizer:
  the text of COMMENT, STRING and FSTRING_MIDDLE tokens kept in place, every
  other token blanked to spaces with a sentence end where it stood, line
  numbers intact the way `blank_struck` keeps them. `corrected` and `corpus`
  both read through it, so both sides of the range and the pool agree.
- **A changelog reader** beside `blank_struck`, blanking every line under a
  version heading of a root `CHANGELOG.md`; and the gathered-fragment test,
  which needs `CHANGELOG.md`'s text at the tip (one `read_blobs` call, not a
  path list — `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
  counts path lists and this adds none). Whether the class predicate grows a
  parameter or a sibling is the work's (`questions.md` Q4).
- **`whole_range`** asks ownership before it appends to `unresolved`. The
  `foreign` mechanism and its `NAMED_EXCEPTION` grounds are unchanged.
- **The module docstring** §*What is excluded, by construction rather than by
  list* gains the changelog paragraph, naming pool, range and both sides;
  and a section stating what a sentence is in a Python file.

Ledger rows whose anchors this work drifts, to be re-read and re-stamped in
phase 4 — each in `seal/ledger.md` under the work item named:

| Rows | Under | Anchors touched |
|---|---|---|
| S3, S6 | `1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks` | `corrected`, `corpus` |
| G5, G6 | `1788912166-red-for-following-the-documents-green-for-ignoring-one` | `whole_range` |
| S1, S3 | `1789211172-a-round-record-disarms-survivor-check` | `corrected`, the docstring section |
| the 12,100-survivors row | `1790076070-the-fold-ships-and-the-corpus-is-still-on-disk` | `whole_range`, `report` if edited |
| G5 | `1790138190-settle-leaves-twelve-directories-with-no-way-out` | `corrected` |
| E1–E5 | `1790174139-survivors-md-silences-what-it-quotes` | `records_a_past_state` if edited, `corrected`, `corpus`, `whole_range`, the docstring section |

Rows anchored on `STRUCK`, `blank_struck`, `BLOCK`, `FLOOR`, `runs`,
`weigh`, `weights`, `score`, `exempted`, `read_exemptions`, `RANGE_CELL`,
`OWNER_DIR` and `retired_directories` are not touched by this design, and a
phase that finds itself editing one of those units has left the frame.

New rows go in `seal/ledger/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording.md`,
anchored on the units the phases add.

## Judgments the tree answered

Listed so nobody reopens them; each can be overturned by opening what is
cited.

1. **Of #543's three candidates, the reader.** The score is already
   document-frequency weighted — `weights` is `log2(F / df) / log2(F)` — and
   the four instances cleared 1.6 anyway, because a three-word run of
   specific code is rare in a 396-file corpus for the same reason a
   three-word run of prose is; rarity is not what separates a loop from a
   rule. A per-file-kind floor has no room: #269's real survivor is a string
   in a `.py` file at 1.89, and the loops scored up to 2.77. Reading only
   prose tokens is the one candidate that keeps every founding case and
   drops all six instances, and it is enumerable by construction.
2. **The class is `.py`, and the census says so.** Of the tree's 502 tracked
   files at `3500e54f`, 172 are `.py`, 279 `.md`, and the rest are 14
   `.cmd`, 13 `.yml` or `.yaml`, 15 without an extension (14 of them `bin/`
   wrappers), 3 `.json`, 2 `.sh` and four singletons.
   Every measured instance is in a `.py` file, and Python is the one kind
   the standard library tokenizes. The rest are named under *Out*.
3. **Comment text keeps its `#`.** See *Out*, first row: the subtractive
   change has one failure direction, and a wider reading is a different
   change.
4. **A released section is identified by its heading, not by the file
   whole.** A heading naming a version — `## 0.15.0 — 2026-09-23`, and the
   `[1.2.0]` and `v1.2.0` spellings other changelogs use — opens a released
   region that runs to the next `## ` heading; `## Unreleased` opens none.
   In this repository the whole file is released sections, so the two
   readings agree here; they part in a repository following
   `agents/smith.md`'s *let the entry accumulate unreleased*, where the
   whole-file reading would drop live prose. A fragment counts as gathered
   by its marker in `CHANGELOG.md` at the tip, which is the rule
   `gather_changelog.py` already pins (`seal/ledger.md` row *A fragment
   counts as gathered when its marker comment is in `CHANGELOG.md`*); the
   sweep reads the marker itself, because a shipped script does not import
   this repository's release automation and `FOLD_MARKER` in the reader it
   already loads is the same shape.
5. **What a record states once its range stops resolving** (#439's *class,
   one level up*). The ends as measured, the instrument's version, and —
   once an end resolves in no clone — a dated note beside the figure saying
   so and why, never a re-pin and never a re-measurement passed off as the
   same one. That is the ticket's first option, it is what R7 already
   carries (added by round 3 of `1789621028`, re-read 2026-09-24 by
   `1790174138`), and it is the shape every `Corrected <date>` note in the
   ledger already takes. For a `survivors.md` range row the sweep's own
   design is the note: the row prints `unresolved` with its grounds to the
   run it addresses (G6). No person's decision is left in #439.
6. **An unresolved declaration is judged by the second anchor before it is
   printed.** `whole_range`'s own comment says a declaration that resolves
   onto a range other than this run's *needs no line: the row is honest and
   says so itself*. A declaration that resolves nowhere and belongs to a
   work item this range touches nothing of is the same fact one step over,
   and the one failure a rotting anchor must not have — quietly stopping
   applying — cannot happen to a row that never applied. The wrong allow is
   empty: an unresolved row excuses nothing whether printed or not.
7. **#526's split needs nothing here.** A section moved between files is
   removed at one path and added at another in the same range; `wanted`
   subtracts every n-gram the range wrote, so a pure move is silent by
   construction and only a sentence reworded in the move is a source. Read,
   and `questions.md` Q5 is the probe that shows it.
8. **The existing `survivors.md` rows of these two classes stay.** Inherited
   from the previous frame's Q2: a dead row silences nothing and is not
   edited. Phase 4 counts them (#307's first *Not verified* item).
9. **The fixture is the four squash commits on `main`, skipped when absent.**
   They are permanent in every clone that carries `main` or
   `release/v0.15.1`; tagging them is a push, which no agent makes, and the
   one loud case stays about the two tags the owner already pushed.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline —
unanswered questions buried in prose read as decided. The residue is six
rows and none of them is a person's: four measurements (Q1, Q2, Q3, Q5) and
two for the work (Q4, Q6).

Framed 2026-09-24 by framer, before the build.
