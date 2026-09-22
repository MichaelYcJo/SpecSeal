# Round 3 — the verifying round for round 2's fixes

Target SHA `02b2038d3a73c3306a255c856110dea4df1f8999`, branch
`feat/458-the-shipped-specs-are-sediment-no-check-reads`, base
`origin/release/v0.13.0`, pull request 486. The fix range is
`cd4ed9dee5af3afd8f44e6700ed4e0373f91506d..8007512602cf1ad8d3437b1dca2e7130654746a7`.

All eight of round 2's verdicts are closed. The refactor inside the fix pass
holds, the one judgment call it made is upheld, and every one of the thirteen
units nobody had reviewed reddens under a named mutation.

Four things are open, and the shape they share is the reason they are worth
the cap: **round 2's finding 5 named one door of a class and the pass closed
that one door.** The same pass closed the other door one function over,
in `folded_items`, and did not carry it back.

```
round 1  a fenced marker in docs/ excuses a removal        closed
round 2  a PARKED marker in docs/ excuses a removal        closed  ← finding 1
         a fenced marker in seal/ledger.md opens a section closed  ← finding 5
            ↓ the two axes were never crossed
round 3  a PARKED marker in seal/ledger.md opens a section OPEN    ← finding 2
         the fragments half of finding 5's fix             unpinned ← finding 3
```

Findings 1 and 4 are separate: an accessor that diverges from the module it
mirrors, and a case whose name promises more than it asks.

The cap is spent, so none of the four is a fix to commission. Each is a
candidate for its own issue.

---

## 🟡 1 — the opt-out refusal reads the marker the way `hooks/optin.py` says is wrong

`skills/settle/scripts/settle.py:614`

The new arm asks `os.path.exists` whether the scratch marker is under the git
common directory. `hooks/optin.py:200` asks `os.path.isfile`, and the comment
above it is a measured decision rather than a preference:

> A FILE, which is what this module and `seal/README.md` both say the signal
> is. `os.path.exists` also accepted a DIRECTORY of that name, and the marker
> used to sit in a committed directory — so `.specseal/scratch/` created once
> turned every gate off in every clone.

So the two readers of one marker now disagree about what counts as one, and
`settle` is the one that got the rejected reading. Round 2's own paste-ready
patch spelled it `os.path.isfile`; the pass departed from that silently.

**What it costs.** Executed against a repository with no `seal/` at either
place and a *directory* named `specseal-scratch` under `.git/`:
`home_at` returns `""` because the marker is not a file, and `settle`
answers

```
settle: <root> has opted out — `specseal-scratch` is under its git directory,
so every gate in this plugin reads it as a repository that never opted in and
this command will remove nothing. Delete that file to turn them back on.
```

Every clause after the dash is false. No gate reads that directory as an
opt-out, and deleting it turns nothing back on. This is finding 7's own defect
— a refusal naming the wrong one of two states — reintroduced inside finding
7's repair.

Reachability is low: it needs a directory of exactly that name. The fix is one
word, and the value of taking it is that the two readers stop disagreeing.

## 🟡 2 — a parked marker in `seal/ledger.md` still opens a section

`skills/settle/scripts/settle.py:320`

Finding 5 said a line anchor is not a test that the line is live, and the fix
routed `coordinates` through `blank_fences`. But the same fix pass established,
in `folded_items`, that **a line stops being live two ways** — a fence is a
quotation and an enclosing comment is a parked draft. `coordinates` was given
only the first.

Executed over a scratch ledger holding a real section and, below it, a section
marker sitting inside a commented-out draft block:

```
alpha: ['hooks/real.py']
beta : ['hooks/quoted.py']
```

The parked marker opened a section and took a coordinate with it. The
consequence is the one finding 5 named: `segment_of` groups that work item by
a coordinate nobody wrote for it, and the segment `settle` prints is wrong for
two work items at once. Nothing is removed, which is why this is not a 🔴.

