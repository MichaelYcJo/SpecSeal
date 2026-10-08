# Round 1 report — 1791384160, a fix range is its own commits across a merge

Reviewed by warden at `7e68ed00f83d53a36ffdd6e2347e015b8f0d1168`, diff
`origin/release/v0.21.0...7e68ed00` (base tip `5623d728`), in a `--no-local`
clone. No earlier rounds, so nothing is carried.

## How the findings relate

```
🔴 1  the pull request's CI is red: the S10 case lists paths from git,
      and the suite-wide guard on that is not told about it
🟡 2  the rule's home says a merged-in commit "descends from `a` never";
      two shapes break that, and the limit paragraph names neither
⬜ 3  own_units reads files `measure` never reads, and own_commits runs twice
⬜ 4  a Contract changes entry can be a sibling's signature change
⬜ 5  one pronoun in orchestration.md now points at a document
```

The code change itself holds up. `own_commits`, the two refusals in `close`,
the `-z` parsers and `-I` survived every probe I ran. The one blocking
finding is in the test suite, not in the scripts.

## Stage 1 — spec compliance

Every reader that `spec.md` §*In* lists imports one reading, and
`walk_tip` and `commits_after` are gone. Nothing outside the release files and
`.test_durations` still names them (`git grep`, read). S1–S10 and S12 each
have a case in the diff. I did not re-run S11 or S13. The orchestrator ran the
five modules (427 passed), and the smith reports `evidence-check --strict` at
exit 0. Both are their claims, not runs of mine.

The account says "every new case red before the fix". I did not re-check
that. The phase records and the ledger rows name the SHA each case went red
at, and that matches the commit order (`38d96e95` → `9a1fbcae`,
`4e849e50` → `e536b92a`).

## 🔴 1 — The S10 case breaks a suite-wide guard, and CI is red on two legs

`tests/test_the_fixes_close_the_record.py:1355`
(`test_a_path_git_would_quote_is_read_as_the_path_it_is`) runs
`git ls-tree -r --name-only` to check that git quotes the fixture's name.
`tests/test_a_shrunken_corpus_declines_to_judge.py` lists every scope in the
suite that derives a path list from git (`LISTS_PATHS` holds `ls-tree`).
Each such scope must be classified in one of its tables. This one is not.

- Executed by CI on PR #878: `pytest (ubuntu-latest)` fails with
  `2 failed, 12758 passed`. `pytest (windows-latest, group 2)` fails with
  `2 failed, 6692 passed`. Both failures are
  `test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard` and
  `test_an_unguarded_scope_is_named_although_a_module_is_mid_edit`, and each
  names the S10 case.
- Executed by me in the clone at the target SHA:
  `bin/test tests/test_a_shrunken_corpus_declines_to_judge.py`, exit 1, the
  same 2 failures. With the fix below applied in the clone, exit 0 and 17
  passed. The edit was then reverted.

Why it matters: the pull request cannot merge on red. The smith's narrow
runs and the orchestrator's five modules both left this module out, because
it reads the whole suite rather than the scripts.

The case lists a repository it built itself, which is what `LISTS_A_FIXTURE`
is for. Nothing it lists is opened. The class is one scope wide: CI names no
other new case, and no other new case calls `ls-tree`, `ls-files` or
`--name-only` (read).

## 🟡 2 — The home says a merged-in commit never descends from `a`, and two shapes say otherwise

`docs/the-record-layout.md:120-122` says: "A commit that a merge brought in
reaches `b` only through the merge and descends from `a` never". The limit
paragraph at line 143 names only the conflict resolution. Two shapes break
the sentence. I built both in a probe and ran `own_commits` on them.

- **A base that merged the item's commits with a merge commit** (a
  back-merge, or a stacked branch merged first). Any sibling commit made on
  the base after that merge descends from `a`. When the item merges the base
  again, `own_commits(T, HEAD)` returned `['f1', 'S(sibling)', 'f2']`. The
  sibling's commit is owned, and its units reach `New units`.
- **An own commit on a topic forked before `a` and merged after it.**
  `own_commits(T, HEAD)` returned `['f']` and left out the topic's fix, and
  `touched` returned `['own.py']` without `topic.py`. That fix's units drop
  out of the surface without a word, and a `fixed` row naming it is refused.

Why it matters: this repository squashes into its release branch, so the
first shape cannot happen here. The overview's last divergence row says so.
But the plugin ships this rule to repositories that merge with merge commits,
and there the policy document states a guarantee the code does not give.
`docs/the-record-layout.md` is the rule's one home (rule 17 of
`tests/test_the_rules_have_one_owner.py`). The overview's divergence row
chose "the home stating descent only". The home states "never" instead.

