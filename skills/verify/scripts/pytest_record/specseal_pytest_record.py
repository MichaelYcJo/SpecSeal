"""The broad gate's recorder: what this pytest process ran, written down by it.

#825. The broad gate used to infer which pytest run printed a line from the
row's text and from what pytest printed. This module ends the inference: the
gate loads it into every run it measures, and the pytest process that
collected a test is the process that writes that test's outcome down.

How it is loaded. The gate prepends this module's directory -- which holds
nothing else, so the row's interpreter is shown nothing else of the plugin's
-- to `PYTHONPATH`, appends ` -p specseal_pytest_record` to `PYTEST_ADDOPTS`,
and sets two variables:

  SPECSEAL_RECORD_DIR   the absolute directory the record goes in
  SPECSEAL_RECORD_KEY   a token the gate makes fresh for each run it measures

Which process records. At import the key is taken OUT of `os.environ`, so a
pytest this process starts in turn -- one a test spawns, an xdist worker --
inherits an environment with no key and records nothing. Within the process,
the first session configured claims the key and clears it, so a second
session (an in-process `pytest.main` a test calls) records nothing either.
With no key or no directory no session records and nothing is written.

What it writes. One JSON Lines file, `<dir>/<key>-<pid>.jsonl`, UTF-8, one
object per line with a `kind`:

  session   key, pid, rootdir, invocation_dir (absolute), pytest's version
  test      nodeid, when, outcome, wasxfail where set, path (absolute), and
            category: the word pytest's own summary counts the report under
  collect   a failed or a skipped collection: nodeid, outcome "failed" or
            "skipped", path (absolute)
  end       exitstatus; unplaced: how many tests and collections were
            written as no line because they had no file of their own; and
            stopped: what stopped the session before its end, a list
            empty where nothing did

A `test` line's `category` is the first element of what pytest's
`pytest_report_teststatus` hook returns for that report, asked with the
report and the config exactly as pytest's terminal reporter asks it before
counting the report on its summary line (#869): `passed`, `failed`,
`skipped`, `xfailed`, `xpassed`, `error` for a failed setup or teardown,
`""` for a report pytest counts nowhere, and whatever word a plugin's own
implementation of the hook gives. The recorder copies no rule of pytest's;
it asks the one judgment pytest's own line is made from. A failed
collection is what that line counts as an `error`, and a skipped one -- a
module that calls `pytest.skip(allow_module_level=True)` -- as a `skipped`.
Neither `deselected` nor `warnings` is a report's category, and neither is
written.

The `end` line's `stopped` holds one entry per thing pytest says stopped the
session, each `{"by": <by>, "what": <text pytest gave>}` (#852):

  interrupt   pytest called `pytest_keyboard_interrupt`: a `KeyboardInterrupt`
              in a test, or the run loop's `Interrupted` -- a failed
              collection without `-x`, a stop a plugin asked for
  exit        the same hook for `pytest.exit()`, whatever return code it
              chose; `what` carries its message and its return code
  failures    `session.shouldfail` was set: `-x` or `--maxfail` stopped it
  stop        `session.shouldstop` was set: a plugin stopped it, as
              `--stepwise` does

The last two are read off the session at `pytest_sessionfinish`, where
pytest's own setters have left them: neither can be unset once set. A stop
no hook shows -- an internal error, a usage error, a `pytest.exit()` in an
xdist worker, which reaches the controller as an internal error -- still
shows in `exitstatus`, and the gate reads both. One stop shows in neither:
a `pytest.exit()` raised by a `pytest_sessionfinish` hook that runs after
this one is raised after the `end` line was written.

A line's path is the node's own: `item.path` for a test, the module that
COLLECTED it, and `collector.path` for a failed collection, `fspath` below
pytest 7. Two hookwrappers, on the hooks that make a test report and a
collect report, read it where pytest holds the node and set it on the
report; the recording process reads it off the report. Under xdist the node
is on a worker and the recorder on the controller, and a report carries
every attribute in its `__dict__` across (#825's reframe after round 3,
`questions.md` Q-M3 of work item 1791270161). No path is ever made from a
node id and a rootdir: pytest makes the node id FROM the path, by a rule
with more branches than three review rounds of #825 could enumerate, so a
file outside the rootdir, a `--pyargs` module wherever Python imports it
from and a collector a conftest builds are each named by their own path.
Never `report.location[0]` either, which names the module that DEFINES the
test function (#825 phase 4). Each line is flushed as it is written, so a
crash leaves what ran.

What it leaves out, and counts. A test whose node's path is a directory --
an item a conftest or a plugin parents to the session or to a directory --
has no file of its own; a failed collection of the session itself -- where
pytest 7 lays a conftest's import error anywhere below the root, and where a
plugin's hook can on any build -- names the rootdir, which is no file of the
tree's; and a report that reaches the recorder without the path -- one a
plugin built or rebuilt itself -- names none, unless the same xdist
worker's last report was of the same node and not its teardown, as the
`setup` report of a test whose worker then crashed is. None of the
three is written; each node is counted once on the `end` line, and the gate
says the count under its list of failing files. A file that is gone is
still named: a module that removes its own file while it runs keeps its
failing line.

It never changes an outcome, never raises out of a hook, and runs none of
the row's code: it looks no module up and imports nothing but pytest. A
directory it cannot write is one warning, shown under the recorder's own
filter so that a run with warnings as errors does not raise it (#825 round
1), and no record, which the gate reads as no record -- the strict side.

It runs in the ROW's interpreter, whose version the gate does not know, so it
is written for Python 3.8 syntax and reads only names pytest has had since
6.1 (`config.rootpath`; `config.invocation_params` since 5.1; `item.path`
since 7.0, `fspath` before; `pytest_collectreport`,
`pytest_report_teststatus`, `pytest_keyboard_interrupt`,
`session.shouldfail`, `session.shouldstop` and the old-style
`hookwrapper=True` older). Measured on pytest 7.4, 8.0, 8.1 and 9.1, plain
and with pytest-xdist 3.8 under `-n 2` on each: the `-p` in `PYTEST_ADDOPTS`
loads it, an xdist controller receives every worker's test and
failed-collection reports, and the path a worker sets on a report reaches
the controller (`phases/phase-1.md` and `phases/phase-5.md` of work item
1791270161 hold the builds and the commands). The category, the skipped
collection and every stop above were measured on pytest 6.1, 7.0 and 9.1,
and on 9.1 with pytest-xdist 3.8 under `-n 2` (`phases/phase-1.md` of work
item 1791384158).
"""

