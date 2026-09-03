#!/usr/bin/env python3
"""PreToolUse gate: a commit needs a review in its cycle.

The code-review skill marks a completed review by writing the reviewed HEAD
into <git-dir>/specseal-reviewed. A commit closes that cycle (HEAD moves),
so the next commit needs a fresh review mark.

Which repository: the one the command commits INTO, not the one the shell
sits in. `git -C <path> commit` moves git without moving the shell, and the
gate used to resolve everything from the payload's `cwd` — so a commit landing
in a scratch repository was gated against whichever repository the session
happened to be working in, and every such command cost the user a prompt for a
verdict about a repository the commit would not touch. The `-C` parsing comes
from hooks/worktree-guard.py, which was fixed for this same defect one release
earlier.

Reading `-C` opened a hole of its own. This hook sees the command
before the shell expands it, so `git -C "$WT" commit` hands it the literal
characters `$WT`: a directory that does not exist, resolving to no repository.
That is not a repository checked and found clean, it is one never looked at,
and both used to produce the same silence. An unresolved `-C` now stops the
commit — in a session whose OWN repository opted in, which is what gives a
globally installed plugin standing to speak about a target it cannot name. The
session's repository decides whether the gate speaks, never what is true of the
target: judging an unknown target against the session's marks would answer for
a repository the commit may never touch.

Opt-in per repository: the gate is active only where the preset workflow is in
use, detected by a `seal/` root (see hooks/optin.py for the two places it is
read at). Everywhere else this hook stays silent — a globally installed plugin
must not nag unrelated repos.

A repo that declares `seal/parity.md` opts into a second check: ported
behavior follows the original where policy is silent, so a commit touching
code should carry a record that the original was consulted. The legacy-parity
skill writes the compared HEAD to <git-dir>/specseal-parity.

Both opt-ins are independent — a repo may declare either, both, or neither.

Decisions:
  - not a git commit, or no opt-in applies → allow
  - each applicable mark matches current HEAD → allow
  - otherwise → deny once, and spend the reason on an AskUserQuestion
    instruction naming both ways on for every arm that fired
  - every attempt after that one → ask, naming every missing mark at once
    (approving IS the waiver — no separate bypass mechanism to maintain)

A hook returns allow/deny/ask and nothing else, and the harness renders an
`ask` as two buttons the model never sees. Declining is then a bare "No": the
user who wanted the OTHER way on has to retype the command themselves. Both
answers have to lead somewhere, so the gate denies instead and asks the model
to put the options up with AskUserQuestion — the same shape, and the same
measurement, as hooks/review-skill-gate.py.

Denying every time would trap the session that picks a way on the gate cannot
detect from the command alone, so the question fires once per session per
repository (<git-dir>/specseal-commit-choice/<session-id>) and every attempt
after that gets the plain `ask` this gate has always returned. That fallback
is also what an environment with nobody to answer lands on: one extra round
trip, then today's behavior.

The skip markers (`[no-review]`, `[no-parity]`) must appear as a BARE WORD in
the command, not anywhere in its text: `git commit -m "fix [no-review] later"`
carries the marker inside the message, where the author is describing work
rather than waiving a gate. A substring test cannot tell those apart.

How the marker is READ and where it can be TYPED are different questions, and
the prompts answered the second one wrongly for three releases.
After `git commit` a bare word is a pathspec, so the form the gate advised was
rejected by git every time it was followed. `waiver_form` below carries the one
that runs, and why the obvious alternative does not.
"""

import collections
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reading a command line is neither gate's property; `hooks/cmdline.py` owns
# it and both gates import it by plain name, which goes through `sys.modules`
# and runs once. This gate used to reach `parse_git` and `apply_chdir` by
# loading `hooks/worktree-guard.py` from disk, which only re-exports them
# from here — and that load could fail, taking the gate's parsing with it
# while leaving the gate running and silent.
import console
import optin
import routing
from cmdline import (
    EXPANDS,
    Unresolved,
    compose,
    drop_comments,
    drop_heredoc_bodies,
    heredoc_bodies,
    parse_git,
    split_segments,
    split_segments_with_separators,
    strip_subshell,
    walk_directories,
)

# `where` is the directory this invocation's git would actually run in, filled
# in by commit_targets once `cwd` is known. commit_invocations parses a command
# without one, so it defaults to empty and callers fall back to the group's cwd.
#
# `base` is the directory the SHELL is in when this invocation runs, which is
# not the same question: a `cd` earlier in the command moves it, and `where` is
# that plus this invocation's own `-C`. It defaults to None, meaning "the
# caller's cwd" — a caller parsing a command without one gets exactly the
# answer this gate gave before the walk existed.
Invocation = collections.namedtuple(
    "Invocation", "args chdirs where base", defaults=("", None)
)

# One marker file per session per repository. Empty; its existence is the fact.
CHOICE_DIR = "specseal-commit-choice"


