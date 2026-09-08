# 1788826000-a-stamp-names-content-not-a-commit — review round 2

| Field | Value |
|---|---|
| Target SHA | 2f0dd02 |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | passed under round 3 |
| Fixes checked by | round-3 |
| Contract changes | comment_blocks → riders_in, region_lines, round-1-report.md, round-1.md, round-2-report.md, round-2.md, pytest |
| New units | test_a_markdown_heading_naming_the_marker_is_not_a_rider (depth 1); test_the_hasher_reads_a_markdown_heading_the_same_way_the_reader_does (depth 1); test_reverify_says_so_when_only_selects_no_rider (depth 1); test_only_without_a_verb_is_refused_rather_than_ignored (depth 1) |
| Needs a fix | yes — findings 10 and 11 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of `1788826000-a-stamp-names-content-not-a-commit` (ticket #239), at target `2f0dd02`, base `origin/release/v0.9.1`. The verifying round over round 1's fixes, whose substance is `eaa8030`, `bdf65df`, `923f86c` and `e1b83b8`.

Round 1's verdicts were inherited. It had confirmed the whole design by re-derivation — the self-reference fixed point, the exclusion rule swallowing only its two stated losses, the two-rider `blocks[:1]` mutation, seven mutations red, the `135` count — and then opened four things, three of them 🔴 because they were the migration's own headline claims being false: all twenty stamps reading `2026-09-08` while twelve were not read that day; the cause, an `and` in the reverify condition, so an unchanged rider was rewritten for the date alone while `--only` selected a file rather than a rider; a date-only re-stamp drifting the ledger row of a unit nobody touched; and two adjacent riders merging into one block so the second stamp was never read — a merge phase 3 had found in its own fixture and not carried to the production reader.

The named targets. The twelve restored dates, each claimed proven against the commit its previous stamp named, to be verified independently including the twelfth, with the four hand-written anchors checked for keeping `2026-09-08` on the stated ground that choosing an anchor required reading the rider. The reverify rule, in both directions, and whether `--only` selects what it says. The re-enumeration, which found the same merge in the HTML form so that two markdown files would have kept the defect just cleared from the `#` form — the class this repository has measured eight times — with the round asked to look for a third corpus or a third form. The HTML opener having been looser than its own docstring, surfaced when the file's own fixture constant became a rider. The trailing-rider shape left open, with its count verified and its disposition judged. `hooks/root-migrate.py`'s `4f78074` reported as the same shape as `881fb0f`, whose refusal message round 1 found untrue. And `seal/ledger.md`'s L5 and R8, re-stamped by `--reverify` before being read — a re-verify before a read being the thing the `Checked` column exists to prevent, so it needed justifying or opening.

The report was to be a file, finding ids bare integers, one row per finding, no real user path, `NAME NOT IN TREE` written by the reviewer on any line naming something the tree does not carry — round 1's report had needed five such marks added afterwards and blocked the broad gate until it had them — and no commit SHA in any rider stamp.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 Twelve stamps assert a 2026-09-08 reading that did not happen | `.github/scripts/rider_check.py#reverify` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | **answered** | **executed** — all twenty riders re-derived independently at `2f0dd02`. Twelve regions hash identically at the commit their pre-migration stamp named and at HEAD, and each carries that stamp's date; `4581fe1` is among them (`8e0a246a` both sides). Three moved and read 2026-09-08 correctly. A thirteenth, `templates/evidence-check.yml:5`, is provable at 2026-08-31 and is disclosed as deliberately left in `phase-4.md` — defensible: its anchor was chosen by hand that day |
| 2 | 🔴 `reverify` rewrites an unchanged stamp, and `--only` takes a file | `.github/scripts/rider_check.py:477` · message at `:368` | **answered** | **executed** — three scratch modules: `--only hooks/b.py` wrote `b.py` alone and left `a.py` byte-identical with its 2026-01-01 date under a `today` of 2026-12-31; a second unscoped run wrote `c.py` only. On the real tree the check is `20 ok`, so a full `--reverify` writes nothing. **read** — the message at `:368-375` says `--only` takes a FILE, and its case asserts both halves |
| 3 | 🟡 A date-only re-stamp drifts the ledger row of a unit nobody edited | `.github/scripts/rider_check.py#reverify` · `phases/phase-4.md` | **answered** | **executed** — `rider_check.py` exit 0 at `20 ok · 0 drifted · 0 broken` and `evidence_check.py .` exit 0 at `822 ok · 0 drifted · 0 broken`, so the two checkers agree on the tree as it stands. **read** — `phase-4.md:108-121` states the steady state conditionally and names what was false when the phase wrote it |
| 4 | 🔴 Two riders back to back merge into one block | `.github/scripts/rider_check.py:170-232` | **answered** | **executed** — seven constructions split correctly in both forms, including three riders in one HTML comment (`[(3,4),(5,6),(7,8)]`, three stamps read) and an unclosed comment followed by a later marker. No third form exists: every comment head in `READABLE` is `#` or `&lt;!--` |
| 5 | 🟡 Three hand-written anchors are quoted sentences, so a reword reports BROKEN | `agents/smith.md:60` · `skills/implement/SKILL.md:379` · `templates/evidence-check.yml:5` | **answered** | **executed** — each anchor resolves to exactly one region and each region encloses its own rider: `"## Phases"` → 27-233 holding line 60, `"### 1. Read the spec before the code"` → 243-458 holding line 379, the quoted YAML line → 1-18 holding line 5. Neither markdown file has a narrower heading available (measured), so the coarse region is forced rather than chosen, and `seal/ledger.md:989` already records that trade for the same heading |
| 6 | 🟡 The headline refusal says git cannot resolve `881fb0f` | `.github/scripts/rider_check.py:387` · `phases/phase-4.md` · ledger row S4 | **answered** | **executed** — `881fb0f` and `4f78074` both resolve, both are ancestors of HEAD, and both refuse their path with *exists on disk, but not in …*. The record now says *a stamp that was wrong when it was written* for both and names `4f78074` explicitly |
| 7 | ⬜ The disclosure says the old stamp string survives in one record; it survives in two | `questions.md:28` · `overview.md:38` | **answered** | **read** — both files say two and name `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96` |
| 8 | ⬜ Phase 3's removes table names two of the four units removed | `phases/phase-3.md` | **answered** | **read** — four rows present, the two added ones marked `NAME NOT IN TREE`, with an HTML note saying which pass added them and why |
| 9 | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck | whole tree | deferred the orchestrator | contract §2. **executed** — no `ruff` module in `.venv` and none on `PATH`, so lint has run nowhere in this work item and cannot be assumed done |
| 10 | 🟡 `--reverify --only <path>` that matches no rider prints `0 restamped · 0 refused` and exits 0 | `.github/scripts/rider_check.py:464` and `:603-610` | **fixed** `677e10f` | fixed at 677e10f — `` — an `--only` selecting no rider is refused by path and the run exits 1. `982b8d3` closes the same cause three instances further out, in `main`; **executed** — `--only hooks/wortree-guard.py` on the working tree returns exit 0 with a clean total and writes nothing. A hand-typed or absolute path selects nothing and the run reports success; exit 0 is what a script reads. Fix verified on a patched copy: the miss is refused by path and a real `--only` still writes its rider |
| 11 | 🟡 A markdown heading is read as a `#` comment head, against the function's own docstring | `.github/scripts/rider_check.py:219`, docstring at `:170-196` | **fixed** `677e10f` | fixed at 677e10f — `` — `#` opens a comment everywhere except a `.md` file, where it opens a heading, and both callers of the reader are told the path so they cannot disagree about it. The module docstring now states the asymmetry the defect broke; **executed** — `## RIDER: what one is` in a `.md` under a scanned root gives `BROKEN … no verification stamp`, exit 2, for a line nobody wrote as a rider. Same class as the HTML opener `923f86c` closed, and it invents an alarm where every stated loss of this design loses one. Fix verified on a patched copy: the corpus stays `20 ok`, the heading returns `[]` against `[(3, 3)]` unpatched, and both real rider forms are untouched |
| 12 | ⬜ The marker-line count is 33 with 13 extras, and three records say 31 with 11 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md:20` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | answered | corrected at `982b8d3` — 33 marker lines with 13 extras at `2f0dd02` and 36 with 16 at `677e10f`, in all three records, each figure naming the commit it was taken at |
| 13 | ⬜ The trailing-rider deferral names the `#` form only | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | answered | corrected at `982b8d3` — both records name both trailing forms, with the round each one was executed in |
| 14 | ⬜ Two of the five ledger rows the fix pass re-stamped carry no note of a reading | `seal/ledger.md:1203` · `seal/ledger.md:1418` | answered | corrected at `982b8d3` — `seal/ledger.md:1203` and `:1418` say who read what, on a fresh reading rather than on round 2's account of it |
| 15 | ⬜ `overview.md` lists as open a records-arm refusal that `2f0dd02` answered | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:37` | answered | corrected at `982b8d3` — the row is marked ✅ with the commit that answered it, and the ONE refusal that replaced it is a new row naming the orchestrator |

## Paste-ready fixes

```python
    checker = checker or load_checker()
    today = today or datetime.date.today().isoformat()
    written, refused = [], []
    seen = 0
    for rider in all_riders(root, roots):
        if only and rider.rel != only:
            continue
        seen += 1
```
```python
        written.append((rider.where(), digest))
    if only and not seen:
        refused.append(
            (
                only,
                "no rider in the tree has this path — `--only` selects by "
                "the path the drift message printed, so a hand-typed or "
                "absolute one selects nothing and this run did nothing",
            )
        )
    return written, refused
```
```python
def test_reverify_says_so_when_only_selects_no_rider(tmp_path):  # NAME NOT IN TREE
    """`--only` selects by exact relative path. One that matches nothing
    printed `0 restamped · 0 refused` and exited 0, so a reader answering a
    drifted rider read success for a run that wrote nothing — and exit 0 is
    what a script reads (round 2, finding 10)."""
    stamped_module(tmp_path, digest="00000000")
    written, refused = riders.reverify(
        str(tmp_path),
        only="hooks/no-such-file.py",
        roots=("hooks",),
        today="2026-12-31",
        checker=CHECKER,
    )
    assert not written and len(refused) == 1, (written, refused)
    assert "no rider in the tree has this path" in refused[0][1], refused
```
```python
def comment_blocks(lines, rel=None):
```
```python
    out = []
    i, n = 0, len(lines)
    # `#` opens a comment in Python, YAML, shell and TOML. In markdown it opens
    # a HEADING, so a heading naming the marker became a rider with no stamp --
    # BROKEN at exit 2 for a line nobody wrote as a rider. Markdown's rider form
    # is the HTML comment the branch above reads, and no `.md` file in the tree
    # uses the `#` form. Every stated loss of this design loses an alarm; this
    # was the one place it invented one (round 2, finding 11).
    hash_opens_a_comment = not (rel or "").endswith(".md")  # NAME NOT IN TREE
```
```python
        elif stripped.startswith("#") and hash_opens_a_comment:
```
```python
def riders_in(rel, text):
    return [Rider(rel, a, b, text) for a, b in comment_blocks(text.splitlines(), rel)]
```
```python
def test_a_markdown_heading_naming_the_marker_is_not_a_rider():  # NAME NOT IN TREE
    """`comment_blocks`'s own docstring gives the `#` form to Python, YAML and
    shell and gives markdown the HTML comment. The code asked only that the
    stripped line start with `#`, which in markdown is a heading, so a heading
    naming the marker became a rider with no stamp and the check exited 2 on
    it. The mirror of the HTML opener `923f86c` closed (round 2, finding 11)."""
    src = f"# Title\n\n## {'RIDER:'} what one is\n\nprose.\n"
    assert riders.comment_blocks(src.splitlines(), "skills/x/SKILL.md") == []
    assert riders.riders_in("skills/x/SKILL.md", src) == []
    # the two real forms are untouched
    py = f"def u():\n    {MARK} claim\n    # Verified 2026-01-01 against u@00000000\n"
    assert riders.comment_blocks(py.splitlines(), "hooks/m.py") == [(2, 3)]
    md = f'## H\n\n{HTML_MARK} claim\n     Verified 2026-01-01 against "## H"@00000000. --&gt;\n'
    assert riders.comment_blocks(md.splitlines(), "a.md") == [(3, 4)]
```
```markdown
**Executed** 2026-09-08 at `2f0dd02`: the widened scan over six roots finds exactly 20 riders; a grep of the same roots at that commit finds 33 marker lines, and all 13 extras are prose or string literals. The count names the commit it was taken at because an aggregate is not a coordinate — it read 31 at `eaa8030` and moved when `923f86c` planted the HTML opener in the case file twice, which is the correction R5 in `0.9.0` already records.
```
```markdown
| **read by nothing, and silent about it.** Not in the tree: at `2f0dd02` a grep of the six roots finds 33 marker lines against the reader's 20 riders, and all 13 extras are prose or string literals. Closing it needs a rule comparing the two corpora, which a fix pass may not add — deferred to the repository owner in `overview.md` |
```
```markdown
| a rider written as a TRAILING comment is read by nothing and says nothing about it, because a block opens only at the head of a comment line. Both forms: `value = 1  # RIDER: …` in a `#` file, and `some text &lt;!-- RIDER: … --&gt;` in a markdown one. Executed in round 2 — each gives `0 ok · 0 drifted · 0 broken` under a scanned root. Executed at `2f0dd02`: a grep of the six roots finds 33 marker lines against the reader's 20 riders, and all 13 extras are prose or string literals, so the tree does not stand in either form today. Closing it means a rule that compares the grep corpus with the reader's, which is mechanism a fix pass may not add | the repository owner. `skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it* is why it is written here rather than built |
```
```markdown
 **Re-read 2026-09-08 in work item 1788826000's round 1 fix pass**: the only edit inside `test_the_refusal_above_can_actually_fail` was its own rider's date, restored from 2026-09-08 to the 2026-09-06 `--migrate` proved. The region moved by one digit inside a comment and the claim did not move at all.
```
```markdown
 **Re-read 2026-09-08 in work item 1788826000's round 1 fix pass**: the only edit inside `unread_items` was its own rider's date, restored from 2026-09-08 to the 2026-09-07 `--migrate` proved. The region moved by one digit inside a comment and the claim did not move at all.
```
```markdown
| the records arm of `bin/evidence-check` refused eight names in `rounds/round-1.md` and `rounds/round-1-report.md` and exited 2 at `7ff1e63`. **Answered at `2f0dd02`**, which wrote `NAME NOT IN TREE` on each line — three in the record and six in the report. Executed in round 2 on the working tree: `3 work items read · 42 unread · 416 names read · 0 stamps read · 0 refused · 0 drifted · 0 external`, exit 0 | answered — the orchestrator, who owns the round records |
```

## Executed probes

| What was run | Result |
|---|---|
| Every rider at `2f0dd02` re-derived: current anchor hashed at the commit its pre-migration stamp named (from `cbdd66e`) and at HEAD | 20 riders, all `ok=True`. 12 pairs identical and each carries its pre-migration date, `4581fe1` among them at `8e0a246a`/`8e0a246a`. 3 moved and read 2026-09-08. 2 unprovable (`881fb0f`, `4f78074`). 1 had no pre-migration rider. 1 provable at 2026-08-31 and left at 2026-09-08 — `templates/evidence-check.yml:5`, `6a954d30` both sides |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` | `25 passed in 1.27s` |
| `rider_check.py` on the working tree, exit read without a pipe | `20 ok · 0 drifted · 0 broken`, exit 0 |
| `evidence_check.py .` on the working tree, exit read without a pipe | `822 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `3 work items read · 42 unread · 416 names read · 0 refused · 0 drifted`, exit 0 |
| `reverify` on three scratch modules — one true hash, two stale — with `--only hooks/b.py` then unscoped, `today=2026-12-31` | scoped wrote `b.py` alone (`a.py`, `c.py` byte-identical); unscoped wrote `c.py` alone; `a.py` still reads `Verified 2026-01-01 against unit@ea8b798d` |
| `rider_check.py --reverify --only hooks/wortree-guard.py` (a mistyped path) on the working tree | `0 restamped · 0 refused`, exit 0, tree unchanged — finding 10 |
| Seven back-to-back constructions through `comment_blocks` | two `#` `.py` `[(2,3),(4,5)]` · two `#` `.yml` `[(1,2),(3,4)]` · two in one HTML comment `[(3,4),(5,6)]` · three in one HTML comment `[(3,4),(5,6),(7,8)]` · two HTML comments `[(3,4),(5,6)]` · HTML then `#` in one `.md` `[(3,4),(5,6)]` · unclosed HTML then a later marker `[(3,7),(8,9)]`. Every stamp read in every case |
| Seven opener constructions through `comment_blocks` | `#` at head `[(2,3)]` · `#` trailing on a code line `[]` · `&lt;!--` at head `[(3,4)]` · `&lt;!--` after text `[]` · `&lt;!--` inside a string literal `[]` · **markdown `##` heading `[(3,3)]`** · list item naming the marker `[]` |
| A markdown heading holding the marker, through `check()` | `0 ok · 0 drifted · 1 broken` — `BROKEN templates/doc.md:3: no verification stamp…` — finding 11 |
| A trailing rider in each form, through `check()` | `0 ok · 0 drifted · 0 broken`, no problems — both silent, finding 13 |
| Both round-2 fixes applied to a copy of `rider_check.py`, six substitutions each asserted to match exactly once | corpus unchanged at `20 ok · 0 drifted · 0 broken`; heading `[]` against `[(3,3)]` unpatched; `.py` `#` and `.md` HTML forms unchanged; `--only hooks/no-such-file.py` refuses by name, `--only hooks/m.py` still writes |
| `git cat-file -t`, `merge-base --is-ancestor` and `git show <sha>:./<path>` for `881fb0f` and `4f78074` | both commits, both ancestors (exit 0), both *exists on disk, but not in …* |
| Marker-line count over the six roots, per commit | `404dd4d` 31 · `eaa8030` 31 · `923f86c` 33 · `e1b83b8` 33 · `bddfa94` 33 · `2f0dd02` 33; 20 riders, so 13 extras, all read and confirmed prose or string literals |
| Each hand-written anchor resolved against its own file | `agents/smith.md` `"## Phases"` → one place, 27-233, holds line 60 · `skills/implement/SKILL.md` `"### 1. …"` → 243-458, holds line 379 · `templates/evidence-check.yml` quoted line → 1-18, holds line 5. No narrower heading exists in either markdown file |
| `evidence_check.py#content_at` and its only caller | returns bare `None` for all three causes, but `migrate` at `:1474` never turns it into a sentence — it counts the row unproven and falls through. No second instance of finding 6's class |
| `ruff --version` in `.venv` and on `PATH` | `No module named ruff`; `ruff not found` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` · `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S4 | round 1's 1 — fixed |
| round-1 | `.github/scripts/rider_check.py:421` · message at `:344` | round 1's 2 — fixed |
| round-1 | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | round 1's 3 — fixed |
| round-1 | `.github/scripts/rider_check.py:197` and `:218` | round 1's 4 — fixed |
| round-1 | `agents/smith.md:60` · `skills/implement/SKILL.md:379` · `templates/evidence-check.yml:5` | round 1's 5 — fixed |
| round-1 | `.github/scripts/rider_check.py:359` and `:504` · `phases/phase-4.md` · ledger row S4 | round 1's 6 — fixed |
| round-1 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md:28` · `overview.md:36` | round 1's 7 — fixed |
| round-1 | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-3.md` | round 1's 8 — fixed |
| round-1 | whole tree | round 1's 9 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a rider written as a trailing comment should be caught at all, in either form. Round 2 adds the markdown half of the shape; the rule still needs a comparison between the grep corpus and the reader's, which a fix pass may not add | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md`, finding 13's row | the repository owner (carried from round 1's fix pass, widened) |
| The `refs/pull/<N>/head` spelling in six documents and one assertion | corrected in `e1b83b8` — no longer deferred. `templates/sdd-round.md:54-64`, `spec.md`, `questions.md` A2, `phases/phase-1.md`, `changelog.md`, ledger row S5 and `tests/test_a_rider_reaches_its_file.py:121` all read `refs/remotes/pull/<N>/head` | closed |
| Whether the mid-run `git checkout 29e0460 -- .` lost any uncommitted work | `overview.md`'s *Where spec and implementation diverged* | the implementing session (carried, unchanged) |
| Whether a drifted rider is answered often enough to be worth its noise | `seal/follow-up.md` | the repository owner (carried, unchanged) |
| `templates/evidence-check.yml`'s rider is half spent | `overview.md` | the repository owner (carried, unchanged) |
