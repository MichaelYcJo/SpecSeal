# Implementation Plan: a payload is written again on every spawn

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Two units and a move. A meter that says what each agent's startup payload is
made of and what it costs in tokens, with every figure labelled measured or
estimated. A check that fails when a section written for the orchestrator
sits in a file an agent's `skills:` list injects. And the move the check
forces: `implement`'s orchestrator half goes to
`skills/implement/orchestration.md`, the shape `code-review` already has. A
fourth, smaller unit answers Q1: the `CLAUDE.md` block gets one source and a
script that keeps the two copies identical.

The work alters what a session reads and acts on — a skill's instructions,
a new command's output, a new pull-request check — which is the top rung of
the `implement` skill's ladder, so `spec.md` and this plan come first and
approval of this plan is the gate. The gate was passed in the owner's one
batch on 2026-09-10 (`routing.md`).

## Technical context

Existing code this builds on, as coordinates. Every one was opened by the
session that wrote this plan; the smith opens them again before building on
them (§5).

- `skills/code-review/SKILL.md` §*The orchestrator's half is a file of its
  own* — the pointer section `implement` copies the shape of, and
  `skills/code-review/orchestration.md:1-16` — the header the new file
  copies the shape of. Headings keep their names across the move (#265).
- `skills/implement/SKILL.md` — the seam is stated by paragraph in
  `spec.md` §*Scope* item 3. The `# RIDER:` at the wake/quiet table is
  answered (the arm named in the sentence) and deleted.
- `skills/verify/scripts/session_cost.py#spawn_labels`,
  `#subagent_transcripts`, `#load` — how a main transcript's `Agent` calls
  name their `subagent_type`, and where the `subagents/` directory is. The
  meter imports from this module rather than re-deriving either. The
  `agentId` a spawn's tool result carries is the basename of
  `subagents/agent-<agentId>.jsonl`; the first `assistant` record's
  `message.usage` holds `cache_creation_input_tokens` and
  `cache_read_input_tokens`, and their sum plus `input_tokens` is the
  prefix.
- `bin/session-cost` and `bin/session-cost.cmd` — the wrapper pair every
  `bin/` entry has. A case pins the pairing; find it with `grep -ln
  '\.cmd' tests/*.py` before adding the new pair.
- `tests/test_the_release_check_watches_what_ships.py` — `bin/`,
  `skills/` and `templates/` already ship; `.github/` stays home. No
  classification changes.
- The 22 test modules that name `skills/implement/SKILL.md`, from
  `grep -ln 'implement/SKILL.md\|"implement", "SKILL.md"' tests/*.py`:
  `test_a_phase_hands_the_next_one_a_record`, `test_a_rider_reaches_its_file`,
  `test_a_segments_record_says_what_it_was_asked`,
  `test_chain_hooks_hardening`, `test_docs_line_wrap`,
  `test_edits_go_through_the_edit_tool`, `test_first_setup_asks_once`,
  `test_handoff_outlives_the_merge`, `test_no_document_names_the_old_roots`,
  `test_one_word_one_meaning`, `test_review_axes`, `test_release_hygiene`,
  `test_the_handoff_before_round_one`, `test_the_fixes_close_the_record`,
  `test_the_ledger_fragments_fold_at_release`,
  `test_the_mode_is_a_row_and_a_command`,
  `test_the_mode_question_is_asked_once`,
  `test_the_pull_request_language_is_the_repositorys`,
  `test_the_rules_have_one_owner`, `test_the_records_can_be_carried_out_and_in`,
  `test_the_set_a_work_item_always_has`, `test_waiver_decided_at_start`,
  `test_the_settings_have_a_front_door`, `test_unverified_rows_close`.
  (Twenty-four names; two of them match by tuple only. #265 named eleven
  and broke five it had not named, so the rule is: run all of them, and
  re-point only what goes red.) Known to move: `test_waiver_decided_at_start`
  (pins *three axes* and the `| Implementation |` row), the four Bootstrap
  pins (`test_first_setup_asks_once`, `test_the_mode_question_is_asked_once`,
  `test_the_settings_have_a_front_door`,
  `test_the_mode_is_a_row_and_a_command`). Known to stay:
  `test_the_rules_have_one_owner`'s `IMPLEMENT` link for rule 2 (§5 stays),
  `test_the_set_a_work_item_always_has` (§3 stays).
- `seal/ledger.md` — twelve rows anchor on `skills/implement/SKILL.md#…`
  (`grep -c 'implement/SKILL.md#' seal/ledger.md`). The ones whose heading
  moves are REMOVED there and re-stated in `seal/ledger/<id>.md` at the new
  coordinate; `evidence-check --reverify` is scoped to the fragment for the
  write and unscoped for the read (`skills/code-review/orchestration.md`
  §*The check a round runs reads everything, and only a write is narrowed*).
- `install.sh:43` (`SOURCE="$REPO_DIR/CLAUDE.md"`),
  `skills/preset-setup/SKILL.md:27-28` and `skills/update/SKILL.md:61-62` —
  the three places that read the block from `CLAUDE.md` today.
- `.github/workflows/hygiene.yml` — the step goes beside *the mode the row
  declares is the mode the folder is in*, this repository's own; NOT into
  `templates/hygiene.yml`, which ships the user-facing subset.
- `CLAUDE.md` block, `## Git` — *stop and load the `implement` skill, and
  follow its Bootstrap section* has to name the file the Bootstrap moves
  to, and the block is generated from the template after phase 3, so the
  sentence is edited in the template.
- `tests/test_no_real_identifiers.py` — the committed JSON files carry a
  transcript basename and a relative root, never an absolute home path.

**What breaks in six months.** Somebody adds a section to `implement` for
the orchestrator and forgets the prefix, and the check is green because it
reads the marker rather than the meaning. That is the limit of a verbatim
check and it is the same limit `tests/test_a_moved_rule_leaves_its_definition.py`
states for itself; the reviewer's finding is what catches a paraphrase. The
second failure: the per-agent ratio drifts as the payload's language mix
changes, and the estimates drift with it while still saying `estimated` —
which is why the basis is printed on every figure and Q4 names the probe
that replaces the estimate.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Count tokens exactly through the API's token-counting endpoint | needs a key no session here has (`ANTHROPIC_API_KEY` is unset — NAME NOT IN TREE, nothing here reads it), and a meter that works only with one is a meter nobody runs | rejected as the only basis; the `basis` column leaves room for it |
| A fixed bytes-per-token ratio from published tokenizer averages | a number nobody measured on this tree, and this tree measured three agents at 2.71, 3.16 and 3.44 | rejected — the ratio is per agent, from a transcript |
| The meter as a flag on `session_cost.py` | that script measures a transcript; this one measures the tree. One script with two subjects is the shape #265 measured a skill into | rejected — a sibling script that imports the transcript helpers |
| A frontmatter field as the audience marker | machine-readable, and no shipped skill has it — two conventions for one fact | rejected (Q2) |
| Mark the sections and leave them in `SKILL.md` | the check this work adds fails on exactly that state | rejected — the move is what the check protects |
| Delete the repository's `CLAUDE.md` block | a contributor without the plugin loses the rules | rejected by the owner (Q1) |
| Keep both `CLAUDE.md` copies and check nothing | they had already drifted by one sentence when #292 measured them | rejected — the build step is the answer to the drift, not to the payload |

## Phases

Vertical slices — each phase ends with something runnable and verified. One
smith spawn per phase; this table and `phases/phase-N.md` are the handoff
between them.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `skills/verify/scripts/payload_meter.py` and `bin/payload-meter` + `.cmd`: the composition table per agent (definition, each `skills:` file, both `CLAUDE.md` files), bytes/chars/tokens with a basis on every token figure, `--sections`, `--json`, `--baseline`, `--calibrate` reading a main transcript's spawns and the baseline agent. `tests/test_the_payload_meter_says_what_it_measured.py`: a fixture tree with known sizes, a fixture transcript pair with hand-written `usage`, the basis label, the missing-baseline refusal, the delta. `payload-before.json` written from this session's main transcript (`--calibrate`) and committed here | `bin/test tests/test_the_payload_meter_says_what_it_measured.py -q` — each case seen red first (§15); `bin/payload-meter --calibrate <main transcript> --json` run and its output read; the wrapper-pair case green | `2c05517` |
| 2 | The marker and the check: `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` (derives agents from the `agents/*.md` glob and each one's `skills:`; fails on a marked heading in an injected file and on an `orchestration.md` under any `skills:`; red-first by planting in a temp copy). The three sections marked in `SKILL.md` and the check **seen red on the real tree** at a commit the phase record names. Then the move to `skills/implement/orchestration.md` with the header and pointer shapes from `code-review`, the waiver paragraphs merged and kept, the rider answered and deleted, the check green. The 24 modules run and each moved pin re-pointed and seen red against the file it left | `bin/test tests/test_a_section_marked_for_one_role_reaches_only_that_role.py <the 24 modules> -q`; `python3 .github/scripts/rider_check.py` clean; `evidence-check .` read for the rows that drifted (not yet re-stamped — phase 4) | `378c63f` |
| 3 | `templates/claude-md-block.md` (the block, markers included, with the Bootstrap sentence now naming `skills/implement/orchestration.md`); `.github/scripts/claude_block.py --write` / `--check`; `install.sh` reading the template; the hygiene step; `preset-setup` and `update` naming the template path; `tests/test_the_claude_md_block_has_one_source.py` with the one-byte mutation and the `install.sh` `SOURCE` pin. `README.md` / `README.ko.md` where they say the block lives in `CLAUDE.md` | `bin/test tests/test_the_claude_md_block_has_one_source.py tests/test_the_release_check_watches_what_ships.py tests/test_release_hygiene.py -q`; `python3 .github/scripts/claude_block.py --check` exit 0 read directly; `bash install.sh /tmp/probe-CLAUDE.md` and the file read | `77ab860` |
| 4 | `payload-after.json` from the same transcript and the delta; the twelve `seal/ledger.md` rows sorted into removed-and-restated or left; `seal/ledger/<id>.md`; `changelog.md` with the delta table and the five-minute finding; `overview.md` closed; the `docs/flow.md` tick for #292; every remaining document pointer to a moved section (`agents/smith.md`, `templates/*.md`, `docs/*.md`, `README*.md`); the narrow verification of every module the branch touched; hand to the review chain | `bin/test tests/test_a_row_points_by_content.py tests/test_the_ledger_fragments_fold_at_release.py tests/test_the_changelog_is_gathered_at_release.py tests/test_no_real_identifiers.py tests/test_no_document_names_the_old_roots.py tests/test_docs_line_wrap.py -q`; `evidence-check --ledger 'seal/ledger/<id>.md' --reverify .` then `evidence-check .` read unscoped; `survivor-check --range <base>..HEAD` read | `26e4236` |

**Why this order.** The meter first, because the before-number has to be
taken before anything moves, and the check second because it is what makes
the move a move rather than an edit — marked, red, moved, green, in that
order, on the real tree. The block's build step is independent of both and
goes third so that the sentence it edits (the Bootstrap pointer) already has
somewhere to point. Records last, from the after-number.

**Every phase commits.** This branch squashes into `release/v0.10.0` and
`routing.md` is on disk, so the review arm of the commit gate is silent and
an intermediate commit costs nothing. An uncommitted change is invisible to
the reviewer.

This table is also where the work records how far it got. There is no
separate task list.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`. **Re-read this column after any rebase.**

## Verification scope, per phase

Narrow and often, broad once. Each phase runs the modules its own diff can
break, named in the table. **No phase runs the full suite, repository-wide
lint or a typecheck** — the broad gate runs once, after the review rounds
settle, and the orchestrator owns it. Every phase hands over with the suite
labelled `unverified` and the orchestrator named as its answerer.

Exit codes are read directly: `cmd >/dev/null 2>&1; echo $?`, never
`cmd | tail; echo $?`.

## Operational impact

- **A new command on every user's PATH**, `payload-meter`, and a new script
  under `skills/verify/scripts/`. Both ship, so the release moves the
  version.
- **`install.sh` reads `templates/claude-md-block.md`.** A clone at this
  release or later; an older clone's `install.sh` still reads its own
  `CLAUDE.md` and is unaffected. `/specseal:update`'s diff command changes
  its path with it.
- **The `CLAUDE.md` block changes one sentence** — the Bootstrap pointer —
  so every user sees a block diff at their next `/specseal:update`, which
  is the path that already exists for that.
- **The hygiene workflow gains one step**, this repository's own; nothing
  reaches `templates/hygiene.yml`.
- **No migration, no new environment variable, no new dependency.**
- **Prompt budget: zero.** Nothing here adds a question to any session.