The same overclaim appears in more places (§12):

- `docs/the-record-layout.md:100-101`, the fragment section: "the base's
  commits descend from round 1's target never"
- `skills/code-review/scripts/chain_check.py:4493-4496`, the `own_commits`
  docstring
- `skills/code-review/scripts/chain_check.py:4560-4563`, the
  `fragment_left_behind` docstring
- the fragment's `S7, S8, S9` row: "A commit a merge brought in is owned on
  neither side of the merge"
- the `Corrected · S2, S3, S4, S6` row: "because they descend from round 1's
  target never"

The fix states the limit once, in the home, and has the other places say
"in a repository that squashes into its base" or link the home. The code
does not change.

## ⬜ 3 — `own_units` reads files `measure` never reads, and `own_commits` runs twice

`skills/code-review/scripts/round_record.py:2384`. `commit_units` runs
`git show` at the parent for every path of every own commit. For a
non-Python path it also runs `git diff`. Prose files (`PROSE_SUFFIXES`,
line 2999) are included, though `measure` skips them whole, so no entry from
them can ever pass the filter. A fix range is mostly records and ledger rows,
so most of these subprocesses buy nothing. Also, `close` calls `own_commits`
at line 4422, `touched` calls it again at line 3400, and `fix_pass_units`
does the same at lines 2355-2356. This is cost, not a defect.

## ⬜ 4 — A sibling's signature change can still be listed as this round's contract change

`skills/code-review/scripts/round_record.py:4450`. `changed` comes from
`measure`, which compares contracts. The filter only asks whether an own
commit changed the unit's `ast.dump`. Suppose an own commit edits only the
body of `f`, and a merged sibling changes `f`'s parameters. Then
`Contract changes` lists `f`, and the verifying round reviews a signature the
item never wrote. The home's sentence ("keeps … only a unit that an owned
commit added or changed") is true as written. The consequence is just not
said anywhere. Read only, not probed.

## ⬜ 5 — "It refuses depth 2" now points at a document

`skills/code-review/orchestration.md:372`. The new sentence before it has
`docs/the-record-layout.md` §… as its subject. So "It refuses depth 2 before
writing any cell" now reads as the document refusing. Write
"`close` refuses depth 2" there.

## Answers to the attack list

1. **`own_commits`** (executed, probe):
   - A start that is a merge gives the right list.
   - An empty range `a..a` gives `[]`.
   - A rebase that moved the start gives `[]`, and `parse_range` refuses it.
   - A fix cherry-picked from a sibling is a new commit that descends from
     `a`, so it is owned. That is right: it is the branch's commit.
   - A criss-cross or back-merge names the sibling. A topic forked before
     the start drops the item's commit. Both are 🟡 2.
2. **The two refusals** (read): `parse_range` runs at
   `round_record.py:4370`. The guard runs at lines 4422-4443. The record is
   first written after line 4516, so both refuse with nothing written. Two
   legitimate ranges trip them:
   - A branch rebased between the review and the fix. The message says to
     name the commit the fixes started from, and `chain_check.fix_range` does
     not compare the start with `Target SHA` (read).
   - A fix made on a topic forked before the start. This is 🟡 2's second
     shape.
3. **The divergences:**
   - `own_units`' return shape is sound. `unit_adders` needs to know which
     commit added a unit as opposed to changed it (read).
   - Intersecting `touched` with the paths `b` carries is sound. A path a
     merge deleted after an own change has no units at `b` to name (read).
   - `-I` drops nothing the old code read (executed). Without `-I`, git
     already reported a file marked `binary` in `.gitattributes` as
     `Binary file … matches`, and the old `:` split read that line as no
     match. A file whose first NUL comes after its first 8000 bytes is text
     to git, and its matches are still read: `late_nul.txt` was named. NAME NOT IN TREE
4. **`-z`** (executed, probe):
   - `--no-renames` leaves no record with two paths. A move read as `D` of
     the old path plus `A` of the new.
   - Paths holding a newline, a leading newline, a leading `\x01`, a `:` or
     `ï` all parsed verbatim in `own_commits` and `tracked_at`.
   - An empty commit read as its header alone.
   - `call_sites` named a caller inside a file whose name holds a newline.
   - Windows: all four Windows shards ran the changed modules on git
     2.55.0.windows.5, and none failed a case of them (executed by CI). Q3
     is answered (a).
