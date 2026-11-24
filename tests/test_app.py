
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Har test ke liye alag temporary database
    test_database = tmp_path / "test_deployments.db"
    monkeypatch.setattr(app_module, "DATABASE", test_database)

    app_module.init_db()

    with app_module.app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_deployment_record_saved(client):
    response = client.post("/record", data={
        "version": "test-v1",
        "deployment_type": "Manual",
        "status": "Success",
        "duration": "60",
        "failure_reason": ""
    })

    assert response.status_code == 302

    records = client.get("/api/deployments").json
    assert len(records) == 1
    assert records[0]["version"] == "test-v1"
    assert records[0]["deployment_type"] == "Manual"


def test_invalid_deployment_data(client):
    response = client.post("/record", data={
        "version": "test-v2",
        "deployment_type": "Invalid",
        "status": "Success",
        "duration": "60",
        "failure_reason": ""
    })

    assert response.status_code == 400
    assert client.get("/api/deployments").json == []


def test_deployment_comparison_api(client):
    client.post("/record", data={
        "version": "manual-v1",
        "deployment_type": "Manual",
        "status": "Success",
        "duration": "120",
        "failure_reason": ""
    })

    client.post("/record", data={
        "version": "auto-v1",
        "deployment_type": "Automated",
        "status": "Success",
        "duration": "40",
        "failure_reason": ""
    })

    response = client.get("/api/deployment-comparison")

    assert response.status_code == 200

    results = {
        item["deployment_type"]: item
        for item in response.json
    }

    assert results["Manual"]["average_duration"] == 120.0
    assert results["Automated"]["average_duration"] == 40.0
