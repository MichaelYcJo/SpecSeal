"""No passage of a rule document is pasted into a second one (#730).

`docs/the-record-layout.md` says that a file stating a rule another file is
the home of links to that home and does not restate it, and that where a copy
is found the copy is the defect. Nothing found copies. Four were measured
before this module existed, each arriving as a paste: #107's contract section
pasted back into `agents/warden.md`, #292's `CLAUDE.md` block that was 95 %
its template, #715's `CLAUDE.md` and `CONTRIBUTING.md` sentences that
disagreed, and #730's merge table in `CLAUDE.md`, which had gone false where
its home had not.

**What is read.** Every tracked `*.md` under `docs/`, `skills/`, `agents/` and
`templates/`, with `CLAUDE.md`, `CONTRIBUTING.md` and `README.md`. Left out:
every `*.ko.md`, because a Korean edition is a sanctioned mirror in other
words; everything under `seal/`, which is records; and `CHANGELOG.md`.

**How a file is normalised.** `CLAUDE.md`'s generated region is dropped,
because `tests/test_the_claude_md_block_has_one_source.py` holds it equal to
`templates/claude-md-block.md` on purpose. Fenced code blocks and heading
lines are dropped. A quoted section name -- `§*...*`, or a `.md` path followed
by `*...*` -- becomes one token, because a link shares its heading's words by
design; the name may wrap across a line, which is the case the first draft
of this method missed. Then the text is lowercased, stripped of `` ` ``, `*`,
`|`, `>` and `#`, and split into words.

**What is counted.** For each unordered pair of files, the number of distinct
runs of `WINDOW` consecutive words the two share. `WINDOW` is imported from
`tests/test_a_moved_rule_leaves_its_definition.py`, never typed here: that
module measured it between the longest kept application (10 words) and the
smallest real copy (25), and this is the same question asked of more files.

**Why verbatim.** The measured failure is a paste. A check that tried to
catch a paraphrase would have to decide when two sentences say the same
thing, which no constant can hold: at any similarity that catches a
paraphrase it also matches a heading against the sentence that links it.
The paraphrase half was measured once, by hand, and its result is recorded in
`seal/specs/1791076836-every-rule-claude-md-restates-has-one-home/spec.md`
§*The method and its result* rather than checked.

**Why a ratchet.** The tree already holds copies, measured into `BASELINE`
below, and moving them is #755's work, cluster by cluster. So the check fails
when a pair not in `BASELINE` shares any run, or when a pair's count goes
above its baseline. It passes when a count goes down, and the baseline need
not be lowered in the same change: otherwise every branch that edits a
duplicated passage would edit this one table, which is the shared-file
conflict `docs/the-record-layout.md` §*A change writes fragments, never a
shared file* exists to stop. The cost is slack, stated: a pair that has
drained can take a later copy up to its old count. The work that drains a
pair lowers its entry on purpose.

**What it does not catch.** A rule restated in fresh words. Measured against
the three restatements #730 names, it finds one of three, the merge table,
through its identical rows; *no real identifiers* and the commit cadence were
both restated in other words. Saying otherwise would be the counterfeit
`CONTRIBUTING.md` refuses.
"""

import itertools
import os
import re

from conftest import git_listing, on_disk
from test_a_moved_rule_leaves_its_definition import WINDOW

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TOP_FILES = ("CLAUDE.md", "CONTRIBUTING.md", "README.md")
TOP_DIRS = ("docs/", "skills/", "agents/", "templates/")

HOME_ACT = "link to the home instead of copying it, per `docs/the-record-layout.md`"

GENERATED = re.compile(r"<!-- specseal:start -->.*?<!-- specseal:end -->", re.S)
FENCE = re.compile(r"^ *(`{3,}|~{3,})")
HEADING = re.compile(r"^ {0,3}#{1,6}(\s|$)")
# A section quoted by name, after `§` or after a `.md` path (with or without
# its possessive). `[^*]` crosses a line break, so a wrapped name is one name.
SECTION = re.compile(r"§\*[^*]{1,200}\*|`?[\w./-]+\.md`?(?:'s)?\s+\*[^*]{1,200}\*")
SECTION_TOKEN = " §section "
STRIP = str.maketrans("", "", "`*|>#")


