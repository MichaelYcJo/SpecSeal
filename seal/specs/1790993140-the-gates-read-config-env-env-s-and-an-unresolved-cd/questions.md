# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The owner answered once, on 2026-10-03: #686
and #678's guard half are decided by a count over the recorded runs, zero
stops builds the ask and one or more keeps the fallback with the count named.
That answer is an input to this frame, not a question in it.

**Judgments the tickets left open that the tree answered**, listed so nobody
reopens them. Each is a `D` row below with its grounds:

- which transcripts count as "the recorded runs" (D1);
- one count per issue rather than one for both, and the creation arm left out
  of #686 (D2);
- the count as an upper bound (D3), and no command excluded from it (D7);
- what "unresolved" means to the guard (D4), and what "asks" means (D5);
- how P4's "no rule added" and the owner's 2026-10-03 rule fit together (D6);
- how `env -S` is read (D8), and how the frozen policy file changes (D9);
- consent first for a creation only the wider reading finds (D10).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| D1 | Which transcripts are "the recorded runs" the owner's rule counts over? | a person, decided by the frame: the tree answers it, so no person is waiting on it | (a) #674 Q2's three sessions; (b) every transcript of this repository on this machine; (c) (b) cut at a moment | (c): every main and subagent transcript under `~/.claude/projects/<this repository's slug>/`, counting each Bash `tool_use` whose entry is timestamped before **2026-10-03T11:06:22+09:00**, the commit time of this work item's `routing.md` (`5c8a49f7`). Grounds: Q2's three sessions `8cadfa28`, `30ac0e06` and `ab2760f5` are not on this machine (executed: `find ~/.claude/projects -name '8cadfa28*'` and the other two returned nothing; the 0.17.0 run moved machines). 507 transcripts are there, 34 of them main (executed, `find … -name '*.jsonl' \| wc -l`). The cut keeps this run's own probes out of the corpus that judges them, and makes the count reproducible | ✅ decided by the frame 2026-10-03 |
| D2 | One count for both issues, or one per issue? And does #686 cover the creation arm? | a person, decided by the frame | (a) one count for both; (b) one per issue; (c) per arm inside each issue | (b), and #686 is the switch arm alone. Grounds: the owner's rule names each issue's shape, and (b) keeps every built piece at zero stops, which is the rule's purpose. The creation arm is left out because without consent every Bash creation row already stops (`docs/worktree-guard-spec.md` §B), and with consent the row is the owner's `automation` press, which `README.md`'s worktree-guard row promises will not ask; #686's comment of 2026-09-30 measured the creation case as "one extra ask later, never a silent pass" | ✅ decided by the frame 2026-10-03 |
| D3 | A transcript does not record whether the tree was dirty or which sessions were live. How is "adds a stop" counted? | a person, decided by the frame | (a) every pair where the candidate fires; (b) try to reconstruct tree state | (a), an upper bound. A wired candidate replaces only silences, so a pair it fires on is a stop unless the base was already stopping it for a tree-state reason the transcript cannot show. Over-counting can only keep a fallback; it can never build an ask that stops a recorded run | ✅ decided by the frame 2026-10-03 |
| D4 | What is an "unresolved" tree to the guard? | a person, decided by the frame | (a) the frozen walk's `Unresolved`; (b) (a), or the commit gate's walk disagreeing about the judged segment; (c) a scan for `cd` words | (b). (a) misses `noglob cd w` and `2>&1 cd w`, two of #686's seven shapes, because the frozen walk is confident about both (read: `hooks/cmdline_base.py#understood`). (c) is a new word list, the kind every round of #692 found short. (b) reuses #674's reading as a second opinion that never picks the tree, so #689's ordering trap does not return | ✅ decided by the frame 2026-10-03 |
| D5 | What does "the guard asks" do? | a person, decided by the frame | (a) `ask` in place of the two silent exits only; (b) `ask` in place of the whole ladder; (c) deny once, then ask | (a). Every base deny, choice and ask still decides first, so nothing is allowed that was refused (`CONTRIBUTING.md`'s failure direction). (b) would turn an ACTIVE deny into an ask. (c) is the `choose` pattern for two named ways on; here there is one question | ✅ decided by the frame 2026-10-03 |
| D6 | P4 (2026-10-01) kept the switch arm on the frozen reader "with no rule added". Does a guard-side ask break that? | a person, decided by the frame | (a) P4 binds `hooks/cmdline_base.py`'s bytes; (b) P4 forbids any new switch-arm rule | (a). The owner's rule of 2026-10-03 says the guard asks where the count is zero, which presupposes a rule can be added; the only thing that can honour both is a rule outside the frozen file. S11 keeps the bytes, and #689's lesson (the wider reading never takes the slot or picks the tree) is kept by D4 and D5 | ✅ decided by the frame 2026-10-03 |
| D7 | Are commands a reviewer typed to probe these very shapes excluded from the count? | a person, decided by the frame | (a) count every pair; (b) exclude probes | (a). Telling a probe from work is a judgment of intent the probe cannot make mechanically, Q2 excluded nothing, and a probe the guard would have stopped was a real stop in that run. D1's cut already keeps this run's own probes out | ✅ decided by the frame 2026-10-03 |
| D8 | How is `env -S '<words>'` read? | a person, decided by the frame | (a) as `env <words> <rest>`, beside the string as a command; (b) instead of it; (c) a known limit | (a). `env` splits the string into its own arguments, so `-i git commit` runs `env -i git commit`. Keeping the base reading beside it means the reader only adds, as every #670 and #674 reader did | ✅ decided by the frame 2026-10-03 |
| D9 | `docs/commit-review-gate-spec.md` is under `Over the ceiling` until #715. Where does #716's policy text go? | a person, decided by the frame | (a) reword the existing `env -S` clause in place; (b) a new document, linked | (a), with no new line and no new fold marker. The stand-aside paragraph already claims `core.hooksPath` in any spelling keeps the reading, which phase 1 makes true; only the `env -S` clause becomes incomplete | ✅ decided by the frame 2026-10-03 |
| D10 | A creation only the wider reading finds, under consent: ask or stay silent? | a person, decided by the frame | (a) consent first, silent under it; (b) ask regardless | (a). Consent is read before every row of §B, and under `automation` it is the owner's press; the README promises it. The base is silent there too, so (a) changes nothing for a consented session | ✅ decided by the frame 2026-10-03 |
| M1 | Which of git's global options take their value as a separate word? `--config-env` is one (round 3 of #692, y05, executed on 2.50.1). The synopsis of the installed git lists `-C`, `-c`, `--exec-path[=…]`, `--git-dir=`, `--work-tree=`, `--namespace=`, `--config-env=` (read: `man git` on 2.54.0); the separated forms are not all in the synopsis | a measurement: phase 1, by running `git <option> <value> status` for each candidate in a scratch repository | Each option that git accepts spaced goes into `takes_value` with a case seen red | `--config-env` alone, until measured | ✅ measured 2026-10-03 on git 2.54.0: `--config-env`, `--attr-source` and `--shallow-file` were missing and went in; `--exec-path` takes no separate value and stays (`phases/phase-1.md`) |
| M2 | Which of #686's seven shapes reach candidate A through the frozen `Unresolved`, and which through the disagreement? The frame read five and two (`plan.md` §*Technical context*) | a measurement: phase 2's unit cases | A case per shape settles it; the answer does not change what is built | The frame's reading | ✅ measured 2026-10-03: five through the frozen `Unresolved` and `noglob cd w` and `2>&1 cd w` through the disagreement, as the frame read (`phases/phase-2.md`) |
| M3 | Count A and count C over D1's corpus | a measurement: phase 3 | Zero builds the ask; one or more keeps the fallback and names the count (`plan.md` §*What phase 4 builds*) | Nothing is wired until counted | ✅ measured 2026-10-03: count A 9, so A was removed and named a known limit; count C 0, so C was wired (`phases/phase-3.md`) |
| W1 | Candidate A compares the frozen walk's directories for the judged segment with the commit gate's walk. The two splitters can cut a command differently. How is the segment matched? | the work: phase 2 | Any matching is acceptable that never returns a tree; where no match is found, A answers true, so a mismatch costs a counted stop rather than a silence | A answers true on no match | ✅ decided by the work 2026-10-03: matched to the wider walk's nth segment with the same words, true on no match (`phases/phase-2.md`); moot since A was removed in phase 4 |

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

The `D` rows are the exception the spawn prompt made: the run is unattended and
nobody is left to ask, so each was decided by the frame with a stated default
and its grounds, and is ticked as decided rather than answered. A reviewer who
opens what the grounds cite can overturn any of them.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
