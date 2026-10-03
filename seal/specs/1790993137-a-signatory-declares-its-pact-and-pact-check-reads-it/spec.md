# Feature Specification: a signatory declares its pact, and pact-check reads it

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#647 steps A and B. Some work items commit in more than one repository, and
those repositories have to keep the same contract. This work gives each of them
a way to know that on its own: a row in its `seal/config.md`, and anchors in
its own records. It also adds one local command, run at the repository that
holds the contract, that reads every signatory and says where they disagree.

The words are the owner's (2026-10-03). Every other word in this file is chosen
to match them.

| Word | Means | Ships |
|---|---|---|
| `pact` | the one copy of what two or more repositories keep together | yes |
| `signatory` | every repository in such a work item, including the one that holds the pact | yes |
| `pact-check` | the reconciliation command, run where the pact lives | yes |
| the pact's repository | the signatory holding `seal/pact.md`. It has no noun of its own | as a phrase only |
| home, member, keeper | working words from #647's thread | **nowhere** |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | `pact-check` and the chain-check print decide nothing a person must answer. A mismatch is classified from the trees and their history, and only the second condition of decision 5 needs a person's judgment |
| #647, decision 1 (owner, 2026-09-28) | first-class. This is a structure the plugin ships, not a documented pattern |
| #647, decision 2 (owner, 2026-10-03) | no CI token. `pact-check` is local only, and a signatory's CI prints and verifies nothing about the pact |
| #647, decision 5 (owner, 2026-10-03) | *a sentence is contract when another repository's code would be wrong if it changed.* It decides whether the structure exists at all (the work item commits in more than one repository **and** they share contract) and which sentences live in the pact |
| #647, comment *The root of the design* | one work-item id, minted once, carried by every share. Placed in step A below, with the grounds |
| #647, the three naming comments, and the owner's names above | `pact` / `signatory` / `pact-check`, and the pact's repository is identified by a `Pact` row, never by a noun |
| `skills/implement/SKILL.md` §*Document layout — two roots, three lifetimes* | `seal/` directly holds the permanent machine-read files. The pact is permanent, outlives every work item, and is hashed by a machine, so it is `seal/pact.md` |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | a pact anchor is a content anchor with a hash and no commit and no line number, the same as a ledger coordinate, and the hash is computed by the same function |
| `skills/evidence-check/scripts/evidence_check.py#ANCHOR_RE` (its comment: *one grammar, so a coordinate means one thing in both arms*) | the pact anchor's pattern lives beside `ANCHOR_RE` in the same module, so every reader that blanks a coordinate can blank a pact anchor the same way |
| `skills/legacy-parity/SKILL.md` §*Migration config* (machine-local paths) | checkout paths never go in a committed file. They are kept per machine, keyed by the origin remote URL, and nothing is guessed |
| `skills/implement/scripts/seal.py#normalise_remote` | one normaliser for remote URLs already exists. `pact-check` and the config reader compare URLs through it, never through a second copy |
| `hooks/routing.py#parse` | a signatory's declaration is an ordinary `routing.md`. It needs no new row, and the commit gate already reads it |
| `skills/implement/orchestration.md` §*Orchestrator: how the work is routed — two questions, one call, one file*, and contract §17 | the routing batch is asked once. Each declaration is written in a command of its own, with the repository's path written out after `git -C` |
| `seal/config.md`, row `Over the ceiling` | `docs/commit-review-gate-spec.md` is frozen until #715. No sentence of this work goes into it. The policy goes into `docs/the-pact.md`, a document of its own |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | every remote URL in a template, a document or a test is on `example.com`, and every path is under `/Users/x/` |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. #715 may move where re-reads are written, and this work follows today's convention |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose* | a signatory can sign pacts held in more than one repository. Wherever more than one can be meant, the text says *the pact held at <repository>* |

## Scope

### In: step A, the declarations and the relationship row

