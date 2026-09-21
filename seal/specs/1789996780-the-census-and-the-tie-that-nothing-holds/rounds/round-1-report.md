# 1789996780-the-census-and-the-tie-that-nothing-holds — round 1 report

| Field | Value |
|---|---|
| Work item | `1789996780-the-census-and-the-tie-that-nothing-holds` |
| Branch | `fix/the-census-and-the-tie-that-nothing-holds` |
| Target SHA | `55ae1b63` |
| Range read | `release/v0.12.3..55ae1b63` (`8531c858..55ae1b63`, twelve commits) |
| Round | 1 — no earlier round of this work item to inherit from |
| Read in | a `git clone --no-local` of the repository at the target SHA |

## The round paragraph, for the record's `Asked` cell

Round 1 of the whole branch, spawned against `55ae1b63` with no earlier round
to inherit from. The prompt named the claim to test hardest — that every
figure the module states about its corpus now stands at one site, carries a
corpus, an instrument and a moment, and that the corpus-moved history claim
behind the grounds replacement holds — and disclosed eight divergences for
the round to judge rather than accept. The census was re-taken independently
at the tip with a walk written for this round, the A7 mutation pair and the
A8 mutation were re-run, the workflow was compared for moved steps, the class
was re-enumerated by construction rather than by the branch's grep, and the
two survivor exemptions were re-measured. Every digit in the census note
reproduces. Three sites stating a corpus figure survive outside the one the
spec permits, one of them false at the tip and measured false by this branch
in a neighbouring record.

## What the account claimed and what the code says

**The history claim holds.** `a8bf2a86` added 44 rows to `seal/ledger.md` and
deleted all three `seal/ledger/*.md` fragments in the same commit — executed:
`git ls-tree a8bf2a86^ -- seal/ledger/` lists three files and
`git ls-tree a8bf2a86 -- seal/ledger/` lists none. So the corpus #470
prescribed as *a corpus a branch cannot move* had already been moved by a
release before the ticket was read, and this branch moves it again: the
`Corrected a third time 2026-09-22` marker it writes into row C1 is itself a
qualified marker the census counts. Replacing the grounds rather than
restating the prescription is right, and the note's replacement grounds — it
is the file a release folds the fragments INTO — is the one that survives.

**Every figure in the census note reproduces at the tip.** Re-taken with a
verb-by-verb walk written for this round, over `seal/ledger.md` at
`55ae1b63`: 429 candidate sites against 429 `MARKER` occurrences with none
`MARKER` fails to see; 426 standing on 204 rows and 3 in prose; 385 bare and
44 qualified in exactly the ten spellings the note lists with exactly the
counts it gives; run lengths 0: 385, 1: 23, 2: 9, 3: 11, 5: 1 and no run of
four; 428 at a bound of three, 428 at four, 429 at five, six and eight; the
longest run five words, spelled `Re-read and re-stamped a third time
2026-09-08`, standing in prose, with no table row carrying a qualifier longer
than three words. Row C2's re-measured split reproduces too: 16 rows carrying
a `Corrected`, 196 a `Re-read`, 204 either, 21 and 405 occurrences.

**The instrument is genuinely wider than the pattern it calibrates, and
cannot be it.** The walk reads `VERBS` from the module and builds its own
verb, date and lowercase-run patterns; it never touches `MARKER`. It is
`MARKER` with the bound removed and with nothing else narrowed: `MARKER`'s
gap can only hold lowercase words, so it can never span a date, which means
the walk's *first date on the line* restriction discards nothing `MARKER`
could have reached. The 429-against-429 bijection with an empty unseen list
is the measured half of the same statement.

**The mutation pair is real, both legs.** Executed by this round, not read.
Narrowing `MARKER`'s bound to `{0,4}` turns the census case red at
`1 of 429 candidate marker site(s) fall outside the bound`, naming the file,
the run length, the spelling and the row as `(prose, outside any row)`.
Narrowing the bound to four **and** rewriting the census to walk `MARKER`
leaves the case green at exit 0. That is the circular census reproduced on
demand, and it is what makes the instrument choice load-bearing rather than a
preference. The A8 mutation is real too: `for parent in reversed(kin)` reddens
exactly the new tie case, 1 failed and 49 passed.

