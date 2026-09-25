# Round 1 report — settle retires a directory main has not seen closed

| Field | Value |
|---|---|
| Work item | `1790297085-settle-retires-a-directory-main-has-not-seen-closed` |
| Round | 1 |
| Target SHA | b589cf91 |
| Compared against | `origin/release/v0.15.4` (7b557144); range 1880cf92..b589cf91 over the frame ce4e96a8 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Issues | #602, #590, #586 |

## Summary

All three fixes do what the frame asked, and every scenario S1–S11 has a
case. The narrow run in this round's clone was green. One finding needs a
fix, and it sits in the #602 half.

`settle` asks the rule at the merge base of `--released-at` and the local
`HEAD`. The code, the printed heading and the paperwork all call that "the
revision both CI readers ask". It is not quite that. The hygiene workflow
checks out the pull request's merge ref, and on that ref the merge base with
the base branch is the base's tip. The two revisions are the same while the
base has not moved since the fork. Once it has moved and carries the
closure, `settle` still keeps the directory. That is the safe direction.
But the heading it prints says the CI readers ask at that old commit, and
tells the person to merge a closure that has already been merged. I
reproduced that state (🟡 1). The same claim appears in the paperwork (⬜ 2).

Five ⬜ follow. None of them changes a verdict: a shallow-clone sentence that
is false (⬜ 3), a report path with no guard where `retire` has one (⬜ 4),
two sibling purposes nothing pins (⬜ 5), and one shipped loader the spec's
enumeration missed (⬜ 6).

The prompt said 17 ledger rows were re-stamped. I count 14 in the range: C8
(0.12.2), S2, S4, R1, R2 (0.13.0), G3, D3, G7 (0.14.0), P1c, P3, P3b
(0.15.0), D1, E1 (0.15.1), G1 (0.15.3). The phase records name the same 14.
The three missing rows are not in the diff.

## Stage 1 — spec compliance

**#590 (phase 1): met.** Read and executed.

- `fold_check.py#load`, `settle.py#load` and `round_record.py#load` now write
  a sentence to stderr and raise `SystemExit(2)` in both branches. I checked
  the three module docstrings' exit lists against the code, and they say 2.
- `chain_check.py` is not in the diff.
- The `# RIDER:` above `round_record.py#load` is gone. A grep over the tree
  found no sentence left saying it is open: `rider_check.py#load_checker`,
  `settle.py#load` and the settle test's docstring were all corrected.
- The class case in `tests/test_a_script_copied_alone_exits_2.py` runs the
  four scripts as subprocesses. It asserts exit 2, no traceback, the path
  and the purpose, and for `settle.py` it asserts that "fold record" is
  absent (S1, S2).
- **The `PURPOSES` deviation.** The account's grounds hold. The tests call
  `settle.load` with two arguments at six places and `round_record.load`
  (as `generator.load`) at fifteen. `settle.load` is monkeypatched at
  `tests/test_settle_reads_before_it_removes.py:951` and `:1855`. Every
  `load` call in `settle.py` passes one of the three module constants, so
  no call site reaches the fallback purpose. The table is keyed by file
  name in `round_record.py` because `chain.READER` and `chain.ROUTING` are
  only known once `chain_check.py` has loaded; the code confirms that. What
  the deviation costs is ⬜ 5.
- **Enumeration (§12).** The spec built the class with
  `grep spec_from_file_location`. That grep cannot see a sibling imported
  through `sys.path.insert` followed by a plain `import`, and
  `skills/implement/scripts/seal.py` does exactly that (⬜ 6). Every other
  loader the spec names checks out.

**#602 (phase 2): met for the scenarios it names; 🟡 1 is outside them.**
Read and executed.

- `survey` asks the tree first, then the base, so a row open on disk keeps
  the old heading. `retire` asks the predicate itself at both revisions and
  takes the base from `found`. `main` refuses a survey with no base at exit
  2, and `retire` refuses one on its own.
- S4–S8 each have a case. S6 is the counter-case: it removes the directory
  once the base holds the closure, which keeps S4 from passing by refusing
  everything.
- **Which base.** `--released-at` defaults to `origin/main`, and the base is
  the merge base of that ref and the local `HEAD`. For the 0.15.3 shape, a
  closure on `release/vX.Y.Z` that `main` has not seen, both the fork point
  and `main`'s tip lack the closure. So the fix closes #602 either way.
