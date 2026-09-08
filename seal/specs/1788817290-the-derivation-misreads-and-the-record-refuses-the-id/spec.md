# Feature Specification: the derivation misreads and the record refuses the id

<!-- seal/specs/1788817290-the-derivation-misreads-and-the-record-refuses-the-id/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Three tickets, one branch, because they are one derivation in one file plus
that file's parsing one row over. `docs/flow.md` §0.9.1's `[#211 · #194 ·
#227]` row is where that grouping was decided.

- **#211** — `Contract changes` reads `no call site found` for a pytest test
  function, where `pytest only` is the value that exists for it.
- **#194** — the derivation compares arities, so a unit returning a new
  *meaning* reads as `none`.
- **#227** — round-prefixed finding ids (`R2-1` … `R2-8`) collapse toward one
  key, and the refusal names neither the format it wants nor the rows it read.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The fix surface — `Contract changes` and `New units`* | The section that defines the row all three of #211 and #194 land in, and the paragraph that enumerates the five values a reach half may hold. #211 changes when one of those five is written; #194 changes what puts a unit in the row at all; both have to be true of this section afterwards |
| `templates/sdd-round.md`, the `Contract changes` field | Already promises "signature, return arity, return type, **or set of returnable values**". The derivation delivers the first two. #194's mechanism is the promise the template already made |
| `skills/code-review/SKILL.md` §*Findings format* | Where reviewers pick severity markers and numbers. #227's ticket asks that the id format be stated where the numbering is chosen, not only at the point of refusal |
| `skills/agent-contract/SKILL.md` §12 | A defect belongs to a class. #211 arrives naming one instance (a test function) and the class is wider — measured below |
| `skills/agent-contract/SKILL.md` §14 | All three fixes change what a person reads: a record row and two refusal messages. Each is pinned by a case in the same commit |
| `CLAUDE.md` §*A change writes fragments, never the shared file* | The changelog entry and the ledger rows go in this work item's own fragments |

## Scope

**In.**

1. `call_sites` classifying a unit pytest reaches without a call site as
   `pytest only` rather than as unreached.
2. `top_units`' contract carrying the set of returned constant literals, so a
   unit that gains or loses a returnable literal reads as a contract change.
3. The paragraph in `docs/review-chain-spec.md` stating what the literal-set
   comparison does **not** catch — a changed input→value mapping.
4. A finding id being a bare integer, in both `fix_table` and `verdict_rows`,
   with a refusal that names the format and quotes the offending row, and a
   duplicate refusal that quotes both rows.
5. The id format stated where reviewers pick numbers.

**Out.**

- Widening the literal-set comparison to reach a changed input→value mapping.
  The design decision, made by the repository owner before the first edit and
  recorded in `routing.md`, is *literal-set comparison plus a stated hole*.
  Documentation alone was refused as a floor; the check ships and the
  paragraph states its limit. A stated hole is a deliverable, not a gap.
- Accepting a round prefix on a finding id. The ticket offers that as one of
  two repairs; the measurement in `plan.md` §*Technical context* is why the
  refusal was chosen instead.
- `tests/test_the_reopening_is_one.py#floor_record`, the one non-runner unit
  under `tests/` that reads `no call site found`. It is passed by name as a
  value and never called, so no `name(` exists — a different cause with a
  different repair, named in `overview.md` §*Not verified*.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A fix changes a pytest test function's signature | Given a fix range that changes a `test_*` def under `tests/` that nothing calls · When `close` writes `Contract changes` · Then the reach reads `pytest only` | `tests/test_a_runner_reached_unit_reads_pytest_only.py`, a real repo built in `tmp_path`, `close` run end to end |
| A fix changes a pytest fixture | Given a fix range that changes a `@pytest.fixture` def under `tests/` requested only by parameter name · When `close` writes the row · Then the reach reads `pytest only`, not `no call site found` | same file — the fixture is a member of #211's class that the ticket did not name |
| A fix changes a `conftest` hook | Given a fix range that changes a `pytest_*` def in a `conftest.py` under `tests/` · When `close` writes the row · Then `pytest only` | same file |
| A dead helper stays dead | Given a fix range that changes a non-runner def under `tests/` nothing calls · When `close` writes the row · Then `no call site found` still | same file — the rule that says *test function* must not become *anything under tests/* |
| A unit gains a returnable literal | Given a fix that makes a unit `return 0` where it never returned a bare constant · When `close` measures the range · Then the unit appears in `Contract changes` with its reach | `tests/test_a_new_returnable_value_is_a_contract_change.py` |
| A unit that only reshuffles which input maps to which returned value | Given a fix that changes `if` conditions and returns the same two literals · When `close` measures · Then the unit does **not** appear, and `docs/review-chain-spec.md` says so | a case asserting the blindness, plus a prose case asserting the paragraph names the shape and the measured instance |
| A reviewer numbers findings `R2-1` … `R2-8` | Given a record whose verdict rows carry round-prefixed ids · When `close` runs · Then it refuses naming the format (`a bare integer`) and quoting the cell | `tests/test_a_finding_id_is_a_bare_integer.py` |
| The fix table carries a round-prefixed id | Given `## Fixes` rows numbered `R2-1` … · When `close` parses it · Then the same refusal, quoting the cell | same file |
| Two rows really do carry the same id | Given two verdict rows numbered `3` · When `close` runs · Then the refusal quotes **both** rows | same file |
| The severity marker still leads the cell | Given `🔴 1`, `⬜ 12`, `✅ 7`, `❓ 9`, and a bare `4` · When either table is parsed · Then all are read as before | same file, plus the corpus case below |
| The 130 committed records do not change verdict | Given every `seal/specs/*/rounds/round-*.md` in the tree · When the new rule is applied to their verdict tables · Then no record that parses today refuses for a reason other than a miscount | `tests/test_a_finding_id_is_a_bare_integer.py::test_the_committed_records_are_measured_against_the_rule` |

## Data & interfaces

No schema, no endpoint. Three functions in one file change:

| Coordinate | What changes |
|---|---|
| `skills/code-review/scripts/round_record.py#call_sites` | The empty-reach branch asks whether the unit is runner-reached before falling to `NO_SITE` |
| `skills/code-review/scripts/round_record.py#top_units` | The contract tuple gains a third element, the returnable literal set |
| `skills/code-review/scripts/round_record.py#fix_table` · `#verdict_rows` | Both read the `#` cell through one new helper instead of `NUMBER_RE.search` |

No reach value is added: #211 writes the existing `PYTEST_ONLY`. That is why
`tests/test_the_fixes_name_their_surface.py#reach_values` — which derives the
reach vocabulary from `call_sites`' own source and asserts the spec section
names every member — stays green without the section gaining a sixth value.

## Open questions → questions.md

Two assumptions are stated there rather than asked, because neither changes
what gets built. Nothing here waits on a person.
