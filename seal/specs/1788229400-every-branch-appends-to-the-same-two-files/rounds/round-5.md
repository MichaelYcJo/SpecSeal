# 1788229400-every-branch-appends-to-the-same-two-files — review round 5

The verifying round for round 4's fixes. Its surface is the fix diff rather
than the branch, and its question is the answers rather than new findings:
for each verdict round 4 recorded as closed, is it actually closed.

All fourteen are closed. What this round found is what closing them opened.

| Field | Value |
|---|---|
| Target SHA | `0a60d52` |
| Diff base | `76e61a4` — round 4's target |
| Fix commit under review | `38802bc` |
| PR | not yet |
| Broad gate | not yet — slices only this round; the full suite, lint and typecheck are the orchestrator's, once, after this round settles |
| Fixes checked by | `round-6` |
| Needs a fix | yes — four 🔴 and four 🟡 from the reviewer, and 🔴 I, which the orchestrator added after the round closed |

- [ ] Pass

## The bound was reached twice over, and that is this round's headline

`docs/review-chain-spec.md:34-42` bounds the run at five rounds while a 🔴 is
open, and separately at **stop regardless — a round opens a new 🔴 at the same
site as the one it was closing**. This round is the fifth, and 🔴 C is a new
🔴 at `generic_units`, the site round 4's 🔴 1 fixed. Either bound alone ends
the run here; both fire.

The second is the one that carries information. The keyword blocklist that
closed 🔴 1 is wrong in both directions — it fails to block the shape it was
written for when no word precedes the call, and it blocks two real
declarations because their modifiers happen to be statement keywords in
another language. That is the cap's own definition of a structure signal:
something is being missed that a third patch at the same coordinates does not
reach. It is recorded as an open question rather than closed by a fix.

## What round 4 closed — all fourteen, answered on this round's grounds

| # | Answer | Settled by |
|---|---|---|
| 🔴 1 | closed for `return render(y);` — and the rule broke the other way, 🔴 C | executed |
| 🔴 2 | closed. Move `handler` to `lib.py` leaving the call: `BROKEN … identical content at src/lib.py#handler (moved?)`, `--reverify` heals to the true destination, recheck exit 0 | executed |
| 🔴 3 | closed in a repository with no cross-repo declaration; still open in a parity repository, 🟡 F | executed |
| 🔴 4 | closed, both halves. `--reverify --default-repo` re-verifies; a row in no checkout leaves the ledger byte-identical and `copycat.py#grab` is absent from the output | executed |
| 🟡 5 | closed — two rows at one coordinate read `1 ok · 1 drifted`, exit 1 | executed |
| 🟡 6 | closed, both halves. Totals carry `2 old-format`, exit 2; the advisor prints the OLD-FORMAT block, and both blocks when a BROKEN accompanies it | executed |
| 🟡 7 | wording and Known limits closed; the limit itself widened to constants, 🟡 G | executed |
| 🟡 8 | closed — a heading-path locator receives the hint and heals | executed |
| 🟡 9 | closed — `--migrate --map … --default-repo …` migrates and preserves the mapped prefix | executed |
| 🟡 10 | engine and CLI closed; the proof reads the wrong file outside a git top level (🔴 A) and the automatic path discards the warning (🟡 E) | executed |
| 🟡 11 | closed | read |
| 🟡 12 | closed | read |
| 🟡 13 | closed; one straggler at `plan.md:69`, recorded 🟢 | read |
| 🟡 14 | the intent is closed; the implementation is wrong in two directions, 🔴 B and 🔴 D | executed |

**Pin discrimination.** Twelve of the new pins were mutated by reverting the
fix each one guards: **12 killed of 12**, run in a separate tree. The
exception is finding 7's output wording, which has no pin — reverting
`(identical content)` to `(content moved intact)` passes all 69 cases in the
four files.

## Verdicts

