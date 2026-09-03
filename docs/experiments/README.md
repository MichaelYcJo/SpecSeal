# docs/experiments/ — what was measured, so nobody measures it twice

One file per experiment: a question that reading could not settle, the
method that settled it, and what the result decided. A platform fact
established here outlives any work item, which is why it lives under
`docs/` and not with the work item that needed it.

Name a file `<date>-<what-was-asked>.md`. Keep the sections in this order,
because a reader who only wants the answer stops after the second one:

1. **Question** — one sentence, and why reading alone did not answer it.
2. **What it established** — numbered, each a fact the reader can act on.
3. **Method** — enough to re-run it, including how to restore.
4. **Results** — the runs, in order, with what each one ruled out.
5. **What it did not establish** — so the next reader knows the edge.

A result that later turns out to be version-specific gets a dated note at
the top, not a rewrite: the old measurement was true when taken.
