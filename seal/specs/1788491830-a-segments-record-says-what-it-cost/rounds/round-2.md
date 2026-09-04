# 1788491830-a-segments-record-says-what-it-cost — review round 2

| Field | Value |
|---|---|
| Target SHA | 0516e095a244213a2b9456b86e14082c71349b33 |
| Ran by | specseal:warden on Opus — handed over in the spawn prompt this time, which is what round 1's reviewer could not be given |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 the arm-order case pins neither the order nor the docstring and the ledger cites it as executed grounds; 🟡 2 the every-record case passes with a one-record fixture; 🟡 3 the spec's no-prefix row contradicts the code and its own next paragraph; 🟡 4 the subsection states an unenforceable rule as enforced |
| Loses a record or crashes | no |

- [ ] Pass

<!-- Written before the fix pass this round commissions, which is what
`templates/sdd-round.md` has always asked for and what the orchestrator failed
to do on this work item's round 1 and on the whole of `1788486395`. #150 is
the ticket for making that observable; this record is the first one written
under the rule since it was measured. -->

## What this round was asked

The verifying round, at the diff of round 1's fixes — `git diff 77eb59d..HEAD`
— with round 1's seven verdicts as the agenda and the six cases its fix pass
created as the finding surface.

Six things to try to break, in order. The first was a consequence of the
orchestrator's own error: **the subsection now in the spec is not the one the
reviewer drafted**, because round 1's record was written after the fix pass
and the draft lived only in a report. The round was asked to compare what
shipped against the neighbouring subsections rather than against a draft it
could not reach.

Three of the fix pass's cases can only go red under mutation and say so in
their own docstrings. The round was asked to treat that as a claim to check
rather than accept, because a case that never fails is indistinguishable from
one that cannot.

The round was also handed its own `Ran by` value, which round 1's reviewer had
correctly refused to invent.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 1's 🟡 1, the missing spec subsection | `docs/review-chain-spec.md:779` | answered | The subsection is there and all three pins go red when it is deleted. Two findings inside it — 🟡 6 and 🟡 7 below |
| 🟢 2 | Round 1's 🟡 3, the no-prefix arm | `chain_check.py:1912` | answered | Removing `began is None` turns exactly one case red and nothing else |
| 🟢 3 | Round 1's 🟡 5, the comment case | `tests/test_a_record_says_what_ran_it.py` | answered | Switching `strip_comments` off in the reader turns exactly that case red. The old version could not have caught it |
| 🟢 4 | Round 1's 🟢 6 and 🟢 7, the two templates and this branch's own records | `templates/`, `phases/` | answered | Re-read rather than re-derived; `evidence-check --strict` on the fragment reports 10 ok |
| 🟢 5 | Round 1's deferral — the `read_record`-returns-`None` arm | `chain_check.py:672`, `:693` | answered | The implementer's judgment holds and the round went looking. `round_records` and `read_record` both ask git about HEAD, so they agree by construction; a `?` in a work-item id does not glob a sibling (executed, git 2.50.1); an empty committed record returns `""` and not `None`. What is left is a concurrent HEAD change, and `checked_by` already errors on the same record. A case here would pin an unreachable state's message |
| 🟡 6 | The case written to close round 1's 🟡 4 pins neither the arm order nor the docstring, **and the ledger cites it as the executed grounds for R1's corrected claim** | `tests/test_a_record_says_what_ran_it.py:606` | open | Executed: reverse the arms and 52 pass; delete the arm-order reasoning from the docstring and 52 pass. Its three behavioural assertions are each asserted verbatim elsewhere, and the one new assertion — `ON_RE.search("unknown") is None` — cannot fail, because `unknown` holds no `on` substring at all. It is satisfied by the input rather than by the whitespace requirement it stands for. That is the mistake R1's own Notes name one sentence later: *a parser argument that is not differentially executed is a story about the code* |
| 🟡 7 | The every-record case passes with a one-record fixture | `tests/test_a_record_says_what_ran_it.py:249` | open | Executed: revert `declared()` to one record and 52 pass, with the last-record narrowing also unseen — one record is the last one. **The fourth instance of the class this work item named in phase 4**, this time in the fixture rather than the needle or the exit code |
| 🟡 8 | A table row copied from the floor's subsection says the opposite of what `ran_by` does, and of the paragraph two lines below it | `docs/review-chain-spec.md:809` | open | *"any of those, work item with no timestamp prefix → prints"* reaches back over three rows that say *fails on any record*. `chain_check.py:1915-1920` refuses all three without consulting `began`, and the same subsection says so in prose. §12: `:686` under the floor makes the same claim about the same three states and is wrong the same way; `:730` under `Needs a fix` is correct, because that row does grandfather whole |
| 🟡 9 | The subsection states its central rule as if the checker enforced it | `docs/review-chain-spec.md:817-823` | open | Every neighbouring subsection names what its check cannot see and who looks instead — the depth's is the clearest. Nothing in `ran_by` can tell a transcribed value from an invented one. Round 1's own record leans on *the limit the spec subsection records rather than closes*, so that record currently describes a document that does not exist |
| ❓ 10 | `test_the_documents_say_why_older_records_are_excused` asserts a constant name, and for `chain_check.py` that is a tautology — the constant is defined and read there, so the file cannot stop containing the string while the code runs | `tests/test_a_record_says_what_ran_it.py:441` | fix or justify | The doc half does go red when the subsection is deleted, so the case is not empty. It is a deliberate copy of `test_the_fixes_name_their_surface.py:568`, which has the identical shape for `SURFACE_FROM`. Keeping the repository's arrangement is defensible; if it is kept, the name should stop claiming more than it checks, and if it is fixed the sibling is owed the same edit |

