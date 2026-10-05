# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | a9bd530b |
| Ran by | unknown — the spawn prompt named no agent or model, and this record is not where a segment names itself |

## What this phase was asked

The word everywhere else, and the check (`plan.md` phase 2):
`templates/config.md` §*Pact*, `templates/seal-README.md` and `seal/README.md`,
`skills/evidence-check/SKILL.md` with its heading renamed,
`skills/implement/SKILL.md`, `skills/implement/orchestration.md`,
`skills/config/SKILL.md`, `README.md`, `README.ko.md`,
`docs/one-root-by-lifetime.md` and `.ko.md`; in
`tests/test_one_word_one_meaning.py` the renamed heading in `PACT_SECTIONS`,
the sweep refusing the old word with fold markers blanked first and two
named exclusions, and the file-name assertion; the S11 enumeration pasted
here. `questions.md` W2: the tests outside the five pact files that hold the
word.

## What this phase found

- **The sweep is its own constant, `PACT_RENAMED`, not a fourth alternative in
  `PACT_LOOSE`.** The two excluded spans say the old word in order to keep a
  0.18.x header reading. Excluding them from `PACT_LOOSE` too would have
  stopped sweeping them for `home`, `member`, `keeper` and the rest, so the
  new case `test_no_pact_text_names_a_signer_the_way_0_18_did` holds the old
  word alone and `PACT_LOOSE` is unchanged. The member lists are not widened,
  so `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found`
  stands. `renamed_header` joins `PACT_PRINTED`, so the rename sentence is
  swept for `PACT_LOOSE` and excluded only from the old-word check.
- **The pattern has no leading `\b`.** `pact_signatories` holds the word after
  an underscore, a word character, and `\bsignator` misses it there and in a
  file name like `test_a_signatory_….py`.
- **The case asserts its exclusions are reached.** A span that stops being
  swept at all would make its exclusion say nothing, so the case fails when
  either excluded `where` is not met, and when the policy's span is the last
  statement in the file (the `SEAL_EXCLUDED` guard's reasoning).
- **`skills/evidence-check/SKILL.md` §*`pact-check` — the signers against the
  pact* gains one paragraph** saying a table headed the 0.18.x way still
  reads and the line moves no exit. It names the old word by description
  only, because the section is swept.
- **W2, the tests outside the pact test files.** Each was a comment or a
  description string and is renamed:
  `tests/test_a_reference_root_is_read_and_never_taken.py` (`SHIPPED`'s
  description of `pact-check`), `tests/test_a_released_row_is_read_again_in_a_fragment.py`
  (the pinned `templates/config.md` sentence, which cites the renamed
  `docs/the-pact.md` heading, and two parametrize ids),
  `tests/test_every_reader_ends_a_line_where_gfm_does.py` and
  `tests/test_the_settings_have_a_front_door.py` (comments). The S11
  enumeration found no fifth.
- **Every fragment that still says the old word is released.** The seven work
  items under `seal/specs/` other than this one whose files hold it,
  1790993137, 1791076833, 1791076834, 1791090130, 1791119072, 1791128260 and
  1791163980, are each gathered into `changelog/0.18.0.md` to `0.18.3.md`, so
  no ungathered changelog fragment carries the word into 0.19.0.

Seen red, each through `bin/mutation-check` at `a9bd530b` against
`test_no_pact_text_names_a_signer_the_way_0_18_did` (verdict `red` every time):

| Mutation | What it shows |
|---|---|
| `templates/pact.md` says `every OTHER signatory` (S10) | the sweep names the planted text: `templates/pact.md names a signer the way 0.18.x did: ['signatory']` |
| `skills/evidence-check/SKILL.md` says `each signatory's checkout` | a swept section is read |
| `hooks/config.py#_signer` prints `every signatory below it` | a `PACT_PRINTED` unit is read |
| the `renamed_header` exclusion removed | the unit is swept, and the exclusion is what lets it say the word |
| the policy span's removal skipped | the statement is swept, and the span is what excludes it |
| fold markers not blanked | the released id `1790993137-a-signatory-…` would otherwise fail the sweep |

The file-name half was seen red by a probe, `tests/test_tmp_signatory_name.py`,
run once and deleted: `a test file is named with the word 0.19.0 renamed:
['test_tmp_signatory_name.py']`.

**S11, executed** — `git grep -i -n signator -- ':!changelog'
':!seal/releases' ':!seal/ledger.md' ':!seal/specs'` at `a9bd530b`, exit 0, by
file:

| File | Hits | Why it stays |
|---|---|---|
| `docs/the-pact.md` | 11 | 8 fold markers naming the released work item `1790993137-a-signatory-declares-…`; 3 lines of this work item's statement about the old header, the sweep's first excluded span |
| `hooks/config.py` | 1 | `renamed_header`, the one unit writing the old tuple, the sweep's second excluded span |
| `tests/test_pact_check.py` | 7 | the S2 compatibility cases plant and assert the old header |
| `tests/test_a_signer_declares_its_pact.py` | 12 | the S2 and S4 compatibility cases |
| `tests/test_a_pact_review_takes_a_pact_change.py` | 5 | the S5 compatibility cases |
| `tests/test_a_signers_ci_prints_its_pact.py` | 4 | the S6 old-header case, and the S1 assertion that a new pact prints no old word |
| `tests/test_one_table_walker_reads_what_gfm_renders.py` | 4 | the walker's old-header case |
| `tests/test_one_word_one_meaning.py` | 3 | the sweep's own pattern and the comments naming what it refuses and why markers are blanked |

The compatibility cases spell the old header rather than read it from
`hooks/config.py#renamed_header`, so `overview.md` records this list as wider
than S11's. A case taking the header from the reader's constant would pass
with that constant changed while every 0.18.x pact stopped reading.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/evidence-check/SKILL.md`'s heading `## \`pact-check\` — the signatories against the pact` | `## \`pact-check\` — the signers against the pact`; the released ledger rows citing it are re-pointed in phase 3 |
