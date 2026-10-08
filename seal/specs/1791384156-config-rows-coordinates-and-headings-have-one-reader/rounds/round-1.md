# 1791384156-config-rows-coordinates-and-headings-have-one-reader — review round 1

| Field | Value |
|---|---|
| Target SHA | 7e0b11932882ff35d188884b12ae19e854379709 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 882 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `9f186d2aceda8cb22660bc73775f555f9a261031..105d96eac49a8fe8dacf09b41dcf8099195db9e6`, 8 commits |
| Contract changes | run → run, attempt, gh_json, _issue_api, drop_label, arrived, existing_labels, create_label, add_label, is_ancestor, commit_message, release_exists, merged_pulls, create, merge_base, subjects_since, milestone_titles, open_in_milestone, labelled, gh, tagged, rasterise, content_at, try_run, list_open_issues, close_issue, open_issue, add_xdist, add_markdown_it, add_pillow, add_cmarkgfm, build, main, README.md, git, _process, common_dir, _git, claude_ancestor, _ps, git_dir, dirty, resolve_runner, git_dir_of, repo_root, git_common_dir, current_branch, owner_pid, latest, ancestors, proc_cwd, host_app, tty_idle_minutes, lease_owner_alive, lease_dir, sessions_in_tree, tracked_changes, phantom_entries, repo_paths, 0.10.0.md, 0.11.2.md, 0.11.3.md, 0.12.2.md, 0.12.3.md, 0.15.4.md, 0.17.0.md, plan.md, questions.md, spec.md, overview.md, post-review-check-2.md, post-review-check.md, round-1-report.md, round-2-report.md, round-2.md, round-1.md, SKILL.md, config_at_head, carried_by_a_pull_head, resolves_to, pull_request_cell, pull_request_is_ready, read_blobs, config_at, git_asked, porcelain, tracked, install_workflow, remove_workflow, gitlinks_under_root, switch, released, tracked_text, run_arms, broad_gate.py, cmd_exe_reads, handed_to_shell, quote, compare_at_base, seal_record, gate, run_gh, commit_of, overviews_at, tree_at, wrote_a_spec, show, pytest |
| New units | config_at_head (depth 1); _shown_lines (depth 1); _LooseHeading (depth 1); test_a_config_that_will_not_read_is_a_notice_and_never_a_crash (depth 1); SETTLE_COPY_AT_0_20_0 (depth 1); released_by_0_20_0 (depth 1); test_a_base_revisions_heading_is_a_level_two_or_three_heading_by_the_rule (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 and 🔴 2 (the pull request is red), 🟡 3 (a re-read that vouches for a broken claim), 🟡 4, 🟡 5, 🟡 6 |
| Loses a record or crashes | yes — `chain_check.py --worktree` raises `UnicodeDecodeError` from `read_record` on an undecodable `seal/config.md` (🟡 5; the raise executed, the path from `main` read; the lines predate this branch) |

- [x] Pass

## What this round was asked

Round 1 of the build at 7e0b1193, against 5623d728, since the release branch's #858 and #864 are not merged in yet. The spawn named seven things to attack. First, the failing Windows group-1 and release jobs of PR #882, read from their logs. Second, whether every reader of seal/config.md goes through one reader. Third, whether the exit-2 refusals reach no hook and no mid-flight command. Fourth, a doubled routing.md row. Fifth, the heading rule against CommonMark corner cases and the vendored twin. Sixth, whether the two reversed cases are what spec Scope 1 asks. Seventh, the Re-read-to-Corrected replacements and a sample of the 61 re-reads, plus the reviewer's own axes. It also ran the eight guard modules once. Facts arrived labelled. Executed by the orchestrator: gh pr checks 882. Read from the smith: the reversals, the two unplanned fixes, the 58/5 identity figures, the byte-identical pattern, the 777-file heading comparison and the ledger rows.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The Windows shard fails: the case asserts `seal/config.md` and the refusal names `seal\config.md` | `tests/test_a_released_row_is_read_again_in_a_fragment.py:859` | **fixed** `c6e32946` | fixed at c6e32946 — the doubled freeze row's case matches `seal/config.md` with `os.sep` read as `/`, as the sealer's cases do; the other new path assertions were read and build their path with `os.path.join` or name a git path; CI log of job 113099210318, 2 failed; `display_name` keeps the OS spelling by design |
| 🔴 2 | The release job fails: the survivor sweep names 33 places and the work item holds no `survivors.md` | `.github/workflows/hygiene.yml:262` | **fixed** `105d96ea` | fixed at 105d96ea — `survivors.md` records the four places the sweep names over `origin/release/v0.21.0...HEAD`, each read; the other 29 of the round's 33 were character-class patterns that stopped being named once 0bb98893 froze `settle`'s old copy in the tests, and the file says so. `survivor-check` with the file exempting: exit 0; reproduced in the clone, exit 1, 33 places; with the paste-ready file, exit 0 |
| 🟡 3 | Two `Re-read ·` rows say 0.19.0 `Corrected · C1` holds; its clause on a vendored copy reading an unreadable config is now an exit-2 refusal | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:16` | answered | corrected at 9e508b5c: the two `Re-read ·` rows for 0.19.0's `Corrected · C1` are replaced by one `Corrected ·` row whose claim says an unreadable `config.md` is refused at exit 2 before anything is planned, carrying every coordinate the released row rests on plus `frozen_from` and `vendored_config_text`; the case row 40 cites asserts exit 2 since this branch (`tests/test_a_signer_records_a_pact_change.py:1572`) |
| 🟡 4 | S7's case compares `coordinate_paths` with the grammar it is built from, so it is red only when the name is missing | `tests/test_settle_reads_before_it_removes.py:1844` | **fixed** `0bb98893` | fixed at 0bb98893 — S7 compares `coordinate_paths` with `settle`'s own pattern as it stood at 0.20.0, frozen in the test, over the ledgers released by 0.20.0; red under `mutation-check` with the checker's quoted locator narrowed; read; the docstring's own red is the missing attribute |
| 🟡 5 | `chain_check.py`'s pact notices read `seal/config.md` by their own rule: lenient at HEAD, and a `UnicodeDecodeError` under `--worktree` | `skills/code-review/scripts/chain_check.py:4320` | **fixed** `f743e6d2` | fixed at f743e6d2 — `pact_notices` reads the config through `config_at_head` (HEAD's blob decoded strictly, or `hooks/config.py#config_text` under `--worktree`), so an unreadable config is one notice naming it; `read_record` decodes a file on disk as the HEAD read does, so `--worktree` no longer raises. Red under `mutation-check` three ways; executed: `read_record` raises on an undecodable file; the call from `main` is read; lines predate the branch |
| 🟡 6 | The S12 heading grep misses a `#{2,3}` spelling, and `LOOSE_HEADING` stands in the rule's own file | `tests/test_a_format_has_one_reader.py:75` | **fixed** `6907b221` | fixed at 6907b221 — `LOOSE_HEADING` asks `heading_level` for level 2 or 3 and decides only the wording; the heading grep reads any counted `#` run (`#\{\d`). Red under `mutation-check` with the old pattern put back; read; `skills/verify/scripts/unverified_check.py:158` |
| ⬜ 7 | The config twin and the plugin's reader differ on a form feed or U+2028 in a row; the docstring says fences and comments are the only difference | `skills/evidence-check/scripts/evidence_check.py:3919` | **fixed** `9af7b103` | fixed at 9af7b103 — `vendored_config_rows`' docstring names the second way the twin differs, a row holding a character only Python ends a line at, with the round's measurement; executed probe over eight shapes, two differ |
| ⬜ 8 | The standing statement says a heading is read where a renderer shows it; the checker blanks closed fences only, so HTML blocks and comments still open sections | `seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md:200` | deferred #872 | #872 — the mechanism, which lines a reader hides before it asks the heading rule, is the live-line family #872 holds; `overview.md` §*Not done* states the limit of `spec.md`'s sentence (293d3ca8); executed; the tree holds none (0 and 0); the hiding rule is #872's family |
| ⬜ 9 | A doubled `Pact` row's refusal no longer says to list every pact in one row | `hooks/config.py:977` | answered | `spec.md` §*Data & interfaces* ordered `pact_declaration`'s own doubled-row sentences to become the generic one's, and `docs/the-pact.md` §*How a signer names the pact* says a row written twice has no value at all; a doubled `Pact` now lists no pact, so there is no row to tell a person to merge entries into; as `spec.md` §*Data & interfaces* ordered |
| ⬜ 10 | A garbled clause and an over-long line in `table_rows`' docstring | `hooks/routing.py:165` | **fixed** `9af7b103` | fixed at 9af7b103 — the clause reads "a label shown twice has no value at all", wrapped under the line length; read |
| ⬜ 11 | `resolve_unit` rebuilds `markdown_lines` once per quoted `.md` anchor | `skills/evidence-check/scripts/evidence_check.py:713` | **fixed** `9af7b103` | fixed at 9af7b103 — `markdown_lines` is memoised per distinct text (`_shown_lines`); one `--strict .` run makes 360 fence-blanking passes with it and 1,626 without, counted in-process; executed, one run each: 13.17 s at base, 15.35 s at target |
| 🟢 | The two reversed cases are what `spec.md` §*Scope* 1 and S2 ask | `tests/test_the_mode_is_a_row_and_a_command.py:694` | confirmed | read against the spec; the folder line is still printed |
| 🟢 | Hooks read a refusal as silence and no hook reaches a command that now exits 2 | `hooks/mode-gate.py:164` | confirmed | read; `hooks/evidence-advisor.py:225`; `seal mode --check` exit 0 executed |
| 🟢 | A doubled strict `routing.md` label is no declaration and a doubled optional one is unanswered | `hooks/routing.py:242` | confirmed | executed probe of four shapes |
| 🟢 | The two 0.11.4 rows replaced by `Corrected ·` rows, and the other seven corrections, state the code as it stands | `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md:89` | confirmed | read against the code; `bin/evidence-check --strict .` exit 0 executed |
| ❓ | The unreadable-config fixtures on Linux and on the three Windows shards that passed | `tests/test_a_released_row_is_read_again_in_a_fragment.py:874` | ❓ out of verified scope | CI shows them green (read); I ran macOS only. The orchestrator answers it from the next CI run after 🔴 1 |

## Paste-ready fixes

```python
    assert "`Ledger frozen from` appears 2 times — one value" in out.stderr
    assert "seal/config.md" in out.stderr.replace(os.sep, "/"), out.stderr
```
```markdown
# Survivors — config rows, the ledger coordinate and a markdown heading have one reader

`survivor-check --range 5623d728...7e0b1193` named 33 places that still carry
wording this item's range removed. Each was read. Thirty are patterns of their
own that share only character classes with the two removed copies of the
coordinate grammar; two are released ledger rows, frozen by `Ledger frozen
from`, which this item's fragment answers; one is a sentence that is still
true where it stands.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.9.1.md` | **A gate is not a writer.** hooks/config.py#declared_mode folds a file that will not open into *declared nothing*, which is right for seal mode | a released ledger row, frozen by `Ledger frozen from`; this item's fragment carries its `Corrected · S7–S10` row |
| `seal/releases/0.15.0.md` | heading_level keeps the reader's own test for a heading — startswith("#") — and adds only the depth, so a #120 at column 0 still ends a | the notes cell of a released ledger row, frozen by `Ledger frozen from`; its claim cell is re-read in this item's fragment (`Re-read · A1`), and the notes record the reading of their date |
| `hooks/cmdline.py` | \{[A-Za-z_][A-Za-z0-9_]*\})?" r"(?:<<< | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | r"(?:<[A-Za-z][A-Za-z0-9-]*" r"(?:[ \t]+[A-Za-z_:][A-Za-z0-9_.:-]*" r"(?:[ \t]*=[ \t]*(?:[^ \t\"'=<>]+ | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/pact_check.py` | r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>[A-Za-z0-9_.-]+)" r"(?:(?=[/#])(?!/\"<)" r" | the pact anchor, which reads a pact name and no ledger coordinate; it shares character classes with the removed copy |
| `skills/evidence-check/scripts/evidence_check.py` | \\\")+\")" r"@(?P<hash>[0-9a-f]{6,12})" | the pact anchor beside the coordinate's one grammar, in the checker that owns both; it reads a pact clause |
| `skills/evidence-check/scripts/pact_check.py` | r"(?P<item>[^\s@]+)@(?P<hash>[0-9a-f]{6,12})" | a pact review's record id, `<work-item-id>@<content hash>`, which is no coordinate |
| `docs/round-record-spec.md` | grep -oE '[0-9a-f]{7,40}\.\.[A-Za-z0-9@_/.-]+' | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/answers.py` | r"[^A-Za-z0-9]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | r"[A-Za-z0-9_.-]+" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/config.py` | </[A-Za-z][A-Za-z0-9-]*[ \t]*>)[ \t]*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/one_heredoc.py` | D is [A-Za-z0-9_]+. | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/one_heredoc.py` | r"[A-Za-z0-9_]+" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/root-migrate.py` | r"^[0-9]{9,10}-[A-Za-z0-9._-]+$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/worktree-guard.py` | r"[^A-Za-z0-9-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `seal/specs/1790381328-malformed-is-graded-like-drifted-and-reads-prose-as-prose/spec.md` | **Item 2, an issue number keeps its sentence.** A # followed by digits that no ASCII word character continues is an issue number, whatever the | another work item's frame, a record of its own time |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/plan.md` | - **The anchor grammar.** skills/evidence-check/scripts/evidence_check.py#ANCHOR_RE needs a path made of [A-Za-z0-9_.@/-], holding a / or a | another work item's plan quoting the coordinate pattern of its time |
| `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/spec.md` | It matches [A-Za-z0-9_.-]+. | another work item's frame quoting a pattern of its time |
| `skills/code-review/scripts/round_record.py` | r"(?<![A-Za-z0-9_])" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/evidence_check.py` | r"[A-Za-z_][A-Za-z0-9_.]*" | the coordinate's one grammar, which the removed copies in `skills/settle/scripts/settle.py` and `.github/scripts/rider_check.py` spelled again |
| `skills/evidence-check/scripts/evidence_check.py` | r"[A-Za-z0-9_.-]+" | the pact anchor built beside the coordinate's one grammar; it reads a pact name |
| `skills/evidence-check/scripts/evidence_check.py` | r"(?<![A-Za-z0-9_.@/-])pact:(?P<name>" | the pact anchor built beside the coordinate's one grammar; it reads a pact name |
| `skills/evidence-check/scripts/evidence_check.py` | # RIDER: the two [A-Za-z0-9_.@/-] repetitions below overlap, so the path | a rider on one of the checker's own path patterns, true as it stands; it shares character classes with the removed copy |
| `skills/evidence-check/scripts/evidence_check.py` | r'[A-Za-z][A-Za-z0-9+.-]*://[^\s"]*' | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/evidence-check/scripts/evidence_check.py` | r"\d+(?![A-Za-z0-9_])" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/implement/scripts/seal.py` | r"[^A-Za-z0-9._-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/broad_gate.py` | r"^ ([A-Za-z0-9_-]+):\s*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/session_cost.py` | r"[A-Za-z_][A-Za-z0-9_]*=" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `skills/verify/scripts/session_cost.py` | r"[^A-Za-z0-9-]" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `tests/test_a_row_points_by_content.py` | r"[A-Za-z0-9_./-]+\.(?:py | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `tests/test_ci_gives_the_checks_what_they_need.py` | r"^ ([A-Za-z0-9_-]+):\s*$" | a pattern of its own that reads no coordinate; it shares only character classes with the removed copy of the coordinate grammar |
| `hooks/routing.py` | A file that cannot be read is not an answer somebody gave, so the gate goes back to asking. | true as it stands: a `routing.md` that cannot be read is no declaration and the commit gate asks; the removed sentence was `hooks/config.py`'s, whose reader now refuses instead |
| `seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/spec.md` | A file that cannot be read is not an answer somebody gave", and 1790635413 pinned R2 the same way. | another work item's frame, a record of its own time |
```
```markdown
| Corrected · C1 · `evidence-check --reverify`, in place and under `--into`, plans every ledger write without making one, records the pact changes the plan owes, and writes the plan only after; it appends one row per re-read ledger row citing a clause of a pact the signer's `Pact` row declares, and per such row with a BROKEN coordinate, to `seal/pact-changes/<work-item-id>.md` (created with its header), and prints a `recorded` line; `Pact notify` filters (`always` adds `—` rows, `never` records nothing); the id is `--into`'s fragment, else the branch's declared work item, else a `LEFT` line and exit 1; a coordinate whose last recorded row for the same clause and ledger row says the same move or the same BROKEN is not appended again, so a change re-landed after its revert is; a record that will not read, decode or parse is named and left; a `seal/config.md` that is there and will not read is refused at exit 2 before anything is planned, by the plugin and by a vendored copy alike, and nothing is re-stamped or recorded; a vendored copy names each citing row, and each other moved row where `seal/config.md` holds a plain `Pact` row and a plain `Pact notify` row that both carry a value, or holds a line that names a pact by `PACT_WORD` (as written or `NFKC(html.unescape)`, the plugin's word and predicate, held equal) and is neither a plain `\| Pact \| … \|` nor a plain `\| Pact notify \| … \|` row, reading a two-cell row (`CONFIG_ROW_RE`, on a GFM line no `str.splitlines`-only character cuts) by its item alone unless it stands directly above a line GFM may read as a delimiter row (`UNDER_A_HEADER`: block-quote markers, a vertical tab or form feed, and a one-column row with no pipe included), where it is a table's header and is read whole with no `\|` asked, and asking no `\|` of a line in a file holding an HTML table cell (`HTML_CELL`), and records nothing; a `Pact notify` row written twice has no value, so `always` cannot be ruled out; a row left whole moved nothing and records nothing; the ledger bytes are what they are without a `Pact` row | `seal/releases/0.19.0.md#"### 1791239490-a-repository-that-keeps-a-pact-is-a-signer">"Corrected · C1 ·"@d1aa3380`, `skills/evidence-check/scripts/evidence_check.py#frozen_from@2f3469f9`, `skills/evidence-check/scripts/evidence_check.py#vendored_config_text@228ea1c7`, `tests/test_a_signer_records_a_pact_change.py#test_a_vendored_copy_whose_config_will_not_read_leaves_the_row@0fa961e4`, `tests/test_a_signer_records_a_pact_change.py#test_a_pact_row_that_will_not_read_leaves_the_row@732701e9` | **Read** 2026-10-08: the cited row's claim against `frozen_from`, which `--reverify` reads before it plans. **Executed** 2026-10-08: both cases, green | 2026-10-08 | Corrected 2026-10-08 by work item 1791384156-config-rows-coordinates-and-headings-have-one-reader: the clause on a vendored copy naming moved rows where `seal/config.md` will not read no longer happens, because the freeze row is read first and an unreadable file is refused there (#867) |
```
```python
# The coordinate pattern `settle.py` kept until #867, frozen here as the
# oracle S7 is measured against. The released ledgers do not change, so the
# paths this copy attributed there are the paths `coordinate_paths` must.
SETTLE_COPY_AT_0_20_0 = re.compile(
    r"(?P<path>[A-Za-z0-9_@.][A-Za-z0-9_.@/-]*[/.][A-Za-z0-9_.@/-]*?)"
    r"#(?:\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)"
    r"(?:>\"(?:[^\"\n]|\\\")+\")?"
    r"@[0-9a-f]{6,12}"
)


def test_settle_attributes_the_paths_its_own_copy_attributed():
    """S7 of #867. `settle` reads `evidence_check.py#ANCHOR_RE` now; over
    this repository's released ledgers every path it attributes is the one
    its own copy attributed, so no segment moved. Red by narrowing the
    checker's locator, which the old copy does not follow."""
    assert not hasattr(settle, "COORDINATE_RE"), "a second grammar is back"
    seen = 0
    for path in real_ledgers():
        with open(path, encoding="utf-8") as f:
            for line in f.read().split("\n"):
                want = [m.group("path") for m in SETTLE_COPY_AT_0_20_0.finditer(line)]
                assert settle.coordinate_paths(line) == want, line
                seen += len(want)
    assert seen > 8000, seen
```
```python
    if WORKTREE:
        try:
            with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
                return f.read()
        except (OSError, ValueError):
            return None
    return git(root, "show", f"HEAD:{rel}")
```
```python
def config_at_head(root, rel):
    """(text, refusal) for REL as HEAD holds it, decoded strictly: the two
    states `hooks/config.py#config_text` tells apart on disk (#867)."""
    if WORKTREE:
        try:
            with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
                return f.read(), None
        except FileNotFoundError:
            return None, None
        except (OSError, ValueError) as exc:
            return None, f"{rel} is there and cannot be read as UTF-8 text ({exc})"
    kind = git(root, "cat-file", "-t", f"HEAD:{rel}")
    if kind is None:
        return None, None
    if kind.strip() != "blob":
        return None, f"{rel} at HEAD is a {kind.strip()}, not a file"
    out = subprocess.run(
        ["git", "-C", root, "cat-file", "blob", f"HEAD:{rel}"], capture_output=True
    )
    try:
        return out.stdout.decode("utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"{rel} at HEAD is not UTF-8 text ({exc.reason})"
```
```python
    config_text, unreadable = config_at_head(root, config_rel)
    ...
    notices = []
    if unreadable:
        notices.append(
            (
                config_rel,
                0,
                f"the pact relationship was not read: {unreadable}. Nothing "
                "about a pact moves this check's exit status, so this is a notice",
            )
        )
    pacts, notify, refusals = config.pact_declaration(config_text or "")
```
```python
HEADING_SPELLING = re.compile(r'#\{\d|startswith\(\(?"#')
```
```python
# The heading matcher for a base revision: a TEXT match, asked only of lines
# `headings` already took by `heading_level`, with the indentation that rule
# allows. It decides the wording, never whether the line is a heading.
LOOSE_HEADING = re.compile(r"^ {0,3}#{2,3}[ \t].*not verified", re.I)
```
```python
    (
        "skills/verify/scripts/unverified_check.py",
        "LOOSE_HEADING = re.compile",
    ): "a base revision's relaxed wording, asked only of lines heading_level took",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules the prompt named | exit 0, 436 passed |
| `bin/test tests/test_one_heading_rule_holds_to_commonmark.py tests/test_a_format_has_one_reader.py` | exit 0, 21 passed |
| `python3 skills/code-review/scripts/survivor_check.py --range 5623d728...7e0b1193` | exit 1, 33 places |
| the same with the paste-ready `survivors.md` under `--exempt` | exit 0, every survivor excused (33) |
| `bin/evidence-check --strict .` at the target, then at 5623d728 | exit 0 both; 15.35 s and 13.17 s |
| `bin/correction-check --range 5623d728...7e0b1193` | exit 0, no merge commit in the range |
| `python3 skills/implement/scripts/seal.py mode --check` | exit 0, folder and row agree |
| probe: plugin config reader against `vendored_config_rows` over eight shapes | six equal; a form feed and a U+2028 in a row differ |
| probe: lines the checker's and `unverified-check`'s shown lines read as headings where markdown-it reads none, every tracked `.md` | 0 and 0 |
| probe: `## B` inside an HTML block, a multi-line comment, a list item | the checker reads a level-2 heading in the first two; markdown-it reads none in any |
| probe: `routing.parse` over a doubled `Review`, a doubled `Planning`, a fenced `Review`, a `Review` in a second table | None, unanswered `planning`, a declaration, None |
| probe: `chain_check.read_record` with `--worktree` over an undecodable `seal/config.md` | raises `UnicodeDecodeError` |
| read, not executed by me: the CI logs of jobs 113099210318 and 113099209523 | the two failures under 🔴 1 and 🔴 2 |
| the full suite, the repository-wide lint and the typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 8's mechanism: which lines a reader hides (HTML blocks, comments) before it asks the heading rule | #872, which the frame filed for the seven live-line rules | the repository owner, who triages #872 |
