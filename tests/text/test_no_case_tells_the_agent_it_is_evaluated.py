"""No behaviour case tells the agent under test that the run is an evaluation.

The agent is shown a case's `prompt.md` and works in the repository its
`scaffold.sh` builds, so neither file holds a word that names the run as a
measurement (#1042). The words are refused at the start of a word, in any
case, as the stems `STEMS` lists: `evaluated`, `graders`, `judged` and
`scenarios` are refused with their stems. `evals/README.md` *The behaviour
suite* states the rule.

Two kinds of text are exempt, each for its reason below, and nothing else
is: the record shapes this plugin's own templates write, and the values a
replay or seeded generator copies from this repository's history into a
case. A copied value is exempt only where the file is the generator's own
text with that value in its place, so a word in the generator's text is
refused like any other.
"""

import os
import re

from conftest import ROOT, load_module

SUITE = os.path.join(ROOT, "evals", "behaviour")
SCRIPTS = os.path.join(ROOT, "evals", "scripts")
FILES = ("prompt.md", "scaffold.sh")

STEMS = ("eval", "grader", "judg", "fixture", "scenario")
REFUSED = re.compile(r"(?<![a-z])(?:" + "|".join(STEMS) + r")[a-z]*", re.I)

# The record shapes a scaffold copies from this plugin's templates, as whole
# lines. The first two are `templates/records/sdd-design.md`'s scenario
# heading, without the ` *(mandatory)*` the template carries, and its table
# header; the third is `templates/records/sdd-round.md`'s heading. A record
# written in the plugin's shape is what the agent meets in production too.
RECORD_LINES = (
    "## User scenarios & acceptance",
    "| Scenario | Given / When / Then | Verifiable how |",
    "## Not judged",
)

# Each value a replay or seeded generator copies from this repository into
# a case, and what the value may be. A copied value is exempt.
COPIED = {
    "item": r".+?",
    # The path of the round record the case was cut from, in its layout.
    "report": r".+?",
    "branch": r".+?",
    "base_ref": r".+?",
    "base": r"[0-9a-f]+",
    "asked": r".+?",
    "subject": r".+?",
    "path": r".+?",
    "old": r".+?",
    "new": r".+?",
}
# Copied too, and read like the generator's own text: a commit, a number
# and the remote's URL.
READ = {"target": r"[0-9a-f]+", "n": r"\d+", "line": r"\d+", "url": r"\S+"}
SLOT = re.compile(r"(QQ[a-z_]+QQ)")
# The hit a replay or seeded case file takes, at line 0, where its generator
# no longer writes it. A word reported below it may be a copied value, so
# the case is written again before anything is reworded.
STALE = "not its generator's text: write the case again with `--case NAME`"


def token(name):
    """The token a generator is rendered with in the place of the value
    NAME. The base's token is eight characters, so the seeded prompt's
    `base[:8]` renders it whole."""
    return f"QQ{name}QQ"


def generators():
    """`{case prefix: generator module}` for the generators that copy
    values into their cases."""
    return {
        "replay-": load_module(
            os.path.join(SCRIPTS, "replay_targets.py"), "replay_targets_for_words"
        ),
        "seeded-": load_module(
            os.path.join(SCRIPTS, "seed_defects.py"), "seed_defects_for_words"
        ),
    }


def rendered(generator, file_name):
    """Every text GENERATOR writes as FILE_NAME, with a token in the place of
    each value: one per way the base ref and the asked paragraph can be
    present."""
    texts = []
    for base_ref in (None, token("base_ref")):
        for asked in ("", token("asked")):
            values = {name: token(name) for name in (*COPIED, *READ)}
            values.update(base_ref=base_ref, asked=asked)
            if file_name == "prompt.md":
                texts.append(generator.prompt(values))
            else:
                texts.append(generator.scaffold(values, token("url")))
    return texts


def pattern_of(text):
    """A regex matching TEXT with each token standing for its value, and the
    names of its groups in order."""
    parts, names = [], []
    for part in SLOT.split(text):
        name = part[2:-2] if SLOT.fullmatch(part) else None
        if name in COPIED or name in READ:
            names.append(name)
            parts.append(f"({COPIED.get(name) or READ[name]})")
        else:
            parts.append(re.escape(part))
    return re.compile("".join(parts)), names


