# 1790154761-folded-statements-pile-into-one-spec — review round 1

| Field | Value |
|---|---|
| Target SHA | c48d410975c71ed4508ed299ff6b37fa7263fe02 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 527 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `edcd2e3312c6b35323bb3f7e13d605e14ad2aa6a..ca3808375a700e401f7826d0e4f515f0394c74d2`, 1 commit |
| Contract changes | ceiling_problems → round-1-report.md, round-1.md, pytest |
| New units | FROZEN_IDS_DIGEST (depth 1); marker_digest (depth 1); test_a_marker_swapped_into_the_listed_document_is_named (depth 1); test_the_frozen_digest_is_the_listed_document_s_markers (depth 1); BOLD_OPENING (depth 1); test_a_target_that_is_not_a_file_in_the_repository_is_named (depth 1); test_a_bare_bold_delimiter_is_not_a_rule_sentence (depth 1); test_a_heading_indented_up_to_three_spaces_is_read (depth 1) |
| Needs a fix | yes — findings 1 and 2: the frozen count passes a marker swap into the listed document, and a target of `.`, a directory or `../x` resolves |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 over the whole branch `f8f1c9de..c48d4109`. Stage 1 checked spec compliance against `spec.md` and #520. Stage 2 attacked the three new checks: whether a document that breaks the rule a check states can still pass it. It covered heading-order false positives from `#458`-style lines, fenced blocks, HTML comments, nested headings and `OVER_CEILING`'s equality semantics. Stage 2 also asked whether settle §2, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md` agree with each other and with the tests. Two questions the smith left unverified were handed to this round: whether the Korean translation of §*What the repository decides for itself* states the same rules as the English, and whether the pairing test stays green after PR #525 merges.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The frozen marker count passes a fold that adds a marker to the listed document and removes another, so the placement rule the 0.14.0 fold is held to has a hole | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | **fixed** `ca380837` | fixed at ca380837 — `ceiling_problems` compares a digest of the sorted marker ids beside the count (`FROZEN_IDS_DIGEST`, `marker_digest`); Executed: a planted listed file frozen at 2, carrying one old and one bound marker, returned `[]`. `spec.md` §Scope item 3 and ledger row P1 say "fails when a listed file gains a marker" |
| 2 | 🟡 An `Enforced by:` target that is the root (`.`), a directory, or a path outside the repository (`../x`) passes resolution | `tests/test_a_folded_statement_names_what_enforces_it.py#target_problem` | **fixed** `ca380837` | fixed at ca380837 — `target_problem` normalises the target, refuses a path outside the root, and requires a file; Executed: `.` and `../outside.txt` both returned `[]`. Ledger row S1 says each target resolves "to a file"; settle §2 says "a repository path" |
| ⬜ | The evidence ledger's "The 101 folded before it" reads as the whole exempt set, while #515's, #517's and `1790119502`'s statements folded at 0.14.0 are exempt too | `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, first bullet | correction | Read. Marker ids are the retired work item's. `plan.md` §*Operational impact* makes the exemption intended, so only the sentence is corrected |
| ⬜ | Settle §2 says the statement "closes with" the `Enforced by:` line, while the check accepts it anywhere; a first line of bare `**` counts as bold | `skills/settle/SKILL.md` §*2. Write one standing statement per segment*; `tests/test_a_folded_statement_names_what_enforces_it.py#shape_problems` | correction | Executed for both. `spec.md` §Scope item 2 says "carries", so the wording is what moves |
| ⬜ | A heading indented one to three spaces is a CommonMark heading that the pairing reader skips | `tests/test_both_editions_carry_the_same_folds.py#outline` | correction | Executed: `   ## A` in one edition only returned `[]`. No instance in the tree |
| 🟢 | The Korean §*저장소가 스스로 정하는 것…* states the same rules as the English §*What the repository decides for itself…* | `docs/one-root-by-lifetime.ko.md` | verified | Read side by side, paragraph by paragraph; no rule added, dropped or softened |
| 🟢 | The pairing test, and the other two modules, stay green once PR #525's branch is merged | `tests/test_both_editions_carry_the_same_folds.py` | verified | Executed: clean merge of `29b79dc9` into `c48d4109`, 32 passed |
| 🟢 | `#458`-style lines, fenced markers and headings (backtick and tilde), headings in HTML comments, and `Enforced by:` in a comment or indented are all not read | the three new modules | verified | Executed, planted inputs through each module's own functions |
| 🟢 | The ceiling is inclusive and the outlived-entry and missing-file rules fire | `tests/test_a_document_has_room_for_the_next_fold.py#ceiling_problems` | verified | Read, and the module's planted cases executed green |

## Paste-ready fixes

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
```markdown
- The shape binds statements from work item `1790154761` on, by the id in
  the marker. Statements from earlier work items carry no `Enforced by:`
  line, whenever they are folded: the 101 folded before it, and those of
  work items released with it or waiting before it.
```
```markdown
it.** It opens with the rule as one bold sentence, and the grounds follow as
prose. It carries exactly one line of its own that names what reads the
rule, and that line is written last:
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Statements folded at 0.14.0 from work items below the cutoff (#515 `1790134781`, #517 `1790138190`, `1790119502`, and the older directories #517 deals with) carry no `Enforced by:` line, and #526's retrofit item names only "the 101" | MichaelYcJo/SpecSeal#526, retrofit checklist item widened to name them | the orchestrator, who filed #526 and edits its checklist |
