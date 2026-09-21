# 1789996780-the-census-and-the-tie-that-nothing-holds — review round 1

| Field | Value |
|---|---|
| Target SHA | 55ae1b63 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 480 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `f6ba0cfc7c71d8fe69ab4dfa42ab98f022e8cdc4..e3cba362708bc458984e783bc18c64ab30f140fc`, 7 commits |
| Contract changes | none |
| New units | ledger_text (depth 1) |
| Needs a fix | yes — findings 1, 2, 3, 4 and 5 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

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

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The module states a corpus figure at three sites, not the one A1 permits, and the docstring's new claim that the census note is the only such site is false. `read_blobs`'s *1.07 MB* is false at the tip, and this branch measured it false in a neighbouring record | `skills/evidence-check/scripts/correction_check.py:559`, `skills/evidence-check/scripts/correction_check.py:377` | **fixed** `0c3b49b6` | fixed at 0c3b49b6; A1's own grep. Executed: the file is 1,112,008 bytes, which is 1.11 MB or 1.06 MiB; the branch's correction marker in the sibling `plan.md` writes 1.11 MB for the same file |
| 2 | 🟡 The `404 on 190 rows` class is still one site short in code — a third docstring in the edited test module states *185 rows … against `Corrected`'s 10* with no moment | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_merge_that_reverts_a_re_read_row_is_reported` | **fixed** `8efdf41b` | fixed at 8efdf41b; Executed: `grep -c` at the tip gives 203 and 19; by markers, 196 rows and 16. The same pair the branch corrected in ledger row C2 for the same reason |
| 3 | 🟡 The census note's last figure cannot be re-taken from the instrument the note names for the block, breaking the note's own three-clause rule | `skills/evidence-check/scripts/correction_check.py:250` | **fixed** `35b140b4` | fixed at 35b140b4; Executed: 9 by `git log -S`, 8 by comparing against every parent, 13 against the first parent. The unbounded walk counts sites, not commits |
| 4 | 🟡 `site_row` is unpinned and the stated grounds do not hold — A11 bounds the case count, and two asserts inside the existing case add no case | `tests/test_a_merge_cannot_silently_drop_a_correction.py#site_row` | **fixed** `3764b97a` | fixed at 3764b97a; Executed: replacing its body with `return ""` leaves 50 passed. `agent-contract` §14 — the row clause is promised in the case's docstring and held by nothing |
| 5 | 🟡 The census case's corpus reader raises `FileNotFoundError` on a tracked path the worktree has lost, which is the state a release fold produces before it is staged | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus` | **fixed** `10459bfd` | fixed at 10459bfd; Executed: removing the work item's own fragment from disk reddens the case on `FileNotFoundError` rather than on either written guard. `git ls-files` reads the index |
| 6 | ⬜ Row C1's third correction carries a half-applied edit — the marker aside stands twice, the two copies disagree, and `was already in place` is stranded between them | `seal/ledger.md`, row C1 Notes | **fixed** `e3cba362` | fixed at e3cba362; Read. The figure after the colon is correct; the sentence does not parse |
| 7 | ⬜ The sibling `spec.md` keeps *Six commits … introduced `Re-read again`*, three lines under this branch's own correction marker, where the instrument now says nine | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md:95` | **fixed** `e3cba362` | fixed at e3cba362; Executed: 9 by `git log -S` over `seal/ledger.md`. Phase 4's removal table names the same sentence as removed from the census note |
| 8 | ⬜ `evidence_check.py` states *all 1520 lines of `seal/ledger.md`* with no moment, over a corpus that has moved twice — arguably outside this work item's declared scope | `skills/evidence-check/scripts/evidence_check.py:83` | **fixed** `60d4f1a6` | fixed at 60d4f1a6; Read; 2408 lines at the tip. Reported under `agent-contract` §12, and because the branch already widened A1 once on the same reasoning |
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

## Paste-ready fixes

```python
    One `git cat-file --batch` for every blob the walk needs rather than one
    `git show` per file per commit. The shared ledger here runs to about a
    megabyte and a range can hold dozens of merges; the difference is the run.
    No measured size stands here: the file grows at every release, and the
    census note beside `MARKER` is the one site in this module that states a
    figure about the corpus.
```
```python
    still stands, which is A3 broken by the identity that runs first. Latent
    when round 1 measured it -- no marked row shared a key -- and not
    unreachable: `seal/ledger.md` repeats its section table headers, so well
    over a hundred of its rows carry one of two first cells.
```
```python
def test_a_merge_that_reverts_a_re_read_row_is_reported(tmp_path):
    """A2, and it is red separately from A1 so a check watching one verb
    cannot pass both. `Re-read` is much the commoner marker in the shared
    file and `Corrected` the rare one; the counts are in the module's census
    note, which is the one site that states them and names the corpus, the
    instrument and the moment each is true of."""
```
```python
# all, so losing one at a merge reported nothing. And the qualifier is not a
# one-off somebody can be asked to stop writing: nine commits in this
# repository's history have introduced `Re-read again` into that file --
# a figure taken with `git log -S'Re-read again' -- seal/ledger.md` rather
# than with the walk above, which counts sites in a file and not commits.
```
```python
    # The `row` clause of the failure message below, pinned. It reaches a
    # reader only through a message no standing case builds, so without these
    # two lines `site_row` can be edited away with the module still green.
    on_a_row = "| R1 · a claim | `a/b.py#f@11111111` | Re-read 2026-09-05. | n |"
    assert site_row(on_a_row, on_a_row.index("Re-read")) == cc.Row(on_a_row).key
    assert site_row("Re-read 2026-09-05.", 0) == "(prose, outside any row)"
```
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
```
after every marker this work item writes into it — this one and row C2's — was already in place — this one, row C2's, and the two that record C3 and C4 being re-read:
```
```
after every marker this work item writes into it — this one, row C2's, and the two that record C3 and C4 being re-read — was already in place:
```
```markdown
spelling, so it was invisible to the check entirely. Nine commits in this
repository's history have introduced `Re-read again` into that file, measured
at the tip of the branch for #469, #470 and #471 with `git log -S`; it was
stated as six here, with no moment and no instrument.
```
```python
# near it: over the whole of `seal/ledger.md` and the `seal/ledger/*.md`
# fragments the slowest is well under a millisecond, on the longest row in
# the corpus, and the rows of 1150-1280 characters are faster still. No
# measured line count stands here: the corpus grows at every release.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Q1 — whether this branch may amend the released `CHANGELOG.md` §0.12.2, which still carries the false figure while the fragment beside it does not | `questions.md` Q1, `overview.md` §*Not verified*, `seal/follow-up.md`, and `survivors.md`'s first row. Already deferred by the build, and the divergence is disclosed four ways | the repository owner |
| Q2 — #469's issue body, whose histogram is neither corpus and sums to 412 | `questions.md` Q2 and `overview.md` §*Not verified*. Already deferred; `agent-contract` §6 withholds posting from every agent | the repository owner, or the orchestrator |
| The `test_a9_the_leg_asks_the_range_the_pull_request_is_about` slice on a bare literal, which any comment naming the script redirects | `overview.md` §*Not verified*. Already deferred by the build, with the right reading — it failed in the safe direction and a fix is mechanism a fix pass may not add | the repository owner, as an issue from this pull request |
