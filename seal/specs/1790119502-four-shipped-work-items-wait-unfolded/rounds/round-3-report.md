# Review round 3 — verifying `d6ecf3b..dc222e0` on `chore/514-four-shipped-work-items-wait-unfolded`

Target SHA `c75f6a7`, base `origin/release/v0.13.2`. Reviewed in a
`git clone --no-local` at the target. This is the verifying round that ends
the run: round 2 was the one reopening, so its target is the five commits
round 2 recorded as its `Fix range`. Round 2 recorded `New units: none`, and
the range touches only prose and records, so there is no unreviewed unit.

```
round 2's ⑤ 🟡  L6 carrier list short, "each points at the ladder" false
    8b126bc  → the paragraph names a search, not a list          answered
round 2's ⑥ ⬜  checklist box: "the one direction that job fails in"
    d2139d8  → three failure directions and the title fallback    answered
                └ same claim, pre-existing, in the script's own
                  docstrings                                      ⬜ deferred round-3.md
round 2's ⑦ ⬜  headline: two pushes fire all three acts
    c26bfd4  → "fire two of them"                                 answered
round 2's ⬜ correction  → 0b0afa9, dc222e0 on this item's records  confirmed
ledger C4, S9 re-verified in the range                            confirmed
```

## Round 2's findings, re-checked against the code

**5 (🟡): answered.** The fix claimed the depth-exit phrase stands in
"documents, agent definitions, skills and the round-record template", that a
whitespace-collapsed search for *or becomes an issue* finds them, that some
spell the clause before it without a comma, and that not every carrier points
at the ladder. I ran that search over every tracked file. The prose sites are
`docs/review-chain-spec.md` §*The bound has a floor*, `docs/review-handoff-protocol.md`,
`agents/smith.md`, three sites in `skills/code-review/orchestration.md` and two
in `templates/sdd-round.md`. Those are exactly the four kinds the paragraph
names. The remaining hits are `seal/ledger.md`, this item's own records, the
runtime strings in `round_record.py` and `chain_check.py`, and three test
modules that pin the string. None of those is a prose carrier.

The comma claim holds. `docs/review-handoff-protocol.md`, the orchestration
table row, the second template site and one `chain_check.py` message all read
*named answerer or becomes an issue*. A search for round 2's longer phrase
would miss them, and the fix searches for the shorter one. The pointer claim
holds too. `docs/review-handoff-protocol.md` and the template's floor sentence
name no table at all, and the first orchestration site points at the document
rather than the ladder. The search admits no false member either:
`CAPPED_EXIT`'s *every finding still open becomes an issue* does not match.

**6 (⬜): answered.** The fix claimed the job fails for a missing changelog
section, for a `v*` tag that is not `vX.Y.Z`, and when a `gh` call fails, and
that a missing title line falls back to the tag name. Against
`.github/scripts/publish_release_note.py`:

- `main` returns 1 when `version_of` gives `None`, and the workflow fires only
  on `tags: ['v*']`, so the second direction is reachable exactly as stated.
- `main` returns 1 when `section_body` gives `None`.
- `release_exists` exits for any `gh api` error that is not a 404, and `run`
  exits for a failed `gh release create`. `sys.exit` with a message exits 1.
- `title_from` returns the tag when `title_line_re` does not match, and
  nothing raises there.

One more path exits through `run`: `commit_message` calls `git log -1 <tag>`.
The workflow checks out with `fetch-depth: 0` at the pushed tag, so I found no
way for it to fail after the checkout succeeds. The box also no longer claims
its list is exhaustive. I do not count it against the fix.

**7 (⬜): answered.** "Two different pushes fire two of them" now agrees with
the paragraph's own next two sentences and with the directory bullet's
"Nothing fires it; a person runs it". The workflows are unchanged from round
2's reading: `close-issues-on-release.yml` on `push: branches: [main]`,
`publish-release.yml` on `push: tags: ['v*']`.

**Round 2's ⬜ correction: confirmed.** Rule (b) in `spec.md`'s
`1790076070` destination row, in `phases/phase-3.md` and in `plan.md` now
matches `docs/the-evidence-ledger.md` §*The fold*: a hit the grep finds keeps
the directory by (a), and REMOVED decides only what the grep missed.
`spec.md:33` and `spec.md:208` cite the work item and its `docs/` section
rather than a commit, which matches G2's replacement note. No live document
and none of this item's non-round records still counts four carriers.

**Round 1's 1–4: carried.** Round 2 answered them and the range does not
reopen any. The one sentence it touched in finding 1's paragraph is 7 above.

## Ledger rows re-verified in the range

**C4 (`15e82c21 → 26fb2b36`): claim-preserving.** The only change under the
anchored heading is the L6 paragraph. The ladder, its test and its table are
byte-identical across `d6ecf3b..dc222e0`, and the row's new note describes
the change accurately. `tests/test_the_rules_have_one_owner.py` is green.

**S9 (`5fd6bcab → 686d8ed5`): claim-preserving.** The only change under §6 is
the release-note box's failure sentence. It names no trigger, the
close-issues paragraph is untouched, and `grep -c "on the tag"
docs/release-checklist.md` returns 0.

## One new thing, outside the fix range

