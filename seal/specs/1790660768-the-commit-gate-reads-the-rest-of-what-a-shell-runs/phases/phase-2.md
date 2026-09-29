# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 2

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 7d488ee6 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 2: compound headers and P4 inside a string
(`spec.md` P7–P9, P4). The phase reads a `case` arm by position: its first
and later arms, `(P)` and `P )`. It reads a function definition in six
spellings and `coproc` with and without a NAME. That reading serves `watch`
and the string's command word, and the stand-in is used only where a header
cannot be placed. Inside a string, a later word that expands counts behind a
runner's options. S8's P7–P9 rewrites of the round-1 controls stay silent, and
each is seen red by a mutant that uses the stand-in for a placeable header.
Q3's header spellings are recorded as read by position or by the fallback.
The spawn's invariant and rules are phase 1's record's.

## What this phase found

**One reader of headers, two consumers.** `header_end` returns where the
command behind a header starts. It returns None when the segment opens with
no header, and `UNPLACEABLE` for a header it does not place. `_is_the_program`
asks it last, after its two phase-1 readings found no program, and reads again
from the first word after the header. `_segment_names_an_unknown_command` asks
it after its two readings and P4, then asks the words after the header again.
Both fall back to the stand-in on `UNPLACEABLE` alone. `command_word` does not
use it, so `git` and `eval` keep the base's stand-in, as `spec.md` §*Two
stand-ins* says they should.

**Q3, the header half.** `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py#HEADERS`
is the answer, one row per spelling, and each row pins the word `header_end`
places the command at. Read by position:

- **A case arm:** `case W in P)`, `(P)`, `P )`, a pattern that runs on past a
  `|` into the next segment, `in` on its own line, a later arm `P)` and
  `P )`, a `case` behind a list opener, and a `case` glued to `(`.
- **A function definition:** `f() {`, `f() (`, `f() (cmd` glued, `f()` with
  its body on a later line, `f ()`, `f(){`, `function f {`, `function f() {`,
  `function f () {`, `function f(){`, and `function f` with its body on a
  later line.
- **A coprocess:** `coproc CMD`, `coproc {`, `coproc (cmd` glued and
  `coproc NAME {`.

Left to the stand-in: a `case` with no `in`, a pattern with no `)`, and a
definition followed by something other than a body. bash refuses all three,
so the fallback is reached by spellings nobody listed, and never by a valid
one this table holds.

**The mutants found the planted rows weaker than the code.** Ten header
mutants survived the first run. Each one masked the same way. Where a
spelling misses its own branch, a neighbouring branch or the stand-in still
gives `watch "$CMD"` a stop, so a row that stops cannot tell the two apart.
What can tell them apart is a command that commits nothing, where the stand-in
is a new stop:

- The header table above.
- Three more control positions: a spaced pattern, a glued subshell body, and
  `case $1 in a|b)` inside a string.
- The shape `(case a in a) watch -g "$CMD";; esac)`.

With those in place nine were killed. The tenth,
`function f()` read by its own branch, was a branch the next line already
answered (`body(j + 1)` either way), so it was removed rather than pinned.

**P4 costs what the frame said.** `sh -c 'timeout 5 wc -l "$1"' _ f` now
stops (`spec.md` (b)). It is pinned as the frame's choice by
`test_a_string_behind_a_runners_operand_stops_as_the_frame_chose`, so a later
narrowing has to remove the pin on purpose. The rule reaches any word that
expands, a glob included. So `bash -c 'find . -name "*.pyc" -delete'` stops
as well: `find` is a runner, and the quoted `*.pyc` arrives from the splitter
unquoted. Phase 6's count over the recorded commands says how often that
happens.

**Seen red.** 25 cases failed at `b1ad717a` against phase 1's reader, which
reads no header, and so against `86256492`'s. The rows added after the mutant
run were seen red by the mutants the table below names. The header table
fails at `86256492`, where `header_end` does not exist.

**Mutants.** Each ran alone under `PYTHONDONTWRITEBYTECODE=1` and was restored
from saved bytes, with `tests/__pycache__` cleared between them. The tree was
clean after each run.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | `_is_the_program` uses the stand-in for every header | the P7–P9 controls in a declared repository (S8's mutant) |
| 2 | the word reader uses the stand-in for every header | the same (S8's mutant) |
| 3 | `_is_the_program` asks no header | `watch` in a case arm |
| 4 | `UNPLACEABLE` is no program | the unplaceable-header pin |
| 5 | the word reader asks no header | `sh -c` a case arm |
| 6 | `UNPLACEABLE` counts no word | the unplaceable-header pin |
| 7 | no P4 | the frame's-choice pin |
| 8 | `_behind_a_runner` reads no runner | the same |
| 9 | `_behind_a_runner` always behind one | the controls |
| 10 | list openers not skipped before a header | a case arm behind `then` |
| 11 | no glued `(` on the head | `HEADERS[a case glued to (]` |
| 12 | a body's `{` or `(` not stepped | the controls |
| 13 | a glued body `(cmd` not placed | `HEADERS[f() (glued]` |
| 14 | a pattern's glued `)` not placed | `sh -c` a case arm |
| 15 | a pattern's spaced `)` not placed | `HEADERS[case W in P )]` |
| 16 | a pattern past a `\|` is unplaceable | `HEADERS[case W in P, the rest past a \|]` |
| 17 | a `case` with no `in` is placed | `HEADERS[a case with no in]` |
| 18 | a `case` pattern read leniently | `HEADERS[a pattern with no )]` |
| 19 | no `coproc` | `coproc watch` |
| 20 | `coproc {` not stepped | `HEADERS[coproc {]` |
| 21 | `coproc NAME {` not read | `coproc NAME { watch }` |
| 22 | no `function` | `function f watch` |
| 23 | `function f ()` not read | `HEADERS[function f () {]` |
| 24 | `f(){` not read | `a glued definition` |
| 25 | `f()` not read | `HEADERS[a definition with no body]` |
| 26 | `f ()` not read | `a spaced definition` |
| 27 | no later arm | a later case arm |

**Verification.** Executed at `7d488ee6`: the 26 modules that load the
reader, either gate, the consent writer or the notice, 1365 passed and 1
skipped, exit 0. The frame's 42 shapes through `main()` at `86256492` and at
`9672662f`: 19 moved from silent to deny, none moved from deny to silent, and
the controls were unchanged. S7 passed.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* 25 cases at `b1ad717a`, and every changed branch has a
  mutant a case kills, S8's placeable-header mutant among them.
- *Failure direction.* Both readers ask the header only after their earlier
  readings found nothing, so every answer from before is kept, and a missed
  spelling falls to the stand-in, which is a stop.
- *Prompt budget.* `watch` or a string's command word in a case arm, a
  function body or a coprocess now meets the gate. On commands that commit
  nothing, two new stops: a header nobody listed with an expanding word after
  it (`spec.md` (a)), and a runner's operand in a string with an expanding
  word after it (`spec.md` (b)), a glob included. Phase 6 counts both.
- *Platform honesty.* String reading only. The header spellings are bash's
  and POSIX sh's, and none was run through a shell in this phase.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
