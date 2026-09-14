# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 1

| Field | Value |
|---|---|
| Target SHA | `7f47eed` |
| Base | `release/v0.11.4` at `34b556a` |
| Diff | `git diff 34b556a...7f47eed` — 20 files, 1204 insertions, 9 deletions |
| Reviewed in | a `git clone --no-local` at `7f47eed` |
| Earlier rounds | none |

## What the change does, checked rather than accepted

The shipped `BLOCK_START` in `skills/code-review/scripts/round_record.py` is
the pattern `.github/scripts/issue_claims_check.py` already carries, plus the
two fence openers, and nothing else. I checked that by loading all three
modules and printing their patterns side by side rather than reading them:
removing the literal fence alternative from this module's spelling leaves the
model's spelling character for character.

The direction claim holds too, and I ran it rather than taking it. With the
constant mutated back to its spelling at `5e09345`, the record module shows
**exactly seven** failures, and they are exactly the seven the ledger fragment
names — the two `#N` continuations and all five members of `STOPS_THE_JOIN`.
Every other new arm is green against that constant and is labelled in
`CONTINUES_THE_LINE` with what it was seen red against instead. The `boundary`
label, which says *no candidate pattern ever cut this*, is the honest form of
§15 rather than an implied demonstration, and I confirmed both `boundary` arms
join under all three patterns.

`BLOCK_START` has one call site, `terminal_value`, and `survivor_check.py`'s
`BLOCK` has one. Narrowing either reaches nothing else in its module.

The scope fence holds. `seal/ledger.md` is untouched by the branch;
`templates/sdd-round.md`'s `Needs a fix` row is still at line 43 unedited and
the branch's only change to that file is an addition below line 180;
`round_record.py`'s diff has two hunks and neither is near `fix_table` or the
two `close` defects.

The `spec.md:252` edit is what it says it is. The builder replaced an
abbreviated anchor with the full row text, and the verdict cell beside it —
`**Unchanged.** The row is not edited; the prose below it is.` — is byte
identical before and after. The unfolded spelling matches `seal/ledger.md:89`'s
own spelling of the same row, and the hash `@9a509e35` is unchanged. **The
claim really is unchanged.** Editing a framer-written file to keep
`evidence-check` from exiting 2 was the right call and it is recorded in three
places.

## 🟡 1 — the pin that was supposed to replace the shared constant was never planted

`skills/code-review/scripts/round_record.py:1252-1258`

`plan.md` §*Alternatives considered* rejects one shared pattern constant and
says what pays for the rejection: *the pin that replaces it is a case asserting
the two spellings accept and reject the same shapes, which goes red when either
drifts and costs no coupling*. `spec.md` §*Scope* repeats it. What shipped is a
prose comment at each constant naming the other two.

A comment does not go red. **Executed**: giving
`.github/scripts/issue_claims_check.py`'s pattern an alternative this module
lacks leaves both carriers' modules green — 167 passed, the record module and
the claims module together. The two spellings can drift apart in silence, which
is the state the rejection was argued against.

`overview.md` §*Not done* records the substitution as though the plan had asked
for it — *what replaces it is the sentence at each constant naming the other
two* — so the divergence does not appear in §*Where spec and implementation
diverged*, which is where a later reader looks for it.

## 🟡 2 — an executed count in the ledger fragment is one short of the tree

`seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md`, row 1

The row reads *Seven of the ten new cases were seen red against the constant at
`5e09345` before it was replaced; the module went 107 → 117 green*.

**Executed**: the record module is 107 at `34b556a` and **118** at `7f47eed`.
The branch adds eleven cases, not ten — six arms in `CONTINUES_THE_LINE` and
five in `STOPS_THE_JOIN`. The *seven* is right; I measured it.

The cause is visible in the history. The figure was measured at phase 1
(`1e91894`), and the sixth `CONTINUES_THE_LINE` arm — the `anchor` one — was
added after it. The ledger row was written at phase 5 and names that eleventh
arm in the same sentence that counts ten.

This is the row that folds into `seal/ledger.md` at the release, so the wrong
number is the one that outlives the branch. Two other current-state carriers
repeat it: `overview.md:21` and PR #392's verification table.
`phases/phase-1.md` asserts a past state and is correct as written — leave it.

## 🟡 3 — the prompt budget is not in the pull request body

PR #392, §*Operational impact*

`CONTRIBUTING.md` §*What a change to a gate must carry* is explicit about where
this one lives: *The prompt budget is the one of these four a passing suite
cannot report on, because nothing counts interruptions. It is answered in the
pull request body or it is not answered.*

`spec.md` §*The gate answer* answers it well — *zero added, and one path to
fewer* — but `spec.md` is a work-item file. The PR body carries the other three
burdens (the red run, the failure direction, and the narrowing argument for why
that direction is the cheaper mistake) and says nothing about how many times
this change puts a question in front of a person.

