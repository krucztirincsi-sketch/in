from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_compile_endpoint():
    response = client.post("/compile", json={
        "intent": "test",
        "context": {"emotion": "neutral"},
        "data": [{"amount": 10}, {"amount": 20}]
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "html_bundle" in json_response
    assert "execution_plan" in json_response
    assert len(json_response["html_bundle"]) > 0
