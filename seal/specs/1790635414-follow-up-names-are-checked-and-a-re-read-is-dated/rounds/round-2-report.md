# 1790635414 — review round 2 report (verifying round)

Target: the fix diff `0cfbcb55..42cd6435`, read in a `--no-local` clone checked out at `4dce9e09`. The commit on top touches `rounds/round-1.md` only, so the code under review is byte-identical to `42cd6435`.

## What this round found, in one view

- Round 1's four yellows and two corrections are closed as their record states. Each new case is red when its fix is reverted (executed).
- One new yellow: finding 3's fix reaches a heading anchor only where the anchor is one of the file's words lower-cased. GitHub builds the anchor by dropping punctuation, so a heading such as `## Don't` or a code-span heading of a file name still draws a false `NOT-IN-TREE` (executed, in a fixture; no heading in this tree has that shape).
- One cosmetic: two sentences still say a row whose hash did not move is never touched, and the fix now re-points exactly such a row.
- One deferral candidate from enumerating finding 4's class: `inferred_anchor` in `.github/scripts/rider_check.py` compares splitlines numbering against `ast` numbering. It predates this branch and only `--migrate` reaches it, which has nothing left to migrate.

## Round 1's closed verdicts, one by one

**Finding 1, a move-only heal dated as a re-read — closed.** Read: `reverify` now carries a fifth element per edit, `new_hash != m.group("hash")` at `skills/evidence-check/scripts/evidence_check.py:2335`, and a row whose edits all carry `False` is spliced without being dated or named (`:2394`). A hash rewrite from the resolving branch always carries `True`, because it is only appended when the hash differs. A row mixing a moved-whole coordinate with a moved hash is dated once and keeps its re-point. Under `--checked` with no date cell, such a mixed row is left whole, re-point included, which matches the rule for a row that cannot be dated. Executed: the moved-whole case passes both parametrizations, and replacing the comparison with `True` turns both red.

**Finding 2, a cross-repo name refused where its stamp is `EXTERNAL` — closed.** Read: the branch at `evidence_check.py:2960` is reached only when the file's tokens are `None`, and its `repo == root` excludes the escaped-path case. The remaining clauses are the four `check_text` tests before it answers `EXTERNAL`, so the comment's "word for word" claim holds. A `--map` path whose file is missing still takes the old reading, where the stamp half calls it `BROKEN`, so the two halves still agree. Executed: the new case passes, and removing the branch turns it red.

**Finding 3, a heading fragment and a line anchor refused as names — closed for the two shapes it named, and the class is not.** Executed: the new case passes, and each of the two new branches, removed alone, turns it red. The remainder is finding 7 below.

The prompt asked whether lower-casing lets an invented name pass. Read: it passes only a lower-case name whose sole occurrence in that `.md` file is cased differently. Round 1 counted no `.md#name` span in this tree's records, and a `#L<n>` segment is skipped only when every segment is a line anchor. Not a finding.

**Finding 4, `region_lines` slicing splitlines — closed.** Read: `rider_check.py:344` now slices `checker.gfm_lines(text)`, and `comment_blocks` is computed on the same list, so the removed rider lines and the hashed lines share one numbering. `riders_in`, the `Rider` body and `write_block` stay on splitlines, but each uses only its own numbering, so nothing there is compared across the two. Executed: the new case passes, and reverting the line to `text.splitlines()` turns it red.

**Corrections 5 and 6 — closed.** Read: the fragment's R1 claim now says a file moved whole is re-pointed and not dated, with a `Corrected 2026-09-29` note. `phases/phase-5.md` has a row for `rider_check.py#region_lines` marked as coupled. Executed: every one of the 55 distinct anchors on the lines the fix diff added under `seal/` resolves `OK` through `check_text`. That includes the re-read rows in `seal/releases/` and the new `LINE_ANCHOR_RE` and test anchors.

## New findings

### 🟡 7 — A heading anchor GitHub builds by dropping punctuation is still refused as a name

