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

That holds only where pytest names a file against the rootdir, which it does
for every file under it by its own lexical rule. A file outside the rootdir
is named against the argument that reached it, so the node id's path joined
to the rootdir names a file that is not the test's, and two files under two
arguments can share one name. A session in which pytest would name any
argument outside its rootdir -- a path outside it, `-c` or `--rootdir`
elsewhere or spelled through a symlink, a config file in one argument's
directory, a `--pyargs` module Python imports from outside it -- therefore
writes no record at all: the strict side (#825 rounds 1 and 2). The one
way past this the arguments cannot show is a collector a conftest or a plugin
builds for a path no argument contains: pytest gives its tests the parent's
node id and a `::` name, whose path is no file, so a test line whose path is
no file abandons the whole record (#825 round 2).

It never changes an outcome and never raises out of a hook: a directory it
cannot write is one warning, shown under the recorder's own filter so that a
run with warnings as errors does not raise it (#825 round 1), and no record,
which the gate reads as no record -- the strict side.

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
        self.file = None

    def absolute(self, relative):
        return os.path.normpath(os.path.join(self.rootdir, str(relative)))

    def write(self, line):
        if self.stream is None:
            return
        kind, path = line.get("kind"), line.get("path")
        empty = os.path.normpath(str(path)) == os.path.normpath(self.rootdir)
        if (kind == "test" and not os.path.isfile(path)) or (
            kind == "collect" and empty
        ):
            # pytest gives a test the node id of its module's file. Where the
            # module lies outside the rootdir and is itself the argument that
            # reached it, that node id's path is empty and names the rootdir;
            # where a collector a conftest or a plugin built for a path no
            # argument contains holds it, the node id is the parent's and a
            # `::` name. Either way the path is no test file, and a failed
            # collection's carries no test line to show it but the rootdir
            # itself. The whole record is abandoned, the strict side (#825
            # round 2).
            stream, self.stream = self.stream, None
            try:
                stream.close()
                os.remove(self.file)
            except (OSError, ValueError):
                pass
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

    def an_argument_lies_outside_the_rootdir(self):
        """Whether pytest was handed a path outside its rootdir, by pytest's
        own rule: lexical, as its `absolutepath` and `relative_to` are, never
        through a symlink. pytest names a file there against the argument
        that reached it, not against the rootdir, so its node id's path
        joined to the rootdir can name another file (#825 rounds 1 and 2).

        A `--pyargs` package is a directory whose modules pytest names
        against it, so it is located where pytest's `search_pypath` finds
        it: the package's directory, or under `consider_namespace_packages`
        its first search location. An argument whose node id's path is
        EMPTY -- a module or a file handed by itself, `::` selection or not,
        a plain `--pyargs` module -- names the rootdir itself, which is no
        test file, and `write` abandons that record, so nothing here reads
        it. An argument that is no path and no module pytest can find is
        passed over: pytest stops on it with a usage error."""
        root = os.path.abspath(self.rootdir)
        here = _invocation_dir(self.config)
        option = getattr(self.config, "option", None)
        pyargs = bool(getattr(option, "pyargs", False))
        namespaces = False
        if pyargs:
            try:
                namespaces = bool(self.config.getini("consider_namespace_packages"))
            except (KeyError, ValueError):
                namespaces = False
        for argument in getattr(self.config, "args", None) or ():
            name = str(argument)
            located = None
            if pyargs:
                # `find_spec` imports a dotted name's parent packages, which
                # pytest's own collection does next.
                import importlib.util

                try:
                    spec = importlib.util.find_spec(name)
                except Exception:
                    spec = None
                places = list(getattr(spec, "submodule_search_locations", None) or ())
                if places and namespaces:
                    located = places[0]
                elif places and spec.origin not in (None, "namespace"):
                    located = os.path.dirname(spec.origin)
            path = os.path.abspath(os.path.join(here, located or name))
            if not os.path.exists(path):
                continue
            try:
                inside = os.path.commonpath([root, path]) == root
            except ValueError:
                inside = False
            if not inside:
                return True
        return False

    def pytest_sessionstart(self, session):
        if self.an_argument_lies_outside_the_rootdir():
            return
        name = f"{self.key}-{os.getpid()}.jsonl"
        self.file = os.path.join(self.directory, name)
        try:
            # Held open across hooks and closed at `pytest_sessionfinish`, so
            # no `with` block can own it.
            self.stream = open(self.file, "w", encoding="utf-8")  # noqa: SIM115
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
