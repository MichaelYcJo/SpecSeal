# 1790635414 — review round 3 report (verifying, the run's last)

## What this round was asked

Round 3 is a verifying round over round 2's fix diff `ec002d24..0b3d1071`, with the branch at `5b115d2e`. The commit on top is round 2's close, and it touches `rounds/round-2.md` alone. The questions were whether 🟡 7 (`fixed`) and ⬜ 8 (`answered`) are actually closed, and what the new units `GITHUB_HEADING_RE` and `heading_slugs` and their one case get wrong in either direction: an invented anchor they now let through, and a real GitHub anchor they still refuse.

The account under review said that `heading_slugs` adds "the anchors GitHub gives BODY's headings". It says so in the unit's docstring, in the `SKILL.md` sentence at `skills/evidence-check/SKILL.md:479`, and in the fragment's P2 claim. This round checked that sentence against the code, and it holds only for one shape of heading.

## Summary

- 🟡 7 is closed for the three shapes it named. The case passes, and each of round 2's three mutants turns it red.
- The class 🟡 7 belongs to is still open, as 🟡 9. `heading_slugs` slugs a heading's source line as it is written. GitHub slugs the heading's rendered text, and it anchors headings this unit never sees. Eight real single-word anchors of that kind are refused.
- ⬜ 8 is closed. The docstring and the `SKILL.md` clause now say what `reverify` does.
- ⬜ 10 is the other direction. A `#` line GitHub does not render as a heading still adds a slug, so an invented anchor spelled from that line's words passes.
- The rows the fix re-pointed resolve, and round 1's closures still stand.

## 🟡 9 — a real anchor is refused when GitHub renders the heading before it slugs it

**Where.** `skills/evidence-check/scripts/evidence_check.py:2906`, `heading_slugs`.

**What is wrong.** The loop matches `GITHUB_HEADING_RE` against the raw line and slugs the captured source text. GitHub does two things this loop does not.

- It anchors headings that do not begin a line with `#`: a setext heading (text on one line, `---` or `===` under it), and an ATX heading behind a blockquote `>` or a list marker.
- It slugs the heading's rendered text. A link's target, an inline tag, the delimiters of an emphasis run and an HTML entity are not in that text. So a heading written as a link to a code-span file name has the anchor `#evidence_checkpy`, where this unit adds `evidence_checkpy` followed by the words of the link target. `## __init__` renders bold, and its anchor is `#init`.

**Executed.** `coordinate_misses` refused all eight in fixture READMEs: a setext `Don't`, `> ## Don't`, `- ## Don't`, an underscore-emphasised `Note`, `## __init__`, the linked code-span heading, `## Don&#39;t`, and `## <code>run.py</code>`. The control, a plain `## Don't`, passes.

**Why it matters.** Each refusal is a `NOT-IN-TREE` at exit 2 on a record citing a heading its file does have. `SKILL.md:479` tells the reader this fragment is not refused. This is the same class round 2 opened as 🟡 7, "a heading anchor GitHub builds by dropping punctuation is refused". A setext `Don't` is exactly that case, reached through a heading shape the fix did not enumerate. The unit is new in this run's fixes, so this is the branch's to fix whatever the cap decides.

**How much it costs here.** Nothing in this repository today. Over the tracked `.md` files, I modelled GitHub's rendering for the eight shapes above and found 532 single-word anchors, none unreachable. Records under `seal/` cite 18 `*.md#name` spans in all. The refusal lands in a user's repository whose README writes one of these shapes.

**The fix.** Strip a container prefix before matching. Take a setext heading from the line above its underline. Slug each heading twice, once as written and once with the link target, inline tags and emphasis delimiters removed, and decode entities in both. Adding a second slug per heading only admits the heading's own words, so it widens nothing an invented name can reach. I applied the fix below in the clone. It turns the new case green, and all eight fixture anchors then pass. Every invented-anchor probe in ⬜ 10 answers the same as before the fix. The whole module passes, 101 cases.

## ⬜ 10 — a `#` line GitHub does not render as a heading still adds a slug

**Where.** `skills/evidence-check/scripts/evidence_check.py:2906`, `heading_slugs`.

**What is wrong.** `unquoted` blanks only a fence that closes, and it is the only exclusion. A `#` line in an unclosed fence, in an HTML comment, in YAML front matter or in a `<pre>` block is read as a heading. GitHub renders none of the four as one. Executed: an invented `#foos` passes in each of the four fixtures, from a line `# Foo's`. A closed fence refuses it.

**Why it is ⬜.** An invented anchor passes only when it equals the punctuation-dropped words of such a line, which the file already carries one by one. That sits inside the price the docstring of `coordinate_misses` already states: a name that survives only in a comment of the named file passes. No fix is owed. The docstring's last sentence, "A line in a fence that closes is not a heading", is accurate as far as it goes.

