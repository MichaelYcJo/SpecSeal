# Feature Specification: three checks that do not see what they are named for

<!-- seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## One shape, three modules, and the shape is this release's own subject

Each of the three checks passes today while the thing it is named for is
wrong. They were written by this release, each was found by the round that
ended its work item's run, and each was deferred because that run had spent
its one reopening rather than because anyone judged it unworthy.

```
  #413  an attribution nobody asserts   the case reads both `&` cells and
                                        finds both shell names in each, so
                                        the two names swap and 18 cases stay
                                        green while the document a person
                                        reads states one platform's
                                        semantics as the other's
  #418  a set that does not grow        the case says it asserts over the
                                        whole phrase set; three of the set's
                                        four sources are hand-copied, so a
                                        phrase joining either sweep is
                                        checked by nothing
  #422  a claim found by a literal      the refusal decides by what a
                                        sentence claims; what it decides
                                        ABOUT is still the exact substring,
                                        and the stems it matches by are
                                        anchored at one end only
```

**These are three repairs, not one.** They share a symptom and nothing else:
one is an attribution missing from a markdown table, one is a set that does
not track its live sources, and one is a regular expression with two
independent holes. A checker over all three would have to know each case's
own subject to say whether that case sees it, which is a second
implementation of each case — the ground on which #418 itself refuses
deriving its phrase set from the sweeps. What the three share is a
**procedure** rather than a mechanism: each repair is proven red under the
mutation its own issue already measured, and each records what it still
cannot see beside itself. That is `agent-contract` §12 and §15, already
written down, and this work item applies them three times.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | All three repairs make a check refuse what it passed. Each owes a test seen red, a stated failure direction, a prompt budget and platform honesty — the `&` cells' `cmd.exe` claim is the unmeasured one, and this work asserts the document's attribution rather than the platform's behaviour |
| `agent-contract` §12 — a defect belongs to a class | #413 is the third instance of one class in one module and #418 the fourth on one branch. Each repair is owed to the instances its cause produces, not to the coordinate the finding named |
| `agent-contract` §15 — a new case is not planted until it has been seen red | Reverting the fix is the only thing that has ever caught a case that cannot fail, and this whole work item exists because three such cases shipped |
| `agent-contract` §5 — nothing that reaches you in prose is evidence | Each issue carries a paste-ready patch, and two of the three were written by the pass that had just produced the defect one layer up. Two of them are adopted changed, for reasons in `plan.md`'s Alternatives table |
| `seal/specs/1789455558-…/overview.md` §*A repair for a check that cannot fail was itself held by nothing* | The two rules that came out of it bind every phase here: pin the function the production path calls, never the helper beside it; and check that a case's own assertion can fire before a fixture's guard does |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | Rows go to `seal/ledger/1789540097-….md` and the entry to this directory's `changelog.md` |
| `CLAUDE.md` §*a ledger coordinate names content* | One row in another work item's fragment anchors the unit phases 3 and 4 change; it drifts by construction and is re-read rather than re-pointed |
| `skills/implement/SKILL.md` §3, top rung | A check that starts refusing what it did not refuse is a gate's verdict changing, which is what puts this work on the rung that needs a `spec.md` written by a party that does not then build to it |

## Scope

### In

1. **#413 — the attribution in the two `&` cells.**
   `test_both_ampersand_cells_name_both_shells` gains, per cell, an assertion
   that ties each shell name to the consequence that is that shell's. The
   existing presence loop stays: it carries the message for a cell that names
   no shell at all.
2. **#418 — the closed set made live.** The three search phrases the two
   sweeps look for become module constants that both the sweep cases and the
   seam-safety case read, so the set the seam case checks is every phrase
   either sweep searches for rather than a copy of it. The folded members are
   pinned as well, so a `.py` member joining a sweep turns the case red. The
   reason seven phrases are the whole of what is at risk — `flat` folds only
   `.py` members, and there are four across both sweeps — is written down
   where a reader meets the set.
3. **#422, half one — both ends of every stem anchored.** `person` matches
   `person`, `people` and `person's` and not `persona`, which
   `agents/smith.md` already uses. The `user` stem stays, anchored, because
   the anchor is what stops `users` and because the user is precisely the
   party who answers.
4. **#422, half two — the occurrence found by the claim.** Markdown emphasis
   is normalised out before the search, and the preposition and article are
   read as a small set rather than as one literal, so `in **one batch**`,
   `in a single batch` and `as a single batch` all reach the window that
   judges them.
5. **What each repair still cannot see, beside it.** Three sentences, each in
   the module it belongs to, in the shape round 2 of #422 already used for
   *you collect the batch* against *your caller collects the batch*.
6. **The two cells `rounds/round-2.md:39` and `:40` of work item
   `1789445605-…` renders with an empty first clause.** Q1 of work item
   `1789455558-…` assigns them here by construction: *a fourth work item, cut
   from `release/v0.12.0` after `fix/401-402-…` has merged into it, repairs
   both cells … the same fourth work item carries #413.* Both conditions
   describe this branch, and Q1 refused the other two homes with grounds.
7. **The stale documented width in `tests/test_docs_line_wrap.py`'s
   docstring.** #422 reports `agents/smith.md` measured at 109 columns where
   the docstring documents 148. A number stated as a measurement, in the one
   module whose subject is measured widths, is corrected against what the
   module's own helpers report.