def corpus():
    """The rule documents git tracks, as repository paths, sorted.

    A path git lists and the tree has deleted is skipped: this check judges
    what it finds, and a missing file can only lower a count, which never
    fails it."""
    listed = git_listing(ROOT, "ls-files", "--", "*.md")
    rules = [
        rel
        for rel in listed
        if (rel in TOP_FILES or rel.startswith(TOP_DIRS)) and not rel.endswith(".ko.md")
    ]
    present, _missing = on_disk(ROOT, rules)
    return sorted(present)


def lines(text):
    """TEXT's lines, ended where GFM ends one: LF, CR or CRLF alone."""
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def words(text):
    """TEXT normalised as the docstring says, as a list of words."""
    text = GENERATED.sub("\n", text)
    kept, fence = [], None
    for line in lines(text):
        opened = FENCE.match(line)
        if fence:
            if (
                opened
                and opened.group(1)[0] == fence[0]
                and len(opened.group(1)) >= len(fence)
                and not line.strip().strip(fence[0])
            ):
                fence = None
            continue
        if opened:
            fence = opened.group(1)
            continue
        if HEADING.match(line):
            continue
        kept.append(line)
    text = SECTION.sub(SECTION_TOKEN, "\n".join(kept))
    return text.lower().translate(STRIP).split()


def windows(word_list):
    return {
        " ".join(word_list[i : i + WINDOW]) for i in range(len(word_list) - WINDOW + 1)
    }


def shared_counts(texts):
    """`{(a, b): n}`, the distinct `WINDOW`-word runs each pair shares.

    TEXTS maps a path to its raw text, so a case can hand in a planted copy."""
    owners = {}
    for rel in sorted(texts):
        for run in windows(words(texts[rel])):
            owners.setdefault(run, []).append(rel)
    counts = {}
    for rels in owners.values():
        for pair in itertools.combinations(rels, 2):
            counts[pair] = counts.get(pair, 0) + 1
    return counts


def longest_run(a_text, b_text):
    """The longest run of words A's normalised text shares with B's."""
    a, b = words(a_text), words(b_text)
    common = windows(a) & windows(b)
    best, start = (0, ""), None
    for i in range(len(a) - WINDOW + 2):
        inside = i < len(a) - WINDOW + 1 and " ".join(a[i : i + WINDOW]) in common
        if inside and start is None:
            start = i
        if not inside and start is not None:
            span = a[start : i - 1 + WINDOW]
            best = max(best, (len(span), " ".join(span)))
            start = None
    return best


def over_baseline(texts, baseline):
    """A sentence per pair whose count exceeds its baseline, or that has none."""
    found = []
    for pair, count in sorted(shared_counts(texts).items()):
        allowed = baseline.get(pair, 0)
        if count > allowed:
            length, run = longest_run(texts[pair[0]], texts[pair[1]])
            found.append(
                f"{pair[0]} and {pair[1]} share {count} runs of {WINDOW} words "
                f"where {allowed} were measured; the longest is {length} words: "
                f"{run[:240]!r}. {HOME_ACT[0].upper()}{HOME_ACT[1:]}"
            )
    return found


def tree():
    texts = {}
    for rel in corpus():
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            texts[rel] = f.read()
    return texts


