# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 91ca7125 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

**new** `docs/the-evidence-ledger.md` — the ledger, its two checkers, the
unverified record and `settle` itself; the file wrapped at 88 and added to
`test_docs_line_wrap.COVERED`. Verified as phase 3, plus the line-wrap case
green on the new file.

## What this phase found

### The wrap limit and the fold marker cannot both be satisfied

**This is the phase's real finding, and the plan could not have known it.**
The plan's own row asks for two things that collide: the file wrapped at 88
**and** in `COVERED`, while carrying markers whose length nobody writing this
file controls.

- `unverified_check.FOLD_MARKER` is `^<!-- specs/(\S+) -->$` — matched
  **whole**. A wrapped marker is not a fold record, so the retirement would
  refuse the directory it covers.
- A marker's length is `<!-- specs/ -->` plus a work item id, and an id is
  `<unix-epoch-seconds>-<slug>` with nothing bounding the slug. The length is
  decided months earlier, in another work item, by whoever opened it.
- Measured over the retire set: **one marker of 88 reaches 89 columns**,
  `1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections`.
  The other 87 fit, which is why this is a class and not a coincidence —
  87 fitting is luck, and the next long slug is the same defect again.

So the limit moved, not the marker. `prose_lines` already skips what cannot
be broken — a URL is its own precedent, and its docstring already said so —
and a fold marker joins that list. The skip is **exactly one line wide**: a
skip written a line too wide would take the folded sentence with it, and a
folded sentence is the prose the limit exists for.

Two cases pin it, and both were seen red with the skip arm deleted: the
parametrised case on the new file, and
`test_a_fold_marker_is_skipped_and_the_line_beside_it_is_not`, which
yielded `[1, 2]` where it asserts `[2]`. A third case pins the other
direction, that a marker **quoted inside a sentence** is still prose — the
same rule `folded_items` reads it by, so the two readers cannot drift.

This is a change to a check, so it is stated rather than slipped in: it
narrows what counts as prose by one line shape, it does not raise `LIMIT`,
and the constant is spelled the way the reader spells it with a comment
saying why the two must agree.

### The document is organised by reader, not by segment

Nine work items across four scripts. Grouping them by script would have
produced four sections a reader has to already know the code to navigate, so
the document is laid out by what somebody opening it wants to know:

| Section | Items |
|---|---|
| A row is a content anchor, and it names no commit | `1788229400`, `1788761915` |
| What the checker refuses, and what it says while refusing | `1789296100`, `1788686494` |
| A correction a merge dropped | `1789969379`, `1789996780` |
| The unverified record, and the baseline it is read against | `1788873600` |
| The fold, and what tells it from a deletion | `1790027178`, `1790039346` |

### What was dropped rather than folded

**`1788229400`'s `--migrate` arm.** A one-shot writer that consulted an old
stamp's commit before trusting a line number. It existed to move rows off
the old scheme, every row has moved, and a one-shot migration is not a
standing rule.

**`1788686494`'s judgment about the scan-suggestion site.** Its `spec.md`
names `evidence_check.py:627` as a path that carries no `..` to collapse and
is therefore out of scope. That is a reading of one line at one commit, not
a rule; the rule is the one that folded — a printed name is the file that
was opened.

**`1789296100`'s document list.** Five documents were brought into step in
that commit. Which five is the change; that the lenient reading names the
strict one beside it is the rule.

**`1788761915`'s `#207`** — `round_record.py new` saying what bound the next
round is under. It is the generator's behaviour, and the generator's
standing statement is phase 3's, in `docs/review-chain-spec.md`. Folding it
here as well would put one rule in two policy documents, which is the drift
this repository's own one-word-one-meaning rule is about.

### One destination question, answered by reading

`1790027178` and `1790039346` are `settle`'s own two work items, and
`docs/one-root-by-lifetime.md` already has a §*What keeps `settle` light*.
They are folded **here** rather than there because what they established is
about the **fold record** — the marker, what makes a line live, which
directory level is read — and the fold record is what the retirement and the
unverified reader both key on. `one-root-by-lifetime.md` owns where the roots
are and what each lifetime is; phase 6 folds that segment into it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| a fold-marker line from the wrap check's definition of prose | `prose_lines`' docstring, which now states the exclusion and its measurement, and the two cases that pin the skip's width |
| nothing from the tree otherwise | none |
