# 1788993115-a-payload-is-written-again-on-every-spawn — phase 2

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-2.md
— what this phase of the build did, written by the implementer when the
phase closed. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `378c63f` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build phase 2 of `plan.md`'s Phases table and nothing past it: the marker
and the check
(`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`,
deriving agents from the `agents/*.md` glob and each one's `skills:`,
failing on a marked heading in an injected file and on an
`orchestration.md` under any `skills:`, red-first by planting in a temp
copy); the three sections marked in `skills/implement/SKILL.md` and the
check seen red on the real tree at a commit this record names; then the
move to `skills/implement/orchestration.md` with the header and pointer
shapes from `code-review`, the two waiver paragraphs merged and kept in
`SKILL.md`, the `# RIDER:` answered and deleted; the 24 modules run and
each moved pin re-pointed and seen red against the file it left (§15).
`evidence-check .` read unscoped at the end, nothing re-stamped.

The spawn prompt labelled its facts. Executed: phase 1's verification at
`471cd69`. Read: the pointer section and the header of `code-review` as the
shapes to copy, the rider at `skills/implement/SKILL.md:390-397`, the order
the record has to show (mark, commit, red, move, green). Unverified with
this phase as answerer: which of the 24 modules go red at the move, and
whether `tests/test_a_moved_rule_leaves_its_definition.py` is untouched.

## What this phase found

**The red commit is `fc50702`.** The check was committed first (`7111132`),
green on the real tree and red on the planted trees; the marking commit
put `### Orchestrator:` on Bootstrap, Parity setup and a new heading over
the routing span, and the real-tree case named exactly those three
headings in `skills/implement/SKILL.md` for `smith`. The move (`4e9c31c`)
turned it green again. The rider was answered in the marking commit rather
than the move, so `python3 .github/scripts/rider_check.py` exited 0 at every
commit of the phase: the sentence now says PARITY arm and migration
repository, and the rider is gone.

**Eight of the 24 modules went red at the move, 21 cases, and the plan's
list was wrong in both directions.** Red: `test_first_setup_asks_once` (10,
all through one `bootstrap()` helper reading `### Bootstrap` at level 3),
`test_waiver_decided_at_start` (6), and one case each in
`test_chain_hooks_hardening`, `test_one_word_one_meaning`,
`test_review_axes`, `test_release_hygiene`,
`test_the_settings_have_a_front_door`. Two the plan listed as known to move
never pinned `SKILL.md` text at all — `test_the_mode_question_is_asked_once`
and `test_the_mode_is_a_row_and_a_command` name
`skills/implement/scripts/seal.py` and stayed green. One the plan listed as
known to stay went red: `test_the_set_a_work_item_always_has` read the
words *one file* in the new pointer section as a file count. The prose was
reworded to *one declaration* rather than the guard widened; the heading in
`orchestration.md` keeps the spec's wording, and that file is not in the
guard's corpus. `test_a_moved_rule_leaves_its_definition.py` is green: its
corpus is `agents/*.md` and the contract, confirmed by running it.

**Each re-pointed case was seen red with its sentence stashed from the file
it now reads, 21 of 21**, restored from bytes kept in the script rather
than from HEAD. The ten bootstrap cases share one helper, so eight of them
were reddened by stashing the `## Orchestrator: Bootstrap` heading and the
other two by the sentence each pins (`Ask only here`, `seal mode`). The
per-command waiver case (`test_the_skill_keeps_the_token_as_a_per_command_waiver`)
stayed green on `SKILL.md` and was not touched, because the merged
paragraph keeps *waives **one command*** and *routes **a work item***.

**An absence assertion goes vacuous at a move.** Three in
`test_first_setup_asks_once` and two in the two `no marker at all` cases
forbade a sentence in `SKILL.md`; after the move they would have passed
with the sentence sitting in `orchestration.md`. Each now reads both
halves. `test_the_release_target_is_asked_before_the_work_starts` is the
opposite shape: it pins the branch question (moved) and the yes/no tell
(stays, `spec.md` item 3), so its implement side reads the two files
concatenated.

