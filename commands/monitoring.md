# /monitoring - Observability & Monitoring Design

## Three Pillars

### Metrics
- Business: conversion, revenue, active users
- Application: request rate, error rate, latency (RED)
- Infrastructure: CPU, memory, disk, network
- Custom: queue depth, cache hit rate

### Logging
- Structured logging (JSON)
- Consistent log levels (ERROR/WARN/INFO/DEBUG)
- Correlation IDs across services
- No sensitive data in logs
- Retention policy defined

### Tracing
- Distributed tracing for multi-service flows
- Span naming conventions
- Critical path identification
- Performance bottleneck detection

## Alerting

### Design
- Alert on symptoms, not causes
- Actionable alerts (runbook linked)
- Severity levels with escalation
- SLO-based alerting over threshold-based

### Anti-patterns
- Alert fatigue (too many low-value alerts)
- Missing alerts on critical paths
- No runbooks for alerts
- Alerting on metrics you can't act on

## Rules
- Start with the critical user path
- Measure what matters to users
- Dashboards: SLOs first, then drill-down
- Don't monitor everything—monitor the right things

## Output

```
## Monitoring Plan: [system/service]

**Key Metrics**: [what to measure]
**Logging**: [what to log, structure]
**Alerts**: [what to alert on, thresholds]
**Dashboards**: [key dashboards to create]
```
