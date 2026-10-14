# Feature Specification: every test file is cut to what it guards

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here asks a person. Every removal is proven by a run (`mutation-check`), every kept case by the `cases` job, every row by `budget_check.py` |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | No gate is added. Each batch changes what three gates measure (the rows, the frozen list, `.test_durations`) and a case it plants is seen red first (`skills/agent-contract/SKILL.md` §15) |
| `docs/the-evidence-ledger.md` §*A claim held by a test*; §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | A removed function a released row cites gets a `Corrected ·` row, a moved one a `Re-read ·` row, in `seal/ledger/1791934662-….md`; the changelog goes to the fragment; no released file changes |
| `docs/the-reader-registry.md` §*A frame names what its work removes* | `## Removes` below; a removal a phase makes that the frame did not name is a divergence in `overview.md` |
| #929's `seal/specs/1791876666-…/spec.md` §*A case names what it guards*, §*The removal criterion*, §*The regrowth check*, §*Rows for seal/budgets.md* (cc4ab070) | The method, applied unchanged: one `Kills:` line per function; a removal is proven by a mutation table and never judged; `case_check.py` proves a new or changed function; `tests/unguarded-files.txt` only shrinks; the five rows. Where this item wants the method different it writes a row in `questions.md` for #929's smith |
| #930's `seal/specs/1791876665-…/spec.md` §*The budgets* (661dc60b) | The ratchet: `measured ≤ ceiling ≤ measured × (1 + slack)`; a lowering lands in the same pull request as the cut |
| #931's `test.yml` `durations` job (a8335041) | A cut pull request downloads its run's union (`gh run download <id> -n test-durations`) and commits it, so `suite-seconds` and `slow-file:*` fall with the cut |
| #923's `seal/specs/1791933022-…/spec.md` §*The boundary with #929* (6969c487) | A case that asserts on this tree's prose moves with the text and is not removed or re-pointed here |
| `skills/implement/SKILL.md` §*3. The SDD file set* | The rows' ceilings and the frozen list are values a contributor is limited by, which is the top rung |

## Scope

**In.** Every test file #929's phases do not open — 180 of 185 — cut to the cases that guard something, in batches, each batch one pull request into `release/v0.22.0`: the module's mutation battery before and after, the removals the table proves, a case where the battery shows a sentence unguarded, a `Kills:` line on every kept function, the batch's files off `tests/unguarded-files.txt`, the rows lowered, the union `.test_durations` downloaded, the ledger and `Enforced by:` lines re-pointed. Coverage, read as the mutants killed, does not drop: every mutation red before a batch is red after it.

**Out, and whose.** #929's five files and its mechanism (`case_check.py`, the `Kills:` grammar, the list, the rows' measurers, the 249 byte-identical helper twins): read, not changed. A prose-pinning case (#923's measure, below): it gets its `Kills:` line here, because a file cannot leave the list without one and #929 S5 already makes a `.md` path legal, and it is never removed or re-pointed here; each phase lists what it left. Which legs run on a pull request (item B). `.test_durations`' cadence (#931). The budget mechanism (#930). A suite-wide census job (#929 alternative E). `conftest.py`'s helper consolidation (#929 phase 4).

## What the remaining suite is

`executed` 2026-10-14 at f35e1f57 (`origin/release/v0.22.0` + `routing.md`) on macOS arm64; commands in `plan.md` §*Technical context*. #929's numbers are at fcd735bc, 203 ids lower.