**The workflow moved nothing but a comment.** Executed: the two revisions of
`.github/workflows/hygiene.yml` with every comment line stripped hash to the
same value and the same 135 lines, so no step, condition, command or range
moved. The rewording around the bare `correction_check.py` literal is honest
— the file now names that token exactly once, on the real run line — and
`test_a9_the_leg_asks_the_range_the_pull_request_is_about` is green.

**Nothing a person reads in the module moved.** Executed: parsing both
revisions of `correction_check.py` and dumping the syntax tree with every
docstring removed gives identical structure, so A11's *no exit code, verdict
or printed line changes* is verified by construction rather than asserted.

**Both survivor exemptions are honest.** `survivor-check` reports no standing
survivor at the tip with no exemption file passed at all, so neither row
excuses anything today. The second row's grounds are a measurement, and it
re-measures true: walking every row of `seal/ledger.md` and keeping those
whose every marker carries a qualifier returns exactly one row, and it is R4.
Nothing was reworded to quiet the checker — the three sentences the check
caught were corrected as live statements of the class, which is what phase 3
says.

**Disclosure 8 is right and understates itself.** `#MARKER` did not drift;
`#standing` did, and the frame names it nowhere. `evidence-check .` reports
`1399 ok · 0 drifted · 0 broken`, and rows C3 and C4 carry the new
`#standing@89914aad` with a `Re-read 2026-09-22` marker each.

**The account's own figures for the sibling work item reproduce.** Re-measured
at `31b320e5` with this round's walk: 404 occurrences in `seal/ledger.md`, 401
on 190 rows, 3 in prose, and 412 / 412 / 413 across the three ledger files at
bounds of three, four and five. Keeping those figures in the sibling's records
with a moment attached rather than re-taking them is the right call and the
grounds hold. `seal/ledger.md:1172` stood in exactly four places before this
branch, which is what the changelog fragment claims.

---

## Finding 1 — 🔴 the module states a corpus figure at three sites, not one, and its own docstring now says otherwise

`skills/evidence-check/scripts/correction_check.py:559` and
`skills/evidence-check/scripts/correction_check.py:377`.

A1 is the work item's central acceptance row, and its stated verification is a
grep over the whole file. That grep fails. Two figures about the corpus stand
outside the census note:

- **`read_blobs`'s docstring, line 559** — *The shared ledger here is 1.07 MB
  and a range can hold dozens of merges*. Present tense, no moment, and false
  at the tip: `seal/ledger.md` is 1,112,008 bytes, which is 1.11 MB decimal
  and 1.06 MiB binary. Neither reading is 1.07.
- **`standing`'s docstring, line 377** — *Latent when round 1 measured it --
  0 of 189 marked rows share a key*. The moment is named, so the sentence is
  not false, but it is a corpus figure at a second site and A1 permits none.

What makes this a spec violation rather than a note is that the branch
measured the first one false and wrote the true value down in the same commit
range. The correction marker this branch added to
`seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md`
says *The file is 2408 lines and 1.11 MB at the tip of the branch for #469,
#470 and #471*, and it removed *2364 lines and 1.07 MB* from that record for
exactly the reason that leaves 1.07 standing here. The same digit was removed
from the module docstring at line 156 and from the `SIZE_CAP` comment at line
187, each replaced by *about a megabyte*, and the `SIZE_CAP` comment's new
sentence reads *No measured size stands here: the file grows at every release,
and the census note below is the one site in this module that states a figure
about the corpus.* Three hundred and seventy lines below it, one does.

And the module docstring now asserts the claim itself: *The census beside
`MARKER` below is the only place in this module that states a figure about the
corpus.* That sentence is false at the tip. A module whose subject is that the
check shipping false claims was shipping two of its own now ships a third, and
it is a claim about itself.

**Why the enumeration missed them.** The class was enumerated by grepping the
tracked tree for the spelling `404 ... on 190 rows`. `1.07 MB` carries no
three-digit run and no `404`, and `0 of 189` carries neither spelling. That is
phase 3's own sharpest finding — *a grep enumerates a spelling; the class is a
kind of claim, and the two do not coincide* — applied to two of the three
copies and not to the third.

