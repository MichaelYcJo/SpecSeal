"""The commit gate's judgment: which arms a commit is missing, and what a
refusal says (#692).

Two parties render it. `hooks/git/pre-commit.py` and
`hooks/git/reference-transaction.py` judge a commit inside git, in the
worktree it lands in, and refuse it by exiting non-zero with the texts below.
`hooks/commit-review-gate.py` is the PreToolUse reading 0.16.0 shipped, kept
for a clone whose hooks slot is foreign (`questions.md` P1 and P5), and it
asks `arms_missing` the same question and keeps its own 0.16.0 texts. One
judgment, so the two cannot come to disagree about WHETHER a commit is
stopped; two renderings, because one of them can put a question to a person
and the other cannot.

**The two arms**, as `docs/the-review-and-parity-arms.md` defines them:

  * review -- the repository opted in (`hooks/optin.py`), no routing
    declaration names the branch (`hooks/routing.py#declared`), nothing waived
    it, and the review mark under the git directory does not name HEAD;
  * parity -- the repository declares a migration config, the change reaches
    outside the document roots, nothing waived it, and the parity mark does not
    name HEAD.

**What a refusal says** follows from where it is read. git prints a hook's
stderr into the output of the command that ran git, so the model reads it as
the Bash tool's result. There is no `ask` -- a git hook cannot render two
buttons -- so the person's choice comes back the way `AskUserQuestion` brings
it: the model asks, then types the way on the person picked. Every refusal is
the same text on every attempt (W2): the budget a once-per-session question
used to spend existed because the second attempt fell to an `ask`, and there
is no `ask` left for it to fall to. Under the `automation` press no question
is put at all, as before (#662, #665).

**The ways on name commands that run.** The git-native waiver is
`git -c specseal.waive=review commit …`: git hands `-c` to the hook through
`GIT_CONFIG_PARAMETERS` (phase 1's M11), the word stays in the command where
shell history keeps it, and inside a commit message it is prose rather than a
waiver. The older `: '[no-review]'; git commit …` keeps working through
`hooks/answers.py` (P3, answer (a)), and every refusal names it second.
"""

import os
import subprocess

import optin
import routing

REVIEW = "review"
PARITY = "parity"

# The mark files the review chain and the legacy-parity skill write under the
# git directory, each holding the HEAD they were taken at.
MARKS = {REVIEW: "specseal-reviewed", PARITY: "specseal-parity"}

# The old bare-word spelling of each arm's waiver, which `hooks/answers.py`
# carries to the hook (P3).
TOKENS = {REVIEW: "[no-review]", PARITY: "[no-parity]"}

# `seal/` as a string rather than `optin.HOME` joined under anything: these
# classify paths as `git diff` prints them, repository-relative. The line is
# the PARITY arm's alone -- `docs/the-review-and-parity-arms.md` §*Review arm*
# (#518) holds why the review arm reads no paths.
DOC_ROOTS = ("docs/", "seal/")


