#!/usr/bin/env python3
"""The root this plugin maintains: where it lives, and how a copy travels.

Three subcommands over one directory. `mode` says which of the two places
the root is at and moves it between them; `export` and `import` carry a copy
of it to another clone.

In local mode the ledger and the work-item records live under the common git
directory, so a new machine or a re-clone starts with nothing and CI's checks
cannot run. That is the mode's whole trade-off
(`docs/one-root-by-lifetime.md`, "Shared or local"), and without a way to
carry a copy it reads as *lose it* rather than *take a copy*. This is that
way:

  seal export                 write the root to a zip beside the clone
  seal export --check         the release reminder; writes nothing
  seal import <zip>           merge a zip's records in, overwriting nothing

Switching between the two modes was two shell lines in `README.md` that a
person had to find, and a repository arriving from the 0.3.x layout was
never asked which mode it wanted (#104). `seal mode` is that section made
runnable, and the section on the mode below this one is its reasoning:

  seal mode                   the folder, the row, and whether they agree
  seal mode --check           the same, writing nothing; exit 1 when they
                              disagree. This is what CI runs
  seal mode local|shared      switch, and write the row
  seal mode --apply           switch to whatever the row says

**The root is its own directory, and that is what makes the export safe.**
Beside it under the git directory sit the smith mark, the worktree choices,
the review and parity marks, the throwaway opt-out, any lease file and this
command's own state. None of that belongs to another machine, and none of it
is in the zip — not because a list is maintained here, but because the export
walks the root and nothing else. A symbolic link inside the root is the one
way back out, so links are skipped and named rather than followed.

**A zip is untrusted input**, and `ZipFile.extractall` is not used on it.
What that buys is narrower than the usual telling, so it is written down
measured rather than repeated: on the CPython this ships on (3.12 to 3.14,
checked 2026-09-03) `extractall` already strips `..` and a leading `/` from a
member's name, and writes a link entry as an ordinary file. It is **not** a
path-traversal sink there.

What actually disqualifies it, in order:

  1. **it overwrites**, which is the one rule this command exists to keep;
  2. it writes members this format has no place for — a name like
     `a\\..\\..\\b.md` lands in the root as a literal file on POSIX;
  3. it follows a symbolic link that is already a directory in the
     destination, and so would a plain `open()`. That one is real and is
     checked for by `linked_path` below.

So every member's name is checked first, one bad member refuses the whole
archive before a byte is written, and each file is written at a path built
from segments this module produced. The name checks are defence that does not
depend on the standard library's sanitiser staying what it is today.

**Import never overwrites and never asks.** A path that is not there is
added. A path that is there with the same bytes is left alone. A path that is
there with different bytes gets the incoming copy beside it as
`<name>.incoming<ext>` — `ledger/<id>.incoming.md` beside
`ledger/<id>.md` — and the collision is reported. A copy is not a sync: which
of the two files is right is a judgement the person makes by reading them,
and there is no answer this command could give that would not sometimes throw
work away.

**What the reminder counts, and what it does not.** `--check` prints
`N work items changed since the last export`, where a work item is
`specs/<id>/` together with `ledger/<id>.md`. Root-level files — `ledger.md`,
`follow-up.md`, `config.md`, `parity.md` — are NOT counted, because the line
the design specifies says *work items* and this command does not get to widen
it. So a release whose only change was to `follow-up.md` reports 0. That gap
is Q1 in the work item's `questions.md`, with the owner named; it is written
here as well because this docstring is where the next reader meets the count.

Exit codes: 0 done · 1 nothing was written, and the message says why. There
is no third one; every refusal here names the file, the path, or the flag
that gets past it.
"""

import argparse
import datetime
import errno
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hooks"),
)
import optin

# The manifest's shape. An import refuses a number it does not know rather
# than guessing at fields: a zip whose fields moved, read by a build that
# assumes the old ones, merges records at the wrong paths — and that merge is
# the operation this command exists to make safe.
FORMAT = 1
MANIFEST = "manifest.json"

# Machine-local state, beside the root with everything else that must never
# leave this clone. Inside the root it would ride into the next zip and, in
# shared mode, into a commit.
STATE = "specseal-last-export.json"

# The root's sub-directory holding one file per work item in development.
# `optin.WORK_ITEMS` is the other half of the pair; there is no constant for
# this one because no hook opens it.
LEDGER_DIR = "ledger"

UNSAFE_IN_A_NAME = re.compile(r"[^A-Za-z0-9._-]")
DRIVE = re.compile(r"^[A-Za-z]:")

ADDED, IDENTICAL, COLLIDED = "added", "identical", "collided"

# A record is markdown, and `write_members` reads each member whole. The zip
# arrives from another machine, so its declared sizes are the sender's choice
# rather than this root's honest contents: measured 2026-09-03, a 408 KB zip
# declaring 400 MB in one member wrote 419 MB and added as much to memory in
# 0.2 s. All three limits are read before a byte is written.
MEMBER_LIMIT = 32 * 1024 * 1024
ARCHIVE_LIMIT = 512 * 1024 * 1024
# The other axis. A member declaring zero bytes passes the member limit and
# adds nothing to the total, so neither byte bound sees a zip that is only a
# count: measured 2026-09-03, a 31 MB zip of 300,000 empty members wrote
# 300,002 files into the root at exit 0, in 34.5 s. A root of records is one
# directory per work item and one ledger fragment each.
MEMBER_COUNT_LIMIT = 20_000


# --- git, asked the way `hooks/optin.py` asks it ----------------------------


