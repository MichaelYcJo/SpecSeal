# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build.** The owner answered the three person-only
questions in #822 on 2026-10-06, before this frame was drawn. They are inputs,
recorded here so nobody reopens them, and they are not rows.

| Decided by the owner | Answer |
|---|---|
| The new word | `signer` / `signers`. `party` was rejected because `docs/the-agent-set.md` and `skills/implement/orchestration.md` already use it for the agents, and one word has one meaning here; `member` is a #647 working word that `PACT_LOOSE` in `tests/test_one_word_one_meaning.py` refuses |
| A pact written with `\| Signatory \|` since 0.18.0 | keeps working: `pact-check` reads both headers, prints one line naming the rename where it read the old one, and `templates/pact.md` begins a pact with `\| Signer \|`. Refusing the old header was offered and declined |
| What does not change | `pact`, `pact change`, `pact review`, `pact anchor`, `pact-check`, the `Pact` / `Pact notify` rows of `seal/config.md`, every path under `seal/`; and released records (`changelog/*.md`, `seal/releases/*.md`, process records under `seal/specs/` other than this one) keep the word they were written with |

**What the tree answered, so nobody reopens it.** Each of these the spawn
prompt left to the frame, and each was settled by something that can be
opened.

| Judgment | Answered by |
|---|---|
| Whether the released ledger rows this rename moves are REMOVED in place and re-claimed in the fragment, as the spawn prompt (reading `CLAUDE.md`) said | **No.** `seal/config.md` declares `Ledger frozen from \| 1790993141`, this work item's id `1791239490` is above it, and `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* says a released file is never edited under the freeze and *a released row whose anchor moved … a `Corrected ·` row re-points it*. `correction-check` (`.github/workflows/hygiene.yml` line 307) refuses the range otherwise. The REMOVED sentence in `CLAUDE.md` is the rule for a repository without the row, which the same document says in §*Without the row, a released row is kept true where it stands* |
| Whether the moved anchors DRIFT or BREAK | **BREAK.** A renamed test file, a renamed `def`, a renamed heading: the unit is gone from its address, which is BROKEN by `docs/the-evidence-ledger.md` §*A row is a content anchor*. `--reverify --into` names each one with the `Corrected ·` repair and exits 1 (§*Five things `--reverify` leaves at exit 0…*, second bullet) |
| Whether the pact review record's `\| Signatory \| Change \| Verdict \|` header gets the same compatibility reading as the pact's table | **Yes, the same reader and the same printed line.** `docs/the-pact.md` §*A pact review takes a pact change* makes the record permanent and 0.18.1 shipped its header with the old word; a refusal would read every record a pact review took as `NOT TAKEN` again at exit 1. The owner's second decision names the pact's table only; this extends it by the same argument, and a reviewer overturns it by opening that section |
| How `tests/test_one_word_one_meaning.py` holds the new word and refuses the old one | `PACT_LOOSE` gains `signator(?:y\|ies)`; fold markers `<!-- specs/… -->` are blanked before the sweep, because `1790993137-a-signatory-declares-…` is a process record's id and keeps the word; two spans are excluded by name on the `SEAL_EXCLUDED` precedent (its lines 240–248 say why a span and not a file): the `docs/the-pact.md` statement about the old header, and the `hooks/config.py` unit holding the old tuple and the rename sentence. A `tests/test_*signator*.py` file name is refused too. The sweep's member lists are not widened, so `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found`'s closure stands |
| Whether the `Enforced by:` node ids in `docs/the-pact.md` can lag the test renames | **No.** `tests/test_a_folded_statement_names_what_enforces_it.py`'s real-tree case resolves every target through `fold_check.py#target_problem` at cutoff `0`; a renamed file or `def` is red in the same suite. So `docs/the-pact.md` is in phase 1 with the tests, not in phase 2 with the prose |
| Whether a `# RIDER:` comment names a renamed unit | **None does.** `grep -rn RIDER` over `*.py` and `*.md` outside `.git` has no hit containing `signator` (2026-10-06) |
| Whether `seal/follow-up.md` holds an item this work is the prerequisite for | **No.** Its one row (line 70) is about `changelog/0.12.2.md`'s evidence label |
| Where the sentence naming the rename lives | `hooks/config.py`, as every refusal sentence both commands print already does (`tests/test_one_word_one_meaning.py` line 607's comment; `seal/releases/0.18.0.md` row P8's grounds). `pact-check` prints it as a line in no exit class; `chain-check` appends it to the notice it already prints at the pact's repository, and its exit does not move (`docs/the-pact.md` §*A signer's CI prints and verifies nothing*) |
| The changelog fragment's shape | `seal/specs/<id>/changelog.md` under `### Changed`, no line starting `## ` (`docs/the-record-layout.md` §*A change writes fragments, never a shared file*; the gather refuses a `## `). The `### Fixed` precedent is `seal/specs/1791128260-…/changelog.md` |
| Whether the Korean texts translate the word | **No.** `README.ko.md` line 282 keeps the product's word in English with a gloss, `signatory(그 계약에 서명한 저장소)`, which is `skills/writing-style/SKILL.md` §*용어는 실물을 확인하고 고른다*'s rule for a word the product made; it becomes `signer(그 계약에 서명한 저장소)` |
| Whether a version number belongs in the printed line | **Yes, 0.19.0**, the release this branch ships in (`release/v0.19.0`). The changelog is one file per release (`changelog/X.Y.Z.md`), so the number is the address of the entry that explains the line |

