# Feature Specification: every file the plugin reads or writes names its encoding (#741)

<!-- seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md
     WHAT this work delivers and how we will know. The policy documents in
     docs/ outrank this file; it cites them rather than restating them.
     Record language: `seal/config.md` has no `Record language` row, so English. -->

**Why this exists.** A file opened, read or written without `encoding=` uses
the locale's encoding. That is UTF-8 on macOS and on the ubuntu runner, and
cp1252 on `windows-latest`, so the class is invisible everywhere except the one
CI leg nobody runs locally. #736 met it after review: a ledger row's ` · `
went out as byte 0xB7 and came back as U+FFFD, 26 cases failed on Windows only,
and two post-review commits (`c3f8215a`, `9d43317a`) repaired one branch's
instances. Nothing holds the next branch to it. This work adds the check that
does, fixes every instance the check names, and closes the one remaining gap
in the console half (the three git hooks).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | The check runs in the suite, unattended, on all three CI legs. Nothing in this work asks a person anything. |
| `skills/agent-contract/SKILL.md` §12 *A defect belongs to a class — enumerate the class* | The class is enumerated by construction, an AST walk over every tracked `.py` (K1, K2), never by the instances #736 happened to meet. |
| `skills/agent-contract/SKILL.md` §15 *A new case is not planted until it has been seen red* | Every case of the new module is shown failing before it is committed (S1–S9 say how for each). The issue asks the same: *every case seen red first*. |
| `skills/agent-contract/SKILL.md` §7 *A probe … deleted* | The every-enumeration-rots point is why the corpus is `git ls-files '*.py'` rather than the issue's list of four roots (D2). |
| `CONTRIBUTING.md` §*House rules*, bullet *No real identifiers* | The precedent for a repository-wide hygiene rule: one sentence in House rules naming the test that enforces it, and an allowlist extended deliberately. D8 adds the encoding rule in that shape. |
| `CONTRIBUTING.md` §*House rules*, bullet *Hooks stay local and quiet* | *A gate that crashes should let the work through.* A read converted to strict UTF-8 inside a hook must not newly raise where the old read did not (D7), because a raise inside `dispatch.py` is an allow. |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The three git hooks gain `console.to_utf8()`. That changes a gate's output under a hostile console, so the pull request states the failure direction (D6) and has a case seen red (S8). |
| `CONTRIBUTING.md` §*Running the checks* | The suite is the only place a hygiene check on the plugin's own code runs, and CI runs it on ubuntu, macOS and Windows. This is the delivery D1 chooses. |
| `hooks/console.py` module docstring | *The call sites are each entry point's `__main__`, not this module's import*, and *each carries the call rather than relying on `dispatch.py`*. The entry-point half (K3) holds exactly that sentence for `hooks/`. |
| `tests/test_console_is_not_utf8.py` module docstring | *Any source-text assertion is satisfiable by dead code.* D5 says why an AST order assertion is not the text check #43's round 3 killed, and why the existing behavioural cases stay where they are. |
| `tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED` and `#classifications_of_nothing` | The precedent this module copies: a classification table whose rows carry grounds, a liveness half that reports a row classifying nothing, and the shrunken-corpus decline from `tests/conftest.py#decline_if_shrunken`. |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | The changelog entry goes in `seal/specs/<this id>/changelog.md`, ledger rows and re-reads in `seal/ledger/<this id>.md`. `seal/config.md` declares `Ledger frozen from`, so a drifted released row is answered by a `Re-read ·` row in the fragment. |
| `seal/follow-up.md`, the row beginning **`console.to_utf8()` is owed by an entry point and nothing says which files are entry points** | That row asks the repository owner whether the entry-point rule widens to `.github/scripts/`. #741 scopes the half to *every hook entry point*, so this work does not answer the row and does not touch it (Out of scope). |

## Scope

**In.**