**The obvious closure is wrong, and that is the part worth carrying.** Asking
`opens_outside_a_comment` of `seal/ledger.md` as it stands today loses three
real section markers — at lines 767, 992 and 1619. The cause is that ledger
cells quote comment fragments inside backticks: the anchor in the row at line
78 carries an opener with no closer inside a code span, and the comment state
it opens runs for hundreds of lines. `seal/ledger.md` has 787 lines that a
naive comment scan calls not-live.

So the rule the ledger needs is the comment rule **with inline code spans
blanked first**. Measured with that added: zero real markers lost, and the
parked marker still reads as not live. The paste-ready fix below is that.

`docs/` is not in the same position — every top-level document there has zero
non-live lines today, so the shipped `folded_items` fix costs nothing on the
real corpus.

## 🟡 3 — half of finding 5's fix is pinned by nothing

`skills/settle/scripts/settle.py:333` · `tests/test_settle_reads_before_it_removes.py:678`

`coordinates` reads two places, and the fix changed both: the ledger loop and
the fragment loop under `seal/ledger/`. Only the ledger half has a case.

Executed: reverting the fragment loop to `COORDINATE_RE.finditer(f.read())`
over the whole file — the pre-fix form, with no fence tracking — leaves
`tests/test_settle_reads_before_it_removes.py` and
`tests/test_unverified_rows_close.py` at **exit 0, nothing red**. Every other
mutation in the matrix reddened at least one case.

§15 is the rule this misses: a new behaviour is not planted until it has been
seen red. A fenced coordinate example in a work item's ledger fragment is
exactly as plausible as one in `seal/ledger.md` — more so, because a fragment
is where a work item explains its own rows — and the next editor who
simplifies that loop back will be told nothing.

## 🟡 4 — the case named for the single scan does not ask about the single scan

`tests/test_unverified_rows_close.py:1482`

`test_one_comment_scanner_serves_both_readers` is the case that guards the
refactor. Its docstring says it *asks that the two views still come out of one
scan*. Its last two assertions compare `comment_scan`'s output against the two
readers' output, which agrees whenever the two readers are correct — including
when one of them has been rewritten with its own private copy of the walk.

That is the duplicate-reader shape #487 is open about, and this case is the
only thing standing between the refactor and it.

Executed: replacing `comment_scan` at module level with a stub returning one
sentinel pair makes `strip_comments` answer `['SENTINEL']` and
`opens_outside_a_comment` answer `[True]`. Both readers go through the module
global, so a monkeypatch is enough to pin the single scan for real.

The first two assertions are sound and catch behaviour changes — the docstring
is what over-promises, and the fix is to make the case earn the sentence.

---

## What was checked and found sound

**Round 2's finding 1, and the refactor under it.** `strip_comments` returns
exactly what it returned. Executed: the pre-refactor body, copied from the diff
at `cd4ed9de`, against the shipped one over every tracked markdown file in the
repository — **1,435 files, zero differing** — plus 584 arrangements of comment
tokens up to length three, zero differing. The caller surface this branch never
touched is green too: the eight modules that exercise `strip_comments`,
`readable` and `round_record.py`'s use of both, **336 passed, exit 0**.

**Round 2's finding 6, and the sub-point the pass refused.** The refusal is
upheld. `survey["released"]` is built as `[i for i in present if i in on_base]`,
so it is a subset of the directories `survey` saw and `present` really is inert
inside `candidates` — but the term now has a second reader that is not inert:
`stranded = sorted(marked & present)` at `settle.py:518`, and
`test_a_marked_item_still_on_disk_is_not_the_fold_being_complete` exercises it.
Both halves of the pass's claim check out. Dropping the term to satisfy the
finding would have made a destructive call rest on an invariant another
function held at another moment, for the saving of one set operation.

**The ordering inside `folded_items` is the right way round.** Fences are
blanked before the comment scan runs, so an unbalanced opener quoted inside a
fenced block cannot swallow a genuine marker below it. The reverse order would
have.