# Measured on 2026-10-04 at this work item's phase 1 tree. Every entry is debt
# that #755 moves, cluster by cluster, except where a comment names the rule
# that makes the copy sanctioned. A change that drains a pair may lower its
# entry; nothing has to.
BASELINE = {
    # Sanctioned: the opening paragraph every agent definition carries,
    # which tests/test_every_agent_reads_the_contract.py requires word for
    # word. framer-smith adds the shared `skills:` list, and smith-warden
    # adds debt of its own (cluster b of the remainder issue).
    ("agents/framer.md", "agents/scribe.md"): 65,
    ("agents/framer.md", "agents/sealer.md"): 65,
    ("agents/framer.md", "agents/smith.md"): 72,
    ("agents/framer.md", "agents/warden.md"): 67,
    ("agents/scribe.md", "agents/sealer.md"): 65,
    ("agents/scribe.md", "agents/smith.md"): 65,
    ("agents/scribe.md", "agents/warden.md"): 65,
    ("agents/sealer.md", "agents/smith.md"): 65,
    ("agents/sealer.md", "agents/warden.md"): 65,
    ("agents/smith.md", "agents/warden.md"): 153,
    # Debt, every entry below.
    ("CLAUDE.md", "CONTRIBUTING.md"): 14,
    ("README.md", "agents/smith.md"): 4,
    ("README.md", "docs/commit-review-gate-spec.md"): 5,
    ("README.md", "docs/the-evidence-ledger.md"): 19,
    ("README.md", "skills/code-review/orchestration.md"): 10,
    ("README.md", "skills/config/SKILL.md"): 22,
    ("README.md", "skills/evidence-check/SKILL.md"): 7,
    ("README.md", "skills/implement/SKILL.md"): 2,
    ("README.md", "skills/implement/orchestration.md"): 1,
    ("README.md", "skills/parity-setup/SKILL.md"): 1,
    ("README.md", "skills/update/SKILL.md"): 9,
    ("README.md", "templates/ledger.md"): 25,
    ("README.md", "templates/seal-README.md"): 1,
    ("agents/framer.md", "skills/implement/orchestration.md"): 7,
    ("agents/framer.md", "templates/sdd-questions.md"): 4,
    ("agents/framer.md", "templates/sdd-spec.md"): 8,
    ("agents/sealer.md", "skills/code-review/orchestration.md"): 3,
    ("agents/sealer.md", "skills/verify/SKILL.md"): 1,
    ("agents/smith.md", "docs/review-chain-spec.md"): 3,
    ("agents/smith.md", "skills/code-review/orchestration.md"): 14,
    ("agents/smith.md", "skills/implement/SKILL.md"): 46,
    ("agents/smith.md", "skills/implement/orchestration.md"): 1,
    ("agents/warden.md", "docs/review-chain-spec.md"): 5,
    ("agents/warden.md", "docs/review-handoff-protocol.md"): 9,
    ("agents/warden.md", "docs/round-record-spec.md"): 36,
    ("agents/warden.md", "skills/code-review/SKILL.md"): 53,
    ("docs/branch-and-release.md", "docs/one-root-by-lifetime.md"): 5,
    ("docs/commit-review-gate-spec.md", "docs/the-commit-gate-inside-git.md"): 11,
    ("docs/commit-review-gate-spec.md", "docs/the-review-and-parity-arms.md"): 11,
    ("docs/commit-review-gate-spec.md", "docs/worktree-guard-spec.md"): 1,
    ("docs/commit-review-gate-spec.md", "skills/agent-contract/SKILL.md"): 14,
    ("docs/issues-and-milestones.md", "docs/release-checklist.md"): 2,
    ("docs/measuring-a-run.md", "docs/the-agent-set.md"): 11,
    ("docs/measuring-a-run.md", "docs/the-broad-gate.md"): 11,
    ("docs/measuring-a-run.md", "docs/the-evidence-ledger.md"): 11,
    ("docs/measuring-a-run.md", "docs/the-pact.md"): 12,
    ("docs/measuring-a-run.md", "skills/verify/SKILL.md"): 1,
    ("docs/one-root-by-lifetime.md", "skills/implement/SKILL.md"): 4,
    ("docs/one-root-by-lifetime.md", "skills/verify/SKILL.md"): 3,
    ("docs/review-chain-spec.md", "docs/round-record-spec.md"): 31,
    ("docs/review-chain-spec.md", "skills/code-review/SKILL.md"): 4,
    ("docs/review-chain-spec.md", "skills/code-review/orchestration.md"): 109,
    ("docs/review-chain-spec.md", "templates/sdd-round.md"): 51,
    ("docs/review-handoff-protocol.md", "docs/round-record-spec.md"): 44,
    ("docs/review-handoff-protocol.md", "skills/agent-contract/SKILL.md"): 1,
    ("docs/review-handoff-protocol.md", "skills/code-review/orchestration.md"): 39,
    ("docs/review-handoff-protocol.md", "skills/evidence-check/SKILL.md"): 10,
    ("docs/review-handoff-protocol.md", "skills/verify/SKILL.md"): 8,
    ("docs/review-handoff-protocol.md", "templates/sdd-phase.md"): 5,
    ("docs/review-handoff-protocol.md", "templates/sdd-round.md"): 27,
    ("docs/round-record-spec.md", "skills/code-review/SKILL.md"): 64,
    ("docs/round-record-spec.md", "skills/code-review/orchestration.md"): 33,
    ("docs/round-record-spec.md", "skills/verify/SKILL.md"): 5,
    ("docs/round-record-spec.md", "templates/sdd-phase.md"): 6,
    ("docs/round-record-spec.md", "templates/sdd-round.md"): 10,
    ("docs/the-agent-set.md", "docs/the-broad-gate.md"): 15,
    ("docs/the-agent-set.md", "docs/the-evidence-ledger.md"): 12,
    ("docs/the-agent-set.md", "docs/the-pact.md"): 12,
    ("docs/the-agent-set.md", "skills/implement/SKILL.md"): 20,
    ("docs/the-broad-gate.md", "docs/the-evidence-ledger.md"): 12,
    ("docs/the-broad-gate.md", "docs/the-pact.md"): 12,
    ("docs/the-commit-gate-inside-git.md", "docs/the-review-and-parity-arms.md"): 11,
    ("docs/the-evidence-ledger.md", "docs/the-pact.md"): 12,
    ("docs/the-evidence-ledger.md", "skills/evidence-check/SKILL.md"): 10,
    ("docs/the-evidence-ledger.md", "skills/settle/SKILL.md"): 14,
    ("docs/the-evidence-ledger.md", "templates/ledger.md"): 14,
    ("docs/the-pact.md", "skills/evidence-check/SKILL.md"): 4,
    ("skills/agent-contract/SKILL.md", "skills/implement/SKILL.md"): 17,
    ("skills/code-review/SKILL.md", "skills/code-review/orchestration.md"): 5,
    ("skills/code-review/SKILL.md", "skills/implement/SKILL.md"): 9,
    ("skills/code-review/SKILL.md", "templates/sdd-round.md"): 30,
    ("skills/code-review/orchestration.md", "skills/evidence-check/SKILL.md"): 6,
    ("skills/code-review/orchestration.md", "skills/implement/SKILL.md"): 22,
    ("skills/code-review/orchestration.md", "skills/implement/orchestration.md"): 7,
    ("skills/code-review/orchestration.md", "skills/verify/SKILL.md"): 5,
    ("skills/code-review/orchestration.md", "templates/sdd-phase.md"): 20,
    ("skills/code-review/orchestration.md", "templates/sdd-round.md"): 83,
    ("skills/commit-pr-convention/SKILL.md", "templates/config.md"): 9,
    ("skills/confidence-check/SKILL.md", "skills/feature-planner/SKILL.md"): 6,
    ("skills/config/SKILL.md", "skills/implement/SKILL.md"): 1,
    ("skills/config/SKILL.md", "skills/implement/orchestration.md"): 5,
    ("skills/config/SKILL.md", "templates/config.md"): 2,
    ("skills/evidence-check/SKILL.md", "templates/ledger.md"): 38,
    ("skills/evidence-check/SKILL.md", "templates/pact.md"): 7,
    ("skills/implement/SKILL.md", "skills/implement/orchestration.md"): 1,
    ("skills/implement/SKILL.md", "skills/legacy-parity/SKILL.md"): 1,
    ("skills/implement/SKILL.md", "templates/sdd-overview.md"): 4,
    ("skills/implement/orchestration.md", "templates/sdd-round.md"): 5,
    ("skills/implement/orchestration.md", "templates/sdd-routing.md"): 10,
    ("skills/verify/SKILL.md", "templates/sdd-phase.md"): 10,
    ("skills/writing-style/SKILL.md", "skills/writing-style/outside-the-review.md"): 3,
    ("templates/sdd-phase.md", "templates/sdd-round.md"): 9,
}