- **A hotfix moving `main`.** CI's revision is `main`'s tip; `settle`'s is
  the fork point. Where `main` carries the closure and the branch never
  merged it back, `settle` keeps a directory CI would pass. That is the safe
  direction, but the output about it is false (🟡 1, executed). The unsafe
  direction needs `main` to reopen a row, or to write a `spec.md` into that
  directory, after the fork. I found no flow in `docs/branch-and-release.md`
  that does that, so I have not raised it.
- **A shallow clone.** `merge_base` returns None, and `settle` exits 2 with
  nothing removed. That is the right answer, but the sentence is false (⬜ 3,
  executed).

**#586 (phase 3): met.** Read and executed.

- The refusal comes after the *nothing to gather* arm and before the section
  is built. So neither `--dry-run` nor the write prints or writes a section
  when it fires. It reads `missing` only.
- **Boundary.** `SECTION_LINE` is `"## "`, tested with `startswith` on every
  line of the file, which is exactly `insert`'s test. `section_body`'s
  `^## ` under `re.M` splits on `\n` only, and `splitlines` also splits on
  U+2028 and form feed. So the predicate is the union of the two readers.
  In that corner it refuses a little more than the note's reader would end
  on, never less. `###`, a bare `##`, an indented `## ` and `##` with no
  space are gathered, and a `## ` line inside a fence is refused. Each has a
  case. A fragment that opens with a BOM before `## ` is not refused, and
  neither reader would end a section on it either, because `str.strip`
  keeps U+FEFF.
- **The 14 re-stamped rows.** I read each one against the edit to its
  anchored unit. Each claim still holds, and D3 was correctly corrected in
  place. The one false sentence among them is D3's note and M2's clause
  repeating the CI-revision claim (⬜ 2). `evidence-check` gave exit 0 on all
  seven edited ledger files (executed).

## Stage 2 — quality

### 🟡 1 — When the base has moved, `settle` prints a heading whose claim and remedy are both false

`skills/settle/scripts/settle.py#RULE_BASE_HEADING` and its two readers,
`#report` and `#retire`. The heading says the CI readers ask the rule at the
merge base of `--released-at` and `HEAD`, and that the remedy is to merge the
closure to the branch the release merges to.

**What happens.** `.github/workflows/hygiene.yml` checks out with no `ref:`,
so on a pull request event `HEAD` is the merge ref. The file's own comment
at the milestone step says so. `unverified_check.py --baseline` and
`chain_check.py --baseline` then compute `merge_base(origin/<base>, HEAD)`,
and that is the base's tip. `settle` runs on a local branch, so its merge
base is the fork point. The two differ as soon as the base moves past the
fork.

**Reproduced, executed.** In a fixture, `main` got a commit closing the
row, standing in for a hotfix. The working branch closed it too and did not
merge `main` back. `settle --retire --released-at main` kept the directory
and exited 1, printing:

```
kept until the closure reaches the merge-base of main and HEAD (84610db) — no `spec.md` and nothing open here, but
the record there still holds an open row, and the CI readers ask the rule there.
Merge the closure to the branch the release merges to first; the directory goes
in a later pull request:
```

In the same fixture, `retired_by_rule` at `main`'s tip returned True. The
merge base of `main` and a merge commit of the branch into `main` was
`main`'s tip. So:

- The CI readers do not ask the rule there.
- The closure is already on the branch the release merges to.
- Following the remedy changes nothing. What moves the base is merging
  `main` into the working branch, and no line of the output says so.

**Why it matters.** Keeping the directory is safe. But a person reading
this output is told to do something they have already done. The only way
out is to reason from the short SHA in the label to the fork point. §14
applies here, because this is a rendered line someone acts on.

**The fix.** Keep the behaviour and make the heading true in both label
forms. `base_label` already tells them apart: `survey` has the ref's own
commit, and the two forms differ exactly when the base moved. Add a second
heading for the moved case that names the working remedy. Correct the four
code-prose sentences that equate the fork point with CI's revision. The
paste-ready block is under `## Paste-ready fixes`.

### ⬜ 2 — The paperwork repeats the CI-revision claim

This is the claim from 🟡 1, in the run's paperwork. It is a correction and
not a fix.

