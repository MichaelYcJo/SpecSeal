### Fixed

- The commit gate no longer refuses a whole Bash call for a here-document
  body that only mentions a commit, where nothing on the line can run that
  body (#739). Writing a pull request body with `cat > pr.md <<'EOF'` and
  handing it to `gh pr edit`, or patching a file with `python3 - <<'EOF'`,
  used to stop with the text for a command the gate cannot place whenever
  the body named a commit; a real commit after such a body is now judged in
  the repository it lands in. The body must sit behind a quoted delimiter,
  be fed to `cat`, `tee` or a Python program read from stdin, and stand on a
  line of plain commands where every delimiter is quoted and nothing can run
  a file it was written to. Every other body is read as before: any body on
  a line holding an unquoted delimiter, a shell or any other program fed the
  body, a body inside `$( … )`, and a file written beside `git`, a Python
  program or a `gh` subcommand that runs local git.
  The paragraph of `docs/commit-review-gate-spec.md` opening **A
  here-document body nothing can run is data** states the rule, and the
  agent contract's §9 says it to every agent.