def git(root, *args):
    """`git -C root <args>` stdout, stripped, or "" for any failure.

    Encoding named for the reason `optin.repo_root` names it: `text=True`
    alone decodes with the parent's locale, git answers UTF-8, and a
    repository under a path this locale cannot decode kills subprocess's
    reader thread without the exception propagating.
    """
    try:
        done = subprocess.run(
            ["git", "-C", root, *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    # The return code, not the output alone. `git rev-parse HEAD` on a branch
    # with no commit yet exits 128 and still prints `HEAD`, which the manifest
    # would record as this export's SHA (measured 2026-09-03).
    if done.returncode != 0:
        return ""
    return (done.stdout or "").strip()


def normalise_remote(url):
    """A remote URL reduced to host and path, so two spellings of one
    repository compare equal.

    `git@example.com:org/repo.git` and `https://example.com/org/repo` are one
    repository, and ssh at one machine with https at another is the ordinary
    case — comparing the strings would refuse every real import.

    The scheme goes, a `user@` prefix goes, the scp-style `host:path` colon
    becomes `/` **only where there was no scheme** (so the port in
    `https://example.com:8443/x` is left alone), a trailing `.git` and `/` go,
    and the result is lowercased.

    Wrong in the accepting direction would need two different repositories to
    reduce to the same host and path, which is the same repository. Wrong in
    the refusing direction costs a message naming `--allow-other-repo`. That
    asymmetry is why this is done at all.

    Anything that is not text reduces to "", because one caller passes a field
    out of a manifest another machine wrote. `read_manifest` checks that the
    manifest is an object and that its `format` is one this build reads; every
    other field is whatever the zip says, and a list here used to reach the
    console as an `AttributeError`.
    """
    if not isinstance(url, str):
        return ""
    text = url.strip()
    if not text:
        return ""
    schemed = "://" in text
    if schemed:
        text = text.split("://", 1)[1]
    authority = text.split("/", 1)[0]
    if "@" in authority:
        text = text.split("@", 1)[1]
    if not schemed and ":" in text:
        text = text.replace(":", "/", 1)
    text = text.rstrip("/")
    if text.endswith(".git"):
        text = text[: -len(".git")]
    return text.lower()


# --- the root, and the one walk everything reads it through -----------------


def resolve(cwd):
    """(repository root, root in force, shared path, local path, mode).

    Every path comes from `optin`: `home_at` says which root is in force and
    `home_paths` says where each mode's root would be, so nothing here spells
    `<repo>/seal` or `.git/seal` for itself.
    """
    repo = optin.repo_root(cwd)
    if not repo:
        return "", "", "", "", ""
    shared, local = optin.home_paths(repo)
    home = optin.home_at(repo)
    mode = "shared" if home and home == shared else "local" if home else ""
    return repo, home, shared, local, mode


def root_files(home):
    """([(relative path, disk path)], [skipped link]) for the whole root.

    Relative paths are `/`-joined on every platform, because they go into a
    zip that another machine reads. Both lists are sorted, so the same tree
    always produces the same zip and the same digest.

    **This is the only walk.** The zip's members and the digests the manifest
    records come from this one list, and `test_the_records_can_be_carried_out_
    and_in.py` asserts the zip's namelist against it. Two enumerations would
    drift at the seam — the manifest recording what one of them saw while the
    reminder compares against what the other sees — and the difference would
    read as a work item somebody changed.

    Symbolic links are excluded here rather than at the zip, so they are
    absent from the members and from the digest together. Excluding them in
    one place only would make every export of a repository holding one report
    a change that nothing made. `os.walk` does not descend into a linked
    directory by default; it is pruned as well so the exclusion is a decision
    in this function rather than a default somewhere else.
    """
    files, links = [], []

    def relative(path):
        return os.path.relpath(path, home).replace(os.sep, "/")

    for dirpath, dirnames, filenames in os.walk(home):
        linked = [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]
        for name in linked:
            links.append(relative(os.path.join(dirpath, name)) + "/")
        dirnames[:] = sorted(d for d in dirnames if d not in linked)
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                links.append(relative(path))
            else:
                files.append((relative(path), path))
    return sorted(files), sorted(links)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def digest(entries):
    """SHA-256 over a sorted [(relative path, disk path)].

    The path, a NUL, the byte length, a NUL, the bytes — so a file renamed to
    another file's name, or two files whose contents swap, change the digest.
    Hashing the concatenated contents alone would not.
    """
    running = hashlib.sha256()
    for rel, path in entries:
        data = read_bytes(path)
        running.update(rel.encode("utf-8"))
        running.update(b"\0")
        running.update(str(len(data)).encode("ascii"))
        running.update(b"\0")
        running.update(data)
    return running.hexdigest()


def work_item_of(rel):
    """The work item a root-relative path belongs to, or "".

    One work item writes in two places: its directory under `specs/` and its
    ledger fragment under `ledger/`. Both count as the same item, so a release
    that only wrote evidence rows is still a work item that changed.
    """
    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == optin.WORK_ITEMS:
        return parts[1]
    if len(parts) == 2 and parts[0] == LEDGER_DIR and parts[1].endswith(".md"):
        return parts[1][: -len(".md")]
    return ""


def work_item_digests(files):
    """{work item id: digest}, built from the list the zip is built from."""
    groups = {}
    for rel, path in files:
        item = work_item_of(rel)
        if item:
            groups.setdefault(item, []).append((rel, path))
    return {item: digest(sorted(entries)) for item, entries in groups.items()}


# --- export -----------------------------------------------------------------


def manifest_of(repo, mode, files):
    return {
        "format": FORMAT,
        "mode": mode,
        "remote": git(repo, "config", "--get", "remote.origin.url"),
        "head": git(repo, "rev-parse", "HEAD"),
        "exported_at": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "items": work_item_digests(files),
    }


def unused(directory, stem, suffix):
    """`<stem><suffix>`, then `<stem>-2<suffix>`, … — the first free path.

    The zip's name goes through this. (`place` has its own chain for the
    `.incoming` siblings, because it also compares bytes — this docstring used
    to claim both went through here, and a fix to one therefore missed the
    other.) The cap is a refusal to spin rather than a limit anyone should
    reach.

    `lexists`, for the reason `place` uses it: a symbolic link to nothing
    reads as absent to `exists`, so this returned a name somebody had made a
    link, and `os.replace` then removed it.
    """
    for n in range(1, 1000):
        tail = suffix if n == 1 else f"-{n}{suffix}"
        path = os.path.join(directory, stem + tail)
        if not os.path.lexists(path):
            return path
    return ""


def zip_stem(repo, when):
    """`seal-<repo>-<date>` — the name a person recognises on a USB stick."""
    base = UNSAFE_IN_A_NAME.sub("-", os.path.basename(repo.rstrip(os.sep))) or "repo"
    return f"seal-{base}-{when}"


def write_zip(path, home, files, manifest):
    """The zip, written to a temporary name and renamed once it is complete.

    A failed write leaves no half archive for someone to carry away and
    discover on the machine that has nothing else.

    `lexists` and then `O_EXCL`, in that order and for two different reasons.
    This name is predictable — `seal-<repo>-<date>.zip.partial`, beside the
    clone, which is where the default export writes — and a broken link
    planted there put the manifest and every record outside the clone at exit
    0, printing `wrote <path>` for a path that was the link (measured
    2026-09-03).

    `lexists` is the check: a link to nothing reads as absent to `exists`, so
    only the l-form sees it. `O_EXCL` is the backstop for the moment between
    the check and the open — **on POSIX**, where the kernel refuses to satisfy
    it through a symbolic link. It does not carry that meaning on Windows:
    CI's windows leg wrote the manifest and every record through a broken link
    at this name, at exit 0, with `O_EXCL` set and nothing else in front of it
    (run 33715420379, 2026-09-03). Seven review rounds and the broad gate all
    ran on macOS and none of them could see it.

    So the check is the defence on every platform and the flag narrows the
    race on one. The race stays open on Windows, recorded rather than closed:
    there is no portable open that refuses a reparse point.
    """
    partial = path + ".partial"
    # The check and the open sit OUTSIDE the try. A name this call did not
    # create is not this call's to remove, and the cleanup below exists so a
    # failed write leaves no half archive — a `.partial` that was already
    # there is not one. Round 3 graded `os.replace` removing a link at the
    # zip's own name; this was that same removal one name over, and it took a
    # concurrent export's in-flight temporary file too.
    if os.path.lexists(partial):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), partial)
    opened = os.open(partial, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o666)
    try:
        with (
            os.fdopen(opened, "w+b") as raw,
            zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as archive,
        ):
            archive.writestr(MANIFEST, json.dumps(manifest, indent=2, sort_keys=True))
            for rel, disk in files:
                archive.write(disk, f"{optin.HOME}/{rel}")
        os.replace(partial, path)
    except BaseException:
        try:
            os.remove(partial)
        except OSError:
            pass
        raise


def export(args, cwd):
    repo, home, shared, local, mode = resolve(cwd)
    if not home:
        return no_root(repo, shared, local)

    if mode == "shared":
        print(
            f"shared mode: the records are committed at {display(repo, shared)}/, "
            "so every clone and CI already have them."
        )
        print(
            "A zip would be a second copy of what git carries, and nothing "
            "would keep it current — so none was written."
        )
        print(
            "\nTo switch this repository to local mode, from the repository "
            "root:\n"
            '  git rm -r --cached "$(git rev-parse --show-toplevel)/seal"\n'
            '  mv "$(git rev-parse --show-toplevel)/seal" '
            '"$(git rev-parse --git-common-dir)/seal"\n'
            "then commit the removal."
        )
        return 1

    files, links = root_files(home)
    when = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    stem = zip_stem(repo, when)

    if args.output:
        target = os.path.abspath(args.output)
        if os.path.isdir(target):
            target = unused(target, stem, ".zip")
        directory = os.path.dirname(target) or "."
        if inside(repo, target):
            print(
                f"note: {target} is inside the working tree, so `git add -A` "
                "can commit it — which is what local mode keeps the records "
                "out of the tree to avoid."
            )
    else:
        # Beside the clone, never in it. The normal place to run this is the
        # repository root, and an untracked zip there is one `git add -A` away
        # from committing the records local mode exists to keep out of the tree.
        directory = os.path.dirname(repo.rstrip(os.sep)) or "."
        target = unused(directory, stem, ".zip")

    if not target:
        print(f"no free name for {stem}*.zip in {directory} — pass --output")
        return 1
    if not os.path.isdir(directory):
        print(f"{directory} is not a directory — pass --output somewhere that is")
        return 1

    manifest = manifest_of(repo, mode, files)
    try:
        write_zip(target, home, files, manifest)
    except OSError as exc:
        print(f"the zip could not be written to {target}: {exc}")
        return 1

    write_state(repo, manifest)
    print(f"wrote {target}")
    print(
        f"  {plural(len(files), 'file')} from {display(repo, home)}, "
        f"{plural(len(manifest['items']), 'work item')}"
    )
    for rel in links:
        print(
            f"  skipped the symbolic link {optin.HOME}/{rel} — links are not followed"
        )
    print(
        f"\nTake it in on the other machine with:\n  seal import {os.path.basename(target)}"
    )
    return 0


# --- shared plumbing --------------------------------------------------------


def plural(count, noun):
    """`1 file` · `2 files`.

    `check()` does NOT use this. Its line is quoted text — the design and the
    issue's done-when list both write `N work items changed since the last
    export` — so it stays that, and at N=1 it reads `1 work items`. Reading
    the quoted line as a template with a grammar rule attached is a change to
    an acceptance criterion, which is not this command's to make; the work
    item's `overview.md` records it where the owner can overturn it.
    """
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def display(repo, path):
    """A path as the reader recognises it: relative to the repository and
    `/`-joined where it is inside, absolute where it is not."""
    if not path:
        return ""
    if inside(repo, path):
        return os.path.relpath(path, repo).replace(os.sep, "/")
    return path


def inside(repo, path):
    """Whether `path` is inside the repository's working tree.

    `commonpath` rather than `startswith`, which reads `/repo-2/x` as being
    inside `/repo`. The git directory of a main worktree is inside the tree by
    this test, and that is correct: nothing here asks the question about it.
    """
    try:
        return os.path.commonpath(
            [os.path.abspath(repo), os.path.abspath(path)]
        ) == os.path.abspath(repo)
    except ValueError:  # different drives on Windows
        return False


def no_root(repo, shared, local):
    if not repo:
        print("not inside a git repository — seal works on a clone")
        return 1
    if optin.git_common_dir(repo) and os.path.isfile(
        os.path.join(optin.git_common_dir(repo), optin.SCRATCH)
    ):
        print(
            f"this repository is marked throwaway "
            f"({optin.SCRATCH} under the common git directory), so every gate "
            "reads it as one that never opted in. Remove the marker to work "
            "with its records."
        )
        return 1
    # Not "nothing to carry": `seal mode` reaches this too, and it carries
    # nothing anywhere. What all three subcommands share is that the root is
    # what they work on, and it is looked for at exactly two places.
    print("no seal/ here, so there is nothing to work with. It is looked for at:")
    print(f"  {shared}   (shared mode)")
    print(f"  {local}   (local mode)")
    print(
        "\nThe first time the smith works in a repository it asks which one, "
        "and creates it."
    )
    return 1


