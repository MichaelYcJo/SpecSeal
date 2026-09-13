# Implementation Plan: the record-before-the-fix sequence has no arm (#345)

<!-- seal/specs/1789296200-the-record-before-the-fix-sequence-has-no-arm/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

`round_record.py new` is the last command the orchestrator runs before it
dispatches a fix pass. It knows the commit the reviewer read and it can ask git
for the branch's HEAD, and today it compares the two for nothing. Where they
differ, the fix pass has already run — or HEAD moved mid-review, which the
record template already asks to be written down — and `new` is the only place
in the sequence where either can be said while anybody can still act.

So `new` gains that one observation and one escape carrying a written reason,
and `chain_check.written_late` gains one pass state for a record that carries
it. That last half is what gives the refusal the honest repair it has never
had: work item 1789034970 (#120) ended with a pull request red on a line no
later commit could clear, and three bad exits — rewrite history, merge red, or
invent an undocumented waiver.

## Technical context

**What exists.**

- `skills/code-review/scripts/round_record.py:1666` `build` — resolves
  `--target` (`reader.resolves(root, args.target)`) and compares it to
  nothing. `round_record.py:848` `git(root, *args)` is the helper a
  `rev-parse` would use.
- `skills/code-review/scripts/round_record.py:1951` `new` — writes the record,
  prints the reach-back and the bound line, then returns
  `run_check(root, baseline)`, which is `chain_check.main --worktree` over the
  whole work item.
- `skills/code-review/scripts/chain_check.py:2415` `written_late` — and
  `chain_check.py:2326` `added_on_branch`, which returns `None` for a file git
  does not carry as added in `<base>..HEAD`. That `None` is why `written_late`
  is already silent at `new` and why nothing needs moving.
- `skills/code-review/scripts/chain_check.py:2766` `close` (in
  `round_record.py`) rewrites verdict cells, `Contract changes`, `New units`
  and `Broad gate`. Whether it preserves an unrecognised field row is phase
  3's question and is what acceptance A7 pins.
- `templates/sdd-round.md`'s field block already spells `Target SHA` as
  *the commit this round actually reviewed — both, if HEAD moved mid-review*,
  and `chain_check.check_round` already reads that cell with
  `SHA_RE.findall`. The mid-review case is house convention already; it has no
  arm either.
- `docs/review-chain-spec.md` §*When the record was written — before the fixes
  it commissioned* — an eight-row states table, all eight of which stay true.
- `tests/test_a_record_precedes_the_fixes_it_commissions.py`, 1,131 lines,
  already carries both kinds of case this needs: git-fixture cases over a
  three-commit repository, and spec-pinning cases of the shape
  `test_the_spec_carries_the_subsection`.

**Constraints.**

- `agent-contract` §15 — every case red before it is planted. Each phase says
  how below, and the two mechanisms are *revert the arm* and *delete the
  sentence the case pins*.
- `agent-contract` §8 — the fixtures commit, so git is driven from Python
  through `subprocess.run(["git", "-C", d, ...])`. The existing module already
  does this; follow it rather than inventing a second way.
- `CLAUDE.md` — the changelog entry goes to this directory's `changelog.md`,
  the ledger rows to `seal/ledger/1789296200-…md`. Neither shared file is
  appended to.
- `tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py`
  — `spec.md`'s naming section says which two words are spent; fixtures use
  `example.com` and `/Users/x/`.

**The failure scenario of the chosen approach, in six months.** The escape
becomes the habit. Every round's `new` refuses because something innocuous
committed during the review, the orchestrator learns the flag, and a genuinely
late record arrives carrying a reason nobody read. That is why phase 1 is a
measurement and not a build: if HEAD routinely differs from the target in this
repository's own correct runs, the refusal is wrong on arrival and the shape
has to be a printed line instead. The criterion is written into phase 1 before
the number is taken.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Move `written_late` to `new`** — #345's literal proposal | Its two inputs do not exist at `new`: the record has no adding commit and its verdict cells read `open`. The moved check returns `([], [])` on every call and ships a gate that can never fire — `skills/verify/SKILL.md`'s counterfeit seal | **rejected.** This is the finding `spec.md` opens with |
| **Run `written_late` at `close`** | `close` is the first moment both inputs exist, and it runs after the fix pass. It detects earlier and prevents nothing; worse, a refusal there blocks the record's own update, so the round is left with `open` cells and a run with no way forward — a gate with no exit, one command further on | **rejected.** Detection without a repair is what the pull request already provides |
| **`new` commits the record and its report** | #330's strongest evidence favours performing the act. But `new` returns `run_check`'s exit code, which is legitimately non-zero mid-run, so `new` either commits a record the check just refused or declines and is a sentence again. And a generator that commits takes `git` decisions away from the orchestrator in a repository whose commit gate is an opt-in hook | **deferred to an issue.** The reasoning is written down so the next reader does not re-derive it |
| **Print a line, refuse nothing** | The orchestrator already reads `run_check`'s output at `new`, and in #120's round 3 it did exactly that and acted on none of it. A line in a stream that already carries the reach-back, the bound and a full chain-check run is a line that gets scrolled past | **held as phase 1's fallback.** Adopted only if the measurement says a refusal would be wrong on arrival |
| **Do nothing; leave it at the pull request** | #120's outcome, exactly: a red line no commit can clear, three bad exits, and a run capped at round 3 with the reverted fixes redistributed across #339–#345 | **rejected.** It is the measured status quo |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The measurement that sets phase 2's verdict.** Over every `rounds/round-N.md` under `seal/specs/`, compare the record's `Target SHA` against its adding commit's first parent, and count how often they differ in runs nobody has called wrong. Criterion, written before the number: **0 or 1 differing record → phase 2 refuses; 2 or more → phase 2 prints and continues.** Write the number and the verdict into `overview.md` | The count itself, and the list of differing records named individually so a reader can open each. `agent-contract` §4 — this is `executed`, and nothing is built on it until it is | `a71e879` — **40 of 152 differ; phase 2 prints** |
| 2 | **`new` observes whether `--target` is HEAD**, and says so in phase 1's verdict. The message names the commits between, both meanings (the fix pass already ran · HEAD moved mid-review), and the escape. `--target` still resolves as today; the ordinary equal case prints nothing new | A2 and A1 in a new case module. Red first by making the observation fire unconditionally (A1 goes red) and by reverting the observation entirely (A2 goes red) | `394a49f` — **prints**, per phase 1 |
| 3 | **The escape and the trace it writes.** One flag carrying a reason; an empty reason refused, the shape `nobody — <why>` already takes. The reason reaches the record, in the home Q3 settles, and `close` does not lose it | A3, A4 and A7. Red first: A3 by having the escape write nothing, A4 by dropping the emptiness test, A7 by having `close` rewrite the field block wholesale | |
| 4 | **`chain_check.written_late` reads the reason and prints instead of failing.** One early return, one new row in the states table. A record without the reason is judged exactly as today | A5 and A6 in `tests/test_a_record_precedes_the_fixes_it_commissions.py`. Red first: A5 by having `written_late` ignore the cell; A6 is the existing `test_a_record_added_after_its_own_fix_fails_after_the_cutoff`, which must stay green untouched. Then `bin/test tests/test_a_record_precedes_the_fixes_it_commissions.py` whole, because this phase edits a module with 39 existing cases | |
| 5 | **The documentation and the pins** — `docs/review-chain-spec.md`'s states table, `skills/code-review/orchestration.md` §*And commit the record before commissioning the fixes*, `templates/sdd-round.md`. Plus `changelog.md` and the ledger fragment, both in this directory's own files | A8, as cases of the shape `test_the_spec_carries_the_subsection` already in the module. Red first by deleting the sentence each pins. `agent-contract` §14 is satisfied by this phase riding the same commit as phase 4, not a later one | |

Phases 4 and 5 land in one commit. §14 says a fix that changes what a person
sees documents it and pins it **in the same commit**, and the person-visible
change is phase 4's new verdict.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

## Operational impact

- **A gate's verdict changes**, so `CONTRIBUTING.md` §*What a change to a gate
  must carry* is owed in the pull request body. The two halves to answer: what
  the new refusal costs a correct run (phase 1's number is the evidence), and
  what the new pass state lets through (a late record whose author wrote down
  why, which today ships as a red line or a silent one).
- **No new dependency, no migration, no config row.** No `ORDER_FROM`-style
  cutoff either, and `spec.md` says why for both directions.
- **One behaviour a deployer should know:** after phase 4, a pull request that
  is red today on a late record can be made green by writing a reason into the
  record. That is the intended fourth exit and it is a relaxation — Q2 is the
  owner's row that authorises it.
