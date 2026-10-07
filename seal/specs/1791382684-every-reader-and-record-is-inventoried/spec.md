# Feature Specification: every reader and record is inventoried (#834)

<!-- seal/specs/1791382684-every-reader-and-record-is-inventoried/spec.md -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #834 §*What the inventory is* | the two tables (readers with an input class, record mechanisms with what drifts them and who re-reads them) and the evidence column, counted from the tracker |
| #834 §*Start here* | the table changes no code; each decision it leads to is its own issue |
| `CLAUDE.md` §*The goal a design is chosen against* | the decisions are weighed for a run that verifies unattended |

## Scope

**In.** The inventory, taken against 5623d728 (0.20.0 as shipped), is committed
under `inventory/` in this directory:

| Part | File | What it covers | Rows |
|---|---|---|---|
| 1 | `inventory/1-hooks-shell.md` | hooks that read shell command text: `cmdline`, `cmdline_base`, `tokens`, `one_heredoc`, `worktree-guard`, `worktree_consent`, `commitgate`, `commit-review-gate`, `gate`, `dispatch` | 144 readers |
| 2 | `inventory/2-hooks-rest.md` | every other hook, `hooks/git/*`, the payload fields each hook reads | 113 readers |
| 3 | `inventory/3-review-chain.md` | `chain_check`, `round_record`, `survivor_check` | 130 readers |
| 4 | `inventory/4-ledger-settle-seal.md` | `evidence_check`, `correction_check`, `pact_check`, `settle`, `fold_check`, `seal` | 159 readers |
| 5 | `inventory/5-verify-bin-ci.md` | `skills/verify/scripts/*`, `bin/`, the shell steps of `.github/workflows/*` | 136 readers |
| 6 | `inventory/6-tests.md` | the tests that read the tree's own text, and the four helper modules | 785 readers |
| 7 | `inventory/7-records.md` | record mechanisms, and what each cost in rows and lines since 0.18.0 | 35 mechanisms |
| 8 | `inventory/8-evidence.md` | the 63 issues since 0.18.0, by family and by file | 63 issues |

Each part was taken by one read-only agent from the code itself. Probes that
were executed are marked as executed in their row, and every other row is
`read`. The row counts are each part's own. A parse of the `Class` column
reads 1,381 of the 1,467 reader rows; the rest wrap or quote a pipe.

**Out.** No code changes here. The table's permanent home under `docs/`, and the
check that reads it as a registry, are decided by #835's frame (its rule 1 says
the table becomes the registry the test reads). The build of this item waits
for that frame and then moves the table into the home it names.

## What the table says

### Input class by part

Read from the `Class` column (parsed rows, see above).

| Part | owned | observed | guess | unknown passed |
|---|---|---|---|---|
| 1 shell-reading hooks | 18 | 25 | 98 | 64 |
| 2 other hooks | 33 | 51 | 20 | 63 |
| 3 review chain | 74 | 30 | 21 | 68 |
| 4 ledger, settle, seal | 73 | 52 | 28 | 76 |
| 5 verify, bin, CI | 43 | 49 | 39 | 82 |
| 6 tests | 125 | 94 | 508 | 101 |

### Families since 0.18.0

From part 8. *Reopened* counts issues that are a new shape of a defect another
issue in the window had just fixed.

| Family | Issues | Guess | Reopened | Converged? |
|---|---|---|---|---|
| reverify judgment and order | 10 | 0 | 5 | no issue since #829, a window of about 1.5 days |
| broad-gate run attribution | 8 | 8 | 6 | no issue since #846; the defect moved to the recorder's record (#849, #852) |
| worktree-guard shell prediction | 6 | 6 | 4 | no: #854 and #856 after #850's redesign |
| pact markdown reader | 5 | 0 | 4 | the `Pact` row reader yes (#793); the compat reader and the sweep's span no (#844) |
| heredoc body as data | 3 | 3 | 2 | yes, after one exact shape (`hooks/one_heredoc.py`) and the copies removed (#803) |
| records sentence vs code | 3 | 0 | 1 | — |
| fix-range walk over merges | 2 | 0 | 1 | no: #805, #860 open |

What converged read an owned format or an observed fact and refused the
unknown. What did not converge read someone else's text and let the unknown
through, which is #834's own observation, now with the table's counts under it.

### What the table found besides

- **One judgment in several places, disagreeing.** This is the shape #824 ended for one
  ledger row, and it is still present:
  - `Needs a fix` is read three ways (part 3 rows 47, 61; part 5 row 36), and a
    deferred finding's home four ways.
  - `seal/config.md`'s duplicate rows are read first-wins in one place and last-wins
    in another, and an unreadable file gets four answers (part 4 E47, C17, F12, X16).
  - The ledger coordinate grammar is written five times (part 4).
  - The guard and the consent writer pick different directories for one creation
    (part 1 row 127, executed).
  - The `claude` process is found by a substring test in one hook and by an exact
    match in another (part 2 rows 9, 14).
- **Record bookkeeping outweighs claims.** 84% of the ledger rows landed since
  0.18.0 are `Re-read ·` or `Corrected ·` (part 7). `# RIDER:` comments, one stamp
  each with no families, held at 20 with 0 drifted.
- **Guesses where an observed source exists.** The broad gate's panel counts
  still come from pytest's printed summary (part 5 row 26). Units outside Python
  are bounded by indentation (part 4 E17, probe executed).
- **The tests read prose.** 508 of the 727 parsed test rows are guesses. The largest
  cell is a sentence pinned verbatim, and the pin files grew most:
  `test_the_seal_is_taken_once_by_the_sealer.py` went from 5,883 to 9,934 lines
  (part 6).

## Decisions taken from the table

Each is its own issue in milestone `release: 0.21.0`. The three drafted on
2026-10-06 are reopened, each with a comment carrying the table's grounds.

| Issue | Decision | Grounds in the table |
|---|---|---|
| #835 (reopened) | a reader declares its input class; a new mechanism names one it removes | the class counts above; the converged/not-converged split |
| #836 (reopened) | a ledger row's claim is the test that enforces it | part 7: 84% bookkeeping rows; a re-read anchors on the unit it re-read |
| #837 (reopened) | a records-level finding closes once at the run's end | part 8: 18 of 33 review-filed issues from a capped run's last round or its check |
| #866 | a round-record cell has one reader | part 3, part 5: `Needs a fix`, deferred home, `Location`, draft state, the floor's two walks |
| #867 | `seal/config.md`, the coordinate and a heading have one reader each | part 4, part 2: duplicate and unreadable answers, five coordinate grammars, four heading rules |
| #868 | the hooks place a creation, find the session, read the waiver and take a failed git call one way | parts 1 and 2, one executed |
| #869 | the broad gate reads its counts from the recorder | part 5 rows 26, 31, and the mark-file traceback; with #852 |
| #870 | a unit the extractor cannot bound is refused, not guessed | part 4 E17 and E18, probe executed; takes #848 |

## User scenarios & acceptance

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A reader asks what a reader reads | Given the inventory, when they look up a unit, then its row gives file, unit, what it reads, class, unknown input and copies | open `inventory/<part>.md` |
| A reader asks what keeps costing | Given part 8, when they sort by family, then the issues and reopenings per family are counted with their numbers | `inventory/8-evidence.md` §*Counts by family* |
| A decision cites its ground | Given an issue from the table above, when it is opened, then it names the part and row it rests on | the issue bodies |

## Data & interfaces

None. The table is a record. Its schema is the column set each part states at
its head.

Framed 2026-10-07 by the session, before the build.