def state_path(repo):
    common = optin.git_common_dir(repo)
    return os.path.join(common, STATE) if common else ""


def write_state(repo, manifest):
    """Record the manifest of this export, after the zip is on disk.

    Written even when `--output` sent the zip somewhere unusual: an export
    happened, and the reminder measures against the last one wherever it went.
    """
    path = state_path(repo)
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, sort_keys=True)
    except OSError:
        # The zip is written and the export succeeded. A reminder that cannot
        # remember costs one over-count at the next release; failing the
        # export here would cost the copy.
        pass


def read_state(repo):
    path = state_path(repo)
    if not path or not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


# --- import -----------------------------------------------------------------


def unsafe(info):
    """Why this zip member may not be written, or "" when it may.

    Checked before anything is written, and one bad member refuses the whole
    archive: a partial import from a hostile zip is still a decision the zip
    made, and the person is then holding records they believe are a copy and
    cannot say of what.

    Some of these `extractall` would also have handled — it strips `..` and a
    leading `/` on today's CPython (the module docstring measures it). They
    are checked here anyway, because a defence that holds only while a
    standard-library sanitiser keeps its current shape is not one this file
    can claim, and because a refusal says what happened where a silent
    sanitise leaves a name nobody chose.

    What is refused, and why each one:

      - a backslash anywhere. A zip stores `/`-separated names (APPNOTE
        4.4.17), so a `\\` is a literal character on POSIX and a separator on
        Windows. `a\\..\\..\\b` is inert on one platform and an escape on the
        other, and a name that means two things is refused on both;
      - an absolute name, or one starting with a drive letter;
      - any `..` segment, which is the escape itself;
      - a NUL, which truncates the path at the C boundary underneath. Kept
        as a guard rather than a claim: `zipfile` cuts the name at the NUL
        before this reads it (measured 2026-09-03), so such a member arrives
        under a shortened name inside the root rather than being refused;
      - a symbolic link entry. A link written into the root is a way to reach
        outside it on the NEXT export, which is the loop this closes;
      - anything not under `seal/` and not the manifest. A member this build
        has no place for is a zip it does not understand, and writing the
        parts it does understand is guessing.
    """
    name = info.filename
    if not name:
        return "a member with no name"
    if "\\" in name:
        return f"{name!r} holds a backslash, which is a separator on one platform only"
    if name.startswith("/") or DRIVE.match(name):
        return f"{name!r} is an absolute path"
    if "\0" in name:
        return f"{name!r} holds a NUL"
    parts = [p for p in name.split("/") if p]
    if any(p == ".." for p in parts):
        return f"{name!r} climbs out of the root with `..`"
    if (info.external_attr >> 16) & 0o170000 == 0o120000:
        return f"{name!r} is a symbolic link"
    if name == MANIFEST or name.rstrip("/") == MANIFEST:
        # The manifest is exempt from the NAME checks — it is the one member
        # that is not a record. Its size is checked in `import_`, which has to
        # know it before reading the manifest and therefore before this runs.
        return ""
    if not parts or parts[0] != optin.HOME:
        return f"{name!r} is not under {optin.HOME}/ and is not the manifest"
    if info.file_size > MEMBER_LIMIT:
        return (
            f"{name!r} declares {info.file_size} bytes, more than the "
            f"{MEMBER_LIMIT} one record may hold"
        )
    return ""


def linked_path(into, archive):
    """A path inside the root that is a symbolic link, or "".

    This is the way a member can still land outside the root, and it is
    measured rather than assumed. `extractall` on the CPython this ships on
    (3.12 to 3.14, checked 2026-09-03) strips `..` and a leading `/` from a
    member's name and writes a link entry as an ordinary file, so those are
    not what a member can escape through. A path in the DESTINATION that is a
    symbolic link is: `extractall` follows it, and so does the plain `open()`
    this module writes with. `seal/specs` pointed elsewhere puts every work
    item there.

    The leaf counts, not only the directories above it. A link named
    `ledger/w1.md` whose target does not exist reads as absent to
    `os.path.exists`, so `place` calls the member ADDED and `open(target,
    "wb")` follows the link and writes outside the root — measured
    2026-09-03, exit 0 with no warning. A link whose target does exist is
    caught by the byte comparison instead and lands as `.incoming`, which is
    why only the broken one leaked.

    So it is refused before anything is written, and the whole import is
    refused rather than the member: the link is this clone's own state, not
    the zip's, and a person who removes it gets a complete copy on the next
    run instead of a partial one now.

    A link this command created is not possible — the export skips links and
    an import refuses a link member — so reaching this means someone made one
    by hand, which is exactly when a stop is worth more than a guess.
    """
    seen = set()
    for info in archive.infolist():
        parts = [p for p in info.filename.split("/") if p][1:]
        for depth in range(1, len(parts) + 1):
            prefix = tuple(parts[:depth])
            if prefix in seen:
                continue
            seen.add(prefix)
            if os.path.islink(os.path.join(into, *prefix)):
                return "/".join(prefix)
    return ""


def blocked_path(into, archive):
    """A path a member needs as a directory that is already a file, or "".

    `write_members` calls `os.makedirs(exist_ok=True)`, which raises
    `FileExistsError` when the name exists and is not a directory — uncaught,
    mid-write, with the records before it already on disk. Measured
    2026-09-03: a zip holding `seal/a` and `seal/a/b.md` left two records
    written, lost the one after them, and printed a traceback with no line of
    this command's own.

    Both the zip's own members and what the root already holds, because the
    clash comes from either side. Refused whole, like every other refusal
    here, and for the same reason: a partial copy is the thing this command
    exists not to leave.
    """
    members = set()
    for info in archive.infolist():
        parts = [p for p in info.filename.split("/") if p][1:]
        if info.is_dir() or not parts:
            continue
        members.add(tuple(parts))
    for parts in sorted(members):
        for depth in range(1, len(parts)):
            prefix = tuple(parts[:depth])
            here = os.path.join(into, *prefix)
            # `isfile` is not the question `makedirs` answers. It is False for
            # a FIFO, a socket and a device node, and `makedirs(exist_ok=True)`
            # raises on all three — measured 2026-09-03, a FIFO at `seal/a`
            # left one record on disk and lost the rest. `lexists and not
            # isdir` is the condition `makedirs` itself checks.
            if prefix in members or (os.path.lexists(here) and not os.path.isdir(here)):
                return "/".join(prefix)
    return ""


def read_manifest(archive, path):
    """The manifest, or (None, message).

    Never raises for a manifest this command cannot make sense of. It can
    still raise for a manifest whose DATA does not read — a bad CRC leaves
    `archive.read` as `BadZipFile`, which is not one of the three this
    catches. `import_` runs `testzip` before reaching here for that reason.
    """
    try:
        raw = archive.read(MANIFEST)
    except KeyError:
        return None, (
            f"{path} holds no {MANIFEST} — it was not written by `seal export`"
        )
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return None, f"{path}'s {MANIFEST} could not be read: {exc}"
    if not isinstance(manifest, dict):
        return None, f"{path}'s {MANIFEST} is not an object"
    if manifest.get("format") != FORMAT:
        return None, (
            f"{path} is format {manifest.get('format')!r} and this build reads "
            f"format {FORMAT}. Reading it anyway would place records by fields "
            "that may have moved"
        )
    return manifest, ""


def place(destination, data):
    """(path to write, outcome) for one incoming file — never overwriting.

    `None` as the path means nothing to write. The candidates are the
    destination itself and then its `.incoming` siblings, in order, and the
    first one whose bytes already equal `data` ends the search: re-importing
    the same zip is then a run that writes nothing, rather than a second pile
    of `.incoming` copies of files that are already there.

    `lexists`, not `exists`. A candidate that is a symbolic link to nothing
    reads as absent to `exists`, and returning it would have the caller write
    THROUGH the link — round 2 measured a record leaving the root that way,
    at exit 0, reported as an ordinary collision. `lexists` calls such a name
    taken, `read_bytes` on it raises, and the copy moves to the next name.
    `linked_path` refuses the member's own name before any of this; the
    fallback names it never sees are what this covers.
    """
    if not os.path.lexists(destination):
        return destination, ADDED
    directory = os.path.dirname(destination)
    stem, ext = os.path.splitext(os.path.basename(destination))
    for n in range(0, 1000):
        candidate = (
            destination
            if n == 0
            else os.path.join(
                directory,
                f"{stem}.incoming{ext}" if n == 1 else f"{stem}.incoming-{n}{ext}",
            )
        )
        if not os.path.lexists(candidate):
            return candidate, COLLIDED
        try:
            if read_bytes(candidate) == data:
                return None, IDENTICAL
        except OSError:
            continue
    return None, COLLIDED


