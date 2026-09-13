"""A shipped document that names a script says how to reach it.

Issue #318. `skills/code-review/scripts/round_record.py` was named on
thirty-six lines of nine shipped documents and no document anywhere gave a
path to it or a command that runs it. Four agent segments went looking,
concluded the generator does not ship, and hand-wrote the record it writes --
two of the resulting records had a field wrong in a way only the next round's
reader caught.

The defect has two halves and a wrapper repairs one. Two of those thirty-six
lines show a command for somebody to TYPE; the other thirty-four describe what
the generator does, and a reader who meets one goes LOOKING for a filename.
Three of the four segments were `warden`, whose definition never tells it to
run the script at all, so the typed half is the half those segments never
touched.

What this file pins is the looking half, as a property of the class rather
than of the instance the ticket named -- `skills/agent-contract/SKILL.md` §12,
*do not fix the coordinate, enumerate the class*. The ticket named three
documents; there were nine, and the one the four segments actually hand-wrote
from (`templates/sdd-round.md`, seven mentions) was not among the three.

Two rules, and the second is narrower than the first on purpose:

  every script a shipped document names   has a `bin/` wrapper pair, or is
                                          classified below with its reason

  every shipped document that names a     carries the command or the script's
  WRAPPED script                          repo-relative path, at least once

An unwrapped script is exempt from the second rule because it has no command
to name, and requiring its path in every document that mentions it would touch
six files for a script nobody is told to run. `test_an_unwrapped_script_is_
shown_in_no_command_form` is what keeps that exemption from being a loophole:
the moment a document shows an unwrapped script being invoked, the
classification stops being true and goes red rather than standing as a note.

Scope is what an agent's startup payload can contain: `agents/`, `skills/` and
`templates/`. `docs/` stays out under
`tests/test_the_release_check_watches_what_ships.py`'s own classification --
it does not ship, no agent's payload holds it, and its readers have the whole
clone to `git grep`.

Shown red before it was committed (§15): against the tree as it stood, this
file failed on all nine of `round_record.py`'s documents and on
`chain_check.py` having no classification, and the command-form case was
driven red by planting an invocation in a shipped document.
"""

import glob
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")

# What an agent's startup payload can contain. `docs/` is deliberately absent.
SHIPPED_ROOTS = ("agents", "skills", "templates")

# Scripts that ship without a `bin/` wrapper, and the reason each one keeps
# none. A script named by a shipped document belongs here or in `bin/`; a
# third state is the one `bin/` itself was in before work item 1788302682 --
# a gap somebody notices while writing something up.
NO_WRAPPER = {
    "chain_check.py": (
        "Named in four shipped documents and invoked in none of them -- the "
        "property `test_an_unwrapped_script_is_shown_in_no_command_form` "
        "asserts below. All three places that DO invoke it "
        "(`.github/workflows/hygiene.yml`, `templates/hygiene.yml` and "
        "`docs/release-checklist.md`) carry its full path, so it is reachable "
        "everywhere it is reached. A wrapper would also change the row in "
        "`templates/config.md` that spells the broad gate to a user, which is "
        "a user-facing change with no defect behind it (#318)."
    ),
}


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def scripts():
    """Every script that ships under a skill, repo-relative with `/`."""
    found = glob.glob(os.path.join(ROOT, "skills", "*", "scripts", "*.py"))
    return sorted(os.path.relpath(p, ROOT).replace(os.sep, "/") for p in found)


def shipped_documents():
    """Every `.md` under the roots an agent's payload is drawn from."""
    found = []
    for root in SHIPPED_ROOTS:
        pattern = os.path.join(ROOT, root, "**", "*.md")
        found += glob.glob(pattern, recursive=True)
    return sorted(os.path.relpath(p, ROOT).replace(os.sep, "/") for p in found)


def command_name(script):
    """The bare word a wrapper for `script` answers to.

    Underscores to hyphens, which is what all eleven existing pairs do and
    what `round_record.py`'s own `--help` has printed since it shipped.
    """
    return os.path.basename(script)[:-3].replace("_", "-")


def wrapper_pair(script):
    """The POSIX wrapper and its `.cmd` twin, whether or not they exist."""
    posix = os.path.join(BIN, command_name(script))
    return posix, posix + ".cmd"


def is_wrapped(script):
    return all(os.path.isfile(p) for p in wrapper_pair(script))


def names(text, script):
    """Whether `text` mentions the script by filename at all."""
    return os.path.basename(script) in text


def reachable(text, script):
    """Whether `text` gives a reader a way to GET to `script`.

    Either accepted form counts. The bare command is what the documents
    already use for `evidence-check` and `session-cost`, and is what a session
    with the plugin enabled can type, because the loader puts `bin/` on the
    Bash tool's PATH. The repo-relative path is what a session working inside
    a clone with the plugin disabled can open.
    """
    command = command_name(script)
    typed = re.search(rf"(?<![\w-]){re.escape(command)}(?![\w-])", text) is not None
    return typed or script in text


