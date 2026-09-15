- **Two round records committed together no longer disagree about which row a
  repeated coordinate belongs to (#404).** `round-record new` attributes a
  coordinate that appears twice in one verdict table to the first of the two
  rows; the map `round-record close` reads ended up holding the last. So a
  confirmation sitting at an open finding's coordinate could win, and round
  N+1's inherited row said that coordinate was `verified` by a row that
  commissioned nothing while round N's own record said `**fixed**`. Both sides
  now take the first row, so they agree by construction rather than by both
  being right.

  Refusing the repeat instead was measured and is not affordable: 71 of the 247
  committed records that parse repeat a coordinate, over 105 of them, so a
  refusal would refuse records this repository has already written. None of the
  105 pairs a numbered row with an unnumbered one today — this is a defect that
  had not yet happened, and the shape that produces it is the one a verifying
  round is asked to write.

- **An inherited table edited or truncated after it was written is refused
  again (#405).** `round-record close` fills round N+1's `## Inherited
  coordinates` from round N's verdicts. Filling nothing used to be silence,
  unconditionally — and it has two causes. One is the ordinary re-review round,
  whose coordinates an earlier round already claimed. The other is a section
  that lost its rows, which no other refusal catches: a table with no rows is
  readable, and it inherits no coordinate for the verdict table to contradict.

  The two are now told apart by asking whether the table still accounts for
  round N's coordinates under any earlier round. When it does not, the run exits
  2 naming the ones it could not account for, and writes nothing to either
  record. A round whose every coordinate an earlier round claimed is unchanged
  and still silent.

  **What a person holding such a record meets is a refusal where they used to
  meet exit 0.** The way out is to regenerate the section or put the rows back,
  and the message says which coordinates are missing rather than stating a rule.

- **A fix row's grounds no longer carry a stray full stop after the dash
  (#414).** The generator cuts the commit out of the third cell of a fix table
  and strips the punctuation around the gap, and the set it stripped held no
  period — so a cell opening `` `6233b769`. `` rendered
  `fixed at 6233b769 — . the note`. This was reported once, repaired by hand in
  nine cells, and the next record the generator wrote carried it again.

  The cause is removed at both of the places that cut a span out of a cell: the
  commit's, and a `deferred` row's cut of its home off the front of the third
  cell, which the report did not name and which rendered the same way. The
  shared separator set is deliberately not widened — five readers share it, and
  a trailing period in a deferral's home or in a `nobody — <why>` reason is part
  of a sentence rather than decoration.

  **One cost, and it is visible in one place.** The strip takes both ends, so a
  note that ends in a full stop loses it too. The note is mid-sentence whenever
  the reviewer wrote a Grounds cell, so this shows only where that cell is
  empty: `` `<sha>`. it reads the cell now. `` renders `fixed at <sha> — it
  reads the cell now`. A one-sided strip would spell these two cuts differently
  from the three beside them, for a stop nobody has yet written.

- **A confirmation that quotes an earlier blocking finding is no longer failed
  as one (#408).** At the pull request, a row's severity was read by asking
  whether 🔴 appeared anywhere in the row — and naming what an earlier round
  found is exactly what a carried-forward closure is for. So a 🟢 row whose
  grounds quoted an earlier 🔴 was announced as *this 🔴 row … a blocking
  finding* in a sentence that then printed `🟢` as the row: one sentence, two
  severities, sending the reader to look for a finding that is not there.

  The severity in the message now comes from the row's own `#` cell, and a row
  whose verdict does not close it is refused by a second arm with its own
  sentence. That sentence names **both** things that put the row there — the
  quote, and the verdict — because either one is a way out: change the word, or
  drop the quote. Which rows fail is unchanged: an unrecognised verdict counting
  as closed is the tolerant read this check exists to refuse.

  **Naming only the word was not enough, and `open` is why.** `open` is the word
  a reviewer is told to write for a finding the round opened, and this same
  check's other arm prints it back as *this 🔴 row reads `open`*. Told instead
  that `open` is outside a vocabulary, a reader goes looking for a rule the
  check does not hold — which is this ticket's own complaint one cell over.

- **The rule that a seal is named with whose has one check again, not two
  (#406).** A second assertion had been added beside the sweep that owns the
  rule, without the sweep's guard for a longer word — so it refused `the
  sealer`, which is the correct way to name the agent. It is removed, and the
  refusal's own exit line now says *before the sealer runs*.

  **The sweep had to be taught one thing first, and that is the interesting
  half.** It reads a module's source text, while the deleted assertion read the
  run's output — and Python joins adjacent string literals where a flattened
  read of the source does not. So a phrase split across two literals was
  invisible to the sweep and perfectly visible in the refusal a person reads,
  and every long refusal here is built from wrapped literals with the wrap
  decided by line length. The sweep now folds that seam, and it found a live
  instance the moment it could see one: a refusal reading *The seal names a
  commit this repository holds* now reads *The sealer's mark names…*.

- **A test fixture that rewrites a record says so when its rewrite misses
  (#407).** Four fixtures across the two record modules edited a record by
  substitution and asserted nothing about the result. A missed substitution
  leaves the record naming no unit, the depth walk then returns at its own
  guard, and the case it feeds passes on assertions that hold for a reason
  unrelated to what the case is named for — measured, and it passes green. Each
  fixture now asserts its substitution landed, and the case beside them asserts
  the judgment it is named for rather than only the two absences.