**The rows below are the residue.** None needs a person. Two are
measurements the build runs, and two are the work's to decide when it meets
them.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | Which released families does the rename break, exactly? The frame read 127 distinct anchors over about 28 roots by `grep` (`plan.md` §*Technical context*), and a root a `Corrected ·` row already supersedes (`P8`, `C1`) takes its row against the superseding row | a measurement | `evidence-check --reverify --into seal/ledger/1791239490-…md --checked <date>` after phases 1–2 names each BROKEN coordinate under a released root with its repair, at exit 1 | the grep's list; the run's list wins where they differ | ⬜ |
| M2 | Does `fold-check` accept the new statement in `docs/the-pact.md` — one bold sentence, grounds, one `Enforced by:` line whose targets are the S2 and S5 cases? | a measurement | `tests/test_a_folded_statement_names_what_enforces_it.py`'s real-tree case, in phase 1's slice run | written in that shape; the run says | ✅ yes — the real-tree case passed in phase 1's slice run at d6bcdd36, the statement citing four targets (the S2, S5, S6-old-header and S4 cases); phase 2 adds the sweep's case as a fifth |
| W1 | The third return value of `pact_signers` and `pact_reviews`: the header tuple read, a boolean, or a sentence to print | the work | a tuple keeps the information and lets `gfm_table`'s refusal wording follow it; a boolean is smaller; a sentence moves the words out of `hooks/config.py`'s one unit. The frame fixes only that a caller can tell the old header from the new without re-reading the text | the header tuple read, `None` where neither read | ✅ the default: the header tuple read, `None` where neither read, through one unit `hooks/config.py#read_table`. The tuple is what lets every refusal and `pact-check`'s own table sentences name the header the file holds; the sentence stays in `#renamed_header` (`phases/phase-1.md`) |
| W2 | Which tests outside the five pact test files pin a string holding `signatory` (`tests/test_the_settings_have_a_front_door.py` line 1, `tests/test_every_reader_ends_a_line_where_gfm_does.py` line 1, `tests/test_a_reference_root_is_read_and_never_taken.py` line 1, `tests/test_a_released_row_is_read_again_in_a_fragment.py` line 3 each hold the word, in a docstring or a fixture) | the work | each is a rename or a fixture header; phase 2's slice run and the S11 enumeration find any the frame's grep missed | renamed in phase 2 | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. There is none here.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row in `overview.md`; it does not travel
  back to the framer.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.
