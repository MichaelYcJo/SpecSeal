### Fixed

- **`bin/test` runs the suite in parallel by default, in every environment
  it builds or adopts (#337).** The runner built its virtualenv with `pytest`
  alone, so `-n auto` failed on every fresh build and the runner withheld it,
  while CI ran the same suite `-n auto` on three platforms for every release.
  Now `pytest-xdist` is installed beside `pytest` on both build strategies,
  an adopted `.venv` that lacks it takes one install step by the same tool
  order (found by the filesystem, never a subprocess, so a warm call still
  runs no builder), and the command carries `-n auto` unless the caller
  passed `-n…`, `--numprocesses…`, `-p no:xdist` or `--pdb`. A failed install
  is one sentence — the package, that the run is serial, the remedy — and
  the suite still runs, with pytest's exit code. Measured on the 0.15.0 run
  (macOS, 10 logical CPUs, 2026-09-24): six sealer runs of the serial suite
  at about thirteen minutes each, against `4397 passed in 3m04s` for the
  same suite run `-n auto` by hand during the release preparation, which is
  the configuration that is now the default; a cold build of the parallel
  environment in a scratch clone took 1.6 s with `uv`'s cache warm and the
  warm call after it 0.9 s. The serial figure (*about five minutes*) is
  gone from `bin/test`, the runner, `CONTRIBUTING.md` §*Running the checks*
  and the test module, and `docs/release-checklist.md` §3's suite line is
  `bin/test -q` rather than a second spelling of the run.
