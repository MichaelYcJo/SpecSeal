# 1789919879-the-outside-contributor-has-no-procedure — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `c0b00d08` |
| Base | `origin/release/v0.12.1` (`b7629edb`) |
| Reviewed in | a `git clone --no-local` of the repository at the target SHA |
| Reviewed by | warden on claude-opus-5[1m] |

This is a finding round, not a verifying one: there is no earlier
`round-N.md` under this work item, so nothing was inherited and every verdict
below is re-derived from the code.

## What the account claimed, and what the code said

The handoff carried the smith's narrow runs as claims. Two of them were
opened and one of them is false.

| Claimed | Found |
|---|---|
| `evidence-check` exit 0, `1368 ok · 0 drifted · 0 broken` | **Executed at `c0b00d08`: exit 2.** The anchor arm is clean — `1368 ok · 0 drifted · 0 broken` — and the record arm refuses three lines, `3 refused`. Finding 1 |
| `survivor-check --range origin/release/v0.12.1...HEAD` exit 0 | Executed: exit 0, 1106 files examined against 6 removed sentences |
| `unverified-check --baseline origin/release/v0.12.1` exit 0, 3 open rows | Executed: exit 0, the three rows are this work item's |
| The rewritten guard pin goes red on all three mutations | Executed, each mutation alone and restored from bytes: all three red, and the `exit 1` mutation red on its own case. Finding-free |
| The two corrected frame coordinates resolve | Confirmed. `body_from` is in `.github/scripts/issue_claims_check.py` and its docstring states both halves of the claim; `running_the_checks()` is at `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:670` and reads one `CONTRIBUTING.md` section to the next heading. The name the frame used, read_body, is in no source file — written bare here for the reason finding 1 is about |
| The three re-verified `seal/ledger.md` rows still hold | Confirmed by reading each claim against the edited unit. The `bin/` row is about the step's shipping-root **pattern**, which phase 2 did not touch; the two `COVERED` rows are about eleven modules and two documented prose maxima, and a new list entry changes neither. Re-verify was the right arm, not removal |

The prompt's own facts were opened the same way: the workflow re-parses (13
steps), and the refusal renders (finding-free, probe below).

## Findings

### 🔴 1 · `evidence-check` exits 2 at the reviewed SHA, so the pull request's `ledger` job goes red

**Location** — `seal/specs/1789919879-the-outside-contributor-has-no-procedure/overview.md:19`,
`seal/specs/1789919879-the-outside-contributor-has-no-procedure/phases/phase-5.md:69`,
`seal/specs/1789919879-the-outside-contributor-has-no-procedure/phases/phase-5.md:114`.

Phase 5 corrected the frame's wrong coordinate in `spec.md` by writing the
retired name **bare**, because the record checker reads backticked names. The
records that document that correction then wrote the same name back in
backticks, three times. Executed at `c0b00d08`:

```
records — what unreleased work items state about the tree
  NOT-IN-TREE  …/overview.md:19       `read_body` — nothing outside seal/specs
                                      and seal/ledger carries this name.
  NOT-IN-TREE  …/phases/phase-5.md:69
  NOT-IN-TREE  …/phases/phase-5.md:114
  4 work items read · 88 unread · 698 names read · 3 stamps read · 3 refused
exit 2
```

**Why it matters, and why it is not paperwork.** `.github/workflows/test.yml`'s
`ledger` job reads the exit code and exits with it when it is 2 or more. So
this is not a note in a record — it is a red check on the pull request this
branch is about to open, on the branch whose whole subject is what CI asks a
contributor for.

It is also the `written_late` shape: phase 5's own Executed table records
`evidence_check.py` (after) as **exit 0 · 0 refused**, and that was true when
it was run. Two of the three refused lines are in the commit that wrote that
table, and the third arrived with it. The record is honest about a tree that
stopped existing one commit later.

### 🟡 2 · A1 is not met, and the divergence is recorded nowhere