1. A new test module, `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
   holding two halves:
   - **the encoding half**: an AST walk over every tracked `.py` that names
     each call of class K1 not naming an encoding, with its own
     classification table (`ALLOWED`) and that table's liveness half;
   - **the entry-point half**: an AST walk over every tracked `hooks/**/*.py`
     with a module-level `if __name__ == "__main__":` block, asserting the
     block's first statement is `console.to_utf8()`, with its own
     classification table (`ENTRY_POINTS_CLASSIFIED`) for `hooks/dispatch.py`.
2. Every product site the walk names, fixed by naming the encoding. The
   framer's census (K4) counts 29 product sites: 15 in 11 files under
   `hooks/`, 14 in 5 files under `.github/scripts/`, none under
   `skills/*/scripts/`.
3. Every test site the walk names, fixed the same way. The census counts 302
   sites in 45 files under `tests/`.
4. `console.to_utf8()` as the first statement of `__main__` in
   `hooks/git/pre-commit.py`, `hooks/git/post-commit.py` and
   `hooks/git/reference-transaction.py`, the three hook entry points that
   lack it today, plus one behavioural case for the pre-commit refusal under
   an ASCII console (S8, conditional on M4).
5. One House rules bullet in `CONTRIBUTING.md` stating the rule and naming
   the test (D8).
6. The changelog fragment and the ledger fragment, including a `Re-read ·`
   row for each released row the edits drift (M3).

**Out, and why.**

| Left out | Why |
|---|---|
| `console.to_utf8()` in `.github/scripts/` (7 of 14 files lack it) and in `skills/*/scripts/` | #741's third box says *every hook entry point*. The `seal/follow-up.md` row above asks the repository owner whether the rule widens past `hooks/`, and names that as a change to what a gate reads. This work leaves that row as it stands. |
| Turning on ruff `PLW1514` | D1: it is a preview rule, and by the ticket's account it misses `Path.read_text` / `write_text` on a variable, which is most of the class (269 of 335 census sites). A second instrument that disagrees with the first is a second thing to reconcile. |
| A `bin/` command | D1: `bin/` holds commands that ship to users and run on their repositories. This check is about the plugin's own source and has no user. |
| Python embedded in shipped Markdown or workflow YAML (`python3 -c` one-liners) | Not in the `.py` corpus (D2). Holding it is a walk over shell bodies in fenced blocks and `run:` steps, which a review fix pass may not add. The two skill one-liners round 1 of review found, and the CI workflow step it named beside them, name `encoding="utf-8"`, and `CONTRIBUTING.md`'s House rules says such a line is outside the test's reach. *Inferred during implementation, round 1 of review.* |
| Setting `PYTHONUTF8=1` anywhere (CI env, `hooks.json`, `conftest.py`) | It would hide the class rather than remove it: the Windows leg would go green with every unnamed call still in place, and a user's interpreter does not inherit a CI setting. |
| `CLAUDE.md` | #730 is about every rule `CLAUDE.md` restates having one home. The rule's home is `CONTRIBUTING.md` House rules, beside *No real identifiers*. |
| Changing `dispatch.py`'s inline reconfigure loop to `console.to_utf8()` | It is the production entry point and its loop is held behaviourally by three cases in `tests/test_console_is_not_utf8.py`. It is classified, with that as grounds (D5). |
| `bytes.decode()` / `str.encode()` with no argument, `json.dumps` | These default to UTF-8 regardless of locale, so they are not in the class. |

## The class, enumerated by construction

**K1 — the calls that take the locale's encoding when none is named.**

| Call shape | Unnamed when |
|---|---|
| builtin `open(...)`, `io.open(...)`, `codecs.open(...)` | mode is text (no `b` in a literal mode, or no mode at all) and `encoding` is neither a keyword nor the 4th positional argument |
| `os.fdopen(fd, ...)` | as `open`, positions shifted by the fd |
| `<expr>.open(...)` on any receiver except `os`, `webbrowser`, `tarfile`, `shelve`, `dbm`, `dbm.dumb`, `wave`, PIL's `Image`, a `ZipFile(...)` or `TarFile(...)` built in the receiver itself, and a bare name no import binds | judged as `Path.open`: text mode and `encoding` neither a keyword nor the 3rd positional (the 2nd on a `zipfile.Path`), every position one to the right where the method is called on its class (`Path.open(p)`); the same shift holds for the two rows below |
| `<expr>.read_text(...)` | no `encoding` keyword and no positional argument |
| `<expr>.write_text(...)` | no `encoding` keyword and fewer than two positional arguments |
| `subprocess.run`, `.Popen`, `.call`, `.check_call`, `.check_output` | `text=`, `universal_newlines=` (any value but a literal `False`) or `errors=` is present, and `encoding` is not. The module name is resolved from the file's own imports, so `import subprocess as sp` and `from subprocess import run` are both seen |
| `subprocess.getoutput`, `subprocess.getstatusoutput`, `os.popen` | no `encoding` keyword, which `os.popen` cannot take and the other two can since 3.11 |
| `tempfile.NamedTemporaryFile`, `.TemporaryFile`, `.SpooledTemporaryFile` | a literal text mode (the default is binary) and no `encoding` |
| `io.TextIOWrapper(...)`, `fileinput.input(...)` | no `encoding` |

*Inferred during implementation, round 1 of review:* the standard library's
half of K1 was enumerated by construction (every public callable whose
signature carries `encoding=None`, each read for whether `None` means the
locale), which added the compressed openers in a text mode, the logging file
handlers, `basicConfig(filename=)` and `fileConfig`, `fileinput.FileInput`
and `hook_compressed`, `argparse.FileType`, `doctest`'s file readers, and
the `.makefile()` and `.write_results_file()` methods. `ElementInclude`'s
text loader, added in round 1, reads UTF-8 when no encoding is named and was
taken out again in round 2. The module docstring holds the whole table,
what the construction excluded and why, and the spellings no row can hold.

**K2 — shapes the walker cannot prove, which therefore count as unnamed.** A
non-literal mode, `encoding=None` written out, and a `**` splat on a K1 call
with no explicit `encoding`. Each must be rewritten or classified in
`ALLOWED`. None of the three exists in the tree today except one non-literal
mode case the census met (`tests/test_the_release_seal_is_drawn.py`,
`Image.open(path)`, which K1's receiver rule names anyway).

**What naming means.** Any `encoding` value but `None` passes. The check holds
that an encoding is chosen, not which one. The repair this work writes is
`encoding="utf-8"` everywhere (D3).

**K3 — the hook entry points.** Every tracked file under `hooks/`, at any
depth, with a module-level `if __name__ == "__main__":` block. Read
2026-10-04 at `4d2afd1e`: 22 files. 18 open the block with
`console.to_utf8()`. `hooks/dispatch.py` carries the inline loop instead. The
three files under `hooks/git/` carry nothing and go straight to
`sys.exit(main())`.

**K4 — the framer's census, executed.** A read-only AST walk written to the
framer's scratchpad, run once at `4d2afd1e` over `git ls-files '*.py'`, then
deleted. It approximates K1 (it matched subprocess calls by function name, so a
local helper named `run` could be counted), so the smith's walker is the
number of record and M1 compares the two. What it found:

- Every tracked `.py` lies under `hooks/`, `skills/*/scripts/`,
  `.github/scripts/` or `tests/`. The issue's four roots are the whole corpus
  today.
- 335 unnamed sites. 29 product, 302 test. By kind: `.write_text()` 236,
  `.read_text()` 33, `subprocess.run(text=True)` 32, builtin `open()` 28,
  `subprocess.Popen(text=True)` 1, `.open()` 1 (`Image.open`, PIL).
- Product sites. `hooks/`: `answers.py` 1, `commit-review-gate.py` 2,
  `commitgate.py` 1, `hook-install.py` 1, `implementer-notice.py` 1,
  `mode-gate.py` 1, `review-skill-gate.py` 1, `session-lease.py` 1,
  `version-check.py` 2, `worktree-guard.py` 3, `worktree_consent.py` 1, all
  builtin `open()`; 9 of the 15 are `open(path, "w").close()` creating an empty
  marker. `.github/scripts/`: `close_issues_on_release.py` 4,
  `plugin_directory_check.py` 3, `publish_release_note.py` 3,
  `release_seal.py` 2, `roll_flow_measurement_issue.py` 2, all
  `subprocess.run(..., text=True)`.
- Its four `os.fdopen` hits under `skills/*/scripts/` were false positives of
  the census itself (all four name `encoding="utf-8"` or a binary mode, read
  at each line), so `skills/*/scripts/` has none.
- The largest test files: `test_session_cost.py` 55,
  `test_the_records_can_be_carried_out_and_in.py` 20,
  `test_the_ledger_migrates_itself.py` 20,
  `test_the_suite_has_a_command_that_is_cheap_twice.py` 17.

## Decisions

**D1 — delivered as a test module, and only as one.** The repository's
hygiene checks over its own source are test modules the suite runs on all
three CI legs: `tests/test_no_real_identifiers.py`,
`tests/test_one_word_one_meaning.py`, and the closest precedent,
`tests/test_a_script_says_which_interpreter_it_needs.py`, an enumeration of a
class over shipped Python with a `CLASSIFIED` table. `bin/` holds commands
that ship to users and judge their repositories (`evidence-check`,
`arm-check`, `broad-gate`), and this check judges nobody's code but the
plugin's. A ruff rule is rejected for the reasons in Out of scope. The test
runs on the Windows leg, which is where the class shows.

**D2 — the corpus is every tracked `.py`, not four named roots.** K4 shows the
two are equal today. Enumerating by `git ls-files` means a fifth root (an
`evals/` script, say) is covered on arrival rather than when somebody
remembers to extend a list, which is the rot §7 describes. The walk reuses
`tests/conftest.py#git_listing` and `#on_disk`, and the liveness half declines
through `#decline_if_shrunken` when a tracked file is missing from disk,
exactly as the precedent does.

**D3 — every site is fixed, and the repair is `encoding="utf-8"`.** The issue
allows *fixed, or listed with grounds*. A row in `ALLOWED` for an
`open(path, "w").close()` marker costs more words than the fix, and a table
that starts full teaches the next branch that classifying is the normal path.
So `ALLOWED` lands with the rows only a fix cannot serve: `Image.open` (PIL
opens images in binary, and it has no text mode to name) and whatever W2
finds. UTF-8 is the encoding every record, ledger row and fixture in this
repository is written in, and the existing named calls already use it.

**D4 — the allowlist is keyed by unit, not by line.** `ALLOWED` maps
`"<path>#<qualname>"` (the enclosing function or class, `<module>` at top
level) to its grounds, in the ledger's own anchor shape. A line number goes
stale on any unrelated edit above it. A row covers every unnamed site in its
unit, which is acceptable because a unit holding a deliberate locale call is
rare and its grounds say why. A row with empty grounds is refused.

**D5 — the entry-point half is an AST order assertion, and dispatch is
classified.** The existing module refuses source-text assertions because
*moving the reconfigure block from before `main()` to after it* left #43's
text checks passing. K3's assertion is on the AST and on order: the guard
block's **first** statement must be the call `console.to_utf8()`. Moving it
after `main()` fails that, and so does deleting it. What the AST cannot see is
`console.to_utf8` itself being neutered, and
`tests/test_console_is_not_utf8.py#test_a_gate_run_on_its_own_still_reaches_a_verdict`
already holds that behaviourally. A behavioural case per entry point was
weighed and rejected (plan.md A7). The entry points read stdin inside a `try`
whose handler returns silently (read at `4d2afd1e`: `hooks/version-check.py#main`
catches `ValueError`, `hooks/hook-install.py#main` catches `Exception`), and
silence is also what a hook says when nothing applies. A uniform case would
see silence with the call and silence without it, so it could not be seen red
without building each hook's own triggering state, which §15 forbids skipping. `hooks/dispatch.py` sits in `ENTRY_POINTS_CLASSIFIED`
with the grounds *inline loop; held by the three dispatch cases of
`tests/test_console_is_not_utf8.py`*.

**D6 — failure direction of the git-hook change.** `hooks/gate.py:182`
builds the waiver it names in a refusal with U+2026 (`commit …`). Read, not
executed: under an ASCII stderr the pre-commit hook should die with
`UnicodeEncodeError`, exit non-zero, and git aborts the commit. So today the
commit is refused and the person reads a traceback in place of the refusal.
After the change the commit is still refused and the refusal is legible. The
gate blocks neither more nor less, and the prompt budget is zero. Under
cp1252 (Windows, stderr a pipe) the ellipsis goes out as byte 0x85 and a UTF-8
terminal shows garbage; UTF-8 output is what the rest of the hooks already
write. M4 measures the ASCII half before S8 is planted.

**D7 — a converted read in a hook must not newly raise.** On a cp1252 machine
an unnamed read never raised, because cp1252 decodes almost any byte. Strict
UTF-8 can raise `UnicodeDecodeError`, a `ValueError`. Inside a hook that
raise reaches `dispatch.py`'s `except Exception`, which is an allow. So each
converted read under `hooks/` either sits in a handler that already catches
`ValueError` or `Exception`, or adds `errors="replace"`. Read at
`4d2afd1e`: `hooks/worktree-guard.py`'s two JSON reads catch `Exception`;
`hooks/commit-review-gate.py#read_mark` catches `OSError` only and needs
`errors="replace"`. The rest is W1. Writes and the empty-marker `open(..., "w")`
cannot raise on encoding. Outside `hooks/` (scripts, tests) strict is right,
because a corrupt read should fail loudly.

**D8 — the rule is stated where a contributor reads it.** One bullet under
`CONTRIBUTING.md` §*House rules*, after *No real identifiers*, in its shape:
the rule in bold, the test that enforces it, and *classify deliberately, never
to make a test pass*. The test module's own docstring carries the reasoning
(the #736 incident, why the AST and not ruff, K1 and K2).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the class is enumerated | Given the tree after this work, when the suite runs, then the encoding half names no unnamed K1 call outside `ALLOWED` in any tracked `.py` | The repository-wide case, executed; seen red at the start of phase 1 against the unfixed tree, naming the product sites, and again at phase 2's widening to `tests/` |
| S2 each K1 shape is seen | Given a source string with one unnamed call of each K1 shape, when the walker reads it, then it reports that call with its kind and line; and given the same call with `encoding=` named, positionally where K1 allows, or in a binary mode, then it reports nothing | One parametrized synthetic case per shape, each shown red by deleting that shape's rule from the walker |
| S3 K2 counts as unnamed | Given a non-literal mode, `encoding=None`, or a `**` splat with no `encoding`, then the walker reports it | Synthetic cases, shown red against a walker that skips the shape |
| S4 aliases resolve | Given `import subprocess as sp; sp.run(x, text=True)` and `from subprocess import run; run(x, text=True)`, then both are reported, and a local function named `run` is not | Synthetic cases, shown red against a walker that matches by attribute name alone |
| S5 a classification of nothing is reported | Given an `ALLOWED` row whose unit has no unnamed call, then the liveness half fails naming the row | Synthetic case on a built tree (`conftest.build_tracked_tree`), red against a check without the liveness half |
| S6 a missing tracked file declines rather than drops a row | Given a tracked file deleted from the working tree and an `ALLOWED` row in it, then the liveness half skips with `shrunken_corpus`'s reason and does not report the row | Synthetic case, mirroring `test_a_skipped_file_does_not_read_as_a_lost_classification` |
| S7 every hook entry point opens with the call | Given every tracked `hooks/**/*.py` with a `__main__` block, then each block's first statement is `console.to_utf8()`, `hooks/dispatch.py` excepted by classification | The repository case, executed; seen red against the unfixed tree naming the three `hooks/git/` files; a synthetic case where the call follows `main()` is reported |
| S8 the pre-commit refusal is legible on an ASCII console | Given a commit the pre-commit hook refuses, run with `PYTHONIOENCODING=ascii` and `PYTHONUTF8=0`, then stderr carries the refusal and no `UnicodeEncodeError` | A behavioural case, planted only if M4 shows it red against the unfixed hook; otherwise S7 alone holds the three git hooks, and `overview.md` says so |
| S9 a hook read does not newly raise | Given a hook file whose read was converted, when its input holds bytes that are not UTF-8, then the hook behaves as it did (empty, default, or skipped), not a raise | Read per site (W1). `read_mark` gets a synthetic case: a mark file holding byte 0xFF, red against `encoding="utf-8"` without `errors="replace"` |
| S10 the rule is where a contributor reads it | Given `CONTRIBUTING.md`, then House rules names the rule and the test module | Read; `tests/test_docs_line_wrap.py` and any test covering `CONTRIBUTING.md`, run narrowly |

## Data & interfaces

- **New module.** `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`.
  The walker is a function over a source string and a path, returning
  `(lineno, kind, qualname)` per unnamed site, so the synthetic cases call it
  without a tree. The repository case composes it with `git_listing` and
  `on_disk`.
- **`ALLOWED`**: `dict[str, str]`, `"<path>#<qualname>"` to grounds (D4).
- **`ENTRY_POINTS_CLASSIFIED`**: `dict[str, str]`, path to grounds, one row
  at landing (`hooks/dispatch.py`).
- **The failure message** names each site as `path:line (kind, unit)` and the
  repair: *name `encoding="utf-8"`, or classify the unit in `ALLOWED` with its
  grounds*. A person reads it at a red Windows leg and acts on it, so the case
  pins the repair sentence (§14).
- **Product edits** add `encoding="utf-8"` (and `errors="replace"` where D7
  needs it) to existing calls. No signature, verdict or message changes. The
  three git hooks gain `import console` beside their existing `import
  commitgate` and the call.
- **Ledger.** New rows in `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md`
  for the claims this work makes (the corpus equals the four roots; the
  entry-point set; D7's per-site handlers). `Re-read ·` rows for released rows
  whose unit an edit drifts, written by `bin/evidence-check --reverify --into
  <fragment> --checked <date>` after each drifted row is read (M3).

## Open questions → questions.md

Every judgment the ticket left open is decided above with its grounds, and
listed in `questions.md` as decided by the frame. Nothing there waits on a
person.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-04 by framer, before the build.
