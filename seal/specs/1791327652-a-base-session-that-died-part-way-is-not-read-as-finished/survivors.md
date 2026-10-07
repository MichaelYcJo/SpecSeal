# Survivors — a base session that died part-way is not read as finished

`survivor-check --range c339dccd..359badfc` named eight places that still
carry wording round 2's fix pass removed. The pass removed two sentences, and
neither was removed because what it said had stopped being true:

- **The New? bullet's sentence on a base session that stopped part-way**
  (`skills/verify/SKILL.md`) was reworded because it copied 21 words of
  rule 3, which `tests/test_no_passage_is_pasted_into_a_second_file.py`
  refuses (#849 round 2's 🔴 2). The fact stands, in other words.
- **The changelog fragment's sentence naming the two stops** was reworded
  for the same reason: it shared a 20-word run with rule 3.

So every place below states the same fact the reworded sentence still
states. Rule 3 is the home both copies were taken from, and the rest are its
pins, its ledger claim, a docstring and the overview's record of it. Each was
read at 359badfc.

| Path | Quote | Grounds |
|---|---|---|
| `templates/config.md` | Two stops are named rather than closed: a test that calls `pytest.exit` with a return code of 0, 1 or 5 chooses one of the three | rule 3, the home of the two named stops; the changelog's copy was reworded so it stops repeating this sentence, and this one is still true |
| `templates/config.md` | Either `new` reads `new?` naming the count, too, where a session of the base stopped part-way | rule 3, the home of the stopped-session sentence; the **New?** bullet was reworded so it stops copying it, and this one is still true |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | Two stops are named rather than closed: a test that calls | the pin of rule 3's sentence above, which has to carry the text it pins |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` | Either `new` reads `new?` naming the count, too, where a session of | the pin of rule 3's sentence above, which has to carry the text it pins |
| `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md` | names two stops rather than closing them | U3's claim, a paraphrase of rule 3's sentence, still true |
| `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md` | U3 · rule 3 of `templates/config.md` §*Broad gate* says either `new` reads `new?` naming the count, too | U3's claim, which quotes rule 3 rather than the bullet; still true |
| `skills/verify/scripts/broad_gate.py` | either `new` reads `UNENDED_AT_BASE` instead where a session of the base stopped part-way | `base_word`'s docstring, which states the same rule for the code; still true |
| `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/overview.md` | are named rather than closed, in rule 3 and in | the overview's *Not done* row naming the two stops, a record of the same fact; still true |
