#!/usr/bin/env python3
"""PostToolUse reminder: keep the round records flowing in both directions.

Three branches with different conditions — the failure modes differ:

  posting a review  → the round record MISSING is the problem
                      (this is the only moment the session still holds its
                      verdicts and probe results; remind it to write
                      rounds/round-N.md, tests-todo.md, evidence-todo.md)

  reading a review  → a round record EXISTING but unread is the problem
                      (inline comments may not contain the todo lists at all;
                      remind the fixer to open them)

  merging           → the records NOT CLOSED is the problem. Once, the
                      directory was deleted before the merge, and that
                      deletion was the deadline that forced the draining.
                      Keeping the records removes the deadline, so the
                      reminder replaces it: a merge with unresolved rows still
                      open leaves a prescribed test unplanted or a verified
                      fact unmerged, and after the merge nobody is looking.

WHICH directory. The records used to live at `.specseal/handoff/PR-<n>/`,
keyed by a pull request number. That number does not exist while the rounds
that would fill it are running, so no correct session could create the
directory, and none ever did — the reminder above fired against a path that
has never existed in this repository. They now live beside the work item, at
`specs/<work-item-id>/rounds/`, which exists from the first commit because the
routing declaration is written before the first edit.

`rounds/` is one level below the work item, and the flat location it replaced
is not read at all. That is a deliberate trade against a permanent dual read,
and what buys it back is a fourth branch: a record still sitting flat is named
out loud, with the directory it must move to. Nothing migrates a repository
that updates the plugin, so that sentence is the whole migration path — and it
fires before the three branches below, because a work item whose records are
unreadable is a different problem from one that has none.

The work item is resolved through the same key the commit gate uses: the
declaration names its branch, and the checked-out branch looks it up. So this
reminder needs a routing declaration to say anything at all. A `gh pr merge`
run from a branch that declared nothing is not reminded — the cost of one
key instead of two, and the enforcement that replaced the deadline is the
pull-request check in CI, not this.

Reminder-only (PostToolUse cannot block). Active only in repos with `.specseal/`
at the root — a globally installed plugin must not nag unrelated repos.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin
import routing

POST_RE = re.compile(
    r"\bgh\s+pr\s+(review|comment)\b"
    r"|\bgh\s+api\b(?=.*(?:-X|--method)\s+POST)(?=.*/pulls/\d+/(reviews|comments))"
)
READ_RE = re.compile(
    r"\bgh\s+pr\s+view\b(?=.*--json\s+\S*comments)"
    r"|\bgh\s+api\b(?!.*(?:-X|--method)\s+POST)(?=.*/pulls/\d+/(comments|reviews))"
)
MERGE_RE = re.compile(r"\bgh\s+pr\s+merge\b")
# A closed directory says so in writing. Any of these spellings counts: the
# point is that a human or a session wrote a closing line, not that it matched
# one phrase.
CLOSED_RE = re.compile(r"nothing to drain|drained|closed", re.IGNORECASE)


def is_closed(records):
    """True when some round record says the rows were drained."""
    if not records:
        return True  # nothing to close
    for path in records:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                if CLOSED_RE.search(f.read()):
                    return True
        except OSError:
            return True  # unreadable: say nothing rather than nag wrongly
    return False


SEG_RE = re.compile(r"&&|\|\||[;\n|]")
# RIDER: two things at this coordinate, both the shapes the commit gate fixed.
# `gh_segments` never reads `gh -R/--repo`, so a `gh` command aimed at another
# repository is recorded against this one -- the same defect `-C` was for
# `git`. And this is a second copy of `WRAPPERS` and the wrapper-skipping loop
# (`hooks/worktree-guard.py:118,152` holds the other); the commit gate imports
# that parsing rather than copying it, for the reason `optin.py` gives for
# existing at all. Left because this hook only emits a notice, so the failure
# is a misfiled reminder rather than a commit going through.
# Verified 2026-08-31 at 9829412.
WRAPPERS = {"command", "env", "nohup", "time", "sudo"}


def gh_segments(command):
    """Segments whose command word is gh — prose mentions never remind."""
    import shlex

    out = []
    for seg in SEG_RE.split(command):
        try:
            toks = shlex.split(seg)
        except ValueError:
            continue
        i = 0
        while i < len(toks) and (
            ("=" in toks[i] and not toks[i].startswith("-"))
            or os.path.basename(toks[i]) in WRAPPERS
        ):
            i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "gh":
            out.append(" ".join(toks[i:]))
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if payload.get("tool_name") != "Bash":
        return
    raw = (payload.get("tool_input") or {}).get("command", "")
    segs = gh_segments(raw)
    if not segs:
        return
    command = "\n".join(segs)
    cwd = payload.get("cwd", "") or "."

    # `optin.repo_root`, not a third `rev-parse`. This was the one root
    # resolver of the three still handing back git's spelling, and `top` goes
    # straight into `routing.item_dir` -> `os.path.join` and then
    # `os.path.relpath` -- the mixed shape the other two were changed to stop
    # producing. It also inherits that helper's named encoding, which is what
    # keeps a repository under a path this locale cannot decode from turning
    # `.stdout` into None.
    top = optin.repo_root(cwd)
    if not top or not optin.opted_in(cwd):
        return

    item = routing.item_dir(top, routing.current_branch(cwd))
    if not item:
        return
    rel = os.path.relpath(item, top)
    # The path a person has to recognise and then TYPE, spelled the way their
    # platform spells it. `rel` comes from `os.path.relpath`, which is native,
    # and joining `ROUNDS_DIR` with a literal `/` produced
    # `specs\\item/rounds` on Windows — half of one command in each dialect.
    # `optin.repo_root` was changed for the same reason: the gates print these
    # to someone who has to find their own repository in them. CI's windows
    # leg is what caught it, which is the row the memo left for it.
    where = os.path.join(rel, routing.ROUNDS_DIR)

    # Said before anything else, and said even when `rounds/` also holds
    # records. A record left at the work item's top level is not read by
    # anything any more, and the reader that merely found nothing would print
    # the same silence as a work item that never ran a review -- which is the
    # state most work items are in and the state that must stay quiet. The
    # message therefore names the file AND the directory it belongs in:
    # nothing migrates a repository that updates the plugin, so this sentence
    # is the entire migration path.
    strays = routing.stray_rounds(item)
    if strays:
        named = ", ".join(os.path.relpath(s, top) for s in strays)
        print(
            f"[specseal] {named} — a round record where nothing reads it. "
            f"Round records live in {where}{os.sep} now: "
            f"`mkdir {where} && git mv` them there — "
            f"`git mv` does not create its destination. Left where they "
            f"are, every gate reads this "
            f"work item as one that never ran a review."
        )

    # Said in every branch, for the reason the stray message above is: a
    # `rounds` that is a FILE — or a symbolic link, which git spells
    # `120000` and an allow-list of regular modes lets through — reads as
    # no records at all, so a review whose
    # whole text git is carrying reports as one that never happened. Reached
    # by following this release's own migration command with the trailing
    # slash dropped, which succeeds for a single record.
    unreadable = routing.rounds_unreadable(item)
    if unreadable:
        print(
            f"[specseal] {where} is not a directory, so "
            f"nothing can read a round record out of it — and a "
            f"review that happened then reads exactly like one that did not. "
            f"`git mv … {routing.ROUNDS_DIR}` without the trailing slash does "
            f"this to a single record. Open it: if it is your round record, "
            f"`mkdir` the directory and move it inside."
        )

    records = routing.rounds(item)

    if POST_RE.search(command):
        if not records and not strays and not unreadable:
            print(
                f"[specseal] A review was just posted but "
                f"{where}{os.sep} holds no round record. Write "
                f"{os.path.join(routing.ROUNDS_DIR, 'round-N.md')} (target "
                f"SHA, verdicts, probe "
                f"results, and the Pass checkbox), tests-todo.md, and "
                f"evidence-todo.md now — after this session ends, nobody can."
            )
    elif MERGE_RE.search(command):
        if records and not is_closed(records):
            print(
                f"[specseal] {rel}{os.sep} has no closing note. Before the merge, "
                f"move every unresolved row to a durable home — tests to the "
                f"implementation commit, facts to the evidence ledger, the "
                f"rest to follow-up — and write what went where (or `nothing "
                f"to drain`). The records are kept, not deleted; after the "
                f"merge nobody is looking at these rows."
            )
    elif READ_RE.search(command):
        if records:
            print(
                f"[specseal] {rel}{os.sep} holds a round record. Read it before "
                f"acting on inline comments — tests-todo.md and "
                f"evidence-todo.md are implementer-owned lists that the "
                f"comments may not contain."
            )


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
