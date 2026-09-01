# 1788229400-every-branch-appends-to-the-same-two-files — review round 2

| Field | Value |
|---|---|
| Target SHA | `d279efacd37c02af69840fdee7c8ffaf392d0b84` |
| Diff base | `origin/main` (`708e348`) |
| PR | not yet |
| Broad gate | not yet |
| Fixes checked by | `round-3` |
| Needs a fix | yes — three 🔴 and seven 🟡 |

- [ ] Pass

## Round 1's ten findings are closed

Each was re-derived rather than inherited. `b1291b1` carries the code fixes,
`aacae56` the documents and cases, `aab921b` and `d279efa` the ledger rows the
fixes drifted.

| Round 1 | Verdict | Grounds |
|---|---|---|
| 🔴 1 | **fixed** `aacae56` | `grep -c 'git blame'` over the four documents returns 0 · 0 · 0 · 1, and the one left (`skills/implement/SKILL.md:87`) describes blame anchoring a line rather than sourcing the baseline |
| 🔴 2 | **fixed** `aacae56` | `BASELINE_DOCUMENTS` at `tests/…:642-649` holds all six; `README.ko.md` has its own case at `:685`. What the same commit removed is finding 10 below |
| 🔴 3 | **fixed** `b1291b1` | Mutation: reverting `evidence_check.py:379` to `first_appearance(root, rel, …)` turns `test_a_renamed_ledger_still_catches_drift` red |
| 🔴 4 | **fixed** `b1291b1` | Mutation: restoring `("OK", …)` at `:507` turns three cases red across two files |
| 🟡 5 | **fixed** `b1291b1` · `aacae56` | `row_stamps` at `:281-308`; the NUL filler holds because `STAMP_RE`'s `\s+` does not match `\x00`. What the second half introduced is findings 4 and 5 |
| 🟡 6 | **fixed** `b1291b1` | `header_of('.specseal/map.md')` returns 3732 characters, cut at the first citing row, against 2000 capped before. What it opened is findings 8 and 9 |
| 🔴 7 | **fixed** `aacae56` | `grep -rn '## Unreleased'` returns nothing from `agents/smith.md`, `skills/implement/SKILL.md` or `CHANGELOG.md`, and `tests/test_release_hygiene.py:183` now forbids it |
| 🟡 8 | **fixed** `aacae56` | `CONTRIBUTING.md:68-79` carries the gather command and its reasoning |
| 🟡 9 | **fixed** `aacae56` | The `sys.exit(0)` stub took 3 cases before and takes 0 now; a `--check` that finds no fragments kills two more than the pre-fix file did |
| 🟡 10 | **fixed** `aacae56` | `.specseal/follow-up.md:39-40` has no empty row and the fragment's duplicated paragraph is gone |

## What the fixes introduced

