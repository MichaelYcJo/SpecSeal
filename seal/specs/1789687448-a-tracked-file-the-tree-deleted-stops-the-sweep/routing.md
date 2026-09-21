# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Automation | yes |
| Answer pressed | automation |
| Branch | fix/432-282-a-tracked-file-the-tree-deleted-stops-the-sweep |

Answered 2026-09-18 by MichaelYcJo, before the first edit.

## Why this way

Two cases that hold `CLAUDE.md`'s no-real-identifiers rule walk `git ls-files`
and open every path. `git ls-files` lists the index, so a file that is tracked
and has been deleted from the working tree is on that list and not on disk:
`open()` raises, the case ends there, and no file after it in the walk is ever
read. The documented release sequence produces exactly that state —
`fold_ledger.py` removes every ledger fragment as its last act and the
checklist then says to run the whole gate before committing — so this is what
a release meets rather than something a session has to contrive. 0.12.1's own
preparation meets it again.

#282 is in the same branch because #432's own body sends it there: *worth
checking in the same pass whether any other case in the suite opens a
`git ls-files` path without the same guard*. #282 is that check, already
written down. Fixing one caller and leaving the class is what this repository
files under a finding fixed at its own coordinate.

A check that crashes is a check whose verdict changed — a crash is not a green
run, but it is not the rule being enforced either, and the failure names a
missing file rather than the rule, so the person reading it debugs the wrong
thing. That puts it on the ladder's top rung, and the frame is drawn by a
party that does not then build to it.
