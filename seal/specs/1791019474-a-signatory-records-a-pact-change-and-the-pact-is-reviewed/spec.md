# Feature Specification: a signatory records a pact change, and the pact is reviewed

<!-- seal/specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

#647 steps C and D, and the five findings and the separator note that #735's
capped round 3 deferred to #647. Steps A and B shipped in #735: a signatory
names the pact in its `seal/config.md`, cites clauses as pact anchors, and
`pact-check` at the pact's repository grades those anchors. This work adds the
other direction. When a signatory changes code that a clause binds, it leaves a
record. `pact-check` reads that record as a change the pact has not taken, and
a pact review at the pact's repository is how the pact takes it.

The words stay the owner's (2026-10-03): `pact`, `signatory`, `pact-check`, and
no noun for the pact's repository. The thread's working names for the two new
things, `contract-changes` and *the contract review*, become **pact change** and
**pact review** here, for the reason #735's frame turned *when the contract is
touched* into `when the pact is touched` (its `questions.md` Q4): the owner
renamed the contract `pact`.

| Word | Means | Ships |
|---|---|---|
| pact change | one row a signatory records when code that cites a clause moved | yes, in `seal/pact-changes/<work-item-id>.md` |
| pact review | the work item at the pact's repository that takes recorded pact changes | yes, its record is `seal/pact-reviews/<work-item-id>.md` |
| `contract-changes`, contract review | the thread's working names | **nowhere** |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | the trigger is mechanical and the record is written by a tool, so no step stops to ask whether a change touched the pact. The one judgment left, whether a recorded change keeps the clause, is a work item's, with the review chain's warden behind it |
| #647, the revised design (*"Touched the contract" needs no judgment*; *Notifying means leaving a record, not pushing one*) | a drifted signatory ledger row citing a clause is the trigger; the record is left in the signatory and read by `pact-check` whenever the pact's repository next runs it |
| #647, decision 2 (owner, 2026-10-03) | no CI token. Nothing on a pull request reads across repositories, so the record is graded by `pact-check` alone, locally |
| #647, decision 4, default stood unobjected (owner, 2026-10-03) | a pact review is owed only where a signatory cites a pact clause. Here it holds by construction: only a row citing a clause produces a change that is owed a review (item 9) |
| #647, decision 5 (owner, 2026-10-03) | a sentence is contract when another repository's code would be wrong if it changed. A recorded change is therefore read against the clause it cites, and nothing else |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/spec.md`, item 8 | *"Step C adds its contract-changes entry as a second source under the same `NOT TAKEN` report, and leaves the name of the report alone."* An untaken pact change is `NOT TAKEN`, exit 1 |
| same file, item 7 | the trigger's input is one ledger row carrying both a local code coordinate and a `PACT_ANCHOR_RE` match. B built exactly that shape |
| `docs/the-pact.md` §*How a signatory names the pact* | says *"Nothing acts on that value until the record of a pact change exists"*. This work is that record, so the sentence is corrected and `Pact notify` gets its meaning |
| `docs/the-pact.md` §*`pact-check` reconciles, locally* and §*What this does not see* | the existing statuses and exit classes stand; this work adds a source to `NOT TAKEN`, one status, `NOTED`, and the limits it brings |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | a pact review takes a change by the content hash of the record, never by a commit SHA, which a squash would orphan |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, and `seal/config.md` `Ledger frozen from \| 1790993141` | this work item is bound by the freeze. A released row it drifts is re-read in its own fragment; a row in an unreleased fragment, #735's included, is re-stamped in place there, because a citation into a fragment is refused |
| `skills/evidence-check/scripts/evidence_check.py#reverify` and `#reverify_into` | the re-read is the one act at which a session acknowledges that code under a row moved. The record is written inside that act, by the same command |
| `hooks/routing.py#item_dir` | names the work item a branch is declared for. It gives the record its file name where no `--into` fragment does |
| `skills/settle/SKILL.md` (`settle --retire` removes a work item's directory under `seal/specs/`) | a record whose life outlasts its work item cannot sit inside that directory. Both new files live directly under `seal/` |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | one file per work item for both records, so no two branches append to one file |
| `skills/implement/SKILL.md` §*Document layout — two roots, three lifetimes* | `seal/` directly holds permanent machine-read files. Both records are permanent and machine-read |
| `tests/commonmark_oracle.py` (#667) and `.github/scripts/run_tests.py#MARKDOWN_IT` | the precedent for a test-only pinned parser that shares nothing with the readers it judges. The cmark-gfm oracle follows it exactly |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-3-report.md` §*Findings from execution*, §*Findings from reading*, §*Paste-ready fixes* | 🟡 18, 🟡 19, ⬜ 21, ⬜ 22 and ⬜ 23, with fixes and case ids that ran green in the reviewer's clone |
| #647, the last comment (after `1a60896c`) | `pact_check.py`'s `UNREADABLE` sentence joins a native absolute path with `/` |
| `skills/agent-contract/SKILL.md` §12, §13, §14, §15 | the separator note is a class (every path `pact-check` prints); its case removes the POSIX guarantee rather than resting on it; every changed sentence is pinned in its commit; every new case is seen red |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | every URL on `example.com`, every path under `/Users/x/` |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose* | *review* is said of several parties here. The new one is always *the pact review*, never a bare *review* |
| `seal/config.md`, row `Over the ceiling` | `docs/commit-review-gate-spec.md` is frozen until #715. Nothing of this work goes there |

## Scope

### In: the deferred fixes, built first because steps C and D read through them

1. **One GFM table walker, held to cmark-gfm by construction.** `pact_signatories`'
   walk becomes one walker that reads a table with any header, and both new
   records (items 6 and 8) are read through it. It reads what cmark-gfm reads
   and refuses, with the true cause, only what it cannot read. That closes:
   - 🟡 18: an autolink row (`<https://…>`, `<git@…>`, `<` and a space) is no
     longer an HTML block that ends the table; a thematic break (`***`, `---`,
     `___`) ends it, as GFM does;
   - ⬜ 22: a header, delimiter or row indented as GFM permits is read, not
     refused for another cause;
   - ⬜ 21: the census comment in
     `tests/test_every_reader_ends_a_line_where_gfm_does.py` stops saying the
     walk is `config_rows`'.

   The oracle is `cmarkgfm`, pinned and test-only on the terms of #667: a
   `tests/` module that imports only it and the standard library, renders a
   shape, and returns the table's cells. **The shapes are enumerated from the
   CommonMark and GFM block kinds, not from examples**: every block start the
   specification lists, each at every position in a table, with 0–3 spaces of
   indentation and a tab where the kind allows it. cmark-gfm gives the answer
   for each, and the case requires the walker's cells to equal it or the walker
   to refuse. Round 3's 21 shapes are a subset of that corpus, so they are not
   listed separately.
2. **The anchor grammar, stated where a reader looks for it.**
   - 🟡 19: `PACT_MENTION_RE` also begins an attempt where the rest of an
     anchor follows with its `/` missing, as round 3's paste-ready pattern
     does. The four shapes are refused at exit 2.
   - ⬜ 23: the grammar stands: a `/` after `pact:<name>` begins an anchor.
     The refusal sentence names the second remedy, a fenced block for an
     example, beside the first.
   - The one-rule grammar becomes a statement in `docs/the-pact.md` §*The pact
     anchor*. Today it lives only in a code comment.
3. **Every path `pact-check` prints is in POSIX form**, `~/`-relative under the
   home directory and relative to its repository inside one. The separator
   note names one sentence. The class is every output line of `pact_check.py`,
   this work's new lines included: the `READ` line's checkout, the `NOT FOUND`
   and `ONE-SIDED` details, the sibling list, the map refusal, the no-repository
   and no-pact sentences, and the `UNREADABLE` sentence. One helper renders
   them all. Its case feeds it `ntpath` input, so the POSIX guarantee is
   removed rather than relied on.

### In: step C, the pact change

4. **The trigger.** A signatory ledger row carries a `PACT_ANCHOR_RE` match
   naming a pact that the signatory's own `Pact` row declares, and one of its
   code coordinates reads DRIFTED or BROKEN. That is the whole test, and it
   needs no judgment.
5. **The writer is `evidence-check --reverify`**, in both of its forms. Before
   a row's hash moves (in place, or into a `Re-read ·` row under `--into`),
   and for a BROKEN coordinate a re-read cannot clear, it appends one row per
   ledger row to `seal/pact-changes/<work-item-id>.md` and prints a `recorded`
   line naming it.
   - **The work item id** is the `--into` fragment's name where one is given,
     and otherwise the work item `hooks/routing.py#item_dir` finds declared for
     the current branch. With neither, nothing is recorded. Each such row is
     named on a `LEFT` line with the two ways to name an id, and the exit is 1.
   - **`Pact notify` decides what is recorded.** `when the pact is touched`
     records rows citing a clause of that pact. `always` also records every
     other drifted row, with `—` in its `Clause` cell. `never` records nothing.
   - **Running it twice records nothing twice.** A row identical to one already
     in the file is not appended.
   - **The ledger is written exactly as before.** The record is an addition to
     the act, not a change to what the act writes.
6. **The record.** `seal/pact-changes/<work-item-id>.md` sits directly under
   the signatory's `seal/`. It is permanent, one file per work item, never
   folded, and never edited by hand. The writer creates it with its header
   (Data & interfaces). Its rows say which clause, which ledger row, what moved
   (each coordinate from its recorded hash to its current one, or `BROKEN`) and
   when. The file's name says why: that work item's `spec.md`.

### In: step D, the pact review

7. **`pact-check` reads every signatory's pact changes**, following that
   signatory's `Pact notify` as read now:
   - a row citing a clause of this pact, which no pact review here has taken,
     is `NOT TAKEN`, exit 1. The line names the signatory, the record and line,
     the clause, the work item, and the record's current content hash, which is
     the value a pact review writes;
   - a `—` row from a signatory whose notify is `always` is `NOTED`, exit 0.
     It is printed until a pact review takes it;
   - under `when the pact is touched` a `—` row is not read, and under `never`
     no row is. The `READ` line says how many rows were read and how many taken;
   - a record that will not parse is `REFUSED`, and one that will not read is
     `UNREADABLE`, both exit 2.
8. **A pact review is a work item at the pact's repository**, routed like any
   other. Its build writes `seal/pact-reviews/<work-item-id>.md`, begun from a
   new `templates/pact-review.md`, one row per record it takes:
   - `holds`: the clause stands as written, and the signatory's change keeps it;
   - `amended`: this work item amends the clause to take the change.

   **Who runs it.** The session at the pact's repository opens it when
   `pact-check` reports a `NOT TAKEN` from a pact change. The builder judges
   each change against its clause. Its review chain's warden verifies those
   judgments by reading each change in the signatory's checkout, at the paths
   `pact-check` printed. Where the routing answer skips the review chain, the
   builder's judgment is the whole pact review, as with any other work item.
   `skills/implement/orchestration.md` gains the act as
   `### A pact review at the pact's repository`, with its row in the acts
   table.
9. **What checks it is `pact-check`.** A record is taken when a pact review row
   names its signatory and its work item **at the record's current content
   hash**. A record that gained rows after its pact review reads `NOT TAKEN`
   again, naming the hash the review took and the hash it holds now. A row
   that cannot be what it says is `REFUSED` at exit 2:
   - it names a signatory the pact does not list;
   - it names a record that signatory does not hold;
   - its verdict is outside the two;
   - it says `amended`, and a clause the taken record cites still has the hash
     the record recorded.

   Decision 4's default holds by construction. Only a row citing a clause is
   owed a pact review, and a `NOTED` row never moves the exit.
10. **A clause the pact's repository changes owes no pact review.** B's
    `SUPERSEDED` already sends every citing signatory to re-read the clause
    against its own code and re-anchor. That is checked where the code is,
    which is #647's principle, and CI could not see which signatories cite a
    clause anyway (decision 2). `docs/the-pact.md` states this rather than
    leaving it to be inferred.

### In: what carries the words

11. `docs/the-pact.md`: new statements in fold shape under this work item's
    marker. They cover the trigger and the writer, the record, how `pact-check`
    reads it, the pact review and its record, and the clause change that owes
    none. The grammar statement comes from item 2. §*How a signatory names the
    pact* gets its `Pact notify` sentence corrected, and §*What this does not
    see* gets this work's limits: a hash edited by hand bypasses the writer,
    and a vendored copy of `evidence_check.py` cannot record.
12. Shipped text:
    - `templates/config.md` §*Pact*: what each notify value now does.
    - `templates/pact-review.md`.
    - `skills/evidence-check/SKILL.md`: §*`pact-check`* and §*Re-verifying is
      recomputing the hash*.
    - The orchestration subsection and its act row.
    - Both new directories in every drawing of the `seal/` root that draws
      `pact.md`, held by the existing layout case.
    - Both READMEs' cheat-sheet `pact-check` row.
13. `tests/test_one_word_one_meaning.py`'s pact case sweeps the new sections,
    and its loose list also refuses `contract-changes` and *contract review*.

### Out, and why

| Left out | Why |
|---|---|
| Cutting this item in two | **not cut.** Five phases, against #735's six. The deferred fixes share units with C and D: both new records are read through item 1's walker, and item 3's class contains every line C and D add. Two items would rewrite one unit in sequence. The fallback cut line is in `questions.md` Q1 |
| The pull-request half of the checks where a token exists | decision 2: no token |
| A pact review owed for a clause change at the pact's repository | item 10 |
| `chain-check` printing a signatory's recorded pact changes | decision 2's posture, *a signatory's CI prints the relationship*, is met by A's notice. The person who acts on a record is at the pact's repository, where `pact-check` names it. A new printed line is a pinned sentence with no reader who acts on it |
| A new agent, or a change to `agents/warden.md` | the pact review is an ordinary work item, and its warden writes its ordinary round report. What it must read reaches it through the spawn prompt the orchestration subsection describes |
| `evidence-check`'s check mode refusing a drift that has no record | the drift is already exit 1 under `--strict`, and once re-stamped nothing shows which record was owed. The writer sits in the re-read so the record cannot be skipped by the tool's own path. A hand-edited hash is the stated limit (item 11) |
| Recording a change from a vendored `evidence_check.py` (no `hooks/` beside it) | a vendored copy runs in CI, which never re-reads. It says it did not record (`questions.md` Q15) and records nothing |
| Removing a recorded pact change | a record is permanent, like a released ledger file. A pact review takes it, and nothing deletes it |
| The handoff document for a long-running work item | the milestone leaves it out |
| `docs/commit-review-gate-spec.md` | frozen over the ceiling until #715 |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The walker agrees with cmark-gfm | Given every shape of the enumerated corpus (item 1), when the walker and the oracle read it, then their cells are equal or the walker refuses. No shape yields cells cmark-gfm does not | a property case over the corpus; seen red by restoring `TABLE_BREAK`'s `<` arm · NAME NOT IN TREE |
| S2 | 🟡 18 end to end | Given a pact whose `Signatory` table lists one URL and then `<https://example.com/org/orders-mobile>`, when `pact-check` runs, then it does not print *1 of 1 signatory read* at exit 0 | the paste-ready `TABLE_ENDS` entries and a `pact-check` case; red against `2b1dcb1f` |
| S3 | ⬜ 22 | Given a `Signatory` header, delimiter or row indented 1–3 spaces, then the walker reads it as cmark-gfm does | corpus shapes, red against the target |
| S4 | 🟡 19 | Given each of the four missing-slash shapes as a signatory's only citation, then `pact-check` exits 2 and says *does not parse* | round 3's parametrised case, four ids red against the target |
| S5 | ⬜ 23 | Given `pact:orders-api/` in a signatory's prose, then the refusal names both remedies, a quoted heading with a hash or a fenced example. `docs/the-pact.md` states the grammar | the refusal pinned; a fold statement with its `Enforced by:` |
| S6 | Paths in POSIX form | Given native paths in `ntpath` form, when the display helper renders each output kind, then no `\` survives, and a path under the home directory begins `~/` | a case through `ntpath`, seen red with the `UNREADABLE` line restored |
| S7 | A drifted row citing a clause is recorded | Given a signatory with `Pact` naming the pact, notify absent, and a fragment row with a pact anchor and a local coordinate whose code moved, when `--reverify --into seal/ledger/<id>.md --checked D` runs, then the row is re-stamped as before and `seal/pact-changes/<id>.md` gains one row naming the clause, the row, the move and D | an `evidence-check` case over a temporary repository |
| S8 | A released row drifted | The same with the row in a released file under `Ledger frozen from`. The `Re-read ·` row is written as before, and one pact change is recorded | `evidence-check` case |
| S9 | No `--into`, a declared branch | In-place `--reverify` on a branch a `routing.md` declares records into that work item's file. On an undeclared branch it records nothing, names the row on a `LEFT` line, and exits 1 | two cases |
| S10 | Notify decides | `never` records nothing; `always` also records a drifted row citing no clause, with `—`; a pact anchor naming an undeclared pact records nothing | three cases |
| S11 | BROKEN and idempotence | A BROKEN coordinate in a citing row is recorded as `BROKEN` while the row is left as today. A second run appends nothing | two cases |
| S12 | `pact-check` reads a change | Given S7's record and no pact review, then `NOT TAKEN` names the signatory, the record and line, the clause, the work item and the record's hash, and exit is 1 | `pact-check` case; the line pinned |
| S13 | `NOTED` and the notify filter at read | Under `always` a `—` row is `NOTED` at exit 0. Under `when the pact is touched` it is not read. Under `never` nothing is | three cases |
| S14 | A pact review takes it | Given a `seal/pact-reviews/<id>.md` row naming the signatory and `<id>@<current hash>` with `holds`, then the change is taken and exit is 0 | `pact-check` case |
| S15 | Taken at an old hash | The record gained a row after the review, so `NOT TAKEN` names both hashes | `pact-check` case |
| S16 | A pact review row that cannot be true | `amended` with an unmoved clause; an unlisted signatory; a record not held; a verdict outside the two. Each is `REFUSED`, exit 2 | four cases |
| S17 | A record that will not read or parse | `UNREADABLE` and `REFUSED`, exit 2, for a pact-changes file and for a pact-reviews file | cases through the walker |
| S18 | The words and the act | The fold statements pass `fold-check`; the act row is held by `tests/test_every_orchestrator_act_names_its_delivery.py`; the layout case finds both directories in every drawing of `pact.md`; the word case refuses `contract-changes` planted in a new section | the named cases, the last seen red by planting |

## Data & interfaces

**A pact change**, `seal/pact-changes/<work-item-id>.md` in a signatory, written
by `--reverify`:

```markdown
| Clause | Row | Code | Checked |
|---|---|---|---|
| pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d | seal/ledger/1791020000-a-field-is-added.md · O1 | `src/orders.py#serialize@0a1b2c3d` → `@9f8e7d6c` | 2026-10-04 |
| — | seal/ledger/1791020000-a-field-is-added.md · O2 | `src/cache.py#evict@5e6f7a8b` BROKEN | 2026-10-04 |
```

The `Clause` cell holds the anchor as the ledger row cites it, at the hash the
signatory was built against, or `—` for a row recorded under `always` that cites
no clause. `pact-check` reads `Clause` and `Checked`. `Row` and `Code` are for
whoever judges the change.

**A pact review**, `seal/pact-reviews/<work-item-id>.md` at the pact's
repository, begun from `templates/pact-review.md`:

```markdown
| Signatory | Change | Verdict |
|---|---|---|
| https://example.com/org/orders-web | 1791020000-a-field-is-added@4c5d6e7f | holds |
```

`Change` is the signatory's work-item id, `@`, and the content hash of that
record (`evidence_check.py#content_hash` over its lines), which `pact-check`
prints on the `NOT TAKEN` line. It is not `ANCHOR_RE`-shaped: it has no `#`.

**The walker**, in `hooks/config.py`: one function reading the first table whose
header row is a given tuple of cell names, returning `(rows, refusals)`.
`pact_signatories` and the two new readers (one per record, in
the same module beside it, named by the build) call it. `pact_check.py` and `evidence_check.py`
reach them the way they reach `pact_declaration` today.

**New `pact-check` output**, one line per finding, in the existing shape
`<STATUS> <signatory> <where> — <what to do>`. `NOT TAKEN` gains a second
source, `NOTED` is new and exit 0, and the summary counts pact changes read and
taken. The exact sentences are the build's, pinned in their commits.

**Code it builds on**, opened for this frame:
`hooks/config.py#pact_signatories`, `#TABLE_BREAK`, `#pact_declaration`,
`#declared_pacts`; `skills/evidence-check/scripts/pact_check.py` (`check`,
`grade`, `PACT_MENTION_RE`, `EXIT_ONE`, `EXIT_TWO`, `MAP_SHOWN`);
`skills/evidence-check/scripts/evidence_check.py` (`PACT_ANCHOR_RE`, `reverify`,
`reverify_into`, `released_drift`, `frozen_from`, `config_reader`, `main`'s
reverify branch); `hooks/routing.py#item_dir`, `#current_branch`;
`tests/commonmark_oracle.py`; `.github/scripts/run_tests.py#PACKAGES`.

## Open questions → questions.md

None blocks the build. The owner's 2026-10-03 answers cover what only a person
could answer. The frame decided the rest with grounds, and `questions.md`
lists each of those decisions with its answer written in, beside the rows a
measurement or the work settles.

Framed 2026-10-03 by framer, before the build.
