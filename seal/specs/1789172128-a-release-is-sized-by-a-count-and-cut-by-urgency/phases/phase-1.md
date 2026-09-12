# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `6de3f54` |
| Ran by | unknown — the spawn prompt named no model, and the template gives this row to the spawning session rather than to the segment. The orchestrating session fills it |

## What this phase was asked

Take the three measurements that decide the prose, before any prose exists,
and write no line under `docs/`:

- **Q5** — does `timers_in` actually refuse `0.11.0` and `0.11.1` in a `docs/`
  file at the running version, and is a shipped-but-running version refused
  with them? One `test_tmp_*` probe, deleted before handover.
- **Q6** — run the sweep command for the last `## Done when` row and record
  what it returns today.
- **Q7** — run `bin/evidence-check .` before the edit, so phase 4 has a
  before-reading to compare against.

Record which route Q1 took, and state whether S11 applies rather than leaving
it ambiguous.

## What this phase found

**Q5 — both citations are refused, and one of them names a release this
repository has shipped.** Executed, exit code 0 on the probe itself; the
readings are the probe's own output.

| Token in a `docs/` file | `timers_in` at running `0.11.0` |
|---|---|
| `0.11.0` | refused — `[(1, '0.11.0')]` |
| `v0.11.0` | refused — `[(1, 'v0.11.0')]` |
| `0.11.1` | refused — `[(1, '0.11.1')]` |
| `v0.11.1` | refused — `[(1, 'v0.11.1')]` |
| `0.8.3` | allowed — `[]` |
| `1.2.3` | allowed — `[]` |

So the frame's central claim holds by execution and not only by reading the
constants, and both spellings are refused — a `v` prefix is no way out.

The off-by-one is measured too, from the same probe run: `CHANGELOG.md` records
`0.11.0` as released, `git tag --list v0.11.*` answers `['v0.11.0']`, and
`0.11.1` is in neither. So the refused pair is one version the repository has
demonstrably shipped and one it has not, and the check treats them
identically. That is the whole of **#363**'s argument, and this phase confirms
it rather than repairing it.

The probe also re-checked that the sizing paragraph's existing evidence
survives: `0.8.3` is below the running version and stays allowed, so phase 2
keeps that sentence untouched.

**Q6 — one owner in the loaded tree, and the sweep needs a second shape.**

```
git grep -niE "three or four|sized in work items|release is sized" \
  -- docs skills agents templates tests README.md README.ko.md CONTRIBUTING.md
exit=0
docs/issues-and-milestones.md:24:**A release is sized in work items rather than in ticket numbers, and three
```

One line, and it is the paragraph phase 2 rewrites. A wider run —
`-niE "is the size|sized (in|by)|release's size"` over the same set — returns
that line and the line under it, and nothing else, so no second carrier
exists. `docs/review-chain-spec.md:53` and `agents/smith.md` state a **round**
ceiling, which is a different subject and is correctly outside the pattern.

**The finding the next phases need: `three or four is the size` cannot be
grepped as a phrase, because the line wraps between `three` and `or four`.**
S3's `Verifiable how` cell proposes
`git grep -n "three or four is the size"` and expects it to exit 1 after the
edit — but it exits 1 **today**, before anything is edited, so as written it
proves nothing. Phase 4's case therefore reads the document through a
whitespace-flattening reader, which is exactly what
`tests/test_one_word_one_meaning.py`'s own `flat()` helper does and why that
module has one. This is a defect in the frame's verification recipe, not in the
scenario: the substance of S3 is unchanged and the sweep above still answers
it.

**Q7 — no drift before the edit.** `bin/evidence-check .`, exit code read
directly: **exit 0**, `total: 1137 ok · 0 drifted · 0 broken · 0 external ·
0 old-format`, with the two work-item fragments at 5 and 16 rows. Phase 4
compares against this reading.

**Q1's route, recorded: (c).** The two releases are cited as prose with no
version numbers, and the checker's off-by-one is filed as #363. So no gate
changes in this work item, and **S11 does not apply** — `CONTRIBUTING.md`
§*What a change to a gate must carry* is not owed here, and `plan.md`'s
§*What a change to a gate must carry* section stands as the conditional it
says it is. `tests/test_release_hygiene.py` is not edited.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `tests/test_tmp_q5_timers_refuses_both_citations.py` — the Q5 probe, deleted before handover per `agent-contract` §7, together with `tests/__pycache__` | its readings, which are the Q5 table above. Nothing else needs it |