## Executed probes

| What was run | Result |
|---|---|
| control, 52 cases in the clone at target | 52 passed |
| `runner_problem` arms reversed | **52 passed — nothing red** |
| the arm-order reasoning deleted from the docstring | **52 passed — nothing red** |
| `declared()` reverted to one record | **52 passed — nothing red** |
| the same, plus `ran_by` narrowed to the last record | **52 passed — nothing red** |
| `ran_by` narrowed to the last record alone | 1 red |
| `began is None` removed from the guard | 1 red |
| the subsection deleted from the spec | 3 red |
| `strip_comments` switched off | 1 red |
| `ON_RE` loses its whitespace | 2 red — `monitor`, both places |
| the round's proposed fixes for 🟡 6 and 🟡 7, unmutated then under three mutations each | green, then red in every case |
| `ls-tree` pathspec with `?` against `git show` | no divergence, git 2.50.1 |
| an empty committed record through the whole checker | `read_record` → `""`, exit 1, seven rows named |
| `evidence-check --ledger 'seal/ledger/1788491830-*.md' --strict .` · `unverified-check` · `uvx ruff check` | 10 ok exit 0 · exit 0 · exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `docs/review-chain-spec.md:779` | Round 1 found the subsection missing; round 2 found two defects inside the one that replaced it, and one of them is inherited from the neighbour it was copied from |
| round 1 | the class named in `phases/phase-4.md` | Three instances at round 1, a fourth here. It has now appeared in a needle, an exit code, and a fixture |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `read_record`-returns-`None` arm, three functions wide | `overview.md` §Not done — answered by round 2 rather than re-litigated, and no fix owed | the repository owner |
| The full suite, repository-wide lint and typecheck | `overview.md` §Not verified | the orchestrator's single broad run, once the rounds settle |
| `seal/ledger.md` S8 | work item `1788472135`'s memo | the repository owner |

**The run does not end here.** Both rounds answered the floor `no`, and four
findings need a fix, so a round at the diff of those fixes is owed — the
sequence `stopping_floor`'s bound is written to permit, and the second time
this branch's own rules have decided what happens next on it.
