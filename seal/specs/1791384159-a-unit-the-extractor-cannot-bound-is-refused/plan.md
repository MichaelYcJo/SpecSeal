# Implementation Plan: a unit the extractor cannot bound is refused (#870, #848)

<!-- seal/specs/1791384159-a-unit-the-extractor-cannot-bound-is-refused/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

Replace one guess with a table of rules that each refuse what they do not
recognise. Brace languages are bounded by a bracket walk that ends at balance
and refuses imbalance; YAML keeps its indentation rule, stated as YAML's own
structure, with the compact sequence added; Python is `ast` or a refusal, never
the text rule; every other suffix refuses a bare symbol and names the
quoted-line anchor as the way. The closing line of a brace unit stays out of
the span, so a row the old rule bounded right keeps its hash and the only
`DRIFTED` an installer meets on upgrade is a body the old span left out.

## Technical context

All coordinates at 5623d728 (0.20.0 as shipped), re-read in the worktree.

- `skills/evidence-check/scripts/evidence_check.py#resolve_unit` (L614–674):
  the quoted arm, the `.py` arm with the `SyntaxError` fall-through at L657–666
  ("The fallback survives only for the file ast cannot read at all"), and the
  default `return generic_units(lines, locator)`.
- `#generic_units` + `STATEMENT_WORDS` (L677–790): the opener regex at L743
  `^(?P<pre>[\w\s*&]*?)\b<name>\s*(?P<delim>[({=]|:)`, the indentation loop
  at L759–765, the `bare_one_liner` and resurrection logic after it. The loop
  is the only part that changes; everything from `pre_words` down is kept.
- `#py_spans`/`#parsed_spans` (L442–514): `None` for a `SyntaxError`, memoised
  per text with `functools.cache`; the memo shape the lexed stream copies.
- `#minor_region` (L869), `#file_units` (L912, the opener copy at L943),
  `#content_matches` (L1000, `markdown = rel.endswith(".md")`): the other three
  suffix dispatches.
- `#judge` (L1669–1831): `places, resurrected = resolve_unit(...)` at L1739;
  the `locator not found` branch at L1778–1810 is where the refusal's line
  goes, before the rename scan, because a refused unit is not a moved one.
- `.github/scripts/rider_check.py#region_lines` (L470–500): unpacks the
  two-tuple, answers "the anchor resolves to nothing in this file".
- `skills/code-review/scripts/survivor_check.py` `resolves` (L1262–1264):
  `bool(loaded.resolve_unit(*anchor, text)[0])`.
- `hooks/evidence-advisor.py` (L112): imports the checker by path at every
  commit, so an installer's plugin update changes the reading at once.
- `skills/evidence-check/SKILL.md` §*Resolving a unit without a parser*
  (L87–136), §*What the region is* (L403–422), §*Known limits* (L680–755,
  the closing-brace bullet at L746–748).