## 🟡 4 — the warden restates the owner's exception list, and nothing pins the two together

`agents/warden.md:409`

The prompt asks whether what landed is two rules or one rule in two places. **It
is two rules.** The protocol owns the conformance statement, which a second
implementation is built from; the warden owns the operative instruction a
reviewer acts on at minute forty. The split is falsifiable, and the third
assertion in the new case — that the warden does not enumerate the three stops —
is what keeps it from collapsing one sentence at a time. That is the right
shape.

The leak is not the rule, it is the exception list. `agents/warden.md:409`
spends a clause on *an indented line, an HTML tag and `**bold**` among the ones
it cannot*, and `docs/review-handoff-protocol.md:305` states the same three
shapes as the owner. `round_record.py:1243` and `:1296` state them twice more.
Four carriers, and no case compares any two of them — I grepped for one.

The consequence is the one this repository already paid for once. If the list
ever gains a fourth shape, the owner moves and the warden goes stale silently,
and a reviewer reads the stale copy.

## 🟡 5 — a whole-line alternative in the constant phase 4 retyped is pinned by nothing

`skills/code-review/scripts/survivor_check.py:384`

**Executed**: mutating `[-*_=]{3,}\s*$` to match nothing leaves the sibling
module 49 green. The build found this and disclosed it in `overview.md` §*Not
verified*, naming *the review chain* as who answers it. I am the review chain,
so this is the answer.

The grounds for deferring — *it predates this branch, and closing it means a
case for code this work did not change* — are true of the alternative's content
and not of the line. Phase 4 rewrote that constant whole. Retyping a pattern is
the cheapest moment to pin what it does, and the hole is in the same direction
the branch just closed one of: kill the alternative and a run of markers stops
ending a segment, so two unrelated claims merge across a horizontal rule and
score as one.

This is the finding most open to being answered with grounds rather than fixed.
The sibling was in scope on `skills/agent-contract/SKILL.md` §12, and §12 draws
scope on the class rather than the coordinate — which is an argument for taking
it, not against.

## ⬜ 6 — a `-` setext underline shorter than three characters is not covered by the claim that says it is

`skills/code-review/scripts/round_record.py:1247` ·
`docs/review-handoff-protocol.md:302`

Both say the setext underline comes back as a whole-line alternative. A setext
underline is any run of `=` or `-`, of any length. The `=` side is covered at
every length; the `-` side is covered only from three, because it rides on the
thematic-break alternative. **Executed**: `--` and a bare `-` join under all
three patterns.

No behaviour is wrong — the blank line is the real stop and the model module
makes the same trade deliberately, saying so in its own comment (*so `a --- b`,
`--` and `= x` are prose*). What is wrong is the sentence: this module's comment
and the protocol both state the coverage without the caveat the model states.
A correction, not a fix.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The case that was to replace the rejected shared constant does not exist; the two spellings can drift apart green | `skills/code-review/scripts/round_record.py:1252-1258` | open | `plan.md` §*Alternatives considered* and `spec.md` §*Scope* both name a case; executed — an alternative added to the model leaves both modules green, 167 passed |
| 2 | An **Executed** count in the ledger row is 117 where the tree is 118, over ten new cases where there are eleven | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 1 | open | Executed — 107 at `34b556a`, 118 at `7f47eed`; the row names the eleventh arm in the sentence that counts ten |
| 3 | The prompt budget is absent from the pull request body, which `CONTRIBUTING.md` names as the only place it is answered | PR #392 §*Operational impact* | open | `CONTRIBUTING.md` §*What a change to a gate must carry*: *It is answered in the pull request body or it is not answered* |
| 4 | The warden enumerates the owner's three-shape exception list; four carriers hold it and no case compares any two | `agents/warden.md:409` | open | Read — `docs/review-handoff-protocol.md:305`, `round_record.py:1243` and `:1296` carry the same list; grep finds no case pinning them together |
| 5 | `BLOCK`'s whole-line alternative is unpinned inside a constant phase 4 rewrote whole | `skills/code-review/scripts/survivor_check.py:384` | open | Executed — mutated to match nothing, the module stays 49 green; disclosed by the build and handed to this round |
| 6 | The claim that the setext underline comes back covers `=` at every length and `-` only from three | `skills/code-review/scripts/round_record.py:1247`, `docs/review-handoff-protocol.md:302` | open | Executed — `--` and `-` join under all three patterns; the model module states the caveat and these two do not |
| — | The narrowed pattern is the model's plus the two fence openers and nothing else | `skills/code-review/scripts/round_record.py#BLOCK_START` | answered | Executed — patterns printed side by side; removing the fence alternative leaves the model's spelling exactly |
| — | §15: the new cases were seen red | `tests/test_the_record_is_generated.py` | answered | Executed — the constant mutated to its `5e09345` spelling turns exactly seven arms red, and they are the seven the ledger names |
| — | `spec.md:252` — the framer's file edited, claim unchanged | `seal/specs/1789347354-…/spec.md:252` | answered | Executed — the verdict cell is byte identical, the anchor hash is unchanged, and the unfolded spelling matches `seal/ledger.md:89` |
| — | The scope fence — `fix_table`, the two `close` defects, `seal/ledger.md`, the template's `Needs a fix` row | `skills/code-review/scripts/round_record.py`, `templates/sdd-round.md` | answered | Read — two hunks in the script, neither near `fix_table`; `seal/ledger.md` absent from the diff; the template row unedited at line 43 |
| — | Q3 — is the split two rules or one rule twice | `agents/warden.md`, `docs/review-handoff-protocol.md` | answered | Two rules. Different audiences, and three assertions make the split falsifiable. The residue is finding 4 |
| — | The sibling is the same class | `skills/code-review/scripts/survivor_check.py#BLOCK` | answered | Executed — the old bare `[-*+>#]` split a line opening `#120`; the new spelling joins it, and the consequence differs as the build says |