def git(args, cwd):
    """git's stdout, stripped, or "" on any failure."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def read_mark(cwd, git_dir, name):
    """Contents of a <git-dir> mark file, or "" when absent/unreadable."""
    if not git_dir:
        return ""
    path = os.path.join(cwd or ".", git_dir, name)
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except OSError:
        return ""


def touches_code(paths):
    """True when one of `paths` is outside the document roots."""
    return any(not path.startswith(DOC_ROOTS) for path in paths)


def arms_missing(cwd, top, waived, paths, head=None):
    """The arms this commit is missing in the repository at `top`, in order.

    `waived` holds the arms the command waived. `paths` is a zero-argument
    callable returning the paths the commit carries; it is asked only when the
    parity arm otherwise stands, because reading them costs a `git diff` the
    review arm never needs. `head` is the HEAD the marks are compared with,
    read here when the caller did not.

    `top` is "" where `cwd` is no repository, and nothing is missing there:
    the direction this gate has always failed in, with `optin` stating the
    same rule one layer down.
    """
    if not top:
        return []
    if head is None:
        head = git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    git_dir = git(["rev-parse", "--git-dir"], cwd)
    missing = []
    if (
        REVIEW not in waived
        and optin.opted_in(cwd)
        and not routing.declared(cwd, top)
        and (not head or read_mark(cwd, git_dir, MARKS[REVIEW]) != head)
    ):
        missing.append(REVIEW)
    if (
        PARITY not in waived
        and optin.parity_config(cwd)
        and touches_code(paths())
        and (not head or read_mark(cwd, git_dir, MARKS[PARITY]) != head)
    ):
        missing.append(PARITY)
    return missing


def declaration_hint(top):
    """The declaration path a refusal tells a session to write, relative to
    `top` and spelled the way the platform spells it.

    Under the root this repository resolves to: in local mode that root is
    under the git directory. A linked worktree on another Windows drive has no
    relative spelling (`ntpath.relpath` raises), and the absolute path is the
    one to type there (round 1 of #80, 🔴 1).
    """
    home = optin.home_at(top)
    if not home:
        return f"{routing.WORK_ITEMS}/<work-item-id>/{routing.FILENAME}"
    try:
        rel = os.path.relpath(home, top)
    except ValueError:
        rel = home
    return os.path.join(rel, optin.WORK_ITEMS, "<work-item-id>", routing.FILENAME)


# --- what a refusal from inside git says -------------------------------------

HEADER = "SpecSeal stopped this commit; nothing was committed."

STATES = {
    REVIEW: (
        "No review is recorded for this cycle in {top}, the repository this "
        "commit lands in, and no routing declaration names its branch "
        "`{branch}`. The code-review skill writes the reviewed HEAD to that "
        "repository's .git/specseal-reviewed."
    ),
    PARITY: (
        "{top}, the repository this commit lands in, declares a migration "
        "config, so behaviour there is ported and the original decides where "
        "policy is silent. Nothing records that the original was consulted "
        "for this change: the legacy-parity skill writes the compared HEAD to "
        "that repository's .git/specseal-parity."
    ),
}

QUESTIONS = {
    REVIEW: "This commit closes a cycle nothing reviewed. Which way?",
    PARITY: "Nothing records that the original was consulted for this change. "
    "Which way?",
}


def waiver(arms):
    """The git-native spelling that waives `arms` and still commits."""
    return "git " + " ".join(f"-c specseal.waive={arm}" for arm in arms) + " commit …"


def old_waiver(arms):
    """The bare-word spelling 0.16.0 advised, still read (P3)."""
    return ": " + " ".join(f"'{TOKENS[arm]}'" for arm in arms) + "; git commit …"


def options(arm, top):
    """The arm's ways on, as (label, detail), each naming a command that runs."""
    if arm == REVIEW:
        declaration = declaration_hint(top)
        return (
            (
                '"Declare the routing"',
                f"this commit belongs to a work item whose `{declaration}` is "
                "not written yet. Write it from `templates/sdd-routing.md`, "
                "naming this branch, then re-issue the commit unchanged. The "
                "Review row is the user's answer and not yours: put both "
                "spellings, `through the review chain` and `straight to the "
                "PR`, to them before writing the file. The declaration is read "
                "from the working tree, so it covers the very commit that adds "
                "it, and CI checks the answer it records at the pull request.",
            ),
            (
                '"Review it first"',
                "hand the change to the review chain, @agent-specseal:warden or "
                f"/specseal:code-review, run against {top}. The mark it writes "
                "there is what lets the same commit through.",
            ),
            (
                '"Commit without a review"',
                f"re-issue it as `{waiver([REVIEW])}`. The older spelling, "
                f"`{old_waiver([REVIEW])}`, still works.",
            ),
        )
    return (
        (
            '"Compare against the original"',
            "run the legacy-parity skill against the baseline in "
            f"{top}'s migration config. The mark it writes there is what lets "
            "the same commit through.",
        ),
        (
            '"Commit without comparing"',
            f"re-issue it as `{waiver([PARITY])}`. The older spelling, "
            f"`{old_waiver([PARITY])}`, still works.",
        ),
    )


SPELLED = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}

BACKSTOP = (
    "This commit did not pass through pre-commit -- `--no-verify`, or a hook "
    "that did not run -- and was met where its branch moves instead. HEAD, the "
    "index and the working tree are as they were."
)

AUTOMATION = (
    "This session's person pressed `automation` on the routing question, so "
    "no question is put to them, and none is to be put to them in its place: "
    "the run was promised that nothing would stop to ask.\n\n"
    "The ways on, none of which needs a person:\n"
    "  1. Only for a commit that belongs to no work item: re-issue it as "
    "`{waiver}`. The older spelling, `{old}`, still works.\n"
    "  2. Otherwise, do not retry it: write the commit down and hand it back "
    "at the end of the run."
)

UNCHANGED = "Re-issuing this commit unchanged meets this same refusal."


def refusal(arms, top, branch, pressed, backstop=False):
    """The whole text a refused commit prints, for `arms` in `top`."""
    states = [
        STATES[arm].format(top=top, branch=branch or "(detached)") for arm in arms
    ]
    lines = [HEADER, ""]
    if backstop:
        lines += [BACKSTOP, ""]
    lines.append("\n\n".join(states))
    lines.append("")
    if pressed:
        lines.append(AUTOMATION.format(waiver=waiver(arms), old=old_waiver(arms)))
    else:
        if len(arms) > 1:
            lines.append(
                "Do not choose for the user. Ask with the AskUserQuestion tool, "
                "putting every question below in ONE call -- each is waived on "
                "its own, and one call costs one interruption:"
            )
        else:
            count = len(options(arms[0], top))
            lines.append(
                "Do not choose for the user. Ask with the AskUserQuestion tool, "
                f"offering exactly these {SPELLED.get(count, str(count))} options:"
            )
        for arm in arms:
            lines.append("")
            lines.append(f"  {QUESTIONS[arm]}")
            for number, (label, detail) in enumerate(options(arm, top), 1):
                lines.append(f"    {number}. {label} — {detail}")
        lines.append("")
        lines.append("Then do what they picked.")
    lines.append("")
    lines.append(UNCHANGED)
    return "\n".join(lines)
