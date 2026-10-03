# Round 1 report — #647 steps A and B (PR #735)

| Field | Value |
|---|---|
| Round | 1 (no earlier round) |
| Target SHA | 90c3323d |
| Base | 233f0455 (`origin/release/v0.18.0`) |
| Diff | `233f0455..90c3323d`, 58 files |
| Ran by | specseal:warden on claude-opus-5-5 |

The review ran in a scratch clone (`git clone --no-local`) checked out at the
target SHA. Nothing in the worktree was written but this file.

## How the account was read

The account is `overview.md`, `plan.md`, `questions.md` Q1–Q13 and the six
phase records. Each claim below was checked against the code. Where a claim
held, the verdict table says so in a 🟢 row; where it did not, the finding
says what was claimed and what the code does.

- **Claimed** (phase 3, Q11): the blanking class is three readers,
  `old_format_rows`, `malformed_rows` and `migrate`. **Found**: re-derived by
  `git grep` over every non-test `.py` for `ANCHOR_RE`, `OLD_COORD_RE`, every
  `*COORD*_RE`, `COORDINATE_RE`, `SELF_ANCHOR_RE` and the hooks that call the
  three functions. The `.sub` sites are exactly those three, each blanks pact
  anchors first, and `correction_check.py`'s own `ANCHOR`, `settle.py`'s
  `COORDINATE_RE` and `fold_ledger.py`'s `SELF_ANCHOR_RE` cannot match inside
  a pact anchor. **But the class the spec promises is wider than `.sub`
  sites.** Spec item 6 says no reader in a signatory takes a pact anchor for
  something of its own, which "leaves a signatory's own `evidence-check` exit
  status alone". The records arm reads a backticked name inside a pact
  anchor's heading as a claim about the signatory's tree, and exits 2
  (finding 3, executed).
- **Claimed** (spec item 8, docs/the-pact.md): git decides the direction of
  a mismatch and never `OK`. **Found**: true. `grade` decides `OK` from the
  working-tree pact alone (`pact_check.py:303`). **But** HEAD's history is
  read with git's default history simplification, which drops a clause
  version on the side of a merge the merge did not keep (finding 1,
  executed).
