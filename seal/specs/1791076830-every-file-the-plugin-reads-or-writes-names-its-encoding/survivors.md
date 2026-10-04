# Survivors — every file the plugin reads or writes names its encoding

Round 1's fix pass removed the encoding test's one `ALLOWED` row, whose key
named the release-seal case that held PIL's `Image.open`. The receiver rule no
longer reports PIL's `Image`, so that unit holds no unnamed call and the row
classified nothing. The place below shares the test's name with the removed
key, and nothing else.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.18.0.md` | test_the_png_carries_the_colours_and_is_clear_where_nothing_is_painted@dd9e1eab | a released row's coordinate for that test unit, which still exists and still holds what R2 claims; the row says nothing about encodings, and the released file is frozen |
