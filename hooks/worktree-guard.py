#!/usr/bin/env python3
"""PreToolUse guard: keep worktrees tied to genuinely CONCURRENT work.

Reads the Claude Code hook JSON on stdin and guards both directions of the same
rule, using one signal -- how many work streams are actually live on this tree.

A) Branch switching (Bash: git checkout/switch of a branch, or a -b/-c variant)

  - ACTIVE Claude session inside THIS working tree -> deny, steer to a worktree
  - only IDLE sessions (no terminal input for a while) -> ask -- they are
    usually forgotten tabs, and the user can tell
  - tracked changes present (dirty)                 -> ask the user first
  - otherwise (single work stream, clean)           -> allow the plain switch

B) Worktree creation, whichever path it takes:
     - Bash: `git worktree add ...`
     - Agent/Task tool with `isolation: "worktree"` (harness-managed, lands in
       `<repo>/.claude/worktrees/<name>` and never goes through Bash)

  - another Claude session inside THIS working tree -> ask (concurrent: justified)
  - cannot tell                                     -> ask
  - otherwise (single work stream)                  -> deny, steer to `git switch`
    (`[worktree-ok]` anywhere in the command downgrades this to ask -- for when
    the user explicitly wants a worktree despite being single-stream)

Session activity: a session counts as ACTIVE when, within
WORKTREE_GUARD_IDLE_MIN minutes (default 5; env-overridable), EITHER its
terminal saw input or output OR its project's transcript files
(session .jsonl files and session subdirs incl. background-agent
transcripts, excluding this session's own) were written. The transcript signal is what makes 5 minutes safe: an autonomous
turn types nothing for long stretches but writes its transcript every few
seconds, while a forgotten tab goes quiet on both signals. Sessions where
neither signal can be read are conservatively treated as active.

Command matching: only segments whose FIRST word (after env assignments and
wrappers like `command`/`nohup`) is `git` are classified. Mentions of
"git switch" inside echo arguments or heredoc prose no longer trigger the
guard. Known residual: a heredoc line that IS exactly a git command still
matches -- segment splitting cannot tell heredoc bodies apart.

Note: sessions living in a linked worktree are already isolated and are NOT
counted -- switching the shared tree cannot affect them. File-restore forms of
`git checkout` (and `git restore`) are always allowed, as is every non-`add`
worktree subcommand (`list`, `remove`, `prune`). `git switch -`/`checkout -`
count as switches (they are). A `git checkout <name>` that would DWIM a
remote-only branch is also a switch.
"""

import json
import os
import re
import shlex
import subprocess
import sys
import time


def _idle_min():
    """A typo in the override must not disable the guard: an unparseable or
    non-positive value falls back to the default rather than raising at
    import time, where the crash would read as a silent allow."""
    try:
        v = int(os.environ.get("WORKTREE_GUARD_IDLE_MIN", "5"))
    except ValueError:
        return 5
    return v if v > 0 else 5


IDLE_MIN = _idle_min()


def _lang():
    """SPECSEAL_LANG wins; otherwise the system locale; default English."""
    v = os.environ.get("SPECSEAL_LANG", "")
    if v:
        return "ko" if v.lower().startswith("ko") else "en"
    sys_locale = os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
    return "ko" if sys_locale.lower().startswith("ko") else "en"


LANG = _lang()


def tr(en, ko):
    return ko if LANG == "ko" else en


WRAPPERS = {"command", "nohup", "time", "env", "sudo"}


def load_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def split_segments(command: str):
    """Split a shell command line into individual command segments."""
    # Break on &&, ||, ;, |, and newlines. Good enough for intent detection.
    return re.split(r"&&|\|\||[;\n|]", command)


def parse_git(tokens):
    """Return (subcommand, args) if this segment IS a git invocation, else None.

    `git` must be the segment's command word -- leading VAR=val assignments and
    common wrappers are skipped, anything else (echo, cat, prose) disqualifies
    the segment. Then git's own global options (-C <path>, -c k=v, ...) are
    skipped to find the subcommand.
    """
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if ("=" in t and not t.startswith("-")) or os.path.basename(t) in WRAPPERS:
            i += 1
            continue
        break
    if i >= len(tokens) or os.path.basename(tokens[i]) != "git":
        return None
    rest = tokens[i + 1 :]
    i = 0
    takes_value = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
    while i < len(rest):
        t = rest[i]
        if t in takes_value:
            i += 2
            continue
        if t.startswith("-") and t != "-":
            i += 1
            continue
        break
    if i >= len(rest):
        return None
    return rest[i], rest[i + 1 :]


