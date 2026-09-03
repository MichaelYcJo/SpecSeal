# The settings live in a file nobody opens — spec

<!-- seal/specs/1788420761-the-settings-live-in-a-file-nobody-opens/spec.md —
issue #105. Written before the first edit. -->

## The problem

`seal/config.md` holds what a repository decides for itself and there is no
way to see it or change it except opening the file. Three rows exist after
#104 and #106 — `Commit and pull request language`, `Record language`,
`Mode` — and every one of them is discovered by reading a template a person
has no reason to open.

That is the complaint that opened #104 in a different shape. Switching modes
was two shell lines nobody could find; the whole file is the same problem one
level up. First setup asks its questions in a batch and never asks again, and
this is the way to ask them later.

## The shape, and the layering is the design

```
seal/config.md          the file — a person can still open and edit it
seal mode <x>           the row that has a side effect, as a script (#104)
/specseal:config        the front door: shows every row, routes a change
```

**The skill holds no logic of its own beyond routing.** A row that needs work
done routes to the script that does it; a row that is only a row is written
directly. That boundary is what keeps this testable — logic inside a skill
cannot be mutation-tested the way `skills/implement/scripts/` can, and this
repository has just spent five review rounds on what an unpinned unit costs.

## Acceptance criteria

| # | Given / when / then | Verifiable how |
|---|---|---|
| S1 | Given a repository with a root, when the skill runs, then it prints every row with its current value and what an absent one defaults to | S1 case: the skill names all three rows |
| S2 | Given the `Mode` row, when the skill shows it, then it also shows the folder's actual location and whether the two agree | S2 case: the skill routes that row to `seal mode` rather than reading it itself |
| S3 | Given a change to a row with a side effect, when the skill applies it, then it runs the command that owns that row and reports what happened beyond the row | S3 case: the skill names `seal mode` and no other way of moving the folder |
| S4 | Given a change to a row with no side effect, when the skill applies it, then it edits the file and nothing else | S4 case |
| S5 | Given `local → shared`, when the skill is about to apply it, then it says the commit is what cannot be undone before acting | S5 case: the sentence is in the skill, and `seal mode` prints it too |
| S6 | Given no root at all, when the skill runs, then it says first setup has not happened and names what does it | S6 case |
| S7 | Given the skill, when a session reads it, then the questions it asks are the same list the bootstrap asks — one list, not two | S7 case: the skill and the bootstrap name the same rows |

## Fail directions

| What goes wrong | What happens | Why that and not something else |
|---|---|---|
| A row's value is unreadable | it is shown as the default with the reason | Every reader of this file already lands on the default for an unreadable value; the skill showing something else would be a second answer |
| The mode row and the folder disagree | shown as a disagreement, with the command that resolves it | That is `seal mode --check`'s own answer, routed rather than reimplemented |
| A person edits the file by hand instead | nothing breaks | The file is the interface; this is a door to it, not a gate in front of it |

## What this does not build

**A generic `seal config set <key> <value>`.** That is a parser for a file
people edit by hand, and it invites the file to drift from a short document
into key-value settings. The skill reads the rows that exist and routes them;
it does not define a schema.

**A "start fresh" command.** Wanting to start over means discarding the ledger
and the work-item records, which is discarding the evidence chain every gate
here reads. It stays a deliberate act done by hand.
