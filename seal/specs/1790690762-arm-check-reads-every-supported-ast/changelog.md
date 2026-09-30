### Fixed

- **`arm-check` reads a module holding a t-string on Python 3.14.** It used to
  refuse the file, naming `TemplateStr`. An interpolation's arms are now
  counted exactly as an f-string's are. Its node-type tables are checked on
  every Python from 3.12 to 3.14, so a table that is right for one interpreter
  and wrong for another no longer passes unnoticed (#684).