def is_ref(name: str, cwd: str) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{name}^{{commit}}"],
            cwd=cwd or None,
            capture_output=True,
        )
        return r.returncode == 0
    except Exception:
        return False


def classify(segment: str, cwd: str):
    """Return a reason string if this segment switches branch or adds a worktree."""
    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None
    parsed = parse_git(tokens)
    if not parsed:
        return None
    sub, args = parsed

    if sub == "worktree":
        # Only creation is guarded; list/remove/prune are how you clean up.
        positionals = [a for a in args if not a.startswith("-")]
        if positionals and positionals[0] == "add":
            return "worktree-add"
        return None

    if sub == "switch":
        # git switch <branch> / -c <branch> / `-` (previous)  => switches tree
        creating = any(a in ("-c", "-C") for a in args)
        has_target = any(a == "-" or not a.startswith("-") for a in args)
        if creating or has_target:
            return "create+switch" if creating else "switch"
        return None

    if sub == "checkout":
        if any(a in ("-b", "-B") for a in args):
            return "create+switch"
        if "--" in args:
            return None  # explicit path restore
        if "-" in args:
            return "switch"  # previous branch
        positionals = [a for a in args if not a.startswith("-")]
        if not positionals:
            return None
        first = positionals[0]
        if (
            first == "."
            or os.path.exists(os.path.join(cwd or ".", first))
            or os.path.exists(first)
        ):
            return None  # restoring a file/dir, not switching branch
        if is_ref(first, cwd):
            return "switch"
        if is_ref(f"origin/{first}", cwd):
            return "switch"  # DWIM checkout of a remote-only branch
        return None

    return None


def ancestors(pid: int):
    """Pids of this process and everything above it (so we never count ourselves)."""
    seen = {pid}
    cur = pid
    for _ in range(20):
        try:
            r = subprocess.run(
                ["ps", "-o", "ppid=", "-p", str(cur)], capture_output=True, text=True
            )
            ppid = int(r.stdout.strip())
        except Exception:
            break
        if ppid <= 1:
            break
        seen.add(ppid)
        cur = ppid
    return seen


def proc_cwd(pid: int):
    """Working directory of another process, or None if it cannot be read.

    /proc first: it is free, and lsof is not installed by default on server
    and container Linux — where its absence used to make every other session
    invisible, which is the fail-open direction (the guard then reports a
    single stream and allows a switch that yanks someone else's branch).
    lsof remains the path on macOS, which has no /proc.
    """
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        pass
    try:
        r = subprocess.run(
            ["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
            capture_output=True,
            text=True,
        )
        for line in r.stdout.splitlines():
            if line.startswith("n"):
                return line[1:]
    except Exception:
        pass
    return None


SHELLS = {
    "zsh",
    "bash",
    "sh",
    "fish",
    "login",
    "tmux",
    "screen",
    "claude",
    "-zsh",
    "-bash",
}
APP_LABELS = [
    ("Code Helper", "VS Code"),
    ("Visual Studio Code", "VS Code"),
    ("Cursor", "Cursor"),
    ("iTerm", "iTerm2"),
    ("Terminal", "Terminal"),
    ("WezTerm", "WezTerm"),
    ("Warp", "Warp"),
    ("kitty", "kitty"),
    ("Alacritty", "Alacritty"),
]


def host_app(pid: int):
    """Which application's terminal hosts this session — from the ANCESTOR
    chain, never from sibling processes (an MCP server's --app flag next to a
    session led to a wrong 'Cursor' attribution in practice)."""
    cur = pid
    for _ in range(15):
        try:
            r = subprocess.run(
                ["ps", "-o", "ppid=,comm=", "-p", str(cur)],
                capture_output=True,
                text=True,
            )
            out = r.stdout.strip()
            if not out:
                return None
            ppid_s, _, comm = out.partition(" ")
            ppid = int(ppid_s)
        except Exception:
            return None
        for needle, label in APP_LABELS:
            if needle in comm:
                return label
        if ppid <= 1:
            name = os.path.basename(comm.strip())
            return name if name not in SHELLS else None
        cur = ppid
    return None


def last_user_snippet(cwd: str, own_session_id: str):
    """(session-id-prefix, ts, text) of the newest OTHER session's last user
    message in this project — so a blocking prompt lets the human recognize
    WHICH forgotten conversation is being protected."""
    proj = os.path.expanduser(os.path.join("~/.claude/projects", project_slug(cwd)))
    best = None
    try:
        for name in os.listdir(proj):
            if not name.endswith(".jsonl"):
                continue
            if own_session_id and name == f"{own_session_id}.jsonl":
                continue
            path = os.path.join(proj, name)
            try:
                m = os.stat(path).st_mtime
            except OSError:
                continue
            if best is None or m > best[0]:
                best = (m, path, name)
    except OSError:
        return None
    if not best:
        return None
    _, path, name = best
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 131072))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    snippet = None
    for line in tail.splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") != "user":
            continue
        content = (d.get("message") or {}).get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                x.get("text", "")
                for x in content
                if isinstance(x, dict) and x.get("type") == "text"
            )
        else:
            continue
        text = " ".join(text.split())
        if text:
            snippet = (name.split(".")[0][:8], d.get("timestamp", "")[:16], text[:80])
    return snippet


