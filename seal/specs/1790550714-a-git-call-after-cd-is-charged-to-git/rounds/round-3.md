# 1790550714-a-git-call-after-cd-is-charged-to-git — review round 3

| Field | Value |
|---|---|
| Target SHA | af1e263e1cb62e44cd9676f27e2afbe6595c2e4d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 635 |
| Broad gate | aff94d4 against 7a39f2f |
| Fixes checked by | no fixes to check |
| Fix range | `9b595a263da50482567c4a00a2f179b12e83f925..9b595a263da50482567c4a00a2f179b12e83f925`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — findings 1 and 2: an unquoted heredoc's body line ending in `\` closes the body where bash does not, and two docstrings say the bounds are never worse than the rule before #377 when four shapes are |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round after the run's one reopening, at the diff of round 2's fixes (f12b995..807e2cc), and so the run's last round. It was asked whether round 2's six fixed and two answered verdicts are closed as a class. It was also asked to break the changed behaviours of `without_comments` and `command_words`: quoted and escaped operators, multi-character operators and redirections, and `\⏎` in heredocs and quotes. Finally it was asked to compare against 2037cf0 and ee72397 over the corpus.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | an unquoted heredoc's body line ending in `\` closes the body at the next delimiter line, where bash joins the two, so `cat <<EOF⏎body \⏎EOF⏎git push` reads `git`; round 2's "`\⏎` as the shell reads it" is not true of the heredoc pass | `skills/verify/scripts/session_cost.py:237` | deferred #642 | #642 — The run is capped at its one reopening, so this record commissions no fix. #642 owns how `session_cost.py` decides a command word and reuses this segmentation; the comment carries the round's paste-ready fix and the corpus figure (0 calls); executed: two shapes read `git` at the target and ee72397, `other` at 2037cf0, not `git` in bash; the paste-ready fix reads them `other`, passes 116 cases, and moves 0 of 22,872 corpus calls |
| 🟡 2 | "neither worse than the rule before #377" (`without_comments`) and "an unmatched quote never answers worse than the old rule did" (`runs_git`) are false: each bound also reads a `git` bash does not run | `skills/verify/scripts/session_cost.py:284` | deferred #642 | #642 — Same grounds; the replacement sentences are in the comment on #642; executed: four shapes read `git` at the target and ee72397, `other` at 2037cf0, not `git` in bash; round 2's answers to its findings 6 and 7 probed only the direction that loses a `git` |
| ⬜ 3 | `overview.md` §Not done says each bound "answers as the rule before #377 did" | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/overview.md:39` | deferred #642 | #642 — The same claim as 2, in `overview.md`; corrected with 2's docstrings so the copies stay in step; read against finding 2's executed shapes; a correction, not counted in `Needs a fix` |
| ⬜ 4 | ledger N2 says a refused line "never answers worse than the anchored rule"; `echo $(ls)#'⏎git push'` is refused and answers `git` | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md:13` | deferred #642 | #642 — The same claim as 2, in ledger N2; corrected with 2's docstrings so the copies stay in step; executed: the shape reads `git` at the target, `other` at 2037cf0; a correction, not counted in `Needs a fix` |
| 🟢 | round 2's finding 1 is closed as a class — a quoted or escaped operator character is a letter | `skills/verify/scripts/session_cost.py:307` | confirmed | executed: ten separator shapes through three copies read as bash does; read: the walk's quote parity equals the tokeniser's, so no separator the tokeniser saw is hidden; `$'\''` falls under `runs_git`'s refusal bound and reads as at ee72397 |
| 🟢 | round 2's finding 2 is closed as a class — an operator token is walked a character at a time | `skills/verify/scripts/session_cost.py:370` | confirmed | executed: every multi-character operator and process-substitution shape the prompt named reads as bash does; `x=$(ls)\|\|(git x)` moves `other` → `git` against ee72397 |
| 🟢 | round 2's finding 3 is closed where `without_comments` reads the command | `skills/verify/scripts/session_cost.py:294` | confirmed | executed: `ls \⏎# x; git push` reads `other` and `cd /x && \⏎git status` reads `git`; the heredoc pass is finding 1 |
| 🟢 | round 2's finding 4 is closed — the here-string sentence states the cut | `skills/verify/scripts/session_cost.py:198` | confirmed | executed: `cat <<< "$x"⏎git push` reads `other`; `cat <<< $x⏎git push` reads `git`, outside the sentence's shape |
| 🟢 | round 2's finding 5 is closed — each of `COMMENT_AFTER`'s eight characters is pinned | `tests/test_session_cost.py:1754` | confirmed | executed: eight mutants, one character removed each, each 1 failed; restored |
| 🟢 | round 2's findings 6 and 7 answer as their bounds state for the shapes named | `skills/verify/scripts/session_cost.py:284` | confirmed | executed: three shapes read `other` at all three copies; the sentence around them is finding 2 |
| 🟢 | round 2's finding 8 is closed — the 107-character line is re-wrapped | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md:12` | confirmed | read: lines 8 and 26 are 79 and 78, against the record's "at most 77" |
| 🟢 | the corpus moves as round 2 recorded, and no call goes from `git` to anything else against 2037cf0 | `skills/verify/scripts/session_cost.py:430` | confirmed | executed: ee72397 → target moves 1 call, `other` → `git`, the `git -C` after `&& \⏎`; refused 16 and 16 |
| 🟢 | the ledger has no drifted or broken row | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | confirmed | executed: `bin/evidence-check --strict`, unscoped, at the target, exit 0 |

