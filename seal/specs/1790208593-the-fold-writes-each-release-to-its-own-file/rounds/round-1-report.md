# Review round 1 — `fix/547-the-fold-writes-each-release-to-its-own-file`

Target SHA `577f1671`, base `9f5902e5` (the built tip of step C's branch,
PR #552). Whole-branch review of `9f5902e5..577f1671`, first round, no
earlier `round-N.md`. Reviewed in a `git clone --no-local` of the worktree at
the target; every probe ran in scratch copies of that clone, never in the
worktree.

The branch does what the ticket and the spec ask of the fold and the readers,
and the split does what the prompt asked me to prove: every row lands in
exactly one file, a second split refuses, and nothing breaks. Two things did
not hold when I measured them.

- **The checker's totals are not the same across the split** (findings 2, 3
  and 7). They rise from `1736 ok` to `1932 ok`, because the checker
  de-duplicates a `(coordinate, hash)` pair within one file and the split puts
  pairs two releases shared into two files. No row changes status. The
  handoff and the PR body say *checker totals identical*, and the release
  checklist tells the release session to expect the same totals, so that
  session will measure a difference the documents call a finding.
- **The split's dry run tells a person to fix two anchors that need nothing**
  (findings 1 and 6). At the target it prints *could not place — open them by
  hand* for two strings in this work item's own fragment: an anchor to a
  header line that the split keeps, and a prose mention with no hash. The
  split reads anchors by a looser rule than the checker does.

Findings 4 and 5 answer the prompt's question about other documents: yes,
four shipped or loaded places outside `CLAUDE.md` and `seal/README.md` still
say the fold writes into `seal/ledger.md`.

## Spec compliance

Read against `spec.md` S1–S21, `plan.md`, and `CONTRIBUTING.md` §*What a
change to a gate must carry*.

| Scenario | What I found | How |
|---|---|---|
| S1–S4, the readers | `default_patterns`, `failing_rows`, `HOME_GLOBS`, `ledger_listing` and `coordinates` each gain the release glob; `anchored_rows` follows `default_patterns` | read; the eight modules executed green |
| S5–S10, the fold and `--check` | The fold writes `seal/releases/<X.Y.Z>.md` and never `seal/ledger.md`; a join goes through C's `insert`; the four `--check` arms are there | read; fold module green |
| S11–S13, `--split` | Holds on the real ledger (probe below), except the unplaceable-anchor report (finding 1) | executed |
| S14, the rehearsal | It compares a SET of `(status, coordinate)`, which is honest in its docstring, and so cannot see the total rising | read and executed |
| S15, S17 | Both hold | read |
| S16, documents | Mostly holds; finding 4 names the places it missed | read, `grep` |
| S18, units unchanged | Holds as `overview.md` says. By AST comparison against `9f5902e5`, `demote`, `insert`, `section_heading`, `fragments`, `marker`, `is_marked`, `open_rows` and `append` are identical, and `section`, `doubled_versions`, `folded` and `main` changed. `hooks/root-migrate.py`, `templates/`, `.github/workflows/` and `gather_changelog.py` show no diff | executed |
| S21, #553 | `own_marker_dropped` drops the fragment's first marker line and the blank lines under it; the doubled-marker arm reads the whole corpus | read; fold and hygiene modules green |
| Gate table | Phase 3 records the four answers for #553's arm. Phases 1 and 2 record only *seen red*: the failure direction, prompt budget and platform answers for the widened readers (two of them under `hooks/`) and for the three phase-2 `--check` arms are in no record and not in the PR body (finding 10) | read |

### The implementer's account, checked

| The account said | What I found |
|---|---|
| *every row in exactly one file* | True. 1006 pipe lines before and after, the same multiset once the two rewritten anchors are undone |
| *checker totals identical* (handoff, PR body phase 4) | False. `1736 ok · 0 drifted · 0 broken` before, `1932 ok · 0 drifted · 0 broken` after. The set of distinct `(status, coordinate)` is 1662 both times. Findings 2, 3 and 7 |
| *a second `--split` refuses* | True, exit 1, `nothing to split: seal/ledger.md heads no release` |
| *29 releases, not 37* | True, 29 files |
| *could not place … The real tree has none* (`overview.md`, `phases/phase-4.md`) | False at the target. Two entries, both in this work item's own fragment, both added after phase 4 measured. Findings 1 and 6 |
| S18's changed and unchanged units | True, by AST comparison |

