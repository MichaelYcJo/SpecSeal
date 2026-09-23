# Review round 2 — verifying `3bbc219..96caaea` on `chore/514-four-shipped-work-items-wait-unfolded`

Target SHA `7660a34`, base `origin/release/v0.13.2`. Reviewed in a
`git clone --no-local` at the target. This round's target is the six fix
commits round 1 recorded as its `Fix range`; its finding surface is those
fixes plus the two `New units`.

```
round 1's ①–④  closed by 71c33d1, 4ee07f9, e2ec58e, b6544f6         (answered)
  └ ④'s fix wrote "four prose carriers … each points at the ladder,
    so none states it wrongly"                                     ⑤ 🟡 both halves false
  └ ①'s fix corrected "goes red only when …"; its twin in the
    checklist §6 box was left standing                              ⑥ ⬜ same class
  └ ①'s new headline says "none waits on somebody remembering",
    and its own bullet says a person runs the command               ⑦ ⬜
96caaea / 36813ff  corrections to this item's records: accurate,
                   three siblings left                              (⬜ correction)
```

## Round 1's findings, re-checked against the code

**1 (🔴): answered.** `docs/branch-and-release.md:43-73` now matches the code on
every trigger: `close-issues-on-release.yml` fires on `push: branches: [main]`;
`publish-release.yml` on `push: tags: ['v*']`; no workflow names
`plugin_directory_check.py`; the fallback clause matches
`publish_release_note.py#title_line_re`.

**2 (🟡): answered.** Rules (a) and (b) in `docs/the-evidence-ledger.md` give one
answer; `plan.md` phase 5 step 2 agrees; `seal/ledger.md:78` is the only
`seal/specs/<id>` anchor; #517's body and design comment carry `1788184145`,
so Q4 has a durable home.

**3 (⬜): answered.** The sentence matches
`tests/test_every_orchestrator_act_names_its_delivery.py#acts`.

**4 (⬜): answered for what it named.** The `CAPPED_EXIT` half is right
(`chain_check.py:773-777` against `docs/review-chain-spec.md:116-121`). The
carrier half is finding 5.

## The new units

`release_tail_rule` and `test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag`
are confirmed: the slice starts at the first `1790076050` marker and stops at
the next heading; the case exits 1 against `d0282bf`'s text and 0 at `7660a34`.

## The C4 re-verify (`4a6c56fa → 15e82c21`)

Claim-preserving: `git diff d0282bf 7660a34 -- docs/review-chain-spec.md` is the
L6 paragraph alone; `evidence-check --strict .` 1468 ok · 0 drifted · 0 broken.

## Findings

### 5. 🟡 The L6 paragraph lists four carriers of the depth-exit wording, and misses one; it says each points at the ladder, and several point nowhere

`docs/review-chain-spec.md:309-316`, written by `b6544f6`. A whitespace-collapsed
search for *named answerer, or becomes an issue* finds the phrase in
`templates/sdd-round.md`, which the list omits — the template every round
record is written from — and several sites state the two homes with no pointer
to the ladder. The paragraph exists so the owner's rewording moves every
carrier; a short list is the pattern ledger row C6 records (*a carrier list was
shorter than the class*). The fix copied `overview.md` §Not done rather than
the grep.

### 6. ⬜ The checklist box still says the note job fails in one direction only

`docs/release-checklist.md:247-249`. `publish_release_note.py#main` also returns 1
for a `v*` tag that is not `vX.Y.Z`, and `run` / `release_exists` exit on a
failed `gh` call. Editing §6 drifts ledger row S9, so it is optional.

### 7. ⬜ The new headline says no act waits on a person, and its bullet has a person run one

`docs/branch-and-release.md:44-53`. *"Two different pushes fire them"* — two of
the three.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The folded release-tail rule gave all three acts to the tag push | `docs/branch-and-release.md:43-73` | answered | fix is round 1's (`71c33d1`); verified against both workflows and `publish_release_note.py#title_line_re`; the new case goes red against `d0282bf`'s text |
| 2 | 🟡 Folded rules (a) and (b) gave opposite answers, and Q4 lost its home | `docs/the-evidence-ledger.md:173-202` | answered | fix is round 1's (`4ee07f9`); `seal/ledger.md:78`; #517 body and design comment |
| 3 | ⬜ The acts-table sentence omitted the `###` rows | `docs/the-agent-set.md:96-105` | answered | fix is round 1's (`e2ec58e`) |
| 4 | ⬜ The L6 paragraph omitted `CAPPED_EXIT`'s lag and the carriers | `docs/review-chain-spec.md:299-316` | answered | fix is round 1's (`b6544f6`); the carrier sentence it added is finding 5 |
| 5 | 🟡 The L6 paragraph's carrier list misses `templates/sdd-round.md`, and its claim that each carrier points at the ladder is false | `docs/review-chain-spec.md:309-316` | open | Executed: whitespace-collapsed search for the phrase; Read each site |
| 6 | ⬜ The checklist box says the note job fails in one direction only | `docs/release-checklist.md:247-249` | open | Read `publish_release_note.py#main`; drifts S9 if edited |
| 7 | ⬜ The headline says two pushes fire all three acts | `docs/branch-and-release.md:44-53` | open | Read |
| ⬜ | This item's records: `spec.md`'s `1790076070` destination row and `phases/phase-3.md:52-54` still state rule (b) as "REMOVED decides each"; `spec.md:33,208` still describe the pin; `overview.md:44` and ledger row C4's note carry the "four carriers" count | `seal/specs/1790119502-four-shipped-work-items-wait-unfolded/`, `seal/ledger.md` C4 | correction | Read |
| 🟢 | New units pin the right facts and go red for the right reason | `tests/test_the_release_tail_does_not_end_at_the_tag.py` | confirmed | Executed: exit 1 against `d0282bf`'s text, exit 0 at `7660a34` |
| 🟢 | C4's re-verify preserves the claim | `seal/ledger.md` C4 | confirmed | Executed: `evidence-check --strict .` 1468 ok |
| 🟢 | `96caaea` and `36813ff` corrections match the code and G2's replacement | this item's records | confirmed | Read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` over seven modules pinning the edited documents | exit 0 · 169 passed |
| the label-acts case against `d0282bf`'s `docs/branch-and-release.md` | exit 1 · the headline attributes every act to the tag push |
| the same case at `7660a34` | exit 0 |
| `./bin/evidence-check --strict .` | exit 0 · 1468 ok · 0 drifted · 0 broken |
| whitespace-collapsed search for the depth-exit phrase | the phrase stands in `templates/sdd-round.md`, absent from the list |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/settle/SKILL.md` says nothing in `seal/ledger.md` moves | a comment on #511, round 1 | the repository owner |

Needs a fix: yes — finding 5 (the L6 paragraph's carrier list and its "each points at the ladder" claim are both false)
Loses a record or crashes: no
