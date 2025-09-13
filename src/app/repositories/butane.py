import json
import shutil
import subprocess


class ButaneError(RuntimeError):
    pass


def transpile_butane_to_ignition(yaml_text: str) -> str:
    """
    Calls the local `butane` binary to transpile YAML -> Ignition JSON.
    Requires `butane` in PATH. Raises ButaneError on failure.
    """
    if shutil.which("butane") is None:
        raise ButaneError("`butane` binary not found in PATH")

    proc = subprocess.run(
        ["butane", "--strict", "--pretty"],
        input=yaml_text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise ButaneError(proc.stderr.decode("utf-8") or "butane failed")

    try:
        json.loads(proc.stdout.decode("utf-8"))
    except Exception as e:
        raise ButaneError(f"Invalid Ignition JSON produced: {e}")

    return proc.stdout.decode("utf-8")
