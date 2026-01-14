## Notes on REGEX 
- Regex for text between parenthesis: r"\((.*?))/"
  - \( -> escaped opening parenthesis
  - (  -> capture group
  - .*? -> Match any number of characters
  - )  -> capture group
  - /) -> escaped closing parenthesis

- Regex for phone number: r"\d{3}-\d{3}-\d{4}"
 
- Regex for email: r"(\w+)@(\w+\.\w+)"
  - Capture group 1: (\w+) -> match alphanumeric characters and underscores
  - Literal: @  
  - Capture group 2: (\w+\.\w+)
  - \w+ -> same as above
  - \. -> literal (but its a special character that needs to be escaped, like parenthesis)
  - \w+ -> same as above
- Negative lookbehind:
  -  Use these when you need to match something that is not preceded by something else.
  -  Example:
  -     "The word cat appears here, but not in concat"
  -     r"(?<!con)cat" <- match the pattern cat if it isn't preceded by con
- https://regexr.com/