def destination_root(repo, home, shared, local, into):
    """(root to write into, message). Names it; `write_members` creates it.

    With no `--into`, the root in force wins; with none in force, local — the
    direction that puts nothing in the tree. Guessing shared would write this
    plugin's files into a repository that may be someone else's, which is the
    harm local mode exists to prevent, so the safe guess is the one made.

    Both roots present refuses whatever `--into` says, including nothing.
    The refusal used to sit inside the `--into` branch, which left the case
    the spec and both READMEs describe — `seal import` with no flag — writing
    into whichever root the gates happen to read first. A clone holding two
    roots is a clone whose owner has not said which is the real one, and a
    copy landing in one of them is not the moment to decide it.
    """
    if os.path.isdir(shared) and local and os.path.isdir(local):
        return "", (
            "both roots exist, and the gates read the first of them:\n"
            f"  {shared}   (shared mode — read first)\n"
            f"  {local}   (local mode)\n"
            "Importing into one would leave the other where nothing reads "
            "it. Move or remove one first; the plugin README's *Shared or "
            "local* section has both commands."
        )
    if into:
        wanted = shared if into == "shared" else local
        if not wanted:
            return "", "the common git directory could not be resolved"
        return wanted, ""
    if home:
        return home, ""
    if not local:
        return "", "the common git directory could not be resolved"
    return local, ""


def import_(args, cwd):
    repo, home, shared, local, _ = resolve(cwd)
    if not repo:
        print("not inside a git repository — seal works on a clone")
        return 1

    path = os.path.abspath(args.zip)
    if not os.path.isfile(path):
        print(f"{path} is not a file")
        return 1

    try:
        archive = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as exc:
        print(f"{path} is not a readable zip: {exc}")
        return 1

    with archive:
        # The order here is the fix for four separate measurements, and it is
        # the order itself rather than any one check: how big, then whether
        # the data reads, then the manifest, and only then the names. The
        # names go last because a later format is exactly what moves them.
        # `read_manifest` reads its member whole, so the bounds above it are
        # what keep that read affordable — and the member bound, which lives
        # in `unsafe`, is therefore read after the manifest rather than before.
        members = archive.infolist()
        if len(members) > MEMBER_COUNT_LIMIT:
            print(
                f"{path} holds {len(members)} members, more than the "
                f"{MEMBER_COUNT_LIMIT} this command will write."
            )
            print("\nNothing was written. A root this large is not a root of records.")
            return 1

        declared = sum(info.file_size for info in members)
        if declared > ARCHIVE_LIMIT:
            print(
                f"{path} declares {declared} bytes unpacked, more than the "
                f"{ARCHIVE_LIMIT} this command will read."
            )
            print("\nNothing was written. A root this large is not a root of records.")
            return 1

        # The manifest's own size, before it is read. It is exempt from the
        # name checks in `unsafe` and used to inherit the size exemption with
        # them, so a 400 MB one cost 400 MB of memory on its way to a verdict.
        fat = [
            info
            for info in members
            # `rstrip("/")`, matching the spelling `unsafe` exempts. The two
            # asked one question by different tests, so `manifest.json/`
            # passed the exemption there and the bound here.
            if info.filename.rstrip("/") == MANIFEST and info.file_size > MEMBER_LIMIT
        ]
        if fat:
            print(
                f"{path} declares {fat[0].file_size} bytes for {MANIFEST}, "
                f"more than the {MEMBER_LIMIT} a manifest may hold."
            )
            print("\nNothing was written. A root this large is not a root of records.")
            return 1

        # Every member's data, before the manifest is decoded and before the
        # first record is written. The manifest is a member too: a bad CRC on
        # it reached the console as a `BadZipFile` traceback, because
        # `read_manifest` ran first and its own `except` does not name that
        # type.
        #
        # `testzip` catches `BadZipFile` itself and answers with the member's
        # name, so that clause is a guard rather than a claim — it is the line
        # that would still be right if `testzip` stopped swallowing it. What
        # does leave `testzip` is an encrypted member (`RuntimeError`) and a
        # compression method this build has no decompressor for
        # (`NotImplementedError`), both measured 2026-09-03 as tracebacks.
        #
        # It reads every member, which the two bounds above are what make
        # affordable.
        try:
            corrupt = archive.testzip()
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as bad:
            corrupt = str(bad)
        if corrupt:
            print(f"{path} holds a member this command cannot read: {corrupt}")
            print(
                "\nNothing was written. A zip that cannot be read whole is "
                "not a copy of anything."
            )
            return 1

        manifest, why = read_manifest(archive, path)
        if not manifest:
            print(why)
            return 1

        # The names AFTER the format, because a later format is exactly what
        # moves the names this checks. Measured 2026-09-03: a zip declaring
        # format 2 with its records under `records/` answered "is not under
        # seal/", which reads as a malformed zip where the truth is a build
        # too old — and that field exists for no other day.
        refusals = [reason for info in members if (reason := unsafe(info))]
        if refusals:
            print(f"{path} holds members this command will not write:")
            for reason in refusals:
                print(f"  {reason}")
            print(
                "\nNothing was written. A zip carrying one of these is not a "
                "zip to take a partial copy from."
            )
            return 1

        here = normalise_remote(git(repo, "config", "--get", "remote.origin.url"))
        there = normalise_remote(manifest.get("remote"))
        if here and there and here != there and not args.allow_other_repo:
            print("this zip was exported from another repository:")
            print(f"  the zip says   {manifest.get('remote')}")
            print(
                f"  this clone is  {git(repo, 'config', '--get', 'remote.origin.url')}"
            )
            print(
                "\nNothing was written. Records are keyed by work-item id, so "
                "merging another project's would spread through the root with "
                "nothing to tell them apart afterwards.\n"
                "If the two are one repository under two spellings, pass "
                "--allow-other-repo."
            )
            return 1

        into, why = destination_root(repo, home, shared, local, args.into)
        if not into:
            print(why)
            return 1

        linked = linked_path(into, archive)
        if linked:
            print(
                f"{optin.HOME}/{linked} in this clone is a symbolic link, and "
                "writing through it would put records outside the root."
            )
            print(
                "\nNothing was written. Replace the link with a real "
                "file or directory and run this again."
            )
            return 1

        blocked = blocked_path(into, archive)
        if blocked:
            # Two sides, two remedies. The clash comes from this clone (move
            # the file) or from the zip alone (there is nothing here to move,
            # and the machine that exported it is who has to send another).
            # Measured 2026-09-03: the second answered with the first's words,
            # sending a person to rename a file they do not have.
            if os.path.lexists(os.path.join(into, *blocked.split("/"))):
                print(
                    f"{optin.HOME}/{blocked} in this clone is not a directory, "
                    "and this zip needs it as one."
                )
                print("\nNothing was written. Move or rename it and run this again.")
            else:
                print(
                    f"{path} names {optin.HOME}/{blocked} as a file and puts "
                    "members under it, which no filesystem can hold at once."
                )
                print(
                    "\nNothing was written. Ask the machine that exported it "
                    "for another zip."
                )
            return 1

        try:
            counts, collisions, refused = write_members(archive, into)
        except OSError as stopped:
            # Every refusal above happens before the first byte, and this is
            # the one failure that cannot: the filesystem can say no with
            # records already written — a directory in the root that is not
            # writable, a full disk. Measured 2026-09-03, both left a partial
            # copy and a traceback with no line of this command's own.
            print(f"the copy stopped part-way: {stopped}")
            print(
                "\nSome records were written and some were not. Fix what the "
                "line above names and run this again — this command "
                "overwrites nothing, so a second run finishes the copy and "
                "reports what was already here byte for byte."
            )
            return 1

    print(f"imported into {display(repo, into)}")
    print(f"  {plural(counts[ADDED], 'file')} added")
    print(f"  {plural(counts[IDENTICAL], 'file')} already here, byte for byte")
    print(
        f"  {plural(counts[COLLIDED], 'file')} landed beside an existing one"
        + (":" if collisions else "")
    )
    for existing, landed in collisions:
        print(f"    {existing}  ->  {landed}")
    for name in refused:
        print(f"  {name} was not written — its name was taken during the import")
    # Both fields read the way `remote` is read, and for the same reason: they
    # come from a manifest another machine wrote. `head` was guarded and
    # `exported_at` was not, so a manifest carrying one without the other
    # raised `KeyError` HERE — after every record was written, so the person
    # saw exit 1 and a traceback for a copy that had succeeded, and the two
    # lines below never printed.
    head = manifest.get("head")
    when = manifest.get("exported_at")
    if isinstance(head, str) and head:
        stamp = when if isinstance(when, str) and when else "an unrecorded time"
        print(f"\nExported at {stamp} from {head[:12]}.")
    print(
        "Which of a collided pair is right is a reading, not a merge — this "
        "command overwrites nothing.\n"
        "`evidence-check .` says which ledger rows drift against this tree."
    )
    return 0


