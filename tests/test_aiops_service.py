import json
from pathlib import Path

from aiops_service.server import IncidentResponder, build_analysis_prompt, parse_alertmanager_payload


def test_parse_alertmanager_payload_extracts_alert_fields():
    payload = {
        "receiver": "ops",
        "status": "firing",
        "alerts": [
            {
                "labels": {
                    "alertname": "HighErrorRate",
                    "severity": "critical",
                    "service": "backend",
                },
                "annotations": {
                    "summary": "High error rate detected",
                    "description": "The backend is returning more than 20% 5xx responses",
                },
                "startsAt": "2026-07-13T10:00:00Z",
                "endsAt": "2026-07-13T11:00:00Z",
            }
        ],
    }

    alert = parse_alertmanager_payload(payload)
    assert alert["alert_name"] == "HighErrorRate"
    assert alert["severity"] == "critical"
    assert alert["service"] == "backend"
    assert alert["summary"] == "High error rate detected"


def test_build_analysis_prompt_includes_logs_and_history(tmp_path):
    history_file = tmp_path / "history.jsonl"
    responder = IncidentResponder(history_path=history_file)
    prompt = build_analysis_prompt(
        alert={
            "alert_name": "HighErrorRate",
            "severity": "critical",
            "service": "backend",
            "summary": "High error rate detected",
        },
        logs=["2026-07-13T10:00:00Z backend error: database connection pool exhausted"],
        history=[{"incident": "database timeout", "outcome": "resolved"}],
    )

    assert "HighErrorRate" in prompt
    assert "database connection pool exhausted" in prompt
    assert "database timeout" in prompt
    assert "incident" in prompt.lower()


def test_generate_analysis_returns_structured_summary(tmp_path):
    history_file = tmp_path / "history.jsonl"
    responder = IncidentResponder(history_path=history_file)
    analysis = responder.generate_analysis(
        alert={
            "alert_name": "HighErrorRate",
            "severity": "critical",
            "service": "backend",
            "summary": "High error rate detected",
            "description": "The backend is returning more than 20% 5xx responses",
        },
        logs=["2026-07-13T10:00:00Z backend error: database connection pool exhausted"],
        history=[],
        use_llm=False,
    )

    assert analysis["root_cause"]
    assert analysis["severity"] in {"critical", "high", "medium", "low"}
    assert 0 <= analysis["confidence"] <= 1
    assert analysis["recommended_remediation"]
