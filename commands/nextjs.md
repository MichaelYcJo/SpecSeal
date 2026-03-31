# /nextjs - Next.js Best Practices

## App Router Patterns

### Server vs Client Components
- Default to Server Components
- Use `'use client'` only when needed (interactivity, hooks, browser APIs)
- Don't wrap entire pages in `'use client'`
- Pass server data as props to client components

### Data Fetching
- Fetch in Server Components (not useEffect)
- Use `generateStaticParams` for static paths
- Implement loading.tsx for Suspense boundaries
- Use `revalidatePath`/`revalidateTag` for cache invalidation

### Routing
- Layout composition (shared layouts via layout.tsx)
- Error boundaries (error.tsx at appropriate levels)
- Not-found handling (not-found.tsx)
- Route groups for organization (parentheses folders)

### Performance
- Image optimization (next/image)
- Font optimization (next/font)
- Dynamic imports for heavy components
- Proper metadata for SEO

### Server Actions
- Form handling with server actions
- Proper validation (zod)
- Error handling and revalidation
- Optimistic updates where appropriate

## Rules
- Follow project's existing Next.js patterns
- Check Next.js version (App Router vs Pages Router)
- Don't mix patterns unnecessarily

## Output

```
## Next.js Review: [scope]

**Issues by priority**:
1. [issue] at file:line → [fix]

**Patterns to adopt**:
- [suggestion with example]
```