5. **The `Corrected ·` rows** (read against the released rows):
   - 0.18.3 `S1, S5, S8, S10` states what is now true.
   - 0.18.3 `S2, S3, S4, S6` is true except its last clause, which is 🟡 2.
   - 0.19.0 `A1` is true. Its "a unit a merge in the range brought in …
     land nowhere" is limited the same way as 🟡 2.
   - 0.16.0 `G9` is true. Under `-z`, `call_sites` ends each match at LF, and
     a U+2028 in the text cuts nothing.

## Not verified

| Item | Who answers |
|---|---|
| The full suite, the repository-wide lint and the typecheck: `unverified` by me, and the broad gate is `not yet` | the sealer, once, after the rounds settle |
| macOS CI leg of PR #878, still running when this report was written | the orchestrator, reading `gh pr checks 878` |
| Whether #879 (#837) conflicts with this diff in `close` and `chain_check.py` | the orchestrator, when the second of the two merges |

My own slip: I ran one `git fetch -q origin` in the user's worktree, which
updates only its remote-tracking refs. `origin/release/v0.21.0` stayed at
`5623d728`, and the working tree and branch did not change.

## Regression tests to plant

- `tests/test_a_shrunken_corpus_declines_to_judge.py` — none new. The fix in
  🔴 1 classifies a scope, and the module's own cases are the regression.
- `tests/test_the_fixes_close_the_record.py`, if 🟡 2 is answered by code
  rather than by prose: a back-merge case, where the base merges the branch,
  a sibling lands on the base, and the branch merges the base. Today it pins
  that the sibling's unit IS listed, so the stated limit stays true.

## Facts for the evidence ledger

- Executed 2026-10-08 on git 2.50.1, macOS: `own_commits` over a back-merge
  owns a sibling commit made on the base after it merged the branch, and does
  not own an own commit on a topic forked before the range's start.
- Executed 2026-10-08: `git grep` without `-I` reports a file the
  `binary` attribute marks as `Binary file <rev>:<path> matches`, so adding
  `-I` changed no call site the old split read.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The S10 case lists paths with `git ls-tree` and is unclassified in the suite-wide path-list guard, so CI fails on ubuntu and on windows group 2 | `tests/test_a_shrunken_corpus_declines_to_judge.py:245` | open | executed: CI on PR #878, 2 failed on each leg; reproduced in the clone (exit 1), and green with the paste-ready fix (exit 0, 17 passed) |
| 🟡 2 | The rule's home says a merged-in commit descends from the range's start never; a back-merge makes a sibling's commit owned, and an own commit on a topic forked before the start is not owned, and the limit paragraph names neither | `docs/the-record-layout.md:121` | open | executed: probe A owned `S(sibling)`, probe B dropped `topic-fix` and `topic.py`; the same sentence also appears at `docs/the-record-layout.md:101`, in the two docstrings and in two ledger rows |
| ⬜ 3 | `own_units` shows and diffs prose paths that `measure` skips, and `own_commits` runs twice per `close` and per `fix_pass_units` | `skills/code-review/scripts/round_record.py:2384` | open | read; cost only |
| ⬜ 4 | A `Contract changes` entry can be a sibling's signature change when an own commit changed only the unit's body | `skills/code-review/scripts/round_record.py:4450` | open | read; the home's sentence is true, its consequence is unstated |
| ⬜ 5 | "It refuses depth 2" now has a document as its antecedent | `skills/code-review/orchestration.md:372` | open | read |
| 🟢 | `close`'s two new refusals both raise before any cell is written | `skills/code-review/scripts/round_record.py:4370` | confirmed | read: `parse_range` at 4370 and the guard at 4422-4443, with the first write after 4516 |
| 🟢 | The `-z` readers parse hostile names verbatim, and `-I` hides no call site the old split read | `skills/code-review/scripts/round_record.py:3711` | confirmed | executed: probes D and E |

## Executed probes

