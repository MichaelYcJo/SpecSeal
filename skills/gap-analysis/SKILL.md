---
name: gap-analysis
description: |
  Compare a design or spec document against what was actually built — API
  surface, data model, business logic — and list what is missing, extra, or
  divergent.
  Use when: a written design exists and someone needs to know how far the
  implementation has drifted from it.
  NOT for: checking that ledger coordinates still resolve (`evidence-check`),
  judging ported behavior against an original (`legacy-parity`), or reviewing
  a diff (`code-review`).
---

# Gap Analysis

Compare what was designed vs what was built.

## Comparison Dimensions

1. **API Surface**
   - Endpoints: paths, methods, status codes
   - Request/response schemas
   - Authentication/authorization

2. **Data Model**
   - Entities and relationships
   - Field names, types, constraints
   - Indexes and migrations

3. **Business Logic**
   - Feature completeness
   - Edge case handling
   - Error scenarios
   - Validation rules

4. **Conventions**
   - Naming patterns
   - Folder structure
   - Import patterns
   - Error message format

## Scoring

For each dimension, calculate match rate:
- **Match**: Implemented as designed
- **Partial**: Implemented differently (note difference)
- **Missing**: Not implemented
- **Extra**: Implemented but not in design (may be intentional)

**Overall Match Rate** = matched items / total designed items × 100

## Thresholds
- ≥90%: Report and proceed
- <90%: List gaps, iterate (max 5 iterations)

## Output Format

```
## Gap Analysis: [feature]

Match Rate: [X]%

| Dimension | Match | Partial | Missing | Extra |
|-----------|-------|---------|---------|-------|
| API       |       |         |         |       |
| Data      |       |         |         |       |
| Logic     |       |         |         |       |
| Convention|       |         |         |       |

**Gaps to Address**:
1. [specific gap with file reference]

**Extras to Review**:
1. [unplanned addition - keep/remove?]
```