**Location** — `seal/specs/…/spec.md` §*User scenarios & acceptance*, row A1,
against `.github/workflows/hygiene.yml:96`.

A1 requires the refusal to say the base branch may be the cause "**before it
says anything about `plugin.json`**". The message ships the opposite order —
`plugin.json` in its first clause — and
`tests/test_the_release_check_watches_what_ships.py::test_the_refusal_still_serves_the_release_and_puts_it_first`
asserts that order as a requirement.

The order is right and the reasoning is sound: `plan.md` §*The design
constraint the message has to satisfy* puts the release case first because
that is the reader the old text already served, and `phases/phase-2.md`
records the decision. What is missing is that nobody noticed the two
documents disagree. `overview.md`'s divergence table carries three rows and
not this one, so a reader checking the branch against its own acceptance
criteria finds an unmet one with no answer beside it.

### 🟡 3 · The exemption list's own reason is false for three of its seven rows

**Location** — `CONTRIBUTING.md`, §*What a contribution is not asked for*,
the sentence "The steps that would demand any of it belong to a release, and
each one exits early on any other base."

Read against each step: the version step, the changelog step and the ledger-fold
step do guard on `base_ref != main`. The other three that the table names do
not.

| Row | The step | Base guard? |
|---|---|---|
| a review round record | *a declared review chain has the round record it claimed* | **none** — it runs on every pull request and passes because no committed declaration names the contributor's branch (`chain_check.py#declared_for_this_branch` keys on `GITHUB_HEAD_REF`) |
| an `overview.md`, or a row inside one | *the unverified record is readable* | **none** — it compares row counts against the baseline |
| an issue number in the description | the issue-claim step | **none** — `body_from` returns the empty body and `main()` returns 0 |

Each row's own cell gives the right reason. The sentence above them
generalises past them, and it is the sentence a maintainer adding a CI step
would read to decide whether the list still holds — which is exactly the
six-month rot `plan.md` predicts.

### 🟡 4 · The ledger job is a second check that can ask a contributor for something they do not have

**Location** — `CONTRIBUTING.md`, §*The one check that can ask you for
something you do not have*, and the exemption table's `seal/ledger/` row.

The table row says the `ledger` job "runs the lenient reader, where drift is a
warning and never a failure". True for drift. It is silent about BROKEN, and
`.github/workflows/test.yml` exits with the code when it is 2 or more.

**Executed.** In the review clone, renaming one heading that a `seal/ledger.md`
row anchors — `## Comparison axes` in `skills/code-review/SKILL.md` — takes the
checker from `1368 ok · 0 broken` to `1367 ok · 1 broken`, which is exit 2 and
a red `ledger` job. Restoring the heading restores the count.

That is a documentation edit of exactly the shape #443 was, and the repair is
to remove the row from `seal/ledger.md` and write the new claim into a work
item's own fragment — the convention the section immediately above says a
contribution does not have. The heading calls survivor-check "the one check";
it is not the one.

### 🟡 5 · The staleness guard covers two of the four surfaces that now carry the convention

**Location** — `README.md:639`, `README.ko.md:631`,
`.github/PULL_REQUEST_TEMPLATE.md:3`, against
`tests/test_the_contributor_has_a_procedure.py:70` and
`tests/test_the_release_check_watches_what_ships.py:203`.

Q1's whole grounds are that a concrete version in a contributor-facing
document is a fact that expires on a schedule, and phase 1 pinned it "in both
directions". Two cases refuse a concrete `release/v\d+\.\d+\.\d+`: one over
`CONTRIBUTING.md` §*Opening a pull request*, one over the refusal line. The
branch put the same convention on three more surfaces and nothing refuses a
concrete branch there. Grepped: those are the only two guards in `tests/`.

The pull request template is the surface most exposed — it is pre-filled into
every pull request, a maintainer reads it weekly, and "helpfully" replacing
`release/vX.Y.Z` with today's branch is the single edit Q1 exists to stop.
`agent-contract` §12: the defect is the class, not the coordinate.

