# Round 1 report — work item 1790993140 (#716, #678's guard half, #686)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `07a3dc7f` |
| Base | `233f0455` (`origin/release/v0.18.0`) |
| Diff | `233f0455..07a3dc7f` |
| Ran by | specseal:warden on claude-opus-5-5 |
| Earlier rounds | none |

Spec compliance first, then quality. The implementer's account (`overview.md`,
`phases/phase-1.md` to `phase-5.md`, the commit messages) was read whole and
treated as claims; each one below says what was claimed and what the code or a
run showed.

## Summary

The count that decided #686 and #678 was honestly produced, and the build
followed it. A re-count with the built functions over the same corpus and the
same cut reproduced every published figure to the digit. Candidate A
(#686) was removed and named as a limit. Candidate C (#678) was wired only at
the guard's silent exits. It takes no tree and no first slot, and it reads
consent first for a creation.

Three defects need a fix. Two are in the commit gate's new `env -S` reading,
and one is in candidate C's subtraction:

1. The new reading of `env`'s own words adds stops on `env -S` commands that
   hold **no commit**, in a declared repository too. That breaks the PR's own
   "prompt budget" sentence (🟡 1).
2. The `env -S` class is not enumerated. `env -iS 'git commit -m x'` runs a
   commit on macOS and is still found by nothing (🟡 2).
3. Candidate C subtracts what the frozen reading's *words* find, not what its
   loop judged. A file restore written before a hidden switch therefore
   silences the question C exists to ask (🟡 3). The fix fires on none of the
   27,351 corpus pairs, so the owner's rule still holds for it.

Four ⬜ follow. Two of them are corrections to the ledger edits.

## Stage 1 — spec compliance

### The count (S6, S8, D1, D3, D7) — honestly produced

**Claimed** (`phases/phase-3.md`): 511 transcripts, 27,551 Bash tool uses
before 2026-10-03T11:06:22+09:00, 27,351 distinct pairs, 395 holding a frozen
switch, 51 a creation, count A = 9 (all through the frozen `Unresolved`),
count C = 0, no pair raised. The self-check fired on all seven #686 shapes and
all nine S9a shapes.

**Found, executed.** A probe in the round's scratch directory loaded phase 3's
candidate A from `c7f84438:hooks/worktree-guard.py` and candidate C from the
target SHA. It read the corpus D1 fixes with D1's cut and reproduced: 27,551
uses, 27,351 pairs, 395 and 51, **A = 9, C = 0**, nothing raised. The self-check
also matched: A was true for all seven shapes, and C gave the expected kind for
all nine. The directory now holds 513 transcripts, and the cut covers the same
entries. The nine A pairs are the nine shapes the phase record tabulates. A first
pass that read the transcripts with `str.splitlines` lost 9 pairs to U+2028
inside JSON lines. It still gave A = 9 and C = 0, and the second pass, which
reads the file line by line, matches exactly.

- **Same functions.** The deleted probe cannot be opened. What can be shown is
  that the built functions give exactly its figures. Between the counted commit
  `c7f84438` and the target, `wider_only_kinds` gained only the `wide is None`
  guard, and `switch_kind` lost only the `-c`/`-C` test, which no valid
  `git switch` reaches (read). `hooks/cmdline.py` has no diff between
  `c7f84438` and `07a3dc7f` (executed, `git diff --stat`).
- **D1's cut excludes this run.** The cut is the author time of `5c8a49f7`,
  11:06:22+09:00 (executed). The frame commit (11:22:54) and every build commit
  come after it. The corpus is complete for this machine: the only other
  SpecSeal project directory holds 0 transcripts (executed).
- **Nothing but counts reached a committed file.** The diff's added lines carry
  no temporary path, no session id, no user path and no transcript fragment
  (executed grep). The phase-3 table describes shapes in its own words.

### Phase 4 followed the count

A was deleted with its unit cases. §*Known limits* carries the count, the
corpus and the date, and the seven shapes are pinned silent by
`test_a_switch_tree_the_guard_cannot_place_is_judged_as_its_own`. C is wired.
The import is kept because a candidate was wired (plan, *In every branch*).

### Candidate C, as wired

- **No tree, no first slot (#689, S5–S7).** `quiet()` replaces only the
  `sys.exit(0)` exits after the walk (read, `hooks/worktree-guard.py` main).
  Every ask it gives leaves `top` None, and `WIDER_FIRST` still denies.
  Executed: the guard module ran green at the target.
- **Consent first (D10).** `ask_what_only_the_wider_reading_finds` reads
  consent before it asks. Executed: a hidden creation under consent is
  silent. But the consent it reads is the session clone's, not the creation's
  (⬜ 4).
- **The subtraction.** It is by kind, and against `switch_kind` over the frozen
  segments. The plan said "for each kind the frozen loop did NOT find" (🟡 3).

### The guarded import

**Claimed:** a broken `hooks/cmdline.py` leaves the ACTIVE deny in force.
**Found:** an import that raises an `Exception` leaves `wide` as None, and every
row that speaks runs before `quiet()`, so the ACTIVE deny is untouched (read).
`test_a_broken_shared_module_names_every_gate_that_imports_it[cmdline]` passed
at the target (executed). One shape escapes: a module body that raises
`SystemExit`, which `hooks/dispatch.py` and its S7 case treat as a real failure
(⬜ 5).

### #716 — the two readings

- **`env -S` both ways, with redirections — executed.** A redirection after
  the string, before the option, between the option and the string, after the
  glued form, and after `--split-string=`: each is found at the target and was
  not at the base. `env -u FOO -S '-i git commit -m x'` and
  `env -S '-u FOO git commit -m x'` are found too.
- **`takes_value` — executed on git 2.54.0.** `--attr-source HEAD status`,
  `--shallow-file x status`, `--config-env core.x=HOME status` and
  `--namespace n status` all ran `status`. `--exec-path status` printed the path
  and exited, so it is rightly left as is. No option git does not separate was
  added.
- **Does any shape the gate stopped go silent? — No.** Only a command where a
  new option swallows the subcommand reads differently
  (`git --shallow-file commit -m x`). Git refuses each such command and commits
  nothing: exit 129, 129 and 128 (executed). The `env` reading only adds texts
  (read).
- **But it adds stops it should not, and misses part of its class** (🟡 1,
  🟡 2).

### Frozen files

`docs/commit-review-gate-spec.md` is 1047 lines before and after, and its 19
comment markers are byte-identical in place (executed). The reword is the one
clause D9 allows. `hooks/cmdline_base.py` has no diff against `233f0455`
(executed), and `tests/test_the_frozen_reading_never_grows.py` passed (executed).

### The ledger edits

The four in-place corrections in `seal/releases/0.16.0.md` and the M4 notes
correction were each read against the edit:

- **I9** — holds. The guard's policy still names a redirected git as one it
  does not read, and the creation now leaves the silent group.
- **M2** — holds.
- **M3** — holds. The cited case asserts `ask` with `top` None.
- **M4** — holds. `hooks/cmdline.py` is no longer `542f920b`'s, which the note
  says. It is written in the notes cell, as the row's own 2026-10-01
  correction was.
- **M1** — its correction contradicts itself (⬜ 7).

Of the 17 re-reads, 16 hold against the edit, which only turns silent exits
into asks. **W10** in `seal/releases/0.15.6.md` does not: its claim is about
the commands a reason prints, and the new reason prints commands that name no
tree (⬜ 6).

## Stage 2 — quality

### 🟡 1 — `env`'s own words stop `env -S` commands that hold no commit, in a declared repository

`hooks/cmdline.py:1740` (`_env_words`) and `hooks/cmdline.py:1871`
(`command_strings`' env arm).

**What is wrong.** `command_strings` hands its env arm to `reparsed_texts`,
which now returns the env-words text beside the string. That text is then asked
the expansion question, `names_an_unknown_command`. Behind `env`, a later word
that expands counts as a command word (I5), so a variable among env's own
option values, or among the operands after the string, reads as an unknown
command. Separately, the join is unquoted, so a quoted operand holding `&&` or
`;` becomes a list.

**Executed.** Through `main()` in a **declared** repository, each of these is a
`deny` at `07a3dc7f` and `silent` at `233f0455`. None of them commits:

| Command | Base | Target |
|---|---|---|
| `env -u "$V" -S 'echo hi'` | silent | deny |
| `env -C "$D" -S 'echo hi'` | silent | deny |
| `env -S 'echo' "$X"` | silent | deny |
| `env -S 'echo' 'a && git commit -m y'` | silent | deny |
| `env -S 'printf %s' 'x; git commit -m y'` | silent | deny |

**Why it matters.** The failure direction is stricter, so nothing is let
through. But the PR's prompt-budget sentence (`phases/phase-5.md:67`) promises
a stop only "on a command holding a spaced `--config-env` or an `env -S`
before a commit", and the shapes above are neither. In an `automation` session
each one is a refusal the run has to route around. The S5 controls held no
variable and no metacharacter, so nothing pinned this. Over D1's corpus no pair
holds an `env` split string at all (executed, 0 of 27,351), so the measured
budget is zero. The defect is in the claim and in the code, not in a figure.

**Fix.** Ask the expansion question of the split string alone, as the base
did. Quote every word but the string when the env-words text is built. Fenced
below; it was verified together with 🟡 2's fence.

### 🟡 2 — the `env -S` class is not enumerated: a cluster and an abbreviation still hide a commit

`hooks/cmdline.py:1726` (the env arm of `reparsed_texts`).

**What is wrong.** `spec.md` §*Scope* 1 asks for "every spelling of `env`'s
split string". The arm knows `-S`, `-S<s>`, `--split-string` and
`--split-string=`. It does not know a short-option cluster ending in `S`, or
GNU getopt's unambiguous prefixes of `--split-string`.

**Executed.** macOS `env -iS 'echo cluster-iS'` and `env -vS '…'` run the
string (exit 0). `env -iS 'git commit -m x'`, `env -vS '-i git commit -m x'`
and `env --split '-i git commit -m x'` are found by nothing, at the target and
at the base. `env -iS` is #716's own shape with the `-i` moved into a cluster.
It empties the environment, so the git hook stub sees no session either
(`spec.md`'s table, y09). It is a commit no gate judges.

**Why it matters.** Contract §12: the fix is owed to every instance the same
cause produces. The cause here is a spelling of the split string the reader
does not parse.

**Fix.** Recognise a cluster and an abbreviation only among env's own options,
before its command word. `env ls -lS "$DIR"` is `ls`'s `-S`, and reading it as
a split string would add a stop. The base spellings stay read anywhere, as
they were. Fenced below with its cases. Verified in the round's clone together
with 🟡 1 and 🟡 3: 706 passed, and ruff check and format were clean.

### 🟡 3 — a file restore before a hidden switch silences candidate C's question

`hooks/worktree-guard.py:336` (`wider_only_kinds`' `found`) and
`hooks/worktree-guard.py:2247` (`quiet`).

**What is wrong.** `found` is `switch_kind` over the frozen segments, which is
the word-level upper bound. `classify` can reject a segment that `switch_kind`
calls a switch, such as `git checkout <path>` or `git checkout <no ref>`. When
it does, the frozen loop judges no switch, and the hidden switch's kind is
still subtracted.

**Executed**, over a dirty `w` under a clean session:

| Command | Target |
|---|---|
| `cd w && 2>/dev/null git switch feature/x` | ask |
| `git checkout README.md && cd w && 2>/dev/null git switch feature/x` | **silent** |
| `git checkout nosuch; cd w && 2>/dev/null git switch feature/x` | **silent** |

**Why it matters.** `docs/worktree-guard-spec.md:619` and K5 say a switch only
the commit gate's reading finds "is put to the person instead of passing
silently". The plan's step 1 says "for each kind the frozen loop did NOT find".
The overview's divergence row argues that the discard in `quiet` could never
change an answer, and that is true. But the subtraction inside
`wider_only_kinds` is the same discard, done against the superset.

**Fix.** Subtract per view, so a view the frozen parser reads as the same kind
is not hidden. Then subtract the kinds the loop actually judged, which `main`
passes in. **Executed:** over D1's corpus, the per-view reading fires on 0 of
27,351 pairs, so the fixed C still counts zero under the owner's rule. It also
drops the second frozen walk from every silent exit. In-process, the wired
version cost 6.1 ms per pair and the per-view version 2.6 ms. Fenced below with
a case that is silent at `07a3dc7f`.

### ⬜ 4 — a hidden creation reads the session clone's consent, not the creation's

`hooks/worktree-guard.py:359`. **Executed**, with consent recorded for the
session's clone only:

- `cd <other clone> && git 2>&1 worktree add ../wt-o b` is silent. The plain
  spelling, `cd <other clone> && git worktree add ../wt-o b`, is a deny.
- From a cwd in no repository, `git -C <session> 2>&1 worktree add ../wt-n b`
  asks. The plain spelling allows.

The base is silent for both hidden shapes, so nothing regressed. But
D10's "exactly as `guard_worktree_creation` does" holds only where the
creation lands in the session's clone. C cannot place the creation (by design,
#689), so cwd's clone stands in. **Fix:** say so in the policy (fenced).

### ⬜ 5 — the guarded import misses `SystemExit`

`hooks/worktree-guard.py:143`. It reads `except Exception:`, while
`hooks/dispatch.py` catches `(Exception, SystemExit)` and
`test_a_system_exit_at_load_does_not_take_the_group_down` treats a module body
that exits as a real failure. A `hooks/cmdline.py` whose body raises
`SystemExit` would still take the guard down, and its ACTIVE deny with it.
No such body exists today: the module imports only `os`, `re` and `shlex`
(read). **Fix:** fenced.

### ⬜ 6 — W10's re-read does not check W10's claim (ledger correction)

`seal/releases/0.15.6.md:17`. W10 says every command a guard reason tells the
person to run names its tree, "except two". The new reason prints
`git switch …` and `git worktree add …`, which name no tree, with
`git -C <dir>` as a placeholder. That is a third exception, of the same kind as
the second. The re-read note says only that every row that speaks still
decides first, which is not what W10 claims. This is a correction under
`seal/releases/`, so it is outside `Needs a fix`.

### ⬜ 7 — M1's correction says the verdict kinds are still `86256492`'s (ledger correction)

`seal/releases/0.16.0.md:247`. The 2026-10-03 correction says "the kinds it
judges a verdict on … are still `86256492`'s". The new `ask` is a verdict on a
kind only the wider reading recognises. The correction also calls
`wider_only_kinds` a question asked of `hooks/cmdline.py`, but it is the
guard's own function, which reads that module's splitter and `parse_git`. This
is a correction under `seal/releases/`, outside `Needs a fix`.

## Regression tests to plant

All are fenced under *Paste-ready fixes*.

- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
  gets `HANDED` entries for the cluster and the abbreviation, each found by
  nothing at `07a3dc7f`. It also gets `CONTROLS` entries for the four
  env-words false stops, each a deny in a declared repository at `07a3dc7f`,
  and for `ls -lS`.
- `tests/test_guard_resolves_the_tree_it_judges.py` gets the restore before a
  hidden switch, silent at `07a3dc7f`.

The `ls -lS` control pins the own-options limit of 🟡 2's fence and passes at
the target. See it red by dropping the `own` gate (the `own and not value`
argument) before planting it (contract §15).

## Facts for the evidence ledger

- Phase 3's figures were reproduced by round 1 with the built functions: A = 9,
  C = 0, 27,351 pairs, 395 and 51. Executed 2026-10-03. This is a re-run of K5
  and K6's measurement and needs no new anchor.
- Over D1's corpus, 0 pairs hold an `env` split string or a spaced
  `--config-env`, `--attr-source` or `--shallow-file`. Executed 2026-10-03.
  This is the commit gate's measured prompt budget for #716, if the PR wants a
  figure there.
- After 🟡 3's fix, K5's anchors on `wider_only_kinds` and `main` drift, and K5
  should say "a kind the frozen loop judged is never reported".

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `env`'s own words are asked the expansion question and joined unquoted, so `env -S` commands holding no commit now deny, in a declared repository too | `hooks/cmdline.py:1740` | open | executed: five shapes deny at `07a3dc7f`, silent at `233f0455`; the PR's prompt-budget sentence promises otherwise |
| 🟡 2 | the `env -S` class misses a cluster ending in `S` and GNU's `--split-string` prefixes; `env -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1726` | open | executed: macOS `env -iS` and `-vS` run the string; three commit shapes found by nothing at target and base |
| 🟡 3 | candidate C subtracts the frozen words' kinds, not the loop's verdicts, so a restore before a hidden switch silences the question | `hooks/worktree-guard.py:336` | open | executed: two shapes silent where the bare hidden switch asks; the per-view fix fires on 0 of 27,351 corpus pairs |
| ⬜ 4 | a hidden creation reads the session clone's consent, not the creation's | `hooks/worktree-guard.py:359` | open | executed: silent into another clone where the plain spelling denies; asks from a non-repo cwd where the plain spelling allows; base silent for both |
| ⬜ 5 | the guarded import catches `Exception` but not `SystemExit` | `hooks/worktree-guard.py:143` | open | read: `hooks/dispatch.py` catches both; no such module body exists today |
| ⬜ 6 | W10's re-read does not test its claim; the new reason is a third exception | `seal/releases/0.15.6.md:17` | open | read; ledger correction, outside `Needs a fix` |
| ⬜ 7 | M1's correction says the verdict kinds are still `86256492`'s | `seal/releases/0.16.0.md:247` | open | read; ledger correction, outside `Needs a fix` |
| 🟢 | phase 3's count was honestly produced: the built functions reproduce A = 9, C = 0 and every denominator | `phases/phase-3.md` | confirmed | executed re-count with `c7f84438`'s A and the target's C over D1's cut |
| 🟢 | the probe fired on the issues' own shapes before a zero was trusted | `phases/phase-3.md` | confirmed | executed: 7 of 7 for A, 9 of 9 for C |
| 🟢 | D1's cut excludes this run's own commands, and the corpus is complete for the machine | `questions.md` D1 | confirmed | executed: cut equals `5c8a49f7`'s time; the other SpecSeal project directory holds 0 transcripts |
| 🟢 | nothing from the corpus but counts and rewritten shapes reached a committed file | `233f0455..07a3dc7f` | confirmed | executed grep over the added lines |
| 🟢 | phase 4 followed the count: A removed and named a limit, C wired | `docs/worktree-guard-spec.md` | confirmed | read; the `UNPLACED` pins and the `WIDER_ONLY` cases passed (executed) |
| 🟢 | candidate C takes no tree or first slot, and `WIDER_FIRST` still denies | `hooks/worktree-guard.py` main | confirmed | read; the guard module passed at the target (executed) |
| 🟢 | a broken `hooks/cmdline.py` that raises leaves the ACTIVE deny in force | `hooks/worktree-guard.py:141` | confirmed | read; the broken-shared-module case passed (executed) |
| 🟢 | `env -S` is read both ways with redirections, and no added option is one git does not separate | `hooks/cmdline.py` | confirmed | executed on git 2.54.0 and through the reader |
| 🟢 | no shape the commit gate stopped goes silent | `hooks/cmdline.py` | confirmed | executed: the three swallowed-subcommand shapes commit nothing in git |
| 🟢 | the frozen policy file has no net growth, and the frozen reader is byte-identical | `docs/commit-review-gate-spec.md` | confirmed | executed: 1047 lines, 19 markers identical; `hooks/cmdline_base.py` no diff |
| 🟢 | the I9, M2, M3 and M4 corrections and 16 of the 17 re-reads hold against the edit | `seal/releases/0.16.0.md` | confirmed | read row by row; W10 and M1 are ⬜ 6 and ⬜ 7 |

## Executed probes

| What was run | Result |
|---|---|
| Re-count of phase 3: `c7f84438`'s candidate A and the target's candidate C over D1's corpus and cut | 27,551 uses, 27,351 pairs, 395 switch, 51 creation, A = 9, C = 0, none raised; self-check 7 of 7 and 9 of 9 |
| The per-view subtraction of 🟡 3 over the same 27,351 pairs | fires on 0; 2.6 ms per pair against 6.1 ms for the wired version |
| `git <option> <value> status` on git 2.54.0 for `--attr-source`, `--shallow-file`, `--config-env`, `--namespace`, `--exec-path` | the first four ran `status`; `--exec-path` printed its path and exited |
| `git <new option> commit --allow-empty -m x` for the three added options | exit 129, 129, 128; no commit |
| macOS `env -iS`, `env -vS`, `env --split-string=` | the two clusters ran the string; `--split-string` is GNU's alone (`illegal option`) |
| `env -S` shapes through `commit_invocations` at target and base | redirection shapes found at the target only; clusters and the abbreviation found at neither |
| Five `env -S` controls through `main()` in a declared repository, target and base | deny at the target, silent at the base |
| Guard probe: a restore or a no-ref checkout before a hidden switch | silent; the bare hidden switch asks |
| Guard probe: consent for the session's clone with a hidden creation elsewhere | silent into another clone (plain spelling denies); ask from a non-repo cwd (plain spelling allows) |
| Corpus count of `env` split strings and spaced added options | 0 of 27,351 |
| Narrow run at the target: the guard module, the wrapper module, the frozen-reading module, the broken-shared-module case, the commit-gate-decides module | 955 passed, 72 skipped |
| The three 🟡 fences applied in the clone, then the guard, wrapper and frozen-reading modules and the broken-shared-module case | 706 passed; ruff check and format clean on the four files |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet: the sealer's, after the rounds settle |

The probe files, the two scratch clones and every scratch directory this round
made were deleted before hand-over.

## Paste-ready fixes

### 🟡 1 — ask the expansion question of the string alone, and quote env's other words

```python
# hooks/cmdline.py

def reparsed_texts(tokens, env_words=True):
    # (body as now; the env arm is replaced by 🟡 2's fence, which carries
    # the `if env_words:` guard on every `_env_words` call)
    ...


def _env_words(word, before, after):
    # (docstring as now)
    after = _without_redirections(after)
    if not after:
        return []
    # Only the string is split again; every other word reached `env` as ONE
    # argument, so it is quoted back into one (`env -S echo 'a && b'` runs
    # `echo` with one operand, not a list).
    head = [shlex.quote(w) for w in _without_redirections(before)]
    tail = [shlex.quote(w) for w in after[1:]]
    return [" ".join([word, *head, after[0], *tail])]


# in command_strings, the env arm:
        elif word in ("env", "genv"):
            # The split string alone: `env`'s own words carry its options'
            # values and the operands after the string, which `env` runs as
            # arguments and never as a command word (round 1 of 1790993140).
            out += reparsed_texts([tok, *rest], env_words=False)
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, CONTROLS
    # Round 1 of 1790993140: env's own words are arguments to `env`, so a
    # variable among them names no command, and a quoted operand stays one
    # word. Each was a deny in a declared repository at `07a3dc7f`.
    "env -S behind an option's variable value": "env -u \"$V\" -S 'echo hi'",
    "env -S behind a variable directory": "env -C \"$D\" -S 'echo hi'",
    "env -S with a variable operand": "env -S 'echo' \"$X\"",
    "env -S with a quoted operand holding a list": "env -S 'echo' 'a && git commit -m y'",
```

### 🟡 2 — every spelling of the split string, among env's own options

```python
# hooks/cmdline.py, the env arm of reparsed_texts
        elif word in ("env", "genv"):
            # OWN: still among env's own options, where a cluster or an
            # abbreviation can spell the split string. The base spellings are
            # read anywhere, as they always were.
            own, value = True, False
            for j, t in enumerate(rest):
                at = _env_split_at(t, own and not value)
                if value:
                    value = False
                elif own and not t.startswith("-"):
                    own = False
                elif own:
                    value = _env_takes_next(t) or (at is not None and at[0] == "next")
                if at is None:
                    continue
                kind, string = at
                if kind == "next" and j + 1 < len(rest):
                    texts += _string_at(rest, j + 1)
                    after = rest[j + 1 :]
                elif kind == "here":
                    texts.append(string)
                    after = [string, *rest[j + 1 :]]
                else:
                    continue
                if env_words:
                    texts += _env_words(word, rest[:j], after)
    return texts


# `env`'s options other than `-S` that take a value, in GNU coreutils and
# BSD/macOS: the rest of the cluster, or the next word where none is left.
ENV_VALUED = frozenset("uCPLa")
ENV_VALUED_LONG = frozenset({"--unset", "--chdir", "--argv0"})


def _env_takes_next(t):
    """True where T is one of `env`'s options whose value is the next word."""
    if t.startswith("--"):
        return t in ENV_VALUED_LONG
    middle = t[1:-1]
    return (
        len(t) > 1
        and t[-1] in ENV_VALUED
        and all(c.isalnum() and c not in ENV_VALUED for c in middle)
    )


def _env_split_at(t, own):
    """Where T spells `env`'s split string (#716), or None.

    ("next", None) where the string is the next word, ("here", s) where T
    carries it. `-S`, `-S<s>` and `--split-string[=<s>]` anywhere, as the
    base read them. Among env's own options (OWN) also a cluster ending in it
    (`-iS`, `-vS<s>`, which macOS `env` and GNU's getopt both accept) and
    every prefix of `--split-string` GNU's getopt takes, from `--s`: no other
    long option of GNU `env` starts with `s`.
    """
    if t in ("-S", "--split-string"):
        return ("next", None)
    if t.startswith("--split-string="):
        return ("here", t.split("=", 1)[1])
    if t.startswith("-S") and len(t) > 2:
        return ("here", t[2:])
    if not own:
        return None
    if t.startswith("--"):
        name, eq, value = t.partition("=")
        if name.startswith("--s") and "--split-string".startswith(name):
            return ("here", value) if eq else ("next", None)
        return None
    if not t.startswith("-") or len(t) < 2:
        return None
    for i, ch in enumerate(t[1:], 1):
        if ch == "S":
            string = t[i + 1 :]
            return ("here", string) if string else ("next", None)
        if ch in ENV_VALUED or not ch.isalnum():
            return None
    return None
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, HANDED
    # Round 1 of 1790993140: a cluster ending in `S`, which macOS `env`
    # accepts, and GNU's abbreviation of `--split-string`. Each found nothing
    # at `07a3dc7f`.
    "env -iS, a cluster": f"env -iS '{C}'",
    "env -vS, a cluster carrying env's own words": f"env -vS '-i {C}'",
    "env -iS glued": f"env -iS'{C}'",
    "env --split, abbreviated": f"env --split '-i {C}'",
    "env --split=, abbreviated": f"env --split='-i {C}'",
    "env -iS behind an option's value": f"env -u FOO -iS '{C}'",

# ... and in CONTROLS:
    # A cluster ending in `S` after the program is the program's (`ls -lS`).
    "a program's own cluster ending in S": "env ls -lS \"$DIR\"",
```

The commit gate's #670 clause in `docs/commit-review-gate-spec.md` needs no
words for this: "`env -S`" names the option, not one spelling.
`overview.md`'s divergence table should gain a row for the class.

### 🟡 3 — subtract per view and by the loop's verdicts

```python
# hooks/worktree-guard.py
def wider_only_kinds(command: str, cwd: str, judged=None) -> set:
    # (docstring as now; replace its last sentence of the first paragraph with:
    # "A kind the frozen loop judged keeps its slot and its verdict, and a
    # view the frozen parser reads as the same kind is not hidden from it,
    # so neither is reported." JUDGED defaults to the kinds the frozen
    # segments' words hold, which is what the unit cases ask.)
    if wide is None:
        return set()
    if judged is None:
        judged = {
            switch_kind(parse_git(tokens))
            for tokens, _wheres in walk_command(command, cwd)
        }
    text = wide.drop_heredoc_bodies(wide.drop_comments(command))
    segments, _clean = wide.split_segments(text)
    views = [*segments, *wide.merged_segments(text)]
    wider = set()
    for tokens in [*views, *filter(None, map(wide.unglued, views))]:
        kind = switch_kind(wide.parse_git(tokens))
        # A view the frozen reader reads as the same kind is not hidden from
        # it: `git checkout README.md` is a restore to `classify`, and must
        # not silence a switch written behind a redirection after it.
        if kind and switch_kind(parse_git(tokens)) != kind:
            wider.add(kind)
    return wider - set(judged)


# in main, quiet():
    def quiet():
        judged = {"switch"} if switch_reason is not None else set()
        if creation_at is not None:
            judged.add("creation")
        hidden = wider_only_kinds(command, cwd, judged)
        ask_what_only_the_wider_reading_finds(hidden, cwd, session_id, transcript_path)
        sys.exit(0)
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py
def test_a_restore_before_a_hidden_switch_does_not_silence_the_question(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of 1790993140. `classify` reads `git checkout README.md` as a
    restore, so the frozen loop judged no switch, and the switch behind the
    redirection is still put to the person. Silent at `07a3dc7f`, where the
    restore's words alone took the switch kind out."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command = f"git checkout README.md && cd w && 2>/dev/null {SWITCH}"
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (decision, reason)
    assert "switches a branch" in reason, reason
    assert top is None, top
```

The comment above `quiet` ("What the loop found, `wider_only_kinds` already
leaves out …") becomes "`quiet` passes what the loop judged". The
divergence row in `overview.md` about the discards should say that the
subtraction now uses the loop's verdicts.

### ⬜ 4 — say whose consent a hidden creation reads

In `docs/worktree-guard-spec.md` §*Which tree*, after "A creation reads
consent first and stays silent under it, as at the base.":

```markdown
The consent read is the session clone's: the guard cannot place a creation
only the wider reading finds, so a hidden creation into another clone is
silent under this clone's consent, and one reached through `git -C` from a
directory in no repository is asked although its clone has consent.
```

### ⬜ 5 — catch an exiting module body too

```python
# hooks/worktree-guard.py
try:
    import cmdline as wide
except (Exception, SystemExit):
    wide = None
```

### ⬜ 6 — W10, corrected rather than re-read

```markdown
**Corrected 2026-10-03** by work item 1790993140 (#678): a third command names
no tree. The question about a switch or creation only the commit gate's
reading finds tells the person to re-issue it as `git switch …` or
`git worktree add …`, with `git -C <dir>` as a placeholder, because the guard
could not place it.
```

### ⬜ 7 — M1's correction, narrowed

```markdown
**Corrected 2026-10-03** by work item 1790993140 (#678): *never through
`hooks/cmdline.py`* no longer holds for the guard. It imports that module as
`wide`, guarded, and at an exit where it was about to say nothing it reads that
module's segments with that module's `parse_git` (`wider_only_kinds`) and asks
about a switch or creation only that reading finds. The tree it judges, each
segment's directories, every verdict the frozen reading earns and the clone
consent is filed under are still `86256492`'s, and the consent writer still
imports only the frozen copy.
```

Needs a fix: yes — 🟡 1 (env's own words stop no-commit `env -S` commands), 🟡 2 (the `env -S` class misses clusters and abbreviations), 🟡 3 (a restore before a hidden switch silences candidate C)
Loses a record or crashes: no

The broad gate has not come due: three findings need a fix first.

## Proof block

Files opened in this round:

- `hooks/cmdline.py`: `reparsed_texts`, `_env_words`, `command_strings`,
  `_without_redirections`, `_string_at`, `_git_options`, `parse_git`, and the
  `names_an_unknown_command` views.
- `hooks/worktree-guard.py`: the import block, `walk_command`, `switch_kind`,
  `wider_only_kinds`, `ask_what_only_the_wider_reading_finds`, `classify`,
  `main`. Also `c7f84438`'s copy of the file.
- `hooks/commit-review-gate.py`: the views block of `_reads_a_commit`.
- `hooks/dispatch.py`: its exception catches.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`,
  `tests/test_guard_resolves_the_tree_it_judges.py`,
  `tests/test_a_gate_that_fails_says_so.py` (the broken-module and S7 cases),
  `tests/test_the_commit_gate_decides_at_the_commit.py` (diff).
- `docs/commit-review-gate-spec.md` (diff and markers),
  `docs/worktree-guard-spec.md` (diff).
- `seal/config.md`; `seal/releases/0.9.1.md`, `0.15.5.md`, `0.15.6.md`,
  `0.16.0.md` and `0.17.0.md` (every changed row); the new fragment under
  `seal/ledger/`.
- The work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `changelog.md`, `routing.md`, and `phases/phase-1.md` to `phase-5.md`.
