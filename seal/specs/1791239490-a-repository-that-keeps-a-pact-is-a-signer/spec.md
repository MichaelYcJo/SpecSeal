# Feature Specification: a repository that keeps a pact is a signer

<!-- seal/specs/1791239490-a-repository-that-keeps-a-pact-is-a-signer/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#822. `signatory` names every repository of a work item that keeps a pact
(#647), and it is a word a reader stops at. The owner renamed it `signer` on
2026-10-06, and this work carries the new word into every live text, keeps a
pact written with the old table header reading, and leaves every released
record as it was written.

| Word | Before | After | Ships |
|---|---|---|---|
| the repositories of a work item that keeps a pact | `signatory`, `signatories` | `signer`, `signers` | yes |
| the pact's one-column table header | `\| Signatory \|` | `\| Signer \|`, and `\| Signatory \|` still reads | yes |
| the pact review's first column | `Signatory` | `Signer`, and `Signatory` still reads | yes |
| `pact`, `pact change`, `pact review`, `pact anchor`, `pact-check`, `Pact`, `Pact notify`, every `seal/` path | unchanged | unchanged | — |
| `party`, `member` | — | **nowhere**: `party` is the agents' word, `member` a #647 working word | no |

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #822, the owner's three decisions (2026-10-06) | the new word is `signer`; the old header keeps reading and `pact-check` names the rename on it; the other pact words and every `seal/` path stay. Recorded in `questions.md`, not reopened here |
| `CLAUDE.md` §*The goal a design is chosen against* | a pact written in 0.18.0 keeps working without a person editing it; the rename is a printed line, never a refusal |
| `CLAUDE.md` §*Repo rule — a thing more than one party can have is named with whose* and `tests/test_one_word_one_meaning.py` | one word, one meaning: `party` is taken by `docs/the-agent-set.md` and `skills/implement/orchestration.md` for the agents, which is why `signer` and not `party`. The check, not the rule, is the repair: the sweep refuses `signatory` after this work |
| `docs/the-pact.md` §*The words* | the definition sentence is the policy's, and it changes here: *every repository of such a work item is a signer*. The three names stay the owner's, now given twice (#647, #822) |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, and `seal/config.md` row `Ledger frozen from \| 1790993141` | this work item's id is above the cutoff, so **no released ledger file is edited**. A released row whose anchor this rename moves — a test file name, a test function, `hooks/config.py#pact_signatories`, a heading — is re-pointed by a `Corrected ·` row in `seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md` that carries every coordinate the claim still rests on. `correction-check` refuses the range otherwise. This overrides the spawn prompt's reading of `CLAUDE.md`'s REMOVED-in-place sentence, which `docs/the-evidence-ledger.md` §*Without the row, a released row is kept true where it stands* says is the rule for a repository without the freeze |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | the changelog entry is `seal/specs/<id>/changelog.md` with no `## ` line; the ledger rows are the fragment above |
| `seal/config.md` row `Fold shape from \| 0`, `tests/test_a_folded_statement_names_what_enforces_it.py` | every statement under `docs/` is a bold sentence, grounds and one `Enforced by:` line whose targets resolve. Renaming a test file or function renames every `::node` that cites it in `docs/the-pact.md`, and the new statement about the old header is written in that shape with this work item's marker |
| `skills/agent-contract/SKILL.md` §14, §15 | every printed line that changes — `pact-check`'s summary, `chain-check`'s count, the rename line — is pinned by a case seen red first |
| `skills/agent-contract/SKILL.md` §12 | the class is *every live text that says the word*, enumerated by `git grep -i signator` over the tree minus the records, and the handover says what the enumeration found |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | every URL in a planted pact is on `example.com` |
| `skills/writing-style/SKILL.md` §*용어는 실물을 확인하고 고른다* | `README.ko.md` keeps the product's word in English with its Korean gloss, as it does today: `signer(그 계약에 서명한 저장소)` |

## Scope

### In

1. **The word, in every live text.** `signatory` → `signer`, `signatories` →
   `signers`, `signatory's` → `signer's`, in: `docs/the-pact.md` (the
   definition sentence, three `##` headings, every paragraph, every
   `Enforced by:` node id), `docs/one-root-by-lifetime.md` and `.ko.md`,
   `templates/pact.md`, `templates/pact-review.md`, `templates/config.md`
   §*Pact*, `templates/seal-README.md` and `seal/README.md` (identical lines),
   `skills/evidence-check/SKILL.md` (its `## \`pact-check\` — the signatories
   against the pact` heading included), `skills/implement/SKILL.md`,
   `skills/implement/orchestration.md`, `skills/config/SKILL.md`,
   `README.md`, `README.ko.md`; the docstrings, comments and printed strings
   of `hooks/config.py`, `skills/evidence-check/scripts/pact_check.py`,
   `skills/evidence-check/scripts/evidence_check.py`,
   `skills/code-review/scripts/chain_check.py`; and every test.
2. **The identifiers.** `hooks/config.py`: `SIGNATORY_HEADER` →
   `SIGNER_HEADER = ("Signer",)`, `pact_signatories` → `pact_signers`,
   `_signatory` → `_signer`, `PACT_REVIEW_HEADER = ("Signer", "Change",
   "Verdict")`; and their callers in `pact_check.py`, `chain_check.py` and the
   tests. Local names (`signatory`, `signatories`, `signatory_at`,
   `SIGNATORY_URL`) follow.
3. **The test names and file names.** `tests/test_a_signatory_declares_its_pact.py`
   → `test_a_signer_declares_its_pact.py`;
   `tests/test_a_signatory_records_a_pact_change.py` →
   `test_a_signer_records_a_pact_change.py`;
   `tests/test_a_signatorys_ci_prints_its_pact.py` →
   `test_a_signers_ci_prints_its_pact.py`;
   `tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py` →
   `test_a_pact_anchor_is_no_coordinate_of_the_signer.py`; moved with `git mv`.
   The fifteen test functions whose names hold the word (listed in `plan.md`)
   are renamed, and every `Enforced by:` line and code comment citing one
   follows.
4. **The compatibility reader.** `pact_signers` reads a `| Signer |` table,
   and where the text holds none, a `| Signatory |` table, and tells its
   caller which it read. `pact_reviews` does the same for
   `| Signer | Change | Verdict |` over `| Signatory | Change | Verdict |`. A
   pact or a record that holds a `Signer` table is read from it alone. The
   old header tuple and the one sentence naming the rename live in
   `hooks/config.py`, in a unit `tests/test_one_word_one_meaning.py` names
   as the allowed span.
5. **The rename, printed.** Where `pact-check` reads the old header of the
   pact or of a pact review record, it prints one line naming the file, the
   old header, the new one and the release that renamed it (0.19.0), in no
   exit class — the exit is what it would be with the new header. Where
   `chain-check` at the pact's repository reads the old header, its existing
   notice gains the same sentence; its exit status does not move
   (`docs/the-pact.md` §*A signer's CI prints and verifies nothing*).
6. **The templates begin with the new word.** `templates/pact.md` opens its
   table `| Signer |`; `templates/pact-review.md` opens `| Signer | Change |
   Verdict |`.
7. **The policy.** `docs/the-pact.md` §*The words* says `signer`, and gains
   one statement in fold shape under this work item's marker: the old header
   reads, the rename is printed, and the texts keep one word.
8. **The check.** `tests/test_one_word_one_meaning.py` pins the new
   definition sentence, refuses `signatory` and `signatories` in every text
   `pact_texts()` sweeps — fold markers `<!-- specs/… -->` blanked first,
   because a process record's id keeps the word — with two named exclusions:
   `docs/the-pact.md`'s statement about the old header, and the `hooks/config.py`
   unit holding the old header tuple and the rename sentence. It also refuses
   a `tests/test_*signator*.py` file name. `PACT_SECTIONS` names the renamed
   `skills/evidence-check/SKILL.md` heading; `PACT_PRINTED` names
   `pact_signers` and `_signer`.
9. **The ledger.** One `Corrected ·` row per released family whose anchor this
   work moves (about 28, read by `grep`; `evidence-check --reverify --into`
   names the exact set), each carrying every coordinate the claim still rests
   on with the moved ones at their new place and a `Corrected <date>` note;
   new rows for what this work adds (the reader, the printed line, the check,
   the templates, the policy). `evidence-check --strict .` exits 0 at the end
   and `seal/ledger.md` and `seal/releases/*.md` are byte-identical to the
   base.
10. **The changelog fragment**, `seal/specs/<id>/changelog.md`, under
    `### Changed`: the rename, the old header still reading, the printed line,
    the renamed identifiers and test files.

### Out

- **Released records keep their word.** `changelog/*.md`, `seal/releases/*.md`,
  `seal/ledger.md`, and every `seal/specs/<id>/` directory other than this
  one, their directory names included (`1790993137-a-signatory-declares-…`).
  The fold markers in `docs/the-pact.md` that name that id keep it.
- **The other pact words and every path.** `pact`, `pact change`, `pact
  review`, `pact anchor`, `pact-check`, `bin/pact-check`, the `Pact` and
  `Pact notify` config rows, `seal/pact.md`, `seal/pact-changes/`,
  `seal/pact-reviews/`, `~/.claude/specseal/pact-paths.md`.
- **The pact-changes record** (`| Clause | Row | Code | Checked |`): it never
  carried the word.
- **Refusing the old header**, and any migration command that rewrites a
  pact: the owner chose a reader that keeps working.
- **A version-agnostic rename line**: the line names 0.19.0, because the
  changelog is per release and the reader will look for it there.
- **Every `signatory` in `hooks/config.py` and `evidence_check.py` that is a
  comment naming an old test file path** is in scope under item 1; nothing in
  those two files is out.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a new pact reads silently | a pact whose table is `\| Signer \|` with one `example.com` row; `pact-check` runs at its repository / it reads the signer as today, prints no rename line, exit as before | a case in `tests/test_pact_check.py` asserting the `READ` line and the absence of the rename line, seen red against the old reader (which refuses `Signer` as "holds no table") |
| S2 a 0.18.0 pact keeps working | the same pact headed `\| Signatory \|` / it is read identically, one line names `seal/pact.md`, `\| Signatory \|`, `\| Signer \|` and 0.19.0, the exit is unchanged (0 where S1 is 0) | a case beside S1 asserting the line's text and equal exit; red against a reader that reads `Signer` only |
| S3 neither header | a pact with no table / refused as today, the refusal naming `Signer` | the existing `test_a_pact_with_no_table_or_an_unfilled_one_is_refused`, reworded |
| S4 a pact with both tables | a `\| Signer \|` table and, below, a `\| Signatory \|` one / the `Signer` table is read, the other is not, no rename line | a case in `tests/test_a_signer_declares_its_pact.py` |
| S5 a 0.18.1 pact review record keeps working | `seal/pact-reviews/<id>.md` headed `\| Signatory \| Change \| Verdict \|` naming a taken record / the record is taken as today, one rename line names the review file, exit unchanged; headed `\| Signer \| … \|` it is taken silently | two cases in `tests/test_a_pact_review_takes_a_pact_change.py`, red against a reader that reads one header |
| S6 `chain-check` counts signers | the pact's repository at a pull request / the notice says `which lists 2 signers`; where the header is the old one the same notice carries the rename sentence, and the exit status does not move | `tests/test_a_signers_ci_prints_its_pact.py::test_the_pacts_repository_prints_how_many_signers_it_lists`, and one case for the old header |
| S7 the summary counts signers | `pact-check` over a pact listing one and two signers / `1 of 1 signer read`, `2 of 2 signers read` | the existing summary assertions in `tests/test_pact_check.py`, reworded and seen red |
| S8 the templates | `templates/pact.md` and `templates/pact-review.md` / each begins its table with `Signer`, and `pact_signers(template text)` refuses the placeholder row as today | the existing template cases, reworded |
| S9 the policy | `docs/the-pact.md` / §*The words* says *every repository of such a work item is a signer, the one holding the pact included*; three headings renamed; a new statement under `<!-- specs/1791239490-… -->` in fold shape; every `Enforced by:` target resolves | `tests/test_one_word_one_meaning.py::test_the_pacts_words_keep_one_meaning` (the sentence); `tests/test_a_folded_statement_names_what_enforces_it.py`'s real-tree case (the targets) |
| S10 the check refuses the old word | `signatory` planted in any text `pact_texts()` sweeps, or a `tests/test_*signator*.py` file / red, naming the text; the two allowed spans and the fold markers / green | the case seen red by planting the word in `templates/pact.md` before the sweep gains it, and recorded in the handover |
| S11 no live text keeps the word | `git grep -i -n signator -- ':!changelog' ':!seal/releases' ':!seal/ledger.md' ':!seal/specs'` plus `seal/specs/1791239490-*` / the hits are exactly: the old header tuple and the rename sentence in `hooks/config.py`, the compat statement in `docs/the-pact.md`, the fold markers naming `1790993137-a-signatory-…`, and this work item's own files | the command's output, pasted into `phases/phase-2.md` |
| S12 the ledger stays true and the released files stay | after the build / `evidence-check --strict .` exits 0; `git diff --stat origin/release/v0.19.0...HEAD -- seal/ledger.md seal/releases` prints nothing; `correction-check --range origin/release/v0.19.0...HEAD` exits 0 | the three commands, exit codes read directly (§1) |
| S13 the fragment | `seal/specs/<id>/changelog.md` / exists, under `### Changed`, holds no line starting `## ` | `python3 .github/scripts/gather_changelog.py --version 0.19.0 --dry-run` or the gather's own refusal |
| S14 the Korean texts | `README.ko.md`, `docs/one-root-by-lifetime.ko.md` / `signer(그 계약에 서명한 저장소)` in the cheat-sheet row, `signer` in the tree line; `PACT_LINES` still finds the row | `tests/test_one_word_one_meaning.py` |

## Data & interfaces

- `hooks/config.py#pact_signers(text)` → `(signers, refusals, header)`:
  `signers` as `remote_entries` parses them, `refusals` as today worded for
  the header actually read, `header` the tuple read — `SIGNER_HEADER`, the
  old one, or `None` where neither read. The exact third value is the work's
  to shape; what the frame fixes is that a caller can tell the old header
  from the new one without re-reading the text. `pact_reviews(text)` returns
  the same third value.
- `hooks/config.py`: `SIGNER_HEADER = ("Signer",)`; the old tuple and the
  rename sentence as module constants in one unit named by the sweep's
  exclusion. Their names are the work's; `SIGNATORY_HEADER` is not kept as a
  name, because keeping it would keep the word in an identifier the sweep
  does not read.
- `pact_check.py`: one line per old header read, shape `pact-check:
  <file> heads its table \`| Signatory |\`, the word before 0.19.0 — \`| Signer |\`
  is the header now; rename it when the file is next edited`, printed before
  the `READ`/status lines of that file, in neither `EXIT_ONE` nor `EXIT_TWO`.
- `chain_check.py#pact_notices`: `plural(len(signers), "signer", "signers")`
  and, where `header` is the old one, the rename sentence appended to the
  pact's notice.
- Ledger coordinates this work moves: `hooks/config.py#pact_signatories` →
  `#pact_signers`; `skills/evidence-check/SKILL.md#"## \`pact-check\` — the
  signatories against the pact"` → `… the signers …`; `docs/the-pact.md`
  headings *How a signatory names the pact*, *A signatory records a pact
  change*, *A signatory's CI prints and verifies nothing*; every
  `tests/test_a_signatory*.py#…` and
  `tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py#…`
  coordinate (127 distinct anchors in `seal/releases/0.18.0–0.18.3.md`,
  read by `grep` 2026-10-06).

## Open questions → questions.md

Nothing blocks the build. `questions.md` records the owner's three decisions
as answered, the judgments the tree settled, and two measurements and two
work-time rows.

Framed 2026-10-06 by framer, before the build.
