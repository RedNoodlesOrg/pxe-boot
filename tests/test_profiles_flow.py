import time

import pytest
from fastapi.testclient import TestClient


def have_butane():
    import shutil

    return shutil.which("butane") is not None


async def test_profile_create_upload_download(app_instance):
    with TestClient(app_instance) as client:
        r = client.post("/profile", json={"name": "base"})
        assert r.status_code == 201, r.text
        pid = r.json()["id"]

        bu = "variant: fcos\nversion: 1.5.0\n"
        r = client.post(
            f"/profile/{pid}/upload", files={"file": ("base.bu", bu, "text/yaml")}
        )
        assert r.status_code == 200, r.text

        r = client.post("/profile", json={"name": "b+se"})
        assert r.status_code == 422, r.text

        r = client.get(f"/profile/{pid}/ignition")
        if have_butane():
            assert r.status_code == 200, r.text


@pytest.mark.asyncio
async def test_profile_rename_and_rerender(app_instance):
    with TestClient(app_instance) as client:
        # create + upload
        r = client.post("/profile", json={"name": "alpha"})
        pid = r.json()["id"]
        files = {"file": ("alpha.bu", "variant: fcos\nversion: 1.5.0\n", "text/yaml")}
        client.post(f"/profile/{pid}/upload", files=files)

        # First render (if butane present)
        r = client.get(f"/profile/{pid}/ignition")
        first_json = None
        if have_butane():
            assert r.status_code == 200, r.text
            first_json = r.text
        assert first_json is not None, r.text

        files = {
            "file": (
                "alpha.bu",
                "variant: fcos\nversion: 1.6.0\nstorage:\n  files: []\n",
                "text/yaml",
            )
        }
        client.post(f"/profile/{pid}/upload", files=files)
        time.sleep(0.1)  # ensure mtime tick

        r = client.get(f"/profile/{pid}/ignition")
        assert r.status_code == 200, r.text
        second_json = r.text
        assert second_json != first_json, r.text

        # Rename
        r = client.put(f"/profile/{pid}", json={"new_name": "alpha-renamed"})
        assert r.status_code == 200, r.text
        info = r.json()
        assert info["name"] == "alpha-renamed", r.text
        assert info["bu_path"].endswith(f"{pid}+alpha-renamed.bu"), r.text

        # Delete
        r = client.delete(f"/profile/{pid}")
        assert r.status_code == 204, r.text
