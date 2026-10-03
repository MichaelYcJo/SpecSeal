# Implementation Plan: a signatory records a pact change, and the pact is reviewed

<!-- seal/specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed/plan.md
— HOW, in phases. This is the Design Gate's artifact: approval of this plan is
the gate. -->

Approved 2026-10-03 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

Five phases. The first two close what #735's round 3 deferred, and they come
first because steps C and D read through them. Phase 1 builds the one table
walker both new records use. Phase 2 owns the printed-path class that every new
line joins. Phase 3 is the writer, `--reverify` recording a pact change. Phase 4
is the reader and the pact review, in `pact-check`. Phase 5 carries the
cross-cutting words. Each phase documents and pins what it changes in its own
commit (contract §14), so phase 5 holds only what spans phases.

## Technical context

- **The walker.** `hooks/config.py#pact_signatories` walks one table with its
  own break list, `TABLE_BREAK`. Round 3 found three of that list's arms · NAME NOT IN TREE
  survive deletion and one is wrong (🟡 18). The repair is not another arm. It
  is one walker that takes a header tuple and is held to cmark-gfm by a
  property case over an enumerated corpus. `pact_signatories` keeps its
  signature and its entry refusals (`remote_entries`) and calls the walker.
  Both callers, `pact_check.py` and `chain_check.py#pact_notices`, are
  unchanged.
- **The oracle.** `cmarkgfm`, pinned in `.github/scripts/run_tests.py` beside
  `MARKDOWN_IT` and carried in `PACKAGES`, `.github/workflows/test.yml` and
  `CONTRIBUTING.md`'s fallback. The case that holds `MARKDOWN_IT`'s string
  across those places is found and extended, so the new string is held the same
  way. The module is `tests/`-only and imports only `cmarkgfm` and the standard
  library. It renders HTML and reads the table's cells with `html.parser`.
  `tests/test_the_hooks_hide_what_a_renderer_hides.py` holds
  `commonmark_oracle.py`'s imports, and the new module is held by the same kind
  of check. `markdown-it-py` stays: it answers a different question, which lines
  a renderer hides, and its table rule is a reimplementation, which is why it is
  not the arbiter here.
- **The corpus**, enumerated by construction:
  - the line kinds are every block start CommonMark §4–§5 and the GFM table
    extension name. That is ATX and setext headings, thematic breaks of each
    character, block quotes, both fences, the seven HTML block starts, bullet
    and ordered list items, indented code, a blank line, and a link reference
    definition. Added to those are the inline shapes a line can open with:
    an autolink, an scp-style autolink, and `<` with a space;
  - each kind is tried after the header, after the delimiter, between rows and
    after the last row;
  - each is tried with 0–3 spaces and with a tab where the kind permits.

  The phase records how the list was derived (spec section by section) and
  names any kind it left out with the reason. Round 3's 21 shapes must fall
  inside the corpus, and the phase checks that they do.
- **The grammar.** Round 3's paste-ready `PACT_MENTION_RE` is the starting
  point. Its seven case ids ran red against the target in the reviewer's clone,
  and the build re-runs them red itself (§15).
- **The printed paths.** `evidence_check.py#display_name` already takes a
  `flavour` argument. The phase decides between reusing it and a helper of
  `pact_check.py`'s own, and in either case one function renders every path
  `pact-check` prints. The enumeration is every `say(` and `found(` call in
  `pact_check.py`, taken as a list from the source rather than from the note.
- **The writer.** `main`'s reverify branch has two paths: `reverify` alone,
  where no freeze or no `--into` applies, and `reverify` on the writable files
  followed by `reverify_into` on the released ones. The record is written in
  both. A row's move is known before its hash is rewritten, so the move is
  captured there. The signatory's `Pact` rows are read through
  `hooks/config.py#pact_declaration`, loaded the way `config_reader` loads
  `config_rows`. The work item comes from `--into`'s file name, else
  `hooks/routing.py#item_dir` for the branch `hooks/routing.py#current_branch` reads.
- **The reader.** `pact_check.py#check`'s per-signatory loop gains the record
  read after the anchors. The pact reviews are read once, from
  `<pact's home>/pact-reviews/*.md`. Exit classes stay in `EXIT_ONE`/`EXIT_TWO`,
  with `NOTED` in neither.

