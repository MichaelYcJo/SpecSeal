#!/usr/bin/env python3
"""Stop hook: draw the sealer's stamp in the session that spawned the sealer.

Issue #400, work item 1790562543. A sealer's stdout is a pipe into a report
that reaches the person folded behind `ctrl+o`, so a stamp drawn there was
never seen. The broad gate therefore draws nothing on a pipe: a recorded seal
writes its panel's rows to a values file under
`<git-common-dir>/specseal-stamp/<session>/`, keyed by
`CLAUDE_CODE_SESSION_ID`, which every Bash call of a session and of its
subagents carries as the MAIN session's id.

This hook draws each undrawn file of its own session once, as a JSON
`systemMessage` from `Stop`. That surface was measured on the owner's screen
(probe D, 2026-09-28): unfolded, in truecolour, after the turn's final text.
The harness shows the message's first line as a dim `Stop says: <line>`, so
line 1 is a label naming what was sealed and the drawing starts on line 2.

**Only the main session's `Stop`.** `SubagentStop` carries the same
`session_id` — the parent's — and differs by `agent_id` alone (`questions.md`
Q2, measured 2026-09-28), so a payload carrying `agent_id` is a subagent's
end and draws nothing: the sealer's own end must not take its own stamp. So
does any event that is not `Stop`.

**Which repository.** The payload's `cwd`, which is the main checkout while
the sealer ran in a linked worktree of the same clone; the git COMMON dir is
the one place both resolve alike. It is found by walking up from `cwd` to the
`.git` entry, and where that entry is a directory the common dir IS it, with
no process started. The hook fires at the end of every turn, so a session
directory that does not exist returns before any `git` call in a main
checkout; a `cwd` in a linked worktree costs one `rev-parse` first.

**One message, held under a budget** (#717). The harness writes a
`systemMessage` longer than `seal_stamp.MESSAGE_LIMIT` characters to a file
and shows a preview of it, which is how every stamp from #666 to #717 reached
the owner. So the message printed is `seal_stamp.fitted`'s: as many of the
oldest pending blocks as fit `MESSAGE_BUDGET` together with their disc. The
rest stay pending for the next `Stop`, and only one block that does not fit
with its disc alone is drawn without it. A stamp may therefore be drawn
without its disc, or at a later `Stop`, but never smaller: the disc has one
size. No file is claimed without its stamp being printed. A `scale` a file
written before #853 carries is read as nothing.

**Claim before print.** Each file is rendered, then renamed to `.drawn.json`
(`seal_stamp.claim`), and only a file this process renamed is printed. Two
hooks racing for one file draw it once, and a crash between the two loses a
drawing rather than repeating one.

**Silent on every failure**, the shape `implementer-notice.py` has: a payload
that is not JSON, a repository that is not opted in, a file that is not a
run's values. That includes an interpreter under `seal_stamp.py`'s floor of
3.12 — a hook runs under whatever `python3` the harness finds, 3.9 on a stock
macOS — where this draws nothing and the `SEALED` line in the sealer's
report, which names the file and `seal-stamp --from` wherever a values file
was written, is what remains. The same line is what remains where the main
session's working directory is outside the sealed clone, and where its
plugin predates this hook; `docs/the-broad-gate.md` §*Where the stamp is
drawn* states all three.

It draws; it never stops anything. `hooks/implementer.py`'s stance holds: a
values file somebody wrote by hand would be drawn, because this catches a
session forgetting and does not stop an adversary.
"""

import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin

HOOKS = os.path.dirname(os.path.abspath(__file__))
STAMP = os.path.join(
    os.path.dirname(HOOKS), "skills", "verify", "scripts", "seal_stamp.py"
)
EVENT = "Stop"


def toplevel(cwd):
    """The nearest directory at or above `cwd` holding a `.git` entry, or
    "" — asked of the filesystem, so the common case starts no process."""
    here = os.path.abspath(cwd or ".")
    while True:
        if os.path.exists(os.path.join(here, ".git")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return ""
        here = parent


def load_stamp():
    """`seal_stamp.py`, or None where it cannot be imported — its own floor
    refuses an interpreter under 3.12 with `SystemExit` at import."""
    try:
        spec = importlib.util.spec_from_file_location(
            "specseal_seal_stamp_for_the_stop_hook", STAMP
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (Exception, SystemExit):
        return None
    return module


def drawings(stamp, directory):
    """The message block for every undrawn file in `directory`, oldest
    first. Each block is built whole, label included, before its file is
    claimed, so a file that is not a run's values — whatever it fails on — is
    left where it is and takes no other file's drawing with it.

    It used to catch `ValueError` alone and build the label after the claim,
    and `label` raises `TypeError` on an `item` that is not a string. So one
    bad file after a good one left both renamed and nothing printed (round
    1's 🟡 2). The file is written by the gate the TREE ships and read by the
    hook the INSTALLED plugin ships, so a format one side does not know is an
    ordinary state, not only a hand-written file.

    A block is `(label, rows)`, which `seal_stamp.fitted` draws (#717). It
    is still drawn whole here, with its disc, before the claim: that is what
    proves the file draws at all. The one rung `fitted` may step down to
    draws the same rows with no disc, so a block drawn here cannot fail
    there.

    Every file is drawn before any is claimed, and only the oldest files
    one message carries are claimed (`seal_stamp.admitted`, the owner's rule
    of 2026-10-02): the rest stay pending under their own names, and the
    next `Stop` draws them whole. A session that ends first leaves them for
    `seal-stamp --from`."""
    ready = []
    for path in stamp.pending(directory):
        try:
            values = stamp.read_values(path)
            block = (stamp.label(values), values["rows"])
            stamp.stamp(values["rows"], shape=False)
        except Exception:
            continue
        ready.append((path, block))
    carried = len(stamp.admitted([block for _, block in ready]))
    blocks = []
    for path, block in ready[:carried]:
        if stamp.claim(path) is None:
            continue
        blocks.append(block)
    return blocks


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    if payload.get("hook_event_name") != EVENT or payload.get("agent_id"):
        return
    session = payload.get("session_id")
    if not session:
        return
    top = toplevel(payload.get("cwd"))
    common = optin.git_common_dir(top) if top else ""
    if not common:
        return
    stamp = load_stamp()
    if stamp is None:
        return
    directory = stamp.values_dir(common, session)
    if not stamp.pending(directory) or not optin.opted_in(top):
        return
    blocks = drawings(stamp, directory)
    if blocks:
        print(json.dumps({"systemMessage": stamp.fitted(blocks)}))


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
