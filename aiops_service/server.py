from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class Field:
    def __init__(self, default=None, default_factory=None):
        self.default = default
        self.default_factory = default_factory


class BaseModel:
    def __init__(self, **data: Any):
        for key, value in data.items():
            setattr(self, key, value)

    def dict(self) -> Dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if not key.startswith("__")}

    def model_dump(self) -> Dict[str, Any]:
        return self.dict()


class AlertPayload(BaseModel):
    receiver: str = "ops"
    status: str = "firing"
    alerts: List[Dict[str, Any]] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)
    notification_webhook: Optional[str] = None

    def __init__(self, **data: Any):
        defaults = {
            "receiver": "ops",
            "status": "firing",
            "alerts": [],
            "logs": [],
            "notification_webhook": None,
        }
        defaults.update(data)
        super().__init__(**defaults)


class IncidentResponder:
    def __init__(self, history_path: Optional[Path] = None, ollama_url: Optional[str] = None) -> None:
        self.history_path = history_path or Path("/tmp/aiops_history.jsonl")
        self.ollama_url = ollama_url or os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

    def generate_analysis(
        self,
        alert: Dict[str, Any],
        logs: Optional[List[str]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        use_llm: bool = True,
    ) -> Dict[str, Any]:
        logs = logs or []
        history = history or []
        if use_llm:
            try:
                prompt = build_analysis_prompt(alert=alert, logs=logs, history=history)
                response = self._query_ollama(prompt)
                return self._parse_llm_response(response)
            except requests.RequestException:
                pass

        return {
            "root_cause": "Likely saturation or misconfiguration around the affected service",
            "severity": alert.get("severity", "high"),
            "confidence": 0.72,
            "recommended_remediation": "Check recent deployments, resource limits, and dependency health before applying a rollout rollback",
        }

    def _query_ollama(self, prompt: str) -> Dict[str, Any]:
        payload = {
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }
        response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def _parse_llm_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = response.get("response", "")
        try:
            parsed = json.loads(raw_text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {
            "root_cause": raw_text[:200],
            "severity": "high",
            "confidence": 0.5,
            "recommended_remediation": "Investigate this alert manually and confirm with logs",
        }

    def notify_summary(self, incident_id: str, alert: Dict[str, Any], analysis: Dict[str, Any], webhook_url: Optional[str] = None) -> Dict[str, Any]:
        webhook = webhook_url or os.getenv("SLACK_WEBHOOK_URL") or os.getenv("TEAMS_WEBHOOK_URL")
        if not webhook:
            return {"status": "skipped", "reason": "no webhook configured"}

        payload = {
            "incident_id": incident_id,
            "alert": alert,
            "analysis": analysis,
        }
        response = requests.post(webhook, json=payload, timeout=15)
        response.raise_for_status()
        return {"status": "sent", "status_code": response.status_code}

    def append_history(self, incident: Dict[str, Any]) -> None:
        with self.history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(incident) + "\n")

    def load_history(self) -> List[Dict[str, Any]]:
        if not self.history_path.exists():
            return []
        rows = []
        with self.history_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def update_history(self, incident_id: str, update: Dict[str, Any]) -> Dict[str, Any]:
        rows = self.load_history()
        updated = False
        for row in rows:
            if row.get("incident_id") == incident_id:
                row.update(update)
                updated = True
                break
        if not updated:
            raise HTTPException(status_code=404, detail="incident not found")
        self.history_path.write_text("", encoding="utf-8")
        with self.history_path.open("a", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")
        return {"status": "updated", "incident_id": incident_id}


def parse_alertmanager_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    alerts = payload.get("alerts", []) or []
    first_alert = alerts[0] if alerts else {}
    labels = first_alert.get("labels", {}) or {}
    annotations = first_alert.get("annotations", {}) or {}
    return {
        "alert_name": labels.get("alertname") or labels.get("alert_name") or "unknown",
        "severity": labels.get("severity", "warning"),
        "service": labels.get("service") or labels.get("job") or "unknown",
        "summary": annotations.get("summary") or first_alert.get("summary") or "No summary provided",
        "description": annotations.get("description") or "No description provided",
        "starts_at": first_alert.get("startsAt"),
        "ends_at": first_alert.get("endsAt"),
        "status": payload.get("status", "firing"),
    }


def build_analysis_prompt(alert: Dict[str, Any], logs: Optional[List[str]], history: Optional[List[Dict[str, Any]]]) -> str:
    history_text = "\n".join(
        f"- incident: {item.get('incident', 'unknown')}; outcome: {item.get('outcome', 'unknown')}" for item in (history or [])
    ) or "- no prior incidents"
    log_text = "\n".join(logs or []) or "- no logs available"
    return (
        "You are an AI incident responder. Analyze the alert and return a compact JSON object with keys: "
        "root_cause, severity, confidence, recommended_remediation. "
        f"Alert: {json.dumps(alert, ensure_ascii=False)}\n"
        f"Recent logs:\n{log_text}\n"
        f"Prior incident history:\n{history_text}\n"
        "Return only valid JSON."
    )


class FastAPI:
    def __init__(self, title: str):
        self.title = title
        self.routes: Dict[tuple[str, str], Any] = {}

    def get(self, path: str):
        def decorator(func):
            self.routes[("get", path)] = func
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes[("post", path)] = func
            return func
        return decorator

    async def __call__(self, scope: Dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self._send_json(send, 500, {"detail": "unsupported scope"})
            return

        method = scope.get("method", "").lower()
        path = scope.get("path", "")
        handler = self.routes.get((method, path))
        if handler is None:
            await self._send_json(send, 404, {"detail": "not found"})
            return

        try:
            if method == "post":
                body = await self._read_json_body(receive)
                if path == "/analyze":
                    result = handler(AlertPayload(**body))
                else:
                    result = handler(body)
            else:
                result = handler()
        except HTTPException as exc:
            await self._send_json(send, exc.status_code, {"detail": exc.detail})
            return

        await self._send_json(send, 200, result)

    async def _read_json_body(self, receive: Any) -> Dict[str, Any]:
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            if message.get("type") != "http.request":
                continue
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        if not body:
            return {}
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    async def _send_json(self, send: Any, status_code: int, payload: Any) -> None:
        body = json.dumps(payload).encode("utf-8")
        headers = [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode("utf-8")),
        ]
        await send({"type": "http.response.start", "status": status_code, "headers": headers})
        await send({"type": "http.response.body", "body": body})


app = FastAPI(title="AI Ops Service")
responder = IncidentResponder()


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: AlertPayload) -> Dict[str, Any]:
    payload_dict = payload.dict() if hasattr(payload, "dict") else payload.model_dump()
    alert = parse_alertmanager_payload(payload_dict)
    history = responder.load_history()
    logs = payload.logs or []
    analysis = responder.generate_analysis(alert=alert, logs=logs, history=history)
    incident_id = f"incident-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    entry = {
        "incident_id": incident_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert": alert,
        "analysis": analysis,
        "status": "new",
    }
    responder.append_history(entry)
    notification = responder.notify_summary(incident_id, alert, analysis, webhook_url=payload.notification_webhook)
    return {"incident_id": incident_id, "alert": alert, "analysis": analysis, "notification": notification}


