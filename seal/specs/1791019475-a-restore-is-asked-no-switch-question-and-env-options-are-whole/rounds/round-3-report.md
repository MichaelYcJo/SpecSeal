# Round 3 report: #737, a restore is asked no switch question and env's options are whole

| Field | Value |
|---|---|
| Round | 3, a verifying round and the run's last |
| Target SHA | `5e4984b1` (round 2's close commit); fix range `6999b001..e8808af1`, four commits |
| Base | `2b1dcb1f` |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at `5e4984b1` under the session scratchpad; this report is the one file written in the worktree |

This round's target is round 2's fix diff, not the branch. I read
`rounds/round-1.md`, `rounds/round-2.md` and `rounds/round-2-report.md` for
coordinates and re-derived each verdict below from the code at `5e4984b1`.
The fix range touches no file under `hooks/`, so round 2's executions of the
guard and of the env reading at `72c8f5a4` describe the same code; where I
re-ran something, the row says so. The units round 2's record names under
`New units` (the rule sentence, `_shapes`, `_policy_text`, `POLICY_RULE`,
`ASKABLE` and the new case) were judged as code.

## What the account claimed, and what I found

**Yellow 5, the rule (executed, by a generator of my own).** The fix commit
`fdb342df` says the paragraph now "states candidate C's rule instead of a list
of positions, and a generated case checks the rule". The rule has two parts:
the condition (a view's words hold a kind none of its frozen segments holds)
and the list of words that make a kind.

- I wrote a generator independent of the case module's `_shapes`: 33 verbs,
  including `checkout feature/x -- README.md`, bare `checkout -B`,
  `switch -- feature/x`, `checkout -- -b`, `checkout --orphan y`,
  `worktree -q add x` and `restore README.md`. Each verb was written plain,
  behind `noglob`, `nocorrect` and `repeat 2`, after a spaced `--config-env`,
  after `-C .`, and with nine redirection operators at every position, glued
  and spaced, two at once, and inside `-C`'s value. That gave 2,859 distinct
  single commands, and the guard asks 1,189 of them.
- I re-implemented the list of words from the sentence alone and put it in
  place of `switch_kind` on both sides of `wider_only_kinds`. The condition
  holds, and the list does not. The guard and the sentence disagree in two
  places (🟡 9):
  - **A checkout naming a word before `--`.** The sentence excludes only
    "anything after `--`", so `checkout feature/x -- README.md` names
    `feature/x` and is a switch by its words. `switch_kind` returns nothing
    for any `checkout` carrying `--`. So the sentence says 37 hidden shapes
    are asked that the guard leaves silent, such as
    `2>/dev/null git checkout feature/x -- README.md`, `noglob git checkout
    feature/x -- README.md` and `git checkout &>/dev/null feature/x --
    README.md`. All three are silent through `main()`. Real git 2.54 restores
    the file and leaves HEAD on `main`, so the silence is right and the
    sentence is wrong.
  - **A bare `checkout -B`.** The sentence names `checkout -b` only.
    `switch_kind` reads `-B` as a switch with or without a name, so the guard
    asks 58 shapes the sentence does not cover (`2>/dev/null git checkout -B`
    asks through `main()`). Real git refuses that command, so nothing runs.
    The four shapes where `-B` does carry a name (`git checkout -B &>/dev/null
    y`) are silent, because the frozen segment `git checkout -B` already holds
    a switch to `switch_kind`, and does not by the sentence's words.
  - **Ambiguous: `switch -- feature/x`.** If "anything after `--`" also
    governs `switch`, the guard asks 60 shapes the sentence excludes. Real git
    switches the branch, so the question is right. Only the wording leaves
    the reading open.
- With the list corrected as in the fence below, the sentence's words and
  `switch_kind` agree on all 2,859 shapes.
- **"As git is handed it" (executed under zsh 5.9).** I ran each of the 2,859
  commands under zsh with a `git` that records its argv, read each argv with
  the sentence's words, and subtracted the frozen segments' kinds. Apart from
  the two word cases above, the only difference is `{fd}>/dev/null` in front
  of `git`, 2 shapes for each of 22 verbs, which zsh does not run as a
  command and the guard asks. bash 4.1 and later run that shape, and round
  1's container measured it. It is the guard asking where one shell runs
  nothing, which #733 settled, and not a gap in the rule.
- **Is the list of words complete?** Checked against `switch_kind` and
  `adds_a_worktree`. `switch` naming a word or `-` matches. `worktree add`
  matches both readers, which read the first argument not led by `-`.
  `checkout -b` matches, but the list omits `-B`. And the `--` clause is
  wrong as above. `checkout .` excluded and `checkout -` included both
  match. `checkout -- -b` is asked because `switch_kind` tests `-b` before
  `--` (the `KINDS` row "checkout -b before --"), and the sentence's
  `checkout -b` also covers it.

**The new case (executed).**
`test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`
passes, and the build's report about it holds.

- **The mutant survives the case.** I replaced `kind and kind not in frozen`
  with `kind` in `wider_only_kinds` and ran the module: 131 passed and 1
  failed. The failure is `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it`
  (`cd w && git checkout README.md`, through `main()`). The new case stays
  green, and one case through `main()` holds the clause. The build wrote
  "cases", and it is one.
- **Why it survives.** With no `judged` argument, `wider_only_kinds`
  subtracts `switch_kind` over `walk_command`'s segments. That is the same
  set the case builds as `frozen`. So an asked kind can never be in `frozen`,
  and the `own in frozen` half of the case's test can never fire. The
  docstring says the case checks "one none of the frozen segments of the
  command as written holds", and it cannot check that (⬜ 10).
- **The case checks the code against the code.** Its oracle is
  `switch_kind`, so it holds the condition and never the sentence's list of
  words. That list is where 🟡 9 sits.

**The policy case (executed).**
`test_the_guard_policy_says_a_hidden_file_checkout_is_asked` pins
`POLICY_RULE`, "it asks whether or not the command moves the tree", "the two
are examples, not the set" and the asked example. It does not pin the list of
words. I deleted the sentence "Each side is read by its words alone: …" from
the doc and ran the guard module: 132 passed. So no case holds the words that
make a kind.

**White 6, the changelog's first bullet (read, against the executions
above).** The detach promise and the `-q` example are gone. The bullet now
states the condition, "asks wherever those words hold a switch or a creation
that the guard's own reading of the command as written misses", and names no
list of words, so 🟡 9 does not reach it. Its example
(`git checkout &>/dev/null README.md`) is asked, as round 2 executed.

**White 7, the changelog's env sentence (executed).** At `5e4984b1`,
`reparsed_texts` reads nothing from `env --quoti --spl '…'` and reads the
string from `env --e -S '…'` and `env --e --split-string '…'`. macOS
`/usr/bin/env` refuses all three (`illegal option`). That matches the new
sentence. GNU's half is round 2's reading, carried.

**White 8, N1 and phase 1 (executed under `/bin/bash` 3.2.57 and zsh 5.9,
with a `git` that records its argv).**

- `git worktree 2>&/dev/null add ../wt b` and `git -C 2>&/dev/null . checkout
  feature/x`: bash refuses each as an ambiguous redirect. zsh hands git
  `worktree add ../wt b` and `-C . checkout feature/x`.
- `{fd}>&/dev/null` in the same places: bash 3.2 hands git `worktree {fd} add
  ../wt b` and `-C {fd} . switch feature/x`. Real git refuses both, with
  `unknown subcommand` and `cannot change to '{fd}'`.
- That is what N1 and phase 1 now say. bash 5.2's refusal is round 1's
  container run, carried.

**The ledger (executed and read).** `bin/evidence-check --strict .` exits 0:
4,049 ok, 0 drifted, 0 broken, and its records pass read 1,316 names and
refused 0. `bin/survivor-check --range 2b1dcb1f...HEAD --exempt
…/survivors.md` exits 0 over 677 files and 42 removed sentences, with the same
two survivors excused. **Read:** the new `Re-read` notes on K7, M2 and N1
against the diff. K7 and M2 say the paragraph traded its list for the rule
and their claims stand, which is true. N1 says the S4 case's generator moved
into a helper with the same shapes. The diff moves the loop verbatim into
`_shapes`, so that is true.

**The narrow run (executed).** `bin/test
tests/test_guard_resolves_the_tree_it_judges.py -q` at `5e4984b1`: 132 passed.
The broad gate is the sealer's, and I did not run it.

## Findings

### 🟡 9 — The rule's list of the words that make a kind says a checkout naming a word before `--` is asked, and leaves out a bare `-B`

`docs/worktree-guard-spec.md:631` to `:633`, the sentence "Each side is read
by its words alone: …" in §*Which tree*'s #678 paragraph. Round 2's fix
created this sentence.

- **What is wrong.** "a `switch` or a `checkout` naming a word or `-` (other
  than `checkout`'s `.` and anything after `--`)" counts a word before `--`.
  The guard's `switch_kind` returns nothing for any `checkout` carrying `--`.
  So by the sentence, `2>/dev/null git checkout feature/x -- README.md` is
  asked, and through `main()` it is silent (37 of my shapes). The sentence
  also names `checkout -b` and not `-B`, while the guard asks
  `2>/dev/null git checkout -B` (58 shapes). Whether "anything after `--`"
  governs `switch` is left open, and the guard asks
  `2>/dev/null git switch -- feature/x`.
- **Why it matters.** This is the sentence a person reads to learn when the
  guard asks. Round 2 replaced a list of positions with it because each of
  two rounds found the list false (yellows 1 and 5), and this is the same
  class one level down: the words that make a kind are again a list, and
  the list is again not the guard's. The behaviour is right in every case:
  real git restores the file without moving HEAD, refuses a bare `-B`, and
  switches on `switch -- feature/x`. Only the sentence is wrong.
- **Nothing pins it.** I deleted the sentence and the guard module stayed
  green (132 passed). The new rule case uses `switch_kind` as its oracle, so
  it cannot see a difference between the sentence and the code.
- **Fix.** State `switch_kind`'s words, pin the sentence, and add three
  `KINDS` rows so the code side holds the same words. I applied the fences
  below in my clone. With them, the two modules that read this sentence and
  three more that read the same doc passed (321), and the new pin was red
  against the current sentence. My re-implementation of the corrected words
  agreed with `switch_kind` on all 2,859 shapes.

### ⬜ 10 — The new rule case's frozen half can never fail, so a mutant dropping the per-view subtraction survives it

`tests/test_guard_resolves_the_tree_it_judges.py:1226`, in
`test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`.

- **What is wrong.** The case calls `wider_only_kinds` with no `judged`. In
  that case the function subtracts `switch_kind` over `walk_command`'s
  segments, which is exactly the set the case then builds as `frozen`. So
  `own in frozen` is false for every kind the function returns, and that
  half of the condition is dead. The docstring says it checks that no frozen
  segment holds the kind, and it does not.
- **Why it is ⬜.** The behaviour is held. The mutant `if kind:` turns
  `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` red through
  `main()`. What the case gets wrong is its own claim.
- **Fix.** Pass `judged=set()` so that only the per-view subtraction runs,
  and read `frozen` from the wider splitter's segments. Those are the views'
  sources for a single command. In my clone, with this change the case
  passes at `5e4984b1` and is red against the mutant `if kind:`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | the rule's list of words says a `checkout` naming a word before `--` is a switch and names `checkout -b` but not `-B`; the guard reads any `checkout` carrying `--` as nothing and a bare `-B` as a switch, and no case pins the list | `docs/worktree-guard-spec.md:631` | open | executed: my generator, 2,859 commands; the sentence's words in place of `switch_kind` differ on 37 shapes (a name before `--`, silent through `main()`) and 58 shapes (a bare `-B`, asked through `main()`); deleting the sentence leaves the module green; real git restores without moving HEAD and refuses a bare `-B`. The same class as yellows 1 and 5, in a unit round 2's fix created |
| ⬜ 10 | the new rule case's `own in frozen` half can never fire, because the function-level default already subtracts the same set; its docstring claims a check it does not make | `tests/test_guard_resolves_the_tree_it_judges.py:1226` | open | executed: the mutant dropping `kind not in frozen` leaves the case green, and only `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` fails; read: the default `judged` and the case's `frozen` are the same expression. Behaviour held, so not counted in `Needs a fix` |
| 🟢 | round 2's yellow-severity finding 5 is closed for what it named — the detach promise and the list of positions are gone, and the rule's condition matches the guard | `docs/worktree-guard-spec.md:628` | confirmed | executed: over 2,859 commands of my own generator, the condition with `switch_kind`'s words and the guard agree on every shape; under zsh-handed argv, the only other difference is `{fd}` in front of `git`, which bash 4.1 runs. The residual, in the list of words, is finding 9 |
| 🟢 | round 2's white 6 is closed — the changelog's first bullet states the condition, with no detach promise and no `-q` example | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:3` | confirmed | read against the executions above; the bullet names no list of words, so finding 9 does not reach it |
| 🟢 | round 2's white 7 is closed — the env sentence is narrowed to an abbreviated split string, and says a fully spelt `-S` is still read | `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/changelog.md:25` | confirmed | executed: `reparsed_texts` reads nothing from `env --quoti --spl`, and reads the string from `env --e -S` and `env --e --split-string`; macOS `env` refuses all three |
| 🟢 | round 2's white 8 is closed — N1 and phase 1 say zsh runs the `-C` value shapes as a switch and bash 3.2 hands git `{fd}` | `seal/ledger/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole.md` N1 | confirmed | executed under bash 3.2.57 and zsh 5.9 with a recording `git`, then real git on bash's argv: both refused |
| 🟢 | the build's report that the mutant dropping `kind not in frozen` survives the new case and is held through `main()` | `hooks/worktree-guard.py:368` | confirmed | executed: 131 passed, 1 failed, and the one is `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it`; one case holds it, not several |
| 🟢 | K7, M2 and N1 re-read and re-stamped; the ledger reads clean and the survivors are excused | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K7 | confirmed | executed: `evidence-check --strict .` exit 0, 4,049 ok, 0 drifted, 0 broken, 0 of 1,316 names refused; `survivor-check` exit 0, two excused; read: the three notes against the diff |
| ❓ | carried from rounds 1 and 2: whether 0.18.0 ships the tree-blind questions `233f0455` never asked (`questions.md` D6) | `questions.md` D6 | ❓ out of verified scope | a decision, not a check; nothing in the fix range changes it. Who answers it: the repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` at `5e4984b1` | 132 passed |
| my own generator, 2,859 single commands over 33 verbs, nine operators, every position, two at once, zsh prefixes, spaced `--config-env`, inside `-C`'s value; `wider_only_kinds` against the same with the sentence's words in place of `switch_kind` | guard asks 1,189; differ on 37 (a name before `--`: the sentence asks, the guard does not) and 58 (a bare `-B`: the guard asks, the sentence does not); 60 more under the reading where "after `--`" governs `switch` |
| the same 2,859 commands under zsh 5.9 with a `git` recording its argv, read with the sentence's words, frozen segments subtracted | the same two word cases, plus `{fd}>/dev/null` before `git` on 2 shapes per verb, which zsh does not run as a command |
| six commands through `main()` in a dirty `w` under a clean session (a probe case, deleted) | silent: three `checkout feature/x -- README.md` hides; ask: `checkout -B`, `switch -- feature/x`, `checkout README.md`, each behind `2>/dev/null` |
| real git 2.54 on `checkout feature/x -- README.md`, `switch -- feature/x`, `checkout -B`, `checkout -b` in fresh repositories | HEAD stays on `main`; switches to `feature/x`; exit 129; exit 129 |
| mutant: `kind and kind not in frozen` made `kind` in `wider_only_kinds`, the guard module run | 131 passed, 1 failed: `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` |
| mutant: the sentence "Each side is read by its words alone: …" deleted from the doc, the guard module run | 132 passed |
| the fences under 🟡 9 and ⬜ 10 applied in the clone; the five modules that read `docs/worktree-guard-spec.md` run; the rule case against the mutant; the new pin against the current sentence; the corrected words against `switch_kind` over my generator | 321 passed; the rule case red against the mutant; the pin red; 0 of 2,859 differ |
| `/bin/bash` 3.2.57 and zsh 5.9 on `2>&/dev/null` and `{fd}>&/dev/null` before `add` and inside `-C`'s value, with a recording `git`; real git on bash's argv | bash: ambiguous redirect, or `{fd}` handed to git, which refuses it; zsh: `worktree add ../wt b`, `-C . checkout feature/x`, `-C . switch feature/x` |
| `reparsed_texts` on three env shapes, macOS `/usr/bin/env` on each | `--quoti --spl` reads nothing; `--e -S` and `--e --split-string` read the string; env refuses all three |
| `bin/evidence-check --strict .` in the clone at `5e4984b1` | exit 0; 4,049 ok, 0 drifted, 0 broken; records: 5 work items, 1,316 names read, 0 refused |
| `bin/survivor-check --range 2b1dcb1f...HEAD --exempt …/survivors.md` | exit 0; 677 files, 42 removed sentences, two survivors excused |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet: not run by this round; the sealer's, once the rounds settle (contract §2) |

## Paste-ready fixes

### 🟡 9

In `docs/worktree-guard-spec.md`, replace these three lines and the start of
the fourth:

```
side is read by its words alone: a `switch` or a `checkout` naming a word or
`-` (other than `checkout`'s `.` and anything after `--`), a `checkout -b`, or a
`worktree add`. The reading looks up no tree (#689), so it asks whether or not
```

with:

```
side is read by its words alone: a `switch` naming a word or `-`, a `checkout`
carrying `-b` or `-B`, a `checkout` with no `--` among its words that names
`-` or a word other than `.`, or a `worktree add`. The reading looks up no
tree (#689), so it asks whether or not
```

At the end of `test_the_guard_policy_says_a_hidden_file_checkout_is_asked`:

```python
    assert (
        "a `switch` naming a word or `-`, a `checkout` carrying `-b` or `-B`, a "
        "`checkout` with no `--` among its words that names `-` or a word other "
        "than `.`, or a `worktree add`"
    ) in text
```

In `KINDS`, after the "checkout with no name" row:

```python
    # §*Which tree*'s words: a `--` takes every name out of a checkout, and
    # `-B` is a switch with or without one (round 3 of #737).
    "checkout a name before --": (["git", "checkout", "x", "--", "f"], None),
    "checkout -B with no name": (["git", "checkout", "-B"], "switch"),
    "switch -- a name": (["git", "switch", "--", "x"], "switch"),
```

The ledger rows citing §*Which tree* (K7 and M2) will drift with the sentence
and need the usual re-read note.

### ⬜ 10

In `test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers`,
replace:

```python
            kinds = wg.wider_only_kinds(command, str(tmp_path))
            if not kinds:
                continue
            asked += 1
            frozen = {
                wg.switch_kind(wg.parse_git(tokens))
                for tokens, _wheres in wg.walk_command(command, str(tmp_path))
            }
```

with:

```python
            # `judged=set()`: the function-level default subtracts what the
            # frozen walk's words hold, which is this case's own frozen half,
            # and would leave nothing for it to check.
            kinds = wg.wider_only_kinds(command, str(tmp_path), judged=set())
            if not kinds:
                continue
            asked += 1
            text = wg.wide.drop_heredoc_bodies(wg.wide.drop_comments(command))
            items, _clean = wg.wide.split_segments_with_separators(text)
            frozen = {wg.switch_kind(wg.parse_git(tokens)) for _sep, tokens in items}
```

## Regression tests to plant

- For 🟡 9: the pin and the three `KINDS` rows in the fence above, in
  `tests/test_guard_resolves_the_tree_it_judges.py`. Shown red: the pin
  fails against the sentence at `5e4984b1`. The `KINDS` rows pass at
  `5e4984b1`, because they pin the code to the words the corrected sentence
  states.
- For ⬜ 10: the change in the fence above, in the same module. Shown red
  against the mutant `if kind:` in `wider_only_kinds`, and green at
  `5e4984b1`.

## Facts for the evidence ledger

- git 2.54 (Apple Git-157): `git checkout feature/x -- README.md` leaves HEAD
  on the current branch; `git switch -- feature/x` switches; a bare `git
  checkout -B` or `-b` exits 129 (`switch 'B' requires a value`). Executed on
  2026-10-03.
- zsh 5.9 does not run `{fd}>/dev/null git …` written at the start of a
  command, and the guard asks it. Executed on 2026-10-03.

## Not verified

| Item | Who must answer |
|---|---|
| bash 4.1 or later on the `{fd}` shapes in front of `git`; I have bash 3.2 only, and round 1's container runs are carried | a reviewer with bash 4.1 or later, if wanted |
| GNU's half of the env sentence against a real GNU `env`; read in round 2, carried | a reviewer or a CI leg with GNU coreutils 9.12 or later |
| the full suite, lint and typecheck | the sealer, after the rounds settle |

Needs a fix: yes — 🟡 9, the list of words in `docs/worktree-guard-spec.md` §*Which tree*'s rule, which counts a checkout's name before `--` and leaves out a bare `-B`, and which no case pins

Loses a record or crashes: no

## Proof block

Files opened: `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/rounds/round-1.md`,
`rounds/round-2.md` and `rounds/round-2-report.md`; the fix diff
`6999b001..e8808af1` in full (`docs/worktree-guard-spec.md`, both ledger
fragments, `changelog.md`, `phases/phase-1.md`,
`tests/test_guard_resolves_the_tree_it_judges.py`) and the close commit's
stat; `docs/worktree-guard-spec.md` lines 600 to 660;
`hooks/worktree-guard.py` (`walk_command`, `switch_kind`, `wider_only_kinds`,
`_bare_words`, `classify`'s head, `main` up to the ladder);
`hooks/cmdline.py` (`adds_a_worktree`, `apply_chdir`);
`tests/test_guard_resolves_the_tree_it_judges.py` (`_redirections`,
`RESTORES`, `_shapes`, `_policy_text`, `POLICY_RULE`, `ASKABLE`, the rule
case, the policy case, `KINDS`, and the cases from
`test_a_restore_before_a_hidden_switch_does_not_silence_the_question` to
`test_candidate_c_reads_a_redirection_glued_to_git`); `bin/test`.
