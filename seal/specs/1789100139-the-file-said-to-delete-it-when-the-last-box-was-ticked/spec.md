# Feature Specification: docs/flow.md is deleted, and what it carried is placed where it is read

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #351. Milestone `release: 0.11.1`.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/issues-and-milestones.md` §*Nothing automated reads a milestone* | The plan is already unenforced state, so moving it out of the tree loses no enforcement — only a reading convenience |
| `docs/issues-and-milestones.md` §`backlog:` *is the unscheduled pool* | Scheduling is currently two acts, and one of them is the row this work removes. The document owns tracker conventions, so it is where the surviving half of the rule lands |
| `docs/release-checklist.md` §*0. Before starting* | Four of its steps are about a file that will not exist; the conflict-resolution step has nothing left to resolve |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | `docs/flow.md` is the third file every branch appended to. The other two were cured with per-work-item fragments because checkers read them; this one has no checker, so it is cured by deletion |
| `CLAUDE.md` §*The goal a design is chosen against* | Between keeping a file a person maintains by hand and moving its content to where the tracker already holds it, the second stops asking a person for the same edit each release |
| `tests/test_release_hygiene.py#RECORDS_OF_A_MOMENT` | `docs/flow.md` is exempted there as *a list headed by the version it tracks*. The exemption and its two fixture usages go with the file |

## Scope

**In.**

- `docs/flow.md` is deleted.
- `## Order inside a ticket` (its three numbered steps) moves into
  `skills/implement/orchestration.md`, which already owns how a work item
  starts. `tests/test_the_rules_have_one_owner.py`'s two cases that read
  `FLOW` move with it rather than being deleted — they pin that the draft
  pull request opens before the rounds, and that step 2 no longer defers the
  framer to a ticket.
- The one standing rule that survives the file — *a release is sized in work
  items, and three or four is the size* — lands in
  `docs/issues-and-milestones.md`. Nothing else restates it.
- `docs/release-checklist.md` loses its four `docs/flow.md` steps, including
  the conflict-resolution bullet.
- Every scheduled release milestone's description carries the release's
  purpose and the grounds for its order. Where a ticket's position has
  grounds that are not already in its own body, they go on that ticket.
- The three live references that would name a file that does not exist are
  repaired: `tests/test_release_hygiene.py` (the exemption entry and two
  fixture paths), `tests/test_a_corrected_sentence_survives_elsewhere.py`
  (the comment that cites the deleted section), and
  `skills/code-review/scripts/survivor_check.py` (two docstring citations).
- `skills/verify/scripts/broad_gate.py`'s single citation, which names
  `docs/flow.md` #103's class.
- `docs/one-root-by-lifetime.md` and `docs/one-root-by-lifetime.ko.md` lose
  the clause naming `docs/flow.md` from §*Order* — the rest of the sentence
  stands (Q3, answered **(c)**). Both editions move together or they drift.

**Out.**

- `CHANGELOG.md` and everything under `seal/specs/`. These are records of
  what was true when they were written, and a path inside one is part of the
  record.
- The rule *a branch writes this file for the rows its own work created*, and
  the rule *a shipped version's section is deleted, not kept*. Both are rules
  about maintaining `docs/flow.md`. They do not move; they end.
- Anything about how a release is cut, merged or tagged.
  `docs/branch-and-release.md` owns that and is untouched.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the order a ticket runs in has one owner, and it is a skill | Given a session starting a work item · When it reads `skills/implement/orchestration.md` · Then the three numbered steps are there, the draft pull request still opens between the smith and the warden rounds, and no other file states the sequence | `tests/test_the_rules_have_one_owner.py`, the two moved cases, seen red against the pre-move tree |
| S2 · scheduling is one act | Given `docs/issues-and-milestones.md` · When a reader asks what scheduling an issue means · Then it is the milestone alone, and the sentence naming a second act in `docs/flow.md` is gone | read; `grep -n "flow\.md" docs/` returns nothing |
| S3 · the sizing rule survives its carrier | Given the release is being planned · When a person asks how large a release may be · Then `docs/issues-and-milestones.md` says three or four work items, and exactly one document says it | `tests/test_one_word_one_meaning.py`-style grep for the sentence across `docs/`, `skills/`, `agents/` |
| S4 · the checklist has no step about a file that is gone | Given `docs/release-checklist.md` · When step 0 and step 2 are read · Then no bullet mentions `docs/flow.md`, and the quadratic-cost measurement survives without naming it | read; `grep -c "flow\.md" docs/release-checklist.md` is 0 |
| S5 · the release plan is answerable without the tree | Given only the GitHub tracker · When a person asks what is in 0.11.1 and why in that order · Then the milestone description answers both, and a ticket whose position has grounds carries them | `gh api repos/:owner/:repo/milestones` read back after the write |
| S5b · the 0.4.0 record loses the dead path and nothing else | Given `docs/one-root-by-lifetime.md` and its Korean edition · When §*Order* is read · Then the milestone sentence stands, the `docs/flow.md` clause is gone from both editions, and no version number was added to either | read, both editions; `tests/test_docs_line_wrap.py` for the 88-column bound; the six doc-scanning modules at 126 passed |
| S6 · nothing loaded names a file that does not exist | Given the whole tree with `docs/flow.md` deleted · When the loaded set is grepped · Then the only remaining hits are in `CHANGELOG.md` and `seal/specs/`, both records | `grep -rn "flow\.md" --include='*.md' --include='*.py' . \| grep -v CHANGELOG \| grep -v 'seal/specs/'` — every survivor is a record naming it as removed |
| S7 · the suite is green with the file gone | Given the deletion committed · When the broad gate runs · Then `bin/test -q`, `ruff check` and `ruff format --check` all exit 0 | `bin/broad-gate`, exit codes read directly |

## Data & interfaces

No schema, no endpoint, no payload. Three code-level surfaces move:

- `tests/test_the_rules_have_one_owner.py#FLOW` — a two-element path tuple
  that becomes the orchestration file's, or is folded into the existing
  `ORCH`-shaped constant for `skills/implement/`.
- `tests/test_release_hygiene.py#RECORDS_OF_A_MOMENT` — the
  `"docs/flow.md"` entry is removed. Two cases use that path as a fixture
  (`test_a_record_of_a_moment_keeps_every_version_it_names` and the
  `timers_in` assertion around line 574); both need an exact-path entry that
  still exists, which `docs/one-root-by-lifetime.md` is.
- `skills/code-review/scripts/survivor_check.py` — two module-docstring
  citations. One names the row that describes the check's own input; the
  other names the section listing the durable copies a deletion leaves
  behind. The second has to say what the section said, not point at it.

## Open questions → questions.md

Q1, Q2 and Q3 were answered on 2026-09-11 by the repository owner and are
recorded in `questions.md`. Q4 and Q5 belong to the work and to a
measurement; neither blocks the build.