def command_forms(text, script):
    """Lines of `text` that show `script` being INVOKED rather than described.

    A flag is the tell, and it is the only sound one in prose. A subcommand
    cannot be told from the sentence around it -- *`round_record.py new`
    writes the record* names a subcommand and is a description -- but nothing
    writes `chain_check.py --worktree` except to say what to run.

    Used on the scripts that keep no wrapper: the classification below rests
    on nobody being told to type them, and this is the property, asked of the
    tree rather than assumed.
    """
    pattern = re.compile(rf"{re.escape(os.path.basename(script))}\s+-")
    return [
        (number, line)
        for number, line in enumerate(text.splitlines(), 1)
        if pattern.search(line)
    ]


def named_pairs():
    """(document, script) for every shipped document naming a WRAPPED script.

    The parametrisation both document cases run over. Built once, at
    collection, so a tenth document naming a script is a case that appears
    rather than a rule somebody has to remember.
    """
    texts = {d: read(os.path.join(ROOT, d)) for d in shipped_documents()}
    return [
        (document, script)
        for script in scripts()
        if is_wrapped(script)
        for document, text in texts.items()
        if names(text, script)
    ]


def unwrapped_pairs():
    """(document, script) for every shipped document naming an unwrapped one."""
    texts = {d: read(os.path.join(ROOT, d)) for d in shipped_documents()}
    return [
        (document, script)
        for script in scripts()
        if not is_wrapped(script)
        for document, text in texts.items()
        if names(text, script)
    ]


def label(pair):
    return f"{pair[0]}::{os.path.basename(pair[1])}"


# --- the script half -------------------------------------------------------


@pytest.mark.parametrize("script", scripts())
def test_every_script_a_shipped_document_names_is_wrapped_or_classified(script):
    """A script a document names either has a command or has a recorded
    reason for having none. Neither answer is safe to leave to whoever
    notices, which is the lesson `bin/` itself paid for."""
    texts = [read(os.path.join(ROOT, d)) for d in shipped_documents()]
    if not any(names(t, script) for t in texts):
        pytest.skip("no shipped document names it, so nobody goes looking")
    base = os.path.basename(script)
    if base in NO_WRAPPER:
        assert NO_WRAPPER[base].strip(), (
            f"{base} is classified as keeping no wrapper with an empty reason "
            f"-- say why in NO_WRAPPER in {os.path.basename(__file__)}"
        )
        return
    posix, windows = wrapper_pair(script)
    command = command_name(script)
    assert os.path.isfile(posix), (
        f"a shipped document names {base} and `bin/{command}` does not exist. "
        f"Write the pair -- model it on `bin/survivor-check` -- or classify "
        f"{base} in NO_WRAPPER in {os.path.basename(__file__)} with the reason"
    )
    assert os.path.isfile(windows), (
        f"`bin/{command}` ships without its `.cmd` twin, so Windows loses the "
        "command: a new command means both files or it means one platform"
    )


def test_nothing_classified_has_grown_a_wrapper():
    """A classification is a claim about the tree, so it stops being true the
    moment somebody writes the wrapper. Left standing, it is a note nobody
    re-reads that says the opposite of what `bin/` holds."""
    stale = [b for b in NO_WRAPPER if is_wrapped(f"skills/x/scripts/{b}")]
    assert not stale, (
        f"{sorted(stale)} now have `bin/` wrappers and are still classified as "
        f"keeping none -- drop the rows from NO_WRAPPER in "
        f"{os.path.basename(__file__)}"
    )


def test_nothing_classified_has_stopped_shipping():
    """A row for a script that no longer exists reads as a live decision."""
    present = {os.path.basename(s) for s in scripts()}
    gone = sorted(set(NO_WRAPPER) - present)
    assert not gone, (
        f"{gone} are classified in {os.path.basename(__file__)} and ship from "
        "no skill -- drop the rows with the script"
    )


# --- the document half -----------------------------------------------------


@pytest.mark.parametrize("pair", named_pairs(), ids=label)
def test_a_document_naming_a_wrapped_script_says_how_to_reach_it(pair):
    """The half of #318 a wrapper does not repair: a reader who meets
    *`round_record.py new` writes the record* goes looking for a filename, and
    finds nothing. One mention per document is enough -- a document naming a
    script forty times pays one sentence."""
    document, script = pair
    command, text = command_name(script), read(os.path.join(ROOT, document))
    assert reachable(text, script), (
        f"{document} names {os.path.basename(script)} and never says where it "
        f"is. A reader who goes looking finds nothing, which is #318. Add "
        f"either reachable form, once: the command `{command}`, or the path "
        f"`{script}`"
    )


