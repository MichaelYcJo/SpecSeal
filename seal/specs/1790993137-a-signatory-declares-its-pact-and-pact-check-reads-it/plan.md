# Implementation Plan: a signatory declares its pact, and pact-check reads it

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Step A is mostly procedure and one reader. The routing step writes an ordinary
declaration into every gated repository under one id, a signatory's
`config.md` gains `Pact` and `Pact notify`, and `chain_check` prints the
relationship without failing on it. Step B adds a grammar, a template and a
command. A pact anchor that no existing reader takes for a coordinate, a
`seal/pact.md` whose `##` headings are its clauses, and `pact-check`, which
reads every signatory from the pact's repository and classifies each mismatch
by which side moved.

## Technical context

- **The table reader.** `hooks/config.py#config_rows` reads every
  `| Item | Value |` row and keeps duplicates in order. The two new rows go
  through it. Their parsing and vocabulary live in `hooks/config.py` beside
  `hooks/config.py#reference_roots`, the nearest precedent: a row with a
  vocabulary and an absent default. `chain_check.py` and `pact_check.py` both
  import it from there, so there is one reader.
- **The routing reader needs nothing.** `hooks/routing.py#parse` already
  accepts a declaration in any opted-in repository. A signatory's declaration
  is an ordinary one, so the commit gate in that repository goes quiet the
  moment it is on disk. That is what ends the prompts #647 measured.
- **The anchor grammar.** `skills/evidence-check/scripts/evidence_check.py#ANCHOR_RE`
  needs a path made of `[A-Za-z0-9_.@/-]`, holding a `/` or a `.`, ending right
  before a `#`. In `pact:<name>/"## A / ### B"@<hash>` every `#` follows a `"`,
  a `#` or a space, so no `ANCHOR_RE` match can end before one. `OLD_COORD_RE`
  is not safe in the same way: a heading holding `v1.2:3` matches it. So every
  place that blanks `ANCHOR_RE` before reading with another pattern (start
  from `git grep -n 'ANCHOR_RE.sub'`; `old_format_rows`, `malformed_rows` and
  `migrate` are three of them) blanks `PACT_ANCHOR_RE` as well. The builder
  enumerates the class by construction (§12) and names the sites in the phase
  record.
- **The hash.** `evidence_check.py#resolve_unit` and
  `evidence_check.py#content_hash` already give a markdown heading path a
  region and an eight-hex hash. `pact_check.py` imports the module by path,
  the way `correction_check.py` loads its reader through
  `importlib.util.spec_from_file_location`, and computes nothing of its own.
- **The URL.** `skills/implement/scripts/seal.py#normalise_remote` reduces
  ssh, https and scp-style spellings to host and path. Import it. Do not copy
  it.
- **The notices.** `chain_check.py#main` builds `errors` and `notices` as
  `(rel, line, message)` and prints a notice through `reader.annotate`. The
  pact print is a notice and only a notice.
- **What breaks in six months.** Two things, both stated rather than left to
  be found.
  - A repository that squashes its pact edits loses the intermediate clause
    versions, so a signatory built against one reads `UNMATCHED` where
    `SUPERSEDED` was true. Both are exit 1 and both say to read the two sides,
    so the classification degrades without going quiet.
  - A pact under local mode has no git history at all, so every mismatch reads
    `UNMATCHED`. `pact-check` says so once in its summary when the pact sits
    under the git directory.

**Ledger rows this work will drift.** It edits units that existing rows cite:
`hooks/config.py`, `evidence_check.py`'s blanking sites,
`chain_check.py#main`, `skills/implement/orchestration.md`'s routing section,
`templates/config.md` and the layout trees. Run `evidence-check` after each
phase, read every row it names against the edit, and correct or re-stamp it in
the file the row lives in. `CLAUDE.md` §*a change writes fragments* treats
that as keeping a claim true, not as appending. New claims go in
`seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md`.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Cite a clause as an ordinary coordinate under a `--map` prefix (`orders-api/seal/pact.md#"## X"@h`) and teach `evidence_check.py#cross_repo_intent` about `Pact` | every `ANCHOR_RE` reader in the signatory reads it as local: the ledger arm, the records arm, `--reverify` and `--migrate`. Without a map it is `BROKEN` at exit 2, or `EXTERNAL` once intent is taught, and the rename scan can propose a local look-alike. That exact defect is recorded at `place` (round 4, 🔴 4) | rejected |
| **`pact:<name>/"<heading path>"@<hash>`, which `ANCHOR_RE` cannot match, with `PACT_ANCHOR_RE` beside it and blanked wherever `ANCHOR_RE` is blanked** | a heading whose own text holds a full coordinate could still be matched inside the quotes. That is pathological, and it is listed as a known limit | **chosen** |
| Name the pact in the anchor with the full remote URL | the anchor would hold `:`, `/`, `.` and `@`, which `OLD_COORD_RE` and a reader can catch on, and it would be unreadable in a table cell | rejected. The last segment of the normalised URL is the name, and two pacts sharing one is refused as ambiguous |
| Keep the pact in `docs/` | `docs/` is the project's own convention, and a repository may have none. The pact is hashed by a machine and is permanent, which is `seal/`'s definition (`skills/implement/SKILL.md` §*Document layout*) | rejected |
| `seal/pacts/<name>.md`, several pacts per repository | nothing in #647 needs a repository holding two pacts, and the anchor would need a second name segment | rejected for now. One pact per repository, and a signatory may sign several |
| Find signatories by scanning every checkout in the map for a `Pact` row naming this repository | a signatory missing from the map is skipped in silence, and the check reads clean | rejected. The pact lists its signatories, so a missing checkout is a finding |
| Decide the second report from step C's `contract-changes` record | C is the second work item. B would ship a report with nothing to read | rejected for B. B decides the direction from the pact file's history, and C adds its record as a second source of the same report |
| Treat every mismatch as one `DISAGREES` status with no direction | the milestone asks for two reports because they send a person to two different repositories | rejected |
| A new skill for `pact-check` | a new skill adds a description to every session's listing for a command typed rarely. `correction-check` set the precedent: a wrapped script under `skills/evidence-check/scripts/` with a section in that skill | rejected |
| Make `chain_check` fail on an unparseable `Pact` row in the signatory | decision 2: a signatory's CI prints and does not verify. The strict reading belongs to `pact-check`, run locally | rejected |
| Read only live work items' `spec.md` (the `unshipped` boundary) | a work item that cites the pact but has written no ledger fragment yet would never be read. That is a silent miss | rejected. Every `spec.md` is read and findings name their file. A shipped spec citing a superseded clause stays visible until `settle` retires it, and that is the louder failure |