| What was run | Result |
|---|---|
| `test_tmp_probe.py`, case A: back-merge, then a sibling on the base, then the branch merges the base; `own_commits(T, HEAD)` — NAME NOT IN TREE | `['f1', 'S(sibling)', 'f2']` — the sibling is owned |
| case B: own fix on a topic forked before `T`, merged after; `own_commits` and `touched` | `['f']` and `['own.py']` — the topic's fix and `topic.py` are absent |
| case C: start is a merge; range `a..a` | `['f']`; `[]` |
| case D: names holding a newline, a leading newline, a leading `\x01`, a `:`, `ï`; an empty commit; a move and a delete | every path verbatim; empty commit `[]`; move read as `D` + `A`; `tracked_at` holds all of them |
| case E: `call_sites` with a newline-named caller, a file with a NUL after 8000 bytes, and a `.py` marked `binary` | `['late_nul.txt', 'caller', 'odd_caller', 'zz_caller']`; with the attribute, `zz_caller` gone, and plain `git grep` printed `Binary file … zz.py matches` — NAME NOT IN TREE |
| `bin/test tests/test_a_shrunken_corpus_declines_to_judge.py` at the target SHA | exit 1, 2 failed, 15 passed |
| the same, with 🔴 1's fix applied in the clone (then reverted) | exit 0, 17 passed |
| PR #878 CI, read with `gh pr checks` and the job logs | ubuntu: fail (2 failed, 12758 passed); windows group 1: pass (2738 passed); windows group 2: fail (the same 2); windows group 3: pass (1038 passed); windows group 4: pass (2149 passed, 66 skipped); macOS: still running when this report was written. No Windows shard failed a case of the changed modules, and the S10 case carries no skip marker, so `questions.md` Q3 is answered (a) by CI on git 2.55.0.windows.5 |
| broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### 🔴 1

In `tests/test_a_shrunken_corpus_declines_to_judge.py`, `LISTS_A_FIXTURE`,
after the `test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure`
entry:

```python
    "tests/test_chain_check_at_the_pull_request.py#test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure": 1,
    # #860: `ls-tree` over the fixture's own commit, to assert git quotes the
    # name the case wrote; no path in it is opened.
    "tests/test_the_fixes_close_the_record.py#test_a_path_git_would_quote_is_read_as_the_path_it_is": 1,
}
```

### 🟡 2

`docs/the-record-layout.md`, the first paragraph's second sentence, and a
second limit in the last paragraph:

```markdown
**A range `a..b` owns the non-merge commits that descend from `a` and that `b`
reaches** — `git log --ancestry-path --no-merges a..b`. A sibling's commit
that a merge of the base brought in reaches `b` only through the merge, and
in a repository that squashes into its base it descends from `a` never, so it
is not owned, whichever side the merge was made from. Two readers walked a
```

```markdown
What no reader can see is a change made only inside a merge's conflict
resolution. The merge is owned by no range, so `close` refuses a `fixed` row
that names it. Descent is the whole test, so two shapes read against the
item's history. Where the base merged any of the item's commits with a merge
commit (a back-merge, or a stacked branch merged first), every commit made on
the base after that merge descends from `a` and is owned. And an own commit on
a topic forked before `a` descends from it never and is not owned, so its
units leave the surface and a `fixed` row naming it is refused. A range whose
start does not reach its end owns nothing, and `close` refuses it rather than
writing an empty surface.
```

Line 100-101 of the same file:

```markdown
checkout, the pull request merged into its base, reads the same commits as the
branch does, because a squash on the base descends from round 1's target never
(the next section names the merge shape where that fails).
```

The two docstrings take the same qualifier, and so do the `S7, S8, S9` and
`Corrected · S2, S3, S4, S6` rows of this item's ledger fragment: "in a
repository that squashes into its base".

Needs a fix: yes — 🔴 1 (CI red on the suite-wide path-list guard) and 🟡 2 (the rule's home states a limit-free guarantee two merge shapes break)
Loses a record or crashes: no

## Proof

Files opened: `skills/code-review/scripts/chain_check.py` (`git`,
`fix_range`, `range_ends`, `last_round_end`, `own_commits`, `paths_of`,
`fragment_left_behind`), `skills/code-review/scripts/round_record.py`
(`unit_dumps`, `fix_pass_units`, `commit_units`, `own_units`, `landings`,
`parse_range`, `touched`, `parse_module`, `top_units`, `measure`,
`call_sites`, `close`), `skills/verify/scripts/unverified_check.py#show`,
`bin/test`, `tests/test_a_shrunken_corpus_declines_to_judge.py`, the diffs of
`tests/test_the_fixes_close_the_record.py`,
`tests/test_a_fragment_left_behind_is_named.py`,
`tests/test_a_fix_of_a_fix_is_counted.py`,
`tests/test_every_reader_ends_a_line_where_gfm_does.py`,
`docs/the-record-layout.md`, `docs/round-record-spec.md`,
`skills/code-review/orchestration.md`, this item's ledger fragment,
`spec.md`, `overview.md`, `survivors.md`, `questions.md`, `changelog.md`, and
the released rows 0.18.3 `S1, S5, S8, S10` and `S2, S3, S4, S6`, 0.19.0 `A1`
and 0.16.0 `G9`. The probe file and every repository it built are deleted. So
are the clone's virtualenv and the clone itself, after this round.