```
① the branch had to edit `.specseal/map.md`, and three documents were rewritten to let it
     ├─ the stamp is a branch commit, and its test was not changed    [1] 🔴
     ├─ the paragraph licensing it is wrong about the code            [2] 🔴
     └─ the rule it broke still names no way out                      [3] 🟡

② the two new verdicts do less than the scheme they replaced
     ├─ AMBIGUOUS swallows a real DRIFTED and exits 0                 [4] 🔴
     ├─ one commit at two abbreviations is a false AMBIGUOUS          [5] 🟡
     ├─ every mapped coordinate is UNMEASURED, fatal under --strict   [6] 🟡
     └─ the script's own --help and the shipped workflow disagree     [7] 🟡

③ what the header fix opened, and what nothing guards
     ├─ a prose SHA anywhere in a fragment header is now its baseline [8] 🟡
     ├─ 🟡 6's fix has no case at all                                 [9] 🟡
     └─ six documents lost the assertion naming the old rule         [10] 🟡
```

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | After the merge the release branch goes red on a stamp this branch wrote. `aab921b` stamped the re-anchored row at `aacae56`, a commit this feature branch made, and the nine fragment rows carry the same stamp. `tests/test_ledger_stamps_resolve.py` was not changed on this branch and still requires every stamp to be reachable | `.specseal/map.md:109` · `.specseal/map/1788229400-….md:32-40` · `tests/test_ledger_stamps_resolve.py:101-117` | open | Reviewer-executed: a branch cut at `708e348`, `git merge --squash d279efa`, commit, then the case — `AssertionError: .specseal/map.md stamps that no ref can reach: [(109, 'aacae56')]`. This is the incident `CLAUDE.md`'s merge-rule section already describes |
| 🔴 2 | The paragraph written to license that stamp describes behaviour the code does not have. It says the stamp *"resolves for nobody, is ignored, and the row falls back to its first appearance in the squashed history, which is current"*. Both halves are false for a row that already existed — which is the only kind of row a re-verification stamp is written on | `CLAUDE.md:104-108` · `templates/map.md:62-66` · `skills/evidence-check/SKILL.md:118-121` | open | Reviewer-executed on the squashed branch: `first_appearance` for `.specseal/map.md:109` returns `982941227`, the repository's first commit, because it walks past edits to a line on purpose. `evidence_check.py` had 299 lines then and the row cites `517-522`, so `overlaps` is False and the row reads `OK` forever. The drift tripwire is dead |
| 🟡 3 | A branch that moves cited code cannot obey the fragment rule and leave the ledger true. `CONTRIBUTING.md:61-63` forbids editing `.specseal/map.md`; `aacae56` added one exception and it covers `CHANGELOG.md` only. The two documents also disagree on the verb — `CLAUDE.md:119` forbids rows *appended*, which a re-anchor is not | `CONTRIBUTING.md:59-66` · `CLAUDE.md:117-119` | open | Reviewer, read. The implementer's act was right and the rule is what is wrong: `evidence_check.py:202` moved, an existing row cited it, the checker reported DRIFTED, and clearing that needs the coordinate re-anchored in the file the rule forbids touching |
| 🔴 4 | Adding a second stamp to a row turns a real DRIFTED into a passing run. The AMBIGUOUS branch `continue`s before the header fallback, so the row is measured from neither candidate | `skills/evidence-check/scripts/evidence_check.py:483-495` | open | Reviewer-executed in a scratch repository with the cited file genuinely rewritten after the baseline: one stamp gives `DRIFTED … — re-verify`, exit 1; the same row plus a stamp in an earlier cell gives `AMBIGUOUS`, **exit 0**. `.github/workflows/test.yml:85` runs without `--strict`, so nothing in CI turns red. This is the group ② shape round 1 refused to grade down, arriving inside a fix |
| 🟡 5 | The same commit written at two abbreviation lengths reads as two stamps, because `row_stamps` dedups on the matched string rather than on the object. The two agree perfectly and the row's drift check is switched off anyway | `skills/evidence-check/scripts/evidence_check.py:305` | open | Reviewer-executed: `` `23cbd2e` `` and `` `23cbd2e24` `` in one row print `row carries 2 stamps`. This is the ordinary shape of a hand-repaired ledger — PR #49 rewrote stamps across seven rows by hand |
| 🟡 6 | Every cross-repo coordinate now reads UNMEASURED, and `--strict` cannot be cleared. `row_baseline` skips the derivation when `repo != root`, a stamp resolves against the original repo, and the fallback yields `None` unless the header carries a SHA resolvable in the original | `skills/evidence-check/scripts/evidence_check.py:499-507` · `skills/evidence-check/SKILL.md:41` | open | Reviewer-executed on a migration-shaped ledger: `1 ok`/exit 0 before `b1291b1`, `UNMEASURED`/exit 0 now, and **exit 2** under `--strict`. A second header row carrying the original's baseline restores `1 ok` — but `SKILL.md:41` tells the reader to fix UNMEASURED by committing the ledger line, which does nothing here, and no template shows a two-baseline header |
| 🟡 7 | The script's own `--help`, its module docstring and the shipped workflow all still describe four verdicts and a `--strict` that concerns drift alone | `evidence_check.py:7-11` · `:27-29` · `:538` · `skills/evidence-check/SKILL.md:33` · `templates/evidence-check.yml:38-40` | open | Reviewer-executed: `bin/evidence-check --help` prints `--strict  drift also fails`, which `:630-631` contradicts. `templates/evidence-check.yml:40` is the one that ships — a user repo adopting the fragment convention fails its build on an uncommitted fragment row with an exit code its own workflow says cannot happen |
| 🟡 8 | A fragment's prose header is now unbounded, so a SHA anywhere in it becomes the file's baseline. Under the old cap that SHA was outside the window and the fragment correctly reported none | `skills/evidence-check/scripts/evidence_check.py:110-116` | open | Reviewer-executed: a 2600-character prose header with a SHA near character 2500 prints `baseline: e43a98bb4 from header prose`. It matters because the header baseline is the fallback for every row the derivation cannot anchor, so an honest UNMEASURED becomes a measurement against whatever commit a rationale paragraph mentioned. The docstring at `:107-108` also still argues the cap exists to bound the scan, and the new loop scans the whole file first |
| 🟡 9 | Nothing guards 🟡 6's fix | `skills/evidence-check/scripts/evidence_check.py:110-116` | open | Reviewer-executed mutation: `header_of` replaced with the pre-fix cap-first body, then the three ledger test files — **55 passed**. The existing `test_a_baseline_declared_in_the_header_is_still_read:527` uses a short fixture that never reaches the cap |
| 🟡 10 | Six documents lost the assertion naming the rejected reading, to accommodate two that lack it. `aacae56` widened `BASELINE_DOCUMENTS` from three files to six and deleted `assert "last touch" in text` in the same hunk | `tests/test_a_row_measures_from_its_own_history.py:652-659` | open | Reviewer, read: only `templates/sdd-plan.md` and `skills/implement/SKILL.md` lack the phrase; the other four carried it and were passing. The case's own docstring still explains the deleted assertion, and `README.ko.md` is still required to carry `마지막으로 건드린` at `:691` — so the Korean document must name what was rejected and no English one has to. Executed: replacing every `last touch` with `the newest edit` in the three documents that carry it leaves all three document cases green |