`spec.md` S5 budgets two pins and both are spent, so this is a scope decision
the owner may keep — but the cost of keeping it is that the guard protects the
document a contributor reads second and not the box they read first.

### 🟡 6 · "CI will refuse a contribution aimed at `main`" is unconditional, and the step is not

**Location** — `.github/PULL_REQUEST_TEMPLATE.md:8`, `README.md:641`,
`README.ko.md:634`.

The template says "CI will refuse a contribution aimed there for leaving
`.claude-plugin/plugin.json` alone", and `README.md` says "A contribution
aimed at `main` is refused by CI for leaving the version alone". The step
refuses only when something under a shipping root changed — `if [ -z "$ships" ];
then echo "nothing that ships changed"; exit 0; fi`, at
`.github/workflows/hygiene.yml:80`.

#443 touched `skills/evidence-check/SKILL.md`, which ships. A contribution
that touches only `docs/`, `tests/` or `.github/` and is based on `main` gets
a green hygiene run — and the reader of these two sentences has just been
taught that the gate is what catches a wrong base. The instruction above them
is unconditional and correct; only the rationale overreaches.

`CONTRIBUTING.md`'s own version of this paragraph does not have the problem:
it explains the refusal the contributor already met rather than promising one.

### ⬜ 7 · The guard pin reads `fi` by exact equality

**Location** — `tests/test_the_release_check_watches_what_ships.py:271`.

