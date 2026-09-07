# a git call that fails reads as no remote — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. -->

📋 implement applied
· spec:     ticket #111 (in full, including what it deferred);
            `seal/specs/1788789329-…/routing.md` at `77005f8`;
            `seal/specs/1788398967-local-modes-records-never-leave-the-clone/spec.md`
            §`manifest.json` and §*What the import refuses* — the prior
            contract for the two fields, superseded here and argued in
            `spec.md` §*What this supersedes*;
            `docs/one-root-by-lifetime.md` §*What each mode gives up*;
            `CLAUDE.md` §*no real identifiers*, §*a change writes fragments*;
            `seal/config.md` (no `Record language` row, so English);
            `seal/follow-up.md` — nothing there is a prerequisite of this work
· evidence: `seal/ledger/1788789329-a-git-call-that-fails-reads-as-no-remote.md`,
            R1–R4, fourteen anchors, stamped by
            `evidence-check --reverify --ledger '<this fragment>'` (the scoped
            write form, so no anchor outside this work item was re-stamped)
· verified: **executed** — `bin/test` over the export/import module and
            fifteen record- and document-scanning modules, exit 0; eleven
            mutations of the new units, all killed; `ruff check` and `ruff
            format --check` on every Python file touched, exit 0;
            `evidence-check` on the fragment, exit 0; git's own exit codes
            probed against a scratch repository before the shape was chosen.
            **Unverified** — the full suite, which is the orchestrator's

## Why this work exists

`seal import`'s refusal — the one thing standing between two projects' records
landing in one root keyed by work-item id — was switched off by any git
failure, because `git()` answered `""` for *there is no remote* and *the
question could not be answered* alike; now the second refuses, and the export
stops writing `""` into the zip for the receiving machine to read as a fact.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The `remote` field's states | #81's `spec.md`: *"`origin`'s fetch URL, or `""` when the repository has no `origin`"* — two states | Three: a URL, `""`, and **absent** | The two-state contract has no spelling for the export failing to look, which is the defect. #81's records are left as they stand — they record what was decided then — and the new contract is `spec.md` §*Data & interfaces* here |
| The `head` field's states | #81's `spec.md`: *"the HEAD SHA at export, or `""` in a repository with no commit"* | Present-or-absent, no empty | `git rev-parse HEAD` prints a SHA whenever it succeeds, so there is nothing a present-and-empty `head` could mean that absence does not say better. The one reader already treated the two alike |
| How many call sites the class holds | Ticket: *"Four are left"* | **Five** | The ticket did not count `:953`, the second `git()` inside the refusal message. The handoff labelled the number `[unverified]` and it was checkable: `grep -n 'git(' seal.py` names every call site by construction |
| Which git failure the cases reproduce | The ticket's examples are a timeout and a git not on PATH | Injected at `subprocess.run`, one git question deep | Neither can be built out of a repository on disk: a `.git/config` broken enough to fail `config --get` also fails the `rev-parse --show-toplevel` that resolves the root, so the command stops one screen earlier with a different message (both exit 128, measured). A duplicated `url =` line answers with the last value at exit 0 |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `agent-contract` §2 reserves them; sixteen modules were run narrowly instead | the orchestrator, before the pull request |
| `Ran by` in `phases/phase-1.md`, `phase-2.md` and `phase-3.md`. The spawn prompt named no model, and `templates/sdd-phase.md` forbids a segment sourcing that from its own idea of what it is | the orchestrator that spawned this segment |
| Whether `git config --get` exits 1 for an unset key on git builds other than 2.50.1. The rule is measured on one build; a git that changed that code would read an unset remote as unanswerable | the repository owner, if a user reports a refusal on a repository that genuinely has no remote. It fails toward a refusal with a flag rather than a silent merge, and S3 is the case that would go red |
| Behaviour on Windows. Nothing here touches a path separator, and the injected failures are process-level, so no platform guarantee is being rested on (`agent-contract` §13) — but the module was not run there | CI's Windows leg |

## Not done

**`porcelain`, `indexed`, `tracked` and `gitlinks_under_root` were not moved
onto `git_asked`.** Each already reads its own return code and each already
draws the line this work is about, so the change would be a refactor the
ticket did not ask for, touching four guards to alter nothing. What it would
buy is one body instead of four; what it would cost is a diff a reviewer has
to read for a behaviour change that is not in it. The promotion is available
whenever one of them next needs editing for a reason of its own.

**The format number stays `1`.** Moving it would refuse every zip an older
build wrote, for a change older builds tolerate: no field was renamed or
repurposed, and format 1's only reader of the two already went through
`manifest.get`.

**`other_worktrees` got a sentence and no code.** It is the one member of the
class where a failure loses nothing and claims nothing falsely, which is what
the ticket asked for and what the docstring now says.

## Fed back into the spec

Two clauses, both *inferred during implementation* and both in `spec.md` here
rather than in #81's:

- **`git config --get` exits 1 for an unset key**, so that one command's
  non-zero code is an answer. Nothing had written this down, and it is the
  fact the whole three-state design rests on.
- **A manifest with no `remote` key refuses.** The ticket said to make the
  field absent so the receiving machine can tell; it did not say what the
  receiving machine should then do. Refusing is the only act available that
  uses the distinction, and `questions.md` A2 records that a different answer
  would not have changed the export side.
