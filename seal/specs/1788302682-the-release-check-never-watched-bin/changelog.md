- **The release check watches `bin/` now, and a test says which roots it
  watches.** The hygiene step that asks a pull request into `main` for a
  version bump filtered the diff through five roots — `skills/`, `agents/`,
  `hooks/`, `templates/`, `.claude-plugin/` — and `bin/` was not one of them,
  although the plugin loader puts `bin/` on the Bash tool's PATH while the
  plugin is enabled. A pull request fixing only a wrapper would have shipped
  without moving the version, which is the one way an update reaches nobody.
  `bin/` is in the pattern; `docs/branch-and-release.md` names it with the
  others; and `tests/test_the_release_check_watches_what_ships.py` classifies
  every tracked top-level entry as shipping or staying home, so the next
  `commands/` or `output-styles/` fails the suite until somebody decides,
  instead of falling out of the pattern the way `bin/` did. Nothing else that
  a user runs directly lives outside those roots: `install.sh` is run from a
  clone, never through the plugin. (#10)