- Tests that pin the old bound: `tests/test_a_row_points_by_content.py`
  `test_the_major_unit_resolves_without_a_parser` (L482, docstring states the
  indentation rule), `test_a_bare_mention…` (L643, "stops AT the closing
  brace"), `test_a_multi_line_declaration_with_a_bare_name_is_still_sure`
  (L2942, a shell-function fixture reached through `generic_units` directly).
- Probe executed 2026-10-07 on Python 3.13.5, deleted after: the spans in
  `spec.md` §*Scope*'s first paragraph and S7's three repository coordinates.

**The failure scenario of the chosen approach, in six months.** A string or
comment form the lexer does not blank in an allow-listed language — a Rust
`r#"…"#`, a C++ `R"(…)"`, a Swift `"""` — carries a brace that re-balances by
accident, and the walk ends the unit early or late without a word. The bound
on it: the list is an allow-list with a case per form, so the next such form
is one row and one case, never a second reading; and an imbalance that does
not re-balance is a refusal, which is loud. The second scenario: a formatter
puts the opening `{` on a line of its own with a deeper indent (GNU style),
which the "next non-blank line opens with `{`" clause still reads. The third:
somebody adds a language to the list without its forms, which Q1 is written
to refuse.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#848's own fix** — a line that is only a closing paren continuing the declaration (`): T {`, `) {`, `] = {`) does not end the block | Allman `{` on its own line is still cut; a multi-line generic `>(` or a `}` of an object-type parameter at the declaration's indent still ends it; every new formatter shape is a new clause. That is the reader-of-more-shapes family #834's table shows did not converge | refused |
| **A per-language parser** (tree-sitter or one grammar per language) | `evidence-ci` vendors the checker as one stdlib file into a consumer's `tools/`; a parser is a dependency to vendor and a grammar per language to version, and the row that cites the parser's answer is only as stable as that grammar | refused |
| **Refuse every bare symbol outside `.py` and `.md`** (the narrowest promise) | Honest, and every TypeScript, Go, Java or Kotlin repository that adopted the skill loses symbol anchors entirely and falls to quoted lines, the brittle form the rule exists to avoid; #848's reporter loses the one anchor the issue is about; this repository's seven bare YAML rows go `BROKEN` | refused |
| **The bracket walk, and include the closing line in the span** | Every brace-language row in every installer's ledger drifts once on upgrade, right ones and wrong ones in one wave, so the installer runs `--reverify` over all of them and the rows that were `ok` over an unread body are re-stamped unread. Leaving the closer out makes every `DRIFTED` in the wave a real one | refused |
| **Keep the Python `SyntaxError` fall-through** (Python is an indentation language, so the guess is usually right) | A multi-line `def f(` / `    a,` / `):` leaves the body out exactly as #848 does (executed: lines 1–3 of 5), silently, on every interpreter older than the file's syntax | refused |
| **The bracket walk for an allow-list of brace languages, the block rule for YAML, `ast` or refusal for Python, a refusal elsewhere, closer line left out** | the six-month scenario above | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
narrow check for every phase is the slice of
`tests/test_a_row_points_by_content.py` it touches plus the cases it plants;
no phase runs the suite, the repository-wide lint or the typecheck
(agent-contract §2). Each new case is shown red first and the hand-back says
how (§15).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The table and the refusal.** `bounding_rule(path)`; the four suffix dispatches read it; `resolve_unit` carries a refusal reason in one reading (Q4) and the three callers unpack it; `.py` that will not parse and a suffix with no rule are `BROKEN` with the reason and the quoted-line remedy on the line; `--reverify` prints and writes nothing. Brace suffixes and YAML still go through today's `generic_units` in this phase. Cases S5, S6, S8, S10 red then green | the cases; the `resolve_unit`/`judge` slice of `tests/test_a_row_points_by_content.py`; `tests/test_a_rider_reaches_its_file.py` | cfcd630d |
| 2 | **The bracket walk.** The lexer (comments, strings, template literals, char literals; forms per language from Q1) memoised per text; the depth walk with the Allman clause and the deeper-continuation clause; the closer-only last line left out; imbalance and an unterminated literal refused; the day-one list; `file_units` on `generic_units`'s opener; the shell-shaped fixture of `test_a_multi_line_declaration_with_a_bare_name_is_still_sure` re-fixtured in a brace language, keeping the property it pins; #848's reproduction as a case. Cases S1, S2, S3, S4, S9 red then green | the cases; the `generic_units`/`file_units`/`content_matches` slice | 0011e870 |
| 3 | **YAML as a declared block rule.** `"block"` for `.yml`/`.yaml` with the compact-sequence item at the key's indent; the three repository coordinates in S7 keep their spans; `bin/evidence-check --strict .` on the branch shows no `BROKEN` and no `DRIFTED` that `main` does not show (Q2 measured here). Case S7 red then green | the case; the executed `--strict .` output, quoted in `phases/phase-3.md` | a2bc18ec |
| 4 | **The documents and the records.** `SKILL.md`'s three sections and the `BROKEN` verdict row; the `docs/the-evidence-ledger.md` paragraph with `Enforced by:`; the docstrings' input class in #835's three words; `changelog.md` with the installer paragraph; `seal/ledger/<work-item-id>.md` rows for the new clauses; the sentences *In* 5 removes are gone. Cases S11, S12 | the hygiene tests the brief names; `tests/test_a_record_states_what_the_tree_has.py`; `tests/test_the_fixes_name_their_surface.py` | 951b0a1d |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Seams with the sibling frames

- **#867** (`seal/config.md` rows, the coordinate grammar, markdown headings
  — `evidence_check.py#heading_level`, `#ANCHOR_RE`, `#frozen_from`). This
  item does not touch those units. Shared units: `file_units`'s `.md` arm
  calls `heading_level`, and `resolve_unit`'s quoted arm calls
  `heading_path`; if #867 moves either, the arm follows the move, and the
  suffix table here is the one place the `.md` dispatch lives after phase 1.
  Whichever lands second rebases; no cell of the table is #867's.
- **#836** (a row's claim is the test that enforces it). The row grammar,
  `ANCHOR_RE` and `Verdict` are unchanged here; what #836 may change is what
  a row's evidence is. The seam is `judge`'s `BROKEN` detail text: if #836
  gives a row a test node id beside its code anchor, the anchor's bound is
  still this item's, and a refusal still reads `BROKEN` on that anchor.
- **#835** (a reader declares its input class). The table in `spec.md` *In*
  1 is written in #835's three words so its registry can read it; this item
  does not write the registry.
- Nothing shared with #866, #869, #868, #860, #858, #864, #837.

## What this removes

The indentation bound for brace languages; the opener's second spelling at
`file_units`; the `SyntaxError` fall-through and its comment; three of four
suffix dispatches; the three sentences `spec.md` *In* 5 names. What it adds is
one lexer and one walk, both behind an allow-list that refuses what it does
not name, and one table.

## Operational impact

- **Every installer**, at the next plugin update (the commit hook) and at the
  next `/specseal:evidence-ci` re-run (the CI copy): rows citing a
  brace-language unit whose body the old span left out read `DRIFTED` once;
  rows citing a bare symbol in a suffix with no rule, or in a `.py` the
  interpreter cannot parse, read `BROKEN` with the remedy; everything else
  keeps its hash. The changelog fragment says so and says what to run. Under
  a freeze a released `BROKEN` row takes the `Corrected ·` repair the policy
  already names.
- **This repository**: no row changes verdict (Q2 measures it in phase 3).
- No new dependency, no new env var, no migration, no change to
  `templates/evidence-check.yml` or to the vendored-copy test.
- The release carrying this is 0.21.0, already a minor.
