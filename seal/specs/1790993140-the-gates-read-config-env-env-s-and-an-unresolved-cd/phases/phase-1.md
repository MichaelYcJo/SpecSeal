# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | bfdb9b18 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Teach the commit gate's reader (`hooks/cmdline.py`) #716's two spellings and
their class. M1 first: run each git global option on the installed git, with
its value as a separate word, in a scratch repository under the session
scratchpad. Add `--config-env` and every other missing member to
`_git_options`. Make the `env -S` arm of `reparsed_texts` add
`env <string> <rest>` beside the string. Change the `TEXTS` pin with a note.
Reword the `env -S` clause of `docs/commit-review-gate-spec.md`'s #670
paragraph in place, with no new line and no new fold marker (D9).

## What this phase found

**M1, executed on git 2.54.0 (Apple Git-157).** Each candidate was run as
`git -C <scratch> <option> <value> status --porcelain=v1 -b`, and the option
counts as taking a separate value where `status` ran:

| Option | Spaced value accepted | Was in `takes_value` |
|---|---|---|
| `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace` | yes | yes |
| `--config-env` | yes | **no** |
| `--attr-source` | yes | **no** |
| `--shallow-file` (undocumented) | yes | **no** |
| `--exec-path` | no: git prints its path and exits 0 | yes |
| `--super-prefix`, `--list-cmds`, `--git-common-dir` | no: `unknown option`, exit 129 | no |
| `--html-path`, `--man-path`, `--info-path` | no: print and exit | no |
| `--bare`, `-p`, `-P`, `--paginate`, `--no-pager`, `--no-replace-objects`, `--no-lazy-fetch`, `--no-optional-locks`, `--no-advice`, the four `--*-pathspecs` | no: the value read as the subcommand | no |

The three missing members went in. `--exec-path` stays: it takes no separate
value, but the word it makes the reader skip is never run either, because git
prints and exits. `--super-prefix` took a separate value in gits older than
the installed one; it is refused by 2.54.0 and was not added, so the class is
the installed git's. CI's legs run other gits, and nothing here measured them.

**`env -S`'s reading is a separate helper, `_env_words`.** It builds
`<env word> <words before the option> <the string> <words after it>`, with
every redirection taken out by the module's existing `_without_redirections`.
The words before the option stay because `env -v -S '…'` passes `-v` to the
same `env`. A redirection as the last word, with no string after it, gives no
env reading. All three spellings (`-S <s>`, `-S<s>`, `--split-string[=]<s>`)
and `genv` share it.

**Which reading each #716 shape reaches** is as `spec.md`'s table says, and
read, not run: `steps_around_hooks` matches `hookspath` in the spaced
`--config-env` shape and `env` is not plain, so in a clone carrying the stubs
the PreToolUse reading judges both. The S2 case executes that half for the
`--config-env` shape (`deny` through `dispatch.py pre-bash`).

**The docs reword fit in the same 14 lines** by reflowing the rest of the
paragraph. `wc -l docs/commit-review-gate-spec.md` is 1047 before and after.

**A rider drifted.** The `# RIDER:` inside `_git_options` (the `--git-dir` and
`--work-tree` values are thrown away) was re-read against the edit. The claim
still holds, and it was re-stamped with `rider_check.py --reverify --only
hooks/cmdline.py`.

**Red, then green.** At `233f0455` the run of the two touched modules gave 22
failures, every one a new case: the six `env -S` shapes twice (read and
gate), five `TEXTS` pins, three spaced options, the undeclared gate case and
the stubbed-clone case. The two `env -S` controls passed there, as pins of an
unchanged answer should. After the fix the same run gave 620 passed.

**Every unit added was broken once with `mutation-check`, and every break was
red**: the base `env -S` text dropped (5 failed, the S5 mutant), the env
reading dropped in each of the three arms (12, 3 and 3 failed), the
redirections before and after the option kept (1 and 2), the empty-after
refusal removed (1), and each of the three new `takes_value` members removed
(2, 1 and 1). Two `TEXTS` pins were added in `5a60fdac` for the first and
third of those, which no case reached before.

**The 18 modules that read `docs/commit-review-gate-spec.md` or
`hooks/cmdline.py`** gave 1463 passed, 73 skipped and 1 failed: this work
item had no `overview.md` yet, which
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` requires.
It is opened in the commit that carries this record.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