## Finding 2 — 🟡 the class is still one site short in code, in the test module this work edited

`tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_merge_that_reverts_a_re_read_row_is_reported`.

The docstring reads *`Re-read` is the marker 185 rows of the shared file carry
against `Corrected`'s 10*. Present tense, no moment, and stale: measured at
the tip, `grep -c` gives 203 lines carrying a `Re-read` against 19 carrying a
`Corrected`, and by markers rather than lines the split is 196 rows against
16. It was already stale at the branch point — 202 against 19 at `f4232014` —
so this is not drift the branch introduced.

It is the same pair of figures, 10 and 185, that this branch corrected in
ledger row C2, and the grounds it wrote there apply here word for word: *a
figure with no moment on it over a corpus that moves*. The branch corrected
two docstrings in this file and left a third that states the same claim in
different words, four hundred lines from the two it did correct. A4 says every
present-state site is enumerated by construction and corrected; `agent-contract`
§12 says the fix is owed to every instance the same cause produces. This is the
fourth time in this lineage the class has shipped one site short.

## Finding 3 — 🟡 the census note states a figure its own named instrument cannot produce

`skills/evidence-check/scripts/correction_check.py:250-252`.

The note opens with a rule it applies to itself: *Every figure here is three
things or it is nothing: a corpus, an instrument and a moment*, and it names
one instrument for the block — *the unbounded walk above, never `MARKER`*.
The block then ends on *Nine commits in this repository's history have
introduced `Re-read again` into that file.*

The unbounded walk counts marker sites in a file. It cannot count commits, so
a reader cannot re-take nine from the instrument the note names, which is what
A2 asks for. Measured this round, three defensible instruments give three
answers over `seal/ledger.md`: `git log -S'Re-read again'` reports **9**,
counting commits whose occurrence count differs from every parent reports
**8**, and counting against the first parent reports **13**. Nine is
reproducible, but only by an instrument the note does not name.

The conclusion the figure supports — the qualifier is not a one-off somebody
can be asked to stop writing — holds at 8, 9 and 13, so nothing downstream is
wrong. What is wrong is that the note's own rule fails on the note's own last
sentence, in the one module where that rule is the deliverable.

## Finding 4 — 🟡 `site_row` is unpinned, and the reason given for leaving it so does not hold

`tests/test_a_merge_cannot_silently_drop_a_correction.py#site_row`.

Verified by execution: replacing the whole body of `site_row` with `return ""`
leaves the module green at 50 passed. So the measurement in `overview.md`
§*Not verified* is honest, and the row clause of the census case's failure
message is held by nothing.

The grounds are where this round disagrees. `overview.md` says *pinning it
needs a case that asserts a failure, and `spec.md` A11 says this module grows
by exactly the two cases. Relaxing A11 is not `smith`'s call.* A11 constrains
the number of **cases**, not the number of assertions, and `site_row` is a
plain function of two arguments that can be pinned by two asserts inside the
census case that already exists. No case is added, A11 is untouched, and
nothing has to be relaxed by anybody.

That matters because `agent-contract` §14 is the rule the work item invoked
for #471: a fix that changes what a person sees documents it and pins it. The
census case's docstring promises a failure message naming *the file, the row,
the run length and the spelling*. Three of those four are pinned by the
bound-narrowed mutation recorded in ledger row D1. The fourth is documented,
promised, and free to be edited away silently.

## Finding 5 — 🟡 the census case's corpus reader crashes on a tracked file the worktree has lost

`tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus`.

`git ls-files` reads the **index**, and the reader then opens each listed path
from the worktree. A path that is tracked but absent from disk raises
`FileNotFoundError` out of `read_text` before any assertion runs.

Reproduced this round: deleting the work item's own ledger fragment from the
worktree without staging the deletion turns the case red on
`FileNotFoundError: ... seal/ledger/1789996780-the-census-and-the-tie-that-nothing-holds.md`
rather than on either of the two guards written for an empty corpus.

