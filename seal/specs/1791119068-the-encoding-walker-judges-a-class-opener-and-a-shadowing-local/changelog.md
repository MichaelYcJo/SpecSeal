### Fixed

- The check that every file is read and written with a named encoding now
  reports `zipfile.Path.open(q, "r")` called on its class (#762). That call
  reads the member in the locale's encoding, cp1252 on the Windows leg, and
  it passed because the check took the path for the mode and `"r"` for an
  encoding. A method's argument positions are now read only where the shift
  for a call on the class is applied, and a test fails by name if a method's
  row is put where a function's belongs. `Traversable.read_text(t)`,
  from `importlib.resources.abc`, called on its class, passed the same way
  and is now reported too, and so is the same method called on
  `ResourceHandle` or `ResourceContainer`, which inherit it, and 3.12's
  `pipes.Template.open(t, f, "r")`, whose mode was read as an encoding.
- A local, a parameter or a loop variable that shares a module's name, such
  as `wave`, `tarfile` or `os`, no longer has its `.open()` excused for the
  spelling. Only a name the file imports is taken for the module, so a branch
  adding `def f(tarfile): return tarfile.open()` now fails every CI leg.
- Importing `dbm.gnu`, `dbm.ndbm`, `dbm.sqlite3`, `aifc`, `sunau`,
  `tokenize`, `posix`, `nt` or `ossaudiodev` and calling its `open` no
  longer fails the check. None of them takes the locale's encoding. The
  list was built by importing every standard-library module on 3.12 to
  3.14, and the modules that import only on Linux or Windows were read in
  their documentation.
