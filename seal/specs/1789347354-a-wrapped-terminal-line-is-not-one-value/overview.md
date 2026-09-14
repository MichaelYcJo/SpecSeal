# 1789347354-a-wrapped-terminal-line-is-not-one-value — overview

📋 implement applied
· spec:     `seal/specs/1789347354-…/{routing,spec,plan,questions}.md`; `seal/config.md` (no `Record language` row, so English); `seal/follow-up.md`; `CLAUDE.md` §*a change writes fragments*, §*a ledger coordinate names content*, §*the merge method is fixed per direction*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `skills/agent-contract/SKILL.md` §§1, 2, 3, 4, 5, 7, 8, 9, 12, 14, 15; `skills/implement/SKILL.md` §§1–4; `docs/review-handoff-protocol.md` §*The Needs a fix field*, §*Loses a record or crashes*, §*Conformance*
· evidence: five rows in `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md`, eight anchors stamped by `evidence-check --reverify`
· verified: executed — the four modules below, the record module before and after; every alternative of both constants mutated in turn, killed and with its lookahead dropped, and every sentence this work pins stashed in turn — the results are per-alternative in ledger rows 1 and 2 rather than as a total here, because a count is the third thing this work item got wrong about its own measurements, `bin/evidence-check .`, `--strict`, and the Q5 measurement over 337 terminal rows. Read — the frame, the round-4 report, `seal/ledger.md` R7 and the `issue_claims_check.py` rows. Unverified — the full suite, repository-wide lint and typecheck, which are the sealer's

## Why this work exists

A reviewer's report is hand-wrapped prose and a round record is a table a
checker reads; the one guard deciding where a wrapped terminal line stops was
wrong in both directions, and the document a second implementation would be
built from had never been told the join exists.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many of the four continuation shapes go red against this branch's base | `spec.md` §*User scenarios*: *A case parametrised over the four shapes `#N`, `**bold**`, `<div>` and an indented line, each seen red against the pattern at `5e09345`*. Measured: only the two `#N` shapes are red; the other three already joined | Keep all the arms, and label each with what it WAS seen red against — `base`, `space`, `anchor`, `boundary` | The report the list came from was measured on `backup/120-before-rewrite`, which this clone cannot resolve (`git cat-file -t 3b228f4` fails). The plan said to re-derive rather than transcribe, and the re-derivation is what found this. Two arms are green from birth and say so rather than implying a demonstration that did not happen (§15) |
| Whether anything that passes today begins to fail | `spec.md` §*The gate answer*: *a report that today produces a whole cell is unaffected* | Ship the bidirectional change the rest of the spec asks for, and record that the bullet is one-directional | §*Scope* says *Both directions close at once* and the whole change is built on it. Five shapes that today join into the cell now stop before it — `---`, `___`, `***`, a setext underline, and `1)`. Nothing that today produces a CORRECT cell is affected, which is what the bullet was reaching for |
| How many cases the record module holds | `plan.md` and `spec.md` both say 104 | 107 at the base, 118 after, 119 with round 1's pin | Measured by running it. The 117 and the "ten new cases" that first went into the ledger row were taken at phase 1, before the `anchor` arm was planted — round 1's 🟡 2 caught both, and the row folds into `seal/ledger.md` at the release, so a wrong count there outlives the branch |
| Whether the wrap rule takes a registry row | `questions.md` Q3 (b): *neither needs a registry row*. `plan.md` phase 3 and `spec.md` §*User scenarios*: *a case in `tests/test_the_rules_have_one_owner.py`'s shape* | One registry row for the conformance rule, plus a separate case pinning the split | Read as *neither needs a row to reconcile the two*, since they are not one rule. The conformance rule alone is one owner and two links, which is what `RULES` models. `phases/phase-3.md` holds the reading; recorded rather than sent back, because the batch this work item spends is spent |
| What pays for rejecting the shared pattern constant | `plan.md` §*Alternatives considered* and `spec.md` §*Scope*: *the pin that replaces it is a case asserting the two spellings accept and reject the same shapes*. The build shipped a prose comment at each constant instead | The case, planted by round 1's fix pass | A comment does not go red. Round 1 executed the drift the rejection was argued against — an alternative added to the model and not to this module leaves both modules green, 167 passed — and §*Not done* had recorded the substitution as though the plan had asked for it, so the divergence reached no reader. `tests/test_the_record_is_generated.py#test_the_two_spellings_differ_only_by_the_fence_openers` is now what fails on that drift |
| Whether the builder edits the framer's `spec.md` | The `implement` skill's file table gives `spec.md` to the framer | Spell one coordinate in full; change no claim | `spec.md:252` abbreviated the template anchor with `…`, which the evidence checker's records arm reads as a locator and refuses. This work item's ledger fragment is what made the arm read the directory at all, so the refusal — and a red pull request, since CI fails on any exit ≥ 2 — arrived with this branch. `phases/phase-5.md` holds the detail |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide `ruff check` and `ruff format --check` | the sealer, after the review rounds settle — `skills/agent-contract/SKILL.md` §2 |
| `evidence_check.py#file_units` reads a heading inside a fenced block as a heading, so a ledger anchor on such a section silently stops at the fence. Three of thirty-six anchored markdown files are affected, and `seal/ledger.md` R7 is under-covered by 81 lines | the repository owner — it is a change to a gate under `CONTRIBUTING.md`, and repairing the reader re-hashes rows across the whole ledger |
| ✅ `survivor_check.py#BLOCK`'s whole-line alternative `[-*_=]{3,}\s*$` is pinned by nothing | closed by round 1's 🟡 5 and its fix pass: pinned at all four shapes, seen red with the alternative mutated to match nothing |
| Two of `survivor_check.py#BLOCK`'s five alternatives are still pinned by nothing — `>` in either direction, and the lookahead on `\d+[.)]`. Round 2's 🟡 1 took the ordered-list alternative as the one whose loss nothing catches; killing `>` or either remaining alternative outright widens the pattern and turns nothing red | the repository owner, as a ticket against `survivor_check.py` — round 3 is this work item's last round, so a case written there would ship unread |
| The three-shape joined-list is stated in two carriers and no case counts them, so it can grow back to four with nothing red | the repository owner, as a ticket against `tests/test_the_rules_have_one_owner.py` — the module already owns the idiom — `occurrences(...)` against `AT_MOST_ONE_MORE_CEILING` — and adding a walk is mechanism a fix pass may not add |
| ✅ Whether `survivor-check` over this branch's own range reports anything | run over round 1's fix range in that pass; what it reported and what was done with each is in the hand-back |

