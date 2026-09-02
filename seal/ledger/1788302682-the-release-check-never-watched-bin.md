# 1788302682-the-release-check-never-watched-bin

Rows for the work item that put `bin/` under the release check's eye and
pinned the list of roots it watches (issue #10).

## The release check watches every root that ships

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| A release pull request that changes `bin/` must move the version, because the loader puts `bin/` on the Bash tool's PATH while the plugin is enabled | `.github/workflows/hygiene.yml#"- name: a change to what ships must move the version"@2b250a60` | **Executed** — `tests/test_the_release_check_watches_what_ships.py::test_every_shipping_root_is_watched[bin]` reads the pattern out of the step and matches `bin/anything`; seen red against the five-root pattern before the fix, and red again with `bin` removed from the fixed pattern. The real engine agrees: `grep -E` with the step's pattern kept `bin/unverified-check` and dropped `docs/x.md` and `install.sh` | 2026-09-02 | That `bin/` ships: executed — this session's PATH carries the plugin cache's `bin/` and `command -v evidence-check` resolves into it; read — the Claude Code plugin reference's *File locations* row for `bin/`, and `README.md` §CLI |
| Every tracked top-level entry of the repository is classified as shipping or staying home, and an entry nobody has classified fails the suite | `tests/test_the_release_check_watches_what_ships.py#test_every_top_level_entry_is_classified@e3ed00ee` | **Executed** — dropping `evals` from `STAYS_HOME` turned the test red naming `['evals']`; `test_the_pattern_names_nothing_this_file_has_not_classified` holds the pattern to exactly the `SHIPS` set, so a root added to the workflow alone is red too | 2026-09-02 | The pattern is matched with Python's `re`, not by spawning `grep`: the suite runs on windows-latest |
