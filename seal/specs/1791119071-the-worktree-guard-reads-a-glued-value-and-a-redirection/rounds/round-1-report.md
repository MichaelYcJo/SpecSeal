# Round 1 report — the worktree guard reads a glued value and a redirection

| Field | Value |
|---|---|
| Work item | 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection |
| Round | 1 |
| Target SHA | a7ab2a4e |
| Base | `release/v0.18.2` at 94d7b2e0 |
| Pull request | #788 (draft), issues #764 and #738 |
| Ran by | specseal:warden on claude-opus-5-5 |

Worked in a `git clone --no-local` of the worktree, checked out at a7ab2a4e,
under this round's scratch directory. Nothing was written in the worktree
but this file. git 2.54.0 (Apple Git-157), bash 3.2.57.

## Summary

One blocking finding and one note. The reader reads every spelling the frame
listed, but the frame's Axis 2 has no `--` placement, and one placement
switches: `git checkout <name> --` with nothing after the `--`. git reads that
as a switch to `<name>`; the `--` only says the name is no file. Both
`classify` and `switch_kind` read any `--` as a restore, so they say nothing.
That silence is the base's too, but the build adds to it. The base read
`git checkout feature/x -->/dev/null` as a switch by accident, because
`-->/dev/null` was not `--`. The build cuts the redirection off, finds a bare
`--` and goes silent. So the property `spec.md` A6 names, nothing that
switches goes quiet, does not hold outside the generator. The shape was
simply not in the generator.

Everything else the prompt asked about holds where I checked it: the option
table, the restore twins, the frozen files, the C-position property, the
`--no-` removal and the survivor cases.

## What the account claimed, and what I found

| Claim (where) | Found |
|---|---|
| `hooks/cmdline_base.py`, its S11 pin and `hooks/cmdline.py` are unchanged (prompt, `spec.md` Out) | **Executed**: `git diff 94d7b2e0 a7ab2a4e` over `hooks/cmdline_base.py`, `hooks/cmdline.py`, `hooks/worktree_consent.py` and `tests/test_the_frozen_reading_never_grows.py` is empty |
| The table holds every option git 2.54.0 lists, and git hides none (`hooks/worktree-guard.py:390` comment) | **Executed**: `git checkout --git-completion-helper-all` and `git switch --git-completion-helper-all` name 22 and 15 long options. These are the table's 22 and 15 exactly, with no hidden option. Every short letter `-h` lists is in the table. Each value-taking flag matches git's `<…>` marker |
| The local operator list is `hooks/cmdline.py`'s (`hooks/worktree-guard.py:300`) | **Executed**: the two compiled patterns are byte-equal |
| 230 newly asked no-switch shapes, every one at a C position (`phases/phase-2.md`) | **Executed, on a different set**: over the module's own `TWINS` and `RESTORES` through `_placed` (12,092 shapes), base against build, 268 are newly asked and 0 of them stand after the subcommand with no `&` or `\|` in the operator. The 230 figure is over the smith's deleted twin set, which I did not rebuild, so it is carried and not re-derived |
| A6: of the generated switching shapes none went quiet, and the 1,130 newly silent shapes are ones git switches nothing on (`phases/phase-2.md`, ledger D1) | True over the generator as built. **False for the class**: 24 shapes of `checkout feature/x --` and 24 of `checkout - --` that the base asked are silent in the build, and git switches on them (🔴 1) |
| A negation (`--no-…`) reads exactly as a word git refuses, so the rule was dropped (`overview.md`, `_long_option` docstring) | **Confirmed.** Executed: no long name of either subcommand begins with `no-` in git's own list. Read: a negation gets the same answer, no value taken and nothing created, as an unknown or ambiguous word. Executed: `git switch -c y --no-create feature/x` switches to `feature/x`. The build reads that as `create+switch`, and `main` treats it exactly like `switch` (`hooks/worktree-guard.py`, the `reason` checks name only `worktree-add`), so the missing negation changes no answer |
| Four survivors closed with cases (`phases/phase-2.md`) | **Read**: `test_an_ambiguous_long_prefix_takes_nothing` (a first-match mutant returns `(True, True)`), `SWITCHES`' `-t feature/x` rows (a `-t`-as-`VALUE` mutant eats the name), `TWINS`' `checkout feature/x -- README.md` (dropping the `--` check reads `feature/x` as a ref), and `test_the_reduction_takes_out_every_redirection_the_reader_names` (`<>`). Each case asserts the value its mutant changes. I did not re-run `bin/mutation-check` |
| Known limits: 25,741 of the 27,351 pairs, no quoted `<`/`>` in any pair, 81 `&`-led pairs with C firing on none (`docs/worktree-guard-spec.md:740`) | **Read and carried**: the counts agree with `phases/phase-1.md` and `phases/phase-3.md`. The corpus probe was deleted and the transcripts are the smith's measurement, so I did not re-derive them. The `git checkout feature/x <&1 -- README.md` sentence holds by reading. The frozen segment is `git checkout feature/x <`, and the reader leaves the name `feature/x` with no `--` |