8. **This work item's own records** — the ledger fragment, the changelog
   fragment, and the re-read of the one drifted row phases 3 and 4 create.

### Out, and why each one is out

- **A shared checker over the three modules.** It would need each case's
  subject to judge that case, which is a second implementation of what it
  checks. This repository has refused that before, and #418 refuses it again
  in its own *Not this*.
- **Widening #422's refusal — more words in the stem set.** Refusing more
  words makes a legitimate definition unwritable, which is round 2's finding
  in the other direction. The change here is to the finder and to the stems'
  boundaries, never to what counts as a refusal.
- **Bounding #422's window at a heading.** The window is 140 characters over
  the flattened file and therefore crosses headings; #422 measured 42 % of
  `agents/framer.md` and 60 % of `agents/smith.md` as positions where a new
  occurrence would fire. Narrowing it is a third change with its own failure
  direction — an instruction split across a heading would pass — and the
  ticket asked for the finder and the boundary. It is recorded as residue
  instead.
- **A per-agent tool inventory.** Declined with grounds in work item
  `1789518345-…`'s `overview.md` §*Not done*, and its own ticket: it needs a
  list kept in step with a harness no file here can read.
- **Bringing `agents/smith.md` and `agents/scribe.md` under the wrap test's
  covered list.** `seal/follow-up.md` holds that as an open row for the
  repository owner, and adding a path changes what a test guards, which
  `CONTRIBUTING.md` asks a separate argument for. Correcting a documented
  number is not that argument and does not make it.
- **A case that pins the wrap module's documented numbers.** Nothing reads a
  docstring today; planting a reader is new mechanism aimed at the file the
  follow-up row already holds open.
- **#415.** `routing.md` states the reason: it is `hooks/config.py` rather
  than a test module, and configuration disappearing without a message is a
  different thing from a check failing to look. That exclusion does not
  reach scope item 6 — a corrected record ships no changelog entry, so the
  one-entry argument that excluded #415 has nothing to bite on.
- **The prose of the two corrected cells.** A round record holds what was
  true when it was written. Only the rendering is repaired; the sentences
  stay as round 2 wrote them, including the clause about what
  `test_both_ampersand_cells_name_both_shells` pins, which #413 shows to be
  incomplete rather than false.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given `templates/config.md`'s refused `&` row, when `/bin/sh` and `cmd.exe` are swapped in it, then the case names the attribution and the module is red | `bin/test tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q`, exit code read directly, at HEAD and under the swap |
| A2 | Given the allowed `&` row, when the two names are swapped in it, then the module is red for that cell | the same command, second mutation |
| A3 | Given the seam-safety case, when a phrase carrying a foldable seam is added to either sweep's phrase set, then the case is red and says the phrase can be cut | `bin/test tests/test_one_word_one_meaning.py -q`, exit read directly |
| A4 | Given the same case, when `chain_check.py` joins the seal sweep, then the case is red and names the folded member whose phrases are unaccounted | the same command, second mutation |
| A5 | Given a reader who meets the phrase set, then the reason it is closed rather than short is stated where the set is | read: the comment names the `.py`-only fold and the four members |
| A6 | Given an agent definition that writes `persona` or `users` a clause away from a batch phrase, then the guard does not refuse it; and given one that instructs an agent to collect what a person answers, then it still does | `bin/test tests/test_chain_hooks_hardening.py -q`, both directions on a throwaway edit, exit read directly |
| A7 | Given `in **one batch**` — `CLAUDE.md:39` verbatim — or `in a single batch` or `as a single batch` beside a person answering, then the guard refuses it. All three pass at exit 0 today | the same command, one planted definition per spelling |
| A8 | Given each of the three repaired cases, then what it still cannot tell apart is written beside it | read: three residue sentences, one per module |
| A9 | Given `rounds/round-2.md` of work item `1789445605-…`, then no Grounds cell opens with an empty clause, and the records still parse for the checker that reads this repository's own | `bin/test tests/test_chain_check_at_the_pull_request.py -q`, whose `_real_records` case runs the checker over the committed records |
| A10 | Given the wrap module's docstring, then every width it documents is what the module's own helpers report for that file today | re-derived with `prose_lines` and `display_width`; `bin/test tests/test_docs_line_wrap.py -q` |
| A11 | Given the ledger after this work, then the row anchored on the guard phases 3 and 4 change has been re-read and its claim judged, and no row is BROKEN | `bin/evidence-check .`, exit read directly |
| A12 | Given `agents/*.md` at HEAD, then no legitimate sentence in any definition has to be reworded for the repaired guard to pass | the module run at HEAD, green, with no edit to any definition |

## Data & interfaces

No schema, no endpoint, no payload. Three test modules change, one test
module's docstring changes, and two cells of a committed record change. The
coordinates each phase works at are in `plan.md` §*Technical context*.

The one interface that moves is what `agents/*.md` may say: after phase 4 a
definition may write `persona` or `users` freely near a batch phrase, and may
no longer hide an instruction behind emphasis or a synonym. Nothing in the
tree has to be reworded for either — A12 is the assertion of that, and it is
checked rather than assumed.

## Open questions → questions.md

Three rows, and **none of them blocks the build**: one is settled by a
measurement, two are settled by the phase that meets them. What a person had
already decided is cited rather than asked again — Q1 of work item
`1789455558-…` for scope item 6, and `seal/follow-up.md`'s open row for the
covered-list widening this work does not do.

Framed 2026-09-16 by framer, before the build.
