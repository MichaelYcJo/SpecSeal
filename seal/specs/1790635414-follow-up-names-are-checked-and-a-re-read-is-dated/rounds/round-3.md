# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — review round 3

| Field | Value |
|---|---|
| Target SHA | 5b115d2ef4303f02785c9a2bb400bb2e051d447c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #668 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `7ddf91eafff5042408e5d2df2f90ce76549f34a6..ba4c48f240605b9c79f99f7b10fcd3152d9b5a02`, 3 commits |
| Contract changes | none |
| New units | SETEXT_UNDERLINE_RE (depth 1); HEADING_CONTAINER_RE (depth 1); HEADING_MARKUP_RES (depth 1); github_slug (depth 1); test_a_heading_github_renders_before_it_slugs_is_not_refused (depth 1) |
| Needs a fix | yes — 🟡 9 (a real single-word heading anchor GitHub builds from a setext, quoted or listed heading, or from rendered text that differs from the source, is refused as `NOT-IN-TREE`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening. Target round 2's fix diff `ec002d24..0b3d1071` at HEAD `5b115d2e`, with `heading_slugs` and `GITHUB_HEADING_RE` as a finding surface.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | `heading_slugs` slugs a heading's source line, so a real single-word anchor GitHub builds from a setext heading, a heading behind `>` or a list marker, or a heading whose rendered text differs from its source (a link, emphasis, an entity, an inline tag) is refused as `NOT-IN-TREE` | `skills/evidence-check/scripts/evidence_check.py:2906` | **fixed** `cd4986e7` | fixed at cd4986e7 — case sharpened in `fbc8029c`: `heading_slugs` reads setext headings and headings behind `>` or a list marker, and adds the slug of the rendered text beside the source line's. The capped run's own unit, so the branch fixed it (`docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped*); no round read the fix; executed: eight fixture anchors refused, the plain ATX control passes; the proposed fix passes all eight, its case red at `5b115d2e` and green with it, whole module 101 passed. Zero instances among 532 single-word anchors in this tree. Same class as round 2's finding 7, in a unit round 2's fixes created |
| ⬜ 10 | A `#` line GitHub does not render as a heading (unclosed fence, HTML comment, front matter, `<pre>`) adds a slug, so an invented anchor equal to its punctuation-dropped words passes | `skills/evidence-check/scripts/evidence_check.py:2906` | answered | Within the price `coordinate_misses` states. `SKILL.md`'s *Known limits* now says so at `cd4986e7`, beside the anchor-name limit the round offered for deferral; executed: an invented anchor passes in each of four fixtures, refused under a closed fence. Within the price `coordinate_misses` states. Not counted in `Needs a fix` |
| 🟢 | round 2's yellow finding 7 is closed for the shapes it named — an apostrophe heading, a code-span file-name heading, a version heading | `skills/evidence-check/scripts/evidence_check.py:2906`, `:2972` | confirmed | executed: the case passes; each of three mutants (slugs not added, fences not blanked, apostrophe kept) exit 1. The rest of the class is finding 9 |
| 🟢 | round 2's correction 8 is closed — `reverify`'s docstring and the `SKILL.md` clause state what a moved-whole and an unmoved row get | `skills/evidence-check/scripts/evidence_check.py:2202`, `skills/evidence-check/SKILL.md:309` | confirmed | read: both sentences match the splice and skip paths in `reverify` |
| 🟢 | the rows round 2's fix re-pointed resolve — `reverify`, `coordinate_misses`, `heading_slugs`, the new case and the 0.8.0 `SKILL.md` section | seven ledger files in the fix diff | confirmed | executed: `evidence-check --ledger` on each, exit 0, 0 drifted, 0 broken; the work item's fragment 70 ok |
| 🟢 | round 1's findings 1 to 4 and corrections 5 and 6 stay closed — the fix diff adds one line to `coordinate_misses` and touches nothing else they rest on | `tests/test_a_record_states_what_the_tree_has.py` | confirmed | executed: the whole module at `5b115d2e`, exit 0, 100 passed |

## Paste-ready fixes

```python
# 🟡 9 — skills/evidence-check/scripts/evidence_check.py
# 1. with the other imports:
import html

# 2. replacing the comment, GITHUB_HEADING_RE and heading_slugs:
# An ATX heading's text, without its closing `#` run.
GITHUB_HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
# A setext heading's underline, and the container prefix -- a blockquote, a
# list marker -- a heading may sit behind. GitHub anchors both kinds.
SETEXT_UNDERLINE_RE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
HEADING_CONTAINER_RE = re.compile(
    r"^(?: {0,3}(?:>[ \t]?|[-*+][ \t]+|\d{1,9}[.)][ \t]+))+"
)
# GitHub slugs a heading's RENDERED text: a link's target, an inline tag and
# an emphasis run's delimiters are not in it.
HEADING_MARKUP_RES = (
    (re.compile(r"!?\[([^\]]*)\]\([^)]*\)"), r"\1"),
    (re.compile(r"<[^>]+>"), ""),
    (re.compile(r"(?<![\w*])(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1(?![\w*])"), r"\2"),
)


def github_slug(text):
    """TEXT's anchor: entities decoded, lower-cased, every character but a
    letter, digit, `_`, `-` or space dropped, each space a `-`."""
    return re.sub(r"[^\w\- ]", "", html.unescape(text).lower()).replace(" ", "-")


def heading_slugs(body):
    """The anchors GitHub gives BODY's headings: the text lower-cased, every
    character but a letter, digit, `_`, `-` or space dropped, and each space
    a `-` (round 2 of work item 1790635414). So `## Don't` is `dont` and a
    code-span heading `evidence_check.py` is `evidence_checkpy`, neither a
    word of the file. A line in a fence that closes is not a heading.

    GitHub slugs what it RENDERS (round 3): a setext heading and one behind a
    blockquote or list marker are headings too, and a link's target, an
    inline tag and an emphasis run's delimiters are not in the text. Each
    heading is slugged as written and as rendered, so the second slug adds
    only the heading's own words."""
    slugs = set()
    lines = gfm_lines(unquoted(body))
    for n, line in enumerate(lines):
        bare = HEADING_CONTAINER_RE.sub("", line)
        m = GITHUB_HEADING_RE.match(bare)
        if m:
            text = m.group(1)
        elif n and SETEXT_UNDERLINE_RE.match(bare) and lines[n - 1].strip():
            text = HEADING_CONTAINER_RE.sub("", lines[n - 1]).strip()
        else:
            continue
        slugs.add(github_slug(text))
        for pattern, repl in HEADING_MARKUP_RES:
            text = pattern.sub(repl, text)
        slugs.add(github_slug(text))
    return slugs
```
```python
# 🟡 9 — tests/test_a_record_states_what_the_tree_has.py, after
# test_a_heading_anchor_github_strips_punctuation_from_is_not_refused
def test_a_heading_github_renders_before_it_slugs_is_not_refused(tmp_path):
    """Round 3 of 1790635414, 🟡 9. GitHub slugs a heading's rendered text
    and anchors a setext heading and one inside a blockquote, so each of
    these is a real anchor of the file. An invented anchor is still refused."""
    tree(
        tmp_path,
        **{
            "README.md": "# Tool\n\nDon't\n-----\n\n> ## Won't\n\n## _Note_\n\n"
            "## [`evidence_check.py`](a.py)\n\n## Isn&#39;t\n"
        },
    )
    findings, names, _ = coordinate_refusals(
        tmp_path,
        "See `README.md#dont`, `README.md#wont`, `README.md#note`, "
        "`README.md#evidence_checkpy`, `README.md#isnt` and `README.md#uninstall`.",
    )
    assert names == 6, findings
    assert [d.split(" — ")[0] for _, _, d in findings] == [
        "`README.md#uninstall`"
    ], findings
```
```text
🟡 9 — skills/evidence-check/SKILL.md:479, the sentence it makes true
-file's words lower-cased and the anchors GitHub builds from its headings; a line
+file's words lower-cased and the anchors GitHub builds from its rendered
+headings, setext and quoted ones included; a line

seal/ledger/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated.md P2:
correct the claim in place ("the anchors GitHub gives the file's rendered
headings, setext and quoted ones included, outside closed fences") with a dated
Corrected note naming round 3's 🟡 9, re-stamp heading_slugs and
coordinate_misses, and add the new case's anchor.
```

## Executed probes

| What was run | Result |
|---|---|
| The two heading cases in `tests/test_a_record_states_what_the_tree_has.py` through `bin/test` in the clone, by name | exit 0, 2 passed |
| Round 2's three mutants of `heading_slugs`, each against its new case: slugs not added, fences not blanked, an apostrophe kept | each exit 1, 1 failed. Clone restored, clean |
| `coordinate_misses` over nine fixture READMEs, one real single-word anchor each | eight refused (setext, blockquote, list item, underscore emphasis, dunder, linked code span, entity, inline tag); the plain ATX control passes |
| `coordinate_misses` over six fixture READMEs, one invented anchor each | five pass (unclosed fence, HTML comment, front matter, `<pre>`, a dotted pair of two headings' slugs); the closed-fence control is refused |
| Every tracked `.md` file, headings modelled the way GitHub renders the eight shapes above, single-word slugs checked against what `coordinate_misses` admits | 532 single-word anchors, 0 unreachable; 18 `*.md#name` spans under `seal/` |
| The proposed fix for 🟡 9 applied in the clone, with its case | without the fix the case is exit 1, `#dont` refused first; with it the heading and coordinate cases are 15 passed, the whole module 101 passed, all eight real anchors pass, and the invented ones answer as before. Clone restored, clean |
| The whole module `tests/test_a_record_states_what_the_tree_has.py` at `5b115d2e` | exit 0, 100 passed |
| `evidence-check --ledger` over each of the seven ledger files the fix diff touched | each exit 0, 0 drifted, 0 broken; the fragment 70 ok |
| A record line citing a two-word anchor that exists, an invented two-word anchor and a digit-leading anchor | 0 names read, no finding |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet. It is the sealer's. It is not due while 🟡 9 is open; once 🟡 9 is fixed or filed, what comes due is the sealer's spawn |

```text
# 🟡 9, the fixture shapes (one README each, plus "# Tool" above)
Don't / -----                      -> #dont              refused
> ## Don't                         -> #dont              refused
- ## Don't                         -> #dont              refused
## _Note_                          -> #note              refused
## __init__                        -> #init              refused
## [`evidence_check.py`](a.py)     -> #evidence_checkpy  refused
## Don&#39;t                       -> #dont              refused
## <code>run.py</code>             -> #runpy             refused
## Don't          (control)        -> #dont              passes

# ⬜ 10, a line "# Foo's" inside each of these -> #foos
unclosed fence, HTML comment, YAML front matter, <pre> block   passes
closed fence (control)                                          refused
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
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2952` | round 2's 🟡 7 — fixed |
| round-2 | `skills/evidence-check/SKILL.md:309`, `skills/evidence-check/scripts/evidence_check.py:2216` | round 2's ⬜ 8 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2335`, `:2394` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2960` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2952`, `:2956` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `RECORD_COORD_RE` takes its name from `ANCHOR_NAME`, which has no hyphen and no leading digit, so a multi-word or digit-leading heading anchor after a `.md` path is never read and an invented one is never refused. It predates round 2; the heading handling reaches single-word anchors only | a new issue against the records arm of `evidence_check.py`, candidate only | the orchestrator, who decides whether to open it; the owner answers the issue |