## Stage 1 — spec compliance

**(1) Words as git's option parser receives them.** I ran 38 spellings under
bash in scratch repositories (executed, table under *Executed probes*). The
build matches git on every one of these:

- stuck, aggregated and abbreviated creating options;
- `--c merge` on `checkout`, a unique prefix of `--conflict`;
- `-lb y`;
- `--orphan y --`;
- `--end-of-options` before a name, before `-` and before `--`;
- `-tdirect` and `--track`, whose value can only be stuck;
- `--recurse-submodules` with a separate name;
- `@{-1}`;
- `-` and a value-taking option behind a redirection.

The base misses several of them: `--c merge feature/x`, `-lb y`,
`--orphan y --` and `--conflict 2>/dev/null merge feature/x`.

In the other direction, git refuses `-h`, `-2`, `--quiet=1` and the ambiguous
`--c` and `--no-c`, and the build asks them. That is the loud direction on
commands that do nothing.

One placement of `--` is missed, and that is 🔴 1. I found no option value
still read as a name, beyond the `-U` the account already names.

**(2) The direction.** `classify` keeps a restore twin silent wherever its
redirection stands after the subcommand with no `&` or `|`:
`test_a_restore_wherever_its_redirection_stands_stays_silent` reads these
through `main()`, and the 12,092-shape sweep found none asked there
(executed). The newly asked twins are C's tree-blind rule, which §*Which
tree* already states.

**(3) Frozen files.** They are unchanged (executed, above).

**(4) Known limits.** The three bullets and the static-table sentence are
accurate as far as I read. The counts are carried, not re-derived. 🔴 1's fix
adds one sentence to the `&`-cut bullet.

**(5) The `--no-` removal and the four survivors.** Confirmed above.

## Stage 2 — quality

The reduction duplicates `hooks/cmdline.py`'s operator list and width rule on
purpose. The duplicate is bound by A8 and by the pattern equality checked
above, so it is no reuse finding. `_bare_words` is now a one-line delegate,
and its docstring says why. ⬜ 2 is the one quality note: A7 binds the table
in one direction only.

## 🔴 1 — `git checkout <name> --` switches, and the guard says nothing; the build adds 48 shapes the base asked

`hooks/worktree-guard.py:1022` (`classify`), `hooks/worktree-guard.py:561`
(`switch_kind`), `docs/worktree-guard-spec.md:644`.

**What is wrong.** `read_switch_words` returns `after` as `[]` when a `--`
stands last. Both readers then test `after is not None` and return no switch.
git's `checkout` reads `<name> --` with nothing after the `--` as "the name
is a commit, not a file" and switches to it.

Executed in a scratch repository with branches `main` and `feature/x`. Each
of the following switched HEAD to `feature/x` with exit 0, while the build
and the base both read no kind:

- `git checkout feature/x --`
- `git checkout feature/x -- 2>/dev/null`
- `git checkout - --`
- `git checkout -f feature/x --`
- `git checkout --conflict=merge feature/x --`
- `git checkout --end-of-options feature/x --`

