# 1791384156-config-rows-coordinates-and-headings-have-one-reader — overview

`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here.

📋 implement applied
· spec:     this work item's `handoff.md`, `spec.md`, `plan.md`, `questions.md`; `docs/the-pact.md` §*How a signer names the pact*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `templates/config.md` §*The ledger freeze*; `CONTRIBUTING.md` §*What a change to a gate must carry* (direction and prompt budget, stated per phase)
· evidence: `seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md` — K1–K25 for the new units, nine `Corrected ·` rows (0.9.1 S7–S10 and S1, 0.15.3 F5 and F1, 0.11.4's two rows, 0.15.0 A6 and A7, 0.8.1 R7), and 61 `Re-read ·` rows written by `--reverify --into` after each cited claim was read
· verified: executed — every new case seen red against 5623d728 (or the earlier phase's code) and green after, `bin/mutation-check` on every added unit, each phase's touched modules, the eight suite-wide guard modules the orchestrator named, `bin/evidence-check --strict .` (0 drifted, 0 broken, 0 refused), `bin/correction-check --range origin/release/v0.21.0...HEAD` (exit 0), `uvx ruff check` and `uvx ruff format --check` on the changed files; measured by probes, deleted: the grammar's compiled patterns, `correction-check`'s identities over the released ledgers, `settle`'s 8,218 spans, the heading rule against markdown-it over 777 tracked `.md` files and 3,000 generated documents. Read — each drifted released row's claim. Unverified — the full suite (the sealer's)

## Why this work exists

Three formats the repository owns — a `seal/config.md` row, the ledger
coordinate and a markdown heading — were each read by several copies that
answered one file differently; each now has one reader, so a doubled row, an
unreadable config, a fenced `##` and a `#NNN`-led line get one answer
everywhere.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which phase built `seal mode`'s refusal | `plan.md` phase 2: "`seal.py#table_span`/`with_row` refusing two `Mode` rows naming both lines" / built in phase 1 | phase 1 | `seal.py` re-exports `declared_mode`, and its report fell through to the *they disagree* arm on the new `refused` kind the moment phase 1 landed; splitting it would have left a commit whose `seal mode` misreports |
| An unreadable `config.md` under `seal mode` | S2c of #104 (`tests/test_the_mode_is_a_row_and_a_command.py::test_a_row_that_cannot_be_written_still_reports`): exit 0, *could not be written* / exit 2, the path named, the folder still reported | exit 2 | `spec.md` §*Scope* 1: "a command a person runs (… `seal mode` …) prints it and exits 2 with nothing judged". The case's own reason — the report does not need the write — still holds: the folder line is printed |
| Two `Mode` rows under `seal mode` | round 1 🟡 5 of #104 (`test_two_mode_rows_converge`, NAME NOT IN TREE since phase 1): two runs reach agreement by setting the first row / refused, both lines named | refused | `spec.md` S2; and `docs/the-pact.md` §*How a signer names the pact*: "a row written twice, has no value at all: its first row is not the answer" |
| Which readers of the freeze refuse | `plan.md` phase 2 names `frozen_from`, `cutoff_at` and the commands / `settle.py#anchored_rows` and `hooks/evidence-advisor.py#main` read `frozen_from` too | both read a refusal as frozen | `spec.md` §*What this delivers*: "The freeze arm never turns off because the file could not be read." Neither refuses (a guard that only advises, and a hook) |
| How many identities `correction-check` gains and loses | `plan.md` phase 3: "gains an identity for two released rows and loses nine MALFORMED-shaped ones" / measured per row: 58 gained, 5 lost, 47 rows keyed whole | the measurement | the frame counted coordinate spans; per row identity the old pattern's `[^`@|]` also refused 56 quoted locators holding a code span or `\|` (`phases/phase-3.md`) |
| What S12's coordinate grep finds | `spec.md` S12: nothing outside `evidence_check.py` / `pact_check.py#CHANGE_RE` | exempted by name | it reads a pact review's `<work-item-id>@<content hash>`, a record id and no coordinate |
| What `evidence-check` refuses on | `spec.md` S1, S3: "`evidence-check` … exits 2" / only `--reverify` refuses | `--reverify` | the plain check reads no config row at all; refusing it on a config it does not read would stop every CI run on an unrelated file |
| Where the property case lives | `spec.md` S10: "a property case beside `tests/test_the_hooks_hide_what_a_renderer_hides.py`" / `tests/test_one_heading_rule_holds_to_commonmark.py` | a module of its own | it reads one rule against one oracle function and has three corpora of its own; the module the spec names holds the hide property, and its own case pins the oracle's imports, which this leaves unchanged |
| What the property compares | `spec.md` S10: "its answer equals markdown-it's ATX heading set for the document" / equal on every shown line except a heading indented one to three spaces under a list item | the stated limit | a rule that reads one line cannot see the list item above it; the module names the limit, counts it in the generated corpus, and requires the tree to hold none (`phases/phase-4.md`) |
| What S12's heading grep finds | `spec.md` S12: nothing outside the rule, its twin, the slugger and the walker / also the fold's and the changelog's `## X.Y.Z` lines, the fold's demotion of a fragment's headings, the three paragraph-end block lists, and YAML and Python comments | exempted by name, each with its reason | all but the demotion are out of scope by `spec.md` §*Scope*'s Out list or are no markdown at all; the demotion is under §*Not done* |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, spawned by the orchestrator after the review rounds settle |
| The unreadable fixtures (a directory named `config.md`, bytes that do not decode as UTF-8) on Linux and the Windows shards | CI at the pull request |

