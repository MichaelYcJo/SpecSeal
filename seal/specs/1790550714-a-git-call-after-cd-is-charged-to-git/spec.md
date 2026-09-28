# Feature Specification: a `git` call after `cd` is charged to `git` (#377)

<!-- seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/measuring-a-run.md` §*What a measurement must survive, and what it must not invent*, the clause *A reading that was published is still wrong after it is published* | the correcting work item says which published numbers a correction moves. Its `Enforced by` is *nothing — a session's act*, so this work item carries it out: the family rows and the repeats lines of every reading published before 0.15.6 move, and span, command time, model time, tokens and the `slowest` list do not |
| `skills/verify/scripts/session_cost.py#analyse`, its own docstring: *Changing what the plain reading prints would make every reading this repository has already published incomparable with the next one, with nothing on the page saying so* | the plain reading's family split changes here, so the page says so. `span_s` is named there as *the one exception*, and that sentence becomes false. It is corrected in the same commit, and the `--segments` comparability line names 0.15.6 |
| `skills/verify/scripts/session_cost.py#newest`: *the two trees do not import each other, so this names it rather than sharing it* | `hooks/cmdline.py`'s segmenter is not imported. `session_cost.py` stays standard-library only and copyable alone. `payload_meter.py#_session_cost` loads it by path |
| `seal/releases/0.9.4.md` S1 and S2 (#200's repair) | the `test`, `lint/type` and `build` families keep matching anywhere on the line, on purpose (`uv run --with pytest pytest`, `uvx ruff`). The heredoc operator keeps its stated bound: a lowercase unquoted delimiter is not read as a heredoc |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | the fix covers the class, meaning every way a git call that ran reads as `other`, and not only the `cd … &&` instance. Every sentence a person reads that changes is pinned in the same commit, and every new case is seen red before it is planted |
| `CLAUDE.md` *a change writes fragments, never the shared file* | changelog in `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md`, new ledger rows in `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md`. A row an edit drifts is re-read in the file it lives in, and a row the edit makes false is corrected in place with a `Corrected <date>` note |

## Scope

### The class, and its members, measured

The finding names one instance: `family('cd /x && git status') == 'other'`,
because `FAMILIES`' `git` pattern is `^\s*(git|gh)\b`, the only family pattern
anchored at position 0 (`session_cost.py#FAMILIES`, read 2026-09-28 at
2037cf0). The class is wider: **a `git` or `gh` process the call ran, which
the table charges to `other`.** Measured 2026-09-28 (executed, a throwaway
probe, deleted) over every transcript on this machine under
`~/.claude/projects/*SpecSeal*/`: 349 transcripts, 22,974 Bash calls,
163,889 command-seconds. The class has four members.

| # | Member | Example | Today | Calls · seconds | This work |
|---|---|---|---|---|---|
| 1 | after `&&`, `\|\|`, `;`, `\|`, `&` or a subshell's `(` | `cd /x && gh issue view 1` · `W=/x; cd $W; git grep y` · `(cd /x && git status)` | `other` | 2,703 · 21,179 s | in |
| 2 | after a reserved word or an assignment | `for n in 1 2; do gh issue view $n; done` · `if git diff --quiet; then …` · `FOO=1 git status` | `other` | inside member 1's count | in |
| 3 | on a line of its own after a newline | `cd /x⏎git status` | `other`: `load` flattens whitespace, so the newline is gone before `family` runs | 310 · 1,047 s | in |
| 4 | after a heredoc's closing line | `cat > b.md <<'EOF'⏎…⏎EOF⏎gh issue create --body-file b.md` | `other`: the heredoc cut drops everything from the operator to the end, not only the body | 694 · 11,497 s | in |
| — | inside a command substitution | `cd $(git rev-parse --show-toplevel) && ls` · `echo "$(git log -1)"` | `other` | 40 · 390 s | **out** (Data & interfaces) |
| — | behind a wrapper command | `timeout 40 gh issue list …` | `other` | 1 · — | **out**, the stated bound |

The whole rule, all four members together, changes today's table on this
machine as follows. 3,634 calls and 31,422 s move from `other` to `git`.
816 calls and 10,631 s move from `other` to `test`, 90 calls and 295 s to
`lint/type`, and 9 calls and 42 s to `build`: these are runs after a heredoc's
closing line, member 4's mechanism applied to every family. 18,454 calls do
not move.

| Family | Today | After |
|---|---|---|
| `other` | 17,727 · 100,855 s | 13,178 · 58,464 s |
| `git` | 2,476 · 10,711 s | 6,101 · 42,055 s |
| `test` | 2,438 · 51,090 s | 3,264 · 61,809 s |
| `lint/type` | 327 · 1,215 s | 417 · 1,510 s |
| `build` | 45 · 110 s | 53 · 142 s |

**The 0.15.5 run's own transcripts are not on this machine**, so they could
not be read (searched 2026-09-28). The eight SpecSeal project directories under
`~/.claude/projects/` hold 349 transcripts, none dated 24–27 September. The
#619 readings name paths under another user's home directory, which is the
other machine's.
What could be read is what #619 printed: its thirteen segment comments list
104 `slowest` commands, flattened and cut at 88 characters. Run through the
candidate (executed), 8 of them move from `other` to `git`. Five are framer C's
`cd …; gh issue view …`, and three are framer B's `cd … && gh …` and
`cd … && git …`. The other 96 do not move. Every warden round's eight slowest
are `R=…; cd …; python3 - <<'EOF'` and similar, and stay `other`. So on
0.15.5's segments the fix moves the `git` row and does **not** stop `other`
leading. `questions.md` Q1 holds the measurement on the real transcripts.

### In

1. **`git` is a command word, not a position.** A call is `git` when `git` or
   `gh`, by basename (`/usr/bin/git` counts), is the command word of any
   command on the line. A command word is the first word of the line, or the
   first word after `&&`, `||`, `;`, `|`, `&`, a newline, or a `(` that opens
   a subshell. Leading `NAME=value` assignments and the reserved words `if`,
   `then`, `elif`, `else`, `do`, `while`, `until`, `!`, `{` and `time` are
   skipped. The line is split by `shlex` in POSIX mode, so a separator or a
   `git` inside a quoted string is not seen. That is the half #200 needed
   and the half the anchor was buying.
2. **When the tokeniser refuses, the answer is today's.** An unbalanced quote
   makes `shlex` raise (213 of 22,974 calls, 0.9%). That call is judged by
   today's anchored pattern, so the new rule never produces an answer worse
   than the old one. It is the same direction as the `HEREDOC` bound: the
   smaller error.
3. **Family reads the command the shell ran, newlines kept.** `load` keeps
   the command text as the harness recorded it, beside the flattened
   `command`. `analyse` classifies from that text at both of its `family`
   call sites, the `by_family` table and the repeats filter.
   `slowest`, `strip_pipe`, the repeats grouping and every printed command
   keep reading the flattened text, so nothing printed changes shape.
4. **A heredoc's body is removed, and what follows it is read.** The body runs
   from the line after the operator to the first line equal to the delimiter.
   Under `<<-` that line may carry leading tabs. The rest of the operator's
   own line is kept, because it runs (`cat > f <<'EOF' && git add f`). What
   follows the closing line is read by every family, since the family
   docstring already says *with any heredoc body removed*. A command with no
   closing line is cut from the operator to the end, which is today's
   behaviour. Every flattened input has no closing line, so every existing
   `family` case string classifies as it does today. What an operator is does
   not change: the `HEREDOC` pattern and its lowercase-delimiter bound stay.
5. **A command with two families is charged as today:** `FAMILIES` order,
   first match wins, and `git` is last. `cd x && git add . && pytest -q` is
   `test`. This is the rule the `FAMILIES` comment states, *so a compound
   `ruff … && pytest …` is charged to the test run that dominates it*, and
   `test_the_family_split_charges_a_compound_command_to_its_test` pins it. It
   does not change.
6. **The statements that change, each in the commit that makes it true.**
   The table below lists them.

### Every statement about the families, enumerated

Found by searching the whole tree for *famil*, `by_family`, `FAMILIES`,
`family(`, `` `other` ``, *names nothing*, *comparable*, *charged to*,
`0.9.4`, `#200`, `lint/type`, and by listing every ledger anchor on
`session_cost.py` (read 2026-09-28, at 2037cf0 plus the routing commit).

| Coordinate | What it says | Verdict |
|---|---|---|
| `skills/verify/scripts/session_cost.py#FAMILIES`: the comment above it and the `git` entry | the families, first-match order, #200's path-named runners | **edit**: states the command-word rule for `git` and why the other three still match anywhere |
| `skills/verify/scripts/session_cost.py#HEREDOC`: the comment | *cutting there*, *A heredoc body is data* | **edit**: body to its closing line; a command with no closing line is cut to the end as before |
| `skills/verify/scripts/session_cost.py#family`: the docstring | *The family of the command that RAN, with any heredoc body removed*; *Cutting at the heredoc operator* | **edit**: the first sentence becomes true; the second is rewritten; the `git` rule and its bounds are stated (substitution, wrappers, tokeniser refusal) |
| `skills/verify/scripts/session_cost.py#analyse`: the docstring's *`span_s` is the one exception* | only the span's rule changed after readings were published | **edit**: the family split and the repeats lines are the second, with #377, the version and the measurement |
| `skills/verify/scripts/session_cost.py#analyse`: the `unnamed` comment (*`other` is the family with no meaning of its own …*) | what `other` is | true after the change; no edit |
| `skills/verify/scripts/session_cost.py#report`: the comment and the printed note *`other` is the largest family and names nothing, so a runner these patterns do not know reads as no such run at all* | what `other` leading means | true after the change; **no wording change** (see *Decided from the tree*) |
| `skills/verify/scripts/session_cost.py#report_segments`: the comment and the line *Comparable with readings taken since 0.9.4 …* | from when a reading is comparable | **edit**: the family rows are comparable only with readings since 0.15.6, and the line says why |
| `skills/verify/scripts/session_cost.py#tool_name`: the docstring's *charged to `?` rather than to its family* | a malformed tool name | true; no edit |
| `skills/verify/scripts/session_cost.py#load`: the docstring | turns and pairing | **edit** only if the new field needs a sentence. The unit drifts either way |
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, step 1, beside the #300 span paragraph | says nothing about families today | **add** one paragraph, #300's shape: what moved, from which version, what a reader comparing across it must know |
| `tests/test_session_cost.py#test_a_runner_named_inside_a_heredoc_is_not_a_run_of_it`: the docstring's *Cutting at the heredoc operator* | the cut | **edit**: the docstring only. Its fixture strings are flat, so the assertions hold |
| `tests/test_session_cost.py#test_the_reading_names_the_release_it_is_comparable_from`: the docstring and its needle | 0.9.4 | **edit or extend**: it also asserts 0.15.6 |
| `tests/test_session_cost.py#test_a_runner_named_by_path_is_a_test_run`, `#test_the_family_split_charges_a_compound_command_to_its_test`, `#test_the_report_names_the_command_the_table_could_not` | the test family, compound order, the `other` note | true; no edit, and all three must pass unchanged |
| `docs/measuring-a-run.md` §*What a measurement must survive*, *a family classification* | #200's history | true; no edit |
| `README.md` rows `session-cost --latest` / `--segments`, and `README.ko.md` rows `session-cost --latest` / `--segments` | describe the reading without naming a family | no family statement; no edit |
| `CHANGELOG.md` 0.9.4 entry | released history | not edited |
| `seal/releases/0.9.4.md` S1 (`#FAMILIES`) | test-by-path; *a `git log` naming the word … stay out* | true; drifts, **re-read** |
| `seal/releases/0.9.4.md` S2 (`#family`, `#HEREDOC`, `#analyse`, `#report`) | ***The classifier stops at the heredoc operator*** | **false after member 4: `Corrected <date>` in place** |
| `seal/releases/0.9.4.md` S4, `0.8.2.md` R2, `0.8.3.md` R1, `seal/ledger.md` row *A turn is one assistant message …* (`#load`) | turns, stamps, input counts | drift if `load` is edited; **re-read** |
| `seal/ledger.md` row *Model time runs from a turn's last result …*, `0.11.3.md` *Nothing the mode adds changes what any existing reading prints*, `0.9.5.md` the four `#analyse` rows | model time, the mode, the span rule | drift with `analyse`; **re-read**. None is about the family split |
| `hooks/cmdline.py` `split_segments*` | the commit gate's segmenter | a different tree and the opposite need (the gate reads a heredoc body AS shell), so it is not a copy |
| `skills/verify/scripts/payload_meter.py` | uses `DELEGATING`, `spawn_labels`, `count`, `subagent_transcripts` from `session_cost.py`, never `family` or `FAMILIES` | the table is not shared; **not absorbed** |

`evidence-check` is the authority for which rows drift. The table above is
what the build should expect it to name, and a row it names that is missing
here is re-read the same way.

### Decided from the tree (the judgments the ticket left open)

- **Shape: #377's candidate 1, command position, for `git` alone.**
  Candidate 3, a separator alternation in the regex, reads inside quotes and
  misses `do gh …`. On the flattened text it disagreed with candidate 1 on
  144 of 22,974 calls, and every disagreement read was one of those two
  shapes. Candidate 2, anchoring every family, makes `cd /x && pytest -q`
  `other`, which the ticket itself calls worse. The other three families stay
  unanchored: `uv run --with pytest pytest` and `uvx ruff check .` are the
  shapes 0.9.4's S1 was written for, and their command words are `uv` and
  `uvx`.
- **Two families on one line: unchanged.** See In §5.
- **The `other` note: no wording change.** The sentence says what `other`
  leading means, and that stays true. It never said `git` was absent. Leading
  is still common after the change: `other` led the Bash-family seconds in
  257 of 349 transcripts before, and 198 after member 1 alone. On 0.15.5's
  warden rounds it still leads, because their slowest work is
  `python3 - <<'EOF'`. Its pinned needle
  (`test_the_report_names_the_command_the_table_could_not`) is untouched.
- **A command substitution is not a command position.** `shlex` cannot see
  into a double-quoted `"$(git …)"`. Counting only the unquoted ones would
  make the family depend on quoting, which a reader cannot see in the table.
  40 calls, 390 s.
- **Newlines and heredoc bodies are in (members 3 and 4), not left for a
  later issue.** Together they are 1,004 calls and 12,544 s of `git` alone,
  and #200's `wrong in both directions` is the precedent: the half left out is
  the next round's finding. Member 4 applies to every family, because a
  `family` that read one text for `git` and another for `test` would state
  two rules in one docstring.

### Out

| Item | Why it is out | Who answers it |
|---|---|---|
| A family for `python3 - <<'EOF'`, the largest remaining `other` bucket: 1,651 calls and 17,343 s here under member 1's rule alone, where `other` held 79,588 s (22%). Not re-measured under the whole rule | a heredoc'd script is a vehicle, not a kind of work. It carries edits (contract §9's territory), probes and measurements, so a row for it would read as one cause when it is a mixture. It is also a new row in every reading, which is a feature, while milestone 48 is a patch of instruments. The `unnamed` line already names the command when it is the slowest in `other`, which is today's answer to *what is in there* | the owner, when 0.16.0 is planned. The orchestrator may file it with these numbers |
| `broad-gate`, this plugin's own suite command, charged to `other` (30 calls, 13,356 s here) | a new member of the `test` family's name list. That is #200's class (a runner the patterns do not know), not #377's (a known runner in a position the pattern does not read) | same as above |
| The mirror of #377 in the other three families: a call whose command word is `git` charged to `test`, `lint/type` or `build` because one of their names is on the line. 115 calls here (`test` 88, `lint/type` 23, `build` 4), some genuine compounds (`git status; ./bin/test`) and some mentions (`gh pr checks 516 \| grep pytest`, a branch named `…-need-not-make` on `git push`) | those families match anywhere on purpose (0.9.4 S1). Changing that is a different rule with its own measurement, and this change does not move any of the 115 | same as above |
| A `git` behind a wrapper (`timeout`, `env`, `xargs`, `nohup`, `command`, `sudo`, `exec`, `watch`) | 1 call in the whole corpus. The docstring states it as a bound | nobody needs to; the docstring states it |
| Non-Bash calls reaching the repeats filter's `family(call["command"])` as a JSON dump (`analyse`, the repeats loop) | today's behaviour, unrelated to position, and outside the class | not deferred: noted so the build does not widen into it |
| Re-deriving the published readings | the policy clause asks the correcting work item to *say which published numbers are affected*, not to recompute them | this spec, `changelog.md` and the `SKILL.md` paragraph |
| `hooks/worktree-guard.py`, `hooks/worktree_consent.py`, `docs/worktree-guard-spec.md`, `skills/evidence-check/scripts/evidence_check.py`, `tests/test_the_fixes_close_the_record.py` | milestone 48's items A and B edit them | A's and B's chains |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the finding's instance | `family` is handed `cd /x && git status` and `cd /x && gh issue view 1` / → `git` for both, where 2037cf0 says `other` | a `family` case in `tests/test_session_cost.py`, red at 2037cf0 |
| S2 the #619 shapes | `cd /w; gh issue view 616 --json title`, `W=/w; cd $W; git grep -n x`, `cd /w && git -C /w grep x`, `git -C /w commit -q -F - <<'EOF'⏎docs: x⏎EOF` / → `git`. `W=/w; cd $W; for f in a b; do grep -c x $f; done` and `cd ~/p && python3 - <<'EOF'⏎import json⏎EOF` → `other` | the same case, both arms |
| S3 member 2 | `for n in 1 2; do gh issue view $n; done`, `if git diff --quiet; then echo y; fi`, `FOO=1 git status`, `(cd /x && git status)`, `cat x \| git apply`, `/usr/bin/git status` / → `git` | a case, red at 2037cf0 |
| S4 the negative direction | `grep -rn "git" .`, `ls /a/git/b`, `x --message "git"`, `cat .git/config`, `echo git`, `rg gh docs/`, `echo 'a; git b'`, `cd $(git rev-parse --show-toplevel) && ls`, `echo "$(git log -1)"`, `timeout 40 gh issue list` / → not `git` | a case. A mutant that unanchors to `\b(git\|gh)\b` must turn it red |
| S5 two families | `cd x && git add . && pytest -q` / → `test` | a case. The existing `ruff … && pytest` case passes unchanged |
| S6 the tokeniser refuses | `echo 'unbalanced git` / → `other`, and `git log 'x` / → `git`, which are today's answers | a case. A mutant that drops the fallback, so a `ValueError` escapes, turns it red |
| S7 member 3, through the transcript | a transcript whose Bash call is `cd /x⏎git status` / `--json` → `by_family` has `git` and no `other` | a transcript case. It pins the `load` → `analyse` wiring, which a `family` case alone cannot |
| S8 member 4 | `cat > b.md <<'EOF'⏎body⏎EOF⏎gh issue create --body-file b.md` → `git`. `python3 - <<'EOF'⏎x=1⏎EOF⏎bin/test -q` → `test`. `cat > f <<-'EOF'⏎⇥body⏎⇥EOF⏎git add f` → `git`. `cat > f <<'EOF'⏎git is here⏎EOF` → `other`, since the body is still data | a case, red at 2037cf0 |
| S9 today's heredoc cases are unchanged | every string in `test_a_runner_named_inside_a_heredoc_is_not_a_run_of_it` classifies as it does at 2037cf0, the lowercase-delimiter pair included | that case, unchanged |
| S10 what the reader is told | `--segments` prints a comparability line naming 0.15.6 and #377 for the family rows, beside the existing 0.9.4 line | the comparability case asserts both versions. Deleting the new sentence turns it red |
| S11 no printed command changes shape | `slowest`, the `unnamed` line and the repeats lines still print the flattened command | the existing `slowest` and `unnamed` cases, unchanged |
| S12 the ledger stays true | `evidence-check` names no DRIFTED row this work left un-re-read, and 0.9.4 S2 carries a `Corrected 2026-…` note | `evidence-check`, read at the phase that writes the ledger |

## Data & interfaces

- **`load`'s call dict gains one key**, holding the command text as the
  harness recorded it (the builder names it). It is present for every call.
  For a non-Bash call it holds the same JSON dump `command` holds. No
  printed field, `--json` field or `--post` body gains or loses a key.
- **`--json`'s `by_family`, `repeat_exact_s` and `repeat_same_work_s`, and
  `unnamed`, change value** for the same transcript. Their shape does not
  change. A caller comparing a pre-0.15.6 `--json` reading with a later one
  is comparing two rules.
- **`family(command)` keeps its signature.** A flattened string gives
  today's answer for every heredoc case (no closing line) and the new answer
  for separators. A string with newlines gets members 3 and 4.
- **Dependencies:** `shlex`, which is standard library. Nothing new is
  installed.
- **Published readings affected** (the policy clause's act): every
  `session-cost` reading taken before 0.15.6, whether posted to a
  `flow-measurement` or `flow-baseline` log, pasted into a seal's `cost` row
  or kept in a round record. In each, the `by family` rows, the two repeats
  figures, the `other`-leads note and the command it names are affected.
  `git` reads low and `other` reads high, and `test` reads low wherever a run
  followed a heredoc. Span, command, model, idle, tokens, tools per turn,
  `slowest` and every `--spawns` and `--segments` span are not affected.

## Open questions → questions.md

No row needs a person. Q1 is a measurement on the other machine, and Q2 and
Q3 are the work's.

Framed 2026-09-28 by framer, before the build.
