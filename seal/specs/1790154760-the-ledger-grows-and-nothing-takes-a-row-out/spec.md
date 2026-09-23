# Feature Specification: the ledger grows, and what its size actually costs (#519)

<!-- seal/specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out/spec.md -->

#519 asked for three measurements before any design, and allowed the answer
that nothing should change. The measurements below were taken while framing.
They say the ledger's size costs something now, but the cost does not come
from the row count. It comes from the checker parsing the same Python file
once per row. So this work takes no row out of the ledger. It makes the
checker parse each file once, and it corrects the one document that states
what the check costs.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*Repo rule — commit early; on a declared branch it costs nothing* and `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | A row leaves the ledger only when the code it cites goes (REMOVED, never re-pointed). No rule lets a row be dropped because it is old or because `docs/` now states a related rule, so a "ledger settle" would need a new policy, not an implementation |
| `docs/the-evidence-ledger.md` §*A row is a content anchor* — *A work item whose ledger fragment still exists has not shipped* | `seal/ledger/*.md` means "unshipped work item" to `evidence_check.py#unshipped`. Splitting released sections into files under that glob would give the directory a second meaning. This is why the split candidate is rejected (plan, Alternatives) |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped* | `correction_check.py` reads the `Corrected <date>` / `Re-read <date>` markers inside rows. Rewriting or trimming a row's Notes cell would remove what that check reads, so the Notes cell is out of scope |
| `docs/the-evidence-ledger.md` §*A correction a merge dropped* — *A bound over the corpus is stated with its instrument and the moment it was taken* | The advisor's cost claim ("about 114 ms") has no instrument and no date, and it is now wrong by 138×. The corrected sentence must name how the number was taken and when |
| `skills/implement/SKILL.md` §3, top rung — *a value someone waits on* | The latency of every `git commit` in an opted-in repository (the PostToolUse advisor) is such a value. Naming it is what puts this work on the rung that needs this spec |
| `skills/agent-contract/SKILL.md` §14 and §15 | The docstring sentence a person reads is changed in the same commit as the behaviour, and a case pins the behaviour |

## Measurements taken while framing

All **executed** on the worktree at `44d5cbba` (f8f1c9de plus `routing.md`),
Python 3.12.11, macOS, 2026-09-23. Scripts are in the framer's scratchpad
and are not committed: `m_time.py`, `m_memo.py`, `m_rows.py`, `m_cols.py`,
`m_git.py`, `m_overlap.py`. Each is described well enough below to rerun.

### 1. How much of the ledger is still load-bearing

| Reading | Value | How taken |
|---|---|---|
| `seal/ledger.md` size | 1,211,115 bytes, 2,546 lines | `wc` |
| Table rows / rows with at least one anchor | 683 / 662 | line scan |
| Anchors (all / unique `(coord, hash)`) | 1,878 / 1,468 | `ec.ANCHOR_RE` over the file |
| `evidence_check.py --strict .` | 1,468 ok · 0 drifted · 0 broken (plus 8 ok in the one fragment) | run, exit 0 |
| Rows carrying a `Corrected`/`Re-read` marker | 234 (35 %) | regex |
| Rows whose `Checked` date is later than their release | 158 | date compare |
| Rows under a work-item marker whose work item is folded into `docs/` | 642 of 642 (89 work items, 1,066 KB) | marker set in `docs/*.md` |
| Rows anchored into a `seal/specs/` directory | 1 | anchor path prefix |
| Where the bytes are, by column | Notes 48 % · Verified behaviour 23 % · Code grounds 15 % · Clause 13 % · Checked 1 % | backtick-aware cell split, 670 five-cell rows |
| Mean / largest row | 1,639 / 10,579 bytes | line length |

Every anchor resolves and none has drifted, so by the checker's own reading
every row is still load-bearing. Nothing measured here marks a row as dead.
Whether anybody reads a row again is not measurable from the tree, and this
frame does not claim it.

### 2. What row count does to run time, and to conflicts

| Reading | Value | How taken |
|---|---|---|
| `evidence_check.py --strict .`, wall time | 15.78 / 15.88 / 15.83 s | `/usr/bin/time -p`, three runs |
| Ledger arm alone / records arm alone | 15.10 s / 0.23 s | in-process timing |
| Ledger arm vs size | first 25 % of lines 2.64 s · 50 % 5.94 s · 75 % 10.18 s · 100 % 15.08 s | `check_text` over prefixes |
| Where the time goes | `py_spans` called 1,328 times for 126 distinct `.py` files; `ast.parse` + walk is ~94 % of the profile | `cProfile` |
| Same run with `py_spans` memoised by file text | 1.81 s, 126 parses, findings identical to the unmemoised run | probe, monkeypatch |
| At 4× the rows (each anchor repeated with a shifted hash) | memoised 4.59 s · unmemoised 61.81 s | probe |
| `hooks/evidence-advisor.py` on a `git commit` payload | 15.73 / 15.74 s (this tree), 15.91 s (installed 0.13.2 copy) | `/usr/bin/time -p` |
| The advisor's own docstring | "about 114 ms", written 2026-09-01 (`117d37fe`) | read |
| Callers paying the full check | the advisor at every `git commit` (PostToolUse, synchronous), the `ledger` CI job, `broad_gate.py`'s `LEDGER` check with `--strict`, and `rider_check.py` through `py_spans` | read |
| Session-start hooks | `ledger-migrate.py` 0.32 s; it reads `old_format_rows` only | timed |

**The cost is now, and it is paid at every commit.** It grows linearly with
the number of unique anchors, but only because each anchor re-parses its
file. With the parse done once per file, the same ledger costs 1.8 s and a
ledger four times larger costs 4.6 s.

| Reading | Value | How taken |
|---|---|---|
| Non-merge commits touching `seal/ledger.md` since 0.5.0 | 97 | `git log` |
| Of them, release/fold commits | +1,843 / −68 lines | `--numstat`, subject match |
| Of them, other commits (65) — corrections, removals, re-reads | +627 / −579 lines | `--numstat` |
| Merge commits touching `seal/ledger.md`, all refs | 4, all hand-resolved (`diff-tree --cc` non-empty), all on 2026-09-22, all merging `release/v0.13.1` into a feature branch | `git log --merges --all` |
| Conflict hunks in those four | 3, 1, 1, 2 | `@@@` count |

Conflicts come from branches editing existing rows in place, which the
rules allow (a removal or a correction must touch the shared file). A larger
file does not make two such edits land in the same hunk more often. Nothing
measured ties the conflict rate to row count. The size does make a
hand resolution longer to read, and that is not measured here.

### 3. Whether the release sections repeat what `docs/` now states

| Reading | Value | How taken |
|---|---|---|
| Work items with a fold marker in `docs/` | 90 | marker scan of `docs/*.md` |
| Share of a row's Clause words (≥ 5 letters) found in the `docs/` paragraphs folded from the same work item | p25 0.10 · median 0.21 · p75 0.40 · p90 0.60 | `m_overlap.py` |
| Rows at ≥ 0.8 / below 0.4 | 30 / 492 of 658 | same |

This instrument is crude: word overlap is neither paraphrase nor
contradiction. It is enough to say the two mostly do not repeat each other.
A `docs/` statement is a rule. A row is the evidence that one unit of code or
one test holds it, and 71 % of a row's bytes are the Verified behaviour and
Notes cells, which no policy sentence carries. Compressing rows to their
anchor would drop that evidence and keep almost nothing that `docs/` holds.

## Scope

**In:**

1. `skills/evidence-check/scripts/evidence_check.py` parses each Python file
   at most once per process: `py_spans` (or the one place that calls it per
   row) is memoised on the file's text, so a file that changed between two
   reads is never served stale spans. Every finding the checker prints stays
   byte-identical on this tree. `rider_check.py` and every other caller of
   `py_spans` get the benefit without changes of their own.
2. The advisor's module docstring (`hooks/evidence-advisor.py`) states the
   measured cost, with the instrument and the date, in place of "about 114 ms".
3. A case pinning the property: one ledger citing one `.py` file through
   several rows costs one parse. It must be seen red against the current code
   (contract §15).
4. The work item's changelog fragment and ledger fragment, and re-reading the
   shared-ledger rows the edit drifts: `evidence_check.py#py_spans@4045ba55`
   (1 row) at minimum, plus any row on a unit phase 1 actually changes.

**Out, and why:**

- **Removing, compressing or splitting ledger rows.** The measurements give
  no row a reason to leave. All anchors hold, and the docs overlap is low.
  The rules allow a row to leave only with its code. A new retirement rule
  would be a policy change nobody has asked for with evidence.
- **Splitting release sections into files.** `seal/ledger/*.md` already means
  "unshipped", and the checker reads every file anyway, so a split saves no
  time.
- **Trimming the Notes cells (48 % of the bytes).** `correction_check.py`
  reads the markers inside them. A trim is its own design, and whoever wants
  it answers it.
- **Memoising the markdown resolvers.** 136 non-Python rows, and they are not
  where the time goes. Phase 1 records what the remaining 1.8 s is spent on,
  so a later item can start from a number.
- **Conflict resolution guidance.** #509 carries it.
- **`seal/follow-up.md`'s first row** (malformed coordinates are ignored). It
  is a different behaviour of the same checker, and this work is not its
  prerequisite.
- **Any timing assertion in the suite.** A wall-clock bound in a test is
  flaky across machines. The pinned property is the parse count, and the
  timing is recorded as a measurement.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A session commits in this repository | Given this tree's ledger, when the advisor runs on a `git commit` payload, then it finishes in a small fraction of today's 15.7 s (framing probe: about 1.8 s), and prints exactly what it printed before | executed: time the advisor as in §2 before and after, and diff its output on a tree with one deliberately broken anchor |
| CI and the broad gate read the ledger | Given this tree, when `evidence_check.py --strict .` runs, then its full output is byte-identical to the unmemoised run and exit code is unchanged | executed: diff of the two outputs, `; echo $?` read directly |
| A ledger cites one Python file many times | Given a fixture ledger with N rows anchored in one `.py` file, when the checker runs, then that file is parsed once | new case, shown red against the unmemoised code |
| A file changes between two reads in one process | Given `py_spans` called on text A then on edited text B, then B's spans are returned, never A's | a case, or the memo key is the text itself and the case above shows it (the work decides; see `questions.md` Q2) |
| A person reads the advisor's cost claim | Given `hooks/evidence-advisor.py`, when its docstring states a cost, then the sentence names the number, how it was taken and the date | read in review |

## Data & interfaces

No interface changes. `py_spans(text)` keeps its signature and its
`None`-for-SyntaxError contract. Output of every command is unchanged. The
rows that grade DRIFTED after the edit are named in Scope item 4, and they
are re-read, not re-pointed.

## Open questions → questions.md

Framed 2026-09-23 by framer, before the build.
