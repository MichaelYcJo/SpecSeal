### Fixed

- **The rider check reads a rider only on the lines its hash leaves out.**
  Before, a rider could follow a closed HTML comment and a U+2028, a form
  feed or one of the six other characters on its line. It could also follow
  `# note` and one of those characters in a Python file. Either way it was
  read past the line the hash cut, so its own stamp was hashed, and
  `--reverify` never made it read ok. Such a rider is now read as it would
  be with a space in place of the character. For the markdown shape that is
  "no verification stamp", because the comment that closes on that line ends
  the rider there (#682).