1. **The routing step covers every repository the work item commits in.** The
   session that asks the routing batch writes one declaration,
   `seal/specs/<id>/routing.md`, into every gated repository the work item
   will commit in. Each one is written before that repository's first edit, in
   a command of its own, and each names that repository's own branch. The
   question is asked once and every declaration carries the same answers.
   "Gated" means the repository already has a `seal/` root at either place
   (§16). A repository with no root is not opted in by this step: creating the
   root is the bootstrap's decision and belongs to the user. The session names
   such a repository in its handback and writes nothing into it.
2. **The id is minted once and carried by every share.** This belongs in step
   A because step A is the act that names the directory in every repository.
   The id is that directory name. If A left it open, A would ship writing a
   differently named directory into each repository. Renaming one later moves
   its ledger fragment, its changelog fragment and the `<!-- specs/<id> -->`
   marker a fold writes, and every one of those is keyed by the id. So the
   session takes `date +%s` once, picks one slug, and uses the resulting
   directory name in every repository.
3. **The relationship row.** Where the work item meets both conditions of
   decision 5, the routing step also writes two rows into every signatory's
   `seal/config.md` except the pact's repository's own, when they are absent:
   - `Pact`: the origin remote URL of the pact's repository. A signatory of
     pacts held in more than one repository lists them separated by `;`, the
     separator `Over the ceiling` already uses.
   - `Pact notify`: one of `always`, `when the pact is touched` and `never`.
     It is written as `when the pact is touched`, the value #647 recommended.
     Nothing acts on it until step C, the second work item. This work reads and
     validates it and prints it, so the row has a reader from the first day.
   The pact's repository needs no row. It is identified by holding
   `seal/pact.md`.
4. **`chain_check` reads the relationship and prints.** At a pull request in a
   repository whose config carries a `Pact` row, it prints one notice per pact
   held elsewhere. The notice names the pact's repository, the notify value, how
   many pact anchors the declared work item's `spec.md` cites (step B), and that
   this CI reads no other repository, so `pact-check` at the pact's repository
   is where the reconciliation runs. In a repository that holds `seal/pact.md`,
   it prints how many signatories the pact lists. **No exit status moves on any
   of it.** A `Pact` row that will not parse, a notify value outside the
   vocabulary, and an anchor naming a pact no `Pact` row declares are all
   printed as notices. That is decision 2 as #647 states it: a signatory's CI
   prints and does not verify. The strict reading of those same rows is
   `pact-check`'s (B).

### In: step B, the pact anchors and `pact-check`

5. **The pact.** `seal/pact.md` in the pact's repository, begun from a new
   `templates/pact.md`. It opens with a `| Signatory |` table listing every
   other signatory by origin remote URL. Every `##` heading below that table is
   a clause, and a `###` under it narrows inside it. The template states
   decision 5's rule as the test for whether a sentence belongs in the file.
   The pact is written by the build at the pact's repository, framed by that
   repository's own spec, the way a policy document is edited here. Its own
   citations of its own clauses are ordinary ledger coordinates
   (`seal/pact.md#"## Clause"@hash`), which `evidence-check` already reads.
6. **The pact anchor.** In every other signatory, a clause is cited as

   ```
   pact:<name>/"<heading path>"@<hash>
   ```

   - `<name>` is the last path segment of the pact's repository's normalised
     origin URL (`seal.py#normalise_remote`). It matches `[A-Za-z0-9_.-]+`.
   - `<heading path>` is `evidence-check`'s quoted locator for a markdown unit,
     `"## A / ### B"`, with the same `\|` and `\"` escapes.
   - `<hash>` is the eight-hex `content_hash` of the clause's region, computed
     by `evidence_check.py`'s own resolver. It is the same value a local
     coordinate to that heading carries.

   **It is built so that no existing reader in a signatory takes it for a
   coordinate.** `ANCHOR_RE` needs a path that ends right before a `#`, and
   inside a pact anchor every `#` follows a `"` or another `#`. So the ledger
   arm, the records arm, `--reverify` and `--migrate` all pass it over. That is
   what leaves a signatory's own `evidence-check` exit status alone.
   `PACT_ANCHOR_RE` is defined beside `ANCHOR_RE`. Wherever a reader blanks the
   matches of `ANCHOR_RE` before it reads a line with another pattern, it
   blanks pact anchors too. Otherwise a heading such as `## v1.2:3 shape`
   inside a pact anchor would read as a pre-anchor `path:line` coordinate,
   which is `OLD-FORMAT` and exit 2.
