# Feature Specification: a case pins what it actually measures

Two tickets, one sentence: **a case that asserts vocabulary pins a phrase, and
a case that asserts a clause pins a claim.** #310 is one case that got that
wrong about a paragraph. #262 is the same failure about a module's branches,
and it asks for the thing that finds it rather than for nine more cases.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #262's own argument | *"Nine cases would close today's list and not the class"* — and *"a written list of arms rots the same way the written list of reader passes did"* |
| #310, verified | The replacement assertions are written and were measured red on five mutation arms. Transcription, not design |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* | Why both were deferred: a fix pass may add the unit that pins a finding and may not add mechanism, and #310's fix arrived after its run was capped |
| `tests/test_chain_hooks.py#reader_blanking_passes` | The precedent named in #262: derive the list instead of typing it. The new checker is that idea at module scale |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The checker changes what the suite refuses, so it answers all four: a test seen red, a failure direction, a prompt budget of zero, platform honesty |
| `CLAUDE.md` §*verification that runs unattended* | Decides the shape: an enumeration a person performs is one nobody performs twice. Four fix passes ran this by hand today |

## Scope

**In.**

- **#262** — a checker that enumerates a module's arms **from its own source**,
  mutates each one, and reports the arms no case kills. It runs over
  `hooks/review-history-guard.py` to start, because that is the module whose
  arms were counted by hand and where the count has already rotted.
- **#310** — the four assertions in
  `test_the_section_names_batching_as_the_way_a_share_passes_one_hundred`
  replaced by the verified version, which asserts the two load-bearing clauses
  whole and lower-cases the negative.

**Out.**

- **Nine hand-written cases for the nine unwatched arms.** #262 refuses this
  by name, and it is the whole reason the ticket exists.
- **Running the checker over every module in the tree.** One module's arms are
  what has been measured; a sweep is a second work item with its own numbers.
- Answering *which* arms should be killed. The checker reports; a person or a
  later work item decides which reports are gaps and which are
  behaviour-preserving. #262 already names two of the latter kind.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The arms are enumerated by construction | Given `hooks/review-history-guard.py` / when the checker runs / then it reports one entry per arm, counting each member of a boolean test and of an except tuple separately | a case asserting the per-function counts against a fixture module whose arms are known by construction |
| The enumeration cannot silently go short | Given a module with a new `if` / when the checker runs / then the new arm appears without anything being typed | a case adding an arm to a fixture and asserting the count moves |
| An unkilled arm is named | Given an arm no case kills / when the checker runs / then it names the function, the arm and the line | a fixture module with one deliberately unwatched arm |
| A killed arm is not named | Given an arm a case kills / when the checker runs / then it is absent from the report | the same fixture, with the case present |
| The report is a verdict a person can act on | Given the real module / when the checker runs / then it prints the arms no case kills and exits non-zero only under the condition the plan states | executed against `hooks/review-history-guard.py`, with the count recorded |
| #310's case pins the claim, not the vocabulary | Given `skills/verify/SKILL.md`'s span paragraph / when the two causes are swapped, the measurement inverted, or the old phrase added at the start of a sentence / then the case is red on each | three of the five arms measured in #310, re-run here |
| The two whole-clause assertions survive a re-wrap | Given the paragraph re-wrapped / when the case runs / then it is green | `section_body()` collapses whitespace; a case asserting it |

## Data & interfaces

No schema. One new checker, one `bin/` wrapper if the repository's convention
asks for it, and four assertions replaced in an existing case.

| Fact | Coordinate | Label |
|---|---|---|
| Counted by construction with #262's own rule — each boolean-test member and except-tuple member separately — the module has **31** arms: `reader` 5, `is_closed` 4, `gh_segments` 5, `main` **17** | `hooks/review-history-guard.py` | **executed 2026-09-09** |
| #262's table says 33: the same three functions and `main` **19**. The file has changed twice since that measurement (`341be0b`, `1dedd1e`) | the ticket, and `git log` | executed |
| **So the ticket's own numbers have rotted, which is the argument it makes** | — | read |
| #310's replacement assertions are red on five arms, one at a time, the file restored and sha256-compared after each | #310's body | **executed 2026-09-09** by this session |

## Open questions → questions.md

Two: what the checker's exit code should mean, and whether nine unwatched arms
on the first run is a failure or a baseline. Neither blocks the enumeration.
