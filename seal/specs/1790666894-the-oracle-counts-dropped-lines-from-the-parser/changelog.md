### Fixed

- The suite's CommonMark oracle no longer reports a false disagreement with
  the hooks' walk on a paragraph that opens with a line of only a Unicode
  space and has a `>` indented four columns, or behind a tab, on a later line
  (#677). markdown-it-py's strip drops such an opening line, and the oracle
  counted the dropped lines back by reading container markers itself, so it
  took that `>` for a quote marker and placed inline HTML one line late. It
  now takes the count from the parser's own paragraph and setext-heading
  rules and reads no marker. Nothing a plugin user runs changes: the oracle
  is test code, and no hook reads it.
