# Questions — every branch appends to the same two files

Three decisions were settled by the repository owner in the routing batch and
are not re-opened here: the changelog is fragmented and gathered at release,
the ledger is fragmented and never gathered, and a ledger row stops carrying a
`Checked` SHA. What follows arrived during implementation.

## Q1 — a row can be stale on arrival, and no derived baseline sees it

**Who must answer:** repository owner. Related to issue #31.

Two branches run at once. Branch A writes a ledger row citing `code.py:10`.
Branch B changes `code.py:10`. B squashes into the release branch first, then
A. The row's first appearance is A's own squash commit, which already contains
B's change — so `git diff <that commit>..HEAD` shows nothing and the row reads
OK, while its coordinate was stale the moment it landed.

Last-touch blame misses it the same way. The written stamp caught it noisily
and by accident: a row stamped at the base reads DRIFTED against everything
that happened after, B's change included, which is the same warning it gives
for work nobody touched.

Catching it properly means checking the coordinate against the code it cites
rather than against a diff window — which is issue #31, and outside this work
item. **Recorded rather than fixed**, so the limit is a known one.

What can be said for the current state: it is not a regression. The stamped
scheme's noise was not detection, and the derived baseline is right about
every case where the row and its code moved together.

## Q2 — nothing forbids a commit SHA in a fragment's prose header

**Who must answer:** repository owner.

`find_baseline` reads a ledger's header for a declared baseline, and a
fragment declares none — so a commit named in a fragment's prose becomes the
whole file's baseline. This happened on the first fragment written: the file
reported drift against a commit resolvable in one clone and nowhere else.

Two things narrow it and neither closes it. The header now ends above the
first row that cites code, so a row's prose is out of reach; and a row's own
baseline must be a date and a SHA together, so prose in a row is inert. What
remains is prose in the header itself, which is a convention
(`templates/map.md` states it) with nothing enforcing it.

The options, if it is worth closing: require a header baseline to sit in a row
labelled `Baseline`, which would break a ledger whose header writes a bare SHA
— `tests/test_evidence_check_hardening.py::test_custom_ledger_glob` has that
exact shape — or leave it as a convention. The failure direction of enforcing
it is that such a ledger silently loses its header baseline and falls back to
per-row derivation, which reports LESS drift. That is the wrong direction, and
it is why this was not decided here.
