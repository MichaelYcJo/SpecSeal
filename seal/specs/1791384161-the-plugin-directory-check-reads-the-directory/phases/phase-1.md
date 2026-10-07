# 1791384161-the-plugin-directory-check-reads-the-directory — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | c216ee5d |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`plan.md` phase 1: the command stops claiming, and its pins move. The constant
PORTAL and the two sentences naming it go; an absent entry becomes one line,
*not an entry in <file> (<N> entries)*, with nothing after it; a closing block
says the directory was not read and cannot be read by a script, and names the
portal's Submissions page and the Console page by the kind of listing each
answers for, with one line that a portal listing takes new versions from its
tracked branch on its own; the docstring's paragraph on how an update reaches
a listed plugin is replaced by the three dated facts from the docs; the
vocabulary of `spec.md` §*Vocabulary* holds in the docstring and every printed
line. `claude.ai` enters `ALLOWED_DOMAINS` with its comment. The test module
loses the PORTAL pin, moves the *readable from nowhere public* pin, and gains
cases for A1 and A3, each seen red against the command at 59998a32. The
command runs once live against `main`.

## What this phase found

**The frame's own files were red under the rule they cite.** Before any edit,
`tests/test_no_real_identifiers.py::test_only_neutral_domains` failed on the
branch at 0fb6fd0c: `spec.md`, `plan.md` and `questions.md` name `claude.ai`
twenty times, and `spec.md` (twice) and `questions.md` (once) name the
company's mail domain — in the very sentences saying that domain stays out of
the allowlist. Allowing `claude.ai` cleared the first; the second would have
stayed red. Those three places now say *the company's mail domain* instead of
spelling it; the meaning is unchanged, and A10's check is still the test
module, which the sweep does not read.

**A2 and the output contract disagree, and the output contract won.** `spec.md`
A2 says the existing cases of the test module stay *green without edit*;
`spec.md` §*Data & interfaces* says an entry's line reads *an entry, pinning
<sha12> of <url>* and *an entry, pinning no commit*. The existing cases assert
`"listed" in head and "not listed" not in head`, so they cannot stay unedited
under the specified output. §*Vocabulary* and A9 decide it: *listed* is the
directory's word, and a marketplace file's line saying it is the guess this
work removes. The two assertions now read `"an entry" in … and "not an entry"
not in …`; the facts A2 is about — the pinned commit on the first line, the
three ancestry answers — are asserted exactly as before. Recorded in
`overview.md` §*Where spec and implementation diverged*.

**The vocabulary reached names, not only prose.** The constant `DIRECTORIES`
held the two GitHub repositories and is now `MARKETPLACES`; the test module's
`directory()` and `listed()` helpers are `marketplace()` and `pinning()`; two
cases were renamed (`test_an_entry_reports_its_pinned_commit`,
`test_it_reads_the_path_the_marketplace_files_actually_have`,
`test_a_payload_that_is_not_a_marketplace_file_is_a_report`), and the absent
case was replaced by `test_an_absent_entry_names_the_file_and_its_count_and_no_act`.
Nothing outside the two files referenced the old names except
`.test_durations`, whose stale keys only unbalance a shard
(`tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`'s
docstring).

**§12, the class.** The class is *a printed line that names an act about the
directory*. The command printed it in two places (the absent entry and the
reachable pin), and both were removed. The A1 run-wide case cannot reach the
reachable line — a fake SHA lands on *unknown here* — and M7 below survived
until the case that builds a real ancestry pinned it (c216ee5d).

**Seen red against the command as #417 left it (§15), executed.** With the
new test module over the command at 59998a32: 10 failed, 6 passed. The
assertion each red case stopped on:

| Case | Said |
|---|---|
| `test_the_run_claims_nothing_about_the_directory_and_names_the_pages`, three ids | *the short link that answers 302 to a documentation page is still a constant here* |
| `test_an_absent_entry_names_the_file_and_its_count_and_no_act` | *an absent entry is followed by more than its own line*, `2 == 1` |
| `test_an_entry_reports_its_pinned_commit` | `'an entry' in '… listed, pinning 0123456789ab …'` |
| `test_an_entry_that_pins_no_commit_is_read_rather_than_raised_on`, three ids | `'an entry' in '… listed, pinning no commit …'` |
| `test_the_run_exits_zero_on_absence_and_on_a_failed_fetch`, two ids | *the run does not say what it cannot answer*: `'was not read' in …` |

The allowlist row was seen red by the baseline run above: the sweep failed on
`claude.ai` before the entry and passed after it.

**Mutations, one unit at a time, executed through `bin/mutation-check`** on
`.github/scripts/plugin_directory_check.py` at edc15efa, each over
`tests/test_the_plugin_directory_answers_the_box.py` with `-p no:xdist`:

| # | Break | Verdict |
|---|---|---|
| M1 | the absent-entry return grows a second line, `"    Act."` | red — `test_an_absent_entry_names_the_file_and_its_count_and_no_act` |
| M2 | the closing says *skipped* where it says *read* (so no *was not read*) | red — 5 cases, A1 and A7 end to end |
| M3 | the Console page's line in the closing becomes an empty string | red — 3 cases of A1 |
| M4 | the Submissions page's line loses the page and its address | red — 3 cases of A1 |
| M5 | *on its own* leaves the closing's last line | red — 3 cases of A1 |
| M6 | the entry line says *listed, pinning* again | red — `test_an_entry_reports_its_pinned_commit` |
| M7 | the reachable line ends *resubmit it.* | SURVIVED at edc15efa; red at c216ee5d — `test_a_commit_this_clone_does_not_have_is_not_called_unreachable` |

**The live run, executed** at edc15efa with
`python3 .github/scripts/plugin_directory_check.py`, exit code read directly:
`exit 0`.

```
plugin 'specseal', against main

official (anthropics/claude-plugins-official): 'specseal' is not an entry in this file (315 entries).

community (anthropics/claude-plugins-community): 'specseal' is not an entry in this file (2284 entries).

The directory -- the catalog people browse inside Claude -- was not read: no script can reach it, so nothing above says whether this plugin is published there.
A person opens the page for the kind of listing it has:
    a portal listing:  the portal's Submissions page, https://claude.ai/directory/manage -- its status, and the version that is live
    a Console listing: the Console page, https://platform.claude.com/plugins/submissions
A portal listing takes new versions from its tracked branch on its own; a Console listing takes none until it is moved to the portal.
```

**Verified by, executed.** `plan.md` names `uv run --frozen pytest`; in this
worktree that cannot start pytest, so the same three modules ran through
`bin/test -q -p no:cacheprovider` at c216ee5d: exit 0, 27 passed. `uvx ruff
check` and `uvx ruff format --check` over the three changed Python files:
exit 0 each.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the constant PORTAL and the short link it held | none — the link answers 302 to a documentation page; the two pages a person opens are `SUBMISSIONS_PAGE` and `CONSOLE_PAGE` |
| *Submit it through …* on an absent entry, *resubmit through …* on a reachable pin | none — `spec.md` §*Vocabulary*: on the portal nothing is resubmitted, and a Console listing takes no new version |
| the docstring's paragraph saying no document tells how an update reaches a listed plugin, pointing at #417's Q1 | the docstring's *Three facts from the documentation, read 2026-10-07* |
| the closing *Whether a submission has been ACCEPTED is readable from nowhere public* | `closing()` in the same command |
| the test pin on PORTAL and the pin on *readable from nowhere public* | `test_the_run_claims_nothing_about_the_directory_and_names_the_pages`, and the A7 end-to-end case's *was not read* |
