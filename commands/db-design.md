# /db-design - Database Schema Design & Review

## Scope
Design or review database schemas, migrations, queries.

## Design Checklist

### Schema
- Appropriate normalization level (usually 3NF, denormalize with reason)
- Primary keys defined (prefer UUID or auto-increment)
- Foreign key constraints
- NOT NULL where appropriate
- Default values where sensible
- Timestamps: created_at, updated_at

### Naming
- snake_case for tables and columns
- Plural table names (users, orders)
- Descriptive column names (no abbreviations)
- Consistent naming patterns across tables

### Performance
- Indexes on foreign keys
- Indexes on frequently queried columns
- Composite indexes for common query patterns
- Avoid over-indexing (writes suffer)

### Data Integrity
- Constraints (CHECK, UNIQUE, FK)
- Soft delete vs hard delete (project convention)
- Enum handling (DB enum vs string vs lookup table)

### Migration
- Reversible migrations
- No data loss in migrations
- Large table migrations need careful planning (online DDL)

## Output

```
## Schema: [entity/feature]

### Tables
[table definitions with columns, types, constraints]

### Relationships
[ERD or text description]

### Indexes
[index definitions with justification]

### Migration Plan
[ordered migration steps]

### Queries
[key query patterns with expected performance]
```