## Decided by the repository owner during this round

**🔴 1 and 🔴 2 are one decision, and it is taken.** A row in `.specseal/map.md`
whose coordinate this branch invalidated is **removed there and written afresh
into the branch's own fragment**, rather than re-anchored in place and stamped.

The grounds are the mechanism finding 2 measured. `first_appearance` walks past
edits to a line, so an edited row reaches its original commit; a **new** line's
first appearance is the commit that added it, which after the squash is the
squash commit and is current. The distinction the derivation makes is between
an edited line and a new one, so the fix is to make the row new.

Three things fall out, and all three are wanted:

- No stamp is written, so 🔴 1's failure cannot occur and
  `tests/test_ledger_stamps_resolve.py` needs no change.
- `CLAUDE.md:104-108` and its two copies lose the paragraph finding 2 refuted,
  rather than gaining a corrected one.
- `.specseal/map.md` empties into fragments as work items touch the code its
  rows cite, which is the migration this work item exists to enable.

## Not raised, and why

The `1 ok` → `UNMEASURED` change to `tests/test_evidence_check.py:117` and
`tests/…_own_history.py:213` keeps the property each case was written for. Both
exist to prove **resolution** — that the coordinate is found in the other
checkout rather than reported EXTERNAL or BROKEN — and the new assertions state
that explicitly where `"1 ok"` stated it by implication. Verified by mutation:
restoring `("OK", …)` turns both red. What the change exposes is finding 6.

## Smaller, recorded rather than raised

| Where | What |
|---|---|
| `CLAUDE.md:124` | still says `agents/smith.md` and the implement skill prescribe `## Unreleased`; `aacae56` removed it from both |
| `README.md:140-142` · `README.ko.md:133-135` | neither carries the two new verdicts, nor Q2's `from header prose` line |
| `tests/…_own_history.py:672` | the third blocklist phrase is a superset of the first, so it can never be the assertion that fires |
| `evidence_check.py:206` | `if int(orig)` is dead — blame's original line numbers are 1-based — and the backfill loop is O(rows) to patch the one entry just recorded |
| `evidence_check.py:489` | `row_stamps` is computed twice per row |
| `skills/implement/SKILL.md:87` | calls the header the fallback for rows blame cannot anchor; those rows now read UNMEASURED, and a fragment has no header |

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check .` and `--strict` | `45 ok · 0 drifted · 0 broken · 0 external · 0 unmeasured · 0 ambiguous`, exit 0 both |
| `uvx ruff check .` | passed |
| squash simulation from `708e348`, then `tests/test_ledger_stamps_resolve.py` | 1 failed — 🔴 1 |
| `first_appearance` / `overlaps` for `.specseal/map.md:109` on the squashed branch | `9829412`, no overlap — 🔴 2 |
| two-stamp probe | `DRIFTED`/exit 1 becomes `AMBIGUOUS`/exit 0 — 🔴 4 |
| abbreviation probe | one commit at 7 and 11 characters reads as 2 stamps — 🟡 5 |
| `--default-repo` probe, with and without `--strict` | `UNMEASURED` exit 0 and exit 2; a second header baseline restores `1 ok` — 🟡 6 |
| long-prose-header probe | `baseline: e43a98bb4 from header prose` — 🟡 8 |
| mutation: `header_of` reverted, three ledger test files | 55 passed — 🟡 9 |
| mutation: rename fix reverted | `test_a_renamed_ledger_still_catches_drift` red — round 1's 🔴 3 holds |
| mutation: `UNMEASURED` reverted to `OK` | three cases red — round 1's 🔴 4 holds |
| `bin/evidence-check --help` | `--strict  drift also fails` — 🟡 7 |
| `header_of` on three files | 3732 cut · 2000 capped · 1573 cut — round 1's 🟡 6 holds |

Every probe that commits ran through `subprocess.run(["git", "-C", d, …])` in a
Python script, so no Bash command line carried a commit and nobody was
prompted. Issue #55 is open about the agent files not saying that.

The full suite, `ruff format --check` across the tree and
`gather_changelog.py --check` did not run this round. The broad gate is the
orchestrator's, once, after the rounds settle.

## Round 3 is the last of the cap

It settles one decision, now taken, and one bug. 🔴 1 and 🔴 2 are closed by
removing the row and rewriting it as a fragment row; 🔴 4 is a fix rather than a
judgement, and it is the one place where this branch leaves the checker
reporting less than it did before. 🟡 3 and 🟡 5 through 🟡 10 ride along; none
of them alone would justify a round.
