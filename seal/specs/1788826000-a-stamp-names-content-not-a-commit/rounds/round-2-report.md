# 1788826000-a-stamp-names-content-not-a-commit — review round 2

| Field | Value |
|---|---|
| Target SHA | 2f0dd02 |
| Base of the reviewed diff | 404dd4d (`git diff 404dd4d..2f0dd02`) |
| Ran by | warden on claude-opus-5 |
| Round | 2, the verifying round |

## What this round was asked

Round 1 closed four findings that need a fix and four corrections, and this
round is the diff of those fixes — `eaa8030`, `bdf65df`, `923f86c` and
`e1b83b8`, plus the two record commits over them. Not the branch: the fixes.

The named targets were the twelve restored dates with a sample proved
independently and the twelfth (`4581fe1`) among them; the reverify rule in
both directions; whether `--only` selects what it says; whether the
re-enumeration that found the block merge in the HTML form reached a third
corpus or a third form; whether the two openers now agree and whether any
other reader in this branch is looser than its own docstring; the count behind
the trailing-rider deferral and its disposition; whether the record now says
something true about both `881fb0f` and `4f78074`; and whether `seal/ledger.md`'s
L5 and R8, re-stamped before being read, were read and recorded.

The report was to be a file, ids bare integers, one row per finding, no commit
SHA in any rider stamp, and `NAME NOT IN TREE` written on any line naming
something the tree does not carry.

## How the findings hang together

Every closure round 1 asked for holds, and I re-derived each rather than
reading the fix record. What this round opens sits in two groups.

- **Two are in the checker** — `--only` reports success for selecting nothing,
  and a markdown heading is still read as a comment head. Both are the class
  `923f86c` was written to close, one instance further on.
- **Four are corrections to records**, all under `seal/`. Three of them are one
  fact: a count taken before the last fix commit, carried into three files.

---

## The twelve dates hold, and a thirteenth was provable and left on purpose

**Executed**, in this repository rather than in a clone, so `4581fe1` is
present. For each of the twenty riders I took the pre-migration stamp from
`cbdd66e`, hashed the region its *current* anchor names at the commit that
stamp claimed, hashed the same region at HEAD, and compared.

Twelve pairs are identical, and each of those twelve carries exactly the
pre-migration date:

| Rider | Old stamp | Region hash then / now | Date in the tree |
|---|---|---|---|
| `hooks/cmdline.py:1775` | 2026-08-31 at `9829412` | `802768ca` / `802768ca` | 2026-08-31 |
| `hooks/cmdline.py:1814` | 2026-08-31 at `9829412` | `7693c50d` / `7693c50d` | 2026-08-31 |
| `hooks/dispatch.py:80` | 2026-09-02 at `5a831e8` | `fec67305` / `fec67305` | 2026-09-02 |
| `hooks/optin.py:51` | 2026-08-31 at `9829412` | `0d131b0f` / `0d131b0f` | 2026-08-31 |
| `hooks/review-history-guard.py:153` | 2026-08-31 at `9829412` | `3de7fd09` / `3de7fd09` | 2026-08-31 |
| `hooks/review-skill-gate.py:122` | 2026-08-31 at `9829412` | `98bb724e` / `98bb724e` | 2026-08-31 |
| `hooks/worktree-guard.py:165` | 2026-08-31 at `9829412` | `8801e5d6` / `8801e5d6` | 2026-08-31 |
| `hooks/worktree-guard.py:222` | 2026-08-31 at `9829412` | `7e3ba403` / `7e3ba403` | 2026-08-31 |
| `hooks/worktree-guard.py:1484` | 2026-08-31 at `9829412` | `7415c477` / `7415c477` | 2026-08-31 |
| `skills/code-review/scripts/round_record.py:1858` | 2026-09-06 at `9241a8b` | `a9185160` / `a9185160` | 2026-09-06 |
| `skills/evidence-check/scripts/evidence_check.py:1790` | 2026-09-07 at `70c272c` | `9046e0b6` / `9046e0b6` | 2026-09-07 |
| `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:618` | 2026-09-06 at `4581fe1` | `8e0a246a` / `8e0a246a` | 2026-09-06 |

