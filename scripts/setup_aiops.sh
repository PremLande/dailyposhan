#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m pip install -r requirements-aiops.txt pytest >/dev/null 2>&1 || true

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required to run the monitoring stack." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose is not available." >&2
  exit 1
fi

echo "Starting Prometheus, Grafana, Alertmanager, Loki, and the AI Ops service..."
docker compose -f docker-compose.yml -f docker-compose.aiops.yml up -d

echo "Deployment complete."
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"
echo "- Alertmanager: http://localhost:9093"
echo "- AI Ops service: http://localhost:8001/health"
