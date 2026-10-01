# Round 1 report — 1790815615, the seal names what it sealed and counts only the steps that run

Target SHA `512f6a89ee82d20f0b8588fdc0c9cf60a06553ae`, base `release/v0.17.0` at
`cd24f516`, diff `cd24f516..512f6a89`. Read and run in a `git clone
--no-local` of the branch at the target; nothing was written in the
worktree but this file. A first round: no earlier `round-N.md` exists for
this work item, so there is nothing carried and every verdict is this
round's.

What the build handed over was read as claims (§5). Each of the seven areas
the prompt names was opened; four findings need a fix, all 🟡, and one ⬜
is a paperwork correction. Nothing found leaves the root or crashes.

How the findings relate:

```
Q1 (owner) said: a long value continues beneath its label
   └─ 🟡 1  two kinds of value are elided instead — suite counts, deferred homes
            └─ 🟡 2  and the home itself is read as "the first word", which
                     misreads prose homes the tree already carries
the base the caller gave now keys the count
   └─ 🟡 3  the gate's coverage call is unpinned, and #638's hunk sits on that line
the gate row's new condition has three arms
   └─ 🟡 4  three documents state two of them (⬜ 5: the changelog fragment too)
```

## Findings from reading, then confirmed by execution

### 🟡 1 — The suite's counts and the deferred homes are elided at the frame, where the owner's Q1 answer says they continue beneath the label