The two edits the smith left to the owner (`CLAUDE.md`'s two paragraphs, and
`seal/README.md` pinned to its template) are not asked for here, as the prompt
says. I confirmed both still say the fold writes into `ledger.md`
(`CLAUDE.md:134`, `CLAUDE.md:177`, `seal/README.md:79-83`).

## Quality

### 1. 🟡 The split names an anchor it keeps as one it cannot place

`.github/scripts/fold_ledger.py:460` and `:500-510`, and the `moved`/`kept`
sets built at `:554-560`.

**What is wrong.** `SELF_ANCHOR_RE` matches `seal/ledger.md#"<text>"` with no
`@hash` after it. `rewrite_self_anchors` then takes the part before the first
` / ` as a heading, and knows only heading lines, in `moved` and in `kept`.
The checker reads the same text three ways differently.

- An anchor is a coordinate only with an `@hash` (`evidence_check.py#ANCHOR_RE`).
- A quoted locator is a heading path only when its first part is a heading.
  Anything else is ONE whole line, matched by `text_regions`
  (`evidence_check.py#resolve_unit`).
- An escaped `\"` inside the locator is part of it. The fold's pattern has no
  `@` after the closing quote to force backtracking, so it stops at the
  backslash. Executed: `### a \"q\" b` comes back as `### a \`.

**Why it matters.** At the target, `--split --dry-run` over the real tree ends
with this section:

```
anchors into seal/ledger.md the split could not place — open them by hand:
  seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md  seal/ledger.md#"<heading>"
  seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md  seal/ledger.md#"> rows from before the fragments existed. **A work item writes"
```

The first is prose in P1's Notes cell. The checker never read it as an
anchor. The second is D1's anchor to line 10 of `seal/ledger.md`'s header,
which the split keeps, and the checker reports it OK before and after. The
spec's case for running the split at the release is *one `--dry-run` a person
already reads* (`spec.md` §Grounding, the unattended-verification row). That
dry run now tells the person to hand-edit two anchors that need nothing. The
likely hand edit is re-pointing D1's anchor at a release file, which would
turn it BROKEN. The same rule also leaves a line anchor INTO a moved section
without rewriting it. That anchor goes BROKEN after the split, even though its
line moved byte for byte just as a heading does.

**Fix.** Read an anchor the way the checker does: require the `@hash`, take a
heading path only when the first part is a heading, and otherwise key on the
whole line. Then build `moved` and `kept` from every non-blank line and not
from headings only. Executed on a scratch copy with the fix applied: the
real-tree dry run prints the same two rewrites and no *could not place*
section, and the fold module is green. The case below was red at the target,
on the *could not place* assertion, and green on the fix.

### 2. 🟡 The release checklist tells the release session to expect the same totals

`docs/release-checklist.md:152-153`, and the same claim at
`docs/the-evidence-ledger.md:42-44`.

**What is wrong.** §3 says that at the release that runs `--split`,
*`evidence_check.py --strict .` reports the same totals before and after the
split*. Executed on a copy of the tree at `577f1671`: `1736 ok` before,
`1932 ok` after, 0 drifted and 0 broken both times. `check_text`
de-duplicates `(coordinate, hash)` through a `seen` set that is local to one
`check_ledger` call, so it de-duplicates per file. Rows that two releases cited
identically were counted once inside `seal/ledger.md` and are counted once
per release file after the split. The in-process accounting agrees: 1662
distinct `(status, coordinate)` pairs both times, and 196 more entries after.
Every added entry is a pair that stands in more than one file, apart from the
two self-anchors, which appear under their new path and are gone from their
old one.

`docs/the-evidence-ledger.md:44` states the same thing about the fold in
general: *changes nothing any of them measures*. This branch's own
`Corrected 2026-09-24` note on the de-duplication row in `seal/ledger.md` says
a fold moves the total.

**Why it matters.** `questions.md` Q6 reads *the same set*, which is true.
The checklist reads *the same totals*, which is false, and Q6's own row says
*a difference is a finding at the release pull request*. The session running
the release tail will take that reading, find 196 more, and either spend the
tail on it or report a defect that is not one. The same one-word overstatement
stands at `skills/evidence-check/SKILL.md:306` (*changes nothing this check
reports*) and `skills/implement/SKILL.md:267` (*changes nothing the checker
measures*), both inside hunks this branch rewrote. What a move cannot change
is a row's status. It can change the count.

### 3. 🟡 `fold_ledger.py`'s docstring says where a row sits changes nothing a check measures

`.github/scripts/fold_ledger.py:18-19`.

The same fact as finding 2, one depth down: *so where a row sits changes
nothing a check measures*. The count measured changes. The code next to this
sentence is correct; the sentence is not.

### 4. 🟡 Two shipped documents still say the fold writes into the shared file

`docs/the-evidence-ledger.md:108-110`, and `docs/review-chain-spec.md:1423`
as a lesser case (finding 8).

`docs/the-evidence-ledger.md:108-110` explains why `correction-check` reads
what it reads: *It reads the shared file and every fragment, because a
fragment becomes part of the shared file at the release*. After this branch,
`correction-check` reads the release files too
(`correction_check.py#ledger_listing`), and a fragment becomes a release file.
The paragraph states both a reason that is no longer true and a scope that is
now incomplete. It is the policy document S16 names, and this branch edited
two other paragraphs of it. A reader who opens it to learn what the check
watches is told two addresses where there are three.

