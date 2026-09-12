# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `9a010fd` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope

Issue #359 — a squash into a release branch labels what it answered, and a
release pull request is refused while its milestone claims work the release
has not got. Nine commits, `ae0d276` through `9a010fd`, on the frame commits
`a01d679` and `fe2c3bc`.

Two new modules, two new `.github/scripts`, one new workflow, one edited
workflow, three edited documents.

## Facts, with labels

**Executed by the orchestrating session** at `9a010fd`, exit codes read
directly with no pipe:

- `bin/test -q` over `tests/test_a_merged_ticket_says_so_on_the_tracker.py`,
  `tests/test_a_release_cannot_ship_an_untrue_milestone.py`,
  `tests/test_ci_gives_the_checks_what_they_need.py`,
  `tests/test_one_word_one_meaning.py`, `tests/test_docs_line_wrap.py`,
  `tests/test_release_hygiene.py`, `tests/test_no_real_identifiers.py`,
  `tests/test_the_rules_have_one_owner.py` → **165 passed, exit 0**.
- `uvx ruff check` and `uvx ruff format --check` over the four changed Python
  files → **exit 0** each.

**Executed by the builder**, its own numbers, in `overview.md`: 306 cases
across 13 modules; the gate run four ways against the live tracker including
a real refusal naming #359; **19 mutations each seen red**, one of which
found a weak case of its own; `survivor-check`, `unverified-check` and
`evidence-check --strict` (1137 rows) each exit 0. Re-derive rather than
inherit — in particular the mutation count and the claim that each was seen
red.

**Executed, and it is the reason phase 3's step is shaped as it is** —
`gh issue list --milestone "release: 9.9.9" --state open` returns `[]` and
**exits 0**. A mistyped or absent milestone would otherwise make the gate
pass by measuring an empty set.

**Read** — the frame said `hygiene.yml` holds four release-only steps each
opening with the same guard. Three do; the fourth opens with the inverted
guard and skips on `main`. The builder recorded this as a frame divergence.

**Read, and it constrains every document edit** — `tests/test_release_hygiene.py`'s
`LOADED` includes `docs/`, so a real version in prose goes red at the release
preparation commit. `.github/` is outside `LOADED`.

**Unverified, and both are rows in `## Not verified`** — whether the workflow
token's `issues: write` covers label *creation*, and whether the signal fires
as specified. Both need a real run on a release branch, which this branch's
own squash produces. Do not try to settle them by writing to the tracker.

**Unverified** — the broad gate. It is the `sealer`'s, after this chain
settles.

## Two answers a person gave, which are not yours to reopen

**Q1 — (c).** `L \ D` fails, `D \ L` reports. Judge whether the code does
that, not whether it is the right answer.

**Q2 — (a), already done.** `release: 0.11.1` holds #351 and #359 alone. The
frame's `plan.md` and `questions.md` say nine at `a01d679`; that was true
then and the move happened after. A note in those files that reads as stale
is a correction, not a defect of the build.

## Where a claim flips on measurement point

The gate's refusal set is `M \ D` — the milestone's open issues minus what
the release branch carries — and `D` is recomputed from the branch's commits
rather than read from labels. Measuring the gate against labels instead
reproduces the defect the design rejects. Measure at the commits.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `bin/evidence-check --strict`,
never narrowed to this work item's fragment.
`bin/survivor-check --range origin/release/v0.11.1...HEAD` — the builder
reports no survivors and therefore no `survivors.md`; check that.