**The interpreter-floor class, which the pass found one member of by accident.**
`skills/verify/scripts/unverified_check.py` carries no floor guard, so
everything this branch added to it has to run on whatever `python3` a user has.
Executed on `/usr/bin/python3`, which is 3.9.6 on this machine: the module
compiles, imports, `folded_items`, `strip_comments` and
`opens_outside_a_comment` all answer correctly, the command runs over this work
item at exit 0, and `--baseline origin/release/v0.13.0 seal/specs` runs over
90 overviews at exit 0. The two other scripts this branch changed that carry no
guard — `.github/scripts/gather_changelog.py` and its neighbour
`.github/scripts/fold_ledger.py` — compile on 3.9 as well. No second member of
the class.

**The four ledger re-reads.** `evidence-check` at this SHA: the work item's
fragment is 13 ok · 0 drifted · 0 broken, and `seal/ledger.md` is 1,402 ok · 0
drifted · 0 broken, both exit 0. The interesting row is the `strip_comments`
one, whose walk moved in this pass: its claim is that a cell inside an HTML
comment is not the row, and that is still exactly what the function at the new
coordinate does — the equivalence measurement above is the grounds, and
`test_a_cell_inside_a_comment_is_not_the_row` is green in the caller run. The
row's note leans on one case for the phrase *returns exactly what it returned*,
which is thinner than the sentence, but the sentence is true.