What the fixes opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 A | `content_at` resolves its path against the git **top level**, not against `-C`. Run `--migrate` from a subdirectory and the since-the-stamp proof reads a same-named file elsewhere in the repo — so a row is rewritten onto the wrong unit **and stamped as proved**, exit 0, silent. The `repo == root` guard at `:899` compares against `root`, not against the top level, so it does not fire. It also refuses the honest direction: an untouched row reads `LEFT content changed since the stamp` forever | `evidence_check.py:821` · used at `:899-916` | **open** | Reviewer-executed both directions; orchestrator confirmed by reading — `git show {sha}:{rel}` with no `./`, and `hooks/optin.py:33` passes `--show-toplevel` so only the CLI path reaches it. Worse than no guard: without it the row would at least print as rewritten without proof |
| 🔴 B | `read()` returns `None` for every `OSError`, and `check_ledger` answers `[]`. An unreadable ledger — permissions, a directory named `.md`, an I/O error — is indistinguishable from an empty one and **exits 0**. Round 4's 🟡 14 called the old `TypeError` a traceback in CI; a traceback is a broken build, and the guard converted it into the green build OLD-FORMAT exists to prevent | `evidence_check.py:656-659` · `:584-589` | **open** | Reviewer-executed: one ledger, `chmod` the only difference — readable is exit 2 with `1 old-format`, unreadable is exit 0 with all zeros. Orchestrator confirmed by reading. Pairs with 🔴 D: a 0600 ledger read by a later CI step under another uid checks zero rows and passes |
| 🔴 C | The declaration rule is wrong in **both** directions. `STATEMENT_WORDS.intersection(pre_words)` matches anywhere in `pre`, so C# `public new void Render(int x)` and Swift `case loading(String)` are refused as declarations — real code, BROKEN, exit 2. And a call statement with nothing before it, `render(1);`, has empty `pre`, so it is still read as a declaration: identical output to the pre-fix code. **This is the structure signal** — see the section above | `evidence_check.py:348-350` | **open — and not by another patch here without an answer to Q2** | Reviewer-executed old and new modules side by side on identical input; orchestrator confirmed by reading — `new` and `case` are both in `STATEMENT_WORDS:286,294`. Not reachable by this repository's CI: the path is for non-`.py` files |
| 🔴 D | `write_atomic` replaces the **path**, not the file. A symlinked ledger is silently replaced by a regular file — the real ledger behind it is never updated and stays stale, while the command reports success. Ordinary ledgers are demoted `0644 → 0600`, which git does not track outside the exec bit. `--reverify`, `--migrate` and the session-start hook all write through it | `evidence_check.py:592-611` | **open** | Reviewer-executed: symlink gone, mode 0600, the real file still at the old hash. Orchestrator confirmed by reading — `mkstemp` is 0600 and `os.replace(tmp, path)` targets the link itself. Fix is `os.path.realpath` before `mkstemp` plus `os.chmod` from the target's mode |
| 🟡 E | The CLI prints the `unproven` count as a paragraph; the session-start hook drops it — `migrated, left, _unproven`. The path a person typed warns, and **the path nobody asked for is silent**, which inverts round 4's 🟡 10, whose whole grounds were that this hook fires without a user's choice. `stamp(root)` is unconditional, so it is not retried | `hooks/ledger-migrate.py:165` | **open** | Orchestrator confirmed by reading the discard and the unconditional `stamp` |
| 🟡 F | `cross_repo_intent` is true on the mere presence of `.specseal/parity.md`, and then the scan is off for **every** unplaceable row, not the cross-repo ones. Round 4's 🔴 3 is therefore still live in a parity repository — a renamed directory reads EXTERNAL at exit 0 over a false message — and a purely local file rename loses its `(moved?)` hint and its `--reverify` heal entirely. Known limits says "directory"; the loss is every move | `evidence_check.py:679-694` · `:977-987` | **open** | Reviewer-executed, one repository with and without `parity.md`. Graded 🟡 rather than 🔴 because round 4's grounds — the two commands disagreeing about one row — are gone: `--reverify` now refuses too. The `--map` half is decidable; the `parity.md`-only half is not, and can close as an answer with grounds plus a Known-limits correction |
| 🟡 G | Fixing 🔴 2 put module- and class-level assignments into `ast`'s answer, so constants became scan candidates — and a constant holding one bare literal collides far more readily than a function. Deleting `TIMEOUT = 10` re-anchors its row onto an unrelated `RETRIES = 10`, `--reverify` accepts it, recheck exits 0. Known limits names `__init__`s, getters and wrappers; the candidate this commit added is not there | `evidence_check.py:134-142` · `:465-468` | **open** | Reviewer-executed end to end. Closes as a Known-limits line, or by excluding one-line `Assign` from `file_units`' `.py` branch |
| 🟡 H | Four documents now contradict the code the same way round 4's 🟡 11-13 did, because 🟡 10's fix put a git call in the file. `CLAUDE.md:88` and `README.md:156` / `README.ko.md:149` say the checker calls git for nothing **at all**; `hooks/evidence-advisor.py:24` says only BROKEN is printed, and the same commit taught it OLD-FORMAT. No test pins any of the three documents | `CLAUDE.md:88` · `README.md:156` · `README.ko.md:149` · `hooks/evidence-advisor.py:24` | **open** | Orchestrator confirmed all four by reading. The module docstring and `SKILL.md` already carry the correct exception; the sentence can be borrowed |
| 🔴 I | A ledger row citing `../…` is read from outside the repository, and `--reverify` writes a hash of what it found back into the ledger — so a project's own ledger becomes a confirmation oracle for a file the project does not contain. `ANCHOR_RE`'s path class admits `.` and `/`; `place()` returns `(root, raw_path)` with no containment test; `read(os.path.join(root, rel))` follows it out of the tree. Absolute paths do not match, so this is relative traversal only | `evidence_check.py` `ANCHOR_RE` · `place()` · every call site of `read` that takes a placed row | **open** | **Orchestrator-executed, after the round closed** — a fixture repository with a row above its root: check prints `DRIFTED ../outside/creds.py#secret`, `--reverify` rewrites the hash and exits 0. **The released 0.1.0 checker has it too** (`708e348`, the `path:line` form, same row, `2 ok`, exit 0), so it is not a defect this redesign introduced and its fix is a new guard rather than a regression close |

