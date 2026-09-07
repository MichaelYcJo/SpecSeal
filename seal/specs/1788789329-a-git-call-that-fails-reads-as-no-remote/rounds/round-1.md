# 1788789329-a-git-call-that-fails-reads-as-no-remote — review round 1

| Field | Value |
|---|---|
| Target SHA | 8fb1fb533c700f43e07c69a9c72cada5b1734234 |
| Ran by | warden on claude-opus-5 |
| PR | 234 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | manifest_of → round-1-report.md, round-1.md, export |
| New units | the_stem_the_export_will_use (depth 1); test_a_manifest_remote_of_the_wrong_type_refuses (depth 1); test_the_advice_names_the_machine_that_can_fix_it (depth 1); test_the_export_says_what_it_could_not_read (depth 1); test_an_export_that_read_everything_says_nothing_extra (depth 1) |
| Needs a fix | yes — findings 1, 2 and 3. A guard whose only signal is key |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of `1788789329-a-git-call-that-fails-reads-as-no-remote` (ticket #111, PR #234), at target `8fb1fb5`, base `86e140f`. No prior rounds.

Judged against five acceptance criteria: the call sites distinguish *no remote* from *unanswerable*; the escape is a flag of its own (the owner's decision, before the first edit — the implementation is what is judged); the manifest omits what could not be read and every reader copes; `other_worktrees` carries its sentence; new cases were seen red.

Five targets were named in order. `seal/ledger.md` was edited — one row removed, nine re-stamped — and `CLAUDE.md` §*a change writes fragments* permits exactly the removal case, so both halves were to be opened and the branch's own `git archive` check re-run rather than inherited. The measurement the design rests on (`git config --get` exits 1 for an unset key, 128 for an unparseable config) was to be re-run against a scratch repository. The promotion of `git_asked` out of three callers was to be checked for behaviour change. The manifest's three states were to be enumerated against every reader by construction, including zips written by earlier versions. And the class was to be re-derived at both commits rather than inherited, because a fix pass's own commit producing the next round's finding is this repository's most-measured regression shape.

`11 mutations, all killed` was named as an aggregate to re-run rather than accept, at least for the two that would hurt most.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A manifest whose `remote` is present but not a string walks past the new refusal — `null`, `42`, `[]`, `{}` and `true` all import at exit 0 with both guards silent | `skills/implement/scripts/seal.py:1048` | **fixed** `60d5354` | fixed at 60d5354; Executed at `8fb1fb5`: five parametrised values, all exit 0 with the record written. The guard's only signal is key absence; `theirs` is never type-checked, and `normalise_remote` turns every non-string into `""` |
| 2 | The refusal advises re-running an import that can never succeed, when the silent side is the zip rather than this clone | `skills/implement/scripts/seal.py:1067`, `README.md:526` | **fixed** `60d5354` | fixed at 60d5354; Executed at `8fb1fb5`: a zip whose manifest is `{"format": 1}` refuses and prints `Run this again if the failure was transient`. The `remote` key is absent in the bytes on disk, so no re-run can change it |
| 3 | The export writes a zip that will be refused on arrival and says nothing; `manifest_of` discards the reason it holds | `skills/implement/scripts/seal.py:406-411` | **fixed** `60d5354` | fixed at 60d5354; Executed at `8fb1fb5`: with `config --get` timing out, the export exits 0, omits `remote`, and the word `remote` appears nowhere in its output. The exporting machine is the only one that can clear the failure |
| 4 | `remote_url`'s docstring enumerates exit 1's meanings and misses `git -C <not a repository>`, which also exits 1 with empty streams | `skills/implement/scripts/seal.py:194-213` | **fixed** `60d5354` | fixed at 60d5354; Executed measurement against git 2.50.1. Not reachable through `resolve`, so a documentation correction rather than a defect — but the enumeration is what a later reader will use to judge a new `answered=(0, 1)` caller |
| 5 | `manifest_of` admits `remote` on `is not None` and `head` on truthiness, two spellings of one question five lines apart | `skills/implement/scripts/seal.py:407-411` | **fixed** `60d5354` | fixed at 60d5354; Read. Identical behaviour today, argued in `head_sha`'s docstring; the shorter spelling is the one that would silently drop a legitimate empty answer if `head_sha` ever gained one |
| 6 | Five call sites of `git()` at the base, `:953` included; exactly one at the target | `skills/implement/scripts/seal.py` | answered | Re-derived independently by `grep -n 'git('` before reading `spec.md`'s table, at both commits. Matches. The fix pass added no new member: `git_asked`, `remote_url` and `head_sha` all return `(value, why)`, so a caller cannot read a value as a fact without the reason beside it |
| 7 | Nine `seal/ledger.md` rows re-stamped, one removed; the drift is this branch's alone | `seal/ledger.md` | answered | Executed: base tree extracted at `86e140f` reads `764 ok · 0 drifted`, so nothing was stale before this branch. All nine anchors are `import_` or `other_worktrees`, the two units edited. I opened all nine claims — zip bounds, member ordering, manifest typing, the worktree note — and none is falsified. Target reads `776 ok · 0 drifted` |
| 8 | The removed row `S4 · a repository with no commit records an empty head` | `seal/ledger.md`, `seal/ledger/1788789329-…md` | answered | Its claim is false at the target: `head` is now absent, not empty. The replacement claim is R2 in the branch's own fragment, which is what `CLAUDE.md` §*a change writes fragments* prescribes. Anchor arithmetic checks out — one row, two anchors, 764 → 762 |
| 9 | The `Checked` date on the nine re-stamped rows still reads `2026-09-03` | `seal/ledger.md` | answered | Already disclosed by the implementer and routed to the repository owner in `overview.md` §*Not verified*. Not re-raised |
| 10 | README and record modules the hand-back did not run | `README.md`, `README.ko.md`, the work item's records | answered | Executed at `8fb1fb5`: ten modules, `355 passed`, exit 0. The `unverified` label on the broad gate is honest — what was left out is the full suite, not these |

## Paste-ready fixes

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
```markdown
when the remote could not be read on either side and so that question cannot
be answered at all (`--allow-unreadable-remote` to import without the check —
a separate flag, because *there is no remote* and *nobody could say* are
different facts). Which side went silent decides what to do next: a git that
failed here may answer on the next run, while a zip that records no remote
reads the same every time and has to be exported again on the machine that
wrote it,
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a re-stamped row's `Checked` date should move | `overview.md` §*Not verified*, row 5 | the repository owner |
| `porcelain`, `indexed`, `tracked` and `gitlinks_under_root` moved onto `git_asked` | `overview.md` §*Not done*, paragraph 1 | whoever next edits one of them for a reason of its own |
| Whether `git config --get` exits 1 for an unset key on builds other than 2.50.1 | `overview.md` §*Not verified*, row 3 | the repository owner. Finding 4 narrows the question rather than reopening it |
| Windows | `overview.md` §*Not verified*, row 4 | CI's Windows leg |