This answers the prompt's question about other documents. Outside `CLAUDE.md`
and `seal/README.md`, the places in shipped or loaded documents that still say
the fold writes into `seal/ledger.md` are this paragraph, the aside at
`docs/review-chain-spec.md:1423`, and `docs/one-root-by-lifetime.md:99` and
`:150`. The last two are a dated record, which `spec.md` §Out leaves to
`settle` on purpose, so they are grounds and not a finding. The code-comment
places are finding 5.

### 5. 🟡 Three shipped code comments still name `seal/ledger.md` as the fold's target or the default

`skills/evidence-check/scripts/evidence_check.py:4-5` and `:2139-2140`,
`skills/evidence-check/scripts/correction_check.py:232-238`, and
`.github/workflows/hygiene.yml:122`.

- `evidence_check.py:4-5`, the module docstring: *default: seal/ledger.md,
  seal/ledger/*.md, and the pre-0.10 docs/**/_evidence.md*. It lacks the
  release glob. `default_patterns`'s own docstring was updated; this one was
  not. S18 allowed `default_patterns` *and its docstring*, which reads as the
  function's, so the frame left this one out.
- `evidence_check.py:2139-2140`, `tree_names`: *The fold moves the fragment
  into `seal/ledger.md` at the release*. That is the argument for why excluding
  `<home>/ledger/` loses nothing. It still holds with release files, because
  they are in the corpus, but it names the wrong file.
- `correction_check.py:232-238`: the census corpus is *`seal/ledger.md` alone
  … because it is the file a release folds the fragments INTO*. After the
  split that reason is false, and the file holding the corpus's markers is 29
  files. The figure beside it is dated and says it goes stale. The reason is
  not dated.
- `hygiene.yml:122`: *The release folds those into `seal/ledger.md`*. S18
  kept `.github/workflows/` untouched, and the step name is pinned by
  `test_the_ledger_fragments_fold_at_release.py:1168`. So this is the one
  place where the fix is a comment edit the frame did not plan for. Whether to
  make it is the orchestrator's call.

These are the §12 class the spec enumerated by grep for readers. It did not
enumerate prose that names the target.

### 6. ⬜ correction — `overview.md` says the real tree has no unplaceable anchor

`seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md:47`.

*The real tree has none.* At `577f1671` it has two (finding 1). Phase 4's
record says the same and was true when phase 4 ran; D1's anchor arrived in
`d767fa4a`. The live `overview.md` is the one to correct, in whichever form
finding 1 is answered.

