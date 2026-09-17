# Round 1 — nothing reads a record against the tree

Round 1 of #344, #426 and #427 at `35796574`, on
`fix/344-426-427-nothing-reads-a-record-against-the-tree`, against
`release/v0.12.1` at `56945007`. Reviewed in a `git clone --no-local` at the
target SHA; nothing was written in the working checkout but this file.

## How the findings relate

The branch does what `spec.md` decided, and the decision holds against its own
grounds. What this round found is one gap in the new reader and two records
that state what nobody can re-derive.

```
① the new row is written and read       — built, and it works
      ↓ but the reader has one state its own model refuses
② `Fix range` can say `the fixes are not yet written` forever   🟡 1
      ↓ and the generator's side of the same row has no grandfathering
③ `close` refuses a record written before the row, with no repair in it   🟡 2
      ↓ and the document the branch ships states a count nobody can re-run
④ the corpus figures in `docs/review-chain-spec.md`   🟡 3
      ↓ the same class, in the records the branch corrected
⑤–⑨ corrections and small cleanups   ⬜
```

## Spec compliance — the first stage

`spec.md`'s decision is sound and the four grounds each hold at the coordinate
they name. **executed**: `evidence_check.py`'s own test module does state *No
fixture here runs git, and no fixture here may*, so the second option is
genuinely closed to a claim about commits;
`tests/test_a_record_states_what_the_tree_has.py` does carry
`test_a_location_column_is_not_an_unmigrated_coordinate`, so the first option
is refused where it would land. The build matches scope items 1 through 4.

Scope item 5 and the fragments landed. One divergence from `spec.md` §Out is
unrecorded — ⬜ 7 below.

Every acceptance row in `spec.md` has a case behind it. **executed**:
`bin/test tests/test_the_fixes_close_the_record.py
tests/test_chain_check_at_the_pull_request.py` — 228 passed, exit 0. I also
took one coverage probe of my own on #426 rather than trusting the report of
it: with `f.read()` mutated to `f.read(2000)`,
`tests/test_chain_hooks_hardening.py` exits 1; restored, exit 0.

`CONTRIBUTING.md` §*What a change to a gate must carry* is answered for all
four refusals in the pull request body, with a test, a direction and a budget
each. **read**.

---

## 🟡 1 — a `Fix range` still saying *the fixes are not yet written* is never named

`skills/code-review/scripts/chain_check.py`, `fix_range`, the `says_none`
early return (the `# A round that commissioned no fixes has no range` comment).

`build` writes the pending value into three rows at once — `Fix range`,
`Contract changes` and `New units` — and its own comment says why: *the same
pending value the two surface rows take, for the same reason*. Two of those
three rows are then read back for whether anybody replaced it. The third is
not.

`fix_surface` refuses a record whose `Contract changes` still says *the fixes
are not yet written* while `Fixes checked by` names a `round-N`, because a
later round opening those fixes proves they exist. `fix_range` returns on the
first `says_none` and asks nothing further.

**executed** — a planted record with `Fix range` and `Contract changes` both
reading `none — the fixes are not yet written` and `Fixes checked by | round-2`:

```
A fix_range   -> ([], [])
A fix_surface -> errors: ['`Contract changes` still says the fixes are not yet written,',
                          '`New units` still says the fixes are not yet written, and `F']
A full run exit: 1
A out names Fix range: False
A out names Contract changes: True
```

What it costs: the row that exists to state which commits a round's fixes were
measured over can say *there are none yet* on a record whose fixes shipped, and
the checker built to read that row against the tree is the one thing that will
never say so. That is the class the work item is named after, inside its own
new arm.

**The wider half, which the smith may answer with grounds.** A bare `none`
beside a `**fixed**` verdict passes the same way, and `closed_with_a_fix` is in
the same module and already called for the neighbouring row. **executed**: a
planted record with `Fix range | none` and a `**fixed** \`abc1234\`` verdict
gives `fix_range -> ([], [])` while `closed_with_a_fix` on the same lines
returns `True`. `docs/review-chain-spec.md`'s own table row states the
justification as *a round that commissioned no fixes has no range* — which is
the case the code does not distinguish. Closing this half would redden
`tests/test_the_last_rounds_fixes_are_checked.py`'s `record` fixture, which
pairs `verdict="fixed"` with `| Fix range | none |`, so it is a decision rather
than a typo. The paste-ready fix below closes the narrow half only.

## 🟡 2 — `close` refuses a record written before the row, and names no repair