`first(lambda line: line == "fi")` matches the stripped line exactly, so `fi
# …` would read as "the guard never closes". The direction is safe — a false
red, not a false green — and the case is otherwise the right shape. Noted, not
asked for.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `evidence-check` exits 2 at the reviewed SHA: three backticked occurrences of the retired name read_body (bare here for that same reason) refused by the record arm, so CI's `ledger` job goes red | `seal/specs/1789919879-…/overview.md:19`, `…/phases/phase-5.md:69`, `…/phases/phase-5.md:114` | open | Executed at `c0b00d08` in a clone: exit 2, `3 refused`. `.github/workflows/test.yml` exits with the code when it is ≥ 2. The name is written bare here for the same reason |
| 2 | 🟡 A1 requires the base-branch case before `plugin.json` and the message ships the opposite order; the divergence is in no record | `seal/specs/1789919879-…/spec.md` §A1 vs `.github/workflows/hygiene.yml:96` | open | Read. `plan.md` §*The design constraint* and `phases/phase-2.md` decide the order deliberately; `overview.md`'s divergence table carries three rows and not this one |
| 3 | 🟡 "each one exits early on any other base" is false for the round-record, unverified-record and issue-claim steps, which the same table names | `CONTRIBUTING.md` §*What a contribution is not asked for* | open | Read: none of those three steps carries a `base_ref != main` guard in `.github/workflows/hygiene.yml`. The table's own cells give the right reasons |
| 4 | 🟡 A BROKEN ledger anchor takes the `ledger` job red, so survivor-check is not "the one check that can ask you for something you do not have" | `CONTRIBUTING.md` §*The one check that can ask you for something you do not have*, and its `seal/ledger/` table row | open | Executed: renaming one anchored heading gives `1367 ok · 1 broken`, exit 2. Restored, counts identical |
| 5 | 🟡 Nothing refuses a concrete `release/v0.12.1` in `README.md`, `README.ko.md` or the pull request template, which now carry the same convention | `README.md:639`, `README.ko.md:631`, `.github/PULL_REQUEST_TEMPLATE.md:3` | open | Executed grep over `tests/`: the two staleness guards are `test_the_contributor_has_a_procedure.py:70` and `test_the_release_check_watches_what_ships.py:203`, and neither reads those three files |
| 6 | 🟡 The template and `README.md` promise CI refuses any contribution based on `main`; the step exits 0 when nothing under a shipping root changed | `.github/PULL_REQUEST_TEMPLATE.md:8`, `README.md:641`, `README.ko.md:634` | open | Read `.github/workflows/hygiene.yml:80`, the `-z "$ships"` early return |
| 7 | ⬜ The guard pin matches the closing `fi` by exact equality, so a trailing comment would read as an unclosed guard | `tests/test_the_release_check_watches_what_ships.py:271` | open | Read. Fails safe — a false red |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_release_check_watches_what_ships.py tests/test_the_contributor_has_a_procedure.py tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py -q` at `c0b00d08` | 78 passed |
| `bin/test` over the eight neighbouring modules the phases name (one word one meaning, release hygiene, cheap twice, the set a work item has, a row points by content, untrue milestone, old roots, script reachability) | 306 passed, 7 skipped |
| Guard pin, mutation 1 — the guard's `exit 0` and its `fi` deleted | **1 failed** (red, as claimed) |
| Guard pin, mutation 2 — only the `exit 0` deleted | **1 failed** |
| Guard pin, mutation 3 — the condition replaced by `if false` | **1 failed** |
| `exit 1` after the refusal changed to `exit 0` | **1 failed** on `test_the_refusal_still_fails_the_run` |
| Unmutated, and the workflow restored from bytes after each | 1 passed; the tree came back byte-identical and `git status --porcelain` empty |
| The step rendered as the runner renders it, `${{ github.base_ref }}` substituted to `main`, then `bash -n` and `bash` | `yaml.safe_load` ok, 13 steps; `bash -n` exit 0; the run exits 1 and prints the whole refusal on one line, `$old` expanded, the nested single quotes intact |
| `python3 skills/evidence-check/scripts/evidence_check.py .` at `c0b00d08` | **exit 2** — `1368 ok · 0 drifted · 0 broken` and `3 refused`. Finding 1 |
| The same after renaming one anchored heading in `skills/code-review/SKILL.md` | `1367 ok · 1 broken`; restored, `1368 ok · 0 broken` |
| `python3 skills/code-review/scripts/survivor_check.py --range origin/release/v0.12.1...HEAD` | exit 0 — 1106 files examined, no removed wording still standing |
| `python3 skills/verify/scripts/unverified_check.py --baseline origin/release/v0.12.1 seal/specs/` | exit 0 — the three open rows are this work item's |
| `python3 .github/scripts/claude_block.py --check` | exit 0 |
| `python3 skills/implement/scripts/seal.py mode --check` | exit 0 — row and folder agree |
| Broad gate — the full suite, the repository-wide lint and the typecheck | **not yet.** `agent-contract` §2 leaves all three to the sealer, and this round ran none of them |

Every probe ran in a `git clone --no-local` of the repository at
`c0b00d08`; nothing was written in the working tree, and the clone, its
virtualenv and the three probe scripts are deleted. Probe scripts were named
test_tmp_guard_mutations, test_tmp_ledger_broken_is_red and
test_tmp_render_refusal — written without backticks, since they are not in the
tree.

## Paste-ready fixes

### 1 — the three backticked occurrences of the retired name

Three `Edit` calls. Each substring is unique in its file. The repair is the
one `spec.md:66` already made: write the name bare, because the record checker
reads backticked names.

```
# seal/specs/1789919879-the-outside-contributor-has-no-procedure/overview.md:19
old: `issue_claims_check.py`'s `read_body` as grounds for
new: `issue_claims_check.py`'s read_body (bare, for the reason this row gives) as grounds for

# seal/specs/1789919879-the-outside-contributor-has-no-procedure/phases/phase-5.md:69
old: `spec.md`'s measurement table cites `read_body` as its grounds for
new: `spec.md`'s measurement table cites read_body — bare, because the checker reads backticked names — as its grounds for

