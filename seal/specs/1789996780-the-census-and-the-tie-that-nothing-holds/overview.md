# 1789996780-the-census-and-the-tie-that-nothing-holds — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789996780-…/spec.md` A1–A11; `plan.md` four phases
            and §*Alternatives considered*; `questions.md` Q1–Q6;
            `CLAUDE.md` §*A ledger coordinate names content, never a
            position*, §*A change writes fragments, never the shared file*;
            `CONTRIBUTING.md` §*House rules*;
            `skills/agent-contract/SKILL.md` §§1, 2, 4, 5, 7, 9, 12, 14, 15;
            `seal/specs/1789969379-…/rounds/round-3-report.md` findings 9, 10
            and 11 with their paste-ready fixes, and `round-2-report.md`
            finding 6; issues #469, #470, #471;
            `git show fix/the-gate-states-what-its-own-fixes-disproved:…/spec.md`
            §*The correction marker*
· evidence: `seal/ledger/1789996780-the-census-and-the-tie-that-nothing-holds.md`
            D1, D2, D3, D4 — new. `seal/ledger.md` C1 corrected a third time,
            C2 corrected, C3 and C4 re-read by hand and re-stamped
· verified: executed — the unbounded census at four SHAs, the two new cases
            seen red then green, three mutations (`examine`'s parent walk
            reversed, `MARKER`'s bound narrowed to four, and the bound
            narrowed with the census taken by `MARKER`), ten test modules,
            `evidence-check` and `--reverify`, `survivor-check` twice,
            `correction-check`, and `ruff check` / `ruff format --check` over
            the two touched source files. Read — the six record sites of A4,
            the two ledger rows read by hand before `--reverify`, and round
            3's report in full. Unverified — the full suite, the
            repository-wide lint and the typecheck, which are the `sealer`'s
            one broad run

## Why this work exists

`correction_check.py` stated two arithmetically false measurements about the
corpus it watches and half of its parent-naming rule was held by nothing, so
the check that exists to stop a false claim shipping was itself shipping two.

## What the frame got wrong, found before anything was built

**`#MARKER` does not drift when the comment above it is rewritten.** Q3's
default was *assume `#MARKER` may drift*, and `spec.md`'s Data & interfaces
row asks the same question. Measured: the anchor covers the assignment
statement alone, lines 289–293 at this tip, so rewriting the whole census note
left `skills/evidence-check/scripts/correction_check.py#MARKER@17486986`
unchanged and `--reverify`
re-stamped it to the hash it already had. The only coordinate this work
drifted in `seal/ledger.md` is `#standing`, which the frame did not name at
all, because the work reached a docstring the spec's surface table does not
list.

**The frame's own `spec.md` failed `evidence-check` at exit 2.** Two cells of
its Data & interfaces table wrote the `#MARKER` and `#examine` coordinates
with the bare file name and no path, and the records arm reads a backticked
coordinate-shaped token as a live claim wherever it stands. Both came back
BROKEN — *file not found — identical content at
skills/evidence-check/scripts/correction_check.py#MARKER (moved?)*. Both cells
now carry the full path and the arm reports `0 refused`.

