# Round 2 — report · `1788817290-the-derivation-misreads-and-the-record-refuses-the-id` (#211, #194, #227)

| Field | Value |
|---|---|
| Target SHA | a283e64 |
| Base | ffd1d05 (round 1's target) |
| Branch | fix/211-194-227-the-derivation-misreads-and-the-record-refuses-the-id |
| Worktree | /Users/x/orca/workspaces/SpecSeal/main-worktrees/wi-211 |
| Kind | verifying round |
| Ran by | warden on claude-opus-5 |

## What this round was asked

Round 2 is the verifying round for round 1's fixes. The surface is
`git diff ffd1d05..a283e64`, whose substance is four commits — `a77ef92` for
finding 3, `824bfca` for findings 1 and 2, `4dfde1d` for the case that closes
a surviving mutation, and `f8180f4` for the records. `release/v0.9.1` was
merged in at `29e0460` and `a283e64` and is not this branch's work.

Seven things were named to attack rather than read. Finding 3's one-character
regex repair, whose claim of an unchanged accepted language is exactly the
kind of claim worth a second measurement, with both patterns to be re-timed.
Findings 1 and 2's widening of `runner_reached`, whose re-enumeration over
3051 defs and whose stated cost at `src/conftest.py` were both to be
re-derived and judged. The one mutation that survived the fix pass's first
sweep, whose new case was to be re-run in case it pins the mutation rather
than the property. Finding 3's class, enumerated over 61 regex literals, and
the deliberate non-repair of `evidence_check.py#OLD_COORD_RE` with its
unreachability claim. The real home directory that made
`test_only_fixture_user_paths` red, and whether any other record carries one.
The two `# RIDER:` stamps, against the convention
`fix/239-a-stamp-names-content-not-a-commit` is moving to. And the four
`seal/ledger.md` and fragment anchors re-verified after each claim was
re-read.

## The shape of what I found

Everything round 1 opened is closed, and each of its six load-bearing claims
reproduced. What I opened is one defect and one gap, and they sit in a line:

- **The repair for finding 2 overshot.** Letting a `conftest.py` through from
  anywhere makes the predicate say `pytest only` about a fixture in a
  directory pytest never loads a conftest from — finding 1's own false
  sentence, at a placement the fix pass built one instance of and read as the
  whole cost.
- **The repair for finding 5 landed where nothing looks.** The `floor_record`
  deferral moved from a file whose rules are enforced to a `# RIDER:` under
  `tests/`, which the rider checks do not walk.

Two more are corrections to the paperwork rather than to the tool, and neither
changes what anybody runs.

---

## The defect the fix for finding 2 introduced

### A fixture in a directory pytest never loads a conftest from now reads `pytest only`

`skills/code-review/scripts/round_record.py:2011` is the gate the fix
rewrote:

    if not under_tests(rel) and base != CONFTEST:
        return False

Anything named `conftest.py` passes it, at any depth, in any directory.
`decorated_as(node, FIXTURE)` then answers True for a fixture in it, and
`call_sites` writes `pytest only`.

**pytest does not load every `conftest.py`.** It loads the ones on the path
from `confcutdir` — the rootdir by default — down to each collected test
file's own directory. In a tree whose tests all live under `tests/`, a
`src/conftest.py` is never imported, so its fixtures are injected into
nothing.

That is exactly the sentence round 1's finding 1 removed, pointing the other
way: the record tells a reviewer the runner covers a unit nothing covers.
`plan.md`'s alternatives table rejected the wider reach rule to avoid writing
it, and finding 1 was raised 🟡 for writing it.

**The class is wider than the one instance the fix pass measured.** The eleven
built placements in `round-1-fixes.md` hold one, `src/conftest.py`, and the
record reads its cost as that single row. Executed here: `a/b/conftest.py`'s
fixture moves the same way, so the members are every `conftest.py` in a
directory nothing is collected under, at every depth — a vendored tree, a
package directory, an example directory.

**The grounds the record gives do not hold.** The ledger fragment R2 and
`round-1-fixes.md` both say *a fixture in a file named `conftest.py` is
pytest's by construction wherever it sits*. It is not; the directory decides,
and that is the same half-of-the-rule mistake finding 1 was about.

**A narrower rule keeps both directions right, and needs nothing the module
does not already have.** A conftest is loaded when something is collected at
or below its own directory, which is one question against the tracked file
list `tracked_at` already fetches. The root conftest — the placement finding 2
was raised for — passes it in any repository that has tests at all;
`src/conftest.py` passes it in a colocated layout and fails it in a segregated
one, which is what pytest does. The paste-ready fix is below.

## And the fix for finding 5 put the rider where the rider checks do not walk

`seal/follow-up.md:15` states the rule — anything tied to a coordinate is a
`# RIDER:` at the line — and finding 5's fix followed it, moving the
`floor_record` deferral to `tests/test_the_reopening_is_one.py:164`.

`tests/test_a_rider_reaches_its_file.py:109` is the list the checks walk:

    RIDER_ROOTS = ["hooks", "skills", "agents", "templates"]

`tests` is not in it. So `test_every_rider_carries_the_date_and_sha_it_was_verified_at`  <!-- NAME NOT IN TREE -->
and `test_every_rider_stamp_names_a_commit_this_branch_can_reach` never see the  <!-- NAME NOT IN TREE -->
rider this branch planted, and the branch's own record asserts *the rider names
no commit of this branch* as though a check had answered it. I verified the
stamp by hand and it is correct — that is finding 7 below — but nothing in the
suite would have said so.

**The file itself records this failure one directory over.** The comment
directly above that list reads *`templates` was missing, so the rider in
`templates/evidence-check.yml` was never checked by anything at all*. The same
sentence is true of `tests` today, and #239 is the release's own instance of a
stamp nobody's check caught.

**Why the repair is not one word.** Adding `tests` turns the stamp check red
twice, and both are real:

- `tests/test_the_records_can_be_carried_out_and_in.py:1415` carries a rider
  with no `Verified … at <sha>` line at all.
- `tests/test_the_root_migrates_itself.py:442` carries the literal string
  `"# RIDER:"` inside an assertion, and `rider_stamps` splits on that text, so
  the assertion reads as a rider with no stamp.

The paste-ready fix below takes all three.

---

## What reproduced, claim by claim

### Finding 3 — the language is unchanged, and both patterns re-timed

Executed. Both patterns loaded from their own revisions and run side by side:

| Input | `ffd1d05` pattern | `a283e64` pattern |
|---|---|---|
| `"!" * 22 + "x"` | 0.171534 s | 0.000009 s |
| `"!" * 26 + "x"` | 2.836958 s | 0.000006 s |
| `"!" * 28 + "x"` | 11.392153 s | 0.000006 s |
| `"!" * 4000 + "x"` | not run | 0.000141 s |
| `"!" * 100000 + "x"` | not run | 0.003217 s |

The doubling per character reproduces, and so does the fix pass's 11.178 s at
28 characters within measurement noise.

**Equivalence, re-derived rather than read.** Both patterns over 6305
first-column table cells from 149 committed records, 1463 constructed shapes
of markers, spaces, digits and letters at lengths 1 to 3, and an exhaustive
sweep of every marker prefix up to length 4 crossed with five tails:
**0 disagreements**, on acceptance and on the captured id alike. My cell count
is 6305 against the record's 6245 because I read every `round-*.md` under
`rounds/` rather than the round records alone; the verdict is the same.

The one-character claim is right for a reason worth writing down: every
repetition of the group already consumes exactly one marker, and the outer `*`
supplies the run, so `[^\w\s]+` inside `[^\w\s]+\s*)*` only ever added ways to
split a run it was already accepting whole.

### Findings 1 and 2 — no verdict in this repository moves

Executed. `runner_reached` at `ffd1d05` and at `a283e64`, over every top-level
def in every tracked `.py` file at `a283e64` — 3052 defs in 114 files.
**Not one verdict moves.** The claim reproduces.

The built placements are where the boundary shows, and four of the five that
move are the two findings landing correctly:

| File | Unit | `ffd1d05` | `a283e64` |
|---|---|---|---|
| `tests/helpers.py` | `test_shaped_but_uncollected` | `pytest only` | **`no call site found`** |
| `conftest.py` (root) | `a_root_fixture` | `no call site found` | **`pytest only`** |
| `conftest.py` (root) | `pytest_configure` | `no call site found` | **`pytest only`** |
| `src/conftest.py` | `a_nested_fixture` · NAME NOT IN TREE | `no call site found` | **`pytest only`** |
| `a/b/conftest.py` | `deep_fixture` · NAME NOT IN TREE | `no call site found` | **`pytest only`** |
| `tests/helpers_test.py` | `test_in_a_suffix_module` | `pytest only` | `pytest only` |
| `conftest.py` (root) | `test_in_a_conftest` · NAME NOT IN TREE | `no call site found` | `no call site found` |
| `conftest.py` (root) | `a_root_helper` · NAME NOT IN TREE | `no call site found` | `no call site found` |
| `conftest_helpers.py` | `sneaky` | `no call site found` | `no call site found` |
| `src/mod.py` | `test_looks_like_one` | `no call site found` | `no call site found` |
| `src/mod.py` | `pytest_looks_like_a_hook` · NAME NOT IN TREE | `no call site found` | `no call site found` |
| `tests/pytest_named_helper.py` | `pytest_not_a_hook` · NAME NOT IN TREE | `no call site found` | `no call site found` |

The last five rows are the boundary holding, and one of them is worth naming:
`conftest_helpers.py` stays put, so the conftest arm compares the whole
basename rather than a prefix.

The fifth mover is finding 1 of this round.

### The surviving mutation — the new case kills the property, not the mutation

Executed, two mutations of `collected`, one at a time, `tests/__pycache__`
cleared between, and the unit restored through `Edit` afterwards with
`git status --porcelain` empty:

| Mutation | Result |
|---|---|
| `return base.startswith(TEST_PREFIX)` — the `_test.py` half dropped | **1 failed** · `test_the_second_python_files_pattern_collects_too` alone |
| `return base.endswith(TEST_SUFFIX)` — the `test_*` half dropped | **1 failed** · `test_a_pytest_test_function_reads_pytest_only` alone |

The new case asserts that a `test_*` def in `tests/helpers_test.py` reads
`pytest only`, which is pytest's second `python_files` pattern stated as a
property. It is not written around the mutation, and each half of the unit is
now held by exactly one case.

### Finding 3's class, and the disposition of `OLD_COORD_RE`

Executed. The cubic claim reproduces on the same shape:

| Input length | Time |
|---|---|
| 502 | 0.0315 s |
| 1002 | 0.2521 s |
| 2002 | 1.9545 s |
| 4002 | 15.7004 s |

Eight times the work per doubling of the input is cubic, and 15.7 s at 4000
characters matches the rider's 15.6 s.

**The unreachability claim holds and is stronger than the rider states.** All
1520 lines of `seal/ledger.md` and the `seal/ledger/*.md` fragments through the
pattern: the slowest is **0.000537 s** on an 8831-character row, not the
0.009 s on a 1213-character row the rider records. Nineteen rows fall in the
1150–1280 character band and the slowest of them is 0.000172 s. Nothing the
tree holds comes within four orders of magnitude of the cubic path, so the
judgment not to repair it stands: the repair changes which paths a coordinate
may name and 805 rows depend on that, which is an argument a fix pass does not
get to make on the side.

**The class enumeration is only partly re-derived, and I say so rather than
call it verified.** An independent scan of the 30 shipped scripts found 47
plain `re.compile("…")` literals against the record's 61, because mine skips
patterns built from concatenated or f-string parts — which is where
`ANCHOR_RE` and `OLD_COORD_RE` themselves live. So I neither confirm nor
contradict the count of four. What I did settle is the direction: the five
patterns in `hooks/review-history-guard.py`, which my cruder detector flagged
and the record's classified as flat, are flat — timed against adversarial
input at four lengths, every one linear at 0.00006 s or less.

### The real home directory, and the riders' stamps

Executed. `tests/test_no_real_identifiers.py` passes, and a grep for the
operator's home directory across the whole worktree returns one hit, the
untracked `.git` pointer file a worktree carries. `f8180f4` moved one line of
`round-1-report.md` and nothing else in it.

Both riders are stamped `Verified 2026-09-08 at 00e63c3`. Executed:
`00e63c3` is an ancestor of `HEAD` and of `origin/release/v0.9.1`, and is not
on `origin/main` — so it is a commit the squash into the release branch keeps
and the 3-way merge into `main` carries. The disposition is right, and it is
`fix/239-a-rider-stamp-names-a-commit-the-squash-discards`'s instance repair
applied by hand.

**What they should read once `fix/239-a-stamp-names-content-not-a-commit`
merges.** That branch replaces the commit with a content anchor, and both
branches touch the same convention on the same release, so whichever lands
second rewrites the other's two lines. Computed here with this tree's own
`evidence_check.content_hash` over each anchored region:

The rider at `tests/test_the_reopening_is_one.py:164` should read:

```
# Verified 2026-09-08 against tests/test_the_reopening_is_one.py#floor_record@bba5c7a1
```

The rider at `skills/evidence-check/scripts/evidence_check.py:77` should read:

```
# Verified 2026-09-08 against skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE@1ca5aff0
```

The hashes are what today's checker computes over each anchored region;
#239's migrator is the authority on them, and these are the values to check
its output against rather than a substitute for running it.

### The four re-verified anchors

Executed and read. `bin/evidence-check` reads **809 ok · 0 drifted · 0 broken ·
0 external · 0 old-format**, exit 0, and `bin/deferral-check` resolves, exit 0.
Four anchors moved in this range and I opened each claim:

| Where the anchor points | Claim | Verdict |
|---|---|---|
| the fragment's R1, at `FINDING_ID_RE` | one shared pattern, refusal naming the format | holds; re-derived above |
| the fragment's R2, at `runner_reached` | the three members pytest reaches | holds for what it states; its *wherever it sits* clause is finding 1 |
| the fragment's R4, at the fix-surface subsection of `docs/review-chain-spec.md` | the hole is stated rather than closed | holds; the added paragraph is about where a file sits and leaves the hole paragraph and its measured instance untouched |
| `seal/ledger.md`'s row at the review-arm heading of `docs/review-chain-spec.md` | both opt-in headings and the parity arm's silence row name `seal/` | holds; the added paragraph names neither |

Only one row of `seal/ledger.md` itself is this branch's. The other 30 changed
lines in the range are the merge of `release/v0.9.1` re-hashing `seal.py`
anchors for #111, which is not this branch's work.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Letting a `conftest.py` through from anywhere makes the predicate say `pytest only` about a fixture in a directory pytest never loads a conftest from — round 1's finding 1 pointing the other way, at every depth rather than at the one placement the fix pass built | `skills/code-review/scripts/round_record.py:2011` | open | executed — `src/conftest.py#a_nested_fixture` and `a/b/conftest.py#deep_fixture` both move to `pytest only` through the shipped predicate; pytest loads a conftest only for tests collected at or below its own directory, so neither is imported in a tree whose tests live under `tests/`. The grounds the ledger fragment and `round-1-fixes.md` give — *pytest's by construction wherever it sits* — are false of pytest |
| 🟡 2 | The rider that closed round 1's finding 5 sits under `tests/`, which the rider checks do not walk, so neither the stamp check nor the ancestry check can see it — the failure the list's own comment records for `templates` | `tests/test_a_rider_reaches_its_file.py:109` | open | executed — the roots are `hooks`, `skills`, `agents`, `templates`; `grep -rn "RIDER:" tests/` returns four files, one of them the rider this branch planted. Adding `tests` turns the stamp check red on an unstamped rider at `tests/test_the_records_can_be_carried_out_and_in.py:1415` and on the literal `"# RIDER:"` inside an assertion at `tests/test_the_root_migrates_itself.py:442`, so the repair is three parts |
| ⬜ 3 | One enumeration is reported with three different totals — 3048 in `824bfca`'s message, 3051 in the fixes record, the ledger fragment and the rider, 3052 in the tree the rider was written against | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md:4` | open | executed — top-level defs per SHA: `ffd1d05` 3003, `824bfca` 3051, `4dfde1d` 3052, `f8180f4` 3052, `a283e64` 3052. 3051 was true when `824bfca` was written and stopped being true when `4dfde1d` added a case; 3048 was never true on this branch. The conclusion the numbers carry — no verdict moves — reproduces at 3052 |
| ⬜ 4 | The `OLD_COORD_RE` rider's reachability measurement does not reproduce: it records 0.009 s on a 1213-character row as the worst the tree holds, and the worst is 0.000537 s on an 8831-character row | `skills/evidence-check/scripts/evidence_check.py:77` | open | executed — 1520 real ledger lines timed three times each; the 19 rows in the 1150–1280 character band top out at 0.000172 s. The claim the rider makes is unreachability and that direction holds with a wider margin than stated, so what is wrong is the number rather than the judgment |
| 🟢 5 | Round 1's findings 1, 2 and 3 are closed, each re-derived rather than read: the language is unchanged over 7768 strings, both patterns re-timed, and no verdict in this repository moves under the widened predicate | `skills/code-review/scripts/round_record.py:1646`, `:1980`, `:2011` | answered | executed — see *What reproduced, claim by claim* |
| 🟢 6 | The mutation that survived the fix pass's first sweep is killed, and the case that kills it pins the property rather than the mutation | `tests/test_a_runner_reached_unit_reads_pytest_only.py:370` | answered | executed — both halves of `collected` dropped separately, each killed by exactly one case, and the new case asserts pytest's second `python_files` pattern as a property |
| 🟢 7 | Round 1's findings 4 and 5 are closed, both riders name a commit the squash keeps, no record carries a real user path, and the four re-verified anchors hold their claims | `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md`, `seal/follow-up.md:44`, `tests/test_the_reopening_is_one.py:164` | answered | executed — `bin/evidence-check` 809 ok, 0 drifted, 0 broken, exit 0; `00e63c3` an ancestor of `origin/release/v0.9.1` and not of `origin/main`; `tests/test_no_real_identifiers.py` green and the tree carries no real home directory |
| ❓ 8 | The full suite, the repository-wide lint and the typecheck | the branch as a whole | open | unverified — `skills/agent-contract/SKILL.md` §2 reserves the broad gate for one run after the rounds settle. Executed here: five modules narrowly, plus `bin/evidence-check` and `bin/deferral-check`. The answerer is the orchestrator |

## Paste-ready fixes

Finding 1 — the predicate. The new unit is `conftest_is_loaded` · NAME NOT IN TREE
It goes below `collected`, and the gate in `runner_reached` calls it:

```python
def conftest_is_loaded(root, b, rel):
    """True when pytest loads this `conftest.py` at all.

    A conftest is loaded for the test files collected at or below its own
    directory — rootdir down to each test file, with `confcutdir` defaulting
    to rootdir — so one in a directory nothing is collected under is never
    imported and its fixtures are injected into nothing. Saying `pytest only`
    about a unit there is round 1's finding 1 pointing the other way: the
    repository root passes this in any tree that has tests at all, which is
    finding 2's placement, and `src/conftest.py` passes it in a colocated
    layout and fails it in a segregated one, which is what pytest does.
    """
    here = os.path.dirname(rel)
    prefix = f"{here}/" if here else ""
    return any(
        p.startswith(prefix) and p.endswith(".py") and collected(os.path.basename(p))
        for p in tracked_at(root, b)
    )
```

```python
    base = os.path.basename(rel)
    if not rel.endswith(".py"):
        return False
    if not under_tests(rel) and not (
        base == CONFTEST and conftest_is_loaded(root, b, rel)
    ):
        return False
```

The docstring's third paragraph in `runner_reached`, which states the boundary
the code now draws:

```python
    Where the file sits decides two different things, and they are not the
    same gate. A conftest is loaded by name rather than by directory, so the
    `tests/` gate lets one through from anywhere pytest would actually load
    it — the directories with a collected test module at or below them, which
    is the repository root in any tree that has tests. A conftest nothing is
    collected under is not loaded, so it is not a member either. Nothing else
    outside `tests/` is a member however it is named.
```

The case, and the placement it needs, in
`tests/test_a_runner_reached_unit_reads_pytest_only.py`. The new constant is
`NESTED_CONFTEST` and it goes beside `ROOT_CONFTEST` · NAME NOT IN TREE
`src/conftest.py` goes into `BEFORE`, `WIDENED` and `_build` beside
`conftest.py`, and the case goes into the boundary section:

```python
# The other half of finding 2's repair. pytest loads a conftest for the tests
# collected at or below its own directory, so one under `src/` in a tree whose
# tests live under `tests/` is never imported — and `pytest only` about its
# fixture is finding 1's false sentence at a second placement.
NESTED_CONFTEST = (
    "import pytest\n"
    "\n"
    "\n"
    "@pytest.fixture\n"
    "def a_nested_fixture(x):\n"
    "    return x\n"
)
```

```python
    "src/conftest.py": (
        "import pytest\n"
        "\n"
        "\n"
        "@pytest.fixture\n"
        "def a_nested_fixture(x, extra=None):\n"
        "    return x\n"
    ),
```

```python
def test_a_conftest_nothing_is_collected_under_is_not_loaded(reach):
    """Round 2's finding 1. `conftest.py` is a name pytest loads by, but the
    directory still decides whether it is loaded at all: rootdir down to each
    collected test file. `src/` holds no test module, so this conftest is
    never imported and its fixture is injected into nothing — the row would
    say the runner covers a unit nothing covers, which is the sentence
    `plan.md`'s alternatives table rejected the wider rule to avoid."""
    generator = generator_module()
    assert reach["a_nested_fixture"] == generator.NO_SITE, reach
```

The two rows of `docs/review-chain-spec.md` that say *anywhere*:

```markdown
| a fixture under `tests/`, or in a `conftest.py` pytest loads | injected by parameter name, so `name(` never occurs |
| a `pytest_*` def in a `conftest.py` pytest loads | dispatched by the plugin manager |
```

And the paragraph under that table, whose last two sentences state the rule
the code now draws:

```markdown
`conftest.py` is the opposite case: pytest loads it by name and documents the
repository root placement first, so a fixture or a hook there is reached from
outside `tests/` exactly as one inside it is. It is still the directory that
decides whether the file is loaded at all — rootdir down to each collected
test file — so a `conftest.py` with no test module at or below it is loaded by
nobody, and calling its fixtures the runner's is the same false sentence one
directory over. Both directions were round 1's findings on the change that
introduced this section, and the second one came back in the repair.
```

The ledger fragment R2's cost sentence, which currently states grounds that
are not true of pytest:

```markdown
**What letting a conftest through costs, and where the line now sits:** a
conftest is loaded for the tests collected at or below its own directory, so
the reach walk asks that question of the tracked file list rather than
accepting the name alone. The repository root passes it in any tree that has
tests, which is the placement #211's own defect stood at; `src/conftest.py`
in a tree whose tests live under `tests/` does not, because pytest never
imports it. Round 2's finding 1 is that accepting the name alone put finding
1's false sentence back at every uncollected directory.
```

Finding 2 — the rider roots, and the two things adding `tests` uncovers:

```python
# Where riders are allowed to live. `templates` was missing, so the rider in
# `templates/evidence-check.yml` was never checked by anything at all —
# `follow-up.md` names it as planted and nothing here could see it. `tests`
# was missing for the same reason and one release longer: four files under it
# carry riders, one of them planted by the branch that fixed #239's instance,
# and neither the stamp check nor the ancestry check could see any of them.
RIDER_ROOTS = ["hooks", "skills", "agents", "templates", "tests"]
```

```python
    for rel in {line.split(":", 1)[0] for line in out.splitlines()}:
        block = read(os.path.join(ROOT, rel))
        # A `# RIDER:` inside a string literal is a case asserting that a
        # rider exists somewhere else, not a rider. `tests/test_the_root_
        # migrates_itself.py` carries one, and splitting on the bare text
        # read it as a rider with no stamp.
        for chunk in re.split(r"^\s*# RIDER:", block, flags=re.M)[1:]:
            head = chunk.split("\n\n", 1)[0]
            m = STAMP.search(head)
            assert m, f"{rel}: a rider with no verification stamp"
            found.append((rel, m.group(1)))
```

And the stamp the third part needs, at
`tests/test_the_records_can_be_carried_out_and_in.py:1422`, on the line after
that rider's last sentence:

```python
# Verified 2026-09-03 at 3f8f846.
```

## Executed probes

| What was run | Result |
|---|---|
| `FINDING_ID_RE` at `ffd1d05` and at `a283e64` against `"!" * n + "x"` | old `n=20` 0.042883 s · `n=22` 0.171534 s · `n=24` 0.695899 s · `n=26` 2.836958 s · `n=28` 11.392153 s; new 0.000006–0.000009 s at every one, 0.000141 s at 4000, 0.003217 s at 100000 |
| Both patterns over 6305 record cells from 149 committed records, 1463 constructed shapes, and an exhaustive marker-prefix sweep | **0 disagreements** over 7768 strings, on acceptance and on the captured id |
| `runner_reached` at `ffd1d05` and at `a283e64` over 3052 top-level defs in 114 tracked `.py` files at `a283e64` | **0 verdicts move** |
| Thirteen built placements through both predicates | 5 move: the three round 1 opened, plus `src/conftest.py#a_nested_fixture` and `a/b/conftest.py#deep_fixture` — finding 1 |
| `collected` mutated to `base.startswith(TEST_PREFIX)`, `tests/__pycache__` cleared | `1 failed, 12 passed` · `test_the_second_python_files_pattern_collects_too` alone, exit 1 |
| `collected` mutated to `base.endswith(TEST_SUFFIX)`, `tests/__pycache__` cleared | `1 failed, 12 passed` · `test_a_pytest_test_function_reads_pytest_only` alone, exit 1 |
| `git status --porcelain` after both mutations were restored | empty |
| `bin/test tests/test_a_runner_reached_unit_reads_pytest_only.py tests/test_a_finding_id_is_a_bare_integer.py tests/test_no_real_identifiers.py tests/test_a_rider_reaches_its_file.py tests/test_the_reopening_is_one.py -q` | `87 passed, 1 skipped in 33.14s`, exit **0** |
| `OLD_COORD_RE` against `"a." + "b/" * n` | len 502 0.0315 s · 1002 0.2521 s · 2002 1.9545 s · 4002 15.7004 s — eight times the work per doubling, cubic |
| `OLD_COORD_RE` over all 1520 lines of `seal/ledger.md` and the `seal/ledger/*.md` fragments | slowest **0.000537 s**, `seal/ledger.md:1356`, 8831 characters; the 19 rows of 1150–1280 characters top out at 0.000172 s |
| The five compiled patterns in `hooks/review-history-guard.py` against adversarial input at four lengths | linear, 0.00006 s or less at 6424 characters |
| Independent scan of the 30 shipped scripts for a repetition nested in a repetition | 47 plain literals found against the record's 61; concatenated patterns are outside this scanner, so the count of 4 is neither confirmed nor contradicted |
| Top-level def counts per SHA | `ffd1d05` 3003 · `824bfca` 3051 · `4dfde1d` 3052 · `f8180f4` 3052 · `a283e64` 3052 |
| `measure` and `call_sites` over `29e0460..f8180f4` and over `ffd1d05..a283e64` | branch-only: 0 contract changes, 9 new units. Whole range: 2 contract changes, both `seal.py` units the merge brought, and 69 new units |
| `git merge-base --is-ancestor 00e63c3 …` against `HEAD`, `origin/release/v0.9.1`, `origin/main` | 0, 0, 1 — a release-branch commit the squash keeps, absent from `main` |
| `evidence_check.content_hash` over the two riders' anchored regions | `floor_record` at lines 179–181 hashes to bba5c7a1; `OLD_COORD_RE` at lines 91–94 hashes to 1ca5aff0 |
| `grep -rn` for the operator's home directory across the worktree | one hit, the untracked `.git` worktree pointer; no tracked file carries one |
| `bin/evidence-check` | `809 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit **0** |
| `bin/deferral-check` | resolves, exit **0** |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1, finding 5's grounds | `tests/test_the_reopening_is_one.py:164` | The one unit in this repository reading `no call site found` for a reason pytest's collection rules do not explain. Carried rather than re-enumerated: the staleness check is that no verdict in the tree moves under the repaired predicate, and it does not |
| round 1, probe 5 | `skills/code-review/scripts/round_record.py:2029` | The corpus measurement that chose refusal over accepting a round prefix — 130 records, 82 either, 46 refused, 2 mis-keyed. Round 1 executed it and this round's equivalence sweep re-covers the same cells |
| round 1, findings 4 and 5 | `tests/test_a_new_returnable_value_is_a_contract_change.py:52`, `seal/follow-up.md:44` | Both closed by `f8180f4`; the ledger fragment R3 and `phases/phase-3.md` now name which half of the cross-check is independent, and the follow-up section is empty |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `OLD_COORD_RE`'s cubic path half — repairing it changes which paths a coordinate may name, and 805 ledger rows depend on that | a `# RIDER:` at the pattern with its measurement, `skills/evidence-check/scripts/evidence_check.py:77` — already deferred by the fix pass; finding 4 corrects the measurement inside it, not the judgment | the repository owner |
| Whether a reach walk should follow a callable passed as a value at all | a `# RIDER:` at `tests/test_the_reopening_is_one.py:164` — already deferred; finding 2 is about the rider being unwatched, not about reopening the decision | the repository owner |
| Whether `Contract changes` wants the narrowing to non-string literals | `questions.md` Q3 — already deferred, carrying round 1's measurement of one added entry across three real ranges | the repository owner |
| Whether the two committed records that miscount their finding ids are corrected in place | `overview.md` §*Not verified* — already deferred; nothing is blocked | the repository owner |
| Which of `fix/239-a-stamp-names-content-not-a-commit` and this branch rewrites the other's two rider stamps, since both touch the convention on the same release | named here, with the anchor each rider should carry | the orchestrator |
| The full suite, the repository-wide lint and the typecheck | `skills/agent-contract/SKILL.md` §2 — the broad gate is one run after the rounds settle | the orchestrator |

## For the record

Needs a fix: yes — 1 and 2
Loses a record or crashes: no
Contract changes: none from this branch's own commits (`29e0460..f8180f4`). Over the full `ffd1d05..a283e64` range the generator reports two, `skills/implement/scripts/seal.py#git` and `skills/implement/scripts/seal.py#manifest_of`, and both are the merge of `release/v0.9.1` rather than this branch's work
New units: `TEST_SUFFIX (depth 1)`, `collected (depth 1)`, `test_a_long_punctuation_cell_is_refused_without_hanging (depth 1)`, `HELPERS (depth 1)`, `SUFFIX_MOD (depth 1)`, `ROOT_CONFTEST (depth 1)`, `test_a_conftest_at_the_repository_root_is_still_a_conftest (depth 1)`, `test_a_test_shaped_def_in_an_uncollected_module_is_not_the_runners (depth 1)`, `test_the_second_python_files_pattern_collects_too (depth 1)` — nine, from `29e0460..f8180f4`. The full range adds 60 more, every one of them the merge's

## Proof

Files opened in this worktree:

- `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/rounds/round-1.md`
- `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/rounds/round-1-fixes.md`
- `seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/routing.md`
- `seal/ledger/1788817290-the-derivation-misreads-and-the-record-refuses-the-id.md`
- `seal/ledger.md`
- `seal/follow-up.md`
- `seal/config.md`
- `skills/code-review/scripts/round_record.py`
- `skills/evidence-check/scripts/evidence_check.py`
- `docs/review-chain-spec.md`
- `tests/test_a_runner_reached_unit_reads_pytest_only.py`
- `tests/test_a_finding_id_is_a_bare_integer.py`
- `tests/test_a_rider_reaches_its_file.py`
- `tests/test_the_reopening_is_one.py`
- `tests/test_the_records_can_be_carried_out_and_in.py`
- `tests/test_the_root_migrates_itself.py`
- `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`
- `tests/test_a_record_states_what_the_tree_has.py`
- `hooks/review-history-guard.py`
- `bin/test`
- `CONTRIBUTING.md`

Commits read in full: `a77ef92`, `824bfca`, `4dfde1d`, `f8180f4`, `2138c98`.

Nothing in the prompt asked for a check `skills/agent-contract/SKILL.md` §2
excludes, so there is no declined instruction to name.
