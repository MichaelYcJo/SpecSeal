# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — review round 1

| Field | Value |
|---|---|
| Target SHA | 626bdeb68fb19a0309644056c93afda44a273a7b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 736 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (`--into` writes a broken coordinate), 🟡 2–7 (the union's stated cost, the partial correction, the double correction, the pipe citation in `correction-check`, fragment row 25, the release checklist's §3 row) |
| Loses a record or crashes | yes — 🔴 1 writes a re-read row whose coordinate is a bare hash and reports it written, so the reading it was asked to record is lost; 🟡 5 lets a dropped `Corrected ·` row pass `correction-check` unreported |

- [ ] Pass

## What this round was asked

Round 1 targets `626bdeb6`, over the build's diff `233f0455..626bdeb6`. It was asked to check #715 against `spec.md` D1–D8 and S1–S15 and the approved plan, then quality. Eight things were named for close checking:
- whether the family verdict (D3) can make a false claim read OK;
- whether the citation literal (W1) can resolve to the wrong row;
- whether re-pointing a moved anchor by a `Corrected ·` row is sound;
- whether the freeze (D5) ever refuses a work item below its cutoff, including the three sibling branches of this release after they merge;
- the fold's and settle's changes (D6);
- whether any carrier lost a rule it alone stated when the rules got one home each;
- the branch's own `Re-read ·` and `Corrected ·` rows, and S12's zero bytes under `seal/releases/`;
- the interpreter floor of the shipped scripts.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `--into` slices the family root's line with a match from another member, writes a bare hash for the coordinate and reports the row written | `skills/evidence-check/scripts/evidence_check.py:3198` | open | executed: the row carried `` `90309471` `` for `src/service.py#other`, exit 0, drift still reported; fixed in the scratch clone with `m.string` |
| 🟡 2 | the per-coordinate union reads OK a pair of hashes no reading recorded together, and the home's stated cost says somebody read it | `skills/evidence-check/scripts/evidence_check.py:2402`, `docs/the-evidence-ledger.md:102` | open | executed: R at (h1,o1), re-read at (h2,o2), revert to (h1,o2) reads 5 OK, exit 0; the replaced in-place rule reads DRIFTED |
| 🟡 3 | a `Corrected ·` row re-pointing one moved coordinate silences the row's other coordinates, and the repair text invites that row | `skills/evidence-check/scripts/evidence_check.py:3217`, `docs/the-evidence-ledger.md:121` | open | executed: after the partial correction an edit to `other` reads exit 0 |
| 🟡 4 | two `Corrected ·` rows correcting one released row both read OK and nothing names them | `skills/evidence-check/scripts/evidence_check.py:2374` | open | executed: contradictory corrections, exit 0, 4 OK; spec D3 is silent on it |
| 🟡 5 | `correction-check` keys a closing-pipe citation on the next coordinate, so its dropped row is never reported | `skills/evidence-check/scripts/correction_check.py:583` | open | executed: key `src/service.py#handler`; `dropped_corrections` then skips it (read); fixed in the scratch clone |
| 🟡 6 | the fragment's row 25 re-reads the per-file dedup claim, which family rows no longer obey | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25` | open | executed: one file goes from 1 ok to 2 ok for one `(coordinate, hash)` once a row is in a family |
| 🟡 7 | the release checklist's §3 drift row prescribes plain `--reverify --checked`, which writes no released file under the freeze | `docs/release-checklist.md:199` | open | read; the 0.18.0 preparation is its first reader |
| ⬜ 8 | the home's REMOVED-not-re-pointed sentence is unqualified beside the freeze's never-removed, re-pointed-by-correction rule | `docs/the-evidence-ledger.md:37` | open | read |
| ⬜ 9 | a row whose first cell also ends another cell of its section gets no citation | `skills/evidence-check/scripts/evidence_check.py:2160` | open | executed: `citation_for` returns None; 0 corpus rows have the shape |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, reverify_into
    for key in sorted(drifted, key=lambda k: (view.files[k[0]][0], k[1])):
        path, body, _, table = view.files[key[0]]
        # ... unchanged down to the stamping loop ...
        stamped = []
        for coord, m in drifted[key].items():
            new = current_hash(m, root, maps, default_repo)
            if new is None:
                left.append((where, f"{coord} — no one place to hash, so not re-read"))
                continue
            # M may come from any released member of the family, not from
            # KEY's own line (`released_drift`): slice the line it was matched on.
            stamped.append(spanned(m.string[m.start() : m.start("hash")] + new))
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_into_re_reads_a_coordinate_a_folded_re_read_carries(repo):
    """The drifted coordinate sits on a folded `Re-read ·` row, not on the
    family's root: the row `--into` writes names it whole (warden round 1)."""
    handler = unit_hash(repo, "src/service.py", "handler")
    other = unit_hash(repo, "src/service.py", "other")
    (row,) = released(
        repo, [f"| R1 · handler adds one | `src/service.py#handler@{handler}` | read | 2026-01-01 | |"]
    )
    folded = (
        f"| Re-read · R1 · handler adds one | `{citation(row, 'R1 · handler adds one')}`, "
        f"`src/service.py#other@{other}` | read | 2026-02-01 | Re-read 2026-02-01 by work item 2 |"
    )
    released(repo, [folded], version="0.2.0", section="### 2000000001-a-later-item")
    (repo / "seal" / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Ledger frozen from | 0 |\n"
    )
    (repo / "src" / "service.py").write_text(SERVICE.replace("x * 2", "x * 7"))
    r = run(
        ["--reverify", "--into", "seal/ledger/3000000001-y.md", "--checked", "2026-03-01", "."],
        repo,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    written = (repo / "seal" / "ledger" / "3000000001-y.md").read_text()
    assert f"`src/service.py#other@{unit_hash(repo, 'src/service.py', 'other')}`" in written
    assert run(["--strict", "."], repo).returncode == 0
```
```markdown
neither matches. Its cost is stated in two parts. Content that returns to a
hash an earlier reading recorded reads OK again, because somebody read the
claim against that content. And the union is per coordinate, not per
reading: a row citing two units is OK when each unit matches some reading,
though no reading may have seen that pair together. A partial revert lands
there — one unit back at an old reading, the other at a newer one — and a
claim about how the two units fit can be false while it reads OK. The in-place
re-stamp this replaced kept one hash per unit and read that state DRIFTED.
```
```python
# skills/evidence-check/scripts/evidence_check.py, reverify_into
    for at, coord, detail in broken:
        left.append(
            (
                at,
                f"{coord} BROKEN — {detail}; a re-read cannot clear it, so a "
                "`Corrected ·` row in your own fragment re-points or retires it — "
                "and carries every other coordinate the claim still rests on, "
                "because the correction supersedes the whole row and a "
                "coordinate it leaves out is not checked again",
            )
        )
```
```markdown
row whose anchor moved is not cleared by a re-read, because the family is
keyed on the coordinate, and a `Corrected ·` row re-points it. That row
supersedes the whole released row, so it carries every coordinate the claim
still rests on, the moved one at its new place: a coordinate it leaves out is
not checked again.
```
```python
# skills/evidence-check/scripts/evidence_check.py, family_view, after `superseded = {...}`
    # A released row corrected by more than one row carries two claims and
    # nothing reconciles them: the conflict two in-place corrections used to
    # meet on is gone, so the checker names the pair instead (warden round 1).
    corrected_by = {}
    for key in parent:
        if verb_of(key) == "Corrected" and root_of(parent[key]) != key:
            corrected_by.setdefault(root_of(parent[key]), []).append(key)
    for top, keys in corrected_by.items():
        if len(keys) < 2:
            continue
        keys.sort(key=lambda k: (str(k[0]), k[1]))
        names = ", ".join(where(k) for k in keys)
        for key in keys:
            emit(
                key,
                (
                    "DRIFTED",
                    coordinate_of(citations[key]),
                    f"the row it cites is corrected by {len(keys)} rows ({names}) "
                    "— read them together and keep one claim",
                ),
            )
```
```python
# skills/evidence-check/scripts/correction_check.py, beside CORRECTED_ROW
# A citation's locator is quoted, and a quoted segment may hold `\|` -- the
# closing-pipe literal `citation_for` writes, or a heading with a pipe in it.
# `ANCHOR` stops at any `|`, so it is tried second.
CITATION = re.compile(
    r'([^\s`|]+\.[A-Za-z0-9]+#"(?:[^"\\]|\\.)*"(?:>"(?:[^"\\]|\\.)*")?)@[0-9a-f]{6,}'
)


def corrections(text):
    """`{citation: row}` for every `Corrected ·` row of `text`."""
    found = {}
    for row in rows(text):
        if not row.key.startswith(CORRECTED_ROW):
            continue
        cited = CITATION.search(row.raw) or ANCHOR.search(row.raw)
        if cited:
            found.setdefault(cited.group(1).strip(), row)
    return found
```
```markdown
| Corrected · `check_text` de-duplicates on `(coordinate, hash)` within one file for the rows no family reads; a row that cites a released row, or is cited by one, is graded per row by `family_view`, which does not de-duplicate, so once citing rows fold a fold moves the `ok` total by more than the rows two files cited identically | `seal/releases/0.4.0.md#"#### The fold is a move, marked and ordered">"The checker de-duplicates"@1e14ea36`, `skills/evidence-check/scripts/evidence_check.py#check_text@c4b73b1a`, `skills/evidence-check/scripts/evidence_check.py#family_view@59d80192` | **Executed** <date>: one release file with two rows citing one `(coordinate, hash)` prints `1 ok`, and `2 ok` once a fragment re-reads one of them | <date> | Corrected <date> by work item 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes: the family reader grades a cited row outside `check_text`'s per-file `seen` |
```
```markdown
| `evidence-check --strict` | rows anchored on units the preparation edited read as drifted. Where `seal/config.md` declares `Ledger frozen from`, as this repository does, re-read every row citing them, write the re-reads with `--reverify --into seal/ledger/<unix-seconds>-fold.md --checked <date>`, and fold that fragment with a second `fold_ledger.py --version X.Y.Z` in the same commit, which joins the release's file; plain `--reverify` writes no released file and exits 1 naming each row. Without the row, `--reverify --checked <date>` narrowed with `--ledger` to the files read, in the same commit. The total can drop across a fold: two fragments citing one coordinate identically fold into one row, and the unique-anchor count is what stays equal |
```
```markdown
removes. **A row whose anchor a change removes is `REMOVED`, not re-pointed**
— its claim went with the code, and the new claim is a new row. Under the
freeze a released row is never removed: a `Corrected ·` row retires it, or
re-points a moved one (§*A released row is read again in the branch's
fragment*).
```
```python
# skills/evidence-check/scripts/evidence_check.py, unique_literal, before `return None`
# (not executed in round 1)
    # The cell whole, with the row's leading pipe: no other cell begins a line.
    whole = "| " + " ".join(cell.split()) + " |"
    if not LITERAL_STOP_RE.search(whole[2:-2]):
        hits = literal_statements(lines, region, whole)
        if len(hits) == 1 and hits[0][0] == number:
            return whole
```

## Executed probes

| What was run | Result |
|---|---|
| S12: `git diff --name-only 233f0455...HEAD -- seal/releases`; hunks in `seal/ledger.md` | 0 files; 1 hunk, in the header above the first table |
| the new and changed modules in the clone: `bin/test` on the five ledger test modules | 179 passed |
| `tests/test_docs_line_wrap.py` | 35 passed |
| `evidence_check.py .` at HEAD under 3.12 / `--strict` under 3.9.6 / at the base under both | HEAD 3.12: 3776 ok, 0 drifted. HEAD 3.9: 8 drifted. Base 3.12: 0 drifted. Base 3.9: the same 8 drifted |
| py_compile of six shipped scripts under 3.9.6; `correction_check.py --range 233f0455...HEAD` under 3.9.6 | all 0; exit 0 with the exempt line for 1790993138 |
| sibling merges (#647, #718, #716, all three) into the tip, then `evidence-check --strict` and `correction-check --range <tip>...<merge>` | 0 conflicts; correction-check exit 0 with the exempt line for each; strict drift 6, 3, 0, 9 |
| M2 end to end: `citation_for` → fragment row → `ANCHOR_RE` → `cited_row`, and `corrections()` | 1,083 rows, 0 without a citation, 0 wrong rows, 0 misread; 0 fallback; 215 literals under 8 chars |
| P1: joint revert (🟡 2) | exit 0, 5 OK at a pair nobody read |
| P2: moved anchor and partial correction (🟡 3) | BROKEN, then LEFT by `--into`, then exit 0 after the correction, then exit 0 after `other` changed |
| P3: `Corrected ·` row with no marker | MALFORMED, exit 1 lenient and 2 strict; it still supersedes |
| P4: two contradicting corrections (🟡 4) | exit 0, 4 OK |
| P5: first cell repeated in another row's last cell (⬜ 9) | `citation_for` → None |
| P6: `--into` with a folded re-read member (🔴 1) | wrote `` `90309471` ``, exit 0; with the `m.string` fix: wrote the full coordinate, then strict exit 0 |
| pipe citation through `corrections()` (🟡 5) | key `src/service.py#handler`; with the `CITATION` fix: the citation |
| dedup (🟡 6) | release file 1 ok → 2 ok once one row is in a family |
| the two touched modules with both fixes applied in the clone | 101 passed |
| `fold_ledger.py --check` at HEAD | exit 1, naming only this branch's unfolded fragment: expected on a feature branch |
| the broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the newest-dated-per-coordinate rule as a replacement for the plain union (🟡 2's second option) | spec D3, as a question beside the stated cost | the repository owner |
| who re-stamps this fragment's 9 citing rows when #647 and #718 land before or after this branch | the orchestrator's handoff to the second lander | the orchestrator of the 0.18.0 run |
