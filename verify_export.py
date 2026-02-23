import json
import hashlib
import sys


def fail(message):
    print(f"EXPORT_VERIFY: FAIL ({message})")
    return 1


def verify_export(path):
    try:
        with open(path, "r") as f:
            payload = json.load(f)
    except Exception as e:
        return fail(f"cannot read file: {e}")

    if not isinstance(payload, dict):
        return fail("top-level is not an object")

    required_fields = ["spec", "version", "exported_at", "chain", "hash_alg"]
    for field in required_fields:
        if field not in payload:
            return fail(f"missing top-level field: {field}")

    if payload["hash_alg"] != "sha256":
        return fail(f"unsupported hash algorithm: {payload['hash_alg']}")

    chain = payload["chain"]
    if not isinstance(chain, list):
        return fail("chain is not a list")

    prev = "GENESIS"
    for i, entry in enumerate(chain, start=1):
        if not isinstance(entry, dict):
            return fail(f"entry {i} is not an object")

        if "hash" not in entry:
            return fail(f"entry {i} missing hash")

        if "previous_hash" not in entry:
            return fail(f"entry {i} missing previous_hash")

        expected = entry["hash"]
        temp = entry.copy()
        del temp["hash"]

        raw = json.dumps(temp, sort_keys=True).encode()
        recalculated = hashlib.sha256(raw).hexdigest()

        if recalculated != expected:
            return fail(f"entry {i} hash mismatch")

        if entry["previous_hash"] != prev:
            return fail(f"entry {i} previous_hash mismatch")

        prev = expected

    print("EXPORT_VERIFY: PASS")
    return 0


def main():
    filename = "execution_log.json"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    return verify_export(filename)


if __name__ == "__main__":
    raise SystemExit(main())
