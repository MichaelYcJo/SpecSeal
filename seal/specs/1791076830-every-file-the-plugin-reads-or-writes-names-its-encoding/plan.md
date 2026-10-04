# Implementation Plan: every file the plugin reads or writes names its encoding (#741)

<!-- seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

One new test module holds every `open`, `read_text`, `write_text`,
text-mode subprocess call and their relatives (`spec.md` K1, K2) to a named
encoding across every tracked `.py`, and holds every hook entry point to
opening `__main__` with `console.to_utf8()` (K3). Every site it names is fixed
with `encoding="utf-8"`: 29 product sites, 302 test sites by the framer's
census (K4). The three git hooks gain the console call. `CONTRIBUTING.md`
gains one House rules bullet. Nothing a gate decides changes.

## Technical context

- **The precedent to copy.**
  `tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED`,
  `#shipped_python`, `#classifications_of_nothing`, and the three cases after
  it (`#test_the_enumeration_survives_a_tracked_file_the_tree_deleted`,
  `#test_a_skipped_file_does_not_read_as_a_lost_classification`,
  `#test_a_present_classified_file_is_still_judged`). The helpers are in
  `tests/conftest.py`: `#git_listing`, `#on_disk`, `#decline_if_shrunken`,
  `#shrunken_corpus`, `#build_tracked_tree`. Reuse them rather than writing a
  second enumeration.
- **The console half.** `hooks/console.py#to_utf8`; the 18 entry points that
  already call it all spell `console.to_utf8()` then `main()` (read at
  `4d2afd1e`, every `__main__` block under `hooks/`). `hooks/git/*.py` insert
  `HOOKS` into `sys.path` already, so `import console` resolves there the way
  `import commitgate` does.
- **The pre-commit refusal.** `hooks/commitgate.py#pre_commit` writes to the
  stream it is handed (`sys.stderr`), and `hooks/gate.py:182` puts U+2026 in
  the waiver it names. The existing git-hook cases live in
  `tests/test_the_commit_gate_decides_at_the_commit.py` and are the fixture
  source for S8.
- **The Windows reproduction.** `tests/test_the_ledger_cases_hold_under_a_latin_1_locale.py`
  is how a cp1252 default is reproduced on a POSIX machine (`LC_ALL=en_US.ISO8859-1`,
  `PYTHONUTF8=0`, skip where the machine has no such locale). It is a
  reference for how to see a test-site fix red, not a pattern to extend: the
  repository case S1 is the proof, and it needs no locale.
- **What breaks in six months.** A new I/O spelling outside K1 (a library
  that opens files itself in text mode, a helper forwarding `**kwargs` to
  `open`) is not seen. K2 catches the splat on a K1 call. A new library is
  not seen, and the module docstring says the class is K1's table so the next
  person widens the table rather than the allowlist.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A1 ruff `PLW1514` alone | Preview-only. By the ticket's account it saw none of the 33 unencoded calls in #736's failing module, because it does not see `Path.read_text` / `write_text` on a variable, which is 269 of the census's 335 sites. The Windows leg stays the only detector | Rejected (M2 holds the ticket's claim) |
| A2 `PLW1514` beside the AST check | Two instruments with different classes. Each disagreement is a suppression comment or an allowlist row in one of them, and neither tells the reader which is right | Rejected |
| A3 a `bin/` command | `bin/` is the product surface users run on their repositories. This judges only the plugin's source, so it would ship a command with no user and a second runner to keep in step | Rejected (D1) |
| A4 a test module, AST, with a classification table | A K1 shape nobody listed slips by. Mitigated by K1 being the module's documented table, by K2 catching what cannot be proven, and by the liveness half keeping the table honest | **Chosen** (D1) |
| A5 a regex over source text | Misses a call whose `encoding=` sits on a later line, and a reformat moves the blind spot. The precedent module's own comment says this is what an AST walk is for | Rejected |
| A6 `PYTHONUTF8=1` in CI, `hooks.json` or `conftest.py` | The Windows leg goes green with every unnamed call still in place. A user's interpreter does not inherit it | Rejected |
| A7 a behavioural case per hook entry point | Each entry point returns silently on a stdin it cannot decode, and silently when nothing applies, so the case cannot be seen red without building each hook's own triggering state (spec D5) | Rejected for the AST order assertion plus the existing behavioural cases |
| A8 classify the 9 empty-marker `open(path, "w").close()` sites rather than fix them | Nine rows of grounds where nine keyword arguments would do, and a table that starts full | Rejected (D3) |
| A9 one phase that fixes product and tests together | 331 edits across 64 files reach the reviewer as one commit. The product sites, where D7's failure direction matters, would be hidden among 302 mechanical test edits | Rejected for the cut below |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The module: the walker (K1, K2, alias resolution) with its synthetic cases (S2–S4), the classification table and its liveness half (S5, S6), and the entry-point half (S7). The repository case runs over every tracked `.py` **except `tests/`** in this phase. Every product site fixed (`hooks/` 15, `.github/scripts/` 14), with D7 applied per hook read and S9's `read_mark` case. `console.to_utf8()` in the three `hooks/git/` entry points, and S8 if M4 shows it red. The House rules bullet (S10) | Each synthetic case seen red by removing its rule; the repository case seen red against the unfixed product tree, then green; S7 seen red naming the three git hooks, then green; `bin/test <new module> -q`, `bin/test tests/test_console_is_not_utf8.py -q`, the git-hook test module and every test module of an edited product file, narrowly; `uvx ruff check` and `uvx ruff format --check` on the touched files | 01f192cf |
| 2 | The repository case widened to `tests/`, and every test site fixed (302 by the census). `Image.open` classified in `ALLOWED`, plus whatever W2 finds | The widened case seen red naming the test sites, then green; each edited test module run narrowly, so a fixture whose bytes changed is caught by its own cases | dac51971 |
| 3 | The records: the changelog fragment, the ledger fragment's new rows, and a `Re-read ·` row for each released row the phase 1 and 2 edits drifted (M3) | `bin/evidence-check .` names no drift left unanswered and no broken anchor; `bin/test tests/test_docs_line_wrap.py -q` and the other text-hygiene modules over the touched records, narrowly | |