### 7. ⬜ correction — the changelog fragment promises nothing a check reports changes

`seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/changelog.md:8`.

*so where it sits changes nothing a check reports*, the claim from finding 2.
This fragment is gathered into `CHANGELOG.md` at the release, so the wording
ships. It is paperwork by location, and I have not counted it toward `Needs a
fix`. The fix is the finding 2 wording.

### 8. ⬜ `review-chain-spec.md` narrates a past incident in the present tense

`docs/review-chain-spec.md:1423`.

*a false count in a ledger fragment that `fold_ledger.py` copies into the
shared file*. This was true when it happened. Read as present tense, it now
names the wrong file. *copied into the shared ledger at the release* keeps
the incident's tense.

### 9. ⬜ The split's printed line number is the first occurrence of the rewritten text

`.github/scripts/fold_ledger.py:574`.

`number = new[: new.index(fresh)].count("\n") + 1` finds the first
occurrence of the rewritten anchor. Two rows in one file that cite the same
moved heading are both reported at the first row's line. The rewrite itself
is correct; only the printed coordinate is. The real tree has one such row,
so the output is right today.

### 10. ⬜ The gate table's three other answers are recorded for phase 3 only

`phases/phase-1.md`, `phases/phase-2.md`, PR #558's body.

`CONTRIBUTING.md` §*What a change to a gate must carry* asks for four answers
on any change under `hooks/` and any gate. Phase 3 gives all four for #553's
arm. Phases 1 and 2 give *seen red* only. The failure direction is *blocks
more* for every reader that now reads one more glob, and for the three
phase-2 `--check` arms. The prompt budget is zero. Platform honesty is `/`
joined through `under()` and no glob order relied on, which I read to be true
in `release_files`, `split` and `coordinates`. None of that is written
anywhere a reader of the pull request would find it. Stating it in the PR
body is the smallest place.

## Regression tests to plant

- `tests/test_the_ledger_fragments_fold_at_release.py`: the case under
  finding 1's fix, beside `test_the_split_rewrites_an_anchor_into_a_moved_section`.
  Seen red at `577f1671` and green on the fix, executed.

## Facts for the evidence ledger

- The checker's `ok` total is per-file de-duplicated. On this tree at
  `577f1671` the split raises it from 1736 to 1932 with the distinct
  `(status, coordinate)` set unchanged at 1662. This belongs in the P2 row's
  Notes, or in a note on the de-duplication row that this branch already
  corrected, so the release session reads the rise as expected.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `--split` reads an anchor by a looser rule than the checker, so its dry run names a kept header-line anchor and a hashless prose mention as unplaceable, truncates an escaped quote, and leaves a line anchor into a moved section unrewritten | `.github/scripts/fold_ledger.py:460` | open | Executed: the real-tree dry run at the target prints two *could not place* entries, both false; the proposed case is red at the target and green on the fix |