The state that produces it is the release, not a hypothetical.
`fold_ledger.py` moves every fragment into `seal/ledger.md` and removes the
files; a suite run between that removal and `git add` meets exactly this. This
repository has already paid for the same class once — an unstaged deletion
against an index-reading command cost a ten-minute run during a release. The
case is the module's first that reads the tree, so it is the first that can.

## Finding 6 — ⬜ row C1's third correction carries a half-applied edit

`seal/ledger.md`, row C1, Notes cell.

The sentence reads:

> Re-measured at this branch's tip with the same unbounded instrument, over
> `seal/ledger.md` alone and after every marker this work item writes into it
> — this one and row C2's — was already in place — this one, row C2's, and the
> two that record C3 and C4 being re-read: **429 marker occurrences…**

The aside is there twice and the two copies disagree. An earlier draft named
two markers; the replacement names four; the replacement was appended and the
original was not removed, leaving `was already in place` stranded between
them. The figure after the colon is correct and re-measured, so nothing a
reader acts on is false — but the cell a reviewer is sent to for the
work item's central correction does not parse as a sentence.

## Finding 7 — ⬜ the sibling spec keeps a figure of the same class, three lines under this branch's correction marker

`seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md:95-96`.

*Six commits in this repository's history introduced `Re-read again` into that
file.* No moment, present perfect, and nine by the instrument that produced
the census note's own replacement for the same sentence. The correction marker
this branch added gave the table directly above it the header *when round 2
measured it*, and stopped one paragraph short of the sentence that needed the
same clause. Phase 4's own removal table lists *the census comment's Six
commits…* as removed; the copy in the record it was corrected from was not.

## Finding 8 — ⬜ a second module states a ledger-corpus figure with no moment

`skills/evidence-check/scripts/evidence_check.py:83-85`.

*over all 1520 lines of `seal/ledger.md` and the `seal/ledger/*.md` fragments
the slowest is 0.000533 s*. The file is 2408 lines at the tip and the fragment
glob was empty from `a8bf2a86` until this branch re-created it, so the corpus
named there has moved twice in the same two ways the census note now warns
about.

This is outside the work item's declared scope, which A1 and A4 bound to
`correction_check.py` and to the `404 on 190 rows` spelling, and the timing
conclusion the figure supports is not sensitive to it. It is reported because
`agent-contract` §12 asks for the class rather than the coordinate, and
because the branch has already widened its own scope once on the same
reasoning — `overview.md`'s first divergence row widened A1 from two sites to
four for figures with exactly this shape. Whether that reasoning stops at the
module boundary is the smith's call, not this round's.

## Regression tests to plant

| What it would pin | Destination file |
|---|---|
| `site_row` returns the row's key for an on-row site and the prose note for one outside any row — finding 4, as two asserts inside the census case, adding no case and leaving A11 untouched | `tests/test_a_merge_cannot_silently_drop_a_correction.py` |
| `ledger_corpus` survives a tracked path the worktree has lost, instead of raising — finding 5, as an assert on a corpus built with one path removed from disk, or folded into the fallback itself | `tests/test_a_merge_cannot_silently_drop_a_correction.py` |

No new case is needed for findings 1, 2, 3, 6, 7 or 8: each is a sentence, and
the check that would catch the class is a grep over a kind of claim rather
than a spelling, which is mechanism a fix pass may not add. Naming it as a
`seal/follow-up.md` item is the proportionate answer.

## Facts for the evidence ledger

