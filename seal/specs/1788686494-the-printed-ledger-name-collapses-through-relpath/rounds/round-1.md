# 1788686494-the-printed-ledger-name-collapses-through-relpath — review round 1

| Field | Value |
|---|---|
| Target SHA | c04977b |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 186 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1 and 2. Finding 1 needs either the two-rule detector widening above or the claim narrowed in four places; finding 2 needs the one boundary assertion. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item `1788686494`, target `c04977b`, base `origin/release/v0.8.3`, draft pull request #186, issue #163.

Attack these first, in this order. Each is a specific claim this branch makes, not a area to browse.

1. **The closure's completeness, from the under-reach side.** `test_no_ledger_path_reaches_relpath` computes a data-flow closure from `resolve_patterns`' three call sites and asserts no carrier reaches `relpath`. Its author reports it OVER-reaches (it marks `findings` and `key`, neither a path), which is the safe direction. The question is the other one: can a ledger path reach a rendering site **without** being a carrier under those four propagation rules — through `os.path.dirname`, a `join`, an f-string, a tuple unpacked later, a dict value, a `%` format? If one can, the case is a vacuity dressed as a proof.
2. **`display_name`'s boundary, at the A×D crossing the mutation battery found late.** The unit compares root and path by segment and slices without rejoining. One mutation — the separator set hardcoded as `("/", "\\")` instead of taken from `flavour` — survived all eighteen cases until a nineteenth assertion was added, because `/tmp/proj\seal/ledger.md` is one segment on POSIX and three under the hardcoded set. Ask whether the added assertion closes that crossing or only the one instance of it, and whether any other axis pair was pruned as uninteresting the same way.
3. **The integration case's assertion order.** Its author reports the first draft compared spellings before comparing inodes, so under the mutation the assertion carrying the claim never ran. Check the reordering is right rather than merely moved, and that the case fails for the reason it names.
4. **A test that baked in the defect.** Five call sites changed the text they print. 170 cases over four modules pass unchanged. Either no existing case asserted a ledger display name, or one asserted the wrong one and still passes. Settle which by opening the assertions, not by trusting the count.
5. **The four `seal/ledger.md` rows this branch drifted** — `check_ledger`, `reverify`, `migrate`, `main`. The author re-read all four and reports the claims still hold, and left them unstamped on purpose. Judge the claims yourself against the edited units; a claim that no longer holds is a removal, not a re-stamp, and that is the repository's rule rather than a preference.
6. **The Windows leg reaches `display_name` through `ntpath` in five cases and through the CLI in none.** Ask whether the real Windows leg exercises the shipped path at all, and whether `flavour` as a test seam is load-bearing for a guarantee or only for coverage.
7. **The local-mode decision.** Where `seal_home` answers a path outside a linked worktree, the header now prints an absolute path where it printed `../main/.git/seal/ledger.md`. Check no document, test or docstring still promises the relative form.
8. **Degenerate roots and paths.** `root` of `/` alone, `root` equal to `path`, an empty tail, a root with repeated separators, and a path that is the root plus a separator and nothing else.

Facts, labelled:

- **executed by the orchestrator at `c04977b`** — `./bin/test` over `test_the_printed_ledger_name_is_the_file_that_was_read.py`, `test_a_narrowed_ledger_read_says_what_it_skipped.py`, `test_evidence_check.py`, `test_a_row_points_by_content.py` → 170 passed, exit 0. `uvx ruff check` and `uvx ruff format --check` over the three changed files → exit 0. `./bin/evidence-check .` unscoped → 685 ok · 6 drifted · 0 broken, exit 1; four of the six are this branch's, two (`templates/config.md#"# Repository config"`, `round_record.py#swallowed`) are the base's.
- **read** — `.venv` carries no `ruff` module; use `uvx ruff`. The suite runs through `./bin/test`.
- **unverified** — everything in the eight items above.

