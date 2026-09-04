# 1788501054-a-check-reports-clean-while-something-is-missing — phase 7

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-7.md
— what this phase of the build did, written by the implementer when the phase
closes. Not in `plan.md`'s original four: round 3's fixes are work the plan did
not contain, and the phase row was added beside them, the way phase 6's was. -->

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | e94c3de |
| Ran by | specseal:smith on opus — filled by the orchestrator that spawned it. The prompt named neither, and `templates/sdd-phase.md` forbids a segment sourcing this from its own idea of what it is, so the cell read `unknown` until the caller answered it. The spawn prompt is where it belonged; #137 gave the row to the record and not to the prompt that fills it |

## What this phase was asked

Round 3's eight open 🟡, handed over **as four classes plus two singletons**
rather than as eight coordinates, with one instruction above all of them:
*fix the class, not the coordinate*. Three of the eight were the unclosed half
of a round 2 finding — the rule that was to stop a recurrence, the case that
was to hold a choice, and eight of the ten rows a rewritten claim requires —
and each time the previous pass had fixed where the finding pointed. That is
`agent-contract` §12, and by round 3 it had cost this work item three rounds.

The four classes as they were given:

- **A — a documented choice held by nothing.** 🟡 6 (`st_ino` over `st_dev`)
  and 🟡 7 (the template phrase must START the reason). Enumerate every
  decision this branch argues in prose inside a unit it changed, and mutate
  each one.
- **B — a description that disagrees with the code it describes.** 🟡 4, and
  the declared-limit halves of 🟡 5 and 🟡 8. Enumerate every description of
  the units this branch changed.
- **C — every row a re-stamp touched.** 🟡 2. Ten rows changed, ten
  re-stamped, eight carrying a re-read clause; `phase-4.md` enumerated the
  class as eight and phase 6 grew it to ten with nobody re-enumerating.
- **D — a contract change's reach.** 🟡 8. Grep the call sites of every unit
  this branch changed, not the two the row names.

And the two singletons: **🟡 1**, the arm that cannot fire on the record it
was built for, separated into a data half and a limit that is a design
question; and **🟡 3**, the terminal `Fixes checked by` value missing from the
spec's table, whose refusal question was explicitly *not* this phase's to
decide.

Two constraints came with it. Every case written or widened had to be seen red
(§15), and the reviewer's own proposals arrived labelled unverified and to be
judged rather than adopted.

## What this phase found

**The enumeration is what the round could not do, and it produced more than
the round did.** Eighteen mutations across class A returned **nine survivors**
where round 3's twelve returned two. Four of the seven new ones are real and
closed here; three are unreachable, and that distinction is the phase's main
finding.

**A mutation battery cannot tell an unheld decision from an unreachable
guard.** `says_not_yet` has three decisions in it and all three survive
mutation, but only one is a hole: `fix_surface` is its only call site and it
calls the function behind `says_none`, so the `none` prefix and the separator
after it have already been checked by the time a value arrives. No case
through the CLI can kill either. The same shape appears twice more —
`normcase` in the path fallback is reachable only where CPython zeroes an
inode, which is the one platform where `normcase` is not the identity, and
`seal_home`'s `SKILL.md` conjunct needs a vendored copy with a plugin tree
above it. All four are now recorded in the code that carries them, because the
next battery will find them again and read them as findings.

**Two of the survivors were closable only by moving something other than the
code.** `default_patterns` (ledger row R4) had stood as *Read* for two rounds
with the reason written down: no ordinary case can distinguish one spelling of
a list from two, because the two are identical on the day they are written.
What separates them is moving the DEFAULTS — the case adds a fourth location
and asks whether the skipped set followed. `resolve_patterns`' deduplication
is the same shape one step out: the three default patterns are disjoint, so no
run through them can produce a duplicate, and `--ledger` taking any number of
globs is where it bites.

**A case can be written for the right defect and still prove nothing.** The
deduplication case was written against the per-ledger `1 ok` line and stayed
green under its own mutation, because each pass over the file prints its own
count and only the total adds them. §15 is what caught it — nine cases, nine
shown red, and this one twice.