| Fact | Where it belongs |
|---|---|
| The census note's every digit reproduces at `55ae1b63` from a walk written independently of the branch's: 429 sites against 429 `MARKER` occurrences with none unseen, 426 on 204 rows, 3 in prose, 385 bare, 44 qualified in ten spellings, run lengths 0: 385, 1: 23, 2: 9, 3: 11, 5: 1, bounds 428 / 428 / 429 / 429 / 429 at three, four, five, six and eight | row D4's Verified behavior, as a second instrument agreeing |
| `correction_check.py`'s executable structure is identical across the range once docstrings are removed, so A11's *no exit code, verdict or printed line changes* is verified by construction rather than by reading | the work item's fragment, as the grounds for the no-behaviour-change claim |
| `MARKER`'s gap can never span a date, so an unbounded verb-by-verb walk taking the first date on the line discards nothing `MARKER` could reach — the wideness of the instrument is a property, not only a count that happened to match | row D2's Notes, which currently argues only the consuming form's narrowness |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The module states a corpus figure at three sites, not the one A1 permits, and the docstring's new claim that the census note is the only such site is false. `read_blobs`'s *1.07 MB* is false at the tip, and this branch measured it false in a neighbouring record | `skills/evidence-check/scripts/correction_check.py:559`, `skills/evidence-check/scripts/correction_check.py:377` | open | A1's own grep. Executed: the file is 1,112,008 bytes, which is 1.11 MB or 1.06 MiB; the branch's correction marker in the sibling `plan.md` writes 1.11 MB for the same file |
| 2 | 🟡 The `404 on 190 rows` class is still one site short in code — a third docstring in the edited test module states *185 rows … against `Corrected`'s 10* with no moment | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_merge_that_reverts_a_re_read_row_is_reported` | open | Executed: `grep -c` at the tip gives 203 and 19; by markers, 196 rows and 16. The same pair the branch corrected in ledger row C2 for the same reason |
| 3 | 🟡 The census note's last figure cannot be re-taken from the instrument the note names for the block, breaking the note's own three-clause rule | `skills/evidence-check/scripts/correction_check.py:250` | open | Executed: 9 by `git log -S`, 8 by comparing against every parent, 13 against the first parent. The unbounded walk counts sites, not commits |
| 4 | 🟡 `site_row` is unpinned and the stated grounds do not hold — A11 bounds the case count, and two asserts inside the existing case add no case | `tests/test_a_merge_cannot_silently_drop_a_correction.py#site_row` | open | Executed: replacing its body with `return ""` leaves 50 passed. `agent-contract` §14 — the row clause is promised in the case's docstring and held by nothing |
| 5 | 🟡 The census case's corpus reader raises `FileNotFoundError` on a tracked path the worktree has lost, which is the state a release fold produces before it is staged | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus` | open | Executed: removing the work item's own fragment from disk reddens the case on `FileNotFoundError` rather than on either written guard. `git ls-files` reads the index |
| 6 | ⬜ Row C1's third correction carries a half-applied edit — the marker aside stands twice, the two copies disagree, and `was already in place` is stranded between them | `seal/ledger.md`, row C1 Notes | open | Read. The figure after the colon is correct; the sentence does not parse |
| 7 | ⬜ The sibling `spec.md` keeps *Six commits … introduced `Re-read again`*, three lines under this branch's own correction marker, where the instrument now says nine | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md:95` | open | Executed: 9 by `git log -S` over `seal/ledger.md`. Phase 4's removal table names the same sentence as removed from the census note |
| 8 | ⬜ `evidence_check.py` states *all 1520 lines of `seal/ledger.md`* with no moment, over a corpus that has moved twice — arguably outside this work item's declared scope | `skills/evidence-check/scripts/evidence_check.py:83` | open | Read; 2408 lines at the tip. Reported under `agent-contract` §12, and because the branch already widened A1 once on the same reasoning |
| carried | 🟢 The corpus-moved history claim — `a8bf2a86` folded three fragments into `seal/ledger.md` and deleted them, so #470's prescribed grounds were false before the ticket was read and the grounds replacement is right | `skills/evidence-check/scripts/correction_check.py:220` | verified | Executed: `git ls-tree` at `a8bf2a86^` lists three fragments, at `a8bf2a86` none; the same commit adds 44 rows to the shared file |
| carried | 🟢 Every digit in the census note reproduces at the tip from an instrument written for this round | `skills/evidence-check/scripts/correction_check.py#MARKER` | verified | Executed: 429 / 429 with none unseen, 426 on 204 rows, 3 in prose, 385 bare, 44 in ten spellings, run lengths and bound sweep all exact |
| carried | 🟢 A7's mutation pair, both legs — the bound narrowed to four reddens the case naming file, run length, spelling and row; the bound narrowed **and** the census taken with `MARKER` leaves it green at exit 0 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_bound_covers_every_candidate_marker_site_the_corpus_carries` | verified | Executed by this round, not inherited. The circularity is demonstrated rather than asserted, exactly as A7 asks |
| carried | 🟢 A8's mutation — `for parent in reversed(kin)` reddens exactly the new tie case and leaves the other 49 green | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_tie_falls_to_the_first_parent` | verified | Executed: 1 failed, 49 passed |
| carried | 🟢 The census instrument is genuinely wider than `MARKER` and cannot be it — `MARKER`'s gap can never span a date, so the walk's first-date restriction discards nothing it could reach | `tests/test_a_merge_cannot_silently_drop_a_correction.py#candidate_sites` | verified | Read, plus the executed 429-to-429 bijection with an empty unseen list |
| carried | 🟢 `.github/workflows/hygiene.yml` moved a comment and nothing else | `.github/workflows/hygiene.yml` | verified | Executed: both revisions hash identically with comment lines stripped, at 135 lines each. The file names the sliced literal exactly once, on the run line |
| carried | 🟢 A11's *no exit code, verdict or printed line changes* | `skills/evidence-check/scripts/correction_check.py` | verified | Executed: identical syntax trees across the range once docstrings are removed |
| carried | 🟢 Both survivor exemptions are honest and nothing was reworded to quiet the checker; the second row's grounds re-measure true | `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/survivors.md` | verified | Executed: `survivor-check` reports no standing survivor with no exemption file passed. Exactly one row carries a qualifier on every marker it has, and it is R4 |
| carried | 🟢 Disclosure 8 — `#MARKER` did not drift and `#standing` did, which the frame names nowhere | `skills/evidence-check/scripts/correction_check.py#standing` | verified | Executed: `evidence-check .` reports `1399 ok · 0 drifted · 0 broken`; rows C3 and C4 carry `#standing@89914aad` |
| carried | 🟢 The sibling work item's retained figures reproduce at round 3's own SHA, which is what makes keeping them with a moment safe | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md` | verified | Executed at `31b320e5`: 404 in the file, 401 on 190 rows, 3 in prose, 412 / 412 / 413 across the three ledger files |
| — | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck. The prompt withholds them and `agent-contract` §2 assigns them elsewhere | repository-wide | out of verified scope | The `sealer`, after the rounds settle. Ten test modules were run by the build and two by this round; nothing here speaks for the rest |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py -q`, as shipped | 50 passed — 48 inherited plus the two this work adds, nothing excused, which is A11's case count |
| An independent verb-by-verb census over `seal/ledger.md` at `55ae1b63`, written for this round and reading `VERBS` from the module | 429 candidate sites against 429 `MARKER` occurrences, none unseen; 426 on 204 rows; 3 in prose; 385 bare; 44 qualified in ten spellings with every listed count exact; run lengths 0: 385, 1: 23, 2: 9, 3: 11, 5: 1; bounds 428 / 428 / 429 / 429 / 429; longest run five words in prose; max run on any row three |
| The same census over `seal/ledger.md` and the fragments at `31b320e5`, round 3's SHA | 404 in the file, 401 on 190 rows, 3 in prose; 412 / 412 / 413 across the three files at bounds of three, four and five — round 3's figures reproduce exactly |
| A7 leg 1 — `MARKER`'s bound narrowed to `{0,4}`, census case alone | Red. `1 of 429 candidate marker site(s) fall outside the bound on MARKER's qualifier`, naming the file, a run of 5, the spelling and `on row '(prose, outside any row)'` |
| A7 leg 2 — the same narrowed bound **and** the census rewritten to walk `MARKER` | Green, exit 0. The circular census reproduced on demand |
| A8 — `examine`'s parent walk changed to `reversed(kin)`, whole module | 1 failed, 49 passed; the tie case is the one that reddens |
| `site_row`'s body replaced with `return ""`, whole module | 50 passed — the row clause of the failure message is held by nothing |
| The work item's ledger fragment removed from the worktree without staging, census case alone | Red on `FileNotFoundError` out of the corpus reader, not on either written guard |
| `bin/evidence-check .`, unscoped, no `--reverify` | exit 0. `1399 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `1 work item read · 95 unread · 0 refused` |
| `bin/correction-check --range f4232014...HEAD` and `--range origin/release/v0.12.3...HEAD` | exit 0 both. No merge commit in either range, so no correction can have been dropped at one |
| `bin/survivor-check --range f4232014...HEAD --exempt …/survivors.md`, and again with no exemption file | exit 0 both. No removed wording is still standing, so both exemption rows are dormant at the tip as `survivors.md` says |
| `bin/test tests/test_no_real_identifiers.py -q` | 5 passed — the branch's new prose carries no real identifier |
| Both revisions of `.github/workflows/hygiene.yml`, comment lines stripped and hashed | Identical, 135 lines each — comment-only, no step or command moved |
| Both revisions of `correction_check.py` parsed and dumped with docstrings removed | Identical syntax trees — A11's behaviour claim verified by construction |
| `uvx ruff check` and `ruff format --check` on the two touched source files | All checks passed; 2 files already formatted |
| Commits introducing `Re-read again` into `seal/ledger.md`, three instruments | 9 by `git log -S`, 8 against every parent, 13 against the first parent |
| `git ls-tree a8bf2a86^ -- seal/ledger/` and `git ls-tree a8bf2a86 --` | Three fragments before, none after — the fold and the deletion are one commit |
| Rows of `seal/ledger.md` whose every marker carries a qualifier | Exactly one, R4 — `survivors.md`'s second grounds cell re-measures true |
| The broad gate — full suite, repository-wide lint, typecheck | not yet. Withheld from this round by the prompt and by `agent-contract` §2; the `sealer` is the answerer |