The last row is the twelfth, and it is the one a `--no-local` clone cannot
prove. Its region hashes to `8e0a246a` at `4581fe1` and at HEAD, so
2026-09-06 is earned.

Three riders' regions moved between the stamped commit and HEAD —
`agents/smith.md:60`, `round_record.py:197` and `round_record.py:837` — and all
three read 2026-09-08, which is right. Two carry no provable stamp because
their old commit does not hold their file, and one never had a pre-migration
rider at all. **Read**: `phase-4.md` lines 24-40 state the split and name the
four hand-written anchors, and the fix record's own reason — choosing an anchor
means reading the rider — is the one that carries them.

**One rider was provable and is deliberately left.**
`templates/evidence-check.yml:5` hashes to `6a954d30` both at `9829412` and at
HEAD, so `--migrate`'s own rule would keep 2026-08-31; the tree reads
2026-09-08. That is disclosed in the same correction block —
*"`templates/evidence-check.yml` is provable at 2026-08-31 now that it has an
anchor, and is deliberately left alone for that reason"* — and the reason is
the one the other three rest on. I judge it defensible and correctly recorded:
the anchor was chosen by hand on 2026-09-08, round 1 put the anchor itself in
question, and the fix pass answered it with an executed measurement. A reading
happened that day. Nothing needs to change here.

## The reverify rule moves a date only where a hash moved, and `--only` takes a file

**Executed**, both directions, on a scratch tree with three modules — one
stamped with its own true hash, two stamped `00000000`.

- `--reverify --only hooks/b.py` wrote `hooks/b.py` alone. `a.py` and `c.py`
  came back byte-identical, and `a.py` still reads
  `# Verified 2026-01-01 against unit@ea8b798d` after a run whose `today` was
  `2026-12-31`.
- A second run with no `--only` wrote `hooks/c.py` and left `a.py` alone.

So the unchanged rider is skipped on the hash alone, the changed one still
moves, and `--only` selects one file rather than one rider. **Executed** on the
real tree: `rider_check.py` with no flags is `20 ok · 0 drifted · 0 broken`,
exit 0, so a full `--reverify` today would write nothing at all — which is
finding 3's steady state actually reached rather than argued.

`.github/scripts/rider_check.py:368-375` says it in the drift message, and
`test_the_drift_message_says_the_re_stamp_takes_a_file` asserts both halves.

## The merge closes in every form the reader can meet — and one it should not have met

**Executed**, seven constructions through `comment_blocks`:

| Constructed | Blocks | Stamps read |
|---|---|---|
| two `#` riders back to back, `.py` | `[(2,3), (4,5)]` | `00000000`, `deadbeef` |
| two `#` riders back to back, `.yml` | `[(1,2), (3,4)]` | `00000000`, `deadbeef` |
| two riders sharing ONE html comment | `[(3,4), (5,6)]` | `00000000`, `deadbeef` |
| **three** riders sharing one html comment | `[(3,4), (5,6), (7,8)]` | `00000000`, `deadbeef`, `feedface` |
| two html riders in two comments | `[(3,4), (5,6)]` | `00000000`, `deadbeef` |
| an html rider then a `#` rider in one `.md` | `[(3,4), (5,6)]` | `00000000`, `deadbeef` |
| an UNCLOSED html rider, then a later marker | `[(3,7), (8,9)]` | `00000000`, `deadbeef` |

The three-rider case matters because it exercises the `in_html` carry twice,
which the two-rider case does not. The class is closed for both forms, and
there is no third form to close: `READABLE` admits `.py`, `.md`, `.yml`,
`.yaml`, `.sh`, `.toml`, `.cfg`, `.txt`, and every comment head among them is
`#` or `&lt;!--`.

**I looked for the third corpus in the place the copy came from.** Round 1's
finding 6 was `content_at` printing one sentence for three causes.
`skills/evidence-check/scripts/evidence_check.py:1369` still returns a bare
`None` for all three — but its only caller, `migrate` at `:1474`, never turns
that `None` into a sentence. It counts the row unproven and falls through. So
the class has no second instance there, and nothing is owed. **Executed** by
reading both call paths.