- `seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/changelog.md`,
  the #602 entry: "The checks on a pull request ask it where the branch
  forked from its base." On a pull request they ask at the base's tip. This
  one matters most of the four, because it ships as `CHANGELOG.md` prose.
- `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md`
  M2: "the revision both CI readers ask it of". The same clause is in
  `seal/releases/0.14.0.md` D3's `Corrected 2026-09-25` note: "because both
  CI readers ask the rule there".
- `plan.md` §*Alternatives considered*, the row "ask it at the tip of
  `--released-at`". It rejects the tip because "a hotfix merged the closure
  straight to `main`; `settle` retires, the release pull request's CI asks
  the merge base, finds the row open, and goes red". On the merge ref, CI
  asks at the tip, where that closure is present. So the failure described
  does not happen. The chosen option is still the safer one, for a different
  reason: it keeps more, never less, in every flow this repository uses.

A suggested wording for the changelog: "The checks on a pull request ask it
at the base branch's tip; `settle` asks where the branch forked from it,
which is the same commit unless the base has moved since, and keeps more,
never less, when it has."

### ⬜ 3 — A shallow clone is told the two refs share no commit

`skills/settle/scripts/settle.py#main`, the no-merge-base refusal. I made a
`--depth 1 --no-single-branch` clone of a repository whose `main` and
working branch share history. `settle --released-at origin/main` exited 2
with "`--released-at origin/main and HEAD share no commit`" (executed). The
exit is right. The sentence is false, and it sends the reader to question
the ref instead of the clone's depth. `merge_base`'s own docstring names the
shallow case, and `chain_check.py`'s refusal says "A shallow checkout lands
here". The pinned substring `share no commit` can stay. The fence below adds
the other state.

### ⬜ 4 — `report` has no guard for a survey with no base

`skills/settle/scripts/settle.py#report`. Read, not executed. `survey`
returns `{"base": None, "base_label": None}` when there is no merge base.
`retire` refuses that dict at 2, and its docstring gives the reason: a caller
that skips `main`. `report` has no such check and would raise `KeyError` on
`found["released"]`. Only `main` and the tests call it today, and `main`
refuses first, so nothing reaches it. It is the one reader of `survey` left
with the old contract.

### ⬜ 5 — Nothing pins which purpose `settle` gives its reader and its checker

`tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback`.
Read. The case now puts its own path into `settle.PURPOSES` with the
fold-record purpose, then asserts the fold-record phrase comes out. It shows
that `load` prints the table entry. It no longer shows what the entry for
`READER` says. The class case pins only `OPTIN`'s entry, because a copy
taken alone stops there first. So if `READER`'s and `CHECKER`'s purposes
were swapped, every case would stay green. That is the #590 defect, one row
over. The fence below pins all three entries.

### ⬜ 6 — `seal.py` copied alone dies with a traceback, and the spec's list of loaders does not name it

`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/spec.md`
§Scope *Out*, the "Enumerated by construction" bullet. The grep behind it
was `spec_from_file_location`. `skills/implement/scripts/seal.py` loads
`hooks/config.py` and `hooks/optin.py` through `sys.path.insert` and a
plain `import`, so that grep cannot see it. I copied it alone and ran
`python3 seal.py mode`. It exited 1 with `ModuleNotFoundError: No module
named 'config'` (executed).

Its documented exit 1 is "nothing was written, and the message says why".
The exit code fits that. The traceback is not a message saying why. It is
the same position as `payload_meter.py`, which the spec put outside #590's
class on the same kind of ground. That is a choice the spec should state
rather than leave out. Correct the enumeration, and let the orchestrator
file the issue or leave it, as the spec says for the others.

## Classes enumerated (§12)

- **Two revisions treated as one:** the merge base of `--released-at` and
  the local `HEAD`, and the revision CI asks at. I grepped
  `revision both CI readers`, `CI readers ask`, `CI readers compare` and
  `where the branch forked` over the diff. The instances are the four
  sentences in `settle.py` (🟡 1) and the four paperwork places (⬜ 2).
  `skills/settle/SKILL.md`'s new paragraph says "the merge base of that pull
  request's base and `HEAD`", which is true on the merge ref. The README
  rows say "where CI asks", which is loose but not false. Neither needs a
  change.
