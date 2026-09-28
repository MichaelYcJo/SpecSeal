# Survivors — every markdown reader shares one fence rule

`survivor-check --range c2478597..56a47561` reported one place. The sentence
this range rewrote is the role test's `headings` docstring, which used to
describe its own copy of the fence rule; the standing sentence describes the
meter's case for round 2's finding 13, and what it says of a closing fence is
still true under the shared rule.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_payload_meter_says_what_it_measured.py` | Round 2, finding 13: a fence closes only on a fence of the same character at least as long | `fence_closes` closes only on a run of the opener's character at least as long, so the sentence holds; it is the docstring of `test_sections_do_not_split_at_a_heading_inside_a_fence`, which passes unchanged over `heading_starts` on the shared rule |