**Two failures in the run were not the move's.**
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` fails
because this work item has no `overview.md` yet; it fails identically on
the base `471cd69` (run there from a `git archive` copy) and phase 4 closes
the memo. Nothing else in the 29 modules run (the 24, the new check, the
three that name `Orchestrator:`, `test_a_moved_rule…`,
`test_every_agent_reads_the_contract`) was red.

**The check reads the meter's parser.** `findings()` imports `frontmatter`
and `agents_in` from `skills/verify/scripts/payload_meter.py`, so the list
of files it checks is the list the meter measures. It reads the definition
itself as well as each listed skill, tracks code fences so a quoted heading
is not a section, and names a listed skill the tree does not ship. Five
mutations — `##` only, fences ignored, an `orchestration` entry allowed,
the definition skipped, a missing skill silent — each turned at least one
planted case red; the module is green on the restored file.

**What moved, in numbers.** `SKILL.md` went from 45,627 to 32,236
characters; `orchestration.md` is 16,411, of which 14,949 are the moved
text (the rest is the header). Its prose fits the 88-column wrap limit at
birth (83, measured), so it is covered by `test_docs_line_wrap.py` from
this commit, the way `code-review`'s was.

**For phase 4, pointers the move left behind.** Inside the moved text,
the Bootstrap bullet *They fill through the feedback rule below* now
points at a section in the other file (`SKILL.md` §2). `SKILL.md`'s own §2
pointers were fixed here (`(§1)` and *§1's table* both name
`orchestration.md` now). Every document outside the skill that names the
Bootstrap is `spec.md` item 5 and phase 4's.

**`evidence-check .` at `378c63f`, read and not re-stamped:** 1047 ok,
6 drifted, 2 broken. Broken: the two rows anchored on
`skills/implement/SKILL.md#"### Bootstrap — create what's missing"` (one
nested under `## Document layout`) — the anchor moved with its text, so
phase 4 removes them from `seal/ledger.md` and re-states them in the
fragment at the new coordinate. Drifted: `skills/implement/SKILL.md#"##
Document layout — two roots, three lifetimes"`, `tests/test_docs_line_wrap.py#COVERED`,
and four test-function rows in `test_first_setup_asks_once.py` and
`test_waiver_decided_at_start.py` that this phase re-pointed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `skills/implement/SKILL.md` §*Bootstrap — create what's missing* | `skills/implement/orchestration.md` §*Orchestrator: Bootstrap — create what's missing*, text unchanged |
| `skills/implement/SKILL.md` §*Parity setup — deriving what can be derived* | `skills/implement/orchestration.md` §*Orchestrator: Parity setup — deriving what can be derived*, text unchanged |
| `skills/implement/SKILL.md` §1, from *How this work is routed is one of them* up to *Once the batch is answered*, less the two waiver paragraphs | `skills/implement/orchestration.md` §*Orchestrator: how the work is routed — three axes, one question, one file*, text unchanged except the arm sentence |
| the two waiver paragraphs' separate form (*`[no-review]` still works* and *For a change that belongs to no work item*) | one paragraph in `SKILL.md` §1 opening *A waiver is one command's*, naming `routing.md` rather than a table it cannot see |
| the `# RIDER:` at the wake/quiet table (`Verified 2026-09-08 against "### 1. Read the spec before the code"@908ef9e0`) | nothing — it asked for the arm to be named in the sentence, and the sentence names it |
| the anchor `skills/implement/SKILL.md#"### Bootstrap — create what's missing"` that two `seal/ledger.md` rows cite (BROKEN at `378c63f`) | phase 4: removed from `seal/ledger.md`, re-stated in `seal/ledger/1788993115-a-payload-is-written-again-on-every-spawn.md` at the `orchestration.md` coordinate |