def _hides_a_commit(text):
    """True when TEXT, read as commands, might invoke `git commit`.

    Only called where the shell really does execute TEXT as commands — a
    heredoc body an interpreter reads from stdin, or the argument `eval`
    re-parses — never on prose. Reusing `parse_git`'s own rule, that a
    segment's own first token must literally be `git`, is what keeps this
    from reading a commit MESSAGE that happens to mention the words: a
    heredoc feeding `git commit -F -` has "words" as its own line, not a
    segment whose command word is `git`.

    "Might", not "does": recurses into a heredoc body or an `eval` argument
    TEXT itself opens — `bash <<'OUTER'` whose body runs `bash <<'INNER'`, or
    `eval eval '…'`, each really execute one construct deeper than a single
    segment scan sees — and an `eval` argument this process cannot expand
    before the shell does (`_eval_hides_a_commit`'s `EXPANDS` check) counts
    the same as a confirmed one, because there is no way to tell "reduces to
    a commit" from "reduces to something else" without running the shell.
    Both used to return nothing found.
    """
    text = drop_comments(text)
    stripped = drop_heredoc_bodies(text)
    segments, _clean = split_segments(stripped)
    for toks in segments:
        parsed = parse_git(toks)
        if parsed and parsed[0] == "commit":
            return True
        arg = _eval_argument(toks)
        if arg is not None and _eval_hides_a_commit(arg):
            return True
    return any(_hides_a_commit(body) for body in heredoc_bodies(text))


def _eval_argument(toks):
    """The text `eval` would re-parse as a command, or None when TOKS isn't eval.

    `eval` concatenates its remaining arguments with a space and re-parses
    the result as a command — the same question `_hides_a_commit` answers,
    just handed the tokens after `eval` instead of a dropped heredoc region.
    The skip here mirrors `cmdline.understood`'s own assignment/subshell skip,
    the same rule that already marks a bare `eval` segment's OWN directory
    `Unresolved` for `cd`-tracking. `source`/`.` sit beside `eval` in
    `RELOCATORS` but take a file, not inline text, so there is nothing here to
    re-parse for them.
    """
    toks, opened = strip_subshell(list(toks))
    if opened:
        return None
    while toks and "=" in toks[0] and not toks[0].startswith("-"):
        toks.pop(0)
    if not toks or toks[0] != "eval":
        return None
    return " ".join(toks[1:])


def _eval_hides_a_commit(arg):
    """True when ARG — the text `eval` would re-parse — might read as a commit.

    A value this process cannot expand before the shell does (`$(...)`, a
    bare `$VAR`, a glob) is unreadable rather than cleared: `EXPANDS` is the
    same set that already makes a `cd` operand or a `git -C` value
    `Unresolved` everywhere else in this module, and the direction is the
    same one — there is no way to tell "this reduces to a commit" from "this
    reduces to something else" without running the shell, so it stops the
    same way a confirmed commit does rather than passing silently because the
    literal text does not spell `git commit`.
    """
    return any(ch in arg for ch in EXPANDS) or _hides_a_commit(arg)


def _unresolved_base(base):
    """BASE as an `Unresolved(CONSTRUCT)` — the target a hidden commit denies against.

    A heredoc body or an `eval` argument is read for whether it commits, not
    for where — `bash`/`eval`'s own segment already has a `base` from the
    walk, and where none applies (a heredoc body, or `commit_invocations`
    called with no `cwd`) this is the session's own directory, the same
    stand-in `eval 'cd <T>' && git commit` already denies against.
    """
    if isinstance(base, Unresolved):
        return base
    return Unresolved(str(base) if base is not None else "", Unresolved.CONSTRUCT)


def commit_invocations(command, cwd=None):
    """Every `git ... commit ...` invocation, as (args, chdirs) — empty when none.

    `args` are the tokens after the `commit` subcommand. `chdirs` are the
    `git -C <path>` values, which decide WHICH repository the commit lands in.

    `cwd` is the directory the shell starts in, and passing it is what makes a
    `cd` earlier in the command count. Each invocation comes back once per
    directory the shell may be in when it runs — more than one only where the
    command branches (`cd X || git commit` commits where the shell already
    was, and reaches X only if the `cd` failed). Leaving `cwd` out asks the
    older question, "what does this command commit", and every invocation then
    defers to the caller's own directory.

    Only a segment whose COMMAND WORD is git with subcommand commit counts; a
    prose mention (echo "git commit", heredoc lines) must not gate. That, and
    the skipping of git's global options to find the subcommand, is what
    `cmdline.parse_git` does — this used to hold a second copy of it, which
    read `-C` only to step over it.

    Two more shapes commit without ever being a segment whose command word is
    `git`: a heredoc body an interpreter executes from stdin, and
    an `eval` argument the shell re-parses. Both come back as an invocation
    with no `args`/`chdirs` of their own and a `base` that is `Unresolved`
    (`CONSTRUCT`) — there is no repository to name, only that the command
    reads as one committing somewhere, so the caller stops the same way it
    already does for `eval 'cd <T>' && git commit`.

    Returns (invocations, parsed_cleanly). When the command cannot be
    tokenized at all, a fail-open pass would exempt exactly the commands too
    gnarly to parse — the caller gates an unparseable command that mentions
    both `git` and `commit` anyway (the gate only asks; a false positive costs
    one approval click).

    There is no fallback for the parser not loading, and that is the change.
    It used to be reached by loading `hooks/worktree-guard.py` from disk, and
    a load that failed returned None here: the gate kept running with no
    parser at all, which read as "every command is unparseable" and produced
    three wrong answers at once. `cmdline` is imported by name like `optin`,
    so a broken one is an ImportError at module load — and a gate that does
    not load has no verdict to give, which is the honest shape. `dispatch.py`
    is where that silence is decided for every gate, and it is the place to
    change it.
    """
    # A JUDGMENT read, so the comments and the heredoc bodies both go first:
    # each is text the shell does not execute, and every newline in one was
    # being read as a segment separator. `has_marker` below is a CONSENT read
    # and deliberately still sees the whole command, because a waiver token is
    # written inside a comment on purpose.
    #
    # `drop_comments` was missing here while `hooks/worktree-guard.py:201` had
    # it, and for a while that cost nothing: a comment segment's first token is
    # `#`, which is neither a `cd` nor a `git`, so nothing read it. Reading a
    # segment for what CONSTRUCT it is ended that — `# stage everything; then
    # commit` splits at the `;` and the next segment starts with the reserved
    # word `then`, so an ordinary commit two lines later was stopped for a
    # sentence in English.
    items, clean = split_segments_with_separators(
        drop_heredoc_bodies(drop_comments(command))
    )
    walked = (
        walk_directories(items, cwd)
        if cwd is not None
        else [(tokens, (None,)) for _, tokens in items]
    )
    found = []
    for toks, bases in walked:
        parsed = parse_git(toks)
        if parsed and parsed[0] == "commit":
            for base in bases:
                found.append(Invocation(parsed[1], parsed[2], base=base))
            continue
        arg = _eval_argument(toks)
        if arg is not None and _eval_hides_a_commit(arg):
            for base in bases:
                found.append(Invocation((), (), base=_unresolved_base(base)))

    for body in heredoc_bodies(drop_comments(command)):
        if _hides_a_commit(body):
            found.append(Invocation((), (), base=_unresolved_base(cwd)))

    return found, clean


