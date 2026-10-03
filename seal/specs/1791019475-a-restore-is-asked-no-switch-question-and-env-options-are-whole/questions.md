# 1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The run is unattended and nobody is left to
ask. The spawn prompt said that where a person would decide, the frame
chooses a stated default with its grounds. Each such row is ticked as decided
by the frame, not as answered. A reviewer who opens what the grounds cite can
overturn any of them.

**The owner's rule of 2026-10-03 is an input, not a question.** A guard
change that could add a question is counted over #733's D1 corpus. Zero added
stops builds it. One or more names it as a limit with its count.

**Judgments the tickets left open that the tree answered.** They are listed
so nobody reopens them, and each is a row below with its grounds:

- whether `--quoting-style` joins the table before any release has it (Q1);
- whether #738 rides along (Q2);
- whether the generated comparisons are planted or stay probes (Q3);
- how `env`'s two grammars combine (D1), and where BSD's `-` lives (D2);
- whether `genv` gets BSD's reading (D3);
- whether the commit gate's corpus delta is the owner's rule (D4);
- where K3 and K5 are corrected (D5);
- what "a question the base never asked" means as a test (D6).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does `ENV_OPTIONS` take GNU's `--quoting-style`, which coreutils' `src/env.c` has but no release ships yet? | a person, decided by the frame. Why the tree could not settle it alone: the sources give the fact, and including an unreleased option is a choice about what the table promises | (a) released options only, as of 9.12, which round 3 chose; (b) everything `src/env.c` at `f799b2f48a61` holds | (b). Every GNU env without the option rejects the word and runs nothing. So the row only stops the GNU walk from reading past a value no released env accepts. Without it, `env --quoting-style X -vS '…'` is missed under GNU's next release, which would reopen this finding as round 4. The table's comment names the commit, so a rename before release is visible | ✅ decided by the frame 2026-10-03 |
| Q2 | Does #738 (🟡 15, a checkout whose name carries a redirection is never asked) ride along? | a person, decided by the frame. Why the tree could not settle it alone: the owner's rule says what a zero count permits, not what must be built | (a) apply the round-3 `_names_anew` fence; (b) leave it in its backlog milestone; (c) name it in `docs/worktree-guard-spec.md` §*Known limits* now | (b). The fence asks *switches a branch* of `git checkout README.md>/dev/null`, a glued restore (the round-3 report's own run: 124 passed, 1 failed). That is 🟡 13's class, inside the work item that removes it, and S5's criterion (a) refuses it whatever the corpus count. A correct fix needs a tree inside C, which #689 forbids for the wider reading. It is no regression: every commit from `233f0455` on is silent there. (c) is #738's own second path, and the issue can take it with S5's count | ✅ decided by the frame 2026-10-03 |
| Q3 | Are the generated comparisons planted as tests, or run as probes? | a person, decided by the frame | (a) plant all of them; (b) probes only; (c) plant the function-level generator for C (S4) and run the bash- and env-executing comparisons (S5, S10) as probes with their counts recorded | (c). S4 runs in milliseconds, needs no oracle, and pins the class 🟡 13 belongs to by construction from `_REDIRECTION`. S5 and S10 run around a thousand bash or `env` processes, and S10's GNU half is a model nobody can run here. As permanent tests they would be slow and would rest on an unexecuted oracle. #733 phase 3 recorded its corpus probe the same way | ✅ decided by the frame 2026-10-03 |
| D1 | Where GNU's and BSD's grammars read one word differently, which reading counts? | a person, decided by the frame | (a) GNU's where the word names a GNU long option, else BSD's (the round-3 fence); (b) both, with the strings unioned | (b). Executed on macOS: `env --unset -iS 'echo …'` and `env --un -vS 'echo …'` run the string, and (a) reads `-iS` and `-vS` as `--unset`'s value. `hooks/cmdline.py#reparsed_texts`' docstring sets the direction: an extra reading costs a stop, and a missed string costs a silence | ✅ decided by the frame 2026-10-03 |
| D2 | Where does BSD's `-` letter live? | a person, decided by the frame | (a) an `ENV_OPTIONS` row; (b) `_ENV_SHORT` beside the table, as the round-3 fence puts it | (b). `test_every_row_of_the_env_grammar_has_a_case` spells a short row as `-<letter>`, which for `-` is `--`, the end of the options. The table's comment says where the letter is | ✅ decided by the frame 2026-10-03 |
| D3 | Does `genv` get BSD's reading? | a person, decided by the frame | (a) yes, as `env`; (b) GNU's alone | (b). `genv` is GNU coreutils installed under a `g` prefix. Reading it as BSD would only add over-reads such as `genv --unset -iS '…'`, where GNU runs `git commit -m x` as one program word. S9 pins it | ✅ decided by the frame 2026-10-03 |
| D4 | The env change can make the commit gate stop more. Is that subject to the owner's rule? | a person, decided by the frame | (a) yes, zero or a named limit; (b) count and record it, as information | (b). The rule names a guard change that could add a question. A commit the env grammar runs and the reader missed is the gate's purpose, and `CONTRIBUTING.md`'s failure direction puts a wrong allow above a wrong deny. The count still goes in the pull request body as the prompt budget | ✅ decided by the frame 2026-10-03 |
| D5 | K3 and K5 sit in work item 1790993140's fragment, which is not folded. Are they corrected there, or cited from this item's fragment? | a person, decided by the frame | (a) corrected in place there; (b) a `Corrected ·` row here citing them | (a). `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: "One into a fragment is refused, because a fragment moves at the fold — re-stamp that fragment's row in place instead." The freeze binds released files only. E14, E16, I5 and I6 are released (`seal/releases/0.16.0.md`), so they go through `--reverify --into` | ✅ decided by the frame 2026-10-03 |
| D6 | "0.18.0 should not ship a question the base did not ask." How is that tested, given the corpus holds none of these shapes? | a person, decided by the frame | (a) the corpus count alone; (b) the generated comparison with bash as the oracle (S5 (a)) | (b), beside the corpus count. The corpus counted 0 for the defect it was meant to catch, because no recorded pair has the shape. A shape-by-shape comparison against what bash actually runs is the only check that sees a false question before a person meets it | ✅ decided by the frame 2026-10-03 |
| M1 | Does macOS `env` agree with the BSD reading on every generated shape? | a measurement: phase 2's S10 probe | A disagreement is either a reader defect, fixed in phase 2, or a shape `env` refuses that the reader over-reads, counted | The sources' reading | ⬜ |
| M2 | How many of D1's 27,351 pairs does the built C fire on? | a measurement: phase 1's corpus count | Zero builds it. One or more names the shape as a limit, under the owner's rule | The round-3 fence's 0 | ⬜ |
| W1 | How `_env_option` takes its grammar: a parameter, or two functions | the work: phase 2 | Either shape is acceptable if each walk is broken once by `mutation-check` and a case kills it | A keyword parameter | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
