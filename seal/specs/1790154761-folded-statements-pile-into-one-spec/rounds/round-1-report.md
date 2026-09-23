# Round 1 report — #520, folded statements pile into one spec

Target: `f8f1c9de..c48d4109` (Target SHA `c48d410975c71ed4508ed299ff6b37fa7263fe02`),
branch `docs/520-folded-statements-pile-into-one-spec`, PR #527, base
`release/v0.14.0`. First round: no earlier `round-N.md` exists, so nothing was
carried. Probes ran in a `git clone --no-local` of the worktree in the session
scratchpad, which is deleted.

## What this round was asked

Round 1 over the whole branch. Stage 1 checks spec compliance against `spec.md`
and #520. Stage 2 attacks the three new checks: can a document that breaks the
rule a check states still pass it? The attack covers heading-order false
positives from `#458`-style lines, fenced blocks, HTML comments, nested
headings and `OVER_CEILING`'s equality semantics. Stage 2 also asks whether
settle §2, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md` agree with each
other and with the tests. Two questions the smith left unverified were handed
to this round: whether the Korean translation of §*What the repository
decides for itself* states the same rules as the English, and whether the
pairing test stays green after PR #525 merges. The smith's account was read
as a claim. The three modules, `evidence-check --strict` and
`unverified-check` were re-run here. The smith's red-first and mutation runs
were not repeated, and they stay labelled as the smith's.

## Stage 1 — spec compliance

All four scope items are built as `spec.md` §Scope states them. Item 1: the
Korean section and all ten markers are present, the pairing test exists, and
the `CONTRIBUTING.md` rule has been widened. Item 2: the shape check follows
the spec's grammar. Item 3: the check has the ceiling, the over-list, the
outlived-entry rule and the home #526. Item 4: settle §2 owns both rules, and
the evidence ledger holds only the values. The five divergence rows in
`overview.md` hold on reading. The one that matters below is the frozen count
compared for equality: the spec says the check "fails when a listed file
gains a marker", and an equality on the count does not do that (finding 1).

**The Korean translation (read, not executed).** I read the Korean section at
`docs/one-root-by-lifetime.ko.md` §*저장소가 스스로 정하는 것…* beside the
English at `docs/one-root-by-lifetime.md` §*What the repository decides for
itself…*. I compared the intro paragraph, each of the five bold rules, and
the grounds and the "names a checker matches stay English" paragraph that
follow them. Every rule states the same thing:

- The routing layer holds no logic of its own.
- The mirror file is named for the language it holds.
- There are three combinations, seven rows, and two audiences.
- Field names, verdict words, markers and anchors stay English.
- The reader and the writer share one row constant.
- A failed git call is named rather than reported as "nothing".

I found no rule added, dropped or softened. The five markers on the shared
sections sit directly under the same heading in both editions, above the
paragraph that carries the same statement. This confirms Q5's answer.

## Stage 2 — attacks on the three checks

**The pairing check holds against the four false positives the prompt named
(executed).** `#458 settled` is not read as a heading, because the space is
required. A heading or a marker inside a backtick fence or a tilde fence is
not read. A heading inside an HTML comment is not read, because `live_lines`
owns the comment state. A marker with a trailing space is not a marker in
either edition, which is also how the fold reads it. A setext heading in one
edition against an ATX heading in the other fails on the level sequence,
which is the safe direction. One gap is a reader gap, and no instance exists
in the tree. A CommonMark heading indented by one to three spaces is not read.
So `   ## A` in the English edition, with no such heading in the Korean,
passes (finding 5, ⬜).

**The pairing check stays green after #525 merges (executed).** I merged
`origin/fix/511-517-settle-leaves-twelve-directories-with-no-way-out`
(`29b79dc9`) into `c48d4109` in the clone. The merge was clean:
`docs/one-root-by-lifetime.ko.md`, `docs/the-evidence-ledger.md`,
`seal/ledger.md` and `skills/settle/SKILL.md` auto-merged. All 32 cases of the
three modules then passed. #525's dated section adds heading 677 to the
English edition and heading 650 to the Korean one, both at level 2, and
neither carries a marker. After the merge the chain spec is 2,175 lines and
still carries 29 markers. The settle-§2 phrase pins and the evidence ledger's
value pin also survive #525's rewrite of those two files.

