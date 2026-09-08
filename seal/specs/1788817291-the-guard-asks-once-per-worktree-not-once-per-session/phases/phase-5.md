# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | d64a3fd |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Not in the plan when it was approved. `agents/smith.md` §Verify requires every
unit added to be mutation-tested one at a time before hand-back — broken, the
covering cases run, and one seen red — because a unit that stays green while
broken has nothing behind it whatever the suite total says. Phases 2–4 added
nine units, so this is their verification pass, and it earned a row of its own
rather than being folded into phase 4's.

## What this phase found

**Sixteen mutations, and three of them were green on the first pass.** A red
baseline for the file said nothing about those three: the cases covering them
passed both before and after the fix, for the wrong reason each time.

| The unit broken | Why nothing caught it | What now does |
|---|---|---|
| `granted` accepting a directory where it wants a file | the unwritable-record case makes the consent DIRECTORY a file, so `<file>/me` is absent under either spelling | `test_a_directory_at_the_record_path_is_not_a_record`, which puts a directory at the record's own path |
| `record` raising instead of failing quietly | the case read the hook's **stdout**, and a traceback goes to stderr — a crashing hook and a quiet one look identical there | the same case now reads the exit status and stderr too, and calls `record` directly |
| `consent_path` refusing a separator-only session id | `..` was caught one layer down, by `open` raising on a directory — a platform guarantee, which `agent-contract` §13 refuses as a defence | `test_a_session_id_that_is_only_separators_has_no_record_path`, which asks the function |

**A fourth mutation could not be made to fail, and that one was a defect in the
code rather than in the cases.** `if session_id and worktree_consent.granted(…)`
— `consent_path` already answers `""` for a missing id, so nothing could make
the extra condition false. A condition no case can pin was removed rather than
pinned, and the line now carries a comment saying why there is no guard in
front of the call.

**`only_creates_a_worktree`'s false branch is unreachable from `main`**, which
is a fifth case of the same shape and was fixed the same way: the predicate is
now asked directly, with commands that create nothing, rather than only through
a caller that never hands it one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `session_id and` condition in front of `worktree_consent.granted` in `guard_worktree_creation` | Nowhere — `consent_path`'s own guard already answers for a missing or separator-only id, and `test_a_session_id_that_is_only_separators_has_no_record_path` pins it there |