def commit_targets(cwd, invocations, root_of=None):
    """(directory, invocations) for each repository this command commits into.

    `git -C <path>` moves git without moving the shell, so the directory to
    judge comes from the command and falls back to `cwd` only when the command
    names none. Repeated `-C` compose, each resolved against the one before it
    (verified against git 2.50), which is what `apply_chdir` already does for
    the worktree guard.

    Order is kept and duplicates merge, so one command committing twice into
    the same repository is judged once and one committing into two is judged
    for both. A command nothing could tokenize yields the session's cwd alone,
    which is the only directory such a command gives the gate to work with.

    `cwd` is where the SHELL starts, not where every invocation runs: an
    invocation carrying a `base` from the walk starts from there instead, so a
    `cd` in front of the commit reaches the target the same way a `-C` does.
    A base the walk could not identify stays unidentified through the join
    unless an absolute `-C` replaces it, and the caller stops rather than
    judging it — `docs/review-chain-spec.md` gives an unresolvable target that
    treatment already, and this is that partition rather than a second one.

    What makes two directories the SAME target is `root_of`, not the string:
    `git commit && git -C <repo>/sub commit` names two directories and one
    repository. Grouping by the string judged that repository twice and
    announced its own subdirectory as a further one, which is not a repository
    at all. Callers with no way to resolve a root pass none and get grouping by
    directory, which is what the parsing tests want.

    Merging by root leaves the group with ONE cwd, and that is not enough for
    everything downstream: a pathspec is resolved against the directory git
    runs in, so `git -C <repo>/sub commit && git -C <repo> commit -m y f.py`
    looked for `<repo>/sub/f.py`, found nothing, and the migration-config arm
    lost its grounds to fire. Each invocation therefore carries its own `where`
    and the group's cwd is only a fallback.
    """
    if not invocations:
        return [(cwd, [])]
    targets, seen = [], {}
    for inv in invocations:
        where = compose(cwd if inv.base is None else inv.base, inv.chdirs)
        if isinstance(where, Unresolved):
            # Never grouped with a repository, and never with another
            # unreadable target that spells a different path — nor with one
            # that spells the same path for a different reason, because the
            # two get different prompts.
            key = (Unresolved, where.why, str(where))
        else:
            key = (root_of(where) if root_of else "") or where
        if key not in seen:
            seen[key] = len(targets)
            targets.append((where, []))
        targets[seen[key]][1].append(inv._replace(where=where))
    return targets


def is_git_commit(command):
    """True when some segment actually invokes `git commit`."""
    found, clean = commit_invocations(command)
    if found:
        return True
    return not clean and "git" in command and "commit" in command


# `git commit` options that consume the NEXT token as their value. A pathspec
# scan that misses one reads that value as a file path (`-m fix` → `fix`).
# Options in `--name=value` form need no entry; they carry their own value.
VALUE_OPTS = {
    "-m",
    "--message",
    "-F",
    "--file",
    "-c",
    "--reedit-message",
    "-C",
    "--reuse-message",
    "--fixup",
    "--squash",
    "--author",
    "--date",
    "-t",
    "--template",
    "--cleanup",
    "--trailer",
    "--pathspec-from-file",
}
ALL_OPTS = {"-a", "--all"}


def commit_shape(tokens):
    """(commits_all, pathspecs) for one `git commit` invocation.

    `-a` commits every tracked modification, and a trailing pathspec commits
    those paths — neither passes through the index, so a staged-only view of
    the change sees nothing at all.
    """
    commits_all, paths, i, only_paths = False, [], 0, False
    while i < len(tokens):
        tok = tokens[i]
        if only_paths:
            paths.append(tok)
            i += 1
            continue
        if tok == "--":
            only_paths = True
            i += 1
            continue
        if tok in VALUE_OPTS:
            i += 2
            continue
        if tok.startswith("--"):
            if tok.split("=", 1)[0] in ALL_OPTS:
                commits_all = True
            i += 1
            continue
        if tok.startswith("-") and len(tok) > 1:
            # Short cluster: -am is -a plus -m, and -m still eats the next
            # token unless its value is glued on (-mfix).
            body = tok[1:]
            if "a" in body:
                commits_all = True
            for pos, ch in enumerate(body):
                if f"-{ch}" in VALUE_OPTS:
                    if pos == len(body) - 1:
                        i += 1
                    break
            i += 1
            continue
        paths.append(tok)
        i += 1
    return commits_all, paths