`skills/verify/scripts/broad_gate.py:2555` passes every value through `fit`
on the way out, and two rows are built as one string:
`skills/verify/scripts/broad_gate.py:2528` (the suite's counts) and
`skills/verify/scripts/broad_gate.py:2419` (`<k> deferred -> <homes>`).
Where either is longer than `PANEL_VALUE_WIDTH` it is cut to 20 columns
plus `...`.

`questions.md` Q1, answered by the owner on 2026-10-01, is the default it
states: *"a value that does not fit on one row continues on an unlabelled
row beneath its label (`tree` / `base` names, `suite`'s exit, `ledger`'s
drifted and broken, `rounds`' deferrals), and a branch or ref name is
elided at the frame"*, with *"nothing is cut"*. Only the two names were
meant to be elided. `phases/phase-3.md` records the choice to elide the
homes as a decision of the phase, and
`tests/test_the_seal_is_taken_once_by_the_sealer.py:2883` pins it
(`endswith(gate.ELISION)` on the deferral row).

It reaches real records, measured over every work item in the tree
(executed): `1790645290`'s last record gives `4 deferred -> #673, #664`
(24 columns), drawn as `4 deferred -> #673, ...`, and `1790297085`'s gives
`4 deferred -> #611, #612, #610` (30), drawn as `4 deferred -> #611, ...`.
The homes are what the row exists to name, and the stamp hides them. The
suite row is the same shape one release away: this repository's suite is
`5081 passed, 10 skipped`, exactly 23 columns, so the next hundred tests or
any `xfailed` or `warnings` term elides the skipped count.

Why it matters: the stamp is the one artifact drawn for a person, and a
row ending `...` sends that person to the record to learn which issues the
run deferred, which is the reading this work item exists to save.

### 🟡 2 — A deferral's home is read as the first word after `deferred`, and the tree carries homes that are not one word

`skills/verify/scripts/broad_gate.py:2366` returns `rest.split()[0]`.
`chain_check.verdict_of` accepts any text after the word as a home, so
every shape below is a closed `deferred` row the gate then misnames.
Measured over every `round-N.md` in the tree (executed), four rows read
wrong:

| Cell | Home printed |
|---|---|
| `deferred — issue #97 already holds this axis, and round 2 put it there` (`1788395377`, round 3) | `issue` |
| `deferred phase 9 of this branch` (`1790635413`, round 1, twice) | `phase` |
| `deferred — they are true statements about the past, …` (`1788395377`, round 1) | `they` |

Beside them, shapes a person types (probed): `deferred to #664` → `to`,
`deferred → #664` → `→`, which also puts a non-ASCII arrow on a panel whose
separators were made ASCII for the letter twin, and `deferred (#664)` →
`(#664)`. None of these is in a last record today, so no stamp drawn from
the tree as it stands prints one. The next capped run that writes its
deferral in prose does.

### 🟡 3 — The coverage line's base is unpinned through the gate, and the sibling #638 rewrites that very line

`skills/verify/scripts/broad_gate.py:2713` hands `coverage_line` the
caller's `base.given`, and `coverage_line` and `unanswered` default `given`
to `None` (`:2170`, `:2182`), which `base_is_main` reads as *not main*.
Dropping the argument survives the three gate modules (executed: 281
passed with the mutation in place). The only gate-level cases that check
the clause run at base `base`, where `None` and `base` print the same
sentence, and the two cases that run the gate at `main` assert nothing
about it.

The cost at `main` is a false sentence, and not a cosmetic one. Read over
this repository's workflow (executed): with the base the line says *runs 11
steps for this base and this seal answers 3. 2 more are steps CI skips…*;
without it the line says *runs 9 steps for this base and this seal answers
5. 4 more run only on a pull request into `main`*. That is wrong on its
face at a pull request into `main`, and it counts the `survivors` and
`corrections` arms as answered on the run that skipped both. The panel
would still read `8 of 11`, so line and panel would disagree.

This is the one place the diff makes the later merge unsafe.
`origin/feat/638-…` changes this line to `coverage_line(workflow) if
workflow and not args.preflight` (read, its `gate` hunk at `@@ -2318`), so
a hunk resolved toward that side's text drops the base silently and the
suite stays green. A trial merge (`git merge-tree`, executed) conflicts in
`broad_gate.py` and in six release ledger files. The other shared line,
`not_sealed(…)` in the failure branch, is pinned through the gate by
`test_the_failure_form_names_the_base_the_checks_were_asked_about`, so a
merge that drops its names goes red.

### 🟡 4 — Three documents state the `gate` row's condition without its third arm, and on this release's own seals that arm is the one that fires

`gate_copy` prints the row where the running copy is under the root AND
either its bytes differ from the invoked copy or **no invoked path was
handed over**. Its docstring says so, and so does the ledger fragment's N6.
Three documents state only the first half:

- `docs/the-broad-gate.md:106-112`: *"the panel's `gate` row reads `tree
  <version>` wherever the copy that ran is not byte for byte the copy
  invoked … The row prints nowhere else"*.
- `agents/sealer.md:82-85`: *"The stamp carries a `gate` row only where the
  copy that ran is not byte for byte the copy you invoked"*.
- `skills/verify/scripts/broad_gate.py:326-327`, the section comment.

The missing arm fires in two places. One is the tree's copy invoked
directly, where the copy that ran IS the copy invoked and the row still
prints. The other is every seal of this repository until 0.17.0 is
installed: the installed 0.16.0 copy redirects without setting
`SPECSEAL_BROAD_GATE_INVOKED_AS`, so the child has no path and prints
`tree <version>` on every stamp of the 0.17.0 run. A sealer reading
`agents/sealer.md` concludes the copies differ, and *"prints nowhere else"*
is false on the first stamps this release draws. The behaviour is the
stated direction (says more when it cannot tell); the documents are what
is wrong.

### ⬜ 5 — The changelog fragment carries the same two-arm sentence

`seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/changelog.md:11-14`
reads *"The `gate` row prints only where the copy of the gate that ran is
not byte for byte the copy that was invoked, so a stamp from a seal whose
branch did not change the gate no longer carries it"*. This is a correction
to the run's paperwork. It becomes `CHANGELOG.md` at the release, so it
goes with 🟡 4's fix.

## What was checked and holds

- **The cell and `chain_check`.** `seal_record` still writes `f"{tree}
  against {base}"` (`broad_gate.py:2616`, outside every hunk), and
  `round_record.py` and `chain_check.py` are not in the diff. The names go
  on the lines, the label and the panel only (read).
- **The names.** `sealed_names` over a detached HEAD, a bare 8- and
  40-character SHA, a 4-character hex prefix, `main` from a repository with
  no remote, `HEAD~2`, and `feat/a@b`, probed: each reads as `spec.md` S1
  intends, with no stray `@` and no `<sha> @ <sha>`. The no-remote case
  reads `main @ <commit>`, which `overview.md` records as a divergence from
  A3 with grounds. That divergence is right: `resolve_base` step 3 returns
  the spelling given, and `main @ 551c7967` repeats nothing. Branch names
  cannot hold spaces, and `@` reads unambiguously beside the ` @ `
  separator. The old values file without `branch` draws today's label
  (probed, and pinned by the A15 cases).
- **The panel's other rows.** Every value is at most 23 columns over a
  73-character branch and a `refs/remotes/other/…` ref. The branch keeps its
  head and the ref its tail, and the drawn letter carries both (probed,
  rendered). `SAMPLE_ROWS` is held against `panel` by a case (read, green).
  The `NOT SEALED` form's `ledger` entry ends with the `total:` line only
  where the quoted lines lack it (read).
- **The variable.** `main` builds a fresh `env` for the child and never
  writes its own environment. The child pops the variable after
  `parse_args` and before `gate()` runs any check, so neither the suite nor
  a gate the suite spawns inherits it (read, and both channel cases green).
  An older tree copy that does not pop it leaks a variable nothing reads.
- **`rounds`.** Over all 36 work items with records (executed), nothing
  raised and every `capped` sits on a record holding a deferral, which
  reproduces Q2's measurement. `deferred_home` uses the separators
  `chain_check` uses. 🟡 2 is about what it does after them.
- **`workflow`.** `ONLY_AT_MAIN` is held against the `!= "main"` guards from
  both sides, and the case is shown able to fail on a flipped guard.
  `4 of 9` and `8 of 11` come from the real workflow, and the stderr clause
  is pinned verbatim (read, green).
- **The uncommitted-cell line.** It prints for an untracked record under a
  shared root, and prints nothing for a record under `.git/seal/` in local
  mode, where `git status` answers empty (both probed). A red run and every
  refusal return before it (read).
- **The ledger.** `evidence-check .` unscoped exits 0 with `3205 ok · 0
  drifted · 0 broken`, and `--strict` exits 0 (executed). The six
  `Corrected 2026-10-01` notes and the N5 extension were read against the
  code: each states what changed, and each claim it leaves standing is true
  of the target. `survivors.md`'s two rows rest on grounds that hold. One
  is G2's history in its Notes cell, beside its own correction. The other
  is two phrases shared with no fact in common.
- **The class (§12).** A grep for `from` row, `row exit`, `lint clean`,
  `8 of 13`, `13 steps`, `beside \`from\``, `or \`plugin <version>\`` and
  the old head shape found nothing stale outside history, the tests that
  assert absence, and the case comments that name the old row. That covers
  `docs/`, `skills/`, `agents/`, `templates/`, `hooks/`, both READMEs and
  `CONTRIBUTING.md`. The two READMEs name no panel row. The one gap in the
  class is the `gate` row's condition, which is 🟡 4.

## Regression tests to plant

- `tests/test_the_gate_names_every_step_ci_runs.py`, in
  `test_a_release_pull_request_is_sealed_as_ci_would_judge_it`: the
  main-base clause through the gate (🟡 3). Run in the clone: green at the
  target, red with the base dropped from `gate`'s call.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in
  `test_no_value_on_the_panel_is_wider_than_the_frame_gives`: every home
  and the skipped count appear in the rows (🟡 1). Not run.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: a parametrized case
  over the deferral shapes in 🟡 2's table. Not run.

## Facts for the evidence ledger

None new. N6 in the fragment already states the third arm 🟡 4 asks the
documents to carry.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the suite's counts and the deferred homes are elided at the frame, where the owner's Q1 answer says a long value continues beneath its label; two real records lose homes (`4 deferred -> #673, ...`, `4 deferred -> #611, ...`) | `skills/verify/scripts/broad_gate.py:2555` | open | `questions.md` Q1's answered default; executed over the tree's 36 work items; the width case pins the elision at `tests/test_the_seal_is_taken_once_by_the_sealer.py:2883` |
| 🟡 2 | a deferral's home is the first word after `deferred`, so `— issue #97 …` reads `issue`, `phase 9 of this branch` reads `phase`, `to #664` reads `to`, `→ #664` reads a non-ASCII `→` | `skills/verify/scripts/broad_gate.py:2366` | open | executed over every `round-N.md` in the tree (four rows) and over typed shapes; `verdict_of` accepts all of them as homed |
| 🟡 3 | the coverage line's base is unpinned through the gate: dropping it survives the gate modules and makes the release-base line say `answers 5` over two arms that did not run; #638's hunk rewrites that line with one argument | `skills/verify/scripts/broad_gate.py:2713` | open | mutation executed (281 passed); line compared for `main` and `None` (executed); #638's hunk read; trial merge executed |
| 🟡 4 | `docs/the-broad-gate.md`, `agents/sealer.md` and the section comment state the `gate` row's condition without the no-invoked-path arm, which fires on every seal of the 0.17.0 run under the installed 0.16.0 copy | `docs/the-broad-gate.md:106` | open | `gate_copy` returns the row where `installed` is None (read; `test_the_gate_row_prints_only_where_the_copy_that_ran_is_not_the_one_invoked` asserts it); the 0.16.0 copy sets no variable |
| ⬜ 5 | the changelog fragment carries 🟡 4's two-arm sentence | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/changelog.md:11` | open | paperwork; goes with 🟡 4's fix |
| 🟢 | the `Broad gate` cell is `<sha> against <sha>` as before and `chain_check` reads it unchanged | `skills/verify/scripts/broad_gate.py:2616` | confirmed | outside every hunk; `round_record.py` and `chain_check.py` not in the diff |
| 🟢 | `SPECSEAL_BROAD_GATE_INVOKED_AS` reaches no check and no child gate | `skills/verify/scripts/broad_gate.py:3047` | confirmed | read: fresh `env` for the child, popped before `gate()`; both channel cases green |
| 🟢 | `ONLY_AT_MAIN` is held both ways, and `4 of 9` and `8 of 11` come from the real workflow | `tests/test_the_gate_names_every_step_ci_runs.py:1100` | confirmed | executed: module green; the flipped-guard arm shows the case can fail |
| 🟢 | the uncommitted-cell line prints only over an uncommitted record and never in local mode, on a red run or on a refusal | `skills/verify/scripts/broad_gate.py:2911` | confirmed | probed in a scratch repository in both modes; red and refusal return earlier (read) |
| 🟢 | the ledger's corrections and re-reads are true of the target | `seal/releases/0.15.1.md` | confirmed | `evidence-check .` and `--strict .` exit 0 (executed); each note read against the code |
| ❓ | whether the installed 0.16.0 hook draws a file the new gate writes, on screen | `hooks/sealer-stamp.py` | ❓ out of verified scope | no case can see a screen; `questions.md` Q3 names the owner as its answerer, on the first real 0.17.0 seal |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules the diff touches, in the clone | exit 0, 487 passed |
| `bin/evidence-check .` unscoped, then `--strict .` | both exit 0; `total: 3205 ok · 0 drifted · 0 broken` |
| a one-off probe calling `sealed_record`, `rounds_rows`, `pull_request` and `item_value` for each of the 36 work items with round records | no exception; 15 records read `capped`; two deferral rows over 23 columns (`1790645290`, `1790297085`) |
| the same probe reading every deferred row of every `round-N.md` through `verdict_table`, `verdict_of` and `deferred_home` | four rows whose printed home is not their home (🟡 2's table) |
| a one-off probe drawing `panel` over the longest inputs, `sealed_names` over nine shapes, `label` over three values files, `deferred_home` over ten cells, and the uncommitted line in a scratch repository in local and shared mode | as reported above |
| `gate`'s coverage call with `base.given` removed, then the three gate modules | exit 0, 281 passed — the mutation survives |
| 🟡 3's proposed assertion, at the target and then with the mutation | green at the target, red with the mutation; both files restored with `git checkout` |
| `coverage_line` over `hygiene.yml` for `main` and for `None` | `runs 11 … answers 3` against `runs 9 … answers 5` |
| `git merge-tree --write-tree` of the target with `origin/feat/638-the-record-arms-run-before-the-sealer-is-spawned` | conflicts in `skills/verify/scripts/broad_gate.py` and six `seal/releases/*.md` |
| the full suite, repository lint and typecheck (the broad gate) | not yet: not run by this round, and it is the sealer's once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — continue a list across rows rather than eliding it

In `skills/verify/scripts/broad_gate.py`, beside `fit`:

```python
def wrapped(label, value, sep=", "):
    """`value` on as many panel rows as it needs, broken after `sep`: the
    first row under `label`, the rest as `""` rows beneath it, which is what
    the owner chose over a wider panel (`questions.md` Q1). A list of counts
    or homes continues; only one part wider than the frame is still elided,
    by `fit`, with the marker (#666)."""
    out, line = [], ""
    for part in str(value).split(sep):
        joined = f"{line}{sep}{part}" if line else part
        if line and len(joined) > PANEL_VALUE_WIDTH:
            out.append(line + sep.rstrip())
            line = part
        else:
            line = joined
    out.append(line)
    return [(label if i == 0 else "", fit(row)) for i, row in enumerate(out)]
```

In `panel`, the suite rows:

```python
    rows += (
        [*wrapped(SUITE, counts), ("", exit_row)] if counts else [(SUITE, exit_row)]
    )
```

In `rounds_rows`, the deferral row:

```python
    if count:
        tail = f" -> {', '.join(homes)}" if homes else ""
        rows.extend(wrapped("", f"{count} deferred{tail}"))
```

In `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`test_no_value_on_the_panel_is_wider_than_the_frame_gives`, replace the
`rows[-1]` elision assertion with:

```python
    at = next(i for i, row in enumerate(rows) if row and row[0] == "rounds")
    beneath = " ".join(value for _label, value in rows[at + 1 :])
    for home in ("seal/follow-up.md", "#12345", "#12346"):
        assert home in beneath, beneath
    assert "67890 skipped" in " ".join(values), values
```

### 🟡 2 — read the home as a home, not as a word

In `skills/verify/scripts/broad_gate.py`:

```python
# What a home looks like inside a deferral's prose: an issue, or a path.
HOME_TOKEN = re.compile(r"#\d+|[\w.-]+(?:/[\w.-]+)+|[\w.-]+\.md\b")
# Where a home written as words ends: a spaced dash, or a sentence's stop.
HOME_END = re.compile(rf" [{chr(0x2014)}{chr(0x2013)}-] |\. ")


def deferred_home(chain, cell):
    """The home a `deferred <home>` verdict cell names, or None.

    Read after `chain_check`'s own normalisation (`EMPHASIS`, `MARKER`) and
    separators (`SEPARATORS`), and only for a row `verdict_of` already
    called `deferred`. An issue or a path anywhere in what follows is the
    home, because the tree writes `deferred — issue #97 already holds…` and
    a person types `deferred to #664`; where there is neither, the words up
    to the first spaced dash or full stop are, so `phase 9 of this branch`
    prints whole rather than as `phase` (#666)."""
    s = chain.MARKER.sub("", chain.EMPHASIS.sub("", cell).strip())
    if not s.lower().startswith(chain.DEFERRED):
        return None
    rest = s[len(chain.DEFERRED) :].strip(chain.SEPARATORS)
    if not rest:
        return None
    found = HOME_TOKEN.search(rest)
    if found:
        return found.group(0)
    return HOME_END.split(rest, maxsplit=1)[0].rstrip(".,;")
```

A case in `tests/test_the_seal_is_taken_once_by_the_sealer.py`:

```python
@pytest.mark.parametrize(
    "cell, home",
    [
        ("deferred #664", "#664"),
        ("**deferred** #664.", "#664"),
        ("deferred to #664", "#664"),
        ("deferred → #664", "#664"),
        ("deferred (#664)", "#664"),
        ("deferred — issue #97 already holds this axis", "#97"),
        ("deferred `seal/follow-up.md`", "seal/follow-up.md"),
        ("deferred [#664](https://example.com/664)", "#664"),
        ("deferred phase 9 of this branch", "phase 9 of this branch"),
    ],
)
def test_a_deferrals_home_is_read_whole(cell, home):
    """S4's homes over the shapes the tree's records and a person write: the
    home is an issue or a path wherever it stands, and words where it is
    neither, never the first word alone."""
    gate = gate_module()
    chain = gate.load(gate.RECORD, "specseal_round_record_for_home_case").chain
    assert chain.verdict_of([cell], 0) == chain.DEFERRED, cell
    assert gate.deferred_home(chain, cell) == home
```

### 🟡 3 — pin the base through the gate, and make the argument required

In `tests/test_the_gate_names_every_step_ci_runs.py`, at the end of
`test_a_release_pull_request_is_sealed_as_ci_would_judge_it` (run in the
clone: green at the target, red with the base dropped):

```python
    # #666 through the gate: the coverage line is keyed on the base it was
    # given, so at `main` it leaves out the two skipped steps, not the
    # milestone step that runs only into `main`.
    assert (
        "2 more are steps CI skips on a pull request into `main`, so this "
        "count leaves them out."
    ) in result.stderr, result.stderr
```

In `skills/verify/scripts/broad_gate.py`, so a merge that drops the
argument fails every gate run rather than reading `None` as *not main*:

```python
def unanswered(text, given):
```

```python
def coverage_line(text, given):
```

The three one-argument test calls of `coverage_line`, in
`tests/test_the_gate_names_every_step_ci_runs.py` at lines 835, 850 and 886,
then pass `"base"`.

### 🟡 4 — state the third arm where the condition is stated

`docs/the-broad-gate.md`, the #475 paragraph:

```markdown
that breaks an arm and passes itself, is named rather than dismissed: one
stderr line names the running copy's path and reads `tree <version>` or
`plugin <version>`, the panel's `gate` row reads `tree <version>` wherever
the copy that ran is not byte for byte the copy invoked, or where the tree's
copy ran with no invoked copy named to compare against — invoked directly,
or redirected by an installed copy older than #666 — and the pull request
asks the same scripts again. The row prints nowhere else: on every
redirected seal of a tree whose gate the branch did not change it said the
same thing and was read by nobody (#666).
```

`agents/sealer.md`, §*The command*:

```markdown
or `plugin <version>`. The stamp carries a `gate` row only where the copy
that ran is not byte for byte the copy you invoked, or where nothing told
it which copy you invoked — the tree's copy run directly, or an installed
copy older than #666: `tree <version>` there means the branch was measured
by the gate it ships, and a stamp with no `gate` row was measured by the
copy you invoked (#666). Quote the gate line
```

`skills/verify/scripts/broad_gate.py`, the section comment above `GATE_REL`:

```python
# says so; every run's stderr names which copy ran, `tree` or `plugin`, with
# its version, and the panel's `gate` row says `tree <version>` where that
# copy's bytes differ from the one the caller invoked, or where no invoked
# copy was handed over to compare (#666, `gate_copy`). A
```

Both document pins keep their sentences
(`tests/test_the_seal_is_taken_once_by_the_sealer.py:3021` and `:3031`).

Needs a fix: yes — 🟡 1 (counts and homes elided against Q1), 🟡 2 (a
home read as its first word), 🟡 3 (the coverage base unpinned, #638
rewrites that line), 🟡 4 (the gate row's third arm missing from three
documents)
Loses a record or crashes: no

The broad gate has not come due: this round leaves four findings open.

## Proof block

Files opened, all at the target in the clone:
`seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/spec.md`,
`…/plan.md`, `…/questions.md`, `…/survivors.md`, `…/changelog.md`,
`…/overview.md` (the divergence row), `…/phases/phase-1.md`,
`…/phases/phase-2.md` and `…/phases/phase-3.md` (regions);
`skills/verify/scripts/broad_gate.py` (the whole diff, and `Base`,
`resolve_base`, `under`, `suite_counts`, `COUNTS_RE`, `first_lines`);
`skills/verify/scripts/seal_stamp.py` (the whole diff);
`skills/code-review/scripts/chain_check.py` (lines 395–560, 1179–1260,
1490–1690); `agents/sealer.md`, `docs/the-broad-gate.md`,
`skills/verify/SKILL.md` and `skills/code-review/orchestration.md` (the
diff and the stamp sections); `.github/workflows/hygiene.yml` (the
`base_ref` guards);
`tests/test_the_gate_names_every_step_ci_runs.py` (lines 585–640,
975–1210), `tests/test_the_seal_is_taken_once_by_the_sealer.py` (lines
900–960, 2835–2910), `tests/test_the_gate_asks_the_range_ci_will_ask.py`
(lines 583–595); the word diff of `seal/releases/*.md`; `#638`'s
`broad_gate.py` diff against the base.