**Round 2's `New units` row is exactly right** — thirteen, and the fix range
adds thirteen: two functions and eleven cases, counting the two parametrised
families as one unit each.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The opt-out refusal reads the scratch marker with `os.path.exists`, the accessor `hooks/optin.py` documents as measured-wrong, so `settle` and the opt-in module disagree about what a marker is | `skills/settle/scripts/settle.py:614` · `hooks/optin.py:200` | open | executed — against a repository with no root and a DIRECTORY of that name, `home_at` answers `""` while `settle` answers *has opted out … Delete that file to turn them back on*, and every clause after the dash is false |
| 🟡 2 | `coordinates` got the fence half of round 2's finding 5 and not the comment half: a marker inside a commented-out draft in `seal/ledger.md` still opens a section | `skills/settle/scripts/settle.py:320` | open | executed — a scratch ledger with a parked marker attributes `hooks/quoted.py` to the id in the parked block. The naive closure is wrong: applying `opens_outside_a_comment` to today's `seal/ledger.md` loses three real markers at lines 767, 992 and 1619, because a row's anchor quotes an unclosed opener inside a code span |
| 🟡 3 | The fragment half of finding 5's fix is pinned by nothing — reverting it turns no case red | `skills/settle/scripts/settle.py:333` · `tests/test_settle_reads_before_it_removes.py:678` | open | executed — mutation M7, the fragment loop back to a whole-file `finditer`: both modules exit 0 with nothing red, where all ten other mutations reddened at least one case |
| 🟡 4 | `test_one_comment_scanner_serves_both_readers` says it pins that the two views come out of one scan; its assertions only ask that they agree, which a duplicated walk also satisfies | `tests/test_unverified_rows_close.py:1482` | open | executed — stubbing `comment_scan` at module level makes both readers answer from the stub, so the single scan is pinnable and is not pinned |
| 🟢 confirmation | Round 2 finding 1: a marker inside a commented-out draft is no longer a fold record | `skills/verify/scripts/unverified_check.py:697` | confirmed closed | executed — M1 and M2 each redden `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record` and the comment-shape family |
| 🟢 confirmation | The refactor is behaviour-preserving: `strip_comments` returns what it returned | `skills/verify/scripts/unverified_check.py:182` | confirmed | executed — 1,435 tracked markdown files and 584 token arrangements, zero differing; the eight caller modules 336 passed at exit 0 |
| 🟢 confirmation | Round 2 finding 2: *The fold is complete.* no longer prints over a marked item still on disk, and still prints when it is | `skills/settle/scripts/settle.py:518` | confirmed closed | executed — M4 reddens the first case, M5 reddens the second |
| 🟢 confirmation | Round 2 finding 3: the exit-code list names five states and the skill names the refusal | `skills/settle/scripts/settle.py:60` · `skills/settle/SKILL.md:39` | confirmed closed | executed — M10 reddens `test_the_module_and_the_skill_both_say_local_mode_is_refused` |
| 🟢 confirmation | Round 2 finding 4: the `--released-at` refusal is about the ref and nothing else | `skills/settle/scripts/settle.py:667` | confirmed closed | executed — M9 reddens the case |
| 🟢 confirmation | Round 2 finding 5, for the half it named: a fenced marker in `seal/ledger.md` opens no section | `skills/settle/scripts/settle.py:320` | confirmed closed | executed — M6 reddens `test_a_fenced_marker_in_the_ledger_opens_no_section`. What the fix did not reach is findings 2 and 3 above |
| 🟢 confirmation | Round 2 finding 6, and the sub-point the pass refused rather than took | `skills/settle/scripts/settle.py:497` · `:518` | confirmed closed | executed for the docstring (M11 reddens the pin); read for the refusal — `survey["released"]` is built from `present`, so the term is inert in `candidates`, and `stranded = sorted(marked & present)` is the second reader the pass claimed |
| 🟢 confirmation | Round 2 finding 7: an opted-out repository is told which state it is in | `skills/settle/scripts/settle.py:608` | confirmed closed | executed — M8 reddens the case. The accessor it uses is finding 1 above |
| 🟢 confirmation | Round 2 finding 8: the S1 row says seven | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | confirmed closed | read — the sentence reads *seven fence shapes* and names the six comment shapes beside them |
| 🟢 confirmation | Every one of the thirteen new units reddens under a named mutation, and the row names exactly the thirteen the fix range adds | `tests/test_settle_reads_before_it_removes.py` · `tests/test_unverified_rows_close.py` · `skills/verify/scripts/unverified_check.py` | confirmed | executed — eleven mutations, each applied alone and restored, every substitution asserted to have matched; the mapping is in the probes table |
| 🟢 confirmation | No construct this branch added to the unguarded reader needs a floor the module does not declare | `skills/verify/scripts/unverified_check.py` | confirmed | executed on 3.9.6 — compile, import, the three changed functions, the command over this work item, and `--baseline` over 90 overviews, all exit 0; the other two unguarded scripts the branch changed compile there too |
| 🟢 confirmation | The four ledger rows re-read in `80075126` are true at their new coordinates | `seal/ledger.md:80` · `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md` | confirmed | executed — `evidence-check` 13 ok and 1,402 ok, 0 drifted, 0 broken, exit 0; the `strip_comments` row's claim is what the equivalence measurement establishes |
| ⬜ 5 | The refusal path asks git for the common directory twice: `home_at` resolves it internally and the new arm resolves it again, although `home_at(root, common)` exists for exactly this and says so | `skills/settle/scripts/settle.py:606` · `hooks/optin.py:178` | open | read — one extra `rev-parse` on an error path only; the parameter is documented with the measurement that created it |
| ⬜ | Round 1 finding 6, deferred to #487 — still the right call, and findings 2 and 4 above both point at it | `skills/settle/scripts/settle.py:218` | deferred #487 | already deferred in round 1 |
| ⬜ | Round 1 finding 9, deferred to #488 | `CLAUDE.md` §*a change writes fragments, never the shared file* | deferred #488 | already deferred in round 1 |
| ❓ scope | The broad gate — the full suite, the repository-wide lint and the typecheck | whole tree | ❓ out of verified scope | §2 gives it to the sealer and the prompt withholds it; the orchestrating session answers. Nothing in this report leaves a fix outstanding that would spend it, so it has come due |

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_settle_reads_before_it_removes.py` and `tests/test_unverified_rows_close.py` in a `--no-local` clone at the target SHA | `161 passed`, exit 0 read directly — the baseline every mutation below runs against |
| M1 — `folded_items` stops asking whether the line is live | red: `test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record`, `test_every_comment_shape_a_policy_document_can_carry` |
| M2 — `comment_scan` reports the state the line ENDED in | red: 18 cases including `test_one_comment_scanner_serves_both_readers`, `test_readable_would_erase_every_fold_record`, both comment-shape and fence-shape families |
| M3 — `comment_scan` keeps the text a comment opener swallows | red: `test_one_comment_scanner_serves_both_readers`, `test_readable_would_erase_every_fold_record`, three older comment cases |
| M4 — the fold-is-complete arm fires on `if marked:` again | red: `test_a_marked_item_still_on_disk_is_not_the_fold_being_complete`, alone |
| M5 — the fold-is-complete arm never fires | red: `test_the_fold_is_complete_still_prints_when_it_is` and two older cases |
| M6 — `coordinates` reads the ledger without fence tracking | red: `test_a_fenced_marker_in_the_ledger_opens_no_section`, alone |
| M7 — `coordinates` reads the FRAGMENTS without fence tracking | **exit 0, nothing red** — finding 3 |
| M8 — the opt-out is not told apart from no root | red: `test_an_opted_out_repository_is_told_which_state_it_is_in`, alone |
| M9 — the ref refusal talks about local mode again | red: `test_the_released_at_refusal_is_about_the_ref_and_nothing_else`, alone |
| M10 — the skill stops saying the command refuses local mode | red: `test_the_module_and_the_skill_both_say_local_mode_is_refused`, alone |
| M11 — `survey`'s docstring says the retirement is derived from it | red: `test_surveys_docstring_does_not_invite_the_mutation_that_reopens_finding_4`, alone |
| the pre-refactor `strip_comments` body against the shipped one, over `git ls-files "*.md"` and 584 comment-token arrangements | 1,435 files, 0 differing; 584 arrangements, 0 differing |
| `comment_scan` replaced at module level by a stub returning one sentinel pair | `strip_comments` → `['SENTINEL']`, `opens_outside_a_comment` → `[True]` — the single scan is pinnable, finding 4 |
| the eight modules that exercise `strip_comments`, `readable` and their callers | `336 passed`, exit 0 |
| `coordinates` over a scratch ledger holding a real section and a parked section marker below it | the parked marker opened a section and took `hooks/quoted.py` with it — finding 2 |
| `opens_outside_a_comment` over today's `seal/ledger.md`, and over it again with inline code spans blanked | 3 real markers lost, 787 lines not live; with code spans blanked, 0 lost and the parked marker still reads not live |
| `opens_outside_a_comment` over every top-level `docs/` document in this repository | 0 non-live lines — the shipped `folded_items` fix costs nothing on the real corpus |
| `settle` against a repository with no `seal/` and a DIRECTORY named `specseal-scratch` under its git directory | `home_at` → `""`; `settle` → exit 2, *has opted out … Delete that file to turn them back on* — finding 1 |
| `/usr/bin/python3` (3.9.6): compile, import and exercise of `skills/verify/scripts/unverified_check.py`; the command over this work item; `--baseline origin/release/v0.13.0 seal/specs` | all exit 0; 90 overviews · 303 open · 65 closed · 0 unreadable |
| `/usr/bin/python3 -m py_compile` over `.github/scripts/gather_changelog.py`, `.github/scripts/fold_ledger.py` and `hooks/optin.py` | exit 0 each |
| `evidence-check` over the work item's ledger fragment, and over `seal/ledger.md` | 13 ok and 1,402 ok · 0 drifted · 0 broken, exit 0 each |
| `folded_items` over this repository at the target SHA | empty set — `settle --retire` here removes nothing, so no destructive arm was reachable from this review |
| the broad gate — the full suite, repository-wide lint, typecheck | not yet. §2 assigns it to the sealer, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `skills/verify/scripts/unverified_check.py:697` | round 2's 1 — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:518` | round 2's 2 — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:60` · `skills/settle/SKILL.md` | round 2's 3 — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:667` | round 2's 4 — confirmed closed |
| round-2 | `skills/settle/scripts/settle.py:320` | round 2's 5 — closed for the half it named; findings 2 and 3 are what it did not reach |
| round-2 | `skills/settle/scripts/settle.py:497` | round 2's 6 — confirmed closed, refusal upheld |
| round-2 | `skills/settle/scripts/settle.py:608` | round 2's 7 — confirmed closed; finding 1 is inside the repair |
| round-2 | `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md:3` | round 2's 8 — confirmed closed |
| round-1 | `skills/settle/scripts/settle.py:218` | round 1's 6 — deferred #487, and two of this round's findings point back at it |
| round-1 | `CLAUDE.md` §*a change writes fragments, never the shared file* | round 1's 9 — deferred #488 |

## Regression cases to plant

| Case | Destination file | What it pins |
|---|---|---|
| `test_a_parked_marker_in_the_ledger_opens_no_section` (NAME NOT IN TREE) | `tests/test_settle_reads_before_it_removes.py`, beside `test_a_fenced_marker_in_the_ledger_opens_no_section` | finding 2 — and the same case has to assert that this repository's own `seal/ledger.md` still yields 94 sections, because that is the half the naive closure breaks |
| `test_a_fenced_coordinate_in_a_fragment_is_not_the_fragments_own` (NAME NOT IN TREE) | the same module | finding 3 — the fragment loop, which today no case reaches |
| the monkeypatch assertions below | `tests/test_unverified_rows_close.py`, inside `test_one_comment_scanner_serves_both_readers` | finding 4 — that the two views come off one walk, rather than merely agreeing |
| the opt-out arm against a DIRECTORY of the marker's name | `tests/test_settle_reads_before_it_removes.py`, beside `test_an_opted_out_repository_is_told_which_state_it_is_in` | finding 1 — that the two readers of the marker answer alike |

## Facts for the evidence ledger

| Claim | Where it was established | Note |
|---|---|---|
| The extraction of `comment_scan` leaves `strip_comments` returning exactly what it returned | measured over 1,435 tracked markdown files and 584 comment-token arrangements at this SHA, 0 differing | the S-row note in `seal/ledger.md` for `strip_comments` currently cites one case for this; this is the measurement behind the sentence |
| `skills/verify/scripts/unverified_check.py` runs on python 3.9 | executed on 3.9.6: compile, import, the three changed functions, the command, and `--baseline` over 90 overviews, all exit 0 | the module carries no floor guard, so this is the floor a user's `python3` actually has to clear |
| `seal/ledger.md` carries 787 lines that a comment scan calls not-live, from anchors quoting an unclosed opener inside a code span | measured at this SHA | this is why the comment rule cannot be carried to `coordinates` unchanged |

## Paste-ready fixes

Finding 1 — `skills/settle/scripts/settle.py:614`:

```python
        if common and os.path.isfile(os.path.join(common, optin.SCRATCH)):
