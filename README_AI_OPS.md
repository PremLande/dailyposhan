# AI Ops workflow

This repository now includes an AI-assisted incident workflow with:

- Prometheus + Grafana + Alertmanager + Loki in Docker Compose
- A Python FastAPI service that accepts Alertmanager webhooks and produces a structured incident analysis
- An approval endpoint for human review
- A simple history log so future analyses can use prior incident patterns

## Quick start

1. Install Docker and Docker Compose.
2. Install Ollama locally and pull a model, for example:
   - `ollama pull llama3.2`
3. Start the stack:
   - `bash scripts/setup_aiops.sh`
4. Verify:
   - `curl http://localhost:8001/health`
   - `curl http://localhost:9093/`

## Example alert webhook

```bash
curl -X POST http://localhost:8001/analyze \
  -H 'Content-Type: application/json' \
  -d '{
    "receiver": "ops",
    "status": "firing",
    "alerts": [{
      "labels": {
        "alertname": "HighErrorRate",
        "severity": "critical",
        "service": "backend"
      },
      "annotations": {
        "summary": "High error rate detected",
        "description": "The backend is returning more than 20% 5xx responses"
      },
      "startsAt": "2026-07-13T10:00:00Z"
    }]
  }'
```

## Approval and remediation

- POST to `/approve` with `{ "incident_id": "..." }` to mark an incident for approval.
- The current implementation is intentionally lightweight and can be extended to call Rundeck, Ansible, or Kubernetes APIs once a target environment is available.