`skills/evidence-check/scripts/evidence_check.py:2952`, in `coordinate_misses`.

The fix accepts a fragment after a `.md` path when the fragment is one of the file's tokens lower-cased. GitHub's anchor is not that. It lower-cases the heading and then removes every character except letters, digits, `_`, `-` and spaces. Where punctuation sat between two word characters, the anchor is a word that appears nowhere in the file:

- `## Don't` becomes `dont`
- a heading that is a code span of `evidence_check.py` becomes evidence_checkpy, with the dot gone
- `## v1.2` becomes `v12`

Each is a correct record that exits 2 with `NOT-IN-TREE`. The remedy the refusal offers, the name-not-in-tree marker, would put a false statement on the line. Round 1 gave the same outcome a yellow, and the fix was aimed at the instance it measured rather than at how GitHub forms the anchor (contract §12).

Executed: a fixture README with those three headings, cited from a live record, exits 2 with three `NOT-IN-TREE`. A survey of this tree's 526 single-word heading anchors found none that the lower-cased tokens miss, so nothing here is refused today. The shipped checker also runs in other repositories, and a version heading is a common shape there.

The fix adds the file's heading anchors to the tokens a `.md` path is read against. The proposed helper is below under *Paste-ready fixes*. Executed: with it applied in the clone, the case below goes from `1 failed` to passing, and the existing heading and coordinate cases in the module stay green (`12 passed`).

### ⬜ 8 — Two sentences say a row whose hash did not move is never touched

`skills/evidence-check/SKILL.md:309` and `skills/evidence-check/scripts/evidence_check.py:2216` (the `reverify` docstring). The comment block at `evidence_check.py:2107` states the owner's original answer and can stay as it is.

The SKILL.md paragraph says a file moved whole keeps its hash and is re-pointed. Its next clause then says a row whose hash did not move is never touched. Both describe the same row, and a reader cannot hold both. The behaviour and the SKILL.md clause before it are right, so this does not count toward `Needs a fix`.

## Regression tests to plant

- `tests/test_a_record_states_what_the_tree_has.py`, beside the case for round 1's finding 3: the case under *Paste-ready fixes*, shown red against the checker at `42cd6435` and green with the fix (executed in the clone).

## Facts for the evidence ledger

- When finding 7's fix lands, the fragment's row that names the three exceptions should say the heading anchor is matched against the file's GitHub heading anchors as well as its lower-cased words. It should also re-stamp `coordinate_misses` there.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 7 | A heading anchor GitHub builds by dropping punctuation (`## Don't`, a code-span file name, `## v1.2`) is refused as a name after a resolving `.md` path | `skills/evidence-check/scripts/evidence_check.py:2952` | open | executed: fixture exit 2 with three `NOT-IN-TREE`; the proposed fix's case red without it and green with it. Zero instances among 526 single-word heading anchors in this tree |
| ⬜ 8 | `reverify`'s docstring and the SKILL.md clause after the new sentence still say a row whose hash did not move is never touched, and a moved-whole row is re-pointed | `skills/evidence-check/SKILL.md:309`, `skills/evidence-check/scripts/evidence_check.py:2216` | open | read. The behaviour is right and the adjacent SKILL.md clause states it. Not counted in `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — a move-only heal is re-pointed, neither dated nor named | `skills/evidence-check/scripts/evidence_check.py:2335`, `:2394` | confirmed | executed: both parametrizations of the moved-whole case pass, and both are red with the comparison replaced by `True`. read: mixed rows are dated once, and an undatable mixed row is left whole |
| 🟢 | round 1's finding 2 is closed — a name is left unread exactly where `check_text` answers `EXTERNAL` | `skills/evidence-check/scripts/evidence_check.py:2960` | confirmed | read: the clauses match `check_text`'s, and `repo == root` excludes the escaped path. executed: the new case passes, and it is red with the branch removed |
| 🟢 | round 1's finding 3 is closed for the shapes it named — a single-word heading anchor and a `#L<n>` line anchor | `skills/evidence-check/scripts/evidence_check.py:2952`, `:2956` | confirmed | executed: the new case passes, and it is red under each branch removed alone. The rest of the class is finding 7 |
| 🟢 | round 1's finding 4 is closed — `region_lines` slices and blocks on `gfm_lines` | `.github/scripts/rider_check.py:344` | confirmed | executed: the new case passes, and it is red with `text.splitlines()` restored. read: the other splitlines users compare only against their own numbering |
| 🟢 | round 1's correction 5 is closed — the fragment's R1 claim no longer says every identical-content heal is dated | `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` R1 | confirmed | read: corrected in place with a dated note. executed: its anchors resolve `OK` |
| 🟢 | round 1's correction 6 is closed — phase 5 lists `rider_check.py#region_lines` as coupled | `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md` | confirmed | read: row present with its dated note |