def git(args, cwd):
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def read_mark(cwd, git_dir, name):
    """Contents of a <git-dir> mark file, or "" when absent/unreadable."""
    if not git_dir:
        return ""
    path = os.path.join(cwd or ".", git_dir, name)
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return ""


def changed_paths(cwd, invocations):
    """Paths this commit would carry, across all its forms.

    A commit reaches the tree three ways and only one of them goes through
    the index, so a `--cached`-only view answered "nothing changed" for
    `git commit -am x` and for `git commit -m x file.py` — the gate then went
    silent on exactly the two forms people type by hand.

    Each invocation is read in the directory ITS git would run in. A pathspec
    is resolved against that directory, so reading one invocation's pathspec
    from another's directory finds nothing and reports a commit that carries
    no files. The output side needs no such care — `--name-only` prints paths
    from the repository root wherever it runs, checked directly — so only the
    pathspec argument was ever wrong.
    """
    paths = set()

    def collect(where, args):
        out = git(["diff", "--name-only", *args], where or cwd)
        paths.update(line for line in out.splitlines() if line)

    collect(cwd, ["--cached"])
    for inv in invocations:
        commits_all, pathspecs = commit_shape(inv.args)
        if commits_all:
            collect(inv.where, ["HEAD"])
        if pathspecs:
            collect(inv.where, ["HEAD", "--", *pathspecs])
    return paths


# `seal/` as a string rather than `optin.HOME` joined under anything: these
# classify paths as `git diff` prints them, repository-relative, and a path
# in a diff is only ever the shared root (`docs/one-root-by-lifetime.md`).
DOC_ROOTS = ("docs/", "seal/")


def touches_code(cwd, invocations):
    """True when the change is not confined to the document roots.

    A commit that only moves docs/ or seal/ has nothing to compare against an
    original, and asking there would train people to click through the
    prompt — which costs more than the check is worth.
    """
    paths = changed_paths(cwd, invocations)
    return any(not path.startswith(DOC_ROOTS) for path in paths)


def has_marker(command, marker):
    """True when `marker` appears as a bare word of the command.

    Inside a quoted message it is prose — `git commit -m "drop [no-review]
    from the docs"` describes work, it does not waive a gate. An unparseable
    command falls back to the substring test: the marker is the author's
    explicit opt-out and refusing to read it is worse than reading it loosely.

    **Cleanliness is measured HERE, on the command as written.** It used to
    arrive from the judgment read, and when that read began dropping comments
    the two texts stopped agreeing: `git commit -m x  # don't [no-review]`
    parses cleanly once the comment is gone, so the strict scan ran — on the
    raw command, where the apostrophe swallows the marker into a quote that
    never closes. The waiver was honoured before that change and refused
    after, with nothing to tell the user why. A CONSENT read has to measure
    its own text as well as read it. The parameter that used to carry the
    judgment read's answer is gone rather than defaulted, so there is no
    argument left to pass it through again.
    """
    segments, clean = split_segments(command)
    if not clean:
        return marker in command
    return any(tok == marker for toks in segments for tok in toks)


def already_asked(cwd, git_dir, session):
    """True when this session was already offered the question in this repo.

    Records it when it was not. A marker that cannot be written counts as
    already asked: one missed question beats a deny the session cannot get
    past. The same rule as review-skill-gate.py, though not the same code —
    that one builds its git-dir as `<root>/.git`, which is a FILE in a linked
    worktree.

    The id names a file, so a separator in a malformed one must not become a
    path escape — measured on the sibling guard: `../../escaped` put an empty
    file at the repository root. `hooks/session-lease.py` guards its own id
    the same way.
    """
    session = os.path.basename(str(session or ""))
    if not git_dir or not session or session in (".", ".."):
        return True
    path = os.path.join(cwd or ".", git_dir, CHOICE_DIR, session)
    if os.path.exists(path):
        return True
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    except OSError:
        return True
    return False


# How a waiver is TYPED, which is not how it is read. `has_marker` finds a bare
# word anywhere in the command, and the obvious placement is the one that does
# not work: after `git commit`, a bare word is a PATHSPEC, so
# `git commit -m x [no-review]` is rejected by git before the gate's advice can
# help. The prompt named that form for three releases — the gate
# stopped the commit, the way past it failed, and approving the prompt was left
# as the only thing that worked.
#
# A trailing `# [no-review]` is not the fix either. Measured in three shells:
# it commits under bash and under `zsh -c`, and fails in an INTERACTIVE zsh,
# whose default leaves `#` uncommented and then refuses `[no-review]` as an
# unmatched glob before git is reached at all.
#
# A no-op `:` carrying the quoted marker works in all three. The shell discards
# it, git never sees it, and the word stays in the command where shell history
# keeps it — which is the whole point of a visible waiver.
def waiver_form(markers):
    """The literal text that waives `markers` and still runs."""
    return ": " + " ".join(f"'{m}'" for m in markers) + "; <the same command>"