## But a markdown heading is still read as a comment head — finding 11

`comment_blocks`'s docstring says the `#` form is *"a `#` comment in Python,
YAML and shell, or an HTML comment in markdown"*. The code at
`.github/scripts/rider_check.py:219` asks only `stripped.startswith("#")`, and
in markdown that is a heading.

**Executed.** A file under a scanned root holding `## RIDER: what one is`:

```
0 ok · 0 drifted · 1 broken
('templates/doc.md:3', 'BROKEN', 'no verification stamp. ...')
```

This is the same shape `923f86c` closed on the other side — a reader looser
than the paragraph above it — and it is the mirror instance the enumeration
stopped one step short of. It is worse than the HTML one in kind: the HTML
opener lost an alarm, and this invents one. Every loss this design states for
itself is a lost alarm, never an invented one, and CI exits 2 on a line nobody
wrote as a rider.

Nothing in the tree stands in it today — **executed**, the 33 marker lines
under the six roots hold no `#`-headed markdown line — so this is a defect
waiting on one future heading in any `.md` under `skills/`, `agents/`,
`templates/`, `tests/`, `hooks/` or `.github/`.

**The fix is verified, not proposed.** Against a patched copy: the corpus stays
at `20 ok · 0 drifted · 0 broken`, the heading returns `[]` where the
unpatched call returns `[(3, 3)]`, and the `.py` `#` form and the `.md` HTML
form are untouched. No `.md` file in the tree uses the bare `#` rider form.

## And `--only` reports success for selecting nothing — finding 10

**Executed** on the working tree:

```
$ rider_check.py --reverify --only hooks/wortree-guard.py
0 restamped · 0 refused
exit=0
```

`reverify` at `:464` filters on `rider.rel != only` and counts nothing, so
`main` at `:603-610` prints a clean total and returns 0. A person answering a
drifted rider gets *done* for a run that did nothing, and the tree is unchanged
underneath them.

The drift message prints the path itself, so a copy-paste always matches. The
reachable case is a path typed by hand — which `phase-4.md` and round 1's own
paste-ready fixes both ask for, one of them for `templates/evidence-check.yml`
— or an absolute one, or `./hooks/…`. Exit 0 is what makes it a defect rather
than a nuisance: it is the answer a script reads.

**The fix is verified.** Against the same patched copy,
`--only hooks/no-such-file.py` refuses with the path named, and
`--only hooks/m.py` still writes its one rider.

## Three ledger re-stamps were recorded and two were not — finding 14

The fix pass moved five hashes in `seal/ledger.md`. Three gained a sentence
saying who read what:

- `hooks/dispatch.py#run_gate` (`:270`) — a note on why the hash moved without
  the claim moving.
- L5 (`:738`) and R8 (`:989`), both anchored at `agents/smith.md#"## Phases"`.

**Read**, and the prompt's premise holds. R8's note says it in its own words —
*"**Re-read 2026-09-08 in work item 1788826000's round 1 fix pass**, the drift
this note predicts, for the third time"* — and R8 had already written down that
`## Phases` is the whole procedure and drifts on any edit to it. L5 carries the
same re-reading as its third such entry. Both `Checked` columns are unmoved
(2026-09-04 and 2026-09-05), which is `evidence_check --reverify` behaving:
it writes the hash and never the column.

**Two rows moved with no note at all.**

- `seal/ledger.md:1203`, *The class check cannot pass vacuously*,
  `test_the_refusal_above_can_actually_fail@56d55d18` → `@d3aa66c9`.
- `seal/ledger.md:1418`, R5, `skills/evidence-check/scripts/evidence_check.py#unread_items@26161a0a` →  <!-- NAME NOT IN TREE -->
  `@1edf61c5`.

**Executed**: in both regions the only edit is that rider's own date digit —
`2026-09-08` → `2026-09-06` and `2026-09-07`. So both claims plainly hold, and
that is exactly why the silence matters: a reader cannot tell these two from a
hash that moved because the code did. `seal/ledger.md`'s own discipline is
against a re-stamp *"on behalf of a session that never read it"*, and the same
pass wrote that sentence three times for the other three rows.