The claim `d2139d8` corrected in the checklist still stands in two places in
the release-note job's own files. Neither was touched by the fix range, so it
is a `deferred` candidate under the reopening rule and not a fix.

- `.github/scripts/publish_release_note.py`'s module docstring lists exit 1 for
  a non-`vX.Y.Z` tag and a missing section only. A failed `gh` call also exits
  1, through `release_exists` or `run`.
- `tests/test_a_release_publishes_its_note.py#test_a_tag_with_no_changelog_section_goes_red`
  says the missing section "is the one direction that fails". In context it
  contrasts with the title fallback, so it reads less wrongly than the old box
  did.

Nothing ships a defect if these stand, so it is ⬜. No open issue owns the
release-note script and nobody has agreed to act on it, so it takes rung 4.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule gave all three acts to the tag push | `docs/branch-and-release.md:43-73` | answered | carried from round 2; the one sentence the range changed there is 7 |
| 2 | 🟡 Folded rules (a) and (b) gave opposite answers, and Q4 lost its home | `docs/the-evidence-ledger.md:173-202` | answered | carried from round 2; the range corrected only this item's records to match it |
| 3 | ⬜ The acts-table sentence omitted the `###` rows | `docs/the-agent-set.md:96-105` | answered | carried from round 2; not in the range |
| 4 | ⬜ The L6 paragraph omitted `CAPPED_EXIT`'s lag and the carriers | `docs/review-chain-spec.md:299-316` | answered | carried from round 2; its carrier sentence is 5 |
| 5 | 🟡 The L6 paragraph's carrier list misses `templates/sdd-round.md`, and its claim that each carrier points at the ladder is false | `docs/review-chain-spec.md:309-317` | answered | `8b126bc` holds. Executed: whitespace-collapsed search over tracked files finds prose carriers only in the four kinds named; both comma spellings match; no false member. Read: each site's pointer |
| 6 | ⬜ The checklist box says the note job fails in one direction only | `docs/release-checklist.md:247-251` | answered | `d2139d8` holds. Read: `publish_release_note.py#main`, `#run`, `#release_exists`, `#title_from`, and the workflow's `v*` trigger |
| 7 | ⬜ The headline says two pushes fire all three acts | `docs/branch-and-release.md:50` | answered | `c26bfd4` holds. Read: both workflow triggers and the directory bullet |
| 🟢 | Round 2's correction: rule (b), the pin citation and the carrier count in this item's records | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/` | confirmed | Read against `docs/the-evidence-ledger.md` §*The fold* and G2's replacement note; grep for a four-carrier count outside round records finds none |
| 🟢 | C4's re-verify preserves the claim | `seal/ledger.md` C4 | confirmed | Read: only the L6 paragraph changed under the anchor. Executed: `evidence-check --strict` 0 drifted; `test_the_rules_have_one_owner.py` green |
| 🟢 | S9's re-verify preserves the claim | `seal/ledger.md` S9 | confirmed | Read: only the box's failure sentence changed under §6. Executed: `grep -c "on the tag"` returns 0 |
| ⬜ | The release-note script's module docstring and its A3 case docstring still name fewer failure directions than the corrected box | `.github/scripts/publish_release_note.py` module docstring; `tests/test_a_release_publishes_its_note.py:188` | deferred round-3.md | new this round and outside the fix range; rung 4, see Deferred |

## Executed probes

| What was run | Result |
|---|---|
| `./bin/evidence-check --strict .` | exit 0 · 1468 ok · 0 drifted · 0 broken |
| `bin/test -q` over nine modules pinning the edited documents and the release-note job | exit 0 · 189 passed, 1 skipped (`test_the_reopening_is_one.py:564`, a release branch not fetched in the clone) |
| whitespace-collapsed search for *or becomes an issue* over `git ls-files` | prose carriers in `docs/` (2 files), `agents/smith.md`, `skills/code-review/orchestration.md` (3 sites), `templates/sdd-round.md` (2 sites); every other hit is a record, a runtime string or a test pin |
| `grep -c "on the tag" docs/release-checklist.md` | 0 |
| line width over the three edited documents | no line the range wrote exceeds 88 |
| broad gate — full suite, lint, typecheck | not yet. Not this round's to run. Nothing is left open, so the sealer's spawn is now due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The release-note script's docstrings name fewer failure directions than the corrected checklist box | round-3.md, and the pull request body | nobody has agreed to act on it — rung 4 |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Opened: `docs/review-chain-spec.md` (L6 paragraph and §*Where a leftover
goes*), `docs/branch-and-release.md:40-75`, `docs/release-checklist.md:236-256`,
`docs/the-evidence-ledger.md:170-205`, `.github/scripts/publish_release_note.py`,
`.github/workflows/publish-release.yml`,
`tests/test_a_release_publishes_its_note.py:140-200`, `seal/ledger.md` rows C4
and S9 (through the range diff),
`seal/specs/1790119502-four-shipped-work-items-wait-unfolded/rounds/round-2.md`
and `round-2-report.md`, `spec.md` G2 and lines 30-33 and 205-210, the full
diff `d6ecf3b..dc222e0`. Read through the search output only: each carrier
site's surrounding 160 characters.