# seal/specs/1789919879-the-outside-contributor-has-no-procedure/phases/phase-5.md:114
old: | The frame's `read_body` coordinate in `spec.md` |
new: | The frame's read_body coordinate in `spec.md` (bare here too) |
```

Then, in the same commit, re-run and read the exit code directly:

```bash
python3 skills/evidence-check/scripts/evidence_check.py . >/dev/null 2>&1; echo $?
# expect 0, and `0 refused` in the record arm's own tail line
```

Phase 5's Executed table needs no edit: its `exit 0` row becomes true again.
One clause saying the row was written before the lines that broke it would
keep the next reader from concluding the run was never taken.

### 2 — A1 says what the message does, and the divergence gets a row

```
# seal/specs/1789919879-the-outside-contributor-has-no-procedure/spec.md, row A1
old: **then** the message says the base branch may be the cause and names where a contribution's base belongs — before it says anything about `plugin.json`
new: **then** the message names both causes and asserts neither — the release case first, because that is the reader the old text already served, and the base-branch case second, naming where a contribution's base belongs

# seal/specs/1789919879-the-outside-contributor-has-no-procedure/overview.md,
# a fourth row in §*Where spec and implementation diverged*
| The order of the two causes in the refusal | `spec.md` A1 asked for the base-branch case **before** `plugin.json`; the message ships `plugin.json` first | The release case first | `plan.md` §*The design constraint the message has to satisfy* fixes that order and `phases/phase-2.md` decides it as Q7: the step cannot tell the two readers apart, and the release reader is the one the old text was already right for. A1 was the older sentence and was corrected to match rather than the message being reordered |
```

### 3 — the exemption list's reason stops generalising past its own table

```
# CONTRIBUTING.md, §*What a contribution is not asked for*
old: demand any of it belong to a release, and each one exits early on any
     other base.
new: demand any of it belong to a release and exit early on any base but
     `main`. Three run on every pull request and ask nothing of a branch
     that declared nothing: the round-record check, the unverified-record
     tally, and the issue-claim report. The table says which is which.
```

Wrapped to 88 columns, which `tests/test_docs_line_wrap.py` covers. No case
pins this sentence — `test_the_exemption_list_says_which_guard_makes_it_true`
pins the table's phrase, which does not move.

### 4 — the ledger job joins the section, and the table row stops being half a fact

```
# CONTRIBUTING.md, the `seal/ledger/` row of the exemption table
old: | a row under `seal/ledger/` | the `ledger` job runs the lenient reader, where drift is a warning and never a failure |
new: | a row under `seal/ledger/` | the `ledger` job runs the lenient reader: content drifting under an anchor is a warning. An anchor that stops resolving is not — see below |

# CONTRIBUTING.md, the heading of the section below the table, and a paragraph
# added at its end
old: ### The one check that can ask you for something you do not have
new: ### The two checks that can ask you for something you do not have

# appended to that section, after the `Do not create one.` paragraph:
**The evidence ledger is the other one.** `seal/ledger.md` pins claims to
units of code and prose by name, and the `ledger` job fails when one of
those names stops resolving — a heading you renamed, a function you removed.
Drift under a name that still resolves is only a warning; a name that is
gone is exit 2. The repair is a maintainer's, for the same reason: the row
is removed from `seal/ledger.md` and the new claim written into a work
item's fragment. Say on the pull request which name your change moved, and
leave the ledger alone.
```

Both pinned strings in `test_the_contributor_has_a_procedure.py` —
`survivors.md` and `Do not create one` — survive this edit; run that module to
see it.

### 5 — the staleness guard covers every surface carrying the convention

Seen red first: apply it with `release/vX.Y.Z` replaced by `release/v0.12.1`
in each of the three files in turn, watch the case fail on that file, restore.

```python
# tests/test_the_contributor_has_a_procedure.py, appended


