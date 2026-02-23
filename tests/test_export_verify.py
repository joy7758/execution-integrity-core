import copy
import json
import os
import subprocess
import sys
import tempfile


REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE_PATH = os.path.join(REPO_DIR, "example.py")
VERIFY_PATH = os.path.join(REPO_DIR, "verify_export.py")
EXPORT_PATH = os.path.join(REPO_DIR, "execution_log.json")


def main():
    run_example = subprocess.run(
        [sys.executable, EXAMPLE_PATH],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert run_example.returncode == 0, run_example.stdout + run_example.stderr
    assert os.path.exists(EXPORT_PATH), "execution_log.json 不存在"

    run_pass = subprocess.run(
        [sys.executable, VERIFY_PATH, EXPORT_PATH],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert run_pass.returncode == 0, run_pass.stdout + run_pass.stderr
    assert "EXPORT_VERIFY: PASS" in run_pass.stdout, run_pass.stdout + run_pass.stderr

    with open(EXPORT_PATH, "r") as f:
        payload = json.load(f)

    tampered = copy.deepcopy(payload)
    assert tampered["chain"], "chain 为空"
    tampered["chain"][0]["output"] = {"result": "Tampered in test"}

    with tempfile.TemporaryDirectory() as tmp_dir:
        tampered_path = os.path.join(tmp_dir, "tampered.json")
        with open(tampered_path, "w") as f:
            json.dump(tampered, f, indent=2)

        run_fail = subprocess.run(
            [sys.executable, VERIFY_PATH, tampered_path],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
        )

    assert run_fail.returncode != 0, run_fail.stdout + run_fail.stderr
    assert "EXPORT_VERIFY: FAIL" in run_fail.stdout, run_fail.stdout + run_fail.stderr

    print("TEST_EXPORT_VERIFY: PASS")


if __name__ == "__main__":
    main()