| 🟡 2 | The release checklist says the checker reports the same totals before and after the split; it reports 1736 then 1932 ok | `docs/release-checklist.md:152` | open | Executed on a copy of the tree; `check_text` de-duplicates per file. Same claim at `docs/the-evidence-ledger.md:44`, `skills/evidence-check/SKILL.md:306`, `skills/implement/SKILL.md:267` |
| 🟡 3 | `fold_ledger.py`'s docstring says where a row sits changes nothing a check measures | `.github/scripts/fold_ledger.py:18` | open | The same measurement as finding 2, one depth down |
| 🟡 4 | The policy document says `correction-check` reads the shared file and the fragments because a fragment becomes part of the shared file | `docs/the-evidence-ledger.md:108` | open | Read against `correction_check.py#ledger_listing`, which lists `seal/releases` too |
| 🟡 5 | Three code comments and one workflow comment still name `seal/ledger.md` as the default or the fold's target | `skills/evidence-check/scripts/evidence_check.py:4` | open | Read; also `evidence_check.py:2139`, `correction_check.py:232`, `.github/workflows/hygiene.yml:122` |
| ⬜ 6 | `overview.md` says the real tree has no unplaceable anchor; it has two | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md:47` | open | Paperwork correction; executed dry run at the target |
| ⬜ 7 | The changelog fragment says where a row sits changes nothing a check reports | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/changelog.md:8` | open | Paperwork correction; gathered into `CHANGELOG.md` at the release, so the fix is worth making |
| ⬜ 8 | A past incident narrated in the present tense names the shared file as where the fold copies | `docs/review-chain-spec.md:1423` | open | Read |
| ⬜ 9 | The split prints the first occurrence's line for every identical rewrite in one file | `.github/scripts/fold_ledger.py:574` | open | Read; the real tree has one such row |
| ⬜ 10 | The failure direction, prompt budget and platform answers are recorded for phase 3's arm only | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/phases/phase-2.md` | open | Read; PR #558's body carries none of the three |
| 🟢 | Every row of the real ledger lands in exactly one file, a second split refuses, and no row changes status | `.github/scripts/fold_ledger.py#split` | confirmed | Executed on a copy at `577f1671`: 1006 pipe lines before and after, same multiset once the two rewrites are undone; exit 1 `nothing to split`; 0 drifted, 0 broken after |
| 🟢 | S18's unchanged units are unchanged and the changed ones are the four `overview.md` names | `.github/scripts/fold_ledger.py` | confirmed | Executed: AST comparison against `9f5902e5` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `CLAUDE.md:134` and `:177` still name `seal/ledger.md` as the fold's target | put to the owner by the orchestrator; paste-ready text in `phases/phase-5.md` | the repository owner |
| `seal/README.md:79-83`, pinned verbatim to `templates/seal-README.md`, says fragments fold into `ledger.md` | put to the owner by the orchestrator | the repository owner |

## Paste-ready fixes

### Finding 1 — read an anchor the way the checker does

`.github/scripts/fold_ledger.py`, the pattern at line 460:

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

`rewrite_self_anchors`, the key inside `one()`:

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

`split`, the two sets, so a line anchor is placed like a heading:

```python
        for line in body:
            key = " ".join(line.split())
            if key:
                moved[key] = None if key in moved else version
    moved = {k: v for k, v in moved.items() if v is not None}
    rest = [line for n, line in enumerate(lines) if n not in inside]
    kept = {" ".join(line.split()) for line in rest if line.strip()}
```

The docstring of `rewrite_self_anchors` and the module docstring's *an
anchor into a moved section that is not a heading path is named and left*
then read: *an anchor whose line or heading is in no section the split
moved or kept is named and left*.

The case, in `tests/test_the_ledger_fragments_fold_at_release.py`, beside
`test_the_split_rewrites_an_anchor_into_a_moved_section`:

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

### Finding 2 — the totals are the set, and the count moves

`docs/release-checklist.md` §3, the sentence at lines 152-153:

```markdown
green, `evidence_check.py --strict .` reports no drifted and no broken row
before and after the split — the `ok` total rises, because the checker
counts a `(coordinate, hash)` pair once per file and the split puts pairs two
releases shared into two files — and `correction-check` over the next
release's merges stays
```

`docs/the-evidence-ledger.md:42-44`:

```markdown
`seal/ledger.md`, the `seal/releases/*.md` glob and the `seal/ledger/*.md`
glob alike, and a row is a content anchor, so the release that folds a
fragment into its release file changes no row's status. The `ok` total
counts a `(coordinate, hash)` pair once per file, so a move can change it.
```

`skills/evidence-check/SKILL.md:306` and `skills/implement/SKILL.md:267`,
the same word:

```markdown
sits, so the fold changes no row's status.
```

```markdown
content anchor, so the move changes no row's status, and the
```

### Finding 3 — the module docstring

`.github/scripts/fold_ledger.py:17-20`:

```python
marker, `### <id>` heading and rows. Every reader of the ledger reads the
three addresses alike (`evidence_check.py#default_patterns`), so where a row
sits changes no row's status — the `ok` total counts a pair once per file,
so a move can change the count; the shared file stops growing, and a
re-stamp's diff lands in the file of the release the row belongs to. The
```

### Finding 4 — what `correction-check` reads, and why

`docs/the-evidence-ledger.md:108-110`:

```markdown
It reads the shared file, every release file and every fragment, because a
fragment becomes part of a release file at the release and a check that
skipped fragments would go blind exactly while the rows are being written.
```

### Finding 5 — the comments

`skills/evidence-check/scripts/evidence_check.py:4-5`:

```python
Scans the evidence ledger (default: seal/ledger.md, seal/ledger/*.md,
seal/releases/*.md, and the pre-0.10 docs/**/_evidence.md) for coordinates
of the form
```

`skills/evidence-check/scripts/evidence_check.py:2139-2141`:

```python
    own ledger file. The fold moves the fragment into its release's file,
    `seal/releases/<X.Y.Z>.md`, at the release, which is the same moment the
    work item stops being live, so nothing changes hands at the boundary.