## Paste-ready fixes

```python
        tabs = operator.startswith("<<-")
        # An unquoted delimiter's body has `\⏎` removed before a line is
        # compared with it, so a body line ending in `\` joins the next one
        # and that line closes nothing. A quoted delimiter keeps the `\`.
        joins = operator[-1] not in "'\""
        body = command.find("\n", opener.end())
        closed = None
        if body != -1:
            at, carried = body + 1, ""
            while at <= len(command):
                end = command.find("\n", at)
                end = len(command) if end == -1 else end
                line = carried + command[at:end]
                trailing = len(line) - len(line.rstrip("\\"))
                if joins and trailing % 2 and end < len(command):
                    carried, at = line[:-1], end + 1
                    continue
                carried = ""
                if (line.lstrip("\t") if tabs else line) == delimiter:
                    closed = end
                    break
                at = end + 1
```
```python
#
# A `\⏎` on the operator's own line is not joined here, so the body starts
# one line early and takes the continued line with it:
# `cat <<EOF \⏎&& git push⏎…⏎EOF` is `other`, as it was before #377.
```
```python
    Two bounds. A `)` inside a word starts a word boundary even when it
    closes a substitution (`echo $(ls)#x` reads `#x` as a comment), and
    quotes nested inside `"$( … )"` are read as closing the outer ones.
    Where they lose a `git`, the rule before #377 lost it too. They can also
    read one bash does not run, which that rule did not:
    `x="$(echo "; git log")"` reads its `git`, and so does
    `echo $(ls)#'⏎git push'`, whose `#'` removes the quote hiding it."""
```
```python
      first word, `git'x` from the pattern, and a quote the shell leaves
      unmatched never answers worse than the old rule did, and never ends a
      reading. A quote the walk sees unmatched only because a bound in
      `without_comments` removed its opener can: `echo $(ls)#'⏎git push'`
      is `git`."""
```
```text
overview.md §Not done — replace "because each answers as the rule before
#377 did and fixing it needs a parser this file does not have" with:
because where each loses a `git` the rule before #377 lost it too, and
fixing it needs a parser this file does not have. Each can also read a
`git` bash does not run, which `without_comments`' docstring shows
```
```text
N2's clause — replace "never answers worse than the anchored rule" with:
never answers worse than the anchored rule for a quote the shell itself
leaves unmatched
and add a `Corrected 2026-09-28` note naming `echo $(ls)#'⏎git push'`.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q -p no:xdist` at the target | 116 passed, exit 0 |
| 42 command shapes through 2037cf0's (flattened), ee72397's and the target's `family`, each against bash's reading | separators, operators, process substitutions and `\⏎` in quotes read as bash does; 6 shapes answer worse than 2037cf0 (findings 1 and 2); 5 more are wrong as at 2037cf0 (the stated bounds, `$'\''`, the operator-line continuation) |
| the contested shapes through `bash -c` | an unquoted body's `body \⏎EOF` joins and does not close; `cat <<EOF \⏎&& echo RAN` runs `RAN`; `"a\⏎b"` is `ab`; `x="$(echo "; echo FP")"` is a string; the `#'⏎…'` and heredoc-in-comment shapes run nothing |
| `COMMENT_AFTER` with each of its eight characters removed, `-k comment_runs_nothing`, one at a time | each 1 failed; the file restored and the clone clean |
| every Bash call under `~/.claude/projects/*SpecSeal*/`, through all three copies | 351 transcripts, 23,779 calls; ee72397 → target: 1 call, `other` → `git`; 2037cf0 → target: no call leaves `git` except 10 to `test` (the order `FAMILIES` states); refused 16 at ee72397 and at the target |
| finding 1's fix on a copy of the target: the shapes, the corpus and the module | the two worse shapes read `other`; 0 of 22,872 calls in 334 transcripts (this session's excluded) move against the target; the fix copied into the clone, `bin/test tests/test_session_cost.py -q -p no:xdist` 116 passed, then restored with `git checkout` |
| the four planted cases at the target and on the patched copy | the first reads `git` at the target and `other` patched; the other three read the same on both |
| `bin/evidence-check --strict`, unscoped, at the target | exit 0 |
| the orchestrator's four modules giving 205 passed, and ruff clean, at the target | not re-run here beyond `tests/test_session_cost.py`: unverified by this round, and the orchestrator answers it |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet. Nobody has run it. It is the sealer's, and it comes due when the orchestrator settles findings 1 and 2 under the cap |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:270` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:265` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:193` | round 1's ⬜ 3 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:184` | round 1's ⬜ 4 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:282` | round 1's ⬜ 5 — answered |
| round-1 | `tests/test_session_cost.py:1572` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/session_cost.py:722` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.4.md:32` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | round 1's 🟢 — confirmed |
| round-1 | `questions.md` Q1 | round 1's ❓ — out of verified scope |
| round-2 | `skills/verify/scripts/session_cost.py:331` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:273` | round 2's 🟡 3 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:199` | round 2's 🟡 4 — fixed |
| round-2 | `tests/test_session_cost.py:1735` | round 2's ⬜ 5 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:258` | round 2's ⬜ 6 — answered |
| round-2 | `skills/verify/scripts/session_cost.py:402` | round 2's ⬜ 7 — answered |
| round-2 | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md:12` | round 2's ⬜ 8 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py:202` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:194` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:361` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:326` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/session_cost.py:313` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md:12` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