## Executed probes

| What was run | Result |
|---|---|
| `python3 .github/scripts/run_tests.py tests/test_the_record_is_generated.py -q` at `7f47eed` | 118 passed, exit 0 |
| The same module with `skills/code-review/scripts/round_record.py` and the test module checked out at `34b556a` | 107 passed, exit 0 — the base count |
| The same module with `BLOCK_START` alone mutated to its `5e09345` spelling | 7 failed, 111 passed — the two `base` arms and all five of `STOPS_THE_JOIN` |
| `python3 .github/scripts/run_tests.py tests/test_a_corrected_sentence_survives_elsewhere.py tests/test_the_rules_have_one_owner.py -q` at `7f47eed` | 97 passed, exit 0 |
| The sibling module with `[-*_=]{3,}\s*$` mutated to match nothing | 49 passed, exit 0 — the alternative is pinned by nothing |
| The record module and `tests/test_a_body_naming_two_issues_claims_one.py` with an alternative added to the model's pattern and not to this module's | 167 passed, exit 0 — the two spellings can diverge green |
| The three patterns loaded and matched against 29 line shapes | This module's spelling is the model's plus the two fence openers, character for character |
| The broad gate — the full suite, repository-wide `ruff check`, and the typecheck | Not run by this round, and not yet run by anybody at this SHA. It is the sealer's single act, and this report leaves findings open, so it is not yet due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py#file_units` reads a `##` line inside a fenced block as a heading, so a ledger anchor on such a section stops at the fence. Three of thirty-six anchored markdown files affected; `seal/ledger.md` R7 under-covered by 81 lines | `overview.md` §*Not verified*, and it is a change to a gate | the repository owner — carried forward unchanged; this round did not reopen it |
| `#309`'s two `close` defects | `#391`, in the `release: 0.11.4` milestone | the third work item of this release. Verified out of this branch: `fix_table` was not opened |
| Whether `survivor-check` over this branch's own range reports anything | `overview.md` §*Not verified* | the review orchestrator at the first fix pass — there was no fix pass to run it over, and there is one now |

## Paste-ready fixes

Finding 1 — a case in `tests/test_the_record_is_generated.py`, beside the other
`BLOCK_START` cases:

```python
def test_the_two_spellings_differ_only_by_the_fence_openers():
    """`plan.md` §*Alternatives considered* rejected one shared constant.

    What it named in place of the coupling is a case asserting the two
    spellings accept and reject the same shapes. A comment at each constant
    cannot do that: an alternative added to one and not the other leaves
    both modules green. The two script roots ship on different paths and
    neither imports the other, so this is the pin that replaces the import.
    """
    model = _load(
        "issue_claims_check",
        os.path.join(ROOT, ".github", "scripts", "issue_claims_check.py"),
    )
    ours = generator_module().BLOCK_START.pattern
    theirs = model.BLOCK_START.pattern
    assert ours.replace(r"|```|~~~", "", 1) == theirs, (
        "the two spellings have drifted apart. They are kept alike on "
        "purpose and differ only by this module's two fence openers.\n"
        f"  this module: {ours}\n"
        f"  the model:   {theirs}"
    )