SPELLED = {2: "two", 3: "three", 4: "four"}


def offer_header(count):
    """The line telling the model how many options to offer, counted.

    Shared by the two prompts that render an option list, because the number
    went stale in exactly the way a written-down count does: the model is told
    to offer EXACTLY what it says, so a `two` beside a list of three is the
    third option being dropped by an instruction. It was written out in both
    places and fixing one left the other -- the defect this counts away is not
    the wrong number, it is the number being a second thing to keep in step.
    """
    return (
        "Do not choose for the user. Ask with the AskUserQuestion tool, "
        f"offering exactly these {SPELLED.get(count, str(count))} options:"
    )


def ask_reason(arms):
    """The plain two-button prompt, for the attempts after the first.

    Its closing sentence names the marker of the arm that actually fired. It
    used to say `[no-review]` unconditionally, which sent a commit stopped by
    the parity arm alone to the one marker that does not silence it.
    """
    ways = " and ".join(arm["way_on"] for arm in arms)
    held = "mark is what silences" if len(arms) == 1 else "marks are what silence"
    form = waiver_form([arm["marker"] for arm in arms])
    # An arm may carry a way on that is neither its mark nor its waiver. This
    # prompt is the one the SECOND attempt reaches, and leaving it at two ways
    # sent a session that had read the first prompt's third option back to a
    # sentence saying there were only two.
    extra = [arm["also"] for arm in arms if arm.get("also")]
    return (
        "\n\n".join(arm["state"] for arm in arms)
        + "\n\nApproving is the waiver — the commit proceeds.\n"
        "Declining cancels the commit and leaves the tree as it is. Two ways "
        f"on from there for any commit: {ways}, whose {held} this, or "
        "re-issue it with the "
        f"waiver in front — `{form}` — when the work was never headed for "
        "that. Written after `git commit` the marker is a pathspec and git "
        "rejects the command." + "".join("\n\n" + e for e in extra)
    )


def question_reason(arms):
    """The first prompt: a deny whose reason hands the choice to the user."""
    lines = ["\n\n".join(arm["state"] for arm in arms), ""]
    if len(arms) > 1:
        lines.append(
            "Do not choose for the user. Ask with the AskUserQuestion tool, "
            "putting BOTH questions in ONE call — each is waived on its own, "
            "and one call costs one interruption:"
        )
    else:
        lines.append(offer_header(len(arms[0]["options"])))
    for arm in arms:
        lines.append("")
        lines.append(f"  {arm['question']}")
        for label, detail in arm["options"]:
            lines.append(f"    {label} — {detail}")
    lines.append("")
    lines.append(
        "Then do what they picked, and do not re-issue this commit before "
        "they answer. A retry reaches the ordinary approval prompt instead, "
        "where approving is the waiver."
    )
    return "\n".join(lines)


UNREADABLE_STATE = (
    "This command commits into {count} it could not resolve to a "
    "repository: {listed}.\n\n"
    "The gate reads the command as it was written, before the shell expands "
    'it, so `-C "$VAR"` arrives as the literal characters `$VAR` and names '
    "no directory. A path that simply does not exist looks exactly the same "
    "from here. In the first case the commit lands in a real repository whose "
    "review nothing checked, and no token in the command records that."
)

UNREADABLE_CONSTRUCT = (
    "This command contains something the gate cannot read as a plain "
    "command, so it cannot say which repository the commit lands in. The last "
    "directory it could name is {listed}, and the commit may not land "
    "there.\n\n"
    "A function body, a sourced script, an `eval`, a `pushd` and a loop all "
    "move the shell somewhere this reader does not follow. It used to answer "
    "that the shell had stayed put, which was silence wherever that answer "
    "happened to be a repository already declared — and the commit landed in "
    "one nothing had reviewed."
)


