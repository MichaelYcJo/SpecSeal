### Changed

- The GitHub Release note opens with a summary read from the release's pull
  requests (#572). An at-a-glance table counts the pull requests, the issues
  they closed and the outside contributors. Then comes one line per pull
  request under its conventional-commit type, with the issues it closed.
  After that, a `🙌 Thanks to` section credits each outside contributor by
  handle, and the note says how to update. The gathered changelog section
  follows in full, folded. Before, the note was that section alone, one
  paragraph of reasoning per change. Every summary line is a pull request
  title, a number or a handle, so a pull request title is now a line of the
  release note. A note whose pull requests cannot be listed is published as
  the section alone, and the tag's job does not fail.