**Finding 1 🟡: the frozen count passes a fold that swaps a marker
(executed).** `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems`
compares the number of markers in a listed file with the frozen number. My
probe listed a file frozen at 2 that carried one old marker and one bound
marker `1790154762-a-later-fold`, and the check returned `[]`. A new fold
into `docs/review-chain-spec.md` passes the check when the same fold removes
an older statement there. That is ordinary at a fold, because settle keeps
only what is still true, so a superseded statement goes out as the new one
comes in. The spec's sentence is "fails when a listed file gains a marker",
and ledger row P1 says the same. Placement is the rule this check exists to
hold at the 0.14.0 fold, and a swap is the one change it cannot see. The fix
freezes which markers are present, not only how many. A digest of the sorted
ids does that without the 92-entry list that `plan.md` §*Alternatives*
row 4 rejected. The digest is `8f8c4d85f213` at `c48d4109`. #525 adds no
marker, so the value holds after that merge too.

**Finding 2 🟡: a target that names no file still "resolves" (executed).**
`tests/test_a_folded_statement_names_what_enforces_it.py#target_problem`
tests existence with `os.path.exists` on an unnormalised join. The probe
showed three targets passing:

- `Enforced by: .` passes, because the root directory exists.
- `Enforced by: ../outside.txt` passes, although the file is outside the
  root.
- A directory passes as a target.

Ledger row S1 says each target resolves "to a file", and settle §2 says "A
target is a repository path". The check can pass a statement that names
nothing, which is exactly what the `Enforced by:` line exists to prevent. The
check itself admits that it cannot tell whether a target really enforces the
rule. It should still refuse a target that is not a file in the repository.

**Finding 3 ⬜: the evidence ledger's exemption sentence reads as covering
only the past (read).** `docs/the-evidence-ledger.md` §*The fold, and what
tells it from a deletion*, first bullet: "The shape binds statements from work
item `1790154761` on. The 101 folded before it carry no `Enforced by:` line."
Marker ids are the retired work item's ids, not the fold's. So the 0.14.0 fold
of #515 (`1790134781`), #517 (`1790138190`) and `1790119502` also folds
without the line. So does any fold of the twelve older directories #517 deals
with. `plan.md` §*Operational impact* says this is intended, so it is grounds
and not a defect. The rule stands, but the sentence implies the 101 are the
whole exempt set. The fenced fix states the set by id. The same statements
also fall outside #526's retrofit item, which counts "the 101". That goes
under Deferred.

