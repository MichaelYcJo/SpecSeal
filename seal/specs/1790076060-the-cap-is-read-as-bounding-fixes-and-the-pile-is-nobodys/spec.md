# Feature Specification: the cap bounds rounds, and a filed finding names who acts

<!-- seal/specs/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys/spec.md
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Two tickets, #492 and #493, and they are one question from two ends. #492: the
cap bounds ROUNDS and was read as bounding FIXES, so a one-line verified repair
was filed instead of made. #493: filing runs at 100% and action at 47%, and
nothing asks who will act. Both are sentences the review chain follows, and
this work repairs the sentences. Neither half adds mechanism — that is #330's,
and it is out of scope below.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The review run has a bound, and an end* | The cap counts rounds that found something, because it exists to stop a loop that is not converging. It decides whether another round is spawned — never what happens to the findings of the round it stopped at. This is the section that owns the cap, so it is where the repaired sentence goes |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | The second exit, and it is not the first one in other words. After a record whose floor row reads `no`, at most one later record may close on a fix; `chain_check.py`'s reopening walk **refuses the second**. So the terminal record of THAT exit commissions nothing, and a sentence letting it write fixes would name a state the checker refuses |
| `docs/review-chain-spec.md` §*What the record carries — a declaration, and why no check reads it* | The moratorium: no new parsed field in `round-N.md` and no new row the ledger must carry. Every field arrived with a checker arm, a template row, a protocol row and a cutoff. This work adds none of the four |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | Unchanged, and it is the reason a fix written at the cap is still bounded: a finding closable only by a rule, a checker, a template section or a walk is filed whoever owns the unit. #493 names this rule as one of the two that produce the pile and explicitly does not touch it |
| `seal/follow-up.md`, its opening rules | *Every row names a person, with no condition attached*, and *anything tied to a coordinate is a `# RIDER:` comment at the line it is about*. The tracker has neither rule, and the two files are filled by the same act at the same moment. This work gives the tracker the first one |
| `docs/issues-and-milestones.md` §*An issue is its body and its comments together* | A comment is how a ticket grows here, which is what makes *comment on the issue that already owns the ground* a home rather than a workaround. That document owns the tracker, so anything about where a filed finding goes has to agree with it |
| `CLAUDE.md` §*a thing more than one party can have is named with whose*, and `skills/writing-style/SKILL.md` §*여럿이 가질 수 있는 것은 누구 것인지 밝힌다* | Two different bounds both exit with the word `capped`, and the run's own documents use the one word for both. Naming them apart — **the round cap** and **the reopening bound** — is what keeps the repaired sentence from being true of one exit and false of the other |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Bounds what this work may touch. It changes no gate: no arm of `chain_check.py`, no subcommand of `round_record.py`, no hook, no workflow. What it owes instead is §15 — the pin cases seen red with their sentence stashed |
| `skills/agent-contract/SKILL.md` §15 | A new case is not planted until it has been seen red. Every row added to `tests/test_the_rules_have_one_owner.py` is shown failing with the sentence it pins removed, and the handover says how |

## Scope

### In

1. **The cap sentence, where the cap is written.** `docs/review-chain-spec.md`
   says that the cap bounds ROUNDS, that a run stopped by it may still write a
   fix, and what decides which of the two a finding gets: **who owns the unit
   now**, not *when did the defect start*. The `New units` rows of the work
   item's own records are named as where that evidence already sits. The
   substitution the measured run made — measuring when the defect started — is
   named as the wrong question rather than left for the next reader to avoid.

2. **The two exits, named apart.** The round cap (three, five while a 🔴 is
   open) and the reopening bound (one reopening after a floor `no`) both end a
   run `capped`, and they permit different things. A run stopped by the round
   cap may write fixes for findings the branch owns; the reopening bound's
   terminal record may not, because `chain_check.py` refuses a second
   fix-closing record after the floor.

