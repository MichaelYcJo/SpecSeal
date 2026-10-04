# 1791076833-the-reverify-writer-records-before-it-restamps — review round 1

| Field | Value |
|---|---|
| Target SHA | 7517df8b5baa6c2a59783cba71c406353f523a41 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #756 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a vendored copy under `always` re-stamps a row citing no clause unrecorded), 🟡 2 (a doubled `Pact notify` row is read as its first value) |
| Loses a record or crashes | yes — 🟡 1 and 🟡 2 each re-stamp a moved row whose pact change `always` owes, with nothing recorded, so the drift that would record it is gone |

- [ ] Pass

## What this round was asked

Round 1 of work item `1791076833-the-reverify-writer-records-before-it-restamps` (#647 steps C and D, PR #756), target `7517df8b` against `release/v0.18.1` at `e141980a`. This is the first review of the carried C+D code and of the record-first writer. Spec compliance comes first: Decision 1 (carry, not merge), W1–W10 (the write order and what is on disk when the process dies at each step, the unreadable ledger, idempotence, the cases where nothing can be recorded, `always` with an unreadable declaration, left coordinates, honest `wrote` lines, strict reads of files the run rewrites, a named `LEFT` instead of a traceback), and K1/K2 (the carry diff shows only the marker and citation edits). Quality comes second. Enumerate failure points by construction, meaning every write step crossed with every way it can fail, and not by example. Execute what you claim. The orchestrator verified 12 changed test modules (1236 passed) and lint on the 17 changed Python files at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A copy with no `hooks/`, under `Pact notify \| always`, re-stamps a moved row citing no clause at exit 0 and records nothing; the plugin's copy then finds nothing to record | `skills/evidence-check/scripts/evidence_check.py:3717` | open | executed in a temporary signatory; contradicts spec W5 and W6 and `docs/the-pact.md:134` and `:300`; fix run in the clone: red then green, 184 passed |
| 🟡 2 | A `Pact notify` row written twice is read as its first value, so with `never` or the default first and `always` second a moved row citing no clause is re-stamped at exit 0, unrecorded and unannounced | `skills/evidence-check/scripts/evidence_check.py:3737` | open | executed for both first values; contradicts spec W6 and `docs/the-pact.md:133`; fix run in the clone: red then green |
| ⬜ 3 | Ledger claim rows `W1 ·` and `W2 ·` (walker, `cmarkgfm`) share labels with the spec's writer-contract clauses W1 and W2, beside rows `W8 ·` to `W10 ·`, which are those clauses | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1` | open | read; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 4 | This item's `plan.md` names a worktree by an absolute path under a real home directory, so `tests/test_no_real_identifiers.py` fails at the target | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24` | open | executed: `test_only_fixture_user_paths` fails at `7517df8b`; came in with `20f2207c`; a correction to the run's paperwork, not counted in `Needs a fix`, and the pull request's pytest job will fail on it |
| 🟢 | PR #749 round 1's blocking finding 1 is closed: an owed change that cannot be recorded re-stamps nothing on the five paths it named | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | executed: 17 cases red with the plan applied before the record; in place with no work item, no claim line and the ledger kept. The vendored path's `always` arm is this round's yellow 1 |
| 🟢 | PR #749 round 2's blocking finding 10 is closed: no step removes a ledger, and an `--into` that will not read is refused before anything is written | `skills/evidence-check/scripts/evidence_check.py:4962` | confirmed | read: the only removal is `write_atomic`'s temporary file; executed: the sibling case red under the apply-first mutation, a non-UTF-8 `--into` exit 2 and byte for byte |
| 🟢 | PR #749 round 2's yellow 11 is closed: no window between a re-stamp and its record remains | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | executed: the kill matrix, ten cells, each next run equal to a clean run |
| 🟢 | PR #749 round 1's yellow 2 is closed: a second identical run adds nothing, compared as the reader reads a cell | `skills/evidence-check/scripts/evidence_check.py:3821` | confirmed | executed: 3 cases red with the raw comparison |
| 🟢 | PR #749 round 2's yellow 12 is closed: a change re-landed after its revert is recorded | `skills/evidence-check/scripts/evidence_check.py:3813` | confirmed | executed: 2 cases red with the ever-recorded key |
| 🟢 | PR #749 round 2's yellow 13 is closed for the two shapes it named: an invalid `Pact notify` value, and an unparseable `Pact` row under `always` | `skills/evidence-check/scripts/evidence_check.py:3737` | confirmed | executed: both parametrisations red with `blind` forced false. The doubled-row shape is this round's yellow 2 |
| 🟢 | PR #749 round 2's yellow 14 is closed: a coordinate the re-read leaves is recorded `BROKEN` at all three exits | `skills/evidence-check/scripts/evidence_check.py:3133` | confirmed | executed: 3 cases red with the moves removed |
| 🟢 | PR #749 round 1's yellow 3 is closed: `amended` is judged at the record's current hash only | `skills/evidence-check/scripts/pact_check.py:848` | confirmed | executed: 1 case red |
| 🟢 | PR #749 round 1's yellow 4 is closed: `.`, `-` or `_` for or before the slash is refused | `skills/evidence-check/scripts/pact_check.py:240` | confirmed | executed: 7 cases red |
| 🟢 | PR #749 round 1's yellow 5 and round 2's yellow 15 are closed: the walker refuses what cmark-gfm does not render | `hooks/config.py:1050` | confirmed | executed: 474 cases red with the three refusals off; round 2's generator, 600,000 documents over seeds 11 and 23, no disagreement |
| 🟢 | PR #749 round 1's white 6 is closed: a pipe after an even backslash run is refused | `hooks/config.py:907` | confirmed | executed: 2 cases red |
| 🟢 | W8, W9 and W10 hold: no write claim before the write lands, strict reads of what the run writes, and a named `LEFT` line instead of a traceback | `skills/evidence-check/scripts/evidence_check.py:1097` | confirmed | executed: the six phase-2 cases fail against the carry commit's writer and pass at the target |
| 🟢 | K1 and K2 hold: the carry diff is marker renames and citations alone, and the tree names no work item it does not hold | `docs/the-pact.md` | confirmed | executed: `git diff b4c9deb2 2d2387fd` over the carry set, 31 lines, each a marker or a citation; `git grep 1791019474` outside this item's records, nothing |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `7517df8b` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the smith's `unverified` label is honest |

## Paste-ready fixes

```python
# beside NOT_RESTAMPED in skills/evidence-check/scripts/evidence_check.py
# A `Pact notify` row as a copy with no `hooks/` can see one: its item cell,
# whatever the value says, because that copy cannot read the value.
NOTIFY_ROW_RE = re.compile(r"^[ \t]{0,3}\|[ \t]*Pact notify[ \t]*\|", re.M | re.I)
```
```python
    config = plugin_module(CONFIG_READER, "specseal_config_for_pact_changes")
    if config is None:
        # A copy with no `hooks/` reads no `Pact notify` value either, so
        # where the signatory's config.md has a `Pact notify` row, or will not
        # read, a moved row citing no clause may be owed under `always`, and
        # this copy cannot rule it out (the writer's contract, W5 and W6).
        declaration = os.path.join(seal_home(root), "config.md")
        said = read(declaration) if os.path.lexists(declaration) else ""
        blind = said is None or bool(NOTIFY_ROW_RE.search(said))
        unknown = [e for e in entries if e[3] or blind]
        for where, _row, _parts, anchors in unknown:
            why = (
                "cites a pact clause"
                if anchors
                else "moved, and `Pact notify` may be `always`"
            )
            print(
                f"  LEFT  {where}  {why}, and this copy of evidence_check.py "
                "has no hooks/ beside it to read the `Pact` row with — "
                f"{NOT_RESTAMPED}; run the plugin's `evidence-check --reverify` "
                "where the signatory is checked out"
            )
        return 1 if unknown else 0
```
```markdown
`hooks/` beside it cannot read the `Pact` row; it names each row citing a
pact, and each other row whose code moved where `seal/config.md` has a `Pact
notify` row it cannot read, says it recorded nothing, and re-stamps nothing,
so the plugin's own checker records the change where the signatory is
checked out.
```
```python
def test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause(
    repo, tmp_path
):
    """A copy with no `hooks/` cannot read `Pact notify`, so under a
    `Pact notify` row a moved row citing no clause is left, not re-stamped
    (round 1, yellow 1)."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), ("Pact", PACT_URL), ("Pact notify", "always")),
        encoding="utf-8",
    )
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    done = subprocess.run(
        [sys.executable, str(vendored), "--reverify", "--into", FRAGMENT,
         "--checked", "2026-09-04", str(repo)],
        cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert "moved, and `Pact notify` may be `always`, and this copy of" in out, out


def test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause(
    repo, tmp_path
):
    """With no `Pact notify` row the default records citing rows alone, so
    the vendored copy still re-stamps a row citing no clause."""
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O2", "", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    done = subprocess.run(
        [sys.executable, str(vendored), "--reverify", "--into", FRAGMENT,
         "--checked", "2026-09-04", str(repo)],
        cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 0, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8"), out
```
```python
    # A row citing a pact is owed under any `Pact notify`; a row citing none
    # is owed under `always`, and a declaration that will not read cannot say
    # it is not `always`, so such a row is unknown (round 2 of PR #749,
    # yellow 13). A `Pact notify` row refused -- written twice, say -- has no
    # value either, whatever its first row says (round 1, yellow 2).
    notify_refused = declared is not None and any(
        refusal.startswith(f"`{config.PACT_NOTIFY_ROW}") for refusal in declared[2]
    )
    blind = (
        declared is None
        or declared[1] in (None, config.NOTIFY_ALWAYS)
        or notify_refused
    )
```
```python
@pytest.mark.parametrize("first", ["never", "when the pact is touched"])
def test_a_notify_row_written_twice_leaves_a_row_citing_no_clause(repo, first):
    """A `Pact notify` row written twice is refused and has no value, so a
    moved row citing no clause is left, not re-stamped (round 1, yellow 2)."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"),
            ("Pact", PACT_URL),
            ("Pact notify", first),
            ("Pact notify", "always"),
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "`Pact notify` may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the two pact-check modules and `tests/test_gates_do_not_fail_open.py` at the target | 145 passed |
| `bin/test` over the 17 unchanged modules that drive `--reverify` | 1046 passed |
| `bin/test` over the 12 changed test modules | 1236 passed |
| Round probes in a temporary signatory: a vendored copy under `always`; a doubled `Pact notify`; three record header spellings; in place with no work item; a non-UTF-8 `--into` | 🟡 1 and 🟡 2 reproduced; the header spellings append under the header with no traceback; no claim line without a write; `--into` refused at exit 2, byte for byte |
| Kill matrix: a kill after each write and a kill inside each write (temporary sibling half-written), then a normal run, compared file by file with one clean run | all ten cells equal to the clean run; the record never appended twice |
| The same matrix with `--checked` older than the rows' own dates | a second `Re-read ·` row on any re-run; the same at `e141980a` and `b4c9deb2` with no pact; #746's stale `--checked`, deferred below |
| The six W8–W10 cases against `evidence_check.py` from `2d2387fd` | 6 failed, 4 passed (the four pin carried behaviour) |
| Nine mutations, each fix of PR #749's rounds taken back out, its module run, the file restored | every mutation red, counts in the table above |
| Round 2 of PR #749's generator, 300,000 documents, seeds 11 and 23 | 0 disagreements, 0 oracle mismatches |
| The paste-ready fixes below, applied in the clone with their cases, then reverted | new cases 3 red without the code fix, 4 green with it; the writer, `test_pact_check.py`, the review module and the declaration module 184 passed |
| `bin/evidence-check --ledger` over this item's fragment | exit 0; 223 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| `tests/test_no_real_identifiers.py` at the target | 1 failed, 4 passed: `test_only_fixture_user_paths` on this item's `plan.md:24` (⬜ 4) |
| This report, copied into the clone and marked for adding (not committed), through the records arm and the identifier check, then removed | records arm 0 refused, 0 drifted; the identifier check names `plan.md:24` alone, nothing in this report |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# Fixture: the freeze, a released row R1 citing the clause, and three
# fragments (the --into one among them) each with a citing row; the code
# under all four moved. Four writes: the record, then the three ledgers.
# For k in 1..5 and mid in (False, True): write_atomic is wrapped to die
# (os._exit(137)) after its k-th call, or, with mid, inside its k-th call
# after writing half of a temporary sibling. Then a normal --reverify --into
# --checked runs, and every file under seal/ is compared with one clean run.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A second `--reverify --into` with a `--checked` older than the released row's own date appends a second identical `Re-read ·` row, because the new row is not the family's newest reading; the same at `e141980a` with no pact | #746, a stale `--checked` under `--into`, which the spec keeps out of this item | #746's work item, in this release |
| `--migrate` reads a ledger leniently and writes it back (`evidence_check.py:2725` and `:2845`), so a byte that is not UTF-8 becomes U+FFFD. This is W9's class outside `--reverify`, in code this branch does not touch | a new issue | the orchestrator, who files it |
