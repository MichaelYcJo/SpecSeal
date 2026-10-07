# Part 2 — hooks/ (the rest): readers inventory (#834)

Scope: every file under `hooks/` except `cmdline.py`, `cmdline_base.py`, `tokens.py`, `one_heredoc.py`,
`worktree-guard.py`, `worktree_consent.py`, `commitgate.py`, `commit-review-gate.py`, `gate.py`, `dispatch.py`.
Tree: `chore/834-every-reader-and-record-is-inventoried` (== `5623d728`, 0.20.0). Read from the code, not the docstrings.

`console.py` holds no reader (it reconfigures streams only). `hooks.json` holds no reader: every event is one
`python3 dispatch.py <group> || py -3 dispatch.py <group>` line; which hook reads which payload field is the
appendix after the Readers table (groups from `hooks/dispatch.py:80-123`).

## Readers

| # | File | Unit | What it reads | Decides | Class | Unknown | Duplicates | Note |
|---|------|------|---------------|---------|-------|---------|------------|------|
| 1 | answer-write.py | `main` | payload `tool_name`, `tool_input.command`, `tool_use_id`, `session_id` | whether/where to record a call's consent tokens | observed | passed | answer-clear.py#main | Harness JSON fields; the token reading itself is `tokens.given` (other part), shell text → guess there. |
| 2 | answer-clear.py | `main` | same four payload fields | which call's answer dir to delete | observed | passed | answer-write.py#main | Silent on any malformed payload. |
| 3 | answers.py | `call_id` | `tool_use_id`, else sha1 of command text | the key one Bash call's answers live under | observed | passed | — | Falls back to command hash when harness sends no id; pre/post derive alike. |
| 4 | answers.py | `root_dir` | env `SPECSEAL_ANSWERS` | where answers live | observed | passed | hook-install.py `SWITCH` (test seams) | Test seam; unset → `~/.claude/specseal/answers`. |
| 5 | answers.py | `given` (age gate) | mtime of `<call>/<token>` vs `FRESH`=900 s, `SKEW`=2 s | whether a stored token is still consent | observed | refused | — | Out-of-window → not given. |
| 6 | answers.py | `given` + `_squash`/`_ESCAPE`/`_OTHER` | stored command text vs the hook's ancestors' `ps args=` strings, both reduced to `[A-Za-z0-9]` after dropping `\NNN` | whether the commit runs under the Bash call that carried `[no-review]`/`[no-parity]` | guess | refused | hooksession.py#call_args | Compares ps's human argv rendering by alnum substring; two calls with identical text are indistinguishable. |
| 7 | answers.py | `_prune` | mtime of each call dir | delete stale call dirs | observed | passed | — | Pure os state. |
| 8 | hooksession.py | `session` | env `CLAUDE_CODE_SESSION_ID` | which session a git hook runs under (route 1) | observed | mixed | githooks.py `_P2` (reads `$CLAUDECODE` too) | Missing → lease route; both missing → "" = person's commit, not judged (passed). |
| 9 | hooksession.py | `claude_ancestor` | `ps -o ppid=,comm= -p <pid>` up to 20 levels; `basename(comm) == "claude"` | the session's process pid | guess | passed | session-lease.py#owner_pid; worktree-guard.py:1228 | Process-name inference; an extension host not named `claude` → None → commit not judged. |
| 10 | hooksession.py | `call_args` | `ps -ww -o args=` of every ancestor up to `claude` | the argv strings `answers.given` matches | guess | refused | answers.py#given | Shell's rendering of the command in ps; no `claude` found → [] → token not given. |
| 11 | hooksession.py | `lease_dirs` + `from_lease` | every `specseal-leases/*` JSON under common dir and `worktrees/*/`; `record["pid"] == pid` | session id via lease (route 2) | owned | passed | — | Lease format written by session-lease.py; unreadable files skipped; two holders → "" (not judged). |
| 12 | session-lease.py | `main` | payload `tool_name`, `tool_input.file_path`/`notebook_path`, `cwd`, `session_id` | which repo's lease to refresh | observed | passed | — | Edit tools lease the edited file's repo, Bash the cwd's. |
| 13 | session-lease.py | `git_dir` | `git rev-parse --absolute-git-dir` | lease directory | observed | passed | implementer.py#git_dir, mode-gate.py#git_dir_of, review-skill-gate.py#git_dir, worktree-guard.py:1502 | Fifth git-dir resolver in hooks/. |
| 14 | session-lease.py | `owner_pid` | `ps -o ppid=,comm=` up to 15 levels; `"claude" in comm` | the pid recorded in the lease | guess | mixed | hooksession.py#claude_ancestor | SUBSTRING test where hooksession uses basename equality, depth 15 vs 20; None → pid omitted, guard asks. |
| 15 | implementer.py | `git_dir` | `git -C cwd rev-parse --absolute-git-dir` | where marks live | observed | passed | #13 | "" → no mark → notice fires later. |
| 16 | implementer.py | `stands` | mark file content `== branch` | whether the declared agent ran on this branch | owned | refused | — | Unreadable → False → reminder prints (notice only). |
| 17 | implementer.py | `mark_for` | `tool_input.subagent_type`, qualifier dropped by `rsplit(":")`, exact match against `framer`/`smith` | which mark a spawn writes | owned | passed | — | Any project-local agent named `smith` also matches; unknown name writes nothing. |
| 18 | implementer-mark.py | `main` | payload `tool_name` in (Agent, Task), `tool_input.subagent_type`, `cwd` | write a mark | observed | passed | — | Gated on optin + `routing.current_branch`. |
| 19 | implementer-notice.py | `commits` | Bash command text via `cmdline.drop_comments/drop_heredoc_bodies/split_segments/parse_git` | whether a commit happened (foreign-slot fallback) | guess | passed | evidence-advisor.py#commits_in; review-history-guard.py#gh_segments | Predicts the shell; only used where `githooks.decides` is False. |
| 20 | implementer-notice.py | `main` | payload `tool_name`, `tool_input.command`, `cwd`, `session_id`; `githooks.decides(root)` | stand aside where git's post-commit speaks | observed | passed | — | — |
| 21 | implementer-notice.py | `already_told` | marker file existence under git dir | once-per-session grain | observed | passed | mode-gate.py#already_asked, review-skill-gate.py#already_asked, hook-install.py#say_once, commit-review-gate.py:700, worktree-guard.py:1515 | Unwritable → "already told". |
| 22 | mode-gate.py | `main` | payload `tool_name`, `cwd`, `session_id` | whether the mode question fires | observed | passed | — | No session id → silent. |
| 23 | mode-gate.py | `undeclared` | `optin.home_at` + `config.declared_mode` kind | whether the root has no recorded mode | owned | refused | — | `unknown` value counts as undeclared → deny then ask. |
| 24 | mode-gate.py | `unreadable` | open+read `config.md` as UTF-8 | silence when the file cannot be read | observed | passed | config.py#declared_mode folds this into "none" | Gate and writer part company deliberately. |
| 25 | mode-gate.py | `git_dir_of` | `git rev-parse --absolute-git-dir` / `--git-common-dir`, joined to root | marker dir | observed | passed | #13 | — |
| 26 | mode-gate.py | `marker_dir` | realpath(home) == realpath(shared root) | per-tree vs per-clone marker key | observed | passed | — | — |
| 27 | mode-gate.py | `already_asked` | marker file existence (two dirs: choice, retry) | deny → ask → silence budget | observed | passed | #21 | Unwritable → silent. |
| 28 | review-skill-gate.py | `main` | payload `tool_input.skill == "code-review"` (exact), `cwd`, `session_id` | deny/ask between the built-in and ours | observed | passed | — | No session → `ask`. |
| 29 | review-skill-gate.py | `git_dir` | `git rev-parse --git-dir` joined onto cwd | marker dir | observed | passed | #13 | Relative-path variant; differs from the absolute-dir resolvers. |
| 30 | review-skill-gate.py | `already_asked` | marker file existence | once per session per tree | observed | passed | #21 | Session id joined raw (`:129`, RIDER) — path escape documented, not fixed. |
| 31 | review-history-guard.py | `gh_segments` + `SEG_RE` + `WRAPPERS` | Bash text split on `&&`, `\|\|`, `;`, `\n`, `\|` (quote-blind), `shlex` per piece, wrappers/assignments skipped | which segments run `gh` | guess | passed | evidence-advisor.py#commits_in (same split + WRAPPERS); cmdline.py:38, cmdline_base.py:58 | Fourth WRAPPERS copy; ignores `gh -R/--repo` (RIDER `:153`). |
| 32 | review-history-guard.py | `POST_RE` / `READ_RE` / `MERGE_RE` | regex over the gh segments | which reminder (posted / read / merge) | guess | passed | — | Lookaheads on `-X POST`, `--json …comments`; any other gh spelling is silence. |
| 33 | review-history-guard.py | `is_closed` + `CLOSED_RE` | round records via `unverified_check.readable` (fences + comments blanked), searched for `nothing to drain\|drained\|closed` | whether records are "closed" before a merge | guess | passed | — | Bare word "closed" anywhere in a person's prose counts; unreadable → closed; no skills/ → raw text. |
| 34 | review-history-guard.py | `main` | payload `tool_name`, `tool_input.command`, `cwd`; routing item/rounds/strays | which stray/unreadable/missing message prints | observed | passed | — | Rounds reading is routing's (#93–#97). |
| 35 | evidence-advisor.py | `commits_in` | same quote-blind split; after a `git` command word, ANY later token `== "commit"` | whether to run the ledger check | guess | passed | #19, #31 | `git log --grep commit` fires; advisory, so over-match is cheap. |
| 36 | evidence-advisor.py | `failing_rows` | globs `ledger.md`, `ledger/*.md`, `releases/*.md` under home + `docs/**/_evidence.md`; `evidence_check.check_ledger` statuses | which BROKEN/OLD-FORMAT/MALFORMED/OVERFLOW rows to print | owned | refused | ledger-migrate.py#ledgers; root-migrate.py `LEDGER_GLOBS` | Unparseable rows surface as MALFORMED via the checker. |
| 37 | evidence-advisor.py | `main` (frozen arm) | `evidence_check.frozen_from(root)` (`Ledger frozen from` row) | which repair line prints | owned | passed | — | Row read by the checker, not by config.py. |
| 38 | evidence-advisor.py | `main` | payload `tool_name`, `tool_input.command`, `cwd` | gate entry | observed | passed | — | — |
| 39 | ledger-migrate.py | `main` | payload `cwd` | gate entry | observed | passed | — | — |
| 40 | ledger-migrate.py | `ledgers` | same glob set as #36 (order differs) | which files are ledgers | owned | passed | #36 | — |
| 41 | ledger-migrate.py | `main` → `ec.old_format_rows` | ledger text | whether any pre-anchor row exists | owned | passed | evidence_check (other part) | — |
| 42 | ledger-migrate.py | `attempted` | `~/.claude/specseal/ledger-migrated`, `root in lines` | once-per-repo | owned | passed | root-migrate.py#attempted (identical body) | — |
| 43 | ledger-migrate.py | `dirty` | `git status --porcelain -- <rels>`: rc≠0 or non-empty stdout | refuse to rewrite over work in progress | observed | refused | root-migrate.py#dirty | Paths outside the tree (local mode) dropped first. |
| 44 | ledger-migrate.py | `main` (shared test) | normcase(home) == normcase(root/seal) | which closing sentence | observed | passed | mode-gate.py#marker_dir | — |
| 45 | root-migrate.py | `main` | payload `cwd`; `islink(.specseal)`, `islink(specs)`, `exists(.specseal/scratch)` | refuse/skip the move | observed | refused | — | Old `.specseal/scratch` honoured here only. |
| 46 | root-migrate.py | `dirty` | `git status --porcelain` XY columns; only `R `/`D ` tolerated | refuse the move | observed | refused | #43 | Porcelain v1 XY is stable. |
| 47 | root-migrate.py | `tracked_names` / `entries` | `git ls-files -z -- <rel>` top-level names; fallback `os.listdir` | units to move | observed | refused | — | Fallback listing only reached when `dirty` already refuses. |
| 48 | root-migrate.py | `ITEM_RE` + `marked` / `unmarked` | dir name `^[0-9]{9,10}-slug$` + `routing.md`/`rounds/` on disk | link refusal; "left behind" wording | guess | passed | — | Name shape can be a team's directory; docstring says shape is not proof. |
| 49 | root-migrate.py | `tracked_marks` | `git ls-files -z -- specs`: `specs/<id>/routing.md` or `specs/<id>/rounds/*` | which old dirs are SpecSeal work items | owned | refused | — | git fails → None → disk fallback, `dirty` refuses. |
| 50 | root-migrate.py | `moves` | names `map.md`, `map`, `README.md`, others | the move plan | owned | passed | — | Old-layout vocabulary. |
| 51 | root-migrate.py | `move` / `git_mv` / `taken` | `exists(dst)`, `git ls-files -z -- src`, `git mv` exit code | stop with a resumable/non-resumable error | observed | refused | — | stderr only quoted, not parsed. |
| 52 | root-migrate.py | `repoint` + `repoint_path` + `moved_items` | ledger text via `ec.unquoted` + `ec.ANCHOR_RE`; `PREFIXES` startswith; `listdir(seal/specs)` | which anchor paths are rewritten | owned | passed | evidence_check.ANCHOR_RE (other part) | Fenced examples left byte for byte. |
| 53 | root-migrate.py | `has_root` | isdir `<root>/seal`, `<common>/seal` | stamp when nothing old is left | observed | passed | optin.py#home_at (bypassed on purpose: ignores scratch) | — |
| 54 | root-migrate.py | `attempted` | `~/.claude/specseal/root-migrated` lines | once-per-repo | owned | passed | #42 | — |
| 55 | sealer-stamp.py | `main` | payload `hook_event_name == "Stop"`, `agent_id` absent, `session_id`, `cwd` | draw only at the main session's Stop | observed | passed | — | `agent_id` as subagent marker measured (Q2), harness field. |
| 56 | sealer-stamp.py | `toplevel` | walk up for a `.git` entry | which repo | observed | passed | optin.py#repo_root (git-based) | Filesystem walk, not git; nested `.git` file of a non-repo would be taken. |
| 57 | sealer-stamp.py | `drawings` / `load_stamp` | values JSON under `<common>/specseal-stamp/<session>/` via `seal_stamp.read_values/label/stamp` | which files to claim and draw | owned | passed | — | Any exception → file left pending; interpreter < 3.12 → silent. |
| 58 | version-check.py | `running` + `parse` | `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json` `version`, `repository`; `v?X.Y.Z` | running version | owned | passed | githooks.py#plugin_version, broad_gate.py:444, seal.py:1736 | Four plugin.json version readers. |
| 59 | version-check.py | `latest` + `TAG` | `git ls-remote --tags <repo>` lines, `refs/tags/vX.Y.Z$` | newest release | observed | passed | — | Other tag shapes skipped; rc≠0 → None → retry in 20 min. |
| 60 | version-check.py | `due` / `main` | marker mtime; payload `cwd` | once-a-day throttle | observed | passed | — | — |
| 61 | hook-install.py | `main` | payload `tool_name` in (None, Bash), `cwd`, `session_id`; env `SPECSEAL_HOOK_INSTALL` | install/remove stubs | observed | passed | — | `off` is the suite's seam. |
| 62 | hook-install.py | `install` | `optin.home_at`, `githooks.foreign`, `read_stub` per hook | write, remove, or report foreign | owned | refused | — | Foreign slot → nothing written (refused to overwrite). |
| 63 | hook-install.py | `write_stubs` | existing file bytes == `stub_text`, `os.access(X_OK)` | rewrite a stale stub | observed | passed | — | — |
| 64 | hook-install.py | `say_once` | marker existence `<common>/specseal-git-hooks/<session>.<kind>` | message once | observed | passed | #21 | — |
| 65 | githooks.py | `plugin_version` | `plugin.json` `version` | stub version line | owned | passed | #58 | — |
| 66 | githooks.py | `read_stub` | first 4096 bytes; line 2 `startswith(MARKER)`; `h='…'` line un-quoted | ours / version / target | owned | refused | — | Any hook file without the marker is foreign. |
| 67 | githooks.py | `hooks_path_setting` | `git config --get core.hooksPath` | whether git's hooks live elsewhere | observed | passed | — | A git failure (`None`) reads as unset. |
| 68 | githooks.py | `foreign` | #66 + #67 | whose hooks slot | owned | refused | — | — |
| 69 | githooks.py | `decides` | every stub ours, target file exists, `X_OK`, no hooksPath | whether PreToolUse text paths stand aside | observed | refused | — | Unknown → False → text paths judge (0.16.0 behaviour). |
| 70 | githooks.py | stub `_P2` (sh) | env `CLAUDE_CODE_SESSION_ID$CLAUDECODE` empty; any lease file in clone | skip Python: person's commit | observed | passed | hooksession.py#session (reads only CLAUDE_CODE_SESSION_ID) | Two env names here, one in Python. |
| 71 | githooks.py | stub `_NARROW["reference-transaction"]` (sh) | argv `$1 == prepared`; `GIT_AUTHOR_DATE` non-empty | whether the backstop runs at all | guess | passed | — | Undocumented git behaviour measured on four versions (M12); a git that stops exporting it bypasses the backstop. |
| 72 | git/pre-commit.py | `main` | cwd, `os.environ` | hands to `commitgate.pre_commit` | observed | — | — | Judgment is commitgate's (other part). |
| 73 | git/post-commit.py | `main` | cwd, `os.environ` | hands to `commitgate.post_commit` | observed | — | — | — |
| 74 | git/reference-transaction.py | `main` | `argv[1]` state; stdin ref-update lines | hands to `commitgate.reference_transaction` | observed | — | — | git plumbing hook protocol. |
| 75 | lint-python.py | `main` | `argv[1]` or payload `tool_input.file_path`; `.py` suffix; env `SPECSEAL_LINT` | whether to run ruff | observed | passed | — | No `tool_name` check; group placement does it. |
| 76 | lint-python.py | `uses_ruff` | `ruff.toml`/`.ruff.toml` exists; substring `"[tool.ruff"` in `pyproject.toml` text; stops at `.git` | whether the project "chose ruff" | guess | passed | — | TOML not parsed: a comment or string holding `[tool.ruff` counts. |
| 77 | lint-python.py | `resolve_runner` | `shutil.which`, `uv run ruff --version` exit code | which runner | observed | passed | — | — |
| 78 | optin.py | `repo_root` | `git rev-parse --show-toplevel` | the repository root | observed | passed | sealer-stamp.py#toplevel | "" → not opted in. |
| 79 | optin.py | `git_common_dir` | `<root>/.git` isdir, else `git rev-parse --git-common-dir` | common dir | observed | passed | mode-gate.py#git_dir_of | — |
| 80 | optin.py | `home_at` | `isfile(<common>/specseal-scratch)`; isdir `<root>/seal`, `<common>/seal` | opted in, and where the root is | owned | passed | root-migrate.py#has_root | Every gate's opt-in. |
| 81 | optin.py | `parity_config` | isfile `<home>/parity.md` | whether the parity arm exists | owned | passed | — | — |
| 82 | routing.py | `table_rows` + `shown` | every `\|`-led line with ≥2 cells not hidden by `blocks.walk_text`; separator = first cell ⊆ `:- ` | (label, value) pairs of routing.md | owned | passed | config.py#indexed_config_rows; chain_check.py:1283 `table_rows` | No header required; any two-cell row anywhere in the file is a row. |
| 83 | routing.py | `parse` | labels `Review`, `Destination`, `Branch` (strict), `Implementation`, `Planning`, `Automation`, `Answer pressed` (optional); dict → LAST row of a label wins | the declaration | owned | mixed | — | Strict rows → None (gate asks); optional rows → None silently. |
| 84 | routing.py | `current_branch` | `git rev-parse --abbrev-ref HEAD`; `HEAD` → "" | the branch key | observed | refused | — | Detached → no declaration → gate asks. |
| 85 | routing.py | `declarations` | `<home>/specs/*/routing.md`, UTF-8; OSError/UnicodeDecodeError skipped | all declarations | owned | mixed | chain_check (reads git's tree, not the working tree) | Skipped file = no declaration: gate asks, reminders go silent. |
| 86 | routing.py | `for_branch` / `item_dir` | parsed `branch` == current branch, exactly one | which declaration/work item applies | owned | refused | — | Two matches → none. |
| 87 | routing.py | `round_number` + `ROUND_RE` | basename `fullmatch round-(\d+)\.md` | a round record's number | owned | passed | broad_gate.py:240, chain_check.py:3851 (own `ROUND_RE`s) | Docstring calls this "the one place"; two other patterns exist. |
| 88 | routing.py | `_ordered` / `rounds` / `stray_rounds` | `listdir(item/rounds)` and `listdir(item)` filtered by #87 | the round records, numerically | owned | passed | — | `rounds` a file → [] (asked separately by #89). |
| 89 | routing.py | `rounds_unreadable` | islink / exists-not-dir / listdir failure of `rounds` | name a records dir nothing can read | observed | refused | — | Prints a message (review-history-guard). |
| 90 | blocks.py | `FENCE` + `fence_opener` / `fence_closes` / `not_spaces_after_the_run` | CommonMark 4.5 fence delimiter lines | fenced block bounds | guess | mixed | unverified_check.py:265 `fence_opener` | Emulates a renderer over person-written markdown; Unicode-space closer → whole tail uncertain. |
| 91 | blocks.py | `walk` (`CONTAINER`, `BLOCK_LOOKING`, `OTHER_HTML`, comment block) | every line of a markdown file | LIVE / FENCED / COMMENTED + `uncertain` per line | guess | mixed | — | Uncertain lines fall back to each reader's base reading. |
| 92 | blocks.py | `leaves_open` / `leaves_html_open` (`INLINE_HTML`, `TAG_END`) | inline `<!--`, CDATA, PI, declaration, tag left open | paragraph lines become uncertain | guess | mixed | — | Errs toward "uncertain", never toward hiding. |
| 93 | blocks.py | `gfm_lines` + `GFM_LINE_RE` + `walk_text` | text split at LF/CR/CRLF, mapped onto `str.splitlines` pieces | which reader line inherits which GFM line's answer | guess | mixed | evidence_check.py:374/377, unverified_check.py:162/165 | Exact GFM line rule, copied three times. |
| 94 | blocks.py | `fence_only` | fence rule alone, unclosed runs to EOF | base reading for uncertain lines | guess | passed | — | Kept only as config.py's pre-#667 reading. |
| 95 | config.py | `CONFIG_HEADER` / `CONFIG_ROW` / `CELL` / `CONFIG_SEPARATOR` + `indexed_config_rows` / `config_rows` + `unescaped` | first `\| Item \| Value \|` table: rows until a non-row line after the first row | every config.md row | owned | passed | routing.py#table_rows (different grammar); fold_check.py:491 wraps this | Malformed line after a row silently ends the table; `refusal` reports it to callers that ask. |
| 96 | config.py | `hidden_lines` / `fence_map` / `unfenced` | `blocks.walk_text` + `blocks.fence_only` | which config.md lines no walk sees; first unclosed fence | guess | mixed | routing.py#shown | — |
| 97 | config.py | `refusal` / `refused_row` | the same walk, read past the stop | refused, below, stopper for broad-gate / seal | owned | refused | — | Reports only; mode-gate does not ask it. |
| 98 | config.py | `declared_mode` | `Mode` row, lowercased, in (`local`, `shared`) | none / mode / unknown | owned | mixed | — | Unreadable file → "none" (passed); bad value → "unknown" → mode-gate asks. |
| 99 | config.py | `reference_roots` | `Reference specs` row: `none`, empty, comma list, `./` and `/` stripped, `seal…` dropped | reference roots tuple or default | owned | passed | — | Unreadable → default (None). |
| 100 | config.py | `under_reference_root` / `inside_the_root` | repo-relative path parts; default: any `specs` component outside `seal/` | whether a path is history, never read as a record | owned | passed | — | Default treats every directory named `specs` as a team's. |
| 101 | config.py | `PACT_WORD` + `names_a_pact` | a line as written and after `html.unescape` + NFKC; `p…a…c…t` with non-letters between; optional `\|` | whether a line names a pact | guess | refused | evidence_check.py:4420/4436 (copies) | Reads a person's prose for a word; loud by design. |
| 102 | config.py | `HTML_CELL`, `UNDER_A_HEADER` | `<td`/`<th` anywhere in the file; a delimiter-ish next line | drop the pipe condition for a line | guess | refused | evidence_check.py:4424/4431 (copies) | Token, not grammar; fails closed. |
| 103 | config.py | `pact_lines_not_read` | every GFM line; items of taken rows; untaken lines naming a pact | lines refused as unread pact declarations | guess | refused | — | Fences and comments read through on purpose. |
| 104 | config.py | `pact_declaration` | `Pact` (`;`-separated URLs), `Pact notify` (3-value vocab); counts of each | pacts, notify, refusals | owned | refused | — | Duplicate rows, bad vocab, any unread pact line → notify None. |
| 105 | config.py | `normalise_remote` / `pact_name` | a remote URL: scheme, `user@`, scp `:`, `.git`, case | repository identity and pact name | guess | refused | re-exported by seal.py; used in chain_check, pact_check | Someone else's URL syntax reduced heuristically; non-str → "". |
| 106 | config.py | `remote_entries` | entries: whitespace, empty name, duplicates, `PACT_NAME_RE` | parsed entries or refusal sentences | owned | refused | — | — |
| 107 | config.py | `declared_pacts` | `lexists(config.md)`, open | None for unreadable (pact-check UNREADABLE) | observed | refused | — | Opposite failure direction from #98/#99, stated. |
| 108 | config.py | `gfm_table` + `table_end` / `html_start` / `raw_html_open` / `a_list_above` / `DELIMITER_ROW` / `ATX_HEADING` / `THEMATIC_BREAK` / `BLOCK_QUOTE` / `LIST_ITEM` / `HTML_KINDS` | a named GFM table, emulating cmark-gfm's end rules | rows or a refusal naming the shape | guess | refused | — | Held to cmark-gfm by a property test; anything not certain refuses. |
| 109 | config.py | `table_cells` + `TABLE_ROW` / `CELL_PIPE` / `EVEN_ESCAPED_PIPE` | `\| … \|` line split into cells | a row's cells | guess | refused | — | Even-backslash pipes → None (cmark-gfm splits differently). |
| 110 | config.py | `read_table` + `renamed_header` | the new header; old `Signatory` header; its OWN refusal sentences via `startswith("holds no ")` and `` re.findall(r"`([^`]*)`") `` | which header was read; dedupe refusals | owned | refused | — | Decides by parsing sentences this module wrote. |
| 111 | config.py | `pact_signers` | `\| Signer \|` rows; `"renders no table" in r` over refusal text | signers or refusals | owned | refused | — | Again matches its own prose. |
| 112 | config.py | `pact_changes` | `\| Clause \| Row \| Code \| Checked \|` rows; `CHECKED_DATE` | change rows | owned | refused | — | — |
| 113 | config.py | `pact_reviews` | `\| Signer \| Change \| Verdict \|` rows (or old header) | review rows | owned | refused | — | Verdict vocabulary left to pact-check. |

Reader rows: **113**.

### Payload and environment fields read, per hook (hooks.json → dispatch.py groups)

| Group (event) | Hook | Payload fields | Env / process / other |
|---|---|---|---|
| pre-bash | hook-install.py | `tool_name` (None or Bash), `cwd`, `session_id` | `SPECSEAL_HOOK_INSTALL`; `git config core.hooksPath`; plugin.json |
| pre-bash | answer-write.py | `tool_name`, `tool_input.command`, `tool_use_id`, `session_id` | `SPECSEAL_ANSWERS` |
| pre-bash | mode-gate.py | `tool_name`, `cwd`, `session_id` | — |
| pre-agent | implementer-mark.py | `tool_name`, `tool_input.subagent_type`, `cwd` | `git rev-parse` |
| pre-skill | review-skill-gate.py | `tool_input.skill`, `cwd`, `session_id` | — |
| post-bash | review-history-guard.py | `tool_name`, `tool_input.command`, `cwd` | loads `skills/verify/scripts/unverified_check.py` |
| post-bash | implementer-notice.py | `tool_name`, `tool_input.command`, `cwd`, `session_id` | — |
| post-bash, post-edit | session-lease.py | `tool_name`, `tool_input.file_path` / `notebook_path`, `cwd`, `session_id` | `ps` ancestry; hostname |
| post-bash | evidence-advisor.py | `tool_name`, `tool_input.command`, `cwd` | loads `evidence_check.py` |
| post-bash | answer-clear.py | `tool_name`, `tool_input.command`, `tool_use_id`, `session_id` | — |
| post-edit | lint-python.py | `tool_input.file_path` (or `argv[1]`) | `SPECSEAL_LINT`; `uv`/`uvx`/`ruff` on PATH |
| session-start | version-check.py | `cwd` | `CLAUDE_PLUGIN_ROOT`; `git ls-remote`; `~/.claude/specseal/version-check` |
| session-start | root-migrate.py | `cwd` | `~/.claude/specseal/root-migrated`; `git status/ls-files/mv/add` |
| session-start | ledger-migrate.py | `cwd` | `~/.claude/specseal/ledger-migrated`; `git status --porcelain` |
| stop | sealer-stamp.py | `hook_event_name`, `agent_id`, `session_id`, `cwd` | `<common>/specseal-stamp/<session>/` |
| git (not harness) | git/pre-commit.py, git/post-commit.py, git/reference-transaction.py | none | cwd, full `os.environ` (`GIT_INDEX_FILE`, `GIT_CONFIG_PARAMETERS`, `GIT_AUTHOR_DATE`, `CLAUDE_CODE_SESSION_ID`), argv, stdin; via hooksession: `ps` ancestry, lease files |

No hook in this part reads the transcript file; the transcript read on the commit path is `worktree_consent.py#automation_answered` (other part), reached from `commitgate`.

## Size and growth

| File | Lines now | Lines at v0.18.0 | Commits v0.18.0..HEAD | Readers counted |
|---|---|---|---|---|
| hooks.json | 82 | 82 | 0 | 0 |
| answer-clear.py | 28 | 28 | 0 | 1 |
| answer-write.py | 34 | 34 | 0 | 1 |
| answers.py | 188 | 188 | 1 | 5 |
| blocks.py | 436 | 436 | 0 | 5 |
| config.py | 1512 | 944 | 4 | 19 |
| console.py | 71 | 71 | 0 | 0 |
| evidence-advisor.py | 263 | 263 | 0 | 4 |
| git/post-commit.py | 25 | 23 | 1 | 1 |
| git/pre-commit.py | 48 | 46 | 1 | 1 |
| git/reference-transaction.py | 35 | 33 | 1 | 1 |
| githooks.py | 254 | 254 | 0 | 7 |
| hook-install.py | 202 | 202 | 1 | 4 |
| hooksession.py | 148 | 148 | 0 | 4 |
| implementer-mark.py | 76 | 76 | 0 | 1 |
| implementer-notice.py | 204 | 204 | 1 | 3 |
| implementer.py | 140 | 140 | 0 | 3 |
| ledger-migrate.py | 244 | 244 | 0 | 6 |
| lint-python.py | 113 | 113 | 0 | 3 |
| mode-gate.py | 351 | 351 | 1 | 6 |
| optin.py | 224 | 224 | 0 | 4 |
| review-history-guard.py | 302 | 302 | 0 | 4 |
| review-skill-gate.py | 184 | 184 | 1 | 3 |
| root-migrate.py | 698 | 698 | 0 | 10 |
| routing.py | 510 | 510 | 0 | 8 |
| sealer-stamp.py | 185 | 183 | 1 | 3 |
| session-lease.py | 138 | 138 | 1 | 3 |
| version-check.py | 189 | 187 | 1 | 3 |
| **Total** | **6884** | **6306** | — | **113** |

Every one-commit row except config.py and sealer-stamp.py is `a4a32514` (#757, encoding names and `to_utf8` at every entry point); sealer-stamp.py's is `149ca9ec` (#832). Growth since v0.18.0 is +578 lines: +568 in config.py, and +2 each in the three git entry points, sealer-stamp.py and version-check.py.

## Observations

- **config.py is where this part is still being patched.** 944 → 1512 lines since v0.18.0, through four commits, all pact: `d671a439` (#756), `1e2b2ed5` (#759/#793), `4b363e68` (#822/#827), `275a7ce0` (#831/#843). Over its whole history it has 11 commits citing 19 issues (#151 … #843). Its comments name review rounds of PR #749, #784 and #793 that each found a shape the previous emulation missed (`config.py:936-938`, `:1206-1222`).
- **There are three markdown-table grammars in hooks/.** `routing.table_rows` takes any ≥2-cell pipe line anywhere, with no header, and the last label wins (`routing.py:175-183`, `:232`). `config.indexed_config_rows` takes the first `| Item | Value |` table and stops at its first non-row (`config.py:353-375`). `config.gfm_table` emulates cmark-gfm and refuses anything uncertain (`config.py:1183-1311`). A fourth, `chain_check.py:1283 table_rows`, sits outside this part.
- **config.py decides by reading sentences it wrote itself.** `read_table` checks `refusals[0].startswith("holds no ")` and pulls backtick-quoted cells out of refusal prose with `re.findall` (`config.py:1345-1364`). `pact_signers` tests `"renders no table" in r` (`config.py:1411`). The input is owned, but rewording a refusal changes the control flow.
- **The `claude` process is found by two different tests.** `session-lease.py:78` uses a substring (`"claude" in comm`, depth 15), while `hooksession.py:59,95` and `worktree-guard.py:1228` use `basename == "claude"` (depth 20). The lease writer and the lease reader can therefore disagree on which pid owns a session.
- **The session is named by different environment variables in sh and Python.** The stub's P2 test reads `$CLAUDE_CODE_SESSION_ID$CLAUDECODE` (`githooks.py:118`), but `hooksession.session` reads only `CLAUDE_CODE_SESSION_ID` (`hooksession.py:142`). If only `CLAUDECODE` is set, Python starts, falls to the lease route, and may answer "no session". No session means the commit is not judged (`hooksession.py:148`).
- **The waiver token is matched through `ps`.** `answers.given` compares the stored command with the `ps args=` rendering of the hook's ancestors, both squashed to alphanumerics (`answers.py:153-187`, `hooksession.py:81-102`). It is keyed by call directory but matched by text, so two parallel calls with the same command text cannot be told apart.
- **The backstop's trigger is an undocumented git behaviour.** `reference-transaction` runs Python only when `GIT_AUTHOR_DATE` is exported (`githooks.py:101-102`). That rule was measured on four git versions (M12); a git that stops exporting the variable skips the backstop silently.
- **Copies across files:**
  - `WRAPPERS` ×4: `cmdline.py:38`, `cmdline_base.py:58`, `review-history-guard.py:162`, `evidence-advisor.py:81`. The two post-bash copies also share the quote-blind `&&|\|\||[;\n|]` split.
  - git-dir resolvers ×6: `implementer.py:60`, `session-lease.py:42`, `review-skill-gate.py:96` (relative `--git-dir`), `mode-gate.py:184`, `worktree-guard.py:1502`, `optin.py:99`.
  - once-per-session markers ×6: `mode-gate.py:90`, `review-skill-gate.py:113`, `implementer-notice.py:122`, `hook-install.py:72`, `commit-review-gate.py:700`, `worktree-guard.py:1515`.
  - plugin.json version readers ×4: `githooks.py:71`, `version-check.py:68`, `broad_gate.py:444`, `seal.py:1736`.
  - `attempted`/`stamp` in `ledger-migrate.py:101` and `root-migrate.py:146` are byte-identical.
- **The round-number rule is not in one place.** `routing.round_number` says it is "the one place the ordering rule lives" (`routing.py:381-387`). `broad_gate.py:240` and `chain_check.py:3851` still define their own `ROUND_RE`, and the three anchor differently (`fullmatch` on the basename; `^…$`; `…$`).
- **The ledger glob set is spelled three times.** `evidence-advisor.py:166-173`, `ledger-migrate.py:82-83` and `root-migrate.py:123`. The root-migrate copy has no `releases/*.md`; it predates #547, and it is the old-layout reader.
- **Some guesses could be made observed or owned:**
  - `lint-python.uses_ruff` matches the substring `[tool.ruff` in pyproject text (`lint-python.py:58`); `tomllib` would make it a parse.
  - `evidence-advisor.commits_in` fires on any later token equal to `commit` (`evidence-advisor.py:106`), so `git log --grep commit` matches. Where `githooks.decides` is True, git's own post-commit already knows a commit happened.
  - `review-history-guard.is_closed` accepts the bare word `closed` anywhere in a record (`review-history-guard.py:72`), which is a person's prose.
- **Known defects left documented as RIDER comments:**
  - `review-skill-gate.py:122-129`: the session id is joined into a path raw, and a path escape was executed.
  - `review-history-guard.py:153-161`: `gh -R/--repo` is ignored, and WRAPPERS is a copy.
  - `optin.py:51-57`: `rev-parse --show-toplevel` runs three times per gated command.
- **Failure directions differ by reader, deliberately and in writing.**
  - config.md: `declared_mode` and `reference_roots` treat an unreadable file as nothing declared, but `declared_pacts` returns None and pact-check refuses it (`config.py:998-1005`).
  - mode-gate's `unreadable` (`mode-gate.py:156-181`) splits from `declared_mode` on purpose.
  - The opt-in, lease, session, notice and stamp readers all fail toward silence. Only `routing.parse`'s two strict rows, `current_branch` and `for_branch` fail toward asking.
- **`blocks.py` is a renderer emulator that knows its limits.** Every line carries an `uncertain` flag, and uncertain lines fall back to each reader's pre-#667 reading (`blocks.py:46-51`). Its GFM line rule is copied verbatim in `evidence_check.py:374` and `unverified_check.py:162`, and its fence rule in `unverified_check.py:265`. The copies are held equal by tests, not by an import.
