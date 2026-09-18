# Round 3 — the last round of a capped run, over round 2's fixes

Target SHA `631df127e44e4d4a337898a88f360e77b1e7bca4`, base `release/v0.12.1`,
draft pull request #445. Fix range `20eade5..5a1f47e`, seven commits.

Read and run in a `git clone --no-local` of the repository at the target SHA.
Nothing was written in the working tree except this report, and every probe
file, the scratch venv and the clone itself are gone.

Round 1's and round 2's coordinates were carried, not their verdicts. The
surface was the fix diff and the units it added, not the branch — round 2
already read the branch, and re-reading it is the cost this round exists to be
cheaper than.

## The headline

**Round 2's four findings are all closed, and each fix is correct at every
arm I could reach.** I ran the seven message shapes `missing_row` can print
and read each sentence against the file that produced it; none of them is
false about its own file. The `with_row` repair terminates exactly the one
line that needed terminating, and the `refusal` tail is now found by position
rather than by identity, on grounds that hold.

**One thing the fix pass handed me does not survive the look.**
`fence_left_open`'s new second parameter defaults to `None`, and with that
default the function answers the whole-file question that round 2's 🟡 2 just
removed from the refusal. Nothing calls it that way and no case touches it, so
nothing ships broken — but the old answer is now what a `None` returns instead
of what raises, and the shorter spelling is the one every caller used until
this commit.

**Two `New units` entries are declared at the wrong depth**, and the check that
should have said so cannot: `units_named_earlier` strips the underscores out
of every name it reads, which is already written down as a RIDER with the
repository owner as its answerer. The consequence here is nil — this round read
both units, which is what the depth rule exists to guarantee.

Nothing here loses a record and nothing raises.

## Stage 1 — spec compliance, and the surface the record named

Everything below is **executed** unless it says *read*.

### The contract change, and every call of it

`Contract changes` is not `none` for the first time in this run, so I took it
first. `fence_left_open` gained a parameter and `fenced_row_at` is new; the
row names `missing_row` as the only production reach of the first and `pytest`
as the only reach of `fenced_row`. I re-derived both rather than inherit them:
a grep of the whole tree finds `fence_left_open` called in exactly one place,
`skills/verify/scripts/broad_gate.py:686`, and `fenced_row` called in exactly
one place, `tests/test_the_seal_is_taken_once_by_the_sealer.py:1887`. The reach
row is right.

**The one production call is correct.** `missing_row` calls
`fence_left_open(home, at)` only inside `if fenced is not None:`, and
`fenced_row_at` returns `(None, None)` or a pair, so `at` is never `None`
there. I worked the fence arithmetic through every arrangement I could build:
a row inside an unclosed block, a row inside a block that closes with a second
block opened below it, a row inside a block that closes with the unclosed
opener above it — which `fence_map` makes unreachable, since an unclosed opener
swallows everything under it. In each one `opened_at < at` is the right test.
Executed over the fixture round 2 named: `fence_left_open(home, at)` is
`False` and the refusal says *Move the row into*, which is the act that person
needs.

### The two things the fix pass judged rather than measured

**1. `write_row`'s non-fence arm is genuinely defensive, and its message is
honest.** *Read.* I enumerated the ways the row can fail to read back after
`with_row` runs. The first arm replaces a row the reader already found, so the
row reads back. The second arm inserts into a span `table_span` derived from
the same walk `config_rows` uses. The third arm appends a table after the end
of the file, which lands inside a fence only when a fence is open — and that is
the branch above. The value is `local` or `shared` at both call sites
(`seal.py:1941` and `:2183`), so no cell can be malformed from the value side.
That leaves a defect in `with_row` itself, which is what the case drives by
replacing it. *would not read the `Mode` row back … This is a defect in this
command rather than in your file* is the true sentence for that state, and the
file is untouched when it prints.

**2. `fence_left_open(home)` with no second argument is a finding.** See
finding 1 below. Executed: over the file where the row sits in a block that
closes and a second block is opened and never closed below it, the default
returns `True` and the two-argument form returns `False`. The default is the
answer the refusal must never use.

### The depth claim

I checked it rather than read it. The rule, in `round_record.py`'s own words,
is that a unit is at depth 2 when a `fixed` finding whose `Location` sits
inside a unit an earlier record's `New units` names is the fix that added it,
in a file the range adds a unit to.