def tty_idle_minutes(pid: int):
    """Minutes since the terminal hosting `pid` last saw input OR output.

    None when the pid has no tty or it cannot be checked -- callers treat
    that conservatively (active). atime is bumped by keystrokes (human
    present), mtime by writes to the screen -- a session streaming its
    progress repaints constantly, while an idle Claude Code prompt does not
    repaint at all (verified), so the fresher of the two is the signal.
    """
    try:
        r = subprocess.run(
            ["ps", "-o", "tty=", "-p", str(pid)], capture_output=True, text=True
        )
        tty = r.stdout.strip()
        if not tty or tty == "??":
            return None
        st = os.stat(f"/dev/{tty}")
        return max(0.0, (time.time() - max(st.st_atime, st.st_mtime)) / 60)
    except Exception:
        return None


def project_slug(path: str) -> str:
    """~/.claude/projects encodes a cwd by replacing non-alphanumerics with '-'."""
    return re.sub(r"[^A-Za-z0-9-]", "-", path)


ACTIVE_EVENT_TYPES = {"user", "assistant", "tool_use", "tool_result", "progress"}


def last_active_event_epoch(path: str):
    """Epoch of the newest ACTIVE event in a transcript's tail, else None.

    File mtime alone over-reports activity: idle sessions still receive
    passive appends (type "attachment" -- e.g. file-changed notices when some
    OTHER session edits a file they had read), observed live. So when the
    mtime looks fresh, confirm by scanning the last 64KB for events that mean
    someone is actually driving: user/assistant/tool traffic.
    """
    import datetime

    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 65536))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    for line in reversed(tail.splitlines()):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") not in ACTIVE_EVENT_TYPES:
            continue
        ts = d.get("timestamp")
        if not isinstance(ts, str):
            continue
        try:
            return datetime.datetime.fromisoformat(
                ts.replace("Z", "+00:00")
            ).timestamp()
        except ValueError:
            continue
    return None


def file_activity_epoch(path: str, stale_before: float):
    """Epoch of a transcript file's last real activity.

    Stale mtime is trusted as-is (mtime bounds every event, and passive
    appends only ever make it look FRESHER); a fresh mtime must be confirmed
    against the tail's active events.
    """
    try:
        m = os.stat(path).st_mtime
    except OSError:
        return None
    if m < stale_before:
        return m
    return last_active_event_epoch(path)


