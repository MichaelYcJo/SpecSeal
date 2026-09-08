# Implementation Plan: the refusal text is unobserved and an uppercase V is invisible

<!-- seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Four tickets, one file, and the same failure underneath three of them: a record
that states a limit nobody measured. #203's docstring and ledger note say the
only unpinned thing is one line, and three mutations disprove it. #205's
docstring and ledger note say an order bug broke a narrower prefix, and it
never did in either implementation. #206's paragraph says the check refuses a
real version whether it has shipped, and it refuses at or above the running one.

#204 is the one behaviour change: `V0.9.0` is this plugin's own version in a
spelling the token cannot see.

The design gate is the tickets themselves — each carries a *What would close
it*, and the routing batch for every 0.9.2 work item was answered before this
one was spawned.

## Technical context

`tests/test_release_hygiene.py` holds the whole surface.

- `refusal(running, offenders)` builds four pieces joined by three separators.
  Enumerated from its own source rather than by reading: the opening sentence
  carrying `{running}`, the timer paragraph, `"\n  ".join(offenders)`, `"\n\n"`,
  `what_to_write_instead()` — and the `"\n  "` that closes the first literal,
  which is the separator *before* the first offender line and is the one three
  consecutive attempts on the original branch missed.
- `VERSION_TOKEN` is `(?<![\w.])v?(\d+\.\d+\.\d+)(?!\.\d)`. The leading class
  has two characters doing two different jobs and no written argument for
  either.
- `is_a_record_of_a_moment` uses `any()`; every `/` entry takes the same
  `DATED_RECORD.match(basename)` check, so only an exact entry — which skips it
  through `rel == entry` — can turn on list order.

**What breaks in six months.** The seven-element case pins wording, so a
rewrite of the refusal's prose reddens it. That is the intended cost: #179's
*Done when* makes the text a deliverable, and a case that survives every
rewording is the case that survived all three deletions here.

> **Corrected by review round 1 — "four pieces joined by three separators" is
> a reading of the source, and the count it produced is wrong.** `ast.parse`
> flattens the returned `+` chain to four operands whose first is one
> `JoinedStr` of three parts: **six** leaves, and the `"\n  "` closing the
> paragraph is the tail of one of them rather than an element beside it. **It
> reaches every use of that vocabulary in this file, not the #206 row alone**
> (round 2 ⬜ 8): §*Technical context* above still says *four pieces joined by
> three separators*, and the alternatives table below still offers *#203 as
> seven assertions*. Both are the superseded reading; neither changes what the
> alternatives were weighed against. The
> approach the table below takes — one assertion per element, each with its own
> message — is unaffected; what changed is that each element is now read WHOLE,
> because reading the paragraph at its two ends left 86 characters that no
> assertion touched. The same round found the other count in this file wrong
> the same way: **two** documents state what the check refuses, not three, and
> the alternatives table's #206 row should be read with that number.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #203 as one structural assertion — build the expected text and compare | It pins the seven as one, so a failure names none of them, and it is `refusal` rewritten in the test | rejected |
| #203 as seven assertions, each with its own message | Wording drift reddens the case; the message says which element went | **taken** |
| #204 by narrowing `(?<![\w.])` so an uppercase `V` is not "a word" | Round 1's finding was exactly this — a lookaround narrowed for one shape taking another with it. `PyV0.9.0` would become an offender | rejected, and the ticket forbids it |
| #204 by widening `v?` to `[vV]?` | Admits nothing the lookbehinds do not already refuse — to be measured, not assumed | **taken** |
| #204 also widening `as_release`'s `lstrip("v")` | Nothing calls it with a prefixed token: `timers_in` passes `match.group(1)`. Speculative, and it drifts a ledger anchor for no claim | rejected |
| #205 with an assertion for the narrower-prefix arrangement | It is the exact failure the ticket names — an assertion over an arrangement that changes no answer | rejected, and the ticket forbids it |
| #206 with a case pinning the three documents agreeing | New mechanism in a fix that four tickets scope to prose; the ticket asks for one sentence | rejected — carried as a follow-up with an answerer |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #204 — the argument beside `VERSION_TOKEN`, `[vV]?`, and the case that pins the widening and the two guards it must not disturb | the new case seen red against `v?`; the loaded-set enumeration run before and after | c05044d |
| 2 | #203 — `test_the_refusal_prints_every_piece_it_builds`, and the neighbouring docstring's false limit corrected | seven mutations of `refusal`, one at a time, each seen red | f6ad622 |
| 3 | #205 and #206 — the case docstring, the two `seal/ledger.md` notes, and the tracker document's sentence | the four arrangements executed through both implementations; the three documents read together | 5b6c533 |

## Operational impact

None. No migration, no environment variable, no dependency. The one behaviour
change is a test-time check refusing one more spelling of this plugin's own
version, and the enumeration over the loaded set says it refuses nothing that
exists in the tree today.