`skills/code-review/scripts/round_record.py`, `close`, the
`raw[field_index(reader, lines, chain.FIX_RANGE)] = fix_range` line.

`chain_check` grandfathers the absent row behind `RANGE_FROM`, and every
document on the branch says so. The generator does not, and its refusal comes
from the shared `field_index` helper, whose message is written for a record
with two of a row rather than none of one.

**executed** — `close` against a record with no `| Fix range |` row, from a
work item begun long before the cutoff:

```
F exit: 2
F out: round-record: the record has 0 `| Fix range | … |` rows and needs one
F record still reads `open`: True
```

Nothing reaches disk, which is right. What is missing is the second half
`agent-contract` §14 and `spec.md`'s own acceptance row both ask for — the
message says what is wrong and not what to do, and the thing to do is one row
a person can paste.

What it costs: the changelog fragment states *Records written before this
release carry no such row and print rather than failing*, and the pull request
body repeats it. Both sentences are true of `chain_check` and false of `close`.
A work item whose round record was generated before this release and whose
fixes are closed after it meets an exit 2 that no document predicts.

**read** — the population is small. All 406 `round-*.md` files in the tree lack
the row, and every one of their work-item ids is below `RANGE_FROM`, so
`chain_check` excuses them all. The path is reachable only across the upgrade
itself. `field_index` behaving this way is also not new — `Contract changes`
arrived the same way — so the smith may reasonably answer that the precedent
stands and correct the two sentences instead.

## 🟡 3 — the shipped document states a corpus count nobody can re-run

`docs/review-chain-spec.md` §*The fix range — `Fix range`*, the paragraph
beginning *Measured over this repository on 2026-09-17*.

The sentence reads: **39 fix-table files, 15 stating a range in their first
eight lines, in 8 different spellings, and 5 of the 15 naming `HEAD`.** It
carries a date and no command, and it is the grounds on which the document
refuses a prose parser.

**executed** — I measured the same corpus at both ends of the branch with a
first-principles reading (every `seal/specs/*/rounds/round-N-fixes.md`, first
eight lines, looking for a stated range):

| | fix-table files | stating a range | spellings | naming `HEAD` |
|---|---|---|---|---|
| `release/v0.12.1` | 39 | 11 | 11 | 3 |
| `35796574` | 39 | 11 | 11 | 3 |
| the document says | 39 | 15 | 8 | 5 |

I cannot tell whether my reading or the builder's is the wrong one, and that
is the finding. The document records no command, so there is nothing to run
against it. One thing my run does show: at the branch tip,
`seal/specs/1789034970-…/rounds/round-2-fixes.md` still matches a crude search
for `HEAD` in its first eight lines, because phase 5 put the word inside the
explanatory comment it added — so a grep-shaped method counts a file the branch
corrected.

What it costs: this is the work item's own R7 turned on its own output — *a
measurement is reproducible only against a named range AND a named version of
the thing that measured it*. `spec.md` and `plan.md` were deliberately left
carrying the frame's figures, on the grounds that the measured ones are what
shipped into the documents. The measured ones shipped without the instrument.

## ⬜ 4 — two comment blocks stacked, and the first describes the second call

`skills/code-review/scripts/chain_check.py`, `main`, the two `# EVERY record
too` blocks above `fix_range`.

The `doubled_grounds` comment — *it has no cutoff — the function's own
docstring holds why* — sits directly above `range_errors, range_notices =
fix_range(...)`, and the `fix_range` comment follows it. `doubled_grounds`'s
own call has no comment above it at all.

Read in place, the file says the arm below has no cutoff. `fix_range` has one,
`RANGE_FROM`, and which of the two arms is grandfathered is the single most
load-bearing fact about either. A reader checking that property from the call
site gets it backwards.

## ⬜ 5 — the new template row is the one field row with no closing pipe

`templates/sdd-round.md`, the `| Fix range |` row.

**executed** — the last two characters of every field row in that table:

```
Target SHA ' |' · Written late ' |' · Ran by ' |' · PR ' |' · Broad gate ' |' ·
Fixes checked by ' |' · Fix range 'g>' · Contract changes ' |' ·
New units ' |' · Needs a fix ' |' · Loses a record or crashes ' |'
```

Nothing breaks: `split_row` tolerates the missing pipe and returns two cells,
and `test_the_field_rows_are_the_templates_in_the_templates_order` reads the
row. The template is a form sessions copy from, so the shape it ships is the
shape that propagates.

## ⬜ 6 — a pinned command beside a number it does not produce

`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/survivors.md`,
the line under `## Over the whole branch — what CI reads`.

