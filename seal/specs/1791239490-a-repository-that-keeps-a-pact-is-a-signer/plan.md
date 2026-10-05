# Implementation Plan: a repository that keeps a pact is a signer

<!-- seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

A rename of one vocabulary word across the live tree, with one piece of
behaviour added so that nothing written under the old word stops working: the
readers of the pact's `| Signatory |` table and of a pact review's
`| Signatory | Change | Verdict |` header read the old header too and tell
their callers, and `pact-check` prints one line naming the rename where it
read one. Everything else is text: documents, templates, skills, READMEs,
identifiers, test names and test file names. Released records keep the word.

The cost that is not text is the ledger. Four test files, one function, three
`docs/the-pact.md` headings and one `skills/evidence-check/SKILL.md` heading
are anchors of 127 released coordinates, and this repository freezes its
released ledger files, so each affected family is re-pointed by a
`Corrected ·` row in this work item's fragment rather than edited where it
stands. That is the last phase, written in one pass.

## Technical context

- **The reader.** `hooks/config.py#pact_signatories` (line 1326) reads the · NAME NOT IN TREE
  pact's table through `gfm_table(text, SIGNATORY_HEADER)` (line 1183) and
  already branches on a refusal that starts `holds no ` (line 1338), which is
  the one refusal that means *no such table* rather than *a table that will
  not read*. The compatibility reading hangs off that branch: a `Signer`
  table absent, try the old tuple; where that reads, use it and report which
  header was read. `pact_reviews` (line 1397) has the same shape over
  `PACT_REVIEW_HEADER` (line 1394). `_signatory` (line 1417) rewords a walk · NAME NOT IN TREE
  refusal for the pact's table.
