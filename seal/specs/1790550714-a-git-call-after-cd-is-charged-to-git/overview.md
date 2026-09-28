# 1790550714-a-git-call-after-cd-is-charged-to-git — overview

📋 implement applied
· spec:     this work item's spec.md (Grounding, the class table, In §1–6, the statements table, Decided from the tree, Out, S1–S12, Data & interfaces), plan.md (phases 1–3, Technical context, Alternatives), questions.md Q1–Q3; docs/measuring-a-run.md §*A reading that was published is still wrong after it is published*; skills/verify/SKILL.md §*Measure the segment, and feed the flow log* (#300's paragraph); seal/releases/0.9.4.md S1, S2 and S4; CLAUDE.md §fragments and §commit early; agent-contract §1–§3, §7, §9, §12, §14, §15
· evidence: seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md N1–N6 added; 0.9.4 S2 corrected in place; re-read and re-stamped where they live: seal/ledger.md (two rows), seal/releases/0.8.0.md F5, 0.8.2.md R2, R3 and G5, 0.8.3.md R1, 0.9.4.md S4, 0.9.5.md (eight rows), 0.11.3.md (three rows), 0.13.1.md O6
· verified: executed — every new case seen red (against 2037cf0 or the phase before), 25 mutants across two phases each killed, the session_cost module and every module reading a file each phase edited, run at each phase boundary, evidence-check lenient and strict, correction-check over the range, the corpus measurement at the tip; read — Q2's call sites; unverified — Q1 (the 0.15.5 transcripts), the full suite, lint and typecheck (the sealer's)

## Why this work exists

A `git` or `gh` call anywhere but the start of a Bash command read as `other`
in every `session-cost` reading, and it now reads as `git`. So does one after
a heredoc's closing line or on a line of its own, and a test run after a
heredoc now reads as `test`.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The version the comparability line names | `spec.md` S10: "`--segments` prints a comparability line naming 0.15.6 and #377". `tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one` failed on it, and on the same version in `session_cost.py`'s docstring and `SKILL.md` | the line names #377 and says `CHANGELOG.md` names its release | the check's docstring: "**at or above the running version is a timer and is refused; below it is history and is kept.**" The running version is 0.15.5, so neither 0.15.5 nor 0.15.6 can be written in a loaded file before the release |
| What the tokeniser fallback decides | `spec.md` In §2: "That call is judged by today's anchored pattern". The walk is lazy, so words read before the refusal answer first | lazy walk, with the pattern for a line refused before its first word | an eager walk sends `cd /x && git log 'x` to the pattern, which answers `other`, and the spec's own grounds are that the new rule "never produces an answer worse than the old one" |
| Which ledger rows drift | `questions.md` Q3's expected set: "`#analyse` ×7, `#load` ×4 if edited, `#FAMILIES`, `#family` and `#HEREDOC` through 0.9.4 S1 and S2". `evidence-check` found `#FAMILIES` and `#HEREDOC` clean, and the `SKILL.md` section anchor drifted in ten rows | all 21 named rows re-read | a row an edit drifts is re-read where it lives (`CLAUDE.md` §*Appended is the word*); the check names the rows, and the frame's set was a read |
| A backtick substitution | `spec.md` §*Decided from the tree*: "**A command substitution is not a command position.**" After round 1's fix it holds for `$( … )`, `<( … )` and `>( … )` whatever they contain, and for a backtick substitution only up to its first word: a separator inside backticks is read as the line's | `$(`-family nesting tracked; backticks narrowed in `command_words`' and `runs_git`'s docstrings, the changelog and ledger N1 | round 1's report: tracking backticks "turned 11 real `git` runs to `other` (every one of them a `grep -c '```'`)", because the tokeniser strips the quotes that would tell a backtick token from a quoted one |

## Not verified

| Item | Who must answer |
|---|---|
| How the 0.15.5 run's own segment readings (#619) move under the new rule (`questions.md` Q1) | the owner, on the machine that holds the 0.15.5 transcripts: `session_cost.py --segments <transcript>` at 2037cf0 and at this branch's tip |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |

## Not done

Nothing beyond the spec's own *Out* table. The word-start comment rule
phase 2 left out (`phases/phase-2.md`) was taken in round 1's fix pass,
because round 1 found the ordinary-`#` reading answers worse than 2037cf0 on
a comment holding a separator. The `HEREDOC` pattern was not widened to a
here-string or an escaped or lowercase delimiter. Its comment states both,
and round 1 found neither moving a call. Three shapes round 2 found are
stated as bounds rather than fixed, because where each loses a `git` the
rule before #377 lost it too, and fixing it needs a parser this file does
not have: a `)` inside a word read as a word start (`echo $(ls)#x`), quotes
nested inside `"$( … )"`, and a heredoc operator inside a comment. Each can
also read a `git` bash does not run, which `without_comments`' docstring
shows. The first two are in `without_comments`' docstring and the third in
the `HEREDOC` comment.

Corrected 2026-09-28 by #642's phase 1: the sentence said each bound
*answers as the rule before #377 did*, which holds only for a `git` it
loses. #635's round 3 found `x="$(echo "; git log")"` and
`echo $(ls)#'⏎git push'` reading a `git` bash does not run.

## Fed back into the spec

Inferred during implementation, so a planner may overturn them:

- The fallback decides only a line refused before its first word is
  finished. Words read before a refusal count (ledger N2).
- A call with no command string holds the flattened dump in `ran` as well as
  in `command`, so the repeats filter's reading of non-Bash calls is exactly
  what it was (ledger N4).
- Two heredoc operators on one line have their bodies one after the other
  (ledger N3).
- A comment is removed by bash's rule before the command words are read,
  and no word anywhere inside `$( … )`, `<( … )` or `>( … )` is a command
  word (ledger N1 and N4, round 1's fix pass).