The line now reads `` survivor-check --range d35c874...ce0f9fe `` **reports
sixteen places**. The comment beside it says, correctly, that the pinned range
gives three under the checker as it stood and two under today's, and that the
sixteen was an accumulation across the branch's life.

Before the correction the command did not resolve, so nobody could contradict
the sentence. After it, the command resolves and returns two. The prose is now
a reproducible claim that is false, with the truth in a comment under it — a
stricter reading of the same defect than the one the branch is closing. The
repair is to state the number the pinned range produces in the prose and to
leave the sixteen where the comment already explains it.

`rounds/round-2-fixes.md` has a milder version of the same shape: the end was
pinned to `371347c7` because that reproduces the *four* the line already
claimed, while `rounds/round-3.md:19` records `de7d693..ce0f9fe`, five commits,
as the range round 3 was given. The comment names both, which is why this is
noted rather than opened.

## ⬜ 7 — the build re-stamped the shared ledger, and no divergence row says so

`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/spec.md` §Out,
row *Re-anchoring or re-stamping anything in `seal/ledger.md`*; and
`seal/specs/1789621028-…/overview.md` §*Where spec and implementation
diverged*.

**executed** — 22 rows of `seal/ledger.md` changed, and every one of them
changed exactly two things: the anchor hash and the `Checked` date's last
digit. That is a re-verification, and it was required — the branch changed
content under those anchors, so `bin/evidence-check --strict` would otherwise
report them drifted.

The act is right and `CLAUDE.md` sanctions it. What is missing is the row:
`spec.md` listed it as out of scope on the grounds *Nothing here removes code
an existing row cites*, the build did it anyway, and the divergence table that
exists for exactly this omits it. `overview.md`'s `evidence:` line mentions the
22 rows in passing, which is disclosure but not the record the table is for.

## ⬜ 8 — one half of a guard the neighbouring module writes in full

`skills/code-review/scripts/round_record.py`, `close`, `spanned =
int(counted.strip())`.

`chain_check.fix_range` guards the same call as `counted is None or not
counted.strip().isdigit()`. `close` checks only `counted is None`, so a
`rev-list` that exits 0 with output `int()` cannot read raises a traceback
where every other failure on this path is a clean exit 2. Defensive only —
`git rev-list --count` returns a number or fails — but the two readings of one
command sit forty lines apart and disagree.

## ⬜ 9 — the new arm adds three git subprocesses per record, uncached

`skills/code-review/scripts/chain_check.py`, `fix_range`, the `resolves_to`
pair and the `rev-list` below them; `resolves_to` at its definition.

**read** — `resolves_to` shells out on every call and is not memoized. A record
carrying a real range costs two `rev-parse` calls and one `rev-list`. The cost
is zero today because no record in the tree carries the row, and it grows with
the corpus once they do: at the present 229 records that is roughly 690 git
invocations added to every pull-request run. Caching `resolves_to` by
`(root, sha)` would cost four lines and the arm's ends repeat heavily inside a
work item.

## ⬜ 10 — the class survives in two records the branch's scope excludes

`seal/specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it/rounds/round-1-fixes.md`
and `rounds/round-2-fixes.md`.