def write_members(archive, into):
    """Write every `seal/…` member under `into`. Names are already checked.

    The path is rebuilt from segments rather than joined from the member's
    name, so nothing the archive wrote reaches the filesystem as a path.
    """
    counts = {ADDED: 0, IDENTICAL: 0, COLLIDED: 0}
    collisions, refused = [], []
    for info in archive.infolist():
        name = info.filename
        if info.is_dir() or name == MANIFEST:
            continue
        parts = [p for p in name.split("/") if p][1:]  # drop the `seal/` prefix
        if not parts:
            continue
        destination = os.path.join(into, *parts)
        data = archive.read(name)
        target, outcome = place(destination, data)
        if target is None:
            counts[outcome] += 1
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        # `place` has already turned every taken name down, so a target that
        # is taken by the time of this open is a name something else took in
        # between. `lexists` asks that question on every platform; `O_EXCL`
        # narrows the moment between the asking and the answering, and it
        # refuses to open THROUGH a symbolic link only on POSIX — CI's windows
        # leg wrote through a broken link with the flag set (run 33715420379,
        # 2026-09-03). Both answers are the same: do not write here.
        # Counted after the write, so the report never names a file that was
        # not written.
        try:
            if os.path.lexists(target):
                raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), target)
            opened = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
        except FileExistsError:
            # The name was free when `place` chose it and is taken now. Named
            # rather than skipped: a silent drop reads as a zip that held one
            # fewer record, which is the one thing this report must not say.
            refused.append("/".join(parts))
            continue
        with os.fdopen(opened, "wb") as handle:
            handle.write(data)
        counts[outcome] += 1
        if outcome == COLLIDED:
            collisions.append(
                (
                    "/".join(parts),
                    os.path.relpath(target, into).replace(os.sep, "/"),
                )
            )
    return counts, collisions, refused


# --- the mode: a row that is declared, and a folder that decides ------------
#
# `README.md`'s *Shared or local* section carried both directions as two shell
# lines — a `mv`, a commit, and the workflow file copied in or deleted by
# hand. They are correct, and a person who has not read that section has no
# way to arrive at them. This is that section made runnable, plus the four
# things a `mv` cannot do: refuse when the other root is already there, refuse
# when the tree is dirty under what it is about to stage, carry the workflow
# file, and write the row so the file and the folder agree afterwards.
#
# **Nothing at runtime reads the row.** Every hook resolves the root through
# `hooks/optin.py#home_at`, which reads `<repo>/seal/` then
# `<git-common-dir>/seal/`, and that stays the only signal. The row says what
# the repository WANTS; the folder's location says what it HAS. A gate that
# trusted the row would go looking in a place with no folder, and everything
# in `optin` is documented to fail toward "not opted in" rather than toward a
# guess (`docs/one-root-by-lifetime.md`, "The opt-in signal is the root
# itself").

CONFIG = "config.md"
ROW_ITEM = "Mode"

# The two modes, spelled the way every document in this repository spells
# them. Read case-insensitively, written lowercase.
LOCAL, SHARED = "local", "shared"
MODES = (LOCAL, SHARED)

# The workflow shared mode installs, as GIT spells a pathspec: forward
# slashes on every platform. `under()` turns it into a path for this
# filesystem. The two dialects live as separate strings rather than one
# string used for both, because a literal separator inside an
# `os.path.join` argument produces `C:/proj\.github/workflows` — a path in
# two dialects that equals nothing any caller built (`hooks/optin.py`
# carries the same reasoning about `repo_root`).
WORKFLOW = ".github/workflows/hygiene.yml"
# The row this command writes itself, spelled as git spells a pathspec —
# beside WORKFLOW and for the same reason.
CONFIG_PATHSPEC = f"{optin.HOME}/{CONFIG}"

# The line CI's own workflow uses to clone this plugin. A file at WORKFLOW
# carrying it is one this plugin wrote; a file that does not is somebody
# else's with our name, and the switch leaves it alone rather than deleting
# it. `tests/test_the_mode_is_a_row_and_a_command.py` asserts the template
# still contains this, so the marker cannot drift away from what it
# identifies.
PLUGIN_CLONE = "https://github.com/MichaelYcJo/SpecSeal.git"

# The version placeholder in `templates/hygiene.yml`. A workflow written with
# it still in place fails CI's `git clone --branch` on the first pull
# request, so a version that cannot be read writes no file at all.
PLACEHOLDER = "v<version>"

PLUGIN_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)

# The `| Item | Value |` table, read exactly as `templates/parity.md` and the
# pull-request-language row are read.
CONFIG_HEADER = re.compile(r"^\|\s*Item\s*\|\s*Value\s*\|\s*$")
CONFIG_ROW = re.compile(r"^\|\s*(?P<item>[^|]+?)\s*\|\s*(?P<value>[^|]*?)\s*\|\s*$")
CONFIG_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")

NEW_CONFIG = """# Repository config

<!-- What this repository says about itself, one row per item. This file was
created by `seal mode`; `templates/config.md` in the plugin documents every
row and what an absent one means. -->

| Item | Value |
|---|---|
| {item} | {value} |
"""


def under(root, rel):
    """The disk path of a `/`-joined repository-relative path.

    Spelled the way `hooks/root-migrate.py#under` spells it, and the split
    happens HERE rather than inside `os.path.join`, for the reason WORKFLOW
    gives above.
    """
    return os.path.join(root, *rel.split("/"))


def config_path(home):
    return os.path.join(home, CONFIG)


def config_rows(text):
    """Every `| Item | Value |` row under the first such header, in order.

    The header and the separator are this table's own furniture ABOVE its
    first row and somebody else's table BELOW it; any other line ends the
    table. Both rules are the ones
    `tests/test_the_pull_request_language_is_the_repositorys.py#items`
    arrived at over two review rounds, and a second reader that read the
    table differently would answer a different question about the same file.
    """
    found, seen_header = [], False
    for line in text.splitlines():
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                break
            continue
        match = CONFIG_ROW.match(line)
        if not match:
            if found:
                break
            continue
        found.append((match.group("item").strip(), match.group("value").strip()))
    return found


def declared(home):
    """(kind, value) for the `Mode` row — what the repository SAYS it wants.

      "none"     nothing is declared: no file, no such row, an empty value,
                 or a file that does not parse as that table. Four spellings
                 of one state, the same four the pull-request-language row
                 has for not naming a language
      "mode"     `local` or `shared`, lowercased
      "unknown"  a row is there and its value is not a mode — a claim nobody
                 can act on, which is not the same as no claim

    **There is no default.** Every other item in `config.md` falls back to
    what every repository got before the row existed; for the mode that is
    *the folder decides*, so an absent row is filled in from the folder by
    `seal mode` rather than assumed here. A default of `shared` would report
    every undeclared local-mode repository as lying.
    """
    try:
        with open(config_path(home), encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError):
        # Unreadable is one of the four, not a failure: `IsADirectoryError`
        # and a file this locale cannot decode both land here, and neither is
        # a reason to stop answering where the folder is.
        return "none", ""
    for item, value in config_rows(text):
        if item == ROW_ITEM:
            lowered = value.lower()
            if not lowered:
                return "none", ""
            return ("mode", lowered) if lowered in MODES else ("unknown", value)
    return "none", ""


def ending_of(line, fallback):
    """The line's own ending, or FALLBACK where it has none."""
    bare = line.rstrip("\r\n")
    return line[len(bare) :] or fallback


def line_ending(lines):
    """The first ending in the file, so a CRLF file stays CRLF."""
    for line in lines:
        found = ending_of(line, "")
        if found:
            return found
    return "\n"


def table_span(lines):
    """(index of the `Mode` row or -1, index just past the first table's last
    row or -1) — one pass, reading exactly what `config_rows` reads."""
    seen_header, mode_at, end = False, -1, -1
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if end >= 0:
                break
            continue
        match = CONFIG_ROW.match(line)
        if not match:
            if end >= 0:
                break
            continue
        end = i + 1
        # The FIRST match, because `config_rows` reads the first. A reader
        # and a writer that disagree about which row is the row leave a file
        # two rows deep that no command can bring into agreement.
        if mode_at < 0 and match.group("item").strip() == ROW_ITEM:
            mode_at = i
    return mode_at, end


def with_row(text, value):
    """TEXT with the `Mode` row set to VALUE, every other line's bytes kept.

    Three cases, and the file is a person's in all three: an existing row is
    replaced where it stands, a table with no such row gains one at its end,
    and a file with no such table at all gets one appended after a blank
    line. Nothing is re-wrapped, re-ordered, or re-ended.
    """
    row = f"| {ROW_ITEM} | {value} |"
    lines = text.splitlines(keepends=True)
    ending = line_ending(lines)
    mode_at, end = table_span(lines)

    if mode_at >= 0:
        lines[mode_at] = row + ending_of(lines[mode_at], ending)
        return "".join(lines)
    if end >= 0:
        lines.insert(end, row + ending)
        return "".join(lines)

    if lines and not lines[-1].endswith(("\n", "\r")):
        lines[-1] += ending
    if lines:
        lines.append(ending)
    lines.extend([f"| Item | Value |{ending}", f"|---|---|{ending}", row + ending])
    return "".join(lines)


