# seal/ — what this plugin maintains

This directory exists for AI sessions to hand work to each other. It is one
root laid out by lifetime: the rows that outlive a work item at the top, and
each work item whole under `seal/specs/<work-item-id>/`, where it waits until
a later `settle` folds it. It is safe to delete a work item's directory
wholesale **after the export rules below have run** — nothing that must
survive is allowed to live only there.

It lives at one of two places, and its presence at either is what opts the
repository into the workflow. There is no config key. **Shared mode** keeps
it at `<repo>/seal/` and commits it — gitignored files don't follow
worktrees or other machines — so CI and every clone read it. **Local mode**
keeps the same root at `$(git rev-parse --git-common-dir)/seal/`, under the
common git directory: every linked worktree of the clone shares it, nothing
under it is ever a commit candidate, and no `.gitignore` line is needed.
What local mode gives up is CI — the pull-request checks read committed
files — and any other machine, which starts empty. **Switching is
`seal mode local` or `seal mode shared`**, which moves the root, stages the
change, carries `.github/workflows/hygiene.yml` in or out where it can and
says so where it cannot, and writes the mode into `config.md` beside this
file; you commit. `seal mode` alone says
where the root is and what that row claims, and `seal mode --check` — which
the pull-request checks run — exits non-zero when the two disagree. The row
is never read at runtime: the folder's location is the only signal, and the
plugin README's *Shared or local* section has the by-hand move as well,
with both paths asked of git so the commands land the same from a
subdirectory: local → shared is
`mv "$(git rev-parse --git-common-dir)/seal" "$(git rev-parse --show-toplevel)/seal"`,
`git add "$(git rev-parse --show-toplevel)/seal"` and a commit; shared →
local is `git rm -r --cached "$(git rev-parse --show-toplevel)/seal"`,
`mv "$(git rev-parse --show-toplevel)/seal" "$(git rev-parse --git-common-dir)/seal"`
and a commit of the removal.

**`seal export` and `seal import` are the way across between machines**, and
the only one there is: local mode's records reach no other clone by
themselves. `seal export` zips this root alone; `seal import` merges a zip
back and never overwrites a file, so a name already here keeps its bytes and
the incoming copy lands beside it as `<name>.incoming<ext>`. What sits
*beside* this root under the git directory is what must not travel — the
smith mark, the worktree choices, the review and parity marks, any lease, and
the last export's manifest at `specseal-last-export.json`. The export walks
this directory and nothing else, which is why the root has to be its own.

Nothing reads `.specseal/` or a top-level `specs/` any more; a
repository still holding them is moved into `<repo>/seal/` once, at session
start, by the plugin.

**The throwaway opt-out is the file `.git/specseal-scratch`, and it cannot be
committed.** Where it exists, every gate reads the repository as one that
never opted in and says nothing. It is for a repository built to be thrown
away — a fixture made by hand to reproduce a gate decision — and it lives
under the git directory because its predecessor, `.specseal/scratch`, sat in
a committed directory and one committed there silently turned the workflow
off in every clone.

## Export rules — drain before closing

| Item still here | Destination |
|---|---|
| Verified facts (`seal/specs/<work-item-id>/evidence-todo.md`) | `seal/ledger/<work-item-id>.md` — this work item's spec-clause ↔ coordinate rows |
| Tests to plant (`seal/specs/<work-item-id>/tests-todo.md`) | the implementation commit — or `seal/follow-up.md` if blocked on prerequisite work |
| Open decisions | the policy document's open-questions section |

Closing without exporting leaves the list where nothing looks for it — a
prescribed test unplanted, a verified fact unmerged.

## Layout

```
seal/
├── README.md            this file
├── ledger.md            spec clause ↔ code coordinates: the gathered ledger,
│                        which each release folds the fragments into
├── ledger/
│   └── <work-item-id>.md  one work item's rows while it is in development —
│                          folded into ledger.md at the release, then removed
├── config.md            what this repository says about itself, one row per
│                        item — `Commit and pull request language`,
│                        `Record language`, and `Mode`, which `seal mode`
│                        reads and writes. Optional: no file and no row both
│                        mean the default, and `Mode` has none — an absent
│                        one is filled in from where the root is
├── parity.md            migration config, only where one is declared
├── follow-up.md         schedulable items in a repository with no tracker
└── specs/<work-item-id>/  one work item, whole
    ├── routing.md         which way it was routed, written before the first edit
    ├── spec.md · plan.md · questions.md · overview.md · changelog.md
    ├── rounds/
    │   └── round-N.md     target SHA · Pass · who checked the fixes · verdicts · executed probes · inherited coordinates · deferrals
    ├── tests-todo.md      regression tests to plant, destination file per row
    └── evidence-todo.md   facts to merge into the evidence ledger
```

There is no task list here and no directory for one. `plan.md`'s Phases table
is where the work records how far it got, in a Status column whose closed value
is the commit that closed the phase — a past state someone can open, rather
than a tick anyone can type.

Reports meant for humans go to PR comments; this directory is for the **next
session** — the two audiences never share a file.
