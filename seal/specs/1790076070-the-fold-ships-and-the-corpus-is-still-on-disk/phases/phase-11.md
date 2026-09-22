# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 11

| Field | Value |
|---|---|
| Phase | 11 |
| Commit | 7811c0b9 |
| Ran by | smith on claude-opus-5[1m] |

<!-- The retirement's own commit. The repairs this phase then made —
`4b81a25e` for the chain checker and `6d1bcab2` for the ledger — are named
where they are argued below. -->

## What this phase was asked

`settle --retire` in a commit of its own; `survivors.md` with the range row;
`changelog.md`; the post-fold re-run of F1–F16 and of A4–A9. The step order
is fixed: settle report → `--retire` → `git add -A` and commit
**immediately** → then the checks, every exit code read directly.

## What this phase found

### Step 1 — the retire set was compared by name, in both directions

`./bin/settle` before the retirement: **0 released and unfolded work items
in 0 segments**, 11 ungrouped, 0 skipped, with 88 listed as folded and
waiting. Compared against the plan's own sets rather than against a count:

| Question | Answer |
|---|---|
| settle's waiting list vs. the plan's 88, by name | identical, both ways |
| only settle lists | none |
| only the plan lists | none |
| the 11 kept ids, each on disk | all 11, plus this work item's own |
| any kept id in settle's waiting list | none |

Three sibling branches were adding work item directories while this ran,
which is why the comparison is by name and never "what the tool finds".

### Step 2 — the retirement, and the commit before any check

`settle --retire` exited **0**: `retired 88 work items; 0 kept`, 88 `removed`
lines. Staged and committed in the next command, `7811c0b9`, **1,345 files
changed, 169,045 deletions** — matching `plan.md`'s operational-impact
figure exactly. Nothing ran between the removal and the commit, which is
what keeps #368's defect off this branch without deciding that ticket.

### Step 3 — the checks, and two of them found something