import json
import os
import warnings

import pytest

KEY_VARIABLE = "SPECSEAL_RECORD_KEY"
DIR_VARIABLE = "SPECSEAL_RECORD_DIR"
# The attribute the two hookwrappers set on a report: the node's own path.
# The recorder's own name, so no field pytest or another plugin reads moves.
# A plugin that writes a report whole writes it too: pytest-reportlog's
# `--report-log` writes what `pytest_report_to_serializable` returns, so a
# row's report log gains this key while the gate measures it (#825 round 4).
PATH_ATTRIBUTE = "specseal_path"

# Taken out at import, before any test of this process can read it, and
# before any child process can inherit it.
_unclaimed_key = os.environ.pop(KEY_VARIABLE, None)
_directory = os.environ.get(DIR_VARIABLE)


def _rootdir(config):
    rootpath = getattr(config, "rootpath", None)
    if rootpath is None:
        rootpath = config.rootdir
    return str(rootpath)


def _invocation_dir(config):
    params = getattr(config, "invocation_params", None)
    if params is None:
        return os.getcwd()
    return str(params.dir)


def _node_path(node):
    path = getattr(node, "path", None)
    if path is None:
        path = getattr(node, "fspath", None)
    return None if path is None else str(path)


def _carry_the_path(outcome, node):
    """Set `node`'s own path on the report the wrapped hook made. Where that
    hook raised there is no report, and pytest's own error stands: read
    again here it would be raised from this frame, which pluggy reports as
    this plugin's teardown failing."""
    try:
        report = outcome.get_result()
    except BaseException:
        return
    setattr(report, PATH_ATTRIBUTE, _node_path(node))


# Module-level, so they run in every process that loaded the module -- an
# xdist worker, which registers no `Recorder`, included: the worker holds the
# node, and the report carries the path to the controller that records.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    _carry_the_path(outcome, item)


@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    outcome = yield
    # The session's own collection is no file's and no directory's: pytest 7
    # lays a conftest's import error anywhere below the root there, and a
    # plugin's hook can on any build, so two different breakages would share
    # the rootdir's word (#825 round 4). Its report carries no path, and a
    # failed one is counted on the `end` line, never written.
    if collector is getattr(collector, "session", None):
        return
    _carry_the_path(outcome, collector)