## Not done

**`spec.md` §*What this delivers* says more than the checker does** (round 1,
⬜ 8). Its statement reads "A markdown heading is CommonMark's ATX heading,
read where a renderer shows it". The checker's shown lines are
`markdown_lines`, which blank closed fences and nothing else, so a `## B`
inside an HTML block or a multi-line comment still opens a section there,
where a renderer shows none; round 1 executed both shapes. The tree holds
neither shape (0 and 0, the round's probe). Which lines a reader hides before
it asks the heading rule is the live-line family #872 holds, so the mechanism
is left to it, and the sentence in `spec.md`, the framer's file, stands with
this paragraph as its limit until #872 decides.

`reference_roots` reads a refusal as the default rather than refusing: its
callers, `unverified-check` and the survivor sweep, are not among the commands
`spec.md` names as refusing, and the default is what an unreadable file always
read there.

`.github/scripts/fold_ledger.py#demote` still reads a fragment's headings by
`^(#{1,6})\s` to push them two levels down at the release. It is a reader of
a markdown heading, but it rewrites bytes the release ships, and moving it
onto the one rule changes what the fold writes for a heading indented one to
three spaces; no fragment in the tree holds one. That is a change to the
release's output with its own argument, so it is left, exempted by name in
`tests/test_a_format_has_one_reader.py`, and stated here for the review.

`unverified_check.py#readable` blanks 41 lines in 15 tracked `.md` files that
markdown-it shows as headings — files that quote fences inside code spans.
That is which lines a reader hides, the family #872 holds (the seven
live-line rules), not the heading rule, so it is left to that issue.

The two formats the issue named and this work did not build are filed:
`seal/config.md`'s own table grammar against the GFM walker as #871, and the
seven live-line rules as #872.

## Fed back into the spec

- Inferred during implementation: `settle` and the commit advisor read a
  refused freeze row as frozen (fragment row K12).
- Inferred during implementation: `correction-check` reads `seal/config.md` at
  a commit with `git cat-file`, so a tree or an undecodable blob there is
  refused naming the cause (fragment row K9).
- Inferred during implementation: a `Corrected ·` row's citation is read from
  its Code grounds cell, never from the claim (fragment row K15).
- Inferred during implementation: a heading indented under a list item is the
  item's, and the one rule, reading one line, does not see it; the tree holds
  none (fragment row K20).
