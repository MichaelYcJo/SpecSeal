- **`evidence-check` says in which order `#` and `@` have to come to count
  as one coordinate (issue #626).** 0.15.5's entry said the two marks count
  as one coordinate only where they are glued, and left out that the `@`
  has to come after the `#`. The checker has always required that order.
  So `@alice#299`, a mention followed by an issue number, is prose, and
  `@alice#299@abcdef12` is still named, because its second `@` follows the
  `#`. The checker's own statement of the rule now says so. Every example
  the rules give, including three that had lost their case in 0.15.5, is now
  held by a case against both the checker and that statement. What the
  checker names is unchanged.