- **Shipped loaders of a sibling:** `spec_from_file_location` and
  `sys.path.insert` over `skills hooks bin` (⬜ 6).
- **Readers of a base-less survey:** `main`, `retire` and `report`. Only
  `report` has no guard (⬜ 4).

## Regression tests to plant

- `tests/test_settle_reads_before_it_removes.py`: the moved-base fixture
  from 🟡 1. Check that the directory is kept, that the output names
  `main`, and that it says to merge `main` into this branch. It is red
  against b589cf91 because the second heading does not exist yet.
- `tests/test_settle_reads_before_it_removes.py`: the per-sibling purpose
  case from ⬜ 5.

## Facts for the evidence ledger

- On a pull request event, the hygiene workflow's `unverified_check.py` and
  `chain_check.py` steps read at the base branch's tip and not at the
  fork point, because the checkout is the merge ref. The anchor is
  `.github/workflows/hygiene.yml`, the comment above `HEAD_SHA`, which
  already states it for the milestone step.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Once `--released-at` has moved past the fork carrying the closure, `settle` keeps the directory and prints that the CI readers ask at the fork point and that the closure must be merged to the release's branch; both are false, and the remedy that works (merge the ref into this branch) is never named | `skills/settle/scripts/settle.py#RULE_BASE_HEADING`, `#report`, `#retire`, `#main` | open | Executed: a fixture where `main` holds the closure printed the heading, while `retired_by_rule` at `main`'s tip was True and the merge-ref merge base was `main`'s tip; CI checks out the merge ref (`.github/workflows/hygiene.yml`, no `ref:`) |
| ⬜ 2 | The changelog fragment, ledger M2, 0.14.0 D3's correction note and `plan.md`'s rejected-alternative row say CI asks at the fork point | `changelog.md` #602 entry; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `seal/releases/0.14.0.md` D3; `plan.md` §*Alternatives considered* | open | Paperwork correction, outside `Needs a fix`; the changelog sentence ships as `CHANGELOG.md` prose |
| ⬜ 3 | A shallow clone is told the two refs "share no commit" | `skills/settle/scripts/settle.py#main` | open | Executed: a depth-1 clone of related history exited 2 with that sentence; `merge_base`'s docstring and `chain_check.py`'s refusal both name the shallow state |
| ⬜ 4 | `report` raises `KeyError` on a base-less survey that `retire` refuses at 2 | `skills/settle/scripts/settle.py#report` | open | Read; no caller reaches it today |
| ⬜ 5 | Nothing pins the purpose `settle` gives `READER` and `CHECKER`; the renamed case inserts the phrase it then asserts | `tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback` | open | Read; the class case reaches `OPTIN` only |
| ⬜ 6 | `skills/implement/scripts/seal.py` copied alone dies with a `ModuleNotFoundError` traceback at exit 1, and the spec's enumeration of loaders does not name it | `spec.md` §Scope *Out* | open | Executed; the enumeration's grep cannot see a `sys.path.insert` import. Paperwork correction; the orchestrator files or leaves the script |
| 🟢 | #590: three loaders refuse a missing sibling at 2 with a sentence naming the path and the purpose; the rider is discharged, and no sentence calling it open remains | `fold_check.py#load`, `settle.py#load`, `round_record.py#load` | confirmed | Read the three and their docstrings; the class case green in this round's run; S3 grep empty |
| 🟢 | #586: the gather refuses exactly the lines both release readers end a section on, among the fragments it would write, before anything is written or printed | `.github/scripts/gather_changelog.py#main`, `#section_lines` | confirmed | Read against `insert` and `publish_release_note.py#section_body`; module green in this round's run |
| 🟢 | The 14 ledger rows re-stamped in the range each still hold against the edit to their anchored unit | `seal/releases/0.12.2.md`, `0.13.0.md`, `0.14.0.md`, `0.15.0.md`, `0.15.1.md`, `0.15.3.md` | confirmed | Read each against its unit; `evidence-check` exit 0 on all seven files; D3's note is ⬜ 2 |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_a_script_copied_alone_exits_2.py`, `tests/test_settle_reads_before_it_removes.py`, `tests/test_the_changelog_is_gathered_at_release.py` and `tests/test_a_folded_statement_names_what_enforces_it.py`, in this round's clone at b589cf91 | exit 0, 189 passed |
| Probe (one file, run once, deleted): moved base. `main` closes the row after the fork, the branch closes it too, `settle.retire` with `--released-at main` | exit 1, kept under "kept until the closure reaches the merge-base of main and HEAD (84610db)" with "the CI readers ask the rule there"; `retired_by_rule` at `main`'s tip True; merge base of `main` and a merge of the branch into `main` equals `main`'s tip |
| Same probe file: a `--depth 1 --no-single-branch` clone of related history, `settle.main --released-at origin/main` | exit 2, "share no commit" |
| `skills/implement/scripts/seal.py` copied alone to an empty directory, `python3 seal.py mode` | exit 1, `ModuleNotFoundError: No module named 'config'` traceback |
| `./bin/evidence-check --ledger <file> .` on the fragment and the six edited `seal/releases/*.md` | exit 0 on each, 0 drifted, 0 broken |
| The broad gate: the full suite, lint and typecheck | not yet. That run belongs to the sealer, once, after the rounds settle; this round ran four modules only |