**executed** — both still state a moving range at the branch tip:
`` over the range `c4e9c58b..HEAD` `` and `` over the range `5137e934..HEAD` ``.
`spec.md` §Out excludes *Records of any work item other than 1789034970's*, so
this is scope honoured rather than scope missed. It is recorded because neither
`chain_check` nor anything else will ever name them — their work-item id is
below `RANGE_FROM` and the rule reads records, not fixes files — and the
changelog's *5 of the 15 naming `HEAD`* is the only place a reader learns that
any survive.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `Fix range` still saying *the fixes are not yet written* is never named, where `fix_surface` refuses exactly that state for its own two rows | `skills/code-review/scripts/chain_check.py` · `fix_range`, the `says_none` early return | open | Executed: a planted record with `Fixes checked by \| round-2` gives `fix_range -> ([], [])` while `fix_surface` errors on both its rows and the full run exits 1 naming `Contract changes` and never `Fix range` |
| 🟡 2 | `close` refuses a record written before the row exists, at exit 2, with a message naming no repair — while the changelog and the pull request body both say such records print rather than fail | `skills/code-review/scripts/round_record.py` · `close`, the `field_index(reader, lines, chain.FIX_RANGE)` write | open | Executed: exit 2, `the record has 0 \| Fix range \| … \| rows and needs one`, record unchanged. `chain_check`'s `RANGE_FROM` covers the same state; the generator has no equivalent |
| 🟡 3 | The shipped specification states a corpus count with a date and no command, and I could not reproduce it | `docs/review-chain-spec.md` · §*The fix range — `Fix range`*, the *Measured over this repository* paragraph | open | Executed at both ends of the branch: 39 files, 11 stating a range, 11 spellings, 3 naming `HEAD`, against the document's 39 / 15 / 8 / 5. The work item's own R7 is the rule this breaks |
| ⬜ 4 | Two `# EVERY record too` comment blocks are stacked, so `doubled_grounds`'s *it has no cutoff* sits above the `fix_range` call, which has one | `skills/code-review/scripts/chain_check.py` · `main`, above `range_errors, range_notices = fix_range(...)` | open | Read. `doubled_grounds`'s own call carries no comment; which arm is grandfathered is the load-bearing fact about either |
| ⬜ 5 | The new template row is the only field row in the table with no closing `\|` | `templates/sdd-round.md` · the `\| Fix range \|` row | open | Executed: every other field row ends ` \|`, this one ends `g>`. `split_row` tolerates it, so nothing breaks; a template is a form sessions copy |
| ⬜ 6 | A now-reproducible command is quoted beside a number it does not produce | `seal/specs/1789034970-…/survivors.md` · the line under `## Over the whole branch — what CI reads` | open | Executed by the branch itself and recorded in its own comment: the pinned range gives 2 today and 3 under the old checker; the prose still says sixteen |
| ⬜ 7 | The build re-stamped 22 rows of `seal/ledger.md`, which `spec.md` §Out excluded, and the divergence table has no row for it | `seal/specs/1789621028-…/overview.md` · §*Where spec and implementation diverged* | open | Executed: 22 rows changed, each in exactly the anchor hash and the `Checked` date. The act was required; the record of it is the omission |
| ⬜ 8 | `close` guards `rev-list --count` with `is None` alone where `chain_check` also checks `isdigit()` forty lines away | `skills/code-review/scripts/round_record.py` · `close`, `spanned = int(counted.strip())` | open | Read. Defensive only, and the two readings of one command disagree |
| ⬜ 9 | The new arm adds two `rev-parse` calls and one `rev-list` per record, and `resolves_to` is not memoized | `skills/code-review/scripts/chain_check.py` · `fix_range` and `resolves_to` | open | Read. Zero cost today because no record carries the row; roughly 690 git invocations per pull-request run once they do |
| ⬜ 10 | Two fix tables still state `..HEAD` at the branch tip, and nothing will ever name them | `seal/specs/1789598366-…/rounds/round-1-fixes.md` and `round-2-fixes.md` | open | Executed. Scope honoured, not missed — `spec.md` §Out excludes other work items' records. Recorded so the survival is not invisible |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone | 228 passed, exit 0 |
| `tests/test_chain_hooks_hardening.py` with `f.read()` mutated to `f.read(2000)`, then restored | exit 1 mutated, exit 0 restored — #426's new guard reddens under the mutation it pins |
| probe A — a planted record with `Fix range` and `Contract changes` both pending and `Fixes checked by \| round-2` | `fix_range -> ([], [])`; `fix_surface` errors on both its rows; full run exit 1 naming `Contract changes`, not `Fix range` |
| probe B — `Fix range \| none` beside a `**fixed**` verdict | `fix_range -> ([], [])`; `closed_with_a_fix` on the same lines returns `True` |
| probe D — the template's field rows | `Fix range` is the only row ending `g>`; every other ends ` \|`. `split_row` returns 2 cells for it |
| probe E — whether git resolves an uppercase abbreviated SHA | it does, and `resolves_to` returns the full lowercase commit. The uppercase branch of `FIX_RANGE_RE` is therefore harmless and is not a finding |
| probe F — `close --range <a>..<b>` against a record with no `\| Fix range \|` row | exit 2, `the record has 0 \| Fix range \| … \| rows and needs one`, record unchanged |
| A first-principles count of `seal/specs/*/rounds/round-N-fixes.md` at `release/v0.12.1` and at `35796574` | 39 / 11 / 11 / 3 at both, against the document's 39 / 15 / 8 / 5 |
| A count of `round-*.md` files carrying `\| Fix range \|` | 0 of 406, every work-item id below `RANGE_FROM` |
| `uvx ruff check` on the five changed Python files | All checks passed, exit 0 |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer, and this round ran none of them. They come due once nothing is open |

All probe files were deleted from the clone before this report was written, and
the clone is the only tree they existed in.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |

