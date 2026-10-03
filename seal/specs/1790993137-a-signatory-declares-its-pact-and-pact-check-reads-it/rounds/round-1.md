# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — review round 1

| Field | Value |
|---|---|
| Target SHA | 90c3323df64392422805597e5fe527852dffc1bf |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 735 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (history simplification hides a superseded clause), 🟡 2 (an unreadable Signatory row drops signatories in silence), 🟡 3 (a backticked name in a pact anchor's heading turns the signatory's check red), 🟡 4 (a pact anchor that does not parse is graded by nobody) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 targets `90c3323d`, over the build's diff `233f0455..90c3323d`. It was asked to check #647 steps A and B against `spec.md` items 1–12 and S1–S14 and the approved plan, then quality. The owner's names and decisions of 2026-10-03 were given as fixed. Seven things were named for close checking:
- whether every site that blanks `ANCHOR_RE` also blanks `PACT_ANCHOR_RE`, re-derived rather than taken from phase 3;
- whether `pact-check` lets git history decide only a mismatch's direction, never `OK`, and never skips a missing signatory silently;
- whether `chain_check` moves no exit code at a signatory's pull request;
- the move of `normalise_remote` into `hooks/config.py`;
- the config rows and the config skill's row count;
- `docs/the-pact.md` against implement SKILL's no-new-docs sentence (Q10);
- the 49 ledger rows re-read in place, sampled hard.

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

## Paste-ready fixes

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
```python
# delete hooks/config.py#declared_pacts (lines 799-808) and its test
```
```markdown
A `Code grounds` cell holding a coordinate none of `ANCHOR_RE`, `OLD_COORD_RE` and `PACT_ANCHOR_RE` parses, or citing none while the row claims something, is `MALFORMED`: … **Corrected 2026-10-03 by work item 1790993137 (#647):** a pact anchor is a third pattern's match and is not refused.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
