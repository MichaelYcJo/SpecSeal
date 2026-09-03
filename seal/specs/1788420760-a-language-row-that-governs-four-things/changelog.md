<!-- seal/specs/1788420760-a-language-row-that-governs-four-things/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A repository can say what language this plugin writes in, and it is two
  answers rather than one.** The row that shipped as `Pull request language`
  governed four things — the commit subject and body, the pull request title
  and body — and everything else this plugin wrote stayed English whatever it
  said. So a team working in Korean got Korean pull requests and English
  specifications, which is a pull-request setting wearing a language
  setting's name. It is now `Commit and pull request language`, which is what
  it always governed, and it takes the review report posted to a pull request
  with it. A second row, `Record language`, governs the prose in the
  work-item records: the specification, the plan, the memo, the questions,
  the changelog fragment, the round records' cells, and a ledger row's claim
  and grounds.
  **The two are independent.** Setting one does not carry the other, because
  an absent row's default is what every repository had before that row
  existed, and a row inheriting another's value is not that. Three
  combinations, which are the three people want: everything English, the
  commits and pull requests in the team's language with the documents in
  English, and both.
  **Prose follows the rows and structure does not.** What stays English in
  every repository, whatever either row says: the commit prefix vocabulary,
  branch names, all code, and every string a checker reads literally — a
  round record's field names, its verdict vocabulary and its `Pass` checkbox,
  the `<!-- -->` markers, a `drained` line, and a ledger anchor's
  `path#unit@hash`. A translated field name is not a translation; it is a
  checker that stops reading. (#106)