## Where 🔴 I came from, and the axis that was missing

🔴 I is not the reviewer's. It came from a security pass the orchestrator ran
after this round closed, prompted by the repository owner asking why security
was not among the corrections being discussed. It is recorded here rather than
in a round of its own because it sits in `place()`, which this round's 🟡 F
already reopens, and because a finding's provenance belongs beside the
findings it will be fixed with.

**The reason it was not found earlier is structural, and it is worth more than
the finding.** `code-review` names security in stage 2, but the comparison
axes table — the thing that makes an axis mandatory — has no security row.
Neither round 4 nor round 5 named one for itself either, though the skill's
own *"floor, not a ceiling"* paragraph asks each round to. Three of this
round's four 🔴 have a security frame stronger than the frame they were given:
🔴 B is a fail-open in a repository that maintains
`tests/test_gates_do_not_fail_open.py` for exactly that failure, whose scope is
one mechanism narrower than the defect; 🔴 D's accepted fix reverses a write
boundary's symlink behaviour; 🔴 A is path confusion. The axis would have
gathered all four.

Disclosure is the orchestrator's and is deliberately not a public issue while
the fix is unreleased: the repository is public, carries no security policy,
and private vulnerability reporting is disabled. The severity that justifies
that pace rather than a faster one is written into the changelog entry.

## Round 4's three deferrals, and its one ❓

- **`README.ko.md`** — the rewritten section matches the code: the
  `path#unit@hash` form, BROKEN → 2 and DRIFTED → 1, `--reverify`'s role, and
  the degrade-to-DRIFTED sentence. Line 149 goes to 🟡 H. A mid-sentence line
  break near 138 is typesetting, 🟢.
- **`.specseal/map.md`, row by row** — the branch's changed files were crossed
  against the nine files the 29 rows cite. They overlap at `agents/warden.md`
  alone, whose branch change is one table row inside `## Role`; no row cites
  that line, all three cite other sentences. The remaining eight files this
  branch never touched. **The `49 ok` no longer stands in for anything.** In
  the work item's own 20-row fragment one Verified cell is stale — the `ast`
  row still says an unparseable file yields no symbols rather than a false
  match, where it now returns `None` and `resolve` falls through. 🟢, one
  sentence.
- **`templates/sdd-plan.md` · `templates/specseal-README.md`, 14 lines** —
  both match the code. One loss: the `map/<work-item-id>.md` description
  dropped `no header`, which `CLAUDE.md` still states. 🟢.
- **❓ `dirty()` on Windows** — the defensive fix is in at
  `hooks/ledger-migrate.py:115` and reads correctly: `os.sep` is `\` there,
  `os.path.relpath` answers with it, and `.replace(os.sep, "/")` makes the
  pathspec forward-slashed; `ledgers(root)` only builds paths under root, so
  no `..` or drive letter can enter. **This is not a claim that the Windows
  leg passes** — what git accepts is the broad gate's windows leg to answer,
  and this round ran on macOS only.

## Recorded without a fix (🟢)

- A short-name anchor on a nested `def` regressed: `resolve("m.py","inner",…)`
  was `[(2,3)]` and is now `[]`, because `py_spans` holds `outer.inner` alone.
  The anchor format is unreleased, so there is no victim, and `--reverify`
  heals it — but Known limits records neither the change nor the remedy.
- A multi-line constant's span grew by one line and its hash changed with it,
  so an unchanged constant flips OK → DRIFTED. All three constants here are
  one-liners and the format is unreleased; the exposure opens the day a cited
  constant becomes multi-line.
- Finding 7's wording change has no pin (mutation-verified above).
- Finding 13's straggler at `specs/…/plan.md:69`.
- `overview.md:337` still lists the `git log -L` cost question as unverified;
  the mechanism it asks about was removed in this span.
- The ledger fragment `.specseal/map/1788229400-….md` has one table row
  separated from its table by a blank line, so it does not render as a table.
  It predates this round and the checker is unaffected.

## Executed probes

The repository's real ledgers at `49 ok · 0 drifted · 0 broken · 0 external ·
0 old-format`, exit 0. The six test files touching the changed code, 168 cases,
all passing. Twelve mutations against the twelve new pins, 12 killed. The
reproduction recipes for findings 1-10 and 14. Twelve side-by-side comparisons
of the old and new modules on identical input for `resolve` and
`generic_units`. Two advisor runs through `dispatch.py post-bash`. The
reproductions for 🔴 A, B, C, D and 🟡 F, G. The reviewer's two suggested
patches applied together: ten language shapes verified and 114 cases passing
across four files. `ruff check` and `ruff format --check`, clean.

Everything ran in a scratchpad tree. The working tree stayed clean at
`0a60d52` and the reviewer wrote no record.

## Deferred

Nothing. Every finding this round opened is in the table above with a home;
the eight 🟢 entries are recorded here rather than carried, and 🔴 C's
structure signal is written as Q2 in `questions.md`, which the PR body names.
