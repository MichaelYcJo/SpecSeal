# Survivors — the encoding walker judges a class opener and a shadowing local

Round 1's fix pass rewrote ledger row J1, which used to say that no table
`judge` matches by dotted name holds a method of a class in
`UNBOUND_RECEIVERS`. The new row still says it, as *a method of such a class*,
and adds that every class `OPEN_METHODS` names is in that list. Each place
below shares the phrase *a method of a class in `UNBOUND_RECEIVERS`* with the
old wording, and each is still true.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/spec.md` | A key of `OPENERS` that is a method of a class in `UNBOUND_RECEIVERS` is reachable from there when the method is called on its class | the frame's C1, describing the defect at the base. It is a record of what was asked, and the defect it names is closed for every class the list holds |
| `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` | Each key of `tables` that is a method of a class in | the docstring of `methods_of_unbound_receivers`, which filters exactly by membership of `UNBOUND_RECEIVERS` |
| `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` | are methods of a class in UNBOUND_RECEIVERS, matched by | the failure message of `test_no_method_is_matched_by_its_dotted_name`, naming what that assertion checks; the `OPEN_METHODS` half has its own message |
