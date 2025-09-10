import time
import pytest
from fastapi.testclient import TestClient


def have_butane():
    import shutil

    return shutil.which("butane") is not None


async def test_profile_create_upload_download(app_instance):
    with TestClient(app_instance) as client:
        r = client.post("/profile", json={"name": "base"})
        assert r.status_code == 201
        pid = r.json()["id"]

        bu = "variant: fcos\nversion: 1.5.0\n"
        r = client.post(
            f"/profile/{pid}/upload", files={"file": ("base.bu", bu, "text/yaml")}
        )
        assert r.status_code == 200

        r = client.get(f"/profile/{pid}/ignition")
        if have_butane():
            assert r.status_code == 200
        else:
            assert r.status_code in (400, 500)


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
        if have_butane():
            assert r.status_code == 200
            first_json = r.text
        else:
            pytest.skip("butane CLI not found; skipping render checks")

        # Update BU → ensure ignition refreshes (mtime changes)
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
        assert r.status_code == 200
        second_json = r.text
        assert second_json != first_json

        # Rename
        r = client.put(f"/profile/{pid}", json={"new_name": "alpha-renamed"})
        assert r.status_code == 200
        info = r.json()
        assert info["name"] == "alpha-renamed"
        assert info["bu_path"].endswith(f"{pid}+alpha-renamed.bu")

        # Delete
        r = client.delete(f"/profile/{pid}")
        assert r.status_code == 204