## The refusals now say something true about both commits — finding 6 closed

**Executed**, both:

| | `881fb0f` (`fold_ledger.py`) | `4f78074` (`root-migrate.py`) |
|---|---|---|
| `git cat-file -t` | commit | commit |
| ancestor of HEAD | yes (exit 0) | yes (exit 0) |
| `git show <sha>:./<path>` | *exists on disk, but not in `881fb0f`* | *exists on disk, but not in `4f78074`* |

`phase-4.md` lines 82-95 and ledger row S4 both now say *a stamp that was wrong
when it was written* rather than the squash caught in the act, and both name
`4f78074` as the same shape. `content_at` at `:387-414` returns the cause, and
`test_a_refusal_names_which_of_the_three_things_failed` pins all three.

## The count behind the trailing-rider deferral moved under it — findings 12 and 13

**Executed** at `2f0dd02`: a grep of the six roots finds **33** marker lines
against the reader's 20 riders, so there are **13** extras, not 11. I read all
thirteen: every one is prose, a docstring, or a string literal.

The number was true when it was taken. **Executed**: 31 at `eaa8030`, 33 at
`923f86c` — the HTML fix planted the opener in the case file twice, at
`tests/test_a_rider_reaches_its_file.py:289` and `:435`, and the three records
carrying the count were written after it.

- `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md:20`, row S3,
  in a cell stamped **Executed 2026-09-08** with `Checked` 2026-09-08.
- `seal/specs/1788826000-…/overview.md:36`, where the count is the whole
  grounds for *"the tree does not stand in this today"*.
- `seal/specs/1788826000-…/rounds/round-1-fixes.md:52`.

R5 in the same ledger already records the remedy this repository adopted for
exactly this — *"an aggregate moves with every line of prose a branch writes,
which is why a count is not a coordinate and why this one now carries the
commit it was taken at"*. S3's count carries no commit.

**And the deferral is written for one corpus.** It names
`value = 1  # RIDER: …` only. **Executed**: the markdown form,
`some text &lt;!-- RIDER: … --&gt;` under a scanned root, gives
`0 ok · 0 drifted · 0 broken` — equally read by nothing, equally silent. That
is the round's own class appearing inside the deferral that closes it, and the
repository owner is being handed half the shape.

## The orchestrator already answered one open row — finding 15

`overview.md:37` lists, as not verified and owned by the orchestrator, that the
records arm refuses eight names in `rounds/round-1.md` and
`rounds/round-1-report.md` and exits 2. **Executed** on the working tree:

```
records — what unreleased work items state about the tree
  3 work items read · 42 unread · 416 names read · 0 stamps read · 0 refused · 0 drifted · 0 external
exit=0
```

`2f0dd02` is the commit that answered it — three `NAME NOT IN TREE` marks in
`round-1.md` and six in `round-1-report.md`. The row is closed and still listed
as open, which sends the next session to redo it.

## Not verified

The full suite, the repository-wide lint and the typecheck are the
orchestrator's under contract §2, and this round ran none of them. **Executed**
on the point the fix pass raised: there is no `ruff` in `.venv` and none on
`PATH`, so no lint has run anywhere in this work item. It is not *deferred*
until the orchestrator has an interpreter that carries it.

