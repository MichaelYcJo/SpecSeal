# 1788826000-a-stamp-names-content-not-a-commit — review round 1

| Field | Value |
|---|---|
| Target SHA | 404dd4d |
| Ran by | warden on claude-opus-5 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | content_at → migrate, round-1-report.md, round-1.md, content_at, pytest |
| New units | HTML_MARK (depth 1); test_a_second_rider_directly_under_the_first_is_its_own_rider (depth 1); test_a_second_rider_sharing_one_html_comment_is_its_own_rider (depth 1); stamped_module (depth 1); test_reverify_does_not_move_a_date_whose_hash_did_not_move (depth 1); test_reverify_still_moves_the_date_of_a_rider_that_did_change (depth 1); test_the_drift_message_says_the_re_stamp_takes_a_file (depth 1); test_a_refusal_names_which_of_the_three_things_failed (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4; 5 and 6 are fix or justify |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of `1788826000-a-stamp-names-content-not-a-commit` (ticket #239), at target `404dd4d`, base `origin/release/v0.9.1`. No prior rounds, and no pull request open — the orchestrator opens it after this round.

The owner moved this into 0.9.1 mid-run and put it first, because it has been costing a cycle rather than an incident: `# RIDER:` comments carried `Verified <date> at <sha>`, a fix pass works on a feature branch, a feature branch squashes into its release branch by rule, and the squash destroys exactly the commits a fix pass has to name — so the check fails on the release branch, where whoever repairs it is never whoever caused it, and it needs no mistake at all. `0946350` is a commit whose whole job was re-pointing three stamps after a rewrite, the release-to-`main` direction cost a patch release, and `release/v0.9.1` went red again the moment #226 merged.

The direction was not open. `skills/evidence-check/SKILL.md` already cites the riders' orphaned SHAs as one of four grounds for deriving a ledger anchor from content, and `CLAUDE.md` states the rule that came out of it. This branch is the migration that decision never got, so what the round was to judge is where the analogy stops holding, not whether to make it.

What was built: a stamp now reads `Verified <date> against <anchor>@<hash>` in the ledger's anchor vocabulary, resolved inside the rider's own file, with the ledger's `path` component dropped because a rider IS the coordinate. The self-reference problem was measured before it was designed against — 12 of 19 riders sit inside the AST span of the unit they describe — and the answer is to strip EVERY rider block from a region before hashing it. Degradation is DRIFTED-not-BROKEN but treated as a failure, on the grounds that a drifted rider is the rider firing. `Target SHA` stays, on a measured rather than inferred ground: `chain_check.py#reachable` falls back to a pull-head namespace the squash does not touch, while the rider check had `git merge-base --is-ancestor` and no fallback, so the two were never the same mechanism. And the corpus count in the handoff was wrong — 14 files and 19 riders plus one quoted inside a round record, with `RIDER_ROOTS` scanning four roots where the tree has riders in six, so two riders were unchecked entirely and one carried no stamp in any form.

The named targets: the exclusion rule as the load-bearing piece, with the two stated losses to be tested for completeness by constructing a change a reviewer would want caught that the exclusion swallows; the self-reference fixed point, verified directly in both directions; two riders in one unit, since the build reported its own case for this was verifying nothing until it asserted its fixture had two blocks; the `Target SHA` decision, with the pull-head fallback re-derived rather than read; the twelve preserved dates, sampled, and the seven refusals checked for defensibility; a test seen red against the unmigrated corpus; whether the rewritten CI message leaves its requirement honestly stated when the case it now rests on skips; and whether the build's own mid-run `git checkout` accident lost anything.

The report was to be written to a file, finding ids bare integers, every verdict row carrying one, no finding carrying two rows, and no commit SHA in any rider stamp.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 Twelve stamps assert a 2026-09-08 reading that did not happen; the records claim the twelve original dates were preserved | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` · `seal/ledger/1788826000-a-stamp-names-content-not-a-commit.md` row S4 | **fixed** `eaa8030` | fixed at eaa8030 — `` — the twelve dates restored, each proved against the commit its pre-migration stamp named; `bdf65df` is the writer that erased them; **executed** — `--migrate` in a fresh clone at `cbdd66e` writes 2026-08-31 / 09-02 / 09-06 / 09-07 for eleven riders; the twelfth region hashes to `8e0a246a` at both `4581fe1` and HEAD, so it keeps 2026-09-06. Every stamp at `4bf8dcb` and at HEAD reads 2026-09-08 |
| 2 | 🔴 `reverify` rewrites a stamp whose region hash is unchanged, and `--only` takes a file so it re-dates every rider in it | `.github/scripts/rider_check.py:421` · message at `:344` | **fixed** `bdf65df` | fixed at bdf65df — `` — `--reverify` skips on the hash alone, and the drift message says `--only` takes a file; **executed** — `--reverify --only hooks/worktree-guard.py` restamped three riders with three unchanged hashes and moved three dates |
| 3 | 🟡 A date-only re-stamp drifts the evidence ledger row for a unit nobody edited, against `phase-4.md`'s steady-state claim | `.github/scripts/rider_check.py:421` · `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-4.md` | **fixed** `bdf65df` | fixed at bdf65df — `` — the same change; a hash that has not moved is no longer re-stamped, so no ledger row drifts for a unit nobody edited. `phase-4.md`'s steady-state paragraph corrected in `e1b83b8`; **executed** — one date digit changed in `hooks/dispatch.py` gives `rider_check` 20 ok exit 0 and `evidence_check` `DRIFTED hooks/dispatch.py#run_gate` exit 1 |
| 4 | 🔴 Two riders written back-to-back merge into one block; the second one's stamp is never resolved, compared, or reported as missing | `.github/scripts/rider_check.py:197` and `:218` | **fixed** `bdf65df` | fixed at bdf65df — `` for the `#` form, `923f86c` for the HTML form and the opener that was looser than its own docstring; **executed** — a fixture whose second rider carries `deadbeef` reports `1 ok · 0 drifted · 0 broken`; `all_riders` returns one rider and reads one stamp |
| 5 | 🟡 Three hand-written anchors are quoted sentences, so a reword reports BROKEN rather than DRIFTED — and `skills/implement/SKILL.md`'s rider asks for exactly that reword | `agents/smith.md:60` · `skills/implement/SKILL.md:379` · `templates/evidence-check.yml:5` | **fixed** `eaa8030` | fixed at eaa8030 — `` — `agents/smith.md` and `skills/implement/SKILL.md` re-anchored to their headings. `templates/evidence-check.yml` answered rather than changed: see below; **executed** — one word changed in each anchored line gives `BROKEN … the anchor resolves to nothing in this file`, exit 2. `evidence_check.resolve_unit`'s docstring and `CLAUDE.md` both state the rule this breaks |
| 6 | 🟡 The migration's headline refusal says git cannot resolve `881fb0f`; git resolves it, and the file simply did not exist at that path | `.github/scripts/rider_check.py:359` and `:504` · `phases/phase-4.md` · ledger row S4 | **fixed** `bdf65df` | fixed at bdf65df — `` for `content_at`, `e1b83b8` for `phase-4.md`'s bullet and ledger row S4; **executed** — `git cat-file -t 881fb0f` → commit, ancestor of HEAD, 2026-09-02; `git show 881fb0f:./.github/scripts/fold_ledger.py` → *path exists on disk, but not in '881fb0f'* |
| 7 | ⬜ The disclosure says the old stamp string survives in one record; it survives in two | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/questions.md:28` · `overview.md:36` | **fixed** `e1b83b8` | fixed at e1b83b8 — `` — `questions.md` C1 and `overview.md` both say two, and name the second; **executed** — `grep -rn "Verified [0-9-]* at [0-9a-f]"` also hits `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96` |
| 8 | ⬜ Phase 3's removes table names two of the four units the phase removed | `seal/specs/1788826000-a-stamp-names-content-not-a-commit/phases/phase-3.md` | **fixed** `e1b83b8` | fixed at e1b83b8 — `` — `phase-3.md` gains the two missing rows, both marked NAME NOT IN TREE; **executed** — an AST comparison of the test file across the range also removes `test_every_rider_carries_the_date_and_sha_it_was_verified_at` and `STAMP`; both have live replacements \|  <!-- NAME NOT IN TREE --> |
| 9 | ❓ out of verified scope — the full suite, the repository-wide lint and the typecheck | whole tree | deferred the orchestrator | the orchestrator |

## Paste-ready fixes

```python
        if digest == rider.new.group("hash"):
            # The content has not moved, so nobody re-read anything. Writing
            # today's date over the recorded one asserts a reading that did
            # not happen, which is the half of a stamp `--migrate` refuses to
            # manufacture and the half `--reverify` was silently rewriting.
            continue
```
```python
                    "`{}` changed since this was verified on {} ({} -> {}). "
                    "Read the rider — that is what it is for — then either do "
                    "what it asks and delete it, or "
                    "`rider_check.py --reverify --only {}` — which re-stamps "
                    "every rider in that file, so read the others in it "
                    "first".format(
```
```
hooks/cmdline.py:1784                                            2026-09-08 -> 2026-08-31
hooks/cmdline.py:1827                                            2026-09-08 -> 2026-08-31
hooks/dispatch.py:94                                             2026-09-08 -> 2026-09-02
hooks/optin.py:57                                                2026-09-08 -> 2026-08-31
hooks/review-history-guard.py:161                                2026-09-08 -> 2026-08-31
hooks/review-skill-gate.py:128                                   2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:173                                      2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:230                                      2026-09-08 -> 2026-08-31
hooks/worktree-guard.py:1494                                     2026-09-08 -> 2026-08-31
skills/code-review/scripts/round_record.py:1870                  2026-09-08 -> 2026-09-06
skills/evidence-check/scripts/evidence_check.py:1802             2026-09-08 -> 2026-09-07
tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:629  2026-09-08 -> 2026-09-06
```
```bash
git clone --no-local . /tmp/rider-dates && git -C /tmp/rider-dates checkout -q cbdd66e
python3 /tmp/rider-dates/.github/scripts/rider_check.py --root /tmp/rider-dates --migrate
# every `migrated` line's date is the date the corresponding stamp must carry
```
```markdown
In steady state it adds no new drift event, but only once `--reverify` stops
rewriting a stamp whose region hash has not moved: until then a date-only
re-stamp drifts the ledger row for a unit nobody edited, and the two checks
disagree — measured, `rider_check` 20 ok and `evidence_check` DRIFTED on
`hooks/dispatch.py#run_gate` from one changed date digit.
```
```python
        elif stripped.startswith("#"):
            j = i
            # A second `RIDER:` inside the run is a second rider, not more of
            # this one. Without this, back-to-back riders merge into one block
            # and only the first stamp is ever resolved -- the same silence as
            # a rider outside `RIDER_ROOTS`, which is what #239 closed.
            while (
                j + 1 < n
                and lines[j + 1].lstrip().startswith("#")
                and MARKER not in lines[j + 1]
            ):
                j += 1
            end = j
```
```python
def test_a_second_rider_directly_under_the_first_is_its_own_rider(tmp_path):
    """Back-to-back riders merged into one comment run, so `all_riders`
    returned one rider, `Rider.new` read the FIRST stamp, and the second
    rider's hash was never resolved. A rider held by nothing is the defect
    #239 closed for `RIDER_ROOTS`; this is the same one inside a block."""
    src = (
        "def unit():\n"
        f"    {MARK} first claim\n"
        "    # Verified 2026-01-01 against unit@00000000\n"
        f"    {MARK} second claim, written straight under the first\n"
        "    # Verified 2026-01-02 against unit@deadbeef\n"
        "    value = 1\n"
        "    return value\n"
    )
    blocks = riders.comment_blocks(src.splitlines())
    assert len(blocks) == 2, f"the two riders merged into one block: {blocks}"
    stamps = [r.new.group("hash") for r in riders.riders_in("m.py", src)]
    assert "deadbeef" in stamps, f"the second rider's stamp was never read: {stamps}"
```
```
     Verified 2026-09-08 against "## <the enclosing heading, verbatim>"@<hash from --reverify>.
```
```
# Verified 2026-09-08 against "name: evidence-check"@<hash from --reverify>.
```
```bash
python3 .github/scripts/rider_check.py --reverify --only skills/implement/SKILL.md
python3 .github/scripts/rider_check.py --reverify --only templates/evidence-check.yml
python3 .github/scripts/rider_check.py --reverify --only agents/smith.md
```
```python
def content_at(root, sha, rel):
    """(the file as the stamped commit held it, why not) — one of them is None.

    Three different things fail here and they are three different repairs: the
    commit is gone, the commit is fine and the path was not in it, or git could
    not be run at all. The refusal used to say the first for all three, and the
    record built on it read a stamp naming a commit that predates its own file
    as the squash orphaning a stamp in the act.
    """
    try:
        run = subprocess.run(
            ["git", "-C", root, "show", f"{sha}:./{rel}"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None, "git could not be run"
    if run.returncode == 0:
        return run.stdout, None
    known = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
    )
    if known.returncode != 0:
        return None, f"git cannot resolve {sha} any more"
    return None, f"{sha} resolves, but {rel} was not in it"
```
```python
        was, why_not = content_at(root, rider.old.group("sha"), rider.rel)
        if was is None:
            refused.append(
                (
                    rider.where(),
                    "{}, so the date cannot be proved. Re-read the rider and "
                    "`--reverify`".format(why_not),
                )
            )
            continue
```
```markdown
- **One names a commit that predates its own file.**
  `.github/scripts/fold_ledger.py` was stamped `881fb0f`, which git resolves
  and which is an ancestor of HEAD — `fold_ledger.py` was simply not in that
  tree. Not the squash orphaning a stamp, which this migration never observed
  in the act; a stamp that was wrong when it was written.
```
```markdown
it is one of the two places the old string survives a `grep`, with
`seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/phases/phase-2.md:96`
```
```markdown
| `test_every_rider_carries_the_date_and_sha_it_was_verified_at` — NAME NOT IN TREE | replaced by `test_every_rider_carries_a_verification_stamp`, in the same file |
| `STAMP` — NAME NOT IN TREE | replaced by `NEW_STAMP` in `.github/scripts/rider_check.py`, which the test file imports rather than restating |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_rider_reaches_its_file.py -q` in a clone at `404dd4d` | `19 passed in 0.35s` |
| `python3 .github/scripts/rider_check.py` in the working tree | `20 ok · 0 drifted · 0 broken`, exit 0 |
| Seven mutations, one at a time, each restored | each turns its named case red; `blocks[:1]` → the second-rider case · exclusion removed → the fixed-point and prose cases · comment-head dropped → the prose/string case · block stopped at `# ` → the blank-comment-line case · one `at <sha>` stamp restored → `test_no_rider_stamp_names_a_commit` · one hash digit changed → the resolve-and-reproduce case · `git status` added to the check path → `test_the_check_asks_git_for_nothing`. Restored: `19 passed` |
| `git clone --no-local` at `cbdd66e`, then `--migrate` | `11 migrated · 8 refused`, exit 1, dates 2026-08-31 / 09-02 / 09-06 / 09-07 preserved. The two extra refusals against this repository are objects a `--no-local` clone does not carry |
| Region hash of `test_the_refusal_above_can_actually_fail` at `4581fe1` and at HEAD | `8e0a246a` both — the twelfth date `--migrate` proves in this repository |
| `--reverify --only hooks/worktree-guard.py` on the migrated clone | `3 restamped · 0 refused`; three unchanged hashes, three dates moved to 2026-09-08 |
| One rider date changed to 2026-09-09, then both checkers | `rider_check` `20 ok`, exit 0 · `evidence_check` `DRIFTED hooks/dispatch.py#run_gate content changed at 54-98`, exit 1 |
| Fixture: two riders back to back, second stamped `deadbeef` | `blocks [(2,5)]` · one rider found · one stamp read · `1 ok · 0 drifted · 0 broken` |
| One word changed in each of the three quoted-line anchors | three `BROKEN … resolves to nothing`, exit 2 |
| Constructed exclusion attacks: guard commented out under a rider · `<!--` on its own line · missing `-->` | drifts · BROKEN *no verification stamp* · BROKEN *entirely rider comment*. None silent |
| `("exported_at", 12345)` added to the parametrize list the twentieth rider names | `DRIFTED tests/test_the_records_can_be_carried_out_and_in.py:1415`, exit 1 |
| `bin/test tests/test_the_reopening_is_one.py -q -rs` | `35 passed, 1 skipped` — `SKIPPED … origin/release/v0.8.1 is not fetched here` |
| `bin/test tests/test_ci_gives_the_checks_what_they_need.py -q` | `2 passed` |
| `bin/evidence-check` on the working tree | `total: 815 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `git for-each-ref 'refs/pull/*/head'` and `'refs/remotes/pull/*/head'` | `0` and `86` |
| `chain_check.reachable` over every round record's `Target SHA` | 120 SHAs parsed; 117 are not ancestors of HEAD, and 116 of those resolve through `refs/remotes/pull/<N>/head`. The one that does not (`bc94eb1`) is still carried by `origin/fix/111-a-git-call-that-fails-reads-as-no-remote`, which `reachable` is given as a declared ref |
| `grep -c '^\| Target SHA \|'` over `seal/specs/**/round-*.md` | 135 rows in 135 files |
| `git merge-base --is-ancestor 29e0460 404dd4d`, and every branch-touched file against `29e0460` | not an ancestor; no file identical to its `29e0460` version |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `templates/sdd-round.md` and five other places name `refs/pull/<N>/head`, and `chain_check.py:617` scans `refs/remotes/pull/`. Executed: `git for-each-ref 'refs/pull/*/head'` returns 0 refs here and `refs/remotes/pull/*/head` returns 86. The exemption's first ground still holds — 117 of 120 squashed target SHAs resolve through the fallback — but a reader who runs the namespace the template names gets nothing and reads the ground as false. `tests/test_a_rider_reaches_its_file.py:116` pins the wrong string. The same six documents also carry it: `spec.md` §Question 2, `questions.md` A2, `phases/phase-1.md`, `changelog.md`, ledger row S5 | the pull request; it is one word in five documents and one assertion, and it is not a defect in the migration | the repository owner |
| Whether the mid-run `git checkout 29e0460 -- .` lost any uncommitted work. The committed tree carries no trace of it, but no record of the incident exists in `spec.md`, `plan.md`, `overview.md` or any phase record, so there is nothing to compare a claim against | `overview.md`'s *Where spec and implementation diverged*, which is where the other mid-run corrections are recorded | the implementing session |
| Whether a drifted rider is answered often enough to be worth its noise | `seal/follow-up.md`, which already states the trade as overturnable | the repository owner (carried from `overview.md`, unchanged) |
| `templates/evidence-check.yml`'s rider is half spent — the quoted phrase *"let drift warn without blocking"* no longer exists in the file | the repository owner, per `overview.md` | the repository owner (carried, unchanged) |
