import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_healthcheck_ok(app_instance):
    with TestClient(app_instance) as client:
        r = client.get("/healthcheck")
        assert r.status_code == 200, r.text
        assert r.json() == {"status": "OK"}