Round 2's finding 2 is `fixed`, its `Location` is
`skills/verify/scripts/broad_gate.py#fence_left_open`, round-1.md's `New units`
names `fence_left_open`, and that finding's commit `15d4f38` adds
`fenced_row_at` and one case to that file. **Both of those are at depth 2**,
and the record declares both at depth 1. The other four entries are at depth 1
and their declarations are right: `fence_map` and the no-ending case come from
finding 1, whose `Location` names `with_row` and `write_row`, and the other two
cases come from findings 3 and 4, whose `Location` names `missing_row` — none of
those three units appears in round-1.md's `New units`.

Why no cell was refused: I reproduced round 2's `close` in the clone from the
record's pre-close state, and it printed the same `New units` value byte for
byte. Then I called `units_named_earlier` over round-1.md directly, and it
returns `fenceleftopen` — `chain.EMPHASIS` is `[*_`]+` applied to the whole
entry, so every underscore inside a name goes with the backticks around it,
while `added` names come from the AST unstripped. `depth_two` therefore reaches
no snake_case parent at all. That is not this branch's defect: it is written
into `units_named_earlier` as a RIDER, with the repair described and the
repository owner named as its answerer.

The substantive consequence here is nothing. The depth rule exists because *the
unit it added is read by nobody* — and this round read `fenced_row_at` and its
case, so the guarantee the rule buys was delivered by the chain rather than by
the checker. The correction is to the declaration.

### The exemptions

Executed: `survivor-check --range 20eade5..5a1f47e --exempt
seal/specs/1789721571-…/survivors.md` exits 0 over 27 removed sentences, with
two survivors and both excused. I read the four rows this range added against
the paragraph of `overview.md` §*Fed back into the spec* that was rewritten.

All four grounds hold. The paragraph was moved, not withdrawn: what it said —
that a sentence about what was **written** may say *no ROW was written* and
nothing stronger — is still exactly what the four arms do, which I confirmed by
reading each arm's string. The case's standing sentence is a historical
measurement (*Measured before the fix*) and stays true. `plan.md`'s row is what
phase 1 was contracted to deliver, and the method that diverged is recorded in
`overview.md`'s own table. `hooks/config.py`'s standing text is `refusal`'s own
contract, untouched and accurate.

What the run showed that the orchestrator's did not: **only two of the six
exemption rows excused anything.** See the ⬜ below.

### `spec.md`, and the two `overview.md` sections

*Read.* Leaving `spec.md` alone is right. §*Data & interfaces* carries its own
escape hatch in the same paragraph as the contract — *A builder who diverges
records the divergence in `overview.md` with both sides quoted* — and the
divergence row now quotes the spec's sentence and the code's sentence side by
side. §*Fed back into the spec* now holds only clauses this work added, which
is what `templates/sdd-overview.md` reserves that heading for, and the new
paragraph about a sentence having to survive being followed is genuinely one
of them.

### The ledger

Executed: `evidence-check` exits 0 — 11 ok, 0 drifted, 0 broken in this work
item's fragment, 1364 ok across the tree. I read R8, R9 and R10 against the
code they cite and each states what that unit does. R7's narrowing is real: its
claim now says *the fence above it*, which is the act `fence_left_open` decides
rather than `fenced_row`, and R10 anchors that decision on the unit that makes
it. So the narrowed claim is covered twice rather than not at all.

One sentence in R10 is worth naming without opening a finding: *Asking about
the whole file is still what a caller gets by passing nothing* sits in a cell
labelled **Executed**, and no case in the tree exercises it. I executed it
myself and it is true, so the row is not false — it is the claim finding 1 is
about.

## Stage 2 — quality

The four fixes are each the smallest change that closes their finding, and
three of them read as the right depth. `with_row`'s guard is conditioned on
`end == len(lines)`, which is the only state in which the insertion point sits
past a line carrying no ending — every other state has a line after the table,
and `splitlines(keepends=True)` gives every line but the last an ending. The
`last_reached` computation is right for the reason its comment gives: `refusal`
appends `(line, stopper is None)` and never resets `stopper`, so `got` is
monotone and the last `True` is the stopper's own entry.

The one place the fix pass stopped short of its own class is the identity
comparison it left standing. See the second ⬜.

## Findings

### 1 · 🟡 `fence_left_open`'s `above=None` default answers the question the refusal must never ask

`skills/verify/scripts/broad_gate.py:397` — **executed**.

The parameter added this round is what makes the refusal say *a fenced code
block above it* truthfully. Its default undoes that: with no second argument
the function still answers *is any fence in this file left open*, which over a
row sitting in an example block that closes, in a file that opens a second
block lower down, is `True` — the exact answer round 2's 🟡 2 was opened
about.

Measured over that file: `fence_left_open(home)` is `True` and
`fence_left_open(home, at)` is `False`.

Two things follow, and neither is hypothetical.

- **The wrong answer is what a `None` returns rather than what raises.** The
  one caller guards `at` through `if fenced is not None`, so it is safe today.
  Move that call, or add a second caller that has no index in hand, and the
  pre-fix behaviour comes back silently. A required parameter turns that into a
  `TypeError` at the call, which is where it can be seen.
- **Nothing pins the unit's own answer.** No test in the tree calls
  `fence_left_open` at all, with or without the argument — I grepped `tests/`
  and the only hits were my own probe. Its behaviour is pinned only through a
  substring of `missing_row`'s message, so a change to the unit that leaves the
  message wording intact goes unnoticed.

The grounds the fix pass gave — that *is any fence in this file left open* is a
real question — names no caller that asks it. The `fence_map` docstring says
the second value exists *for the one caller that has somebody to tell*, and
that caller now always has an index.

Home if it becomes an issue: **"`fence_left_open`'s default answers about the
file when the question is about a row"** — the parameter that made the refusal
honest has a default that gives the dishonest answer back, no caller uses it,
and no case pins the unit at all.

### ⬜ `mine is stopper` is the last member of the class round 2's sweep was for

`skills/verify/scripts/broad_gate.py:591` — **executed**.

Three lines under the comment explaining that comparing `refused` line text by
identity is unsound, the same function still chooses an arm with
`elif mine is stopper:`.

It is correct today, and I measured it rather than assumed it. Over a file
carrying two identical `| Broad gate | a | b |` lines, one above the first
parsed row and one as the stopping line, `mine == stopper` is `True` and
`mine is stopper` is `False`, and the refusal takes the right arm — *The reader
stopped LOWER DOWN*. The reason is that CPython's shared-object cache is one
character wide, and `names_this_row` requires a first cell reading `Broad gate`,
so `mine` is never short enough to be shared.

That is the premise the comparison rests on, and the code does not state it,
no case pins it, and it is not the reason the fix pass gave. The grounds
offered — that `stopper` is the first refused line after a row was found and
`mine` is now taken at its first match too — do not establish soundness:
first-match on both sides does not stop two different positions holding equal
text from being one object. What stops it is the string length.

No defect ships, which is why this is ⬜ and not 🟡. What it costs is that the
class `agent-contract` §12 asks for is closed at one site and open at the
other, in one function.

Home if it becomes an issue: **"one identity comparison over `refused` text is
left, and its grounds are not the reason it works"** — `mine is stopper` is
sound only because `names_this_row` guarantees a long string, which nothing
states and nothing pins.

### ⬜ `fenced_row` has no production caller left

`skills/verify/scripts/broad_gate.py:365` — **read**.

`missing_row` now calls `fenced_row_at`, so the wrapper's only remaining reader
is one assertion at `tests/test_the_seal_is_taken_once_by_the_sealer.py:1887`.
The record's `Contract changes` row already says this in as many words
(`fenced_row → … pytest`), which is the row working.

I am not asking for its removal, and I want that on the record rather than
implied. Three docstrings name it, `hooks/config.py:343` points a reader at it
by name, and the ledger's R7 anchors on it. Widening it to return the pair and
deleting the wrapper would move all four. Naming it so the next reader does not
have to rediscover that the shorter name is the one nothing runs.

### ⬜ Two `New units` entries are declared at depth 1 and are at depth 2

`seal/specs/1789721571-…/rounds/round-2.md` — **executed**. A correction; it
owes no fix pass.

`fenced_row_at` and
`test_a_fence_opened_below_the_row_is_not_the_fence_above_it` were both added
by `15d4f38`, the fix of finding 2, whose `Location` names `fence_left_open` —
a unit round-1.md's `New units` names. The derivation and the reason `close`
could not see it are in Stage 1 above.

Nothing follows for the code. The rule's purpose is that a fix pass's units get
a reader, and this round is that reader.

### ⬜ Two survivor exemptions excuse nothing in this range

`seal/specs/1789721571-…/survivors.md` — **executed**. A correction.

`survivor-check` prints every excused survivor with its grounds, and it printed
two: the case module and `broad_gate.py`. The rows naming `plan.md` and
`hooks/config.py` matched no candidate. Their grounds are sound as reasoning —
I checked all four — but as rows they are now standing exemptions written about
a range they did not apply to.

`exempted` matches on the path and on a contiguous run of the quote's words in
the candidate's own text, with no tie to the range that produced the file. So a
later range that removes wording overlapping `refusal`'s docstring opening is
silenced by a row whose grounds read *The same rewritten paragraph*, naming a
paragraph that was rewritten here. The file's own header says there is no value
meaning *check nothing*; a row that excuses nothing is the closest thing to
one.

### ⬜ The changelog fragment does not carry the new site-1 sentence

`seal/specs/1789721571-…/changelog.md` — **read**. A correction.

The #430 bullet says the refusal *says that fixing the quoted line moves the
stopping place down rather than clearing the table*. The sentence round 2's
🟡 4 added says something strictly worse and different: that the rows arriving
**today** go with the repair, and that there is more than one line to write.
A person reading the released changelog would not learn that the refusal now
warns about a cost the old one never mentioned.

The fragment does carry the 🔴 (the no-ending row). The other three fixes are
covered by wording that was already there and is still true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `fence_left_open`'s `above=None` default answers the whole-file question round 2's 🟡 2 removed from the refusal — no caller, no case, and a `None` reaching it returns the old answer instead of raising | `skills/verify/scripts/broad_gate.py#fence_left_open` | deferred #446 | Executed: over the fixture round 2 named, `fence_left_open(home)` is `True` and `fence_left_open(home, at)` is `False`. No test in the tree calls the unit at all; its behaviour is pinned only through a substring of `missing_row`'s message. The chain is capped, so this goes to an issue rather than to a fix pass · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| ⬜ | `mine is stopper` is the one identity comparison over `refused` line text the sweep left, and its stated grounds are not the reason it works | `skills/verify/scripts/broad_gate.py#missing_row` | deferred #447 | Executed: over two identical `Broad gate` refused lines `mine == stopper` is `True` and `mine is stopper` is `False`, and the right arm is taken. It is sound because CPython's shared-object cache is one character wide and `names_this_row` guarantees a longer string — a premise nothing states and nothing pins · The round closed this `deferred` with no home; the number is the orchestrator's, written after the issue was opened. |
| ⬜ | `fenced_row` has no production caller left; one assertion is its whole reach | `skills/verify/scripts/broad_gate.py#fenced_row` | **answered** | Read: `missing_row` calls `fenced_row_at` now, and the only reader is `tests/test_the_seal_is_taken_once_by_the_sealer.py:1887`. Keeping it is grounded — three docstrings, `hooks/config.py:343` and ledger R7 name it — so this is named rather than commissioned |
| ⬜ | `New units` declares `fenced_row_at` and `test_a_fence_opened_below_the_row_is_not_the_fence_above_it` at depth 1; both are at depth 2 | `seal/specs/1789721571-…/rounds/round-2.md` | **correction** | Executed: both were added by `15d4f38`, the fix of finding 2, whose `Location` names `fence_left_open`, which round-1.md's `New units` names. `close` reproduced in a clone prints the same value; `units_named_earlier` returns `fenceleftopen`, the RIDERed emphasis-stripping defect, so `depth_two` reaches no snake_case parent. No consequence for the code — this round read both units |
| ⬜ | Two of the six survivor exemptions excused nothing in this range and stand ready to silence a later one | `seal/specs/1789721571-…/survivors.md` | **correction** | Executed: `survivor-check` exits 0 and names two excused survivors, the case module and `broad_gate.py`. `exempted` matches on path plus a word run with no tie to a range, so the `plan.md` and `hooks/config.py` rows apply to any future range carrying that wording |
| ⬜ | The changelog fragment does not carry the sentence round 2's 🟡 4 added | `seal/specs/1789721571-…/changelog.md` | **correction** | Read: the #430 bullet covers *moves the stopping place down* and not *the rows under THAT line, which arrive today, go with the repair*, which is a different and worse cost |
| 🟢 | Round 2's finding 1 is closed, both acts of it | `skills/implement/scripts/seal.py#with_row`, `#write_row` | **confirmed** | Executed: both touched modules are green in a clean clone at the target SHA, `164 passed, 3 skipped`. Read: `end == len(lines)` is the only state where the insertion point follows a line with no ending, since `splitlines(keepends=True)` terminates every line but the last |
| 🟢 | Round 2's finding 2 is closed, and the fence arithmetic is right at every arrangement | `skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row` | **confirmed** | Executed: `fence_left_open(home, at)` is `False` for a row in a block that closes with an unclosed block below, `True` for a row inside an unclosed block. An unclosed opener above a closed block is unreachable — `fence_map` lets it swallow everything under it |
| 🟢 | Round 2's finding 3 is closed, and the tail is found by position on grounds that hold | `skills/verify/scripts/broad_gate.py#missing_row` | **confirmed** | Read: `refusal` appends `(line, stopper is None)` and never resets `stopper`, so `got` is monotone and `max(position … if got)` is the stopper's own entry. Executed through the two-bare-pipe file, where the clause about further lines now prints |
| 🟢 | Round 2's finding 4 is closed, and the new clause is true exactly where it prints | `skills/verify/scripts/broad_gate.py#missing_row` | **confirmed** | Executed over seven config shapes covering all five arms. In the `stopper is None` arm every refused line precedes every parsed row, so `after_mine` non-empty means every row arriving today sits under the next refused line — which is what the sentence says. It correctly stays silent in the arm where the repair costs nothing |
| 🟢 | `write_row`'s non-fence arm is reachable only through a defective `with_row`, and its message is honest for that state | `skills/implement/scripts/seal.py#write_row` | **confirmed** | Read: the three `with_row` arms and both call sites enumerated — the value is `local` or `shared`, the insert arm now terminates, and the append arm lands outside every closed fence. Executed: the case drives the arm by replacing `with_row`, and the refusal names no fence |
| 🟢 | The four new survivor exemptions' grounds are sound | `seal/specs/1789721571-…/survivors.md` | **confirmed** | Read: the rewritten paragraph was moved rather than withdrawn, and what it claimed is still what the four arms do. The case's sentence is a historical measurement, `plan.md`'s row is a contracted past state, and `hooks/config.py`'s is `refusal`'s own untouched contract |
| 🟢 | Leaving `spec.md` unedited is grounded, and both `overview.md` sections now hold the right things | `seal/specs/1789721571-…/spec.md` §*Data & interfaces*, `…/overview.md` | **confirmed** | Read: §*Data & interfaces* carries its own escape hatch in the paragraph that states the contract, the divergence row quotes both sides, and §*Fed back into the spec* now holds only clauses this work added |
| 🟢 | R7's narrowing, R8, R9 and R10 state what the code does, and every anchor resolves | `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md` | **confirmed** | Executed: `evidence-check` exit 0 — 11 ok, 0 drifted, 0 broken in the fragment; 1364 ok across the tree. Read: R10 anchors the *above it* decision on the unit that makes it, so R7's narrowed claim is covered twice |
| ❓ | The full suite, the repository-wide lint and the typecheck | `tests/`, the repository's `Broad gate` row | **out of verified scope** | `agent-contract` §2 and this round's prompt both place the broad gate with the sealer, after the rounds settle. Two modules were run narrow, `evidence-check` and `survivor-check` were run whole, and nothing broad was run |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q` in a clean clone at `631df12` | `164 passed, 3 skipped` |
| `evidence-check` over the whole tree at `631df12` | exit 0 · `1364 ok · 0 drifted · 0 broken`; this work item's fragment `11 ok` |
| `survivor-check --range 20eade5..5a1f47e --exempt seal/specs/1789721571-…/survivors.md` | exit 0 · 27 removed sentences · two survivors, both excused; the other four exemption rows matched nothing |
| `fence_left_open` over a config whose row sits in a block that closes with a second block opened and never closed below it | `fence_left_open(home)` is `True`; `fence_left_open(home, at)` is `False`, `at` is 7. The default gives the pre-fix answer |
| A grep of `tests/` for `fence_left_open` | no hit. Nothing in the suite calls the unit, with or without the second argument |
| `refusal` over a config with two identical `Broad gate` refused lines, one above the first parsed row and one as the stopper, then `missing_row` over the same file | `mine == stopper` is `True`, `mine is stopper` is `False`, distinct ids; the refusal takes the *stopped LOWER DOWN* arm. `"\|\n\|\n".splitlines()` gives one shared object; the same two long lines give two |
| `missing_row` over seven config shapes — all five arms of the quoted-line refusal and the hidden-row refusal, each with and without a further refused line below | every sentence true of the file that produced it; the new *There is more than one line to write here* clause prints in the one arm where the repair costs a row and is absent from the arm where it costs nothing |
| `round-record close --item … --round 2 --fixes … --range 20eade5..5a1f47e` re-run in a clone from round-2.md's pre-close state | the same `Fix range`, `Contract changes` and `New units` values byte for byte, including `fenced_row_at (depth 1)`; no depth-2 refusal |
| `units_named_earlier` over round-1.md with the reader `close` uses | `{'fencemap': 1, 'fenceleftopen': 1, …}` — `chain.EMPHASIS` is `[*_`]+` over the whole entry, so `fence_left_open` is unreachable to `depth_two` |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** It is the sealer's, once, after the rounds settle (`agent-contract` §2) |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `fence_left_open`'s `above=None` default, and the unit having no case of its own | an issue — the run is capped, so nothing it opens is commissioned as a fix | the repository owner |
| The `mine is stopper` identity comparison and its unstated premise | an issue, for the same reason | the repository owner |
| `units_named_earlier` strips underscores, so `depth_two` reaches no snake_case parent | already RIDERed at `skills/code-review/scripts/round_record.py#units_named_earlier`, with the repair described | the repository owner |
| `round_record.py` and `chain_check.py` were not driven against a fenced example table | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after this record | the sealer |

## Paste-ready fixes

Finding 1 — drop the default, and say in the docstring why there is none:

```python
def fence_left_open(home, above):
    """Whether a fenced code block ABOVE the line at index ABOVE is never
    closed.

    Read off the one fence rule, not a second one. It is the difference
    between a row somebody pasted into an example block and a row that is in
    the live table with a fence swallowing it: the first has to move and the
    second must not, and telling the second person to move a row that is
    already where it belongs is an instruction that changes nothing (#429).

    `hooks/config.py#fence_map` already computes this while it walks; this
    reads the value rather than walking again.

    False for every way of not having an answer: no file, a file that will not
    read, a file with no fence in it at all.

    **Above, because that is what the sentence says.** A file whose row sits
    in an example block that closes and which opens a second block further
    down answered True for the whole file, and the person was told to close a
    fence that has nothing to do with their row while the act they needed --
    move it -- was the sentence they did not get (#429, round 2).

    **ABOVE has no default, and that is the guard rather than an omission.**
    The whole-file answer is the one this refusal must never use, so the
    shorter spelling must not reach it: a caller with no index in hand is a
    caller that has not decided which row it is speaking about, and a `None`
    arriving from one has to stop at the call rather than return the answer
    the line above was written to remove.
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return False
    opened_at = config.fence_map(text.splitlines())[1]
    return opened_at is not None and opened_at < above
```

And the case the unit has never had. It goes beside
`test_a_fence_opened_below_the_row_is_not_the_fence_above_it` in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, and it is red against the
current code at its second assertion:

```python
def test_the_fence_question_is_asked_about_the_row_and_not_the_file(tmp_path):
    """The unit itself, which until now was pinned only through a substring of
    `missing_row`'s message.

    The file has two blocks: the one holding the row closes, and the one below
    it never does. *Is any fence in this file left open* is True for it and
    *is a fence above this row left open* is False, and only the second is a
    question this refusal may ask. Asking the first is what told the person to
    close a fence that has nothing to do with their row (#429, round 2).
    """
    module = gate_module()
    home = tmp_path / "asked_about_the_row" / "seal"
    home.mkdir(parents=True)
    (home / "config.md").write_text(
        "# Repository config\n\nAn example of the format:\n\n"
        "```markdown\n| Item | Value |\n|---|---|\n"
        f"| {ROW} | EXAMPLE |\n```\n"
        "\nAnd a block somebody opened and never closed:\n\n"
        "```markdown\n| Item | Value |\n",
        encoding="utf-8",
    )
    at, line = module.fenced_row_at(str(home))
    assert at is not None and line is not None, (at, line)
    assert module.fence_left_open(str(home), at) is False, (
        "the row is inside a block that closes; the block opened below it is "
        "not a fence above the row"
    )
    with pytest.raises(TypeError):
        module.fence_left_open(str(home))
```

The ⬜ about `mine is stopper` — compare positions, so no comparison of
`refused` line text by identity is left in the function:

```python
    mine, reached, after_mine, after_stopper = None, False, [], []
    mine_at, stopper_at = None, None
    for position, (line, got) in enumerate(refused):
        if names_this_row(line):
            mine, reached, mine_at = line, got, position
            after_mine = [text for text, _got in refused[position + 1 :]]
            break
    if stopper is not None:
        # **The stopper's POSITION, not its identity.** `refused` holds line
        # text, and CPython hands back one shared object for every
        # one-character string -- so two refused lines that are both `|` are
        # the same object, `line is stopper` matched both, and the tail came
        # from the last of them with the clause about the lines below silently
        # dropped. Every entry appended before the stopper carries `got` True
        # and the stopper's is the last of those, which is a fact about how
        # `refusal` fills the list rather than about the text (#430, round 2).
        #
        # **And the arm below is chosen the same way**, because it was the
        # other half of the same class. `mine is stopper` is sound only while
        # `names_this_row` keeps `mine` too long for that shared cache -- a
        # premise nothing here states and no case pins, three lines under the
        # comment saying what the cache costs (#430, round 3).
        stopper_at = max(
            position for position, (_line, got) in enumerate(refused) if got
        )
        after_stopper = [text for text, _got in refused[stopper_at + 1 :]]
```

with the one arm rewritten:

```python
        elif mine_at == stopper_at:
```

Needs a fix: yes — finding 1, `fence_left_open`'s default answering about the file when the question is about a row.
Loses a record or crashes: no — nothing I found leaves the root and nothing raises.

The run is capped, so finding 1 lands as an issue rather than as a fix pass,
and this record is the last one. What comes due next is the sealer's spawn.

## Proof block

Files opened this round, in the tree at `631df12` unless a range is named:

- `skills/verify/scripts/broad_gate.py` — `fenced_row_at`, `fenced_row`,
  `fence_left_open`, `missing_row`, `refused_broad_row`, `names_this_row`,
  `hides_this_row`, `rows_read`
- `skills/implement/scripts/seal.py` — `table_span`, `with_row`, `write_row`,
  `line_ending`, the `fence_map` alias, `mode_report` and the second call site
- `hooks/config.py` — `fence_map`, `unfenced`, `refusal`, `refused_row`,
  `declared_mode`, `unescaped`, `CONFIG_ROW`, `FENCE`
- `tests/test_the_mode_question_is_asked_once.py`,
  `tests/test_the_seal_is_taken_once_by_the_sealer.py` — the four new cases and
  the fixtures they share
- `skills/code-review/scripts/round_record.py` — `depth_two`,
  `units_named_earlier`, `location_units`, the `close` parser, the module
  docstring's cell list
- `skills/code-review/scripts/survivor_check.py` — the module docstring,
  `exempted`
- `seal/specs/1789721571-…/` — `rounds/round-1.md`, `rounds/round-2.md`,
  `rounds/round-2-report.md`, `overview.md`, `spec.md`, `plan.md`,
  `survivors.md`, `changelog.md`
- `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`
- `docs/review-chain-spec.md` §*A verdict row that commissions nothing*,
  §*The reopening — one, and then the run is capped*, §*The depth in `New units`*
- `docs/review-handoff-protocol.md` §*`New units` names the verifying round's
  finding surface*, §*Loses a record or crashes*
- `templates/sdd-overview.md`, `CONTRIBUTING.md` §*What a change to a gate must
  carry*, `bin/test`
- the diff `20eade5..5a1f47e`, whole