@pytest.mark.parametrize(
    "surface",
    [
        "README.md",
        "README.ko.md",
        os.path.join(".github", "PULL_REQUEST_TEMPLATE.md"),
    ],
)
def test_no_contributor_facing_surface_names_a_concrete_release_branch(surface):
    """Q1 as a class rather than as the one instance it was found on.

    Four surfaces carry the release-branch convention after this work item
    and two were pinned. A concrete branch is deleted after its release, so
    the sentence expires on a schedule wherever it is written — and the
    template is the surface a maintainer reads on every pull request, which
    is where "helpfully" writing today's number is most likely.
    """
    text = read(os.path.join(ROOT, surface))
    assert "release/vX.Y.Z" in text, (
        f"{surface} no longer names the release-branch convention at all, so "
        "a contributor reading it has no rule to apply after the next release"
    )
    stale = re.findall(r"release/v\d+\.\d+\.\d+", text)
    assert not stale, (
        f"{surface} names {sorted(set(stale))} — a concrete release branch is "
        "deleted after its release. Name the convention instead"
    )
```

### 6 — the rationale stops promising a refusal the step does not always give

```
# .github/PULL_REQUEST_TEMPLATE.md
old: A pull request into `main` is a release here, so CI will refuse a
     contribution aimed there for leaving `.claude-plugin/plugin.json` alone. The
     base is the cause, not the version — change the base rather than that file.
new: A pull request into `main` is a release here. If yours touches what the
     plugin ships, CI refuses it for leaving `.claude-plugin/plugin.json`
     alone; if it does not, nothing catches the wrong base at all. Either
     way the base is the cause, not the version — change the base rather
     than that file.

# README.md, §Contributing
old: contribution aimed at `main` is refused by CI for leaving the version alone,
     and the base is the cause rather than the version.
new: contribution aimed at `main` that touches what the plugin ships is refused
     by CI for leaving the version alone — and the base is the cause rather
     than the version. One that touches nothing shipped is not refused at
     all, which is why the rule is the branch and not the check.

# README.ko.md, §기여
old: `main` 으로 연 기여는 버전을 올리지 않았다는 이유로 CI 에서 막히는데,
     실제 원인은 버전이 아니라 기준 브랜치입니다.
new: `main` 으로 연 기여가 플러그인이 배포하는 파일을 건드리면, 버전을
     올리지 않았다는 이유로 CI 에서 막힙니다. 실제 원인은 버전이 아니라
     기준 브랜치입니다. 배포되는 파일을 건드리지 않으면 아무 검사도
     걸리지 않으므로, 기준으로 삼아야 할 것은 검사가 아니라 브랜치입니다.
```

All three files are in `tests/test_docs_line_wrap.py`'s `COVERED` at 88
display columns, Hangul counted double — run that module after the edit.

Needs a fix: yes — finding 1 takes the pull request's `ledger` job red at the
reviewed SHA, and findings 2 through 6 are each a document or a case this
work item's own standard asks for.

Loses a record or crashes: no.

## Proof block

📋 code-review applied
· read: `seal/specs/1789919879-…/{routing,questions,overview,spec,plan,changelog}.md`
  and `phases/phase-1.md` … `phase-5.md`; `seal/ledger/1789919879-….md`;
  `.github/workflows/hygiene.yml`, `.github/workflows/test.yml`,
  `.github/PULL_REQUEST_TEMPLATE.md`; `CONTRIBUTING.md`, `README.md`,
  `README.ko.md`, `seal/ledger.md` (the three re-stamped rows);
  `tests/test_the_contributor_has_a_procedure.py`,
  `tests/test_the_release_check_watches_what_ships.py`,
  `tests/test_docs_line_wrap.py`,
  `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`;
  `.github/scripts/issue_claims_check.py`,
  `skills/evidence-check/scripts/evidence_check.py`,
  `skills/code-review/scripts/chain_check.py`,
  `skills/code-review/scripts/survivor_check.py`;
  `docs/review-chain-spec.md` §*The last round verifies*
· executed: the fifteen rows of §*Executed probes* above, all in a
  `git clone --no-local` at `c0b00d08`
· unverified: the full suite, the repository-wide lint and the typecheck —
  the sealer answers, after the rounds settle. Whether the refusal reads
  well in GitHub's rendered error panel — `overview.md` names the answerer
  and this round did not widen it