**What breaks in six months.**
- A signatory edits a hash by hand instead of running `--reverify`, and no
  record is written. It is named as a limit, and nothing can see it.
- A pact under local mode keeps its pact reviews under the git directory. One
  clone's reviews do not travel, so another clone of the pact's repository reads
  the same changes as `NOT TAKEN`. That is loud in the right direction, and it
  goes beside the existing local-mode limit.
- `cmarkgfm` changes its table rule at a new version. The pin is what stops
  that from moving the suite, as `MARKDOWN_IT`'s does.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| The record in `seal/specs/<id>/pact-changes.md` | `settle --retire` removes the directory after the signatory releases, possibly before the pact's repository runs `pact-check`. The change disappears and nothing reports it | rejected |
| One shared `seal/pact-changes.md` | every branch appends to it, which is the conflict `CLAUDE.md`'s fragment rule exists to end | rejected |
| The `Re-read ·` row is itself the record | an in-place re-stamp, the path every unreleased fragment and every repository without `Ledger frozen from` takes, writes no row. Most changes would leave nothing | rejected |
| **`seal/pact-changes/<work-item-id>.md`, permanent, one per work item** | the directories accumulate, one file per work item that touched a cited row. That is the ledger's growth rate | **chosen** |
| A separate command the session runs to record | a step somebody must remember is a step that gets skipped, and the first goal asks for the mechanical path | rejected |
| `evidence-check`'s check mode refusing a drift with no record | once re-stamped, nothing shows which record was owed. The drift itself is already loud | rejected |
| **The writer inside `--reverify`** | a hand-edited hash bypasses it | **chosen**, limit stated |
| A pact review takes a change by commit SHA | a signatory's feature branch squashes and the SHA stops resolving: the ledger's own history (`docs/the-evidence-ledger.md`) | rejected |
| A change is taken when its clause's hash moves | a change that keeps the clause, a refactor, can never be taken and reads `NOT TAKEN` forever | rejected |
| The signatory closes its own record | the pact side's decision recorded on the other side, by the party whose change is under review | rejected |
| **A pact review row takes a record at its content hash** | a record that grows after its review reads `NOT TAKEN` again, which is correct | **chosen** |
| A pact review owed for every clause change at the pact's repository | CI cannot see which signatories cite a clause (decision 2), so decision 4's default could not be checked. And `SUPERSEDED` already sends each citing signatory to re-read where its code is | rejected |
| A new agent for the pact review | a definition, a writes table and a spawn path, for a review the warden already performs on any work item | rejected |
| `markdown-it-py`, already pinned, as the table oracle | its table rule is a reimplementation. The defect was found with cmark-gfm, which is GitHub's renderer, where these files are read | rejected |
| Three bespoke walkers for three tables | three break lists to keep in step, the drift round 3 measured in one of them | rejected |
| Cut the deferred fixes into their own item | two items rewrite one walker in sequence, and C and D cannot be built until the other squashes | rejected; fallback in `questions.md` Q1 |

## Phases