```

`skills/evidence-check/scripts/correction_check.py:232-238`:

```python
#   corpus       `seal/ledger.md` alone. Not because a branch cannot move it
#                -- a branch CAN, and the one that wrote this comment moved it
#                twice, correcting rows C1 and C2 -- but because it was, on
#                the day below, the file a release folded the fragments INTO,
#                so it was the part of the corpus that survives a release. A
#                release now folds into `seal/releases/<X.Y.Z>.md` (#547), so
#                a figure taken today spans those files too.
```

`.github/workflows/hygiene.yml:122`:

```yaml
      # its evidence rows. The release folds those into that release's own
      # file, `seal/releases/<X.Y.Z>.md`,
```

Needs a fix: yes — 🟡 1 (the split's anchor reading), 🟡 2 and 🟡 3 (the
totals claim in the checklist, the policy document and the docstring), 🟡 4
and 🟡 5 (documents and comments naming the old fold target)
Loses a record or crashes: no

The broad gate has not come due: this report leaves five findings open, so
what comes next is the fix pass and a verifying round, not the sealer's spawn.

## Proof block

Opened in the clone at `577f1671`, all read in full or at the lines cited:
`.github/scripts/fold_ledger.py` (whole),
`skills/evidence-check/scripts/evidence_check.py` (lines 1-12, 60-92,
225-420, 940-975, 2120-2175, 2380-2395), `skills/evidence-check/scripts/correction_check.py`
(the diff; lines 222-275), `skills/settle/scripts/settle.py` (the diff),
`hooks/evidence-advisor.py` (lines 105-140), `hooks/ledger-migrate.py` (the
diff), `skills/code-review/scripts/survivor_check.py` (lines 110-175),
`skills/implement/scripts/seal.py` (lines 60-125),
`skills/verify/scripts/broad_gate.py` (lines 175-200),
`.github/workflows/hygiene.yml` (lines 119-137),
`seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/`
`spec.md`, `overview.md`, `changelog.md` (lines 1-12), `questions.md`
(Q6), `phases/phase-2.md` (lines 55-103), `phases/phase-3.md` (lines 60-80),
`phases/phase-4.md` (whole),
`seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md`
(whole), the diffs of `CONTRIBUTING.md`, `docs/branch-and-release.md`,
`docs/release-checklist.md`, `docs/the-evidence-ledger.md`, `seal/ledger.md`,
`skills/evidence-check/SKILL.md`, `skills/settle/SKILL.md`,
`skills/implement/SKILL.md`, `README.md`, `agents/framer.md`,
`skills/verify/SKILL.md`, `tests/test_release_hygiene.py`,
`tests/test_a_row_points_by_content.py`, `tests/test_unverified_rows_close.py`,
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, and in
`tests/test_the_ledger_fragments_fold_at_release.py` the helpers and the
split cases (lines 64-72, 666-830, 866-953);
`tests/test_a_merge_cannot_silently_drop_a_correction.py` (the census case
and `ledger_corpus`); `docs/review-chain-spec.md` (lines 1418-1426);
`CONTRIBUTING.md` (lines 36-78, 161-180); `bin/test`; PR #558's body.
Not opened: `plan.md` beyond the lines a grep returned, `phases/phase-1.md`,
`phases/phase-5.md` and `phases/phase-6.md` beyond grep lines,
`survivors.md`, `routing.md`.
