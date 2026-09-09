# 1788936260-a-case-pins-what-it-actually-measures — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `8d53ca4` |
| Ran by | unknown — the spawn prompt carried no `Ran by` value, and this row is the spawning session's rather than the segment's own; the orchestrator fills it |

## What this phase was asked

The run over `hooks/review-history-guard.py`, its count recorded, and the
fragments — the changelog entry to
`seal/specs/1788936260-a-case-pins-what-it-actually-measures/changelog.md` and
the ledger rows to
`seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md`, never
`CHANGELOG.md` or `seal/ledger.md`.

## What this phase found

**The run, in full.** `arm-check hooks/review-history-guard.py --tests
"bin/test tests/test_chain_hooks.py -q"`, 64 mutations, module restored from
held bytes and sha256-compared after every one, exit 0 (report-only).

| | Arms | Asked | Killed | Survived |
|---|---|---|---|---|
| `invert` | 32 | 32 | 31 | **1** |
| `remove` | 32 | 32 | 20 | **12** |
| combined — watched by any operator | 32 | — | 31 | **1** |

Per scope: `reader` 5 · `is_closed` 4 · `gh_segments` 5 · `main` 17 ·
`<module>` 1.

**The one arm nothing notices at all** is `main:189`, the `except Exception`
around `json.load(sys.stdin)`. No case in `tests/test_chain_hooks.py` feeds
the hook malformed stdin. Reported, not called a defect: whether it wants a
case is `questions.md` Q2, which `spec.md` puts out of scope.

**The twelve `remove` survivors, which is the row #262's nine compares with:**

| Where | Arm |
|---|---|
| `reader:96` | `spec.loader is None` (2/2) |
| `main:189` | `except Exception` |
| `main:191` | `payload.get("tool_name") != "Bash"` |
| `main:195` | `not segs` |
| `main:208` | `not top` (1/2) |
| `main:208` | `not optin.opted_in(cwd)` (2/2) |
| `main:212` | `not item` |
| `main:233` | `strays` |
| `main:252` | `unreadable` |
| `main:265` | `not strays` (2/3) · `not unreadable` (3/3) |
| `main:278` | `records` (1/2) |

Ten of the twelve are in `main`, which is where #262 put eight of its nine.
Two of the twelve are the ones #262 names as **behaviour-preserving rather
than gaps** — the opt-in halves at `main:208`, whose removal makes a globally
installed plugin nag unrelated repositories, are precisely the arms the ticket
says a case cannot construct without the hook being installed globally.
`gh_segments` now has **none**, which agrees with the ticket: four of its arms
were closed under one parametrized case on #209 · #210's branch.

**12 against the ticket's 9, and the difference is the ticket's own
argument.** The file changed twice after that measurement (`341be0b`,
`1dedd1e`), and the nine was itself thirteen before four were closed. The
ticket's table is left exactly as written (`questions.md` assumption 3): it
was true when measured, and correcting a shipped measurement would hide the
argument it makes. Both numbers are recorded in the ledger fragment, beside
the run that produced each.

**Q1 — the exit code — is unanswered and the code is the first of its three
answers: report-only, exit 0 whether or not an arm survived.** That is now a
number rather than a guess, which is what the question was waiting for: a
gate on any survivor would fail on 1 arm under `invert` and 12 under
`remove`, and a baseline gate has a baseline to record. Pinned by
`test_the_checker_is_report_only_and_exits_zero_over_the_real_module`, so
whichever answer the owner gives arrives as a decision somebody makes rather
than an edit that slips through.

**Writing the ledger fragment found a fourth silent-drop.** Four anchors were
written as bare `#unit@hash` with no path — a continuation of the anchor
before them, which reads naturally and is not what the checker parses. It
produced **no row at all** for them: `evidence-check` reported 12 anchors for
6 rows, silently, and only counting them by hand against what I had written
caught it. That is the failure mode already sitting in `seal/follow-up.md`
with the repository owner — a malformed coordinate removes the claim from the
ledger instead of drifting or breaking — met from the writing side rather
than the reading side. Fixed here by giving each its full path; all 15 anchors
now resolve and `evidence-check .` reports `1056 ok · 0 drifted · 0 broken`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
