"""Two agents alive at once cannot share a scratch name.

Issue #544. Every agent of one session shares one scratchpad, and four work
items ran their review chains in parallel from one session in the 0.15.0 run.
`agents/warden.md` named the clone's shape (`git clone --no-local` at the
target SHA) and no directory; `agents/sealer.md` named no capture file;
`skills/verify/SKILL.md`'s capture example redirected to `/tmp/run.txt`,
which every session on the machine shares. Measured three times in that run:
two wardens cloned to the same `r2clone`, a third's clone had its HEAD moved
by a foreign checkout for fifty-five seconds, and two sealers wrote
`broad-gate.out` over each other.

The class (`agent-contract` §12) is *an instruction that names a scratch
location with a name any parallel agent would also pick*, and the repair is
the same in each of its three instances: the location carries the work item
id, which no two work items share, and the round where there is one. This
file pins the three sentences, because a definition is a sentence an agent
reads and a sentence can be dropped without a case going red.

What it cannot pin is obedience: a spawn prompt that names a different
directory still wins in the moment, and nothing in the tree reads a prompt.
`plan.md` §*Failure scenario* of the work item says so.

Shown red before the sentences were written (§15): against the tree at
`5d51b319`, all three cases failed — no `<work-item-id>` in either
definition's section, and `/tmp/run.txt` standing in the skill.
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

WARDEN = os.path.join(ROOT, "agents", "warden.md")
SEALER = os.path.join(ROOT, "agents", "sealer.md")
VERIFY = os.path.join(ROOT, "skills", "verify", "SKILL.md")

CLONE = "<scratchpad>/<work-item-id>/round-<n>/clone"
ROUND_HOME = "<scratchpad>/<work-item-id>/round-<n>/"


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def section(path, heading):
    """`## <heading>` to the next `## `, as one line so a pinned phrase
    survives re-wrapping."""
    text = read(path)
    start = text.index(f"## {heading}")
    end = text.find("\n## ", start + 1)
    body = text[start : end if end != -1 else len(text)]
    return " ".join(body.split())


def test_the_wardens_clone_is_named_for_the_work_item_and_the_round():
    """A12. The clone directory carries the work item id the prompt names
    and the round, under the scratchpad the harness names — so two wardens
    alive at once, on two work items, cannot pick the same directory. Every
    probe, capture or fixture the round makes outside the clone sits beside
    it, which is also what makes *every one of them is gone* (§7) answerable
    by the agent that made them."""
    where = section(WARDEN, "Where you work")
    assert CLONE in where, (
        "agents/warden.md §Where you work does not name the clone directory "
        f"as `{CLONE}`, so two parallel wardens can clone to one name"
    )
    assert ROUND_HOME in where, (
        "the section does not put the round's probes and captures under "
        f"`{ROUND_HOME}`, so a round's leavings have no one home to remove"
    )
    assert "share" in where and "scratchpad" in where, (
        "the sentence names the directory and not why: agents of one session "
        "share the scratchpad"
    )


def test_the_sealers_capture_file_carries_the_work_item_id():
    """A13. Where the sealer redirects the gate's output to a file to read,
    the file is named for the work item; and the gate's own `outputs kept
    under broad-gate-<random>/` line is quoted in the report, so a capture
    that was overwritten can still be told apart — which is how the 0.15.0
    sealers were not misread."""
    command = section(SEALER, "The command")
    assert "<scratchpad>/<work-item-id>/" in command, (
        "agents/sealer.md §The command names no capture file carrying the "
        "work item id, so two parallel sealers write one file over each other"
    )
    assert "outputs kept under" in command, (
        "the section does not tell the sealer to quote the gate's `outputs "
        "kept under` line, which is the one name per run the gate itself makes"
    )


def test_the_capture_example_is_not_a_name_every_session_shares():
    """A14. `/tmp/run.txt` is the same class one file over, shared across
    every session on the machine rather than across one session's agents.
    The fenced example redirects under the scratchpad with the work item id."""
    text = read(VERIFY)
    assert "/tmp/run.txt" not in text, (
        "skills/verify/SKILL.md still shows a capture file every session on "
        "the machine would also pick"
    )
    start = text.index("**Capture once, filter locally.**")
    example = text[start : text.index("The tell is a second invocation", start)]
    assert "<scratchpad>/<work-item-id>/" in example, (
        "the capture example does not carry the work item id in the file it "
        "redirects to"
    )
