# 1789081272-the-writer-of-the-contract-is-not-its-executor — survivor exemptions

## Phase 2 — the move out of the design gate

`survivor-check --range 02c5b90..5571996` examines 843 files against the
seventeen sentences the range removed and reports one place. It is a
coincidence of ordinary Python, scoring 1.89 on three shared phrases — two of
them the same fragment counted twice — and it is not a copy of anything this
phase corrected.

The removal that produced it is `test_the_design_gate_belongs_to_the_smith`,
whose body opened `agents/smith.md` and looped `for name in
("confidence-check", "feature-planner")`. What the check found standing is a
different loop over a different directory, in a module about the root
migration.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_root_migrates_itself.py` | `for name in sorted(os.listdir(os.path.join(ROOT, "hooks"))):` | **About which hooks still read `.specseal/`**, which is S15 of another work item and has nothing to do with who calls the two utility skills. The shared phrases the check names are `8 read assert` — the `encoding="utf-8"` read followed by an assertion, twice — and `for name in`, which is every walk over a sorted list of file names. The claim this phase corrected was *the design gate belongs to the smith*; nothing resembling it appears in this file |

**What would make this exemption stop holding.** The quote is the anchor. If
that loop ever comes to read `agents/*.md` or to assert which agent calls a
skill, it is the same subject and the report is a finding rather than a
coincidence.

The exemption is anchored on this range as well as on this quote. A different
range re-runs the check from scratch, and a row written for
`02c5b90..5571996` does not answer for it.

**Over the phase's whole range the report is gone, and the row is kept
anyway.** `survivor-check --range 02c5b90..dfe9d6f` examines 844 files against
twenty-four removed sentences and reports nothing standing: the phase's later
commits changed what the range removed, and the 1.89 that put this pairing
over the floor did not survive the recount. The row stays because it records a
judgment somebody made and can check — deleting it would leave the phase
record naming a survivor with nothing behind it — and because it costs
nothing: an exemption that matches no candidate silences nothing.
