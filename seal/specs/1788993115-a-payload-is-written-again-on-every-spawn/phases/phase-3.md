# 1788993115-a-payload-is-written-again-on-every-spawn — phase 3

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/phases/phase-3.md
— what this phase of the build did, written by the implementer when the
phase closed. -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `77ab860` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build phase 3 of `plan.md`'s Phases table and nothing past it: the `CLAUDE.md`
block gets one source. `templates/claude-md-block.md` holds the marker block,
with the `## Git` bullet's *load the `implement` skill, and follow its
Bootstrap section* now sending the reader to
`skills/implement/orchestration.md`, because a `Skill implement` load no
longer carries that section; `.github/scripts/claude_block.py --write` /
`--check`, exit 0 / 1 / 2 as `spec.md` §*Data & interfaces* states, stdlib
only, with the interpreter-floor guard `round_record.py#below_floor` was
written to be copied; `install.sh` reading the template instead of the
repository's `CLAUDE.md`; a hygiene step beside *the mode the row declares
is the mode the folder is in*, with a comment in that file's voice, and
nothing in `templates/hygiene.yml`; the `preset-setup` and `update` skills
naming the template path; `README.md` and `README.ko.md` naming the template
as the source and `CLAUDE.md` as a generated copy;
`tests/test_the_claude_md_block_has_one_source.py` with the one-byte mutation
seen red, `install.sh`'s `SOURCE` pinned, the two runtime readers pinned to
the template path, each case seen red first. `~/.claude/CLAUDE.md` is the
owner's and is not written; `install.sh` runs only against a scratch target.

The spawn prompt labelled its facts. Executed: phase 2's verification re-run
at `41af142`, 363 passed and the one `overview.md` failure that is phase 4's.
Read: the marker region at `CLAUDE.md:1-17`, `install.sh:43`, the two skill
readers, the hygiene step's neighbour, `README.md:44` and `:335`. Unverified
with this phase as answerer: whether any test pins `install.sh`'s `SOURCE`
line or the block's line count.

## What this phase found

**No test pinned `SOURCE` or the line count, and two described the source
in prose.** The seven modules that match `install.sh\|specseal:start` were
each read. `test_chain_hooks_hardening` reads `install.sh` for un-namespaced
commands; `test_no_document_names_the_old_roots`, `test_release_hygiene` and
`test_the_release_check_watches_what_ships` list it by name;
`test_broad_gate_rule` and `test_first_setup_asks_once` read the block out of
`CLAUDE.md` and were left reading it, because `--check` holds that copy
identical to the template and a case reading either reads the same bytes.
`test_first_setup_asks_once` and `test_the_mode_question_is_asked_once` said
in their prose that `install.sh` copies the block out of `CLAUDE.md`; both
now say what it copies. `README.md`'s *12 always-on lines* still counts: the
block has 12 non-blank lines between its markers before and after the
sentence changed. `uninstall.sh` names the markers and no source, and is
untouched.

**The block grew by 50 bytes, not 139.** The first draft of the new sentence
explained why the pointer moved (*which a `Skill implement` load no longer
carries*); that explanation would ride every spawn in every repository with
the block installed, twice. The pointer alone is what a reader needs, so the
sentence is *stop and follow the Bootstrap section of
`skills/implement/orchestration.md`, the `implement` skill's orchestrator
half*. `templates/claude-md-block.md` is 3,158 B against the 3,108 B cut from
`CLAUDE.md` at the start of the phase.

**Red first, in three ways.** The module was written before the script: 10
red and 5 green on the first run, and two of the five — the exit-2 cases —
were green for the wrong reason, because Python exits 2 for a script it
cannot find. Those two were seen red by mutation instead (the script's
`return 2` turned to `return 0`). Three cases pin edits that landed in later
commits — the runtime readers, the hygiene step, the Bootstrap sentence — and
were red at `d6305b4`, green at `3ee7c00`, `941c5c5` and `b932604`
respectively. The sweep over the script's units: *compare says equal*,
*write writes nothing*, *no markers is exit 0*, *a mode is optional*, *the
line number is off by one*, *the guard lets everything through* — each
turned at least one case red, restored from bytes kept in the sweep script
and never from HEAD.

**One mutation survived, and the branch it hit was dead.** `first_difference`
had a branch for one block being a prefix of the other, printing `<end of
block>`; a case was written for it and stayed red on the restored file,
because `block()` cuts both files at the line holding the end marker, so a
block with a line more or fewer differs at some line before the shorter one
runs out — the marker line at the latest. The branch is removed and the
case pins the shape that is reachable: the template's end-marker line against
the copy's extra rule. `quote()` lost its `None` arm with it.

