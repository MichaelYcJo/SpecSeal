# 1791076833-the-reverify-writer-records-before-it-restamps — overview

📋 implement applied
· spec:     this item's `spec.md` (Decision 1, Scope items 1–13, W1–W10, K1–K2), `plan.md`, `questions.md` Q1–Q7; `docs/the-pact.md` §*A signatory records a pact change* and §*What this does not see*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `skills/settle/SKILL.md` §*A standing statement has one shape*; PR #749's fragment, `changelog.md` and `survivors.md` at `b4c9deb2`
· evidence: `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md` — ten claim rows carried (W1, W2, G1, G2, C1, D1, D2, F1–F3; C1's claim corrected), three added (W8, W9, W10), one `Corrected ·` row (0.18.0's P8), 50 `Re-read ·` rows
· verified: executed — the module runs, red-first runs and mutations listed in `phases/phase-1.md` and `phases/phase-2.md`, and `evidence-check --strict`, `survivor-check`, `correction-check`, `unverified-check`, `chain-check` named in `phases/phase-3.md`; read — every released row re-read; unverified — the full suite (the sealer's)

## Why this work exists

#647 C and D were built once and refused at depth 2 inside their own chain;
carried here whole, they are reviewed from round 1, and the writer now also
stops claiming writes it did not make, stops rewriting bytes it could not
decode, and names a ledger it cannot write instead of ending in a traceback.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many comments changed on the way in | spec: "the 17 code and test comments citing `round N of #647 C and D`", and four changes "and nothing else" / the build: 19 round citations, and two more comments citing PR #749's `questions.md` Q2 and phase 2 | the build | a citation wrapped across a line is still a citation (§12), and "`questions.md` Q2" and "phase 2" resolve to this item's own, different files in this tree. `phases/phase-1.md` has the enumeration |
| Whether `--into` is read strictly inside the run | spec W9: a file the run would write "— a ledger it plans, `--into`, the record —" that will not decode is unreadable under W3 / code: step 0 refuses such an `--into` at exit 2 before anything is planned, and `reverify_into` reads it leniently after | step 0's refusal | Q4's own option text: "`--into` is already read strictly at step 0". A strict read behind it survived its mutation, so it was taken out (`4a9bdd06`) |
| What a run under `--into` that cannot record prints as its count | spec W8 names the `wrote` and `citing rows written` lines / code: the whole line `N citing rows written · M released rows left` is held, so its released-rows-left count goes with it | the code | spec silent on the second half of the line; each left released row still prints its own `LEFT` line |
| Which name the W10 line prints | spec: "names each file it could not write on a `LEFT` line with the cause" / phase 2 used `built_name`, then `2e5c6c35` switched to `display_name`, and the post-review fix after the seal switched it back, with W9's `ledger unreadable` line beside it | `built_name` | 0.18.0 prints every path in `/` form (#735), and CI's Windows leg read `seal\ledger\…` on the W9 line. `built_name` is `display_name` with `/` for the separator, so 0.8.3's row, "Every place a ledger path becomes a name a person reads calls `display_name`", still holds through it. Re-reading that row in phase 3 sent the line the wrong way, and no macOS run could see it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck on this branch | the sealer, once, after the review rounds settle |
| The W10 and `--into` apply-step cases on Windows and as root: both skip there, under the module's `UNREADABLE` mark, because a directory's mode is not expected to refuse a write on Windows and refuses nothing as root | the repository owner, who decides whether a Windows case that refuses the replace some other way is worth building; CI's Windows leg runs the module with both cases skipped, so until then the platform half is a stated gap rather than a pass |
| #741's encoding check over the carry set (Q7): its check had not landed on `release/v0.18.1` when this branch was built | the smith or the orchestrator, at the merge of `release/v0.18.1` after #741 squashes |

## Not done

Closing PR #749 and its comment are the orchestrator's (`spec.md`
§*Decision 1*). #746's refusal of a stale `--checked` is not taken; W9's seam
sentence in `spec.md` is where it goes. No `fsync` was added (Q3).

## Fed back into the spec

none — the frame's count of 17 is corrected in `phases/phase-1.md` rather
than in `spec.md`, which records the frame as approved.
