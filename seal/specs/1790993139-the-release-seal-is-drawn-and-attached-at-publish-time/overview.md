# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — overview

📋 implement applied
· spec:     `spec.md` S1–S16, `plan.md` phases 1–4, `questions.md` Q1–Q11; `CONTRIBUTING.md` §*Running the checks*; `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`*; `docs/release-checklist.md` §6; `.github/scripts/publish_release_note.py`'s module docstring; `CLAUDE.md`'s fragment and ledger rules
· evidence: `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md`; corrected in place `seal/releases/0.17.0.md` B1; re-read in place `seal/releases/0.17.0.md` B2 and `seal/releases/0.16.0.md` G1, G2 and the rows each phase record names
· verified: executed — every case named in the phase records seen red, each phase's modules, the mutations the phase records list; read — the hand-drawn 0.17.0 script, 0.17.0's published note, the rows re-read

## Why this work exists

The 0.17.0 seal was drawn and attached by hand; the tag push now draws one
for every release and puts it where the note's glance table stood, and any
failure leaves the note exactly as it is published today.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The case that pins the reserve | `spec.md` S14: *the reserve comment's re-measured figures are pinned by the case that already pins 533 and 909*; no case in `tests/` named either number at `6ee8d2b7` | a new case, `test_two_failed_gates_fit_the_reserve_with_every_field_at_its_cap`, measuring the report and requiring the comment to state each figure | `git grep` over `tests/`; `phases/phase-1.md` |
| The reserve's figures | `spec.md` §*Scope* 5: `909 + 2 × (40 − 19) = 951`; measured 957 | the measurement | 909 was already stale at the base: today's `GROUPS` give 915 with a 19-character name (`phases/phase-1.md`) |
| What `describe` caps at read | `spec.md` §*Scope* 5 and `plan.md` phase 1: `error` and `message`; the build also caps `group` | the build's three | Contract §12 and `spec.md`'s own grounding row: every field the report takes from a record without a fixed vocabulary. `group`'s vocabulary is fixed only at this plugin's writer |
| The pixel pin's ink check | `spec.md` S6: *the darkest pixel is nearer the cell's ink than `PARCHMENT`*; that check passed with the ink's red and green swapped | some pixel is the ink exactly | Measured with `bin/mutation-check` over `rgb`'s cube levels: every glyph at this size covers whole pixels in Menlo and in Pillow's default (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| Which font `ubuntu-latest` gives `font()` (`questions.md` Q11) | the work: the first CI run of the pixel case under `-s`, and the first live run at a tag, whose log names it |

## Not done

Nothing yet.

## Fed back into the spec

none