**The floor guard is live, on both sides of the floor.** Executed: a copy
with `FLOOR = (99, 0)` exits 2 naming 99.0 and this interpreter, and the real
file under `/usr/bin/python3` (3.9.6, the Xcode shim) exits 2 with the
sentence and no traceback. The script uses no construct
`test_a_script_says_which_interpreter_it_needs.py`'s pattern finds, so it
takes no `CLASSIFIED` row there; its own module pins the raised-floor copy
the way that file does for `round_record.py`, seen red with the guard's
comparison replaced by `True`.

**A sentence the update skill almost shipped.** The first draft said a clone
*at a release before 0.10.0* has no template; `test_release_hygiene.py`
refuses a loaded file naming a version at or above the running one, and the
sentence was cut before the commit. The marketplace clone is refreshed before
the diff runs, so the case it described does not arise.

**What the check reaches and what it does not.** The drift #292 measured is
between the repository's copy and an installed one, on a user's machine,
where no CI step can read it. The step holds the repository's copy — the one
the installer used to read — to the template, which is what makes the next
installed block the template's. It found nothing at birth, because the copy
was generated in the commit that added it. The comment in `hygiene.yml` says
so.

**Measured at `77ab860`, all executed.** The phase's verified-by set
(`test_the_claude_md_block_has_one_source`, `test_the_release_check_watches_what_ships`,
`test_release_hygiene`): 76 passed. The wider narrow set — those plus
`test_first_setup_asks_once`, `test_broad_gate_rule`,
`test_ci_gives_the_checks_what_they_need`, `test_docs_line_wrap`,
`test_the_mode_question_is_asked_once`, `test_no_document_names_the_old_roots`,
`test_chain_hooks_hardening`, `test_a_corrected_sentence_survives_elsewhere`,
`test_unverified_rows_close`, `test_the_mode_is_a_row_and_a_command`,
`test_one_word_one_meaning`, `test_a_script_says_which_interpreter_it_needs`,
`test_no_real_identifiers`: 466 passed, 1 failed, the failure being
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, phase
4's. `claude_block.py --check` exit 0, read directly. `bash install.sh
/tmp/probe-CLAUDE.md` exit 0 and the probe file identical to the template
byte for byte, then removed. `rider_check.py` exit 0. `ruff check` and
`ruff format --check` clean on the three Python files touched.
`survivor-check --range 41af142..3ee7c00`: 11 sentences removed, none still
standing. The full suite, repository-wide lint and typecheck: unverified,
the orchestrator's after the rounds.

**For phase 4.** `evidence-check .` at `3ee7c00`, read and not re-stamped:
1043 ok, 10 drifted, 2 broken. The 2 broken and 6 of the drifted are phase
2's list unchanged. Four drifted rows are this phase's:
`skills/update/SKILL.md#"## Procedure"`, `README.md#"### Updating"`,
`README.ko.md#"### 업데이트"`, and
`CLAUDE.md#"## Git">"Routing, decided at the start"`. `templates/` ships, so
the release moves the version — already the case from phase 1's `bin/`
entry.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `install.sh`'s `SOURCE="$REPO_DIR/CLAUDE.md"` | `SOURCE="$REPO_DIR/templates/claude-md-block.md"`, and the comment above it saying why |
| the sentence *stop and load the `implement` skill, and follow its Bootstrap section* in the block | *stop and follow the Bootstrap section of `skills/implement/orchestration.md`, the `implement` skill's orchestrator half* — in `templates/claude-md-block.md`, and in `CLAUDE.md` by `--write` |
| `skills/preset-setup/SKILL.md`'s *in this plugin's CLAUDE.md* | the same step, naming `$CLAUDE_PLUGIN_ROOT/templates/claude-md-block.md` |
| `skills/update/SKILL.md`'s diff against `~/.claude/plugins/marketplaces/specseal/CLAUDE.md` | the same command against `…/marketplaces/specseal/templates/claude-md-block.md` |
| `CLAUDE.md`'s comment *install.sh distributes only the marker block above* | the comment in the same place, saying the block above is a generated copy of the template and how it is regenerated |
| the `<end of block>` branch of `first_difference` and `quote`'s `None` arm | none — unreachable, as the docstring on `first_difference` says |
