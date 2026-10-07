# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | bffcb3a2 |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`plan.md` phase 3: put `-z` into `tracked_at` and into `call_sites`' parse
(two partitions on NUL, one on the first `:`), with `touched` already
verbatim through phase 1. See S10's fixture red against each of the three
readers. Run `tests/test_a_runner_reached_unit_reads_pytest_only.py` at the
boundary, because it reads `call_sites`.

## What this phase found

**Each reader was seen red in turn, on one fixture.** The fixture turns
`core.quotePath` on, so the case does not depend on the config of whoever
runs it. Against 361b4e4a, `New units` read `none`, because `touched` reads
paths verbatim since phase 2 and the quoted `ls-tree` name matched none of
them. With `tracked_at` on `-z`, `Contract changes` read `helper → caller,
"na\303\257ve.py", pytest`. With `call_sites` on `-z`, the case went green.
The third reader, the `Location` resolved through `tracked_at` when `new`
counts a fix of a fix, could not be seen red on its own while the first two
failed ahead of it. A `bin/mutation-check` break that reads only `landings`'
tracked set back through the old quoting split turns the case red at that
assertion.

**`-I` joins `-z` in `call_sites`.** git reports a binary file that holds the
call as one `Binary file … matches` line with no NUL in it. The old split
on `:` read that line as no match. The NUL walk would read it as the head of
the next match and name `caller` by a path that is no file. `-I` leaves
binary files out of the search. `test_a_binary_file_holding_the_call_hides_no_call_site`
pins it, and dropping `-I` turns that case red.

**A `:` inside a path is a case of its own.** The NUL walk splits on the first
`:` of `<rev>:<path>`, and the revision is a full commit, which has no `:`.
Reading the last `:` instead SURVIVED every case until
`test_a_colon_in_a_path_does_not_split_it` was added. That case is skipped
on Windows, which allows no `:` in a file name.

**The line-split inventory shrank by two.**
`tests/test_every_reader_ends_a_line_where_gfm_does.py`'s `OUT_OF_CLASS`
listed `touched` and `tracked_at` as `splitlines` callers over git output.
Neither splits on lines now, and that module refuses a listed unit that no
longer calls it, so both entries are gone, with a comment saying why.

**0.16.0's `G9` is corrected.** It said `call_sites` splits `git grep -n`
with `gfm_lines`. Under `-z` git ends each match at LF and nothing else, so
the walk ends a match's text at LF. A U+2028 in the text still cuts nothing,
and the case that pins that stayed green. The claim's wording went with the
code, so the row is a `Corrected ·` one. A `--reverify --into` run first
wrote a `Re-read ·` row for `G9`, because the correction had not reached the
fragment yet. That row was replaced by the `Corrected ·` row before this
commit.

**Q3 is open.** The `-z` shapes were measured on macOS, git 2.50. Whether the
Windows leg's git emits the same `grep -z` shape is a CI run's answer, and
`overview.md` §*Not verified* names it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tracked_at`'s `splitlines` over quoted `ls-tree` output | `ls-tree -z`, split on NUL |
| `call_sites`' `gfm_lines` walk and its `split(":", 3)` | the NUL walk over `git grep -n -z -I` |
| the `OUT_OF_CLASS` entries for `touched` and `tracked_at` | none: neither unit splits on lines now |
| 0.16.0's `G9` claim about `call_sites` | a `Corrected ·` row in this item's ledger fragment |