def copied_spans(text, generator, file_name):
    """The spans of TEXT that hold a value GENERATOR copied, where TEXT holds
    one of the texts it writes as FILE_NAME; None where it holds none."""
    for shape in rendered(generator, file_name):
        pattern, names = pattern_of(shape.strip())
        m = pattern.search(text)
        if m:
            return [m.span(i) for i, name in enumerate(names, 1) if name in COPIED]
    return None


def hits(suite, by_prefix=None):
    """`[(path relative to SUITE, line, word)]` for every refused word in a
    case file under SUITE, outside the exemptions. BY_PREFIX maps a case
    name's prefix to the generator that copies values into it.

    A replay or seeded case file its generator no longer writes takes the
    hit `STALE` at line 0, ahead of its words, and keeps no exemption."""
    by_prefix = generators() if by_prefix is None else by_prefix
    found = []
    for path in case_files(suite):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        case = os.path.basename(os.path.dirname(path))
        masked = list(text)
        for prefix, generator in by_prefix.items():
            if case.startswith(prefix):
                spans = copied_spans(text, generator, os.path.basename(path))
                if spans is None:
                    found.append((os.path.relpath(path, suite), 0, STALE))
                    spans = []
                for start, end in spans:
                    masked[start:end] = " " * (end - start)
        lines = text.split("\n")
        for n, line in enumerate("".join(masked).split("\n"), 1):
            if lines[n - 1] in RECORD_LINES:
                continue
            for m in REFUSED.finditer(line):
                found.append((os.path.relpath(path, suite), n, m.group()))
    return found


def case_files(suite):
    """Every `prompt.md` and `scaffold.sh` of a case under SUITE, sorted."""
    return sorted(
        os.path.join(directory, name)
        for directory, _dirs, names in os.walk(suite)
        for name in names
        if name in FILES
    )


def test_no_case_file_holds_a_refused_word():
    """Guards S4: no `prompt.md` and no `scaffold.sh` under
    `evals/behaviour/` holds a refused word outside the exemptions; each hit
    is named by its file, line and word."""
    assert case_files(SUITE), "no case file was read under evals/behaviour/"
    found = hits(SUITE)
    assert found == [], "\n".join(f"{p}:{n}: {word}" for p, n, word in found)


def test_a_word_in_the_generators_text_is_refused_and_one_it_copied_is_not(
    tmp_path,
):
    """Guards S5: a replay prompt holding `judge` in the paragraph its
    generator copies passes, and the same prompt written by a scratch copy of
    the generator whose own text holds `judged` is refused at that line
    alone. Read against the real generator, whose text that prompt is not,
    the prompt is reported as no longer its generator's text first, and it
    keeps no exemption, so both words are refused below that report."""
    real = generators()["replay-"]
    source_path = os.path.join(SCRIPTS, "replay_targets.py")
    with open(source_path, encoding="utf-8") as f:
        source = f.read()
    own = "Review, edit and commit nothing yourself."
    assert own in source
    scratch_path = tmp_path / "replay_targets_planted.py"
    scratch_path.write_text(
        source.replace(own, own[:-1] + ", as the round is judged."), encoding="utf-8"
    )
    planted = load_module(str(scratch_path), "replay_targets_planted")
    target = {
        "item": "1-a-work-item",
        "n": 2,
        "report": "seal/threads/1-a-work-item/trail/rounds/round-2.md",
        "branch": "feat/a-branch",
        "target": "a" * 40,
        "base": "b" * 40,
        "base_ref": None,
        "asked": "It was asked to judge the fix range.",
    }
    for name, writer, reader, want in (
        ("copied", real, real, []),
        ("planted", planted, planted, [(1, "judged")]),
        (
            "not-the-generators-text",
            planted,
            real,
            [(0, STALE), (1, "judged"), (5, "judge")],
        ),
    ):
        suite = tmp_path / name
        case = suite / "proofer" / "replay-1-r2"
        case.mkdir(parents=True)
        (case / "prompt.md").write_text(writer.prompt(target) + "\n", encoding="utf-8")
        found = hits(str(suite), {"replay-": reader})
        assert [(n, word) for _p, n, word in found] == want, (name, found)
