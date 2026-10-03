# Round 1 report — the commit gate's policy is cut into files by question (#727)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | e2f5270f |
| Base | 2b1dcb1f (`origin/release/v0.18.0`) |
| Diff | `2b1dcb1f..e2f5270f` |
| Ran by | specseal:warden on claude-opus-5-5 |

Spec compliance first (`spec.md` D1–D11, K1–K7, S1–S10), then quality. Every
probe ran in a `git clone --no-local` of the worktree at the target, under the
round's scratch directory, and nothing was written in the worktree but this
file. This is the first round, so nothing was carried from an earlier one.

## What the account claimed, and what the code showed

- **The move is byte for byte except at base 91, 152, 199, 273, 274, 283 and
  284, plus the three preambles** (`phases/phase-1.md`, ledger row C1). A
  `difflib` probe over each moved span against
  `git show 2b1dcb1f:docs/commit-review-gate-spec.md` found exactly those, and
  one more: base line 153, which 152's edit re-wrapped with no word changed
  (`docs/the-commit-gate-inside-git.md:127-130`). The trailing blank line of
  each moved block was dropped, as phase 1 says. Nothing else differs. The
  claim is right in substance and short by one re-wrapped line; finding 2.
- **Each changed line is a locator citing file and section** (the spawn
  prompt; C1 says *now cite a file and section*). Three of seven do: base 152
  (`docs/the-commit-gate-inside-git.md:128`, §*commit-review-gate
  (PreToolUse, Bash)*) and base 283–284 (`docs/commit-review-gate-spec.md:56-57`,
  §*The commit gate inside git*). Base 91 names the arms file alone, which is
  right, because it means the whole file. Base 199, 273 and 274
  (`docs/the-commit-gate-inside-git.md:176`, `:251`, `:252`) say *the
  PreToolUse reading in `docs/commit-review-gate-spec.md`* with no section,
  which is not D5's shape and is recorded nowhere as a divergence. Each still
  sends a reader to the right file. Findings 2 and 3.
- **No other positional line crosses** (W1). Re-derived without K6's `awk`:
  every line of the base holding *above*, *below*, *next*, *previous*,
  *following*, *the table*, *the paragraph*, *this section*, *this document*
  and kin, labelled by the part it moved to. Only 152, 283 and the K6 lines
  cross. Arms line 182, *This is a reversal, and of this document*, is still
  true: the paragraph it means is in the arms file beside it. A second probe
  looked for an italic reference in one part to a heading or bold statement
  that sits in another, and found none.
- **Every `§*…*` citation resolves** (S5). My resolver walked every live
  tracked file (excluding `seal/specs/`, `seal/releases/`, `seal/ledger*` and
  `CHANGELOG.md`), collapsed the whitespace, and took every `§*X*` or
  `under *X*` whose text begins a heading of one of the three files. It found
  21. Seventeen name the file that holds the heading, and the other four are
  `docs/worktree-guard-spec.md` §*Known limits*, which is that document's own
  heading and not a hit. A `git grep` of every moved heading's words outside
  the three files found no bare reference left on the parent's path. The
  hooks, skills and agents that name a moved heading
  (`hooks/commit-review-gate.py:634`, `:649`, `hooks/gate.py:60`,
  `skills/agent-contract/SKILL.md:251`, `:356`) now name the file holding it.
- **Bare references whose subject stayed were left** (D6). I opened each one:
  `hooks/cmdline.py:2234`, `:2384`, `hooks/cmdline_base.py:1692`, `:1772` and
  `hooks/commit-review-gate.py:454` (an unresolvable `-C`, parent :82 and
  :278); `tests/test_chain_hooks_hardening.py:377` (*no longer declared
  independently*, parent :64); `tests/test_gate_judges_the_repo_it_commits_to.py:1213`
  (the subshell, parent :275). Each subject is in the parent.
