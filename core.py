import json
import hashlib
import time


class ExecutionIntegrityCore:
    def __init__(self):
        self.chain = []
        self.previous_hash = "GENESIS"

    def record(self, action, input_data, output_data):
        entry = {
            "timestamp": time.time(),
            "action": action,
            "input": input_data,
            "output": output_data,
            "previous_hash": self.previous_hash
        }

        raw = json.dumps(entry, sort_keys=True).encode()
        current_hash = hashlib.sha256(raw).hexdigest()

        entry["hash"] = current_hash
        self.previous_hash = current_hash
        self.chain.append(entry)

    def export(self, filename="execution_log.json"):
        with open(filename, "w") as f:
            json.dump(self.chain, f, indent=2)

    def verify(self):
        prev = "GENESIS"
        for entry in self.chain:
            expected = entry["hash"]
            temp = entry.copy()
            del temp["hash"]

            raw = json.dumps(temp, sort_keys=True).encode()
            recalculated = hashlib.sha256(raw).hexdigest()

            if recalculated != expected or entry["previous_hash"] != prev:
                return False

            prev = expected

        return True
