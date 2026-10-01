# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's routing.md, spec.md (I1–I11, S1–S15), plan.md (phases 1–4), questions.md (A1, A2, Q1–Q5); docs/review-handoff-protocol.md §After the run — the per-segment bars and §Status; skills/agent-contract/SKILL.md §10; agents/framer.md whole; CLAUDE.md §fragments
· evidence: seal/ledger/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file.md P1–P4, G1–G3 added; 22 rows re-read and re-stamped in seal/ledger.md and eight seal/releases files, two of them corrected in place (0.4.0.md, 0.15.7.md A2)
· verified: executed — the narrow modules each phase names, every new case seen red, 16 mutants (one survivor, then killed), evidence-check exit 0 at the tip, --segments over the run's transcript; unverified — the full suite, lint and the broad gate (the sealer's)

## Why this work exists

The framer's opening lived only in spawn prompts and forbade the batching its
own readings need, and `--segments` printed per-kind ratios with no bar beside
them; the opening now lives in `agents/framer.md`, bounded rather than
forbidden, and the page names each row that sits under its kind's bar.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| An existing case had to change for I7 | S10: *every existing assertion passes unchanged*; I7: *`--json` rows gain two keys, `kind` and `bar`*. `test_either_route_prints_the_same_slices` strips a fixed tuple of label keys and compares the rest, so the two keys made it red | I7; the case's label tuple gained `kind` and `bar` | Both cannot hold. The two keys are derived from `agent`, which the tuple already strips for the same reason, so the case's claim — equal numbers row for row — is the one it made before. `seal/releases/0.15.7.md` A2 corrected in place |
| The ungraded line's wording | I5: *a kind the table does not know, a row the parent could not name, an own-file row*. The page says *a kind not listed, a row no spawn named, a segment that made no call* | the page's wording | Two own-file cases refuse *the parent could not name* and *no paired call* anywhere on an own-file page (`test_an_own_file_page_says_what_its_rows_are`, `test_an_own_file_whose_messages_are_adjacent_invents_no_slice`); both are S10's to keep |
| The bound's grounds in the definition | I1: grounds are *this frame's own run, which sent batches of five to seven on every turn of its gather*, and #548 | the definition cites #548 and #640 only | This frame's batches were unmeasured when the definition was written. Measured in phase 4: its five largest turns were 11, 7, 7, 6 and 5 calls, so *five to seven on every turn* undercounts the largest; the reading is in `phases/phase-4.md` and in `questions.md` Q1 |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and the broad gate over the tip | the orchestrator, through the sealer after the review rounds settle (contract §2) |
| A warden row graded on a real transcript: the run measured in phase 4 had no warden segment yet, so only framer and smith rows met the grade outside fixtures | the orchestrator, at the `--segments` reading it takes after this item's first review round |
| `questions.md` Q2 — a framer spawned after this ships, reading its tools per turn and whether it finishes | the orchestrator of the first framer spawn after this merges, posting its `--segments` row to the open `flow-measurement` log |

## Not done

- **A1 is not raised.** The measured largest batch (11) is well above six,
  which `questions.md` Q1 says makes the number loose; raising it is the
  owner's call, and the definition already says the number can be overturned.
- **The protocol's draft is not bumped** (Q5, with grounds in `phases/phase-2.md`).
- **`kind` keeps the name the spec fixed**, though `--spawns` rows use the
  same key for `cycle`/`head`/`tail` (`phases/phase-3.md`).

## Fed back into the spec

None. The divergences above are recorded here and in the phase records;
`spec.md` is the framer's and is not rewritten by the build.
