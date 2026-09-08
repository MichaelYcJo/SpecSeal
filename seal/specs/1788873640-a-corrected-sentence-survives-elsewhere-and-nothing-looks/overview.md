# a corrected sentence survives elsewhere and nothing looks — overview

📋 implement applied
· spec:     `docs/flow.md` §0.9.3 (the `#180` row, which supersedes the ticket's `Done when`) · `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments*, §*no real identifiers* · `skills/agent-contract/SKILL.md` §1 §2 §3 §5 §8 §9 §10 §12 §14 §15 · `skills/implement/SKILL.md` §1–§4 · `skills/code-review/SKILL.md` §*Orchestrator: a fix pass resumes the implementer*, §*A fix pass adds the unit that pins it* · `seal/follow-up.md` · this item's `routing.md` · issues #180, #267, #269, #229
· evidence: six rows in `seal/ledger/1788873640-a-corrected-sentence-survives-elsewhere-and-nothing-looks.md`, hashes written by `evidence-check --reverify`
· verified: **executed** — the check against `7bcf36a` and `ad6f81a`; the calibration over 77 real ranges and 4 pull-request-shaped ones; `tests/test_a_corrected_sentence_survives_elsewhere.py` 31 passed; two mutation sweeps, 25 mutations, 24 caught. **read** — the base full suite, `2808 passed, 2 skipped in 439.63s` at `c0a65d5`, run by the orchestrator. **unverified** — the suite on this branch, and the CI step under GitHub's runner

## Why this work exists

A fix repairs the coordinate a finding named while the same claim stays
standing somewhere else, seven measured times including once by a session that
had read the rule against it — so this ships the check that looks, and the
eighth sentence nobody would have read is not written.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The phase table | `plan.md` planned four phases: the reader, the check, the calibration, then the carriers | Three, with 1–3 merged and a new phase 3 for what verification found | None of the first three is a runnable slice alone: a threshold is a measurement OF the finished check, and the reader's normalisation is observable only through the score that reads it. Splitting them buys three commits that cannot be verified apart, which is what `plan.md`'s own *vertical slices* line forbids |
| The threshold's unit | `plan.md` §The metric: *`score(corrected, candidate)` = the summed `idf` … Report a candidate whose score reaches `BITS`* | A score divided by `log2(F)`, whose unit is one phrase occurring nowhere else | The plan's form made the constant a property of THIS repository's 633 files. A two-file probe scored a survivor plainly standing there at 2 against a floor of 15, so every smaller repository running the plugin would have been silently exempt from a check reporting clean |
| The independence requirement | `plan.md` §The metric, step 6, and the `SHARED_FLOOR` constant beside it | No such constant | A mutation sweep found it could not change a single answer: one run is capped at 1.0 and the floor is 1.6. A constant that cannot change the answer tells a reader the requirement lives somewhere it does not |
| Where a survivor's own file is judged | `plan.md` §The metric, step 3: *the sentences the file held at `A` and does not hold at `B`* | Sentences the file holds FEWER times at `b` | The plan's membership form misses #267's shape one file narrower — a claim repaired in one copy and left in another copy of the same file reads as untouched, because the wording is still there |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite on this branch. Contract §2 reserves it for the orchestrator; the base reading of `2808 passed, 2 skipped` is cited as read, not executed | the orchestrator |
| The CI step under GitHub's runner. Its shell was executed locally under `bash -eo pipefail` with an empty exemption glob and with `--exempt` arguments, but `github.base_ref` and the `refs/pull/*` fetch above it exist only in Actions | the orchestrator, at the pull request |
| Whether the CI step should fail or only report. It fails, on a measurement of four real pull requests in THIS repository's corpus; #229 is the evidence that the class arrives from repositories with different corpora — a documentation set of fifteen files, where every sentence has more neighbours | the repository owner (`questions.md` Q2) |
| `seal/ledger.md` row R3 still carries *What is left unpinned is only the one line…*, a claim a docstring in `tests/test_release_hygiene.py` corrected. Found by this check on three separate branch ranges, and standing in the tree today. Not fixed here: it is #267's own second open item, that `CONTRIBUTING.md` §House rules does not name the case of correcting a false note in a row that has not drifted, which two branches have already had to decide without a written rule | the repository owner, on #267 |
| `survivors.md` has no template and no checker of its own, so a malformed row exempts nothing silently rather than being named | the repository owner (`questions.md` Q3) |
| Reporting a candidate against its weakest matching source instead of its best. The one mutation of 25 that survived both sweeps: the floor is applied per source-candidate pair before the tie-break, so a candidate reaches it twice only when two sources each clear the floor alone, which neither real range produces. It would change which true source is named, never whether a survivor is reported | the repository owner, if a range ever produces two clearing sources |

## Not done

**The other two rules #180 names are out of scope with a home each, and both
are named in the pull request body.** The `-C` rule — the commit gate guesses
which repository a commit reaches when a command spells `cd … && git commit` or
`git -C .` — belongs to **#22**, and building a `PreToolUse` hook here would put
a second gate beside the one that ticket is about. The handoff's ledger count —
a handoff must not assert a number taken from the scoped read — belongs to
`docs/review-handoff-protocol.md` and to the checker that today only warns; it
is `questions.md` Q1 with the repository owner as answerer.

**No fourth document was written.** The ticket's own *Not this* section forbids
it and it is the failure mode this work replaces. The reasoning lives in the
script's docstring, which is where this repository already keeps it, and the
three carriers that run the check name it in one paragraph each.

**Contract §12 was not widened with the method.** That is #180's third rule and
this work does not take it.

## Fed back into the spec

- **A floor above 1.0 is what requires two independent phrases**, inferred
  during implementation. `plan.md` had a separate constant for it and the
  arithmetic already guaranteed it; a planner may overturn the removal, but
  only by moving the floor below 1.0 first.
- **A record of a past round is excluded for a second reason nobody planned
  for**, inferred during implementation. `plan.md` gives one — those files
  quote a finding's wording by design — and the measurement found the exclusion
  does not do that job at the shipped floor, where the records sit 0.09 below
  it anyway. What it does do is stop those files diluting `idf` for the phrases
  they carry, which moved #267's shared-file row from 1.69 to 1.79.
