# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — overview

📋 implement applied
· spec:     `spec.md` S1–S7 and A1–A20, `plan.md` phases 1–3, `questions.md` Q1–Q6; `docs/the-broad-gate.md` §*Where the stamp is drawn*; `skills/verify/SKILL.md` §*A seal says what it did not answer* and §`mutation-check`; `CONTRIBUTING.md`'s fragment rule as `CLAUDE.md` states it
· evidence: `seal/ledger/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner.md` B1–B3, P1–P2, L1–L4; corrected in place `seal/releases/0.15.7.md` N5 and N7, `seal/releases/0.10.0.md` S2, `seal/ledger/1790815615-….md` N5 and N10; re-read in place the rows each phase record names
· verified: executed — the threshold probe (six headless turns), every case named in the phase records seen red, each phase's modules, the mutations the phase records list; read — the prototype scripts, the owner's chosen output, the rows re-read

## Why this work exists

Every stamp drawn since #666 reached the owner as a preview of a persisted
file, because the harness persists a hook message over 10,000 characters;
the stamp is now a letter of about 6,300 characters, held under a budget the
code names, so it is seen whole.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The threshold probe's sizes | `plan.md` phase 1: *at `N = 9990` and then `N = 10010`*; the build ran 9,990, 10,000, 10,001, 10,010, 12,000 and 9,990 `▀` | the build's six | Two sizes leave the limit anywhere in twenty characters and say nothing about bytes against characters; four more turns pinned both (`phases/phase-1.md`) |
| The gap between the text and the wax | `spec.md` S3: *two clear parchment cells* on every text line; the owner's rendering had zero on the `suite` row | the spec's two | The frame's judgement, named for the owner in the spawn prompt. It moves the disc two cells right on every line — the binding line is the `suite` row, `6621 passed, 11 skipped` — and costs 40 characters over #702's values: 6,279 with the prototype's two trailing empty lines against its 6,239, label included and no final newline |
| Trailing empty lines | The prototype's output ends with two empty lines, the rows of #30's rope-sized grid below the wax | dropped | A line carrying nothing is not part of the letter, and the twin and the block form drop them alike; `phases/phase-3.md` |
| `spec.md` §*What was measured* | named two cases the build renamed, and `hook_success` | a `NAME NOT IN TREE` note on each line | `evidence-check --strict`'s record walk refused the three names; the note records the rename rather than rewriting the frame's measurement (`phases/phase-2.md`) |
| How several pending seals share one message | `spec.md` S1: *one rung for the whole message … A message with two stamps is two stamps at one scale*; round 1 measured two seals of #702's size both drawn without the disc, and eight at 10,118 characters, past the limit | the owner's rule of 2026-10-02 (`questions.md` Q6): as many as fit with the disc, oldest first, each at the highest rung it can take, the rest left pending | Owner-directed, in round 1's fix pass. The rung with no disc stays for a single seal that cannot fit at 0.75 alone; a session that ends right after leaves the rest for `seal-stamp --from`. `spec.md` is left as the frame wrote it |
| What the limit counts | `spec.md` S1 and the frame: characters, as Python `str` length | UTF-16 units | Measured in round 1's fix pass: 4,999 characters outside the BMP were shown and 5,001 persisted, so each counts two; `admitted` counts the same way |

## Not verified

| Item | Who must answer |
|---|---|
| That a real seal of 0.17.0, drawn by the hook, is shown whole rather than as a preview on the owner's screen (`spec.md` §*What cannot be checked*) | the repository owner, on the first real seal after 0.17.0 is installed |
| How the sheet reads on a light terminal background and on a dark one (`questions.md` Q2; the contrast figures are in `phases/phase-3.md`) | the repository owner, on the first real seal on each background |
| What the installed 0.16.0 hook draws over a values file this branch's gate writes, during this release's own run: its rope-and-gold drawing over the new rows, which reading puts under the limit (`questions.md` Q3) | the repository owner, on the first real seal of this branch |

## Not done

Nothing in scope was left. Two things were within reach and not taken: the
twin's characters and the text-set width were decided by the build (Q4) and
pinned rather than asked, and `test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter`
keeps a name half of which is no longer true, because its other half is what
it is for (`phases/phase-2.md`).

## After the chain

The first broad gate, at `c7f7df6e` against `e4399b65`, was NOT SEALED: three
cases red, each one new on this branch. None is a defect in the stamp, and no
round read the repairs, because the capped run had ended.

- `test_no_shipped_script_needs_more_than_the_floor_without_saying_so`:
  `admitted`'s `zip(..., strict=True)` matched the pattern. The file already
  refuses at entry under 3.12, so it is classified `guarded` in
  `CLASSIFIED`, and 0.9.1's R3 is re-read and re-stamped.
- `test_no_loaded_file_names_a_version_at_or_above_the_running_one`: the
  `MESSAGE_LIMIT` comment names Claude Code 2.1.287 as the build the limit was
  measured on. It is pinned in `VERSIONS_OF_ANOTHER_PRODUCT`, beside git's
  rows of the same class.
- `test_only_neutral_domains`: `handoff.md` named the owner's commit address.
  It now names it without the address.

The three modules passed afterwards (77 passed), and then the re-seal ran.

## Fed back into the spec

none — the clauses this work states are in `docs/the-broad-gate.md` under its marker, and the spec was not amended beyond the two `NAME NOT IN TREE` notes.
