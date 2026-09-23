# Review round 1 — `chore/519-the-ledger-grows-and-nothing-takes-a-row-out`

Target SHA `be4e0917`. The target is the whole branch, `f8f1c9de..be4e0917`
(nine commits, 13 files). The review ran in a `git clone --no-local` at the
target, with a second clone at `f8f1c9de` used only as the old checker's
plugin copy. Both clones and every probe file have been deleted.

## What this round was asked

Round 1 of #519, PR #531 (draft, base `release/v0.14.0`). Stage 1 asked
whether the decision (no ledger row leaves; memoise `py_spans` by file text)
follows from the framer's measurements, and whether output is truly
unchanged, re-measured in a clone with `--reverify` and the advisor path as
well as `--strict`. Stage 2 asked for an attack on the memo: staleness within
one process (`--reverify`, a file edited between two reads, identical text
at two paths), whether callers still get independent mutable copies, whether
`functools.cache`'s unbounded size matters for this corpus, and whether
`rider_check.py` or any other caller depends on parsing per call. It also
asked whether every place that states the old cost was corrected and whether
the new sentence names its instrument and date. The smith's two edits
outside the code, the reworded stamp in the framer's `spec.md` and
`phases/phase-2.md`, and the raw test docstring, were to be judged too. No
full suite, repository-wide lint or broad gate.

There is no earlier round, so nothing was carried. Every verdict below is
this round's.

How the findings relate:

```
the memo (evidence_check.py#py_spans / #parsed_spans)
  ├ output, re-measured old vs new on one tree   → identical but stderr (🟢)
  ├ staleness, copies, memory, callers           → nothing found (🟢)
  └ the cost the checker states about itself
      ├ advisor docstring, scan_candidates, one test → corrected (🟢)
      ├ hooks/ledger-migrate.py "the checker's ~130 ms full run" → missed (🟡 1)
      └ two new sentences state a corpus count with no instrument (⬜ 2)
```

## Stage 1 — spec compliance

**The decision follows from the measurements (read).** `spec.md` §2 shows
1,328 parses of 126 files and a memoised probe at 1.81 s with identical
findings. §1 shows every anchor resolving and §3 shows low overlap with
`docs/`. A memo over the parse is the smallest change that answers the cost,
and removing rows would have answered nothing the measurements found. The
Out list gives a reason for each exclusion. Q1 (close or keep #519 open) is
still the owner's and is marked so in `overview.md`.

**Output is unchanged, re-measured (executed, Python 3.13.5, macOS,
2026-09-23).** The same tree was run by the old checker file (the clone at
`f8f1c9de`) and the new one (the clone at `be4e0917`), with cwd and root the
same for both:

- `--strict .` and a plain run on the clean tree: stdout, stderr and exit
  identical (exit 0). Old 16.75 s, new 1.90 s.
- A perturbed copy of the tree with three functions renamed, one body edited,
  one advisor function renamed and edited, `hooks/ledger-migrate.py` moved,
  `.github/scripts/fold_ledger.py` deleted, and a new file that raises
  `SyntaxWarning`. `--strict .` gave stdout identical, exit 2 from both,
  `1459 ok · 1 drifted · 22 broken`. The `(renamed?)` hints went through the
  repository-wide scan.
- `--reverify .` on two identical copies of that perturbed tree: stdout
  identical, exit 0 from both, `21 rows re-verified`. `diff -r` of the two
  trees afterwards is empty, so both versions write the same ledger bytes.
  A follow-up `--strict .` on each gave identical stdout.
- `hooks/evidence-advisor.py` fed a `git commit` payload: on the clean tree
  both print nothing (old 15.13 s, new 1.69 s). On the perturbed tree both
  print the same 24 lines, starting `evidence-check: this commit leaves 22
  anchors broken`.

The only difference is on stderr. Where a scanned file raises
`SyntaxWarning`, the old code printed the warning at every parse (14 to 39
lines depending on the run) and the new code prints it once. `overview.md`
discloses this, and it is not a finding. `spec.md` Scope 1 speaks of
findings, and the advisor's scenario ("prints exactly what it printed
before") concerns stdout, which is what the hook shows.

**The smith's cases are real (executed).** With the old `evidence_check.py`
put into the clone, `test_rows_citing_one_file_cost_one_parse` fails with
`10 parses of one file for five rows` and the other four selected cases pass.
Three mutants of the new code each turn exactly one case red: `py_spans`
returning the stored dict, copying the dict but not the lists, and removing
`@functools.cache`.

**The new cost sentence names its instrument and its date (read).**
`hooks/evidence-advisor.py:6-14` gives `/usr/bin/time -p`, three runs,
2026-09-23, Python 3.12.11 on macOS, and the before figure. My one advisor
run measured 1.69 s against its "about 1.7 s". It says 1,476 anchors where
the checker prints `total: 1482 ok` at the target. The difference is this
work item's own six anchors, which were added after the measurement, and the
sentence is dated, so this is not a defect.

## Stage 2 — the memo attacked

- **Staleness inside one process: none found.** `parsed_spans` takes the
  text as its only argument. `ast.parse` depends only on that text and on the
  interpreter, which is fixed for the life of the process. A path key would
  be stale after an edit. A text key cannot be, and `--reverify` rewrites
  markdown ledgers, not the `.py` sources whose text is the key. The executed
  `--reverify` comparison above covers the path that reads and then writes in
  one process. `rider_check.py`'s migration rewrites `.py` files. The text it
  passes afterwards is a new key, so it is parsed fresh (read).
- **Identical text at two paths: nothing path-dependent is cached.** The
  path's influence (`path.endswith(".py")` in `resolve_unit`, `rel` in
  `file_units`) is applied by the callers outside the memo
  (`evidence_check.py:363-371`, `:638-641`, read).
