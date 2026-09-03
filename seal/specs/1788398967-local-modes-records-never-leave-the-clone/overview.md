# 1788398967-local-modes-records-never-leave-the-clone — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"Shared or local" (the four
            export/import bullets), §"The opt-in signal is the root itself",
            §"The proposed tree"; `seal/README.md` §"Export rules";
            `CONTRIBUTING.md` §"House rules"; issue #81's done-when list;
            this work item's `spec.md`, `plan.md`, `questions.md`,
            `routing.md`
· evidence: 12 rows in `seal/ledger/1788398967-local-modes-records-never-leave-the-clone.md`;
            2 rows in `seal/ledger.md` re-verified and re-dated, both citing
            `hooks/optin.py#home_at`, which this work rewrote
· verified: **Executed** — `tests/test_the_records_can_be_carried_out_and_in.py`
            (51), `tests/test_optin_home.py` (42), and the neighbouring files
            named under Not verified. **Read** — the Windows wrapper, which no
            runner here executes

## Why this work exists

Local mode's records lived only in the clone that wrote them, so the mode's
honest description was *lose it*; `seal export` and `seal import` make it
*take a copy*, and make the mode switch possible between two machines rather
than only within one.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `extractall` is a path-traversal sink | `spec.md` and `plan.md` both said so before any code was written; the probe said otherwise | Corrected both documents in place, kept the member-name validation, and added the check for the escape that DOES exist | Measured 2026-09-03 under CPython 3.13.9 and 3.12.11: `seal/../../escaped.md` extracted to `<dest>/seal/escaped.md` and nothing outside. The claim would have been a docstring, a spec section and a changelog line all wider than what runs |
| The reminder's grammar at N=1 | The design and the issue both write `N work items changed since the last export`; at N=1 that reads `1 work items` | Kept the line exactly as written | The line is quoted text in an acceptance criterion. Reading it as a template with a grammar rule attached is a change to the criterion, which is the owner's to make. `plural()`'s docstring says so at the code, and this row is where it can be overturned |
| Where a work item's digest comes from | The design says the reminder counts work items; it does not say what a work item's bytes are | `specs/<id>/` **plus** `ledger/<id>.md` | One work item writes in two places, so a release whose only output was evidence rows is still a work item that changed. Inferred — see *Fed back into the spec* |
| `seal export` in shared mode | The design is silent; the handoff guessed "probably a message rather than a zip" | A message, and exit 1 | The record is already committed, so the zip would be a second copy nothing keeps current. Exit 1 rather than 0 matches `fold_ledger.py`'s *nothing to fold*, so `seal export && cp …` cannot copy nothing and report success. Recorded as Q3 with the alternative |

## Not verified

| Item | Who must answer |
|---|---|
| `bin/seal.cmd` on Windows — that `py -3` is preferred and `python` is the fallback is asserted by reading the file, never by running it | the Windows CI job on the release pull request, or the repository owner on a Windows machine |
| The full suite, `ruff check .` and a repository-wide format check | the review orchestrator's broad gate, once the rounds settle. This branch ran the tests for what it touched and lint on the files it touched, per the verification-scope rule |
| Whether `<git-common-dir>/specseal-last-export.json` should be listed anywhere a person reads besides `seal/README.md` — the gate table in `README.md` names the other markers under `.git/` | the repository owner |
| Whether the three limits are the right numbers — 32 MB a member, 512 MB a zip, 20,000 members. Round 1 measured the unbounded read (408 KB declaring 400 MB wrote 419 MB in 0.2 s) and the limits answer it, but no record has approached any of them | the repository owner, at the first root that meets one |
| Whether a root that is itself a symbolic link should be refused. `home_at` follows it, so it reads as a valid root and an import writes through it — which is also what a person who deliberately put the root elsewhere would want | the repository owner |

## Not done

**No `--list` on the reminder.** `seal export --check` prints one number and
nothing else, which is what the design specifies, and a reader who wants to
know *which* work items changed cannot get it from this command. A flag was
within reach and not taken: the criterion says *and nothing else*, and adding
a flag to a line whose whole point is being one line invites the next flag.

**No unified diff between a collision's two files.** The import reports which
file landed where, and reading the pair is left to the person. Generating a
diff would make the command look like it was helping with a merge it
deliberately refuses to do.

**Nothing was uploaded, offered to upload, or given a default destination
beyond the clone's parent directory.** The design is explicit that where the
copy goes is the user's business, and a default that reached a network would
need the three limits `CONTRIBUTING.md` puts on the two hooks that do.

**The `settle` step is untouched.** `seal` is one command with subcommands
precisely so a later `settle` has somewhere to go, and this work item added
none.

## Fed back into the spec

- **A work item's bytes are `seal/specs/<id>/` together with
  `seal/ledger/<id>.md`** — *inferred during implementation*. The design
  names the reminder's unit and never says what belongs to it. One work item
  writes in both places, so counting only the first would report 0 for a
  release whose output was evidence rows. A planner may overturn it; the
  consequence is confined to `work_item_of`.
- **The manifest carries a `format` number and an import refuses one it does
  not know** — *inferred during implementation*. The design names the
  manifest's two fields (remote, HEAD) and not its versioning. A zip whose
  fields moved, read by a build that assumes the old ones, places records at
  the wrong paths, which is the operation this command exists to make safe.
- **A collision keyed by path, not by work-item id** — *inferred during
  implementation*. The design says files are keyed by work-item id and that a
  collision lands as `<id>.incoming.md`, which reads exactly for a ledger
  fragment (one file per id) and does not say what happens to
  `specs/<id>/spec.md`. One rule — the incoming copy lands beside the file it
  collided with — produces the design's spelling where the design's example
  applies, and covers every other file without a second rule.
