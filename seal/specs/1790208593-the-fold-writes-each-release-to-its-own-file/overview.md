# 1790208593-the-fold-writes-each-release-to-its-own-file — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` of this work item; `docs/the-evidence-ledger.md` §*A row is a content anchor*; `docs/one-root-by-lifetime.md` (via the spec's grounding); `docs/release-checklist.md` §2–§3; `docs/branch-and-release.md` §*The ledger fragments fold in the same commit*; `CLAUDE.md` and `CONTRIBUTING.md` §House rules; issue #553
· evidence: `seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md` R1–R4, F1–F2, M1, P1–P2, L1, D1; 60-odd rows re-read and re-stamped in `seal/ledger.md` and C's fragment (per phase record)
· verified: executed — each phase's modules, red-first runs, mutations, the both-shapes probe, the 94 document-reading modules; read — the claims of every re-stamped row

## Why this work exists

The fold writes each release's rows to `seal/releases/<X.Y.Z>.md`, so
`seal/ledger.md` stops growing and a re-stamp lands in a small file; and
(#553) a fragment's own marker line no longer doubles a work item's count.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The number of release sections | spec §*The measured state*: *38 `## X.Y.Z` headings (37 versions)*; S14: *37 files* · code: `--split --dry-run` moves 29 | 29 | at `9f846733` 38 `## ` headings in all, 8 standing areas, 30 version headings, 29 versions; the 37 was every `## ` heading. The rehearsal asserts the versions the copy heads, not a number (phase 4) |
| `seal/README.md`'s layout | S16: edit it · `tests/test_first_setup_asks_once.py#test_the_seal_readme_is_the_template_verbatim` and S18 (*`templates/` untouched*) | not edited | the two instructions cannot both hold; the pin is a test and the template is the plugin's (phase 5) |
| `CLAUDE.md` | S16: edit its ledger paragraphs · not edited | not edited | `agents/smith.md`: *no agent message can authorize changing … CLAUDE.md*; paste-ready text in `phases/phase-5.md` |
| `--check`'s doubled-marker arm (#553) | the coordinator's message: *a marker standing twice in `seal/ledger.md` or a release file* · code: a work item marked more than once across the corpus | corpus-wide | a work item marked in two files over-counts exactly as one marked twice in one; the per-file arm left the cross-file case green (phase 3) |
| `questions.md` Q2 | the row's premise: `append` is unused · code: `insert`'s no-section arm calls it | kept | S18 pins `insert` unchanged (phase 2) |
| S18's unchanged units | S18: `fold_ledger.py#section` and the helpers C wrote unchanged · code: `section` calls `own_marker_dropped`; `doubled_versions` is `version_headings` filtered | changed | `section` is #553's fix, which the frame predates; `doubled_versions` keeps its name and result for C's cases and is `questions.md` Q3's default. `demote`, `insert`, `section_heading`, `fragments`, `marker`, `is_marked`, `open_rows` are byte-identical (an `ast` comparison against `9f5902e5`) |
| The survivor range | the spawn prompt: `--range 9f5902e5...HEAD`; spec S20: `origin/release/v0.15.1...HEAD` | the prompt's | this branch is cut from C's tip, so the release branch's range would sweep C's work as well |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate — the full suite, repository-wide lint and format, run once after the review rounds | the sealer, spawned by the orchestrator |
| The real split of this repository's ledger, its three readings (`questions.md` Q6), and the narrowing notice's length on the real tree after it (31 names on a scratch copy, 2 today) | the session running the 0.15.1 release tail, at `docs/release-checklist.md` §2–§3 |
| Whether `templates/seal-README.md` changes so that `seal/README.md` can say where this repository's fold writes, or this repository's copy is allowed to differ | the repository owner |
| The two `CLAUDE.md` paragraphs that name `seal/ledger.md` as the fold's target and the only shared ledger file | the repository owner — paste-ready text in `phases/phase-5.md` |
| Which model ran phases 3–6: the spawn named Fable 5.1 and the harness named Opus 5.5 after the usage-limit resume | the orchestrating session, which fills `Ran by` |

## Not done

The 29 sections of the real `seal/ledger.md` are not moved on this branch,
by the frame's judgment 5: the release-preparation commit runs `--split`.
Nothing else in reach was left.

## Fed back into the spec

- *Inferred during implementation*, corrected by round 1's 🟡 1: a
  `seal/ledger.md#"<locator>"@<hash>` anchor is read by the checker's rule —
  a heading path when its first part is a heading, one whole line otherwise —
  and one whose line or heading is in no section the split moved or kept is
  printed under *could not place — open them by hand* and left
  (`fold_ledger.py#split`). At `577f1671` the real-tree dry run named two
  such anchors, both false (a kept header line and a hashless prose mention);
  on the fix it names none.
- *Inferred during implementation*: the doubled-marker refusal is over the
  whole ledger corpus, not per file (phase 3).