def unreadable_reason(paths, first, also_stopped):
    """The prompt for a target the gate could not identify at all.

    Its own text rather than an arm in `question_reason`, because the arms
    each name a mark that is missing in a repository the gate resolved. This
    one has no repository to name. Saying "no review is recorded in " and
    then nothing would be the same silence one layer up.

    The first way on is not a marker. It is making the target readable, which
    is what lets the gate reach a verdict at all — so it leads the options,
    and the waiver is second.

    **What "readable" means differs, and offering the wrong one leaves no way
    on at all.** For a value the shell would have expanded, writing the path
    out replaces it and the gate can then judge. For a CONSTRUCT the reader
    cannot follow there is no value to replace: the directory named is the
    last one the reader could name, usually the session's own, and telling the
    user to write it out is an instruction that changes nothing. Both arms
    then collapse onto the waiver, which is the standing exemption this gate
    exists to avoid. `cmdline.Unresolved.why` is what tells them apart.

    `paths` holds the targets themselves rather than their text, for that
    reason.
    """
    # Counted and listed by PATH, judged by reason. The two are different
    # questions: one command can reach one directory twice, once because a
    # value could not be expanded and once because a construct could not be
    # read, and announcing that as "2 directories" naming the same path twice
    # is the reader's bookkeeping leaking into the prompt. Which arm it gets
    # still has to see BOTH, because the construct wording says nothing about
    # writing a path out and cannot speak for the value half.
    seen, unique = set(), []
    for p in paths:
        if str(p) not in seen:
            seen.add(str(p))
            unique.append(p)
    listed = ", ".join(str(p) for p in unique)
    count = "a directory" if len(unique) == 1 else f"{len(unique)} directories"
    construct = all(getattr(p, "why", None) == Unresolved.CONSTRUCT for p in paths)
    state = UNREADABLE_CONSTRUCT if construct else UNREADABLE_STATE
    lines = [state.format(count=count, listed=listed), ""]
    if first:
        # Built as a list so the header can COUNT it. This prompt renders its
        # own options rather than going through `question_reason`, and it kept
        # a hand-written `two` after the other site learned to count -- one
        # number in step and one not, which is the same defect wearing the
        # right value.
        options = [
            '    1. "Say where it commits" — re-issue the commit outside the '
            "construct the gate could not read, as `cd <absolute path> && git "
            "commit …` or `git -C <absolute path> commit …`. Whatever the "
            "surrounding command does, the gate has to see the directory to "
            "judge the repository at all."
            if construct
            else '    1. "Write the path out" — re-issue the command with the '
            "absolute path in place of the unresolved value. That is the only "
            "way this commit gets a verdict at all, and it is what the gate "
            "needs to tell a scratch repository from the one being worked on.",
            '    2. "Commit without a review" — re-issue the command with the '
            "waiver in front of it, exactly like this, quotes included: "
            "`: '[no-review]'; git commit …`. Written after `git commit` the "
            "marker is a pathspec and git rejects the command. The waiver "
            "then stays in the command, where a reader can point at it.",
        ]
        lines.append(offer_header(len(options)))
        lines.append("")
        lines.append("  This commit's target repository could not be read. Which way?")
        lines.extend(options)
        lines.append("")
        lines.append(
            "Then do what they picked, and do not re-issue this commit before "
            "they answer. A retry reaches the ordinary approval prompt "
            "instead, where approving is the waiver."
        )
    else:
        lines.append(
            "Approving is the waiver — the commit proceeds, and no repository "
            "was checked.\nDeclining cancels the commit and leaves the tree "
            "as it is. Two ways on from there: re-issue it so the commit "
            "names an absolute directory of its own, which is what lets the "
            "gate judge the repository at all, or re-issue it with the "
            "waiver in front — "
            "`: '[no-review]'; git commit …` — when the work was never headed "
            "for a review."
        )
    if also_stopped:
        noun = "repository" if also_stopped == 1 else "repositories"
        lines.append("")
        lines.append(
            f"This command also commits into {also_stopped} further {noun} "
            "that the gate did read and stopped for the ordinary reason. "
            "Settling this one and retrying meets them."
        )
    return "\n".join(lines)


def also_pending(others, decision):
    """One line naming the repositories this command ALSO gets stopped for.

    What it means depends on which decision carries it, and the two are
    opposites. A `deny` cancels the command, so the user settles one
    repository and meets the next on the retry — without the line, that second
    stop reads as the first answer not having worked. An `ask` approves the
    command WHOLE: measured, both commits land and the further repositories
    are never asked about at all.

    Saying "the retry meets the next" on the `ask` path would promise a
    question that never comes, about the repositories least likely to be
    looked at. Closing the hole with budget instead would cost a round trip
    per repository on every such command, and prompt volume is what this whole
    change exists to bring down.
    """
    listed = ", ".join(others)
    noun = "repository" if len(others) == 1 else "repositories"
    tail = (
        "One decision settles one repository, so the retry meets the next."
        if decision == "deny"
        else "Approving runs the command whole, so it waives those too and "
        "they are never asked about separately."
    )
    return (
        f"\n\nThis command also commits into {len(others)} further {noun}, "
        f"stopped here for the same reason: {listed}. {tail}"
    )


def decide(decision, reason):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def declaration_hint(top):
    """The declaration path the review arm's stop text tells a session to write.

    Under the root this repository resolves to, and relative to it. In local
    mode (#80) that root is under the git directory, and the literal
    `seal/specs/…` named a file the gate never reads; from a linked worktree
    the path climbs out of the tree, which is still the one to type. Joined
    the way the platform spells it, for the reason `implementer-notice.py`
    gives.

    On Windows a linked worktree on another drive than the main tree has no
    relative spelling at all — `ntpath.relpath` raises `ValueError` — and the
    absolute path is the one to type. Left unguarded, that exception left
    `main()`, `dispatch.py` swallowed it, and empty stdout was an allow for a
    commit the gate never judged (round 1 of #80, 🔴 1).
    """
    home = optin.home_at(top)
    if not home:
        return f"{routing.WORK_ITEMS}/<work-item-id>/{routing.FILENAME}"
    try:
        rel = os.path.relpath(home, top)
    except ValueError:
        rel = home
    return os.path.join(rel, optin.WORK_ITEMS, "<work-item-id>", routing.FILENAME)