## Paste-ready fixes

### 🟡 1

In `skills/settle/scripts/settle.py`: a second heading for the moved base,
one helper that picks between the two headings, and two more keys in
`survey`'s dict.

```python
# beside RULE_BASE_HEADING
# #602, round 1: `--released-at` has moved past the fork. The CI readers ask
# at its tip (a pull request is checked out as the merge ref), and this asks
# at the fork, so a closure already merged there is not read here until the
# ref is merged into this branch.
RULE_MOVED_HEADING = (
    "kept until the closure reaches {base} — no `spec.md` and nothing open "
    "here, but\nthe record there still holds an open row. {ref} has moved past "
    "that commit: where\n{ref} already holds the closure, merge {ref} into this "
    "branch and run `settle`\nagain; otherwise merge the closure to {ref} "
    "first. The directory goes in a later\npull request:"
)


def base_heading(found):
    """The heading for a directory kept at the base, true of both label forms:
    the ref's own commit, where the CI readers ask too, or a fork the ref has
    moved past, where they do not."""
    if found.get("base_moved"):
        return RULE_MOVED_HEADING.format(base=found["base_label"], ref=found["ref"])
    return RULE_BASE_HEADING.format(base=found["base_label"])
```

```python
# survey: replace the two base lines of the dict
    ref_commit = reader.commit_of(root, ref)
    survey = {
        "base": base,
        "base_label": reader.base_label(ref, ref_commit, base),
        "base_moved": base != ref_commit,
        "ref": ref,
```

```python
# report
    if found["rule_base_kept"]:
        write(f"\n{base_heading(found)}\n")
        write_rule_kept(found["rule_base_kept"], out, base=found["base_label"])

# retire
    if base_kept:
        out.write(f"\n{base_heading(found)}\n")
        write_rule_kept(base_kept, out, base=label)
```