---

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
| 10 | 🟡 `--reverify --only <path>` that matches no rider prints `0 restamped · 0 refused` and exits 0 | `.github/scripts/rider_check.py:464` and `:603-610` | open | **executed** — `--only hooks/wortree-guard.py` on the working tree returns exit 0 with a clean total and writes nothing. A hand-typed or absolute path selects nothing and the run reports success; exit 0 is what a script reads. Fix verified on a patched copy: the miss is refused by path and a real `--only` still writes its rider |
| 11 | 🟡 A markdown heading is read as a `#` comment head, against the function's own docstring | `.github/scripts/rider_check.py:219`, docstring at `:170-196` | open | **executed** — `## RIDER: what one is` in a `.md` under a scanned root gives `BROKEN … no verification stamp`, exit 2, for a line nobody wrote as a rider. Same class as the HTML opener `923f86c` closed, and it invents an alarm where every stated loss of this design loses one. Fix verified on a patched copy: the corpus stays `20 ok`, the heading returns `[]` against `[(3, 3)]` unpatched, and both real rider forms are untouched |
| 12 | ⬜ The marker-line count is 33 with 13 extras, and three records say 31 with 11 | `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md:20` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | open | **executed** — 33 at `2f0dd02`, 31 at `eaa8030`; `923f86c` added `tests/test_a_rider_reaches_its_file.py:289` and `:435`. All thirteen extras read and confirmed prose or string literals, so the substance holds and only the number is stale. S3's cell is stamped Executed 2026-09-08 and carries no commit for the count; R5 in the same ledger already records naming the commit as the remedy |
| 13 | ⬜ The trailing-rider deferral names the `#` form only | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:36` · `rounds/round-1-fixes.md:52` | open | **executed** — `some text &lt;!-- RIDER: … --&gt;` under a scanned root gives `0 ok · 0 drifted · 0 broken`, identical to the `#` form's silence. The owner is handed half the shape of the rule they are being asked to decide |
| 14 | ⬜ Two of the five ledger rows the fix pass re-stamped carry no note of a reading | `seal/ledger.md:1203` · `seal/ledger.md:1418` | open | **executed** — in both regions the sole edit is that rider's own date digit, so both claims hold; the record does not say so, and a reader cannot tell them from a hash that moved because the code did. The same pass wrote that sentence for the other three rows (`:270`, `:738`, `:989`) |
| 15 | ⬜ `overview.md` lists as open a records-arm refusal that `2f0dd02` answered | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md:37` | open | **executed** — the records arm now reads `416 names read · 0 refused · 0 drifted`, exit 0. `2f0dd02` added three `NAME NOT IN TREE` marks to `round-1.md` and six to `round-1-report.md` |

## Paste-ready fixes

Finding 10 — `.github/scripts/rider_check.py`, in `reverify`:

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

Finding 10 — the case, in `tests/test_a_rider_reaches_its_file.py`:

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

Finding 11 — `.github/scripts/rider_check.py`, four substitutions:

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

Finding 11 — the case, in `tests/test_a_rider_reaches_its_file.py`:

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

Finding 12 — `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md:20`,
the *Verified behavior* cell of row S3, first sentence:

```markdown
**Executed** 2026-09-08 at `2f0dd02`: the widened scan over six roots finds exactly 20 riders; a grep of the same roots at that commit finds 33 marker lines, and all 13 extras are prose or string literals. The count names the commit it was taken at because an aggregate is not a coordinate — it read 31 at `eaa8030` and moved when `923f86c` planted the HTML opener in the case file twice, which is the correction R5 in `0.9.0` already records.
```

Finding 12 — `rounds/round-1-fixes.md:52`, the right-hand cell:

```markdown
| **read by nothing, and silent about it.** Not in the tree: at `2f0dd02` a grep of the six roots finds 33 marker lines against the reader's 20 riders, and all 13 extras are prose or string literals. Closing it needs a rule comparing the two corpora, which a fix pass may not add — deferred to the repository owner in `overview.md` |
```

Finding 13 — `seal/specs/1788826000-…/overview.md:36`, replacing the row:

```markdown
| a rider written as a TRAILING comment is read by nothing and says nothing about it, because a block opens only at the head of a comment line. Both forms: `value = 1  # RIDER: …` in a `#` file, and `some text &lt;!-- RIDER: … --&gt;` in a markdown one. Executed in round 2 — each gives `0 ok · 0 drifted · 0 broken` under a scanned root. Executed at `2f0dd02`: a grep of the six roots finds 33 marker lines against the reader's 20 riders, and all 13 extras are prose or string literals, so the tree does not stand in either form today. Closing it means a rule that compares the grep corpus with the reader's, which is mechanism a fix pass may not add | the repository owner. `skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it* is why it is written here rather than built |
```

Finding 14 — appended to the Notes cell of `seal/ledger.md:1203`:

