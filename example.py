from core import ExecutionIntegrityCore

ei = ExecutionIntegrityCore()

ei.record("search", {"query": "AI regulation"}, {"result": "Found 12 documents"})
ei.record("calculate", {"expression": "2+2"}, {"result": 4})

ei.export()

print("Verification result:", ei.verify())