def test_the_corpus_is_found():
    """A glob that matches nothing passes every pair it would have judged."""
    found = corpus()
    assert len(found) >= 50, f"the rule corpus has {len(found)} files"
    for rel in TOP_FILES:
        assert rel in found, f"{rel} is missing from the corpus"
    assert not [rel for rel in found if rel.endswith(".ko.md")]


def test_no_pair_shares_more_than_it_was_measured_at():
    found = over_baseline(tree(), BASELINE)
    assert not found, "\n".join(found)


# --- the check can fail, and it does not fail the wrong way ------------------


def a_sentence_of(text, length=20):
    """LENGTH consecutive words from TEXT's prose, normalised, as raw text."""
    return " ".join(words(text)[200 : 200 + length])


def test_a_paste_is_named_with_the_pair_the_run_and_the_act():
    """S6: twenty words of `CONTRIBUTING.md` pasted into another rule document
    are named, with both files, the count, the run and the act.

    The paste lands in a document of its own, so the pair is new and the
    longest run it reports is the paste and not a copy the tree already
    held."""
    texts = tree()
    paste = a_sentence_of(texts["CONTRIBUTING.md"])
    texts["docs/planted.md"] = "Some words of its own.\n\n" + paste + "\n"
    found = over_baseline(texts, BASELINE)
    named = [f for f in found if "CONTRIBUTING.md and docs/planted.md" in f]
    assert named, found
    assert f"share {20 - WINDOW + 1} runs" in named[0], named[0]
    assert "longest is 20 words" in named[0], named[0]
    assert paste in named[0]
    assert "link to the home instead of copying it" in named[0].lower()