## Executed probes

| What was run | Result |
|---|---|
| The fixes' cases by name through `bin/test` in the clone: the moved-whole case (two parametrizations), the renamed R6 case, the cross-repo case, the heading-and-line-anchor case, the rider-region case | exit 0, 6 passed |
| Five mutants, each with its own case: the moved-hash comparison set to `True`; the `EXTERNAL` branch removed; the lower-casing removed; the line-anchor branch removed; `region_lines` back on `text.splitlines()` | each exit 1: 2 failed, 1, 1, 1, 1 |
| Every ATX heading outside a fence in the clone's tracked `.md` files, slugged the way GitHub does, keeping the single-word slugs, checked against that file's tokens and their lower-cased forms | 526 single-word slugs, 0 unreachable |
| A live record citing three heading anchors in a fixture README: an apostrophe heading, a code-span file-name heading, a version heading | exit 2, three `NOT-IN-TREE`, `3 names read · 3 refused` |
| The proposed fix for finding 7 applied in the clone, with its case appended to the module, run with the module's heading and coordinate cases | without the fix: 1 failed, 11 passed. With it: 12 passed. Clone restored, clean |
| `check_text` over each distinct anchor on the lines the fix diff added under `seal/` | 55 anchors, 0 not `OK` |
| `rider_check.inferred_anchor` for a rider inside `g`, with 0, 1 and 2 form-feed lines above it | inferred `g`, `g`, then `f` at two form feeds. A search for old-form rider stamps outside tests found none |
| The three touched test modules as whole modules | not run in this round. Only the cases named above ran |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's once the rounds settle, and it is not due: finding 7 is open |

```text
# finding 7, the fixture
README.md:
    # Tool
    ## Don't
    ## `evidence_check.py`
    ## v1.2
seal/specs/1700000000-probe/plan.md:
    See `README.md#dont`.
    See `README.md#evidence_checkpy`.
    See `README.md#v12`.
seal/ledger/1700000000-probe.md: empty, so the work item is live
run: evidence_check.py <root>   -> exit 2, three NOT-IN-TREE

# the deferral candidate
text = "\x0c\n" * 2 + "def g():\n    # RIDER: about g. Verified 2026-01-01 against g@00000000\n    return 1\ndef f():\n    pass\n"
riders_in -> rider at line 6 (splitlines); py_spans -> g (3, 5), f (6, 7); inferred_anchor -> "f"
```

## Paste-ready fixes

### 🟡 7

```python
# skills/evidence-check/scripts/evidence_check.py, above coordinate_misses
# GitHub's anchor for an ATX heading: its text lower-cased, every character
# but a letter, digit, `_`, `-` or space dropped, and each space a `-`.
HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")


def heading_slugs(body):
    """The anchors GitHub gives BODY's headings. A fenced line is blanked
    first, so a `#` comment in a code block is not a heading."""
    slugs = set()
    for line in gfm_lines(unquoted(body)):
        m = HEADING_RE.match(line)
        if m:
            slugs.add(re.sub(r"[^\w\- ]", "", m.group(1).lower()).replace(" ", "-"))
    return slugs
