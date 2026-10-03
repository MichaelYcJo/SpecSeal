# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | e887aa06 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 4, `chain_check` prints: one notice per pact held elsewhere,
giving the repository, the notify value and the count of anchors in the
declared work item's `spec.md`, and saying it is not verified here; a notice
where the repository holds `seal/pact.md`; notices for an unparseable row
and for an anchor naming an undeclared pact; no exit status moves. Verified
by S5 and S6 as `chain_check` cases in temporary repositories, in the shape
of `tests/test_chain_check_at_the_pull_request.py`, each asserting the same
exit status as the tree without the row and pinning the printed sentence.

## What this phase found

**The frame holds, and one reader it did not name was needed.** The notice
for a repository holding `seal/pact.md` prints how many signatories the
pact lists, so something has to read the pact's `| Signatory |` table, and
phase 5 needs the same reading. It went into `hooks/config.py` as
`pact_signatories`, beside `pact_declaration`, through the walk
`config_rows` uses, and the entry check both share became
`remote_entries`. The name rules (the anchor's character class, two entries
ending in one name) apply to `Pact` entries alone: nobody cites a signatory
by name, and two signatories may end in one path segment.

**Where the print sits in `main`.** Computed once the declarations are
known and before the early return, so a pull request that declares nothing
still prints a relationship the tree holds; on the main path the notices
seed `notices`, never `errors`. The cases build each tree twice, with and
without the pact, and assert the two exit statuses equal, passing and
failing, because the claim is *does not move* and a fixed expected code
could hold by accident.

**A reader that will not load is a notice too.** `pact_notices` loads
`hooks/config.py` and `evidence_check.py` (for `PACT_ANCHOR_RE` and
`unquoted`) itself, and a failure there is one notice rather than the
exit 2 the shared reader's failure gives, for decision 2's reason.

**Anchors are counted outside closed fences.** `unquoted` blanks a fenced
example, the rule the ledger reader keeps, so a spec quoting the anchor's
shape in a code block does not count it as a citation.

**The `splitlines` census named the new call.**
`tests/test_every_reader_ends_a_line_where_gfm_does.py` holds every
`.splitlines(` in shipped code to a list with a reason, and failed on
`pact_signatories`. The call feeds the same `unfenced(lines, text)` walk
`config_rows` and `refusal` feed, which reads GFM lines from TEXT, so it was
listed under their reason.

**Ledger rows this phase drifted (Q13, phase 4).** Six rows cite
`chain_check.py#main` (`seal/ledger.md` one, `seal/releases/0.4.0.md`,
`0.13.1.md` and `0.14.0.md` one each, `0.15.4.md` two). Each was read
against the edit, each claim holds, and each carries a dated note. This
work item's own P1 drifted with the refactor of `pact_declaration` and was
re-read. P8's first wording carried bare pipes and was refused as a split
row; it was escaped.

**Verified, executed.** Red: all 7 new `chain_check` cases with
`chain_check.py` stashed; the pact notices seeded into `errors` turned the 5
declared cases red; three breaks of `pact_signatories` each turned one case
red. Green: the 44 modules naming `chain_check` or `config.py`, the two new
ones among them, gave 2775 passed, 7 skipped and the census failure above; with
the census entry, that module gave 153 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
