# Part 5 — `skills/verify/scripts/`, `bin/`, `.github/workflows/*.yml`

Tree: `chore/834-every-reader-and-record-is-inventoried` == origin/main 5623d728 (0.20.0 as shipped). Read only.
Paths below are relative to the repository root; `bg` = `skills/verify/scripts/broad_gate.py`.

## broad_gate in 0.20.0: what is observed, and what is still read from printed output

| Decision | How 0.20.0 gets it | Class |
|---|---|---|
| each arm passed / failed → `SEALED` / `NOT SEALED` | exit code of the subprocess (`bg:1434`, `bg:3474`) | observed |
| which test files failed at HEAD | the recorder's JSONL, written by pytest hooks in the row's own pytest (`bg:3484-3489`, `bg:1966`) | observed |
| `new` / `failing on base too` / `new? …` per file | the base run's JSONL record + that run's exit code (`bg:2169`, `bg:2186`) | observed |
| a session stopped part-way, tests with no file | the record's `end` line (`exitstatus`, `unplaced`) (`bg:2023-2032`) | observed |
| failing files when no record carries the HEAD key | **pytest's printed `FAILED path::` lines** (`FAILED_RE` `bg:340`, `failing_files` `bg:2043`) — fallback only; base not run, every file reads `new? not measured` | guess |
| the panel's `suite ✓ N passed · …` row, and `NO_SUMMARY` in the failure form | **pytest's printed summary line + wall clock** (`COUNTS_RE` `bg:344`, `suite_counts` `bg:2703`) | guess |
| the panel's `ledger ✓ ok · drifted · broken` row; the failure form's `total:` line | evidence-check's printed `total:` line (`LEDGER_RE` `bg:349`, `ledger_total` `bg:2747`) | owned (sibling's stdout) |
| cell written vs refused before the write, after `round_record.py seal` exits non-zero | the merged stdout/stderr line prefix `round-record: sealed` (`bg:3551-3553`) | owned (sibling's stdout) |
| whether the row may run at all | the row's TEXT: whole-value backticks / `$(…)` / trailing `&` (`bg:1330`, `bg:1356`) | guess |
| what `cmd.exe` is handed | a model of cmd.exe's lexer over the row's text (`bg:1655`) | guess |
| what CI runs for this base | `hygiene.yml` read by line regex + a declared copy of its guards (`bg:2310`, `bg:2388-2505`, `bg:2513`) | guess / owned |

What 0.20.0 removed: v0.18.0's `first_command` (`git show v0.18.0:…broad_gate.py` line 1820, a prediction of which part of the row runs pytest) and `FAILED_RE` as the primary source of failing files.

## Readers

| # | File | Unit | What it reads | Decides | Class | Unknown | Duplicates | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | bg | `below_floor` :192 | `sys.version_info` | exit 2 under 3.12 | observed | refused | `payload_meter.below_floor`, `seal_stamp.below_floor`, `round_record.py` floor (copied block) | Copied verbatim in four files by stated convention. |
| 2 | bg | `repo_root` :385 | `git rev-parse --show-toplevel` | refuse: not a repository | observed | refused | `unverified_check.repo_root` :1055 | Plumbing, exit code. |
| 3 | bg | `branch_name` :390 | `git symbolic-ref --short -q HEAD` | branch shown / left out | observed | passed | — | Detached HEAD → None, label only. |
| 4 | bg | `shipped_gate` :426 | `isfile` + `realpath` of `<root>/skills/verify/scripts/broad_gate.py` | redirect run to the tree's copy | observed | passed | — | Any repo shipping that path runs its copy. |
| 5 | bg | `plugin_version` :444 | `.claude-plugin/plugin.json` `version` | label on stderr / `gate` row | owned | passed | hygiene.yml:80-81 reads the same key | Unreadable → `?`. |
| 6 | bg | `gate_copy` :486 + `under` :455 | realpath containment; byte compare with the file named in `SPECSEAL_BROAD_GATE_INVOKED_AS` | whether the panel prints a `gate` row | observed | passed | — | Unreadable installed copy counts as different. |
| 7 | bg | `main` :3816 | env `SPECSEAL_BROAD_GATE_INVOKED_AS` (popped) | which copy the caller invoked | owned | passed | — | Variable set only by the gate's own redirect :3807. |
| 8 | bg | `resolve_base` :719 (+`short_commit` :670, `names_a_branch` :676) | `rev-parse --abbrev-ref <b>@{upstream}`, `refs/remotes/origin/<b>`, `check-ref-format --branch` | the commit every arm compares against | observed | mixed | `unverified_check.commit_of`/`merge_base` (resolve the same `--baseline` again in the child) | Resolves nowhere → exit 2; no remote counterpart → the spelling as given. |
| 9 | bg | `moved_line` :590 (+`a_runner_could_hold` :702) | `rev-list --count --left-right` split on whitespace; `check-ref-format` | wording of the moved-base line | observed | passed | — | Output not two fields → counts omitted. |
| 10 | bg | `seal_home` :774 | `isdir(<root>/seal)`, `rev-parse --git-common-dir` | refuse: not opted in | observed | refused | `hooks/optin.py#home_at` (used by unverified_check) | Second resolver of the root, not loaded from hooks. |
| 11 | bg | `broad_command` :798 | `seal/config.md` `Broad gate` row via `hooks/config.py#config_rows` | the command to seal over | owned | refused | — (delegated to the one table reader) | Empty value → treated as no row. |
| 12 | bg | `names_this_row` :857 + `FIRST_CELL` :814 | first cell, up to the first `\|`, of a line the table reader refused | whether a malformed line is "this gate's row" | guess | refused | — | Reads a line that does not parse "the way a cell was read before the escape existed". |
| 13 | bg | `missing_row` :1016 (+`refusal` :817, `refused_broad_row` :883, `hides_this_row` :863, `rows_read` :831) | `hooks/config.py#refusal` (refused, below, stopper) | which of five refusal sentences | owned | refused | — | Exit 2 either way; position-not-identity fix #430. |
| 14 | bg | `hidden_row_at` :932 (+`fenced_row_at` :902, `commented_row_at` :921, `fence_left_open` :985) | `hooks/config.py#hidden_lines`, `#fence_map` | fence vs comment vs unclosed-fence sentence | owned | refused | — | Message choice only; exit 2 regardless. |
| 15 | bg | `not_as_written` :1356 + `wholly_substituted` :1330 | the row value's text | refuse backticks / `$(…)` wrapping the whole value / trailing single `&` | guess | passed | — | Three forms enumerated; every other shell shape runs (`;`, `\|` allowed by design). |
| 16 | bg | `cmd_exe_reads` :1542 | `os.name`, env `COMSPEC` basename | whether the row is rewritten | observed | passed | — | Unset COMSPEC → cmd.exe. |
| 17 | bg | `command_names_backslashed` :1655 (+`handed_to_shell` :1562, `CMD_BUILTINS` :1606, `as_cmd_expands` :1509, `CMD_VARIABLE` :1506) | the row text, modelled as cmd.exe's lexer | which `/` become `\` | guess | passed | — | Docstring lists unmodelled shapes (`call`, `start`, `%V:~%`, `cd` earlier in row). |
| 18 | bg | `run` :1442 / `Check.failed` :1434 | subprocess exit code of each arm | SEALED vs NOT SEALED | observed | refused | — | Every arm's verdict is an exit code. |
| 19 | bg | `draft_env` :1793 | presence of env `GITHUB_EVENT_PATH` | whether to hand chain_check a fake draft payload | observed | passed | `chain_check.py` reads draft from the same variable | Writer of a payload the next reader trusts. |
| 20 | bg | `exemptions` :1814 | glob `seal/specs/*/survivors.md` | `--exempt` args | owned | passed | hygiene.yml:258-261 (same glob in bash) | Two copies of one list. |
| 21 | bg | `read_record` :1966 | recorder JSONL under `records/`: first line `key`; `kind`, `path`, `outcome`, `exitstatus`, `unplaced` | sessions, failing files, collected, unplaced, unended | observed | mixed | — | Foreign key: skipped whole. Non-object lines counted in `skipped`, which nothing reads (:2010, :2015). |
| 22 | bg | `RAN_TO_ITS_END` :1963 | `end` line `exitstatus` ∈ {0,1,5} | session ran to its end vs `unended` | observed | mixed | — | `pytest.exit(1)` and `-x` stops pass as ended; named limit. |
| 23 | bg | `base_word` :2169 | base `RunRecord` + base run exit code | `new` / `failing on base too` / four `new?` words | observed | mixed | — | No session → `new?`; not collected and exit 0 → `new`. |
| 24 | bg | `compare_at_base` :2186 | `git worktree add --detach` exit | NOT_CHECKED_OUT for every file | observed | passed | — | Base unavailable → `new?`, run continues. |
| 25 | bg | `failing_files` :2043 + `FAILED_RE` :340 | pytest's printed `FAILED <path>::` lines in `suite.txt` | which files to list when no record at HEAD | guess | passed | — | Fallback only; pattern changed in #813 (space in path). |
| 26 | bg | `suite_counts` :2703 + `COUNTS_RE` :344 | last printed line with counts followed by `in N.Ns` | panel `suite` row; failure form `NO_SUMMARY` | guess | passed | `.github/scripts/release_seal.py#suite_counts` :229 reads the same counts from JUnit XML | Not replaced by the recorder in 0.20.0; no match → `exit N`. |
| 27 | bg | `ledger_counts` :2733 + `LEDGER_RE` :349 | evidence-check's `total: N ok · D drifted · B broken` | panel `ledger` row | owned | passed | #28 (same line, other rule) | Sibling's prose line, regex-coupled. |
| 28 | bg | `ledger_total` :2747 | last line starting `total:` of evidence-check output | appended to the failure form | owned | passed | #27 | Two readers of one printed line. |
| 29 | bg | `gate` :3551-3553 | merged child output: any line `startswith("round-record: sealed")` | which of two exit-2 sentences | owned | passed | — | Exit code cannot discriminate (docstring :100-109); a printed word does. |
| 30 | bg | `job_steps` :2310 (+`JOB_RE` :2296, `STEP_RE` :2299, `unquote` :2302) | `.github/workflows/hygiene.yml` as text, `- name:` lines of job `release` | the step list CI runs | guess | passed | `tests/test_ci_gives_the_checks_what_they_need.py#jobs` (same gap) | YAML by regex; trailing `# comment` joins the name; anything else → `[]`. |
| 31 | bg | `workflow_text` :2609 | open the workflow, None on OSError/ValueError | whether coverage is computed at all | observed | passed | — | Non-UTF-8 file = no workflow. |
| 32 | bg | `PARTITION` :2388 + `ONLY_AT_MAIN` :2500 + `SKIPPED_AT_MAIN` :2485 (+`steps_for` :2531, `skipped_at_main` :2566, `unanswered` :2628, `coverage_line` :2642) | declared copy of the step names and their `base_ref` guards | arms skipped; `CI also N more steps` | owned | mixed | hygiene.yml guards :66,:117,:136,:348,:251,:304 | Held to the workflow by a test; an unclassified step is named, not refused. |
| 33 | bg | `base_is_main` :2513 | the `--base` spelling, one leading `origin/` stripped, `== "main"` | which arms run; the CI count | guess | passed | hygiene.yml `${{ github.base_ref }}` guards | Predicts `github.base_ref` from typed text; `refs/heads/main` reads as not-main. |
| 34 | bg | `round_count` :2757 + `ROUND_RE` :240 | filenames `rounds/round-N.md` | `rounds` row count | owned | passed | — | Other names ignored. |
| 35 | bg | `sealed_record` :2787 | `round_record.where`/`seal_home`, `chain.table_rows` | the record the panel reads | owned | passed | — (delegated) | Any exception or SystemExit → None. |
| 36 | bg | `rounds_rows` :2895-2902 | `Needs a fix` cell, `visible().strip().lower().startswith("yes")` | ` · capped` | owned | passed | `chain_check.py:3603` (`yes_or_no`/`says_reopened`, strict), `round_record.py:2062` | Prefix read here; chain_check refuses a bare `yes` that this reads as capped. |
| 37 | bg | `rounds_rows` :2904-2912 | `chain.verdict_of` per verdict row | count of deferred rows | owned | passed | — (delegated) | One judge reused. |
| 38 | bg | `deferred_home` :2828 + `HOME_TOKEN` :2823 + `HOME_END` :2825 | the prose after `deferred` in a person's verdict cell | the homes after `→` | guess | passed | `chain_check.verdict_of` :1653 decides homed vs `(no home)` on the same cell by its own rule | First `#N` or path-with-extension, else words up to a dash. |
| 39 | bg | `pull_request` :2923 | `PR` row via `chain.PR_RE` | `#N` on the `item` row | owned | passed | `chain_check.declared_pull_head` :1477 | `not yet opened` → None. |
| 40 | bg | `item_value` :2939 | work item directory name, text before first `-` | the `item` id | owned | passed | `unverified_check.work_item_of` :1499; `seal_stamp.label` :947 | No `-` → whole name. |
| 41 | bg | `gate` :3376-3378 | `hooks/routing.py#item_dir(root, branch)` | which item `seal --check` asks (preflight) | owned | passed | chain arm reads declarations at HEAD instead (docstring :132-136) | None/two/detached → not asked, one stderr line. |
| 42 | bg | `gate` :3362-3367 | `--record` isdir; `--preflight` with `--record` | refuse | observed | refused | — | Argument checks. |
| 43 | bg | `uncommitted_line` :3664 | `git status --porcelain -- <rel>` non-empty | the `not committed` line | observed | passed | — | Porcelain v1, emptiness only. |
| 44 | bg | `common_dir` :3685 | `git rev-parse --git-common-dir` | where the values file goes | observed | passed | `seal_home` #10 asks the same | None → VALUES_UNWRITTEN, still sealed. |
| 45 | bg | `signal` :3712 + `SESSION_VAR` :3622 | env `CLAUDE_CODE_SESSION_ID` | which session's hook draws the stamp | guess | passed | — | Undocumented harness variable (comment :3617-3621); absent → `none/`, no hook reads it. |
| 46 | pytest_record/specseal_pytest_record.py | module :97-98, `pytest_configure` :299 | env `SPECSEAL_RECORD_KEY` (popped), `SPECSEAL_RECORD_DIR` | whether this process records | owned | passed | — | No key → no file → gate reads "no record", the strict side. |
| 47 | pytest_record | `_node_path` :115, `_carry_the_path` :122, hookwrappers :137-153 | `item.path` / `fspath`; `collector is collector.session` | the path set on each report | observed | passed | — | Hook raised → no attribute, pytest's own error stands. |
| 48 | pytest_record | `Recorder.path_of` :169 | report attribute; else same worker's last report with same nodeid, not teardown; `isdir` | path written, or counted `unplaced` | observed | mixed | — | Crash attribution is an inference: "a worker runs one test at a time". |
| 49 | pytest_record | `pytest_runtest_logreport` :253, `pytest_collectreport` :268, `pytest_sessionfinish` :283 | `report.outcome`, `when`, `wasxfail`, `report.failed`, `exitstatus` | the lines written | observed | passed | — | `rootdir`, `invocation_dir`, `pytest`, `nodeid`, `when` are written and never read by bg. |
| 50 | skills/verify/scripts/arm_check.py | `_refuse_unknown` :390 + `CLASSIFIED`/`ONLY_ON_SOME_PYTHONS` :306-332 | `ast.walk` node type names | refuse an unclassified node type | observed | refused | — | Totality held against `ast`'s class tree by a test. |
| 51 | arm_check.py | `_node_arms` :445, `_members` :405 | ast shapes (`BoolOp`, `Tuple`, `MatchOr`, guards) | the arm list | observed | refused | — | Unhandled listed shape raises. |
| 52 | arm_check.py | `_lines` :618 + `_LINE_END` :615 | source split at `\r\n\|\r\|\n` | splice offsets | observed | passed | `unverified_check.gfm_lines` (same three terminators) | Mirrors the tokenizer's rule, not `splitlines`. |
| 53 | arm_check.py | `mutate` :694 | `arm.note` strings (`bare except`, `guard…`), `arm.shape` | mutation or NoMutationDefined | owned | refused | — | Its own note vocabulary read back. |
| 54 | arm_check.py | `run_arms` :948-963 | baseline `--tests` exit code / timeout / OSError | NoBaseline (exit 2) | observed | refused | `mutation_check.mutation_run` :333-344 | Exit 5/4 no longer read as killed (#703). |
| 55 | arm_check.py | `run_arms` :1012-1035 | per-mutation `returncode != 0` | killed / survived / no verdict | observed | mixed | `mutation_check.run_cases` :273 | Timeout/OSError → no verdict, listed. |
| 56 | arm_check.py | `restore` :846 | sha256 of the file after write-back | stop the run | observed | refused | used by mutation_check | — |
| 57 | arm_check.py | `clear_bytecode_cache` :790 | `sys.pycache_prefix`/`PYTHONPYCACHEPREFIX`; filenames `<stem>.*.pyc` | which `.pyc` to delete | observed | passed | used by mutation_check | Name-prefix match on `stem.`. |
| 58 | arm_check.py | `main` :1254 | `shlex.split(--tests)` run without a shell | the argv | guess | passed | `mutation_check.main` :428 | `&&`, pipes, `cd` become literal arguments. |
| 59 | skills/verify/scripts/mutation_check.py | `mutated` :154 | count of literal OLD in the file | refuse 0 or >1, empty, OLD==NEW | observed | refused | — | Exact-once is the whole rule. |
| 60 | mutation_check.py | `mutation_run` :305 | UTF-8 decode of the file | refuse | observed | refused | — | — |
| 61 | mutation_check.py | `run_cases` :273 + `mutation_run` :334-353 | `proc.returncode`; baseline red → NO_BASELINE; `detail.rfind("(exit ")` | verdict and exit code | observed | refused | #54, #55 | Reads back its own detail string for the exit. |
| 62 | mutation_check.py | `strategy` :176 | `os.name` | process group vs direct child kill | observed | passed | — | — |
| 63 | mutation_check.py | `mutation_run` :367-384 | on-disk sha256 vs original | NotRestored (exit 2) | observed | refused | #56 | — |
| 64 | mutation_check.py | `main` :428 | `shlex.split(--tests)` | the argv; empty → error | guess | passed | #58 | — |
| 65 | skills/verify/scripts/deferral_check.py | `read_events` :89 | another repo's workflow `on:` by regex (three forms) | pre-merge vs too late | guess | passed | — | Empty set → counted as resolving, "trigger unread" (:191-193). |
| 66 | deferral_check.py | `runners_in` :121 + `RUNNERS` :37 | any non-comment line matching a runner word | the check "resolves" | guess | mixed | `session_cost.FAMILIES` :128 (another runner list) | Unlisted runner → exit 1; `pip install pytest` line → resolves. |
| 67 | deferral_check.py | `inspect` :197-202 + `other_ci_files` :148 | presence of six fixed CI paths + runner words | resolves, "pipeline" | guess | passed | — | Assumes those systems run on PR; trigger never read. |
| 68 | deferral_check.py | `inspect` :204-208 | `.pre-commit-config.yaml` + runner words | "local only" | guess | passed | — | Line text only. |
| 69 | skills/verify/scripts/unverified_check.py | `gfm_lines` :165 + `GFM_LINE_RE` :162 | line ends LF/CR/CRLF only | every index into a record | owned | passed | `evidence_check.py#gfm_lines` (vendored copy, held equal by a test) | The one split rule for markdown readers. |
| 70 | unverified_check.py | `split_row` :194 | `\|`-split with `\\\|` escape | cells or None | owned | passed | `hooks/config.py` row split, `chain_check` table rows (other parts) | — |
| 71 | unverified_check.py | `fence_opener` :265 / `fence_closes` :364 + `FENCE_RE` :143 | CommonMark 4.5 subset (≤3 spaces, ```/~~~) | fence state | owned | passed | `hooks/blocks.py#FENCE`, `hooks/config.py#FENCE`, `close_issues_on_release.py#FENCE`, `round_record.py#fenced_after` + vendored copy (docstring :301-348) | Docstring enumerates the copies kept on purpose. |
| 72 | unverified_check.py | `comment_scan` :225 / `strip_comments` :256 | `<!--`/`-->` across lines | blanks comment text | owned | passed | `hooks/blocks.py#walk` (line-start comments); `_liveness` (#73) has its own comment state | Unclosed comment blanks to end. |
| 73 | unverified_check.py | `live_lines` :599 (+`_liveness` :440, `_partner_ahead` :579, `_paragraph_ends_at` :516, `BACKTICKS` :124) | fence + comment + code-span state, two span readings ANDed | whether a line is live | guess | mixed | used by `settle.py#coordinates`, `fold_ledger.py`/`gather_changelog.py#live_markers` | Approximates a block model; disagreement parks the line. Indented code block not modelled. |
| 74 | unverified_check.py | `fence_spans` :381, `closed_fence_lines` :411, `blank_fences` :423, `readable` :683 | fence spans | blanked / skipped lines | owned | passed | `readable` used by chain_check, round_record, survivor_check | Unclosed fence: blanked to end here, read by row readers. |
| 75 | unverified_check.py | `check_text` :824 + `sections` :811 + `parse_section` :698 (+`visible` :215, `PLACEHOLDER`, `CLOSED`, `HEADER`) | one exact `## Not verified`, exact header, 2-cell rows, ✅ prefix | open/closed rows or errors (exit 1) | owned | refused | — | Strict in the working tree; `none — …` first line accepted. |
| 76 | unverified_check.py | `check_text(…, LOOSE_HEADING, strict_header=False)` :1673, :1378 + `LOOSE_HEADING` :158 | base revision: any `##`/`###` heading containing "not verified", header starting `Item` | base row count | guess | mixed | — | Legacy spellings tolerated; unreadable base → notice, exit 0. |
| 77 | unverified_check.py | `overviews` :870 + `reference_rule` :933 + `references_at` :906 | os.walk minus `SKIP_DIRS`, `hooks/config.py#reference_roots`, `hooks/optin.py#home_at` | which overviews are read | owned | passed | `overviews_at` #78 keeps the same skip rule | Copy without `hooks/` prunes nothing. |
| 78 | unverified_check.py | `overviews_at` :1145 | `git ls-tree -r --name-only <base>` split on newlines | overviews present at the base | observed | passed | `tree_at` :1322 (same command) | Not `-z`: a C-quoted path never matches its working-tree spelling. |
| 79 | unverified_check.py | `commit_of` :1066, `resolves` :1085, `merge_base` :1098 | `rev-parse --verify --quiet`, `merge-base <ref> HEAD` exit codes | exit 2 | observed | refused | bg #8 resolves the same ref first | — |
| 80 | unverified_check.py | `folded_items` :1191 + `FOLD_MARKER` :117 | live lines of top-level `docs/*.md`, `^<!-- specs/(\S+) -->$` | a removed overview is a fold, not a deletion | owned | mixed | `fold_ledger.py#marker`/`#is_marked`, `gather_changelog.py#marker`, `fold_check.py` marker readers | A live marker anywhere in `docs/*.md` excuses; a parked one does not. |
| 81 | unverified_check.py | `todo_open_rows` :1263 + `DRAINED_RE` :1260 + `TODO_SEPARATOR_RE` :1259 | evidence-todo.md: a live non-table line whose first word is `drained`; rows without ✅ | open rows (or none) | owned | mixed | callers `settle.py#open_rows`, `fold_ledger.py#open_rows` (one judge) | A prose word on any live line closes the whole file. |
| 82 | unverified_check.py | `retired_by_rule` :1392 (+`open_record_rows` :1358, `tree_at` :1322) | tree at base, no `spec.md`, no open rows | a removed dir is "retired by the rule" | owned | mixed | one judge, called by chain_check, survivor_check, settle | `ls-tree` failure → `[]` → not retired (strict). |
| 83 | unverified_check.py | `wrote_a_spec` :1423 | `git log --full-history -1 --format=%H <ref> -- <dir>/spec.md` | spec ever written | observed | mixed | — | git failure → "wrote one" (strict); shallow clone → "never" (passed). |
| 84 | unverified_check.py | `settled_root` :1462 | path basename `specs` under `seal`, empty or absent | exit 0 "settled" | owned | passed | — | Only that one path is excused. |
| 85 | unverified_check.py | `main` :1670-1672 + `show` :1509 | `git show <base>:<rel>` exit code | compare rows, or skip | observed | passed | — | Any `show` failure is read as "new file", comparison silently skipped. |
| 86 | unverified_check.py | `annotate` :1519 | env `GITHUB_ACTIONS` | `::error` annotation vs plain line | observed | passed | — | Output format only. |
| 87 | skills/verify/scripts/session_cost.py | `parse_time` :153 | transcript `timestamp`; naive read as UTC | every duration | guess | passed | — | Unparseable → None, row dropped; mixed zones → wrong at exit 0 (stated). |
| 88 | session_cost.py | `load` :898 | transcript JSONL: `message.content[]` `tool_use`/`tool_result`, `id`, `input.command`, `usage` | calls and turns | guess | passed | `payload_meter._rows`/`spawns_in` (second transcript reader) | Undocumented harness format; non-JSON and odd rows skipped silently. |
| 89 | session_cost.py | `message_key` :788 | `message.id` → `uuid` → `row-N` | turn identity, token dedup | guess | passed | — | Fallback double-counts split messages (stated). |
| 90 | session_cost.py | `count` :743 | `usage` values; bool / non-number / non-finite → 0 | token arithmetic | guess | passed | — | — |
| 91 | session_cost.py | `tool_name` :878, `spawn_labels` :855, `DELEGATING` :834 | `name == "Agent"`, `subagent_type`, `description` | spawn cycles | guess | mixed | `payload_meter.spawns_in` | Zero found → count printed, table refused (`report_spawns` :2182). |
| 92 | session_cost.py | `family` :709 + `FAMILIES` :128 | the recorded Bash command text | test / lint / build / git / read / other | guess | passed | `deferral_check.RUNNERS` | Unknown runner → `other`; slowest unnamed command printed. |
| 93 | session_cost.py | `without_heredoc_bodies` :230 + `HEREDOC` :227 | `<<` operators, delimiters | text removed before classifying | guess | passed | — | Lowercase unquoted delimiter left as command text. |
| 94 | session_cost.py | `without_comments` :300, `shell_words` :390, `command_words` :360 | shlex POSIX walk with punctuation, RESERVED, assignments | command positions | guess | mixed | — | Tokeniser refusal → words so far, then anchored regex. |
| 95 | session_cost.py | `runs_git` :447 | command words' basename `git`/`gh` | `git` family | guess | passed | — | Wrappers (`timeout`, `env`) not looked through. |
| 96 | session_cost.py | `only_reads` :637 + `writes` :595 + `READ_WORDS`/`NEUTRAL_WORDS`/`HIDDEN_FROM_THE_WALK`/`SEPARATOR_THEN_REDIRECTION`/`FIND_WRITES` | command words, flags, redirections | `read` family | guess | passed | — | Errs to `other`; sed/awk programs not read. |
| 97 | session_cost.py | `strip_pipe` :1028 | split at first unquoted-looking `\|` | repeat grouping | guess | passed | — | Quotes not honoured. |
| 98 | session_cost.py | `subagent_transcripts` :1443 | `<session>/subagents/**.jsonl` | which files are the run's segments | guess | passed | `payload_meter.calibration_of` (via this) | Harness layout; absent → []. |
| 99 | session_cost.py | `opening_stamp` :1465 | first parseable `timestamp` | join key | guess | passed | — | — |
| 100 | session_cost.py | `resume_cuts` :1528 + `COORDINATOR_MESSAGE` :1525 | `type=user`, `isMeta`, content starting with a harness sentence | where a resumed agent's file is cut | guess | passed | — | Reworded sentence → no cut; idle gap named instead. |
| 101 | session_cost.py | `join_segments` :1591 + `JOIN_TOLERANCE_S` :852 | opening stamp within 1.0 s of an `Agent` result | which spawn a segment is | guess | passed | — | Unmatched → "named by nobody", counted. |
| 102 | session_cost.py | `token_totals` :1857 | `usage` max per message key | token block | guess | passed | — | — |
| 103 | session_cost.py | `segment_kind` :2368 + `SEGMENT_BARS` :2361 | `subagent_type` after last `:` | bar and grade | guess | passed | `docs/review-handoff-protocol.md` bars (test holds); `payload_meter.short_name` :461 | Unknown kind → ungraded, counted. |
| 104 | session_cost.py | `newest` :2780 | `~/.claude/projects/<slug>` with `[^A-Za-z0-9-]`→`-`, newest mtime | `--latest` transcript | guess | passed | `hooks/worktree-guard.py#project_slug` (named, not shared) | — |
| 105 | session_cost.py | `open_log` :2854 + `run_gh` :2834 | `gh issue list --json number,state` exit code and JSON | log state | observed | mixed | — | Unreadable → exit 0 nothing posted; two open → exit 1. |
| 106 | session_cost.py | `post` :2982-2992 | `gh issue comment` exit code | posted or exit 1 | observed | refused | — | — |
| 107 | skills/verify/scripts/payload_meter.py | `below_floor` :103 | `sys.version_info` | exit 2 | observed | refused | #1 | — |
| 108 | payload_meter.py | `frontmatter` :215 | agent file YAML frontmatter by regex: `name:`, `skills:` block / flow forms | which skills an agent loads | guess | passed | — | The harness parses the same YAML; unknown spelling → no skills, silently. |
| 109 | payload_meter.py | `agents_in` :357 | `agents/*.md`, `name` else filename | agents measured | owned | passed | — | — |
| 110 | payload_meter.py | `composition` :328 | `skills/<s>/SKILL.md`, `~/.claude/skills/<s>/SKILL.md` shadow, CLAUDE.md pair | the payload rows | guess | passed | — | Models how the harness assembles a prefix; missing file → `missing` row. |
| 111 | payload_meter.py | `heading_starts` :256 + `HEADING` :131 | `##`/`###` outside fences (unverified_check rule) | section split | owned | passed | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings` | — |
| 112 | payload_meter.py | `spawns_in` :403 + `AGENT_ID` :132 | `agentId: <hex>` in the `Agent` tool result's text | spawn → transcript id | guess | mixed | #91 | No id → `unread` listed. |
| 113 | payload_meter.py | `first_prefix` :442 | first assistant `usage` sum | measured prefix | guess | passed | — | — |
| 114 | payload_meter.py | `calibration_of` :466 | `agent-<id>.jsonl` names; `short_name` rsplit `:` | per-agent prefixes | guess | refused | #103 (same rsplit) | Baseline agent absent → CalibrationError, exit 1. |
| 115 | payload_meter.py | `measure` :604 + `_ratio_from_baseline` :529 + `_spawn_of` :539 + `_same_spawn_over_other_bytes` :571 | an earlier `--json` output | lent ratios, notes | owned | mixed | — | Bad JSON → uncaught traceback; missing keys → ignored. |
| 116 | payload_meter.py | `delta_against` :753-754 | `basis` string `startswith("measured")` | how the total delta is taken | owned | passed | — | Its own prose label read back as a flag. |
| 117 | skills/verify/scripts/seal_stamp.py | `below_floor` :111 | `sys.version_info` | exit 2 | observed | refused | #1 | — |
| 118 | seal_stamp.py | `read_chart` :323, `CHART` :357 | `seal-mark.txt`: 28 lines × 28 of `.M`, `M` inside the field | the disc's mark | owned | refused | — | Raised at import: bg's `load` lets ValueError through as a traceback, not exit 2. |
| 119 | seal_stamp.py | `check_scale` :272 | scale float, NaN | refuse | owned | refused | — | — |
| 120 | seal_stamp.py | `ref_is_commit` :741 + `HEX_REF` :712 | ref spelled 4-40 hex, prefix-related to base | whether the ref is printed | guess | passed | one judge for `sealed_names` and bg `panel` | A hex-named branch prefixing the base reads as a commit. |
| 121 | seal_stamp.py | `text_lines` :558, `VALUE_MARKS` :541 | value's first char + space; `TITLE_ROW` | styling | owned | passed | — | Panel's own characters. |
| 122 | seal_stamp.py | `pick_shape` :776, `is_terminal` :790 | stream `encoding`, `isatty()` | draw, and which form | observed | passed | — | — |
| 123 | seal_stamp.py | `session_key` :835 | session id basename, `.`/`..`/empty | values directory | owned | passed | — | — |
| 124 | seal_stamp.py | `read_values` :873 | values JSON: object, `rows` list of 2-string lists or null, numeric `scale` | refuse or draw | owned | refused | — | — |
| 125 | seal_stamp.py | `pending` :915, `claim` :931, `drawn_from` :1051 | `.json` / `.drawn.json` suffixes, leading `.`, `os.replace` | pending, drawn once | owned | refused | — | Drawn file → exit 2. |
| 126 | seal_stamp.py | `label` :947 | `"branch" in values` | old or new label format | owned | passed | — | Version tolerance between tree gate and installed hook. |
| 127 | bin/{17 POSIX wrappers} | e.g. `bin/broad-gate`:11-12 | `$(dirname "$0")`, `exec python3` from PATH | which interpreter | observed | passed | — | No version read; floor exists in 3 of the 8 verify scripts (+round_record). |
| 128 | bin/*.cmd (17) | e.g. `bin/broad-gate.cmd`:9-15 | `where /q py` errorlevel | `py -3` vs `python` | observed | passed | — | — |
| 129 | bin/test, bin/test.cmd | `bin/test`:31-34, `test.cmd`:8-11 | `[ ! -f run_tests.py ]` / `if not exist` | refuse exit 2 | observed | refused | — | Only wrapper that checks its target. |
| 130 | .github/workflows/hygiene.yml | steps :66, :117, :136, :348 (`!= "main"`), :251, :304 (`= "main"`) | `${{ github.base_ref }}` | step skipped (exit 0) | observed | passed | bg #32, #33 | Six copies of the release/feature split. |
| 131 | hygiene.yml | step :70-79 | `git diff --name-only base...HEAD \| grep -E '^(skills\|agents\|hooks\|templates\|bin\|\.claude-plugin)/'` | "what ships changed" | observed | passed | `tests/test_the_release_check_watches_what_ships.py` | Not `-z`; a C-quoted path misses the anchor. |
| 132 | hygiene.yml | step :80-97 | `plugin.json` `version` at base vs HEAD via `json` | refuse unchanged version | owned | refused | bg #5 | KeyError / bad JSON fails the step too. |
| 133 | hygiene.yml | step :258-263 | glob `seal/specs/*/survivors.md` | `--exempt` args | owned | passed | bg #20 | — |
| 134 | hygiene.yml | step :408-413 | `grep -cx 'README.md'` / `'README.ko.md'` on name-only diff | warning | observed | passed | — | Never fails. |
| 135 | .github/workflows/test.yml | `ledger` job :155-164 | evidence_check exit code: ≥2 fail, 1 warn | job red or warning | observed | mixed | bg LEDGER arm (`--strict`, any non-zero fails) | Reads exit code, never text (comment :143). |
| 136 | .github/workflows/publish-release.yml | `seal` job `if:` :73 | `needs.publish.outputs.created == 'true'` | whether the seal job runs | owned | passed | — | Written by `publish_release_note.py#write_output`. |

## Size and growth

| Source file | Lines now | Lines at v0.18.0 | Commits v0.18.0..HEAD |
|---|---|---|---|
| skills/verify/scripts/broad_gate.py | 3849 | 3354 | 6 |
| skills/verify/scripts/pytest_record/specseal_pytest_record.py | 307 | — | 2 |
| skills/verify/scripts/arm_check.py | 1303 | 1303 | 0 |
| skills/verify/scripts/mutation_check.py | 486 | 486 | 0 |
| skills/verify/scripts/deferral_check.py | 281 | 281 | 0 |
| skills/verify/scripts/unverified_check.py | 1840 | 1840 | 0 |
| skills/verify/scripts/session_cost.py | 3242 | 3241 | 1 |
| skills/verify/scripts/payload_meter.py | 967 | 967 | 0 |
| skills/verify/scripts/seal_stamp.py | 1083 | 1069 | 1 |
| skills/verify/scripts/seal-mark.txt | 28 | — | 1 |
| bin/* (34 files, 12-35 lines each) | 12-35 | same | 0 |
| .github/workflows/hygiene.yml | 414 | 413 | 2 |
| .github/workflows/test.yml | 191 | 141 | 3 |
| .github/workflows/publish-release.yml | 138 | 122 | 3 |
| .github/workflows/close-issues-on-release.yml | 71 | 71 | 0 |
| .github/workflows/label-merged-on-release-branch.yml | 49 | 49 | 0 |

Distinct readers counted: **136** rows (bg 45, pytest recorder 4, arm_check 9, mutation_check 6, deferral_check 4, unverified_check 18, session_cost 20, payload_meter 10, seal_stamp 10, bin 3, workflows 7). By class: observed 51, owned 44, guess 41. Unknown input: passed 86, refused 30, mixed 20.

## Observations

- **broad_gate's six commits since v0.18.0 are all one reader moved four times**: `edee5ca2` (#758), `b3319a0f` (#761/#787), `db250692` (#789, #812/#814), `6de64c19` (#825, #807, #813, #816, #818/#846), `ec09faf9` (#849/#851), then `149ca9ec` (#832, panel). +495 lines; the recorder (307 lines) is new.
- **The recorder replaced the file-level verdict, not the counts.** `suite_counts` (`bg:2703`, `COUNTS_RE` `bg:344`) still decides the panel's `suite ✓ …` row and the failure form's `NO_SUMMARY` from pytest's printed line; the record already holds every outcome (`bg:2033-2039`). `.github/scripts/release_seal.py:229` reads the same counts from JUnit XML — two mechanisms for one number.
- **`FAILED_RE` survives as a fallback** (`bg:340`, `bg:3491`) and changed in #813 (a space in a path); it labels files only, the base is not run, and every word is `new? not measured`.
- **The gate still predicts shell behaviour from the row's text in two units**: `not_as_written` (`bg:1356`, three refused forms, everything else passes) and the cmd.exe lexer model `command_names_backslashed` (`bg:1655`, ~135 lines, unmodelled shapes listed in its docstring).
- **A silently dropped count**: `read_record` increments `RunRecord.skipped` for lines that are not JSON objects (`bg:2010`, `bg:2015`) and no code reads `skipped`.
- **One cell, two judgments**: `rounds_rows` reads `Needs a fix` by `startswith("yes")` (`bg:2901`); `chain_check.py:3603-3635` reads the same cell with `yes_or_no`/`says_reopened` and refuses a bare `yes` that the panel prints as `capped`.
- **One prose cell, two rules**: `deferred_home` (`bg:2828`) pulls a home out of a person's verdict text with `HOME_TOKEN`; `chain_check.verdict_of` (`chain_check.py:1653`) decides homed vs `(no home)` on the same cell independently.
- **The release/feature split is written six times in hygiene.yml** (`:66, :117, :136, :348, :251, :304`) and mirrored in bg by `ONLY_AT_MAIN`/`SKIPPED_AT_MAIN`/`base_is_main` (`bg:2485-2528`), which guesses `github.base_ref` from the typed `--base` spelling. Held together by `tests/test_the_gate_names_every_step_ci_runs.py`, not by one source.
- **`job_steps` reads YAML by line regex** (`bg:2296-2366`) with a stated trailing-comment gap shared with `tests/test_ci_gives_the_checks_what_they_need.py#jobs`.
- **The verify cluster of unverified_check (0 commits since v0.18.0) is the shared markdown kernel**: `gfm_lines`, `fence_opener`/`fence_closes`, `live_lines`, `readable`, `todo_open_rows`, `retired_by_rule` are imported by settle, fold_ledger, gather_changelog, chain_check, survivor_check, payload_meter. `live_lines` (`:599`) is the one unit in it that approximates CommonMark (two readings ANDed).
- **`todo_open_rows` closes a whole file on a prose word**: any live non-table line whose first word is `drained` (`unverified_check.py:1260`, `:1303`).
- **git output read without `-z`**: `overviews_at`/`tree_at` (`unverified_check.py:1153`, `:1339`) and hygiene.yml `:70`, `:409` split `--name-only` on newlines; git C-quotes unusual paths there.
- **session_cost (20 readers) and payload_meter read the same undocumented transcript format twice** (`session_cost.load` :898, `payload_meter._rows`/`spawns_in` :377/:403), including a harness sentence (`COORDINATOR_MESSAGE` :1525) and tool-result prose (`agentId:` `payload_meter.py:132`). Both are report-only; nothing gates on them.
- **Interpreter discovery is unchecked in `bin/`**: every POSIX wrapper `exec python3` (`bin/broad-gate:12`). broad_gate, payload_meter, seal_stamp carry the 3.12 floor; session_cost has none yet calls `dt.UTC` (3.11, `session_cost.py:189`) and `itertools.pairwise` (3.10, `:1584`).
- **A refusal that is not an exit 2**: `seal_stamp.read_chart` raises at import (`seal_stamp.py:357`), and `bg.load` (`bg:356-363`) does not convert that ValueError to `Refused`, so a malformed `seal-mark.txt` ends broad-gate in a traceback before any arm runs.
