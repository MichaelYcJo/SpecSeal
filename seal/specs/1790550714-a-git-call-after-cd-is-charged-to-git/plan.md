# Implementation Plan: a `git` call after `cd` is charged to `git` (#377)

<!-- seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

`family` stops reading `git` by position and reads it by command word. It
reads the command the shell ran, newlines included, with each heredoc body
removed up to its closing line rather than everything after the operator.
Every sentence that states the old rule, or states that nothing but the span
changed after publication, is corrected in the commit that makes it false.
One file of code, `skills/verify/scripts/session_cost.py`, plus its cases, one
`SKILL.md` paragraph, the changelog fragment and the ledger.

## Technical context

- `skills/verify/scripts/session_cost.py#FAMILIES`: four `(name, pattern)`
  pairs in priority order. `git` is last and the only one anchored
  (`^\s*(git|gh)\b`).
- `#HEREDOC` and `#family`: `family` cuts at the first heredoc operator and
  runs the four patterns over what is left.
- `#load` builds `command` as `" ".join(text.split())`, so every newline is
  gone before `family` sees the text. This is why members 3 and 4 need the
  unflattened text, and why phase 2 touches `load`.
- `#analyse` calls `family` twice: the `by_family` table (Bash calls only)
  and the repeats filter (every call not in `delegated`). Both sites move to
  the unflattened text. The repeats filter's non-Bash calls keep today's
  JSON-dump reading (spec *Out*).
- `#report_segments` prints the comparability line and `#report` prints the
  `other` note. The first changes and the second does not.
- `hooks/cmdline.py` has a quote-aware segmenter, and it is not reused:
  `session_cost.py#newest` records that the two trees do not import each
  other, `payload_meter.py#_session_cost` loads `session_cost.py` alone by
  path, and the gate's segmenter reads a heredoc body as shell on purpose,
  which is the opposite of what a family needs.
- The measurement script the spec's numbers came from was a throwaway probe
  (contract §7) and is deleted. Its method is in phase 3's row so the builder
  can repeat it at the tip.