- **Callers get independent copies (executed and read).**
  `evidence_check.py:180-183` builds a new dict of new lists, and the tuples
  inside are immutable. The mutants above show the case can fail.
- **Memory is bounded by what one run reads (executed).** After a full
  in-process check of every ledger, the memo's own cache statistics show 127 entries, 1,212
  hits and 4.88 MB of key text, with 22.7 MB traced by `tracemalloc` for the
  whole run (40.6 MB peak). The BROKEN-path scan adds at most 200 files of
  256 KB or less per extension. The advisor runs `exec_module` on every commit
  (`hooks/evidence-advisor.py:118-120`), so its memo does not outlive a
  commit. That is not a concern.
- **The warnings filter is process state that the memo freezes (executed).**
  Under `warnings.simplefilter("error")`, a text that raises `SyntaxWarning`
  parses to `None`, and that `None` is then served when the same text is
  asked for under `"ignore"`. A fresh module under `"ignore"` returns the
  spans. The CLI and the advisor set the filter once per process, and the
  repository sets no `filterwarnings` or `-W` for pytest (read). So no real
  caller sees a difference. Recorded as not a defect.
- **No caller depends on parsing per call (read).** `check_text`, `reverify`,
  `file_units`, `rider_check.py#inferred_anchor` (`.github/scripts/rider_check.py:555`)
  and `rider_check.py#region_lines` (through `checker.resolve_unit`, `:331`)
  rebind or read and never mutate. That agrees with the smith's Q2 answer.
  Exceptions other than `SyntaxError` (for example `RecursionError`) are not
  cached by `functools.cache` and propagate as before.

## 🟡 1 — `hooks/ledger-migrate.py` still states the checker's cost as "~130 ms"

`hooks/ledger-migrate.py:32-35` says the session-start scan is cheap
*"against the checker's ~130 ms full run"*. It was written 2026-09-01
(`117d37fe`), like the advisor's "114 ms". It has no instrument and no date,
and it is now wrong by a factor of 14 (1.9 s, executed above). Before this
branch it was wrong by 120.

This is the class the work item exists to correct, the checker's clean-run
cost stated as current. The branch enumerated the class by the literal
string "114 ms" (`phases/phase-1.md`, *"stated in two more places"*; C2's
Read cell, *"the other two places stating '114 ms'"*), so this fourth
instance is outside what the branch searched (`agent-contract` §12).
`spec.md`'s opening claim that the work *"corrects the one document that
states what the check costs"* is false for the same reason.

Why it matters: this is the one other sentence in the shipped tree that
tells a reader what the full check costs. A reader deciding whether a hook
can afford the full check would read 130 ms and be wrong by an order of
magnitude, which is exactly the misreading this work item fixed in the
advisor.

The fix edits a module docstring only. No ledger row anchors that docstring
(the anchors are `#main`, `#dirty` and `#HOME_GLOBS`), so nothing drifts.
The "~24 ms" and "~60 ms" figures are not re-measured here. The fix dates
them rather than restating them. `spec.md` §2 measured the whole hook at
0.32 s wall, and whether "~60 ms for the whole session-start group" still
holds is for whoever takes the fix to measure or leave dated.

## ⬜ 2 — two new sentences state a corpus count with no instrument

