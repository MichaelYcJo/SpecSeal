- **A repository can say what language its pull requests are written in,
  and the skill reads that instead of requiring English of everyone.** The
  new `seal/config.md` holds one markdown table in the shape `parity.md`
  already uses, and its first row is `Pull request language`. Where that row
  names a language, `commit-pr-convention` writes the commit subject, the
  commit body, the pull request title and the pull request body in it — all
  four, because a squash makes them one text. **No file and no row both mean
  English**, so a repository that says nothing behaves exactly as it did
  before, and nothing is created for it: the file is written by a repository
  that wants a non-default, from the new `templates/config.md`. The root is
  resolved the two-place way, `<repo>/seal/` then
  `$(git rev-parse --git-common-dir)/seal/`, so local mode carries a config
  too.
  **Three things the row deliberately does not reach**, stated in the skill
  and again in the template, because the person writing the config reads the
  second and never the first: the prefix vocabulary is not translated
  (`feat:` stays `feat:` — it is scanned in a log and parsed by tooling);
  branch names stay ASCII, since a branch name is typed into a shell and
  pasted into a URL; and the response language, what the session says to
  you, remains a person's own setting, because two people in one repository
  can want different answers there and the same one here.
  The translated body is now named for **its own** language rather than the
  body's — `pr.<lang>.md`, so an English repository keeps `pr.ko.md` and a
  Korean one keeps `pr.en.md`. Nothing in this repository is renamed: the
  name was under-specified rather than wrong.
  Nothing in `hooks/` reads the file, and that is a decision rather than an
  omission: judging what language a commit message is in means being wrong
  about names, identifiers and quoted English, and a gate that guesses stops
  a correct commit. The mechanism is the skill's text, as it already is for
  the prefix vocabulary.