def write_row(home, value):
    """Write `| Mode | value |` into the root's `config.md`; "" or why not.

    Refused rather than followed: a symbolic link at that name is a write
    that leaves the root, which is the one way out of a structure the export
    walks (`root_files`), and a directory is `IsADirectoryError` arriving as
    a traceback.
    """
    path = config_path(home)
    if os.path.islink(path):
        return f"{path} is a symbolic link"
    if os.path.isdir(path):
        return f"{path} is a directory"
    try:
        # `newline=""` on both sides, so a CRLF file is read and written back
        # as one: with translation on, every line of somebody's file would be
        # rewritten by an edit to one row of it.
        with open(path, encoding="utf-8", newline="") as handle:
            text = handle.read()
    except FileNotFoundError:
        text = None
    except (OSError, ValueError) as exc:
        return f"{path} could not be read: {exc}"

    new = (
        NEW_CONFIG.format(item=ROW_ITEM, value=value)
        if text is None
        else with_row(text, value)
    )
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(new)
    except (OSError, ValueError) as exc:
        return f"{path} could not be written: {exc}"
    return ""


def porcelain(repo, *paths):
    """`git status --porcelain` lines under PATHS, or one line saying git
    could not answer.

    **Both paths this command stages, not just the root.** The switch stages
    a removal or an addition of the workflow file too, and a guard watching
    only the root would leave that path's uncommitted work to be taken by
    `git rm`. Enumerating the class is the point; `spec.md` §"What the switch
    touches" lists all five.

    An unanswerable question reads as dirty, the direction
    `hooks/root-migrate.py#dirty` takes: moving on a guess is the one
    direction with no undo. `git rm -r --cached` drops a staged edit out of
    the index and prints nothing about it (measured 2026-09-03).
    """
    try:
        done = subprocess.run(
            ["git", "-C", repo, "status", "--porcelain", "--", *paths],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"git status could not be run ({exc})"]
    if done.returncode != 0:
        return [(done.stderr or "").strip() or f"git status exited {done.returncode}"]
    return [line for line in (done.stdout or "").splitlines() if line.strip()]


def indexed(line, moved=False):
    """Whether a porcelain line is something the index can lose.

    **Untracked is not.** The guard exists because `git rm -r --cached` takes
    a staged edit out of the index and prints nothing about it (measured
    2026-09-03); a file the index has never heard of cannot be taken out of
    it, and it travels with the folder in both directions — moved out with
    the root going to local, staged by `git add` going to shared. Refusing
    over one was not a stricter version of the same rule, it was a different
    rule with no grounds, and it made the ordinary first run refuse: `seal
    mode` writes an absent row, and the switch a person runs next met the
    file it had just written.

    **A pure deletion is not, once the move has already happened.** That is
    the shape a stopped run — or a person who ran the README's `mv` by hand —
    leaves behind: the files are gone from the worktree because they are at
    the other root now, and the `git rm -r --cached` that stages it is the
    step still owed. `hooks/root-migrate.py#dirty` makes exactly this
    exception, in the same words: "a resume has to see past its own earlier
    steps or a stopped move can never finish". It is a deletion and NOTHING
    else — `MD` and `AD` still refuse, because a staged edit is precisely
    what `git rm -r --cached` drops without a word.

    **The row this command wrote itself is not, either.** `seal mode` fills
    an absent row in from the folder, so the switch a person runs next meets
    a worktree-only modification of the one file the switch rewrites anyway.
    The `??` exception above was written for this and reached half of it: an
    untracked `config.md` passed and a TRACKED one still refused — and the
    tracked spelling is every repository `hooks/root-migrate.py` carried over
    from the 0.3.x layout, whose `.specseal/config.md` arrives committed.
    That is the population this whole work item exists for. Measured
    2026-09-03: `seal mode` then `seal mode local` exits 1.

    A STAGED edit to it still refuses, for the reason every staged edit does:
    `git rm -r --cached` drops it without a word.

    A line git could not produce at all does not start with a status pair,
    and reads as indexed — the unanswerable question refuses, which is
    `hooks/root-migrate.py#dirty`'s direction.
    """
    pair = line[:2]
    if pair == "??":
        return False
    if pair == " M" and line[3:].strip() == CONFIG_PATHSPEC:
        return False
    return not (moved and pair in ("D ", " D"))


def tracked(repo, rel):
    """True when git tracks anything under REL.

    `git rm -r --cached` on a pathspec matching no index entry exits 128
    (measured 2026-09-03), so the step is skipped rather than run and
    excused — which is also what makes a second run of a stopped switch
    finish it instead of failing.
    """
    try:
        done = subprocess.run(
            ["git", "-C", repo, "ls-files", "-z", "--", rel],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if done.returncode != 0:
        return False
    return bool([p for p in (done.stdout or "").split("\0") if p])


def other_worktrees(repo):
    """Every other worktree of this clone, by path.

    Measured 2026-09-03: switching shared → local from one worktree leaves
    every other one holding the committed `<repo>/seal/` on its own branch,
    so the two read two different roots until the commit reaches both. It
    heals itself and loses nothing, so it is named rather than refused.
    """
    here = os.path.realpath(repo)
    found = []
    for line in git(repo, "worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree ") :].strip()
            if path and os.path.realpath(path) != here:
                found.append(path)
    return found


def plugin_version():
    """The installed plugin's version, or "".

    Read from beside this script rather than from `CLAUDE_PLUGIN_ROOT`: this
    file IS in the plugin, and an environment variable is one more thing that
    can be unset in the shell a person happens to be in.
    """
    try:
        with open(
            os.path.join(PLUGIN_ROOT, ".claude-plugin", "plugin.json"),
            encoding="utf-8",
        ) as handle:
            version = json.load(handle).get("version")
    except (OSError, ValueError, AttributeError):
        return ""
    return version if isinstance(version, str) else ""


def plugin_workflow():
    """The exact bytes `install_workflow` writes, or "" when it could not.

    One reader for two questions — what to write, and whether a file already
    there is the one this plugin would have written. `remove_workflow` asks
    the second: an untracked workflow this plugin can put back byte for byte
    costs nothing to remove, and that is the state the way back names.
    """
    version = plugin_version()
    if not version:
        return ""
    source = os.path.join(PLUGIN_ROOT, "templates", "hygiene.yml")
    try:
        with open(source, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError):
        return ""
    if PLACEHOLDER not in text:
        return ""
    return text.replace(PLACEHOLDER, "v" + version)


