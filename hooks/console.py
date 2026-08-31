"""Where the streams get fixed, and why it is at every entry point.

A hook that raises while reading or printing dies with **stdout empty**, and
empty stdout is exactly how a hook says "nothing to see here". So the failure
mode of every gate in this repository, under a console it cannot encode to, is
a silent pass — the exact condition the gates exist to end. The same shape
costs the `bin/`-wrapped checks their output, and `chain_check.py` its verdict
in CI.

Korean, Japanese and Chinese Windows default to cp949/cp932/cp936 and encode
none of the em dash, arrow or middle dot these files print; a bare `LC_ALL=C`
does the same on POSIX. The English `windows-latest` runner uses cp1252, which
encodes the em dash — which is why CI never saw the writing half, and why the
reading half bit it anyway (cp1252 decodes every byte to *something*, so a
round record's 🔴 arrives as four other characters, and an open blocking
finding passes).

Three decisions live here, and each was paid for once already on the branch
that first attempted this, in a pull request that was closed:

**Unconditional, not `if os.name == "nt"`.** Where a stream is already UTF-8
this is a no-op, and branching on the platform would leave the Windows path
proven by nothing while Linux CI runs the other one.

**`stdin` is in the loop.** The payload is where the non-ASCII actually is — it
carries the user's own command text, and one Korean path or an em dash in a
commit subject is enough. `hooks/dispatch.py` holds the only stdin read
production takes, so a raise there takes every gate in the group down at once,
and `hooks.json` runs `python3 … || py -3 …`, so the retry meets an
already-consumed stdin and passes silently a second time. Round 2 of that pull
request found this defect INSIDE the first fix.

**`errors` is named.** `TextIOWrapper.reconfigure` resets it to `strict`
whenever `encoding` is given without it, so naming the encoding alone turns a
degradable character into a crash — round 1 of that pull request found exactly
that, on `sys.stderr`, which ships as `backslashreplace`. A path holding a lone
surrogate must degrade, not take the gate down on its way to reporting
something.

The call sites are each entry point's `__main__`, not this module's import,
because a module that changes the process's streams as a side effect of being
imported would do it to `pytest` too. Every gate is also runnable on its own —
that is how the tests drive them and how anyone debugging one reaches them — so
each carries the call rather than relying on `dispatch.py` having made it.

The five scripts under `skills/*/scripts/` spell the loop inline instead of
importing this. They are standalone by design and assume nothing about their
import path; four lines duplicated is cheaper than the machinery that would
avoid it, and what must not diverge is the ANSWER, which is written down here.
"""

import sys

# stderr keeps `backslashreplace`, which is what Python ships it with and what
# makes an undecodable path degrade rather than raise while it is being
# reported.
STREAMS = (("stdin", "replace"), ("stdout", "replace"), ("stderr", "backslashreplace"))


def to_utf8():
    """Put this process's three streams into UTF-8. Idempotent, and a no-op
    where they already are.

    `hasattr` rather than a `None` check, because a stream can be absent (a
    process invoked with stdin closed) or be something without `reconfigure`
    at all — pytest's capture objects are the case the suite meets.
    """
    for name, errors in STREAMS:
        stream = getattr(sys, name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors=errors)