class Recorder:
    """The one session of this process that claimed the key."""

    def __init__(self, key, directory, config):
        self.key = key
        self.directory = directory
        self.config = config
        self.rootdir = _rootdir(config)
        self.stream = None
        self.file = None
        self.unplaced = set()
        self.last_sent = {}
        self.stops = []

    def path_of(self, report, kind):
        """The path the report carries, or None where it carries none, or
        where a test's is a directory: neither is a file of its own, and the
        node is counted rather than written.

        A report built outside the two hooks carries no path -- xdist builds
        one on the controller for a test whose worker crashed
        (`DSession.handle_crashitem`), and sets `report.node` to that worker,
        as it does on every report it forwards. A worker runs one test at a
        time, so where the last report the same worker sent was of the same
        node and was not its teardown, the crash is that node's and that
        report's path is used (#825 round 4). Never a lookup by node id
        alone: two nodes can share one -- pytest 7 names a file outside the
        rootdir from the argument it came from -- and round 4's lookup by id
        wrote the crash under the other node's file (#825 round 5).

        The map is keyed on the worker's `id()` and holds the worker in the
        value, so a worker xdist makes to replace a crashed one cannot take
        the freed one's address and its last report with it (#849). Nothing
        is asked of the worker but its identity -- no hash and no equality,
        either of which a `node` could raise from or share with another --
        so any `node` is a sender and nothing raises (#849 round 1)."""
        path = getattr(report, PATH_ATTRIBUTE, None)
        sender = getattr(report, "node", None)
        if isinstance(path, str):
            if sender is not None:
                when = getattr(report, "when", None)
                self.last_sent[id(sender)] = (sender, report.nodeid, when, path)
        elif sender is not None:
            last = self.last_sent.get(id(sender), (None, None, None, None))
            if last[1] == report.nodeid and last[2] != "teardown":
                path = last[3]
        if not isinstance(path, str) or (kind == "test" and os.path.isdir(path)):
            self.unplaced.add((kind, report.nodeid))
            return None
        return path

    def write(self, line):
        if self.stream is None:
            return
        try:
            self.stream.write(json.dumps(line) + "\n")
            self.stream.flush()
        except (OSError, ValueError) as error:
            self.give_up(error)

    def give_up(self, error):
        # Shown, never raised: a row run with warnings as errors (`python -W
        # error`, `filterwarnings = error`) would otherwise turn this one
        # warning into an exception out of a hook, and pytest would end in
        # INTERNALERROR with the suite's own result lost (#825 round 1).
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            warnings.warn(
                f"specseal_pytest_record: no record written: {error}", stacklevel=2
            )
        stream, self.stream = self.stream, None
        if stream is not None:
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def pytest_sessionstart(self, session):
        name = f"{self.key}-{os.getpid()}.jsonl"
        self.file = os.path.join(self.directory, name)
        try:
            # Held open across hooks and closed at `pytest_sessionfinish`, so
            # no `with` block can own it.
            self.stream = open(self.file, "w", encoding="utf-8")  # noqa: SIM115
        except OSError as error:
            self.give_up(error)
            return
        self.write(
            {
                "kind": "session",
                "key": self.key,
                "pid": os.getpid(),
                "rootdir": self.rootdir,
                "invocation_dir": _invocation_dir(self.config),
                "pytest": getattr(pytest, "__version__", ""),
            }
        )

    def pytest_runtest_logreport(self, report):
        path = self.path_of(report, "test")
        if path is None:
            return
        line = {
            "kind": "test",
            "nodeid": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "path": path,
        }
        if hasattr(report, "wasxfail"):
            line["wasxfail"] = str(report.wasxfail)
        line["category"] = self.category_of(report)
        self.write(line)

    def category_of(self, report):
        """The word pytest's summary line counts `report` under: the first
        element of the teststatus hook's answer, asked the way the terminal
        reporter asks it. None where the hook answered nothing a word can be
        read from, or raised -- the terminal reporter would then have raised
        first, and this hook raises nothing out."""
        try:
            status = self.config.hook.pytest_report_teststatus(
                report=report, config=self.config
            )
        except Exception:
            return None
        if not isinstance(status, (tuple, list)) or not status:
            return None
        category = status[0]
        return category if isinstance(category, str) else None

    def pytest_collectreport(self, report):
        if report.failed:
            outcome = "failed"
        elif report.skipped:
            outcome = "skipped"
        else:
            return
        path = self.path_of(report, "collect")
        if path is None:
            return
        self.write(
            {
                "kind": "collect",
                "nodeid": report.nodeid,
                "outcome": outcome,
                "path": path,
            }
        )

    def pytest_keyboard_interrupt(self, excinfo):
        """pytest calls this for a `KeyboardInterrupt`, for the run loop's
        `Interrupted` and for `pytest.exit()`, before `pytest_sessionfinish`
        (`wrap_session`). Remembered here and written on the `end` line."""
        value = getattr(excinfo, "value", None)
        name = type(value).__name__
        exit_type = getattr(pytest.exit, "Exception", None)
        if exit_type is not None and isinstance(value, exit_type):
            message = getattr(value, "msg", None)
            if message is None:
                message = str(value)
            code = getattr(value, "returncode", None)
            what = f"{name}: {message} (returncode {code})"
            self.stops.append({"by": "exit", "what": what})
            return
        said = str(value)
        self.stops.append(
            {"by": "interrupt", "what": f"{name}: {said}" if said else name}
        )

    def stopped(self, session):
        """Every stop pytest showed this session, in the order it showed
        them: what the keyboard-interrupt hook was handed, then the two
        flags pytest's own stops set and never unset."""
        stops = list(self.stops)
        for by, flag in (("failures", "shouldfail"), ("stop", "shouldstop")):
            value = getattr(session, flag, False)
            if value:
                stops.append(
                    {"by": by, "what": value if isinstance(value, str) else str(value)}
                )
        return stops

    def pytest_sessionfinish(self, session, exitstatus):
        self.write(
            {
                "kind": "end",
                "exitstatus": int(exitstatus),
                "unplaced": len(self.unplaced),
                "stopped": self.stopped(session),
            }
        )
        stream, self.stream = self.stream, None
        if stream is not None:
            try:
                stream.close()
            except (OSError, ValueError):
                pass


def pytest_configure(config):
    """Claim the key for the first session configured in this process."""
    global _unclaimed_key
    key, _unclaimed_key = _unclaimed_key, None
    if not key or not _directory:
        return
    config.pluginmanager.register(
        Recorder(key, _directory, config), "specseal_pytest_record_session"
    )