`git checkout feature/x -->/dev/null` also switched. The base asked it and
the build is silent.

**Why it matters.** The guard exists to stop a switch over a dirty tree or
one another session is working in. §*Unknowns resolve conservatively* says a
wrong allow can break another session's tree. The `--` form is not exotic.
It is git's own documented way to name a branch that shares a name with a
file.

The regression half shows up in the generated sweep over `_placed` (executed).
Of 492 placements of `checkout feature/x --`, the base leaves 442 silent and
the build 460. Of 492 placements of `checkout - --`, the base leaves 436
silent and the build 460. The 24 newly silent placements of each are every
operator glued to the `--` (`-->/dev/null`, `--<<<word`, `--<>…`, `-->&1`,
…). The build cuts the operator off correctly, so the defect is not in the
reduction. The reduction now exposes the bare `--` that the readers misjudge.

**Why the generator missed it.** `spec.md`'s Axis 2 enumerates option
spellings, and `SWITCHES` and `TWINS` carry `--` only before a name or before
a pathspec. A trailing `--` is not a point of the product, so A4 and A6 held
over a class that did not contain it (§12).

**The fix.** A `--` with a pathspec after it is a restore. A `--` with
nothing after it leaves the name before it as the switch target, and skips
the path test, since git does not read that name as a file. The fix is
fenced below. Executed in the clone:

- with the fix, the guard module passes (246 passed, including the four
  proposed cases);
- against a7ab2a4e as committed, the four proposed cases fail, which is
  §15's red;
- the sweep with the fix leaves 0 of the 492 placements of each trailing-`--`
  verb silent;
- newly asked twins rise from 268 to 294, all at C positions.

The 26 extra twins are `checkout feature/x -- <&1 README.md`-style. The frozen
splitter cuts at the `&`, so the frozen segment holds a bare trailing `--`.
That is the same `&`-cut limit §*Known limits* already names one word
earlier, so the bullet gains a sentence.

The policy sentence states the rule `switch_kind` reads, so it changes in the
same commit (§14). Its pin and the `Corrected · G1` claim in this item's
ledger fragment carry the same words.

## ⬜ 2 — A7 binds the option table in one direction only

`tests/test_guard_resolves_the_tree_it_judges.py:1685`.

`test_the_option_table_binds_the_installed_git` checks that every option git
lists with a mandatory value is `VALUE` in the table. It never checks the
reverse: that a `VALUE` entry is one git lists with a mandatory value.

The reverse is the silent direction. Suppose a later git turns
`--conflict <style>` into `--conflict[=<style>]`. The table would still take
the next word, `checkout --conflict feature/x` would read no name, and the
case would stay green.

Today every `VALUE` entry matches git 2.54.0 (executed, above), so nothing
ships wrong. The test could also collect the `VALUE` entries it saw git list
and assert the table holds no others.

## Regression tests to plant

- `tests/test_guard_resolves_the_tree_it_judges.py` `KINDS`: `"checkout a name and a bare --": (["git", "checkout", "x", "--"], "switch")`.
- `tests/test_guard_resolves_the_tree_it_judges.py` `SWITCHES`: `"checkout feature/x --"` and `"checkout - --"`. This puts every `_placed` position of the trailing `--` into `test_no_constructed_switch_is_silent` and `test_classify_reads_the_name_past_an_options_value`.
- Both were seen red at a7ab2a4e and green with the fix (executed in the clone, above).

## Facts for the evidence ledger

