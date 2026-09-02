### Fixed

- The evidence-ci guard test resolves the interpreter on Windows: the bash
  step quoted `sys.executable` with backslashes, so the step failed before
  its guard ran and the Windows CI leg has been red since the test landed.
  (`1788276387-the-windows-step-never-reaches-its-guard`)