**Failure scenario, six months out.** A new shell shape puts `git` in
command position through a construct the tokeniser does not treat as a
separator. The likeliest are a wrapper (`timeout 60 git fetch`), a `case`
arm, or a `$( … )` somebody decides should count. It reads as `other`, as it
does today, with no crash. The `family` docstring names each bound, so the
reader who meets it knows it is a bound and not an oversight. The mirror
failure, a false `git`, needs `git` as a command word outside any quote, and
that is a git run.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #377 candidate 3: keep the anchor and add the ticket's separator alternation in front of `(git\|gh)\b` | reads inside quotes (`grep -E "a\|git"`, `echo 'a; git b'` become `git`) and misses `do gh`, `then git` and `{ gh`. It disagreed with the command-word rule on 144 of 22,974 flattened calls, all of those two shapes | rejected |
| #377 candidate 2: anchor every family | `cd /x && pytest -q` becomes `other`, #200 undone | rejected, as the ticket does |
| Unanchor to `\b(git\|gh)\b` | `grep -rn git`, `cat .git/config` and a `--message "git"` become `git`: #200's *wrong in both directions* from the other side | rejected. S4 is its mutant |
| Import `hooks/cmdline.py`'s `split_segments` | a skill script depends on the hooks tree, which `#newest` records the two trees do not do. A lone copy loses its classifier, and the gate's segmenter reads heredoc bodies as shell | rejected |
| The command-word rule for all four families | `uv run --with pytest pytest`, `uvx ruff check .` and `python -m pytest` stop being `test` or `lint/type`, which are 0.9.4 S1's shapes | rejected. The three stay unanchored |
| Charge a two-family call to a set, or split its seconds | the table's calls stop summing to the call count, and the shape of every reading changes. `FAMILIES`' comment states first-match as the design | rejected. First match stays |
| Member 1 alone, on the flattened text (phase 1 without phase 2) | leaves 310 newline calls and 694 post-heredoc calls, 12,544 s of `git`, in `other`. That is the next round's finding, the way 0.15.4 and 0.15.5 each paid a reopening | rejected |
| Remove heredoc bodies for `git` only, and keep the cut-to-end for the other three | `family` reads two different texts under one docstring that already says *with any heredoc body removed* | rejected |
| Count `$(git …)` and backtick substitutions | `shlex` cannot see into a quoted substitution, so only the unquoted ones would count and the family would depend on quoting. 40 calls, 390 s | rejected. The docstring states it as a bound |
| Fall back to `other` (not today's anchor) when `shlex` raises | `git log 'x` becomes `other`, which is worse than today on 0.9% of calls | rejected. The fallback is today's pattern |
| Reword the `other` note | the sentence stays true. Rewording it spends a pinned needle and a ledger drift and buys nothing | rejected |

## Phases

Each phase runs the module it edits (`bin/test tests/test_session_cost.py`)
and the modules that read what it edited. Each new case is seen red first
(contract §15), against 2037cf0's `family` or by reverting the phase's edit,
and the phase record says which. No phase runs the full suite, lint or
typecheck (contract §2). The sealer owns that.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **`git` by command word, on the text `family` already reads.** A helper tokenises with `shlex` (POSIX, `punctuation_chars`, newline as punctuation so phase 2 needs no second tokeniser) and yields each command word by the spec's In §1 rule. `family` answers `git` when any command word's basename is `git` or `gh`, and falls back to today's anchored pattern on `ValueError`. `FAMILIES` order is unchanged. Statements in the same commit: `#FAMILIES` comment, `#family` docstring (the rule and its three bounds), `#analyse` docstring (*the one exception* becomes two, with #377 and 0.15.6), the `#report_segments` comparability line and its comment (0.15.6), the `skills/verify/SKILL.md` paragraph beside #300's, and the changelog fragment's entry | S1–S6 as cases. S4 killed by the `\b(git\|gh)\b` mutant, S6 by the no-fallback mutant, S10 by deleting the new sentence. The existing family, heredoc, `other`-note and comparability cases pass unchanged. The narrow modules: `tests/test_session_cost.py`, plus every module that reads `skills/verify/SKILL.md` (`grep -l` at the tip) | 0fca8c5 |
| 2 | **The text the shell ran.** `load` keeps the unflattened command beside `command`. `analyse` classifies from it at both `family` sites. `family` removes each heredoc body to its closing line (`<<-` strips leading tabs; the operator's own line is kept; no closing line means cut to the end as today) and reads what follows with every family. Statements in the same commit: `#HEREDOC` comment, `#family` docstring (body, not rest), `#load` docstring if the key needs a sentence, the heredoc case's docstring, and the `SKILL.md` paragraph and changelog entry extended with members 3 and 4 and the `test` movement | S7 (transcript, through `--json`) and S8 as cases, red at 2037cf0. S9 and S11 pass unchanged. A mutant that classifies from `command` instead of the new key turns S7 red | ca8f4e0 |
| 3 | **The ledger and the numbers.** `evidence-check` at the tip names the drifted rows. Each is re-read against the edit and re-stamped in its own file with a dated note. 0.9.4 S2's *stops at the heredoc operator* gets `Corrected <date>` in place. New rows for the rule, the fallback and the heredoc body go in `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md`. The corpus measurement is re-run at the tip with a `test_tmp_*` probe, deleted after: every `*.jsonl` under `~/.claude/projects/*SpecSeal*/`, each Bash call's raw command through `session_cost.family` at 2037cf0 against the tip, a transitions table in calls and seconds. Any number in `SKILL.md` or `changelog.md` that differs from the frame's is the tip's number | S12: `evidence-check`'s exit code read directly (contract §1), no un-re-read DRIFTED row of this work's. The probe's table is in `phases/phase-3.md` | |

## Operational impact

- No new dependency (`shlex` is standard library), no environment variable
  and no migration.
- **Compatibility:** the family split, the two repeats figures, the
  `other`-leads note and the command it names are computed by a new rule.
  A reading taken before 0.15.6 is not comparable with one taken after in
  those rows. `--segments` says so on the page, and `SKILL.md` and the
  changelog say so where a person comparing readings meets it. Every other
  number and every printed shape is unchanged.
- **Squash order:** milestone 48 squashes A, B, C. This branch edits no file
  A or B edits. The ledger files it may re-stamp (`seal/ledger.md`,
  `seal/releases/0.8.2.md`, `0.8.3.md`, `0.9.4.md`, `0.9.5.md`, `0.11.3.md`)
  are the likely conflict surface with B's ledger work. Resolve hunk by hunk,
  never `--ours` or `--theirs`, then run `evidence-check`.