@pytest.mark.parametrize("pair", unwrapped_pairs(), ids=label)
def test_an_unwrapped_script_is_shown_in_no_command_form(pair):
    """What keeps the exemption above from being a loophole. A script with no
    wrapper is excused the locator rule because nobody is told to type it, and
    this is that premise asked of the tree rather than assumed."""
    document, script = pair
    base = os.path.basename(script)
    shown = command_forms(read(os.path.join(ROOT, document)), script)
    assert not shown, (
        f"{document} shows {base} being invoked, so the classification in "
        f"{os.path.basename(__file__)} -- kept unwrapped because no document "
        "tells anybody to run it -- is no longer true:\n"
        + "\n".join(f"  {document}:{n}: {line.strip()}" for n, line in shown)
        + f"\n\nEither write `bin/{command_name(script)}` and its `.cmd` twin, "
        "or take the invocation out."
    )


# --- the checks can fail ---------------------------------------------------


def test_a_document_with_no_locator_is_caught():
    """`reachable` is the whole of the document rule, so a reader that
    answered yes to any mention would make every case above vacuous."""
    assert not reachable(
        "`round_record.py new` writes the record.", "skills/x/scripts/round_record.py"
    )
    assert reachable(
        "Run `round-record new --item <dir>`.", "skills/x/scripts/round_record.py"
    )
    assert reachable(
        "It lives at `skills/x/scripts/round_record.py`.",
        "skills/x/scripts/round_record.py",
    )


def test_a_locator_inside_a_longer_word_does_not_count():
    """`round-record` inside `round-record-writer` is a different name, and a
    substring test would let one satisfy the rule for the other."""
    script = "skills/x/scripts/round_record.py"
    assert not reachable("the round-record-writer protocol", script)
    assert not reachable("a pre-round-record step", script)


def test_a_planted_invocation_turns_the_classification_red():
    """The classification-defence case, driven from a fixture: a document that
    starts showing an unwrapped script being run has to fail rather than pass
    quietly. Neutral text, no real path."""
    script = "skills/x/scripts/chain_check.py"
    assert command_forms("Run `chain_check.py --worktree` first.\n", script)
    assert command_forms("    chain_check.py -q\n", script)
    assert not command_forms("`chain_check.py` reads the record.\n", script)
    assert not command_forms("what `chain_check.py new` would say\n", script)


def test_a_half_shipped_pair_is_not_a_wrapped_script(monkeypatch):
    """`is_wrapped` asks for BOTH files, and no half-shipped pair exists in the
    tree to ask it with -- so the twin is taken away here instead.

    It matters because the two enumerations below split on this answer. A
    POSIX wrapper whose `.cmd` twin was never written is one platform's
    command, not the repository's; reading it as wrapped would put its
    documents under the locator rule, pointing every reader at a command
    Windows cannot run, and would take the script out of the classification
    rule that would otherwise have caught the missing twin.
    """
    script = "skills/code-review/scripts/round_record.py"
    _, windows = wrapper_pair(script)
    assert is_wrapped(script), "the fixture is stale: this pair should be whole"
    real = os.path.isfile
    monkeypatch.setattr(os.path, "isfile", lambda p: real(p) and p != windows)
    assert not is_wrapped(script), (
        "a POSIX wrapper whose `.cmd` twin is missing reads as wrapped, so its "
        "documents fall under the locator rule while Windows cannot run the "
        "command and the classification rule never sees the script"
    )


def test_every_mention_lands_in_exactly_one_enumeration():
    """The two parametrisations partition the mentions between them.

    Without this, an enumeration that returned nothing would be a GREEN suite:
    an empty parametrisation runs no case and reports success. That is how the
    classification defence would go silent -- `unwrapped_pairs` answering with
    an empty list means `chain_check.py` is invoked nowhere, checked nowhere.
    """
    texts = {d: read(os.path.join(ROOT, d)) for d in shipped_documents()}
    every = {(d, s) for s in scripts() for d, t in texts.items() if names(t, s)}
    wrapped, unwrapped = set(named_pairs()), set(unwrapped_pairs())
    assert wrapped | unwrapped == every, (
        "a document naming a script reaches neither enumeration, so no case "
        f"runs over it: {sorted(every - wrapped - unwrapped)}"
    )
    assert not wrapped & unwrapped, (
        f"a script is enumerated as both wrapped and not: {sorted(wrapped & unwrapped)}"
    )
    if NO_WRAPPER:
        assert unwrapped, (
            "a script is classified as keeping no wrapper and no document "
            "reaches the case defending that classification"
        )


def test_the_enumeration_is_not_empty():
    """Every case above is parametrised off the tree. An enumeration that
    silently returned nothing would be a green suite that checks nothing --
    the shape a `glob` typo produces, and it exits zero."""
    assert len(scripts()) >= 10, scripts()
    assert len(shipped_documents()) >= 20, len(shipped_documents())
    assert named_pairs(), "no shipped document names a wrapped script"