def test_a_count_over_its_baseline_is_named_and_one_at_it_is_not():
    """The ratchet's own edge, on a pair the table already holds."""
    texts = tree()
    counts = shared_counts(texts)
    pair = max(counts, key=counts.get)
    assert not [
        f
        for f in over_baseline(texts, {**BASELINE, pair: counts[pair]})
        if f.startswith(f"{pair[0]} and {pair[1]} share")
    ]
    found = over_baseline(texts, {**BASELINE, pair: counts[pair] - 1})
    assert [f for f in found if f.startswith(f"{pair[0]} and {pair[1]} share")]


def test_a_removed_copy_passes_without_a_baseline_edit():
    """S7: a pair whose count goes down passes, whatever the table says.

    One shared run is broken in the second file, so the pair still shares
    something and is still judged; a check that held counts exactly, rather
    than at most, fails here."""
    texts = tree()
    counts = shared_counts(texts)
    a, b = max(counts, key=counts.get)
    mine = words(texts[b])
    common = windows(words(texts[a])) & windows(mine)
    first = next(
        i
        for i in range(len(mine) - WINDOW + 1)
        if " ".join(mine[i : i + WINDOW]) in common
    )
    del mine[first + WINDOW // 2]
    texts[b] = " ".join(mine)
    after = shared_counts(texts)
    assert 0 < after[(a, b)] < counts[(a, b)]
    assert not over_baseline(texts, {**BASELINE, (a, b): counts[(a, b)]})


def test_a_wrapped_section_name_is_one_token():
    """A link carries its heading's words; a name broken across a line is
    still the name, and two links to one long heading share nothing."""
    name = (
        "A change writes fragments, never a shared file, and the release "
        "gathers every one of them before it folds"
    )
    assert len(name.split()) > WINDOW
    one = f"See `docs/the-record-layout.md` §*{name}* for where it goes.\n"
    two = f"Read §*{name.replace(' a shared', chr(10) + 'a shared')}*\nfirst.\n"
    path = f"`CONTRIBUTING.md`'s *{name}*\n"
    other = f"As docs/the-record-layout.md *{name}* says.\n"
    assert not shared_counts(
        {"one.md": one, "two.md": two, "three.md": path, "four.md": other}
    )


def test_the_generated_block_fences_and_headings_are_not_read():
    run = " ".join(f"w{i}" for i in range(WINDOW))
    fenced = f"```\n{run}\n```\n"
    block = f"<!-- specseal:start -->\n{run}\n<!-- specseal:end -->\n"
    heading = f"## {run}\n"
    for skipped in (fenced, block, heading):
        assert not shared_counts({"a.md": skipped, "b.md": run}), skipped
    assert shared_counts({"a.md": run, "b.md": run}) == {("a.md", "b.md"): 1}
    # A copy whose first word was capitalised by its new sentence is a copy.
    assert shared_counts({"a.md": run.upper(), "b.md": f"`{run}`"}) == {
        ("a.md", "b.md"): 1
    }