- git 2.54.0: `git checkout <name> --` with nothing after the `--` switches to `<name>`. With a pathspec after it, it restores. Executed.
- git 2.54.0: `--git-completion-helper-all` names exactly `SWITCH_OPTIONS`' long names for both subcommands, with no hidden option. Executed.
- D1's "over the generated shapes nothing git switches on went quiet" is true of the generator and stops being the whole class once 🔴 1 is fixed. When the fix lands, D1 and `Corrected · G1` take the new sentence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `git checkout <name> --` with nothing after the `--` switches, and `classify` and `switch_kind` read any `--` as a restore; the build newly silences 48 generated shapes the base asked (`-->/dev/null` and its kin) | `hooks/worktree-guard.py:1022`, `hooks/worktree-guard.py:561`, `docs/worktree-guard-spec.md:644` | open | Executed under bash with git 2.54.0: six trailing-`--` spellings switch while both readers read no kind; the `_placed` sweep counts 460 of 492 silent at the build against 442 and 436 at the base; the fix below turns the four proposed cases from red at a7ab2a4e to green |
| ⬜ 2 | A7 binds the table one way only: a `VALUE` entry git no longer lists as mandatory stays green and eats a name | `tests/test_guard_resolves_the_tree_it_judges.py:1685` | open | Read; every `VALUE` entry matches git 2.54.0 today (executed), so nothing ships wrong |
| 🟢 | `hooks/cmdline_base.py`, S11 and `hooks/cmdline.py` are unchanged | `hooks/cmdline_base.py` | confirmed | Executed: the diff over the four frozen-side files is empty |
| 🟢 | The option table is git 2.54.0's, hidden options included | `hooks/worktree-guard.py:394` | confirmed | Executed: `--git-completion-helper-all` lists exactly the 22 and 15 long names, and `-h` lists the short letters and value markers |
| 🟢 | Every newly asked no-switch shape stands at a C position | `hooks/worktree-guard.py:568` | confirmed | Executed over the module's 12,092 twin placements: 268 newly asked, none after the subcommand without `&` or a pipe; the 230 figure is the smith's set and is carried |
| 🟢 | A restore twin with a redirection after the subcommand stays silent in `classify` | `hooks/worktree-guard.py:1018` | confirmed | Executed: the sweep and the three `main()` restore cases |
| 🟢 | Dropping the `--no-` rule changes no answer | `hooks/worktree-guard.py:466` | confirmed | Executed: no long name begins with `no-`; `switch -c y --no-create feature/x` switches and is read as a switch |
| 🟢 | The four survivors each have a case that pins the mutated unit | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | Read: each case asserts the value its mutant changes; `bin/mutation-check` not re-run |

## Executed probes

| What was run | Result |
|---|---|
| 38 `git checkout` and `git switch` commands under bash 3.2.57 with git 2.54.0, one fresh scratch repository each (branches `main` and `feature/x`, a committed `README.md`, a previous branch), HEAD compared before and after; the build's and the base's `classify` per frozen segment plus `wider_only_kinds` on the same command | Six trailing-`--` spellings switch while both readers read nothing; `checkout feature/x -->/dev/null` switches, the base asks and the build does not; every other switching spelling is asked by the build; `-h`, `-2`, `--quiet=1`, `--c` and `--no-c` are refused by git and asked by the build |
| `git checkout --git-completion-helper-all`, `git switch --git-completion-helper-all`, `git checkout -h`, `git switch -h` against `SWITCH_OPTIONS` | 22 and 15 long names, the table's exactly; no hidden option; value markers match |
| Pattern equality of the guard's `_REDIRECTION` and `hooks/cmdline.py`'s | equal |
| `git diff 94d7b2e0 a7ab2a4e` over `hooks/cmdline_base.py`, `hooks/cmdline.py`, `hooks/worktree_consent.py`, `tests/test_the_frozen_reading_never_grows.py` | empty |
| A deleted probe module through `bin/test`: the module's `TWINS` and `RESTORES` through `_placed`, base guard against build guard, `is_ref` a lookup over the repository's refs; then the trailing-`--` verbs through `_placed` | 12,092 twin placements, 268 newly asked, 0 outside C positions; `checkout feature/x --` 442 silent at base, 460 at build; `checkout - --` 436 and 460; `checkout --conflict=merge feature/x --` 546 and 564 |
| The same, with 🔴 1's fix applied in the clone | trailing-`--` verbs 0 silent of 492, 492 and 596; newly asked twins 294, 0 outside C positions |
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` in the clone with 🔴 1's fix and its cases | 246 passed |
| The same module with the cases and a7ab2a4e's guard | 4 failed (the KINDS row, two `classify` rows, the generated A4 case), 242 passed |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run, at any SHA; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🔴 1

`hooks/worktree-guard.py`, in `classify`'s `checkout` arm:

```python
    if sub == "checkout":
        creating, names, after = read_switch_words(sub, args)
        if creating:
            return "create+switch"
        if after:
            return None  # explicit path restore: a pathspec follows `--`
        if "-" in names:
            return "switch"  # previous branch
        if not names:
            return None
        first = names[0]
        # `git checkout <name> --`, nothing after the `--`, names a commit and
        # switches to it: the `--` only says the name is no file.
        if after is None and (
            first == "."
            or os.path.exists(os.path.join(cwd or ".", first))
            or os.path.exists(first)
        ):
            return None  # restoring a file/dir, not switching branch
