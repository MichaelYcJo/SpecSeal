# Round 1 — a git call that fails reads as no remote (#111, PR #234)

Target SHA `8fb1fb533c700f43e07c69a9c72cada5b1734234`. The tree did not move
under me: `git rev-parse HEAD` reads that SHA and `git status --short` is
empty at the start and at the end of the round, except for this report.

Reviewed in a `git clone --no-local` of the worktree at the target SHA. The
worktree itself was read and never written, apart from this file.

## What the account claimed, and what I found

The hand-back's five load-bearing claims were each opened rather than taken.

| The account claimed | What I found |
|---|---|
| Five call sites of `git()`, the fifth being the second call inside the refusal message | **Confirmed, re-derived before reading `spec.md`'s table.** `grep -n 'git('` at `86e140f` returns nine hits: one definition (`:139`), three prose mentions inside a comment or docstring (`:1571`, `:1748`, `:1981`), and five calls at `:322`, `:323`, `:947`, `:953`, `:1476`. My partition matches the table's, including that `:1476` is the safe one |
| `git config --get` exits 1 with empty streams when the key is unset; an unparseable config exits 128 | **Confirmed by my own measurement** against git 2.50.1 (Apple Git-155), nine shapes, in a scratch repository I built. See finding 4 for the one meaning of exit 1 the docstring does not enumerate |
| The promotion of `git_asked` did not change `porcelain`, `tracked` or `gitlinks_under_root` | **Confirmed by construction.** The diff touches none of the three; each still runs its own `subprocess.run`. `git()`'s contract is also unchanged — it is now `git_asked(root, *args)` with the default `answered=(0,)` and `text or ""`, which is the old body's two failure paths collapsed to the same `""` |
| One ledger row removed on the grounds its claim went with the behaviour; nine re-stamped after re-reading | **Confirmed, and the drift is this branch's alone.** I re-ran the hand-back's own check: `git archive 86e140f \| tar -x` into a scratch directory, `evidence-check` over it reads `764 ok · 0 drifted`. All nine re-stamped rows are anchored at `import_` (eight) or `other_worktrees` (one), the two units this branch edited, and I opened each of the nine claims — none is falsified by the change |
| Eleven mutations, all killed | **Six of my own, all killed**, including the two that would hurt most. See the probes table |

Two claims I could not close from the diff and answered by running:

- The README changes are pinned by modules the hand-back did not run. I ran
  them; they pass (probes table, row 2).
- `remote_url`'s docstring names git 2.50.1, and `test_release_hygiene.py`
  grew an allowlist entry for it. That module passes at the target.

## Findings

### 1 🟡 A manifest whose `remote` is present but not a string walks past the new refusal

`skills/implement/scripts/seal.py:1048`

The refusal's only signal for *the exporting machine could not look* is that
the key is absent. `theirs = manifest.get("remote")` is never checked for its
type, so `"remote": null` — which is what a JSON writer produces from the very
`None` this work item introduced — counts as present, the refusal does not
fire, and `normalise_remote` turns it into `""`, which switches the
other-repository check off as well. The zip imports at exit 0 with both
guards silent.

Measured, not reasoned: five values, all imported at exit 0 with the record
written (probe A). `null`, `42`, `[]`, `{}` and `true`.

This is the class `seal/ledger.md` already carries a row for — *S17c · a
manifest another machine wrote is read for its type, not only for its
presence* — and this commit adds a new read of that manifest without the type
check the row exists for. It is not a regression against `86e140f`: the
other-repository check was already off for a non-string. What is new is that
the guard this ticket exists to add inherits the same hole on its first day.

### 2 🟡 The refusal tells the person to re-run an import that can never succeed

`skills/implement/scripts/seal.py:1067`, and the same sentence in
`README.md:526`

The closing advice is one line for two different failures:

```
Run this again if the failure was transient, or pass --allow-unreadable-remote
to import without the check.
```

When the unanswerable side is *this* clone, re-running is right. When the
unanswerable side is the zip — the `remote` key is absent — re-running reads
the same bytes and refuses identically, forever. The fix is on the other
machine: export again once its git answers. Nothing in the output says so.

Measured: probe B runs the import against a zip whose manifest is
`{"format": 1}` and the advice line is printed verbatim.

`README.md:526` carries the same reading — *"only the second is a reason to
run the command again"* — which is true for one of the two silent sides and
wrong for the other.

### 3 🟡 The export writes a zip that will be refused on arrival and says nothing

`skills/implement/scripts/seal.py:406-411`

`manifest_of` holds the reason git could not answer and throws it away twice
(`url, _` and `head, _`). The export then prints `wrote <path>`, the file
count and *Take it in on the other machine with: seal import …*, at exit 0,
with no mention that the manifest is short a field.

The consequence is that the failure is diagnosed on the machine that cannot
fix it. The person at the importing end gets a hard refusal whose only escape
is a flag; the person at the exporting end — the only one who can re-run
until git answers — is told the export succeeded.

Measured: probe C. Exit 0, `"remote" not in manifest`, and the word `remote`
appears nowhere in the export's output.

### 4 ⬜ `remote_url`'s docstring enumerates exit 1's meanings and misses one

`skills/implement/scripts/seal.py:194-213`

The docstring is the design's foundation, and it says exit 1 means the key is
unset, adding that *"Exit 1 also covers `error: key does not contain a
section`, which a literal well-formed key cannot reach."* My measurement finds
a third: `git -C <a path that is not a repository> config --get
remote.origin.url` also exits 1 with both streams empty, indistinguishable
from an unset key.

**This is not reachable here** and I am not asking for a code change.
`import_` and `manifest_of` both take `repo` from `resolve`, which is
`optin.repo_root(cwd)` — a path git itself resolved one command earlier — and
`import_` returns 1 before either call when that is empty. The correction is
to the sentence, because a later reader deciding whether `answered=(0, 1)` is
safe for a new caller will read this enumeration and act on it.

### 5 ⬜ `manifest_of` reads the two fields by two different tests

`skills/implement/scripts/seal.py:407-411`

`remote` is admitted on `if url is not None` and `head` on `if head`. Both are
correct today, and `head_sha`'s docstring argues why the truthiness test loses
nothing — `git rev-parse HEAD` has no empty answer. It is still two spellings
of one question in five consecutive lines, and the one that would silently
drop a legitimate empty answer is the shorter one. `if head is not None`
behaves identically today and cannot become wrong.

## Correction — the record's own paperwork

None. `routing.md`, `spec.md`, `questions.md`, `overview.md`, `plan.md`, the
three phase files, `changelog.md` and the ledger fragment were read and are
internally consistent with the code at the target. `evidence-check .` at the
target reads `776 ok · 0 drifted · 0 broken`, exit 0.

Two disclosures the hand-back made itself, which I confirm rather than
re-raise: the `Checked` column on the nine re-stamped rows still reads
`2026-09-03` over content stamped `2026-09-07`, routed to the repository owner
in `overview.md` §*Not verified*; and the four sibling guards were left off
`git_asked` with grounds, in §*Not done*.

## Regression tests to plant

All three go in
`tests/test_the_records_can_be_carried_out_and_in.py`, beside the `#111`
block that starts at line 398.

| For | Case | Shown red by |
|---|---|---|
| Finding 1 | `test_a_manifest_remote_of_the_wrong_type_refuses` — parametrised over `None`, `42`, `[]`, `{}`, `True`; assert exit 1 and the root unchanged | reverting the `isinstance` check; measured red five times over at the target |
| Finding 2 | `test_the_advice_names_the_machine_that_can_fix_it` — a zip with no `remote` key; assert the output does not tell the person to re-run, and does name exporting again | reverting the split; measured red at the target |
| Finding 3 | `test_the_export_says_what_it_could_not_read` — inject a timeout on `config --get`, assert `remote` appears in the export's output | reverting the print; measured red at the target |

## Facts for the evidence ledger

Three, all for this work item's own fragment, once the fixes land.

- `git config --get` exits 1 with both streams empty for **three** distinct
  states on git 2.50.1: an unset key, `error: key does not contain a section`,
  and a path that is not a repository. `answered=(0, 1)` is safe only for a
  caller whose `root` git has already resolved. Coordinate:
  `skills/implement/scripts/seal.py#remote_url`.
- The receiving guard's signal is the manifest field's **type**, not its
  presence: `null`, a number, a list, an object and a bool are each *no
  answer*, and presence alone let all five through (measured at `8fb1fb5`).
  Coordinate: `skills/implement/scripts/seal.py#import_`.
- The exporting machine is the only one that can clear an unreadable remote,
  so the reason `manifest_of` reads has to reach the export's own output.
  Coordinate: `skills/implement/scripts/seal.py#manifest_of`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A manifest whose `remote` is present but not a string walks past the new refusal — `null`, `42`, `[]`, `{}` and `true` all import at exit 0 with both guards silent | `skills/implement/scripts/seal.py:1048` | open | Executed at `8fb1fb5`: five parametrised values, all exit 0 with the record written. The guard's only signal is key absence; `theirs` is never type-checked, and `normalise_remote` turns every non-string into `""` |
| 2 | The refusal advises re-running an import that can never succeed, when the silent side is the zip rather than this clone | `skills/implement/scripts/seal.py:1067`, `README.md:526` | open | Executed at `8fb1fb5`: a zip whose manifest is `{"format": 1}` refuses and prints `Run this again if the failure was transient`. The `remote` key is absent in the bytes on disk, so no re-run can change it |
| 3 | The export writes a zip that will be refused on arrival and says nothing; `manifest_of` discards the reason it holds | `skills/implement/scripts/seal.py:406-411` | open | Executed at `8fb1fb5`: with `config --get` timing out, the export exits 0, omits `remote`, and the word `remote` appears nowhere in its output. The exporting machine is the only one that can clear the failure |
| 4 | `remote_url`'s docstring enumerates exit 1's meanings and misses `git -C <not a repository>`, which also exits 1 with empty streams | `skills/implement/scripts/seal.py:194-213` | open | Executed measurement against git 2.50.1. Not reachable through `resolve`, so a documentation correction rather than a defect — but the enumeration is what a later reader will use to judge a new `answered=(0, 1)` caller |
| 5 | `manifest_of` admits `remote` on `is not None` and `head` on truthiness, two spellings of one question five lines apart | `skills/implement/scripts/seal.py:407-411` | open | Read. Identical behaviour today, argued in `head_sha`'s docstring; the shorter spelling is the one that would silently drop a legitimate empty answer if `head_sha` ever gained one |
| — | Five call sites of `git()` at the base, `:953` included; exactly one at the target | `skills/implement/scripts/seal.py` | answered | Re-derived independently by `grep -n 'git('` before reading `spec.md`'s table, at both commits. Matches. The fix pass added no new member: `git_asked`, `remote_url` and `head_sha` all return `(value, why)`, so a caller cannot read a value as a fact without the reason beside it |
| — | Nine `seal/ledger.md` rows re-stamped, one removed; the drift is this branch's alone | `seal/ledger.md` | answered | Executed: base tree extracted at `86e140f` reads `764 ok · 0 drifted`, so nothing was stale before this branch. All nine anchors are `import_` or `other_worktrees`, the two units edited. I opened all nine claims — zip bounds, member ordering, manifest typing, the worktree note — and none is falsified. Target reads `776 ok · 0 drifted` |
| — | The removed row `S4 · a repository with no commit records an empty head` | `seal/ledger.md`, `seal/ledger/1788789329-…md` | answered | Its claim is false at the target: `head` is now absent, not empty. The replacement claim is R2 in the branch's own fragment, which is what `CLAUDE.md` §*a change writes fragments* prescribes. Anchor arithmetic checks out — one row, two anchors, 764 → 762 |
| — | The `Checked` date on the nine re-stamped rows still reads `2026-09-03` | `seal/ledger.md` | answered | Already disclosed by the implementer and routed to the repository owner in `overview.md` §*Not verified*. Not re-raised |
| — | README and record modules the hand-back did not run | `README.md`, `README.ko.md`, the work item's records | answered | Executed at `8fb1fb5`: ten modules, `355 passed`, exit 0. The `unverified` label on the broad gate is honest — what was left out is the full suite, not these |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_records_can_be_carried_out_and_in.py tests/test_release_hygiene.py -q` at `8fb1fb5` | `118 passed`, exit 0 — the inherited claim, re-run |
| `bin/test` over ten modules that pin the changed READMEs, ledger, changelog fragment and work-item records (`test_docs_line_wrap`, `test_the_pull_request_language_is_the_repositorys`, `test_no_real_identifiers`, `test_lint_python`, `test_a_row_points_by_content`, `test_the_ledger_fragments_fold_at_release`, `test_the_changelog_is_gathered_at_release`, `test_the_set_a_work_item_always_has`, `test_routing_is_recorded`, `test_absence_claims`) | `355 passed`, exit 0 |
| Six mutations of the changed units in a `git clone --no-local` at `8fb1fb5` | All six killed. M1 the refusal never firing → 3 red; M2 `remote_url` dropping `answered=(0, 1)` → 2 red; M3 `manifest_of` collapsing absent into `""` → 1 red; M4 `mine is None` weakened to `not mine` → 1 red; M5 the zip-side absence unchecked → 1 red; M6 the second `git()` restored in the message → 1 red |
| git's own exit codes, nine shapes, against scratch repositories I built (git 2.50.1, Apple Git-155) | unset `(1, '', '')`; set `(0, url, '')`; unparseable config `(128, '', 'fatal: bad config line 9 …')`; duplicated `url =` `(0, last value, '')`; a valueless `url` `(0, '', '')`; `url = ""` `(0, '', '')`; **not a repository `(1, '', '')`**; `rev-parse HEAD` unborn `(128, 'HEAD', …)`; unreadable config `(128, '', 'fatal: unable to access …')` |
| `bin/evidence-check .` at `8fb1fb5` | `776 ok · 0 drifted · 0 broken`, exit 0 |
| `git archive 86e140f \| tar -x` into a scratch directory, `evidence_check.py .` over it | `764 ok · 0 drifted`, exit 0 — the hand-back's own check, re-run |
| Probe A/B/C (`test_tmp_probe_111.py` in the clone, run once, deleted) | All three red: five wrong-type `remote` values imported at exit 0; the re-run advice printed for a zip-side silence; the export silent about the field it omitted |

The mutation harness, run from the clone root:

```python
MUTATIONS = {
  "M1 remove the whole refusal (the ticket's bug, back)": (
     "        if unreadable and not args.allow_unreadable_remote:",
     "        if False and unreadable and not args.allow_unreadable_remote:"),
  "M2 `git config --get` exit 1 is NOT an answer": (
     '    return git_asked(root, "config", "--get", "remote.origin.url", answered=(0, 1))',
     '    return git_asked(root, "config", "--get", "remote.origin.url")'),
  "M3 manifest_of: absent vs empty collapsed for `remote`": (
     '    if url is not None:\n        manifest["remote"] = url',
     '    manifest["remote"] = url or ""'),
  "M4 import_: `mine is None` -> falsy (no-origin clone refuses)": (
     "        if mine is None:",
     "        if not mine:"),
  "M5 zip-side absence not checked": (
     '        if "remote" not in manifest:',
     '        if False and "remote" not in manifest:'),
  "M6 refusal message asks git a second time": (
     '            print(f"  this clone is  {mine}")',
     '            print(f"  this clone is  {git(repo, \'config\', \'--get\', \'remote.origin.url\')}")'),
}
# each pattern asserted to match exactly once, applied, pytest run, reverted
```

The probe that produced findings 1, 2 and 3:

```python
"""Round-1 probe. Deleted before the report was handed over."""
import json, zipfile
import pytest
from test_the_records_can_be_carried_out_and_in import (
    seal, carried, local, run, git, only_zip,
    git_cannot_answer, timed_out, CONFIG_GET_REMOTE,
)


@pytest.mark.parametrize("value", [None, 42, [], {}, True])
def test_probe_a_manifest_remote_of_the_wrong_type(seal, carried, capsys, value):
    _z, other, home = carried
    bad = other.parent / f"typed-{type(value).__name__}.zip"
    with zipfile.ZipFile(bad, "w", zipfile.ZIP_DEFLATED) as a:
        a.writestr("manifest.json", json.dumps({"format": 1, "remote": value}))
        a.writestr("seal/ledger/1788000000-a-work-item.md", "# rows\n")
    code, out = run(seal, ["import", str(bad)], other, capsys)
    assert code == 1, f"remote={value!r} imported at exit 0 with no check"


def test_probe_b_the_advice_when_only_the_zip_is_silent(seal, carried, capsys):
    _z, other, _home = carried
    silent = other.parent / "silent.zip"
    with zipfile.ZipFile(silent, "w", zipfile.ZIP_DEFLATED) as a:
        a.writestr("manifest.json", json.dumps({"format": 1}))
        a.writestr("seal/ledger/1788000000-a-work-item.md", "# rows\n")
    code, out = run(seal, ["import", str(silent)], other, capsys)
    assert "Run this again if the failure was transient" not in out, (
        "the advice tells the person to re-run an import that can never succeed"
    )


def test_probe_c_the_export_says_nothing_when_it_could_not_read(
    seal, repo, local, monkeypatch, capsys
):
    git_cannot_answer(monkeypatch, seal, CONFIG_GET_REMOTE, timed_out)
    code, out = run(seal, ["export"], repo, capsys)
    m = json.loads(zipfile.ZipFile(only_zip(repo.parent)).read("manifest.json"))
    assert "remote" not in m
    assert "remote" in out.lower(), (
        "the export wrote a zip that will be refused on arrival and said nothing"
    )
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a re-stamped row's `Checked` date should move | `overview.md` §*Not verified*, row 5 | the repository owner |
| `porcelain`, `indexed`, `tracked` and `gitlinks_under_root` moved onto `git_asked` | `overview.md` §*Not done*, paragraph 1 | whoever next edits one of them for a reason of its own |
| Whether `git config --get` exits 1 for an unset key on builds other than 2.50.1 | `overview.md` §*Not verified*, row 3 | the repository owner. Finding 4 narrows the question rather than reopening it |
| Windows | `overview.md` §*Not verified*, row 4 | CI's Windows leg |

## Paste-ready fixes

Finding 1 — `skills/implement/scripts/seal.py:1044-1054`. The signal becomes
the field's type, which is what `normalise_remote` has always needed it to be.

```python
        mine, why = remote_url(repo)
        theirs = manifest.get("remote")
        unreadable = []
        if mine is None:
            unreadable.append(f"this clone's remote could not be read: {why}")
        if not isinstance(theirs, str):
            # The TYPE, not the presence. Absent is the export's word for *I
            # could not read it*, and so is `null` — which is what a writer
            # holding this file's own `None` produces. Every other non-string
            # reduces to "" in `normalise_remote`, which is the empty ANSWER
            # this check exists to tell apart from silence, so presence alone
            # let five values through at exit 0 with both guards off.
            unreadable.append(
                "the zip records no remote this command can read, so the "
                "machine that exported it could not read one either"
            )
```

Finding 2 — `skills/implement/scripts/seal.py:1063-1070`. One advice line
became two, because the two silent sides have two different next steps.

```python
        if unreadable and not args.allow_unreadable_remote:
            print("whether this zip came from this repository cannot be answered:")
            for reason in unreadable:
                print(f"  {reason}")
            print(
                "\nNothing was written. Records are keyed by work-item id, so "
                "merging another project's would spread through the root with "
                "nothing to tell them apart afterwards, and a remote that "
                "could not be read is not the same fact as a repository "
                "without one."
            )
            # Which machine can fix this decides what to tell the person. A
            # git that failed HERE may answer on the next run; a zip that
            # records no remote will read the same on every run there is, and
            # the export has to happen again on the machine that wrote it.
            if mine is None:
                print(
                    "Run this again if the failure here was transient, or pass "
                    "--allow-unreadable-remote to import without the check."
                )
            else:
                print(
                    "Re-running this cannot change what the zip records — "
                    "export again on the machine that wrote it, or pass "
                    "--allow-unreadable-remote to import without the check."
                )
            return 1
```

Finding 2, the same sentence in `README.md:520-526`:

```markdown
when the remote could not be read on either side and so that question cannot
be answered at all (`--allow-unreadable-remote` to import without the check —
a separate flag, because *there is no remote* and *nobody could say* are
different facts). Which side went silent decides what to do next: a git that
failed here may answer on the next run, while a zip that records no remote
reads the same every time and has to be exported again on the machine that
wrote it,
```

Finding 3 — `skills/implement/scripts/seal.py:398-412`. The reason reaches the
one person who can act on it.

```python
def manifest_of(repo, mode, files):
    """(the manifest, what git could not answer), a field LEFT OUT for each.

    Absent and empty are different facts, and `remote` needs all three states:
    a URL, `""` for a repository with no `origin`, and absent for a question
    that went unanswered. Freezing `""` in for the third switched off the
    receiving machine's own refusal (#111) — an export cannot ask the importer
    to tell two facts apart while writing one string for both.

    `head` has no empty state at all. `git rev-parse HEAD` prints a SHA
    whenever it succeeds, so present here means a SHA was read, and a
    repository with no commit leaves the field out.

    **The reasons come back rather than being dropped.** An omitted `remote`
    is refused on arrival, and the machine running THIS command is the only
    one that can clear the failure by running it again — so an export that
    said nothing left the diagnosis on the machine that cannot act on it.

    The format number does not move for this. No field was renamed or
    repurposed, and format 1's only reader of these two already goes through
    `manifest.get`.
    """
    manifest = {
        "format": FORMAT,
        "mode": mode,
        "exported_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "items": work_item_digests(files),
    }
    unread = []
    url, why = remote_url(repo)
    if url is not None:
        manifest["remote"] = url
    else:
        unread.append(f"the remote was left out — {why}")
    head, head_why = head_sha(repo)
    if head is not None:
        manifest["head"] = head
    else:
        unread.append(f"the HEAD SHA was left out — {head_why}")
    return manifest, unread
```

Its one caller, `skills/implement/scripts/seal.py:547-560`:

```python
    manifest, unread = manifest_of(repo, mode, files)
    try:
        write_zip(target, home, files, manifest)
    except OSError as exc:
        print(f"the zip could not be written to {target}: {exc}")
        return 1

    write_state(repo, manifest)
    print(f"wrote {target}")
    print(
        f"  {plural(len(files), 'file')} from {display(repo, home)}, "
        f"{plural(len(manifest['items']), 'work item')}"
    )
    for line in unread:
        print(f"  {line}")
    if unread:
        # Named here because this is the machine that can fix it. `seal
        # import` refuses a zip recording no remote, and re-running the import
        # there cannot change what these bytes say.
        print(
            "  Running this again once git answers writes a zip the other "
            "machine takes in without a flag."
        )
```

Finding 5 — `skills/implement/scripts/seal.py:410-411`, folded into the block
above as `if head is not None`. Identical behaviour today; it cannot become
wrong if `head_sha` ever gains an empty answer.

Needs a fix: yes — findings 1, 2 and 3. A guard whose only signal is key
presence lets five wrong-type values past it; a refusal sends the person into
a re-run loop that can never end; and the export tells the machine that can
fix the failure that everything succeeded.
Loses a record or crashes: no

Every refusal returns 1 at `:1070`, before
`destination_root` at `:1087` and `write_members` at `:1129`, so nothing is
written on any of these paths, and nothing raises — `normalise_remote` returns
`""` for every non-string and `git_asked` catches `OSError` and
`subprocess.SubprocessError`. Finding 1's outcome is a guard that stays quiet,
not a record leaving the root.

## Proof

Files opened:

- `skills/implement/scripts/seal.py` (at `86e140f` and `8fb1fb5`)
- `tests/test_the_records_can_be_carried_out_and_in.py`
- `tests/test_release_hygiene.py`
- `seal/ledger.md` (the diff, and the ten touched rows)
- `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`
- `seal/specs/1788789329-a-git-call-that-fails-reads-as-no-remote/`:
  `routing.md`, `spec.md`, `questions.md`, `overview.md`, `changelog.md`
- `README.md`, `README.ko.md`
- `bin/test`, `bin/evidence-check`, `.github/scripts/run_tests.py` (head)
- `CLAUDE.md` (repository and user), `skills/agent-contract/SKILL.md`,
  `skills/code-review/SKILL.md`

Commands run are the Executed probes table above. Exit codes were read as
`cmd >/dev/null 2>&1; echo $?` or from the runner's own status, never through
a pipe.

Not run, and who answers: the full suite, the repository-wide lint and the
typecheck — `agent-contract` §2 reserves them for the orchestrator. The
Windows leg — CI. `ruff check` / `ruff format --check` on the changed files
are inherited as executed from the hand-back and were not re-run here;
`tests/test_lint_python.py` passed at the target, which is the closest thing
this round has to a check on them.
