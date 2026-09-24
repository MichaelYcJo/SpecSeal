# 1790208593-the-fold-writes-each-release-to-its-own-file — review round 1

| Field | Value |
|---|---|
| Target SHA | 577f16712a809498803a94be308196db79eb4c6a |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 558 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `635627c70b6c16dc0c1e9428efa47687e7ebc70e..47ca9ce68ab744c4d249aa25e66d6650f02c5097`, 6 commits |
| Contract changes | none |
| New units | test_the_split_names_only_the_anchors_it_cannot_place (depth 1); test_each_identical_rewrite_prints_its_own_line (depth 1) |
| Needs a fix | yes — 🟡 1 (the split's anchor reading), 🟡 2 and 🟡 3 (the totals claim in the checklist, the policy document and the docstring), 🟡 4 and 🟡 5 (documents and comments naming the old fold target) |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/hygiene.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 was asked to review the branch at 577f1671 against step C's built tip 9f5902e5, which it stacks on: spec compliance first against `spec.md`, `plan.md` and the gate table for every new `--check` arm and every widened reader, then quality, in a clone under the round's own directory, narrow runs only, with the smith's handoff before round 1 as the account to audit — and to probe `--split` against a copy of the real ledger itself: every row in exactly one file, a second split refusing, the checker's totals the same before and after. The two edits the smith left to the owner (`CLAUDE.md`, `seal/README.md`) were out of its findings; it was asked whether any other shipped or loaded document still says the fold writes into `seal/ledger.md`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `--split` reads an anchor by a looser rule than the checker, so its dry run names a kept header-line anchor and a hashless prose mention as unplaceable, truncates an escaped quote, and leaves a line anchor into a moved section unrewritten | `.github/scripts/fold_ledger.py:460` | **fixed** `63fbfa52` | fixed at 63fbfa52 — `SELF_ANCHOR_RE` reads an anchor by the checker's rule (the `@hash` look-ahead, `\"` inside the quotes); the heading path is taken only when its first part is a heading; `moved` and `kept` are built from every non-blank line; the reviewer's case, with a ` / ` added so the one-line-key branch is pinned too, red at 577f1671 and green after; the real-tree dry run prints no *could not place* entry; Executed: the real-tree dry run at the target prints two *could not place* entries, both false; the proposed case is red at the target and green on the fix |
| 🟡 2 | The release checklist says the checker reports the same totals before and after the split; it reports 1736 then 1932 ok | `docs/release-checklist.md:152` | **fixed** `20059cce` | fixed at 20059cce — the release checklist, the evidence ledger policy and the two skills say a row's status does not change and the `ok` count may rise because a pair is counted once per file; the checklist's comparison is 0 drifted, 0 broken and the count of distinct (status, coordinate) pairs; `check_text` untouched; Executed on a copy of the tree; `check_text` de-duplicates per file. Same claim at `docs/the-evidence-ledger.md:44`, `skills/evidence-check/SKILL.md:306`, `skills/implement/SKILL.md:267` |
| 🟡 3 | `fold_ledger.py`'s docstring says where a row sits changes nothing a check measures | `.github/scripts/fold_ledger.py:18` | **fixed** `63fbfa52` | fixed at 63fbfa52 — `fold_ledger.py`'s docstring says the same; The same measurement as finding 2, one depth down |
| 🟡 4 | The policy document says `correction-check` reads the shared file and the fragments because a fragment becomes part of the shared file | `docs/the-evidence-ledger.md:108` | **fixed** `20059cce` | fixed at 20059cce — `docs/the-evidence-ledger.md` names the release files `correction-check` reads and the reason that holds; Read against `correction_check.py#ledger_listing`, which lists `seal/releases` too |
| 🟡 5 | Three code comments and one workflow comment still name `seal/ledger.md` as the default or the fold's target | `skills/evidence-check/scripts/evidence_check.py:4` | **fixed** `20059cce` | fixed at 20059cce — the four comments naming the old default or fold target, `.github/workflows/hygiene.yml`'s included; the step names unchanged; Read; also `evidence_check.py:2139`, `correction_check.py:232`, `.github/workflows/hygiene.yml:122` |
| ⬜ 6 | `overview.md` says the real tree has no unplaceable anchor; it has two | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md:47` | answered | corrected at 898c3bad — `overview.md` is this work item's record; Paperwork correction; executed dry run at the target |
| ⬜ 7 | The changelog fragment says where a row sits changes nothing a check reports | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/changelog.md:8` | answered | corrected at 898c3bad — the changelog fragment's wording, which ships into `CHANGELOG.md`; Paperwork correction; gathered into `CHANGELOG.md` at the release, so the fix is worth making |
| ⬜ 8 | A past incident narrated in the present tense names the shared file as where the fold copies | `docs/review-chain-spec.md:1423` | **fixed** `20059cce` | fixed at 20059cce — `docs/review-chain-spec.md`'s past incident in the past tense; Read |
| ⬜ 9 | The split prints the first occurrence's line for every identical rewrite in one file | `.github/scripts/fold_ledger.py:574` | **fixed** `63fbfa52` | fixed at 63fbfa52 — each identical rewrite prints its own line; a case pins it; Read; the real tree has one such row |
| ⬜ 10 | The failure direction, prompt budget and platform answers are recorded for phase 3's arm only | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/phases/phase-2.md` | answered | corrected at 898c3bad — the failure direction, prompt budget and platform answers for phases 1 and 2 in their phase records; Read; PR #558's body carries none of the three |
| 🟢 | Every row of the real ledger lands in exactly one file, a second split refuses, and no row changes status | `.github/scripts/fold_ledger.py#split` | confirmed | Executed on a copy at `577f1671`: 1006 pipe lines before and after, same multiset once the two rewrites are undone; exit 1 `nothing to split`; 0 drifted, 0 broken after |
| 🟢 | S18's unchanged units are unchanged and the changed ones are the four `overview.md` names | `.github/scripts/fold_ledger.py` | confirmed | Executed: AST comparison against `9f5902e5` |

## Paste-ready fixes

```python
# An anchor whose path is exactly `seal/ledger.md`, with a quoted locator and
# the `@hash` every coordinate carries (`evidence_check.py#ANCHOR_RE`). The
# look-behind keeps `x/seal/ledger.md` — some other file — out; the
# look-ahead keeps a backticked mention with no hash out, and makes the
# locator backtrack over an escaped `\"` rather than stop at its backslash.
SELF_ANCHOR_RE = re.compile(
    r'(?<![A-Za-z0-9_.@/-])seal/ledger\.md#"((?:[^"\n]|\\")+)"'
    r'(?=(?:>"(?:[^"\n]|\\")+")?@[0-9a-f]{6,12})'
)
```
```python
        body = match.group(1).replace('\\"', '"').replace("\\|", "|")
        # The checker's rule (`evidence_check.py#resolve_unit`): a heading
        # path when the first part is a heading, one whole line otherwise.
        parts = [p for p in body.split(HEADING_SEP) if p.strip()]
        if parts and HEADING_RE.match(parts[0].strip()):
            first = " ".join(parts[0].split())
        else:
            first = " ".join(body.split())
        version = moved.get(first)
```
```python
        for line in body:
            key = " ".join(line.split())
            if key:
                moved[key] = None if key in moved else version
    moved = {k: v for k, v in moved.items() if v is not None}
    rest = [line for n, line in enumerate(lines) if n not in inside]
    kept = {" ".join(line.split()) for line in rest if line.strip()}
```
```python
def test_the_split_names_only_the_anchors_it_cannot_place(split_tree):
    """#547, round 1's 🟡 1. The split reads an anchor the way the checker
    does: a quoted locator whose first part is a heading is a heading path,
    anything else is one whole line, and only a coordinate with a hash is an
    anchor. So a line the standing area keeps is left and not named, a
    backticked mention with no hash is prose, and a line inside a moved
    section follows it to the release file."""
    path = split_tree / "seal" / "ledger.md"
    text = path.read_text(encoding="utf-8").replace(
        "### 1700000002-beta\n\n", "### 1700000002-beta\n\nA sentence beta wrote.\n\n"
    )
    kept = ledger_hash(text, "> The gathered ledger.")
    line = ledger_hash(text, "A sentence beta wrote.")
    rows = (
        f'| a header line | `seal/ledger.md#"> The gathered ledger."@{kept}` '
        "| read | 2026-09-01 | |\n"
        f'| a moved line | `seal/ledger.md#"A sentence beta wrote."@{line}` '
        '| read | 2026-09-01 | the shape `seal/ledger.md#"<heading>"` |\n'
    )
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + rows + text[at:], encoding="utf-8")
    before_line, before_rc = check(split_tree)
    assert before_rc == 0 and "0 broken" in before_line, before_line
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "could not place" not in r.stdout, r.stdout
    shared = ledger(split_tree)
    assert f'`seal/ledger.md#"> The gathered ledger."@{kept}`' in shared, shared
    assert f'`seal/releases/0.2.0.md#"A sentence beta wrote."@{line}`' in shared, shared
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 broken" in after_line, after_line
```
```markdown
green, `evidence_check.py --strict .` reports no drifted and no broken row
before and after the split — the `ok` total rises, because the checker
counts a `(coordinate, hash)` pair once per file and the split puts pairs two
releases shared into two files — and `correction-check` over the next
release's merges stays
```
```markdown
`seal/ledger.md`, the `seal/releases/*.md` glob and the `seal/ledger/*.md`
glob alike, and a row is a content anchor, so the release that folds a
fragment into its release file changes no row's status. The `ok` total
counts a `(coordinate, hash)` pair once per file, so a move can change it.
```
```markdown
sits, so the fold changes no row's status.
```
```markdown
content anchor, so the move changes no row's status, and the
```
```python
marker, `### <id>` heading and rows. Every reader of the ledger reads the
three addresses alike (`evidence_check.py#default_patterns`), so where a row
sits changes no row's status — the `ok` total counts a pair once per file,
so a move can change the count; the shared file stops growing, and a
re-stamp's diff lands in the file of the release the row belongs to. The
```
```markdown
It reads the shared file, every release file and every fragment, because a
fragment becomes part of a release file at the release and a check that
skipped fragments would go blind exactly while the rows are being written.
```
```python
Scans the evidence ledger (default: seal/ledger.md, seal/ledger/*.md,
seal/releases/*.md, and the pre-0.10 docs/**/_evidence.md) for coordinates
of the form
```
```python
    own ledger file. The fold moves the fragment into its release's file,
    `seal/releases/<X.Y.Z>.md`, at the release, which is the same moment the
    work item stops being live, so nothing changes hands at the boundary.
