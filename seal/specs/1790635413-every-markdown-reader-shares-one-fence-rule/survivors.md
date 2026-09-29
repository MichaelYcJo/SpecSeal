# Survivors — every markdown reader shares one fence rule

`survivor-check --range c2478597..56a47561` reported one place. The sentence
this range rewrote is the role test's `headings` docstring, which used to
describe its own copy of the fence rule; the standing sentence describes the
meter's case for round 2's finding 13, and what it says of a closing fence is
still true under the shared rule.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_payload_meter_says_what_it_measured.py` | Round 2, finding 13: a fence closes only on a fence of the same character at least as long | `fence_closes` closes only on a run of the opener's character at least as long, so the sentence holds; it is the docstring of `test_sections_do_not_split_at_a_heading_inside_a_fence`, which passes unchanged over `heading_starts` on the shared rule |
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/plan.md` | a routing row quoted inside a fence in `routing.md` reads as a declaration | phase 8's own row, which describes the defect the phase was asked to fix; it is the ask, not a claim about the tree (`phases/phase-8.md` says what was done) |
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/spec.md` | and the `--exempt` file reader in `survivor_check.py#main` | the framer's out-of-scope row as the frame stood; the plan's phase 8, added at the owner's request after round 1, supersedes it, and the frame is the framer's document rather than this build's to rewrite |
| `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | a comment opener and a closer each quoted in a code span, on lines either side of the table, read as a comment that closes and hide the table | round 1's dated re-read note on H1, a record of what round 1 decided; the `Corrected` note after it in the same row says round 2 reversed it, and a correction appends rather than rewrites a note |
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/spec.md` | What the copy does not model is therefore exactly what the oracle does not model | the framer's frame as it stood; round 2 moved the hook copies and the oracle together onto `_liveness`'s literal reading, so the sentence still holds of the pair, and the frame is not this fix pass's to rewrite |
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/spec.md` | inside a code span is read as an opener, as `comment_scan` and every reader through `readable` already read it | the framer's frame as it stood (the quote starts after the comment opener, which this file cannot hold: `read_exemptions` reads it through `readable`, which would open a comment there); round 2 reversed it for the hook copies at the reviewer's finding and the orchestrator's answer to the ❓, and `overview.md` is where the build records a divergence; the frame is not this fix pass's to rewrite |
| `skills/implement/scripts/seal.py` | `fence_map` is the fence walk with the state it ENDS in kept | still true: `fence_map` returns `walk`'s shown lines and the index of an unclosed opener |
| `hooks/cmdline.py` | A name is UNBOUND rather than left alone when the assignment is one this reader does not model | an unrelated sentence about shell assignments that shares only the phrase *does not model* |
| `seal/specs/1790297086-the-broad-gate-says-what-ci-says/plan.md` | Every guard spelling it does not model is silently not mirrored | an unrelated work item's plan that shares only the phrase *does not model* |
| `seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/plan.md` | which the checker's four ledger walks read through | work item A's (#585) plan, merged in from `release/v0.16.0` at `33d77479`. It quotes `fence_opener`'s docstring as it stood before this branch's phase 7 reworded that sentence, and what it quotes still holds: the docstring still names `evidence_check.py#quoted_lines` as the unit the checker's four ledger walks read through. The plan is A's frame and not this branch's to rewrite |

The rows for `seal.py` and the ledger's H1 row no longer anchor anything:
the revert after round 3 put `seal.py` back to the release's text and
removed H1, so neither quote stands. The grounds of the two `spec.md` rows
above them name round 2's hook copies, which the same revert took out; the
frame's sentences they excuse are the framer's and still stand.

The revert after round 3 takes `hooks/config.py`, `hooks/routing.py` and
`.github/scripts/rider_check.py` back to `release/v0.16.0`'s text, with
everything that existed only because of them. `survivor-check` over it
reported 66 places.

| Range | Grounds |
|---|---|
| `4edc5de6..4588df33` | the revert after round 3. Every sentence it removed was written by this branch's phases 3, 6 and 8 and round 1's and round 2's fixes to them, and the places still carrying that wording are the durable copies that describe the release's behaviour, which is the behaviour the three readers have again (`hooks/config.py`'s own fence copy, `fold_ledger.py`'s and `payload_meter.py`'s kept sentences on the shared rule, other work items' frames), or this work item's own records of what was built and taken out (`overview.md`, `phases/phase-6.md`). `git diff origin/release/v0.16.0 -- hooks/config.py hooks/routing.py .github/scripts/rider_check.py` is empty at `4588df33` |
