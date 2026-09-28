# 1790562541-reading-is-charged-to-a-read-family — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     this item's spec.md, plan.md, questions.md, routing.md; docs/measuring-a-run.md §*What a measurement must survive*; the #377 item's round-3 report §*Paste-ready fixes* and overview §*Not done*; seal/releases/0.15.6.md N1–N6, 0.9.4.md S1–S2
· evidence: seal/ledger/1790562541-reading-is-charged-to-a-read-family.md R1–R7 added; 26 rows re-read and re-stamped over nine ledger files, N1–N3 corrected in place
· verified: executed — the module and its readers at each phase, 35 mutants, bash's own heredoc join, the corpus probe, evidence-check (exit 0, and 0 under --strict); read — item A's hunks against the plan's units

## Why this work exists

A call that only read a file was charged to `other`, so `other` led most
readings and named a `sed -n`; `session-cost` now charges it to `read`, and
`other` falls from 57% of the Bash calls to 25% on this machine's corpus.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| the neutral set | spec In §1 lists `case` and `esac` as neutral | left out | spec In §3: *what the walk cannot see is not `read`*; `runs_git`'s third bound says a `case` arm's `)` does not put the next word in command position, so `case $x in a) rm f;; esac; ls` would read as reading |
| how a hidden shape is found | spec In §3 speaks of tokens on the line | a text match on the recorded command | `without_comments` turns a quoted operator into a letter, so `"$(ls)"` reaches the walk as `$_ls_`; the match errs toward `other`, and command words and arguments still come from the one walk |
| which text `read` is judged on | spec: `family` removes heredoc bodies, then judges | `read` alone is judged on the command as recorded | `without_heredoc_bodies` cuts a here-string's `<<<` away, and `grep x <<< "$y"` read as `read` on the stripped text |
| `sed --in-place` and `sort --output` | spec In §2 names the long options | any GNU prefix of three characters or more | contract §12: `sed --in s/a/b/ f` edits in place; `--` alone stays the end of options |
| round 3's paste-ready join | carried `end < len(command)` | dropped | an equivalent mutant: a join on the last line ends the walk as a failed comparison does |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, repository-wide lint and format — this build ran each phase's module, the modules that read what it edited, and ruff on the two edited Python files | the sealer, once, after the review rounds settle |
| bash's heredoc join was asked of the darwin system bash only | the reviewer, if a Linux bash reading matters; POSIX states the same join |
| bash 5.3's `${ cmd; }` running `cmd` was read from its manual, not run (no bash 5.3 on this machine); round 1's fix keeps `${` followed by a space or `\|` out of `read` on that reading | anyone with bash 5.3; the pattern errs toward `other` if the reading is wrong |

## Not done

The read-word list was not widened. `cut`, `tr` and `uniq` are the counted
candidates (`phases/phase-3.md`), and the frame left that to the owner with
the numbers in hand. Nothing was built for #640.

## Fed back into the spec

Inferred during implementation, so a planner may overturn them:

- `case` and `esac` are not neutral words (R1).
- `read` is judged on the command as recorded, heredoc bodies kept (R3).
- A long option is matched by any prefix GNU's parser accepts (R2).