7. **Where a signatory cites a clause.** In two places:
   - a work item's `spec.md`, in its Grounding table, recording what that work
     was built against;
   - a ledger row's `Clause` cell, beside the signatory's own code coordinate
     in `Code grounds`. This is the durable link, and it survives `settle`.
   **This is the shape step C's trigger reads.** Step C fires on a DRIFTED
   signatory ledger row that cites a pact clause. Both halves are in one row:
   the code coordinate `evidence-check` already grades, and a `PACT_ANCHOR_RE`
   match in the same row. B adds neither the trigger nor any output for it.
8. **`pact-check`**, run at the pact's repository. It is a script under
   `skills/evidence-check/scripts/`, beside `correction_check.py`, with a
   `bin/pact-check` wrapper pair.
   1. It reads `seal/pact.md` and its `Signatory` table. It derives `<name>`
      from its own origin URL.
   2. It resolves each signatory's checkout. First it reads the machine-local
      map `~/.claude/specseal/pact-paths.md`, a `| Remote | Path |` table keyed
      by remote URL and compared normalised. Then it tries each sibling
      directory of the pact's repository whose normalised origin matches.
      Nothing is guessed. A signatory neither finds is reported with the map
      line to add.
   3. In each signatory it reads the `Pact` and `Pact notify` rows strictly.
      A listed signatory whose config does not name this repository is
      reported: the relationship is recorded on one side only.
   4. It collects every pact anchor naming `<name>` from that signatory's
      ledger files (`seal/ledger.md`, `seal/ledger/*.md`, `seal/releases/*.md`)
      and from every `seal/specs/*/spec.md`.
   5. It grades each anchor against the clause in the pact's current checkout:

   | Status | When | What a person does |
   |---|---|---|
   | `OK` | the hash matches | nothing |
   | `SUPERSEDED` | it does not match, and some commit in HEAD's own history of `seal/pact.md` gave the clause this hash | **the signatory was built against a superseded clause.** Re-read it in the signatory and re-anchor |
   | `NOT TAKEN` | it does not match, and a commit reachable from another local ref, but not from HEAD, gave it this hash. The ref is named | **the pact has not taken the signatory's recorded change.** Land that ref's pact change, or reconcile |
   | `UNMATCHED` | no commit in this repository gave the clause this hash | the version was squashed away or never existed. Read both sides |
   | `BROKEN` | the heading path resolves to no clause, or to more than one | the clause was renamed or removed. Re-coordinate the signatory |

   Git is asked one thing here: which way a mismatch points. It never decides
   `OK`, which is the same bound `evidence-check` keeps by asking git for
   nothing. The second report needs the direction. Without step C's record,
   the only trace of *a signatory's recorded change* is an anchor citing a
   version of the clause that the pact's current checkout has not taken. Step C
   adds its `contract-changes` entry as a second source under the same
   `NOT TAKEN` report, and leaves the name of the report alone.
9. **Exit status.** 0: every listed signatory was read and every anchor is
   `OK`. 1: any `SUPERSEDED`, `NOT TAKEN` or `UNMATCHED`, or a signatory that
   could not be found on this machine. 2: unusable input. That covers no pact
   here, a pact or file that cannot be read, a `BROKEN` anchor, a `Pact` row or
   notify value that will not parse, a relationship recorded on one side only,
   and a pact's repository with no origin remote. These mirror
   `evidence-check`'s classes, where `BROKEN` is exit 2 and drift is exit 1.
   `pact-check` writes nothing.

### In: what carries the words

10. `docs/the-pact.md`: the policy, in the fold shape `fold-check` holds every
    statement to (`Fold shape from | 0`). It covers the model, decision 5's
    rule, the names, the anchor, and what CI does not do.