Vertical slices. Each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The cmark-gfm oracle (pinned, test-only, held like `MARKDOWN_IT`); one header-tuple walker in `hooks/config.py`; `pact_signatories` on it; the enumerated corpus and its property case; round 3's `TABLE_ENDS` entries; the census comment (⬜ 21); `pact_signatories`' docstring table rewritten to the walker's actual rules | the property case red with `TABLE_BREAK`'s `<` arm restored and with the indentation rule removed; `bin/mutation-check` over every arm of the walker, each one red or recorded as behaviour-equivalent with grounds; the five pact modules and `tests/test_every_reader_ends_a_line_where_gfm_does.py` green · NAME NOT IN TREE | ddbd24b9 |
| 2 | 🟡 19's pattern; ⬜ 23's refusal sentence naming both remedies; the grammar statement in `docs/the-pact.md` §*The pact anchor*; one display helper for every path `pact-check` prints, the `UNREADABLE` line among them | round 3's four missing-slash ids red against `2b1dcb1f`; the `ntpath` case red with the old `{their_home}/{CONFIG_FILE}` restored; `fold-check` exit 0; `test_pact_check.py` green | 79eb2872 |
| 3 | `--reverify` records pact changes in both paths: the trigger (item 4), the work item from `--into` or the branch's declaration, the notify filter, `BROKEN`, no duplicate rows; the pact-changes reader on the walker; the docs and skill text for the writer | S7–S11 each red with the writer's call removed; `bin/mutation-check` over the notify branches and the id resolution; the evidence-check modules naming `evidence_check.py` green | 869ac116 |
| 4 | `pact-check` reads each signatory's record (`NOT TAKEN`, `NOTED`, the read filter, `REFUSED`, `UNREADABLE`); the pact-reviews reader on the walker; taking by content hash; the four review refusals; `templates/pact-review.md`; the docs and skill text for the reader and the pact review; every new sentence pinned | S12–S17 each seen red; `bin/mutation-check` over each refusal and over the hash comparison; `test_pact_check.py` green | b9623ffd |
| 5 | `skills/implement/orchestration.md` `### A pact review at the pact's repository` and its act row; `templates/config.md` §*Pact* notify meanings; both directories in every `seal/` drawing that draws `pact.md`, and the layout case extended; both READMEs' `pact-check` row; the word case sweeping the new sections, with `contract-changes` and *contract review* loose; `seal/specs/<id>/changelog.md` | the act case, the layout case and the word case, each seen red by planting; `fold-check` exit 0; `bin/evidence-check --strict .` exit 0; `bin/survivor-check --range origin/release/v0.18.0...HEAD` over the whole branch | |

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
`seal/specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

**Re-read the Status column after any rebase.** A rebased commit still answers
`git cat-file` in the worktree that wrote it and nowhere else.

### Rules every phase keeps, from 0.18.0's first wave

- **Enumerate against the reference, not a list.** Any unit that reads GFM is
  judged by the cmark-gfm oracle over the phase 1 corpus. The two new readers
  inherit that by calling the walker, and each gets its own corpus pass with its
  header.
- **`encoding="utf-8"` on every `open`, `read_text` and `write_text`, and a
  `subprocess` call that reads text names it.** Every printed path goes through
  phase 2's helper. Windows CI failed two of 0.18.0's first-wave items on
  exactly these two (the spawn prompt's account, not opened here).
- **The ledger freeze binds this item** (`Ledger frozen from | 1790993141`).
  New rows go in `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md`.
  A drifted row in a released file is re-read with
  `bin/evidence-check --reverify --into <that fragment> --checked <date>`.
  A drifted row in another unreleased fragment, #735's P1, P8 and P9 among the
  likely ones, is re-stamped in place there and given a dated note. A released
  file is never edited. Read each drifted row before the date goes on it.
- **Before handing back, run `bin/survivor-check --range origin/release/v0.18.0...HEAD`
  over the whole branch**, not only over the last fix range.
- **No `git stash`.** The stash stack is shared across worktrees. A case is seen
  red by `bin/mutation-check`, by reverting one hunk with the `Edit` tool, or by
  running against `2b1dcb1f` in a scratch checkout removed afterwards (§7).
- **The broad gate is the sealer's.** The full suite, the repository-wide lint
  and the typecheck are labelled `unverified` in every handback. `ruff` on the
  touched files is narrow and runs.

## Operational impact

- **A new test-only dependency: `cmarkgfm`, pinned.** It is installed by
  `bin/test`'s runner and by `.github/workflows/test.yml` on all three
  platforms. A plugin user installs nothing new, because nothing under `hooks/`
  or `skills/` imports it. The pinned version and its wheels on Windows, macOS
  and Linux are `questions.md` Q12.
- **Two new permanent directories under `seal/`:** `pact-changes/` in a
  signatory, written by `--reverify`, and `pact-reviews/` at the pact's
  repository, written by a pact review's build. Neither is folded or retired.
- **`evidence-check --reverify` can now exit 1 where it exited 0.** That
  happens in a signatory whose drifted row cites a declared pact while no work
  item is named, by `--into` or by the branch's declaration. The `LEFT` line
  names both remedies.
- **`pact-check` can now exit 1 where it exited 0**, on any recorded change no
  pact review has taken. Every existing signatory starts with no record, so
  nothing reads differently on the day this ships.
- No migration, no environment variable, no change to `docs/commit-review-gate-spec.md`.
