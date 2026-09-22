# the fold ships, and the corpus is still on disk — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1790076070-…/{routing,spec,plan,questions}.md`;
            `skills/settle/SKILL.md` §§1–4 and *What a fold branch owes*;
            `CLAUDE.md` §*a change writes fragments*, §*no real identifiers*,
            §*a thing more than one party can have*, §*A row whose anchor a
            change removes is REMOVED*; `templates/config.md` (no
            `Record language` row, so these records are English)
· evidence: `seal/ledger/1790076070-….md` — four rows: the fold marker
            against the wrap limit, the retired declaration, the five broken
            ledger anchors, and the 12,100-survivor range. Plus
            `seal/ledger.md`: three rows removed, two rows' dead anchors
            dropped, 23 rows re-verified
· verified: **executed** — `settle` and `settle --retire` (0);
            `unverified-check --baseline` (0, 87 folded, 0 deletions);
            `survivor-check --range … --exempt` (0, every survivor excused);
            `evidence_check --strict .` (0, 1444 ok · 0 drifted · 0 broken);
            `chain_check --baseline` on both bases (1, one error — this
            item's own absent round record); the six repaired floor modules
            (0, 352 passed) and the fourteen real-corpus readers (0, 701
            passed); `uvx ruff check` and `ruff format --check` on every
            touched Python file (0).
            **unverified** — the broad gate, which is the sealer's

## Why this work exists

0.13.0 shipped `settle` and folded nothing, so 99 released work item
directories and 1,379 files were still on disk; this branch writes the
standing statements into `docs/`, answers every check that counted the
records, and retires the 88 directories the prose now covers.

## The policy surface changes, and that is the owner's to overturn

**Four new top-level `docs/` files become ratified norms in this branch** —
`the-evidence-ledger.md`, `the-broad-gate.md`, `measuring-a-run.md` and
`the-agent-set.md`. A `docs/` file outranks the SDD set from the moment it
lands, so a reader of this release meets four new policy documents rather
than the side effect of a cleanup.

**The plan named five, and phase 8 did not write the fifth.**
`docs/the-gates-a-session-meets.md` would have been a second document for an
area `docs/review-chain-spec.md` already covers with a section per gate,
which `plan.md` forbids without going back to it. Its four items folded onto
the sections that hold their rules instead
(`phases/phase-8.md` has the coordinates). That moves Q1's answer in the
direction the owner can most easily accept and most easily reverse: four
files rather than five, each folded item on a named section.

That shape is `questions.md` Q1, and Q1 is addressed to a person. The run is
`automation`, so it ships on its default rather than waiting: the files are
built, and the count is the owner's to overturn at the merge. Each is its
own phase and each carries its own markers, so merging two of them
afterwards is one edit and a marker move, and nothing else in the branch
depends on the count.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| the corpus measurement's moment | `spec.md` lines 15–16 say "100 directories … 1,381 files" measured "at `6d410023`" | the branch records 99 directories and 1,379 files at `6d410023`, and 100 / 1,383 in the worktree at `5cde6dc5` | `git ls-tree -r --name-only 6d410023 -- seal/specs` counts 1,379 paths under 99 directories. This work item's own directory did not exist at `6d410023`, so one sentence was measuring two moments. Nothing decided on it changes |
| F6 `assert teeth` | `spec.md` F6 "unmeasured … if no surviving record exercises it, re-point at a fixture record"; `questions.md` Q3's default "assume it does not survive and plan the fixture" | **decline** — the floor is right and the population survives | measured in phase 1: 4 of the 7 surviving records carry `#` cells `FINDING_ID_RE` refuses (`1788395377`'s rounds 1–4). Q3 named a measurement as its instrument and the measurement says the teeth are there, so no fixture is written |
| G3's file count | `spec.md` G3 and `plan.md`'s alternatives table both say keeping `1788184145-…` costs "eight files" | nine | `find` counts 9 files in that directory. The trade it describes is unchanged |
| **G3's enumeration, and A7 and O3 with it** | `spec.md` G3: `seal/ledger.md` line 78 is "the one permanent row anchored into a work item directory"; A7: the file is byte-identical; O3: removing any row is out of scope | **five more rows**, and `seal/ledger.md` is edited | Measured: after the retirement `evidence_check .` reported `5 broken`, each on a `seal/specs/<retired-id>/spec.md#…` anchor — work items 1788331011, 1788354065, 1788398967, 1788420760, 1788789330. G3 counted rows anchored at a `rounds/` record and missed the ones anchored at a `spec.md`. `CLAUDE.md` outranks `spec.md` and says a row whose anchor a change removes is REMOVED, and that a branch removing what a row cites must touch the file to leave the ledger true. CI's ledger job exits on ≥ 2, so this was blocking as well as wrong. Three single-anchor rows removed; two multi-anchor rows lose the dead anchor only. `phases/phase-11.md` has the table |
| `plan.md`'s destination map, phase 8 | **new** `docs/the-gates-a-session-meets.md` | not written; its four items folded onto existing sections | `plan.md`'s own constraint: "no new document for an area one already covers". `docs/review-chain-spec.md` carries a section per gate — `commit-review-gate`, `review-history-guard`, `implementer-mark · implementer-notice`, and the `-C`/`cd` reader. `phases/phase-8.md` has the coordinates |
| `plan.md`'s phase 5 row | the new document wrapped at 88 **and** in `test_docs_line_wrap.COVERED` | both, and the wrap check now skips a fold marker | The two cannot hold together: `FOLD_MARKER` is matched whole, so a wrapped marker is not a fold record, and one of this fold's 88 markers is 89 columns. The limit moved by one line shape rather than the marker or the document. `phases/phase-5.md` has the measurement |
| `spec.md` F6 and `questions.md` Q3 | "unmeasured … re-point at a fixture record"; the default assumed the teeth do not survive | **decline** | Measured in phase 1: four of the seven surviving records carry `#` cells `FINDING_ID_RE` refuses. Q3 named a measurement as its instrument |

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate on the folded tree — `bin/test -q`, `uvx ruff check .`, `uvx ruff format --check .` (`spec.md` A4) | the **sealer**, in its single act after the review rounds settle. This branch runs narrow checks only (agent-contract §2) |
| whether any of the 38 standing statements drops a sentence a later work item had already overturned, wrongly | the **review chain** — the argument is gone once the directory is, which is why each phase record names what it dropped rather than folded |
| whether a ledger row with more than one anchor should be REMOVED when one anchor dies, or keep the survivors | the **repository owner**. `seal/ledger.md` §1788354065's S12 row named this as theirs at 0.4.0 and this branch is its second instance. Two rows were treated the narrow way — the dead anchor dropped, the live code anchor kept — and widening it to removal is one edit |
| whether four new top-level `docs/` files is the policy surface the repository wants (`questions.md` Q1) | the **repository owner**, at the merge. Shipped on its default; each file is its own phase and each folded item sits on a named section, so merging two is one edit and a marker move |

## Not done

`spec.md`'s O1–O8 stand as written. #368's repair is not taken here: the
branch stages and commits the retirement before any check runs, so the
defect cannot bite it, and phase 11 reports what the gate said.

## Fed back into the spec

Seven corrections, recorded in the divergence table above rather than by
editing `spec.md`, and marked *inferred during implementation* — a planner
may overturn any of them.

Three are the frame's measured facts, opened in phase 1: the corpus figures'
moment, F6's answer, and G3's file count. **The fourth is the one that
matters** — G3's enumeration was one row where the tree holds six, and A7 and
O3 were built on it. The other three are decisions the build made against the
plan and recorded where they happened: the gates document not written, the
wrap limit moved rather than the marker, and F6 declined rather than
re-pointed.