| Check | Exit | What it said |
|---|---|---|
| `unverified-check --baseline origin/release/v0.13.1 seal/specs/` | **0** | `5 overviews · 7 open · 2 closed · 0 unreadable · 87 folded` — **every removal read as a fold, none as a deletion** (A5) |
| `survivor-check --range origin/release/v0.13.1...HEAD --exempt …` | **0** | `every survivor is excused by a row above (12100)`, and **11972** on the re-run after this phase's repairs (A6) |
| `chain_check.py --baseline origin/main` | **1** | 88 refusals — **Q2's answer, and it is red** |
| `chain_check.py --baseline origin/release/v0.13.1` | **1** | the same 88, on the base CI will actually ask about |
| `evidence_check.py --strict .` | **2** | `17 drifted · 5 broken` — **five rows `spec.md` G3 did not know about** |
| `evidence_check.py .` (CI's lenient form) | **2** | the same; the CI job exits on ≥ 2, so this was blocking |
| the six repaired floor modules | **0** | 352 passed, 1 skipped |
| the fourteen real-corpus readers | **0** | 701 passed |
| `git diff --stat origin/release/v0.13.1 -- seal/ledger.md` | — | **25 insertions, 28 deletions. A7 does not hold** |

After both repairs: `chain_check` exit 1 with **one** error, this work item's
own absent round record, which the review chain writes; `evidence_check
--strict .` exit **0**, `1444 ok · 0 drifted · 0 broken`.

### Q2 — the chain checker does not survive the removal, and why

`chain_check` failed **all 88** retired declarations with *git does not carry
this file at HEAD*. `changed_routing` takes the declarations from the pull
request's diff and excludes a **rename** — the root move renames every
declaration at once, and "a declaration the pull request only moved is not
one it made". A retirement is the other way a declaration leaves a diff, and
nothing excluded it.

The repair is at the point of refusal rather than at the enumeration, and it
reads the same signal `unverified_check.folded_items` already reads: where
`docs/` carries the work item's marker on a live line the check prints
`retired: …`; where it does not, the refusal stands. That second half is the
case the refusal was written for, and it has a case of its own — both were
run with the excusing arm deleted, and the excusing case failed while the
refusing case stayed green. Documented in
`docs/review-chain-spec.md` beside the declaration table (§14), committed at
`4b81a25e`.

**Only `unverified_check` grew a folded-versus-deleted arm when `settle`
shipped.** That is the whole of Q2's answer: two readers of one tree, one
taught the distinction and one not.

### The ledger finding, which no question anticipated

`spec.md` G3 says `seal/ledger.md` line 78 is "the one permanent row
anchored into a work item directory", and A7 and O3 are built on it. **It is
false.** That row anchors at a `rounds/` record and survived, because its
directory is kept. Five OTHER rows anchor at a retired work item's own
`spec.md`, and the retirement broke all five:

| Work item | Anchor | Other anchors |
|---|---|---|
| 1788331011 | `spec.md#"### What the session prints, and what it refuses"` | `hooks/root-migrate.py#main` |
| 1788354065 | `spec.md#"## User scenarios & acceptance *(mandatory)*"` | none |
| 1788398967 | `spec.md#"## Fail directions / ### What extractall does…"` | `skills/implement/scripts/seal.py#linked_path` |
| 1788420760 | `spec.md#"## Two rows, and why not one and not seven"` | none |
| 1788789330 | `spec.md#"## The class, enumerated by construction"` | none |

`CLAUDE.md` outranks `spec.md` and is explicit: a row whose anchor a change
removes is REMOVED, and a branch that removes what a row cites must touch
the shared file to leave the ledger true. So the three single-anchor rows are
removed, and the two multi-anchor rows lose only the dead anchor and say so
in their Notes.

**The multi-anchor case is not mine to settle and I did not settle it.** The
ledger's own §1788354065 S12 row already named it as the owner's — *"the
rule says nothing about a row with more than one anchor; whether it should
is the owner's, named in the PR body"* — and this branch is its second
instance. Removing those two rows whole would have deleted a verified,
executed code claim to repair a documentation anchor; what I did is the
narrower act, and the owner can widen it.

**A7 does not hold, and it rested on the false premise above.** The right
outcome under policy is a ledger that is true, which this is and a
byte-identical one would not have been.

### Seventeen anchors drifted, and re-verifying them was the implementer's

Every drifted anchor is a section this branch edited — marker lines and
folded paragraphs added to `docs/` sections, and the floor repairs in
`tests/`. Each claim is about what a document **states**, and nothing stated
was removed; each was read while its marker was being placed. Re-verified,
and the diff checked to be hashes only: **23 rows across 17 anchors, no
other change**. Committed at `6d1bcab2`.

### The before and after

| | at `6d410023` | after the fold |
|---|---|---|
| directories | 99 | 12 |
| files | 1,379 | 51 |
| `round-N.md` records | 263 | 7 |
| bytes | 13,265,097 | 211,770 |

The 51 is higher than `plan.md`'s projected 38 because this work item's own
directory grew from 4 files to 17 — eleven phase records, the overview, the
changelog and survivors fragments.

### A2, checked by name

12 directories on disk, identical by name to the eleven kept ids plus this
work item's own. **None of the 88 is still on disk.**

## What this phase removes

| Removed item | Where it must land |
|---|---|
| 88 work item directories, 1,345 files | `docs/`, which carries each one's standing statement under its marker. Phases 3 to 10 name which statement went where |
| three `seal/ledger.md` rows whose only anchor was a retired `spec.md` | nowhere — their claims were about the spec prose that was folded, and `CLAUDE.md` says a row whose anchor a change removes is REMOVED rather than re-pointed. The finding itself is a new row in `seal/ledger/1790076070-….md` |
| the dead `spec.md` anchor from two multi-anchor rows | the rows' own Notes cells, which name the drop, the date, this work item and the open owner question |
| `spec.md` A7's claim that `seal/ledger.md` is byte-identical | `overview.md`'s divergence table, and the pull request body |