**Class B is wider than a scan of the finding's own file.** Enumerating every
description of every changed unit found three instances round 3 had not named:
`overview.md`'s divergence row and the widened case's own docstring both
carried the *rewording* claim, and `skills/evidence-check/SKILL.md` named one
way out of the inode fold where the code has two — a description that went
stale when round 2's fix landed and nothing re-read it. A fourth is sharper:
`docs/review-chain-spec.md` says *only the ABSENT row is grandfathered* four
lines below a table row stating that a PRESENT one prints before `ORDER_FROM`.
The same sentence sits in `seal/ledger.md:181`, which is where class C's
re-read found it.

**The declared limit was answered by widening the sentence and not the match,
and the reviewer's reason for that was wrong.** Its argument was that
enumerating punctuation is the unbounded domain this file declines twice. The
measurement says something narrower and firmer: of the three spellings that
escape with the template's words unchanged, only one is punctuation. A doubled
space sits INSIDE the constant, so no separator set reaches it; a clause in
front of the phrase is reached only by a substring match, which is the exact
mutation 🟡 7 requires to stay refused. Widening `SEPARATORS` would close one
of three, leave the sentence false about the other two, and move a constant
four other readers in the file share.

**On 🟡 6 the reviewer's depth reasoning was also wrong, and the act it
proposed was still right.** It argued that a new unit answering either 🟡 6 or
🟡 7 would be depth 2. That holds for 🟡 7 — `says_not_yet` is in round 2's
`New units` — and not for 🟡 6, because `skipped_by_narrowing` was added by
this branch's phases and predates the run, which makes a unit answering a
finding inside it depth 1. Widening the existing case is better anyway: it
adds no unit, so the depth question never arises, and the widened case is
where the separating state belongs.

**🟡 4's pin is the one thing the depth rule genuinely refuses.** The finding
is inside `says_not_yet`, a depth-1 unit, so any unit added to pin its
docstring is depth 2 and the rule's own exit applies: deferred with a named
answerer, or an issue. It is a `# RIDER:` at the function, because
`seal/follow-up.md`'s header sends anything tied to a coordinate there.

**🟡 1's widening was declined, with the reasoning written down rather than
the decision.** A non-terminal record carrying `nobody` is false by
construction — a later record exists, and round N+1 reviews round N's fixes —
so keying the arm on the sibling records would answer both this and 🟡 3. It
is a change to a gate with its own cutoff, its own cases and its own spec
subsection, and it would give the arm the second source of truth that ledger
row R7 records as the reason the narrow key is defensible at all. It is
`questions.md` Q4 with three options and the repository owner as answerer.

**Round 2's `Contract changes` row was corrected in place, and the precedent
for that is on this branch.** A phase record's prose is what that phase found,
which is why `phases/phase-3.md:53` keeps a rule that has since changed. A
round record's FIELD rows are different: they are read by `chain_check.py` and
by the next round as a finding surface, and they assert something about the
branch rather than about the round's own moment. `4b72d7e` already corrected
`round-1.md`'s `Needs a fix` count on exactly that ground. `phase-4.md` was
corrected only where it made a present-tense claim — *all eight rows now carry
a clause* — which phase 6 made false; what phase 4 itself did is untouched.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The claim that the pending arm's escape is **a rewording**, from `docs/review-chain-spec.md`, `chain_check.py#says_not_yet`, ledger row R7, `changelog.md` and `overview.md` | Each of the five now names the three spellings that escape with the words unchanged, and `test_the_declared_limit_names_what_escapes_with_the_words_unchanged` pins three of them. `phases/phase-6.md:49` keeps the old sentence deliberately, as a record of what phase 6 believed |
| The claim that **only the ABSENT row is grandfathered**, from `docs/review-chain-spec.md` and `seal/ledger.md:181` | Both now say that the pending arm grandfathers a row which is PRESENT, keyed to `ORDER_FROM`, and that what still holds is the refusal of a MALFORMED row at any age |
| `round-2.md`'s claim that `main` is the only call site of `fix_surface` and of `skipped_by_narrowing` | The same cell, with both second call sites named and the correction marked as round 3's |
| `round-1.md`'s `Fixes checked by: nobody — …` | The same cell, reading `round-2`. `git merge-base --is-ancestor b87ba49 4b72d7e` exits 0, so round 2 did open those fixes; the arm then prints nothing at all for that record |
| Ledger row R4's *Read* status, and with it the sentence that no case distinguishes one spelling of the defaults from two | The row is **Executed** now, against a case that moves the defaults rather than the code |
