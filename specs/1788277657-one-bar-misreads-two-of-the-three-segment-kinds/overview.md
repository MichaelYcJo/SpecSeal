# one bar misreads two of the three segment kinds — overview

📋 implement applied
· spec:     CLAUDE.md (goal clause, fragment convention), docs/review-handoff-protocol.md
            (whole document), skills/code-review/SKILL.md (orchestrator sections),
            agents/smith.md §Phases steps 4–5, specs/1788224363-…/questions.md Q1,
            .specseal/follow-up.md (empty tables — nothing waiting on this work)
· evidence: 2 rows in .specseal/map/1788277657-one-bar-misreads-two-of-the-three-segment-kinds.md;
            1 row re-verified in .specseal/map.md (the protocol's handoff-section anchor,
            re-read in full while writing into it)
· verified: executed — pytest on test_docs_line_wrap / test_one_word_one_meaning /
            test_no_real_identifiers / test_the_handoff_before_round_one (28 passed),
            evidence_check --strict (69 ok, 0 drifted). Read — the inserted sections,
            the neighbouring anchored regions. Unverified — the broad gate (below)

## Why this work exists

Three decisions the owner made on 2026-09-01 existed only in an issue
discussion and a session transcript; this writes them where the parties they
govern already read, so the next run is judged (and resumed) by rule rather
than by memory.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The spawn prompt quoted `agents/smith.md`'s caveat as "1.27 tools per turn" | the file reads "1.08–1.17 tools per turn where review rounds read 1.29–1.89" | the file's figures, used in the bars section | a spawn prompt ranks below the ratified documents (`implement` §1); recorded as A2 in `questions.md` |

## Not verified

| Item | Who must answer |
|---|---|
| ✅ the broad gate — full suite, lint, typecheck | executed at 6dee2ca: 1142 passed · 1 failed · 1 skipped, ruff clean, evidence --strict 69 ok, unverified/chain/gather exit 0; the one failure (a PR #67 pin holding the draft's literal number) fixed at 0b126c4 and its file re-run in full, 31 passed — recorded as round-3. Session of 2026-09-02 |
| ✅ that the next fix pass is actually run as a resume, and that the bars are applied per segment kind | executed by this work item's own chain: the round-1 fix pass ran as a resume (21 calls / 3.8m on the corrected meter) and the segments were read against the bars this change writes. Session of 2026-09-02 |

## Not done

The fix pass wrote no pins of its own invention: round 1's tests-todo
prescribed four, and all four were planted as prescribed (the draft-number
pin first, seen red against the state it guards). What stays not done: no
pointer was added in `agents/smith.md` or
`agents/warden.md`: their existing sentences already carry the same measured
ranges, and an edit there would drift four minor ledger anchors to say
nothing new (A3 in `questions.md`).

## Fed back into the spec

none