| | Value |
|---|---|
| The suite | 13,914 cases in 185 files (`--collect-only`, 6.1 s); 5,475 test functions; 157,736 lines in `tests/test_*.py`, 160,228 in `tests/*.py`; `.test_durations` prices 13,482 at 7,861 Windows seconds |
| #929's five files | 5,064 cases · 15,177 lines · 2,545 s |
| **The 180 remaining** | **8,850 cases · 5,071 functions · 142,559 lines · 5,316 s** · 3,591 released ledger mentions of their units (24 files with none) · 466 `Enforced by:` node ids in prose files (79 files with none) · 45 files carry `skipif`/`pytest.skip` |
| Prose-pinning, by #929's measure (errs over) | 998 functions, 1,470 cases; 31 files are over half prose. **This item's own: 7,380 cases, 4,073 functions** |
| Shape | 20 files at ≥ 3 cases per function hold 2,380 own cases in 391 functions, 15,232 lines, 597 s; the 160 others hold 5,000 own cases in 3,682 functions, 127,327 lines, 4,719 s |
| Duplication proxies | 389 functions share a body shape with another in the same file (names and constants normalised; a different measure from #929's byte twins); 24 functions hold no `assert` (errs over on a helper that asserts) |
| The proof's cost | A `Kills:` line on a kept function makes it a changed function to `case_check.py`, which runs its file twice. Σ own functions × Windows seconds × 0.23 × 2 = **2,082 ubuntu-minutes** over the 180 files (1,041 at one run); 150 files under 10 min each (5,203 cases, 80,995 lines, 189 min together), 16 at 10–30 (1,562 · 24,960 · 338), **14 at ≥ 30 min hold 1,554 of the 2,082** (2,085 cases, 36,604 lines). 0.23 is the suite's ubuntu/Windows median ratio (9.9/42.4), the one figure here nobody measured per file (`questions.md` Q3) |

**What a sample of five files shows** (`bin/mutation-check`, operator-swap mutations spread over the module, the file run under `bin/test <file> -q -rf`; the module restored and `git status` clean after each table):

| File · module | Ran | Red · killers each | Survived |
|---|---|---|---|
| `test_one_heredoc_shape_is_read_exactly.py` (131 cases) · `hooks/one_heredoc.py` | 5 | 5 · 4, 13, 14, 15, 15 | 0 |
| `test_the_mode_question_is_asked_once.py` (180) · `skills/implement/scripts/seal.py` | 8 | 3 · 12, 12, 3 | 5 |
| `test_the_pull_request_language_is_the_repositorys.py` (124) · `hooks/config.py` | 8 | 4 · 11, 10, and two by collection error | 4 |
| `test_a_record_states_what_the_tree_has.py` (130) · `skills/evidence-check/scripts/evidence_check.py` | 8 | 3 · 129, 129, 3 | 5 |
| `test_the_hooks_hide_what_a_renderer_hides.py` (129) · `hooks/blocks.py` | 5 of 8 | 5 · 14, 10, 3, 6, one by collection error | 0; the sixth (`break`→`continue` in `#walk`) loops and the run was ended |

No sampled mutation had one killer, in a parametrized file or in a one-case-per-function file, so the duplication is not confined to the fan-out files. Four or five of eight mutations survive a single file against a module that other files also load, so a file's survivors are read against the module's files before a case is planted. **How the ranking errs:** an operator swap is coarser than a hand-named sentence (#929 phase 1's m2 had 5 killers), so killer counts here read high; the killer parse reads `FAILED` lines, so a collection error is red with no killer named; the prose measure errs over; the shape-twin measure errs over.

## Batches, order, and what each proves

A **batch is the files whose first-named module is the same shipped module** (`plan.md` §*Technical context* says how it was read), one pull request each. The module's battery — one mutation per sentence the kept files' `Kills:` lines or docstrings name, with a `--timeout` on every run — is run over every file that loads the module, before and after. Removal is within a file under #929's criterion; planting is decided by the module's table. **Order:** the shape proven on one small family first, then families by lines removed per pull request; a file whose own proof costs ≥ 30 ubuntu-minutes at #929's two-run model is held back to one phase of its own (`plan.md` phase 10). **Bound:** a batch's `cases` job stays under the Windows leg's median wait of 42 minutes, measured on its run; a batch over it is split by file before the next opens.

## Targets

Against #929's end values; each ceiling is re-set from the batch's table where the table shows less, under the ratchet.

| Row | #929's end | This item's end | Basis |
|---|---|---|---|
| `test-cases` | ≤ 10,500 | ≤ 8,700 | −1,190 from the 20 fan-out files at phase 1's −51 %; −650 from the 160 others: half the 364 shape twins, the 23 bare functions, a tenth of 3,682 functions |
| `test-lines` | ≤ 150,000 | ≤ 133,500 | −2,500 (fan-out rows at ~2 lines each) −14,000 (~570 functions at ~25 lines) |
| `unguarded-files` | ≤ 175 | 0, or the count phase 10 leaves to 0.22.1 (`questions.md` Q1: 14) | every file this item opens leaves the list |
| `test-cases:<file>` · `test-lines:<file>` | the listed files | each ≤ its table's count | 4 remaining files at ≥ 200 cases, 14 at ≥ 2,000 lines |
| `suite-seconds` · `slow-file:*` | #930's | fall by the removed seconds, ≈ −870 s of 5,316 | the union each batch downloads |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the shape on one batch | phase 1's four files: cases, lines, seconds, the table before and after, the `cases` job's minutes | `phases/phase-1.md`; every mutation red before and after, the killers that are not removed cases unchanged |
| S2 the battery is the module's | a mutation one file survives | run over every file loading the module before a case is planted; the table names the file that kills it or the case planted |
| S3 nothing protects less | each batch's table | every mutation red before is red after; a survivor gets one case, seen red first; the suite may grow by it |
| S4 every kept function declares | a batch's files | every function carries a `Kills:` line; the files leave `tests/unguarded-files.txt`; `unguarded-files` lowered in the same pull request; `case_check.py` exit 0 on the run |
| S5 the rows move with the cut | a batch lands | `test-cases`, `test-lines`, the per-file rows, `slow-file:*` lowered; the union downloaded where the batch removes a twentieth of the seconds; `budget_check.py` exit 0; `test_the_durations_file_prices_the_suite` green |
| S6 prose pins move with the text | a prose-pinning function in an opened file | its `Kills:` line names the document and the literal; it is not removed; the phase record lists it for #923 |
| S7 the ledger and the docs follow | a removed or changed function a released row or an `Enforced by:` line names | `Corrected ·` or `Re-read ·` row in the fragment; the `Enforced by:` line names a remaining killer; `evidence-check --strict .` exit 0; `tests/test_a_folded_statement_names_what_enforces_it.py` green |
| S8 a bare case leaves on its run | a function asserting nothing | removed on that showing, named in the table |
| S9 the proof fits the run | a batch's `cases` job | under 42 minutes on the pull request's run, or the batch is split by file |
| S10 a heavy file is named, not deferred silently | the 14 files at ≥ 30 min | each in `plan.md` phase 10 with its minutes; `questions.md` Q1 says which milestone |
| S11 nothing asks a person | the whole change | no `AskUserQuestion`, no prompt, no box |
| S12 the records are compact | each phase record | the table, the lists (removed · planted · left to #923) and the numbers; no narrative |

## Data & interfaces

No new script. Per batch: the test files cut and lined; rows out of `tests/unguarded-files.txt`; ceilings lowered in `seal/budgets.md`; `.test_durations` replaced by the run's `test-durations` artifact; `Corrected ·` and `Re-read ·` rows in `seal/ledger/1791934662-every-test-file-is-cut-to-what-it-guards.md`; `Enforced by:` lines re-pointed in place; `changelog.md` in this directory; `phases/phase-N.md` with the table and the three lists.

## Removes

nothing — the frame names no unit: which cases leave is each batch's mutation table, so every removed function is a divergence row in `overview.md` with its `Corrected ·` ledger row where a released row cites it, as `docs/the-reader-registry.md` §*A frame names what its work removes* has it and as #929's frame does.

## Open questions → questions.md

Framed 2026-10-14 by framer, before the build.