**Round 3's list of six sites was three short, and two of the three were live
false statements rather than moved ones.** `spec.md` A4 anticipated that the
list had aged and asked for the class to be enumerated by construction, which
is what found them: `.github/workflows/hygiene.yml`, work item 1789969379's
`questions.md`, and its `spec.md` all stated a figure the list does not name.
Two more arrived from `survivor-check` rather than from the grep — ledger row
C2's claim cell and row C4's Notes — because they state the same class of fact
in different words.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How wide A1's *one census site* reaches inside the module | `spec.md` §*Data & interfaces* lists the module docstring and the census note. A1's verification is a grep over the **whole file** | Four further sites corrected. Two in the build: the `SIZE_CAP` comment's *the shared file in this repository is 1.07 MB* and `standing`'s docstring *123 rows carrying one of two first cells*. Two more in the fix pass for round 1's finding 1, which found the widening had itself stopped short: `read_blobs`'s docstring kept *1.07 MB*, and `standing`'s kept *0 of 189 marked rows* | Both are figures about the corpus stated in the present tense with no moment, and both were already stale — the file is 2408 lines and 126 rows share a first cell at this tip. Leaving two false statements about the corpus inside the module this work item exists to make true would be the class closed one name short for the fourth time in this lineage (`agent-contract` §12). Neither is re-measured: both are reworded to a proportion that survives a release, so no new figure is created to drift |
| Whether work item 1789969379's records take the tip's figures or their own | A6 says the digits are re-measured at the branch tip and never restated from the report; A4 says every present-state site is corrected | The **ledger rows** take the tip's figures. The **SDD records** keep round 2's and round 3's figures and gain the moment they were taken at | A record of a past work item that states the present corpus is a record that goes stale at the next release, which is the defect rather than the repair. Round 3's figures were not inherited from its prose — they were re-measured at `31b320e5` with this work's own instrument and reproduce exactly: 404 in the file, 401 on 190 rows, 3 in prose, and 412/412/413 across the three fragments (`agent-contract` §5) |
| The test module's census comment stated two totals | Phase 2 committed *the consuming form found 423 candidate sites where `MARKER` matched 425* | Restated as *two candidate sites fewer than `MARKER` matched* | The defect is the difference between two instruments over one file, and the two totals are figures over a corpus this very branch then moved twice. Stating the difference makes the sentence permanently true and removes a site that would have needed correcting again in phase 4 — the same judgment the work item is about, applied to its own phase 2 |
| The census walk's shape | Neither `spec.md` nor #469 says how the unbounded walk is written; #469 gives it as *for every verb, find the next date on the same line* | Walked verb by verb with no single regular expression spanning the two | The one-expression form is what #469's words read like, and it is wrong: `finditer` does not overlap, so a first verb whose gap is not a lowercase run consumes a second verb standing before the date and drops its site. It found two fewer sites than `MARKER` matches, so the instrument built to be strictly wider than the pattern under test was narrower than it |
| The tie case's fixture carries a difference the paste-ready text does not explain | Round 3's fixture differs between `ours` and `theirs` only in the last cell | Kept verbatim, and the reason is recorded in `phases/phase-1.md` | Without that cell the two parents' texts are identical, git finds no conflict, and the fixture stops constructing a tie at all. The case would still pass and would be testing nothing, which is the shape §15 exists to catch |

## What the broad gate found, and the one commit after it

The sealer's run came back **NOT SEALED, exit 1**, one file red out of 3955
cases and labelled `new` because it passes 17/17 at the base:
`tests/test_a_shrunken_corpus_declines_to_judge.py`, both
`test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard` and
`test_an_unguarded_scope_is_named_although_a_module_is_mid_edit`.

> AssertionError: the suite derives a path list from git in
> `['tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus']`
> that this case does not account for. Classify it: it either applies
> `on_disk`, or it belongs in one of the five tables above with the grounds a
> reader can weigh

`ledger_corpus` is the helper this work item wrote for round 1's finding 5,
and that case exists to catch exactly the seventh instance of the class it
enumerates. **It caught ours.** The whole shape is this work item's own
subject arriving from the other side: an enumeration that holds because
something re-derives it rather than because somebody remembered.

**The message offered two routes and only one of them was true.** The
tempting one was the table — `CONTENT_FROM_GIT`, whose grounds nothing
re-checks, and which the code would have fitted: `git ls-files` names the
path and `git show :<path>` reads the same index entry, so there is no tree
state where the name exists and the content does not. Taking it would have
been classifying around the finding. Applying the shared predicate was both
the honest route and the better code, because the bespoke test this helper
had written for itself was **wrong in a state the shared one handles**:

- `pathlib.Path.exists()` is **true of a directory**. A tracked path that is
  now a directory took the worktree route and `read_text` raised
  `IsADirectoryError` — the same crash class finding 5 was about, one tree
  state over, reintroduced by the fix for it.
- `conftest.on_disk` asks `os.path.isfile`, and
  `test_a_directory_on_the_list_is_not_a_file_that_is_there` is the case that
  pins it. Five helpers already share that predicate; this made a sixth
  copy of it and got it wrong.

So `ledger_corpus` now splits its listing with `conftest.on_disk` and is
classified in `APPLIES_THE_SHARED_GUARD`, where the case re-checks the code
rather than reading a row. What it does with the missing half is **neither of
the two dispositions that module describes**: it does not skip them, which
would shrink the corpus the census is taken over without a word, and it does
not decline, because it has somewhere true to read them from. It reads the
index entry `git ls-files` just named.

Three things said plainly, because the commit lands after the rounds closed:

- **The red was seen first**, by the gate and then again here before anything
  was edited: 2 failed, 15 passed, both messages quoted above.
- **Both failing cases are satisfied by one classification**, not by two
  accommodations. The second reads the same table from the other side — it
  thins one module out of the enumeration and asserts that only a planted key
  is unaccounted — so a row in `PATH_LIST_CALLS` is what closes both, and
  `ledger_corpus` is in it exactly once.
- **It ships unreviewed.** Round 2 was the verifying round and the run's one
  reopening is spent, so no reader opened this. What a reader would weigh:
  whether `APPLIES_THE_SHARED_GUARD` is the right table when this caller's
  disposition for the missing half is a third one the module's docstring does
  not describe, and whether reading a missing file from the index is right at
  all for a case whose subject is the corpus as it stands. The argument for
  both is that the census must be taken over the whole corpus or it is the
  vacuous green A7 exists to refuse.