```

Finding 2 — `skills/verify/scripts/unverified_check.py`, a helper beside
`blank_fences`, then `skills/settle/scripts/settle.py#coordinates` reading
through both. The helper name below does not exist in the tree yet.

```python
CODE_SPAN = re.compile(r"`+[^`]*`+")


def blank_code_spans(lines):
    """The same lines with inline code spans blanked out, indices intact.

    A ledger row's anchor quotes the text it is anchored to, and that text is
    often a comment -- `seal/ledger.md` carries an anchor holding an opener
    with no closer, and the comment state it opens runs for hundreds of lines.
    Measured 2026-09-22: asking `opens_outside_a_comment` of that file without
    this loses three real section markers, at lines 767, 992 and 1619, and
    calls 787 of its lines not live.
    """
    return [CODE_SPAN.sub(lambda m: " " * len(m.group(0)), line) for line in lines]
```

```python
    out = collections.defaultdict(list)
    reader = load(READER, "specseal_unverified_reader")
    ledger = under(root, LEDGER)
    if os.path.isfile(ledger):
        with open(ledger, encoding="utf-8") as f:
            lines = reader.blank_fences(f.read().split("\n"))
            # A line stops being live two ways, which is what `folded_items`
            # already asks: a fence is a quotation and an enclosing comment is
            # a parked draft. Code spans are blanked first because a row's
            # anchor quotes comment text, and an unclosed opener inside one
            # would park every section below it.
            live = reader.opens_outside_a_comment(reader.blank_code_spans(lines))
            current = None
            for n, line in enumerate(lines):
                if not live[n]:
                    continue
                marker = MARKER_LINE_RE.match(line)
```

Finding 3 — `tests/test_settle_reads_before_it_removes.py`, beside the fenced
ledger case. The opener is assembled rather than written out because a report
carrying a literal unclosed one blanks itself; the planted case should write
it literally.

```python
def test_a_fenced_coordinate_in_a_fragment_is_not_the_fragments_own(tree):
    """The other half of round 2's finding 5. `coordinates` reads two places
    and the fix changed both; only the ledger half had a case, so reverting
    the fragment loop to a whole-file `finditer` turned nothing red."""
    fragment = tree / "seal" / "ledger" / "1700000001-alpha.md"
    fragment.write_text(
        fragment.read_text(encoding="utf-8")
        + "\nAn example of the convention:\n\n```markdown\n"
        + "| q | `hooks/quoted.py#thing@99999999` | read | 2026-01-01 | |\n"
        + "```\n",
        encoding="utf-8",
    )
    assert "hooks/quoted.py" not in settle.coordinates(str(tree))["1700000001-alpha"]
```

Finding 4 — `tests/test_unverified_rows_close.py`, replacing the last two
assertions of `test_one_comment_scanner_serves_both_readers`:

```python
    # One scan, asked of the code rather than of the two answers agreeing:
    # a second private copy of the walk answers identically and would pass
    # every assertion above. Both readers reach `comment_scan` through the
    # module global, so replacing it is what tells them apart.
    real = uc.comment_scan
    uc.comment_scan = lambda lines: iter([(True, "SENTINEL")])
    try:
        assert uc.strip_comments(lines) == ["SENTINEL"]
        assert uc.opens_outside_a_comment(lines) == [True]
    finally:
        uc.comment_scan = real
```

Needs a fix: yes — findings 1 through 4. None of them is a fix to commission,
because the cap is spent: each is a candidate for its own issue, and finding 2
is the one that should carry the measurement about code spans with it.
Loses a record or crashes: no

## Proof block

Executed in a `git clone --no-local` of this repository at
`02b2038d3a73c3306a255c856110dea4df1f8999`, deleted with its probe before this
report was handed over. Every mutation was applied alone, asserted to have
matched, and restored before the next; the baseline and the restored state were
both exit 0 with nothing red.

Read: `seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/rounds/round-1.md`
· `rounds/round-2.md` · `rounds/round-2-report.md` · `changelog.md` ·
`skills/settle/scripts/settle.py` · `skills/settle/SKILL.md` ·
`skills/verify/scripts/unverified_check.py` · `hooks/optin.py` ·
`tests/test_settle_reads_before_it_removes.py` ·
`tests/test_unverified_rows_close.py` ·
`tests/test_a_script_says_which_interpreter_it_needs.py` ·
`skills/code-review/scripts/round_record.py` (the verdict and id rules) ·
`.github/scripts/run_tests.py` · `seal/ledger.md` ·
`seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`
· `seal/config.md` · `docs/release-checklist.md` · `bin/test` · `CLAUDE.md`.

Not run, and named rather than omitted: the broad gate. The orchestrating
session answers for it, and it comes due now.