## Closures checked

- **🟡 7, the shapes it named.** Executed: `test_a_heading_anchor_github_strips_punctuation_from_is_not_refused` passes. Each of round 2's three mutants turns it red: the slugs not added, fences not blanked, an apostrophe kept. The fenced `# Fenced's` in the case is what the second mutant needs, and it does fail without the fence blanking. The rest of the class is 🟡 9.
- **⬜ 8.** Read: `reverify`'s docstring at `:2202` now says a moved-whole row is re-pointed and an unmoved one is neither dated nor named. The code agrees. A reconstruction whose new hash equals the recorded one is spliced without dating, and a resolving row whose hash matches is skipped. `SKILL.md:309` says the same.
- **The re-anchored rows.** Executed: `evidence-check --ledger` over each of the seven ledger files the fix diff touched exits 0 with nothing drifted or broken. The work item's fragment reads 70 ok.
- **Round 1's closures.** The fix diff adds one line to `coordinate_misses` and nothing else they rest on. Executed: the whole module passes at `5b115d2e`, 100 cases.

## Regression tests to plant

`tests/test_a_record_states_what_the_tree_has.py`, directly after `test_a_heading_anchor_github_strips_punctuation_from_is_not_refused`: the case in the second block under `## Paste-ready fixes`. It was seen red against `5b115d2e`: exit 1, with `#dont` refused as the first of five findings. It is green with the fix, and the whole module then passes 101.

## Facts for the evidence ledger

- The fragment's P2 claim ("against the anchors GitHub gives the file's headings outside closed fences") becomes true only once 🟡 9 is fixed. It is corrected in place with a dated note in the same commit, and `heading_slugs` is re-stamped.
- `ANCHOR_NAME` admits no hyphen and no leading digit, so `RECORD_COORD_RE` never matches a multi-word or digit-leading heading anchor. Executed: a record line citing a two-word anchor that exists, an invented two-word anchor, and a digit-leading anchor reads 0 names and refuses none. The heading-anchor handling therefore reaches single-word anchors only. That is the deferral candidate below.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | `heading_slugs` slugs a heading's source line, so a real single-word anchor GitHub builds from a setext heading, a heading behind `>` or a list marker, or a heading whose rendered text differs from its source (a link, emphasis, an entity, an inline tag) is refused as `NOT-IN-TREE` | `skills/evidence-check/scripts/evidence_check.py:2906` | open | executed: eight fixture anchors refused, the plain ATX control passes; the proposed fix passes all eight, its case red at `5b115d2e` and green with it, whole module 101 passed. Zero instances among 532 single-word anchors in this tree. Same class as round 2's finding 7, in a unit round 2's fixes created |
| ⬜ 10 | A `#` line GitHub does not render as a heading (unclosed fence, HTML comment, front matter, `<pre>`) adds a slug, so an invented anchor equal to its punctuation-dropped words passes | `skills/evidence-check/scripts/evidence_check.py:2906` | open | executed: an invented anchor passes in each of four fixtures, refused under a closed fence. Within the price `coordinate_misses` states. Not counted in `Needs a fix` |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `RECORD_COORD_RE` takes its name from `ANCHOR_NAME`, which has no hyphen and no leading digit, so a multi-word or digit-leading heading anchor after a `.md` path is never read and an invented one is never refused. It predates round 2; the heading handling reaches single-word anchors only | a new issue against the records arm of `evidence_check.py`, candidate only | the orchestrator, who decides whether to open it; the owner answers the issue |

Needs a fix: yes — 🟡 9 (a real single-word heading anchor GitHub builds from a setext, quoted or listed heading, or from rendered text that differs from the source, is refused as `NOT-IN-TREE`)
Loses a record or crashes: no

## Proof

Files opened this round, in the clone at `5b115d2e` unless noted:

- `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/rounds/round-2.md`
- `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/rounds/round-2-report.md`
- `git diff ec002d24..0b3d1071` for `skills/`, `tests/` and, word by word, `seal/`; `git diff 0b3d1071..5b115d2e`
- `skills/evidence-check/scripts/evidence_check.py`: `gfm_lines`, `unquoted`, `quoted_lines`, `fence_rule`, `ANCHOR_PATH`, `ANCHOR_NAME`, `RECORD_COORD_RE`, `TOKEN_RE`, `claim_lines`, `stated_coordinates`, `GITHUB_HEADING_RE`, `heading_slugs`, `coordinate_misses`, `reverify`
- `skills/evidence-check/SKILL.md:306-310`, `:475-484`
- `tests/test_a_record_states_what_the_tree_has.py`: `coordinate_refusals`, the two heading cases
- `bin/test`