def install_workflow(repo):
    """Write the pull-request checks; (what happened, the line to print).

    Never overwrites — the same stance the `implement` skill's bootstrap
    takes at first setup, and the same one the rest of this command takes.
    """
    path = under(repo, WORKFLOW)
    if os.path.lexists(path):
        return "kept", (
            f"  {WORKFLOW} was already there and was left alone — check that "
            "it runs the checks you want"
        )
    version = plugin_version()
    if not version:
        return "no-version", (
            f"  {WORKFLOW} was NOT written: the plugin's version could not be "
            f"read from {os.path.join(PLUGIN_ROOT, '.claude-plugin', 'plugin.json')}, "
            f"and a workflow still carrying `{PLACEHOLDER}` fails CI's clone "
            "on the first pull request. Copy templates/hygiene.yml in by hand "
            "and replace that placeholder with the release you run."
        )
    source = os.path.join(PLUGIN_ROOT, "templates", "hygiene.yml")
    try:
        with open(source, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError) as exc:
        return "unreadable", f"  {WORKFLOW} was NOT written: {source} — {exc}"
    if PLACEHOLDER not in text:
        # The substitution has to be able to fail. A template that stopped
        # carrying the placeholder would be written pinned to whatever it
        # says instead, and nothing would report it.
        return "no-placeholder", (
            f"  {WORKFLOW} was NOT written: {source} no longer carries "
            f"`{PLACEHOLDER}`, so the version could not be pinned. This is a "
            "defect in the plugin — report it rather than working around it."
        )
    text = text.replace(PLACEHOLDER, "v" + version)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    except (OSError, ValueError) as exc:
        return "failed", (
            f"  {WORKFLOW} was NOT written: {exc}. Copy "
            "templates/hygiene.yml in by hand, or run this command again."
        )
    # The return code here for the reason the root's `git add` reads it, one
    # screen down: `git()` answers "" for a failure, and an ignore rule
    # matching `.github/` reaches this one. Measured 2026-09-03 — the file was
    # written, nothing entered the index, and the command said `staged it`
    # and `Now commit`. The switch to shared exists to get the checks running,
    # so a workflow that never reaches the commit is the whole point lost,
    # silently.
    done = subprocess.run(
        ["git", "-C", repo, "add", "--", WORKFLOW],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if done.returncode != 0:
        return "unstaged", (
            f"  {WORKFLOW} was written (pinned to v{version}) but could NOT "
            f"be staged: {(done.stderr or '').strip()}\n"
            f"  A commit now would not carry it, so the pull-request checks "
            f"would never run. An ignore rule matching {WORKFLOW} or "
            f"`.github/` is the usual cause. Run `git add -f :/{WORKFLOW}` "
            "yourself, or take the rule out."
        )
    return "written", f"  wrote {WORKFLOW} (pinned to v{version}) and staged it"


def remove_workflow(repo):
    """Remove the pull-request checks; (what happened, the line to print).

    **Not tidiness.** Measured 2026-09-03 in a repository with no `seal/`:
    `unverified_check.py` exits 2 for a path that is nowhere and
    `chain_check.py` exits 0 having examined nothing. A workflow left behind
    after a switch to local gets both — a build that is red forever for a
    repository doing the right thing, and a review-chain check reporting a
    pass it never earned.

    A file this plugin did not write is left alone: deleting somebody's
    workflow because it shares a name is the destructive direction.
    """
    path = under(repo, WORKFLOW)
    if not os.path.lexists(path):
        return "absent", ""
    if os.path.islink(path):
        return "kept", (
            f"  {WORKFLOW} is a symbolic link, so it is not this plugin's "
            "file to remove — left alone. The checks it runs read committed "
            "files, and local mode commits none."
        )
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, ValueError) as exc:
        return "kept", (
            f"  {WORKFLOW} could not be read ({exc}), so it was left alone. "
            "Check by hand whether it is this plugin's."
        )
    if PLUGIN_CLONE not in text:
        return "kept", (
            f"  {WORKFLOW} was not written by this plugin, so it was left "
            "alone. Its checks read committed files and local mode commits "
            "none, so whatever it runs there will read nothing."
        )
    if not tracked(repo, WORKFLOW):
        # git holds no copy, so removing it would take the only one — unless
        # this plugin can write it back byte for byte, which is exactly the
        # state the way back it names creates: the switch to shared wrote the
        # file and staged it, `git reset` untracked it again, and the switch
        # back then left it behind. Round 1's guard was reasoned about
        # SOMEBODY ELSE'S file and applied to one this command had written a
        # moment earlier.
        if text != plugin_workflow():
            return "kept", (
                f"  {WORKFLOW} is not tracked and is not byte for byte what "
                "this plugin writes NOW — it may be somebody's own, or this "
                "plugin's from another release, since the file is pinned to "
                "the version that wrote it. Either way git holds no copy and "
                "removing it would take the only one, so it is left alone. "
                "Its checks read committed files and local mode commits none, "
                "so look at it and delete it yourself."
            )
        try:
            os.remove(path)
        except OSError as exc:
            return "failed", f"  {WORKFLOW} could not be removed: {exc}"
        return "removed", (
            f"  removed {WORKFLOW} — untracked, and byte for byte this "
            "plugin's, so `seal mode shared` writes it back"
        )
    done = subprocess.run(
        ["git", "-C", repo, "rm", "--quiet", "--", WORKFLOW],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if done.returncode != 0:
        return "failed", (
            f"  {WORKFLOW} could not be removed: {(done.stderr or '').strip()}"
        )
    return "removed", f"  removed {WORKFLOW} and staged the removal"


def say_report(repo, home, shared, local, current, kind, value):
    """The report both `seal mode` and `seal mode --check` print."""
    print(f"  folder: {current:<7}{display(repo, home)}/")
    if kind == "mode":
        print(f"  row:    {value:<7}{display(repo, config_path(home))}")
    elif kind == "unknown":
        print(
            f"  row:    {value} — which is not a mode. The two values are "
            f"`{LOCAL}` and `{SHARED}`."
        )
    else:
        print(f"  row:    not declared  ({display(repo, config_path(home))})")


def mode_report(args, repo, home, shared, local, current):
    """`seal mode` and `seal mode --check`: the folder, the row, and whether
    they agree. The folder is never moved here.

    An absent row is written from the folder — the state every repository
    with a `config.md` is in today, since the pull-request language shipped
    as its only row. The value is an observation this command just made, so
    it cannot be wrong; nothing falls back to a default, because there is
    none. `--check` writes nothing at all: it runs in CI, and a check that
    mutates the tree it checks is not a check.
    """
    kind, value = declared(home)
    if kind == "none" and not args.check:
        failed = write_row(home, current)
        if failed:
            print(f"the `{ROW_ITEM}` row could not be written: {failed}")
            print("The folder is still the answer, and it is:")
        else:
            print(
                f"no `{ROW_ITEM}` row was declared, so one was written from "
                f"where the folder is: `| {ROW_ITEM} | {current} |` in "
                f"{display(repo, config_path(home))}"
            )
            kind, value = "mode", current

    say_report(repo, home, shared, local, current, kind, value)

    if kind == "unknown":
        print(
            f"\nThe row names no mode, so nothing can be applied from it. "
            f"`seal mode {current}` writes what the folder says; editing the "
            f"row to `{LOCAL}` or `{SHARED}` and running `seal mode --apply` "
            "moves the folder."
        )
        return 1 if args.check else 0
    if kind == "none":
        return 0
    if value == current:
        print("\nThey agree.")
        return 0
    print(
        f"\nThey disagree: the row says `{value}` and the folder is "
        f"{current}. Two commands end it —"
    )
    print(f"  seal mode --apply     move the folder to {value}, as the row says")
    print(f"  seal mode {current:<11}correct the row to {current}, as the folder is")
    return 1 if args.check else 0


def both_roots(shared, local):
    return (
        "both roots exist, and the gates read the first of them:\n"
        f"  {shared}   (shared mode — read first)\n"
        f"  {local}   (local mode)\n"
        "Switching from here would leave the other where nothing reads it. "
        "Move or remove one first."
    )


def gitlinks_under_root(repo):
    """(submodule entries under the root, why they could not be read).

    Entries is None when the question could not be answered. `git()` reads
    every failure as "", so asking through it would answer "no submodule" for
    a timeout or a git that is not on PATH — and this guard exists to stop a
    break that cannot be undone, which is the shape `indexed`'s docstring
    calls the unanswerable question refusing.

    Entries are as `git ls-files --stage` prints them.

    `git rm -r --cached <root>` drops a gitlink from the index and leaves
    `.gitmodules` naming the path, and moving the root breaks the submodule's
    relative gitdir. Measured 2026-09-03: the switch exited 0 and `git
    status` in the moved root died with `fatal: not a git repository`.

    A sixth member of the class `spec.md`'s *What the switch touches* table
    enumerates — the table that says it is enumerated rather than fixed where
    a finding points, and then listed five.
    """
    try:
        done = subprocess.run(
            ["git", "-C", repo, "ls-files", "--stage", "--", optin.HOME],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"git ls-files could not be run ({exc})"
    if done.returncode != 0:
        return None, (done.stderr or "").strip() or (
            f"git ls-files exited {done.returncode}"
        )
    return [
        line for line in (done.stdout or "").splitlines() if line.startswith("160000")
    ], ""


def refusals(repo, home, shared, local, wanted):
    """Every reason not to switch, gathered before anything is written.

    The list is the class in `spec.md` §"What the switch touches", walked in
    order, rather than the guards a reader thinks of first. The one act that
    is NOT preflighted is the workflow file, because it is the last step and
    a second run finishes it — the resume is what makes preflighting it
    unnecessary.
    """
    if not local:
        return ["the common git directory could not be resolved"]
    if os.path.isdir(shared) and os.path.isdir(local):
        return [both_roots(shared, local)]

    source = shared if wanted == LOCAL else local
    destination = local if wanted == LOCAL else shared
    found = []

    gitlinks, unreadable = gitlinks_under_root(repo)
    if gitlinks is None:
        found.append(
            f"whether there is a submodule under {optin.HOME}/ could not be "
            f"read: {unreadable}. A gitlink does not survive the move, so the "
            "unanswerable question refuses — the direction `porcelain` and "
            "`indexed` already take."
        )
    elif gitlinks:
        found.append(
            f"there is a submodule under {optin.HOME}/:\n  "
            + "\n  ".join(gitlinks)
            + f"\nMoving the root breaks its relative gitdir, and `git rm -r "
            f"--cached {optin.HOME}` drops the gitlink while .gitmodules goes "
            "on naming the path. Deinit it or move it out of the root first."
        )

    if os.path.islink(source):
        found.append(
            f"{source} is a symbolic link, not the root itself. Moving it "
            "would move the link and leave the records where they are."
        )
    if os.path.isdir(source) and os.path.lexists(destination):
        found.append(
            f"{destination} already exists, and nothing here overwrites. "
            "Move or remove it first."
        )

    # Whether the root is already where this is trying to put it. A move
    # somebody already made by hand is the one state whose deletions are not
    # work in progress — see `indexed`.
    moved = os.path.isdir(destination) and not os.path.lexists(source)
    lines = [
        line
        for line in porcelain(repo, optin.HOME, WORKFLOW)
        if indexed(line, moved=moved)
    ]
    if lines:
        found.append(
            "the tree is not clean under the paths this would stage:\n  "
            + "\n  ".join(lines)
            + "\nCommit or stash them first. `git rm -r --cached` takes a "
            "staged edit out of the index and prints nothing about it, so a "
            "half-staged switch is worse than none."
        )

    config = config_path(home)
    if os.path.islink(config):
        found.append(f"{config} is a symbolic link, and the row is written there")
    elif os.path.isdir(config):
        found.append(f"{config} is a directory, and the row is written there")
    elif os.path.isfile(config):
        try:
            with open(config, encoding="utf-8", newline="") as handle:
                handle.read()
        except (OSError, ValueError) as exc:
            found.append(
                f"{config} could not be read ({exc}), and the row is written there"
            )
    return found


def switch(args, repo, home, shared, local, current, wanted):
    """Move the root, write the row, stage the index, carry the workflow file.

    In the order of `spec.md` §"Order, and what a stopped run leaves": the
    rename first, because it is the step that can fail for reasons outside
    this command and until it succeeds nothing has happened. Every step after
    it is idempotent, so `seal mode <the same mode>` finishes a stopped run —
    and so does a person who already ran the README's `mv` by hand.
    """
    source = shared if wanted == LOCAL else local
    destination = local if wanted == LOCAL else shared

    stop = refusals(repo, home, shared, local, wanted)
    if stop:
        for line in stop:
            print(line)
        print("\nNothing was moved.")
        return 1

    if wanted == SHARED:
        print(
            "Going to shared mode puts the records in the tree. Until you "
            f"commit, `git reset -- :/{optin.HOME} :/{WORKFLOW}` and then "
            "`seal mode local` walk the whole thing back — the switch stages, "
            "and the guard refuses a switch over a staged change. The "
            "pathspec is there because a bare `git reset` unstages the whole "
            "index, and this guard has never looked outside those two paths. "
            "`:/` makes each path mean the same thing from any directory — a "
            "git pathspec is read from where you stand, and without it the "
            "command exits 0 having unstaged nothing when you are not at the "
            "root. Every command this file hands you to run carries it, for "
            "that reason. "
            "After the commit they are in the history, and taking "
            "them out of the tree later does not take them out of it."
        )
    else:
        print(
            "Going to local mode takes the records out of the tree. Every "
            "other clone loses them at the next pull — `seal export` here "
            "and `seal import` there is how a teammate gets a copy."
        )
    for line in porcelain(repo, optin.HOME):
        # `??` itself, not `indexed`. That function has three exceptions now
        # and only this one means untracked — reading its answer as the
        # question called a tracked, modified `config.md` untracked, in a
        # note whose whole subject is what the index can lose.
        if line[:2] == "??":
            print(
                f"note: {line[3:]} is untracked, so the index cannot lose it "
                "— it travels with the folder."
            )
    for path in other_worktrees(repo):
        print(
            f"note: {path} is another worktree of this clone. Until the "
            "commit reaches its branch it reads the root its own tree has, "
            "which is not the one this move leaves."
        )
    print("")

    moved = False
    if os.path.isdir(source):
        try:
            os.rename(source, destination)
        except OSError as exc:
            print(f"the root could not be moved: {exc}")
            print(
                "Nothing else has run. From the repository root, this does "
                "the move across filesystems:\n"
                f'  mv "{source}" "{destination}"\n'
                "then run this command again to finish."
            )
            return 1
        moved = True
        print(f"  moved {display(repo, source)} to {display(repo, destination)}")
    else:
        print(f"  {display(repo, destination)} is already the root")

    failed = write_row(destination, wanted)
    if failed:
        print(f"  the `{ROW_ITEM}` row was NOT written: {failed}")
    else:
        print(f"  wrote `| {ROW_ITEM} | {wanted} |` in {CONFIG}")

    if wanted == LOCAL:
        if tracked(repo, optin.HOME):
            done = subprocess.run(
                [
                    "git",
                    "-C",
                    repo,
                    "rm",
                    "-r",
                    "--cached",
                    "--quiet",
                    "--",
                    optin.HOME,
                ],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if done.returncode != 0:
                print(
                    f"  the records are still tracked: "
                    f"{(done.stderr or '').strip()}\n"
                    f"  Run `git rm -r --cached :/{optin.HOME}` yourself, or "
                    "this command again."
                )
            else:
                print(f"  staged the removal of {optin.HOME}/ from the tree")
        else:
            print(f"  nothing under {optin.HOME}/ was tracked")
        _, line = remove_workflow(repo)
        if line:
            print(line)
    else:
        # The return code, not the call. `git()` reads a failure as "" — and
        # `git add` exits non-zero for an ignore rule matching the root, or a
        # held `index.lock`. Measured 2026-09-03: the root moved into the
        # tree, nothing was staged, and the command printed `staged seal/`
        # and `Now commit`. The local direction has read this code since it
        # was written; this side had not.
        done = subprocess.run(
            ["git", "-C", repo, "add", "--", optin.HOME],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if done.returncode != 0:
            print(
                f"  {optin.HOME}/ could NOT be staged: "
                f"{(done.stderr or '').strip()}\n"
                f"  A commit now would record nothing. An ignore rule "
                f"matching the root is the usual cause. Run "
                f"`git add -f :/{optin.HOME}` yourself, or this command again."
            )
        else:
            print(f"  staged {optin.HOME}/")
        _, line = install_workflow(repo)
        if line:
            print(line)

    print("\nNow commit. The switch is what the commit records:\n  git commit")
    if moved and wanted == SHARED:
        print(
            f"Until then, `git reset -- :/{optin.HOME} :/{WORKFLOW}` and then "
            "`seal mode local` puts it back — the switch stages, and the "
            "guard refuses a switch over a staged change. The pathspec is "
            "there because a bare `git reset` unstages the whole index."
        )
    return 0


def mode(args, cwd):
    repo, home, shared, local, current = resolve(cwd)
    if not home:
        if args.check:
            if not repo:
                # Not the same answer as "there is no root". A repository
                # that could not be resolved is a check that did not RUN, and
                # a gate that cannot tell reads exactly like an allow — the
                # shape issue #28 is open on. `optin.repo_root` answers ""
                # for a timeout or a git that is not on PATH, and a shared
                # root committed beside a row saying `local` is what CI is
                # here to catch.
                print(
                    "no git repository could be resolved here, so the mode "
                    "was never read. This is not agreement and it is not a "
                    "disagreement — the check could not run."
                )
                return 1
            # A check that fails where there is nothing to check teaches
            # people to delete the check. A workflow that outlived its root
            # already goes red on `unverified_check.py`, which exits 2 for a
            # path that is nowhere; this one has nothing to add to that.
            print("no seal/ here, so nothing is declared and nothing can disagree.")
            return 0
        return no_root(repo, shared, local)

    wanted = args.mode
    if args.apply:
        kind, value = declared(home)
        if kind == "mode":
            wanted = value
        else:
            named = (
                f"names `{value}`, which is not a mode"
                if kind == "unknown"
                else "is not declared"
            )
            print(f"the `{ROW_ITEM}` row {named}, so there is nothing to apply.")
            print(
                f"Write one in {display(repo, config_path(home))} —\n"
                f"  | {ROW_ITEM} | {LOCAL} |\n"
                f"or run `seal mode {LOCAL}` / `seal mode {SHARED}` to switch "
                "and write the row in one step."
            )
            return 1

    if not wanted:
        return mode_report(args, repo, home, shared, local, current)
    return switch(args, repo, home, shared, local, current, wanted)


# --- the release reminder ---------------------------------------------------


def check(cwd):
    repo, home, shared, local, mode = resolve(cwd)
    if not home:
        return no_root(repo, shared, local)
    if mode == "shared":
        # Never a failure. A release script runs this unconditionally, and a
        # shared-mode repository has nothing to be reminded about: the records
        # are in the commit range already.
        print("shared mode: the records are committed, so there is nothing to export.")
        return 0

    files, _ = root_files(home)
    now = work_item_digests(files)
    last = read_state(repo)
    if not last or not isinstance(last.get("items"), dict):
        print(
            f"{len(now)} work items here and no export yet — "
            "`seal export` writes the first copy."
        )
        return 0

    then = last["items"]
    changed = len({*now, *then}) - sum(
        1 for item in now if item in then and now[item] == then[item]
    )
    print(f"{changed} work items changed since the last export")
    return 0


# --- entry point ------------------------------------------------------------


def main(argv=None, cwd=None):
    cwd = cwd or os.getcwd()
    parser = argparse.ArgumentParser(
        prog="seal",
        description="where this repository's seal/ root lives, and how a copy "
        "of it travels between clones",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ex = sub.add_parser("export", help="write the root to a zip")
    ex.add_argument("--output", help="the zip's path, or a directory to put it in")
    ex.add_argument(
        "--check",
        action="store_true",
        help="print how many work items changed since the last export, and "
        "write nothing",
    )

    im = sub.add_parser("import", help="merge a zip's records in")
    im.add_argument("zip", help="the zip `seal export` wrote")
    im.add_argument(
        "--into",
        choices=("shared", "local"),
        help="which mode's root to write into, creating it. Default: the one "
        "in force, or local where neither exists",
    )
    im.add_argument(
        "--allow-other-repo",
        action="store_true",
        help="import although the manifest names a different remote",
    )

    md = sub.add_parser(
        "mode", help="report the mode, or switch between shared and local"
    )
    md.add_argument(
        "mode",
        nargs="?",
        choices=MODES,
        help="the mode to switch to. With none, the mode is reported",
    )
    md.add_argument(
        "--check",
        action="store_true",
        help="report, write nothing, and exit 1 when the row and the folder "
        "disagree. This is what CI runs",
    )
    md.add_argument(
        "--apply", action="store_true", help="switch to whatever the `Mode` row says"
    )

    args = parser.parse_args(argv)
    if args.command == "export":
        return check(cwd) if args.check else export(args, cwd)
    if args.command == "mode":
        # Three spellings of one answer, and any two together is a question
        # with two answers rather than a shorthand. Refused here rather than
        # resolved by precedence: a person who typed both meant one of them,
        # and this command moves directories.
        given = [
            name
            for name, on in (
                ("a mode", bool(args.mode)),
                ("--check", args.check),
                ("--apply", args.apply),
            )
            if on
        ]
        if len(given) > 1:
            parser.error(f"{' and '.join(given)} cannot be given together")
        return mode(args, cwd)
    return import_(args, cwd)


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