## Phases

Vertical slices, in the order the work depends on them. Each case is shown red
before it is committed (§15), and the phase record says how.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The relationship row.** `Pact` and `Pact notify` read and validated in `hooks/config.py`. `templates/config.md` gains a section for both, and its *What no row governs* gains the three notify values. `skills/config/SKILL.md`'s row table gains both rows, and every count of that table's rows is corrected (it says *all seven*) | a new `tests/test_a_signatory_declares_its_pact.py`, covering S1–S3 at the reader level. `tests/test_the_pull_request_language_is_the_repositorys.py` (the *What no row governs* derivation) still passes | |
| 2 | **The routing step across repositories.** A `###` subsection under `skills/implement/orchestration.md` §*Orchestrator: how the work is routed* covering: the two conditions of decision 5; a declaration in every gated repository, one id minted once, each in its own command with `git -C <path>`; ungated repositories named and never written; the `Pact` rows written where both conditions hold. The act table gains its row | `tests/test_every_orchestrator_act_names_its_delivery.py`, plus S4's pinned sentences in the phase-1 module | |
| 3 | **The pact and its anchor.** `PACT_ANCHOR_RE` beside `ANCHOR_RE`, blanked at every enumerated site. `templates/pact.md`. A `pact.md` line in every layout tree: `README.md`, `README.ko.md`, `skills/implement/SKILL.md`, `templates/seal-README.md`, `seal/README.md`, `docs/one-root-by-lifetime.md` and its `.ko` edition (enumerate with `git grep -n 'parity.md'` in tree drawings). `templates/config.md` *What no row governs* gains the anchor. One sentence in `templates/sdd-spec.md`'s Grounding comment on how a pact clause is cited | S7 as an `evidence-check` case, red with the blanking removed. A case asserting `ANCHOR_RE` finds nothing in a set of pact anchors. The existing template and layout pins still pass | |
| 4 | **`chain_check` prints.** One notice per pact held elsewhere, giving the repository, the notify value and the count of anchors in the declared work item's `spec.md`, and saying it is not verified here. A notice where the repository holds `seal/pact.md`. Notices for an unparseable row and for an anchor naming an undeclared pact. No exit status moves | S5 and S6 as `chain_check` cases in temporary repositories, in the shape of `tests/test_chain_check_at_the_pull_request.py`. Each asserts the same exit status as the tree without the row, and pins the printed sentence | |
| 5 | **`pact-check`.** `skills/evidence-check/scripts/pact_check.py`, `bin/pact-check` and `bin/pact-check.cmd` (copied from `bin/correction-check`). It reads the pact and its signatories, the map and the siblings, each signatory's rows and anchors, and grades with the history classification and the exit codes in `spec.md` items 8–9. A `## pact-check` section in `skills/evidence-check/SKILL.md`, and a row in both editions of the README cheat sheet | S3 and S8–S12 in a new `tests/test_pact_check.py` over two temporary repositories (the pact with clause v1 then v2 committed and v3 on a side branch), with `HOME` pointed at a temporary directory holding the map. S14 through `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` | |
| 6 | **The words and the policy.** `docs/the-pact.md` in fold shape (marker `<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->`, a bold rule sentence, one `Enforced by:` line per statement), added to `tests/test_docs_line_wrap.py`'s list. The S13 case in `tests/test_one_word_one_meaning.py`. The changelog fragment and the ledger fragment | S13, red by planting "the home repository" in `templates/pact.md`. `fold-check` over `docs/`. `evidence-check` over the new fragment. The suite and the lint stay `unverified` until the sealer's run | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase**, or it names commits that resolve in
one clone and nowhere else.

## Operational impact

- **New config rows**: `Pact` and `Pact notify`, both optional. A repository
  without them behaves exactly as it does today.
- **New committed file**: `seal/pact.md`, only in the repository that holds a
  pact.
- **New machine-local file**: `~/.claude/specseal/pact-paths.md`, read by
  `pact-check` and never written by it.
- **New command**: `pact-check`, through `bin/`. Nothing runs it on its own,
  and no workflow changes.
- **CI**: `chain_check` prints more lines in a signatory and in the pact's
  repository. No exit status changes.
- **No migration, no dependency, no compatibility break.**
