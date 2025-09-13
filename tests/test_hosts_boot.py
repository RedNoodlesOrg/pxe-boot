# tests/test_hosts_boot.py
import json
import pytest
from fastapi.testclient import TestClient
import urllib.parse

def have_butane():
    import shutil

    return shutil.which("butane") is not None


@pytest.mark.asyncio
async def test_hosts_and_boot_endpoints(app_instance):
    with TestClient(app_instance) as client:

        r = client.post("/profile", json={"name": "node"})
        prof_id = r.json()["id"]
        bu = "variant: fcos\nversion: 1.5.0\n"
        client.post(
            f"/profile/{prof_id}/upload", files={"file": ("node.bu", bu, "text/yaml")}
        )

        r = client.post(
            "/host",
            json={
                "hostname": "core01",
                "ip": "10.0.0.10",
                "mac": "52:54:00:aa:bb:01",
                "profile_id": prof_id,
            },
        )
        assert r.status_code == 201, r.text
        host = r.json()
        hid = host["id"]
        hmac = host["mac"]
        hmac_bad: str = host["mac"].replace("00", "ff")
        r = client.get(f"/ignition", params={"profile_id": prof_id})
        if have_butane():
            assert r.status_code == 200
            j = json.loads(r.text)
            assert "ignition" in j
            
        r = client.get(f"/ignition", params={"mac": hmac})
        if have_butane():
            assert r.status_code == 200
            j = json.loads(r.text)
            assert "ignition" in j


        r = client.get(f"/ignition/{hid}")
        if have_butane():
            assert r.status_code == 200
            j = json.loads(r.text)
            assert "ignition" in j
            
        r = client.get(f"/ignition")
        assert r.status_code == 400

        r = client.get(f"/ignition", params={"mac": hmac_bad})
        assert r.status_code == 404