```

`hooks/worktree-guard.py`, in `switch_kind`, the code and the docstring
clause:

```python
    if creates:
        return "switch"
    if after:
        return None
    if any(n != "." for n in names):
        return "switch"
    return None
```

```text
    branch, in `classify`'s order: one carrying a creating option counts,
    with or without a name; then one with a word after its `--` does not,
    whatever stands before it; then one naming `-` or a word other than `.`
    does, a `--` with nothing after it included.
```

`docs/worktree-guard-spec.md`, the #678 sentence. Change the same words in
`test_the_guard_policy_says_a_hidden_file_checkout_is_asked`'s pin and in
`Corrected · G1`'s claim in this item's ledger fragment:

```text
Each side is read by its words alone, as git is handed them: a `switch`
naming a word or `-` or carrying a creating option, a `checkout` carrying a
creating option (`-b`, `-B` or `--orphan`, in any spelling git's option
parser accepts), a `checkout` that names `-` or a word other than `.` and
has no `--` among its words or nothing after its `--`, or a `worktree add`;
an option's value is not a name, and a redirection is no word.
```

`docs/worktree-guard-spec.md` §*Known limits*, the `&`-cut bullet, after its
last sentence:

```text
A cut after a `--` leaves the frozen reading a `--` with nothing after it, so
`git checkout feature/x -- <&1 README.md`, a restore, is judged a switch to
`feature/x` too.
```

`tests/test_guard_resolves_the_tree_it_judges.py`:

```python
    "checkout a name before --": (["git", "checkout", "x", "--", "f"], None),
    "checkout a name and a bare --": (["git", "checkout", "x", "--"], "switch"),
```

```python
    "switch -- feature/x",
    # A `--` with nothing after it only says the name before it is no file.
    "checkout feature/x --",
    "checkout - --",
```

Needs a fix: yes — 🔴 1, `git checkout <name> --` read as a restore by `classify` and `switch_kind`, and 48 placements the base asked now silent
Loses a record or crashes: no

## Proof block

Files opened (all at a7ab2a4e in the clone unless noted):

- `hooks/worktree-guard.py` (the diff; `handed_words` through `switch_kind`, `wider_only_kinds`, `_bare_words`, `is_ref`, `classify`, the `reason` checks in `main`)
- `hooks/cmdline.py` (`_REDIRECTION`, `redirection_width`)
- `docs/worktree-guard-spec.md` (the diff)
- `tests/test_guard_resolves_the_tree_it_judges.py` (the diff; `_redirections`, `RESTORES`, `ASKABLE`, `KINDS`, `test_switch_kind_reads_the_words_alone`)
- `tests/conftest.py` (`load_hook_module`, `repo`)
- `CONTRIBUTING.md` §*Running the checks*
- this item's `spec.md`, `questions.md`, `overview.md`, `survivors.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`, and `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md`
- the base guard at 94d7b2e0, extracted with `git archive` for the comparison probes

No earlier round exists, so nothing was inherited. The probes, their scratch
repositories, the base extract and the clone were deleted before handover.