def judge(cwd, top, command, invocations, clean):
    """The marks this commit is missing in ONE repository, and that repo's git-dir.

    `top` is that repository's root, resolved by the caller — "" when `cwd` is
    no repository at all, including a `-C` path that does not exist, where
    `git` returns "" rather than raising. Returning ([], "") there is the
    direction this gate has always failed in. `optin` states the same rule one
    layer down (its own docstring: everything there fails toward "not opted
    in", and it resolves the root through this same `rev-parse`), so no
    decision rests on the early return alone — it is the cheap exit, not the
    guarantee.

    Every arm names `top`. The verdict used to be about the session's cwd
    always, so "hand it to the review chain" meant one repository and needed no
    address. Now the commit can land elsewhere, and a review run where the
    session happens to sit writes its mark in the wrong repository — the gate
    keeps stopping the commit, the budget runs out, and the real target ships
    unreviewed on an approval click.
    """
    if not top:
        return [], ""

    head = git(["rev-parse", "--verify", "--quiet", "HEAD"], cwd)
    git_dir = git(["rev-parse", "--git-dir"], cwd)

    # Two independent opt-ins. A repo can declare either, both, or neither,
    # so each is checked on its own rather than nested behind the other.
    missing = []

    # A declaration is the answer this gate used to have to guess at. Where one
    # is in force the arm stays silent, for EITHER way on: the routing question
    # was answered before the first edit, and asking for `[no-review]` as well
    # would be asking for the same answer twice. What each answer costs is
    # checked at the pull request, by CI, where nobody has to be sitting.
    #
    # Both this and `[no-review]` silence the arm, and they are independent.
    # The token still waives one command for a commit that belongs to no work
    # item; the declaration routes a work item.
    routed = routing.declared(cwd, top)

    if optin.opted_in(cwd) and not has_marker(command, "[no-review]") and not routed:
        if not head or read_mark(cwd, git_dir, "specseal-reviewed") != head:
            # Built here, inside the arm that stands, and nowhere earlier:
            # it costs one more `git` in a linked worktree, and building it
            # before the judgment put a `relpath` that can raise in front of
            # every commit (round 1 of #80, 🔴 1 and 🟢 6).
            declaration = declaration_hint(top)
            missing.append(
                {
                    "marker": "[no-review]",
                    "way_on": f"run the review chain against {top}",
                    # The way out that is neither the mark nor the waiver, and
                    # the only one that fits a work item just starting. It is
                    # carried on the arm rather than written into `ask_reason`
                    # because the parity arm has no equivalent -- nothing
                    # declares a comparison in advance the way routing is
                    # declared before the first edit.
                    "also": (
                        "There is a third way out of the REVIEW arm when this "
                        "commit belongs to a work item: write "
                        f"`{declaration}` naming this "
                        "branch, in a command of its own, then re-issue the "
                        "commit. The declaration is read from the working "
                        "tree, so it silences the review arm for the very "
                        "commit that adds it, and the answer it records — the "
                        "user's answer, not yours — is checked at the pull "
                        "request instead. It silences NOTHING ELSE, so any "
                        "other arm named above still has to be answered on "
                        "its own and the commit does not go through until it "
                        "is. The separate command matters: this gate denies "
                        "the whole call, so a write batched with the commit "
                        "never runs."
                    ),
                    "state": (
                        f"No review is recorded for this cycle in {top} — the "
                        "repository this commit lands in (the code-review "
                        "skill writes the reviewed HEAD to that repository's "
                        ".git/specseal-reviewed)."
                    ),
                    "question": (
                        "This commit closes a cycle nothing reviewed. Which way?"
                    ),
                    "options": (
                        (
                            '1. "Declare the routing"',
                            "this commit belongs to a work item whose "
                            f"`{declaration}` is not "
                            "written "
                            "yet. Write it from `templates/sdd-routing.md`, "
                            "naming THIS branch, IN A COMMAND OF ITS OWN, and "
                            "then re-issue the commit unchanged. The Review "
                            "row is the USER'S answer and not yours: put both "
                            "spellings — `through the review chain` and "
                            "`straight to the PR` — to them before writing "
                            "the file. `straight to the PR` is the one CI "
                            "requires nothing for, and it silences this arm "
                            "for every later commit on this branch, so "
                            "writing it yourself is the waiver below taken "
                            "without the word that records it — and this way "
                            "leaves no word in the command at all. The "
                            "declaration is read from the WORKING TREE, so it "
                            "silences this arm for the very commit that adds "
                            "it — there is nothing to wait for and no waiver "
                            "to spend. It is not a way past review: the answer "
                            "written in it is what CI checks at the pull "
                            "request, and `through the review chain` still "
                            "requires a round record there. The separate "
                            "command is not a style note — this gate runs "
                            "before the shell does and denies the WHOLE call, "
                            "so a write batched with the commit never happens "
                            "and the declaration this option is about is the "
                            "file that was lost.",
                        ),
                        (
                            '2. "Review it first"',
                            "hand the change to the review chain — "
                            "@agent-specseal:warden, or /specseal:code-review "
                            f"— run AGAINST {top}. That is where this commit "
                            "lands and where the mark has to be written, and "
                            "it is not necessarily the repository this session "
                            "is sitting in. The mark is what silences this "
                            "gate, so the same commit then goes through "
                            "untouched.",
                        ),
                        (
                            '3. "Commit without a review"',
                            "re-issue the command with the waiver in front of "
                            "it, exactly like this, quotes included: "
                            "`: '[no-review]'; git commit …`. Written after "
                            "`git commit` the marker is a pathspec and git "
                            "rejects the command; an interactive zsh refuses "
                            "it earlier still, as an unmatched glob. The `:` "
                            "is a no-op that carries the word into the command "
                            "without handing it to git, so the waiver stays "
                            "visible in shell history. It must be outside the "
                            "commit message, where it waives the gate instead "
                            "of describing one.",
                        ),
                    ),
                }
            )

    if (
        optin.parity_config(cwd)
        and not has_marker(command, "[no-parity]")
        and touches_code(cwd, invocations)
    ):
        if not head or read_mark(cwd, git_dir, "specseal-parity") != head:
            missing.append(
                {
                    "marker": "[no-parity]",
                    "way_on": f"compare {top} against the original",
                    "state": (
                        f"{top} — the repository this commit lands in — "
                        "declares a migration config, so behavior there is "
                        "ported and the original decides where policy is "
                        "silent. Nothing records that the original was "
                        "consulted for this change (the legacy-parity skill "
                        "writes the compared HEAD to that repository's "
                        ".git/specseal-parity)."
                    ),
                    "question": (
                        "Nothing records that the original was consulted for "
                        "this change. Which way?"
                    ),
                    "options": (
                        (
                            '1. "Compare against the original"',
                            "run the legacy-parity skill against the baseline "
                            f"in {top}'s migration config, and against that "
                            "repository — not necessarily the one this session "
                            "is sitting in. The mark that comparison writes is "
                            "what silences this gate.",
                        ),
                        (
                            '2. "Commit without comparing"',
                            "re-issue the command with the waiver in front of "
                            "it, exactly like this, quotes included: "
                            "`: '[no-parity]'; git commit …`. Written after "
                            "`git commit` the marker is a pathspec and git "
                            "rejects the command. It must be outside the "
                            "commit message.",
                        ),
                    ),
                }
            )

    return missing, git_dir


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("tool_name") != "Bash":
        return
    command = (payload.get("tool_input") or {}).get("command", "")
    cwd = payload.get("cwd", "")
    invocations, clean = commit_invocations(command, cwd)
    if not invocations and not (not clean and "git" in command and "commit" in command):
        return

    # Every target is judged, not just the first to fire. The decision is
    # about one of them — a hook returns one — but the rest are what the
    # retry will meet, and the prompt says so rather than letting the second
    # stop look like the first answer having failed.
    roots = {}

    def root_of(path):
        """The repository root for a directory, memoised — "" when there is none."""
        if path not in roots:
            # `optin.repo_root`, not a `rev-parse` of its own. Two resolvers
            # for one question is what the RIDER in that module counts as
            # cost; what it also bought was two SPELLINGS. git answers with
            # forward slashes on every platform, so on Windows this root was
            # printed to the user as `C:/proj` while `commit_targets`
            # grouped by it and `judge` joined onto it with `os.sep` -- and
            # the address in the prompt is the one thing the user has to
            # recognise as their own repository.
            roots[path] = optin.repo_root(path)
        return roots[path]

    # A target the command NAMED and the gate could not resolve is not a
    # repository that came back clean — it is a repository the gate never
    # looked at. Those two produced the same nothing, and the
    # second is the one that ships an unreviewed commit.
    def names_a_directory(where, group):
        """True when the COMMAND said where this commit lands.

        A `-C` says it, and so does a `cd` in front of the commit — the whole
        point of reading one. Without the second half, `cd sub && git commit`
        where `sub` is no repository fell through to the early return in
        `judge` and went SILENT, which is the same fail-open as that defect
        wearing different clothes: a repository the gate never saw, reported
        as one it checked and found clean.

        The session's own directory used as a fallback is not the command
        naming anything, and a `cd` that lands back where it started (`cd x &&
        cd -`) has named the session's own repository, which is the same thing.
        """
        if isinstance(where, Unresolved):
            return True
        return any(
            inv.chdirs or (inv.base is not None and inv.base != cwd) for inv in group
        )

    stopped, unreadable = [], []
    for where, group in commit_targets(cwd, invocations, root_of):
        if names_a_directory(where, group) and (
            isinstance(where, Unresolved) or not root_of(where)
        ):
            # The target itself, not its text: `unreadable_reason` reads
            # `why` off it to pick which way out it can honestly offer.
            unreadable.append(where if isinstance(where, Unresolved) else str(where))
            continue
        missing, git_dir = judge(where, root_of(where), command, group, clean)
        if missing:
            stopped.append((where, git_dir, root_of(where), missing))

    session = payload.get("session_id")

    # Standing to speak comes from the session's own repository, not from the
    # target: the target is exactly what could not be read. It decides WHETHER
    # this globally installed plugin says anything here, never WHAT is true of
    # the repository the commit lands in — judging an unknown target against
    # the session's marks would answer for a repository it may never touch.
    if unreadable and optin.opted_in(cwd) and not has_marker(command, "[no-review]"):
        here = git(["rev-parse", "--git-dir"], cwd)
        first = bool(session) and not already_asked(cwd, here, session)
        decide(
            "deny" if first else "ask",
            unreadable_reason(unreadable, first, len(stopped)),
        )
        return

    if not stopped:
        return

    target, git_dir, _, missing = stopped[0]
    # Repository roots, not the directories named: the arms address a
    # repository and the announcement has to address the same thing.
    others = [top for _, _, top, _ in stopped[1:]]

    # No session id means no way to record that the question was asked, so a
    # deny would repeat forever. `ask` cannot loop: approving is the way out.
    # The budget is per repository, like the verdict it spends — answering for
    # one repository does not answer for the next.
    if session and not already_asked(target, git_dir, session):
        decision, reason = "deny", question_reason(missing)
    else:
        decision, reason = "ask", ask_reason(missing)
    decide(decision, reason + (also_pending(others, decision) if others else ""))


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    console.to_utf8()
    main()
