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
With no key or no directory the module registers nothing and changes nothing.

What it writes. One JSON Lines file, `<dir>/<key>-<pid>.jsonl`, UTF-8, one
object per line with a `kind`:

  session   key, pid, rootdir, invocation_dir (absolute), pytest's version
  test      nodeid, when, outcome, wasxfail where set, path (absolute)
  collect   a failed collection: nodeid, outcome "failed", path (absolute)
  end       exitstatus -- for the person reading the kept file only

A path is the rootdir joined to `report.fspath`, the node id's path: the
module that COLLECTED the test, relative to the rootdir on a plain run and on
an xdist controller alike. Never `report.location[0]`, which names the module
that DEFINES the test function, so a test a module inherits or imports from
another would be written under the other module, and the gate would give a
file the base passes `failing on base too` (#825 phase 4, the regression
corpus's N1). Each line is flushed as it is written, so a crash leaves what
ran.

It never prints, never changes an outcome and never raises out of a hook: a
directory it cannot write is one warning and no record, which the gate reads
as no record -- the strict side.

It runs in the ROW's interpreter, whose version the gate does not know, so it
is written for Python 3.8 syntax and reads only names pytest has had since
6.1 (`config.rootpath`; `config.invocation_params` since 5.1; `fspath` and
`pytest_collectreport` older). Measured on pytest 7.4, 8.0, 8.1
and 9.1, with pytest-xdist 3.8 under `-n 2` on the last: the `-p` in
`PYTEST_ADDOPTS` loads it on each, and an xdist controller receives every
worker's test and failed-collection reports (`phases/phase-1.md` of work item
1791270161 holds the builds and the commands).
"""

import json
import os
import warnings

KEY_VARIABLE = "SPECSEAL_RECORD_KEY"
DIR_VARIABLE = "SPECSEAL_RECORD_DIR"

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


class Recorder:
    """The one session of this process that claimed the key."""

    def __init__(self, key, directory, config):
        self.key = key
        self.directory = directory
        self.config = config
        self.rootdir = _rootdir(config)
        self.stream = None

    def absolute(self, relative):
        return os.path.normpath(os.path.join(self.rootdir, str(relative)))

    def write(self, line):
        if self.stream is None:
            return
        try:
            self.stream.write(json.dumps(line) + "\n")
            self.stream.flush()
        except (OSError, ValueError) as error:
            self.give_up(error)

    def give_up(self, error):
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
        try:
            # Held open across hooks and closed at `pytest_sessionfinish`, so
            # no `with` block can own it.
            self.stream = open(  # noqa: SIM115
                os.path.join(self.directory, name), "w", encoding="utf-8"
            )
        except OSError as error:
            self.give_up(error)
            return
        import pytest

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
        line = {
            "kind": "test",
            "nodeid": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "path": self.absolute(report.fspath),
        }
        if hasattr(report, "wasxfail"):
            line["wasxfail"] = str(report.wasxfail)
        self.write(line)

    def pytest_collectreport(self, report):
        if not report.failed:
            return
        self.write(
            {
                "kind": "collect",
                "nodeid": report.nodeid,
                "outcome": "failed",
                "path": self.absolute(report.fspath),
            }
        )

    def pytest_sessionfinish(self, session, exitstatus):
        self.write({"kind": "end", "exitstatus": int(exitstatus)})
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