```

```python
# skills/evidence-check/scripts/evidence_check.py, in coordinate_misses
            found = None if body is None else set(TOKEN_RE.findall(body))
            if found is not None and rel.endswith(".md"):
                found |= {token.lower() for token in found}
                found |= heading_slugs(body)
            file_tokens[full] = found
```

```python
# tests/test_a_record_states_what_the_tree_has.py, after
# test_a_heading_fragment_and_a_line_anchor_are_not_refused
def test_a_heading_anchor_github_strips_punctuation_from_is_not_refused(tmp_path):
    """Round 2 of 1790635414. GitHub's anchor drops every character of a
    heading but letters, digits, `_`, `-` and spaces, so `## Don't` is
    `#dont` and a code-span heading `evidence_check.py` is `#evidence_checkpy`:
    neither is a word of the file, lower-cased or not."""
    tree(
        tmp_path,
        **{"README.md": "# Tool\n\n## Don't\n\n## `evidence_check.py`\n\n## v1.2\n"},
    )
    findings, names, _ = coordinate_refusals(
        tmp_path,
        "See `README.md#dont`, `README.md#evidence_checkpy`, `README.md#v12` "
        "and `README.md#uninstall`.",
    )
    assert names == 4, findings
    assert [s for s, _, _ in findings] == ["NOT-IN-TREE"], findings
    assert "`uninstall`" in findings[0][2], findings
```

The docstring of `coordinate_misses`, the SKILL.md paragraph that names the three exceptions, and the fragment's claim row each say the heading anchor is read "lower-cased". Each should also say it is read against the file's GitHub heading anchors (contract §14).

### ⬜ 8

```text
skills/evidence-check/SKILL.md:309
-row whose hash did not move is never touched.
+row whose anchor still resolves at its recorded path and hash is never touched.

skills/evidence-check/scripts/evidence_check.py:2216 (reverify docstring)
-    whose hash moved is named, with its date as it stands. A row whose hash
-    did not move is never touched and never named.
+    whose hash moved is named, with its date as it stands. A row whose hash
+    did not move is never dated and never named; one whose file moved whole
+    is re-pointed, and one that still resolves is not touched.
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `inferred_anchor` in `.github/scripts/rider_check.py` compares a rider's splitlines line numbers against `py_spans`' `ast` numbers, so two form-feed lines above a rider move its inferred unit to the next function. It predates this branch, and `--migrate` is its only caller, with no old-form stamp left in the tree | a new issue against `rider_check.py`, candidate only | the orchestrator, who decides whether to open it; the owner answers the issue |

Needs a fix: yes — 🟡 7 (a heading anchor GitHub builds by dropping punctuation is refused as a name after a `.md` path)
Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/rounds/round-1.md` in full and `round-1-report.md` in part (its paste-ready fixes and executed probes; the middle of the file was cut from the read); the fix diff `0cfbcb55..42cd6435` in full (code hunks as a patch, record hunks at word level); `skills/evidence-check/scripts/evidence_check.py` (`place`, `cross_repo_intent`, `seal_home`, `check_text` through its `EXTERNAL` branch, the #387 comment block, `reverify`, `gfm_lines`, the record regexes, `compound`'s head, `coordinate_misses`, `file_claims`, `check_records`); `.github/scripts/rider_check.py` (the stamp regexes, `comment_blocks`, `Rider`, `riders_in`, `all_riders`, `region_lines`, `region_hash`, `check`, `write_block`, `reverify`, `inferred_anchor`); `tests/test_a_record_states_what_the_tree_has.py` (`coordinate_refusals`, the new cases); `bin/test`; the check list at the top of `skills/verify/scripts/broad_gate.py`; `docs/round-record-spec.md` on the open verdict word. Probes ran from two single-use scripts under the round's scratch directory, and the clone was removed after they ran.
