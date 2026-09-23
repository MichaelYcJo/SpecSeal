# 1790154761-folded-statements-pile-into-one-spec — overview

📋 implement applied
· spec:     `spec.md`, `plan.md` (approved at `fb2b03f7`), `questions.md`; `skills/settle/SKILL.md` §2; `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*; `CONTRIBUTING.md` §*House rules* (*Both READMEs move together*); `docs/one-root-by-lifetime.md` and `.ko.md` in full outline, and the English §*What the repository decides for itself, and how it is read* line by line; `skills/verify/scripts/unverified_check.py#FOLD_MARKER`, `#live_lines`, `#folded_items`; `tests/test_settle_reads_before_it_removes.py#test_both_editions_took_the_same_decisions`; `tests/test_docs_line_wrap.py#COVERED`
· evidence: `seal/ledger/1790154761-folded-statements-pile-into-one-spec.md` E1, S1, P1 added; `seal/ledger.md` — the release-`--check` row (anchor `CONTRIBUTING.md#"The fold refuses, naming the file…"`) and C8 (`CONTRIBUTING.md#"## House rules"`) re-read and re-verified, each with a `Re-read` marker, because phase 1's edit to the README rule sits in the same section
· verified: executed — the three new modules (6, 14 and 12 cases), each red first and then under one-at-a-time mutations; the narrow set `test_settle_reads_before_it_removes`, `test_first_setup_asks_once`, `test_no_document_names_the_old_roots`, `test_unverified_rows_close`, `test_release_hygiene`, `test_docs_line_wrap`, `test_the_rules_have_one_owner`, `test_no_real_identifiers`, `test_one_word_one_meaning`, `test_a_document_that_names_a_script_says_how_to_reach_it`, `test_the_records_can_be_carried_out_and_in`, C8's `a8` case; `evidence-check --strict .` (exit 0); `ruff check` and `ruff format` on the three new modules. read — the Korean translation's fidelity to the English section. unverified — the broad gate

## Why this work exists

Two folds put 29 of 101 folded statements into one 2,159-line document and none into the Korean edition of another, with no rule saying where a fold lands or what a statement must carry. The next fold now meets three written rules, and a test reads each one.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the values paragraph sits in the evidence ledger | `spec.md` §*Overlap with PR #525*: "places its paragraphs directly after the *top level of `docs/`* paragraph". Built: at the head of §*The fold, and what tells it from a deletion*, above the first marker | the section head | A statement's provenance runs from its marker to the next marker or heading (settle §2, and the shape check's own reading). After that paragraph, this non-fold text would read as part of `1790039346`'s fold. The head has no marker above it and is further from the lines #525 rewrites |
| What the base's red looked like | `plan.md` phase 1: "Seen red at the base (10 ids against 0)". Executed: red on the heading levels first (23 positions against 22), then, with the heading added and no markers, red on the missing ids | both reds, in that order | The check compares ids only when the outlines agree, because a shifted outline would misattribute every id below the shift |
| The frozen count is compared for equality | `spec.md` §Scope item 3: the check "fails when a listed file gains a marker" | equality: gaining or losing a marker fails | A removed marker left unrecorded is room the next fold can refill without the count moving. The message says to lower the count. *Inferred during implementation* |
| Targets may be in backticks | `spec.md` §*Data & interfaces*: "A target is `path` or `path::name`" | backticks around a target are accepted and stripped | A markdown writer puts a path in backticks by habit, and refusing that would fail the first real fold on form. Settle §2 says so. *Inferred during implementation* |
| One `Enforced by:` line under an 88-column limit | `spec.md`: the line is "a line of its own". Six top-level `docs/` files are in `tests/test_docs_line_wrap.py#COVERED` | unchanged: one line | No fold has met it yet. A folder with several long targets names the module rather than each case. If that proves too tight, the choice is the wrap test's exemption or a continuation form, and it belongs to whoever meets it at the 0.14.0 fold |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds |
| The Korean section reads as the same rules as the English one. The check pairs markers and headings, never sentences | the warden in review, or the repository owner, reading both editions side by side |
| The pairing test stays green when PR #525 merges, since #525 adds one dated section to each edition by hand | whichever of the two branches merges second; its narrow run of `tests/test_both_editions_carry_the_same_folds.py` after the merge |

## Not done

- **Q1, Q2 and Q4 were built on their defaults**, as `questions.md` says each may be: the Korean edition is kept and paired (Q1), the ceiling is 1000 lines (Q2), and a design record may take a fold (Q4, the status quo). Each row stays open for the repository owner. A different answer to Q1 or Q2 changes one constant or one file and no phase order.
- **Q5 was the work's, and it is answered** in phase 1: each marker sits above the Korean paragraph carrying the same statement, directly under the heading for the five on shared sections. `questions.md`'s row is ticked by the work, which is the party its `Who can answer` cell names.
- **The chain spec is not split, and the 101 existing statements are not retrofitted.** Both are MichaelYcJo/SpecSeal#526's, filed by the orchestrator before phase 3, together with shipping the checks as a plugin command.
- **`docs/one-root-by-lifetime.ko.md`'s other drift is not audited.** The pairing test reads outline and markers. Whether each Korean paragraph still says what its English one says is the unverified row above.

## Fed back into the spec

- *Inferred during implementation*: the frozen marker count is an equality, not a ceiling on growth (neither settle §2 nor the evidence ledger states it; the ceiling test's message does).
- *Inferred during implementation*: an `Enforced by:` target may be written in backticks (settle §2, second bullet of the shape rule).