```
```python
#   corpus       `seal/ledger.md` alone. Not because a branch cannot move it
#                -- a branch CAN, and the one that wrote this comment moved it
#                twice, correcting rows C1 and C2 -- but because it was, on
#                the day below, the file a release folded the fragments INTO,
#                so it was the part of the corpus that survives a release. A
#                release now folds into `seal/releases/<X.Y.Z>.md` (#547), so
#                a figure taken today spans those files too.
```
```yaml
      # its evidence rows. The release folds those into that release's own
      # file, `seal/releases/<X.Y.Z>.md`,
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the fold, hygiene, narrowed-ledger, printed-name, settle, local-mode, ledger-migrates and correction modules, in the clone at `577f1671` | `332 passed`, exit 0 |
| `evidence_check.py .` on a scratch copy of the clone, before `--split` | `1736 ok · 0 drifted · 0 broken`, exit 0 |
| `fold_ledger.py --split --dry-run` on that copy | exit 0; 29 sections, lines 105–2696; 2 anchors rewritten; 2 *could not place* entries, both in this work item's fragment; `seal/ledger.md` byte-identical and no `seal/releases/` |
| `fold_ledger.py --split` on that copy | exit 0; output equal to the dry run apart from the verbs; 29 files; `seal/ledger.md` 103 lines |
| `evidence_check.py .` on that copy after the split | `1932 ok · 0 drifted · 0 broken`, exit 0 |
| In-process accounting (a `test_tmp_` script, deleted): pipe lines, and `check_ledger` over the copy before and every file after | 1006 pipe lines both times, multiset equal after undoing the two rewrites; 1662 distinct `(status, coordinate)` both times; 1662 entries before and 1858 after, the 198 added all pairs standing in more than one file except the two self-anchors, whose old coordinates are the 2 gone |
| A second `fold_ledger.py --split` on the split copy | exit 1, `nothing to split: seal/ledger.md heads no release` |
| `fold_ledger.py --check` on the split copy | exit 1, on the two unfolded fragments only; no release-heading arm |
| `SELF_ANCHOR_RE` against `ANCHOR_RE` on an anchor holding `\"` (a `test_tmp_` script, deleted) | the fold's pattern stops at the backslash; the checker's reads the whole locator |
| Finding 1's fix applied on a scratch copy: the real-tree dry run, the fold module, and the proposed case at the target and on the fix | dry run: the same 2 rewrites and no *could not place*; fold module `60 passed`; the case exit 1 at the target on the *could not place* assertion, exit 0 on the fix |
| AST comparison of `fold_ledger.py` units, `9f5902e5` against `577f1671` | eight unchanged as S18 lists; `section`, `doubled_versions`, `folded`, `main` changed |
| The broad gate — full suite, repository-wide lint and typecheck | not yet — the sealer's, after the rounds settle; never taken in this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `CLAUDE.md:134` and `:177` still name `seal/ledger.md` as the fold's target | put to the owner by the orchestrator; paste-ready text in `phases/phase-5.md` | the repository owner |
| `seal/README.md:79-83`, pinned verbatim to `templates/seal-README.md`, says fragments fold into `ledger.md` | put to the owner by the orchestrator | the repository owner |
