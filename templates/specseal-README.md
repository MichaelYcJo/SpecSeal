# .specseal/ — what this plugin maintains

This directory exists for AI sessions to hand work to each other. It is safe
to delete wholesale **after the export rules below have run** — nothing that
must survive is allowed to live only here.

It is **committed** (gitignored files don't follow worktrees or other
machines). Everything in it is permanent: `map.md`, `parity.md`, and
`follow-up.md`.

**A repository under review must never carry `.specseal/scratch`.** That file
is an opt-out: where it exists, every gate reads the repository as one that
never opted in and says nothing. It is for a repository built to be thrown
away — a fixture made by hand to reproduce a gate decision — and in a
repository anyone reviews it silently turns the workflow off.

Review round records used to live here too, under `handoff/PR-<n>/`. They
moved to `specs/<work-item-id>/`, beside the work item they are about. The PR
number was the wrong key: it does not exist while the rounds that would fill
the directory are running, so the directory was never once created. The work
item's directory exists from its first commit.

## Export rules — drain before closing

| Item still here | Destination |
|---|---|
| Verified facts (`evidence-todo.md`) | `map.md` — the spec-clause ↔ coordinate table |
| Tests to plant (`tests-todo.md`) | the implementation commit — or `.specseal/follow-up.md` if blocked on prerequisite work |
| Open decisions | the policy document's open-questions section |

Closing without exporting leaves the list where nothing looks for it — a
prescribed test unplanted, a verified fact unmerged.

## Layout

```
.specseal/
├── map.md               spec clause ↔ code coordinates (split into map/ if it grows)
├── parity.md            migration config, only where one is declared
└── follow-up.md         schedulable items in a repository with no tracker
```

The review round records are next door, in the work item's own directory:

```
specs/<work-item-id>/
├── routing.md           which way this work item was routed, written before the first edit
├── rounds/
│   └── round-N.md       target SHA · Pass · who checked the fixes · verdicts · executed probes · inherited coordinates · deferrals
├── tests-todo.md        regression tests to plant, destination file per row
└── evidence-todo.md     facts to merge into the evidence ledger
```

There is no task list here and no directory for one. `plan.md`'s Phases table
is where the work records how far it got, in a Status column whose closed value
is the commit that closed the phase — a past state someone can open, rather
than a tick anyone can type.

Reports meant for humans go to PR comments; this directory is for the **next
session** — the two audiences never share a file.