- **The re-pointed bare references name the right holder.** `hooks/mode-gate.py:63`
  and `hooks/routing.py:27` (the standing waiver, arms :182–192),
  `hooks/gate.py:14` (the two arms), `hooks/commit-review-gate.py:1333` (the
  known limit, inside git's second *Known limits* bullet) and
  `skills/code-review/scripts/chain_check.py#restored_from` (enforcement at
  the pull request, the arms' declaration section).
- **Fold markers and `Enforced by:` lines** (K1, S4). `bin/fold-check --root .`
  exits 0 over 157 statements in 18 documents, every one at or under 1,000
  lines and none listed. 6, 8 and 4 markers per file, as the spec said.
- **`Over the ceiling` reads `none` and the ceiling check still runs**. Read:
  `skills/settle/scripts/fold_check.py#parse_over` returns an empty listing
  for `none`, and the per-document line check in
  `skills/settle/scripts/fold_check.py#ceiling_problems` runs for every
  unlisted document. Executed: with 1,200 filler lines appended to
  `docs/the-review-and-parity-arms.md` in the clone, `fold-check` exited 1
  and named that document over the ceiling of 1000; the file was restored by
  `git checkout`. The prose pin
  (`tests/test_a_document_has_room_for_the_next_fold.py#prose_disagreements`)
  compares listed entries only, so *No document is listed over the ceiling
  now* is held by its regex finding none; that is #526's design, not this
  branch's.
- **`REVIEW_CHAIN_DOCS` and its consumers** (S7). The tuple names five
  documents. Every consumer either reads absence through
  `review_chain_text`, which widens, or slices a document for presence. Each
  presence slice that moved (`### Review arm` … `####`, `#### The
  declaration` … `### Parity arm`, the two-answers sentence, *no standing
  waiver* and *per command*, *resolves to \*no declaration\**, the four git
  versions) now reads the file holding it, and the three tests still reading
  the parent read text that stayed there (`## Registration`, the two prompts,
  `.specseal/handoff`).
- **The ledger** (K3, S8). Read against both released rows: the G17
  `Corrected ·` row carries all five coordinates, four at the released hashes
  and §*Known limits* at `docs/the-commit-gate-inside-git.md`, new hash
  `da878498`; its claim cell is the released claim word for word. The
  *two opt-in headings* `Corrected ·` row carries both coordinates at the
  released hashes `3f374912` and `4b9d8901`, re-pointed to the arms file. No
  other fragment row cites either released row. The 13 `Re-read ·` rows each
  sit on a unit this branch drifted, and each edit is what the row says: a
  comment in `hooks/commit-review-gate.py#main` (E1, E2, E6, E17, E18, G8), a
  docstring (R1, A2), the tuple (S3), §17's citation (E8), `COVERED`'s two
  entries (0.12.0, 0.9.3), and for E9 the arms leaving the unit. I opened E9's
  released claim: the automation row (parent :85), the reversal under *Why a
  deny* (parent :471–477) and #662/#665 (parent :512–514) all stayed, so
  `Re-read ·` and not `Corrected ·` is right. P11 in work item 1790993137's
  fragment is re-stamped in place, hash and dated note. S2's minor anchor
  does not drift because D4 kept the paragraph's first line; I read the
  claim and it holds, as the overview's divergence row says. No released
  ledger file changed.
- **The 9 DRIFTED rows** are the ones the spawn prompt named. With
  `origin/chore/0-18-0-the-four-items-read-each-other-after-the-squash`
  (5463fd82) merged into the clone, `evidence-check --strict` exits 0, with
  0 drifted and 0 refused. The four NOT-IN-TREE refusals the tip also shows,
  all in work item 1790993137's records, are gone after that merge too.
- **D9, the record layout** (S9). F1 is marked built by #727, the section's
  opening says F1 is built and three are not, the over-target list lost the
  gate's bullet and says two kinds, the `docs/` table narrows the parent and
  adds the two files, and *each is under 500 lines* became 586, 254 and 250,
  which match `wc -l` at the target. One sentence beside those counts still
  says the `Over the ceiling` row *goes away*; finding 1.

## Findings from reading

### 🟡 1 — The record layout says the ceiling row goes away, beside the line that marks F1 built

`docs/the-record-layout.md:177-178`: *Built, the parent is 586 lines, … Fold
markers go across whole, and the `Over the ceiling` row goes away in the same
change.*

The branch rewrapped this sentence and left it standing next to *Built*, so
it now reads as what happened. It did not happen: `seal/config.md` keeps the
row and it reads `none`, which is D8's decision and the one
`docs/the-evidence-ledger.md:305-309` states (*its entry went with the cut*).
The difference matters, because an absent row is *not declared* and turns that
half of `fold-check` off with one printed line, while `none` keeps it running
(D8's grounds, `templates/config.md` §*The fold's values*). This document is
the policy the next split reads. A session building the next cut from it is
told to remove the row, and the check stops holding every document to the
ceiling without anything going red.

The fix states what was built. It edits a unit this item's C5 row anchors
(`docs/the-record-layout.md` §*What is decided and not built yet*, as it stood at `e2f5270f`),
so C5 is re-stamped in place in the same commit. The removed sentence also
stands in work item 1790993138's `spec.md:116`, which records the decision as
it was made, so survivor-check will name it; exempt it in `survivors.md`.

## Findings that are corrections to the records

### ⬜ 2 — Ledger row C1 says seven lines changed and each now cites a file and section

`seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md`,
row C1: *The moved text is the base's, byte for byte, but for the seven lines
that pointed across the cut by position and now cite a file and section*, and
its verification cell lists the differing base lines as 91, 152, 199, 273,
274, 283 and 284.

Two parts of that are not what the tree holds. Base line 153 differs too,
re-wrapped beside 152 with the same words. And four of the seven name a file
with no section (91, 199, 273, 274). The ledger is where a reader goes to
learn what is true, and this row will fold into a released file that is never
edited again, so a correction is cheaper now. `phases/phase-1.md` §*What this
phase found* carries the same list. Located in a record, so it is a
correction, not a round (`docs/review-chain-spec.md` §*The last round
verifies*).

### ⬜ 3 — Three re-pointed locators cite the parent without a section, and no divergence row says so

`docs/the-commit-gate-inside-git.md:176`, `:251` and `:252` (base 199, 273
and 274) read *the PreToolUse reading in `docs/commit-review-gate-spec.md`*.
D5 decides *a citation by file and section, in the shape
`` `docs/commit-review-gate-spec.md` §*commit-review-gate (PreToolUse, Bash)* ``*,
and line 128 of the same file follows it. A reader still lands in the right
file, and the parent is mostly that section, so the release ships nothing
false. What is missing is the record: `overview.md` §*Where spec and
implementation diverged* has four rows and none for this. Either add the
section to the three lines or record the choice. Line 176 sits inside
§*Known limits of the commit gate inside git*, so adding the section there
moves G17's re-pointed hash off `da878498` and the `Corrected ·` row must be
re-stamped. The paste below records the divergence instead, which touches no
anchor.

## Findings from execution

None. Every command below exited as the account said it would, apart from
the one line finding 2 names.

## Regression tests to plant

None owed. D11 decides no new checker, and finding 1 is a sentence no case
pins. A pin of the form *the record layout does not say the row goes away*
would hold one wording and not the class.

## Facts for the evidence ledger

None new. If finding 2 is corrected, C1's claim and verification cells change
and its anchors do not.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the record layout's F1, marked built, still says the `Over the ceiling` row goes away; the row stays and reads `none` (D8), and the next split reading this policy turns half of `fold-check` off | `docs/the-record-layout.md:177` | open | read: `seal/config.md` row `Over the ceiling` is `none`; `docs/the-evidence-ledger.md:305-309` says the entry went; D8 says why an absent row is a different state |
| ⬜ 2 | ledger row C1 says seven base lines changed and each now cites a file and section; base 153 differs too (re-wrapped), and 91, 199, 273, 274 name no section | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` (C1) | open | executed: the S1 probe found base 153 changed beside 152; read: the seven lines as they stand. A record, so a correction |
| ⬜ 3 | three re-pointed locators cite the parent by path alone, not D5's file-and-section shape, and no divergence row records it | `docs/the-commit-gate-inside-git.md:176` | open | read: lines 176, 251, 252 against D5 and line 128; `overview.md` has no row for it. Behaviour and facts are right |
| 🟢 | the moved spans equal the base except the three preambles, base 91, 152–153, 199, 273, 274, 283, 284 | `docs/the-commit-gate-inside-git.md`, `docs/the-review-and-parity-arms.md`, `docs/commit-review-gate-spec.md` | confirmed | executed: `difflib` probe against `git show 2b1dcb1f:docs/commit-review-gate-spec.md` |
| 🟢 | no other positional or italic reference crosses the cut | the three files | confirmed | executed: a wider word list over the base by part, and an italic-to-heading and italic-to-bold probe across the three files |
| 🟢 | every `§*…*` citation of a heading in the three files names the file holding it, in docs, hooks, skills, READMEs and tests | live tree | confirmed | executed: resolver probe, 21 citations, 17 resolved, 4 are worktree-guard's own heading; `git grep` of the moved headings' words |
| 🟢 | the ceiling check still runs with `Over the ceiling` at `none` | `skills/settle/scripts/fold_check.py#ceiling_problems` | confirmed | executed: an arms file padded past 1,000 lines fails `fold-check` with exit 1; the real tree exits 0 |
| 🟢 | the 9 DRIFTED rows reach 0 once the integration chore is merged | `seal/ledger/`, `seal/releases/` | confirmed | executed: `evidence-check --strict` exit 2 at e2f5270f (9 drifted, 4 refused), exit 0 after merging 5463fd82 (0, 0) |
| 🟢 | G17 and the two opt-in headings carry every coordinate; the 13 `Re-read ·` rows hold against their edits; P11 is re-stamped in place; no released file changed | `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md` | confirmed | read: each row against the released row and the diff; executed: `evidence-check`, `correction-check` |
| 🟢 | the record layout marks F1 built, drops the gate from the over-target list, adds both files to its table and states 586, 254, 250 | `docs/the-record-layout.md` | confirmed | read against `wc -l` at the target; the one stale sentence is finding 1 |

## Executed probes

| What was run | Result |
|---|---|
| S1 probe (a scratch file, run once, deleted): `difflib` of each moved span and the parent against the base | only the three preambles and base 91, 152, 153, 199, 273, 274, 283, 284 differ; 153 is a re-wrap |
| base lines by part, grepped for a wider set of positional words | crossing: 152, 283 and the K6 lines; nothing new |
| italic references across the three files, against headings and bold statement openings | none crosses |
| citation resolver over the live tree | 21 citations of a heading in the three files; 17 resolve to the holder; 4 are `docs/worktree-guard-spec.md` §*Known limits* |
| `bin/evidence-check --strict .` at e2f5270f | exit 2: the 9 named DRIFTED rows, 4 NOT-IN-TREE refusals in 1790993137's records, nothing BROKEN |
| the same after merging 5463fd82 into the clone | exit 0: 0 drifted, 0 refused |
| `bin/correction-check --range 2b1dcb1f...HEAD`, before and after the merge | exit 0 both; no released ledger file changed |
| `bin/fold-check --root .` | exit 0: 157 statements, 18 documents, 0 listed over the ceiling |
| `bin/fold-check --root .` with the arms file padded to 1,450 lines | exit 1, the arms file named over the ceiling of 1000; file restored |
| `bin/survivor-check --range 2b1dcb1f...HEAD` | exit 1, one place (1790815613's overview line 49); with `--exempt` this item's `survivors.md`, exit 0 |
| `python3 .github/scripts/rider_check.py --root .` | 20 ok, 0 drifted, 0 broken |
| `bin/test -q` over 14 modules: hooks hardening, the direct answer, the reopening, the waiver, release hygiene, a gate that fails, the handoff, line wrap, fold room, one word, ledger rules, changelog, no real identifiers, one owner | 462 passed, 1 skipped |
| `bin/test -q` over the other four `REVIEW_CHAIN_DOCS` consumers and the agent contract module | 306 passed |
| the broad gate: full suite, repository-wide lint, typecheck | not yet — the sealer's, once, after the rounds settle; nothing in this round ran it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

In `docs/the-record-layout.md`, replace the paragraph after F1's table:

```
Each part answers one question — what git decides, what the text reading
decides, what each arm wants. Built, the parent is 586 lines, the commit gate
inside git 254 and the arms 250, each under the ceiling of 1,000. Fold markers
went across whole, and the `Over the ceiling` entry went with the cut in the
same change. The row stays and reads `none`, so `fold-check` still holds every
document to the ceiling (`docs/the-evidence-ledger.md` §*The fold, and what
tells it from a deletion*).
```

Then re-stamp C5 in place (`bin/evidence-check --reverify --ledger
seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md
--checked <date>`), and add to `survivors.md`:

```
| `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md` | The `Over the ceiling` row goes away in the same change | work item 1790993138's frame, recording F1 as #715 decided it; #727 kept the row at `none` (D8) and corrected the present-tense statement in `docs/the-record-layout.md`, and `spec.md` §*Scope* leaves every other work item's records untouched |
```

### ⬜ 2

In row C1 of this item's ledger fragment, replace the claim's last sentence:

```
The moved text is the base's, byte for byte, but for the seven lines that pointed across the cut by position, which now name the file that holds what they pointed at (152 and 283–284 name its section too), and base line 153, re-wrapped beside 152 with no word changed
```

and in its verification cell, and in `phases/phase-1.md`'s first *Verified*
bullet, the list of differing lines:

```
the three preambles and base lines 91, 152, 153 (re-wrapped, same words), 199, 273, 274, 283 and 284
```

### ⬜ 3

Add a row to `overview.md` §*Where spec and implementation diverged*:

```
| D5's citation shape | Spec D5: "A positional reference that crosses the cut becomes a citation by file and section". Base 91, 199, 273 and 274 name the file alone; 152 and 283–284 name file and section | the file alone for those four | 91 means the whole arms file. 199, 273 and 274 say *the PreToolUse reading*, which is what the parent chiefly holds, and 199 sits inside the unit G17 anchors, so a section there would move G17's re-pointed hash again |
```

Needs a fix: yes — 🟡 1, the record layout's F1 says the `Over the ceiling`
row goes away while the row stays at `none`.
Loses a record or crashes: no

The broad gate has not come due: finding 1 is open. Once it is fixed and a
verifying round closes it, the sealer's spawn is what comes due.

## Proof block

Opened in this round, at e2f5270f unless said otherwise:

- `seal/specs/1791019477-the-commit-gate-policy-is-cut-into-files-by-question/`: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `phases/phase-1.md`, `phase-2.md`, `phase-3.md`, `survivors.md`, `changelog.md`
- `docs/commit-review-gate-spec.md` (and its base), `docs/the-commit-gate-inside-git.md`, `docs/the-review-and-parity-arms.md`, `docs/the-record-layout.md`, `docs/the-evidence-ledger.md` (the fold section, *A released row is read again in the branch's fragment*), `docs/review-chain-spec.md` (preamble, *A finding located in a record*), `docs/round-record-spec.md` (preamble)
- `seal/config.md`, `seal/ledger/1791019477-the-commit-gate-policy-is-cut-into-files-by-question.md`, the P11 row of `seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md`, rows G17 of `seal/releases/0.17.0.md`, E9 of `seal/releases/0.16.0.md`, *two opt-in headings* of `seal/releases/0.4.0.md`, *The eleven modules* of `seal/releases/0.9.3.md`, line 116 of 1790993138's `spec.md`
- `skills/settle/scripts/fold_check.py` (`ceiling_problems`, `parse_over`), `tests/test_a_document_has_room_for_the_next_fold.py` (`prose_disagreements` and its two cases), `tests/test_docs_line_wrap.py` (`COVERED`), `tests/test_chain_hooks_hardening.py:366-382`, `tests/test_gate_judges_the_repo_it_commits_to.py:1205-1218`, `tests/test_one_word_one_meaning.py:128-145`, `tests/test_handoff_outlives_the_merge.py:280-305`, `tests/test_a_gate_that_fails_says_so.py:890-915`, `skills/code-review/scripts/chain_check.py#restored_from` (base and tip)
- the whole diff `2b1dcb1f..e2f5270f` outside `seal/specs/`