Every probe file this round wrote was deleted before it handed over, and every
mutation was restored and the restoration compared byte for byte. The clone
the round read in is outside the repository and holds nothing the tree needs.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Q1 — whether this branch may amend the released `CHANGELOG.md` §0.12.2, which still carries the false figure while the fragment beside it does not | `questions.md` Q1, `overview.md` §*Not verified*, `seal/follow-up.md`, and `survivors.md`'s first row. Already deferred by the build, and the divergence is disclosed four ways | the repository owner |
| Q2 — #469's issue body, whose histogram is neither corpus and sums to 412 | `questions.md` Q2 and `overview.md` §*Not verified*. Already deferred; `agent-contract` §6 withholds posting from every agent | the repository owner, or the orchestrator |
| The `test_a9_the_leg_asks_the_range_the_pull_request_is_about` slice on a bare literal, which any comment naming the script redirects | `overview.md` §*Not verified*. Already deferred by the build, with the right reading — it failed in the safe direction and a fix is mechanism a fix pass may not add | the repository owner, as an issue from this pull request |

## Paste-ready fixes

Finding 1, first site — `skills/evidence-check/scripts/correction_check.py`,
`read_blobs`'s docstring:

```python
    One `git cat-file --batch` for every blob the walk needs rather than one
    `git show` per file per commit. The shared ledger here runs to about a
    megabyte and a range can hold dozens of merges; the difference is the run.
    No measured size stands here: the file grows at every release, and the
    census note beside `MARKER` is the one site in this module that states a
    figure about the corpus.
```

