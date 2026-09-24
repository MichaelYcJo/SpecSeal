# Round 1 report — the spec is split and its sentences are settled

Target SHA `ca9314de`, base the release branch at `06f10aaa`, whole-branch
review of `origin/<base>...ca9314de`. No earlier rounds. Reviewed in a
`git clone --no-local` at the target under the session scratchpad; nothing
was written in the worktree except this file.

## What the handoff claimed, and what the code does

- **The move is clean (claimed; confirmed, executed).** A section-by-section
  diff of the base's `docs/review-chain-spec.md` against the three new files,
  keyed by heading text with fences skipped, finds every old heading exactly
  once, the levels `plan.md` §*Where each section goes* names, and body
  differences only in: the three openings; the rewordings `phases/phase-1.md`
  lists (the plan's rows, the corrected *floor* row and the six extra); the
  declaration's tail moved whole (35 lines, as `overview.md` says, not the
  frame's 17); and two re-wraps in §*Which repository* with no word changed.
  No unlisted rewording exists.
- **29 fold markers, id and digest unchanged (claimed; confirmed, executed).**
  The multiset of live marker lines is identical, 9 / 4 / 16 across the three
  files.
- **878 / 523 / 885 lines (claimed).** `wc -l` at the target reads 879 for the
  run document; the smith's figure was taken at phase 1. All three are under
  the ceiling.
- **30 test modules re-pointed (claimed in the PR body).** Phase 2's
  population is 30 modules that name the document, but the diff edits 27
  `tests/test_*.py` plus `tests/conftest.py`: one module names the base
  commit's tree on purpose, and the run-stops module was reverted. The PR
  body over-states; the tree is right.
- **The absence checks read all three documents (claimed; confirmed,
  executed).** Planting *There is no third case to run away* in
  `docs/round-record-spec.md` and *oldest commit that touched* in
  `docs/commit-review-gate-spec.md` turned both cases red, and the files were
  restored. A scan of every test function that reads one of the three files
  found no `not in` assertion over the spec still reading one file.
- **#561 (claimed 1047 three times; confirmed as equality, executed).** In
  zsh on a scratch clone at the target, the checklist's `find` reads 1061
  before `--split`, after it and after `--version 1.2.3`, and the strict
  checker exits 0 each time; the old after-command prints `no matches found`
  and `0`. `git grep` over the same files reads 1047 at `eaba2dd1`, so the
  smith's figure is the count at phase 7 and the later rows explain the
  difference.
- **#562 escapes only (claimed; confirmed, executed).** Both ledger files of
  `28439296` equal their parents once `\|` is read as `|`.
- **The #488/#509 carriers (claimed; read).** Present in all four carriers
  and the checklist, and the needles are in both guides. Two defects in what
  the sentences say are findings 1 to 4 below.
- **#55, #316, #474, #556, #268 (claimed; read).** Each sentence matches the
  code it describes: `arm_check.py#run_arms` (the 900 s default, the
  direct-child kill), `.github/scripts/run_tests.py` (pytest as a
  subprocess), `round_record.py#kept_broad_gate` and `#same_run`. #268's
  three greps find nothing standing. The one *four shapes* hit, in
  `broad_gate.py`, is about another subject.
- **S18 (the smith asks for a reading).** Every hook hunk is a comment or a
  docstring. I read S18 as *no behaviour under `hooks/`*, and it holds.

## Findings — from reading

The halves rule and the edit arm are new sentences in the policy document
and its three copies, so each defect is written twice: once where the owner
states it, once where the copies carry it.

### 🟡 1 — the halves rule says the hash is exactly one side's, and this branch's own merge met the case where it is neither's

`docs/the-evidence-ledger.md:98`. *The anchor's hash belongs to exactly one
side: the side that edited the anchored unit* holds only when one side
edited the unit. When both sides edited it, the merged unit is content
neither side hashed. The procedure then says to re-read the row *against that
side's edit*, which leaves the other side's edit unread. That is not a
hypothetical case: `75b226a7` re-read *nine anchors both sides edited* after
`4a077852`. Row F1, for example, went from this branch's `9ceb2e34` to
`c6fe69c1`, which is neither side's hash. The fix keeps both needles.

The same paragraph also ended up in the wrong place (finding 5), so the
paste-ready block moves it too.

### 🟡 2 — the two guides carry the same *exactly one side*

`CONTRIBUTING.md:255` and `CLAUDE.md:168`, together with the changelog
fragment's #509 entry (a record, corrected in passing). The same sentence
appears in each, and a reader following a guide does what finding 1
describes. `CLAUDE.md` is the orchestrator's to edit.

### 🟡 3 — the edit arm re-stamps every edit, including one that made the claim false

`docs/the-evidence-ledger.md:47`. *An edit drifts the row, and the branch
re-reads it against that edit and re-stamps it there* names one outcome for
every edit. `CONTRIBUTING.md` §*House rules* says the choice between the two
answers *is about the claim rather than the code*, and the guides are held to
agree with the owner. The owner is keyed to the code act instead. So an edit
that falsifies a claim is sent to a re-stamp, which re-certifies a false
claim with a fresh hash. This branch's own phase 6 corrected G6, G7, G1 and
A5 in place with `Corrected` notes. That is neither a re-stamp nor a removal,
and it is the shape `spec.md` §*Out* relies on the sentence to cover (the
`seal/follow-up.md` row, Q3). The smith can answer this one with grounds if
*re-reads it against that edit* is meant to carry the correction.

### 🟡 4 — `CLAUDE.md`'s copy of the edit arm has the same single outcome

`CLAUDE.md:138`: *an edit drifts the row, which is re-read against that edit
and re-stamped there with a dated note*. This is the same defect as finding 3,
in the orchestrator's file.

### ⬜ 5 — *Nothing downstream can see that* now points at the paragraph that says the checker sees it

`docs/the-evidence-ledger.md:107`. The halves paragraph was inserted between
the #424 paragraph and the paragraph whose *that* refers to it. The paragraph
right above *Nothing downstream can see that* now ends by saying
`evidence-check` names the row. Both guides put the halves paragraph after
the `correction-check` paragraph, which is the placement the fix for
finding 1 takes.

### ⬜ 6 — the record document cites *this document's `blocks more` default*, and holds none

`docs/round-record-spec.md:529`. The only `blocks more` statement is the
reopening's, which stayed in `docs/review-chain-spec.md` (`:447`). This
positional reference moved and was not reworded.

### ⬜ 7 — the gate document's new pointer sends *every row* to the record document

`docs/commit-review-gate-spec.md:340`. The floor, `Needs a fix`, the
reopening and `Written late` are refused at the pull request by
`docs/review-chain-spec.md`'s sections, as `docs/round-record-spec.md`'s own
opening says. Its enumeration class has one more instance, the docstring in
finding 9.

### ⬜ 8 — the #316 paragraph describes SpecSeal's own `bin/test` in the shipped skill, the class #474 item 2 corrects in the same file

`skills/verify/SKILL.md:80`. *`bin/test` execs `.github/scripts/run_tests.py`*
is true of SpecSeal and of no installation reading the skill. The guidance
itself (name pytest directly) is right. Two sections down, this branch
rewrote *this repository* to *SpecSeal's own* for the same reason.

### ⬜ 9 — a re-pointed docstring says the record document owns every refusal of a record's rows

`tests/test_a_record_says_what_ran_it.py:439`. The same sentence names the
floor and the reopening as the run document's, so it contradicts itself. The
line is also over 100 columns.

### ⬜ 10 — `skills/evidence-check/SKILL.md` says a branch *falsifies what a row cites*

`skills/evidence-check/SKILL.md:316`. A row cites code and claims a
behaviour, and the old sentence said *what … row claims*. As written, the
merged list runs the code act and the claim together.

### ⬜ 11 — three ledger claims still name `docs/review-chain-spec.md` for a section that moved (a correction)

`seal/ledger.md:1086` (R8, §*The fix surface*), `:1256` (R2, §*The fix
surface*) and `:2682` (A6, §*A verdict row that commissions nothing*). Each
row carries this branch's *Re-read … #526's split* note, and R8's and A6's
say *the claim unchanged*. But each Claim cell's first words name a file that
no longer holds the section, which is the failure `plan.md` §*Failure
scenario* predicts for the citations left behind. It is located in a record,
so it is a correction and not counted by `Needs a fix`. The replacement is
`docs/round-record-spec.md` in each of the three Claim cells, with a
`Corrected <date>` note.

### ⬜ 12 — the records still describe the `CLAUDE.md` paste as pending (a correction)

`seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/survivors.md:16`
exempts a `CLAUDE.md` quote that `233d1a13` removed. The sweep no longer uses
the row: with the exemptions it reports one exempt place,
`correction_check.py`. `overview.md:12`, `:45` and `:49` still say the paste
is unverified or not done. The three records should say the paste landed at
`233d1a13`, and the dead exemption row should go.

### ⬜ 13 — the three doubled-notes ledger rows have no answerer (a correction)

`seal/ledger.md`, rows G5 and S4 of #386's section and *The eleven modules
that pin the path* (`phases/phase-8.md`). Escaping the second
date-and-notes pair was right for #562. Which pair is the row's is left
open, and `overview.md` §*Not done* names nobody for it. The Deferred row
below names the party.

## Findings — from execution

### ⬜ 14 — the chain checker reads the plan's approval line as absent (a correction)

`seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/plan.md:7`.
I ran `round_record.py new` over this report in the clone to check that the
generator accepts it. It exited 0, and I deleted the generated record. Its
`chain_check` pass printed *plan.md's approval line is absent* and quoted the
shape it wants: ``Approved <date> by <who>, when `smith` was spawned.`` The
line exists, but a clause follows *spawned* after a semicolon (*; phases 3
and 6 wait for step D …*). The checker reports this and does not refuse it.
It is still a durable trace that nothing reads. The fix is to end the line
at *spawned.* and put the clause in a sentence of its own.

Every other run below matched the claim it was run against.

## Regression tests to plant

- `tests/test_a_merge_cannot_silently_drop_a_correction.py`: after the fix
  for findings 1 and 2, a needle for *to neither side where both did* in
  `CONFLICT_SENTENCES`. It is red with the clause deleted from either guide,
  and `OWNED_SENTENCES` should take it too.

## Facts for the evidence ledger

- The split's section map as measured: 29 markers at 9 / 4 / 16, 879 / 523 /
  885 lines at `ca9314de`, and every old heading found once at its planned
  level. This is already this item's S1/S2 rows, so nothing new is needed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the halves rule says the hash belongs to exactly one side; where both sides edited the unit it is neither's, and the re-read reads one edit | `docs/the-evidence-ledger.md:98` | open | `75b226a7` re-read nine anchors both sides edited after `4a077852`; F1 `9ceb2e34` → `c6fe69c1` |
| 🟡 2 | the guides carry the same *exactly one side* | `CONTRIBUTING.md:255`, `CLAUDE.md:168` | open | same sentence as 🟡 1 in each; `CLAUDE.md` is the orchestrator's edit |
| 🟡 3 | the edit arm names re-stamp as the one outcome of an edit, so a falsifying edit is re-stamped; `CONTRIBUTING.md` keys the choice to the claim | `docs/the-evidence-ledger.md:47` | open | phase 6 corrected G6, G7, G1, A5 in place, a third outcome the owner omits; `spec.md` §*Out* relies on the sentence covering it |
| 🟡 4 | `CLAUDE.md`'s edit arm has the same single outcome | `CLAUDE.md:138` | open | copy of 🟡 3's sentence |
| ⬜ 5 | *Nothing downstream can see that* now follows the paragraph saying the checker sees it | `docs/the-evidence-ledger.md:107` | open | the halves paragraph was inserted before the paragraph that pointed at the #424 one |
| ⬜ 6 | *this document's `blocks more` default* moved into a document with none | `docs/round-record-spec.md:529` | open | the only `blocks more` is at `docs/review-chain-spec.md:447` |
| ⬜ 7 | the pointer sends every row's refusal to the record document | `docs/commit-review-gate-spec.md:340` | open | floor, `Needs a fix`, reopening, `Written late` are the run document's |
| ⬜ 8 | the #316 paragraph describes SpecSeal's `bin/test` in a shipped skill as the reader's | `skills/verify/SKILL.md:80` | open | the class #474 item 2 corrected at `:367` and `:372` |
| ⬜ 9 | a docstring says the record document owns every row refusal and names the floor as the run document's | `tests/test_a_record_says_what_ran_it.py:439` | open | self-contradictory; over 100 columns |
| ⬜ 10 | *falsifies what an existing ledger row cites* | `skills/evidence-check/SKILL.md:316` | open | a row claims; it cites code |
| ⬜ 11 | three ledger claims name the run document for a section now in the record document | `seal/ledger.md:1086` | open | also `:1256`, `:2682`; a record, so a correction |
| ⬜ 12 | the `CLAUDE.md` exemption and the overview's pending-paste rows outlived `233d1a13` | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/survivors.md:16` | open | also `overview.md:12`, `:45`, `:49`; a record, so a correction |
| ⬜ 13 | the three doubled-notes rows' reading has no answerer | `seal/ledger.md` | open | `overview.md` §*Not done* names nobody; a record |
| ⬜ 14 | the plan's approval line carries a trailing clause, and `chain_check` reports it absent | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/plan.md:7` | open | executed: printed by the generator's check pass; reported, not refused; a record |
| 🟢 | the move adds no rewording beyond the recorded list | `docs/review-chain-spec.md`, `docs/commit-review-gate-spec.md`, `docs/round-record-spec.md` | confirmed | section diff against the base, executed |
| 🟢 | fold markers carried whole | the three documents | confirmed | multiset identical, 9 / 4 / 16, executed |
| 🟢 | absence checks read all three documents | `tests/conftest.py` | confirmed | two planted sentences turned two cases red, executed |
| 🟢 | #561's count is equal across the split and the fold in zsh | `docs/release-checklist.md` | confirmed | 1061 three times, strict 0 three times, executed |
| 🟢 | #562 changes escapes only | `seal/ledger.md` | confirmed | byte-identical modulo `\|`, executed |

## Executed probes

| What was run | Result |
|---|---|
| section diff of the base's run document against the three new documents, by heading, fences skipped | every old heading once, planned levels, body changes only the recorded rewordings, the 35-line tail and two re-wraps |
| citation resolver: every `§` citation naming one of the three documents in tracked `.md` and `.py`, against that file's headings | no miss in a shipped file; three ledger Claim cells name the old file (⬜ 11) |
| positional-reference read (`above`, `below`, `this document`) across the three documents | one dangling (⬜ 6) |
| live fold-marker multiset, base against the three files | identical, 29; 9 / 4 / 16 |
| `bin/test` over the 27 changed test modules | exit 0, `1331 passed, 1 skipped` |
| planted a forbidden sentence in each sibling document, ran the two absence cases, restored | both red, tree clean after |
| the checklist's step 2 and §3 readings in zsh on a scratch clone, gather then `--split` then `--version 1.2.3` | 1061 / 1061 / 1061, strict exit 0 / 0 / 0; old form `no matches found`, `0` |
| `git grep` table-line count at `eaba2dd1` and the target | 1047 and 1061 |
| `28439296`'s two ledger files against their parents with every escaped pipe read as a bare one | identical |
| `bin/survivor-check --range origin/<base>...HEAD`, with and without `--exempt survivors.md` | with: exit 0, one exempt used; without: exit 1, one place |
| `correction_check.py --range origin/<base>...HEAD` | exit 0 |
| `claude_block.py --check`; `uvx ruff check` and `format --check` over the edited `.py`; `rider_check.py` | exit 0 each |
| `evidence_check.py --strict .` in the clone, with this report copied in | exit 0 |
| `bin/test tests/test_no_real_identifiers.py` with this report staged intent-to-add in the clone | `5 passed` |
| `round_record.py new` over this report in the clone, record deleted after | exit 0; the tables parse; `Needs a fix` and the floor row copied; ⬜ 14 printed |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; not run by this round, which leaves it to the sealer |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| which date-and-notes pair is the row's, in the three doubled rows (⬜ 13) | not placed; a comment on #562 is the candidate | the orchestrator, who decides whether it goes to #562 or a new issue |

## Paste-ready fixes

### 🟡 1 and ⬜ 5 — `docs/the-evidence-ledger.md`

Delete the paragraph at `:98`–`:105` where it stands. Insert this after the
paragraph beginning *It reads the shared file, every release file and every
fragment* (`:121`):

```
**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read <date>` and `Corrected <date>` notes are both sides', because each
records a reading somebody performed. The anchor's hash is not a union: it
belongs to the side that edited the anchored unit, and to neither side where
both did, because the merged unit is then content neither side hashed. A
resolution that keeps a hash the merge made stale names content that no
longer exists anywhere, and the marker check above cannot see it, because no
marker was dropped. So run `evidence-check` after the resolution: a drifted
anchor is the tool naming the row, and the row is re-read against every edit
the merged unit carries, one side's or both, before it is re-stamped.
```

### 🟡 2 — `CONTRIBUTING.md:255` (indent two spaces) and `CLAUDE.md:168`

```
**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read` and `Corrected` notes are both sides', because each records a
reading somebody performed; the anchor's hash belongs to the side that edited
the anchored unit, and to neither side where both did. `correction-check`
cannot see a union that kept a stale hash, because no marker was dropped, so
run `evidence-check` after the resolution: a drifted anchor is the tool naming
the row, which is re-read against every edit the merged unit carries.
`docs/the-evidence-ledger.md` §*A correction a merge dropped* owns the rule.
```

The changelog fragment's #509 entry takes the same clause: *belongs to the
side that edited the anchored unit, and to neither where both did*.

### 🟡 3 — `docs/the-evidence-ledger.md:47`

```
**Appended is the word, and a removal is not one — nor is an edit.** A
branch that removes or edits code an existing shared-file row cites must touch
the file the row is in to leave the ledger true. A removal takes the row out
there, and the new claim goes in the branch's own fragment. An edit drifts the
row, and the branch re-reads it against that edit: a claim that still holds is
re-stamped there with a dated note, and one the edit made false is corrected
there first, with a `Corrected <date>` note. Both are keeping an existing
claim true, which is not appending; adding a claim is what belongs in the
fragment, and always did.
```

### 🟡 4 — `CLAUDE.md:138`, the second and third sentences

From *the ledger true.* to *which is not appending.*, replacing those lines;
the sentence naming `CONTRIBUTING.md` that follows stays as it is.

```
the ledger true. A removal takes the row out there and writes the new claim
into the branch's own fragment; an edit drifts the row, which is re-read
against that edit and re-stamped there with a dated note, its claim first
corrected in place with a `Corrected <date>` note where the edit made it
false. Both are keeping an existing claim true, which is not appending.
```

Needs a fix: yes — 🟡 1 and 🟡 2 (the halves rule's *exactly one side*, owner and guides), 🟡 3 and 🟡 4 (the edit arm's single outcome, owner and `CLAUDE.md`)
Loses a record or crashes: no

## Proof block

Files opened: `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/{spec,plan,overview,survivors,changelog}.md`,
`phases/phase-1.md`, `phases/phase-2.md` (§*What this phase found*),
`phases/phase-8.md`; the base's `docs/review-chain-spec.md`;
`docs/review-chain-spec.md`, `docs/commit-review-gate-spec.md` and
`docs/round-record-spec.md` by their changed and positional lines;
`docs/the-evidence-ledger.md` (`:40`–`:125`, `:140`–`:170`);
`CONTRIBUTING.md` (`:196`–`:270`); `CLAUDE.md` (diff);
`docs/release-checklist.md` (`:15`–`:110` and the §3 diff);
`skills/verify/SKILL.md` (`:55`–`:90` and the diff);
`skills/evidence-check/SKILL.md` (diff); `agents/smith.md`, `agents/sealer.md`
and `agents/warden.md` (diffs); `skills/code-review/scripts/round_record.py`
(`kept_broad_gate`, `same_run`, the two comments);
`skills/verify/scripts/arm_check.py` (`run_arms` docstring); `bin/test`;
`.github/scripts/run_tests.py` (its subprocess lines);
`skills/verify/scripts/broad_gate.py` (`:820`–`:826`); the diffs of
`tests/conftest.py` and the 27 changed test modules' re-points I name above;
`seal/ledger.md` rows at `:1086`, `:1256`, `:2069`, `:2304`, `:2585`,
`:2682` and the diff of `75b226a7`; `README.md` (`:172`–`:180`);
`README.ko.md` (`:170`–`:178`); the diffs of the hooks, `chain_check.py`,
`templates/sdd-round.md`, `docs/review-handoff-protocol.md` and
`docs/worktree-guard-spec.md`.