11. Shipped text: a section in `skills/evidence-check/SKILL.md`, the routing
    subsection in `skills/implement/orchestration.md` with its row in the act
    table, `templates/config.md` for the two rows and their vocabulary (and
    *What no row governs* for the anchor and the notify words),
    `skills/config/SKILL.md`'s row table, `templates/pact.md`, a `pact.md` line
    in every layout tree, and a `pact-check` row in both editions of the README
    cheat sheet.
12. A case in `tests/test_one_word_one_meaning.py` holding `pact` and
    `signatory` to one meaning each, and holding home, member and keeper out of
    the shipped pact text.

### Out, and why

| Left out | Why |
|---|---|
| Step C: the notify record (`contract-changes`) and its trigger | the second work item, stacked on this branch after this one is sealed. B's anchor is its input (item 7) |
| Step D: the contract review, and the pull-request half of the checks where a token exists | the second work item. Decision 2 also leaves the token half optional |
| One framer run writing the pact and every signatory's spec ("this repository's part") | it writes into other repositories, and `agents/framer.md`'s writes table is that agent's whole permission. Nothing in A or B needs it. Each signatory frames its own share, as today |
| Round records or seals of one signatory kept at another; the cross-repository status board and build order (#647, the fullstack comment) | the revised design keeps every signatory's records in that signatory. The board and the order belong to a later step and are not part of A or B |
| Writing a declaration into an ungated repository | it would create `seal/`, which opts the repository in. That is the bootstrap's decision and the user's (`CLAUDE.md`, the routing paragraph's first sentence) |
| The `CLAUDE.md` routing block (`templates/claude-md-block.md`) | that block is copied into a person's global file. It already sends a session to `skills/implement/orchestration.md`, which is where the multi-repository step goes |
| A check that every share carries the same id | nothing can tell an id minted twice from a signatory's own work item that cites the pact without changing it. That one is legitimate and common. The rule is stated and not enforced (item 2) |
| `pact-check` in CI, and a `--map` override flag | decision 2 for the first. The second is not needed: the map and the sibling search cover the case |
| Reusing `~/.claude/specseal/parity-paths.md` as the map | no code reads that file and nothing defines its shape. Defining a shape for it would change a file sessions write by hand. The new map has the same key and a stated shape |
| The handoff document for a long-running work item | the milestone leaves it out: it concerns work that runs long, whether or not it spans repositories |
| `docs/commit-review-gate-spec.md` | frozen over the ceiling until #715 |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | Relationship row read | Given a `config.md` with `Pact` naming one URL and no `Pact notify`, when the reader runs, then it returns that URL normalised and the notify value `when the pact is touched` | a unit case in a new test module |
| S2 | Two pacts | Given `Pact` holding two URLs separated by `;`, then both come back, in order | unit case |
| S3 | Notify outside the vocabulary | Given `Pact notify \| sometimes`, then the reader returns a refusal naming the three values, and `pact-check` exits 2 on that signatory | unit case, plus a `pact-check` case |
| S4 | The routing step across repositories | `orchestration.md` says every gated repository gets a declaration under one id minted once, each written in its own command, with ungated repositories named and left alone. The act table has a row for the new subsection | `tests/test_every_orchestrator_act_names_its_delivery.py`, plus a case pinning the id-once sentence and the gated-only sentence |
| S5 | A signatory's CI prints | Given a pull request in a repository whose config names a pact, when `chain_check` runs, then it prints the pact's repository, the notify value and the anchor count, and its exit status equals that of the same tree with no `Pact` row | `chain_check` cases in temporary repositories. The printed text is pinned (§14) |
| S6 | A signatory's CI never fails on the pact | Given an unparseable `Pact` row, or an anchor naming an undeclared pact, then `chain_check` prints a notice and the exit status does not move | `chain_check` cases |
| S7 | A pact anchor is invisible to the signatory's own check | Given a signatory ledger row with a pact anchor in `Clause` (its heading carrying `v1.2:3`) and a local coordinate in `Code grounds`, when `evidence-check` runs, then it reports the local coordinate's status alone, with no OLD-FORMAT, BROKEN or EXTERNAL for the pact anchor | an `evidence-check` case, seen red with the new blanking removed |
| S8 | SUPERSEDED | Given a pact whose clause was committed as v1 then v2, and a signatory citing v1's hash, when `pact-check` runs on v2, then `SUPERSEDED` is reported, naming the signatory file and the clause, and exit is 1 | `pact-check` case over two temporary repositories |
| S9 | NOT TAKEN | Given a local branch in the pact's repository with clause v3 not merged into HEAD, and a signatory citing v3's hash, then `NOT TAKEN` names that branch, and exit is 1 | `pact-check` case |
| S10 | UNMATCHED and BROKEN | A hash no commit gave the clause gives `UNMATCHED` (exit 1). A heading path that resolves to nothing gives `BROKEN` (exit 2) | `pact-check` cases |
| S11 | A checkout that cannot be found, and a relationship on one side only | A listed signatory missing from the map and from the siblings is reported with the line to add (exit 1). A signatory whose config does not name this repository is refused (exit 2) | `pact-check` cases, with `HOME` pointed at a temporary directory |
| S12 | Clean | Every listed signatory resolves, names this repository, and cites current hashes, so exit is 0 with a summary line | `pact-check` case |
| S13 | The words hold | `pact` and `signatory` keep one meaning each. home, member and keeper appear nowhere in `templates/pact.md`, the new `orchestration.md` subsection, the `evidence-check` section or `docs/the-pact.md` as names for this concept | a case in `tests/test_one_word_one_meaning.py`, seen red by planting "the home repository" |
| S14 | The command can be reached | `bin/pact-check` and `bin/pact-check.cmd` exist, and every shipped document that names `pact_check.py` carries the command | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` |

## Data & interfaces

**`seal/config.md` rows**, in a signatory:

```markdown
| Item | Value |
|---|---|
| Pact | git@example.com:org/orders-api.git |
| Pact notify | when the pact is touched |
```

| Row | Values | Absent |
|---|---|---|
| `Pact` | one or more remote URLs, separated by `;` | no pact is held elsewhere |
| `Pact notify` | `always` · `when the pact is touched` · `never` | `when the pact is touched` where a `Pact` row exists. Ignored where none does |

**`seal/pact.md`**, in the pact's repository:

```markdown
# Pact

| Signatory |
|---|
| git@example.com:org/orders-web.git |

## Order response shape

### Fields
...
```

**A pact anchor**, in a signatory's spec Grounding cell or a ledger `Clause` cell:

```
pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d
```

**The machine-local map**, `~/.claude/specseal/pact-paths.md`, never committed:

```markdown
| Remote | Path |
|---|---|
| git@example.com:org/orders-web.git | /Users/x/work/orders-web |
```

**`pact-check [ROOT]`**: ROOT is the pact's repository and defaults to the
current directory. It prints one line per finding as
`<STATUS> <signatory> <file> <anchor> — <what to do>`, then one summary line.
The exit codes are in item 9.

**Code it builds on**, opened for this frame:
`hooks/config.py#config_rows` (the table reader every row goes through),
`hooks/routing.py#parse`, `skills/evidence-check/scripts/evidence_check.py`
(`ANCHOR_RE`, `content_hash`, `resolve_unit`, `heading_path`,
`old_format_rows`, `malformed_rows`, `check_text`, `check_records`),
`skills/code-review/scripts/chain_check.py#main` (the notices list) and
`chain_check.py#frame`, `skills/implement/scripts/seal.py#normalise_remote`,
`bin/correction-check` (the wrapper to copy).

## Open questions → questions.md

None of the rows blocks the build. The owner's 2026-10-03 answers cover every
question only a person could answer, and the frame decided the rest with
grounds. `questions.md` lists each frame decision with its answer written in,
so a reviewer can overturn one by opening what the frame opened.

Framed 2026-10-03 by framer, before the build.