Finding 1, second site — the same file, `standing`'s docstring:

```python
    still stands, which is A3 broken by the identity that runs first. Latent
    when round 1 measured it -- no marked row shared a key -- and not
    unreachable: `seal/ledger.md` repeats its section table headers, so well
    over a hundred of its rows carry one of two first cells.
```

Finding 2 — `tests/test_a_merge_cannot_silently_drop_a_correction.py`:

```python
def test_a_merge_that_reverts_a_re_read_row_is_reported(tmp_path):
    """A2, and it is red separately from A1 so a check watching one verb
    cannot pass both. `Re-read` is much the commoner marker in the shared
    file and `Corrected` the rare one; the counts are in the module's census
    note, which is the one site that states them and names the corpus, the
    instrument and the moment each is true of."""
```

Finding 3 — `skills/evidence-check/scripts/correction_check.py`, the last
sentence of the census block:

```python
# all, so losing one at a merge reported nothing. And the qualifier is not a
# one-off somebody can be asked to stop writing: nine commits in this
# repository's history have introduced `Re-read again` into that file --
# a figure taken with `git log -S'Re-read again' -- seal/ledger.md` rather
# than with the walk above, which counts sites in a file and not commits.
```

Finding 4 — the same test module, two asserts at the head of the census case,
after its docstring and before `corpus = ledger_corpus()`. No case is added:

