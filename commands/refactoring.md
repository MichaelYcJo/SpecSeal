# /refactoring - Systematic Code Refactoring

## When to Use
- Code smells identified
- Technical debt reduction
- Before adding new features to messy code

## Process

### 1. Assess
- What's the problem? (specific smell or pain point)
- What's the goal? (measurable improvement)
- What's the risk? (what could break)

### 2. Safety Net
- Ensure tests exist for affected code
- If no tests: write characterization tests FIRST
- Commit current state (checkpoint)

### 3. Refactor
- One refactoring at a time
- Small steps: extract → rename → move → simplify
- Run tests after EACH step
- Commit after each successful step

### 4. Verify
- All existing tests still pass
- Code is measurably better (fewer lines, clearer intent, less coupling)
- No behavior changes (unless explicitly intended)

## Common Refactorings
- Extract method/function (long functions)
- Extract class (god classes)
- Introduce parameter object (long parameter lists)
- Replace conditional with polymorphism
- Move method to where the data lives
- Remove middle man

## Rules
- Never refactor and change behavior simultaneously
- If tests don't exist, write them first
- Small commits: one refactoring per commit
- Stop when "good enough" - don't gold-plate