3. **What `Fixes checked by` reads at the cap.** The sentence that says it
   reads `no fixes to check` is true of a record that wrote no fixes and false
   of one that did. A capped record that wrote fixes reads `round-N` and is not
   the last record: `round_record.py seal` refuses to write `Broad gate` on a
   last record whose cell says anything else, so the fixes' one reader — a
   verifying round at their diff, commissioning nothing — is required by the
   generator and not only by this document.

4. **The filing ladder (#493).** An open finding takes the first home that
   fits, and a new issue is no longer the default:
   fixed on the branch → a comment on the open issue that already owns the
   ground → a new issue, only where the finding can name a party who will act
   → the round record alone, with the finding named in the pull request body.
   The test is the one `seal/follow-up.md` already applies to itself, read off
   the `Who answers it` column the reviewer's own `## Deferred` table already
   carries.

5. **The carriers.** Every place in the tree that repeats the sentences above
   becomes a link naming the owner, in the shape
   `tests/test_the_rules_have_one_owner.py` already holds: one carrier states
   the rule, every other names it. The known carriers are
   `skills/code-review/orchestration.md`, `agents/warden.md`,
   `agents/smith.md`, `agents/sealer.md`, `templates/sdd-round.md`,
   `docs/review-handoff-protocol.md` and `docs/issues-and-milestones.md`, and
   the comment in `skills/code-review/scripts/chain_check.py` that restates the
   exit.

6. **`docs/issues-and-milestones.md` learns the `from-review` label.** It is
   carried by 89 issues and named in no document in the tree. #493's whole
   measurement is taken through it, and a measurement whose key is undocumented
   is not repeatable.

7. **Both rules pinned.** New rows in `tests/test_the_rules_have_one_owner.py`,
   one owner and its links each, every assertion seen red.

8. **The fragments.** `seal/specs/<work-item-id>/changelog.md` and, where a
   claim is verified against a coordinate, `seal/ledger/<work-item-id>.md`.
   Never the shared files.

### Out

- **The lookup.** Deriving *does this branch own the unit* from `New units`
  automatically is mechanism on the chain gate, it carries
  `CONTRIBUTING.md` §*What a change to a gate must carry*, and #492 scopes it
  out by name. It stays against #330.
- **Any change to what a checker accepts or refuses.** No arm of
  `chain_check.py`, no subcommand of `round_record.py`, no hook, no workflow.
  A comment or docstring inside those files may be corrected to stop restating
  a sentence that moved; nothing they compute changes.
- **A new parsed field, a new verdict word, a new round-record row.** The
  moratorium above, and the ladder is spelled in vocabulary that already
  exists: `deferred <home>`, where the home is an issue, a file, or this
  record.
- **Raising the cap, and removing the deferral.** #492 refuses both by name.
  The cap stopped a loop at six rounds and that is it working.
- **Rule 1 of #493's two** — a fix pass may not add mechanism. #493 says
  plainly that it does not touch it, and this work does not either.
- **`seal/follow-up.md` as a home for a review finding.** Its own rule
  requires a named person, which is the same test the ladder applies before
  an issue is opened; it is not a cheaper home, and this work does not make
  it one.
- **Retitling, reopening or closing any existing issue**, #491 included.
- **Both README editions.** Neither describes the cap or the filing decision;
  if a phase finds otherwise, the house rule is that they move together.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 the cap bounds rounds | Given a reader opens the section that owns the cap · When they ask whether a capped run may write a fix · Then the document answers yes, and says the ownership test decides which findings get one | Read `docs/review-chain-spec.md` §*The review run has a bound, and an end*; `grep -n "bounds rounds"` names that file |
| A2 the question is *who owns the unit now* | Given the same section · Then it states the ownership test in those words, names `New units` as where the evidence sits, and names *when did the defect start* as the substitution that was made | Read; the phrase appears once, in the owner |
| A3 the two exits are apart | Given any sentence in the branch about a run ending `capped` · Then it says which bound ended it, and no sentence claims a capped record's `Fixes checked by` reads `no fixes to check` unconditionally | `grep -rn "no fixes to check" docs skills agents templates` and read each hit |
| A4 the capped run's fixes have a reader | Given a run stopped by the round cap that wrote fixes · Then the documents say those fixes owe one verifying round at their diff, that it commissions nothing, and that the record carrying them reads `round-N` while the last record reads `no fixes to check` | Read against `agents/sealer.md` §*The one write* and `round_record.py seal`'s three refusals; the shape is the one `seal/specs/1790039346-…/rounds/round-6.md` and `round-7.md` already carry and CI passed |
| A5 the reopening bound is not widened | Given the reopening bound's terminal record · Then the documents say it commissions nothing, with `chain_check.py`'s refusal of a second fix-closing record as the reason | Read; cross-check against `run_reopened`/`stopping_floor` in `skills/code-review/scripts/chain_check.py` — no code change, so the refusal is unchanged |
| A6 filing is no longer the default | Given a finding open at any exit · Then the documents give an ordered ladder, and a new issue is opened only where the finding names a party who will act and no open issue already owns the ground | Read `docs/review-chain-spec.md`; the leftovers table is the ladder |
| A7 the test is the one already on the page | Given the reviewer's `## Deferred` table · Then the rule reads the filing test off its `Who answers it` column, and no new column, row or field is added | `diff` of `templates/sdd-round.md` shows no new table column; `round_record.py`'s `DEFERRED_HEADER` is untouched |
| A8 the tracker document agrees | Given `docs/issues-and-milestones.md` · Then it carries a one-sentence link naming the owner of the filing rule, and documents `from-review` — what it marks and what it is counted for | Read; `grep -n "from-review" docs/issues-and-milestones.md` returns a hit where it returned none |
| A9 one owner, and links | Given the two new rules · Then `tests/test_the_rules_have_one_owner.py` pins each with one owner and every carrier naming it | `bin/test -q tests/test_the_rules_have_one_owner.py`, and each new assertion seen red with its sentence stashed |
| A10 nothing mechanical moved | Given the branch's diff · Then no line of `chain_check.py` or `round_record.py` outside a comment or docstring changed, and no hook or workflow changed | `git diff --stat` and a read of those two files' diffs |
| A11 the removed wording is answered | Given the survivor sweep on this branch · Then every place still carrying wording this branch removed is either corrected or recorded in `seal/specs/<work-item-id>/survivors.md` with grounds | `survivor-check` against the base, and its report read line by line |
| A12 the release rules hold | Given the loaded documents · Then none names the running version or anything above it, and the one-word rule holds | `bin/test -q tests/test_release_hygiene.py tests/test_one_word_one_meaning.py` |

## Data & interfaces

No schema, no endpoint, no payload. What this work touches that a machine
reads:

| Coordinate | What this work does to it |
|---|---|
| `skills/code-review/scripts/chain_check.py`, the comment above `DEFERRED` and the block near `CAPPED_EXIT` | Corrects prose that restates the exit sentence. No constant, pattern or branch changes |
| `skills/code-review/scripts/round_record.py`, `DEFERRED_HEADER` | Untouched. The filing test reads the column that is already there |
| `templates/sdd-round.md` `## Deferred` | Its `Who answers it` cell becomes the recorded evidence of the filing test. No new column |
| `tests/test_the_rules_have_one_owner.py`, `RULES` | Two new rows, owner and links, in the shape rules 10, 11 and 12 already take |
| `tests/test_the_rules_have_one_owner.py`, `AT_MOST_ONE_MORE_CEILING` and the `UNLESS` sweep | Constraints on the new prose rather than things to change: the phrase *at most one more round record* stays at one occurrence in the owner and one in each named carrier, and the four swept files may not state an exception as *Unless th…* |

The ledger rows this work can honestly write are claims about where a rule is
stated and which checker refuses what. They go in
`seal/ledger/1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys.md`,
never appended to `seal/ledger.md`.

## Open questions → questions.md

Three rows, one per kind. The run is `automation`, so no row blocks: each says
what the build does until somebody overturns it.

Framed 2026-09-22 by framer, before the build.
