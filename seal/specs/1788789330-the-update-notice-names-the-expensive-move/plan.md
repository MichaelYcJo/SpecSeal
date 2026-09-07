# Implementation Plan: the update notice names the expensive move

<!-- seal/specs/1788789330-the-update-notice-names-the-expensive-move/plan.md — HOW, in phases.
This is the Design Gate's artifact. -->

## Summary

Fifteen sentences across five files say *restart* where the repository has a
measured cheaper move. Each gains the reload, what a reload was measured to do,
and what nobody measured about it. The notice's wording is pinned by a case
seen red first.

The work alters observable behaviour — a hook's output and a skill's
instructions — so it sits on the top rung of `implement` §3 at file one, and
this plan is the gate. Routing was answered before the first edit and is
recorded in `routing.md`.

## Technical context

- `hooks/version-check.py#notice` builds the whole systemMessage as one
  concatenated literal; `:151` is its last fragment. The function takes
  `(have, want)` and touches nothing else, so the edit cannot reach the three
  limits the module's other tests guard.
- `hooks/version-check.py`'s module docstring, third paragraph, carries the
  same claim one level up.
- `tests/test_version_check.py:69` asserts `"restart" in msg.lower()` inside
  `test_the_warning_names_both_commands_in_order`. That assertion stays — the
  reload is added beside the restart, not in place of it — and a second case
  carries the new wording.
- `skills/update/SKILL.md` is not in `tests/test_docs_line_wrap.py`'s
  `COVERED`, but it was written wrapped at 79 columns; the edits keep that.
- Both READMEs **are** covered at 88 display columns, Korean counted at two
  columns per codepoint. `CONTRIBUTING.md` requires the pair to move together.
- `tests/test_release_hygiene.py` refuses a loaded file naming a version at or
  above the running one (0.9.0). No edit names a version.

**What breaks in six months.** Someone measures the unmeasured half and the
texts then understate it. That is the cheap direction of failure: the sentences
name what would settle it, so the person holding the answer knows which
sentences it belongs in. The expensive direction — asserting the reload is
enough and being wrong — leaves a user with a half-loaded plugin and no way to
tell.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Replace *restart* with *reload* | The ticket's own summary — *"a full restart is not required"* — is broader than run 6, which edited the **running** version's own directory and shows nothing about picking up a new one. A user who reloads and is told that is enough gets a plugin that did not move, silently | **rejected.** A ticket is a request, not an authority |
| Name the reload and say nothing about hooks or agent definitions | The ticket's second *Done when* exists to refuse exactly this. A reader infers from silence that the reload covers everything, which is the assertion nobody measured | **rejected** |
| Name the reload, say what was measured, say what was not, name the run that would settle it | Three sentences where one would do, in a session-start notice that competes for a user's first screen | **chosen.** The notice carries the short form and the skill carries the boundary in full; a hedge a reader can act on beats a claim they cannot check |
| Measure the hooks half in this segment | A `/reload-plugins` is typed by a person and a spawn is the orchestrator's; `agent-contract` §6 forbids the spawn and no agent can invoke a built-in CLI command | **not available.** Stated as unverified with the orchestrator named |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The notice and its module docstring — the case written and seen red against the old text first | `bin/test tests/test_version_check.py -q`, plus the recorded red run and a mutation of the new sentence | |
| 2 | `skills/update/SKILL.md` — steps, the scope statement, the output template | read; `bin/test tests/test_first_setup_asks_once.py -q` for the path claim it also carries | |
| 3 | Both READMEs, English and Korean, in one commit | `bin/test tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py tests/test_chain_hooks_hardening.py -q` | |
| 4 | Records — changelog fragment, ledger fragment, overview, the `docs/flow.md` tick | `bin/test tests/test_the_set_a_work_item_always_has.py tests/test_no_real_identifiers.py tests/test_release_hygiene.py -q` | |

Phase 1 is the vertical slice: the sentence a user reads, the case that pins
it, and the docstring that makes the same claim. Phases 2 and 3 widen the same
sentence outward through the corpus, and the grep is re-run over the rest after
each — this repository has seven measured instances of a rule re-broken one
text over, inside the fix for the first one.

## Operational impact

None. No migration, no environment variable, no dependency, no compatibility
break. The notice grows by about two lines of text and prints on the same
schedule under the same three limits.