def transcript_idle_minutes(cwd: str, own_session_id: str):
    """Minutes since any OTHER session's transcript in `cwd`'s project dir was
    written -- top-level <session-id>.jsonl files AND session subdirectories,
    where background-agent transcripts live (<session-id>/subagents/*.jsonl).
    None when there is no readable transcript to judge by.

    A session running an autonomous turn appends its transcript every few
    seconds even though the keyboard is silent, and a background agent does
    the same in the session's subagents directory -- these signals keep
    working sessions out of the "forgotten tab" bucket. Per-project, not
    per-pid: if ANY other session of this project is writing, treat the tree
    as actively worked on.
    """
    proj = os.path.expanduser(os.path.join("~/.claude/projects", project_slug(cwd)))
    newest = None
    threshold = time.time() - IDLE_MIN * 60
    try:
        entries = os.listdir(proj)
    except OSError:
        return None
    for name in entries:
        path = os.path.join(proj, name)
        if name.endswith(".jsonl"):
            if own_session_id and name == f"{own_session_id}.jsonl":
                continue
            m = file_activity_epoch(path, threshold)
            if m is not None and (newest is None or m > newest):
                newest = m
        elif os.path.isdir(path):
            # Session subdirectories hold background-agent transcripts
            # (<session-id>/subagents/agent-*.jsonl). A session whose
            # foreground sits quiet while a background agent grinds for 30+
            # minutes is only visible here. Skip our own session's dir.
            if own_session_id and name == own_session_id:
                continue
            for root, _dirs, files in os.walk(path):
                for f in files:
                    if not f.endswith(".jsonl"):
                        continue
                    m = file_activity_epoch(os.path.join(root, f), threshold)
                    if m is not None and (newest is None or m > newest):
                        newest = m
                if newest is not None and newest >= threshold:
                    break  # already fresh enough -- no need to walk further
            if newest is not None and newest >= threshold:
                break
    if newest is None:
        return None
    return max(0.0, (time.time() - newest) / 60)


def fresh_leases(top: str, own_session_id: str = ""):
    """DECLARED work streams — leases beat every heuristic. The session-lease
    hook stamps <git-dir>/specseal-leases/<session-id> on each tool call
    touching this tree, which catches what process scanning cannot:
    extension-hosted sessions (comm != claude) and sessions editing this tree
    from another cwd (both observed live)."""
    entries = []
    try:
        gd = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"],
            cwd=top or None,
            capture_output=True,
            text=True,
        )
        leases = (
            os.path.join(gd.stdout.strip(), "specseal-leases")
            if gd.returncode == 0
            else None
        )
    except Exception:
        leases = None
    if leases and os.path.isdir(leases):
        for name in os.listdir(leases):
            if own_session_id and name == own_session_id:
                continue
            try:
                age = (time.time() - os.stat(os.path.join(leases, name)).st_mtime) / 60
            except OSError:
                continue
            if age < IDLE_MIN:
                entries.append((None, f"{top}  [lease: {name[:8]}…]", None, age, None))
    return entries


def sessions_in_tree(top: str, own_session_id: str = ""):
    """Other Claude sessions whose cwd sits inside `top`.

    Returns (active, idle, reliable). A session is idle when BOTH signals are
    quiet for IDLE_MIN minutes: no terminal input AND no transcript writes in
    its project -- alive, but nobody (human or autonomous turn) is driving it.
    `reliable` is False when detection cannot be trusted -- notably when we
    cannot even spot our own process -- and the caller then falls back to the
    conservative behaviour.
    """
    # `pgrep -x claude` was observed to silently miss live sessions on macOS,
    # so enumerate with ps and match the executable basename ourselves.
    try:
        r = subprocess.run(["ps", "-axo", "pid=,comm="], capture_output=True, text=True)
        pids = set()
        for line in r.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            num, _, comm = line.partition(" ")
            if os.path.basename(comm.strip()) == "claude":
                pids.add(int(num))
    except Exception:
        return [], [], False
    if not pids:
        return [], [], False

    mine = ancestors(os.getpid())
    if not (pids & mine):
        return [], [], False  # our own session is invisible -> detection is unusable

    active, idle = [], []
    for p in sorted(pids - mine):
        d = proc_cwd(p)
        if d and (d == top or d.startswith(top + os.sep)):
            tty_idle = tty_idle_minutes(p)
            tr_idle = transcript_idle_minutes(d, own_session_id)
            signals = [v for v in (tty_idle, tr_idle) if v is not None]
            # Idle only when every readable signal is quiet; no signals at all
            # -> conservative (active).
            entry = (p, d, tty_idle, tr_idle, host_app(p))
            if signals and min(signals) >= IDLE_MIN:
                idle.append(entry)
            else:
                active.append(entry)

    active.extend(fresh_leases(top, own_session_id))

    # Sessions whose process is NOT named claude (VS Code extension panels,
    # embedded hosts) are invisible to the scan above — but they still write
    # this project's transcripts. Fresh active events with no process to pin
    # them on = an unattached live session; measured live when a background
    # agent kept working after its terminal pid died from the scan's view.
    if not active:
        tr_idle = transcript_idle_minutes(top, own_session_id)
        if tr_idle is not None and tr_idle < IDLE_MIN:
            active.append((None, top, None, tr_idle, None))
    return active, idle, True


