# 1791240748-reverify-computes-once-and-judges-in-one-place — review round 1

| Field | Value |
|---|---|
| Target SHA | ca46718589d5f06cd2525056c52736a40f5f5e80 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #829 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `935b39180d0a8e3323b1ad3ddcb2a03a398f206e..bd9f9eb88a277f4443ec2af532fca38480e6c346`, 3 commits |
| Contract changes | cited_row → round-1-report.md, round-1.md, family_view, moved_and_left_out, pytest; on_a_cycle → round-1-report.md, round-1.md, reverify |
| New units | read_citation (depth 1); known_gone (depth 1); test_a_row_downstream_of_a_cycle_one_stale_row_starts_is_restamped (depth 1); test_a_row_that_never_settles_costs_no_round_per_coordinate (depth 1); test_reverify_names_a_citation_in_the_family_readers_words (depth 1); test_a_coordinate_whose_statement_is_gone_breaks_a_cycle (depth 1); test_a_coordinate_no_checkout_places_records_no_pact_change (depth 1); _two_moved_fragments (depth 1); test_the_record_is_the_same_bytes_in_any_ledger_order (depth 1) |
| Needs a fix | yes — 🟡 1 (downstream row left on an alternating cycle), 🟡 2 (a pass at its bound costs rounds × coordinates), 🟡 3 (a citation read by two readers), 🟡 4 (EXTERNAL and escaping coordinates recorded as BROKEN pact changes) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Spec compliance first against `spec.md` (one `judge` used by `--strict`, `--reverify` and `--reverify --into`; code coordinates judged once from disk; ledger coordinates, citations or not, judged against the planned ledger text until it stops changing, then one write; moves recorded as the pair before and after; #806 and #809 closed; a row that never settles named on a `LEFT` line with exit 1), then quality: the fixed-point loop's bound and its `on_a_cycle` exit attacked with self-citing rows, two-row cycles, a cycle through a released file, and a row that settles only on the last pass; the 112 classified `--reverify` differences from the differential probe, sampled to see whether each class is what it is called, with the 28 order-only differences as the likeliest place for a real behaviour change to hide; pact-change recording under the new write; the narrowed run's `moved_and_left_out`; the 46 re-pointed released rows and the eight `Corrected ·` choices against the claims they correct.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A row downstream of a cycle whose members move on alternate rounds is left and named does not settle; the result flips with an unrelated coordinate | `skills/evidence-check/scripts/evidence_check.py:3293` | **fixed** `63ca12a5` | fixed at 63ca12a5; Executed: the four-coordinate tree left D drifted with exit 1; spec D1, the docstring of on_a_cycle and the E3 Corrected row say a downstream row settles |
| 🟡 2 | A pass that reaches its bound re-judges every coordinate of the cycling file once per dynamic coordinate | `skills/evidence-check/scripts/evidence_check.py:3554` | **fixed** `8c73b19c` | fixed at 8c73b19c; Executed: 300 rows took 93.6 s with one self-quoting row and 2.4 s without; 3.3 s with the fix; 1,846 judge calls fell to 165 |
| 🟡 3 | A citation is read by the family reader in --strict and by judge in --reverify; they disagree on a duplicated literal and a duplicated section | `skills/evidence-check/scripts/evidence_check.py:3509` | **fixed** `63ca12a5` | fixed at 63ca12a5; Executed: BROKEN in --strict against a DRIFTED sentence or silence in --reverify; spec §12 claims the class closed; the 0.4.0 Corrected row at the fragment's line 41 is false |
| 🟡 4 | An EXTERNAL coordinate, or one escaping the repository, is recorded as a BROKEN pact change | `skills/evidence-check/scripts/evidence_check.py:3182` | **fixed** `63ca12a5` | fixed at 63ca12a5; Executed: the base recorded nothing and the branch records BROKEN; docs/the-pact.md defines BROKEN as unit, file or quoted statement gone |
| ⬜ 5 | The pact-change record's row order follows the --ledger order, which S4's sentence about every file does not allow | `skills/evidence-check/scripts/evidence_check.py:3599` | answered | resolve_patterns returns sorted(out), so the command line order of --ledger never orders the record; the order differences the reviewer saw were between base and branch; pinned by test_the_record_is_the_same_bytes_in_any_ledger_order, red when the sort is removed; Executed in one tree (rows swapped against the base); read for the permutation; no row's meaning changes |
| ⬜ 6 | Two Re-read rows vouch for released sentences written in terms of walks (E1, A4) | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | answered | corrected at bd9f9eb8 — E1 and A4 are Corrected rows now, with the walk wording removed; Records correction; the claims hold, the vocabulary names a removed mechanism |
| 🟢 | One judge reads every code coordinate for --strict, --reverify and --into | `skills/evidence-check/scripts/evidence_check.py:1669` | confirmed | Read: every caller found; executed: --strict . exits 0 at the target |
| 🟢 | #806 is closed: one run re-stamps a coordinate naming a line it moves, in any ledger order | `skills/evidence-check/scripts/evidence_check.py:3549` | confirmed | Executed: S2 and six S4 orderings, base exit 1, branch exit 0 |
| 🟢 | #809's cell C8 is closed for code coordinates, in place and under --into | `skills/evidence-check/scripts/evidence_check.py:1827` | confirmed | Executed: three trees, the move recorded where the base recorded BROKEN |
| 🟢 | A row that never settles is named on a LEFT line and the run exits 1 | `skills/evidence-check/scripts/evidence_check.py:3653` | confirmed | Executed in the differential and in the cycle probe |
| 🟢 | The differential's classes are what they are called, the 27 order-only differences included | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-2.md:80` | confirmed | Executed: re-run, 116 differences; the 4 beyond 112 come from later cases |
| 🟢 | Probe 3: both scripts write byte-identical fragments over this repository | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-4.md:21` | confirmed | Executed at 1f4d6cfc; 46 rows each; the same set of stdout lines |
| 🟢 | The eight Corrected choices match the claims they correct, apart from the two findings name | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | confirmed | Read: six hold; E3 at line 23 and 0.4.0 at line 41 turn true with the fixes for 1 and 3 |

## Paste-ready fixes

```python
def on_a_cycle(moving, spots, verdicts, among=None):
    """The keys of MOVING whose coordinate reaches itself (S6).

    MOVING is the coordinates whose verdict changed on the last round the
    bound allowed; SPOTS maps a key to its `Spot`, VERDICTS to the verdict
    that round gave it. A coordinate names the rows its verdict's region
    spans in its target file, and one whose naming leads back to its own row
    -- a row quoting its own line, or rows quoting each other -- has no
    hash the run can write that the write does not move again. A coordinate
    downstream of such a cycle is not on it, and settles once the cycle is
    left where it stands. AMONG, where given, is the keys the naming may
    pass through."""
    # The naming is read over every coordinate still judged, not over MOVING
    # alone: the members of a cycle one stale row starts move on alternate
    # rounds, so no single round's MOVING holds the whole cycle.
    live = [
        key
        for key in (spots if among is None else among)
        if verdicts.get(key) is not None
    ]
    names = {}
    for key in live:
        region = verdicts[key].region
        names[key] = [
            other
            for other in live
            if region is not None
            and spots[other].home == spots[key].target
            and region[0] <= spots[other].number <= region[1]
        ]
    found = set()
    for key in moving:
        if key not in names:
            continue
        stack, seen = list(names[key]), set()
        while stack:
            other = stack.pop()
            if other == key:
                found.add(key)
                break
            if other not in seen:
                seen.add(other)
                stack.extend(names[other])
    return found
```
```python
@pytest.mark.parametrize("unrelated", [0, 1, 2], ids=["none", "one", "two"])
def test_a_row_downstream_of_a_cycle_one_stale_row_starts_is_restamped(
    repo, unrelated
):
    """A quotes B's line and holds it; B quotes A's at a stale hash; D names
    B's line. Only B moves in the first round, so A and B move on alternate
    rounds and no one round's moving set holds both. One of A and B is left
    and named, and D, on no cycle, is re-stamped, however many unrelated
    coordinates name a written ledger. Red at ca467185 with one."""

    def names(label):
        return f'{R_FILE}#"{SECTION}">"\\| {label}"'

    b = f"| B · quotes A | `{names('A · quotes')}@0000beef` | read | 2026-01-01 | |"
    a = f"| A · quotes B | `{names('B · quotes')}@{line_hash(b)}` | read | 2026-01-01 | |"
    d = f"| D · names B | `{names('B · quotes')}@{line_hash(b)}` | read | 2026-01-01 | |"
    released(repo, [a, b, d])
    o = unit_hash(repo, "src/service.py", "other")
    rows = []
    for i in range(unrelated):
        z = f"| Z{i} · plain | `src/service.py#other@{o}` | read | 2026-01-01 | |"
        rows += [
            z,
            f'| E{i} · names Z | `seal/releases/0.2.0.md#"{SECTION}">"\\| Z{i} · '
            f'plain"@{line_hash(z)}` | read | 2026-01-01 | |',
        ]
    if rows:
        released(repo, rows, version="0.2.0")
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    named = [line for line in fix.stdout.splitlines() if "does not settle" in line]
    assert len(named) == 1 and "D · names B" not in named[0], fix.stdout
    check = run(["--strict", "."], repo)
    drifted = [line for line in check.stdout.splitlines() if "DRIFTED" in line]
    assert len(drifted) == 1, check.stdout
```
```python
    def rewrites(key):
        """Whether a re-stamp of KEY rewrites its row: not where `--checked`
        leaves the row whole for want of a date cell."""
        spot = by_key[key]
        header, cells = parsed[spot.key[0]].rows.get(spot.number, (None, []))
        return checked is None or (
            bool(cells) and date_column(header, cells) is not None
        )

    propagating = {key for key in by_key if rewrites(key)}
    texts = {ledger.home: ledger.text for ledger in parsed}
    pinned, earlier, changed = set(), {}, set(texts)
    while True:
        # Each pass is bounded, and a pass that reaches its bound leaves the
        # coordinates still moving on a cycle (`on_a_cycle`) and runs again
        # over the rest. A key once left stays left, so the passes end.
        moving, settled, looping = set(), False, set()
        for step in range(len(dynamic) - len(pinned) + 2):
            verdicts = judged_against(
                texts, [key for key in by_key if key not in pinned], earlier, changed
            )
            verdicts.update((key, None) for key in pinned)
            plans = planned(verdicts)
            following = {
                home: plans[home].text if plans[home].text is not None else original
                for home, original in ((ledger.home, ledger.text) for ledger in parsed)
            }
            moving = {
                key for key, found in verdicts.items() if found != earlier.get(key)
            }
            changed = {home for home in texts if following[home] != texts[home]}
            before, earlier, texts = texts, verdicts, following
            if not changed:
                settled = True
                break
            if step:
                # From a pass's second round on, a coordinate whose own row
                # this round rewrote again, on a cycle of rows each re-stamp
                # rewrites, cannot settle: waiting for the bound only judges
                # every coordinate of its file once per coordinate the run
                # carries.
                old = {home: gfm_lines(before[home]) for home in changed}
                new = {home: gfm_lines(texts[home]) for home in changed}
                rewrote = {
                    key
                    for key in (moving & propagating) - pinned
                    if by_key[key].home in changed
                    and old[by_key[key].home][by_key[key].number - 1]
                    != new[by_key[key].home][by_key[key].number - 1]
                }
                looping = on_a_cycle(rewrote, by_key, verdicts, propagating)
                if looping:
                    break
        if settled:
            break
        pinned |= looping or on_a_cycle(moving, by_key, verdicts) or moving
```
```python
def test_a_row_that_never_settles_costs_no_round_per_coordinate(repo, monkeypatch):
    """S6 beside forty citations of its file. The run leaves the self-quoting
    row once a round rewrites it again on its own cycle, rather than judging
    every citation of the file once per coordinate the run carries. Red at
    ca467185, which called judge 1,846 times here; 165 with the fix."""
    n = 40
    h = unit_hash(repo, "src/service.py", "handler")
    rows = [
        f"| R{i:02d} · handler adds one | `src/service.py#handler@{h}` | read "
        "| 2026-01-01 | |"
        for i in range(n)
    ]
    rows.append(
        f'| X · quotes itself | `{R_FILE}#"{SECTION}">"\\| X · quotes"@0000beef` '
        "| read | 2026-01-01 | |"
    )
    released(repo, rows)
    fragment(
        repo,
        [
            f"| Re-read · R{i:02d} | `{citation(rows[i], f'R{i:02d} · handler adds one')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
            for i in range(n)
        ],
    )
    edit_handler(repo)
    calls = []
    real = ec.judge
    monkeypatch.setattr(ec, "judge", lambda *a: calls.append(a) or real(*a))
    paths = sorted(str(p) for p in (repo / "seal").rglob("*.md"))
    ec.reverify(paths, str(repo), {}, None, "2026-03-01")
    assert len(calls) < 10 * n, len(calls)
```
```python
    def verdict_of(spot):
        """`judge`'s verdict for SPOT, except that a citation the family
        reader refuses takes that reader's status and sentence, the ones
        `--strict` prints for it: one citation, one reading (#809's class)."""
        verdict = judge(spot.m, root, maps, default_repo, scan_cache)
        if not spot.citation:
            return verdict
        files = {}

        def load(path):
            ident = file_identity(path)
            if ident not in files:
                body = read(path)
                files[ident] = (
                    None
                    if body is None
                    else (
                        path,
                        body,
                        gfm_lines(unquoted(body)),
                        {n: (h, c) for n, h, c in ledger_table_rows(body)},
                    )
                )
            return ident, files[ident]

        _header, cells = parsed[spot.key[0]].rows.get(spot.number, (None, []))
        status, detail, _ = cited_row(
            spot.m, citing_verb(cells), root, maps, default_repo, load
        )
        if status in ("OK", "DRIFTED"):
            return verdict
        return verdict._replace(status=status, detail=detail, now=None, dest=None)
```
```diff
-            index = (coordinate_of(spot.m), spot.m.group("hash"))
+            index = (coordinate_of(spot.m), spot.m.group("hash"), spot.citation)
             if index not in memo:
-                memo[index] = judge(spot.m, root, maps, default_repo, scan_cache)
+                memo[index] = verdict_of(spot)
@@ judged_against
-                    found[key] = judge(
-                        by_key[key].m, root, maps, default_repo, scan_cache
-                    )
+                    found[key] = verdict_of(by_key[key])
```
```python
@pytest.mark.parametrize("shape", ["literal twice", "section twice"])
def test_reverify_names_a_citation_in_the_family_readers_words(repo, shape):
    """A citation `--strict` reads BROKEN through the family reader -- its
    literal on two lines of its section, or its section there twice -- is
    named by `--reverify` with that sentence. Red at ca467185, which said
    the anchored statement is gone, or nothing, at exit 0."""
    h = unit_hash(repo, "src/service.py", "handler")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    released(repo, [r1])
    fragment(
        repo,
        [
            f"| Re-read · R1 | `{citation(r1, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    path = repo / R_FILE
    body = path.read_text(encoding="utf-8")
    if shape == "literal twice":
        body += r1.replace("2026-01-01", "2026-01-02") + "\n"
    else:
        body += (
            f"\n{SECTION}\n\n"
            "| R2 · other | `src/service.py#other@00000000` | read | 2026-01-01 | |\n"
        )
    path.write_text(body, encoding="utf-8")
    check = run(["--strict", "."], repo)
    (said,) = [
        line
        for line in check.stdout.splitlines()
        if "BROKEN" in line and "0.1.0.md#" in line
    ]
    detail = said.split('"R1 · handler adds one"', 1)[1].strip()
    fix = run(
        [
            "--reverify",
            "--checked",
            "2026-03-01",
            "--ledger",
            "seal/ledger/2000000001-a-later-item.md",
            ".",
        ],
        repo,
    )
    assert f'"R1 · handler adds one"  {detail} — left' in fix.stdout, fix.stdout
```
```diff
         left.append((spot, verdict.detail))
+        if verdict.status == "EXTERNAL" or spot.target is None:
+            # Another checkout this run was not given, or a path out of the
+            # repository: no unit, file or quoted statement is known gone,
+            # which is all the pact's BROKEN says, so MOVES gets no part.
+            continue
         pending.append((spot, None))
     dated, undated, undatable = [], [], []
```
```python
@pytest.mark.parametrize(
    "coord", ["legacy/src/x.py#f@0000beef", "../outside.py#f@0000beef"]
)
def test_a_coordinate_no_checkout_places_records_no_pact_change(repo, coord):
    """A row citing a clause beside a coordinate in another checkout the run
    was not given, or one escaping the repository: the run names it `left`
    and records nothing, because nothing is known gone. Red at ca467185,
    which recorded it BROKEN; e6d5a055 recorded nothing."""
    (repo / "seal" / "parity.md").write_text(
        "| Item | Value |\n|---|---|\n", encoding="utf-8"
    )
    cite(repo, [row("O1", f"`{CLAUSE}`, ", coord)])
    _code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert f"  {coord.rsplit('@', 1)[0]}  " in out, out
    assert record_rows(repo) == [], out
```

## Executed probes

| What was run | Result |
|---|---|
| A two-row cycle started by one stale row, with a row D naming B, with 0, 1 and 2 unrelated coordinates naming a written ledger | At the target, the tree with one unrelated coordinate left D and named it does not settle, exit 1, --strict 2; with the fix for 🟡 1, all three trees named one row and re-stamped D |
| A release file of 150 and of 300 rows, each cited from a fragment, with and without one self-quoting row, unfrozen --reverify --checked | 0.6 s and 11.7 s; 2.4 s and 93.6 s; with the fix for 🟡 2, 2.7 s and 3.3 s |
| judge calls counted in-process, 40 rows and one self-quoting row | 1,846 at the target; 165 with the fix |
| Differential: every --reverify call of the script in nine modules, base script first in the same tree, tree restored, then the branch | 562 calls: 446 identical, 72 left words, 27 order only, 17 named cells (C8 3, #806 7, S6 family 3, S8 1, D4 1, re-point section 1, record row order 1) |
| A pact-citing row with an EXTERNAL coordinate and with an escaping one, through both scripts | Base: no record row; branch: one BROKEN row each |
| A fragment citation whose literal is on two lines, and whose section heading is there twice, through both scripts | --strict BROKEN both; --reverify says a DRIFTED sentence, or nothing, at exit 0, on both scripts |
| D6 probe 3 at 1f4d6cfc in two archive copies, base and branch scripts | Both exit 1; fragments byte-identical, 46 rows; the same set of stdout lines |
| bin/evidence-check --strict . at the target | exit 0 |
| All four fixes applied in the clone, the eight modules that drive --reverify plus the four new cases | 832 passed; each new case failed at the target SHA |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet; the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
