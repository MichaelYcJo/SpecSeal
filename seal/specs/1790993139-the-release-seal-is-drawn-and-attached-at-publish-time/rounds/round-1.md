# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — review round 1

| Field | Value |
|---|---|
| Target SHA | 28c807fc07f7ad2f4721aa1a2fc10d4f8c1b6826 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 731 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `e01e1b1295ecb6a6da71333479b9bae8a20942f9..1d6ac8952991f834a3bcf7e7a19c2cd038666b77`, 9 commits |
| Contract changes | none |
| New units | test_a_record_another_version_wrote_names_its_own_group_and_a_capped_gate (depth 1); test_a_tree_whose_records_are_not_there_is_not_read_never_zero (depth 1); test_a_capped_pull_request_with_no_work_item_leaves_the_tree_rows_unread (depth 1); test_an_unlistable_rounds_leaves_rounds_unread_not_zero (depth 1); test_a_verdict_row_the_table_skipped_leaves_deferred_unread (depth 1) |
| Needs a fix | yes — 🔴 1 (the chain rows draw zeros for a tree they cannot read), 🟡 2 (two more incomplete reads become numbers), 🟡 3 (#722's bound does not hold for another plugin's record), 🟡 4 (no timeout on the seal job), 🟡 5 (the write token stays in `.git/config` during the suite) |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/publish-release.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 targets `28c807fc`, over the build's diff `233f0455..28c807fc`. It was asked to check the build against `spec.md` S1–S16 and the approved plan, then quality. Six things were named for close checking:
- whether every failure in the `seal` job leaves the published note intact, with the job exiting 0;
- whether `chain_counts`, which reads round records in the tree by Q1's decision, degrades to `not read` and never to a wrong number;
- the measured 0.17.0 reproduction (10, 27, 6, 12);
- #722's cap on write and on read, and the reserve's re-measured comment;
- Pillow as a test-and-release-only pin, with the gates kept on the stdlib and the interpreter floor;
- the ledger corrections and re-reads made in place in `seal/releases/`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A tree with no declarations (records moved by #715, items retired, or a capped pull request whose item is gone) gives the seal `0 . 0 rounds`, `capped N of 0`, `0 issues` with no log line, against S10, Q1 and `NOT_READ`'s own comment | `.github/scripts/release_seal.py:422` | **fixed** `7966a9f9` | fixed at 7966a9f9; Executed: `(0, 0, 1, 0)` over an empty root, nothing printed |
| 🟡 2 | An unreadable `rounds` counts its item's rounds as 0; a short verdict row's `deferred #N` is dropped because `verdict_table`'s errors are discarded | `.github/scripts/release_seal.py:428` | **fixed** `64196684` | fixed at 64196684; Executed: `(1, 0, 1, None)` and deferred `1` for two deferrals |
| 🟡 3 | `describe` expands a record's group from today's `GROUPS` even when the gate is not in it, and leaves the gate's file name uncapped; two gates reach 1,023 and 1,118 units against the 1,000 reserve, so the comment, D1 and 0.17.0 B1's corrected claim are false for the records the read-side cap exists for | `hooks/dispatch.py:468` | **fixed** `f118f7b5` | fixed at f118f7b5; Executed over the clone's `describe`; with the fix, 564/972/1,378 |
| 🟡 4 | The `seal` job and its suite step have no `timeout-minutes`, so a hung suite runs to the 360-minute default and ends outside every step's `continue-on-error` | `.github/workflows/publish-release.yml:69` | **fixed** `e91e33b9` | fixed at e91e33b9; Read; the runtime outcome is unverified, and the first hung run or the owner answers it |
| 🟡 5 | `actions/checkout` persists the `contents: write` token in `.git/config` during the suite step; the S5 docstring says the suite runs with none | `.github/workflows/publish-release.yml:76` | **fixed** `071c9005` | fixed at 071c9005; Read; answerable with grounds by changing the sentence |
| ⬜ 6 | The deferred row counts verdict cells only, not the record's `## Deferred` table, so 0.17.0 reads 12 against the owner's 13 | `.github/scripts/release_seal.py:445` | answered | The deferred row counts Verdicts cells only, by `questions.md` Q10's rule. A record's `## Deferred` table is not a verdict, so 0.17.0 reads 12; the changelog states the rule since round 2's ⬜ 11 (corrected at `4ac391e0`); the orchestrator's decision, with no code change; Decided by frame (Q10, overview *Not done*); a question for the repository owner |
| ⬜ 7 | The not-found refusal always says the note was edited, also when it was published as the section alone or the pull request set moved | `.github/scripts/release_seal.py:526` | **fixed** `626be3ab` | fixed at 626be3ab; Read |
| ⬜ 8 | The checklist's by-hand route does not say to run from a checkout at the tag, and stops at `gh release upload` without the edit | `docs/release-checklist.md:343` | **fixed** `318d3426` | fixed at 318d3426; Read |
| ⬜ 9 | The workflow comment says a re-run writes `false`; re-running the `seal` job alone keeps `created=true` | `.github/workflows/publish-release.yml:21` | **fixed** `93ff907a` | fixed at 93ff907a; Read; GitHub's re-run semantics not executed |
| 🟢 | The 0.17.0 reproduction holds: 10 items, 27 rounds, 6 capped, 12 deferred; #722 is named only in a `## Deferred` table | `.github/scripts/release_seal.py#chain_counts` | confirmed | Executed over a clone at `233f0455` with the live pull request list |
| 🟢 | Every exception inside `seal_release` ends as one `no seal:` line, one `::warning::` and exit 0; the module imports only the standard library | `.github/scripts/release_seal.py:549` | confirmed | Read; the 16 S2 cases passed (executed) |
| 🟢 | Pillow is test-and-release only: no file under `hooks/`, `skills/`, `bin/` or `.github/` imports it except `release_seal.py`; the floor module passes | `.github/scripts/run_tests.py#PILLOW` | confirmed | Executed: `grep -rnE "from PIL\|import PIL"` exit 1; floor module green |
| 🟢 | The 909 at base was stale: 538, 915 and 1,289 at `233f0455` | `skills/verify/scripts/seal_stamp.py#MESSAGE_RESERVE` | confirmed | Executed |
| ❓ | The `seal` job on GitHub's runners: the font Q11 names, the browsers Q9 names, and whether the suite at a tag push (detached HEAD, a tag-push event payload in `GITHUB_EVENT_PATH`) passes as it does on `push: main` | `.github/workflows/publish-release.yml` | ❓ out of verified scope | Nothing local can run it; the repository owner answers at 0.18.0's tag push, from the job log and the release page |

## Paste-ready fixes

```python
def chain_counts(root, pulls):
    # ... docstring as it stands, plus:
    # A tree with no declaration at all, or a pull request labelled
    # `CAPPED_LABEL` that resolves to no work item, is a count known to be
    # incomplete -- records moved (#715) or retired before the tag -- so the
    # three tree rows are not read rather than drawn as 0.
    capped = sum(1 for pull in pulls if CAPPED_LABEL in labels_of(pull))
    try:
        routing, chain, reader = readers()
    except Exception as problem:
        print(
            f"the chain rows are not read: the round-record readers did not load ({problem})"
        )
        return None, None, capped, None
    if not routing.declarations(root):
        print(
            "the chain rows are not read: no routing.md under "
            f"{root} declares a branch, so the round records are not where "
            "the readers look"
        )
        return None, None, capped, None
    items, rounds, deferred, unread, lost = 0, 0, set(), [], []
    for pull in pulls:
        item = routing.item_dir(root, pull.get("headRefName") or "")
        if not item:
            if CAPPED_LABEL in labels_of(pull):
                lost.append(f"#{pull.get('number')}")
            continue
        items += 1
        # ... the rest of the loop as in fix 2 ...
    if lost:
        print(
            f"the chain rows are not read: {', '.join(lost)} carry "
            f"{CAPPED_LABEL!r} and resolve to no work item under {root}"
        )
        return None, None, capped, None
    # ... the returns as in fix 2 ...
```
```python
def test_a_tree_whose_records_are_not_there_is_not_read_never_zero(tmp_path, capsys):
    """S10, `questions.md` Q1. A root with no declaration -- the records
    moved by #715, or retired before the tag -- leaves the three tree rows
    None, and the log says why; capped is read from the labels alone."""
    counts = seal().chain_counts(str(tmp_path), [pr(20, "feat/12-an-item", "chain: capped")])
    assert counts == (None, None, 1, None), counts
    assert "not read" in capsys.readouterr().out


def test_a_capped_pull_request_with_no_work_item_leaves_the_tree_rows_unread(tmp_path):
    """S10. A pull request labelled `chain: capped` was reviewed, so one that
    resolves to no declaration makes the item count incomplete."""
    root = tree(tmp_path, verdicts=[["deferred #12"]])
    pulls = [pr(20, "feat/12-an-item"), pr(21, "feat/99-retired", "chain: capped")]
    assert seal().chain_counts(root, pulls) == (None, None, 1, None)
```
```python
    rounds_unread = False
    for pull in pulls:
        # ... item resolution as in fix 1 ...
        items += 1
        if routing.rounds_unreadable(item):
            # Its records exist and cannot be listed, so its rounds are not
            # zero; the rounds row is not read, and neither is deferred.
            rounds_unread = True
            unread.append(os.path.join(item, routing.ROUNDS_DIR))
            continue
        records = routing.rounds(item)
        rounds += len(records)
        for path in records:
            try:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
            except (OSError, UnicodeDecodeError):
                unread.append(path)
                continue
            rows, col, _header, errors = chain.verdict_table(
                reader, reader.readable(text), path
            )
            # A row `verdict_table` skipped is a verdict nobody counted.
            if col < 0 or errors:
                unread.append(path)
                continue
            for _line, seen in rows:
                if chain.verdict_of(seen, col) == chain.DEFERRED:
                    deferred.update(int(n) for n in re.findall(r"#(\d+)", seen[col]))
    # ... `lost` check from fix 1 ...
    if unread:
        print(
            ("the rounds and deferred rows are" if rounds_unread else "the deferred row is")
            + " not read: no verdict table could be read in "
            + ", ".join(os.path.relpath(p, root) for p in unread)
        )
        return items, None if rounds_unread else rounds, capped, None
    return items, rounds, capped, len(deferred)
```
```python
def test_an_unlistable_rounds_leaves_rounds_unread_not_zero(tmp_path, capsys):
    """S10. A `rounds` that is a file holds records nobody can count."""
    root = tree(tmp_path)
    item = tmp_path / "seal" / "specs" / "1700000000-an-item"
    (item / "rounds").rmdir()
    (item / "rounds").write_text("# round 1\n", encoding="utf-8")
    assert seal().chain_counts(root, [pr(20, "feat/12-an-item")]) == (1, None, 0, None)
    assert "rounds" in capsys.readouterr().out


def test_a_verdict_row_the_table_skipped_leaves_deferred_unread(tmp_path):
    """S10. `verdict_table` skips a row too short for the Verdict column; a
    deferral in it is a count nobody made."""
    root = tree(tmp_path, verdicts=[["deferred #12"]])
    record = tmp_path / "seal" / "specs" / "1700000000-an-item" / "rounds" / "round-1.md"
    record.write_text(record.read_text(encoding="utf-8") + "| 2 |\n", encoding="utf-8")
    assert seal().chain_counts(root, [pr(20, "feat/12-an-item")]) == (1, 1, 0, None)
```
```python
    group = capped(flat(body.get("group")), NAME_CAP)
    # The gate's name is the record's FILE name, which another plugin's
    # gates name: capped like every other field without a fixed vocabulary.
    gate = capped(gate, NAME_CAP)
    phase = body.get("phase")
    how = {"load": "failed to load", "run": "failed while running"}.get(phase, "failed")
    error = capped(flat(body.get("error")), NAME_CAP)
    message = capped(flat(body.get("message")), MESSAGE_CAP)
    cause = f"{error}: {message}" if error and message else error or message
    groups = [group] if group else []
    # Expanded only where this plugin's `GROUPS` puts the gate in the group
    # the record names: a record whose pair this version would never write
    # (a gate that moved groups between versions) names its own group alone.
    if phase == "load" and gate in GROUPS.get(group, ()):
        groups += [g for g, gates in GROUPS.items() if gate in gates and g != group]
```
```python
def longest_report(d, count):
    """The longest report `count` failed gates can put before a stamp, in
    UTF-16 units, the blank line `report` adds included: every gate this
    plugin names and three foreign ones, in every group this plugin names and
    a foreign one, at every phase, with each field past its cap -- a record
    an older or newer plugin wrote is what the read-side caps are for."""
    fields = {"error": "E" * 300, "message": "m" * 400}
    gates = {g for gs in d.GROUPS.values() for g in gs} | {c * 300 for c in "xyz"}
    groups = [*d.GROUPS, "G" * 300]
    longest = {}
    for gate in gates:
        for group in groups:
            for phase in ("load", "run", None):
                line = d.describe(gate, {"group": group, "phase": phase, **fields})
                longest[gate] = max(longest.get(gate, ""), line, key=units)
    chosen = sorted(longest.values(), key=units, reverse=True)[:count]
    one = count == 1
    label = d.LABEL.format(
        count=f"{count} gate{'' if one else 's'}", verb="was" if one else "were"
    )
    return units("\n".join([label, *chosen, d.CLOSING])) + 2
```
```yaml
  seal:
    needs: publish
    if: needs.publish.outputs.created == 'true'
    runs-on: ubuntu-latest
    # A hung suite must end as a failed step, not as a job the runner ends at
    # its six-hour default: a step's `continue-on-error` does not reach the
    # job's own timeout, and the job's line below keeps the run green if it
    # is reached anyway.
    timeout-minutes: 60
    continue-on-error: true
    steps:
```
```yaml
      - name: run the suite at the tag
        id: suite
        continue-on-error: true
        timeout-minutes: 30
        shell: bash
```
```python
    # In the S5 case:
    assert "    timeout-minutes: 60" in seal and "    continue-on-error: true" in seal, seal
    assert any(line.strip() == "timeout-minutes: 30" for line in suite[0]), suite
```
```yaml
      - uses: actions/checkout@v4
        continue-on-error: true
        with:
          fetch-depth: 0
          # Nothing in this job pushes: the draw reaches GitHub through `gh`
          # and `GH_TOKEN`. So the token is not left in `.git/config`, where
          # every process of the suite at the tag could read it.
          persist-credentials: false
```
```python
    # In the S5 case:
    assert any(line.strip() == "persist-credentials: false" for line in held[0]), held[0]
```
```python
            for _line, seen in rows:
                if chain.verdict_of(seen, col) == chain.DEFERRED:
                    deferred.update(int(n) for n in re.findall(r"#(\d+)", seen[col]))
            # The record's own `## Deferred` table: its `Where it went` cell
            # is a deferral's home, the field round records keep for exactly
            # that (0.17.0's #722 sits only there).
            lines = reader.readable(text)
            for start in reader.sections(lines, "Deferred"):
                for line in lines[start + 1 : chain.section_end(lines, start)]:
                    cells = reader.split_row(line)
                    if cells and len(cells) >= 2 and not reader.is_separator(cells):
                        deferred.update(int(n) for n in re.findall(r"#(\d+)", cells[1]))
```
```python
    if body.count(table) != 1:
        raise Refused(
            "the glance table is not in the note exactly once as `glance` "
            "writes it for this release -- the note was edited after "
            "publication, went out without one, or the pull requests moved "
            "between the two lists; nothing was uploaded"
        )
```
```
      To draw one by hand, from a checkout at the tag, run
      `DRY_RUN=1 python3 .github/scripts/release_seal.py` with `TAG`,
      `REPO` and `SUITE_XML` set; attach the PNG it names with
      `gh release upload`, then apply the note it prints with
      `gh release edit --notes-file`.
```
```yaml
# Then the seal (#718). A second job, `seal`, runs only when `publish` created
# the release in this run (`created` is its output; a re-pushed tag or a full
# re-run finds a release already there and writes `false`, and a re-run of
# `seal` alone keeps `true` and meets the glance-table guard instead).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the release seal, release note and gate-failure modules, in the clone at `28c807fc` | 98 passed, exit 0 |
| `bin/test` on the interpreter-floor, runner, stamp and release-hygiene modules, in the clone | 198 passed, exit 0 |
| `evidence_check.py .` over the clone | exit 0; 0 drifted, 0 broken in every ledger file |
| `chain_counts` over an empty root (one capped, one plain pull request) | `(0, 0, 1, 0)`, no log line → 🔴 1 |
| `chain_counts` with `rounds` as a file | `(1, 0, 1, None)` → 🟡 2 |
| `chain_counts` with a short verdict row carrying `deferred #13` | deferred `1`, no log line → 🟡 2 |
| `chain_counts` over a clone at `233f0455` with `merged_pulls` for 0.17.0 through `tally` | `(10, 27, 6, 12)` |
| `gh release view` for v0.16.0 and v0.15.5 against `glance` rebuilt from `gh pr list` | no `\r`; the table occurs once in each |
| `describe` over every known gate and known group, at caps, with an inconsistent group/gate pair | two gates 1,023 → 🟡 3 |
| `describe` with two 123-character gate file names | two gates 1,118 → 🟡 3 |
| `describe` with the guard and the gate cap applied in memory, foreign gates and groups included | 564 / 972 / 1,378 |
| `describe` with a 19-unit name at base and at target | 538 / 915 / 1,289 at both |
| The broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
