<!-- seal/specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`broad-gate`'s refusal for a `Broad gate` line that will not parse said
  every row below it was lost without ever asking whether anything was below
  it** (#430). The sentence was computed from which line stopped the table
  reader, never from what anybody had written under that line. A `Broad gate`
  row written LAST in its table — the shape `seal/config.md` has in this
  repository, the shape the table `templates/config.md` ships has, and the
  shape the stub `seal mode` writes grows into — loses nothing with it, and
  the person holding that file was told to go looking for rows they had never
  written.

  - **Four sentences of that shape, not the one the ticket named.** The arm
    for a line nothing stopped the reader at, the arm for the line that
    stopped it, the arm for a line read with something lower down stopping the
    reader, and the hidden-row refusal, where this gate's row can be the one
    and only row under the stopping line and there is then no *other* one. Each
    now has a subject in every state it can be reached in, and each shipped
    with a case seen red against its own unfixed arm. The fifth arm keeps its
    flat sentence deliberately: its clause *this one included* names the quoted
    line, so it never spoke about rows that might not exist.

  - **Three of the four read what the reader reported as lost; the first
    cannot, and reads what arrived instead.** `hooks/config.py#refusal` fills
    `below` with the rows written under the STOPPING line, and the first arm is
    the one with no stopping line — so `below` is empty there whether the file
    holds rows under that line or not, measured both ways. That arm asks the
    table reader what it returned, which in that arm alone is exactly the rows
    below the quoted line: a row above it would have made the quoted line the
    stopping one.

  - **No verdict moves.** Nothing new is refused and nothing previously
    refused is now run; only the sentence a refusal already printed changes.
    The repository's own config answers identically before and after — mode,
    command, and no refusal at all — and that is now a case rather than a
    reading somebody took once.