## Not done

**#309's two `close` defects are out, and they are #391.** A `deferred` row's
grounds reduced to the home alone, and an empty code span in a `fixed` row's
grounds. Q2 answered *out*: they belong to the cells work item, and the half
that made excluding them unsafe is paid by #391 existing in the `release:
0.11.4` milestone. `round_record.py#fix_table` was not opened.

**No migration of the round records already truncated.** Q5 measured 337
terminal rows across 348 records and found seven carrying a bare `yes`, in
four work items whose ids all begin `17886` — early enough that no reviewer
report survives beside them to say whether the bare word was truncated or
written. The question's own premise did not survive the measurement:
`chain.yes_or_no("yes")` returns `("yes", "")`, the same verdict word a long
value gives, so the checker reads a bare `yes` exactly as it reads
`yes — <what>`. A wrap-truncation also cannot produce one — it keeps the first
physical line, which for a written `yes — <what>` is `yes — <what…>`, never a
bare word. The exclusion in `spec.md` §*Scope* stands, on both grounds.

**No shared pattern constant across the three modules.** `plan.md`
§*Alternatives considered* rejected it, and what pays for the rejection is the
case it named: `test_the_two_spellings_differ_only_by_the_fence_openers`
asserts this module's spelling is the model's plus the two fence openers and
nothing else. **The build shipped only a comment at each constant**, which
does not go red — round 1's 🟡 1 measured the two drifting apart green at 167
passed, and its fix pass planted the case. `.github/scripts/` is not
importable from an installed plugin's `skills/*/scripts/` anyway.

**`templates/sdd-round.md`'s `Needs a fix` row is untouched**, which
`spec.md` §*Scope* puts out for the anchor `seal/ledger.md:89` quotes. The
guidance went into the prose below it; the row's hash is unchanged.

## Fed back into the spec

**Inferred during implementation.** The guard is a narrowing whose boundary is
a property of the shapes themselves rather than of the marker list: a
continuation opening with an HTML tag, with `**bold**`, or with an indented
run of prose is unreachable by any spelling, so the blank line is the only
stop that covers every shape. That sentence is now stated in
`docs/review-handoff-protocol.md`, which owns it, and a planner may overturn
it — but overturning it means choosing the refusal Q1 declined, not a longer
marker list.
