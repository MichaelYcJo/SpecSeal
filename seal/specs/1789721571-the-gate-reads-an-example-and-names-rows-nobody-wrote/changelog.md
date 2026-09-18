<!-- seal/specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A `| Item | Value |` table written inside a code fence was the table every
  gate read** (#429). `seal/config.md`'s own header comment points the reader
  at `templates/config.md`, a document of example tables, and the config skill
  tells a session to copy a block of that template — fenced example row
  included — naming no position for it. Pasted above the live table, or above
  a table whose first line will not parse, that example supplied the mode, the
  broad command and every other row, and the sealer's seal was taken over a
  plausible command nobody chose. Measured: with the rule absent, a repository
  whose live table sits under an unclosed fence runs the example's command and
  the gate exits 0 with the stamp printed.

  - **One rule, in front of all three walks of that table.** The gates'
    reader, the mode gate's reader and `seal mode`'s writer now read the file
    through one generator, which hands back each surviving line with its own
    index because the writer overwrites a line by position. A rule in the
    reader alone would have `seal mode` rewriting the `Mode` row inside
    somebody's pasted example while every gate read the live one.

  - **The live table is the first one outside every fence**, and a fence is
    CommonMark's: three or more backticks or tildes, indented at most three
    spaces, closed by at least as many of the same character. A fence that is
    never closed runs to the end of the file, so what it swallows reads as
    undeclared — loud rather than quiet, which is the direction this reader
    already fails in.

  - **`broad-gate` refuses four ways now rather than three.** Where this
    gate's row exists only inside a fence, the refusal quotes that line and
    says where it has to move to, instead of reporting the row absent and
    sending a person to write a row they can see in front of them.

  - **Neither half of the stop rule moved**, and a table can now span a fenced
    block where the fence's own delimiter line used to end it. The filter
    decides which lines the walks are shown; what they do with a line they are
    shown is unchanged.

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
