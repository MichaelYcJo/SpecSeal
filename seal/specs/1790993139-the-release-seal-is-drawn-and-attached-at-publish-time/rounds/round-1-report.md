# Round 1 report — the release seal is drawn and attached at publish time

- Work item: `1790993139-the-release-seal-is-drawn-and-attached-at-publish-time` (#718 boxes 2 and 3, #721, #722)
- Target: `28c807fc` on `feat/718-the-release-seal-is-drawn-and-attached-at-publish-time`; base `origin/release/v0.18.0` at `233f0455`; diff `233f0455..28c807fc`
- Round: 1 (no earlier round exists, so nothing is carried)
- Ran by: `specseal:warden on claude-opus-5-5`
- Where: a `git clone --no-local` of the worktree at `28c807fc` in the round's scratch directory, and a second clone at `233f0455` for the base measurements. Nothing was written in the worktree except this file.

## Summary

The build does what its spec asks on the paths its cases drive. I reproduced
the 0.17.0 measurement independently: 10 items, 27 rounds, 6 capped and 12
deferred. The exact-match lookup of the glance table also holds against two
notes GitHub really published. Every exception path inside
`release_seal.py#main` ends in exit 0. Pillow reaches nothing under `hooks/`
or `skills/`.

Two of the build's own promises are not kept, and both were checked by
execution:

- **The chain rows do not fall back to `not read` when the round records are
  missing (🔴 1).** That fallback is the condition `questions.md` Q1 gave for
  reading the tree at all. A tree with no `seal/specs/` makes the seal print
  `0 . 0 rounds`, `capped 1 of 0` and `0 issues`, and nothing is logged.
  Smaller versions of the same gap sit inside the loop (🟡 2).
- **#722's bound does not hold for a record that another plugin version
  wrote (🟡 3).** Yet that record is the reason `describe` re-applies the
  caps when it reads. Two gates come to 1,023 units, against a 1,000-unit
  reserve.

The workflow has two hardening gaps the step-level `continue-on-error` cannot
close. The first is a hung suite (🟡 4). The second is the write token that
`actions/checkout` leaves in `.git/config` while the suite runs (🟡 5). Four
⬜ rows follow: one is a question for the owner and three are wording fixes.

## Stage 1 — spec compliance

| Spec | What the account claimed | What I found |
|---|---|---|
| S1 | The glance table is replaced byte for byte | Read: `seal_release` replaces `glance`'s text with `sealed_glance`'s. **Executed:** I fetched the published v0.16.0 and v0.15.5 notes with `gh release view`, rebuilt each glance block from a fresh `gh pr list` through `tally` and `glance`, and found it exactly once in each, with no `\r` in either body |
| S2 | Any failure leaves today's note | Read: `main` catches `Exception` and `SystemExit`, and the module imports only the standard library, so no import can fail before `main` runs. A job-level timeout is outside every step's `continue-on-error`, though (🟡 4) |
| S3, S4, S12 | Hand-edited note left alone; `created` output; dry run | Read and driven by the module's cases, 98 passed (executed) |
| S5 | The workflow cannot turn red; the suite runs with no token | The steps are each `continue-on-error`, but the job has no timeout (🟡 4), and the token is left in `.git/config` (🟡 5) |
| S6, S7 | The PNG carries the terminal colours | The pixel case passed in the clone (executed). Q11, which font ubuntu gives, is still open as the overview says |
| S8, S9, S11 | Rows, JUnit, alt text | Read, and the cases passed (executed) |
| S10 | A source that cannot be read gives `not read`, never zero | **Not met** for a tree with no declarations, for an unreadable `rounds`, or for a malformed verdict row. All three were executed (🔴 1, 🟡 2) |
| S13 | #721 rewrap | Read: the paragraph matches, and the stamp module's cases passed (executed) |
| S14, S15 | #722 caps on write and on read; the two-gate report fits the reserve | The caps work for this plugin's own records. They do not hold for a record whose group/gate pair is not in today's `GROUPS`, or whose file name is long (🟡 3, executed) |
| S16 | Pillow pinned once | Read, and the runner and floor modules passed (executed). The dist-info name `pillow-12.3.0.dist-info` is what a uv build really writes (executed) |

**The 909 at base.** The account says the figure was already stale at the
base, and I checked that claim. Measured over `describe` with a 19-unit
`ModuleNotFoundError` and a 200-unit message, both at `233f0455` and at
`28c807fc`, the figures are 538, 915 and 1,289. That matches the `Corrected`
note on `seal/releases/0.17.0.md` B1.

**The 13th deferral.** The account says #722 is named only in a `## Deferred`
section. That is true: `grep -rn "#722"` over the base tree's round records
finds one line, which is row 94 of
`seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/rounds/round-3.md`
inside its `## Deferred` table. See ⬜ 6 for what that leaves open.

**The ledger edits.** I opened each re-read row's claim against the edit:
0.10.0 S1, 0.11.1 S9, 0.15.0 P1c, 0.15.1 P1/P2/P3, 0.15.3 A6, 0.16.0
G1/G2/P1-1, 0.17.0 B1/B2, and 0.8.2 R1/R3/R4. Every re-read claim holds
against the code at `28c807fc`, with one exception. **0.17.0 B1's corrected
claim and the fragment's D1 state 957 as the bound "as it reads a record",
and that is false under 🟡 3.** The evidence check over the clone reported 0
drifted and 0 broken anchors (executed).

## Stage 2 — quality

### 🔴 1 — A tree whose round records are missing draws zeros, not `not read`

`.github/scripts/release_seal.py:422` (`chain_counts`). The loop starts at
`items, rounds = 0, 0` and only counts pull requests whose branch
`routing.item_dir` resolves. When the tree holds no declarations at all,
`item_dir` answers `""` for every pull request. The function then returns
`(0, 0, capped, 0)` and logs nothing. The tree can be empty for three
reasons: #715 moves the records, a release's work items were retired before
the tag, or `seal/` lives under the git directory. `release_rows` then draws
`items 0 . 0 rounds`, `capped 6 of 0` and `deferred 0 issues`.

This matters because the decision to read the tree at all rests on the
opposite behaviour. `questions.md` Q1 says: *#715 moving the records turns the
rows into `not read`, never a wrong number*. S10 says *never dropped and never
zero*, and `NOT_READ`'s comment says *a 0 reads as a count*. A seal is the one
artifact people read as a measurement, and `capped 6 of 0` is not a
measurement.

Executed: `chain_counts` over an empty directory, with one pull request
labelled `chain: capped` and one unlabelled, returned `(0, 0, 1, 0)` and
printed nothing. The rows it drew were `('items', '0 . 0 rounds')`,
`('capped', '1 of 0')` and `('deferred', '0 issues')`.

The class is wider than the empty tree. A pull request labelled
`chain: capped` is by definition a reviewed work item, so when one resolves to
no declaration, the item count is known to be incomplete. That happens when
its work item was retired, renamed, or held a `routing.md` that did not
decode. Both shapes are covered by the fix below. One residual case is left:
an uncapped item that was retired is still invisible, and nothing the tree
carries can show it.

### 🟡 2 — Two more incomplete reads become numbers

This finding is the same class as 🔴 1, at two more coordinates inside the
same loop.

- `.github/scripts/release_seal.py:428`. When `routing.rounds_unreadable(item)`
  is true, only the deferred count is dropped. `routing.rounds(item)` returns
  `[]` for the same item, so its rounds are counted as zero. The log then says
  *the deferred row is not read*, while the rounds row drew a wrong number
  beside it. Executed: a `rounds` that is a file, the shape `routing.py`'s own
  docstring says this release's migration produces, gave
  `(1, 0, 1, None)` → `items 1 . 0 rounds`.
- `.github/scripts/release_seal.py:439`. `verdict_table` returns a fourth
  value, `errors`, which lists the rows it skipped for having fewer cells than
  the Verdict column needs. `chain_counts` discards it as `_errors`. A
  `deferred #13` in such a row is silently left out of the count. The
  function's own docstring says *an incomplete count is a wrong number*.
  Executed: two rows with `deferred #12` and `deferred #13`, the second short
  one cell, gave deferred `1` and no log line.

### 🟡 3 — #722's bound does not hold for a record another plugin version wrote

`hooks/dispatch.py:468` and `hooks/dispatch.py:461` (`describe`). The build
re-caps `error`, `message` and `group` on read, *because `read_record`'s
writer may be an older or a newer plugin*. Two fields of the same record still
escape the bound. The reserve's figures, D1 and B1's corrected claim are all
measured only over records this plugin writes.

- **The group's expansion trusts today's `GROUPS`.** At line 468,
  `if phase == "load" and group in GROUPS` adds every group the gate belongs
  to in *this* version. An older or newer plugin can record a known group that
  does not contain the gate, for example because a gate moved between groups
  across versions. For such a record, the line names three groups twice:
  `session-lease.py failed to load in session-start and post-bash and
  post-edit (…); …, and the other gates in session-start and post-bash and
  post-edit still decided.` That line is 431 units, where the build's longest
  is 400. Executed: two distinct gates in that shape, with every field at its
  cap, give **1,023** units. The reserve is 1,000.
- **The gate's name is the record's file name, and it has no cap.** The
  docstring excuses it because *the reserve's figures measure over `GROUPS`*.
  That is the same argument the build rejected for `group` one sentence
  earlier. Executed: two records named with 120-character gate names give
  **1,118** units.

Contract §12 and the spec's own grounding row make #722 a class: *every field
the failure report takes from a record without a fixed vocabulary is bounded*.
This is that class's last two members.

Executed with both changes in the fix applied, over every known gate plus
three 300-character foreign names, every known group plus a 300-character
foreign one, and phases `load`, `run` and none: **564, 972 and 1,378** units.
Two gates fit the reserve and three do not, which is the property the reserve
is meant to have. With that fix, the reserve comment, D1 and B1 have to state
those three figures, and the case that measures them has to iterate the
foreign shapes.

### 🟡 4 — A hung suite at the tag is not covered by any step's `continue-on-error`

`.github/workflows/publish-release.yml:69` (the `seal` job). Every step is
`continue-on-error: true`, but neither the job nor the suite step has a
`timeout-minutes`. A suite that hangs runs to the runner's 360-minute default.
The job is then ended by the runner, not by a failing step, and `continue-on-
error` on a step does not reach that outcome. The run should show a
non-success job and should have spent six hours of runner time first. This
memory's own record says a single Bash call once sat for 4h48m.

This is runtime behaviour I did not execute. GitHub documents `timeout-minutes`
and job-level `continue-on-error`. Whether a timed-out job reads as `failure`
or `cancelled` is the part I have not seen. Either way it is not the green
job that S5 promises.

### 🟡 5 — The suite at the tag runs with a write token in `.git/config`

`.github/workflows/publish-release.yml:76`. `actions/checkout@v4` persists
the job's token by default as an `http.extraheader` in the checkout's
`.git/config`. The `seal` job runs under `contents: write`, so every process
in the suite step can read a write-scoped token. The S5 case's docstring says
*the token is on the drawing step alone, so the suite at the tag runs with
none*. Spec §*Data & interfaces* says the same about the step's environment.
The environment half is true. The "runs with none" half is not.

Nothing in the job needs git credentials. The draw reaches GitHub through `gh`
with `GH_TOKEN`, and `tagged` only calls `git rev-parse`. So
`persist-credentials: false` costs nothing and makes the sentence true. This
is read, not executed. The smith may answer with grounds instead, but then the
docstring's sentence has to change.

### ⬜ 6 — The deferred row ignores the record's own `## Deferred` field

`.github/scripts/release_seal.py:445`. The deferred count reads only Verdicts
cells. The round record's `## Deferred` table is where a deferral is written
down: its heading is `round_record.py#DEFERRED`, and the warden definition
calls it the field that records an item taken out of scope and the durable
home it went to. 0.17.0's seal therefore says 12 where the owner's hand count
said 13. The 13th is #722, and it sits in exactly that table.

`questions.md` Q10 and the overview's *Not done* record this deliberately, so
there are grounds and it is not a defect. The overview's ground is *a second
section reader that no checker shares*. That is only half true. The shared
reader `chain_counts` already loads provides `sections` and `split_row`, which
are what a `## Deferred` count would use. **Question for the repository
owner:** should "deferred N issues" mean the issues a round wrote anywhere as
deferred, which would give 13 for 0.17.0, or only those in verdict cells,
which gives 12? Paste-ready fix 6 is the first answer, written out.

### ⬜ 7 — The refusal blames a hand edit for notes nobody edited

`.github/scripts/release_seal.py:526`. When the glance block is not found,
the reason given is always *the note was edited after publication*. Two other
causes reach the same branch:

- The publish job's `gh pr list` failed, and the note went out as the section
  alone. `release_body` returns `section` there.
- The two `gh pr list` calls, minutes apart, saw different sets.

`docs/release-checklist.md` §6 then sends the reader looking for an edit that
never happened. The behaviour is right and only the sentence is wrong.

### ⬜ 8 — The checklist's by-hand route draws from whatever checkout it runs in, and stops before the edit

`docs/release-checklist.md:343`. A `DRY_RUN` reads the chain rows from the
checkout the script sits in (`ROOT = CODE`) and the tag row from `git
rev-parse` there, so it has to be run from a checkout at the tag. The box does
not say so. The box also says to attach the PNG with `gh release upload`.
That leaves an asset the note does not show, the exact state the script's own
warning names as a failure. The dry run prints the note to write, and the box
should say to apply it.

### ⬜ 9 — "A re-run finds a release already there" is true of a full re-run only

`.github/workflows/publish-release.yml:21`. GitHub keeps the `publish` job's
outputs from the earlier attempt when only the `seal` job is re-run (read, not
executed). So `created` stays `true`. The glance-table guard and the upload's
refusal of an existing `seal.png` keep that safe, and a re-run after a flaky
suite would even seal correctly. The comment still states the opposite.

## Regression tests to plant

| Finding | Destination | Case |
|---|---|---|
| 🔴 1 | `tests/test_the_release_seal_is_drawn.py`, beside `test_the_chain_rows_count_items_rounds_capped_and_deferred` | A root with no `seal/specs/` → `(None, None, capped, None)` and a log line. A capped pull request resolving to no item → the same. Both are in fence 1 below. Seen red against `28c807fc` (executed as a probe: `(0, 0, 1, 0)`) |
| 🟡 2 | same file | A `rounds` that is a file → rounds `None`. A short verdict row carrying `deferred #13` → deferred `None`. Fence 2. Seen red as probes against `28c807fc` |
| 🟡 3 | `tests/test_a_gate_that_fails_says_so.py`, `longest_report` widened | Foreign gate names and a foreign group, phases including none. Fence 3. The current `describe` gives 1,023 for two gates, so the widened case is red until the guard lands |
| 🟡 4, 🟡 5 | `tests/test_a_release_publishes_its_note.py`, the S5 case | Assert `timeout-minutes` on the suite step and `persist-credentials: false` on the checkout. Fences 4 and 5 |

## Facts for the evidence ledger

- 0.17.0's chain counts over the base tree (`233f0455`), with the pull
  requests `publish_release_note.merged_pulls` lists for 0.17.0 run through
  `tally`: 10 work, 11 closed, 0 outside contributors. `chain_counts` gave
  `(10, 27, 6, 12)`. Capped pull requests: #696, #698, #699, #700, #705, #719.
  Every one of the ten resolves to a work item. Executed 2026-10-03.
- `gh release view` returns the v0.16.0 and v0.15.5 bodies with no `\r`, and
  `glance` rebuilt from a fresh `gh pr list` occurs exactly once in each.
  Executed 2026-10-03.
- `describe`'s reserve figures with a 19-unit name at `233f0455`: 538, 915
  and 1,289. Executed 2026-10-03.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A tree with no declarations (records moved by #715, items retired, or a capped pull request whose item is gone) gives the seal `0 . 0 rounds`, `capped N of 0`, `0 issues` with no log line, against S10, Q1 and `NOT_READ`'s own comment | `.github/scripts/release_seal.py:422` | open | Executed: `(0, 0, 1, 0)` over an empty root, nothing printed |
| 🟡 2 | An unreadable `rounds` counts its item's rounds as 0; a short verdict row's `deferred #N` is dropped because `verdict_table`'s errors are discarded | `.github/scripts/release_seal.py:428` | open | Executed: `(1, 0, 1, None)` and deferred `1` for two deferrals |
| 🟡 3 | `describe` expands a record's group from today's `GROUPS` even when the gate is not in it, and leaves the gate's file name uncapped; two gates reach 1,023 and 1,118 units against the 1,000 reserve, so the comment, D1 and 0.17.0 B1's corrected claim are false for the records the read-side cap exists for | `hooks/dispatch.py:468` | open | Executed over the clone's `describe`; with the fix, 564/972/1,378 |
| 🟡 4 | The `seal` job and its suite step have no `timeout-minutes`, so a hung suite runs to the 360-minute default and ends outside every step's `continue-on-error` | `.github/workflows/publish-release.yml:69` | open | Read; the runtime outcome is unverified, and the first hung run or the owner answers it |
| 🟡 5 | `actions/checkout` persists the `contents: write` token in `.git/config` during the suite step; the S5 docstring says the suite runs with none | `.github/workflows/publish-release.yml:76` | open | Read; answerable with grounds by changing the sentence |
| ⬜ 6 | The deferred row counts verdict cells only, not the record's `## Deferred` table, so 0.17.0 reads 12 against the owner's 13 | `.github/scripts/release_seal.py:445` | open | Decided by frame (Q10, overview *Not done*); a question for the repository owner |
| ⬜ 7 | The not-found refusal always says the note was edited, also when it was published as the section alone or the pull request set moved | `.github/scripts/release_seal.py:526` | open | Read |
| ⬜ 8 | The checklist's by-hand route does not say to run from a checkout at the tag, and stops at `gh release upload` without the edit | `docs/release-checklist.md:343` | open | Read |
| ⬜ 9 | The workflow comment says a re-run writes `false`; re-running the `seal` job alone keeps `created=true` | `.github/workflows/publish-release.yml:21` | open | Read; GitHub's re-run semantics not executed |
| 🟢 | The 0.17.0 reproduction holds: 10 items, 27 rounds, 6 capped, 12 deferred; #722 is named only in a `## Deferred` table | `.github/scripts/release_seal.py#chain_counts` | confirmed | Executed over a clone at `233f0455` with the live pull request list |
| 🟢 | Every exception inside `seal_release` ends as one `no seal:` line, one `::warning::` and exit 0; the module imports only the standard library | `.github/scripts/release_seal.py:549` | confirmed | Read; the 16 S2 cases passed (executed) |
| 🟢 | Pillow is test-and-release only: no file under `hooks/`, `skills/`, `bin/` or `.github/` imports it except `release_seal.py`; the floor module passes | `.github/scripts/run_tests.py#PILLOW` | confirmed | Executed: `grep -rnE "from PIL|import PIL"` exit 1; floor module green |
| 🟢 | The 909 at base was stale: 538, 915 and 1,289 at `233f0455` | `skills/verify/scripts/seal_stamp.py#MESSAGE_RESERVE` | confirmed | Executed |
| ❓ | The `seal` job on GitHub's runners: the font Q11 names, the browsers Q9 names, and whether the suite at a tag push (detached HEAD, a tag-push event payload in `GITHUB_EVENT_PATH`) passes as it does on `push: main` | `.github/workflows/publish-release.yml` | ❓ out of verified scope | Nothing local can run it; the repository owner answers at 0.18.0's tag push, from the job log and the release page |

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

The probe scripts were deleted after one run each. The two scratch clones and
the clone's `.venv` are removed with the round's scratch directory before
handover.

## Paste-ready fixes

### 1

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

### 2

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

### 3

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

The reserve comment in `skills/verify/scripts/seal_stamp.py`, the fragment's
D1 and `seal/releases/0.17.0.md` B1 then state 564, 972 and 1,378, as
measured over the patched `describe`. The smith re-measures them rather than
copying them from here.

### 4

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

### 5

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

### 6

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

### 7

```python
    if body.count(table) != 1:
        raise Refused(
            "the glance table is not in the note exactly once as `glance` "
            "writes it for this release -- the note was edited after "
            "publication, went out without one, or the pull requests moved "
            "between the two lists; nothing was uploaded"
        )
```

### 8

```
      To draw one by hand, from a checkout at the tag, run
      `DRY_RUN=1 python3 .github/scripts/release_seal.py` with `TAG`,
      `REPO` and `SUITE_XML` set; attach the PNG it names with
      `gh release upload`, then apply the note it prints with
      `gh release edit --notes-file`.
```

### 9

```yaml
# Then the seal (#718). A second job, `seal`, runs only when `publish` created
# the release in this run (`created` is its output; a re-pushed tag or a full
# re-run finds a release already there and writes `false`, and a re-run of
# `seal` alone keeps `true` and meets the glance-table guard instead).
```

Needs a fix: yes — 🔴 1 (the chain rows draw zeros for a tree they cannot read), 🟡 2 (two more incomplete reads become numbers), 🟡 3 (#722's bound does not hold for another plugin's record), 🟡 4 (no timeout on the seal job), 🟡 5 (the write token stays in `.git/config` during the suite)
Loses a record or crashes: no

## Proof block

Files opened in this round:

- `seal/specs/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time/spec.md`, `questions.md`, `overview.md`, `changelog.md`
- `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md`
- `.github/scripts/release_seal.py` (whole), `.github/scripts/publish_release_note.py` (the diff, `changes`), `.github/scripts/run_tests.py` (the diff)
- `.github/workflows/publish-release.yml`, `.github/workflows/test.yml` (the diff and the pytest job)
- `hooks/dispatch.py` (`GROUPS`, `capped`, `first_line`, `record`, `read_record`, `flat`, `describe`, `draw`), `hooks/routing.py` (`declarations`, `for_branch`, `item_dir`, `rounds`, `rounds_unreadable`, `_ordered`)
- `skills/code-review/scripts/chain_check.py` (`verdict_table`, `verdict_of`), `skills/verify/scripts/unverified_check.py` (`readable`), `skills/verify/scripts/seal_stamp.py` (the diff), `skills/verify/scripts/deferral_check.py` (head), `skills/code-review/scripts/round_record.py` (the `Deferred` lines)
- `tests/test_the_release_seal_is_drawn.py` (whole), and the diffs of `tests/test_a_release_publishes_its_note.py`, `tests/test_a_gate_that_fails_says_so.py`, `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` and `tests/test_release_hygiene.py`
- `CONTRIBUTING.md`, `docs/branch-and-release.md`, `docs/release-checklist.md` (the diffs)
- `seal/releases/0.8.2.md`, `0.10.0.md`, `0.11.1.md`, `0.15.0.md`, `0.15.1.md`, `0.15.3.md`, `0.16.0.md`, `0.17.0.md` (the changed words, and the claim of every row they touch)
- The base tree's round records for `#722` (`grep`), and `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/rounds/round-3.md`'s headings
