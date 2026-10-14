# what an agent opens on demand states the current rule only — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. -->

**Judgments the ticket left open that the tree answered** — listed so nobody reopens them; the grounds are in `spec.md` and `plan.md` §*Alternatives considered*.

- The shape, the check, the proof and the ledger plan are #923's and are applied, not redesigned; what this item adds is in `spec.md` §*What this set needs that the preload set did not*.
- The templates are in: their content is comments, a comment is a rule for its cell, and `templates/sdd-routing.md`'s is instanced 108 times (alternative F).
- The orchestrator is a reader with no agent, so its files are proved by the acts table's `check:`/`command:` rows plus five rule-exercise cases that end at their artifact (alternatives J, K, L).
- Which suites a phase runs is read off the transcript census, dated in `spec.md` (alternative I; Q1 asks about its cost).
- Order: the file in every prefix first, the largest second, the orchestrator cases before the first orchestrator file (alternative C).
- One branch, coupled files in one phase (alternatives A, B).
- `seal/README.md`, the standing `routing.md` copies and the user's global `CLAUDE.md` block are out (alternatives M, N).
- The small skills are read against the shape and left where they hold; `skills/writing-style/outside-the-review.md` is the tree's own and is in.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Proving the on-demand set costs more agent runs than the preload set, because nearly every file here is opened by all four agents: four phases run all four suites (≈ 38 runs, ≈ 2.5 h at `-j 4` and ≈ 25 M uncached input tokens each) and three run three, ≈ 16 h and ≈ 150 M tokens over the item on the orchestrator's account, on top of #923's. Is that accepted? | a person — the owner pays for the runs and set the condition | **accept**: every reader's full suite per phase, `spec.md` §*Non-inferiority, per file*. **subset**: only the rule-exercise cases a file's census maps to, roughly a third of the runs; needs a `--cases` filter in #923's comparator (Q2) and loses the replay and seeded cases, which no on-demand file's rules are shown by anyway. **batch**: phases 2, 7 and 8 merged into fewer, larger phases sharing one eval each; cheaper by two or three suite runs, and the review chain reads a larger census per record | accept | ⬜ |
| Q2 | Does #923's comparator accept an agent name outside the four (`orchestrator`) and a case subset, and does its record test read its scope from a fixed set? If fixed, `plan.md` phase 1 widens the scope and phase 3 adds the name here; if #923's smith makes both configurable in its phase 2, this item changes nothing there | #923's smith — a disagreement with its design, named here for it | configurable in #923 phase 2 · changed here in phases 1 and 3 | changed here | ⬜ |
| Q3 | Can a `claude plugin eval` case grade the absence of a tool call (no `AskUserQuestion`), run a post-run command (`git log --name-only` into a file the regex grader reads), and take its cases from a directory other than the plugin target, so the merge base's tree can be run against this branch's new cases? | a measurement — phase 3's first act runs O1 against today's tree and reads what the harness offers; where a grader kind is missing the case's `scaffold.sh` writes the fact into a file and a regex reads it, and where the eval dir cannot differ the cases are copied into the archived tree | the cases as `spec.md` describes | ⬜ |
| Q4 | `skills/legacy-parity/SKILL.md` (5,364 B) is `scribe`'s preload and appears in neither #923's scope nor its `Out`; #923's `preload:scribe` target of 17,128 implies it stays as is. Whose row is it? | #923's smith | #923 reads it against the shape in phase 6 with `agents/scribe.md` · this item takes it in phase 8 | #923, phase 6 | ⬜ |
| Q5 | `A range that DELETES a shipped section` is stated in `agents/smith.md` (#923 phase 5) and `skills/code-review/orchestration.md` (this item's phase 4) at Jaccard 0.53. Which is the home? The orchestrator runs `survivor-check`; the smith obeys its reading | #923's smith — whichever phase lands second writes the link | home `skills/code-review/orchestration.md`, the smith links · home `agents/smith.md`, this item links | home `skills/code-review/orchestration.md` | ⬜ |
| Q6 | Of the 984 pinned literals in the set, which pin a rule and which pin narration that goes? | the work — each phase sorts its file's pins as it rewrites and lists the dropped ones in `phases/phase-N.md` and `overview.md` | — | ⬜ |
| Q7 | Do the 151 released rows on `templates/config.md` all still hold after its rewrite, or does any claim move onto a test (`Corrected ·`)? The 89 on `## Broad gate` drift together | the work — phase 7 reads them one at a time and the fragment records each | — | ⬜ |
| Q8 | How many of `skills/verify/SKILL.md`'s 57 rules can no case show (`not exercisable`)? The owner's condition is weakest where that list is longest | the work — phase 2's census; the round reads the list | — | ⬜ |

One row waits on a person (Q1), and it blocks nothing before phase 1's eval run; two are #923's smith's (Q2, Q4, Q5 — three rows, one party); one is a measurement; three are the work's. The three kinds are the template's.