- **Claimed** (Q5, plan's alternatives): the pact lists its signatories, "so a
  missing checkout is a finding" and nothing is skipped in silence.
  **Found**: true for a checkout. **Not** true for a table row the walk
  cannot read: a row without its closing pipe, or with a second cell, ends
  the walk and every signatory below it is dropped, exit 0 (finding 2,
  executed).
- **Claimed** (overview, divergence 1): `normalise_remote` moved to
  `hooks/config.py` and `seal.py` keeps an alias, so one normaliser remains.
  **Found**: true. The body is byte-identical to the removed one,
  `seal.py:284` is `normalise_remote = repo_config.normalise_remote`, every
  caller in the tree reaches that one function, and a probe confirmed the
  identity.
- **Claimed** (overview, divergence 2): the config skill must say ten rows.
  **Found**: true. `templates/config.md` ships ten rows across its main table
  (seven) and `## The fold's values` (three), and the skill's table now names
  all ten. `Reference specs` was missing from the skill before this branch.
- **Claimed** (Q10): writing `docs/the-pact.md` from a work item is allowed
  here. **Found**: the grounds hold. The implement skill's sentence at
  `skills/implement/SKILL.md:91` is about a repository's own docs
  convention, and this repository already carries fold markers of four other
  live work items in `docs/` (`the-broad-gate.md`,
  `commit-review-gate-spec.md`, `worktree-guard-spec.md`). `fold-check`
  exits 0 over the result (executed).
- **Claimed** (S13): "home" and "member" ship nowhere. **Found**: every added
  line outside `seal/` and `tests/` was searched. The only hits are code
  variables named `home` that mean a `seal/` root, which the overview names
  as left on purpose. No printed sentence carries one. The case sweeps four
  texts, the four S13 names (⬜ 11).

## Findings from execution

### 🟡 1 — A merge that took the other side's clause hides HEAD's own older version

`skills/evidence-check/scripts/pact_check.py:240`. `History.commits` runs
`git rev-list <revs> -- seal/pact.md` with git's default history
simplification. At a merge that is TREESAME to one parent for the pact file,
git follows only that parent. So when both sides edited the clause and the
merge kept the side branch's text, the first-parent commits that held the
older clause are not in HEAD's list. They are not in the other list either,
because it says `--not HEAD`.

Executed: main v1 → side (from v1) v3 → main v2 → merge keeping v3. A
signatory citing v2 read `UNMATCHED` ("the version was squashed away or
never existed") where `SUPERSEDED` is true. `rev-list HEAD` listed two
commits; `rev-list --full-history HEAD` listed four, v2 among them.

Why it matters: the two reports send a person to different places.
`SUPERSEDED` says re-anchor in the signatory. `UNMATCHED` says read both
sides because the history is gone, and here it is not gone. A merge that
resolves a pact conflict toward the incoming branch is an ordinary act, so
this is not the squash case `docs/the-pact.md` §*What this does not see*
already accepts. The exit code stays 1, so nothing goes quiet.

The fix adds `--full-history` to both lists. A merge commit that is TREESAME
to one parent is then listed as well, and its text equals that parent's,
so no verdict changes but the hidden one.

### 🟡 2 — A Signatory row the walk cannot read drops every signatory below it in silence

`hooks/config.py:820` (`pact_signatories`). The walk stops at the first line
that is not a one-cell row, and returns what it read with no refusal. A GFM
table row may omit its closing pipe, and a person may add a note column to
one row. Either ends the walk.

Executed: a pact whose table lists the row
`| https://example.com/org/orders-web |` and then
`| https://example.com/org/orders-mobile`, with no closing pipe.
`pact_signatories` returned one signatory and no refusal. `pact-check`
printed `1 of 1 signatory read` and exited 0. A second row with two cells
gave the same result.

Why it matters: Q5 chose "the pact lists them" over scanning the map
precisely because "a signatory missing from the map is skipped in silence".
This is that silence, reached through the table instead of the map. A
signatory nobody read reports as clean.

### 🟡 3 — A backticked name inside a pact anchor's heading turns the signatory's own check red

`skills/evidence-check/scripts/evidence_check.py:2930` (`stated_names`) and
`:2945` (`stated_coordinates`). The records arm reads every backticked
compound name on a claim line with `RECORD_NAME_RE`, and every backticked
`path#name` with `RECORD_COORD_RE`. Neither blanks pact anchors first. A
pact clause heading that names a field in backticks is the ordinary shape of
a contract clause, and the field name belongs to the pact's repository.

Executed: a signatory whose live work item's `spec.md` Grounding cites
``pact:orders-api/"## Order response shape / ### The `order_total` field"@1a2b3c4d`` (NAME NOT IN TREE)
— the signatory's own `evidence-check` exited 2 with `NOT-IN-TREE
seal/specs/1790000000-x/spec.md:7` for that name. A signatory written in
another language, where the field is spelled differently or only arrives
over the wire, never carries the name.

Why it matters: spec item 6 promises that a pact anchor leaves the
signatory's own exit status alone, and S7 tested only `OLD-FORMAT`,
`BROKEN` and `EXTERNAL`. Phase 3 enumerated the class as sites that call
`.sub` on a coordinate pattern. The class the promise needs is every reader
that reads text inside a pact anchor with a pattern of its own (§12), and
these two readers do that without a `.sub`. For a local coordinate the same
reading is harmless, because the name lives in a file of this tree. For a
pact anchor it lives in another repository. The remedy the message prints,
`NAME NOT IN TREE` on the line, works, but it asks every signatory to mark
up every clause citation.

## Findings from reading

### 🟡 4 — A pact anchor that does not parse is read by nobody

`skills/evidence-check/scripts/pact_check.py:437`. `pact-check` grades only
`PACT_ANCHOR_RE` matches. An anchor typed with `#` for `/`, without its
quotes, or without its hash matches nothing. The signatory's own
`evidence-check` passes it over by design, and `chain_check` does not count
it. So a mistyped citation leaves the signatory's link to the clause
unchecked, and `pact-check` exits 0.

Why it matters: spec item 7 makes this anchor the durable link and the input
step C's trigger reads. The local equivalent has a net, `MALFORMED`, for
exactly this reason. Here the anchor is hand-written in two places per
citation, and nothing names a near miss. The template's own advice
(`@00000000`, corrected from the first report) only helps an anchor that
parses.

### ⬜ 5 — `declared_pacts` has no caller, and it holds the opposite policy to `pact-check`

`hooks/config.py:799`. Nothing outside its test calls it. Its docstring says
a config that will not read is "answered as no row at all". `pact-check`
does the opposite on purpose (`UNREADABLE`, exit 2, `pact_check.py:403`),
and `pact_declaration`'s own docstring calls reading a written row as absent
"the silence this reader exists to end". A dead helper with the refused
policy is what the next caller will reach for.

### ⬜ 6 — 0.15.4's MALFORMED row names two patterns as the whole list, and there are now three

`seal/releases/0.15.4.md:54`. The claim reads "a coordinate neither
`ANCHOR_RE` nor `OLD_COORD_RE` parses … is `MALFORMED`". A pact anchor in a
`Code grounds` cell is parsed by neither and is not refused, by design. The
phase-3 note explains that, but the claim's letter is now false and was not
corrected in place. Paperwork, so a correction rather than a fix.

### ⬜ 7 — Two released rows had their coordinate re-pointed to another file

`seal/releases/0.5.0.md:212` (S17c) and `seal/releases/0.9.1.md:77` (R5).
Each row's `seal.py#normalise_remote` coordinate now reads
`hooks/config.py#normalise_remote`, under a `Corrected` note. `CLAUDE.md`
§*commit early* says "A row whose anchor a change removes is REMOVED, not
re-pointed … Write the new claim as a new row in the work item's own
fragment." The anchor did not strictly go away, since the alias is a
module-level unit of that name, so the rule's trigger is arguable. What
changed is that two release files now say those releases verified a unit in
a file that did not hold it then. Paperwork. Whether this counts as a
removal is the orchestrator's reading of the rule. If it does, the
`isinstance` claim belongs in the fragment, beside P2, which states the move
but not the guard.

### ⬜ 8 — Four printed branches of `pact-check` have no case

`skills/evidence-check/scripts/pact_check.py:393`, `:403`, `:433`, `:352`.
These are `ONE-SIDED` for a signatory with no `seal/` root, `UNREADABLE` for
its config, for an anchor file, and for the pact. None is reached by a case,
so none of the four sentences is pinned (§14). The first is load-bearing: by
reading, without the branch `their_home` is `""` and the next line joins a
path onto it and reads `config.md` from the current directory. It is listed
under the tests to plant.

### ⬜ 9 — A pact that lists its own repository reports it as not found

`skills/evidence-check/scripts/pact_check.py:387`. The owner's definition
makes the pact's repository a signatory too, so listing it in the
`Signatory` table is a plausible slip. The sibling search skips the root, so
the entry reads `NOT FOUND … no checkout of it was found on this machine`,
which sends a person to look for a checkout of the repository they are
standing in. The template says the table lists every OTHER signatory. The
code does not refuse the case in those words.

### ⬜ 10 — Two reads repeat work they could do once

- `pact_check.py:195`: the sibling search runs `git remote get-url origin`
  once per sibling directory per signatory. In a parent directory holding
  many checkouts, which is where siblings are searched, that is siblings ×
  signatories subprocesses for answers that do not change between
  signatories.
- `chain_check.py:4013`: every chain-check run in a repository with a
  `seal/config.md` now loads `evidence_check.py` and `hooks/config.py`,
  though most such repositories have no `Pact` row, no `seal/pact.md` and no
  `pact:` in a spec.

### ⬜ 11 — The word case holds four texts, and the words ship in at least five more

`tests/test_one_word_one_meaning.py:565`. `PACT_SWEPT` and `PACT_SECTIONS`
are the four texts S13 names. The same words also ship in
`templates/config.md` §*Pact*, both READMEs' cheat-sheet rows,
`skills/config/SKILL.md`'s two rows, and the sentences `pact-check` and
`chain-check` print. All of them are clean today, which I searched for. They
are just not held.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | HEAD's history of the pact is read with default history simplification, so a clause version on the side a merge did not keep reads `UNMATCHED` where `SUPERSEDED` is true | `skills/evidence-check/scripts/pact_check.py:240` | open | executed: merge keeping the side branch's clause; signatory citing main's v2 read `UNMATCHED`; `--full-history` lists the hidden commit |
| 🟡 2 | `pact_signatories` stops at the first row it cannot read and refuses nothing, so every signatory below it goes unread and `pact-check` exits 0 | `hooks/config.py:820` | open | executed: a row with no closing pipe, and a row with two cells, each dropped the signatory, `1 of 1 signatory read`, exit 0 |
| 🟡 3 | The records arm reads a backticked name inside a pact anchor's heading as a claim about the signatory's tree, so the signatory's own `evidence-check` exits 2 | `skills/evidence-check/scripts/evidence_check.py:2930` | open | executed: `NOT-IN-TREE` at exit 2 for a field name in a cited clause heading; spec item 6 promises the exit status is left alone |
| 🟡 4 | A pact anchor that does not parse is graded by nobody and `pact-check` exits 0 | `skills/evidence-check/scripts/pact_check.py:437` | open | read: only `PACT_ANCHOR_RE` matches are graded, and no reader names a near miss |
| ⬜ 5 | `declared_pacts` has no production caller and answers an unreadable config as no row, the policy `pact-check` refuses | `hooks/config.py:799` | open | read: `git grep` finds only its test |
| ⬜ 6 | 0.15.4's MALFORMED claim lists two patterns as exhaustive; a pact anchor is now a third, exempt match, and the claim was not corrected in place | `seal/releases/0.15.4.md:54` | open | read: paperwork correction |
| ⬜ 7 | Two released rows had `seal.py#normalise_remote` re-pointed to `hooks/config.py#normalise_remote` rather than removed and re-stated in the fragment | `seal/releases/0.5.0.md:212` | open | read: `CLAUDE.md` REMOVED-not-re-pointed rule; trigger arguable because the alias still resolves; paperwork, and the orchestrator reads the rule |
| ⬜ 8 | Four printed branches of `pact-check` (no-root `ONE-SIDED`, three `UNREADABLE`) are reached by no case | `skills/evidence-check/scripts/pact_check.py:393` | open | read: no case writes those states; §14 |
| ⬜ 9 | A pact listing its own repository reads it as `NOT FOUND` on this machine | `skills/evidence-check/scripts/pact_check.py:387` | open | read: the sibling search skips the root, and nothing refuses the entry |
| ⬜ 10 | The sibling search asks git once per sibling per signatory, and chain-check loads two readers on every run with a `config.md` | `skills/evidence-check/scripts/pact_check.py:195` | open | read |
| ⬜ 11 | The word case holds the four texts S13 names; five more shipped texts carry the words unheld | `tests/test_one_word_one_meaning.py:565` | open | read: conforms to S13 as written; every added line outside `seal/` and `tests/` searched clean |
| 🟢 | The `ANCHOR_RE` blanking sites are exactly `old_format_rows`, `malformed_rows` (two expressions) and `migrate`, and each blanks pact anchors first | `skills/evidence-check/scripts/evidence_check.py:1658` | confirmed | read: re-derived by `git grep` over every non-test `.py`; executed: the three cases went red with the `old_format_rows` blanking removed |
| 🟢 | Git never decides `OK`; exit 0/1/2 classes match spec item 9, and every new status is in one exit set | `skills/evidence-check/scripts/pact_check.py:295` | confirmed | read: `grade` and `EXIT_ONE`/`EXIT_TWO`; executed: the module's 17 cases green |
| 🟢 | `chain_check` moves no exit status on anything about a pact, before or after its early return | `skills/code-review/scripts/chain_check.py:4514` | confirmed | read: notices only, `errors` untouched; executed: the S5/S6 cases green |
| 🟢 | One remote normaliser; `seal.py`'s name is an alias of `hooks/config.py`'s | `skills/implement/scripts/seal.py:284` | confirmed | read: bodies identical; executed: identity probe |
| 🟢 | The config skill's count of ten rows matches what the template ships | `skills/config/SKILL.md:31` | confirmed | read: seven in the main table, three under §*The fold's values* |
| 🟢 | Q10's grounds for a new `docs/` file hold | `docs/the-pact.md` | confirmed | read: four live work items already carry fold markers in `docs/`; executed: `fold-check` exit 0 |
| 🟢 | The ledger re-reads sampled hold, except ⬜ 6 and ⬜ 7 | `seal/releases/0.13.1.md:65` | confirmed | read: all six `chain_check.py#main` rows (the new call precedes the early return and touches no error list); 0.13.1's region claim (0.5.0.md lines 154–231 changed only at 212); 0.5.0's S1 and S2 `Procedure` rows; 0.17.0's `SHIPPED` row; executed: `evidence-check --strict` exit 0 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the six new or changed modules (`test_pact_check`, `test_a_signatory_declares_its_pact`, `test_a_signatorys_ci_prints_its_pact`, `test_a_pact_anchor_is_no_coordinate_of_the_signatory`, `test_one_word_one_meaning`, `test_the_settings_have_a_front_door`) | 84 passed, exit 0 |
| `bin/test` on seven modules the diff touches or the phases name (`test_a_document_that_names_a_script_says_how_to_reach_it`, `test_every_orchestrator_act_names_its_delivery`, `test_a_reference_root_is_read_and_never_taken`, `test_docs_line_wrap`, `test_every_reader_ends_a_line_where_gfm_does`, `test_the_pull_request_language_is_the_repositorys`, `test_the_records_can_be_carried_out_and_in`) | 478 passed, 7 skipped, exit 0 |
| `bin/evidence-check --strict .` at the target SHA | exit 0 |
| `bin/fold-check` at the target SHA | exit 0, 158 statements in 15 documents |
| Red check: `old_format_rows`' pact blanking removed, and "the home repository" planted in `templates/pact.md` | 4 cases red (three in the anchor module, the word case); tree restored |
| Probe A (finding 1): merge keeping the side branch's clause, signatory citing main's v2 | `UNMATCHED`, exit 1; `rev-list` lists 2 commits, `--full-history` lists 4 |
| Probe B (finding 2): a Signatory row with no closing pipe, then a row with two cells | one signatory returned, no refusal; `pact-check` exit 0 |
| Probe 2 (finding 3): a live spec citing a clause whose heading holds a backticked field name, signatory's `evidence-check` | exit 2, `NOT-IN-TREE` for that name |
| Probe D: a pact anchor with `v1.2:3` in its heading in a ledger row | `old_format_rows` empty |
| The full suite, the repository-wide lint and the typecheck | not yet — never run in this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🟡 1

`skills/evidence-check/scripts/pact_check.py`, `History.commits`:

```python
    def commits(self, *revs):
        # `--full-history`: by default git follows only the TREESAME parent
        # of a merge, so a clause version on the side a merge did not keep
        # vanished from HEAD's list (and `--not HEAD` kept it out of the
        # other one), and its hash read UNMATCHED where SUPERSEDED is true.
        # A merge listed this way carries one parent's text, so it changes
        # no verdict.
        out = git(self.root, "rev-list", "--full-history", *revs, "--", self.rel)
        return out.split() if out else []
```

### 🟡 2

`hooks/config.py`, `pact_signatories`:

```python
    values, seen_header, stray = [], False, None
    for _index, line in unfenced(text.splitlines(), text):
        if not seen_header:
            seen_header = bool(SIGNATORY_HEADER.match(line))
            continue
        if CONFIG_SEPARATOR.match(line.strip()) and not values:
            continue
        match = SIGNATORY_ROW.match(line)
        if not match:
            # A table line the walk cannot read ends the walk, and every
            # signatory written below it would go unread in silence.
            if line.lstrip().startswith("|"):
                stray = line.strip()
            break
        values.append(unescaped(match.group("value").strip()))
    if not seen_header:
        return [], ["holds no `| Signatory |` table, so it names no signatory"]
    signatories, refusals = remote_entries(
        values, "the `Signatory` table holds an empty row", named=False
    )
    if stray is not None:
        refusals.append(
            f"its `Signatory` table stops at `{stray}`, which is not a one-cell "
            "row closed by `|` — every signatory below it would go unread"
        )
    if not values:
        refusals.append("its `Signatory` table lists nobody")
    return signatories, refusals
```

### 🟡 3

`skills/evidence-check/scripts/evidence_check.py`, both readers:

```python
def stated_names(lines):
    """[(line number, name)] for every compound identifier a record states.

    A pact anchor is blanked first (#647): its heading is a clause of
    another repository's pact, so a name quoted in it is not a claim about
    this tree."""
    out = []
    for number, line in claim_lines(lines):
        for match in RECORD_NAME_RE.finditer(blank_pact_anchors(line)):
            name = match.group(1)
            if compound(name):
                out.append((number, name))
    return out


def stated_coordinates(lines):
    """[(line number, path, name)] for every name a record writes as
    `path#name`, on the lines `claim_lines` reads, outside pact anchors.

    Every such span, compound or not: whether its name is a claim depends on
    whether its path resolves, which is `coordinate_misses`' question."""
    return [
        (number, match.group("path"), match.group("name"))
        for number, line in claim_lines(lines)
        for match in RECORD_COORD_RE.finditer(blank_pact_anchors(line))
    ]
```

### 🟡 4

`skills/evidence-check/scripts/pact_check.py`: a module constant, and a
second pass in the per-file loop of `check`, after the graded loop:

```python
# Anything that starts like a pact anchor, so one that does not parse is
# named rather than passed over (a mistyped citation is otherwise read by
# nobody: not here, not by the signatory's own check, not by chain-check).
PACT_MENTION_RE = re.compile(r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]+)\S*")
```

```python
            graded = {m.start() for m in checker.PACT_ANCHOR_RE.finditer(view)}
            for near in PACT_MENTION_RE.finditer(view):
                if near.group("name").lower() != name or near.start() in graded:
                    continue
                line = view.count("\n", 0, near.start()) + 1
                found(
                    REFUSED,
                    written,
                    f"{shown}:{line}",
                    f"`{near.group(0)}` does not parse as "
                    f"`pact:{name}/\"<heading path>\"@<hash>`, so "
                    "nothing grades it. Quote the heading path and give it a "
                    "hash, `@00000000` until the first report names the real one",
                )
```

### ⬜ 5

`hooks/config.py`: delete `declared_pacts`, and the case
`test_an_unreadable_config_is_no_declaration` in
`tests/test_a_signatory_declares_its_pact.py`, or have `pact_check.py` call
one helper whose unreadable answer is the refusal it already prints.

```python
# delete hooks/config.py#declared_pacts (lines 799-808) and its test
```

### ⬜ 6

`seal/releases/0.15.4.md:54`, claim cell, with a dated note:

```markdown
A `Code grounds` cell holding a coordinate none of `ANCHOR_RE`, `OLD_COORD_RE` and `PACT_ANCHOR_RE` parses, or citing none while the row claims something, is `MALFORMED`: … **Corrected 2026-10-03 by work item 1790993137 (#647):** a pact anchor is a third pattern's match and is not refused.
```

### ⬜ 9

`skills/evidence-check/scripts/pact_check.py`, in `check`, before resolving
each signatory's checkout:

```python
        if signatory[1] == config.normalise_remote(mine):
            found(
                REFUSED,
                written,
                f"seal/{PACT_FILE}",
                "the pact lists its own repository; the `Signatory` table "
                "lists every OTHER signatory, so take this row out",
            )
            continue
```

## Regression tests to plant

| Finding | Destination | Case |
|---|---|---|
| 🟡 1 | `tests/test_pact_check.py` | a merge keeping a branch's clause leaves main's older version in HEAD's history |
| 🟡 2 | `tests/test_a_signatory_declares_its_pact.py` and `tests/test_pact_check.py` | a row with no closing pipe, and a row with two cells, are refused and `pact-check` exits 2 |
| 🟡 3 | `tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py` | a live spec citing a clause whose heading holds a backticked compound name: the signatory's `evidence-check` exits 0 |
| 🟡 4 | `tests/test_pact_check.py` | `pact:orders-api#"## X"@1a2b3c4d` and a quoted locator with no hash are each `REFUSED`, exit 2 |
| ⬜ 8 | `tests/test_pact_check.py` | a signatory with no `seal/` root is `ONE-SIDED` with its sentence pinned; a config, an anchor file and the pact that will not read are each `UNREADABLE`, exit 2 |

```python
# tests/test_pact_check.py — 🟡 1
def test_a_clause_a_merge_did_not_keep_is_still_heads_history(world):
    """Main held v2; a branch cut from v1 changed the clause, and the merge
    kept the branch's text. A signatory built against v2 is SUPERSEDED,
    not UNMATCHED: v2 is in HEAD's history, on the side git's default
    simplification does not follow."""
    api = world["api"]
    git(api, "switch", "-qc", "early", "main~1")
    write(api, "seal/pact.md", pact("id, total, tax"))
    commit(api, "the clause, changed from v1")
    git(api, "switch", "-q", "main")
    git(api, "merge", "-q", "--no-ff", "-s", "ours", "--no-commit", "early")
    write(api, "seal/pact.md", pact("id, total, tax"))
    commit(api, "merge early, keeping its clause")
    cite(world, clause(V2))
    code, out = run(world)
    assert code == 1, out
    assert "SUPERSEDED" in out and "UNMATCHED " not in out, out
```

```python
# tests/test_a_signatory_declares_its_pact.py — 🟡 2
@pytest.mark.parametrize(
    "row",
    ["| https://example.com/org/orders-mobile", "| https://example.com/org/orders-mobile | the app |"],
    ids=["no closing pipe", "two cells"],
)
def test_a_signatory_row_the_walk_cannot_read_is_refused(row):
    text = (
        "# Pact\n\n| Signatory |\n|---|\n| https://example.com/org/orders-web |\n"
        + row
        + "\n\n## A\n\nx\n"
    )
    signatories, refusals = config.pact_signatories(text)
    assert [s[2] for s in signatories] == ["orders-web"]
    assert any("every signatory below it would go unread" in r for r in refusals), refusals
```

```python
# tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py — 🟡 3
def test_a_name_quoted_in_a_pact_clause_heading_is_not_a_claim_here():
    line = (
        '| G1 | pact:orders-api/"## Order response shape / ### The `order_total` '
        'field"@1a2b3c4d | the total is a string |'
    )
    assert ec.stated_names([line]) == []
    assert ec.stated_coordinates([line]) == []
```

## Facts for the evidence ledger

| Claim | Where it is grounded | How it was established |
|---|---|---|
| `pact-check` decides `OK` from the working-tree pact alone, and reads git only after a mismatch | `skills/evidence-check/scripts/pact_check.py#grade` | read |
| The three `ANCHOR_RE` blanking sites in `evidence_check.py` are `old_format_rows`, `malformed_rows` and `migrate`, and each blanks pact anchors first | `skills/evidence-check/scripts/evidence_check.py#blank_pact_anchors` | read (re-derived by `git grep`), executed (red with the blanking removed) |
| `seal.py`'s `normalise_remote` is the same object as `hooks/config.py`'s | `skills/implement/scripts/seal.py#normalise_remote` | executed |

These are already P2, P5 and P9 in the work item's fragment, in substance.
Nothing new needs a row until findings 1–4 are fixed. Each fix then changes
what P8, P9 or P5 claims, and those rows are re-read then.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (history simplification hides a superseded clause), 🟡 2 (an unreadable Signatory row drops signatories in silence), 🟡 3 (a backticked name in a pact anchor's heading turns the signatory's check red), 🟡 4 (a pact anchor that does not parse is graded by nobody)
Loses a record or crashes: no

The broad gate has not come due: four findings need a fix, so the sealer's
spawn waits for the verifying round.

## Proof block

Files opened in this round, at the target SHA: `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/`
`spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
`phases/phase-3.md`, `phases/phase-5.md`; `hooks/config.py` (the new pact
section, `CELL`, `CONFIG_ROW`, `unescaped`); `hooks/optin.py` (`home_paths`,
`home_at`); `skills/evidence-check/scripts/pact_check.py` (whole);
`skills/evidence-check/scripts/evidence_check.py` (`ANCHOR_RE`,
`PACT_ANCHOR_RE`, `OLD_COORD_RE`, `gfm_lines`, `unquoted`, `content_hash`,
`heading_level`, `unescape`, `heading_path`, `resolve_unit`, the malformed
helpers, `grounds_cells`, the records arm from `NOT_IN_TREE` to
`file_claims`); `skills/code-review/scripts/chain_check.py` (the pact
section, `load`, `main` from the reader load to the end);
`skills/implement/scripts/seal.py` (the alias); `bin/pact-check`,
`bin/pact-check.cmd`, `bin/correction-check`; `templates/pact.md`,
`templates/config.md` (the row table, §*What no row governs*, §*Pact*);
`skills/config/SKILL.md` (§*Procedure*); `skills/evidence-check/SKILL.md`
(§*pact-check*); `skills/implement/orchestration.md` (the new subsection);
`docs/the-pact.md`; `tests/test_pact_check.py` (fixtures and S11/S3 cases),
`tests/test_a_signatorys_ci_prints_its_pact.py` (S5/S6),
`tests/test_one_word_one_meaning.py` (the new case),
`tests/test_the_settings_have_a_front_door.py` (the diff); the
`seal/ledger.md` and `seal/releases/*.md` diff (every added note), and the
rows named in the 🟢 ledger verdict and in ⬜ 6 and ⬜ 7.