def _age(minutes):
    if minutes is None:
        return tr("unknown", "확인 불가")
    if minutes >= 60:
        return tr(f"{minutes / 60:.1f}h ago", f"{minutes / 60:.1f}시간 전")
    return tr(f"{minutes:.0f}m ago", f"{minutes:.0f}분 전")


def fmt_sessions(entries):
    """Per-session line with DISAGGREGATED signals and host app. "마지막 활동
    1분 전" alone proved undiagnosable in practice — the reader could not tell
    a keystroke from an autonomous turn's transcript write, and app guesses
    made from sibling MCP processes misattributed a VS Code tab to Cursor."""
    lines = []
    for p, d, tty_idle, tr_idle, app in entries:
        if p is None:
            kind = (
                tr("lease declaration", "lease 선언")
                if "[lease:" in d
                else tr("transcript activity", "작업 기록(트랜스크립트)")
            )
            lines.append(
                tr(
                    f"    (unidentified session — extension panel or a session in another cwd)  {d}\n"
                    f"        {kind} {_age(tr_idle)} — working on this tree right now",
                    f"    (프로세스 미확인 세션 — VS Code 확장 패널·다른 cwd 의 세션 등)  {d}\n"
                    f"        {kind} {_age(tr_idle)} — 지금 이 트리에서 작업 중",
                )
            )
            continue
        where = (tr(f" ({app} terminal)", f" ({app} 터미널)")) if app else ""
        lines.append(
            tr(
                f"    pid {p}{where}  {d}\n"
                f"        terminal in/out {_age(tty_idle)} · transcript activity {_age(tr_idle)}",
                f"    pid {p}{where}  {d}\n"
                f"        터미널 입력/출력 {_age(tty_idle)} · 작업 기록(트랜스크립트) {_age(tr_idle)}",
            )
        )
    return "\n".join(lines)


def fmt_snippet(cwd, own_session_id):
    s = last_user_snippet(cwd, own_session_id)
    if not s:
        return ""
    sid, ts, text = s
    quoted = chr(34) + text + chr(34)
    return tr(
        f"\nNewest other-session record for this tree [{sid}… {ts}], last user message:\n"
        f"    {quoted}\n",
        f"\n이 트리의 가장 최근 다른 세션 기록 [{sid}… {ts}] 마지막 사용자 메시지:\n"
        f"    {quoted}\n",
    )