**What the gate did not answer.** `uvx ruff check .` and `uvx ruff format
--check .` never ran: the repository's `Broad gate` row is one `&&` chain and
`bin/test` short-circuited it, so repository-wide lint and format have no
result on this branch. Both were run here on the two touched files and pass;
the repository-wide pair is the sealer's re-take.

## Not verified

| Item | Who must answer |
|---|---|
| **Q1 — whether this branch may amend the released `CHANGELOG.md` §0.12.2**, which carries the same false figure at `CHANGELOG.md:121`. The default was built: the section is left, the work item's changelog fragment beside it is corrected, and the two now diverge. `gather_changelog.py` decides by marker and never by content, so a corrected fragment is never re-gathered and nothing downstream can see the divergence. **The same answer governs work item 1789996775's Q1** about a different sentence in the same released section, and that row is still ⬜ on `fix/the-gate-states-what-its-own-fixes-disproved` | the repository owner |
| **Q2 — #469's issue body**, whose histogram counts its `0 words` row over the three ledger files and its `1 word` row over `seal/ledger.md` alone, so it sums to 412 and is neither corpus. `agent-contract` §6 withholds posting from every agent, so no agent can repair a ticket however clear the answer. The tree is made true instead and the error is named here. The conclusion the histogram supports — there is no run of four — is unchanged on either corpus and is re-measured true at this tip | the repository owner, or the orchestrator |
| ✅ **The full suite, the repository-wide lint and the typecheck.** The `sealer`'s second run answered all three: `broad-gate --base release/v0.12.3 --record …` at `af56a9da` against `8531c858` — **SEALED, exit 0**, eight arms. The `&&` chain ran to its end this time and `suite.txt` carries three distinct answers rather than one: `3955 passed, 9 skipped` in 11m54s, then `All checks passed!` and `154 files already formatted`. The ledger, chain, seal, mode, corrections, survivors and unverified arms each exited 0. **The first run did not answer the lint half at all** — it came back NOT SEALED on one failing file and the `&&` chain short-circuited before either ruff command, which is why the section above says what the gate did not answer as well as what it did | answered by the `sealer`'s second run; the first run's refusal and the commit that cleared it are the section above |
| ✅ **Whether the `row` clause of the census case's failure message stays correct.** Every unit this work added was mutated one at a time. Breaking `ledger_corpus` to return `{}` and breaking `candidate_sites` to return `[]` each turn the case red on its own guard, so A7's *refuses to pass over an empty corpus* is real rather than declared. Breaking `site_row` to return `""` leaves the case **green**: its output reaches a reader only through the failure message, which no standing case exercises. It is verified by execution — the bound-narrowed-to-four mutation printed `on row '(prose, outside any row)'`, and ledger row D1 records it — but pinning it needs a case that asserts a failure, and `spec.md` A11 says this module grows by exactly the two cases. Relaxing A11 is not `smith`'s call | ✅ **closed by round 1's finding 4, and the reasoning above was wrong.** A11 bounds the number of CASES, not the number of things a case establishes. Two asserts inside the census case that already exists pin `site_row`: no case added, A11 untouched, nobody's call to relax. The measurement was honest and the grounds were not. Fixed at `3764b97a`, seen red first — with the asserts in place and `site_row` returning `""`, the case fails where it passed |
| **Whether `.github/workflows/hygiene.yml`'s correction-check leg can survive a comment that names the script.** `test_a9_the_leg_asks_the_range_the_pull_request_is_about` slices the workflow on the bare literal `correction_check.py`, so any comment mentioning the file by name silently redirects the slice and the case fails on text that is correct. It caught this work's first edit, which is the right direction to fail in; the fragility is latent and a fix is mechanism a fix pass may not add | the repository owner, as an issue from this pull request |

## What was fed back into the spec

Four facts this work measured that no document held, all in the ledger
fragment as D1–D4 and marked here as *inferred during implementation* so a
later planner may overturn them:

- **The census instrument cannot be written as one expression**, for a reason
  that has nothing to do with the bound (D2).
- **The five-word run the bound exists to admit stands in the file's prose,
  and no table row carries a qualifier longer than three words** (D4). Three
  review rounds argued about the bound without ever taking that split, so the
  survival test would return the same verdicts today at a bound of three. The
  bound is deliberately not narrowed, and the census note now says why.
- **The tie behaviour is a property of `max` over a dict in insertion order**,
  which is to say the sentence a person acts on was held by an implementation
  detail of a builtin and by nothing written down (D3).
- **`#MARKER`'s anchor covers the assignment and not the comment above it**,
  which is what makes a census note rewritable without re-stamping every row
  that cites it.