**Phase 2's edits may be applied by a script** rather than 302 `Edit` calls.
`skills/agent-contract/SKILL.md` §9 allows it where the edit would otherwise
be unable to fail, and asks that every substitution assert it matched. Here
there is a stronger proof than that: the walker itself, re-run, must name
zero sites, and each edited module must still pass. Write the script to the
scratchpad with `Write` and run it by path. A heredoc on the Bash command line
is what the commit gate reads as shell. Keep `ruff format` on the touched
files, because a call that grows `encoding="utf-8"` may cross 88 columns.

**The suite as a whole is not run by any phase.** It is the sealer's, once,
after the review rounds settle (`skills/agent-contract/SKILL.md` §2). Each
phase hands over with it labelled `unverified`, answerer the sealer.

## What a sibling branch does when it merges this in

This item lands first in 0.18.1. #739 (the commit gate's here-document
reading), #747 (the broad gate's base re-run) and #647 (the cross-repository
work item, including `--reverify`) each meet the new module when they merge
`release/v0.18.1` into their branch.

1. **Merge, never rebase.** `templates/sdd-plan.md`'s caveat under the Phases
   table says why: a rebase orphans every SHA the branch's `plan.md` Status
   cells and round records name, and quietly, because the orphan still
   resolves in the worktree that wrote it.
2. **Run the module narrowly**: `bin/test tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py -q`.
   It names every unnamed call the branch added, as `path:line (kind, unit)`.
3. **Name the encoding at each site it names**: `encoding="utf-8"`. In
   `hooks/`, apply D7: a read either sits in a handler that catches
   `ValueError`, or adds `errors="replace"`, because a raise inside a hook is
   an allow.
4. **Classify only what a fix cannot serve**, in `ALLOWED`, keyed by unit,
   with grounds. A row added to turn the case green is the move
   `CONTRIBUTING.md` already refuses for the identifier allowlist.
5. **A new hook entry point** under `hooks/` opens its `__main__` with
   `console.to_utf8()`. The entry-point half names it otherwise.
6. **Where the sibling's own edits land on a line this work also edited**
   (possible for #739, since phase 1 touches `hooks/commit-review-gate.py`
   twice and `hooks/commitgate.py` once; this work edits nothing under
   `skills/*/scripts/`, so #647's and #747's product files should meet no such
   line, but phase 2 edits 45 test modules and any sibling may share one),
   resolve the conflict by keeping both: the sibling's change plus the
   `encoding=` argument. Then re-run step 2, since the merge can carry an
   unnamed call back in. Its own `Re-read ·` rows for a released row
   follow `docs/the-evidence-ledger.md` §*A released row is read again in the
   branch's fragment* as before.

A sibling that skips step 2 finds out at the sealer's broad run or on the
Windows leg, which is the late discovery this item exists to end.

## Operational impact

None for a user. No new dependency, environment variable or command. The
hooks write and read the same bytes on a UTF-8 machine. On a non-UTF-8
Windows machine three things change: a hook's marker and lease files are
written as UTF-8, its JSON reads decode as UTF-8, and the three git hooks
write UTF-8 to stderr, where the ellipsis in a refusal used to go out in the
console's code page. For a contributor, a branch that writes an unnamed call
now fails on every CI leg instead of the Windows one, and fails locally.
