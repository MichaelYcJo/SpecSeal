# _ai/ — inter-session workspace

This directory exists for AI sessions to hand work to each other. It is safe
to delete wholesale **after the export rules below have run** — nothing that
must survive is allowed to live only here.

It is **committed** (gitignored files don't follow worktrees or other
machines) but short-lived: each `review-history/PR-<n>/` directory is deleted
in a cleanup commit before its PR merges.

## Export rules — drain before deleting

| Item still here | Destination |
|---|---|
| Verified facts (`evidence-todo.md`) | `docs/policies/<domain>/_evidence.md` |
| Tests to plant (`tests-todo.md`) | the implementation commit — or `docs/policies/<domain>/_follow-up.md` if blocked on prerequisite work |
| Open decisions | the policy document's open-questions section |

Deleting without exporting is discarding the list.

## Layout

```
_ai/
└── review-history/
    └── PR-<n>/          ← one directory per PR so parallel reviews don't clobber
        ├── round-N.md      target SHA · verdicts · executed probe results · inherited axes
        ├── tests-todo.md   regression tests to plant, destination file per row
        └── evidence-todo.md facts to merge into the evidence ledger
```

Reports meant for humans go to PR comments; this directory is for the **next
session** — the two audiences never share a file.
