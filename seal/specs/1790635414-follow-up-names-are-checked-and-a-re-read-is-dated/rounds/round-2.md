# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — review round 2

| Field | Value |
|---|---|
| Target SHA | 4dce9e093f5e7e495b3ca4c2122cda71eb439662 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #668 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 7 (a heading anchor GitHub builds by dropping punctuation is refused as a name after a `.md` path) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `0cfbcb55..42cd6435` at HEAD `4dce9e09`. Asked whether each verdict round 1 closed is closed, with the fixes' new units (`LINE_ANCHOR_RE` and four cases) as a finding surface, and in particular whether a false `NOT-IN-TREE` survives the heading and line-anchor fix or the lower-casing lets an invented name pass.

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

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2321`, `:2385`; `skills/evidence-check/SKILL.md:306` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2928` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2924` | round 1's 🟡 3 — fixed |
| round-1 | `.github/scripts/rider_check.py:344` | round 1's 🟡 4 — fixed |
| round-1 | `seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md` R1 | round 1's ⬜ 5 — answered |
| round-1 | `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md` | round 1's ⬜ 6 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py#check_records`, `#tree_names` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py#date_column`, `#dated_cell` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` O4, `seal/releases/0.9.0.md` R1 | round 1's 🟢 — confirmed |
| round-1 | `README.ko.md:167` | round 1's 🟢 — confirmed |
| round-1 | the pull request | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `inferred_anchor` in `.github/scripts/rider_check.py` compares a rider's splitlines line numbers against `py_spans`' `ast` numbers, so two form-feed lines above a rider move its inferred unit to the next function. It predates this branch, and `--migrate` is its only caller, with no old-form stamp left in the tree | a new issue against `rider_check.py`, candidate only | the orchestrator, who decides whether to open it; the owner answers the issue |