The same claim in the code prose, corrected (`main`'s comment above the
no-merge-base refusal, the comment above `RULE_BASE_HEADING`, and the
refusal's own sentence):

```python
    # #602: the rule arm asks its predicate of the merge base of the ref and
    # `HEAD`. The CI readers compute the same merge base from their own
    # `HEAD`, which on a pull request is the merge ref, so theirs is the
    # base's tip: the same commit while the base has not moved since the
    # fork, and a later one when it has, where this keeps more and never
    # less. Two histories that share no commit have none, and the predicate
    # asked of nothing would be asked of the working tree alone.
```

```python
# #602: nothing is open in the tree, and the base still holds a row open.
# `{base}` is `unverified_check.py#base_label`'s spelling of the merge base of
# `--released-at` and `HEAD`. It is the revision the CI readers ask at when
# the ref has not moved since the fork; `RULE_MOVED_HEADING` is the other case.
```

The pin, beside `test_a_closure_the_base_has_not_seen_keeps_the_directory`:

```python
def test_a_base_that_moved_past_the_fork_names_the_merge_that_moves_it(tree):
    """Round 1, 🟡 1. `main` took the closure after this branch forked, and
    this branch never merged it back. CI asks at `main`'s tip and would pass;
    `settle` asks at the fork and keeps the directory. That keeps more than
    it must, which is the safe direction, but the remedy it prints has to be
    the one that works: merge `main` in."""
    moment(tree, overview=OVERVIEW_OPEN)
    git(tree, "branch", "-M", "main")
    git(tree, "switch", "-qc", "work")
    ov = tree / "seal" / "specs" / MOMENT / "overview.md"
    ov.write_text(OVERVIEW_CLOSED, encoding="utf-8")
    git(tree, "add", "--", f"seal/specs/{MOMENT}")
    git(tree, "commit", "-qm", "close on work")
    git(tree, "switch", "-q", "main")
    ov.write_text(OVERVIEW_CLOSED, encoding="utf-8")
    git(tree, "add", "--", f"seal/specs/{MOMENT}")
    git(tree, "commit", "-qm", "hotfix: close on main")
    git(tree, "switch", "-q", "work")
    code, text = at(tree, "main", "--retire")
    assert (tree / "seal" / "specs" / MOMENT).exists(), text
    assert code == 1, text
    flat_text = " ".join(text.split())
    assert "merge main into this branch" in flat_text, text
    assert "the CI readers ask the rule there" not in flat_text, text
```

### ⬜ 3

```python
    if found["base"] is None:
        sys.stderr.write(
            f"settle: --released-at {args.released_at} and HEAD share no commit "
            f"in {root}, or this clone is too shallow to reach the one they "
            "share (`git fetch --unshallow`) — nothing was read. The rule arm "
            "asks whether a record is closed at their merge base, and there is "
            "none to ask.\n"
        )
        return 2
```

### ⬜ 5

```python
@pytest.mark.parametrize(
    "which, phrase",
    [
        ("READER", "it is where the fold record is read from"),
        ("CHECKER", "it is what resolves a ledger row's anchor"),
        ("OPTIN", "it is what finds the repository's seal/ root"),
    ],
)
def test_each_sibling_is_refused_with_its_own_purpose(which, phrase, monkeypatch, capsys):
    """#590's second half, per file: the table entry for each real sibling,
    not an entry the case put there itself."""
    path = getattr(settle, which)
    real = os.path.isfile
    monkeypatch.setattr(os.path, "isfile", lambda p: False if p == path else real(p))
    with pytest.raises(SystemExit) as raised:
        settle.load(path, "absent")
    assert raised.value.code == 2
    assert phrase in capsys.readouterr().err
```

Needs a fix: yes — 🟡 1 (the heading printed when the base has moved past the fork says the CI readers ask there and gives a remedy that changes nothing)
Loses a record or crashes: no

## Proof block

Opened in this round, at b589cf91 in this round's clone unless stated:

- The work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`, `routing.md`, `changelog.md` and `phases/phase-1.md`–`phase-3.md`, in the worktree.
- `git diff 1880cf92..b589cf91` of `skills/settle/scripts/settle.py`, `skills/settle/scripts/fold_check.py`, `skills/code-review/scripts/round_record.py`, `.github/scripts/gather_changelog.py`, `.github/scripts/rider_check.py`, every file under `tests/` in the range, `README.md`, `README.ko.md`, `CONTRIBUTING.md`, `docs/branch-and-release.md`, `docs/the-evidence-ledger.md`, `skills/settle/SKILL.md` and `seal/releases/*.md`.
- `skills/settle/scripts/settle.py` `#retire`, `#main` and `#survey` in full.
- `.github/scripts/gather_changelog.py` from its imports to the end.
- `skills/verify/scripts/unverified_check.py` `#commit_of` to `#wrote_a_spec`, and `#main`'s baseline block.
- `.github/scripts/publish_release_note.py#section_body`.
- `.github/workflows/hygiene.yml`: the trigger and checkout, the `unverified_check.py` and `chain_check.py` steps, and the milestone step's comment.
- `skills/evidence-check/scripts/evidence_check.py`, the optin loader.
- `skills/implement/scripts/seal.py`, its imports.
- `tests/test_settle_reads_before_it_removes.py`, its fixtures and `moment`.
- `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md`.
- The 14 changed rows in `seal/releases/0.12.2.md`, `0.13.0.md`, `0.14.0.md`, `0.15.0.md`, `0.15.1.md` and `0.15.3.md`.
- `seal/specs/1790260563-the-fold-checks-run-only-as-this-repositorys-tests/rounds/round-1-report.md`, for its headings only.