`skills/evidence-check/scripts/evidence_check.py:169-172` (`py_spans`'s
docstring) and `tests/test_a_row_points_by_content.py:126-128` (the
parse-count case's docstring) state *"1,328 parses of 126 files … about 94 %
of a 15.8 s run"*. Each is dated only by `#519` and neither names how the
number was taken. That is the shape `docs/the-evidence-ledger.md` §*A bound
over the corpus is stated with its instrument and the moment it was taken*
names. Both are in the past tense and describe why the memo exists, so no
reader is misled about the present and no release ships a defect. Adding the
instrument keeps the sentence re-derivable. Fixing it is optional.

## 🟢 The smith's two edits outside the code

- **The reworded stamp in `spec.md` Scope 4 and `phases/phase-2.md`.** The
  only change in `spec.md` since the framer's commit `afb0f136` is that line.
  The hash and its meaning (the row's anchor at framing time) are kept, and
  the anchor shape that the records arm read as a BROKEN stamp is removed.
  `overview.md` discloses it as the framer's file. `--strict .` exits 0 at
  the target (executed). This is the right edit and not a defect.
- **The raw docstring.** `test_an_old_format_ledger_is_loud_never_invisible`'s
  docstring value, compared through `ast.get_docstring` at `f8f1c9de` and at
  the target, is identical (executed). The warning was a backslash-backtick escape and the
  value keeps the backslash either way.

## Regression tests to plant

None. The three planted cases cover the memo's properties and each has been
seen red.

## Facts for the evidence ledger

- If 🟡 1 is fixed, C2's Read cell should say three other places carried the
  stale cost and name `hooks/ledger-migrate.py`'s module docstring as the
  third, found in round 1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `hooks/ledger-migrate.py` still states the checker's full run as "~130 ms", undated and with no instrument, now wrong by 14x. It is a fourth instance of the stale-cost class that the branch enumerated by the literal "114 ms" | `hooks/ledger-migrate.py:32-35` | open | Read and `git log -S` (`117d37fe`, 2026-09-01). The full check measured 1.90 s at the target (executed) |
| 2 | ⬜ `py_spans`'s docstring and the parse-count case's docstring state "1,328 parses of 126 files, about 94 % of a 15.8 s run" with no instrument | `skills/evidence-check/scripts/evidence_check.py:169-172`, `tests/test_a_row_points_by_content.py:126-128` | open | Read. The sentences are past-tense motivation, so no behaviour or current fact is wrong |
| 🟢 | The decision (memoise the parse, remove no row) follows from `spec.md`'s three measurements | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` §1–§3, Scope | not a defect | Read |
| 🟢 | Output unchanged: `--strict`, plain, `--reverify` and the advisor are identical old vs new on one tree, clean and perturbed. The only difference is the `SyntaxWarning` collapsing on stderr, which is disclosed | `skills/evidence-check/scripts/evidence_check.py:152-222` | not a defect | Executed. `diff -r` after `--reverify` is empty |
| 🟢 | No staleness within one process: the key is the text, and the path's influence stays outside the memo | `skills/evidence-check/scripts/evidence_check.py:186-222`, `:363-371`, `:638-641` | not a defect | Read, and the `--reverify` comparison was executed |
| 🟢 | Callers get independent dicts and lists, and each case goes red against its mutant | `skills/evidence-check/scripts/evidence_check.py:180-183` | not a defect | Executed: three mutants, one red each; the old checker gives `10 parses` |
| 🟢 | The memo's size is bounded by what one run reads: 127 texts, 4.88 MB of keys, and the advisor rebuilds it on every commit | `skills/evidence-check/scripts/evidence_check.py:186`, `hooks/evidence-advisor.py:118-120` | not a defect | Executed (the memo's cache statistics, `tracemalloc`) |
| 🟢 | The memo freezes an answer computed under the process's warnings filter. No caller changes the filter mid-process | `skills/evidence-check/scripts/evidence_check.py:186-195` | not a defect | Executed: under `error` the result is `None` and the same text is served `None` under `ignore`. Read: no `filterwarnings` or `-W` in the repository |
| 🟢 | `rider_check.py` and the other callers never mutate the result and do not depend on parsing per call | `.github/scripts/rider_check.py:331`, `:555` | not a defect | Read |
| 🟢 | The advisor's new cost sentence names its instrument, runs, date, platform and the before figure | `hooks/evidence-advisor.py:6-14` | not a defect | Read, plus one run executed at 1.69 s |
| 🟢 | The reworded framing-time stamp in `spec.md` Scope 4 and `phases/phase-2.md` keeps its meaning and is disclosed | `seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md` Scope 4 | not a defect | Read `git diff afb0f136..be4e0917`, and `--strict .` exit 0 was executed |
| 🟢 | The raw docstring keeps its value byte for byte | `tests/test_a_row_points_by_content.py:822` | not a defect | Executed an `ast.get_docstring` comparison at base and target |

## Executed probes

| What was run | Result |
|---|---|
| Old checker file (`f8f1c9de`) vs new (`be4e0917`) on the same clean tree: `--strict .` and a plain run | stdout, stderr and exit identical, exit 0. 16.75 s → 1.90 s and 15.50 s → 1.87 s |
| The same on a perturbed copy (renames, an edit, a moved file, a deleted file, a `SyntaxWarning` file): `--strict .` | stdout identical, exit 2 both, `1459 ok · 1 drifted · 22 broken`. Stderr 22 warning lines old, 1 new |
| `--reverify .` on two identical perturbed copies, old and new | stdout identical, exit 0 both, `21 rows re-verified`. `diff -r` of the two trees afterwards is empty |
| `hooks/evidence-advisor.py` with a `git commit` payload, old and new plugin copies, clean and perturbed trees | clean: empty stdout both, 15.13 s → 1.69 s. Perturbed: the same 24 lines both |
| `bin/test tests/test_a_row_points_by_content.py -k` the three new cases plus the two `py_spans` cases, new checker and then old checker file | new: 5 passed. Old: 1 failed (`10 parses of one file for five rows`), 4 passed |
| The three new cases against three mutants (stored dict returned, dict copied without its lists, `@functools.cache` removed) | each is 1 failed and 2 passed, exit 1. The file was restored and byte-compared |
| In-process full check, reading the memo's cache statistics and `tracemalloc` | 127 misses, 1,212 hits, 4.88 MB of key text, 22.7 MB traced (40.6 MB peak) |
| The same text under `simplefilter("error")` and then `"ignore"`, one module, and a fresh module under `"ignore"` | `None`, then `None` from the memo, then spans from the fresh module |
| `ast.get_docstring` of `test_an_old_format_ledger_is_loud_never_invisible` at `f8f1c9de` and at the target | identical |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due when the rounds leave nothing open. This round leaves 🟡 1 open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `hooks/ledger-migrate.py`'s "~24 ms in-process" and "~60 ms wall for the whole session-start group" still hold (`spec.md` §2 measured the hook at 0.32 s wall) | this round's 🟡 1 fix dates them rather than re-measuring them | the smith taking 🟡 1, who re-measures them or leaves them dated |
| The `ledger` CI job's wall time on Linux after the change | `overview.md` §Not verified, already deferred by the smith | the orchestrator, reading PR #531's CI run |

## Paste-ready fixes

🟡 1 — `hooks/ledger-migrate.py`, replacing lines 32-35 of the module docstring:

```
  - **silent when there is nothing to migrate** — the every-session scan
    reads `old_format_rows` alone and never runs the full check. Measured
    2026-09-01 at ~24 ms in-process on this repository's own ledgers and
    ~60 ms wall for the whole session-start group; the full check it skips
    took about 1.9 s on the same repository on 2026-09-23
    (`/usr/bin/time -p` over `evidence_check.py --strict .`, macOS, #519)
```

⬜ 2 — `skills/evidence-check/scripts/evidence_check.py`, in `py_spans`'s docstring:

```
    **One parse per distinct text, for the life of the process** (#519). The
    ledger cites one file from many rows, and parsing it once per row was
    1,328 parses of 126 files, about 94 % of a 15.8 s `--strict` run that
    every `git commit` paid through `hooks/evidence-advisor.py` (`cProfile`
    over `--strict .`, 2026-09-23). The memo is
```

Needs a fix: yes — finding 1, `hooks/ledger-migrate.py` still states the checker's full run as ~130 ms, the stale-cost class this work item exists to correct

Loses a record or crashes: no

## Proof block

Files opened: `hooks/evidence-advisor.py`, `hooks/ledger-migrate.py` (lines 25-45 and grep),
`skills/evidence-check/scripts/evidence_check.py` (imports, 140-240, 330-380,
620-720, 920-945, 2356-2380, grep), `skills/evidence-check/SKILL.md` (448-464),
`.github/scripts/rider_check.py` (540-580, grep), `tests/test_a_row_points_by_content.py`
(diff, 821-835), `seal/ledger.md` (diff hunks), `seal/ledger/1790154760-the-ledger-grows-and-nothing-takes-a-row-out.md`,
the work item's `spec.md`, `questions.md`, `overview.md`, `changelog.md`,
`routing.md`, `phases/phase-1.md`, `phases/phase-2.md`,
`docs/the-evidence-ledger.md` (the instrument clause), `bin/test`.