@app.post("/approve")
def approve(approval: Dict[str, Any]) -> Dict[str, Any]:
    incident_id = approval.get("incident_id")
    if not incident_id:
        raise HTTPException(status_code=400, detail="incident_id is required")
    update = {
        "status": "approved",
        "approved_by": approval.get("approved_by", "unknown"),
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    return responder.update_history(incident_id, update)


@app.post("/execute")
def execute(approval: Dict[str, Any]) -> Dict[str, Any]:
    incident_id = approval.get("incident_id")
    if not incident_id:
        raise HTTPException(status_code=400, detail="incident_id is required")

    command = approval.get("command") or os.getenv("REMEDIATION_COMMAND")
    if not command:
        raise HTTPException(status_code=400, detail="command is required")

    completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
    result = {
        "status": "executed",
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }
    responder.update_history(incident_id, result)
    return {"incident_id": incident_id, **result}


@app.post("/outcome")
def record_outcome(outcome: Dict[str, Any]) -> Dict[str, Any]:
    incident_id = outcome.get("incident_id")
    if not incident_id:
        raise HTTPException(status_code=400, detail="incident_id is required")
    update = {
        "outcome": outcome.get("outcome", "unknown"),
        "resolution_notes": outcome.get("resolution_notes", ""),
        "resolved_at": datetime.now(timezone.utc).isoformat(),
    }
    return responder.update_history(incident_id, update)