**Finding 4 ⬜: settle §2 says "closes with" while the check reads "carries"
(executed).** Settle §2 says a statement "closes with exactly one line of its
own that names what reads the rule". `#shape_problems` counts the
`Enforced by:` lines anywhere in the statement. An `Enforced by:` line
followed by more grounds passes. The spec (§Scope item 2, "carries exactly
one line") agrees with the check, so the fix belongs in settle's wording. In
the same function, `body[0].startswith("**")` accepts a first line that is
only `**`. The probe returned `[]` for `**` followed by
`Enforced by: nothing — r`. Neither ships a defect, so both are ⬜.

**Finding 5 ⬜: the heading pattern misses CommonMark headings indented by
one to three spaces (executed).** See the pairing paragraph above. No
top-level `docs/` file has such a heading today.

**Other attacks that held (executed).**

- `Enforced by:` inside an HTML comment is not counted.
- An indented `Enforced by:` is not counted.
- `nothing —` with no reason fails.
- A bare `nothing` falls through to target resolution and fails.
- The `OVER_CEILING` boundary is right: the check lets a file of exactly
  `LINE_CEILING` lines through and fails at `LINE_CEILING + 1`. The planted
  cases cover both sides, and the spec says "at or under".

**The three prose documents agree with each other and with the tests
(read).** Settle §2, `CONTRIBUTING.md` §*House rules* and the evidence ledger
say the same thing as the three modules. The one mismatch in wording is
finding 4. `CONTRIBUTING.md`'s sentence describes exactly what
`#disagreements` compares. The evidence ledger's three values are pinned by
`test_the_evidence_ledger_states_the_values_these_constants_hold`, and the
module is green at `c48d4109`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The frozen marker count passes a fold that adds a marker to the listed document and removes another, so the placement rule the 0.14.0 fold is held to has a hole | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | open | Executed: a planted listed file frozen at 2, carrying one old and one bound marker, returned `[]`. `spec.md` §Scope item 3 and ledger row P1 say "fails when a listed file gains a marker" |
| 2 | 🟡 An `Enforced by:` target that is the root (`.`), a directory, or a path outside the repository (`../x`) passes resolution | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | open | Executed: `.` and `../outside.txt` both returned `[]`. Ledger row S1 says each target resolves "to a file"; settle §2 says "a repository path" |
| ⬜ | The evidence ledger's "The 101 folded before it" reads as the whole exempt set, while #515's, #517's and `1790119502`'s statements folded at 0.14.0 are exempt too | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, first bullet | correction | Read. Marker ids are the retired work item's. `plan.md` §*Operational impact* makes the exemption intended, so only the sentence is corrected |
| ⬜ | Settle §2 says the statement "closes with" the `Enforced by:` line, while the check accepts it anywhere; a first line of bare `**` counts as bold | `skills/settle/SKILL.md` §*2. Write one standing statement per segment*; `tests/test_a_folded_statement_names_what_enforces_it.py#shape_problems` | correction | Executed for both. `spec.md` §Scope item 2 says "carries", so the wording is what moves |
| ⬜ | A heading indented one to three spaces is a CommonMark heading that the pairing reader skips | `tests/test_both_editions_carry_the_same_folds.py#outline` | correction | Executed: `   ## A` in one edition only returned `[]`. No instance in the tree |
| 🟢 | The Korean §*저장소가 스스로 정하는 것…* states the same rules as the English §*What the repository decides for itself…* | `docs/one-root-by-lifetime.ko.md` | verified | Read side by side, paragraph by paragraph; no rule added, dropped or softened |
| 🟢 | The pairing test, and the other two modules, stay green once PR #525's branch is merged | `tests/test_both_editions_carry_the_same_folds.py` | verified | Executed: clean merge of `29b79dc9` into `c48d4109`, 32 passed |
| 🟢 | `#458`-style lines, fenced markers and headings (backtick and tilde), headings in HTML comments, and `Enforced by:` in a comment or indented are all not read | the three new modules | verified | Executed, planted inputs through each module's own functions |
| 🟢 | The ceiling is inclusive and the outlived-entry and missing-file rules fire | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | verified | Read, and the module's planted cases executed green |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three new modules at `c48d4109`, in the clone | 32 passed |
| `bin/test` over `test_settle_reads_before_it_removes`, `test_docs_line_wrap`, `test_the_rules_have_one_owner` at `c48d4109` | 154 passed |
| `bin/evidence-check --strict .` at `c48d4109` | exit 0 |
| `bin/unverified-check` at `c48d4109` | exit 0 |
| Merge of `29b79dc9` (PR #525's head) into `c48d4109`, then the three new modules | clean merge; 32 passed |
| One `test_tmp_` probe with planted inputs through `#shape_problems`, `#ceiling_problems`, `#disagreements` | swap in a listed file `[]`; `Enforced by: .` `[]`; `../outside.txt` `[]`; bare `**` `[]`; indented `   ## A` `[]`; HTML-comment and indented `Enforced by:` named; setext against ATX named. Probe file and clone deleted |
| Digest of the sorted live marker ids of `docs/review-chain-spec.md` at `c48d4109` | 29 ids, `8f8c4d85f213` |
| The smith's red-first runs and per-unit mutations | not re-run here: they are the smith's account, read as claims |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet run; the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Statements folded at 0.14.0 from work items below the cutoff (#515 `1790134781`, #517 `1790138190`, `1790119502`, and the older directories #517 deals with) carry no `Enforced by:` line, and #526's retrofit item names only "the 101" | MichaelYcJo/SpecSeal#526, retrofit checklist item widened to name them | the orchestrator, who filed #526 and edits its checklist |

## Paste-ready fixes

Finding 1. Freeze which markers are present, as a digest, beside the count.
The constant's value was measured at `c48d4109`. The evidence ledger's value
pin reads `OVER_CEILING` only, so it needs no change.

```python
# tests/test_a_document_has_room_for_the_next_fold.py — beside OVER_CEILING
import hashlib

# Which markers the listed document holds, not only how many: a fold that
# adds one statement and removes another keeps the count and changes this.
# Recompute with marker_digest() when a marker is deliberately removed.
FROZEN_IDS_DIGEST = {
    "docs/review-chain-spec.md": "8f8c4d85f213",
}


def marker_digest(text):
    ids = sorted(
        found
        for line, live in uc.live_lines(text.splitlines())
        if live
        for found in uc.FOLD_MARKER.findall(line)
    )
    return hashlib.sha256("\n".join(ids).encode()).hexdigest()[:12]


# in ceiling_problems, take the digests as a parameter
# (`def ceiling_problems(root, ceiling, over, digests=None):`) and, after the
# `found != frozen` block:
        want = (digests or {}).get(rel)
        if want is not None and found == frozen and marker_digest(text) != want:
            problems.append(
                f"{rel} carries {frozen} fold markers, but not the ones frozen "
                f"until {home} splits it. A fold that adds a statement here and "
                "removes another keeps the count; the new rule goes to the "
                "document for its own sub-subject"
            )

# the real-tree case passes FROZEN_IDS_DIGEST; a planted case:
def test_a_marker_swapped_into_the_listed_document_is_named(tmp_path):
    root = tree(tmp_path, {"big.md": body(12, 2)})
    digest = marker_digest(body(12, 2))
    swapped = "<!-- specs/1790154762-new -->\n" + body(11, 1)
    (tmp_path / "docs" / "big.md").write_text(swapped, encoding="utf-8")
    found = ceiling_problems(root, 10, OVER, {"docs/big.md": digest})
    assert len(found) == 1 and "but not the ones frozen" in found[0], found
```

Finding 2. Normalise the target, keep it inside the root, and require a file.

```python
# tests/test_a_folded_statement_names_what_enforces_it.py — target_problem
    path, _, name = target.partition("::")
    base = os.path.normpath(root)
    full = os.path.normpath(os.path.join(base, *path.split("/")))
    if full == base or os.path.commonpath([full, base]) != base:
        return f"{path} is not a path inside the repository"
    if not os.path.isfile(full):
        return f"{path} is not a file in the repository"
    if not name:
        return None
    if not path.endswith(".py"):
        return f"{target}: `::name` needs a Python file"
    # the rest of the function (ast lookup) is unchanged


# one planted tree per target, because planted() creates tests/ each time
def test_a_target_that_is_not_a_file_in_the_repository_is_named(tmp_path):
    for i, target in enumerate((".", "tests", "../outside.txt")):
        sub = tmp_path / f"t{i}"
        sub.mkdir()
        (tmp_path / "outside.txt").write_text("x")
        found = planted(sub, f"**Rule.**\nEnforced by: {target}\n")
        assert len(found) == 1 and "repository" in found[0], (target, found)
```

Finding 3 (⬜, correction), `docs/the-evidence-ledger.md`, first bullet:

```markdown
- The shape binds statements from work item `1790154761` on, by the id in
  the marker. Statements from earlier work items carry no `Enforced by:`
  line, whenever they are folded: the 101 folded before it, and those of
  work items released with it or waiting before it.
```

Finding 4 (⬜, correction), `skills/settle/SKILL.md` §2, the shape rule's
second sentence:

```markdown
it.** It opens with the rule as one bold sentence, and the grounds follow as
prose. It carries exactly one line of its own that names what reads the
rule, and that line is written last:
```

Needs a fix: yes — findings 1 and 2: the frozen count passes a marker swap
into the listed document, and a target of `.`, a directory or `../x` resolves

Loses a record or crashes: no

## Regression tests to plant

- `tests/test_a_document_has_room_for_the_next_fold.py`: a swap case, one
  marker out and one in at the same count (the fenced case under finding 1).
- `tests/test_a_folded_statement_names_what_enforces_it.py`: `.`, a
  directory and `../outside.txt` as targets, each named (finding 2).

## Facts for the evidence ledger

- P1's `Verified behavior` should say that a swap at equal count is refused
  once finding 1 is fixed, and name the digest constant.
- S1 already claims "resolve to a file". It is true only after finding 2's
  fix, so re-verify S1 then.

## Proof block

Opened: `spec.md`, `questions.md`, `overview.md`, `plan.md` (lines 40–60,
66–78, 120–132), `changelog.md`; the full diff of `CONTRIBUTING.md`,
`docs/one-root-by-lifetime.ko.md`, `docs/the-evidence-ledger.md`,
`seal/ledger.md`, `skills/settle/SKILL.md` and
`seal/ledger/1790154761-folded-statements-pile-into-one-spec.md`; the three
new test modules in full; `skills/verify/scripts/unverified_check.py`
(`FOLD_MARKER`, the top of `live_lines`); the English
§*What the repository decides for itself…*; `tests/test_docs_line_wrap.py`
(`COVERED`); `bin/test`; `skills/code-review/scripts/round_record.py`
(finding-id and open-word rules); the #525 branch's diff stat and its merged
fold section of `docs/the-evidence-ledger.md`.
