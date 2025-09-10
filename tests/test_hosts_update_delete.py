import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_update_and_delete_host_flow(app_instance):
    with TestClient(app_instance) as client:
        # Create two profiles to validate profile change on update
        r = client.post("/profile", json={"name": "p1"})
        assert r.status_code == 201, r.text
        p1 = r.json()
        r = client.post("/profile", json={"name": "p2"})
        assert r.status_code == 201, r.text
        p2 = r.json()

        # Create a host bound to p1
        r = client.post(
            "/host",
            json={
                "hostname": "node01",
                "ip": "10.0.0.21",
                "mac": "52:54:00:aa:cc:01",
                "profile_id": p1["id"],
            },
        )
        assert r.status_code == 201, r.text
        host = r.json()
        hid = host["id"]

        # Update hostname and change profile to p2 (success)
        r = client.put(f"/host/{hid}", json={"hostname": "node01-renamed", "profile_id": p2["id"]})
        assert r.status_code == 200, r.text
        updated = r.json()
        assert updated["hostname"] == "node01-renamed"
        assert updated["profile_id"] == p2["id"]

        # Attempt to update with a non-existent profile -> 404
        r = client.put(f"/host/{hid}", json={"profile_id": 999999})
        assert r.status_code == 404

        # Delete the host -> 204
        r = client.delete(f"/host/{hid}")
        assert r.status_code == 204, r.text

        # Ensure host no longer retrievable -> 404
        r = client.get(f"/host/{hid}")
        assert r.status_code == 404

        # Deleting again should also yield 404
        r = client.delete(f"/host/{hid}")
        assert r.status_code == 404