```python
    # The `row` clause of the failure message below, pinned. It reaches a
    # reader only through a message no standing case builds, so without these
    # two lines `site_row` can be edited away with the module still green.
    on_a_row = "| R1 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. | n |"
    assert site_row(on_a_row, on_a_row.index("Re-read")) == cc.Row(on_a_row).key
    assert site_row("Re-read 2026-09-05.", 0) == "(prose, outside any row)"
```

Finding 5 — the same test module, the tail of `ledger_corpus`:

```python
    paths = [p for p in listed.split("\0") if p.endswith(".md")]
    corpus = {}
    for p in paths:
        path = pathlib.Path(ROOT, p)
        if path.exists():
            corpus[p] = path.read_text(encoding="utf-8")
            continue
        # Tracked and gone from the worktree: what a release fold looks like
        # between removing the fragments and staging the removal. Read the
        # index blob `git ls-files` just listed rather than crashing on it.
        corpus[p] = subprocess.run(
            ["git", "-C", ROOT, "show", f":{p}"],
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout
    return corpus
```

Finding 6 — `seal/ledger.md`, row C1's Notes cell. Replace

```
after every marker this work item writes into it — this one and row C2's — was already in place — this one, row C2's, and the two that record C3 and C4 being re-read:
```

with

```
after every marker this work item writes into it — this one, row C2's, and the two that record C3 and C4 being re-read — was already in place:
```

Finding 7 — `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md`:

```markdown
spelling, so it was invisible to the check entirely. Nine commits in this
repository's history have introduced `Re-read again` into that file, measured
at the tip of the branch for #469, #470 and #471 with `git log -S`; it was
stated as six here, with no moment and no instrument.
```

Finding 8 — `skills/evidence-check/scripts/evidence_check.py`, if the smith
takes it rather than deferring it:

```python
# near it: over the whole of `seal/ledger.md` and the `seal/ledger/*.md`
# fragments the slowest is well under a millisecond, on the longest row in
# the corpus, and the rows of 1150-1280 characters are faster still. No
# measured line count stands here: the corpus grows at every release.
```

## Proof block

Files opened this round, all in a clone of the repository at `55ae1b63`:

- `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/` —
  `spec.md`, `plan.md`, `questions.md`, `routing.md`, `overview.md`,
  `survivors.md`, `changelog.md`, `phases/phase-1.md` … `phases/phase-4.md`
- `skills/evidence-check/scripts/correction_check.py`, whole file and the
  full range diff
- `tests/test_a_merge_cannot_silently_drop_a_correction.py`, the full range
  diff and the new cases in place
- `.github/workflows/hygiene.yml`, both revisions
- `seal/ledger.md` rows C1–C9 and the whole file as corpus;
  `seal/ledger/1789996780-the-census-and-the-tie-that-nothing-holds.md`
- `seal/follow-up.md`, the added row and its neighbours
- `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/`
  — `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`, the
  full range diff of all five
- `skills/code-review/SKILL.md` §*Findings format*;
  `docs/review-chain-spec.md` §*The last round verifies*
- `skills/evidence-check/scripts/evidence_check.py:78-92`
- `CONTRIBUTING.md`, the test-runner section
- `CLAUDE.md`, both the repository's and the user's

Not opened: the rest of the suite, the remaining skills, and every
`rounds/round-N.md` of work item 1789969379 beyond the figures this round
grepped for — round 3's findings were re-derived from the tree rather than
read as verdicts.

**How the two lines below read.** Findings 6 and 7 are located in records, so
`docs/review-chain-spec.md` §*The last round verifies* makes them corrections
rather than fixes and `Needs a fix` does not count them; finding 8 is a ⬜
note. Finding 5 crashes a test helper in a state a release produces rather
than crashing the tool, and no finding leaves a record outside the root, so
the floor below is `no`.

Needs a fix: yes — findings 1, 2, 3, 4 and 5
Loses a record or crashes: no

