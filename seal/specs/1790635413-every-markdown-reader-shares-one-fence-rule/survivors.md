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