```

Finding 2 — the ledger row, `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md`:

```
Seven of the eleven new cases were seen red against the constant at
`5e09345` before it was replaced; the module went 107 → 118 green
```

`overview.md:21`, the third row of the divergence table:

```
| How many cases the record module holds | `plan.md` and `spec.md` both say 104 | 107 at the base, 118 after | Measured by running it. No consequence beyond the number |
```

PR #392's verification table, first row:

```
| The generator's own module | **executed** — 107 green before, 118 after |
```

Finding 3 — a paragraph for PR #392 §*Operational impact*:

```
**Prompt budget: zero added.** The generator puts no question in front of a
person — it refuses or it writes, and both go to a log. The one option that
would have added one was refusing the ambiguity instead of joining it, which
would stop a run whose report omitted a blank line at whatever minute the
record is generated, with nobody at the keyboard. It was put to the owner
before the first edit and declined, on this project's first goal.
```

Finding 4 — `agents/warden.md`, replacing the clause that enumerates the list:

```
**Either line may wrap, and a wrapped line is one value.**
`round_record.py new` joins it across the wrap, and the guard deciding where
that join stops does not reach every shape a continuation can begin with. So
**leave a blank line under the pair**, which markdown wants anyway and which
is the one stop nothing can read wrong. Where the join stops, and which
shapes it cannot reach, is stated once in
`docs/review-handoff-protocol.md` §*The Needs a fix field — the answer a run
ends on*; this line is the instruction, that section is the rule. The
generator used to keep the first physical line and drop the rest without
saying so, and a round record shipped ending mid-clause.
```

Finding 5 — a case in `tests/test_a_corrected_sentence_survives_elsewhere.py`,
beside the arms this branch planted:

```python
# The alternative that predates this branch and that phase 4 retyped without
# pinning. Mutated to match nothing, the whole module stayed green.
@pytest.mark.parametrize("rule", ["---", "___", "***", "==="])
def test_a_whole_line_of_one_marker_ends_the_segment(rule):
    """A thematic break and a setext underline are blocks in their own right.

    Without this alternative a claim above a horizontal rule and an
    unrelated claim below it land in one segment, which is the false
    positive `.github/scripts/issue_claims_check.py` spends its own
    whole-line alternatives to avoid."""
    reader = module()
    text = f"the claim above the rule.\n{rule}\nan unrelated claim below it."
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any("above the rule" in k and "below it" in k for k in keys), (
        f"{rule!r} is a block of its own and the segment ran straight "
        f"through it: {keys!r}"
    )
```

Finding 6 — `skills/code-review/scripts/round_record.py`, the sentence about
the run-of-three markers, and the matching sentence in
`docs/review-handoff-protocol.md`:

```
# requirement then takes the run-of-three markers out of the class, so a
# thematic break and a setext underline come back as whole-line alternatives
# of their own; `\r*$` on each is what makes a CRLF checkout read like an LF
# one. A `-` underline shorter than three characters is not among them and is
# joined, which is the model module's trade and stated in its comment.
```

Needs a fix: yes — findings 1, 2 and 3. The pin the plan named in place of the
shared constant does not exist, an **Executed** count in the ledger row that
folds into `seal/ledger.md` is one short of the tree, and the prompt budget is
absent from the only place `CONTRIBUTING.md` says it is answered.

Loses a record or crashes: no

Findings 4, 5 and 6 are open and none of them is that. Finding 5 is the one a
smith may reasonably answer with grounds rather than a case. Nothing in this
diff can lose a record or raise: the change makes one guard join more and
refuse less, `terminal_value`'s two refusal paths are untouched, and the five
shapes that now stop the join end a value early in a way that reads as wrong at
a glance rather than silently.

## Proof

Opened at `7f47eed`, in a `git clone --no-local` of the repository:

- `skills/code-review/scripts/round_record.py` — `BLOCK_START`, `terminal_value`, and every call site of the constant
- `skills/code-review/scripts/survivor_check.py` — `BLOCK` and its call site
- `.github/scripts/issue_claims_check.py:100-135` — the model pattern and its comment
- `agents/warden.md` — the diff and §*Report* as it now stands
- `docs/review-handoff-protocol.md` — the diff and the added section
- `templates/sdd-round.md` — the diff, and the `Needs a fix` row at line 43
- `tests/test_the_record_is_generated.py` — the diff, the module header and its loaders
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — the diff
- `tests/test_the_rules_have_one_owner.py` — the diff, rule 11 and the split case
- `seal/specs/1789347354-…/` — `spec.md`, `plan.md`, `questions.md`, `overview.md`, `routing.md`, `phases/phase-1.md`, `phases/phase-5.md`, `changelog.md`
- `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` — all five rows
- `seal/ledger.md:85-92` — the anchor the scope fence is drawn around
- `CONTRIBUTING.md:65-96` — §*What a change to a gate must carry*
- `bin/test` and `.github/scripts/run_tests.py` — the runner
- PR #392 — title and body

Carried from the orchestrator rather than re-run: `bin/evidence-check .` exit 0
at `7f47eed`, `ruff check` on the two changed scripts and three changed test
modules exit 0, and the five-module phase-boundary set at 269 passed / 8
skipped / exit 0. I ran three of those five modules myself and they agree.