def tracked_changes(cwd: str) -> list[tuple[str, str]]:
    """(XY, path) entries of staged+unstaged changes to TRACKED files.

    Untracked files are excluded on purpose: they stay put across a switch and
    do not get carried onto the other branch.
    """
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=cwd or None,
            capture_output=True,
            text=True,
        )
        return [(line[:2], line[3:]) for line in r.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def phantom_entries(entries: list[tuple[str, str]], cwd: str) -> list[tuple[str, str]]:
    """Dirt invisible in the working tree: index-only entries (AD) and
    force-added paths that .gitignore hides from a plain directory view.
    """
    phantoms = []
    for xy, path in entries:
        if xy == "AD":
            phantoms.append(
                (
                    path,
                    tr(
                        "exists only in the index (added, then deleted in the worktree)",
                        "index에만 존재 (add 후 워크트리에서 삭제됨)",
                    ),
                )
            )
        # --no-index: check-ignore never flags indexed paths without it, and a
        # force-added file is by definition in the index.
        elif (
            xy[0] != " "
            and subprocess.run(
                ["git", "check-ignore", "-q", "--no-index", path],
                cwd=cwd or None,
                capture_output=True,
            ).returncode
            == 0
        ):
            phantoms.append(
                (
                    path,
                    tr(
                        "gitignored path force-staged into the index",
                        ".gitignore 경로인데 강제 스테이징됨",
                    ),
                )
            )
    return phantoms


def respond(decision: str, reason: str):
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
    sys.exit(0)


def repo_paths(cwd: str):
    """Return (toplevel, suggested worktree root) for the repo containing cwd."""
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd or None,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:
        top = ""
    if not top:
        return "", "../<repo>-worktrees"
    return top, os.path.join(os.path.dirname(top), f"{os.path.basename(top)}-worktrees")


def steer_to_switch() -> str:
    return tr(
        "  git fetch origin\n"
        "  git switch -c <branch> origin/main   # new branch\n"
        "  git switch <branch>                  # existing branch\n\n"
        "If this genuinely is concurrent work needing separation, state why and get the "
        "user's confirmation first (if the user already asked for a worktree, retry with "
        "[worktree-ok] in the command).",
        "  git fetch origin\n"
        "  git switch -c <branch> origin/main   # 새 브랜치\n"
        "  git switch <branch>                  # 기존 브랜치\n\n"
        "정말 동시 작업이라 분리가 필요하면 그 이유를 밝히고 사용자 확인을 먼저 받으세요 "
        "(사용자가 이미 워크트리를 지시했다면 명령에 [worktree-ok] 를 붙여 다시 시도).",
    )


def guard_worktree_creation(
    top: str, cwd: str, origin: str, user_ok: bool, session_id: str = ""
):
    """Worktrees are for CONCURRENT work only -- block the single-stream case."""
    active, idle, reliable = sessions_in_tree(top or cwd, session_id)

    # 1) 같은 트리에서 다른 세션이 동시에 작업 중 -> 분리가 타당. 확인만 받는다.
    if active:
        respond(
            "ask",
            (
                f"{origin}\n"
                + tr(
                    "Another Claude session is actively working in this tree, so a worktree "
                    "split looks justified. Worktree creation still needs the user's confirmation.\n",
                    "이 작업 트리에서 다른 Claude 세션이 동시에 작업 중이라 worktree 분리가 "
                    "타당해 보입니다. 다만 룰상 worktree 생성은 사용자 확인이 필요합니다.\n",
                )
                + f"{fmt_sessions(active)}\n"
                + f"{fmt_snippet(top or cwd, session_id)}\n"
                + tr("Confirm to proceed.", "진행할지 확인해 주세요.")
            ),
        )

    # 1-b) 살아 있긴 하나 한동안 입력이 없는 세션뿐 -> 잊힌 탭일 가능성. 사용자가 안다.
    if idle:
        respond(
            "ask",
            (
                f"{origin}\n"
                + tr(
                    f"The only other sessions here have shown no activity (input or transcript) "
                    f"for {IDLE_MIN}+ minutes — if they are forgotten tabs this is effectively "
                    f"single-stream work and plain `git switch` beats a worktree.\n",
                    f"이 트리의 다른 세션은 {IDLE_MIN}분 이상 활동(키 입력·작업 기록)이 없는 것뿐입니다 — "
                    f"잊힌 탭이면 사실상 단건 작업이라 worktree 없이 `git switch` 가 낫습니다.\n",
                )
                + f"{fmt_sessions(idle)}\n"
                + f"{fmt_snippet(top or cwd, session_id)}\n"
                + tr(
                    "Still split into a worktree?",
                    "그래도 worktree 로 분리할지 확인해 주세요.",
                )
            ),
        )

    # 2) 동시 세션 판정 불가 -> 자동으로 만들지 말고 물어본다.
    if not reliable:
        respond(
            "ask",
            (
                f"{origin}\n"
                + tr(
                    "Cannot determine whether other sessions are working here (ps/lsof "
                    "unavailable), so no automatic verdict.\n"
                    "Confirm if this really is concurrent work; if single-stream, cancel and "
                    "use `git switch`.",
                    "동시 세션 여부를 확인할 수 없어(ps/lsof 사용 불가) 자동 판정을 못 합니다.\n"
                    "정말 동시 작업이면 확인해 주시고, 단건이면 취소하고 `git switch` 로 진행하세요.",
                )
            ),
        )

    # 3) 단건 작업 -> 원칙은 worktree 금지. 사용자가 명시한 경우만 확인으로 낮춘다.
    if user_ok:
        respond(
            "ask",
            (
                f"{origin}\n"
                + tr(
                    "Single-stream work, but [worktree-ok] was given — treating this as the "
                    "user's explicit intent. Confirm the worktree creation.",
                    "단건 작업이지만 [worktree-ok] 가 지정되어 사용자 의사로 판단합니다. "
                    "worktree 를 생성할지 확인해 주세요.",
                )
            ),
        )
    respond(
        "deny",
        (
            f"{origin}\n"
            + tr(
                "No other session is working in this tree (= single-stream). Rule: for "
                "single-stream work, don't create a worktree — just switch branches in the "
                "shared tree. Everything stays visible in one editor window, and half-used "
                "worktree folders don't pile up.\n\n",
                "이 트리에서 동시에 작업 중인 다른 세션이 없습니다(= 단건 작업). "
                "룰: 단건이면 worktree를 만들지 말고 공유 트리에서 브랜치만 갈아끼웁니다 "
                "— 에디터 한 창에서 다 보여 코드 파악이 빠르고, 쓰다 만 worktree 폴더가 "
                "쌓이지 않습니다.\n\n",
            )
            + steer_to_switch()
        ),
    )


def main():
    data = load_input()
    tool = data.get("tool_name", "")
    cwd = data.get("cwd") or os.getcwd()
    tool_input = data.get("tool_input", {}) or {}

    # 하네스가 관리하는 worktree(Agent/Task `isolation: "worktree"`)는 Bash를 거치지
    # 않고 <repo>/.claude/worktrees/<name> 에 바로 생성되므로 툴 호출에서 잡는다.
    if tool in ("Agent", "Task"):
        if str(tool_input.get("isolation", "")).lower() != "worktree":
            sys.exit(0)
        top, _ = repo_paths(cwd)
        guard_worktree_creation(
            top,
            cwd,
            tr(
                'The Agent tool was called with isolation: "worktree" (the harness creates a '
                "worktree at <repo>/.claude/worktrees/<name>). Re-invoking without isolation "
                "proceeds in the shared tree.",
                'Agent 툴을 isolation: "worktree" 로 호출했습니다 '
                "(하네스가 <repo>/.claude/worktrees/<name> 에 worktree를 만듭니다). "
                "isolation 없이 다시 호출하면 공유 트리에서 그대로 진행됩니다.",
            ),
            user_ok=False,
            session_id=data.get("session_id", ""),
        )
        sys.exit(0)

    if tool != "Bash":
        sys.exit(0)
    command = tool_input.get("command", "") or ""

    reason = None
    for seg in split_segments(command):
        reason = classify(seg, cwd)
        if reason:
            break
    if not reason:
        sys.exit(0)

    top, wt_root = repo_paths(cwd)

    if reason == "worktree-add":
        guard_worktree_creation(
            top,
            cwd,
            tr(
                "Attempting to create a worktree with `git worktree add`.",
                "`git worktree add` 로 worktree를 만들려 합니다.",
            ),
            user_ok="[worktree-ok]" in command,
            session_id=data.get("session_id", ""),
        )
        sys.exit(0)

    active, idle, reliable = sessions_in_tree(top or cwd, data.get("session_id", ""))

    steer = tr(
        f"  # check an existing branch out into a worktree\n"
        f"  git worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # or create a new branch off the latest origin/main\n"
        f"  git fetch origin\n"
        f"  git worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
        "Then work in that folder from a separate Claude Code session. "
        "`git worktree list` shows worktrees.",
        f"  # 기존 브랜치를 worktree로 꺼내기\n"
        f"  git worktree add {wt_root}/<branch> <branch>\n\n"
        f"  # 새 브랜치를 최신 origin/main 기준으로 생성 (저장소 정책)\n"
        f"  git fetch origin\n"
        f"  git worktree add {wt_root}/<name> -b <branch> origin/main\n\n"
        "그런 다음 그 폴더에서 별도의 Claude Code 세션으로 작업하세요. "
        "worktree 목록은 `git worktree list`.",
    )

    # 1) 같은 작업 트리에서 다른 세션이 '지금' 일하는 중 -> 진짜 다중작업. 차단.
    if active:
        respond(
            "deny",
            (
                tr(
                    "Blocking this branch switch: another Claude session is actively working in "
                    "this tree (switching would land its next edits on an unintended branch).\n",
                    "이 작업 트리에서 다른 Claude 세션이 동시에 작업 중이라 브랜치 전환을 차단합니다 "
                    "(전환하면 상대 세션의 다음 편집이 의도치 않은 브랜치에 떨어집니다).\n",
                )
                + f"{fmt_sessions(active)}\n"
                + f"{fmt_snippet(top or cwd, data.get('session_id', ''))}\n"
                + tr(
                    "This is concurrent work — take this branch to a separate worktree:\n\n",
                    "다중작업이므로 이 브랜치는 별도 worktree에서 진행하세요:\n\n",
                )
                + steer
            ),
        )

    # 1-b) 살아 있으나 입력이 끊긴 세션뿐 -> 잊힌 탭일 공산. 차단 대신 사용자 판단.
    if idle:
        respond(
            "ask",
            (
                tr(
                    f"Other Claude sessions exist in this tree but have shown no activity (input "
                    f"or transcript) for {IDLE_MIN}+ minutes — if they are forgotten tabs, "
                    f"switching is fine.\n",
                    f"이 트리에 다른 Claude 세션이 있지만 {IDLE_MIN}분 이상 활동(키 입력·작업 기록)이 없습니다 — "
                    f"잊힌 탭이면 그대로 전환해도 됩니다.\n",
                )
                + f"{fmt_sessions(idle)}\n"
                + f"{fmt_snippet(top or cwd, data.get('session_id', ''))}\n"
                + tr(
                    "If you'll keep working in that session, don't switch — split into a "
                    "worktree instead:\n\n",
                    "그 세션에서 계속 작업할 것이라면 전환하지 말고 worktree 로 분리하세요:\n\n",
                )
                + steer
            ),
        )

    # 2) 세션 감지 자체가 불가능하면 사용자에게 확인. deny 였으나 확장 호스트처럼
    #    조상 프로세스가 `claude` 로 보이지 않는 환경에서 모든 전환이 막혔다 —
    #    판정 불가의 비용은 사용자가 한 번 확인하는 것으로 충분하다.
    if not reliable:
        respond(
            "ask",
            (
                tr(
                    "Cannot determine whether other sessions are working in this tree "
                    "(process inspection unavailable in this environment). Your call:\n"
                    "  · Approve — switch branches in this shared tree (safe when no "
                    "other session is active here).\n"
                    "  · Deny — the switch is cancelled; split into a worktree instead "
                    "so any concurrent session keeps its branch:\n\n",
                    "이 트리에서 다른 세션이 작업 중인지 확인할 수 없습니다(이 환경에서는 "
                    "프로세스 조회가 불가능합니다). 선택해 주세요:\n"
                    "  · 승인 — 이 공용 트리에서 그대로 브랜치를 전환합니다(다른 활성 세션이 "
                    "없다면 안전합니다).\n"
                    "  · 거부 — 전환을 취소하고 worktree 로 분리해, 동시 세션의 브랜치를 "
                    "보존합니다:\n\n",
                )
                + steer
            ),
        )

    # 3) 단건이지만 추적 중인 변경이 있으면 사용자에게 확인.
    entries = tracked_changes(cwd)
    if entries:
        listing = "\n".join(f"    {xy}  {path}" for xy, path in entries)
        phantoms = phantom_entries(entries, cwd)
        note = ""
        if phantoms:
            why = "\n".join(f"    {p} — {r}" for p, r in phantoms)
            fixes = "\n".join(
                f"    git restore --staged {shlex.quote(p)}" for p, _ in phantoms
            )
            note = tr(
                f"\nIndex-only residue invisible in the working tree:\n{why}\n"
                f"These commands clean the tree (run `git restore <path>` first to keep "
                f"index-only content):\n{fixes}\n",
                f"\n이 중 워크트리에서는 보이지 않는 index 잔재:\n{why}\n"
                f"아래 명령으로 정리하면 트리가 clean이 됩니다 "
                f"(index에만 존재하는 내용을 살리려면 `git restore <path>` 를 먼저 실행):\n{fixes}\n",
            )
        respond(
            "ask",
            (
                tr(
                    f"Single-stream tree, so the switch is allowed — but there are "
                    f"{len(entries)} uncommitted tracked changes:\n{listing}\n{note}"
                    f"They will follow you onto the target branch. Confirm to proceed "
                    f"(commit/stash first is recommended).",
                    f"이 트리는 단건 작업이라 브랜치 전환을 허용할 수 있지만, "
                    f"커밋되지 않은 변경 {len(entries)}건이 있습니다:\n{listing}\n{note}"
                    f"전환하면 이 변경이 대상 브랜치로 따라갑니다. 진행할지 확인해 주세요 "
                    f"(커밋/스태시 후 전환을 권장).",
                )
            ),
        )

    # 4) 단건 + clean -> 워크트리 없이 그냥 전환.
    sys.exit(0)


if __name__ == "__main__":
    main()