Run the ledger check in its **unscoped** form; the narrowing is a writer's tool and this is a read.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The class guard under-reaches in six constructible shapes, and four records claim it cannot false-pass | `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:441`, `:405`; claims at `changelog.md:23`, `overview.md:57`, `phases/phase-2.md:98`, `tests/…:370`, `seal/ledger/1788686494-…md:10` | open | Executed: six source mutations, none reported by `relpath_on_a_ledger`; the shipped shape is. `main:1721`'s existing tuple unpack makes the tuple case reachable by an ordinary refactor. A narrower fix was run and is clean on the current source |
| 2 | Building the separator set without `altsep` survives all 43 cases, and changes four reachable Windows spellings | `skills/evidence-check/scripts/evidence_check.py:999`; case at `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py:295` | open | Executed: eight mutations, six killed, this one exit 0 at 43 passed. `--ledger C:/proj/seal/ledger.md` under an `abspath` root is the reachable input |
| 3 | The drive comparison is unpinned in both directions | `skills/evidence-check/scripts/evidence_check.py:1002` | open | Executed: case-folding the drive survives all 43 cases. The docstring states the choice, so this is a missing pin rather than a wrong answer |
| 4 | The five rendering sites are the whole class on the current source | `skills/evidence-check/scripts/evidence_check.py:1131`, `:1389`, `:1514`, `:1708`, `:1741` | answered | Re-derived independently: 61 carrier-bearing statements over ten functions, five of them rendering. Matches the author's enumeration |
| 5 | The integration case's reordering is right and fails for the reason it names | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:642` | answered | Executed with `relpath` back at `main:1741`: stops on the inode assertion, premise passed, spelling compare never reached |
| 6 | No existing case baked in the wrong ledger name | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:91`, `:119`, `:687`, `:703` | answered | Read: all four assert `seal/ledger.md` and pass under either rendering because their fixtures carry no `..` |
| 7 | The four drifted `seal/ledger.md` rows still hold, and leaving them DRIFTED is correct | `seal/ledger.md:121`, `:123`, `:125`, `:132`, `:133`, `:135`, `:149`, `:161`, `:162`, `:169`, `:170`, `:296`, `:381` | answered | Read all thirteen against the edited units; every edit is a rendering swap. Executed: the CI ledger job warns at exit 1 and fails only at >= 2 (`.github/workflows/test.yml:85-94`), so no gate is lost |
| 8 | The Windows leg exercises the shipped path through the CLI; `flavour` is coverage, not a guarantee | `.github/workflows/test.yml:37`; `skills/evidence-check/scripts/evidence_check.py:959` | answered | Read: `os.path is ntpath` there, and the four CLI assertions render through both sites. The seam takes the real module |
| 9 | No document, test or docstring still promises the local-mode relative form | `skills/evidence-check/SKILL.md:186` | answered | Read: swept `docs/`, every `SKILL.md`, `templates/`. The one output example is shared-mode and still exact |
| 10 | Degenerate roots and paths render correctly | `skills/evidence-check/scripts/evidence_check.py:999-1031` | answered | Executed over sixteen shapes: `/` root, root equal to path, empty tail, repeated separators, empty root, drive-relative, UNC |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` at `c04977b`, `uv venv` + `pytest 9.1.1` inside it | clone and main tree both left clean; all `test_tmp_*` files deleted |
| Six source mutations against `relpath_on_a_ledger` — alias, subscript, wrapper, tuple unpack, bare `relpath` import, `normpath` | none reported; the direct `relpath` shape reported at `main` L1741 |
| A narrower detector (one alias rule + a widened first-argument gate) over the current source and the same six mutations | carrier sets byte-identical to shipped, zero offenders on the current source, alias/subscript/inline-wrapper now named |
| A wider detector (propagate through any assignment mentioning a carrier) | rejected: fifteen extra names in `main`, six false alarms on the current source |
| Eight mutations of `display_name` against the two changed test modules, 43 cases each | six killed (hardcoded seps, `<=`→`<`, drive check dropped, anchor check dropped, rejoin, `startswith`); two survived (`altsep` dropped, drive case-folded) |
| `relpath` restored at `main:1741`, integration case alone | fails on the inode assertion, `assert (16777232, 185999773) == (16777232, 185999771)` |
| `display_name` over sixteen degenerate POSIX and Windows shapes | no wrong answer |
| Carrier-statement enumeration over the checker's source | 61 statements, ten functions, five rendering sites — matches the author's five |
| `./bin/evidence-check .` unscoped in the clone | 685 ok · 6 drifted · 0 broken, exit 1 — confirms the orchestrator's figure |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Four rows in `seal/ledger.md` left DRIFTED; their claims re-read and holding | `overview.md` §Not verified and §Not done | the orchestrator or the release step, by `--reverify` over the whole ledger with every branch in flight in view |
| Two rows drifting since `885acf8` — `templates/config.md#"# Repository config"`, `round_record.py#swallowed` | `overview.md` §Not verified | whoever owns those work items; untouched by this change |
| The full suite, repository-wide lint and typecheck | `agent-contract` §2 | the orchestrator, once, after the rounds settle |