```markdown
 **Re-read 2026-09-08 in work item 1788826000's round 1 fix pass**: the only edit inside `test_the_refusal_above_can_actually_fail` was its own rider's date, restored from 2026-09-08 to the 2026-09-06 `--migrate` proved. The region moved by one digit inside a comment and the claim did not move at all.
```

Finding 14 — appended to the Notes cell of `seal/ledger.md:1418`, row R5:

```markdown
 **Re-read 2026-09-08 in work item 1788826000's round 1 fix pass**: the only edit inside `unread_items` was its own rider's date, restored from 2026-09-08 to the 2026-09-07 `--migrate` proved. The region moved by one digit inside a comment and the claim did not move at all.
```

Finding 15 — `seal/specs/1788826000-…/overview.md:37`, replacing the row:

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
| round 1, finding 4 | `.github/scripts/rider_check.py:170-232` | The whole block reader in one function; both round-1 and round-2 findings in it live here |
| round 1, finding 1 | `cbdd66e` as the last pre-migration tree | The only place a rider's old `Verified <date> at <sha>` stamp survives, so any later re-derivation of the twelve starts there |
| round 1, deferred | `seal/ledger.md:989`, row R8's Notes | Already records that `## Phases` is coarse and drifts on unrelated edits, and why the minor-anchor escape hatch was not taken. It answers the same question for the rider now anchored there |
| this round | `seal/ledger.md:1418`, row R5's Notes | Holds this repository's own rule for a stale count — an aggregate is not a coordinate, so the number carries the commit it was taken at |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a rider written as a trailing comment should be caught at all, in either form. Round 2 adds the markdown half of the shape; the rule still needs a comparison between the grep corpus and the reader's, which a fix pass may not add | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/overview.md`, finding 13's row | the repository owner (carried from round 1's fix pass, widened) |
| The `refs/pull/<N>/head` spelling in six documents and one assertion | corrected in `e1b83b8` — no longer deferred. `templates/sdd-round.md:54-64`, `spec.md`, `questions.md` A2, `phases/phase-1.md`, `changelog.md`, ledger row S5 and `tests/test_a_rider_reaches_its_file.py:121` all read `refs/remotes/pull/<N>/head` | closed |
| Whether the mid-run `git checkout 29e0460 -- .` lost any uncommitted work | `overview.md`'s *Where spec and implementation diverged* | the implementing session (carried, unchanged) |
| Whether a drifted rider is answered often enough to be worth its noise | `seal/follow-up.md` | the repository owner (carried, unchanged) |
| `templates/evidence-check.yml`'s rider is half spent | `overview.md` | the repository owner (carried, unchanged) |

Needs a fix: yes — findings 10 and 11
Loses a record or crashes: no

## Proof

Files opened in this round: `.github/scripts/rider_check.py`,
`skills/evidence-check/scripts/evidence_check.py`,
`tests/test_a_rider_reaches_its_file.py`, `agents/smith.md`,
`skills/implement/SKILL.md`, `templates/evidence-check.yml`,
`templates/sdd-round.md`, `hooks/cmdline.py`, `hooks/dispatch.py`,
`hooks/optin.py`, `hooks/review-history-guard.py`,
`hooks/review-skill-gate.py`, `hooks/worktree-guard.py`,
`hooks/root-migrate.py`, `.github/scripts/fold_ledger.py`,
`skills/code-review/scripts/round_record.py`,
`tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`,
`tests/test_the_records_can_be_carried_out_and_in.py`, `bin/test`,
`bin/evidence-check`, `seal/ledger.md`,
`seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md`, and under
`seal/specs/1788826000-a-stamp-names-content-not-a-commit/`: `overview.md`,
`spec.md`, `questions.md`, `changelog.md`, `phases/phase-1.md`,
`phases/phase-3.md`, `phases/phase-4.md`, `rounds/round-1.md`,
`rounds/round-1-asked.md`, `rounds/round-1-fixes.md`,
`rounds/round-1-report.md`. Plus `/Users/x/.claude/skills/writing-style/SKILL.md`.

Three probe scripts were written outside the repository, run once, and deleted.
The working tree is unchanged: `git status --porcelain` is empty.