## Paste-ready fixes

🟡 1 — `skills/code-review/scripts/chain_check.py`, in `fix_range`. Keep the
`lines` the record was already split into, and ask the pending value the
question `fix_surface` asks of its own two rows:

```python
    text = read_record(root, rel)
    if text is None:
        return [], []
    lines = reader.readable(text)
    rows = table_rows(reader, lines)
```

```python
    if says_none(value):
        # A round that commissioned no fixes has no range, and `none` is the
        # honest value -- the one `new` writes before the fixes exist. What it
        # stops being honest about is a record a LATER round has already
        # opened the fixes of: they exist, so `not yet written` is false, and
        # this is the arm `fix_surface` runs on its own two rows for the
        # identical reason. The three rows take the same pending value from
        # `build` in one line; two of them were read back for whether anybody
        # replaced it and this one was not.
        checker = (
            reader.visible(field(rows, CHECKED_BY) or "")
            .strip()
            .strip("`")
            .strip()
            .rstrip(".")
            .lower()
        )
        if CHECKER_RE.match(checker) and says_not_yet(value):
            return [
                (
                    rel,
                    0,
                    f"`{FIX_RANGE}` still says the fixes are not yet written, "
                    f"and `{CHECKED_BY}` names `{checker}` above it — so a "
                    "later round opened those fixes and they do exist. The "
                    "cell contradicts its own file. It is the starting value "
                    "every record carries, because a record is committed "
                    "BEFORE its fixes; what is missing is the reach-back that "
                    "fills it when they land. Write "
                    "`` `<a>..<b>`, N commits ``, or let `round-record close` "
                    f"write it — or a bare `{NONE_WORD}` if this round "
                    "commissioned no fixes after all",
                )
            ], []
        return [], []
```

🟡 2 — `skills/code-review/scripts/round_record.py`, in `close`. Replace the
bare `field_index` call for the new row with one that says what to paste:

```python
    try:
        at_range = field_index(reader, lines, chain.FIX_RANGE)
    except Refused:
        raise Refused(
            f"the record has no `| {chain.FIX_RANGE} | … |` row, so there is "
            f"nowhere to write the range this pass was measured over. It was "
            f"written by a `new` from before that row existed — `close` "
            f"replaces the row rather than inserting one, because a record's "
            f"field order is the template's. Add `| {chain.FIX_RANGE} | "
            f"{chain.NONE_WORD} |` under `| {chain.CHECKED_BY} | … |` and run "
            f"`close` again. No cell was written"
        ) from None
```

```python
    raw[at_range] = fix_range
```

🟡 3 — `docs/review-chain-spec.md` §*The fix range — `Fix range`*. Name the
instrument beside the figures, and state what a re-run needs. Fill the
backticked command with what the build actually ran; the reviewer's own
first-principles count gives 39 / 11 / 11 / 3 and the two readings have to be
reconciled before either number ships:

```markdown
prose to enforce, which is why the authoritative statement moves into the
record instead of a parser being pointed at the prose. The figures are
reproducible only against both the tree and the instrument (`seal/ledger/
1789621028-nothing-reads-a-record-against-the-tree.md` R7): measured at
`35796574` by `<the command>`. A different reading of *stating a range in
their first eight lines* gives a different count, and this sentence is what
lets the next reader tell the two apart.
```

Needs a fix: yes — 🟡 1, the pending `Fix range` no arm ever reads back; and
🟡 2 and 🟡 3, either of which the smith may close with grounds instead

Loses a record or crashes: no

## Proof block

Files opened: `skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/orchestration.md`, `skills/verify/scripts/unverified_check.py`,
`docs/review-chain-spec.md`, `templates/sdd-round.md`, `CLAUDE.md`,
`seal/config.md`, `seal/ledger.md`, `bin/test`,
`seal/specs/1789621028-…/{spec,plan,questions,routing,overview,changelog}.md`,
`seal/ledger/1789621028-…md`,
`seal/specs/1789034970-…/{survivors,overview}.md` and its
`rounds/{round-2,round-2-fixes}.md`,
`seal/specs/1789598366-…/rounds/{round-1-fixes,round-2-fixes}.md`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_chain_hooks_hardening.py`, `tests/test_the_record_is_generated.py`,
`tests/test_the_fixes_name_their_surface.py`,
`tests/test_the_run_stops_at_the_last_finding.py`,
`~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all inside a `git clone --no-local`
at `35796574`, exit codes read from `$?` or from `returncode` and never through
a pipe. Both probe modules were deleted before this report was written.