- **The callers.** `skills/evidence-check/scripts/pact_check.py#main`
  (line 532 reads the table, 664–665 prints `N of M signator{y|ies} read`),
  `pact_check.py#pact_reviews` (line 683, reads each review record through
  `config.pact_reviews`), `skills/code-review/scripts/chain_check.py#pact_notices`
  (line 4084 reads the table, 4090 prints `plural(…, 'signatory',
  'signatories')`). Both commands already print `hooks/config.py`'s refusal
  sentences, so a sentence both print belongs there
  (`tests/test_one_word_one_meaning.py` line 607's comment states the rule).
- **The lines a person reads today**, pinned: `tests/test_a_signatorys_ci_prints_its_pact.py`
  line 249 (`which lists 2 signatories`), `tests/test_pact_check.py` lines
  471–635 (five `REFUSED … \`Signatory\` table …` sentences), and the
  summary's `signator{y|ies}` in the same file.
- **The sweep.** `tests/test_one_word_one_meaning.py` lines 561–691:
  `PACT_SWEPT`, `PACT_SECTIONS` (names the `skills/evidence-check/SKILL.md`
  heading at line 583, which this work renames), `PACT_LINES`,
  `PACT_PRINTED` (names `pact_signatories` at line 611 and `_signatory` at · NAME NOT IN TREE
  line 629), `PACT_LOOSE` (line 635). `SEAL_EXCLUDED` (line 245) is the
  precedent for a named span excluded from a sweep; the file's own comment
  at lines 240–244 says why a span and not a file.
- **The fold shape.** `skills/settle/scripts/fold_check.py#target_problem`
  (line 262) resolves each `Enforced by:` target to a file and a `def`;
  `tests/test_a_folded_statement_names_what_enforces_it.py`'s real-tree case
  runs it over `docs/` at cutoff `0`. So every renamed test file and function
  that a `docs/the-pact.md` line cites must be renamed on that line in the
  same commit, or the suite is red.
- **The ledger rule.** `docs/the-evidence-ledger.md` §*A released row is read
  again in the branch's fragment*: *A released row whose anchor moved is not
  cleared by a re-read, because the family is keyed on the coordinate, and a
  `Corrected ·` row re-points it. That row supersedes the whole released
  row, so it carries every coordinate the claim still rests on, the moved one
  at its new place.* `evidence-check --reverify --into <fragment> --checked
  <date>` names each BROKEN coordinate under a released root with the
  `Corrected ·` repair and exits 1; the rows are written by hand. The shape
  of such a row is at `seal/releases/0.18.2.md` line 129 and
  `seal/releases/0.18.1.md` line 177 (`Corrected · \`pact_signatories\` …`,
  itself a family this work moves again).
- **Families affected**, read by `grep` over `seal/releases/*.md` on
  2026-10-06 (the measurement in `questions.md` M1 fixes the set):
  0.18.0 `P1`–`P10` and `P11` (through its `Re-read ·` row at 0.18.1:205);
  0.18.1 `T1`, `G2`, `D2`, `W8`, `W9`, `W10`, `F1`, `F2`, `Corrected ·
  pact_signatories`; 0.18.2 `E1`, `E2`, `E4`, `Corrected · C1`, `O1`, `O2`,
  `O3`; 0.18.3 `A1`. About 28 roots; a root already superseded by a
  `Corrected ·` row (`P8` by 0.18.1:177, `C1` by 0.18.2:129) takes its new
  row against the superseding row, not against itself.
- **CI.** `.github/workflows/test.yml` line 110 runs `evidence_check.py .`
  on every pull request (BROKEN is exit 2 there as under `--strict`), and
  `hygiene.yml` line 307 runs `correction_check.py` over the range. Neither
  passes with a released file edited or an anchor left BROKEN.
- **What breaks in six months.** A second rename of a pact word would
  reach for this reader's shape and stack a third header; the sweep's
  exclusion list grows by a span each time. The cost is stated in the
  compat statement of `docs/the-pact.md`: one old header, read for pacts
  written before 0.19.0, and no migration command.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `party` for the repositories | one word names an agent (`docs/the-agent-set.md`, `skills/implement/orchestration.md`: *every party runs*) and a repository; the state `tests/test_one_word_one_meaning.py` exists to refuse | rejected by the owner (#822) |
| `member` | a #647 working word `PACT_LOOSE` already refuses | rejected by the owner (#822) |
| Refuse the old `\| Signatory \|` header | every pact written since 0.18.0 exits 2 at `pact-check` until a person edits it; a change that stops to ask where a reader could continue | rejected by the owner (#822) |
| Read the old header and say nothing | a pact keeps the old word for ever and nobody is told; the one-word rule holds in the plugin's texts and not in the pacts it reads | rejected: the owner asked for the line |
| Read the old header of the pact only, refuse it on a pact review record | `seal/pact-reviews/<id>.md` is permanent (`docs/the-pact.md` §*A pact review takes a pact change*) and 0.18.1 shipped its header as `Signatory`; refusing it reads every taken record as `NOT TAKEN` again at exit 1 in every repository that ran a pact review | rejected by the frame: the same reader, the same line |
| Keep the test file names, rename only inside them | four file renames account for about 110 of the 127 moved anchors, so this saves most of phase 3 — but the owner listed test file names, a file called `test_a_signatory_…` is live text, and the sweep would have to exempt its own tests' names | rejected: the ledger cost is mechanical and paid once |
| Edit the released rows in place, as `CLAUDE.md`'s REMOVED/re-stamped sentence and the spawn prompt read it | `seal/config.md` declares `Ledger frozen from \| 1790993141` and this id is above it; `correction-check` refuses the range; two branches re-reading one row meet on its line at the squash | rejected: `docs/the-evidence-ledger.md` §*Without the row…* says that sentence is the rule for a repository without the freeze |
| Return the rename as a refusal string from `pact_signers` | refusals are `REFUSED`, exit 2, at `pact-check`; the line would have to be fished out of the list by its text | rejected: a third return value, the header read |
| Print the rename from `pact-check` only | the pact's repository's CI (`chain-check`) is the one place a pull request already prints the pact's count, and the sentence costs one constant | chosen: both print one sentence owned by `hooks/config.py`; `chain-check`'s exit does not move |
| Exclude whole files from the new sweep | `docs/the-pact.md` and `hooks/config.py` are the two files most likely to regain the word | chosen instead: two named spans, the `SEAL_EXCLUDED` precedent |
| Write the ledger rows phase by phase | one edit per family, about 28 round trips | chosen instead: draft as the phases go, write in one pass in phase 3 (`skills/implement/SKILL.md` §2) |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The readers, the printed lines, the tests and the policy. `hooks/config.py`: `SIGNER_HEADER`, `pact_signers` reading `Signer` then the old header and returning which it read, `pact_reviews` the same, `_signer`, the old tuple and the rename sentence in one unit; `pact_check.py` printing the rename line in no exit class and `N of M signer(s) read`; `chain_check.py` counting `signers` and appending the sentence where the header was old; every comment in the four scripts. The four test files moved with `git mv`, the fifteen functions renamed, every fixture header `Signer` but the compatibility cases, new cases S1, S2, S4, S5, S6-old-header seen red first; `templates/pact.md` and `templates/pact-review.md` begin `Signer`; `docs/the-pact.md` whole — definition sentence, three headings, prose, every `Enforced by:` node id, and the new fold-shape statement under this work item's marker | `uv run pytest tests/test_pact_check.py tests/test_a_signer_declares_its_pact.py tests/test_a_signer_records_a_pact_change.py tests/test_a_signers_ci_prints_its_pact.py tests/test_a_pact_review_takes_a_pact_change.py tests/test_a_pact_anchor_is_no_coordinate_of_the_signer.py tests/test_one_table_walker_reads_what_gfm_renders.py tests/test_a_folded_statement_names_what_enforces_it.py -q` exit 0; each new case's red shown against the pre-change reader and named in `phases/phase-1.md` | d6bcdd36 |
| 2 | The word everywhere else, and the check. `templates/config.md` §*Pact*, `templates/seal-README.md` and `seal/README.md`, `skills/evidence-check/SKILL.md` (heading renamed), `skills/implement/SKILL.md`, `skills/implement/orchestration.md`, `skills/config/SKILL.md`, `README.md`, `README.ko.md`, `docs/one-root-by-lifetime.md` and `.ko.md`; `tests/test_one_word_one_meaning.py`: the pinned definition sentence, `PACT_SECTIONS`'s renamed heading, `PACT_PRINTED`'s `pact_signers` and `_signer`, `PACT_LOOSE` gaining `signator(?:y\|ies)`, fold markers blanked before the sweep, the two named exclusions, and the file-name assertion; the S11 enumeration pasted into `phases/phase-2.md` | `uv run pytest tests/test_one_word_one_meaning.py tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_a_reference_root_is_read_and_never_taken.py tests/test_docs_line_wrap.py -q` exit 0; the sweep seen red with `signatory` planted in `templates/pact.md` before `PACT_LOOSE` gains it; `git grep -i -n signator -- ':!changelog' ':!seal/releases' ':!seal/ledger.md' ':!seal/specs'` lists only the coordinates S11 names | a9bd530b |
| 3 | The ledger and the fragment. `evidence-check --reverify --into seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md --checked <date>` run once to name the BROKEN families; one `Corrected ·` row per family, carrying every coordinate the claim still rests on at its new place with `Corrected <date>`; new rows for the reader, the printed line, the check, the templates and the policy; `seal/specs/<id>/changelog.md` under `### Changed`; `overview.md` closed | `uv run python skills/evidence-check/scripts/evidence_check.py --strict .` exit 0; `git diff --stat origin/release/v0.19.0...HEAD -- seal/ledger.md seal/releases` empty; `python3 skills/evidence-check/scripts/correction_check.py --range origin/release/v0.19.0...HEAD` exit 0; exit codes read directly (§1) | |

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
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

### The fifteen test functions phase 1 renames

`test_a_pact_anchor_is_no_coordinate_of_the_signatory.py`:
`test_a_live_spec_citing_such_a_clause_leaves_the_signatorys_check_at_0`, and
the fixture `signatory()`.
`test_a_signatorys_ci_prints_its_pact.py`:
`test_a_signatory_prints_its_pact_and_its_exit_status_does_not_move`,
`test_the_pacts_repository_prints_how_many_signatories_it_lists`.
`test_a_pact_review_takes_a_pact_change.py`:
`test_a_review_of_another_signatory_takes_nothing_here`, · NAME NOT IN TREE
`test_a_review_row_naming_a_signatory_since_dropped_stays_refused`. · NAME NOT IN TREE
`test_a_signatory_declares_its_pact.py`:
`test_the_pact_lists_its_signatories_and_a_comment_is_not_the_table`,
`test_a_signatory_row_the_walk_cannot_read_is_refused`.
`test_pact_check.py`: `test_s12_a_signatory_citing_the_current_clause_is_clean`,
`test_s7_a_notify_row_below_the_signatorys_table_is_exit_2`,
`test_two_siblings_with_the_signatorys_origin_are_not_guessed_between`, · NAME NOT IN TREE
`test_a_signatory_row_the_table_walk_cannot_read_is_exit_2`,
`test_a_signatory_with_no_seal_root_is_one_sided`,
`test_a_signatory_config_that_will_not_read_is_unreadable`,
`test_a_signatory_row_below_a_blank_line_is_refused`,
`test_a_signatory_written_as_an_autolink_is_never_passed_over`; and the · NAME NOT IN TREE
constant `SIGNATORY_URL`. Each `docs/the-pact.md` `Enforced by:` line that · NAME NOT IN TREE
names one of these is renamed in the same commit.

### What the compatibility cases must keep

`tests/test_one_table_walker_reads_what_gfm_renders.py` reads `gfm_table`
through the header tuples at its lines 48–50 and builds `| Signatory |`
fixtures throughout. Its fixtures move to `Signer`; one case keeps the old
header to show the walker reads it through `pact_signers`'s second attempt.
The refusals `tests/test_pact_check.py` pins at lines 471–635 keep their
shape and say `Signer` where the planted pact says `Signer`; a case planting
the old header with a broken table shows the refusal names `Signatory`,
because `gfm_table` names the header it was asked for.

## Operational impact

- **Compatibility, kept.** A pact written with `| Signatory |` and a pact
  review record written with `| Signatory | Change | Verdict |` read as they
  did, and `pact-check` prints one line per such file naming the rename. No
  exit status moves on the old header anywhere.
- **Identifiers.** `hooks/config.py#pact_signatories` → `pact_signers`, · NAME NOT IN TREE
  `SIGNATORY_HEADER` gone, `_signatory` → `_signer`. The plugin's own three · NAME NOT IN TREE
  scripts are the only callers; a vendored copy of `evidence_check.py` does
  not call them.
- **Test files renamed.** Four files under `tests/`; anything outside this
  repository that ran them by path is not known to exist.
- **No migration, no new dependency, no new config row.**
